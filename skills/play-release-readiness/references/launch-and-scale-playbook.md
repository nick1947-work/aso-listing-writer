# Launch and Scale Playbook for Android Developers

A step-by-step guide from first idea to a healthy, growing app on Google Play. Rule dates are in `current-requirements.md`; this file is about the order of work and good habits.

---

## Phase 0: Decide before you build

1. **Account type.**
   - *Personal account*: fastest to open, but if created after 2023-11-13 you must run a closed test with 12+ testers for 14 continuous days before production.
   - *Organization account*: exempt from that test, but needs business verification (often a D-U-N-S number, which can take weeks). Choose this if you have a registered business.
2. **Verify your identity** in Play Console and keep contact details current. Register your apps for Android developer verification (most Play apps auto-register; check Play Console Home).
3. **Pick the app's single job.** A clear, unique purpose avoids "minimum functionality" and spam rejections.
4. **Decide your data stance.** The less data you collect, the shorter your policy, the easier your Data safety form, and the lower your risk. Offline-first and on-device processing are real advantages.
5. **Pick a permanent package name** (`com.yourbrand.appname`, never `com.example`). It cannot change after publishing.

## Phase 1: Build for approval

- Set `targetSdk` to the current required level and test on the newest Android version and a low-end device.
- Use the **photo picker, Contact Picker, Storage Access Framework** instead of broad permissions. See `permissions-guide.md`.
- Log every SDK you add and what data it sends; you will need this for the Data safety form (`sdk-data-map.md`).
- If users can create accounts, build **in-app account deletion** from day one and a public web page for deletion requests.
- Use HTTPS only. Do not ship debug flags, test ad IDs, hard-coded secrets, or verbose logging.
- Shrink and optimise: enable R8/minify, ship an Android App Bundle, keep the install size small. Test cold start.
- Support the 16 KB page size if you ship native libraries.
- Handle edge cases: no network, permission denied, low storage, rotation, dark mode, back navigation.

## Phase 2: Paperwork (do this while you build, not at the end)

| Item | Where | Notes |
|---|---|---|
| Privacy policy | Public web page (GitHub Pages works) | Template: `assets/privacy-policy-template.md` |
| Terms and conditions | Public web page and in-app | Template in `assets/` |
| Account deletion page | Public web page | Needed if accounts exist |
| Data safety form | Play Console > App content | Use `assets/data-safety-worksheet.md` |
| Content rating | Play Console > App content | Answer truthfully |
| Target audience and content | Play Console > App content | Declare kids status honestly |
| Ads declaration | Play Console > App content | Yes if the app shows ads |
| App access | Play Console > App content | Reviewer credentials if login is needed |
| Permission / sensitive declarations | Play Console | Only for restricted permissions you truly need |
| Store listing | Play Console > Store presence | Use the `aso-listing-writer` skill |

## Phase 3: Test (the 14-day plan for new personal accounts)

| Day | Action |
|---|---|
| -7 to 0 | Create the closed testing track, upload a release-quality AAB, prepare a tester message with the opt-in link. Recruit 15-25 people so drop-outs do not break the 12-tester minimum. |
| 1 | Testers opt in and install. Verify the count in Play Console. |
| 2-13 | Ask testers to use the app on different days, report issues, and rate flows. Ship at least one update from their feedback. Keep a simple log of changes. |
| 14 | Confirm 12+ testers have been opted in continuously. Apply for production access and answer the questionnaire with specifics about testing and fixes. |
| 15+ | Wait for review; fix anything Google asks. If testing restarts, keep the same testers. |

Tips: use real people and honest feedback; avoid services that sell fake testers (they can get an account flagged). Internal and open tracks do not satisfy the requirement.

## Phase 4: Pre-submission checklist

Run the readiness scan and report from the `play-release-readiness` skill, then confirm by hand:
- [ ] Release build, signed with your upload key, Play App Signing enabled
- [ ] Unique, increasing `versionCode`; correct `versionName`
- [ ] Targets the required API level
- [ ] No test ad IDs, no debug flags, no secrets in the APK
- [ ] Privacy policy and deletion URLs load in a private browser window
- [ ] Data safety answers match the SDKs and the policy
- [ ] Reviewer login works and is documented
- [ ] Screenshots, icon, feature graphic match the real app; no misleading claims
- [ ] Pre-launch report in Play Console has no critical crashes
- [ ] You can answer: "What does this app do that a WebView of a website would not?"

## Phase 5: Release safely

1. Use a **staged rollout** (for example 5%, 20%, 50%, 100%).
2. Watch **Android vitals** (crash and ANR rates) and Crashlytics for the first 48 hours. Halt the rollout if rates jump.
3. Reply to reviews, especially bug reports. Use the in-app review API after a positive moment, never on first launch.
4. Keep a rollback plan: the previous build stays available as the base for a hotfix.

## Phase 6: Scale

**Engineering**
- Modularize by feature as the codebase grows; keep domain logic free of UI and Android classes.
- Use remote config and feature flags to ship safely and run experiments.
- Automate: CI on every pull request (build, lint, unit tests, the readiness scan), and release automation with a tool such as Gradle Play Publisher or Fastlane.
- Add baseline profiles and track startup, jank and app size as release gates.
- Offline-first with a sync layer (Room/Flow, WorkManager) makes quality and privacy easier at scale.

**Quality and monitoring**
- Crash reporting, vitals dashboards, and alerts on regressions.
- Test on a device matrix that matches your actual users (low-RAM Android devices are common in India).

**Growth**
- Treat the store listing as a product: run Store listing experiments, localize (Hindi and regional languages), refresh screenshots each release. Use the `aso-listing-writer` skill.
- Write release notes users can understand; keep a public changelog.
- Build a feedback loop: in-app feedback link, support email, and a public roadmap.

**Monetization**
- Start with the least intrusive model that fits (paid features, subscription, or well-placed ads). Declare ads and billing correctly; keep the Billing Library current.
- Never gate core privacy or deletion features behind payment.

**Compliance at scale**
- Revisit privacy policy and Data safety every time you add an SDK or feature.
- Prepare for DPDP obligations (India), and GDPR/UK GDPR if you have EU/UK users; consent screens for ads where required.
- If revenue becomes meaningful, move to an organization account and use the official account transfer flow.

**Security and account hygiene**
- Turn on 2-step verification for the Play account, limit users and roles, back up your upload key, and keep payment and identity details up to date.
- Never share your Play account credentials with freelancers; invite them with limited roles.

## Phase 7: Maintain every year
- Each spring/summer, check the next target API deadline and raise `targetSdk`; migrate away from deprecated APIs early.
- Re-run the readiness scan before every release.
- Remove unused permissions and SDKs; each one is future risk.
- Keep the app updated at least periodically; abandoned apps lose visibility.

## Common mistakes to avoid
1. Waiting until the last day to write the privacy policy and fill the Data safety form.
2. Declaring "no data collected" while shipping ads or analytics.
3. Using broad storage or media permissions when a picker would work.
4. Forgetting reviewer credentials and getting rejected for "app not working".
5. Starting the 14-day test late and missing a launch date.
6. Using someone else's name, logo, or screenshots.
7. Resubmitting the same build after a rejection without fixing the cause.
8. Treating rules as permanent: they change every year.
