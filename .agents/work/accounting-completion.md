# Accounting completion goal

User authorized a persistent goal and sub-agents for the listed partial and missing accounting capabilities. Implementation is not company readiness or external acceptance. New/changed tests are not authorized yet; explicit approval requested in chat.

## Baseline

`bun run check-types` passed, including web build. Existing `bun run test:e2e`: 17 passed, 3 failed. Expiry fixture attempts an immutable approval update; cookie fixture targets removed token-login API; Chromium executable missing. Do not weaken runtime protections. Receipts: `accounting-completion-baseline/`. These observations do not verify newly implemented domains.

## Active work

- commerce: COM-06 immutable ageing/register-to-ledger snapshots. New register-reports contracts/API, SQL `0920-commerce-register-snapshots.sql`, commerce-local UI. Exact amounts, fixed basis, explicit incomplete coverage, durable reads and JSON download. No postings.
- reports-closing: END-01 evidenced family applicability declarations and new complete-inventory technical-close scope. SQL `0930-closing-family-inventory.sql`, closing-local contracts/API/UI. Preserve old bank-only interpretation, fail closed for missing/unsupported providers, never waive observed failures; statutory readiness stays false.
- tax-payroll: primary-source research for a narrow VAT-return profile, exact official rounding/aggregation/sign/effective-date rules. New research doc only. No pretend payroll calculator or production activation.
- root: shared contract exports/API/capabilities/dispatcher and MCP integration, diff review, serialized validation and maintained roadmap evidence.

Another live root session `01a0c96b-3987-720a-a379-3bf855d10e1a` owns concurrent shared frontend/self-host work. Coordination requested; preserve all its changes. Do not treat old `.agents/work` instructions about missing git or seven retained agents as live session facts.

## Gates

The user has now stopped test and validation work: implementation and source review only. Do not run checks or add/change tests or fixtures. No production data use, filings, payments, provider connections, deployment, commits or pushes authorized. All existing migrations immutable. New synthetic runtime acceptance must retain exact receipts and independent controls; static passes alone do not verify financial behavior. D-04 company facts, D-08 reviewed legal profiles, and D-10 external accounts/authority remain open. Whole goal remains active and incomplete.

## MCP integration boundary

Risk: a domain adds a shared capability but its runtime binding is omitted, or a runtime-only binding advertises an undeclared operation. The runtime registry now satisfies the exact shared capability-key set at compile time. Operator-only approval/activation remains outside that set. Initialization directs callers to the live catalog and book readiness, not a stale hand-maintained family list.

Observed: API typecheck passes; project-native imports show all 110 declared capabilities bound with identical keys. The existing MCP E2E is being rerun after the change; no tests were added or changed. This protects key coverage, not semantic equivalence of every operation.

## Integrated source checkpoint

Root wired register-report package export, API group, handlers, shared capabilities and typed SQL statements. Closing0930 reuses existing bindings. Shared native module import succeeds after fixing the unsupported Effect constraint. Commerce is hardening its list to use a scoped fixed cutoff and enforcing full materialization counts before runtime validation. Independent reports-closing read-only review found no additional arithmetic/scope defects at its pinned0920 revision; it did not execute SQL.

Tax-payroll now owns1000-vat-return-drafts.sql and new VAT return modules/UI: exact bounded draft calculations, immutable source/ledger basis and explicit non-filing readiness. Root must connect its dependency hook into closing so new VAT facts cannot be hidden by a tax-not-applicable declaration. The official research is docs/sources/vat-return-profile-research.md. No legal profile is activated.

The other root confirmed it is idle and has no shared writer collision. Its owned Worker19788 stopped on the transient invalid Effect import; do not restart or touch its PG55472. Root validation remains isolated and must wait for a coherent migration/source checkpoint.

## Frozen validation and next slice

A writer outside the reachable Prime roster added0940-preparation-jobs.sql and shared workspace/job code. Preserve it; do not attribute or claim its verification. VAT migration is reserved as1000 (renamed while unapplied), SIE transaction artifacts as1100. Both are excluded from first-wave validation while in flight. reports-closing now owns the1100 SIE4I artifact slice; it is not4E/full export.

Frozen copy: .cache/accounting-wave-validation-01, with captured-source-hashes.json. It contains integrated0920/0930 and excludes unreviewed0940 plus in-flight VAT. Uses the exact installed Bun/workspace dependencies through links, not newly installed packages. Initial frozen typecheck failed because workspace-local dependency links were omitted; that environment setup was corrected and the check restarted. No source/type/lint rules were weakened.

## Implementation-only checkpoint

User explicitly stopped tests/test writing; root also stopped validation commands and notified all children. Prior frozen E2E completed17/20 including MCP, with the same baseline failures. Source hashes, logs and exact migration manifest are retained in accounting-completion-wave-01/. Manifest includes1000-customer-workspace.sql; it excludes0940-preparation-jobs.sql and in-flight VAT/SIE. Frozen lint selected zero files due to its ignored.cache location; it is not a lint pass and format did not run. No more checks will be started.

VAT shared package export, API group, Worker handlers, parameterized SQL dispatch and five MCP capabilities are integrated in source. Preparation uses the sole trusted Effect calculator; fact recording remains operator-only REST. VAT panel is mounted under vat-returns with a scoped key and navigation entry. No new validation performed. tax-payroll owns forward1001-closing-vat-dependencies.sql and its provider contracts/views/docs;0930 remains unchanged after frozen application.

commerce now implements native customer-invoice commercial drafts/revisions in reserved1200-invoice-drafts.sql and disjoint invoice-drafts modules. This does not issue numbers, post, or deliver. reports-closing continues1100 SIE4I only. Root integrates shared joins after handoffs.

## VAT closing dependency handoff

Forward1001-closing-vat-dependencies.sql is implementation-ready and source-reviewed, not executed. It binds the whole VAT hook (including saved draft count) into closing dependency equality and new accountant-review-v2 packs/CSV manifests. Nonzero facts or drafts contradict tax N/A; required tax controls remain unavailable. Historical contract fields stay optional and old artifact bytes/replays remain unchanged. No additional root routes/bindings are required. SIE owner was informed to support both immutable accountant-review generator versions.

## SIE source composition

Root connected ./sie export, SieApi/SieHandlers, capability catalog and four Effect capabilities, plus typed sieStatements dispatch. Prepare/resume keep capture→render→seal outside the DB transaction and expose no public seal. Accountant-review inspector already mounts owned SIE panel. Source review found that line IDs must be voucher-scoped and that list cursors must bind scope; reports-closing is fixing both in unapplied1100/encoder/contracts/UI. Do not mark this integration accepted until that handoff. No tests or validation commands ran.

## Revised SIE handoff

reports-closing delivered both source-review fixes: encoder duplicate detection uses voucherId:lineId; si1_ cursors bind normalized scope/cutoff/after with complete ordinal membership. List response now includes scope/cutoff/total/first/items/next and excludes mutable seal status; GET remains the current artifact-state source. UI retains first cursor across retries/invalidation and refreshes membership only explicitly. Root reviewed the revised source; shared signatures/bindings need no further change.1100 remains unapplied and unvalidated. Invoice-draft1200 implementation continues with commerce; tax-payroll and reports-closing have delivered their current slices.

## User-requested TypeScript error repair

User reported “errors” then “ts”, authorizing targeted TypeScript diagnosis/repair. No tests resumed. The targeted checks found API errors caused by the in-flight invoice-drafts module lacking its root-owned shared export/API/database/capability registration. Root added those joins and InvoiceDraftHandlers; operator-only draft mutations remain outside MCP, whose three added tools are read-only. A targeted contracts/API/web tsc rerun is in progress. Other validation remains stopped; invoice draft UI/SQL handoff is still with commerce.

Targeted contracts/API/web TypeScript recheck passed after invoice-draft registration. No tests, builds, lint, formatter or runtime checks were run for this repair.
