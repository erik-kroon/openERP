# Product capability backlog and coverage

Status: planned requirements, reconciled with the supplied capability list on 2026-09-24. This is a coverage index plus a supplemental backlog for requirements not explicit in the seven accounting-area plans. It makes no new implementation or verification claim. Consult the [roadmap](../roadmap.md), [frontend progress](../frontend.md) and linked evidence for observed behavior.

The supplied IDs use one digit (`COM-1`); existing delivery packets use two (`COM-01`). They are separate namespaces, not aliases. The existing 53-packet dependency index covers the accounting baseline only; the supplemental work below is not included in that count. Requirements mapped to an existing owner must be completed there, not recreated as duplicate systems.

## Requested capability coverage

Each row preserves the requested scope and names its requirement owner. A link means planning coverage, not that the capability is complete. Sections below own the added requirements; their linked domain plans continue to own accounting effects and shared controls.


### Sales, purchasing, and payments

| ID | Required scope | Plan owner |
| --- | --- | --- |
| SALES-1 | Customer invoice lifecycle: Drafting, issuance, delivery, payments, credits, cancellations, and corrections. | [Owner](04-invoices-payments-registers.md) |
| SALES-2 | Customer register and ageing: Invoice/payment balances, overdue status, and register-to-GL controls. | [Owner](04-invoices-payments-registers.md) |
| SALES-3 | Collections: Reminders, statements, disputes, and follow-up history. | [Owner](capability-backlog.md#collections) |
| PUR-1 | Supplier invoice lifecycle: Source documents, invoice drafts, VAT and account suggestions, review, booking, and evidence. | [Owner](04-invoices-payments-registers.md) |
| PUR-2 | Supplier credits and payments: Credits, partial allocations, payment batches, payment-file generation, and recovery. | [Owner](04-invoices-payments-registers.md) |
| PUR-3 | Purchase acceptance: Link purchase evidence to invoices and reconcile AP to ledger controls. | [Owner](04-invoices-payments-registers.md) |

### Banking, cash, and tax account

| ID | Required scope | Plan owner |
| --- | --- | --- |
| BANK-1 | Statement intake and reconciliation: File intake, matching, partial/many-to-many allocation, unmatch, and signoff. | [Owner](03-imports-matching-reconciliation.md) |
| BANK-2 | Connected bank feeds: Provider consent, account coverage, cursors, synchronization, retries, and recovery. | [Owner](03-imports-matching-reconciliation.md) |
| BANK-3 | Cash controls: Expected-account inventories, statement continuity, ledger balances, and stale signoffs. | [Owner](03-imports-matching-reconciliation.md) |
| TAXACCT-1 | Skattekonto: Statement import or connection, event classification, matching, controls, and settlement handling. | [Owner](05-vat-payroll-assets-fx.md) |

### VAT and tax

| ID | Required scope | Plan owner |
| --- | --- | --- |
| VAT-1 | Reviewed tax rules and facts: Effective-dated treatments, evidence, and unsupported-case handling. | [Owner](05-vat-payroll-assets-fx.md) |
| VAT-2 | VAT return preparation: Box calculations, source lineage, exclusions, and control-account reconciliation. | [Owner](05-vat-payroll-assets-fx.md) |
| VAT-3 | Tax settlement: Connect return results to explicit accounting effects and tax-account events. | [Owner](05-vat-payroll-assets-fx.md) |
| VAT-4 | Amendments and filing: Preserve versions and distinguish preparation, export, submission, and acceptance. | [Owner](05-vat-payroll-assets-fx.md) |
| TAX-1 | Income-tax bridge and declarations: INK2, NE, SRU, adjustments, and amendments under reviewed profiles. | [Owner](06-year-end-reports-filing.md) |

### Ledger, accounting controls, and reporting

| ID | Required scope | Plan owner |
| --- | --- | --- |
| GL-1 | Journal lifecycle: Prepare, approve, post, and recover journal operations. | [Owner](01-posting-approval-receipts.md) |
| GL-2 | Corrections: Reversals and replacements with retained lineage and downstream effects. | [Owner](02-corrections.md) |
| GL-3 | Ledger and register controls: Reconcile subledgers and selected accounts at fixed cutoffs. | [Owner](06-year-end-reports-filing.md) |
| REP-1 | Core financial reports: Trial balance, GL, P&L, balance sheet, cash flow, and comparisons. | [Owner](06-year-end-reports-filing.md) |
| REP-2 | Register and accountant reports: Show source coverage and reconcile represented registers to the ledger. | [Owner](06-year-end-reports-filing.md) |
| REP-3 | Retained reports: Preserve report bytes/manifests and show currentness and limitations. | [Owner](06-year-end-reports-filing.md) |

### Period close and statutory accounts

| ID | Required scope | Plan owner |
| --- | --- | --- |
| CLOSE-1 | Obligation inventory: Evidence which source and obligation families apply; block unsupported completeness claims. | [Owner](06-year-end-reports-filing.md) |
| CLOSE-2 | Technical close and reopen: Verify approval, locks, certificates, invalidation, replay, and concurrency. | [Owner](06-year-end-reports-filing.md) |
| CLOSE-3 | Financial year-end: Result transfer, carryforward, opening basis, and year-end adjustments. | [Owner](06-year-end-reports-filing.md) |
| STAT-1 | Annual accounts: K2/K3 statements, notes, completeness, and versioned output. | [Owner](06-year-end-reports-filing.md) |
| STAT-2 | Statutory declarations: Applicable income-tax declarations and validation. | [Owner](06-year-end-reports-filing.md) |
| STAT-3 | Signature and filing: Signature, authority submission, and external outcome tracking. | [Owner](06-year-end-reports-filing.md) |

### Assets, expenses, and payroll

| ID | Required scope | Plan owner |
| --- | --- | --- |
| AST-1 | Fixed-asset register and opening basis: Assets, evidence, cost, accumulated depreciation, and cutover values. | [Owner](05-vat-payroll-assets-fx.md) |
| AST-2 | Depreciation and deferrals: Reviewed schedules, occurrences, posting, and amendments. | [Owner](05-vat-payroll-assets-fx.md) |
| AST-3 | Asset disposal and controls: Disposal, impairment, gains/losses, and register reconciliation. | [Owner](05-vat-payroll-assets-fx.md) |
| EXP-1 | Expenses and receipts: Employee/owner claims, receipt capture, review, classification, and posting. | [Owner](04-invoices-payments-registers.md) |
| EXP-2 | Mileage and reimbursements: Trips, rates, tax treatment, payroll or payment handoff, and controls. | [Owner](capability-backlog.md#expenses-and-payroll-handoffs) |
| PAY-1 | Employment foundation: Employee records, work inputs, sensitive-data permissions, and opening balances. | [Owner](05-vat-payroll-assets-fx.md) |
| PAY-2 | Payroll calculations: Pay, benefits, absence, vacation, deductions, taxes, and contributions. | [Owner](05-vat-payroll-assets-fx.md) |
| PAY-3 | Pay-run accounting: Frozen inputs, approval, posting, and corrections. | [Owner](05-vat-payroll-assets-fx.md) |
| PAY-4 | Payment files and payslips: Retained artifacts and separate payment-state tracking. | [Owner](capability-backlog.md#expenses-and-payroll-handoffs) |
| PAY-5 | AGI/KU declarations: Validated declarations, amendments, and delivery state. | [Owner](05-vat-payroll-assets-fx.md) |
| PAY-6 | Payroll controls: Reconcile payroll registers, ledger, tax payments, and declarations. | [Owner](capability-backlog.md#expenses-and-payroll-handoffs) |

### Foreign currency

| ID | Required scope | Plan owner |
| --- | --- | --- |
| FX-1 | Financial FX policy and ownership: Foreign obligation identity, rate provenance, account roles, and paired balances. | [Owner](05-vat-payroll-assets-fx.md) |
| FX-2 | FX recognition: Foreign-denominated receivable/payable recognition and carrying value. | [Owner](05-vat-payroll-assets-fx.md) |
| FX-3 | Settlement and realized FX: Partial/full settlement, fees, residuals, and realized gain/loss. | [Owner](05-vat-payroll-assets-fx.md) |
| FX-4 | Revaluation: Period-end open-item valuation and reversal/correction. | [Owner](05-vat-payroll-assets-fx.md) |
| FX-5 | FX controls and reports: Per-currency registers and book-currency reconciliation. | [Owner](05-vat-payroll-assets-fx.md) |

### Imports, migration, and dimensions

| ID | Required scope | Plan owner |
| --- | --- | --- |
| IMP-1 | Source coverage: Providers, formats, records, and known limitations. | [Owner](03-imports-matching-reconciliation.md) |
| IMP-2 | Provider adapters: Consent, identity checks, pagination, retries, and resumability. | [Owner](03-imports-matching-reconciliation.md) |
| IMP-3 | Mapping and preview: Loss-preserving maps, exclusions, missing facts, duplicates, and controls. | [Owner](03-imports-matching-reconciliation.md) |
| IMP-4 | Durable import execution: Immutable plans, bounded chunks, receipts, recovery, and compensation. | [Owner](03-imports-matching-reconciliation.md) |
| IMP-5 | Cutover and opening balances: History/opening choice, year partitions, open items, and double-count prevention. | [Owner](03-imports-matching-reconciliation.md) |
| IMP-6 | Register migration: Connect imported history to live registers without assuming source assertions are current. | [Owner](03-imports-matching-reconciliation.md) |
| IMP-7 | Actual-source acceptance: Independently controlled provider/file migration and failure recovery. | [Owner](03-imports-matching-reconciliation.md) |
| DIM-1 | Dimension model: Multiple dimensions, coded values, effective dates, and archival. | [Owner](capability-backlog.md#dimensions) |
| DIM-2 | Dimension propagation: Carry dimensions through ledger, corrections, registers, and imports/exports. | [Owner](capability-backlog.md#dimensions) |
| DIM-3 | Dimension posting policies: Required, default, and fixed values with historical exemptions. | [Owner](capability-backlog.md#dimensions) |
| DIM-4 | Tagging and audit: Line, bulk, and reviewed retagging with retained history. | [Owner](capability-backlog.md#dimensions) |
| DIM-5 | Dimension reporting: Filtered GL/P&L and reconciled by-value results. | [Owner](capability-backlog.md#dimensions) |
| DIM-6 | Dimension interoperability: Import preservation and SIE round-trip acceptance. | [Owner](capability-backlog.md#dimensions) |

### Documents, sales operations, and commerce

| ID | Required scope | Plan owner |
| --- | --- | --- |
| DOC-1 | Document management and archive: Upload, link, search, retention, export, and recovery. | [Owner](07-restore-operations-cutover.md) |
| DOC-2 | Invoice/supporting-document lifecycle: Capture, attach, review, and preserve source links. | [Owner](04-invoices-payments-registers.md) |
| COM-1 | Quotes and orders: Quotes, sales orders, and conversion into invoices. | [Owner](capability-backlog.md#sales-operations) |
| COM-2 | Articles/catalog and webshop orders: Product records and external order intake. | [Owner](capability-backlog.md#sales-operations) |

### Agents, integrations, and operations

| ID | Required scope | Plan owner |
| --- | --- | --- |
| AGT-1 | MCP/API coverage: Operation parity, authentication, authorization, and recovery. | [Owner](../operations.md); [source inventory](agt01-api-mcp-parity.md) |
| AGT-2 | AI assistance and document extraction: OCR, classification, suggestions, and mandatory human review. | [Owner](../operations.md) |
| INT-1 | External delivery: Peppol/e-invoicing, email, payment, signing, and filing integrations with outcome recovery. | [Owner](07-restore-operations-cutover.md) |
| INT-2 | Extension framework: Extension contracts, permissions, configuration, and lifecycle. | [Owner](capability-backlog.md#extensions) |
| IAM-1 | Identity and company access: Production identity setup, roles, memberships, and firm/client boundaries. | [Owner](00-shared-contracts.md) |
| OPS-1 | Hosting and runtime readiness: Deploy and verify the intended Cloudflare or self-hosted distribution. | [Owner](07-restore-operations-cutover.md) |
| OPS-2 | Retention and recovery: Archive policy, backups, restore, and evidence retention. | [Owner](07-restore-operations-cutover.md) |
| REL-1 | Integrated acceptance: Complete end-to-end journeys across UI, API, database, recovery, and reporting. | [Owner](09-acceptance.md) |

## Collections

Owner: commerce/API and Sales UI; extends [invoice registers](04-invoices-payments-registers.md). SALES-3 adds dated reminders, customer statements, disputes, assigned follow-up and an append-only contact/action history linked to the customer and invoice. Statements pin an as-of date and invoice/payment cutoff. A dispute records reason, evidence, owner, resolution and any explicit reminder hold; it does not change invoice principal or ledger recognition. Reminder delivery uses the existing authorized outbox and retained outcome tracking. Fees or interest require a separately reviewed treatment, never an inferred charge.

Depends on party/invoice records, ageing and durable delivery. Acceptance: a partial payment changes the next statement's residual without rewriting a prior statement; a disputed or settled invoice is rechecked before reminder dispatch; response loss recovers the same delivery attempt; resolution retains the dispute and follow-up history.

## Sales operations

Owner: commerce/API and Sales UI. COM-1 adds versioned quotes and sales orders, acceptance/cancellation history and reviewed conversion to invoice drafts. Preserve source revision and per-line converted quantity/amount so retry or partial conversion cannot invoice the same order portion twice. Quote acceptance and order intake do not themselves issue an invoice or recognize revenue.

COM-2 adds articles/catalog records with stable codes, effective revisions, descriptions, units and explicit price/tax defaults. Drafts snapshot chosen defaults; later catalog edits cannot rewrite issued invoices. External webshop intake retains provider/order/line identity, revisions, cancellations and raw evidence with duplicate/retry recovery. Missing tax, identity or account mappings remain review blockers. Inventory, warehouse management and general CRM remain outside this scope.

Depends on source retention and the [commerce calculation/issue contracts](04-invoices-payments-registers.md). Acceptance: revise a catalog after quotation, partially convert an accepted order, retry after response loss and receive a duplicate webshop event; retained quote/invoice facts remain stable and converted capacity is consumed once. Refunds and post-issue cancellations use the existing credit/correction workflow.

## Dimensions

Owner: domain/contracts/API with Books and Reports UI; integrates [imports](03-imports-matching-reconciliation.md), [corrections](02-corrections.md) and [reports](06-year-end-reports-filing.md). DIM-1–DIM-6 add multiple named dimensions, stable coded values, effective dates and archival without deleting historical references. Carry explicit dimension assignments through draft and posted lines, registers, reversals/replacements and supported import/export profiles.

Posting policies pin required, default and fixed values to an effective policy revision. Preserve historical exemptions with their reason and provenance; missing imported values cannot silently inherit today's defaults. Required or fixed-value violations block new posting before approval consumption.

Line and bulk tagging use scoped review with expected revisions. Retagging posted records retains immutable original assignments plus a separately reviewed classification history; it must not rewrite posted bytes or old report snapshots. The exact classification storage/read contract remains a design gate before implementation. Reports identify whether they use original or reviewed classifications, pin that basis and include unassigned/exempt values so by-value totals reconcile to the same unfiltered ledger cutoff.

Acceptance: exercise two dimensions, an archived value, a changed fixed policy, an exempt historical line, a stale bulk review and a later retag. Saved reports retain their original basis; current by-value totals reconcile without double counting. Supported SIE round trips preserve codes and assignments; unsupported dimensions produce explicit loss diagnostics before admission/export acceptance.

## Expenses and payroll handoffs

Owner: commerce and payroll with Purchases UI. EXP-1 uses the existing [owner expense/recognition](04-invoices-payments-registers.md) and [reviewed tax](05-vat-payroll-assets-fx.md) owners; extend the claim workflow explicitly to employees with claimant, original receipt, review decisions, rejection/withdrawal and retained posting links.

EXP-2 adds trips with claimant, dates, purpose, route/distance evidence, vehicle facts and a dated reviewed rate/tax profile. Seal exact reimbursable amounts and choose one explicit payroll or payable/payment handoff. Corrections preserve the original trip/claim and reconcile any prior reimbursement; an exported instruction does not mark the claim paid.

PAY-4 additionally requires retained employee payslip bytes bound to the exact approved run and accessible only under payroll permissions. PAY-6 requires frozen controls across employee/register totals, payroll expense/liability ledger accounts, payments, tax-account events and declaration versions. Retain imported payroll opening balances and their source/cutover basis under PAY-1; missing opening history stays visible.

Depends on reviewed rule/company inputs, claims/payment capacity and the payroll run owner where payroll handoff is selected. Acceptance: receipt or trip retries do not create duplicate claims; a payroll handoff cannot also create a second payable; changed rates do not alter an approved claim; a corrected run preserves old payslips and declarations; discrepancies and absent opening data block complete control signoff. No rates or legal profiles are activated by this plan.

## Extensions

Owner: API/runtime and identity owners; INT-2 adds a bounded extension contract, not a marketplace. Before implementation, specify version compatibility, declared capabilities, entity/book-scoped permissions, configuration validation, secret references, enable/disable/upgrade and removal behavior. Use existing shared operations and durable jobs/outbox; an extension receives no direct ledger-write or human-approval privilege. Retain accounting evidence and receipts after disable/removal.

Depends on [shared admission contracts](00-shared-contracts.md) and [operations/recovery](07-restore-operations-cutover.md). The execution/isolation model and first concrete extension consumer remain design gates; do not add a speculative plugin runtime. Acceptance: incompatible versions refuse activation, revoked scope blocks new execution, disabling prevents unstarted external work, and committed work remains discoverable/recoverable without repeating an external effect.

## Delivery and evidence

Resolve each supplemental section's contract gates, then slice implementation around the named owning records and dependencies. Collections and sales operations can follow commerce independently of statutory completion; dimension identity/propagation must precede dimension policies, retagging and reporting acceptance. Expense handoff depends on the selected payment/payroll path, not every payroll feature. Extensions wait for a concrete consumer and execution contract.

REL-1 joins the applicable capabilities into the ordinary UI → API → database → recovery → reporting journeys described in [acceptance](09-acceptance.md) and [frontend acceptance](../frontend.md#acceptance-and-verification). Preserve repeatable evidence with revision, environment, inputs, actions, durable identities, expected/observed totals, artifacts and limitations. Existing local SALES-1 or PUR-1 observations do not close an entire capability row. New test changes still require the repository's explicit authorization; this documentation update adds no tests.

VAT settlement, financial FX and impairment use the adopted contracts in [ADR 0008](../adr/0008-financial-fx-vat-impairment.md). Their implementation/proof work and applicable legal rules, company facts and provider outcomes remain separately tracked in [open decisions](../open-decisions.md). Adoption does not complete any capability.

## Repository comparison reconciliation

The user supplied a product-domain comparison and consolidated assignment list on 2026-09-24. They are planning inputs, not a fresh verification of either repository. Statements that Accounted has a surface do not establish production correctness; statements that OpenERP lacks a surface must be checked against live code before assignment. The comparison adds the requirements below without changing existing packet identities or counting overlapping work twice.

### Assignment aliases and conflicts

| Supplied assignment | Canonical owner / disposition |
| --- | --- |
| AR-LEGAL | SALES-1 under COM-02/COM-05 in [commerce](04-invoices-payments-registers.md); reconcile existing legal-issue work before extending it. |
| AP-INTAKE | PUR-1 + DOC-2 + AGT-2; the [supplier inbox](#supplier-inbox-and-extraction) adds the missing channel/review contract. |
| COLLECTIONS | Alias of SALES-3, not another assignment. |
| CRM-MASTER | COM-01; [party master data](#party-master-data) adds bounded accounting-party operations, not general CRM. |
| TAXACCT-1 | VAT-03 owns tax-account events, matching and settlement; retain the broader source/connection scope and implement the adopted ADR 0008 settlement contract. |
| CLOSE-3 | END-02; financial year-end remains distinct from END-01 technical closing. |
| REP-1 / REP-2 / REP-3 | END-03, with statutory outputs in END-05/END-06. |
| Supplied PAY-04: payslips/payments | PAY-4 capability under canonical PAY-03 plus the expense/payroll handoff requirements above. Do not rename canonical PAY-04, which owns AGI/KU declarations. |
| Supplied PAY-05: declarations | PAY-5 capability under canonical PAY-04. No new PAY-05 packet is created. |
| Supplied PAY-06: controls | PAY-6 capability spanning PAY-03/PAY-04 and END-03; no separate duplicate PAY-06 packet. |
| Supplied FX-04: reports/controls | FX-5 capability under canonical FX-02/FX-03 and END-03. The existing FX-4 capability means revaluation; do not conflate them. |
| OPS-EXT | OPS-1 capability under OPS-04 and [distribution acceptance](../operations/cloudflare.md), with [self-host setup](../../infra/self-host/README.md). |
| BANK-2 / BANK-3 | Existing import/reconciliation owner and IMP-02/IMP-04/IMP-05, with provider authority through OPS-03. File intake does not satisfy feed acceptance. |

FND/PST/COR/IMP/COM/VAT/AST/END/OPS assignments otherwise retain their existing two-digit packet definitions and dependency graph. PAY-01–03 and FX-01–03 also retain their current meanings. Single-digit product capability IDs remain coverage labels. The suggested first wave is a priority view, not authorization to restart completed FND-01 work or bypass dependencies, test permissions or provider gates.

### Supplier inbox and extraction

Owner: source intake, commerce and governed AI operations; AP-INTAKE refines PUR-1/DOC-2/AGT-2. Retain upload and permitted inbound-email message/attachment identities, original bytes, arrival history and parsing/extraction attempts. Route each source to an explicit company/book before exposing it. Deduplicate retries by source identity without collapsing distinct documents merely because their bytes match.

Extraction retains model/parser version, source locations, suggested supplier/number/date/line/account/VAT facts, confidence and diagnostics separately from reviewed facts. Show the original beside editable suggestions, unresolved discrepancies and the resulting accounting proposal. Human review is mandatory before acceptance/posting; an email sender or source instruction grants no authority. Reprocessing retains previous interpretation and review lineage, and cannot silently revise an accepted invoice.

Depends on IMP-01, COM-01/COM-02, FND-02 and the existing [governed interpretation rules](../operations.md#governed-rules-and-agent-context). Acceptance: retry an attachment, deliver two legitimate identical-byte documents, misroute a message, fail extraction and revise a suggested tax/account. Preserve both legitimate occurrences, prevent cross-company disclosure, retain the draft on failure and recover one accepted invoice/receipt. Email-provider intake and OCR-provider data access need their specific configuration and acceptance; upload-only proof does not close those channels.

### Party master data

Owner: COM-01 commerce party revisions. CRM-MASTER covers customer/supplier directories, contacts, aliases, registry lookup provenance and scoped import/export needed for accounting. Reviewed duplicate resolution preserves original party IDs and invoice snapshots. A merge must retain redirects/resolution history, reconcile open-item ownership and refuse incompatible legal identities; it cannot rewrite old payee facts or combine settlement capacity without an explicit reviewed contract.

Depends on scoped party records and source identity. Acceptance: two suppliers with similar names remain distinct until reviewed; a registry change does not rewrite an issued invoice; a bank-detail change invalidates dependent payment approval; import retry and merge recovery preserve historical references and balances. General lead pipelines, campaigns and CRM remain outside scope.

### Recurring invoices and ROT/RUT

Owner: COM-02/COM-05 plus PST-05 for recurring work. SALES-1 includes recurring invoice templates with versioned schedule, effective dates, pause/end state and stable occurrence identity. Each occurrence produces a recoverable draft/review under the current eligible profile; template edits cannot change issued history. Existing recurring journal preparation alone does not satisfy recurring invoicing. Acceptance: replay a due occurrence after response loss and change the template concurrently; at most one invoice is issued for that occurrence and future work uses the declared revision.

ROT/RUT enters as an explicitly conditional sales/tax profile, not a default tax discount. Before implementation, establish applicable customer/property/work facts, reviewed eligibility and amount rules, the customer-versus-authority receivable split, claim/submission identity, rejection/adjustment and settlement controls. Acceptance must independently reconcile invoice gross value, each obligor's outstanding amount, credits and authority outcome without treating claim export as payment. D-04/D-08/D-10 gate legal/provider activation. Unsupported cases remain named blockers.

### Deadlines and calendar

Owner: obligation inventory and operations, with Overview/To do UI; supplemental ID DEADLINE-1. Retain obligation identity, company applicability, period, responsible actor, due date/time zone, reviewed rule/source revision, manual override reason and links to preparation/submission outcomes. Distinguish upcoming, overdue, prepared, submitted and accepted; a dismissed reminder cannot fulfill an obligation. A revised rule creates review work and retains the old deadline basis.

Calendar export/feed tokens are scoped and revocable, expose only permitted fields and use stable event identity for updates/cancellations. Depends on FND-02/FND-03, END-01 and relevant VAT/PAY/END-07 obligation owners. Acceptance: change a reviewed due date, revoke a feed, submit without acceptance and resolve a reminder; clients update the same calendar event, revoked access fails, and fulfillment remains tied to the required outcome. No statutory dates are invented by this plan.

### Additional breadth retained under existing owners

- Routine chart-of-accounts and bookkeeping-period operations belong to FND-03/PST/END-01: version account metadata, preserve historical references and enforce period/approval controls. Owner transaction reporting stays under COM-04/COM-06 and END-03.
- Mileage export and salary handoff remain EXP-2. Dimension/project reporting remains DIM-1–6; KPI reports belong to END-03 and require explicit formulas, source cutoffs and reconciled drilldown rather than unlabelled dashboard totals.
- Assistant chat, scoped knowledge/memory, classification and workflow suggestions belong to AGT-2 and PST-05. Retain reviewed interpretation provenance; recalled context is not current authority. Acceptance includes revoked knowledge access, stale suggestions and recovery without repeating approved effects.
- Shopify, WooCommerce, Stripe and Zettle are candidate COM-2/INT-1 provider profiles, not blanket support commitments. Banking, Skatteverket, Peppol and email use the same per-provider coverage inventory: supported resources, consent/authority, source/event identity, pagination/webhook replay, fees/refunds, cursor recovery, configuration and observed external outcomes. Select each concrete adapter before implementation; reconcile gross activity and clearing rather than posting net payouts as revenue.
- Firm/client operations remain IAM-1 and the frontend firm workflow. Each distribution must declare any hosted-only or unavailable connector and verify that its advertised capabilities match its deployment configuration. An adapter file or settings screen alone does not establish integration support.

### Assignment and progress accounting

Use canonical packets for implementation assignments and retain the capability labels as acceptance scope. AP-INTAKE, CRM-MASTER and DEADLINE-1 identify supplemental work; AR-LEGAL, COLLECTIONS and OPS-EXT are aliases of existing scope. Resolve each added section's stated contract gates before broad implementation. This reconciliation does not assign agents, activate integrations or schedule recurring work.

Keep implementation, runtime proof, actual-company readiness and external acceptance separate. The earlier percentage estimate remains approximate; adding a comparison inventory does not make it a measured completion score. The generated accounting index excludes supplemental capabilities and must not be used as the denominator for full-product completion.
