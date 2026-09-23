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
