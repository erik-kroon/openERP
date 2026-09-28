# NEXT-88: Employment termination and final-pay obligation closure

**Priority when applicable:** P2. **Lane:** PAYROLL.

**New work:** Add a reviewed employment-end event and complete final-pay inventory. This is not another regular salary or generic paid-correction implementation.

**Use existing owners:** Employment/work revisions, holiday balances, employee claims, payroll runs and paid-reporting owners.

**Required earlier contracts:** NEXT-20, NEXT-21, NEXT-35, NEXT-36.

**Conditional gates:** NEXT-87: pension obligations require a final provider settlement.

**Evidence basis:** R03, P35, P36. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## End event and still-open obligations

```text
TerminationRevision {employeeId, actualEmploymentEnd, noticeTerms,
  lastWorkCoverage, reasonCodeRestricted, applicableAgreement,
  finalPaymentPolicy, signedDecisionEvidence}
FinalPayInventory {ordinaryEarned, unprocessedVariablePay, remainingHoliday,
  benefitsEndFacts, reimbursements, lawfulDeductions, pensionItems,
  unfulfilledExternalReporting, unknownItems}
```

Ending employment does not erase a debt, future payroll adjustment or access to retained payslips through an authorized historical channel. The source event and private personnel documents use payroll access, not general party directory permissions.

## Calculate a bounded final run

```text
prepareFinalPay(termination, cutoff):
  capture complete paid/recognized/work/holiday/claim membership
  require termination date and actual scheduled work, not salary divided by30 by default
  use qualified payroll formulas for remaining salary and unused leave entitlement
  release already accrued holiday and related provisions to avoid duplicate expense
  include approved unpaid reimbursements through their existing liability route
  enumerate every proposed deduction with its separate lawful basis
  do not offset a recovery claim merely because the employee owes the company money
  calculate withholding/contributions using actual intended payment/reporting facts
```

The first supported profile excludes complex severance, disputes and cross-border exit treatment unless explicitly qualified. Unknown final expense claims or benefit-return facts remain open checklist items rather than zero amounts.

Final-run execution is an ordinary payroll aggregate with exact approval, input versions and earning identities. It consumes each outstanding source component once. A concurrent regular run for the same earning period cannot pay the same wages again.

## Close scheduling without blocking legitimate later facts

```text
executeEmploymentEnd(plan):
  atomically retain end revision and stop eligible future recurring work-generation rights
  invalidate unexecuted overlapping salary preparations
  leave original approved/paid runs and reporting items unchanged
  create final-pay and remaining-obligation tasks through existing owners
```

A scheduled payment already admitted externally cannot be cancelled merely by ending the employee record. Its payment owner resolves the actual outcome. New post-end earnings corrections must reference the ended employment and use NEXT-36, not resurrect an active recurring salary template.

## Reporting and final status

Paid/provided dates determine reporting under the qualified rules, independent of last employment day. NEXT-73 handles submission. A final-pay slip does not prove all employer obligations are discharged.

Define `financialObligationsComplete` from an exact inventory: all known pay and benefit cases resolved, employee/withholding controls reconciled and required follow-up assigned. Keep separate states for employment ended, final calculation, paid, declarations handled and unresolved provider obligations.

```text
holiday liability12000; final supported holiday pay15000 -> release12000,
    additional expense3000, not another15000 expense
employee claim2000 routed to final payroll -> claim liability consumed once
recovery claim5000 but no lawful deduction decision -> cannot silently reduce net5000
new expense claim after final run -> new owned claim/payment, no repeat final salary
```

The UI must expose missing facts and the exact reason completion remains open. No automated employment-law judgment or blanket deduction authority is created.
