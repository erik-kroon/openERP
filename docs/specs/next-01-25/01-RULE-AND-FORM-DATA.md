# Qualified data inputs, not hidden algorithms

Edition v2: the packet algorithms are specified as application-owned operations. This carries forward the supplied rule-data requirements without a fresh legal or provider verification. Statutory tables, field codes, taxonomy packages and actual company facts must enter as explicit versioned inputs. This package does not invent those bytes or certify the example rates as current law.

## Release contract

```text
QualifiedReleaseManifest {
  releaseId, family, jurisdiction,
  officialSourceLocations, fetchedAt,
  exactFileHashes, parserVersion, calculationCodeVersion,
  effectiveDatePredicate, supportedCaseMatrix,
  formulaOrMappingData, independentExpectedCases,
  reviewRecord, status: staged|qualified|withdrawn
}

qualifyRelease(candidate, independentReview):
    verify source files and hashes against retained originals
    parse strictly; require complete supported table/field/taxonomy membership
    check ranges nonoverlapping, required branches covered and units explicit
    validate independent expected cases and semantic counterexamples
    require reviewer approves exact candidate digest and applicability
    freeze qualified release; never update its bytes in place

loadReleaseForOperation(operation, facts, dates):
    select by exact family and applicability predicate
    require exactly one qualified supported release
    if missing/ambiguous: return typed missing-release blocker
    return immutable data + code checksum for the packet's deterministic calculator
```

This is a deployment/review mechanism for existing finite domain calculators, not a general financial scripting language. Data may define a finite table, tiers or report-field mapping. It cannot write SQL, grant authority or execute arbitrary supplied code.

## Required inputs by family

| Family | Required data | Deterministic use |
| --- | --- | --- |
| Company admission | Legal identity, fiscal interval, accounting method, dated registrations, framework applicability and reviewed account roles | Resolve exact operation/date witness in NEXT-02 |
| Domestic purchase/VAT | Supply/tax-point predicates, rates, deduction rules, source-tax tolerance and line/box rounding | NEXT-03/04 calculate and publish source-linked tax components |
| Cross-border services | General-rule eligibility, exception assessment, tax-point conversion, reverse-charge boxes and credit rules | NEXT-05 keeps tax base distinct from carrying/settlement value |
| FX | Directional exact rate observations and policy dates | NEXT-17/18 consume commerce paired balances and reporting-rate witnesses |
| Payroll withholding | Official year/frequency/table/column rows and formulas, or valid individual withholding decision | NEXT-20 selects one bracket/formula, never nearest available row or universal percentage |
| Employer liabilities | Date/age/status eligibility, monthly/annual bands, rate tiers and aggregation rounding | NEXT-20 evaluates cumulative liability and exact incremental share |
| AGI | Exact XSD bundle, namespaces, field meanings, person/period identity and replacement/removal rules | NEXT-21 renders and validates the paid/provided population |
| Corporate tax | Tax-year rates/rounding, supported adjustments, loss eligibility and form maps | NEXT-22 calculates pre-close tax and reconciles after-tax form starting values |
| SRU | Exact INFO/BLANKETTER grammar, encodings, form identifiers, field codes/types and limits | NEXT-22 serializes known fields and rejects unsupported output |
| SIE4E | Qualified version/record grammar, encoding, balance/object/period semantics | NEXT-11 emits complete selected-book data without changing existing4I |
| K2/iXBRL | Framework applicability, required disclosures, concept mapping, taxonomy/entry points and presentation/signature rules | NEXT-24 freezes semantic content, renders and checks exact facts |
| Payment cancellation | Provider-specific finality/authentication and no-execution semantics | NEXT-08 releases only instruction capacity supported by actual proof |

## Date selection

```text
posting eligibility              -> actual accounting date and fiscal period
supplier/customer legal identity  -> event/issuance identity evidence required by operation
VAT registration/treatment        -> qualified supply/tax-point and method selection
payroll calculation               -> earnings inputs plus planned payment basis
AGI                               -> actual paid/provided reporting basis
statement accounting framework    -> fiscal-year applicability including published exceptions
FX recognition/settlement/report  -> three separately named rate/evidence policies
```

Do not replace these selectors with `latestRelease(today)`. A changed rule creates a new release and impact analysis; it does not rewrite old approved plans or filed bytes.

## External-version observation limits

The original dossier recorded checks of official Plaid, SIE, BFN and Skatteverket material for the narrow facts cited in SOURCES.md. Those are inherited source observations, not new checks in this rewrite. No complete statutory table/XSD/SRU/taxonomy bundle was downloaded and qualified here. The AGI portal surfaced differing1.1.18.x labels across search/open results, so no exact production schema version is asserted by this package. The implementation must pin the actual selected schema bytes, not a page title.

No model invents a tax table when a release is missing. A missing company registration does not stop source retention. A missing mandatory qualified field mapping does prevent claiming a finished statutory artifact. These boundaries are outputs of the specified algorithms, not unanswered choices about the architecture.

## Application persistence of qualification

Qualification and book activation are named Effect operations. They decode retained releases, apply the finite checks above and persist the review/release identity through the caller's transaction. No SQL function selects tax rates or declares a rule applicable. Database records enforce immutable identity, scope and allowed storage states. The algorithm/rule version is part of each prepared plan and artifact, independently of the database schema version.
