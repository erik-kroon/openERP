# NEXT implementation dossiers: packets, prerequisites and mapping

Status: **planning scope, implementation-level design; no implementation or verification status**. Added 2026-09-26. Owner: cross-area integrator, with the per-packet owner lane named in each packet. Phase: supplemental to the seven-area [delivery plan](README.md); the packets are **not** added to the 53-packet accounting index or its dependency DAG.

The decision to vendor these dossiers, keep them outside the maintained plan namespace and treat `NEXT-nn` as a work namespace rather than a delivery index is [ADR 0012](../adr/0012-next-implementation-dossier.md). The vendored files themselves are listed in [the specifications index](../specs/README.md).

## What these documents are

Two externally produced dossiers specify **how** fifty work items would be implemented inside the application-owned Effect boundary: named application operations, pure exact calculations, transaction-passing persistence, typed approval, durable queue delivery through the existing outbox and effect-mq runner, and the failure/replay cases each operation must survive. They supply per-item algorithms, record shapes, transaction sketches, UI/agent expectations and concrete numeric vectors.

They are not a repository audit, not an applied implementation and not runtime proof. Each packet states its own status as proposed application-owned pseudocode.

| Wave | Packets | Pinned review | Archive self-check, re-run on import |
| --- | --- | --- | --- |
| `next-01-25` — application-owned Effect edition v2 | NEXT-01 … NEXT-25 | `422276ae…` architecture context, `bb628452…` inherited task baseline | 7,465 assertions, 0 failures; 37 of 37 checksums OK |
| `next-26-50` — second wave | NEXT-26 … NEXT-50 | `5ac3433e…` repository review dated 2026-09-26, plus the limited late observation `4671a2fb…` | 90 of 90 named design checks passed; 41 of 41 checksums OK |

The dated import observation and its limits are recorded in [next-dossier-verification.md](evidence/next-dossier-verification.md).

## Relationship to the other planning layers

| Layer | Owns | Does not own |
| --- | --- | --- |
| [Seven-area delivery plan](README.md) (`FND`/`PST`/`COR`/`IMP`/`COM`/`VAT`/`PAY`/`AST`/`FX`/`END`/`OPS-nn`) | The delivery denominator, mandatory dependency DAG, acceptance and traceability | Implementation-level algorithms, exact vectors, per-operation failure matrices |
| [Capability backlog](capability-backlog.md) (`SALES`/`PUR`/`BANK`/`TAX`/… labels) | Which requested capability is owned, and the supplemental collections, supplier inbox, party master, recurring invoicing, deadlines and expense/payroll handoffs | Work units, prerequisites and proof for those requirements |
| [Reference parity backlog](11-parity-backlog.md) (`PRY-nn`) | Reference-implementation findings with an adopt/structure-only/re-derive class per rule | Anything the reference does not contain, including the second wave's treasury, tax-assessment and cash-flow work |
| **NEXT dossiers (`NEXT-nn`, this document)** | Implementation-level design per work item: existing owner, new scope, algorithm, transaction boundary, failure and replay cases, vectors | Requirements, applicability decisions, delivery order, completion counts or proof |

A `NEXT-nn` packet is therefore the **implementation design for a requirement the plans already own**, plus a small number of lifecycle extensions the plans name only as follow-up work. It does not add scope on its own, and it never renumbers either existing namespace.

## Rules for an implementing agent

1. **The repository instructions win.** Read `AGENTS.md`, [ADR 0009](../adr/0009-effect-mq-background-jobs.md), [ADR 0010](../adr/0010-application-owned-accounting-replacement.md) and the owning area plan first. A packet that conflicts with them is corrected by the packet, not by the repository rule.
2. **Pinned statements are dated, not current.** The pinned revisions are ancestors of this repository's history. Reconcile the actual checkout before coding: a named path, function or module is a proposed responsibility to bind to real code, and a statement that something was missing describes that pinned revision only. The second wave's own `REVISION-NOTE.md` records that NEXT-01 was reported implemented at `4671a2f` with static checks only and no runtime proof.
3. **`APP-SLICE-READY(area)` is a prerequisite, not extra work.** Resolve it against the real checkout: the area's named operations, scoped persistence and complete correction/recovery behavior must be released by the migration owner. A route that returns `UnsupportedProfile` is not a ported implementation. When the port is missing, deliver the leaf calculator, schema and exact integration contract without taking over the migration owner.
4. **One financial transaction per group.** The caller's transaction is passed into every nested journal, tax, register, approval-use and receipt write. No public execute/HTTP call opens a second transaction from inside a financial group, and no nested operation re-acquires a book lock.
5. **Exact values only.** Canonical exact integer strings over the wire, `bigint` internally, exact rational rates and quantities with units. An amount, balance or sequence never becomes a JavaScript number. Retain a rounding residual and explain it rather than posting a plug.
6. **Reserved owners stay reserved.** The five reserved workstreams and the application replacement are listed below. Consume a released owner; do not reimplement it, and do not create a second writable financial register to avoid a missing port.
7. **Vectors are obligations, not tests.** Each packet's numeric vectors and failure cases are design obligations to satisfy and to verify under the actual test authorization in force. The dossiers add no repository test and grant no deployment, provider, payment, filing or company-data authority.
8. **Report the real state.** A worker returns exact changed paths, exported operations and contracts, schema/grant needs, declared financial ownership, the checks actually run, unresolved gates and remaining blockers. A documented function that refuses every case is not a completed packet, and a JSON preparation record or a UI button alone is not completion.

## Packet index

`Requires` lists the packets whose contracts must exist first. `Integrate after` lists the released application slices the packet composes with; an empty cell means the packet names an existing owner directly. `Conditional` entries apply only when the selected company actually uses that case — a conditional edge is not a reason to delay independent work, and an inapplicable case is never a reason to call the product complete.

Lane codes are the archives' own owner lanes. The first wave's single-letter lanes are not defined in the vendored files; the second wave's named lanes are self-describing.

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

## Requirements the maintained index does not yet own

These six packets describe lifecycles the plans name only as follow-up work, or do not name at all. They are recorded here rather than added to the 53-packet index, because adding them would change a reviewed denominator on the strength of an external design input. Each needs a decision before implementation.

| Packet | What is not owned today | Decision required |
| --- | --- | --- |
| NEXT-32 loan lifecycle | No maintained packet or capability label covers loan principal, interest accrual or repayment allocation. NEXT-06 owns owner funding only, and capital contributions must not become loans. | Whether lending is product scope for the selected company, and which owner holds the obligation. A dated company fact under [D-04](../open-decisions.md) decides applicability, not this document. |
| NEXT-41 late FX chain repair | FX-03 owns period remeasurement; the first wave explicitly refuses revaluation after settlement consumed the old basis. | Whether the consumed-chain repair is accepted scope, and its proof obligation. This is a limitation the plans already record, not a newly discovered defect. |
| NEXT-42 economic impairment reversal | [ADR 0008](../adr/0008-financial-fx-vat-impairment.md) adopts the impairment contract with positive remaining carrying and a bounded immediate error correction; economic reversal and broader asset classes remain scoped follow-up. | The qualification of the without-impairment cap, the eligible asset/framework and the residual schedule — all D-08 qualified inputs. |
| NEXT-40 foreign cash holdings | FX packets own foreign obligations. Native foreign-currency cash balances and transfers are a second, distinct capacity. | Whether foreign cash is in scope for the company, and the acquisition/release policy as a dated rule. |
| NEXT-45 direct cash-flow statement | REP-1 names cash flow as a capability and END-03 covers P&L, balance sheet and openings; no packet owns a cash-flow statement with a reconciliation bridge. | Whether the statement is built from owned relationships, and the reviewed cash perimeter and classification policy. |
| NEXT-36 paid payroll recovery | PAY-03 owns frozen-run posting and correction; the first wave's correction is bounded to an unpaid run. Recovery or future-pay adjustment after actual payment is a different financial case. | Whether recovery is permitted for the company, which requires an enforceable legal basis and, for declarations, a case-specific treatment under D-08. |

## Independent proof obligations

A packet is finished when the supported input reaches its complete intended result and the related consumers agree — not when a preparation record, a route or a button exists. For each implemented packet, retain:

- a before/after financial vector and independent expected outcomes that were not obtained by calling the production code;
- identity and capacity checks, including repeated-key recovery and refusal of a different key that would repeat the same economic effect;
- a stale-approval case, a concurrent-consumer case and a failure injected after each persistence phase;
- correction behavior that repairs the complete domain consequence, not only the journal lines, with reconciliation still exposing unexplained records whose net is zero.

Task states stay separate: designed, leaf implementation, integrated, runtime observed, company-qualified, externally accepted. The archives assume no first-wave packet is complete, and neither may an implementer.

## What this dossier does not establish

- No repository file was changed by the archives, and no application, database, queue or provider workflow was run to produce them.
- Their structural and arithmetic self-checks are document checks. They are not compiled operations, transaction tests, browser tests, legal qualification or provider acceptance.
- A statement that a capability was missing describes a pinned revision. This repository has advanced past both pinned reviews.
- Statutory rates, tax and contribution tables, reporting boxes, deadlines, per-diem and mileage amounts, declaration schema versions, e-invoicing profiles, provider contracts and credentials remain qualified inputs under [D-04](../open-decisions.md), [D-08](../open-decisions.md) and [D-10](../open-decisions.md). Nothing here activates a rule, rate, provider or legal profile.
- Nothing here authorizes new repository tests, a data reset, a deployment, a payment or a filing. The test-change policy in `AGENTS.md` and [D-09](../open-decisions.md) still governs.

## Maintaining this plan

Update the packet index when a packet is implemented, qualified or superseded, and record the evidence revision rather than deleting the row. When a packet's design changes materially, change it in a dated revision of the vendored archive or in a new plan, and keep the checksummed trees unmodified. Add a mapping row only after the actual checkout confirms it. Re-resolve the reserved-work list whenever a reserved owner is released, and record the release rather than deleting the reservation.
