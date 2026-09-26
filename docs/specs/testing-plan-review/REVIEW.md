# OpenERP testing-plan review

Review date: 2026-09-26.

Reviewed test-plan commit: `8bff9fadbcacf9d369758b967971469548834365` (`test plans`). Files were read at `ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb`, the branch head observed during this review. The later parity-backlog work is not the subject of this review.

Status: source review and proposed revisions. No repository file, test or database was modified. No application suite, Worker, browser or live provider was executed. Findings about implementation describe inspected source, not reproduced runtime failures.

## Verdict

Keep the plan's real-Worker/real-PostgreSQL approach, negative neighbors, independent observations, explicit recovery and non-vacuous checks. Do not implement the pseudologic verbatim. Several expected outcomes contradict the selected application-owned architecture, the same document's guard ladders or the inspected implementation. These would train tests to reject correct behavior or encourage changes that weaken accounting controls.

The central revision is to make the plan a specification of observable business behavior rather than an exhaustive transcription of today's if-statement order. Preserve guard-order assertions only when the order is an actual contract: current access before receipt disclosure, replay before new-work expiry/freshness, complete validation before committed effects and owner routing before constituent execution.

## Source-grounded findings

### TP-01 / Critical: HARNESS-1 reverses the accepted database boundary

**Source:** `test-suite-pseudologic.md` section 1 says the runtime role must be unable to write `openerp.commerce_invoices`. Current `AGENTS.md` assigns scoped DML to the trusted application. The existing persistence test is already named `runtime has scoped DML while protected posting history rejects mutation` and positively inserts evidence through the runtime login. [R01, R03, R07]

**Consequence:** the proposed harness can reject the intended installation. It conflates a backend database identity with an end-user identity. Direct SQL under a shared runtime login is not a test of book membership enforced by the application.

**Revision:** assert the actual login, non-owner role flags and effective allowed/denied DML matrix. Use HTTP/MCP/application operations to test current actor/book policy. Use direct runtime SQL for structural constraints and prohibited mutation of history. Require a valid own-book operation as the positive neighbor. Do not reintroduce RLS, GUC tenant identities or function-only grants to satisfy this plan.

### TP-02 / High: schema readiness must describe the new baseline

**Source:** HARNESS-2 asks for a period-lock trigger and says every recorded migration must be applied. Current architecture assigns posting eligibility to the application and retains only narrow integrity SQL. The actual runner already invokes the production migrator before starting workerd. [R01, R03, R05]

**Revision:** compare the complete expected migration manifest to `public.openerp_migrations` in both directions, including names and hashes. Check the reviewed actual integrity mechanisms and effective grants, not an obsolete business trigger name. Test period lock behavior through every relevant application writer. Existing feature-policy SQL retained during migration is a cutover finding, not a reason to redefine the target architecture.

### TP-03 / High: the plan overlooks working harness infrastructure

**Source:** suite-design section 8 says explicit serial execution is missing. Root `vite.config.ts` already has `fileParallelism: false`, `retry: 0`, a global setup, JSON/JUnit reporters and `forbidOnly` in CI. Setup already creates a disposable cluster, separates admin/runtime URLs, runs migration and records a manifest. Helpers already live in `apps/api/tests/support`. [R02, R04, R05, R06]

**Revision:** extend this harness. Add identity/catalog preflight and better run evidence. Do not spend a packet rediscovering serial execution or moving support into a second test platform. Do not copy Accounted's optional-environment behavior into a required lane: missing prerequisites must fail the selected lane rather than remove it from discovery.

### TP-04 / Critical: SA-H1 is not a valid happy path

**Source:** it starts with twelve unposted occurrences, chooses `firstOrdinal: 5`, supplies four replacements and expects eight occurrences. The same plan says a dates-only amendment must preserve count and its prefix must already be posted. Current `scanAmendedPrefix`, `buildAmendedOccurrences` and `amendSchedule` enforce these distinctions. The source computes `allocatedMinor = recognized + remaining`, not remaining alone. [R01, R10]

**Revision:** use twelve 10000-unit occurrences with the first four posted, then replace the eight future dates while preserving amounts and occurrence identity. Expected recognized is 40000, future is 80000 and allocated is 120000. A four-installment replacement of 20000 each belongs to an estimate/lifetime amendment, not dates-only. An all-unposted schedule instead starts from ordinal 1.

### TP-05 / Critical: CB-R3 turns tenant isolation into cross-tenant interference

**Source:** CB-R3 puts an already-used supplier credit number in another book and expects `IdempotencyConflict` in this book. `readCreditConflicts` filters number conflicts by both book and counterparty. [R01, R09]

**Revision:** a number used only in another book must not prevent an otherwise valid local credit. Test separately: same local supplier/number conflict; another local supplier's same number where the contract permits it; foreign child ID under an accessible local scope; inaccessible top-level scope. Verify no foreign references leak. Do not require 404 for all these cases if the maintained public contract distinguishes forbidden top-level scope from not-found child identity.

### TP-06 / Critical: CB-X1 confuses proposals with reservations

**Source:** it requires at most one concurrent preparation to see zero prior usage and sums both proposed capacities. The inspected prior-usage query joins executed `supplier_credits` to their immutable reviews. The preparation step is not an implemented capacity reservation. [R01, R09]

**Revision:** competing alternative proposals may describe the same remaining amount. They must not consume it. Prepare distinct 7000-unit alternatives against 12500 remaining, approve as permitted, then race execution. Exactly one may consume 7000; the other must refuse or require fresh preparation because only 5500 remains. Same-key execution is a separate case: both callers recover the same result. A new key for the same economic effect must not create another credit.

### TP-07 / High: several other fixtures target the wrong branch

**Source:** source and plan comparison found:

- SO-R6 says `50 -> 49` should succeed. The positive boundary is `49 -> 50`; revision history is not decremented.
- SO-R9 expects a stale-shaped error although its G10 and current transition guard return `InvalidJournal` for wrong kind/state with otherwise current expectations.
- SO-H1 expects `receipt.documentId` and SO-H2 expects `previousDigest`. The current sales document schema exposes `id` and has no `previousDigest` field. Generated IDs need captured aliases, not guessed literals.
- SA-R2 chooses `firstOrdinal: 1` but attributes the failure to a prefix scan. There is no prefix at ordinal 1. A posted occurrence in that suffix is an `AlreadyPosted` path in the inspected source.
- SA-R3 combines an old unconsumed suffix that is already due with invalid replacement dates. The source distinguishes old-suffix `UnsupportedProfile` from replacement-date `InvalidJournal`.
- AB-R2b has posted 1-3 followed by prepared 4 and unprepared 5-12. That alone is a contiguous consumed prefix followed by an unconsumed suffix. The impairment rejection occurs when a later posted/reversed occurrence appears after suffix start.
- AB-R2c cannot promise disposal success for the same overdue unconsumed suffix. The source explicitly refuses unconsumed dates strictly before the disposal date.
- HI-R4's description of two 600-unit payments against one 1000-unit payment is ambiguous. It must instead identify whether two match legs consume one payment or two distinct payments.

**Revision:** use the concrete replacements in `CORRECTED-WORKFLOW-CASES.md`. Assert one predicate at a time with all earlier prerequisites valid. Label unreachable-through-API corrupt states as integrity/corruption tests rather than ordinary workflow fixtures. [R01, R08, R10, R11, R12, R17]

### TP-08 / High: digest verification is circular and its signed payload is unclear

**Source:** SO-H1 calls recomputation using `canonicalizeJson` independent; XC-4 asks to digest the returned body. The same production canonicalizer is not an independent oracle. Inspected sales code hashes the body before adding the digest. [R01, R08]

**Revision:** specify each schema's exact digest payload. For that sales schema, exclude the top-level digest. Maintain independently specified canonical bytes and hashes for fixed microvectors. For dynamic documents, distinguish persistence agreement, independently serialized digest validation and business-field verification. Do not hash a normalized alias view in place of real IDs. Optional field omissions must be asserted for the selected variant, not against every possible field in a union schema.

### TP-09 / High: `max(sequence)` does not prove counters were not consumed

**Source:** XC-1 observes the maximum recorded sequence. A counter could advance without a persisted voucher, leaving that maximum unchanged. [R01]

**Revision:** read the actual book and series counter rows before/after in addition to journal membership. Observe approval-use, domain effects, outbox intent and command receipts. Use multiset comparison over exact rows and scoped identities, not only counts or net balances. Two equal/opposite unintended lines are still a failure.

### TP-10 / High: blanket time freezing is not implementable as written

**Source:** HARNESS-3 freezes every case at March 17 and forbids wall-clock reads. Existing fixtures create credentials from Node time and PostgreSQL `now()`. Schedule amendment reads a database timestamp. The standing verification strategy already warns that browser overrides do not change database expiry. [R01, R06, R10, R13]

**Revision:** separate business dates, application clock and database transaction clock. Keep exact supplied business dates stable. Use a scoped test clock only for already injected application clocks. For DB expiry use the actual DB clock and test-owned expiry fixtures or a scoped fixture-only validity policy. Never mutate an immutable approval to expire it or add a public time-control endpoint. Record actual DB anchors and assert time intervals when exact timestamps are not fixed.

### TP-11 / High: rollback/savepoint techniques are not interchangeable with committed E2E

**Source:** suite-design promotes an Accounted savepoint technique. The project's maintained strategy expressly requires genuine commits visible from other connections. [R02, R13]

**Revision:** use real commits for application HTTP, browser and queue scenarios. A fixture seed must commit before another runtime uses it. Use fresh scenario books and cluster teardown, not a shared outer rollback. Isolated direct-DB constraint probes may use savepoints, but must force deferred checks where appropriate and still include a real COMMIT-failure case. Never claim a deferred integrity rule was exercised when all writes were rolled back before it fired. [W01]

### TP-12 / High: the concurrency plan leaves its main mechanism unspecified

**Source:** section 10 admits no barrier implementation. Merely proposing `Promise.all` or a tiny timeout does not resolve this. [R01]

**Revision:** use the actual book row as a test-owned gate and observe runtime waiters using `pg_blocking_pids` plus `pg_stat_activity` in the isolated test cluster. Retain the blocker/waiter graph before releasing the gate. Shared requester locks can create a transitive chain, so direct blockers alone are not sufficient. Then assert all allowed serialization outcomes. See `REVISED-TEST-PLAN.md` for the complete protocol. [W02]

### TP-13 / High: most new cases stop at preparation

**Source:** the credit and asset sections predominantly inspect prepared snapshots. Schedule revisions and historical admission are rightly non-posting operations, but testing those alone cannot establish the downstream credit or asset financial lifecycle. [R01]

**Revision:** classify effects precisely. Add credit prepare -> approve -> execute -> reload and distinct-key economic duplicate cases. For asset paths consume the reserved owner's released qualification instead of assigning a second implementation. Assert impairment-aware schedule/control/disposal results once that handoff is available. Keep preparatory success distinct from financial acceptance.

### TP-14 / Medium: browser deferral is a scope choice, not a Vitest limitation

**Source:** the suite-design postpones browsers as though a runner change were necessary. Root dependencies already include Playwright and the maintained strategy already specifies Vitest with Playwright-driven browser actions. [R02, R04, R13]

**Revision:** retain Vitest as runner and use the Playwright library for a thin full-application browser lane. This is separate from adopting Playwright Test as a runner. Browser Mode is another documented Vitest option, but a rendered component alone would not prove TanStack Start routing, sessions and API integration. Start with login/setup plus review/approve/reload and owner-aware correction routing. [W03, W04]

### TP-15 / Medium: reported coverage counts are internally inconsistent

**Source:** the zero-coverage list E-05, E-07, E-10, E-12 through E-19 and E-21 contains twelve IDs, not eleven. The pseudologic table totals 17 + 42 + 9 = 68 while prose says 59. Many rows expand into multiple predicates and some H/R labels contain both kinds, so even 68 is not a verified executable-case count. [R01, R02]

**Revision:** generate inventories from stable leaf case IDs and runner collection. Track planned, collected, executed and passed separately. Track E-scenario coverage by operation family and failure mode. One exact-money roundtrip does not complete every part of E-02; one posting happy path does not prove all of E-03. A failed setup is not a tested product failure and not a pass.

### TP-16 / Medium: the change-coverage gate targets the wrong primary surface

**Source:** suite-design recommends a migration-triggered gate. In the selected architecture important policy changes can touch only application TypeScript, domain calculations, auth helpers, contracts or job handlers. [R02, R03]

**Revision:** require affected behavior evidence for application/domain/jurisdiction/contract/persistence/runtime changes as well as DDL. References to existing cases must resolve to collected IDs and run in the relevant lane. A free-text `covered-by` comment is not sufficient evidence. Do not copy a several-thousand-line custom SQL/AST analyzer before simpler real-query, type and ownership checks prove insufficient.

### TP-17 / Medium: evidence preservation needs concrete repair

**Source:** global setup deletes `test-results/e2e` at the beginning. Its Git diff hash excludes untracked files and records a runner version literal. [R05]

**Revision:** write immutable run-ID directories, with only a replaceable latest pointer. Record actual runtime/package versions and explicit hashes for executed tests, fixtures and relevant untracked inputs, excluding secrets. Distinguish setup failure, product failure, oracle failure and cleanup failure. Retain enough evidence to replay the exact case without dumping credentials or arbitrary company documents.

### TP-18 / Medium: reference material must not become a new source of authority

**Source:** suite-design treats a taxonomy calculation linkbase as the statement arithmetic oracle and recommends copying a public SIE corpus. Its restoration recommendation is both byte-exact and header-modified. [R02]

**Revision:** external references supply vectors and independent validators, not universal proof of statutory classification or completeness. Pin the applicable version and supported subset. Clear fixture redistribution/privacy before vendoring. Restore a hash-preserved historical file unchanged with a separate status note, or label a modified copy with a new hash. Neither restoring references nor resolving K2/K3 is a prerequisite for testing a synthetic asset calculation with explicitly supplied role accounts.

## Retained strengths

The plan correctly prioritizes behavior beyond HTTP status, exact amounts, negative neighbors, explicit post-commit recovery and the distinction between one-time evidence and regression coverage. Its strongest transferable ideas are oracle self-tests, declared scope, realistic database effects and readable financial diffs. The revision retains these.

## Decision on pure tests

Recommend explicitly clarifying the policy: reject mock-heavy tests that restate implementation calls, not small deterministic tests of money, canonical bytes, schedules and finite rule calculators. A pure test remains a unit test; renaming it a drift guard is not an honest exception. Existing repository restrictions still apply until the authorized scope changes. This review creates no such tests.

## Delivery recommendation

Repair the oracle specification first. Extend the current harness next. Implement the highest-value lifecycle cases before broad guard enumeration. Add observed races and rollback probes, then a thin browser/MCP/Bun lane and generated coverage gating. Do not redesign the product to satisfy an erroneous fixture.
