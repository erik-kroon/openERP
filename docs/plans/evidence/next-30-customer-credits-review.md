# NEXT-30 customer unapplied cash, paid credits and refunds — delivery evidence

Baseline: `0aef73c`. Scope is this evidence file and the nine files listed under
_Changed files_. This delivers a previously deferred leaf: the
`customer-credits` entry in `docs/plans/domain-leaf-integration.json` moves
from `deferred` to `wired` because a real application owner now composes it.

The existing customer-credit owner covers NEXT-15's unpaid-credit scope. This
is the complementary NEXT-30 scope the packet names: the customer-side surplus
and paid-credit lifecycle. It extends the same commerce lane rather than
rewriting the existing owner.

## What was wired

The leaf already had correct pure rules and **no consumer**. It now has:

- a named application owner, `apps/api/src/application/commerce/customer-receipts.ts`,
  with five operations: prepare and execute a receipt, apply credit, refund
  credit, and read an origin;
- tx-passing persistence in `apps/api/src/db/commerce/customer-receipts.ts`;
- two tables in `apps/api/migrations/0034-next-30-customer-credits.sql`;
- the wire contract inside the existing `CustomerCreditNotesApi` group and the
  handlers inside the existing `CustomerCreditHandlers` group;
- a focused E2E over real workerd, PostgreSQL and the restricted runtime role.

No `api.ts`, `index.ts`, `contracts/package.json` or capability registration
was touched. One member, `customer_receipt`, was added to the shared
`PostingOwner` union so the posting kernel attributes the voucher to its real
owner rather than to an unrelated one.

## What the owner reads and what it computes

Every amount, remaining and capacity below is read from a retained row. The
caller names customers, invoices, origins and witnesses; it states no
remaining balance and no carrying.

- **Legs.** Each named invoice's remaining comes from the retained live
  invoice projection, and its customer and currency from the retained invoice
  row. A leg naming an unknown invoice, another customer's invoice, another
  currency or more than remains refuses here rather than entering the compiler
  on asserted numbers.
- **Surplus.** The unallocated remainder becomes a liability only with a
  qualified classification. An unreviewed taxable advance refuses toward its
  owner; it never defaults to unapplied cash.
- **Origins.** The origin retains its customer, currency, original amount, both
  account identities and the posting receipt. Its remaining is original less
  every effective application and refund the retained effects record.
- **Effects.** Each application and refund re-reads the origin and its
  remaining, runs the leaf against those numbers, posts through the shared
  kernel and appends the effect. A changed remaining between preview and commit
  refuses rather than posting a stale split.
- **Execution re-derives.** The execute step recomputes the plan from retained
  rows and requires its digest to match the prepared one. The digest covers the
  input and the plan, never a fresh id, so it is reproducible.
- **Evidence.** Every posting cites the retained content hash read back from
  the evidence row, so admission verifies exact bytes rather than a bare id.
- **Posting date.** Today, proved inside the named unlocked period. A period
  that ended, or that never contained today, refuses rather than backdating a
  receipt.

## E2E results

`bun run test:e2e apps/api/tests/customer-receipts.e2e.test.ts` — **3 passed,
0 failed**, exit 0. Real workerd, PostgreSQL with the full migration chain, and
the restricted runtime role.

Invoices ride on real posted receivables created through the change-set flow,
so every remaining below is retained. Expected splits, origins and remainings
are derived by hand from those postings, never from the receipt compiler.

| Case                               | Observed                                                                                                                                           |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Receipt across a leg and a surplus | 8000 of 10000 cash allocated, 2000 retained as a credit origin; the journal balances with the surplus on the liability; the origin rereads at 2000 |
| Apply then refund                  | 1500 of 2000 applied to a second invoice; a 501 refund of the remaining 500 refuses; a 500 refund succeeds; the origin rereads at 0                |
| Unclassified surplus               | `UnsupportedProfile`, never a default to credit                                                                                                    |

## Leaf probe

`next30-probe.ts` records the failure contract written before any production
edit: **13 passed, 0 failed**. The leaf needed no repair.

## Gates

- `bun run check:integration`: passed, 24 wired / 24 declared deferred.
- `bun run check:changed`: passed.
- `bun run check:changed:full`: passed.
- `bun run format:check`: passed.
- `bun run check:tests` (the E2E type gate): passed.
- No command timed out. No grant, migration or access rule was weakened.

## Changed files

- `apps/api/migrations/0034-next-30-customer-credits.sql` (new)
- `apps/api/src/db/commerce/customer-receipts.ts` (new origin/effect store)
- `apps/api/src/application/commerce/customer-receipts.ts` (new owner)
- `apps/api/src/application/posting-admission.ts` (one union member)
- `packages/contracts/src/customer-credit-notes.ts` (contract and endpoints in
  the existing group)
- `apps/api/src/transport/http/routes/customer-credit-notes.ts` (five handlers
  in the existing group)
- `apps/api/tests/customer-receipts.e2e.test.ts` (new, 3 cases)
- `docs/plans/domain-leaf-integration.json` (this leaf only)

## Not proven

- **Paid-credit compilation is leaf-verified only.** `compilePaidCustomerCredit`
  has no owner operation and no E2E; the paid-after-invoice lifecycle is proven
  for applications and refunds, not for paid-credit origination.
- **No reversal transport.** `refuseConsumedHistoryReversal` is leaf-verified
  only; correcting a misapplied effect has no endpoint.
- **Adopted clearing is unexercised.** The `adopted_clearing` source branch
  exists in the leaf and the contract, but no E2E adopts a proven clearing
  capacity instead of posting new cash.
- **Single customer, single currency, exact rounding.** Multi-invoice splits
  across currencies, partial-leg edge cases and `half_up` rounding are leaf
  rules, not journeys.
- **No concurrency case.** Two operators racing the same origin rely on the
  unique receipt keys and the remaining recheck, exercised only sequentially.
- No provider, filing, tax or statutory claim. Synthetic fixtures only.
