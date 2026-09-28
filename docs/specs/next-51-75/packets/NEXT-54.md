# NEXT-54: Customs imports, import VAT and landed-cost attribution

Priority: **P2 when applicable**. Lane: **TAX-COMMERCE**.

**New deliverable:** Add the customs assessment and import-tax basis alongside purchase recognition. A non-EU service purchase is not an imported-goods tax record.

**Existing owner to extend:** Existing supplier recognition, source intake, tax facts and supported expense/asset cost owner.

**Required contracts:** NEXT-02, NEXT-03, NEXT-04. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** PRY-55/56; canonical family COM-02, VAT-02. Customs import decisions and landed-cost attribution extend purchase recognition, not inventory custody.

**Atomic result:** Customs assessment delta + qualified cost/tax effects.

**Evidence:** R03, R04, X04 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Separate the documents and amounts

Retain `ImportEntryRevision` with customs reference and line identity, importer/legal entity, declaration/release decision, currency, customs value and authority-assessed quantities/charges. Link commercial invoice, freight, duty, agency fees and import evidence through explicit component relationships. A broker's invoice is not automatically the customs decision.

`ImportTaxBasis` holds the qualified customs value plus eligible duty/other charges and ancillary costs not already included. Skatteverket's 2026 guidance distinguishes this base from the supplier invoice and requires avoiding duplicate additions [X04]. The packet's first profile covers a reviewed Swedish import where the selected company is the relevant importer and its VAT reporting method is established.

## Cost and VAT compiler

```text
compileImportBasis(entry,linkedCharges,qualifiedRule):
    require unique external customs-line identity and version
    C=reviewed customsValueBookMinor
    additions=[]
    for charge:
        prove eligible kind and destination/time scope
        record includedInCustomsValue yes/no/unknown
        if unknown: block complete basis
        if no: include exactly the eligible component once
    B=C+sum(additions)
    O=qualifiedImportTax(B,rate)
    D=qualifiedDeduction(O,companyUse,evidence)
    return B,O,D with independent customs and purchase-cost witnesses
```

Financial purchase cost and customs tax base are not the same number. If commercial/freight/duty costs are already posted, adding them to `B` does not post those costs again. Their import attribution is nonfinancial provenance. An actual cost correction uses a separately reviewed cost delta through the existing expense/asset owner.

For the supported self-reported import VAT event, debit deductible input `D`, debit eligible non-deductible cost `O-D` and credit import-output tax `O`. If a different authority/payment regime applies, the profile supplies its different event semantics or the operation refuses. Do not create a Swedish AP for a self-assessed tax component just because it has an amount.

## Allocate landed cost without double recognition

A cost lot retained by the existing asset/expense owner may receive an allocated freight/duty component exactly once. Use reviewed weights such as value, mass or quantity with explicit units and stable residual allocation. Sum allocations to the charge's eligible amount. Unused amounts remain visible. A missing inventory owner blocks inventory capitalization rather than routing the balance to arbitrary expenses.

Customs reassessment appends a new effective decision. Compute a target-minus-effective delta per original customs component and qualified reporting rule. Preserve the original entry and earlier tax facts. A repeated amended XML or broker attachment is evidence of the same decision, not a new import.

## Execution, views and proof

The named import-tax application transaction rechecks current entry/charge relationships, posts the tax group, consumes its once-only external identity and writes tax facts/receipt together. Source attachment and actual foreign supplier payment remain existing separate owners. UI shows commercial cost, customs base, self-assessed output, deductible input and all included/excluded charges side by side.

Synthetic example: customs value100000, duty5000 and eligible freight2000 not already included yields B107000. At a synthetic 1/4 rate O26750. Full deduction gives input26750/output26750 and no extra commercial purchase. With already included freight, B105000, not107000.

Finish with an original entry, a reassessment, a previously posted broker cost and import-VAT return contribution. The accounting balances must agree independently of the customs-base arithmetic. Missing customs facts remain unknown rather than reusing a supplier exchange rate as an authority value.
