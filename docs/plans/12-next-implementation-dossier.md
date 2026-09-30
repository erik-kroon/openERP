# NEXT implementation dossiers: packets, prerequisites and mapping

Status: **planning scope, implementation-level design; no implementation or verification status**. Added 2026-09-26; the third, fourth and fifth waves added 2026-09-28. Owner: cross-area integrator, with the per-packet owner lane named in each packet. Phase: supplemental to the seven-area [delivery plan](README.md); the packets are **not** added to the 53-packet accounting index or its dependency DAG.

The decision to vendor these dossiers, keep them outside the maintained plan namespace and treat `NEXT-nn` as a work namespace rather than a delivery index is [ADR 0012](../adr/0012-next-implementation-dossier.md). The vendored files themselves are listed in [the specifications index](../specs/README.md).

## What these documents are

Five externally produced dossiers specify **how** one hundred twenty-five work items would be implemented inside the application-owned Effect boundary: named application operations, pure exact calculations, transaction-passing persistence, typed approval, durable queue delivery through the existing outbox and effect-mq runner, and the failure/replay cases each operation must survive. They supply per-item algorithms, record shapes, transaction sketches, UI/agent expectations and concrete numeric vectors.

They are not a repository audit, not an applied implementation and not runtime proof. Each packet states its own status as proposed application-owned pseudocode.

| Wave | Packets | Pinned review | Archive self-check, re-run on import |
| --- | --- | --- | --- |
| `next-01-25` — application-owned Effect edition v2 | NEXT-01 … NEXT-25 | `422276ae…` architecture context, `bb628452…` inherited task baseline | 7,465 assertions, 0 failures; 37 of 37 checksums OK |
| `next-26-50` — second wave | NEXT-26 … NEXT-50 | `5ac3433e…` repository review dated 2026-09-26, plus the limited late observation `4671a2fb…` | 90 of 90 named design checks passed; 41 of 41 checksums OK |
| `next-51-75` — third wave | NEXT-51 … NEXT-75 | `116a5ca6…` repository review, prepared 2026-09-28 | 80 of 80 named design checks passed; 40 of 40 checksums OK |
| `next-76-100` — fourth wave | NEXT-76 … NEXT-100 | `66355b6…` — this repository's head at import — prepared 2026-09-28; targeted reading, not a source audit | 264 of 264 named design checks passed (131 structure, 69 document, 64 arithmetic); 40 of 40 checksums OK |
| `next-101-125` — fifth wave | NEXT-101 … NEXT-125 | `66355b6…` — this repository's head at import — prepared 2026-09-28; targeted reading of the branch and shared operations/contracts | 741 of 741 named design checks passed (572 structure/dependency/document/link, 169 arithmetic, model and published-vector); 40 of 40 checksums OK |

The dated import observations and their limits are recorded in [next-dossier-verification.md](evidence/next-dossier-verification.md) for the first two waves, [next-51-75-dossier-verification.md](evidence/next-51-75-dossier-verification.md) for the third and [next-76-100-dossier-verification.md](evidence/next-76-100-dossier-verification.md) for the fourth, [next-101-125-dossier-verification.md](evidence/next-101-125-dossier-verification.md) for the fifth.

## Relationship to the other planning layers

| Layer | Owns | Does not own |
| --- | --- | --- |
| [Seven-area delivery plan](README.md) (`FND`/`PST`/`COR`/`IMP`/`COM`/`VAT`/`PAY`/`AST`/`FX`/`END`/`OPS-nn`) | The delivery denominator, mandatory dependency DAG, acceptance and traceability | Implementation-level algorithms, exact vectors, per-operation failure matrices |
| [Capability backlog](capability-backlog.md) (`SALES`/`PUR`/`BANK`/`TAX`/… labels) | Which requested capability is owned, and the supplemental collections, supplier inbox, party master, recurring invoicing, deadlines and expense/payroll handoffs | Work units, prerequisites and proof for those requirements |
| [Reference parity backlog](11-parity-backlog.md) (`PRY-nn`) | Reference-implementation findings with an adopt/structure-only/re-derive class per rule | Anything the reference does not contain, including the second wave's treasury, tax-assessment and cash-flow work |
| **NEXT dossiers (`NEXT-nn`, this document)** | Implementation-level design per work item: existing owner, new scope, algorithm, transaction boundary, failure and replay cases, vectors | Requirements, applicability decisions, delivery order, completion counts or proof |

A `NEXT-nn` packet is therefore the **implementation design for a requirement the plans already own**, plus a small number of lifecycle extensions the plans name only as follow-up work. It does not add scope on its own, and it never renumbers any existing namespace.

## Rules for an implementing agent

1. **The repository instructions win.** Read `AGENTS.md`, [ADR 0009](../adr/0009-effect-mq-background-jobs.md), [ADR 0010](../adr/0010-application-owned-accounting-replacement.md) and the owning area plan first. A packet that conflicts with them is corrected by the packet, not by the repository rule.
2. **Pinned statements are dated, not current.** The pinned revisions are ancestors of this repository's history. Reconcile the actual checkout before coding: a named path, function or module is a proposed responsibility to bind to real code, and a statement that something was missing describes that pinned revision only. The second wave's own `REVISION-NOTE.md` records that NEXT-01 was reported implemented at `4671a2f` with static checks only and no runtime proof. The third wave's own `INTEGRATION-MAP.md` is narrower still: "new" there means absent from the **prior NEXT scope**, and it states explicitly that this is not an exhaustive absence audit of current source. The fourth and fifth waves are both pinned to the current head and both state that their reading was targeted rather than a source audit, so they are the best-pinned and the least-audited at the same time.
3. **`APP-SLICE-READY(area)` is a prerequisite, not extra work.** Resolve it against the real checkout: the area's named operations, scoped persistence and complete correction/recovery behavior must be released by the migration owner. A route that returns `UnsupportedProfile` is not a ported implementation. When the port is missing, deliver the leaf calculator, schema and exact integration contract without taking over the migration owner.
4. **One financial transaction per group.** The caller's transaction is passed into every nested journal, tax, register, approval-use and receipt write. No public execute/HTTP call opens a second transaction from inside a financial group, and no nested operation re-acquires a book lock.
5. **Exact values only.** Canonical exact integer strings over the wire, `bigint` internally, exact rational rates and quantities with units. An amount, balance or sequence never becomes a JavaScript number. Retain a rounding residual and explain it rather than posting a plug.
6. **Reserved owners stay reserved.** The five reserved workstreams and the application replacement are listed below. Consume a released owner; do not reimplement it, and do not create a second writable financial register to avoid a missing port.
7. **Vectors are obligations, not tests.** Each packet's numeric vectors and failure cases are design obligations to satisfy and to verify under the actual test authorization in force. The dossiers add no repository test and grant no deployment, provider, payment, filing or company-data authority.
8. **Report the real state.** A worker returns exact changed paths, exported operations and contracts, schema/grant needs, declared financial ownership, the checks actually run, unresolved gates and remaining blockers. A documented function that refuses every case is not a completed packet, and a JSON preparation record or a UI button alone is not completion.
9. **An unfinished earlier packet is not a new packet.** The third, fourth and fifth waves all state that the earlier ranges keep their own application, persistence and proof obligations, and the last two record their prior ranges as "not assumed complete". Finishing a later packet on top of an unreleased earlier owner is not the earlier packet's completion, and a "new deliverable" is not evidence that the earlier work item is done. Read required and conditional integrations separately: a services-only reporting profile does not wait for goods support, and a customer portal need not wait for payment-link checkout. A new work number is never a migration number.

## Packet index

`Requires` lists the packets whose contracts must exist first. `Integrate after` lists the released application slices the packet composes with; an empty cell means the packet names an existing owner directly. `Conditional` entries apply only when the selected company actually uses that case — a conditional edge is not a reason to delay independent work, and an inapplicable case is never a reason to call the product complete.

Lane codes are the archives' own owner lanes. The first wave's single-letter lanes are not defined in the vendored files; the second and third waves' named lanes are self-describing.

The third wave's `Requires` column mixes prior-wave and same-wave contracts, because its own integration table does; the wave states that prior NEXT contracts are external nodes whose completion is not assumed. The fourth wave separates `prior_dependencies` from same-wave `dependencies` in its own table, and several of its packets name only "existing core owners" with no NEXT prerequisite at all — those are the ones to check against the checkout first. The fifth wave uses the same shape and adds that only its own new-wave edges are checked, with no 125-node graph claim.

### First wave: NEXT-01 … NEXT-25

| ID | Priority | Lane | Solution | Requires | Integrate after | Conditional | Packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT-01 | P0 | F | Owner-aware case review | — | — | — | [NEXT-01](../specs/next-01-25/packets/NEXT-01.md) |
| NEXT-02 | P0 | A | Capability-specific company admission | — | — | — | [NEXT-02](../specs/next-01-25/packets/NEXT-02.md) |
| NEXT-03 | P0 | B | Domestic purchasing with owned tax recognition | NEXT-02 | — | — | [NEXT-03](../specs/next-01-25/packets/NEXT-03.md) |
| NEXT-04 | P0 | B | Actual domestic VAT return and controls | NEXT-02, NEXT-03 | — | — | [NEXT-04](../specs/next-01-25/packets/NEXT-04.md) |
| NEXT-05 | P0 | B | General-rule cross-border service purchases | NEXT-03, NEXT-04 | — | NEXT-17 (actual unpaid foreign-denominated supplier obligations occur) | [NEXT-05](../specs/next-01-25/packets/NEXT-05.md) |
| NEXT-06 | P0 | A | Owner-paid expenses, reimbursement and funding | NEXT-02, NEXT-03 | — | — | [NEXT-06](../specs/next-01-25/packets/NEXT-06.md) |
| NEXT-07 | P1 | B | Supplier paid credits and refunds | NEXT-03 | — | NEXT-08 (an exported payment reservation must first be resolved) | [NEXT-07](../specs/next-01-25/packets/NEXT-07.md) |
| NEXT-08 | P1 | C | Payment instruction resolution and replacement | — | — | — | [NEXT-08](../specs/next-01-25/packets/NEXT-08.md) |
| NEXT-09 | P1 | C | Complete Plaid sync windows | — | — | — | [NEXT-09](../specs/next-01-25/packets/NEXT-09.md) |
| NEXT-10 | P1 | C | Provider revisions to reviewed bank observations | NEXT-09 | — | — | [NEXT-10](../specs/next-01-25/packets/NEXT-10.md) |
| NEXT-11 | P0 | D | Separate complete-book SIE4E export | NEXT-02, NEXT-13 | — | NEXT-14 (dimension assignments occur in the selected book) | [NEXT-11](../specs/next-01-25/packets/NEXT-11.md) |
| NEXT-12 | P1 | D | Historical open-item adoption | NEXT-02 | — | — | [NEXT-12](../specs/next-01-25/packets/NEXT-12.md) |
| NEXT-13 | P0 | D | Semantic P&L and balance-sheet snapshots | NEXT-02 | — | — | [NEXT-13](../specs/next-01-25/packets/NEXT-13.md) |
| NEXT-14 | P2 | F | Original dimension assignments | — | NEXT-13 | — | [NEXT-14](../specs/next-01-25/packets/NEXT-14.md) |
| NEXT-15 | P1 | F | Legal customer credit notes | NEXT-02 | NEXT-04 | — | [NEXT-15](../specs/next-01-25/packets/NEXT-15.md) |
| NEXT-16 | P0 | A | Evidence-aware period preparation | NEXT-01, NEXT-03, NEXT-06 | — | — | [NEXT-16](../specs/next-01-25/packets/NEXT-16.md) |
| NEXT-17 | P1 | E | Payable FX and explicit fees | NEXT-02 | NEXT-03 | — | [NEXT-17](../specs/next-01-25/packets/NEXT-17.md) |
| NEXT-18 | P1 | E | Incremental open-item FX remeasurement | NEXT-17 | — | — | [NEXT-18](../specs/next-01-25/packets/NEXT-18.md) |
| NEXT-19 | P1 | E | Disposal with proceeds | — | — | NEXT-04 (the disposal has a VAT-reporting consequence); NEXT-15 (the chosen flow requires a supported legal invoice/credit interaction) | [NEXT-19](../specs/next-01-25/packets/NEXT-19.md) |
| NEXT-20 | P2 | E | Frozen regular-payroll calculation | NEXT-02 | — | — | [NEXT-20](../specs/next-01-25/packets/NEXT-20.md) |
| NEXT-21 | P2 | E | Payroll posting, payslip and AGI artifact | NEXT-20 | — | — | [NEXT-21](../specs/next-01-25/packets/NEXT-21.md) |
| NEXT-22 | P1 | D | Pre-close tax bridge and INK2/SRU | NEXT-13 | — | — | [NEXT-22](../specs/next-01-25/packets/NEXT-22.md) |
| NEXT-23 | P1 | D | Financial close and single-count carry-forward | NEXT-13, NEXT-22 | — | NEXT-04 (the reviewed company/year inventory makes this treatment applicable); NEXT-05 (the reviewed company/year inventory makes this treatment applicable); NEXT-06 (the reviewed company/year inventory makes this treatment applicable); NEXT-07 (the reviewed company/year inventory makes this treatment applicable); NEXT-12 (the reviewed company/year inventory makes this treatment applicable); NEXT-18 (the reviewed company/year inventory makes this treatment applicable); NEXT-19 (the reviewed company/year inventory makes this treatment applicable); NEXT-21 (the reviewed company/year inventory makes this treatment applicable) | [NEXT-23](../specs/next-01-25/packets/NEXT-23.md) |
| NEXT-24 | P1 | D | K2 annual-report semantic model and iXBRL | NEXT-13, NEXT-23 | — | — | [NEXT-24](../specs/next-01-25/packets/NEXT-24.md) |
| NEXT-25 | P0 | ROOT | Fixed-revision company rehearsal and restore | — | — | NEXT-02 (required by the selected real-company rehearsal scope); NEXT-03 (required by the selected real-company rehearsal scope); NEXT-04 (required by the selected real-company rehearsal scope); NEXT-05 (required by the selected real-company rehearsal scope); NEXT-06 (required by the selected real-company rehearsal scope); NEXT-11 (required by the selected real-company rehearsal scope); NEXT-12 (required by the selected real-company rehearsal scope); NEXT-13 (required by the selected real-company rehearsal scope); NEXT-16 (required by the selected real-company rehearsal scope); NEXT-21 (required by the selected real-company rehearsal scope); NEXT-23 (required by the selected real-company rehearsal scope); NEXT-24 (required by the selected real-company rehearsal scope) | [NEXT-25](../specs/next-01-25/packets/NEXT-25.md) |

**Implementation status, first wave.** NEXT-01, NEXT-02, NEXT-11 and NEXT-13 are implemented in source. "Implemented" means merged source with static checks passing and **no runtime proof**; the unverified surface per packet is recorded in [next-packet-progress.md](next-packet-progress.md). Rows are retained, not deleted, and the reserved-work and mapping tables above are unchanged. NEXT-25 is deliberately deferred to the end of the programme despite its P0 priority: it rehearses a fixed-revision company across the financial slices it requires, so running it before those slices exist would prove nothing.

### Second wave: NEXT-26 … NEXT-50

| ID | Priority | Lane | Solution | Requires | Integrate after | Conditional | Packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT-26 | P0 | INTAKE | Supplier extraction jobs and field-level reviewed merge | — | APP-SLICE-READY(purchases/inbox) | NEXT-03 (a reviewed draft is subsequently accepted and posted) | [NEXT-26](../specs/next-26-50/packets/NEXT-26.md) |
| NEXT-27 | P1 | COMMERCE | Reviewed party identity resolution without balance merging | — | APP-SLICE-READY(commerce/crm-master) | NEXT-02 (legal identity facts or payment-role qualification are needed) | [NEXT-27](../specs/next-26-50/packets/NEXT-27.md) |
| NEXT-28 | P1 | DELIVERY | Authorized collection reminders and dispatch recovery | — | APP-SLICE-READY(commerce/collections), APP-SLICE-READY(durable-delivery) | NEXT-15 (the selected invoice has credit-note adjustments); NEXT-30 (customer-credit balances affect the reminder amount) | [NEXT-28](../specs/next-26-50/packets/NEXT-28.md) |
| NEXT-29 | P1 | COMMERCE | Recurring invoice occurrences without duplicate billing | NEXT-02 | APP-SLICE-READY(commerce/invoice-lifecycle) | NEXT-15 (an issued recurring invoice needs a credit) | [NEXT-29](../specs/next-26-50/packets/NEXT-29.md) |
| NEXT-30 | P1 | COMMERCE | Customer unapplied cash, paid credits and refunds | NEXT-15 | APP-SLICE-READY(commerce/register) | NEXT-04 (credit notes affect a supported VAT return) | [NEXT-30](../specs/next-26-50/packets/NEXT-30.md) |
| NEXT-31 | P1 | SCHEDULES | Invoice-linked prepayments and accrued-cost true-up | NEXT-03, NEXT-13 | APP-SLICE-READY(subledger/schedules) | WIP-AST03-UI (the released schedule/control implementation is shared with the asset owner) | [NEXT-31](../specs/next-26-50/packets/NEXT-31.md) |
| NEXT-32 | P2 | TREASURY | Loan principal, interest accrual and repayment allocation | NEXT-02 | APP-SLICE-READY(subledger/owners) | NEXT-06 (shareholder funding already recognized supplies the opening loan basis); NEXT-13 (publishing reconciled loan controls) | [NEXT-32](../specs/next-26-50/packets/NEXT-32.md) |
| NEXT-33 | P1 | PAYROLL | Employee expense claims with one financial handoff | NEXT-03 | APP-SLICE-READY(purchases), APP-SLICE-READY(payroll-foundation) | NEXT-21 (the approved payout route is payroll rather than a payable payment) | [NEXT-33](../specs/next-26-50/packets/NEXT-33.md) |
| NEXT-34 | P2 | PAYROLL | Mileage reimbursement with exact tax and payout partition | NEXT-33 | APP-SLICE-READY(payroll-foundation) | NEXT-20 (the selected entitlement includes taxable compensation); NEXT-21 (payout/reporting uses payroll) | [NEXT-34](../specs/next-26-50/packets/NEXT-34.md) |
| NEXT-35 | P2 | PAYROLL | Variable pay, absence and holiday-liability reconciliation | NEXT-20 | NEXT-21 | — | [NEXT-35](../specs/next-26-50/packets/NEXT-35.md) |
| NEXT-36 | P1 | PAYROLL | Paid payroll recovery and retroactive compensation | NEXT-21 | APP-SLICE-READY(payroll) | NEXT-35 (the correction includes variable, absence or holiday components) | [NEXT-36](../specs/next-26-50/packets/NEXT-36.md) |
| NEXT-37 | P0 | TAX | VAT assessment ownership and exact-to-assessed bridge | NEXT-04 | WIP-VAT03, WIP-VAT04-A1, APP-SLICE-READY(tax-account) | — | [NEXT-37](../specs/next-26-50/packets/NEXT-37.md) |
| NEXT-38 | P0 | TAX | Cash-method recognition and unpaid year-end cutover | NEXT-03, NEXT-04 | APP-SLICE-READY(commerce/register) | NEXT-23 (the reviewed unpaid population is consumed by financial year-end) | [NEXT-38](../specs/next-26-50/packets/NEXT-38.md) |
| NEXT-39 | P1 | TREASURY | Processor balance and payout clearing, Stripe first | NEXT-30 | APP-SLICE-READY(source-intake), APP-SLICE-READY(commerce/register) | NEXT-40 (processor balances use a non-book currency); WIP-COM2-W1 (read-only order provenance is required; do not modify its intake) | [NEXT-39](../specs/next-26-50/packets/NEXT-39.md) |
| NEXT-40 | P1 | TREASURY | Foreign-currency cash holdings and transfers | NEXT-17, NEXT-18 | WIP-FX02-P1, APP-SLICE-READY(banking) | — | [NEXT-40](../specs/next-26-50/packets/NEXT-40.md) |
| NEXT-41 | P1 | TREASURY | Late FX valuation and consumed-chain correction | NEXT-18 | WIP-FX02-P1, APP-SLICE-READY(commerce-fx) | NEXT-40 (the affected chain includes native foreign-cash holdings); NEXT-23 (affected financial periods require approved reopening) | [NEXT-41](../specs/next-26-50/packets/NEXT-41.md) |
| NEXT-42 | P1 | SCHEDULES | Economic impairment reversal and zero-carrying assets | — | WIP-AST03-UI, APP-SLICE-READY(subledger) | NEXT-19 (checking disposal/proceeds consumers); NEXT-13 (presenting the resulting financial controls) | [NEXT-42](../specs/next-26-50/packets/NEXT-42.md) |
| NEXT-43 | P1 | REPORTING | Reviewed dimension restatement without editing journals | NEXT-14, NEXT-13 | APP-SLICE-READY(dimensions) | — | [NEXT-43](../specs/next-26-50/packets/NEXT-43.md) |
| NEXT-44 | P1 | REPORTING | Multi-year SIE partition and dimension-preserving import | NEXT-12, NEXT-14 | APP-SLICE-READY(historical-migration) | NEXT-11 (independent roundtrip export is part of acceptance) | [NEXT-44](../specs/next-26-50/packets/NEXT-44.md) |
| NEXT-45 | P1 | REPORTING | Direct cash-flow statement with a full reconciliation bridge | NEXT-13 | APP-SLICE-READY(reports) | NEXT-40 (the selected cash perimeter contains foreign-currency holdings); NEXT-39 (processor/transit positions belong to the selected cash perimeter) | [NEXT-45](../specs/next-26-50/packets/NEXT-45.md) |
| NEXT-46 | P1 | DELIVERY | Peppol invoice and credit exchange through a selected access point | NEXT-03, NEXT-15 | APP-SLICE-READY(invoice-delivery) | NEXT-26 (inbound documents enter the assisted supplier-review workflow) | [NEXT-46](../specs/next-26-50/packets/NEXT-46.md) |
| NEXT-47 | P1 | DELIVERY | Document signatures bound to exact content and purpose | NEXT-24 | APP-SLICE-READY(artifacts) | — | [NEXT-47](../specs/next-26-50/packets/NEXT-47.md) |
| NEXT-48 | P1 | DELIVERY | Bolagsverket submission and authority-outcome lifecycle | NEXT-24, NEXT-47 | APP-SLICE-READY(external-delivery) | — | [NEXT-48](../specs/next-26-50/packets/NEXT-48.md) |
| NEXT-49 | P0 | REPORTING | Rule-change impact and evidence-backed obligation fulfillment | NEXT-02 | APP-SLICE-READY(closing/deadlines) | NEXT-04 (VAT calculations are impacted); NEXT-21 (payroll declarations are impacted); NEXT-48 (annual-report authority outcomes fulfill deadlines) | [NEXT-49](../specs/next-26-50/packets/NEXT-49.md) |
| NEXT-50 | P0 | AGENT | Agent book context, deltas and cross-domain unresolved-work index | NEXT-01, NEXT-16 | APP-SLICE-READY(capabilities) | NEXT-49 (including qualified deadline/impact outcomes); NEXT-33 (including employee claim summaries under separate permissions) | [NEXT-50](../specs/next-26-50/packets/NEXT-50.md) |

**Implementation status, second wave.** Recorded in [next-packet-progress.md](next-packet-progress.md), where NEXT-37 and NEXT-39 carry the only real HTTP/MCP or integrated E2E evidence in this wave; both are explicitly bounded to synthetic or local cases, with real-company and provider qualification open. Most second-wave rows are leaf or compiler-level with the HTTP/MCP journey unobserved. These are source-review statements about that table, not a completion denominator.

### Third wave: NEXT-51 … NEXT-75

The third wave's `Requires` column names both prior-wave and same-wave contracts. Its own `dependency-graph.json` publishes an acyclic order over the new wave only, and states that the earlier fifty are external nodes whose completion is not assumed.

| ID | Priority | Lane | Solution | Requires | Conditional | Packet |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT-51 | P0 | COMMERCE | Mixed-rate domestic sales and tax-inclusive prices | NEXT-02, NEXT-04, NEXT-15 | — | [NEXT-51](../specs/next-51-75/packets/NEXT-51.md) |
| NEXT-52 | P1 | COMMERCE | Cross-border B2B service sales and customer-status evidence | NEXT-02, NEXT-04, NEXT-15, NEXT-51 | NEXT-17 (the selected sale is in foreign currency) | [NEXT-52](../specs/next-51-75/packets/NEXT-52.md) |
| NEXT-53 | P2 | TAX-COMMERCE | Intra-EU goods acquisition and supply accounting | NEXT-02, NEXT-03, NEXT-04, NEXT-15, NEXT-51 | — | [NEXT-53](../specs/next-51-75/packets/NEXT-53.md) |
| NEXT-54 | P2 | TAX-COMMERCE | Customs imports, import VAT and landed-cost attribution | NEXT-02, NEXT-03, NEXT-04 | — | [NEXT-54](../specs/next-51-75/packets/NEXT-54.md) |
| NEXT-55 | P1 | TAX-REPORTING | Periodisk sammanställning with correction lineage | NEXT-04, NEXT-49 | NEXT-52 (the statement includes general-rule cross-border services); NEXT-53 (the statement includes qualifying intra-EU goods) | [NEXT-55](../specs/next-51-75/packets/NEXT-55.md) |
| NEXT-56 | P1 | COMMERCE | Customer advances, deposits and final-invoice application | NEXT-02, NEXT-04, NEXT-30, NEXT-51 | — | [NEXT-56](../specs/next-51-75/packets/NEXT-56.md) |
| NEXT-57 | P1 | COMMERCE | Supplier advances and final-purchase settlement | NEXT-02, NEXT-03, NEXT-07 | — | [NEXT-57](../specs/next-51-75/packets/NEXT-57.md) |
| NEXT-58 | P0 | SCHEDULES | Invoice-driven deferred revenue and service-period changes | NEXT-02, NEXT-15 | NEXT-29 (the originating invoice is a recurring occurrence); NEXT-31 (the shared schedule contract is extended together with expense deferral) | [NEXT-58](../specs/next-51-75/packets/NEXT-58.md) |
| NEXT-59 | P1 | COMMERCE | Installment terms, partial due amounts and payment promises | NEXT-15, NEXT-30 | NEXT-50 (installment and promise summaries appear in agent context) | [NEXT-59](../specs/next-51-75/packets/NEXT-59.md) |
| NEXT-60 | P1 | COMMERCE | Payment discounts and evidenced settlement differences | NEXT-07, NEXT-15, NEXT-30 | NEXT-17 (the settlement includes foreign-currency principal or an evidenced FX difference) | [NEXT-60](../specs/next-51-75/packets/NEXT-60.md) |
| NEXT-61 | P1 | COMMERCE-TAX | Receivable allowances, confirmed losses and later recovery | NEXT-04, NEXT-15, NEXT-30 | — | [NEXT-61](../specs/next-51-75/packets/NEXT-61.md) |
| NEXT-62 | P2 | COMMERCE | Dunning interest and enforceable reminder fees | NEXT-28, NEXT-30, NEXT-59 | — | [NEXT-62](../specs/next-51-75/packets/NEXT-62.md) |
| NEXT-63 | P2 | COMMERCE | Self-billed sales and buyer-issued invoice acceptance | NEXT-02, NEXT-15, NEXT-51 | — | [NEXT-63](../specs/next-51-75/packets/NEXT-63.md) |
| NEXT-64 | P1 | PAYMENTS | Invoice payment links with outstanding-bound settlement | NEXT-30, NEXT-39 | NEXT-59 (a link covers a selected installment rather than the whole residual) | [NEXT-64](../specs/next-51-75/packets/NEXT-64.md) |
| NEXT-65 | P1 | COMMERCE-UX | Scoped customer document and statement portal | NEXT-13, NEXT-30 | NEXT-59 (the portal shows installment due amounts and promises); NEXT-64 (the portal offers a separately authorized payment link) | [NEXT-65](../specs/next-51-75/packets/NEXT-65.md) |
| NEXT-66 | P2 | PROCUREMENT | Purchase commitments and three-way invoice matching | NEXT-03 | NEXT-26 (invoice source matching uses extraction suggestions); NEXT-31 (accepted unbilled service is recognized through an accrued-cost decision) | [NEXT-66](../specs/next-51-75/packets/NEXT-66.md) |
| NEXT-67 | P2 | PROCUREMENT | Commitment-aware budgets with stop and warn decisions | NEXT-13, NEXT-14, NEXT-66 | — | [NEXT-67](../specs/next-51-75/packets/NEXT-67.md) |
| NEXT-68 | P0 | FOUNDATION-REPORTING | Versioned BAS chart adoption and controlled annual updates | NEXT-02, NEXT-13, NEXT-49 | NEXT-14 (account changes affect active dimension requirements) | [NEXT-68](../specs/next-51-75/packets/NEXT-68.md) |
| NEXT-69 | P1 | INTAKE | Spreadsheet master-data import with staged reconciliation | NEXT-02, NEXT-27 | — | [NEXT-69](../specs/next-51-75/packets/NEXT-69.md) |
| NEXT-70 | P0 | BANKING | Structured bank-statement ingestion with exact entry lineage | NEXT-09, NEXT-10 | NEXT-40 (the statement belongs to a native foreign-currency cash account) | [NEXT-70](../specs/next-51-75/packets/NEXT-70.md) |
| NEXT-71 | P0 | PAYMENTS | Bank-qualified payment exports and status reconciliation | NEXT-08, NEXT-10, NEXT-70 | NEXT-17 (the bank profile settles foreign-currency obligations); NEXT-59 (transfers select invoice installments) | [NEXT-71](../specs/next-51-75/packets/NEXT-71.md) |
| NEXT-72 | P0 | TAX-DELIVERY | VAT declaration submission and authoritative return history | NEXT-04, NEXT-49 | NEXT-37 (link an actual later assessment; submission itself has no assessment journal) | [NEXT-72](../specs/next-51-75/packets/NEXT-72.md) |
| NEXT-73 | P1 | PAYROLL-DELIVERY | AGI submission and stable individual correction outcomes | NEXT-21, NEXT-49 | NEXT-36 (the submission changes previously paid compensation); NEXT-47 (the protocol uses an independently qualified signature adapter) | [NEXT-73](../specs/next-51-75/packets/NEXT-73.md) |
| NEXT-74 | P1 | TAX-DELIVERY | INK2 filing, signature handoff and assessment attribution | NEXT-22, NEXT-23, NEXT-49 | — | [NEXT-74](../specs/next-51-75/packets/NEXT-74.md) |
| NEXT-75 | P2 | TAX-FOUNDATION | Accounting-method change with conserved recognition coverage | NEXT-02, NEXT-03, NEXT-04, NEXT-23, NEXT-38 | NEXT-12 (imported open items require historical recognition evidence) | [NEXT-75](../specs/next-51-75/packets/NEXT-75.md) |

**Implementation status, third wave.** None. No third-wave packet has a row in [next-packet-progress.md](next-packet-progress.md), and this document creates no implementation state for one. The wave's own suggested sequence — 51, 58, 68, 70 first, then 52 and 55, then 64, 65, 71, 72 — is its authors' advice about where ordinary commercial demand starts, not a release checklist this repository adopts.

### Fourth wave: NEXT-76 … NEXT-100

Like the third wave, the `Requires` column mixes prior-wave and same-wave contracts. Its `solution-index.json` records `prior_status: "not assumed complete"` and states that only the new-wave graph is checked — the earlier seventy-five are an external contract dependency, not a revalidated hundred-task graph.

| ID | Priority | Lane | Solution | Requires | Conditional | Packet |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT-76 | P1 | SALES | Accepted contract changes and sales-order billing limits | existing core owners | NEXT-51 (issuing invoices with the chosen tax/price profile) | [NEXT-76](../specs/next-76-100/packets/NEXT-76.md) |
| NEXT-77 | P1 | SALES | Time-and-materials billing with once-only work coverage | NEXT-51, NEXT-76 | NEXT-79 (the selected work already has unbilled revenue recognition) | [NEXT-77](../specs/next-76-100/packets/NEXT-77.md) |
| NEXT-78 | P1 | SALES | Milestone certificates and retained contract consideration | NEXT-51, NEXT-59, NEXT-76 | NEXT-79 (prior earned revenue or a conditional contract-asset treatment is selected) | [NEXT-78](../specs/next-76-100/packets/NEXT-78.md) |
| NEXT-79 | P1 | SALES | Earned but unbilled service revenue and later invoicing | NEXT-13, NEXT-51, NEXT-58, NEXT-76 | — | [NEXT-79](../specs/next-76-100/packets/NEXT-79.md) |
| NEXT-80 | P1 | PURCHASES | Supplier disputes with partial payment holds and release | NEXT-03, NEXT-07, NEXT-08, NEXT-71 | — | [NEXT-80](../specs/next-76-100/packets/NEXT-80.md) |
| NEXT-81 | P1 | ASSETS | Asset work-in-progress and commissioning from purchase costs | NEXT-03, NEXT-31 | NEXT-54 (qualified import/landed-cost components enter the asset basis) | [NEXT-81](../specs/next-76-100/packets/NEXT-81.md) |
| NEXT-82 | P2 | ASSETS | Component replacement, improvements and partial asset retirement | NEXT-19, NEXT-42, NEXT-81 | — | [NEXT-82](../specs/next-76-100/packets/NEXT-82.md) |
| NEXT-83 | P2 | PURCHASES | Operating-rental contracts, refundable deposits and index changes | NEXT-31, NEXT-57, NEXT-59 | — | [NEXT-83](../specs/next-76-100/packets/NEXT-83.md) |
| NEXT-84 | P2 | TAX | Book-to-tax depreciation cohorts and excess-depreciation bridge | NEXT-02, NEXT-13 | NEXT-22 (the annual tax bridge consumes the selected deduction); NEXT-81 (new commissioned assets enter the eligible tax pool) | [NEXT-84](../specs/next-76-100/packets/NEXT-84.md) |
| NEXT-85 | P2 | TAX | Periodiseringsfond cohorts, reversals and annual tax linkage | NEXT-22, NEXT-49 | — | [NEXT-85](../specs/next-76-100/packets/NEXT-85.md) |
| NEXT-86 | P2 | TAX | ROT/RUT split claims and customer-authority settlement | NEXT-51, NEXT-15, NEXT-30, NEXT-49 | — | [NEXT-86](../specs/next-76-100/packets/NEXT-86.md) |
| NEXT-87 | P2 | PAYROLL | Pension invoice reconciliation and SLP annual basis | NEXT-03, NEXT-20, NEXT-22 | NEXT-35 (payroll accruals already include pension provisions) | [NEXT-87](../specs/next-76-100/packets/NEXT-87.md) |
| NEXT-88 | P2 | PAYROLL | Employment termination and final-pay obligation closure | NEXT-20, NEXT-21, NEXT-35, NEXT-36 | NEXT-87 (pension obligations require a final provider settlement) | [NEXT-88](../specs/next-76-100/packets/NEXT-88.md) |
| NEXT-89 | P2 | EQUITY | Dividend resolutions, shareholder payables and KU31 preparation | NEXT-02, NEXT-22, NEXT-23, NEXT-49 | — | [NEXT-89](../specs/next-76-100/packets/NEXT-89.md) |
| NEXT-90 | P2 | INCOME | Conditional grants, earned funding and repayment obligations | NEXT-02, NEXT-03, NEXT-13, NEXT-22 | — | [NEXT-90](../specs/next-76-100/packets/NEXT-90.md) |
| NEXT-91 | P1 | PURCHASES | Apply supplier credit balances to other payable invoices | NEXT-07, NEXT-57, NEXT-71 | — | [NEXT-91](../specs/next-76-100/packets/NEXT-91.md) |
| NEXT-92 | P2 | TREASURY | Documented bilateral receivable-payable setoff | NEXT-30, NEXT-07 | — | [NEXT-92](../specs/next-76-100/packets/NEXT-92.md) |
| NEXT-93 | P1 | EVIDENCE | Source-located evidence search and retained-page retrieval | NEXT-26, NEXT-50 | — | [NEXT-93](../specs/next-76-100/packets/NEXT-93.md) |
| NEXT-94 | P1 | EVIDENCE | Read-only mailbox intake and scoped attachment routing | NEXT-26 | — | [NEXT-94](../specs/next-76-100/packets/NEXT-94.md) |
| NEXT-95 | P1 | REVIEW | Counterparty balance confirmations with independent evidence | NEXT-13, NEXT-65 | — | [NEXT-95](../specs/next-76-100/packets/NEXT-95.md) |
| NEXT-96 | P1 | AUTHORITY | Multi-human approval routing and segregated review policies | existing core owners | NEXT-67 (budget classifications contribute to routing only, not permission to hide liabilities) | [NEXT-96](../specs/next-76-100/packets/NEXT-96.md) |
| NEXT-97 | P1 | BANKING | Exact covering-set reconciliation with explicit ambiguity | NEXT-09, NEXT-10 | NEXT-70 (the selected source is a structured bank file); NEXT-40 (native foreign-cash comparability is supported) | [NEXT-97](../specs/next-76-100/packets/NEXT-97.md) |
| NEXT-98 | P1 | REVIEW | Accountant period-review engagements and versioned acceptance | NEXT-13, NEXT-23, NEXT-25, NEXT-49, NEXT-50 | NEXT-95 (counterparty confirmations are part of the selected review evidence) | [NEXT-98](../specs/next-76-100/packets/NEXT-98.md) |
| NEXT-99 | P1 | CASH | Cash forecast vintage scoring and error attribution | NEXT-13, NEXT-45, NEXT-50 | — | [NEXT-99](../specs/next-76-100/packets/NEXT-99.md) |
| NEXT-100 | P1 | INTEGRATIONS | Scoped integration event subscriptions and delivery receipts | existing core owners | — | [NEXT-100](../specs/next-76-100/packets/NEXT-100.md) |

**Implementation status, fourth wave.** NEXT-97 has a bounded synthetic HTTP/browser delivery recorded in [next-packet-progress.md](next-packet-progress.md) and [its evidence](evidence/next-97-exact-covers.md). Other fourth-wave packets have no implementation state recorded here. Its suggested independent starts — evidence 93/94, contract changes 76, acquisition/commissioning 81, exact matching 97 — and its statement that the tax, grant, dividend, termination and lease profiles are "conditional capability extensions, not a demand to delay Book Zero" are the archive's own prioritisation. Selection follows the company and customer facts under [D-04](../open-decisions.md).

### Fifth wave: NEXT-101 … NEXT-125

Same shape as the fourth: `Requires` mixes prior-wave and same-wave contracts, and the archive states that only its own new-wave edges are checked, with no 125-node graph claim.

| ID | Priority | Lane | Solution | Requires | Conditional | Packet |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT-101 | P1 | IDENTITY | Accounting-firm delegation and multi-client workspaces | NEXT-50 | NEXT-98 (a client delegates a period-review engagement) | [NEXT-101](../specs/next-101-125/packets/NEXT-101.md) |
| NEXT-102 | P1 | EVIDENCE | Scoped evidence requests and response reconciliation | NEXT-26, NEXT-65, NEXT-93, NEXT-98 | NEXT-101 (the requester uses firm-to-client delegated access) | [NEXT-102](../specs/next-101-125/packets/NEXT-102.md) |
| NEXT-103 | P1 | REVIEW | Versioned balance-sheet substantiation schedules | NEXT-13, NEXT-23, NEXT-95, NEXT-98 | NEXT-102 (missing supporting evidence is requested from a client) | [NEXT-103](../specs/next-101-125/packets/NEXT-103.md) |
| NEXT-104 | P1 | REPORTING | Shared-cost attribution across projects and dimensions | NEXT-13, NEXT-14 | NEXT-43 (the analytical view uses reviewed classification revisions) | [NEXT-104](../specs/next-101-125/packets/NEXT-104.md) |
| NEXT-105 | P1 | REPORTING | Project margin with billing, recognition and cash bridges | NEXT-13, NEXT-58, NEXT-77, NEXT-79, NEXT-104 | NEXT-78 (milestone/retention balances enter the selected project) | [NEXT-105](../specs/next-101-125/packets/NEXT-105.md) |
| NEXT-106 | P1 | COMMERCE | Service-retainer entitlements and once-only drawdown | NEXT-56, NEXT-58, NEXT-76, NEXT-77 | — | [NEXT-106](../specs/next-101-125/packets/NEXT-106.md) |
| NEXT-107 | P2 | SCHEDULES | Onerous service-contract provisions and release on performance | NEXT-13, NEXT-76, NEXT-79, NEXT-105 | NEXT-42 (a related asset impairment assessment must precede contract-loss recognition) | [NEXT-107](../specs/next-101-125/packets/NEXT-107.md) |
| NEXT-108 | P2 | SCHEDULES | Warranty cohorts, expected claims and provision consumption | NEXT-03, NEXT-13, NEXT-51 | — | [NEXT-108](../specs/next-101-125/packets/NEXT-108.md) |
| NEXT-109 | P2 | COMMERCE | Insurance-loss claims and gross compensation accounting | NEXT-03, NEXT-13, NEXT-19 | — | [NEXT-109](../specs/next-101-125/packets/NEXT-109.md) |
| NEXT-110 | P2 | TREASURY | Borrowing reschedules, debt forgiveness and amended obligations | NEXT-32, NEXT-71 | NEXT-22 (a book gain or cost needs separate corporate-tax treatment) | [NEXT-110](../specs/next-101-125/packets/NEXT-110.md) |
| NEXT-111 | P1 | TAX | Annual common-cost VAT deduction true-up | NEXT-03, NEXT-04, NEXT-22, NEXT-49 | — | [NEXT-111](../specs/next-101-125/packets/NEXT-111.md) |
| NEXT-112 | P2 | TAX | Domestic construction reverse-charge sales and purchases | NEXT-03, NEXT-04, NEXT-15, NEXT-51 | — | [NEXT-112](../specs/next-101-125/packets/NEXT-112.md) |
| NEXT-113 | P2 | TAX | EU B2C destination VAT and Union OSS reporting | NEXT-51, NEXT-49 | NEXT-39 (proceeds arrive through a processor); NEXT-53 (a qualified goods supply rather than a service) | [NEXT-113](../specs/next-101-125/packets/NEXT-113.md) |
| NEXT-114 | P1 | TAX | EU foreign input-VAT recovery claims and receipts | NEXT-03, NEXT-49 | NEXT-17 (an approved foreign refund receivable needs supported FX settlement) | [NEXT-114](../specs/next-101-125/packets/NEXT-114.md) |
| NEXT-115 | P2 | PAYROLL | Overnight travel allowances and meal-benefit partition | NEXT-20, NEXT-21, NEXT-33 | NEXT-34 (the same retained trip also includes a mileage award) | [NEXT-115](../specs/next-101-125/packets/NEXT-115.md) |
| NEXT-116 | P2 | PAYROLL | Recurring car-benefit valuation and employee payment links | NEXT-20, NEXT-21, NEXT-35 | — | [NEXT-116](../specs/next-101-125/packets/NEXT-116.md) |
| NEXT-117 | P2 | TAX | Interest statements: KU20 and applicable KU25 identities | NEXT-32, NEXT-49 | NEXT-62 (received late-payment interest creates a reporting obligation) | [NEXT-117](../specs/next-101-125/packets/NEXT-117.md) |
| NEXT-118 | P2 | PAYROLL | Prospective salary exchange into pension contributions | NEXT-20, NEXT-21, NEXT-87 | NEXT-36 (an already paid or reported period needs a supported correction) | [NEXT-118](../specs/next-101-125/packets/NEXT-118.md) |
| NEXT-119 | P2 | EQUITY | Cash share subscriptions and registered-capital transition | NEXT-02, NEXT-13, NEXT-49, NEXT-89 | — | [NEXT-119](../specs/next-101-125/packets/NEXT-119.md) |
| NEXT-120 | P1 | TAX | Preliminary income-tax revisions and authoritative installment schedules | NEXT-22, NEXT-49 | NEXT-74 (linking final annual filing outcomes); NEXT-99 (scoring the retained estimate against actual outcomes) | [NEXT-120](../specs/next-101-125/packets/NEXT-120.md) |
| NEXT-121 | P1 | AGENT | Opt-in bounded standing posting mandates | NEXT-02, NEXT-03, NEXT-16, NEXT-96 | — | [NEXT-121](../specs/next-101-125/packets/NEXT-121.md) |
| NEXT-122 | P1 | TREASURY | Cash-constrained payment proposals with explicit optimization bounds | NEXT-71, NEXT-80 | NEXT-59 (installment promises define permitted partial payment options); NEXT-67 (reviewed spending policy contributes constraints); NEXT-99 (forecast accuracy informs separately reviewed assumptions) | [NEXT-122](../specs/next-101-125/packets/NEXT-122.md) |
| NEXT-123 | P1 | DELIVERY | Autogiro mandates and direct-debit collection outcomes | NEXT-30 | NEXT-59 (collecting contractually defined installments); NEXT-100 (publishing customer integration events) | [NEXT-123](../specs/next-101-125/packets/NEXT-123.md) |
| NEXT-124 | P1 | BANKING | Bank-feed provider handover with continuity evidence | NEXT-09, NEXT-10 | NEXT-70 (independent control from a supported structured statement); NEXT-97 (ambiguous grouped overlap needs candidate discovery) | [NEXT-124](../specs/next-101-125/packets/NEXT-124.md) |
| NEXT-125 | P1 | DELIVERY | Processor refund initiation with reserved entitlement and outcome recovery | NEXT-30, NEXT-39 | NEXT-64 (the original charge came through the invoice payment-link owner) | [NEXT-125](../specs/next-101-125/packets/NEXT-125.md) |

**Implementation status, fifth wave.** None. No fifth-wave packet has a row in [next-packet-progress.md](next-packet-progress.md), and this document creates no implementation state for one. Its recommended start — 101 through 105, then 106, then 122 and 124 — is the archive's own prioritisation; it states separately that specialist tax, provision, benefit and capital profiles should follow actual customer requirements, and that NEXT-121 should stay gated behind demonstrated deterministic preparation, authority and recovery behaviour rather than being enabled because the model appears confident. Selection follows the company and customer facts under [D-04](../open-decisions.md).

## Reserved work and non-overlap

The archives reserve the following owners. The reserved list is stated at their pinned revisions and must be re-resolved against the current tree before anything is consumed: this repository records [ADR 0010](../adr/0010-application-owned-accounting-replacement.md) as implemented, and the VAT control-reclassification slice as source-integrated but unapplied and runtime-unverified.

| Reservation | Owner scope | What a NEXT packet may do |
| --- | --- | --- |
| `WIP-VAT03` | VAT control reclassification and its qualification, including the 9120/9130 effect and recovery cases | Consume the released application owner. Do not repeat the qualification, and do not add a second reclassification owner. |
| `WIP-FX02-P1` | Paired FX partial settlement: principal release, residuals, realized gain/loss, replay | Consume the released pure release calculation and internal transaction mutation. Do not recreate the algorithm or a second FX register. |
| `WIP-AST03-UI` | Impairment UI, control and disposal base closure over 9150, including schedule and control views | Consume the final asset basis and released transaction ports after the owner handoff. |
| `WIP-VAT04-A1` | Obligation-owned VAT amendment financial delta | No second target-minus-prior owner. |
| `WIP-COM2-W1` | Webshop intake, raw order identity, catalog snapshots and order conversion capacity | Read-only order provenance only. Never modify its intake. |
| `APPLICATION-REPLACEMENT` | The application-owned migration, placeholder-operation closure and baseline proof | Every second-wave packet requires released owning slices first. |

No packet redoes VAT reclassification qualification, FX partial release, impairment UI closure, the VAT amendment delta or webshop intake. Historical migration numbers in the archives identify reserved scope only; they are never instructions to restore stored procedures or to allocate migration numbers.

The third wave adds no new reservation and releases none. It re-asserts the same non-overlap: do not repeat PDF extraction adapter work, credit rendering, SIE dimension repair, payroll run integration, Cash forecasting or the original VAT/FX/impairment work, and do not add a new lending or card platform, inventory engine, consolidation suite, alternative SQL workflow layer, arbitrary rule interpreter or separate job runtime. New source facts flow into the released owners' APIs.

The fifth wave also adds and releases no reservation, and is explicit that a new packet is a genuinely new behaviour in its delta, "not a renamed unfinished earlier integration": if equivalent code exists, extend and qualify that owner and report the actual remaining difference.

The fourth wave also adds and releases no reservation, and makes a sharper point about the existing ones: "Names/numbers identify the original reservations, not a claim they are still unfinished." [ADR 0010](../adr/0010-application-owned-accounting-replacement.md) records the application migration as implemented, and the VAT control-reclassification slice as source-integrated but unapplied and runtime-unverified, so every reservation in the table above must be re-resolved against the current tree rather than assumed either busy or free.

## Cross-owner contracts

The second wave states the concrete results one packet must hand another. Each row is a required result, not a second authority. A receiving worker checks actual exports rather than copying the illustrative names.

| Producer | Consumer | Required result |
| --- | --- | --- |
| NEXT-03 | 26, 31, 33, 38, 46 | Source-line recognition and tax-fact compiler, plus internal transaction creation and adoption |
| NEXT-15 | 30, 46 | Original line credit capacity, legal document identity and negative tax effects |
| NEXT-30 | 28, 39 | Customer-credit liability and refund capacity, distinct from unpaid receivables |
| Existing schedule/impairment owner | 31, 42 | Exact source basis, future occurrence lifecycle and approved internal transaction effects |
| NEXT-20/21 | 33–36 | Frozen earnings and tax computations, the already-recognized liability handoff, and actual paid/reporting identity |
| VAT owners | 37 | Effective role-signed reclassification and amendment vectors, plus the current obligation version |
| NEXT-38 | 23 | The complete cash-method unpaid-recognition population and the next-year no-duplicate settlement contract |
| FX owner and NEXT-17/18 | 40, 41 | Exact paired release and effective carrying/event history, without another obligation balance |
| NEXT-14/13 | 43–45 | Original classifications, fixed financial cutoffs and source-anchored contributions |
| NEXT-24 | 47, 48 | Immutable statement model, exact copy artifact and local validation basis |
| NEXT-47 | 48 | Purpose-specific signature evidence, not an authority-hosted certification event |
| Domain outcome owners | 49 | Typed same-scope prepared/submitted/accepted receipts, never free-text truth |
| Every released context adapter | 50 | Bounded coherent summary, complete counts, exact versions and an honest unavailable state |

Known shared-file and semantic conflicts are named in the second wave's `INTEGRATION-MAP.md`: treasury 39–41 must serialize cash and FX capacity projections; customer credit 30 and reminders 28 share customer state without owning each other's writes; payroll 33–36 must agree source-component and liability handoff identity before implementation; dimension restatement 43 may not change original-journal or SIE input meaning; signing 47 and filing 48 share artifact references but never substitute one signature purpose for another.

The third wave names five lanes instead of twenty-five concurrent writers, and the shared agreements it requires are these. Each is a required agreement between two owners, not a new authority:

| Shared agreement | Packets | Required result |
| --- | --- | --- |
| One multi-treatment invoice/credit representation | 51, 52, 53, 63 | A single sealed document holding per-line tax witnesses, allowance allocation, rounding effect and a versioned tax summary. Adding three new mutable tax ledgers is the failure this prevents. |
| One source-component and residual contract | 56, 58, 59, 60, 61, 62 | Advance application, service-period change, term change, cash discount and confirmed loss are different mutations of one native obligation. Reports may not each derive a different outstanding amount. |
| One residual contribution map | 64, 65, 71 | Payment links, the customer portal and bank transfers read the same current native residual and the same retained document bytes. |
| One bank-source admission | 70, 71 | Structured file decoding reuses the NEXT-10 admission owner instead of duplicating the provider sync windows, and a payment-file status authorizes no accounting inference beyond the bank's actual semantics. |
| One declaration/outcome substrate | 72, 73, 74 | VAT, AGI and INK2 dispatch share the durable attempt, artifact and outcome machinery with distinct mandates. A pending or unknown attempt cannot be duplicated with a new key to manufacture certainty. |

Its stated sequencing advice — begin with 51, 58, 68 and 70 where those profiles apply, then 52 and 55, then 64, 65, 71 and 72 — is the archive's own recommendation about ordinary commercial demand. This repository does not adopt it as a release order; selection follows the company and customer facts under [D-04](../open-decisions.md).

The fourth wave states the same rule against its own graph: no mandatory dependency is created on an optional profile merely because it shares a module. Its named examples are exact — 97 may use existing booked native bank data without enabling a new bank-file importer, 98 need not require a counterparty confirmation for every engagement, 99 consumes an existing Cash forecast rather than forcing any tax strategy, and 83 does not wait for a finance-lease model. Each of those is a decision this repository endorses, because each prevents an optional profile from becoming a launch gate.

The fourth wave's cross-owner table names thirteen producer/consumer agreements. The three that carry the most risk of a second owner are these:

| Shared agreement | Packets | Required preserved meaning |
| --- | --- | --- |
| One order/invoice owner | 76–79 | Stable accepted component identities, draft reservations, once-only issue and credit history across contract change, time billing, milestones and unbilled earnings |
| One asset and tax-bridge pair | 81–85 | Book versus tax basis, and a tax bridge stage that is an input rather than a circular final-close prerequisite |
| One approval authority | 96, 100 | Exact quorum-set semantics supported by a new explicit contract rather than forged legacy approval, and a minimal versioned public event with current subscriber authority and durable economic idempotency |

The fifth wave's cross-owner table is again about preserved meaning rather than new ledgers. The two agreements that matter most are that a delegated accountant's access never becomes financial authority over another client's book, and that a pending processor or bank outcome never authorizes a replacement payment:

| Shared agreement | Packets | Required preserved meaning |
| --- | --- | --- |
| One access/authority boundary | 101, 102, 103, 121 | Client-approved access intersected with firm roles, never cross-book financial authority, and no unattended posting; the existing human approval remains the financial authority |
| One money-movement source owner | 122, 123, 124, 125 | Actual source evidence for cash, collections, provider handover and refunds stays with the existing intake, instruction, allocation and processor owners; a proposal, a consent, a status or a pending outcome is not a movement |

## Proposed mapping to the maintained owners

This table is a **reading aid derived from packet titles, the archives' stated existing owners and the plans' own coverage**. It is not a verified reconciliation: confirm it against the actual checkout and the owning plan section before treating a row as an assignment. Its purpose is to stop an agent from inventing a second owner for work the plans already own, and to make the genuinely uncovered items visible.

`Plan` names the maintained packet or supplemental section. `PRY` names a parity packet that carries the rule classification or reference logic for the same requirement. `Dossier value` says what the packet contributes beyond the requirement.

| NEXT | Plan owner | PRY | Dossier value |
| --- | --- | --- | --- |
| NEXT-01 | PST-05, FND-02 | — | Read-only current-owner resolution for case review, with the ownership-refusal execution case |
| NEXT-02 | FND-03 | — | Capability-specific company admission as one non-journal transaction with its receipt |
| NEXT-03 | PUR-1, IMP-02, VAT-01 | PRY-58 | Purchase journal, payable, source recognition and tax facts as one transaction group |
| NEXT-04 | VAT-01, VAT-02 | PRY-55, PRY-56, PRY-57 | Consistent capture, pure box calculation, immutable snapshot and independent controls |
| NEXT-05 | VAT-01 | PRY-47, PRY-11 | Cross-border service purchase treatment behind an explicit general-rule profile |
| NEXT-06 | COM-04, EXP-1 | — | Owner-paid expense, reimbursement and funding effects in one group |
| NEXT-07 | COM-04, PUR-2 | — | Supplier paid credit and refund receipts, reusing the shared line-credit math |
| NEXT-08 | COM-03, PRY-18 | PRY-18, PRY-24 | Instruction resolution, dispatch fencing and replacement as distinct states |
| NEXT-09 | IMP-02, BANK-2 | PRY-02, PRY-09 | Complete sync windows, claim/page/publication transactions and out-of-order recovery |
| NEXT-10 | IMP-04, BANK-1 | — | Provider revisions to already reviewed bank observations, without automatic posting |
| NEXT-11 | END-06 | PRY-32 | Separate complete-book SIE4E export distinct from the movement-transfer export |
| NEXT-12 | COM-06, IMP-06 | — | Historical open-item adoption without new recognition, with pool assignment |
| NEXT-13 | END-03 | — | Immutable semantic P&L and balance-sheet snapshot membership and calculation |
| NEXT-14 | DIM-1, DIM-2, DIM-3 | — | Original dimension assignments written in the same transaction as the journal lines |
| NEXT-15 | COM-04 | PRY-45 | Legal customer credit note: number series, journal, receivable reduction, tax facts, artifact |
| NEXT-16 | PST-05, END-01 | — | Evidence-aware period preparation with run checkpoints and idempotent recovery |
| NEXT-17 | FX-02 | — | Payable FX and explicit fees against the reserved paired-release owner |
| NEXT-18 | FX-03 | — | Incremental open-item remeasurement as one carrying-change group |
| NEXT-19 | AST-03 | — | Disposal with proceeds, retiring the schedule in the same transaction |
| NEXT-20 | PAY-02 | PRY-60, PRY-61 | Frozen regular-payroll calculation with no financial effect until run execution |
| NEXT-21 | PAY-03, PAY-04 | PRY-59, PRY-72 | Run, correction and payment groups, payslip and AGI artifact generation in Bun jobs |
| NEXT-22 | END-04, TAX-1 | — | Pre-close tax bridge and INK2/SRU lineage separated from the bridge journal |
| NEXT-23 | END-02 | — | Transfer, financial certificate, next opening, locks and receipt in one transaction |
| NEXT-24 | END-05, END-06 | — | K2 semantic model and iXBRL with atomic final approval and deferred native validation |
| NEXT-25 | OPS-02, OPS-05 | — | Fixed-revision rehearsal across the real application boundary with quarantined restore |
| NEXT-26 | [Supplier inbox and extraction](capability-backlog.md#supplier-inbox-and-extraction), IMP-01, AGT-2 | PRY-75, PRY-76, PRY-77, PRY-80 | Bounded extraction lifecycle, safe reprocessing and the three-way reviewed merge |
| NEXT-27 | [Party master data](capability-backlog.md#party-master-data), COM-01 | PRY-11 | Reviewed identity resolution in a retained overlay, explicitly refusing balance merging |
| NEXT-28 | [Collections](capability-backlog.md#collections), SALES-3 | PRY-14, PRY-49 | Exact-message approval, dispatch admission and honest recovery of an ambiguous send |
| NEXT-29 | [Recurring invoices](capability-backlog.md#recurring-invoices-and-rotrut), COM-02, PST-05 | PRY-46 | Occurrence identity independent of template revision, with no duplicate billing |
| NEXT-30 | COM-03, COM-04 | PRY-45 | Customer credit as its own liability: unapplied cash, paid credits, refunds, corrections |
| NEXT-31 | AST-02, COM-02 | PRY-52 | Invoice-linked prepayments and accrued-cost true-up over the existing schedule owner |
| NEXT-32 | **unmapped — see gaps** | — | Loan principal, interest accrual and repayment allocation lifecycle |
| NEXT-33 | [Expenses and payroll handoffs](capability-backlog.md#expenses-and-payroll-handoffs), EXP-1 | — | Employee claim submission and review with an exclusive payroll or direct-payment handoff |
| NEXT-34 | EXP-2 | PRY-70 | Distance-based reimbursement with entitlement, tax-free limit and taxable excess kept distinct |
| NEXT-35 | PAY-02 | PRY-60, PRY-64, PRY-65, PRY-67 | One selected variable/absence profile plus a holiday-liability rollforward |
| NEXT-36 | PAY-03 | PRY-59 | Paid-payroll recovery and retroactive compensation after actual payment |
| NEXT-37 | VAT-03, VAT-04 | PRY-06 | Authority assessment lifecycle and the exact-to-assessed bridge, without repeating reserved owners |
| NEXT-38 | COM-02, END-02 | PRY-50 | Cash-method recognition and once-only year-end unpaid capture with source coverage |
| NEXT-39 | [Additional breadth](capability-backlog.md#additional-breadth-retained-under-existing-owners), INT-1, COM-2 | PRY-03 | Processor gross-event clearing, fees, refunds and payout transit instead of net payout revenue |
| NEXT-40 | FX-02, FX-05 | PRY-10, PRY-20 | Native foreign-currency cash holdings and transfers as a capacity distinct from foreign obligations |
| NEXT-41 | FX-03 | — | Bounded chain-adjustment repair for a valuation corrected after settlement consumed the basis |
| NEXT-42 | AST-03 | — | Economic reversal with a counterfactual cap and an explicit zero-carrying-but-owned state |
| NEXT-43 | DIM-4, DIM-5 | — | Reviewed classification overlay with its own cutoff; original tags and amounts never change |
| NEXT-44 | IMP-02, END-06 | PRY-26 | Multi-year SIE partition and dimension-preserving import with explicit loss diagnostics |
| NEXT-45 | END-03, REP-1 | — | Direct cash-flow statement whose bridge explains the entire closing balance change |
| NEXT-46 | INT-1 | PRY-12, PRY-13 | One selected Peppol access point, with inbound review distinct from posting |
| NEXT-47 | END-07, STAT-3 | PRY-15 | Purpose-bound document signature evidence over an exact content manifest |
| NEXT-48 | END-07, STAT-3 | — | Bolagsverket filing lifecycle keeping signature, copy certification, upload and registration distinct |
| NEXT-49 | [Deadlines and calendar](capability-backlog.md#deadlines-and-calendar), END-07 | PRY-82, PRY-83 | Rule-change impact inventory and typed fulfillment receipts instead of a nonempty reference string |
| NEXT-50 | AGT-2, [agent context](../operations.md#governed-rules-and-agent-context) | — | Cross-domain context snapshot, delta semantics and an honest unavailable state |

The third wave maps the same way. Its own `INTEGRATION-MAP.md` crosswalk supplies the source requirement and canonical owner for every packet; the rows below restate it against this repository's plan identifiers. The same caution applies: derived from the archive's crosswalk and the plans' own coverage, **not** verified against the checkout.

| NEXT | Plan owner | PRY | Dossier value |
| --- | --- | --- | --- |
| NEXT-51 | COM-02, VAT-01, VAT-2 | PRY-47, PRY-51, PRY-55 | Reduced, exempt and mixed-rate documents plus inclusive-price backout on the existing domestic issue owner, not a second issue engine |
| NEXT-52 | COM-02, VAT-1, VAT-2 | PRY-47, PRY-11 | Sale-side general-rule B2B services, distinct from the NEXT-05 purchase side |
| NEXT-53 | COM-02, VAT-1, VAT-2 | PRY-47, PRY-55, PRY-56 | Intra-EU goods acquisition and supply; goods treatment is not inferred from the service profile |
| NEXT-54 | PUR-1, VAT-2 | PRY-55, PRY-56 | Customs assessment delta and landed-cost attribution over purchase recognition, without inventory custody |
| NEXT-55 | VAT-2, VAT-4, END-07 | — | EU sales-statement artifact and correction membership, distinct from the ordinary VAT return |
| NEXT-56 | COM-02, COM-03, COM-04 | — | Customer advance as its own liability with its own tax timing, distinct from NEXT-30 overpayment |
| NEXT-57 | COM-02, COM-03, PUR-2 | — | Supplier cash prepayment, distinct from NEXT-31 cost deferral and from crediting an unrecognized purchase |
| NEXT-58 | COM-04, AST-02 | PRY-52 | Invoice-driven revenue deferral with a service interval, distinct from prepaid cost and billing date |
| NEXT-59 | COM-03, COM-06 | — | Installment partitioning and non-legal payment promises over one native obligation |
| NEXT-60 | COM-03, COM-04, IMP-05 | PRY-34, PRY-51 | An evidenced cause for each settlement difference instead of a size-based tolerance plug |
| NEXT-61 | COM-04, COM-06, VAT-04 | — | Book allowance, confirmed loss with VAT relief, and later recovery as three distinct states |
| NEXT-62 | [Collections](capability-backlog.md#collections) | PRY-49 | A qualified monetary interest and reminder-fee claim; the collections backlog already requires a separately reviewed treatment rather than an inferred charge |
| NEXT-63 | COM-02, COM-04 | PRY-48 | Buyer-issued sale acceptance that preserves external numbering and the seller's own revenue owner |
| NEXT-64 | COM-03, INT-1 | PRY-131 | A payment link bound to the issued invoice identity, never a second invoice |
| NEXT-65 | COM-05, COM-06, DOC-1, INT-2 | PRY-53 | Customer-facing constrained artifact and current-balance access; the statement artifact with a revocable scoped link is already owned by PRY-53 |
| NEXT-66 | PUR-3, COM-02, IMP-05 | — | Commitment and acceptance records that precede AP, without a warehouse or a second accrual owner |
| NEXT-67 | **unmapped — see gaps** | — | Discretionary commitment control with stop/warn decisions; see the gap table below |
| NEXT-68 | FND-03, IMP-01, VAT-1, END-03 | PRY-24, PRY-30, PRY-99 | Versioned BAS chart adoption with stable native identities; PRY-99 already owns the versioned reference chart and its per-book seeding |
| NEXT-69 | [Party master data](capability-backlog.md#party-master-data), COM-01 | PRY-27, PRY-28 | Staged spreadsheet master-data reconciliation, distinct from financial-history import |
| NEXT-70 | BANK-1, IMP-01, IMP-03, IMP-04 | PRY-08 | Structured bank-file decoding and entry lineage through the existing admission owner |
| NEXT-71 | PUR-2, COM-03, INT-1 | PRY-08 | A qualified bank payment format and status channel around the existing export and instruction owners |
| NEXT-72 | VAT-4, END-07, INT-1 | PRY-57 | Declaration dispatch and authoritative return history, distinct from NEXT-04 calculation and NEXT-37 assessment |
| NEXT-73 | PAY-04, END-07, INT-1 | — | AGI submission and correction outcomes consuming the payroll owner's output |
| NEXT-74 | TAX-1, END-06, END-07, INT-1 | — | Income-tax filing and signature over NEXT-22 fields, distinct from NEXT-48 annual-report registration |
| NEXT-75 | FND-03, COM-02, VAT-1, END-02 | — | A reviewed cash/accrual transition as one controlled activation; see the gap table below |

The fourth wave's own `INTEGRATION-MAP.md` supplies a per-packet "new versus already designed" statement rather than a source-requirement crosswalk, so its rows below are mapped against this repository's plan identifiers from packet titles, stated existing owners and the plans' coverage. The same caution applies: **not** verified against the checkout.

| NEXT | Plan owner | PRY | Dossier value |
| --- | --- | --- | --- |
| NEXT-76 | [Sales operations](capability-backlog.md#sales-operations), COM-02 | — | Reviewed post-acceptance scope/price change with billing-capacity conservation; the sales-operations backlog already requires per-line converted capacity consumed once |
| NEXT-77 | **unmapped — see gaps** | — | Reviewed billable work capture converted into invoice lines; see the gap table below |
| NEXT-78 | **unmapped — see gaps** | — | Delivered-milestone acceptance and retained contract consideration; see the gap table below |
| NEXT-79 | **unmapped — see gaps** | — | Earned-but-unbilled recognition before issue, the opposite timing direction to NEXT-58; see the gap table below |
| NEXT-80 | **unmapped — see gaps** | — | Supplier-side documentary dispute and bounded payment hold; the collections backlog owns the customer side only |
| NEXT-81 | AST-01, AST-02 | — | Multi-source construction accumulation and an explicit ready-for-use transition; [ADR 0008](../adr/0008-financial-fx-vat-impairment.md) already records broader asset classes as scoped follow-up |
| NEXT-82 | AST-03 | — | Separately supported component replacement and improvement; whole-asset disposal and impairment stay unchanged |
| NEXT-83 | **unmapped — see gaps** | — | Contract-owned operating-rental commitments and deposit recovery; see the gap table below |
| NEXT-84 | **unmapped — see gaps** | — | Book-to-tax depreciation cohorts; see the gap table below |
| NEXT-85 | **unmapped — see gaps** | — | Periodiseringsfond cohorts and reversals; see the gap table below |
| NEXT-86 | [ROT/RUT](capability-backlog.md#recurring-invoices-and-rotrut), COM-02 | — | The household-work profile the conditional sales/tax section already requires, with split obligors and claim/rejection recovery |
| NEXT-87 | **unmapped — see gaps** | — | Pension provider charge reconciliation and the separate SLP basis; see the gap table below |
| NEXT-88 | PAY-02, PAY-03, PAY-04 | — | The payroll plan already lists termination and retroactive corrections in scope; this adds the final-pay inventory and closure event |
| NEXT-89 | **unmapped — see gaps** | — | Company-side dividend lifecycle with resolution evidence and KU31; see the gap table below |
| NEXT-90 | **unmapped — see gaps** | — | Grant lifecycle as earned funding and repayment obligation; the archive itself calls it a proposed accounting expansion |
| NEXT-91 | COM-03, PUR-2 | — | Noncash application of an established supplier credit asset to another invoice, consuming shared ageing and payment readers once |
| NEXT-92 | **unmapped — see gaps** | — | Documented same-counterparty AR/AP discharge without cash; see the gap table below |
| NEXT-93 | DOC-1, AGT-2 | — | A searchable located projection over retained originals; the document backlog owns archive search at document level, not exact source locators |
| NEXT-94 | [Supplier inbox and extraction](capability-backlog.md#supplier-inbox-and-extraction) | — | The real inbound-email channel the inbox backlog already requires, without replacing uploads, extraction or reviewed drafts |
| NEXT-95 | **unmapped — see gaps** | — | Counterparty balance confirmation requests and difference investigation; see the gap table below |
| NEXT-96 | [Shared contracts](00-shared-contracts.md), IAM-1 | — | Finite versioned multi-reviewer quorum routing; the shared-contracts separation-of-powers clause already requires configurable preparer/reviewer separation |
| NEXT-97 | IMP-05, BANK-1 | PRY-33 | Bounded one-to-many covering-set discovery; PRY-33 already owns covering-set detection and reviewed one-to-many confirmation |
| NEXT-98 | [Book Zero review](15-book-zero-workflow-cash.md), NEXT-25, REL-1 | — | The collaborative accountant-review workflow around the review outcome Book Zero already owns, not a second close certificate |
| NEXT-99 | [Cash forecast](15-book-zero-workflow-cash.md) | — | Retrospective scoring of saved forecast vintages with error attribution, not a second forecasting engine |
| NEXT-100 | INT-1, AGT-1 | — | A concrete read-only outbound event subscription with delivery receipts; existing outbox jobs are internal delivery, not a client-facing contract |

The fifth wave maps mostly onto owners this repository already has, which is a favourable result. Its `INTEGRATION-MAP.md` supplies "new versus already designed" statements rather than a source-requirement crosswalk, so the rows below are mapped against plan identifiers from packet titles, stated existing owners and the plans' coverage — the same caution applies: **not** verified against the checkout.

| NEXT | Plan owner | PRY | Dossier value |
| --- | --- | --- | --- |
| NEXT-101 | IAM-1, [shared contracts](00-shared-contracts.md) | — | Client-approved delegation intersected with firm roles and separate client cutoffs; IAM-1 already owns firm/client boundaries and the firm workflow, so this is a delta on an owned requirement |
| NEXT-102 | AGT-2, [Supplier inbox](capability-backlog.md#supplier-inbox-and-extraction) | — | A scoped request/response loop connecting a reviewed answer to the original accounting question; the operations plan already permits agent-raised questions, and uploading a file is not an answer |
| NEXT-103 | REP-2, REP-3 | — | Substantiation of selected balances through exact ledger components, independent evidence and reconciling items |
| NEXT-104 | FND, DIM-4 | PRY-104 | Allocation across projects/dimensions with exact residual conservation; PRY-104 already owns the exact proportional-allocation algorithm |
| NEXT-105 | END-03, REP-1 | — | A margin view reconciling billed, earned, unbilled, deferred, cost and cash; it compounds the unowned project-billing gaps (NEXT-77/78/79) rather than adding a new one |
| NEXT-106 | COM-04, AST-02 | — | Prepaid service units consumed once against existing deferred consideration; compounds the same project-billing gap |
| NEXT-107 | **unmapped — see gaps** | — | Onerous contract provisions; ADR 0008 records broader asset classes as follow-up, but a contract-loss liability provision is a different case |
| NEXT-108 | **unmapped — see gaps** | — | Warranty cohorts and claim consumption; see the gap table below |
| NEXT-109 | **unmapped — see gaps** | — | Insurance loss, recovery entitlement and insurer settlement; see the gap table below |
| NEXT-110 | **compounds NEXT-32** | — | Reschedules and debt forgiveness on the loan lifecycle this plan already records as unowned |
| NEXT-111 | **unmapped — see gaps** | — | Annual common-cost deduction true-up; see the gap table below |
| NEXT-112 | VAT-1, VAT-2 | PRY-47 | The VAT treatment matrix already names domestic reverse charge; this is the construction-specific buyer evidence, notice and reporting profile |
| NEXT-113 | **unmapped — see gaps** | — | B2C destination VAT and a separate OSS obligation; see the gap table below |
| NEXT-114 | **unmapped — see gaps** | — | Moving from retained foreign-tax evidence to a recovery claim and refund; see the gap table below |
| NEXT-115 | EXP-2, PAY-02 | PRY-70 | Allowance entitlement, tax-exempt limits and meal reductions partitioned from taxable benefit; PRY-70 already owns per-diem, meal deductions and mileage rates |
| NEXT-116 | **unmapped — see gaps** | — | Recurring car-benefit valuation; see the gap table below |
| NEXT-117 | **unmapped — see gaps** | — | KU20/KU25 interest-statement identities; see the gap table below |
| NEXT-118 | PAY-02, PAY-04 | PRY-70 | Prospective salary exchange; PRY-70 already owns the factor, income and contribution thresholds and the employer pension cap |
| NEXT-119 | **unmapped — see gaps** | — | Share subscription stages up to registered capital; see the gap table below |
| NEXT-120 | TAX-1, END-07 | PRY-69 | Preliminary-tax status and installment decisions kept distinct from actual tax-account events; PRY-69 already owns the preliminary-tax status |
| NEXT-121 | [Operations](../operations.md), E-17 | — | **Already specified.** The operations plan states the mandate scope, cumulative limits, atomic budget consumption and the rule that a mandate never implicitly authorizes payment, closure, signature or filing, and already places unattended posting outside the Book Zero delivery. This packet needs an authorization decision, not an owner |
| NEXT-122 | [Book Zero Cash](15-book-zero-workflow-cash.md), COM-03 | — | A bounded payment proposal with honest optimality, feasibility and search-exhaustion outcomes; it may only offer partial payment where the existing contractual owner supplies that option |
| NEXT-123 | **unmapped — see gaps** | — | Autogiro consent, authority, instruction and returned-payment outcomes; see the gap table below |
| NEXT-124 | BANK-2, IMP-02 | — | Provider handover for one account with reviewed overlap and no duplicate transactions or openings; BANK-2 already owns feed coverage, cursors and recovery |
| NEXT-125 | NEXT-39, NEXT-30, COM-03 | — | Refund entitlement reserved across a processor transit stage; the existing processor clearing, customer-credit and allocation owners supply the movement |


## Product scope: dispositioned and still open

These packets describe lifecycles the maintained plans name only as follow-up work, or do not name at all. They are recorded here rather than added to the 53-packet index, because adding them would change a reviewed denominator on the strength of an external design input.

**23 of these were dispositioned on 2026-09-28** by the [owner-delegated decision pass](../adr/0015-owner-delegated-decision-pass.md). The full record is [the vendored decision pass](../specs/decision-pass-2026-09-28/README.md); the dispositions are reproduced in the table below. The remaining eleven are carried forward **open** in their own table, because the pass predates the fifth dossier wave.

A disposition is a **product decision, not an implementation state**. Dispositioned does not mean designed, implemented, runtime-observed, company-qualified or externally accepted. The historical core denominator and every identifier are unchanged, and `NEXT-nn` remains a work namespace.

| Disposition | Meaning | Identifiers |
| --- | --- | --- |
| `adopt_conditional_accounting` | Adopted as a bounded accounting capability. The selected company's actual case decides whether it is required for that release. It is not optional forever, and it is no longer a question about whether the product should support it. | NEXT-32, 40, 42, 55, 61, 79, 80, 84, 85, 87, 89 |
| `adopt_correction_envelope` | Adopted as a correction capability attached to the **existing** FX and payroll owners. No second generic correction engine and no second financial register. | NEXT-36, 41 |
| `adopt_optional_product` | Adopted as product work, sequenced later. It does not all precede the first usable accounting period. | NEXT-45, 66, 67, 75, 77, 78, 92, 95 |
| `adopt_limited_profile` | Adopted within a stated boundary. Operating-rental support does **not** adopt finance-lease or right-of-use scope; that broader engine is excluded from the first-release decision. | NEXT-83 |
| `defer_product_expansion` | Deferred beyond the first release. This is **not** permission to ignore a real transaction or to invent another human signature. An actual unsupported case remains visible. | NEXT-90, 96 |

Two rules bind every disposition above. A positive workflow may not be advertised without a clearly supported correction boundary and a truthful refusal and recovery path for cases outside it. And current valid code in a deferred module is retained — no deletion is required merely to align the roadmap.

### Still open: eleven capabilities the decision pass does not reach

The pass dispositions 23 capabilities, which correspond exactly to the gaps surfaced by the first four dossier waves. The fifth wave added eleven more and the pass does not mention them. They are **not** decided by [ADR 0015](../adr/0015-owner-delegated-decision-pass.md), and an agent must not read its silence as a decision.

### From the first two waves — dispositioned

| Packet | What the maintained plans did not own | Disposition (2026-09-28) |
| --- | --- | --- |
| NEXT-32 loan lifecycle | No maintained packet or capability label covers loan principal, interest accrual or repayment allocation. NEXT-06 owns owner funding only, and capital contributions must not become loans. | **`adopt_conditional_accounting`** — Ordinary documented borrowing, principal, interest and repayment. No lending product. Required when the selected company period actually contains it. |
| NEXT-41 late FX chain repair | FX-03 owns period remeasurement; the first wave explicitly refuses revaluation after settlement consumed the old basis. | **`adopt_correction_envelope`** — Bounded chain repair where settlement already consumed the basis, attached to the reserved FX owner. No second FX register or algorithm. |
| NEXT-42 economic impairment reversal | [ADR 0008](../adr/0008-financial-fx-vat-impairment.md) adopts the impairment contract with positive remaining carrying and a bounded immediate error correction; economic reversal and broader asset classes remain scoped follow-up. | **`adopt_conditional_accounting`** — Economic reversal of an existing adopted impairment contract, with the qualified without-impairment cap and residual schedule still D-08 inputs. |
| NEXT-40 foreign cash holdings | FX packets own foreign obligations. Native foreign-currency cash balances and transfers are a second, distinct capacity. | **`adopt_conditional_accounting`** — Native foreign-currency cash holdings and transfers, distinct from foreign obligations. Applicability is a company fact. |
| NEXT-45 direct cash-flow statement | REP-1 names cash flow as a capability and END-03 covers P&L, balance sheet and openings; no packet owns a cash-flow statement with a reconciliation bridge. | **`adopt_optional_product`** — A direct cash-flow statement with a full reconciliation bridge over owned relationships, and a reviewed cash perimeter and classification policy. |
| NEXT-36 paid payroll recovery | PAY-03 owns frozen-run posting and correction; the first wave's correction is bounded to an unpaid run. Recovery or future-pay adjustment after actual payment is a different financial case. | **`adopt_correction_envelope`** — Recovery or future-pay adjustment after actual payment, attached to the existing payroll owner. Needs an enforceable legal basis and a case-specific declaration treatment. |

### Surfaced by the third wave — dispositioned

A title-and-text search of the maintained plans, the capability backlog and the parity backlog on 2026-09-28 found no owner for the lifecycles below. This is the search that was run and its date, not a verified absence claim: confirm against the checkout before acting on it. Each row's disposition is a product decision from 2026-09-28 and does not change that caution.

| Packet | What the maintained plans did not own | Disposition (2026-09-28) |
| --- | --- | --- |
| NEXT-55 EU sales statement (periodisk sammanställning) | No maintained plan, capability label or `PRY-nn` row names the EU sales list or its correction history. VAT-2 owns the domestic return boxes; an EU sales statement is a different artifact with a different cadence. | **`adopt_conditional_accounting`** — EU sales statement artifact and correction membership, distinct from the domestic VAT return. Reviewed statement schema, threshold and cadence are D-08 inputs. |
| NEXT-61 receivable allowance, confirmed loss and recovery | No maintained owner covers a book allowance that reduces valuation without forgiving the legal claim, a confirmed loss with VAT relief, or later recovery of a written-off balance. The collections backlog owns disputes and follow-up, not valuation. | **`adopt_conditional_accounting`** — Book allowance, confirmed loss with VAT relief, and later recovery as three distinct states. Reviewed measurement basis is a D-08 input. |
| NEXT-66 purchase commitments and three-way matching | PUR-3 owns linking purchase evidence to invoices and reconciling AP to ledger controls. It does not own order-level commitment records, acceptance state or a three-way match decision. | **`adopt_optional_product`** — Commitment and acceptance records that precede AP. A commitment must never become duplicated actual spend, and a real supplier obligation is still recorded. |
| NEXT-67 commitment-aware budgets | No maintained packet, capability label or parity row owns budgets, budget periods or a stop/warn authorization decision. The only budget language in the plans is a provider call budget and an unrelated concurrency allowance. | **`adopt_optional_product`** — Discretionary commitment control with stop/warn decisions. A hard stop applies to discretionary commitments only, never to recording an existing obligation. |
| NEXT-75 accounting-method change | NEXT-38 owns ordinary cash-method recognition events and PRY-50 owns the cash-method profile. A reviewed **transition** between methods — with conserved recognition coverage and one controlled activation — is a different case, and D-04 records the method itself only as a company fact. | **`adopt_optional_product`** — A reviewed cash/accrual transition as one controlled activation with conserved recognition coverage. Not a general method switch. |

### Surfaced by the fourth wave — dispositioned

The same dated search, repeated on 2026-09-28 over the maintained plans, the capability backlog and the parity backlog. The fourth wave is broader than the third: its conditional profiles are mostly tax, payroll, equity and grant lifecycles, and the search found no owner for most of them. Again this is the search that was run and its date, not a verified absence claim, and again each is recorded rather than adopted.

| Packet | What the search did not find | Decision required |
| --- | --- | --- |
| NEXT-77/78 project billing | The sales-operations backlog owns quotes, orders and conversion with once-only converted capacity. Nothing owns reviewed billable work capture, delivered-milestone acceptance, or retention money held on a customer contract. | **`adopt_optional_product`** — billable work capture, milestone acceptance and retained consideration, requiring actual service-contract needs. An invoice installment does not prove a milestone occurred. |
| NEXT-79 earned but unbilled revenue | Nothing owns revenue recognised before an invoice exists. NEXT-58 defers **invoiced** revenue, the opposite timing direction, and a search for "unbilled", "contract asset" and "accrued revenue" returned nothing. | **`adopt_conditional_accounting`** — Earned-but-unbilled recognition before issue, sharing one source-component contract with the NEXT-58 deferral owner. |
| NEXT-80 supplier-side disputes and payment holds | The collections backlog owns customer disputes, statements and follow-up. Nothing owns a supplier-side documentary dispute or a bounded hold that releases part of a payable. | **`adopt_conditional_accounting`** — Supplier-side documentary dispute and bounded payment hold against the existing payment-instruction owner. |
| NEXT-83 operating leases and right-of-use | No maintained plan, capability label or parity row mentions operating leases, finance leases or right-of-use assets. | **`adopt_limited_profile`** — Contract-owned operating-rental commitments and deposit recovery. **Excludes** finance-lease and right-of-use asset scope. |
| NEXT-84 book-to-tax depreciation | AST-02 owns book schedules and END-04 owns the tax bridge. Nothing owns a tax-value basis separate from the book basis, tax-depreciation cohorts or an excess-depreciation carry-forward. | **`adopt_conditional_accounting`** — A tax-value basis separate from the book basis, tax-depreciation cohorts and excess-depreciation carry-forward. The basis rule is a D-08 input. |
| NEXT-85 periodiseringsfond | Nothing in the maintained plans names tax allocation reserves, their deadlines, cohort history or reversals. | **`adopt_conditional_accounting`** — Tax allocation reserve cohorts, deadlines, reversals and annual tax linkage. Applicability is a company fact. |
| NEXT-87 pension reconciliation and SLP | The payroll plan names pensions and collective-agreement obligations as explicit **company inputs**, but owns no provider-charge reconciliation, no reconciliation against an accrued provision and no special-payroll-tax basis. | **`adopt_conditional_accounting`** — Pension provider charges reconciled against the accrued obligation, plus the separate special-payroll-tax basis. |
| NEXT-89 dividends and KU31 | Nothing in the maintained plans owns a dividend resolution, shareholder entitlement, shareholder payable or the KU31 issuer report. NEXT-06 owns owner funding and reimbursement, which the archive correctly says is a different thing. | **`adopt_conditional_accounting`** — Company-side dividend resolution, shareholder entitlement, payable and the KU31 issuer report. Separate from owner expense reimbursement. |
| NEXT-90 grants | Nothing in the maintained plans owns grant accounting. The only "grant" language is a prohibition on treating an email sender or source instruction as authority. The archive states plainly that this is "a proposed accounting expansion, not a finding that a current grant implementation is defective". | **`defer_product_expansion`** — Deferred beyond the first release. An actual grant transaction is not ignored and no assumption is invented; current valid code is retained. |
| NEXT-92 bilateral setoff | Nothing in the maintained plans owns same-counterparty AR/AP discharge without cash. NEXT-30 customer credit and NEXT-07/57 supplier refunds are different operations. | **`adopt_optional_product`** — Documented same-counterparty AR/AP discharge without cash, with the agreement and legal basis as evidence. |
| NEXT-95 counterparty confirmations | Nothing in the maintained plans owns requesting a customer or supplier to confirm a frozen balance or investigating the difference. PRY-14 is outbound email delivery, not confirmation evidence. | **`adopt_optional_product`** — Counterparty confirmation requests and difference investigation. Not an audit-certification claim. |
| NEXT-96 multi-reviewer quorum | The shared-contracts separation-of-powers clause already requires configurable preparer/reviewer separation and explicitly does not claim two-person review where one operator is permitted. Nothing owns a finite, versioned quorum set over an exact plan. | **`defer_product_expansion`** — Deferred beyond the first release: there is one operator. Never unattended posting or an agent mandate, and no second signature is invented. |
### Surfaced by the fifth wave — still open

The same dated search, repeated on 2026-09-28. This wave maps better than the third and fourth — most of it lands on owners this repository already has, and NEXT-121 turns out to be design for a contract [the operations plan](../operations.md) has already adopted. What remains unowned is a set of liability, tax and capital lifecycles, plus three that compound gaps already recorded above rather than adding new decisions.

| Packet | What the search did not find | Decision required |
| --- | --- | --- |
| NEXT-103 balance-sheet substantiation | REP-2 owns register and accountant reports and REP-3 owns retained report bytes. Nothing owns explaining a selected balance through exact ledger components plus independent supporting evidence and reconciling items. | Whether substantiation schedules are a product capability or a reviewer's own working paper. If in scope, they need a pinned cutoff and an honest statement of what is not substantiated. |
| NEXT-107 onerous contract provisions | No maintained plan, capability label or parity row names contract-loss provisions. ADR 0008 records *asset* impairment; a liability provision for an onerous contract is a different case. | Whether the company has onerous contracts, and the qualified measurement and release basis. Its own rule that an asset impairment assessment must precede contract-loss recognition is a prerequisite, not optional. |
| NEXT-108 warranty provisions | Nothing owns warranty cohorts, expected-claim assumptions or provision consumption. | Whether the company sells warranted products, and the reviewed assumption and measurement basis. |
| NEXT-109 insurance losses and recoveries | Nothing owns keeping the loss, the recovery entitlement, the insurer settlement and the cash distinct, including an insurer paying a supplier directly. | Whether insurance is in scope and which coverages exist; gross-versus-net presentation is a policy decision, not a default. |
| NEXT-111 common-cost VAT deduction true-up | The VAT treatment matrix owns treatment families and VAT-02 owns the return, but nothing owns an annual true-up from provisional to qualified final allocation over a complete population. | Whether the company has common costs allocated across deductible and non-deductible use, and the qualified allocation basis. |
| NEXT-113 B2C destination VAT and Union OSS | Nothing in the maintained plans names B2C, destination VAT or the Union OSS scheme. A word-boundary search found no occurrence. | Whether the company sells to consumers in other EU countries, and the qualified country/rate set, reporting currency and correction rules. This is a real new external obligation, not a treatment variant. |
| NEXT-114 EU foreign input-VAT recovery | NEXT-05 owns foreign service *purchases* on the purchase side. Nothing owns moving retained foreign-tax evidence to a recovery claim, a recognized entitlement and an actual refund. | Whether the company has recoverable foreign VAT, and per-country claim and refund mechanics. The packet's own rule that it is never Swedish input VAT is the constraint that keeps this out of VAT-02. |
| NEXT-116 car-benefit valuation | Nothing in the maintained plans owns a company-car benefit, its recurring monthly valuation or an employee payment against it. PRY-70 covers salary exchange, per-diem, meals and mileage, not a car. | Whether the company provides cars, and the qualified valuation basis and payment treatment. |
| NEXT-117 KU20 and KU25 interest statements | PAY-04 owns AGI/KU *employer* declaration profiles. Nothing owns interest-statement identities for lenders or borrowers, or the correction identity for a corrected statement. | Whether the company has interest relationships requiring these statements, and the reporter/recipient case for each. Depends on the loan-lifecycle decision already recorded above. |
| NEXT-119 share subscriptions and registered capital | Nothing in the maintained plans owns a subscription, allotment, nominal capital, premium or the transition to registered capital. NEXT-89 is the dividend lifecycle, which the archive correctly treats as separate. | Whether the company issues shares, and the qualified subscription, allotment and registration conditions. Its own rule — a transfer labelled "shares" is not registered capital — is the invariant to preserve. |
| NEXT-123 autogiro and direct debit | Nothing in the maintained plans owns payer consent, company collection authority, direct-debit instructions, returned payments or their correction. INT-1 owns external delivery generally, not a collection instrument. | Whether direct debit is the chosen collection channel, and the provider contract, consent model and return handling. |

Three fifth-wave packets **compound** a gap already recorded rather than adding a decision: NEXT-105 and NEXT-106 build on the unowned project-billing lifecycle (NEXT-77/78/79), and NEXT-110 builds on the unowned loan lifecycle (NEXT-32). Deciding the earlier one decides these; they should not be tracked as separate open questions.

Two further fifth-wave packets are **already specified** rather than unowned, and are mapped above rather than listed as gaps. NEXT-121 is the notable one: [the operations plan](../operations.md) already states the mandate scope, validity, revocation, cumulative limits, atomic shared-budget consumption and the rule that a mandate never implicitly authorizes payment, closure, signature or filing, and already places unattended posting under a standing mandate outside the Book Zero delivery as later scope. The packet's proposed profile is narrower than that contract. It needs an authorization decision, not an owner, and the operations plan stays the maintained authority.

Two further fourth-wave packets are **partially** covered rather than unowned, and are mapped above rather than listed as gaps: NEXT-93 evidence search extends the document backlog's archive search, and NEXT-100 event subscriptions extend the external-delivery capability the coverage map already places behind per-provider authorization. Both need a named contract, not a new owner.

## Independent proof obligations

A packet is finished when the supported input reaches its complete intended result and the related consumers agree — not when a preparation record, a route or a button exists. For each implemented packet, retain:

- a before/after financial vector and independent expected outcomes that were not obtained by calling the production code;
- identity and capacity checks, including repeated-key recovery and refusal of a different key that would repeat the same economic effect;
- a stale-approval case, a concurrent-consumer case and a failure injected after each persistence phase;
- correction behavior that repairs the complete domain consequence, not only the journal lines, with reconciliation still exposing unexplained records whose net is zero.

Task states stay separate: designed, leaf implementation, integrated, runtime observed, company-qualified, externally accepted. The archives assume no first-wave packet is complete, and neither may an implementer. The third, fourth and fifth waves add their own vocabularies — `designed`, `leaf_present`, `integrated`, `journey_observed`, `company_qualified`, `external_accepted`, plus blocked-with-a-named-owner at any state — which are compatible; use one column set rather than five.

## What this dossier does not establish

- No repository file was changed by the archives, and no application, database, queue or provider workflow was run to produce them.
- Their structural and arithmetic self-checks are document checks. They are not compiled operations, transaction tests, browser tests, legal qualification or provider acceptance.
- A statement that a capability was missing describes a pinned revision. This repository has advanced past the earlier pinned reviews; the fourth and fifth are both pinned to the head observed at import. The third wave states its own "new" claims against the *prior NEXT scope* rather than against an exhaustive audit of current source, the fourth states its reading was targeted rather than a source audit, and the fifth states its reading was targeted to the branch and shared operations/contracts with specialist facts only narrowly checked. All three are therefore weak evidence of absence, and both later waves are explicit that no complete source audit or runtime qualification is claimed.
- The third, fourth and fifth waves all assert that they preserve rather than renumber the earlier packets, and the last two record their prior ranges as "not assumed complete". Neither renumbers anything, and neither discharges any earlier packet's application, persistence or proof obligation.
- Statutory rates, tax and contribution tables, reporting boxes, deadlines, per-diem and mileage amounts, declaration and statement schema versions, bank formats, pension and tax-reserve parameters, provider contracts and credentials remain qualified inputs under [D-04](../open-decisions.md), [D-08](../open-decisions.md) and [D-10](../open-decisions.md). Nothing here activates a rule, rate, provider or legal profile. The later waves add no new decision row: company identity and applicability stay D-04, dated parameters stay D-08, provider authority stays D-10 and any test change stays D-09. The fifth wave's specialist profiles — provisions, B2C/OSS, foreign VAT recovery, car benefit, share subscriptions, direct debit and standing posting mandates — are conditional by its own statement and are not launch prerequisites.
- Nothing here authorizes new repository tests, a data reset, a deployment, a payment or a filing. The test-change policy in `AGENTS.md` and [D-09](../open-decisions.md) still governs. The fourth and fifth waves say the same in their own terms and add that they create no test, browser, provider, production-data or deployment permission.

## Maintaining this plan

Update the packet index when a packet is implemented, qualified or superseded, and record the evidence revision rather than deleting the row. When a packet's design changes materially, change it in a dated revision of the vendored archive or in a new plan, and keep the checksummed trees unmodified. Add a mapping row only after the actual checkout confirms it. Re-resolve the reserved-work list whenever a reserved owner is released, and record the release rather than deleting the reservation.
