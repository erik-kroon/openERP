# NEXT-35: Variable pay, absence and holiday-liability reconciliation

**Priority:** P2. **Owner lane:** PAYROLL. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing payroll employment/work facts and frozen regular-pay calculator. Add one explicitly selected variable/hourly/absence profile and a holiday-liability rollforward.

**New scope, not repeated work:** Extend the first wave beyond fixed salary. Do not replace its tax-table selection, employee directory or pay-run posting authority.

**Dependencies:** NEXT-20. **Integrate after:** NEXT-21.

**Evidence:** R10, P20, P21 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Precisely bounded inputs

```text
WorkSegment {
  employee, startInstant, endInstant, localScheduleDate,
  kind: worked | overtime | paid_absence | unpaid_absence | sick,
  contractRevision, sourceTimesheetOrDecision
}
VariableEarning {sourceIdentity, units, rate, entitlementDate, intendedPayRun}
HolidayOpening {employee, entitlementUnits, moneyLiability, socialProvision, evidence}
HolidayMovement {
  kind: earned | used | expired_if_qualified | paid_out | corrected,
  units, valuationBasis, sourceIdentity, recordedAt
}
```

The scope is one reviewed employment/agreement regime at a time. Irregular schedules are explicit input. Do not assume 40 hours/week, five working days or a salary/30 deduction. Collective-agreement, sick-pay, waiting-deduction and holiday formulas are dated qualified data/code from the selected release, not embedded guesses.

## Normalize the actual work timeline

```text
normalizeWork(inputs, contractCalendar):
  convert instants to actual contract timezone and local work segments
  split at contract/rate/date and schedule boundaries
  reject duplicate source components and impossible negative intervals
  reject overlapping mutually exclusive worked/unpaid-absence segments
  require each scheduled interval accounted for or explicitly unresolved
  calculate exact worked, overtime and absence units by qualified calendar rules
```

Use paid hours or contractual unit meanings, not clock duration blindly. DST can produce a difference between elapsed and contractual time. If the supported profile cannot resolve that case, retain it for review.

## Calculate additional components

```text
calculateVariablePay(basis):
  work = normalizeWork(...)
  components = []
  for segment:
    formula = qualifiedRelease.select(segment.kind, employmentFacts, dates)
    require exactly one applicable formula and required facts
    components += formula.evaluateExact(segment, earningsBasis)
  components += explicit separately sourced bonus/commission amounts
  verify no earning or absence source is consumed by another active run
  pass component bases to existing NEXT-20 withholding/contribution calculator
```

The component classifier explicitly determines cash, taxable benefit, withholding base, employer-contribution base and holiday-accrual base. One amount may participate in several calculation bases without becoming several expenses. Reject unsupported treatment rather than classify every benefit as cash pay.

## Holiday liability as an owned rollforward

```text
holidayTarget(employee, cutoff):
  units = reviewedOpeningUnits + earned - used - qualifiedExpiredOrPaidOut
  value = qualifiedValuation(units, retainedRateAndEarningBasis, cutoff)
  socialTarget = qualifiedContributionProvision(value, applicableFacts)
  return {units, value, socialTarget}

compileHolidayAdjustment(currentControl, target):
  moneyDelta = target.value-currentEffectiveMoneyLiability
  socialDelta = target.socialTarget-currentEffectiveSocialProvision
  debit holiday accrual expense moneyDelta
  credit holiday liability moneyDelta
  debit social accrual expense socialDelta
  credit social provision liability socialDelta
```

Negative deltas reverse the relevant accrual effects, not paid wages. During holiday pay H, the payroll compiler debits the existing holiday liability to the eligible accrued extent and expenses only the unprovided remainder. For actual contribution S and released provision SP, it debits provision SP, posts expense delta S-SP and credits payroll contribution liability S. It does not expense the same holiday cost or contribution twice. All released provision capacities are explicit and current.

## Commit, correction and interface

Pay-run execution binds the frozen normalized work, component outputs, monthly cumulative tax/contribution basis and holiday effects. Internal payroll and holiday writers share the same tx. All employee rows in an approved run are either committed as its supported aggregate or none are.

A time correction after approval creates a new run revision. After payment, NEXT-36 owns the financial/reporting delta. Old timesheets, payslips and declaration inputs remain reconstructable.

Expose component explanations and holiday opening/earned/used/closing balances in payroll-only UI. Salary privacy is not weakened for general report views. Reconcile holiday-related GL controls independently of the cash payroll register.

```text
synthetic 75/2 hours *2000 minor/hour -> cash earning75000
overlap: same hour both worked and unpaid_absence -> conflict, no calculation
holiday opening10000 + earned2000 - consumed3000 -> target9000
prior posted holiday liability10000 -> adjustment-1000, not new9000 credit
holiday paid3000 already accrued -> release liability3000, do not expense3000 again
```

These vectors prove mechanics only. Support for a real sick-pay or holiday regime requires its exact reviewed formulas and agreement inputs.
