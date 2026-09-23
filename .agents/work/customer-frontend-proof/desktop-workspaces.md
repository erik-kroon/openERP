# Desktop workspace observations — 23 September 2026

This records manual browser observations of the implemented desktop UI, not a production or customer-acceptance verdict. No test files were added or changed. Mobile, assistive-technology and theme audits were outside this pass.

## Environment

- Local web: `http://127.0.0.1:3107`; Worker: `http://127.0.0.1:18790`.
- Isolated PostgreSQL database: `frontend_20260923` on the existing local preview PostgreSQL instance. Prior preview data was preserved. Versioned migrations were applied normally, without changing stored migration receipts.
- Local private original-file storage uses Wrangler's persisted R2 emulation, bound as `EVIDENCE_BUCKET`. No cloud bucket or deployment was created.
- Synthetic company/book: `entity_customer_demo` / `book_customer_demo`, “Northstar Studio · Demo”, SEK, 2026 period.
- The working tree changed concurrently with other accounting-domain work. `frontend-files.json` records hashes for the frontend files inspected by this pass; it does not claim a clean or immutable repository revision.

## Observed through the browser

| Journey | Result |
| --- | --- |
| Sign in → Overview | Company identity, zero journal-review count, one open period and actual ledger balances displayed. No invented financial data |
| Invoicing → Customers & suppliers → New contact | Saved “Linden Design AB”, reference `C-1001`, with one form submission. The entered facts were retained as evidence before the contact save |
| New invoice → customer selection → save | Selected the new customer by name; entered 12,000.00 SEK net and 3,000.00 SEK tax. Saved detail showed 15,000.00 SEK total |
| Reload invoice detail | The URL reopened the saved record and its amounts; live issue history was checked before enabling editing |
| Edit draft → save revision | Restored customer, dates, addresses and decimal values. Added unit price and demo identity references; saved an immutable revision without issuing or posting |
| Purchases → Documents → Upload | Uploaded a synthetic 247-byte text receipt. The first attempt found missing local object storage; after configuring the local binding, Retry upload reused the captured operation and succeeded |
| Document detail | Displayed the original text, filename, upload date and byte count beside Download original. Upload did not create a posting |
| Reports → Trial balance → Generate | Prepared and opened a saved 2026 report. Six accounts, zero vouchers and 0.00 SEK debit/credit were displayed, matching this unposted demo book |
| Report → Business account | Opened the account explanation and correctly showed no contributions for the zero-entry report. Nonzero contribution/evidence lineage was not exercised in this pass |
| Company menu → Change workspace | Opened the searchable directory with only the authorized demo book, latest period, journal-review count and observation time |
| Directory → period | Opened the correct scoped period. Its readiness read returned 11 of 14 checks, with expected-bank inventory, reconciliation and required closing areas outstanding. No lock was attempted |

Desktop screenshots were inspected for Overview, invoice entry/detail, document detail, report, directory and period readiness. No acceptance claim follows from those inspections.

## Reopen the retained examples

With the local services running and an authorized session:

- Invoice: `/entities/entity_customer_demo/books/book_customer_demo/sales?view=drafts&record=invoice_draft_65eec3cac12a412c9af371148f0a9148`
- Original: `/entities/entity_customer_demo/books/book_customer_demo/purchases?view=documents&record=source_570194e5c5f94775bb966e8bf301e887`
- Report: `/entities/entity_customer_demo/books/book_customer_demo/reports?view=trial&record=report_945793013d9f4eed874f3bdb11b9283a`
- Directory: `/companies`
- Period: `/entities/entity_customer_demo/books/book_customer_demo/closing?record=period_2026`

Repeat creation using a fresh synthetic contact reference and explicitly synthetic source. Reload the resulting detail URL and compare the displayed totals. Existing saved records are retained; do not replace migration history or delete prior preview data to repeat this observation.

## Checks and limits

The final build, web typecheck and type-aware lint over the changed frontend files are recorded in the task's local `.cache/customer-frontend/implementation-*.log` files. These are code checks, not accounting acceptance proof.

The remaining plan includes source-led preparation without the initial manual source note, full cross-domain work coverage, customer workflows for advanced domain controls, persisted assignments/shared views and firm relationships. The company directory does not manufacture a client relationship model. Invoice issuance remains subject to its domain's synthetic/live boundaries. Full plan and customer acceptance remain open in `docs/frontend.md`.
