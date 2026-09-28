# NEXT-118: Prospective salary exchange into pension contributions

**Priority when applicable:** P2. **Owner lane:** PAYROLL.

**New scope:** Add an effective-dated employee/employer salary-exchange agreement with distinct salary and pension bases. Pension invoice reconciliation alone does not define the waived salary or prevent double deductions.

**Existing owner to extend:** Existing employment revisions, payroll component compiler, pension accrual/provider reconciliation and SLP basis.

**Earlier contracts:** NEXT-20, NEXT-21, NEXT-87. **This-wave dependencies:** None.

**Conditional:** NEXT-36: an already paid or reported period requires a supported correction.

**Basis:** X08, P87 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Contractual inputs

```text
SalaryExchangeAgreementRevision {
  employee, executedAgreementEvidence, futureEffectiveInterval,
  preExchangeSalary, exchangeAmountOrFormula,
  postExchangeSalary, employerExtraPremiumTerms,
  pensionableSalaryBasisFromActualPensionAgreement,
  absence/bonus/terminationTreatment, cancellationTerms,
  ruleAndEligibilityWitnesses
}
ExchangeOccurrence {
  agreementId, payrollPeriod, sourceSalaryEvent,
  waivedSalary, additionalPensionEntitlement,
  payrollRunRef, pensionAccrualRef, consumedState
}
```

The initial profile is prospective voluntary salary exchange under supported employment/pension terms. No net-pay deduction retroactively converts already earned/paid salary into pension. Official guidance makes the actual pension agreement relevant to the pensionable salary/allowable basis [X08]. An employee side note is not enough to redefine that underlying basis.

Do not promise that salary exchange is beneficial or infer social-insurance/pension thresholds from a remembered current amount. The review records the relevant current eligibility/impact information and any required specialist decision before activation.

## Calculation

```text
prepareExchangePeriod(agreement, payrollFacts):
  require agreement effective before the supported salary entitlement boundary
  S = supported gross cash salary before exchange
  E = exact contractual exchange for this period
  require 0<=E<=eligible salary and all applicable safeguards satisfied
  cashGross = S-E
  pensionExtra = exact agreed premium entitlement, including any explicit employer top-up
  pensionableBase = actual pension contract's supported base selector
  retain S,E,cashGross,pensionExtra,pensionableBase separately
  emit one waived-salary modifier and one pension-entitlement component
```

A top-up is an actual employer promise, not automatically the difference between guessed social-tax rates. Existing ordinary pension premium calculations use their contractual base, which might not equal either S or S-E without an explicit rule. General withholding/contribution calculation then consumes cashGross and any other supported taxable components.

## Atomic payroll/pension handoff

The salary expense is the actual qualified post-exchange salary. The exchange amount is not then deducted again from net pay. The additional pension cost/liability is recognized once by the pension accrual owner with its proper tax/SLP classification and external provider identity.

```text
executeRunWithExchange(plan): OwnedTx
  recheck agreement, earning identity, payroll and pension source versions
  post salary/tax/payable effects using cashGross
  record additional pension entitlement/accrual through internal pension writer
  consume exchange occurrence exactly once
  record full run/occurrence/pension links and one aggregate receipt
```

A later provider invoice reconciles and releases the existing pension accrual under NEXT-87. It must not expense the premium a second time. A provider failure or missed transfer does not automatically restore the employee's waived salary; actual agreement rights and supported correction decide the response.

## Amendments and exits

A rate or salary change affects only future eligible occurrences through a new agreement revision. A prepared but unexecuted run becomes stale if its selected agreement changes. Pausing because of absence uses the agreement's actual formula and preserves why a period was skipped; it does not keep deducting a fixed amount from an unsupported zero salary.

Termination inventories unpaid pension contributions and already executed exchanges alongside ordinary final pay. Revoking an agreement does not delete historical premium entitlements. Corrections to already paid/reporting periods use NEXT-36 and preserve original individual declarations.

## Operator view and examples

Show cash salary before/after, premium entitlement, contractual pension base, actual provider premiums and warnings requiring review. Employee acknowledgments are retained separately from operator posting approval. Private payroll grants cover all reads and replay.

```text
synthetic S6000000 E500000 -> cashGross5500000
agreed extra premium530000 -> pension cost/liability530000 once
net salary calculation starts from5500000, not another minus500000 afterward
provider invoice530000 -> releases prior accrual; new premium expense0
pension agreement says post-exchange base -> do not use6000000 because another text says so
new request key for same period/exchange event -> no second modifier
```

Completion is an actual agreement-to-pay-run-to-provider-control journey. It is not a calculator recommending pension optimization or a generic gross-deduction toggle.
