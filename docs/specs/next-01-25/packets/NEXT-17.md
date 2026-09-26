# NEXT-17: Payable FX and explicit fees

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/commerce/fx-settlements.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/commerce/fx-settlements.ts` or the existing equivalent owner |
| Pure calculation | Payable/receivable signed consideration and fee compiler |
| Atomic scope | Journal and released WIP paired-capacity consumption share one tx. |
| Prerequisites | NEXT-02 |
| Reserved handoff | WIP-FX02-P1 |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Wait for WIP-FX02-P1. Use its paired-release result and existing commerce monetary item. NEXT-03 supplies qualified purchase recognition where applicable. Do not copy the WIP partial-release algorithm into this packet.

## Inputs

```text
FxSettlementInput {
  monetaryItemId, direction: receivable|payable,
  requestedOriginalUnits,
  considerationEvidence: {grossBookMinor K, actualCashSources},
  fees: [{sourceIdentity, bookMinor, expenseRole, treatmentWitness}],
  settlementDate, expectedCapacityVersion,
  releasedPrincipalPlanFromWip
}
```

Fees must be in book currency in this profile. Fee tax, foreign cash, hedges and multilateral netting require separate supported treatment or refusal. `K` is evidenced gross settlement consideration, not the current exchange-rate quote multiplied by principal.

## Supplier monetary-item recognition

```text
prepareForeignPayable(purchase):
    require qualified original-currency obligation and book-value recognition witness
    if current commerce owner already supports that payable variant: use it
    else add discriminated foreign payable variant through same owner
    retain original units and carrying value from purchase recognition
    preserve existing synthetic_invoice_v1 meanings and amounts
    return a purchase-owned aggregate for one application tx containing journal, paired payable basis and tax facts
    # This compiler does not call a public purchase execution or open a transaction.
```

The operation cannot make a supplier payable by relabeling an already retained book-currency number as foreign units.

## Compiler

```text
compileSettlement(basis, input):
    release = FxDomain.planPairedRelease(basis, input.requestedOriginalUnits)
    b = release.bookCarryingReleased
    K = input.grossBookConsideration
    F = sum(input.fees.bookMinor)
    require K>=0 AND F>=0 and fee source identities unique
    if receivable:
        signedCash = K-F
        require signedCash >=0 for initial supported net-receipt profile
        gain = K-b
        Journal.addSigned(cashOrQualifiedClearingRole, +signedCash)
        Journal.addSigned(receivableControl, -b)
    else:
        signedCash = -(K+F)
        gain = b-K
        Journal.addSigned(cashOrQualifiedClearingRole, signedCash)
        Journal.addSigned(payableControl, +b)
    for fee:
        Journal.addSigned(fee.expenseRole, +fee.amount)
    if gain>0: Journal.addSigned(realizedFxGainRole, -gain)
    if gain<0: Journal.addSigned(realizedFxLossRole, -gain)
    require sum(actualCashSources.signedBookAmounts) == signedCash
    require no fee or cash source is consumed by another financial operation
    return {journal: finish(), pairedRelease: release, K,F,gain, sourceBindings}
```

`cashOrQualifiedClearingRole` is explicit. For an unposted bank observation, it is cash and the operation creates that cash movement once. For an already posted bank receipt/payment, only a supported settlement-clearing posting with proven unused capacity can be adopted. Use its clearing side and create no second cash entry. An arbitrary existing AP/AR journal is not a clearing witness.

When fees are a separate bank debit rather than withheld from the principal receipt, retain separate cash lines/source links whose signed total agrees with the equation. Do not manufacture one net observation or match one source twice.

```text
executeFxSettlement(command):
    return withAdmittedPrincipal(access, scope, fxSettlementPermission, (tx, principal) =>
        lock book; replay exact command first
        load exact plan and current commerce monetary-item/source/fee capacities in batches
        require WIP paired release still binds this exact item, version and ordered legs
        FxSettlementDomain.assertApprovedDirectionAndConservation(plan, current)
        approval = validate exact FX approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal)
        paired = FxApp.applyPairedConsumptionWithinTransaction(tx, plan.pairedRelease, journal)
        links = FxDb.insertSettlementFeeAndSourceEffects(tx, plan, paired, journal)
        FxDb.bumpAffectedControlVersions(tx, plan)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journal.ids, paired, links}, approval)
    )
```

Latest-unconsumed settlement correction delegates to the existing FX correction owner and restores journal, both capacities and fee/source rights together. A no-journal unallocation cannot reverse realized FX. Consumed later settlement/valuation history refuses unsupported standalone correction.

## Vectors with b supplied by WIP

```text
payable b110000 K112000 F1000:
    AP+110000, FXloss+2000, fee+1000, cash-113000
receivable b110000 K112000 F1000:
    cash+111000, fee+1000, AR-110000, FXgain-2000
payable b110000 K108000 F1000:
    AP+110000, fee+1000, cash-109000, FXgain-2000
b0 is allowed only when WIP supports that exact principal release:
    no zero AP/AR line, but principal consumption and remaining effects stay explicit
```

Evidence baseline: S03/S07 and released WIP contract. No new foreign-principal capacity owner.
