# NEXT-41: Late FX valuation and consumed-chain correction

**Priority:** P1. **Owner lane:** TREASURY. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** The existing commerce monetary-item and FX correction owner. Add a bounded chain-adjustment operation using its own balances and recorded events.

**New scope, not repeated work:** NEXT-18 refuses late revaluation after settlement consumed the old basis. Solve that explicit limitation with a complete approved delta, not reversal of real cash or another writable FX register.

**Dependencies:** NEXT-18. **Integrate after:** WIP-FX02-P1, APP-SLICE-READY(commerce-fx).

**Conditional gates:** NEXT-40: the affected chain includes native foreign-cash holdings; NEXT-23: affected financial periods require approved reopening.

**Evidence:** R10, R11, P18 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Scope and immutable repair plan

Initially support one monetary item with known recognition, deterministic partial/full settlements and reporting-rate valuations. Mixed credits, netting, foreign-cash links or cross-item allocation chains require their explicit supported replay handlers. If one affected event lacks a handler, return its identity as a blocker before any journal is prepared.

```text
FxChainBasis {
  itemId, anchorBeforeChangedCutoff, originalEconomicEvents,
  priorEffectiveCarryingAdjustments, activeChainRevision,
  relatedCash/feeIdentities, valuationRateVersions,
  selectedAccountingDates, recordedCutoff, closureDigest
}
FxChainRepair {
  inputChange, orderedClosure,
  revisedPerEventCarrying, deltaByAccountingDateAndRole,
  originalCurrencyDelta: 0, cashSourceDelta: 0,
  resultingBalances, downstreamImpactRefs, approvalDigest
}
```

A late rate decision does not change how many foreign units were paid, the actual cash consideration or the original fee evidence. Event ordering is the qualified economic chronology with explicit tie-breaking, not arrival-time sort. Ambiguous chronology blocks repair.

## Replay the financial meaning over frozen facts

```text
calculateChainRepair(basis, correctedRate):
  events = all dependent events through the current endpoint, not just the next payment
  require complete closure and bounded size
  state = independently reconstructed anchor {foreignRemaining, bookCarrying}
  desired = []
  for event in chronological order with inserted/replaced valuation decision:
    if valuation:
      T = exact native remaining * selected reporting rate under policy
      append target carrying adjustment T-state.B and its direction-specific P&L
      state.B = T
    if settlement:
      b = existing FxDomain exact paired release(state, event.originalUnits)
      gain = event.K-b for AR; b-event.K for AP
      append desired control release and realized P&L, preserving K and fees
      state.Q -= event.originalUnits; state.B -= b
    if other event:
      call its explicitly supported pure replay rule or refuse
  oldEffective = original owned vectors + all previous repair deltas
  delta = desired - oldEffective, grouped by economic accounting date and role
  require delta contains NO change to real cash quantities or fee/source principal
  require final original-unit balance unchanged
  require reconstructed final carrying equals planned current owner balance
  return full witness and delta, not replacement of old source records
```

The posted correction can include several dated vouchers in one approved book-scoped aggregate. Each date must be eligible under the selected correction policy. Closed periods require approved reopening or a separately qualified prior-period adjustment policy. Do not move an old-year tax/result effect into today's date for convenience.

## Atomic application of a new effective chain

```text
executeFxChainRepair(plan): FinancialTx
  lock book, all affected periods and complete owned resource closure
  replay first, then verify active chain revision and closure membership
  require no intervening settlement, rate change or other consumer
  verify journal delta equals the approved old-to-desired role vector
  post all required correcting vouchers as one complete group
  append carrying deltas referencing ORIGINAL settlement/valuation effects
  advance the original item's effective-chain revision
  record downstream report/close/tax review obligations
  save one aggregate receipt and change intent
```

The current commerce projection folds original effects plus the approved deltas exactly once. It must not replace the entire register and then also apply the original effects again. Old snapshots keep their recorded cutoff and chain revision. A zero total difference across two years does not justify omitting both nonzero period corrections.

## Concrete late-year-end example

```text
AR initially110000
No old year-end valuation; January cash settlement116000
Old January realized gain6000, AR now0

Correct December target115000:
  December delta: AR +5000; valuation gain -5000
  January delta:  AR -5000; realized gain +5000

Cash delta0; foreign quantity delta0; ending AR delta0
Revised total gain remains6000 = December5000 + January1000
```

Do not reverse/repost the January cash receipt or restore original payment capacity. Those events occurred correctly; only their carrying-release and gain attribution changes.

## Read/UI/recovery requirements

Show the old and target per-event carrying path, each dated journal delta, unchanged cash/principal and every affected report/close. Approval must cover the entire closure. Report readers identify whether they show original historical knowledge or the newly corrected recorded basis.

```text
another settlement occurs after review -> whole repair stale, no partial delta
same repair key after commit -> same aggregate receipt
new key with already applied input change -> AlreadyApplied/no-effect determination
missing credit handler in chain -> explicit blocker, never skip event
December closed without authorized correction policy -> refuse before posting
```

This is a bounded domain replay calculation, not a generic event-sourcing platform. No other domain acquires authority over the FX item's balances.
