# Recovery candidate A

Status. Proposed design only. No application code, grants, policies, migrations, credentials, runtime checks or company data changed. Grounding follows the supplied recovery-grounding.md and source read in this session. Rebind this proposal to the frozen baseline before implementation.

## Problem

The operator needs to inspect a restored book through its real application read owners and receive a recovery receipt. Normal admission locks credentials or sessions, identity admission, membership and book rows. PostgreSQL rejects those locking reads in a read-only transaction. A different book lock alone cannot fix this. The existing restore preserves database and object closure but leaves applicationRecovery blocked. The runtime role has financial, authentication and queue writes, so lending that role to recovery does not establish restricted inspection.

The proposed boundary authorizes a fresh inspection identity against immutable restored authority. It does not revive a restored browser session or API token. Existing live admission and authority locks remain unchanged.

## Usage

The proposed CLI accepts the existing restored-bundle identity, a private inspection authorization and a bounded request list. The authorization names the destination cluster/database, manifest digest, one entity/book, the captured operator authority being inspected, expiry and approved read families. The operator receives one application-inspection receipt only after the final quarantine check. The CLI coordinates provisioning, native Effect reads, independent comparisons and cleanup behind one operation.

```ts
const receipt = yield* inspectRestoredBook({
	manifestSha256,
	restoreReceiptPath,
	authorizationPath,
	requests: [
		{ kind: "original", occurrenceId },
		{ kind: "evidence", evidenceId },
		{ kind: "executionReceipt", key },
		{ kind: "savedReport", reportId },
		{ kind: "correctionBundle", bundleId },
	],
	outputDirectory,
});
```

Inside the restricted host, the dispatch registry selects the existing owner port. The caller cannot provide a token, database transaction, authority mode or arbitrary capability name.

```ts
const evidence = yield* Posting.readEvidenceInContext(context, { evidenceId });
const original = yield* Sources.readOriginalInContext(context, { occurrenceId });
const lines = yield* Reports.readSavedLinesInContext(context, { reportId, after });
```

These are proposed signatures. Their bodies are not implemented. Each owner retains its decoding, digest, lineage and object-integrity decisions. The recovery executor owns scope, inspection authority, transaction mode and command admission.

## Shape

The public input is a discriminated request union. Derive its identifier and result types from existing contracts. Do not duplicate the evidence, source, report, receipt or correction record schemas.

```ts
type InspectionRequest =
	| { readonly kind: "original"; readonly occurrenceId: OccurrenceId }
	| { readonly kind: "evidence"; readonly evidenceId: EvidenceId }
	| { readonly kind: "executionReceipt"; readonly key: CommandKey }
	| { readonly kind: "savedReport"; readonly reportId: ReportId }
	| { readonly kind: "savedReportLines"; readonly reportId: ReportId; readonly after?: AccountId }
	| { readonly kind: "savedReportExplanation"; readonly reportId: ReportId; readonly lineId: AccountId; readonly after?: ContributionCursor }
	| { readonly kind: "correctionBundle"; readonly bundleId: BundleId }
	| { readonly kind: "correctionChain"; readonly voucherId: VoucherId };

type ReadExecutionContext = LiveReadContext | RecoveryReadContext;

type RecoveryReadContext = {
	readonly kind: "recoveryInspection";
	readonly authority: ImmutableRecoveryAuthority;
	readonly scope: Scope;
	readonly database: ReadOnlyDatabase;
	readonly originals: VerifiedRecoveredObjectStore;
};

type ImmutableRecoveryAuthority = {
	readonly inspectionId: InspectionId;
	readonly manifestSha256: ManifestDigest;
	readonly restoreReceiptSha256: RestoreReceiptDigest;
	readonly destination: VerifiedDestination;
	readonly operatorAuthority: CapturedOperatorAuthority;
	readonly permittedReads: NonEmptyReadonlyArray<InspectionRequest["kind"]>;
	readonly expiresAt: Expiry;
	readonly overlaySha256: InspectionOverlayDigest;
};
```

These opaque types have private constructors at the CLI/runtime boundary. No wire input can construct a RecoveryReadContext. A recovery identity never becomes VerifiedPrincipal by a cast. A LiveReadContext is constructed after the existing locked admission. A RecoveryReadContext is constructed after inspection authorization, retained authority, database identity and closure checks. Both expose the same transaction-bound owned read functions. Neither exposes financial methods. This choice follows Model the Domain and Type System Discipline.

The explicit registry admits only the request union. It owns the complete grant/read dependency list for each selected owner, including every table an existing access check expects. It does not infer safety from HTTP GET, operatorOnly=false, lockMode=share, or a function name. prepareReport writes a snapshot and remains excluded. This choice follows Boundary Discipline.

ReadOnlyDatabase opens a native Effect/Drizzle repeatable-read transaction and sets it read-only before any application query. PostgreSQL session state must independently report transaction_read_only=on and transaction_isolation=repeatable read. The current withTransaction has no such configuration. The exact adapter API must be verified in the frozen checkout before implementation. Do not invent a Drizzle option or replace the repository adapter with Promise accounting queries.

## Exact source seams

| Existing seam | Proposed change and evidence |
| --- | --- |
| application/identity.ts withAdmittedPrincipal and withVerifiedPrincipal | Leave their existing live paths unchanged. db/identity.ts lockCredential, lockSession, lockAdmission and lockMembership all use for("share"). lockBook also uses share or update. A separate recovery executor constructs inspection authority without passing through those live functions. |
| db/transaction.ts and db/connection.ts | Add a narrow read-only acquisition/transaction owner. Keep Database and ordinary withTransaction behavior intact. The recovery host acquires only the temporary inspection login. No ordinary API Worker, Better Auth, preparation queue or provider adapter is composed. |
| application/posting.ts getEvidence and getReceipt | Extract their owned decode/read body into transaction-bound read ports reused by the live wrappers. Live wrappers keep Db.lockBookForShare. Recovery uses the already verified immutable book context. getReceipt remains limited to execute_change. db/posting.ts readCommandReceipt currently ignores its _lock argument and performs an ordinary SELECT. Do not claim that query needs lock removal. |
| application/source-retention.ts readOccurrenceView/getSourceOccurrence | Reuse retained metadata, requireRetentionAccess, readStorage and readRetainedObject. Live entrypoints retain both authority checks and lockBookForShare. Recovery reads the same immutable metadata before and after the object read and verifies the same size/hash. Its object adapter additionally admits only manifest-listed objects for the selected book. |
| application/reports.ts getReport/reportLines/reportExplanation | Reuse saved snapshot decode, pagination and fixed-cutoff contribution queries. requireReportAccess(false) checks SELECT on Db.reportTables. Include those actual dependencies in the restricted grant set. Do not call prepareReport, prepareReportFamily or recalculate a missing saved snapshot. |
| application/posting-corrections.ts getCorrectionBundle/getCorrectionChain | Reuse readBundleView, validateBundle, validateBundleRow, bundleView and correctionChain. Live wrappers retain Db.lockBookForShare. Grant the actual read dependencies needed for the retained original/reversal/replacement and approval currentness. Never expose approve or execute. Recovery results are inspection observations, not executable approval authority. |
| scripts/operations/workflows.ts restore finalizer | Keep the existing restore success receipt and its blocked applicationRecovery literal. Add a separate inspection procedure and receipt rather than retroactively changing old restore receipts. The new procedure ends with NOT datallowconn and datconnlimit=0, exactly as the existing finalizer checks. |
| contracts/operations.ts | Add a distinct application-inspection receipt schema. Retain version-2 RestoreReceipt interpretation. Bind the source release, migrations, original restore receipt, authority/overlay witnesses, read result hashes, independent controls and final quarantine. writerPromotion stays not-performed and resumeAllowed stays false. |

## Database restriction and immutable authority

Application scoping alone cannot protect another book from direct SQL by the inspection login. Candidate A therefore requires a reviewed, temporary database inspection overlay on the restored destination. This is a material extension to the current inventory contract, not a change to the accounting baseline.

1. Verify the unmodified destination tables, schema, migrations, role inventory and recovered objects against the restore receipt while all ordinary connections remain fenced.
2. Create a fresh expiring LOGIN with no role membership, no superuser, no database/role creation, no replication, no BYPASSRLS and no ability to SET ROLE to a privileged role. It is not a member of openerp_runtime. Never export its credential in receipts.
3. Grant CONNECT only to this identity. Verify effective CONNECT privileges for every ordinary runtime/provider login and PUBLIC remain absent. Open at most the bounded inspection connection capacity. Existing zero connection capacity cannot admit a non-superuser. Capture this exact temporary change and refuse any unexpected existing session. Authorized maintenance superusers remain outside the restricted-login threat model and must not mutate the inspection destination.
4. Grant schema USAGE and SELECT only on the reviewed owner dependencies. Grant no auth session/account/rate-limit access, queue tables, sequences, CREATE, DML or unneeded executable functions. Grant canonical/digest only if the selected existing owner actually needs them. Verify effective privileges including inherited PUBLIC privileges.
5. Add role-specific, SELECT-only RLS policies with fixed reviewed predicates for the one restored book. Tables with book_id use its literal identity. books uses the exact entity/id pair. Global actor/admission rows are visible only when tied to retained memberships in that book and needed for the approved read. Any table without a reviewed ownership predicate refuses the profile. No mutable session tenant variable is used. The role cannot change policies or their bound scope.
6. Treat the overlay as an explicit enumerated schema/grant delta. Current inventory.ts refuses RLS. Add a destination-inspection verifier for this exact overlay, not a general exemption from inventory. Preserve the original restored schema fingerprint as a separate witness. No new policy may enter a backup source or be accepted by ordinary restore inventory.
7. Before each read transaction, verify destination identity, role, immutable authority, authorization expiry and transaction modes. Capture operator enabled/membership evidence using plain SELECT against the frozen restored snapshot. Missing membership and disabled admission refuse. Preserve the existing meaning that absent identityAdmissions is not an explicit disable. The new external inspection identity is not proof that a historical credential is currently valid.
8. Close all inspection connections, revoke CONNECT, set the inspection role NOLOGIN, remove only the recorded overlay, and confirm the original restored schema/grants and full table/queue/object fingerprints. Finish with database connections disabled and capacity zero. If cleanup or quarantine cannot be proved, emit a failed diagnostic, never a successful inspection receipt.

The repeated closure checks plus fenced writers make the captured authority immutable for inspection. Repeatable-read alone does not prove database immutability. A restarted or retried inspection revalidates the manifest and restored state and uses fresh bounded inspection authority. It never replays a financial command.

## Synthesis decision

Pending parent synthesis. This is candidate A only. It has not won against the other candidate and is not implementation authority. The alternative below provides a structurally different comparison, per Exhaust the Design Space.

## Tradeoffs accepted

- We accept small read-port extractions in the existing owners in exchange for retaining their actual decoders, lineage, pagination and corruption refusals. The recovery registry concentrates admission instead of adding ambient recovery branches to every withBook call.
- We accept a temporary destination-only RLS/grant overlay in exchange for proving direct-SQL book isolation. Its exact-delta verification and removal add work. A global policy exception would invalidate this choice.
- We accept captured operator authority plus fresh inspection authorization in exchange for keeping restored sessions inactive. This proves recovery inspection, not live-session restoration or continuing production authority.
- We accept a limited saved-report/read family in exchange for complete proof. Unsupported owned receipt families remain explicitly outside the first inspection profile. getReceipt's execute_change limit remains visible.
- We accept a separate application-inspection receipt in exchange for preserving existing restore contracts and historical blocked receipts.

## Alternatives considered

A dedicated recovery application owner could accept the same request union and directly implement its own scoped reads and decoding over restored tables. Its public interface is equally small and its admission is easier to isolate. It loses if it copies report, correction and original-integrity policy. A variant that calls shared owner read ports converges on candidate A but adds a central policy owner without new domain knowledge. Parent synthesis may prefer the dedicated owner if it can reuse the same owned cores without enlarging the interface.

Passing an ambient recovery service through ordinary withAdmittedPrincipal was rejected. Share mode is not a safe read marker, selected owners lock the book again, and source originals re-enter admission. The service could unintentionally admit newly added writes unless every operation learned recovery policy. Direct-SQL backup comparisons were rejected as application proof because they do not exercise the real owners.

## Independent failures and E2E expectations before code

Use synthetic fixtures and a disposable PostgreSQL 17 cluster. Establish all literal expected accounting values and refusal outcomes before implementing the executor. Existing recovery.recovery.test.ts and restore-host.ts are the nearest proof owners. Their current ordinary runtime login/destination Worker does not qualify this profile. The default suite includes only *.e2e.test.ts, so either add a scoped recovery.e2e.test.ts or explicitly add a separate bounded recovery gate. Do not silently leave the decisive test unselected.

| Scenario | Independent expectation |
| --- | --- |
| Originals/evidence | A fixed original byte string returns byte-for-byte after restore, with independently calculated SHA-256 and length. The evidence record and selected-book source link match literal fixture identities. Object access to another book is refused even when the key is known. |
| Financial receipt | Post one independently specified 12500-minor-unit debit/credit group through normal source owners before backup. Restore inspection returns its exact retained execute_change receipt, voucher identity and amounts. No new voucher, counter or receipt appears. Unsupported operation receipts return the existing NotFound boundary. |
| Saved report/correction | Prepare the saved report and an approved correction through normal source owners before capture. Pin literal original, reversal and replacement amounts. Inspect saved headers, all pages, contributing vouchers and retained correction receipt. Do not compute expected totals with the report function under test. Compare expected digests/relationships independently. |
| Scope and identity | Other entity, book, destination, manifest, operator mapping, unknown read kind and expired inspection authorization refuse. Disabled captured operator or absent required membership refuse. Restored browser/API credentials never authorize the recovery host. Direct SQL sees no rows from the other restored book. |
| Actual transaction restriction | Every application transaction reports read-only and repeatable-read under the dedicated non-superuser role. Direct INSERT/UPDATE/DELETE, sequence changes, DDL, SELECT FOR SHARE/UPDATE and attempted read-write mode followed by a write fail. The inspection role cannot gain runtime membership or change its RLS scope. |
| Application mutations | Journal prepare/approve/execute, correction prepare/approve/execute, report prepare, source retain and arbitrary capability dispatch refuse before owner invocation. Probe DB permissions independently, so a registry-only refusal does not conceal a writable role. |
| Auth/queue/provider | Better Auth mutation routes and restored sessions are absent. Direct auth and effect-mq table access/writes refuse. No outbox claim, preparation runner, provider request, writer activation or external callback occurs. Full queue state/sequence fingerprints match the pre-inspection image. |
| Corruption | Independently altered original bytes, size metadata, evidence linkage, saved report digest, bundle/voucher linkage or closure/migration/role witnesses prevent success. A missing page/reference is not treated as zero. Keep diagnostics and final quarantine observations. |
| Replay and interruption | Repeat the inspection after response loss and restart. Owned returned records and comparison hashes match, while the financial/auth/queue image remains unchanged. Interrupt during object retrieval and during final cleanup. A partial read never yields a success receipt. Cleanup restores quarantine or reports not-confirmed explicitly. |
| Final quarantine | Observe no inspection session, no ordinary runtime/provider CONNECT, inspection identity disabled, overlay removed, original schema/grants matched, all durable table/sequence/object fingerprints unchanged, NOT datallowconn and datconnlimit=0. A finalizer failure cannot be relabeled as a successful inspection. |

Retain a verifiable artifact with manifest.json, source-integrity.json, independently specified expected.json, sanitized owner-results.json, privilege-denials.json, transaction-modes.json, before/after closure controls, overlay identity/removal controls, quarantine.json and application-inspection-receipt.json. Record revision, dirty-source hash, lockfile, migration identity, PostgreSQL/Bun versions, selected cases, first failures, replay command and cleanup result. Store credentials and session data outside the artifact. The owner can rerun the declared bounded E2E command against isolated synthetic targets.

## Open questions and risks

- Does parent synthesis accept the temporary destination-only RLS overlay, or does another candidate achieve equally strong direct-SQL book isolation with less schema work? Application-only scoping is insufficient for this candidate's isolation claim.
- Which exact frozen-baseline report and correction dependency tables require global identity visibility? Audit their current read graphs before deriving role policies. Unknown dependencies must block admission rather than broaden grants.
- Does the native Drizzle/Effect version provide transaction mode/isolation options, or must the owner issue SET TRANSACTION immediately after BEGIN? The required observed PostgreSQL state is settled. The adapter spelling is not.
- How does the private operator authorization authenticate the fresh inspection grant? operatorId in the current RecoveryPlan is explicitly only a declaration. It cannot silently become authentication.

## Next implementation step

After synthesis, write the independent E2E failure fixture and authorization/grant dependency matrix, then implement the scoped executor and extract only the selected owned read ports in an isolated worktree.

## Evidence read

- apps/api/src/db/identity.ts and application/identity.ts define the locked live admission.
- apps/api/src/db/transaction.ts and db/connection.ts define current native acquisition with no recovery mode.
- application/posting.ts, source-retention.ts, reports.ts and posting-corrections.ts contain the selected owner bodies and redundant book locks.
- db/posting.ts shows readCommandReceipt is currently an ordinary SELECT despite its _lock parameter.
- scripts/operations/workflows.ts creates the restricted database and confirms final quarantine. contracts/operations.ts retains the blocked literal.
- migrations/0003-roles.sql exposes runtime financial/auth/queue writes. That role is unsuitable for inspection.
- tests/assurance/excellence/recovery.recovery.test.ts and restore-host.ts provide the existing recovery exercise and real Effect owner host.
- docs/operations/local-recovery.md and application-recovery.md distinguish maintenance closure, restricted application proof and production custody.

Prove It Works changed the acceptance gate to actual restricted owner reads and independently observed final quarantine. Model the Domain and Type System Discipline changed the public shape to a finite request union with privately constructed inspection authority. Boundary Discipline moved admission into one executor. Exhaust the Design Space requires parent comparison with the dedicated-owner alternative before implementation. Sequence Work into Verifiable Units keeps this design, the failure fixture, the implementation and fixed-source runtime proof as separate gates.
