# Common contract for NEXT-26 through NEXT-50

Late branch movement is recorded in [REVISION-NOTE.md](REVISION-NOTE.md). The source review remains pinned; the current resolver is consumed rather than rebuilt.

This is a second wave of implementation-level pseudocode, not another rewrite of NEXT-01 through NEXT-25. Repository evidence is pinned to `5ac3433e3e75ef7fc0229cbe00107003b63aa32d` on 26 September 2026. The current application replacement remains in progress. A packet can be designed now but cannot be called implemented until its actual dependencies and runtime proofs exist.

The initial 25 application-owned v2 packets remain their financial owners. The five named WIPs and the current SQL-to-Effect replacement remain reserved. No packet below restarts them. Source review here was targeted, not an every-file audit. No application tests, migration, real financial operation or provider request was run.

## 1. The implementation boundary

`Domain` means pure typed calculations over explicit input. `App` means named Effect application operations. `Db` means bounded parameterized reads and DML accepting the caller's transaction. These are notation, not a requirement for an interface factory, service tag or file for every helper.

Application code owns authorization, rule selection, eligibility, capacity policy, preparation, approval, execution and recovery. PostgreSQL owns authoritative persisted records, scoped references, exact storage constraints, uniqueness, row locks, rollback-safe counters and narrow immutable-voucher integrity. Do not restore feature stored procedures, a SQL command dispatcher or a duplicate policy engine.

Use the installed Effect/Drizzle transaction adapter, existing verified-principal admission, Better Auth, TanStack Query and StyleX. REST, MCP and the Bun job runner reach the same application operation. An ordinary MCP tool cannot grant human approval. A trusted backend with DML permissions is the policy trust boundary; database constraints do not prove human judgment.

### Port prerequisite, not an extra task

Before coding a packet, resolve `APP-SLICE-READY(area)` against the actual checkout: its named operations, scoped persistence and complete correction/recovery behavior must be released by the migration owner. An HTTP function that returns UnsupportedProfile is not a ported implementation. If that prerequisite is missing, deliver the leaf calculator/schema and its exact integration contract without taking over the migration owner.

The current plan reports placeholder operations and retained policy guards still requiring work [R02]. Treat that as a dated source statement, not an assumption that every placeholder is still present when the agent starts.

## 2. Values and conventions

Money uses canonical exact integer strings over the wire and `bigint` internally. Signed journal notation in these documents is debit-positive and credit-negative. Actual output retains the existing paired `debitMinor`/`creditMinor` schema. Never convert an amount, balance or sequence to a JavaScript number. Quantity, rates and distance use explicit exact rational or bounded decimal representations with units.

```text
roundExact(n, positiveDenominator, policy):
    q, r = divmod(abs(n), positiveDenominator)
    match policy:
      exact: require r==0; increase=0
      toward_zero: increase=0
      half_up: increase=(2*r >= positiveDenominator ? 1 : 0)
      half_even:
        increase=(2*r>positiveDenominator OR (2*r==positiveDenominator AND q odd) ? 1 : 0)
      otherwise: fail UnsupportedRounding
    # Half-up here means ties away from zero.
    result = sign(n) * (q + increase)
    assert result within the destination codec's bound
    return {result, residualNumerator: n-result*denominator}

splitCumulatively(totalComponent, totalGross, priorConsumedGross, nextGross, policy):
    require totalGross>0 and totalComponent>=0
    require 0 <= priorConsumedGross <= totalGross
    require 0 <= nextGross <= totalGross-priorConsumedGross
    old = roundExact(totalComponent*priorConsumedGross, totalGross, policy).result
    require the retained effective release matches old under this policy version
    consumed = priorConsumedGross+nextGross
    now = totalComponent if consumed==totalGross else
          roundExact(totalComponent*consumed, totalGross, policy).result
    return now-old

allocateByWeights(total, positiveIntegerWeightsByStableId, policy):
    require total>=0, unique IDs and all weights>0
    require policy==largest_remainder_stable_id_v1
    W = sum(weights); require W>0
    share[id], remainder[id] = divmod(total*weight[id], W)
    left = total-sum(shares)
    order IDs by descending remainder, then the declared stable byte ordering
    increment the first left shares by one minor unit
    require sum(shares)==total
    return exact shares and retained allocation witness

addSigned(role, amount, sourceAndDimensionRefs):
    if amount == 0: emit no line
    else emit {resolvedAccountId, debit=max(amount,0), credit=max(-amount,0), refs}
finishJournal(lines):
    require every line has one positive side and valid exact amount
    require sum(debit-credit)==0 and complete semantic component membership
    # Equal account IDs do not justify merging different tax/source components.
```

A reported integer filing amount, accounting minor-unit amount and externally assessed amount are different fields. A rounding residual is retained and explained, not automatically posted as a plug. Exact source assertions are retained even when rejected.

`businessDate` uses the operation's explicit legal/calendar meaning and timezone. `recordedAt` is a database-derived instant. Queries that reconstruct history use both accounting dates and recorded cutoffs. Hash order, arrival order and a user's clock do not establish economic chronology.

## 3. Records that are evidence, decisions and authority

Keep original document bytes, provider observations and extraction suggestions separate from reviewed facts. A provider callback authenticates a transport origin only to the extent the selected adapter proves; it does not establish deductibility or settlement. A reviewed classification is not a posting approval.

Each plan retains owner, schema version, compiler/rule release, complete source identity, relevant revisions, exact effects and a canonical digest. Authority names the exact plan/revision/digest and permitted operation. A code deployment cannot silently reinterpret an old approved plan. Either its semantic version is supported or a new preparation and review is required.

Deduplication has three levels:

```text
content hash -> identical bytes
provider/source identity + revision -> repeat delivery of that occurrence
economic operation identity -> this financial effect may happen only once
```

Do not collapse legitimate equal-byte documents. Do not allow a new request key to repeat the same economic effect. Conversely, evidence may legitimately support multiple different financial components when the relationship is explicit.

## 4. Preparation and typed approval

```text
prepareSpecific(command):
    capturedOrReplay = short admitted transaction(tx, principal):
        recover exact scoped command if already committed
        capture selected facts, complete relevant population and revisions consistently
        return a typed immutable basis
    if replay: return it

    proposal = SpecificDomain.compile(capturedBasis, reviewedInput)
    # Pure computation. No client-supplied arbitrary effects or unreviewed model authority.

    return short admitted transaction(tx, principal):
        lock book and declared resources using the shared lock plan
        recover exact command first
        recheck captured revisions and membership, including previously empty populations
        validate proposal's complete domain equations
        insert typed plan and command receipt

approveSpecific(command):
    admitted transaction(tx, human):
        lock declared authority/book/resource set
        recover exact command first
        load exact plan and current approval prerequisites
        require authorized human and independent reviewer where the profile requires it
        append immutable approval with expiry, scope and digest
        save receipt; do not execute the plan
```

A bounded calculation may stay inside one short transaction. Do not introduce capture/seal/job machinery for a trivial check. Model inference, provider I/O, document rendering and human waiting never occur while financial locks are held.

## 5. Atomic application execution

`FinancialTx` below is specification shorthand for the existing actual Drizzle/Effect transaction. It is not a proposed generic financial interpreter.

```text
executeSpecific(command):
    return withAdmittedPrincipal(currentAccess, command.scope, namedPermission, (tx, principal):
        # Current requester admission and its required locks already established.
        BookDb.lockWriter(tx, scope)
        prior = CommandDb.replay(tx, scope, principal, operation, key, exactInput)
        if prior: return prior

        plan = PlanDb.getExact(tx, scope, planId, digest)
        require plan owner and semantic versions supported
        require no committed effect already owns plan.economicIdentity
        lock and load declared period/account/domain/approval resources
        require current selected dependencies and population agree with plan
        ApprovalApp.validateWithinTransaction(tx, principal, plan, approvalId)
        SpecificDomain.assertStoredEffects(plan, currentBasis)

        result = SpecificApp.applyWithinTransaction(tx, validatedPlan, currentBasis)
        # ALL journal, tax, register and capacity writes required by this named operation.
        # Nested operations use this tx and never call public execute/HTTP or open a new tx.
        ApprovalDb.appendUse(tx, exactApprovalId, result.operationIdentity)
        OutboxDb.appendRequiredIntents(tx, result.stableEventIdentities)
        receipt = ReceiptDb.append(tx, approvedDigest, actualEffectRefs, noJournalIfApplicable)
        CommandDb.save(tx, completeCommandIdentity, receipt)
        return receipt
    )
    # The wrapper returns success only after COMMIT acknowledgment.
```

If an operation needs no financial approval, its contract says so statically. A caller cannot select `skipApproval`. Matching, party resolution and fulfillment links can legitimately produce no voucher. True zero financial deltas get a no-effect receipt, not a fake zero journal.

Current access still applies to replay. Replay of a committed identical command precedes fresh-plan, approval-expiry and current-config checks. Old approval expiry cannot erase historical success. A different actor/input/operation under the same key conflicts; another authorized actor can discover the existing effect through an authorized read rather than impersonating the original command.

Domain failure, SQL failure and cancellation cross the transaction boundary. Do not swallow a failed child write and return success after partial DML. Unknown commit outcome is recovered with the original request identity. Never automatically invent another key. Idempotency records survive queue-history pruning.

### Lock and query discipline

Use the root-owned global lock protocol. Do not independently choose an approver-membership locking order in a domain worker. The admitted requester, book, relevant period/account resources, domain resources, approval authority and counters must have one deadlock-analyzed ordering shared with revocation. If the installed helper cannot satisfy it, raise one exact root prerequisite rather than substituting a cached permission read.

Initial financial serialization is per book. Every competing writer that changes a capacity or readiness predicate participates. Set-based queries load distinct resource IDs once; aggregate usage independently before joining requested legs. Do not multiply sums by joining repeated request legs. Never hide inconsistent copies with MAX. Discovery counts/rankings do not become financial dependencies.

Read-only multi-query reports use one coherent snapshot, not unrelated READ COMMITTED statements. Durable pagination uses frozen membership and a stable real anchor. Empty filtered pages can still have continuation.

## 6. External attempts, queue delivery and artifacts

Use the chosen persistent Bun/effect-mq runner. API Workers remain request-scoped. The application owns domain intent, cancellation version and receipts; effect-mq owns queue scheduling, claims and retries. No new generic queue runtime.

```text
domain tx: domain effect + outbox intent commit together
relay: enqueue stable job identity, then acknowledge intent
handler: resolve current scoped service authority, read intent/revision, call named App operation
```

Enqueue acknowledgment loss can duplicate jobs. A stale queue handler can still run after claim loss. Domain fences and receipts must reject or recover it.

For real external effects:

```text
prepare -> approve exact target/bytes -> admit dispatch attempt in tx
    -> provider call OUTSIDE tx
    -> retain observed outcome in a new tx
```

The local dispatch-admission transaction is the ordering boundary for a simultaneous cancellation or payment. It cannot guarantee that an external recipient sees no message after that instant. If cancellation wins before admission, no call is allowed. If dispatch wins, the result can be pending or unknown and must be reconciled honestly. Without provider idempotency or read-back, ambiguous send is not safe to retry blindly.

A lease expiring does not prove an external call never happened. Terminal failure status must come from evidence appropriate to that provider. Polling uses persisted references; no job payload contains user credentials. Server-side current scope is required before admitting or acting on returned data.

Artifacts are generated outside financial locks from immutable semantic content. Store exact bytes, hash, length, renderer and schema versions before attaching them in a short transaction. Failure can leave orphan bytes for controlled cleanup, not a false successful artifact. Signing or filing always references a specific artifact/semantic revision.

## 7. Safety against duplicated first-wave work

Do not rebuild NEXT-01..25. Each packet states its delta from them. Import the shared calculation/obligation owner or extend its typed contract through the integrator. A library-shaped folder is not a reason to add another writable financial register.

Reserved handoffs remain:

- VAT reclassification execution/qualification and VAT amendment delta inventory.
- FX principal partial-release computation and paired-balance mutations.
- Asset impairment UI/control/disposal base closure.
- Webshop order intake, catalog snapshots and order conversion capacity.
- Current application-owned migration and its placeholder-operation closure.

Read-only integration is not permission to edit a reserved owner. A true combined financial group requires a released internal `applyWithinTransaction(tx, ...)` function.

## 8. Independent proof and status

For each assigned implementation retain a before/after financial vector, identity/capacity checks, repeated-key recovery, different-key economic duplicate refusal, stale approval, concurrent consumer and failure after each persistence phase. Add real runtime/provider observations only under actual authorization. This dossier adds no repository tests and grants no deployment, production data reset, bank-payment or filing authority.

Task states are separate: designed, leaf implementation, integrated, runtime observed, company-qualified and externally accepted. First-wave proposals are not assumed complete. A documented function that refuses every case is not a completed packet.

The packet bodies contain proposed new contracts and bounded examples. Explicit unavailable rule tables or provider schema packages are external inputs, not invented algorithms. Do not label unqualified output as legally valid. Perform current primary-source qualification for the actual company and reporting interval.
