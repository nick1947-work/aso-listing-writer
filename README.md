# ASO Listing Writer

An agent skill that writes Google Play and Apple App Store listings that rank and convert: keyword map, title, short and full description, What's New, and Hindi/Hinglish versions tuned for the Indian market. It includes a checker for character limits and common metadata policy red flags.

Works with Claude, Antigravity and any agent that reads `SKILL.md` or `AGENTS.md`.

## What you get
- Keyword strategy first (primary, secondary and local terms), then copy written around it
- Title (30), short description (80), full description (4000), What's New (500)
- Natural Hindi copy and an optional Hinglish short description
- `scripts/check_listing.py`: validates length limits, emoji and promo words in titles, keyword repetition and primary-keyword placement
- References for Play metadata rules and India search behaviour

## Install

**Any agent with the skills CLI**
```bash
npx skills add nick1947-work/aso-listing-writer
```

**Claude Code plugin**
```
/plugin marketplace add nick1947-work/aso-listing-writer
/plugin install aso-listing-writer@creation-unicorn
```

**Claude Code (manual)**
```bash
mkdir -p ~/.claude/skills && cp -r skills/aso-listing-writer ~/.claude/skills/
```

**Antigravity (manual)**
```bash
mkdir -p .agent/skills && cp -r skills/aso-listing-writer .agent/skills/
# or global: ~/.gemini/antigravity/skills/
```
Check Antigravity's current docs if the path has changed.

**Claude.ai**
Zip the `aso-listing-writer` folder (so it is the top level of the zip) and upload it under Settings > Capabilities > Skills.

## Use
> Write a Play Store listing for my offline expense tracker. Include Hindi.

> Improve my app's title and short description for better search visibility.

## Check a listing yourself
```bash
python skills/aso-listing-writer/scripts/check_listing.py skills/aso-listing-writer/assets/listing.example.json
```

## Notes
Store rules change; verify limits and policy wording in Play Console before publishing. The skill cannot see real search volumes unless you provide Play Console data.

## License
MIT
