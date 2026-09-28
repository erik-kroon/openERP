# Qualified rule, company and provider inputs

Reuse the existing finite rule-release and company-activation owners. Do not build another general rules engine. The pseudocode solves data flow, arithmetic boundaries and state transitions. It does not fabricate the public tables, private agreements or actual business events that make a specific profile valid.

A release records named calculator/adapter versions, exact source/schema checksums, applicability, mandatory inputs, supported/unsupported cases, independent expected examples and review. Activation selects that immutable release for an actual company/date/operation. It does not turn a returned model suggestion into legal truth.

| Packet family | Required additional input |
|---|---|
| 101-102 | Client-granted firm scope, staff assignment, request purpose and permitted recipient evidence |
| 103-105 | Account support templates, independent balance evidence, actual allocation drivers, project scope and explicitly included/excluded costs |
| 106 | Real service-retainer contract, nontransferable unit definitions, original consideration/tax and qualified revenue/refund terms |
| 107-108 | Applicable provision-recognition/measurement rule, actual obligation, complete uncovered exposure and independently reviewed estimate basis |
| 109 | Insurance rights, actual covered loss, sufficient recovery recognition evidence and approved repair/payment relationships |
| 110 | Executed loan modification, exact released obligations, permissible measurement and existing uncertain instructions |
| 111 | Selected common-cost allocation method, source-tax ceiling, direct-cost exclusions, final driver/rounding and correction periods |
| 112 | Actual service/property/buyer qualifications, supplier tax presentation and current correct report mappings |
| 113 | Effective OSS registration and supply family, consumer/place evidence, destination rates, EUR reporting conversion and corrections |
| 114 | Refund-country eligibility/codes, original foreign tax, claim period/attachments and recoverable entitlement measurement |
| 115-116 | Actual travel/meal/vehicle facts, dated tables, employee payments and cash/noncash reporting rules |
| 117 | Actual reporter duty, person/instrument class, paid/available dates, withholding and exact year-specific electronic schema |
| 118 | Signed prospective salary exchange, actual pension agreement, contribution/SLP roles and benefit/absence effects |
| 119 | Actual share resolution/subscription/payment/registration evidence and qualified interim capital/premium classifications |
| 120 | Qualified full-year tax profile, actual-to-date and labelled scenario inputs, genuine preliminary-tax decisions |
| 121 | Explicit human-activated scope, independently verified source pattern, shared limits and released authority/lock contract |
| 122 | Complete cash perimeter, true reservations/holds, permitted dates/partial options and reviewed objective/constraint policy |
| 123 | Actual bank Autogiro agreement, payer mandate evidence, precise notice/file/status/cancellation/return contracts |
| 124 | Independent real-account identity and complete overlap/continuity evidence for both providers |
| 125 | Actual Stripe account/mode/charge/refundability, exact refund state/financial discharge mapping and idempotency/read-back limits |

## Deterministic selection

```text
resolveQualifiedInputs(family, company, caseFacts, semanticDates):
  select immutable releases whose exact applicability predicates match
  none -> MissingQualifiedRelease(family)
  ambiguous -> UnresolvedReleaseSelection
  required fact absent/contradictory -> specific MissingFact/Conflict
  supported profile not implemented -> UnsupportedCase, not fallback to another regime
  return exact release/fact identities and dependency witness
```

No statutory threshold, daily allowance, net/gross treatment or filing field is picked from memory in an activated implementation. Synthetic packet examples intentionally use illustrative amounts. When a specialist family is inapplicable, record the actual fact and scope rather than invoking every new packet before a company can close.

## External guarantees

Provider idempotency retention, exact cancellation support, error meaning, read-back identity and accounting evidence are verified per real adapter. A local command key is not a provider guarantee. Direct-debit marketing about due dates is not final cash evidence. An OSS or tax web-service page does not establish a public programmable endpoint.

A failed schema validation or missing actual outcome remains an explicit gate. Useful local preview/artifact generation can continue independently without calling the external path complete. No captured account, token, signature or invoice in this dossier authorizes a real action.
