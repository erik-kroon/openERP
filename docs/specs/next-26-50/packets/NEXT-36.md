# NEXT-36: Paid payroll recovery and retroactive compensation

**Priority:** P1. **Owner lane:** PAYROLL. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing pay-run, employee payable, reporting identity and payment evidence owners. Add consumed-history adjustment records without rewriting paid runs.

**New scope, not repeated work:** NEXT-21 only specifies bounded unpaid-run correction. This packet distinguishes later compensation, future-pay adjustment and a gross repayment claim after actual payment.

**Dependencies:** NEXT-21. **Integrate after:** APP-SLICE-READY(payroll).

**Conditional gates:** NEXT-35: the correction includes variable, absence or holiday components.

**Evidence:** R10, P21, X04 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Choose an explicit correction kind

```text
PaidPayrollAdjustment =
    AdditionalCompensation {earningPeriods, plannedPaymentDate, deltaInputs}
  | FuturePayAdjustment {originalPayRefs, lawfulOffsetBasis, futureRun, grossDelta}
  | GrossRecoveryClaim {originalPayRefs, enforceableClaimEvidence, amount}
  | ReportingOnlyCorrection {originalItemIdentity, correctedFacts, evidence}
```

A future-pay adjustment and a gross repayment claim are not interchangeable. Skatteverket distinguishes them, generally retains previously reported withholding and requires the original specification identity for replacement reporting. A gross recovery reporting correction can be made when the amount is claimed, without waiting for cash repayment [X04]. Apply the exact qualified case rather than infer one from a negative amount.

## Retained model

```text
AdjustmentPlan immutable {
  kind, employee, originalRunRevisions, paidEvidence,
  originalDeclarationItemIds, actualClaimOrPaymentDates,
  recomputedSupportedComponents, financialDeltaVector,
  reportingActions, capacityClaims, applicabilityWitness
}
RecoveryReceivableEffect {claimId, originalPaidComponent, grossClaimed, recovered, journalRefs}
ReportingAction {originalStableItemIdentity, targetValues, priorFiledArtifact, reason}
```

A correction references original immutable payslips, actual payments and filed snapshots. It cannot relabel their dates or erase the withholding already credited to the employee.

## Compute the selected branch

```text
compileAdjustment(basis, decision):
  require exact original and current facts, payment/reporting coverage and lawful case
  if AdditionalCompensation:
      recompute only additional entitlement using qualified original/current rules
      create a new earning instruction for actual future payment/reporting basis
      no reversal of original cash or original reporting item merely due to earned date

  if FuturePayAdjustment:
      require qualified right to adjust and sufficient supported future earnings
      record negative earning component consumed ONCE by future run
      future run calculates withholding/contributions on its qualified current basis
      leave original reporting unchanged under this selected case
      do not also create a gross-recovery receivable
      if result would be unsupported negative pay: refuse and select another reviewed case

  if GrossRecoveryClaim:
      G = evidenced gross amount legally claimed
      require G <= unclaimed eligible original compensation
      debit employee recovery receivable G
      credit original wage-cost role G
      preserve original withholding values and cash payment
      reporting action targets reduced original compensation with SAME item identity
      calculate contribution correction separately
      pending authority reassessment is not a posted skattekonto refund

  if ReportingOnlyCorrection:
      prove ledger/pay facts already correct and which declaration facts differ
      produce reporting revision only, no automatic wage/cash journal
```

Where the accounting profile allows recognition of an employer-contribution recovery before authority assessment, use an explicit pending-reassessment receivable and qualified expense reversal. Otherwise retain the expected adjustment as pending. In either case, an actual tax-account adjustment is posted only from its own evidenced assessment event. Do not manufacture a skattekonto balance from filing a replacement.

## Commit and actual repayment

`executePaidPayrollAdjustment` locks the affected employee, original paid-component capacities and reporting identities under the shared book protocol. It replays first, verifies authority and exact basis, then commits all supported financial effects, employee claim/instruction, reporting preparation links and one receipt. It never sends a replacement AGI inside that transaction.

```text
recordRecoveryCash(claim, cashReceipt):
  require actual received amount <= remaining gross receivable
  debit bank amount
  credit employee recovery receivable amount
  append claim allocation; create no further wage/tax correction
```

Future-pay instructions are reserved and consumed by exactly one pay run. Cancelling a prepared run can release an unexecuted instruction, but not undo a paid one. Correcting a recovery claim after repayment needs its complete employee/cash/reporting consequence; otherwise refuse with an impact list.

## Presentation and proof

Show original earnings/payment/withholding, adjustment reason, employee debt or future delta, filed replacement target and actual authority outcome separately. A submitted correction is not an accepted reassessment. Old payslips remain downloadable; a correction notice links to them.

```text
gross recovery20000, prior withholding unchanged -> employee receivable20000,
    wage expense credit20000; original bank/withholding delta0
employee repays5000 -> remaining receivable15000; wage expense delta0
future gross adjustment6000 -> next run earning reduction6000,
    no simultaneous20000-style recovery receivable
same claim/component under new key -> no second recovery entitlement
replacement AGI uses new specification number -> refuse accidental duplicate identity
```

The selected financial dates and recovery rights must be reviewed. This packet does not grant a general right to deduct arbitrary amounts from salary or lower reported withholding.
