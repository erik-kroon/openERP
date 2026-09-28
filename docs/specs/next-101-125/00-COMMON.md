# Common execution contract: NEXT-101 through NEXT-125

This fifth wave supplements the first 100 packet designs. It neither declares them finished nor reassigns their missing integration. The attached 76..100 package establishes the previous scope. A current branch read and targeted operations/shared-contract reads use `66355b62b23e3b8007c2d324f3739fbbcc96cdc0` on 28 September 2026. No complete source audit or application execution is claimed.

The new collaboration, provision, specialist tax and controlled-automation choices are proposed designs. Legal applicability, business evidence and provider outcomes remain separate qualifications. The new standing-mandate packet is opt-in later scope: it does not silently replace Book Zero's exact human-approval default.

## C1. Owner, scope and explicit values

Effect application operations own policy, identity, authorization, workflow and scoped writes. Pure domain/jurisdiction code calculates over immutable typed facts. Parameterized `Db` queries read or write on the caller's actual transaction. PostgreSQL supplies authoritative records, rollback, row locks, scoped foreign keys, uniqueness, immutable history and narrow complete-journal integrity. No feature SQL procedure or parallel tax engine is introduced.

Private internal `applyWithinTransaction(tx, ...)` calls never open a connection, start a runtime, call HTTP or commit independently. Public commands run with no caller transaction unless an explicit internal aggregate contract exists. API/MCP/job wrappers call the same owner. Scope comes from trusted admission, never a document, URL ID alone or queue payload assertion.

Wire money is canonical integer text with currency/scale. Rates, unit counts and original decimal lexemes are distinct exact types. Bigint arithmetic does not permit string comparison, floating-point conversion or confusing whole units with minor units. Sequences use the actual bounded counter type, not the wider amount limit. Dates are valid business-calendar dates; instants are recording/authority times. Service intervals are half-open. Fiscal, tax, reporting, payment and evidence dates remain separate.

```text
roundRatio(n,d,mode):
  require d>0
  q,r = divmod(abs(n),d)
  match mode:
    exact: require r==0; add=0
    toward_zero: add=0
    floor: add=(n<0 AND r>0 ? 1 : 0)
    half_up: add=(2*r>=d ? 1 : 0)
    half_even: add=(2*r>d OR (2*r==d AND q odd) ? 1 : 0)
    otherwise: UnsupportedRounding
  value=sign(n)*(q+add)
  require destinationBounds(value)
  return value and n-value*d

roundToMinorQuantum(n,d,quantum,mode):
  require quantum>0
  return roundRatio(n,d*quantum,mode).value*quantum

allocate(total,weightsByStableId):
  require total>=0, unique IDs, integer weights>=0, sum(weights)>0
  floorShare,remainder = divmod(total*weight,sum(weights)) for each ID
  distribute total-sum(floorShare) units by descending remainder then declared stable ID order
  require sum(shares)==total
  return shares and complete input/policy witness

cumulativeRelease(component,totalCoverage,used,next):
  require totalCoverage>0, component>=0, 0<=used<=totalCoverage, 0<=next<=totalCoverage-used
  target(x)=component when x==totalCoverage else qualifiedRound(component*x/totalCoverage)
  require retainedEffectiveRelease == target(used)
  return target(used+next)-target(used)
```

The distribution algorithm is a product policy, not a universal statutory rounding rule. Specific tax/profile calculations can require other aggregation orders. Retain exact source tax separately from calculated and deductible tax. Sum each physical GL component once; several explanatory facts can allocate its amount, not each copy the complete amount.

Journal notation is debit-positive, but storage keeps the existing debit/credit fields. Emit no zero journal lines. A semantically meaningful zero fact or a verified zero-effect result is retained without fabricating a voucher. Never plug an unexplained reconciliation difference.

## C2. Plan construction and identity

An immutable plan binds owner, full scope, operation/economic identity, source revisions, rule/calculator versions, date/unit conventions, exact effects, complete selected population and relevant dependency epochs. Canonicalization excludes the plan's own digest and mutable progress. Compute final timestamp and other unsigned content before hashing. Plan digest and approval-body digest have separate fields. Arrays remain arrays through shared JSON codecs; decode outer releases before their nested family.

Content hash identifies bytes. Source identity/revision identifies one observation. Economic identity prevents one business effect happening twice across different request keys/transports. Equal bytes can still belong to different occurrences. A new generated claim/draft ID is not a new invoice or payment.

Capture relevant data coherently under the existing read snapshot/book barrier. Scope membership includes an initially empty population epoch. Do not use a maximum observed value to hide inconsistent capacity reads. Batch distinct IDs and aggregate each capacity once before joining requested legs. Candidate counts and display labels are not financial execution dependencies.

```text
prepareSpecific(command):
  capturedOrReplay = short admitted tx:
    recover exact committed command first
    capture typed selected facts and complete scope with dependency witness
  if replay: return saved result
  proposed = SpecificDomain.compile(captured, reviewedInputs)
  short admitted tx:
    lock required authority/book/resources in the root-owned order
    replay exact command first
    recheck captured dependencies and complete scope
    validate named domain equations and supported profiles
    persist immutable plan and command receipt
```

Small bounded computations can stay in one short tx. Model calls, network, object downloads, document rendering and human waiting stay outside financial locks. An unavailable required source is not an empty list. Proposals that contain unresolved judgment remain review work rather than executable financial plans.

## C3. Atomic application execution

```text
executeSpecific(command):
  withAdmittedPrincipal(currentAccess, scope, operationPermission, (tx, principal) =>
    BookDb.lockWriter(tx, scope)
    prior=CommandDb.replay(tx, principal, completeCommandIdentity)
    if prior: return prior
    plan=PlanDb.loadExact(tx, scope, id, digest)
    require supported semantic version and correct owner
    require economic effect not already committed
    lock/read relevant periods/accounts/domain capacities and authority in shared order
    validate current basis, applicable policy and exact approval
    result=SpecificApp.applyWithinTransaction(tx, validatedPlan, currentBasis)
    record approval/mandate use as required by the static operation contract
    append exact receipt and explicitly required outbox intents
    save immutable command result
    return result
  )
  # Return success only after the actual transaction runner acknowledges COMMIT.
```

Journal, register, source usage, tax facts, counters, authority consumption and receipt for one group commit together. A derived reader must incorporate each new effect through its existing owner, not only one screen. Never call another public executor to achieve a combined transaction.

Current private access precedes sensitive reads/replay. Replay of an identical committed command precedes new-work expiry or stale checks. Another key cannot repeat the economic action. An unknown commit outcome retains the original key/input for recovery. Cancellation, exceptions and failed DML cross the transaction boundary; do not swallow failure after partial writes or keep querying an aborted transaction.

Retain the reviewed global lock protocol: requester credential/membership admission before book, then relevant periods/accounts and domain resources, approval/approver authority and rollback-safe counters. Root alone extends this order for delegation or mandates. No domain-specific book-first authority updater may create an inverse lock path. Revocation is an authority-only operation unless a reviewed complete ordering says otherwise. Cross-book financial groups remain unsupported.

New nonfinancial actor/delegation operations need explicit identity transaction composition, not a fake journal. A firm dashboard uses separate authorized client-book reads with individually labelled cutoffs, not a global financial transaction or combined confidential cache.

## C4. Readers, corrections and accounting date

Current balances are projections of retained effects and adopted openings. They never independently authorize writes without the source owner recheck. Changes update the shared residuals consumed by ageing, payments, Cash and controls. Do not add a private outstanding balance only the new feature reads.

A posted correction preserves original documents, plans and receipts. It repairs all affected register/tax/authority consequences. If a later payment or closed period consumed them, use the supported linked adjustment/correction policy or refuse with exact impact. Do not automatically reopen locked periods. Payroll preserves ADR 0014's explicit authorized open-date adjustment default; tax/reporting attribution is separate.

A captured report fixes its financial cutoff, mapping, classifications and source membership. Later publication or new labels do not rewrite it. A currentness change appears separately. Historical replay is not inserted into a live cache as if it were the newest state.

No real bank/customer/provider source is silently dismissed to make the books balance. Unknown exposure is retained even when offsetting values sum to zero. A book-level equality check is necessary but does not establish source completeness, legal treatment or independent substantiation.

## C5. External attempts and persistent delivery

Use existing outbox intent and the persistent Bun/effect-mq worker. Queue claims/retries are not financial identity. Domain run versions and external-attempt states remain authoritative after queue pruning or expired leases.

```text
prepare exact payload/target -> explicit permitted human authorization
  -> tx admits one attempt and reserves applicable source capacity
  -> provider call outside tx
  -> tx retains original response plus typed current outcome
```

Admission orders cancellation: if cancellation commits first, no new call is allowed. If dispatch admission commits first, a later cancellation cannot claim the provider saw nothing. Without documented idempotency/read-back, an ambiguous request remains unknown and blocks replacement. Never treat lease expiry, local timeout, HTTP200 or browser redirect as proof of no execution, payment settlement or authority acceptance.

Artifact generation uses frozen semantics and qualified renderer/schema bytes outside locks. Retain hash/length/content and validation evidence, then attach via a short transaction. Return existing retained artifacts before trying to render again during recovery. Authenticity and scope of provider callbacks must be checked before current access or financial effects are inferred. Secrets are neither source evidence nor job parameters.

## C6. Standing automation is a separate capability

NEXT-121 is an explicit optional later-scope extension to an allowlisted application operation. It never creates a counterfeit human approval or enables itself through a rule edit. Ordinary Book Zero operations stay human-approved by default. Payment, refund, issue, payroll, period close, signing, tax adjustment and filing powers are excluded from its first bounded scope. NEXT-96 quorum routing is not a standing mandate.

The execution authority union must be implemented deliberately across API, application and persistence before activation. Cumulative budgets are shared and checked atomically in execution, not only per plan. Qualification is required even when inputs look similar to previously approved work. Rule simulation and confidence are not authority.

## C7. Native UX, APIs and completion

Extend existing StyleX/Paraglide/TanStack components and scoped query keys. Every new packet needs usable prepare/review/execute/read/recovery or evidence-only output, not a pure file with no consumers. Shared operation schemas declare permissions and effects for every capability; neither a missing annotation nor an API key can default to human financial powers.

Success is a persisted receipt. Loading, empty, unknown, stale, denied, pending external outcome and service failure remain different. Private payroll data never appears in a firm/project aggregate without a separately permitted projection. Financial originals retain provenance; a search result or estimate cannot overwrite their authority.

A packet's status is: designed, leaf implemented, application integrated, supported journey observed, company/rule qualified and provider outcome observed where applicable. A passing local calculation closes only its actual assertion. New tests, runtime exercises, database changes or external actions need current repository/user authorization.

Use forward migrations where records have already been retained/applied. Do not reset meaningful books or resurrect the earlier disposable-baseline assumption merely because an old plan mentions it. All existing NEXT/PRY/core owners and currently reserved tasks keep their scopes. The new wave is not evidence that the prior 100 are complete.
