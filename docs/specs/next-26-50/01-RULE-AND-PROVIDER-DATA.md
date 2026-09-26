# Qualified inputs for the second wave

Reuse NEXT-02's rule and company profile ownership. Do not build another rule registry. The fields below define the exact missing inputs that a selected packet needs. They are not permission for an LLM to invent rates or execute arbitrary policy code.

Every release binds a finite named calculator/adapter, exact data/schema checksums, applicability predicates, evidence source, reviewed expected cases, unsupported cases and an activation review. A human selecting a release does not qualify missing source data. Retain old used releases as historical provenance even after new use is withdrawn.

| Family | Required qualified data | Packet |
|---|---|---|
| Extraction | Provider/model/parser identity, output schema, source-location contract, data-use permission, cancellation and cost limits | 26 |
| Identity resolution | Legal-identity schemes, evidence interpretation and supported entity/branch cases | 27 |
| Reminder channel | Message identity, provider idempotency lifetime, delivery-status meaning, read-back and cancellation semantics | 28 |
| Recurrence | Calendar anchor, end-of-month policy, service coverage, timezone and changed-cadence rules | 29 |
| Customer credit | Same-currency credit treatment, refund-liability roles and distinction from taxable advances | 30 |
| Deferral/accrual | Expense-recognition method, service-date basis, partial-period allocation, estimate/credit treatment | 31 |
| Loan | Actual agreement, day-count convention, rates, dated principal changes, repayment split and supported accounting treatment | 32 |
| Employee claim/trip | Employer obligation, payer/vehicle facts, rate unit, tax exemption, taxable excess and one payout route | 33-34 |
| Variable payroll | Actual employment schedule, agreement, supported sick/absence/holiday formulas, tax/contribution tables and entitlement valuation | 35 |
| Paid correction | Enforceable recovery or lawful future-pay adjustment, original paid/reporting facts and case-specific declaration treatment | 36 |
| VAT bridge | Exact return-box/whole-unit rounding, settlement-account roles, assessment identity and typed tax-account evidence | 37 |
| Cash method | Actual eligible accounting/VAT method, payment recognition, unpaid year-end population and supported credit rules | 38 |
| Stripe | Account/mode/API version, balance types, source links, fees, payout identities and independent balance controls | 39 |
| Foreign cash | Currency scales, acquisition/release policy, reporting-rate witnesses and supported cash/overdraft boundary | 40 |
| FX repair | Original event chronology, every affected calculation version, corrected rate and permissible correction dates | 41 |
| Asset reversal | Eligible asset/framework, recoverable-value evidence, without-impairment cap, residual and new future schedule | 42 |
| Classification | Explicit analytical policy, original data restrictions and revised report basis | 43 |
| SIE | Exact supported record grammar, encoding, source years, object mappings and omission rules | 44 |
| Cash flow | Reviewed cash perimeter and classification/FX/perimeter-change policy | 45 |
| Peppol | Exact UBL/XSD/Schematron/code lists plus chosen access-point routing/outcome specification | 46 |
| Signing | Actual document-signing protocol, visible consent, signed-data binding, certificate validation and purpose eligibility | 47 |
| Filing | Actual service specification, checksum algorithm, supported artifact, temporary upload, certifier/submission and authority receipts | 48 |
| Deadlines | Effective statutory rule, timezone/holiday policy, required fulfillment predicate and scope-bound receipt types | 49 |
| Agent context | Per-domain summary schema, complete-count/continuation semantics, access filtering and stable state revisions | 50 |

## Selection algorithm

```text
selectRelease(family, operationFacts, semanticDates):
    candidates = registered qualified releases that match family and exact applicability
    if none: MissingQualifiedRelease(family, affectedOperation)
    if more than one unresolved: AmbiguousRelease with exact candidates
    require finite calculator/adapter implementation supports this case
    require every mandatory fact has evidence and a current authorized review
    return exact release ID/hash, required inputs and dependency witness
```

Select by the operation's relevant dates, not `latest(today)`. Loan agreement terms, holiday formulas and advance-tax behavior cannot be inferred from adjacent supported profiles. The observed Peppol release title is not a substitute for its actual XSD/Schematron bytes. The BankID and Bolagsverket entry points did not establish all their exact machine contracts in this review.

## Provider interface without fictitious guarantees

```text
SelectedProviderProfile {
    actualApiVersion, operationSchemas, requiredCredentials,
    requestIdentity, idempotencyRetention?, readBackIdentity?,
    terminalOutcomeMeaning, cancellationMeaning,
    authenticatedObservationRules, unsupportedBranches
}
```

Absence of provider idempotency/read-back is represented as absent. Do not emulate it by merely reusing a local command key. A timeout around an external call stays unknown until the provider contract supports resolution. Local simulation demonstrates application state behavior, not authentic provider execution.

## Actual data and acceptance

The dossier uses artificial financial amounts and selected mathematical policies for examples. It provides no live company payroll, bank credentials or signing identity. Independently qualified statutory values and real source coverage remain necessary before a company uses affected operations. This does not block independent schema, compiler or state-machine implementation.
