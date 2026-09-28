# OpenERP: NEXT-76 through NEXT-100

Twenty-five new implementation-level work packets, continuing the application-owned design after NEXT-51..75. This is a proposed delivery specification, not a repository patch or evidence that the prior75 are complete.

Checkpoint: `66355b62b23e3b8007c2d324f3739fbbcc96cdc0`, observed 28 September 2026. The attached prior-wave dossier was used as the continuity basis. Current repository and official-source reads were targeted; their limits are recorded at the end.

Use named Effect application operations, one transaction passed to all participating writers, pure exact calculators and the existing private/financial authority. PostgreSQL retains narrow integrity. The persistent Bun/effect-mq runtime delivers background work. All earlier owners and qualified-profile gates remain in force.

## Contents

1. [Shared contract: NEXT-76 through NEXT-100](#part-01)
2. [Qualified inputs and activation gates](#part-02)
3. [NEXT-76: Accepted contract changes and sales-order billing limits](#part-03)
4. [NEXT-77: Time-and-materials billing with once-only work coverage](#part-04)
5. [NEXT-78: Milestone certificates and retained contract consideration](#part-05)
6. [NEXT-79: Earned but unbilled service revenue and later invoicing](#part-06)
7. [NEXT-80: Supplier disputes with partial payment holds and release](#part-07)
8. [NEXT-81: Asset work-in-progress and commissioning from purchase costs](#part-08)
9. [NEXT-82: Component replacement, improvements and partial asset retirement](#part-09)
10. [NEXT-83: Operating-rental contracts, refundable deposits and index changes](#part-10)
11. [NEXT-84: Book-to-tax depreciation cohorts and excess-depreciation bridge](#part-11)
12. [NEXT-85: Periodiseringsfond cohorts, reversals and annual tax linkage](#part-12)
13. [NEXT-86: ROT/RUT split claims and customer-authority settlement](#part-13)
14. [NEXT-87: Pension invoice reconciliation and SLP annual basis](#part-14)
15. [NEXT-88: Employment termination and final-pay obligation closure](#part-15)
16. [NEXT-89: Dividend resolutions, shareholder payables and KU31 preparation](#part-16)
17. [NEXT-90: Conditional grants, earned funding and repayment obligations](#part-17)
18. [NEXT-91: Apply supplier credit balances to other payable invoices](#part-18)
19. [NEXT-92: Documented bilateral receivable-payable setoff](#part-19)
20. [NEXT-93: Source-located evidence search and retained-page retrieval](#part-20)
21. [NEXT-94: Read-only mailbox intake and scoped attachment routing](#part-21)
22. [NEXT-95: Counterparty balance confirmations with independent evidence](#part-22)
23. [NEXT-96: Multi-human approval routing and segregated review policies](#part-23)
24. [NEXT-97: Exact covering-set reconciliation with explicit ambiguity](#part-24)
25. [NEXT-98: Accountant period-review engagements and versioned acceptance](#part-25)
26. [NEXT-99: Cash forecast vintage scoring and error attribution](#part-26)
27. [NEXT-100: Scoped integration event subscriptions and delivery receipts](#part-27)
28. [Integration map and non-overlap record](#part-28)
29. [Decisions selected for this wave](#part-29)
30. [Coordinator handoff: NEXT-76..100](#part-30)
31. [Sources, continuity and evidence limits](#part-31)

---

<a id="part-01"></a>

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


---

<a id="part-02"></a>

# Qualified inputs and activation gates

Reuse NEXT-02's existing fact/rule-release owner. This file defines required data, not another rule framework. Every financial/profile decision binds source evidence, semantic dates, an exact calculator/mapping version, supported cases, independent expected results and the actual reviewer. Missing data is a specific blocker to the dependent operation, not permission to fabricate a default.

| Packet family | Required input before the relevant financial stage |
|---|---|
|76-79 contract/work recognition | Accepted price/quantity rights, actual performance, billability, applicable revenue method, VAT tax point and conditional versus unconditional collection rights |
|80 supplier holds | Exact disputed components, legal/contractual payment basis, active reservations and actual provider cancellation outcome where needed |
|81-82 assets | Qualified eligible cost, ownership/use evidence, component gross/contra split, residual/life/method, tax treatment and complete inherited depreciation history |
|83 rentals | Actual lease classification, service dates, index series/formula, fees/incentives, refundable versus applied deposit terms and termination obligations |
|84 tax depreciation | Tax opening values, eligible tax pool/cohorts, allowed disposal-basis treatment, dated method coefficients, book-linkage and applicable reporting rules |
|85 reserves | Prior book/tax cohorts, fiscal/tax-year sequence, mandatory release events, release order, vintage factors, imputed-income computation and allocation-basis rules |
|86 ROT/RUT | Customer/property/work eligibility, performed and paid coverage, qualified year/rates/caps, actual authority identity, claim schema and customer recovery terms |
|87 pensions/SLP | Pension agreement and provider components, prior accrued liabilities, actual deductible/SLP treatment, annual basis rules and source statements |
|88 termination | Actual end decision/date, schedules, work/leave balances, lawful recovery/offset decisions, benefit/pension facts and actual reporting/payment dates |
|89 dividends | Actual resolution, authorised corporate evidence, reviewed capital/prudence basis, entitled holders/class rights, availability date, recipient status and KU31 rules |
|90 grants | Actual award conditions, eligible costs, permitted funding overlap, recognition presentation, entitlement/repayment events and tax timing |
|91-92 noncash settlement | Recognised claim identities, same legal counterparty, enforceable application/setoff evidence, supported currency/method and absence or release of conflicting reservations |
|93-95 evidence workflows | Data-use/access classes, source text/part locators, provider mailbox scope, recipient verification and scope-specific evidence retention |
|96 approval routing | Operator-approved risk measure, thresholds/units, finite role slots, distinct-human/conflict rules, eligible membership and revocation protocol |
|97 search | Exact comparable source/ledger capacities, supported date/currency scope, full pool count, deterministic ranking, disclosed computation limits and existing execution eligibility |
|98 review | Engagement scope, authorised reviewers, required procedures, exact report/evidence revisions, finding resolution witnesses and disclosed limits |
|99 scoring | Immutable forecast vintage, independently qualified actual outcome coverage, conserved payment identity matching and fixed metric definitions |
|100 integrations | Explicit event schemas/field projection, subscription authority, approved endpoint rules, exact signature protocol/key rotation and receiver replay contract |

## Select a finite supported release

```text
selectForOperation(family,facts,dates):
    candidates = existing qualified releases matching the actual family and applicability
    require exactly one unambiguous applicable release
    require every mandatory input has its required provenance and review
    require the named calculator/adapter implements this case, not merely a schema tag
    return retained release digest + selected fact/review revisions + dependency witness
```

The release can be finite data (rates, brackets, code maps) plus explicitly reviewed pure code. It must not execute arbitrary stored scripts or grant financial permissions. A newly downloaded official page is evidence to review, not an activated company policy.

## Legal and provider limits

Only narrow public-source checks listed in SOURCES.md were made. No complete pension, corporate-tax, depreciation, ROT/RUT, employment-law, grant or invoice rule release was qualified. All numeric rate/amount examples are synthetic unless an example explicitly identifies itself otherwise. They are arithmetic contracts, not current statutory constants.

The Gmail documents support the selected retrieval/history behavior, but no account was connected. Outbound subscriptions use an explicitly proposed signature protocol, not a claimed industry/provider compatibility. Any delivery adapter's actual authentication, idempotency, timeout and accepted-status semantics must be tested against its real contract under authority.

A formula can refuse an unsupported case while sources remain retainable and other work continues. It cannot silently label unknown payroll, tax or capital-availability facts as inapplicable. Financial operations, external submissions and actual release claims remain gated separately.


---

<a id="part-03"></a>

# NEXT-76: Accepted contract changes and sales-order billing limits

**Priority when applicable:** P1. **Lane:** SALES.

**New work:** Add reviewed post-acceptance scope/price changes and billing-capacity conservation. This is not another webshop order intake, catalog or recurring-template owner.

**Use existing owners:** Existing quote, order, catalog revision and invoice conversion owners.

**Required earlier contracts:** Existing core operation owners.

**Conditional gates:** NEXT-51: issuing invoices with the chosen tax/price profile.

**Evidence basis:** R02, P29, P66. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Records and stable components

```text
ContractRevision {contractId, customer, currency, effectiveInterval, acceptedEvidence,
  components:[{stableComponentId, unit, agreedQuantity, agreedNetCap, priceRule}]}
ChangeOrder {originalContractRevision, changedComponents, effectiveFrom,
  customerAcceptanceEvidence, internalReview, reason, supersededDrafts}
BillingCoverage {componentId, sourceOccurrence, reservedQuantity, issuedQuantity,
  reservedNet, issuedNet, originatingInvoiceId, changeAuthority}
```

An internal quote update is not evidence the customer accepted a variation. Stable component IDs survive revisions; cloning the order cannot reset already invoiced coverage. Quantities with different units are not additive.

## Pure preparation

```text
prepareChange(basis, proposal):
  resolve exact accepted contract and current component coverage
  require same legal customer/currency for the bounded profile
  for component:
    floorQuantity = irrevocablyIssuedQuantity + remainingLegitimateReservations
    floorNet = irrevocablyIssuedNet + remainingLegitimateReservations
    if proposed cap below its consumed floor:
      return RequiresCreditOrApprovedReservationRelease(affectedRefs)
    compute new remaining rights, explicit price-effective boundary and deadline changes
  identify affected UNISSUED drafts and acceptances
  freeze before/after component rights plus actual acceptance evidence
```

A cancellation of remaining scope does not delete an issued invoice or reverse earned revenue. A credit can fix an earlier invoice, but it does not automatically grant permission to bill the same delivered service again. A replacement billing right requires a specific approved relationship.

## Application transaction

`executeContractChange` locks the current contract/order and component versions, checks current authority and exact approval, then inserts the new revision and closes/replaces affected unissued reservation authority. It calls the existing sales-order amendment writer on the same tx; it creates no revenue, tax fact or receivable. The record/receipt and notifications commit together. If a legal issue races with a reduction, the shared order-capacity lock makes one stale rather than both spending the same capacity.

Invoice draft generation reads the selected accepted revision and explicit coverage. Final issue rechecks and consumes the same exact rights through an internal owner port. A displayed quote total is not a writable balance.

## Readers and correction

Show original agreement, customer acceptance, every variation, issued amounts and remaining rights. Forecasts read the unbilled remainder only as a labelled commitment, not a booked receivable. Material currency/customer replacement is unsupported in v1; a linked new contract with reviewed transition is required.

A mistaken accepted change is superseded, not deleted. If no downstream issue consumed it, the replacement can restore prior rights. Otherwise the proposal names the necessary invoice/recognition corrections before authority is changed.

```text
contract100 units; issued40; live reservations10; increase cap120 -> remaining70
reduce cap45 while50 committed/reserved -> refuse or release the10 through its owner
draft issued concurrently with variation -> one wins, other must refresh
same accepted amendment replay -> same receipt and no new contract version
```

Completion includes amendment review, unchanged old invoice bytes, server-side issue revalidation and matching order/forecast readers. No contract-management framework or automatic revenue recognition is added.


---

<a id="part-04"></a>

# NEXT-77: Time-and-materials billing with once-only work coverage

**Priority when applicable:** P1. **Lane:** SALES.

**New work:** Add reviewed billable work capture and conversion into invoice lines. Payroll work facts, recurring invoices and deferred revenue remain separate owners.

**Use existing owners:** Existing employee/project references, source occurrences, sales-order capacity and invoice draft/issue owners.

**Required earlier contracts:** NEXT-51, NEXT-76.

**Conditional integration:** NEXT-79 when selected work was already recognised as unbilled revenue or requires its qualified contract-asset treatment.

**Evidence basis:** R02, P35, P58. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Distinct work and billing meaning

```text
WorkEntryRevision {entryId, personOrContractorRef, contractComponentId,
  serviceInterval, exactUnits, unit, workEvidence, billableDecision, revision}
PriceWitness {contractRevision, rateRevision, unitConversion, currency,
  roundingRule, negotiatedCap, review}
BillingSlice {workEntryId, reviewedRevision, unitRangeOrQuantity,
  reservedByDraft?, issuedByInvoice?, correctedBy?, economicCoverageIdentity}
```

Time recorded for payroll is not automatically billable and client acceptance is not payroll approval. Role-limited project views must not expose employee salary or private payroll fields. One original work item can be split, but its effective issued plus reserved quantities cannot exceed its reviewed billable quantity.

## Calculate and reserve

```text
compileTimeBilling(entries, acceptedContract):
  reject overlaps/duplicate economic work and unsupported mixed units
  for selected entry:
    quantity = reviewed available units after effective coverage
    rate = exact accepted price at the contract's agreed date basis
    net = roundRatio(quantityNumerator * rateMinor,
                     quantityDenominator * rateUnitDivisor, priceRounding)
    retain work locations, service dates and exact calculation residual
  enforce contract cap from NEXT-76 and qualified invoice-tax calculation from NEXT-51
  freeze selected work revisions, quantities and resulting invoice line identities
```

For example,90 minutes at120000 minor units/hour produces180000 net minor units before the separately qualified tax calculation. Neither a floating-hour approximation nor a later edited hourly rate may change that retained proposal.

`reserveAndCreateDraft` uses one application tx to recheck work and contract coverage, append reservations and create the ordinary invoice draft. Final legal issue consumes those exact reservations through the existing invoice transaction. Issue failure rolls back consumption; a lost response recovers the original invoice receipt. Do not consume work in a job after invoice issue, since that admits duplicate billing during the gap.

## Changes and exceptions

Editing unissued work invalidates dependent drafts. Abandoning a draft can release its reservation only through an owned state transition that proves it was not issued. Issued work is immutable financial evidence; later corrected time produces a credit or replacement-billing proposal referencing the original coverage. A credit does not automatically make the same hours billable again.

Write-downs and nonbillable decisions retain reason and actual quantities but create no invoice. Where work was already recognized as unbilled revenue, NEXT-79 supplies the exact asset-release branch so billing does not recognize revenue again. Otherwise normal issue recognition remains in force. Do not route the same work through both branches.

## Operator journey and proof

The user reviews person/task/service period, billable units, contract price, retained approvals and cap usage, then opens the normal invoice review. Reports distinguish recorded, accepted, reserved, billed and written-down work.

```text
reviewed10h, issued4h, reserved2h -> selectable4h
same work selected in two drafts -> second reservation fails or becomes stale
client disputes2h after issue -> retain10h original; create linked credit proposal
invoice issue commits before timeout -> replay returns it with coverage consumed once
```

Finish with real draft/issue/residual integration, not just a timesheet table or pure invoice calculator. No employee wage liability is created by billability.


---

<a id="part-05"></a>

# NEXT-78: Milestone certificates and retained contract consideration

**Priority when applicable:** P1. **Lane:** SALES.

**New work:** Add delivered-milestone acceptance and retained amounts on customer contracts. Invoice installments split due dates; they do not prove a milestone occurred or that retention is unconditional.

**Use existing owners:** Existing sales agreement, acceptance evidence, invoice and installment owners.

**Required earlier contracts:** NEXT-51, NEXT-59, NEXT-76.

**Conditional integration:** NEXT-79 when selected work was already recognised as unbilled revenue or requires its qualified contract-asset treatment.

**Evidence basis:** R02, P59, P66. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Required distinctions

```text
Milestone {contractComponentId, acceptanceCriteria, contractualNet,
  evidenceRequirements, billableTrigger, retentionTerms}
AcceptanceRevision {milestoneId, completedQuantity, customerAcceptance,
  exceptions, effectiveDate, reviewedBy}
RetentionSlice {sourceInvoiceLine, amount, legalStatus:
  unconditional_debt_due_later | conditional_right, releaseConditions,
  expectedReleaseDate?, evidenceRefs, currentRevision}
```

Initial financial support covers an accepted fixed-price milestone and an enforceable invoice receivable with a retained amount due later. If payment remains contingent on additional performance such that no unconditional debt exists, refuse that AR branch; use NEXT-79's separately qualified contract-asset treatment when available. Calling every withheld amount an installment would overstate receivables.

## Billing proposal

```text
prepareMilestoneInvoice(milestone, acceptance):
  require actual acceptance/entitlement evidence and unused milestone coverage
  gross = qualified net + VAT from existing invoice compiler
  retention = exact contractually supported amount, not a discretionary rounding remainder
  require 0 <= retention <= gross
  dueNow = gross-retention
  freeze milestone coverage + invoice semantic lines
  create due components(dueNow, retainedAmount) through installment owner
```

The chosen tax profile establishes the tax point independently. A retained cash amount does not automatically postpone VAT or reduce the invoiced supply. Recognition follows the revenue profile, not the date the customer releases retention.

One tx creates/reserves the milestone-linked draft. Issue atomically consumes milestone/order coverage and records the invoice and due components. If revenue was already recognized from this performance, consume the corresponding NEXT-79 recognition rights inside that issue tx; do not post the same revenue twice.

## Retention release and disputes

```text
releaseRetention(retentionId, proof):
  require current contract condition, acceptance and independent approval
  require retained invoice slice still outstanding
  reclassify its due status/date in the installment owner
  append release evidence and receipt, no new invoice/revenue/VAT
```

A revised expected date used by Cash does not itself satisfy legal release conditions. A paid retained amount consumes its existing AR slice. A dispute reduces collectible status or adds a hold, not the legal invoice principal. A negotiated price reduction uses the normal credit owner with original-line capacity.

If a mistaken release has already been paid, do not reverse the cash to restore a future due date. Record a linked correction or refund obligation only when evidence and the selected profile justify it.

## Visible workflow and vectors

The milestone screen shows acceptance, issued amount, immediately due balance, retained balance, release evidence and actual settlement independently. Contract totals and Cash use one underlying obligation identity and cannot add a retention twice.

```text
net100000 VAT25000 gross125000; retention12500 -> dueNow112500 + retained12500
release12500 -> AR total unchanged, revenue/VAT delta0
unaccepted milestone -> cannot issue from the accepted-milestone path
retention already paid -> release changes no cash balance
```

Completion requires two-stage collection and credit/currentness behavior against actual application owners. It does not add a construction-industry legal profile by default.


---

<a id="part-06"></a>

# NEXT-79: Earned but unbilled service revenue and later invoicing

**Priority when applicable:** P1. **Lane:** SALES.

**New work:** Add earned-unbilled recognition before invoice issue. NEXT-58 defers invoiced revenue and is the opposite timing direction.

**Use existing owners:** Existing contract, revenue schedules, GL, invoice and tax-fact owners.

**Required earlier contracts:** NEXT-13, NEXT-51, NEXT-58, NEXT-76.

**Evidence basis:** R02, R03, P58. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Recognition coverage

```text
PerformanceComponent {contractId, stableServiceCoverage, exactSupportedMeasure,
  earnedEvidence, collection/acceptanceConditions, valuationRelease}
EarnedRevenueTarget {componentId, asOf, earnedNetTarget, previouslyEffectiveNet,
  basisRefs, ruleVersion, accountingDate}
UnbilledEffect {componentId, recognizedNet, invoicedReleaseNet,
  correctionRefs, journalRefs, sourceCoverageIdentity}
```

Start with one reviewed service-recognition profile under the applicable framework. Do not equate hours worked, cost incurred or a forecast milestone with legally/accountingly earned revenue. An uncertain entitlement produces a review case rather than a manufactured contract asset. Construction percentage-of-completion and loss-making contracts need their own qualified profiles.

## Target calculation and posting

```text
prepareEarnedRevenue(component, qualifiedMeasure):
  target = exact contractual price * qualified earned fraction, rounded per release
  require target <= supported total contract consideration
  delta = target - totalEffectiveRevenueRecognizedForThisCoverage
  determine whether delta changes unbilled asset or an already invoiced/deferral component
  initial path permits only the currently unbilled portion
  debit unbilled contract asset delta
  credit service revenue delta
  no invoice, customer AR or tax fact unless a separate qualified tax trigger exists
```

SQL reads return exact prior effects; the domain computes the target/delta. A new target revision does not post the entire target again. Negative deltas may reduce existing unbilled carrying only to its available amount. Reductions of already invoiced amounts require the proper credit/deferral owner rather than a negative contract-asset shortcut.

## Issue without re-recognizing revenue

```text
compileInvoiceWithPriorEarnings(invoiceLines, coverage):
  N = invoice net; V = independently qualified invoice tax
  E = exact earlier earned-unbilled carrying released for this invoice coverage
  require 0 <= E <= N and available unbilled capacity
  debit customer AR N+V
  credit unbilled asset E
  credit revenue or deferred-revenue owner for remaining N-E, per supported treatment
  credit output VAT V unless already represented by qualified earlier tax facts
```

Already recognized tax also has coverage and must be released/adopted exactly once; the initial profile can refuse earlier-tax cases instead of assuming every unbilled asset is tax-free. The combined invoice issue consumes unbilled coverage on the same tx as numbering, financial posting and tax/open-item effects.

## Controls and correction

Reconcile unbilled opening plus recognition deltas less invoiced releases to the GL. Keep recognized revenue and commercially billable amounts distinct. An invoice claim is not another cash event. Expired collection rights or disputed earned values go through a reviewed correction/impairment profile, not silent source deletion.

Views show supported earned amount, already invoiced amount, remaining asset, tax status and evidence. Closed-date refusal never changes the proposed posting date automatically. Historical reports keep their captured target revisions.

```text
earned60000 -> asset+60000/revenue-60000
invoice net80000 tax20000 -> AR+100000, asset-60000, revenue-20000, VAT-20000
lifetime revenue80000, not140000
same coverage target revised70000 before billing -> additional recognition10000
```

Delivery must include invoice consumption and fixed-cutoff controls. A standalone accrued-income journal generator is not completion.


---

<a id="part-07"></a>

# NEXT-80: Supplier disputes with partial payment holds and release

**Priority when applicable:** P1. **Lane:** PURCHASES.

**New work:** Add supplier-side documentary dispute and explicitly bounded payment holds. Customer collection disputes and procurement acceptance do not supply this payable workflow.

**Use existing owners:** Existing payable residual, supplier credit, payment reservation and invoice evidence owners.

**Required earlier contracts:** NEXT-03, NEXT-07, NEXT-08, NEXT-71.

**Evidence basis:** R02, P28, P66. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Separate debt, disputed amount and payment eligibility

```text
SupplierDisputeRevision {invoiceId, sourceLineScope, disputedGross, reason,
  supplierCommunications, owner, openedAt, resolution?}
PaymentHold {disputeId, coveredComponents, blockedAmount,
  effectiveFrom, releaseDecision?, sourceVersion}
```

Opening a dispute creates no accounting entry and does not remove a valid recognized payable. Commercial rejection, an invoice mistake, a credit and an invalid liability are different outcomes. Any change to expense/VAT/debt requires its qualified financial correction owner.

```text
paymentEligibility(invoice, currentScope):
  outstanding = shared payable owner's current residual
  held = union of effective held monetary components, not sum of overlapping hold labels
  reserved = current live instruction reservations
  availableForNewInstruction = outstanding - held - distinctReservedUnheldAmount
  require each capacity counted exactly once and result>=0
```

Hold definitions reference stable source components or disjoint amount slices. Overlapping holds must be merged deterministically or refused at preparation; taking `min(totalHolds,outstanding)` hides conflicting instructions and is not the selected design.

## Opening and resolving

`openSupplierDispute` captures payable/source/hold versions, checks permitted evidence and writes the dispute, hold inventory change and receipt under the book lock. It invalidates unexecuted payment preparations for the affected capacity. It does not claim to cancel an exported or remotely admitted instruction: those routes stay outcome-unknown until NEXT-08/71 proves cancellation or execution.

```text
resolveDispute(decision):
  if supplier confirms full amount: release exact held capacity with evidence
  if valid credit issued: call/prepare existing credit owner; keep hold until effects reconcile
  if partial settlement agreed: qualified discount/credit owner determines financial effect
  if unsupported legal outcome: retain hold and named unresolved obligation
```

A release and replacement payment preparation can be separate deliberate steps. Final payment execution checks current hold/credit/reservation state, so a dispute opened after preparation cannot be ignored by a stale UI.

## Partial payments and historical views

Known undisputed slices can remain eligible when the selected contractual policy permits partial payment. The app cannot universally assume withholding is legally permitted. Legal due date is not rewritten; Cash may show an expected-delay assumption while retaining contractual exposure. Independent source coverage still includes disputed invoices.

A dispute added after a payment commits cannot unpay it. It records a refund/credit pursuit and links real cash history. Removing a hold does not mark an invoice settled.

## Journey and cases

The supplier workspace exposes recognized residual, held components, reservation/outcome state and actually available payment capacity. All payment paths, not only the new screen, consume this owner. History shows the original dispute and every resolution.

```text
invoice100000; held30000; no reservations -> eligible70000
another hold over the same30000 -> union30000, not60000
payment reservation70000 + hold30000 -> new eligible0
exported instruction now disputed -> no fake cancellation; create outcome/recovery work
credit10000 agreed on held portion -> post via credit owner, then re-evaluate remaining hold
```

The packet is complete only when manual, batch and provider payment admissions observe the same hold inventory. It is not a general legal-dispute or procurement system.


---

<a id="part-08"></a>

# NEXT-81: Asset work-in-progress and commissioning from purchase costs

**Priority when applicable:** P1. **Lane:** ASSETS.

**New work:** Add multi-source asset construction/acquisition accumulation and an explicit ready-for-use transition. Existing asset bases and depreciation schedules remain their owners.

**Use existing owners:** Purchase recognition, asset register, original-cost allocation and schedule application services.

**Required earlier contracts:** NEXT-03, NEXT-31.

**Conditional gates:** NEXT-54: qualified import/landed-cost components enter the asset basis.

**Evidence basis:** R03, P54. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Source-cost coverage

```text
AssetBuild {buildId, intendedAsset, eligibleCostProfile, stage: accumulating|commissioned|abandoned}
CostAllocation {recognitionId, sourceLineId, costComponentId, allocatedMinor,
  constructionAccount, targetBuild, availableCoverageVersion}
CommissioningPlan {buildId, acceptedInServiceDate, componentAllocation,
  grossTarget, usefulLife/residual evidence, uncommissionedCosts, digest}
```

Cost is the eligible net plus non-deductible tax and independently qualified direct costs, not the invoice gross by default. Evidence that a cost belongs to the asset is mandatory. Marketing, training or finance costs do not become capitalizable merely because the build is over budget.

## Accumulation

An unposted purchase uses the existing compiler with the qualified asset-under-construction role. That one transaction writes purchase/tax/payable and source-cost allocation. An already recognized eligible expense can be reclassified through an approved dated operation: debit construction asset, credit that expense. No new payable, bank transaction or tax recognition is created.

```text
allocateBuildCost(source, build, amount):
  require exact recognized cost component and amount<=unallocated eligible cost
  capture original purchase/credit history and cost profile
  freeze source-to-build allocation; reserve no duplicate expense recognition
  transaction: recheck capacity, post required reclassification, append allocation + receipt
```

A credit reduces the linked uncommissioned basis or triggers an owned adjustment to the commissioned asset. It must not quietly delete a source allocation or leave depreciation on refunded cost.

## Commissioning

```text
prepareCommissioning(build):
  G = sum effective eligible allocations selected for this commissioned component set
  require actual ready-for-use evidence and complete ownership/use-date facts
  require G>0 and exact component shares sum to G
  determine qualified method, residual and future recognition start
  debit in-use asset role G; credit construction role G
  create existing asset basis with original sources and the approved future schedule
```

`executeCommissioning` locks the build, cost rights and schedule dependencies. Journal reclassification, commissioned asset basis, transferred source allocations and schedule creation share one tx. It cannot first move the GL then hope a later job creates the schedule. Partial commissioning uses explicitly partitioned components; remaining costs stay on the build without being depreciated.

## Abandonment and corrections

Abandonment needs reviewed recoverable value and treatment. The supported decision can reclassify unrecoverable construction cost to loss, but it does not fabricate disposal proceeds. Existing advances for undelivered assets remain NEXT-57 prepayments rather than installed costs.

Correcting commissioning after depreciation requires the asset owner's complete correction/estimate path. Changing the date or useful life in place is prohibited. Old source and report snapshots retain their original basis.

## Completion cases

```text
eligible cost100000 + installation20000 -> construction120000
commission120000 -> in-use+120000/construction-120000; AP/VAT delta0
commission component70000 -> build still50000, only70000 schedule authority
same source line allocated twice -> capacity refusal
supplier credit after commissioning -> owned asset adjustment, not source deletion
```

UI shows cost provenance, unallocated/accumulating/commissioned amounts, actual in-service evidence and schedule. Complete controls reconcile construction and in-use accounts separately. This is not an inventory, project-cost capitalization or arbitrary asset-recognition framework.


---

<a id="part-09"></a>

# NEXT-82: Component replacement, improvements and partial asset retirement

**Priority when applicable:** P2. **Lane:** ASSETS.

**New work:** Add separately supported asset-component replacement and improvement accounting. Whole-asset impairment and disposal remain unchanged.

**Use existing owners:** Existing asset carrying/impairment/schedule owners and the source-cost owner from NEXT-81.

**Required earlier contracts:** NEXT-19, NEXT-42, NEXT-81.

**Evidence basis:** R03, P19, P42. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Component basis

```text
AssetComponent {assetId, componentId, grossCost, ordinaryAccumulated,
  impairmentAccumulated, remainingSchedule, residual, sourceAllocation}
ComponentEvent {kind: addition|replacement|partial_retirement, affectedComponents,
  exactOldBasis, newCostAllocations, taxTreatmentRefs, effectiveDate}
```

For existing assets without component histories, require a reviewed allocation of gross cost, accumulated depreciation, impairment and residual that reconciles exactly to the parent. Do not allocate only net carrying and invent the missing gross/contra amounts. The classification split itself creates no new total value or depreciation expense.

```text
validateComponentSplit(parent, children):
  for quantity in gross, ordinary, impairment, residual:
    require sum(children.quantity)==parent.quantity
  require each child gross-ordinary-impairment>=0
  require complete original source/history explanation or explicit unresolved split blocker
```

An arbitrary estimated fraction is not sufficient disposal evidence. A qualified historical component estimate can be used only with its reviewed method and applicable policy.

## Replace a component

Let old component values be G, A and I, so B=G-A-I. Let N be the new independently qualified capitalized cost.

```text
compileReplacement(old, newSource):
  require exact supported component identity and current carrying basis
  debit accumulated ordinary A
  debit accumulated impairment I
  debit retirement loss B
  credit old gross asset G
  debit new gross asset N
  credit construction/qualified purchase clearing N
  create new component and approved future schedule
  retire old future occurrences, retaining all posted history
```

If proceeds exist, use the component-specific proceeds branch from NEXT-19 rather than also booking full loss B. If the new purchase was already recognized in construction, consume it; if not, recognition must be part of the same transaction through the purchase owner. No second vendor payable or tax fact is allowed.

## Improvements versus repairs

A reviewed repair expenses its cost through purchasing and does not change gross asset basis. An improvement adds a cost component only when the selected accounting profile permits it. Any changed remaining life or residual is a separate explicit future-schedule decision. Never recompute all previous depreciation from the new larger gross cost.

Execution checks component membership, prior ordinary/impairment changes, source-cost rights and possible proceeds before writing all journal/register/schedule effects together. A concurrent depreciation occurrence makes the old replacement plan stale.

## Readers and correction

The parent aggregates child gross/contra/carrying exactly. Historical reports retain their component revisions. Existing book-level asset controls include one contribution per actual posting, not both the parent amount and duplicated child amounts.

A reversal after the new component has depreciated requires a dependency-aware plan. Until supported, refuse rather than resurrect the old schedule and leave the new one running.

```text
old G100000 A60000 I10000 -> B30000
replace with N80000 -> old gross/contra cleared, loss30000, new carrying80000
parent component split60000+40000 gross -> aggregate100000, no extra asset
simultaneous installment on old component -> stale replacement, no partial posting
```

Deliver the full component basis, atomic retirement/new schedule and controls. A form that posts a manual capital addition without closing the removed component is not this feature.


---

<a id="part-10"></a>

# NEXT-83: Operating-rental contracts, refundable deposits and index changes

**Priority when applicable:** P2. **Lane:** PURCHASES.

**New work:** Add contract-owned operating-rental commitments and deposit recovery. This is not a finance-lease/right-of-use asset or another recurring expense scheduler.

**Use existing owners:** Existing purchase, prepayment/accrual, supplier advance, schedule and Cash contribution owners.

**Required earlier contracts:** NEXT-31, NEXT-57, NEXT-59.

**Evidence basis:** R03, P31, P57. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Supported profile

Start with one reviewed rental/operating-lease accounting profile and currency. Financial leases, sale-and-leaseback and uncertain classification refuse before financial admission. Contract dates, base rent, incentives, service charges, refundable deposits and cancellation terms are independent components.

```text
RentalRevision {agreementId, serviceInterval, periodicAmount,
  indexFormula, indexObservationRefs, noticeTerms, taxProfile, depositTerms}
RentOccurrence {agreementId, stableCycle, expectedCost, actualInvoiceRefs,
  accruedCostRefs, plannedPaymentIdentity}
RefundableDeposit {originalPaymentIdentity, principal, appliedToCosts, returned, remaining}
```

A deposit with an unconditional refund right is not rent expense. Where it is actually advance rent or its treatment is uncertain, NEXT-57/31 or a review blocker applies. A supplier calling a fee a deposit does not determine accounting.

## Contract changes and invoice replacement

```text
calculateIndexedRent(revision, observations):
  require specified base/index dates, series, caps/floors and rounding
  rateFactor = exact allowed formula over retained index values
  newAmount = roundRatio(baseRent*factorNumerator,factorDenominator,policy)
  freeze change-effective cycle and contractual notice evidence
```

The formula is a reviewed contract, not a guessed CPI lookup. An index observation change does not edit old invoices or occurrences. Amendments replace only eligible future commitments.

Committed expected rent is a forecast obligation, not automatically a payable. As service is consumed, the selected accrual/deferral owner recognizes expense with the contract evidence. An actual invoice replaces its specific forecast/accrual occurrence, avoiding duplicate Cash outflow and expense. Recurring preparation does not grant unattended posting approval.

## Deposit and termination

```text
payRefundableDeposit(D): debit deposit receivable D; credit cash D
receiveRefund(R): debit cash R; credit deposit receivable R
applyDepositToValidRent(A): debit supplier payable A; credit deposit receivable A
```

The last branch requires an already recognized supported rent obligation and evidence of actual application. If rent was not recognized, the purchase/accrual recognition and deposit application must compose in one approved aggregate. There is no second bank payment. Any forfeiture is a separate reviewed cost/loss with its own tax assessment, not silently treated as returned cash.

Termination ends unperformed commitments but does not reverse valid past expense or waive outstanding debt. Final fees, incentives needing repayment and restored premises costs require explicit reviewed components. Any unresolved obligation remains visible after the agreement is inactive.

## Transaction and output

Each deposit/expense/application operation uses the existing tx-passing owner and records exact source rights. Contract amendment is nonfinancial unless accompanied by explicitly approved accounting effects. Controls reconcile deposit principal and accrued/prepaid rent separately. Cash includes remaining contractual expectations replaced by actual invoices, not both.

```text
deposit30000; valid payable20000; apply15000 -> deposit15000, AP5000, cash delta0
rent10000 indexed by103/100 ->10300 for new cycles only
termination cancels3 future10000 expectations -> forecast-30000, GL delta0
refund12000 after3000 evidenced forfeiture -> deposit clears through separate events
```

UI must expose classification, service dates, index evidence, actual invoices and remaining refundable principal. No blanket K2/K3 lease qualification is claimed.


---

<a id="part-11"></a>

# NEXT-84: Book-to-tax depreciation cohorts and excess-depreciation bridge

**Priority when applicable:** P2. **Lane:** TAX.

**New work:** Add a tax-value and deduction calculation linked to book assets. Ordinary book depreciation and income-tax calculation remain separate owners.

**Use existing owners:** Asset register, qualified tax release, corporate-tax bridge and appropriation/reserve journal owners.

**Required earlier contracts:** NEXT-02, NEXT-13.

**Conditional gates:** NEXT-22: the annual tax bridge consumes the selected deduction; NEXT-81: new commissioned assets enter the eligible tax pool.

**Evidence basis:** R03, P22. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Separate bases, not parallel ledger books

```text
TaxAssetCohort {taxPool, acquisitionTaxYear, eligibleCost,
  disposalAdjustment, sourceBookAssetRefs, qualificationWitness}
TaxDepreciationCalculation {year, openingTaxValue, currentEligibleMovements,
  methodCandidates, selectedDeduction, closingTaxValue,
  bookCarryingBasis, requiredBookLinkage, priorEffectiveAppropriation, digest}
```

Start with a qualified ordinary machinery/equipment pool. Land, goodwill, special property, immediate deductions and mixed unsupported tax methods remain explicit cases. Imported tax opening values need prior-return evidence; do not derive them from book carrying alone.

## Exact calculation graph

```text
B = openingTaxValue + eligibleAdditions - qualifiedDisposalBasisAdjustment
require B>=0 or route to the separately supported recapture/disposal-tax profile
candidateDecliningClosing = roundRatio(B*(denominator-rate),denominator,rule)
candidateCohortClosing = sum(eligible cohort costs * qualified remaining factor by tax year)
validate each candidate's applicability and required accounting linkage
maximumDeduction = B - lowest permitted candidate closing
require 0 <= selectedDeduction <= maximumDeduction
closingTaxValue = B-selectedDeduction
```

The disposal adjustment and year factors come from the actual qualified method; neither necessarily equals book carrying or cash proceeds. For rules with book linkage, a tax choice cannot be finalized without the associated permitted book depreciation/appropriation. Selecting an unavailable method because it gives lower tax is refused. The operator chooses a permitted deduction rather than the app always maximizing it.

## Bridge and financial effect

For the specifically qualified excess-depreciation reserve profile:

```text
targetReserve = bookCarryingAfterOrdinaryDepreciation - closingTaxValue
require targetReserve>=0 and legal/book linkage satisfied
reserveDelta = targetReserve-priorEffectiveReserve
addSigned appropriation expense +reserveDelta
addSigned untaxed reserve -reserveDelta
```

Do not apply this formula to every framework or temporary difference. A negative/unsupported relationship requires its own treatment rather than a negative reserve default. Ordinary asset depreciation remains unchanged. Tax adjustments consumed by NEXT-22 distinguish book ordinary depreciation, appropriation and allowed deduction so the same deduction is not counted twice.

## Persistence and annual rollforward

Preparation captures actual asset events, tax cohorts, prior filings and book/tax computation versions. Execution of an approved appropriation posts only its delta and retains the chosen tax closing movement in the same tx. A draft does not consume tax capacity. Final year selection is linked to the actual tax/close record, never merely the last calculated preview.

Subsequent disposal or corrected acquisition creates impact on the cohort and affected tax years. Preserve submitted returns and book journals; generate reviewed target deltas or amendment work. Do not rebuild earlier years from today's asset labels.

## Examples and UI

Synthetic rates only: B1000000, permitted closing alternatives700000 and760000 yields maximum deduction300000. Selected deduction250000 gives tax closing750000. If qualified book carrying is800000, target reserve50000; prior reserve30000 gives a20000 appropriation, not another50000.

The view shows every cohort, candidate method, chosen deduction, remaining tax value and exact form/GL bridge. Delivery includes the tax-bridge consumer and independent controls. A second writable general ledger labelled tax is out of scope.


---

<a id="part-12"></a>

# NEXT-85: Periodiseringsfond cohorts, reversals and annual tax linkage

**Priority when applicable:** P2. **Lane:** TAX.

**New work:** Add optional tax-allocation reserve choices and their cohort history. Current-tax calculation alone does not own reserve deadlines or reversals.

**Use existing owners:** Existing tax bridge, closing, qualified rule releases, deadline and appropriation posting owners.

**Required earlier contracts:** NEXT-22, NEXT-49.

**Evidence basis:** X01, R03, P22. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Qualified cohort model

```text
ReserveCohort {entity, originalTaxYear, originalDeduction,
  bookReserve, taxReleaseBasis, remainingBook, remainingTax,
  mandatoryReleaseYear, vintageRules, sourceReturnRefs}
ReserveDecision {year, orderedReleases, newAllocation,
  preAllocationTaxBasis, eligibleMaximum, imputedIncomeBasis,
  targetEffects, evidence, reviewer}
```

Official guidance makes each year's reserve its own cohort and requires dated release rules [X01]. Tax-year age is not a fixed count of elapsed days. Preserve vintage-specific tax treatment and any mandatory early-release reason. Do not infer an opening reserve of zero merely because the app lacks imported cohort rows.

## Acyclic tax computation

```text
prepareReserveDecision(preReserveBridge, knownCohorts, chosenAllocation):
  determine mandatory and optional releases using qualified order/vintage rules
  bookRelease = sum selected book principal
  taxableRelease = sum each cohort's qualified tax-equivalent release
  imputedIncome = rule's exact computation on its specified opening reserve population
  basis = preReserveTaxResult + taxableRelease + imputedIncome
          + other explicitly ordered eligible adjustments
  maximum = rule's rounded permitted fraction of positive qualified allocation basis
  require 0<=chosenAllocation<=maximum
  return revised taxable basis = basis-chosenAllocation
```

The rule release defines the interaction with loss deductions and other restrictions. Do not use a fixed shortcut when the company's case falls outside that order. Imputed income is a tax-bridge contribution, not automatically accounting revenue. The pre-reserve input must exclude this decision's own book appropriation to avoid self-reference.

## Journals and lifecycle

```text
release prior reserve B: debit reserve B; credit appropriation income B
allocate new reserve A: debit appropriation expense A; credit current-year reserve A
```

Taxable reversal may differ from book B under a vintage rule; retain that difference in the tax bridge, not by changing the reserve's original ledger principal. Preparation is a selectable scenario. Execution consumes the selected old cohort capacities, creates the new cohort and posts its journal effects atomically with exact approval and receipt. Re-running the same year target cannot create another reserve merely under a new key.

A revised tax decision posts a target-minus-effective delta with original cohort identity and relevant correction dates. It never silently moves all reserves into one current-year bucket. Authority filing and assessment remain NEXT-74, not effects of the reserve journal.

## Controls and proof

Book cohort total must equal the qualified reserve GL accounts. Every annual tax bridge lists book changes, taxable changes and nonbook imputed income once. Deadline generation references each real cohort and its applicable tax-year sequence. Complete close refuses unknown old reserve history where material.

```text
synthetic allocation basis1000000 with permitted fraction1/4 -> ceiling250000
operator selects200000 -> current-year reserve200000, not default250000
old book reserve100000 with qualified tax factor104/100 -> book release100000,
    taxable release104000, separate tax adjustment4000
same decision replay -> same cohort effects; new key same target -> no duplicate reserve
```

Synthetic rates/factors are examples, not an activated Swedish rule. This packet does not advise a company to maximize reserves or choose a tax strategy; it makes a reviewed permitted decision traceable and executable.


---

<a id="part-13"></a>

# NEXT-86: ROT/RUT split claims and customer-authority settlement

**Priority when applicable:** P2. **Lane:** TAX.

**New work:** Add the explicitly conditional household-work profile, with labour evidence, split obligors and claim/rejection recovery. Mixed-rate ordinary invoices are not this workflow.

**Use existing owners:** Existing invoice/tax facts, receivable allocations, customer credit and external declaration-attempt owners.

**Required earlier contracts:** NEXT-51, NEXT-15, NEXT-30, NEXT-49.

**Evidence basis:** R02, X02. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Original consideration remains complete

```text
HouseholdWorkCase {customerPersonRefs, property/workFacts, workCategory,
  performedCoverage, labour/material/travelLineBreakdown,
  customerPaymentRefs, applicableRelease, reportedAllowanceEvidence}
AuthorityClaimSlice {caseId, person, performedAndPaidCoverage,
  eligibleAmount, priorClaimedAmount, claimArtifact, outcome, authorityReceivableRef}
```

Invoice gross revenue and VAT do not shrink because a customer requests relief. Labour, materials and other charges retain their original economic meaning. Shared per-person caps need sourced information and a clear limitation when other providers' usage is unknown; this book cannot guarantee the customer's total national allowance.

## Calculation and financial admission

```text
prepareHouseholdInvoice(case):
  use ordinary qualified invoice arithmetic for full consideration and VAT
  calculate conditional relief only for eligible performed labour and person/date facts
  display planned customer payment and conditional authority share distinctly
  recognition uses the selected qualified receivable policy, not a fictional grant discount

prepareClaim(case, paidAndPerformedScope):
  require work and customer-payment prerequisites for selected rule
  compute eligible gross labour share with exact cumulative partial-payment allocation
  apply qualified person caps/rates/date rules and prior effective claim coverage
  newClaim = eligibleCumulativeClaim - priorEffectiveClaims
  require newClaim>=0 and no duplicated labour/payment entitlement
```

Official guidance distinguishes work/payment eligibility and partial-payment claim coverage; authority payment is not simply a tax-account deposit [X02]. Do not implement a generic current-rate multiplier independent of payment year or scope. No fixed statutory rates are activated here.

When the profile's recognition threshold for a claim receivable is established, reclassify its exact amount from the customer receivable to the authority claim receivable. Until then, retain the conditional split without an unsupported financial transfer. The customer and authority positions must jointly reconcile to recognized invoice principal after actual collections; never create both full customer debt and an additional full authority asset.

## Claim, outcome and rejection

A human approves the exact claim and scope. Persist one submission attempt before the external action and use documented outcome recovery. Registered/submitted claims do not mean paid. Actual bank receipt debits bank and credits the authority claim; a documented authority offset uses its actual destination obligation, not an invented bank receipt.

```text
onRejectedClaim(amount):
  retain authority decision and original claim
  if reviewed customer agreement supports additional customer debt:
      debit customer AR; credit authority claim amount
  else:
      prepare supported loss/dispute treatment with evidence
  do not create new sale revenue or VAT
```

Revisions reduce or replace explicit claim slices. Credits to the original invoice propagate through its relieved labour, claim/repayment and customer capacities using one complete owned plan. A cash-method case needs its own supported tax-recognition profile rather than silently borrowing accrual behavior.

## Complete journey

Show full invoice, customer payments, eligible labour, already claimed, accepted/rejected and collected amounts. Deadlines and identity use the qualified rule release. Keep sensitive person/property facts out of general summaries.

```text
synthetic invoice gross125000; supported claim25000; customer pays100000
reclass claim25000 -> combined remaining25000, revenue/VAT unchanged
claim accepted and bank25000 -> both receivables0
claim rejected -> customer debt or evidenced loss, never stranded invisible amount
same paid/work slice requested twice -> capacity refusal
```

Delivery requires actual claim artifact validation and an authorized official-channel outcome for the external stage. A plausible relief calculation is not legal/company qualification.


---

<a id="part-14"></a>

# NEXT-87: Pension invoice reconciliation and SLP annual basis

**Priority when applicable:** P2. **Lane:** PAYROLL.

**New work:** Add actual pension provider charges, reconciliation against accrued obligations and separate special-payroll-tax basis. Regular pay calculations do not implement this evidence lifecycle.

**Use existing owners:** Payroll provisions, purchasing, tax bridge, private personnel scope and tax-account assessment owners.

**Required earlier contracts:** NEXT-03, NEXT-20, NEXT-22.

**Conditional gates:** NEXT-35: payroll accruals already include pension provisions.

**Evidence basis:** R03, X03. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Contract and source components

```text
PensionCharge {providerDocument, employmentOrPolicyRef,
  coveragePeriod, components:[premium|riskInsurance|adminFee|other],
  exactAmounts, taxTreatmentWitness, correctionOf?}
PensionAccrualAllocation {payrollProvisionId, chargeComponentId, consumedProvision}
SLPBasisComponent {sourceIdentity, effectiveDate, statutoryCategory,
  signedIncludedAmount, exclusionReason?, reportingYear, ruleVersion}
```

A provider total may include pension premiums, risk cover and fees with different treatment. Neither all payroll cost nor all amounts on the invoice are automatically SLP basis. The official guidance distinguishes SLP and ordinary employer reporting [X03]; use the selected dated component rules and actual provider statements.

## Reconcile before recognizing twice

```text
compilePensionCharge(charge, accruals):
  require complete component classification and original provider identity
  for component:
    A = explicitly matched available prior pension provision
    C = qualified actual component cost excluding separately recoverable VAT
    debit pension provision A
    addSigned corresponding cost C-A
  V = separately qualified deductible VAT on supported fee components only
  debit input VAT V through the purchase tax owner if nonzero
  require sum(C)+V == retained invoice gross
  credit supplier payable sum(C)+V
  publish supported SLP-basis components from qualified recognition facts
```

Tax/deductibility is a separate component decision. A VAT-bearing provider fee uses the purchase tax owner where supported; do not subtract input VAT merely because a provider supplies pensions. A payment later settles AP only. Repeated payroll accrual and supplier-invoice intake cannot both own the same principal expense.

## Annual SLP computation

```text
prepareAnnualSLP(year):
  capture qualified included/excluded source components and prior carry basis
  reconcile provider statements, financial costs and documented timing differences
  B = sum(category-directed contributions under the selected statutory formula)
  T = qualified rounding and rate computation on supported taxable basis
  if negative/carry-forward treatment not supported by release: explicit blocker
  delta = T - priorEffectiveSLPExpenseLiabilityForYear
  debit SLP expense delta
  credit SLP liability delta
```

A corrected provider statement revises the supported target and produces only the delta. It does not post another full annual tax. The tax-account owner records actual assessed charges later. A calculated SLP liability is not provider payment, AGI submission or observed tax-account balance.

NEXT-22/74 consume exact declared SLP basis and its source/GL bridge through a dedicated form mapping. Keep this distinct from the ordinary contribution calculation and avoid adding pension components again as salary merely to reach a declaration.

## Atomicity, dates and privacy

Charge recognition, prior-provision release, supported basis facts and receipt are one transaction. Final annual SLP execution rechecks complete membership and prior targets. Retroactive corrections use the approved accounting date while preserving original coverage/reporting attribution; closed history is not rewritten.

Only permitted payroll users inspect individual pension details. Shared reports can show aggregate controls without granting raw employee access. No automatic provider certificate or contract entitlement is inferred from a received invoice.

```text
provision10000; actual premium11000 -> provision debit10000, cost debit1000, AP11000
synthetic SLP basis50000 at1/5 -> target10000; prior8000 -> adjustment2000
provider total contains unsupported fee -> named exclusion/blocker, not blanket inclusion
payment11000 -> AP settled, pension cost and SLP basis not recreated
```

Acceptance includes reconciled provider/GL/payroll contributions and the corporate-return consumer. Complete official tables, private facts and real provider access remain separately qualified inputs.


---

<a id="part-15"></a>

# NEXT-88: Employment termination and final-pay obligation closure

**Priority when applicable:** P2. **Lane:** PAYROLL.

**New work:** Add a reviewed employment-end event and complete final-pay inventory. This is not another regular salary or generic paid-correction implementation.

**Use existing owners:** Employment/work revisions, holiday balances, employee claims, payroll runs and paid-reporting owners.

**Required earlier contracts:** NEXT-20, NEXT-21, NEXT-35, NEXT-36.

**Conditional gates:** NEXT-87: pension obligations require a final provider settlement.

**Evidence basis:** R03, P35, P36. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## End event and still-open obligations

```text
TerminationRevision {employeeId, actualEmploymentEnd, noticeTerms,
  lastWorkCoverage, reasonCodeRestricted, applicableAgreement,
  finalPaymentPolicy, signedDecisionEvidence}
FinalPayInventory {ordinaryEarned, unprocessedVariablePay, remainingHoliday,
  benefitsEndFacts, reimbursements, lawfulDeductions, pensionItems,
  unfulfilledExternalReporting, unknownItems}
```

Ending employment does not erase a debt, future payroll adjustment or access to retained payslips through an authorized historical channel. The source event and private personnel documents use payroll access, not general party directory permissions.

## Calculate a bounded final run

```text
prepareFinalPay(termination, cutoff):
  capture complete paid/recognized/work/holiday/claim membership
  require termination date and actual scheduled work, not salary divided by30 by default
  use qualified payroll formulas for remaining salary and unused leave entitlement
  release already accrued holiday and related provisions to avoid duplicate expense
  include approved unpaid reimbursements through their existing liability route
  enumerate every proposed deduction with its separate lawful basis
  do not offset a recovery claim merely because the employee owes the company money
  calculate withholding/contributions using actual intended payment/reporting facts
```

The first supported profile excludes complex severance, disputes and cross-border exit treatment unless explicitly qualified. Unknown final expense claims or benefit-return facts remain open checklist items rather than zero amounts.

Final-run execution is an ordinary payroll aggregate with exact approval, input versions and earning identities. It consumes each outstanding source component once. A concurrent regular run for the same earning period cannot pay the same wages again.

## Close scheduling without blocking legitimate later facts

```text
executeEmploymentEnd(plan):
  atomically retain end revision and stop eligible future recurring work-generation rights
  invalidate unexecuted overlapping salary preparations
  leave original approved/paid runs and reporting items unchanged
  create final-pay and remaining-obligation tasks through existing owners
```

A scheduled payment already admitted externally cannot be cancelled merely by ending the employee record. Its payment owner resolves the actual outcome. New post-end earnings corrections must reference the ended employment and use NEXT-36, not resurrect an active recurring salary template.

## Reporting and final status

Paid/provided dates determine reporting under the qualified rules, independent of last employment day. NEXT-73 handles submission. A final-pay slip does not prove all employer obligations are discharged.

Define `financialObligationsComplete` from an exact inventory: all known pay and benefit cases resolved, employee/withholding controls reconciled and required follow-up assigned. Keep separate states for employment ended, final calculation, paid, declarations handled and unresolved provider obligations.

```text
holiday liability12000; final supported holiday pay15000 -> release12000,
    additional expense3000, not another15000 expense
employee claim2000 routed to final payroll -> claim liability consumed once
recovery claim5000 but no lawful deduction decision -> cannot silently reduce net5000
new expense claim after final run -> new owned claim/payment, no repeat final salary
```

The UI must expose missing facts and the exact reason completion remains open. No automated employment-law judgment or blanket deduction authority is created.


---

<a id="part-16"></a>

# NEXT-89: Dividend resolutions, shareholder payables and KU31 preparation

**Priority when applicable:** P2. **Lane:** EQUITY.

**New work:** Add a company-side dividend lifecycle with real resolution evidence, shareholder entitlements and reporting. It is not owner expense reimbursement or personal K10 optimization.

**Use existing owners:** Reviewed company/financial statements, ownership evidence, liability/payment and statutory artifact owners.

**Required earlier contracts:** NEXT-02, NEXT-22, NEXT-23, NEXT-49.

**Evidence basis:** X04, X05, P24. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Decision is not a forecast recommendation

```text
DividendResolution {entity, meetingEvidence, approvedFinancialBasis,
  declaredAmount, shareClassRights, entitledHoldersSnapshot,
  availabilityDate, paymentTerms, requiredBoardAssessment,
  legalProfile, version}
DividendEntitlement {resolutionId, holderIdentity, sharesOrRight,
  grossEntitlement, withholdingTreatment, paidComponents, KUIdentity}
```

The first profile is one supported ordinary AB distribution with actual meeting/board evidence and established shareholder rights. Cash headroom, retained earnings or an AI-generated minute cannot independently authorize a value transfer. Applicable capital-protection and prudence requirements need reviewed evidence [X05], not just a positive bank balance.

## Prepare and record

```text
prepareDividend(resolution):
  require actual authorised resolution and permitted financial/legal basis
  require complete entitled-holder snapshot and known class rights
  compute exact entitlements from the resolution's per-share or fixed allocation rule
  require sum(entitlements)==declaredAmount and all rounding differences explicitly resolved
  reject missing resident/status facts needed for supported withholding/reporting
  debit approved distributable-equity role declaredAmount
  credit dividend-payable role declaredAmount
```

This reclassifies equity into a liability only at the qualified recognition event. A draft distribution proposal remains nonfinancial. The accounting identity is the actual resolution, not its upload or review ID. Execute the journal and entitlement obligations together with independent required review and a receipt.

## Payment and reporting

Actual payout debits dividend payable and credits bank, plus a separately qualified withholding liability if required. Ordinary employee withholding rules are not reused. An instructed transfer or a due date is not cash evidence. Do not automatically assume either withholding or no withholding for every recipient.

KU31 preparation captures recipient identity, entitlement, relevant availability/reporting period and required form fields from the selected profile. It does not simply copy bank payment year if the actual legal reporting trigger differs. Preserve the original stable item identity for replacement reporting and retain exported/submitted evidence separately. Official examples illustrate issuer obligations for supported dividends [X04]; they do not activate every share/residency case here.

## Corrections and controls

A voided/mistaken resolution needs actual legal evidence and the appropriate supported accounting correction. Once distributed, do not silently reverse cash or deduct repayment from future owner expenses. A lawful recovery creates its own receivable and reporting-impact decision. Unsupported unlawful-distribution recovery remains a blocker rather than guessed income.

Reconcile total declared, actual payable, net payouts and withheld liabilities to the GL. Individual shareholder files have explicit private access; the general company view can show aggregate equity/liability effects.

```text
actual declaration100000 across rights3/5 and2/5 -> entitlements60000/40000
pay first holder20000 -> payable80000, equity already reduced100000 only once
same meeting resolution under new key -> AlreadyApplied
forecast shows surplus200000 -> cannot create dividend resolution or approval
```

Deliver issuer-side preparation, approved recognition, payout linkage and qualified KU31 handoff. No personal dividend tax planning, automated company-law conclusion or market-traded share registry is included.


---

<a id="part-17"></a>

# NEXT-90: Conditional grants, earned funding and repayment obligations

**Priority when applicable:** P2. **Lane:** INCOME.

**New work:** Add a bounded operating-grant lifecycle separate from sales and loans. This is a proposed accounting expansion, not a finding that a current grant implementation is defective.

**Use existing owners:** Source evidence, qualified recognition rules, GL, grant receivable/deferred-income and tax-bridge owners.

**Required earlier contracts:** NEXT-02, NEXT-03, NEXT-13, NEXT-22.

**Evidence basis:** R03, P31. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Conditions and earned coverage

```text
GrantAward {funder, agreementRevision, fundingCap, eligiblePeriod,
  eligibleCostCategories, milestones, evidenceRequirements,
  paymentSchedule, repaymentConditions, accounting/taxProfile}
GrantEntitlementSnapshot {awardId, recognizedEligibleCosts,
  reviewedAchievementEvidence, earnedTarget, cashReceived,
  previousRecognition, disputedOrUnknownConditions}
```

Start with a qualified cost-related operating grant. Customer consideration, asset-cost grants, state loans and uncertain funding awards are different profiles. Receiving money does not by itself establish income. A submitted application does not establish a receivable.

## Recognition graph

```text
eligibleCost = sum explicitly qualified actual cost components allocated to this award
require no source cost allocated beyond its permitted funding coverage
T = min(cap, qualified reimbursementFraction * eligibleCost)
require all recognition conditions evidenced before selecting earnedTarget T
D = T - previouslyEffectiveEarnedIncome
```

The profile fixes gross-income versus expense-offset presentation. It cannot switch based on which result looks better. The first implementation uses an explicit grant-income role so original expenses remain visible, unless the activated policy requires and implements another treatment.

Cash received before earning debits bank and credits deferred grant liability. As conditions are met, debit deferred liability to the available extent and debit a qualified grant receivable for any excess entitlement, with one credit to earned grant income. Later cash consumes the receivable first; genuinely unearned excess remains deferred rather than extra income.

```text
recognizeNewEarned(D):
  fromDeferred = min(D, unearnedCashLiability)
  debit deferredGrant fromDeferred
  debit grantReceivable D-fromDeferred
  credit grantIncome D
```

For a supported negative entitlement revision D=priorEarned-newEarned, first identify the matching uncollected entitlement U. Credit its receivable by min(D,U), debit grant income D and credit deferred or repayment liability by D-min(D,U). The selected award policy and actual funder decision determine which liability is correct; an unsupported classification blocks execution. All amounts refer to the same affected entitlement components, not unrelated receivables. Actual repayments debit that liability and credit cash with no second income reversal. Never leave a rejected receivable in place merely to preserve an expected dashboard balance.

## Atomic ownership and reporting

Each entitlement revision freezes award, cost and condition membership. Journal, recognised entitlement effects and cost-coverage claims commit together. A new review cannot earn the same cost twice under the same award. Multiple grants funding one cost need explicit allowed stacking limits; otherwise refuse overlapping funded coverage rather than double counting support.

Provider certification/submission and received funds are separate records. The corporate-tax bridge uses a qualified tax treatment and timing, not the assumption every grant is tax-free. Unknown conditions block complete recognition but not evidence capture or a cash receipt into deferred liability under the supported policy.

## UI and vectors

Show awarded cap, eligible cost, earned amount, unearned cash, receivable, repayments and outstanding conditions. Open work is tied to exact evidence gaps rather than a generic confidence score.

```text
cash advance50000 -> bank50000/deferred50000
eligible cost60000 at synthetic1/2 -> earned30000; deferred remains20000
later earned target70000 -> additional40000: deferred debit20000,
    receivable debit20000, income credit40000
cash receipt20000 -> receivable0, no new grant income
rejected condition -> supported entitlement reversal/repayment plan, not automatic tax exemption
```

Completion includes negative revisions, cash adoption and independent GL controls. This packet does not search for subsidies, promise funding or decide a real agreement's recognition terms without qualification.


---

<a id="part-18"></a>

# NEXT-91: Apply supplier credit balances to other payable invoices

**Priority when applicable:** P1. **Lane:** PURCHASES.

**New work:** Add noncash application of an established supplier refund/credit asset to another invoice. Creating credits/refunds and supplier advances do not yet define this settlement.

**Use existing owners:** Supplier credit asset, payable residual, allocation and payment reservation owners.

**Required earlier contracts:** NEXT-07, NEXT-57, NEXT-71.

**Evidence basis:** P07, P57, R02. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Pair actual rights

```text
SupplierCreditApplication {creditOrigin, targetInvoice, exactAmount,
  supplierAgreementEvidence, currency, expectedVersions, accountingDate}
CreditOriginPosition = original recognised refund/credit asset - refunds - applications
```

Require the same reviewed legal counterparty and supported currency. Party aliases or a duplicate-identity redirect do not themselves prove contractual permission to use the credit. Supplier advances retain their own treatment and consumption path; this packet initially consumes a genuine recognised credit/refund receivable.

## Prepare and execute

```text
prepareApplication(credit, target, x):
  require x>0 and x<=credit.available and x<=target.payableRemaining
  require actual supplier agreement/remittance allocation and current legal scope
  require no pending refund request or outgoing payment competing for x
  debit target supplier payable x
  credit supplier credit/refund asset x
  freeze exact origin, target, capacities, agreement and source relationships
```

A paid invoice cannot accept another application. Do not select a target simply because it has the same amount. Allocation can span multiple invoices through a fixed set of disjoint legs whose sums match the credit consumption.

Execution rechecks both capacity owners under one book transaction, including exported payment/refund reservations. It posts the noncash settlement journal, appends the credit consumption and target invoice allocation, updates the shared residual readers and saves one receipt. There is no bank entry, new purchase expense or new VAT credit.

If an existing compatible noncash posting already represents the agreement, adopt it through reviewed role/capacity evidence instead of posting again. Either mode must consume each right once; the UI cannot choose both under separate keys.

## Reversal and history

A mistaken application can be reversed through an owned exact allocation reversal while both sides remain available. If the invoice has since been credited, the credit refunded or the period consumed, return the dependency closure and require a supported coordinated correction. A generic journal reversal cannot restore capacity independently of the credit/invoice histories.

Stored balances remain derived from immutable origin/effect records. Do not introduce a mutable supplier aggregate that disagrees with payment eligibility. Statement, ageing and Cash readers see the target residual reduced and credit availability consumed at the same recorded cutoff.

## Journey and examples

Provide a supplier-credit page with eligible invoices, contractual application evidence and exact effects. Mixed currencies or different counterparties are explicitly unsupported unless a later qualified settlement profile exists. A tax-account or private-owner balance is not an interchangeable supplier credit.

```text
credit asset30000; invoiceA50000 -> apply20000 => credit10000, AP30000
then invoiceB8000 -> apply8000 => credit2000, invoiceB0
same credit refund request for remaining10000 races with application -> one wins
all applications plus refunds never exceed30000
journal debit AP20000/credit refundAsset20000; bank/expense/VAT delta0
```

Completion requires the shared invoice residual and refund-capacity consumers, not just the new application screen. Existing NEXT-07/57 identifiers and code remain the authorities for origins.


---

<a id="part-19"></a>

# NEXT-92: Documented bilateral receivable-payable setoff

**Priority when applicable:** P2. **Lane:** TREASURY.

**New work:** Add explicitly agreed same-counterparty AR/AP discharge without cash. This is not applying a customer credit or supplier refund to another invoice.

**Use existing owners:** Existing receivable/payable settlement and current party/authority owners.

**Required earlier contracts:** NEXT-30, NEXT-07.

**Evidence basis:** R02, P30, P07. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Bound the legal and financial case

```text
SetoffAgreement {entity, counterpartyLegalIdentity, signedOrReviewedEvidence,
  effectiveDate, identifiedClaims, permittedAmount, currency, legalBasis}
SetoffPlan {agreementId, receivableLegs, payableLegs,
  exactGrossDischarge, currentHoldsReservations, basisDigest}
```

Initial support is the same legal counterparty, book currency and already recognised accrual invoices. Related companies, group treasury, disputed eligibility, insolvency cases and foreign-currency release require separate qualified treatment. Never infer setoff rights from a directory merge or matched amounts.

Cash-method tax recognition on noncash settlement is not automatically the accrual result. Refuse that branch until its method owner supplies a qualified recognition contract; do not silently omit a possible tax trigger.

## Compilation

```text
prepareSetoff(agreement, selectedLegs):
  capture exact claim identities and legally eligible outstanding capacities
  require sums(receivableLegs)==sums(payableLegs)==X and X>0
  require X<=agreementPermittedAmount
  require no unhandled payment, refund, hold or assignment reservations
  debit payable controls by their exact selected legs
  credit receivable controls by their exact selected legs
  retain each claim's effective date and documentary release relationship
```

Different VAT treatments on the underlying invoices do not justify recomputing tax in this recognised-accrual settlement. A settlement discount or waiver is a different financial event and must be separately compiled by its owner.

## One atomic discharge

`executeSetoff` follows C4: current authority, receipt recovery, one book lock, stable claim-resource ordering, exact approval and current mutuality/evidence witnesses. It writes the balanced journal and both AP/AR noncash allocation sets on the same transaction, then one receipt. It must use the existing internal settlement ports, not call two public allocation commands that can commit separately.

Setoff blocks conflicting outgoing instructions before effect admission. An instruction with unknown remote outcome cannot be safely ignored; resolve or explicitly partition an unreserved amount. A later actual bank payment does not undo the setoff automatically; it becomes an overpayment against the updated obligation.

## Reversal and reconciliation

Both sides' histories retain the agreement and receipt. Reversal restores both claim capacities and its journal together only if downstream credits/payments permit it. Otherwise identify the consumed closure and refuse a one-sided reversal. An actual invalidated agreement is not merely a UI unmatch.

Reports distinguish noncash discharge from collections/payments. Cash excludes this amount from future incoming and outgoing contributions using the same linked event, not by creating equal forecast cash entries. Tax/AR/AP controls still trace to original recognised invoices.

```text
AR150000 and AP100000; agreed setoff80000 -> AR70000/AP20000
journal AP+80000/AR-80000; cash delta0
remaining invoice paid20000 later -> ordinary cash settlement on remaining leg
one side changes after approval -> whole setoff stale, no partial discharge
same agreement/claim slice under another key -> no duplicate use
```

Delivery is a narrow enforceable-setoff workflow with all shared readers updated. It is not an automatic treasury netting service or legal opinion about a company's right to withhold money.


---

<a id="part-20"></a>

# NEXT-93: Source-located evidence search and retained-page retrieval

**Priority when applicable:** P1. **Lane:** EVIDENCE.

**New work:** Add a searchable projection of retained originals and interpretation text with exact source locations. Extraction suggestions and agent context are not a document search index.

**Use existing owners:** Original evidence/content store, extraction attempts, permissions and existing artifact/retention owners.

**Required earlier contracts:** NEXT-26, NEXT-50.

**Evidence basis:** R02, R04. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Search is a projection, not evidence authority

```text
TextRevision {originalContentHash, extractorRelease, representation,
  pageOrSectionLocators, textHash, extractionWarnings, recordedAt}
SearchDocument {book, evidenceIdentity, sourceRevision, textRevision,
  accessClass, tokenizationVersion, indexedAt}
SearchHit {originalRef, sourceRevision, locator, exactSnippet,
  textRevision, interpretationState, score, limitations}
```

Use the existing database's suitable text index for the first bounded implementation before adding another search service. Source text, OCR/model interpretation and reviewed facts have separate labels. A search result does not confer authority on the original prose or prove the accounting treatment.

## Build and query

```text
indexOriginal(version):
  read authorised immutable source and supported native/extracted text
  retain source-located text revision with engine/version and known gaps
  outbox job stages index entries keyed by exact content/text revision
  publish only after complete selected representation is retained and validated
  old text revisions remain historical; current index pointers may advance

searchEvidence(scope, query, filters):
  validate bounded query grammar, book and permitted private scopes
  perform access-filtered search over selected index revision
  return snippets only from authorised hits with exact original locators
  distinguish partial index coverage from an exhaustive no-match result
```

A payroll original must not appear as a snippet to a user who only has aggregate accounting permission. Filtering after fetching/displaying snippets is too late. Search history, autocomplete counts and exports must follow the same scope rules.

## Reprocessing and navigation

Reindexing an original does not change accepted purchase fields, amounts or existing citations. Return the text revision used by the hit. The page/section viewer loads that exact original revision and highlights its locator; a locator that cannot be reproduced is shown as unavailable, never silently moved to similar current text.

Same-byte content may be associated with several legitimate source occurrences. Results can group identical content for convenience while exposing occurrence identities and their separate financial links. Do not merge those economic events in the index.

## Access and failure

Current authority is rechecked on opening/downloading an old hit. Revocation removes future access even if the browser cached a reference. Previously delivered bytes cannot be retracted; do not promise otherwise. Search suppression, retention expiry and legal retention remain governed by the existing evidence owner, not a delete button that destroys bookkeeping information.

Index lag or extractor failure appears as coverage diagnostics. The user can still open originals manually. An unavailable index returns an explicit degraded result; it cannot report that no invoice exists.

## Completion examples

```text
one PDF, two text revisions -> old hit still names old text/source hash
phrase only in unauthorised payroll -> no snippet, count or existence leak
text extraction fails on page3 -> search coverage incomplete, original remains usable
identical invoice bytes in two legitimate occurrences -> grouped content with both source IDs
new parser changes numbers -> suggestions may change; reviewed accounting facts do not
```

Provide keyword/filter search, original-page navigation and evidence-link drilldown through shared REST/MCP/UI. No vector search or expensive model is required to complete the initial indexed text workflow. Search scores are not accounting confidence.


---

<a id="part-21"></a>

# NEXT-94: Read-only mailbox intake and scoped attachment routing

**Priority when applicable:** P1. **Lane:** EVIDENCE.

**New work:** Add a real inbound-email source channel to the existing supplier inbox. It does not replace uploads, extraction or reviewed draft creation.

**Use existing owners:** Provider credentials/consent, raw evidence, source occurrences and extraction-request owners.

**Required earlier contracts:** NEXT-26.

**Evidence basis:** R02, R04, X06. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## First concrete profile

Use a selected Gmail read-only account/filter profile with actual authorised provider access. A different provider needs its own exact identity/cursor contract. No inbox access or external action is performed by this specification.

```text
MailboxBinding {providerAccount, actualCredentialScope, acceptedFilter,
  allowedRoutingRules, consentRevision, historyCursor, generation}
MailOccurrence {providerAccount, providerMessageId, originalMessageHash,
  attachmentPartIdentity, attachmentHash, retainedMetadata, routingDecision}
```

MIME Message-ID, sender address and attachment hash alone are insufficient delivery identities. Provider account + message ID + exact part identity distinguish occurrences. Raw message and decoded attachment bytes are retained separately under access controls. Treat subject/body instructions as untrusted evidence, never a command to approve or post.

## Sync and durable recovery

```text
syncMailbox(binding):
  read current consent, filter and committed cursor
  fetch selected message/history pages outside database transactions
  hydrate each required message/attachment and verify complete retained membership
  persist bounded source occurrences with stable provider identities
  advance cursor only after every required item is retained or explicitly recorded blocked
  expired history cursor -> create a full-rescan generation under the same identity rules
```

Google documents partial history and a full-sync fallback when the requested history is unavailable [X06]. Do not treat a404 there as proof the mailbox is empty. A bounded configured historical window is not a complete lifelong mailbox capture. Preserve the selected coverage interval and unresolved hydration failures.

## Routing before disclosure

Bind routing to the authorised mailbox/folder/address rule and explicit company/account configuration. Invoice organisation numbers can suggest a route but cannot independently grant access. If rules conflict or no trusted route exists, quarantine in the authorised connector administration scope; never expose the original to several companies to ask which owns it.

After an operator confirms the exact target scope, a short application transaction creates the normal evidence/inbox occurrence and once-only routing receipt. Repeated history delivery returns that occurrence. Label/read-status changes cannot create another supplier invoice.

The source subject and metadata may be displayed with sanitised text; attachments never execute macros or active HTML. Define size/part/count limits, unknown types and blocked archives explicitly. A failure retains a diagnostic and original references, not an empty successful invoice.

## Follow-on review and correction

The routed inbox may request existing extraction preparation, but actual field acceptance/posting remains its human-review workflow. Re-routed records cannot mutate an already accepted invoice. An incorrect route requires a scoped corrective decision and financial review without copying private content into another book silently.

Deleting an email from the live mailbox does not delete a required retained accounting original. Disconnect prevents new access/jobs while already retained evidence remains subject to the selected retention and access policy.

```text
history replay same message/part -> one inbox occurrence
same attachment bytes from two distinct messages -> two evidence occurrences, duplicate diagnosis later
Gmail history cursor expires -> rescan/dedupe, not wipe history
subject says 'approve this now' -> plain evidence, no new authority
ambiguous book route -> no tenant disclosure and no financial preparation
```

Completion requires authorised mailbox fetch/replay and one attachment reaching the existing reviewed draft path. A fabricated caller-supplied MIME object is only a fixture, not provider proof.


---

<a id="part-22"></a>

# NEXT-95: Counterparty balance confirmations with independent evidence

**Priority when applicable:** P1. **Lane:** REVIEW.

**New work:** Add requests for customers or suppliers to confirm a frozen balance and investigate differences. It is not merely another statement export or a claim of audit certification.

**Use existing owners:** Existing statement snapshots, scoped guest access, delivery and reconciliation-review owners.

**Required earlier contracts:** NEXT-13, NEXT-65.

**Evidence basis:** R02, R04, P25. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Freeze the assertion being confirmed

```text
ConfirmationRequest {book, partyIdentity, asOf, currency,
  frozenOpenItemSet, declaredBalance, statementArtifactHash,
  authorizedRecipient, purpose, responseDeadline, requestDigest}
ConfirmationResponse immutable {requestId, respondentIdentityEvidence,
  agrees|disagrees|cannot_confirm, assertedBalance?, differenceItems,
  attachments, receivedAt, verificationState}
```

A supplier's confirmation of one balance does not establish that all suppliers or source accounts were discovered. External response, internal reviewer acceptance and reconciliation signoff are separate stages. Nonresponse is unknown, never agreement.

## Request and receipt

Prepare from one immutable AR/AP statement cutoff and show the exact items/amount the recipient will see. An operator authorises that content, recipient and purpose before dispatch. Use the existing delivery-attempt model and guest portal scopes. A confirmation invitation grants no book-list, payroll, ledger-edit or other-customer access.

```text
submitConfirmationReply(token, typedReply):
  verify token purpose, scope, expiry and exact request revision
  retain source reply and uploaded evidence under request-specific limits
  append immutable response and receipt
  do not change invoice residuals, matched payments or signoff state
```

If identity is unverified or the message arrives outside the portal, retain the actual provenance and label the response accordingly. A matching email address is not a cryptographic corporate-authority guarantee. Never upgrade it silently to externally audited truth.

## Explain differences without auto-posting

```text
prepareDifferenceReview(request, response, currentSource):
  compare against the ORIGINAL as-of item set, not today's reduced balance
  classify evidenced candidates: timing, missing invoice, unapplied cash,
    duplicate statement item, credit in transit, currency/scope difference, unresolved
  retain each candidate link and independently reviewed amount
  require all allocations explain the stated difference without double counting
```

A late payment after the confirmation date belongs to a timing explanation, not a correction of the original statement. A real missing invoice routes to the source/purchase owner. A credit claim routes to the normal credit review. No response can directly generate a balancing voucher.

The reconciliation reviewer may accept the evidenced difference disposition for a named scope and cutoff. That attestation references all response versions and remaining unknowns. It is not a replacement for required bank/source controls or an implicit financial close.

## Revision, control and proof

Corrected requests create new versions with explicit supersession. Historical responses remain tied to the request they answered. A changed recipient invalidates unstarted delivery or needs fresh authorisation; uncertain prior dispatch cannot be assumed unsent.

```text
statement AR100000 asOf June30; July2 payment20000 -> response June30 compared to100000
recipient asserts80000 with evidence of June29 payment -> investigation, not automatic AR-20000
no response by due date -> pending/no response, never balanceConfirmed
unverified forwarded reply -> retained with identity limitation
new statement revision -> old token cannot answer the new amount
```

Provide request, response, differences and reviewer outcome in one usable workflow. Do not claim conformance with an audit standard or universal legal sufficiency from this product mechanism.


---

<a id="part-23"></a>

# NEXT-96: Multi-human approval routing and segregated review policies

**Priority when applicable:** P1. **Lane:** AUTHORITY.

**New work:** Add finite, versioned multi-reviewer routing for exact plans. Existing human approvals remain the financial authority; this is not unattended posting or an agent mandate.

**Use existing owners:** Current principal/role admission, exact approval records, task routing and final operation execution owners.

**Required earlier contracts:** Existing core operation owners.

**Conditional gates:** NEXT-67: budget classifications contribute to routing only, not permission to hide liabilities.

**Evidence basis:** R04, P16. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Policy, not a new financial interpreter

```text
ApprovalPolicyRevision {book, operationFamily, effectiveScope,
  exactRiskMeasure, thresholds, requiredRoleSlots, distinctHumanRules,
  conflictRestrictions, expiry, delegationRules}
ApprovalCase {planId, planDigest, policyRevision, riskBasis,
  slots:[{role, eligibleScope, decision?}], currentState}
ApprovalDecision {caseId, slotId, humanId, approve|reject, digest,
  currentMembershipWitness, recordedAt, supersedes?}
```

Routing depends on the actual operation's risk measure, not merely net journal total, which is always zero. For a payment batch, use gross approved disbursement; for a credit, use the affected claim reduction. Cross-currency threshold conversion requires a pinned reviewed policy and exact rate basis; otherwise refuse. A plan cannot be split into artificial fragments to evade a rule that explicitly covers one business request aggregate.

## Select and collect

```text
openApprovalCase(plan):
  choose exactly one applicable qualified routing policy
  derive risk and required slots from retained plan effects
  require enough currently eligible distinct reviewers or return UnstaffedPolicy
  persist case bound to exact plan+policy digests

recordDecision(case, slot, human):
  authorize current private/book role; lock case and declared authority resources
  require plan and policy still applicable and exact digest unchanged
  reject self-approval/conflicts required by the policy
  append immutable decision; never let one human fill two distinct-person slots
  reevaluate rejection/quorum state, save receipt
```

A delegate must be explicitly eligible for the slot under the same restrictions. Delegation does not copy the previous person's signature or bypass independence. A source/model suggestion can notify a reviewer but cannot fill a slot.

## Execute through the existing owner

An approval case reaching quorum is not itself a posting. It provides a supported approval-set reference to the ordinary named operation. At execution that owner rechecks exact plan binding, every required nonrevoked decision, current membership/role eligibility and expiry under the root lock protocol. A person losing authority before consumption can invalidate the quorum. Same-key recovery of an already committed result remains possible under current requester access, even if a former reviewer later leaves.

If the current single-approval schema cannot express the set, root introduces one explicit new supported approval contract/version. Do not fake quorum by having a service account mint the old single-human approval. No blanket shared policy engine gets raw arbitrary ledger writes.

## Change and UI

A material plan change requires a new case over a new digest. A policy change has explicit effective scope: urgent retroactive revocation can stop unexecuted cases, but it cannot undo a committed receipt. Historical decisions remain readable. Rejection and withdrawal are append-only, not deletion of an inconvenient review.

UI shows required roles, eligible assignees, conflicts, exact financial content and missing decisions. The amount explained to reviewers is the same risk basis used to select the policy.

```text
policy requires preparer-excluded finance+director, distinct humans
one person with both roles -> cannot supply two signatures
payment total1200000 in two legs600000 -> route by1200000, not each leg
reviewer revoked before execute -> unconsumed case loses valid quorum
committed command replay after reviewer exit -> same receipt, no reapproval/reposting
```

Complete one real operation family end to end before broadening. This packet does not grant agents approval rights or create standing execution budgets.


---

<a id="part-24"></a>

# NEXT-97: Exact covering-set reconciliation with explicit ambiguity

**Priority when applicable:** P1. **Lane:** BANKING.

**New work:** Add bounded one-to-many discovery and cross-proposal conflict analysis. Existing exact matches and reviewed allocation execution remain their owners.

**Use existing owners:** Current banking candidate reads, exact-money comparability and bank-allocation prepare/approve/execute operations.

**Required earlier contracts:** NEXT-09, NEXT-10.

**Conditional gates:** NEXT-70: the selected source is a structured bank file; NEXT-40: native foreign-cash comparability is supported.

**Evidence basis:** R05, P09, P10. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Candidate state

```text
CandidateBasis {observationId, account, currency, selectedDateScope,
  observationRemaining, ledgerCandidates:[{lineId, remaining, date, sourceRefs}],
  populationCount, poolComplete, versions, sourceEligibility}
CoverResult = UniqueWithinDeclaredPool | Ambiguous | NoMatchWithinDeclaredPool
            | IncompleteSearch | Unavailable
```

Compare signed, same-currency amounts only under the existing comparability contract. No stored qualified conversion means not comparable, not a raw numeric match. Candidate lookup failures stay unavailable. Opposite-sign decomposition, fees and generated adjustment vouchers are outside the first exact-sum profile.

## Bounded search

```text
findCovers(basis, maxSetSize, maxCandidates, maxVisited):
  qualify and deduplicate candidate identities; verify one consistent capacity per ID
  retain full population count and any excluded/truncated candidates
  search subset sizes k=1..maxSetSize using exact integer sums
  apply nonnegative remaining-sum bounds to prune, never tolerance plugs
  for each exact sum:
    retain IDs, total, maximum service/date gap and deterministic ranking components
  stop when declared computation budget is exhausted
  if exhausted or candidate pool incomplete: return IncompleteSearch with observed alternatives
  after completely exploring the first successful cardinality k, larger sets need not run
  select best date/other permitted rank within k, retaining all equal-ranked distinct covers
  one -> UniqueWithinDeclaredPool; many -> Ambiguous; none -> NoMatchWithinDeclaredPool
```

Stable ID ordering only makes output repeatable. It does not prove that one equal-ranked economic explanation is correct. A pool capped at40 candidates cannot claim uniqueness among every line in the book. Results name the exact scope searched.

## Several observations

Build a conflict graph over candidate covers sharing any observation or ledger capacity. Present incompatible alternatives together instead of independently labelling each a unique automatic match. A deterministic optimisation can rank whole-set proposals, but it must preserve ties and incomplete-search limits. User review selects the exact intended economic links.

```text
prepareSelectedCover(result, selectedIds):
  require original observation and selected candidate identities match the shown basis
  call existing allocation PREPARE with explicit legs outside any held caller tx
  owning allocation operation recaptures actual capacities and eligibility
  obtain human approval, then execute through that owner
```

This feature posts no fee/residual voucher and consumes no allocation capacity during discovery. For this initial full-residual cover profile, a candidate contributes its selected whole remaining capacity. Partial sub-leg search is a separate supported variant, not an undisclosed change to the search. Two competing selections resolve at the shared allocation owner's transaction. If one side changed, the selected proposal becomes stale rather than silently substituting another cover.

## Proof and operator experience

Show exact total, leftover zero, candidate provenance, search completeness and ambiguity. No confidence percentage is a calibrated probability unless independently evaluated. Requests can expand a bounded scope explicitly, never return an incomplete empty result as no match.

```text
target100; candidates70,30,60,40 -> two exact2-item covers, Ambiguous
max visited reached before alternate branch -> IncompleteSearch, not Unique
same ledger line suggested for two bank rows -> conflict shown, no double allocation
selected cover100 but one line already consumed20 -> owner refuses/reprepares
unsupported currency pair -> explicit exclusion, not 1:1 comparison
```

Delivery includes actual candidate-to-allocation review and two-successive-consumer recovery cases. It does not replace matching receipts or repair a supposed missing SQL rule.


---

<a id="part-25"></a>

# NEXT-98: Accountant period-review engagements and versioned acceptance

**Priority when applicable:** P1. **Lane:** REVIEW.

**New work:** Add an in-product accountant review engagement around exact period artifacts and findings. Book Zero already owns the review outcome; this adds its collaborative workflow rather than another close certificate.

**Use existing owners:** Book-scoped membership, review packs, existing cases, corrections and period-readiness owners.

**Required earlier contracts:** NEXT-13, NEXT-23, NEXT-25, NEXT-49, NEXT-50.

**Conditional gates:** NEXT-95: counterparty confirmations are part of the selected review evidence.

**Evidence basis:** R02, R04, P25. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Engagement scope

```text
ReviewEngagement {entity/book, period, purpose, assignedReviewers,
  authorizedSourceClasses, financialSnapshotSet, evidenceManifest,
  requestedProcedures, limitations, revision}
ReviewFinding {engagementRevision, sourceRefs, claimedIssue,
  severity, proposedResolutionOwner, replyEvidence, disposition}
ReviewAcceptance {exactEngagementDigest, reviewerAuthority,
  selectedFindingsAndDispositions, coverageLimitations,
  acceptedAt, currentnessState}
```

An accountant's access is explicitly delegated through existing membership rules. Being assigned a review does not automatically grant payroll details, payment initiation or authority to approve their own proposed corrections. Do not introduce a second identity system or call this an audit opinion.

## Capture and review

```text
prepareEngagement(period):
  retain exact financial reports, controls, open items, coverage and source manifest
  record all required procedures and unresolved inputs for selected scope
  grant only reviewed existing read permissions to the assigned reviewer
  send invitation through authorised delivery, without exposing unrelated books

replyToFinding(finding, evidence):
  retain versioned response and source links
  classify proposed financial correction, missing evidence or explained difference
  route financial changes to their existing prepare/approve/execute owners
  never modify the ledger directly from a comment or mark a fix complete from text alone
```

After a correction commits, a new engagement revision captures the affected reports and receipt. Old findings remain linked to what the reviewer actually saw. A reply may resolve an explanation without a journal; that outcome still requires the assigned review policy and evidence.

## Acceptance

```text
acceptReview(command):
  admitted tx: current reviewer scope, book/review locks and exact replay
  require exact engagement revision, completed selected procedures and no hidden mandatory finding
  verify resolution receipts and relevant source/control dependencies
  append acceptance with explicit limitations and digest
  update current readiness links, not financial period locks
```

Financial close, review acceptance, signature and external filing are distinct events. A local policy may require an accepted review before a particular close operation, but that is an explicit scope dependency, not a universal statutory claim.

A new material source or posting can stale the current acceptance. Irrelevant metadata changes need not invalidate it when the selected dependency model proves they do not affect scope. Never re-sign an old acceptance with the new reports' hash or hide unresolved findings behind a refreshed dashboard.

## Interface and outcomes

The accountant sees assigned engagements, required work, concise differences since prior review and direct source/report links. The owner sees actionable requests with preserved draft responses and one current acceptance state. Exports reproduce exact reviewed bytes and all limitations.

```text
review snapshotA accepted -> later correction produces snapshotB, A remains historical
owner writes 'fixed' but no required receipt -> finding not financially resolved
reviewer has no payroll grant -> cannot open private payroll original through a finding link
missing bank month -> engagement incomplete despite balanced trial balance
review accepted -> does not submit VAT or unlock a period
```

Completion is a real invitation, scoped review, correction/reply, recapture and accepted-result journey. Existing first-period qualification remains a separate observed company outcome, not assumed complete by installing this workflow.


---

<a id="part-26"></a>

# NEXT-99: Cash forecast vintage scoring and error attribution

**Priority when applicable:** P1. **Lane:** CASH.

**New work:** Add retrospective evaluation of saved forecasts, not another forecasting engine. Cash scenarios and historical cash-flow statements remain their original owners.

**Use existing owners:** Existing immutable Cash forecasts, payment-occurrence identities, actual bank/control observations and report snapshots.

**Required earlier contracts:** NEXT-13, NEXT-45, NEXT-50.

**Evidence basis:** R06, P45. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Preserve what was actually known

```text
ForecastVintage {forecastId, createdAt, economicAsOf, recordedCutoff,
  accountPerimeter, currency, predictedOpening, events, assumptions, horizon}
ActualOutcomeBasis {cutoff, observedCoverage, matchedPaymentOccurrences,
  actualOpening, datedSignedCashEvents, correctionsKnownAtEvaluation}
ForecastScore {vintageId, actualBasisId, identityLinks,
  dailyErrorComponents, metrics, incompleteOutcomeCases, version}
```

The original forecast is never rerun using later facts and labelled historical accuracy. Restated actuals can be used in a separately labelled score revision. Missing bank coverage or an unelapsed horizon remains incomplete, not a zero outcome.

## Conserved decomposition

Define error as actual balance minus forecast balance. Align events through the existing payment/economic identity, not amount/date similarity alone. For one matched same-sign aggregate P forecast and A actual, let W=min(abs(P),abs(A)) and s=their sign.

```text
timingError(d) = s*W*(indicator(actualDate<=d)-indicator(predictedDate<=d))
amountError(d) = s*((abs(A)-W)*indicator(actualDate<=d)
                    -(abs(P)-W)*indicator(predictedDate<=d))
```

Their sum equals that event's actual-minus-predicted cash contribution. Opposite-sign/unmatched events are explicit classification or scope cases, not forced into the timing formula. Partial payments first partition by the owner's conserved allocations; an individual payment cannot be matched to two predicted events.

Add opening-balance differences, actually absent/present economic events, scope/perimeter changes and documented FX valuation differences as nonoverlapping components. Every unexplained residual remains a score diagnostic. Do not attribute a changed account perimeter to customer lateness.

## Metrics and query

```text
scoreVintage(vintage, actualBasis):
  require same supported cash semantics or an explicit reconciliation bridge
  compute daily actual/forecast curves over the fully observed intersection
  compute exact signed error and sum of decomposed effects per day
  require decomposition == actualCurve-forecastCurve exactly
  report MAE as exact rational minor-units/day, maximum error, minimum-balance error,
         first-buffer-crossing difference and unmatched-event coverage
  leave percentage metrics undefined where zero/negative denominators make them misleading
```

Use held-out saved forecasts and report sample size/horizon/coverage. A correct closing balance does not imply correct liquidity timing. A credit not committed at the forecast cutoff may legitimately be a later event, not evidence that the forecast ignored known information.

## Persistence and readers

Capture actual memberships under a fixed recorded cutoff, calculate outside locks and persist the score with immutable identity links. A later payment/reconciliation change produces another score revision. This is read-only financial analysis; it does not change due dates, probabilities, legal balances or payment plans.

The UI shows original forecast assumptions and each explainable error. Any suggested model/heuristic improvement becomes a separately evaluated policy version, not an automatic rewrite of future invoice expected dates. Restricted payroll contributions stay aggregated unless the evaluator has permission to inspect them.

```text
forecast +100 on day5; actual+80 on day7
at day5: timing -80 + amount -20 = balance error-100
at day7: timing0 + amount-20 = balance error-20
forecast closing correct but day5 liquidity shortfall -> timing error still visible
actual statement missing last week -> horizon incomplete, no full-horizon score
```

Deliver one retained vintage-to-realized-outcome comparison with exact decomposition and coverage. No claim of improved predictive accuracy follows from the existence of a scoring module.


---

<a id="part-27"></a>

# NEXT-100: Scoped integration event subscriptions and delivery receipts

**Priority when applicable:** P1. **Lane:** INTEGRATIONS.

**New work:** Add a concrete read-only outbound event subscription capability for external consumers. Existing outbox jobs are internal delivery, not a client-facing event contract.

**Use existing owners:** Existing scoped API authority, application outbox, effect-mq, immutable receipts and guarded outbound transport.

**Required earlier contracts:** Existing core operation owners.

**Evidence basis:** R04. See [SOURCES.md](SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](00-COMMON.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Finite public event surface

```text
SubscriptionRevision {book, subscriberPrincipal, endpointProfile,
  allowedEventTypes, payloadVersion, fieldProjection, secretRef,
  enabled, activationVersion, retentionAndReplayPolicy}
PublicEvent {eventId, book, type, ownerIdentity, ownerRevision,
  committedAt, minimalPermittedData, immutablePayloadHash}
DeliveryAttempt {eventId, subscriptionRevision, attemptId, targetDigest,
  admittedAt, responseEvidence, status}
```

Begin with a small explicit catalogue such as invoice issued, payment allocation committed, review requested and report ready. Event handlers do not execute supplied code or grant a financial write privilege. Sensitive payroll events are a separately scoped profile, absent by default. An integration marketplace/runtime is out of scope.

## From financial transaction to subscriber

```text
originatingOperation(tx):
  write actual domain effect and stable outbox intent in same transaction
  # A public event cannot exist as committed before the financial group commits.

publishEvent(intent):
  load exact committed owner result
  map through the versioned explicit event schema and authorised field projection
  retain payload once with stable event identity
  create delivery work for currently eligible subscriptions
```

No queue enqueue is performed while the financial lock is held. Duplicate outbox delivery produces the same event, not a second financial action. A consumer must treat event ID as idempotency identity; arrival order is not a global chronological guarantee. Provide an authorised read/snapshot path for gap recovery and a bounded retained replay range.

## Current authorization and transport

Before dispatch, check current subscription, subscriber/book permissions and endpoint/cancellation version. A revoked subscription cannot publish newly read private data. Retained historical payloads still require current permission to replay. Already delivered data cannot be retracted by deleting a subscription.

Use HTTPS and a reviewed endpoint policy. Reject credentials in URLs, unapproved private/internal destinations and redirect/DNS-rebinding escapes. A self-hosted internal endpoint requires a separate explicit allowlist, not a global insecure-mode flag. Resolve and connect under the guarded transport's verified destination contract.

A proposed v1 signature contract binds exact raw payload bytes, event ID, subscription ID, timestamp and key ID through HMAC-SHA256. Define canonical header formatting and freshness windows; never claim compatibility with another provider's webhook signature. Keep secrets in the credential owner, not queue payloads/logs.

```text
admitDelivery -> short scoped tx with current permission and attempt identity
send -> network outside tx with exact retained bytes
observe -> short tx retains bounded response and delivery outcome
```

A response success means the remote endpoint acknowledged transport, not that its business action completed. Lost response permits at-least-once redelivery of the same event identity, not a new financial command. Retry budget, backoff and dead-letter state remain explicit and inspectable.

## Rotation, disable and proof

Secret/endpoint rotation creates a subscription revision. In-flight attempts retain their admitted target/key identity; new admission uses current authority. Late ambiguous responses stay linked to the original attempt. Disabling stops unstarted dispatch and replay, while committed domain receipts remain recoverable independently.

```text
one invoice issue +3 transport retries -> one eventId, three attempts, one invoice
subscription loses book access before admission -> no outgoing payload
HTTP200 but consumer did nothing -> acknowledged transport only
same amount on two legitimate invoices -> distinct owner/event identities
queue history pruned -> domain idempotency and retained authorised replay policy still govern
```

Completion includes a documented receiver-verification example and an authorised test endpoint exercise. It does not require a new event broker or confer write access on webhook subscribers.


---

<a id="part-28"></a>

# Integration map and non-overlap record

NEXT-76..100 supplements the prior75 designs. It does not certify their implementation or replace their outstanding tasks. Only the new-wave dependency graph, including its declared conditional edges, is checked here. Earlier IDs are external contracts to resolve at dispatch.

## Ownership and prerequisites

| Packet | Required earlier contracts | New-wave dependencies | Conditional gates |
|---|---|---|---|
| [NEXT-76](packets/NEXT-76.md) | Existing core owners | None | NEXT-51: issuing invoices with the chosen tax/price profile |
| [NEXT-77](packets/NEXT-77.md) | NEXT-51 | NEXT-76 | NEXT-79: selected work already has unbilled revenue recognition |
| [NEXT-78](packets/NEXT-78.md) | NEXT-51, NEXT-59 | NEXT-76 | NEXT-79: prior earned revenue or conditional contract-asset treatment is selected |
| [NEXT-79](packets/NEXT-79.md) | NEXT-13, NEXT-51, NEXT-58 | NEXT-76 | None |
| [NEXT-80](packets/NEXT-80.md) | NEXT-03, NEXT-07, NEXT-08, NEXT-71 | None | None |
| [NEXT-81](packets/NEXT-81.md) | NEXT-03, NEXT-31 | None | NEXT-54: qualified import/landed-cost components enter the asset basis |
| [NEXT-82](packets/NEXT-82.md) | NEXT-19, NEXT-42 | NEXT-81 | None |
| [NEXT-83](packets/NEXT-83.md) | NEXT-31, NEXT-57, NEXT-59 | None | None |
| [NEXT-84](packets/NEXT-84.md) | NEXT-02, NEXT-13 | None | NEXT-22: the annual tax bridge consumes the selected deduction; NEXT-81: new commissioned assets enter the eligible tax pool |
| [NEXT-85](packets/NEXT-85.md) | NEXT-22, NEXT-49 | None | None |
| [NEXT-86](packets/NEXT-86.md) | NEXT-51, NEXT-15, NEXT-30, NEXT-49 | None | None |
| [NEXT-87](packets/NEXT-87.md) | NEXT-03, NEXT-20, NEXT-22 | None | NEXT-35: payroll accruals already include pension provisions |
| [NEXT-88](packets/NEXT-88.md) | NEXT-20, NEXT-21, NEXT-35, NEXT-36 | None | NEXT-87: pension obligations require a final provider settlement |
| [NEXT-89](packets/NEXT-89.md) | NEXT-02, NEXT-22, NEXT-23, NEXT-49 | None | None |
| [NEXT-90](packets/NEXT-90.md) | NEXT-02, NEXT-03, NEXT-13, NEXT-22 | None | None |
| [NEXT-91](packets/NEXT-91.md) | NEXT-07, NEXT-57, NEXT-71 | None | None |
| [NEXT-92](packets/NEXT-92.md) | NEXT-30, NEXT-07 | None | None |
| [NEXT-93](packets/NEXT-93.md) | NEXT-26, NEXT-50 | None | None |
| [NEXT-94](packets/NEXT-94.md) | NEXT-26 | None | None |
| [NEXT-95](packets/NEXT-95.md) | NEXT-13, NEXT-65 | None | None |
| [NEXT-96](packets/NEXT-96.md) | Existing core owners | None | NEXT-67: budget classifications contribute to routing only, not permission to hide liabilities |
| [NEXT-97](packets/NEXT-97.md) | NEXT-09, NEXT-10 | None | NEXT-70: the selected source is a structured bank file; NEXT-40: native foreign-cash comparability is supported |
| [NEXT-98](packets/NEXT-98.md) | NEXT-13, NEXT-23, NEXT-25, NEXT-49, NEXT-50 | None | NEXT-95: counterparty confirmations are part of the selected review evidence |
| [NEXT-99](packets/NEXT-99.md) | NEXT-13, NEXT-45, NEXT-50 | None | None |
| [NEXT-100](packets/NEXT-100.md) | Existing core owners | None | None |

## Cross-owner financial contracts

| Producer | New consumer | Required preserved meaning |
|---|---|---|
|Sales-order/invoice owner|76-79|Stable accepted component identities, draft reservations, once-only issue and credit history|
|Purchasing and schedules|81-83|Source cost capacity, exact already recognised purchase/tax, retained future schedule state|
|Asset and tax bridge|84-85|Book versus tax basis and pre-appropriation input stage, not a circular final-close prerequisite|
|VAT and external claims|86|Original consideration/tax plus separately qualified authority claim scope|
|Payroll/claims/holiday|87-88|Already accrued liabilities, actual paid facts and immutable prior declaration identity|
|Company evidence/statutory output|89|Actual resolution/availability facts and separate KU31 issuer reporting|
|Payable/refund residual owners|91-92|Noncash consumption included once in shared ageing/payment/Cash readers|
|Evidence/permissions|93-95|Original bytes, exact locators and current access; source assertions cannot approve accounting|
|Existing approval/execution|96|Exact quorum-set semantics supported by a new explicit contract, not forged legacy approval|
|Bank allocations|97|Candidate search is advisory; execution retains source/line capacities and rechecks scope|
|Reports/cases/close|98|Review acceptance of immutable scope, not a second financial certificate or ledger writer|
|Cash/actual source owners|99|Saved forecast vintages and independently reconciled payment identities|
|Outbox/capability owner|100|Minimal versioned public event, current subscriber authority and durable economic idempotency|

## Reservation policy

The historical VAT-03, FX-02-P1, AST-03, VAT-04-A1 and COM-2-W1 owners keep their current tasks. Names/numbers identify the original reservations, not a claim they are still unfinished. The current application migration owner also retains its ports and qualification. New consumers use released internal tx-passing functions or report the exact missing handoff.

No mandatory dependency is created on an optional profile merely because it shares a module. In particular97 may use existing booked native bank data without enabling a new bank-file importer;98 need not require a counterparty confirmation for every engagement;99 consumes an existing Cash forecast rather than forcing any tax strategy;83 does not wait for a finance-lease model.

## New versus already designed

**NEXT-76.** Add reviewed post-acceptance scope/price changes and billing-capacity conservation. This is not another webshop order intake, catalog or recurring-template owner.

**NEXT-77.** Add reviewed billable work capture and conversion into invoice lines. Payroll work facts, recurring invoices and deferred revenue remain separate owners.

**NEXT-78.** Add delivered-milestone acceptance and retained amounts on customer contracts. Invoice installments split due dates; they do not prove a milestone occurred or that retention is unconditional.

**NEXT-79.** Add earned-unbilled recognition before invoice issue. NEXT-58 defers invoiced revenue and is the opposite timing direction.

**NEXT-80.** Add supplier-side documentary dispute and explicitly bounded payment holds. Customer collection disputes and procurement acceptance do not supply this payable workflow.

**NEXT-81.** Add multi-source asset construction/acquisition accumulation and an explicit ready-for-use transition. Existing asset bases and depreciation schedules remain their owners.

**NEXT-82.** Add separately supported asset-component replacement and improvement accounting. Whole-asset impairment and disposal remain unchanged.

**NEXT-83.** Add contract-owned operating-rental commitments and deposit recovery. This is not a finance-lease/right-of-use asset or another recurring expense scheduler.

**NEXT-84.** Add a tax-value and deduction calculation linked to book assets. Ordinary book depreciation and income-tax calculation remain separate owners.

**NEXT-85.** Add optional tax-allocation reserve choices and their cohort history. Current-tax calculation alone does not own reserve deadlines or reversals.

**NEXT-86.** Add the explicitly conditional household-work profile, with labour evidence, split obligors and claim/rejection recovery. Mixed-rate ordinary invoices are not this workflow.

**NEXT-87.** Add actual pension provider charges, reconciliation against accrued obligations and separate special-payroll-tax basis. Regular pay calculations do not implement this evidence lifecycle.

**NEXT-88.** Add a reviewed employment-end event and complete final-pay inventory. This is not another regular salary or generic paid-correction implementation.

**NEXT-89.** Add a company-side dividend lifecycle with real resolution evidence, shareholder entitlements and reporting. It is not owner expense reimbursement or personal K10 optimization.

**NEXT-90.** Add a bounded operating-grant lifecycle separate from sales and loans. This is a proposed accounting expansion, not a finding that a current grant implementation is defective.

**NEXT-91.** Add noncash application of an established supplier refund/credit asset to another invoice. Creating credits/refunds and supplier advances do not yet define this settlement.

**NEXT-92.** Add explicitly agreed same-counterparty AR/AP discharge without cash. This is not applying a customer credit or supplier refund to another invoice.

**NEXT-93.** Add a searchable projection of retained originals and interpretation text with exact source locations. Extraction suggestions and agent context are not a document search index.

**NEXT-94.** Add a real inbound-email source channel to the existing supplier inbox. It does not replace uploads, extraction or reviewed draft creation.

**NEXT-95.** Add requests for customers or suppliers to confirm a frozen balance and investigate differences. It is not merely another statement export or a claim of audit certification.

**NEXT-96.** Add finite, versioned multi-reviewer routing for exact plans. Existing human approvals remain the financial authority; this is not unattended posting or an agent mandate.

**NEXT-97.** Add bounded one-to-many discovery and cross-proposal conflict analysis. Existing exact matches and reviewed allocation execution remain their owners.

**NEXT-98.** Add an in-product accountant review engagement around exact period artifacts and findings. Book Zero already owns the review outcome; this adds its collaborative workflow rather than another close certificate.

**NEXT-99.** Add retrospective evaluation of saved forecasts, not another forecasting engine. Cash scenarios and historical cash-flow statements remain their original owners.

**NEXT-100.** Add a concrete read-only outbound event subscription capability for external consumers. Existing outbox jobs are internal delivery, not a client-facing event contract.

## Practical release sequencing

Evidence93/94, approved contract changes76, acquisition/commissioning81 and exact matching97 are useful independent starts once their existing owners are released. Project77/78/79 require actual service-contract needs and mutually agreed recognition/billing coverage. Tax84/85/86/87/89/90 are conditional capability extensions, not a demand to delay Book Zero until every one exists.

Source presence, a passing pure example and a complete application journey are different statuses. When changing a financial owner, include all its current residual/read/correction consumers in the acceptance evidence. Root owns shared schema/grant migrations and the exact deployment checkpoint.


---

<a id="part-29"></a>

# Decisions selected for this wave

These are proposed implementation choices, not activated legal profiles or new repository code. They refine bounded workflows while retaining all previous financial owners.

## 1. Billing coverage belongs to the economic service

A new contract revision, timesheet edit or draft does not reset previously invoiced quantities. Accepted changes preserve component IDs. Time and milestone billing reserve and consume exact coverage through the existing issue transaction. A credit corrects consideration; it does not automatically authorise rebilling the same service.

Unbilled earned revenue and billed-but-unearned revenue are opposite states. Invoicing prior earned coverage releases its contract asset rather than recording that revenue again. Tax point, enforceable payment right and revenue recognition remain distinct.

## 2. Holds control payment, not recognition

Supplier disputes retain valid invoices in AP. Holds block explicit components and shared payment admissions, while undisputed eligible components can proceed. A downloaded payment file cannot be cancelled by creating a hold. Actual debt changes require the proper credit/correction owner.

## 3. Asset construction and component replacement preserve source costs

Costs flow once from purchase to eligible construction or asset components. Commissioning changes classification and starts approved recognition, not a new payable. Component retirement removes its own gross, ordinary accumulation and impairment before recognising replacement cost. No current estimate fabricates missing historical gross/contra proportions.

Tax depreciation is a dated tax calculation linked to book assets, not a second ledger. A qualified excess-depreciation reserve is posted only as its target-minus-existing appropriation and reconciles to the tax bridge. Book depreciation itself is not rewritten.

## 4. Reserve and special-tax arithmetic uses explicit stages

Corporate reserve choices consume a pre-reserve taxable-basis stage, add qualified releases and imputed income, then apply the chosen allowed allocation. This avoids taxing a computation that includes its own appropriation twice. Cohort dates are fiscal/tax-year identities, not fixed elapsed days.

Pension invoices consume existing payroll provisions before expensing only the difference. SLP has its own qualified annual basis and target delta; it is not ordinary salary withholding or a tax-account payment.

## 5. ROT/RUT remains full consideration with split collection

Invoice net and VAT remain complete. Conditional planned relief is not automatically an additional authority receivable. Recognise/reclassify the claim at the qualified evidence threshold and keep the combined customer/authority principal conserved. Rejection leads to a reviewed customer recovery or loss, never silent uncollectible residue.

## 6. Dividends and grants require actual rights

Cash headroom does not authorise a dividend. Record the actual corporate resolution and shareholder entitlement, then settle the recognised payable. Availability/reporting facts are distinct from the bank date.

For an operating grant, money received before earning is deferred. Qualified earned targets release that liability or establish an evidenced receivable. Negative targets remove the affected receivable first and recognise the required repayment/deferred liability for previously funded entitlement. Income is not reversed again when that cash is repaid.

## 7. Noncash settlement consumes both owners together

Applying a supplier credit debits the target payable and credits its existing credit asset. Bilateral setoff debits AP and credits AR. Neither invents a cash receipt, expense or VAT correction for already recognised accrual claims. Legal identity alone is not consent to set off. Both balances and the journal change in one application transaction.

## 8. Reconciliation search never turns limits into certainty

An exact sum can have several equally ranked explanations. Stable ID order makes output deterministic but does not prove uniqueness. The first complete successful cardinality can end search; a budget exhaustion or truncated pool remains incomplete. Discovery cannot consume money or book a residual plug. The current allocation owner rechecks every selected leg.

## 9. External evidence remains a statement by its source

Indexed text, inbound email and a counterparty reply are not human-approved accounting. Preserve exact original and interpretation revisions, route before disclosing and keep current permission checks. Nonresponse to a balance confirmation is unknown, not agreement. A matching sender address is not universal corporate-authority proof.

## 10. Additional reviewers approve the exact same plan

Finite required role slots and distinct-human constraints extend the current approval contract. Risk is operation-specific gross exposure, not balanced journal net. Quorum is rechecked at execution against current authority. A service account may not synthesize an old single-human approval to represent several reviews.

## 11. Review acceptance is neither financial close nor audit opinion

The accountant accepts a precise engagement revision with limits and finding dispositions. New material facts stale current acceptance without rewriting its historical content. Financial corrections use their normal owners. Optional governance gates reference that acceptance, but review cannot silently post, unlock or file anything.

## 12. Forecast scoring preserves the original information boundary

Retain the actual saved forecast. Compare it with an explicitly dated and independently supported outcome basis. Matched cash differences are split into timing and amount effects whose sum exactly equals actual minus forecast. Missing coverage remains incomplete. No model claim follows from a lower error measured after rewriting the old forecast with later data.

## 13. Public events are read-only notifications

A committed financial result can publish a minimal authorised versioned event. Retries retain the same event ID. Receiver acknowledgment does not prove its downstream business action completed. Revocation prevents new delivery/replay but cannot recall data already delivered. This does not add a plugin marketplace, raw-ledger API or external approval powers.


---

<a id="part-30"></a>

# Coordinator handoff: NEXT-76..100

Implement selected new packets against the actual current checkout, not against an assumption that the prior75 are complete. First read current AGENTS.md, architecture decisions and owner status. This specification's planning checkpoint is `66355b62b23e3b8007c2d324f3739fbbcc96cdc0`; later source can supersede a proposed name or already satisfy a slice.

Give each worker its packet, 00-COMMON.md, 01-QUALIFIED-INPUTS.md and the relevant source entries. Root retains shared contracts, global authority/transaction primitives, baseline/grants, journal admission, capability registration and common UI/job composition. No worker creates a second writable financial balance or independently changes lock ordering.

The next packet must be a genuinely new behaviour described in its delta, not a renamed unfinished earlier integration. If equivalent code is present, extend/qualify that owner and report the actual remaining difference. Preserve active work and do not revive the pre-release data-reset assumption for installed records. A new work number is not a migration number.

Implement through named Effect application operations and pure domain calculations. Every internal writer in a financial group receives the same transaction. Preserve exact source identities, semantic versions, scope, approval and original-key recovery. Jobs and remote calls run outside financial locks through the current outbox/effect-mq composition. Operator decisions, provider evidence and legal applicability remain different facts.

Prioritise selected company/customer needs. General evidence and source search, practical asset admission and matching can be useful without enabling optional tax/grant/termination profiles. Project billing76-79 belongs to a service-contract customer. ROT/RUT, dividends, special tax and grants require actual applicability; they do not become launch prerequisites for every AB.

Do not launch25 concurrent writers. Keep one retained owner per intersecting domain. Suggested independent preparation lanes are evidence93/94, banking97, contract76 and assets81, subject to actual current ownership. New tax work should follow the qualified inputs and existing tax-bridge stage contracts, not block source intake while awaiting company facts.

For each packet return the complete implemented journey, exact changed paths, required shared integration, schema/grant changes, independent expected results, checks actually run and unobserved gates. A pure calculator plus a status row is not completion. Respect actual permission for new repository tests, browser/provider exercises, production data and deployment. No such permission is created by this document.


---

<a id="part-31"></a>

# Sources, continuity and evidence limits

Repository checkpoint: `66355b62b23e3b8007c2d324f3739fbbcc96cdc0`, observed 28 September 2026. Targeted reads only. No cloned checkout, changed code, executed ERP, migrated database or provider workflow is claimed.

## Requested source basis

The attached `openerp-next-51-75.zip` was inspected and extracted locally. Its README and shared contract were read through Files; its solution index and packet metadata were used to check overlap. This new package expands rather than silently replaces those instructions. It preserves prior task IDs and authority boundaries.

NEXT-01..50 relationships use the earlier visible conversation dossiers/summaries. Those complete source archives were not reread in this turn. Their references below are design dependencies, not evidence they are fully implemented. The unrelated earlier allocation source in the conversation is not treated as current implementation proof.

## Current repository planning and path evidence

### R01: Pinned main-branch metadata

https://github.com/erik-kroon/openERP/commit/66355b62b23e3b8007c2d324f3739fbbcc96cdc0

Read scope: Branch metadata only.

Observed main at this revision. This does not establish an end-of-task latest-head claim or a full commit-diff review.

### R02: Capability backlog

https://github.com/erik-kroon/openERP/blob/66355b62b23e3b8007c2d324f3739fbbcc96cdc0/docs/plans/capability-backlog.md

Read scope: Requested lines90-255, returned requirement sections through document, sales, expenses and recurring work.

Supports owning areas and stated requirements. Historical missing/unowned language is not adopted as verified absence in current code.

### R03: VAT, payroll, assets and FX plan

https://github.com/erik-kroon/openERP/blob/66355b62b23e3b8007c2d324f3739fbbcc96cdc0/docs/plans/05-vat-payroll-assets-fx.md

Read scope: Requested lines1-180.

Supports dated profiles, termination/benefit inputs and distinct book/tax/asset calculations. Old migration/subset descriptions are planning history, not fresh runtime evidence.

### R04: Operations and review

https://github.com/erik-kroon/openERP/blob/66355b62b23e3b8007c2d324f3739fbbcc96cdc0/docs/operations.md

Read scope: Requested lines1-175; returned complete operation/review/provider sections.

Application ownership, authority, retained context and provider/outbox requirements. Its pre-release baseline language is not authority to reset current meaningful data.

### R05: Bank candidate application entry point

https://github.com/erik-kroon/openERP/blob/66355b62b23e3b8007c2d324f3739fbbcc96cdc0/apps/api/src/application/banking/candidates.ts

Read scope: Lines1-145 only.

Confirms the current scoped candidate application and selected capacity/comparability inputs. The unread remainder and other match modules were not audited; no complete absence claim for covering sets is made.

### R06: Book Zero and Cash

https://github.com/erik-kroon/openERP/blob/66355b62b23e3b8007c2d324f3739fbbcc96cdc0/docs/plans/15-book-zero-workflow-cash.md

Read scope: Requested lines100-230; returned results, scenarios and acceptance sections.

Supports saved Cash scenarios, outcome comparison by timing/amount/information and independent reviewer gates. Proposed NEXT-99 adds scoring mechanics, not another forecast authority.

## Prior packet aliases

`Pnn` means the corresponding `NEXT-nn` design from the preceding waves. It is a scope/contract reference, not a claim of execution or source presence. The current source owner must be reconciled at dispatch. For51..75, titles below come from the attached index.

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

P01..P50 refer to the unchanged earlier task IDs described in this conversation. Relevant examples: P03 purchasing, P07 supplier refunds, P13 statements, P16 period preparation, P19 asset disposal, P22 tax bridge, P24 annual report, P25 rehearsal/review, P26 extraction, P29 recurrence, P30 customer credit, P31 cost deferral, P35 variable payroll, P36 paid corrections, P42 impairment reversal, P45 cash-flow statement and P50 agent context.

## Narrow primary-source checks

### X01: Skatteverket: periodiseringsfond for AB

Separate annual reserve cohorts, release ordering and dated tax-year/vintage rules. The examples in the packet use synthetic factors. No complete release/exception corpus was qualified.

Observation limit: Official search-rendered pages; no full statutory-rule compilation.

https://www.skatteverket.se/foretag/drivaforetag/foretagsformer/aktiebolag/periodiseringsfond.4.4887341d16e1e2b8ddf30e.html

https://www4.skatteverket.se/rattsligvagledning/edition/2026.7/329552.html

### X02: Skatteverket: ROT/RUT work, payment and claim scope

Claim coverage depends on completed work and payment facts; partial payments and actual authority payment/offset are distinct. Do not copy a page example rate into every case.

Observation limit: Official search-rendered passages; exact production schema, current full eligibility/caps and company facts were not qualified.

https://www.skatteverket.se/foretag/etjansterochblanketter/svarpavanligafragor/rotochrutarbete/foretagrotochrutarbetefaq/narskajagsomutforareansokaomutbetalningdakundenbetalatbaraendelavfakturabeloppetexempelvisviddelfaktureringochvadhanderombetalningargorspabadasidornaavettarsskifte.5.71004e4c133e23bf6db800013003.html

https://www.skatteverket.se/foretag/skatterochavdrag/rotochrut/safungerarrutavdraget.4.64a656d113f4c7597011e41.html

https://www4.skatteverket.se/rattsligvagledning/edition/2026.14/326163.html

### X03: Skatteverket: SLP and employer contribution distinction

SLP on pension costs is distinct from ordinary employer contribution and other special payroll tax. Its basis belongs in the qualified income-tax reporting workflow. No actual rate or annual formula release supplied here.

Observation limit: Official search-rendered summaries; complete pension policy/provider data not read.

https://www.skatteverket.se/arbetsgivaravgifter

https://www4.skatteverket.se/rattsligvagledning/edition/2026.7/2912.html

### X04: Skatteverket: KU31 examples

Illustrates company-side distribution reporting and case-dependent withholding. The packet requires actual availability/recipient/form qualification; it supplies no universal dividend rule.

Observation limit: Official example inspected through search output, not a complete form/schema qualification.

https://www.skatteverket.se/foretag/skatterochavdrag/kontrolluppgifter/kontrolluppgiftomutdelningmedmerapadelagarrattku31/exempelpahurdufyllerikontrolluppgiftenomutdelningmmpadelagarratt.4.3810a01c150939e893f289fc.html

### X05: Aktiebolagslag: value transfer and dividend authority

A dividend is a legally authorised value transfer with applicable capital/governance conditions. A positive Cash forecast is not that authority. Effective-date selection is required; the consolidated text includes future provisions.

Observation limit: Official legislation search result, not a legal opinion or full current corporate-law analysis.

https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/aktiebolagslag-2005551_sfs-2005-551/

### X06: Google Gmail sync and message retrieval

Partial history can expire and require full synchronization; get supports retained full/raw message capture subject to actual authorised scopes. The proposed workflow adds domain-specific evidence/routing semantics.

Observation limit: Official pages opened; no Gmail account accessed or adapter exercised.

https://developers.google.com/workspace/gmail/api/guides/sync

https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages/get

## Design versus verified facts

All new equations, workflow records, bounded profiles and release sequencing are original proposed design choices, except the explicitly attributed general source observations above. A plan requirement does not prove a missing implementation. No assertion is made that a similar capability cannot exist in unread modules or current dirty branches.

The package does not contain official tax tables, commercial BAS text, employer agreements, signing credentials, provider schema packages, financial source originals or font files. Legal/date/rate/profile activation and actual external acceptance remain independent gates. Where a case exceeds the declared supported profile, refusal is explicit rather than a guessed fallback.

