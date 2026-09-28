# NEXT-123: Autogiro mandates and direct-debit collection outcomes

**Priority when applicable:** P1. **Owner lane:** DELIVERY.

**New scope:** Payment links ask a customer to pay; supplier payment exports initiate outgoing payments. Add authorized direct-debit collection of customer receivables, with payer mandates and returned-payment effects.

**Existing owner to extend:** Existing customer residual, bank-source, external-attempt, notification and payment-capacity owners.

**Earlier contracts:** NEXT-30. **This-wave dependencies:** None.

**Conditional:** NEXT-59: collecting contractually defined installments; NEXT-100: publishing customer integration events.

**Basis:** X11, P30, P71 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Select one actual scheme/bank profile

Bankgirot describes separate payer-consent and payment submission/cancellation workflows through the bank-connected service [X11]. Acquire the exact current agreement, message/status files, notification timing and supported cancellation/return semantics before activation. Do not infer successful collection from the service's marketing description or an accepted file.

```text
DebitMandateRevision {
  customerPayerIdentity, creditorAgreement, mandateReference,
  exactEligibleAccountBinding, actualConsentEvidence,
  providerAcceptance, validScope, revocation/terminationEvidence
}
CollectionIntent {
  originalInvoiceOrInstallmentRefs, mandateRevision,
  exactAmount, currency, collectionDate, noticeArtifact,
  oneEconomicCollectionIdentity, approval, reservation
}
CollectionOutcome {attemptId, providerReference, rawMessage, typedState, bankEventRef?}
```

Payer consent authorizes the scheme-specific debit, not issuance of a new invoice or an arbitrary amount. A recurring invoice template cannot authorize a new mandate by itself. Company-side authority and required payer notices remain separate prerequisites.

## Prepare and reserve

```text
prepareCollection(invoiceSelection, mandate):
  require actual mandate/provider acceptance and permitted payer/invoice relationship
  capture current residuals, disputes, credits, existing payment reservations and term dates
  require proposed amount <= free collectible capacity
  apply actual bank-calendar/notice/cutoff rules from selected scheme
  render exact required notice and retain its appropriate delivery evidence
  seal attempt payload and intended date; require authorized collection approval
```

Dispatch admission reserves the actual collectible capacity under the shared customer/payment owner. Another payment link, manual collection or direct debit cannot reserve the same free amount unnoticed. An unexpected voluntary payment can still arrive after admission; retain it as real cash and resolve any resulting surplus through NEXT-30.

Network/file delivery occurs outside the financial transaction. Stable collection/provider identity and authenticated observations recover ambiguous response loss. Failed/unaccepted consent is not a successful collection. A mandate revoked before admission blocks dispatch; a later revocation does not prove an already admitted debit never happened.

## Accounting only on qualified financial evidence

```text
recordCollectedCash(outcome, bankOrSchemeCashEvidence):
  require actual supported final cash amount/currency and source identity
  debit bank or qualified scheme cash-clearing amount
  credit customer receivable amount
  consume invoice principal and convert the matching reservation to completed use
  save financial receipt and source links atomically
```

If the bank cash is already posted into the scheme clearing owner, adopt its exact unused components without debiting bank again. Provider instruction accepted and payment booked are distinct fields. A rejected instruction releases reservations only under evidence proving the amount will not execute; a local timeout or queue cancellation is insufficient.

## Returns and conflicts

A return after a posted collection is a new actual financial event, not deletion of the original payment. In the first unconsumed supported case, debit AR and credit bank/clearing, append the owned allocation reversal and retain the scheme return identity. Fees are separate evidenced expenses.

If later credits, refunds or setoff consumed the resulting customer balance, require the complete customer-credit/settlement correction path. Do not simply reopen full principal while leaving an already refunded credit liability uncorrected. Retain the bank return and mark its unresolved accounting impact; complete reconciliation cannot ignore the actual movement.

Cancellation of a collection is separate from termination of the mandate. A material mandate or date change requires new preparation. It cannot reuse an unknown previous instruction's capacity. No unsupported automatic retries of rejected bank collections are invented.

## Interface and vectors

```text
invoice125000, paid25000 -> eligible collection<=100000
accepted instruction100000 -> posted AR unchanged until qualified cash evidence
booked100000 -> AR0, one collection receipt
later full unconsumed return100000 -> AR100000, original cash history retained
mandate revoked before admission -> no new request
payment-link capture arrives while debit pending -> retain both real outcomes,
    resolve surplus under customer-credit owner instead of suppressing cash
```

Completion is one bank-qualified consent/notice/collection/return workflow with authorized evidence. No exact file record codes, provider cutoff or refund rights are invented by the pseudocode.
