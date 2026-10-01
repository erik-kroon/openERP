# Cash commercial-document period admission

Local synthetic verification on 2026-10-01 repaired admission of the existing commercial-only cash supplier invoice. Migration `0048-cash-invoice-recognition-period.sql` runs `invoice_recognition_period_open` only when `recognition_voucher_id` is nonnull. The financial-period function, voucher trigger, recognition constraints and historical migration bytes remain unchanged.

The existing row contract has two variants. A recognized invoice retains its voucher and line. A commercial-only cash supplier invoice retains its reviewed source draft and has both recognition identifiers null. Applying the recognition-period lookup to the latter returned HTTP `422 InvalidJournal` because it has no recognition voucher. The repair changes the trigger predicate without adding a document-period admission policy.

## Independently specified expectations

Before the migration, the E2E specified gross `125000`, net `100000`, VAT `25000`, null recognition and outstanding `125000`. Admission and replay create zero vouchers, journal lines, purchase recognitions, purchase tax facts, cash lines and cash recognition rows. The voucher counter remains `0`, and replay preserves population version `1`.

The added regression locks the document's period before admission. It also requires SQLSTATE `23514` from `commerce_recognition_shape` for ordinary null recognition, a cash invoice without its draft, and each mixed nullable recognition pair. The existing DF-08 tests require HTTP `409 PeriodLocked` for a final voucher write and a final recognized-invoice write after their actual period becomes locked.

## Observed evidence

The complete test-first commit `0c59dbb` reproduced HTTP `422 InvalidJournal`. Its artifact directory is `test-results/cash-period-test-first-red-20261001`. The first pre-migration reproduction is retained separately in `test-results/cash-period-red-20261001`.

Implementation revision `5c12de580fa6c4cfc74fc03e68e0a566cf422d25` passed 50 tests across cash invoice, payment, year-end, credit, register, period-lock and persistence E2E files. Its artifact directory is `test-results/cash-period-fixed-20261001`. `source-integrity.json` reports `stable` with no changed paths. `manifest.json` retains the revision, source inventory, migration checksums and runtime identity. `cash-commercial-period-admission.json` retains the direct positive and negative results. `df-08-vouchers.json` and `df-08-commerce_invoices.json` retain the financial guards.

The existing payment and year-end tests also passed the `50000` payment and `75000` unpaid recognition journey, next-year settlement without new VAT or recognition journal, stale membership, backdated original refusal, empty-year assessment and financial-close receipt gates. These are focused observations, not broad whole-year qualification or company applicability.

Frozen installation, changed-source checks, type-aware changed-source checks and `check:integration` passed. Gate logs are in `test-results/cash-period-gates-20261001`. Migration replay preserved posted state, and checksum drift refused the migrator. The new migration SHA-256 is `9997994f777c091bfb668c24af3283d4b7cc49a147a71e236983f1d93034fee2`.

Run the same focused proof with an unused artifact directory.

```sh
OPENERP_E2E_ARTIFACTS=test-results/cash-period-repeat bun run test:e2e apps/api/tests/cash-invoice.e2e.test.ts apps/api/tests/cash-payment.e2e.test.ts apps/api/tests/cash-year-end.e2e.test.ts apps/api/tests/cash-credit.e2e.test.ts apps/api/tests/cash-register-report.e2e.test.ts apps/api/tests/period-lock-integrity.e2e.test.ts apps/api/tests/persistence.e2e.test.ts
```

The next qualification step is the unchanged broad integrated E2E run on a frozen revision that includes this repair. No real company data, live provider, deployment or statutory submission was used.
