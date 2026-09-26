# NEXT-31: Invoice-linked prepayments and accrued-cost true-up

**Priority:** P1. **Owner lane:** SCHEDULES. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing subledger schedules/occurrence effects and purchase recognition. Reuse application/subledger/schedules.ts and controls.ts, with separate expense-deferral semantics.

**New scope, not repeated work:** Prior packets use existing schedule mechanics but do not specify complete invoice-to-deferral admission and accrued-cost invoice resolution. This adds those relationships without another scheduling engine.

**Dependencies:** NEXT-03, NEXT-13. **Integrate after:** APP-SLICE-READY(subledger/schedules).

**Conditional gates:** WIP-AST03-UI: the released schedule/control implementation is shared with the asset owner.

**Evidence:** R09, R10 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Linked recognition, not another purchase

```text
CostBasis {
  purchaseRecognitionId, sourceLineIds, expenseAccountRoles,
  costMinor = net + qualified nonDeductibleTax,
  serviceStart, serviceEndExclusive, serviceEvidence, currentCutoff
}
DeferralBasis immutable {
  id, costBasisRefs, prepaidRole, originalExpenseRoles,
  allocatedCost, recognitionProfile, scheduleId, reclassificationRefs
}
AccrualDecision immutable {
  id, suppliedServiceIdentity, serviceCoverage, expectedCost,
  expenseRole, accruedLiabilityRole, evidence, cutoff
}
AccrualResolution immutable {
  accrualId, sourceInvoiceLine, coverageConsumed, liabilityReleased,
  actualCost, expenseTrueUp, taxFactRefs, receipt
}
```

The expense cost excludes deductible input VAT. Deferring cost changes accounting expense timing, not VAT tax-point attribution. An invoice can contain immediately consumed and future service portions. A valid tax invoice does not prove a service spans the dates asserted by the model.

## Build an exact schedule from reviewed service coverage

```text
compilePrepayment(basis, selectedPolicy):
  require same-currency supported service cost, reviewed start/end and cost ownership
  require endExclusive > start and nonoverlapping source allocations
  periods = accounting-period intersections with [start,endExclusive)
  weight[p] = exact covered days OR explicitly selected contractual weight
  # No implicit daily proration when the reviewed policy uses equal months.
  shares = allocateByWeights(cost, weights, selectedResidualPolicy)
  require sum(shares)==cost
  recognizedNow = sum(shares whose service is already consumed under cutoff policy)
  future = cost-recognizedNow
  if purchase is unposted:
      use NEXT-03 purchase compiler with cost split into expense and prepaid roles
  else:
      require existing cost components and unused deferral capacity
      debit prepaid future; credit original expense future
      create no payable, cash or VAT fact
  schedule = existing schedule owner with future expense debit/prepaid credit occurrences
  return complete reclassification + basis + future schedule
```

A partial period uses the selected policy's exact dates, not an entire-month shortcut. Zero shares are retained as schedule metadata where needed but create no zero journal. Final positive installment consumes the remaining amount exactly.

`executePrepayment` uses one application transaction to verify source-cost rights, post the reclassification if needed and insert basis/schedule links. If purchase recognition and deferral form one approval, call both internal writers on the same tx. Do not first post an invoice and then rely on a second unapproved job to repair expense timing.

## Accrued expense before an invoice

```text
compileAccrual(decision):
  require evidenced service already received and reviewed supported estimate
  debit expense expectedCost
  credit accrued liability expectedCost
  no deductible VAT fact without qualified supporting tax evidence

resolveAccrualWithInvoice(accrual, reviewedInvoiceCoverage):
  A = exact accrued liability consumed by this matching coverage
  N = actual expense-cost component for that coverage
  T = qualified deductible tax from the invoice owner
  G = N+T
  require explicit overlap/coverage relationship and 0<=A<=remainingAccrual
  debit accrued liability A
  addSigned expense (N-A)  # Can be a credit for an overestimate.
  debit deductible input VAT T
  credit supplier payable G
  return purchase recognition + accrual consumption + signed expense true-up + tax facts
```

This equation assumes the selected actual cost includes non-deductible tax consistently. Mixed invoices split related and unrelated source-line components before calculation. Do not consume an entire accrual for a partially invoiced service unless the evidence supports full settlement of that estimate. An invoice already recognized must be adopted through a once-only accrual-release/reclassification, not posted again.

## Later changes and controls

Estimate changes affect only future unrecognized schedule cost through an approved revision. A termination/refund ties to the original purchase credit and recalculates remaining deferral; the schedule cannot continue recognizing refunded cost. Past recognized expense stays historical or is corrected by an explicit owned operation. An accrued expense reversal can be scheduled only under a selected policy, not blindly every 1 January.

Controls reconcile opening prepaid/accrued positions plus owned changes to closing GL roles. Unknown service coverage prevents complete signoff. UI shows source invoice/estimate, allocation dates, already recognized amount, future balance and eventual resolving invoice.

```text
cost120000 allocated equally to12 periods -> 10000 each, exact total120000
3 consumed periods -> expense30000, prepaid90000; no second VAT recognition
accrual10000, later invoice cost11000 tax2750 -> accrued debit10000,
    expense debit1000, input debit2750, AP credit13750
accrual10000, actual9000 tax2250 -> expense credit1000, not a balancing plug
same invoice resolves accrual twice -> duplicate economic relationship refusal
```

Calculation/true-up is original design bounded by the reviewed policy. A synthetic date schedule is not automatically a legally qualified expense policy.
