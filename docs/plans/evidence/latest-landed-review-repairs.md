# Latest landed review repair record

The user supplied `openerp-latest-landed-review.zip`, reviewing `6209a764` through
`0eaad640`. Its archive checksums were verified. Findings are design/source
evidence, not application-runtime observations. The user authorized existing
checks only; no tests or fixtures are added by this repair pass.

| Finding | Current repair state | Verification boundary |
| --- | --- | --- |
| LR-01: frozen installation | Fixed in `893e33f`; CI also selects PostgreSQL 17 explicitly to match local development and recovery. | Frozen install passed locally. Existing E2E suite passed all 23 cases on local PostgreSQL/workerd. Updated hosted workflow has not been observed. |
| LR-02: VAT arrays decoded as objects | Control bindings and coverage decode through their exact array schemas. Invalid JSON-key casts in the same owner's SQL reads are also corrected. | Changed-file full gate and existing E2E pass. The suite does not exercise qualified actual-VAT capture. |
| LR-03: owner approval digest | Source repaired: the stored `digest` seals the approval body; generated `review_digest` has a foreign key to the exact review digest. Execution and usability compare `reviewDigest`. Forward migration `0019-owner-approval-digests.sql` preserves the earlier migration and body-hash constraint. | Full changed-file gate and existing E2E pass, including fresh migration/rerun. The suite does not exercise this owner-specific approval flow. |
| LR-04: recurring component arrays | Source repaired: materialization and agreement reads decode the retained template contract and use its exact component array. | Full changed-file gate and existing E2E pass. No successive recurring-invoice issue journey is covered by that suite. |
| LR-05: adjacent recurrence intervals | Source repaired: service intervals are half-open, adjacency is permitted, and empty/reversed intervals refuse explicitly. | Full changed-file gate and existing E2E pass; the selected interval policy below is source-verified, not an observed recurring-issue journey. |
| LR-06: duplicated VAT control components | Pending. | Physical GL identity and fact relationships must not multiply amounts. |
| LR-07: source versus deductible VAT | Pending. | Retain the recognition owner's source tax and deduction decision separately. |
| LR-08: negative integral floor | VAT now reuses the purchasing owner's sign-aware `roundRational`. | Changed-file full gate and existing E2E pass; no dedicated VAT-rounding regression case is added. |
| LR-09: owner-paid payable residual | Source repaired: live invoices and fixed-cutoff register reports share the owner-discharge summary, include its amount and version, and validate its payable posting. Owner operations no longer subtract it locally a second time and refuse exported-payment conflicts. Register lines retain explicit owner-discharge provenance. | Full changed-file gate and existing E2E pass. The suite does not exercise the owner-discharge/ordinary-settlement competition or the affected report query. |
| LR-10: zero-tax credit lines | Source repaired: zero tax retains its semantic correction and a null posting-line reference; only nonzero VAT lines are emitted. Forward migration `0020-zero-tax-credit-lines.sql` checks that correspondence and retains nonnull FKs. The correction writer also supplies the `creditId` required by its existing body constraint. | Full changed-file gate and existing E2E pass, including migration/rerun. The suite does not issue this small customer credit. Same-original-period qualification and missing renderer remain explicit limits. |
| LR-11: fulfillment reverification | Pending. | Preserve command replay and append new evidence observations explicitly. |
| LR-12: stale progress/parity claims | Pending. | Source presence, integration, qualification and runtime evidence remain distinct. |

The CI repair also corrected the previously unapplicable `0015-next-04.sql`
JSON-key cast and broke the invoice-draft/recurring-invoice schema import cycle
by moving occurrence identity to its domain owner. A fresh database and Worker
then started successfully. The existing suite writes its source/migration/lock
manifest, JSON results, JUnit results and runtime logs to `test-results/e2e/`;
the next run replaces those artifacts.

The existing recurrence compiler is a bounded arrears profile: service starts at
the preceding cycle boundary (the anchor for the first selected cycle) and ends
at the cycle date, exclusively. A cycle on the anchor itself has no service
duration and now refuses with `InvalidServiceInterval`; choose a first cycle
after the anchor for this profile. Advance billing and an initial point charge
need a separately reviewed policy. This repair does not infer either. Issuance
uses the same overlap check, while schedule amendments retain their stricter
frozen-history comparison. Existing zero-length coverage refuses further
billing rather than silently disappearing from capacity checks.

Reproduce current gates with `bun install --frozen-lockfile`,
`bun run check:changed:full <base-ref>` and `bun run test:e2e`. Core E2E success
does not close the unexercised financial feature paths in the table.
