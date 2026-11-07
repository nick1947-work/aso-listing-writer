#!/usr/bin/env python3
"""Validate a store listing against character limits and common metadata red flags.

Usage:
    python check_listing.py listing.json

listing.json shape (all fields optional except the ones you want checked):
{
  "primary_keyword": "expense tracker",
  "title": "SpendWise: Expense Tracker",
  "short_description": "Track spending offline. Scan bills, no login.",
  "full_description": "....",
  "whats_new": "...."
}

Exit code is 1 if any FAIL is reported, otherwise 0. WARN items are review prompts.
Keyword-density thresholds are heuristics, not Google rules.
"""
import json
import re
import sys
from collections import Counter

LIMITS = {
    "title": 30,
    "short_description": 80,
    "full_description": 4000,
    "whats_new": 500,
}

PROMO_WORDS = ["best", "#1", "no.1", "top", "free", "new", "sale", "discount", "download now", "official"]
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2B06\u2194-\u21AA]")
STOPWORDS = set(
    "the a an and or of to in on for with your you is are it this that be as at by from "
    "can will all any more not no but app apps".split()
)


def words(text):
    return re.findall(r"[A-Za-z\u0900-\u097F']+", text.lower())


def main(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    fails, warns = [], []

    for field, limit in LIMITS.items():
        text = data.get(field)
        if text is None:
            continue
        n = len(text)
        status = "OK" if n <= limit else "FAIL"
        print(f"[{status}] {field}: {n}/{limit} chars")
        if n > limit:
            fails.append(f"{field} is {n - limit} chars over the {limit} limit")

    title = data.get("title", "")
    if title:
        if EMOJI_RE.search(title):
            fails.append("title contains emoji or symbols")
        lowered = title.lower()
        for w in PROMO_WORDS:
            if re.search(r"(?<!\w)" + re.escape(w) + r"(?!\w)", lowered):
                fails.append(f"title contains promo/ranking word: '{w}'")
        for token in re.findall(r"\b[A-Z]{4,}\b", title):
            warns.append(f"title has ALL-CAPS word '{token}' (fine only if it is the brand)")
        if re.search(r"[!?*~]{2,}", title):
            fails.append("title has repeated special characters")

    short = data.get("short_description", "")
    if short:
        if EMOJI_RE.search(short):
            warns.append("short description contains emoji")
        if re.search(r"[!?]{2,}", short):
            warns.append("short description has repeated punctuation")

    pk = (data.get("primary_keyword") or "").strip().lower()
    full = data.get("full_description", "")
    if pk:
        if title and pk not in title.lower():
            warns.append("primary keyword missing from title")
        if short and pk not in short.lower():
            warns.append("primary keyword missing from short description")
        if full and pk not in full[:250].lower():
            warns.append("primary keyword not in the first 250 chars of the full description")
        if full:
            count = full.lower().count(pk)
            print(f"[INFO] primary keyword appears {count}x in full description")
            if count > 6:
                warns.append(f"primary keyword repeated {count}x in full description (stuffing risk)")
            if count == 0:
                warns.append("primary keyword absent from full description")

    if full:
        toks = [w for w in words(full) if len(w) > 3 and w not in STOPWORDS]
        total = max(len(toks), 1)
        for w, c in Counter(toks).most_common(5):
            density = 100.0 * c / total
            print(f"[INFO] '{w}': {c}x ({density:.1f}% of meaningful words)")
            if c >= 8 and density > 3.0:
                warns.append(f"'{w}' repeated {c}x ({density:.1f}%) - check it reads naturally")
        emoji_count = len(EMOJI_RE.findall(full))
        if emoji_count > 10:
            warns.append(f"{emoji_count} emoji in full description - consider trimming")

    print()
    for m in warns:
        print(f"[WARN] {m}")
    for m in fails:
        print(f"[FAIL] {m}")
    if not fails and not warns:
        print("All checks passed.")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
