# NEXT-53: Intra-EU goods acquisition and supply accounting

Priority: **P2 when applicable**. Lane: **TAX-COMMERCE**.

**New deliverable:** Add goods-specific intra-EU acquisition and sale profiles, including movement evidence. Neither service-purchase NEXT-05 nor service-sale NEXT-52 establishes goods treatment.

**Existing owner to extend:** Purchase/sales recognition and reporting fact owners, with existing asset/expense destinations.

**Required contracts:** NEXT-02, NEXT-03, NEXT-04, NEXT-15, NEXT-51. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** PRY-47, PRY-55/56; canonical family COM-02/04, VAT-02. Goods movement/acquisition/supply treatment is not inferred from the service profile.

**Atomic result:** Journal + original goods recognition + tax/movement lineage.

**Evidence:** R03, R04, X01, X02 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Bounded goods workflow

Create a reviewed `GoodsMovementDecision` linking invoice lines, dispatch/arrival evidence, origin/destination VAT territory, seller/buyer identity, transfer dates and one supported transaction classification. Customs territory, EU membership and EU VAT territory are not interchangeable labels. The initial slice covers a direct two-party movement with the reporting company as buyer or seller. Triangulation, call-off stock, installation supplies, margin schemes and own-goods transfers remain explicit unsupported profiles.

This packet does not implement perpetual inventory. Purchases must name an existing supported expense or asset destination. Quantity evidence can exist without a warehouse register; stock accounting is a separate prerequisite when it is required for the selected company.

## Purchase calculation

```text
compileAcquisition(invoice,movement,release):
    require complete movement and qualified acquisition decision
    B=qualified book-currency purchase cost
    BT=qualified VAT acquisition base using its own date/conversion witness
    O=qualifiedTax(BT,rate)
    D=qualifiedDeductiblePortion(O,reviewedUse)
    debit expense_or_asset B+(O-D)
    debit input_tax D
    credit supplier_payable B
    credit acquisition_output_tax O
    return financial and reporting components with separate B/BT lineage
```

A supplier's incorrectly charged foreign VAT cannot automatically become Swedish deductible VAT. Retain it as a source discrepancy or supported gross cost/claim treatment after review. No assumption that the acquisition output tax equals deductible input tax is permitted.

## Sale calculation and reporting

The supported qualifying intra-EU supply posts AR and revenue with no Swedish output VAT only after its own eligibility and movement decision. Otherwise refuse or prepare an explicitly reviewed alternative. Tax identifier verification and shipment documents are retained at issue. They do not replace proof of actual dispatch under the selected policy.

Both branches publish qualified reporting facts linked to the original supply, with acquisition/supply categories and original currency conversion. NEXT-55 consumes qualifying sale facts. A purchase never enters the seller's EU-sales list merely because its counterparty is in the EU.

## Transactions and later movement changes

Execute through existing purchase/sales internal writers on one supplied transaction: journal, obligation, tax facts, movement relationship, source identity and receipt. Where financial recognition precedes complete tax evidence, use only an explicitly supported pending-tax workflow with tracked liabilities and a blocking report condition. Do not label incomplete proof as zero-rated.

A returned shipment is not only a financial credit. Retain the return relationship and exact original line capacity. A credit reduces the original financial and reporting components under its applicable date rule. A source error is distinct from a later price change, a distinction NEXT-55 must receive. Never delete original shipment evidence or rerun all recognition when an attachment arrives.

## Completion and examples

UI shows logistics evidence separately from tax treatment and payment status. API readers expose source document, movement, selected role/rate witnesses and unresolved evidence. Cross-border stock use outside this slice is visible to Book Zero readiness.

Synthetic acquisition: B100000, BT100000, O25000 and D12500 produces debit cost112500, debit input12500, credit AP100000 and credit output25000. With D25000, cost remains100000. The later supplier payment creates no new acquisition VAT.

Finish with one acquisition, one qualifying supply, partial return/credit, VAT reconciliation and a sales-list source. Include changed movement evidence after approval, an unsupported triangular case and duplicate invoice/movement deliveries. Do not count two observations as two physical movements without an explicit occurrence distinction.
