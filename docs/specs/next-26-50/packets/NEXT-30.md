# NEXT-30: Customer unapplied cash, paid credits and refunds

**Priority:** P1. **Owner lane:** COMMERCE. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing customer invoice, payment allocation and legal-credit owners. Add customer-credit liability effects and refund operations through their shared transaction boundary.

**New scope, not repeated work:** NEXT-15 stops at unpaid customer credit principal; NEXT-07 handles suppliers. Add the customer-side surplus and paid-credit lifecycle without changing those original meanings.

**Dependencies:** NEXT-15. **Integrate after:** APP-SLICE-READY(commerce/register).

**Conditional gates:** NEXT-04: credit notes affect a supported VAT return.

**Evidence:** R09, P15, P07 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Separate liabilities from negative receivables

```text
CustomerCreditOrigin immutable {
  id, customerId, currency, amount, kind: unapplied_cash | paid_invoice_credit,
  cashReceiptRef? | creditNoteRef?, journalControlRefs, receiptId
}
CustomerCreditEffect immutable {
  originId, kind: apply_to_invoice | cash_refund | owned_correction,
  signedConsumedMinor, destinationIdentity, journalRefs, receiptId
}
availableCredit = originalAmount - effectiveApplications - effectiveRefunds
```

Use an explicit reviewed customer-credit liability role. Do not put negative amounts into the old nonnegative invoice residual. This is not a universal advance/deposit VAT profile: money received before an identified supply may have its own tax timing and must be routed to a qualified advance owner or a visible blocker.

## Unapplied receipt

```text
compileCustomerReceipt(cashEvent, selectedInvoiceLegs):
  require same customer/currency, supported final cash observation
  G = exact incoming cash
  A = sum(explicit invoice allocations)
  require 0 <= A <= G and each leg <= its invoice remaining
  U = G-A
  require U classified as qualified refundable overpayment/unapplied cash,
          not an unreviewed taxable advance
  debit bank G
  credit receivable controls A
  credit customer-credit liability U
  return journal + invoice allocations + credit origin(U)
```

When the bank receipt was already posted through a qualified clearing entry, adopt its proven unused clearing-side capacity rather than debit cash again. Exact source identity and allocations commit with the journal and credit origin. A different request key cannot produce a second cash event.

## Credit after payment

For one same-currency invoice let `G` be original gross, `K` effective credits, `P` payments applied and `Q` resulting credit liability already refunded/applied elsewhere.

```text
unpaidAR = max(G-K-P, 0)
creditPrincipal = max(P-(G-K), 0)
remainingCredit = creditPrincipal-Q

compilePaidCustomerCredit(original, capacity, credit):
  use original-line net/tax compiler from NEXT-15
  C = credit gross; require original line and tax capacities permit C
  arReduction = min(C, unpaidAR)
  creditIncrease = C-arReduction
  debit original revenue and output-VAT effects exactly once
  credit customer AR arReduction
  credit customer-credit liability creditIncrease
  return journal + negative tax facts + retained legal credit + liability increase
```

Execute this as one customer-credit aggregate, extending legal-credit issuance with its number/semantic document. Prior payment allocations remain historical; reducing revenue is not evidence cash was refunded.

## Apply credit or receive an observed refund payment

```text
applyCustomerCredit(creditOrigin, destinationInvoice, amount):
  require same evidenced customer/currency and current capacities
  debit customer-credit liability amount
  credit destination AR amount
  consume credit amount and invoice principal in one tx
  create no bank movement and no new VAT fact

recordCustomerRefund(creditOrigin, cashPaymentEvidence, amount):
  require authorized evidenced payment or compatible existing clearing posting
  require amount <= remaining credit and exact cash source unused
  debit customer-credit liability amount
  credit bank or evidenced refund-clearing role amount
  append refund allocation and receipt together
```

External refund initiation, when selected, is separately approved and outcome-tracked. A refund API response is not automatically a posted bank payment. Unknown outcomes reserve the affected instruction amount until resolved, using the payment-intent owner rather than adding another reservation balance here.

## Corrections and controls

A standalone reversal of an invoice payment that generated subsequently consumed credit is refused. A correction must restore the related credit/application/refund consequences atomically or identify the unsupported dependency chain. Do not edit `P` to make the equation look right.

Reconcile AR and customer-credit liabilities separately. Display original sale, legal credits, historical paid amount, unpaid amount, credit balance and refunds. Cash-method sales and foreign-currency credit liabilities require their own profile integrations; this first profile is same-currency accrual.

```text
G125000 P100000 K0 -> AR25000, credit0
credit50000 -> debit revenue/VAT50000, credit AR25000, credit liability25000
refund10000 -> debit liability10000, credit cash10000; credit remains15000
apply15000 to another invoice -> liability0, that invoice residual drops15000
cash125000 for invoice100000 -> AR settled100000 + refundable credit25000
new key for same credit note -> AlreadyApplied, not another liability
```

These are new customer financial consequences. Existing supplier refund implementation is a calculation reference, not a shared mutable register or permission to flip signs blindly.
