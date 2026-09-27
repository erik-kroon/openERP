# Latest landed review repair record

The user supplied `openerp-latest-landed-review.zip`, reviewing `6209a764` through
`0eaad640`. Its archive checksums were verified. Findings are design/source
evidence, not application-runtime observations. The user authorized existing
checks only; no tests or fixtures are added by this repair pass.

| Finding | Current repair state | Verification boundary |
| --- | --- | --- |
| LR-01: frozen installation | Fixed in `893e33f`; CI also selects PostgreSQL 17 explicitly to match local development and recovery. | Frozen install passed locally. Existing E2E suite passed all 23 cases on local PostgreSQL/workerd. Updated hosted workflow has not been observed. |
| LR-02: VAT arrays decoded as objects | Control bindings and coverage decode through their exact array schemas. Invalid JSON-key casts in the same owner's SQL reads are also corrected. | Changed-file full gate and existing E2E pass. The suite does not exercise qualified actual-VAT capture. |
| LR-03: owner approval digest | Pending. | Separate review binding from approval-body integrity. |
| LR-04: recurring component arrays | Pending. | Exact array must survive template, materialization, read and issue. |
| LR-05: adjacent recurrence intervals | Pending. | First-cycle and service-boundary policy must be consistent. |
| LR-06: duplicated VAT control components | Pending. | Physical GL identity and fact relationships must not multiply amounts. |
| LR-07: source versus deductible VAT | Pending. | Retain the recognition owner's source tax and deduction decision separately. |
| LR-08: negative integral floor | VAT now reuses the purchasing owner's sign-aware `roundRational`. | Changed-file full gate and existing E2E pass; no dedicated VAT-rounding regression case is added. |
| LR-09: owner-paid payable residual | Pending. | All shared capacity consumers must include the discharge exactly once. |
| LR-10: zero-tax credit lines | Pending. | Preserve semantic zero tax without emitting a zero journal line. |
| LR-11: fulfillment reverification | Pending. | Preserve command replay and append new evidence observations explicitly. |
| LR-12: stale progress/parity claims | Pending. | Source presence, integration, qualification and runtime evidence remain distinct. |

The CI repair also corrected the previously unapplicable `0015-next-04.sql`
JSON-key cast and broke the invoice-draft/recurring-invoice schema import cycle
by moving occurrence identity to its domain owner. A fresh database and Worker
then started successfully. The existing suite writes its source/migration/lock
manifest, JSON results, JUnit results and runtime logs to `test-results/e2e/`;
the next run replaces those artifacts.

Reproduce current gates with `bun install --frozen-lockfile`,
`bun run check:changed:full <base-ref>` and `bun run test:e2e`. Core E2E success
does not close the unexercised financial feature paths in the table.
