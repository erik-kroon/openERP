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
| LR-06: duplicated VAT control components | Source repaired: purchase facts resolve their own journal ordinals from the retained purchase journal or ordered credit releases. Reconciliation counts each physical voucher/line once and blocks conflicting representations or per-line amount/date disagreement. | Full changed-file gate and existing E2E pass. No qualified multiline VAT capture is exercised by that suite. |
| LR-07: source versus deductible VAT | Source repaired for the selected exact-rate profile: capture retains signed source tax separately, rate checking uses source tax, and the retained deductible component is published without recalculating the deduction. A zero deduction needs no monetary VAT line. Earlier sealed captures remain readable. | Full changed-file gate and existing E2E pass; partial/zero deduction and signed-credit feature journeys remain unobserved. Source tax outside the selected exact-rate policy still refuses. |
| LR-08: negative integral floor | VAT now reuses the purchasing owner's sign-aware `roundRational`. | Changed-file full gate and existing E2E pass; no dedicated VAT-rounding regression case is added. |
| LR-09: owner-paid payable residual | Source repaired: live invoices and fixed-cutoff register reports share the owner-discharge summary, include its amount and version, and validate its payable posting. Owner operations no longer subtract it locally a second time and refuse exported-payment conflicts. Register lines retain explicit owner-discharge provenance. | Full changed-file gate and existing E2E pass. The suite does not exercise the owner-discharge/ordinary-settlement competition or the affected report query. |
| LR-10: zero-tax credit lines | Source repaired: zero tax retains its semantic correction and a null posting-line reference; only nonzero VAT lines are emitted. Forward migration `0020-zero-tax-credit-lines.sql` checks that correspondence and retains nonnull FKs. The correction writer also supplies the `creditId` required by its existing body constraint. | Full changed-file gate and existing E2E pass, including migration/rerun. The suite does not issue this small customer credit. Same-original-period qualification and missing renderer remain explicit limits. |
| LR-11: fulfillment reverification | Source repaired: an explicit operator-only reverification command checks the obligation revision and prior observation digest, rereads authoritative owner evidence, and appends a numbered observation with its evidence digest. Same-key replay retains its original result. Effective outcome reads reject superseded, wrong-revision or wrong-reference observations. The deadline write-access query now actually checks required insert privileges. | Full product lint/types and existing E2E pass, including migration `0021`. The suite does not exercise a changing provider outcome; unknown environment evidence still remains pending. |
| LR-12: stale progress/parity claims | Source repaired: current packet rows distinguish NEXT-04/22/29 integration from feature proof and NEXT-16/17 work in progress. The reference ledger classifies coverage/design advantages, never plan ownership as verified parity. | Documentation reconciled to the integration commits and existing-suite artifacts; broader packet readiness is not inferred. |

The CI repair also corrected the previously unapplicable `0015-next-04.sql`
JSON-key cast and broke the invoice-draft/recurring-invoice schema import cycle
by moving occurrence identity to its domain owner. A fresh database and Worker
then started successfully. The existing suite writes its source/migration/lock
manifest, JSON results, JUnit results and runtime logs to `test-results/e2e/`;
the next run replaces those artifacts.

The VAT pass also corrected the filing-unit conversion: with a scale-2 book,
filing scale 0 divides minor units by 100, while filing scale 2 retains minor
units. The factor is `10^(currencyScale - filingUnitScale)`; finer-than-book
filing units refuse. Owner-purchase and customer-credit tax producers, exact
registered-period qualification and other source-tax policies remain explicit
integration/qualification boundaries, not implied by these repairs.

The existing recurrence compiler is a bounded arrears profile: service starts at
the preceding cycle boundary (the anchor for the first selected cycle) and ends
at the cycle date, exclusively. A cycle on the anchor itself has no service
duration and now refuses with `InvalidServiceInterval`; choose a first cycle
after the anchor for this profile. Advance billing and an initial point charge
need a separately reviewed policy. This repair does not infer either. Issuance
uses the same overlap check, while schedule amendments retain their stricter
frozen-history comparison. Existing zero-length coverage refuses further
billing rather than silently disappearing from capacity checks.

Fulfillment callers use
`POST /v1/entities/:entityId/books/:bookId/deadlines/:id/fulfillments/reverify`
with an idempotency header and the retained `reference`,
`expectedObligationRevision` and `expectedFulfillmentDigest`. A changed latest
observation refuses as stale instead of silently replacing the caller's reviewed
state. Ordinary linking recovers the latest retained observation; it is not a
fresh verification. Neither path treats a caller's environment string as owner
attestation. Prior immutable observations and command receipts remain intact.

Reproduce current gates with `bun install --frozen-lockfile`,
`bun run check:changed:full <base-ref>` and `bun run test:e2e`. Core E2E success
does not close the unexercised financial feature paths in the table.
