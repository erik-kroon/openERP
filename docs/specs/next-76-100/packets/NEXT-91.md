# NEXT-91: Apply supplier credit balances to other payable invoices

**Priority when applicable:** P1. **Lane:** PURCHASES.

**New work:** Add noncash application of an established supplier refund/credit asset to another invoice. Creating credits/refunds and supplier advances do not yet define this settlement.

**Use existing owners:** Supplier credit asset, payable residual, allocation and payment reservation owners.

**Required earlier contracts:** NEXT-07, NEXT-57, NEXT-71.

**Evidence basis:** P07, P57, R02. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Pair actual rights

```text
SupplierCreditApplication {creditOrigin, targetInvoice, exactAmount,
  supplierAgreementEvidence, currency, expectedVersions, accountingDate}
CreditOriginPosition = original recognised refund/credit asset - refunds - applications
```

Require the same reviewed legal counterparty and supported currency. Party aliases or a duplicate-identity redirect do not themselves prove contractual permission to use the credit. Supplier advances retain their own treatment and consumption path; this packet initially consumes a genuine recognised credit/refund receivable.

## Prepare and execute

```text
prepareApplication(credit, target, x):
  require x>0 and x<=credit.available and x<=target.payableRemaining
  require actual supplier agreement/remittance allocation and current legal scope
  require no pending refund request or outgoing payment competing for x
  debit target supplier payable x
  credit supplier credit/refund asset x
  freeze exact origin, target, capacities, agreement and source relationships
```

A paid invoice cannot accept another application. Do not select a target simply because it has the same amount. Allocation can span multiple invoices through a fixed set of disjoint legs whose sums match the credit consumption.

Execution rechecks both capacity owners under one book transaction, including exported payment/refund reservations. It posts the noncash settlement journal, appends the credit consumption and target invoice allocation, updates the shared residual readers and saves one receipt. There is no bank entry, new purchase expense or new VAT credit.

If an existing compatible noncash posting already represents the agreement, adopt it through reviewed role/capacity evidence instead of posting again. Either mode must consume each right once; the UI cannot choose both under separate keys.

## Reversal and history

A mistaken application can be reversed through an owned exact allocation reversal while both sides remain available. If the invoice has since been credited, the credit refunded or the period consumed, return the dependency closure and require a supported coordinated correction. A generic journal reversal cannot restore capacity independently of the credit/invoice histories.

Stored balances remain derived from immutable origin/effect records. Do not introduce a mutable supplier aggregate that disagrees with payment eligibility. Statement, ageing and Cash readers see the target residual reduced and credit availability consumed at the same recorded cutoff.

## Journey and examples

Provide a supplier-credit page with eligible invoices, contractual application evidence and exact effects. Mixed currencies or different counterparties are explicitly unsupported unless a later qualified settlement profile exists. A tax-account or private-owner balance is not an interchangeable supplier credit.

```text
credit asset30000; invoiceA50000 -> apply20000 => credit10000, AP30000
then invoiceB8000 -> apply8000 => credit2000, invoiceB0
same credit refund request for remaining10000 races with application -> one wins
all applications plus refunds never exceed30000
journal debit AP20000/credit refundAsset20000; bank/expense/VAT delta0
```

Completion requires the shared invoice residual and refund-capacity consumers, not just the new application screen. Existing NEXT-07/57 identifiers and code remain the authorities for origins.
