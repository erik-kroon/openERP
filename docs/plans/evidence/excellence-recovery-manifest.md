# Excellence recovery manifest qualification

## Retained failure

[Main CI run 37138469537](https://github.com/erik-kroon/openERP/actions/runs/37138469537) at revision `09cb6b68a010698e41bfd7fcd66b1f02f8d08d67` passed validation and all 357 native tests. The full assurance foundation passed. The separate excellence recovery case failed at `recovery.recovery.test.ts:474` because a historical assertion expected 55 migration files while the current captured release contained 67.

The later missing `excellence-recovery.json` error followed the failed assertion. It does not identify a separate restore defect. The recovery case did not reach its strict qualification probe after this assertion.

Downloaded artifacts remain under `/tmp/native-ci-main-37138469537/`. The authentic failure is in the excellence `recovery.log` and `recovery.json` reports.

## Failure obligations before the correction

- Adding a reviewed migration must qualify against the complete release without changing a historical count constant.
- An omitted, extra, renamed, or changed restored migration receipt must fail exact release comparison.
- The strict schema inventory and JSON closure probe must still execute and report its literal expected result.
- Database, approval, command receipt, original bytes, missing-original refusal, corrupt-original refusal, and retired deployment login checks must remain intact.
- The retained release artifact must include every current migration with path, byte length, and SHA-256.

## Intended correction

Compare the restored database's sorted migration receipt names and SHA-256 values with the captured release's exact migration names and SHA-256 values. Preserve the existing strict qualification probe. This removes the stale count and strengthens the earlier observation into an independently retained database check.

## Verification status

The correction passed fast, full, and current primary strict lint. The exact excellence recovery case passed 1/1 in 15.78 seconds with unchanged timeout settings. Source integrity stayed stable at `3c703ee6439d96b4479b08be2698c9ae5b8651c69914775699facd70c6c1b5b1`. Exact worktree process inspection found no survivors.

The strict probe returned exactly `{ "evaluationRows": "1", "schemaInventory": "matched", "jsonClosure": "matched" }`. Database and command receipt recovery, retained original bytes, missing and corrupt original refusals, and the retired deployment login checks passed. The retained summary and migration list are [excellence-recovery-manifest.json](excellence-recovery-manifest.json).

Repeat the case with `OPENERP_E2E_ARTIFACTS=test-results/excellence-recovery-manifest EXCELLENCE_JSON_REPORT=test-results/excellence-recovery-manifest/results.json EXCELLENCE_JUNIT_REPORT=test-results/excellence-recovery-manifest/junit.xml bun run test:e2e --config verification/assurance/excellence/recovery.config.ts`.

Complete artifacts remain under `test-results/excellence-recovery-manifest/`. Gate receipts are `/tmp/excellence-recovery-fast2.log`, `/tmp/excellence-recovery-full.log`, and `/tmp/excellence-recovery-primary.log`. The runtime receipt is `/tmp/excellence-recovery-manifest.log`. This local case verifies the corrected recovery path. The complete remote excellence run still needs confirmation after integration.
