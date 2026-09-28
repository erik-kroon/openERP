# NEXT-113: EU B2C destination VAT and Union OSS reporting

**Priority when applicable:** P2. **Owner lane:** TAX.

**New scope:** Add destination-tax consumer sales and a distinct Union OSS obligation. Earlier EU B2B sales and periodisk sammanställning do not cover this reporting family.

**Existing owner to extend:** Existing source/order intake, sale recognition, country/rate witnesses, FX reporting and external-obligation owners.

**Earlier contracts:** NEXT-51, NEXT-49. **This-wave dependencies:** None.

**Conditional:** NEXT-39: proceeds arrive through a processor; NEXT-53: a qualified goods supply rather than service is selected.

**Basis:** X03, R02, P51 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Bounded profile

Begin with a reviewed Swedish-established seller and one supported Union OSS supply family. Registration, scheme, customer status, place of supply and current rate must be actual facts. Exclude IOSS, non-Union scheme, marketplace deemed-supplier arrangements, unsupported establishments and small-business exemption interactions until separately qualified. Do not infer threshold eligibility from only the orders this system happens to have imported.

```text
OssSaleFact {
  originalSaleIdentity, consumerEvidence, placeOfSupplyWitness,
  consumptionCountry, supplyFamily, registrationRevision,
  originalCurrencyAmounts, originalTaxRate,
  bookCurrencyRecognitionWitness, reportCurrencyConversionWitness,
  correctionOfOriginalPeriod?, domesticDisclosureRole
}
OssReturnRevision {
  registration, scheme, period, completeCountryRateGroups,
  originalPeriodCorrections, reportEURAmounts, priorSubmittedRefs,
  contributionLineage, conversionRelease, sourceCoverage
}
```

Official Swedish OSS guidance distinguishes this declaration and euro payment from the ordinary VAT process [X03]. Do not route the foreign output tax into domestic output-tax boxes or the ordinary VAT settlement obligation. Any required local disclosure is supplied by its explicit qualified mapping.

## Source classification and financial recognition

```text
classifyConsumerSupply(source, profile):
  require final legal supplier and customer status known
  require enough noncontradictory country/location evidence under this supply rule
  determine eligible scheme and country/rate effective at actual tax point
  if uncertain, retain review case; never let a billing address alone override contradictions

compileOssSale(fact):
  derive net/tax/gross under original price and qualified destination rate
  convert book amounts under the normal recognition policy with conserving rounding
  debit AR or qualified payment clearing grossBook
  credit revenue netBook
  credit country/scheme output-tax liability taxBook
  retain original-currency amounts and tax basis for reporting
```

Order, payment and invoice records about the same sale remain one recognition identity. A payment processor is not automatically the seller or deemed supplier. Fees do not reduce the taxable sale without a qualified source treatment.

## Reporting currency and corrections

```text
prepareOssReturn(period):
  capture complete eligible facts and effective registration/period inventory
  group by scheme, consumption country, supported supply/rate category and original period
  translate using the qualified reporting-currency/date rule, not today's book carrying rate
  retain exact conversion and permitted rounding per reporting group
  compute positive and correcting components under the supported OSS schema
  reconcile reported liability target to booked country/scheme balances
```

A prior-period correction stays identified with its original reporting period. Do not simply overwrite an old accepted return or net every negative into current sales. The selected authority correction windows and procedure are explicit release data. A missing country group cannot become zero merely because fetching its source failed.

The euro reporting target can differ from book-currency liability due to reporting conversion and later payment FX. Store that bridge explicitly through the appropriate tax-liability/FX owner. Do not retroactively change revenue to force it to match. Purchases and deductible input VAT are not netted against OSS output liability by this packet.

## Submission and settlement

Create a distinct typed obligation/artifact and use a supported e-service handoff or qualified API if actually available. Do not invent a public OSS submission endpoint or reuse the domestic VAT API by changing a form name. The payment uses the actual OSS destination, reference and euro amount; an ordinary tax-account deposit is not its settlement evidence.

```text
example supplied gross120 EUR at synthetic20% -> net100/tax20
book rate11 SEK/EUR -> AR1320/revenue1100/OSS liability220 SEK
reported tax20 EUR; later actual20 EUR payment costs224 SEK
  -> liability220 + supported FXloss4 against cash224, not another revenue entry
registered period with verified zero activity -> required zero report if profile requires it
```

Completion requires the selected supply profile, complete country/rate lineage and honest reported/submitted/paid states. This is not a claim of all EU consumer-sales support.
