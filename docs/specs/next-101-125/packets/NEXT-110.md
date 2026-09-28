# NEXT-110: Borrowing reschedules, debt forgiveness and amended obligations

**Priority when applicable:** P2. **Owner lane:** TREASURY.

**New scope:** Extend existing loan principal/interest with evidenced rescheduling and extinguishment. Merely editing a rate or due date must not erase debt or create an unsupported modification gain.

**Existing owner to extend:** Existing borrowing agreement, principal/interest effect history and payment instruction owners.

**Earlier contracts:** NEXT-32, NEXT-71. **This-wave dependencies:** None.

**Conditional:** NEXT-22: a book gain or cost needs separate corporate-tax treatment.

**Basis:** R02, P32 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Selected profile and distinctions

Start with a same-currency ordinary borrowing whose qualified accounting policy permits the supported modification treatment. Complex effective-interest instruments, debt-to-equity exchanges, derivatives, linked new financing and unqualified fair-value calculations are refused. This is borrower accounting, not a credit product offered to others.

```text
LoanAmendmentDecision {
  originalAgreementRevision, legallyEffectiveDate,
  kind: schedule_only | rate_change | principal_forgiveness | interest_forgiveness,
  signedCounterpartyAgreement, revisedTerms, specificReleasedComponents,
  measurementPolicy, outstandingInstructionRefs, economicIdentity
}
LoanAmendmentEffect {
  decisionId, oldRevision, newRevision, principalDelta, interestDelta,
  gainOrExpenseComponents, futureScheduleRevision, journalRefs, receipt
}
```

A proposal from a lender or an unanswered negotiation is not an effective release of liability. The amendment identifies exactly which principal or accrued interest is discharged, not simply a target lower monthly payment.

## Compute each supported effect

```text
compileLoanAmendment(basis, decision):
  require effective executed agreement, supported policy and exact current obligations
  if schedule_only:
    require sums and entitlement unchanged except explicit dates
    journal=[]; preserve principal and accrued interest
  if rate_change:
    split future accrual timeline at the contractually effective date
    calculate any authorized accrued-interest correction through NEXT-32
    do not assume every rate change implies a present-value gain
  if principal_forgiveness:
    F = exact enforceably released outstanding principal
    require 0<F<=principalRemaining
    debit loan principal liability F
    credit qualified debt-release gain F
  if interest_forgiveness:
    H = exact released interest already accrued
    require H<=recognized interest remaining
    debit accrued interest liability H
    credit qualified interest reversal/gain role H
    future unaccrued interest removal is a schedule change, not income recognized today
```

The book income role and tax treatment are separate decisions. No universal percentage test decides substantial modification here. If the activated framework requires a derecognition/present-value method not implemented by the selected case, return that specific unsupported measurement before producing a financial plan.

Fees charged for the amendment are separate evidenced costs or capitalization under a qualified profile. They are not silently deducted from principal forgiven or automatically expensed without review. Future interest uses the revised principal timeline and terms, avoiding interest on forgiven balances after the effective date.

## Payment and concurrency boundary

Capture every admitted/exported repayment instruction affected by new terms. Unknown old instruction outcomes cannot be discarded when reducing a payment schedule. Before new instructions are prepared, require existing reservations resolved under NEXT-08/71 or explicitly preserved as still capable of execution. A reduced debt plus later executed old cash payment may create a lender receivable; do not hide it by clamping principal to0.

`executeLoanAmendment` rechecks agreement versions, principal/interest capacities, effective dates and payment-reservation inventory. It posts any journal and appends revised terms/schedule/effects in the same book transaction, with immutable receipt and Cash/currentness events. An unposted pure schedule change still needs its own approved relationship and replay identity.

## Read and correction

Show old/new repayment calendar, preserved actual payments, principal reduction, accrued-interest release and any fee. A later correction must respect payments/accruals that consumed the amendment. Do not simply restore the old agreement head while retaining incompatible new payments; require a complete linked adjustment or explicit unsupported chain repair.

```text
principal100000 accruedInterest5000; principal forgiven20000
  => principal80000, interest5000, book gain20000
future rate reduction with no required remeasurement -> principal unchanged
forgive unaccrued future interest3000 -> no current gain3000
old repayment instruction10000 outcome unknown -> cannot replace it blindly with8000
same legal amendment under new key -> duplicate effect refused
```

Completion includes loan controls, future interest calculation and common payment/Cash readers. A editable agreement form without conserved financial effects is not the delivered feature.
