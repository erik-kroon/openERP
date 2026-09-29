# Assurance suite integration

Status: **installed and fast-lane green.** Runtime/full/mutation lanes are deferred to CI or a
clean worktree (see remaining gates).

## Provenance

- Source: `openerp-testing-suite.zip`, reviewed against `erik-kroon/openERP@6bcfe1e`.
- Installer dry-run reported zero source drift; `--apply` wrote 29 files and nothing else.
- Added paths: `apps/api/tests/assurance/` (5 conformance + 6 E2E tests, 2 support helpers)
  and `verification/assurance/` (corpus, runner, gates, mutation scripts).
- Installed files diverge from the suite's `overlay-manifest.json` checksums: repo `oxfmt`
  reformatted them and `oxlint --fix` added blank lines for anti-slop rules. No test semantics
  were changed by formatting; the fast-lane rerun below is the authority, not byte identity.

## Decisions

- **Tests do not wire domain leaves** (`scripts/check-integration.ts`): conformance tests import
  leaves to prove contracts, but no application owner composes them, so test-owned files
  (`*/tests/*`, `*.test.ts(x)`) are excluded from consumer detection. `cash-method` therefore
  stays `deferred` instead of being falsely marked `wired` by its new conformance test.
- **Delivered-test repairs, all semantics-preserving**: `%j` to `%s %s %s %s` in the
  release-refusal title (`JSON.stringify` throws on BigInt at collection; `%s` also consumed
  only the first element, collapsing four identities); explicit guard/`?.`/type annotation for
  three strict-TS errors; blank-line lint fixes plus a 5-binding destructure split in `gates.mjs`.

## Verified results

- `node verification/assurance/scripts/run.mjs fast`: **passed** at `03e3b74`
  (harness 26/26, pure 553/553, fixed-revision digests match).
  Evidence: `test-results/assurance/2026-09-29T07-24-46.880Z-1438bd63…/run.json`.
- `bun run check:tests`: green. `oxlint` on both overlay paths: clean.
- `bun run check:integration`: only failure is `party-identity`, which is another effort's
  uncommitted owner work, not this suite.

## Remaining gates

- `run.mjs runtime`, `run.mjs full`, `mutate.mjs`: need a quiet checkout (concurrent commits
  invalidate fixed-revision evidence), PostgreSQL 17, and the Bend toolchain for the release lane.
- Corpus provenance and coverage boundaries: see
  `verification/assurance/corpus/README.md` and `verification/assurance/scenario-register.json`.
