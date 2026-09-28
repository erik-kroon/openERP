# NEXT-23 review repair and HTTP evidence

Target: isolated `review/next23-financial-close`, baseline `fc47b27`.
Status: implemented in the isolated worktree; fast/full static gates and 27 real
Worker/HTTP/restricted-PostgreSQL E2E cases passed on 2026-09-28. Not a company,
statutory or provider qualification. Integration and commit remain with the caller.

## Observable contract (recorded before implementation)

1. Real HTTP preparation/advance must decode retained statement pages and return a sealed proposal.
2. A nonzero close admits only its owned transfer through internal approval and execution, and observes that transfer in its final conservation check.
3. Profit excludes owned transfers; prior effective transfers are subtracted exactly once. `60000 -> 50000` after correction produces `-10000`.
4. An opening consists of raw per-account balance-sheet balances after transfer, sums to zero, and is selected exactly once by the next year's report. Presentation rows and nominal balances cannot become opening accounts.
5. The exact tax bridge must have an executed effect and receipt, its target must be recognized, and the financial basis must include the tax posting.
6. Unknown applicability, missing current owned controls, unresolved selected adjustments, and contradictory activity block close. Client declarations cannot establish control completeness.
7. Approval binds the exact proposal, expires, requires an independent current operator, and reviewer authority is protected before book admission. Revocation blocks new execution but not committed replay.
8. Mutations acquire the writer barrier before replay and mutable reads. Concurrent identical commands return one result; changed identities conflict.
9. Only a full fiscal-year population can close. Stale ledger/account/period/control/tax inputs refuse before effects.
10. Reopen requires a reviewed impact plan and approval. Unsupported downstream consumption returns a durable typed refusal with exact dependencies. Old records remain immutable.
11. Successful reopen reports open/reopened and invalidates the old current opening basis; revised close appends a replacement projection.
12. Failure between posting and certificate/opening persistence rolls back posting, counters, approval use and locks together.

## Implemented ownership shape

```text
HTTP -> authority admission (requester + referenced reviewer)
     -> book writer barrier -> exact command replay
     -> current owned basis and controls -> immutable proposal/approval
     -> transaction-passing journal -> raw balance conservation
     -> transfer + certificate + opening + locks + receipt -> commit
```

Synthetic fixtures are declared engineering data, not company qualification.
Before source edits, the HTTP advance regression returned `500 InternalError`
after successful preparation (run 2026-09-28 11:47 CEST). Its snapshot was seeded
only to isolate that failure: the real snapshot producer first exposed malformed
SQL array binding for `result_transfer_v1`. The final proof uses HTTP capture,
company-fact review, role bindings, NEXT-22 tax preparation/approval/execution,
owned closing inventories, close and reopen. No report, bridge, tax effect,
close proposal, approval, certificate or opening is seeded in the passing journey.

The next E2E scenarios must fail if: tax is unexecuted; controls are unknown or
contradicted; a selected adjustment lacks its exact receipt; capture is interim;
reviewer is revoked; requester uses the wrong book; concurrent replay duplicates
an effect; a post-transfer persistence failure leaks counters; reopen lacks
approval; a later consumer is omitted; or reclose/opening repeats prior profit.
The positive vector uses a declared synthetic 1/5 tax rate: revenue 75000, tax
15000, profit 60000; correction expense 12500, revised tax 12500, profit 50000.
Tax proposals and effects must use the existing NEXT-22 HTTP owner, not seeded
bridges/effects. Fixture-only installation of the declared rule release is allowed.
Only forward migration `0030-next-23-review.sql` is reserved for this repair.
NEXT-05/07/24/37 are separate owners; any consumed-port changes will be listed here.

## Review findings resolved

| Original finding | Repair and observation |
| --- | --- |
| 1. Advance page decoding | Decode the SQL JSON array directly. Real retained statement rows advance successfully. |
| 2. Transfer approval admission | Internal approval receives the financial-close owner and admits its transfer purpose; ordinary callers gain no new purpose. |
| 3. Self-staling transfer | Insert its ownership record before the same-transaction conservation recheck. First nonzero close commits. |
| 4. Double-subtracted prior transfer | Derive full ordinary year profit from raw ledger entries, excluding exactly owned transfers; apply `D=P-F` once. Reclose observes `P=50000`, `F=60000`, `D=-10000`. |
| 5. Presentation rows as openings | Seal raw account balances plus the exact transfer; verify final BS and nominal conservation. Opening carries a source boundary; next-year reports select its version once. Old opening stays byte-identical. |
| 6. Unexecuted tax / pretax profit | Require the exact executed effect, consumed group receipt, recognized target and current tax-owner basis. The final raw basis includes actual tax. |
| 7. Missing controls / adjustments | Consume each period's complete inventory/readiness result and bind its current digest. Unknown/unavailable controls block. Selected adjustment evidence must match distinct executed, unreversed, year-scoped receipt IDs. |
| 8. Revoked reviewer | Lock referenced reviewer admission/membership before the writer barrier; validate after replay. Revocation refuses new execution, while committed replay survives it. Author/preparer cannot self-review. |
| 9. Shared mutation lock | Use the book writer barrier before replay and mutable reads. Four concurrent executions return one identical certificate. |
| 10. Interim year | Require full fiscal-year snapshot intervals and continuous non-overlapping period coverage. An executed interim zero-tax bridge cannot close the year. |
| 11. Unapproved reopen | Preparation returns an immutable impact proposal. Independent approval and execution are separate HTTP operations. Missing approval refuses. Technical period reopening cannot bypass an active financial certificate. |
| 12. Lost refusal evidence | Execution commits a typed `refused` event and receipt with exact consumers, without unlocking. The journey reads the saved event back from PostgreSQL. |
| 13. Wrong reopened status | Use certificate identities and ignore preparations preceding the latest successful reopen. Status becomes `open` / `reopened=true`. |

## Wire and exported operation changes

- `PrepareYearClose.adjustmentReceiptIds` pairs with `proposedAdjustmentRefs`.
  An evidence reference alone is not an execution receipt. `otherFamilies` is
  retained supplemental evidence, not the applicability/completeness authority.
- New preparations retain `currentBasisDigest`, `taxEffectId`, `taxReceiptId`;
  new openings retain `sourceBoundary`. Historical records still decode. An old
  proposal without the current basis must be recaptured, and a pre-repair opening
  remains readable but cannot silently become a reviewed next-year basis.
- `POST .../closing/financial-years/:fiscalYearId/reopen` now returns
  `FinancialReopenProposal` and changes no period state.
- New `approveYearReopen` and `executeYearReopen` exports in
  `apps/api/src/application/closing/financial-reopen.ts` own
  `POST .../reopen-proposals/:id/approvals` and `POST .../reopen-proposals/:id/execute`.
  Execution requires `version`, `digest`, `approvalId` and returns an immutable
  `FinancialReopenEvent` with `status: executed | refused`.
- `FinancialCloseHistory.reopenings` exposes successful and refused events through
  the existing HTTP/read-only MCP history capability. No MCP mutation was added.
- Statement snapshots retain optional `fiscalYtdProfitMinor`; opening basis adds
  `financial_close` with the selected opening ID and reviewed status.
- Internal ports: `captureFinancialBasis`, `withFinancialApproval`,
  `reviewerIsCurrent`, existing closing `readBasis`, and tax-owner
  `executedBridgeIsCurrent`. Every call receives the owning transaction.

## Cross-owner prerequisites discovered by the real journey

These are narrow consumed-port repairs, not replacement owners:

- `application/company-profiles.ts`: the runtime should select rule releases,
  not require permission to insert them. Fact/review/binding and impact bodies
  use the ordinary canonical digest; they do not have the numeric-version
  envelope required by `versionedDigest`.
- `application/report-statements.ts`, `db/report-statements.ts`: fix SQL array
  binding, page-array decoding and mapping digest; select financial openings;
  include financial reopen events in live status. New snapshots retain full YTD
  profit so later tax calculation does not mistake `P-F` for `P`.
- `application/tax/corporate.ts`, `db/tax/corporate.ts`: fix retained-row decoding,
  unversioned snapshot/overlay/bridge/effect hashes, account-list SQL binding,
  explicit bridge creation time, and P&L tax-component selection (exclude the
  liability leg). Read an immutable no-effect plan without an unnecessary SQL
  row-lock privilege. Expose the existing tax revalidation for an executed target.
- Migration `0030-next-23-review.sql` alone adds the missing corporate-tax family
  and role values, compares timestamps as timestamps, binds bridge statement
  references through the retained overlay, and grants only `UPDATE(id)` on the
  immutable bridge to support its existing row lock. The immutable trigger still
  rejects changes. It also adds reopen proposals/approvals and unique outcome/use
  indexes. No existing migration was edited.
- `application/posting.ts`: admit the transfer during internal approval.
  `db/posting-admission.ts`: protect owned transfers from generic corrections.
  `db/identity.ts`: trusted optional `beforeBook` hook for referenced-authority
  locks, after requester admission and before the book.
- `application/closing/proposals.ts`: expose its owned readiness port and prevent
  technical reopening from bypassing a financial certificate.
- NEXT-24 implementation is untouched. Reopen reads its actual
  `closeCertificateId` reference, alongside later openings/reports, affected tax
  declarations and complete-book exports. NEXT-05/07/37 implementation is untouched.
  The single additional union in `db/posting-admission.ts` needs preservation when
  integrating the other owners' changes to that shared file.

## Verification and repeatable artifacts

Completed on 2026-09-28:

```sh
bun install --frozen-lockfile
bun run check:changed
bun run check:changed:full
bun run test:e2e apps/api/tests/financial-close.e2e.test.ts \
  apps/api/tests/posting.e2e.test.ts apps/api/tests/admission.e2e.test.ts \
  apps/api/tests/mcp-authority.e2e.test.ts apps/api/tests/persistence.e2e.test.ts
```

Final run: **5 files / 27 cases passed**. The four financial-close cases cover
the actual financial journey, interim/adjustment/current-control/stale-ledger
refusals, and zero-delta finalization. The shared cases cover exact posting,
admission, MCP authority, protected persistence, rollback, migration rerun and
checksum refusal. The close journey injects a certificate CHECK failure after
posting and verifies unchanged financial counters/effects and eligible periods.

Artifacts relative to the isolated worktree:

- `test-results/e2e/financial-close-journey.json`: actual first/second certificates,
  opening versions, approved reopen, next-year statement and durable refusal.
- `test-results/e2e/financial-close-ledger.json`, `financial-close-zero.json`,
  `financial-close-refusals.json`: retained ledger/receipt observations.
- `test-results/e2e/results.json`, `manifest.json`, `source-integrity.json`,
  `migrations.log`: runner result, file-level source hashes and migration receipt.
- Baseline advance failure: archive
  `test-results/e2e-history/2026-09-28T10-09-06.539Z-51a78d79/`.

Final source inventory SHA-256:
`0a4757d1dbae25124395846a41cba85bd6844a3af8aa6da2e8f20248cfbcfbb8`.
The final source-integrity artifact reports `stable`, no changed paths, at
`2026-09-28T10:58:16.638Z`. Only this documentation was updated afterward.

## Independent-review P1: cumulative opening source protection

Counterexample recorded before source changes: leave zero-balance FY2025 open,
close FY2026, then execute a FY2025 bank debit 1000 / equity credit 1000. The new
three-year HTTP regression observed the defect at 12:53 CEST: execution returned
HTTP 200 with voucher sequence 4, rather than the expected 409 refusal. The
existing opening remained at its earlier source boundary.

Repair:

- `db/posting-admission.ts` exports `readActiveCloseCoveringDate`. An active
  certificate covers all posting dates through its fiscal-year end, not only
  dates inside its own year. `application/posting-admission.ts` applies this
  fence in the existing internal posting admission path. Successful approved
  reopen releases that certificate; refused reopen does not. Existing exact
  replay occurs before admission, and the close's own transfer is posted before
  its certificate is inserted in the same transaction.
- `db/report-statements.ts` exports `readOpeningSourceDrift`.
  `application/report-statements.ts` refuses a selected financial opening when
  any later-sequenced voucher predates the reporting year's start. It does not
  recompute or rewrite the immutable opening.
- The regression proves normal backdated execution refuses without financial
  changes, future-year posting still commits, approved reopen permits the
  earlier-year correction, and stale opening selection independently refuses.
  The last check is explicitly maintenance-only: after the approved correction,
  the disposable fixture removes its successful reopen event to model an
  out-of-band writer against the old active certificate. This is not an API
  capability. The authorized reopen receipt is retained in the artifact and
  the opening is read back byte-identical after refusal.

Additional artifacts: `test-results/e2e/financial-close-prior-year-boundary.json`
and `test-results/e2e/financial-close-prior-year-fence.json`. The first separates
normal API outcomes from the maintenance-only fixture. The full 27-case command
above and both required static gates passed after this repair. No additional
migration or existing migration edit was needed. Integration must preserve the
new financial-close fence and the prior correction-protection union alongside
main's NEXT-07/37 posting-admission changes.

Limit: source-drift detection assumes the normal committed voucher sequence
contract. It is not a defense against maintenance rewriting voucher sequences
or immutable history. No unrelated future year is locked by this repair.

## Scope and reading order

The exercised profile is native `synthetic-core-v1`, with declared synthetic
jurisdiction/rate/evidence. Required families without a released complete control
provider remain explicit blockers; no company facts or statutory support are
invented. Reopening a consumed downstream basis returns a durable refusal; this
slice implements no automatic cascade or external amendment/filing. Enumeration
of annual-report/tax/export consumers is source-reviewed; the exercised downstream
refusal is a real next-year statement snapshot.

Reviewer order:

1. `apps/api/tests/financial-close.e2e.test.ts` and its `support/financial-close.ts`.
2. `application/closing/financial-basis.ts`, then `financial-close.ts`.
3. `financial-authority.ts`, `financial-reopen.ts`, and their scoped DB queries.
4. `0030-next-23-review.sql`, the HTTP contract/routes, and statement opening selection.
5. The small company-profile, posting and tax prerequisite diffs listed above.
