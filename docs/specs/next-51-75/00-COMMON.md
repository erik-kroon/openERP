# Shared contract: NEXT-51 through NEXT-75

Edition: wave 3, prepared 28 September 2026. Detailed repository basis: `116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5`. These are 25 proposed new work packets, not an assertion that NEXT-01..50 is operationally complete. The current progress ledger distinguishes many pure leaves from their remaining application and provider work [R02]. Missing integration of an old packet stays with that old owner.

The source review was targeted: current progress, the parity and Book Zero plans, the ERPNext review, current contributor instructions and selected payment code. No every-file audit, new application test, deployment or real financial action was performed. Public code search can lag HEAD and is not an exhaustive absence proof. A container clone failed because DNS was unavailable; the connected GitHub reader supplied the repository evidence.

## C0. Product scope and the ownership rule

Extend ordinary Swedish AB accounting. Source-grounded requirements are distinguished from proposed design choices in each packet. This wave does not adopt a bank, lending, factoring, credit-decision, card-issuing, warehouse or consolidation product. Goods workflows below cover explicitly supported invoice/customs accounting, not a perpetual-stock ledger. Procurement and budgets are optional operating extensions, not prerequisites to Book Zero.

Reuse the named Effect application operations, pure domain/jurisdiction calculators, transaction-passing persistence and existing HTTP/MCP capability registry. PostgreSQL remains the authoritative store with reviewed relational constraints and narrow integrity. Do not add business-policy stored functions, another general transaction framework or an event-sourcing rewrite. Ordinary agents may read and prepare within scope; approval and external mandate remain explicitly human/authorized operations.

Reuse the existing commerce residual/capacity owner. PRY-133 requests consistent readers, not a second writable outstanding balance. New allocations, advances, losses and schedules contribute through that owner. Do not fix only one screen while payment preparation and Cash use a different residual.

Cite historical task IDs as dependencies, not migration numbers. Root owns shared schemas, grants, journal admission, capability registration and common UI/runtime integration. Use forward migrations for already-applied installations; never edit applied history, reset a real book or revive the old disposable-baseline assumption. Resolve current dirty ownership claims before coding.

## C1. Explicit types and exact arithmetic

Wire money is a canonical integer string with declared currency/scale. Domain money is a bounded `bigint`. Filing integers, minor units, quantities, rate ratios and calendar ordinals are different types even if all serialize as strings. A value named Minor never returns a count of whole kronor. No floating-point amount arithmetic or lexicographic comparison of money.

```text
roundRatio(n, d, mode):
    require d > 0
    q,r = divmod(abs(n),d)
    match mode:
        exact: require r==0; a=q
        toward_zero: a=q
        floor: a=q + (n<0 AND r!=0 ? 1 : 0)
        half_up: a=q + (2*r>=d ? 1 : 0)
        half_even: a=q + (2*r>d OR (2*r==d AND q odd) ? 1 : 0)
        otherwise: UnsupportedRounding
    value = (n<0 ? -a : a)
    check destination bound
    return {value, residualNumerator:n-value*d}

roundToQuantumMinor(n,d,positiveQuantum,mode):
    units = roundRatio(n,d*positiveQuantum,mode).value
    minor = units*positiveQuantum
    return {minor, residualNumerator:n-minor*d}

allocateExact(total, weightsByStableId):
    require total>=0, distinct IDs, integer weights>=0 and sum(weights)>0
    W=sum(weights)
    each share[id],remainder[id]=divmod(total*weight[id],W)
    left=total-sum(shares)
    add one to the first left IDs ordered by descending remainder then stable ID
    require sum(shares)==total
    return shares and witness

releaseOriginalComponent(totalComponent,totalCoverage,usedCoverage,nextCoverage):
    require totalCoverage>0 AND 0<=usedCoverage<=totalCoverage
    require 0<=nextCoverage<=totalCoverage-usedCoverage
    target(x)=totalComponent if x==totalCoverage else
              selectedQualifiedCumulativeRule(totalComponent*x,totalCoverage)
    require priorEffectiveRelease==target(usedCoverage)
    return target(usedCoverage+nextCoverage)-target(usedCoverage)
```

`allocateExact` is a proposed deterministic product rule, not automatically the correct tax-rounding rule. The activated treatment chooses the appropriate tax calculation order. Store any original source tax separately from deductible tax. One original GL line is counted once even when several facts cite it; contribution allocations must sum to that line, not duplicate it per fact.

Journal notation is debit-positive. Actual writes use the repository's debit/credit columns. Omit zero posting lines, retain meaningful zero semantic facts and never manufacture a balancing plug. Validate complete group membership and both financial/register conservation before posting.

## C2. Dates, source identity and semantic history

Use explicit business-calendar dates and half-open service intervals `[start,endExclusive)`. Accounting date, supply/tax date, expected payment date, bank booking/value date and statutory reporting period stay separate. A timestamp string is not proof of an accounting date. The current payroll open-period correction decision remains with NEXT-36/PAY-04; none of these packets reverses that decision or reopens locked history by default.

Distinguish content hash, source occurrence, external provider identity and economic operation identity. Identical bytes can support multiple legitimate occurrences. A new request or review ID cannot make the same business event happen twice. Namespaced source-line IDs do not collide across different invoices.

Original documents, issued numbers, reviewed releases, approved plans and successful receipts remain immutable. New meaning gets an explicit schema/calculator/profile version. Do not silently reinterpret existing plans after widening a schema. Labels and current party details do not replace captured historical values.

## C3. Capture, compute, seal

Small operations may stay in one short transaction. Larger deterministic calculation uses a coherent captured basis, computation outside locks and a short recheck/seal transaction. One transaction connection does not by itself guarantee a coherent multi-statement read; use the current shared book barrier or a deliberate snapshot protocol.

```text
prepareSpecific(command):
    captureOrReplay = admitted short tx:
        recover identical command first
        capture selected facts, complete relevant membership and owner revisions
    if replay: return saved result
    computed = SpecificDomain.compile(capture,reviewedInputs)
    short admitted tx:
        lock required book/resources
        recover identical command first
        recheck selected versions and relevant population, including previously empty sets
        validate all predicted journal/register/control effects
        persist exact plan and receipt
```

Use typed JSON values correctly. Arrays go through array/JSON schemas, not object-only encoders. Decode an outer shared release before selecting its nested family. Build the complete unsigned body, including final timestamps, hash it using its declared canonicalization and only then add its own digest. Approved-plan digest and approval-record body digest are separate fields and meanings.

Approval binds exact scope, plan ID/digest, relevant policy and expiry. A price change, different beneficiary or recalculated tax requires a new plan where financially material. An old approval does not authorize an arbitrary future batch.

## C4. Complete application transactions

`OwnedTx` below is notation for the existing Effect/Drizzle transaction owner, not a new library to install.

```text
executeSpecific(command):
    withAdmittedPrincipal(currentAccess,scope,requiredPermission,(tx,principal) =>
        BookDb.lockWriter(tx,scope)
        prior=CommandDb.replay(tx,principal,completeCommandIdentity)
        if prior: return prior
        plan=PlanDb.loadExact(tx,scope,planId,planDigest)
        require correct named owner and supported semantic version
        require economic operation not already applied
        load and lock relevant periods/accounts/capacities/authority in global order
        revalidate dependencies, exact approval and complete effect equations
        result=SpecificApp.applyWithinTransaction(tx,validatedPlan)
        consume exact approval
        append effect receipt and required outbox intents
        save command result
        return result
    )
    # Success is returned only after actual COMMIT acknowledgment.
```

Every nested financial writer receives `tx`. It must not independently commit, open another runtime, invoke public HTTP or enqueue an external effect inside that transaction. Failure, interruption and database exceptions must cross the transaction boundary. Do not catch a failed SQL statement and continue querying its aborted transaction. Unknown commit outcome uses original-key recovery, not another financial key.

Current private permissions are checked before returning sensitive replay or historical data. New-work freshness, approval expiry and changed configuration do not override an already committed identical receipt. Economic uniqueness separately blocks a duplicate event under another key.

Follow the root-owned global lock plan, including approver authority and cancellation. All writers that compete for a capacity must use the same serialization or reservation protocol. An ordinary SQL `EXISTS` read is not a reviewed race solution. Do not introduce domain-local lock order or session tenant flags. Named no-financial-effect operations write no voucher but still own their record/receipt atomicity.

Each new mutation must update the existing residual/currentness/read contracts. Controls retain unexplained records even if they net to zero. Imported openings and historical events are not re-recognized.

## C5. External actions and artifacts

The persistent Bun/effect-mq runtime remains the durable runner. The application owns business intent, cancellation version and receipts. The queue owns claims and retries. Job history pruning must not erase financial or submission idempotency. An expired job lease does not prove that a network effect never happened.

```text
prepare exact semantic payload and destination
    -> human authorization where required
    -> short tx admits one scoped external attempt with stable identity
    -> network call OUTSIDE financial transaction
    -> short tx retains authentic raw outcome and derived domain status
```

A cancellation winning before dispatch admission prevents the call. If admission wins first, a subsequent cancellation cannot promise the remote system saw nothing. Without documented provider idempotency/read-back, ambiguous send remains unknown and blocks replacement. Never invent a provider key guarantee or API endpoint. Transport accepted, instruction accepted, cash booked and obligation fulfilled are distinct observations.

Render immutable artifact bytes outside locks from a frozen semantic revision and pinned renderer/schema. Retain digest, size, exact content and validation report. Recovery returns retained bytes before attempting a new render. A report page is not authority acceptance. A handoff file remains useful without API credentials, but the packet's selected external-outcome gate stays open.

Skatteverket submission packets 72-74 share the existing external-attempt infrastructure, not a newly built generic filing engine. Their report identities, submission scopes, signature steps and correction behavior remain separately typed. The public portal entry points were verified, not every production API specification or access agreement.

## C6. Native UI, APIs and operational completion

Reuse React/TanStack Router/Start, TanStack Query, Better Auth and StyleX. Each packet includes an operator workflow, exact review, permission-aware reads, meaningful failures and receipt recovery. Data parsing does not execute macros or formula links. Guest sharing never grants book-list or accounting API access. Monetary messages identify units and currency.

Read/prepare/execute capabilities reach one application operation regardless of HTTP, MCP or job caller. Do not expose approvals because a new capability forgot its authority classification. Internal helper exports and a pure test case are not finished customer behavior.

Completion is recorded by stage:

```text
designed -> leaf compiled -> application integrated -> supported journey observed
         -> selected rule/company qualified -> external outcome observed, if applicable
```

A packet cannot be marked complete with only the first two stages. It can be useful locally while credentials are missing, but that is a stated limited stage. Scope not applicable to the company is a reviewed fact, not a label used to hide unfinished required work.

## C7. Evidence and dispatch policy

For each implemented financial packet demonstrate through the actual owner: a supported operation, late failure rollback, same-key replay, distinct-key economic duplicate, competing capacity use, stale review/authority and correction with preserved originals. Read-only packets need actual capture/filter/pagination/access and reproducible exported values. External packets additionally need the selected provider or honest manual-handoff outcome evidence.

This package supplies independent example checks in its own folder. It does not change repository tests, grant provider access, authorize real postings or change the user's test-change policy. Use actual current AGENTS.md and any separately granted test authorization. Update manifests with the lockfile and keep frozen install enabled. Do not run unbounded parallel checks merely because workers are parallel.

The five originally reserved WIP identifiers and current branches must be reconciled at dispatch. Some have advanced since earlier reviews. Retain their current owner rather than freezing the old WIP status or allocating duplicate work. Do not renumber PRY or the 53 core packets. NEXT-51..75 is this design's new delivery namespace, cross-linked to those maintained owners.
