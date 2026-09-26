# NEXT-22: Pre-close tax bridge and INK2/SRU

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/tax/corporate.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/tax/corporate.ts` or the existing equivalent owner |
| Pure calculation | Pretax bridge, current-tax delta and INK2/SRU fields |
| Atomic scope | Tax-effect journal and owned year target share one tx; form artifacts are separate. |
| Prerequisites | NEXT-13 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-13. Draft tax computation precedes final close. It does not wait for an already finalized year that itself needs current tax.

## Typed bridge

```text
PreTaxOverlay immutable {
  fiscalYear, ledgerBasis, proposedNonTaxAdjustments,
  effectiveIncomeTaxEffectsExcludedFromPretaxResult,
  mechanicalTransferEffectsExcludedFromPL,
  pretaxProfit, supportedRuleWitnesses, sourceCoverage
}
TaxAdjustment immutable {
  id, year, kind: nondeductible_expense|nontaxable_income|supported_schedule_adjustment,
  signedTaxableAdjustment, sourceContributionIds, evidence, ruleRelease,
  explanation, economicComponentIdentity
}
TaxBridge immutable {
  overlayDigest, adjustments[], lossBasis,
  taxableBeforeLoss, allowedLossOffset, taxableIncome,
  currentTaxTarget, projectedAfterTaxResult,
  fieldLineage, mappingRelease, status
}
```

A duplicate tax adjustment over the same economic component is refused unless the mapping explicitly establishes distinct nonoverlapping adjustments. The tax return mapping is versioned data/code from the applicable official release, not an inferred account-prefix table.

## Calculation

```text
calculateCorporateTax(overlay, adjustments, reviewedLosses, taxRelease):
    P = overlay.pretaxProfit
    require overlay pretax definition excludes current income-tax expense exactly once
    require every material tax adjustment family is supported or evidenced inapplicable
    require reviewedLosses known, including an evidenced zero when applicable
    A = sum(adjustments.signedTaxableAdjustment)
    beforeLoss = P+A
    if loss restrictions/ownership changes exceed supported profile:
        fail UnsupportedLossTreatment
    allowedOffset = min(max(beforeLoss,0), reviewedEligibleLossAvailable)
    taxableRaw = max(beforeLoss-allowedOffset,0)
    taxable = apply exact taxRelease.taxableBaseRounding(taxableRaw)
    currentTax = roundRational(taxable*taxRelease.rate.n,
                              taxRelease.rate.d, taxRelease.taxRounding)
    require otherSupportedIncomeTaxExpense is evidenced and supported (or evidenced0)
    projectedAfterTax = P-currentTax-otherSupportedIncomeTaxExpense
    closingLossBasis = reviewedOpeningLoss-allowedOffset+max(-beforeLoss,0)
        # Only for the qualified no-special-restrictions profile.
    return all rows and formula dependencies, not just currentTax
```

Draft calculations do not consume loss carry-forwards. The final selected year/certificate owns the adopted loss movement. Competing drafts cannot consume the same opening allowance repeatedly. A negative taxable result does not produce a negative current-tax cash receivable by multiplying it by a rate.

## Current-tax journal and self-reference avoidance

```text
prepareCurrentTaxEffect(bridge, priorYearTaxEffects):
    target = bridge.currentTaxTarget
    alreadyRecognized = sum(effective current-tax effects for this company/year)
    delta = target-alreadyRecognized
    Journal.addSigned(currentIncomeTaxExpense, +delta)
    Journal.addSigned(currentTaxLiability, -delta)
    return sealed year-tax target and exact delta or a no-effect receipt
```

Preliminary tax transferred to skattekonto is not current income-tax expense. Reconcile tax prepayments, assessed charges and the liability separately. Do not subtract bank tax payments from the tax expense target to make the return agree.

The tax journal changes the actual ledger. It must not change the definition of pretax profit used to calculate itself. Revalidation compares the retained pretax contribution set and supported tax adjustments, not simply a global ledger sequence.

## INK2 semantic fields

```text
prepareIncomeTaxFields(bridge, actualOrProjectedStatements, formRelease):
    INK2R receives the qualified financial-statement values, including after-tax result
    INK2S starts from that declared accounting result
    add back the nondeductible tax expense under its explicit tax mapping
    include the other bridge adjustments once
    require resulting taxable basis reconciles to bridge.taxableIncome
    INK2 main fields and any supported additional bases derive from the same bridge
    for every required mapping:
        value = typed source selector + allowed sign/unit/rounding transformation
        retain source formula IDs and reviewed mapping checksum
    missing required fields or unsupported supplementary obligations -> draft blocked
```

This reconciles a pretax calculation with an accounting form whose result may be after tax. It avoids silently using different starting results in the engine and exported declaration.

## SRU serialization

```text
renderSru(fields, exactFormatBundle, submitterFacts):
    require selected forms/year/fiscal interval supported by bundle
    require complete field-code map and real submitter/declarant identity
    INFO.SRU = serialize bundle's INFO header/contact/terminator grammar
    BLANKETTER.SRU = for each selected form in deterministic order:
        emit '#BLANKETT' and its exact release-specific form identifier
        emit identity/date metadata required by bundle
        emit '#UPPGIFT', exact fieldCode, formatCheckedValue for each required/present field
        emit per-form terminator
    emit bundle's file terminator
    reject unsupported encoding, embedded line breaks/control characters and size overflow
    validate lexical grammar, field types, identities and cross-field totals independently
    retain both filenames, byte hashes, lengths, form release and validation results
```

The concrete current field codes, headers and encodings are required reviewed data, not guessed literals. INFO.SRU and BLANKETTER.SRU are distinct deliverables under Skatteverket's file-transfer contract [X13/X14]. Export is not signing or filing. NE and comprehensive special corporate-tax regimes are outside this selected AB profile.

## Vector, synthetic20% tax

```text
P=1000000, addback50000, deduction20000, known losses0
beforeLoss=1030000; currentTax=206000; afterTax=794000
form bridge: 794000 + taxAddback206000 +50000 -20000 =1030000
prepaid tax90000 does not change currentTax206000
existing currentTax effect200000 => new tax adjustment6000, not206000 again
```

## Application tax-effect execution

```text
executeCurrentTaxEffect(command):
    return withAdmittedPrincipal(access, scope, taxPostingPermission, (tx, principal) =>
        lock book; replay exact command first
        load sealed year-tax plan and current pretax/adjustment/loss witnesses
        require year target identity and effective prior tax effects match approved basis
        require no unsupported change to eligible loss facts or pretax population
        CorporateTaxDomain.assertTargetAndDelta(plan, current)
        approval = validate exact tax-effect approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal) if nonempty else []
        effect = CorporateTaxDb.insertYearTargetEffect(tx, plan, journal)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: ids(journal), effect}, approval)
    )

prepareCorporateDeclaration(command):
    capture fixed statement, tax-bridge and exact form-release inputs through application reads
    fields = CorporateTaxDomain.prepareIncomeTaxFields(captured)
    persist immutable semantic fields and lineage through a short application tx
    append render intent; effect-mq Bun job renders and validates SRU outside the tx
    attach exact file manifests and results, never an inferred submission receipt
```

The tax calculator, form mapping and rounding policy live in `jurisdictions/se` or the owning application/domain module. Typed SQL returns exact contribution and previously applied effect sets. Draft bridges do not consume loss rights; final selected closing facts own that adoption. No tax-rate or INK2 state machine is implemented in an integrity trigger.
