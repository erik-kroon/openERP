# NEXT-63: Self-billed sales and buyer-issued invoice acceptance

Priority: **P2 when applicable**. Lane: **COMMERCE**.

**New deliverable:** Admit buyer-issued sales documents under an explicit self-billing agreement. This is not a supplier purchase or another use of the seller-generated invoice-number counter.

**Existing owner to extend:** Existing source occurrence, sales recognition/credit, party identity and document provenance owners.

**Required contracts:** NEXT-02, NEXT-15, NEXT-51. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** PRY-48; canonical family COM-02/04. Buyer-issued sale acceptance preserves external numbering and seller revenue ownership.

**Atomic result:** Original buyer-issued source accepted/adopted into seller revenue/tax owner.

**Evidence:** R03, X07 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Agreement and issuer identity

Retain `SelfBillingAgreementRevision` identifying the seller, authorized buyer/issuer, covered supplies, agreement dates, acceptance/rejection method and numbering responsibility. The applicable invoicing jurisdiction matters. Current rules distinguish invoice-number and issuer responsibilities; a foreign buyer's self-bill cannot be assumed to follow every domestic rule [X07].

`BuyerIssuedDocument` retains original bytes, issuer namespace/series/number, seller, supply period, amount/tax assertions and source occurrence. It is an incoming source about OUR sale, not a payable. Its economic key includes seller and authorized issuer's identity/namespace. An identical document received twice does not create two receivables.

## Preparation and acceptance

```text
prepareSelfBilledSale(original,agreement):
    require active agreement for this supply and actual issuer
    parse source assertions without inventing seller facts or numbering
    reconcile to retained contract/performance/quantity evidence
    validate mandatory content and tax treatment under the actual jurisdiction
    detect already recognized supply or seller-issued invoice
    if already recognized:
        prepare evidence linkage or a specific replacement/correction, not new revenue
    else:
        compile the existing sales journal/tax/AR semantics
    seal accepted commercial identity and exact source values
```

An app approval is not automatically acceptance under the commercial agreement. Record the applicable outward acceptance/objection event separately where required. No reply within a period is an acceptance condition only under an explicitly qualified agreement, not a universal timer rule.

When the buyer is the agreed numbering owner, OpenERP preserves their invoice identity and allocates only its normal accounting voucher number. It does not issue a second legal invoice under its own ordinary invoice series. A product requirement to produce a seller acknowledgment uses a different document kind, not a replacement invoice number.

## Atomic recognition and payment

The named acceptance transaction posts the native sales journal, records the source document as the issued commercial basis, creates AR, publishes tax facts and binds the supply occurrence once. It rechecks agreement/current customer/supply state, complete amounts and human authorization. Existing invoice, reporting and payment readers consume the same AR owner.

A buyer remittance statement can also contain fees, commissions and withholding. Separate the self-billed gross sale from independently qualified deductions and cash. A net receipt is not net revenue. Unsupported deductions leave an explicit remaining AR or settlement discrepancy rather than reducing sales silently.

## Correction and consumers

A replacement document with the same external number but changed bytes is not silently an update. Retain revisions/conflict evidence and apply the agreement's corrected-document identity. Credit notes reference original source components and use existing tax/AR capacity. If OpenERP has already issued a seller invoice for the supply, the operator must choose the lawful reconciliation relationship; the importer cannot simply discard one financially.

UI distinguishes buyer-issued original, seller approval, outward acknowledgment and actual payment. Statements show the real buyer-issued number. Reports, tax facts and SIE retain original reference and normal accounting voucher identity separately.

## Completion vector

A qualified buyer-issued sale100000+25000 recognizes AR125000 once. A remittance of122000 with an independently evidenced fee3000 settles AR125000 using bank122000 plus fee3000, not revenue122000. The same original delivered by email and import is one sale with two source occurrences.

Finish with original acceptance, duplicate delivery, an already seller-invoiced supply, corrected self-bill and partial remittance. No current self-billing legality is inferred solely from a check box or a printed phrase.
