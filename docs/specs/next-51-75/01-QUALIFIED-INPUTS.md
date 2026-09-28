# Qualified rules, external contracts and supported profiles

These requirements extend the existing company-profile, rule-release and provider owners. They do not create a second rules database, arbitrary policy-programming language or generic integration framework. A release is a finite typed input to a named implementation.

## Release manifest

```text
QualifiedRelease {
    id, family, semanticVersion, supportedCalculatorOrAdapter,
    effectiveDateScope, jurisdictionAndEntityScope,
    exactDataAndSchemaHashes, interpretationOfUnitsAndRounding,
    requiredCompanyAndTransactionFacts, supportedCases, refusedCases,
    sourceProvenance, reviewer, reviewReceipt,
    licenseOrUseConditions, independentExpectedCases
}
```

Preserve metadata that identifies a release separately from its optional family payload. Decode the shared outer release, validate its checksum and then select the correct family. A release with no selected payload is unsupported, not empty default data. Tax rates are not chosen by the most recent effective date alone; the actual supply, invoice, payment and reporting dates determine applicability.

Use the current qualified-profile admission owner. Source evidence, reviewed treatment, human approval and external mandate are separate authorities. A model may suggest a classification but cannot activate a missing profile or make a registry outage mean valid.

## Required inputs per packet

| Packet | Exact required policy/data | Explicit unsupported or unestablished boundary |
|---|---|---|
| 51 | Domestic supply classifications, effective rates, inclusive/exclusive pricing, line/document rounding, notices, allowance and credit rules | Every new rate/treatment requires actual applicable release; a zero rate is not an exemption decision |
| 52 | Service category and establishments, customer business/identifier evidence, place-of-supply rule, notices, reporting membership | No B2C or special-service fallback; unavailable customer verification remains unavailable |
| 53 | VAT territory, dispatch/arrival evidence, acquisition/supply status, tax basis and conversion rules | No triangle/call-off/margin or perpetual-stock inference |
| 54 | Actual customs declarations/revisions, importer identity, duties and already-included charges, import VAT and cost-allocation rules | Commercial purchase and customs taxable value are distinct; no duplicate expense recognition |
| 55 | Goods/services statement obligation, cadence, buyer/category keys, currency/filing units, original-error versus later-adjustment rules, selected export/submission format | Exact schema/provider package and company filing obligation still required |
| 56 | Identified future supply, deposit/advance distinction, payment/tax timing, rate changes, component application and refund treatment | An overpayment is not automatically a taxable advance; changed rates need an explicit compatible branch |
| 57 | Contract, actual payment, deduction evidence/date, advance carrying and final-application treatment | Foreign/nonmonetary advances and recovery/impairment require supported profiles, not payable revaluation by default |
| 58 | Service coverage and recognition method, contract changes, residual allocation, earned/unearned credit attribution | The first profile is explicitly time-based; milestones and variable consideration are not assumed |
| 59 | Contractual installment weights/dates, cash allocation order, legal amendment versus nonbinding payment promise | A forecast date does not edit due date; face amount remains the invoice owner's result |
| 60 | Discount entitlement, consideration/VAT correction, explicit fee/FX/currency rounding decisions and bounds | Small amount alone is never a qualification or rounding proof |
| 61 | Framework allowance policy, invoice-specific confirmed-loss evidence, tax relief and recovery treatment | General ageing allowance does not establish VAT relief or legal forgiveness |
| 62 | Contract/statutory authority, dated reference rate and spread, due-date/interest commencement, day count, fee entitlement and caps | No automatic fee, compounding, statutory number or consumer-credit product |
| 63 | Self-billing agreement/acceptance, external issuer numbering scope, applicable invoicing jurisdiction, tax notices and source responsibilities | Buyer-issued document is not automatically a purchase or a new self-issued invoice |
| 64 | Merchant account, payment method, exact checkout amount/currency, expiry/capture/idempotency/refund semantics and authenticated status | Browser return and local token expiry do not prove capture or remote cancellation |
| 65 | Authorized customer identity, exact resource scope, link/session expiry, revocation and retained artifact policy | No broad book query through guest credentials or unrevocable public bucket |
| 66 | Reviewed supplier commitments, quantity/value acceptance, invoice matching and accrued-service treatment | Purchase order alone is not AP, expense, tax or stock |
| 67 | Budget scope/period, qualified cost measure, exposure substitution, discretionary Stop/Warn rule and exception authority | A budget stop never deletes or refuses to record an already existing legal accounting event |
| 68 | Actual BAS reference release, use/license conditions, native account identity, effective rename/split/retire mapping and report/tax effects | Chart-name changes are not automatic tax/accounting policy |
| 69 | Selected workbook parser and file types, sheet/header/cell semantics, column maps, target schemas and private fields | First release need not support XLS/ODS. No macros, external workbook evaluation or blind numeric-ID coercion |
| 70 | Selected bank camt.053 message guide/XSD, booked balance types, parent/detail relation, direction/reversal rules and source identity | camt.052/054 and every bank variant need their own explicit profiles |
| 71 | Actual bank payment MIG/XSD, beneficiary/address/currency/calendar rules, message identity, status/rejection/cancellation proof | Valid XML is not bank acceptance; unknown outcome cannot release reservations |
| 72 | VAT submission API or official handoff profile, entity/period permissions, complete box serialization, replacement and signed-outcome meanings | Exact API machine contracts and credentials not acquired by this design |
| 73 | Selected AGI schema/period API, stable individual keys, permitted corrections, actual signing authority and private data retention | Registration permission is not signing permission; auxiliary facts can have distinct correction rules |
| 74 | INK2 main/annex edition, exact fiscal-year semantics, file/API channel, transfer and signature protocol, declaration outcome evidence | Income-tax filing and annual-report filing are separate; a transfer can still await signature |
| 75 | Official old/new methods, actual effective dates and permitted transition, old paid/recognized coverage, accounting/tax adjustment rules | Method change is not ordinary import or an app-level Boolean; unsupported direction remains unavailable |

## Selection and data preparation

```text
selectQualifiedCase(operation, facts, dates):
    candidates = active releases matching required family AND supported semantic case
    filter using the operation's relevant dates and actual entity/transaction facts
    if required fact absent: MissingEvidence with affected operations
    if no applicable qualified release: UnsupportedProfile with named case
    if more than one contradictory release: AmbiguousProfile, no default winner
    require exact data/schema checksums and finite implementation version available
    return typed witness with selected source facts and explicit refused branches
```

For algorithms that already exist in NEXT-01..50, consume that owner's selected calculation rather than porting a second copy. A partial-deduction purchase preserves source VAT and deductible VAT independently. A reporting integer cannot be compared as though it were minor units. A once-rounded cumulative target differs from summing individually rounded fragments.

The amount vectors in this package are synthetic. Fractions such as 1/4, 3/25 or 1/10 demonstrate exact mechanics and are not an activated statement of today's statutory rate for a real transaction.

## External profile contract

```text
ExternalProfile {
    environment, actualEndpointAndSchemaRelease,
    scopeAndRepresentativeRequirements,
    idempotencyKeySemanticsAndRetention?, readBackIdentity?,
    partialAcceptanceRules, authenticOutcomeValidation,
    signatureOrSubmissionCeremony, cancellationAndExpiryMeaning,
    operationalLimits, requiredExternalAcceptanceEvidence
}
```

Question marks mean genuinely optional provider capabilities. Do not invent them with a local UUID. The internal intent, provider request and real economic outcome each have identities. An actual credential store is required for live calls, but an offline parser/calculator does not wait for OAuth infrastructure it never uses.

No secrets, actual company facts, statutory table bundles, validation schemas or authentic external submission receipts are included in this package. The official sources identify what to qualify, not what was deployed. A useful file handoff can be delivered while connected access is pending, with the unsatisfied external outcome stated explicitly.
