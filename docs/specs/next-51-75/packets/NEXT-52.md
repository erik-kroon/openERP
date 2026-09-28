# NEXT-52: Cross-border B2B service sales and customer-status evidence

Priority: **P1 when applicable**. Lane: **COMMERCE**.

**New deliverable:** Add the sale-side general-rule EU and non-EU B2B service profiles. NEXT-05 covers service purchases, not these sales or their customer-status evidence.

**Existing owner to extend:** Existing sales issue/credit and party fact owners; dated jurisdiction treatment selection.

**Required contracts:** NEXT-02, NEXT-04, NEXT-15, NEXT-51. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-17: The selected sale is in foreign currency and needs the existing monetary-item representation.

**Crosswalk:** PRY-47, PRY-11; canonical family COM-02/04, VAT-02. Sale-side general-rule B2B services are distinct from NEXT-05 purchase-side services.

**Atomic result:** Journal + AR + zero/output tax and cross-border reporting facts.

**Evidence:** R03, R04, X02, X03 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Evidence and explicit exclusions

Retain a `ServicePlaceDecision` for each supply, with supplier/customer establishments, customer business status, service category, participating fixed establishment, supply date and qualified determination. A two-letter country or a valid-looking VAT number is not sufficient evidence of the place of supply.

A `TaxIdentifierVerification` retains provider, queried identifier, response time, exact result, correlation and raw evidence. Outcomes include valid, invalid, unavailable and conflicting. The observation supports the reviewed decision, not a timeless guarantee. The first slice excludes B2C digital services, land-related services, admissions, transport and every special rule not explicitly implemented. An unavailable registry service does not silently establish exemption; qualified alternative evidence is its own reviewed branch.

## Preparation

```text
prepareCrossBorderServiceSale(draft):
    capture exact party revisions, original contract and supply facts
    decision=qualifiedServicePlace(facts,datedRelease)
    require decision is one supported branch
    if EU_general_B2B:
        require customer identity/status and applicable destination established
        retain required customer identifier and reverse-charge notice
        choose statutory reporting treatment and ESL eligibility under this release
    if nonEU_general_B2B:
        retain business-status/place evidence and applicable notice
        ESL eligibility=false with explicit reason, not absent
    price and convert using existing exact invoice/FX owners
    compile AR, revenue and only taxes actually due under this selected treatment
    publish traceable VAT and sales-list candidates for this same supply
```

For the supported no-Swedish-output-tax branch, debit AR `N`, credit revenue `N` and retain a zero-output-tax semantic fact. No zero journal line is required. The buyer's reverse-charge accounting is not a seller journal. A foreign tax obligation cannot be forced into this branch; it needs its own applicable jurisdiction profile.

## Atomic effects and later evidence

The shared issue transaction commits the legal document, recognition, AR and reporting facts. Where foreign-currency sales are selected, the existing commerce FX owner retains original units, carrying value and the qualified conversion witness. NEXT-17 is consumed only to the extent its released contract covers that case; a payable-only implementation cannot be passed an AR item as a substitute. NEXT-55 consumes the reporting fact without recognizing revenue again.

If a customer verification changes after issue, preserve the original evidence and create an impact case. Re-evaluate the affected supply date and actual facts. Do not retroactively rewrite every invoice based on today's registry result. A needed adjustment is an explicit existing credit/reissue or treatment-correction operation with financial, customer-balance and reporting effects together.

The new preparation can be implemented while live registry credentials are absent using supplied reviewed evidence, but automatic registry verification remains an unqualified adapter until observed. Do not infer registry availability from a browser link.

## User and agent experience

Show the exact reason for no Swedish output tax, required notice, evidence freshness and whether an EU sales-list record is expected. A missing fact blocks the affected sale, not capture of the draft. Surface a dedicated unsupported-service explanation rather than suggesting another rate until validation passes.

Synthetic vector: a qualified EU B2B service of100000 book-minor produces AR100000, revenue100000 and output tax0, plus one EU-services reporting source. The equivalent qualified non-EU branch has no EU-services reporting source. A later receipt of100000 settles AR only. A source fact appearing through both the invoice and an import must not create a second sale.

Completion requires issue, credit/correction, receipt recovery and the exact report adapter. A printed reverse-charge notice without an applicable decision or financial/reporting integration is incomplete. Official reporting coverage is broader than merely possessing a customer VAT number [X02].
