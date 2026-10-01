# Stable Effect runtime repair

The repair is committed as `854ae4deefafbd8141918466062e93333ed8c9c0` in the exclusive `/Users/admin/.codex/worktrees/effect-runtime-repair/openERP` worktree on `codex/effect-runtime-repair`. The failing listener regression is the preceding commit `a9725ff`. The worktree is clean.

The original runtime failures are repaired. The maintained package patch corrects the installed library, and the application boundary preserves its existing money, timestamp, privacy, and HTTP contracts. The completed source tree passed eight selected E2E tests and all required focused/static gates.

## Failure expectations before implementation

- A wrong database password must return safe correlated HTTP 503. The diagnostic must retain `AuthenticationError` and SQLSTATE `28P01`, and omit the password and token.
- Real effect-mq `awaitWake` must resolve after another PostgreSQL connection sends a matching notification. No worker polling or local store mutation can satisfy this observation.
- A notification naming another queue must leave the waiter unresolved. A wildcard must wake it.
- Terminating the exact test-owned LISTEN backend must cause the library to acquire a different backend and receive another notification. Each subscription attempt must release its scoped connection before retrying.
- Runner application queries must retain exact application timestamp/int8 strings. Queue raw timestamps must remain `Date` values. Existing credit and preparation receipts must complete without duplicate accounting effects.
- A fresh frozen install must apply the committed source and emitted-module patch. No runtime mutation, compatibility wrapper, dependency downgrade, or second queue is permitted.
- The newly observed recovery-inventory contract must accept exactly seven table fingerprints and exactly two queue sequences. Independent refusal/acceptance vectors are table lengths 6/7/8 and sequence lengths 1/2/3. Exercise the real exported decoder before changing this newly scoped root.

## Work steps

1. Reproduce it yourself on the matching surface through the applicable Codex browser, computer-use, terminal, or project verification skill (Non-negotiables). Completed in the diagnosis report.
2. Binary-search the cause. Completed through real runtime failures and independent contract probes.
3. Plan the fix. The parent accepted the three direct boundary repairs. Write and run listener E2E before production edits.
4. Verify on the same surface. Completed with eight passing E2E tests and stable source integrity.
5. Stage the commits so the failing repro lands before the fix in git history. Completed as `a9725ff` followed by `854ae4d`.
6. Run Opening a PR. Skip, the parent authorizes local commits only.

Throughput checkpoint: the smallest complete unit combines the listener regression with the installed-package correction, then the application classifier/registry repairs and existing journeys.

## Implemented changes

`apps/api/src/db/connection.ts` exports its existing native registry. The runner application pool reuses it. The queue pool keeps native defaults, including raw timestamp `Date` values. The Promise-based node-postgres parser configuration remains with its owning connection path.

`apps/api/src/db/transaction.ts` classifies native `AuthenticationError` as `Unavailable`. The diagnostic E2E retains HTTP 503 and checks `AuthenticationError`, SQLSTATE `28P01`, and absence of the password and token from the correlated diagnostic.

`patches/effect-mq@0.7.0.patch` changes only the published PostgreSQL store source, emitted store module, and generated schema declaration. It acquires the notification queue through `Effect.flatMap`, consumes `Stream.fromQueue`, reads `notification.payload`, and scopes each subscription attempt before the existing catch/sleep/retry loop. Wildcard routing, polling recovery, claims, retries, and leases retain their existing owners.

The first check exposed a separate published declaration mismatch against pinned Drizzle. Faithful declaration generation from unchanged `src/drizzle-postgres/schema.ts` adds `isAlias: false` to each of its seven table factories. The installed declaration exactly matches the generated output SHA-256 `2ccc85c84864f9d427be3e454e8f1a22edf903c56f93d38c559af356cbd338ce`. No schema factory, runtime table, cast, or lint/type suppression changed. An initial suspicion about emitted `TTableName` was rejected because faithful regeneration retains that identifier; the required table alias metadata was the decisive mismatch.

The broader API type check then exposed `Schema.isLengthBetween` in the retained recovery-inventory contract. The public contract failed at import time. `packages/contracts/src/operations.ts` now uses stable `isMinLength` and `isMaxLength` filters with the same exact cardinalities. The six independent length vectors pass. This extra root was explicitly added to scope by the parent before editing it.

`docs/adr/0009-effect-mq-background-jobs.md` records the maintained patch, separate codec ownership, and the upstream release condition for removing the patch.

## Failure-first and verification evidence

The listener E2E was committed first as `a9725ff`. The unpatched library produced one failed test and repeated `channel.transform` defects in `test-results/effect-runtime-listen-red`. Its first expected LISTEN backend never appeared. The same test then passed with real PostgreSQL notification delivery and reconnection. It exercises the library's public `awaitWake`, so no worker polling or local store mutation can satisfy the positive assertions.

The first repaired runtime run passed all seven diagnostics, credit-document, and listener tests. `test-results/effect-runtime-repair-final` then passed eight selected tests, including the normal self-host/preparation journey after its web build. Twelve unrelated document-reader tests were skipped. That run retained stable source inventory, synthetic local provider fixtures, actual PDF/credit receipts, queue PID observations, and a self-host extraction receipt. It preceded the extra recovery-contract repair. The completed-tree rerun below supplies the final evidence.

The completed tree then passed the same eight selected tests in `test-results/effect-runtime-repair-final-head`, with twelve unrelated tests skipped. Its `source-integrity.json` records `stable`, no changed paths, and identical source inventory SHA-256 `053bfee49123051d6ce824eadaa64f6f6281e7a17cd41a9f9cf37f56c8c9e4fb`. The listener receipt records matching delivery on PID `62583` and wildcard delivery after reconnection on PID `62589`. The normal self-host receipt proves the Bun preparation worker reads retained originals using local provider fixtures. The credit receipts prove document recovery without another accounting posting.

Run the final proof from the worktree root.

```sh
OPENERP_E2E_ARTIFACTS=test-results/effect-runtime-repair-final-head bun run test:e2e apps/api/tests/queue-listen.e2e.test.ts apps/api/tests/diagnostics.e2e.test.ts apps/api/tests/credit-document.e2e.test.ts apps/api/tests/document-reader.e2e.test.ts -t 'queue notifications|connection failures|retained schema failures|database faults|real Worker|credit PDF recovery|VAT capture|normal self-host'
```

The install and check artifacts are at `/Users/admin/.codex/worktrees/effect-runtime-repair/openERP/test-results/effect-runtime-repair-install/`.

- `frozen-install-final.log` records successful `bun install --frozen-lockfile --force` after removing the unrelated `.bun-tag` metadata hunk from the persisted patch.
- `installed-patch-final.json` records Bun `1.4.0`, TypeScript `7.0.2`, pinned Drizzle `1.0.0-rc.5-5935859`, manifest/lock/patch hashes, generated declaration identity, and unchanged installed source/module/schema hashes after reinstall.
- `declaration-diff.patch` records the generated declaration diff. `declaration-generation.log` and the command in the installed-patch receipt make it repeatable.
- `operation-length-contract-probe.ts`, `operation-length-red.json`, and `operation-length-green.json` retain the real exported decoder's import failure and all six refusal/acceptance results. Run the probe with Bun from the worktree root.
- `check-fast-final.log` and `check-full-final.log` record passing changed-file gates against the packet base `b72a463beb5246f9cc805fce62106af10d294456`, including API, runner, contracts, and test imports.
- `api-types-red.log` retains the broader API failure on the removed schema API. `api-types-final.log` records the passing broader API source and scripts check after repair.
- `check-integration.log` records the passing domain integration declaration check. `web-build.log` records the successful normal web build required by the self-host test.
- `delivery.json` records the final commit, binary diff hash against the packet base, and matching patch/source/module/schema hashes after the final runtime run. The cleaned patch SHA-256 is `72935be3cd522d5168fe7f33d57206bb7690d4c56c1ce2790d2d40f624a9be19`.

The supplementary `check:tests` launch accidentally overlapped the broader API check. It was canceled and is not reported as passing. Exact task-owned compiler/launcher PIDs were inspected, received TERM, and then KILL when they remained. Subsequent inspection found no survivors. Final changed-file type checks include the edited E2E files and their imports.

## Review and limits

The parent reviewed the diff and identified an unrelated Bun install-metadata hunk. It was removed, and the cleaned patch passed another frozen reinstall. The parent found no new narrating comments. The repair keeps one queue implementation and stable dependencies. No runtime monkey patch, wrapper, dependency downgrade, rule weakening, or unit test added after production code is present.

All data and provider fixtures were synthetic and local. No live provider, company data, migration change, deployment, push, external message, or production action occurred. The E2E global source inventory does not include patch files; the separate installed-patch receipt supplies their exact identities. The parent's integrated baseline should include `patches` in its integrity inventory before relying on that inventory alone for dependency-patch mutation detection.

## Principles that changed decisions

- **Fix Root Causes** kept the invalid application registry, obsolete LISTEN contract, missing declaration metadata, and removed recovery-schema API separate. Each correction follows its observed failure.
- **Boundary Discipline** keeps database classification in its application boundary and notification decoding in the existing library adapter.
- **Laziness Protocol** reuses the existing registry and corrects the installed library directly. It avoids a second queue and duplicate schemas.
- **Test Behavior, Not Implementation** uses public queue waits, external PostgreSQL notifications, real receipts, and independent exact-length expectations.
- **Sequence Work into Verifiable Units** commits the failing listener proof before the repair.
- **Prove It Works** requires a frozen installed artifact, same-surface E2E rerun, source integrity, and generated declaration identity.
