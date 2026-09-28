# NEXT-66: Purchase commitments and three-way invoice matching

Priority: **P2 when applicable**. Lane: **PROCUREMENT**.

**New deliverable:** Add purchase request, purchase order and receipt/acceptance evidence before supplier invoice recognition. Webshop sales-order intake and supplier invoice drafting are not purchase commitments.

**Existing owner to extend:** Existing supplier/party, source, purchase recognition and approval operations; no new inventory ledger.

**Required contracts:** NEXT-03. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-26: Invoice source matching uses extraction suggestions. NEXT-31: Accepted but unbilled service is recognized through an accrued-cost decision.

**Crosswalk:** Purchase/acceptance bridges in ERPNext review; canonical family COM-02, IMP, Cash readers. Commitment/acceptance records precede AP and do not implement a warehouse or a second accrual owner.

**Atomic result:** No accounting for purchase order alone; recognition/accrual only through existing owner.

**Evidence:** R04, R05 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Bounded procurement model

The first slice covers services and non-stock business purchases. `PurchaseRequestRevision` records business need, requester, supplier options and amount estimate. `PurchaseOrderRevision` freezes approved supplier, currency, line quantities/units, prices, taxes as assertions, delivery terms and commercial conditions. `AcceptanceEvent` records received quantity or accepted service scope with actual evidence. No object independently posts stock or cost.

A purchase order is a commercial commitment, not a supplier payable. Received-but-uninvoiced cost can require an accrual through NEXT-31 under a qualified recognition policy. Reject unsupported inventory accounting rather than create stock journal entries from quantity records.

## Three-way matching

```text
prepareInvoiceMatch(invoice,order,acceptances):
    capture original order revision and every relevant receipt/acceptance revision
    for invoice line:
        map to explicit order line and accepted scope
        require compatible supplier, currency, unit/base quantity and service identity
        compute unbilled accepted quantity/value from prior effective allocations
        compare price, quantity, charges and tax assertions independently
        classify exact_match / permitted_variance / review_needed / unsupported
    require every source line accounted for or deliberately unrelated
    seal matching manifest, differences, evidence and existing recognition plan
```

Tolerance is a procurement decision, not permission to guess tax or silently plug financial balances. An over-delivery or price change requires a reviewed commercial decision with its own limit and reason. Tax deductibility stays with the purchase owner. A zero invoice variance is not evidence that service was actually received.

## Atomic invoice consumption

The actual purchase transaction consumes order/acceptance billing capacities, recognizes the invoice or resolves its existing accrual, creates AP/tax facts and writes one receipt. Recheck all capacities under the shared lock protocol. A second invoice cannot claim an already fully billed acceptance. An unrelated invoice must not be blocked merely because a supplier also has an open order.

Acceptance does not automatically post an expense. Where policy calls for accrued received service, invoke the named accrual owner separately with explicit evidence/approval or combine it within an approved aggregate. At invoicing, release that accrual rather than expense the same accepted service twice.

An order amendment preserves already received/billed quantities and changes only remaining commercial scope. Cancelling an unfilled order releases its remaining commitment but does not reverse a real receipt or cancel an accepted invoice. A supplier credit may reopen billing capacity only when a supported decision actually represents returned/replaced goods/service; a price credit does not recreate receipt quantity automatically.

## Interfaces and controls

Operator UI goes request, approval, order, acceptance, invoice review and receipt. Ordinary agents may gather quotes, suggest mappings and prepare decisions. They cannot authorize procurement spend or confirm actual receipt by inference. Expose all variances before posting, with original order and evidence side by side.

Cash represents a purchase commitment until an actual invoice/payment replaces the same exact occurrence. It cannot sum the order, accrued liability and supplier invoice as three future payments. NEXT-67 adds optional budget consequences, but this packet can be delivered without budget functionality.

Synthetic order10 units at1000: acceptance6 units, invoice4 units consumes4 of the accepted6. Two remain accepted/unbilled and4 remain unreceived. A second invoice3 units fails against the accepted remaining2 unless additional receipt or explicit supported exception is established. No quantity event alone creates inventory value.

Completion requires request-to-invoice, partial receipt/billing, an accrued-service resolution, change/cancel and duplicate supplier invoice cases through native operations. This is optional commercial scope, not a required expansion into a warehouse ERP.
