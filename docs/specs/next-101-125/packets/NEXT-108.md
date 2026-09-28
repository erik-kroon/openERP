# NEXT-108: Warranty cohorts, expected claims and provision consumption

**Priority when applicable:** P2. **Owner lane:** SCHEDULES.

**New scope:** Add an assurance-warranty obligation and claim-cost lifecycle. A customer refund, billed service warranty or asset impairment is not the same liability.

**Existing owner to extend:** Existing sale occurrence, purchase expense and supported provision posting owners.

**Earlier contracts:** NEXT-03, NEXT-13, NEXT-51. **This-wave dependencies:** None.

**Basis:** R03, P51 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Bounded cohort model

The first profile covers an actual assurance-type obligation attached to supported sales/services and a qualified expected-cost method. Separately sold warranty services follow contract/deferred revenue instead. Product insurance, discretionary goodwill and unsupported contingent liabilities are outside this initial profile.

```text
WarrantyCohort {
  coveredSaleComponentIds, termsRevision, coverageInterval,
  unitsOrCoverageMeasure, qualifyingObligationEvidence
}
WarrantyEstimateRevision {
  cohortId, independentClaimPopulation, frequency/severityBasis,
  currentRemainingCoverage, expectedCost, ruleRelease, assessmentDate
}
WarrantyClaim {
  cohortId, customer/sourceIdentity, supportedEntitlement,
  actualRepairOrCompensationRefs, expectedOutstandingCost,
  reviewedDeductibility, state
}
WarrantyEffect {recognition | actual_cost_consumption | remeasurement | release, journalRefs}
```

Retain the complete source population used for estimate frequency and severity. A warranty budget chosen by management is not automatically a recognizable liability. A zero past-claims sample is not evidence zero future obligation. Where an actuarial or specialist measurement is required, retain that reviewed result and its limits rather than invent probabilities.

## Estimate and posting

```text
calculateWarrantyTarget(coverage, estimateRelease):
  for homogeneous supported cohort segment:
    expected = eligibleRemainingUnits * qualifiedClaimProbability * qualifiedMeanCost
    retain exact rational intermediate and uncertainty evidence
  apply the profile's aggregation, discounting/refusal and rounding boundaries
  exclude costs already satisfied or separately recognized with explicit coverage links
  return supportedTarget with complete inputs

prepareWarrantyAdjustment(target):
  current = initial provision + prior remeasurements - actual releases
  delta = target-current
  debit warranty expense delta
  credit warranty provision delta
```

No rate or expected frequency in this packet is a legal standard. The activated rule defines what uncertainty and obligation evidence suffice. If that profile does not allow the computed expected-value method, it cannot be selected merely because the calculator produces a balanced entry.

## Actual warranty performance

For a repair invoice already recorded by NEXT-03, claim resolution can release the qualified covered cost from the provision through a linked reclassification. Deductible tax remains with the purchase owner; it is not included in warranty expense merely because the invoice gross was paid.

```text
resolveWarrantyCost(claim, actualExpenseComponents):
  C = supported net cost plus non-deductible tax for this actual claim
  P = min(C, remaining eligible provision consumption assigned to claim)
  debit warranty provision P
  credit warranty-cost expense P
  preserve original purchase expense/tax and payable
  actual cost exceeding P remains current expense and informs a fresh estimate
```

When actual repair and provision consumption are approved together, use the same transaction and private purchase/provision writers. If the invoice already exists, adopt its exact cost components and post only the provision release. Never pay the customer or repairer from a mere claim-status transition.

Cash compensation requiring a legal credit/refund uses the correct original-sale tax and liability owner. It cannot be treated as a tax-free repair expense automatically. One actual cost is consumed by at most one claim/provision relationship.

## Claim closure, controls and vectors

A rejected claim does not erase evidence or change the cohort estimate without a reviewed measurement. Expiry of contractual coverage triggers assessment; it is not a blanket release while known unresolved covered claims remain. Outstanding disputes/claims stay in the target population. Closed-period estimate changes follow the supported adjustment-date policy and preserve original snapshots.

```text
synthetic100 covered units * probability1/20 * cost10000 -> target50000
actual qualified repair cost12000 -> release12000, provision38000
remaining expected target40000 -> new expense/provision2000
same repair invoice linked to two claims -> duplicate coverage refusal
separately sold service warranty payment -> route to revenue owner, not provision shortcut
```

UI shows covered sales, known claims, estimate basis, costs paid versus incurred and the liability rollforward. Completion requires actual purchase/claim/provision/control integration, not a spreadsheet value called reserve.
