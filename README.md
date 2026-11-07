# Creation Unicorn Agent Skills

Reusable agent skills for Android and indie-app developers. Each skill is a folder with a `SKILL.md` (instructions the agent loads when relevant) plus optional `references/`, `scripts/` and `assets/`. The same folders work in Claude, Antigravity, and any agent that reads `SKILL.md` or `AGENTS.md`.

## Skills

| Skill | What it does |
|---|---|
| [`play-release-readiness`](skills/play-release-readiness) | Checks whether an Android/Flutter app is ready for Google Play: scans the project, produces a PASS/WARN/FAIL report, drafts the privacy policy, terms, account-deletion page and Data safety answers, decodes rejection emails, and includes a launch-and-scale playbook for new developers. |
| [`aso-listing-writer`](skills/aso-listing-writer) | Writes Play Store / App Store listings (title, short + full description, keyword map, What's New, Hindi/Hinglish) tuned for India, with a character-limit and policy checker. |

The two skills work together: run readiness first, then write the listing.

## Install

**Any agent that supports the skills CLI**
```bash
npx skills add nick1947-work/aso-listing-writer
```

**Claude Code plugin**
```
/plugin marketplace add nick1947-work/aso-listing-writer
/plugin install android-skills@creation-unicorn
```

**Claude Code (manual copy)**
```bash
mkdir -p ~/.claude/skills && cp -r skills/* ~/.claude/skills/
```
Use `.claude/skills/` inside a repo to scope it to one project.

**Antigravity (manual copy)**
```bash
# per project
mkdir -p .agent/skills && cp -r skills/play-release-readiness skills/aso-listing-writer .agent/skills/

# or global
mkdir -p ~/.gemini/antigravity/skills && cp -r skills/* ~/.gemini/antigravity/skills/
```
(Check Antigravity's current docs if the skills path has changed.)

**Claude.ai / Claude app**
Zip a single skill folder (so `play-release-readiness/` is the top level of the zip) and upload it under Settings > Capabilities > Skills.

**Other agents (Cursor, Codex, Gemini CLI, ...)**
Point the agent at `AGENTS.md`, which tells it when to read each skill.

## Use

> Is my app ready for Google Play? Scan this project and tell me what will get it rejected.

> Create a privacy policy, terms and account-deletion page for my app.

> I got a Play Console rejection email, here it is. What do I fix?

> Write a Play Store listing for my offline expense tracker, include Hindi.

## Keeping rules fresh
Play policies change several times a year. `skills/play-release-readiness/references/current-requirements.md` carries a "Last verified" date and official source links, and the skill tells the agent to re-check sources when the file is old. Pull requests that update a rule should change the date and cite the official page.

## Tests
```bash
sh skills/play-release-readiness/tests/run_tests.sh
```

## Automate in your own app repo
Copy `skills/play-release-readiness/assets/github-action-readiness.yml` to `.github/workflows/` in your app to run the scan on every pull request.

## Adding more skills
Create `skills/<skill-name>/SKILL.md` with this frontmatter:

```yaml
---
name: skill-name
description: What it does AND when to use it. Be specific about trigger phrases.
---
```

## Disclaimer
Templates and checks reduce avoidable mistakes but do not guarantee approval. Documents are templates, not legal advice. This project is not affiliated with Google.

## License
MIT
