# Candidate B: a dedicated recovered-book inspection owner

Status: design proposal only. Grounded in the read-only dirty source at HEAD `50c745dfc268c51b6fa4075683d71018f0adf125`; bind every seam to the frozen baseline before implementation. The conceptual PostgreSQL locking-read incompatibility was traced, not reproduced in this task. No code, rehearsal, provider action or company-data claim is represented here.

Phases: Ground completed from `recovery-grounding.md`; Sketch completed here; Agree belongs to root synthesis; Implement and Scrap are outside this design-only brief. Other agents own source work; this candidate changes only this document.

## Problem

SQL/object restoration currently ends in confirmed quarantine and `blocked-restricted-read-admission`. Ordinary application admission deliberately locks credentials/sessions, identity admission, membership and book; changing only the book lock cannot make it read-only. The selected packet needs real application evidence, original, receipt, correction and saved-report interpretation under distinct restricted inspection authority, while preserving live authority locking and writer/provider fencing. Candidate B gives that inspection one application owner. It shares the existing read interpretation underneath ordinary wrappers rather than adding a recovery configuration to every ordinary owner.

## Usage (caller's view)

The operator first receives the unchanged reconstruction receipt from `operations/workflows.ts.restore()`. A separate inspection command consumes that exact receipt and manifest, opens one bounded inspection window, and returns an application-recovery receipt. It cannot resume work or promote a writer.

```ts
// Proposed usage; no implementation exists.
const restored = await restoreFreshVerifiedBundle(privateRestorePlan);
const inspected = await inspectRecoveredBook({
  restoreReceipt: restored.receiptPath,
  expectedManifestSha256: independentlyRetainedDigest,
  scope: { entityId, bookId },
  inspectionId: operatorPreparedInspectionId,
  receiptDirectory: newPrivateDirectory,
});
// inspected.applicationRecovery is verified only if all required reads,
// independent comparisons and the final connection quarantine pass.
```

For a lost response, the operator retries the same inspection identity and inputs; an existing complete, hash-verified receipt is returned after independently confirming current quarantine. Changed scope, manifest or source release with the same identity is refused. An incomplete attempt produces diagnostics and requires explicit fresh inspection identity after quarantine is confirmed; it does not silently start another window.

The operator never supplies a session/token copied from the source, SQL, an arbitrary route, table names, transaction flags, a writer epoch or expected financial amounts. The command derives the expected retained IDs and closure from the verified backup/control inventories. Supplementary independently specified fixture expectations belong to the test oracle, not trusted operator input.

## Shape

Proposed private data shapes:

```ts
type InspectionBinding = {
  inspectionId: string;
  manifestSha256: string;
  restoreReceiptSha256: string;
  sourceReleaseSha256: string;
  destination: { systemIdentifier: string; database: string };
  scope: { entityId: string; bookId: string };
  inspectorDatabaseRole: string;
  allowedReads: "recovered_book_v1";
};

// Constructed only by validated inspection admission, never decoded from callers.
type RecoveryReadContext = {
  transaction: ReadTransaction;
  binding: InspectionBinding;
};

type ApplicationRecoveryReceipt = {
  inspectionId: string;
  binding: InspectionBinding;
  baseReconstruction: { receiptSha256: string; schemaSha256: string };
  inspectionOverlay: { ddlSha256: string; effectivePrivilegesSha256: string };
  observations: RecoveredReadWitnesses; // IDs, independent hashes, cutoffs/counts
  deniedOperations: DenialWitnesses;
  transactionSettings: { readOnly: true; isolation: "repeatable read" };
  connections: "disabled";
  connectionLimit: 0;
  writerPromotion: "not-performed";
  providerPromotion: "not-performed";
  resumeAllowed: false;
  applicationRecovery: "verified_restricted_reads";
};
```

`inspectRecoveredBook` is the sole public application operation. Its runtime caller owns private input/output paths, process/network isolation, bounded connection opening and final quarantine. The Effect owner owns immutable inspection admission, the fixed read inventory, pagination, comparison and witness assembly. The PostgreSQL adapter owns the real restricted-role transaction and effective-grant verification. This is a deep interface: callers do not coordinate projection reads, object rechecks, paging or database stages (per the architect interface-depth and boundary-discipline guidance).

The context uses a compile-time read interface with no insert/update/delete/transaction-setting escape API, backed by actual Effect/Drizzle transactions. It is an accidental-misuse guard; the restricted PostgreSQL role and `BEGIN ... READ ONLY` are the enforcement. Verify the installed native adapter's transaction options against the frozen dependency rather than assume a Drizzle API. Add one explicit transaction entry point in `db/transaction.ts`; ordinary `withTransaction()` remains unchanged. Read-only/isolation must be established before any query, and `SHOW transaction_read_only`/isolation must be recorded inside the same transaction.

### Authority and connection window

The inspection login is newly created, has no `openerp_runtime` membership, no superuser/bypass-RLS/create-role/create-database/replication rights, no grant/set-role escape, and only the fixed read table/column/function closure. It is bound to the exact destination, manifest and entity/book; no source credential/session is admitted. The owner checks that binding at each transaction entry and around an object read. This is inspection authority, not pretending expired restored live authority remains valid.

To enforce selected-book scope in PostgreSQL as well as the application, candidate B includes a **target-only inspection overlay** after base reconstruction comparisons. Reviewed SELECT policies bind a concrete inspection role to constant entity/book IDs, never caller-set GUCs. Policies cover the precise projection tables, including books whose key is `id`; inspection receives no auth/credential or queue access. Ordinary runtime policies preserve their existing behavior while ordinary destination connections remain revoked. No policy changes financial calculations or performs a workflow. Inspection reads invoke the same query projections through native Drizzle.

This overlay is a material cost: current `operations/inventory.ts` refuses policies. Do not weaken that baseline gate or claim the final schema equals the source. Keep the base comparison unchanged, then independently hash/verify the exact reviewed overlay, role attributes, table coverage and effective grants; record both in the application receipt. A policy/grant outside that allowlist fails. Source backups remain under the existing policy-free inventory contract. The overlay must be removed or the role disabled during finalization and its cleanup observed; final schema equality should be rechecked if removal is the selected cleanup contract.

The runtime window changes destination connection availability only after base quarantine is confirmed: revoke destination CONNECT from all ordinary roles, admit solely the inspection login, bound its connection count, and retain read-only defaults. Never change a cluster-wide existing login to NOLOGIN, which could fence another database. The finalizer closes the inspection connection, removes/disables its admission and restores `datallowconn=false`, limit zero. An ambiguous open/close or response loss produces `not-confirmed`, no successful application receipt, and an operator containment requirement.

Run only the dedicated recovery host with local recovered storage and no Better Auth or provider composition. The host must have an enforceable outbound allowlist for the loopback destination PostgreSQL endpoint and required local IPC; denied-provider/network attempts are observed against a synthetic sink. Absence of credentials alone is not an egress fence. The native transaction and object adapter must work under that host restriction before this design can be accepted.

### Exact reuse seams

| Existing owner | Proposed seam; preserve ordinary wrapper behavior |
| --- | --- |
| `application/posting.ts` `getEvidence`, `getReceipt` | Extract transaction-scoped validated evidence/execute-receipt projection. Ordinary wrapper retains book/receipt share locks. Dedicated read uses unlocked immutable projection. `getReceipt` remains execute-only; do not flatten all command outcomes into it. |
| `application/source-retention.ts` `readStorage`, `getSourceOccurrence` | Share storage decoding, occurrence/admission validation and original-byte assembly. `readRetainedObject` retains size/hash checks. Ordinary wrapper retains authority/book/occurrence locks; recovery checks its inspection binding before and after external-byte read. |
| `db/source-retention.ts` `readOccurrenceStorage`, `listArchive` | Factor query body once with an explicit internal locked versus immutable-snapshot read choice. Current `FOR SHARE OF o` remains the default for ordinary callers. Do not globally remove it. |
| `db/posting.ts` `readCommandReceipt` | Share selected columns/predicate; preserve ordinary share/update locking. Recovery has a private unlocked read over immutable command result. |
| `application/reports.ts` `getReport`, `listReports`, `reportLines`, `reportExplanation`, `reportGeneralLedger` | Share transaction-scoped read interpretation and cursor validation beneath existing admission wrappers. Reuse saved header, date interval, sequence cutoff and report-line/contribution SQL. No `prepareReport` or replacement snapshot is called. |
| `application/posting-corrections.ts` `readBundleView`, `bundleView`, `getCorrectionBundleForVoucher` | Share retained bundle digest/row validation, original/reversal/replacement identity, receipt and approval-history projection. No new approval or calculation occurs. |

These seams extract existing semantics rather than copy report arithmetic, correction validation or evidence rules into recovery. If a read helper is inseparable from mutable workflow policy, refactor that owner into an owned read projection first; do not reproduce the calculation in the inspector. The inspector's fixed dispatch has only retained-read variants and refuses every unrecognized request.

```text
private inspection caller
  verified base restore + immutable inspection binding
  bounded destination-only connection/egress window
  application/recovery-inspection.ts
    restricted Effect/Drizzle READ ONLY transaction
    existing owned read projections + independently checked witnesses
    original bytes -> size/hash check -> binding recheck
  final quarantine and overlay/admission cleanup
  private application-recovery receipt, or contained failure diagnostics
```

## Failures and E2E obligations specified before code

Use disposable synthetic PostgreSQL/workerd/Bun fixtures and retained filesystem originals. The existing recovery test's ordinary target Worker/session activation must not be reused as inspection admission. Existing global setup supplies fixed-source/migration manifests, fixtures supply independently known postings/corrections/reports, and `database-support.ts` supplies scoped table images, privilege probes and sanitized artifact writing. Ensure the selected test is included explicitly: the existing `.recovery.test.ts` suffix is outside the default E2E glob.

| Trigger | Required independent expectation and durable witness |
| --- | --- |
| Complete fixture with another book, external and inline originals, posting and correction receipts, saved report exceeding one page | Exact independently specified bytes/hashes, IDs, signed amounts, saved cutoffs and full ordered lines/contributions; continuation reaches explicit end; before/after complete row fingerprints and sequences unchanged. Ordinary projection response equivalence is supplemental, not the sole oracle. |
| Different book/entity, destination identity, manifest, restore receipt, release or inspection identity; foreign resource ID/cursor | Refusal before data disclosure; no cross-book payload or existence leak; direct SELECT through inspection role cannot read the second book. |
| Restored API token/session; ordinary runtime login; role membership/set-role escalation | Admission denied; no auth queries required by inspection; ordinary authority locks unchanged in their existing race proof. |
| Financial preparation/approval/posting/correction/report preparation; auth/session/rate-limit mutation; outbox/queue claim, migration or provider route | Dedicated dispatcher refuses; direct restricted-role writes fail even after attempted `SET transaction_read_only=off`; all auth/queue/financial fingerprints and counters remain unchanged. No provider sink receives traffic. |
| Missing/truncated/incorrect object, damaged retained receipt/bundle digest, corrupt saved report/cursor or missing closure member | Appropriate refusal, no synthesized replacement, no partial success receipt; private diagnostic identifies stage/class without original content or credentials. |
| Lost response after receipt or repeated same inspection; same ID with changed inputs | Same receipt/digest after confirmed quarantine, or explicit incomplete/refused result; no financial or provider work and no silently repeated admission window. |
| Cancellation/error at admission, transaction, object fetch, receipt write or finalizer; wrong privilege/policy; stalled connection | Every owned connection/overlay is cleaned up; confirmed `datallowconn=false` and limit zero. If unconfirmed, no success claim, explicit containment diagnostic. Preserve primary error and cleanup error evidence. |

The repeatable artifact must bind source revision and dirty/source-inventory hash, migrations, base manifest/receipt, overlay DDL/effective grants, scope/role attributes, transaction settings, exact recovered witnesses, denied-operation observations, before/after images, egress sink count, measured elapsed time and final quarantine. It contains neither tokens, connection strings nor original contents. Custody/configuration checks are individually run/not-run; balanced totals do not establish company completeness, zero VAT or production recovery objectives.

## Synthesis decision

Reserved for root comparison with candidate A. Candidate B has not been selected or implemented.

## Tradeoffs accepted

- Accept extraction of a small set of existing read projections in exchange for preserving ordinary admission wrappers and avoiding recovery flags across every owner.
- Accept a target-only, independently verified restriction overlay in exchange for database-enforced book scope, rather than merely filtering application requests while granting unrestricted table reads.
- Accept one bounded inspection command rather than a general recovery browsing API in exchange for complete, reviewable closure proof and a small public surface.
- Accept separate base and overlay schema witnesses in exchange for truthful restricted-role proof; a changed final schema cannot be mislabeled a source match.

## Alternatives considered

**Injected authority/read context into every ordinary owner.** It hides transaction/admission selection but exposes recovery state throughout otherwise ordinary routes and risks accidental propagation to writers. It can reduce extraction when many owners already use a common context; root should compare that advantage against the exact source-retention/receipt locks and restricted dispatch burden. Candidate B confines inspection policy to one owner and shares only owned read interpretation.

**Maintenance-role reads or an ordinary Worker with restored sessions.** These hide little policy and fail restricted-role/authority proof. They cannot serve as the acceptance surface.

**Application-only book scope with SELECT grants on the whole restored database.** This has a smaller overlay but leaks selected-book authority when the same role makes a direct query. It fails candidate B's direct cross-book denial expectation and is not silently substituted if RLS/inventory support is difficult.

## Open questions and risks

- Does the frozen native Effect/Drizzle adapter support an explicit read-only repeatable-read transaction without an unsafe SQL cast/escape? Resolve from the installed adapter and a failing isolated E2E first.
- Can the selected Bun/workerd host enforce the required outbound fence while running native PostgreSQL? Resolve with a synthetic denied-egress probe; provider-free composition alone is insufficient.
- Can all needed read tables use the reviewed fixed role/book policy without affecting ordinary runtime semantics or immutable integrity checks? Enumerate the closure before implementing; a missing join/column fails acceptance rather than broadening grants.
- Does removing the overlay restore exact source schema/grants under the current inventory hash? Make cleanup equality explicit; an intentional residual overlay requires its own accurately named witness, never a false source-match claim.

## Next implementation step

After root synthesis, write the independent synthetic failure/E2E contract and restricted-role transaction/egress proof first, then extract only the owned read projections required by that contract.
