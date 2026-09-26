# OpenERP: NEXT-26 through NEXT-50, solved in application-owned pseudocode

This complete second-wave specification supplements the prior NEXT-01..25 application-owned v2 package. It does not assume those tasks are done. The five reserved workstreams and current application migration remain owned elsewhere.

Detailed source review is pinned to `5ac3433e3e75ef7fc0229cbe00107003b63aa32d`. A later branch observation found `4671a2fbaea88bcab613f28b6d34a209b040ab06` reporting NEXT-01 implementation. The final revision note records that limited observation without pretending the intervening diff was fully reviewed.

**Status:** proposed pseudocode and implementation contracts. No source patch, deployed feature, executed application test or legal/provider qualification is claimed. See the source map and design-check report for exact limits.

## Contents

1. [Common contract for NEXT-26 through NEXT-50](#part-01)
2. [Qualified inputs for the second wave](#part-02)
3. [NEXT-26: Supplier extraction jobs and field-level reviewed merge](#part-03)
4. [NEXT-27: Reviewed party identity resolution without balance merging](#part-04)
5. [NEXT-28: Authorized collection reminders and dispatch recovery](#part-05)
6. [NEXT-29: Recurring invoice occurrences without duplicate billing](#part-06)
7. [NEXT-30: Customer unapplied cash, paid credits and refunds](#part-07)
8. [NEXT-31: Invoice-linked prepayments and accrued-cost true-up](#part-08)
9. [NEXT-32: Loan principal, interest accrual and repayment allocation](#part-09)
10. [NEXT-33: Employee expense claims with one financial handoff](#part-10)
11. [NEXT-34: Mileage reimbursement with exact tax and payout partition](#part-11)
12. [NEXT-35: Variable pay, absence and holiday-liability reconciliation](#part-12)
13. [NEXT-36: Paid payroll recovery and retroactive compensation](#part-13)
14. [NEXT-37: VAT assessment ownership and exact-to-assessed bridge](#part-14)
15. [NEXT-38: Cash-method recognition and unpaid year-end cutover](#part-15)
16. [NEXT-39: Processor balance and payout clearing, Stripe first](#part-16)
17. [NEXT-40: Foreign-currency cash holdings and transfers](#part-17)
18. [NEXT-41: Late FX valuation and consumed-chain correction](#part-18)
19. [NEXT-42: Economic impairment reversal and zero-carrying assets](#part-19)
20. [NEXT-43: Reviewed dimension restatement without editing journals](#part-20)
21. [NEXT-44: Multi-year SIE partition and dimension-preserving import](#part-21)
22. [NEXT-45: Direct cash-flow statement with a full reconciliation bridge](#part-22)
23. [NEXT-46: Peppol invoice and credit exchange through a selected access point](#part-23)
24. [NEXT-47: Document signatures bound to exact content and purpose](#part-24)
25. [NEXT-48: Bolagsverket submission and authority-outcome lifecycle](#part-25)
26. [NEXT-49: Rule-change impact and evidence-backed obligation fulfillment](#part-26)
27. [NEXT-50: Agent book context, deltas and cross-domain unresolved-work index](#part-27)
28. [Integration, non-overlap and dispatch](#part-28)
29. [Consequential decisions made in this wave](#part-29)
30. [Coordinator instruction](#part-30)
31. [Sources and evidence boundaries](#part-31)
32. [Repository movement during this review](#part-32)


---

<a id="part-01"></a>

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


---

<a id="part-02"></a>

# Qualified inputs for the second wave

Reuse NEXT-02's rule and company profile ownership. Do not build another rule registry. The fields below define the exact missing inputs that a selected packet needs. They are not permission for an LLM to invent rates or execute arbitrary policy code.

Every release binds a finite named calculator/adapter, exact data/schema checksums, applicability predicates, evidence source, reviewed expected cases, unsupported cases and an activation review. A human selecting a release does not qualify missing source data. Retain old used releases as historical provenance even after new use is withdrawn.

| Family | Required qualified data | Packet |
|---|---|---|
| Extraction | Provider/model/parser identity, output schema, source-location contract, data-use permission, cancellation and cost limits | 26 |
| Identity resolution | Legal-identity schemes, evidence interpretation and supported entity/branch cases | 27 |
| Reminder channel | Message identity, provider idempotency lifetime, delivery-status meaning, read-back and cancellation semantics | 28 |
| Recurrence | Calendar anchor, end-of-month policy, service coverage, timezone and changed-cadence rules | 29 |
| Customer credit | Same-currency credit treatment, refund-liability roles and distinction from taxable advances | 30 |
| Deferral/accrual | Expense-recognition method, service-date basis, partial-period allocation, estimate/credit treatment | 31 |
| Loan | Actual agreement, day-count convention, rates, dated principal changes, repayment split and supported accounting treatment | 32 |
| Employee claim/trip | Employer obligation, payer/vehicle facts, rate unit, tax exemption, taxable excess and one payout route | 33-34 |
| Variable payroll | Actual employment schedule, agreement, supported sick/absence/holiday formulas, tax/contribution tables and entitlement valuation | 35 |
| Paid correction | Enforceable recovery or lawful future-pay adjustment, original paid/reporting facts and case-specific declaration treatment | 36 |
| VAT bridge | Exact return-box/whole-unit rounding, settlement-account roles, assessment identity and typed tax-account evidence | 37 |
| Cash method | Actual eligible accounting/VAT method, payment recognition, unpaid year-end population and supported credit rules | 38 |
| Stripe | Account/mode/API version, balance types, source links, fees, payout identities and independent balance controls | 39 |
| Foreign cash | Currency scales, acquisition/release policy, reporting-rate witnesses and supported cash/overdraft boundary | 40 |
| FX repair | Original event chronology, every affected calculation version, corrected rate and permissible correction dates | 41 |
| Asset reversal | Eligible asset/framework, recoverable-value evidence, without-impairment cap, residual and new future schedule | 42 |
| Classification | Explicit analytical policy, original data restrictions and revised report basis | 43 |
| SIE | Exact supported record grammar, encoding, source years, object mappings and omission rules | 44 |
| Cash flow | Reviewed cash perimeter and classification/FX/perimeter-change policy | 45 |
| Peppol | Exact UBL/XSD/Schematron/code lists plus chosen access-point routing/outcome specification | 46 |
| Signing | Actual document-signing protocol, visible consent, signed-data binding, certificate validation and purpose eligibility | 47 |
| Filing | Actual service specification, checksum algorithm, supported artifact, temporary upload, certifier/submission and authority receipts | 48 |
| Deadlines | Effective statutory rule, timezone/holiday policy, required fulfillment predicate and scope-bound receipt types | 49 |
| Agent context | Per-domain summary schema, complete-count/continuation semantics, access filtering and stable state revisions | 50 |

## Selection algorithm

```text
selectRelease(family, operationFacts, semanticDates):
    candidates = registered qualified releases that match family and exact applicability
    if none: MissingQualifiedRelease(family, affectedOperation)
    if more than one unresolved: AmbiguousRelease with exact candidates
    require finite calculator/adapter implementation supports this case
    require every mandatory fact has evidence and a current authorized review
    return exact release ID/hash, required inputs and dependency witness
```

Select by the operation's relevant dates, not `latest(today)`. Loan agreement terms, holiday formulas and advance-tax behavior cannot be inferred from adjacent supported profiles. The observed Peppol release title is not a substitute for its actual XSD/Schematron bytes. The BankID and Bolagsverket entry points did not establish all their exact machine contracts in this review.

## Provider interface without fictitious guarantees

```text
SelectedProviderProfile {
    actualApiVersion, operationSchemas, requiredCredentials,
    requestIdentity, idempotencyRetention?, readBackIdentity?,
    terminalOutcomeMeaning, cancellationMeaning,
    authenticatedObservationRules, unsupportedBranches
}
```

Absence of provider idempotency/read-back is represented as absent. Do not emulate it by merely reusing a local command key. A timeout around an external call stays unknown until the provider contract supports resolution. Local simulation demonstrates application state behavior, not authentic provider execution.

## Actual data and acceptance

The dossier uses artificial financial amounts and selected mathematical policies for examples. It provides no live company payroll, bank credentials or signing identity. Independently qualified statutory values and real source coverage remain necessary before a company uses affected operations. This does not block independent schema, compiler or state-machine implementation.


---

<a id="part-03"></a>

# NEXT-26: Supplier extraction jobs and field-level reviewed merge

**Priority:** P0. **Owner lane:** INTAKE. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** apps/api/src/application/purchases/inbox.ts; application/purchases/drafts.ts; existing source-retention adapters and supplier-inbox contracts.

**New scope, not repeated work:** The current inbox can record extraction attempts and bind a reviewed draft. Add the actual bounded extraction lifecycle and safe reprocessing, not another inbox, matcher or purchase engine.

**Dependencies:** No new first-wave financial feature is a hard prerequisite. **Integrate after:** APP-SLICE-READY(purchases/inbox).

**Conditional gates:** NEXT-03: a reviewed draft is subsequently accepted and posted.

**Evidence:** R03, R08 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Records and selection

```text
ExtractionRequest {
  id, book, occurrenceId, originalHash, parserOrModelRelease,
  selectedPages, dataUsePolicy, generation, cancelVersion, requestedBy
}
ExtractionAttempt immutable {
  requestId, attemptId, sourceHash, engineRelease, outputSchema,
  result: succeeded | rejected_output | failed | unknown,
  fields: [{fieldKey, proposedValue, sourceLocators[], diagnostics}],
  candidateLines: [{candidateLineId, sourceLocators, fields}], retainedOutputHash
}
FieldDecision immutable {
  occurrenceId, draftRevision, fieldKey, decisionKind,
  selectedValue, attemptId?, evidenceLocators, reviewer, priorDecisionId?
}
UNIQUE(book, requestId, attemptIdentity)
UNIQUE(book, occurrenceId, acceptedDraftOwner)  # reuse the existing actual owner
```

A field key is a semantic identity, not a model array position. A proposed invoice line must have an unambiguous mapping to retained original source locations or receive a new candidate identity for review. Two equal lines are not automatically the same line.

## Preparation and extraction

```text
requestExtraction(input):
  App tx:
    current scope + exact command replay
    require authorized use of this original and chosen engine
    load occurrence metadata and current review/draft state
    capture exact source hash, page selection and engine version
    insert request and outbox intent; save receipt

runExtraction(requestId, expectedGeneration):
  read current request and cancellation/data-use permissions
  fetch original; verify its retained hash and length OUTSIDE tx
  extract existing native text first where supported
  only use selected document/vision provider when necessary and authorized
  enforce bounded bytes/pages/time/cost; no financial tools available to extractor
  decode output strictly: money remains exact source assertions, never JS float
  reject unknown fields, invented source locators and duplicate field IDs
  retain raw interpretation and normalized suggestions
  App tx:
    recover result for this exact source/attempt
    require current generation and cancellation fence
    verify original hash unchanged
    append attempt and receipt; do not change reviewed facts or post anything
```

A provider timeout is an extraction outcome, not a reason to delete the original. Repeated execution can produce different suggestions. Preserve each attempt; only one explicitly selected attempt enters a review. Cancellation after remote computation can discard publication while retaining a diagnostic attempt under the data policy. It cannot erase an already accepted invoice.

## Three-way merge instead of replacing a draft

Use `B` for the reviewed draft revision on which extraction was requested, `L` for the current draft and `S` for suggestions. Compare typed values, not formatted display text.

```text
mergeField(B, L, S, decisions):
  if S has no supported source locator: return needs_review(missing_provenance)
  if a human explicitly confirmed L after B:
      keep L; show S as an alternative, never silently overwrite
  if L != B:
      if L == S: retain convergent provenance, no value change
      else: return conflict(base=B, current=L, suggestion=S)
  if S == B: return unchanged
  return proposed_change(S)  # NOT automatically accepted

prepareExtractionReview(selection, expectedDraftRevision):
  load exact attempt, original and B/L values consistently
  require expected current draft revision matches
  map candidate lines explicitly; retain unmapped/deleted/duplicate-line conflicts
  calculate proposed source totals with existing draft calculator
  expose discrepancy list and exact chosen values
  require human selects each affected conflict and confirms the resulting review
```

For a new inbox record, reuse its existing reviewed-draft creation function inside the caller's transaction. For an unaccepted existing draft, create one new revision with a field-decision manifest. For an already accepted/issued invoice, create a correction-review case referencing suggestions; never revise the original economic document.

## Review transaction and consumers

The review transaction rechecks occurrence, attempt, draft and field-decision versions. It appends decisions, creates/revises the draft through the existing internal tx function and stores the binding/receipt together. A competing review either returns its identical receipt or fails stale; it cannot create another payable. Acceptance and tax preparation remain NEXT-03.

REST/MCP can request extraction and inspect suggestions under the existing permitted prepare role. Human confirmation stays operator-only. The UI places original evidence beside proposed changes and labels fields as source, suggested or reviewed. It displays job failure separately from source validity.

## Required vectors

```text
same request delivered twice -> one recorded result identity, no second draft
model returns 100.00 as numeric JSON -> reject monetary encoding, retain diagnostic
operator changes account after extraction start -> keep operator value + conflict
invoice accepted while extraction runs -> correction suggestions only
two legitimate identical lines -> two source-located line identities
request cancelled before publication -> no draft change or accounting effect
```

Close this packet with a runnable request -> extraction -> human merge -> recoverable draft path. Recording another caller-supplied JSON attempt alone does not satisfy the new scope.


---

<a id="part-04"></a>

# NEXT-27: Reviewed party identity resolution without balance merging

**Priority:** P1. **Owner lane:** COMMERCE. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** apps/api/src/application/commerce/crm-master.ts and commerce/register.ts; existing party revisions, invoice snapshots and payee verification.

**New scope, not repeated work:** Extend the existing directory and annotations with reviewed duplicate identity resolution. Do not build general CRM or silently merge financial capacity.

**Dependencies:** No new first-wave financial feature is a hard prerequisite. **Integrate after:** APP-SLICE-READY(commerce/crm-master).

**Conditional gates:** NEXT-02: legal identity facts or payment-role qualification are needed.

**Evidence:** R03, R05 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Identity model

```text
PartyResolution immutable {
  id, book, members: [{partyId, partyRevision}], canonicalPartyId,
  kind: same_legal_entity | related_but_distinct | not_duplicate,
  legalIdentityWitness, evidence, memberDigest, approvedAt
}
ResolutionChange immutable {resolutionId, replaces?, reason, reviewRef, receipt}
PartyIdentityHead {book, partyId, activeResolutionId?, identityEpoch}
```

Only `same_legal_entity` creates a lookup redirect. Related companies and similar trading names remain separate legal counterparties. Unknown identity can produce a possible-duplicate case, not an irreversible merge. No original party, invoice, payment verification or ledger reference is rewritten.

## Prepare and validate

```text
prepareResolution(selectedIds, chosenCanonical, suppliedEvidence):
  capture all selected party revisions and their current redirect closures
  reject cross-book membership and cycles
  require chosenCanonical belongs to the full resolved member set
  classify identifiers by jurisdiction and legal-identifier scheme
  if incompatible verified legal identities:
      permit related_but_distinct/not_duplicate only
  if same_legal_entity:
      require reviewed evidence establishing identity, not name/email similarity
  capture open obligation IDs, payment reservations and unissued dependent drafts
  report duplicates as candidates; do not net AR against AP
  seal exact member set, revisions, classification and downstream invalidation list
```

A tax registration number or bank account is not universally equivalent to legal identity. Scheme-specific qualification decides which evidence proves identity. Cross-border branches and represented entities need explicit treatment.

## Atomic resolution

```text
executeResolution(command): FinancialTx without journal
  recheck current scope, replay and exact approved resolution
  lock selected identity heads in stable ID order
  require full closures and all member epochs equal prepared basis
  append resolution and advance each affected identity head
  invalidate dependent UNEXECUTED payee/payment and party-sensitive plans
  preserve issued document snapshots and all existing allocations
  append identity_changed outbox event and receipt
```

Discovery for new documents follows the canonical identity but still selects a current legal revision explicitly. The old IDs remain searchable. New supplier duplicate checks search the entire resolved group, while returning the original invoice owner and source identity. They must not merge two invoices merely because the parties now resolve together.

## Financial reads and reversal

```text
resolvedDirectoryBalances(group, cutoff):
  retrieve each ORIGINAL obligation once by stable obligation ID
  group by legal identity and currency for presentation
  retain per-source-owner detail and control-account classification
  never sum different currencies or cancel AR with AP implicitly

settleExistingInvoice(invoiceId):
  use original invoice and its existing capacity owner
  identity resolution is provenance/discovery, not extra payment capacity
```

An erroneous identity resolution is replaced by a reviewed resolution change. It does not undo financial operations that used the grouping. Any unissued plans based on it become stale. Already issued invoices and verified payee facts remain historical and receive impact cases when relevant. Before splitting a group, identify any newer records that actually depended on its legal identity; missing evidence blocks their further use, not the ability to inspect history.

Runtime reads must avoid redirect recursion. Resolve a bounded member set under an epoch and reject cycles/oversize data. A materialized current lookup can accelerate discovery but is rebuildable from retained decisions and never owns ledger values.

## API/UI and completion

Add prepare/approve/apply/read/history operations under party resolution. The UI shows original and proposed identities, evidence, invoices affected and explicit statements that balances/issued bytes do not change. Directory exports name their resolution basis and retained original IDs. Existing annotation APIs remain unchanged.

```text
A and B same reviewed legal entity, each has one invoice100 -> total200, not100
A customer and B supplier related but distinct -> no redirect or automatic netting
concurrent A->B and B->C -> one serialized current closure or stale refusal
bank details change while merge review open -> stale payment-dependent witness
undo redirect after invoice issue -> issued party snapshot unchanged
```

Evidence supports an existing directory/annotation owner [R05]. A complete equivalent resolution service was not established by this bounded inspection; reconcile live source before creating its records.


---

<a id="part-05"></a>

# NEXT-28: Authorized collection reminders and dispatch recovery

**Priority:** P1. **Owner lane:** DELIVERY. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** apps/api/src/application/commerce/collections.ts and existing invoice-delivery/legal-delivery adapters; existing dispute and statement records.

**New scope, not repeated work:** The inspected reminder action explicitly records sendAuthorized=false. Add exact-message approval, dispatch admission and outcome recovery without recreating statements or disputes.

**Dependencies:** No new first-wave financial feature is a hard prerequisite. **Integrate after:** APP-SLICE-READY(commerce/collections), APP-SLICE-READY(durable-delivery).

**Conditional gates:** NEXT-15: the selected invoice has credit-note adjustments; NEXT-30: customer-credit balances affect the reminder amount.

**Evidence:** R03, R04 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Durable intent

```text
ReminderIntent immutable {
  id, invoiceIds, customerRevision, recipientRevision,
  balanceSnapshotId, disputeEpoch, templateRevision,
  exactMessageArtifact, amountByCurrency, asOf, stage,
  occurrenceIdentity, contentDigest, expiresAt
}
ReminderApproval {intentId, digest, operator, expiry}
DispatchAttempt {
  id, intentId, channel, providerProfile, externalKey,
  admittedAt, cancellationVersion, exactPayloadHash
}
DispatchObservation immutable {
  attemptId, source, rawRef, observedOutcome, providerCorrelation, receivedAt
}
```

The first profile adds no collection fee or interest. A later fee is its own evidenced financial operation, not a number inserted into an email. One intent corresponds to one approved reminder occurrence, not every queue retry.

## Prepare and authorize

```text
prepareReminder(customer, selectedInvoices, template):
  capture current supported invoices and effective payments/credits at one cutoff
  require positive collectible residual and no applicable dispute hold
  resolve intended recipient with reviewed address revision
  require no active ambiguous send for the same occurrence
  render exact content outside financial locks using frozen statement values
  seal recipient + subject + body + attachments + residual digest

approveReminder(command):
  validate exact digest and permitted stage/recipient
  recheck disputed/settled status and expiry
  append operator approval; append durable send intent in same tx
```

Do not approve a variable template that will pick a different amount or recipient at send time. Changes require another exact preview unless the original approval explicitly covers a finite alternative that the selected profile supports.

## Dispatch boundary and race semantics

```text
admitReminderDispatch(intentId):
  App tx:
    authorize current service identity and book
    lock reminder and referenced live invoice/dispute resources
    recover existing attempt or definitive receipt first
    require exact approval current and not cancelled
    require collectible amounts and recipient still equal the approved basis
    require no live dispute hold and no superseding reminder resolution
    create immutable attempt with stable provider identity
    append dispatch-admitted receipt
  return admitted exact payload

sendAttempt(attempt):
  perform provider call OUTSIDE tx
  persist authenticated/raw outcome evidence
  reduce outcomes using the provider's documented state semantics
  if outcome unknown:
      read back using correlation or retry SAME provider identity only if supported
      otherwise require investigation, never create a new send to probe success
```

If payment or a dispute commits before admission, sending is refused as stale. If admission wins first, the external message can still arrive afterward. Expose that order honestly. Do not hold a database lock across email I/O or claim an impossible atomic transaction with the provider. A known late payment may create a follow-up notification, not rewrite the already sent statement.

Queue claim expiry is not proof no email was sent. Provider idempotency retention can be finite; an ancient unknown attempt cannot be retried merely because its queue job is new. Capture that limit in the selected channel profile.

## Current state and historical evidence

A reminder history separates prepared, approved, dispatch-admitted, provider-accepted, delivered if evidenced, failed and unknown. SMTP/API acceptance is not evidence the customer read it. Collection disputes remain in their existing append-only owner. Dismissing a reminder neither cancels an invoice nor marks its debt paid.

A new deliberate reminder stage gets a new occurrence identity after checking the old outcome, cadence and policy. It does not overwrite the old artifact. Follow-up worklists use current residuals; saved statements keep their prior values.

## Interfaces and required outcomes

Use existing collection read APIs and add named reminder prepare/approve/dispatch-status operations. Only operator approval admits sending. Ordinary agents may propose and inspect. Show exact recipient, invoice references, as-of balance, hold reason and any unknown attempt before a send action.

```text
invoice10000, later paid4000 before dispatch -> stale10000 reminder, no call
new6000 reminder -> approved exact bytes, one external attempt on retry
hold added before admission -> refusal
provider accepted, response lost -> recover same external identity, no second reminder
payment after admission -> retain sent-as-of history and current paid status separately
```

Completion includes a configured adapter's observed send/recovery in an authorized environment. Local state simulation alone does not prove external delivery.


---

<a id="part-06"></a>

# NEXT-29: Recurring invoice occurrences without duplicate billing

**Priority:** P1. **Owner lane:** COMMERCE. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing commerce invoice drafts, legal issuance and application preparation/job owners. Add recurrence beside them without editing webshop intake or order conversion.

**New scope, not repeated work:** NEXT-16 prepares accounting from existing evidence. This packet owns recurring COMMERCIAL invoice occurrences and billing coverage, not recurring manual journals.

**Dependencies:** NEXT-02. **Integrate after:** APP-SLICE-READY(commerce/invoice-lifecycle).

**Conditional gates:** NEXT-15: an issued recurring invoice needs a credit.

**Evidence:** R03, R09 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Stable identity

```text
RecurringAgreement {
  id, book, customerId, anchorLocalDate, timeZone,
  cadenceKind, billingWindowRule, firstCycleOrdinal
}
TemplateRevision immutable {
  agreementId, revision, effectiveFromCycle,
  lines, price/tax defaults, customer snapshot policy, issueDatePolicy
}
AgreementEvent immutable {pause | resume | end | amend, effectiveCycle, evidence}
InvoiceOccurrence {
  agreementId, cycleOrdinal, serviceInterval, chargeComponentKeys,
  selectedTemplateRevision, draftId?, issuedInvoiceId?, status
}
UNIQUE(book, agreementId, cycleOrdinal)
UNIQUE approved billing coverage for a component/service interval
```

Template revision is deliberately absent from occurrence identity. Otherwise editing a template can bill the same cycle twice. Service coverage has its own conflict check to catch frequency changes whose new ordinal scheme would overlap an already billed interval.

## Calendar algorithm

```text
cycleDate(agreement, k):
  if monthly:
    targetMonth = anchor year/month + k*monthInterval
    targetDay = lastDay(targetMonth) if anchorPolicy=end_of_month
                else min(anchorDay, lastDay(targetMonth))
    return localDate(targetMonth, targetDay)
  if fixed_day_interval:
    return anchorLocalDate + k*declaredDayInterval
  otherwise: UnsupportedCadence
```

Always derive from the original anchor. Never repeatedly add one month to a clamped February date. DST changes affect due instants, not the service-cycle identity. Missing/skipped local times use the selected calendar policy or require review; no implicit UTC-month billing.

```text
planDueOccurrences(now, horizon):
  capture agreement state and last materialized cycles
  generate bounded cycle ordinals deterministically up to horizon
  select effective template revision BY CYCLE
  exclude paused/ended cycles according to explicit event policy
  disclose skipped cycles; do not turn resume into catch-up billing by default
  return complete bounded candidate set and continuation
```

## Materialization and issuance

```text
materializeOccurrence(agreementId, cycleOrdinal):
  App tx:
    authorize job, lock book/agreement
    replay exact command first
    if occurrence already has draft/issue: return its owned result
    recheck cadence/template/pause versions and service overlap
    create occurrence with chosen revision and service interval
    draft = InvoiceApp.createDraftWithinTransaction(tx, frozen fields,
             sourceIdentity=agreement+cycle+component)
    link draft and save receipt atomically
```

Creating a draft is not permission to issue. The normal human prepare/approve/execute issue flow applies. The invoice owner must enforce occurrence uniqueness at issuance too, so copying or editing a draft cannot bypass billing coverage. The narrow occurrence reference is part of the approved issue plan; the originating job never mints human approval.

Template defaults become explicit draft values. Current customer facts required for legal issue are revalidated there; frozen service/price facts are not silently replaced. If tax applicability changed, show the recalculated draft and require new review.

## Amendments, pauses and credit

A template amendment names the first affected unissued cycle and the billing boundary. Already issued cycles are immutable. A prepared but unissued draft needs explicit supersession and reapproval when amounts change. A pause that wins before issue admission blocks issuance; a pause after committed issue does not undo it.

A credit through NEXT-15 reduces the issued invoice but does not reopen the recurrence occurrence or permit rebilling the same coverage. Corrected replacement billing is a separate approved relationship, with a once-only replacement identity and net coverage check. Do not decrement an order's converted quantity or modify WIP webshop/catalog ownership.

## Controls and vectors

Report due, skipped, draft, approved, issued and delivered independently. Link every issued cycle to its legal number and ledger receipt. A schedule ending does not delete past invoices or waive their receivable.

```text
Jan31 monthly anchored -> Feb28 -> Mar31, not Mar28
same cycle twice with template v1/v2 -> one occurrence and one issue
pause after draft before issue -> blocked until explicit resume/review
resume after three paused cycles -> gaps disclosed, no surprise catch-up
change monthly to quarterly -> reject overlapping already-billed service coverage
queue failure after draft commit -> recover linked draft, no second occurrence
```

This packet is independent of order intake. Any future order-based recurring contract must consume the existing order owner's capacity rather than infer it from recurrence.


---

<a id="part-07"></a>

# NEXT-30: Customer unapplied cash, paid credits and refunds

**Priority:** P1. **Owner lane:** COMMERCE. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing customer invoice, payment allocation and legal-credit owners. Add customer-credit liability effects and refund operations through their shared transaction boundary.

**New scope, not repeated work:** NEXT-15 stops at unpaid customer credit principal; NEXT-07 handles suppliers. Add the customer-side surplus and paid-credit lifecycle without changing those original meanings.

**Dependencies:** NEXT-15. **Integrate after:** APP-SLICE-READY(commerce/register).

**Conditional gates:** NEXT-04: credit notes affect a supported VAT return.

**Evidence:** R09, P15, P07 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Separate liabilities from negative receivables

```text
CustomerCreditOrigin immutable {
  id, customerId, currency, amount, kind: unapplied_cash | paid_invoice_credit,
  cashReceiptRef? | creditNoteRef?, journalControlRefs, receiptId
}
CustomerCreditEffect immutable {
  originId, kind: apply_to_invoice | cash_refund | owned_correction,
  signedConsumedMinor, destinationIdentity, journalRefs, receiptId
}
availableCredit = originalAmount - effectiveApplications - effectiveRefunds
```

Use an explicit reviewed customer-credit liability role. Do not put negative amounts into the old nonnegative invoice residual. This is not a universal advance/deposit VAT profile: money received before an identified supply may have its own tax timing and must be routed to a qualified advance owner or a visible blocker.

## Unapplied receipt

```text
compileCustomerReceipt(cashEvent, selectedInvoiceLegs):
  require same customer/currency, supported final cash observation
  G = exact incoming cash
  A = sum(explicit invoice allocations)
  require 0 <= A <= G and each leg <= its invoice remaining
  U = G-A
  require U classified as qualified refundable overpayment/unapplied cash,
          not an unreviewed taxable advance
  debit bank G
  credit receivable controls A
  credit customer-credit liability U
  return journal + invoice allocations + credit origin(U)
```

When the bank receipt was already posted through a qualified clearing entry, adopt its proven unused clearing-side capacity rather than debit cash again. Exact source identity and allocations commit with the journal and credit origin. A different request key cannot produce a second cash event.

## Credit after payment

For one same-currency invoice let `G` be original gross, `K` effective credits, `P` payments applied and `Q` resulting credit liability already refunded/applied elsewhere.

```text
unpaidAR = max(G-K-P, 0)
creditPrincipal = max(P-(G-K), 0)
remainingCredit = creditPrincipal-Q

compilePaidCustomerCredit(original, capacity, credit):
  use original-line net/tax compiler from NEXT-15
  C = credit gross; require original line and tax capacities permit C
  arReduction = min(C, unpaidAR)
  creditIncrease = C-arReduction
  debit original revenue and output-VAT effects exactly once
  credit customer AR arReduction
  credit customer-credit liability creditIncrease
  return journal + negative tax facts + retained legal credit + liability increase
```

Execute this as one customer-credit aggregate, extending legal-credit issuance with its number/semantic document. Prior payment allocations remain historical; reducing revenue is not evidence cash was refunded.

## Apply credit or receive an observed refund payment

```text
applyCustomerCredit(creditOrigin, destinationInvoice, amount):
  require same evidenced customer/currency and current capacities
  debit customer-credit liability amount
  credit destination AR amount
  consume credit amount and invoice principal in one tx
  create no bank movement and no new VAT fact

recordCustomerRefund(creditOrigin, cashPaymentEvidence, amount):
  require authorized evidenced payment or compatible existing clearing posting
  require amount <= remaining credit and exact cash source unused
  debit customer-credit liability amount
  credit bank or evidenced refund-clearing role amount
  append refund allocation and receipt together
```

External refund initiation, when selected, is separately approved and outcome-tracked. A refund API response is not automatically a posted bank payment. Unknown outcomes reserve the affected instruction amount until resolved, using the payment-intent owner rather than adding another reservation balance here.

## Corrections and controls

A standalone reversal of an invoice payment that generated subsequently consumed credit is refused. A correction must restore the related credit/application/refund consequences atomically or identify the unsupported dependency chain. Do not edit `P` to make the equation look right.

Reconcile AR and customer-credit liabilities separately. Display original sale, legal credits, historical paid amount, unpaid amount, credit balance and refunds. Cash-method sales and foreign-currency credit liabilities require their own profile integrations; this first profile is same-currency accrual.

```text
G125000 P100000 K0 -> AR25000, credit0
credit50000 -> debit revenue/VAT50000, credit AR25000, credit liability25000
refund10000 -> debit liability10000, credit cash10000; credit remains15000
apply15000 to another invoice -> liability0, that invoice residual drops15000
cash125000 for invoice100000 -> AR settled100000 + refundable credit25000
new key for same credit note -> AlreadyApplied, not another liability
```

These are new customer financial consequences. Existing supplier refund implementation is a calculation reference, not a shared mutable register or permission to flip signs blindly.


---

<a id="part-08"></a>

# NEXT-31: Invoice-linked prepayments and accrued-cost true-up

**Priority:** P1. **Owner lane:** SCHEDULES. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing subledger schedules/occurrence effects and purchase recognition. Reuse application/subledger/schedules.ts and controls.ts, with separate expense-deferral semantics.

**New scope, not repeated work:** Prior packets use existing schedule mechanics but do not specify complete invoice-to-deferral admission and accrued-cost invoice resolution. This adds those relationships without another scheduling engine.

**Dependencies:** NEXT-03, NEXT-13. **Integrate after:** APP-SLICE-READY(subledger/schedules).

**Conditional gates:** WIP-AST03-UI: the released schedule/control implementation is shared with the asset owner.

**Evidence:** R09, R10 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Linked recognition, not another purchase

```text
CostBasis {
  purchaseRecognitionId, sourceLineIds, expenseAccountRoles,
  costMinor = net + qualified nonDeductibleTax,
  serviceStart, serviceEndExclusive, serviceEvidence, currentCutoff
}
DeferralBasis immutable {
  id, costBasisRefs, prepaidRole, originalExpenseRoles,
  allocatedCost, recognitionProfile, scheduleId, reclassificationRefs
}
AccrualDecision immutable {
  id, suppliedServiceIdentity, serviceCoverage, expectedCost,
  expenseRole, accruedLiabilityRole, evidence, cutoff
}
AccrualResolution immutable {
  accrualId, sourceInvoiceLine, coverageConsumed, liabilityReleased,
  actualCost, expenseTrueUp, taxFactRefs, receipt
}
```

The expense cost excludes deductible input VAT. Deferring cost changes accounting expense timing, not VAT tax-point attribution. An invoice can contain immediately consumed and future service portions. A valid tax invoice does not prove a service spans the dates asserted by the model.

## Build an exact schedule from reviewed service coverage

```text
compilePrepayment(basis, selectedPolicy):
  require same-currency supported service cost, reviewed start/end and cost ownership
  require endExclusive > start and nonoverlapping source allocations
  periods = accounting-period intersections with [start,endExclusive)
  weight[p] = exact covered days OR explicitly selected contractual weight
  # No implicit daily proration when the reviewed policy uses equal months.
  shares = allocateByWeights(cost, weights, selectedResidualPolicy)
  require sum(shares)==cost
  recognizedNow = sum(shares whose service is already consumed under cutoff policy)
  future = cost-recognizedNow
  if purchase is unposted:
      use NEXT-03 purchase compiler with cost split into expense and prepaid roles
  else:
      require existing cost components and unused deferral capacity
      debit prepaid future; credit original expense future
      create no payable, cash or VAT fact
  schedule = existing schedule owner with future expense debit/prepaid credit occurrences
  return complete reclassification + basis + future schedule
```

A partial period uses the selected policy's exact dates, not an entire-month shortcut. Zero shares are retained as schedule metadata where needed but create no zero journal. Final positive installment consumes the remaining amount exactly.

`executePrepayment` uses one application transaction to verify source-cost rights, post the reclassification if needed and insert basis/schedule links. If purchase recognition and deferral form one approval, call both internal writers on the same tx. Do not first post an invoice and then rely on a second unapproved job to repair expense timing.

## Accrued expense before an invoice

```text
compileAccrual(decision):
  require evidenced service already received and reviewed supported estimate
  debit expense expectedCost
  credit accrued liability expectedCost
  no deductible VAT fact without qualified supporting tax evidence

resolveAccrualWithInvoice(accrual, reviewedInvoiceCoverage):
  A = exact accrued liability consumed by this matching coverage
  N = actual expense-cost component for that coverage
  T = qualified deductible tax from the invoice owner
  G = N+T
  require explicit overlap/coverage relationship and 0<=A<=remainingAccrual
  debit accrued liability A
  addSigned expense (N-A)  # Can be a credit for an overestimate.
  debit deductible input VAT T
  credit supplier payable G
  return purchase recognition + accrual consumption + signed expense true-up + tax facts
```

This equation assumes the selected actual cost includes non-deductible tax consistently. Mixed invoices split related and unrelated source-line components before calculation. Do not consume an entire accrual for a partially invoiced service unless the evidence supports full settlement of that estimate. An invoice already recognized must be adopted through a once-only accrual-release/reclassification, not posted again.

## Later changes and controls

Estimate changes affect only future unrecognized schedule cost through an approved revision. A termination/refund ties to the original purchase credit and recalculates remaining deferral; the schedule cannot continue recognizing refunded cost. Past recognized expense stays historical or is corrected by an explicit owned operation. An accrued expense reversal can be scheduled only under a selected policy, not blindly every 1 January.

Controls reconcile opening prepaid/accrued positions plus owned changes to closing GL roles. Unknown service coverage prevents complete signoff. UI shows source invoice/estimate, allocation dates, already recognized amount, future balance and eventual resolving invoice.

```text
cost120000 allocated equally to12 periods -> 10000 each, exact total120000
3 consumed periods -> expense30000, prepaid90000; no second VAT recognition
accrual10000, later invoice cost11000 tax2750 -> accrued debit10000,
    expense debit1000, input debit2750, AP credit13750
accrual10000, actual9000 tax2250 -> expense credit1000, not a balancing plug
same invoice resolves accrual twice -> duplicate economic relationship refusal
```

Calculation/true-up is original design bounded by the reviewed policy. A synthetic date schedule is not automatically a legally qualified expense policy.


---

<a id="part-09"></a>

# NEXT-32: Loan principal, interest accrual and repayment allocation

**Priority:** P2. **Owner lane:** TREASURY. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing owner-funding principal records and general ledger/schedule owners. Add a loan-specific effect owner without turning capital contributions into loans.

**New scope, not repeated work:** NEXT-06 recognizes funding and loan principal. This proposed product extension supplies the later accrued-interest and repayment lifecycle; it is not presented as a newly discovered source defect.

**Dependencies:** NEXT-02. **Integrate after:** APP-SLICE-READY(subledger/owners).

**Conditional gates:** NEXT-06: shareholder funding already recognized supplies the opening loan basis; NEXT-13: publishing reconciled loan controls.

**Evidence:** R09, P06 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Bounded contractual model

Start with one book-currency borrowing, fixed or evidenced variable simple-interest rate and explicit repayment allocation. Exclude effective-interest amortized-cost instruments, loan origination fee capitalization, leases, foreign-currency borrowing and debt conversion until qualified profiles exist.

```text
LoanAgreementRevision {
  id, borrower, lender, currency, effectiveInterval,
  principalTerms, interestSegments, dayCountConvention,
  paymentAllocationRule, accountRoleWitness, evidence
}
LoanEffect immutable {
  loanId, kind: drawdown | principal_repayment | interest_accrual |
                interest_payment | rate_correction,
  principalDelta, interestDelta, accountingDate, journalRefs, sourceIdentity
}
InterestCalculation immutable {
  loanId, coverageStart, coverageEndExclusive, principalTimelineDigest,
  rateTimelineDigest, segments, exactRationalTotal, roundedTarget,
  previouslyEffectiveInterest, delta, policyVersion
}
```

Interest accrued is distinct from scheduled interest, due interest and paid interest. A contribution with uncertain repayment rights remains a funding classification case, not a loan inferred from a bank transfer.

## Recognition and adoption

A new drawdown debits cash and credits principal liability through the existing source owner. If NEXT-06 or historical opening already recognized principal, adopt that owned balance with evidence and no new journal. One original funding event cannot supply two principal registers.

```text
principalAt(date, cutoff):
  return reviewed opening
       + evidenced drawdowns effective before date
       - effective principal repayments before date
       + supported owned corrections
```

The profile declares whether a payment affects interest from the beginning or end of its effective date. Use that convention consistently rather than guessing from message arrival time.

## Deterministic interest accrual

```text
calculateInterest(loan, start, end, cutoff):
  require start<end and complete principal/rate timeline
  boundaries = union(start,end,principalChangeDates,rateChangeDates,yearSplitsIfNeeded)
  sum = rationalZero
  for segment [a,b):
      P = principalAt(a); rate = applicableRate(a)
      require P>=0 and one supported rate
      factor = exact dayCountFraction(a,b,convention)
      sum += P * rate * factor
  target = roundExact(sum, selected cumulative rounding policy)
  effective = prior accrued interest for the same owned coverage basis
  return target-effective with full segment witness
```

Recompute from a stable coverage origin or retain exact accumulated residuals. Do not round each day independently. A rate revision requires an explicit effective date and changed-source witness. A subsequent calculation posts the delta to the same cumulative target, not the full target again.

```text
postAccruedInterest(delta):
  debit interest expense delta
  credit accrued interest liability delta
  # negative deltas use opposite signs with an approved correction reason
```

## Repayment allocation

```text
prepareRepayment(cashSource, contractualSplit):
  read exact principal and accrued/due interest balances
  split = explicit reviewed principal, interest and separately evidenced fees
          OR the agreement's qualified deterministic waterfall
  require principalPart<=principalRemaining
  require interestPart<=recognizedInterestRemaining or accrue approved missing part atomically
  require sum(parts)==actual cash amount
  debit principal liability principalPart
  debit interest liability interestPart
  debit qualified fee expense feePart
  credit bank actualCash
  seal register deltas and exact source allocation
```

Execution rechecks agreement/timeline/capacity under the book lock and commits journal, principal/interest effects, cash adoption and receipt together. Automatic bank instructions are outside scope. An existing payment journal can be adopted only with exact role/capacity evidence.

## Changes, output and vectors

A backdated principal or rate change after accrued/paid interest creates a recalculation impact. Compute an explicit delta with stable coverage and preserve prior statements. If a correction requires changing already settled history beyond the supported scope, refuse with affected effects; do not alter old cash payments or simply reset the principal.

Show opening, drawdowns, principal repayments, accrued interest, paid interest and independent lender-statement differences. Missing lender statements are unknown coverage, not zero difference.

```text
principal10000000, annual6%, ACT/365F, 30days -> 49315 minor after half-up
accrue49315 twice with same coverage -> second economic effect0/replay, not98630
repay principal1000000 + interest49315 -> cash1049315, principal9000000
different explicit rates across boundary -> split exact rational segments before rounding
adopt shareholder principal already posted -> ledger delta0
```

No tax deduction, related-party price or legal loan validity is inferred from this arithmetic. Those are qualified profile inputs and are not solved by selecting an interest formula.


---

<a id="part-10"></a>

# NEXT-33: Employee expense claims with one financial handoff

**Priority:** P1. **Owner lane:** PAYROLL. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing source evidence, purchase classification and employee foundation. Reuse liability/allocation mechanics without giving every employee owner-register administration.

**New scope, not repeated work:** NEXT-06 concerns owners. Add employee claim submission/review and an exclusive payroll or direct-payment handoff, not another purchase recognition for the same receipt.

**Dependencies:** NEXT-03. **Integrate after:** APP-SLICE-READY(purchases), APP-SLICE-READY(payroll-foundation).

**Conditional gates:** NEXT-21: the approved payout route is payroll rather than a payable payment.

**Evidence:** R03, R10, P06 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Claim facts and liability ownership

```text
EmployeeClaimRevision {
  claimId, employeeId, paidByEvidence, sourceOccurrences,
  companyBusinessPurpose, submittedItems, currency, revision, previousRevision
}
ClaimDecision immutable {
  revision, approvedItems, rejectedItems, treatmentWitness,
  recognizedPurchaseRefs, reimbursementAmount, reason, reviewer
}
PayoutRoute immutable {
  claimDecisionId, kind: direct_payable | payroll,
  destinationOwnerId, financialRecognitionOwner,
  amount, routeRevision, cancellationOrReplacementRef?
}
UNIQUE economic expense component across purchase/owner/employee recognition
UNIQUE active financial handoff per approved reimbursable component
```

Employee self-service access is restricted to permitted own records and required reviewers. It does not grant general book or payroll directory access. Evidence submission is not approval. Rejected items remain in the source history without creating a liability.

## Review and prepare

```text
prepareEmployeeClaim(revision):
  capture employee identity and exact source/review versions
  for each submitted item:
    confirm company expense, payer and documentary relationship under selected profile
    if already recognized as supplier payable and employee paid it:
        plan AP debit / employee-liability credit, no new cost/tax
    else if not recognized:
        invoke the existing purchase compiler with employee-liability funding role
    else if already employee/owner-funded:
        recover recognized relationship or require conflict resolution
  separate reimbursable cost from taxable cash allowances
  require selected reimbursement route and no conflicting claim component
  seal exact accounting, claimant liability and approved/rejected item manifest
```

A bank/card charge on the company's own account does not automatically create a payable to the employee. Nor may an employee claim VAT just because an image contains a tax amount. NEXT-03's qualified deduction decision remains authoritative.

## Commit and select one payout route

```text
executeClaim(plan): FinancialTx
  verify current reviewed claim revision, source identity and financial owner
  post expense/tax or AP-transfer group through internal existing owners
  create employee reimbursement liability with source-item capacity
  append exactly one route owner for each payable component
  if payroll route:
      add payroll instruction referencing EXISTING reimbursement liability
      do not book expense or liability a second time in payroll
  save receipt and required preparation outbox
```

In payroll the claim may appear on the payslip as a cash reimbursement. Its accounting is debit employee reimbursement liability / credit payroll-payment clearing or bank on actual payout. It is not new salary expense. Taxable allowance components follow the payroll tax profile instead and are excluded from tax-free claim capacity.

For a direct-payment route use the existing payee verification, payment instruction and bank settlement owners. Exporting an instruction does not settle the claim.

## Route changes and recovery

A route can be replaced only if its prior destination owner proves the referenced component unexecuted and unreserved or provides a valid cancellation/release. An unknown payroll/payment outcome blocks another route. Queue cancellation alone is insufficient. A route change retains both decisions and the release receipt.

A correction before payment can reverse/replace the complete claim aggregate if no dependent tax filing or later settlement prevents it. After reimbursement, an overpaid amount becomes a separately reviewed employee receivable or legally supported future offset, not a negative new expense claim. NEXT-36 owns the paid payroll consequence when payroll was the route.

## Controls and visible workflow

Provide employee submission, reviewer side-by-side evidence, approved amount, rejected explanation and payout status. Display claimed, recognized, instructed, paid and recovered states separately. Reconcile employee-liability totals with the GL and payroll-payment handoff, including imported openings.

```text
employee paid qualified purchase net10000 tax2500 -> liability12500 once
payroll shows reimbursement12500 -> no new expense/tax on pay-run posting
direct payment5000 -> employee liability7500
same receipt component resubmitted under another claim -> existing recognition/conflict
switch payroll to direct while payroll payment unknown -> refused, no second instruction
company-paid card receipt -> no employee reimbursement liability
```

This is a claimant workflow around existing purchase recognition. Do not create an independent employee-cost ledger or use a mutable paid flag as the accounting source.


---

<a id="part-11"></a>

# NEXT-34: Mileage reimbursement with exact tax and payout partition

**Priority:** P2. **Owner lane:** PAYROLL. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Employee claim and payroll handoff owners. Add trip evidence and qualified rate calculation without altering receipt matching or inventing a universal mileage rate.

**New scope, not repeated work:** The first wave does not calculate trips. This adds distance-based reimbursement with distinct entitlement, tax-free limit and taxable excess.

**Dependencies:** NEXT-33. **Integrate after:** APP-SLICE-READY(payroll-foundation).

**Conditional gates:** NEXT-20: the selected entitlement includes taxable compensation; NEXT-21: payout/reporting uses payroll.

**Evidence:** R03, R10 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Inputs and release contract

```text
TripRevision {
  id, claimantId, businessPurpose, departure/arrival local dates,
  routeEvidence, origin, destination, distanceInMeters,
  vehicleIdentity, ownershipKind, fuelPaymentFacts,
  passengersOrOtherRelevantFacts, recordClass, previousRevision
}
MileageRuleRelease {
  applicability, distanceUnit, entitlementRule,
  exemptionRule, taxableExcessRule, roundingPolicy,
  requiredVehicleAndPayerFacts, evidenceSourceHash
}
TripAward immutable {
  tripRevision, ruleRelease, distanceWitness,
  entitlement, exemptionCeiling, exemptPaidPart, taxablePart,
  qualifiedTaxComponents, payoutRoute, receipt
}
```

Distance is an exact unit-bearing value. A displayed kilometre is not a Swedish mile, and decimals are not silently truncated. Route estimates are suggestions until reviewed. Use a selected legal/employment entitlement and a separately selected tax exemption profile; neither is inferred from the other.

## Pure calculation

```text
calculateMileage(trip, facts, release):
  require trip dates, business purpose, distance and required vehicle facts established
  require no duplicate or overlapping same economic trip claim
  require release supports this claimant/vehicle/payer/date combination
  distance = exactRational(trip.distanceInMeters, metersPerReleaseUnit)
  entitlement = round(distance * release.entitlementRate, entitlementRounding)
  ceiling = round(distance * release.taxExemptRate, taxRounding)
  exemptPaidPart = min(entitlement, ceiling)
  taxablePart = entitlement-exemptPaidPart
  require entitlement>=0 and exemptPaidPart+taxablePart==entitlement
  return all inputs, exact intermediates and outputs
```

The simple min formula applies only to a qualified profile whose exemption is a per-distance ceiling. Other car/fuel/benefit arrangements must supply a different explicit supported profile or refuse. Rates below are synthetic test inputs, not statutory rates.

## Financial handoff

```text
prepareTripAward(input):
  capture trip revision, prior awards, payroll/claim capacity and rule witness
  compute split; require current reviewed route
  if taxablePart>0: require the corresponding payroll profile exists
  seal exempt component and taxable component as disjoint source identities

executeTripAward(plan): FinancialTx
  append award and exclusive handoff manifest
  exempt part:
    record reimbursable employee liability/cost through NEXT-33's owner
  taxable part:
    debit qualified taxable-travel compensation expense
    credit accrued taxable-award liability
    create one payroll instruction referencing that EXISTING entitlement liability
    payroll later consumes the liability instead of expensing the award again
    no direct-payment route exists for this component
  append receipt and preparation outbox
```

The first supported accrual profile recognizes the taxable entitlement at award time. Payroll remains the sole owner of withholding, employer contributions and paid reporting for that component. Its gross-pay calculation includes the taxable amount while its journal debits the existing award liability, not wage expense again. A different recognition policy would require a separately qualified profile, not a caller flag.

A mileage award does not generate deductible invoice VAT merely from its tax-free status. Separate actual parking/toll receipts use purchase/claim rules with separate source identities. Do not add them to distance or reimburse them twice.

## Correction, payouts and controls

Revising distance after approval does not edit the award. Before handoff is consumed, prepare an exact replacing award. After payment or payroll reporting, produce a delta with an owned employee/payroll correction and the original trip reference. An overclaim does not become an unexplained negative net salary. Require the relevant lawful recovery/offset basis.

A trip can be paid through a bank payable or payroll, never both. Retain each attempted handoff and cancellation evidence. Claim totals reconcile to exempt liability plus taxable payroll instructions; settled instructions then reconcile to actual payment evidence.

## UI and vectors

Show unit, route, distance evidence, vehicle facts, entitlement, exempt part, taxable part and the selected payroll/direct route before approval. A missing vehicle fact blocks calculation but not trip capture.

```text
synthetic distance15000m, unit1000m, entitlement300 minor/unit,
exempt ceiling250 minor/unit -> entitlement4500, exempt3750, taxable750
same trip under second key -> no second award
missing fuel-payer fact required by profile -> incomplete, not private-car default
trip changed after pay-run approval -> old award retained + correction case
direct-payout selection with taxable component but no payroll owner -> refuse
```

The packet is complete only with the selected payroll/claim handoff and its controls. A mileage total displayed without downstream exclusive ownership is not the delivered workflow.


---

<a id="part-12"></a>

# NEXT-35: Variable pay, absence and holiday-liability reconciliation

**Priority:** P2. **Owner lane:** PAYROLL. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing payroll employment/work facts and frozen regular-pay calculator. Add one explicitly selected variable/hourly/absence profile and a holiday-liability rollforward.

**New scope, not repeated work:** Extend the first wave beyond fixed salary. Do not replace its tax-table selection, employee directory or pay-run posting authority.

**Dependencies:** NEXT-20. **Integrate after:** NEXT-21.

**Evidence:** R10, P20, P21 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Precisely bounded inputs

```text
WorkSegment {
  employee, startInstant, endInstant, localScheduleDate,
  kind: worked | overtime | paid_absence | unpaid_absence | sick,
  contractRevision, sourceTimesheetOrDecision
}
VariableEarning {sourceIdentity, units, rate, entitlementDate, intendedPayRun}
HolidayOpening {employee, entitlementUnits, moneyLiability, socialProvision, evidence}
HolidayMovement {
  kind: earned | used | expired_if_qualified | paid_out | corrected,
  units, valuationBasis, sourceIdentity, recordedAt
}
```

The scope is one reviewed employment/agreement regime at a time. Irregular schedules are explicit input. Do not assume 40 hours/week, five working days or a salary/30 deduction. Collective-agreement, sick-pay, waiting-deduction and holiday formulas are dated qualified data/code from the selected release, not embedded guesses.

## Normalize the actual work timeline

```text
normalizeWork(inputs, contractCalendar):
  convert instants to actual contract timezone and local work segments
  split at contract/rate/date and schedule boundaries
  reject duplicate source components and impossible negative intervals
  reject overlapping mutually exclusive worked/unpaid-absence segments
  require each scheduled interval accounted for or explicitly unresolved
  calculate exact worked, overtime and absence units by qualified calendar rules
```

Use paid hours or contractual unit meanings, not clock duration blindly. DST can produce a difference between elapsed and contractual time. If the supported profile cannot resolve that case, retain it for review.

## Calculate additional components

```text
calculateVariablePay(basis):
  work = normalizeWork(...)
  components = []
  for segment:
    formula = qualifiedRelease.select(segment.kind, employmentFacts, dates)
    require exactly one applicable formula and required facts
    components += formula.evaluateExact(segment, earningsBasis)
  components += explicit separately sourced bonus/commission amounts
  verify no earning or absence source is consumed by another active run
  pass component bases to existing NEXT-20 withholding/contribution calculator
```

The component classifier explicitly determines cash, taxable benefit, withholding base, employer-contribution base and holiday-accrual base. One amount may participate in several calculation bases without becoming several expenses. Reject unsupported treatment rather than classify every benefit as cash pay.

## Holiday liability as an owned rollforward

```text
holidayTarget(employee, cutoff):
  units = reviewedOpeningUnits + earned - used - qualifiedExpiredOrPaidOut
  value = qualifiedValuation(units, retainedRateAndEarningBasis, cutoff)
  socialTarget = qualifiedContributionProvision(value, applicableFacts)
  return {units, value, socialTarget}

compileHolidayAdjustment(currentControl, target):
  moneyDelta = target.value-currentEffectiveMoneyLiability
  socialDelta = target.socialTarget-currentEffectiveSocialProvision
  debit holiday accrual expense moneyDelta
  credit holiday liability moneyDelta
  debit social accrual expense socialDelta
  credit social provision liability socialDelta
```

Negative deltas reverse the relevant accrual effects, not paid wages. During holiday pay H, the payroll compiler debits the existing holiday liability to the eligible accrued extent and expenses only the unprovided remainder. For actual contribution S and released provision SP, it debits provision SP, posts expense delta S-SP and credits payroll contribution liability S. It does not expense the same holiday cost or contribution twice. All released provision capacities are explicit and current.

## Commit, correction and interface

Pay-run execution binds the frozen normalized work, component outputs, monthly cumulative tax/contribution basis and holiday effects. Internal payroll and holiday writers share the same tx. All employee rows in an approved run are either committed as its supported aggregate or none are.

A time correction after approval creates a new run revision. After payment, NEXT-36 owns the financial/reporting delta. Old timesheets, payslips and declaration inputs remain reconstructable.

Expose component explanations and holiday opening/earned/used/closing balances in payroll-only UI. Salary privacy is not weakened for general report views. Reconcile holiday-related GL controls independently of the cash payroll register.

```text
synthetic 75/2 hours *2000 minor/hour -> cash earning75000
overlap: same hour both worked and unpaid_absence -> conflict, no calculation
holiday opening10000 + earned2000 - consumed3000 -> target9000
prior posted holiday liability10000 -> adjustment-1000, not new9000 credit
holiday paid3000 already accrued -> release liability3000, do not expense3000 again
```

These vectors prove mechanics only. Support for a real sick-pay or holiday regime requires its exact reviewed formulas and agreement inputs.


---

<a id="part-13"></a>

# NEXT-36: Paid payroll recovery and retroactive compensation

**Priority:** P1. **Owner lane:** PAYROLL. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing pay-run, employee payable, reporting identity and payment evidence owners. Add consumed-history adjustment records without rewriting paid runs.

**New scope, not repeated work:** NEXT-21 only specifies bounded unpaid-run correction. This packet distinguishes later compensation, future-pay adjustment and a gross repayment claim after actual payment.

**Dependencies:** NEXT-21. **Integrate after:** APP-SLICE-READY(payroll).

**Conditional gates:** NEXT-35: the correction includes variable, absence or holiday components.

**Evidence:** R10, P21, X04 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Choose an explicit correction kind

```text
PaidPayrollAdjustment =
    AdditionalCompensation {earningPeriods, plannedPaymentDate, deltaInputs}
  | FuturePayAdjustment {originalPayRefs, lawfulOffsetBasis, futureRun, grossDelta}
  | GrossRecoveryClaim {originalPayRefs, enforceableClaimEvidence, amount}
  | ReportingOnlyCorrection {originalItemIdentity, correctedFacts, evidence}
```

A future-pay adjustment and a gross repayment claim are not interchangeable. Skatteverket distinguishes them, generally retains previously reported withholding and requires the original specification identity for replacement reporting. A gross recovery reporting correction can be made when the amount is claimed, without waiting for cash repayment [X04]. Apply the exact qualified case rather than infer one from a negative amount.

## Retained model

```text
AdjustmentPlan immutable {
  kind, employee, originalRunRevisions, paidEvidence,
  originalDeclarationItemIds, actualClaimOrPaymentDates,
  recomputedSupportedComponents, financialDeltaVector,
  reportingActions, capacityClaims, applicabilityWitness
}
RecoveryReceivableEffect {claimId, originalPaidComponent, grossClaimed, recovered, journalRefs}
ReportingAction {originalStableItemIdentity, targetValues, priorFiledArtifact, reason}
```

A correction references original immutable payslips, actual payments and filed snapshots. It cannot relabel their dates or erase the withholding already credited to the employee.

## Compute the selected branch

```text
compileAdjustment(basis, decision):
  require exact original and current facts, payment/reporting coverage and lawful case
  if AdditionalCompensation:
      recompute only additional entitlement using qualified original/current rules
      create a new earning instruction for actual future payment/reporting basis
      no reversal of original cash or original reporting item merely due to earned date

  if FuturePayAdjustment:
      require qualified right to adjust and sufficient supported future earnings
      record negative earning component consumed ONCE by future run
      future run calculates withholding/contributions on its qualified current basis
      leave original reporting unchanged under this selected case
      do not also create a gross-recovery receivable
      if result would be unsupported negative pay: refuse and select another reviewed case

  if GrossRecoveryClaim:
      G = evidenced gross amount legally claimed
      require G <= unclaimed eligible original compensation
      debit employee recovery receivable G
      credit original wage-cost role G
      preserve original withholding values and cash payment
      reporting action targets reduced original compensation with SAME item identity
      calculate contribution correction separately
      pending authority reassessment is not a posted skattekonto refund

  if ReportingOnlyCorrection:
      prove ledger/pay facts already correct and which declaration facts differ
      produce reporting revision only, no automatic wage/cash journal
```

Where the accounting profile allows recognition of an employer-contribution recovery before authority assessment, use an explicit pending-reassessment receivable and qualified expense reversal. Otherwise retain the expected adjustment as pending. In either case, an actual tax-account adjustment is posted only from its own evidenced assessment event. Do not manufacture a skattekonto balance from filing a replacement.

## Commit and actual repayment

`executePaidPayrollAdjustment` locks the affected employee, original paid-component capacities and reporting identities under the shared book protocol. It replays first, verifies authority and exact basis, then commits all supported financial effects, employee claim/instruction, reporting preparation links and one receipt. It never sends a replacement AGI inside that transaction.

```text
recordRecoveryCash(claim, cashReceipt):
  require actual received amount <= remaining gross receivable
  debit bank amount
  credit employee recovery receivable amount
  append claim allocation; create no further wage/tax correction
```

Future-pay instructions are reserved and consumed by exactly one pay run. Cancelling a prepared run can release an unexecuted instruction, but not undo a paid one. Correcting a recovery claim after repayment needs its complete employee/cash/reporting consequence; otherwise refuse with an impact list.

## Presentation and proof

Show original earnings/payment/withholding, adjustment reason, employee debt or future delta, filed replacement target and actual authority outcome separately. A submitted correction is not an accepted reassessment. Old payslips remain downloadable; a correction notice links to them.

```text
gross recovery20000, prior withholding unchanged -> employee receivable20000,
    wage expense credit20000; original bank/withholding delta0
employee repays5000 -> remaining receivable15000; wage expense delta0
future gross adjustment6000 -> next run earning reduction6000,
    no simultaneous20000-style recovery receivable
same claim/component under new key -> no second recovery entitlement
replacement AGI uses new specification number -> refuse accidental duplicate identity
```

The selected financial dates and recovery rights must be reviewed. This packet does not grant a general right to deduct arbitrary amounts from salary or lower reported withholding.


---

<a id="part-14"></a>

# NEXT-37: VAT assessment ownership and exact-to-assessed bridge

**Priority:** P0. **Owner lane:** TAX. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing VAT obligations, released reclassification/amendment effects and tax-account statement/match owners.

**New scope, not repeated work:** Add the evidenced authority-assessment lifecycle. Do not reimplement or requalify the reserved reclassification or target-minus-prior amendment operations.

**Dependencies:** NEXT-04. **Integrate after:** WIP-VAT03, WIP-VAT04-A1, APP-SLICE-READY(tax-account).

**Evidence:** R10, R11, P04 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Three amounts and one reporting obligation

```text
VatObligationState {
  obligationId, effectiveReturnRevision,
  N: exact accounting net in minor units,
  R: declared net represented in minor units,
  effectiveReclassificationRefs, effectiveAmendmentRefs
}
VatRoundingBridge immutable {
  obligationId, returnRevision, exactNet, reportedNet,
  bridgeDelta, roundingRelease, journalRefs, receipt
}
AuthorityAssessment immutable {
  providerAssessmentIdentity, obligationId, authorityPeriod,
  signedChargeMinor, sourceTaxAccountEvent, replacesOrAdjusts?, evidence
}
AssessmentEffect immutable {
  assessmentIdentity UNIQUE, linkedTaxMatchOrNewPosting,
  settlementControlVector, taxAccountVector, receipt
}
```

Use positive amounts for an assessed tax charge and negative for a credit/refund entitlement. Cash arriving at a bank is still a separate event. A generic tax-charge classification or equal amount does not prove which VAT obligation an event assesses.

## Separate legitimate filing precision from disagreement

For a complete current reclassification target, the settlement control contribution is `-N` in debit-positive notation. If the qualified filing rule legitimately reports `R`, a separate bridge can change that to `-R`.

```text
compileRoundingBridge(obligation, release):
  require exact and reported values derived by this qualified return rule
  targetBridge = N-R
  delta = targetBridge - effectivePriorBridgeEffectsForSameObligation
  require every component of delta explained by retained rounding lineage
  addSigned VAT settlement control +delta
  addSigned designated rounding gain/loss role -delta
  preserve original reclassification/amendment receipts
```

Use the proper debit/credit gain or loss role for the sign. Never use a tolerance such as “less than 100 means rounding” without the qualified formula. An actual assessment `A` different from `R` remains an assessment discrepancy, pending amendment or separate evidenced authority decision. It is not automatically included in this bridge.

## Assessment capture and financial effect

```text
prepareAssessment(sourceEvent, obligationRelation):
  require original retained tax-account event and independent authority identity
  confirm registered period, legal entity and exact charge/credit relationship
  require same assessed identity not already financially represented
  determine whether event has a compatible existing journal + owned tax-account match
  if already posted:
      require exact settlement/tax-account role vectors and unused assessment relationship
      mode = adopt_existing_effect
  else:
      mode = new_assessment_posting
  retain amount difference to expected remaining assessed amount as explained/pending
  seal exact source, prior assessments and role relationship

executeAssessment(plan): FinancialTx
  replay and recheck obligation/source/outcome memberships
  if new_assessment_posting:
      addSigned VAT settlement control +A
      addSigned tax-account control -A
      post journal and call the existing tax-account match owner in this same tx
  else:
      reference the existing owned match/entry; do not reserve its line again
  append assessment effect and once-only identity; save receipt
```

If the match owner has no released internal tx port, do not approximate atomicity with two public calls. Request that exact integration port. Old manual journals can be adopted only through explicit reviewed role evidence, never equal-amount inference.

## Later reassessment and payment

A corrected authority decision is a new source event or a proven delta under the provider's contract. Never overwrite the old assessment. Tie it to the same obligation and leave previous return/bridge/assessment revisions readable. The VAT amendment owner calculates reclassification changes; this owner posts only assessment changes and qualified precision bridges.

```text
expected VAT settlement control =
    all owned reclassification and amendment vectors
    + all qualified rounding bridge vectors
    + all signed assessment vectors
```

A residual can be legitimate while assessment is pending. It is not “reconciled and paid” merely because a bank deposit equals the declared VAT. A payment to the tax account posts between bank and tax-account control without this packet reallocating it to a particular tax.

## UI and vectors

Show exact net, reported net, assessed events, rounding witnesses and pending differences. A zero return may have a no-effect assessment relationship, but no zero journal is manufactured.

```text
N12349 R12300 -> bridge debit settlement49 / credit rounding49
assessment A12300 -> debit settlement12300 / credit tax account12300
combined settlement control: -12349+49+12300 == 0
N=-12349 R=-12300 -> bridge -49; assessment -12300; net control0
A differs from R by500 -> visible discrepancy, never rounding plug500
existing posted assessment matched already -> adoption journal delta0
same assessment under a different command key -> AlreadyApplied
```

Financial design follows the adopted separation [R11]. Exact filing precision and authority proof remain qualified external inputs. This new owner must not take over either active VAT packet.


---

<a id="part-15"></a>

# NEXT-38: Cash-method recognition and unpaid year-end cutover

**Priority:** P0. **Owner lane:** TAX. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Commerce invoice/open-item and tax-fact owners, with a cash-method profile beside the existing accrual profile.

**New scope, not repeated work:** NEXT-03/04 start with accrual. Add paid recognition and once-only year-end unpaid recognition, not another invoice or VAT ledger.

**Dependencies:** NEXT-03, NEXT-04. **Integrate after:** APP-SLICE-READY(commerce/register).

**Conditional gates:** NEXT-23: the reviewed unpaid population is consumed by financial year-end.

**Evidence:** R09, R10, X03 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Keep commercial balance separate from recognition

Start with qualified domestic same-currency invoices and explicitly supported ordinary tax treatments. Do not infer cash-method eligibility from company size or switch the book by relabeling existing accrual effects. Method changes need a separately reviewed cutover.

```text
CashMethodInvoice {
  originalGross, originalLineComponents, commercialIssueOrAcceptance,
  paidAllocations, creditRelationships, profileWitness
}
RecognitionSlice immutable {
  invoiceId, sourceLineId, componentCoverage,
  trigger: actual_payment | unpaid_year_end,
  grossCoverage, netExpenseOrRevenue, taxComponents,
  journalRefs, taxPeriod, economicIdentity
}
RecognizedOpenPosition {
  recognitionSliceId, initialGross, laterSettlements, remainingGross
}
```

Per source line, disjoint recognized coverage prevents paid and year-end paths from recognizing the same portion. A receipt number or invoice issue is not itself the cash-method recognition trigger. Retain unrecognized commercial debt visibly.

## Partial payment compiler

```text
prepareCashMethodPayment(invoice, explicitLineAllocations, cashEvidence):
  require actual final cash event with supported timing and no duplicate source use
  for selected line in frozen original order:
    p = gross amount paid against this line
    s = min(p, existing recognized-unpaid coverage allocated by approved policy)
    r = p-s
    require r <= this line's unrecognized outstanding coverage
    if purchase:
        debit payable control s
        recognize remaining r as expense + deductible tax under original treatment
        credit bank p
    if sale:
        debit bank p
        credit receivable control s
        recognize remaining r as revenue + output tax
    publish tax facts ONLY for newly recognized r
    consume recognized position s and claim new recognized coverage r
```

Split source-line net/tax components by cumulative exact gross coverage using the qualified rounding rule; final consumption releases exact residuals. The operator-selected line allocations sum to the cash principal. Fees are separate sources/effects. Do not round each partial payment as an unrelated invoice.

All cash, recognition, tax facts, commercial settlement and source rights commit in one named application transaction. When a compatible cash posting already exists, adopt its clearing-side capacity and create no duplicate bank entry.

## Year-end population

```text
prepareCashMethodYearEnd(year, cutoff):
  capture complete eligible issued/received unpaid invoice population
  pin registration/method, fiscal interval, source coverage and membership epoch
  for every original line:
    u = commercial unpaid coverage not already recognized
    derive exact remaining cost/revenue and tax components for u
    purchase: debit cost/input VAT; credit payable u
    sale: debit receivable u; credit revenue/output VAT
    append recognition slices(trigger=unpaid_year_end)
  seal entire supported group and unresolved exclusions
```

Skatteverket describes unpaid invoices as recognized at year-end under cash bookkeeping; later payment must not repeat their VAT [X03]. The exact legal dates and special cases must be supplied by the qualified profile. The app must not call an incomplete selected page a complete year-end population.

```text
executeYearEndRecognition(plan): FinancialTx
  recheck membership and every outstanding/recognized capacity
  reject new relevant invoices/payments or changed treatment
  post aggregate and tax facts; create recognized open positions
  save complete membership receipt, including valid no-effect items
```

Payment in the next year then consumes those positions. It posts bank versus AP/AR only for the previously recognized amount. It does not create new revenue, expense or tax facts.

## Credits and correction boundary

An unpaid credit consumes explicitly linked source-line coverage. If that portion was unrecognized, revise the commercial residual with no reversal of nonexistent accounting. If it was recognized at year-end, create the exact recognized credit/tax correction under the applicable credit-date rule. Do not subtract both the original tax fact and another negative fact. Paid-principal credits route to the qualified customer/supplier refund extension; until cash-method reporting there is qualified, refuse that branch explicitly.

A backdated payment or newly discovered prior-year invoice invalidates the relevant year-end assessment. Preserve the old receipt and create the required owned amendment/closing impact, not silently undo year-end recognition.

## Controls and vectors

```text
original gross125000 = net100000 + VAT25000
first payment50000 -> net recognition40000, VAT10000
year-end unpaid75000 -> net60000, VAT15000, AP/AR75000
next-year payment75000 -> only AP/AR settlement, VAT delta0
payment and year-end compete for same coverage -> one wins; other stale/recomputes
invoice recorded but no payment and before year-end -> commercial debt, GL recognition0
```

Reports distinguish all commercial outstanding from the recognized GL-controlled portion. Unknown or unsupported invoices block complete year-end readiness, not source retention or independent supported work.


---

<a id="part-16"></a>

# NEXT-39: Processor balance and payout clearing, Stripe first

**Priority:** P1. **Owner lane:** TREASURY. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Source retention, customer settlement/refund owners and bank reconciliation. Add a selected Stripe balance-transaction adapter and processor control ledger projection.

**New scope, not repeated work:** Plaid packets cover bank feeds and webshop WIP covers orders. Neither specifies processor gross/fees/refunds/payout clearing. This packet owns that financial reconciliation, not sales-order intake.

**Dependencies:** NEXT-30. **Integrate after:** APP-SLICE-READY(source-intake), APP-SLICE-READY(commerce/register).

**Conditional gates:** NEXT-40: processor balances use a non-book currency; WIP-COM2-W1: read-only order provenance is required; do not modify its intake.

**Evidence:** R03, R09, X01, X02 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Identity and exact source interpretation

```text
ProcessorObservation {
  accountId, liveOrTestMode, balanceTransactionId,
  rawSourceRef, providerSourceId, type, reportingCategory,
  currency, grossMinor, feeMinor, netMinor, availableOn, recordedAt
}
ProcessorEffect {observationIdentity UNIQUE, ownedFinancialKind, journalRefs, settlementRefs}
PayoutMovement {providerPayoutId, debitBalanceTransaction, transitRole, bankSettlementRefs}
```

Stripe exposes exact integer gross, fee and net fields with `net=amount-fee`. Its payout filter is documented for automatic payouts only [X01/X02]. Keep account, mode and currency in identity. Do not silently use a test-account object or another connected account's record.

Retain fetched pages/raw bytes and normalize through a pinned provider profile. Webhooks can trigger fetch/reconciliation but arrival order does not establish accounting order. Capture a fixed retrieval interval, deduplicate exact provider IDs and compare to independent processor balance/report controls. A list ending is not proof of all historical activity.

## Classify explicitly, never net payouts as revenue

```text
compileProcessorObservation(o, economicLinks):
  require gross-fee==net and exact supported currency/scale
  if charge/payment:
    require recognized sale or authorized customer obligation relationship
    debit processor control net
    debit qualified processor fee cost fee
    credit customer AR gross
    allocate AR principal; create NO new sale/VAT

  if refund:
    require original refund/credit liability and its remaining capacity
    R = -gross; require R>=0
    debit customer-credit liability R
    debit qualified refund fee cost fee
    credit processor control R+fee
    consume customer refund capacity; create NO second credit-note tax fact

  if payout:
    P = -net; require ordinary supported payout and reconciled gross/fee shape
    debit payout-in-transit P
    credit processor control P

  if supported fee-only:
    debit qualified fee cost(-net)
    credit processor control(-net)

  otherwise:
    return RequiresClassification(originalObservation, preciseUnsupportedType)
```

Fee tax, refunded fees and cross-currency conversions require explicitly supported variants. A missing supplier fee invoice may permit gross-cost posting only under a qualified policy, not an invented input-VAT deduction. Missing sale recognition produces a link/review prerequisite, not fabricated revenue from the payout.

## Disputes, reversals and cash

A dispute debit is not necessarily a credit note or bad debt. For a supported recoverable hold, debit a dispute receivable and credit processor control with separate fee treatment. If won, clear the receivable against the processor credit. If lost, a reviewed decision reclassifies the receivable to the appropriate loss; VAT treatment remains a separate qualified decision. An unsupported reserve/Connect/capital transaction remains visible and blocks complete control reconciliation.

```text
recordBankPayoutReceipt(payout, bankObservation):
  require exact provider/bank relationship, currency and current transit capacity
  debit bank amount; credit payout-in-transit amount
  or adopt existing compatible cash/clearing posting
  append settlement; do not create revenue/expense again
```

A payout failure reverses its transfer to transit only if evidence proves the original cash did not settle. If funds reached the bank and later returned, retain both real cash events instead. Never use a status flag to erase cash.

## Atomic effects and independent controls

Each supported balance transaction commits its journal, customer settlement/refund or transit effect and once-only source identity together. Aggregating a complete payout can use a fixed manifest of these identities; no second accounting pass posts their totals again. Same source fetched through both balance API and payout API resolves to one effect.

```text
processor closing = reviewed opening + sum(all supported net balance effects)
payout transit closing = payouts moved out - actual bank receipts - supported failures
```

Compare both with independent provider/bank evidence. Availability date can partition pending/available states without being another principal posting. Manual payouts reconcile from the full ledger/balance history, not an unsupported automatic-payout membership assumption.

```text
charge125000 fee3000 -> processor122000 + fee3000 - AR125000
payout122000 -> transit122000 - processor122000
bank receives122000 -> bank122000 - transit122000; revenue delta0 throughout
same txn read under payout and balance list -> one journal effect
unknown reserve debit -> visible unclassified difference, not silently omitted
```

Initial implementation requires an authorized Stripe read configuration and reconciliation fixture. It does not claim all gateways, Connect modes or merchant-of-record arrangements are supported.


---

<a id="part-17"></a>

# NEXT-40: Foreign-currency cash holdings and transfers

**Priority:** P1. **Owner lane:** TREASURY. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Bank/processor cash account owner with existing FX pure arithmetic and commerce obligation settlement.

**New scope, not repeated work:** First-wave FX owns receivables/payables. Add native-currency CASH balances and their book carrying values, not a duplicate invoice FX register.

**Dependencies:** NEXT-17, NEXT-18. **Integrate after:** WIP-FX02-P1, APP-SLICE-READY(banking).

**Evidence:** R09, R10, R11, P17, P18 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Cash representation

```text
ForeignCashAccount {
  sourceAccountId, book, nativeCurrency, nativeScale, bookCurrency,
  cashControlAccount, reviewedOpeningNative, reviewedOpeningCarrying, valuationPolicy
}
CashHoldingEffect immutable {
  sourceIdentity, nativeDelta, carryingDelta,
  kind: deposit | withdrawal | internal_transfer | exchange | valuation | correction,
  actualNativeDate, rateOrSettlementWitness, journalRefs
}
CashHoldingState = fold(reviewed opening + effective effects)
```

The initial profile permits nonnegative balances only. An overdraft changes liability and valuation semantics and requires another qualified profile. A SEK-denominated bank account receiving a foreign invoice payment is not a foreign-cash account merely because its source invoice used EUR.

## Capture and release

```text
captureCashBasis(account, cutoff):
  retrieve complete native and book movements at accounting/recorded cutoff
  Q = remaining native units; B = book carrying value
  require Q>=0 and B>=0
  if Q==0: require B==0
  return {Q,B,capacityVersion,valuationBoundary,sourceCoverage}

planCashWithdrawal(basis, q):
  require 0<q<=Q and policy permits the selected weighted carrying release
  use the shared exact paired-release pure calculation with this CASH basis
  b = B when q==Q, otherwise selected exact proportional release
  return {nativeConsumed:q, carryingReleased:b, witness}
```

The pure arithmetic can be reused from the FX owner. Cash mutation remains owned here; do not call a commerce-obligation mutation with a cash account ID or copy an invoice's remaining balance. Repeated reads of each selected account are batched.

## Settlement using foreign cash

For an already recognized same-native-currency payable, capture both independent capacities. Let `bP` be the payable carrying release and `bC` the cash holding release.

```text
compilePayableFromForeignCash(q):
  payableRelease = existing FxDomain release(payableBasis,q)
  cashRelease = planCashWithdrawal(cashBasis,q)
  debit payable control bP
  credit foreign-cash control bC
  gain = bP-bC
  credit gain if positive; debit loss if negative
  apply both native/carrying consumptions in ONE tx with same journal references
```

An incoming receivable settlement similarly increases cash at the qualified receipt-date book value `K`, releases AR carrying `bR` and recognizes gain `K-bR`. Subsequent cash valuation is a different holding effect. A payment already posted to a qualified foreign-cash clearing account is adopted without another cash movement.

## Transfers, exchanges and valuation

Same-currency transfer between two owned foreign accounts consumes native units/carrying from the sender and adds exactly the same pair to the receiver, absent separately evidenced fees. There is no economic gain from moving identical owned currency between accounts under that profile.

```text
exchangeForeignForBookCash(source,q,actualBookReceipt K,fee F):
  b = released foreign carrying
  debit book-currency cash K-F
  debit qualified fee cost F
  credit foreign-cash control b
  credit realized gain K-b or debit corresponding loss
```

Foreign-to-foreign exchange requires both native quantities and a qualified transaction-date book consideration. It cannot be inferred by independently rounded current quotes. Initial implementation may refuse that branch while delivering foreign-to-book exchange correctly.

For reporting-date valuation, compute target carrying from native units and the qualified reporting rate, then post only target minus current carrying. Native units remain unchanged. No automatic next-period reversal. Late valuation after a later cash withdrawal is a consumed-history case for NEXT-41, not a blind rewrite.

## Transactions, controls and vectors

Every journal plus sender/receiver/obligation effect commits on one supplied tx. Source cash identity is once-only across bank import, processor intake and native cash operations. Reconciliation compares native statement balance to native holding and book-currency GL to carrying independently. A zero SEK difference cannot explain missing native units.

```text
cash Q10000 EUR-minor, B110000 SEK-minor; withdraw q4000 -> b44000
payable same q releases45000 -> AP+45000, cash-44000, gain-1000
remaining cash Q6000/B66000; reporting target69000 -> cash+3000/gain-3000
same-currency internal transfer q1000,b11500 -> sender/receiver net book effect0
withdraw all -> consume all remaining carrying, no residual öre
```

UI displays native balance, book carrying, selected valuation and independent reconciliation. Summing currencies into one native total is prohibited; consolidated book values identify their valuation cutoff.


---

<a id="part-18"></a>

# NEXT-41: Late FX valuation and consumed-chain correction

**Priority:** P1. **Owner lane:** TREASURY. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** The existing commerce monetary-item and FX correction owner. Add a bounded chain-adjustment operation using its own balances and recorded events.

**New scope, not repeated work:** NEXT-18 refuses late revaluation after settlement consumed the old basis. Solve that explicit limitation with a complete approved delta, not reversal of real cash or another writable FX register.

**Dependencies:** NEXT-18. **Integrate after:** WIP-FX02-P1, APP-SLICE-READY(commerce-fx).

**Conditional gates:** NEXT-40: the affected chain includes native foreign-cash holdings; NEXT-23: affected financial periods require approved reopening.

**Evidence:** R10, R11, P18 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Scope and immutable repair plan

Initially support one monetary item with known recognition, deterministic partial/full settlements and reporting-rate valuations. Mixed credits, netting, foreign-cash links or cross-item allocation chains require their explicit supported replay handlers. If one affected event lacks a handler, return its identity as a blocker before any journal is prepared.

```text
FxChainBasis {
  itemId, anchorBeforeChangedCutoff, originalEconomicEvents,
  priorEffectiveCarryingAdjustments, activeChainRevision,
  relatedCash/feeIdentities, valuationRateVersions,
  selectedAccountingDates, recordedCutoff, closureDigest
}
FxChainRepair {
  inputChange, orderedClosure,
  revisedPerEventCarrying, deltaByAccountingDateAndRole,
  originalCurrencyDelta: 0, cashSourceDelta: 0,
  resultingBalances, downstreamImpactRefs, approvalDigest
}
```

A late rate decision does not change how many foreign units were paid, the actual cash consideration or the original fee evidence. Event ordering is the qualified economic chronology with explicit tie-breaking, not arrival-time sort. Ambiguous chronology blocks repair.

## Replay the financial meaning over frozen facts

```text
calculateChainRepair(basis, correctedRate):
  events = all dependent events through the current endpoint, not just the next payment
  require complete closure and bounded size
  state = independently reconstructed anchor {foreignRemaining, bookCarrying}
  desired = []
  for event in chronological order with inserted/replaced valuation decision:
    if valuation:
      T = exact native remaining * selected reporting rate under policy
      append target carrying adjustment T-state.B and its direction-specific P&L
      state.B = T
    if settlement:
      b = existing FxDomain exact paired release(state, event.originalUnits)
      gain = event.K-b for AR; b-event.K for AP
      append desired control release and realized P&L, preserving K and fees
      state.Q -= event.originalUnits; state.B -= b
    if other event:
      call its explicitly supported pure replay rule or refuse
  oldEffective = original owned vectors + all previous repair deltas
  delta = desired - oldEffective, grouped by economic accounting date and role
  require delta contains NO change to real cash quantities or fee/source principal
  require final original-unit balance unchanged
  require reconstructed final carrying equals planned current owner balance
  return full witness and delta, not replacement of old source records
```

The posted correction can include several dated vouchers in one approved book-scoped aggregate. Each date must be eligible under the selected correction policy. Closed periods require approved reopening or a separately qualified prior-period adjustment policy. Do not move an old-year tax/result effect into today's date for convenience.

## Atomic application of a new effective chain

```text
executeFxChainRepair(plan): FinancialTx
  lock book, all affected periods and complete owned resource closure
  replay first, then verify active chain revision and closure membership
  require no intervening settlement, rate change or other consumer
  verify journal delta equals the approved old-to-desired role vector
  post all required correcting vouchers as one complete group
  append carrying deltas referencing ORIGINAL settlement/valuation effects
  advance the original item's effective-chain revision
  record downstream report/close/tax review obligations
  save one aggregate receipt and change intent
```

The current commerce projection folds original effects plus the approved deltas exactly once. It must not replace the entire register and then also apply the original effects again. Old snapshots keep their recorded cutoff and chain revision. A zero total difference across two years does not justify omitting both nonzero period corrections.

## Concrete late-year-end example

```text
AR initially110000
No old year-end valuation; January cash settlement116000
Old January realized gain6000, AR now0

Correct December target115000:
  December delta: AR +5000; valuation gain -5000
  January delta:  AR -5000; realized gain +5000

Cash delta0; foreign quantity delta0; ending AR delta0
Revised total gain remains6000 = December5000 + January1000
```

Do not reverse/repost the January cash receipt or restore original payment capacity. Those events occurred correctly; only their carrying-release and gain attribution changes.

## Read/UI/recovery requirements

Show the old and target per-event carrying path, each dated journal delta, unchanged cash/principal and every affected report/close. Approval must cover the entire closure. Report readers identify whether they show original historical knowledge or the newly corrected recorded basis.

```text
another settlement occurs after review -> whole repair stale, no partial delta
same repair key after commit -> same aggregate receipt
new key with already applied input change -> AlreadyApplied/no-effect determination
missing credit handler in chain -> explicit blocker, never skip event
December closed without authorized correction policy -> refuse before posting
```

This is a bounded domain replay calculation, not a generic event-sourcing platform. No other domain acquires authority over the FX item's balances.


---

<a id="part-19"></a>

# NEXT-42: Economic impairment reversal and zero-carrying assets

**Priority:** P1. **Owner lane:** SCHEDULES. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing asset, impairment and schedule owners after their reserved UI/control closure.

**New scope, not repeated work:** The adopted first profile requires positive remaining carrying and only a bounded immediate error correction. Add later economic reversal with a qualified cap and an explicit zero-carrying-but-owned state.

**Dependencies:** No new first-wave financial feature is a hard prerequisite. **Integrate after:** WIP-AST03-UI, APP-SLICE-READY(subledger).

**Conditional gates:** NEXT-19: checking disposal/proceeds consumers; NEXT-13: presenting the resulting financial controls.

**Evidence:** R10, R11 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Do not confuse three events

`ErrorCorrection` repairs a mistaken recorded impairment. `EconomicReversal` reflects a newly evidenced recovery under an applicable accounting rule. `Disposal` ends ownership or the selected asset recognition. They have different dates and downstream consequences.

```text
AssetValuationDecision {
  assetId, kind: further_impairment | economic_reversal,
  assessmentDate, supportedValuationEvidence, targetCarrying,
  counterfactualPolicyRelease, counterfactualBasis,
  expectedAssetVersion, expectedScheduleRevision
}
ScheduleState = active | exhausted | zero_carrying_in_use | disposed
```

No-counterfactual evidence means reversal cannot be approved. Do not compute the cap from the currently impaired depreciation schedule itself.

## Qualified counterfactual cap

```text
calculateCounterfactual(basis, rule):
  require complete original cost and eligible ordinary-depreciation history
  replay the qualified WITHOUT-IMPAIRMENT basis through assessment date
  include only estimate revisions that the policy permits in that counterfactual
  exclude impairment-caused schedule changes unless independently justified
  return carryingWithoutImpairment H and its full witness

compileEconomicReversal(basis, decision):
  B = gross - effectiveOrdinaryAccumulation - effectiveImpairment
  H = calculateCounterfactual(...)
  I = impairment contra amount eligible for reversal
  require decision.targetCarrying >= B
  maximumTarget = min(H, B+I)
  require decision.targetCarrying <= maximumTarget
  R = decision.targetCarrying-B
  debit accumulated impairment R
  credit qualified impairment-reversal income R
  future = approved new useful-life/residual allocation for target carrying
  require futureInstallments + residual == targetCarrying
  return journal + impairment delta -R + complete schedule revision
```

The target comes from reviewed economic evidence and a qualified framework profile. The formula is a design contract for an eligible depreciable asset, not a claim that every asset category or intangible permits reversal. No tax reversal is inferred from a book impairment reversal.

## Full impairment without fabricated installments

```text
compileZeroCarryingDecision(basis, supportedDecision):
  require still-owned asset and qualified complete write-down
  B = current carrying
  debit impairment loss B
  credit accumulated impairment B
  new carrying = 0; future installments = []; residual = 0
  new state = zero_carrying_in_use
```

Empty future installments are valid only under this explicit terminal-recognition state. It is not a generic relaxation of the existing active schedule's positive-installment requirement. The asset remains in inventory and control reporting. Fully depreciated/exhausted and fully impaired positions retain their different histories.

If a later economic reversal from zero is allowed, construct a new positive future schedule from approved dates and residual. Do not reuse retired occurrence keys or rerun old installments. A disposed asset cannot be revived by this operation; reacquisition is another evidenced event.

## Atomic application and correction

`executeAssetValuationChange` rechecks assessment, ordinary/impairment effects, current schedule and absence of incompatible disposal/consumption. It commits the journal, valuation event, schedule revision and retired future-authority markers together. Counterfactual computation happens before the transaction; currentness is checked inside it. Consumers for controls, depreciation, closing and disposal all use the same effective basis.

Immediate correction of this new event is allowed only while its consequences remain unconsumed and can be restored with a complete replacement schedule. Otherwise identify the affected chain and refuse unsupported standalone reversal. Never delete a schedule revision to make old plans usable.

## Controls and vectors

For gross `G`, ordinary accumulation `A`, impairment `I`, carrying is `G-A-I`. The impairment contra rollforward includes positive impairment and negative economic reversals independently from ordinary depreciation. Controls reconcile each role, not just net carrying.

```text
G1000000 A200000 I300000 -> B500000
qualified H700000, target650000 -> reversal150000, I150000, B650000
target750000 -> above cap700000, refuse
B500000 -> full impairment500000 -> B0, no future installment, still in inventory
zero-carrying asset later disposed without proceeds -> release gross and contra,
    not another500000 loss
```

The packet includes application/schema version changes for the new schedule states and every affected consumer. It cannot be accepted as a UI-only toggle or manual journal feature. Legal eligibility and counterfactual data require separate qualification.


---

<a id="part-20"></a>

# NEXT-43: Reviewed dimension restatement without editing journals

**Priority:** P1. **Owner lane:** REPORTING. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing original dimension assignments, report snapshots and contribution identities. Add classification history beside them.

**New scope, not repeated work:** NEXT-14 deliberately excludes posted retagging. Add the explicitly planned original-versus-reviewed analytical view without changing financial amounts, original tags or old exports.

**Dependencies:** NEXT-14, NEXT-13. **Integrate after:** APP-SLICE-READY(dimensions).

**Evidence:** R03, P14 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Classification history

```text
DimensionRestatementPlan {
  scope, selectedJournalLines, financialRecordedCutoff,
  originalAssignmentDigest, currentClassificationHeads,
  desiredAssignmentsByLine, effectiveAccountingScope,
  policyRelease, reason, evidence, digest
}
ClassificationRevision immutable {
  lineId, originalFinancialDigest, fullReviewedAssignmentSet,
  predecessorClassificationId?, effectiveScope, approvedPlan, recordedAt
}
ClassificationHead {book, lineId, revisionId, version}
```

A revision describes the complete reviewed assignment set for a line at its scope. Explicit removal becomes `unassigned`, not omission that accidentally inherits today's default. Unknown original history and an evidenced exemption remain distinct. The raw original line and tax/source relationships never change.

## Review and application

```text
prepareRestatement(selection, requestedChanges):
  capture complete selected line membership and current classification heads
  require no amount/account/currency/tax-point/economic-owner change in request
  resolve target dimension/value revisions and validity for chosen analytical scope
  validate required/fixed analytical policies and explicit exceptions
  require each selected line's financial digest matches retained original
  calculate before/after per-value totals and unassigned buckets
  require unfiltered signed totals unchanged
  seal exact selection, full assignments, reasons and policy witnesses

executeRestatement(plan): App transaction, no journal
  current access, book lock and exact replay
  lock classification heads in stable line order
  require original line digests and expected heads unchanged
  recheck relevant classification policy and approved target values
  append immutable revisions and advance heads
  append classification_changed event and receipt
  do not alter vouchers, original dimension tables or legal artifacts
```

The initial implementation can conservatively stale an entire line if another classification changed, rather than silently merge conflicting edits. Refining to independent dimension-level concurrency requires explicit combined-policy validation.

## Report semantics

```text
classificationAt(line, mode, classificationCutoff):
  if mode==original: return original assignments
  if mode==reviewed:
    return latest approved applicable revision recorded at/before cutoff
           or explicit original/unknown state

captureRestatedReport(selection):
  freeze ledger boundary, classification cutoff and selected revision IDs
  use those assignments throughout all pages and artifacts
  report includes mode and full classifier basis digest
```

Each financial contribution appears once in each chosen dimension partition. A cross-tab uses one tuple of assignments per contribution. Separate project and cost-center totals are two views of the same money, not additive totals. A single cost center need not balance the company balance sheet, so no balancing journal is created.

Original SIE export remains original accounting data. A separately requested analytically restated export must identify its altered classification basis and satisfy the format/recipient contract. Never silently replace the original dimension bag in the statutory/accounting archive.

## Subsequent reversal and explanation

Undoing a classification creates another reviewed revision restoring the desired assignment set. It does not delete prior history. Old saved reports retain old classification cutoffs. A new report can compare classification-only differences separately from new financial postings.

The source journal's exact reversal inherits original dimensions. Analytical reporting can optionally propagate a reviewed classification to the related reversed contribution only under an explicit linked classification decision; do not rewrite the financial correction itself to match today's analytics.

## API/UI and vectors

The bulk-review screen shows selected rows, original tags, current reviewed tags, proposed tags, total effect and missing/exempt values. Scope changes invalidate the preview rather than keeping approval for a different selection. Ordinary agents can propose and inspect; authorized humans approve the restatement.

```text
A100 + B200 + unassigned50 =350
move original A100 to reviewed B -> original report A100/B200/U50,
    reviewed report A0/B300/U50; both total350
old saved report before restatement -> unchanged
attempt to change account while retagging -> rejected as financial correction
same revision replay -> same receipt; concurrent changed head -> stale
```

This resolves the backlog's classification-storage gate with immutable overlays and fixed report bases. It does not introduce a second financial ledger or permission to alter VAT attribution via project tagging.


---

<a id="part-21"></a>

# NEXT-44: Multi-year SIE partition and dimension-preserving import

**Priority:** P1. **Owner lane:** REPORTING. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing bounded SIE parser, retained source staging, historical basis and financial run owners.

**New scope, not repeated work:** Extend the single-year/dimension-restricted import boundary. Do not rebuild byte retention, opening selection, financial admission or the historical open-item bridge.

**Dependencies:** NEXT-12, NEXT-14. **Integrate after:** APP-SLICE-READY(historical-migration).

**Conditional gates:** NEXT-11: independent roundtrip export is part of acceptance.

**Evidence:** R09, R10, P11, P12, X09 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Immutable partition model

```text
SourceYearPartition {
  sourceOccurrence, parsedRevision, sourceYearOrdinal,
  exactFiscalStart/End, accountControls, voucherMembership,
  dimensionDeclarations, sourceObjectMap, unsupportedRecords
}
ImportPlan {
  sourceHash, partitionsInChronologicalOrder,
  nativeFiscalMapping, accountMappings, dimensionMappings,
  selectedHistoryModeByYear, independentControls,
  completeMembershipDigest, exclusionDecisions
}
```

SIE source-year ordinal is not a year inferred from today's calendar. A native voucher identity includes book/fiscal year/series/number. Identical series and number in two different fiscal years are not duplicates.

## Parse and partition

```text
partitionParsedSource(parsed, reviewedFiscalMap):
  retain all records and original byte/line locators
  read explicit source #RAR intervals with real date validation
  require each mapped interval unambiguous and native fiscal boundaries agree
  for complete #VER block:
    choose the unique source year containing its accounting date
    if no match or multiple matches: blocking diagnostic
    retain final #TRANS lines separately from #RTRANS/#BTRANS history
    never add historical correction records to final transaction totals again
  attach year-indexed #IB/#UB/#RES and dimension/object balances to their own year
  retain unassigned or unsupported records visibly
```

If source line dates imply a financially unsupported cross-year voucher, do not split a balanced source voucher silently or move dates. Either the qualified format mapping preserves them as non-posting metadata or the plan refuses that block with its location.

## Dimensions and source controls

```text
resolveObjectAssignments(line, declarations, reviewedMapping):
  require each source dimension/value pair is declared or diagnosed
  map source dimension numeric ID to one stable native dimension
  map object code to reviewed native value preserving original source code
  retain explicit no-assignment, unknown and allowed historical exemptions
  reject dropped, duplicate or ambiguous assignments
```

Do not import current default dimensions onto historical lines. Unknown/unsupported dimensions must stop financial admission of affected vouchers rather than becoming an empty object list. Use NEXT-14's original assignment schema.

Missing zero control rows can be interpreted only when the exact supported format and independent source coverage establish that omission means zero. Otherwise absent remains unknown. Check each year's reviewed opening plus final financial movements against closing controls, then check the next year's balance-sheet opening relationship with explicit result-transfer/migration semantics. Never add an opening voucher on top of the same earlier history.

## Durable multi-year admission

```text
startMultiYearRun(plan):
  authorize operator; freeze complete partitions and per-year controls
  require one supported writer/cutover authority and no competing financial run
  retain current year/ordinal and domain fence

advanceYear(run, boundedChunk):
  select only the next reviewed source partition and exact source voucher membership
  prepare/approve through the existing owning financial-run flow
  execute a bounded group in one tx with source/native links and checkpoint receipt
  after all vouchers in year:
      independently compare native year closing to reviewed source controls
      require exact complete agreement or stop with retained diagnostics
      authorize the next partition's opening relationship; do not post it twice
```

Do not hold a transaction open for the entire source file. Already committed chunks remain accounting history if a later partition fails. Resume at the saved fence/checkpoint; rollback of the entire business migration requires an explicit supported correction/cutover procedure, not deleting earlier chunks.

Historical receivable/payable facts are admitted and bridged by NEXT-12 after the correct basis is established. SIE alone need not contain enough invoice-level detail to reconstruct those obligations. Missing detail stays a separate blocker, not an invented invoice.

## UI and vectors

Show source years, native year mapping, controls, object mappings, unsupported records and staged-versus-posted counts. A public exercise file parsing successfully does not establish destination or real-company migration acceptance.

```text
A/1 in source year-1 and A/1 in year0 -> two scoped voucher identities
prior UB matches next IB -> link basis once, no extra opening movement
source #TRANS100 plus historical #RTRANS-100 -> final amount remains100
dimension1='DEP-A' -> original mapped tag retained on journal/export
missing control row with unknown completeness -> unknown, not zero
failure in year2 after year1 committed -> recoverable paused run, no silent reset
```

Source-format grammar, encoding and allowed omitted records require the pinned specification [X09]. This packet does not invent support for SIE5 or all exporter-specific extensions.


---

<a id="part-22"></a>

# NEXT-45: Direct cash-flow statement with a full reconciliation bridge

**Priority:** P1. **Owner lane:** REPORTING. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing semantic report snapshots, original financial contributions and owned cash/settlement links.

**New scope, not repeated work:** NEXT-13 produces P&L and balance sheet. Add historical actual cash-flow classification and closing-cash reconciliation, not a forecast or dashboard estimate.

**Dependencies:** NEXT-13. **Integrate after:** APP-SLICE-READY(reports).

**Conditional gates:** NEXT-40: the selected cash perimeter contains foreign-currency holdings; NEXT-39: processor/transit positions belong to the selected cash perimeter.

**Evidence:** R09, R10, P13 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Report definition

```text
CashFlowPolicy {
  cashAndEquivalentPerimeter, effectiveDateBasis,
  operating/investing/financing classification rules,
  tax/interest/dividend policy, internalTransferRoles,
  exchangeEffectRules, perimeterReclassificationRules
}
CashFlowSnapshot {
  ledgerBoundary, recordedCutoff, period,
  openingCash, closingCash, originalCashContributions,
  externalFlowLeaves, internalEliminations, exchangeEffects,
  perimeterChanges, unclassifiedRows, exactReconciliation
}
```

The perimeter is reviewed, not inferred from every account whose name contains bank. Tax accounts, restricted processor reserves and transfer-in-transit positions require explicit inclusion or exclusion. A policy cannot silently change between opening and closing without a disclosed perimeter bridge.

## Trace actual cash components

```text
calculateCashFlow(basis, policy):
  cashRows = all actual posted components in the selected perimeter and cutoff
  for row:
    if owned valuation/exchange effect with no external cash flow:
        assign to exchangeEffect using exact owner witness
    else if owned internal transfer:
        locate complete counterpart relationship and its permitted interval treatment
        eliminate internal movement only to extent both sides/perimeter bridge are explained
    else:
        origin = resolve exact settlement/purchase/payroll/asset/funding relationship
        splits = qualifiedClassification(origin, row.signedCash)
        require splits sum exactly to this original cash component
        if unresolved: keep unclassified with row reference
        else emit operating/investing/financing leaves with lineage
  retain every row once across external flows, eliminations or bridge categories
```

Never infer that two equal opposite amounts are an internal transfer. They may be unrelated customer and supplier payments. Use owned transfer identities. For a mixed payment, allocate using exact invoice/asset/principal/fee relationships rather than split proportionally by account labels.

Direct cash flows use actual receipts/payments, not invoiced revenue or P&L expense. A depreciation entry is noncash. Tax and interest placement follow the chosen reporting policy. No unclassified item defaults to operating just to make the report complete.

## Closing bridge

```text
netExternal = operatingNet + investingNet + financingNet
expectedClosing = openingCash + netExternal + exchangeEffects + perimeterChanges
reconciliationDifference = actualClosing-expectedClosing
complete = noUnclassifiedRows AND noMissingInternalCounterparts
           AND difference==0 AND requiredSourceControlsComplete
```

Internal transfers inside the perimeter contribute zero. Transfers crossing a reporting date may leave a transit balance: include that balance under an explicitly qualified equivalent-cash policy or show its reconciled perimeter treatment. Do not invent an external cash flow or drop the unmatched leg while still claiming a complete bridge.

Foreign-currency cash remeasurement changes book carrying without native cash flow. An exchange between two cash holdings can create a realized carrying difference; attribute it to the exchange bridge, while genuine bank fees remain external flows. Use NEXT-40's exact witnesses instead of recomputing every cash movement at today's rate.

## Snapshot, UI and export

Capture fixed financial membership, classification release and relationship revisions. Calculate outside locks, then seal after relevant currentness checks. The resulting report pages/explanations use its saved classification, not current supplier/customer labels. A later correction creates a new snapshot and comparison.

Provide total operating/investing/financing flows, exchange and perimeter bridges, opening/closing cash and every unresolved item. One click reaches the original cash line, allocation and source. Export the same semantic rows to JSON/CSV. This is not an indirect cash-flow statement until that separate calculator exists.

## Exact vectors

```text
opening100000; customer receipts200000; supplier payments-80000;
asset purchase-50000; loan inflow40000; FX carrying gain2000
operating120000; investing-50000; financing40000; exchange2000
closing=100000+120000-50000+40000+2000=212000

transfer accountA-30000/accountB+30000 inside perimeter -> external0
unexplained +500/-500 -> difference may0 but complete=false
invoice200000 unpaid -> no cash flow200000
foreign cash valuation+2000 -> exchange bridge, not operating receipt
```

The selected statement mapping is original design over the repo's report requirements. Its presentation and statutory applicability need the appropriate company/framework release, not merely balanced arithmetic.


---

<a id="part-23"></a>

# NEXT-46: Peppol invoice and credit exchange through a selected access point

**Priority:** P1. **Owner lane:** DELIVERY. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing semantic invoice/credit models, retained artifacts, supplier intake and authorized external-delivery owner. Add a selected access-point adapter, not a Peppol network implementation.

**New scope, not repeated work:** First-wave packets issue documents and generate local reports. This adds a concrete structured e-invoice/credit format and transport boundary, with inbound review distinct from posting.

**Dependencies:** NEXT-03, NEXT-15. **Integrate after:** APP-SLICE-READY(invoice-delivery).

**Conditional gates:** NEXT-26: inbound documents enter the assisted supplier-review workflow.

**Evidence:** R03, R09, X05 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Pinned exchange profile

```text
PeppolRelease {
  version, exact CustomizationID/ProfileID,
  supportedUBLDocumentTypes, schemaHashes, schematronHashes,
  codeListVersions, countryRuleVersions, monetaryRules
}
ParticipantBinding {book, schemeId, participantId, verifiedRevision, providerAccount}
ExchangeArtifact {semanticInvoiceRevision, release, exactXMLHash, validationReport}
ExchangeAttempt {artifactId, senderBinding, recipientBinding, externalMessageId, providerKey}
IncomingEnvelope {providerAccount, messageId, participant, rawBytesHash, signatureOrAuthWitness}
```

The checked official BIS index identifies a May 2026 release [X05]. Pin actual schema/rule bytes before activation; a page title is not a validation bundle. No access-point vendor or credential has been selected by this design. Its concrete adapter must implement the declared send/status/inbound-proof contract before external acceptance can be claimed.

## Semantic rendering

```text
renderBIS(document, release):
  require document is an immutable issued invoice OR legal credit, not a draft
  require seller/buyer endpoint schemes and legal identities explicitly mapped
  require supported currency/tax categories and exact line price-base quantities
  emit selected UBL Invoice or CreditNote root and matching type-specific fields
  per line:
    retain quantity, unit, price/baseQuantity, allowances and charges
    compute/check line extension under the release's exact rounding rules
    emit original tax category/rate with exemption/reverse-charge reason where applicable
  documentNet = sum(lineNet) - documentAllowances + documentCharges
  tax = sum(taxCategorySubtotals)
  inclusive = documentNet+tax
  payable = inclusive-prepaidAmount+documentRounding
  require every amount matches the retained semantic document and original rules
  emit legal references, payment means and original-invoice references for credits
  return exact UTF-8 XML
```

Credit documents use their own UBL structure and economic direction. Do not blindly negate every field from an Invoice. The first implementation can support only the existing domestic invoice/credit profiles; other BIS categories remain named unsupported cases. It must not change a legally issued total merely to satisfy a validator.

## Validation and outbound delivery

Run strict XML parsing, XSD and Schematron plus semantic reconciliation against the source invoice. A valid syntax with the wrong party, amount or original invoice reference fails. Retain validator versions, complete diagnostics and no-network schema resolution. Validation unavailable is not pass.

```text
prepareOutbound(artifact, recipient):
  require exact artifact validation and current sender/recipient bindings
  seal external target, document hash and delivery purpose
approveOutbound -> existing authorized-delivery operation
admitDispatch -> current binding/authority check + one stable attempt in tx
sendOutsideTx -> selected access point
recordOutcome -> retain actual transport acknowledgment/status with exact message identity
```

Transport accepted, recipient delivered and invoice paid are different states. An unknown outcome is resolved by provider correlation/idempotency, not a new invoice number or repeated send with a new identity. A replacement delivery intentionally references the same legal document and its prior attempt.

## Inbound path

```text
receiveEnvelope(raw, providerProof):
  verify selected provider authentication and destination participant scope
  key = providerAccount + recipientParticipant + transportMessageId
  if key already retained:
    require identical content hash; return same receipt
  retain envelope/original XML under authorized source intake
  validate supported BIS content and extract structured SOURCE assertions
  create supplier inbox occurrence with sender/message/document provenance
  run ordinary duplicate diagnosis and human review
  do not accept/pay/post solely because Peppol delivered it
```

A new message ID for the same supplier invoice is additional evidence or a duplicate candidate, not another expense. Conflicting bytes under the same transport identity are an integrity incident. A legitimate repeat document with different business identity remains representable.

## Controls and vectors

Link outbound delivery to immutable issue/credit and retain incoming source-to-draft-to-recognition lineage. API/MCP inspect format and delivery state through existing permissions. Approval/signing remain separate where needed.

```text
line10000 + tax2500 -> exclusive10000/inclusive12500/payable12500
same invoice with prepaid2500 -> payable10000; no reduction of original tax by default
credit4000+1000 -> CreditNote for5000 with original invoice reference
XSD-valid XML changed buyer -> semantic mismatch, no send
provider retry same message/hash -> one inbox occurrence
provider accepted, response lost -> recover attempt, no second legal issue
```

Scope is a qualified BIS subset and one actually configured access point. No claim of automatic support for all e-invoicing networks, national rules or receipt types is made.


---

<a id="part-24"></a>

# NEXT-47: Document signatures bound to exact content and purpose

**Priority:** P1. **Owner lane:** DELIVERY. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing artifact, identity and external-attempt owners. Add document-signature intent and a selected BankID/signing adapter.

**New scope, not repeated work:** The first wave generates K2/iXBRL content but does not prove document signing. Add purpose-bound signature evidence without treating ordinary login or accounting approval as document signature.

**Dependencies:** NEXT-24. **Integrate after:** APP-SLICE-READY(artifacts).

**Evidence:** R03, R10, P24, X06 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Signing scope

```text
SignatureManifest immutable {
  book, legalEntityRevision, purpose,
  semanticModelId/hash, renderedArtifactId/hash/length,
  reviewedDisplayRepresentation, requiredSignerSet,
  signaturePolicyRelease, artifactRelations, createdAt
}
SignatureIntent {
  manifestId, expectedSignerIdentity, consentTextHash,
  nonce, expiry, providerEnvironment, requestDigest
}
SignatureEvidence immutable {
  intentId, providerOrderRef, signedPayloadHash, actualSignerIdentity,
  signatureBytesRef, certificate/statusEvidenceRefs,
  verifierVersion, technicalResult, completionTime, usageEligibility
}
```

Purposes include signing the original annual report, approving an internal accounting plan and certifying an adopted copy. They are not equivalent. Authority for one purpose cannot satisfy another. A signature manifest names which exact bytes are signed and which semantic copy relationship is allowed.

## Start flow

```text
prepareSignature(document, signer):
  require immutable selected content and required document validation
  require actual required signer roles from reviewed company/governance facts
  require rendered content shown to signer agrees with semantic manifest
  freeze visible consent text and cryptographically bound document manifest
  select qualified signing profile, not authentication-only login
  persist intent and exact request identity

startSignature(intent):
  short tx: current authority + exact replay + admit one external start attempt
  outside tx: call selected provider with the exact visible text and bound data
  short tx: retain returned order/correlation identity and challenge metadata
```

An adapter exposing nonvisible signed data may bind the document digest there only when its qualified protocol and visible-consent presentation establish the intended document-signing relationship. Merely storing a PDF hash beside a successful login is insufficient. Do not label a hash-binding experiment a legally valid signing product.

BankID's public autostart guidance says client return is not sufficient outcome evidence and completion should be obtained from collect [X06]. Exact current signing request/response and cryptographic verification details were not fully extractable in this review; the adapter release must pin them before production activation. No invented API fields or endpoint version are mandated here.

## Completion and verification

```text
completeSignature(orderRef):
  read intent under current service retention authority
  query/receive authentic provider result OUTSIDE financial tx
  require returned orderRef matches original attempt and provider environment
  verify signature chain, signed data binding and status using qualified verifier
  require signed digest == exact manifest digest
  require signer identity == intended permitted signer under purpose policy
  App tx:
    replay known result first
    append raw completion and verification evidence
    evaluate current document revision/authority for intended use
    mark technical signature valid independently from current usage eligibility
    save receipt; do not mutate signed artifact or issue accounting
```

A role change can make a technically valid signature unusable for the intended submission without erasing the historical signature. A content change after any required signer signs produces a new manifest and new required signatures for that content. Do not silently combine signatures over different versions.

## Lost response, multiple signers and scope

Persist known provider references immediately. If the start response is lost and the provider offers no safe lookup, keep an unknown start attempt until the documented cancellation/expiry recovery proves how to proceed. Do not restart a second signature order merely because a local lease expired. A known pending order is collected/cancelled through its actual contract.

For multiple signers, each signs the same allowed content manifest with an independent intent. Completion requires exactly the required set under the chosen governance policy, not an arbitrary count. A duplicate signer does not replace another required role.

The app can orchestrate original-document signing. It does not replace an authority service's own later fastställelse signing ceremony. NEXT-48 keeps that distinct.

## Interface and vectors

Show actual document, purpose, signer role, version, technical completion and usable-for-submission status. Do not expose signature secrets/order challenge material in general accounting lists.

```text
login succeeds -> documentSignatures remains0
signature returns for artifact A while current selected artifact B -> retain A,
    cannot mark B signed
three required signers, same person signs twice -> still missing required distinct signer
provider order completion replay -> one signature evidence record
membership revoked after signature -> retain history; re-evaluate permitted future use
```

Completion requires configured provider access and observed end-to-end evidence. The pseudocode solves ownership and recovery, not the unavailable cryptographic/schema qualification bytes.


---

<a id="part-25"></a>

# NEXT-48: Bolagsverket submission and authority-outcome lifecycle

**Priority:** P1. **Owner lane:** DELIVERY. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing annual-report semantic models/artifacts, signature records and external attempts. Implement one selected Bolagsverket profile through the provider adapter.

**New scope, not repeated work:** NEXT-24 ends at local generation/validation. Add the actual filing lifecycle while keeping original signatures, adopted copy certification, upload and registration distinct.

**Dependencies:** NEXT-24, NEXT-47. **Integrate after:** APP-SLICE-READY(external-delivery).

**Evidence:** R03, P24, X07, X08 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Obligations and immutable intent

```text
StatutoryObligation {
  entity, reportingFamily, fiscalYear, applicableFramework,
  requiredOutcomePolicy, deadlineRef
}
SubmissionIntent immutable {
  obligationId, reportRevision, copyArtifactHash,
  originalSignedManifest, copyEquivalenceProof,
  actualMeeting/adoptionFacts, authorizedCertifierIdentity,
  providerProfileVersion, environment, predecessorIntent?
}
SubmissionAttempt {intentId, attemptId, stableProviderIdentity?, requestHash, admittedAt}
ProviderObservation immutable {
  attemptId, exactProviderStatus, rawEvidenceRef, receivedAt,
  normalizedMeaning, receiptIdentity?, coveredArtifactHash?
}
```

Bolagsverket's published user workflow separates software upload, an invited authorized person's certification/submission and later authority processing [X07]. Do not equate an upload response with fulfillment. The exact services, fields and legal status mapping must come from the selected current service specification [X08], not a guessed REST interface.

## Prepare and admit

```text
prepareSubmission(reportRevision, governanceFacts):
  require selected report complete under its qualified local profile
  require required original-signature evidence and actual adoption facts for this stage
  require copy faithfully represents signed original under the qualified copy policy
  require correct entity/year and no incompatible active/accepted submission
  verify intended certifier is actually eligible, not merely app administrator
  freeze artifact, signer/certifier, service version and return/deadline relationships
  obtain separate human authorization for external submission

admitSubmission(intent):
  App tx:
    recheck current authority, report/signature/copy facts and intent version
    replay exact successful admission before new-work checks
    refuse unresolved prior same-obligation attempt unless provider-safe continuation exists
    create attempt and outbox with exact bytes hash and stable correlation
```

A signed original and an iXBRL copy need not be byte-identical formats. Their semantic equality is an explicit validated relationship, not permission to sign one set of figures and submit another.

## Provider state machine, without fictitious status names

The application normalizes actual provider observations into these internal distinctions. The adapter mapping is finite and versioned; unsupported raw statuses are retained as `needs_review` rather than assumed success.

```text
prepared
  -> validation_blocked | authorized
  -> upload_admitted
  -> upload_outcome_unknown | copy_uploaded
  -> awaiting_authority_certification
  -> submitted_pending
  -> received | rejected | outcome_unknown
  -> registered_if_required | correction_requested
```

Not every raw API provides every state directly. A missing observation remains unknown. `registered_if_required` is fulfilled only by a receipt/status that actually means it under the selected obligation policy. Copy upload, original signature and authority fastställelse certification are separate recorded events.

```text
advanceSubmission(attempt):
  recover known remote correlation before initiating another request
  call only the action allowed by current provider state and human authorization
  outside tx: upload/query/invite through selected provider contract
  inside short tx: append authentic observation and update derived attempt state
  enqueue bounded follow-up only when its allowed next action is known
```

Where the authority hosts certification, direct the eligible person to that ceremony. Do not simulate it by marking NEXT-47's internal signature complete or using a general accounting-agent credential.

## Rejection, correction and unknown outcomes

A rejection creates a case with the exact artifact and diagnostic. Correcting the report produces new content, validation and signatures where required, then a new linked intent. The old rejected or accepted bytes remain retained. After acceptance, replacement/correction follows an explicitly supported authority procedure, not a blind repeated upload.

A lost upload response is resolved using documented correlation/read-back or supported provider idempotency. If neither exists, freeze the attempt as unknown and require evidenced investigation. Enqueue retry cannot establish an external exactly-once guarantee.

Manual evidence can be retained, but label it as reported/reviewed evidence rather than pretending the backend fetched a provider-verified receipt. The obligation's required outcome policy decides what review can satisfy it.

## UI, controls and vectors

Display original signed content, submission copy, actual meeting/certification facts, all attempts, pending human action and authority receipt. A deadline reminder is not dismissed merely because an upload exists.

```text
HTTP upload200 with copy reference -> copy_uploaded, obligation not fulfilled
original signature valid, authority certification absent -> awaiting human action
same artifact upload outcome unknown -> no new submission identity automatically
rejected report corrected -> new revision linked to original rejection
accepted receipt for other entity/year -> reject linkage, keep raw evidence quarantined
registered required but only received observed -> still pending required outcome
```

No provider credentials, actual meeting facts or acceptance evidence were supplied by this design. Local model/adapter tests can prove the transition machinery; only an authorized provider exercise proves connected filing.


---

<a id="part-26"></a>

# NEXT-49: Rule-change impact and evidence-backed obligation fulfillment

**Priority:** P0. **Owner lane:** REPORTING. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing rule releases, retained plan/report dependencies and closing/deadlines.ts manual obligations/calendar feeds.

**New scope, not repeated work:** Do not rebuild deadlines or rule activation. Add exact affected-record analysis and require meaningful fulfillment evidence instead of treating any nonempty reference string as proof.

**Dependencies:** NEXT-02. **Integrate after:** APP-SLICE-READY(closing/deadlines).

**Conditional gates:** NEXT-04: VAT calculations are impacted; NEXT-21: payroll declarations are impacted; NEXT-48: annual-report authority outcomes fulfill deadlines.

**Evidence:** R03, R06, P02 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Impact inventory

```text
RuleChangeNotice immutable {
  oldReleaseId, newReleaseId, effectiveScope,
  reason, qualificationEvidence, affectedSemanticSelectors
}
ImpactSnapshot {
  noticeId, recordedCutoff, completeTargetMembership,
  targets: [{owner,id,revision,usedRule,basisDigest,impactKind}]
}
ImpactDecision immutable {
  targetRevision, kind: unaffected_with_reason | reprepare | amend | human_review,
  evidence, proposedSuccessor?, reviewer
}
```

Query actual retained dependency references. Do not grep free-text documents or invalidate every book because a new rate table exists. Historical correctness and current executability are distinct: a future-only rule change need not invalidate a past calculation. A retroactive correction identifies affected original periods without rewriting their reports.

## Bounded impact calculation

```text
captureRuleImpact(notice):
  require newly qualified release and explicit effective-scope relationship
  select exact plans, calculations, declarations and deadlines referencing old release
  intersect each target's semantic dates/case with notice's applicability change
  freeze target IDs/revisions and cutoff before paging
  if full selection exceeds bound: partition explicitly, retain total/continuation

classifyImpact(target, notice):
  if outside changed applicability: unaffected_with_reason
  if prepared/unexecuted: require fresh computation and approval when effects differ
  if committed/unfiled: create owned financial/control review, no automatic reversal
  if filed/accepted: create amendment obligation retaining original receipt/artifact
  if missing old facts prevent determination: needs_evidence, not unaffected
```

A background handler may compute prospective replacements or comparisons through the owning prepare operation. It cannot approve them, mutate old artifacts or call a generic arbitrary financial correction. Freeze child identity by notice+target+revision so restarts do not create duplicate amendment cases.

## Typed fulfillment evidence

```text
FulfillmentReference =
    LocalPreparedArtifact {owner, artifactId, revision, digest}
  | SubmittedAttempt {owner, attemptId, artifactDigest, environment}
  | AuthorityOutcome {owner, observationId, receiptIdentity, coveredScope}
  | ReviewedExternalEvidence {originalRef, reviewer, assertedMeaning, limitations}

verifyFulfillment(obligation, reference):
  resolve reference under current book/role access
  require same entity, family, period and intended revision/supersession relation
  require exact required outcome predicate, not a numeric status ranking
  require environment appropriate to obligation; sandbox cannot fulfill production
  require artifact integrity and relevant source/outcome evidence
  return satisfied OR pending/mismatch with precise reason
```

Keep existing arbitrary operator references as historical `reported` observations. Do not silently upgrade them to verified authority evidence. A required `prepared` deliverable can be satisfied by its valid local artifact; a required authority outcome cannot.

## Transactions and calendar behavior

```text
linkFulfillment(command):
  App tx:
    reauthorize; lock book/obligation; recover exact command
    check expected obligation revision and required-outcome policy
    validate referenced retained outcome/artifact from its own owner
    append fulfillment link with validation witness
    update derived current state and calendar revision
    save receipt
```

Dismissed reminder and fulfilled obligation remain separate. A revised due date changes the existing calendar event's revision while retaining stable identity. Genuine withdrawal needs a reason/evidence and explicit cancellation output; successful fulfillment is not automatically a cancellation of historical obligation. Use the existing feed revocation and renderer rather than another calendar service.

Statutory date rules are selected by actual reporting period and jurisdiction plus the applicable holiday/timezone release. Do not invent due dates from a generic “monthly plus30days” shortcut. An override retains the original basis and its reason.

## UI and vectors

Show what rule changed, exactly which records are affected, old/new calculation differences, owner action and fulfillment evidence. Sensitive payroll impacts obey payroll scope even when displayed in a shared work index.

```text
new rate effective next year -> prior-year accepted artifact not silently stale
retroactive mapping fix affects3 returns -> exactly3 retained impact targets
nonempty string 'done' -> reported note only, not verified authority acceptance
sandbox receipt matches production period -> wrong environment, unfulfilled
due-date revision -> same calendar identity, higher revision
reminder dismissed -> required submission still outstanding
```

This completes the backlog's impact/fulfillment semantics. It does not automatically decide that a legally filed document must be amended merely because a code version changed; the notice must specify the actual corrected rule and affected cases.


---

<a id="part-27"></a>

# NEXT-50: Agent book context, deltas and cross-domain unresolved-work index

**Priority:** P0. **Owner lane:** AGENT. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing shared capability registry, case snapshots, period preparation runs and domain report/read owners.

**New scope, not repeated work:** NEXT-16 prepares a period and NEXT-01 routes a case. Add a compact cross-domain orientation and delta interface so an agent does not rebuild the full book context every turn.

**Dependencies:** NEXT-01, NEXT-16. **Integrate after:** APP-SLICE-READY(capabilities).

**Conditional gates:** NEXT-49: including qualified deadline/impact outcomes; NEXT-33: including employee claim summaries under separate permissions.

**Evidence:** R02, R03, R07, P01, P16 in [SOURCES.md](SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

**Late source handoff:** NEXT-01 is reported implemented in `4671a2fb` as `cases_resolve_review`. Consume that actual contract, not a proposed ownership-version field it intentionally omits. See [REVISION-NOTE.md](REVISION-NOTE.md).

## No second accounting authority

```text
BookContextSnapshot {
  id, principalScopeFingerprint, book, requestedGoal,
  coherentRecordedCutoff, ledgerBoundary,
  profile/applicabilityRefs, sourceCoverage,
  moduleStatuses: available | unsupported | unavailable | not_authorized,
  unresolvedWorkRefs, existingPlans/receipts,
  allowedCapabilityRefs, dependencies, contentDigest
}
WorkRef {
  owner, identity, revision, kind, severity, affectedPeriod,
  blockedOperation, missingInputs, nextPermittedPreparation, immutableRef
}
```

Context rows point to existing owners. They are not mutable balances, a second approval register or a vector database of authoritative financial facts. A source quotation is untrusted evidence, not instructions to the agent. General context omits salary details unless the principal has the separate payroll grant.

## Coherent capture

```text
prepareBookContext(goal, scope, key):
  use one admitted repeatable-read capture or equivalent coherent snapshot
  recover identical successful capture first
  for each explicit supported context adapter:
    check capability/scope before querying
    read bounded summary and full count/continuation under the SAME tx
    retain referenced owner versions and exact selected scope
  unknown profile fields remain Unknown
  unavailable owner remains Unavailable, not zero unresolved cases
  abort capture on an unexpected database transaction failure
  # Do not catch failed SQL and keep querying an aborted transaction.
  derive work dependency order and next permitted preparation actions
  materialize immutable context membership and save receipt
```

Read-only retrieval of an existing context creates nothing. A request to refresh context is an explicit capture operation with a key. A large scope returns a bounded context plus continuation to owner-specific pages, not an unlabelled first-page total. Complete ledger boundary excludes half of a multi-voucher group.

## Work selection and compact output

```text
rankWork(context, requestedGoal):
  retain only authorized work relevant to selected goal/period
  order by: prevents selected goal, financial materiality class,
            deadline urgency under verified dates, stable owner/id
  collapse repeated identical missing-fact blockers into one question with affected refs
  do not merge their distinct financial effects
  return concise current facts, unresolved decisions and existing operation links
```

A capability registry identifies read, prepare, human approval and external effects. Progressive exposure chooses a useful authorized subset without inventing another tool implementation. Suggested next actions include exact known IDs and missing required inputs, never a forged approval token. The target operation rechecks authority and dependencies on execution.

## Delta semantics

```text
getContextDelta(baseId, targetId):
  authorize BOTH snapshots and current scope
  if scope/permission fingerprint differs in a way that can disclose revoked content:
      return FreshContextRequired without old private names or values
  require same selected book/goal semantics and supported context versions
  compare by (owner,identity), not display text
  added = target identities absent in base
  changed = same identity with changed semantic revision/digest
  resolved = source owner explicitly reports resolution
  removed = only a confirmed scope/deletion-status change under that owner
  unknownNow = target adapter unavailable or no longer sufficient evidence
  return delta + baseDigest + targetDigest + complete continuation metadata
```

An item absent because a domain adapter failed is not resolved. A receipt remains committed after a queue record is pruned. An expired pending approval can change next actions while its historical approval record remains in the old snapshot.

Optional remembered choices are records with source scope, reviewed applicability and expiry. Recall can suggest an already approved deterministic rule, but it cannot convert an old conversation into current permission or an accounting fact. User corrections propose new rules through the existing review path.

## Agent/UI integration and verification

Expose prepare/get/delta/work-page operations via shared REST/MCP semantics. The UI uses the same context to show “what blocks this period” and exact links to owning review screens. Never call a financial operation merely by rendering the overview.

```text
module contains0 rows + coverage unknown -> do not report complete
payroll grant revoked -> no delta leaking previous employee names
new bank payment for recognized invoice -> settlement suggestion, not new purchase
one shared missing VAT-method fact blocks12 items -> one question +12 references
base3 work items, target2 plus owner reports resolved1 -> precise resolution
owner unavailable in target -> unknownNow, not deleted/resolved
```

Measure returned bytes, tool calls and reproducible task success on the same fixed cases before claiming improved agent efficiency. A shorter context that hides a financial blocker is worse, not better. This packet promises an inspectable interface and proof criteria, not an unmeasured model-performance improvement.


---

<a id="part-28"></a>

# Integration, non-overlap and dispatch

Late branch movement is recorded in [REVISION-NOTE.md](REVISION-NOTE.md). The source review remains pinned; the current resolver is consumed rather than rebuilt.

These 25 packets are NEXT-26 through NEXT-50. They extend the prior application-owned v2 designs, not the superseded SQL-owned package. Their IDs are work IDs, never migration numbers.

## Root handoff

Before dispatch, read current AGENTS.md and the application replacement plan. Record current HEAD and dirty ownership claims. Resolve each existing-operation path in the actual checkout. If a proposed slice already exists, qualify/complete that implementation and record the difference instead of rebuilding it. Do not infer that all first-wave packets are complete because this second wave exists.

Do not dispatch 25 independent writers into shared files. Root integrates schema/grants, core transaction/admission, shared contract exports, capability composition and top-level routing. Domain owners supply leaf operations, pure calculators, typed persistence and local UI. All nested financial writers accept the caller's transaction. No public execute call opens another transaction from inside a financial group.

The current replacement owner retains all placeholder-operation ports and baseline proof. The five earlier WIPs remain reserved. Old numeric migration references are provenance, not instructions to resurrect stored procedures.

## Priority interpretation

P0 means high accounting value when the workflow applies and its prerequisites exist. It does not mean a company must use cash bookkeeping or employ staff. P1 extends important business lifecycles. P2 is conditional breadth. A no-payroll company must not wait for payroll expansion; a company using an unsupported required case cannot be labelled complete by omitting it.

Use NEXT-37 after the VAT owners hand off to finish the distinction between tax-account assessment and reclassification. NEXT-38 matters only for a verified cash-method company. NEXT-31 helps period accuracy for supported subscriptions/accruals. NEXT-50 improves agent operation only after actual domain summaries exist. Extraction in NEXT-26 is for missing/new facts, not a reason to redo existing receipt matching.

Possible nonconflicting leaf starts are 26, 27 and 28 once their existing application owners are available. None is permission to overlap the current source-intake/commerce/delivery port. Treasury and payroll chains are deliberately sequential within shared capacity owners.

## Reserved work

**WIP-VAT03:** Existing VAT control reclassification and its qualification. Consume the released application owner, do not repeat the former 9120/9130 qualification assignment.

**WIP-FX02-P1:** Existing paired FX partial settlement. Consume the released pure release calculation and internal tx mutation, do not recreate the former 9140 algorithm.

**WIP-AST03-UI:** Existing impairment UI/control/disposal closure. Consume the final asset basis and released tx ports after owner handoff.

**WIP-VAT04-A1:** Existing obligation-owned VAT amendment financial delta. No second target-minus-prior owner.

**WIP-COM2-W1:** Webshop intake, raw order identity, catalog snapshots and order authority. No packet takes this over.

**APPLICATION-REPLACEMENT:** Existing SQL-to-Effect migration, placeholder-operation closure and baseline proof. All new packets require released owning slices.

## Packet dependency map

| Packet | Required first/new wave contracts | Integration handoff | Conditional cases |
|---|---|---|---|
| [NEXT-26](packets/NEXT-26.md) | Existing owner | APP-SLICE-READY(purchases/inbox) | NEXT-03: a reviewed draft is subsequently accepted and posted |
| [NEXT-27](packets/NEXT-27.md) | Existing owner | APP-SLICE-READY(commerce/crm-master) | NEXT-02: legal identity facts or payment-role qualification are needed |
| [NEXT-28](packets/NEXT-28.md) | Existing owner | APP-SLICE-READY(commerce/collections), APP-SLICE-READY(durable-delivery) | NEXT-15: the selected invoice has credit-note adjustments; NEXT-30: customer-credit balances affect the reminder amount |
| [NEXT-29](packets/NEXT-29.md) | NEXT-02 | APP-SLICE-READY(commerce/invoice-lifecycle) | NEXT-15: an issued recurring invoice needs a credit |
| [NEXT-30](packets/NEXT-30.md) | NEXT-15 | APP-SLICE-READY(commerce/register) | NEXT-04: credit notes affect a supported VAT return |
| [NEXT-31](packets/NEXT-31.md) | NEXT-03, NEXT-13 | APP-SLICE-READY(subledger/schedules) | WIP-AST03-UI: the released schedule/control implementation is shared with the asset owner |
| [NEXT-32](packets/NEXT-32.md) | NEXT-02 | APP-SLICE-READY(subledger/owners) | NEXT-06: shareholder funding already recognized supplies the opening loan basis; NEXT-13: publishing reconciled loan controls |
| [NEXT-33](packets/NEXT-33.md) | NEXT-03 | APP-SLICE-READY(purchases), APP-SLICE-READY(payroll-foundation) | NEXT-21: the approved payout route is payroll rather than a payable payment |
| [NEXT-34](packets/NEXT-34.md) | NEXT-33 | APP-SLICE-READY(payroll-foundation) | NEXT-20: the selected entitlement includes taxable compensation; NEXT-21: payout/reporting uses payroll |
| [NEXT-35](packets/NEXT-35.md) | NEXT-20 | NEXT-21 | None |
| [NEXT-36](packets/NEXT-36.md) | NEXT-21 | APP-SLICE-READY(payroll) | NEXT-35: the correction includes variable, absence or holiday components |
| [NEXT-37](packets/NEXT-37.md) | NEXT-04 | WIP-VAT03, WIP-VAT04-A1, APP-SLICE-READY(tax-account) | None |
| [NEXT-38](packets/NEXT-38.md) | NEXT-03, NEXT-04 | APP-SLICE-READY(commerce/register) | NEXT-23: the reviewed unpaid population is consumed by financial year-end |
| [NEXT-39](packets/NEXT-39.md) | NEXT-30 | APP-SLICE-READY(source-intake), APP-SLICE-READY(commerce/register) | NEXT-40: processor balances use a non-book currency; WIP-COM2-W1: read-only order provenance is required; do not modify its intake |
| [NEXT-40](packets/NEXT-40.md) | NEXT-17, NEXT-18 | WIP-FX02-P1, APP-SLICE-READY(banking) | None |
| [NEXT-41](packets/NEXT-41.md) | NEXT-18 | WIP-FX02-P1, APP-SLICE-READY(commerce-fx) | NEXT-40: the affected chain includes native foreign-cash holdings; NEXT-23: affected financial periods require approved reopening |
| [NEXT-42](packets/NEXT-42.md) | Existing owner | WIP-AST03-UI, APP-SLICE-READY(subledger) | NEXT-19: checking disposal/proceeds consumers; NEXT-13: presenting the resulting financial controls |
| [NEXT-43](packets/NEXT-43.md) | NEXT-14, NEXT-13 | APP-SLICE-READY(dimensions) | None |
| [NEXT-44](packets/NEXT-44.md) | NEXT-12, NEXT-14 | APP-SLICE-READY(historical-migration) | NEXT-11: independent roundtrip export is part of acceptance |
| [NEXT-45](packets/NEXT-45.md) | NEXT-13 | APP-SLICE-READY(reports) | NEXT-40: the selected cash perimeter contains foreign-currency holdings; NEXT-39: processor/transit positions belong to the selected cash perimeter |
| [NEXT-46](packets/NEXT-46.md) | NEXT-03, NEXT-15 | APP-SLICE-READY(invoice-delivery) | NEXT-26: inbound documents enter the assisted supplier-review workflow |
| [NEXT-47](packets/NEXT-47.md) | NEXT-24 | APP-SLICE-READY(artifacts) | None |
| [NEXT-48](packets/NEXT-48.md) | NEXT-24, NEXT-47 | APP-SLICE-READY(external-delivery) | None |
| [NEXT-49](packets/NEXT-49.md) | NEXT-02 | APP-SLICE-READY(closing/deadlines) | NEXT-04: VAT calculations are impacted; NEXT-21: payroll declarations are impacted; NEXT-48: annual-report authority outcomes fulfill deadlines |
| [NEXT-50](packets/NEXT-50.md) | NEXT-01, NEXT-16 | APP-SLICE-READY(capabilities) | NEXT-49: including qualified deadline/impact outcomes; NEXT-33: including employee claim summaries under separate permissions |

## Concrete cross-owner contracts

| Producer | Consumer | Required result, not a second authority |
|---|---|---|
| NEXT-03 | 26, 31, 33, 38, 46 | Source-line recognition and tax-fact compiler plus internal tx creation/adoption |
| NEXT-15 | 30, 46 | Original line credit capacity, legal document identity and negative tax effects |
| NEXT-30 | 28, 39 | Customer-credit liability and refund capacity, distinct from unpaid AR |
| Existing schedule/impairment WIP | 31, 42 | Exact source basis, future occurrence lifecycle and approved internal tx effects |
| NEXT-20/21 | 33-36 | Frozen earnings/tax computations, already-recognized liability handoff and actual paid/reporting identity |
| VAT WIP owners | 37 | Effective role-signed reclassification/amendment vectors and current obligation version |
| NEXT-38 | NEXT-23 | Complete cash-method unpaid-recognition population and next-year no-duplicate settlement contract |
| FX WIP and NEXT-17/18 | 40-41 | Exact paired release and effective carrying/event history, without another obligation balance |
| NEXT-14/13 | 43-45 | Original classifications, fixed financial cutoffs and source-anchored contributions |
| NEXT-24 | 47-48 | Immutable statement model, exact copy artifact and local validation basis |
| NEXT-47 | 48 | Purpose-specific signature evidence, not an authority-hosted fastställelse event |
| Domain outcome owners | 49 | Typed same-scope prepared/submitted/accepted receipts, never free-text truth |
| Every released context adapter | 50 | Bounded coherent summary, complete counts, exact versions and honest unavailable state |

## Shared-file and semantic conflicts

Treasury 39-41 must serialize changes to cash/FX capacity projections. Customer credit 30 and reminder 28 share customer state but do not own each other's writes. Payroll 33-36 must agree source-component and liability handoff identity before implementation. Dimension restatement 43 may not change original-journal or SIE44 input meaning. Signing47 and filing48 share artifact references but never substitute one signature purpose for another.

A safe port can retain conservative stale checks. Narrow them only in a new understood plan version after the corresponding mutation population and concurrency proof exist. Removing a whole-account version without replacing its affected resource/predicate dependency is not an optimization.

## Worker completion format

Each worker returns one concise handoff with: exact changed paths; exported operations and contracts; schema/grant requirements; declared financial ownership; examples and independent expected outcomes; static/runtime checks actually run; unresolved input/port gates; shared integration diff; and a next action. No repeated full logs to the coordinator. No nested delegation unless the coordinator explicitly selects it.

Use the existing test authorization policy. This dossier supplies design vectors and proof obligations, not permission to add repository tests, run provider calls, post actual company books or deploy. Financial and legal profiles remain separately qualified.


---

<a id="part-29"></a>

# Consequential decisions made in this wave

These are proposed financial/application designs for NEXT-26..50. They do not activate a legal profile, change repository code or grant execution authority. Their source anchors and limitations are in SOURCES.md. They preserve the application-owned boundary and the reserved first-wave owners.

## 1. Record extraction suggestions without replacing reviewed facts

Extraction runs against an immutable original and returns source-located suggestions. The review performs a three-way comparison against the draft revision on which extraction started and the current draft. Confirmed human changes win; conflicts stay visible. Accepted invoices receive correction suggestions, never rewritten fields. This closes the useful lifecycle around the existing inbox rather than restarting receipt matching.

## 2. Resolve party identity in a retained overlay

Same legal identity can redirect discovery, but original invoice and payment relationships remain unchanged. Neither legal identity resolution nor a common bank account grants permission to net debts or reuse payment capacity. An erroneous merge is another reviewed identity decision with downstream impact, not mass rewriting of historical foreign keys.

## 3. A recurring cycle is independent of template revision

The occurrence key uses the agreement and stable cycle, while the selected template is retained as input. Changing price or template version cannot generate a second invoice for the same cycle. Service-coverage checks catch cadence changes that might overlap prior billing. Dates are calculated from the original anchor, not successive clamped dates.

## 4. Customer credit is its own liability, not negative AR

For a same-currency invoice, original gross G, effective credits K and paid amount P imply:

```text
unpaidAR = max(G-K-P,0)
creditPrincipal = max(P-(G-K),0)
```

A new credit first clears unpaid AR and then increases a refund/applicable-credit liability. Refunds debit that liability against actual cash. They do not reverse sales or VAT again. Unapplied cash has its own origin and is distinguished from taxable advance receipts. The ordinary invoice capacity cannot become negative to hide either condition.

## 5. Payroll handoffs consume existing liabilities

An employee receipt claim can be recognized once and paid through payroll or direct payment, not both. A taxable mileage award in the initial accrual profile establishes its entitlement liability at award time. Payroll calculates its tax/reporting consequences and debits that existing liability rather than recognizing the cost twice. Variable/holiday pay similarly releases previously accrued holiday and social provisions before expensing only a true difference.

Paid payroll correction distinguishes a new payment, a qualified future-pay adjustment and an actual gross recovery claim. Original withholding and cash do not disappear because a later entitlement is lower. The exact permitted reporting case is a qualified input, with original item identity preserved.

## 6. VAT assessment is not reclassification or payment

The two active VAT owners retain reclassification and amendment effects. NEXT-37 owns authority assessment and an explicitly qualified precision bridge.

```text
N = exact accounting net
R = reported amount represented in minor units
A = actual evidenced assessed charge

initial settlement vector = -N
qualified rounding bridge = +(N-R)
assessment vector = +A
```

If A=R, those settlement vectors clear. An unexplained A-R remains a difference; it is not a rounding plug. Existing tax-account journal/match evidence is adopted without posting/reserving twice. Bank-to-tax-account cash transfer remains separate.

## 7. Cash-method recognition has explicit source coverage

Each invoice line has disjoint recognized portions and unrecognized commercial outstanding. Payment recognizes only the part not already covered by a prior recognition. Year-end records eligible unpaid portions exactly once. Next-year payment settles their AP/AR positions and does not create another cost/revenue or VAT fact. Complete year-end capture must include population changes, not merely the invoices on the first page.

## 8. Processor clearing uses gross events, not net payout revenue

Stripe balance-transaction identities own charge, refund, fee and payout effects. A charge settles an already recognized sale, a refund consumes an owned refund liability and a payout moves processor balance into transit. Bank receipt clears transit. Each event is accounted once even when retrieved through several provider endpoints. Disputes/reserves are not automatic VAT credits or hidden operating costs.

## 9. Foreign cash and foreign obligations are different capacities

Commerce continues to own the foreign payable/receivable. Foreign cash has native quantity and book carrying under its own cash owner. A payable paid with foreign cash consumes both capacities atomically. Their different carrying releases explain realized FX; no second principal expense or cash entry is created. Native and book-currency controls reconcile separately.

## 10. A late FX correction adjusts carrying attribution, not actual cash

Replay the complete supported dependent chain from a known anchor, inserting the corrected valuation and retaining actual quantities, cash and fees. Compare the desired role/date vectors with prior effective vectors and post only the difference.

Example: an AR of110000 was settled for116000 with old realized gain6000. A corrected prior-year valuation to115000 requires:

```text
December: AR+5000 / valuation gain-5000
January:  AR-5000 / realized gain+5000
```

Cash remains unchanged, final AR remains zero and total gain remains6000. Different period attribution is not zero work merely because the lifetime total matches. Unsupported consumers or closed dates stop the complete repair rather than yielding a partial adjustment.

## 11. Economic impairment reversal needs a counterfactual cap

The cap is computed from the qualified without-impairment history, not the current reduced schedule. The approved target cannot exceed that cap or the eligible impairment reversal capacity. Journal, valuation effect and new future schedule commit together. A fully impaired but still-owned asset has explicit zero-carrying state, no fake positive installment and no automatic disposal.

## 12. Analytical restatement does not modify original dimension assignments

Original tags remain financial evidence. Reviewed classification revisions form an overlay with its own cutoff. Every report declares original or reviewed mode and pins exact classification IDs. By-value totals reconcile to the same unfiltered total. A project retag cannot alter tax, account, currency or journal amount.

## 13. Cash-flow classification must explain the entire balance change

Actual cash flows are categorized through owned economic relationships. Internal transfers are eliminated only with evidence. Exchange carrying effects and perimeter changes are explicit bridges:

```text
closing = opening + external net flows + exchange effects + perimeter changes
```

Unknown rows can produce a zero arithmetic difference and still make the statement incomplete. An unpaid invoice or depreciation entry is not a cash movement.

## 14. Upload, signing and fulfillment remain separate

Signing binds a specific purpose and exact content manifest. A successful identity login is not a document signature. The original annual report, a faithful electronic copy and authority-hosted fastställelse certification have separate relationships and evidence. Local upload success does not fulfill a submission obligation.

NEXT-49 therefore verifies typed same-entity/period/revision outcome references. A free-text 'done' can remain a reported note but cannot become a verified authority receipt. Reminder dismissal is not fulfillment.

## 15. Agent context is a read model with explicit unknowns

The cross-domain context snapshots existing owners at a coherent cutoff. It groups repeated questions without merging financial effects. A missing or inaccessible module cannot be represented as no work. Deltas compare owner identities and revisions; unavailable data is unknown, not resolved. Permission changes cannot leak prior private context. Shorter output is valuable only when it preserves the financial blockers and safe next actions.

## Not selected

No second ledger, generic workflow interpreter, arbitrary plugin runtime, new queue infrastructure, general CRM, warehouse/inventory project, Rust extraction or multi-country launch is added. The loan lifecycle is a proposed expansion of existing funding, explicitly labelled rather than falsely attributed to a source defect. Statutory tables and provider schemas remain qualified inputs, not invented constants.


---

<a id="part-30"></a>

# Coordinator instruction

Implement the selected NEXT-26..50 work from this package against the actual current OpenERP checkout. This is a second wave, not permission to abandon incomplete first-wave financial work.

Start by reading current AGENTS.md, ADR 0010, ADR 0009 and the application replacement record. Compare HEAD and dirty ownership claims with the pinned evidence in SOURCES.md. The repository changed during preparation; the late observation is recorded in REVISION-NOTE.md. Do not assume an old missing capability remains missing.

Use README.md to select work by the actual company/product priority. Resolve first-wave prerequisites and the owning application migration before integrating a dependent financial operation. Missing company data or provider credentials need not stop pure calculations and internal state-machine implementation, but they prohibit false real-company/provider acceptance claims.

Assign domain-local files and explicit interfaces. Preserve the five reserved WIP owners, current application migration and unrelated dirty edits. Root alone composes shared transaction/admission, baseline/grants, common contract exports, capability routing and top-level UI. Do not resurrect old feature SQL, allocate migration numbers independently or create a compatibility framework for disposable unreleased data. Real retained data is never reset without explicit authority.

For a financial task, implement its pure calculation and named Effect application operation. Pass the same Drizzle transaction into all nested journal, tax, register, approval-use and receipt writes. Use existing outbox and effect-mq ownership. Provider calls, rendering and model inference stay outside financial locks. The packet's helper names describe contracts to bind to actual code; do not create a new framework merely to reproduce their notation.

Retain exact amounts, source identities, purpose-specific approval and once-only financial effects. Corrections repair complete domain consequences, not just journal debits/credits. Reconciliation exposes unexplained records even if their net is zero. A successful same-key retry returns the original receipt after current access admission and before new-work expiry/staleness checks.

Before a worker starts, identify its new delta from NEXT-01..25 and the inspected existing module. Reuse any equivalent code already delivered since the review. A work packet is finished only when the supported input reaches its complete intended financial or nonfinancial result and the related consumers agree. Another JSON preparation record or a UI button alone is not completion.

Use existing permitted checks. New/changed repository tests and real runtime/provider actions follow actual user authorization, not this artifact. The package's checks are design checks only. Do not report them as application proof. Return each worker's exact files, integration requirements, observed checks, retained receipts/artifacts and remaining blockers in one concise handoff.


---

<a id="part-31"></a>

# Sources and evidence boundaries

Repository: `erik-kroon/openERP`, pinned commit `5ac3433e3e75ef7fc0229cbe00107003b63aa32d`. Review date: 26 September 2026. This is a targeted source and requirement review, not an every-file audit. No repository implementation, database suite or external integration was executed.

The new algorithms, ownership choices and packet ordering are design proposals. The cited source supports the observed starting point or requirement. A missing operation in an inspected file is not proof that no other branch or uncommitted workspace implements it. Agents must reconcile the actual checkout before claiming a packet.

## Repository evidence

### R01: GitHub main branch

Branch resolved to 5ac3433e3e75ef7fc0229cbe00107003b63aa32d; capture is a pinned review, not a live-state promise.

Source: https://api.github.com/repos/erik-kroon/openERP/branches/main

### R02: docs/plans/application-owned-accounting.md

Requested lines 1-250 and 250-480. Selected returned plan/status and failure matrix: application-owned replacement, clean baseline, incomplete domain ports and proof. Not all runtime paths were executed or reviewed.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/docs/plans/application-owned-accounting.md

### R03: docs/plans/capability-backlog.md

Coverage index plus supplemental sections; requested full content and lines 140-310. Collections, retagging, employee expenses, recurring invoices, provider exchanges, rule/deadline impacts and agent context are requirements, not completion claims.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/docs/plans/capability-backlog.md

### R04: apps/api/src/application/commerce/collections.ts

Inspected returned code for disputes/actions/history/worklist and reminder preparation. sendAuthorized is false in the recorded action. The full application delivery graph was not exercised.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/apps/api/src/application/commerce/collections.ts

### R05: apps/api/src/application/commerce/crm-master.ts

Directory/export and contact/alias/registry-provenance annotations. A complete reviewed identity-resolution lifecycle was not established by this module review.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/apps/api/src/application/commerce/crm-master.ts

### R06: apps/api/src/application/closing/deadlines.ts

Manual obligation revision, activity, feed and revocation operations. record_outcome accepts a bounded reference string in the inspected operation; it does not itself validate a typed authority receipt.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/apps/api/src/application/closing/deadlines.ts

### R07: apps/api/src/application/capabilities/commerce-invoices.ts

Lines 1-130 map existing purchase/invoice/party operations into shared capability dispatch. Used as path/ownership evidence, not functional acceptance.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/apps/api/src/application/capabilities/commerce-invoices.ts

### R08: apps/api/src/application/purchases/inbox.ts

Inbox registration, recorded extraction attempts and reviewed draft binding through createSupplierInvoiceDraftInTransaction. A provider extraction job was not established by the inspected code.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/apps/api/src/application/purchases/inbox.ts

### R09: docs/plans/04-invoices-payments-registers.md

Lines 1-135: commercial versus financial state, accrual/cash method, year-end unpaid invoices, advances/overpayments, source identities, payment capacities and reports. Historical migration prose is not a fresh runtime observation.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/docs/plans/04-invoices-payments-registers.md

### R10: docs/plans/05-vat-payroll-assets-fx.md

Requested lines 1-190: tax/payroll/asset/FX requirements and selected historical context. Automatic FX reversal wording in old prose is superseded by R11 incremental valuation.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/docs/plans/05-vat-payroll-assets-fx.md

### R11: docs/adr/0008-financial-fx-vat-impairment.md

Lines 1-150 requested. Adopted paired FX carrying, VAT role separation and impairment equations, explicitly reconciled with application ownership under ADR 0010.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/docs/adr/0008-financial-fx-vat-impairment.md

### R12: apps/api/src/application/capabilities/subledger-owners.ts

Lines 1-100 identify existing schedule, control and owner-register operations. Used for paths, not proof of supported new asset states.

Source: https://github.com/erik-kroon/openERP/blob/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/apps/api/src/application/capabilities/subledger-owners.ts

### R13: Application/commerce directory inventories

Connector directory/tree results establish present source paths. A filename is not evidence that every requested scenario is implemented.

Source: https://github.com/erik-kroon/openERP/tree/5ac3433e3e75ef7fc0229cbe00107003b63aa32d/apps/api/src/application

### R14: Supplied NEXT-01..25 application-owned v2 dossier

Input artifact openerp-next-25-effect.zip plus its shared contract and solution index. Used to preserve task identity, exclusions and distinct feature scope. It remains proposed pseudocode, not deployed source.

## Prior-wave identifiers

The following are the supplied application-owned v2 designs, not inferred source functionality. A dependency on one means a released contract/implementation is needed, not that the earlier artifact proves it exists. `Pnn` refers to packet `NEXT-nn` in `openerp-next-25-effect.zip`.

- P01: NEXT-01, Owner-aware case review.
- P02: NEXT-02, Capability-specific company admission.
- P03: NEXT-03, Domestic purchasing with owned tax recognition.
- P04: NEXT-04, Actual domestic VAT return and controls.
- P05: NEXT-05, General-rule cross-border service purchases.
- P06: NEXT-06, Owner-paid expenses, reimbursement and funding.
- P07: NEXT-07, Supplier paid credits and refunds.
- P08: NEXT-08, Payment instruction resolution and replacement.
- P09: NEXT-09, Complete Plaid sync windows.
- P10: NEXT-10, Provider revisions to reviewed bank observations.
- P11: NEXT-11, Separate complete-book SIE4E export.
- P12: NEXT-12, Historical open-item adoption.
- P13: NEXT-13, Semantic P&L and balance-sheet snapshots.
- P14: NEXT-14, Original dimension assignments.
- P15: NEXT-15, Legal customer credit notes.
- P16: NEXT-16, Evidence-aware period preparation.
- P17: NEXT-17, Payable FX and explicit fees.
- P18: NEXT-18, Incremental open-item FX remeasurement.
- P19: NEXT-19, Disposal with proceeds.
- P20: NEXT-20, Frozen regular-payroll calculation.
- P21: NEXT-21, Payroll posting, payslip and AGI artifact.
- P22: NEXT-22, Pre-close tax bridge and INK2/SRU.
- P23: NEXT-23, Financial close and single-count carry-forward.
- P24: NEXT-24, K2 annual-report semantic model and iXBRL.
- P25: NEXT-25, Fixed-revision company rehearsal and restore.

## Primary external sources

Legal and provider facts below are deliberately narrow. Formulas and workflows elsewhere in the dossier are proposed implementations conditional on qualified profiles. We did not download every statutory table, XSD, taxonomy or provider contract.

### X01: Stripe Balance Transaction object

Gross, fee and net in smallest currency units, with net=amount-fee. Source object/type identity needs an explicit accounting mapping.

**Observation limit:** Official page read; no provider access or certified adapter.

Source: https://docs.stripe.com/api/balance_transactions/object

### X02: Stripe Balance Transaction list

The payout filter is for automatic Stripe payouts. Manual payouts cannot assume that membership query.

**Observation limit:** Official page read.

Source: https://docs.stripe.com/api/balance_transactions/list

### X03: Skatteverket cash bookkeeping guidance

Cash bookkeeping recognizes during-year payments and unpaid invoices at year-end. Qualified tax timing and method selection are still required for each supported case.

**Observation limit:** Official page opened; no complete VAT method release qualified.

Source: https://www.skatteverket.se/foretag/drivaforetag/startaochregistrera/fordigsomvillstartaforetag.4.6e8a1495181dad540842251.html

### X04: Skatteverket employer declaration corrections

Future-pay adjustment and gross recovery differ. Gross recovery can lead to original-period compensation correction when claimed; prior withholding normally stays. Replacements preserve item specification identity. Tax-account changes depend on authority reassessment.

**Observation limit:** Official page read, notably correction and recovery sections. No general recovery/offset legal entitlement is inferred.

Source: https://www.skatteverket.se/foretag/arbetsgivare/lamnaarbetsgivardeklaration/rattaenarbetsgivardeklaration.4.2cf1b5cd163796a5c8b6698.html

### X05: Peppol BIS Billing 3.0

Index identifies May 2026 release; BIS text supplies structured invoice/credit and monetary relationships.

**Observation limit:** Official index and BIS page opened. Exact XSD/Schematron/code-list bundles were not downloaded or qualified.

Source: https://docs.peppol.eu/poacc/billing/3.0/

Related official source: https://docs.peppol.eu/poacc/billing/3.0/bis/

### X06: BankID autostart and signing entry point

App return is not completion evidence; collect is needed. Access requires appropriate provider arrangements/certificates.

**Observation limit:** Autostart/support text available; signing API page returned minimal client-rendered text. No exact signing API schema or signature-verifier qualification is claimed.

Source: https://developers.bankid.com/getting-started/autostart

Related official source: https://developers.bankid.com/api-references/auth--sign/sign

Related official source: https://developers.bankid.com/support

### X07: Bolagsverket digital annual-report workflow

Original signing, company adoption, upload of a faithful copy, authority certification/submission and receipt/registration are distinct. A general representative cannot simply replace the eligible certifier.

**Observation limit:** Official search-rendered pages provided relevant text. Direct opening returned a minimal/challenge response. No actual filing performed.

Source: https://bolagsverket.se/sjalvservice/etjanster/lamnainarsredovisningendigitalt.1663.html

Related official source: https://bolagsverket.se/sjalvservice/etjanster/lamnainarsredovisningendigitalt/saharlamnarduinarsredovisningendigitalt.1667.html

Related official source: https://bolagsverket.se/sjalvservice/etjanster/lamnainarsredovisningendigitalt/vanligafragoromattlamnainarsredovisningendigitalt.1671.html

Related official source: https://bolagsverket.se/sjalvservice/etjanster/lamnainarsredovisningendigitalt/forutsattningarforattlamnainarsredovisningendigitalt.1665.html

### X08: Bolagsverket current service specifications entry point

Provides versioned filing, information, event and checksum services. The packet requires the actual selected service contracts rather than invented routes/statuses.

**Observation limit:** Official search result inspected; exact linked OpenAPI/specification bundles not acquired or exercised.

Source: https://bolagsverket.se/apierochoppnadata/lamnaforetagsinformation/digitalinlamningavarsredovisningochrevisionsberattelse/gallandeservicespecifikationerfordigitalinlamningavarsredovisning.5938.html

### X09: SIE Group format family

Balance/transaction export and voucher transfer are different format purposes. Exact year/dimension/omission grammar must be qualified against the chosen specification.

**Observation limit:** Official format page opened; this work does not certify a new parser or exporter.

Source: https://sie.se/format/

## Not established by this review

Current company registrations, accounting-method eligibility, real employee entitlements, all applicable sick/holiday/loan rules, provider credentials, signed original annual reports, complete schemas and production acceptance are not supplied by these sources. No packet may fill them with a plausible default. Existing source data must never be relabelled synthetic to bypass admission.

## R15: Late branch observation

`4671a2fbaea88bcab613f28b6d34a209b040ab06` was observed after the detailed source review. Its commit reports NEXT-01 implementation and no runtime exercise. See [REVISION-NOTE.md](REVISION-NOTE.md). No full-diff review or independent execution is claimed.


---

<a id="part-32"></a>

# Repository movement during this review

The detailed source review and proposed packet evidence are pinned to `5ac3433e3e75ef7fc0229cbe00107003b63aa32d`.

A later branch read returned `4671a2fbaea88bcab613f28b6d34a209b040ab06`, authored on 26 September 2026 at 11:22:22 UTC. Its commit message reports implementation of NEXT-01 through `cases_resolve_review`, including current correction-bundle ownership, local route selection and no inherited ownership token. The commit reports static checks passing and explicitly says no PostgreSQL/Worker requests were made for its runtime vectors.

This package does not claim to have reviewed the full intervening diff or independently run those checks. NEXT-01 is not reassigned here. NEXT-50 consumes the actual released resolver contract; do not require the old proposed ownershipVersion or other_owner fields if the implemented schema does not supply them. Its execution-time owner checks remain the financial authority.

Before implementing any new packet, reconcile the current HEAD and in-progress ownership claims. This late observation does not silently rebase all source evidence or imply the other first-wave packets are complete.

Source: https://github.com/erik-kroon/openERP/commit/4671a2fbaea88bcab613f28b6d34a209b040ab06
