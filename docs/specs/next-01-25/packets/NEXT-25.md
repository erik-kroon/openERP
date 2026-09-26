# NEXT-25: Fixed-revision company rehearsal and restore

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/operations/rehearsal.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/operations/recovery.ts` or the existing equivalent owner |
| Pure calculation | Applicable acceptance inventory and independent conservation checks |
| Atomic scope | Exercise the actual application boundary; native backup uses a consistent snapshot and external quarantine. |
| Prerequisites | None |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Root/integrator owns this packet. It consumes the five WIP owners' proof without taking over qualification. This is pseudocode for a controlled exercise, not authorization to use actual data, run forbidden tests, deploy, pay or file.

## Acceptance ledger

```text
Checkpoint {
  repositoryCommit, dirtyTreeDigest, sourceFileHashes,
  baselineSchemaManifest, installedMigrationManifest, narrowIntegrityHashes,
  applicationOperationAndCompilerVersions, grantedTableColumnMatrix,
  dependencyVersions, runtimeAndDatabaseVersions,
  permittedDataScope, externalEgressPolicy, writerEpoch,
  ownerHandoffs: [{packet, sourceDigest, observedAssertions, evidenceRefs, limits}]
}
AcceptanceRow {
  scope, requiredBehavior, applicable: yes|no_with_evidence|unknown,
  implementedRevision?, observedEvidence?, qualificationLevel,
  blockers, responsibleOwner
}
```

A successful old observation is reusable only for the exact asserted contract and unchanged relevant code/runtime state. Unrelated changes need not invalidate every proof, but do not merge separate old passing fragments into a claimed current end-to-end run without exercising its connections.

## Source and permission preflight

```text
captureCheckpoint():
    read current repository instructions, source status and live owner claims
    hash committed+dirty source without displaying credentials or private input contents
    reserve one integration checkpoint; do not mutate active WIP files
    identify the reviewed clean baseline and exact current source/baseline checksums
    refuse a mismatching/old installation without modifying it
    require separately confirmed disposal authority before resetting any development database
    verify no old operation dispatcher, feature-function fallback or alternate live writer remains
    compare application operation, compiler and job handler versions with retained plans
    verify effective table/column grants and narrow integrity match the selected baseline
    load WIP accepted handoffs; mark missing integrations waiting, not failed-complete
    record test/runtime/data permissions actually granted

buildApplicableAcceptance(company):
    require evidenced legal/fiscal/source inventory
    for each required family:
        select relevant packet behavior and independent control requirements
    keep unknown applicability blocked
    keep no-payroll evidence separate from unfinished payroll product work
```

## Rehearse one real period on an authorized copy

```text
rehearsePeriod(checkpoint, authorizedCopy):
    verify clone is isolated, non-delivering and uses intended profile/data class
    inventory actual source accounts, prior postings, matched documents and declarations
    preserve existing matches and original source/economic identity
    run source import in preview; reconcile counts and independent totals
    prepare supported domain operations using NEXT-16 or manual equivalent
    obtain explicit approvals within permitted isolated environment
    execute and retain named receipts
    reconcile every applicable bank/tax/owner/AP/AR/asset control independently
    create statement snapshots and required review/export artifacts
    check journal totals and source lineage independently of UI status flags
    retain unresolved and unsupported items, never create mystery balancing entries
```

The actual exercise runs only when authorized. Without actual data or permission, run a separately labeled synthetic rehearsal if allowed and keep company acceptance open. Passing schemas/builds is not a substitute for this financial observation.

## Consistent backup of database plus objects

```text
captureBackup():
    acquire operator backup/migration lease; block destructive object deletion
    open consistent database snapshot with an exported snapshot token
    from SAME snapshot:
        capture schema/migration/role manifests and installed app semantic versions
        enumerate every referenced evidence/artifact object and immutable version/hash/size
        enumerate rule/profile/mapping releases, receipts and required supplementary files
        enumerate application outbox, business job progress/cancellation and effect-mq store inventory
    databaseDump = dump using that same snapshot while snapshot owner remains alive
    copy every referenced immutable object version and verify hash/size
    capture permitted config/secret REFERENCES, not unprotected reusable live credentials
    verify no dangling required references and every inventory family has a handler
    persist signed/hashed backup manifest only after all required members verified
    release snapshot and deletion lease
```

`pg_dump` orchestration belongs to the native maintenance boundary, not a Cloudflare request. A timestamp-named dump plus a later live object listing is not a consistent backup. If a store cannot provide immutable versions, copy under a fence that prevents relevant content changes until verified.

## Restore into quarantine

```text
restoreAndInspect(backup, destination):
    require fresh isolated destination and explicit operator authorization
    set external network/credential/writer fences OUTSIDE restored database
    verify archive path safety, manifest signatures/hashes and all required members
    restore database, immutable objects and required release data
    keep restored tokens/instructions unable to send requests or activate old writer authority
    provision a separate read-only inspection identity through controlled setup
    compare schema/migration hashes, entity counts, per-book ledger boundaries,
            exact balances, receipts, object hashes and artifact bytes with manifest
    run permitted historical receipt/statement reads
    require reads create no postings or external effects
    emit restore-verification artifact with exact passed/failed/unavailable assertions
```

A restored `writerEnabled` database field cannot override the external quarantine fence. The restored effect-mq worker and outbox relay remain stopped/fenced until a separate authorized recovery step. Queue rows cannot resume bank/payment/filing delivery merely because they were restored. Production promotion is a separate authority transfer with physical old-writer/egress fencing, not part of this rehearsal.

## Failure exits

```text
missing original object -> backup incomplete; no successful restore certificate
migration drift -> stop before modifying destination; preserve diagnostic manifest
independent control differs -> retain difference; no balancing plug
response lost after domain execution -> recover original receipt, never new-key duplicate
restored provider job tries to dispatch -> external fence denies; record proof
missing WIP handoff -> wait at that integration, continue disjoint approved work
```

Final artifact names the selected period, source coverage, implementation revision, environments, original/restore totals, actually performed checks and remaining facts/approvals. Financial completeness, backup recoverability and external acceptance remain separate claims.

## Application-owned release observations

```text
qualifyReplacement(checkpoint):
    enumerate every REST/MCP/UI/job/script entrypoint and its named application owner
    verify all nested persistence receives the same tx for each owned financial group
    examine actual baseline: no feature workflow, authorization or tax calculator in SQL
    exercise permitted same-key, new-key duplicate, stale approval and competing capacity cases
    inject authorized failure between each financial/register/receipt persistence phase
    observe rollback or original committed receipt, never a half-complete group
    compare pure expected financial effects with persisted journals/registers
    run API Worker path and persistent Bun job path against the same domain contracts
    exercise outbox enqueue/ack loss and queue redelivery against durable application identity
    inspect sanitized failure outcomes without leaking private credentials or source content
```

Queue-library behavior, application business identity and external provider acceptance are separate observations. Pure examples or an intact three-file baseline do not establish any of them. No tests, database, source reset or deployment are executed merely by delivering this specification.
