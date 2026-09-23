# Continuous implementation — next packet

User objective: keep implementing; do not focus on tests, browser or mobile.

Source-only work continues with three retained owners. No test/fixture edits, validation commands, migration application, servers, dependencies, commits or external actions.

| Owner | Slice | Forward migration |
| --- | --- | --- |
| core-gap-map | Read-only bank match candidates with effective capacities, ambiguity and reasons; never automatic matching |1600-bank-match-candidates.sql |
| commerce-gap-map | Reviewed whole-allocation payment unallocation, immutable history and effective restored capacities |1700-commerce-allocation-reversals.sql |
| compliance-gap-map | Linked carrying-basis validity enforced at schedule preparation and posting, including stale prepared paths |1800-subledger-basis-posting-guards.sql |

Root owns shared registration, current/legacy composition, cross-domain source integration and maintained status docs. Historical migrations through1510 are not rewritten. New private commerce effective-allocation views must propagate to capacity/report/correction consumers without replacing active-bank semantics. Existing standalone synthetic schedules keep their interpretation; linked bases are not legal-policy activation. No new source-completeness or readiness claim follows from these slices.

Workers report final source handoffs or real blockers only. Source review and runtime proof remain distinct. No task is marked verified from source alone.

## Integrated follow-up

1600 shared composition and Accounts/Matching + legacy UI mounts complete in source.1700 shared composition, Accounts/Payment allocation and legacy UI mounts complete; existing receipts/reports show live release/allocation-freshness overlays. Independent1700 source review found no concrete blocker.1800 source reviewed and routed schedule UI mounted. No runtime validation.

Next retained assignments: compliance-gap-map1900 exchange-rate reviews; core-gap-map2000 bank interval coverage; commerce-gap-map2100 immutable synthetic issue documents. All forward/source-only, root integration still owns shared files.

1900 rates/conversion review registered in domain+contracts/API/MCP/SQL and mounted under Reports/Exchange rates plus legacy workspace. Owner is fixing form recovery when observed rate revision changes.2100 invoice artifacts wired through Effect workflow only and mounted beside committed synthetic issue receipts; independent security source review assigned.2000 source coverage still active.

### Root integration: statement-row candidate entry (failure cases before code)

A viewed statement must open candidate discovery for the exact retained row without retyping identifiers. A wrong statement response must refuse. Selected candidate state must reset on book/statement change. Switching candidate rows must not replace the existing manual match form or any pending match request. Discovery stays read-only, does not infer amounts/identity or submit a match, and links users to the reviewed matching workspace. No additional route or backend API is needed; reuse1600 BankCandidateResults. Source-only; no browser/runtime checks.

## Next packet after source integration1900–2100

Independent source review found no concrete blocker in1900 exact arithmetic,2000 coverage or2100 document rendering/sealing paths.1900 pinned-form and unknown-currentness fixes are complete in source. Root added per-statement-row candidate discovery and preserved concurrently added money formatting. No runtime validation.

Retained owners now: core-gap-map safe identifier-only candidate-to-allocation draft handoff (owns settlements/index.tsx plus candidate-local workspace; not bank-statement.tsx); commerce-gap-map2200 full native synthetic invoice cancellation, proposing cross-domain live/effective shape before broad edits; compliance-gap-map2300 evidence-backed manual-rate withdrawal. Root still owns shared composition and integration. Historical migrations through2100 must not be rewritten. No financial source delivery is accepted if aggregate/register/report dependencies remain open.

###2200 root shared-shape agreement (before source edits)

Cancellation must not erase original amount/recognition, allow new invoice revisions/allocations, hide reversal ledger rows, or relabel old snapshots as current. Add optional live cancellation summary and effective/cancelled amounts to current invoice/report schemas; old bodies must still decode. New status label must be explicit. Keep InvoiceRevisionForm mounted to retain uncertain requests; CommandForm retry is outside the allowed/new-command gate, so prohibit new revisions after cancellation without blocking saved-key recovery. Report columns distinguish missing historical fields from zero and display saved cancellation contributions; report status remains historical. Owner handles exact financial aggregate and forward SQL separately.

### Root issue-review recovery follow-up (failure cases before code)

A prepare/approve/execute request can have an uncertain response. A later failed query refresh currently changes isSuccess to false and unmounts its CommandForm, dropping captured request/key. Retain the last scoped review/draft data on query errors, gate new commands on a successful idle read after mount, and leave CommandForm exact captured retries available outside that gate. Confirmed issued receipt remains the historical success path. Do not interpret query failure as no issue, current approval or permission to edit. No test or runtime execution.

### Root integration update

Candidate handoff is source-integrated in both routed Accounts/Matching and legacy workspace through BankMatchingWorkspace. Only explicit discard/use candidate resets a draft; no amount, reason or acknowledgment is copied.2300 rate withdrawal is source-integrated through the existing exchange-rates contract/group/statements composition, with no ordinary MCP mutation. Core is independently reviewing2300; compliance is independently checking existing2200 downstream consumers for omissions. Root agreed and added optional cancellation schemas and historical report columns;2200 financial transition remains in progress. Root retained issuance cached forms on query-refresh errors and gated new commands on a successful idle post-mount read; saved-key CommandForm retries remain available. No runtime validation.

2200 independent preflight found that correction_impact_resources lacks1500 subledger_bases ownership: an issued voucher can back a carrying basis. Owner was directed to refuse cancellation when a scoped basis references the recognition voucher, including approval/execution rechecks.1800 future-post guards do not repair already-posted recognition. No other omitted consumer was found in this source review.

### Root parent recovery boundary (failure cases before code)

Independent source review found BookWorkspace unmounts all routed forms after a transient shared setup refresh error, losing captured commands despite leaf retention. Keep previously loaded setup/children mounted for non-access errors. Explicit Unauthorized/Forbidden/NotFound setup results still hide the scoped workspace; AccountingAccess authentication/identity gating and sign-out cache clearing remain unchanged. Thus recovery preservation is within the retained authenticated scope, not a promise to survive identity loss or auth-gate failures. Also fix duplicate outer sibling keys for legacy coverage/matching mounts.

## User error triage pause

User said "errors n shieet". Root paused all new feature work and asked permission for type/lint checks (no tests), or the observed app error. No validation authority has been confirmed yet. All three workers instructed to stop new edits.2200 is saved but incomplete: migration, invoice-cancellations contract/statements/routes and UI exist; shared package/API/dispatcher/handler wiring and UI mount NOT added. See apps/api/SYNTHETIC-INVOICE-CANCELLATIONS.md partial handoff. Basis-conflict refusal is in the resources path. Do not claim2200 source-ready or resume feature expansion before triage decision.

## Source-only error repair continuation

Goal continuation resumed bounded source fixes, not new domain expansion or validation commands. Root repaired concrete2200 package export/Api group/catalog/two read bindings/query statements/HTTP-layer registration gaps. Independent source financial review found no remaining blocker after the basis ownership refusal; execution remains unverified. Core reviews owned2200 contract/route/UI shape. Commerce is fixing current-approval-key remounting that can discard uncertain execute/revoke requests. UI mount waits that handoff. Source import search found no remaining undeclared contracts/domain package subpath in the scanned TypeScript source; this is not type checking.

2200 root integration completed after owner recovery fix: package/API/catalog/query/handler composition and issued-review cancellation panel mounted. Independent financial review has no remaining concrete blocker; core found no additional definite source/type/API-shape mismatch after registration repair. All claims remain source-only; original reported user error still has no supplied output or authorized type/lint diagnostic run. No new domain expansion was started.

### Source lint and access-error repairs

Workers fixed definite configured no-overzealous-destructuring violations in settlements/index.tsx, commerce/invoice-documents.tsx and exchange-rates/{forms,views,withdrawal-form}.tsx. No lint invocation or rule suppression.

Before the shared reader fix: malformed/non-JSON401/403/404 error bodies must still trigger explicit access/scope failures, not cached-setup retention. Valid structured ApprovalRequired and other domain errors must retain their codes. Successful response JSON/schema validation must remain strict, and non-access/network failures must not be mislabeled as authorization loss. HTTP status is available even when parsing its failure body fails. Fix readAccounting at the common boundary, not each form. No tests/checks run.

### Prior-denial recovery case (before fix)

Source reviewer found setup success → explicit403 → generic500 retry could re-expose cached setup because only the latest error was checked. Latch a denied/unconfirmed scope until a successful idle post-mount scoped setup fetch; initialize blocked on every mount and force mount refresh. Ordinary transient failures after a confirmed scope preserve forms. Explicit denial still immediately unmounts them, and a remount cannot rely on a cached old success. No hidden wrappers (which would not contain portaled dialogs), query-cache mutation or auth fallback is needed. No tests/checks.

The prior-denial latch received a narrow independent source review with no blocker found: initial mount needs fresh scoped success; confirmed scope retains forms on ordinary transient errors; explicit denial stays blocked through later generic failures. AccountingStatus now shows pending while a blocked cached scope is being rechecked. No execution proof.

### Issuance committed-status recovery (before code)

1400 UI still removed prepare forms when issue history became issued, and approval/execute forms when a receipt appeared. That can discard an uncertain command completed through another approval/review or a successful fetch after an ambiguous response. Keep existing form positions mounted, gate only new commands on current unissued/operator state, and leave captured-key retry/download available through CommandForm. Historical issued receipts/documents remain separate. No new API/financial behavior or tests.

### Existing workflow recovery follow-through

Root1400 preparation/approval/execute forms now stay mounted after issuance appears; only new commands are disabled, while captured request retry/download survives. Commerce owner applied equivalent1700 release recovery, with stable retained approval rows and successful idle fetch gating; backend automation execution authority unchanged.

Core has explicit delegated ownership of router.tsx (and one helper only if needed) for request-scoped Unauthorized handling from any read/mutation. Cancel/remove accounting query state and close books gate; preserve403 ApprovalRequired/transient failures. Old cleared request callbacks must not log out a new session. This is bounded error repair, not feature expansion. No checks/runtime.

### Request-scoped auth-loss repair delivered

Core changed router.tsx and accounting-access.tsx only. Current-cache typed Unauthorized from reads/mutations cancels accounting reads, null-notifies current books gate, removes accounting Query instances, retires mutation cache and seeds fresh null books gate. Cache-object membership guards ignore retired callbacks. AccountingAccess no longer swallows /books401; null disables automatic retries until login resetQueries restores a fresh read. Source rationale: /Users/admin/.prime/agent/session-artifacts/01a0cd4f-12f6-756f-bb98-e326197e1ae3/sub-ceeb3deb/AUTH-LOSS-BOUNDARY.md. No runtime proof. Independent source review assigned compliance. Existing component-local SignOut onSuccess can still run after cache retirement; this is a recorded separate race, not solved by global callbacks. Ordinary /books errors still use the existing fail-closed ancestor behavior; do not overclaim universal form retention.

Independent auth-boundary source review found no new concrete blocker and traced installed TanStack reset/observer semantics. Router/client remain request-scoped. No runtime claims; existing detached component-local SignOut callback race remains outside this bounded fix. Current source hashes are in error-repair-source-manifest.json (shared contributions, not an atomic tree or validation artifact).

###2000 coverage currentness follow-up (before edit)

Saved report bytes may remain verified when a later dependency refresh fails, pauses or is in flight. BankSourceCoverageInspector currently shows the old currentness during fetch and removes the report on error. Retain only previously verified cached data, report currentness unknown unless successful idle fetched-after-mount, and leave exact saved bytes downloadable. No money recomputation, new endpoint, readiness waiver or check/test. Match the existing1900/subledger-control pattern.

### Bounded currentness/recovery source repair assignments

Root completed2000 cached artifact/unknown-currentness fix. Active retained workers: core bank settlements/review.tsx + bank-match-reversals/review.tsx; commerce ordinary commerce/allocations.tsx; compliance closing/review.tsx + accountant-review/inspector.tsx with copy modules as needed. Scope is concrete stale-status/new-action gating or uncertain-key loss only, no new features/SQL/frameworks/tests/checks. Preserve root overlays, concurrent money formatting, exact authority and authentication clearing. New commands need successful idle current reads; saved-key replay remains separately available.

### Post-mount action-read admission (before edits)

Router queries default to30-second freshness. Adding isFetchedAfterMount gates without forcing a read can leave recently cached financial reviews permanently disabled until manual refresh. Cancellation preparation's setup observer can hit this on its first mount after the parent loaded setup. Set staleTime0/refetchOnMount always only on reads that admit new review commands; keep immutable historical artifact downloads independent of live freshness. No API/writes/checks changed.

Bank allocation/unmatch, ordinary payment allocation, closing and accountant-review repairs are source-delivered. New actions distinguish unknown cached status from successful idle reads, and captured requests survive live status changes. Root additionally enabled fresh-on-mount reads on actionable review queries so post-mount gates do not strand freshly cached views. Historical-only artifact reads were not broadly forced to refetch. No validation commands or runtime acceptance.

### Authenticated book-list transient recovery (before edit)

AccountingAccess still unmounts the entire feature tree on a temporary /books refresh failure, discarding captured requests despite leaf recovery fixes. Preserve an already-authorized cached book list during transient errors, with visible error/retry UI. Explicit401/403/404 or a null auth gate must block immediately and remain blocked through a later generic failure. A remount seeing a cached error starts blocked until success. Do not use isFetchedAfterMount to reopen login after resetQueries: reset counters can equal an observer's captured initial count. Successful idle non-null data clears the local denial latch; global Unauthorized cache retirement stays authoritative. No checks/tests or backend changes.

Book-list transient retention latch independently source-reviewed with no blocker. Remaining explicit predicates using !isFetching on cached data assigned narrowly: core source-intake/review.tsx; commerce recurring-rule.tsx; compliance owner-register/owner-register-panel.tsx. Fix paused/currentness/new-action admission and captured retry loss only; no new domain/API/SQL/checks. Scope is existing behavior error repair.

The recurring-rule and owner-register repairs are delivered. Source-intake review/workspace repair is also complete, including initial-null preview pinning, an occupied mapping slot that survives background admission/latest-preview changes, and exact-variable retries. Concurrent PreviewStatus/PreviewReceipt extraction and formatting were preserved; attribution is another workstream, not this root. All source-only; no checks/runtime. Workers are idle with no new assignments.

### Sign-out local cache handoff (before edit)

Installed TanStack mutation source calls the mutation-local onSuccess even after cache retirement. SignOut currently awaits cancellation then unconditionally clears/seeds the client, so an old result can erase a replacement books gate. Capture the exact books Query object when the HTTP mutation starts; check identity before cancellation and again after its await. Successful same-gate logout must notify the existing books observer with null before cache removal, then seed null for future observers (same two-write rationale as the global Unauthorized path). Ordinary refetches preserve Query identity and must not suppress cleanup. Missing/retired gates must not clear a replacement. This guards local cache cleanup only: overlapping Set-Cookie responses and cross-tab identity changes remain unresolved. No tests/checks/runtime.

SignOut local cleanup guard is implemented and independently source-reviewed with no blocker in its stated scope. The before/after-await Query identity checks prevent this old callback from clearing a replacement gate; null notification precedes retirement. Overlapping cookie responses, cross-tab authentication and other component-local callback races are still outside this fix. Shared-contracts plan updated. No checks/runtime. All workers idle again.

### Sign-in local cache handoff (before edit)

Login still cancels/resets all queries unconditionally after a response. A removed Login mutation can finish after its books gate was replaced, or after another Login on the same gate already reopened the workspace. Capture the gate at HTTP start; before cancellation and after its await, require exact current Query identity AND its null signed-out sentinel. Only an unchanged signed-out gate may reset to enable a fresh /books read. Ordinary sign-in retains existing cancellation/reset behavior. Missing/replaced/already-reopened gates must not reset newer workspace state. This does not serialize authentication cookies or prove identity freshness. No tests/checks/runtime.

Sign-in cache cleanup guard implemented: exact current books Query plus null signed-out sentinel, checked before cancellation and again after await; normal login still resets to enable fresh books read. Auth-cookie serialization remains out of scope. Independent invoice-document workflow review found no concrete capture/replay loss or public raw-seal escape in owning HTTP/MCP paths; no execution proof. Core backend error-mapping source review remains active; commerce/compliance idle.

### Database transport error classification (before edit)

Core source review traced pg socket ECONNRESET/EPIPE/ETIMEDOUT → SqlError.reason.cause → EffectDrizzleQueryError Cause → queryFailure. Because PostgresFailure accepts a string code, these transport codes enter the SQLSTATE branch and fall back to InternalError/HTTP500. Recognize exactly these transport codes as Unavailable/HTTP503 while preserving intentional P0001 domain failures, current availability SQLSTATEs, unknown-code InternalError and uncoded SqlError fallback. Never forward raw error text/parameters or automatically retry a write: a lost response may follow commit. Source cases: each of the three transport codes, existing08/53/57014/57P0x codes, known P0001 domain detail, unknown SQLSTATE/Node code, malformed/uncoded cause and non-SqlError wrapper. No tests/checks/runtime; Effect CLI is not run under source-only restriction.

Database queryFailure availability classification now recognizes the three traced transport codes. API README documents redaction and uncertain-write recovery with original input/key. No automatic query retry added; existing HTTP status map provides503 for Unavailable. Source review of final classifier/runtime consumers pending with core; other workers idle.

Final source review of the transport-code repair found no blocker. HTTP/MCP return the mapped failure without retry; no application runtime branch uses Unavailable to newly retry writes. Existing preparation recovery is unchanged. External caller503 retry policies remain outside this repair. No checks/runtime. All retained workers idle with no pending assignment.

Next bounded source-only backend reviews started: core retained-file upload/get plus SQL transitions; compliance durable preparation-job runtime/SQL recovery; commerce HTTP bounded-request admission/caller. Read-only, at most grounded findings, no new features or execution. Root read preparation-jobs/source-retention/body/index; no root finding established yet.

Background-job UI recovery is assigned to commerce in preparation-background.tsx. Root caller fix: preparation-run.tsx currently admits paused cached run state via !isFetching; require successful idle postmount read and force that read. Existing recurring-preparation.tsx keys PreparationRunPanel by runId, so explicit run navigation already clears memory-only command state. No expansion of manual run actions.

Two grounded backend recovery fixes now authorized, no new domain expansion: compliance owns forward2600-preparation-job-recovery.sql plus automation handoff; commerce preparation-background.tsx UI replacement request/retry (root owns already-fixed preparation-run.tsx caller gate); core owns forward2700-source-upload-replay.sql plus source-retention.ts private optional completed admission result and handoff. Historical0940/0910 frozen. Concurrent2400-workspace* and2500-firm-workspaces migrations are not this root's work; preserve them. SQL2600 must stop obsolete job and admit replacement atomically under book lock without executing/resuming a run; SQL2700 must authorize/compare exact input before completed receipt replay, while fresh uploads still verify bytes. Both will remain unapplied/runtime-unverified.

2600 and2700 delivered in source. Root independently read forward SQL/workflow and latest background UI; no remaining concrete blocker found. UI immutable-admission-receipt/live-job overwrite follow-up is fixed (invalidate latest job rather than seed with replay), unknown/last-read cached status explicit. Preparation-run parent now forces fresh postmount idle admission; scoped/run-keyed lifetime traced. Owning docs/API handoffs and completion-wave plan updated. Both migrations unapplied/runtime-unverified; no checks. Three workers now idle; no further assignments.

Next source-only artifact recovery review: core VAT workflow/capture/seal; commerce SIE workflow/capture/seal. Read-only bounded findings, no legal/profile expansion or execution. Compliance idle. Root read both owning workflows and VAT pure calculation; no root defect established yet.

VAT and SIE source reviews complete with no grounded defect found. VAT pre-replay calculation is currently bounded/pure and no reachable non-ordinary failure was established; no speculative hardening applied. SIE returns existing scoped artifact before rendering and preserves exact stored bytes. No edits/checks/runtime/legal-profile claim for either slice. All retained workers idle again. A useful next bounded investigation is web query-cache writes: verify every setQueryData value matches its owning read schema and distinguishes immutable command receipts from live/latest views (as fixed for preparation background).

### Command-receipt versus live query caches (before root bank edit)

1300 import_bank_statement replays its saved original receipt; get_bank_statement instead reads effective active matches and the live checkpoint. BankImport currently seeds that live query key from the immutable import receipt, restoring released/old matches or an old checkpoint and marking it fresh. Replace cache seeding with a scoped cancellation then invalidation; preserve navigation and reconciliation invalidation. Installed TanStack query.ts only cancels an in-flight fetch on invalidate/refetch when cached data is defined; an initial in-flight read can otherwise be reused and finish with pre-command state. Explicit cancelQueries before invalidation covers that initial-read race too. Cases: initial import; same-key replay after match/unmatch/checkpoint changes; active initial read; inactive cached view; exact input/key preservation. No tests/checks/runtime.

The same initial-read coalescing race also applies to the prior preparation-background receipt/live-query fix. Root will cancel the two exact scoped job/run reads before invalidating them; no receipt is written into live caches and no write retry is added.

Live cache repair delivered in bank-import.tsx, recurring-rule.tsx, preparation-run.tsx and preparation-background.tsx. Bank import/create-run/advance-run no longer seed live read keys from saved command replay; target reads are cancelled before exact invalidation to avoid coalescing an older initial request. Background job/run invalidation received the same exact-read cancellation. Immutable ChangeSet/simulation/report caches left unchanged after SQL/read-schema trace. SavedPostingRequest mutation returns a freshly built envelope, not an old receipt envelope; unchanged. Shared-contracts plan updated. No checks/runtime. All workers idle, no pending assignments.

### Typed write uncertainty (before edit)

RunCommands treats every AccountingError as definitive, so typed Unavailable from a lost database connection (including after commit) unlocks new inputs instead of retaining exact retry. InternalError also cannot establish rollback (for example response decoding after commit). A shared web predicate will classify non-domain errors plus typed Unavailable/InternalError as uncertain; null and definite domain refusals keep existing behavior. RunCommands will keep the original variables/key and block replacement; AccountingStatus(write=true) must not hide uncertainty solely because the error is typed. Read messages remain unchanged. Failure cases recorded: generic network/schema error, both ambiguous typed codes, null, definite InvalidJournal/StaleDependency/ApprovalRequired, pending retry, failed current-read gate. No tests/checks/runtime.

Typed-write uncertainty repair delivered: shared isUncertainWriteError in accounting-api.ts covers generic errors plus Unavailable/InternalError; RunCommands locks new actions and retains exact retry for them; AccountingStatus preserves typed service text and adds uncertainty warning for writes only. Existing definite refusal/read behavior unchanged. Independent durable saved-posting trace found no analogous bug: transport errors retain identity, refused envelopes require validated persisted outcomes, and SQL subtransaction refusal allowlist excludes Unavailable/InternalError. Shared-contracts plan updated. No checks/runtime. All workers idle.

Backend authentication review found no direct header/session admission defect. New cross-boundary integration defect CONFIRMED: concurrent2501/2502 identity disable affects API tokens as well as sessions, but provisioning deletes only browser sessions, preserving API credentials and potentially memberships.0940 stored API-submitter authority checks therefore miss disabled requested_by; separate enabled agent can keep preparing, and2600 same-executor replacement refuses. Compliance owns forward2800-preparation-identity-admission.sql plus automation handoff: shared-lock original requester admission between credential/session and membership/book before fresh execution; nonlocking disabled-requester obsolescence in current admission. Missing admission row keeps2502 legacy behavior. Historical/concurrent migrations untouched, no API/role expansion/checks.

2800 delivered in source. Root read full replacement functions: execute adds nullable identity flag/share lock before membership/book and fresh-step stop on false; admit adds only nonlocking disabled-requester obsolescence. Other behavior/signatures preserved, no composition needed. Core independent review pending; compliance/commerce idle. AUTOMATION.md and completion-wave plan updated. Migration unapplied/runtime-unverified, no checks.

Independent2800 source review found no blocker in the stated scope. Existing-row requester admission lock order, fresh-step stop, absent-row compatibility, replay ordering and atomic replacement were confirmed in source. No compilation/concurrency/runtime proof. All workers idle/no pending assignments.
