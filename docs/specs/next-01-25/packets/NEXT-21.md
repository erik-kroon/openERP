# NEXT-21: Payroll posting, payslip and AGI artifact

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/payroll/runs-and-declarations.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/payroll/runs-and-declarations.ts` or the existing equivalent owner |
| Pure calculation | Pay-run journal, paid/reporting bridge, AGI mapping and payslip semantics |
| Atomic scope | Run/correction/payment groups commit atomically; documents render in Bun jobs. |
| Prerequisites | NEXT-20 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-20. Use private payroll access and immutable run semantics. AGI reporting timing follows paid/provided compensation, not creation of a proposed run [X10/X11].

## Atomic accrual/posting

```text
compilePayRunJournal(run):
    for employee:
        Journal.addSigned(cashSalaryExpense, +G)
        Journal.addSigned(reimbursementExpenseOrClearing, +cashReimbursements)
        Journal.addSigned(employeeNetPayLiability, -payable)
        Journal.addSigned(withholdingLiabilityOrProvision, -H)
        for deduction:
            Journal.addSigned(deduction.reviewedDestinationRole, -deduction.amount)
        Journal.addSigned(employerContributionExpense, +C)
        Journal.addSigned(employerContributionLiabilityOrProvision, -C)
        add supported holiday/pension accrual pairs with their own explicit liabilities
        add NO benefit expense when its cost is already recognized
    return balanced journal + per-employee obligation components

executePayRun(command):
    return withAdmittedPrincipal(access, scope, payrollExecutePermission, (tx, principal) =>
        lock book; replay exact command first
        load exact plan and payroll-authorized employee/work/month-capacity basis
        require supported rule witnesses, current grants and unconsumed earning identities
        PayrollDomain.assertApprovedEmployeeAndControlTotals(plan, current)
        approval = validate exact pay-run approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal)
        effects = PayrollDb.insertRunPostingEmployeeObligationsAndReservations(tx, plan, journal)
        OutboxDb.insert(tx, payslip render intents bound to immutable run semantics)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journal.ids, effects}, approval)
    )
    # No cash movement or paid-reporting fact from posting alone.
```

Where the selected accounting profile uses provisional withholding/contribution accounts before payment, retain those roles and the later reclassification explicitly. Do not advertise provisional liabilities as authority-assessed tax.

## Cash and reporting events

```text
recordPayrollPayment(runEmployee, paymentEvidence):
    require actual supported payment identity, payee and amount match employee liability
    initial profile requires full employee net payment; partial pay needs its own qualified allocation
    create or adopt exactly one bank payment through owned salary settlement
    debit employee net-pay liability; credit bank if not already posted
    append PaidCompensationEvent with actual paidOn and original run components
    if actual reporting period/date invalidates calculated tax/contribution profile:
        mark ReportingAdjustmentRequired, preserve originals
        require owned payroll adjustment before final reporting

recordBenefitProvided(runEmployee, benefitEvidence):
    append explicit provided-date/reporting-period event under qualified benefit policy
    no fabricated cash movement
```

An exported salary instruction or an operator's unverified “settled” status is not a PaidCompensationEvent. Missing cash evidence keeps final AGI membership incomplete. Unpaid pay-run accruals remain reconcilable through an explicit accrual-to-paid bridge, not silently included in a paid declaration.

## AGI semantic aggregate

```text
prepareAgi(period):
    capture actual PaidCompensationEvents and qualified BenefitProvidedEvents
    capture existing AGI individual identity inventory and prior submitted revisions
    capture all required employees and zero-reporting applicability
    group by employer identity, actual reporting period, payee identity, specificationNumber
    specificationNumber = retained nonzero stable ID for that reporting item
    for item:
        aggregate exact gross cash, relevant benefits, actual withholding and contribution bases
        apply AGI release's field-level rounding and aggregate-control rules
        validate required identities/periods and every supported conditional field
    compute employer control values from same semantic population
    reconcile paid semantic totals to employee/run registers and GL:
        posted accruals - unpaid/other-period components +/- explicit adjustments
        == declared period components, with all bridges evidenced
    refuse unsupported schema fields/cases or unexplained differences
    return immutable AgiRevision with item identities, mappings, formula lineage and basis
```

Do not recalculate table withholding from the employee's current salary during export. Use the actual recorded withholding and frozen run evidence, with any qualified correction explicitly attached.

## Owned payroll correction

```text
prepareUnpaidRunCorrection(original, correctedCalculation):
    require original has no payment, filed individual record or later dependent consumption
    capture exact original journal, employee obligations and reserved monthly contribution basis
    compile exact reversal + replacement obligations/calculation effects as one owned group
executeUnpaidRunCorrection(command):
    return withAdmittedPrincipal(access, scope, payrollCorrectionPermission, (tx, principal) =>
        lock book; replay exact command first
        load exact approved correction and all original run/payment/reporting dependents
        require no payment, filed individual record or later consumed allocation
        validate original reversal and replacement as ONE owned group
        approval = validate exact correction approval using C5
        journalGroup = JournalApp.postWithinTransaction(tx, complete reversal + replacement)
        effects = PayrollApp.applyCorrectionWithinTransaction(tx, plan, journalGroup)
        PayrollDb.retireSupersededExecutionAuthority(tx, plan)
        OutboxDb.insert(tx, corrected payslip render intent)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journalGroup.ids, effects}, approval)
    )
    # No fabricated cash payment or declaration amendment.

reconcilePaidMonthContributions(period):
    target = contribution policy evaluated over actual paid/provided eligible month population
    attributed = exact effective contribution amount already attributed to that population
    delta = target-attributed
    if delta !=0:
        prepare an owned expense/liability adjustment, with complete paid/accrued bridge
        require approval and atomic receipt before final control reconciliation
    unpaid provisions stay explicit, not included in paid declaration totals
```

Negative recovery of already paid salary, reduced reported withholding and consumed retroactive calculations require their separately qualified recovery profiles. Refuse them in this initial profile rather than apply the unpaid reversal algorithm to paid money. Nonfinancial declaration corrections do not create salary journals.

## XML and amendments

```text
renderAgi(revision, exactSchemaBundle):
    require supported namespace/schema/mapping release actually acquired and hashed
    emit XML from typed semantic fields in required order with strict escaping
    validate exact XSD + employer/person/period/control constraints
    store bytes/hash/schema version/validation result in artifact manifest

prepareAgiAmendment(originalItem, newSemanticResult):
    retain employer, period, payee and SAME specificationNumber
    # A new specification number can add another item instead of replacing the old one [X11].
    require amendment policy permits each changed field
    if withholding decreased and no specifically qualified correction exception:
        refuse and create specialist review case [X12]
    emit replacement/removal operation required by that exact schema, not a second ordinary item
    preserve previous files and submission observations
```

No AGI/KU interchangeability and no “filed” flag from XSD success. Export, signature, submission and assessed outcome are distinct. Empty employer-registered months may need a zero declaration according to their qualified obligation inventory, not simply absence of employees.

## Payslip and vectors

Payslips render the original employee identity/run version, cash components, deductions, net and relevant benefits under payroll authorization. A later employee edit does not change saved bytes. Mark a prepayment slip as calculated/posted, not paid.

```text
G3000000 H900000 N10000 => salary expense3000000;
    net liability2090000 + tax provision900000 + deduction destination10000
January work paid February => February paid-reporting population under the selected rule
same-key pay-run execute => same receipt, one payroll posting
AGI amendment same employer/period/payee/specification => replacement identity retained
unpaid run + no paid evidence => no fabricated paid individual record
```

## Application payment and artifact boundaries

Salary payment accounting and `PaidCompensationEvent` admission are one named application transaction, not a public payment call followed by a separately committed reporting event. Capture actual evidence and compile the payment outside the commit when necessary; execute with C5 current grants, source capacity and approval. A domain state requiring reporting adjustment can be retained honestly, but it must not swallow a failed financial write.

AGI and payslip preparation use C4's captured basis and immutable model sealing. The effect-mq Bun handler renders XML/PDF and runs validation outside financial transactions, then attaches exact artifact/validation references in a short reauthorized tx. A native XSD process is a concrete job dependency, not a database procedure or a Worker request that assumes native execution. Provider submission remains a separately authorized operation.
