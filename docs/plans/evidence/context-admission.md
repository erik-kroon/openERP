# Bounded context admission

## Durable continuation implementation — 2026-10-01

`apps/api/src/application/agent/continuation.ts` composes the existing context
owner inside the admitted transaction. Migration `0056` retains immutable,
principal-scoped captures and append-only discovery progress. REST and MCP expose
capture, page and advance operations. Pages contain at most50 work references;
the exact page digest and expected progress revision bind acknowledgement.
Acknowledgement is not execution, approval or resolution. Historical pages remain
readable while `current=false`; stale progress refuses and a fresh capture recovers.
Original financial owners still revalidate execution.

`test-results/context-durable-restart-20261001` records two passing real
PostgreSQL/workerd E2E cases with no skips. Independently generated103 journal
identities are recovered over50/50/3 pages, replay preserves capture/progress,
another book cannot read the capture, execution invalidates progress, and fresh
capture contains102 unresolved records. A separate MCP journey closes its serving
Worker, starts a replacement against retained PostgreSQL, and resumes at50 with
the final record. JSON journey artifacts, runtime/migration manifest and stable
source inventory are retained. The full changed-file gate passes.

Packet6 remains open: current adapter coverage does not establish all unresolved
application owners; supported-empty/unsupported/unknown registry and owner-backed
delta delivery still need acceptance. Capture construction and fresh checks retain
the existing full internal traversal; only continuation responses are item-bounded.
This proof does not claim bounded capture memory or whole-company completeness.

## Packet 6 continuation update — 2026-10-01

The context owner now follows the existing workspace cursors until both selected
inventories are exhausted. Each database query remains bounded to51 rows; attention
advances by its retained key, journals by retained creation timestamp/identity.
Both traversals run in the original admitted book SHARE transaction. Repeated
cursors fail closed. The public response remains a freshly ranked complete
inventory of the currently supported adapters, not a frozen cross-request page.
No new financial facts, approvals, grants, tables or dependencies were added.

Failure-first `test-results/context-continuation-red-20261001` reproduces the old
selected51-row refusal. Focused proof `context-continuation-recovery-20261001`
passes3 selected cases,10 unselected: selected51 mixed rows,51 journals with current
membership revocation, and103 journals traversing three database pages. A fresh
authenticated session rediscovers all103 exact retained identities; executing one
through the posting owner removes only that item on fresh capture, retaining
fullCount103/openCount102. Context reads change no financial state. Artifacts
retain exact expected IDs and exchanges; this is new-session recovery, not a
worker-process restart claim. Full changed-file lint/type gate passes.

Consolidated context/expense-owner suite `context-traversal-combined-20261001`
passes13/13 with zero failed/skipped on unchanged source. This includes the
retained selected-period, missing-fact, same-row revision and expense-authority
regressions; it is not a workspace-wide baseline claim.

Packet6 remains incomplete: immutable capture, externally resumable continuation,
explicit durable progress, complete adapter registry and delta delivery remain.
The historical50/51 refusal evidence below describes its recorded source only.

## Historical bounded admission

This unit originally preserved the released context/ordinary attention contracts, current book authority and the selected status=all50-row admission bound. Packet6 remains incomplete: immutable capture, continuation, durable progress, complete adapter registry and delta delivery are separate work.

Failure-first context test source is committed at `f71fc67b4b50b36179db76fffbebb028d3e3f692`. Its exact committed-head run `test-results/context-admission-red-committed-20261001` retains5 failed/6 passed with stable source. Invoice/expense review digests were supplied to numeric context revision, selected-period attention used null date bounds, missing source facts returned500, and51 out-of-period rows incorrectly consumed the selected inventory bound. Supported51-selected refusal and current membership revocation controls passed.

The required actual expense ordinal2 owner fixture exposed a separate prerequisite: its current immutable revision read used FOR UPDATE/FOR SHARE and failed native42501 because the runtime role retains SELECT/INSERT but no UPDATE. Exact owner failure-first source is committed at `26219ba`; `test-results/context-expense-prerequisite-red-20261001` captures both initial getter500 and revision2 mutation500 before decoding. No grants were changed to reproduce or repair it.

The prerequisite removes only that immutable-row lock clause and its obsolete parameter. Record/review/withdraw retain the existing book UPDATE lock, and getter retains book SHARE. The same-row current revision read is now a plain SELECT. Actual owner HTTP proof `test-results/context-expense-prerequisite-green-20261001` passes1/1: revision2 and exact replay, old-digest409, two different-key concurrent contenders at expected2 yielding one ordinal3 and one409, exact history1/2/3, getter/review/withdraw, foreign-book404 and agent-review403. Financial fingerprints and effective grants remain identical; UPDATE/DELETE remainfalse. The context repair is still pending at this prerequisite checkpoint.

Repeat the dedicated owner proof on isolated synthetic infrastructure:

```sh
umask 077
OPENERP_E2E_ARTIFACTS=test-results/context-expense-unique \
bun run test:e2e apps/api/tests/agent-context.e2e.test.ts \
-t 'expense immutable revision admission'
```

Artifacts preserve actual request keys/status/body, retained owner responses, financial-state witnesses, effective privileges and source/migration manifest/integrity. No unit tests, schema exceptions, live provider/company data, deployment or production action are part of this evidence.

The context repair now projects the invoice ordinal from its exact current revision row and the expense ordinal/body from one row-preserving latest-source selection. Context checks the supported owner ordinal and digest before decoding the response. Missing or unsupported facts use a fixed nonprivate422 completeness refusal; a missing expense revision is retained and refused, rather than silently removed. Ordinary attention continues exposing the same digest-valued revision JSON.

A non-null selected period is read once with its actual book predicate inside the admitted transaction. Missing/foreign period returns404. Exact retained inclusive bounds filter attention; only null input selects all dates. Journal selection/version/severity and review affectedPeriodnull remain unchanged. No ranking, vocabulary, global date signature, paging, public schema, grants or migration changed.

`test-results/context-admission-red-after-prerequisite-20261001` preserves authentic5 failed/7 passed at committed prerequisite4c104a7, including complete actual owner ordinals1/2 and same-row digests, before context implementation. The first green `test-results/context-admission-green-20261001` passes12/12 with stable source inventory `03fc981ef71764cc31c4d46151bdda2fc733922f4086cee3c90188e21eec81a2` and no changed paths. Literal two-period/ordinal/journal controls, inclusive endpoints/adjacent dates/undated, missing/foreign periods, empty selection,51outside+smallselected,50selectedincludingcompleted/51refusal, missingfacts422, current revocation, and zero financial changes all pass. The dedicated immutable expense concurrency/replay/review/withdraw journey remains in the suite.

Repeat the complete bounded proof:

```sh
umask 077
OPENERP_E2E_ARTIFACTS=test-results/context-admission-unique \
bun run test:e2e apps/api/tests/agent-context.e2e.test.ts
```

New evidence is private: directories0700/files0600. The first attempted red's duplicate component locator and overlapping foreign-period fixture errors are retained and explicitly superseded; neither is claimed as the admission defect. Test-first history retains both authentic committed red boundaries. The existing bounded refusal still admits no continuation, and observed-kind module summaries still do not establish a complete supported-empty/unknown registry. This repair does not deliver packet6.

Coordinator integration at `69a0526d7dcad2cdbf7db54b257fb2322f7e1a23` independently repeats all12 ordinary HTTP cases with0 failed/skipped and stable source inventory `03fc981ef71764cc31c4d46151bdda2fc733922f4086cee3c90188e21eec81a2`. Fast and type-aware changed gates against325f5ae and integration33wired/17deferred pass. Integrated artifacts are `test-results/integrated-context-admission-20261001`; private copied verifier and actual PASS receipt are `test-results/integrated-context-verifier-20261001`. The verifier retains literal ordinal/history, selected50/51 and six named financial-table boundary assertions without importing production projections. Independent review accepted exact writer6cde93d, including failure-first chronology and fresh Comment Sicko0flags. Missing revision is the executed malformed-fact case; arbitrary invalid ordinal/digest handling is source-backed, not an additional HTTP claim. Packet6 continuation, durable capture/progress and complete adapter coverage remain open. The earlier269-case baseline applies to375bea6, not this bounded integration.
