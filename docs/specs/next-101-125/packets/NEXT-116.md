# NEXT-116: Recurring car-benefit valuation and employee payment links

**Priority when applicable:** P2. **Owner lane:** PAYROLL.

**New scope:** Payroll already accepts benefit inputs. Add a concrete retained car-benefit eligibility/valuation lifecycle and payment reconciliation so those inputs are not anonymous monthly amounts.

**Existing owner to extend:** Existing employee revisions, private payroll calculations, actual paid/provided reporting and company car cost records.

**Earlier contracts:** NEXT-20, NEXT-21, NEXT-35. **This-wave dependencies:** None.

**Basis:** X06, P20 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Profile and source facts

The first profile supports a reviewed company-provided car and defined ordinary cases. Fuel, congestion/infrastructure charges, mixed employer arrangements, special reductions and retroactive disputes require separately supported branches. A vehicle purchase or rental does not alone prove a taxable benefit was provided to a particular employee.

```text
CarBenefitAssignmentRevision {
  vehicleIdentity, employeeId, effectiveDates, actualAvailabilityEvidence,
  valuationYearInputs, publishedModelFacts, userPaidCosts,
  relevantDrivingEvidence, supportedExceptions, ruleRelease
}
BenefitPeriodResult {
  employeePeriod, assignmentRevision, grossBenefitValue,
  eligibleActualEmployeePayment, remainingTaxableValue,
  cashVsNoncashClassification, providedDateEvidence, formulaWitness
}
EmployeeBenefitPayment {
  assignmentId, period, source: bank|net_payroll_deduction|qualified_direct_cost,
  actualAmount, financialRefs, sourceComponentIdentity
}
```

The official guidance distinguishes payments made with the employee's own funds from a contractual gross-salary reduction [X06]. The latter is not automatically payment for the benefit. A benefit-period output keeps that distinction and never treats negative cash payroll as a generic cure.

## Exact valuation and period capture

```text
calculateCarBenefit(assignment, yearRelease, period):
  require supported vehicle/year/availability facts and complete effective-period evidence
  V = exact qualified formula applied to published input values and selected exceptions
  P = sum(actual eligible employee payments attributable to this benefit period)
  require no payment already credited to another benefit or refund obligation
  taxable = max(V-P,0) under this supported payment-offset profile
  excess = max(P-V,0)  # explicitly unresolved/refundable/other treatment, not negative benefit
  retain original V, P, taxable and the complete formula/data release
```

Not every car-related employee payment reduces every benefit base. The selected release maps each payment type explicitly. Fuel benefits can have different bases; the initial profile cannot reuse the ordinary-car formula for them by changing a field label. More generous employer terms do not override tax eligibility.

A monthly revision is generated from current evidence with a stable assignment/period identity. A later car change creates a new assignment segment. Zero taxable value is retained as a semantic benefit result where the reporting rule needs it, while no artificial zero journal line is created.

## Payroll and accounting handoff

Noncash benefit increases the relevant withholding/contribution bases through NEXT-20 but does not increase employee cash earnings. Company car costs are already recognized through purchases/rental/assets; do not expense the statutory benefit value a second time unless a separately qualified presentation requires explicit offsetting records.

A planned net-pay deduction is not an actual payment until the payroll owner commits its deduction/settlement effect under the qualified policy. Capture anticipated treatment for the proposed run, then bind the exact deduction use atomically with the pay-run records. If actual payment timing changes the reporting basis, create the required adjustment rather than claiming paid evidence from preparation.

```text
executeBenefitHandoff(plan):
  use same transaction as the consuming payroll operation when payment offset depends on it
  persist period benefit, payroll component and any deduction source usage exactly once
  require run/assignment/payment versions agree
  return one owned handoff receipt, not another salary payment
```

Independent bank payments use their own actual financial source and allocation; do not both collect through payroll and use the same amount as an unlinked bank offset. Refund of an excess employee payment requires the real employee-liability/refund treatment, not a negative AGI benefit.

## Controls and vectors

Display vehicle, period, valuation facts, actual employee payments, gross benefit and reportable base. Current private permissions protect all employee-specific reads and replays. A change after filing links to the original individual reporting identity and current payroll-correction owner.

```text
synthetic benefit50000, eligible net payment10000 -> taxable40000
same50000 benefit and gross salary reduction10000 -> benefit stays50000
noncash benefit40000 -> relevant tax bases rise40000, cash gross does not
payment60000 against50000 -> taxable0 plus explicit excess10000
same payment identity in two benefit periods -> source-capacity conflict
```

Completion includes qualified computation, actual payroll/reporting handoff and preserved original cost/payment records. A settings field for a guessed monthly car value is not this capability.
