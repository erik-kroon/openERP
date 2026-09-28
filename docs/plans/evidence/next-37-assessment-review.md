# NEXT-37 rounding-bridge and assessment ownership

**Historical handoff for `c828603`.** The later [review repair](next-37-review-repair.md)
supersedes its implementation status and disproves the match-before-post ordering
hypothesis below. The new proof uses actual tax-owner import/match operations,
not the original seeded match, and completes new posting plus stale-plan renewal.

## Scope and status

NEXT-37 adds the HTTP surface for the already-implemented `@open-erp/domain/vat-assessment` leaf: a rounding bridge between the exact net of a saved actual VAT return and its assessed figure, and an authority assessment that either posts new or adopts an existing tax-account match. The work spans `packages/contracts/src/vat-assessment.ts`, `apps/api/migrations/0028-next-37.sql`, `apps/api/src/db/vat/assessment.ts`, `apps/api/src/application/vat/assessment.ts`, the capability and route wiring, and one focused E2E.

Status: the focused HTTP journey for the rounding bridge and the adopted-match path is observed and repeatable. The MCP journey is unobserved. The new-assessment posting mode is still refused, but no longer for a missing port: the port now exists and the remaining blocker is an ordering conflict between control-account admission and the match itself, described below.

## Observed defects and repairs

The first run of the focused E2E failed at `POST /vat/assessments/bridges` with HTTP 500 `InternalError`. The three defects below were each located by bisecting the application workflow with a temporary early return and by reading committed rows back from the E2E database, then removing the probe.

| Defect | Observed before repair | Repair |
| --- | --- | --- |
| `readBridgesForReturn` and `readBridge` selected `voucher_id` from `openerp.vat_rounding_bridges` | HTTP 500 `InternalError` on bridge preparation. Migration `0028-next-37.sql` does not define that column; execution references live in `openerp.vat_bridge_receipts`. The `42703` error surfaced through `databaseFailure` as `InternalError` | Dropped the stale select and the unused `BridgeRow.voucherId` field |
| Bridge execution recomputed the live prior effects over *all* bridges of the return, counting the executing bridge as its own predecessor | HTTP 409 `StaleDependency`. Committed rows gave `exact -125`, `reported -100`, prior `-25`, so `live = -125 − (−100) − (−25) = 0` against the sealed `bridgeDeltaMinor` of `-25` | Excluded `bridge.id` from the live prior set, so a sealed bridge is compared against the effects of *other* bridges only |
| Assessment execution re-verified that the adopted match was "unused by any other assessment" with a query that also matched the assessment being executed, whose `match_ref` is its own adopted reference | HTTP 409 `StaleDependency` on assessment execution, immediately after the bridge posted | `readAssessmentByMatch` takes an `excludingAssessmentId`; the execute path passes the current assessment, while the prepare path still refuses a match already used by any assessment |

The second and third defects are the same class: a re-verification query scoped to the return or the match also matched the row under evaluation, so a correctly sealed record could never satisfy its own guard.

## The tax-account match port

`apps/api/src/application/vat/tax-account.ts` owned `matchEvent`, whose whole body was a closure inside `withTaxBook`, so no caller could create a match inside a transaction it already owned. `recordTaxAccountMatch` is that body extracted as a transaction-passing entrypoint, following the same convention the posting owner already uses for `prepareJournalInTransaction`, `approveChangeInTransaction` and `executeChangeInTransaction`. `matchEvent` now delegates to it, so the public path is unchanged: it still enforces the previewed `expectedBasisDigest`. An in-transaction caller passes `null` and the sealed match records the basis digest actually used, because its selection was built from rows it wrote under the same lock.

`apps/api/src/application/posting.e2e.test.ts`, `persistence.e2e.test.ts` and `admission.e2e.test.ts` pass unchanged after the extraction (23 tests with the focused NEXT-37 file).

## Why new-assessment posting is still refused

The settlement line of a new assessment posts to the tax-account control account. Control-account admission requires the tax-account match to exist, while the match is defined in terms of the assessment's own journal line, which does not exist until the journal posts. The two requirements are circular, and the E2E records the observed result: the journal posts, and the posting is refused with `InternalError` rather than completing. Choosing the ordering is a financial-contract decision for the tax-account and posting owners, so the sealed intent stays readable as pending and the status reports it as awaiting execution.

## Observed journey

The focused E2E posts a synthetic domestic purchase, admits it as a VAT fact, saves the actual return, and then exercises the bridge and assessment lifecycle:

| Step | Observed |
| --- | --- |
| Saved actual return | filing ready; box `49` exact `-125`, reported `-1`, residual `-25` |
| Bridge preparation | `plan.bridgeDeltaMinor` of `-25`, exactly the return's retained residual |
| Bridge execution | posts the residual delta; live-prior guard satisfied after excluding the executing bridge |
| Assessment execution (adoption) | adopts an existing tax-account match and references the posted effects |
| New-assessment posting mode | sealed and approved, then refused with `UnsupportedProfile`; the status reports it as awaiting execution, and the reason is the admission/match ordering above rather than a missing port |

Approval is exercised by a second actor, and the self-approval and already-receipted paths are refused rather than silently accepted.

## Repeatable command

```bash
bunx vitest run apps/api/tests/vat-assessment.e2e.test.ts
```

Two consecutive runs passed with no "source inputs changed during the E2E run" warning, so the result is fixed-revision evidence rather than an artifact of a concurrently edited tree. The temporary debug probe used during diagnosis was deleted.

## Remaining integration obligations

`new_assessment_posting` still needs the tax-account and posting owners to settle the control-account admission ordering described above; the internal match port it needed is delivered. Reclassification and amendment effects remain with their reserved owners. The MCP transport journey is unobserved, and no financial journey is claimed for the packet as a whole beyond the bridge and adoption paths recorded above.
