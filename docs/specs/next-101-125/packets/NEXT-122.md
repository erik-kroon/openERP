# NEXT-122: Cash-constrained payment proposals with explicit optimization bounds

**Priority when applicable:** P1. **Owner lane:** TREASURY.

**New scope:** Cash forecasts explain expected balances and budgets constrain authorization. Add a read-only constrained selection/scheduling proposal over actual payable capacity; it does not alter debts, due dates or initiate payment.

**Existing owner to extend:** Existing Cash contribution graph, contractual payment terms, disputes/reservations and payment-plan preparation owners.

**Earlier contracts:** NEXT-71, NEXT-80. **This-wave dependencies:** None.

**Conditional:** NEXT-59: installment promises define permitted partial payment options; NEXT-67: reviewed spending policy contributes constraints; NEXT-99: historical forecast accuracy informs separately reviewed assumptions.

**Basis:** R02, P59, P99 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Fixed problem definition

```text
PaymentProposalBasis {
  horizonDates, reviewedOpeningLiquidity, unchangedBaseContributions,
  candidates: [{obligationId, remainingAmount, allowedPaymentDates,
                legalPartialOptions, mandatoryConstraints, priority, sourceRefs}],
  liquidityFloorByDate, account/currencyPerimeter,
  sourceCoverage, solverPolicy, exactBasisDigest
}
SolverResult {
  selection, objectiveVector, liquidityPath,
  notSelectedObligations, infeasibilityWitnesses,
  searchBudget, bestKnownBound, proofStatus
}
```

Separate contractual due date, agreed extension and proposed payment date. A suggested delay does not amend the creditor's rights or hide overdue status. The system must not invent priorities from legal stereotypes, recommend concealment or omit taxes/payroll obligations it failed to read. The operator selects explicit hard constraints and priorities from qualified facts.

## Avoid double-counting cash

Build the base forecast by excluding exactly the candidate payment contributions that this solver will reinsert. Preserve already dispatched/unknown payment instructions as committed constraints with their current cash treatment; do not make them freely optional. A prior tax transfer or invoice already represented in a batch cannot appear as another outflow.

Initial solver scope is one book currency/account perimeter, a bounded horizon and known finite payment options. Multi-currency FX execution and arbitrary fractional payment amounts are outside the first profile. Partial amounts must be allowed by the existing term/payment owner, not cut down by the solver to make feasibility easier.

## Bounded exact search

```text
searchPaymentOptions(basis):
  reject incomplete mandatory source coverage for an executable recommendation
  sort candidates/options deterministically
  frontier = initial state with unchanged base cash path
  bestFeasible = none
  while frontier not empty AND workBudget remains:
    state = pop best optimistic objective bound
    choose next candidate
    for option in permitted complete/partial/date choices:
      next = state plus option
      update exact cumulative daily cash and hard obligation constraints
      if hard constraint violated: prune with witness
      if unassigned options are outflows only and next breaches floor: prune
      optimisticBound = chosenScore + best possible unassigned scores ignoring liquidity
      if cannot beat bestFeasible under declared lexicographic objective: prune
      if all assigned: validate full exact feasibility and retain best
      else push next
  return feasible candidate plus declared search/proof status
```

The objective's integer priorities and date penalties are a reviewed product policy, not money or a statutory ranking. Stable tie-breaking means deterministic selection, not a guarantee the choice is economically optimal beyond the declared model.

Statuses distinguish proven optimum within the finite model, feasible but search-bounded, proven infeasible within model, incomplete input and no candidate found before budget exhaustion. The last is not proof that no solution exists. For infeasible mandatory outflows, display the exact minimum shortfall/date rather than deleting a mandatory candidate.

## Approval and execution handoff

A saved proposal binds its captured basis and explainable decisions. It has no payment authority. The operator can select its exact result, then the existing payment owner recaptures current payables, holds, beneficiary details and available instruction capacities and prepares a new approval-bound payment batch.

If a material basis changed, show the difference and require review. No plan adjusts legal due dates, relaxes a dispute hold, releases a live instruction or bypasses NEXT-96 approval routing. Actual bank liquidity may change after the calculation; a feasible forecast is not a guarantee a payment will clear.

## UI and examples

Show each chosen/omitted obligation, cash-floor effect, changed expected dates, stated assumptions and why a better-looking alternative was excluded. Missing future income is not silently assumed guaranteed. A stress view can place same-day outflows before uncertain inflows.

```text
available100000; mandatory tax60000; optional invoice50000 -> shortfall10000 if both
allowed explicit installment40000 -> feasible100000 if creditor terms permit
no installment permission -> solver cannot invent40000 payment
search interrupted with one feasible option -> feasible_bounded, not optimal
chosen obligation already included in base forecast -> remove original contribution once
```

Completion requires exact model reconciliation, bounded-search outcomes and current payment-preparation handoff. No autonomous disbursement power is added by this packet or by NEXT-121.
