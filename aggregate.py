#!/usr/bin/env python3
"""
RSS Aggregator
==============
Pulls items from a list of source sites (real RSS/Atom feeds where they
exist, lightweight scraping where they don't) and merges everything into
one combined feed.xml.

Usage:
    python aggregate.py                # writes feed.xml in this folder
    python aggregate.py --out out.xml  # custom output path
    python aggregate.py --per-source 8 # max items pulled per source
    python aggregate.py --workers 12   # concurrency

Designed to be run on a schedule (see .github/workflows/aggregate.yml).
"""

import argparse
import concurrent.futures as cf
import datetime as dt
import hashlib
import html
import re
import sys
import urllib.parse as urlparse

import feedparser
import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

from sources import SOURCES, KNOWN_FEEDS
from filters import matches_filter

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 RSSAggregatorBot/1.0"
    )
}
TIMEOUT = 15
COMMON_FEED_PATHS = [
    "feed/", "feed", "rss/", "rss", "rss.xml", "feed.xml", "atom.xml",
    "?feed=rss2", "index.xml",
]


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def fetch(url, **kw):
    return requests.get(url, headers=HEADERS, timeout=TIMEOUT, **kw)


def looks_like_feed(text):
    head = text[:400].lower()
    return "<rss" in head or "<feed" in head or "<?xml" in head


def discover_feed_url(base_url):
    """Try to find a real RSS/Atom feed for a given site URL."""
    # 1. Look for <link rel="alternate" type="application/rss+xml"> in the HTML head
    try:
        resp = fetch(base_url)
        if resp.ok:
            soup = BeautifulSoup(resp.text, "html.parser")
            for link in soup.find_all("link", rel="alternate"):
                t = (link.get("type") or "").lower()
                if "rss" in t or "atom" in t:
                    href = link.get("href")
                    if href:
                        candidate = urlparse.urljoin(base_url, href)
                        try:
                            r2 = fetch(candidate)
                            if r2.ok and looks_like_feed(r2.text):
                                return candidate
                        except requests.RequestException:
                            pass
    except requests.RequestException as e:
        log(f"  [discover] could not load {base_url}: {e}")

    # 2. Try common feed paths
    parsed = urlparse.urlparse(base_url)
    root = f"{parsed.scheme}://{parsed.netloc}/"
    for path in COMMON_FEED_PATHS:
        candidate = urlparse.urljoin(base_url if base_url.endswith("/") else base_url + "/", path)
        try:
            r = fetch(candidate)
            if r.ok and looks_like_feed(r.text):
                return candidate
        except requests.RequestException:
            continue
        # also try relative to domain root, not just the given path
        candidate_root = urlparse.urljoin(root, path)
        if candidate_root != candidate:
            try:
                r = fetch(candidate_root)
                if r.ok and looks_like_feed(r.text):
                    return candidate_root
            except requests.RequestException:
                continue

    return None


def pull_from_feed(feed_url, source_name, limit):
    parsed = feedparser.parse(feed_url, request_headers=HEADERS)
    items = []
    for entry in parsed.entries[:limit]:
        title = html.unescape(entry.get("title", "").strip())
        link = entry.get("link", "").strip()
        if not title or not link:
            continue
        summary = html.unescape(re.sub("<[^<]+?>", "", entry.get("summary", "")).strip())[:500]
        published = None
        for key in ("published_parsed", "updated_parsed"):
            if entry.get(key):
                published = dt.datetime(*entry[key][:6], tzinfo=dt.timezone.utc)
                break
        items.append({
            "source": source_name,
            "title": title,
            "link": link,
            "summary": summary,
            "published": published or dt.datetime.now(dt.timezone.utc),
        })
    return items


def scrape_fallback(base_url, source_name, limit):
    """Best-effort generic scrape: grab headline-like links from the page."""
    items = []
    try:
        resp = fetch(base_url)
        if not resp.ok:
            return items
        soup = BeautifulSoup(resp.text, "html.parser")
    except requests.RequestException as e:
        log(f"  [scrape] failed to load {base_url}: {e}")
        return items

    seen_links = set()
    candidates = []

    # Prefer links inside heading tags (h1-h4) - usually article titles
    for tag in soup.find_all(["h1", "h2", "h3", "h4"]):
        a = tag.find("a", href=True)
        if a:
            candidates.append(a)

    # Also grab links inside <article> containers
    for art in soup.find_all("article"):
        a = art.find("a", href=True)
        if a:
            candidates.append(a)

    for a in candidates:
        href = a.get("href", "").strip()
        text = a.get_text(strip=True)
        if not href or not text or len(text) < 15:
            continue
        full_url = urlparse.urljoin(base_url, href)
        if full_url in seen_links:
            continue
        seen_links.add(full_url)
        items.append({
            "source": source_name,
            "title": html.unescape(text),
            "link": full_url,
            "summary": "",
            "published": dt.datetime.now(dt.timezone.utc),
        })
        if len(items) >= limit:
            break

    return items


def process_source(name, url, limit):
    log(f"Processing: {name} ({url})")
    feed_url = KNOWN_FEEDS.get(name) or discover_feed_url(url)
    if feed_url:
        try:
            items = pull_from_feed(feed_url, name, limit)
            if items:
                log(f"  -> feed found ({feed_url}), {len(items)} items")
                return items
        except Exception as e:
            log(f"  [feed parse error] {e}")

    log("  -> no usable feed, falling back to scraping")
    items = scrape_fallback(url, name, limit)
    log(f"  -> scraped {len(items)} items")
    return items


def build_feed(all_items, title, link, description):
    fg = FeedGenerator()
    fg.title(title)
    fg.link(href=link, rel="alternate")
    fg.description(description)
    fg.language("en")

    all_items.sort(key=lambda i: i["published"], reverse=True)

    for item in all_items:
        fe = fg.add_entry()
        fe.title(f"[{item['source']}] {item['title']}")
        fe.link(href=item["link"])
        guid = hashlib.sha256(item["link"].encode("utf-8")).hexdigest()
        fe.guid(guid, permalink=False)
        if item["summary"]:
            fe.description(item["summary"])
        fe.pubDate(item["published"])

    return fg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="feed.xml")
    ap.add_argument("--per-source", type=int, default=20)
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument(
        "--no-filter", action="store_true",
        help="Skip keyword filtering and include everything (useful for debugging sources)."
    )
    args = ap.parse_args()

    all_items = []
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {
            ex.submit(process_source, name, url, args.per_source): name
            for name, url in SOURCES
        }
        # also pull any KNOWN_FEEDS not already covered by SOURCES
        for name, feed_url in KNOWN_FEEDS.items():
            if name not in dict(SOURCES):
                futures[ex.submit(pull_from_feed, feed_url, name, args.per_source)] = name

        for fut in cf.as_completed(futures):
            name = futures[fut]
            try:
                items = fut.result()
                all_items.extend(items)
            except Exception as e:
                log(f"[ERROR] {name}: {e}")

    log(f"\nTotal items collected: {len(all_items)}")

    if args.no_filter:
        filtered_items = all_items
    else:
        filtered_items = [
            item for item in all_items
            if matches_filter(item["title"], item["summary"])
        ]
        log(f"Items after keyword filter: {len(filtered_items)}")

    fg = build_feed(
        filtered_items,
        title="Sri Lanka Tea, Rubber & Plantation News",
        link="https://example.com/feed.xml",
        description="Filtered headlines about tea, rubber, palm oil, and the plantation industry from multiple Sri Lankan news/business sources.",
    )
    fg.rss_file(args.out)
    log(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
