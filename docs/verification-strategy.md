# Verification strategy

Status: requirements for the existing E2E suite; coverage remains tied to actual run artifacts. [E-01–E-21](verification.md) define outcomes; the [acceptance plan](plans/09-acceptance.md) supplies independent examples. Test changes require the authorization in [AGENTS.md](../AGENTS.md).

## Runner and environment

Run `bun run test:e2e` from the root. [Vite+](../vite.config.ts) runs Vitest over `apps/api/tests` and `apps/web/tests`; Playwright drives browser actions. The [suite instructions](../apps/api/tests/README.md) specify prerequisites and `test-results/e2e` artifacts. Preserve this runner unless a demonstrated need warrants a change.

Drive public requests through the real API Worker and PostgreSQL. Give the Worker only a restricted runtime login. Use separate maintenance credentials for setup and independent database observations. Browser journeys use the same operations. Do not replace internal services or wrap the suite in an outer transaction: requests must commit and remain visible to fresh connections.

Own a disposable database/cluster, fresh actors/books and bounded process/port lifetimes. Refuse unexpected or pre-existing targets. Concurrent workers need separate databases unless isolation is proved. Readiness checks database/migration access as well as HTTP health. Reused servers must match the revision and configuration. Teardown removes only run-owned resources, including after setup failure.

Use production migration/provisioning commands. Check fresh install, rerun, rejection of changed applied migrations and populated upgrade. Preserve old values, identities, seals, approvals and receipts. Inspect effective grants and attempt forbidden table/function access under the runtime login.

Label runtime evidence precisely:

| Surface                         | What it can establish                                                                   |
| ------------------------------- | --------------------------------------------------------------------------------------- |
| Local workerd/direct PostgreSQL | Local API, transactions and resource cleanup.                                           |
| Browser/Vite proxy              | Development routing and interaction.                                                    |
| Built web/API Workers           | Assets, service binding and deployment composition.                                     |
| Managed Hyperdrive              | Actual uncached reads, networking and connection behavior in an authorized environment. |
| Bun                             | Migration/maintenance behavior; separately exercise any self-host application adapter.  |

## Expectations and fault control

Write failure outcomes before implementation. Use small synthetic fixtures with scenario/invariant IDs, provenance, exact expected values and profile/rule/schema versions. Do not compute expectations with the production calculator or backfill unit tests after implementation.

For a fresh-book posting of `12500` minor units, expect two lines, bank/clearing balances `12500`/`-12500`, sequence and series number `1`, one receipt, one outbox event and one consumed approval. Observe through a fresh request and connection. Retry preserves those counts; reversal retains the original and returns balances to zero. This is arithmetic proof, not a tax example.

Also cover `9007199254740993`, the `10^38 - 1` line boundary, overflow and aggregates beyond a line's bound. Distinguish lexical admission from SQL integrality/range checks. Reject numeric JSON money, fractions, exponent forms, negative zero, invalid dates and unsupported precision. Specify canonicalization bytes/hashes independently, including key/array order, Unicode and duplicate keys. Old seals remain interpretable.

Anchor fixture time explicitly. Browser clock overrides do not change database approval expiry. Format corpora retain raw-byte hashes, encoding, feature coverage and expected semantics, including Swedish characters and correction records. Roundtrips can share bugs; use independent facts and pinned validators with known exclusions. Demonstrate that a deliberately wrong expectation fails, without weakening product validation.

Synchronize races through observed locks or test-owned barriers with bounded timeouts. Concurrent promises alone do not prove overlap. Allow each valid serialization. Test competing first executions separately from replay after success. Drop a response after commit; recover by durable identity. Connection loss during commit does not prove rollback. Real transaction failures must leave no partial effects, counters, approval consumption, receipts or outbox state.

Remove test-owned fault fixtures after use. Keep fault controls out of public product endpoints. Simulate external providers only for deterministic failure cases and label the result; sandbox acceptance and model evaluations are separate runs. Exercise oversized, interrupted and slow streamed bodies with/without declared lengths through REST/MCP, followed by a valid request and cleanup checks. MCP proof includes a real client, negotiation, schemas and error envelopes.

## Human journeys

Use accessible roles/labels and real actions. Check source bytes, exact lines, displayed digest, approval and durable receipt together. Cover stale, denied and uncertain outcomes, reload/recovery, logout and identity/book cache changes. Assert persisted results beyond labels, screenshots or HTTP success.

Cover Swedish/English money/date presentation, keyboard/focus recovery, narrow layouts and reduced motion. Record actual 200% browser zoom, contrast and screen-reader observations separately; viewport resizing does not prove them. Keep decisive success screenshots and failure traces. Downloaded reports need exact fact/hash checks and independent semantic validation where applicable.

## Evidence and gates

Each successful or failed run retains a readable result, source/environment manifest, machine-readable assertions, sanitized requests/receipts/ledger observations, setup/runtime/cleanup logs and relevant browser/export artifacts. Preserve a run before another overwrites it. Link approval → receipt → voucher → evidence.

Record revision plus dirty-input, lockfile, migration, contract, rule and validator hashes; runtime/database/browser versions; locale/timezone/time anchor/seed; selected, collected and executed cases; expected/observed values; failures, omissions and retries; exact replay commands and working directories. Capture evidence before teardown and report cleanup failure separately. Exclude credentials, session files and company data; traces may contain headers and forms.

| Gate                     | Required evidence                                                                                           |
| ------------------------ | ----------------------------------------------------------------------------------------------------------- |
| Every product change     | Strict static checks, relevant real Worker/PostgreSQL cases, core browser journeys and nonempty collection. |
| Migration change         | Fresh/rerun and populated upgrade; retained effects and restricted grants.                                  |
| Runtime/packaging change | Built routing, assets, service binding and financial journey.                                               |
| Capability release       | Applicable corpus, races, reports, restore and operational cases at fixed versions.                         |
| External capability      | Authorized environment, exact integration stage and provider receipts.                                      |

These are required gates, not claims of current CI coverage. Missing prerequisites, required validators, fixtures or cases fail the lane. Skipped/cancelled jobs and empty check sets cannot yield readiness. Include SQL, rules/fixtures, runtime configuration and lockfile changes in affected gates; retain evidence on success and failure.

Start serially across files and with zero retries; keep deliberate concurrency inside cases. Shard only after proving isolation and measuring need. Diagnostic retries retain the first failure and cannot silently pass flaky financial behavior. Measure named scenario coverage, first-attempt reliability and duration. A nightly run, benchmark score or coverage percentage cannot replace the required outcome.
