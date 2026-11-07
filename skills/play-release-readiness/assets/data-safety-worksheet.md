# Data safety worksheet for [[APP_NAME]]

Fill this in before opening the Data safety form in Play Console. Use `references/sdk-data-map.md` to find what SDKs collect. Data collected by any SDK in your app counts.

## Step 1: Does any data leave the device?
- [ ] Yes (continue)
- [ ] No (then "no data collected" may be correct; confirm no ads, analytics, crash reporting, accounts, or network calls with user data)

## Step 2: Data types

| Category / type | Collected? | Shared with third parties? | Required or optional | Purposes (choose) | Source (app / SDK name) |
|---|---|---|---|---|---|
| Personal info: name | | | | | |
| Personal info: email address | | | | | |
| Personal info: user IDs | | | | | |
| Financial info: purchase history | | | | | |
| Location: approximate | | | | | |
| Location: precise | | | | | |
| Photos and videos | | | | | |
| Files and docs | | | | | |
| Contacts | | | | | |
| App activity: interactions | | | | | |
| App info and performance: crash logs, diagnostics | | | | | |
| Device or other IDs (advertising ID, instance ID) | | | | | |
| Messages | | | | | |
| Audio | | | | | |

Purposes to choose from: App functionality, Analytics, Developer communications, Advertising or marketing, Fraud prevention/security/compliance, Personalization, Account management.

## Step 3: Security practices
- [ ] Data encrypted in transit (HTTPS)
- [ ] Users can request data deletion  -> URL: [[DELETION_PAGE_URL]]
- [ ] In-app deletion available (if accounts exist)
- [ ] Follows Families Policy (only if targeting children)

## Step 4: Consistency check
- [ ] Privacy policy lists the same data and purposes
- [ ] AD_ID permission matches the ads/analytics answers
- [ ] No SDK was added since this worksheet was filled in
