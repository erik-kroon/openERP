# NEXT-42: Economic impairment reversal and zero-carrying assets

**Priority:** P1. **Owner lane:** SCHEDULES. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing asset, impairment and schedule owners after their reserved UI/control closure.

**New scope, not repeated work:** The adopted first profile requires positive remaining carrying and only a bounded immediate error correction. Add later economic reversal with a qualified cap and an explicit zero-carrying-but-owned state.

**Dependencies:** No new first-wave financial feature is a hard prerequisite. **Integrate after:** WIP-AST03-UI, APP-SLICE-READY(subledger).

**Conditional gates:** NEXT-19: checking disposal/proceeds consumers; NEXT-13: presenting the resulting financial controls.

**Evidence:** R10, R11 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Do not confuse three events

`ErrorCorrection` repairs a mistaken recorded impairment. `EconomicReversal` reflects a newly evidenced recovery under an applicable accounting rule. `Disposal` ends ownership or the selected asset recognition. They have different dates and downstream consequences.

```text
AssetValuationDecision {
  assetId, kind: further_impairment | economic_reversal,
  assessmentDate, supportedValuationEvidence, targetCarrying,
  counterfactualPolicyRelease, counterfactualBasis,
  expectedAssetVersion, expectedScheduleRevision
}
ScheduleState = active | exhausted | zero_carrying_in_use | disposed
```

No-counterfactual evidence means reversal cannot be approved. Do not compute the cap from the currently impaired depreciation schedule itself.

## Qualified counterfactual cap

```text
calculateCounterfactual(basis, rule):
  require complete original cost and eligible ordinary-depreciation history
  replay the qualified WITHOUT-IMPAIRMENT basis through assessment date
  include only estimate revisions that the policy permits in that counterfactual
  exclude impairment-caused schedule changes unless independently justified
  return carryingWithoutImpairment H and its full witness

compileEconomicReversal(basis, decision):
  B = gross - effectiveOrdinaryAccumulation - effectiveImpairment
  H = calculateCounterfactual(...)
  I = impairment contra amount eligible for reversal
  require decision.targetCarrying >= B
  maximumTarget = min(H, B+I)
  require decision.targetCarrying <= maximumTarget
  R = decision.targetCarrying-B
  debit accumulated impairment R
  credit qualified impairment-reversal income R
  future = approved new useful-life/residual allocation for target carrying
  require futureInstallments + residual == targetCarrying
  return journal + impairment delta -R + complete schedule revision
```

The target comes from reviewed economic evidence and a qualified framework profile. The formula is a design contract for an eligible depreciable asset, not a claim that every asset category or intangible permits reversal. No tax reversal is inferred from a book impairment reversal.

## Full impairment without fabricated installments

```text
compileZeroCarryingDecision(basis, supportedDecision):
  require still-owned asset and qualified complete write-down
  B = current carrying
  debit impairment loss B
  credit accumulated impairment B
  new carrying = 0; future installments = []; residual = 0
  new state = zero_carrying_in_use
```

Empty future installments are valid only under this explicit terminal-recognition state. It is not a generic relaxation of the existing active schedule's positive-installment requirement. The asset remains in inventory and control reporting. Fully depreciated/exhausted and fully impaired positions retain their different histories.

If a later economic reversal from zero is allowed, construct a new positive future schedule from approved dates and residual. Do not reuse retired occurrence keys or rerun old installments. A disposed asset cannot be revived by this operation; reacquisition is another evidenced event.

## Atomic application and correction

`executeAssetValuationChange` rechecks assessment, ordinary/impairment effects, current schedule and absence of incompatible disposal/consumption. It commits the journal, valuation event, schedule revision and retired future-authority markers together. Counterfactual computation happens before the transaction; currentness is checked inside it. Consumers for controls, depreciation, closing and disposal all use the same effective basis.

Immediate correction of this new event is allowed only while its consequences remain unconsumed and can be restored with a complete replacement schedule. Otherwise identify the affected chain and refuse unsupported standalone reversal. Never delete a schedule revision to make old plans usable.

## Controls and vectors

For gross `G`, ordinary accumulation `A`, impairment `I`, carrying is `G-A-I`. The impairment contra rollforward includes positive impairment and negative economic reversals independently from ordinary depreciation. Controls reconcile each role, not just net carrying.

```text
G1000000 A200000 I300000 -> B500000
qualified H700000, target650000 -> reversal150000, I150000, B650000
target750000 -> above cap700000, refuse
B500000 -> full impairment500000 -> B0, no future installment, still in inventory
zero-carrying asset later disposed without proceeds -> release gross and contra,
    not another500000 loss
```

The packet includes application/schema version changes for the new schedule states and every affected consumer. It cannot be accepted as a UI-only toggle or manual journal feature. Legal eligibility and counterfactual data require separate qualification.
