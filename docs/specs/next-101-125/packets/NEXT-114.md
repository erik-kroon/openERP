# NEXT-114: EU foreign input-VAT recovery claims and receipts

**Priority when applicable:** P1. **Owner lane:** TAX.

**New scope:** Add foreign VAT recovery from the foreign authority. A foreign tax amount must not be claimed as Swedish deductible input VAT merely because it appears on a purchase.

**Existing owner to extend:** Existing original purchase, evidence, tax-claim obligation, currency and receipt owners.

**Earlier contracts:** NEXT-03, NEXT-49. **This-wave dependencies:** None.

**Conditional:** NEXT-17: an approved foreign-currency refund receivable needs supported FX settlement.

**Basis:** X04, P03 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Candidate versus recognized entitlement

Official guidance distinguishes foreign VAT recovery from Swedish input-tax deduction and describes an EU electronic application through the Swedish service [X04]. The refund country's eligibility, expense categories, establishment restrictions, periods, required attachments and thresholds are qualified inputs. Non-EU paper or other-country procedures are not implied by this first EU profile.

```text
ForeignTaxComponent {
  purchaseRecognitionId, sourceInvoiceLine, refundCountry,
  originalCurrencyTax, originalBookedCostAllocation, invoiceEvidence
}
RefundClaimRevision {
  applicantIdentity, refundCountry, claimPeriod,
  exactSelectedComponentAmounts, countryRuleRelease,
  originalAttachments, registrationEligibility, artifactRefs
}
AuthorityRefundDecision {claimRevision, accepted/rejected component amounts, evidence}
RecoveryReceivableEffect {componentCoverage, originalUnits, bookCarrying, settlements, receipt}
```

A cost can be a claim candidate before a book receivable is justified. The initial recognition profile uses an actual qualified recoverable entitlement, such as a verified authority decision where that satisfies the applicable rule. A submitted request alone does not increase assets.

## Prepare the claim

```text
prepareForeignVatClaim(selection):
  capture original invoices, corrected invoices and prior claim allocations
  require same refund country/applicant and permitted reporting period
  require each source tax amount retained, not inferred from gross at a Swedish rate
  require requested amount <= unclaimed eligible source-tax capacity
  classify each expense under the refund country's actual rule and code list
  include required original document representation and exact currency amounts
  keep rejected/unsupported items with reasons rather than silently exporting only successes
  seal request fields, attachments and applicant authority
```

One component can be partially claimed only if the qualified application supports the split and total coverage is conserved. A repeat submission of the same revision recovers its existing attempt. Another claim period or local ID does not permit claiming the same invoice tax twice. Credit notes reduce the effective eligible source capacity and trigger review of any already filed claim.

## Accounting and payout

```text
recognizeApprovedRefund(decision):
  approved = supported entitlement by component
  targetBook = qualified receivable measurement using explicit currency/date evidence
  delta = target - prior effective recognized entitlement for that coverage
  debit foreign-tax-refund receivable delta
  credit qualified original-cost recovery role delta
  retain original purchase and source foreign-tax facts unchanged
```

If the original nonrecoverable cost entered an asset or unconsumed deferral, its appropriate cost-basis owner must participate. The initial fully-expensed-cost profile refuses unsupported capitalization changes rather than crediting arbitrary current income. No Swedish VAT-return fact is created by this recovery.

```text
recordRefundCash(claim, actualReceipt):
  release the matching original-currency/book carrying receivable once
  debit actual bank/qualified clearing
  credit recovery receivable carrying amount
  separately recognize evidenced FX or bank fee differences through their owner
```

A rejection reduces only a previously recognized entitlement under the qualified correction rule; it does not expense the original purchase twice if it was never capitalized as receivable. An authority grant beyond requested/recognized capacity needs explanation, not automatic surplus income.

## Delivery, review and controls

Retain submitted bytes or an explicit official-service manual handoff and authentic receipt. No API is invented. Additional-information requests link to the original immutable claim and deadline. Country/year/source totals reconcile through candidate, requested, accepted and paid states. Unsupported current rules remain visible gates.

```text
original purchase cost12000 includes foreign tax2000
accepted claim1500 under qualified fully-expensed profile -> AR1500/cost recovery1500
cash1500 -> AR0, no additional expense/VAT effect
claim2000 followed by repeat new-key claim2000 -> duplicate coverage refusal
requested2000, never recognized, rejected -> financial journal0
```

This provides the applicant company's accounting and electronic handoff. It does not promise a refund entitlement, foreign tax advice or production acceptance from a syntactically valid file.
