# Baseline proof-tool rereview

## Verdict

The repaired proof tools resolve the five original tool defects. The explicit manifest is enforced before selected source bytes are read. Credential-like paths are refused before patching or copying. Target dirt and untracked collisions are refused before mutation. Attempt selection and artifact hashes are bound to an immutable selection receipt. Private modes are enforced in code and present on the retained raw artifacts. The historical 1,985-path proof remains unchanged and correctly discloses that `apps/api/.dev.vars.five` was historically read and hashed.

The nine synthetic cases are credible actual CLI observations, not merely prose claims. `exercise-tools.py` invokes the three tools as subprocesses, checks all exit statuses, asserts exact tracked and untracked bytes, checks excluded and collision bytes, asserts absent refusal outputs, verifies modes, and writes the result only after every assertion passes. `synthetic-cli-proof-v2.json` records 26 subprocess executions, including 18 proof-tool calls, with the expected zero and refusal exits.

One material provenance issue remains. The v2 synthetic receipt is not hash-bound to the current tool digests or to the failure-contract bytes. The current script digests and synthetic receipt coexist, but no retained receipt proves that this exact tool set produced `synthetic-cli-proof-v2.json`. Two older passed synthetic receipts also remain under authoritative-looking names without being listed as superseded. The tool behavior is independently supported by source inspection, but the synthetic execution chain is not cryptographically closed.

## Original findings

### Resolved: credential admission

`proof_tools.py::load_manifest` validates every tracked and untracked pathname through `validate_path` before `capture.py` or `source-proof.py` resolves the source root, computes a patch, inventories selected files, or creates an output directory. `credential_path` refuses `.env*`, `.dev.vars*`, private key formats, key/token/password configuration names, and secret or credential components. The source reader separately refuses source symlinks.

The synthetic exercise checks `.dev.vars.fixture`, `.env.local`, `runtime.key`, `secrets.json`, and `private-key.pem` through both capture and source-proof CLIs. Every refusal exits 2. The fixture sentinel is absent from stdout and stderr. Static ordering confirms the named credential bytes are not read before refusal. The successful capture restricts `git diff --binary` to the admitted literal tracked path, and the fixture asserts that neither the credential pathname nor sentinel bytes enter the patch.

The future reviewed manifest contains 1,959 tracked paths and 25 untracked paths. It excludes `apps/api/.dev.vars.five` while retaining legitimate source names `apps/api/src/adapters/json-keys.ts` and `packages/ui/src/theme/tokens.stylex.ts`.

### Resolved: target collision and overwrite

`capture.py:18` requires a clean target with all untracked paths included. Lines 20 and 50 also refuse selected untracked destination collisions before patch application and before untracked copy. `write_bytes` uses `O_EXCL`, so output and copied untracked files cannot silently overwrite an existing path.

The collision fixture records capture exit 2, then asserts the prior target untracked bytes remain `prior target bytes\n`, the tracked target remains `old\n`, and no capture output directory exists.

### Resolved: attempt and receipt binding

`capture.py` writes `acceptedAttempt` and every selected artifact digest to a read-only selection receipt. `verify-capture.py` first validates the caller-pinned selection SHA-256, then refuses an attempt that differs from `acceptedAttempt`, then validates every selected artifact hash before reading the attempt inventories.

The synthetic receipt records attempt 2 accepted, attempt 1 refused with exit 2 against the same selection, and a modified selection refused with exit 2 before output creation.

The historical v2 selection is read-only mode 0400. Its SHA-256 is `8958087488d438a274b7718256c028c064b1c50e37a8a1845f17febd524df23a`, matching the separate pinned hash file. All 30 artifact digests named by that selection match the retained attempt-1 files.

### Resolved: private creation and raw diagnostics

`proof_tools.py` installs umask 077, creates proof directories at 0700, writes files with `O_EXCL` at 0600, and changes immutable receipts to 0400. The synthetic exercise inspects every generated output path and asserts those modes.

Current retained modes also match the report. The capture, attempt, tool-repair, stable runtime, and history directories are 0700. Historical selection and its pinned hash are 0400. The synthetic v2 receipt, raw JUnit files, and runtime files sampled in this review are 0600.

### Resolved: historical script and artifact identity

The three archived pre-repair scripts match the original `proof-script-sha256.json` exactly:

- `capture.py`: `53d2c715997e7141a1837df4ea1aa550cea7b16a7af73ddff7eb6078529d158f`.
- `source-proof.py`: `f6f58c304048bbc056386c5d96cf44e401392fcf5f292be9e890eec81049275b`.
- `verify-capture.py`: `e6d78a2fe7019d6b55002d59781f5ff626a4dfcd152b401cc3ab0368316a5f03`.

The current five tool and exercise-script digests match `proof-script-sha256.v2.json`. Every file named by the old runtime `artifact-sha256.json` still matches its historical digest. Permission changes did not alter those bytes.

`historical-normalized-verification.v2.json` is bound to historical attempt 1 and the pinned v2 selection. It reports stable inputs, matching target bytes, normalized Git modes, and saved untracked copies. It correctly records `historicallyIncludedCredentialPaths=["apps/api/.dev.vars.five"]` and `credentialExclusionProven=false`. The repair does not rewrite the historical capture limitation or change the failed runtime verdict.

### Resolved: canonical trail gap

The root canonical `decisions.tsv` now appends the failed runtime disposition, superseding isolation evidence, non-authoritative status of the manually adapted receipt, permission correction, integration correction, JUnit relocation, accepted proof-tool findings, cash artifact correction, integrated cash repair, and proof-tool repair. Row 19 points to the repair report and keeps independent rereview open pending this report.

## Remaining material findings

### Medium: the synthetic execution receipt is not bound to the tool version it claims to exercise

Location: `/Users/admin/.codex/worktrees/whole-year-baseline/openERP/test-results/stable-baseline-capture/tool-repair/exercise-tools.py:93` and `synthetic-cli-proof-v2.json`.

Failure: the receipt stores command names, arguments, and exit codes, but not the SHA-256 of `capture.py`, `source-proof.py`, `verify-capture.py`, `proof_tools.py`, `exercise-tools.py`, or `cli-failure-expectations.json`. It also does not retain hashes of each command's stdout and stderr. `proof-script-sha256.v2.json` proves current bytes, but no receipt links those bytes to this execution. A later script replacement or hand-edited receipt cannot be distinguished from the claimed run using retained artifacts alone.

Remedy: have `exercise-tools.py` hash the four exercised tools, itself, and the failure contract before the first subprocess; include those digests and per-command stdout/stderr digests in the exclusively created result. Add the synthetic receipt's digest to `proof-provenance.v2.json` or a superseding provenance receipt.

### Medium: two superseded passed synthetic receipts remain ambiguous

Location: `tool-repair/synthetic-cli-proof.json`, `tool-repair/synthetic-cli-proof-final.json`, and `tool-repair/proof-provenance.v2.json`.

Failure: the bare and `final` receipts each report the same nine passed case labels from 18 commands. V2 reports 26 commands and is the report's intended authority. `proof-provenance.v2.json` names superseded historical selections, normalized verification, and manifest receipts, but does not name the two earlier synthetic receipts as superseded. The filename `synthetic-cli-proof-final.json` can lead a reviewer to select weaker evidence.

Remedy: preserve the older bytes, but list both receipts under `supersededRepairReceipts` with a reason and make the v2 receipt's digest the sole authoritative synthetic execution pointer.

### Low: the CLI receipt proves assertions indirectly

Location: `tool-repair/synthetic-cli-proof-v2.json`.

Failure: the retained temporary repositories and raw command streams are intentionally gone. Exact byte, absence, collision, and mode results are represented by case labels and by the fact that `exercise-tools.py` reached its exclusive result write. This is repeatable and credible, but a reviewer cannot independently recompute those observations from the receipt alone.

Remedy: the digest binding above is sufficient for this synthetic tool proof. Retaining disposable repositories is unnecessary if the execution receipt binds the script and records hashes of observed values and command streams.

## No-comments review

Scoped files reviewed: `capture.py`, `source-proof.py`, `verify-capture.py`, `proof_tools.py`, `tool-repair/exercise-tools.py`, the nine-case contract, v2 synthetic and historical receipts, provenance receipts, sanitized v2 summary, repair report, original review, and root canonical decision trail.

Deletion candidates: zero. The repaired Python files contain no comments, narrating banners, lint suppressions, `TODO`, `FIXME`, `HACK`, or workaround sermons.

Exact `MUST KILL` target:

- `exercise-tools.py` result assembly at lines 93 through 97: close the tool-version provenance gap by serializing the exercised tool and contract digests plus command-stream digests, then bind that receipt from the authoritative provenance map.

Justified exceptions: none were needed because the repaired scripts contain no comments. No application code was reviewed or changed.

The no-comments workflow requested a separate Comment Sicko spawn. The host refused the spawn because the collaboration thread limit was full. This rereview therefore includes a direct Comment Sicko pass by the assigned independent reviewer rather than a second nested reviewer.

## Review limits

No project checks, tool exercises, database access, provider access, credentials, company data, process changes, product edits, or artifact edits were performed. Read-only digest, mode, JSON, and source inspections were used. Only this rereview report was written.
