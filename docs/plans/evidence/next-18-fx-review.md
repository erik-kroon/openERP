# NEXT-18 incremental open-item FX remeasurement — delivery evidence

Baseline: `c6d5c2b`. Scope is this evidence file and the nine files listed under
_Changed files_. This delivers a previously deferred leaf: the `fx-remeasurement`
entry in `docs/plans/domain-leaf-integration.json` moves from `deferred` to
`wired` because a real application owner now composes it.

## What was wired

The leaf already had correct pure rules (`prepareValuation`,
`assertValuationMembership`, `carryingAfter`) and **no consumer**. It now has:

- a named application owner, `apps/api/src/application/commerce/fx-remeasurement.ts`,
  with four operations: prepare, approve, execute and get;
- tx-passing persistence in `apps/api/src/db/commerce/fx-remeasurement.ts`,
  plus one bounded enumeration added to the existing FX db module;
- one table pair in `apps/api/migrations/0034-next-18-fx-remeasurement.sql`;
- the wire contract inside the existing `CommerceFxApi` group and the handlers
  inside the existing `CommerceFxHandlers` group;
- a focused E2E over real workerd, PostgreSQL and the restricted runtime role.

This extends the **existing** commerce FX owner rather than creating one, so no
`api.ts`, `index.ts`, `contracts/package.json` or capability registration was
touched. Four helper functions in the FX owner gained the `export` keyword so
the remeasurement reuses the exact item-state computation and the exact posting
path; no logic in the existing owner changed.

## What the owner reads and what it computes

Every amount, carrying, rate numerator and denominator below is read from a
retained row. The caller names item ids, a rate revision, a cutoff and the
posting witnesses; it states no amount and no carrying.

- **Items.** Each named item's retained remaining and carrying come from the
  same `readItemState` the settlement flow uses. The direction maps
  customer→receivable and supplier→payable; the control account is the retained
  `control` binding; the capacity version is the retained item digest, which
  changes exactly when the item's state changes.
- **Completeness.** The named set must equal the retained eligible set
  (everything with anything left to remeasure), proved by a bounded
  enumeration. A population past the bound, or a named set that is not the
  eligible set, refuses rather than valuing a partial population.
- **Rate.** The caller names a rate observation and digest; the owner reads the
  current retained revision, refuses a withdrawn one, and verifies the digest,
  the currency pair and that the rate is effective on or before the cutoff.
- **Consumption.** Settlements touching vouchers dated after the cutoff need a
  full correction chain, so the owner reads settlement voucher dates rather
  than trusting the request.
- **Scale and accounts.** The named book scale must equal the book's retained
  scale, the gain and loss accounts must exist, and the cutoff must fall in the
  named unlocked period.
- **Execution.** The population is recomputed and checked against the sealed
  membership, the journal posts through the shared posting path with the
  reporting-rate evidence cited, and a zero-delta plan retains its membership
  without consuming a voucher.

The posting witnesses (fiscal year, period, series) and the economic decision
are reviewed configuration, sealed with the plan. They are recorded here
explicitly rather than dressed up as derived values.

## E2E results

`bun run test:e2e apps/api/tests/fx-remeasurement.e2e.test.ts` — **3 passed,
0 failed**, exit 0. Real workerd, PostgreSQL with the full migration chain, and
the restricted runtime role.

The FX item is created through the real recognition owner (counterparty,
rate, evidence, approval, execution), so its parents are genuine retained rows.
The reporting rate comes from the real exchange-rate owner. Expected valuation
figures are derived by hand: 10000 foreign minor at 10.85 is 108500 book minor,
less 100000 carried is a +8500 gain.

| Case                           | Observed                                                                                                                                                                                                                                                                                      |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Remeasure an open item         | Target 108500, delta +8500, balanced journal with the 8500 gain leg on the unrealized gain account; approval by a second operator; execution posts a retained voucher whose gain leg is 8500 on the gain account and 8500 debit on the control account; the sealed review rereads identically |
| Incomplete eligible population | Two items eligible, one named: `InvalidJournal`                                                                                                                                                                                                                                               |
| Withdrawn reporting rate       | `StaleDependency`                                                                                                                                                                                                                                                                             |

## Leaf probe

`next18-probe.ts` records the failure contract written before any production
edit: **16 passed, 0 failed**. The leaf needed no repair.

## Gates

- `bun run check:integration`: passed, 23 wired / 25 declared deferred.
- `bun run check:changed`: passed.
- `bun run check:changed:full`: passed.
- `bun run format:check`: passed.
- `bun run check:tests` (the E2E type gate): passed.
- No command timed out. No grant, migration or access rule was weakened. The
  four `export` keywords added to the existing FX owner change no behavior.

## Changed files

- `apps/api/migrations/0034-next-18-fx-remeasurement.sql` (new)
- `apps/api/src/db/commerce/fx-remeasurement.ts` (new review/approval store)
- `apps/api/src/db/commerce/fx.ts` (one bounded enumeration)
- `apps/api/src/application/commerce/fx.ts` (four `export` keywords only)
- `apps/api/src/application/commerce/fx-remeasurement.ts` (new owner)
- `packages/contracts/src/commerce-fx.ts` (contract and endpoints in the
  existing group)
- `apps/api/src/transport/http/routes/commerce-fx.ts` (four handlers in the
  existing group)
- `apps/api/tests/fx-remeasurement.e2e.test.ts` (new, 3 cases)
- `docs/plans/domain-leaf-integration.json` (this leaf only)

## Not proven

- **Supersession is carried, not enforced.** The leaf computes a superseding
  target less current carrying, and the prior effect id rides as lineage, but
  no owner invalidates or links the prior effect row.
- **No settlement interplay.** A remeasurement between a partial settlement and
  its correction, or across a fee settlement, is refused or untested rather
  than proven; the `consumedAfterCutoff` guard is the fence, not a proof of
  every interleaving.
- **One currency pair, one direction.** USD receivable at exact rounding only;
  `half_up`, payables, multi-item populations and multi-currency selections are
  implemented by the leaf but not exercised end to end.
- **No concurrency case.** Two preparers racing the same population rely on the
  digest-unique review and the membership recheck, exercised only sequentially.
- No provider, filing, tax or statutory claim. Synthetic fixtures only.
