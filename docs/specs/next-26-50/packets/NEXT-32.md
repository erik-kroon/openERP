# NEXT-32: Loan principal, interest accrual and repayment allocation

**Priority:** P2. **Owner lane:** TREASURY. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing owner-funding principal records and general ledger/schedule owners. Add a loan-specific effect owner without turning capital contributions into loans.

**New scope, not repeated work:** NEXT-06 recognizes funding and loan principal. This proposed product extension supplies the later accrued-interest and repayment lifecycle; it is not presented as a newly discovered source defect.

**Dependencies:** NEXT-02. **Integrate after:** APP-SLICE-READY(subledger/owners).

**Conditional gates:** NEXT-06: shareholder funding already recognized supplies the opening loan basis; NEXT-13: publishing reconciled loan controls.

**Evidence:** R09, P06 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Bounded contractual model

Start with one book-currency borrowing, fixed or evidenced variable simple-interest rate and explicit repayment allocation. Exclude effective-interest amortized-cost instruments, loan origination fee capitalization, leases, foreign-currency borrowing and debt conversion until qualified profiles exist.

```text
LoanAgreementRevision {
  id, borrower, lender, currency, effectiveInterval,
  principalTerms, interestSegments, dayCountConvention,
  paymentAllocationRule, accountRoleWitness, evidence
}
LoanEffect immutable {
  loanId, kind: drawdown | principal_repayment | interest_accrual |
                interest_payment | rate_correction,
  principalDelta, interestDelta, accountingDate, journalRefs, sourceIdentity
}
InterestCalculation immutable {
  loanId, coverageStart, coverageEndExclusive, principalTimelineDigest,
  rateTimelineDigest, segments, exactRationalTotal, roundedTarget,
  previouslyEffectiveInterest, delta, policyVersion
}
```

Interest accrued is distinct from scheduled interest, due interest and paid interest. A contribution with uncertain repayment rights remains a funding classification case, not a loan inferred from a bank transfer.

## Recognition and adoption

A new drawdown debits cash and credits principal liability through the existing source owner. If NEXT-06 or historical opening already recognized principal, adopt that owned balance with evidence and no new journal. One original funding event cannot supply two principal registers.

```text
principalAt(date, cutoff):
  return reviewed opening
       + evidenced drawdowns effective before date
       - effective principal repayments before date
       + supported owned corrections
```

The profile declares whether a payment affects interest from the beginning or end of its effective date. Use that convention consistently rather than guessing from message arrival time.

## Deterministic interest accrual

```text
calculateInterest(loan, start, end, cutoff):
  require start<end and complete principal/rate timeline
  boundaries = union(start,end,principalChangeDates,rateChangeDates,yearSplitsIfNeeded)
  sum = rationalZero
  for segment [a,b):
      P = principalAt(a); rate = applicableRate(a)
      require P>=0 and one supported rate
      factor = exact dayCountFraction(a,b,convention)
      sum += P * rate * factor
  target = roundExact(sum, selected cumulative rounding policy)
  effective = prior accrued interest for the same owned coverage basis
  return target-effective with full segment witness
```

Recompute from a stable coverage origin or retain exact accumulated residuals. Do not round each day independently. A rate revision requires an explicit effective date and changed-source witness. A subsequent calculation posts the delta to the same cumulative target, not the full target again.

```text
postAccruedInterest(delta):
  debit interest expense delta
  credit accrued interest liability delta
  # negative deltas use opposite signs with an approved correction reason
```

## Repayment allocation

```text
prepareRepayment(cashSource, contractualSplit):
  read exact principal and accrued/due interest balances
  split = explicit reviewed principal, interest and separately evidenced fees
          OR the agreement's qualified deterministic waterfall
  require principalPart<=principalRemaining
  require interestPart<=recognizedInterestRemaining or accrue approved missing part atomically
  require sum(parts)==actual cash amount
  debit principal liability principalPart
  debit interest liability interestPart
  debit qualified fee expense feePart
  credit bank actualCash
  seal register deltas and exact source allocation
```

Execution rechecks agreement/timeline/capacity under the book lock and commits journal, principal/interest effects, cash adoption and receipt together. Automatic bank instructions are outside scope. An existing payment journal can be adopted only with exact role/capacity evidence.

## Changes, output and vectors

A backdated principal or rate change after accrued/paid interest creates a recalculation impact. Compute an explicit delta with stable coverage and preserve prior statements. If a correction requires changing already settled history beyond the supported scope, refuse with affected effects; do not alter old cash payments or simply reset the principal.

Show opening, drawdowns, principal repayments, accrued interest, paid interest and independent lender-statement differences. Missing lender statements are unknown coverage, not zero difference.

```text
principal10000000, annual6%, ACT/365F, 30days -> 49315 minor after half-up
accrue49315 twice with same coverage -> second economic effect0/replay, not98630
repay principal1000000 + interest49315 -> cash1049315, principal9000000
different explicit rates across boundary -> split exact rational segments before rounding
adopt shareholder principal already posted -> ledger delta0
```

No tax deduction, related-party price or legal loan validity is inferred from this arithmetic. Those are qualified profile inputs and are not solved by selecting an interest formula.
