# Meridian — Filtered News Aggregator

Pulls headlines from ~46 news and business sites, filters them down to a
specific set of topics/keywords, and publishes the result as both:

- a standard RSS feed (`feed.xml`) any reader can subscribe to, and
- a styled webpage (`index.html`) for browsing in a browser.

Everything refreshes automatically once a day via GitHub Actions.

## How it works

For each source in `sources.py`, the script:
1. **Tries to auto-discover a real RSS/Atom feed** — checks the page's
   `<link rel="alternate">` tags, then tries common paths like `/feed/`,
   `/rss/`, `/rss.xml`, etc.
2. If a real feed is found, pulls items from it directly (title, link,
   summary, published date — all accurate).
3. **If no feed exists**, falls back to lightweight scraping: it grabs
   headline-like links from `<h1>`–`<h4>` tags and `<article>` blocks on
   the homepage/category page. These items won't have real publish dates
   (the scrape time is used instead) and quality varies by site layout.
4. All items are checked against the keyword list in `filters.py` — only
   items that match are kept.
5. Everything is merged, sorted by date, and written out as `feed.xml`.
6. `index.html` is a static page that reads `feed.xml` live in the
   browser and displays it as a styled list — no separate build step.

## Files

| File | Purpose |
|---|---|
| `aggregate.py` | Main script — discovers/scrapes/filters/writes `feed.xml` |
| `sources.py` | List of source sites (edit to add/remove) |
| `filters.py` | Keyword include/exclude list — edit to change what gets kept |
| `index.html` | Styled homepage that displays the feed |
| `requirements.txt` | Python dependencies |
| `.github/workflows/aggregate.yml` | Runs the script daily, commits `feed.xml` |
| `.nojekyll` | Tells GitHub Pages to serve files as-is (no Jekyll processing) |

## Setup — new repository, step by step

1. **Create a new GitHub repository** (public, so Pages can serve it for free).
2. **Upload every file in this folder to the repo root**, preserving folder
   structure — i.e. `.github/workflows/aggregate.yml` must stay nested,
   not get flattened. If uploading via the GitHub web UI, drag-and-drop
   the whole folder, or use "Add file → Create new file" and type the
   full path (`.github/workflows/aggregate.yml`) to auto-create folders.
3. **Enable workflow write permissions**: repo **Settings → Actions →
   General → Workflow permissions** → select "Read and write permissions"
   → Save. (Without this, the workflow can't commit the updated feed.)
4. **Enable GitHub Pages**: repo **Settings → Pages** → under "Build and
   deployment," set **Source** to "Deploy from a branch" → branch `main`,
   folder `/ (root)` → Save.
5. **Run the workflow once manually**: go to the **Actions** tab → click
   "Update aggregated RSS feed" → **Run workflow**. Wait for it to finish
   with a green checkmark — this generates the first `feed.xml`.
6. **Visit your site**: `https://<your-username>.github.io/<repo-name>/`
   — should show the styled Meridian page with live entries.
7. **Raw feed for RSS readers**:
   `https://<your-username>.github.io/<repo-name>/feed.xml`

## Running locally (optional, for testing)

```bash
pip install -r requirements.txt
python aggregate.py --out feed.xml --per-source 20 --workers 10
```

Add `--no-filter` to see everything unfiltered (useful for checking a
source is actually pulling data before keywords narrow it down).

## Tuning

- **Change what topics it tracks** → edit `INCLUDE_KEYWORDS` /
  `EXCLUDE_KEYWORDS` in `filters.py`. No need to touch anything else.
- **Add/remove sources** → edit `SOURCES` in `sources.py`. If you've
  confirmed a source's real feed URL, add it to `KNOWN_FEEDS` too —
  skips auto-discovery, faster and more reliable.
- **How often it runs** → edit the `cron:` line in
  `.github/workflows/aggregate.yml` (currently daily at 03:00 UTC).
- **How many raw items per source before filtering** → `--per-source`
  flag (default 20).

## Troubleshooting

- **Actions tab says "Get started with GitHub Actions"** → the workflow
  file isn't where GitHub expects it. Confirm the exact path
  `.github/workflows/aggregate.yml` exists on the `main` branch.
- **Homepage shows your README instead of the styled page** → `index.html`
  isn't at the repo root, or Pages hasn't rebuilt yet (takes 1-2 min after
  a commit — check the separate "pages build and deployment" run in the
  Actions tab).
- **Page loads but says "Could not load feed.xml"** → open
  `.../feed.xml` directly in your browser. If that 404s, `feed.xml`
  hasn't been generated yet (run the workflow manually) or isn't on the
  branch Pages is serving from.

## Important notes

- **Not live-tested against all sources** — auto-discovery and the
  scraping fallback use general-purpose techniques, but some sites with
  unusual layouts, JS-rendered content, or anti-bot protection may
  return zero items. Run it once, check the Action's log output (it
  reports per-source whether it found a feed, fell back to scraping, or
  failed), and refine as needed.
- Sites that render content via JavaScript won't work with the scraping
  fallback as-is — those need a headless browser (not included, to keep
  this lightweight).
- Respect each site's `robots.txt` and terms of use — this pulls
  headlines/links/summaries for aggregation, not full article content.
