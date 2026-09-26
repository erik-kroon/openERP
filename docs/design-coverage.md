# Design coverage

Each requirement has one owner below. This map records documentation coverage, not implementation or acceptance. [Work packets](plans/README.md), [open inputs](open-decisions.md) and [observed results](roadmap.md) have separate status.

| Concern                                                 | Owner                                                                                                                                | Acceptance               |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------ |
| Product scope and first reconciled period               | [Product](product.md)                                                                                                                | R-01–R-12                |
| Runtime, domain/SQL ownership and scoped resources      | [Architecture](architecture.md), [shared contracts](plans/00-shared-contracts.md)                                                    | D-02; E-01/E-20          |
| Exact money, dates, identities and compatible seals     | [Domain](domain.md), [exact contracts](plans/00-shared-contracts.md#exact-values-and-canonical-identity)                             | D-03; E-02/E-05/E-10     |
| Immutable approval, atomic posting and recovery         | [Posting](plans/01-posting-approval-receipts.md)                                                                                     | E-03–E-08/E-11           |
| Corrections and register consistency                    | [Corrections](plans/02-corrections.md)                                                                                               | E-09/E-13                |
| Bytes, source occurrences, matches and import resume    | [Imports](plans/03-imports-matching-reconciliation.md)                                                                               | E-05/E-08/E-12/E-17/E-18 |
| Independent source coverage and reconciliation          | [Imports](plans/03-imports-matching-reconciliation.md)                                                                               | E-13/E-15                |
| Invoices, payments, owners and settlement capacity      | [Commerce](plans/04-invoices-payments-registers.md)                                                                                  | E-12–E-14                |
| VAT/tax account, payroll, assets, schedules and FX      | [Accounting profiles](plans/05-vat-payroll-assets-fx.md)                                                                             | D-04/D-08; E-13–E-18     |
| Close, openings, reports, lineage and tax bridge        | [Year-end](plans/06-year-end-reports-filing.md)                                                                                      | E-07/E-10/E-14/E-16      |
| SIE, iXBRL, signatures and filing outcomes              | [Compliance](compliance.md), [year-end](plans/06-year-end-reports-filing.md)                                                         | D-08/D-10; E-18/E-19     |
| Rules, model interpretation, mandates and MCP           | [Operations](operations.md#governed-rules-and-agent-context)                                                                         | E-06/E-11/E-17           |
| Provider credentials, webhooks and delivery             | [Provider boundaries](operations.md#provider-and-delivery-boundaries)                                                                | E-17/E-19/E-20           |
| Archive, restore and single-writer cutover              | [Operations plan](plans/07-restore-operations-cutover.md), [migration ADR](adr/0003-native-accounting-and-migration.md)              | D-06/D-07; E-21          |
| Customer layout, routes, audience views and migration    | [Frontend plan](frontend.md), [workspace decision](adr/0006-customer-workspaces.md)                                                    | FE-01–FE-06; R-11        |
| Review UI, scoped caches and accessibility              | [Operations](operations.md), [frontend acceptance](frontend.md#acceptance-and-verification), [verification](verification-strategy.md#human-journeys) | E-03/E-06/E-11           |
| Independent expectations, races, upgrades and artifacts | [Scenarios](verification.md), [strategy](verification-strategy.md), [failure cases](plans/09-acceptance.md#additional-failure-cases) | E-01–E-21                |
| Official rules, formats and unresolved facts            | [Sources](sources/README.md), [external inputs](plans/10-external-inputs.md)                                                         | D-01–D-10                |

The [ADRs](adr/README.md) record selected choices and alternatives. Executable schemas own wire names; existing approved digests remain interpretable. Alternative package layouts, example schemas and runner proposals are not additional contracts.

The [initial runtime checkpoint](evidence/initial-runtime-checkpoint.md) retains exact results, migration hashes, failures and unexecuted cases. The [planning baseline](plans/evidence/planning-baseline.json) is a dated observation, not a live inventory. The [VAT research manifest](sources/sweden-vat-sources.json) retains source records and access limits. None establishes production or legal acceptance.

Additional industry, inventory, project, payroll or framework needs enter through the company profile. Missing applicability blocks release of the affected workflow. Broad topic coverage is not a claim of support. Update the owning specification and independent failure case when new knowledge changes a requirement.

The [product capability map](plans/capability-backlog.md) tracks the supplied capability IDs, reuses the owners above and owns supplemental collections, sales operations, dimensions, expense/payroll handoffs and extension requirements. It records planned scope only.

The [NEXT dossier plan](plans/12-next-implementation-dossier.md) is implementation-level design for work items whose requirements are owned above and in the capability map. It owns no requirement and no acceptance gate: a `NEXT-nn` packet states an existing owner, a delta and a set of design vectors, and its mapping to a maintained packet is a proposal to confirm against the checkout. The [vendored specifications](specs/README.md) hold the reviewed copies, and their checksums and self-checkers are the only proof recorded for them.
