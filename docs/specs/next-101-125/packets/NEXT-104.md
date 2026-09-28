# NEXT-104: Shared-cost attribution across projects and dimensions

**Priority when applicable:** P1. **Owner lane:** REPORTING.

**New scope:** NEXT-43 changes analytical labels. Add conserved fractional attribution of one shared cost to several recipients without duplicating costs or modifying the financial journal.

**Existing owner to extend:** Existing original/reviewed dimension histories and report contribution owner.

**Earlier contracts:** NEXT-13, NEXT-14. **This-wave dependencies:** None.

**Conditional:** NEXT-43: the selected analytical view uses reviewed classification revisions.

**Basis:** R03, P14, P43 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Explicit analytical scope

Start with management-cost attribution, not tax allocation or intercompany recharging. A reviewed allocation may help project profitability, but does not change legal deduction, account identity, company total or original journal dimensions.

```text
AllocationRuleRevision {
  scope, sourceCostSelector, recipientSet, driverKind,
  driverEvidence, effectiveInterval, roundingPolicy, costDefinition
}
AllocationSnapshot {
  ledgerBoundary, classificationCutoff, ruleRevision,
  physicalSourceComponents, exactDriverValues, allocationRows, unresolvedItems, digest
}
AllocationRow {
  originalComponentId, recipientId, signedAttributedAmount,
  weight, totalWeight, residualRank, sourceEvidence
}
```

Use already recognized expense cost, which includes only the appropriate non-deductible tax. Paid cash, asset acquisition capital and expense amortization are different costs. A single source component cannot appear both in a direct-cost result and its full shared-pool result in the same report basis.

## Calculation and residuals

```text
allocateSharedCost(basis, rules):
  require each source component belongs to one compatible selected attribution rule
  require drivers complete, exact and independently evidenced for chosen period
  for source component s:
    sign = sign(s.expenseAmount)
    shares = allocate(abs(s.expenseAmount), nonnegative recipient weights)
    rows = sign*shares with exact source identity
    require sum(rows.amount)==s.expenseAmount
  retain explicit unallocated bucket for unsupported/missing drivers
```

Zero total driver is not an instruction to use equal allocation automatically. Require a reviewed fallback or show unallocated cost. Stable ID tie-breaking ensures reproducible minor-unit residuals, not a claim of economically perfect allocation. Select the actual reviewed method by source/period.

```text
composeProjectExpense(reportMode):
  for every physical expense component:
    choose EITHER direct assignment EITHER its selected allocation rows
    not both
  aggregate by recipient and cost category
  require all recipients + unallocated == included expense universe
```

Separate allocation layers may redistribute support-department cost only under an explicit acyclic sequence. The initial profile disallows circular allocations and arbitrary equations. A later stage consumes the prior stage's attributed rows as lineage, not another copy of original expense in the final total. No hidden reciprocal-cost solver is introduced.

## Retain and revise

Application capture retains fixed source membership, exact driver revisions and current classification mode. Pure calculation produces rows, then a short transaction rechecks the relevant basis and saves the immutable snapshot. Approval of analytical use is separate from financial posting; nothing invokes the journal writer.

A driver correction creates a new allocation snapshot and exact before/after attribution bridge. Old reports retain old amounts. An expense credit carries a negative source component and either references the original allocation basis or a newly reviewed period method; do not silently change original shares with today's headcount.

## UI and output

Provide a driver worksheet, source-pool preview, allocated/unallocated reconciliation and click-through to original entries. Payroll cost drivers require appropriate private permissions or a separately approved aggregate input, not raw employee salary in project-manager context. Cross-book allocations remain unsupported; a firm/client dashboard cannot redistribute one company's expense into another.

```text
shared cost10001, driver A1/B2 -> A3334 B6667; total10001
same source also tagged A -> direct line suppressed in allocated view,
    original unallocated view remains available
missing B driver -> incomplete/unallocated, not A receives100%
credit-10001 with original driver basis -> -3334/-6667
two allocation rules both claim source -> ambiguity refusal, not twice the cost
```

Completion means the allocated report reconciles to the chosen unallocated report at the same source cutoff, with preserved original classifications and independent driver evidence. This is not a tax return allocation or a new writable cost ledger.
