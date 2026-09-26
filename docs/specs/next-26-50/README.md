# OpenERP: NEXT-26 through NEXT-50

Late branch movement is recorded in [REVISION-NOTE.md](REVISION-NOTE.md). The source review remains pinned; the current resolver is consumed rather than rebuilt.

**25 new application-owned work packets with implementation-level pseudocode.** These supplement the existing NEXT-01..25 v2 dossier; they do not replace it or assume it is complete.

Pinned repository review: `5ac3433e3e75ef7fc0229cbe00107003b63aa32d`. Proposed design only. No repository files were modified and no application/database/provider workflow was run.

## Use this package

Give the coordinator [MASTER-PSEUDOCODE.md](MASTER-PSEUDOCODE.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Give a domain worker [00-COMMON.md](00-COMMON.md), [qualified inputs](01-RULE-AND-PROVIDER-DATA.md), its packet and [SOURCES.md](SOURCES.md). Read the actual current repository instructions before implementing.

The source review combines the current application replacement plan, capability backlog and selected application modules. Statements of missing scope mean a specified next capability or limitation of the inspected owner, not a claim of having audited every file or uncommitted branch. Paths for new functions are proposals to place beside the existing owners.

All financial workflows live in Effect application operations. Pure calculations use exact inputs. Persistence passes one transaction through related domain writes. PostgreSQL retains scoped constraints, atomicity and narrow integrity. Background delivery uses the selected persistent Bun/effect-mq composition, not a resurrected SQL dispatcher or Worker listener.

## Packets

| ID | Priority | Solution | Owner lane |
|---|---|---|---|
| NEXT-26 | P0 | [Supplier extraction jobs and field-level reviewed merge](packets/NEXT-26.md) | INTAKE |
| NEXT-27 | P1 | [Reviewed party identity resolution without balance merging](packets/NEXT-27.md) | COMMERCE |
| NEXT-28 | P1 | [Authorized collection reminders and dispatch recovery](packets/NEXT-28.md) | DELIVERY |
| NEXT-29 | P1 | [Recurring invoice occurrences without duplicate billing](packets/NEXT-29.md) | COMMERCE |
| NEXT-30 | P1 | [Customer unapplied cash, paid credits and refunds](packets/NEXT-30.md) | COMMERCE |
| NEXT-31 | P1 | [Invoice-linked prepayments and accrued-cost true-up](packets/NEXT-31.md) | SCHEDULES |
| NEXT-32 | P2 | [Loan principal, interest accrual and repayment allocation](packets/NEXT-32.md) | TREASURY |
| NEXT-33 | P1 | [Employee expense claims with one financial handoff](packets/NEXT-33.md) | PAYROLL |
| NEXT-34 | P2 | [Mileage reimbursement with exact tax and payout partition](packets/NEXT-34.md) | PAYROLL |
| NEXT-35 | P2 | [Variable pay, absence and holiday-liability reconciliation](packets/NEXT-35.md) | PAYROLL |
| NEXT-36 | P1 | [Paid payroll recovery and retroactive compensation](packets/NEXT-36.md) | PAYROLL |
| NEXT-37 | P0 | [VAT assessment ownership and exact-to-assessed bridge](packets/NEXT-37.md) | TAX |
| NEXT-38 | P0 | [Cash-method recognition and unpaid year-end cutover](packets/NEXT-38.md) | TAX |
| NEXT-39 | P1 | [Processor balance and payout clearing, Stripe first](packets/NEXT-39.md) | TREASURY |
| NEXT-40 | P1 | [Foreign-currency cash holdings and transfers](packets/NEXT-40.md) | TREASURY |
| NEXT-41 | P1 | [Late FX valuation and consumed-chain correction](packets/NEXT-41.md) | TREASURY |
| NEXT-42 | P1 | [Economic impairment reversal and zero-carrying assets](packets/NEXT-42.md) | SCHEDULES |
| NEXT-43 | P1 | [Reviewed dimension restatement without editing journals](packets/NEXT-43.md) | REPORTING |
| NEXT-44 | P1 | [Multi-year SIE partition and dimension-preserving import](packets/NEXT-44.md) | REPORTING |
| NEXT-45 | P1 | [Direct cash-flow statement with a full reconciliation bridge](packets/NEXT-45.md) | REPORTING |
| NEXT-46 | P1 | [Peppol invoice and credit exchange through a selected access point](packets/NEXT-46.md) | DELIVERY |
| NEXT-47 | P1 | [Document signatures bound to exact content and purpose](packets/NEXT-47.md) | DELIVERY |
| NEXT-48 | P1 | [Bolagsverket submission and authority-outcome lifecycle](packets/NEXT-48.md) | DELIVERY |
| NEXT-49 | P0 | [Rule-change impact and evidence-backed obligation fulfillment](packets/NEXT-49.md) | REPORTING |
| NEXT-50 | P0 | [Agent book context, deltas and cross-domain unresolved-work index](packets/NEXT-50.md) | AGENT |

## Scope and verification

The five original active workstreams and the application migration retain ownership. Their dependencies are spelled out in the integration map. No new packet redoes VAT reclassification qualification, FX partial release, impairment UI closure, VAT amendment delta or webshop intake.

The packet algorithms include financial effects, state identity, concurrency, correction consequences, UI/agent behavior and concrete vectors. Statutory rates, employment agreements, complete validation bundles and credentials remain explicit qualified inputs. The external source notes state where only an official index/search rendering was available.

[DECISIONS.md](DECISIONS.md) highlights the consequential new choices. [CHECKS.md](CHECKS.md) and [checks/results.json](checks/results.json) report only this dossier's structural and arithmetic self-checks. They do not establish runtime correctness of the application.

The task/dependency board is [solution-index.json](solution-index.json). Every packet contains a specific delta from the prior wave or an existing source owner. The loan packet is explicitly a proposed extension of the funding lifecycle, not a false claim that a source bug was found.

The compact exact example inventory is [design-examples.json](design-examples.json). The coordinator can start from [COORDINATOR-HANDOFF.md](COORDINATOR-HANDOFF.md).
