# Current Google Play requirements

**Last verified: 2026-11-07.** Dates below were checked against official pages where possible; items marked (secondary) came from developer-news sources and should be confirmed on the official page before you rely on them. Always re-check before a release.

Official sources to consult first:
- Policy announcements and deadlines: https://developer.android.com/distribute/play-policies
- Target API requirement: https://support.google.com/googleplay/android-developer/answer/11926878
- Testing requirements for new personal accounts: https://support.google.com/googleplay/android-developer/answer/14151465
- Android developer verification: https://developer.android.com/developer-verification
- Developer Program Policy centre: https://play.google/developer-content-policy/

## Date-bound requirements
| Topic | Requirement | Date | Notes |
|---|---|---|---|
| Target API level | New apps and app updates must target Android 16 (API 36) or higher. Wear OS / Automotive: API 35. TV / XR: API 34. | Since 2026-08-31 | The extension window to 2026-11-01 has closed. Existing apps must target API 35+ to stay visible to new users on newer Android versions. Expect the next bump around 2027-08-31 (verify). |
| Closed testing (new personal accounts) | Personal accounts created after 2023-11-13 must run a closed test with at least 12 testers opted in continuously for 14 days, then apply for production access. | Ongoing | Organization accounts are exempt but need verification (often a D-U-N-S number, which can take weeks). Internal and open tracks do not satisfy it. Google may ask for more testing if engagement is low. |
| Android developer verification | Developers must be verified and apps registered. Play developers with completed verification are mostly auto-registered; check Play Console Home for any unregistered apps. | Enforcement started 2026-09-30 in Brazil, Indonesia, Singapore, Thailand; global rollout 2027+ | India was not in the first phase. Do not wait: register now to avoid removal later. |
| Contacts permissions | Apps that do not need broad contact access should use the Android Contact Picker; broad access needs a Play Developer Declaration. | 2026-10-28 | Pre-review checks appear in Play Console. |
| Location permissions | Location button recommended as minimum scope for precise location; request the least precision needed. | 2026-10-28 | |
| Account transfer | Use the official "Transfer ownership" flow in Play Console. | 2026-10-28 | |
| Geofencing | Geofencing is no longer an approved foreground-service use case; use the Geofence API. | 2026-09-30 | |
| Third-party AI integrations | User Data policy (limited use, disclosure, consent) explicitly applies to third-party AI SDKs/APIs the app sends user data to. | July 2026 update | Applies to any LLM or AI API call. |
| Anonymous/random chat apps | Child Safety Standards and Age-restricted content rules expanded; Families policy prohibits targeting children. | 2026 update | |
| Play Billing Library | A minimum Billing Library version is enforced for updates. (secondary) | 2026-08-31, extendable to 2026-11-01 | Confirm the current minimum in the Play Billing docs. |
| Payments KYC (India) | RBI rules require India-based developers to complete merchant KYC to receive cross-border payments; international sales pause otherwise. (secondary) | Deadline was 2026-09-15 | Relevant only if you sell paid apps/IAP to users outside India. Check Payments profile. |
| DPDP Rules, India | Core obligations (notice, consent, safeguards, breach intimation, children's data, erasure) become effective around 2027-05-13; Data Protection Board provisions already in force. | Phased: 2025-11 to 2027-05 | See `india-compliance.md`. |

## Standing requirements (not date-bound)
- Upload an Android App Bundle (.aab); use Play App Signing; keep the upload key safe.
- Package name is permanent and must not start with `com.example`; versionCode must increase with every upload.
- Privacy policy: public, active URL (not a PDF, not geo-blocked, not editable by others), linked in Play Console and consistent with the app.
- Data safety form: must match real behaviour, including all SDKs. Mismatches are a leading rejection cause.
- Account deletion: if users can create an account in the app, provide an in-app deletion path **and** a web link for deletion requests, declared in the Data safety form.
- App access: if any part of the app is behind login, give reviewers working demo credentials and steps in "App access".
- Content rating questionnaire and Target audience and content declaration must be completed truthfully; ads declaration if the app shows ads.
- Advertising ID: apps targeting Android 13+ that use it must declare the `com.google.android.gms.permission.AD_ID` permission.
- Sensitive permissions need a permission declaration and a core-functionality justification: `MANAGE_EXTERNAL_STORAGE`, SMS and Call Log, background location, `QUERY_ALL_PACKAGES`, `REQUEST_INSTALL_PACKAGES`, photo and video media permissions (use the photo picker where possible), full-screen intents, exact alarms.
- 16 KB memory page size support is required for apps with native code that target Android 15+ (verify the current enforcement date).
- Financial features declaration (and extra requirements for personal-loan apps), health apps declaration, and government-app declaration apply where relevant.
- Quality: crash-on-launch, ANRs, non-working core features and misleading descriptions are common rejection reasons even when paperwork is perfect.

## How to update this file
When rules change: edit the table row, set the date in "Last verified", and note the official URL. Keep rows factual and short; avoid opinions.
