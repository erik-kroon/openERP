# NEXT-125: Processor refund initiation with reserved entitlement and outcome recovery

**Priority when applicable:** P1. **Owner lane:** DELIVERY.

**New scope:** NEXT-30 owns customer refund liability and NEXT-39 records processor movements. Add the authorized external refund request and its in-flight financial bridge instead of treating a local refund record as money sent.

**Existing owner to extend:** Existing customer-credit/refund capacity, processor source events and authenticated external attempts; Stripe card refunds are the first bounded profile.

**Earlier contracts:** NEXT-30, NEXT-39. **This-wave dependencies:** None.

**Conditional:** NEXT-64: the original charge was created through the invoice payment-link owner.

**Basis:** X12, P30, P39 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Exact request authority

```text
RefundInstruction {
  book, processorAccount/mode, originalChargeIdentity,
  customerRefundOrigin, amount, currency,
  currentLocalLiabilityCapacity, providerRemainingRefundabilityWitness,
  originalDestinationPolicy, exactPayloadHash, approval,
  requestId, providerIdempotencyKey, cancellationVersion
}
RefundOutcome {instruction, actualProviderRefundId, status, rawEvidence, balanceTxnRefs}
RefundTransitEffect {instruction, processorOutflow, discharge, returnedFunds, journalRefs}
```

Stripe permits partial refunds against an original charge and restricts total refundability. Refunds return through the original payment mechanism; pending/failed/cancelled outcomes and later returned-funds records must be handled [X12]. Do not offer an arbitrary bank beneficiary through the original-charge refund API or copy unsupported Connect/other-payment-method semantics into this card profile.

## Prepare and admit

```text
prepareProcessorRefund(origin, amount):
  require approved commercial credit/overpayment entitlement, not just a desire to refund
  capture local available refund capacity and existing pending disbursements
  retrieve exact original provider charge and its refund inventory outside locks
  require account, mode, currency and customer relationship match
  require no unresolved competing refund/dispute preventing this selected action
  seal amount and original destination; require separate money-movement approval

admitRefund(plan): OwnedTx with no new cash journal
  replay first; verify local refund and attempt versions
  reserve entitlement and instruction amount at shared customer-payment owner
  persist one external attempt/payload and required outbox intent
```

Provider checks remain subject to concurrent manual dashboard action. A later provider refusal is retained, not forced through by changing the amount under the old approval. Reconcile both local rights and processor reality.

## Dispatch and uncertainty

Call the actual refund API outside the transaction with the saved provider idempotency key and exact charge/payment identity. Preserve returned refund IDs immediately in a short reauthorized transaction. Webhooks trigger authenticated observation/refetch, not blind financial authority. Out-of-order statuses are resolved through the current actual object and retained event evidence, not whichever event arrived last.

Response loss first uses known refund ID or provider-supported exact lookup/idempotency within its documented retention window. A new local key is not a provider guarantee. If the original request cannot be proved absent, keep the reserved amount and outcome unknown. Pending due to funding does not authorize a substitute bank refund.

## Financial transit and actual discharge

Some processor funds can move before the customer's claim is conclusively discharged under the selected evidence policy. Preserve both stages:

```text
observed processor refund debit A:
  debit refund-in-transit asset A
  credit processor control A

qualified refund-discharge evidence for A:
  debit customer-credit liability A
  credit refund-in-transit A
  consume customer refund capacity and convert its reservation to completed use
```

When both observations are available, execute the combined group once. NEXT-39 must identify this owned refund instruction and route/adopt its financial component, not also post its generic customer-refund journal. Original balance-transaction identity is unique across retrieval/webhook/payout views.

If funds return before discharge, debit processor control and credit transit, then release the instruction reservation only after qualified final no-execution evidence. If the customer liability had already been discharged, a genuine reversal restores it with a linked refund-settlement reversal, not a fresh sales credit or VAT correction. Unsupported consumed later history becomes an explicit correction case, never negative untracked capacity.

Fees and original processing charges remain separately evidenced. A refund does not automatically refund the original fee or alter the commercial VAT credit. A provider success status is not a claim that the application inspected the customer's bank statement.

## Cancellation and examples

Expose cancellation only where the actual refund/profile supports it. Some card cancellations require an official dashboard flow; do not invent an API. Record the real cancellation and returned-funds evidence before reuse of capacity.

```text
customer credit50000; request20000 -> free instruction capacity30000
processor debits20000 while pending -> transit20000, credit liability still50000
qualified completion -> liability30000, transit0
failure with funds returned before completion -> liability50000, transit0,
  capacity restored only after outcome proof
same processor balance transaction retried -> no second cash/control effect
```

Completion requires one configured authorized refund and recovery path with matching local liability, processor cash and provider references. No packet or standing mandate implicitly authorizes this external money movement.
