# Proposed revision: OpenERP test suite design and execution

Basis: test-plan commit `8bff9fadbcacf9d369758b967971469548834365`, inspected at `ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb`.

This is a proposed replacement for the operational recommendations and standing requirements in `test-suite-design.md` and `test-suite-pseudologic.md`. Keep their source survey as historical analysis. Preserve the existing E-01 through E-21 acceptance identifiers and the five workflow families. This document does not grant permission to edit tests, run provider actions or activate legal profiles.

## 0. Objective and scope

Prove that named Effect operations preserve accounting meaning and complete atomic effects across the application/transaction boundary. Test the public Worker path and compare committed state on a fresh observer connection. Supplement it with narrow structural database probes, protocol/browser journeys and independent deterministic vectors when authorized.

The first implementation scope remains:

1. Sales order write path.
2. Supplier credit basis and the resulting supported credit lifecycle.
3. Schedule amendment.
4. Historical item admission.
5. Asset basis capture, with financial execution evidence consumed from the existing owner.

Do not restart the five reserved WIP assignments or the application migration. Qualification scenarios can consume their released interfaces and results. When a port is not ready, report the exact blocked scenario instead of adding a second implementation.

## 1. Retain the existing runner and improve its composition

Keep Vite+/Vitest, `fileParallelism: false`, zero retries, real workerd, production migrations and a run-owned PostgreSQL cluster. These already exist. Start with folders/tags and explicit lane selection; project splitting is optional once it solves actual setup cost.

| Lane | Execution boundary | What it proves | What it does not prove |
|---|---|---|---|
| Financial HTTP | Real API Worker with restricted runtime connection and committed PostgreSQL transactions | Application behavior, persistence, rollback and recovery | Browser/session journey or managed Hyperdrive behavior |
| Database integrity | Explicit runtime SQL in the disposable database | Allowed DML, scoped references, amount storage, append protection and deferred journal integrity | End-user authorization, legal treatment or whole workflow |
| Protocol | Real MCP negotiation/tools over the same app | Encoding, tool contracts, permissions, errors and recovery equivalence | Correct accounting by response equality alone |
| Browser | Vitest orchestrates Playwright library against web app plus real API/DB | Actual route, session, form, approval and reload behavior | Accessibility certification or every browser |
| Bun jobs | Actual selected Bun/effect-mq process and application operations | Restart, dispatch gaps, stale claims, cancellation and durable business identity | Provider exactly-once delivery |
| Pure domain, subject to policy approval | Real deterministic functions over fixed inputs, no mocked repository chains | Exact arithmetic, canonicalization and finite-rule edge cases | Database transactions or production profile qualification |
| External qualification, separately authorized | Selected managed runtime/provider/validator | Only the exercised environment and outcome | Blanket completeness or production approval |

Using the Playwright library under Vitest does not introduce the Playwright Test runner. The existing dependency can supply browser control. Vitest Browser Mode is a separate option for component tests, not a substitute for full-app requests. [R04, R13, W03, W04]

Missing prerequisites fail a selected required lane. A local pure-only command may intentionally select no database lane, but its success must never be reported as financial acceptance.

## 2. Revised standing harness requirements

### HARNESS-1: assert the actual trust boundary

Before application cases:

```text
assert generated database target belongs to this run
assert Worker uses the generated runtime login, not the maintenance URL
assert runtime role is non-owner and lacks superuser/DDL/trigger-disable privileges
assert effective table/column grants match the selected manifest
assert an allowed scoped write succeeds through the actual application
assert another book's actor cannot perform that application operation
assert forbidden history mutation fails under the actual runtime login
```

Use a direct runtime connection for role flags and structural probes. To establish which role the Worker really uses, bind it explicitly in setup and retain test-local connection-role observations through the existing connection instrumentation or scoped test probe. Do not add a publicly callable debug endpoint.

A shared backend DB credential can have access to rows from several books. Tenant policy is exercised through the application. Composite foreign keys remain independently testable in SQL. Do not claim direct-DML membership isolation that ADR 0010 does not provide.

### HARNESS-2: fail loudly on the wrong schema

```text
expected = sorted migration names + file hashes from selected source tree
actual = migration ledger names + hashes from public.openerp_migrations
require exact expected/actual equality, not only 'all rows found are known'
inspect required actual tables, constraints, indexes and integrity triggers
inspect runtime grants and role flags
run minimal allowed-DML and protected-history probes
```

Use actual baseline names and definitions. Check missing, unexpected, stale and disabled objects separately. A period policy need not have a stored trigger. A schema inventory is useful but does not replace behavioral integrity tests.

The new baseline's fresh install, populated rerun, checksum drift and old-installation refusal remain distinct scenarios. After the first real deployed release, add its actual forward-upgrade scenarios. Do not invent an unreleased legacy compatibility project.

### HARNESS-3: reproducible semantics and honest clocks

Use a fresh book and fixture identity namespace per leaf scenario, including each parameterized variant. Shared suite-owned database processes are acceptable while files are serial. Do not rely on H1 having run before H2: H2's builder establishes its own prerequisite.

A seed label may be deterministic, while generated server IDs and credentials remain random. Capture a mapping such as `quoteA -> actual ID` for semantic assertions. Retain actual IDs for linkage and digest verification. Never force insecure deterministic credentials or require server-generated IDs to equal invented literals.

Use three clock categories:

- **Business dates:** explicit, stable inputs used by accounting calculations.
- **Application clock:** injected/frozen only where the product already uses an owned clock dependency.
- **Database time:** observed directly for approval expiry, leases and DB-derived current dates.

A browser or Node fake clock does not change PostgreSQL. For DB-relative schedule checks, construct dates around a retained database anchor and provision the needed periods/years. Keep amounts and relative ordering exact. For pure fixed-date vectors use a stated input time without pretending it changes the server.

For approval expiry, seed a correctly bound immutable expired approval as an explicitly classified fixture, or use an approved test-scoped validity configuration at issuance. Test real issuance expiry arithmetic separately. For expiry after a lock wait, wait until the observed database clock crosses the retained expiry while the request is demonstrably blocked, then release. Never update a sealed approval or add a production test-time bypass.

Prefer cluster teardown over TRUNCATE/CASCADE cleanup. It is not true that adding a table necessarily makes an old truncate list fail. Table ownership/fixture coverage should be checked explicitly.

### HARNESS-4: immutable run evidence

Write `test-results/e2e/<run-id>/`, not a directory deleted at the next run. A `latest.json` pointer may be replaced. Choose the run directory before setup and ensure reporters and helper artifacts all use it.

Retain:

```text
revision and worktree manifest, including relevant untracked files
lockfile and exact baseline hashes
actual package/runtime/browser/PostgreSQL versions
selected lane, required case IDs and collected case IDs
fixture IDs, exact expected financial data and source provenance
application/database time anchors, locale and timezone
public requests with secrets removed
scoped before/after state and exact field differences
request, plan, approval, receipt and economic identities
lock graphs, injected fault phase and recovery trace where applicable
first-attempt result, skips, diagnostic reruns and teardown result
```

Keep data minimization explicit. Do not hash or archive credential files as ordinary fixture evidence. A source manifest must include only relevant allowed paths, not every file on the developer's machine.

Represent `setup_failed`, `oracle_failed`, `product_failed`, `not_run`, `blocked`, `passed` and `cleanup_failed` distinctly. A cleanup failure after product success still fails the required run without overwriting the product observations. Observations are collected before teardown.

## 3. Fixture construction and oracle independence

### Two named fixture tiers

**Valid workflow fixtures:** produce the ordinary prerequisite through owned operations where practical. Larger committed seed graphs are allowed when explicitly declared and independently checked against their expected relationships. Each family has one setup smoke scenario proving its builder produces a supported basis.

**Corruption/integrity fixtures:** intentionally impossible or damaged states, seeded only with maintenance authority in the isolated database. They test defensive read behavior or integrity enforcement, not the public ability to create those states. Do not disable production integrity globally to build a normal happy path.

Every negative case starts from a known valid neighbor and changes one condition. If an earlier prerequisite blocks both variants, the intended guard was not exercised. Earlier predicates need validation, not mocks that return whatever the next guard expects.

### Separate three kinds of oracle

1. **Domain oracle:** independently chosen amounts, dates, identities and expected financial relationships.
2. **Persistence oracle:** raw scoped DB observations on a fresh connection, without importing the production reporting/calculation helper.
3. **Transport oracle:** documented response fields, status/error mapping and protocol envelope.

Schema decoding is necessary but not sufficient. Comparing REST with MCP proves consistency, not correctness. Reading another projection produced by the same buggy query is not an independent DB oracle.

### Assert footprints, not only empty ledgers

Declare an operation-specific footprint before running it:

| Operation | Allowed success effects | Financial non-effects |
|---|---|---|
| Quote/order write | Document head/revision and command receipt | No voucher, approval use, cash or financial counter change |
| Credit preparation | Exact review/plan and named preparatory records/receipt | No executed credit, liability reduction or VAT posting |
| Credit execution | Journal, credit/register effects, approval use and required receipts/outbox | No unrelated line-capacity use |
| Schedule amendment | New schedule revision, dependencies and receipt | No installment journal merely for changing the suffix |
| Historical admission | Retained source item/payment/match admission and receipt | No new live settlement capacity or GL recognition merely from source assertions |
| Asset preparation | Exact basis/review/plan and named preparatory records | No impairment/disposal posting until owned execution |

Resolve each footprint against current application code before registration. Preparatory writes such as a sealed plan are allowed only when declared. Refused commands must leave accounting state and successful-command receipts unchanged; a separately specified attempt/audit event is assessed separately rather than silently forbidden or ignored.

Snapshots compare exact scoped rows as multisets. Require actual book/series counters, not `max(vouchers.sequence)`. Check domain control amounts and per-line capacity, not only aggregate balance. Check absence of extra rows as well as presence of expected ones.

## 4. Deterministic concurrency against the real Worker

### Book-row gate

This protocol tests the selected row-lock design without adding advisory locks to product code.

```text
fixture = valid isolated scenario
stop unrelated jobs for that fixture
baseline = fresh observer snapshot

GATE connection:
    BEGIN
    lock exact openerp.books row FOR UPDATE
    record gate backend PID

launch request A with retained command identity
OBSERVER:
    poll with a bounded deadline until a runtime backend is waiting
    prove a blocking path from that backend to GATE via pg_blocking_pids

launch request B
OBSERVER:
    prove both in-flight operations have runtime waiters in the isolated scenario
    record direct/transitive blocking paths and wait-event evidence
    # Same-actor admission can put B behind A's authority lock, not directly behind GATE.

release GATE
await both bounded results
observe final committed state from a fresh connection
assert the declared allowed serialization and exact economic effects
always cancel/join remaining requests, roll back gate and release all clients
```

Request-to-backend association must be established rather than inferred from arbitrary global lock activity. Start with a dedicated isolated case, known runtime login and no unrelated work. Where that is insufficient, add a test-only request/transaction trace in the test composition, never a user-controlled SQL or public pause hook.

If overlap was not observed, report harness failure/not exercised. Do not let a fast sequential success pass as a race proof. Polling for a known condition is allowed; an arbitrary sleep offered as evidence is not.

Use deadlines comfortably greater than the expected setup and barrier steps. A tiny lock timeout is not the desired winner/loser oracle. Separate lock-timeout recovery from a successful serialized race. PostgreSQL exposes both direct and wait-queue blockers; retain the graph, not only `wait_event_type = Lock`. [W02]

### Required race classes

**Same key and same actor/input:** one committed operation and the same recovered receipt for both requests. No fresh key on uncertainty.

**Distinct keys, same economic identity:** one economic result, then the contract's duplicate/conflict/recovery response. No second financial effect.

**Distinct proposals competing for capacity:** preparation may succeed for both. Execution cannot overconsume; loser re-prepares or refuses with the documented current-state error.

**Revocation versus execution:** test revocation committed before admission and execution committed before revocation. Record which serialization occurred. A stale edge token is not sufficient authority.

**Close versus posting:** valid outcomes are either posting first and close re-evaluating its basis, or close first and posting refusing. Never close on a stale population or commit into the disallowed period.

**Snapshot versus multi-voucher group:** captured reports include all or none of an atomic group. Later pages use the same cutoff. A half-group boundary is not a valid report.

## 5. Failure injection and commit uncertainty

### In-transaction failure probes

Use test-owned triggers or existing dependency seams in a disposable environment. Scope an injection to the exact test book/operation and remove it in `finally`. It may force a failure but must not manufacture financial success or bypass normal validation.

Add an explicit injection point after each relevant persistence phase:

```text
header/counter write
first line batch
domain/register effect
approval consumption
outbox intent
command receipt
commit-time deferred integrity
```

For every point, assert complete rollback including counters and register capacity, then remove the fault and recover/retry the same command. Do not assume all domains necessarily write an outbox row; inject at actual boundaries of each declared effect group.

A separate commit-time probe is essential. Deferred constraint triggers fire at commit, while forced immediate checking is a different timing path. SAVEPOINT/ROLLBACK-only cases may never exercise the deferred check. Keep a real COMMIT rejection case. [W01]

The current outbox-fault test is a useful base, but it is not a substitute for faults after domain register writes or for swallowed Effect failures. Preserve its actual DB path instead of mocking the whole repository. [R07]

### Two separate lost-outcome tests

**Response lost after known server success:** use a test-owned HTTP proxy that forwards the request, waits for the real committed response, records that phase and closes the downstream response without delivering it. Client recovers the original key. This proves response-loss recovery, not DB connection loss during COMMIT.

**Connection lost near COMMIT:** a scoped fault proxy or controlled termination may leave commit versus rollback uncertain. Assert only that durable lookup/recovery converges to one result and never duplicates the economic effect. Do not assert rollback from the network error. Re-authorize before receipt disclosure.

Keep these identities separate in the coverage ledger. A test that simply ignores a successfully received body is narrower than a real client-side transport loss.

## 6. Digest, precision and protocol requirements

### Canonicalization

Use independent fixed UTF-8 byte vectors plus independently computed expected SHA-256. Do not use the production canonicalizer to generate the expectation. Specify:

- Exact digest payload and self-digest exclusion for each saved schema.
- Object-key order independence and array-order significance.
- Exact string preservation, including Unicode behavior defined by the selected canonicalization version.
- Rejection of unsupported numeric/Unicode values and duplicate raw keys at their admission boundary.
- Explicit omission versus `null` for each supported optional-field variant.

Do not silently normalize Unicode in the oracle when the product's contract preserves it. Do not normalize generated IDs away before validating a real document digest. Schema shape checks and independent accounting expectations supplement hash checks.

### Monetary coverage

Test ordinary and negative/reversal values, the double-precision boundary, the admitted maximum line value, maximum plus one and aggregates exceeding a single-line limit. Cover exact divisibility and named rounding policies separately. Distinguish lexical malformed input from otherwise valid exact values refused by a domain capacity rule.

The relevant runtime cases must exercise meaningful multiplication/division and residual release, not just transport a large number once. The database storage probe must demonstrate fractional values are refused before scale coercion could round them into validity.

### HTTP and MCP

Use current shared route/error contracts rather than invented 201/422 assumptions. Pin exact failure code for a single violated semantic predicate. Do not accept `UnsupportedProfile or InvalidJournal` as a completed oracle.

Retain the existing raw JSON-RPC test and add an actual negotiated client journey when supported by the selected protocol stack. A regex excluding tool names containing `approv` or `activat` is only a diagnostic. Test a typed capability authorization manifest and direct unauthorized invocation through every exposed surface. Compare the resulting ledger/register state with independent expected data. [R16]

## 7. Revised E-scenario coverage and release accounting

Keep E-01 through E-21. Split each into concrete cells:

```text
scenario family x operation family x case x required runtime
```

A machine-readable case record names:

```text
id, parentCaseId?, E_ids, workflow, layer
contractSource, oracleSource, fixtureId, recordClass
supportedProfile, rules/schema/handler versions
preconditions, request identity, expected failure or exact result
expected footprint, independent observation queries
barrier/fault protocol, allowed serialization outcomes
owner, status, observed run IDs, explicit limitations
```

Do not promote an entire E-family to green because one operation passed. For example, posting precision does not cover credit deduction release, FX paired balances and payroll boundaries. Refusal-only coverage does not make an unimplemented operation supported.

The document's 59/68 case arithmetic and eleven/twelve E-gap arithmetic are replaced by generated counts. Nested variants receive their own stable leaf IDs. Collected tests must be nonempty and equal the required selected manifest; skipped, cancelled and missing IDs are reported distinctly. A case prevented from reaching its intended precondition is not a successful negative test.

### Gates

**Product change:** existing static checks, affected scenario cells, kernel sentinels and relevant first-attempt integration evidence.

**Financial/domain change:** include the owning register consequences, duplicate economic identity, exact values and applicable failure/race cases.

**Shared transaction/identity change:** include all runtime callers, revocation, rollback, commit-uncertainty and complete-group observation.

**Schema/grant change:** baseline install/rerun/drift/refusal, real catalog/grants and required integrity probes.

**Browser/runtime change:** at least one real visible journey using the changed composition. Component-only tests cannot discharge SSR/proxy/session/service-binding gates.

**Provider/format release:** selected independent specification/validator or authorized provider evidence, with exact supported subset and versions.

**Full company release:** applicable financial families, source completeness and controls, period/year transitions, restored-state verification and outstanding real-world obligations.

Fast developer checks may select a smaller lane. They must not claim to satisfy the whole release gate. If a required browser lane is not implemented, mark the release gate open instead of describing the lane as impossible.

## 8. Prevent tests that cannot detect their target defect

Three distinct checks are useful:

1. Valid/invalid input neighbors prove the product's refusal behavior.
2. Feeding a known-bad observed result to the assertion helper proves the oracle rejects it.
3. A narrowly controlled mutation of product behavior, where authorized, proves the suite detects the targeted regression.

Do not conflate them. Changing one expected value so an assertion throws is not proof that the product branch was exercised. Avoid a new mutation-testing platform initially; hand-selected counterexamples for source scope, double posting, missing register rows, swallowed failures and absent catalog objects are sufficient first targets.

An oracle self-test must fail for the intended mismatch, not a setup error. Assertions about complete results should reject an extra offsetting journal pair and a duplicate allocation even if final balances still agree.

## 9. Implementation sequence

**TEST-00: Repair the specification.** Apply the case corrections and source/contract distinctions. Resolve exact response schemas and synthetic fixture profiles. Keep unresolved product decisions visible rather than deriving policy from existing branches.

**TEST-01: Extend the current support directory.** Add role/catalog preflight, per-scenario fixtures, exact footprint observers, immutable run directories and a bounded book-gate helper. Prove the helpers with both valid and known-bad observations.

**TEST-02: Supplier credit and sales lifecycle.** Cover valid profiles, line residuals, same/foreign-book number scope, replay, quote/order semantic identities and full credit execution. Start with a handful of decisive end-to-end cases, then expand predicate boundaries.

**TEST-03: Schedule, historical admission and asset basis.** Use the corrected prefix/suffix fixtures. Preserve nonfinancial effects as such. Add control completeness and paired source chronology. Consume asset execution proof from the reserved owner.

**TEST-04: Cross-cutting financial races and fault phases.** Add capacity competition, expiry/revocation after waits, close/post ordering, complete report boundaries and commit uncertainty. Exercise both the real Worker and relevant Bun financial caller.

**TEST-05: Thin browser/MCP/job journeys and coverage automation.** Add review/approve/reload, lost-response recovery, current owner routing and one nonempty durable preparation job. Generate the selected/collected/executed coverage ledger and change-impact gate. Extend remaining E-families according to the existing acceptance scope.

Tests and fixtures are edited only under the applicable user authorization. A plan review is not itself a production posting, deployment or provider authorization.

## 10. Release evidence and limits

This revision specifies how to collect evidence. It does not assert any new passing application case. Runtime proof, company applicability, format validation and provider acceptance remain separate. Preserve valid existing tests and known defects; do not loosen product controls to make an erroneous pseudocode expectation pass.
