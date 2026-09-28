# NEXT-81: Asset work-in-progress and commissioning from purchase costs

**Priority when applicable:** P1. **Lane:** ASSETS.

**New work:** Add multi-source asset construction/acquisition accumulation and an explicit ready-for-use transition. Existing asset bases and depreciation schedules remain their owners.

**Use existing owners:** Purchase recognition, asset register, original-cost allocation and schedule application services.

**Required earlier contracts:** NEXT-03, NEXT-31.

**Conditional gates:** NEXT-54: qualified import/landed-cost components enter the asset basis.

**Evidence basis:** R03, P54. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Source-cost coverage

```text
AssetBuild {buildId, intendedAsset, eligibleCostProfile, stage: accumulating|commissioned|abandoned}
CostAllocation {recognitionId, sourceLineId, costComponentId, allocatedMinor,
  constructionAccount, targetBuild, availableCoverageVersion}
CommissioningPlan {buildId, acceptedInServiceDate, componentAllocation,
  grossTarget, usefulLife/residual evidence, uncommissionedCosts, digest}
```

Cost is the eligible net plus non-deductible tax and independently qualified direct costs, not the invoice gross by default. Evidence that a cost belongs to the asset is mandatory. Marketing, training or finance costs do not become capitalizable merely because the build is over budget.

## Accumulation

An unposted purchase uses the existing compiler with the qualified asset-under-construction role. That one transaction writes purchase/tax/payable and source-cost allocation. An already recognized eligible expense can be reclassified through an approved dated operation: debit construction asset, credit that expense. No new payable, bank transaction or tax recognition is created.

```text
allocateBuildCost(source, build, amount):
  require exact recognized cost component and amount<=unallocated eligible cost
  capture original purchase/credit history and cost profile
  freeze source-to-build allocation; reserve no duplicate expense recognition
  transaction: recheck capacity, post required reclassification, append allocation + receipt
```

A credit reduces the linked uncommissioned basis or triggers an owned adjustment to the commissioned asset. It must not quietly delete a source allocation or leave depreciation on refunded cost.

## Commissioning

```text
prepareCommissioning(build):
  G = sum effective eligible allocations selected for this commissioned component set
  require actual ready-for-use evidence and complete ownership/use-date facts
  require G>0 and exact component shares sum to G
  determine qualified method, residual and future recognition start
  debit in-use asset role G; credit construction role G
  create existing asset basis with original sources and the approved future schedule
```

`executeCommissioning` locks the build, cost rights and schedule dependencies. Journal reclassification, commissioned asset basis, transferred source allocations and schedule creation share one tx. It cannot first move the GL then hope a later job creates the schedule. Partial commissioning uses explicitly partitioned components; remaining costs stay on the build without being depreciated.

## Abandonment and corrections

Abandonment needs reviewed recoverable value and treatment. The supported decision can reclassify unrecoverable construction cost to loss, but it does not fabricate disposal proceeds. Existing advances for undelivered assets remain NEXT-57 prepayments rather than installed costs.

Correcting commissioning after depreciation requires the asset owner's complete correction/estimate path. Changing the date or useful life in place is prohibited. Old source and report snapshots retain their original basis.

## Completion cases

```text
eligible cost100000 + installation20000 -> construction120000
commission120000 -> in-use+120000/construction-120000; AP/VAT delta0
commission component70000 -> build still50000, only70000 schedule authority
same source line allocated twice -> capacity refusal
supplier credit after commissioning -> owned asset adjustment, not source deletion
```

UI shows cost provenance, unallocated/accumulating/commissioned amounts, actual in-service evidence and schedule. Complete controls reconcile construction and in-use accounts separately. This is not an inventory, project-cost capitalization or arbitrary asset-recognition framework.
