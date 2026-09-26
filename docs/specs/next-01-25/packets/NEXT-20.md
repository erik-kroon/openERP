# NEXT-20: Frozen regular-payroll calculation

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/payroll/calculations.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/payroll/calculations.ts` or the existing equivalent owner |
| Pure calculation | Qualified salary, withholding and cumulative contribution calculation |
| Atomic scope | Private consistent capture and frozen calculation; no financial effect until run execution. |
| Prerequisites | NEXT-02 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-02. Build on 9050/9107 employment/work/opening records. Initial support: one explicitly supported regular salaried profile. Unsupported leave, cross-border status, special benefit treatment or unknown collective obligations block the affected run rather than becoming0.

## Typed inputs and releases

```text
EmploymentForCalculation {
  employeeId, effectiveRevision, monthlyCashSalary, workPattern,
  taxStatusEvidence, tableIdAndColumnOrDecision,
  benefitComponents[], deductionComponents[], holidayPolicy,
  pensionAndOtherObligations: SupportedTerms|EvidencedNotApplicable|Unknown
}
WorkInput {earningsPeriod, actualSchedule, absence, adjustments, reimbursements, evidence}
PayrollRuleRelease {
  applicableYearAndDates, supportedCases,
  cashProrationPolicy, withholdingTableOrDecisionRules,
  contributionTiersAndEligibility, benefitBaseMappings,
  roundingByComponentAndReportingLevel, checksum
}
CalculationBasis {
  employmentAndWorkRevisions, expectedPaymentDate,
  priorPaidAmountsByEmployeeMonthYear,
  otherCommittedUnpaidRunReservations,
  ruleRelease, sourceCoverage, monthCapacityVersion
}
```

Skatteverket publishes machine-readable withholding tables and dated contribution changes. They must be imported/versioned, not represented as one universal percentage [X08/X09]. A person reference alone is not enough to infer age/status eligibility.

## Explicit calculator

```text
calculateRegularPayroll(basis):
    require all supplied inputs supported, obligations known and revisions compatible
    require no unsupported absence or irregular-period proration
    G = monthly salary after explicitly qualified gross adjustments
    cashReimbursements = sum(supported non-taxable cash reimbursement components)
    taxableBenefits = sum(component withholding bases after qualified employee payments)
    contributionBenefits = sum(component employer-contribution bases)
    N = sum(post-tax net deductions with explicit destination/benefit relationship)
    withholdingBase = G + taxableBenefits

    if withholding decision is fixed explicit amount:
        H = qualified decision amount for this pay event
    else if table:
        wageUnit = convertBaseToTableUnit(withholdingBase, release.tableBaseRounding)
        rows = table entries matching year, frequency, tableId, column and wage interval
        require exactly one row
        H = row.amount or exact evaluation of its published formula
    else if approved percentage decision:
        H = roundRational(withholdingBase*n, d, decision.rounding)
    else: fail MissingWithholdingRule

    totalContributionBase = G+contributionBenefits
    eligibleTiers = select exact dated age/status contribution profile
    function F(base):
        exact = sum(max(0,min(base,tier.upper)-tier.lower) * tier.rate as rational)
        return roundRational(exact.n, exact.d, release.contributionRounding)
    C = F(priorCompatibleMonthlyBase+totalContributionBase) - F(priorCompatibleMonthlyBase)
        # Include owned committed run reservations in the calculation basis to avoid
        # allocating the same monthly band to two concurrent approved runs.

    payable = G + cashReimbursements - H - N
    require H>=0 AND payable>=0 for this bounded profile
    # Do not silently reduce withholding to available cash without a qualified rule.
    extraAccruals = calculate explicit supported holiday/pension components
    return frozen {G,H,N,C,payable,reimbursements,benefitBases,extraAccruals,
                   formulaRows,roundingResiduals,allInputRefs}
```

Do not confuse benefit valuation with new benefit expense. An already accounted car/insurance cost can produce a taxable benefit base without another journal expense. Each benefit declares whether its cost is already recognized, must be recognized by a supported paired effect or is unsupported. Net deductions that reduce a benefit need that explicit relationship; unrelated deductions do not reduce the benefit base.

A contribution tier threshold is scoped to its actual statutory aggregation period and status. `F(prior+new)-F(prior)` avoids granting a monthly reduced band to every pay run. Annual thresholds and exceptional rules require separate exact policy inputs or an explicit unsupported result.

```text
preparePayRun(command):
    basis = application C4 capture through PayrollDb using current payroll-only access
    calculated = PayrollDomain.calculateRegularPayroll(basis)
    return withAdmittedPrincipal(access, scope, payrollPreparePermission, (tx, principal) =>
        lock book; replay exact command first
        require one original regular earning event per employee/pay cycle
        # A new work revision requires correction, not another salary event.
        recheck employee/work/rule and month-capacity dependency versions
        run = PayrollDb.insertFrozenCalculation(tx, calculated, basis)
        return CommandDb.save(tx, principal, command, run)
    )
    # No financial posting, salary payment or declaration yet.
    # Monthly contribution capacity is consumed/reserved only by the owning execution.
```

Later employee changes do not rewrite a saved calculation. New relevant dated work inputs make new execution require a new calculation. Separate employees' evidence capture can continue while one calculation is blocked.

The planned payment date selects an estimated reporting basis. NEXT-21 requires actual payment/benefit evidence and reconciles any period change; creating this run is not proof the employee received income.

## Vectors

```text
synthetic supplied H900000, G3000000, N10000, reimbursements0 => payable2090000
add noncash benefit50000 => relevant tax bases change, cash earnings do not become3050000
synthetic tiers first100 at1/10 then excess1/5:
    F(80)=8; next50 => F(130)-F(80)=16-8=8, not5
missing holiday/pension applicability => blocked, not assumed absent
```

These are design examples. Current statutory rates/tables are not provided by the synthetic inputs.
