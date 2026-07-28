# List of source sites to aggregate.
# For each: (Friendly Name, URL to check/scrape)
# The aggregator will try to auto-discover a real RSS/Atom feed for each
# URL first. If none is found, it falls back to lightweight scraping.
#
# If a source already has a known/working feed URL, put it directly in
# KNOWN_FEEDS below to skip discovery (faster + more reliable).

SOURCES = [
    ("Lanka News Web", "https://lankanewsweb.net/"),
    ("WSWS Sri Lanka", "https://www.wsws.org/en/search"),
    ("Groundviews", "https://groundviews.org/"),
    ("Lanka C News", "https://www.lankacnews.com/"),
    ("Lanka eNews", "https://www.lankaenews.com/"),
    ("WhatNews.lk", "https://whatnews.lk/"),
    ("Tamil Guardian - Tamil Affairs", "https://tamilguardian.com/index.php/tamil-affairs"),
    ("The Diplomat", "https://thediplomat.com/"),
    ("Dasatha Lanka News", "https://dasathalankanews.com/"),
    ("Ceylon Wire - Business", "https://www.ceylonwire.lk/bussiness/"),
    ("Gossip Lanka News", "https://www.gossiplankanews.com/"),
    ("Sri Lanka News (EN)", "https://srilankanews.lk/en/"),
    ("Morning.lk", "https://morning.lk/"),
    ("Lanka Leader", "https://lankaleader.lk/"),
    ("News First - Business", "https://www.newsfirst.lk/category/business"),
    ("UTV News - Business", "https://english.utvnews.lk/category/business/"),
    ("The Morning Money", "https://themorningmoney.com/"),
    ("Ada Derana Biz English", "https://bizenglish.adaderana.lk/"),
    ("Business Cafe", "https://businesscafe.lk/"),
    ("Lanka Business News", "https://www.lankabusinessnews.com/"),
    ("EconomyNext", "https://economynext.com/"),
    ("Colombo Gazette", "https://colombogazette.com/"),
    ("Suratha.lk", "https://suratha.lk/"),
    ("ENBSL", "https://enbsl.lk/"),
    ("Eyeview SL", "https://eyeviewsl.com/"),
    ("Newswire.lk", "https://www.newswire.lk/"),
    ("Lankapuvath - Business", "https://english.lankapuvath.lk/category/business/"),
    ("Mawrata News", "https://mawratanews.lk/"),
    ("Topic.lk", "https://en.topic.lk/"),
    ("Lanka Talks", "https://lankatalks.com/"),
    ("Bizmediaa English", "https://bizmediaa.com/english/"),
    ("Profit Magazine", "https://profitmagazine.lk/category/english-news/"),
    ("Sri Lanka Mirror", "https://srilankamirror.com/"),
    ("Ceylon Business Reporter", "https://ceylonbusinessreporter.com/"),
    ("Times24 - Business", "https://times24.lk/category/business/"),
    ("Buzzer.lk", "https://buzzer.lk/"),
    ("Asian Mirror - Business", "https://asianmirror.lk/news/category/business/"),
    ("Hiru News - Business", "https://hirunews.lk/en/news_listing.php?category=Business"),
    ("VivaLanka - Business Search", "https://www.vivalanka.com/rcsearch/news?&q=&fq=category:%22Business%22&NarrowBy=Category"),
    ("Enterprise News", "https://enterprisenews.lk/?cat=1"),
    ("Business News LK", "https://businessnews.lk/"),
    ("Eyeview Sri Lanka", "https://eyeviewsrilanka.com/"),
    ("eLanka", "https://www.elanka.com.au/"),
    ("Business Gossips", "https://businessgossips.lk/"),
    ("TTV News", "https://ttvnews.lk/"),
    ("Lanka Newspapers", "https://www.lankanewspapers.com/"),
]

# Known-good direct feed URLs (skip auto-discovery for these — faster & reliable).
# Fill in as you confirm ones that work. Example already confirmed:
KNOWN_FEEDS = {
    "Daily FT - Front Page": "https://www.ft.lk/rss/top-story/26",
    "Daily FT - News": "https://www.ft.lk/rss/news/3",
    "Daily FT - Business/Sectors": "https://www.ft.lk/rss/sectors/20",
}
