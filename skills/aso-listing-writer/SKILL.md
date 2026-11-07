---
name: aso-listing-writer
description: Write Google Play Store (and Apple App Store) listings that rank and convert - app title, short description, full description, keyword map, What's New text, and Hindi/Hinglish localization - tuned for the Indian market. Use this skill whenever the user mentions ASO, app store optimization, Play Store listing, app title, app description, store keywords, store ranking, release notes for the store, or wants more downloads or visibility for an app, even if they never say "ASO".
---

# ASO Listing Writer

Produce a complete, policy-safe store listing for an app, backed by a keyword strategy rather than guesswork. The goal is a listing that (1) matches what real users type into search, and (2) convinces a person on the store page to tap Install.

## Why the order matters

On Google Play there is no hidden keyword field. Ranking comes from the visible text: title, short description, full description (and, to a lesser degree, the developer name and in-app signals). So the keyword work and the copywriting are the same job. Decide the keywords first, then write copy that carries them naturally. Copy written first and keywords sprinkled afterwards reads as stuffing and risks a metadata-policy rejection.

## Workflow

### 1. Gather inputs
Collect what is not already in the conversation. Do not interrogate; ask at most one short question, and work with assumptions for the rest (state them in one line).

- App name, platform (Play / App Store / both), category
- 3-6 core features and the single strongest differentiator (offline, no ads, privacy, low storage, etc.)
- Target user and the problem they have in their own words
- Languages to cover (default: English + Hindi/Hinglish for India)
- Any real data: Play Console search-term reports, current title/description, competitor names

If the user has an existing listing, rewrite it rather than starting blind, and say what changed and why.

### 2. Build the keyword map
Read `references/india-market.md` for local search behaviour and `references/play-store-rules.md` for limits and policy.

- Brainstorm seed terms from the problem, not the feature ("scan receipts to track spending" beats "OCR expense module").
- Group into intent clusters: **core** (what the app is), **task** (what the user wants done), **qualifier** (offline, free, lite, no login), **local** (Hinglish, UPI, regional phrasing).
- Pick one **primary keyword** (goes in title, short description, and the first sentence of the full description) and 4-8 **secondary keywords**.
- Never invent search volumes or rankings. If there is no data, label priorities as "hypothesis" and tell the user how to verify (Play Console > Statistics > search terms, store autocomplete, competitor titles).

### 3. Write the copy
Follow the output template below. Draft several options where choice matters (title, short description), but commit to one recommendation and say why.

Craft rules:
- Title: brand + primary keyword, within the limit, no emoji, no promo words ("best", "#1", "free", "new", "sale").
- Short description: the one-line pitch with the primary keyword and the strongest benefit. It is the first thing under the screenshots.
- Full description: the first 2-3 lines decide whether people expand it, so put the primary keyword and the core benefit there. Then benefits before features, short paragraphs, plain bullets, a privacy/offline line if true, and a closing call to action. Use secondary keywords where they read naturally; repeating any one term more than a handful of times looks like stuffing.
- Only claim what the app really does. Unverifiable claims ("fastest", "most accurate") and misleading permissions language are policy risks and erode trust.
- Match the user's voice: clean, modern, privacy-respecting apps should sound calm and specific, not hypey.

### 4. Validate
Put the draft in a JSON file and run the checker. It verifies character limits, emoji and promo words in the title, keyword repetition, and where the primary keyword appears.

```bash
python scripts/check_listing.py listing.json
```

Fix every FAIL. Treat WARN items as review prompts, not automatic errors. See the script header for the JSON shape.

### 5. Localize
For Hindi, write natural Devanagari copy, not a literal translation, and keep the app/brand name in Latin script. Offer a Hinglish (Hindi in Latin script) variant of the short description only when the keyword research shows users search that way. Re-run the checker on each language's version.

## Output template

Use this structure so the result can be pasted straight into Play Console:

```
## Assumptions
(one or two lines)

## Keyword map
Primary: ...
Secondary: ...
Local / Hinglish: ...
Priority notes: (hypotheses vs. data-backed)

## Title (max 30)
Recommended: ...   [N chars]
Alternatives: ...

## Short description (max 80)
Recommended: ...   [N chars]
Alternatives: ...

## Full description (max 4000)
...                [N chars]

## What's New (max 500)
...

## Hindi version
(title, short, full, if requested)

## Why these choices
(3-5 lines)
```

## Examples

**Example input:** "Offline expense tracker, no login, scans bill photos, for India."
**Good title:** `SpendWise: Expense Tracker` (primary keyword "expense tracker" present, brand first, 26 chars)
**Good short description:** `Offline expense tracker. Scan bills, no login, data stays on your phone.` (primary keyword first, three concrete benefits, privacy angle)
**Weak short description:** `Best #1 free expense tracker app download now!!!` (promo words, punctuation spam, no benefit - likely rejected)

## When not to use this skill
Paid user-acquisition copy (ad creatives), in-app UI text, and legal text such as privacy policies are different jobs; do the task directly instead of forcing this template.
