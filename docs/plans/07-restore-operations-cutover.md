# Restore, production operations and cutover

Owner: operational tooling/runtime adapters and the integrator for deployment/authority. Phase: foundations begin at P0/P1; full release/cutover at P7. Retain the existing [local recovery tooling](../operations/local-recovery.md) as an explicitly synthetic, fresh-destination exercise. Its checksum/table comparison is not yet complete application recovery or production archive evidence.

## Operating model and boundaries

Deploy one authoritative PostgreSQL book with immutable object manifests, the Effect application and durable delivery workers. Worker and Bun compositions use the same domain operations. Select actual database/object/archive providers, geography, access/retention settings, recovery objectives and operator responsibility through D-07. These are deployment facts with a concrete readiness checklist, not missing core architecture.

Release authority is distinct from accounting and restore authority. Operators can inspect metadata without accessing every payroll/evidence payload. Production logs carry scoped correlation, operation/key digest, receipt/run/attempt identity, outcome, latency and error class; they omit tokens, raw source documents, personal payroll content and complete connection strings. Evidence access is authorized and audited.

## Evidence and archive lifecycle

Use immutable content-addressed object references plus storage version, size and hash. Upload first to a pending object, verify bytes, then commit the database reference. A failed reference commit leaves a discoverable orphan eligible for reviewed cleanup after a retention grace period; it must not leave a financial effect referring to absent evidence. An existing content object may be shared by occurrences only within permitted access/retention scope.

Archive manifests include original evidence, source occurrences/matches, approvals/corrections, rule/mapping/taxonomy bundles, report/filing/payment artifacts, external receipts and audit history. Encryption/key custody, access revocation, retention/hold and deletion rules are explicit operational policy. A delete requires both policy eligibility and proof of no required retained reference/hold; never use a generic age-based purge on accounting objects. Cloud location alone cannot prove compliant retention.

Restore depends on usable decryption keys and configuration as well as object bytes. Back up key identifiers/recovery procedure and exercise key recovery through authorized custody; do not place live secrets in Git, manifests or public artifacts. The archive must remain readable when the original application process/provider is unavailable.

## Consistent backup contract

`BackupManifest` identifies source environment/cluster, schema/migration versions, book writer epochs/cutoffs, database snapshot/LSN basis, complete object reference closure, file hashes/versions, required roles/extensions/configuration, rule/artifact versions and pending external work. Capture the database under one consistent snapshot. Enumerate all committed object references from that snapshot, then verify immutable object versions are retained and readable. Concurrent new objects are outside the snapshot; referenced objects cannot be garbage-collected while the backup lease/retention holds them.

Back up the whole required database state, including sequences, privileges and extension requirements, not a hard-coded table allowlist. Extend the current tool's explicitly unsupported relation types only with a named verification mechanism. If any required table/object/role/key/schema element cannot be backed up, the result is incomplete, not a successful bundle with a warning hidden in logs. Preserve duplicate row multiplicity and independent control totals.

A local checksum detects alteration relative to that checksum; authenticity requires a manifest signature or independently controlled digest registry. Retain independent attestations of successful backups and periodic restore evidence. Define accepted RPO/RTO numerically in the deployment record and measure them in rehearsal. If a recovery point predates an acknowledged accounting/provider effect, that effect must be reconstructed and reconciled before writes reopen; never erase acknowledged history to satisfy a time target.

## Quarantined restore and promotion

Restore to a fresh isolated destination, with application/provider egress and write admission disabled. Validate dump/schema/migrations, object closure/decryption, privileges, sequence/counter state, immutable receipt identities and independent ledger/register/source controls. Run read-only application paths through the actual restricted role; prove evidence retrieval and historical report reconstruction. A matching table hash alone cannot prove role equivalence, object completeness or app behavior.

Keep outbox, filing/payment workers and scheduled tasks suspended. Compare durable provider attempts with actual provider state before allowing resumed delivery. Unknown results remain unknown until resolved; restoring a pre-acknowledgment attempt cannot authorize duplicate submission. Record missing/partial work and any manual resolution in the restore receipt.

`RestoreReceipt` includes all checks run/not run, failures, reconstructed boundaries, measured recovery duration, object/key evidence, role/application checks and operator identity. A restore receipt does not itself promote a writer. Promotion requires a separate reviewed authority transition with new environment identity/epoch and source fencing.

## Delivery and operational monitoring

Outbox rows are immutable intent plus mutable lease/attempt projection. Claim bounded work using transactional row locking and a fencing token. Persist every provider attempt and its response/uncertainty. Derive abandonment/recovery windows from the entire maximum worker cycle plus request allowance; do not reclaim the last items in a still-active serial batch. Charge actual failed/abandoned attempts and release unattempted claims. Receiver idempotency and our event identity make at-least-once delivery converge.

Monitor pending-age and lease-expiry distributions, retries/dead deliveries, unknown external outcomes, failed mandatory checks, source lag, stale approvals/reconciliations, transaction lock/connection pressure, archive integrity and restore age. Alerts name the affected scope and recovery action. An alert cannot automatically repost, broaden authority, delete retained evidence or resubmit an uncertain payment.

Use deployment-specific measured limits for concurrency, request/object sizes, transaction timeout and worker budgets. Readiness refuses a required capability if its dependency is unhealthy/unavailable. Cost/rate limits must queue or reject transparently rather than silently omit provider records.

## Deployment and schema changes

Keep immutable applied migrations/checksums. Validate a clean install and upgrade from a populated previous supported schema under the real runtime role. Introduce additive schema and adapters first where an actual coexistence window exists; backfill with durable checkpoints and independent counts; switch consumers after validation; remove obsolete access only after the compatibility window closes. Do not keep a parallel ledger as a migration convenience.

A release manifest binds code, contracts, migrations, rules, validators and deployment configuration to its acceptance artifact. Destructive transforms require a reviewed recoverable procedure and separately authorized operation. Application rollback is allowed only to a version compatible with the current schema/receipts; otherwise use a forward fix. A stale client/worker must fail explicitly against a changed schema or writer epoch, not bypass new invariants.

## Cutover protocol

Choose an **offline, fenced single-writer transfer** for the first company. Online dual writing is not part of the plan. An explicit maintenance window trades availability for a tractable accounting boundary.

1. Inventory the actual source, target, provider credentials, jobs, pending payments/filings and admitted imports. Produce the source/target comparison and cutover proposal.
2. Obtain operational/accounting approval of exact scope, reconciled controls, recovery objectives and the proposed authority change.
3. Freeze the old writer at its database and admission boundaries; suspend jobs/provider egress, revoke old runtime credentials, drain/terminate active write sessions, and verify a real old-client write is refused. A UI banner or quiet session count is not a freeze.
4. Capture final source watermark/delta and immutable backup/archive closure. Import/reconcile the delta, all open-item/register controls, outstanding external attempts and evidence coverage on the quarantined target.
5. Record promotion in an independently retained authority log outside restorable data, using a new monotonically increasing epoch/environment identity. Configure new credentials, enable only the target writer and verify old credentials/jobs still fail.
6. Execute an authorized bounded acceptance action, verify its receipt/controls, then release the company workflow and observe the declared monitoring window. Resume external work only after individual attempt reconciliation.

Before target-native effects, rollback can restore the old writer only by reversing the reviewed authority switch after fencing the target. After any acknowledged native posting or external action, a backup rollback is prohibited as a business recovery strategy; use a reconciled delta/correction plan that preserves those effects. Loss of fence evidence aborts promotion. A restored old backup cannot regain authority merely because it contains an old `native` flag or epoch.

## Incident procedures

The runbook covers unavailable database, uncertain commit, corrupted/missing object, failed migration, stale/duplicate worker, lost credential, compromised actor, incorrect rule release, wrong report mapping and provider timeout. First contain authority and preserve evidence, then determine durable accounting/provider outcomes. Correct through named operations and forward repairs. Document customer/accounting impact and exact affected IDs; never rewrite a posted amount directly to make a dashboard look correct.

## Delivery packets

| ID     | Deliverable                                                                                           | Depends on             | Acceptance                                                                                                                                                     |
| ------ | ----------------------------------------------------------------------------------------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OPS-01 | Complete storage/archive inventory and consistent DB/object/key backup contract over current tooling. | FND-03, IMP-01         | E-21: missing referenced object/required relation fails completeness; original bytes recoverable.                                                              |
| OPS-02 | Quarantined full application restore, privilege/configuration reconstruction and measured recovery.   | OPS-01, FND-04         | E-20/E-21: read-only app and evidence/report reconstruction; no automatic writer/provider activation.                                                          |
| OPS-03 | Durable delivery/attempt state, bounded leases, fencing and provider-uncertainty recovery.            | PST-05                 | E-08/E-17/E-19: active worker not reclaimed; retry converges; unknown outcome does not resubmit blindly.                                                       |
| OPS-04 | Release manifest, populated upgrades, observability, credential/permission and incident runbooks.     | FND-04, OPS-01         | E-01/E-20: exact release proof, safe upgrade/forward recovery and redacted useful diagnostics.                                                                 |
| OPS-05 | Read-only actual-source cutover preflight and enforceable freeze rehearsal.                           | IMP-06, OPS-02, OPS-03 | E-21: actual old-client write/egress refusal; final delta and pending external work accounted for.                                                             |
| OPS-06 | Reviewed promotion/rollback-boundary protocol and actual company cutover.                             | OPS-05, OPS-04         | E-21: one writer, fresh epoch, preserved receipts and independently reconciled post-switch controls; applicable company gates and explicit authority required. |
| OPS-07 | Recurring restore/retention/recovery drills and operational acceptance review.                        | OPS-06                 | Measured accepted recovery objectives and coverage remain current; failures open incidents rather than silent green status.                                    |

OPS-06's END-07 gate applies when connected statutory fulfillment is required for the selected company release. A company using a reviewed external filing workflow still needs retained exact artifact and acknowledgment evidence; the actual provider connector is then explicitly not applicable to cutover. Do not delay early synthetic backup/restore work on later statutory development.

## Current local recovery implementation boundary

The [v2 recovery package](../operations/recovery-package-handoff.md) adds snapshot schema/role/migration inventory, inline evidence and declared supplementary/configuration closure, source-release capture, retained diagnostics and fenced reconstruction controls. It is implemented but not runtime-verified. Current normal application admission uses row locks and Better Auth mutable state; [restricted application recovery](../operations/application-recovery.md) remains a root-owned security decision. OPS-01/02/04 acceptance remains open; this package does not activate remote archive, production retention or cutover.
