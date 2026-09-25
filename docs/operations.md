# Operations and review

Status: working design with partial implementation. [Area plans](plans/README.md) define delivery contracts; the [roadmap](roadmap.md) records observed results. The current trust boundary and replacement cutover are specified in [ADR 0010](adr/0010-application-owned-accounting-replacement.md); effect-mq durable delivery is specified in [ADR 0009](adr/0009-effect-mq-background-jobs.md). Neither ADR claims runtime proof.

## Shared operations

Define JSON-safe inputs, outputs and errors in `packages/contracts`. UI, REST, MCP and jobs call the same owning handler. Generate transport descriptions from those contracts. Each operation declares scope, permission, side effects, approval, idempotency, snapshot, atomicity and recovery semantics.

Preserve supported operation IDs, `/api/v1` routes and generated `/api/openapi.json`. Resolve and recheck entity/book scope for every resource, including ID-only URLs. [Shared contracts](plans/00-shared-contracts.md#common-operation-contract) own errors, cursors and the public contract; D-05 owns actual transport proof. Advertise only supported handlers.

## Application-owned replacement boundary

The application process owns authentication, authorization, policy, calculations, workflow decisions and scoped writes. Every financial group uses one book-scoped transaction and passes it through nested persistence. Lock authority before the book, then periods/accounts, domain resources, approval and counters. The database owns DDL, constraints, grants, row locks, receipts and the narrow integrity layer; it does not own feature workflows. Financial transactions use no session-level tenant context and no advisory locks.

A failed transaction produces no partial effect. A lost response is uncertain, so recover with the original idempotency key and receipt; never issue a fresh economic command automatically. Outbox intent commits with the financial group, but delivery is later and at least once. The selected effect-mq Bun worker owns queue claims, retries and leases; application progress, current authority, cancellation versions and financial receipts remain authoritative. Its session-preserving listener is a separate queue connection, not API transaction state.

The clean replacement uses `0001-schema.sql`, `0002-integrity.sql` and `0003-roles.sql`. There is no old-schema adapter, old-digest interpreter, dual writer, feature-function fallback or compatibility period. Public route and capability IDs may be retained while their implementation moves; no old SQL path remains live after cutover.

## Prepare, approve, execute, recover

Retain evidence → prepare a sealed plan → review exact effects → approve selected groups → execute → recover the durable receipt.

Preparation returns a complete plan or explicit blockers; it does not post. Edits create revisions. Validation records what was checked; execution rechecks dependencies and authority. Approval requests do not grant approval. Execution supplies references, never replacement financial content.

A sealed revision has immutable groups and separate execution progress. Each group is pending, blocked or committed with a receipt. Expiry/revocation stops new approval consumption without erasing prior results. Superseding one group cannot hide already applied or still-valid groups.

One group is the atomic boundary. Multiple groups require durable run admission, one receipt per group and recovery of unfinished work. An array in a schema does not prove multi-group support. Use the clean-baseline [seal contract](plans/00-shared-contracts.md#exact-values-and-canonical-identity); independent vectors remain D-03. Historical sealed records and evidence remain readable as dated records, not as an old-digest compatibility path.

Derive identity at the trusted server boundary. Agents may request review and execute within granted scope, but cannot mint human approval or activate their own mandate. Posting, payment, closing, filing and signature are distinct powers. Production OIDC/session inputs remain D-01; a synthetic operator token does not prove human review.

Errors name affected resources, missing/changed facts, retryability and a supported remedy. Business refusals are not transient failures. A timeout during commit leaves an unknown outcome; recover by the original identity. A missing receipt at one observation time does not prove cancellation.

## Human workbench

The [customer frontend plan](frontend.md) owns the workspace layouts, scoped routes, audience starting views and migration from the current all-sections page. Its [acceptance scenarios](frontend.md#acceptance-and-verification) apply the review and recovery requirements below to customer journeys.

Show the selected scope, missing evidence, exceptions, eligible approvals and completed work. Review joins original evidence, accepted/conflicting facts and exact financial/tax effects. Show assumptions, dependency changes and approval scope. Group equivalent cases while exposing exceptions.

Human and agent views use the same sealed plan. Query keys include entity/book and revision/snapshot/filter scope. Preserve drafts on failure, recover durable work after reload, and display financial success only after a receipt. Keep posted, reconciled, prepared, signed and accepted distinct.

Reuse StyleX components and Paraglide. Provide loading, empty, blocked, stale, denied, pending, uncertain and recoverable states. Verify accessibility through the [human journeys](verification-strategy.md#human-journeys). Stable links carry scope and immutable review references; optional chat opens the same operations and review screens.

## Governed rules and agent context

A resolved exception may propose typed predicates and a constrained treatment with evidence and positive/negative examples. Simulate against relevant history, expose differences/conflicts, then approve activation of that exact version and scope. Arrival order cannot resolve conflicting rules. A company rule cannot override jurisdiction policy or turn one approval into a universal treatment.

Retain selected model interpretations with source digest, extraction/prompt schema, model version, rule context and review status. Retries reuse that result rather than reinterpret approved evidence. Calculations use explicit facts/rates/rule versions. Store concise decisions and references, not private reasoning transcripts. Source prose and model confidence grant no authority.

Return compact scoped observations with snapshot, coverage, blockers and next actions. Distinguish source assertions, human confirmations and derived facts. Batch related reads; expand from summary to rows, lineage or source. Declare truncation and stable cursors. Aliases resolve to immutable revisions. Resource IDs grant no access. Durable checkpoints retain inputs, versions, results and pending work beyond a chat or transport session.

Keep the negotiated MCP catalogue deterministic. Discovery describes capabilities; it does not register tools a client never listed. Hosts may select subsets without changing semantics. Schemas describe encoded JSON and annotations do not enforce authorization. New protocols/transports require D-05 proof; platform task state cannot overrule business receipts.

Standing mandates require explicit operation/book/period/account scope, currency, validity, revocation and cumulative limits. Reserve/consume shared budgets atomically. Per-entry caps cannot enforce daily allowances. A mandate never implicitly authorizes payment, closure, signature or filing.

Evaluate proposal quality separately from accounting correctness. Use versioned, independently reviewed cases, accepted alternatives and holdouts. Measure correct outcomes, missed/false exceptions, duplicates, unnecessary questions, repeated retrieval, calls, bytes/tokens, cost and time on identical work. Efficiency cannot excuse omitted checks.

## Provider and delivery boundaries

Provider contracts specify environment, credential scopes, resource/format versions, pagination/detail coverage, quotas, idempotency, lookup and supported actions. Preserve raw records, retrieval metadata, exact values and errors. Missing, invalid, not-fetched and zero differ. Failed detail hydration cannot yield a complete import.

Coordinate token rotation and quotas across the actual provider/account scope. Transient refresh failure must not erase valid credentials or recovery state; distinguish expiry, revocation and invalid grant. Persist bounded retries and cursors. Callbacks verify signatures over defined bytes, replay policy and tenant binding before applying effects; durable event identity handles duplicates. Keep secrets out of evidence.

Persist external intent and artifact identity before sending. Distinguish unconfigured/test/production capability and pending/rejected/accepted/unknown outcomes. Look up an uncertain result before resubmission. An exported payment file or upload acknowledgement does not prove settlement or fulfilled filing.

Outbox delivery uses a bounded dispatcher and the selected effect-mq PostgreSQL store. effect-mq owns queue claims, heartbeats, retries and attempt history; application records own domain progress, cancellation versions and financial receipts. A stale handler cannot commit a business effect after its application version/fence changes, and duplicate delivery cannot repost the originating voucher. Detailed recovery belongs to the [operations plan](plans/07-restore-operations-cutover.md).
