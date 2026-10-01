# Baseline proof trail and cash-period review

## Verdict

Packet 1 remains correctly reported as incomplete. The retained baseline receipts consistently show a stable source run at `b72a463beb5246f9cc805fce62106af10d294456` with 267 tests, 222 passing and 45 failing. The JUnit relocation claim is also byte-consistent. The proof trail is not ready to be treated as independently auditable because the canonical decision log omits material actions, the initial capture receipt was manually adapted and is not reproducible from the retained `capture.py`, and the capture admission rules do not enforce the stated credential boundary.

The cash-period implementation review is separate. Immutable source `5c12de580fa6c4cfc74fc03e68e0a566cf422d25` differs from `b72a463beb5246f9cc805fce62106af10d294456` only by migration `0048-cash-invoice-recognition-period.sql` and 149 E2E lines. The source change is coherent with the existing database shape constraint. No completed runtime verdict is made here because the runtime proof area was still being assembled outside this review.

## Baseline findings

### High: the canonical decision trail omits the decisions that produced the baseline

Location: `/Users/admin/openERP/.codex/pstack-runs/whole-year-proof/decisions.tsv:2` through `:6`.

Contract: the show-me-your-work trail requires one canonical append-only log, one row per material decision or checkpoint, followed by an audit against this run's matching transcript.

Failure: the canonical log ends before the actual baseline outcome. It does not record the manual adaptation of `accepted.json`, the `.dev.vars.five` permission correction, the cash-method integration registry correction, checkpoint `b72a463`, the 45-test runtime failure, the JUnit relocation, or the decision to keep packet 1 open. Those actions appear in the worker-local `/Users/admin/.codex/worktrees/whole-year-baseline/openERP/test-results/stable-baseline-capture/decisions.tsv`, the retained artifacts, and assistant messages at 10:07:41, 10:15:35 and 10:19:56 in the matching task transcript.

Evidence: `/Users/admin/.codex/sessions/2026/10/01/rollout-2026-10-01T11-52-48-01a0f6e1-80a1-7e81-9d78-f6aa4e9e1b17.jsonl` has `session_meta.payload.cwd=/Users/admin/openERP` and the requested task id. No unrelated transcript was read.

Remedy: append superseding rows to the canonical log for each material checkpoint and point them to the retained receipts. Do not edit or delete the existing rows.

### High: the retained initial capture receipt cannot be produced by the retained capture script

Location: `/Users/admin/.codex/worktrees/whole-year-baseline/openERP/test-results/stable-baseline-capture/capture.py:56` and `:59`; `/Users/admin/.codex/worktrees/whole-year-baseline/openERP/test-results/stable-baseline-capture/accepted.json:7`.

Contract: evidence must resolve and show what the trail claims. A script hash proves provenance only when that exact script produced the receipt.

Failure: retained `capture.py` raises when the source and target inventories differ, including the observed 0600 versus 0644 filesystem permission on `apps/api/.dev.vars.five`. Its success writer emits `targetMatches`, while retained `accepted.json` contains `targetBytesMatch`, `targetGitModesMatch`, and `permissionDifferences`. The baseline report acknowledges that `accepted.json` was manually adapted, but the canonical decision log does not. `proof-script-sha256.json` matches the current scripts, so it does not identify the code that originally emitted the accepted receipt.

Evidence: `capture-verification.json` is internally consistent and the reusable verifier independently establishes byte equality, normalized Git-mode equality, stable before/after patch bytes, and the single filesystem permission difference. The initial acceptance receipt remains non-reproducible.

Remedy: retain `accepted.json` as historical, mark it non-authoritative, and append a decision row that names the manual adaptation. Future runs must preserve the original capture result and write any normalized verification to a separate receipt.

### High: the capture guard does not enforce the stated credential boundary

Location: `/Users/admin/.codex/worktrees/whole-year-baseline/openERP/test-results/stable-baseline-capture/capture.py:8` and `/Users/admin/.codex/worktrees/whole-year-baseline/openERP/test-results/stable-baseline-capture/source-proof.py:7`.

Contract: the baseline task excluded credentials and required private raw capture.

Failure: both `admitted()` functions use a denylist that excludes `.env*` but admits credential-like tracked or untracked names such as `apps/api/.dev.vars.five`. Both functions read admitted bytes. `capture.py` also copies every admitted untracked path rather than a reviewed explicit list. Current artifacts contain only the configuration file's hash and the binary patch does not contain that path, so no secret value was observed in this review. A future reuse can copy or hash credentials with a different name.

Evidence: `source-before.json` includes `apps/api/.dev.vars.five`. Current raw capture permissions are correctly 0700 for directories and 0600 for files, but those modes depend on execution context or later correction rather than explicit mode creation in `capture.py`.

Remedy: replace the denylist with a reviewed explicit path manifest for untracked files, reject credential-like paths including `.dev.vars*`, and set private directory and file modes in the capture program before writing bytes.

### Medium: the target precondition ignores untracked collisions

Location: `/Users/admin/.codex/worktrees/whole-year-baseline/openERP/test-results/stable-baseline-capture/capture.py:43`.

Contract: an isolated target must not overwrite unrelated state and then certify the result as an exact snapshot.

Failure: `git status --porcelain --untracked-files=no` checks only tracked changes. The later untracked copy loop overwrites an existing target path with `shutil.copy2`. A reused target could lose unrelated untracked bytes while the final inventory still matches the source.

Remedy: require a fully clean target including untracked files, or fail on every destination collision before applying the patch or copying bytes.

### Medium: the reusable verifier is pinned to attempt 1

Location: `/Users/admin/.codex/worktrees/whole-year-baseline/openERP/test-results/stable-baseline-capture/verify-capture.py:5`.

Contract: the capture loop permits attempts 1 through 3, and the report describes the verifier as reusable.

Failure: `verify-capture.py` always reads `attempt-1`. If attempt 1 observes changing source and attempt 2 or 3 succeeds, the verifier checks the wrong attempt.

Remedy: select the accepted attempt from an immutable capture receipt or an explicit CLI argument, and verify that selection against the receipt before reading its inventories.

### Medium: the relocated JUnit contains machine identity outside the sanitized proof folder

Location: `/Users/admin/.codex/worktrees/whole-year-baseline/openERP/test-results/stable-accounting-baseline/junit.xml:3`.

Contract: proof intended for review should separate private raw artifacts from sanitized receipts.

Failure: the copied JUnit is mode 0644 and contains the local hostname `MacBook-Pro-som-tillhor-Admin.local`; failure bodies also retain absolute `/Users/admin/...` paths. The sanitized proof folder stores only its hash and summary, which is appropriate, but the baseline report links the raw runtime artifact without naming this privacy limit.

Evidence: the original history JUnit and copied runtime JUnit have identical SHA-256 `ffd9204675991a1c82e853f493c9c3435bb8b62f933313637ce7629f9c710d81`. The original file was created at 12:06:57 and both files were finalized at 12:13:30; the destination birth time is 12:13:30. Its XML reports 267 tests, 45 failures, and zero reporter errors. This supports the copy-after-run claim and the counts, but does not make the raw XML shareable.

Remedy: keep raw JUnit private, publish only the hashed sanitized summary, and state the hostname and absolute-path limitation wherever the raw artifact is linked.

### Low: the first isolation decision points to unrelated evidence

Location: `/Users/admin/openERP/.codex/pstack-runs/whole-year-proof/decisions.tsv:2`.

Contract: each evidence cell must directly prove the row's decision or checkpoint.

Failure: `docs/plans/evidence/df-09-supplier-credit-cap.md` does not prove that concurrent processes were editing the original checkout or that an isolated snapshot was selected. The matching transcript at 09:55:21 and the retained capture artifacts support that decision.

Remedy: append a superseding decision row with the capture receipt and matching transcript timestamp as evidence.

## Baseline claims that held

- `e2e.exit` is `1`; `results.json`, `e2e.log`, `proof-summary.json`, and JUnit agree on 64 suites, 267 tests, 222 passed, and 45 failed.
- `manifest.json` names revision `b72a463beb5246f9cc805fce62106af10d294456`, 51 migrations, lock hash `a644afe2d8a4196a1092cb7ae61ca73b5ba65a7390c37538423cff11f69f3f65`, and final migration `0047-supplier-credit-cap.sql` with the reported hash.
- Built-in and supplementary source-integrity receipts report stable source with no changed paths. The supplementary before and after inventory hashes match over 1,985 admitted paths.
- All hashes in `artifact-sha256.json` and `proof-script-sha256.json` match the current named files.
- The two baseline-report copies are byte-identical.
- The cash-method integration registry correction is narrow and justified. Each of the three declared application consumers imports `@open-erp/domain/cash-method`; the note keeps runtime qualification pending. Formatting-only expansion of the unrelated bank-cover consumer array is harmless, although it is avoidable churn.

## Cash-period immutable source review

Reviewed refs: implementation `5c12de580fa6c4cfc74fc03e68e0a566cf422d25`; test-first parent `0c59dbb4e21a90cd3584fbb74a2d736756b82af7`; base `b72a463beb5246f9cc805fce62106af10d294456`.

Verdict: source is acceptable with one proof-artifact refactor target. Migration 0048 replaces the existing invoice trigger with the same function guarded by `NEW.recognition_voucher_id IS NOT NULL`. Existing `commerce_recognition_shape` requires both recognition identifiers for ordinary invoices and permits both null only for the retained supplier cash-invoice shape. The voucher trigger and all recognized-invoice period checks remain. The E2E addition drives the public cash-invoice HTTP owner, locks the synthetic document period, verifies no admission posting, verifies same-key replay, probes four malformed nullable shapes against the database constraint, and confirms the period stays locked.

The retained red log shows the test-first commit failing at the expected public response, 422 `InvalidJournal` instead of 200. A later local log reports 50 passing tests across seven relevant files. This review does not promote that log to a final runtime verdict because the parent stated that runtime proof was still changing; source status and runtime status remain separate.

### Medium: the E2E artifact serializes expected constants as observed proof

Location: `/Users/admin/.codex/worktrees/cash-period-admission/openERP/apps/api/tests/cash-invoice.e2e.test.ts:622` in test `locked document period admits only a constrained commercial cash invoice without posting`.

Contract: the final E2E artifact must be repeatable and verifiable from observed results rather than restating expectations.

Failure: `documentPeriodLocked: true`, `replayPreserved: true`, and each invalid invoice's `code` and `constraint` are hard-coded after assertions. The test assertions are meaningful, but the JSON artifact alone cannot distinguish observed values from expected values.

Remedy: retain the second population query, locked-period row, and caught database errors as observed values; assert those values and serialize the same values. The product migration does not need to change.

## Comment-sicko report

Touched files reviewed:

- Baseline: canonical `decisions.tsv`, `baseline-report.md`, `capture.py`, `source-proof.py`, `verify-capture.py`, capture inventories and receipts, stable proof receipts, runtime result/manifest/source-integrity/JUnit receipts, and the baseline-owned integration registry diff.
- Cash: immutable diff for `apps/api/migrations/0048-cash-invoice-recognition-period.sql` and `apps/api/tests/cash-invoice.e2e.test.ts`, plus the scoped `.codex/cash-period-admission` plan and retained logs.

Deletion candidates: zero new narrating comments in owned proof scripts or the cash two-file diff. Existing comments in pre-base migrations and tests were skipped because they are not newly authored work in this scope. Imported vendored code under `config/oxlint/anti-slop/vendor` was not reviewed as task-authored code.

Exact `MUST KILL` targets:

- `capture.py::admitted` and `source-proof.py::admitted`: replace the credential-blind denylist with an explicit reviewed admission manifest and private-mode writes.
- `capture.py` target cleanliness guard at line 43: reject untracked collisions before copying.
- `verify-capture.py::attempt` at line 5: bind verification to the actually accepted attempt.
- `cash-invoice.e2e.test.ts` test `locked document period admits only a constrained commercial cash invoice without posting`, artifact serialization at lines 622 through 640: serialize observed replay, lock, and rejection data.

Justified exceptions: no new code comments qualified for retention because the reviewed new source contains none. The baseline report's explicit statement that JUnit relocation cause is an inference is retained because it correctly limits an unproved causal claim. The cash migration's direct trigger replacement is retained because the predecessor trigger is guaranteed by migration order and the forward migration is intentionally immutable.

## Review limits

No checks, database access, provider access, credentials, company data, process changes, or source edits were performed. Only this report was written. The baseline transcript was available and matched both the required cwd and task id. The cash runtime proof was not treated as completed, and packet 1's known failed status was not reclassified.
