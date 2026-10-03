# P06 invoice defaults: owner brief and failure contract

Status: design and pre-implementation failure vectors. No implementation or runtime proof is claimed by this document.

## Selected ownership

CRM owns separate immutable customer invoice-default and reviewed-recipient revision streams, scoped by book and party. Embedding the recipient in each terms revision was rejected: terms/language changes would supersede reviewed contact identity and blur evidence. One current email destination per party has explicit `invoice_delivery` and/or `payment_reminder` purposes and reviewed/withdrawn status. An operator review retains evidence, actor, time and reason; it is not independently verified mailbox ownership or delivery. Contact annotations never grant recipient or send authority.

Customer defaults retain calendar-day terms, the book's supported currency, en/sv language, and an optional exact recipient revision/digest reference. No foreign exchange or business-day terms are inferred. A small application operation applies retained defaults to an invoice date before line prices are complete; the P02 owning calculation rereads the selected revisions before saving. The commercial revision retains the copied defaults and their reference. Explicit due-date overrides remain overrides when unrelated fields change.

Catalog owns revisioned description, unit, price, optional reviewed tax-policy reference and active/archived status. Free-text tax descriptions remain assertions. New selection checks the current scoped revision/digest and rejects archived rows. An exact selection already copied into the retained target draft remains usable after master edits or archive. Historical reads and legal admission do not require that copied article remain current. Selecting new defaults is explicit; refresh never replaces entered draft fields.

## Concrete change owners

- Shared schemas and HTTP/read-only MCP descriptions: `packages/contracts/src/crm-master.ts`, `catalog.ts`, `invoice-drafts.ts`.
- CRM/canonical composition and exact calendar-day calculation: `apps/api/src/application/commerce/crm-master.ts`, `draft-calculation.ts`, `invoice-lifecycle.ts`.
- Article revisions/archive/treatment: `apps/api/src/application/commerce/catalog.ts`.
- Passed-transaction persistence and typed table mappings: `apps/api/src/db/commerce/crm-master.ts`, `catalog.ts`, `schema.ts`.
- Migration `0062-customer-invoice-defaults.sql`: scoped pointer/revision tables for defaults and recipients, immutable-row triggers, bounded JSON, deferred current-pointer integrity and scoped runtime grants. Existing article JSON revisions retain archive/treatment state without rewriting earlier bodies.
- HTTP adapters `apps/api/src/transport/http/routes/crm-master.ts`, `catalog.ts`; MCP application registration `apps/api/src/application/capabilities/commerce-invoices.ts`.
- Minimal existing directory/composer callers: `apps/web/src/components/commerce/counterparties.tsx`, `catalog-articles.tsx`, `invoice-drafts.tsx`, `invoice-draft-session.tsx`, `invoice-editor-lines.tsx`. No layout or styling redesign.

## Independent pre-code vectors

1. Fourteen `calendar_days_v1` days from 2026-10-02 yields 2026-10-16. Fourteen days from 2028-02-20 yields 2028-03-05. Date and day bounds reject unsupported calendar results.
2. Choosing defaults with an explicit 2026-10-20 override keeps that override after title/line changes. Refresh or master edit cannot replace it.
3. Two hours of article revision 1 at 100000 minor units with a retained qualified 25% policy yields net 200000, tax 50000, gross 250000. Editing the article to 150000 leaves the saved revision and digest unchanged; a new explicit selection yields net 300000, tax 75000, gross 375000.
4. A new selection of stale revision 1 or an archived article refuses. The already copied revision remains readable and usable during unrelated draft edits and real legal issue.
5. Unsupported tax text without a qualified reference leaves VAT and gross unknown. Arbitrary policy text or contact annotations authorize neither tax nor delivery.
6. Defaults and recipient update with an obsolete expected revision/digest refuses. Retry of the same committed request returns its exact receipt; a changed payload with the same key refuses.
7. Defaults, recipient and article references from another book refuse before a draft write, including a collision on article code/revision. Refused writes leave the complete immutable inventory unchanged.
8. Unsupported currency, business-day terms, malformed destination, duplicate purposes, noncustomer party, missing/foreign evidence and agent writes refuse.
9. Terms/language edits keep the exact reviewed recipient reference. Withdrawn or superseded recipient revisions refuse new defaults/dispatch admission; historical copies remain audit facts. Recipient review itself grants no message-send approval.
10. Ordinary read-only MCP sees the same scoped defaults/recipient/article records. It cannot approve a send. Private annotations are not used as a defaults or recipient oracle.
11. The existing editor receives copied defaults and article treatment through actual caller wiring. User overrides and origin references survive recovery. Keyboard and 200% zoom use existing owned controls.

`apps/api/tests/invoice-defaults.e2e.test.ts` is authored before production changes. It exercises public HTTP plus the existing browser and retains literal expectations, immutable receipts, screenshots, performance timings and source-integrity manifests. Synthetic fixtures only; no live contact, provider or company-data use. Parent/trunk/head measurements and operator review remain separate evidence obligations and are not inferred from implementation.

Principles: Model the Domain separates recipient review from reusable commercial defaults; Boundary Discipline resolves retained revisions inside the owning transaction; Make Operations Idempotent reuses retained receipts; Test Behavior Not Implementation and Prove It Works require public-boundary proof; Sequence Verifiable Units keeps defaults application, draft calculation and eventual dispatch admission distinct.

## Feature checkpoint

1. `how` over the affected subsystem. Completed by tracing CRM annotations, article JSON revisions, commercial calculation and legal admission.
2. `architect` for parallel design exploration. Completed by parent review of separate recipient streams and embedded recipient alternatives.
3. Write the throughput checkpoint as four todo items.
   - Blocking first steps. Author public-boundary failures, install frozen dependencies and retain an initial failing run before production.
   - Independent workstreams. Contracts, persistence, calculator and callers are coupled by retained revision references; implement sequentially in this worktree.
   - Shared mutable state. This worktree owns P06 and migration0062. Parent owns integration and runtime scheduling.
   - Smallest safe decomposition. One worker owns the canonical copy contract and its callers to preserve one calculation authority.
4. Delegate code-writing to a subagent. This delegated worker owns the diff directly under parent review; no nested delegation is allowed by the task.
5. Verify on the matching surface. Pending isolated HTTP, MCP and actual composer browser proof.
6. Rebase into small, ordered commits. Stack follow-ups. Pending test-first and coherent implementation checkpoints.
7. If the design is contested, `interrogate` before shipping. Skip because parent synthesized and approved the competing designs.
8. Run Opening a PR. Skip because user directs main integration and parent owns publishing.
