# NEXT-05: General-rule cross-border service purchases

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/purchasing/service-purchases.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/purchasing/service-purchases.ts` or the existing equivalent owner |
| Pure calculation | Service-place/tax treatment and separate recognition/tax-point conversion |
| Atomic scope | Journal, original/book payable or owner liability and tax facts share one tx. |
| Prerequisites | NEXT-03, NEXT-04 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-03/04. Unpaid foreign-denominated obligations additionally wait for NEXT-17 and WIP-FX02-P1. No replacement FX register.

## Classification contract

```text
ServicePurchaseFacts {
  invoiceLegalSupplier, supplierCountry, supplierEstablishment,
  customerTaxablePersonEvidence, receivingEstablishment,
  serviceKind, specialPlaceOfSupplyExceptionAssessment,
  sourceNetAndAnyForeignTax, invoiceCurrency, suppliedOn, receivedOn,
  taxPointEvidence, businessUse, deductionFraction, creditOf?
}
classifyGeneralService(facts, release):
    require known actual invoicing entity; a brand name is insufficient
    require recipient and place-of-supply conditions satisfied
    require serviceKind in release.supportedGeneralRuleServices
    require no applicable special exception, else UnsupportedProfile
    require source tax is qualified for treatment
    if foreign tax is nonzero in this initial reverse-charge profile:
        retain the entire invoice gross and foreign tax
        fail UnsupportedForeignTaxOnSourceInvoice
        # A separate qualified treatment may later handle it. Never drop it from liability
        # or treat it as Swedish input VAT just to continue.
    jurisdictionClass = EU_OTHER or NON_EU from facts effective at tax point
    return explicit treatment with tax rate, basis box21 or22 and output box30/31/32
```

The general-rule box mappings and conditional deduction follow Skatteverket's EU/non-EU service guidance [X05/X06]. This does not cover goods, imported goods, every digital-service arrangement or special place-of-supply exceptions.

## Three different values

```text
original liability in supplier currency
book carrying value at recognition
SEK reverse-charge tax base at the qualified tax point
```

The latter two may differ because their policies/dates can differ. Never overwrite one with the other to balance an entry. If the first implementation supports only coincident dates/rate policies, require that equality explicitly and refuse other cases until the qualified profile handles them.

## Compiler

```text
compileCrossBorderService(basis, facts):
    treatment = classifyGeneralService(facts, qualifiedRelease)
    accountingValue = convert original net by accounting-recognition policy
    taxBase = convert original taxable base by qualified tax-point policy
    outputTax = roundRational(taxBase*treatment.rate.n, treatment.rate.d, taxRounding)
    deductible = roundRational(outputTax*deductionFraction.n, deductionFraction.d,
                               deductionRounding)
    nonDeductible = outputTax-deductible
    Journal.addSigned(serviceCostRole, accountingValue + nonDeductible)
    Journal.addSigned(reverseChargeInputRole, +deductible)
    Journal.addSigned(reverseChargeOutputRole, -outputTax)
    Journal.addSigned(fundingOrPayableRole, -accountingValue)
    finish()
    taxFact = {
      signedBase: taxBase,
      basisBox: treatment EU ?21:22,
      outputTaxBox: treatment.outputBox,
      outputTax, deductibleInputBox48: deductible,
      originalSourceAmount, accountingRateWitness, taxRateWitness
    }
    if unpaid foreign obligation:
        append commerce monetary item using original units and accountingValue
    return native purchase aggregate + taxFact
```

Already-paid recognition needs an explicit selection: either recognize through AP and a separately linked settlement, or recognize against an existing evidenced cash/owner payment through the appropriate owner. Do not use the same bank debit as both new cash movement and adoption of an existing cash posting.

For later credit, consume the original line's source net/tax capacities and the qualified credit-period policy. A credit's monetary conversion and tax correction may have different prescribed bases. Where the release requires original-tax-basis reversal, release its retained tax components proportionately with exact final residuals. Where another policy applies, use that explicit release. Never infer a generic current-FX reversal of old VAT.

```text
executeServicePurchase(command):
    return withAdmittedPrincipal(access, scope, purchasePermission, (tx, principal) =>
        lock book; replay exact command first
        load exact sealed service-purchase plan
        load current source, recognition, rate and qualified tax witnesses in batches
        require treatment supported and economic purchase not already recognized
        ServicePurchaseDomain.assertApprovedConservation(plan, current)
        approval = validate exact current approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal)
        if foreign payable:
            obligation = CommerceFxApp.recordRecognitionWithinTransaction(tx,
                plan.originalUnits, plan.bookCarrying, journal, plan.recognitionWitness)
        else:
            obligation = selected existing payable/owner application writer(tx, plan, journal)
        taxFacts = TaxFactApp.recordRecognitionWithinTransaction(tx, plan.taxFacts, journal)
        RecognitionDb.insertOwnedIdentity(tx, plan.economicKey, journal, obligation, taxFacts)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journal.ids, obligation, taxFacts}, approval)
    )
```

## Vectors, all illustrative minor units

```text
accountingValue=100000, taxBase=100000, rate1/4, deduction1:
    cost100000 + input25000 - output25000 - payable100000 == 0
same with deduction1/2:
    cost112500 + input12500 - output25000 - payable100000 == 0
accountingValue=101000, taxBase=100000, full deduction:
    cost101000 + input25000 - output25000 - payable101000 == 0
later foreign settlement changes carrying/FX but changes no original tax fact
```

Use exact conversion witnesses from C1 and existing rate owners. Reject unknown FX source, scheme or tax point rather than defaulting rate to1.
