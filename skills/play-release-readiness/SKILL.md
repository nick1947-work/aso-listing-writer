---
name: play-release-readiness
description: Check whether an Android or Flutter app is ready to submit to Google Play, and prevent avoidable rejections. Scans the project (manifest, permissions, targetSdk, SDKs, debug/test leftovers), produces a PASS/WARN/FAIL readiness report, drafts the Privacy Policy, Terms and Conditions, account-deletion page and Data safety answers, and gives a launch-and-scale playbook for new developers. Use this skill whenever the user mentions publishing or releasing an app, Play Console, app rejection or suspension, policy violation, Data safety form, privacy policy, terms and conditions, target API level, closed testing or the 12 testers rule, production access, account deletion, sensitive permissions, "is my app ready", a launch checklist, or how to scale an app after launch, even if they never say "readiness".
---

# Play Release Readiness

Help a developer (especially a first-time one) find the problems that get apps rejected *before* they submit, produce the documents Play expects, and plan the road from first release to scale. The aim is to remove avoidable rejections, not to promise approval: Google's review has parts nobody outside Google can see, so never say an app "will be approved".

## Principles

- **Evidence over assurance.** Report what was actually checked and what could not be checked. Use four statuses: PASS, WARN, FAIL, UNKNOWN (needs a human or the Play Console to confirm).
- **Rules go stale.** Play deadlines and policies change several times a year. Before giving a verdict, follow "Freshness check" below.
- **Truthful declarations beat clever ones.** Most Data safety and policy rejections come from a mismatch between what the app does (including its SDKs) and what was declared. Never write a declaration or policy sentence the app does not support.
- **Not legal advice.** Policy and terms are templates. Say so, and recommend a lawyer review when the app handles payments, health, children's data, or sensitive personal data.

## Freshness check (do this first)

1. Open `references/current-requirements.md` and read its "Last verified" date.
2. If it is older than about 60 days, or the user asks about a deadline, web-search the official sources listed in that file (Play Console Help, developer.android.com policy pages) and prefer them over blogs. Tell the user which rules changed. Offer to update the file.
3. If you cannot search, say the rules were last verified on that date and may be outdated.

## Workflow

### 1. Pick the mode
- **Audit**: user has a project or code. Go to step 2.
- **Documents**: user wants privacy policy, terms, deletion page, or Data safety answers. Go to step 4.
- **Roadmap**: user is new and asks what to do. Give `references/launch-and-scale-playbook.md`, tailored (account type, timeline, testers).
- **Rejection or suspension**: user pastes a rejection email. Map it using `references/rejection-reasons.md`, explain the cause in plain words, give the minimal fix, and how to appeal or resubmit. Do not advise resubmitting unchanged.

### 2. Scan the project
If the project folder is accessible, run:

```bash
python scripts/scan_project.py <project-root> [--json] [--min-target 36]
```

It reads manifests, Gradle/TOML files and `pubspec.yaml` (Flutter), and reports targetSdk, permissions, SDKs that imply data collection, debug leftovers, test ad IDs, cleartext traffic, backup settings and more. If you cannot run it, ask for the manifest and `build.gradle(.kts)` or `pubspec.yaml` and apply `references/permissions-guide.md` and `references/sdk-data-map.md` by hand. If the minimum target in `current-requirements.md` differs from the script default, pass `--min-target`.

### 3. Build the readiness report
Use `assets/readiness-report-template.md`. Group findings as:
1. **Blockers** (will fail upload or review)
2. **Likely rejection risks** (policy mismatches, missing declarations)
3. **Console tasks** only a human can do in Play Console (Data safety, content rating, target audience, ads declaration, app access instructions, privacy policy URL, deletion URL, store listing, testing track)
4. **Quality and growth suggestions** (optional)

End with a verdict: *Blocked*, *At risk*, or *No known blockers found*. Include a short "what I could not check" list. For store-listing copy, hand off to the `aso-listing-writer` skill if it is available.

### 4. Generate documents
Templates live in `assets/`. Fill them from facts the user or the scan provided; ask at most one short question for missing essentials (developer/company name, contact email, country, whether there are accounts or ads). Leave unresolved items as `[[PLACEHOLDER]]` and list them at the end.

- `privacy-policy-template.md`: include only the optional sections that match detected features (ads, analytics, accounts, location, camera/microphone, payments, children, AI). Keep claims aligned with the scan.
- `terms-and-conditions-template.md`
- `account-deletion-page-template.md`: required when the app lets users create accounts.
- `data-safety-worksheet.md`: answer per data type using `references/sdk-data-map.md`, noting that data collected by an SDK counts as collected by the app.

Remind the user the privacy policy must be a public, always-available web page (not a PDF, not behind login or a region block) and that the same URL goes in the store listing and, where asked, inside the app. For indie developers, free static hosting such as GitHub Pages works.

### 5. Plan the next steps
Suggest automating the scan: `assets/github-action-readiness.yml` runs it on every pull request in the developer's own repo.

Offer the playbook (`references/launch-and-scale-playbook.md`). For first launches on a new personal account, spell out the closed-testing timeline in calendar dates, since it adds at least two weeks.

## India context
Read `references/india-compliance.md` when the developer or users are in India: DPDP Act notice and consent expectations, grievance contact, children's data, payments and lending declarations.

## Output style
Plain language. A new developer should understand every line without having read the policy. Lead with blockers, give the exact file and line or setting to change, and explain *why* it matters in one sentence. Do not pad with generic advice.

## When not to use this skill
Pure coding help unrelated to publishing, iOS App Store review (different rules; say so and offer general advice only), and legal opinions on specific disputes.
