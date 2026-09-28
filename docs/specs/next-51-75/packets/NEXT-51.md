# NEXT-51: Mixed-rate domestic sales and tax-inclusive prices

Priority: **P0 when applicable**. Lane: **COMMERCE**.

**New deliverable:** Extend the bounded domestic standard-rate invoice into explicitly qualified reduced-rate, exempt and mixed-rate documents with inclusive pricing. This is new sales scope, not a repair of the original credit or purchase packets.

**Existing owner to extend:** Existing commerce invoice draft/issue/credit operations, legal policy, VAT facts and retained renderers.

**Required contracts:** NEXT-02, NEXT-04, NEXT-15. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** PRY-47, PRY-51, PRY-55; canonical family COM-02/04, VAT-02. Domestic standard-rate owner gains new mixed/reduced/exempt profiles, not a second issue engine.

**Atomic result:** Journal + invoice/tax components + original credit capacities.

**Evidence:** R03, R04, X01 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Supported slice and records

Start with one book-currency domestic accrual document. Each line names a reviewed supply classification, rate/treatment release, price basis, unit/base quantity and tax date. Exemption is a distinct legal treatment, not a rate chosen as zero. Construction reverse charge and cross-border rules are separate profiles. Do not assert a current rate without its dated release [X01].

Retain `LineTaxWitness`, `DocumentAllowanceAllocation`, `DocumentRoundingEffect` and a versioned `InvoiceTaxSummary` inside the existing sealed invoice. They are owned components, not another invoice table. The original monetary amount, exact intermediates, rounding residual, account-role binding and mandatory notice decision travel through issue and credit.

## Calculation

```text
compileMixedInvoice(lines,documentAllowances,policy):
    validate unique local line IDs and supported exact quantity/price units
    for line:
        treatment=selectQualifiedTreatment(line.facts,line.taxDate)
        compute exact quantity * unitPrice / baseQuantity
        apply its explicit line discounts/charges once
        if priceBasis==exclusive:
            N=qualifiedPriceRound(exactLineNet)
            T=qualifiedTaxRound(N*rateNumerator/rateDenominator)
            G=N+T
        if priceBasis==inclusive:
            G=qualifiedPriceRound(exactLineGross)
            N=qualifiedInclusiveBackout(G,rate)
            T=G-N
            require inverse/tax checks mandated by this inclusive profile
        retain {N,T,G,treatment,sourceLineId,residuals}
    assign each document allowance/charge to eligible treatment buckets
    allocate integer residuals by the selected stable allocation rule
    recompute the affected bucket/line tax using the declared tax-rounding level
    net=sum(all final line net)
    tax=sum(final bucket tax)
    payableBeforeRounding=net+tax
    delta=qualifiedDocumentPayableRound(payableBeforeRounding)-payableBeforeRounding
    return exact totals and every allocation; do not deduct line discounts twice
```

For a selected `gross-preserving-inclusive-v1` policy with rate numerator `r` and denominator `d`, the original proposed backout is `N=roundRatio(G*d,d+r,selectedMode)` and `T=G-N`. The policy must explicitly permit this gross-preserving remainder treatment and its calculation level. Do not combine it with an incompatible independent net-tax rounding promise or change an imported source assertion to force agreement.

A total document discount cannot be allocated wholly to a preferred tax rate for convenience. An allowance with known source-line attribution follows that evidence. Unsupported mixed jurisdictions or conflicting rounded source assertions are review failures, not guesses.

## Financial execution and credit

The existing issue operation posts debit AR for the final payable, credits the exact revenue and output-tax components and posts the explicit payable-rounding difference to its reviewed role. For debit-positive notation, the rounding line is `-delta`. A negative amount uses the opposite sign. Omit zero journal lines while preserving zero/exempt semantic facts.

Issue, numbering, per-line tax facts, semantic document, commercial obligation and receipt share one transaction. Extend existing posting-purpose admission instead of using a manual-journal bypass. Relevant accounts and treatment releases are checked again before commit. Metadata for future Peppol rendering is the same retained tax summary, not another calculation.

Credit selection reuses original line amounts and exact remaining capacities. It must not apply today's rate or recompute the whole document from mutable defaults. A final original-line credit consumes its exact remaining net/tax components. Update VAT capture and invoice residual readers in the same implementation slice.

## User flow and acceptance

The draft presents line classification, exclusive/inclusive basis, discount allocation, rate source, notices and total. Human approval covers the exact result. API/MCP prepare uses the same compiler; ordinary agents cannot activate tax profiles or approve issue.

Synthetic vector: net 10000 at 1/4, net 20000 at 3/25 and net 5000 under a qualified exemption gives tax 2500+2400 and gross 39900. Inclusive gross12500 at 1/4 yields net10000/tax2500 under that selected profile. A rounding delta must reconcile the AR face amount without changing source tax.

Finish with one mixed-rate issue, a partial credit, a final credit, retained PDF/JSON totals, VAT contribution reconciliation and response-loss replay. A new enum of rate names alone does not complete the packet.
