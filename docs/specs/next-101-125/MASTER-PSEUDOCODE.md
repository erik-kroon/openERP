# OpenERP: NEXT-101 through NEXT-125

Complete fifth-wave application-owned pseudocode specification. This supplements the first 100 packet designs rather than certifying their completion or replacing their remaining work.

Planning checkpoint: `66355b62b23e3b8007c2d324f3739fbbcc96cdc0`, 28 September 2026. The current read was limited to branch and shared operations/contracts, with the attached previous wave used for scope. Specialist external material was checked narrowly. No full source audit, runtime execution, qualified statutory bundle or production acceptance is claimed.

Use the existing Effect application and pure calculation owners, caller-passed transactions, PostgreSQL narrow integrity and persistent Bun/effect-mq delivery. The original reserved owners remain in force. New standing mandates are explicitly opt-in later scope, not a replacement for Book Zero human approval.

## Contents

1. [Shared execution contract](#part-01)
2. [Qualified legal, company and provider inputs](#part-02)
3. [NEXT-101: Accounting-firm delegation and multi-client workspaces](#part-03)
4. [NEXT-102: Scoped evidence requests and response reconciliation](#part-04)
5. [NEXT-103: Versioned balance-sheet substantiation schedules](#part-05)
6. [NEXT-104: Shared-cost attribution across projects and dimensions](#part-06)
7. [NEXT-105: Project margin with billing, recognition and cash bridges](#part-07)
8. [NEXT-106: Service-retainer entitlements and once-only drawdown](#part-08)
9. [NEXT-107: Onerous service-contract provisions and release on performance](#part-09)
10. [NEXT-108: Warranty cohorts, expected claims and provision consumption](#part-10)
11. [NEXT-109: Insurance-loss claims and gross compensation accounting](#part-11)
12. [NEXT-110: Borrowing reschedules, debt forgiveness and amended obligations](#part-12)
13. [NEXT-111: Annual common-cost VAT deduction true-up](#part-13)
14. [NEXT-112: Domestic construction reverse-charge sales and purchases](#part-14)
15. [NEXT-113: EU B2C destination VAT and Union OSS reporting](#part-15)
16. [NEXT-114: EU foreign input-VAT recovery claims and receipts](#part-16)
17. [NEXT-115: Overnight travel allowances and meal-benefit partition](#part-17)
18. [NEXT-116: Recurring car-benefit valuation and employee payment links](#part-18)
19. [NEXT-117: Interest statements: KU20 and applicable KU25 identities](#part-19)
20. [NEXT-118: Prospective salary exchange into pension contributions](#part-20)
21. [NEXT-119: Cash share subscriptions and registered-capital transition](#part-21)
22. [NEXT-120: Preliminary income-tax revisions and authoritative installment schedules](#part-22)
23. [NEXT-121: Opt-in bounded standing posting mandates](#part-23)
24. [NEXT-122: Cash-constrained payment proposals with explicit optimization bounds](#part-24)
25. [NEXT-123: Autogiro mandates and direct-debit collection outcomes](#part-25)
26. [NEXT-124: Bank-feed provider handover with continuity evidence](#part-26)
27. [NEXT-125: Processor refund initiation with reserved entitlement and outcome recovery](#part-27)
28. [Integration and non-overlap](#part-28)
29. [Design decisions](#part-29)
30. [Coordinator handoff](#part-30)
31. [Sources and evidence limits](#part-31)

---

<a id="part-01"></a>

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


---

<a id="part-02"></a>

# Qualified rule, company and provider inputs

Reuse the existing finite rule-release and company-activation owners. Do not build another general rules engine. The pseudocode solves data flow, arithmetic boundaries and state transitions. It does not fabricate the public tables, private agreements or actual business events that make a specific profile valid.

A release records named calculator/adapter versions, exact source/schema checksums, applicability, mandatory inputs, supported/unsupported cases, independent expected examples and review. Activation selects that immutable release for an actual company/date/operation. It does not turn a returned model suggestion into legal truth.

| Packet family | Required additional input |
|---|---|
| 101-102 | Client-granted firm scope, staff assignment, request purpose and permitted recipient evidence |
| 103-105 | Account support templates, independent balance evidence, actual allocation drivers, project scope and explicitly included/excluded costs |
| 106 | Real service-retainer contract, nontransferable unit definitions, original consideration/tax and qualified revenue/refund terms |
| 107-108 | Applicable provision-recognition/measurement rule, actual obligation, complete uncovered exposure and independently reviewed estimate basis |
| 109 | Insurance rights, actual covered loss, sufficient recovery recognition evidence and approved repair/payment relationships |
| 110 | Executed loan modification, exact released obligations, permissible measurement and existing uncertain instructions |
| 111 | Selected common-cost allocation method, source-tax ceiling, direct-cost exclusions, final driver/rounding and correction periods |
| 112 | Actual service/property/buyer qualifications, supplier tax presentation and current correct report mappings |
| 113 | Effective OSS registration and supply family, consumer/place evidence, destination rates, EUR reporting conversion and corrections |
| 114 | Refund-country eligibility/codes, original foreign tax, claim period/attachments and recoverable entitlement measurement |
| 115-116 | Actual travel/meal/vehicle facts, dated tables, employee payments and cash/noncash reporting rules |
| 117 | Actual reporter duty, person/instrument class, paid/available dates, withholding and exact year-specific electronic schema |
| 118 | Signed prospective salary exchange, actual pension agreement, contribution/SLP roles and benefit/absence effects |
| 119 | Actual share resolution/subscription/payment/registration evidence and qualified interim capital/premium classifications |
| 120 | Qualified full-year tax profile, actual-to-date and labelled scenario inputs, genuine preliminary-tax decisions |
| 121 | Explicit human-activated scope, independently verified source pattern, shared limits and released authority/lock contract |
| 122 | Complete cash perimeter, true reservations/holds, permitted dates/partial options and reviewed objective/constraint policy |
| 123 | Actual bank Autogiro agreement, payer mandate evidence, precise notice/file/status/cancellation/return contracts |
| 124 | Independent real-account identity and complete overlap/continuity evidence for both providers |
| 125 | Actual Stripe account/mode/charge/refundability, exact refund state/financial discharge mapping and idempotency/read-back limits |

## Deterministic selection

```text
resolveQualifiedInputs(family, company, caseFacts, semanticDates):
  select immutable releases whose exact applicability predicates match
  none -> MissingQualifiedRelease(family)
  ambiguous -> UnresolvedReleaseSelection
  required fact absent/contradictory -> specific MissingFact/Conflict
  supported profile not implemented -> UnsupportedCase, not fallback to another regime
  return exact release/fact identities and dependency witness
```

No statutory threshold, daily allowance, net/gross treatment or filing field is picked from memory in an activated implementation. Synthetic packet examples intentionally use illustrative amounts. When a specialist family is inapplicable, record the actual fact and scope rather than invoking every new packet before a company can close.

## External guarantees

Provider idempotency retention, exact cancellation support, error meaning, read-back identity and accounting evidence are verified per real adapter. A local command key is not a provider guarantee. Direct-debit marketing about due dates is not final cash evidence. An OSS or tax web-service page does not establish a public programmable endpoint.

A failed schema validation or missing actual outcome remains an explicit gate. Useful local preview/artifact generation can continue independently without calling the external path complete. No captured account, token, signature or invoice in this dossier authorizes a real action.


---

<a id="part-03"></a>

# NEXT-101: Accounting-firm delegation and multi-client workspaces

**Priority when applicable:** P1. **Owner lane:** IDENTITY.

**New scope:** NEXT-98 owns a period review. Add firm membership, client-granted scopes and a multi-client queue without turning a reviewer into a book administrator.

**Existing owner to extend:** Existing verified-principal admission, client memberships, capability registry and review engagements.

**Earlier contracts:** NEXT-50. **This-wave dependencies:** None.

**Conditional:** NEXT-98: a client delegates an accountant period-review engagement.

**Basis:** R02, R03, P98 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Records and authority intersection

```text
FirmMembership {firmId, actorId, role, activeRevision, expiresAt}
ClientDelegation immutable {
  clientEntity, permittedBooks, firmId, grantedOperationFamilies,
  sensitiveDataScopes, periodBounds, permitsStaffAssignment,
  designatedStaffOrAssignmentPolicy, clientAuthorizer, revision, expiry
}
StaffAssignment {delegationId, actorId, permittedSubset, revision, active}
DelegationEvent immutable {grant | narrow | revoke | expire, evidence, recordedAt}
```

A client approves the firm's exact access envelope. Firm administrators may assign only the subset that envelope expressly permits. They cannot extend periods, add a book or turn read/prepare into signing/payment. Payroll and evidence access are separately named. Professional engagement acceptance is not technical delegation or authority to represent the company externally.

```text
resolveDelegatedAccess(actor, targetBook, operation):
  verify current actor credential and active firm membership
  resolve current client delegation and staff assignment
  allowed = operation in intersection(
      clientGrant, firmRole, staffAssignment, periodScope, sensitiveScope)
  require allowed and every layer unrevoked/unexpired
  return Principal(actor, viaFirm, delegationRevision, exactPermissionWitness)
```

Do not synthesize a permanent client operator token or copy firm membership into every client with broader grants. User identity remains the actual human, with delegation provenance appended. Nested domain operations use the resulting scoped principal through existing admission.

## Creation, revocation and lock discipline

An invitation alone creates no client access. The client authorizer chooses an explicit book and permission set, reviews it and activates it through the identity owner. Firm acceptance records contractual participation without widening that set. Initial activation is one client delegation at a time.

The root identity owner defines the lock ordering over credential, firm membership, delegation and assignment before book admission. Exclusive revocation uses that same authority hierarchy without acquiring a financial book lock afterward. If implementation needs new multi-row authority locking, prove the complete ordering before support. Do not bolt a book-first `revokeFirm` onto authority-first financial commands.

An admitted action holding the current authority locks can complete before revocation wins. Revocation that wins first blocks new admission. Already committed financial receipts survive removal of the firm's access; authorized client administrators retain them. A former firm member receives no continued access just because the receipt names them.

## Multi-client overview

```text
captureFirmQueue(actor, selection):
  obtain current authorized delegation IDs under firm identity scope
  fan out bounded, separate READ operations to each permitted client book
  retain book-specific contextId, cutoff, coverage and authorization revision
  aggregate only permitted counters/status summaries
  recheck active permission envelope before returning/retaining a shared view
  on scope loss, remove affected private content; do not return stale client names
```

Each book can have a different cutoff; display that fact. A dashboard is not a consolidated balance sheet. Do not hold a database transaction over every client or execute one cross-book financial batch. Optional firm-wide task actions are individual admitted client commands with separate receipts and partial-progress status.

## UI and operational result

Provide client grant/withdrawal, firm assignment, per-client outstanding tasks and an explicit scope switch. Query keys include firm actor identity, client entity/book and delegation revision. Changing clients cancels stale reads and cannot reattach an old mutation result to a new scope. Existing review98 still controls which period pack was accepted.

Client offboarding produces an inventory of retained review outputs and active delegated delivery jobs. Jobs reauthorize against current client permission; they cannot use a cached employee credential. Offboarding changes no financial balances or external authorizations by implication.

```text
client grants read+prepare; firm gives employee operator role -> still no approval
staff removed during queue capture -> no private client rows in new response
two clients both have invoiceId='x' -> queries remain book-scoped
firm action across10 clients fails on3 ->7 separate receipts, not global atomicity
review engagement accepted but delegation expired -> reads refused
```

Completion requires observed client-to-firm grant, staff use, scope reduction, revocation races and client switching through UI/API. This is a new collaboration control, not a replacement authentication provider.


---

<a id="part-04"></a>

# NEXT-102: Scoped evidence requests and response reconciliation

**Priority when applicable:** P1. **Owner lane:** EVIDENCE.

**New scope:** Add an explicit request/reply workflow for missing facts or documents. Search, upload and a review finding alone do not say who was asked, what they supplied or whether the request was satisfied.

**Existing owner to extend:** Existing source occurrence/inbox, permission-scoped sharing and review-case owners.

**Earlier contracts:** NEXT-26, NEXT-65, NEXT-93, NEXT-98. **This-wave dependencies:** None.

**Conditional:** NEXT-101: the requester uses firm-to-client delegated access.

**Basis:** R02, P93, P98 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Request contract

```text
EvidenceRequestRevision {
  id, book, originatingCaseRefs, recipientIdentity, requestedItems,
  permittedPurpose, accountingPeriod, deadline, revision, supersedes?
}
RequestedItem {
  stableItemId, question, acceptableEvidenceKinds,
  requiredFactSchema, sourceRelationship, privacyClass
}
ReplyEnvelope immutable {
  requestId, requestRevision, authenticatedOrVerifiedResponder,
  receivedAt, originalMessageRef, retainedOccurrenceIds, assertedFacts
}
ItemResolution immutable {
  requestItemId, replyRefs, reviewer, outcome: satisfied|partial|rejected|waived,
  acceptedFactRefs, remainingQuestions, evidenceDigest
}
```

Request state distinguishes sent, viewed if evidenced, replied, reviewed and resolved. A file arriving is not proof that every question is answered. A waiver preserves the missing/failed requirement and can never masquerade as verified evidence in a mandatory accounting check.

## Prepare and send

Capture the exact originating case and missing fields, then prepare a minimized message with recipient scope and a revocable request-specific upload token. The token permits only viewing this request's authorized content and submitting replies; it confers no book search, ledger read or posting authority. Mask private salary/party details unless necessary and explicitly permitted.

Use the existing authorized delivery/outbox for the message. Persist attempt identity before network I/O. An unknown delivery outcome is not a reason to create another request ID. A reminder references the same request revision, not a new obligation. Redaction happens before message sealing, not as mutable view-time replacement of approved bytes.

## Receive and link without automatic fact confirmation

```text
acceptReply(requestToken, envelope):
  authorize token, intended recipient and current request visibility
  retain original message and files with safe media/size handling
  do not execute document macros or obey instructions embedded in attachments
  in short application tx:
    replay exact message/source identity
    append reply-to-request relationship and source occurrences
    label matches to requested items as proposed
    queue supported extraction through NEXT-26
```

A legitimate duplicate byte file can answer more than one distinct evidence purpose while sharing content storage. Economic recognition remains with the financial owner. Source revision or email routing alone cannot move evidence into another client's book.

```text
reviewReply(request, selectedItems, decision):
  capture original item requirements, reply revisions and current case facts
  compare actual supplied facts/documents with each required field and period
  preserve partial, contradicted and unrelated replies explicitly
  reviewer selects the accepted evidence and resolves discrepancies
  App tx:
    recheck request/item/reply/case revisions and current reviewer authority
    append item decisions and accepted fact references through owning fact operations
    update the original case only for the exact fulfilled requirements
    store receipt; do not post, approve a financial plan or auto-close period
```

When a request is revised, old replies remain linked to the old questions. They can be explicitly adopted to a new item if semantically applicable; the app does not silently mark new questions answered. A later invalidation of accepted evidence reopens the affected case/current readiness while retaining the prior resolution.

## Workspace and vectors

Show request items beside original replies, provenance, extraction suggestions and accepted decisions. The firm/client queue can group identical missing facts without merging distinct evidence scope. A private respondent sees only their own request; an authorized accountant can see case effects across selected items.

```text
asked invoice and business-purpose explanation; only invoice uploaded -> partial
new request adds foreign-establishment fact -> old reply does not satisfy it
recipient token revoked after upload -> retained authorized evidence survives,
    new request views/submissions denied
same inbound message retried -> one reply envelope and original occurrences
review accepts a document already used in purchase -> no new expense or payable
```

Completion includes one real UI request, retained response, reviewed fact/case resolution and uncertainty/revocation recovery in an authorized environment. Message delivery and accounting completeness are independently evidenced.


---

<a id="part-05"></a>

# NEXT-103: Versioned balance-sheet substantiation schedules

**Priority when applicable:** P1. **Owner lane:** REVIEW.

**New scope:** Add per-account explained balance schedules and preparer/reviewer certification. This supports an existing close/review; it is not another close certificate or journal reconciliation engine.

**Existing owner to extend:** Existing immutable report snapshots, financial contribution identities and independent evidence/review owners.

**Earlier contracts:** NEXT-13, NEXT-23, NEXT-95, NEXT-98. **This-wave dependencies:** None.

**Conditional:** NEXT-102: missing supporting evidence is requested from a client.

**Basis:** R03, P13, P98 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Schedule basis

```text
SubstantiationTemplate {
  accountRoleOrSelectedAccounts, purpose, requiredEvidenceKinds,
  allowedSupportRelations, ageingRules, independentControlRequirements
}
ScheduleRevision immutable {
  templateVersion, ledgerSnapshotId, balanceDate, recordedCutoff,
  sourceContributionSet, supportLines, unassignedContributionIds,
  independentControlRefs, explanations, preparedBy, digest
}
SupportLine {
  id, economicItemRef, signedAmount, originalCurrency?, bookCarrying,
  attributionShares, evidenceRefs, dueOrReleaseDate?, reviewState
}
ScheduleReview {revisionDigest, reviewer, acceptedScope, unresolvedExceptions, recordedAt}
```

Only the existing GL/report owner supplies the balance. An AP or asset subledger adapter contributes its original item identities, not a second mutable control total. A manually created support line must explicitly distinguish an explanation from independently substantiated value. A manager's assertion is labelled as such.

## Construct and validate

```text
prepareSubstantiation(accountSelection, date):
  capture exact opening/movement/closing contribution identities at one cutoff
  load supported subledger items and independent statement/contract evidence
  map each selected amount to item-level support with exact shares
  reject duplicate physical GL amounts counted under several support lines
  compute:
    explained = sum(valid signed support shares)
    unexplained = authoritativeClosing - explained
    staleEvidence, missingItems, unexplainedRows, unsupportedAllocations
  retain unmatched offsetting rows even when unexplained net is0
  seal complete source membership and template/version
```

For a grouped control account, require each support item's sign and currency/carrying convention to match the role. Positive supplier credits and negative payables may need separate presentation lines rather than hiding behind a net balance. Cross-currency native quantities do not sum into a meaningless total.

A support amount can be split across evidence items only when shares conserve the original component and each relationship is meaningful. Multiple documents corroborating the same receivable increase provenance, not amount. Imported openings require their actual retained basis; no source is invented for an unexplained opening.

## Acceptance is scoped and nonfinancial

```text
reviewSchedule(revision, reviewerDecision):
  recheck exact revision and required reviewer permission/segregation
  require mandatory controls observed and accepted support types
  unresolved material item => qualified exception/refusal, not silently removed
  append review of this specific schedule and cutoff
  notify existing period-review/close owner of the result
  never create an adjusting journal or declare the whole company complete
```

Currentness uses account-specific content and supporting evidence revisions. A new posting to another unrelated account need not invalidate it. A backdated item affecting the selected balance does. Prior accepted revisions remain readable even when current readiness becomes stale.

The schedule can propose a named owned adjustment for a genuine supported discrepancy. It cannot post an arbitrary plug equal to the unexplained difference. Adjustments flow through their domain owner with new approval, then a fresh substantiation revision explains their receipt.

## Interface and evidence

An accountant chooses the balance date and template, sees source items and documents, requests missing support and reviews the complete schedule. Exports use the same fixed rows and review status. A reviewer can restrict the acceptance to a specific account rather than pretending every connected account is substantiated.

```text
closing100000; supported75000+15000 -> unexplained10000 remains
closing0 with unexplained+5000 and-5000 -> not complete
two PDFs prove same receivable20000 -> support20000, not40000
source confirmation from wrong year -> retain reply but reject support relation
new valid posting later recorded for old period -> previous report unchanged,
    current substantiation stale until recaptured
```

Independent evidence is genuinely independent of the computed ledger total where the template requires it. Generating a second report from the same journal does not establish external completeness. Completion includes capture, review, stale-change detection and reproducible exported evidence through the existing workbench.


---

<a id="part-06"></a>

# NEXT-104: Shared-cost attribution across projects and dimensions

**Priority when applicable:** P1. **Owner lane:** REPORTING.

**New scope:** NEXT-43 changes analytical labels. Add conserved fractional attribution of one shared cost to several recipients without duplicating costs or modifying the financial journal.

**Existing owner to extend:** Existing original/reviewed dimension histories and report contribution owner.

**Earlier contracts:** NEXT-13, NEXT-14. **This-wave dependencies:** None.

**Conditional:** NEXT-43: the selected analytical view uses reviewed classification revisions.

**Basis:** R03, P14, P43 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Explicit analytical scope

Start with management-cost attribution, not tax allocation or intercompany recharging. A reviewed allocation may help project profitability, but does not change legal deduction, account identity, company total or original journal dimensions.

```text
AllocationRuleRevision {
  scope, sourceCostSelector, recipientSet, driverKind,
  driverEvidence, effectiveInterval, roundingPolicy, costDefinition
}
AllocationSnapshot {
  ledgerBoundary, classificationCutoff, ruleRevision,
  physicalSourceComponents, exactDriverValues, allocationRows, unresolvedItems, digest
}
AllocationRow {
  originalComponentId, recipientId, signedAttributedAmount,
  weight, totalWeight, residualRank, sourceEvidence
}
```

Use already recognized expense cost, which includes only the appropriate non-deductible tax. Paid cash, asset acquisition capital and expense amortization are different costs. A single source component cannot appear both in a direct-cost result and its full shared-pool result in the same report basis.

## Calculation and residuals

```text
allocateSharedCost(basis, rules):
  require each source component belongs to one compatible selected attribution rule
  require drivers complete, exact and independently evidenced for chosen period
  for source component s:
    sign = sign(s.expenseAmount)
    shares = allocate(abs(s.expenseAmount), nonnegative recipient weights)
    rows = sign*shares with exact source identity
    require sum(rows.amount)==s.expenseAmount
  retain explicit unallocated bucket for unsupported/missing drivers
```

Zero total driver is not an instruction to use equal allocation automatically. Require a reviewed fallback or show unallocated cost. Stable ID tie-breaking ensures reproducible minor-unit residuals, not a claim of economically perfect allocation. Select the actual reviewed method by source/period.

```text
composeProjectExpense(reportMode):
  for every physical expense component:
    choose EITHER direct assignment EITHER its selected allocation rows
    not both
  aggregate by recipient and cost category
  require all recipients + unallocated == included expense universe
```

Separate allocation layers may redistribute support-department cost only under an explicit acyclic sequence. The initial profile disallows circular allocations and arbitrary equations. A later stage consumes the prior stage's attributed rows as lineage, not another copy of original expense in the final total. No hidden reciprocal-cost solver is introduced.

## Retain and revise

Application capture retains fixed source membership, exact driver revisions and current classification mode. Pure calculation produces rows, then a short transaction rechecks the relevant basis and saves the immutable snapshot. Approval of analytical use is separate from financial posting; nothing invokes the journal writer.

A driver correction creates a new allocation snapshot and exact before/after attribution bridge. Old reports retain old amounts. An expense credit carries a negative source component and either references the original allocation basis or a newly reviewed period method; do not silently change original shares with today's headcount.

## UI and output

Provide a driver worksheet, source-pool preview, allocated/unallocated reconciliation and click-through to original entries. Payroll cost drivers require appropriate private permissions or a separately approved aggregate input, not raw employee salary in project-manager context. Cross-book allocations remain unsupported; a firm/client dashboard cannot redistribute one company's expense into another.

```text
shared cost10001, driver A1/B2 -> A3334 B6667; total10001
same source also tagged A -> direct line suppressed in allocated view,
    original unallocated view remains available
missing B driver -> incomplete/unallocated, not A receives100%
credit-10001 with original driver basis -> -3334/-6667
two allocation rules both claim source -> ambiguity refusal, not twice the cost
```

Completion means the allocated report reconciles to the chosen unallocated report at the same source cutoff, with preserved original classifications and independent driver evidence. This is not a tax return allocation or a new writable cost ledger.


---

<a id="part-07"></a>

# NEXT-105: Project margin with billing, recognition and cash bridges

**Priority when applicable:** P1. **Owner lane:** REPORTING.

**New scope:** Add a coherent project-performance snapshot combining contract rights, earned revenue, allocated cost and actual cash. It does not replace P&L, Cash forecasts or contract recognition.

**Existing owner to extend:** Existing sales coverage, deferred/unbilled revenue, time billing, cost contribution and cash-settlement readers.

**Earlier contracts:** NEXT-13, NEXT-58, NEXT-77, NEXT-79. **This-wave dependencies:** NEXT-104.

**Conditional:** NEXT-78: milestone/retention balances enter the selected project.

**Basis:** R02, P77, P79 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Distinct measures

```text
ProjectSnapshot {
  projectIdentity, financialCutoff, commercialCutoff,
  contractRevisions, issuedInvoices, credits,
  recognizedRevenueComponents, deferredBalances, unbilledBalances,
  directCostRows, sharedCostAllocationSnapshot,
  actualReceipts, actualCostPayments, unallocatedCrossProjectItems,
  remainingCommitments, knownUnperformedScope, coverageDiagnostics
}
```

Use book-currency values with explicit conversion/carrying basis. Contract value, billed net, accounting revenue, cash receipts and invoicing opportunity are five different fields. Gross receipts include tax and cannot be subtracted from net expense to label a profit measure.

## Derive without double counting

```text
calculateProject(snapshot):
  billings = issued net - legal credit net
  revenue = sum(existing revenue owner's included source components)
  directCost = sum(once-only actual expense components attributed directly)
  sharedCost = sum(selected NEXT-104 attribution rows)
  margin = revenue - directCost - sharedCost
  marginRatio = margin/revenue when revenue!=0 else NotApplicable

  billedNotYetEarned = exact existing deferred-revenue owner balance
  earnedNotYetBilled = exact unbilled/contract-asset owner balance
  billingToRevenueBridge = classified differences between billings and revenue
  require every difference has owned timing/credit/adjustment lineage
```

A simplified initial balance equation may be `revenue = billings + change(unbilled) - change(deferred)`, but it is used only when the complete bridge classifies all contract modifications, credits and direct-recognition effects. Do not force that identity by adding an unexplained “other” plug. Raw movements, not ending balances alone, support it.

Time entries used for billable revenue estimation are not automatically payroll expense. Payroll/contractor costs need actual recognized contribution links. A work item already included in unbilled revenue cannot become new revenue again when invoiced. Its billing coverage is consumed through NEXT-77/79.

```text
cashView:
  display actual project-linked receipts and payments with tax and allocation treatment
  unresolved multi-project payments stay unallocated
  do not infer all invoices collected because one project receipt equals their sum
```

Forecasted remaining margin is an optional separate scenario with explicit remaining-cost and pricing assumptions, not historical profit. Future staffing estimates never enter the actual expense table. Revenue recognition and contract-loss decisions remain at their financial owners.

## Capture and controls

Capture each domain at a common recorded/ledger cutoff where its model supports that cutoff. If commercial information has a later revision, label the mixed context and avoid claiming a fully synchronized accounting snapshot. Persist exact membership and formulas, including whichever analytical dimension mode was selected.

At company level, projects plus unassigned reconcile to the selected financial universe, not necessarily every statutory P&L line. Show excluded taxes, central costs or nonproject operations explicitly. Shared-cost allocation is already deducted once from the source/direct view. A single physical GL line cannot be in two complete-cost totals.

## UI and access

Provide Overview, Revenue bridge, Cost detail, Billing opportunity and Actual cash tabs over the same saved snapshot. Sensitive cost details use scoped aggregated projections; an actor allowed to see margin is not automatically allowed to see individual payroll. Recheck permission when exporting or opening original evidence.

```text
billings80000, unbilled movement+10000, deferred movement-5000
  => qualified bridged revenue95000
recognized direct cost40000, shared10000 -> margin45000
cash receipts60000 do not change recognized revenue95000
missing project assignment on expense5000 -> unassigned diagnostics retained
revised staffing estimate -> new forecast, no historical margin edit
```

Completion includes reconciliation and drilldown across actual owners, not a dashboard summing unrelated endpoints at different times. Report “unknown” when a required owner or allocation is unavailable rather than hiding missing cost and inflating margin.


---

<a id="part-08"></a>

# NEXT-106: Service-retainer entitlements and once-only drawdown

**Priority when applicable:** P1. **Owner lane:** COMMERCE.

**New scope:** Add unit-denominated contractual service rights and consumption against prepaid retainers. Customer advances track money; recurring invoices track billing dates; neither alone tracks remaining service entitlement.

**Existing owner to extend:** Existing accepted contract, work coverage, advance/deferred-revenue and billing-capacity owners.

**Earlier contracts:** NEXT-56, NEXT-58, NEXT-76, NEXT-77. **This-wave dependencies:** None.

**Basis:** R02, P56, P77 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Scope and retained buckets

The first profile is a named customer's nontransferable entitlement to a defined service at an explicit tax/recognition treatment. This is not a transferable gift-card currency, third-party voucher platform or cash wallet. If the arrangement requires another voucher tax scheme, refuse this profile.

```text
RetainerBucket {
  contractId, customerId, serviceKind, exactGrantedUnits,
  unitDefinition, serviceWindow, cashRefundTerms,
  purchaseInvoiceOrAdvanceRef, netConsiderationBasis,
  existingRevenueOwner, rateAndTaxWitness
}
EntitlementEffect immutable {
  bucketId, grant | accepted_use | release_unused | refunded | corrected,
  sourceWorkIdentity, unitDelta, considerationRelease,
  journalRefs?, creditOrInvoiceRefs?, receipt
}
```

Retainer rights and financial liabilities have different units and owners. A paid receipt can support many service units, but cannot produce another advance liability here if NEXT-56 already recorded it. A bucket referring to already recognized revenue has no remaining deferred-revenue authority; its units may still be operationally tracked under a separately explicit recognition profile.

## Drawdown calculation

```text
prepareRetainerUse(bucket, acceptedWork):
  require work already accepted under its contract and not billed/consumed elsewhere
  q = supported exact service units for this work
  require q>0 and q<=remainingEntitlement
  require within permitted service window or explicit reviewed extension
  C = bucket net consideration subject to this qualified use-based recognition
  release = cumulativeRelease(C, grantedUnits, priorConsumedUnits, q)
  require financial release <= existing deferred consideration remaining
  return workCoverage, unit consumption, release and exact existing-owner refs
```

If a work item exceeds remaining units, split it explicitly into covered and separately billable parts before approval. An implicit negative entitlement or whole extra invoice is not allowed. Use the existing work-coverage authority so a timesheet cannot be charged once through NEXT-77 and again through a retainer.

```text
executeRetainerUse(plan): OwnedTx
  replay and verify bucket, work, contract and deferred-revenue versions
  validate exact qualified use-based recognition and authority
  debit deferred revenue liability release
  credit service revenue release
  call existing deferred-revenue writer with this same tx
  record entitlement/work-capacity consumption and receipt together
  create no new cash, receivable or VAT solely because prepaid service was used
```

Where the qualified revenue policy is time-based or performance-based rather than units used, the first profile refuses financial drawdown and retains operational use only. It does not override NEXT-58's schedule to accelerate revenue.

## Amendments, expiry and refund

Top-ups create a new funded bucket with its own price/tax facts and contractual priorities. Do not add units to an old bucket while retroactively changing the cumulative price paid per consumed unit. A first-expiring-first-use suggestion is a reviewed product policy, not permission to move value between different customers or service classes.

Expiry disables new service use only under the contract's actual terms. It does not automatically make remaining liability income. Breakage, extension or refund requires its qualified decision and the existing revenue/credit owner. A refund consumes unused entitlement and its exact monetary rights once, with original tax corrections where required. Previously earned revenue is corrected only if the reviewed facts justify it.

A reversal after later bucket use needs a complete supported capacity/consideration adjustment. Never delete old consumption or restart its occurrence counter. Preserve original invoices, service evidence and remaining rights in portal views.

```text
600 service minutes, net100000 deferred, use150 -> release25000, remaining450/75000
second work attempts same150 source identity -> AlreadyApplied
another600-minute top-up net120000 -> separate rate bucket, no repricing first150
expired remaining450 without qualified income decision -> liability stays75000
extra200-minute work with150 remaining -> explicit150-covered/50-billable split
```

Completion includes a real accepted-work-to-entitlement-to-revenue path, shared billing conflict refusal and retained rights in client/accountant views. A number called credits in a UI is not financial or service authority.


---

<a id="part-09"></a>

# NEXT-107: Onerous service-contract provisions and release on performance

**Priority when applicable:** P2. **Owner lane:** SCHEDULES.

**New scope:** Add reviewed loss obligations on remaining service contracts. Project margin is a report and unbilled revenue is an asset; neither records a qualified future unavoidable loss.

**Existing owner to extend:** Existing contract, provision/adjustment posting, purchase/payroll expense and financial-close owners.

**Earlier contracts:** NEXT-13, NEXT-76, NEXT-79. **This-wave dependencies:** NEXT-105.

**Conditional:** NEXT-42: a related asset impairment assessment must precede contract-loss recognition.

**Basis:** R03, P76, P79 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## A specific obligation, not a forecast loss journal

```text
ContractLossAssessment {
  contractRevision, remainingCoverage, measurementDate,
  unavoidableFulfilmentCosts, enforceableExitCost?, futureEconomicBenefits,
  costEvidence, relatedAssetAssessments, recognitionPolicyRelease,
  supportedUnavoidableCostTarget, eligibleProvisionTarget, digest
}
ContractProvisionEffect {
  assessmentId, recognition | remeasurement | covered_loss_release,
  signedLiabilityChange, coveredObligationComponent,
  actualPerformanceRefs?, journalRefs, receipt
}
```

A negative sales forecast or discretionary future budget is not enough. Establish the actual contractual obligation, permissible exit rights, remaining performance scope and the applicable framework's measurement rule. The first profile handles short-duration supported service obligations without material discounting. Disputes, legal uncertainty or unsupported long-term measurement remain explicit gates.

## Measurement

```text
compileContractProvision(basis, qualifiedDecision):
  remainingBenefits = evidenced benefits attributable to remaining contract coverage
  fulfilCost = exact supported unavoidable cost estimate for that same coverage
  if the activated rule permits an enforceable exit alternative:
    unavoidable = min(fulfilCost, independently evidenced exitCost)
  else:
    unavoidable = fulfilCost
  require related asset loss already treated where the rule requires it
  target = qualifiedRule.recognizableLoss(unavoidable, remainingBenefits, facts)
  require target>=0 and complete nonduplicated cost/benefit membership
  current = prior recognized provision - explicit consumed/released effects
  delta = target-current
  addSigned lossExpense +delta
  addSigned contractProvisionLiability -delta
```

The familiar `max(unavoidable-benefits,0)` is used only by a released profile that permits it. A forecast engine may calculate that number for review, but cannot activate recognition. Already recognized liabilities, asset impairments and costs cannot also appear as an unrecorded remaining loss without a documented bridge.

## Release against actual covered loss

```text
prepareCoveredRelease(actualPerformance, activeProvision):
  link completed coverage and actual cost/revenue effects to the original assessed component
  calculate qualified consumed-loss share using its retained coverage/rule
  require share<=remaining supported provision component
  debit provision liability share
  credit provision-loss/released-cost role share under the selected presentation policy
  preserve original actual expense and revenue journals
```

Do not release the full gross supplier invoice against a reserve for only the contract's net loss. Costs are still recognized by purchase/payroll owners. The provision release prevents expensing the same loss a second time, with transparent source relationships. If the next estimate changes, calculate its new target after this release rather than applying both old and new complete provisions.

Execution binds contract, assessment, coverage and prior provision versions. Journals, used-coverage effects, updated provision projection and receipt share one tx. A real termination payment is a separately evidenced settlement under its exact obligation; no cash is invented by recognizing the estimate.

## Controls and examples

Reports show initial obligation, revised estimates, covered performance, releases and remaining provision by contract. A subsequent estimate change creates a new dated assessment. No old close or estimate is edited. Tax deductibility is separately mapped by NEXT-22, not inferred from the book expense.

```text
qualified remaining costs260000, benefits200000 -> target provision60000
half completed: actual cost130000/revenue100000, eligible loss share30000
  => provision debit30000, released loss credit30000; remaining30000
new qualified remainder costs125000, benefits100000 -> target25000,
  delta-5000 against remaining30000, not another25000 credit
forecast loss but no qualifying obligation -> review only, journal0
```

This is a conditional accounting expansion, not a source-defect claim or a universal K2/K3 rule. Independent qualified recognition evidence is required before the proposed financial path can be used.


---

<a id="part-10"></a>

# NEXT-108: Warranty cohorts, expected claims and provision consumption

**Priority when applicable:** P2. **Owner lane:** SCHEDULES.

**New scope:** Add an assurance-warranty obligation and claim-cost lifecycle. A customer refund, billed service warranty or asset impairment is not the same liability.

**Existing owner to extend:** Existing sale occurrence, purchase expense and supported provision posting owners.

**Earlier contracts:** NEXT-03, NEXT-13, NEXT-51. **This-wave dependencies:** None.

**Basis:** R03, P51 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Bounded cohort model

The first profile covers an actual assurance-type obligation attached to supported sales/services and a qualified expected-cost method. Separately sold warranty services follow contract/deferred revenue instead. Product insurance, discretionary goodwill and unsupported contingent liabilities are outside this initial profile.

```text
WarrantyCohort {
  coveredSaleComponentIds, termsRevision, coverageInterval,
  unitsOrCoverageMeasure, qualifyingObligationEvidence
}
WarrantyEstimateRevision {
  cohortId, independentClaimPopulation, frequency/severityBasis,
  currentRemainingCoverage, expectedCost, ruleRelease, assessmentDate
}
WarrantyClaim {
  cohortId, customer/sourceIdentity, supportedEntitlement,
  actualRepairOrCompensationRefs, expectedOutstandingCost,
  reviewedDeductibility, state
}
WarrantyEffect {recognition | actual_cost_consumption | remeasurement | release, journalRefs}
```

Retain the complete source population used for estimate frequency and severity. A warranty budget chosen by management is not automatically a recognizable liability. A zero past-claims sample is not evidence zero future obligation. Where an actuarial or specialist measurement is required, retain that reviewed result and its limits rather than invent probabilities.

## Estimate and posting

```text
calculateWarrantyTarget(coverage, estimateRelease):
  for homogeneous supported cohort segment:
    expected = eligibleRemainingUnits * qualifiedClaimProbability * qualifiedMeanCost
    retain exact rational intermediate and uncertainty evidence
  apply the profile's aggregation, discounting/refusal and rounding boundaries
  exclude costs already satisfied or separately recognized with explicit coverage links
  return supportedTarget with complete inputs

prepareWarrantyAdjustment(target):
  current = initial provision + prior remeasurements - actual releases
  delta = target-current
  debit warranty expense delta
  credit warranty provision delta
```

No rate or expected frequency in this packet is a legal standard. The activated rule defines what uncertainty and obligation evidence suffice. If that profile does not allow the computed expected-value method, it cannot be selected merely because the calculator produces a balanced entry.

## Actual warranty performance

For a repair invoice already recorded by NEXT-03, claim resolution can release the qualified covered cost from the provision through a linked reclassification. Deductible tax remains with the purchase owner; it is not included in warranty expense merely because the invoice gross was paid.

```text
resolveWarrantyCost(claim, actualExpenseComponents):
  C = supported net cost plus non-deductible tax for this actual claim
  P = min(C, remaining eligible provision consumption assigned to claim)
  debit warranty provision P
  credit warranty-cost expense P
  preserve original purchase expense/tax and payable
  actual cost exceeding P remains current expense and informs a fresh estimate
```

When actual repair and provision consumption are approved together, use the same transaction and private purchase/provision writers. If the invoice already exists, adopt its exact cost components and post only the provision release. Never pay the customer or repairer from a mere claim-status transition.

Cash compensation requiring a legal credit/refund uses the correct original-sale tax and liability owner. It cannot be treated as a tax-free repair expense automatically. One actual cost is consumed by at most one claim/provision relationship.

## Claim closure, controls and vectors

A rejected claim does not erase evidence or change the cohort estimate without a reviewed measurement. Expiry of contractual coverage triggers assessment; it is not a blanket release while known unresolved covered claims remain. Outstanding disputes/claims stay in the target population. Closed-period estimate changes follow the supported adjustment-date policy and preserve original snapshots.

```text
synthetic100 covered units * probability1/20 * cost10000 -> target50000
actual qualified repair cost12000 -> release12000, provision38000
remaining expected target40000 -> new expense/provision2000
same repair invoice linked to two claims -> duplicate coverage refusal
separately sold service warranty payment -> route to revenue owner, not provision shortcut
```

UI shows covered sales, known claims, estimate basis, costs paid versus incurred and the liability rollforward. Completion requires actual purchase/claim/provision/control integration, not a spreadsheet value called reserve.


---

<a id="part-11"></a>

# NEXT-109: Insurance-loss claims and gross compensation accounting

**Priority when applicable:** P2. **Owner lane:** COMMERCE.

**New scope:** Add insured-loss claims, recognized recoveries and insurer-to-repairer settlements. Insurance compensation is not ordinary sale proceeds or a grant and must not hide gross damage/repair effects.

**Existing owner to extend:** Existing damaged-asset disposal/impairment, purchase recognition, receivable and payment owners.

**Earlier contracts:** NEXT-03, NEXT-13, NEXT-19. **This-wave dependencies:** None.

**Basis:** R03, P19 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Retained loss and claim identities

```text
InsuredLoss {
  incidentId, affectedAssetOrExpenseComponents, incidentDate,
  originalEvidence, policyRevision, insurerIdentity, claimReference
}
ClaimDecisionRevision {
  claimedAmount, acceptedAmount, currency, deductibleOrExclusions,
  recognitionEligibility, evidence, expectedPaymentDate, previousDecision
}
RecoveryEffect {
  claimId, kind: recovery_recognized | amended | cash_received | direct_settlement,
  entitlementChange, settledAmount, journalRefs, providerEvidence, receipt
}
```

The loss event and insurer recovery have separate recognition dates and evidence. Filing a claim or receiving an automated claim number does not establish a recoverable receivable. The first profile requires a qualified accounting recognition decision supported by an actual accepted entitlement or other sufficient evidence under the selected rule.

## Gross recognition and changes

```text
prepareInsuranceRecovery(loss, decision):
  require insurer/legal entity/currency and covered incident identified
  require loss/cost/asset effects already represented or explicitly pending at their owner
  T = qualified recognized claim entitlement, not management's requested amount
  currentTarget = effective recognized claim entitlement
  delta = T-currentTarget
  debit insurance receivable delta
  credit qualified recovery-income or permitted separate recovery role delta
  retain coverage references; do not reverse original impairment/repair cost
```

An insurance deductible reduces the approved recovery or reflects a separate retained cost, not a second expense merely because both the policy and repair invoice mention it. A repair's recoverable input VAT can affect the insurer settlement basis without changing the invoice's legally determined deduction. Do not derive VAT treatment from the insurer amount.

A downward revised entitlement after prior cash settlement can create an insurer repayment liability. It is not a negative receivable left hidden in a nonnegative schema. The initial workflow must either support that explicit liability/recovery or refuse the consumed-history adjustment with a complete impact list.

## Cash and direct settlement

```text
recordInsurerCash(claim, actualBankReceipt):
  require amount<=remaining eligible receivable or explicitly classified excess
  debit bank amount
  credit insurance receivable amount
  consume claim settlement capacity and source payment once

recordInsurerPaysRepairer(claim, supplierInvoice, evidence):
  require enforceable same covered payment and both obligations outstanding
  debit supplier payable amount
  credit insurance receivable amount
  consume supplier payable AND claim capacity on one tx
  company bank movement =0
```

The repair invoice is still recognized once at its actual purchase/tax terms. Direct insurer payment is a noncash discharge linked to independent proof, not a second invoice expense or an unverified note marked paid. Any remainder due to the supplier stays outstanding.

If the insurer replaces an asset in kind or owns the salvage, the rights and valuation require a separate supported policy. Do not treat a replacement asset as a free addition at the old acquisition cost. The existing asset owner decides disposal and new recognition with actual evidence.

## Application and controls

Prepare from a consistent loss/claim/invoice/source basis, then validate exact decision versions, economic identities and current approval at execution. Journal, receivable/payable effects, independent source usage and receipt commit together. External insurance portal correspondence occurs outside that transaction and carries no authority by itself.

Show original loss, claim demand, qualified recognized entitlement, actual receipts, insurer direct payments and pending disputes separately. Reconcile claim receivables to their GL role and affected supplier balances. A report may present gross loss and recovery with a disclosed relationship; it cannot simply delete both because they approximately net.

```text
asset carrying50000 written off by asset owner; recognized compensation40000
  => independent loss50000 and recovery income40000, net economic loss10000
repair AP12500; insurer entitlement10000 paid directly to repairer
  => AP debit10000, insurance AR credit10000, AP remainder2500, bank0
claim requested50000 but unaccepted/uncertain -> no automatic AR50000
same insurer bank receipt imported twice -> one recovery allocation
```

This is the insured company's accounting, not insurance underwriting or a lending product. Legal recognition, payout rights and tax treatment are qualified inputs, not consequences of the claim's UI status.


---

<a id="part-12"></a>

# NEXT-110: Borrowing reschedules, debt forgiveness and amended obligations

**Priority when applicable:** P2. **Owner lane:** TREASURY.

**New scope:** Extend existing loan principal/interest with evidenced rescheduling and extinguishment. Merely editing a rate or due date must not erase debt or create an unsupported modification gain.

**Existing owner to extend:** Existing borrowing agreement, principal/interest effect history and payment instruction owners.

**Earlier contracts:** NEXT-32, NEXT-71. **This-wave dependencies:** None.

**Conditional:** NEXT-22: a book gain or cost needs separate corporate-tax treatment.

**Basis:** R02, P32 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Selected profile and distinctions

Start with a same-currency ordinary borrowing whose qualified accounting policy permits the supported modification treatment. Complex effective-interest instruments, debt-to-equity exchanges, derivatives, linked new financing and unqualified fair-value calculations are refused. This is borrower accounting, not a credit product offered to others.

```text
LoanAmendmentDecision {
  originalAgreementRevision, legallyEffectiveDate,
  kind: schedule_only | rate_change | principal_forgiveness | interest_forgiveness,
  signedCounterpartyAgreement, revisedTerms, specificReleasedComponents,
  measurementPolicy, outstandingInstructionRefs, economicIdentity
}
LoanAmendmentEffect {
  decisionId, oldRevision, newRevision, principalDelta, interestDelta,
  gainOrExpenseComponents, futureScheduleRevision, journalRefs, receipt
}
```

A proposal from a lender or an unanswered negotiation is not an effective release of liability. The amendment identifies exactly which principal or accrued interest is discharged, not simply a target lower monthly payment.

## Compute each supported effect

```text
compileLoanAmendment(basis, decision):
  require effective executed agreement, supported policy and exact current obligations
  if schedule_only:
    require sums and entitlement unchanged except explicit dates
    journal=[]; preserve principal and accrued interest
  if rate_change:
    split future accrual timeline at the contractually effective date
    calculate any authorized accrued-interest correction through NEXT-32
    do not assume every rate change implies a present-value gain
  if principal_forgiveness:
    F = exact enforceably released outstanding principal
    require 0<F<=principalRemaining
    debit loan principal liability F
    credit qualified debt-release gain F
  if interest_forgiveness:
    H = exact released interest already accrued
    require H<=recognized interest remaining
    debit accrued interest liability H
    credit qualified interest reversal/gain role H
    future unaccrued interest removal is a schedule change, not income recognized today
```

The book income role and tax treatment are separate decisions. No universal percentage test decides substantial modification here. If the activated framework requires a derecognition/present-value method not implemented by the selected case, return that specific unsupported measurement before producing a financial plan.

Fees charged for the amendment are separate evidenced costs or capitalization under a qualified profile. They are not silently deducted from principal forgiven or automatically expensed without review. Future interest uses the revised principal timeline and terms, avoiding interest on forgiven balances after the effective date.

## Payment and concurrency boundary

Capture every admitted/exported repayment instruction affected by new terms. Unknown old instruction outcomes cannot be discarded when reducing a payment schedule. Before new instructions are prepared, require existing reservations resolved under NEXT-08/71 or explicitly preserved as still capable of execution. A reduced debt plus later executed old cash payment may create a lender receivable; do not hide it by clamping principal to0.

`executeLoanAmendment` rechecks agreement versions, principal/interest capacities, effective dates and payment-reservation inventory. It posts any journal and appends revised terms/schedule/effects in the same book transaction, with immutable receipt and Cash/currentness events. An unposted pure schedule change still needs its own approved relationship and replay identity.

## Read and correction

Show old/new repayment calendar, preserved actual payments, principal reduction, accrued-interest release and any fee. A later correction must respect payments/accruals that consumed the amendment. Do not simply restore the old agreement head while retaining incompatible new payments; require a complete linked adjustment or explicit unsupported chain repair.

```text
principal100000 accruedInterest5000; principal forgiven20000
  => principal80000, interest5000, book gain20000
future rate reduction with no required remeasurement -> principal unchanged
forgive unaccrued future interest3000 -> no current gain3000
old repayment instruction10000 outcome unknown -> cannot replace it blindly with8000
same legal amendment under new key -> duplicate effect refused
```

Completion includes loan controls, future interest calculation and common payment/Cash readers. A editable agreement form without conserved financial effects is not the delivered feature.


---

<a id="part-13"></a>

# NEXT-111: Annual common-cost VAT deduction true-up

**Priority when applicable:** P1. **Owner lane:** TAX.

**New scope:** Invoice-level partial deduction already exists. Add a qualified final common-cost allocation over a complete annual population and post only the difference from effective deductions.

**Existing owner to extend:** Existing recognized tax components, qualified releases, VAT return amendments and cost/asset owners.

**Earlier contracts:** NEXT-03, NEXT-04, NEXT-22, NEXT-49. **This-wave dependencies:** None.

**Basis:** R02, X01, P03, P04 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Scope and legal choice

Start with common operating expenses already recognized to expense accounts. Directly attributable full-deduction/zero-deduction costs, private use, special deduction prohibitions and capital-goods adjustment regimes are explicitly separated. Do not multiply every input tax amount by one company turnover ratio.

The official mixed-activity guidance distinguishes reasonable resource-based allocation from the optional qualifying turnover method and discusses provisional versus final allocation [X01]. The actual selected method, denominator/exclusions, rounding and correction period must be qualified as one release. The algorithm below does not choose a legal method from the most favorable result.

```text
RecoveryPoolRevision {
  entity, fiscalAndTaxYear, eligibleOriginalTaxComponents,
  directCostExclusions, allocationMethodRelease,
  independentlyReviewedDriverPopulation, preliminaryDeductionRefs, cutoff
}
DeductionTrueUp {
  poolId, targetBySourceComponent, effectivePriorDeduction,
  signedDeltaByComponent, reportingAttribution, originalCostCounterparts,
  priorTrueUpRefs, digest
}
```

## Calculation

```text
calculateFinalDeduction(pool):
  require complete eligible original source/correction population
  require driver basis known and method applies to each selected cost
  fraction = qualifiedMethod.computeDriverFraction(exactSourceDriverFacts)
  require fraction within supported bounds; zero denominator is a decision case
  for source component:
    availableTax = original supported source tax after effective credits
    target = qualifiedMethod.allocate(availableTax, fraction, sourceFacts)
    effective = originalDeduction + priorDeductionAdjustments - creditedDeduction
    require 0<=target<=availableTax
    delta = target-effective
    retain target, calculation/rounding witness and exact prior effect identities
  require every source component appears once
```

Where the rule rounds the recovery percentage separately, do that before its required monetary calculation. Do not substitute the generic half-up helper for statutory percentage rounding. If the rule works at a pool total, apportion that exact result back to components using a disclosed conserving policy rather than obtaining a different total by independent line rounding.

## Financial and return effects

For an eligible fully expensed cost and a positive additional deduction `D`:

```text
debit deductible input VAT D
credit original non-deductible cost D
```

Negative `D` reverses those sides. Create a signed deduction-adjustment tax fact referencing the original component and qualified reporting attribution. Supplier payable, cash and original purchase gross do not change. Do not delete the original deduction or replace it with the target and also post the delta.

Initial execution refuses a source whose non-deductible portion has been capitalized, deferred or consumed by an unsupported later cost allocation that requires financial basis changes. Those cases need their actual asset/schedule writer to adjust remaining cost and past recognition consistently, not a credit to any convenient current expense account.

`executeTrueUp` checks the exact pool membership, current deductions, source credits and approved release. The journal, adjustment facts, source-capacity claims and receipt commit together. The existing VAT amendment owner subsequently prepares the required return version; this packet does not recreate its settlement delta or submit a declaration.

## Versioning and controls

An additional late invoice/credit changes the relevant pool epoch. A revised target posts only the new difference against all effective prior true-up effects. Old filed declarations retain their bytes. Tax-point attribution and accounting adjustment dates are explicit and can differ under the qualified correction profile.

UI shows provisional allocation, final qualified driver, source-tax ceiling, prior deduction and proposed delta per item, with all excluded costs explained. A complete review cannot omit a mandatory source because it was difficult to classify.

```text
common input tax10000, existing eligible deduction4000, qualified final target6500
  => input VAT debit2500, cost credit2500
repeat same target after posted true-up -> delta0, no duplicate deduction
credit reduces eligible tax to8000; revised target5200; effective old6500
  => deduction adjustment-1300, subject to exact original credit history
capitalized source but no asset adjustment integration -> explicit refusal
```

Completion requires original-cost/tax lineage, amended-report preparation and current controls, not just a percentage displayed on a settings page.


---

<a id="part-14"></a>

# NEXT-112: Domestic construction reverse-charge sales and purchases

**Priority when applicable:** P2. **Owner lane:** TAX.

**New scope:** Add a qualified domestic construction reverse-charge profile. Cross-border services and ROT/RUT claims do not establish the seller/buyer conditions for this treatment.

**Existing owner to extend:** Existing invoice issue, purchase recognition, tax-fact and credit-note owners.

**Earlier contracts:** NEXT-03, NEXT-04, NEXT-51, NEXT-15. **This-wave dependencies:** None.

**Basis:** R02, X02, P03, P51 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Eligibility is an evidence decision

```text
ConstructionTreatmentWitness {
  actualSupplier, actualBuyer, serviceDescription,
  propertyOrWorkLocation, supportedServiceClass,
  buyerQualifyingActivityOrIntermediaryEvidence,
  contractualCompositeSupplyAssessment, effectiveDate,
  sourceTaxPresentation, selectedRuleRelease
}
```

Official guidance makes the nature of the supplied service and the purchaser's qualifying activity important [X02]. A company name, registration number, account code or industry-code label is not sufficient proof. Mixed material/service arrangements require a supported supply classification. Unsupported property, intermediary or incorrectly charged tax cases stay visible.

## Compile a valid qualified sale

```text
compileConstructionSale(witness, lines):
  require all mandatory conditions supported and reviewed at the relevant date
  require no incompatible supplier-charged VAT for this selected treatment
  net = exact supported consideration
  debit customer receivable net
  credit service revenue net
  publish sale tax basis with explicit reverse-charge role and required report mapping
  output VAT charged by seller =0
  freeze mandatory invoice wording, buyer identifiers and treatment evidence
```

Zero seller VAT is not absence of a tax fact. Preserve the taxable-activity basis and its separate report role. The invoice owner still allocates the legal number and records the issue once. A subsequent delivery through Peppol or PDF cannot change the approved treatment.

## Compile a valid qualified purchase

```text
compileConstructionPurchase(witness, source):
  require selected invoice has supported no-supplier-VAT presentation
  N = exact source consideration
  O = qualified self-assessed tax(N, taxPoint, rateRelease)
  D = qualified deductible portion of O
  debit construction expenseOrQualifiedAssetCost (N+O-D)
  debit reverse-charge input VAT D
  credit reverse-charge output VAT O
  credit supplier payable N
  publish separate basis, output and deductible components
```

The rule release supplies precise return-box identities and calculation order. They are not guessed from the ordinary domestic sales-rate mapping. The same component cannot later be admitted again as foreign-service reverse charge or domestic supplier-charged VAT.

The first profile refuses incorrectly charged supplier VAT rather than dropping it from the payable or automatically deducting it. A later supplier correction must preserve the original actual document and follow a qualified incorrect-invoice treatment. Such evidence is not converted to synthetic to pass admission.

## Credit, correction and application

A legal customer credit or supplier credit references original source-line coverage and the supported tax-period policy. It reverses the exact appropriate basis and tax components once. Partial credits release original qualified rounding residuals rather than independently changing rates. A buyer-status change after a posted transaction creates an impact/correction case, not a retroactive toggle that rewrites every invoice.

Use one capture/compiler per transaction direction and existing named application execution. Journal, invoice/payable, tax facts, exact source identities and receipt share the same transaction. Profile activation is a separate reviewed company/rule decision and cannot be performed by an invoice-issuing agent.

## Review and controls

The UI shows the ordinary-treatment alternative, the specific condition that selects reverse charge, evidence and exact financial differences. Only a selected qualified treatment can become executable; uncertainty is not resolved by always choosing the treatment with less tax due.

```text
synthetic N100000, output self-tax25000, deduction25000:
  buyer cost100000 + input25000 - output25000 - AP100000 =0
seller same N -> AR100000/revenue100000 and retained basis, no seller VAT line
half deduction -> buyer cost112500/input12500/output25000/AP100000
buyer evidence missing -> source retained, financial plan blocked
new key and other tax family for same recognized source -> duplicate refusal
```

This is a conditional specialist profile. No new VAT engine, journal owner or automatic company-wide reverse-charge flag is introduced.


---

<a id="part-15"></a>

# NEXT-113: EU B2C destination VAT and Union OSS reporting

**Priority when applicable:** P2. **Owner lane:** TAX.

**New scope:** Add destination-tax consumer sales and a distinct Union OSS obligation. Earlier EU B2B sales and periodisk sammanställning do not cover this reporting family.

**Existing owner to extend:** Existing source/order intake, sale recognition, country/rate witnesses, FX reporting and external-obligation owners.

**Earlier contracts:** NEXT-51, NEXT-49. **This-wave dependencies:** None.

**Conditional:** NEXT-39: proceeds arrive through a processor; NEXT-53: a qualified goods supply rather than service is selected.

**Basis:** X03, R02, P51 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Bounded profile

Begin with a reviewed Swedish-established seller and one supported Union OSS supply family. Registration, scheme, customer status, place of supply and current rate must be actual facts. Exclude IOSS, non-Union scheme, marketplace deemed-supplier arrangements, unsupported establishments and small-business exemption interactions until separately qualified. Do not infer threshold eligibility from only the orders this system happens to have imported.

```text
OssSaleFact {
  originalSaleIdentity, consumerEvidence, placeOfSupplyWitness,
  consumptionCountry, supplyFamily, registrationRevision,
  originalCurrencyAmounts, originalTaxRate,
  bookCurrencyRecognitionWitness, reportCurrencyConversionWitness,
  correctionOfOriginalPeriod?, domesticDisclosureRole
}
OssReturnRevision {
  registration, scheme, period, completeCountryRateGroups,
  originalPeriodCorrections, reportEURAmounts, priorSubmittedRefs,
  contributionLineage, conversionRelease, sourceCoverage
}
```

Official Swedish OSS guidance distinguishes this declaration and euro payment from the ordinary VAT process [X03]. Do not route the foreign output tax into domestic output-tax boxes or the ordinary VAT settlement obligation. Any required local disclosure is supplied by its explicit qualified mapping.

## Source classification and financial recognition

```text
classifyConsumerSupply(source, profile):
  require final legal supplier and customer status known
  require enough noncontradictory country/location evidence under this supply rule
  determine eligible scheme and country/rate effective at actual tax point
  if uncertain, retain review case; never let a billing address alone override contradictions

compileOssSale(fact):
  derive net/tax/gross under original price and qualified destination rate
  convert book amounts under the normal recognition policy with conserving rounding
  debit AR or qualified payment clearing grossBook
  credit revenue netBook
  credit country/scheme output-tax liability taxBook
  retain original-currency amounts and tax basis for reporting
```

Order, payment and invoice records about the same sale remain one recognition identity. A payment processor is not automatically the seller or deemed supplier. Fees do not reduce the taxable sale without a qualified source treatment.

## Reporting currency and corrections

```text
prepareOssReturn(period):
  capture complete eligible facts and effective registration/period inventory
  group by scheme, consumption country, supported supply/rate category and original period
  translate using the qualified reporting-currency/date rule, not today's book carrying rate
  retain exact conversion and permitted rounding per reporting group
  compute positive and correcting components under the supported OSS schema
  reconcile reported liability target to booked country/scheme balances
```

A prior-period correction stays identified with its original reporting period. Do not simply overwrite an old accepted return or net every negative into current sales. The selected authority correction windows and procedure are explicit release data. A missing country group cannot become zero merely because fetching its source failed.

The euro reporting target can differ from book-currency liability due to reporting conversion and later payment FX. Store that bridge explicitly through the appropriate tax-liability/FX owner. Do not retroactively change revenue to force it to match. Purchases and deductible input VAT are not netted against OSS output liability by this packet.

## Submission and settlement

Create a distinct typed obligation/artifact and use a supported e-service handoff or qualified API if actually available. Do not invent a public OSS submission endpoint or reuse the domestic VAT API by changing a form name. The payment uses the actual OSS destination, reference and euro amount; an ordinary tax-account deposit is not its settlement evidence.

```text
example supplied gross120 EUR at synthetic20% -> net100/tax20
book rate11 SEK/EUR -> AR1320/revenue1100/OSS liability220 SEK
reported tax20 EUR; later actual20 EUR payment costs224 SEK
  -> liability220 + supported FXloss4 against cash224, not another revenue entry
registered period with verified zero activity -> required zero report if profile requires it
```

Completion requires the selected supply profile, complete country/rate lineage and honest reported/submitted/paid states. This is not a claim of all EU consumer-sales support.


---

<a id="part-16"></a>

# NEXT-114: EU foreign input-VAT recovery claims and receipts

**Priority when applicable:** P1. **Owner lane:** TAX.

**New scope:** Add foreign VAT recovery from the foreign authority. A foreign tax amount must not be claimed as Swedish deductible input VAT merely because it appears on a purchase.

**Existing owner to extend:** Existing original purchase, evidence, tax-claim obligation, currency and receipt owners.

**Earlier contracts:** NEXT-03, NEXT-49. **This-wave dependencies:** None.

**Conditional:** NEXT-17: an approved foreign-currency refund receivable needs supported FX settlement.

**Basis:** X04, P03 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Candidate versus recognized entitlement

Official guidance distinguishes foreign VAT recovery from Swedish input-tax deduction and describes an EU electronic application through the Swedish service [X04]. The refund country's eligibility, expense categories, establishment restrictions, periods, required attachments and thresholds are qualified inputs. Non-EU paper or other-country procedures are not implied by this first EU profile.

```text
ForeignTaxComponent {
  purchaseRecognitionId, sourceInvoiceLine, refundCountry,
  originalCurrencyTax, originalBookedCostAllocation, invoiceEvidence
}
RefundClaimRevision {
  applicantIdentity, refundCountry, claimPeriod,
  exactSelectedComponentAmounts, countryRuleRelease,
  originalAttachments, registrationEligibility, artifactRefs
}
AuthorityRefundDecision {claimRevision, accepted/rejected component amounts, evidence}
RecoveryReceivableEffect {componentCoverage, originalUnits, bookCarrying, settlements, receipt}
```

A cost can be a claim candidate before a book receivable is justified. The initial recognition profile uses an actual qualified recoverable entitlement, such as a verified authority decision where that satisfies the applicable rule. A submitted request alone does not increase assets.

## Prepare the claim

```text
prepareForeignVatClaim(selection):
  capture original invoices, corrected invoices and prior claim allocations
  require same refund country/applicant and permitted reporting period
  require each source tax amount retained, not inferred from gross at a Swedish rate
  require requested amount <= unclaimed eligible source-tax capacity
  classify each expense under the refund country's actual rule and code list
  include required original document representation and exact currency amounts
  keep rejected/unsupported items with reasons rather than silently exporting only successes
  seal request fields, attachments and applicant authority
```

One component can be partially claimed only if the qualified application supports the split and total coverage is conserved. A repeat submission of the same revision recovers its existing attempt. Another claim period or local ID does not permit claiming the same invoice tax twice. Credit notes reduce the effective eligible source capacity and trigger review of any already filed claim.

## Accounting and payout

```text
recognizeApprovedRefund(decision):
  approved = supported entitlement by component
  targetBook = qualified receivable measurement using explicit currency/date evidence
  delta = target - prior effective recognized entitlement for that coverage
  debit foreign-tax-refund receivable delta
  credit qualified original-cost recovery role delta
  retain original purchase and source foreign-tax facts unchanged
```

If the original nonrecoverable cost entered an asset or unconsumed deferral, its appropriate cost-basis owner must participate. The initial fully-expensed-cost profile refuses unsupported capitalization changes rather than crediting arbitrary current income. No Swedish VAT-return fact is created by this recovery.

```text
recordRefundCash(claim, actualReceipt):
  release the matching original-currency/book carrying receivable once
  debit actual bank/qualified clearing
  credit recovery receivable carrying amount
  separately recognize evidenced FX or bank fee differences through their owner
```

A rejection reduces only a previously recognized entitlement under the qualified correction rule; it does not expense the original purchase twice if it was never capitalized as receivable. An authority grant beyond requested/recognized capacity needs explanation, not automatic surplus income.

## Delivery, review and controls

Retain submitted bytes or an explicit official-service manual handoff and authentic receipt. No API is invented. Additional-information requests link to the original immutable claim and deadline. Country/year/source totals reconcile through candidate, requested, accepted and paid states. Unsupported current rules remain visible gates.

```text
original purchase cost12000 includes foreign tax2000
accepted claim1500 under qualified fully-expensed profile -> AR1500/cost recovery1500
cash1500 -> AR0, no additional expense/VAT effect
claim2000 followed by repeat new-key claim2000 -> duplicate coverage refusal
requested2000, never recognized, rejected -> financial journal0
```

This provides the applicant company's accounting and electronic handoff. It does not promise a refund entitlement, foreign tax advice or production acceptance from a syntactically valid file.


---

<a id="part-17"></a>

# NEXT-115: Overnight travel allowances and meal-benefit partition

**Priority when applicable:** P2. **Owner lane:** PAYROLL.

**New scope:** Mileage reimburses distance. Add overnight business-travel allowance eligibility, country/day classification and separate meal reductions/benefit inputs without reusing the mileage rate formula.

**Existing owner to extend:** Existing employee trip, claim, payroll earning/benefit and payout-handoff owners.

**Earlier contracts:** NEXT-33, NEXT-20, NEXT-21. **This-wave dependencies:** None.

**Conditional:** NEXT-34: the same retained trip also includes a mileage award.

**Basis:** X05, P34 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Facts and independent classifications

```text
TravelStayRevision {
  employee, departure/return instants, actual business locations,
  ordinary workplace/home facts, overnight evidence,
  itinerary segments, accommodationPayer, mealEvents,
  continuousLocationHistory, employmentAgreementAllowance
}
MealDecision {
  mealType, actualProvider/Payer, mandatoryInTransportOrHotelPrice,
  external/internalRepresentationWitness, sourceReceipt,
  reducesAllowance, createsTaxableBenefit, ruleWitness
}
TravelAward {
  exact day/country/night classifications, agreedEntitlement,
  exemptLimitAfterReductions, exemptPaidPart, taxableExcess,
  mealBenefitComponents, alreadyRecognizedCostRefs, payoutRoute
}
```

The official guidance distinguishes allowance reduction from taxable meals: they are not always the same condition [X05]. Do not encode `freeMeal => reduce allowance and create benefit` for every meal. A compulsory hotel breakfast, for example, needs its own reviewed branch. Keep the actual source and chosen rule evidence.

## Calendar and calculation

```text
calculateTravelAward(trip, profile):
  require actual business-trip/overnight eligibility and complete itinerary
  split using the profile's day, country and travel-time attribution rules
  include continuous prior stays for reduced-rate thresholds; new tripId cannot reset duration
  for eligible segment:
    baseLimit = dated qualified country/day/night allowance
    reduction = exact supported meal/accommodation reductions
    remainingExemptLimit = max(baseLimit-reduction,0)
    entitlement = employment/travel agreement amount for this segment
    exemptPaid = min(entitlement,remainingExemptLimit)
    taxableExcess = entitlement-exemptPaid
    mealBenefits = independent qualified benefit valuation for applicable meals
  retain exact intermediates and aggregate under the rule's prescribed rounding order
```

Country changes, arrival/departure classification and long-term assignment exceptions need their actual release data. Do not multiply elapsed24-hour blocks by a universal rate, reset a continuous stay at fiscal year end or treat employee overnight assertions as verified accommodation evidence.

The first implementation can support one domestic short-stay profile with explicit boundaries. Foreign/long-duration cases are then named unsupported rather than guessed from the nearest country's amount. Evidence intake remains usable while the calculation is blocked.

## Exclusive handoff and posting

Use distinct component identities for mileage, per diem, actual hotel receipts and taxable meals so the same trip can legitimately contain all without paying a receipt twice. The exemption is a tax classification, not employer contractual entitlement or a deductible VAT invoice.

The exempt reimbursement reaches NEXT-33's recognized employee liability and one payroll/direct route. Taxable excess is one payroll earning component. Taxable noncash meals reach the benefit owner without creating another cash reimbursement. If meal costs were already purchased by the company, they are not expensed again when the benefit is reported.

```text
executeTravelAward(plan): OwnedTx
  recheck trip/meal/continuous-stay/rate and payout-owner versions
  recognize only the supported reimbursement/earning liabilities assigned to this owner
  create exact existing-liability payroll instructions where already accrued
  publish meal-benefit facts separately from cash entitlement
  commit source-component capacities and receipt together
```

A changed itinerary after payment follows NEXT-36's qualified recovery/adjustment path. An expired queue claim is not proof the old allowance was never paid. Route replacement requires the prior route's actual unconsumed/released status.

## Views and examples

Show each day/night, country, supplied meals, contract amount, exemption ceiling, excess and noncash benefit. Employee explanations omit other employees' data. Payroll reports expose the actual paid/provided period rather than the request date.

```text
synthetic agreed allowance3000, base limit2500, qualified meal reduction500
  => exempt2000 + taxable cash1000
separate supplied meal benefit400 -> noncash payroll base400, not extra400 cash
mandatory hotel breakfast case -> apply its distinct reduction/benefit rule
same meal also entered as employee-paid receipt -> payer conflict requiring review
same stay split into two requests -> continuous duration preserved
```

The amounts are hypothetical design vectors. Actual tables, timing thresholds, eligibility and meal exceptions must be qualified before the selected company uses the calculation.


---

<a id="part-18"></a>

# NEXT-116: Recurring car-benefit valuation and employee payment links

**Priority when applicable:** P2. **Owner lane:** PAYROLL.

**New scope:** Payroll already accepts benefit inputs. Add a concrete retained car-benefit eligibility/valuation lifecycle and payment reconciliation so those inputs are not anonymous monthly amounts.

**Existing owner to extend:** Existing employee revisions, private payroll calculations, actual paid/provided reporting and company car cost records.

**Earlier contracts:** NEXT-20, NEXT-21, NEXT-35. **This-wave dependencies:** None.

**Basis:** X06, P20 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Profile and source facts

The first profile supports a reviewed company-provided car and defined ordinary cases. Fuel, congestion/infrastructure charges, mixed employer arrangements, special reductions and retroactive disputes require separately supported branches. A vehicle purchase or rental does not alone prove a taxable benefit was provided to a particular employee.

```text
CarBenefitAssignmentRevision {
  vehicleIdentity, employeeId, effectiveDates, actualAvailabilityEvidence,
  valuationYearInputs, publishedModelFacts, userPaidCosts,
  relevantDrivingEvidence, supportedExceptions, ruleRelease
}
BenefitPeriodResult {
  employeePeriod, assignmentRevision, grossBenefitValue,
  eligibleActualEmployeePayment, remainingTaxableValue,
  cashVsNoncashClassification, providedDateEvidence, formulaWitness
}
EmployeeBenefitPayment {
  assignmentId, period, source: bank|net_payroll_deduction|qualified_direct_cost,
  actualAmount, financialRefs, sourceComponentIdentity
}
```

The official guidance distinguishes payments made with the employee's own funds from a contractual gross-salary reduction [X06]. The latter is not automatically payment for the benefit. A benefit-period output keeps that distinction and never treats negative cash payroll as a generic cure.

## Exact valuation and period capture

```text
calculateCarBenefit(assignment, yearRelease, period):
  require supported vehicle/year/availability facts and complete effective-period evidence
  V = exact qualified formula applied to published input values and selected exceptions
  P = sum(actual eligible employee payments attributable to this benefit period)
  require no payment already credited to another benefit or refund obligation
  taxable = max(V-P,0) under this supported payment-offset profile
  excess = max(P-V,0)  # explicitly unresolved/refundable/other treatment, not negative benefit
  retain original V, P, taxable and the complete formula/data release
```

Not every car-related employee payment reduces every benefit base. The selected release maps each payment type explicitly. Fuel benefits can have different bases; the initial profile cannot reuse the ordinary-car formula for them by changing a field label. More generous employer terms do not override tax eligibility.

A monthly revision is generated from current evidence with a stable assignment/period identity. A later car change creates a new assignment segment. Zero taxable value is retained as a semantic benefit result where the reporting rule needs it, while no artificial zero journal line is created.

## Payroll and accounting handoff

Noncash benefit increases the relevant withholding/contribution bases through NEXT-20 but does not increase employee cash earnings. Company car costs are already recognized through purchases/rental/assets; do not expense the statutory benefit value a second time unless a separately qualified presentation requires explicit offsetting records.

A planned net-pay deduction is not an actual payment until the payroll owner commits its deduction/settlement effect under the qualified policy. Capture anticipated treatment for the proposed run, then bind the exact deduction use atomically with the pay-run records. If actual payment timing changes the reporting basis, create the required adjustment rather than claiming paid evidence from preparation.

```text
executeBenefitHandoff(plan):
  use same transaction as the consuming payroll operation when payment offset depends on it
  persist period benefit, payroll component and any deduction source usage exactly once
  require run/assignment/payment versions agree
  return one owned handoff receipt, not another salary payment
```

Independent bank payments use their own actual financial source and allocation; do not both collect through payroll and use the same amount as an unlinked bank offset. Refund of an excess employee payment requires the real employee-liability/refund treatment, not a negative AGI benefit.

## Controls and vectors

Display vehicle, period, valuation facts, actual employee payments, gross benefit and reportable base. Current private permissions protect all employee-specific reads and replays. A change after filing links to the original individual reporting identity and current payroll-correction owner.

```text
synthetic benefit50000, eligible net payment10000 -> taxable40000
same50000 benefit and gross salary reduction10000 -> benefit stays50000
noncash benefit40000 -> relevant tax bases rise40000, cash gross does not
payment60000 against50000 -> taxable0 plus explicit excess10000
same payment identity in two benefit periods -> source-capacity conflict
```

Completion includes qualified computation, actual payroll/reporting handoff and preserved original cost/payment records. A settings field for a guessed monthly car value is not this capability.


---

<a id="part-19"></a>

# NEXT-117: Interest statements: KU20 and applicable KU25 identities

**Priority when applicable:** P2. **Owner lane:** TAX.

**New scope:** KU31 covers dividends and AGI covers compensation. Add annual interest reporting with its own reporter/recipient, timing and correction rules rather than treating every loan accrual as a reportable amount.

**Existing owner to extend:** Existing loan interest, actual settlement, tax withholding and versioned information-return artifact owners.

**Earlier contracts:** NEXT-32, NEXT-49. **This-wave dependencies:** None.

**Conditional:** NEXT-62: received late-payment interest creates an applicable reporting obligation.

**Basis:** X07, P32 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Obligation and direction

```text
InterestReportingObligation {
  reportingEntity, incomeYear, family: KU20|KU25,
  recipientOrBorrowerIdentity, actualReportingDutyWitness,
  applicableInstrument/securityFacts, qualifiedRelease
}
ReportableInterestEvent {
  originalInterestComponent, paidOrMadeAvailableDate,
  originalCurrencyAmount, SEKReportingAmount, conversionWitness,
  withholdingIfApplicable, sourcePaymentOrCreditingEvidence
}
InterestStatementRevision {
  obligationId, specificationNumber, selectedEventIds,
  reportedValues, exclusions, previousFiledIdentity, artifactDigest
}
```

The company paying interest on a shareholder loan may have KU20 duties. Its own interest expense paid to a bank is not therefore a KU25 it should issue. KU25 applies only where this entity is the actual qualifying reporter of the recipient individual's interest expense. Late-interest-only and other exceptions need their real rules.

The current official page also has year-specific digital format changes [X07]. Do not reuse an old PDF/field map merely because the form family name remains KU25. Acquire the actual supported year schema and rules before release.

## Select the reportable population

```text
captureInterestStatement(obligation):
  require reporter identity, recipient class and actual reporting duty established
  select interest events by this family's legally relevant paid/available timing rule
  keep accrued but unreported interest in an explicit bridge
  apply instrument, prepaid-interest, security and withholding rules by exact release
  convert using the qualified reporting-date/source rule, not year-end cash remeasurement
  require each economic interest component included once per permitted reporting meaning
```

Cash payment and crediting an available account may have different evidence but can identify the same reportable event. Do not count both. A book interest accrual alone is not assumed available to the recipient. Conversely a genuine availability event is not omitted merely because cash transfer occurs later. The activated rule specifies the distinction.

## Withholding and financial linkage

If the selected KU20 case requires withholding, its actual liability and payment come from the interest-payment operation, not a new journal when exporting the statement. Extend that operation's internal compiler so it splits gross interest into net recipient amount and withholding liability in the same financial group, retaining the applicable authority. No withholding percentage is hardcoded in this packet.

```text
grossInterest = netPaid + actualWithholding
report values = exact captured gross and withholding under the permitted year rules
```

Missing required actual withholding evidence is a reconciliation blocker; the renderer cannot fabricate a tax liability after year end to match an expected formula. Corrections to financial interest stay separate from reporting-only corrections.

## Artifact and correction identity

```text
prepareInterestStatement(command):
  capture complete event/correction population and independent recipient controls
  calculate exact year totals and qualified field mappings
  retain same nonzero specification identity for a replacement of the same item
  seal semantic revision plus schema/calculator version
  render and validate through the existing information-return artifact infrastructure
```

A corrected year amount creates a new revision preserving original submitted bytes. A second specification number can create an additional valid item rather than replace the first, so the operation must distinguish replacement, removal and genuinely distinct reporting items. Exact current submission actions remain external-attempt operations with actual representative authority and receipts.

## Controls and examples

Reconcile: opening accrued interest plus current accruals and supported changes, less actual paid/available components, equals closing accrual. The statement uses its qualified subset of those components and timing bridge, not the complete GL expense sum. Confidential individual identities are protected under the selected tax-reporting grant.

```text
accrued12000, supported reportable paid/available8000 -> report8000,
    remaining4000 shown as timing basis, not silently reported12000
same8000 credited then transferred in cash -> one event8000
gross8000/net6000/actual withheld2000 synthetic -> equality holds
company pays its bank interest -> not automatically an outbound KU25
replacement changes only amount -> same reporter/year/person/specification identity
```

Completion requires correct duty selection, supported-year electronic artifacts, immutable corrections and source controls. This packet does not originate consumer loans or provide personal tax planning.


---

<a id="part-20"></a>

# NEXT-118: Prospective salary exchange into pension contributions

**Priority when applicable:** P2. **Owner lane:** PAYROLL.

**New scope:** Add an effective-dated employee/employer salary-exchange agreement with distinct salary and pension bases. Pension invoice reconciliation alone does not define the waived salary or prevent double deductions.

**Existing owner to extend:** Existing employment revisions, payroll component compiler, pension accrual/provider reconciliation and SLP basis.

**Earlier contracts:** NEXT-20, NEXT-21, NEXT-87. **This-wave dependencies:** None.

**Conditional:** NEXT-36: an already paid or reported period requires a supported correction.

**Basis:** X08, P87 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Contractual inputs

```text
SalaryExchangeAgreementRevision {
  employee, executedAgreementEvidence, futureEffectiveInterval,
  preExchangeSalary, exchangeAmountOrFormula,
  postExchangeSalary, employerExtraPremiumTerms,
  pensionableSalaryBasisFromActualPensionAgreement,
  absence/bonus/terminationTreatment, cancellationTerms,
  ruleAndEligibilityWitnesses
}
ExchangeOccurrence {
  agreementId, payrollPeriod, sourceSalaryEvent,
  waivedSalary, additionalPensionEntitlement,
  payrollRunRef, pensionAccrualRef, consumedState
}
```

The initial profile is prospective voluntary salary exchange under supported employment/pension terms. No net-pay deduction retroactively converts already earned/paid salary into pension. Official guidance makes the actual pension agreement relevant to the pensionable salary/allowable basis [X08]. An employee side note is not enough to redefine that underlying basis.

Do not promise that salary exchange is beneficial or infer social-insurance/pension thresholds from a remembered current amount. The review records the relevant current eligibility/impact information and any required specialist decision before activation.

## Calculation

```text
prepareExchangePeriod(agreement, payrollFacts):
  require agreement effective before the supported salary entitlement boundary
  S = supported gross cash salary before exchange
  E = exact contractual exchange for this period
  require 0<=E<=eligible salary and all applicable safeguards satisfied
  cashGross = S-E
  pensionExtra = exact agreed premium entitlement, including any explicit employer top-up
  pensionableBase = actual pension contract's supported base selector
  retain S,E,cashGross,pensionExtra,pensionableBase separately
  emit one waived-salary modifier and one pension-entitlement component
```

A top-up is an actual employer promise, not automatically the difference between guessed social-tax rates. Existing ordinary pension premium calculations use their contractual base, which might not equal either S or S-E without an explicit rule. General withholding/contribution calculation then consumes cashGross and any other supported taxable components.

## Atomic payroll/pension handoff

The salary expense is the actual qualified post-exchange salary. The exchange amount is not then deducted again from net pay. The additional pension cost/liability is recognized once by the pension accrual owner with its proper tax/SLP classification and external provider identity.

```text
executeRunWithExchange(plan): OwnedTx
  recheck agreement, earning identity, payroll and pension source versions
  post salary/tax/payable effects using cashGross
  record additional pension entitlement/accrual through internal pension writer
  consume exchange occurrence exactly once
  record full run/occurrence/pension links and one aggregate receipt
```

A later provider invoice reconciles and releases the existing pension accrual under NEXT-87. It must not expense the premium a second time. A provider failure or missed transfer does not automatically restore the employee's waived salary; actual agreement rights and supported correction decide the response.

## Amendments and exits

A rate or salary change affects only future eligible occurrences through a new agreement revision. A prepared but unexecuted run becomes stale if its selected agreement changes. Pausing because of absence uses the agreement's actual formula and preserves why a period was skipped; it does not keep deducting a fixed amount from an unsupported zero salary.

Termination inventories unpaid pension contributions and already executed exchanges alongside ordinary final pay. Revoking an agreement does not delete historical premium entitlements. Corrections to already paid/reporting periods use NEXT-36 and preserve original individual declarations.

## Operator view and examples

Show cash salary before/after, premium entitlement, contractual pension base, actual provider premiums and warnings requiring review. Employee acknowledgments are retained separately from operator posting approval. Private payroll grants cover all reads and replay.

```text
synthetic S6000000 E500000 -> cashGross5500000
agreed extra premium530000 -> pension cost/liability530000 once
net salary calculation starts from5500000, not another minus500000 afterward
provider invoice530000 -> releases prior accrual; new premium expense0
pension agreement says post-exchange base -> do not use6000000 because another text says so
new request key for same period/exchange event -> no second modifier
```

Completion is an actual agreement-to-pay-run-to-provider-control journey. It is not a calculator recommending pension optimization or a generic gross-deduction toggle.


---

<a id="part-21"></a>

# NEXT-119: Cash share subscriptions and registered-capital transition

**Priority when applicable:** P2. **Owner lane:** EQUITY.

**New scope:** Dividends distribute existing equity. Add the company-side record of cash subscriptions, paid allotments and an evidenced capital-registration transition without inventing share rights from bank receipts.

**Existing owner to extend:** Existing company/shareholder facts, bank receipt, equity roles, signed-decision and external-obligation owners.

**Earlier contracts:** NEXT-02, NEXT-13, NEXT-49, NEXT-89. **This-wave dependencies:** None.

**Basis:** X09, P89 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Restrict the first issue profile

Support a reviewed cash issue with fixed subscription terms and explicit nominal/premium allocation. Exclude noncash contributions, convertibles, warrants, mergers, debt conversion and complex conditional instruments until their own legal/accounting profiles exist. Public registration instructions identify a process, not the validity of a particular company resolution [X09].

```text
CashIssueResolutionRevision {
  companyIdentity, actualDecisionEvidence, authorizedScope,
  classAndRightsFacts, maximumShares, subscriptionPrice,
  nominalAmountPerShare, premiumAllocationPolicy,
  subscriptionWindow, paymentAndRegistrationConditions
}
Subscription {subscriberIdentity, acceptedUnits, termsRevision, legalCommitmentEvidence}
SubscriptionCashEffect {sourceBankIdentity, subscriber, amount, accountingRole, receipt}
AllotmentEffect {subscription, units, nominalAmount, premiumAmount, effectiveConditions, receipt}
CapitalRegistrationObservation {authorityReceipt, registeredIssueIdentity, amount, dates, scope}
```

A bank transfer carrying the word shares is not automatically registered share capital. Conditional/refundable money remains in the selected liability/holding role until the reviewed legal/accounting conditions support another classification. Issuance fees and their tax treatment are separate source-backed costs, not deducted from nominal capital without authority.

## Exact money and units

```text
prepareCashAllotment(subscription, paidSources):
  require original valid resolution and subscription conditions established
  units = reviewed accepted/allotted integer units
  require units<=remaining resolution/subscription capacity
  total = units * exactSubscriptionPrice
  nominal = units * exactNominalPerShare
  premium = total-nominal
  require premium>=0 for the selected profile
  require evidenced allocatable payment covers required total
  require no cash source used for another subscription or financial receipt
  capture all remaining conditions and registration state
```

A rounding policy cannot create fractional share units or silently absorb an underpayment. Overpayments are separately refundable/unallocated funds, not additional issued shares. Partial payment/allotment requires a profile that defines exactly which subscription units can be allotted; otherwise the funds stay pending.

## Accounting stages

For the selected refundable-before-allotment profile:

```text
actual receipt P:
  debit bank P
  credit pending subscription funds liability P

qualified effective paid allotment P=N+S:
  debit pending subscription funds liability P
  credit unregistered issue nominal role N
  credit unregistered premium role S

verified registration:
  transfer nominal N to registered capital role
  transfer premium S to its correctly classified paid-in-premium role
  update company/shareholder issue facts through the owning reviewed operation
```

The precise intermediate equity/liability classifications are selected by a qualified framework and legal-condition decision. Do not treat this illustrative profile as a universal rule or post registered capital before the required evidence. Where an initial receipt was already posted correctly, adopt its unused allocation rather than debit bank again.

All source usage, allotted unit capacity, journal and receipt commit atomically per supported stage. Registration consumes the exact allotted issue once. An authority response for another issue or partial amount cannot register the whole plan.

## Failure and correction

If an issue fails or lapses, determine the actual refundable obligation from the retained terms/decision. Restore or reclassify pending equity through the supported complete correction, then separately settle real cash refunds. Never erase the receipt, create negative registered shares or use dividend permission as an issue-cancellation power.

The maintained shareholder register/entitlement owner preserves dates and classes for later dividends. This is not a trading system, cap-table valuation product or authority filing done from an API response alone.

```text
100 units at1000 minor, nominal200 each -> total100000, capital20000, premium80000
bank receives105000 ->100000 subscription capacity +5000 explicit excess
pending funds received but subscription unaccepted -> registered capital0
same registration receipt retried -> one classification transition
registered receipt20000 nominal does not imply another100 units can be allotted
```

Completion includes company/equity control reconciliation, actual source references and an honest registration/return-of-funds state. A generated resolution template does not establish the real decision.


---

<a id="part-22"></a>

# NEXT-120: Preliminary income-tax revisions and authoritative installment schedules

**Priority when applicable:** P1. **Owner lane:** TAX.

**New scope:** Annual current-tax calculation and final INK2 filing already have owners. Add a separately labelled forecast-based preliminary declaration, its revised authority decision and the payment-schedule impact.

**Existing owner to extend:** Existing corporate-tax calculator, immutable Cash forecast/scenario, tax-account events and external obligations.

**Earlier contracts:** NEXT-22, NEXT-49. **This-wave dependencies:** None.

**Conditional:** NEXT-74: linking final annual filing outcomes; NEXT-99: later scoring the retained estimate against actual tax outcomes.

**Basis:** X10, P22, P99 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Actual forecast versus actual obligation

```text
PreliminaryTaxEstimateRevision {
  fiscalYear, actualToDateBasis, remainingForecastScenario,
  corporateTaxProfile, forecastAdjustments, completeAssumptions,
  estimatedFullYearBases, existingAuthorityDecision, digest
}
PreliminaryDeclarationIntent {estimateRevision, officialFormProfile, applicantAuthority, attempt}
PreliminaryTaxDecision {
  originalAuthorityEvidence, fiscalYear, assessedScope,
  installmentSchedule, replacesDecisionRef?, effectiveDate
}
```

A forecast can estimate a proposed full-year tax basis. It is not a finalized tax computation or a permission to reduce payments unilaterally. The official preliminary-tax service separates submitted declarations from decisions on debited tax [X10]. Continue to represent the currently authoritative obligations until an effective replacement or other actual authority evidence changes them.

## Estimate without contaminating the books

```text
preparePreliminaryEstimate(actualBasis, selectedForecast):
  require same company/year and explicit split between actual and hypothetical periods
  require no overlap between actual recognized components and scenario projections
  re-use the qualified corporate-tax pure calculator with inputMode=forecast
  retain every assumed revenue, cost, tax adjustment and unsupported family
  compute fullYearTarget and compare with existing debited schedule
  output estimate/uncertainty, not a current-tax journal or filed-return fact
```

Known losses, reserve choices, pensions and other tax adjustments must have supported actual facts or labelled scenario inputs. A missing mandatory tax adjustment cannot become zero to make the estimate look precise. A historical Cash forecast's expected tax contributions are not independent source evidence for recalculating the same tax.

The planning view can show a hypothetical remaining-installment amount, but it must not label an equal split as the authority's future decision. The real installment dates, catch-up effects and effective scope are taken from the actual returned decision.

## Request and decision lifecycle

Create a fixed application/form payload or official-service handoff from the approved estimate. Use actual applicant/representative authority and retained external-attempt identity. The available public entry point is not proof a supported API exists; never invent one. Capture authentic receipt and later decision separately.

```text
admitNewDecision(observation):
  verify company/year, original evidence and exact replaced decision scope
  retain every assessed installment/date and any retroactive adjustment
  compare with already posted tax-account charges and actual payments
  append decision revision and intended current obligation schedule
  do not reverse old booked bank payments or alter final current-tax expense
```

When actual assessed tax-account events arrive, their owner posts/matches them using this decision as supporting evidence. A decision changing future debits is not automatically a new cash payment. Overpayments/refunds follow actual authority and bank events rather than a formula guessed from the annual estimate.

## Cash and reporting integration

Cash selects one authoritative schedule for each still-outstanding obligation and keeps the hypothetical estimate as a scenario. Existing tax-account funding, charges and already reserved payment instructions must be reconciled so the schedule does not subtract the same expected outflow twice. An old exported instruction cannot be cancelled merely by changing a forecast; its external outcome remains with the payment owner.

Final INK2/current tax later reconciles against actual provisional tax history. It does not become dependent on every preliminary estimate having been submitted. Old estimates remain useful for forecast-error evaluation through NEXT-99.

```text
estimated annual tax120000, later scenario90000 -> proposed reduction30000,
    actual payable schedule unchanged until evidence of replacement
received decision revises future installment10000 to6000 -> exact new schedule selected,
    prior bank payments unchanged
book current-tax expense90000 and prepaid charges80000 -> separate balances,
    no rule automatically books only10000 as tax expense
submission accepted but new decision unavailable -> status pending decision
```

Completion requires an estimate with honest assumptions, a supported official handoff and versioned actual decision/payable/Cash consumers. It does not certify tax advice or external acceptance through a screenshot of a local form.


---

<a id="part-23"></a>

# NEXT-121: Opt-in bounded standing posting mandates

**Priority when applicable:** P1. **Owner lane:** AGENT.

**New scope:** Multi-human approval covers exact plans. Add an explicitly enabled later-scope authority for a narrowly allowed recurring purchase pattern, with atomic cumulative limits. Book Zero remains exact-human-approval by default.

**Existing owner to extend:** Existing admission, rule activation, plan execution and financial receipts; extend only explicitly allowlisted application operations.

**Earlier contracts:** NEXT-02, NEXT-03, NEXT-16, NEXT-96. **This-wave dependencies:** None.

**Basis:** R02, R03, P96 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## A new authority kind, never a forged approval

```text
ExecutionAuthority = ExactApprovalRef | SupportedStandingMandateRef
StandingMandateRevision {
  book, allowedOperationAndCompilerVersions,
  reviewedSupplierAndServiceIdentities, permittedSourceEvidenceClasses,
  specificRuleReleaseIds, accounts, currency,
  postingDate/periodRestrictions, perEventLimit,
  sharedBudgetPoolIds, maxCount, validity, authorizingHumans,
  revocationEpoch, explicitExcludedCases
}
MandateConsumption {
  mandateRevision, originalEconomicEvent, planDigest, receiptId,
  chargedBudgetBuckets, grossRiskAmount, eventCount
}
```

Default feature state is off. First supported operation is qualified same-currency purchase recognition for an evidenced recurring service pattern. Exclude payments, refunds, legal document issue, payroll, tax adjustments, corrections, filing, period close and signing. A later scope extension needs its own explicit qualified authority contract.

The plan is still calculated and sealed by the real purchase owner. The mandate authorizes execution only when its exact eligibility predicate and bounds hold. A model probability or previous approval frequency cannot satisfy source truth or grant power.

## Human activation and eligibility

```text
prepareMandate(candidate):
  require narrow stable supplier/service/source pattern and supported rule versions
  evaluate against retained independently reviewed examples and adverse cases
  list every operation excluded and every shared budget affected
  freeze exact conditions, limits and effective interval
activateMandate:
  require configured independent human/role quorum through NEXT-96
  grant only the scope approved; agents cannot activate or expand it
```

Required input fields come from verified structured sources or actual human review under the stated evidence policy. Newly inferred supplier identity, changed tax treatment, missing invoice, changed rate or conflicting credit becomes human review. Never approve a free-form prompt whose semantic scope can widen later.

## Atomic budgets and financial effect

Use cumulative gross recognized purchase exposure for the first profile, not debit-plus-credit totals or net tax. Currency is fixed. Buckets include per supplier/window, mandate lifetime and any shared book risk pool. An amendment/new mandate references the existing pool rather than resetting its consumed amount.

```text
executePurchaseUnderMandate(command): OwnedTx
  current actor/service permission and book lock
  replay original command BEFORE new-work limit/expiry checks
  load exact sealed plan, mandate revision and current authority witnesses
  validate plan facts/rules/versions against complete allowed pattern
  now = trusted database instant after potentially blocking locks
  bucketKeys = selected calendar windows in declared book timezone
  lock all shared budget rows in deterministic order
  require used+newGross<=eachLimit and count+1<=eachCountLimit
  require unrevoked mandate and current authorizer policy as selected
  call existing PurchaseApp.applyWithinTransaction(tx, validatedPlan)
  append consumption for original economic identity and all budget increments
  append receipt and outbox; commit everything together
```

Preparation does not consume capacity. An unsuccessful transaction consumes none. A lost successful response must replay before checking the now-full budget; it cannot count the event again. No automatic credit/reversal restores budget headroom in this first policy, because that would permit cycling exposure. Human-reviewed budget amendments remain possible and auditable.

Backdating the accounting date cannot choose yesterday's empty risk bucket. Budget time is the selected trusted execution calendar; accounting eligibility has its separate approved date rule. A task waiting beyond mandate expiry is no longer eligible merely because its plan was prepared earlier.

## Rollout, suspension and output

Begin shadow mode: evaluate proposed executions and reasons without any new authority use. Promotion needs actual supported journey/race evidence and human activation, not just a passing mean score. Suspension blocks new admissions; it does not erase receipts or imply admitted work failed. The authority owner must prove ordering with revocation, shared budget consumption and other human executors using the same pool.

```text
limit100000, consumed70000, eligible event25000 -> consumed95000
another10000 -> refused, no journal or partial budget increment
same25000 request after commit/expiry -> original receipt, still consumed95000
two concurrent events20000 at used70000 -> at most one fits
new mandate same supplier/pool -> existing pool usage retained
```

UI shows exact scope, expiration, remaining limits, each autonomous receipt and the human who activated the rule. No existing operation gains this authority simply because a default permission annotation was omitted.


---

<a id="part-24"></a>

# NEXT-122: Cash-constrained payment proposals with explicit optimization bounds

**Priority when applicable:** P1. **Owner lane:** TREASURY.

**New scope:** Cash forecasts explain expected balances and budgets constrain authorization. Add a read-only constrained selection/scheduling proposal over actual payable capacity; it does not alter debts, due dates or initiate payment.

**Existing owner to extend:** Existing Cash contribution graph, contractual payment terms, disputes/reservations and payment-plan preparation owners.

**Earlier contracts:** NEXT-71, NEXT-80. **This-wave dependencies:** None.

**Conditional:** NEXT-59: installment promises define permitted partial payment options; NEXT-67: reviewed spending policy contributes constraints; NEXT-99: historical forecast accuracy informs separately reviewed assumptions.

**Basis:** R02, P59, P99 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Fixed problem definition

```text
PaymentProposalBasis {
  horizonDates, reviewedOpeningLiquidity, unchangedBaseContributions,
  candidates: [{obligationId, remainingAmount, allowedPaymentDates,
                legalPartialOptions, mandatoryConstraints, priority, sourceRefs}],
  liquidityFloorByDate, account/currencyPerimeter,
  sourceCoverage, solverPolicy, exactBasisDigest
}
SolverResult {
  selection, objectiveVector, liquidityPath,
  notSelectedObligations, infeasibilityWitnesses,
  searchBudget, bestKnownBound, proofStatus
}
```

Separate contractual due date, agreed extension and proposed payment date. A suggested delay does not amend the creditor's rights or hide overdue status. The system must not invent priorities from legal stereotypes, recommend concealment or omit taxes/payroll obligations it failed to read. The operator selects explicit hard constraints and priorities from qualified facts.

## Avoid double-counting cash

Build the base forecast by excluding exactly the candidate payment contributions that this solver will reinsert. Preserve already dispatched/unknown payment instructions as committed constraints with their current cash treatment; do not make them freely optional. A prior tax transfer or invoice already represented in a batch cannot appear as another outflow.

Initial solver scope is one book currency/account perimeter, a bounded horizon and known finite payment options. Multi-currency FX execution and arbitrary fractional payment amounts are outside the first profile. Partial amounts must be allowed by the existing term/payment owner, not cut down by the solver to make feasibility easier.

## Bounded exact search

```text
searchPaymentOptions(basis):
  reject incomplete mandatory source coverage for an executable recommendation
  sort candidates/options deterministically
  frontier = initial state with unchanged base cash path
  bestFeasible = none
  while frontier not empty AND workBudget remains:
    state = pop best optimistic objective bound
    choose next candidate
    for option in permitted complete/partial/date choices:
      next = state plus option
      update exact cumulative daily cash and hard obligation constraints
      if hard constraint violated: prune with witness
      if unassigned options are outflows only and next breaches floor: prune
      optimisticBound = chosenScore + best possible unassigned scores ignoring liquidity
      if cannot beat bestFeasible under declared lexicographic objective: prune
      if all assigned: validate full exact feasibility and retain best
      else push next
  return feasible candidate plus declared search/proof status
```

The objective's integer priorities and date penalties are a reviewed product policy, not money or a statutory ranking. Stable tie-breaking means deterministic selection, not a guarantee the choice is economically optimal beyond the declared model.

Statuses distinguish proven optimum within the finite model, feasible but search-bounded, proven infeasible within model, incomplete input and no candidate found before budget exhaustion. The last is not proof that no solution exists. For infeasible mandatory outflows, display the exact minimum shortfall/date rather than deleting a mandatory candidate.

## Approval and execution handoff

A saved proposal binds its captured basis and explainable decisions. It has no payment authority. The operator can select its exact result, then the existing payment owner recaptures current payables, holds, beneficiary details and available instruction capacities and prepares a new approval-bound payment batch.

If a material basis changed, show the difference and require review. No plan adjusts legal due dates, relaxes a dispute hold, releases a live instruction or bypasses NEXT-96 approval routing. Actual bank liquidity may change after the calculation; a feasible forecast is not a guarantee a payment will clear.

## UI and examples

Show each chosen/omitted obligation, cash-floor effect, changed expected dates, stated assumptions and why a better-looking alternative was excluded. Missing future income is not silently assumed guaranteed. A stress view can place same-day outflows before uncertain inflows.

```text
available100000; mandatory tax60000; optional invoice50000 -> shortfall10000 if both
allowed explicit installment40000 -> feasible100000 if creditor terms permit
no installment permission -> solver cannot invent40000 payment
search interrupted with one feasible option -> feasible_bounded, not optimal
chosen obligation already included in base forecast -> remove original contribution once
```

Completion requires exact model reconciliation, bounded-search outcomes and current payment-preparation handoff. No autonomous disbursement power is added by this packet or by NEXT-121.


---

<a id="part-25"></a>

# NEXT-123: Autogiro mandates and direct-debit collection outcomes

**Priority when applicable:** P1. **Owner lane:** DELIVERY.

**New scope:** Payment links ask a customer to pay; supplier payment exports initiate outgoing payments. Add authorized direct-debit collection of customer receivables, with payer mandates and returned-payment effects.

**Existing owner to extend:** Existing customer residual, bank-source, external-attempt, notification and payment-capacity owners.

**Earlier contracts:** NEXT-30. **This-wave dependencies:** None.

**Conditional:** NEXT-59: collecting contractually defined installments; NEXT-100: publishing customer integration events.

**Basis:** X11, P30, P71 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Select one actual scheme/bank profile

Bankgirot describes separate payer-consent and payment submission/cancellation workflows through the bank-connected service [X11]. Acquire the exact current agreement, message/status files, notification timing and supported cancellation/return semantics before activation. Do not infer successful collection from the service's marketing description or an accepted file.

```text
DebitMandateRevision {
  customerPayerIdentity, creditorAgreement, mandateReference,
  exactEligibleAccountBinding, actualConsentEvidence,
  providerAcceptance, validScope, revocation/terminationEvidence
}
CollectionIntent {
  originalInvoiceOrInstallmentRefs, mandateRevision,
  exactAmount, currency, collectionDate, noticeArtifact,
  oneEconomicCollectionIdentity, approval, reservation
}
CollectionOutcome {attemptId, providerReference, rawMessage, typedState, bankEventRef?}
```

Payer consent authorizes the scheme-specific debit, not issuance of a new invoice or an arbitrary amount. A recurring invoice template cannot authorize a new mandate by itself. Company-side authority and required payer notices remain separate prerequisites.

## Prepare and reserve

```text
prepareCollection(invoiceSelection, mandate):
  require actual mandate/provider acceptance and permitted payer/invoice relationship
  capture current residuals, disputes, credits, existing payment reservations and term dates
  require proposed amount <= free collectible capacity
  apply actual bank-calendar/notice/cutoff rules from selected scheme
  render exact required notice and retain its appropriate delivery evidence
  seal attempt payload and intended date; require authorized collection approval
```

Dispatch admission reserves the actual collectible capacity under the shared customer/payment owner. Another payment link, manual collection or direct debit cannot reserve the same free amount unnoticed. An unexpected voluntary payment can still arrive after admission; retain it as real cash and resolve any resulting surplus through NEXT-30.

Network/file delivery occurs outside the financial transaction. Stable collection/provider identity and authenticated observations recover ambiguous response loss. Failed/unaccepted consent is not a successful collection. A mandate revoked before admission blocks dispatch; a later revocation does not prove an already admitted debit never happened.

## Accounting only on qualified financial evidence

```text
recordCollectedCash(outcome, bankOrSchemeCashEvidence):
  require actual supported final cash amount/currency and source identity
  debit bank or qualified scheme cash-clearing amount
  credit customer receivable amount
  consume invoice principal and convert the matching reservation to completed use
  save financial receipt and source links atomically
```

If the bank cash is already posted into the scheme clearing owner, adopt its exact unused components without debiting bank again. Provider instruction accepted and payment booked are distinct fields. A rejected instruction releases reservations only under evidence proving the amount will not execute; a local timeout or queue cancellation is insufficient.

## Returns and conflicts

A return after a posted collection is a new actual financial event, not deletion of the original payment. In the first unconsumed supported case, debit AR and credit bank/clearing, append the owned allocation reversal and retain the scheme return identity. Fees are separate evidenced expenses.

If later credits, refunds or setoff consumed the resulting customer balance, require the complete customer-credit/settlement correction path. Do not simply reopen full principal while leaving an already refunded credit liability uncorrected. Retain the bank return and mark its unresolved accounting impact; complete reconciliation cannot ignore the actual movement.

Cancellation of a collection is separate from termination of the mandate. A material mandate or date change requires new preparation. It cannot reuse an unknown previous instruction's capacity. No unsupported automatic retries of rejected bank collections are invented.

## Interface and vectors

```text
invoice125000, paid25000 -> eligible collection<=100000
accepted instruction100000 -> posted AR unchanged until qualified cash evidence
booked100000 -> AR0, one collection receipt
later full unconsumed return100000 -> AR100000, original cash history retained
mandate revoked before admission -> no new request
payment-link capture arrives while debit pending -> retain both real outcomes,
    resolve surplus under customer-credit owner instead of suppressing cash
```

Completion is one bank-qualified consent/notice/collection/return workflow with authorized evidence. No exact file record codes, provider cutoff or refund rights are invented by the pseudocode.


---

<a id="part-26"></a>

# NEXT-124: Bank-feed provider handover with continuity evidence

**Priority when applicable:** P1. **Owner lane:** BANKING.

**New scope:** Add operational replacement of a read-only feed provider for the same real bank account. Historic import and one provider sync do not by themselves prove continuous coverage or safe cross-provider identity.

**Existing owner to extend:** Existing bank account identity, source occurrences, sync generations, matching and consent owners.

**Earlier contracts:** NEXT-09, NEXT-10. **This-wave dependencies:** None.

**Conditional:** NEXT-70: independent control comes from a supported structured statement; NEXT-97: ambiguous grouped overlap needs candidate discovery.

**Basis:** R02, P09, P70 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Two streams, one bank-account authority

```text
FeedHandoverPlan {
  realBankAccountId, oldConnection, proposedConnection,
  independentlyVerifiedAccountIdentity, old/newProviderScopes,
  overlapInterval, cutoverPolicy, originalCoverageRefs,
  observationMappingManifest, unmatchedItems, digest
}
ObservationAliasDecision {
  oldSourceOccurrence, newSourceOccurrence, canonicalBankObservation,
  relationshipEvidence, matchingVersion, reviewIdentity
}
FeedSelectionEpoch {bankAccountId, eligibleSourceStreamsByInterval, handoverReceipt}
```

Provider account IDs are namespaced source identities. They are not the actual bank account merely because the strings are similar. Establish ownership, currency and account identity using qualified independent bank evidence. No new GL bank account or opening-balance voucher is created for a provider change.

## Shadow intake and overlap reconciliation

```text
prepareHandover(old,new):
  retain new provider observations in shadow source state
  retrieve a bounded explicit overlap and preserve both originals
  compare account/balance/coverage assertions using independent statements
  identify exact shared bank transaction IDs when both providers genuinely supply them
  otherwise use NEXT-97 only to propose reviewed same/different-event relationships
  seal complete compared memberships and unresolved gaps
```

Equal amount/date/text alone is not an automatic alias. Two legitimate equal purchases remain two movements. Pending-to-booked relations use provider evidence and the existing source owner. A removed/modified observation can produce an impact case on already matched accounting rather than silently deleting the old canonical record.

Alias decisions attach new provenance to an existing canonical bank observation without creating another source capacity. Already reviewed bank matches and financial receipts remain attached to the same economic movement. A genuine new movement is admitted normally. A residual gap remains unknown coverage, not zero activity.

## Cutover transaction

```text
executeHandover(plan): nonfinancial admitted tx
  lock bank-account source-selection identity and relevant stream versions
  replay original command first
  require new consent and complete approved account/overlap witness current
  require reviewed source interval selection has no unacknowledged gaps/duplication
  append source-selection epoch and all validated alias/admission links
  fence old stream from new canonical publication after selected boundary
  retain old originals, cursors and published generations as history
  save handover receipt; invalidate affected live coverage/matching summaries
```

Do not hold a transaction across provider calls. Old in-flight read results may still arrive; they are retained according to the permitted source policy but cannot publish under a superseded epoch. Read-only provider cutover does not cancel unrelated banking payment mandates or external transfers.

A source-selection rule can retain the old stream for historical ranges while selecting the new stream going forward. It does not retroactively rewrite a report snapshot's original provider evidence. Failed new-provider synchronization leaves explicit current unavailability; it cannot quietly revert the source selection and admit duplicate overlap activity.

## Disconnect and restore behavior

Only disconnect the old connection after reviewing its remaining read/recovery needs and current actual consent authority. Revoking a provider token changes retrieval capability, not retention of legitimately held originals. The data-retention policy separately governs private source preservation. A backup restore starts with delivery fenced and must re-establish the selected current consent/epoch before activating either stream.

Rollback before cutover can discard shadow eligibility, not original evidence. After canonical adoption, a return to the old provider is another reviewed source-selection transition, not deletion of the handover or reimport of old balances.

## Controls and examples

```text
old feed balance100000, new feed same real account100000 -> GL opening delta0
oldTxnA/newTxnB proven same bank movement5000 -> one canonical capacity5000
two5000 transactions without unique evidence -> ambiguous, no automatic merge
late old response after cutover -> retained source but stale publication denied
new feed lacks last2 days -> coverage incomplete, not a clean continuity certificate
```

UI shows providers, retained account identity, overlap mappings, unresolved items and which stream covers each interval. Completion requires actual independent control evidence and observed no-duplicate handover in the selected provider pair, not merely saving a new API credential.


---

<a id="part-27"></a>

# NEXT-125: Processor refund initiation with reserved entitlement and outcome recovery

**Priority when applicable:** P1. **Owner lane:** DELIVERY.

**New scope:** NEXT-30 owns customer refund liability and NEXT-39 records processor movements. Add the authorized external refund request and its in-flight financial bridge instead of treating a local refund record as money sent.

**Existing owner to extend:** Existing customer-credit/refund capacity, processor source events and authenticated external attempts; Stripe card refunds are the first bounded profile.

**Earlier contracts:** NEXT-30, NEXT-39. **This-wave dependencies:** None.

**Conditional:** NEXT-64: the original charge was created through the invoice payment-link owner.

**Basis:** X12, P30, P39 in [SOURCES.md](SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Exact request authority

```text
RefundInstruction {
  book, processorAccount/mode, originalChargeIdentity,
  customerRefundOrigin, amount, currency,
  currentLocalLiabilityCapacity, providerRemainingRefundabilityWitness,
  originalDestinationPolicy, exactPayloadHash, approval,
  requestId, providerIdempotencyKey, cancellationVersion
}
RefundOutcome {instruction, actualProviderRefundId, status, rawEvidence, balanceTxnRefs}
RefundTransitEffect {instruction, processorOutflow, discharge, returnedFunds, journalRefs}
```

Stripe permits partial refunds against an original charge and restricts total refundability. Refunds return through the original payment mechanism; pending/failed/cancelled outcomes and later returned-funds records must be handled [X12]. Do not offer an arbitrary bank beneficiary through the original-charge refund API or copy unsupported Connect/other-payment-method semantics into this card profile.

## Prepare and admit

```text
prepareProcessorRefund(origin, amount):
  require approved commercial credit/overpayment entitlement, not just a desire to refund
  capture local available refund capacity and existing pending disbursements
  retrieve exact original provider charge and its refund inventory outside locks
  require account, mode, currency and customer relationship match
  require no unresolved competing refund/dispute preventing this selected action
  seal amount and original destination; require separate money-movement approval

admitRefund(plan): OwnedTx with no new cash journal
  replay first; verify local refund and attempt versions
  reserve entitlement and instruction amount at shared customer-payment owner
  persist one external attempt/payload and required outbox intent
```

Provider checks remain subject to concurrent manual dashboard action. A later provider refusal is retained, not forced through by changing the amount under the old approval. Reconcile both local rights and processor reality.

## Dispatch and uncertainty

Call the actual refund API outside the transaction with the saved provider idempotency key and exact charge/payment identity. Preserve returned refund IDs immediately in a short reauthorized transaction. Webhooks trigger authenticated observation/refetch, not blind financial authority. Out-of-order statuses are resolved through the current actual object and retained event evidence, not whichever event arrived last.

Response loss first uses known refund ID or provider-supported exact lookup/idempotency within its documented retention window. A new local key is not a provider guarantee. If the original request cannot be proved absent, keep the reserved amount and outcome unknown. Pending due to funding does not authorize a substitute bank refund.

## Financial transit and actual discharge

Some processor funds can move before the customer's claim is conclusively discharged under the selected evidence policy. Preserve both stages:

```text
observed processor refund debit A:
  debit refund-in-transit asset A
  credit processor control A

qualified refund-discharge evidence for A:
  debit customer-credit liability A
  credit refund-in-transit A
  consume customer refund capacity and convert its reservation to completed use
```

When both observations are available, execute the combined group once. NEXT-39 must identify this owned refund instruction and route/adopt its financial component, not also post its generic customer-refund journal. Original balance-transaction identity is unique across retrieval/webhook/payout views.

If funds return before discharge, debit processor control and credit transit, then release the instruction reservation only after qualified final no-execution evidence. If the customer liability had already been discharged, a genuine reversal restores it with a linked refund-settlement reversal, not a fresh sales credit or VAT correction. Unsupported consumed later history becomes an explicit correction case, never negative untracked capacity.

Fees and original processing charges remain separately evidenced. A refund does not automatically refund the original fee or alter the commercial VAT credit. A provider success status is not a claim that the application inspected the customer's bank statement.

## Cancellation and examples

Expose cancellation only where the actual refund/profile supports it. Some card cancellations require an official dashboard flow; do not invent an API. Record the real cancellation and returned-funds evidence before reuse of capacity.

```text
customer credit50000; request20000 -> free instruction capacity30000
processor debits20000 while pending -> transit20000, credit liability still50000
qualified completion -> liability30000, transit0
failure with funds returned before completion -> liability50000, transit0,
  capacity restored only after outcome proof
same processor balance transaction retried -> no second cash/control effect
```

Completion requires one configured authorized refund and recovery path with matching local liability, processor cash and provider references. No packet or standing mandate implicitly authorizes this external money movement.


---

<a id="part-28"></a>

# Integration map and explicit non-overlap

NEXT-101..125 is a new wave, not a rewrite or an assertion that prior 100 are implemented. Keep task identities, financial owner contracts and current source ownership. Resolve the actual checkout and active reservations at dispatch. A module/function equivalent already delivered since planning should be reused and qualified, not recreated to match this packet's suggested name.

## New work and dependencies

| Packet | Earlier contracts | New-wave dependencies | Conditional integration |
|---|---|---|---|
| [NEXT-101](packets/NEXT-101.md) | NEXT-50 | None | NEXT-98: a client delegates an accountant period-review engagement |
| [NEXT-102](packets/NEXT-102.md) | NEXT-26, NEXT-65, NEXT-93, NEXT-98 | None | NEXT-101: the requester uses firm-to-client delegated access |
| [NEXT-103](packets/NEXT-103.md) | NEXT-13, NEXT-23, NEXT-95, NEXT-98 | None | NEXT-102: missing supporting evidence is requested from a client |
| [NEXT-104](packets/NEXT-104.md) | NEXT-13, NEXT-14 | None | NEXT-43: the selected analytical view uses reviewed classification revisions |
| [NEXT-105](packets/NEXT-105.md) | NEXT-13, NEXT-58, NEXT-77, NEXT-79 | NEXT-104 | NEXT-78: milestone/retention balances enter the selected project |
| [NEXT-106](packets/NEXT-106.md) | NEXT-56, NEXT-58, NEXT-76, NEXT-77 | None | None |
| [NEXT-107](packets/NEXT-107.md) | NEXT-13, NEXT-76, NEXT-79 | NEXT-105 | NEXT-42: a related asset impairment assessment must precede contract-loss recognition |
| [NEXT-108](packets/NEXT-108.md) | NEXT-03, NEXT-13, NEXT-51 | None | None |
| [NEXT-109](packets/NEXT-109.md) | NEXT-03, NEXT-13, NEXT-19 | None | None |
| [NEXT-110](packets/NEXT-110.md) | NEXT-32, NEXT-71 | None | NEXT-22: a book gain or cost needs separate corporate-tax treatment |
| [NEXT-111](packets/NEXT-111.md) | NEXT-03, NEXT-04, NEXT-22, NEXT-49 | None | None |
| [NEXT-112](packets/NEXT-112.md) | NEXT-03, NEXT-04, NEXT-51, NEXT-15 | None | None |
| [NEXT-113](packets/NEXT-113.md) | NEXT-51, NEXT-49 | None | NEXT-39: proceeds arrive through a processor; NEXT-53: a qualified goods supply rather than service is selected |
| [NEXT-114](packets/NEXT-114.md) | NEXT-03, NEXT-49 | None | NEXT-17: an approved foreign-currency refund receivable needs supported FX settlement |
| [NEXT-115](packets/NEXT-115.md) | NEXT-33, NEXT-20, NEXT-21 | None | NEXT-34: the same retained trip also includes a mileage award |
| [NEXT-116](packets/NEXT-116.md) | NEXT-20, NEXT-21, NEXT-35 | None | None |
| [NEXT-117](packets/NEXT-117.md) | NEXT-32, NEXT-49 | None | NEXT-62: received late-payment interest creates an applicable reporting obligation |
| [NEXT-118](packets/NEXT-118.md) | NEXT-20, NEXT-21, NEXT-87 | None | NEXT-36: an already paid or reported period requires a supported correction |
| [NEXT-119](packets/NEXT-119.md) | NEXT-02, NEXT-13, NEXT-49, NEXT-89 | None | None |
| [NEXT-120](packets/NEXT-120.md) | NEXT-22, NEXT-49 | None | NEXT-74: linking final annual filing outcomes; NEXT-99: later scoring the retained estimate against actual tax outcomes |
| [NEXT-121](packets/NEXT-121.md) | NEXT-02, NEXT-03, NEXT-16, NEXT-96 | None | None |
| [NEXT-122](packets/NEXT-122.md) | NEXT-71, NEXT-80 | None | NEXT-59: installment promises define permitted partial payment options; NEXT-67: reviewed spending policy contributes constraints; NEXT-99: historical forecast accuracy informs separately reviewed assumptions |
| [NEXT-123](packets/NEXT-123.md) | NEXT-30 | None | NEXT-59: collecting contractually defined installments; NEXT-100: publishing customer integration events |
| [NEXT-124](packets/NEXT-124.md) | NEXT-09, NEXT-10 | None | NEXT-70: independent control comes from a supported structured statement; NEXT-97: ambiguous grouped overlap needs candidate discovery |
| [NEXT-125](packets/NEXT-125.md) | NEXT-30, NEXT-39 | None | NEXT-64: the original charge was created through the invoice payment-link owner |

## Delta from earlier work

**NEXT-101.** NEXT-98 owns a period review. Add firm membership, client-granted scopes and a multi-client queue without turning a reviewer into a book administrator.

**NEXT-102.** Add an explicit request/reply workflow for missing facts or documents. Search, upload and a review finding alone do not say who was asked, what they supplied or whether the request was satisfied.

**NEXT-103.** Add per-account explained balance schedules and preparer/reviewer certification. This supports an existing close/review; it is not another close certificate or journal reconciliation engine.

**NEXT-104.** NEXT-43 changes analytical labels. Add conserved fractional attribution of one shared cost to several recipients without duplicating costs or modifying the financial journal.

**NEXT-105.** Add a coherent project-performance snapshot combining contract rights, earned revenue, allocated cost and actual cash. It does not replace P&L, Cash forecasts or contract recognition.

**NEXT-106.** Add unit-denominated contractual service rights and consumption against prepaid retainers. Customer advances track money; recurring invoices track billing dates; neither alone tracks remaining service entitlement.

**NEXT-107.** Add reviewed loss obligations on remaining service contracts. Project margin is a report and unbilled revenue is an asset; neither records a qualified future unavoidable loss.

**NEXT-108.** Add an assurance-warranty obligation and claim-cost lifecycle. A customer refund, billed service warranty or asset impairment is not the same liability.

**NEXT-109.** Add insured-loss claims, recognized recoveries and insurer-to-repairer settlements. Insurance compensation is not ordinary sale proceeds or a grant and must not hide gross damage/repair effects.

**NEXT-110.** Extend existing loan principal/interest with evidenced rescheduling and extinguishment. Merely editing a rate or due date must not erase debt or create an unsupported modification gain.

**NEXT-111.** Invoice-level partial deduction already exists. Add a qualified final common-cost allocation over a complete annual population and post only the difference from effective deductions.

**NEXT-112.** Add a qualified domestic construction reverse-charge profile. Cross-border services and ROT/RUT claims do not establish the seller/buyer conditions for this treatment.

**NEXT-113.** Add destination-tax consumer sales and a distinct Union OSS obligation. Earlier EU B2B sales and periodisk sammanställning do not cover this reporting family.

**NEXT-114.** Add foreign VAT recovery from the foreign authority. A foreign tax amount must not be claimed as Swedish deductible input VAT merely because it appears on a purchase.

**NEXT-115.** Mileage reimburses distance. Add overnight business-travel allowance eligibility, country/day classification and separate meal reductions/benefit inputs without reusing the mileage rate formula.

**NEXT-116.** Payroll already accepts benefit inputs. Add a concrete retained car-benefit eligibility/valuation lifecycle and payment reconciliation so those inputs are not anonymous monthly amounts.

**NEXT-117.** KU31 covers dividends and AGI covers compensation. Add annual interest reporting with its own reporter/recipient, timing and correction rules rather than treating every loan accrual as a reportable amount.

**NEXT-118.** Add an effective-dated employee/employer salary-exchange agreement with distinct salary and pension bases. Pension invoice reconciliation alone does not define the waived salary or prevent double deductions.

**NEXT-119.** Dividends distribute existing equity. Add the company-side record of cash subscriptions, paid allotments and an evidenced capital-registration transition without inventing share rights from bank receipts.

**NEXT-120.** Annual current-tax calculation and final INK2 filing already have owners. Add a separately labelled forecast-based preliminary declaration, its revised authority decision and the payment-schedule impact.

**NEXT-121.** Multi-human approval covers exact plans. Add an explicitly enabled later-scope authority for a narrowly allowed recurring purchase pattern, with atomic cumulative limits. Book Zero remains exact-human-approval by default.

**NEXT-122.** Cash forecasts explain expected balances and budgets constrain authorization. Add a read-only constrained selection/scheduling proposal over actual payable capacity; it does not alter debts, due dates or initiate payment.

**NEXT-123.** Payment links ask a customer to pay; supplier payment exports initiate outgoing payments. Add authorized direct-debit collection of customer receivables, with payer mandates and returned-payment effects.

**NEXT-124.** Add operational replacement of a read-only feed provider for the same real bank account. Historic import and one provider sync do not by themselves prove continuous coverage or safe cross-provider identity.

**NEXT-125.** NEXT-30 owns customer refund liability and NEXT-39 records processor movements. Add the authorized external refund request and its in-flight financial bridge instead of treating a local refund record as money sent.

## Root-owned integration

Root composes shared operation contracts, principal/admission and lock ordering, journal writes, schema/grants, common residual projections, capability registration and top-level UI/job routing. Domain workers provide pure calculations, named Effect services, tx-passing persistence and local UI. No nested runtime/transaction or public HTTP call can make an atomic multi-owner group.

A true new financial consequence needs its related journal, tax/register/source rights and receipt in the same tx. A read-only report or classification overlay does not receive a ledger-write path to fix its own differences. Every new mutation must participate in common balance/currentness consumers.

Priorities are applicability-relative. P1 collaboration and operational automation need actual usable source owners. P2 specialist tax, salary or provision profiles are not a reason to postpone an otherwise complete ordinary company. Missing integration in an earlier packet stays there rather than being renamed a new task.

## Concrete contract handoffs

| Existing owner | Consumer | Exact preserved meaning |
|---|---|---|
| Identity and review98 | 101/102 | Effective client scopes and original reviewer identity, not a copied superuser token |
| Evidence/requested facts | 102/103 | Original reply/document revisions, independent support and explicit unresolved items |
| Report and classifications13/14/43 | 103/104/105 | Fixed original contribution IDs and amounts, plus explicit analytical mode |
| Contract/work76/77 and deferral58 | 106 | Once-only work coverage and existing financial liability, not a second invoice |
| Expense/payroll/asset owners | 107/108/109 | Real costs/losses recognized once, separate provision/recovery rights |
| Borrowing32 | 110 | Principal/interest histories and actual payment reservations |
| Tax facts03/04 and VAT amendments | 111/112 | Original source-tax capacity and new qualified adjustment/treatment facts |
| Sales/order/processor owners | 113 | One sale identity with separate country/scheme tax and book/report currencies |
| Original purchase and FX | 114 | Foreign tax retained separately from Swedish VAT; exact approved receivable |
| Claim/payroll20/21/33/87 | 115-118 | Cash, noncash, original liabilities and paid/provided reporting facts stay distinct |
| Company/shareholder89 | 119 | Actual resolution/unit rights and registered status, not bank-text inference |
| Corporate tax/Cash | 120/122 | Actual facts and hypothetical forecasts remain labelled and nonduplicated |
| Existing approval96 and purchase | 121 | New explicit authority union and shared cumulative pool, never a fake approval |
| Customer residual and delivery | 123/125 | Shared in-flight reservation and observed discharge, not independent paid flags |
| Source sync09/10 and matching | 124 | Original cash-event identity survives provider replacement |

## Nonfinancial versus financial closure

103 substantiates a captured account; it does not close the book.104 allocates analytical cost without changing VAT.105 reports margins; it cannot recognize revenue.120 estimates provisional tax; it cannot replace an authority decision.122 proposes payments; it cannot send them.121's bounded posting mandate expressly excludes payments/refunds/signing/filing.

The new mandate packet is explicitly later scope, opt-in and disabled by default. All default human-approval workflows remain. Its activation, budgets and revocation must be integrated and observed across every allowed operation before it can be advertised.

## Suggested owner lanes

Begin independently with101 firm/client scope design,103 substantiation over released reports,104 shared-cost attribution and122 payment-proposal analysis once the needed readers exist.102 joins the delegated evidence workflow but can operate with ordinary direct-client authority before101 is activated. Specialist financial/tax profiles follow actual company demand.

Do not start25 simultaneous writers. Payroll115-118 share component identities and require one integration owner. Tax111-114 share facts but not declaration identities. Delivery123/125 must agree on the shared customer refund/collection capacity before parallel work. Source handover124 must not rewrite the canonical bank identity used by those financial flows.

## Worker handoff

Return changed paths, exact exported operations, source/calculator versions, schema/grant requirements, complete effect groups, declared dependencies, actual executed checks, retained receipts/artifacts and remaining blockers. Distinguish source-present from complete observed journey. No new package tests, provider requests, resets or deployments are authorized by this text.


---

<a id="part-29"></a>

# Design decisions for NEXT-101 through NEXT-125

These decisions define new bounded product behavior. They do not establish that the first 100 packets are implemented, qualify a statutory profile or authorize an actual financial operation. The shared Effect transaction contract and the earlier financial owners remain in force.

## 1. Delegation is an intersection of permissions, not an account copy

A firm employee can act for a client only when the client's active grant, the firm's role, the particular employee's assignment and the selected book/period/privacy permissions all allow the operation. A client grant cannot turn every firm employee into an operator. Payroll access remains separately scoped.

Portfolio views run authorized per-book reads and identify each capture's cutoff. They do not imply a cross-book transaction or consolidated financial statement. Current access is required even when reading a saved client report. A revoked relationship must not leave a confidential stale cache visible through an old portfolio selection.

## 2. Uploading a response does not resolve the accounting question

An evidence request has a fixed requested scope and a reply relationship. A submitted file is a response, not proof that it answers the request or establishes the asserted fact. The reviewer selects and confirms the relevant source evidence through the owning accounting/case operation. The request then records the exact resolution evidence.

A new reply to a previously resolved question can create an impact review. It does not overwrite a posted invoice, signed artifact or old review acceptance. Guest tokens grant access only to their request and permitted response operation.

## 3. Substantiation and analytical allocation have separate purposes

A substantiation schedule explains a selected balance at a frozen financial cutoff using its original components and genuinely independent evidence. Another query over the same ledger can establish arithmetic consistency but is not independent evidence that the transaction occurred.

Shared-cost attribution is an analytical partition. Every source cost is counted once, either directly or through its selected allocation shares. It creates no new expense or VAT entry. For an exact source amount of 10,001 and weights 1:2, the declared largest-remainder policy yields 3,334 and 6,667. The unfiltered total stays 10,001.

A financial reclassification of an account or tax treatment is not disguised as an analytical allocation. It remains an approved operation at the original financial owner.

## 4. Project margin uses recognized revenue, not whichever cash figure is available

The project view identifies billed consideration, earned revenue, unbilled assets, deferred revenue, cash and recognized costs separately. These are joined through retained source coverage, not assumed to be interchangeable.

A useful reconciliation is:

```text
recognized revenue = billed net
                   + movement in earned-unbilled revenue
                   - movement in deferred revenue
```

The actual qualified recognition events remain the authority. The equation is a reconciliation witness, not permission to manufacture missing revenue. Cash collection and customer credit are separate views. Shared analytical costs come from NEXT-104 without duplicating direct costs.

## 5. Service retainers consume entitlement and financial coverage together

A retainer covers a finite nontransferable service entitlement under a specific contract. It is not a generic financial wallet or gift-card scheme. The advance, tax and deferred-revenue owners retain their earlier financial effects.

Using 150 of a retained 600-minute entitlement funded by net consideration of 100,000 releases 25,000 of that deferred consideration under the illustrative proportional policy. The remaining entitlement is 450 minutes and the remaining deferred amount is 75,000. The same work component cannot also become an ordinary billable time entry.

Expiry does not automatically turn the remaining liability into revenue. Refund, extension, cancellation and enforceable expiry use the applicable reviewed contract and qualified recognition policy.

## 6. Provision targets are remeasured against effective prior provisions

The onerous-contract and warranty packets are qualified provision profiles, not extensions that every K2 company automatically needs. Eligibility, unavoidable cost, recoveries and actual obligation evidence must be established before measurement.

For a supported onerous remaining contract, the target is the reviewed unavoidable net loss. A later measurement posts target less the effective remaining provision, after recorded consumption. The actual fulfillment cost is not the same thing as the provision release. For warranty cohorts, the target must reflect claims already settled and the remaining eligible exposure rather than reusing the original unit count forever.

A valid provision cannot become an automatic smoothing reserve. Independently justified estimate changes retain their evidence, rate/model version and effect history. Repairs, invoices and payroll that consume a provision reuse their existing recognition owners rather than create the cost twice.

## 7. Insurance and debt forgiveness preserve the underlying event

Damage, disposal or repair is accounted for separately from insurance recovery. A claim request is not automatically an asset. Recognize a recovery only when the selected profile's entitlement/evidence threshold is met. Direct insurer payment of a supplier invoice reduces the payable and insurance receivable without inventing a bank movement.

Loan rescheduling retains outstanding principal and accrued interest. Legally effective forgiveness identifies the exact recognized components being extinguished. Cancelling unaccrued future interest is not a gain equal to all of those hypothetical payments. An amended bank instruction must resolve existing reservations and unknown outcomes before replacement.

## 8. Annual VAT true-up changes deduction, not supplier consideration

Select the complete eligible common-cost population and the qualified final allocation method. Do not apply one turnover ratio to every purchase. Directly attributable costs, disallowed costs, capital-goods adjustments and private-use questions have their own treatment.

For each selected original component:

```text
new deduction adjustment = qualified final target
                         - effective deduction already recognized
```

An additional deduction for an already fully expensed cost debits input VAT and credits the attributable non-deductible cost. Supplier payable and cash remain unchanged. Repeating the same target produces zero additional deduction. A source credit or changed driver requires a fresh complete basis; the existing VAT amendment owner handles declaration consequences.

## 9. Specialized VAT families do not borrow domestic return identity

Domestic construction reverse charge requires the supported service and customer facts. Ordinary invoicing with a zero tax rate is not equivalent because the required reverse-charge basis, notices and buyer-side effects still exist.

Union OSS keeps country/scheme liabilities, original-sale identity and reporting-currency conversion distinct from ordinary domestic VAT. The book carrying value and euro reporting target can legitimately differ; their reconciliation requires its own qualified conversion/settlement effects. One economic sale cannot appear as two recognitions because both the order and processor deliver records.

Foreign EU input-VAT recovery is also distinct. A foreign tax amount is not deductible Swedish input VAT merely because it appears on an invoice. Initial recovery eligibility, a recognized approved entitlement and the actual refund are separate stages.

## 10. Payroll sources have different cash, tax and expense effects

Travel-allowance reduction and a taxable meal benefit are independently classified. A meal can affect one or both according to its applicable facts; the calculation cannot assume they are the same amount or event. Mileage remains its existing separate award.

A recurring car benefit is a noncash tax/reporting base, not another purchase cost. An actual qualified net payment by the employee may reduce that base. A gross salary reduction is not automatically the employee paying for the benefit.

Prospective salary exchange changes the agreed future cash salary and creates the corresponding pension entitlement under the actual agreement. It does not also subtract the exchanged amount as a net-pay deduction. The pension provider invoice consumes already accrued obligations; it must not duplicate the pension expense. Retrospective paid cases use the existing correction owner.

## 11. Tax statements and capital events use real identities and conditions

KU20 and KU25 have different reporter/recipient obligations. A company paying interest to its bank is not automatically required to create a KU25 for itself. Accrual, reportable availability, cash payment and withholding are retained separately under the qualified reporting profile. Replacement preserves the required statement identity.

A cash share subscription has actual resolution, payment, allotment and registration conditions. Cash received is not proof of registered share capital. Under the selected illustrative profile, pending funds transition into unregistered nominal/premium components, then into their registered classifications when evidenced. Overpaid cash does not silently issue more shares.

## 12. Preliminary-tax estimates do not alter assessed installments

The estimated annual tax and the authority's currently effective preliminary schedule are separate records. A lower forecast does not reduce the next legal installment until a qualifying decision changes it. Actual tax-account debits and payments remain their respective source-backed effects.

The annual current-tax expense is not calculated by subtracting bank payments from the expected tax amount. Estimated expense, prepayments, assessed liabilities and settlement controls must reconcile without collapsing into a single net number.

## 13. A standing mandate is a new, explicit authority kind

Book Zero keeps exact human approval as its default. NEXT-121 introduces a deliberately separate opt-in contract for one narrow stable purchase-recognition case. It excludes payment, refunds, legal issue, payroll, closing, correction and filing.

The initial exposure measure is gross recognized purchase amount, not the sum of debit and credit lines. Supplier, daily and lifetime limits share atomic consumption rows. Renewing or replacing a mandate cannot reset the shared budget. A credit does not automatically replenish exposure in the initial policy.

The financial effect and budget consumption commit together. Current admission is still checked, but successful identical replay precedes new-work limit and expiry checks. With a limit of 100,000, used amount 70,000 and a new event of 25,000, usage becomes 95,000. A replay stays 95,000; another 10,000 is refused. Two competing 20,000 events cannot both fit.

## 14. Cash-constrained proposals preserve creditors' rights

The payment planner searches a finite declared set of permitted dates, complete payments and authorized installment amounts. It never invents a smaller permissible payment because available cash is low. Candidate obligations already represented in Cash are removed once before the chosen alternatives are inserted.

Results distinguish optimal within the declared model, feasible within a search budget, proved infeasible, exhausted search and incomplete financial inputs. The deterministic objective does not turn missing source coverage into certainty. A proposal still needs fresh exact bank-payment authorization and current residual checks.

## 15. Provider continuity and refunds have their own bridges

Changing a bank-feed provider does not create a new bank account, opening balance or economic transaction. The new stream is retained and reviewed against the same account. Only proved source aliases or reviewed same-event relationships allow reuse of existing bank observations and financial capacity.

Autogiro payer consent and the company's collection authority are distinct from accounting recognition. An accepted collection instruction does not settle AR. Returned cash restores the supported original capacity through an owned correction, subject to later credits/refunds and exact source evidence.

A processor refund reserves customer entitlement before dispatch. Processor cash can leave before the customer liability is qualified as discharged. The selected transit model records those stages separately. Pending or unknown outcomes cannot justify an alternative bank refund. The processor source owner routes the same balance transaction to this refund owner instead of posting a second generic refund journal.

## Scope discipline

These are delivery contracts, not a mandate to add every specialized profile before a release. Firm workflows and service-retainer/project reporting are broad product improvements where relevant. Specialist VAT, provision, benefits, capital and collection profiles follow actual customer requirements. Existing unfinished first-wave behavior remains with its existing packet, rather than being renamed to inflate this wave.


---

<a id="part-30"></a>

# Coordinator handoff

Implement selected NEXT-101..125 from this application-owned dossier against the actual current checkout. Read current AGENTS.md, ADR0010/0009 and shared operations before assigning work. The packet IDs identify new bounded scope, not migration numbers or proof the earlier100 are complete.

Reconcile HEAD and dirty owners with the pinned source record. Reuse equivalent implementation that has already landed. Keep existing NEXT/PRY/core owners, including reserved VAT reclassification/amendment, FX partial capacity, asset controls and webshop conversion. Do not take over their incomplete integration under a new task name.

Pick work from actual company demand. Firm/evidence/project workflows are ordinary product extensions; specialist provisions, tax families, pension and equity profiles remain optional until applicable. Do not require unrelated schemes or actual external filing to develop useful independent local work.

Root owns shared schemas/grants, authority lock ordering, internal journal writer, source/economic capacity integrations, API/MCP registration and top-level UI/job composition. Workers own concrete pure calculators, named Effect operations and tx-passing persistence/local UI. Every related financial write uses one caller transaction. External operations, model calls and rendering happen outside financial locks.

All new financial effects must reach common residual/Cash/control/read owners and preserve corrections/replay. Unknown facts and failed required checks do not become zero or pass. Match declared object/array shapes, complete unsigned hash input and exact semantic IDs across application and database storage. Never remove integrity to conceal a contract mismatch.

NEXT-121 is explicitly later scope and off by default. It must introduce a supported authority union, human activation and atomic shared limits. It cannot forge approval or enable payments/refunds/filing/closing/signing. NEXT-122 is proposals only. NEXT-123/125 have their own actual money-movement permission and external outcomes.

Use current authorized checks, not permission inferred from this artifact. For each supported workflow observe actual application/storage/UI output, same-key recovery, new-key economic duplicate refusal, stale/authority failure, concurrent capacity use and a late rollback. Read-only work needs correct snapshots, privacy, counts and drilldown. External acceptance requires authentic observed provider or official-channel evidence.

Return exact changed files, owner exports, schema/grant requirements, validated equations, executed evidence and unresolved gates. No check of this dossier is an ERP test. A task cannot be marked complete from a pure calculator with missing consumers or a sent request with unknown outcome.


---

<a id="part-31"></a>

# Sources, design basis and limitations

Prepared28 September 2026. Current repository planning checkpoint: `66355b62b23e3b8007c2d324f3739fbbcc96cdc0`. The branch and two operations/shared-contract documents were read during this task. The prior 76..100 attachment and51..75 index were checked for scope. The first50 definitions are carried from this conversation. No full repository audit, live application exercise or uncommitted-work inspection was performed.

Each new packet distinguishes existing owner from proposed additional capability. References do not prove absence from all code or completion of an earlier packet. Some new specialist profiles are deliberate product proposals rather than source-discovered defects. No new module is a mandatory prerequisite for an inapplicable company.

## Repository and supplied artifacts

### R01: Current main branch observation

Resolved to 66355b62b23e3b8007c2d324f3739fbbcc96cdc0 (clean up). A commit pin, not a claim of execution or completion.

https://api.github.com/repos/erik-kroon/openERP/branches/main

### R02: Application operations and future mandate boundaries

Current source read of operation ownership, tx passing, exact human review, effect-mq, governed rules, scoped context and standing-mandate requirements. Book Zero retains human approval; unattended mandates are later scope.

https://github.com/erik-kroon/openERP/blob/66355b62b23e3b8007c2d324f3739fbbcc96cdc0/docs/operations.md

### R03: Shared contracts and admission/integrity

Read lines1-180 through GitHub. Contains exact types, current authority lock ordering, snapshots, app-owned writes, group idempotency and profile/rule distinctions. No application behavior was executed.

https://github.com/erik-kroon/openERP/blob/66355b62b23e3b8007c2d324f3739fbbcc96cdc0/docs/plans/00-shared-contracts.md

### R04: Attached NEXT-76..100 dossier

README and integration map read through Files; archive index/common decisions read from the supplied mounted ZIP. It defines the preceding25 scopes and does not claim the first75 are complete.

### R05: Supplied bank-allocation application example

User-supplied source shows explicit tx-passing allocation writes, request replay and application capacity checks. Used as architectural context only, not a current-HEAD code audit or endorsement of every earlier expression.

### R06: Earlier NEXT task definitions

NEXT-01..50 scopes come from the prior conversation. NEXT-51..75 and76..100 metadata were read from their provided ZIP indexes. New deltas are crosswalked to those definitions, not proven absent from every repo file.

## Previous design identifiers

`Pnn` refers to prior packet NEXT-nn. They identify design contracts to locate in the actual checkout, not implementation assertions. `NEXT-100` and above keep their full decimal IDs. A prior pending integration is still assigned to its original owner.

- P51: Mixed-rate domestic sales and tax-inclusive prices.
- P52: Cross-border B2B service sales and customer-status evidence.
- P53: Intra-EU goods acquisition and supply accounting.
- P54: Customs imports, import VAT and landed-cost attribution.
- P55: Periodisk sammanställning with correction lineage.
- P56: Customer advances, deposits and final-invoice application.
- P57: Supplier advances and final-purchase settlement.
- P58: Invoice-driven deferred revenue and service-period changes.
- P59: Installment terms, partial due amounts and payment promises.
- P60: Payment discounts and evidenced settlement differences.
- P61: Receivable allowances, confirmed losses and later recovery.
- P62: Dunning interest and enforceable reminder fees.
- P63: Self-billed sales and buyer-issued invoice acceptance.
- P64: Invoice payment links with outstanding-bound settlement.
- P65: Scoped customer document and statement portal.
- P66: Purchase commitments and three-way invoice matching.
- P67: Commitment-aware budgets with stop and warn decisions.
- P68: Versioned BAS chart adoption and controlled annual updates.
- P69: Spreadsheet master-data import with staged reconciliation.
- P70: Structured bank-statement ingestion with exact entry lineage.
- P71: Bank-qualified payment exports and status reconciliation.
- P72: VAT declaration submission and authoritative return history.
- P73: AGI submission and stable individual correction outcomes.
- P74: INK2 filing, signature handoff and assessment attribution.
- P75: Accounting-method change with conserved recognition coverage.
- P76: Accepted contract changes and sales-order billing limits.
- P77: Time-and-materials billing with once-only work coverage.
- P78: Milestone certificates and retained contract consideration.
- P79: Earned but unbilled service revenue and later invoicing.
- P80: Supplier disputes with partial payment holds and release.
- P81: Asset work-in-progress and commissioning from purchase costs.
- P82: Component replacement, improvements and partial asset retirement.
- P83: Operating-rental contracts, refundable deposits and index changes.
- P84: Book-to-tax depreciation cohorts and excess-depreciation bridge.
- P85: Periodiseringsfond cohorts, reversals and annual tax linkage.
- P86: ROT/RUT split claims and customer-authority settlement.
- P87: Pension invoice reconciliation and SLP annual basis.
- P88: Employment termination and final-pay obligation closure.
- P89: Dividend resolutions, shareholder payables and KU31 preparation.
- P90: Conditional grants, earned funding and repayment obligations.
- P91: Apply supplier credit balances to other payable invoices.
- P92: Documented bilateral receivable-payable setoff.
- P93: Source-located evidence search and retained-page retrieval.
- P94: Read-only mailbox intake and scoped attachment routing.
- P95: Counterparty balance confirmations with independent evidence.
- P96: Multi-human approval routing and segregated review policies.
- P97: Exact covering-set reconciliation with explicit ambiguity.
- P98: Accountant period-review engagements and versioned acceptance.
- P99: Cash forecast vintage scoring and error attribution.
- P100: Scoped integration event subscriptions and delivery receipts.

Earlier referenced owners include purchase/tax recognition03/04, payroll20/21, corporate tax22, source sync09/10, private claims33/34, approved corrections36, processor39, reviewed classifications43, obligation49 and context50. Their full previous code and all design files were not re-audited for this continuation.

## Primary external references

The following are narrow verifications, not complete legal/format/provider releases. Search-returned observations are identified rather than relabelled as full-page or full-specification reviews. Supplied formulas are original proposed design conditional on the stated supported profile.

### X01: Skatteverket: allocation of input VAT

Official search-returned text distinguishes common-cost allocation methods, provisional/final allocation and separate capital-goods adjustment cases. The proposed packet must qualify a selected method, not apply a universal turnover ratio.

https://www4.skatteverket.se/rattsligvagledning/edition/2026.13/407328.html

### X02: Skatteverket: construction reverse charge

Official search text covers service class and buyer activity conditions. It does not establish eligibility for a real invoice. Exact current tax-box and exception releases remain unqualified inputs here.

https://www4.skatteverket.se/rattsligvagledning/edition/2026.9/423282.html

https://www4.skatteverket.se/rattsligvagledning/edition/2026.12/423288.html

### X03: Skatteverket: declare and pay OSS

Official page opened. Separates OSS reporting and euro payment from regular VAT; registered zero-activity periods still have reporting requirements. Full schema, all scheme eligibility rules and provider access were not qualified.

https://www.skatteverket.se/foretag/moms/deklareramoms/ansokomattredovisadistansforsaljningionestopshoposs/deklareraochbetalamomsionestopshop.4.40cab8f8197edf03e644dee.html

### X04: Skatteverket: foreign VAT refunds

Official search text states foreign tax is not deducted as Swedish VAT and describes EU electronic applications through the Swedish service. Country eligibility/expense/form requirements remain actual qualification inputs.

https://www.skatteverket.se/foretagorganisationer/moms/momsvidhandelmedeulander/aterbetalningavmomsinomeu.4.58d555751259e4d661680001107.html

### X05: Skatteverket: employer travel allowances

Official search-returned guidance distinguishes allowance reductions and meal benefits, with dated tables and specific exceptions. This dossier supplies no activated allowance rates.

https://www.skatteverket.se/foretagochorganisationer/arbetsgivare/lonochersattning/traktamente.4.361dc8c15312eff6fd1703e.html

https://www.skatteverket.se/privat/skatter/arbeteinkomst/traktamente.4.dfe345a107ebcc9baf80006547.html

### X06: Skatteverket: benefit valuation and employee payments

Official text distinguishes net employee payments from gross salary exchange and contains separate benefit reporting categories. The car packet uses a bounded qualified profile, not all benefit/fuel rules.

https://www4.skatteverket.se/rattsligvagledning/edition/2026.12/1323.html

https://www.skatteverket.se/agbeskrivning

### X07: Skatteverket: KU20/KU25 interest reporting

Official search-returned text distinguishes reporting directions, actual timing, specification number and year-specific digital format changes. Exact applicable schemas and each company reporting duty remain unqualified here.

https://www.skatteverket.se/foretag/skatterochavdrag/kontrolluppgifter/kontrolluppgiftomranteinkomstku20ochranteutgiftku25.4.1df9c71e181083ce6f6349.html

### X08: Skatteverket: salary and pension basis

Official text explains that pensionable salary and allowable basis depend on the actual pension agreement, not simply the salary-exchange amount or a side clause. No recommendation about personal suitability is made.

https://www4.skatteverket.se/rattsligvagledning/edition/2026.7/402073.html

### X09: Bolagsverket: company forms and registration entry point

Official search-rendered index identifies capital-increase registration/form workflow. It does not qualify the legal effect, accounting date or intermediate equity classification of a particular cash issue. Those in NEXT-119 are proposed conditional contracts.

https://bolagsverket.se/sjalvservice/blanketterochmallar/aktiebolag.1713.html

### X10: Skatteverket: preliminary income-tax service

Official search-rendered service guidance separates declarations, saved drafts and decisions for a selected year. The proposed forecast is not an authoritative payable schedule or a full API integration.

https://www.skatteverket.se/sdginstruktioner/howtouseoureservicepreliminaryincometax.4.5dc1d8b31903014b1bf11be.html

### X11: Bankgirot: Bg Autogiro

Official page opened and search text inspected. The service has payer consents, payment submission and cancellation via the bank/service. Marketing claims of on-time payment are not adopted as final cash guarantees. Exact file/status/cutoff specifications were not acquired.

https://www.bankgirot.se/tjanster/autogiro/Autogiro/

### X12: Stripe: refunds and create-refund API

Official pages opened. Support partial original-charge refunds, original destination, pending/failure/cancellation states and returned-funds references. Card cancellation is not assumed to have a general API. No provider request was executed and no complete current adapter contract qualified.

https://docs.stripe.com/refunds

https://docs.stripe.com/api/refunds/create

## What was not established

No complete statutory tables, XML schema bundles, country VAT-rate data, pension agreements, actual company grants, actual share resolutions, direct-debit agreement or provider idempotency contract was supplied or activated. This task did not inspect a specific deployed customer database or run the ERP. A qualified profile is an actual missing input when applicable, not an invitation to invent a plausible constant.

The repository source remains app-owned. Current user/repository instructions govern test changes, migrations, deployment and real financial actions. This dossier grants none. Proposed function/record names are contracts to bind to existing owners, not claims that those exports already exist.

