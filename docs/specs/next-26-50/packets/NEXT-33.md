# NEXT-33: Employee expense claims with one financial handoff

**Priority:** P1. **Owner lane:** PAYROLL. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing source evidence, purchase classification and employee foundation. Reuse liability/allocation mechanics without giving every employee owner-register administration.

**New scope, not repeated work:** NEXT-06 concerns owners. Add employee claim submission/review and an exclusive payroll or direct-payment handoff, not another purchase recognition for the same receipt.

**Dependencies:** NEXT-03. **Integrate after:** APP-SLICE-READY(purchases), APP-SLICE-READY(payroll-foundation).

**Conditional gates:** NEXT-21: the approved payout route is payroll rather than a payable payment.

**Evidence:** R03, R10, P06 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Claim facts and liability ownership

```text
EmployeeClaimRevision {
  claimId, employeeId, paidByEvidence, sourceOccurrences,
  companyBusinessPurpose, submittedItems, currency, revision, previousRevision
}
ClaimDecision immutable {
  revision, approvedItems, rejectedItems, treatmentWitness,
  recognizedPurchaseRefs, reimbursementAmount, reason, reviewer
}
PayoutRoute immutable {
  claimDecisionId, kind: direct_payable | payroll,
  destinationOwnerId, financialRecognitionOwner,
  amount, routeRevision, cancellationOrReplacementRef?
}
UNIQUE economic expense component across purchase/owner/employee recognition
UNIQUE active financial handoff per approved reimbursable component
```

Employee self-service access is restricted to permitted own records and required reviewers. It does not grant general book or payroll directory access. Evidence submission is not approval. Rejected items remain in the source history without creating a liability.

## Review and prepare

```text
prepareEmployeeClaim(revision):
  capture employee identity and exact source/review versions
  for each submitted item:
    confirm company expense, payer and documentary relationship under selected profile
    if already recognized as supplier payable and employee paid it:
        plan AP debit / employee-liability credit, no new cost/tax
    else if not recognized:
        invoke the existing purchase compiler with employee-liability funding role
    else if already employee/owner-funded:
        recover recognized relationship or require conflict resolution
  separate reimbursable cost from taxable cash allowances
  require selected reimbursement route and no conflicting claim component
  seal exact accounting, claimant liability and approved/rejected item manifest
```

A bank/card charge on the company's own account does not automatically create a payable to the employee. Nor may an employee claim VAT just because an image contains a tax amount. NEXT-03's qualified deduction decision remains authoritative.

## Commit and select one payout route

```text
executeClaim(plan): FinancialTx
  verify current reviewed claim revision, source identity and financial owner
  post expense/tax or AP-transfer group through internal existing owners
  create employee reimbursement liability with source-item capacity
  append exactly one route owner for each payable component
  if payroll route:
      add payroll instruction referencing EXISTING reimbursement liability
      do not book expense or liability a second time in payroll
  save receipt and required preparation outbox
```

In payroll the claim may appear on the payslip as a cash reimbursement. Its accounting is debit employee reimbursement liability / credit payroll-payment clearing or bank on actual payout. It is not new salary expense. Taxable allowance components follow the payroll tax profile instead and are excluded from tax-free claim capacity.

For a direct-payment route use the existing payee verification, payment instruction and bank settlement owners. Exporting an instruction does not settle the claim.

## Route changes and recovery

A route can be replaced only if its prior destination owner proves the referenced component unexecuted and unreserved or provides a valid cancellation/release. An unknown payroll/payment outcome blocks another route. Queue cancellation alone is insufficient. A route change retains both decisions and the release receipt.

A correction before payment can reverse/replace the complete claim aggregate if no dependent tax filing or later settlement prevents it. After reimbursement, an overpaid amount becomes a separately reviewed employee receivable or legally supported future offset, not a negative new expense claim. NEXT-36 owns the paid payroll consequence when payroll was the route.

## Controls and visible workflow

Provide employee submission, reviewer side-by-side evidence, approved amount, rejected explanation and payout status. Display claimed, recognized, instructed, paid and recovered states separately. Reconcile employee-liability totals with the GL and payroll-payment handoff, including imported openings.

```text
employee paid qualified purchase net10000 tax2500 -> liability12500 once
payroll shows reimbursement12500 -> no new expense/tax on pay-run posting
direct payment5000 -> employee liability7500
same receipt component resubmitted under another claim -> existing recognition/conflict
switch payroll to direct while payroll payment unknown -> refused, no second instruction
company-paid card receipt -> no employee reimbursement liability
```

This is a claimant workflow around existing purchase recognition. Do not create an independent employee-cost ledger or use a mutable paid flag as the accounting source.
