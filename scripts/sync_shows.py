#!/usr/bin/env python3
"""
Bands in Bend — sync shows.js from Bri's approved-shows feed.

Reads the public, read-only calendar the Desk publishes, maps venue names onto
the canonical names used by venues.html, and rewrites shows.js for that week.

    python3 scripts/sync_shows.py                   # next Monday's week
    python3 scripts/sync_shows.py --week 2026-10-05
    python3 scripts/sync_shows.py --dry-run         # show what would change
    python3 scripts/sync_shows.py --strict          # stop if a venue is unknown

Then review `git diff shows.js`, commit, push. Nothing is sent anywhere and the
site stays static — this only rewrites a data file.

The feed returns ONLY shows Bri has approved onto the calendar; anything still
awaiting review or marked 👎 is excluded upstream. Re-run it whenever she makes
changes and the site picks them up on the next push.

Venue names: the feed emits display names ("Niblicks", "The Capital"). The site
needs the exact names on the venues.html cards, so every venue is resolved via
scripts/venue_aliases.json. Unknown venues are reported loudly — add an alias
line, or add a venue card, before committing.

Artist names and times are written through exactly as the feed provides them,
per the project's weekly-update rules. Only venue names are corrected.

Stdlib only.
"""

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))

FEED = "https://bands-in-bend-desk.geland.workers.dev/api/v1/approved-events"
TIMEOUT = 30
RETRIES = 3

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# ────────────────────────────── text helpers ──────────────────────────────

def clean(s):
    s = html.unescape(s or "")
    return re.sub(r"\s+", " ", s).strip()


def norm(s):
    """Loose key for venue matching: lowercase, strip punctuation and filler words."""
    s = clean(s).lower()
    s = re.sub(r"\(.*?\)", " ", s)           # drop "(Eagle Crest)", "(La Pine)" etc.
    s = re.sub(r"&", " and ", s)
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = re.sub(r"\b(the|at|on|pub|bar|and|co|company|brewing|brewery|inc|llc)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def js_str(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


_TIME = re.compile(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", re.I)


def sort_minutes(time_label):
    """Minutes-since-midnight of a listing's start time, for ordering within a day."""
    t = (time_label or "").strip().lower()
    if not t:
        return 9999
    if t.startswith("noon"):
        return 12 * 60
    m = _TIME.search(t)
    if not m:
        return 9999
    hour, minute, ap = int(m.group(1)), int(m.group(2) or 0), m.group(3)
    if not ap:
        # "12-8pm" / "7-9pm": the meridiem belongs to the end of the range.
        tail = re.search(r"(am|pm)", t)
        ap = tail.group(1) if tail else "pm"
        # A range that starts at 12 and ends pm runs from noon, not midnight.
        if hour == 12 and ap == "pm":
            return 12 * 60
        # "7-9pm" starting before the end hour is still pm; "11am-2pm" stays am.
        end = re.search(r"[-–]\s*(\d{1,2})", t)
        if end and ap == "pm" and hour > int(end.group(1)):
            ap = "am"
    hour = hour % 12 + (12 if ap == "pm" else 0)
    return hour * 60 + minute


# ────────────────────────────── venues ──────────────────────────────

class VenueMap:
    """Resolve feed venue strings to the exact names used on venues.html cards."""

    def __init__(self, canonical, aliases):
        self.cards = list(canonical)
        self.by_norm = {}
        for c in canonical:
            self.by_norm.setdefault(norm(c), c)
        self.aliases = {clean(k).lower(): v for k, v in aliases.items() if not k.startswith("_")}
        self.unknown = {}
        self.applied = {}

    def resolve(self, raw):
        raw_c = clean(raw)
        if not raw_c:
            return None
        hit = self.aliases.get(raw_c.lower())
        if not hit:
            n = norm(raw_c)
            hit = self.by_norm.get(n)
            if not hit:
                for cn, c in self.by_norm.items():
                    if len(n) >= 5 and len(cn) >= 5 and (n in cn or cn in n):
                        hit = c
                        break
        if not hit:
            self.unknown[raw_c] = self.unknown.get(raw_c, 0) + 1
            return None
        if hit != raw_c:
            self.applied[raw_c] = hit
        return hit

    def has_card(self, name):
        return name in self.cards


def load_canonical_venues():
    h = open(os.path.join(ROOT, "venues.html"), encoding="utf-8").read()
    return [clean(v) for v in re.findall(r'class="venue-name">([^<]*)<', h)]


def load_aliases():
    p = os.path.join(HERE, "venue_aliases.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


# ────────────────────────────── feed ──────────────────────────────

def fetch_feed(monday, url=FEED):
    full = f"{url}?week_start={monday.isoformat()}"
    last = None
    for attempt in range(1, RETRIES + 1):
        try:
            req = urllib.request.Request(full, headers={
                "User-Agent": "bands-in-bend-sync/1.0", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                if r.status != 200:
                    raise RuntimeError(f"HTTP {r.status}")
                return json.loads(r.read().decode("utf-8")), full
        except Exception as e:                       # noqa: BLE001 - report, then retry
            last = e
            if attempt < RETRIES:
                print(f"  feed attempt {attempt} failed ({e}); retrying…")
    raise SystemExit(f"ERROR: could not read the feed after {RETRIES} tries: {last}\n"
                     f"       {full}\n"
                     f"       shows.js was NOT changed.")


def validate(data, monday):
    if not isinstance(data, dict):
        raise SystemExit("ERROR: feed did not return a JSON object. shows.js was NOT changed.")
    got = data.get("week_start")
    if got and got != monday.isoformat():
        raise SystemExit(f"ERROR: asked for week_start={monday.isoformat()} but the feed "
                         f"returned {got}. shows.js was NOT changed.")
    events = data.get("events")
    if not isinstance(events, list):
        raise SystemExit("ERROR: feed has no 'events' list. shows.js was NOT changed.")
    for e in events:
        for field in ("event_date", "artist", "venue", "time"):
            if not e.get(field):
                raise SystemExit(f"ERROR: an event is missing '{field}': "
                                 f"{json.dumps(e)[:200]}\n       shows.js was NOT changed.")
    return events


# ────────────────────────────── build ──────────────────────────────

def week_label(monday):
    sunday = monday + dt.timedelta(days=6)
    if monday.month == sunday.month:
        return f"{monday.strftime('%B')} {monday.day} – {sunday.day}"
    return f"{monday.strftime('%B')} {monday.day} – {sunday.strftime('%B')} {sunday.day}"


def day_label(d):
    return f"{d.strftime('%a %b')} {d.day}"


def build(data, monday, vmap, warn):
    events = validate(data, monday)
    days = [monday + dt.timedelta(days=i) for i in range(7)]
    by_day = {d: [] for d in days}

    for e in events:
        try:
            d = dt.date.fromisoformat(e["event_date"])
        except ValueError:
            warn(f"skipped event with unreadable date {e['event_date']!r}: {clean(e['artist'])}")
            continue
        if d not in by_day:
            warn(f"skipped {d} ({clean(e['artist'])}) — outside the requested week")
            continue
        raw_venue = clean(e["venue"])
        venue = vmap.resolve(raw_venue) or raw_venue
        by_day[d].append({
            "artist": clean(e["artist"]),     # exactly as provided
            "venue": venue,                   # corrected to the canonical card name
            "time": clean(e["time"]),         # exactly as provided
        })

    for d in days:
        by_day[d].sort(key=lambda s: (sort_minutes(s["time"]), s["artist"].lower()))

    highlights = []
    for h in data.get("highlights") or []:
        artist = clean(h.get("artist"))
        if not artist:
            continue
        label = clean(h.get("day"))
        try:
            hd = dt.date.fromisoformat(h["event_date"])
            expected = day_label(hd)
            if label != expected:
                if label:
                    warn(f"highlight day label {label!r} doesn't match {h['event_date']}; "
                         f"using {expected!r}")
                label = expected
        except (KeyError, ValueError, TypeError):
            if not label:
                warn(f"highlight {artist!r} has no usable day label; skipped")
                continue
        highlights.append({"artist": artist, "day": label})

    return days, by_day, highlights


def render(monday, days, by_day, highlights):
    L = ["// ─────────────────────────────────────────────",
         "// BANDS IN BEND — Weekly Show Data",
         "// Synced from the approved-shows feed by scripts/sync_shows.py",
         f"// Week of {monday.isoformat()} · generated {dt.date.today().isoformat()}",
         "// ─────────────────────────────────────────────",
         "",
         "const WEEK = {",
         f"  label: {js_str(week_label(monday))},",
         f"  year: {js_str(monday.year)},",
         "};",
         "",
         "const SHOWS = ["]
    for d in days:
        if not by_day[d]:
            continue                                  # omit empty days entirely
        L += ["  {",
              f"    day: {js_str(DAY_NAMES[d.weekday()])},",
              f"    date: {js_str(d.strftime('%B ') + str(d.day))},",
              "    shows: ["]
        for s in by_day[d]:
            L.append(f"      {{ artist: {js_str(s['artist'])}, "
                     f"venue: {js_str(s['venue'])}, time: {js_str(s['time'])} }},")
        L += ["    ],", "  },"]
    L += ["];", "",
          "// Highlights shown on the cover — Bri's starred shows, in her order",
          "const HIGHLIGHTS = ["]
    for h in highlights:
        L.append(f"  {{ artist: {js_str(h['artist'])}, day: {js_str(h['day'])} }},")
    L += ["];", ""]
    return "\n".join(L)


def nice_path(p):
    rel = os.path.relpath(p, ROOT)
    return rel if not rel.startswith("..") else os.path.abspath(p)


def write_atomic(path, text):
    d = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".shows-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


# ────────────────────────────── main ──────────────────────────────

def next_monday(today=None):
    today = today or dt.date.today()
    return today + dt.timedelta(days=(7 - today.weekday()) % 7 or 7)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--week", help="Monday of the target week (YYYY-MM-DD). Default: next Monday.")
    ap.add_argument("--out", default=os.path.join(ROOT, "shows.js"), help="output file (default: shows.js)")
    ap.add_argument("--dry-run", action="store_true", help="report only; write nothing")
    ap.add_argument("--strict", action="store_true", help="refuse to write if any venue is unknown")
    ap.add_argument("--allow-empty", action="store_true",
                    help="allow writing a week with no approved shows (off by default)")
    ap.add_argument("--url", default=FEED, help="override the feed URL")
    args = ap.parse_args()

    monday = dt.date.fromisoformat(args.week) if args.week else next_monday()
    if monday.weekday() != 0:
        adjusted = monday - dt.timedelta(days=monday.weekday())
        print(f"note: --week {monday} is a {monday.strftime('%A')}; using Monday {adjusted}")
        monday = adjusted

    warnings = []

    def warn(msg):
        warnings.append(msg)

    print(f"Week of {monday} ({week_label(monday)})")
    data, url = fetch_feed(monday, args.url)
    print(f"  feed OK — {url}")

    vmap = VenueMap(load_canonical_venues(), load_aliases())
    days, by_day, highlights = build(data, monday, vmap, warn)
    total = sum(len(v) for v in by_day.values())

    print(f"\n  {total} approved shows, {len(highlights)} highlights")
    for d in days:
        if by_day[d]:
            print(f"    {DAY_NAMES[d.weekday()][:3]} {d.month}/{d.day}: {len(by_day[d])}")

    if vmap.applied:
        print(f"\n  venue names corrected ({len(vmap.applied)}):")
        for raw, canon in sorted(vmap.applied.items()):
            print(f"    {raw!r} → {canon!r}")

    nocard = sorted({s["venue"] for v in by_day.values() for s in v if not vmap.has_card(s["venue"])})
    if vmap.unknown:
        print(f"\n  ⚠️  UNKNOWN VENUES ({len(vmap.unknown)}) — written through as-is:")
        for v, n in sorted(vmap.unknown.items(), key=lambda x: -x[1]):
            print(f"    {v!r} ×{n}")
        print("    Fix: add a line to scripts/venue_aliases.json mapping it to an existing")
        print("    card, or add a .venue-card to venues.html and use that exact name.")
    if nocard:
        print(f"\n  ⚠️  NO VENUE CARD in venues.html ({len(nocard)}):")
        for v in nocard:
            print(f"    {v!r}")

    if warnings:
        print(f"\n  notes ({len(warnings)}):")
        for w in warnings:
            print(f"    - {w}")

    if highlights:
        print("\n  highlights:")
        for h in highlights:
            print(f"    {h['day']:11} {h['artist']}")

    # ---- guards: never leave shows.js empty or half-written ----
    if total == 0 and not args.allow_empty:
        raise SystemExit(
            "\nERROR: the feed returned no approved shows for this week.\n"
            "       That usually means Bri hasn't finished reviewing yet.\n"
            "       shows.js was NOT changed. (Use --allow-empty to override.)")
    if vmap.unknown and args.strict:
        raise SystemExit("\nERROR: --strict and unknown venues present. shows.js was NOT changed.")

    text = render(monday, days, by_day, highlights)

    if args.dry_run:
        print(f"\n--dry-run: would write {len(text)} bytes to {nice_path(args.out)}")
        return

    write_atomic(args.out, text)
    print(f"\nwrote {nice_path(args.out)} ({len(text)} bytes)")
    print("next: review `git diff shows.js`, then commit and push.")
    if vmap.unknown or nocard:
        print("      ⚠️  resolve the venue warnings above first.")


if __name__ == "__main__":
    main()
