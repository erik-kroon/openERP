# NEXT-107: Onerous service-contract provisions and release on performance

**Priority when applicable:** P2. **Owner lane:** SCHEDULES.

**New scope:** Add reviewed loss obligations on remaining service contracts. Project margin is a report and unbilled revenue is an asset; neither records a qualified future unavoidable loss.

**Existing owner to extend:** Existing contract, provision/adjustment posting, purchase/payroll expense and financial-close owners.

**Earlier contracts:** NEXT-13, NEXT-76, NEXT-79. **This-wave dependencies:** NEXT-105.

**Conditional:** NEXT-42: a related asset impairment assessment must precede contract-loss recognition.

**Basis:** R03, P76, P79 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## A specific obligation, not a forecast loss journal

```text
ContractLossAssessment {
  contractRevision, remainingCoverage, measurementDate,
  unavoidableFulfilmentCosts, enforceableExitCost?, futureEconomicBenefits,
  costEvidence, relatedAssetAssessments, recognitionPolicyRelease,
  supportedUnavoidableCostTarget, eligibleProvisionTarget, digest
}
ContractProvisionEffect {
  assessmentId, recognition | remeasurement | covered_loss_release,
  signedLiabilityChange, coveredObligationComponent,
  actualPerformanceRefs?, journalRefs, receipt
}
```

A negative sales forecast or discretionary future budget is not enough. Establish the actual contractual obligation, permissible exit rights, remaining performance scope and the applicable framework's measurement rule. The first profile handles short-duration supported service obligations without material discounting. Disputes, legal uncertainty or unsupported long-term measurement remain explicit gates.

## Measurement

```text
compileContractProvision(basis, qualifiedDecision):
  remainingBenefits = evidenced benefits attributable to remaining contract coverage
  fulfilCost = exact supported unavoidable cost estimate for that same coverage
  if the activated rule permits an enforceable exit alternative:
    unavoidable = min(fulfilCost, independently evidenced exitCost)
  else:
    unavoidable = fulfilCost
  require related asset loss already treated where the rule requires it
  target = qualifiedRule.recognizableLoss(unavoidable, remainingBenefits, facts)
  require target>=0 and complete nonduplicated cost/benefit membership
  current = prior recognized provision - explicit consumed/released effects
  delta = target-current
  addSigned lossExpense +delta
  addSigned contractProvisionLiability -delta
```

The familiar `max(unavoidable-benefits,0)` is used only by a released profile that permits it. A forecast engine may calculate that number for review, but cannot activate recognition. Already recognized liabilities, asset impairments and costs cannot also appear as an unrecorded remaining loss without a documented bridge.

## Release against actual covered loss

```text
prepareCoveredRelease(actualPerformance, activeProvision):
  link completed coverage and actual cost/revenue effects to the original assessed component
  calculate qualified consumed-loss share using its retained coverage/rule
  require share<=remaining supported provision component
  debit provision liability share
  credit provision-loss/released-cost role share under the selected presentation policy
  preserve original actual expense and revenue journals
```

Do not release the full gross supplier invoice against a reserve for only the contract's net loss. Costs are still recognized by purchase/payroll owners. The provision release prevents expensing the same loss a second time, with transparent source relationships. If the next estimate changes, calculate its new target after this release rather than applying both old and new complete provisions.

Execution binds contract, assessment, coverage and prior provision versions. Journals, used-coverage effects, updated provision projection and receipt share one tx. A real termination payment is a separately evidenced settlement under its exact obligation; no cash is invented by recognizing the estimate.

## Controls and examples

Reports show initial obligation, revised estimates, covered performance, releases and remaining provision by contract. A subsequent estimate change creates a new dated assessment. No old close or estimate is edited. Tax deductibility is separately mapped by NEXT-22, not inferred from the book expense.

```text
qualified remaining costs260000, benefits200000 -> target provision60000
half completed: actual cost130000/revenue100000, eligible loss share30000
  => provision debit30000, released loss credit30000; remaining30000
new qualified remainder costs125000, benefits100000 -> target25000,
  delta-5000 against remaining30000, not another25000 credit
forecast loss but no qualifying obligation -> review only, journal0
```

This is a conditional accounting expansion, not a source-defect claim or a universal K2/K3 rule. Independent qualified recognition evidence is required before the proposed financial path can be used.
