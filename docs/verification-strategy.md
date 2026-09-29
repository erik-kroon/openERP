# Verification strategy

Status: requirements for the existing E2E suite; coverage remains tied to actual run artifacts. [E-01–E-21](verification.md) define outcomes; the [acceptance plan](plans/09-acceptance.md) supplies independent examples. Test changes require the authorization in [AGENTS.md](../AGENTS.md).

## Runner and environment

Run `bun run test:e2e` from the root. [Vite+](../vite.config.ts) runs the existing API Vitest suite against workerd and disposable PostgreSQL. There is no automated browser suite in this configuration. The [suite instructions](../apps/api/tests/README.md) specify prerequisites and `test-results/e2e` artifacts. Preserve this runner unless a demonstrated need warrants a change.

Drive public requests through the real API Worker and PostgreSQL. Give the Worker only a restricted runtime login. Use separate maintenance credentials for setup and independent database observations. Browser journeys use the same operations. Do not replace internal services or wrap the suite in an outer transaction: requests must commit and remain visible to fresh connections.

Own a disposable database/cluster, fresh actors/books and bounded process/port lifetimes. Refuse unexpected or pre-existing targets. Concurrent workers need separate databases unless isolation is proved. Readiness checks database/migration access as well as HTTP health. Reused servers must match the revision and configuration. Teardown removes only run-owned resources, including after setup failure.

Use production migration/provisioning commands. For the application-owned baseline, check the clean three-file baseline, rerun, checksum-drift rejection and refusal of the old installation; after release, verify normal forward migrations separately. Preserve historical evidence and financial meaning, but do not require an old-schema upgrade or old-digest interpreter. Inspect effective grants and attempt forbidden table/function access under the runtime login.

Label runtime evidence precisely:

| Surface                         | What it can establish                                                                   |
| ------------------------------- | --------------------------------------------------------------------------------------- |
| Local workerd/direct PostgreSQL | Local API, transactions and resource cleanup.                                           |
| Browser/Vite proxy              | Development routing and interaction.                                                    |
| Built web/API Workers           | Assets, service binding and deployment composition.                                     |
| Managed Hyperdrive              | Actual uncached reads, networking and connection behavior in an authorized environment. |
| Bun                             | Migration/maintenance behavior; separately exercise any self-host application adapter.  |

## Continuous integration

[OpenERP CI](../.github/workflows/ci.yml) runs on pull requests, pushes to `main` and manual dispatch. It pins Ubuntu and Node, reads the Bun version from `package.json`, and requires `bun install --frozen-lockfile` in both jobs. Dependency changes must include the corresponding `bun.lock` update; never remove frozen installation to hide drift.

The validation job reports formatting, type-aware lint, type checking and application builds separately. Once installation succeeds, a failed validation step does not hide the remaining checks. The E2E job runs independently and installs PostgreSQL 17 from the official PostgreSQL Apt repository, matching the [local development](local-development.md) and recovery proof target. `PG_BINDIR` selects those server binaries explicitly rather than an image's unrelated `pg_config` default. Both jobs and their expensive steps have time limits; superseded runs on the same ref are cancelled.

An E2E run uploads `e2e-evidence` on success or failure, including the console log under `test-results/ci` and available results, manifest and runtime logs under `test-results/e2e`. The console log remains available even when global setup fails before the normal manifest is written. Read the PostgreSQL log for migration errors and `worker.json` for Worker startup errors: type checking and a successful bundle do not prove schema initialization or runtime startup.

For application failures, match the response's `x-request-id` to `worker.json`.
Unexpected transaction failures retain sanitized schema/database causes in Effect
logs; public responses remain generic. The [diagnostics regression](../apps/api/tests/README.md#failure-diagnostics-regression-contract)
exercises console capture, retained-schema failure, a database constraint and
rejected connection credentials on real workerd/PostgreSQL. Its separate
`diagnostics-worker.json` is captured from its test-owned Worker. Set
`OPENERP_E2E_ARTIFACTS` to a distinct `test-results/` subdirectory when another run
owns the default artifacts; this does not relax source-integrity checks.

Reproduce the gates locally with `bun install --frozen-lockfile`, `bun run format:check`, `bun run lint`, `bun run check-types`, `bun run build` and `bun run test:e2e`. Run these sequentially in one worktree. The source and environment manifest limits what a passing local run proves; it is not an observed GitHub Actions result.

The E2E job runs the scoped `core` excellence profile rather than the bare E2E
command, so ordinary continuous integration supplies synthetic regression
protection and per-case evidence. It is not the whole release claim.

## Expectations and fault control

The isolated [Bend verification kit](../verification/bend/README.md) adds an
offline model lane: exact arithmetic, ledger/allocation laws, qualified VAT
monetary projection and bounded covering-set suggestions. Run
`npm --prefix verification/bend run verify:local` to retain source hashes,
command results and current-owner monetary comparisons. Its bundled development
checker is not an official Bend compiler or independent safe-kernel result;
`verify:release` requires those tools and fails when they are absent. This lane
does not establish PRY-33 product integration, VAT eligibility, statutory
applicability or application transaction behavior.

The additive [authority candidate](../verification/bend/authority/README.md) keeps
its evidence separate. Its compiler lane verifies pinned upstream source,
reproducible JS generation and compiled execution before independent safe-kernel
checking. Current-owner mapping, actual-host integration and explicit deployment
approval are additional gates; compiler success alone cannot promote a release.

The dedicated VAT qualification config reuses the existing PostgreSQL/workerd
setup and invokes the actual Effect capture/sealing/read workflow at a Bun
boundary. Its [failure obligations](../apps/api/tests/BEND-QUALIFICATION.md)
cover currentness, immutable records, replay, no fallback and shared
approval/execution. This separate lane requires a qualified build artifact;
ordinary E2E runs remain independent of the Bend/Lean toolchain.

Write failure outcomes before implementation. Use small synthetic fixtures with scenario/invariant IDs, provenance, exact expected values and profile/rule/schema versions. Do not compute expectations with the production calculator or backfill unit tests after implementation.

For a fresh-book posting of `12500` minor units, expect two lines, bank/clearing balances `12500`/`-12500`, sequence and series number `1`, one receipt, one outbox event and one consumed approval. Observe through a fresh request and connection. Retry preserves those counts; reversal retains the original and returns balances to zero. This is arithmetic proof, not a tax example.

Also cover `9007199254740993`, the `10^38 - 1` line boundary, overflow and aggregates beyond a line's bound. Distinguish lexical admission from SQL integrality/range checks. Reject numeric JSON money, fractions, exponent forms, negative zero, invalid dates and unsupported precision. Specify the clean-baseline canonicalization bytes/hashes independently, including key/array order, Unicode and duplicate keys. Historical seals and evidence remain available as dated records; they are not an old-digest compatibility interpreter in the replacement.

Anchor fixture time explicitly. Browser clock overrides do not change database approval expiry. Format corpora retain raw-byte hashes, encoding, feature coverage and expected semantics, including Swedish characters and correction records. Roundtrips can share bugs; use independent facts and pinned validators with known exclusions. Demonstrate that a deliberately wrong expectation fails, without weakening product validation.

Synchronize races through observed locks or test-owned barriers with bounded timeouts. Concurrent promises alone do not prove overlap. Allow each valid serialization. Test competing first executions separately from replay after success. Drop a response after commit; recover by durable identity. Connection loss during commit does not prove rollback. Real transaction failures must leave no partial effects, counters, approval consumption, receipts or outbox state.

Remove test-owned fault fixtures after use. Keep fault controls out of public product endpoints. Simulate external providers only for deterministic failure cases and label the result; sandbox acceptance and model evaluations are separate runs. Exercise oversized, interrupted and slow streamed bodies with/without declared lengths through REST/MCP, followed by a valid request and cleanup checks. MCP proof includes a real client, negotiation, schemas and error envelopes.

## Human journeys

Use accessible roles/labels and real actions. Check source bytes, exact lines, displayed digest, approval and durable receipt together. Cover stale, denied and uncertain outcomes, reload/recovery, logout and identity/book cache changes. Assert persisted results beyond labels, screenshots or HTTP success.

Cover Swedish/English money/date presentation, keyboard/focus recovery, narrow layouts and reduced motion. Record actual 200% browser zoom, contrast and screen-reader observations separately; viewport resizing does not prove them. Keep decisive success screenshots and failure traces. Downloaded reports need exact fact/hash checks and independent semantic validation where applicable.

## Excellence profiles

The scoped qualification layer lives in
[`verification/assurance/excellence`](../verification/assurance/excellence) and
adds profile-scoped gates on top of the existing assurance runner. It reuses the
same workerd/PostgreSQL harness; it does not replace that runner or the native
suite.

```sh
node verification/assurance/excellence/scripts/run.mjs core
```

| Profile   | Adds                                                                                                                                                                                                                                        | Requires                                                                    |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `core`    | Independent supplier oracle, three seeded HTTP histories, a late refund fault with same-key retry, an FX valuation chain oracle, payroll rounding/band conformance and a real `pg_dump`/`pg_restore` drill through a second Worker runtime. | Nothing beyond the standard harness.                                        |
| `stress`  | The semantic mutation campaign, which now counts a killed mutant only when the executed test identities exactly match the passing baseline.                                                                                                 | A clean committed checkout.                                                 |
| `kernel`  | The official Bend release gate.                                                                                                                                                                                                             | `BEND_SOURCE_ROOT` and `OPENERP_OWNER_ADAPTER`. There is no local fallback. |
| `company` | An independent reviewed business-case comparator.                                                                                                                                                                                           | `EXCELLENCE_COMPANY_CASES` and `EXCELLENCE_COMPANY_OBSERVED`.               |
| `release` | All three additional stages together.                                                                                                                                                                                                       | Every prerequisite above.                                                   |

A missing prerequisite keeps its lane `blocked`; it is never downgraded to a
pass. Read `run.json` and `verdict.json` under
`test-results/excellence/<run>/` before any test count: a green tooling counter
is not a qualification. `core` and `stress` do not imply production readiness,
and the recovery drill shares one PostgreSQL cluster rather than qualifying
production object-store, IAM, network or old-writer recovery.

## Evidence and gates

Each successful or failed run retains a readable result, source/environment manifest, machine-readable assertions, sanitized requests/receipts/ledger observations, setup/runtime/cleanup logs and relevant browser/export artifacts. Preserve a run before another overwrites it. Link approval → receipt → voucher → evidence.

The current runner preserves previous local runs under `test-results/e2e-history`.
Its manifest hashes tracked and untracked files in declared source roots, including
new tests. Teardown compares that inventory with startup and fails on a difference.
Require a successful command, nonempty passing results and stable source integrity
together. See [the suite evidence contract](../apps/api/tests/README.md#run-evidence)
for exclusions; a hash is an identity check, not deployment or company acceptance.

Record revision plus dirty-input, lockfile, migration, contract, rule and validator hashes; runtime/database/browser versions; locale/timezone/time anchor/seed; selected, collected and executed cases; expected/observed values; failures, omissions and retries; exact replay commands and working directories. Capture evidence before teardown and report cleanup failure separately. Exclude credentials, session files and company data; traces may contain headers and forms.

| Gate                     | Required evidence                                                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| Every product change     | Strict static checks, relevant real Worker/PostgreSQL cases, core browser journeys and nonempty collection.                    |
| Migration change         | Clean-baseline fresh/rerun, checksum-drift refusal and effective grants for this reset; forward-migration proof after release. |
| Runtime/packaging change | Built routing, assets, service binding and financial journey.                                                                  |
| Capability release       | Applicable corpus, races, reports, restore and operational cases at fixed versions.                                            |
| External capability      | Authorized environment, exact integration stage and provider receipts.                                                         |

These are required gates, not claims of current CI coverage. Missing prerequisites, required validators, fixtures or cases fail the lane. Skipped/cancelled jobs and empty check sets cannot yield readiness. Include SQL, rules/fixtures, runtime configuration and lockfile changes in affected gates; retain evidence on success and failure.

Start serially across files and with zero retries; keep deliberate concurrency inside cases. Shard only after proving isolation and measuring need. Diagnostic retries retain the first failure and cannot silently pass flaky financial behavior. Measure named scenario coverage, first-attempt reliability and duration. A nightly run, benchmark score or coverage percentage cannot replace the required outcome.
