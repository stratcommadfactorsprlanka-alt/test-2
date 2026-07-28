# Keyword filter for the aggregator.
#
# INCLUDE_KEYWORDS: an item is kept if its title+summary contains ANY of these
#                    (case-insensitive, substring match)
# EXCLUDE_KEYWORDS: an item is dropped if it contains ANY of these, even if it
#                    also matched an include keyword
#
# This implements:
#   ("TEA" OR "Rubber" OR ... ) NOT ("real estate" OR "real-estate")

INCLUDE_KEYWORDS = [
    "tea",
    "rubber",
    "palm oil",
    "oil palm",
    "sri lanka tea board",
    "niraj de mel",
    "jeevan thondaman",
    "sanjaya herath",
    "vadivel suresh",
    "malayaga",
    "planters association",
    "plantation industry",
    "tea plantation",
    "fertiliser",
    "fertilizer",
    "sri lanka's tea pickers",
    "sri lankas tea pickers",
    "sri lanka's tea",
    "sri lankas tea",
    "malaiyaha",
    "mano ganesan",
    "senaka alawattegama",
    "colombo tea traders association",
    "anil cooke",
    "ganesh deivanayagam",
    "ceylon tea",
    "estate workers",
    "plantation",
    "plantations",
    "planters",
    "plantation authority association",
    "plantation authorities association",
    "plantation worker",
    "estate",
    "estates",
    "planters' association",
    "planters association",
    "upcountry",
    "up-country",
    "ctta",
    "poiasl",
]

EXCLUDE_KEYWORDS = [
    "real estate",
    "real-estate",
]


def matches_filter(title: str, summary: str) -> bool:
    """Return True if this item should be kept."""
    text = f"{title} {summary}".lower()

    if any(bad.lower() in text for bad in EXCLUDE_KEYWORDS):
        return False

    return any(good.lower() in text for good in INCLUDE_KEYWORDS)
