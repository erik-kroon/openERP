# Stable Effect runtime diagnosis

The two selected E2E failures reproduce on `b72a463beb5246f9cc805fce62106af10d294456` in `/Users/admin/.codex/worktrees/effect-runtime-repair/openERP`, branch `codex/effect-runtime-repair`. No application source, tests, manifest, or lockfile changed. `bun install --frozen-lockfile` passed.

The database-password failure is an application error-classification omission. The stalled credit-document background receipt has two independent causes. The runner passes the old node-postgres parser configuration to the native PostgreSQL client. effect-mq also consumes the obsolete `PgClient.listen` return contract.

Throughput checkpoint: n/a, read-only forensics.

## Evidence and repeatable run

Run from the isolated worktree.

```sh
OPENERP_E2E_ARTIFACTS=test-results/effect-runtime-diagnosis-20261001 bun run test:e2e apps/api/tests/diagnostics.e2e.test.ts apps/api/tests/credit-document.e2e.test.ts -t 'connection failures|credit PDF recovery'
bun test-results/effect-runtime-diagnosis-20261001/contract-probe.ts
```

The existing tests produced two failures and four skipped tests. The selected credit recovery timed out after its 30-second receipt deadline. The wrong-password request returned HTTP 500 instead of 503. The expected deliberate credit checkpoint fault still returned 503 before the background recovery phase.

The [results](/Users/admin/.codex/worktrees/effect-runtime-repair/openERP/test-results/effect-runtime-diagnosis-20261001/results.json) and artifacts are at `/Users/admin/.codex/worktrees/effect-runtime-repair/openERP/test-results/effect-runtime-diagnosis-20261001/`.

- `manifest.json` records the revision, lockfile, runtimes, migrations, and source inventory.
- `source-integrity.json` records `stable`, no changed paths, and identical initial/final SHA-256 `f2f2ee1e4acdbfd038823d47a5d2e90a3dd03cd39519bd81d05d9fd7953fa146`.
- `diagnostics-worker.json` retains the authentication cause, SQLSTATE, request ID, and HTTP route.
- `credit-render-runner.log` retains all four dispatch failures and repeated LISTEN failures.
- `contract-probe.ts` and `contract-probe.json` provide a repeatable, database-free reproduction of both dependency-contract mismatches. This is a diagnostic artifact, not an added test or product implementation.
- `upstream-package-evidence.json` retains the registry inventory, upstream head, declared peers, and upstream LISTEN excerpt observed at `2026-10-01T10:21:45.136Z`.

## Wrong password becomes the wrong application error

The retained Worker cause is `SqlError` with `reason._tag === "AuthenticationError"` and original PostgreSQL `code === "28P01"`. The native driver's `src/internal/sqlError.ts` maps SQLSTATE class `28` to `AuthenticationError`. This is a valid connection-startup refusal.

`apps/api/src/db/transaction.ts` recognizes native `ConnectionError`, transient lock/transaction errors, and selected raw SQLSTATE classes as `Unavailable`. It omits `AuthenticationError` and class `28`. Because the retained cause satisfies `PostgresFailure`, this omission reaches its explicit `InternalError` return. The public result becomes HTTP 500.

The minimum repair is to include native `AuthenticationError` in the database boundary's unavailable classification. Preserve HTTP 503, the safe public error, request correlation, SQLSTATE retention, and secret redaction. Change the diagnostic test's log expectation from `ConnectionError` to `AuthenticationError` and assert `28P01`. That reflects the actual driver contract without lowering the HTTP expectation. Do not normalize the native cause into a false `ConnectionError` or change the expected public status.

## The runner gives the native client the wrong parser object

`apps/api/scripts/preparation-runner.ts` creates separate queue and application pools. This separation is intentional. Its application pool imports `applicationPostgresTypes` from `apps/api/src/db/connection.ts` and passes it as `PgClient.layer({ types })`.

`applicationPostgresTypes` is a `pg.CustomTypesConfig` object with `getTypeParser`. It belongs to the Promise-based node-postgres connection used by Better Auth. Stable `@effect/sql-pg` requires a `PgTypes.Registry`, created through `PgTypes.makeRegistry()` and recognized by its private registry state. It cannot consume a `getTypeParser` object.

The contract probe calls the native encoder with that same object. The exact failure is `PgTypesCodecError` with message `Invalid PgTypes Registry`. The existing credit E2E log reports the corresponding stack through `lookupFor`, `writeParameter`, `encodeQuery`, and `EffectDrizzleQueryError`. The application query fails before PostgreSQL receives it. The dispatcher then leaves the outbox intent pending. This failure also affects the preparation, extraction, and period-work dispatchers.

`apps/api/src/db/connection.ts` already constructs a valid private `nativePostgresTypes` registry for request-owned database composition. Its timestamp/timestamptz decoders retain six fractional digits as a string, while its int8 decoder retains an exact decimal string. Its encoders call the native binary codecs. The simplest runner repair is to export and reuse this registry for the application pool. Keep the queue pool on native default codecs.

The native defaults decode OID 20 as `bigint` and OIDs 1114/1184 as `Date`. The probe verifies these values. Native encoding accepts int8 bigint, timestamps as `Date` or epoch milliseconds, and untyped string parameters for PostgreSQL inference. Drizzle's Effect driver casts typed timestamp projections to text and applies its field decoder. effect-mq raw projections independently call `.getTime()` on timestamps and `Number(...)` on queue counters. Sharing the application's string timestamp registry with the queue would violate the queue's raw-read contract.

| Application codec shape | Queue codec shape | Judgment |
| --- | --- | --- |
| Reuse existing `nativePostgresTypes` | Leave `types` absent | Smallest coherent repair. Both owners retain their current intended contracts. |
| Construct a second application registry with the same codecs | Leave `types` absent | Valid, but duplicates timestamp precision and int8 policy. No observed benefit. |
| Reuse application registry for both pools | Application timestamp strings | Reject. effect-mq raw timestamps require `Date`. |
| Remove application codec override | Native defaults | Removes the invalid object, but does not preserve the established raw application timestamp/int8 string contract. Requires a wider caller audit. |

## effect-mq calls the obsolete LISTEN API

The installed `effect-mq@0.7.0` source at `src/drizzle-postgres/DrizzleJobStore.ts:421` pipes `client.listen(wakeChannel)` directly into `Stream.runForEach`. It treats each element as a payload string.

Stable `@effect/sql-pg@4.0.0` declares the following return shape in `src/PgClient.ts:62`.

```ts
Effect.Effect<Queue.Dequeue<PgConnection.Notification, SqlError>, SqlError, Scope.Scope>
```

Each notification has `processId`, `channel`, and `payload`. The library therefore treats an Effect as a Stream and fails while reading its nonexistent stream channel. The contract probe reproduces the exact `TypeError` on `channel.transform`. The existing E2E log shows the same failure every second. Its catch/retry path deliberately retains polling, so the LISTEN warning alone does not prove that polling can never complete. The invalid application registry independently prevents admission and handling in this run.

The direct correction belongs in the existing library's PostgreSQL store. Acquire the notification queue with `Effect.flatMap`, consume it with `Stream.fromQueue`, and feed `notification.payload` to the existing `signalWake`. Preserve the wildcard payload, scope lifetime, original SQL errors, one-second resubscription loop, and polling recovery. Stable `SqlClient.stream` still returns a Stream. The incompatible return contract is specifically `PgClient.listen`.

## Declared peers do not prove API compatibility

The installed effect-mq package declares `effect`, `@effect/sql-pg`, and `@effect/vitest` peers `>=4.0.0-rc <5` and Drizzle `>=1.0.0-rc <2`. The pinned stable versions satisfy those declared ranges. The concrete LISTEN code still uses the earlier API.

The [npm registry](https://registry.npmjs.org/effect-mq) lists `0.7.0` as latest and no later published version. The [upstream main head](https://api.github.com/repos/TeamWarp/effect-mq/commits/main) remains `b5898fbae56fe926c28768a5a8ff9ad74f1e57a0`. Its [PostgreSQL store source](https://github.com/TeamWarp/effect-mq/blob/b5898fbae56fe926c28768a5a8ff9ad74f1e57a0/packages/effect-mq/src/drizzle-postgres/DrizzleJobStore.ts#L421) contains the same obsolete LISTEN call. The [package peers](https://github.com/TeamWarp/effect-mq/blob/b5898fbae56fe926c28768a5a8ff9ad74f1e57a0/packages/effect-mq/package.json) do not establish a supported repaired stable release. No published upgrade candidate solves this failure today.

## Competing implementation shapes before code

The parent requested comparison of a direct Bun package patch with a downgrade after these roots were reported. No patch was applied during diagnosis.

| Shape | Benefit | Cost or limit |
| --- | --- | --- |
| Export the existing native application registry, classify `AuthenticationError`, and retain a Bun `patchedDependencies` correction to the effect-mq store | Repairs the actual owners with a small diff. Preserves stable Effect and the existing queue implementation. A package patch changes the library implementation directly, rather than wrapping its public API. | Commit the patch, manifest and regenerated `bun.lock`. Confirm both installed source and emitted JavaScript contain the correction. Frozen reinstall and listener/recovery E2E must prove the installed artifact. |
| Same application repairs plus a maintained source fork of effect-mq | Direct library ownership without a runtime mutation or compatibility wrapper. Preserves stable Effect. | Larger provenance, packaging and maintenance obligation. Still needs the same concrete LISTEN correction and installed-artifact proof. |
| Downgrade Effect and associated platform/SQL packages to the old supported API family | May recover the older library contract. | Reject for this packet. Abandons its stable-Effect prerequisite, changes many packages, and does not repair the stable dependency mismatch. Its exact older combination remains unverified here. |
| Repair only the application registry and error classification | Likely permits polling to make progress, inferred from the source separation. | Leaves LISTEN broken. A passing credit receipt would not establish compatibility or notification recovery. |

The minimum complete path is a direct correction to the existing library plus the two application-boundary repairs. I recommend the reviewed `patchedDependencies` source correction requested by the parent for comparison. It is smaller than a fork and leaves the existing queue owner intact. This treats the original no-monkey-patch rule as forbidding runtime mutations, rather than a persisted library-source repair. Implementation remains gated on the parent's rebrief.

The [official Bun patch documentation](https://bun.sh/docs/pm/cli/patch) confirms that `bun patch effect-mq@0.7.0` first creates an unlinked package copy. `bun patch --commit` then writes a patch, updates the manifest and lockfile, and reapplies the patch during installs. Run the preparation command before editing installed files so other worktrees and the shared Bun cache remain untouched. Do not add a second queue, runtime monkey patch, old/new API compatibility shim, or weaker receipt assertions.

Before calling the repair complete, rerun the existing diagnostics and credit-document tests against a fresh frozen install. Preserve the 503 and privacy contract, PDF success/failure receipts, exact document digest and bytes, unchanged accounting balances, idempotent replay, and outbox recovery. Add focused existing-system E2E coverage for real `LISTEN` delivery and disconnect/resubscribe if the current tests do not prove those mechanisms. A receipt completed by fallback polling alone cannot prove LISTEN repair.

## Principles that changed decisions

- **Fix Root Causes** kept the codec-registry failure separate from the noisy LISTEN warning. Both reproduce independently in the retained probe.
- **Boundary Discipline** places database authentication classification in `databaseFailure` and notification decoding inside the library adapter. It avoids false cause normalization and scattered guards.
- **Laziness Protocol** favors reuse of the existing native application registry and a direct existing-library correction. It rejects duplicate codec policy and a second queue implementation.
- **Prove It Works** required a fresh frozen install, real Worker/Bun/PostgreSQL reproduction, source-integrity receipt, and repeatable contract probe. Declared peers and compilation are insufficient evidence.

Diagnosis is complete. Implementation remains unstarted pending the parent's rebrief.
