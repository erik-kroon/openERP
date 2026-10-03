# Daily-work integration receipts

Delivery source: `3ed96bd1` plus documentation-only delivery updates. Runtime source hashes and selected/unselected cases are retained in `source-integrity.json`, `manifest.json` and `results.json`. The final focused E2E run passed **28**, skipped/unselected **18**, across five files. `cash-templates-runtime.log` retains the command and result. Fixtures are synthetic and local.

Retained gates include frozen installation, web build, earlier full changed-file lint/types and domain-leaf integration, plus the latest fast changed-file gate. Earlier gate logs bind to their then-current source, not automatically to all later corrections.

## Reproduce

```sh
OPENERP_E2E_ARTIFACTS=test-results/final-cash-templates bun run test:e2e apps/api/tests/cash-basis.e2e.test.ts apps/api/tests/cash-forecast.e2e.test.ts apps/api/tests/sales-register-identity.e2e.test.ts apps/api/tests/collection-reminders.e2e.test.ts apps/api/tests/invoice-templates.e2e.test.ts -t 'P10|P11|existing sales register|collections caller|invoice templates copy exact|template replacement requires|unresolved template treatment|template article selections'
```

## Pending at immediate as-is delivery

The owner requested no further delay before direct-main delivery. The final full changed-file gate, tests-wide type check, complete integrated recurring suite and final actual backup/restore remain pending. P10 performance qualification, P11 expanded performance qualification, native 200% zoom and walkthroughs remain open. P12 overview and P13 workspace search are planned, not implemented. Reminder transport remains default-disabled and loopback-only; no live provider delivery, production migration or deployment occurred.
