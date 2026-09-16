#!/usr/bin/env python3
"""
Bands in Bend — weekly show fetcher.

Pulls upcoming live-music listings for one Monday–Sunday week from several
public sources, normalizes venue names against venues.html, dedupes across
sources, and writes a draft shows.js plus a review report.

    python3 scripts/fetch_shows.py                 # next Monday's week
    python3 scripts/fetch_shows.py --week 2026-09-21
    python3 scripts/fetch_shows.py --week 2026-09-14 --compare shows.js

Outputs (default dir: drafts/):
    shows-YYYY-MM-DD.js   ready-to-review draft in the exact shows.js format
    report-YYYY-MM-DD.md  where each show came from, unknown venues, gaps

Sources (each is best-effort; a failing source is reported, not fatal):
    bendsource   community.bendsource.com day listings, "Live Music" category
    bulletin     Bend Bulletin "Where to find live music in Central Oregon"
    eventbrite   eventbrite.com Bend music search
    jsonld       schema.org Event blocks on venue sites (see VENUE_PAGES)
    squarespace  Squarespace event lists on venue sites (see VENUE_PAGES)
    ics          iCalendar feeds (e.g. Silver Moon's Facebook-events widget export)
    playwright   JS-rendered venue pages (Tower Theatre) — needs the optional
                 Playwright install below; skipped with a note if it's missing

Stdlib only for everything except the playwright sources. To enable those:
    pip3 install --user playwright && python3 -m playwright install chromium
"""

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import sys
import urllib.request
import urllib.error
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TZ = ZoneInfo("America/Los_Angeles")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

# Venue pages with machine-readable events. Add more as they're discovered.
# kind: "jsonld" (schema.org Event blocks), "squarespace" (eventlist markup),
#       "ics" (iCalendar feed), or "playwright" (JS-rendered; needs a "parser")
VENUE_PAGES = [
    {"kind": "jsonld", "venue": "Volcanic Theatre Pub", "url": "https://volcanictheatre.com/calendar"},
    {"kind": "squarespace", "venue": "Worthy Brewing", "url": "https://www.worthy.beer/events"},
    # Silver Moon's site embeds a SociableKIT widget of their Facebook events; it exports ICS.
    {"kind": "ics", "venue": "Silver Moon Brewing", "url": "https://data.accentapi.com/widget_export_calendar/105713"},
    # Tower's Webflow CMS list is loaded client-side, so it has to be rendered.
    {"kind": "playwright", "parser": "tower_webflow", "venue": "Tower Theatre", "url": "https://www.towertheatre.org/events/"},
]

# Tower Theatre category tags that mean "a concert" (skips Movies, Speakers, Dance, Comedy…)
TOWER_MUSIC_CATS = {"Concerts", "Rock/Pop", "Country/Folk", "Global", "Classical/Chamber", "R&B", "Jazz", "Blues"}

BENDSOURCE_LIVE_MUSIC = "2176893"   # eventCategory id for "Live Music"

# Listings that show up in "live music" feeds but aren't shows.
EXCLUDE = re.compile(
    r"\b(karaoke|trivia|bingo|football|watch party|comedy|film|movie|"
    r"dance class|lessons?|workshop|registration|drag brunch|yoga|worship|scripture|"
    r"support group|ward |church)\b", re.I)

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
BIG_ROOMS = ["Hayden Homes Amphitheater", "Midtown Ballroom", "Tower Theatre",
             "The Domino Room", "Volcanic Theatre Pub", "Silver Moon Brewing"]


# ────────────────────────────── fetching ──────────────────────────────

class Fetcher:
    def __init__(self, cache_dir, use_cache=True):
        self.cache_dir = cache_dir
        self.use_cache = use_cache
        os.makedirs(cache_dir, exist_ok=True)

    def _path(self, key):
        return os.path.join(self.cache_dir, hashlib.sha1(key.encode()).hexdigest())

    def get_cached(self, key):
        p = self._path(key)
        return open(p, encoding="utf-8").read() if self.use_cache and os.path.exists(p) else None

    def put_cached(self, key, body):
        with open(self._path(key), "w", encoding="utf-8") as fh:
            fh.write(body)

    def get(self, url, timeout=30):
        path = self._path(url)
        if self.use_cache and os.path.exists(path):
            return open(path, encoding="utf-8").read()
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8", "replace")
        with open(path, "w", encoding="utf-8") as f:
            f.write(body)
        return body


# ────────────────────────────── helpers ──────────────────────────────

def strip_tags(s):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.S)
    s = re.sub(r"<br\s*/?>|</p>|</div>|</li>|</h\d>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s)


def clean(s):
    s = html.unescape(s or "")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip()


TIME_RE = re.compile(
    r"\b(noon|midnight|(\d{1,2})(?::(\d{2}))?\s*(a\.?m\.?|p\.?m\.?)?)"
    r"(?:\s*[-–]\s*(noon|midnight|(\d{1,2})(?::(\d{2}))?\s*(a\.?m\.?|p\.?m\.?)))?", re.I)


def parse_start_time(text):
    """Return ('6pm', minutes_since_midnight) for the first time found in text."""
    if not text:
        return None, None
    m = TIME_RE.search(text)
    if not m:
        return None, None
    word, h, mm, ap, _, _, _, ap2 = m.groups()
    if word and word.lower() in ("noon", "midnight"):
        return ("12pm", 12 * 60) if word.lower() == "noon" else ("12am", 0)
    if h is None:
        return None, None
    ap = (ap or ap2 or "").lower().replace(".", "")
    if not ap:
        return None, None            # bare number without am/pm — too ambiguous
    hour = int(h) % 12 + (12 if ap == "pm" else 0)
    label = f"{int(h)}{':' + mm if mm and mm != '00' else ''}{ap}"
    return label, hour * 60 + int(mm or 0)


def norm(s):
    s = clean(s).lower()
    s = re.sub(r"&", " and ", s)
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = re.sub(r"\b(the|at|pub|bar|and|co|company|brewing|brewery|inc|llc)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()


class VenueMap:
    """Map raw venue strings to the canonical names used in venues.html."""

    def __init__(self, canonical, aliases):
        self.canonical = list(canonical)
        self.by_norm = {norm(c): c for c in canonical}
        self.aliases = {clean(k).lower(): v for k, v in aliases.items()}
        self.unknown = {}

    def resolve(self, raw):
        raw_c = clean(raw)
        if not raw_c:
            return None
        low = raw_c.lower()
        if low in self.aliases:
            return self.aliases[low]
        n = norm(raw_c)
        if n in self.by_norm:
            return self.by_norm[n]
        for cn, c in self.by_norm.items():
            if len(n) >= 5 and len(cn) >= 5 and (n in cn or cn in n):
                return c
        self.unknown[raw_c] = self.unknown.get(raw_c, 0) + 1
        return None


def load_canonical_venues():
    path = os.path.join(ROOT, "venues.html")
    h = open(path, encoding="utf-8").read()
    return [clean(v) for v in re.findall(r'class="venue-name">([^<]*)<', h)]


def load_aliases():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venue_aliases.json")
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}


class Show:
    def __init__(self, date, artist, venue_raw, time_label, minutes, source, url=""):
        self.date = date
        self.artist = clean(artist)
        self.venue_raw = clean(venue_raw)
        self.venue = None
        self.time = time_label
        self.minutes = minutes
        self.sources = {source}
        self.url = url

    def __repr__(self):
        return f"{self.date} {self.artist} @ {self.venue or self.venue_raw} {self.time} [{','.join(self.sources)}]"


def strip_venue_from_artist(artist, venue_raw, venue_canon):
    """'The Jugulars live at Northside Bar & Grill!' -> 'The Jugulars'"""
    a = artist.strip().rstrip("!").strip()
    names = [n for n in (venue_raw, venue_canon) if n]
    for v in names:
        first = norm(v).split(" ")[0] if norm(v) else ""
        if not first:
            continue
        m = re.search(r"\s+[-–|]?\s*(live\s+(music\s+)?)?(@|at)\s+(the\s+)?" + re.escape(first), a, re.I)
        if m:
            a = a[:m.start()].strip()
    a = re.sub(r"\s*[-–|:]\s*(live music|live at .*|live)$", "", a, flags=re.I).strip(" -–|")
    return a or artist


def titlecase_if_shouting(s):
    """Facebook event names often arrive ALL CAPS; make them readable for the draft."""
    letters = [c for c in s if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.9:
        small = {"a", "an", "and", "at", "by", "for", "in", "of", "on", "or", "the", "to", "w", "with", "ft", "feat"}
        words = s.lower().split(" ")
        out = []
        for i, w in enumerate(words):
            core = re.sub(r"[^a-z0-9']", "", w)
            if i and core in small:
                out.append(w)
            elif w.startswith("dj") and len(w) <= 3:
                out.append("DJ")
            else:
                out.append(w[:1].upper() + w[1:])
        return " ".join(out)
    return s


def parse_ics(text):
    """Yield (datetime_local, summary, url) for each VEVENT in an iCalendar feed."""
    text = re.sub(r"\r?\n[ \t]", "", text)          # unfold continuation lines
    for block in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", text, re.S):
        props = {}
        for line in block.strip().split("\n"):
            if ":" not in line:
                continue
            key, _, val = line.partition(":")
            name, _, params = key.partition(";")
            props[name.upper()] = (params, val.strip())
        if "DTSTART" not in props:
            continue
        params, val = props["DTSTART"]
        m = re.match(r"(\d{4})(\d{2})(\d{2})(?:T(\d{2})(\d{2})(\d{2})?)?(Z?)", val)
        if not m:
            continue
        y, mo, d, hh, mm, ss, z = m.groups()
        when = dt.datetime(int(y), int(mo), int(d), int(hh or 0), int(mm or 0))
        if z:
            when = when.replace(tzinfo=dt.timezone.utc).astimezone(TZ)
        else:
            tzid = re.search(r"TZID=([^;]+)", params)
            try:
                when = when.replace(tzinfo=ZoneInfo(tzid.group(1)) if tzid else TZ).astimezone(TZ)
            except Exception:
                when = when.replace(tzinfo=TZ)
        summary = html.unescape(props.get("SUMMARY", ("", ""))[1]).replace("\\,", ",").replace("\\;", ";")
        yield when, summary, props.get("URL", ("", ""))[1]


def render_with_playwright(url, log, scrolls=8):
    """Return fully rendered HTML, or None (with a logged hint) if Playwright isn't installed."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        log("playwright not installed — skipping JS-rendered venue pages "
            "(pip3 install --user playwright && python3 -m playwright install chromium)")
        return None
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent=UA)
        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(1500)
        for _ in range(scrolls):
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(400)
        content = page.content()
        browser.close()
    return content


def parse_tower_webflow(h, lo, hi):
    """Tower Theatre's Webflow CMS list: cards with name, 'Sep 17' @ '7:30 pm', category tags."""
    out = []
    cards = re.split(r'<div role="listitem" class="upcoming_events_list_item', h)[1:]
    for c in cards:
        name = re.search(r'fs-cmsfilter-field="event-name"[^>]*>([^<]*)', c)
        if not name:
            continue
        cats = set(html.unescape(x) for x in re.findall(r'fs-cmsfilter-field="category"[^>]*>([^<]*)', c))
        if not (cats & TOWER_MUSIC_CATS):
            continue
        ex = re.findall(r'class="events_card-extract">([^<]*)<', c)
        if len(ex) < 2:
            continue
        href = re.search(r'href="(/event/[^"]*)"', c)
        yr = re.search(r"-(\d{1,2})-(\d{1,2})-(\d{2})(?:-|$|\")", href.group(1) + '"') if href else None
        try:
            md = dt.datetime.strptime(ex[0].strip(), "%b %d")
        except ValueError:
            continue
        year = 2000 + int(yr.group(3)) if yr else lo.year
        d = dt.date(year, md.month, md.day)
        if not (lo <= d <= hi):
            continue
        label, minutes = parse_start_time(ex[1])
        out.append((d, clean(name.group(1)), label, minutes, "https://www.towertheatre.org" + href.group(1) if href else ""))
    return out


PLAYWRIGHT_PARSERS = {"tower_webflow": parse_tower_webflow}


# ────────────────────────────── sources ──────────────────────────────

def src_bendsource(f, days, log):
    shows = []
    for d in days:
        seen = set()
        for page in range(1, 6):
            url = (f"https://community.bendsource.com/bend/EventSearch?narrowByDate={d.isoformat()}"
                   f"&eventCategory={BENDSOURCE_LIVE_MUSIC}&page={page}")
            try:
                h = f.get(url)
            except Exception as e:
                log(f"bendsource {d}: {e}")
                break
            blocks = re.findall(r'fdn-event-search-text-block(.*?)(?:fdn-teaser-tag-link-block|</li>)', h, re.S)
            new = 0
            for b in blocks:
                t = re.search(r'fdn-teaser-headline[^>]*>\s*<a href="([^"]*)"[^>]*>([^<]*)', b)
                if not t:
                    continue
                oid = re.search(r"oid=(\d+)", t.group(1))
                oid = oid.group(1) if oid else t.group(2)
                if oid in seen:
                    continue
                seen.add(oid)
                new += 1
                title = clean(t.group(2))
                when = re.search(r'fdn-teaser-subheadline">\s*(.*?)\s*</p>', b, re.S)
                when = clean(when.group(1)) if when else ""
                ven = re.search(r'fdn-event-teaser-location-link"[^>]*>([^<]*)', b)
                ven = clean(ven.group(1)) if ven else ""
                if EXCLUDE.search(title):
                    continue
                # multi-date strings: take the time chunk that follows this day's date
                chunk = when
                mon = d.strftime("%b").replace("Sep", "Sept")
                m = re.search(rf"{mon}\.? {d.day}\b,?\s*([^,]*(?:,\s*)?[^,]*)", when)
                if m:
                    chunk = m.group(1)
                label, minutes = parse_start_time(chunk)
                shows.append(Show(d, title, ven, label, minutes, "bendsource", t.group(1)))
            if new == 0:
                break
    return shows


def src_bulletin(f, days, log):
    shows = []
    url = ("https://bendbulletin.com/wp-json/wp/v2/posts?search=%22live%20music%20in%20Central%20Oregon%22"
           "&per_page=6&orderby=date&_fields=date,link,title,content")
    try:
        posts = json.loads(f.get(url))
    except Exception as e:
        log(f"bulletin: {e}")
        return shows
    want = {d for d in days}
    used = []
    for p in posts:
        title = clean(p["title"]["rendered"])
        if not re.search(r"where to find live music", title, re.I):
            continue
        pub = dt.date.fromisoformat(p["date"][:10])
        text = strip_tags(p["content"]["rendered"])
        cur = None
        hit = 0
        for line in (clean(l) for l in text.split("\n")):
            m = re.match(r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+(\d{1,2})/(\d{1,2})\b", line)
            if m:
                mo, da = int(m.group(2)), int(m.group(3))
                yr = pub.year + (1 if mo < pub.month - 6 else 0)
                cur = dt.date(yr, mo, da)
                continue
            if cur is None or cur not in want or ":" not in line:
                continue
            head, _, rest = line.partition(":")
            segs = [s.strip() for s in rest.split(";")]
            time_seg = next((s for s in segs if TIME_RE.search(s) and re.search(r"[ap]\.?m|noon", s, re.I)), "")
            venue = ""
            for s in segs:
                if s is time_seg or not s:
                    continue
                if re.search(r",\s*(Bend|Redmond|Sisters|Sunriver|La Pine|Tumalo|Prineville|Madras|Powell Butte|Terrebonne|Culver)$", s):
                    venue = s.split(",")[0].strip()
                    break
            if not venue or EXCLUDE.search(head):
                continue
            label, minutes = parse_start_time(time_seg)
            shows.append(Show(cur, head, venue, label, minutes, "bulletin", p["link"]))
            hit += 1
        if hit:
            used.append(f"{title} ({hit})")
    log("bulletin issues used: " + ("; ".join(used) if used else "none matched this week"))
    return shows


def src_eventbrite(f, days, log):
    shows = []
    lo, hi = days[0], days[-1]
    for page in range(1, 4):
        url = (f"https://www.eventbrite.com/d/or--bend/music--events/?page={page}"
               f"&start_date={lo.isoformat()}&end_date={hi.isoformat()}")
        try:
            h = f.get(url)
        except Exception as e:
            log(f"eventbrite p{page}: {e}")
            break
        i = h.find("window.__SERVER_DATA__ = ")
        if i < 0:
            break
        try:
            sd, _ = json.JSONDecoder().raw_decode(h[i + len("window.__SERVER_DATA__ = "):])
        except Exception as e:
            log(f"eventbrite p{page}: bad JSON ({e})")
            break
        results = []

        def walk(o, depth=0):
            if depth > 5:
                return
            if isinstance(o, dict):
                for k, v in o.items():
                    if k == "results" and isinstance(v, list) and v and isinstance(v[0], dict) and "start_date" in v[0]:
                        results.extend(v)
                    else:
                        walk(v, depth + 1)
            elif isinstance(o, list):
                for v in o:
                    walk(v, depth + 1)
        walk(sd)
        if not results:
            break
        for r in results:
            try:
                d = dt.date.fromisoformat(r["start_date"])
            except Exception:
                continue
            if not (lo <= d <= hi):
                continue
            name = clean(r.get("name", ""))
            tags = {t.get("tag", "") for t in (r.get("tags") or []) if isinstance(t, dict)}
            # 103 = Music; 3016 = Religious/Spiritual (church calendars mis-tag as Music)
            if "EventbriteCategory/103" not in tags or "EventbriteSubCategory/3016" in tags or EXCLUDE.search(name):
                continue
            ven = ((r.get("primary_venue") or {}).get("name")) or ""
            st = r.get("start_time") or ""
            label, minutes = None, None
            if re.match(r"^\d{2}:\d{2}$", st):
                hh, mm = map(int, st.split(":"))
                label = f"{hh % 12 or 12}{':' + st[3:] if mm else ''}{'pm' if hh >= 12 else 'am'}"
                minutes = hh * 60 + mm
            shows.append(Show(d, name, ven, label, minutes, "eventbrite", r.get("url", "")))
    return shows


def _iter_jsonld(h):
    for m in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S):
        try:
            d = json.loads(m)
        except Exception:
            continue
        items = d if isinstance(d, list) else d.get("@graph", [d]) if isinstance(d, dict) else []
        for it in items:
            if isinstance(it, dict) and it.get("@type") in ("Event", "MusicEvent"):
                yield it


def src_venue_pages(f, days, log):
    shows = []
    lo, hi = days[0], days[-1]
    for vp in VENUE_PAGES:
        try:
            if vp["kind"] == "playwright":
                key = "pw:" + vp["url"]
                h = f.get_cached(key) or render_with_playwright(vp["url"], log)
                if h is None:
                    continue
                f.put_cached(key, h)
            else:
                h = f.get(vp["url"])
        except Exception as e:
            log(f"{vp['venue']}: {e}")
            continue
        n = 0
        if vp["kind"] == "ics":
            for when, summary, url in parse_ics(h):
                d = when.date()
                if not (lo <= d <= hi):
                    continue
                name = titlecase_if_shouting(clean(summary))
                if EXCLUDE.search(name):
                    continue
                label = f"{when.hour % 12 or 12}{':' + when.strftime('%M') if when.minute else ''}{'pm' if when.hour >= 12 else 'am'}"
                shows.append(Show(d, name, vp["venue"], label, when.hour * 60 + when.minute, "venue-site", url or vp["url"]))
                n += 1
        elif vp["kind"] == "playwright":
            for d, name, label, minutes, url in PLAYWRIGHT_PARSERS[vp["parser"]](h, lo, hi):
                if EXCLUDE.search(name):
                    continue
                shows.append(Show(d, name, vp["venue"], label, minutes, "venue-site", url))
                n += 1
        elif vp["kind"] == "jsonld":
            for it in _iter_jsonld(h):
                sd = it.get("startDate") or ""
                try:
                    when = dt.datetime.fromisoformat(sd.replace("Z", "+00:00"))
                    if when.tzinfo:
                        when = when.astimezone(TZ)
                except Exception:
                    continue
                d = when.date()
                if not (lo <= d <= hi):
                    continue
                name = clean(it.get("name", ""))
                if EXCLUDE.search(name):
                    continue
                label = f"{when.hour % 12 or 12}{':' + when.strftime('%M') if when.minute else ''}{'pm' if when.hour >= 12 else 'am'}"
                shows.append(Show(d, name, vp["venue"], label, when.hour * 60 + when.minute, "venue-site", it.get("url", vp["url"])))
                n += 1
        elif vp["kind"] == "squarespace":
            for a in re.findall(r'<article class="eventlist-event[^"]*">(.*?)</article>', h, re.S):
                t = re.search(r'eventlist-title-link[^>]*>([^<]*)', a)
                dm = re.search(r'<time class="event-date" datetime="(\d{4}-\d{2}-\d{2})"', a)
                if not (t and dm):
                    continue
                d = dt.date.fromisoformat(dm.group(1))
                if not (lo <= d <= hi):
                    continue
                name = clean(t.group(1))
                if EXCLUDE.search(name):
                    continue
                st = re.search(r'event-time-localized-start[^>]*>([^<]*)', a) or re.search(r'event-time-12hr-start[^>]*>([^<]*)', a)
                label, minutes = parse_start_time(st.group(1) if st else "")
                shows.append(Show(d, name, vp["venue"], label, minutes, "venue-site", vp["url"]))
                n += 1
        log(f"{vp['venue']}: {n} in range")
    return shows


SOURCES = [("bendsource", src_bendsource), ("bulletin", src_bulletin),
           ("eventbrite", src_eventbrite), ("venue-site", src_venue_pages)]
PRIORITY = {"bulletin": 0, "venue-site": 1, "bendsource": 2, "eventbrite": 3}


# ────────────────────────────── merge ──────────────────────────────

def artist_tokens(a):
    stop = {"live", "music", "with", "band", "trio", "duo", "night", "presents", "featuring", "feat", "show", "tour", "the", "and"}
    return {t for t in re.findall(r"[a-z0-9]+", a.lower()) if len(t) >= 3 and t not in stop}


def same_show(a, b):
    if a.date != b.date or a.venue != b.venue:
        return False
    ta, tb = artist_tokens(a.artist), artist_tokens(b.artist)
    if not ta or not tb:
        return norm(a.artist) == norm(b.artist)
    if ta & tb:
        return True
    na, nb = norm(a.artist), norm(b.artist)
    return bool(na and nb and (na in nb or nb in na))


def merge(shows):
    out = []
    for s in sorted(shows, key=lambda x: PRIORITY[next(iter(x.sources))]):
        for o in out:
            if same_show(s, o):
                o.sources |= s.sources
                if o.time is None and s.time:
                    o.time, o.minutes = s.time, s.minutes
                break
        else:
            out.append(s)
    return out


# ────────────────────────────── output ──────────────────────────────

def js_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def fmt_week_label(days):
    a, b = days[0], days[-1]
    if a.month == b.month:
        return f"{a.strftime('%B')} {a.day} – {b.day}"
    return f"{a.strftime('%B')} {a.day} – {b.strftime('%B')} {b.day}"


def write_draft(path, days, shows, unknown_flags):
    by_day = {d: [] for d in days}
    for s in shows:
        by_day[s.date].append(s)
    lines = ["// ─────────────────────────────────────────────",
             "// BANDS IN BEND — Weekly Show Data (DRAFT, auto-fetched)",
             "// Review against Instagram/venue pages, then copy over shows.js",
             "// ─────────────────────────────────────────────", "",
             "const WEEK = {", f"  label: {js_str(fmt_week_label(days))},",
             f"  year: {js_str(str(days[0].year))},", "};", "", "const SHOWS = ["]
    for d in days:
        items = by_day[d]
        if not items:
            continue
        lines += ["  {", f"    day: {js_str(DAY_NAMES[d.weekday()])},",
                  f"    date: {js_str(d.strftime('%B ') + str(d.day))},", "    shows: ["]
        for s in sorted(items, key=lambda x: (x.minutes if x.minutes is not None else 9999, x.artist.lower())):
            v = s.venue or s.venue_raw
            note = ""
            if not s.venue:
                note = "  // UNKNOWN VENUE — check spelling / add to venues.html"
            elif s.time is None:
                note = "  // TIME MISSING"
            lines.append(f"      {{ artist: {js_str(s.artist)}, venue: {js_str(v)}, time: {js_str(s.time or '?')} }},{note}")
        lines += ["    ],", "  },"]
    lines += ["];", "", "// Highlights shown on the cover — pick 4-5 (auto-suggested from bigger rooms)", "const HIGHLIGHTS = ["]
    picks = []
    for d in days:
        for s in sorted(by_day[d], key=lambda x: BIG_ROOMS.index(x.venue) if x.venue in BIG_ROOMS else 99):
            if s.venue in BIG_ROOMS and len(picks) < 5 and not any(p.date == d for p in picks):
                picks.append(s)
    for p in picks:
        lines.append(f"  {{ artist: {js_str(p.artist)}, day: {js_str(p.date.strftime('%a %b ') + str(p.date.day))} }},")
    lines += ["];", ""]
    open(path, "w", encoding="utf-8").write("\n".join(lines))


def write_report(path, days, shows, raw_counts, vmap, logs, compare):
    L = [f"# Fetch report — week of {days[0]} to {days[-1]}", ""]
    L.append(f"**{len(shows)} shows after merge** (raw: " + ", ".join(f"{k} {v}" for k, v in raw_counts.items()) + ")")
    L.append("")
    L.append("| Day | Shows | Only 1 source |")
    L.append("|---|---|---|")
    for d in days:
        items = [s for s in shows if s.date == d]
        single = sum(1 for s in items if len(s.sources) == 1)
        L.append(f"| {DAY_NAMES[d.weekday()]} {d.month}/{d.day} | {len(items)} | {single} |")
    L.append("")
    if vmap.unknown:
        L.append("## Unknown venues (add an alias in scripts/venue_aliases.json, or a card in venues.html)")
        L.append("")
        for v, n in sorted(vmap.unknown.items(), key=lambda x: -x[1]):
            L.append(f"- **{v}** ×{n}")
        L.append("")
    if compare:
        L += compare
    L.append("## Every show, with sources")
    L.append("")
    for d in days:
        L.append(f"### {DAY_NAMES[d.weekday()]} {d.month}/{d.day}")
        for s in sorted([s for s in shows if s.date == d], key=lambda x: (x.minutes or 9999, x.artist.lower())):
            flag = "" if s.venue else " ⚠️ unknown venue"
            L.append(f"- {s.time or '?'} — **{s.artist}** — {s.venue or s.venue_raw}{flag} · _{', '.join(sorted(s.sources))}_" + (f" · [link]({s.url})" if s.url else ""))
        L.append("")
    L.append("## Source log")
    L.append("")
    L += [f"- {l}" for l in logs]
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")


def load_shows_js(path):
    """Parse an existing shows.js (regex, no node needed) -> list of (date, artist, venue)."""
    src = open(path, encoding="utf-8").read()
    year = re.search(r'year:\s*"(\d{4})"', src)
    year = int(year.group(1)) if year else dt.date.today().year
    out = []
    for m in re.finditer(r'date:\s*"([A-Za-z]+ \d+)",\s*shows:\s*\[(.*?)\]', src, re.S):
        d = dt.datetime.strptime(f"{m.group(1)} {year}", "%B %d %Y").date()
        for a, v, t in re.findall(r'artist:\s*"((?:[^"\\]|\\.)*)",\s*venue:\s*"((?:[^"\\]|\\.)*)",\s*time:\s*"((?:[^"\\]|\\.)*)"', m.group(2)):
            out.append((d, a.replace('\\"', '"'), v.replace('\\"', '"'), t))
    return out


def compare_with(existing, shows, vmap):
    L = ["## Comparison with existing shows.js", ""]
    found = 0
    missed = []
    for d, a, v, t in existing:
        ven = vmap.resolve(v) or v
        probe = Show(d, a, v, t, None, "x")
        probe.venue = ven
        if any(same_show(probe, s) for s in shows):
            found += 1
        else:
            missed.append(f"- {DAY_NAMES[d.weekday()][:3]} {d.month}/{d.day} {t} — {a} — {v}")
    extra = []
    for s in shows:
        probe_hits = False
        for d, a, v, t in existing:
            p = Show(d, a, v, t, None, "x")
            p.venue = vmap.resolve(v) or v
            if same_show(p, s):
                probe_hits = True
                break
        if not probe_hits:
            extra.append(f"- {DAY_NAMES[s.date.weekday()][:3]} {s.date.month}/{s.date.day} {s.time or '?'} — {s.artist} — {s.venue or s.venue_raw} · _{', '.join(sorted(s.sources))}_")
    L.append(f"**Recall: {found}/{len(existing)}** of the posted shows were found automatically.")
    L.append("")
    L.append(f"### Missed by the fetcher ({len(missed)})")
    L += missed or ["- none"]
    L.append("")
    L.append(f"### Found by the fetcher but not in shows.js ({len(extra)})")
    L += extra or ["- none"]
    L.append("")
    return L


# ────────────────────────────── main ──────────────────────────────

def next_monday(today=None):
    today = today or dt.date.today()
    return today + dt.timedelta(days=(7 - today.weekday()) % 7 or 7)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--week", help="Monday of the target week (YYYY-MM-DD). Default: next Monday.")
    ap.add_argument("--out", default=os.path.join(ROOT, "drafts"), help="output directory (default: drafts/)")
    ap.add_argument("--compare", help="path to a shows.js for the same week; adds a recall section to the report")
    ap.add_argument("--no-cache", action="store_true", help="re-download everything (cache lives in drafts/.cache)")
    ap.add_argument("--only", help="comma-separated source names to run (bendsource,bulletin,eventbrite,venue-site)")
    args = ap.parse_args()

    monday = dt.date.fromisoformat(args.week) if args.week else next_monday()
    if monday.weekday() != 0:
        monday -= dt.timedelta(days=monday.weekday())
        print(f"note: --week adjusted to Monday {monday}")
    days = [monday + dt.timedelta(days=i) for i in range(7)]
    os.makedirs(args.out, exist_ok=True)
    f = Fetcher(os.path.join(args.out, ".cache"), use_cache=not args.no_cache)

    logs = []

    def log(msg):
        logs.append(msg)
        print("  " + msg)

    vmap = VenueMap(load_canonical_venues(), load_aliases())
    raw, counts = [], {}
    only = set(args.only.split(",")) if args.only else None
    for name, fn in SOURCES:
        if only and name not in only:
            continue
        print(f"[{name}]")
        try:
            got = fn(f, days, log)
        except Exception as e:
            log(f"{name} failed: {e}")
            got = []
        counts[name] = len(got)
        raw += got
        print(f"  {len(got)} listings")

    for s in raw:
        s.venue = vmap.resolve(s.venue_raw)
        s.artist = strip_venue_from_artist(s.artist, s.venue_raw, s.venue)
    shows = merge(raw)

    compare = None
    if args.compare:
        compare = compare_with(load_shows_js(args.compare), shows, vmap)

    tag = monday.isoformat()
    draft = os.path.join(args.out, f"shows-{tag}.js")
    report = os.path.join(args.out, f"report-{tag}.md")
    write_draft(draft, days, shows, vmap.unknown)
    write_report(report, days, shows, counts, vmap, logs, compare)

    print(f"\n{len(shows)} shows → {os.path.relpath(draft, ROOT)}")
    print(f"report     → {os.path.relpath(report, ROOT)}")
    if vmap.unknown:
        print(f"{len(vmap.unknown)} unknown venue name(s) — see report")
    if compare:
        print(next(l for l in compare if l.startswith("**Recall")))


if __name__ == "__main__":
    main()
