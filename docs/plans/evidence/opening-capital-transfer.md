# Packet7 — retained opening-capital transfer

Status: existing opening workflow verified; packet7 remains open.

Owners: `apps/api/src/application/sie/historical-basis.ts` prepares, refreshes and
posts the opening; `apps/api/src/application/posting-corrections.ts` owns its
reviewed reversal/replacement. No new subscription or registration owner is added.

## Independently specified journey

The retained synthetic SIE original declares bank12500000, capital-2500000 and
shareholder loan-10000000 minor units at opening. It separately contains a1000
bank/loan movement. Choosing opening-set transfers only the opening controls;
it does not also import that movement or claim company/shareholder legal facts.

Ordinary REST intake retains the original, preview, mapped independent controls,
staged source run and opening proposal. Wrong source digest and a foreign book
with the same account identifiers refuse. Refresh preserves the controls while
superseding the proposal; an approval of the old proposal cannot execute it.

A real PostgreSQL fault on the historical-basis voucher checkpoint returns an
outcome-unknown error and leaves0 vouchers. The original command key then retries
successfully and replays exactly, leaving1 voucher. Ordinary basis reads recover
the source plan/digest, controls and voucher identity. A second opening or a
full-history basis over the same book refuses AlreadyPosted.

The independent correction intent leaves bank12500000 unchanged, changes capital
to-3000000 and loan to-9500000. Its exact impact review is required before sealing;
then approval and execution retain the original, reversal and replacement.
Same-key replay preserves one correction receipt and3 total vouchers. The original
basis remains historical evidence, not a rewritten assertion of current balances.
Correction reads expose the retained receipt and original voucher relationship.

## Repeatable artifact

Run:

```sh
OPENERP_E2E_ARTIFACTS=test-results/opening-funding-batch-acceptance-20261002 bun run test:e2e apps/api/tests/opening-capital.e2e.test.ts apps/api/tests/owner-funding-admission.e2e.test.ts apps/api/tests/period-work-batch.e2e.test.ts
```

13/13 cases pass without skips; source inventory is stable:
`fe53f4798c9430fe26ed6366ca32b08d18510bf9e0e8d9016e287123980fa6f1`.
JSON/JUnit reports and before/after opening-lineage artifacts live in that directory.
`bun run check:changed:full` passes for the added journey.

## Remaining acceptance

Native funding/repayment correction and already-posted-cash adoption remain open
under [owner funding admission](owner-funding-admission.md). This opening does not
adopt the historical loan into repayable owner-register capacity or create legal
share rights. Those missing relationships cannot be hidden by a generic journal.
The original packet asks for opening transfer and composed funding owners, not
NEXT-119's separately designed new share-issue product. This proof does not assert
NEXT-119 delivery, real company qualification or five completed packets.
