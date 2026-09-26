# Sources and evidence boundaries

Repository: `erik-kroon/openERP`, pinned commit `5ac3433e3e75ef7fc0229cbe00107003b63aa32d`. Review date: 26 September 2026. This is a targeted source and requirement review, not an every-file audit. No repository implementation, database suite or external integration was executed.

The new algorithms, ownership choices and packet ordering are design proposals. The cited source supports the observed starting point or requirement. A missing operation in an inspected file is not proof that no other branch or uncommitted workspace implements it. Agents must reconcile the actual checkout before claiming a packet.

## Repository evidence

### R01: GitHub main branch

Branch resolved to 5ac3433e3e75ef7fc0229cbe00107003b63aa32d; capture is a pinned review, not a live-state promise.

Source: https://api.github.com/repos/erik-kroon/openERP/branches/main

### R02: docs/plans/application-owned-accounting.md

Requested lines 1-250 and 250-480. Selected returned plan/status and failure matrix: application-owned replacement, clean baseline, incomplete domain ports and proof. Not all runtime paths were executed or reviewed.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/docs/plans/application-owned-accounting.md

### R03: docs/plans/capability-backlog.md

Coverage index plus supplemental sections; requested full content and lines 140-310. Collections, retagging, employee expenses, recurring invoices, provider exchanges, rule/deadline impacts and agent context are requirements, not completion claims.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/docs/plans/capability-backlog.md

### R04: apps/api/src/application/commerce/collections.ts

Inspected returned code for disputes/actions/history/worklist and reminder preparation. sendAuthorized is false in the recorded action. The full application delivery graph was not exercised.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/apps/api/src/application/commerce/collections.ts

### R05: apps/api/src/application/commerce/crm-master.ts

Directory/export and contact/alias/registry-provenance annotations. A complete reviewed identity-resolution lifecycle was not established by this module review.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/apps/api/src/application/commerce/crm-master.ts

### R06: apps/api/src/application/closing/deadlines.ts

Manual obligation revision, activity, feed and revocation operations. record_outcome accepts a bounded reference string in the inspected operation; it does not itself validate a typed authority receipt.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/apps/api/src/application/closing/deadlines.ts

### R07: apps/api/src/application/capabilities/commerce-invoices.ts

Lines 1-130 map existing purchase/invoice/party operations into shared capability dispatch. Used as path/ownership evidence, not functional acceptance.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/apps/api/src/application/capabilities/commerce-invoices.ts

### R08: apps/api/src/application/purchases/inbox.ts

Inbox registration, recorded extraction attempts and reviewed draft binding through createSupplierInvoiceDraftInTransaction. A provider extraction job was not established by the inspected code.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/apps/api/src/application/purchases/inbox.ts

### R09: docs/plans/04-invoices-payments-registers.md

Lines 1-135: commercial versus financial state, accrual/cash method, year-end unpaid invoices, advances/overpayments, source identities, payment capacities and reports. Historical migration prose is not a fresh runtime observation.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/docs/plans/04-invoices-payments-registers.md

### R10: docs/plans/05-vat-payroll-assets-fx.md

Requested lines 1-190: tax/payroll/asset/FX requirements and selected historical context. Automatic FX reversal wording in old prose is superseded by R11 incremental valuation.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/docs/plans/05-vat-payroll-assets-fx.md

### R11: docs/adr/0008-financial-fx-vat-impairment.md

Lines 1-150 requested. Adopted paired FX carrying, VAT role separation and impairment equations, explicitly reconciled with application ownership under ADR 0010.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/docs/adr/0008-financial-fx-vat-impairment.md

### R12: apps/api/src/application/capabilities/subledger-owners.ts

Lines 1-100 identify existing schedule, control and owner-register operations. Used for paths, not proof of supported new asset states.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/apps/api/src/application/capabilities/subledger-owners.ts

### R13: Application/commerce directory inventories

Connector directory/tree results establish present source paths. A filename is not evidence that every requested scenario is implemented.

Source: https://github.com/erik-kroon/openERP/tree/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/apps/api/src/application

### R14: Supplied NEXT-01..25 application-owned v2 dossier

Input artifact openerp-next-25-effect.zip plus its shared contract and solution index. Used to preserve task identity, exclusions and distinct feature scope. It remains proposed pseudocode, not deployed source.

## Prior-wave identifiers

The following are the supplied application-owned v2 designs, not inferred source functionality. A dependency on one means a released contract/implementation is needed, not that the earlier artifact proves it exists. `Pnn` refers to packet `NEXT-nn` in `openerp-next-25-effect.zip`.

- P01: NEXT-01, Owner-aware case review.
- P02: NEXT-02, Capability-specific company admission.
- P03: NEXT-03, Domestic purchasing with owned tax recognition.
- P04: NEXT-04, Actual domestic VAT return and controls.
- P05: NEXT-05, General-rule cross-border service purchases.
- P06: NEXT-06, Owner-paid expenses, reimbursement and funding.
- P07: NEXT-07, Supplier paid credits and refunds.
- P08: NEXT-08, Payment instruction resolution and replacement.
- P09: NEXT-09, Complete Plaid sync windows.
- P10: NEXT-10, Provider revisions to reviewed bank observations.
- P11: NEXT-11, Separate complete-book SIE4E export.
- P12: NEXT-12, Historical open-item adoption.
- P13: NEXT-13, Semantic P&L and balance-sheet snapshots.
- P14: NEXT-14, Original dimension assignments.
- P15: NEXT-15, Legal customer credit notes.
- P16: NEXT-16, Evidence-aware period preparation.
- P17: NEXT-17, Payable FX and explicit fees.
- P18: NEXT-18, Incremental open-item FX remeasurement.
- P19: NEXT-19, Disposal with proceeds.
- P20: NEXT-20, Frozen regular-payroll calculation.
- P21: NEXT-21, Payroll posting, payslip and AGI artifact.
- P22: NEXT-22, Pre-close tax bridge and INK2/SRU.
- P23: NEXT-23, Financial close and single-count carry-forward.
- P24: NEXT-24, K2 annual-report semantic model and iXBRL.
- P25: NEXT-25, Fixed-revision company rehearsal and restore.

## Primary external sources

Legal and provider facts below are deliberately narrow. Formulas and workflows elsewhere in the dossier are proposed implementations conditional on qualified profiles. We did not download every statutory table, XSD, taxonomy or provider contract.

### X01: Stripe Balance Transaction object

Gross, fee and net in smallest currency units, with net=amount-fee. Source object/type identity needs an explicit accounting mapping.

**Observation limit:** Official page read; no provider access or certified adapter.

Source: https://docs.stripe.com/api/balance_transactions/object

### X02: Stripe Balance Transaction list

The payout filter is for automatic Stripe payouts. Manual payouts cannot assume that membership query.

**Observation limit:** Official page read.

Source: https://docs.stripe.com/api/balance_transactions/list

### X03: Skatteverket cash bookkeeping guidance

Cash bookkeeping recognizes during-year payments and unpaid invoices at year-end. Qualified tax timing and method selection are still required for each supported case.

**Observation limit:** Official page opened; no complete VAT method release qualified.

Source: https://www.skatteverket.se/foretag/drivaforetag/startaochregistrera/fordigsomvillstartaforetag.4.6e8a1495181dad540842251.html

### X04: Skatteverket employer declaration corrections

Future-pay adjustment and gross recovery differ. Gross recovery can lead to original-period compensation correction when claimed; prior withholding normally stays. Replacements preserve item specification identity. Tax-account changes depend on authority reassessment.

**Observation limit:** Official page read, notably correction and recovery sections. No general recovery/offset legal entitlement is inferred.

Source: https://www.skatteverket.se/foretag/arbetsgivare/lamnaarbetsgivardeklaration/rattaenarbetsgivardeklaration.4.2cf1b5cd163796a5c8b6698.html

### X05: Peppol BIS Billing 3.0

Index identifies May 2026 release; BIS text supplies structured invoice/credit and monetary relationships.

**Observation limit:** Official index and BIS page opened. Exact XSD/Schematron/code-list bundles were not downloaded or qualified.

Source: https://docs.peppol.eu/poacc/billing/3.0/

Related official source: https://docs.peppol.eu/poacc/billing/3.0/bis/

### X06: BankID autostart and signing entry point

App return is not completion evidence; collect is needed. Access requires appropriate provider arrangements/certificates.

**Observation limit:** Autostart/support text available; signing API page returned minimal client-rendered text. No exact signing API schema or signature-verifier qualification is claimed.

Source: https://developers.bankid.com/getting-started/autostart

Related official source: https://developers.bankid.com/api-references/auth--sign/sign

Related official source: https://developers.bankid.com/support

### X07: Bolagsverket digital annual-report workflow

Original signing, company adoption, upload of a faithful copy, authority certification/submission and receipt/registration are distinct. A general representative cannot simply replace the eligible certifier.

**Observation limit:** Official search-rendered pages provided relevant text. Direct opening returned a minimal/challenge response. No actual filing performed.

Source: https://bolagsverket.se/sjalvservice/etjanster/lamnainarsredovisningendigitalt.1663.html

Related official source: https://bolagsverket.se/sjalvservice/etjanster/lamnainarsredovisningendigitalt/saharlamnarduinarsredovisningendigitalt.1667.html

Related official source: https://bolagsverket.se/sjalvservice/etjanster/lamnainarsredovisningendigitalt/vanligafragoromattlamnainarsredovisningendigitalt.1671.html

Related official source: https://bolagsverket.se/sjalvservice/etjanster/lamnainarsredovisningendigitalt/forutsattningarforattlamnainarsredovisningendigitalt.1665.html

### X08: Bolagsverket current service specifications entry point

Provides versioned filing, information, event and checksum services. The packet requires the actual selected service contracts rather than invented routes/statuses.

**Observation limit:** Official search result inspected; exact linked OpenAPI/specification bundles not acquired or exercised.

Source: https://bolagsverket.se/apierochoppnadata/lamnaforetagsinformation/digitalinlamningavarsredovisningochrevisionsberattelse/gallandeservicespecifikationerfordigitalinlamningavarsredovisning.5938.html

### X09: SIE Group format family

Balance/transaction export and voucher transfer are different format purposes. Exact year/dimension/omission grammar must be qualified against the chosen specification.

**Observation limit:** Official format page opened; this work does not certify a new parser or exporter.

Source: https://sie.se/format/

## Not established by this review

Current company registrations, accounting-method eligibility, real employee entitlements, all applicable sick/holiday/loan rules, provider credentials, signed original annual reports, complete schemas and production acceptance are not supplied by these sources. No packet may fill them with a plausible default. Existing source data must never be relabelled synthetic to bypass admission.

## R15: Late branch observation

`4671a2fbaea88bcab613f28b6d34a209b040ab06` was observed after the detailed source review. Its commit reports NEXT-01 implementation and no runtime exercise. See [REVISION-NOTE.md](REVISION-NOTE.md). No full-diff review or independent execution is claimed.
