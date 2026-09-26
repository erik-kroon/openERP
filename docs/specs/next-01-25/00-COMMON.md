# Shared Effect application-owned pseudocode conventions

Edition: **v2, replacement of the complete NEXT-01 through NEXT-25 dossier**.

Status: proposed implementation-level pseudocode. Symbols below specify contracts, not compilable TypeScript, implemented exports or a generic financial interpreter. This edition incorporates the supplied application-ownership amendment based on ADR 0010 and ADR 0009 at `422276ae5ed9d0ca146447d92bb3d27c99f8c48a`. The original task/source baseline was `bb628452196a55ceef7516f76fc3cd6471ae4d91`. No fresh repository or regulatory audit was performed for this rewrite. Reconcile current source and active owner claims before implementation.

## Ownership and notation

The application process owns policy, current authorization, calculation, workflow and scoped DML. PostgreSQL stores authoritative records and provides transactions, row locks, references, uniqueness and narrow integrity checks. It does not independently prove human approval or correct tax classification once the trusted application has scoped write grants.

`...Db.method(tx, ...)` means a bounded parameterized query or DML operation on the supplied transaction. `...Domain.compile(...)` means a pure calculation over decoded values. `...App.operation(...)` means a named Effect application service. These namespaces describe responsibility; adapt names to existing modules rather than making a file or interface for every helper.

Public operations open a transaction when required. Internal `applyWithinTransaction(tx, ...)` functions NEVER acquire a new database connection, start a runtime, call HTTP or independently commit. SQL aggregation remains appropriate for selecting and summarizing persisted facts. Readiness, treatment choice and business admission belong in the application.

## C1. Wire values and exact arithmetic

```text
MinorString := canonical decimal integer string, bounded by its existing codec
PositiveMinor := MinorString > 0
SignedMinor := canonical signed aggregate integer string, never IEEE floating point
Money := {currency: ISOCode, scale: integer, minor: MinorString}
Rational := {numerator: bigint, denominator: positive bigint}
AccountingDate := real local calendar date, not an implicitly UTC timestamp
RecordedAt := timestamp assigned by the committing authority

assertSameMoneyUnit(a, b):
    require a.currency == b.currency AND a.scale == b.scale

# Policy is explicit. Signed half-up here means nearest, ties away from zero.
roundRational(n, d, mode):
    require d > 0
    s = sign(n); a = abs(n); q = a div d; r = a mod d
    if mode == exact: require r == 0; return s*q
    if mode == toward_zero: return s*q
    if mode == floor: return floor_div(n, d)
    if mode == half_up: return s*(q + (2*r >= d ? 1 : 0))
    if mode == half_even: return s*(q + (2*r > d OR (2*r == d AND q odd) ? 1 : 0))
    fail UnsupportedRounding

convertMinor(sourceMinor, sourceScale, targetScale, majorUnitRate, policy):
    n = sourceMinor * majorUnitRate.numerator * 10^targetScale
    d = majorUnitRate.denominator * 10^sourceScale
    y = roundRational(n, d, policy)
    requireWithinCodec(y)
    return {minor: y, exactNumerator: n, denominator: d, residualNumerator: n-y*d}

# Used for deduction release, not as a replacement for the WIP FX allocation owner.
cumulativeRelease(originalCapacity, totalBasis, consumedBefore, consumeNow, rounding):
    require 0 <= consumedBefore <= totalBasis
    require 0 <= consumeNow <= totalBasis-consumedBefore
    if totalBasis == 0: require consumeNow == 0; return 0
    releasedBefore = roundRational(originalCapacity*consumedBefore, totalBasis, rounding)
    consumedAfter = consumedBefore+consumeNow
    releasedAfter = originalCapacity if consumedAfter == totalBasis else
                    roundRational(originalCapacity*consumedAfter, totalBasis, rounding)
    return releasedAfter-releasedBefore

# A finite integer schedule, not a new depreciation-method selector.
allocateByWeights(total, [{stableId, positiveWeight}], remainderPolicy):
    require total >= 0 AND all weights > 0 AND ids unique AND nonempty weights
    require remainderPolicy == largest_remainder_stable_id_v1
    W = sum(weights)
    floorShare[id] = (total*weight[id]) div W
    remainder[id] = (total*weight[id]) mod W
    left = total-sum(floorShare)
    order = descending remainder, then stableId in specified byte ordering
    add 1 to first left shares
    require sum(shares) == total
    return shares with policy/version and input weights
```

Rates, currency scales and tax policies are selected from qualified inputs, not guessed by these helpers. Negative credit amounts keep the sign of their economic correction. A bound failure is an error, not truncation or saturation.

```text
Journal.addSigned(accountRole, x, metadata):
    if x == 0: return  # Never manufacture a zero-valued line.
    append {
      accountId: resolvedRoleAccount,
      debitMinor: max(x,0).toString(),
      creditMinor: max(-x,0).toString(),
      metadata
    }
Journal.finish():
    require sum(debitMinor-creditMinor) == 0
    require every line has exactly one positive side
    preserve line identity, tax component, dimensions and source links
    # Do not merge lines just because their account IDs happen to match.
```

## C2. Evidence and economic identity

```text
Content      := {sha256, byteLength, mediaType, storageVersion}
Occurrence   := {book, sourceSystem, providerStream?, sourceId, sourceRevision, contentRef, locator}
EconomicKey  := {book, eventOwner, stableExternalOrReviewedIdentity}
Recognition  := {economicKey, sourceRevision, operationId, journalRefs, taxFactRefs, obligationRefs}
```

Content deduplication does not deduplicate business events. A revised document is not automatically another purchase. Multiple systems can retain evidence about one recognized event. Only an explicit economic relationship allows adoption of an existing recognition. Recognition identity is enforced in both owner-specific and generic admission paths. Do not introduce a universal ban on reusing evidence or a journal line for all purposes: bank reconciliation and subledger evidence may legitimately reference the same underlying posting.

## C3. Frozen input and approval contracts

```text
Dependency := {
    owner, resourceId, version, scope,
    semanticKind: row_revision | membership_epoch | eligibility_epoch | rule_release
}
CapturedBasis := {
    book, entity, recordedCutoff, ledgerBoundary,
    exactSourceRevisions, relevantConfiguration, dependencies,
    completeMembership: [{identity, revision}], completenessStatus
}
Prepared<DomainPlan> := {
    planId, schemaVersion, canonicalizationVersion,
    owner, inputDigest, basis, payload: DomainPlan,
    digest, createdBy, createdAt
}
Approval := {
    id, planId, digest, exactScope, approver,
    expiresAt, independentReviewerRequirement?, explicitBatchMember?
}
Receipt := {
    id, ownerOperation, planId, digest, economicIdentity,
    committedAt, journalIds, domainEffectIds, noFinancialEffect: boolean
}
```

`sealPlan` persists the whole computed proposal once. It rejects extra unsupported fields and stale dependencies. It does not recalculate a different plan at execution. Use the selected canonicalization contract and record its version. Any meaningful retained plan keeps its interpretation; do not build a compatibility runtime for disposable pre-release fixtures.

Eligibility and population are different dependencies. An independent purchase depends on its source, accounts, policy and posting eligibility. A VAT return also depends on all relevant taxable facts and control movements, including the epoch for an initially empty population. Do not depend every ordinary purchase on the global book sequence.

Changes to applicable rules or dates produce a fresh proposal and approval. Changes in irrelevant future facts need not invalidate the plan. New backdated relevant data increments the affected scope's population epoch even when its accounting date is old.

## C4. Preparation, approval and set-based capture

Decode input at the shared application boundary so REST, MCP and jobs cannot obtain different semantics. Decode persisted JSON once into owned schemas. Do not carry untyped JSON-field plumbing through the domain.

```text
prepareNamed(command) = named Effect application operation:
    capturedOrReplay = withAdmittedPrincipal(access, scope, preparePermission, (tx, principal) =>
        lock book using the capture/read protocol
        existing = CommandDb.replay(tx, principal, completeCommandIdentity)
        if existing: return Replayed(existing)
        basis = DomainDb.captureCompleteBasis(tx, selection)
        require complete requested membership or return an explicit scope limit
        return Captured(basis)
    )
    if Replayed: return its saved result

    proposal = Domain.compile(capturedBasis, command.reviewedInput)
        # Pure. No database/network access and no caller-supplied calculated effects.
    require no unresolved mandatory decision

    return withAdmittedPrincipal(access, scope, preparePermission, (tx, principal) =>
        lock book, then relevant resources in the established order
        existing = CommandDb.replay(tx, principal, completeCommandIdentity)
        if existing: return existing
        current = DomainDb.captureRelevantDependencies(tx, selection)
        require current agrees with capturedBasis
        require semantic compiler/rule versions supported
        plan = sealExactTypedPlan(proposal, basis, versions, canonicalization)
        PlanDb.insert(tx, plan)
        return CommandDb.save(tx, principal, completeCommandIdentity, plan)
    )
```

Capture uses one consistent database snapshot or the shared book barrier with all writers obeying that protocol. Large fixed populations must be materialized consistently before paging outside the capture. A small bounded operation can calculate and seal inside one short transaction instead of adding extra stages. Never perform model inference, provider calls, rendering or human waits while financial locks are held.

Use set-based loads over distinct selected IDs. Load each capacity once, validate repeated references for consistency and aggregate requested consumption separately. Do not multiply usage by joining it against repeated request legs. Candidate counts and rankings belong to discovery, not an exact allocation's financial dependency basis.

```text
approveNamed(command) = named human/operator Effect operation:
    withAdmittedPrincipal(access, scope, approvalPermission, (tx, principal) =>
        lock book and the declared dependency/approval resources
        replay exact command first
        plan = load exact saved plan and digest
        verify current selected facts, resources and owner-specific approval policy
        require independent reviewer where this operation requires one
        record immutable approval over planId + planDigest + scope + expiry + actor
        save receipt in this same tx
    )
```

Approval does not execute. Rule activation does not mint financial approvals. Multi-plan approval is allowed only through the explicit fixed manifest in NEXT-16.

## C5. One application transaction for one complete owned effect

The template below is an implementation convention for named services, not a stored procedure, arbitrary effect interpreter or external CRUD API.

```text
executeNamed(command) = named Effect application operation:
    decode complete command with the owning contract
    return withAdmittedPrincipal(currentAccess, scope, executePermission, (tx, principal) =>
        # withAdmittedPrincipal owns one actual Drizzle/Effect DB transaction.
        # Requester credential/session/membership admission precedes the book lock.
        book = BookDb.lockWriter(tx, scope)
        prior = CommandDb.replay(tx, principal, {
            scope, key, operationName, targetId, completeTypedInput
        })
        if prior exists: return prior.result

        plan = PlanDb.loadExact(tx, scope, command.planId)
        require plan.digest == command.planDigest
        require plan.owner == namedOwner AND supported version AND matching scope
        require no committed effect already owns this economic identity
        # A new key cannot authorize another posting of the same economic event.

        current = DomainDb.loadSelectedBasisInBatches(tx, plan.selection)
        require current relevant dependencies equal the approved basis
        require eligible periods, accounts and domain resources
        approval = ApprovalApp.validateWithinTransaction(tx, principal, plan, command)
        require exact plan binding, non-revocation, expiry and owner execution policy
        require current authority is concurrency-protected under the global lock protocol
        Domain.assertConservationAndCompleteEffects(plan, current)

        result = applyNamedWithinTransaction(tx, plan, current)
        # Concrete domain DML, including JournalApp.postWithinTransaction when needed.
        # Complete journal + tax + obligation/schedule/capacity consequences, not partial effects.
        ApprovalDb.insertUse(tx, approval, result.operationIdentity)
        ReceiptDb.insert(tx, exact effect references and approved digest)
        OutboxDb.insertRequiredIntents(tx, stable event identities and record references)
        CommandDb.save(tx, principal, completeCommandIdentity, result)
        return result
    )
    # Return success only after the transaction wrapper acknowledges COMMIT.
```

All nested reads/writes receive the caller's `tx`. `applyNamedWithinTransaction` does not call a public `execute*` that opens its own transaction. Its validated input is constructed by trusted application code, not accepted as an arbitrary browser/MCP financial payload.

**Lock discipline:** retain ADR 0010's reviewed global ordering: requester credential/session and executor membership; book writer; relevant periods/accounts; domain resources in stable type/ID order; approval and its authority; counters. Implement approval-member locking through that reviewed protocol, including identities already locked during requester admission. No owner invents a conflicting order or substitutes a plain cached/EXISTS permission check. If the current shared implementation cannot enforce that ordering for a referenced authority, resolve it at the root transaction/identity owner before qualification. Revocation stays authority-only. No cross-book call from inside a held book transaction.

**Replay:** current requester access is still checked. A committed identical command is returned before new-work dependencies, approval expiry or economic-duplicate checks. A different actor/operation/input using the same key conflicts. An expired historical approval or newly changed account cannot erase an already committed result. Discovery of a prior economic receipt never grants a new execution.

**Failure:** let domain failures, SQL failures and interruption cross the transaction boundary. Do not swallow an error after partial DML and return success. A connection loss near commit is outcome unknown, not proof of rollback. Recover through the original scope/key/input. Same-key recovery and distinct business-effect uniqueness both remain necessary.

**No-effect operations:** matching, adoption, activation and resolution can have no journal. A genuinely zero financial plan gets a no-effect domain receipt after its normal checks, not a fake zero voucher or consumed voucher number.

### Journal application primitive

```text
JournalApp.postWithinTransaction(tx, validatedJournalGroup):
    require group was compiled/approved for its owning application operation
    verify complete supported line/effect membership in application code
    validate exact money, one positive side per line and balance
    allocate rollback-safe counter(s) through ordered UPDATE ... RETURNING
    insert journal header(s) with expected immutable line membership/count
    insert exact lines in bounded batches
    retain group identity for complete snapshot boundaries
    return inserted journal/line identities
    # No nested transaction, implicit approval or public arbitrary writer.
```

Public manual posting, imports, corrections, recurring work and domain posting must all enforce their relevant owner restrictions before calling this primitive. A correction cannot execute only its reversal while omitting the replacement/register effects. The application now owns those business admission checks.

### Database integrity that remains

Keep composite book-scoped keys/references, unique command/economic-effect identities, approval-use uniqueness, exact integer bounds, nullability and ordinary row checks. Keep immutable sealed records and posted history, append protection and narrow deferred journal line-count/balance integrity. An aggregate voucher balance is not a row-level CHECK querying other rows.

DDL/indexes and scoped table/column grants stay in PostgreSQL. No feature stored procedure, tax/payroll/FX calculator, approval lifecycle or second business state machine is introduced. Cross-record financial capacity rules live in the owning application service and depend on every competing writer following the same resource/book-lock protocol. The SQL layer is deliberately not a shadow implementation of those policies.

### Shared receipt helper used in the packet pseudocode

```text
finishOwnedWithinTransaction(tx, principal, command, plan, result, approval):
    verify result references the exact complete group already written by its named owner
    if this operation requires approval: ApprovalDb.insertUse(tx, approval, result.operationId)
    receipt = ReceiptDb.insert(tx, plan identity + actual effect references + no-effect status)
    CommandDb.save(tx, principal, complete command identity, {result, receipt})
    return {result, receipt}
```

This is a small internal application helper over the caller's transaction. It does not calculate policy, post journals, open a transaction, enqueue jobs or invent additional outbox events. The named operation writes its explicitly required outbox intents once using stable operation/event identities before completion. The enclosing wrapper commits. When an operation has no approval requirement, that is explicit in its typed owner contract, not selected by an arbitrary caller flag.

## C6. Snapshot reads, artifacts and effect-mq delivery

```text
readHistorical(scope, id):
    authorize current read access
    return immutable saved model + separately computed live status
    # No current labels/rates mixed into historical financial values.

readSnapshotPage(scope, snapshotId, cursor):
    verify scope, selection and real saved anchor
    use only retained snapshot membership and full-scope totals
    return next even for an empty filtered page when unscanned members remain

renderArtifact(modelRevision, rendererRelease):
    load the immutable model under current authority
    render exact bytes OUTSIDE any financial transaction
    persist immutable object bytes and verify hash/length/version
    in a short application tx:
        reauthorize and replay exact attachment key
        bind the exact model, renderer and verified object manifest
        persist attachment and receipt
    # Unreferenced bytes after failed attachment do not imply a completed artifact.
```

ADR 0009 selects effect-mq in a separate persistent Bun process. The API Worker never loads its continuous listener. The queue pool's session-preserving listener is not tenant context or a financial lock; authoritative API transactions use their own correct uncached connection path.

```text
financialOperation(tx):
    write domain effects
    insert application outbox intent with immutable event/operation identity
    commit both

outboxRelay():
    claim bounded undispatched outbox rows in a short transaction
    enqueue through effect-mq with stable event-derived identity OUTSIDE that tx
    acknowledge dispatch in a later short transaction
    # A crash after enqueue can duplicate delivery. Domain receipts resolve it.

jobHandler(job):
    establish current scoped service authority, not a user token from the payload
    check run/checkpoint/cancellation versions
    call the same named application operation used by REST/MCP
    recover saved domain receipt on redelivery
    return to effect-mq for queue acknowledgment
```

The library owns queue claims, scheduling, retry history and transport leases. Application records own business progress, financial identity, approval, cancellation versions and receipts. A stream publication fence or owned financial capacity is a domain invariant, not a duplicate general queue runtime. A stale handler may still run after queue claim loss; the application must reject stale domain writes. Queue pruning cannot erase economic idempotency.

External payments and filings have their own attempt identity and unknown-outcome recovery. A queue retry does not make those effects exactly once. No live provider action is authorized by this dossier.

## C7. Reserved application handoff ports

Keep all five original WIP assignments reserved. The old migration numbers identify the user's task boundaries; they are NOT instructions to restore the retired SQL chain. Their owners provide the selected application equivalents.

```text
VatReclassificationApp.readEffectiveWithinTransaction(tx, scope, obligation, cutoff)
VatAmendmentApp.readEffectiveWithinTransaction(tx, scope, obligation, cutoff)
    -> signed per-account vectors, exact component links, receipts and versions
# Invoke each owner's public prepare/approve/execute flow outside another transaction.
# A true larger aggregate needs an explicitly released internal tx-passing port.

FxDomain.planPairedRelease(capturedBasis, orderedPrincipalLegs)
    -> the WIP owner's exact paired consumptions and residuals
FxApp.applyPairedConsumptionWithinTransaction(tx, approvedRelease, journalRefs)
    -> one owned change to original units and book carrying; never a second balance
FxDb.captureSettlementBasis(tx, scope, itemId)
    -> originalRemaining, carryingRemaining, versions and lineage

AssetDb.captureDispositionBasis(tx, scope, assetId, cutoff)
    -> gross, ordinaryAccumulation, impairment, carrying, futureSuffix and lineage
AssetApp.applyDispositionWithinTransaction(tx, validatedDisposition, journalRefs)
    -> same transaction retires future recognition and records disposal
```

Do not requalify VAT-03, reproduce FX-02-P1 partial release, take over AST-03 UI/control closure, build a second VAT-04-A1 delta owner or modify COM-2-W1 webshop/order/catalog authority. Missing ports are exact handoff dependencies. No owner can bypass them by calling a remaining SQL function or opening a second transaction.

## C8. Status and failure vocabulary

Map semantic reasons to the existing public error family. This notation is not permission to rename supported errors.

```text
MissingFact(field, affectedOperations)
UnsupportedProfile(profile, case)
StaleDependency(owner, expected, current)
IdempotencyConflict(existingOperation)
AlreadyApplied(receiptRef)
CapacityExceeded(owner, requested, remaining)
IncompleteScope(missingIdentities, unavailableOwners)
OutcomeUnknown(requestRef, safeRecoveryAction)
ValidationUnavailable(requiredArtifact)
```

Keep design, implemented source, runtime proof, company applicability and provider acceptance separate. Source examples and pure arithmetic checks prove neither a transaction nor a tax profile.

## C9. Clean baseline and retained business data

Under ADR 0010's stated pre-release condition, the application replacement has a reviewed `0001-schema.sql`, `0002-integrity.sql` and `0003-roles.sql` baseline. Do not carry an old-schema adapter, function dispatcher or invented upgrade path for disposable old development data. Reconcile the actual baseline before allocating a schema change; do not revive historical numbered feature migrations.

This is NOT permission to delete meaningful newly retained records. Once the new baseline is released, use forward migrations and preserve existing record meanings. Refuse an unknown/old installation without modifying it. A current operator must establish whether the target is genuinely disposable before any reset.

Importing a company's real previous bookkeeping is a PRODUCT FEATURE, separate from replacing the app's unreleased development schema. NEXT-11/12/25 therefore retain evidence, source identities, historical balances and real external migration requirements.

Semantic algorithm, rule, canonicalization and handler versions belong to sealed plans and job inputs. A newly deployed Worker or Bun handler must understand the exact saved meaning or require a new plan/approval. Schema compatibility alone is insufficient. Existing meaningful historical artifacts are read as history, not silently recalculated.

## C10. Worker integration and qualification

Each packet has a named application owner, a pure compiler where appropriate, tx-passing persistence and its precise complete group. Root integrates shared contracts, capability maps, transaction/identity primitives, baseline integrity/grants and common UI/runtime composition. No domain worker adds raw SQL execution tools or ordinary-agent approval powers.

Before retiring each source path, map every accepted case and refusal to its application owner and remaining structural DB constraint. Exercise same-key replay, different-key duplicate, competing capacity consumption, stale authority/dependencies, interruption, response loss and failures between DML phases through real PostgreSQL/application boundaries when authorized. Do not substitute a typecheck for those observations.

This design does not grant additional test-change, database, deployment, real-company posting or provider authority. Follow the actual user task and current AGENTS.md. Keep the five active tasks under their assigned owners. The packet dependency graph is preserved; implementation readiness is checked against the actual released application ports.
