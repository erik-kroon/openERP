# Six-books A slice: recognition PASS, two credit/service boundaries

Observed 2026-09-29 on the current worktree (HEAD `16a532c` plus the in-progress
`party-identity` work) through the **real** Worker and the **real** restricted
`e2e_runtime` role on a disposable per-run PostgreSQL cluster, driven over HTTP
into the named application owners. No oracle journal was imported, no manual SQL
repaired a financial result, and no provider was called. The Book A inputs come
from the synthetic `openerp-six-books/v2` challenge bundle only.

Reproduce with `bun run test:e2e apps/api/tests/six-books/`. Artifacts land in
`test-results/e2e/six-books-*.json`. The fiscal year is the corpus actual year
`2025-05-17…2026-04-30`, provisioned as a synthetic fixture per book.

## What passed

| Case                                          | Observation                                                                                                                                                                                                                                                                                                        |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `A005` two-line domestic purchase (A-P01)     | Recognized through `counterparties → supplier-invoice-drafts → supplier-acceptance-reviews (swedish-purchase-v1) → approvals → execute`. Invoice `2000000`, outstanding `2000000`, two tax facts with deductible total `400000`, per-line capacities `1000000/250000` and `600000/150000`, trial balance balanced. |
| Single-line partial supplier credit (control) | Invoice `1250000` (`1000000` net + `250000` tax), credit `625000` (`500000` + `125000`) executed. Outstanding `625000`, capacity remaining `500000` net / `125000` tax, ledger balanced.                                                                                                                           |
| A-CAP retention and Book A admission          | Loopback-only harness, A-CAP bytes retained and read back, `A001` correctly `BLOCKED_UNSUPPORTED` (NEXT-119 has no owner), `A002` `owner_loan` refused `422 InvalidJournal` with the corpus date outside the fixture year.                                                                                         |

## Finding 1 — a multi-line recognition cannot take a supplier credit (regression)

`apps/api/src/application/purchases/credit-basis.ts:524` requires
`action.lines.length === original.length + 1 + (deductible > 0n ? 1 : 0)`, and
`credit-basis.ts:521` requires a **single** input-VAT debit equal to the whole
deductible total. The NEXT-03 recognition compiler posts VAT **per source line**,
so a two-line A-P01 recognition journals five lines (expense, VAT, expense, VAT,
payable) against two plan lines. Both conditions fail and prepare refuses
`409 StaleDependency` even though every freshness field matches — the live
invoice reports `status=open`, `blockers=[]`, `outstandingMinor=2000000`,
`allocationVersion=0`, `revision=1`, and the acceptance digest is the one the
credit request supplies.

The single-line control in the same run passes, which isolates the defect to the
line-count and VAT-aggregation checks rather than to credit cardinality, amounts
or capacity.

**This contradicts an existing recorded observation.** The 2026-09-24 run in
`ap-partial-line-credit-http.md` credited a line of a _two-line_ invoice
successfully. `git blame` puts both guard conditions in `1245089` (NEXT-03,
2026-09-26), after that run, in the same commit that introduced the per-line VAT
journal shape. The 2026-09-24 artifact therefore does not reproduce on current
HEAD for a multi-line invoice and must not be read as current proof for that
case.

Repair options, for the credit owner's decision rather than an unowned guess:

1. Verify the posted voucher against the recognition's own sealed
   `plan.journal` instead of a re-derived line count and an aggregated VAT debit.
2. Or keep the per-line identity but count one VAT line per taxable source line
   and compare the VAT sum rather than a single line.

Both keep the guard's intent — the credit may only release a deduction the
original recognition actually recorded. Neither belongs to a verification
harness, so this change records the defect and does not alter the owner.

## Finding 2 — a foreign-currency service purchase cannot stage its own units

`apps/api/src/application/purchases/service-purchases.ts:400` requires each
assignment's `originalNetMinor` and `originalCurrency` to equal the retained draft
line, while `apps/api/src/application/purchases/draft-calculation.ts:181`
requires every supplier draft to be in the book currency. A EUR-native line
therefore can never be expressed: with the draft in SEK and the assignment in
EUR the owner refuses `422 InvalidJournal` at reconciliation, and the
`accountingRate`/`taxPointRate` witnesses that exist precisely to convert native
units are never consulted. With everything in SEK, reconciliation passes and the
owner refuses `UnsupportedProfile` at `service-purchases.ts:267` because no
qualified `rule_releases` row ships with this release, so
`readReleaseSelection` finds no `generalRuleServices` section.

The two gates are independent and both are recorded. The second is the designed
behaviour; the first is a structural contradiction between two owners, not a
missing qualification.

## Scope not claimed

Settlement, payroll, assets, FX remeasurement, the paid-credit/refund legs, VAT
returns and any annual close step remain unexercised here. `BLOCKED_UNSUPPORTED`
for those owners is recorded in the same artifacts rather than treated as
applicable. Real company qualification, the legal VAT profile and every external
provider gate stay open under D-04, D-08 and D-10.
