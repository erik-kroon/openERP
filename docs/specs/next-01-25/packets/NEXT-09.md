# NEXT-09: Complete Plaid sync windows

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/banking/sync.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/banking/sync.ts` or the existing equivalent owner |
| Pure calculation | Provider page interpretation and complete-generation publication validation |
| Atomic scope | Short claim/page/publication txs. Remote calls occur in the persistent Bun job outside them. |
| Prerequisites | None |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

BANK-local changes only. Run remote synchronization in the ADR 0009 persistent Bun job composition and reuse source-content storage. Do not touch webshop order intake. Official pagination restart behavior is documented in [X01/X02].

## Persistent state

```text
Stream {
  id, book, providerItem, accountFilter, consentId,
  publishedCursor, publicationVersion, currentGeneration?, fence, leaseUntil
}
Generation immutable header {
  id, streamId, baseCursor, basePublicationVersion, attemptNumber
}
GenerationEvent append-only {kind: started|abandoned|completed|published, evidence, time}
Page immutable {
  generationId, ordinal, requestCursor, nextCursor, hasMore,
  rawContentRef, rawDigest, normalizedChangesDigest, recordCount, chainedDigest
}
CandidateChange immutable {generationId, pageOrdinal, recordOrdinal, kind, sourceId, rawLocator}
Publication immutable {
  generationId UNIQUE, streamId, fromVersion UNIQUE per stream,
  baseCursor, finalCursor, pageCount, changeCount, manifestDigest, receiptId
}
Canonical changes = candidate rows JOIN Publication on generationId
```

The publication marker makes a completed generation visible without copying all staged records in the final transaction. Candidate rows are not exposed by ordinary canonical-source readers before that marker exists.

## Lease admission and recovery

```text
claimWindow(scope, streamId, key):
    enter short application tx with current scoped service admission; lock book then stream
    replay prior key first
    require valid current consent and unchanged stream/account mapping
    if another unexpired lease exists: return Busy
    fence += 1
    if incomplete resumable generation exists:
        keep its baseCursor and staged pages; claim new fence
    else:
        create generation(baseCursor=publishedCursor, baseVersion=publicationVersion)
    save claim receipt and lease
```

A claim does not call Plaid. Provider credentials remain in the existing private adapter boundary.

```text
syncWindow(claim):
    loop within explicit page/byte/time bounds:
        renew owned lease or stop
        if exact next page is retained: verify bytes/digest and recover it
        else:
            cursor = last retained.nextCursor or generation.baseCursor
            response = call Plaid /transactions/sync with this stream/account filter
            if TRANSACTIONS_SYNC_MUTATION_DURING_PAGINATION:
                atomically abandon current generation under expected fence
                begin NEW generation at publishedCursor captured for this window
                # Same original base, NOT failed page cursor, empty cursor or 'now'.
                continue subject to bounded backoff/restart budget
            if item limit, auth/consent failure or non-retryable response:
                record failure; do not publish; return precise blocked state
            raw = retain exact HTTP body outside publication transaction
            decoded = parse known schema with exact monetary lexemes
            appendPage(claim, cursor, raw, decoded)
        if lastPage.hasMore == false: return publishGeneration(claim)
    return resumable checkpoint, not an incomplete publication
```

`appendPage` locks the book/stream, checks fence/lease/current generation/expected next ordinal/cursor and retains raw and mapped digests with a receipt. A different raw response for an already saved page conflicts; it cannot overwrite that evidence. Repeated empty polling windows may leave the cursor unchanged when the provider explicitly returns no changes. An unchanged cursor with unexplained changes or an infinite has-more loop is rejected.

```text
publishGeneration(command):
    return withAdmittedPrincipal(serviceAccess, scope, syncPermission, (tx, principal) =>
        lock book then stream
        if prior = CommandDb.replay(tx, principal, command): return prior
        load generation, immutable page manifests and current stream state in bounded queries
        require current domain fence, valid lease and consent
        require publicationVersion == generation.basePublicationVersion
        require publishedCursor == generation.baseCursor
        require contiguous pages, exact cursor chain and terminal hasMore=false
        require acknowledged content manifests and candidate counts/digests agree
        require provider-specific source reduction rules resolved every conflicting update
        publication = SyncDb.insertPublication(tx, completeGenerationManifest)
        SyncDb.advancePublishedCursorAndVersion(tx, stream, generation.finalCursor)
        OutboxDb.insert(tx, publication-derived normalization intent)
        return CommandDb.save(tx, principal, command, publication)
    )
```

If the process dies after commit, receipt recovery answers the outcome. A superseded worker's fence fails. Consent revocation blocks new pages/publication but does not erase old evidence. Do not hold a PostgreSQL connection or transaction while waiting for HTTP/object storage.

Under the clean replacement, do not retain a live per-page SQL workflow for disposable development records. If meaningful prior provider records actually exist, require a reviewed stream baseline/reconciliation decision before starting window mode. Never relabel those prior receipts as complete windows.

## Adversarial traces

```text
G1: page1 saved, page2 saved, page3 mutation => canonical publication count0
G2: restart at C0, pages1..3 complete => one marker and cursorC1
crash after marker before response => same command returns marker receipt
old fence publishes after new claimant => refusal, cursor unchanged
no changes at C1 => no false claim that historical bank coverage is complete
```

No live Plaid behavior or storage durability was exercised by this design.

### Queue versus stream ownership

Use effect-mq for scheduling, queue claims, heartbeat and retry history. The stream generation/fence above remains a domain publication contract because a late remote response must not publish over a newer cursor even if an old handler is still running. Queue claim loss alone does not prove that handler stopped. Job payloads contain stream/generation references and expected domain versions, not credentials. A resumed handler reads retained pages and domain receipts before fetching. The outbox is committed with publication; queue enqueue is performed later, not inside the publication transaction.
