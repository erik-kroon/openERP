# NEXT-39: Processor balance and payout clearing, Stripe first

**Priority:** P1. **Owner lane:** TREASURY. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Source retention, customer settlement/refund owners and bank reconciliation. Add a selected Stripe balance-transaction adapter and processor control ledger projection.

**New scope, not repeated work:** Plaid packets cover bank feeds and webshop WIP covers orders. Neither specifies processor gross/fees/refunds/payout clearing. This packet owns that financial reconciliation, not sales-order intake.

**Dependencies:** NEXT-30. **Integrate after:** APP-SLICE-READY(source-intake), APP-SLICE-READY(commerce/register).

**Conditional gates:** NEXT-40: processor balances use a non-book currency; WIP-COM2-W1: read-only order provenance is required; do not modify its intake.

**Evidence:** R03, R09, X01, X02 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Identity and exact source interpretation

```text
ProcessorObservation {
  accountId, liveOrTestMode, balanceTransactionId,
  rawSourceRef, providerSourceId, type, reportingCategory,
  currency, grossMinor, feeMinor, netMinor, availableOn, recordedAt
}
ProcessorEffect {observationIdentity UNIQUE, ownedFinancialKind, journalRefs, settlementRefs}
PayoutMovement {providerPayoutId, debitBalanceTransaction, transitRole, bankSettlementRefs}
```

Stripe exposes exact integer gross, fee and net fields with `net=amount-fee`. Its payout filter is documented for automatic payouts only [X01/X02]. Keep account, mode and currency in identity. Do not silently use a test-account object or another connected account's record.

Retain fetched pages/raw bytes and normalize through a pinned provider profile. Webhooks can trigger fetch/reconciliation but arrival order does not establish accounting order. Capture a fixed retrieval interval, deduplicate exact provider IDs and compare to independent processor balance/report controls. A list ending is not proof of all historical activity.

## Classify explicitly, never net payouts as revenue

```text
compileProcessorObservation(o, economicLinks):
  require gross-fee==net and exact supported currency/scale
  if charge/payment:
    require recognized sale or authorized customer obligation relationship
    debit processor control net
    debit qualified processor fee cost fee
    credit customer AR gross
    allocate AR principal; create NO new sale/VAT

  if refund:
    require original refund/credit liability and its remaining capacity
    R = -gross; require R>=0
    debit customer-credit liability R
    debit qualified refund fee cost fee
    credit processor control R+fee
    consume customer refund capacity; create NO second credit-note tax fact

  if payout:
    P = -net; require ordinary supported payout and reconciled gross/fee shape
    debit payout-in-transit P
    credit processor control P

  if supported fee-only:
    debit qualified fee cost(-net)
    credit processor control(-net)

  otherwise:
    return RequiresClassification(originalObservation, preciseUnsupportedType)
```

Fee tax, refunded fees and cross-currency conversions require explicitly supported variants. A missing supplier fee invoice may permit gross-cost posting only under a qualified policy, not an invented input-VAT deduction. Missing sale recognition produces a link/review prerequisite, not fabricated revenue from the payout.

## Disputes, reversals and cash

A dispute debit is not necessarily a credit note or bad debt. For a supported recoverable hold, debit a dispute receivable and credit processor control with separate fee treatment. If won, clear the receivable against the processor credit. If lost, a reviewed decision reclassifies the receivable to the appropriate loss; VAT treatment remains a separate qualified decision. An unsupported reserve/Connect/capital transaction remains visible and blocks complete control reconciliation.

```text
recordBankPayoutReceipt(payout, bankObservation):
  require exact provider/bank relationship, currency and current transit capacity
  debit bank amount; credit payout-in-transit amount
  or adopt existing compatible cash/clearing posting
  append settlement; do not create revenue/expense again
```

A payout failure reverses its transfer to transit only if evidence proves the original cash did not settle. If funds reached the bank and later returned, retain both real cash events instead. Never use a status flag to erase cash.

## Atomic effects and independent controls

Each supported balance transaction commits its journal, customer settlement/refund or transit effect and once-only source identity together. Aggregating a complete payout can use a fixed manifest of these identities; no second accounting pass posts their totals again. Same source fetched through both balance API and payout API resolves to one effect.

```text
processor closing = reviewed opening + sum(all supported net balance effects)
payout transit closing = payouts moved out - actual bank receipts - supported failures
```

Compare both with independent provider/bank evidence. Availability date can partition pending/available states without being another principal posting. Manual payouts reconcile from the full ledger/balance history, not an unsupported automatic-payout membership assumption.

```text
charge125000 fee3000 -> processor122000 + fee3000 - AR125000
payout122000 -> transit122000 - processor122000
bank receives122000 -> bank122000 - transit122000; revenue delta0 throughout
same txn read under payout and balance list -> one journal effect
unknown reserve debit -> visible unclassified difference, not silently omitted
```

Initial implementation requires an authorized Stripe read configuration and reconciliation fixture. It does not claim all gateways, Connect modes or merchant-of-record arrangements are supported.
