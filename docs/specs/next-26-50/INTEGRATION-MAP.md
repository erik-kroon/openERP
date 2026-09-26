# Integration, non-overlap and dispatch

Late branch movement is recorded in [REVISION-NOTE.md](REVISION-NOTE.md). The source review remains pinned; the current resolver is consumed rather than rebuilt.

These 25 packets are NEXT-26 through NEXT-50. They extend the prior application-owned v2 designs, not the superseded SQL-owned package. Their IDs are work IDs, never migration numbers.

## Root handoff

Before dispatch, read current AGENTS.md and the application replacement plan. Record current HEAD and dirty ownership claims. Resolve each existing-operation path in the actual checkout. If a proposed slice already exists, qualify/complete that implementation and record the difference instead of rebuilding it. Do not infer that all first-wave packets are complete because this second wave exists.

Do not dispatch 25 independent writers into shared files. Root integrates schema/grants, core transaction/admission, shared contract exports, capability composition and top-level routing. Domain owners supply leaf operations, pure calculators, typed persistence and local UI. All nested financial writers accept the caller's transaction. No public execute call opens another transaction from inside a financial group.

The current replacement owner retains all placeholder-operation ports and baseline proof. The five earlier WIPs remain reserved. Old numeric migration references are provenance, not instructions to resurrect stored procedures.

## Priority interpretation

P0 means high accounting value when the workflow applies and its prerequisites exist. It does not mean a company must use cash bookkeeping or employ staff. P1 extends important business lifecycles. P2 is conditional breadth. A no-payroll company must not wait for payroll expansion; a company using an unsupported required case cannot be labelled complete by omitting it.

Use NEXT-37 after the VAT owners hand off to finish the distinction between tax-account assessment and reclassification. NEXT-38 matters only for a verified cash-method company. NEXT-31 helps period accuracy for supported subscriptions/accruals. NEXT-50 improves agent operation only after actual domain summaries exist. Extraction in NEXT-26 is for missing/new facts, not a reason to redo existing receipt matching.

Possible nonconflicting leaf starts are 26, 27 and 28 once their existing application owners are available. None is permission to overlap the current source-intake/commerce/delivery port. Treasury and payroll chains are deliberately sequential within shared capacity owners.

## Reserved work

**WIP-VAT03:** Existing VAT control reclassification and its qualification. Consume the released application owner, do not repeat the former 9120/9130 qualification assignment.

**WIP-FX02-P1:** Existing paired FX partial settlement. Consume the released pure release calculation and internal tx mutation, do not recreate the former 9140 algorithm.

**WIP-AST03-UI:** Existing impairment UI/control/disposal closure. Consume the final asset basis and released tx ports after owner handoff.

**WIP-VAT04-A1:** Existing obligation-owned VAT amendment financial delta. No second target-minus-prior owner.

**WIP-COM2-W1:** Webshop intake, raw order identity, catalog snapshots and order authority. No packet takes this over.

**APPLICATION-REPLACEMENT:** Existing SQL-to-Effect migration, placeholder-operation closure and baseline proof. All new packets require released owning slices.

## Packet dependency map

| Packet | Required first/new wave contracts | Integration handoff | Conditional cases |
|---|---|---|---|
| [NEXT-26](packets/NEXT-26.md) | Existing owner | APP-SLICE-READY(purchases/inbox) | NEXT-03: a reviewed draft is subsequently accepted and posted |
| [NEXT-27](packets/NEXT-27.md) | Existing owner | APP-SLICE-READY(commerce/crm-master) | NEXT-02: legal identity facts or payment-role qualification are needed |
| [NEXT-28](packets/NEXT-28.md) | Existing owner | APP-SLICE-READY(commerce/collections), APP-SLICE-READY(durable-delivery) | NEXT-15: the selected invoice has credit-note adjustments; NEXT-30: customer-credit balances affect the reminder amount |
| [NEXT-29](packets/NEXT-29.md) | NEXT-02 | APP-SLICE-READY(commerce/invoice-lifecycle) | NEXT-15: an issued recurring invoice needs a credit |
| [NEXT-30](packets/NEXT-30.md) | NEXT-15 | APP-SLICE-READY(commerce/register) | NEXT-04: credit notes affect a supported VAT return |
| [NEXT-31](packets/NEXT-31.md) | NEXT-03, NEXT-13 | APP-SLICE-READY(subledger/schedules) | WIP-AST03-UI: the released schedule/control implementation is shared with the asset owner |
| [NEXT-32](packets/NEXT-32.md) | NEXT-02 | APP-SLICE-READY(subledger/owners) | NEXT-06: shareholder funding already recognized supplies the opening loan basis; NEXT-13: publishing reconciled loan controls |
| [NEXT-33](packets/NEXT-33.md) | NEXT-03 | APP-SLICE-READY(purchases), APP-SLICE-READY(payroll-foundation) | NEXT-21: the approved payout route is payroll rather than a payable payment |
| [NEXT-34](packets/NEXT-34.md) | NEXT-33 | APP-SLICE-READY(payroll-foundation) | NEXT-20: the selected entitlement includes taxable compensation; NEXT-21: payout/reporting uses payroll |
| [NEXT-35](packets/NEXT-35.md) | NEXT-20 | NEXT-21 | None |
| [NEXT-36](packets/NEXT-36.md) | NEXT-21 | APP-SLICE-READY(payroll) | NEXT-35: the correction includes variable, absence or holiday components |
| [NEXT-37](packets/NEXT-37.md) | NEXT-04 | WIP-VAT03, WIP-VAT04-A1, APP-SLICE-READY(tax-account) | None |
| [NEXT-38](packets/NEXT-38.md) | NEXT-03, NEXT-04 | APP-SLICE-READY(commerce/register) | NEXT-23: the reviewed unpaid population is consumed by financial year-end |
| [NEXT-39](packets/NEXT-39.md) | NEXT-30 | APP-SLICE-READY(source-intake), APP-SLICE-READY(commerce/register) | NEXT-40: processor balances use a non-book currency; WIP-COM2-W1: read-only order provenance is required; do not modify its intake |
| [NEXT-40](packets/NEXT-40.md) | NEXT-17, NEXT-18 | WIP-FX02-P1, APP-SLICE-READY(banking) | None |
| [NEXT-41](packets/NEXT-41.md) | NEXT-18 | WIP-FX02-P1, APP-SLICE-READY(commerce-fx) | NEXT-40: the affected chain includes native foreign-cash holdings; NEXT-23: affected financial periods require approved reopening |
| [NEXT-42](packets/NEXT-42.md) | Existing owner | WIP-AST03-UI, APP-SLICE-READY(subledger) | NEXT-19: checking disposal/proceeds consumers; NEXT-13: presenting the resulting financial controls |
| [NEXT-43](packets/NEXT-43.md) | NEXT-14, NEXT-13 | APP-SLICE-READY(dimensions) | None |
| [NEXT-44](packets/NEXT-44.md) | NEXT-12, NEXT-14 | APP-SLICE-READY(historical-migration) | NEXT-11: independent roundtrip export is part of acceptance |
| [NEXT-45](packets/NEXT-45.md) | NEXT-13 | APP-SLICE-READY(reports) | NEXT-40: the selected cash perimeter contains foreign-currency holdings; NEXT-39: processor/transit positions belong to the selected cash perimeter |
| [NEXT-46](packets/NEXT-46.md) | NEXT-03, NEXT-15 | APP-SLICE-READY(invoice-delivery) | NEXT-26: inbound documents enter the assisted supplier-review workflow |
| [NEXT-47](packets/NEXT-47.md) | NEXT-24 | APP-SLICE-READY(artifacts) | None |
| [NEXT-48](packets/NEXT-48.md) | NEXT-24, NEXT-47 | APP-SLICE-READY(external-delivery) | None |
| [NEXT-49](packets/NEXT-49.md) | NEXT-02 | APP-SLICE-READY(closing/deadlines) | NEXT-04: VAT calculations are impacted; NEXT-21: payroll declarations are impacted; NEXT-48: annual-report authority outcomes fulfill deadlines |
| [NEXT-50](packets/NEXT-50.md) | NEXT-01, NEXT-16 | APP-SLICE-READY(capabilities) | NEXT-49: including qualified deadline/impact outcomes; NEXT-33: including employee claim summaries under separate permissions |

## Concrete cross-owner contracts

| Producer | Consumer | Required result, not a second authority |
|---|---|---|
| NEXT-03 | 26, 31, 33, 38, 46 | Source-line recognition and tax-fact compiler plus internal tx creation/adoption |
| NEXT-15 | 30, 46 | Original line credit capacity, legal document identity and negative tax effects |
| NEXT-30 | 28, 39 | Customer-credit liability and refund capacity, distinct from unpaid AR |
| Existing schedule/impairment WIP | 31, 42 | Exact source basis, future occurrence lifecycle and approved internal tx effects |
| NEXT-20/21 | 33-36 | Frozen earnings/tax computations, already-recognized liability handoff and actual paid/reporting identity |
| VAT WIP owners | 37 | Effective role-signed reclassification/amendment vectors and current obligation version |
| NEXT-38 | NEXT-23 | Complete cash-method unpaid-recognition population and next-year no-duplicate settlement contract |
| FX WIP and NEXT-17/18 | 40-41 | Exact paired release and effective carrying/event history, without another obligation balance |
| NEXT-14/13 | 43-45 | Original classifications, fixed financial cutoffs and source-anchored contributions |
| NEXT-24 | 47-48 | Immutable statement model, exact copy artifact and local validation basis |
| NEXT-47 | 48 | Purpose-specific signature evidence, not an authority-hosted fastställelse event |
| Domain outcome owners | 49 | Typed same-scope prepared/submitted/accepted receipts, never free-text truth |
| Every released context adapter | 50 | Bounded coherent summary, complete counts, exact versions and honest unavailable state |

## Shared-file and semantic conflicts

Treasury 39-41 must serialize changes to cash/FX capacity projections. Customer credit 30 and reminder 28 share customer state but do not own each other's writes. Payroll 33-36 must agree source-component and liability handoff identity before implementation. Dimension restatement 43 may not change original-journal or SIE44 input meaning. Signing47 and filing48 share artifact references but never substitute one signature purpose for another.

A safe port can retain conservative stale checks. Narrow them only in a new understood plan version after the corresponding mutation population and concurrency proof exist. Removing a whole-account version without replacing its affected resource/predicate dependency is not an optimization.

## Worker completion format

Each worker returns one concise handoff with: exact changed paths; exported operations and contracts; schema/grant requirements; declared financial ownership; examples and independent expected outcomes; static/runtime checks actually run; unresolved input/port gates; shared integration diff; and a next action. No repeated full logs to the coordinator. No nested delegation unless the coordinator explicitly selects it.

Use the existing test authorization policy. This dossier supplies design vectors and proof obligations, not permission to add repository tests, run provider calls, post actual company books or deploy. Financial and legal profiles remain separately qualified.
