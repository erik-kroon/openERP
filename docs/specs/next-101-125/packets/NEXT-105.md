# NEXT-105: Project margin with billing, recognition and cash bridges

**Priority when applicable:** P1. **Owner lane:** REPORTING.

**New scope:** Add a coherent project-performance snapshot combining contract rights, earned revenue, allocated cost and actual cash. It does not replace P&L, Cash forecasts or contract recognition.

**Existing owner to extend:** Existing sales coverage, deferred/unbilled revenue, time billing, cost contribution and cash-settlement readers.

**Earlier contracts:** NEXT-13, NEXT-58, NEXT-77, NEXT-79. **This-wave dependencies:** NEXT-104.

**Conditional:** NEXT-78: milestone/retention balances enter the selected project.

**Basis:** R02, P77, P79 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Distinct measures

```text
ProjectSnapshot {
  projectIdentity, financialCutoff, commercialCutoff,
  contractRevisions, issuedInvoices, credits,
  recognizedRevenueComponents, deferredBalances, unbilledBalances,
  directCostRows, sharedCostAllocationSnapshot,
  actualReceipts, actualCostPayments, unallocatedCrossProjectItems,
  remainingCommitments, knownUnperformedScope, coverageDiagnostics
}
```

Use book-currency values with explicit conversion/carrying basis. Contract value, billed net, accounting revenue, cash receipts and invoicing opportunity are five different fields. Gross receipts include tax and cannot be subtracted from net expense to label a profit measure.

## Derive without double counting

```text
calculateProject(snapshot):
  billings = issued net - legal credit net
  revenue = sum(existing revenue owner's included source components)
  directCost = sum(once-only actual expense components attributed directly)
  sharedCost = sum(selected NEXT-104 attribution rows)
  margin = revenue - directCost - sharedCost
  marginRatio = margin/revenue when revenue!=0 else NotApplicable

  billedNotYetEarned = exact existing deferred-revenue owner balance
  earnedNotYetBilled = exact unbilled/contract-asset owner balance
  billingToRevenueBridge = classified differences between billings and revenue
  require every difference has owned timing/credit/adjustment lineage
```

A simplified initial balance equation may be `revenue = billings + change(unbilled) - change(deferred)`, but it is used only when the complete bridge classifies all contract modifications, credits and direct-recognition effects. Do not force that identity by adding an unexplained “other” plug. Raw movements, not ending balances alone, support it.

Time entries used for billable revenue estimation are not automatically payroll expense. Payroll/contractor costs need actual recognized contribution links. A work item already included in unbilled revenue cannot become new revenue again when invoiced. Its billing coverage is consumed through NEXT-77/79.

```text
cashView:
  display actual project-linked receipts and payments with tax and allocation treatment
  unresolved multi-project payments stay unallocated
  do not infer all invoices collected because one project receipt equals their sum
```

Forecasted remaining margin is an optional separate scenario with explicit remaining-cost and pricing assumptions, not historical profit. Future staffing estimates never enter the actual expense table. Revenue recognition and contract-loss decisions remain at their financial owners.

## Capture and controls

Capture each domain at a common recorded/ledger cutoff where its model supports that cutoff. If commercial information has a later revision, label the mixed context and avoid claiming a fully synchronized accounting snapshot. Persist exact membership and formulas, including whichever analytical dimension mode was selected.

At company level, projects plus unassigned reconcile to the selected financial universe, not necessarily every statutory P&L line. Show excluded taxes, central costs or nonproject operations explicitly. Shared-cost allocation is already deducted once from the source/direct view. A single physical GL line cannot be in two complete-cost totals.

## UI and access

Provide Overview, Revenue bridge, Cost detail, Billing opportunity and Actual cash tabs over the same saved snapshot. Sensitive cost details use scoped aggregated projections; an actor allowed to see margin is not automatically allowed to see individual payroll. Recheck permission when exporting or opening original evidence.

```text
billings80000, unbilled movement+10000, deferred movement-5000
  => qualified bridged revenue95000
recognized direct cost40000, shared10000 -> margin45000
cash receipts60000 do not change recognized revenue95000
missing project assignment on expense5000 -> unassigned diagnostics retained
revised staffing estimate -> new forecast, no historical margin edit
```

Completion includes reconciliation and drilldown across actual owners, not a dashboard summing unrelated endpoints at different times. Report “unknown” when a required owner or allocation is unavailable rather than hiding missing cost and inflating margin.
