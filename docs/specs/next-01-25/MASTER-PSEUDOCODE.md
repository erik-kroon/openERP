# OpenERP: all 25 work packets rewritten for Effect application ownership

Edition **v2**. This complete specification replaces the earlier SQL-owned pseudocode dossier; no separate amendment needs to be applied. Use the individual packets for delegation or this full document for coordination.

The supplied application-ownership decision is based on revision `422276ae5ed9d0ca146447d92bb3d27c99f8c48a`. The original financial/task evidence baseline is `bb628452196a55ceef7516f76fc3cd6471ae4d91`. This rewrite does not claim another repository or legal audit. Pseudocode is not compiled TypeScript/SQL or executed accounting behavior.

**Core rule:** application services own business decisions and scoped writes; every atomic financial group uses one transaction passed to all internal writers. SQL owns relational durability and narrow integrity. Background delivery uses effect-mq in a separate persistent Bun process. The five active assignments remain reserved.

## Contents

1. [Shared application-owned contracts](#part-01)
2. [Qualified rule and form data](#part-02)
3. [NEXT-01: Owner-aware case review](#part-03)
4. [NEXT-02: Capability-specific company admission](#part-04)
5. [NEXT-03: Domestic purchasing with owned tax recognition](#part-05)
6. [NEXT-04: Actual domestic VAT return and controls](#part-06)
7. [NEXT-05: General-rule cross-border service purchases](#part-07)
8. [NEXT-06: Owner-paid expenses, reimbursement and funding](#part-08)
9. [NEXT-07: Supplier paid credits and refunds](#part-09)
10. [NEXT-08: Payment instruction resolution and replacement](#part-10)
11. [NEXT-09: Complete Plaid sync windows](#part-11)
12. [NEXT-10: Provider revisions to reviewed bank observations](#part-12)
13. [NEXT-11: Separate complete-book SIE4E export](#part-13)
14. [NEXT-12: Historical open-item adoption](#part-14)
15. [NEXT-13: Semantic P&L and balance-sheet snapshots](#part-15)
16. [NEXT-14: Original dimension assignments](#part-16)
17. [NEXT-15: Legal customer credit notes](#part-17)
18. [NEXT-16: Evidence-aware period preparation](#part-18)
19. [NEXT-17: Payable FX and explicit fees](#part-19)
20. [NEXT-18: Incremental open-item FX remeasurement](#part-20)
21. [NEXT-19: Disposal with proceeds](#part-21)
22. [NEXT-20: Frozen regular-payroll calculation](#part-22)
23. [NEXT-21: Payroll posting, payslip and AGI artifact](#part-23)
24. [NEXT-22: Pre-close tax bridge and INK2/SRU](#part-24)
25. [NEXT-23: Financial close and single-count carry-forward](#part-25)
26. [NEXT-24: K2 annual-report semantic model and iXBRL](#part-26)
27. [NEXT-25: Fixed-revision company rehearsal and restore](#part-27)
28. [Integration and ownership map](#part-28)
29. [Rewrite record](#part-29)
30. [Sources and limits](#part-30)

---

<a id="part-01"></a>

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


---

<a id="part-02"></a>

# Qualified data inputs, not hidden algorithms

Edition v2: the packet algorithms are specified as application-owned operations. This carries forward the supplied rule-data requirements without a fresh legal or provider verification. Statutory tables, field codes, taxonomy packages and actual company facts must enter as explicit versioned inputs. This package does not invent those bytes or certify the example rates as current law.

## Release contract

```text
QualifiedReleaseManifest {
  releaseId, family, jurisdiction,
  officialSourceLocations, fetchedAt,
  exactFileHashes, parserVersion, calculationCodeVersion,
  effectiveDatePredicate, supportedCaseMatrix,
  formulaOrMappingData, independentExpectedCases,
  reviewRecord, status: staged|qualified|withdrawn
}

qualifyRelease(candidate, independentReview):
    verify source files and hashes against retained originals
    parse strictly; require complete supported table/field/taxonomy membership
    check ranges nonoverlapping, required branches covered and units explicit
    validate independent expected cases and semantic counterexamples
    require reviewer approves exact candidate digest and applicability
    freeze qualified release; never update its bytes in place

loadReleaseForOperation(operation, facts, dates):
    select by exact family and applicability predicate
    require exactly one qualified supported release
    if missing/ambiguous: return typed missing-release blocker
    return immutable data + code checksum for the packet's deterministic calculator
```

This is a deployment/review mechanism for existing finite domain calculators, not a general financial scripting language. Data may define a finite table, tiers or report-field mapping. It cannot write SQL, grant authority or execute arbitrary supplied code.

## Required inputs by family

| Family | Required data | Deterministic use |
| --- | --- | --- |
| Company admission | Legal identity, fiscal interval, accounting method, dated registrations, framework applicability and reviewed account roles | Resolve exact operation/date witness in NEXT-02 |
| Domestic purchase/VAT | Supply/tax-point predicates, rates, deduction rules, source-tax tolerance and line/box rounding | NEXT-03/04 calculate and publish source-linked tax components |
| Cross-border services | General-rule eligibility, exception assessment, tax-point conversion, reverse-charge boxes and credit rules | NEXT-05 keeps tax base distinct from carrying/settlement value |
| FX | Directional exact rate observations and policy dates | NEXT-17/18 consume commerce paired balances and reporting-rate witnesses |
| Payroll withholding | Official year/frequency/table/column rows and formulas, or valid individual withholding decision | NEXT-20 selects one bracket/formula, never nearest available row or universal percentage |
| Employer liabilities | Date/age/status eligibility, monthly/annual bands, rate tiers and aggregation rounding | NEXT-20 evaluates cumulative liability and exact incremental share |
| AGI | Exact XSD bundle, namespaces, field meanings, person/period identity and replacement/removal rules | NEXT-21 renders and validates the paid/provided population |
| Corporate tax | Tax-year rates/rounding, supported adjustments, loss eligibility and form maps | NEXT-22 calculates pre-close tax and reconciles after-tax form starting values |
| SRU | Exact INFO/BLANKETTER grammar, encodings, form identifiers, field codes/types and limits | NEXT-22 serializes known fields and rejects unsupported output |
| SIE4E | Qualified version/record grammar, encoding, balance/object/period semantics | NEXT-11 emits complete selected-book data without changing existing4I |
| K2/iXBRL | Framework applicability, required disclosures, concept mapping, taxonomy/entry points and presentation/signature rules | NEXT-24 freezes semantic content, renders and checks exact facts |
| Payment cancellation | Provider-specific finality/authentication and no-execution semantics | NEXT-08 releases only instruction capacity supported by actual proof |

## Date selection

```text
posting eligibility              -> actual accounting date and fiscal period
supplier/customer legal identity  -> event/issuance identity evidence required by operation
VAT registration/treatment        -> qualified supply/tax-point and method selection
payroll calculation               -> earnings inputs plus planned payment basis
AGI                               -> actual paid/provided reporting basis
statement accounting framework    -> fiscal-year applicability including published exceptions
FX recognition/settlement/report  -> three separately named rate/evidence policies
```

Do not replace these selectors with `latestRelease(today)`. A changed rule creates a new release and impact analysis; it does not rewrite old approved plans or filed bytes.

## External-version observation limits

The original dossier recorded checks of official Plaid, SIE, BFN and Skatteverket material for the narrow facts cited in SOURCES.md. Those are inherited source observations, not new checks in this rewrite. No complete statutory table/XSD/SRU/taxonomy bundle was downloaded and qualified here. The AGI portal surfaced differing1.1.18.x labels across search/open results, so no exact production schema version is asserted by this package. The implementation must pin the actual selected schema bytes, not a page title.

No model invents a tax table when a release is missing. A missing company registration does not stop source retention. A missing mandatory qualified field mapping does prevent claiming a finished statutory artifact. These boundaries are outputs of the specified algorithms, not unanswered choices about the architecture.

## Application persistence of qualification

Qualification and book activation are named Effect operations. They decode retained releases, apply the finite checks above and persist the review/release identity through the caller's transaction. No SQL function selects tax rates or declares a rule applicable. Database records enforce immutable identity, scope and allowed storage states. The algorithm/rule version is part of each prepared plan and artifact, independently of the database schema version.


---

<a id="part-03"></a>

# NEXT-01: Owner-aware case review

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/cases/review-targets.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/cases/review-targets.ts` or the existing equivalent owner |
| Pure calculation | Typed ownership resolution and safe local route selection |
| Atomic scope | A read transaction captures the exact owner. It creates no journal or approval. |
| Prerequisites | None |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Implement in the existing case components and their current-owner lookup. Shared workspace composition stays root-owned. No change to financial approval powers. See C1–C10 in `00-COMMON.md`.

## Contract

```text
ReviewResolution =
    Standalone {changeSetId, planDigest, resolvedAt, ownershipVersion}
  | Correction {bundleId, bundleDigest, constituentId, role, resolvedAt}
  | OtherOwner {ownerKind, ownerId, safeInspectionRef}
  | Ambiguous {conflictingOwnerRefs}

resolveReviewTarget(access, scope, changeSetId):
    return withAdmittedPrincipal(access, scope, readPermission, (tx, principal) =>
        BookDb.lockForShare(tx, scope)
        plan = PlanDb.loadSameBook(tx, scope, changeSetId)
        owners = OwnershipDb.loadExactConstituentOwners(tx, scope, plan.id)
        # Both reversal and replacement membership, not just latest case metadata.
        if >1 incompatible owner: return Ambiguous(authorized safe references)
        if one correction:
            require exact scope, constituent and bundle digest relationship
            return Correction(bundle.id, bundle.digest, plan.id, exactRole)
        if one other owner: return OtherOwner(owned read target)
        return Standalone(plan.id, plan.digest, databaseTime, ownershipVersion)
    )
```

Use a current read operation when available. If the only current resolver is targeted case capture, invoke it as an explicit preparation mutation with its own idempotency key, then read the new snapshot. Never mislabel that fallback as a harmless GET. An unavailable resolver leaves inspection enabled and financial routing unavailable.

```text
CaseContextPanel.onReviewClicked(planId):
    set resolutionState = loading(planId)
    resolution = await resolveReviewTarget(book.scope, planId)
    discard response if selection or book changed while request was in flight
    match resolution:
      Standalone -> onReview({kind: 'standalone', id, planDigest})
      Correction -> onReview({kind: 'correction', bundleId, bundleDigest})
      OtherOwner -> display existing owned inspector; do not expose standalone execution
      Ambiguous -> show conflict; no financial button
    after actual destination mounts:
        focus destination's review heading

renderReview(target):
    switch target.kind:
      standalone: existing PostingRecoveryReview(target.id)
      correction: existing CorrectionBundleReview(target.bundleId)
    # Each review rechecks live owner/approval state. The resolution is not a capability token.
```

The latest-plan button resolves the latest plan. Each history-row button resolves its own plan. Do not apply the latest plan's owner to all alternatives. Ignore stored arbitrary URIs for navigation; select from a local route table. Query keys include entity, book and plan. Abort previous reads when selection changes.

A bundle created after resolution is still protected by the application execute-time aggregate-owner validation. Show the resulting owned-operation refusal and route through a fresh resolution rather than retrying the constituent.

## Design vectors

```text
historical snapshot has no optional owner + current reversal belongs to bundle B
    => open B, not standalone
history has standalone P1 and replacement P2 in B
    => P1 and P2 resolve independently
owner lookup unavailable
    => source/history inspection works, execution routing is blocked
book changes during lookup
    => discard stale response
```

Evidence baseline: original handoff S05/S06. Proposed resolver name is not an assertion that an endpoint already exists.


---

<a id="part-04"></a>

# NEXT-02: Capability-specific company admission

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/company/profiles.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/company/profiles.ts` or the existing equivalent owner |
| Pure calculation | Effective-date profile selection and overlap validation |
| Atomic scope | Activation, affected membership versions and receipt commit together without a journal. |
| Prerequisites | None |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Extend company setup and existing legal-policy records. Do not change the book's historical synthetic meaning or redesign authentication. Shared records follow C2–C5.

## Records and keys

```text
FactRevision immutable {
  id, entityId, factKind, effectiveInterval, recordedAt,
  value | Unknown | NotApplicable(reason), evidenceRefs, supersedes?
}
FactReview immutable {factRevisionId, digest, reviewer, result, reviewedAt}
RuleRelease immutable {
  id, jurisdiction, family, version, checksum,
  applicabilityPredicate, requiredFactKinds, requiredRoleKinds,
  calculatorVersion, roundingRules, validInterval, sourceManifest,
  qualificationStatus
}
RoleBinding immutable {
  bookId, roleKind, accountId, accountRevision, effectiveInterval,
  evidence, reviewer, supersedes?
}
Activation immutable {
  bookId, family, ruleReleaseId, selectedFactReviews, roleBindings,
  applicabilityScope, effectiveInterval, approvedDigest
}
# Revocation/supersession append records; no editing activated bytes.
```

A `RuleRelease` contains executable code/data already reviewed for that family. It is not a user-supplied prompt or arbitrary code. A book activation selects an existing supported release, not permission to invent a treatment.

## Resolve by the operation's dates

```text
resolveProfile(captured, family, dates, eventFacts):
    needed = requiredFactsForFamily(family)
    facts = {}
    for kind in needed:
        selectorDate = dateBasisFor(family, kind, dates)
        matches = effective reviewed revisions(kind, selectorDate, captured.recordedCutoff)
        require exactly one usable match else MissingFact/AmbiguousFact
        facts[kind] = matches.only
    candidates = active releases and book activations with:
        matching family, jurisdiction, date interval and explicit applicability predicate
    require exactly one candidate
    require candidate qualification supports this case and record class
    roles = resolve explicit reviewed account roles at relevant posting date
    require each role exists, is active for new posting and belongs to book
    return ProfileWitness {
      factRevisionIds, factReviewIds, roleBindingIds,
      ruleReleaseChecksum, activationId, dates,
      dependencies for precisely these selections
    }
```

Date selection is family-specific: posting eligibility uses posting date, VAT uses its qualified tax point/method, payroll uses payment/reporting dates and statements use the fiscal-year framework applicability. An annual rule version is not selected merely by today's date.

## Activation transition

```text
prepareActivation(request):
    capture referenced facts/reviews, rule release, roles and prior activations
    require rule code and schema support exist
    require no contradictory evidence or overlapping ambiguous activation
    return seal exact activation proposal + capabilities it would enable

executeActivation(command):
    return withAdmittedPrincipal(access, scope, operatorPermission, (tx, principal) =>
        BookDb.lockWriter(tx, scope)
        if prior = CommandDb.replay(tx, principal, command): return prior
        plan = ProfileDb.loadActivationPlan(tx, scope, command.planId)
        current = ProfileDb.loadSelectionAndOverlaps(tx, scope, plan)
        ProfileDomain.assertSameFactsRolesReleaseAndScope(plan, current)
        require no contradictory evidence or ambiguous overlapping activation
        approval = ApprovalApp.validateWithinTransaction(tx, principal, plan, command)
        activation = ProfileDb.insertActivation(tx, plan, approval)
        ProfileDb.bumpAffectedFamilyMembership(tx, plan.applicabilityScope)
        CaseDb.insertImpacts(tx, affected unexecuted proposals)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {activation, journalIds: []}, approval)
    )
```

Prior fact selections in committed records remain historical. A retroactive fact correction creates impact cases for already posted work and does not rewrite the old computation. A future-only change need not invalidate a past event's profile witness.

## Integration

```text
canPrepare(family, event) = resolveProfile(...) succeeds
canReportComplete(period) = all applicable families have complete qualified controls
canFile(artifact) = canReportComplete AND format/signature/provider requirements met
```

Never collapse these into `company.productionReady = true`. Let evidence capture run when accounting facts are incomplete. Extend the current legal-AR activation owner rather than making a second authority for the same operation. The clean replacement does not need an old-database adapter. Any meaningful retained activation keeps its original scope and evidence.

UI returns structured missing facts with affected operations. Unknown is not `false`, empty text or zero. Actual company activation needs actual reviewed records; synthetic fixtures are usable only in their explicit class.

Evidence baseline: handoff S02/S03/S17. Framework release selection must follow official applicability guidance [X04 in SOURCES.md].


---

<a id="part-05"></a>

# NEXT-03: Domestic purchasing with owned tax recognition

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/purchasing/recognition.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/purchasing/recognition.ts` or the existing equivalent owner |
| Pure calculation | Domestic purchase and original-line credit compilers |
| Atomic scope | Journal, payable, source recognition, tax facts and receipt share one tx. |
| Prerequisites | NEXT-02 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-02. Extend supplier acceptance and credit owners, not their WIP VAT settlement/amendment consumers. Start with qualified same-currency SEK accrual cases.

## Immutable recognition result

```text
PurchaseRecognition {
  economicKey, supplierInvoiceRevision, profileWitness,
  lines: [{sourceLineId, net, sourceTax, deductibleTax, nonDeductibleTax,
           expenseRole, taxPoint, recognitionDate, taxComponentId}],
  payableId, voucherId, taxFacts[], receiptId
}
TaxFact {
  identity: (recognitionId, sourceLineId, componentRole),
  signedBase, signedOutputTax, signedDeductibleTax,
  sourceTax, treatment, taxPoint, reportingObligation,
  journalComponentRefs, sourceRefs, ruleRelease, adjustsTaxFactId?
}
UNIQUE recognized purchase economicKey
UNIQUE taxFact(recognitionId, sourceLineId, componentRole)
```

A valid invoice may have zero tax. That requires a supported zero/exempt treatment, not classification as deductible 25% VAT with the amount changed to zero.

## Pure calculation

```text
compileDomesticPurchase(basis, reviewedLines, funding = supplierPayable):
    witness = resolveProfile(basis, domesticPurchase, dates, sourceFacts)
    require complete source-line selection and invoice gross reconciliation
    for line in sourceLines in original order:
        N = exact source net; T = exact asserted source VAT; G = exact source gross
        require N >= 0 AND T >= 0 AND G == N+T
        treatment = witness.classify(line)  # explicit supported table, no brand inference
        expected = roundRational(N*treatment.rate.n, treatment.rate.d,
                                 treatment.invoiceTaxRounding)
        checkSourceTaxDifference(T, expected, treatment.acceptancePolicy)
            # exact-match, qualified tolerance + retained discrepancy, or review-required
        D = roundRational(T*deductionFraction.n, deductionFraction.d,
                          treatment.deductionRounding)
        require 0 <= D <= T
        E = N + T-D
        Journal.addSigned(line.expenseRole, E, sourceLine=line.id)
        Journal.addSigned(inputVatRole, D, taxComponent=line.id)
        taxFacts += signed purchase component(base=N, deductibleTax=D,
                                              sourceTax=T, nonDeductible=T-D)
    totalGross = sum(N+T)
    require totalGross > 0
    Journal.addSigned(funding.controlRole, -totalGross)
    return {journal: finish(), payable: totalGross, lines, taxFacts, witness}
```

A tax fact with zero deductible amount may still carry a required basis/exclusion. Do not manufacture a zero tax journal line. Preserve raw source amounts and the qualified discrepancy result separately. Any material source mismatch creates a review case rather than silently rewriting the invoice to match the calculator.

## Atomic posting

```text
executePurchase(command):
    return withAdmittedPrincipal(access, scope, purchasePermission, (tx, principal) =>
        BookDb.lockWriter(tx, scope)
        if prior = CommandDb.replay(tx, principal, command): return prior
        plan = PurchaseDb.loadExactPlan(tx, scope, command.planId)
        current = PurchaseDb.loadSourcesCapacitiesAndRoleClaims(tx, plan)
        require source revision/profile current and no recognized economic duplicate
        require no conflicting reservation or economic role
        PurchaseDomain.validateStoredAggregate(plan, current)
        approval = ApprovalApp.validateWithinTransaction(tx, principal, plan, command)
        journal = JournalApp.postWithinTransaction(tx, plan.journal)
        payable = PurchaseDb.insertPayableAndLineCapacities(tx, plan, journal)
        taxFacts = TaxFactApp.recordRecognitionWithinTransaction(tx, plan.taxFacts, journal)
        RecognitionDb.insertOwnedIdentity(tx, plan.economicKey, journal, payable, taxFacts)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journal.ids, payable, taxFacts}, approval)
    )
```

Generic manual entry, expense-review and independent tax-fact admission must reject a second recognition of those same economic components. A second evidence document about the purchase is still retainable. Adoption of an already posted purchase is a separate reviewed no-reposting operation, not an extra recognition.

## Partial credit compiler

```text
compilePurchaseCreditLines(original, previousCredits, sourceCredit):
    for selected original line:
        require credit net/tax supported by original treatment and distinct credit evidence
        require cumulative credited net <= original net
        require cumulative credited source tax <= original source tax
        require previouslyReleasedDeduction matches this versioned cumulative policy
            else require an explicit retained-credit basis decision; never conceal a residual
        d = cumulativeRelease(original.deductibleTax, original.sourceTax,
                              priorCreditedTax, newCreditedTax, deductionReleasePolicy)
        e = creditNet + creditTax-d
        Journal.addSigned(original.expenseRole, -e)
        Journal.addSigned(original.inputVatRole, -d)
        append negative TaxFact adjusting original component, with qualified credit taxPoint
    return exact line releases, signed tax adjustments and remaining line capacities
        # No payable/refund counterpart selected in this reusable line compiler.

compileUnpaidPurchaseCredit(original, previousCredits, sourceCredit, current):
    lines = compilePurchaseCreditLines(original, previousCredits, sourceCredit)
    g = sum(lines.creditNet + lines.creditTax)
    require g <= current.unpaidResidual
    journal = lines.expenseAndTaxReversals + debit(payableRole, g)
    return balanced journal, lines.taxAdjustments and updated credit capacities

executeUnpaidPurchaseCredit(command):
    withAdmittedPrincipal(access, scope, creditPermission, (tx, principal) =>
        lock book; replay exact command first
        load sealed credit and current original-line/payment/reservation basis in batches
        validate capacities, qualified tax policy and exact approved effects
        approval = validate current exact credit approval using C5
        journal = JournalApp.postWithinTransaction(tx, approved journal)
        credit = PurchaseDb.insertCreditAndCapacityEffects(tx, plan, journal)
        tax = TaxFactApp.recordAdjustmentsWithinTransaction(tx, plan.taxAdjustments, journal)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journal.ids, credit, tax}, approval)
    )
```

NEXT-07 handles the amount exceeding unpaid principal. It consumes the same credit compiler and capacities rather than duplicating them. A final credit releases exactly the remaining original deduction, not independently rounded fragments with leftover tax.

Payment execution consumes the payable and bank/owner consideration. It calls no purchase-recognition or VAT publisher. Corrections use signed adjusting facts; do not both remove the original tax fact and subtract it again.

## Vectors

```text
N=10000 T=2500 deduction=1 => expense10000 / input2500 / payable12500
same purchase paid later => zero new purchase-tax facts
N=10000 T=2500 deduction=1/2 => expense11250 / input1250 / payable12500
N=101 T=25 G=126 with explicitly allowed half-up => retain126, not126.25
credit N=4000 T=1000 full deduction => AP debit5000 / expense credit4000 / input credit1000
```

New rates/tolerance/deduction releases must be qualified. This pseudocode does not certify every merchant's VAT treatment. Evidence baseline: S07/S08.


---

<a id="part-06"></a>

# NEXT-04: Actual domestic VAT return and controls

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/tax/vat-returns.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/tax/vat-returns.ts` or the existing equivalent owner |
| Pure calculation | Qualified VAT contribution mapping and control reconciliation |
| Atomic scope | Consistent capture then pure calculation then immutable snapshot/receipt persistence. |
| Prerequisites | NEXT-02, NEXT-03 |
| Reserved handoff | WIP-VAT03, WIP-VAT04-A1 |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-02/03. Financial integration waits for WIP-VAT03 and WIP-VAT04-A1. Their execution, delta algorithm and qualification remain external owners.

## Separate dependencies and state

```text
VatCalculationBasis {
  obligationId, registeredPeriod, profileWitness,
  capturedFacts, signedAdjustments, sourceCoverage,
  taxableMembershipEpoch, recognitionVersions, mappingRelease,
  ledgerControlSnapshot, settlementOwnerSnapshot, amendmentOwnerSnapshot,
  cutoff: {ledgerBoundary, recordedAt}
}
VatCalculation {
  exactByBox, reportedByBox, roundingResiduals,
  contributionsByFactAndBox, exclusions,
  calculationSupported, coverageComplete, controlsReconciled,
  filingReady, basisDigest
}
```

A tax fact remains included in its historical recognition period after a correcting fact is appended; the new negative component applies according to the qualified adjustment policy. Withdrawal of an erroneous nonfinancial observation is different from a posted credit. Build the fact selection so a reversal is represented exactly once, never original removal plus double negative adjustment.

## Capture and calculate

```text
captureVatBasis(tx, scope, obligation):
    under shared book barrier:
        require actual registered period and supported profile witness
        capture complete tax-fact membership and corrections, including zero-count epoch
        capture required-source inventory with explicit unavailable/unknown members
        capture all GL movements in each selected VAT control, not just known good ones
        capture VatReclassificationApp/VatAmendmentApp.readEffectiveWithinTransaction(tx, ...)
        for EVERY obligation affecting these accounts
        in the control interval, as signed per-account vectors
        # Not only the obligation whose return is being prepared.
        retain fixed IDs/digests and complete counts

calculateActualVat(basis):
    issues = []
    totals = zero vector for all declared report boxes
    for fact in basis.facts:
        eligibility = check retained treatment/rule/date/source/recognition identities
        if invalid: retain exclusion(fact, reason); issues += reason; continue
        rows = taxMappingRelease.map(fact)
        # Domestic sales basis05; output10/11/12 by qualified rate.
        # Deductible input48. Other cases require their explicit supported mappings.
        for row in rows:
            totals[row.box] += row.signedMinor
            provenance[row.box].append(fact.id, row.signedMinor, mappingRuleId)
    require sum(provenance[box]) == totals[box] for every box
    reported = for each primitive box: round to filing unit using release's box rule
    reported49 = sum(reported output-tax boxes) - reported48
    exact49 = sum(exact output-tax boxes) - exact48
    residual49 = exact49 - 100*reported49  # SEK scale2 for this profile
    retain both; do not assume round(exact49/100) equals reported49
    controls = reconcileTaxControls(basis)
    coverage = every applicable source family has current independent coverage evidence
    supported = no relevant unhandled treatment or excluded mandatory fact
    ready = supported AND coverage AND controls.noUnexplainedRows AND periodVerified
    return calculation with ready flags, never a submitted/assessed/paid state
```

The qualified filing release owns whole-krona rules. Do not automatically require `box05 % 100 == 0`, propagate the old synthetic `vat*4==net` check or remove all guards to accept actual data. Do not silently change the meaning of retained synthetic calculations. Use a distinct qualified actual-company compiler; an unused pre-release implementation need not remain a live fallback.

## Independent control rollforward

```text
reconcileTaxControls(basis):
    for controlAccount in requiredControls:
        expectedClosing = reviewedOpening[account]
        expectedComponents = []
        for recognized fact component POSTED in the GL control interval:
            expectedClosing += its actual signed owned GL amount
            expectedComponents += its exact linked journal component
        for reclassification/amendment effect from released WIP owner:
            expectedClosing += effect.vector[account]
            expectedComponents += effect.journalComponents
        for other explicitly reviewed owned non-tax movements:
            expectedClosing += movement.signedAmount
            expectedComponents += movement.journalComponents
        actualClosing = frozenGL[account].closing
        unexplainedRows = actualMovementIdentities - expectedComponents
        missingRows = expectedComponents - actualMovementIdentities
        result = {difference: actualClosing-expectedClosing, unexplainedRows, missingRows}
        # Two opposite unexplained rows still block; their zero net cannot conceal them.
```

Tax-point attribution and GL posting dates can differ. The declaration selects facts by the qualified tax point. The control rollforward selects components by their actual GL accounting dates. Retain an explicit timing bridge for declaration facts already represented in opening balances and GL movements attributable to another tax period. Never add an opening-balance component again just because it enters this return. Known out-of-period facts are explained exclusions, not automatically missing mandatory current-period facts.

A complete return depends on all relevant boxes being known or evidenced inapplicable. Empty facts do not by themselves establish a zero return. With complete independently reviewed zero-activity coverage, however, zero facts can validly calculate zero without a fabricated dummy fact.

Sealing the new return stores all contributions, exclusions and relevant epochs. A subsequent owned reclassification does not change historical taxable-source membership. Its receipt and control inventory change independently. Later source corrections or unexplained VAT-control postings invalidate current readiness. Retained snapshot bases remain immutable. The new baseline does not require a parallel legacy-global-sequence workflow.

UI shows exact, reported and assessed amounts separately, each box's contributors and unresolved control rows. A read of an old return displays its saved calculation plus separate currentness. Any amendment execution routes only to the released WIP amendment owner.

## Vectors

```text
sales net10000 output2500, purchase deductible1000 => exact payable1500
no facts + complete reviewed no-activity scope => zero calculation possible
no facts + unknown source coverage => zero calculated amount, readiness false
two unowned GL lines +500 and -500 => net difference0, controlsReconciled false
later unrelated non-tax posting => no automatic taxable-basis invalidation
later backdated tax fact => taxable membership changes, new return required
```

Evidence baseline: S08/S03 and approved external rule manifests. Scope remains supported domestic families, not universal Swedish VAT.

## Effect application sealing

```text
prepareActualVatReturn(command):
    captured = withAdmittedPrincipal(access, scope, taxReadPermission, (tx, principal) =>
        lock book for consistent capture; replay the preparation key if committed
        return VatDb.captureAllFactsCoverageAndControlRows(tx, scope, selection)
            + VatReclassificationApp.readEffectiveWithinTransaction(tx, scope, controls, cutoff)
            + VatAmendmentApp.readEffectiveWithinTransaction(tx, scope, controls, cutoff)
    )
    if captured is replay: return saved result
    calculated = VatDomain.calculateActualVat(captured)
    # Complete assessments can be retained with readiness false; do not fake a final return.
    return withAdmittedPrincipal(access, scope, taxPreparePermission, (tx, principal) =>
        lock book; replay exact command first
        verify captured dependency versions and complete memberships
        snapshot = VatDb.insertImmutableCalculation(tx, calculated, captured)
        return CommandDb.save(tx, principal, command, snapshot)
    )
```

Calculation, readiness and exclusion decisions are application-owned. Persistence queries may sum exact stored movements but may not select tax treatment or activate a profile. Every WIP inventory is read through its released tx-passing application port. No reclassification or amendment is executed inside this preparation transaction.


---

<a id="part-07"></a>

# NEXT-05: General-rule cross-border service purchases

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/purchasing/service-purchases.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/purchasing/service-purchases.ts` or the existing equivalent owner |
| Pure calculation | Service-place/tax treatment and separate recognition/tax-point conversion |
| Atomic scope | Journal, original/book payable or owner liability and tax facts share one tx. |
| Prerequisites | NEXT-03, NEXT-04 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-03/04. Unpaid foreign-denominated obligations additionally wait for NEXT-17 and WIP-FX02-P1. No replacement FX register.

## Classification contract

```text
ServicePurchaseFacts {
  invoiceLegalSupplier, supplierCountry, supplierEstablishment,
  customerTaxablePersonEvidence, receivingEstablishment,
  serviceKind, specialPlaceOfSupplyExceptionAssessment,
  sourceNetAndAnyForeignTax, invoiceCurrency, suppliedOn, receivedOn,
  taxPointEvidence, businessUse, deductionFraction, creditOf?
}
classifyGeneralService(facts, release):
    require known actual invoicing entity; a brand name is insufficient
    require recipient and place-of-supply conditions satisfied
    require serviceKind in release.supportedGeneralRuleServices
    require no applicable special exception, else UnsupportedProfile
    require source tax is qualified for treatment
    if foreign tax is nonzero in this initial reverse-charge profile:
        retain the entire invoice gross and foreign tax
        fail UnsupportedForeignTaxOnSourceInvoice
        # A separate qualified treatment may later handle it. Never drop it from liability
        # or treat it as Swedish input VAT just to continue.
    jurisdictionClass = EU_OTHER or NON_EU from facts effective at tax point
    return explicit treatment with tax rate, basis box21 or22 and output box30/31/32
```

The general-rule box mappings and conditional deduction follow Skatteverket's EU/non-EU service guidance [X05/X06]. This does not cover goods, imported goods, every digital-service arrangement or special place-of-supply exceptions.

## Three different values

```text
original liability in supplier currency
book carrying value at recognition
SEK reverse-charge tax base at the qualified tax point
```

The latter two may differ because their policies/dates can differ. Never overwrite one with the other to balance an entry. If the first implementation supports only coincident dates/rate policies, require that equality explicitly and refuse other cases until the qualified profile handles them.

## Compiler

```text
compileCrossBorderService(basis, facts):
    treatment = classifyGeneralService(facts, qualifiedRelease)
    accountingValue = convert original net by accounting-recognition policy
    taxBase = convert original taxable base by qualified tax-point policy
    outputTax = roundRational(taxBase*treatment.rate.n, treatment.rate.d, taxRounding)
    deductible = roundRational(outputTax*deductionFraction.n, deductionFraction.d,
                               deductionRounding)
    nonDeductible = outputTax-deductible
    Journal.addSigned(serviceCostRole, accountingValue + nonDeductible)
    Journal.addSigned(reverseChargeInputRole, +deductible)
    Journal.addSigned(reverseChargeOutputRole, -outputTax)
    Journal.addSigned(fundingOrPayableRole, -accountingValue)
    finish()
    taxFact = {
      signedBase: taxBase,
      basisBox: treatment EU ?21:22,
      outputTaxBox: treatment.outputBox,
      outputTax, deductibleInputBox48: deductible,
      originalSourceAmount, accountingRateWitness, taxRateWitness
    }
    if unpaid foreign obligation:
        append commerce monetary item using original units and accountingValue
    return native purchase aggregate + taxFact
```

Already-paid recognition needs an explicit selection: either recognize through AP and a separately linked settlement, or recognize against an existing evidenced cash/owner payment through the appropriate owner. Do not use the same bank debit as both new cash movement and adoption of an existing cash posting.

For later credit, consume the original line's source net/tax capacities and the qualified credit-period policy. A credit's monetary conversion and tax correction may have different prescribed bases. Where the release requires original-tax-basis reversal, release its retained tax components proportionately with exact final residuals. Where another policy applies, use that explicit release. Never infer a generic current-FX reversal of old VAT.

```text
executeServicePurchase(command):
    return withAdmittedPrincipal(access, scope, purchasePermission, (tx, principal) =>
        lock book; replay exact command first
        load exact sealed service-purchase plan
        load current source, recognition, rate and qualified tax witnesses in batches
        require treatment supported and economic purchase not already recognized
        ServicePurchaseDomain.assertApprovedConservation(plan, current)
        approval = validate exact current approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal)
        if foreign payable:
            obligation = CommerceFxApp.recordRecognitionWithinTransaction(tx,
                plan.originalUnits, plan.bookCarrying, journal, plan.recognitionWitness)
        else:
            obligation = selected existing payable/owner application writer(tx, plan, journal)
        taxFacts = TaxFactApp.recordRecognitionWithinTransaction(tx, plan.taxFacts, journal)
        RecognitionDb.insertOwnedIdentity(tx, plan.economicKey, journal, obligation, taxFacts)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journal.ids, obligation, taxFacts}, approval)
    )
```

## Vectors, all illustrative minor units

```text
accountingValue=100000, taxBase=100000, rate1/4, deduction1:
    cost100000 + input25000 - output25000 - payable100000 == 0
same with deduction1/2:
    cost112500 + input12500 - output25000 - payable100000 == 0
accountingValue=101000, taxBase=100000, full deduction:
    cost101000 + input25000 - output25000 - payable101000 == 0
later foreign settlement changes carrying/FX but changes no original tax fact
```

Use exact conversion witnesses from C1 and existing rate owners. Reject unknown FX source, scheme or tax point rather than defaulting rate to1.


---

<a id="part-08"></a>

# NEXT-06: Owner-paid expenses, reimbursement and funding

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/owners/operations.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/owners/operations.ts` or the existing equivalent owner |
| Pure calculation | Owner expense, existing-payable transfer, funding and reimbursement compilers |
| Atomic scope | Relevant journal, owner/commerce capacities and source usage commit together. |
| Prerequisites | NEXT-02, NEXT-03 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-02/03. Extend the existing owner register. Tax classification comes from the qualified purchase compiler, not from bank description or owner identity.

## Explicit modes

```text
OwnerOperation =
    NewOwnerPaidPurchase {purchaseSource, payerOwner, paidEvidence}
  | OwnerPaysExistingPayable {payableId, originalUnits, owner, paidEvidence}
  | ReimburseOwner {claimAllocations, cashSource}
  | OwnerLendsToCompany {lender, principal, bankEvidence, reviewedLoanTerms}
  | OwnerCapitalContribution {contributor, amount, reviewedLegalClassification, evidence}
```

Existing owner identities, effects and receipts remain authoritative. New modes do not reinterpret old synthetic data. A contribution does not acquire repayment rights because the UI calls it funding.

## New versus previously recognized purchase

```text
prepareOwnerPaidPurchase(input):
    recognition = find economic source recognition using preserved invoice/payment matches
    if none:
        require explicit evidence owner paid this company purchase
        compiled = compileDomesticPurchase(..., funding = ownerLiability(owner))
        bind same purchase economic key and tax identities as supplier-paid path
        return seal owner aggregate + new owner claim
    if recognition is supplier payable:
        return prepareOwnerPaymentOfPayable(recognition, input)
    if recognition already owner-paid:
        return AlreadyApplied(owner receipt)
    otherwise:
        return UnsupportedExistingRecognition with exact references

prepareOwnerPaymentOfPayable(payable, input):
    require current payable capacity >= amount and compatible same-currency profile
    require payment source not already consumed by a supplier/bank/owner settlement
    Journal.addSigned(supplierPayableControl, +amount)
    Journal.addSigned(ownerLiabilityControl, -amount)
    return plan {
      original invoice unchanged,
      supplier obligation consumption: amount,
      new owner claim: amount,
      new tax facts: []
    }
```

This transfer is not a second purchase. It creates no company-bank movement when the owner used a private account. An existing accounted owner payment can instead be adopted through an explicitly checked posted-control-line link, without duplicating the transfer.

## Reimbursement

```text
prepareReimbursement(owner, selectedClaims, cashSource):
    require all claims same owner, control role, currency and current version
    require claims have recognized owned effects, not merely a reviewed description
    require every requested leg >0 AND <= claim.remaining
    total = sum(legs)
    require total <= cashSource.unconsumedOwnerReimbursementCapacity
    if cashSource is unposted evidenced bank event:
        journal = debit owner liability(total), credit bank(total)
        action = post_and_allocate
    else if cashSource is existing compatible posted owner-control debit:
        action = adopt_existing_payment_and_allocate; journal = []
    else: fail UnsupportedSource
    seal complete legs, source identity and affected capacities

executeOwnerOperation(command):
    return withAdmittedPrincipal(access, scope, ownerOperationPermission, (tx, principal) =>
        lock book; replay exact command first
        plan = OwnerDb.loadExactPlan(tx, scope, command.planId)
        current = OwnerDb.loadSourcesClaimsAndCompatibleCapacities(tx, plan)
        OwnerDomain.assertCurrentCompleteOperation(plan, current)
        approval = validate exact current approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal) if nonempty else []
        if new purchase:
            TaxFactApp.recordRecognitionWithinTransaction(tx, plan.taxFacts, journal)
            RecognitionDb.insertOwnedIdentity(tx, plan.economicKey, journal)
        if payment of existing supplier payable:
            CommerceApp.applySettlementWithinTransaction(tx, plan.payableConsumption, journal)
        effects = OwnerDb.insertClaimSettlementAndAllocationEffects(tx, plan, journal)
        OwnerDb.bumpAffectedControlVersions(tx, plan)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: ids(journal), effects}, approval)
    )
```

For partial reimbursement, one payment may consume several claims. Every claim keeps its original source and prior allocations. A receipt replay restores neither capacity nor an old live view. It returns its original immutable result.

## Funding

```text
compileFunding(input, witness):
    require explicit classification supported by witness
    require observed company cash inflow or qualified existing posting adoption
    if loan:
        debit bank; credit shareholderLoanLiability
        create principal obligation; interest is separate and unsupported unless qualified
    if supported capital contribution:
        debit bank; credit reviewedEquityRole
        create contribution record, NOT a reimbursable owner claim
    if classification unknown or conditional rights unresolved:
        retain evidence/review only; no financial plan
```

Correct a consumed claim, liability transfer or reimbursement only through an owned aggregate reversal/replacement. If its downstream obligations cannot be restored together, refuse with an impact list. Do not create a new source key to bypass the refusal.

Controls use reviewed opening amounts plus owned current movements. A missing opening remains unknown. Company-bank reconciliation references the bank-side line independently of owner claim allocation; do not consume the same bank event twice by introducing a second matching authority.

## Vectors

```text
new owner-paid N10000 T2500 fully deductible:
    expense+10000, inputVAT+2500, ownerLiability-12500
reimburse5000:
    ownerLiability+5000, cash-5000; claim remaining7500; no new tax
already recognized AP12500 paid by owner:
    AP+12500, ownerLiability-12500; expense/tax delta0
capital contribution12500:
    bank+12500, qualified equity-12500; reimbursement capacity0
```

Evidence baseline: S12/S07.


---

<a id="part-09"></a>

# NEXT-07: Supplier paid credits and refunds

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/purchasing/credits-and-refunds.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/purchasing/refunds.ts` or the existing equivalent owner |
| Pure calculation | Shared line credit math plus payable/refund counterpart allocation |
| Atomic scope | Paid credit and refund receipt each have one complete owned tx. |
| Prerequisites | NEXT-03 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-03. NEXT-08 is conditional when an exported instruction still reserves the affected amount. Reuse original-line credit/tax capacity. No FX, advances or general netting in this first profile.

## State derived from immutable effects

```text
G = original gross obligation
K = effective cumulative credits
P = effective payments allocated under this bounded profile
Q = refunds already allocated to the linked refund receivable

require 0 <= K <= G
require 0 <= P <= G  # pre-existing overpayment profiles need their own admission
unpaid = max(G-K-P, 0)
refundPrincipal = max(P-(G-K), 0)
refundDue = refundPrincipal-Q
require 0 <= Q <= refundPrincipal
```

Do not store negative values in old nonnegative `outstandingMinor`. Add an explicit refund-receivable projection and preserve the older contract. The formula assumes effective payments/credits have not been reversed through an unsupported consumed-history path.

## Credit beyond unpaid capacity

```text
compilePaidSupplierCredit(original, history, creditDocument):
    creditLines = compile original-line net/source-tax/deduction releases from NEXT-03
    g = sum(creditLines.net + creditLines.sourceTax)
    require g <= remaining original-line gross capacity
    require no unresolved export reservation over affected payable
    before = derive(G,K,P,Q)
    apRelease = min(g, before.unpaid)
    newRefund = g-apRelease
    Journal.addSigned(payableControl, +apRelease)
    Journal.addSigned(supplierRefundReceivableControl, +newRefund)
    for line in creditLines:
        Journal.addSigned(originalExpenseRole, -(line.net + line.tax-line.deductible))
        Journal.addSigned(originalInputVatRole, -line.deductible)
    require before.refundPrincipal+newRefund == max(P-(G-(K+g)),0)
    return plan with credit tax facts, apRelease and refundPrincipalIncrease
```

The refund control is an explicit reviewed role, not an automatically inferred account or negative payable. A full paid credit is allowed only within the original line/tax limits and supported credit treatment.

```text
executePaidCredit(command):
    return withAdmittedPrincipal(access, scope, supplierCreditPermission, (tx, principal) =>
        lock book; replay exact command first
        load approved paid-credit plan and all original credit/payment/reservation capacities
        require current source-line basis, economic credit identity and exact approved digest
        RefundDomain.assertCreditConservation(plan, current)
        approval = validate exact current approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal)
        credit = PurchaseDb.insertCreditAndLineCapacityEffects(tx, plan, journal)
        refund = RefundDb.insertPrincipalIncrease(tx, plan, credit, journal)
        tax = TaxFactApp.recordAdjustmentsWithinTransaction(tx, plan.taxFacts, journal)
        bump owned credit/refund/control versions through tx
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journal.ids, credit, refund, tax}, approval)
    )
```

## Refund receipt

```text
prepareSupplierRefund(refundReceivable, source, allocations):
    require amount>0 AND sum(allocations)<=refundDue
    require source is evidenced same-currency cash receipt from supplier
    if source unposted:
        journal = debit bank(amount), credit supplierRefundReceivable(amount)
    else:
        require source references existing compatible posted refund-control credit
        require exact unused source capacity; journal=[]
    seal expected refund version + source capacity + exact allocation legs

executeRefund(command):
    return withAdmittedPrincipal(access, scope, refundPermission, (tx, principal) =>
        lock book; replay exact command first
        load approved refund plan and current cash-source/refund capacities
        validate scope, current source and every requested allocation
        approval = validate exact current approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal) if postNewCash else []
        refund = RefundDb.insertRefundAllocation(tx, plan, journalOrAdoptedComponents)
        SourceClaimDb.insertFinancialUsage(tx, plan.sourceBindings)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: ids(journal), refund}, approval)
    )
    # No expense reversal or additional VAT credit.
```

If a payment is reversed after a refund receivable or cash refund depends on it, the resulting formula could become negative. Reject the standalone reversal. An owned correction must restore the payment, credit and refund relationships together or give an explicit unsupported-consumed-history response.

Read views expose original invoice, credits, historical payments, current payable, refund principal and received refunds separately. Report cutoffs use accounting dates AND recorded cutoffs so later credits do not enter earlier saved statements.

## Vectors

```text
G125000 P100000 K0 Q0 => unpaid25000 refund0
credit50000 => AP debit25000 + refundAR debit25000 + original cost/tax credits50000
G125000 P100000 K50000 Q10000 => unpaid0 refundDue15000
another refund16000 => CapacityExceeded, no partial posting
new key for same credit-note identity => AlreadyApplied, not another refund entitlement
```

Evidence baseline: S07/S09. These equations are the chosen bounded design, not a universal receivables model.


---

<a id="part-10"></a>

# NEXT-08: Payment instruction resolution and replacement

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/payments/resolutions.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/payments/resolutions.ts` or the existing equivalent owner |
| Pure calculation | Proof-qualified instruction release and successor eligibility |
| Atomic scope | Reservation release, dispatch fencing and receipt share a non-journal tx. |
| Prerequisites | None |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Extend existing supplier payment-batch/export ownership. An XML file is not a paid invoice. It can nevertheless be submitted later, so absence of local success is not no-execution proof.

## Records

```text
Instruction immutable {
  id, batchId, exportHash, endToEndId, beneficiaryRevision,
  originalAmount, currency, invoiceAllocationIntents, disclosedOrDownloaded
}
OutcomeObservation immutable {
  instructionId, sourceEvidence, sourceKind,
  authenticatedProviderIdentity?, externalStatus, observedAt, amountScope?
}
NoExecutionProof immutable {
  instructionId, exportHash, providerContractVersion,
  exactAmountProvenNotExecuted, evidenceRefs,
  finalityScope, permitsResubmissionOfOldIdentity: false | unknown
}
Resolution immutable {instructionId, proofDigest, releasedAmount, receipt}
Replacement immutable {newInstructionId, predecessorId, resolutionId, approvedNewDigest}
```

Keep both external outcome and local accounting status. A provider may prove execution before the corresponding bank accounting is posted. That amount stays reserved against duplicate instructions until the payment is accounted for or separately resolved.

## Proof evaluation

```text
evaluateNoExecution(instruction, observations, proposedEvidence):
    if proposedEvidence.kind == operatorReportedRejected:
        fail InsufficientExternalProof
    if proposedEvidence.kind == controlledNeverDispatched:
        require channel controlled exclusively by this system
        require no bytes exposed/downloaded/copied outside that controlled channel
        require dispatch fence proves no admitted/inflight provider request
        require immutable revocation preventing future dispatch
        return exact undispatched amount
    if proposedEvidence.kind == qualifiedProviderFinalCancellation:
        require retained authentic response identifies this exact instruction/export scope
        require provider contract establishes no execution for stated amount
        require known accepted/settled history reconciles with cancellation
        require old identity cannot later execute under that contract
        return exact finally cancelled amount
    fail OutcomeUnknown
```

An ordinary downloaded manual file cannot satisfy the controlled-never-dispatched branch. Do not manufacture that proof from HTTP access logs, user assertion or a timeout. Such cases remain reserved until an actually applicable external cancellation/no-execution resolution is available.

## Exact capacity and atomic release

```text
prepareResolution(instruction):
    availableReservation = originalAmount
                         - alreadyAccountedExecutedAmount
                         - effectiveNoExecutionReleases
    release = qualified proof amount not previously consumed
    require 0 < release <= availableReservation
    require proven executed-but-not-accounted amounts excluded from release
    capture outcomeInventoryVersion, reservationVersion, invoice capacities, proof digest
    seal review and approval requirement

executeResolution(command):
    return withAdmittedPrincipal(access, scope, resolutionPermission, (tx, principal) =>
        lock book; replay exact command first
        lock affected instruction/reservation and dispatch-intent rows in stable order
        load exact resolution plan and current outcome/proof inventory
        PaymentDomain.assertNoExecutionProof(plan, current)
        require no admitted or in-flight request can later execute the released amount
        require stale workers are fenced by domain dispatch/cancellation version
        approval = validate exact current resolution approval using C5
        resolution = PaymentDb.insertInstructionCapacityRelease(tx, plan)
        PaymentDb.invalidateSuccessorEligibility(tx, affected allocations)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: [], resolution}, approval)
    )
```

Release is not a cancellation journal or supplier credit. It frees instruction capacity only. Existing financial payment allocations remain unchanged.

## Replacement and late outcomes

```text
prepareReplacement(resolution, currentInvoices):
    require resolution effectively released exactly this capacity
    re-read live outstanding and other reservations
    revalidate beneficiary evidence/revision and independent verification
    assign NEW immutable instruction identity with predecessor relation
    compile file from current approved amounts, never edit old bytes
    fresh approval; export through existing owner

onLateOldExecution(observation):
    append raw observed evidence
    if conflicts with released capacity:
        create high-priority duplicate-execution case
        stop any not-yet-dispatched successor for this capacity
        if successor may already have executed: keep both outcomes unknown/observed precisely
        do not silently allocate two payments to one invoice
        reconcile real cash separately, using overpayment/recovery treatment only when supported
```

All release/dispatch/admission mutations use one instruction-reservation authority and lock discipline. A stale worker cannot dispatch after release by holding a cached approval. External reality can still disagree with a provider report; retain the conflict instead of rewriting history.

Vectors: unknown -> no release; reported rejection -> no release; final no-execution100 -> release100 once; invoice paid while review open -> stale; same-key replay -> same resolution; late old debit -> conflict, not silent success.

Evidence baseline: S09. Real proof must come from the chosen provider contract, not from this pseudocode.


---

<a id="part-11"></a>

# NEXT-09: Complete Plaid sync windows

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

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


---

<a id="part-12"></a>

# NEXT-10: Provider revisions to reviewed bank observations

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/banking/source-admission.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/banking/source-admission.ts` or the existing equivalent owner |
| Pure calculation | Exact provider revision mapping and same/different economic-event decisions |
| Atomic scope | Source admission and provenance commit together; no automatic posting or matching. |
| Prerequisites | NEXT-09 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-09. Interpret only published generations. Raw provider delivery is not already a statement, a reviewed bank observation or accounting.

## Source and admission model

```text
ProviderIdentity := (book, provider, stream, providerTransactionId)
Revision immutable {
  identity, publicationVersion, changeKind, rawLocator, rawDigest,
  providerPendingReference?, normalizedFacts, parserVersion
}
ObservationHead {identity, latestRevision, eligibilityVersion}
BankAdmission immutable {
  sourceRevision, economicObservationId, reviewDigest, existingBankObservationId
}
OverlapDecision immutable {
  evidenceBasedRelation: same_event | different_events,
  identities[], reviewer, originalEvidence
}
```

The revision order is the ordered published update stream, not a guessed timestamp or hash ordering. For conflicting changes to one ID within a window, use only the provider's documented application order. If it does not resolve the ambiguity, keep raw facts and block normalization for that identity.

## Exact interpretation

```text
interpretPlaidChange(change, rawPage, streamProfile):
    require published generation, account matches exact configured account filter
    require known change kind and supported account/currency profile
    if removed:
        return Removed(providerId, rawLocator)  # Do not require an amount absent in removal schema.
    x = parse raw JSON amount lexeme as rational decimal, not JS Number
    scale = qualified currency metadata; reject unknown unofficial currency
    providerMinor = exactConvertToMinor(x, scale)  # fractional minor units refuse
    cashMovementMinor = -providerMinor
        # Transactions API positive means money leaving the account [X03].
        # Initial admission profile is a supported deposit/cash account, not arbitrary investment data.
    dates = retain provider date, authorization date and datetime independently
    postingDateCandidate = explicit profile's reviewed booking-date mapping
    return Revision(..., amount=cashMovementMinor, dates,
                    pending=provider.pending, pendingRef=provider.pending_transaction_id)
```

Descriptions and counterparty enrichment are source assertions. They do not establish accounting purpose, account ownership or VAT.

## Material changes

```text
applyPublishedRevision(revision):
    inside withAdmittedPrincipal(..., (tx, principal) => ...) with the book lock:
        recover same source revision if already retained
        old = current head for exact provider identity
        append revision; advance head/version
        if pending:
            retain as nonfinancial pending observation
            no final bank admission or accounting preparation
        else if provider explicitly links a pending predecessor:
            link pending lineage; preserve predecessor bytes
            require predecessor cannot already be a separately accepted final economic observation
            otherwise raise overlap case, do not silently combine financial capacities
        if old admitted or matched:
            if amount/currency/booking-date/removal materially changes meaning:
                append source-change impact case with old admission/match/voucher refs
                mark current matching/coverage eligibility stale
                preserve old bank observations, matches and vouchers
            else retain nonfinancial metadata change without rewriting old snapshots
```

## Reviewed admission and file overlap

```text
prepareBankAdmission(revision, overlapDecision?):
    require terminal supported observation, current revision, no unresolved material conflict
    if an evidenced CSV/feed same-event relation exists:
        adopt existing economic observation with additional provenance
        require amount/currency/date semantics reconcile under explicit decision
        do not create a second observation or cash capacity
    else if unresolved lookalike exists:
        show candidates and require same/different decision; do not deduplicate automatically
    else:
        prepare exact ordinary bank observation through existing intake owner

executeBankAdmission(command):
    return withAdmittedPrincipal(access, scope, bankAdmissionPermission, (tx, principal) =>
        lock book; replay exact command first
        load plan, source revision, publication and overlap-decision dependencies
        BankSourceDomain.assertCurrentReviewedAdmission(plan, current)
        approval = validate required source-review authority using C5
        if plan adopts existing economic observation:
            observation = existing exact same-book observation
        else:
            observation = BankIntakeApp.admitWithinTransaction(tx, plan.normalizedObservation)
        BankSourceDb.insertAdmissionAndProvenance(tx, plan, observation)
        BankSourceDb.bumpAffectedMembership(tx, plan)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: [], observation}, approval)
    )
    # No journal or bank match is created by ingestion.
```

A provider feed page contains no guaranteed independent opening/closing balance. Require real statement/coverage evidence for reconciliation signoff. A removed transaction that had already been booked becomes an investigation/correction workflow, never an automatic deletion or reversal.

UI distinguishes pending, source-reviewed, admitted, matched and accounting-complete. An outdated match stays visible with its original basis and a material-source-change warning.

Vectors: repeated source revision -> one observation; two identical legitimate IDs -> two; pending predecessor + evidenced posted successor -> one final observation; changed matched amount -> impact case; removed matched observation -> no automatic ledger delta.

Evidence baseline: S10/S11; external sign/schema behavior [X03].


---

<a id="part-13"></a>

# NEXT-11: Separate complete-book SIE4E export

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/reports/sie4e.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/reports/sie4e.ts` or the existing equivalent owner |
| Pure calculation | Complete-book SIE encoding and semantic comparison |
| Atomic scope | Capture is consistent; rendering/validation is external to financial tx; attachment is a short tx. |
| Prerequisites | NEXT-02, NEXT-13 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-02/13 and on NEXT-14 where the selected book has dimensions. Preserve the current `openerp-sie4i-v1` renderer and old bytes. Format qualification remains tied to the actual SIE specification [X07].

## Frozen capture

```text
FullBookSieCapture immutable {
  profile: supported_sie4e_version, fiscalYear, asOf,
  entityRevision, openingBasisId, ledgerBoundary, recordedCutoff,
  completeAccounts, originalDimensions, completeVoucherMembership,
  rawOpeningByAccount, rawClosingByAccount, nominalPeriodMovements,
  objectAndPeriodBalancesWhereRequired, source/nativeIdentityMap,
  independentChecks, coverageLimitations, rendererRelease, generationDate
}
```

The capture is a complete selected-book export through `asOf`, not a assertion that the fiscal year is closed or all external source events are known. If `asOf` precedes year end, disclose year-to-date scope. Do not fabricate future activity. Empty but genuinely established books may export required metadata/balances without dummy vouchers.

```text
captureFullBook(year, asOf):
    under consistent snapshot / shared book barrier:
        resolve reviewed entity and fiscal dates
        resolve one opening representation from NEXT-13
        select complete committed groups through asOf and cutoff
        capture all accounts, including inactive accounts used by selected history
        capture original dimensions and all referenced object declarations
        calculate raw account balances from opening plus included actual journal lines
        capture full original descriptions and voucher identifiers, not display truncations
        if any required source cannot be represented: block export with precise diagnostics
        persist fixed membership and financial rows; page later from this snapshot only
```

## Renderer

```text
renderSie4E(capture, formatRelease):
    require capture profile supported by exact formatRelease checksum
    require source text representable in chosen declared encoding
    w = strict record writer using that specification's quoting/escaping/line ending rules
    w.record('#FLAGGA', 0)
    w.record('#PROGRAM', retainedProgramName, rendererRelease.version)
    w.record('#FORMAT', selectedEncodingToken)
    w.record('#GEN', capture.generationDate)
    w.record('#SIETYP', 4)
    w.record('#FNAMN', capture.entityRevision.legalName)
    w.record('#ORGNR', qualifiedOrganizationNumberRepresentation)
    w.record('#RAR', 0, fiscalYear.start, fiscalYear.end)
    w.record('#VALUTA', functionalCurrency)
    w.record('#PROSA', exact as-of and known completeness limitations)
    for account in stable numeric-code ordering:
        w.record('#KONTO', account.code, account.frozenName)
        emit supported type/SRU metadata only from qualified mappings
    for dimension/value in frozen supported object map:
        emit '#DIM' and '#OBJEKT' records using retained numeric dimension mapping
    for balance-sheet account:
        emit '#IB' for established opening and '#UB' for captured closing
    for nominal account:
        emit '#RES' using RAW specified result-account balance semantics
        # Not a copied presentation P&L. Mechanical result-transfer lines remain in raw data.
    emit required object/period balance record families from same capture
        # '#OIB', '#OUB', '#PSALDO' or other records only under the pinned specification.
    for complete voucher in native fiscal-year/series/number ordering:
        emit '#VER' with frozen native identity, dates and full description
        begin block
        for original line in exact ordinal order:
            emit '#TRANS', code, original object bag, signed decimal amount,
                 applicable date, original description, supported quantity/sign fields
        end block
    require every captured voucher and line emitted exactly once
    require every required record family present or validly omitted under format profile
    return strict bytes without substitution/transliteration
```

Native voucher IDs/numbers describe the target ledger. Source voucher identifiers remain separate provenance, not silently substituted for native identities. Where historical native numbering differs, include the permitted source description/reference and a sidecar identity map.

`#RES` must not be replaced by the adjusted financial-statement display of annual profit. After a result-transfer bridge, the raw nominal transfer account and all ordinary nominal balances still describe the ledger. Independent format validation establishes their correct encoding.

## Reconciliation and artifact lifecycle

```text
checkSemanticExport(capture, independentlyParsedOutput):
    match entity/year/currency and required account/object declarations
    compare every native voucher identity, ordered line amount and dimension assignment
    compare record counts and exact opening/movement/closing control totals
    assert opening[a] + actualMovements[a] == closing[a] for each supported account
    assert no omitted nonzero account or unknown historical opening silently became0
    reject unexpected parser loss warnings even if parsing returned success
```

Generate bytes outside the financial transaction. Store immutable content and then attach the verified digest/length to the capture. Repeated downloads return those bytes, not a newly rendered file with today's date. A failure to store/validate leaves a captured or rendered-but-unvalidated export, never an accepted format.

A dimension-bearing book is blocked until object mapping is supported. No empty `{}` substitution. A parser that accepts a subset is an independent check of that subset, not blanket destination compatibility.

Evidence baseline: S13/S14/S15 and official format-family description [X07].

## Application capture, rendering and attachment

```text
prepareFullBookExport(command):
    withAdmittedPrincipal(access, scope, exportPermission, (tx, principal) =>
        lock book for a consistent capture; replay the command
        rows = SieDb.loadCompleteSelectedYear(tx, scope, selection)
        basis = ReportDomain.selectOpeningAndRawMovements(rows)
        SieDomain.validateRepresentableCompleteSelection(basis, qualifiedFormatRelease)
        capture = SieDb.insertCaptureAndMembership(tx, basis)
        OutboxDb.insert(tx, render request bound to capture + renderer version)
        return CommandDb.save(tx, principal, command, capture)
    )

renderFullBookExport(job):
    capture = application read of exact saved capture under current authority
    bytes = SieDomain.renderSie4E(capture, pinnedFormatRelease)
    validation = independent exact-profile format/semantic check outside financial tx
    objectManifest = retain immutable verified bytes
    withAdmittedPrincipal(serviceAccess, scope, artifactPermission, (tx, principal) =>
        lock book; replay artifact attachment key
        require exact capture/renderer/format identities and verified byte hash
        insert artifact attachment and validation result through tx
        save receipt; do not infer destination acceptance
    )
```

The Bun effect-mq handler runs rendering/validation outside financial transactions. An already captured historical export remains renderable without changing it to current balances. Future account labels or tax profiles do not replace captured values. The database supplies bounded joins, storage and integrity, not a SIE feature procedure.


---

<a id="part-14"></a>

# NEXT-12: Historical open-item adoption

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/imports/historical-items.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/imports/historical-items.ts` or the existing equivalent owner |
| Pure calculation | Historical residual and existing-control-pool conservation |
| Atomic scope | Live obligation adoption and pool assignment commit without new recognition. |
| Prerequisites | NEXT-02 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-02. Financial basis already belongs to the historical import/OpeningSet owner. Adoption adds live settlement identity, not another journal.

## Data model

```text
ControlPool immutable {
  id, book, historicalBasisId, cutoverDate, direction: AR|AP,
  currency, scale, controlAccount, exactReviewedResidual,
  supportingGLBasisRefs, independentSourceControlDigest
}
HistoricalAdoption immutable {
  sourceItemIdentity UNIQUE per book/source system,
  historicalBasisId, controlPoolId, residualAtCutover,
  originalFaceAmount: Known(amount)|Unknown,
  priorPayments: EvidencedReferences|Unknown,
  sourceIssueDate: Known(date)|Unknown,
  liveObligationId, receiptId
}
PoolAssignment immutable {controlPoolId, adoptionId, amount}
```

The pool is a partition of an existing reviewed GL basis. It is not a new ledger balance. Construct separate AR/AP and debit/credit-direction pools where needed; do not use one net account balance to hide offsetting supplier/customer credit positions.

## Adoption

```text
prepareAdoption(sourceItem, pool):
    require source item is from the selected reviewed historical inventory
    require exactly one selected financial basis: full_history XOR opening_set
    require pool's GL identity and independent source total verified
    require item currency/direction/control account match pool
    residual = exact evidenced outstanding at cutover
    require residual >0; zero items remain historical evidence without live capacity
    require item not already adopted or represented by an existing native obligation
    used = sum(effective pool assignments)
    require residual <= pool.exactReviewedResidual-used
    require source item belongs to complete reviewed control partition
    seal adoption with pool/version/source digests and unknown-history fields intact

executeAdoption(command):
    return withAdmittedPrincipal(access, scope, historicalAdoptionPermission, (tx, principal) =>
        lock book; replay exact command first
        load adoption plan, reviewed source item, control pool and effective assignments
        require source/basis versions current and no duplicate native obligation
        HistoricalDomain.assertConservedPoolAssignment(plan, current)
        approval = validate exact adoption approval using C5
        obligation = CommerceApp.adoptHistoricalItemWithinTransaction(tx, {
            openingResidual: plan.residual,
            sourceHistory: immutable source references,
            kind: historical_open_item_v1
        })
        adoption = HistoricalDb.insertAdoptionAndPoolAssignment(tx, plan, obligation)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: [], obligation, adoption}, approval)
    )
    # No new recognition journal and no financial ledger sequence increment.
```

If native full-history import already established the same live obligation, adopt provenance onto that identity rather than create another. A per-line recognition amount100000 is not automatically a40000 residual pool after60000 historical payments; prove the complete net basis first.

## Later lifecycle

```text
historicalObligationRemaining(item, cutoff):
    return openingResidual
           - effective NEW settlements through cutoff
           - supported NEW credit reductions through cutoff
           + supported owned correction effects
    # Do not subtract historical payments again.

settleAdoptedItem(item, newPayment):
    use current commerce settlement owner with historical_open_item adapter
    conserve new payment and residual capacities
    create only payment accounting if cash is not already posted
    preserve source original amount/history as metadata, not current capacity
```

A credit requiring original line-level tax amounts cannot be compiled from residual alone. Missing detail is a specific unsupported-credit blocker; it does not prevent a separately supported payment settlement.

## Controls

```text
adoptedTotal + explicitlyUnadoptedResidual == independentlyReviewedPoolTotal
liveResidual + postCutoverSettlements + supportedCredits == adopted opening residual
```

Any unexplained control difference blocks complete-register readiness. Partial adoption is allowed with a named unadopted bucket, not labeled full migration. Avoid universal line exclusivity; enforce conflict only when the same financial basis would supply duplicate AR/AP capacity.

Vectors: original100000, evidenced prior settled60000, residual40000 -> live40000 and GL delta0; new payment10000 -> remaining30000; missing original face but evidenced residual -> payment may be supported, credit may not; duplicate adoption -> same-key replay or AlreadyApplied.

Evidence baseline: S13.


---

<a id="part-15"></a>

# NEXT-13: Semantic P&L and balance-sheet snapshots

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/reports/statements.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/reports/statements.ts` or the existing equivalent owner |
| Pure calculation | P&L/BS mapping, opening selection, virtual result and subtotal graph |
| Atomic scope | Immutable snapshot membership and calculation persist through the reporting app owner. |
| Prerequisites | NEXT-02 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-02. Extend the frozen report/contribution authority. A correct arithmetic statement and complete company records are separate statuses.

## Mapping and contribution model

```text
StatementMappingRelease immutable {
  framework, effectiveFiscalRules, checksum,
  accountRoleRules,
  leafRows: [{rowId, statement, side, contributionPredicate, presentationSign}],
  subtotalDAG, mechanicalTransferRoles, comparativePolicy
}
SemanticSnapshot immutable {
  ledgerBoundary, recordedCutoff, fiscalYear, selectedInterval,
  openingBasisId, mappingRelease, factRevisions,
  leafContributions, rows, calculationNodes, diagnostics, coverage
}
```

Only a reviewed mapping may assign a financial contribution to a row. Require exactly one ordinary leaf destination per relevant account/component for a statement. Subtotals are calculations over leaves, not additional financial contributions. Contra accounts keep their signed effects. Do not infer every8xxx account as an expense.

## Opening and movement selection

```text
selectStatementBasis(year, asOf, cutoff):
    opening = latest authorized immutable OpeningSet for year at cutoff
        OR explicitly reviewed prior native balance basis for initial implementation
    require opening representation selected exactly once
    movements = complete committed journal groups with accountingDate in year..asOf
                and commitBoundary <= cutoff.boundary
    if opening is represented by an opening voucher:
        exclude that voucher from movements, retain it as opening provenance
    require no other overlap between opening coverage and selected movement identities
    return {opening, movements, cutoff}
```

A captured report is never filled later from current account labels, live profile facts or a newer movement cutoff.

## Calculation

```text
calculateStatements(basis, mapping, requestedPLInterval):
    rawClosing[a] = opening[a] + sum(actual movement debits-credits[a])
    periodActivity = movement components within requestedPLInterval
    yearOrdinaryPL = all year movements classified as nominal activity by mapping,
                     excluding only OWNED mechanical result-transfer components
    ordinaryPL = yearOrdinaryPL restricted to requestedPLInterval
    profitForInterval = -sum(ordinaryPL.signedAmount)
    fiscalYtdProfit = -sum(yearOrdinaryPL.signedAmount)
    transferredYtd = net credit to year-result equity from owned result-transfer receipts
    virtualUntransferredResult = fiscalYtdProfit-transferredYtd

    for component in ordinaryPL:
        leaf = require exactly one mapped P&L leaf
        add contribution(component.id, rawSigned, presentationSign)
    for balance-sheet account:
        leaf = require exactly one mapped BS leaf
        add opening and actual movement contributions with their original signs
    add a COMPUTED equity row for virtualUntransferredResult
        # No journal entry; explanation points to P&L and actual transfer receipts.
    evaluate subtotalDAG in topological order
    require all nonzero unassigned/ambiguous accounts remain in diagnostics
    check assets == liabilities + equity including virtual result
```

The BS virtual result is fiscal-year-to-date, not the P&L's arbitrary one-month slice. Retained earnings brought forward belongs to the opening basis. A first year does not imply that its opening is zero.

For a result-bridge closing style, ordinary revenue/expense entries remain in place and a separate nominal transfer role balances the year-result equity posting. Report exclusion uses the owned financial role, not merely a suspicious account number or text label. An unexplained manual entry to that account remains visible and cannot silently erase P&L.

## API/UI

```text
POST statement-snapshots -> capture + calculate + seal immutable model
GET snapshot -> rows, complete-scope totals, diagnostics, basis
GET row/:id/explanation -> frozen contribution IDs or computed child nodes
GET comparison(left,right,mode) -> same-unit signed changes and mapping differences
```

Comparison either uses each original mapping with an explicit classification-change display, or a separately retained comparative-reclassification model. Do not edit the older statement to make the graphs match. Every page refers to one frozen snapshot, including opening and calculated virtual-result explanations.

Internal reports may be shown with arithmetic pass and coverage unknown. Complete/statutory readiness requires all mapped and external completeness conditions. Export JSON/CSV from the same semantic rows, not another UI-side calculation.

## Vectors

```text
cash+100000 / revenue-100000; expense+40000 / cash-40000
    => profit60000; cash60000; virtual equity60000
owned transfer nominal+60000 / year-result equity-60000
    => profit still60000; virtual result0; actual equity60000
unmapped nonzero account => visible diagnostic, complete readiness false
new backdated posting after cutoff => old snapshot unchanged
```

Evidence baseline: S15/S20. A retained report keeps its exact semantic version. No parallel legacy SQL report runtime is required for disposable development snapshots.

## Effect snapshot service

```text
prepareStatements(command):
    capture = withAdmittedPrincipal(access, scope, reportingPermission, (tx, principal) =>
        lock book for consistent capture; replay committed preparation key first
        basis = StatementDb.captureRowsAndCompleteMembership(tx, scope, selection)
        return retained fixed basis or a captured typed value with complete version witness
    )
    if capture is replay: return saved snapshot
    result = StatementDomain.calculateStatements(capture, capturedMapping, requestedInterval)
    return withAdmittedPrincipal(access, scope, reportingPermission, (tx, principal) =>
        lock book; replay exact command first
        verify retained capture identity OR recheck captured dependency witness
        snapshot = StatementDb.insertModelRowsAndContributions(tx, capture, result)
        return CommandDb.save(tx, principal, command, snapshot)
    )
```

Once the basis has been retained, later activity does not make rendering its historical statement invalid. Report currentness is a separate query. SQL computes efficient scoped raw sums and retrieves contribution rows; the pure application calculator owns opening representation, transfer exclusions, mapping selection, virtual result and subtotal DAG. Browser components render the saved model rather than recomputing totals.


---

<a id="part-16"></a>

# NEXT-14: Original dimension assignments

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/dimensions/assignments.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/dimensions/assignments.ts` or the existing equivalent owner |
| Pure calculation | Original assignment eligibility and dimension projection |
| Atomic scope | Original dimensions are inserted using the same tx as journal lines. |
| Prerequisites | None |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Report integration follows NEXT-13. Root coordinates the shared journal union and application posting admission after WIP handoff. This packet does not implement posted retagging or a generic allocation engine.

## Versioned original facts

```text
OriginalAssignment {
  dimensionCode, dimensionRevision,
  valueCode, valueRevision, capturedLabel,
  status: explicit | explicit_unassigned | historical_exemption,
  exemptionEvidence?
}
NewJournalLineV2 {
  existing financial fields,
  originalDimensions: sorted unique-by-dimension list<OriginalAssignment>
}
SourceLineWithoutDimensionEvidence -> originalDimensions = NotRecordedInSource
# The missing state is an explicit import/read fact, not an old-schema execution adapter.
```

Do not add an array to old saved JSON or recalculate its digest. Explicit unassigned, historical unknown and evidenced exemption are different buckets.

```text
validateAssignments(line, postingDate, policy, mode):
    require dimension keys unique, same book and canonical ordering
    if mode == exact_reversal:
        require assignment bytes equal referenced original line's assignments
        allow historically valid but now archived catalog values
        return
    for applicable dimension in policy:
        chosen = line.assignment(dimension)
        if fixed: require chosen == policy.fixedValueRevision
        if required: require chosen is explicit and eligible
        if default:
            resolve default during PREPARATION and retain it explicitly
            # Never insert today's default silently at execution or historical import.
        if historical_exemption: require reviewed exemption applies to this source/date
        if explicit: require dimension/value effective and allowed for new posting
    reject unknown dimensions, ambiguous revisions or incompatible multiple values
```

Plan approval covers the new line shape and policy revision. The application posting service checks exact assignments against approved lines and the supported reversal/new-posting mode before its tx-passing batch inserts. PostgreSQL retains scoped references, immutable original assignments and storage uniqueness, not dimension-default policy. A replacement correction keeps unaffected original assignments and explicitly reviews changed ones; only an exact reversal inherits archived values automatically.

## Projection

```text
projectOneDimension(snapshot, dimension):
    buckets = [each frozen value, explicit_unassigned, not_recorded_in_source, exempt]
    for contribution in snapshot.financialContributions:
        bucket = resolve original assignment or proper missing-state bucket
        append contribution exactly once to bucket
    require sum(bucket amounts) == unfiltered snapshot amount

projectCrossTab(snapshot, dimensions):
    key = ordered tuple(one original assignment state per requested dimension)
    assign each contribution to exactly one tuple
```

Do not sum totals across separate dimension systems: cost-center totals and project totals each independently partition the same money. Also do not require each cost center to have a balanced balance sheet unless a specific complete allocation policy exists. No artificial balancing lines are created to make dimension filters look balanced.

## SIE handoff

```text
freezeObjectMap(catalog, usedAssignments):
    preserve stable exported numeric dimension IDs and original value codes
    require every emitted assignment has a matching declared dimension/object
    preserve historical code aliases explicitly when a native code differs
    refuse unsupported loss rather than emit empty object lists
```

Retagging later needs its own reviewed classification history and `original` versus `reclassified` report modes. It cannot mutate `originalDimensions` or previously exported files.

Vectors: A100+B200+unassigned50+legacy25 -> unfiltered375; archive A then reverse original -> exact -100 in originalA; new posting with archivedA -> refuse; two different dimension partitions both total375, not750.

Evidence baseline: S16/S27/S14.

## In-transaction journal integration

```text
applyOriginalAssignmentsWithinTransaction(tx, validatedJournal, insertedLineIds):
    require validatedJournal was prepared under its pinned dimension policy
    assignments = DimensionDomain.validateAssignmentsForEveryLine(validatedJournal)
    require one immutable assignment state per applicable line/dimension
    DimensionDb.insertOriginalAssignmentsBatch(tx, insertedLineIds, assignments)
    # Caller owns journal, assignments, approval use and receipt in one tx.
    # No public assignment API may append classifications to an already posted line.
```

Historical exemptions and unrecorded source values remain explicit inputs. Exact reversals inherit original assignments even when a catalog value is now archived. Adding dimensions never grants permission to modify posted amounts or bypass the pending WIP owner.


---

<a id="part-17"></a>

# NEXT-15: Legal customer credit notes

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/sales/credit-notes.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/sales/credit-notes.ts` or the existing equivalent owner |
| Pure calculation | Qualified legal credit, source-line limits and tax corrections |
| Atomic scope | Number, journal, AR reduction, tax facts, semantic document and outbox share one tx. |
| Prerequisites | NEXT-02 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-02; actual return integration follows NEXT-04. Preserve WIP webshop/order/catalog ownership. Reuse current legal-issue policy and native accounting boundary, never synthetic cancellation.

## Credit record

```text
CustomerCreditPlan {
  originalLegalIssueId, originalDocumentHash,
  sourceCreditDecisionIdentity, reason, creditDate, datePolicy,
  selectedLines: [{originalLineId, creditedNet, creditedTax,
                  priorCreditedNet, priorCreditedTax}],
  currentUnpaidCapacity, legalPolicyWitness, taxCorrectionWitness,
  semanticCreditDocument, expectedInvoiceVersion
}
UNIQUE(book, sourceCreditDecisionIdentity)
UNIQUE(book, creditSeries, creditNumber)
```

Credit-note numbering belongs to the reviewed issue policy. Allocate it during the atomic issue transaction. Never fetch today's catalog price or re-open converted-order quantity just because a credit is issued.

## Compiler

```text
compileCustomerCredit(original, capacity, input, profile):
    require original belongs to existing supported legal domestic sale family
    require each original source line appears at most once in request
    for credit line:
        require n>=0, t>=0 and n+t>0
        require n <= original.net-priorCreditedNet
        require t <= original.tax-priorCreditedTax
        require credit evidence and qualified original-rate/rounding contract hold
        # Full final line credit uses its exact remaining original tax.
        Journal.addSigned(original.revenueRole, +n)
        Journal.addSigned(original.outputVatRole, +t)
        append tax correction with base=-n, outputTax=-t,
               adjusts=original recognition component and qualified tax period
    g = sum(n+t)
    require g <= current unpaid balance
    Journal.addSigned(original.receivableRole, -g)
    finish()
    freeze legal document fields, original references and reason
```

The bounded path rejects paid-principal excess. It does not secretly create a customer credit balance or cash refund. Foreign tax, mixed treatments or unsupported credit chronology receive specific profile failures.

## Atomic issue plus asynchronous rendering

```text
executeLegalCredit(command):
    return withAdmittedPrincipal(access, scope, legalCreditPermission, (tx, principal) =>
        lock book; replay exact command first
        load exact plan and current original issue/line/payment/tax-policy basis
        require issue-date boundary still valid, including required day-rollover refusal
        CreditDomain.assertLineCapacityAndUnpaidConservation(plan, current)
        approval = validate exact legal-credit approval using C5
        creditNumber = CounterDb.allocateRollbackSafeNumber(tx, plan.legalSeries)
        journal = JournalApp.postWithinTransaction(tx, plan.journal)
        credit = SalesDb.insertCreditAndReceivableEffects(tx, plan, creditNumber, journal)
        tax = TaxFactApp.recordAdjustmentsWithinTransaction(tx, plan.taxFacts, journal)
        document = SalesDb.insertImmutableCreditSemanticRevision(tx, plan, creditNumber)
        OutboxDb.insert(tx, render intent referencing document and renderer version)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journal.ids, credit, tax, document}, approval)
    )
    # Bytes are rendered afterward by the Bun job handler. Issuance does not repeat.
```

If rendering fails, the legal credit and journal still exist and recover by their receipt. Rendering resumes from the retained semantic revision. It never issues another number or recalculates tax from newer customer details. The UI distinguishes issued-but-artifact-pending from not issued.

Reflect credit effects in ageing, statements, collection eligibility and reminder dispatch rechecks. Existing invoice bytes and prior payments remain unchanged. Dispatch of a reminder sees current unpaid/dispute status rather than the old statement's historical outstanding amount.

For existing legal invoices without owned tax-fact publication, require an explicit original-recognition adoption through NEXT-04 before producing tax corrections. Do not fabricate an original fact, and do not call a partial bookkeeping-only path complete statutory credit support.

Vectors: original10000+2500, credit4000+1000 -> remaining7500 before payments; second credit beyond remaining source tax -> refusal; day rollover -> no numbering/posting; duplicate key -> same receipt; new key same economic credit -> AlreadyApplied; credit does not restore order-to-invoice conversion capacity.

Evidence baseline: S17/S07/S03.


---

<a id="part-18"></a>

# NEXT-16: Evidence-aware period preparation

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/automation/period-work.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/automation/period-work.ts` or the existing equivalent owner |
| Pure calculation | Evidence-aware routing, rule selection and fixed approval manifest |
| Atomic scope | Public prepares/executes own their tx; separate run checkpoint recovery bridges calls. |
| Prerequisites | NEXT-01, NEXT-03, NEXT-06 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-01/03/06. Extend existing recurring run/checkpoint ownership. Keep automatic posting mandates out of this packet.

## Rules and manifest

```text
PreparationRule immutable {
  legalSupplierIdentity, supportedDocumentClass, currency,
  qualifiedTreatmentId, acceptedEvidenceRequirements,
  operationFamily, approvedExamples, negativeExamples,
  version, activationReview
}
PeriodWorkManifest immutable {
  scope, requestedInterval, cutoff, sourceCoverage,
  children: [{workIdentity, economicIdentity, sourceRevision,
             existingRecognitionRef?, existingMatchRefs, intendedOwner}],
  digest
}
WorkChild state {
  pending | waiting_predecessor | needs_review | prepared(planRef)
  | recovered(receiptRef) | committed(receiptRef) | refused(reason)
}
```

Frozen membership excludes later arrivals. A new manifest can select them explicitly. Do not copy a bank row into a new purchase identity when a matched invoice already establishes its recognition.

## Deterministic routing

```text
routeWork(child, currentEvidence, activeRules):
    identity = resolve reviewed economic relationships using preserved matches
    if committed purchase exists AND child is new bank/owner payment:
        return existing obligation's settlement owner
    if expense was paid by owner and not recognized:
        return OwnerPaidPurchase
    if new supported supplier invoice:
        return SupplierRecognition
    if source revises already recognized facts:
        return owned correction/credit review, not new recognition
    otherwise:
        return ReviewCase(exactMissingFacts)

selectRule(event):
    candidates = exact active conditions matching invoicing entity, class, currency and treatment
    require one unambiguous candidate and required evidence
    changed supplier entity, eligibility or source amounts -> needs_review
    # AI may propose missing facts/rules. It cannot supply confirmed facts or approval.
```

## Resumable preparation

```text
advanceManifest(runId, expectedFence, boundedCount):
    # Invoked by the effect-mq Bun handler, not a new queue implementation.
    for next pending child in fixed order:
        claim/check child business revision in a short application tx
        require current run cancellation/checkpoint version
        # Queue claims belong to effect-mq; child version fences domain result publication.
        re-read current source/recognition dependencies
        target = routeWork(...)
        if already posted: store recovered receipt, no new proposal
        if needs evidence/decision: store precise case; continue independent children
        if prerequisite child uncommitted: waiting_predecessor; continue independent children
        otherwise:
            key = stable key derived from run child and requested immutable revision
            plan = call existing domain PREPARE application operation with this key
                # No caller DB transaction is held while this public operation runs.
            in a new short run-owned application tx:
                replay checkpoint command
                recheck child revision and run cancellation version
                persist planRef + child checkpoint + receipt together
            # Crash between domain preparation and checkpoint is repaired by domain-key recovery.
```

No current agent tool approves on behalf of a human. Rule activation approves a treatment-selection rule, not every future journal.

## Fixed-manifest human approval

```text
prepareApprovalBatch(selectedPreparedChildren):
    require each child has an existing sealed plan and explicit owning operation
    require selected children independently executable or one existing atomic domain aggregate
    manifest = [(owner, planId, digest, inputIdentity) in deterministic order]
    show exact journals, source references and combined informational totals
    seal batch digest

approveBatch(command, humanAccess):
    return withAdmittedPrincipal(humanAccess, scope, batchApprovalPermission, (tx, principal) =>
        lock book; replay exact command first
        load exact sealed batch and batch member plans in a bounded set
        lock dependency/approval resources in the complete shared ordering
        for member:
            require exact digest, owner-specific approver rules and current basis
        approvals = for each member:
            owner.approveWithinTransaction(tx, principal, exact member plan)
            # Internal operation only. It never opens a new transaction or calls HTTP.
        persist batch-to-child-approval memberships and receipt through tx
        return exact batch result
    )
    # One human gesture approves exact members, not future arrivals or ordinary-agent powers.

executeApprovedBatch(batch):
    for member:
        dispatch ONLY to member's owning execution with stable captured request/key
        on response loss: recover same member; do not move to a new key
        on stale member: mark needs new review, keep other independent members runnable
        persist each receipt and honest partial progress
```

A child whose financial effects depend on an unknown predecessor result cannot be smuggled into the preapproved batch. Prepare it after the predecessor commits, then obtain the required new approval, unless an existing single aggregate explicitly owns both effects.

New narrow-dependency plans may avoid unrelated global-sequence staleness. Plans retained in the released replacement keep their exact approved dependency interpretation. Disposable old-schema fixtures do not require a fallback SQL workflow.

Counts distinguish prepared, committed, blocked and unresolved. A run with all children visited is not a reconciled period. That requires the separate source/control inventory.

UI focus is exceptions and exact approvals. Return compact structured context with source/case/plan references; let agents fetch evidence only for unresolved cases. Existing retained operations remain the recovery authority after reload.

Vectors: known recurring invoice -> same plan as manual purchasing; invoice already recognized + bank debit -> settlement; rule ambiguity -> review; crash after prepare -> recover same plan; stale one member -> other independent children continue; approval of batch never approves later added child.

Evidence baseline: S18/S05/S07.

The job's queue acknowledgment may be lost after the domain operation succeeds. Recover the prepared/committed child through the same domain command identity before changing progress. A cancellation after preparation keeps the prepared plan as retained evidence but prevents the stale handler from publishing new work or executing anything. Financial execution, when separately authorized, still goes through each owner's public execute service with its existing approval and economic receipt.


---

<a id="part-19"></a>

# NEXT-17: Payable FX and explicit fees

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/commerce/fx-settlements.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/commerce/fx-settlements.ts` or the existing equivalent owner |
| Pure calculation | Payable/receivable signed consideration and fee compiler |
| Atomic scope | Journal and released WIP paired-capacity consumption share one tx. |
| Prerequisites | NEXT-02 |
| Reserved handoff | WIP-FX02-P1 |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Wait for WIP-FX02-P1. Use its paired-release result and existing commerce monetary item. NEXT-03 supplies qualified purchase recognition where applicable. Do not copy the WIP partial-release algorithm into this packet.

## Inputs

```text
FxSettlementInput {
  monetaryItemId, direction: receivable|payable,
  requestedOriginalUnits,
  considerationEvidence: {grossBookMinor K, actualCashSources},
  fees: [{sourceIdentity, bookMinor, expenseRole, treatmentWitness}],
  settlementDate, expectedCapacityVersion,
  releasedPrincipalPlanFromWip
}
```

Fees must be in book currency in this profile. Fee tax, foreign cash, hedges and multilateral netting require separate supported treatment or refusal. `K` is evidenced gross settlement consideration, not the current exchange-rate quote multiplied by principal.

## Supplier monetary-item recognition

```text
prepareForeignPayable(purchase):
    require qualified original-currency obligation and book-value recognition witness
    if current commerce owner already supports that payable variant: use it
    else add discriminated foreign payable variant through same owner
    retain original units and carrying value from purchase recognition
    preserve existing synthetic_invoice_v1 meanings and amounts
    return a purchase-owned aggregate for one application tx containing journal, paired payable basis and tax facts
    # This compiler does not call a public purchase execution or open a transaction.
```

The operation cannot make a supplier payable by relabeling an already retained book-currency number as foreign units.

## Compiler

```text
compileSettlement(basis, input):
    release = FxDomain.planPairedRelease(basis, input.requestedOriginalUnits)
    b = release.bookCarryingReleased
    K = input.grossBookConsideration
    F = sum(input.fees.bookMinor)
    require K>=0 AND F>=0 and fee source identities unique
    if receivable:
        signedCash = K-F
        require signedCash >=0 for initial supported net-receipt profile
        gain = K-b
        Journal.addSigned(cashOrQualifiedClearingRole, +signedCash)
        Journal.addSigned(receivableControl, -b)
    else:
        signedCash = -(K+F)
        gain = b-K
        Journal.addSigned(cashOrQualifiedClearingRole, signedCash)
        Journal.addSigned(payableControl, +b)
    for fee:
        Journal.addSigned(fee.expenseRole, +fee.amount)
    if gain>0: Journal.addSigned(realizedFxGainRole, -gain)
    if gain<0: Journal.addSigned(realizedFxLossRole, -gain)
    require sum(actualCashSources.signedBookAmounts) == signedCash
    require no fee or cash source is consumed by another financial operation
    return {journal: finish(), pairedRelease: release, K,F,gain, sourceBindings}
```

`cashOrQualifiedClearingRole` is explicit. For an unposted bank observation, it is cash and the operation creates that cash movement once. For an already posted bank receipt/payment, only a supported settlement-clearing posting with proven unused capacity can be adopted. Use its clearing side and create no second cash entry. An arbitrary existing AP/AR journal is not a clearing witness.

When fees are a separate bank debit rather than withheld from the principal receipt, retain separate cash lines/source links whose signed total agrees with the equation. Do not manufacture one net observation or match one source twice.

```text
executeFxSettlement(command):
    return withAdmittedPrincipal(access, scope, fxSettlementPermission, (tx, principal) =>
        lock book; replay exact command first
        load exact plan and current commerce monetary-item/source/fee capacities in batches
        require WIP paired release still binds this exact item, version and ordered legs
        FxSettlementDomain.assertApprovedDirectionAndConservation(plan, current)
        approval = validate exact FX approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal)
        paired = FxApp.applyPairedConsumptionWithinTransaction(tx, plan.pairedRelease, journal)
        links = FxDb.insertSettlementFeeAndSourceEffects(tx, plan, paired, journal)
        FxDb.bumpAffectedControlVersions(tx, plan)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journal.ids, paired, links}, approval)
    )
```

Latest-unconsumed settlement correction delegates to the existing FX correction owner and restores journal, both capacities and fee/source rights together. A no-journal unallocation cannot reverse realized FX. Consumed later settlement/valuation history refuses unsupported standalone correction.

## Vectors with b supplied by WIP

```text
payable b110000 K112000 F1000:
    AP+110000, FXloss+2000, fee+1000, cash-113000
receivable b110000 K112000 F1000:
    cash+111000, fee+1000, AR-110000, FXgain-2000
payable b110000 K108000 F1000:
    AP+110000, fee+1000, cash-109000, FXgain-2000
b0 is allowed only when WIP supports that exact principal release:
    no zero AP/AR line, but principal consumption and remaining effects stay explicit
```

Evidence baseline: S03/S07 and released WIP contract. No new foreign-principal capacity owner.


---

<a id="part-20"></a>

# NEXT-18: Incremental open-item FX remeasurement

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/commerce/fx-valuations.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/commerce/fx-valuations.ts` or the existing equivalent owner |
| Pure calculation | Complete-population target carrying and incremental FX differences |
| Atomic scope | All selected carrying changes, journal and valuation receipt commit as one group. |
| Prerequisites | NEXT-17 |
| Reserved handoff | WIP-FX02-P1 |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-17 and released WIP-FX02-P1. ADR 0008 selects incremental valuation without an automatic next-period reversal.

## Valuation basis and identity

```text
ValuationBasis immutable {
  book, currency, accountingCutoff, recordedCutoff,
  completeEligibleItemMembership, populationEpoch,
  items: [{itemId, originalRemaining, bookCarrying,
           capacityVersion, recognitionAndSettlementLineage}],
  rateRevisions, valuationPolicy, priorValuationRefs
}
ValuationEffect immutable {
  itemId, cutoff, economicDecisionId, priorCarrying, targetCarrying,
  delta, rateWitness, journalRefs, predecessorEffect?, receiptId
}
UNIQUE(book, itemId, cutoff, economicDecisionId)
```

The eligible set is explicit by book, currency and valuation purpose. A bounded query must prove it selected all items in that scope or fail with a narrower permitted scope. Do not value the first page and call it a complete remeasurement.

## Calculation

```text
prepareValuation(selection):
    capture current unhedged supported monetary items as of accounting+recorded cutoff
    require no item with unsupported later consumption across the selected cutoff
    # Backdating across already posted settlements needs a separate full correction chain.
    for item:
        T = convertMinor(item.remainingOriginal, originalScale, bookScale,
                         selectedReportingRate, qualifiedRounding).minor
        B = item.currentBookCarrying
        delta = T-B
        controlSigned = delta if item is receivable else -delta
        Journal.addSigned(item.controlRole, controlSigned)
        if controlSigned>0: Journal.addSigned(unrealizedGainRole, -controlSigned)
        if controlSigned<0: Journal.addSigned(unrealizedLossRole, -controlSigned)
        effects += {item, B,T,delta, witness}
    return seal plan with complete membership, journal and effects
```

Receivable appreciation debits the asset and credits a gain. Payable appreciation credits the liability and debits a loss. A no-delta item is retained in the valuation membership and decision result without a zero journal line.

```text
executeValuation(command):
    return withAdmittedPrincipal(access, scope, valuationPermission, (tx, principal) =>
        lock book; replay exact command first
        load exact valuation plan and complete eligible scope membership
        load all selected item capacities, rate revisions and cutoff restrictions in batches
        require population and every item version still match
        require no intervening settlement, credit or unsupported backdated consumption
        ValuationDomain.assertAllTargetsAndSignedDeltas(plan, current)
        approval = validate exact valuation approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal) if nonempty else []
        effects = FxApp.applyValuationEffectsWithinTransaction(tx, plan.effects, journal)
        valuation = FxDb.insertResultAndCutoff(tx, plan, effects, includingNoEffectItems)
        bump owned item/control/closing dependency versions through tx
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: ids(journal), valuation, effects}, approval)
    )
```

A new approved reporting-rate revision at the same cutoff is an explicitly superseding economic decision. Compute only its new target less CURRENT carrying. Do not reapply its original delta or overwrite the previous effect. Reject correction after later consumption unless the owned chain-repair workflow is available.

## Later settlement and controls

```text
settlementBasis(item):
    initialCarrying + effectiveValuationDeltas - effectiveCarryingReleases

controlExpected(currency, cutoff):
    sum each eligible item's signed carrying under its direction
    compare to its exact owned GL control contributions
    expose unassigned/unexplained control lines, not merely net difference
```

Foreign quantity does not change when valued. Rate withdrawal affects new use/readiness and can create a review case; it does not erase historical carrying values. Keep valuation P&L and settlement P&L attribution separate. A later classification-only realized/unrealized reclassification, if required, is not another economic gain.

## Vectors

```text
AR initial110000 -> target115000: AR+5000 / valuationGain-5000
later settlement116000 releases115000: cash+116000 / AR-115000 / realizedGain-1000
total gain6000, not11000
AP110000 ->115000: APLiability-5000 / valuationLoss+5000
zero delta: receipt with complete membership, no voucher number consumed
new item dated before cutoff while approval pending: stale population, no partial valuation
```

The first profile explicitly refuses a late year-end revaluation when later settlements already consumed its old basis. It must not pretend that refusal is a successful close; supporting such a company's history needs an owned chain-recalculation extension.


---

<a id="part-21"></a>

# NEXT-19: Disposal with proceeds

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/subledgers/disposals.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/subledgers/disposals.ts` or the existing equivalent owner |
| Pure calculation | Proceeds, tax and post-impairment disposal conservation |
| Atomic scope | Disposal journal, asset/schedule retirement and proceeds usage share one tx. |
| Prerequisites | None |
| Reserved handoff | WIP-AST03-UI |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Wait for WIP-AST03-UI release, including its final impairment/control/disposal consumers. Qualified sale VAT and legal-invoice integration are conditional prerequisites. One asset and book currency initially.

## Snapshot and conservation

```text
basis = AssetDb.captureDispositionBasis(tx, scope, assetId, cutoff)
# Captured consistently before pure compilation, through the released WIP owner.
G = gross cost
A = imported ordinary accumulation + later effective ordinary recognition
I = effective impairment
B = G-A-I
require B>=0 and exact basis current
P = qualified net proceeds, not gross cash including VAT
V = separately qualified output VAT
profit = P-B
```

Proceeds must have a unique economic relationship to this disposal. The first profile rejects allocation of a single undivided invoice line to several assets unless an explicit allocation owner supplies conserved shares.

## Two supported acquisition-of-proceeds modes

```text
compileDisposal(basis, proceeds):
    if proceeds.kind == unposted_cash_sale:
        require observed unposted cash receipt P+V and qualified tax/sale evidence
        Journal.addSigned(cashRole, +(P+V))
        Journal.addSigned(outputVatRole, -V)
        append sale tax fact(base=P, output=V)
    else if proceeds.kind == existing_legal_invoice:
        require exact asset-sale invoice line, legal issue and unused proceeds capacity
        require line.net==P and line.tax==V
        require existing invoice accounting/tax remains valid
        if invoice used a dedicated asset-proceeds clearing role:
            Journal.addSigned(assetProceedsClearingRole, +P)
        else if qualified reclassification of ordinary sale revenue is explicitly supported:
            Journal.addSigned(originalSalesRevenueRole, +P)
            # Offsets existing revenueP, leaving only disposal profit below.
        else: fail UnsupportedProceedsAccounting
        new cash, receivable and VAT facts = NONE
    else: fail UnsupportedProceedsMode

    Journal.addSigned(ordinaryAccumulationRole, +A)
    Journal.addSigned(impairmentContraRole, +I)
    Journal.addSigned(grossAssetRole, -G)
    if profit>0: Journal.addSigned(disposalGainRole, -profit)
    if profit<0: Journal.addSigned(disposalLossRole, -profit)
    return {journal: finish(), removeCarrying:B,
            stopFutureOccurrences:true, usedProceedsIdentity, basisDigest}
```

The original standard sales invoice may have already recognized revenue. Posting full proceeds again would double revenue/cash. The explicit reclassification branch debits that original revenue exactly once and replaces its P&L effect with the disposal gain/loss. It does not reverse the invoice's genuine sales/VAT facts.

Issuing a new receivable invoice and disposing simultaneously needs a single coordinated owner aggregate. Do not approximate it by calling a public invoice-issue endpoint and then an independent disposal transaction. It is outside the two initial modes unless that owner is provided.

```text
executeDisposal(command):
    return withAdmittedPrincipal(access, scope, disposalPermission, (tx, principal) =>
        lock book; replay exact command first
        load plan and released impairment-aware asset basis
        require asset not disposed and no intervening installment, estimate or impairment
        load/recheck exact proceeds identity and unused accounting capacity
        DisposalDomain.assertApprovedConservation(plan, current)
        approval = validate exact disposal approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal)
        if unposted sale mode:
            TaxFactApp.recordRecognitionWithinTransaction(tx, plan.saleTaxFacts, journal)
        disposition = AssetApp.applyDispositionWithinTransaction(tx, plan, journal)
        ProceedsDb.insertOwnedUse(tx, plan.proceedsIdentity, disposition)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journal.ids, disposition}, approval)
    )
```

The WIP asset owner remains responsible for impairment-aware ordinary recognition, controls and disposal reads. This packet adds proceeds behavior only after its handoff.

## Correction and presentation

Latest-unconsumed error correction must reverse the entire financial effect, restore valid asset/schedule state and release proceeds rights together. If a legal credit, later asset action, closed-period consumer or cash refund depends on it, refuse until a complete supported chain exists. A generic journal reversal must not resurrect the asset register alone.

Show original cost, ordinary accumulation, impairment, carrying, net/gross proceeds, VAT and gain/loss. After disposal the gross and contra controls attributable to the asset all clear, not just the carrying subtotal.

## Vectors

```text
G1000000 A300000 I100000 => B600000
P650000 V162500 unposted sale:
    cash+812500, ordinary+300000, impairment+100000,
    gross-1000000, VAT-162500, gain-50000
P550000 with already invoiced proceeds:
    originalRevenueOrClearing+550000, ordinary+300000, impairment+100000,
    loss+50000, gross-1000000
    no second AR/cash/VAT recognition
```

Actual VAT rate/eligibility is a qualified input. The example's1/4 is illustrative, not an automatic rule for every asset sale.


---

<a id="part-22"></a>

# NEXT-20: Frozen regular-payroll calculation

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/payroll/calculations.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/payroll/calculations.ts` or the existing equivalent owner |
| Pure calculation | Qualified salary, withholding and cumulative contribution calculation |
| Atomic scope | Private consistent capture and frozen calculation; no financial effect until run execution. |
| Prerequisites | NEXT-02 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-02. Build on 9050/9107 employment/work/opening records. Initial support: one explicitly supported regular salaried profile. Unsupported leave, cross-border status, special benefit treatment or unknown collective obligations block the affected run rather than becoming0.

## Typed inputs and releases

```text
EmploymentForCalculation {
  employeeId, effectiveRevision, monthlyCashSalary, workPattern,
  taxStatusEvidence, tableIdAndColumnOrDecision,
  benefitComponents[], deductionComponents[], holidayPolicy,
  pensionAndOtherObligations: SupportedTerms|EvidencedNotApplicable|Unknown
}
WorkInput {earningsPeriod, actualSchedule, absence, adjustments, reimbursements, evidence}
PayrollRuleRelease {
  applicableYearAndDates, supportedCases,
  cashProrationPolicy, withholdingTableOrDecisionRules,
  contributionTiersAndEligibility, benefitBaseMappings,
  roundingByComponentAndReportingLevel, checksum
}
CalculationBasis {
  employmentAndWorkRevisions, expectedPaymentDate,
  priorPaidAmountsByEmployeeMonthYear,
  otherCommittedUnpaidRunReservations,
  ruleRelease, sourceCoverage, monthCapacityVersion
}
```

Skatteverket publishes machine-readable withholding tables and dated contribution changes. They must be imported/versioned, not represented as one universal percentage [X08/X09]. A person reference alone is not enough to infer age/status eligibility.

## Explicit calculator

```text
calculateRegularPayroll(basis):
    require all supplied inputs supported, obligations known and revisions compatible
    require no unsupported absence or irregular-period proration
    G = monthly salary after explicitly qualified gross adjustments
    cashReimbursements = sum(supported non-taxable cash reimbursement components)
    taxableBenefits = sum(component withholding bases after qualified employee payments)
    contributionBenefits = sum(component employer-contribution bases)
    N = sum(post-tax net deductions with explicit destination/benefit relationship)
    withholdingBase = G + taxableBenefits

    if withholding decision is fixed explicit amount:
        H = qualified decision amount for this pay event
    else if table:
        wageUnit = convertBaseToTableUnit(withholdingBase, release.tableBaseRounding)
        rows = table entries matching year, frequency, tableId, column and wage interval
        require exactly one row
        H = row.amount or exact evaluation of its published formula
    else if approved percentage decision:
        H = roundRational(withholdingBase*n, d, decision.rounding)
    else: fail MissingWithholdingRule

    totalContributionBase = G+contributionBenefits
    eligibleTiers = select exact dated age/status contribution profile
    function F(base):
        exact = sum(max(0,min(base,tier.upper)-tier.lower) * tier.rate as rational)
        return roundRational(exact.n, exact.d, release.contributionRounding)
    C = F(priorCompatibleMonthlyBase+totalContributionBase) - F(priorCompatibleMonthlyBase)
        # Include owned committed run reservations in the calculation basis to avoid
        # allocating the same monthly band to two concurrent approved runs.

    payable = G + cashReimbursements - H - N
    require H>=0 AND payable>=0 for this bounded profile
    # Do not silently reduce withholding to available cash without a qualified rule.
    extraAccruals = calculate explicit supported holiday/pension components
    return frozen {G,H,N,C,payable,reimbursements,benefitBases,extraAccruals,
                   formulaRows,roundingResiduals,allInputRefs}
```

Do not confuse benefit valuation with new benefit expense. An already accounted car/insurance cost can produce a taxable benefit base without another journal expense. Each benefit declares whether its cost is already recognized, must be recognized by a supported paired effect or is unsupported. Net deductions that reduce a benefit need that explicit relationship; unrelated deductions do not reduce the benefit base.

A contribution tier threshold is scoped to its actual statutory aggregation period and status. `F(prior+new)-F(prior)` avoids granting a monthly reduced band to every pay run. Annual thresholds and exceptional rules require separate exact policy inputs or an explicit unsupported result.

```text
preparePayRun(command):
    basis = application C4 capture through PayrollDb using current payroll-only access
    calculated = PayrollDomain.calculateRegularPayroll(basis)
    return withAdmittedPrincipal(access, scope, payrollPreparePermission, (tx, principal) =>
        lock book; replay exact command first
        require one original regular earning event per employee/pay cycle
        # A new work revision requires correction, not another salary event.
        recheck employee/work/rule and month-capacity dependency versions
        run = PayrollDb.insertFrozenCalculation(tx, calculated, basis)
        return CommandDb.save(tx, principal, command, run)
    )
    # No financial posting, salary payment or declaration yet.
    # Monthly contribution capacity is consumed/reserved only by the owning execution.
```

Later employee changes do not rewrite a saved calculation. New relevant dated work inputs make new execution require a new calculation. Separate employees' evidence capture can continue while one calculation is blocked.

The planned payment date selects an estimated reporting basis. NEXT-21 requires actual payment/benefit evidence and reconciles any period change; creating this run is not proof the employee received income.

## Vectors

```text
synthetic supplied H900000, G3000000, N10000, reimbursements0 => payable2090000
add noncash benefit50000 => relevant tax bases change, cash earnings do not become3050000
synthetic tiers first100 at1/10 then excess1/5:
    F(80)=8; next50 => F(130)-F(80)=16-8=8, not5
missing holiday/pension applicability => blocked, not assumed absent
```

These are design examples. Current statutory rates/tables are not provided by the synthetic inputs.


---

<a id="part-23"></a>

# NEXT-21: Payroll posting, payslip and AGI artifact

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/payroll/runs-and-declarations.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/payroll/runs-and-declarations.ts` or the existing equivalent owner |
| Pure calculation | Pay-run journal, paid/reporting bridge, AGI mapping and payslip semantics |
| Atomic scope | Run/correction/payment groups commit atomically; documents render in Bun jobs. |
| Prerequisites | NEXT-20 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-20. Use private payroll access and immutable run semantics. AGI reporting timing follows paid/provided compensation, not creation of a proposed run [X10/X11].

## Atomic accrual/posting

```text
compilePayRunJournal(run):
    for employee:
        Journal.addSigned(cashSalaryExpense, +G)
        Journal.addSigned(reimbursementExpenseOrClearing, +cashReimbursements)
        Journal.addSigned(employeeNetPayLiability, -payable)
        Journal.addSigned(withholdingLiabilityOrProvision, -H)
        for deduction:
            Journal.addSigned(deduction.reviewedDestinationRole, -deduction.amount)
        Journal.addSigned(employerContributionExpense, +C)
        Journal.addSigned(employerContributionLiabilityOrProvision, -C)
        add supported holiday/pension accrual pairs with their own explicit liabilities
        add NO benefit expense when its cost is already recognized
    return balanced journal + per-employee obligation components

executePayRun(command):
    return withAdmittedPrincipal(access, scope, payrollExecutePermission, (tx, principal) =>
        lock book; replay exact command first
        load exact plan and payroll-authorized employee/work/month-capacity basis
        require supported rule witnesses, current grants and unconsumed earning identities
        PayrollDomain.assertApprovedEmployeeAndControlTotals(plan, current)
        approval = validate exact pay-run approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal)
        effects = PayrollDb.insertRunPostingEmployeeObligationsAndReservations(tx, plan, journal)
        OutboxDb.insert(tx, payslip render intents bound to immutable run semantics)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journal.ids, effects}, approval)
    )
    # No cash movement or paid-reporting fact from posting alone.
```

Where the selected accounting profile uses provisional withholding/contribution accounts before payment, retain those roles and the later reclassification explicitly. Do not advertise provisional liabilities as authority-assessed tax.

## Cash and reporting events

```text
recordPayrollPayment(runEmployee, paymentEvidence):
    require actual supported payment identity, payee and amount match employee liability
    initial profile requires full employee net payment; partial pay needs its own qualified allocation
    create or adopt exactly one bank payment through owned salary settlement
    debit employee net-pay liability; credit bank if not already posted
    append PaidCompensationEvent with actual paidOn and original run components
    if actual reporting period/date invalidates calculated tax/contribution profile:
        mark ReportingAdjustmentRequired, preserve originals
        require owned payroll adjustment before final reporting

recordBenefitProvided(runEmployee, benefitEvidence):
    append explicit provided-date/reporting-period event under qualified benefit policy
    no fabricated cash movement
```

An exported salary instruction or an operator's unverified “settled” status is not a PaidCompensationEvent. Missing cash evidence keeps final AGI membership incomplete. Unpaid pay-run accruals remain reconcilable through an explicit accrual-to-paid bridge, not silently included in a paid declaration.

## AGI semantic aggregate

```text
prepareAgi(period):
    capture actual PaidCompensationEvents and qualified BenefitProvidedEvents
    capture existing AGI individual identity inventory and prior submitted revisions
    capture all required employees and zero-reporting applicability
    group by employer identity, actual reporting period, payee identity, specificationNumber
    specificationNumber = retained nonzero stable ID for that reporting item
    for item:
        aggregate exact gross cash, relevant benefits, actual withholding and contribution bases
        apply AGI release's field-level rounding and aggregate-control rules
        validate required identities/periods and every supported conditional field
    compute employer control values from same semantic population
    reconcile paid semantic totals to employee/run registers and GL:
        posted accruals - unpaid/other-period components +/- explicit adjustments
        == declared period components, with all bridges evidenced
    refuse unsupported schema fields/cases or unexplained differences
    return immutable AgiRevision with item identities, mappings, formula lineage and basis
```

Do not recalculate table withholding from the employee's current salary during export. Use the actual recorded withholding and frozen run evidence, with any qualified correction explicitly attached.

## Owned payroll correction

```text
prepareUnpaidRunCorrection(original, correctedCalculation):
    require original has no payment, filed individual record or later dependent consumption
    capture exact original journal, employee obligations and reserved monthly contribution basis
    compile exact reversal + replacement obligations/calculation effects as one owned group
executeUnpaidRunCorrection(command):
    return withAdmittedPrincipal(access, scope, payrollCorrectionPermission, (tx, principal) =>
        lock book; replay exact command first
        load exact approved correction and all original run/payment/reporting dependents
        require no payment, filed individual record or later consumed allocation
        validate original reversal and replacement as ONE owned group
        approval = validate exact correction approval using C5
        journalGroup = JournalApp.postWithinTransaction(tx, complete reversal + replacement)
        effects = PayrollApp.applyCorrectionWithinTransaction(tx, plan, journalGroup)
        PayrollDb.retireSupersededExecutionAuthority(tx, plan)
        OutboxDb.insert(tx, corrected payslip render intent)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journalGroup.ids, effects}, approval)
    )
    # No fabricated cash payment or declaration amendment.

reconcilePaidMonthContributions(period):
    target = contribution policy evaluated over actual paid/provided eligible month population
    attributed = exact effective contribution amount already attributed to that population
    delta = target-attributed
    if delta !=0:
        prepare an owned expense/liability adjustment, with complete paid/accrued bridge
        require approval and atomic receipt before final control reconciliation
    unpaid provisions stay explicit, not included in paid declaration totals
```

Negative recovery of already paid salary, reduced reported withholding and consumed retroactive calculations require their separately qualified recovery profiles. Refuse them in this initial profile rather than apply the unpaid reversal algorithm to paid money. Nonfinancial declaration corrections do not create salary journals.

## XML and amendments

```text
renderAgi(revision, exactSchemaBundle):
    require supported namespace/schema/mapping release actually acquired and hashed
    emit XML from typed semantic fields in required order with strict escaping
    validate exact XSD + employer/person/period/control constraints
    store bytes/hash/schema version/validation result in artifact manifest

prepareAgiAmendment(originalItem, newSemanticResult):
    retain employer, period, payee and SAME specificationNumber
    # A new specification number can add another item instead of replacing the old one [X11].
    require amendment policy permits each changed field
    if withholding decreased and no specifically qualified correction exception:
        refuse and create specialist review case [X12]
    emit replacement/removal operation required by that exact schema, not a second ordinary item
    preserve previous files and submission observations
```

No AGI/KU interchangeability and no “filed” flag from XSD success. Export, signature, submission and assessed outcome are distinct. Empty employer-registered months may need a zero declaration according to their qualified obligation inventory, not simply absence of employees.

## Payslip and vectors

Payslips render the original employee identity/run version, cash components, deductions, net and relevant benefits under payroll authorization. A later employee edit does not change saved bytes. Mark a prepayment slip as calculated/posted, not paid.

```text
G3000000 H900000 N10000 => salary expense3000000;
    net liability2090000 + tax provision900000 + deduction destination10000
January work paid February => February paid-reporting population under the selected rule
same-key pay-run execute => same receipt, one payroll posting
AGI amendment same employer/period/payee/specification => replacement identity retained
unpaid run + no paid evidence => no fabricated paid individual record
```

## Application payment and artifact boundaries

Salary payment accounting and `PaidCompensationEvent` admission are one named application transaction, not a public payment call followed by a separately committed reporting event. Capture actual evidence and compile the payment outside the commit when necessary; execute with C5 current grants, source capacity and approval. A domain state requiring reporting adjustment can be retained honestly, but it must not swallow a failed financial write.

AGI and payslip preparation use C4's captured basis and immutable model sealing. The effect-mq Bun handler renders XML/PDF and runs validation outside financial transactions, then attaches exact artifact/validation references in a short reauthorized tx. A native XSD process is a concrete job dependency, not a database procedure or a Worker request that assumes native execution. Provider submission remains a separately authorized operation.


---

<a id="part-24"></a>

# NEXT-22: Pre-close tax bridge and INK2/SRU

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/tax/corporate.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/tax/corporate.ts` or the existing equivalent owner |
| Pure calculation | Pretax bridge, current-tax delta and INK2/SRU fields |
| Atomic scope | Tax-effect journal and owned year target share one tx; form artifacts are separate. |
| Prerequisites | NEXT-13 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-13. Draft tax computation precedes final close. It does not wait for an already finalized year that itself needs current tax.

## Typed bridge

```text
PreTaxOverlay immutable {
  fiscalYear, ledgerBasis, proposedNonTaxAdjustments,
  effectiveIncomeTaxEffectsExcludedFromPretaxResult,
  mechanicalTransferEffectsExcludedFromPL,
  pretaxProfit, supportedRuleWitnesses, sourceCoverage
}
TaxAdjustment immutable {
  id, year, kind: nondeductible_expense|nontaxable_income|supported_schedule_adjustment,
  signedTaxableAdjustment, sourceContributionIds, evidence, ruleRelease,
  explanation, economicComponentIdentity
}
TaxBridge immutable {
  overlayDigest, adjustments[], lossBasis,
  taxableBeforeLoss, allowedLossOffset, taxableIncome,
  currentTaxTarget, projectedAfterTaxResult,
  fieldLineage, mappingRelease, status
}
```

A duplicate tax adjustment over the same economic component is refused unless the mapping explicitly establishes distinct nonoverlapping adjustments. The tax return mapping is versioned data/code from the applicable official release, not an inferred account-prefix table.

## Calculation

```text
calculateCorporateTax(overlay, adjustments, reviewedLosses, taxRelease):
    P = overlay.pretaxProfit
    require overlay pretax definition excludes current income-tax expense exactly once
    require every material tax adjustment family is supported or evidenced inapplicable
    require reviewedLosses known, including an evidenced zero when applicable
    A = sum(adjustments.signedTaxableAdjustment)
    beforeLoss = P+A
    if loss restrictions/ownership changes exceed supported profile:
        fail UnsupportedLossTreatment
    allowedOffset = min(max(beforeLoss,0), reviewedEligibleLossAvailable)
    taxableRaw = max(beforeLoss-allowedOffset,0)
    taxable = apply exact taxRelease.taxableBaseRounding(taxableRaw)
    currentTax = roundRational(taxable*taxRelease.rate.n,
                              taxRelease.rate.d, taxRelease.taxRounding)
    require otherSupportedIncomeTaxExpense is evidenced and supported (or evidenced0)
    projectedAfterTax = P-currentTax-otherSupportedIncomeTaxExpense
    closingLossBasis = reviewedOpeningLoss-allowedOffset+max(-beforeLoss,0)
        # Only for the qualified no-special-restrictions profile.
    return all rows and formula dependencies, not just currentTax
```

Draft calculations do not consume loss carry-forwards. The final selected year/certificate owns the adopted loss movement. Competing drafts cannot consume the same opening allowance repeatedly. A negative taxable result does not produce a negative current-tax cash receivable by multiplying it by a rate.

## Current-tax journal and self-reference avoidance

```text
prepareCurrentTaxEffect(bridge, priorYearTaxEffects):
    target = bridge.currentTaxTarget
    alreadyRecognized = sum(effective current-tax effects for this company/year)
    delta = target-alreadyRecognized
    Journal.addSigned(currentIncomeTaxExpense, +delta)
    Journal.addSigned(currentTaxLiability, -delta)
    return sealed year-tax target and exact delta or a no-effect receipt
```

Preliminary tax transferred to skattekonto is not current income-tax expense. Reconcile tax prepayments, assessed charges and the liability separately. Do not subtract bank tax payments from the tax expense target to make the return agree.

The tax journal changes the actual ledger. It must not change the definition of pretax profit used to calculate itself. Revalidation compares the retained pretax contribution set and supported tax adjustments, not simply a global ledger sequence.

## INK2 semantic fields

```text
prepareIncomeTaxFields(bridge, actualOrProjectedStatements, formRelease):
    INK2R receives the qualified financial-statement values, including after-tax result
    INK2S starts from that declared accounting result
    add back the nondeductible tax expense under its explicit tax mapping
    include the other bridge adjustments once
    require resulting taxable basis reconciles to bridge.taxableIncome
    INK2 main fields and any supported additional bases derive from the same bridge
    for every required mapping:
        value = typed source selector + allowed sign/unit/rounding transformation
        retain source formula IDs and reviewed mapping checksum
    missing required fields or unsupported supplementary obligations -> draft blocked
```

This reconciles a pretax calculation with an accounting form whose result may be after tax. It avoids silently using different starting results in the engine and exported declaration.

## SRU serialization

```text
renderSru(fields, exactFormatBundle, submitterFacts):
    require selected forms/year/fiscal interval supported by bundle
    require complete field-code map and real submitter/declarant identity
    INFO.SRU = serialize bundle's INFO header/contact/terminator grammar
    BLANKETTER.SRU = for each selected form in deterministic order:
        emit '#BLANKETT' and its exact release-specific form identifier
        emit identity/date metadata required by bundle
        emit '#UPPGIFT', exact fieldCode, formatCheckedValue for each required/present field
        emit per-form terminator
    emit bundle's file terminator
    reject unsupported encoding, embedded line breaks/control characters and size overflow
    validate lexical grammar, field types, identities and cross-field totals independently
    retain both filenames, byte hashes, lengths, form release and validation results
```

The concrete current field codes, headers and encodings are required reviewed data, not guessed literals. INFO.SRU and BLANKETTER.SRU are distinct deliverables under Skatteverket's file-transfer contract [X13/X14]. Export is not signing or filing. NE and comprehensive special corporate-tax regimes are outside this selected AB profile.

## Vector, synthetic20% tax

```text
P=1000000, addback50000, deduction20000, known losses0
beforeLoss=1030000; currentTax=206000; afterTax=794000
form bridge: 794000 + taxAddback206000 +50000 -20000 =1030000
prepaid tax90000 does not change currentTax206000
existing currentTax effect200000 => new tax adjustment6000, not206000 again
```

## Application tax-effect execution

```text
executeCurrentTaxEffect(command):
    return withAdmittedPrincipal(access, scope, taxPostingPermission, (tx, principal) =>
        lock book; replay exact command first
        load sealed year-tax plan and current pretax/adjustment/loss witnesses
        require year target identity and effective prior tax effects match approved basis
        require no unsupported change to eligible loss facts or pretax population
        CorporateTaxDomain.assertTargetAndDelta(plan, current)
        approval = validate exact tax-effect approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal) if nonempty else []
        effect = CorporateTaxDb.insertYearTargetEffect(tx, plan, journal)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: ids(journal), effect}, approval)
    )

prepareCorporateDeclaration(command):
    capture fixed statement, tax-bridge and exact form-release inputs through application reads
    fields = CorporateTaxDomain.prepareIncomeTaxFields(captured)
    persist immutable semantic fields and lineage through a short application tx
    append render intent; effect-mq Bun job renders and validates SRU outside the tx
    attach exact file manifests and results, never an inferred submission receipt
```

The tax calculator, form mapping and rounding policy live in `jurisdictions/se` or the owning application/domain module. Typed SQL returns exact contribution and previously applied effect sets. Draft bridges do not consume loss rights; final selected closing facts own that adoption. No tax-rate or INK2 state machine is implemented in an integrity trigger.


---

<a id="part-25"></a>

# NEXT-23: Financial close and single-count carry-forward

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/closing/financial-years.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/closing/financial-years.ts` or the existing equivalent owner |
| Pure calculation | Current close controls, result-transfer delta and single-count opening |
| Atomic scope | Transfer, financial certificate, next opening, locks and receipt share one tx. |
| Prerequisites | NEXT-13, NEXT-22 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-13/22 plus the actually applicable accounting families. Root composes shared control/closing changes after reserved owners release their contracts. Do not require unrelated payroll or webshop features for every company.

## State and stages

```text
FinancialYearStatus = open | preparing | adjustments_pending | ready_for_finalization | closed
Technical period locks remain separate.
ClosePreparation immutable {baseline, applicableFamilies, proposedAdjustmentRefs, openCases}
FinalCloseProposal immutable {
  year, actualAfterAdjustmentBasis, taxBridgeAndReceipt,
  exactCurrentControlManifests, resultTransferPlan,
  nextOpeningSemanticTarget, digest
}
FinancialCloseCertificate immutable {proposalDigest, receipt, closingBasis, openingSetId}
OpeningSet immutable {
  year, version, previousCertificateOrMigrationBasis,
  rawBSBalances, sourceBoundary, priorOpeningVersion?, digest
}
ReopenEvent immutable {certificateId, reason, authorizedImpactManifest}
```

## Acyclic preparation

```text
prepareYearClose(year):
    capture applicable family inventory with independent evidence
    for family:
        Required -> request owned complete control result
        NotApplicable -> verify dated evidence and absence of contradictory retained events
        Unknown/Unsupported -> record blocker
    collect non-tax adjustment plans through each existing domain owner
    return preparation, not a final certificate

advanceClosePreparation(preparation):
    review/approve/execute domain adjustments through their owners
    recapture actual books after non-tax changes
    calculate NEXT-22 pretax bridge and approve/execute required current-tax delta
    recapture actual after-tax books
    require actual adjustment receipts exactly match selected economic effects
    prepare FINAL proposal at this new basis
```

No approval silently survives a changed economic proposal. No model/provider call runs inside the final transaction. If a technically locked period needs a closing adjustment, use an explicit authorized reopen/adjustment workflow first. Do not bypass application period admission or database integrity through an ambient flag.

## Mechanical result transfer

The qualified first closing profile uses a distinct nominal result-transfer role and a year-result equity role. Original ordinary revenue/expense entries are not erased.

```text
P = current after-tax year profit from NEXT-13, excluding OWNED transfers
F = net credit to year-result equity from prior effective transfers for this same year
D = P-F
resultTransferJournal:
    addSigned(nominalResultTransferRole, +D)
    addSigned(yearResultEquityRole, -D)
# A loss makes D negative and reverses the debit/credit direction naturally.
```

For a reopened/reclosed year, post only the additional transfer delta. Do not transfer the whole revised profit on top of an earlier valid transfer. Account mapping identifies which nominal role is technical for statement presentation. Arbitrary manual entries to that account are not automatically ignored.

## Atomic finalization

```text
executeFinalClose(command):
    return withAdmittedPrincipal(access, scope, financialClosePermission, (tx, principal) =>
        lock book; replay exact command first
        load exact final-close plan
        lock all relevant periods/accounts and domain resources in the shared ordering
        load complete required-family/control/source/tax dependency manifests
        require all approved measurements and required current controls satisfied
        require designated year-end posting period eligible for this exact action
        ClosingDomain.assertCurrentTargetAndOpeningConservation(plan, current)
        approval = validate exact financial-close approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.resultTransferJournal) if nonempty else []
        resultingBalances = ClosingDb.readBalancesWithinSameTransaction(tx, plan.year)
        require resulting raw BS equals sealed next-opening target
        require raw final nominal aggregate closes under selected bridge convention
        certificate = ClosingDb.insertFinancialCertificate(tx, plan, journal)
        opening = ClosingDb.insertDerivedOpeningSet(tx, certificate, plan.nextOpening)
        ClosingDb.applyYearAndPeriodLockStates(tx, plan)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: ids(journal), certificate, opening}, approval)
    )
    # One acknowledged commit. Artifact rendering/signing/filing occur later.
```

The whole finalization has one receipt. A failure after posting but before opening creation rolls everything back. A zero delta creates no fake voucher, but the certificate/opening/lock result remains atomic.

## Opening semantics

```text
nextYearReport:
    opening = selected authorized OpeningSet
    movement = actual next-year journals, EXCLUDING any journal already representing that opening
    closing = opening + movement
```

In a continuous native ledger, generating the OpeningSet creates no new cash, asset or liability journal. Old year's actual postings already establish those balances. A migration into an empty book may require one explicit opening voucher; use that as the basis once and exclude it from ordinary movements.

Nominal accounts begin a new year's report at0 under the qualified year partition, not with prior-year operating balances. BS balances include the transferred prior profit. Unadopted/missing source opening values are not set to0.

## Reopen and downstream opening impact

```text
prepareReopen(certificate):
    enumerate later openings, reports, tax/artifacts/signatures and subsequent closed years
    if unsupported consumed downstream year requires cascade: refuse with exact dependency list
    seal reason and permitted period changes
executeReopen(command):
    withAdmittedPrincipal(access, scope, reopenPermission, (tx, principal) =>
        lock book; replay exact command first
        load exact reopen plan and complete downstream membership
        require supported cascade scope and current authorized approval
        append ReopenEvent and update permitted lock state through tx
        retain old certificate, opening and files unchanged
        persist downstream invalidation/outbox intent and exact receipt through tx
    )

after corrections and revised close:
    append new OpeningSet revision with delta against old opening for explanation
    continuous ledger => projection replacement, not another opening journal
    require new next-year reports select new basis; old reports stay byte-identical
    do not rewrite already filed returns; create amendment obligations
```

## Vectors

```text
profit60000 -> nominalTransfer+60000/equity-60000; P&L stays60000
next opening cash60000/equity60000 -> no extra60000 cash journal
reopen adds expense10000 -> revisedProfit50000, previousTransfer60000 => delta-10000
reclose transfers back10000, new opening reflects50000; old snapshot remains60000
missing required VAT control -> no certificate, no transfer, no new opening
```

Certificate scope names what was checked. Financial close does not fabricate signature, filing or external acknowledgment.


---

<a id="part-26"></a>

# NEXT-24: K2 annual-report semantic model and iXBRL

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/reports/annual.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/reports/annual.ts` or the existing equivalent owner |
| Pure calculation | K2 requirements, semantic model, presentation and iXBRL |
| Atomic scope | Final semantic approval/receipt and render intent are atomic; native validation runs later. |
| Prerequisites | NEXT-13, NEXT-23 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-13/23. Select the company's applicable framework version, not whichever template was newest when development began [X04]. Native XBRL validation is a narrow artifact-worker capability.

## Records

```text
AnnualReportRevision immutable {
  entityRevision, fiscalYear, financialCloseCertificate,
  statementSnapshotIds, comparativeBases,
  frameworkRelease, disclosureRelease, taxonomyMappingRelease,
  facts: [{semanticId, typedValue|Unknown|NotApplicable,
           evidenceRefs, calculationRefs, reviewedBy?}],
  narrativeSections, signerRoles, completionStatus, digest
}
PresentationRevision immutable {
  annualReportDigest, displayUnitAndPrecision,
  displayedFacts, roundingExplanations, rendererRelease, digest
}
ArtifactManifest immutable {
  modelDigest, presentationDigest, contentHash, mediaType, size,
  taxonomyVersion, entryPointHash, transformRegistryVersion,
  validationRuns, financialSignatureScopeDigest
}
```

Financial facts, narratives, governance assertions and actual signature events are distinct. An agent may draft prose but cannot turn an unsupported statement into a verified fact.

## Required disclosure evaluation

```text
prepareAnnualReport(year):
    witness = resolveProfile(..., K2AnnualReport, fiscalDates, entityFacts)
    require eligibility supports chosen K2 release, else explicit unsupportedK3/applicability blocker
    statements = exact approved financial snapshots
    for requirement in disclosureRelease:
        applicability = evaluate known entity/year facts
        if applicability unknown: retain required question
        if applicable:
            value = derive from retained financial/source evidence where supported
            otherwise require reviewed explicit non-ledger fact
        if inapplicable: retain reason and fact evidence, not an empty default
    compare periods using explicitly mapped comparable facts and known missing-history limits
    seal draft with complete requirement checklist

finalizeSemanticReport(draft):
    require no missing mandatory disclosure, unsupported comparison or financial mismatch
    require narratives contain only approved statements, with unknown drafts excluded
    freeze exact model approved for rendering
```

Meeting dates, signatures, dividend decisions and directors are never inferred from ledger balances. A prior year absent because the company is newly formed is established by company evidence, not by an empty export.

## Presentation and semantic numeric consistency

```text
preparePresentation(model, presentationRules):
    for numeric fact:
        displayed = exact rounding/unit transformation permitted by presentationRules
        retain source exact value, displayed value and rounding provenance
    validate arithmetic of displayed totals and permitted presentation differences
    if discrepancy needs an allowed rounding row: retain explicit presentation-only row
    otherwise use another permitted precision or refuse final rendering
    # No balancing journal is created for display rounding.
```

Rendered numeric facts must agree with their displayed values and declared units/precision. Do not display one rounded number but encode a different undisclosed XBRL value.

## iXBRL rendering

```text
renderIxbrl(model, presentation, taxonomyBundle):
    require all required concepts resolve to pinned entry point/DTS and qualified mapping
    build contexts keyed by (entity identifier, instant OR duration, dimensions)
    build units keyed by the actual ISO currency / other supported unit
    for semantic fact:
        mapping = exact concept, context rule, datatype, sign/unit/precision mapping
        require mapping applicable to this model/framework and disclosure role
        numeric -> emit ix:nonFraction with strict contextRef, unitRef,
                   sign, decimals/scale and supported transformation
        nonnumeric -> emit ix:nonNumeric with escaped approved content
        null/unknown -> do not manufacture0 or a fact; mandatory unknown blocks finalization
    emit readable statements/notes from SAME presentation data and stable templates
    reject duplicate concept/context/unit facts with inconsistent values
    add all referenced contexts/units; reject dangling references
    return deterministic XHTML bytes
```

The exact concept QNames, taxonomy packages and XBRL transformations are required qualified data, not names invented by this document. Comparatives use their proper periods/contexts and retained disclosures, not current-year labels pasted onto last year's amounts.

## Independent validation and immutable retention

```text
validateArtifact(bytes, bundle, validatorRelease):
    execute pinned native validator with local hashed taxonomy dependencies
    record actual document load, chosen entry points, complete DTS resolution,
           required validation stages executed, errors/warnings and run environment
    require documentLoaded
    require every required stage actually ran
    require no fatal/error and no unreviewed blocking warnings
    independently extract facts and compare to finalized semantic/presentation model
    require count/identity/value/context matches, including missing/duplicate fact checks
    store immutable validation report
    # A process exit0 with skipped document validation is NOT a pass.
```

Upload bytes and attach the verified manifest using C6. Validation unavailable preserves draft artifacts but blocks the required final state. No claim of Bolagsverket acceptance follows from a local validator pass.

## Signature/adoption boundaries

```text
FinancialSignatureEvent -> exact financial-report content and signer authority
AdoptionEvent -> actual meeting decision/evidence
AdoptionCertificate -> actual adoption facts and authorized attester
SubmissionAttempt -> exact submitted artifact variant plus external outcome
```

If an adoption certificate is added after the financial report was signed, verify the signed financial content remains identical and preserve its original signature scope. Never treat a signature over one digest as covering arbitrary later content. Different required signing/filing events remain separate even when shown in one UI wizard.

Vectors: changed note -> new semantic/presentation/artifact digest; unknown mandatory fact -> draft only; bad context date -> validation failure; exit0 but document not loaded -> failure; prior model/model after governance change -> old signed bytes retained; K2 output does not imply K3 support.

## Application model and native validation runtime

```text
finalizeAnnualReport(command):
    withAdmittedPrincipal(access, scope, annualReportPermission, (tx, principal) =>
        lock book; replay exact command first
        load exact report draft and captured close/statements/disclosure revisions
        AnnualReportDomain.assertCompleteApprovedSemantics(draft, current)
        approval = validate exact report-finalization authority using C5
        final = AnnualReportDb.insertFinalSemanticRevision(tx, draft)
        OutboxDb.insert(tx, render request with model/renderer/taxonomy identities)
        return finishOwnedWithinTransaction(tx, principal, command, draft,
            {journalIds: [], final}, approval)
    )

annualReportArtifactJob(job):
    establish scoped service permission and current artifact-work revision
    load exact finalized semantic/presentation model and hashed taxonomy bundle
    bytes = AnnualReportDomain.renderIxbrl(model, presentation, taxonomy)
    validation = run qualified native validator and independent extraction on Bun worker
    # No open financial tx, no native executable assumption inside API Worker.
    retain bytes and validation artifact with their exact hashes
    short application tx: reauthorize, replay, verify model/job versions and attach manifests
```

The job cannot mutate financial statements, finalize missing disclosures or mint signatures to make validation pass. A failed validation is retained as a failed result; it is not a thrown-and-ignored error that becomes an accepted artifact. No extra general-purpose execution service is required.


---

<a id="part-27"></a>

# NEXT-25: Fixed-revision company rehearsal and restore

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

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


---

<a id="part-28"></a>

# Integration map: application-owned edition v2

This is a complete replacement ownership map for the same 25 tasks. No task has been renumbered or replaced with a new task. Dependency priorities and all five WIP reservations remain. Earlier SQL function and migration identifiers are historical evidence, not implementation targets.

## Root integration ownership

Root owns shared `packages/contracts` API/capability registration, `packages/domain` unions used across domains, application identity/transaction primitives, the internal journal writer, baseline schema/integrity/grants and common UI/runtime composition. Domain workers own named Effect application services, pure calculations and tx-passing persistence with their local UI.

Do not recreate `db/query.ts` operation-string dispatch. All REST/MCP/worker/script callers reach the same application operation. Public operation IDs can stay stable while internals change. Calls to internal writers pass the same `tx`; calls to another public operation occur with no enclosing financial transaction unless an explicitly supported internal aggregate port is used.

A private `applyWithinTransaction` contract is a real composition boundary, not a second transaction, a public arbitrary posting endpoint or a security boundary against compromised trusted backend code.

## Dependency table

Independent leaf preparation may proceed before final wiring. Conditional dependencies become mandatory only when the selected company/operation uses the relevant case. Do not treat an absent qualified profile as an empty or inapplicable business population.

| Packet | Required | Integrate after | Conditional | Reserved handoff |
|---|---|---|---|---|
| [NEXT-01](packets/NEXT-01.md) | None | None | None | None |
| [NEXT-02](packets/NEXT-02.md) | None | None | None | None |
| [NEXT-03](packets/NEXT-03.md) | NEXT-02 | None | None | None |
| [NEXT-04](packets/NEXT-04.md) | NEXT-02, NEXT-03 | None | None | WIP-VAT03, WIP-VAT04-A1 |
| [NEXT-05](packets/NEXT-05.md) | NEXT-03, NEXT-04 | None | NEXT-17: actual unpaid foreign-denominated supplier obligations occur | None |
| [NEXT-06](packets/NEXT-06.md) | NEXT-02, NEXT-03 | None | None | None |
| [NEXT-07](packets/NEXT-07.md) | NEXT-03 | None | NEXT-08: an exported payment reservation must first be resolved | None |
| [NEXT-08](packets/NEXT-08.md) | None | None | None | None |
| [NEXT-09](packets/NEXT-09.md) | None | None | None | None |
| [NEXT-10](packets/NEXT-10.md) | NEXT-09 | None | None | None |
| [NEXT-11](packets/NEXT-11.md) | NEXT-02, NEXT-13 | None | NEXT-14: dimension assignments occur in the selected book | None |
| [NEXT-12](packets/NEXT-12.md) | NEXT-02 | None | None | None |
| [NEXT-13](packets/NEXT-13.md) | NEXT-02 | None | None | None |
| [NEXT-14](packets/NEXT-14.md) | None | NEXT-13 | None | None |
| [NEXT-15](packets/NEXT-15.md) | NEXT-02 | NEXT-04 | None | None |
| [NEXT-16](packets/NEXT-16.md) | NEXT-01, NEXT-03, NEXT-06 | None | None | None |
| [NEXT-17](packets/NEXT-17.md) | NEXT-02 | NEXT-03 | None | WIP-FX02-P1 |
| [NEXT-18](packets/NEXT-18.md) | NEXT-17 | None | None | WIP-FX02-P1 |
| [NEXT-19](packets/NEXT-19.md) | None | None | NEXT-04: the disposal has a VAT-reporting consequence; NEXT-15: the chosen flow requires a supported legal invoice/credit interaction | WIP-AST03-UI |
| [NEXT-20](packets/NEXT-20.md) | NEXT-02 | None | None | None |
| [NEXT-21](packets/NEXT-21.md) | NEXT-20 | None | None | None |
| [NEXT-22](packets/NEXT-22.md) | NEXT-13 | None | None | None |
| [NEXT-23](packets/NEXT-23.md) | NEXT-13, NEXT-22 | None | NEXT-04: the reviewed company/year inventory makes this treatment applicable; NEXT-05: the reviewed company/year inventory makes this treatment applicable; NEXT-06: the reviewed company/year inventory makes this treatment applicable; NEXT-07: the reviewed company/year inventory makes this treatment applicable; NEXT-12: the reviewed company/year inventory makes this treatment applicable; NEXT-18: the reviewed company/year inventory makes this treatment applicable; NEXT-19: the reviewed company/year inventory makes this treatment applicable; NEXT-21: the reviewed company/year inventory makes this treatment applicable | None |
| [NEXT-24](packets/NEXT-24.md) | NEXT-13, NEXT-23 | None | None | None |
| [NEXT-25](packets/NEXT-25.md) | None | None | NEXT-02: required by the selected real-company rehearsal scope; NEXT-03: required by the selected real-company rehearsal scope; NEXT-04: required by the selected real-company rehearsal scope; NEXT-05: required by the selected real-company rehearsal scope; NEXT-06: required by the selected real-company rehearsal scope; NEXT-11: required by the selected real-company rehearsal scope; NEXT-12: required by the selected real-company rehearsal scope; NEXT-13: required by the selected real-company rehearsal scope; NEXT-16: required by the selected real-company rehearsal scope; NEXT-21: required by the selected real-company rehearsal scope; NEXT-23: required by the selected real-company rehearsal scope; NEXT-24: required by the selected real-company rehearsal scope | None |

## Reserved work

**WIP-VAT03.** VAT-03 qualification of 9120/9130, including migration, Worker/PostgreSQL and outcome/recovery cases. Do not reimplement or take over qualification. Historical migration numbers identify reserved scope only; consume its released application replacement, never restore the retired SQL workflow.

**WIP-FX02-P1.** FX-02-P1 partial settlement extending 9140, including paired release, residuals, gain/loss and replay. Do not implement partial allocation in this wave. Historical migration numbers identify reserved scope only; consume its released application replacement, never restore the retired SQL workflow.

**WIP-AST03-UI.** AST-03 impairment UI/control/disposal closure over 9150, including schedules.tsx and its control views. Do not take these consumers over. Historical migration numbers identify reserved scope only; consume its released application replacement, never restore the retired SQL workflow.

**WIP-VAT04-A1.** VAT-04-A1 financial amendment delta owner. Do not build another target-minus-prior effect calculator or obligation owner. Historical migration numbers identify reserved scope only; consume its released application replacement, never restore the retired SQL workflow.

**WIP-COM2-W1.** COM-2-W1 provider-neutral webshop intake and order/catalog identity. Do not create competing intake, catalog snapshots or order revisions. Historical migration numbers identify reserved scope only; consume its released application replacement, never restore the retired SQL workflow.

## Handoff contract between runtime owners

Each domain handoff must identify its application operations and current source hashes, wire contracts, pure compiler versions, tx-passing persistence methods, expected locks, complete effect membership, receipt identity, required outbox intents and remaining qualification gates. The receiver checks actual exports rather than copying illustrative names literally.

The receiving worker may not create a second financial balance to avoid a missing port. In particular VAT amendments, paired FX consumption and impairment/disposition remain at their existing owners.

## Runtime and baseline

The API runs on the selected Worker/Bun request composition. effect-mq runs in a separate persistent Bun process with its own session-preserving listener connection. Queue delivery invokes the same application operations. Financial transaction authority never lives in a queue payload or connection session variable.

The pre-release clean baseline has the selected schema, narrow integrity and role files. No old-schema compatibility adapter is required for disposable development data. Any actual meaningful data discovered at a target blocks a destructive reset until its preservation is resolved. Real historical company-bookkeeping import remains in scope for NEXT-12 and NEXT-25.

## Implementation lanes

Keep the original owner lanes from the index, with root coordinating shared files. A worker does not add its own generic transaction wrapper, event language or queue framework. Finish a coherent named operation including reads, execution, corrections and recovery before retiring its previous application dispatch path.

NEXT-01, NEXT-02, NEXT-09 and NEXT-13 remain sensible independent starts subject to actual source ownership. NEXT-13 can develop its pure model while waiting for NEXT-02's profile contract. NEXT-04 waits for released VAT owner ports for financial controls. NEXT-17/18 and NEXT-19 wait for the FX and asset owner handoffs respectively.

## Required proof, not a claimed result

For each port, enumerate former accepted cases/refusals and the new application function enforcing each one. Inspect structural DB constraints separately. Observe real one-connection rollback, concurrent capacity use, approval revocation, same-key recovery and handler/version behavior under actually authorized tests. Nothing in this file authorizes taking over the five active assignments or editing repository tests.


---

<a id="part-29"></a>

# Changes from the SQL-owned dossier

Edition v2 rewrites all 25 packet files, the shared contract and the ownership map. It is not an amendment that must be mentally applied to the old files.

## Shared changes

Named Effect operations now own preparation, approval, execution and recovery. Typed persistence performs explicit reads/DML on the caller's transaction. PostgreSQL retains narrow relational and journal integrity only. Job dispatch uses application outbox intent and the separate effect-mq Bun worker. The clean pre-release baseline replaces the old feature migration/dispatcher architecture under ADR 0010's no-deployed-data condition.

Original financial equations, task IDs, bounded scope and the five WIP exclusions remain. Splitting the reusable line-credit compiler from unpaid-only counterpart selection makes the pre-existing NEXT-03/NEXT-07 reuse contract explicit; it does not change their amounts. External-source IDs in index metadata were aligned with the source dossier's actual registry where an old ID pointed to the wrong subject.

References to meaningful retained source or financial history remain preservation requirements. References requiring a disposable old-schema execution runtime were removed. New wording does not grant data reset, testing or financial authority.

## Per-packet rewrite record

### NEXT-01

Current review ownership is resolved by an application read over one shared snapshot. Ownership refusal moves to application execution.

### NEXT-02

Remove the superseded legacy-schema adapter requirement. Activation is an application-owned non-journal transaction.

### NEXT-03

Purchase journals, payables and tax facts are one application-owned DML group. Separate reusable line credit math from unpaid-only counterpart selection. Retained financial interpretation is preserved without a legacy-schema adapter. Unpaid credits use their own complete application execution; paid credits reuse line math only.

### NEXT-04

Replace permanent legacy runtime retention with explicit semantic versions. Retain meaningful snapshot history without preserving old dispatch. Add complete capture/compile/seal service with same-transaction WIP reads.

### NEXT-05

Cross-border recognition composes qualified purchase, FX/owner and tax writers on one tx.

### NEXT-06

Owner transfers, reimbursements and their counterparty effects share the caller tx.

### NEXT-07

Paid supplier credits keep payable release and refund increase atomic in application code. Refund receipt and its source usage share one app tx without new tax recognition.

### NEXT-08

Payment instruction release is a non-journal application transaction with domain dispatch fencing.

### NEXT-09

Use the selected persistent Bun job runtime rather than a Cloudflare workflow. Window claim is application-owned. Replace SQL publication transition with explicit application tx and outbox intent. Remove obsolete schema compatibility while preserving meaningful external provider history. Clarify transport lease versus domain publication fence.

### NEXT-10

Provider normalization persists in an application transaction. Bank admission composes the current intake app owner on one transaction.

### NEXT-11

Provide application-owned export capture and queued artifact lifecycle.

### NEXT-12

Historical adoption uses one application tx and does not re-recognize opening balances.

### NEXT-13

Remove implication that a legacy runtime is required. Add explicit capture/compile/persist statement service without SQL policy.

### NEXT-14

Move dimension policy to application admission. Preserve unknown source classifications without a disposable-schema interpreter. Replace SQL dimension workflow with app validation and narrow relational constraints. Use source-unknown dimensions rather than legacy-runtime assumptions. Define application journal/assignment composition on the caller transaction.

### NEXT-15

Legal credit issuance is a single app tx followed by outbox-driven rendering.

### NEXT-16

Use effect-mq delivery with separate persisted business versions. Separate public preparation transaction from durable run checkpoint recovery. Batch approval uses one app tx with owner-private approval functions. Apply clean-baseline scope to preparation compatibility. Retain late-handler and acknowledgment-loss domain recovery with effect-mq.

### NEXT-17

Foreign payable recognition is compiled into the purchase aggregate. Consume the released WIP pure calculator, without copying its algorithm. FX settlement consumes released WIP application ports with the same tx as journal and fees.

### NEXT-18

Valuation membership and all carrying deltas commit as one application group.

### NEXT-19

Use transaction-passing asset basis capture. Disposal uses the released asset app port and never independently commits a component.

### NEXT-20

Pay-run capture, pure calculation and sealing live in Effect, not SQL payroll logic.

### NEXT-21

Payroll postings and contribution reservations share one app transaction; outbox replaces inline enqueue. Unpaid payroll correction passes the same tx through reversal, replacement and payroll consequences. Make salary payment/reporting admission atomic and route native artifacts through Bun jobs.

### NEXT-22

Add explicit application execution of tax delta and queued declaration artifact generation.

### NEXT-23

Period policy belongs in the application without introducing context bypasses. Financial finalization performs journal, opening, certificate and lock DML in one app tx. Reopen is a separate application-owned transaction preserving downstream history.

### NEXT-24

Add application finalization plus explicit persistent-Bun native validation and attachment.

### NEXT-25

Acceptance inventories application owners plus narrow integrity rather than old feature functions. Rehearse the accepted clean baseline, not the retired procedural migration chain. Backups include app-owned interpretation. Include application and queue recovery inventories. Fence new persistent job runtime during restore. Require application transaction and effect-mq failure observations instead of SQL workflow proof.

## Coverage and remaining limits

Every individual packet was edited and now identifies an application owner, tx-passing persistence and its atomic scope. The pure financial algorithms and their examples were retained where ownership did not change. These are proposed pseudocode contracts, not runnable Effect code. No claim is made that actual exports match the illustrative method names or that all current application guards already implement this specification.

Source-based audit and arithmetic checks over this dossier are recorded separately in CHECKS.md. They do not execute the ERP, migrations, queues or provider integrations.


---

<a id="part-30"></a>

# Sources and evidence boundaries

This v2 rewrite uses the attached 25-packet pseudocode archive, its rule-data contract and the attached application-ownership amendment. The amendment records the selected ADR 0010/0009 architecture at `422276ae5ed9d0ca146447d92bb3d27c99f8c48a`; the task/source baseline below is the earlier `bb628452196a55ceef7516f76fc3cd6471ae4d91`.

No fresh repository review, external provider request or legal/regulatory verification was performed in this rewrite. References S01 onward and X01 onward are inherited evidence from the source dossier. Treat words such as “current” in their historical titles as describing that pinned baseline, not a newly observed state. Earlier claims that a document was read directly describe the original dossier's work, not this rewrite.

The old SQL ownership/migration instructions are superseded by the supplied amendment. Financial requirements and bounded example calculations remain design inputs, not proof of correctness for a real company. Rule tables, exact formats and company facts still need qualified evidence.

## Application-owned source inputs

- Attached `APPLICATION-OWNERSHIP-AMENDMENT.md`, based on the prior review at the application-owned revision.
- ADR 0010, `docs/adr/0010-application-owned-accounting-replacement.md`, content supplied in the conversation and summarized by the amendment.
- ADR 0009, `docs/adr/0009-effect-mq-background-jobs.md`, content supplied in the conversation and summarized by the amendment.
- User-supplied allocation source showing application operations, explicit tx-passing reads/writes and receipt recovery. It is supporting design context, not runtime proof or the full implementation specification.

## Repository references

### S01: Repository engineering and test-change constraints

`AGENTS.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/AGENTS.md

Evidence level: instructions. Inherited from the supplied packet evidence registry.

### S02: Adopted design versus remaining facts and proof

`docs/open-decisions.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/docs/open-decisions.md

Evidence level: maintained decision record. Inherited from the supplied packet evidence registry.

### S03: Adopted FX, VAT and impairment contracts

`docs/adr/0008-financial-fx-vat-impairment.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/docs/adr/0008-financial-fx-vat-impairment.md

Evidence level: adopted design, not runtime proof. Directly reread at this commit during this pseudocode task.

### S04: Current Effect, transport and PostgreSQL ownership

`apps/api/README.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/README.md

Evidence level: implementation documentation. Inherited from the supplied packet evidence registry.

### S05: Case review routes a bare latestPlanId

`apps/web/src/components/case-context.tsx`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/web/src/components/case-context.tsx

Evidence level: implementation inspected. Inherited from the supplied packet evidence registry.

### S06: Correction-bundle provenance and unresolved browser handoff

`apps/api/docs/CASES.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/CASES.md

Evidence level: implementation documentation. Inherited from the supplied packet evidence registry.

### S07: Supplier posting and partial credits already exist; actual VAT and paid refunds remain separate

`apps/api/docs/SUPPLIER-ACCEPTANCE-PAYMENTS.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/SUPPLIER-ACCEPTANCE-PAYMENTS.md

Evidence level: implementation documentation with bounded recorded observations. Inherited from the supplied packet evidence registry.

### S08: Actual-profile refusal and synthetic exact-25-percent calculation

`jurisdictions/se/src/vat/calculation.ts`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/jurisdictions/se/src/vat/calculation.ts

Evidence level: implementation inspected. Inherited from the supplied packet evidence registry.

### S09: Offline payment exports stay reserved after reported rejection

`apps/api/docs/PAYMENT-RECOVERY.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/PAYMENT-RECOVERY.md

Evidence level: implementation documentation with bounded recorded observations. Inherited from the supplied packet evidence registry.

### S10: Per-page cursor persistence and unsupported mutation-window recovery

`apps/api/docs/PLAID-CONNECTOR.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/PLAID-CONNECTOR.md

Evidence level: implementation documentation with bounded recorded observations. Inherited from the supplied packet evidence registry.

### S11: Raw connector observations are not bank-accounting admission

`apps/api/docs/BANK-CONNECTOR.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/BANK-CONNECTOR.md

Evidence level: implementation documentation with bounded recorded observations. Inherited from the supplied packet evidence registry.

### S12: Owner facts, effects and allocations; actual treatment and corrections remain bounded

`apps/api/docs/OWNER-REGISTER.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/OWNER-REGISTER.md

Evidence level: implementation documentation; early integration paths may be historical. Inherited from the supplied packet evidence registry.

### S13: Existing staging, financial import and read-only historical items

`apps/api/docs/SIE-HISTORICAL-IMPORT.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/SIE-HISTORICAL-IMPORT.md

Evidence level: implementation documentation with bounded recorded observations. Inherited from the supplied packet evidence registry.

### S14: Existing bounded SIE4I renderer

`jurisdictions/se/src/sie/encoder.ts`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/jurisdictions/se/src/sie/encoder.ts

Evidence level: implementation inspected. Inherited from the supplied packet evidence registry.

### S15: Existing frozen trial balance and earlier-posting opening semantics

`apps/api/docs/REPORTS.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/REPORTS.md

Evidence level: implementation documentation. Inherited from the supplied packet evidence registry.

### S16: Dimension catalog contracts

`packages/contracts/src/dimensions.ts`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/packages/contracts/src/dimensions.ts

Evidence level: implementation inspected. Inherited from the supplied packet evidence registry.

### S17: Bounded legal customer invoice issue; credits remain unsupported

`apps/api/docs/AR-LEGAL-ISSUE.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/AR-LEGAL-ISSUE.md

Evidence level: implementation documentation with bounded recorded observations. Inherited from the supplied packet evidence registry.

### S18: Existing exact-description preparation runs, not general invoice accounting

`apps/api/docs/AUTOMATION.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/AUTOMATION.md

Evidence level: implementation documentation. Inherited from the supplied packet evidence registry.

### S19: 9050 plus 9107 employee/work-input foundation

`apps/api/docs/PAYROLL-FOUNDATION.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/PAYROLL-FOUNDATION.md

Evidence level: implementation documentation. Inherited from the supplied packet evidence registry.

### S20: Financial closing, tax bridge and statutory output requirements

`docs/plans/06-year-end-reports-filing.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/docs/plans/06-year-end-reports-filing.md

Evidence level: working plan, not implementation proof. Inherited from the supplied packet evidence registry.

### S21: Product capability inventory and accounting packet aliases

`docs/plans/capability-backlog.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/docs/plans/capability-backlog.md

Evidence level: working plan. Inherited from the supplied packet evidence registry.

### S22: Retained money representation, licensing and deferred Rust extraction

`docs/architecture-followup.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/docs/architecture-followup.md

Evidence level: maintained design record. Inherited from the supplied packet evidence registry.

### S23: Historical implementation checkpoints; compare later feature notes before using

`docs/plans/accounting-completion-wave.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/docs/plans/accounting-completion-wave.md

Evidence level: historical progress log. Inherited from the supplied packet evidence registry.

### S24: Scope and delivery checkpoints

`docs/roadmap.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/docs/roadmap.md

Evidence level: maintained roadmap with historical entries. Inherited from the supplied packet evidence registry.

### S26: Maintained documentation entrypoint

`docs/README.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/docs/README.md

Evidence level: repository documentation. Inherited from the supplied packet evidence registry.

### S27: Current journal lines lack dimension assignments; shared action union includes VAT work

`packages/domain/src/ledger.ts`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/packages/domain/src/ledger.ts

Evidence level: implementation inspected; shared WIP-sensitive contract. Inherited from the supplied packet evidence registry.

## Official external references inherited from the original dossier

X identifiers are scoped to this dossier. They do not inherit the numbering of the earlier handoff. Those prior checks supported narrow source observations, not blanket qualification of Swedish accounting, tax or provider behavior.

### X01: Plaid Transactions errors

https://plaid.com/docs/errors/transactions/

Pagination mutation requires restarting the affected window from its original cursor. Other error classes are not automatically the same recovery.

### X02: Plaid Transactions Sync migration

https://plaid.com/docs/transactions/sync-migration/

Complete-window retrieval and added/modified/removed processing inform staged publication. This dossier makes no live Plaid request.

### X03: Plaid Transactions API

https://plaid.com/docs/api/products/transactions/

Provider update identity, cursor fields, pending relationships and amount semantics must follow the selected response contract. Exact HTTP bytes remain evidence, not proof of complete bank coverage.

### X04: BFN framework-version applicability

https://www.bfn.se/vilken-version-av-k-regelverken-ska-jag-tillampa/

Select the accounting framework by the actual fiscal-year applicability rules and exceptions. A current calendar date is not a universal rule-version selector.

### X05: Skatteverket: services from another EU country

https://www.skatteverket.se/foretag/moms/kopavarorochtjanster/inkopfranandraeulander/kopatjansterfranandraeulander.4.361dc8c15312eff6fd1d011.html

General-rule business service purchases can require basis in box 21, output VAT in the applicable box and separately eligible input deduction. Do not apply this merely from a foreign supplier name.

### X06: Skatteverket: services from outside the EU

https://www.skatteverket.se/foretag/moms/kopavarorochtjanster/inkopfranlanderutanforeu/kopatjansterfranlanderutanforeu.4.361dc8c15312eff6fd33a46.html

The corresponding qualified general-rule service-purchase basis is distinguished through box 22. Exceptions, tax-point conversion and deduction remain explicit.

### X07: SIE Group format family

https://sie.se/format/

Voucher transfer and transaction export with the preceding balance information are distinct format purposes. Exact record grammar/versions still require their own qualified specification.

### X08: Skatteverket machine-readable tax tables

https://www.skatteverket.se/specialversionerforprogramforetagmfl.4.319dc1451507f2f99e86ee.html

Payroll must use the exact dated table/column/formula or an applicable individual decision. No complete table data set was downloaded or qualified here.

### X09: Skatteverket employer contributions

https://www.skatteverket.se/arbetsgivaravgifter

Rates, eligibility and thresholds are effective-dated inputs. The payroll examples in this dossier are synthetic, not actual Swedish contribution rates.

### X10: Skatteverket cash-principle guidance

https://www4.skatteverket.se/rattsligvagledning/edition/2026.7/325040.html

Search-supported guidance on paid/provided compensation, cross-checked with AGI item guidance. Direct retrieval of this legal-guidance page failed; no broader legal interpretation is attributed to it.

### X11: Skatteverket AGI fields and individual identity

https://www.skatteverket.se/agbeskrivning

The reporting identity includes employer, period, payee and specification number. Preserve the same identity for a replacement instead of creating another individual item. The technical portal also surfaced inconsistent 1.1.18.x labels, so exact XSD bytes must be pinned independently.

### X12: Skatteverket AGI corrections

https://www.skatteverket.se/foretag/arbetsgivare/lamnaarbetsgivardeklaration/rattaenarbetsgivardeklaration.4.2cf1b5cd163796a5c8b6698.html

Reported withholding cannot ordinarily be lowered as a routine amendment. The initial profile refuses that change without a separately qualified exception and keeps authority outcomes distinct.

### X13: Skatteverket SRU file transfer

https://www.skatteverket.se/foretag/etjansterochblanketter/allaetjanster/tjanster/filoverforing/informationomsruuppgifter.4.3dfca4f410f4fc63c86800020896.html

Search-supported identification of INFO.SRU and BLANKETTER.SRU. Direct page retrieval was unsuccessful. No exact field-code map, encoding or current grammar bundle is certified here.

### X14: Skatteverket Inkomstdeklaration 2

https://www.skatteverket.se/4.39f16f103821c58f680006188.html

INK2, INK2R and INK2S are distinct parts of the corporate declaration. The calculation and mapped form values must reconcile; obtaining a form is not proof that an exported SRU file is accepted.

## Deliberately not claimed

No current full BAS data release, payroll tax table, SRU field map, AGI XSD bundle, K2 taxonomy or provider agreement was completely ingested and qualified. Those are enumerated data inputs in [the rule/form data contract](01-RULE-AND-FORM-DATA.md), not guessed examples. No production credentials, user documents, vendor raw corpus, source code or fonts are distributed in this dossier.

No repository patch, applied migration, application test, hosted deployment, actual-company posting, payment, declaration filing or provider acceptance was performed by producing this pseudocode.

