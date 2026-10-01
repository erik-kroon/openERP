# Whole-year packet 8: bounded synthetic accrual slice

Implemented owner: `apps/api/src/application/purchases/supplier-settlements.ts`. This extends the previously integrated pending-review slice with real HTTP/MCP execution, joined native posting/match/allocation receipts and atomic latest same-open-period cancellation. It is **not complete packet 8** and does not activate a real-company rule.

## Observed proof — 2026-10-01

From `/Users/admin/.codex/worktrees/cash-period-admission/openERP`:

```sh
OPENERP_E2E_ARTIFACTS=test-results/takeover-supplier-20261001-r5 bun run test:e2e apps/api/tests/supplier-settlement.e2e.test.ts
OPENERP_E2E_ARTIFACTS=test-results/takeover-supplier-regression-20261001 bun run test:e2e apps/api/tests/posting.e2e.test.ts apps/api/tests/bank-match-integrity.e2e.test.ts apps/api/tests/supplier-refunds.e2e.test.ts apps/api/tests/cash-payment.e2e.test.ts
bun run check:changed:full
bun run check:integration
```

Supplier suite: **7 passed, 0 failed, 0 skipped**. Selected regression suite: **21 passed, 0 failed, 0 skipped**. Full changed-file gate passed; integration registry passed with 33 wired and 17 declared deferred leaves. Dependencies and lockfile are unchanged; the earlier frozen-install observation is not a new install claim.

Runtime: disposable PostgreSQL 17.11, actual restricted runtime role, local workerd, Vitest 4.1.10. Base revision `ed41a9705bad458a04b3d3324b7124bcf9eeabca` plus retained worktree changes; the supplier manifest records diff SHA256 `e5d1a4ade44932dcdce3fce41c5f77f5bf292e5a2bfdeef64087c20b464ae1fa`. Stable source inventory before/after: `3b5c0714af27cd4ba5aaa7384f475ea64c473817e61cab46d486d2f3d0515c34`, no changed paths. Manifest includes per-file and migration hashes, including forward migration `0053-supplier-settlement-execution.sql`. The exact source, not merely HEAD, owns this claim.

Artifacts reside in those two `test-results` directories: `manifest.json`, `source-integrity.json`, `results.json`, `postgres.log`, `worker.json`; supplier proof also retains `supplier-settlement-accrual.json` and pending proof. Reporter prints a JUnit path but no JUnit file was observed; do not claim one. Earlier failure artifacts in `takeover-supplier-20261001`, `-r2`, `-r3`, `-r4` remain intact.

## Independently specified outcomes

Accrued invoice 10000 minor units, observed bank debit -4000:

| State | Bank ledger | Expense | Payable | Vouchers/lines |
| --- | --- | --- | --- | --- |
| Prepared/approved | 0 | 10000 | 10000 | 1/2 |
| Executed | -4000 | 10000 | 6000 | 2/4 |
| Cancelled | 0 | 10000 | 10000 | 3/6 |

Cancellation preserves the original bank debit and permanent source claim. Real reconciliation reports difference -4000 and the source remains unavailable for a new settlement. Exact replay returns the retained receipts without another financial effect. Equal rows retain distinct identities; competing source/capacity plans produce one financial winner. Independently disabled reviewer authority refuses execution. Runtime history UPDATE/DELETE/TRUNCATE is denied; admin immutable and uniqueness probes exercise database integrity.

Five disposable rejecting-trigger boundaries exercise settlement match, allocation leg and parent receipt, then cancellation match reversal and parent receipt. Source logs show actual trigger errors; exact financial/counter/approval snapshots remain unchanged. Removing faults permits successful retry, including the full cancellation. These are bounded failure points, not every possible fault/race.

The takeover fixed native reversal defects uncovered on this real path: missing bank-plan command receipt, wrong array projection of released match legs, and nonexistent allocation-reversal execution/approval columns. Cancellation now admits only the invoice state produced by its exact settlement; a later invoice revision refuses before inverse preparation. Its red observation is retained in `-r4`.

## Remaining obligations and blocker

The bounded synthetic transaction works. The blocker to **whole packet acceptance** is incomplete qualification and coverage, not credentials or an outside reviewer: wider transaction populations and correction paths remain unsupported. Real-company activation still requires evidenced accrual/VAT methods and dated applicable rules (D-04/D-08). Cash, FX/fees, provider payment instructions, replacement/reassignment and cross-period/later-consumed correction are not released by this slice.

The larger first-unit design also retains obligations beyond these seven tests: exhaustive changed-rule/account/source and child-approval refusal vectors; explicit lock-order/revocation races; full cross-book relational constraint vectors; generic mutation probes on executed/cancelled children and bank-allocation preparation; complete retained fiscal-impact refusal coverage; paginated owner plan/receipt discovery and cancellation reads. No UI, whole-year journey, complete backup/restore or first-pass freeze/comparison proof is claimed. Packet 1 remains verified only at its recorded `375bea6` source.
