# Stable accounting baseline

Packet 1 runtime acceptance passed on 2026-10-01 at committed source `375bea6def60db083e3642f3cc13dee9e0699be9`, branch `codex/whole-year-baseline`. The disposable PostgreSQL/workerd E2E run passed all 269 tests in 65 suites, with zero failures and zero skipped tests. This establishes the integrated engineering baseline, not whole-year completion or actual-company accounting qualification.

The clean isolated checkout combines the captured stable-Effect changes, the cash commercial-invoice period guard repair, and the PostgreSQL codec/authentication/queue compatibility repair. Original migrations remain unchanged. The run applied 52 migrations through `0048-cash-invoice-recognition-period.sql`, SHA-256 `9997994f777c091bfb668c24af3283d4b7cc49a147a71e236983f1d93034fee2`.

## Verification

Frozen dependency installation, changed-file fast/full gates against `b72a463`, web build, and the domain integration gate passed before the full runtime run. Integration reported 33 wired and 17 explicitly deferred domain leaves. Deferral is not delivery.

The built-in source-integrity gate passed. A supplemental manifest selected 1,994 tracked source files, including the dependency patch, and excluded `apps/api/.dev.vars.five`. Before/after inventories are identical, SHA-256 `70e3f765998b9bae1cc1d9b306b188451a53b70e62a095c58e5c8cc688c87969`; manifest SHA-256 is `718789c2908eff968c4f938eb4ea414fe5aebc3d8e7384d8106c27d7e01abd36`. Installed effect-mq source/module/declaration, unchanged schema source, lockfile and built web shell hashes remained identical from the early-runtime observation, approximately 18 seconds after launch, through completion. Despite its filename, `installed-before.json` is not a strict prelaunch observation. The raw built-in inventory hashes `apps/api/.dev.vars.five` and omits patches; the supplemental scope supplies patch coverage and does not retroactively change configuration hashing.

Repeat from this revision in an isolated checkout with the repository's disposable local prerequisites:

```sh
bun install --frozen-lockfile
bun run check:changed b72a463
bun run check:changed:full b72a463
bun run --filter web build
bun run check:integration
OPENERP_E2E_ARTIFACTS=test-results/integrated-accounting-baseline-repeat bun run test:e2e
```

Use a fresh artifact name and private output permissions. The actual run used `test-results/integrated-accounting-baseline-20261001`; JSON results, manifest, migration/runtime logs and source integrity are retained there. Supplemental source/tool/install identities and the exit-zero receipt are in `test-results/integrated-baseline-proof-20261001-v2`. These ignored local artifacts are retained in the attached isolated worktree, not published company records.

The JUnit reporter's actual file was observed under `test-results/e2e-history/2026-10-01T11-02-07.632Z-9b735bf8/junit.xml`, reporting 269 tests and zero failures. A byte-identical copy is retained with the run; `junit-location.json` records both paths and hashes. Reporter initialization preceding setup archival is an inference. JSON results and the process exit independently establish the result.

## Review and remaining scope

The runtime repair received independent source/artifact acceptance at its exact worker commit `854ae4deefafbd8141918466062e93333ed8c9c0`. Ordinary listener cancellation is supported by the scoped implementation but lacks a direct post-scope backend assertion. The final integrated run directly names its committed revision and includes patch identity, resolving the worker run's composite revision binding. A separate independent receipt/transcript audit accepted packet 1's local engineering-baseline predicate at the tested source and documentation-only evidence commit `6711199c384d8d27832877ee4ff2e95ca5619442`, with the observation-scope limits above retained.

The proof tools received independent v4 acceptance after real CLI admission/refusal and provenance exercises. Historical failed evidence remains preserved. The earlier `b72a463` run still records 222 passes and 45 failures, and its capture still discloses historical configuration hashing. New results do not rewrite that history.

Packets 2 through 20 remain separate obligations. Company-profile facts reported by the owner remain distinct from admitted original records and runtime activation. Missing settlement, recovery, evaluation, reference comparison and complete-year capabilities are not satisfied by this baseline.
