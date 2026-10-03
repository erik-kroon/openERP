# P06 invoice defaults: owner brief and failure contract

Status: implemented and verified locally in the P06 worktree. Test-first commit `6bf688b` retains the initial failing public-boundary run. The final run passed all three feature journeys and the portable performance test. Full changed checks, current primary strict lint, frozen installation and integration passed. Main integration remains root-owned.

## Selected ownership

CRM owns separate immutable customer invoice-default and reviewed-recipient revision streams, scoped by book and party. Embedding the recipient in each terms revision was rejected: terms/language changes would supersede reviewed contact identity and blur evidence. One current email destination per party has explicit `invoice_delivery` and/or `payment_reminder` purposes and reviewed/withdrawn status. An operator review retains evidence, actor, time and reason; it is not independently verified mailbox ownership or delivery. Contact annotations never grant recipient or send authority.

Customer defaults retain calendar-day terms, the book's supported currency, en/sv language, and an optional exact recipient revision/digest reference. No foreign exchange or business-day terms are inferred. A small application operation applies retained defaults to an invoice date before line prices are complete; the P02 owning calculation rereads the selected revisions before saving. The commercial revision retains the copied defaults and their reference. Explicit due-date overrides remain overrides when unrelated fields change.

Catalog owns revisioned description, unit, price, optional reviewed tax-policy reference and active/archived status. Free-text tax descriptions remain assertions. New selection checks the current scoped revision/digest and rejects archived rows. An exact selection already copied into the retained target draft remains usable after master edits or archive. Historical reads and legal admission do not require that copied article remain current. Selecting new defaults is explicit; refresh never replaces entered draft fields.

For a selected article, the calculator uses the retained article price returned by the scoped resolver. A contradictory request price refuses. An uncatalogued row retains P02's explicit commercial input contract. VAT amounts still come from the retained qualified policy and exact calculator.

## Concrete change owners

- Shared schemas and HTTP/read-only MCP descriptions: `packages/contracts/src/crm-master.ts`, `catalog.ts`, `invoice-drafts.ts`.
- CRM/canonical composition and exact calendar-day calculation: `apps/api/src/application/commerce/customer-invoice-defaults.ts`, `draft-calculation.ts`, `invoice-lifecycle.ts`.
- Article revisions/archive/treatment: `apps/api/src/application/commerce/catalog.ts`.
- Passed-transaction persistence and typed table mappings: `apps/api/src/db/commerce/customer-invoice-defaults.ts`, `catalog.ts`, `schema.ts`.
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

## Integration obligations

P07's optional customer-facing note must survive the explicit `calculateCommercialContent` content mapping when its contract is integrated. P07's extracted revise owner must retain the book lock added here before draft resource locks. Template application may preserve catalog references only against the real canonical target snapshot. New template-created drafts reject stale or archived selections; refreshing the template rows is the recovery action. These integration obligations require proof after the branches are combined.

The first feature run retained stable source inputs in `test-results/product-P06-functional1`. The configured native PostgreSQL registry decodes `int8` as a string, while the catalog raw projection declared a bigint. Current-revision comparisons therefore refused valid selections. The projection now names the actual string boundary; arithmetic converts it explicitly. The final native PostgreSQL journeys pass after the projection correction.

## Feature checkpoint

1. `how` over the affected subsystem. Completed by tracing CRM annotations, article JSON revisions, commercial calculation and legal admission.
2. `architect` for parallel design exploration. Completed by parent review of separate recipient streams and embedded recipient alternatives.
3. Write the throughput checkpoint as four todo items.
   - Blocking first steps. Author public-boundary failures, install frozen dependencies and retain an initial failing run before production.
   - Independent workstreams. Contracts, persistence, calculator and callers are coupled by retained revision references; implement sequentially in this worktree.
   - Shared mutable state. This worktree owns P06 and migration0062. Parent owns integration and runtime scheduling.
   - Smallest safe decomposition. One worker owns the canonical copy contract and its callers to preserve one calculation authority.
4. Delegate code-writing to a subagent. This delegated worker owns the diff directly under parent review; no nested delegation is allowed by the task.
5. Verify on the matching surface. Public HTTP, MCP and the actual composer browser passed in the final local run.
6. Rebase into small, ordered commits. Stack follow-ups. Test-first checkpoint `6bf688b` is retained. The verified implementation checkpoint follows the retained failure-first commit.
7. If the design is contested, `interrogate` before shipping. Skip because parent synthesized and approved the competing designs.
8. Run Opening a PR. Skip because user directs main integration and parent owns publishing.


## Local verification receipts

`test-results/product-P06-final-local` retains four passing tests across two files in 50.76 seconds. Source integrity is stable at `41e14924371f4f51b3b316b5d859a221fd1216738fe05a9a96e953dbb91559e5`. The retained JSON contains exact copied defaults and draft revisions. The browser screenshot covers keyboard save and a CSS 200% zoom proxy. This is not native browser zoom proof.

The public journeys verify exact calendar terms, explicit due-date overrides, immutable article and customer copies after master revisions, stale and foreign references, forged article prices, recipient review boundaries, concurrent writes, read-only MCP and legal issuance after article archive. The browser exercises recipient review, defaults selection, archive, Apply, Save, reload and Replace. `/tmp/p06-resume-full.log` and `/tmp/p06-resume-primary.log` retain the final successful source gates.

The earlier `product-P06-browser3` recipient-field timeout remains inconclusive. Its Worker restart warnings do not establish a cause. A diagnostic rerun passed in 23.48 seconds without a production behavior fix or a timeout increase. The final complete run also passes. Failure capture now retains the actual page and screenshot if that boundary fails again.

The portable performance test uses 12 customers, 20 articles, five warmup pairs and 30 measured samples. The approved shared-program baseline is `96247e350b405022c08f8c86fa6d547567c68a27` in the P04 worktree. It is distinct from the original sales parent `aafbfbe4`. The copied portable test was removed after the baseline run. Baseline source integrity is stable at `b3ffb34e89bfd501ec0c738c92040a25fdec11d85c8c9152831ff2f42fbe1cc5`.

| Public operation | Shared-program baseline p95 | P06 head p95 |
| --- | ---: | ---: |
| Customer directory | 13.610 ms | 12.424 ms |
| Articles | 11.249 ms | 12.155 ms |
| Apply defaults | Absent, confirmed HTTP 404 | 14.926 ms |

The existing reads remain within the accepted regression allowance. Apply defaults meets the 1000 ms budget. Raw durations remain in `crm-catalog-performance.json` beside each source manifest. Reproduce the head with `OPENERP_E2E_ARTIFACTS=test-results/product-P06-final-local OPENERP_PERF_LABEL=p06-head-local bun run test:e2e apps/api/tests/invoice-defaults.e2e.test.ts apps/api/tests/invoice-defaults-performance.e2e.test.ts`. Use `OPENERP_P06_FEATURE_EXPECTATION=absent` and label the pinned shared-program checkout for the portable baseline.

An independent P05 worker reviewed the diff against the original sales parent and the new files. Its verdict found no correctness defect, narration or suppression. The review traced scoped transactions, current selection admission and copied historical snapshots. Integration still owes the P07 note and transaction-lock obligations above.
