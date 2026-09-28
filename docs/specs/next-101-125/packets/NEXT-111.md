# NEXT-111: Annual common-cost VAT deduction true-up

**Priority when applicable:** P1. **Owner lane:** TAX.

**New scope:** Invoice-level partial deduction already exists. Add a qualified final common-cost allocation over a complete annual population and post only the difference from effective deductions.

**Existing owner to extend:** Existing recognized tax components, qualified releases, VAT return amendments and cost/asset owners.

**Earlier contracts:** NEXT-03, NEXT-04, NEXT-22, NEXT-49. **This-wave dependencies:** None.

**Basis:** R02, X01, P03, P04 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Scope and legal choice

Start with common operating expenses already recognized to expense accounts. Directly attributable full-deduction/zero-deduction costs, private use, special deduction prohibitions and capital-goods adjustment regimes are explicitly separated. Do not multiply every input tax amount by one company turnover ratio.

The official mixed-activity guidance distinguishes reasonable resource-based allocation from the optional qualifying turnover method and discusses provisional versus final allocation [X01]. The actual selected method, denominator/exclusions, rounding and correction period must be qualified as one release. The algorithm below does not choose a legal method from the most favorable result.

```text
RecoveryPoolRevision {
  entity, fiscalAndTaxYear, eligibleOriginalTaxComponents,
  directCostExclusions, allocationMethodRelease,
  independentlyReviewedDriverPopulation, preliminaryDeductionRefs, cutoff
}
DeductionTrueUp {
  poolId, targetBySourceComponent, effectivePriorDeduction,
  signedDeltaByComponent, reportingAttribution, originalCostCounterparts,
  priorTrueUpRefs, digest
}
```

## Calculation

```text
calculateFinalDeduction(pool):
  require complete eligible original source/correction population
  require driver basis known and method applies to each selected cost
  fraction = qualifiedMethod.computeDriverFraction(exactSourceDriverFacts)
  require fraction within supported bounds; zero denominator is a decision case
  for source component:
    availableTax = original supported source tax after effective credits
    target = qualifiedMethod.allocate(availableTax, fraction, sourceFacts)
    effective = originalDeduction + priorDeductionAdjustments - creditedDeduction
    require 0<=target<=availableTax
    delta = target-effective
    retain target, calculation/rounding witness and exact prior effect identities
  require every source component appears once
```

Where the rule rounds the recovery percentage separately, do that before its required monetary calculation. Do not substitute the generic half-up helper for statutory percentage rounding. If the rule works at a pool total, apportion that exact result back to components using a disclosed conserving policy rather than obtaining a different total by independent line rounding.

## Financial and return effects

For an eligible fully expensed cost and a positive additional deduction `D`:

```text
debit deductible input VAT D
credit original non-deductible cost D
```

Negative `D` reverses those sides. Create a signed deduction-adjustment tax fact referencing the original component and qualified reporting attribution. Supplier payable, cash and original purchase gross do not change. Do not delete the original deduction or replace it with the target and also post the delta.

Initial execution refuses a source whose non-deductible portion has been capitalized, deferred or consumed by an unsupported later cost allocation that requires financial basis changes. Those cases need their actual asset/schedule writer to adjust remaining cost and past recognition consistently, not a credit to any convenient current expense account.

`executeTrueUp` checks the exact pool membership, current deductions, source credits and approved release. The journal, adjustment facts, source-capacity claims and receipt commit together. The existing VAT amendment owner subsequently prepares the required return version; this packet does not recreate its settlement delta or submit a declaration.

## Versioning and controls

An additional late invoice/credit changes the relevant pool epoch. A revised target posts only the new difference against all effective prior true-up effects. Old filed declarations retain their bytes. Tax-point attribution and accounting adjustment dates are explicit and can differ under the qualified correction profile.

UI shows provisional allocation, final qualified driver, source-tax ceiling, prior deduction and proposed delta per item, with all excluded costs explained. A complete review cannot omit a mandatory source because it was difficult to classify.

```text
common input tax10000, existing eligible deduction4000, qualified final target6500
  => input VAT debit2500, cost credit2500
repeat same target after posted true-up -> delta0, no duplicate deduction
credit reduces eligible tax to8000; revised target5200; effective old6500
  => deduction adjustment-1300, subject to exact original credit history
capitalized source but no asset adjustment integration -> explicit refusal
```

Completion requires original-cost/tax lineage, amended-report preparation and current controls, not just a percentage displayed on a settings page.
