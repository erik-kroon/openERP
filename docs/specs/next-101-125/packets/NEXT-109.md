# NEXT-109: Insurance-loss claims and gross compensation accounting

**Priority when applicable:** P2. **Owner lane:** COMMERCE.

**New scope:** Add insured-loss claims, recognized recoveries and insurer-to-repairer settlements. Insurance compensation is not ordinary sale proceeds or a grant and must not hide gross damage/repair effects.

**Existing owner to extend:** Existing damaged-asset disposal/impairment, purchase recognition, receivable and payment owners.

**Earlier contracts:** NEXT-03, NEXT-13, NEXT-19. **This-wave dependencies:** None.

**Basis:** R03, P19 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Retained loss and claim identities

```text
InsuredLoss {
  incidentId, affectedAssetOrExpenseComponents, incidentDate,
  originalEvidence, policyRevision, insurerIdentity, claimReference
}
ClaimDecisionRevision {
  claimedAmount, acceptedAmount, currency, deductibleOrExclusions,
  recognitionEligibility, evidence, expectedPaymentDate, previousDecision
}
RecoveryEffect {
  claimId, kind: recovery_recognized | amended | cash_received | direct_settlement,
  entitlementChange, settledAmount, journalRefs, providerEvidence, receipt
}
```

The loss event and insurer recovery have separate recognition dates and evidence. Filing a claim or receiving an automated claim number does not establish a recoverable receivable. The first profile requires a qualified accounting recognition decision supported by an actual accepted entitlement or other sufficient evidence under the selected rule.

## Gross recognition and changes

```text
prepareInsuranceRecovery(loss, decision):
  require insurer/legal entity/currency and covered incident identified
  require loss/cost/asset effects already represented or explicitly pending at their owner
  T = qualified recognized claim entitlement, not management's requested amount
  currentTarget = effective recognized claim entitlement
  delta = T-currentTarget
  debit insurance receivable delta
  credit qualified recovery-income or permitted separate recovery role delta
  retain coverage references; do not reverse original impairment/repair cost
```

An insurance deductible reduces the approved recovery or reflects a separate retained cost, not a second expense merely because both the policy and repair invoice mention it. A repair's recoverable input VAT can affect the insurer settlement basis without changing the invoice's legally determined deduction. Do not derive VAT treatment from the insurer amount.

A downward revised entitlement after prior cash settlement can create an insurer repayment liability. It is not a negative receivable left hidden in a nonnegative schema. The initial workflow must either support that explicit liability/recovery or refuse the consumed-history adjustment with a complete impact list.

## Cash and direct settlement

```text
recordInsurerCash(claim, actualBankReceipt):
  require amount<=remaining eligible receivable or explicitly classified excess
  debit bank amount
  credit insurance receivable amount
  consume claim settlement capacity and source payment once

recordInsurerPaysRepairer(claim, supplierInvoice, evidence):
  require enforceable same covered payment and both obligations outstanding
  debit supplier payable amount
  credit insurance receivable amount
  consume supplier payable AND claim capacity on one tx
  company bank movement =0
```

The repair invoice is still recognized once at its actual purchase/tax terms. Direct insurer payment is a noncash discharge linked to independent proof, not a second invoice expense or an unverified note marked paid. Any remainder due to the supplier stays outstanding.

If the insurer replaces an asset in kind or owns the salvage, the rights and valuation require a separate supported policy. Do not treat a replacement asset as a free addition at the old acquisition cost. The existing asset owner decides disposal and new recognition with actual evidence.

## Application and controls

Prepare from a consistent loss/claim/invoice/source basis, then validate exact decision versions, economic identities and current approval at execution. Journal, receivable/payable effects, independent source usage and receipt commit together. External insurance portal correspondence occurs outside that transaction and carries no authority by itself.

Show original loss, claim demand, qualified recognized entitlement, actual receipts, insurer direct payments and pending disputes separately. Reconcile claim receivables to their GL role and affected supplier balances. A report may present gross loss and recovery with a disclosed relationship; it cannot simply delete both because they approximately net.

```text
asset carrying50000 written off by asset owner; recognized compensation40000
  => independent loss50000 and recovery income40000, net economic loss10000
repair AP12500; insurer entitlement10000 paid directly to repairer
  => AP debit10000, insurance AR credit10000, AP remainder2500, bank0
claim requested50000 but unaccepted/uncertain -> no automatic AR50000
same insurer bank receipt imported twice -> one recovery allocation
```

This is the insured company's accounting, not insurance underwriting or a lending product. Legal recognition, payout rights and tax treatment are qualified inputs, not consequences of the claim's UI status.
