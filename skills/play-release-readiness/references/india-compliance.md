# India compliance notes

General information for developers, not legal advice. Consult a lawyer for specific questions.

## DPDP Act 2023 and DPDP Rules 2025
- The Rules were notified in November 2025 with a phased timeline; the main duties on organizations that decide why and how personal data is processed (notice, consent, security safeguards, breach intimation, children's data, erasure) are expected to apply from around May 2027. Verify current dates before relying on them.
- **Notice**: clear, plain-language, standalone; itemize the personal data collected and the purpose; give a way to withdraw consent as easily as it was given, to exercise rights, and to complain to the Data Protection Board.
- **Consent**: specific, informed, tied to the stated purpose. Do not bundle optional processing with essentials.
- **Children**: under-18 users generally need verifiable parental consent before processing their data. If your app is not meant for children, say so and do not target them.
- **Safeguards and breaches**: use reasonable security (encryption in transit, access control); have a process to notify affected users and the Board after a breach.
- **Retention and erasure**: keep data only as long as needed; let users request deletion.
- **Grievance contact**: publish a named contact (an email is enough for a small developer) and respond within a reasonable time.

Practical effect for an indie app: a privacy notice that lists data and purposes, a visible withdraw/delete path, a contact email, honest handling of children, and minimal data collection. Offline-first and on-device processing make most of this easier.

## Payments and finance
- Receiving international payments through Play may require merchant KYC in India; check **Payments profile** in Play Console.
- Lending, investment, insurance, and payment apps need Play's Financial features declaration and often regulatory documents (for example NBFC registration for lending). Personal-loan apps face extra Play requirements. Do not publish a lending app without the licences.
- Do not imply affiliation with UPI, NPCI, RBI, the government, or banks. State compatibility factually.

## Other practical points
- GST and tax on earnings are separate from Play policy; get an accountant once revenue starts.
- Support Hindi and regional languages in the UI and the policy summary when your audience needs it; the legally binding text should be one clear version.
- Keep a bilingual contact page if users are mostly regional-language speakers.
