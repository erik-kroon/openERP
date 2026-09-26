# Sources and review boundary

Repository reads used the connected GitHub tool. No local clone, application run, database inspection or upstream full-suite audit was performed. The review compares the test-plan prose with selected current implementation paths and the existing test harness. External documentation supports specific test mechanisms, not company compliance.

Review source revision: `ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb`. The test-plan commit is `8bff9fadbcacf9d369758b967971469548834365`. Later parity-backlog requirements are outside this review.

## R00

**GitHub commit metadata**

Read scope: Test-plan commit metadata/diff; observed branch head separately pinned to ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb.

```text
https://github.com/erik-kroon/openERP/commit/8bff9fadbcacf9d369758b967971469548834365
```

## R01

**docs/plans/test-suite-pseudologic.md**

Read scope: Sections 0-10, full 746-line document via ranged reads.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/test-suite-pseudologic.md
```

## R02

**docs/plans/test-suite-design.md**

Read scope: Sections 1-10, 477-line document via ranged reads; Accounted survey treated as the plan author's observations, not an independent re-audit of all upstream repositories.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/test-suite-design.md
```

## R03

**AGENTS.md**

Read scope: Full file.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/AGENTS.md
```

## R04

**package.json**

Read scope: Full file.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/package.json
```

**vite.config.ts**

Read scope: Full file.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/vite.config.ts
```

## R05

**apps/api/tests/support/global-setup.ts**

Read scope: Full file.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/apps/api/tests/support/global-setup.ts
```

## R06

**apps/api/tests/support/fixtures.ts**

Read scope: Lines 1-210.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/apps/api/tests/support/fixtures.ts
```

## R07

**apps/api/tests/persistence.e2e.test.ts**

Read scope: Full file.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/apps/api/tests/persistence.e2e.test.ts
```

## R08

**apps/api/src/application/commerce/sales-orders.ts**

Read scope: Lines 1-230, including write context and transition guards.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/apps/api/src/application/commerce/sales-orders.ts
```

## R09

**apps/api/src/db/purchases/credits.ts**

Read scope: Lines 1-170, including prior credit line and conflict queries.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/apps/api/src/db/purchases/credits.ts
```

## R10

**apps/api/src/application/subledger/schedules.ts**

Read scope: Ranges 1-190, 700-900 and 1000-1430; amendment context, prefix/suffix logic and revision construction.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/apps/api/src/application/subledger/schedules.ts
```

## R11

**apps/api/src/application/subledger/asset-basis.ts**

Read scope: Lines 1-250, including consumed scan, capture and impairment basis.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/apps/api/src/application/subledger/asset-basis.ts
```

## R12

**apps/api/src/application/sie/historical-items.ts**

Read scope: Lines 1-250, including controls and admission.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/apps/api/src/application/sie/historical-items.ts
```

## R13

**docs/verification-strategy.md**

Read scope: Full file.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/verification-strategy.md
```

## R14

**apps/api/tests/README.md**

Read scope: Full file; some descriptions conflict with current persistence test and need reconciliation.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/apps/api/tests/README.md
```

## R15

**apps/api/tests/**

Read scope: Directory listing; not an independent recount of every executable test.

```text
https://github.com/erik-kroon/openERP/tree/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/apps/api/tests/
```

## R16

**apps/api/tests/mcp.e2e.test.ts**

Read scope: Full file.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/apps/api/tests/mcp.e2e.test.ts
```

## R17

**packages/contracts/src/sales-orders.ts**

Read scope: Full file returned for range 1-210.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/packages/contracts/src/sales-orders.ts
```

## R18

**apps/api/src/application/purchases/credit-basis.ts**

Read scope: Lines 1-250; acceptance profiles, conflict checks and beginning of line selection.

```text
https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/apps/api/src/application/purchases/credit-basis.ts
```

## W01

**PostgreSQL SET CONSTRAINTS**

Read scope: Deferred checks run at commit; SET CONSTRAINTS IMMEDIATE can force outstanding checks. Consult deployed PostgreSQL version during implementation..

```text
https://www.postgresql.org/docs/current/sql-set-constraints.html
```

## W02

**PostgreSQL system information functions**

Read scope: pg_blocking_pids and backend identities; proposed test harness is our design, not an executed recipe.

```text
https://www.postgresql.org/docs/current/functions-info.html
```

## W03

**Playwright library**

Read scope: Library browser control is distinct from selecting the Playwright Test runner.

```text
https://playwright.dev/docs/library
```

## W04

**Vitest browser mode**

Read scope: Documented Playwright provider; proposed full-app lane uses the library under the existing runner.

```text
https://vitest.dev/guide/browser/
```

## W05

**Vitest v4 fileParallelism**

Read scope: Runner configuration reference; current repository configuration was inspected directly.

```text
https://v4.vitest.dev/config/fileparallelism
```

## Limits

No blanket claim is made about all functions, grants, triggers or tests outside the inspected paths. Source-based discrepancy findings are not reproduced runtime bug reports. A desired invariant without observed enforcement remains a requirement to test. All replacement fixtures are proposals requiring current contract binding. Actual-company facts, statutory data and provider outcomes were not qualified.
