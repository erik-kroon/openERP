# Shared contract: NEXT-76 through NEXT-100

This fourth wave contains proposed new work, not a finding that the first75 tasks are complete or that every capability is absent from unreviewed source. The attached NEXT-51..75 dossier supplies the preceding ownership and scope. The current targeted repository check is pinned to `66355b62b23e3b8007c2d324f3739fbbcc96cdc0`, observed 28 September 2026. Sources and review limits are in SOURCES.md.

## C0. Scope, provenance and priority

Extend ordinary Swedish AB accounting and its actual review/billing/evidence work. No bank, card issuer, lender, factoring marketplace, perpetual-stock system, corporate consolidation or general HR/CRM platform is adopted. Conditional tax, payroll, grant and project profiles are not universal Book Zero prerequisites. Prior incomplete integration stays with its original NEXT/core owner; do not relabel it as a new task.

`Domain`, `App` and `Db` in these documents are proposed responsibility names, not assumed existing exports or a new framework. Bind them to the current owning application modules. Retain Effect, the selected Drizzle adapter, Better Auth, TanStack Query and StyleX. PostgreSQL is the authoritative store with scoped structural integrity; business decisions live in application code. The separate persistent Bun/effect-mq process runs background work. No feature stored procedures, independent register balances or generic financial-command interpreters are added.

Current AGENTS.md, source ownership and test authorization must be checked before coding. Use forward schema changes for installed data. Do not reset a meaningful book or change old digests because a previous pre-release plan described a disposable baseline. These packets authorize no tests, deployments, production financial actions or provider calls by themselves.

## C1. Exact values

Wire monetary values are canonical integer strings carrying currency and scale. Domain operations use bounded bigint/rational values, never floating point or string ordering for amount comparisons. Rates, quantities, units, amounts, identifiers and calendar ordinals are separate types. Every destination codec is range checked.

```text
roundRatio(n,d,policy):
    require d>0
    q,r=divmod(abs(n),d)
    exact: require r==0; a=q
    toward_zero: a=q
    floor: a=q+(n<0 AND r!=0 ?1:0)
    half_up: a=q+(2*r>=d ?1:0)
    half_even: a=q+(2*r>d OR (2*r==d AND q odd) ?1:0)
    unsupported policy -> refuse
    result=sign(n)*a
    return {result,residual:n-result*d}

allocateExact(total,weightedStableIds):
    require total>=0, unique IDs, weights>=0 and sum(weights)>0
    q[id],r[id]=divmod(total*weight[id],sum(weights))
    remaining=total-sum(q)
    increment first remaining IDs ordered by r descending then declared stable ordering
    require sum(q)==total; return q with retained witness

releaseCumulative(component,basis,used,next,policy):
    require basis>0 AND 0<=used<=basis AND 0<=next<=basis-used
    target(x)=component if x==basis else roundRatio(component*x,basis,policy).result
    require retained effective release agrees with target(used)
    return target(used+next)-target(used)
```

A product allocation rule is not automatically a statutory tax rounding rule. Preserve source tax, deductible tax, reporting amount and assessed amount separately. Journal examples use debit-positive signed amounts. Real inserts retain paired debit/credit fields. Omit zero financial lines without deleting meaningful zero semantic facts. Never invent an unexplained balancing plug.

## C2. Dates, revisions and evidence

Use actual civil dates and half-open service intervals `[start,endExclusive)`. Supply, earned, approved, posted, due, expected, available-for-recipient and paid dates are not interchangeable. Reporting selects the qualified date for its own obligation. A current UI date cannot silently replace a historical fact or move a refused posting into an open period.

Content hash deduplicates bytes; source identity/revision deduplicates delivery; economic identity deduplicates the financial event. A review ID or new request key is not a new business event. Historical invoices, original journal lines, rule releases, approved plans and successful receipts are immutable. Revision creates linked new meaning rather than editing history.

Qualifying legal rules and company facts is separate from writing a deterministic calculator. No rates, eligibility, agreements, shareholder entitlements or public-authority outcomes are invented by this dossier. Synthetic examples prove only the specified arithmetic. Source prose and model confidence do not grant authority.

## C3. Capture, compile and approval

```text
prepareNamed(command):
    captureOrReplay = admitted short transaction:
        authorize current scope; replay exact command first
        capture complete selected membership, values and relevant revisions coherently
    if replay: return saved result
    plan = NamedDomain.compile(capture, reviewedInputs)
    admitted short transaction:
        lock book and declared resources in global order
        replay exact command first
        recheck captured dependencies, including previously empty relevant populations
        persist the exact complete plan, body digest and receipt
```

A small operation may stay in one short transaction. Large captures need fixed membership, counts, continuation and a coherent cutoff. Do not let raw totals from one snapshot mix with line details from another. A failed or unauthorized domain read is not an empty set.

Parse arrays with their array/JSON schema, not object-only helpers. Decode an outer release before selecting its family. Hash the fully constructed unsigned body, including final timestamps, then add its own digest. Approval's body hash is distinct from the hash of the financial plan it authorizes. Domain source-line identities include their parent recognition.

An approved plan freezes amounts, financial identities, rule/profile versions and selected destinations. A material change needs new preparation/review. Historical successful execution can still be read after its former approval expires, under current access. No task below grants ordinary agents the right to approve or activate their own mandate.

## C4. Atomic application operations

`OwnedTx` is notation for the existing transaction wrapper, not a library to build.

```text
executeNamed(command):
    withAdmittedPrincipal(currentAccess,scope,permission,(tx,principal) =>
        BookDb.lockWriter(tx,scope)
        previous=CommandDb.replay(tx,principal,scope,key,operation,exactInput)
        if previous: return previous
        plan=PlanDb.loadExact(tx,scope,id,digest)
        require correct owner and supported semantic version
        require economic identity not already applied
        load and lock relevant resources in the reviewed global order
        validate current dependencies, authority, exact approval and complete equations
        result=NamedApp.applyWithinTransaction(tx,validatedPlan)
        record approval use, actual effect receipt and required outbox intents
        save complete command result
        return result
    )
    # Caller observes success only after COMMIT acknowledgment.
```

All journal, source-capacity, tax, obligation, schedule and register writers participating in one effect receive the same tx. No nested public execute/HTTP call, new connection or independent commit is allowed. Application errors, interruption and SQL failures cross the transaction boundary. Do not catch failed SQL inside the transaction and keep querying an aborted connection.

Follow the shared authority-before-book, period/account, domain, approval and counter lock protocol. No domain may invent a conflicting order or use a cached EXISTS authorization check as a race solution. Batch-load distinct IDs and independently aggregate usages. Repeated request legs must not multiply persisted capacity sums. Every competing writer of the same residual participates in the same serialized owner protocol.

PostgreSQL retains scoped keys/references, exact storage constraints, uniqueness, immutable history and narrow voucher completeness/balance integrity. It does not independently certify correct business judgment. One shared commerce residual must feed invoices, ageing, collections, payments and Cash. New noncash allocations contribute through that owner instead of patching one screen.

Current private admission precedes replay. Replay of the same committed command precedes new-work freshness and expiry checks. A new key cannot repeat the economic event. Unknown commit outcome uses original-key recovery; absence of a receipt from one momentary read does not prove rollback or cancellation.

A no-journal action still has an atomic record/receipt boundary. Complete-effect membership matters even when the journal sums to zero. Corrections must repair the owned register/source consequences too, not only reverse a voucher.

## C5. External delivery and artifacts

Application outbox intent commits with the domain result. The separate effect-mq runner handles delivery/retry transport; business state, cancellation versions and receipts remain authoritative. An expired queue lease cannot prove a network request never happened.

```text
freeze payload + target -> authorized dispatch admission in short tx
-> perform network call OUTSIDE financial locks
-> retain raw authenticated outcome in short tx
```

A cancellation before admission prevents dispatch. After admission, expose possible/in-flight/unknown outcomes honestly. Provider idempotency/read-back must be documented rather than inferred from a local key. Returned provider data creates evidence, not implicit financial approval. Credentials never appear in source evidence or ordinary queue payloads.

Artifacts render outside transactions from retained semantic content and exact renderer/schema versions. Store bytes, hash, size and validation results; attach in a short reauthorized tx. Recovery returns retained bytes before rerendering. A local PDF, a sent message, a signed artifact, a filed declaration and authority acceptance are distinct states.

## C6. UI and completion

Every packet delivers one real supported workflow using existing routes/components, not merely a pure leaf. Include exact review, useful refusals, scoped historical/current reads, receipt recovery and affected report/control consumers. Current-status displays never rewrite historical snapshots.

Completion stages: designed; pure/compiler source; application/storage integrated; actual supported journey observed; qualified company/rule profile; external result observed if relevant. Only the first two stages are insufficient. A manual official-channel handoff may be an explicitly supported delivery mode with real evidence, never a simulated API success.

Document independent examples for success, stale approval, same-key recovery, different-key economic duplicate, competing capacity consumption and late failure rollback as applicable. New acceptance examples do not override repository test-change permissions. Root owns shared schema/grants, contract exports, transaction/admission primitives, capability classification and global UI/job composition.

The five historical WIP families, current migration owners and NEXT-01..75 retain their current ownership. Reconcile what has actually landed before implementation; do not freeze an old WIP label as a claim of present status. New task numbers are work IDs, not migration prefixes.
