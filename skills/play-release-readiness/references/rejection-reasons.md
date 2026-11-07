# Common rejection and suspension causes (and fixes)

Use this to translate a Play Console rejection email into a plain-language cause and the smallest correct fix. The email names a policy and usually a violation reference; check **Play Console > Policy status** for details. Fix the real cause, then resubmit with a short, factual note. Resubmitting unchanged repeats the rejection and can hurt the account.

| Cause | Typical trigger | Fix | Prevent it by |
|---|---|---|---|
| Missing or broken privacy policy | URL 404s, is a PDF, is geo-blocked, or does not name the app/developer | Host a public HTML page; add the same URL in Play Console and in-app | Template in `assets/`, test the URL in a private window |
| Data safety mismatch | SDKs (ads, analytics, crash) collect data the form says is not collected | Update the form to match the SDKs; update the privacy policy | `sdk-data-map.md`, run the scan script |
| Permission not justified | Sensitive permission with no declaration, or used for non-core features | Remove it or complete the permission declaration; use the photo picker / contact picker / scoped access | `permissions-guide.md` |
| App access blocked | Reviewer cannot get past login | Add demo credentials and steps under App access | Create a reviewer account that never expires |
| Crash or broken core feature | Crash on launch on new Android versions; features need unavailable server | Fix and test on real devices and in Pre-launch report | Test on API 36 and a low-end device |
| Deceptive claims / metadata | "Best", "#1", fake ratings, speed-booster or "virus cleaner" claims that the app cannot deliver; keyword stuffing | Rewrite title, description, screenshots truthfully | `aso-listing-writer` skill |
| Ads policy | Disruptive full-screen ads, ads that mimic system UI, ads shown on exit/launch unexpectedly, wrong ads declaration | Follow ad placement rules; declare ads; use AdMob test ads only in debug | Scan flags test IDs |
| Minimum functionality / spam | WebView wrapper with no added value, template apps, many near-identical apps | Add real native functionality or do not publish | Check the app has a clear unique purpose |
| User-generated content | Chat, posts, uploads without reporting, blocking, and moderation | Add in-app report/block, terms, moderation process | Terms template; UGC checklist in playbook |
| Impersonation / IP | Name or icon resembles another brand; uses logos you do not own | Rename and replace assets | Search the store for similar names before launch |
| Families / children | App appeals to kids but includes ads or analytics that are not allowed, or the audience declaration is wrong | Correct target audience; remove non-certified SDKs or do not target children | Declare audience honestly |
| Financial / lending apps | Loan or investment features without the required declaration and documents | Complete the Financial features declaration and provide licences | `india-compliance.md` |
| Account deletion missing | Users can sign up but not delete their account/data | Add in-app deletion and a public web deletion request page | `account-deletion-page-template.md` |
| Target API / technical | Uploaded bundle targets an old API, wrong signing, duplicate versionCode, `com.example` package | Raise targetSdk, fix signing/versionCode/package | Scan script |
| Production access denied | Closed test had too few active testers or little real usage | Keep 12+ testers opted in, ask for feedback, fix issues, fix answers in the questionnaire, re-apply | Playbook day plan |
| Account-level action | Repeated violations, linked accounts, inactivity, payment or identity problems | Follow the appeal path in the notice; provide correct identity documents | Keep contact info and verification current |

## Appeal and resubmission tips
1. Read the exact policy text cited; do not guess.
2. Fix everything that matches, not only the first example in the email.
3. Describe what changed in two or three sentences; do not argue or copy long policy text.
4. Use the appeal form only if you believe the decision was wrong; otherwise submit an update.
5. Keep a changelog of rejections and fixes for the next release.
