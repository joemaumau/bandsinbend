# Bands in Bend — Project Context

## What This Is
Bands in Bend (bandsinbend.com) is a hyperlocal live music discovery platform for Bend, Oregon. It's a static website hosted on GitHub Pages, updated weekly with new show listings. The site is a partnership project between the site operator and JDM Creative (joe@jdmcreative.co).

---

## Live Site
- **URL:** https://bandsinbend.com
- **GitHub Repo:** https://github.com/joemaumau/bandsinbend
- **Local repo path:** ~/Documents/GitHub/bandsinbend (or wherever cloned)
- **Host:** GitHub Pages (free, deploys on push to main)
- **Domain registrar:** Namecheap

---

## Tech Stack
- Pure HTML / CSS / Vanilla JS — no frameworks, no build tools
- All files in repo root (no subdirectory structure)
- `shows.js` is the single data file — the only file that changes week to week
- `main.js` reads from `shows.js` and renders everything dynamically
- `style.css` handles all styling
- No backend, no CMS, no dependencies

---

## File Structure
```
bandsinbend/
├── index.html        # Homepage — hero, show listings, newsletter signup
├── venues.html       # Venue directory page (static, SEO-focused)
├── style.css         # All styles — brand tokens as CSS custom properties
├── shows.js          # ← THE ONLY FILE UPDATED WEEKLY
├── main.js           # Renders shows, handles day filter, scroll animations
├── CNAME             # bandsinbend.com (do not modify)
├── .nojekyll         # Disables Jekyll processing (do not modify)
└── README.md         # Project notes
```

---

## Brand Tokens
```css
--orange:  #E8632A   /* Primary accent */
--gold:    #C4973A   /* Secondary accent, venue names */
--cream:   #F5F0E8   /* Primary text on dark */
--dark:    #0F0F0F   /* Page background */
--dark2:   #161410
--mid:     #1E1C1A   /* Show item background */
--border:  #2A2825
--gray:    #6B6560
--lgray:   #A09890
```

**Fonts:**
- Display: Playfair Display (700, 900) — headings, day names
- Body: Inter (400, 500, 600) — all UI text

---

## Contact & Social
- **Email:** bandsinbend@gmail.com
- **Instagram:** https://www.instagram.com/bands_in_bend
- **Copyright:** © 2026 Bands in Bend · Bend, Oregon

---

## The Weekly Update Workflow

### What changes each week
Only `shows.js` needs to be edited. It contains three exports:

1. **`WEEK`** — date range label displayed in the hero
2. **`SHOWS`** — array of day objects, each with a `shows` array
3. **`HIGHLIGHTS`** — 4-5 featured artists shown on the cover card

### shows.js structure
```javascript
const WEEK = {
  label: "June 22 – 28",
  year: "2026",
};

const SHOWS = [
  {
    day: "Monday",
    date: "June 22",
    shows: [
      { artist: "Artist Name", venue: "Venue Name", time: "7pm" },
    ],
  },
  // ... one object per day, Monday through Sunday
];

const HIGHLIGHTS = [
  { artist: "Featured Artist", day: "Mon Jun 22" },
  // ... 4-5 highlights
];
```

The `day` field holds a short day + date label (e.g. `"Mon Jun 22"`), matching the
format of the day-filter buttons. Always include the date — not just the weekday —
so highlights stay unambiguous, especially when a listing spans two calendar weeks.

### Days order
Always list days Monday through Sunday. If a day has no shows, omit it entirely.

### Verify & correct venue spellings
Venue names in the lineup notes are often misspelled or use unofficial variants.
For every venue in a weekly update, verify the spelling against the venue's official
name using the web search tool (check the venue's own site / Visit Bend / Facebook),
and correct it in `shows.js` — keep the matching `venues.html` card aligned. Examples
already corrected: "Volcanic Theater" → "Volcanic Theatre Pub", "Tower Theater" →
"Tower Theatre". This is a deliberate exception to the "enter venue names exactly as
provided" note below — venue spellings ARE corrected; artist names and times are still
entered exactly as provided unless the user asks otherwise.

### New venues → add a card to venues.html
Whenever the weekly lineup introduces a venue that does NOT already have a card in
`venues.html`, add a `.venue-card` for it as part of the same update. Append new cards
at the end of the `.venues-grid` (the established pattern — newer venues go last).
Each card has three parts: `.venue-name` (exact venue name), `.venue-type` (e.g.
"Brewery · Live Music"), and `.venue-desc` (one short sentence in the existing tone).
Watch for naming variants of an existing venue (e.g. "Domino Room" vs "The Domino Room")
— those are the SAME venue and should NOT get a duplicate card; flag the inconsistency
instead. Remember to `git add venues.html` alongside `shows.js` when a card was added.

### Update prompt to use with Claude Code
Paste the week's show listings and say:
> "Update shows.js with this week's lineup. Week is [date range]."

Claude Code will edit shows.js directly in the repo. Review the diff, then commit and push.

---

## Deployment
Every push to `main` triggers an automatic GitHub Pages deploy. Live in ~60 seconds. No build step needed.

**To push after editing:**
```bash
git add shows.js
git commit -m "Update shows: [week date range]"
git push
```

Or use GitHub Desktop: stage changes → commit → Push Origin.

---

## Venue Reference
Common Bend venues for shows.js entries:

| Venue | Notes |
|-------|-------|
| Silver Moon | Most active, multiple nights/week |
| Hayden Homes Amphitheater | Major outdoor venue |
| Tower Theater | Historic downtown theater |
| Volcanic Theater Pub / Volcanic Theater Courtyard | Indoor + outdoor |
| Domino Room / The Domino Room | Indie/rock/electronic |
| The Commonwealth Pub | Neighborhood bar, regular bookings |
| Worthy Brewing | East side brewery |
| Bevel Craft Brewing | Local brewery |
| Rivers Place Taphouse | Neighborhood taphouse |
| Father Luke's Room | Intimate bar |
| Northside Bar & Grill | North side staple |
| Dogwood at the Pine Shed | Late night bookings |
| On Tap | Casual neighborhood bar |
| M&J Tavern | Classic tavern |

---

## Future Development Roadmap

### Phase 2 (next)
- Add Mailchimp/Kit newsletter embed to replace placeholder form
- Add "Submit a Show" form (Netlify Forms or Formspree)
- Add individual venue pages for SEO (e.g. /venues/silver-moon.html)

### Phase 3
- Filterable calendar by genre
- Venue sponsorship featured placement
- Artist promotion highlighted listings

---

## Key Decisions Already Made
- Static site over Webflow/Squarespace to keep costs at $0/month
- GitHub Pages over Netlify (simpler for this use case, may revisit for forms)
- No Jekyll (`.nojekyll` file present)
- Shows rendered via JS from data file rather than hardcoded HTML (easier weekly updates)
- All files in root (not in subdirectories) due to GitHub upload UI limitations during initial setup

---

## People
- **Site operator / content:** [Partner name] — gathers weekly show listings, manages social
- **Build / design / tech:** Joe Maurer, JDM Creative — joe@jdmcreative.co / jdmcreative.co
- **GitHub username:** joemaumau

---

## Notes for Claude Code
- Always edit `shows.js` only for weekly updates — do not modify `main.js`, `style.css`, `index.html`, or `venues.html` unless explicitly asked
- When updating shows, preserve the exact JS variable names: `WEEK`, `SHOWS`, `HIGHLIGHTS`
- Do not add `export` statements — these are plain script tags, not ES modules
- Artist names and times should be entered exactly as provided — do not correct spelling or standardize formatting unless asked
- Venue names ARE the exception: verify each against its official spelling via web search and correct it (see "Verify & correct venue spellings" above)
- Days run Monday through Sunday
- After editing, remind the user to commit with: `git add shows.js && git commit -m "Update shows: [week]" && git push`
