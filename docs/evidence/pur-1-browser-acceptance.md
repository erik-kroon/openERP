# PUR-1 browser acceptance — synthetic local book

This is execution evidence, not a legal-company or VAT activation. The original bytes are retained in a disposable R2 bucket; a disposable PostgreSQL 17 database is migrated through `8740-supplier-draft-source-history.sql`. The browser uses a local password account and a scoped operator book. The synthetic acceptance profile posts a zero-tax gross-cost draft; it does **not** establish supplier legal identity, VAT deductibility or payment.

## Repeat

From the repo root, with Node 26, Bun and PostgreSQL 17 available, run:

```bash
node --experimental-strip-types test-results/pur-browser-replay.ts
```

The ignored local runner creates and cleans up a fresh database, Worker, web server and browser session. It writes `test-results/e2e/pur-browser/receipts.json`, `connection.json`, `migrations.log`, desktop/mobile screenshots and logs. No existing company data is used. The runner is a local verification artifact, not a committed test change. If the ignored runner is absent, repeat the sequence below with a disposable local book and real browser; this document does not claim a CI browser gate.

## Observed flow

1. Sign in as a synthetic operator. Retain an original text document and a corrected text document. Create a synthetic supplier and an invoice draft with an explicit 100.00 SEK line and original-source evidence. The first original’s purchase links identify the current draft.
2. Open the source beside the editor at 1440 × 900 and 390 × 844. Open the saved draft at both widths.
3. Edit the draft and choose the corrected original. Intercept its first source-read request with HTTP 503. The editor shows **Retry original** while preserving the entered title; retry reveals the corrected original. Capture `read-error-mobile.png` and `replacement-editor-mobile.png`.
4. Revise the line and source total to 125.00 SEK, retain the reason, and save. The revision history contains revisions 1 and 2. The first original’s purchase link has `currentSource: false`; the corrected original’s link has `currentSource: true`.
5. Prepare, approve and execute the synthetic supplier acceptance. Reload the draft and open its posted review, then follow **Open registered invoice**. Expand **Inspect retained evidence**: the registered invoice shows the corrected original, **Download original**, and **Open work linked to original**. Capture posted draft and registered invoice at desktop and mobile widths. The invoice has a voucher receipt; it is not marked paid.

The local run on 2026-09-24 returned draft revision 2, a registered supplier invoice, a voucher, both source links and zero browser page errors. `receipts.json` retains IDs and digests without tokens or passwords. The source-read 503 and retry were exercised in the browser; unknown-outcome POST recovery was **not** fault-injected in this run. No accessibility audit or legal VAT acceptance is claimed.
