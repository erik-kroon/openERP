# NEXT-18: Incremental open-item FX remeasurement

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/commerce/fx-valuations.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/commerce/fx-valuations.ts` or the existing equivalent owner |
| Pure calculation | Complete-population target carrying and incremental FX differences |
| Atomic scope | All selected carrying changes, journal and valuation receipt commit as one group. |
| Prerequisites | NEXT-17 |
| Reserved handoff | WIP-FX02-P1 |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-17 and released WIP-FX02-P1. ADR 0008 selects incremental valuation without an automatic next-period reversal.

## Valuation basis and identity

```text
ValuationBasis immutable {
  book, currency, accountingCutoff, recordedCutoff,
  completeEligibleItemMembership, populationEpoch,
  items: [{itemId, originalRemaining, bookCarrying,
           capacityVersion, recognitionAndSettlementLineage}],
  rateRevisions, valuationPolicy, priorValuationRefs
}
ValuationEffect immutable {
  itemId, cutoff, economicDecisionId, priorCarrying, targetCarrying,
  delta, rateWitness, journalRefs, predecessorEffect?, receiptId
}
UNIQUE(book, itemId, cutoff, economicDecisionId)
```

The eligible set is explicit by book, currency and valuation purpose. A bounded query must prove it selected all items in that scope or fail with a narrower permitted scope. Do not value the first page and call it a complete remeasurement.

## Calculation

```text
prepareValuation(selection):
    capture current unhedged supported monetary items as of accounting+recorded cutoff
    require no item with unsupported later consumption across the selected cutoff
    # Backdating across already posted settlements needs a separate full correction chain.
    for item:
        T = convertMinor(item.remainingOriginal, originalScale, bookScale,
                         selectedReportingRate, qualifiedRounding).minor
        B = item.currentBookCarrying
        delta = T-B
        controlSigned = delta if item is receivable else -delta
        Journal.addSigned(item.controlRole, controlSigned)
        if controlSigned>0: Journal.addSigned(unrealizedGainRole, -controlSigned)
        if controlSigned<0: Journal.addSigned(unrealizedLossRole, -controlSigned)
        effects += {item, B,T,delta, witness}
    return seal plan with complete membership, journal and effects
```

Receivable appreciation debits the asset and credits a gain. Payable appreciation credits the liability and debits a loss. A no-delta item is retained in the valuation membership and decision result without a zero journal line.

```text
executeValuation(command):
    return withAdmittedPrincipal(access, scope, valuationPermission, (tx, principal) =>
        lock book; replay exact command first
        load exact valuation plan and complete eligible scope membership
        load all selected item capacities, rate revisions and cutoff restrictions in batches
        require population and every item version still match
        require no intervening settlement, credit or unsupported backdated consumption
        ValuationDomain.assertAllTargetsAndSignedDeltas(plan, current)
        approval = validate exact valuation approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal) if nonempty else []
        effects = FxApp.applyValuationEffectsWithinTransaction(tx, plan.effects, journal)
        valuation = FxDb.insertResultAndCutoff(tx, plan, effects, includingNoEffectItems)
        bump owned item/control/closing dependency versions through tx
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: ids(journal), valuation, effects}, approval)
    )
```

A new approved reporting-rate revision at the same cutoff is an explicitly superseding economic decision. Compute only its new target less CURRENT carrying. Do not reapply its original delta or overwrite the previous effect. Reject correction after later consumption unless the owned chain-repair workflow is available.

## Later settlement and controls

```text
settlementBasis(item):
    initialCarrying + effectiveValuationDeltas - effectiveCarryingReleases

controlExpected(currency, cutoff):
    sum each eligible item's signed carrying under its direction
    compare to its exact owned GL control contributions
    expose unassigned/unexplained control lines, not merely net difference
```

Foreign quantity does not change when valued. Rate withdrawal affects new use/readiness and can create a review case; it does not erase historical carrying values. Keep valuation P&L and settlement P&L attribution separate. A later classification-only realized/unrealized reclassification, if required, is not another economic gain.

## Vectors

```text
AR initial110000 -> target115000: AR+5000 / valuationGain-5000
later settlement116000 releases115000: cash+116000 / AR-115000 / realizedGain-1000
total gain6000, not11000
AP110000 ->115000: APLiability-5000 / valuationLoss+5000
zero delta: receipt with complete membership, no voucher number consumed
new item dated before cutoff while approval pending: stale population, no partial valuation
```

The first profile explicitly refuses a late year-end revaluation when later settlements already consumed its old basis. It must not pretend that refusal is a successful close; supporting such a company's history needs an owned chain-recalculation extension.
