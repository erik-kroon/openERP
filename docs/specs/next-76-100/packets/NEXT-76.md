# NEXT-76: Accepted contract changes and sales-order billing limits

**Priority when applicable:** P1. **Lane:** SALES.

**New work:** Add reviewed post-acceptance scope/price changes and billing-capacity conservation. This is not another webshop order intake, catalog or recurring-template owner.

**Use existing owners:** Existing quote, order, catalog revision and invoice conversion owners.

**Required earlier contracts:** Existing core operation owners.

**Conditional gates:** NEXT-51: issuing invoices with the chosen tax/price profile.

**Evidence basis:** R02, P29, P66. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Records and stable components

```text
ContractRevision {contractId, customer, currency, effectiveInterval, acceptedEvidence,
  components:[{stableComponentId, unit, agreedQuantity, agreedNetCap, priceRule}]}
ChangeOrder {originalContractRevision, changedComponents, effectiveFrom,
  customerAcceptanceEvidence, internalReview, reason, supersededDrafts}
BillingCoverage {componentId, sourceOccurrence, reservedQuantity, issuedQuantity,
  reservedNet, issuedNet, originatingInvoiceId, changeAuthority}
```

An internal quote update is not evidence the customer accepted a variation. Stable component IDs survive revisions; cloning the order cannot reset already invoiced coverage. Quantities with different units are not additive.

## Pure preparation

```text
prepareChange(basis, proposal):
  resolve exact accepted contract and current component coverage
  require same legal customer/currency for the bounded profile
  for component:
    floorQuantity = irrevocablyIssuedQuantity + remainingLegitimateReservations
    floorNet = irrevocablyIssuedNet + remainingLegitimateReservations
    if proposed cap below its consumed floor:
      return RequiresCreditOrApprovedReservationRelease(affectedRefs)
    compute new remaining rights, explicit price-effective boundary and deadline changes
  identify affected UNISSUED drafts and acceptances
  freeze before/after component rights plus actual acceptance evidence
```

A cancellation of remaining scope does not delete an issued invoice or reverse earned revenue. A credit can fix an earlier invoice, but it does not automatically grant permission to bill the same delivered service again. A replacement billing right requires a specific approved relationship.

## Application transaction

`executeContractChange` locks the current contract/order and component versions, checks current authority and exact approval, then inserts the new revision and closes/replaces affected unissued reservation authority. It calls the existing sales-order amendment writer on the same tx; it creates no revenue, tax fact or receivable. The record/receipt and notifications commit together. If a legal issue races with a reduction, the shared order-capacity lock makes one stale rather than both spending the same capacity.

Invoice draft generation reads the selected accepted revision and explicit coverage. Final issue rechecks and consumes the same exact rights through an internal owner port. A displayed quote total is not a writable balance.

## Readers and correction

Show original agreement, customer acceptance, every variation, issued amounts and remaining rights. Forecasts read the unbilled remainder only as a labelled commitment, not a booked receivable. Material currency/customer replacement is unsupported in v1; a linked new contract with reviewed transition is required.

A mistaken accepted change is superseded, not deleted. If no downstream issue consumed it, the replacement can restore prior rights. Otherwise the proposal names the necessary invoice/recognition corrections before authority is changed.

```text
contract100 units; issued40; live reservations10; increase cap120 -> remaining70
reduce cap45 while50 committed/reserved -> refuse or release the10 through its owner
draft issued concurrently with variation -> one wins, other must refresh
same accepted amendment replay -> same receipt and no new contract version
```

Completion includes amendment review, unchanged old invoice bytes, server-side issue revalidation and matching order/forecast readers. No contract-management framework or automatic revenue recognition is added.
