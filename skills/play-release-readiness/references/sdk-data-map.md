# SDK to data-collection map (for Data safety and privacy policy)

Data collected or sent by an SDK inside your app counts as data your app collects. This table lists *typical* behaviour so you can prepare honest answers. It is a starting point: confirm in each vendor's own Data safety guidance, which Google and many vendors publish, and in your actual configuration (for example analytics collection can be disabled).

| SDK / package | Typical data | Data safety hints | Also remember |
|---|---|---|---|
| Firebase Analytics (`firebase-analytics`, `firebase_analytics`) | App interactions, device and other IDs, diagnostics | Collected; purpose Analytics | Mention in privacy policy; AD_ID permission if ads personalization is on |
| Firebase Crashlytics | Crash logs, diagnostics, device/installation IDs | Collected; purpose App functionality / Analytics | Mention in policy |
| Firebase Auth, Google Sign-In, Credential Manager | Email, name, user IDs | Collected; linked to user | Account deletion requirement |
| Firebase Cloud Messaging / OneSignal | Device or push token | Collected | Notification permission on Android 13+ |
| AdMob (`play-services-ads`, `google_mobile_ads`) | Advertising ID, IP-derived location, app interactions, device info | Collected and shared; purpose Advertising | Declare ads; AD_ID; consent for EEA/UK (UMP); children rules; use test ads only in debug |
| Facebook / Meta SDK | Device IDs, events | Collected and shared | Keep App Events minimal |
| Play Billing (`billing`, `in_app_purchase`) | Purchase history | Collected (purchases) | Use the minimum supported Billing Library version |
| Location (`play-services-location`, `geolocator`) | Precise or approximate location | Collected | Least precision, foreground only, policy disclosure |
| Camera/media (`camera`, `image_picker`) | Photos/videos, if uploaded | Collected only if sent off device | Say whether processing is on-device |
| ML Kit text recognition, TFLite (on-device) | Typically none leaves the device | Not collected if truly on-device | Cloud-based ML Kit/Vertex AI calls do send data |
| Generative AI APIs (`generativeai`, Firebase AI, any LLM API) | Prompts, user content sent to a third party | Collected and possibly shared | Disclose; user consent; Play's rule on third-party AI integrations |
| Sentry, Bugsnag | Crash logs, device info | Collected | Mention in policy |
| Mixpanel, Amplitude, PostHog | Events, IDs | Collected | Mention in policy |
| AppsFlyer, Adjust, Branch | Attribution, device IDs | Collected and shared | Mention in policy |
| Razorpay, Stripe, PayU (payments) | Payment info handled by provider | Provider processes card data; you may still collect purchase/contact info | Keep card data out of your own servers |
| Room, SQLite, DataStore, Hive, Isar (local only) | Data stays on device | Not collected unless synced or sent | Say "stored on your device" |
| Retrofit/OkHttp/Dio (network clients) | Depends on your backend | Declare whatever you send | Use HTTPS only |

## Data safety answering approach
1. List every kind of data the app or any SDK sends off the device.
2. For each: is it collected, is it shared with a third party, is it required or optional, what is the purpose, is it encrypted in transit, can users request deletion.
3. Set "no data collected" only if nothing leaves the device. Apps with ads or analytics almost never qualify.
4. After release, re-check whenever an SDK is added or upgraded.
