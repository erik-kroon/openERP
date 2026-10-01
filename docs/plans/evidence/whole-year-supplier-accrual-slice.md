# Whole-year packet 8: bounded synthetic accrual slice

Implemented owner: `apps/api/src/application/purchases/supplier-settlements.ts`. This extends the previously integrated pending-review slice with real HTTP/MCP execution, joined native posting/match/allocation receipts and atomic latest cancellation in the original or a selected later open period. It is **not complete packet 8** and does not activate a real-company rule.

## Observed proof — 2026-10-01

Current consolidated supplier proof: **20 passed, zero failed/skipped** at
`test-results/supplier-packet8-current-20261001`, including later-open-period
recovery, report concurrency and migration0055 receipt bindings. The full
changed-file gate and integration declaration check pass. This does not release
the unimplemented wider families or establish actual-company qualification.

Earlier bounded supplier verification is **16/16, zero failed/skipped** at
`test-results/supplier-qualified-accrual-20261001`, after the discovery,
cancellation impact/revocation/history, qualification and authority changes below.
Full changed-file gate passed. This is the supplier suite only, not a repetition
or extension of the older selected-regression or whole-workspace claims.
Unsupported retained provider observations now return `UnsupportedProfile`,
separately from malformed journals and oversized payable capacity.

After the native cancellation preflight and forward maker-exclusion additions,
the consolidated supplier suite passed **17/17, zero failed/skipped** at
`test-results/supplier-accrual-preflight-complete-20261001`. Full changed-file
gate passed; source/migration inventory is retained by that run. This consolidates
the focused observations below on one unchanged source, without rerunning the
workspace baseline or unrelated regression suites. It remains bounded accrual
proof, not whole packet completion.

From `/Users/admin/.codex/worktrees/cash-period-admission/openERP`:

```sh
OPENERP_E2E_ARTIFACTS=test-results/takeover-supplier-20261001-r5 bun run test:e2e apps/api/tests/supplier-settlement.e2e.test.ts
OPENERP_E2E_ARTIFACTS=test-results/takeover-supplier-regression-20261001 bun run test:e2e apps/api/tests/posting.e2e.test.ts apps/api/tests/bank-match-integrity.e2e.test.ts apps/api/tests/supplier-refunds.e2e.test.ts apps/api/tests/cash-payment.e2e.test.ts
bun run check:changed:full
bun run check:integration
```

Supplier suite: **7 passed, 0 failed, 0 skipped**. Selected regression suite: **21 passed, 0 failed, 0 skipped**. Full changed-file gate passed; integration registry passed with 33 wired and 17 declared deferred leaves. Dependencies and lockfile are unchanged; the earlier frozen-install observation is not a new install claim.

Runtime: disposable PostgreSQL 17.11, actual restricted runtime role, local workerd, Vitest 4.1.10. Base revision `ed41a9705bad458a04b3d3324b7124bcf9eeabca` plus retained worktree changes; the supplier manifest records diff SHA256 `e5d1a4ade44932dcdce3fce41c5f77f5bf292e5a2bfdeef64087c20b464ae1fa`. Stable source inventory before/after: `3b5c0714af27cd4ba5aaa7384f475ea64c473817e61cab46d486d2f3d0515c34`, no changed paths. Manifest includes per-file and migration hashes, including forward migration `0053-supplier-settlement-execution.sql`. The exact source, not merely HEAD, owns this claim.

Artifacts reside in those two `test-results` directories: `manifest.json`, `source-integrity.json`, `results.json`, `postgres.log`, `worker.json`; supplier proof also retains `supplier-settlement-accrual.json` and pending proof. Reporter prints a JUnit path but no JUnit file was observed; do not claim one. Earlier failure artifacts in `takeover-supplier-20261001`, `-r2`, `-r3`, `-r4` remain intact.

## Independently specified outcomes

Accrued invoice 10000 minor units, observed bank debit -4000:

| State | Bank ledger | Expense | Payable | Vouchers/lines |
| --- | --- | --- | --- | --- |
| Prepared/approved | 0 | 10000 | 10000 | 1/2 |
| Executed | -4000 | 10000 | 6000 | 2/4 |
| Cancelled | 0 | 10000 | 10000 | 3/6 |

Cancellation preserves the original bank debit and permanent source claim. Real reconciliation reports difference -4000 and the source remains unavailable for a new settlement. Exact replay returns the retained receipts without another financial effect. Equal rows retain distinct identities; competing source/capacity plans produce one financial winner. Independently disabled reviewer authority refuses execution. Runtime history UPDATE/DELETE/TRUNCATE is denied; admin immutable and uniqueness probes exercise database integrity.

Five disposable rejecting-trigger boundaries exercise settlement match, allocation leg and parent receipt, then cancellation match reversal and parent receipt. Source logs show actual trigger errors; exact financial/counter/approval snapshots remain unchanged. Removing faults permits successful retry, including the full cancellation. These are bounded failure points, not every possible fault/race.

The takeover fixed native reversal defects uncovered on this real path: missing bank-plan command receipt, wrong array projection of released match legs, and nonexistent allocation-reversal execution/approval columns. Cancellation now admits only the invoice state produced by its exact settlement; a later invoice revision refuses before inverse preparation. Its red observation is retained in `-r4`.

## Remaining obligations and blocker

### Exact receipt relational integrity

Migration `0055-supplier-settlement-receipt-bindings.sql` adds composite receipt
foreign keys tying the approval to the exact plan, and the plan to the exact
payable/statement/row. Existing scoped keys remain; no grants or workflow logic
move into PostgreSQL. The new E2E failed before the migration at the missing
approval/plan constraint (`supplier-receipt-relations-red-20261001`) and passed
one selected case after it (`supplier-receipt-relations-green-20261001`). It
inspects both installed composite constraints and observes three foreign-book
receipt insert refusals with SQLSTATE `23503`, rolling back each isolated probe.
Financial snapshots remain unchanged. These are cross-book insert probes, not
independent executions of each same-book mismatch; exact same-book relationships
are enforced by the installed composite constraints. Full changed gate passed.

### Later-open-period cancellation

Cancellation preparation now accepts optional `correction` with
`accountingPeriodId` and `postingDate`, matching the native correction owner's
selection fields. Omitting it preserves the original date/period. Amounts,
accounts, source claims and native child identities remain owner-derived.
Both original and selected periods must remain open; the selected date must lie
in its period and cannot precede the settlement. Native allocation/match period
guards are unchanged. This does **not** release correction from a closed period.

The parent retains a separately qualified correction-date profile witness and
the union of original-date and correction-date impact resources. Approval and
execution revalidate both dated witnesses and the native correction dependencies.
Earlier same-date plans remain readable and use their original profile witness
when no separate correction witness was retained. Reports covering either date
and retained closing certificates still refuse; the permanent source claim remains.

Focused verification passed **4 selected tests, 14 unselected** at
`test-results/supplier-cross-period-qualified-20261001`: normal same-period
settlement/cancellation, both existing report-consumption refusals, and a new
September-to-October correction. Its independent period oracle is September bank
`-4000`/payable `6000`, October bank `4000`/payable `4000`, total bank `0`/payable
`10000`, expense unchanged `10000`, three vouchers/six lines. It also proves locked
original/target refusal, invalid target-date refusal, exact committed replay and
one retained source claim. `supplier-cross-period-cancellation.json` retains
period balances and joined receipts. Full changed-file gate passed. No schema
migration, dependency change, provider action or real-company activation occurred.

Original and selected period locks are acquired once each in sorted ID order.
After this ordering change, two selected cases passed at
`test-results/supplier-cross-period-lock-order-20261001` (16 unselected): the
existing same-period journey and the later-open-period journey. This verifies
behavior after the ordering change, not a concurrent deadlock proof.

Report creation uses the same update book lock as cancellation. A concurrent
ordinary REST probe passed one selected case (18 unselected) at
`test-results/supplier-report-concurrent-20261001`. Its independent allowed
outcomes are: report first retains two vouchers and cancellation refuses without
effects; cancellation first retains three vouchers and a report including the
inverse. The artifact `supplier-report-cancellation-order.json` records the
observed ordering. This single race does not claim both orderings were exercised.

### Retained report cancellation fence

Cancellation execution now rechecks actual native approval actors and plan IDs
against the sealed parent before any reversal, excludes the maker, and checks
parent plus all three native expiries in one database-time snapshot. Invalid
timestamp text fails closed; forward approval usability also rejects invalid
expiry text. Focused verification passed two selected cases at
`test-results/supplier-cancellation-expiry-binding-20261001`: the normal financial
journey and independently inserted wrong-parent-actor/past-expiry/malformed-expiry
records. All refusals retained the prior independent financial fingerprint.
This is later source than the 16/16 claim above and does not extend that whole-run
claim; its full changed-file gate passed.

Native cancellation approval preflight now also compares each retained child
digest, checks native revocations and posting consumption before any reversal.
`test-results/supplier-native-approval-preflight-20261001` passed two selected
cases: normal cancellation and one refusal journey covering maker impersonation,
past/malformed parent expiry, an independently inserted wrong native match digest,
and ordinary operator revocation of the exact native match approval. Its artifact
retains the actual revocation plus independent financial snapshots. No new
database grants or migration were needed for these plain scoped reads.

Sealed settlement currentness now treats lost accounting-profile qualification
as a stale dependency, rather than presenting an already approved plan as a new
unsupported request. New preparation retains `UnsupportedProfile`; locked-period
and other error semantics remain unchanged. Cancellation revalidation applies the
same stale mapping. Focused ordinary company-fact/review verification passed one
selected case at `test-results/supplier-qualification-change-20261001`: supersede
confirmed accrual with independently confirmed cash, refuse the old approved plan
with `StaleDependency`, refuse fresh preparation with `UnsupportedProfile`, retain
identical independent financial snapshots. This does not release cash settlement.

`test-results/supplier-stale-and-revocation-20261001` passed two selected cases:
one four-vector matrix observes account version, writer epoch, source revision and
locked-period refusal after independent synthetic database changes; the pending
journey now also exercises fresh execution after approval revocation and invoice
revision. Each refusal retains its independent pre/post financial fingerprint.
The matrix artifact is `supplier-stale-bases.json`; this is not a broad-suite rerun.

Reviewer admission now requires an actual enabled row for both forward and
cancellation execution. A missing row no longer passes the old `enabled === false`
check. Focused verification passed at `test-results/supplier-missing-authority-20261001`
after independently deleting only the synthetic reviewer's admission: execution
refuses `ApprovalRequired`, with unchanged financial snapshots.

`test-results/supplier-source-qualification-20261001` passed two selected cases
covering scoped foreign-book preparation refusal, positive observations, and a
retained debit 11000 against payable capacity 10000. The owner refuses instead of
clipping or posting another cash movement. `supplier-source-refusals.json` retains
literal input amounts, expected codes, and independent pre/post snapshots.

Cancellation basis validation now refuses `StaleDependency` when a retained
report snapshot in the admitted book covers the settlement date. The shared
basis check runs during preparation and later cancellation revalidation; this
bounded owner does not adopt the generic correction owner's nonblocking report
policy. No report is rewritten or deleted.

The cancellation plan now retains the correction owner's actual impact-resource
list and compares it again at approval/execution. Retained closing certificates
also refuse, and an over-limit impact list fails closed. Historical plans without
this witness remain readable but require fresh preparation before execution.
Focused verification at `test-results/supplier-impact-witness-20261001` passed
three selected cases, including a report created after cancellation approval.

Operator REST now exposes cancellation approval revocation at
`/purchases/supplier-settlement-cancellation-approvals/:id/revoke`. Migration
`0054-supplier-cancellation-revocations.sql` adds scoped append-only records with
only runtime SELECT/INSERT grants. Revocation shares the book lock with execution;
committed exact replay still returns its original result. No MCP approval or
revocation tool was added. Focused verification at
`test-results/supplier-cancellation-revoke-20261001` passed one selected journey:
revoke, refuse execution without effects, independently approve again, cancel once.

Focused ordinary-owner verification passed **1 selected test** (8 unselected)
at `test-results/supplier-report-fence-20261001`: settle, retain a trial balance
through `/report-snapshots`, refuse cancellation, and compare independent
financial snapshots. `supplier-report-consumption.json` retains those snapshots.
Both changed-file gates passed. This is not proof of report/cancellation races
or whole-packet completion.

### Scoped discovery and cancellation recovery

Cancellation approval history is additionally recoverable through
`GET /purchases/supplier-settlement-cancellation-plans/:id/approvals?after=ID`
and read-only MCP `purchases_list_supplier_settlement_cancellation_approvals`.
Pages join scoped immutable approvals to their revocations, at most 25 per page.
They do not imply current permission. Completed cancellation under a fresh
command key now refuses `AlreadyPosted`, while exact committed replay retains
the original receipt. Consumption refusals identify the retained report/closing
record and its ordinary read path.

`test-results/supplier-authority-order-20261001` proves a blocked execution is
waiting for reviewer admission, while a second transaction can still lock the
book NOWAIT. Committing reviewer disable then produces `ApprovalRequired` and
unchanged independent financial snapshots. This uses observed blockers rather
than sleep timing and retains `supplier-authority-lock-order.json`.

Combined supplier run `supplier-cancellation-recovery-combined-20261001` passed
11 and failed one: the old MCP-name assertion mistook a read-only approval-history
tool for an approval write. The assertion now checks the actual approve/revoke
verbs; the affected pending case alone passed in
`supplier-cancellation-recovery-pending-20261001`. No whole-suite green claim is
made for that failed run. Subsequent focused history/fresh-key/report refusal
verification passed two selected cases at `supplier-history-idempotency-20261001`.

The owner now exposes `GET /purchases/supplier-settlements?after=ID` and
`GET /purchases/supplier-settlement-cancellation-plans/:id`, with read-only MCP
tools `purchases_list_supplier_settlements` and
`purchases_get_supplier_settlement_cancellation`. Discovery scopes both union
arms and receipt joins to the admitted book, sorts stable IDs and returns at
most 25 entries with a continuation cursor. It is a live identifier page, not
a frozen source inventory. Cancellation reads return the retained plan and
its exact committed receipt; they make no current approval/execution claim.

Failure-first ordinary REST observations returned 404 for both absent reads
(`test-results/supplier-discovery-red-20261001`). Full supplier verification
then passed **8/8, zero failed/skipped** at
`test-results/supplier-discovery-green-20261001`, including a 26-plan two-page
journey, foreign-book empty page, REST/MCP continuation parity, cancellation
receipt recovery and unchanged financial state. The discovery artifact retains
both pages and independent pre/post financial snapshots. Full changed gate
passed; no schema migration or dependency change was needed.

### Follow-up owned-source fence

After the first integration at `517d597`, an additional failure-first probe found
that generic bank-allocation preparation could still seal a plan over a cancelled,
permanently claimed observation (HTTP 200). The final writer already refused its
execution, but preparation must not advertise that capacity. Preparation now
checks retained claims under the admitted book lock and refuses `ApprovalRequired`.
The same real journey also verifies generic posting correction, allocation reversal,
match reversal and cancelled-source direct matching fences.

Red artifact: writer `test-results/takeover-supplier-fences-red-20261001` (one failed,
six intentionally unselected). Green artifact: writer
`test-results/takeover-supplier-fences-green-20261001` (**7/7**, none skipped).
Full changed-file gate passed. This follow-up does not repeat or extend the earlier
21-test regression claim. The subsequent API README edit only corrects the stale
missing-owner description; it changes no executable source.

The bounded synthetic transaction works. The blocker to **whole packet acceptance** is incomplete qualification and coverage, not credentials or an outside reviewer: wider transaction populations and correction paths remain unsupported. Real-company activation still requires evidenced accrual/VAT methods and dated applicable rules (D-04/D-08). Cash, FX/fees, provider payment instructions, replacement/reassignment, closed-period and later-consumed correction are not released. Later-open-period cancellation is supported under the bounds above.

Remaining first-unit qualification includes exhaustive child-expiry/native-approval relation and cross-book relational constraint vectors, cancellation/revocation commit-order races beyond the observed reviewer-disable ordering, and wider retained assessment/close consumption. The implemented and verified discovery, cancellation reads, generic source fences, account/source/writer changes, method supersession and reviewer prebook ordering are no longer missing. No UI, whole-year journey, complete backup/restore or first-pass freeze/comparison proof is claimed. Packet 1 remains verified only at its recorded `375bea6` source.
