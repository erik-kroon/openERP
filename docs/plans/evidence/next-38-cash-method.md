# NEXT-38 cash-method recognition and unpaid year-end cutover

**Status: wired and observed 2026-09-29.** Real E2E over workerd + PostgreSQL
17.11 + the restricted `e2e_runtime` role, with the source inventory stable
across the run.

## What the packet needed

The leaf in `packages/domain/src/cash-method.ts` calculates a payment's
recognition split and a year-end's unpaid cutover. It was reviewed and repaired
in `fc47b27`, which distinguished paid from recognized from credited coverage and
made the component policy explicit and gross-conserving, but nothing composed
it. This packet gives it a named owner rather than a second owner.

## The owner

`apps/api/src/application/commerce/cash-method.ts` composes the leaf at two
boundaries inside the existing commerce invoice owner, because a cash-method
document is an invoiced document. It is not a new engine:

- The caller names a line, an amount, a cash-evidence reference and a basis. It
  never states a net, a tax or a split.
- The net/tax split is read from the retained recognition voucher's journal
  lines, with the control line identified by the recognition line the invoice
  owner already retained. A cash-method document posts its gross against a net
  and a tax, so the non-control sides must sum to exactly the control gross; the
  net is the largest of them and the tax is what remains. A voucher that does
  not balance that way is refused rather than guessed at.
- The commercial gross is the invoice's own amount, so commercial unpaid is
  `gross - credits - paid` and recognized unpaid is
  `recognized gross - paid`. The two are reported separately and never merged.

`apps/api/src/db/commerce/cash-method.ts` holds the reads, all passing the
caller's transaction. `0040-next-38-cash-method.sql` retains the recognized
prefix per line, the append-only recognition history naming the trigger that
caused it, and at most one cutover run per period. The line advances one
version under the version the writer observed, so two concurrent recognitions
cannot both succeed. Recognition journals are prepared through the released
prepare/approve/execute boundary, so responses report `journalIds: []` and the
cash effect is not committed by this packet.

## What the E2E proves

1. **A payment recognizes without changing what is owed.** Paying 500 of a 1250
   document recognizes 500, composed as 400 net and 100 tax by the leaf's
   cumulative tax-first policy. Commercial unpaid falls to 750 while recognized
   unpaid is 0, because the payment covered everything the book had taken. The
   recognition is prepared, not executed: the book has no bank voucher. The
   same payment under a different command key still refuses, because the
   trigger is the payment's own retained identity rather than the command.
2. **A year end recognizes the unpaid remainder once per period and never
   again.** The same document is carried into a year end, the cutover run
   recognizes 1000 with its journal prepared, and the commercial balance is
   unchanged at 1000 — the customer still owes, which is the whole point of the
   method. A second year end for the same period refuses.
3. **A line with no reviewed witness is not a cash-method line.** The witness is
   the recognition voucher and line the invoice owner retained; a document
   without one never becomes a cash-method line.

## Bounds

No vendor invoice import, no payment reconciliation, no year-end close
workflow and no VAT return line exists. The leaf is composed at two
recognition boundaries only. `bun run check:integration` reports 31 wired and
17 declared deferred; the full E2E suite passes 170 tests across 42 files.
