# NEXT-04: Actual domestic VAT return and controls

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/tax/vat-returns.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/tax/vat-returns.ts` or the existing equivalent owner |
| Pure calculation | Qualified VAT contribution mapping and control reconciliation |
| Atomic scope | Consistent capture then pure calculation then immutable snapshot/receipt persistence. |
| Prerequisites | NEXT-02, NEXT-03 |
| Reserved handoff | WIP-VAT03, WIP-VAT04-A1 |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-02/03. Financial integration waits for WIP-VAT03 and WIP-VAT04-A1. Their execution, delta algorithm and qualification remain external owners.

## Separate dependencies and state

```text
VatCalculationBasis {
  obligationId, registeredPeriod, profileWitness,
  capturedFacts, signedAdjustments, sourceCoverage,
  taxableMembershipEpoch, recognitionVersions, mappingRelease,
  ledgerControlSnapshot, settlementOwnerSnapshot, amendmentOwnerSnapshot,
  cutoff: {ledgerBoundary, recordedAt}
}
VatCalculation {
  exactByBox, reportedByBox, roundingResiduals,
  contributionsByFactAndBox, exclusions,
  calculationSupported, coverageComplete, controlsReconciled,
  filingReady, basisDigest
}
```

A tax fact remains included in its historical recognition period after a correcting fact is appended; the new negative component applies according to the qualified adjustment policy. Withdrawal of an erroneous nonfinancial observation is different from a posted credit. Build the fact selection so a reversal is represented exactly once, never original removal plus double negative adjustment.

## Capture and calculate

```text
captureVatBasis(tx, scope, obligation):
    under shared book barrier:
        require actual registered period and supported profile witness
        capture complete tax-fact membership and corrections, including zero-count epoch
        capture required-source inventory with explicit unavailable/unknown members
        capture all GL movements in each selected VAT control, not just known good ones
        capture VatReclassificationApp/VatAmendmentApp.readEffectiveWithinTransaction(tx, ...)
        for EVERY obligation affecting these accounts
        in the control interval, as signed per-account vectors
        # Not only the obligation whose return is being prepared.
        retain fixed IDs/digests and complete counts

calculateActualVat(basis):
    issues = []
    totals = zero vector for all declared report boxes
    for fact in basis.facts:
        eligibility = check retained treatment/rule/date/source/recognition identities
        if invalid: retain exclusion(fact, reason); issues += reason; continue
        rows = taxMappingRelease.map(fact)
        # Domestic sales basis05; output10/11/12 by qualified rate.
        # Deductible input48. Other cases require their explicit supported mappings.
        for row in rows:
            totals[row.box] += row.signedMinor
            provenance[row.box].append(fact.id, row.signedMinor, mappingRuleId)
    require sum(provenance[box]) == totals[box] for every box
    reported = for each primitive box: round to filing unit using release's box rule
    reported49 = sum(reported output-tax boxes) - reported48
    exact49 = sum(exact output-tax boxes) - exact48
    residual49 = exact49 - 100*reported49  # SEK scale2 for this profile
    retain both; do not assume round(exact49/100) equals reported49
    controls = reconcileTaxControls(basis)
    coverage = every applicable source family has current independent coverage evidence
    supported = no relevant unhandled treatment or excluded mandatory fact
    ready = supported AND coverage AND controls.noUnexplainedRows AND periodVerified
    return calculation with ready flags, never a submitted/assessed/paid state
```

The qualified filing release owns whole-krona rules. Do not automatically require `box05 % 100 == 0`, propagate the old synthetic `vat*4==net` check or remove all guards to accept actual data. Do not silently change the meaning of retained synthetic calculations. Use a distinct qualified actual-company compiler; an unused pre-release implementation need not remain a live fallback.

## Independent control rollforward

```text
reconcileTaxControls(basis):
    for controlAccount in requiredControls:
        expectedClosing = reviewedOpening[account]
        expectedComponents = []
        for recognized fact component POSTED in the GL control interval:
            expectedClosing += its actual signed owned GL amount
            expectedComponents += its exact linked journal component
        for reclassification/amendment effect from released WIP owner:
            expectedClosing += effect.vector[account]
            expectedComponents += effect.journalComponents
        for other explicitly reviewed owned non-tax movements:
            expectedClosing += movement.signedAmount
            expectedComponents += movement.journalComponents
        actualClosing = frozenGL[account].closing
        unexplainedRows = actualMovementIdentities - expectedComponents
        missingRows = expectedComponents - actualMovementIdentities
        result = {difference: actualClosing-expectedClosing, unexplainedRows, missingRows}
        # Two opposite unexplained rows still block; their zero net cannot conceal them.
```

Tax-point attribution and GL posting dates can differ. The declaration selects facts by the qualified tax point. The control rollforward selects components by their actual GL accounting dates. Retain an explicit timing bridge for declaration facts already represented in opening balances and GL movements attributable to another tax period. Never add an opening-balance component again just because it enters this return. Known out-of-period facts are explained exclusions, not automatically missing mandatory current-period facts.

A complete return depends on all relevant boxes being known or evidenced inapplicable. Empty facts do not by themselves establish a zero return. With complete independently reviewed zero-activity coverage, however, zero facts can validly calculate zero without a fabricated dummy fact.

Sealing the new return stores all contributions, exclusions and relevant epochs. A subsequent owned reclassification does not change historical taxable-source membership. Its receipt and control inventory change independently. Later source corrections or unexplained VAT-control postings invalidate current readiness. Retained snapshot bases remain immutable. The new baseline does not require a parallel legacy-global-sequence workflow.

UI shows exact, reported and assessed amounts separately, each box's contributors and unresolved control rows. A read of an old return displays its saved calculation plus separate currentness. Any amendment execution routes only to the released WIP amendment owner.

## Vectors

```text
sales net10000 output2500, purchase deductible1000 => exact payable1500
no facts + complete reviewed no-activity scope => zero calculation possible
no facts + unknown source coverage => zero calculated amount, readiness false
two unowned GL lines +500 and -500 => net difference0, controlsReconciled false
later unrelated non-tax posting => no automatic taxable-basis invalidation
later backdated tax fact => taxable membership changes, new return required
```

Evidence baseline: S08/S03 and approved external rule manifests. Scope remains supported domestic families, not universal Swedish VAT.

## Effect application sealing

```text
prepareActualVatReturn(command):
    captured = withAdmittedPrincipal(access, scope, taxReadPermission, (tx, principal) =>
        lock book for consistent capture; replay the preparation key if committed
        return VatDb.captureAllFactsCoverageAndControlRows(tx, scope, selection)
            + VatReclassificationApp.readEffectiveWithinTransaction(tx, scope, controls, cutoff)
            + VatAmendmentApp.readEffectiveWithinTransaction(tx, scope, controls, cutoff)
    )
    if captured is replay: return saved result
    calculated = VatDomain.calculateActualVat(captured)
    # Complete assessments can be retained with readiness false; do not fake a final return.
    return withAdmittedPrincipal(access, scope, taxPreparePermission, (tx, principal) =>
        lock book; replay exact command first
        verify captured dependency versions and complete memberships
        snapshot = VatDb.insertImmutableCalculation(tx, calculated, captured)
        return CommandDb.save(tx, principal, command, snapshot)
    )
```

Calculation, readiness and exclusion decisions are application-owned. Persistence queries may sum exact stored movements but may not select tax treatment or activate a profile. Every WIP inventory is read through its released tx-passing application port. No reclassification or amendment is executed inside this preparation transaction.
