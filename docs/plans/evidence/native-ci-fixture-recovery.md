# Native CI fixture recovery

## Retained failure vectors

The native main run on 2026-10-03 retained 21 failures across seven files. Five supplier-extraction fixture failures are tracked separately. These six files account for the remaining 16 failures:

- Company activation fixture: seven tests collide with the supplier-settlement fixture's global `(ZZ, posting_eligibility, 1)` release identity. Each fixture needs a distinct synthetic jurisdiction; multiple overlapping versions would create an ambiguous release selection.
- MCP catalog and cash-flow report: two assertions mistake the read-only supplier settlement cancellation approval listing for an approval mutation. The catalog must expose that exact listing with read-only metadata and withhold approval and activation writes.
- Payment resolutions: five tests request execution on 2026-10-01 after the database's current UTC date has passed it. The fixture must derive a future date from the database clock while retaining all reservation, settlement, replacement and refusal expectations.
- Browser business date: the clock starts ticking on installation, so pausing at the same installed instant races against elapsed time. Pause at a later instant on the intentionally skewed date; retain server-derived date and periodic refresh assertions.
- Recovery constraints: the selector stage applies every current migration, then asserts only the historical 0051 CHECK changed. Bound the historical stage and its exact preservation assertions to 0051. Separately apply the complete current release before the populated evaluation and restore qualification, retaining exact inventory and data equality.

## First corrected run

The full changed-file gate and current primary Effect lint passed. The eight-file run on 2026-10-03 returned **44 passed / 3 failed**, not a complete pass. Company activation passed 7/7 after supplier settlement passed 20/20 in the same disposable database. Recovery passed 1/1, cash flow 7/7, extraction 5/5 and four payment resolution cases passed.

The remaining payment catalog assertion has the same read-only listing mismatch previously identified in MCP and cash flow. Before correcting it, the retained failure shows exactly `purchases_list_supplier_settlement_cancellation_approvals` where the test expects an empty approval-name list. The correction must assert this exact listing with read-only and non-destructive metadata while refusing every other matched approval or activation capability.

Business date timed out before login while waiting for the Email field; its retained page body is the company-route read error with a retry control. The shared API Worker reported three crashes/restarts, and the subsequent MCP case timed out. The skewed browser clock code was not reached. The retained structured Worker log contains only six deliberate rollback failures; the web log contains startup without a fatal native banner. macOS diagnostics report no workerd crash or OOM kill. Source inspection shows that Miniflare discards exit code and signal when emitting its restart warning. The crash cause therefore remains unknown. A diagnostic-only process receipt will distinguish unexpected exits before timeout from ordinary harness cleanup; neither case has corrected runtime proof yet.

Receipts: `/tmp/native-ci-fixture-full3.log`, `/tmp/native-ci-fixture-primary2.log`, `/tmp/native-ci-fixture-e2e.log`; artifacts under `test-results/native-ci-fixture-recovery/`, including results, source integrity, company activation, recovery and business-date failure records. Source integrity was stable: `bec73b0b0f93741cefd1848fec4731ac417834677713e28e682e6c97f5c3bcba`. The run took 216.51 seconds and returned exit 1. Exact process inspection after completion found no surviving worktree test or Worker processes.

## Diagnostic confirmation

The bounded three-file diagnostic run passed 7/7 on 2026-10-03 in 31.55 seconds. It exercised payment resolution, business date, and MCP with unchanged test budgets. Fast, full, and current primary Effect lint passed before execution. Source integrity stayed stable at `7fea2ab4ce02d1d2efac5e5264895271fc5b0ad581d59c24f61a14318e17b9d0`.

The process receipt captured four workerd processes. All four received SIGKILL during browser or global harness teardown after their work completed. The run reported no unexpected restart. The original restart cause remains unknown because this run did not reproduce it. The browser succeeded with its existing environment, so no environment correction was made. Its Worker log now remains available as `business-date-worker.json` even if Worker close fails.

The missing-original helper is checkpoint `15df0bb`. It returns null only for filesystem ENOENT and preserves other IO failures. The retained eight-file run exercised supplier extraction 5/5 with that helper.

Diagnostic receipts are `/tmp/native-ci-fixture-fast4.log`, `/tmp/native-ci-fixture-full4.log`, `/tmp/native-ci-fixture-primary4.log`, `/tmp/native-ci-fixture-diagnostic4.log`, and `/tmp/native-ci-workerd-process-diagnostic4.jsonl`. Runtime artifacts remain under `test-results/native-ci-fixture-diagnostic4/`. Exact worktree process inspection found no survivors after execution.

## Ordinary combined confirmation

The complete eight-file cohort passed 47/47 without diagnostic preload on 2026-10-03. The process returned exit 0 in 103.98 seconds. Vitest reported 100.48 seconds. Source integrity stayed stable at the same digest as the diagnostic run. No unexpected restart warning appeared. Exact worktree process inspection found no survivors.

The supplier settlement and company activation fixtures passed in the same database. Recovery retained its historical 0051 checks, complete release migration, populated inventory, and restore proof. Payment retained reservation, settlement, replacement, and refusal checks while using the database clock. MCP retained the exact read-only cancellation approval listing and withheld approval mutations. Business date exercised clock skew and supplier history paging on the real browser.

Repeat the ordinary run from the repository root with `OPENERP_E2E_ARTIFACTS=test-results/native-ci-fixture-ordinary5 bun run test:e2e apps/api/tests/supplier-settlement.e2e.test.ts apps/api/tests/company-profile-admission.e2e.test.ts apps/api/tests/payment-resolutions.e2e.test.ts apps/api/tests/cash-flow-statement.e2e.test.ts apps/api/tests/supplier-extraction.e2e.test.ts apps/api/tests/business-date.e2e.test.ts apps/api/tests/mcp.e2e.test.ts apps/api/tests/recovery-constraint-validation.e2e.test.ts`.

The retained summary is [native-ci-fixture-recovery.json](native-ci-fixture-recovery.json). Complete runtime artifacts remain under `test-results/native-ci-fixture-ordinary5/`; the process log is `/tmp/native-ci-fixture-ordinary5.log`.

## Verification status

The corrected cohort is verified on the isolated prerequisite worktree. Integration onto current main requires the root's final checks. These corrections change test fixtures and expectations about fixture setup, without changing application authority, migration integrity or financial behavior.
