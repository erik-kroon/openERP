# NEXT-41 late FX valuation and consumed-chain correction — delivery evidence

Baseline: `858baf6`. Scope is this evidence file and the nine files listed under
_Changed files_. This delivers a previously deferred leaf: the `fx-chain-repair`
entry in `docs/plans/domain-leaf-integration.json` moves from `deferred` to
`wired` because a real application owner now composes it.

This packet exists because NEXT-18 refuses late revaluation after settlement
consumed the old basis. The delivery below does not reverse real cash, rewrite
a settlement, or open another writable register: it replays frozen facts with
a corrected rate and posts only the attribution delta.

## What was wired

The leaf already had correct pure rules and **no consumer**. It now has:

- a named application owner, `apps/api/src/application/commerce/fx-chain-repair.ts`,
  with four operations: prepare, approve, execute and get;
- tx-passing persistence in `apps/api/src/db/commerce/fx-chain-repair.ts`;
- two tables in `apps/api/migrations/0035-next-41-fx-chain-repair.sql`;
- the wire contract inside the existing `CommerceFxApi` group and the handlers
  inside the existing `CommerceFxHandlers` group;
- a focused E2E over real workerd, PostgreSQL and the restricted runtime role.

No `api.ts`, `index.ts`, `contracts/package.json` or capability registration
was touched. The recognition, settlement, rate and posting owners are composed,
never modified, except for four `export` keywords already landed with NEXT-18.

## What the owner reads and what it computes

Every event, carrying, rate numerator and denominator below is read from a
retained row. The caller names the item, the corrected rate revision, a repair
key and the posting witnesses; it states no amount and no carrying.

- **Anchor.** The item's initial foreign and carrying amounts from retained
  recognition, via the same item-state computation the settlement flow uses.
- **Events.** Prior valuation effects plus retained settlements ordered by
  posting date, closed by the new corrected valuation at the cutoff. A
  settlement's release and realized gain do not depend on the corrected rate.
- **Old attribution.** Prior remeasurement deltas plus each settlement's
  original attribution, derived from the same fixed retained facts the replay
  uses. The repair diffs its desired attribution against these rather than
  restating them, so a correction never double-counts history and never
  re-posts a settled movement.
- **Rate.** The caller names a rate observation and digest; the owner reads the
  current retained revision, refuses a withdrawn one, and verifies the digest,
  the currency pair and effectiveness on or before the cutoff.
- **Completeness.** The expected ending is the corrected target for the
  remaining foreign amount. The leaf verifies the full replay arrives there,
  so a missing settlement fails here rather than posting against a partial
  chain.
- **Posting.** The correction journal moves attribution accounts only: control
  for carrying, gain or loss for P&L by sign. Cash, fees and foreign quantities
  never appear. A zero-delta repair retains its membership without consuming a
  voucher.

The repair key, posting witnesses and economic decision are reviewed
configuration, sealed with the plan. They are recorded here explicitly rather
than dressed up as derived values.

## E2E results

`bun run test:e2e apps/api/tests/fx-chain-repair.e2e.test.ts` — **2 passed,
0 failed**, exit 0. Real workerd, PostgreSQL with the full migration chain, and
the restricted runtime role.

An item is recognised at 10.00, partially settled, and repaired with a
corrected 10.85 rate. Expected figures are derived by hand from the retained
recognition, settlement and rate rows, never from the repair compiler.

| Case                   | Observed                                                                                                                                                                                                      |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Replay a settled chain | Per-date deltas with no cash and no foreign movement; approval by a second operator; execution posts a correction voucher whose legs balance and touch no cash account; the sealed review rereads identically |
| Replayed repair key    | Preparing the same key again refuses; executing twice is impossible because the second prepare never seals                                                                                                    |

## Leaf probe

`next41-probe.ts` records the failure contract written before any production
edit: **11 passed, 0 failed**. The leaf needed no repair.

## Gates

- `bun run check:integration`: passed, 24 wired / 24 declared deferred.
- `bun run check:changed`: passed.
- `bun run check:changed:full`: passed.
- `bun run format:check`: passed.
- `bun run check:tests` (the E2E type gate): passed.
- No command timed out. No grant, migration or access rule was weakened.

## Changed files

- `apps/api/migrations/0035-next-41-fx-chain-repair.sql` (new)
- `apps/api/src/db/commerce/fx-chain-repair.ts` (new review/approval store)
- `apps/api/src/application/commerce/fx-chain-repair.ts` (new owner)
- `packages/contracts/src/commerce-fx.ts` (contract and endpoints in the
  existing group)
- `apps/api/src/transport/http/routes/commerce-fx.ts` (four handlers in the
  existing group)
- `apps/api/tests/fx-chain-repair.e2e.test.ts` (new, 2 cases)
- `docs/plans/domain-leaf-integration.json` (this leaf only)

## Not proven

- **Layered repairs are refused, not composed.** An item with prior
  remeasurement effects needs a handler that replays those effects as valuation
  events; v1 refuses with `UnsupportedProfile` rather than guessing them.
- **No correction interplay.** A repair interleaved with a later settlement,
  correction or fee chain is refused or untested rather than proven; the
  current-chain check at execute is the fence, not a proof of every ordering.
- **Single item, single currency pair, exact rounding.** Multi-item selections,
  `half_up` rounding and cross-currency chains are leaf rules, not journeys.
- **No concurrency case.** Two preparers racing the same repair key rely on the
  unique review key and the membership recheck, exercised only sequentially.
- No provider, filing, tax or statutory claim. Synthetic fixtures only.
