# NEXT-64: Invoice payment links with outstanding-bound settlement

Priority: **P1 when applicable**. Lane: **PAYMENTS**.

**New deliverable:** Add a customer payment request tied to an already issued invoice or installment. NEXT-39 reconciles processor money after events exist and does not own the checkout request.

**Existing owner to extend:** Existing invoice residual, external-attempt/credential, processor clearing and customer-credit owners.

**Required contracts:** NEXT-30, NEXT-39. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-59: A link covers a selected installment rather than the entire residual.

**Crosswalk:** PRY-131; canonical family COM-03/05, OPS-03. An invoice payment link precedes settlement; NEXT-39 remains processor-event accounting.

**Atomic result:** No invoice at link creation; processor/cash settlement through original owner.

**Evidence:** R03, R05 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Intent identity and capability

`InvoicePaymentIntent` pins book, legal invoice, selected installment/amount, currency, current residual version, payee merchant account, expiry and allowed partial-payment policy. `ProviderCheckoutBinding` records the exact external object and safe return/display metadata. Link creation is not a new invoice, reservation of revenue or evidence of cash.

A guest browser receives only a bounded token that resolves to this intent. It cannot supply a different merchant account, invoice ID, currency or amount to the server after review. The source of current collectibility is the native invoice residual, not the amount cached in a link.

## Creation and completion

```text
prepareLink(invoice,selection):
    require issued supported invoice, current positive selected residual
    capture authorized merchant/payee configuration and exact amount/currency
    seal request intent and selected external profile

admitCheckout(intent):
    short tx: reauthorize, replay, recheck residual/expiry/cancellation
    create stable provider attempt
    outside tx: create selected checkout object with that identity
    short tx: retain provider correlation and exact amount binding

observeProviderCompletion(event):
    authenticate source and bind merchant/account/environment
    fetch authoritative object using selected provider contract when needed
    require amount/currency/intended invoice relationship matches
    retain payment observation and call existing processor settlement workflow
```

Success navigation in the browser is not a financial result. A provider authorization is not a captured payment, and a captured payment is not a bank payout. NEXT-39 owns processor cash and fees; the link owner never posts a second receipt from its redirect callback.

## Concurrency and residual changes

One use means one supported successful payment occurrence for the intent, not that no duplicate callback can arrive. Provider enforcement must be real and documented. If the provider does not support atomic single-success semantics, record that limit and rely on native payment identity, not a promised guarantee.

Invoice payment, credit or cancellation before checkout dispatch admission can make the old intent stale. If the external payment was already admitted and later succeeds, retain real money honestly: settle only remaining native principal and route surplus through NEXT-30. Do not reject the cash observation and pretend the customer was never charged.

A partial-payment link must specify its minimum/maximum and updated residual policy. New checkouts for the same invoice cannot cumulatively overconsume principal. Provider unknown outcome blocks unsafe replacement where duplicate charging is possible. Closing an old link does not refund a captured payment.

## UI, source and Cash integration

The invoice page presents amount, currency, payee and status before redirect. After return it shows confirmed, pending or unknown based on retained server evidence. Receipts link invoice application and processor source. Book users can expire or replace unexecuted intents with reasons; refunds stay with the actual refund owner.

Cash forecasts read the same remaining invoice/instalment occurrence. Creating a link neither adds a second expected inflow nor changes due dates. Customer statements reflect actual applications and credit balances.

Synthetic invoice125000: link40000, successful captured event40000, native residual85000. A second delivery of the same event changes nothing. If another payment settles125000 before an admitted checkout finally captures40000, the real excess becomes customer credit40000, not an extra sale or a negative residual.

Completion requires one configured provider's authorized sandbox journey, verified callback/recovery, invoice change race and processor reconciliation. Offline intent logic remains useful but is not connected-payment acceptance. No paid card-processing service is made a prerequisite for core self-hosted accounting.
