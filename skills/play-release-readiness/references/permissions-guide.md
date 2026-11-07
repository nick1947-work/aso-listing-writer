# Permissions guide

Request only what the app needs, as late as possible, with a clear reason shown to the user. Each sensitive permission is both a user-trust issue and a policy issue.

| Permission | Why it is risky | Declaration/policy | Prefer instead |
|---|---|---|---|
| `MANAGE_EXTERNAL_STORAGE` (All files access) | Broad file access | Permission declaration; only for core uses like file managers, backup, antivirus | Storage Access Framework, MediaStore, scoped storage |
| `READ_MEDIA_IMAGES`, `READ_MEDIA_VIDEO` | Broad media access | Photo and video permissions policy; must be core functionality | System photo picker (no permission) |
| `READ_SMS`, `RECEIVE_SMS`, `SEND_SMS`, `READ_CALL_LOG` | Highly sensitive | Only for default handler or narrow exceptions; declaration required | SMS Retriever / User Consent APIs |
| `ACCESS_BACKGROUND_LOCATION` | Tracks location when app is closed | Declaration, in-app disclosure, video demo | Foreground location; location button; Geofence API |
| `ACCESS_FINE_LOCATION` | Precise location | Data safety; request least precision needed | Coarse location or the location button |
| `READ_CONTACTS` | Broad contacts access | Contacts permissions policy (Oct 2026); declaration for broad access | Android Contact Picker |
| `CAMERA`, `RECORD_AUDIO` | Sensor access | Disclose in privacy policy; runtime request in context | Intent to system camera if you do not need custom UI |
| `QUERY_ALL_PACKAGES` | Lists installed apps | Declaration; only for specific core uses | `<queries>` element for named packages |
| `REQUEST_INSTALL_PACKAGES` | Installs other apps | Restricted use | Avoid |
| `SYSTEM_ALERT_WINDOW` | Overlays | Restricted; often rejected | Avoid, use notifications |
| `USE_FULL_SCREEN_INTENT` | Interrupts users | Allowed for calls/alarms only | Normal notification |
| `SCHEDULE_EXACT_ALARM` / `USE_EXACT_ALARM` | Battery impact | Only for alarm/calendar-type apps | Inexact alarms, WorkManager |
| `FOREGROUND_SERVICE_*` | Needs a declared type and use | Foreground service declaration with justification | WorkManager for deferrable work |
| `com.google.android.gms.permission.AD_ID` | Advertising ID | Must be declared (or removed) when targeting Android 13+ and using ads/analytics | Remove if truly unused |
| `POST_NOTIFICATIONS` | Spam risk | Runtime prompt on Android 13+ | Ask after value is shown |
| `INTERNET`, `ACCESS_NETWORK_STATE` | Normal | None | N/A |

## Rules of thumb
- If a feature works without the permission, drop the permission.
- A permission in a library's manifest merges into yours. Check the merged manifest (`app/build/intermediates/merged_manifests`) for surprises.
- Show an in-app explanation before system prompts for sensitive permissions, and make the app usable if the user says no.
