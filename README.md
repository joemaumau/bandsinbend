# Bands in Bend

Your weekly guide to live music in Bend, Oregon.

**Live site:** [bandsinbend.com](https://bandsinbend.com)

---

## Weekly Update Workflow

Each week, only one file needs updating:

### `js/shows.js`

This is the single source of truth for all show listings. Update three things:

1. **`WEEK`** — Update the date range label
2. **`SHOWS`** — Replace the full shows array with the new week's listings
3. **`HIGHLIGHTS`** — Update the 4-5 artists shown on the cover card

Then commit and push to `main` — the site updates automatically within ~60 seconds.

---

## File Structure

```
bandsinbend/
├── index.html        # Homepage
├── venues.html       # Venue directory
├── CNAME             # Custom domain (don't touch)
├── css/
│   └── style.css     # All styles
└── js/
    ├── shows.js      # ← UPDATE THIS WEEKLY
    └── main.js       # Site logic (rarely needs changes)
```

---

## Agentic Update Workflow with Claude

Paste the week's show listings into Claude with:

> "Update the Bands in Bend shows.js with this week's lineup: [paste listings]"

Claude will return the updated `shows.js` content ready to copy-paste or commit directly.

---

## DNS Config (Namecheap)

| Type  | Host | Value                  |
|-------|------|------------------------|
| A     | @    | 185.199.108.153        |
| A     | @    | 185.199.109.153        |
| A     | @    | 185.199.110.153        |
| A     | @    | 185.199.111.153        |
| CNAME | www  | joemaumau.github.io.   |

---

## Contact

Built by [JDM Creative](https://jdmcreative.co) · joe@jdmcreative.co
