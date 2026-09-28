# NEXT-37 review repair

Base: `0195527`, branch `review/next37-assessment-completion`. Work is isolated from main. This record distinguishes the failure contract, implementation and observed proof.

## Integrator acceptance

The reviewed repair is committed as `c5075fe`. Independent review identified
the stale-preparation recovery gap recorded below; after repair it approved the
receipt-level uniqueness, fresh approval and immutable-history behavior.

The integrator merged main's `3127991` credit source-identity fix into the isolated
branch. `bun run check:changed:full 0195527` passed. The combined NEXT-37,
NEXT-07 supplier-refund, NEXT-23 financial-close, posting, admission and persistence
run passed **38 tests across six files**. Source inventory remained stable:
`8a48c4d55fbed35abb1be15e0957d7c712fad30c1fbab4a09391e9ed0297f37b`.
This supplements the prior 35-case receipt; the additional three cases exercise
unpaid credit numbers and exact-key recovery on the integrated financial owners.

## Failure contract recorded before production edits

The seam is real HTTP against the disposable PostgreSQL/workerd E2E runtime. Only synthetic identity, rule and chart prerequisites may be seeded; assessment matches and financial receipts must be produced by their owners.

| Given / when | Required result | Counterfactual caught |
| --- | --- | --- |
| Return residual -25; prepare two bridges before executing either | Both propose -25; executing one makes the other stale | Pending preparation counted as a posted vector |
| Execute a bridge; retry identical command key and payload | Same successful response, one voucher and receipt | Receipt decoded as preparation on replay |
| Save another snapshot for the same obligation after a bridge | Effective prior bridge follows the obligation, not snapshot ID | Double rounding posting |
| Concurrent same-key writes | One result recovered by both callers | Shared-lock writer race |
| Reviewer disabled or removed after approval | Execution refused; previously committed response remains recoverable | Historical approval mistaken for current authority |
| Wrong book/scope | No foreign record or financial write | Scope escape |
| Valid match unmatches before adoption/execution | Refuse retired relationship | Immutable history mistaken for active capacity |
| Assessment consumes match; ordinary unmatch/correction requested | Refuse; original effect stays owned | Unmatch/rematch duplicates assessment effect |
| Assessed amount differs from effective reported remaining | Difference visible before and after execute | Caller hides discrepancy by supplying expectation |
| New assessed movement | Exact settlement +A / tax-account -A, real owned match and one receipt in one transaction | Always-refused path or journal without match |
| Failure during final receipt persistence | No voucher, match, capacity, counters or receipt survive | Partial financial group |
| Closed financial interval | Posting refused through shared close fence | Assessment bypasses NEXT-23 |
| Zero assessment | No zero journal; only supported evidenced relationship, otherwise explicit unsupported source meaning | Manufactured zero line |

Command: `bunx vitest run apps/api/tests/vat-assessment.e2e.test.ts`.

Initial hypotheses: bridge queries include unexecuted plans; bridge command result has the wrong wire shape. The claimed match-before-post circular prerequisite is not established by the current source and must not be used to justify a bypass.

## Observed fail-before

Before any production edit, the focused HTTP run on 2026-09-28 failed both required assertions:

- Second preparation returned bridge delta `0`, expected `-25`, while its predecessor remained unexecuted.
- Identical bridge-execution key and payload returned HTTP 500 `InternalError`, expected the original HTTP 200 result.

The failed run is retained locally at `test-results/e2e-history/2026-09-28T11-41-25.692Z-d283b215/`. Its `results.json` contains both failures; `source-integrity.json` records stable source inventory `d6f5d92a32d2cfb2ba3a0875048f527397af50a15239919867f61f2e3cd6f09a`. The directory timestamp is when the harness archived that earlier run, not its execution time.

## Reconciled owner contract

The real reporting owner is `vat_reporting_obligations`, uniquely keyed by book, registration namespace/identity, jurisdiction, scheme and period. Its released contract is specifically `synthetic` / `synthetic_registration` / `SE` / `synthetic_output_input_v1`. NEXT-37 reuses the reclassification owner's `readReportingObligationInTransaction`; it does not create a second obligation register. Migration 0031 adds immutable return-to-obligation references. Under this single released synthetic registration, reads include prior snapshots of the same exact period, including legacy rows that predate the references.

Actual-return rows remain immutable calculation snapshots. The most recent saved ordinal for the exact period is the supported calculation target for new work; execution refuses a superseded snapshot. The selected return ID and digest remain lineage, not obligation identity or evidence of filing. A calculation must be supported by its retained qualified rounding profile; filing readiness, control completeness and external acceptance remain separate states. Reclassification vectors are selected by the reporting obligation, not by the date on which their voucher happened to post. The existing draft-amendment owner supplies no financial effect, so NEXT-37 invents none.

Supported assessment meaning is `signed_statement_movement`: one retained, independently evidenced tax-account charge or credit event, attested to the obligation. Positive A requires a `tax_charge` event of `-A`; negative A requires `tax_credit` of `-A`. An evidenced zero statement movement can consume its event with a no-journal/no-match receipt. This does not infer a zero decision from absence of events. Full-replacement authority decisions and provider-specific reassessment deltas need their own qualified provider semantics; this implementation does not guess them.

## Repairs by finding

| Finding | Implemented repair |
| --- | --- |
| Pending bridge counted as effect | Only bridge rows with successful receipts enter prior vectors. Prior receipt membership is sealed and checked under the writer lock; two pending preparations propose the same residual, then the losing plan becomes stale after one commits. |
| Historical reviewer accepted | The trusted `beforeBook` hook locks the referenced reviewer admission/membership before the book. After replay, execution requires a current independent operator, matching digest and unexpired approval. |
| Retired/rematched effect adopted | The tax-account owner validates the active usable exact event/voucher/tax-line relationship. A successful assessment consumes the event independently of match identity. Consumed matches cannot be ordinarily unmatched, and their vouchers cannot be generically corrected. |
| Caller hides discrepancy | `expectedRemainingMinor` is derived from the selected return's reported book-minor amount minus receipted prior assessments. The retained source and prior membership are sealed. Read status includes pending source movements; it computes unique captured movements minus the reported target rather than summing successive residuals. |
| Snapshot used as obligation | New plans carry the real reporting-obligation ID. Return bindings are append-only. Prior effects and history span the obligation's same-period snapshots. |
| Shared writer lock and replay mismatch | Every NEXT-37 mutation acquires the book writer lock at admission, before replay and capacity reads. Bridge command receipts now store the same preparation-shaped result returned to the caller. Old receipt-shaped bridge command results are decoded and resolved back to their original immutable bridge. |
| New posting always refused | The assessment owner posts the exact approved settlement/tax vectors through the existing kernel and calls the tax-account match owner on the posted tax-account line in the same caller-owned transaction. The final assessment receipt consumes its source event. Any failure rolls the entire group back. |

The posting admission check resolves the retained bridge/assessment from its exact owned event, requires its internal owner ID, and compares its sealed account/amount vectors and evidence. Ordinary callers cannot execute that owned event. There is no control-account bypass switch. Existing period, account, historical, correction and NEXT-23 close admission remain in force. Rounding gain/loss accounts cannot be another control family, and settlement/tax roles use the existing resource-admission owner.

```text
authority locks (executor + referenced reviewer)
  -> book FOR UPDATE
  -> exact-key recovery OR current source/prior/approval checks
  -> kernel voucher + lines + kernel receipts/counters/outbox
  -> tax-account owner match + capacity, on the actual tax-account line
  -> assessment receipt + event consumption + command result
  -> one commit (or complete rollback)
```

`recordTaxAccountMatch` no longer reacquires the book lock. Its public caller already enters with writer admission; the assessment caller owns the same lock and transaction. No nested public operation or second financial transaction is used.

## Actual failure behind the earlier ordering claim

Replacing the seeded empty statement and wrong settlement-line match with real HTTP import/preview/match exposed HTTP 500 in `previewMatch`. Source inspection located an invalid PostgreSQL query in `db/vat/reclassification.ts`: multidimensional `unnest` produces one scalar column, not the two columns assigned by its alias. The repair uses a typed two-column `VALUES` relation. The subsequent real match journey passes.

The match usability projection also counted its own tax-match capacity as a competing claim. Its internal query now excludes only the exact match being evaluated; every other owner/capacity check remains. These are the integration defects repaired at the shared owners. The old “a match must exist before the journal posts” diagnosis is not retained: new posting followed by matching has now succeeded atomically through the real owners.

## Forward migration and compatibility

Only **`apps/api/migrations/0031-next-37-review.sql`** is added. No applied migration, including 0028, changes.

- The immutable return binding references the existing return and reporting-obligation owners.
- Assessment receipts carry non-null `event_id` and `assessment_identity`, each unique per book, and a once-only non-null match reference. Foreign keys tie the proposal, identity, event, match and voucher together. The follow-up renewal repair removes preparation-level identity/match uniqueness and backfills the two relational keys on legacy successful receipts from their existing proposal rows. The migration owner temporarily disables only the receipt's immutable-row trigger for this backfill, then restores it in the same migration transaction; bodies, digests, command results and runtime permissions remain unchanged. Conflicting historical successful receipts fail the new uniqueness constraints rather than being discarded.
- The historical match-reference FK is added `NOT VALID`: new writes must satisfy it, but migration does not assert that unreviewed legacy rows are valid. No old body/digest is rewritten or retroactively labelled verified.
- `expectedRemainingMinor` remains accepted on preparation for older callers, but is optional and not authoritative. Responses contain the server-derived value.
- New optional fields retain source/prior seals, supported movement meaning and the bridge posting date. Optional decoding preserves old records and command responses.
- A compatible legacy assessment can receive a fresh independent approval over its validated source and prior receipts. Its stored expected amount must equal the live derived amount. An old approval lacking those seals cannot authorize fresh execution. A stale unexecuted assessment can now be prepared again with the same authority identity: the new immutable ID/digest captures the current basis and requires its own approval. Old plans remain stale and readable rather than being silently reinterpreted. Existing committed same-key responses remain recoverable.
- Execute responses keep their existing immutable preparation shape; financial receipts remain separate persisted records. History/status span same-period obligation revisions. Status discrepancy semantics are now captured signed movements versus the reported target, including pending movements; this is intentionally different from the former caller-controlled sum.

## Final observed verification

All commands ran in the isolated worktree against disposable synthetic data, local workerd and PostgreSQL 17.11 with the restricted runtime role. Dependencies were installed with `bun install --frozen-lockfile`; manifests and `bun.lock` did not change.

```sh
bun run check:changed
bun run check:changed:full
bunx vitest run \
  apps/api/tests/vat-assessment.e2e.test.ts \
  apps/api/tests/supplier-refund-journey.e2e.test.ts \
  apps/api/tests/financial-close.e2e.test.ts \
  apps/api/tests/posting.e2e.test.ts \
  apps/api/tests/admission.e2e.test.ts \
  apps/api/tests/persistence.e2e.test.ts
```

Final result after the P1 renewal repair: **both changed-file gates passed; 35 tests passed across six files**, including all six NEXT-37 tests. The combined run completed on 2026-09-28 at 12:29:20 UTC. The existing persistence test also observed migration rerun preservation and checksum-drift refusal with the refined migration 0031 present. No timeout or source-change warning occurred.

The focused NEXT-37 HTTP assertions observe:

- exact `-125`, reported `-1` whole unit (`-100` book minor), residual/bridge `-25`;
- pending preparation exclusion, losing-plan staleness and exact-key bridge recovery;
- a second saved snapshot retaining the same obligation and proposing bridge `0`, including concurrent preparation recovery;
- real tax-account import, preview, match, unmatch, rematch and retired-match adoption refusal;
- adopted `+5000` against derived expected `-100`, with discrepancy visible before execution despite caller input `5000`;
- consumed-match unmatch refusal and generic correction execution refusal (preparation/approval of the correction remain readable);
- disabled-reviewer refusal, wrong-book refusal, and concurrent identical new-posting execution returning one result;
- a deliberately failing final assessment-receipt constraint rolling back posted-state counts, sequence/counter, kernel receipts, outbox and match; the original command then succeeds after removing the fault;
- new `+100` charge with the matched tax line credit `100`, and a separate `-5200` credit movement with derived expected `-5200`;
- an evidenced zero movement with null voucher and match, without a zero journal;
- status ending at assessed `-100` and discrepancy `0`, with identical read-only MCP and HTTP results;
- actual NEXT-23 close followed by assessment execution refusing `PeriodLocked`.
- four renewal variants: new posting and real-match adoption, each with prior-receipt staleness alone and with a further return snapshot. Each proves A60/B40 prepared and approved against reported `100`, A execution, original B refusal, fresh B preparation under the same identity, old-approval refusal on the fresh ID, independent fresh approval, concurrent exact-key recovery, and exactly one B execution/match. Old preparations/approvals remain recoverable under their exact keys; successful identity/event reuse is refused and obsolete proposal blockers disappear from status while full history retains the proposals.

NEXT-07 paid-credit/refund tests and the four NEXT-23 close/reopen/carry-forward tests pass unchanged in the same combined run. These are integrated-source compatibility observations, not a claim that the NEXT-37 fixture itself contains a supplier-refund or reclassification journey.

### Retained artifacts

Final local artifacts are under `test-results/e2e/`:

- `results.json`: exact retained test results (the runner announced JUnit output, but no `junit.xml` remains in the final artifact directory, so it is not relied on);
- `manifest.json`: base revision, runtime, migration/source inventory and hashes;
- `source-integrity.json`: `stable`, no changed paths; initial/final source inventory **`8ae0945a6547edaaf4d370b48e6ba549ce7112474119e5ce7c20f7f4d2679874`**;
- `next37-assessment-outcomes.json`: actual prepared plans, returned results, history and status vectors;
- `next37-assessment-completion.json`: final ledger and persisted financial counts;
- `next37-close-fence.json`: the closed-book financial state;
- `next37-renewal-{new,adopt}-{false,true}.json` and matching `-outcomes.json` files: ledger/persisted state plus original and renewed proposals, approvals, response, proposal IDs, status and retained history for all four renewal variants;
- `migrations.log`, `next-07-paid-credit-refund-journey.json`, and the `financial-close-*.json` files: combined integration evidence.

The assessment ledger ends with five vouchers/receipts/outbox records: purchase, bridge, existing assessment voucher, new charge and new credit. Adoption and zero movement add no vouchers. Settlement remains `-125` because this fixture has not executed the separate reclassification owner. It does not claim reconciled or paid VAT.

### Limits and remaining qualification

Real-company registration, account mappings, original authority identity/period evidence, dated rounding rules and provider replacement/delta semantics remain D-04/D-08 (D-10 for connected provider use). The released tax-account/obligation contract remains synthetic. No real filing, payment, provider acceptance or production readiness is claimed.

The legacy-result decoder, fresh-approval compatibility paths and relational receipt-key backfill are source-reviewed, not exercised by restoring a pre-0031 production database. Fresh installation and migration rerun are observed. No historical target receipts were seeded to simulate upgrade proof. The reclassification-by-obligation query is source-reviewed against the actual owner/schema; the focused journey does not execute a reclassification voucher outside its reporting period. These limits do not revive the disproved circular prerequisite.

## Follow-up P1: renewable unexecuted assessments

### Failure contract recorded before renewal source edits

A preparation is not financial consumption of an authority identity or match. Given reported VAT `100`, prepare and independently approve A=`60` and B=`40` against empty assessment receipts. After A executes, the original B and a new approval attempt on it must refuse stale basis. Preparing B again with the **same authority identity and event** must create a new immutable proposal, derived expected remaining `40`, and require an approval for that new ID/digest. An exact-key retry of the old preparation/approval still returns its old sealed response.

The real HTTP regression will exercise both new posting and adoption of a real imported/matched tax-account line. It will repeat renewal after a further actual-return snapshot, reject old approvals on new proposal IDs, race identical execution requests, verify one B receipt/effect/match, reject executed identity reuse even with another event, reject event/match reuse under another identity, retain old rows in history, and report no obsolete pending B blocker after successful renewal. Test/fixture edits precede migration/application edits; fail-before and final source fingerprints will be recorded here.

### Observed failure and repair

After correcting the synthetic fixture's declared source-family coverage, all four HTTP variants reached the same failure **before renewal production edits**: A had executed, stale B execution and reapproval had both correctly refused, but `POST /vat/assessments/records` for renewed B returned HTTP 409 `AlreadyPosted` instead of HTTP 200. B had no successful receipt. That run is retained at `test-results/e2e-history/2026-09-28T12-26-21.833Z-dc6178e3/`, with stable source fingerprint **`225d893bffe100694fafb8076c4a9580f25d58339ab257afa889ed72b01da2af`**.

The repair stays within the existing preparation/approval/receipt model:

- `prepareAssessment` and the pure compiler's known-identity input now consult successful receipts, not preparations. `readExecutedAssessmentByMatch` likewise reads receipts. Another unexecuted proposal does not consume an identity or an adopted match.
- A shared writer-transaction check refuses an already-executed authority identity or event at preparation, approval and execution. It runs after exact-key replay so old preparation, approval and execution responses remain recoverable.
- Every renewal uses a new immutable preparation ID/digest and current source/prior seals. Approval is still keyed to that exact preparation ID/digest; there is no approval transfer or stale-plan mutation.
- Migration 0031 moves identity/match uniqueness from `vat_assessments` to `vat_assessment_receipts`; event uniqueness remains there. The receipt carries the actual authority identity, authenticated by a composite proposal FK. The typed mappings in `db/schema.ts` reflect the receipt columns and return-binding table.
- Status excludes unexecuted sibling proposals once that authority identity has a receipt. Full history and exact-key responses continue to expose the old proposals. Existing prior-effect digests retain their `{id, amount}` shape even though the read projection also returns identity for the once-only status check.

All four renewal variants now pass. Each ends with assessed total `100`, discrepancy `0`, no obsolete B pending blocker, exactly one A and one B assessment receipt, one B tax-account match and three ledger vouchers/seven lines (sale, A and B). In adoption mode B's pre-existing voucher is referenced, not reposted. The final combined 35-test proof and source fingerprint above supersede the earlier 31-test handoff.

## Integrator reading order

1. This failure/contract/evidence record, then the focused E2E.
2. `apps/api/migrations/0031-next-37-review.sql` and `packages/contracts/src/vat-assessment.ts`.
3. `apps/api/src/application/vat/assessment.ts`, `apps/api/src/db/vat/assessment.ts` and the NEXT-37 mappings in `apps/api/src/db/schema.ts`.
4. `apps/api/src/application/vat/tax-account.ts` and `apps/api/src/db/vat/tax-account.ts`.
5. `apps/api/src/application/posting-admission.ts` and `apps/api/src/db/posting-admission.ts`.
6. The narrow obligation-port extraction in `application/vat/reclassification.ts` and claimed-line repair in `db/vat/reclassification.ts`.

All changes remain unstaged and uncommitted on `review/next37-assessment-completion`, based on `0195527`. The integrator owns final review, staging, commit and merge.
