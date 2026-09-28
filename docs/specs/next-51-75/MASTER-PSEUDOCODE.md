# OpenERP: NEXT-51 through NEXT-75

Complete wave-3 implementation specification. These are 25 new supported economic or external workflows over existing owners, not a reset of NEXT-01..50.

**Source basis:** `116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5`. **Status:** proposed pseudocode and contracts. No repository patch, live accounting, application test or provider qualification is claimed. Missing older integrations stay with their original packet.

The shared contract keeps business logic in Effect, exact calculation in domain/jurisdiction modules and atomic persistence in one caller-passed PostgreSQL transaction. Every new packet has a completion criterion beyond a pure leaf. Read the qualification and integration sections before scheduling work.

## Contents

1. [Shared contract: NEXT-51 through NEXT-75](#part-01)
2. [Qualified rules, external contracts and supported profiles](#part-02)
3. [NEXT-51: Mixed-rate domestic sales and tax-inclusive prices](#part-03)
4. [NEXT-52: Cross-border B2B service sales and customer-status evidence](#part-04)
5. [NEXT-53: Intra-EU goods acquisition and supply accounting](#part-05)
6. [NEXT-54: Customs imports, import VAT and landed-cost attribution](#part-06)
7. [NEXT-55: Periodisk sammanställning with correction lineage](#part-07)
8. [NEXT-56: Customer advances, deposits and final-invoice application](#part-08)
9. [NEXT-57: Supplier advances and final-purchase settlement](#part-09)
10. [NEXT-58: Invoice-driven deferred revenue and service-period changes](#part-10)
11. [NEXT-59: Installment terms, partial due amounts and payment promises](#part-11)
12. [NEXT-60: Payment discounts and evidenced settlement differences](#part-12)
13. [NEXT-61: Receivable allowances, confirmed losses and later recovery](#part-13)
14. [NEXT-62: Dunning interest and enforceable reminder fees](#part-14)
15. [NEXT-63: Self-billed sales and buyer-issued invoice acceptance](#part-15)
16. [NEXT-64: Invoice payment links with outstanding-bound settlement](#part-16)
17. [NEXT-65: Scoped customer document and statement portal](#part-17)
18. [NEXT-66: Purchase commitments and three-way invoice matching](#part-18)
19. [NEXT-67: Commitment-aware budgets with stop and warn decisions](#part-19)
20. [NEXT-68: Versioned BAS chart adoption and controlled annual updates](#part-20)
21. [NEXT-69: Spreadsheet master-data import with staged reconciliation](#part-21)
22. [NEXT-70: Structured bank-statement ingestion with exact entry lineage](#part-22)
23. [NEXT-71: Bank-qualified payment exports and status reconciliation](#part-23)
24. [NEXT-72: VAT declaration submission and authoritative return history](#part-24)
25. [NEXT-73: AGI submission and stable individual correction outcomes](#part-25)
26. [NEXT-74: INK2 filing, signature handoff and assessment attribution](#part-26)
27. [NEXT-75: Accounting-method change with conserved recognition coverage](#part-27)
28. [Integration and delivery map](#part-28)
29. [Design decisions resolved for NEXT-51..75](#part-29)
30. [Coordinator handoff: NEXT-51 through NEXT-75](#part-30)
31. [Sources, provenance and limits](#part-31)


---

<a id="part-01"></a>

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


---

<a id="part-02"></a>

# Qualified rules, external contracts and supported profiles

These requirements extend the existing company-profile, rule-release and provider owners. They do not create a second rules database, arbitrary policy-programming language or generic integration framework. A release is a finite typed input to a named implementation.

## Release manifest

```text
QualifiedRelease {
    id, family, semanticVersion, supportedCalculatorOrAdapter,
    effectiveDateScope, jurisdictionAndEntityScope,
    exactDataAndSchemaHashes, interpretationOfUnitsAndRounding,
    requiredCompanyAndTransactionFacts, supportedCases, refusedCases,
    sourceProvenance, reviewer, reviewReceipt,
    licenseOrUseConditions, independentExpectedCases
}
```

Preserve metadata that identifies a release separately from its optional family payload. Decode the shared outer release, validate its checksum and then select the correct family. A release with no selected payload is unsupported, not empty default data. Tax rates are not chosen by the most recent effective date alone; the actual supply, invoice, payment and reporting dates determine applicability.

Use the current qualified-profile admission owner. Source evidence, reviewed treatment, human approval and external mandate are separate authorities. A model may suggest a classification but cannot activate a missing profile or make a registry outage mean valid.

## Required inputs per packet

| Packet | Exact required policy/data | Explicit unsupported or unestablished boundary |
|---|---|---|
| 51 | Domestic supply classifications, effective rates, inclusive/exclusive pricing, line/document rounding, notices, allowance and credit rules | Every new rate/treatment requires actual applicable release; a zero rate is not an exemption decision |
| 52 | Service category and establishments, customer business/identifier evidence, place-of-supply rule, notices, reporting membership | No B2C or special-service fallback; unavailable customer verification remains unavailable |
| 53 | VAT territory, dispatch/arrival evidence, acquisition/supply status, tax basis and conversion rules | No triangle/call-off/margin or perpetual-stock inference |
| 54 | Actual customs declarations/revisions, importer identity, duties and already-included charges, import VAT and cost-allocation rules | Commercial purchase and customs taxable value are distinct; no duplicate expense recognition |
| 55 | Goods/services statement obligation, cadence, buyer/category keys, currency/filing units, original-error versus later-adjustment rules, selected export/submission format | Exact schema/provider package and company filing obligation still required |
| 56 | Identified future supply, deposit/advance distinction, payment/tax timing, rate changes, component application and refund treatment | An overpayment is not automatically a taxable advance; changed rates need an explicit compatible branch |
| 57 | Contract, actual payment, deduction evidence/date, advance carrying and final-application treatment | Foreign/nonmonetary advances and recovery/impairment require supported profiles, not payable revaluation by default |
| 58 | Service coverage and recognition method, contract changes, residual allocation, earned/unearned credit attribution | The first profile is explicitly time-based; milestones and variable consideration are not assumed |
| 59 | Contractual installment weights/dates, cash allocation order, legal amendment versus nonbinding payment promise | A forecast date does not edit due date; face amount remains the invoice owner's result |
| 60 | Discount entitlement, consideration/VAT correction, explicit fee/FX/currency rounding decisions and bounds | Small amount alone is never a qualification or rounding proof |
| 61 | Framework allowance policy, invoice-specific confirmed-loss evidence, tax relief and recovery treatment | General ageing allowance does not establish VAT relief or legal forgiveness |
| 62 | Contract/statutory authority, dated reference rate and spread, due-date/interest commencement, day count, fee entitlement and caps | No automatic fee, compounding, statutory number or consumer-credit product |
| 63 | Self-billing agreement/acceptance, external issuer numbering scope, applicable invoicing jurisdiction, tax notices and source responsibilities | Buyer-issued document is not automatically a purchase or a new self-issued invoice |
| 64 | Merchant account, payment method, exact checkout amount/currency, expiry/capture/idempotency/refund semantics and authenticated status | Browser return and local token expiry do not prove capture or remote cancellation |
| 65 | Authorized customer identity, exact resource scope, link/session expiry, revocation and retained artifact policy | No broad book query through guest credentials or unrevocable public bucket |
| 66 | Reviewed supplier commitments, quantity/value acceptance, invoice matching and accrued-service treatment | Purchase order alone is not AP, expense, tax or stock |
| 67 | Budget scope/period, qualified cost measure, exposure substitution, discretionary Stop/Warn rule and exception authority | A budget stop never deletes or refuses to record an already existing legal accounting event |
| 68 | Actual BAS reference release, use/license conditions, native account identity, effective rename/split/retire mapping and report/tax effects | Chart-name changes are not automatic tax/accounting policy |
| 69 | Selected workbook parser and file types, sheet/header/cell semantics, column maps, target schemas and private fields | First release need not support XLS/ODS. No macros, external workbook evaluation or blind numeric-ID coercion |
| 70 | Selected bank camt.053 message guide/XSD, booked balance types, parent/detail relation, direction/reversal rules and source identity | camt.052/054 and every bank variant need their own explicit profiles |
| 71 | Actual bank payment MIG/XSD, beneficiary/address/currency/calendar rules, message identity, status/rejection/cancellation proof | Valid XML is not bank acceptance; unknown outcome cannot release reservations |
| 72 | VAT submission API or official handoff profile, entity/period permissions, complete box serialization, replacement and signed-outcome meanings | Exact API machine contracts and credentials not acquired by this design |
| 73 | Selected AGI schema/period API, stable individual keys, permitted corrections, actual signing authority and private data retention | Registration permission is not signing permission; auxiliary facts can have distinct correction rules |
| 74 | INK2 main/annex edition, exact fiscal-year semantics, file/API channel, transfer and signature protocol, declaration outcome evidence | Income-tax filing and annual-report filing are separate; a transfer can still await signature |
| 75 | Official old/new methods, actual effective dates and permitted transition, old paid/recognized coverage, accounting/tax adjustment rules | Method change is not ordinary import or an app-level Boolean; unsupported direction remains unavailable |

## Selection and data preparation

```text
selectQualifiedCase(operation, facts, dates):
    candidates = active releases matching required family AND supported semantic case
    filter using the operation's relevant dates and actual entity/transaction facts
    if required fact absent: MissingEvidence with affected operations
    if no applicable qualified release: UnsupportedProfile with named case
    if more than one contradictory release: AmbiguousProfile, no default winner
    require exact data/schema checksums and finite implementation version available
    return typed witness with selected source facts and explicit refused branches
```

For algorithms that already exist in NEXT-01..50, consume that owner's selected calculation rather than porting a second copy. A partial-deduction purchase preserves source VAT and deductible VAT independently. A reporting integer cannot be compared as though it were minor units. A once-rounded cumulative target differs from summing individually rounded fragments.

The amount vectors in this package are synthetic. Fractions such as 1/4, 3/25 or 1/10 demonstrate exact mechanics and are not an activated statement of today's statutory rate for a real transaction.

## External profile contract

```text
ExternalProfile {
    environment, actualEndpointAndSchemaRelease,
    scopeAndRepresentativeRequirements,
    idempotencyKeySemanticsAndRetention?, readBackIdentity?,
    partialAcceptanceRules, authenticOutcomeValidation,
    signatureOrSubmissionCeremony, cancellationAndExpiryMeaning,
    operationalLimits, requiredExternalAcceptanceEvidence
}
```

Question marks mean genuinely optional provider capabilities. Do not invent them with a local UUID. The internal intent, provider request and real economic outcome each have identities. An actual credential store is required for live calls, but an offline parser/calculator does not wait for OAuth infrastructure it never uses.

No secrets, actual company facts, statutory table bundles, validation schemas or authentic external submission receipts are included in this package. The official sources identify what to qualify, not what was deployed. A useful file handoff can be delivered while connected access is pending, with the unsatisfied external outcome stated explicitly.


---

<a id="part-03"></a>

# NEXT-51: Mixed-rate domestic sales and tax-inclusive prices

Priority: **P0 when applicable**. Lane: **COMMERCE**.

**New deliverable:** Extend the bounded domestic standard-rate invoice into explicitly qualified reduced-rate, exempt and mixed-rate documents with inclusive pricing. This is new sales scope, not a repair of the original credit or purchase packets.

**Existing owner to extend:** Existing commerce invoice draft/issue/credit operations, legal policy, VAT facts and retained renderers.

**Required contracts:** NEXT-02, NEXT-04, NEXT-15. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** PRY-47, PRY-51, PRY-55; canonical family COM-02/04, VAT-02. Domestic standard-rate owner gains new mixed/reduced/exempt profiles, not a second issue engine.

**Atomic result:** Journal + invoice/tax components + original credit capacities.

**Evidence:** R03, R04, X01 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Supported slice and records

Start with one book-currency domestic accrual document. Each line names a reviewed supply classification, rate/treatment release, price basis, unit/base quantity and tax date. Exemption is a distinct legal treatment, not a rate chosen as zero. Construction reverse charge and cross-border rules are separate profiles. Do not assert a current rate without its dated release [X01].

Retain `LineTaxWitness`, `DocumentAllowanceAllocation`, `DocumentRoundingEffect` and a versioned `InvoiceTaxSummary` inside the existing sealed invoice. They are owned components, not another invoice table. The original monetary amount, exact intermediates, rounding residual, account-role binding and mandatory notice decision travel through issue and credit.

## Calculation

```text
compileMixedInvoice(lines,documentAllowances,policy):
    validate unique local line IDs and supported exact quantity/price units
    for line:
        treatment=selectQualifiedTreatment(line.facts,line.taxDate)
        compute exact quantity * unitPrice / baseQuantity
        apply its explicit line discounts/charges once
        if priceBasis==exclusive:
            N=qualifiedPriceRound(exactLineNet)
            T=qualifiedTaxRound(N*rateNumerator/rateDenominator)
            G=N+T
        if priceBasis==inclusive:
            G=qualifiedPriceRound(exactLineGross)
            N=qualifiedInclusiveBackout(G,rate)
            T=G-N
            require inverse/tax checks mandated by this inclusive profile
        retain {N,T,G,treatment,sourceLineId,residuals}
    assign each document allowance/charge to eligible treatment buckets
    allocate integer residuals by the selected stable allocation rule
    recompute the affected bucket/line tax using the declared tax-rounding level
    net=sum(all final line net)
    tax=sum(final bucket tax)
    payableBeforeRounding=net+tax
    delta=qualifiedDocumentPayableRound(payableBeforeRounding)-payableBeforeRounding
    return exact totals and every allocation; do not deduct line discounts twice
```

For a selected `gross-preserving-inclusive-v1` policy with rate numerator `r` and denominator `d`, the original proposed backout is `N=roundRatio(G*d,d+r,selectedMode)` and `T=G-N`. The policy must explicitly permit this gross-preserving remainder treatment and its calculation level. Do not combine it with an incompatible independent net-tax rounding promise or change an imported source assertion to force agreement.

A total document discount cannot be allocated wholly to a preferred tax rate for convenience. An allowance with known source-line attribution follows that evidence. Unsupported mixed jurisdictions or conflicting rounded source assertions are review failures, not guesses.

## Financial execution and credit

The existing issue operation posts debit AR for the final payable, credits the exact revenue and output-tax components and posts the explicit payable-rounding difference to its reviewed role. For debit-positive notation, the rounding line is `-delta`. A negative amount uses the opposite sign. Omit zero journal lines while preserving zero/exempt semantic facts.

Issue, numbering, per-line tax facts, semantic document, commercial obligation and receipt share one transaction. Extend existing posting-purpose admission instead of using a manual-journal bypass. Relevant accounts and treatment releases are checked again before commit. Metadata for future Peppol rendering is the same retained tax summary, not another calculation.

Credit selection reuses original line amounts and exact remaining capacities. It must not apply today's rate or recompute the whole document from mutable defaults. A final original-line credit consumes its exact remaining net/tax components. Update VAT capture and invoice residual readers in the same implementation slice.

## User flow and acceptance

The draft presents line classification, exclusive/inclusive basis, discount allocation, rate source, notices and total. Human approval covers the exact result. API/MCP prepare uses the same compiler; ordinary agents cannot activate tax profiles or approve issue.

Synthetic vector: net 10000 at 1/4, net 20000 at 3/25 and net 5000 under a qualified exemption gives tax 2500+2400 and gross 39900. Inclusive gross12500 at 1/4 yields net10000/tax2500 under that selected profile. A rounding delta must reconcile the AR face amount without changing source tax.

Finish with one mixed-rate issue, a partial credit, a final credit, retained PDF/JSON totals, VAT contribution reconciliation and response-loss replay. A new enum of rate names alone does not complete the packet.


---

<a id="part-04"></a>

# NEXT-52: Cross-border B2B service sales and customer-status evidence

Priority: **P1 when applicable**. Lane: **COMMERCE**.

**New deliverable:** Add the sale-side general-rule EU and non-EU B2B service profiles. NEXT-05 covers service purchases, not these sales or their customer-status evidence.

**Existing owner to extend:** Existing sales issue/credit and party fact owners; dated jurisdiction treatment selection.

**Required contracts:** NEXT-02, NEXT-04, NEXT-15, NEXT-51. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-17: The selected sale is in foreign currency and needs the existing monetary-item representation.

**Crosswalk:** PRY-47, PRY-11; canonical family COM-02/04, VAT-02. Sale-side general-rule B2B services are distinct from NEXT-05 purchase-side services.

**Atomic result:** Journal + AR + zero/output tax and cross-border reporting facts.

**Evidence:** R03, R04, X02, X03 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Evidence and explicit exclusions

Retain a `ServicePlaceDecision` for each supply, with supplier/customer establishments, customer business status, service category, participating fixed establishment, supply date and qualified determination. A two-letter country or a valid-looking VAT number is not sufficient evidence of the place of supply.

A `TaxIdentifierVerification` retains provider, queried identifier, response time, exact result, correlation and raw evidence. Outcomes include valid, invalid, unavailable and conflicting. The observation supports the reviewed decision, not a timeless guarantee. The first slice excludes B2C digital services, land-related services, admissions, transport and every special rule not explicitly implemented. An unavailable registry service does not silently establish exemption; qualified alternative evidence is its own reviewed branch.

## Preparation

```text
prepareCrossBorderServiceSale(draft):
    capture exact party revisions, original contract and supply facts
    decision=qualifiedServicePlace(facts,datedRelease)
    require decision is one supported branch
    if EU_general_B2B:
        require customer identity/status and applicable destination established
        retain required customer identifier and reverse-charge notice
        choose statutory reporting treatment and ESL eligibility under this release
    if nonEU_general_B2B:
        retain business-status/place evidence and applicable notice
        ESL eligibility=false with explicit reason, not absent
    price and convert using existing exact invoice/FX owners
    compile AR, revenue and only taxes actually due under this selected treatment
    publish traceable VAT and sales-list candidates for this same supply
```

For the supported no-Swedish-output-tax branch, debit AR `N`, credit revenue `N` and retain a zero-output-tax semantic fact. No zero journal line is required. The buyer's reverse-charge accounting is not a seller journal. A foreign tax obligation cannot be forced into this branch; it needs its own applicable jurisdiction profile.

## Atomic effects and later evidence

The shared issue transaction commits the legal document, recognition, AR and reporting facts. Where foreign-currency sales are selected, the existing commerce FX owner retains original units, carrying value and the qualified conversion witness. NEXT-17 is consumed only to the extent its released contract covers that case; a payable-only implementation cannot be passed an AR item as a substitute. NEXT-55 consumes the reporting fact without recognizing revenue again.

If a customer verification changes after issue, preserve the original evidence and create an impact case. Re-evaluate the affected supply date and actual facts. Do not retroactively rewrite every invoice based on today's registry result. A needed adjustment is an explicit existing credit/reissue or treatment-correction operation with financial, customer-balance and reporting effects together.

The new preparation can be implemented while live registry credentials are absent using supplied reviewed evidence, but automatic registry verification remains an unqualified adapter until observed. Do not infer registry availability from a browser link.

## User and agent experience

Show the exact reason for no Swedish output tax, required notice, evidence freshness and whether an EU sales-list record is expected. A missing fact blocks the affected sale, not capture of the draft. Surface a dedicated unsupported-service explanation rather than suggesting another rate until validation passes.

Synthetic vector: a qualified EU B2B service of100000 book-minor produces AR100000, revenue100000 and output tax0, plus one EU-services reporting source. The equivalent qualified non-EU branch has no EU-services reporting source. A later receipt of100000 settles AR only. A source fact appearing through both the invoice and an import must not create a second sale.

Completion requires issue, credit/correction, receipt recovery and the exact report adapter. A printed reverse-charge notice without an applicable decision or financial/reporting integration is incomplete. Official reporting coverage is broader than merely possessing a customer VAT number [X02].


---

<a id="part-05"></a>

# NEXT-53: Intra-EU goods acquisition and supply accounting

Priority: **P2 when applicable**. Lane: **TAX-COMMERCE**.

**New deliverable:** Add goods-specific intra-EU acquisition and sale profiles, including movement evidence. Neither service-purchase NEXT-05 nor service-sale NEXT-52 establishes goods treatment.

**Existing owner to extend:** Purchase/sales recognition and reporting fact owners, with existing asset/expense destinations.

**Required contracts:** NEXT-02, NEXT-03, NEXT-04, NEXT-15, NEXT-51. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** PRY-47, PRY-55/56; canonical family COM-02/04, VAT-02. Goods movement/acquisition/supply treatment is not inferred from the service profile.

**Atomic result:** Journal + original goods recognition + tax/movement lineage.

**Evidence:** R03, R04, X01, X02 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Bounded goods workflow

Create a reviewed `GoodsMovementDecision` linking invoice lines, dispatch/arrival evidence, origin/destination VAT territory, seller/buyer identity, transfer dates and one supported transaction classification. Customs territory, EU membership and EU VAT territory are not interchangeable labels. The initial slice covers a direct two-party movement with the reporting company as buyer or seller. Triangulation, call-off stock, installation supplies, margin schemes and own-goods transfers remain explicit unsupported profiles.

This packet does not implement perpetual inventory. Purchases must name an existing supported expense or asset destination. Quantity evidence can exist without a warehouse register; stock accounting is a separate prerequisite when it is required for the selected company.

## Purchase calculation

```text
compileAcquisition(invoice,movement,release):
    require complete movement and qualified acquisition decision
    B=qualified book-currency purchase cost
    BT=qualified VAT acquisition base using its own date/conversion witness
    O=qualifiedTax(BT,rate)
    D=qualifiedDeductiblePortion(O,reviewedUse)
    debit expense_or_asset B+(O-D)
    debit input_tax D
    credit supplier_payable B
    credit acquisition_output_tax O
    return financial and reporting components with separate B/BT lineage
```

A supplier's incorrectly charged foreign VAT cannot automatically become Swedish deductible VAT. Retain it as a source discrepancy or supported gross cost/claim treatment after review. No assumption that the acquisition output tax equals deductible input tax is permitted.

## Sale calculation and reporting

The supported qualifying intra-EU supply posts AR and revenue with no Swedish output VAT only after its own eligibility and movement decision. Otherwise refuse or prepare an explicitly reviewed alternative. Tax identifier verification and shipment documents are retained at issue. They do not replace proof of actual dispatch under the selected policy.

Both branches publish qualified reporting facts linked to the original supply, with acquisition/supply categories and original currency conversion. NEXT-55 consumes qualifying sale facts. A purchase never enters the seller's EU-sales list merely because its counterparty is in the EU.

## Transactions and later movement changes

Execute through existing purchase/sales internal writers on one supplied transaction: journal, obligation, tax facts, movement relationship, source identity and receipt. Where financial recognition precedes complete tax evidence, use only an explicitly supported pending-tax workflow with tracked liabilities and a blocking report condition. Do not label incomplete proof as zero-rated.

A returned shipment is not only a financial credit. Retain the return relationship and exact original line capacity. A credit reduces the original financial and reporting components under its applicable date rule. A source error is distinct from a later price change, a distinction NEXT-55 must receive. Never delete original shipment evidence or rerun all recognition when an attachment arrives.

## Completion and examples

UI shows logistics evidence separately from tax treatment and payment status. API readers expose source document, movement, selected role/rate witnesses and unresolved evidence. Cross-border stock use outside this slice is visible to Book Zero readiness.

Synthetic acquisition: B100000, BT100000, O25000 and D12500 produces debit cost112500, debit input12500, credit AP100000 and credit output25000. With D25000, cost remains100000. The later supplier payment creates no new acquisition VAT.

Finish with one acquisition, one qualifying supply, partial return/credit, VAT reconciliation and a sales-list source. Include changed movement evidence after approval, an unsupported triangular case and duplicate invoice/movement deliveries. Do not count two observations as two physical movements without an explicit occurrence distinction.


---

<a id="part-06"></a>

# NEXT-54: Customs imports, import VAT and landed-cost attribution

Priority: **P2 when applicable**. Lane: **TAX-COMMERCE**.

**New deliverable:** Add the customs assessment and import-tax basis alongside purchase recognition. A non-EU service purchase is not an imported-goods tax record.

**Existing owner to extend:** Existing supplier recognition, source intake, tax facts and supported expense/asset cost owner.

**Required contracts:** NEXT-02, NEXT-03, NEXT-04. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** PRY-55/56; canonical family COM-02, VAT-02. Customs import decisions and landed-cost attribution extend purchase recognition, not inventory custody.

**Atomic result:** Customs assessment delta + qualified cost/tax effects.

**Evidence:** R03, R04, X04 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Separate the documents and amounts

Retain `ImportEntryRevision` with customs reference and line identity, importer/legal entity, declaration/release decision, currency, customs value and authority-assessed quantities/charges. Link commercial invoice, freight, duty, agency fees and import evidence through explicit component relationships. A broker's invoice is not automatically the customs decision.

`ImportTaxBasis` holds the qualified customs value plus eligible duty/other charges and ancillary costs not already included. Skatteverket's 2026 guidance distinguishes this base from the supplier invoice and requires avoiding duplicate additions [X04]. The packet's first profile covers a reviewed Swedish import where the selected company is the relevant importer and its VAT reporting method is established.

## Cost and VAT compiler

```text
compileImportBasis(entry,linkedCharges,qualifiedRule):
    require unique external customs-line identity and version
    C=reviewed customsValueBookMinor
    additions=[]
    for charge:
        prove eligible kind and destination/time scope
        record includedInCustomsValue yes/no/unknown
        if unknown: block complete basis
        if no: include exactly the eligible component once
    B=C+sum(additions)
    O=qualifiedImportTax(B,rate)
    D=qualifiedDeduction(O,companyUse,evidence)
    return B,O,D with independent customs and purchase-cost witnesses
```

Financial purchase cost and customs tax base are not the same number. If commercial/freight/duty costs are already posted, adding them to `B` does not post those costs again. Their import attribution is nonfinancial provenance. An actual cost correction uses a separately reviewed cost delta through the existing expense/asset owner.

For the supported self-reported import VAT event, debit deductible input `D`, debit eligible non-deductible cost `O-D` and credit import-output tax `O`. If a different authority/payment regime applies, the profile supplies its different event semantics or the operation refuses. Do not create a Swedish AP for a self-assessed tax component just because it has an amount.

## Allocate landed cost without double recognition

A cost lot retained by the existing asset/expense owner may receive an allocated freight/duty component exactly once. Use reviewed weights such as value, mass or quantity with explicit units and stable residual allocation. Sum allocations to the charge's eligible amount. Unused amounts remain visible. A missing inventory owner blocks inventory capitalization rather than routing the balance to arbitrary expenses.

Customs reassessment appends a new effective decision. Compute a target-minus-effective delta per original customs component and qualified reporting rule. Preserve the original entry and earlier tax facts. A repeated amended XML or broker attachment is evidence of the same decision, not a new import.

## Execution, views and proof

The named import-tax application transaction rechecks current entry/charge relationships, posts the tax group, consumes its once-only external identity and writes tax facts/receipt together. Source attachment and actual foreign supplier payment remain existing separate owners. UI shows commercial cost, customs base, self-assessed output, deductible input and all included/excluded charges side by side.

Synthetic example: customs value100000, duty5000 and eligible freight2000 not already included yields B107000. At a synthetic 1/4 rate O26750. Full deduction gives input26750/output26750 and no extra commercial purchase. With already included freight, B105000, not107000.

Finish with an original entry, a reassessment, a previously posted broker cost and import-VAT return contribution. The accounting balances must agree independently of the customs-base arithmetic. Missing customs facts remain unknown rather than reusing a supplier exchange rate as an authority value.


---

<a id="part-07"></a>

# NEXT-55: Periodisk sammanställning with correction lineage

Priority: **P1 when applicable**. Lane: **TAX-REPORTING**.

**New deliverable:** Add EU-sales-list preparation, versioning and delivery handoff. VAT-return calculations and generic annual filing do not supply this distinct reporting obligation.

**Existing owner to extend:** Existing reporting snapshots, qualified releases, deadline/fulfillment and external-delivery infrastructure.

**Required contracts:** NEXT-04, NEXT-49. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-52: The selected statement includes general-rule cross-border services. NEXT-53: The selected statement includes qualifying intra-EU goods.

**Crosswalk:** PRY-47/55 and EU reporting requirements; canonical family VAT, END-06/07. EU statement artifacts and correction history are not the ordinary VAT return.

**Atomic result:** No journal; statement artifact, correction membership and submission observations.

**Evidence:** R03, X02, X03 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Scope and identities

Consume the exact qualifying sale facts produced by the EU service/goods owners. A service-only company needs NEXT-52, not implemented goods handling; NEXT-53 is conditional on goods activity. The combined dependency list is a coverage map, not permission to block a service-only release on irrelevant goods work.

Retain a `SalesListPeriodDecision`, a complete frozen source set and a `BuyerCategoryTotal` keyed by reporting entity, period, buyer VAT identity and reporting category. Reporting cadence is determined independently from VAT-return cadence using the qualified company/activity history. The official guidance distinguishes goods, services and combined activity and their correction rules [X02/X03]. Do not copy a VAT period ID and assume equivalence.

## Calculation and correction

```text
prepareSalesList(period):
    decide period/cadence from applicable rule and actual activity history
    capture all qualifying sources at one recorded cutoff
    require all necessary buyer identities/conversions and exclusions explained
    group exact book-currency consideration by buyer identifier and category
    apply the selected reporting-rounding rule at its specified grouping level
    retain raw sums, filing integers, residuals and source membership

prepareCorrection(originalFiled,changedFacts):
    for each affected buyer/category:
        if original source was wrong:
            compute corrected TOTAL for original reporting period
            retain original filed row and explicit replacement identity
        if later consideration changes:
            emit the qualified delta in the applicable later period
    require no implicit conversion of a later credit into an original-error correction
```

The official rule distinguishes replacing an erroneous original buyer total from reporting a later consideration adjustment [X03]. Zero and negative rows, identifier changes and empty-period obligations follow the selected format/rule. Do not silently drop negative values or send a nil list merely to mark the task done.

No journal is produced. This report consumes tax/supply facts without recognizing another sale. If a source correction requires accounting, that source owner completes the approved financial change before the successor report capture.

## Artifact and external outcome

Seal exact reporting data and the selected official file/service format. Render and validate outside financial locks, then attach immutable bytes and validation results. The first operational slice can provide an authorized official file-transfer handoff with actual retained receipt evidence. A direct API is used only when its actual specification and access are qualified. No guessed endpoint or screen automation is introduced.

Prepare, reviewed, transferred, submitted and authority receipt are separate states. Duplicate transfer uses the same external attempt identity where the provider supports it; an uncertain outcome stays unknown. Replacement/correction submissions link to the original scope and proof. NEXT-49 verifies typed receipts rather than accepting a text 'filed' flag.

## Reconciliation and completion

Reconcile qualifying sale totals to the corresponding VAT/supply facts at the same cutoff, with an explicit bridge for differences in reporting period, foreign conversion or correction treatment. Totals that happen to agree do not prove complete buyer membership. Show excluded categories, missing identifiers and a buyer drilldown to issued invoices and credits.

Synthetic example: buyerA services60000+40000 yields100000 for that category. An original source correction to the second supply at35000 produces a replacement total95000 for the original period, not a new35000 sale. A later contractual credit5000 instead follows the later-period adjustment rule. These amounts illustrate identity semantics, not reporting thresholds or due dates.

Completion requires actual capture, retained file, one original and one correction path, access after revocation and an observed authorized handoff outcome. A CSV grouped by buyer without cadence, correction lineage and source reconciliation is only a leaf.


---

<a id="part-08"></a>

# NEXT-56: Customer advances, deposits and final-invoice application

Priority: **P1 when applicable**. Lane: **COMMERCE**.

**New deliverable:** Handle money received before a supply with its own tax and liability timing. NEXT-30 deliberately distinguishes refundable excess cash from a taxable advance and does not implement that advance.

**Existing owner to extend:** Existing customer-credit, invoice recognition, bank-source and tax-fact owners.

**Required contracts:** NEXT-02, NEXT-04, NEXT-30, NEXT-51. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** Advance concepts in ERPNext review; canonical family COM-02/03/04, VAT. Customer advance tax timing differs from NEXT-30 refundable overpayments.

**Atomic result:** Cash/clearing + advance liability/tax + final AR application.

**Evidence:** R03, R04, X05 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Distinct economic classes

Retain an `AdvanceAgreementDecision` with identified supply, contract, tax classification, payer and application/refund terms. `RefundableSecurityDeposit`, `TaxableSupplyAdvance` and `UnappliedOverpayment` are separate cases. Do not classify them by the bank description. A pro-forma/advance request is not a final sale and does not automatically create revenue or VAT.

`AdvanceReceipt` retains gross principal, net liability carrying, source VAT, tax already reported, cash identity and exact remaining component capacities. It references existing cash and customer liability owners rather than introducing a second cash ledger.

## Receipt and final application

For the qualified taxable advance profile, actual receipt of `G=N+T` posts debit bank `G`, credit customer-advance liability `N` and credit output VAT `T`. The advance VAT timing must follow the selected applicable rule; payment is material under the official advance guidance [X05]. A security deposit profile retains gross liability without VAT until a separately supported tax event occurs.

```text
prepareAdvanceReceipt(source,agreement):
    require actual cash or compatible already-posted clearing source
    classify under reviewed contract and tax release
    derive retained N,T,G under explicit exclusive/inclusive basis
    prove cash event unused for this financial component
    seal journal + liability + tax facts + source relation

compileFinalSupply(invoice,advanceApplications):
    derive original final supply totals NF,TF,GF once
    for each application:
        release exact remaining advance net NA and previously reported tax TA
        require same supported supply/treatment relationship and gross GA=NA+TA
    remainingAR=GF-sum(GA)
    require remainingAR>=0
    debit AR remainingAR
    debit advance liability sum(NA)
    credit earnedRevenue_or_deferredRevenue NF
    credit additional output VAT TF-sum(TA)
```

Tax differences across rate/date changes need a qualified adjustment rule; the first profile can refuse them rather than use the subtraction above without justification. Partial deliveries release original components cumulatively with recorded coverage. The final invoice presents full supply totals, applied advances and amount due, while reporting facts explicitly distinguish prior tax from the newly recognized delta.

## Execution and refund

Issue/application is one transaction with invoice identity, journal, advance capacity use, AR and tax facts. Advancing a deposit does not reserve or consume stock/order quantities outside their own existing owner. An invoice already issued for the full amount needs a reviewed application/reclassification variant, not another issue journal.

An approved refund of unused taxable advance posts debit advance liability `N`, debit qualified output-tax reversal `T` and credit actual bank/refund clearing `G`, with its own source event and correction facts. Refunding already applied value must use the final invoice/credit owner. An unknown external refund outcome keeps its payment reservation and cannot trigger another refund.

Cash forecasts include future unused refunds or final receivables through the native payment identities. They do not include the original advance receipt again after it is already in opening cash.

## UI and completed journey

Show requested versus received, taxable versus security deposit, gross remaining, net liability, tax previously declared, applications and actual refunds. Separate commercial status from paid status. Preparation may be agent-assisted; tax activation, approval and external payments remain appropriately authorized.

Synthetic receipt12500 produces liability10000 and tax2500. Final supply37500, comprising30000+7500, consumes the advance and leaves AR25000: debit AR25000 plus liability10000, credit revenue30000 plus additional tax5000. Lifetime tax remains7500, not10000.

Complete with two partial applications, a final application, an unused balance refund, duplicate cash observation and a changed treatment between prepare/execute. Amounts and tax facts must reconcile to original advance capacities and the final invoice without manual SQL repair.


---

<a id="part-09"></a>

# NEXT-57: Supplier advances and final-purchase settlement

Priority: **P1 when applicable**. Lane: **COMMERCE**.

**New deliverable:** Add prepayment to suppliers before an expense or asset is recognized. NEXT-31 defers already recognized service cost and is not a supplier advance register.

**Existing owner to extend:** Existing supplier payment, purchase recognition, refund and cash-source owners.

**Required contracts:** NEXT-02, NEXT-03, NEXT-07. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** Advance concepts in ERPNext review; canonical family COM-02/03/04, VAT. Supplier cash prepayment is not NEXT-31 expense deferral or a credit of an unrecognized purchase.

**Atomic result:** Cash/clearing + supplier advance/deduction + final purchase/AP.

**Evidence:** R03, R04, X05 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Advance basis

`SupplierAdvanceDecision` identifies the supplier, underlying contract/supply, original currency, authorized payment destination and selected VAT evidence/timing. `SupplierAdvancePosition` stores gross paid, carrying value, claimed input tax and remaining source components. A supplier payment instruction alone does not establish an advance asset or VAT deduction.

The initial slice is same-currency with an explicitly supported tax profile. Foreign advances can be monetary or nonmonetary under their accounting treatment; do not automatically use the foreign payable revaluation algorithm. Missing supported treatment is a named scope limit.

## Pure financial contract

If eligible input VAT `D` is recognized on a paid advance with net `N` and source tax `T`, then gross `G=N+T` creates advance carrying `C=G-D`:

```text
debit supplier-advance asset C
debit deductible input VAT D
credit actual bank/payment clearing G
```

A qualified profile with deduction deferred until valid evidence can retain gross carrying and no claimed tax, with an explicit pending-tax fact. The default is not to invent a deduction from the rate printed on a payment request.

For a final invoice with total gross `GF`, deductible VAT `DF` and cost `GF-DF`, consume a compatible advance gross `GA` whose claimed VAT was `DA` and carrying was `GA-DA`:

```text
debit expense_or_asset GF-DF
debit newly deductible input VAT DF-DA
credit supplier-advance asset GA-DA
credit supplier payable GF-GA
```

This simplified vector requires matching eligible tax and supply coverage. Different tax dates, changed rates, partial applicability or already recognized final invoices require explicit qualified branches. A final invoice that has already generated its full AP uses a separate approved advance-to-AP settlement without recognizing cost or input VAT again.

## Transactions and allocations

Prepare captures the actual original cash, supplier, prior deductions and final source-line membership. Advance applications are allocated to final source components, not to an arbitrary whole-invoice total. The application transaction rechecks remaining capacity and executes journal, advance consumption, payable recognition/settlement, tax facts and receipt together.

Only one native financial owner may consume a given advance component. Store a stable economic identity independent of review ID and enforce at most one original cash recognition. A later supplier refund consumes the remaining advance/recoverable claim through the existing refund cash owner; it is not a purchase credit for an expense that never existed.

If a supplier becomes unable to deliver, create a reviewed advance impairment or recovery case. Do not flip the supplier advance into paid inventory or ordinary expense merely to clear an old balance. Corrections after final application must address the downstream invoice and tax facts, or refuse the unsupported chain.

## Controls and UI

Expose requested, instructed, paid, applied and refunded amounts separately. Reconcile the advance asset to active original positions and the AP residual to the existing shared invoice projection. A positive supplier advance is not a negative payable available for arbitrary netting. Forecast only the remaining committed cash using current native identity.

Synthetic advance: G12500 with D2500 gives carrying10000. Final purchase G37500 with D7500 debits cost30000 and newly deductible VAT5000, credits advance10000 and AP25000. Subsequent payment25000 settles AP with no new purchase tax. With no advance deduction initially, retain carrying12500 and final newly deductible VAT7500 under a qualified evidence-timing branch.

Completion requires one paid advance, partial application, final application, refund and retained controls through the actual HTTP/UI owners. An extra payment category or a negative AP line without component/deduction conservation is not the deliverable.


---

<a id="part-10"></a>

# NEXT-58: Invoice-driven deferred revenue and service-period changes

Priority: **P0 when applicable**. Lane: **SCHEDULES**.

**New deliverable:** Add the sales-side unearned-revenue lifecycle. NEXT-31 owns prepaid expenses/accrued costs, while recurring invoice occurrences do not establish when revenue is earned.

**Existing owner to extend:** Existing sales issue/credit and schedule recognition owners; reuse exact weighted allocation machinery.

**Required contracts:** NEXT-02, NEXT-15. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-29: The originating invoice is a recurring occurrence. NEXT-31: The shared schedule contract is being extended together with expense deferral; no duplicate schedule owner.

**Crosswalk:** PRY-52; canonical family COM-02/04, AST. Revenue liability/service recognition differs from NEXT-31 prepaid costs and NEXT-29 billing dates.

**Atomic result:** Revenue/deferral journal + schedule occurrence ownership.

**Evidence:** R03, R04 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Contract and source coverage

Retain a `RevenueRecognitionBasis` linked to immutable invoice lines and their approved service interval, performance evidence, net amount, residual treatment and method. The first profile covers a clearly defined time-based service using reviewed equal-period or day-weighted allocation. Milestone/percentage-of-completion accounting needs its own profile and is not inferred from a project label.

A service schedule, commercial billing schedule and payment schedule are different objects. A recurring invoice can bill services already provided or services yet to be provided. A security deposit is not deferred revenue. If NEXT-56 already carries an advance liability, final supply application must use that same carrying basis rather than recognize a second unearned liability.

## Calculation and issue integration

```text
compileDeferredRevenue(invoiceLine,cutoff,qualifiedMethod):
    slices=intersect([serviceStart,endExclusive),supported accounting periods)
    weights=qualifiedWeights(slices)
    shares=exact allocation of original NET consideration across slices
    require sum(shares)==original net
    earned=qualified consumed shares at cutoff
    unearned=originalNet-earned
    if issue not yet posted:
        allocate invoice net credit between revenue earned and deferred liability unearned
    else:
        debit original revenue unearned
        credit deferred revenue unearned
        create no new AR, cash or VAT
    retain schedule and future occurrence identities
```

Do not defer VAT merely because revenue is deferred. Tax facts stay on the applicable tax-point rule. Source tax and discount adjustments remain linked to original invoice components. Journal and schedule admission share a transaction at initial issue or the reviewed reclassification.

Each later occurrence debits deferred revenue and credits revenue for its approved retained amount. Compute due target less effective already-recognized amount. A queue retry cannot recognize a month twice. Human approval binds a fixed schedule batch or exact occurrence under the current owner policy, not an arbitrary future auto-post.

## Cancellation, credits and changes

A service-period amendment changes only the eligible unrecognized remainder. Allocate from current carrying, not the original full invoice again. Preserve previously recognized occurrences. If a correction to past recognition is needed, route a complete approved correction rather than editing old schedule rows.

A credit identifies whether it reduces earned service, unused future service or both. The qualified credit journal debits the corresponding revenue and/or deferred liability, debits eligible output-tax correction and credits AR/customer-credit liability. Retire or revise the future schedule atomically with the legal credit. The old schedule cannot continue recognizing refunded service.

Existing credit-number, source capacity and refund behavior remain NEXT-15/NEXT-30. This packet supplies the revenue-recognition counterpart and schedule effect, not a second credit document.

## Views and proof

Show invoice net, service interval, earned-to-date, remaining liability, recognized occurrences and pending future actions. Report explanations reach the exact source line and approved timing rule. Cash uses the remaining invoice/advance payment identity, not monthly revenue as monthly cash.

Synthetic annual net120000 with12 equal months produces10000 per month. After three months, revenue30000 and deferred liability90000. A credit for six unused months consumes deferred60000 plus its qualified original tax correction, leaving deferred30000. No extra cash event occurs until a refund or settlement is actually observed.

Complete with initial issue, first recognition, later month, future service shortening and a credit after partial recognition. Verify both the GL rollforward and retired future authority. General schedule creation without invoice/credit integration remains a leaf, not completed revenue deferral.


---

<a id="part-11"></a>

# NEXT-59: Installment terms, partial due amounts and payment promises

Priority: **P1 when applicable**. Lane: **COMMERCE**.

**New deliverable:** Partition one invoice receivable into contractual due installments and retain later payment promises without multiplying the invoice or changing legal dates silently.

**Existing owner to extend:** Existing invoice residual/allocations, collection work and read-only Cash contribution adapters.

**Required contracts:** NEXT-15, NEXT-30. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-50: Include installment and promise summaries in agent context.

**Crosswalk:** Payment-term schedules in ERPNext review; canonical family COM-03/06, Cash readers. Legal installment residuals and payment promises extend one native obligation, not recurring billing.

**Atomic result:** No journal for term or promise changes; shared settlement updates remain owned.

**Evidence:** R04, R05 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## One debt, multiple timing components

`PaymentTermRevision` binds the issued invoice, legal agreement, date rule and exact amounts or reviewed weights. `Installment` has a stable ID, contractual due date, initial principal and links to reductions. `PaymentPromise` is a separate expectation with source, promised date/amount, review and expiry. A promise does not replace a contractual due date or change the ledger.

The sum of installment principal equals the invoice's original eligible collectible amount. Installment remaining sums to the SAME live invoice residual after native payments, credits, advance applications and write-offs. These rows are timing/allocation detail, not a second mutable debt ledger.

## Calculation and allocation

```text
prepareTerms(invoice,weightsOrAmounts,dateRule):
    require legal agreement and exact invoice/tax/rounding basis
    amounts=reviewed amounts OR stable residual allocation of total across weights
    require sum(amounts)==invoice principal and each amount>0
    dates=qualified contractual rule with explicit calendar adjustment
    retain original terms and successor revision identity

allocateInvoiceReduction(reduction,selectedInstallments):
    recover existing native financial identity first
    use explicit reviewed mapping OR qualified deterministic waterfall
    require allocation sum==the eligible reduction amount
    require each amount<=current installment remaining
    preserve actual cash, credit and write-off types separately
    append installment allocations in the SAME tx as native invoice consumption
```

Contractual due dates are not assumed to be evenly spaced months. No business-day adjustment is inferred from a date library alone. Rounded residuals use a stable specified installment order. Payment fee/interest obligations remain separate from installment principal.

## Terms change and delinquency

A genuine restructuring records the old arrangement, legal basis, exact unchanged or qualified changed principal and successor unpaid schedule. Previously paid installments remain historical. Replacing dates does not restore principal capacity or clear an existing overdue event as though payment occurred. If the new agreement contains interest, forgiveness or fees, the relevant financial owner commits that consequence with its own approved basis.

A payment promise can move an expected Cash date while leaving arrears based on contractual due date. Expired promises return to a visible undated/overdue expectation, not an invented next business day. Customer communications show the actual legal schedule and separately label promises.

## Atomicity and consumers

Attach terms to an unissued invoice in its issue transaction or append a reviewed timing arrangement to an already issued invoice with no duplicate AR. Credits/advance applications must notify the term owner internally so all residual views remain equal. Concurrent payments share the book/capacity lock; adding installment rows cannot authorize over-allocation.

Update aging to age each unpaid installment, not the whole invoice at its last due date. NEXT-28 reminders select due principal only under the selected stage policy. Cash emits the same installment identities once, replacing an old whole-invoice forecast rather than adding both. Invoice documents and statements retain the exact terms revision they displayed.

## Completion vector

Split original125000 into three equal-weight installments:41667,41667,41666 using stable residual order. A payment50000 consumes41667 from the first and8333 from the second, leaving0,33334,41666 and total75000. A promise to pay the second next week changes expected timing, not the contractual residual or the original due date.

Finish with term issue, cross-installment partial payment, credit allocation, restructuring of only the unpaid remainder and late promise expiry. Reconcile aging, statement, collection eligibility and Cash against one native invoice residual. No new journal should be created solely because due dates changed.


---

<a id="part-12"></a>

# NEXT-60: Payment discounts and evidenced settlement differences

Priority: **P1 when applicable**. Lane: **COMMERCE**.

**New deliverable:** Add economically classified discounts and small-difference settlement, without a general rounding plug. Existing exact allocation correctly refuses these unmodelled residuals.

**Existing owner to extend:** Existing customer/supplier settlement, credit, tax adjustment and bank-source owners.

**Required contracts:** NEXT-07, NEXT-15, NEXT-30. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-17: The settlement includes foreign-currency principal or a separately evidenced FX difference.

**Crosswalk:** PRY-34, PRY-51; canonical family COM-03/04, IMP. Explicit price/fee/rounding difference decisions are not a generic tolerance plug or a new FX owner.

**Atomic result:** Explicit discount/fee/FX/rounding journal + exact principal settlement.

**Evidence:** R03, R04 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Classify before calculating

`SettlementDifferenceDecision` selects one finite supported meaning: contractual cash discount, separately evidenced payment fee, qualified minor rounding, accepted commercial reduction or unresolved short payment. They are not interchangeable. Difference magnitude alone never decides tax or expense treatment. An unresolved short payment remains an outstanding amount.

Retain original invoice/source components, actual cash/clearing identity, declared deduction terms, deadline/payment proof, counterpart role, required credit-document relationship and tax adjustment basis. A foreign-currency difference is split by the existing FX owner before any commercial discount is considered.

## Compile the selected branch

```text
compileSettlement(invoice,actualCash,reviewedDifference):
    P=eligible principal to settle
    C=actual principal consideration from cash/clearing, excluding separate fees
    diff=P-C
    classify using evidence and a supported explicit profile
    if unresolved: settle only C, leave diff outstanding
    if cash_discount:
        require contractual eligibility on actual qualifying payment date
        derive net/tax release from ORIGINAL remaining source components
        require netRelease+taxRelease==diff
        require required legal-credit condition satisfied or create its owned credit atomically
    if fee: use the fee owner and do not reduce invoice price/tax without its evidence
    if rounding: require explicit economic and profile bound, record residual as such
    return journal + native principal consumption + adjustment provenance
```

A customer discount vector can be debit bank `C`, debit sales reduction `dN`, debit qualified output-VAT reduction `dT` and credit AR `P`, where `P=C+dN+dT`. Supplier discounts invert the commercial roles: debit AP `P`, credit bank `C`, credit purchase cost reduction `dN` and credit eligible input-tax correction `dT`. A profile where tax is unaffected uses its own qualified vector rather than those formulas.

When a legal credit was already issued, settlement consumes the reduced invoice balance. It must not post the same discount/tax correction again. Payment allocations reference the credit/discount event's once-only identity.

## Execution and correction

The named settlement operation rechecks invoice residual, actual bank/cash capacity, discount eligibility and document status before committing all journal, allocation, tax and source-usage effects. No raw difference account is accepted from an ordinary model payload. New account roles are selected/reviewed through the existing role owner.

A returned payment reverses actual settlement consumption and its dependent discount only under the qualified legal condition. Some discounts remain granted even if payment later fails; do not hard-code reactivation. If a credit/refund subsequently consumed the adjusted basis, an unsupported standalone reversal is refused with the impact chain.

The difference record, failed eligibility and remaining residual appear in the work queue. Operator override can establish a reviewed treatment, never bypass conservation, same-currency comparison or source uniqueness.

## UI, controls and examples

Preview shows invoice residual, actual paid amount, fee, FX, discount, tax correction and still-unpaid balance separately. API output must not label everything 'rounding'. Aging and Cash reflect the same effective principal; GL control and adjustment components reconcile independently.

Synthetic customer invoice10000, actual cash9800 and an eligible gross discount200 with original quarter-rate split160+40 yields bank debit9800, sales reduction debit160, output-tax debit40 and AR credit10000. Without qualified discount evidence, only9800 settles and200 remains due. A processor fee200 is not that price discount.

Finish with a qualifying and nonqualifying payment date, a pre-issued credit adoption, a later payment reversal, duplicate source delivery and two competing residual consumers. Never use a tolerance to declare the unmatched amount nonexistent.


---

<a id="part-13"></a>

# NEXT-61: Receivable allowances, confirmed losses and later recovery

Priority: **P1 when applicable**. Lane: **COMMERCE-TAX**.

**New deliverable:** Add impaired receivable valuation and confirmed bad-debt disposal without treating every overdue invoice as a credit. Neither normal customer credit nor a collection reminder creates this accounting.

**Existing owner to extend:** Existing AR residual, customer source-line tax, valuation/control and recovery cash owners.

**Required contracts:** NEXT-04, NEXT-15, NEXT-30. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** Receivable lifecycle extension; canonical family COM-04/06, VAT. Accounting allowance and confirmed tax loss are not customer credits or disputes alone.

**Atomic result:** Allowance/loss/VAT recovery effects + original receivable lineage.

**Evidence:** R03, R04, X06 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Three separate states

Retain an invoice-specific `CollectabilityAssessment`, an effective allowance target, a `ConfirmedLossDecision` and any subsequent `RecoveryEvent`. A book allowance changes valuation, not the debtor's legal principal. A credit changes the consideration for the supply. A confirmed bad debt has its own qualification and tax consequences. The official guidance requires the assessment of VAT bad-debt treatment for the particular claim, not merely a pooled age-based estimate [X06].

The first profile is same-currency accrual AR with known original line/tax and payment history. An unrecognized cash-method claim has no previously reported VAT to reverse. Foreign claims require the existing carrying-value owner, not nominal-rate conversion here.

## Calculation

```text
prepareAllowance(invoice,reviewedLossTarget):
    require target between0 and eligible remaining book carrying
    delta=target-effectiveAllowance
    debit loss expense delta
    credit receivable-allowance contra asset delta
    leave contractual AR principal and payment capacity unchanged

compileConfirmedWriteoff(invoice,claimPart,taxDecision):
    G=eligible original principal written off
    T=qualified VAT relief from original components, never inferred from arrears age
    A=allowance released for this exact claim portion
    debit allowance A
    debit loss expense G-T-A   # Negative amount reverses an over-provision.
    debit output-VAT relief T
    credit AR G
    consume native AR principal through one write-off identity
```

Tax relief can be zero or unavailable even when a book loss is justified. In that case, write-off and pending tax assessment are separate reviewed consequences. Do not fabricate a credit note or reduce taxable consideration solely to align reports. A later accepted tax adjustment posts its explicit delta and links to the original loss.

## Actual later payment

Civil recovery rights can remain after book write-off. A recovery record references the written-off principal capacity, not a recreated original invoice. Under a qualified case where recovered consideration restores the previously reduced output tax, receipt `C=NR+TR` posts debit bank `C`, credit loss recovery `NR` and credit output VAT `TR`. Tax restoration cannot exceed the relieved source components attributable to that recovery. Where no VAT was relieved, no restoration is manufactured.

A legally supported forgiveness is different from bad-debt accounting and changes recoverability rights. Record that decision rather than keep offering collection on a discharged claim.

## Atomicity and readers

Each allowance/write-off/recovery operation uses the existing journal plus AR/capacity/tax writers on one transaction. Recheck original-payment and credit consumption before execution. A concurrent customer payment makes an old write-off plan stale; it must not write off already paid principal. Recovering the same bank receipt twice returns the original result or conflicts by economic identity.

Aging shows legal principal, book allowance, written-off amount and collection status separately. Cash does not forecast a write-off as an outflow; forecast assumptions about uncertain receipts remain read-only reviewed scenarios. Controls reconcile gross AR, allowance and net carrying with retained source-level effects.

## Exact illustration and completion

Original claim125000 with eligible VAT25000 and allowance40000: confirmed write-off debits allowance40000, expense60000 and VAT25000, credits AR125000. With allowance125000, expense delta is-25000, releasing the over-provision. Later qualified receipt25000 with restored tax5000 yields recovery income20000, not25000 plus hidden tax.

Finish with partial allowance, increase/release, confirmed loss, late partial recovery and simultaneous-payment refusal. Keep independent evidence for book impairment and VAT qualification. An aging percentage dashboard is not this packet's completed workflow.


---

<a id="part-14"></a>

# NEXT-62: Dunning interest and enforceable reminder fees

Priority: **P2 when applicable**. Lane: **COMMERCE**.

**New deliverable:** Add financial interest and fee claims. NEXT-28 deliberately sends exact reminders without inventing those charges.

**Existing owner to extend:** Existing collections, contract/party evidence, AR and reminder-delivery owners.

**Required contracts:** NEXT-28, NEXT-30, NEXT-59. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** PRY-49; canonical family COM-04/05/06. Creates qualified monetary interest/fee claims; NEXT-28 only owns reminder dispatch.

**Atomic result:** Qualified interest/fee claim + receipt allocation, not implicit invoice repricing.

**Evidence:** R03, R04, X13 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Inputs and enforceability

A `DunningChargePolicy` is a reviewed contractual/statutory profile with applicability, rate-source periods, grace and accrual rules, day-count convention, claim dates, fee conditions and maximum supported amounts. Its legal basis is not a product toggle. Capture invoice/instalment principal history and actual payments/credits in economic order.

Separate `InterestAccrual`, `InterestClaim`, `ReminderFeeClaim`, `ChargeWaiver` and actual settlement. An unissued internal estimate is not necessarily an enforceable receivable. The selected accounting treatment determines when a book claim is recognized. No default reference rate, spread, fee or administrative charge ships in the compiler [X13].

## Exact segmented computation

```text
calculateInterest(claimScope,[start,endExclusive),policy):
    boundaries=principal changes + rate changes + applicable year/day-count boundaries
    exact=0
    for segment:
        P=eligible overdue principal under qualified date/order rule
        rate=one evidenced applicable rate
        exact += P*rate*dayCountFraction(segment)
    target=qualifiedCumulativeRound(exact)
    effective=previously recognized interest for the SAME coverage chain
    return target-effective with full segment witness
```

Do not compound interest or charge interest on fees unless a separately qualified profile permits it. A payment on a boundary follows an explicit contract convention. Repeated daily jobs calculate an incremental target rather than rounding and posting every day independently.

A fee becomes eligible only on its specified event/evidence. Retain one fee occurrence identity per legally supported event, not per failed delivery or retry. A reminder API's successful request does not by itself prove a legal charging condition.

## Financial application and settlement

An approved recognized charge debits a separate interest/fee receivable and credits the corresponding income role, with any applicable tax treatment explicitly selected. It does not amend original invoice principal or original sales VAT. A synthetic no-VAT example is not authority that every fee is outside VAT.

Payment allocation identifies original principal, interest and fee parts separately. Use explicit customer evidence or a reviewed legally appropriate waterfall. The amounts must sum to actual consideration, and each consumption is bounded by its own current capacity. A refund/waiver reverses the correct charge effect rather than creating a sale credit for the underlying invoice.

NEXT-28 renders the exact approved amount from these saved charge records. A stopped/cancelled message leaves the accounting event unchanged unless the selected charge condition actually depends on successful delivery. If it does, use a pending conditional claim and the evidenced outcome, not a fictional cross-system atomic transaction.

## Views and acceptance

Statements show original invoice residual plus separate charges and their basis/date. A debtor dispute may put collections on hold without deleting recognized receivables. A late backdated payment creates a target recalculation and reviewed adjustment, preserving prior charge documents. Cash lists only the qualified expected receipts, not all automatically calculated interest as certain income.

Synthetic ACT/365F interest on100000 at an input rate1/10 for30days rounds to822 minor under half-up. If principal drops to60000 halfway through, calculate two exact segments and round their sum, not two separately rounded daily batches. Re-running the same cumulative coverage yields zero new effect.

Complete with changing rates, partial principal payment, a legitimately chargeable fee, a waived fee, duplicate dispatch and payment allocation across claim types. Deliver the actual collection/AR integration and history, not just an interest formula.


---

<a id="part-15"></a>

# NEXT-63: Self-billed sales and buyer-issued invoice acceptance

Priority: **P2 when applicable**. Lane: **COMMERCE**.

**New deliverable:** Admit buyer-issued sales documents under an explicit self-billing agreement. This is not a supplier purchase or another use of the seller-generated invoice-number counter.

**Existing owner to extend:** Existing source occurrence, sales recognition/credit, party identity and document provenance owners.

**Required contracts:** NEXT-02, NEXT-15, NEXT-51. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** PRY-48; canonical family COM-02/04. Buyer-issued sale acceptance preserves external numbering and seller revenue ownership.

**Atomic result:** Original buyer-issued source accepted/adopted into seller revenue/tax owner.

**Evidence:** R03, X07 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Agreement and issuer identity

Retain `SelfBillingAgreementRevision` identifying the seller, authorized buyer/issuer, covered supplies, agreement dates, acceptance/rejection method and numbering responsibility. The applicable invoicing jurisdiction matters. Current rules distinguish invoice-number and issuer responsibilities; a foreign buyer's self-bill cannot be assumed to follow every domestic rule [X07].

`BuyerIssuedDocument` retains original bytes, issuer namespace/series/number, seller, supply period, amount/tax assertions and source occurrence. It is an incoming source about OUR sale, not a payable. Its economic key includes seller and authorized issuer's identity/namespace. An identical document received twice does not create two receivables.

## Preparation and acceptance

```text
prepareSelfBilledSale(original,agreement):
    require active agreement for this supply and actual issuer
    parse source assertions without inventing seller facts or numbering
    reconcile to retained contract/performance/quantity evidence
    validate mandatory content and tax treatment under the actual jurisdiction
    detect already recognized supply or seller-issued invoice
    if already recognized:
        prepare evidence linkage or a specific replacement/correction, not new revenue
    else:
        compile the existing sales journal/tax/AR semantics
    seal accepted commercial identity and exact source values
```

An app approval is not automatically acceptance under the commercial agreement. Record the applicable outward acceptance/objection event separately where required. No reply within a period is an acceptance condition only under an explicitly qualified agreement, not a universal timer rule.

When the buyer is the agreed numbering owner, OpenERP preserves their invoice identity and allocates only its normal accounting voucher number. It does not issue a second legal invoice under its own ordinary invoice series. A product requirement to produce a seller acknowledgment uses a different document kind, not a replacement invoice number.

## Atomic recognition and payment

The named acceptance transaction posts the native sales journal, records the source document as the issued commercial basis, creates AR, publishes tax facts and binds the supply occurrence once. It rechecks agreement/current customer/supply state, complete amounts and human authorization. Existing invoice, reporting and payment readers consume the same AR owner.

A buyer remittance statement can also contain fees, commissions and withholding. Separate the self-billed gross sale from independently qualified deductions and cash. A net receipt is not net revenue. Unsupported deductions leave an explicit remaining AR or settlement discrepancy rather than reducing sales silently.

## Correction and consumers

A replacement document with the same external number but changed bytes is not silently an update. Retain revisions/conflict evidence and apply the agreement's corrected-document identity. Credit notes reference original source components and use existing tax/AR capacity. If OpenERP has already issued a seller invoice for the supply, the operator must choose the lawful reconciliation relationship; the importer cannot simply discard one financially.

UI distinguishes buyer-issued original, seller approval, outward acknowledgment and actual payment. Statements show the real buyer-issued number. Reports, tax facts and SIE retain original reference and normal accounting voucher identity separately.

## Completion vector

A qualified buyer-issued sale100000+25000 recognizes AR125000 once. A remittance of122000 with an independently evidenced fee3000 settles AR125000 using bank122000 plus fee3000, not revenue122000. The same original delivered by email and import is one sale with two source occurrences.

Finish with original acceptance, duplicate delivery, an already seller-invoiced supply, corrected self-bill and partial remittance. No current self-billing legality is inferred solely from a check box or a printed phrase.


---

<a id="part-16"></a>

# NEXT-64: Invoice payment links with outstanding-bound settlement

Priority: **P1 when applicable**. Lane: **PAYMENTS**.

**New deliverable:** Add a customer payment request tied to an already issued invoice or installment. NEXT-39 reconciles processor money after events exist and does not own the checkout request.

**Existing owner to extend:** Existing invoice residual, external-attempt/credential, processor clearing and customer-credit owners.

**Required contracts:** NEXT-30, NEXT-39. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-59: A link covers a selected installment rather than the entire residual.

**Crosswalk:** PRY-131; canonical family COM-03/05, OPS-03. An invoice payment link precedes settlement; NEXT-39 remains processor-event accounting.

**Atomic result:** No invoice at link creation; processor/cash settlement through original owner.

**Evidence:** R03, R05 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Intent identity and capability

`InvoicePaymentIntent` pins book, legal invoice, selected installment/amount, currency, current residual version, payee merchant account, expiry and allowed partial-payment policy. `ProviderCheckoutBinding` records the exact external object and safe return/display metadata. Link creation is not a new invoice, reservation of revenue or evidence of cash.

A guest browser receives only a bounded token that resolves to this intent. It cannot supply a different merchant account, invoice ID, currency or amount to the server after review. The source of current collectibility is the native invoice residual, not the amount cached in a link.

## Creation and completion

```text
prepareLink(invoice,selection):
    require issued supported invoice, current positive selected residual
    capture authorized merchant/payee configuration and exact amount/currency
    seal request intent and selected external profile

admitCheckout(intent):
    short tx: reauthorize, replay, recheck residual/expiry/cancellation
    create stable provider attempt
    outside tx: create selected checkout object with that identity
    short tx: retain provider correlation and exact amount binding

observeProviderCompletion(event):
    authenticate source and bind merchant/account/environment
    fetch authoritative object using selected provider contract when needed
    require amount/currency/intended invoice relationship matches
    retain payment observation and call existing processor settlement workflow
```

Success navigation in the browser is not a financial result. A provider authorization is not a captured payment, and a captured payment is not a bank payout. NEXT-39 owns processor cash and fees; the link owner never posts a second receipt from its redirect callback.

## Concurrency and residual changes

One use means one supported successful payment occurrence for the intent, not that no duplicate callback can arrive. Provider enforcement must be real and documented. If the provider does not support atomic single-success semantics, record that limit and rely on native payment identity, not a promised guarantee.

Invoice payment, credit or cancellation before checkout dispatch admission can make the old intent stale. If the external payment was already admitted and later succeeds, retain real money honestly: settle only remaining native principal and route surplus through NEXT-30. Do not reject the cash observation and pretend the customer was never charged.

A partial-payment link must specify its minimum/maximum and updated residual policy. New checkouts for the same invoice cannot cumulatively overconsume principal. Provider unknown outcome blocks unsafe replacement where duplicate charging is possible. Closing an old link does not refund a captured payment.

## UI, source and Cash integration

The invoice page presents amount, currency, payee and status before redirect. After return it shows confirmed, pending or unknown based on retained server evidence. Receipts link invoice application and processor source. Book users can expire or replace unexecuted intents with reasons; refunds stay with the actual refund owner.

Cash forecasts read the same remaining invoice/instalment occurrence. Creating a link neither adds a second expected inflow nor changes due dates. Customer statements reflect actual applications and credit balances.

Synthetic invoice125000: link40000, successful captured event40000, native residual85000. A second delivery of the same event changes nothing. If another payment settles125000 before an admitted checkout finally captures40000, the real excess becomes customer credit40000, not an extra sale or a negative residual.

Completion requires one configured provider's authorized sandbox journey, verified callback/recovery, invoice change race and processor reconciliation. Offline intent logic remains useful but is not connected-payment acceptance. No paid card-processing service is made a prerequisite for core self-hosted accounting.


---

<a id="part-17"></a>

# NEXT-65: Scoped customer document and statement portal

Priority: **P1 when applicable**. Lane: **COMMERCE-UX**.

**New deliverable:** Let a customer view exact issued documents and a frozen statement through revocable scoped access. Existing accountant book access and artifact rendering do not provide this external customer workflow.

**Existing owner to extend:** Existing immutable document/statement artifacts, customer identity, access and delivery owners.

**Required contracts:** NEXT-13, NEXT-30. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-59: Portal displays installment-level due amounts and payment promises. NEXT-64: Portal offers a separately authorized payment link.

**Crosswalk:** PRY-53; canonical family COM-05/06, FE, OPS. Customer-facing constrained artifact/current-balance access is not general book access.

**Atomic result:** No financial writes; exact authorized customer artifact/current-data views.

**Evidence:** R03, R05, R06 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Narrow sharing manifest

Create `CustomerShareGrant` with issuer book, reviewed recipient, selected document IDs or customer statement scope, expiry, token hash, revocation version and allowed actions. Store only a hash of a cryptographically random bearer token. Prefer an authenticated recipient binding for sensitive multi-document portals. Link possession never grants general book-list, search, payroll, supplier, reviewer or accounting-write capability.

`StatementShareArtifact` pins the same native invoice/credit/payment residual snapshot and as-of/recorded cutoff used by the statement owner. It contains exact issued identities, terms and payment applications. Future payments change a new statement, not old shared bytes.

## Share and read

```text
prepareCustomerShare(selection,recipient):
    current operator access; prove every selected artifact belongs to this customer scope
    require issued/allowed document kinds, not internal review materials by default
    bind exact artifact hashes, frozen statement basis and expiry
    record approved share manifest and revocation head
    retain outward-delivery intent separately if a message is sent

readSharedArtifact(token,artifactId):
    resolve current grant by token hash in trusted server scope
    verify unexpired/unrevoked grant and optional recipient authentication
    require artifactId in the retained allowed manifest
    return exact stored bytes and minimal metadata
    do not rerender from current logo, address, tax settings or invoice totals
```

A direct object URL must not bypass future revocation. Use a mediated download or a deliberately short-lived signed URL with an explicitly disclosed revocation window. Revocation cannot erase bytes a recipient already legitimately obtained; do not promise it can.

## Current versus historical views

The default portal displays immutable document history and labels each statement's cutoff. A separately requested current outstanding view is generated through the native residual owner under the grant's permitted scope, with current data clearly separated from frozen statement values. It must not silently replace an invoice's printed original amount with the amount still due.

A payment promise is a proposed claim from the customer requiring the existing collection policy and authenticated scope. It is not payment evidence or a ledger mutation. NEXT-64 checkout links are optional actions over the server-selected invoice/instalment intent, not arbitrary amounts accepted from the page.

The customer cannot discover the existence of another party's artifact by guessing IDs. Guest errors should avoid disclosing denied names or numbers. Access audit records describe grant/artifact activity without placing credentials or sensitive document contents in logs.

## Cancellation and delivery evidence

Expiry or revocation changes only sharing eligibility. It does not cancel an invoice, reverse a payment or delete retained accounting evidence. Sending a link records delivered content/destination through the existing transport owner; a successful link page view does not prove the customer accepted the invoice legally.

A corrected document is another legal artifact with explicit relationship and its own inclusion decision. A broad grant that automatically includes future artifacts requires an explicitly reviewed bounded policy; the initial slice uses an exact static manifest.

## Complete workflow

UI supports selection, recipient preview, expiry, revoke, guest statement/document navigation and return to the exact shared list. Use accessible layouts and localized dates/amounts without changing semantic bytes. The guest has no accounting sidebar because no general book scope was granted.

Synthetic original invoice100000, shared statement residual80000 at T1 and later payment30000: original invoice stays100000; T1 statement stays80000; new authorized current view shows50000. Revocation blocks new mediated reads but does not erase the retained artifacts.

Finish with actual guest views/downloads, another-customer refusal, expiry/revocation, a changed current balance and recovery of the original shared bytes after application restart. An unsigned public bucket link is not the packet.


---

<a id="part-18"></a>

# NEXT-66: Purchase commitments and three-way invoice matching

Priority: **P2 when applicable**. Lane: **PROCUREMENT**.

**New deliverable:** Add purchase request, purchase order and receipt/acceptance evidence before supplier invoice recognition. Webshop sales-order intake and supplier invoice drafting are not purchase commitments.

**Existing owner to extend:** Existing supplier/party, source, purchase recognition and approval operations; no new inventory ledger.

**Required contracts:** NEXT-03. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-26: Invoice source matching uses extraction suggestions. NEXT-31: Accepted but unbilled service is recognized through an accrued-cost decision.

**Crosswalk:** Purchase/acceptance bridges in ERPNext review; canonical family COM-02, IMP, Cash readers. Commitment/acceptance records precede AP and do not implement a warehouse or a second accrual owner.

**Atomic result:** No accounting for purchase order alone; recognition/accrual only through existing owner.

**Evidence:** R04, R05 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Bounded procurement model

The first slice covers services and non-stock business purchases. `PurchaseRequestRevision` records business need, requester, supplier options and amount estimate. `PurchaseOrderRevision` freezes approved supplier, currency, line quantities/units, prices, taxes as assertions, delivery terms and commercial conditions. `AcceptanceEvent` records received quantity or accepted service scope with actual evidence. No object independently posts stock or cost.

A purchase order is a commercial commitment, not a supplier payable. Received-but-uninvoiced cost can require an accrual through NEXT-31 under a qualified recognition policy. Reject unsupported inventory accounting rather than create stock journal entries from quantity records.

## Three-way matching

```text
prepareInvoiceMatch(invoice,order,acceptances):
    capture original order revision and every relevant receipt/acceptance revision
    for invoice line:
        map to explicit order line and accepted scope
        require compatible supplier, currency, unit/base quantity and service identity
        compute unbilled accepted quantity/value from prior effective allocations
        compare price, quantity, charges and tax assertions independently
        classify exact_match / permitted_variance / review_needed / unsupported
    require every source line accounted for or deliberately unrelated
    seal matching manifest, differences, evidence and existing recognition plan
```

Tolerance is a procurement decision, not permission to guess tax or silently plug financial balances. An over-delivery or price change requires a reviewed commercial decision with its own limit and reason. Tax deductibility stays with the purchase owner. A zero invoice variance is not evidence that service was actually received.

## Atomic invoice consumption

The actual purchase transaction consumes order/acceptance billing capacities, recognizes the invoice or resolves its existing accrual, creates AP/tax facts and writes one receipt. Recheck all capacities under the shared lock protocol. A second invoice cannot claim an already fully billed acceptance. An unrelated invoice must not be blocked merely because a supplier also has an open order.

Acceptance does not automatically post an expense. Where policy calls for accrued received service, invoke the named accrual owner separately with explicit evidence/approval or combine it within an approved aggregate. At invoicing, release that accrual rather than expense the same accepted service twice.

An order amendment preserves already received/billed quantities and changes only remaining commercial scope. Cancelling an unfilled order releases its remaining commitment but does not reverse a real receipt or cancel an accepted invoice. A supplier credit may reopen billing capacity only when a supported decision actually represents returned/replaced goods/service; a price credit does not recreate receipt quantity automatically.

## Interfaces and controls

Operator UI goes request, approval, order, acceptance, invoice review and receipt. Ordinary agents may gather quotes, suggest mappings and prepare decisions. They cannot authorize procurement spend or confirm actual receipt by inference. Expose all variances before posting, with original order and evidence side by side.

Cash represents a purchase commitment until an actual invoice/payment replaces the same exact occurrence. It cannot sum the order, accrued liability and supplier invoice as three future payments. NEXT-67 adds optional budget consequences, but this packet can be delivered without budget functionality.

Synthetic order10 units at1000: acceptance6 units, invoice4 units consumes4 of the accepted6. Two remain accepted/unbilled and4 remain unreceived. A second invoice3 units fails against the accepted remaining2 unless additional receipt or explicit supported exception is established. No quantity event alone creates inventory value.

Completion requires request-to-invoice, partial receipt/billing, an accrued-service resolution, change/cancel and duplicate supplier invoice cases through native operations. This is optional commercial scope, not a required expansion into a warehouse ERP.


---

<a id="part-19"></a>

# NEXT-67: Commitment-aware budgets with stop and warn decisions

Priority: **P2 when applicable**. Lane: **PROCUREMENT**.

**New deliverable:** Add controlled expense/commitment budgets. Existing reports show actuals and Cash forecasts liquidity; neither is a spend-budget admission rule.

**Existing owner to extend:** Existing dimensions, purchase commitment, approval and report contribution owners.

**Required contracts:** NEXT-13, NEXT-14, NEXT-66. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** Budget Stop/Warn mechanisms in ERPNext review; canonical family COM authorization, report readers. Discretionary commitment control adds no balance ledger and must not prevent recording reality.

**Atomic result:** No journal; commitments and enforcement decision for discretionary authorization.

**Evidence:** R04, R05 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Budget semantics

Retain `BudgetRevision` for book, interval, cost category/dimensions, exact amount, currency and one policy: stop, warn or observe. A budget is a management control, not available bank cash, legal authorization or an expense journal. One native source component belongs to a defined budget classification; reject ambiguous double membership unless an explicit split totals100 percent.

`BudgetExposure` is a derived projection of approved requests, unconsumed orders and recognized actual cost. It references the existing economic component identities and their replacements. No new writable actual-spend ledger is created.

## Exclusive stage calculation

```text
exposure(budget,cutoff):
    actual=sum(qualified posted cost contributions net of owned credits)
    ordered=sum(approved order commitment not yet replaced by actual)
    requested=sum(approved/request-reserved amount not yet replaced by order or actual)
    consumed=actual+ordered+requested
    headroom=budgetAmount-consumed
    return complete source membership and exceptions

checkProposedSpend(proposal,current):
    delta=proposed new exposure - exact replaced earlier-stage exposure
    after=current.consumed+delta
    compare annual AND relevant cumulative-period limits under policy
    stop -> refuse new discretionary authorization when exceeded
    warn -> require reviewed acknowledgment tied to current digest
    observe -> record decision without refusing
```

Do not include the full request after its order exists or the full order after invoicing. Taxes, FX conversion and non-deductible components follow the reviewed budget basis. An allowance credit and a payment are not new cost reductions unless their accounting effects actually change cost. Zero headroom does not authorize accessing private payroll detail to compute a result.

## Where stopping is legitimate

Apply hard stops before committing discretionary procurement or new spend authorization. A company may already have a real obligation from received goods/service. Budget exhaustion must not cause its mandatory bookkeeping to disappear. Capture the source, raise a breach and record the real liability through the authorized accounting path; any exception to a policy gate is explicit, independently approved and evidenced.

A budget override never supplies missing financial approval, invalidates tax evidence or permits an unbalanced journal. The override binds exact proposal, amount, budget versions, resource scope, reason and expiry. A changed budget or competing commitment requires a new currentness check.

## Atomic integration

Request/order approval and its budget reservation happen together in the existing operation transaction. Releasing or replacing a commitment consumes the exact reservation. Use the shared book lock initially to serialize competing budget consumers. A background report cache cannot authorize spending from stale headroom.

Invoice recognition consumes corresponding commitment budget rights while recording actual cost. If actual exceeds the accepted commitment, preserve the actual financial truth and report the difference with required accounting/procurement authority. A returned item, voided order or corrected invoice changes exposure through the relevant original owner, not a manual adjustment to cached headroom.

## UI, reporting and example

Show budget, actual, unconsumed orders, request exposure, remaining headroom and every override. Distinguish budget date from payment due/expected date. Cash may display budget assumptions as a separate scenario but cannot treat an unused budget as a committed cash payment.

Example budget100000, actual30000, open order20000 and independent reserved request10000 gives consumed60000/headroom40000. Turning that request into an order of10000 changes its stage, not total exposure. A new proposal45000 would exceed by5000 under stop. Two concurrent30000 proposals cannot both spend the same40000 headroom.

Complete with those transitions, a legitimate over-budget invoice, reviewed warning/override, cancellation release and a restarted request. A dashboard traffic-light calculation without atomic commitment admission is not the packet.


---

<a id="part-20"></a>

# NEXT-68: Versioned BAS chart adoption and controlled annual updates

Priority: **P0 when applicable**. Lane: **FOUNDATION-REPORTING**.

**New deliverable:** Add reviewed adoption and upgrade of a reference chart without rewriting historical accounts or silently changing tax/report mappings. Existing account CRUD and historical SIE mapping do not deliver annual chart maintenance.

**Existing owner to extend:** Existing native accounts, role bindings, report mapping and qualified-release owners.

**Required contracts:** NEXT-02, NEXT-13, NEXT-49. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-14: Account changes affect active dimension requirements.

**Crosswalk:** PRY-24/30 and chart foundations; canonical family FND-03, IMP, VAT, END. Versioned chart adoption maintains stable native identities and retained historical meaning.

**Atomic result:** No journal for chart metadata; reclassification requires a separate financial plan.

**Evidence:** R03, R04, X09 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Reference versus native identity

`ChartRelease` retains origin, edition, applicable framework, exact account/code/name data, source hashes, notices and usage rights. A freely downloadable chart does not automatically license every associated instruction or commentary. Preserve source/redistribution conditions rather than bundling copied explanatory books. BAS publishes chart changes separately and emphasizes that names alone do not define full account treatment [X09].

`ChartAdoptionPlan` maps immutable reference identities to native account IDs and selected definitions. Native ID, displayed code, name, account kind, tax default and report mapping are different properties. A code rename is not automatically an economic reclassification.

## Compare and prepare

```text
prepareChartUpdate(currentAdoption,newRelease):
    verify source release/version/hash and selected company applicability
    classify changes: added, renamed, retired, split, merged, semantic_changed
    for each native account:
        retain current posted history, active plans, balance and mappings
        suggest exact/name/class mappings as suggestions only
        require explicit review for split, merge or semantic change
    create prospective accounts/mappings and selected effective dates
    enumerate affected role bindings, defaults, report rules and unexecuted plans
    seal entire change manifest with before/after meanings
```

Never derive VAT deductibility from an account code alone. Reference tax/report suggestions are corroboration for the qualified treatment owner. Do not auto-map a balance-sheet account into a sales VAT box because a source spreadsheet used a familiar label.

## Apply without rewriting history

The application transaction rechecks account and rule dependencies, creates/updates prospective definitions, applies reviewed role/report mappings and appends adoption receipt. Posted journal lines retain their original native IDs and captured meaning. Historical report snapshots retain the exact mapping release used when captured.

An old account with a balance may be closed for new posting only when existing supported settlement/correction access and report interpretation remain coherent. Do not delete the account or refuse historical reads. If the business decision requires moving a balance to a new account, prepare a separate explicit financial reclassification with source reasoning, date and approval. No hidden journal is emitted by metadata adoption.

A split requires selected rules for future postings and a separate decision about existing balances. A merge does not erase source provenance. A renamed account does not cause all old vouchers to be rendered with an invented current historical label.

## Migrations and rollback semantics

Reference release import is data under the current qualified-release owner, not SQL stored logic. Structural schema changes are forward migrations. A mistaken adoption is superseded by a reviewed prospective revision; reversing financial reclassifications, if any, is its own existing correction operation. Replaying the exact adoption returns the same result.

Existing SIE accounts and mappings remain first-class. User-defined accounts can stay outside BAS with explicit meaning and mapping, subject to the selected company/report requirements. A missing BAS adoption cannot be resolved by silently renumbering all accounts.

## UI and validation

The preview shows additions, name-only changes, semantic changes, affected balances and report/role effects. Export a human-readable mapping history and exact machine manifest. NEXT-49 receives the impacted identities, not a blanket 'all books changed' event.

Example: native account A code5000 with old expense30000 survives a reference rename. Its journal count and balance remain unchanged. A reviewed future split into A1/A2 requires a new posting rule; no historical30000 is arbitrarily divided. A proposed mapping with active unpaid plans exposes those stale dependencies.

Finish with a release import, reviewed adoption, next-edition change, preserved historical report, compatible ongoing settlement and an explicit optional reclassification. Matching account names alone does not qualify a chart migration.


---

<a id="part-21"></a>

# NEXT-69: Spreadsheet master-data import with staged reconciliation

Priority: **P1 when applicable**. Lane: **INTAKE**.

**New deliverable:** Add typed workbook/CSV onboarding for customers, suppliers and catalog records. NEXT-44 imports accounting history, and NEXT-26 reads supplier documents, not bulk master data.

**Existing owner to extend:** Existing source retention, party/catalog revision and reviewed import-run owners.

**Required contracts:** NEXT-02, NEXT-27. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** PRY-27/28; canonical family IMP, COM master data. Spreadsheet master-data staging differs from NEXT-12/44 financial-history imports.

**Atomic result:** No journal; staged master-data inserts/revisions and per-row receipts.

**Evidence:** R03, R05 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Declare a finite source profile

The first release supports CSV and XLSX through a qualified bounded parser. XLS/ODS are explicit additional formats, not claimed because their extensions resemble spreadsheets. Retain original bytes, workbook metadata, selected sheets/ranges, encoding and parse diagnostics. Never evaluate macros, external links or spreadsheet formulas. Formula cells retain raw formula/cached value provenance and require an explicit accepted-value policy.

`MasterDataImportCapture` pins source occurrence, parser release, chosen sheet/header mapping and every source row identity. `MappingDecision` identifies type and normalization per column. `ImportRowDisposition` is create, revise, link_existing, duplicate_candidate, reject or missing_fact. An import job does not silently delete records absent from a later workbook.

## Deterministic interpretation

```text
prepareMasterImport(original):
    parse with cell/sheet/row/byte and archive-expansion bounds
    list candidate tables and headers; preserve ambiguous alternatives
    user selects exact table and column mapping
    for row:
        retain raw typed cell and source coordinate
        normalize using explicit field grammar, not formatted display guesses
        preserve identifier leading zeros and reject lost precision
        resolve existing records by stable source mapping or reviewed identity
        produce proposed typed revision plus field conflicts and missing facts
    freeze complete row count, continuation and decision inventory
```

Numeric cells are not proof of a valid organization number, bank account or postal code. Do not infer business-versus-person or EU-tax status from a guessed pattern. Date cells require a declared workbook epoch and field semantics; a date-only value must not shift timezone. Monetary prices require exact scale/currency and no IEEE-754 round-trip through application amount types.

Supplier bank details enter the existing payee-verification workflow as unverified source assertions. Import cannot activate a payment beneficiary. Catalog tax categories are suggestions until reviewed under their actual treatment profile. Unknown values are not empty strings silently overwriting verified data.

## Commit and recovery

```text
commitReviewedRows(capture,selection):
    require exact reviewed mapping, row identities and current target revisions
    apply one bounded chunk through existing party/catalog internal writers
    write row receipts/checkpoint in same transaction
    replay chunk from original identity after response loss
    record each deliberate rejection and retain source rows
```

Partial success is explicit at chunk boundaries, not catch-and-ignore inside a failed SQL transaction. A row conflict can pause the run without deleting prior successful revisions. The operator can issue a new reviewed resolution for conflicted rows. Current privacy and book scope apply on resume and download.

This packet imports master data only. Opening balances, unpaid invoices, payroll history and journal entries require their existing financial migration owners and independent controls. Selecting a supplier sheet does not grant permission to synthesize payables from a balance column.

## User interface and proof

Provide sheet/table selection, type-aware mapping, sample and whole-dataset statistics, side-by-side field conflicts and explicit complete-versus-partial status. A preview of20 rows is not proof that all2000 rows are clean. CSV export of diagnostics uses safe cells so source formula text is not executed when opened.

Example: source row keys001 and1 remain distinct unless a reviewed source identity rule establishes equality. A supplier whose verified bank details differ from a spreadsheet yields a proposed unverified revision, not an active payee change. A second delivery of the same source/capture recovers row receipts without duplicating parties.

Completion includes actual parser output, two sheets with ambiguous headers, numeric identifier hazards, target revision changes, resumable chunks and an independently reconciled imported record count. An auto-selected 'best sheet' with no review is not the workflow.


---

<a id="part-22"></a>

# NEXT-70: Structured bank-statement ingestion with exact entry lineage

Priority: **P0 when applicable**. Lane: **BANKING**.

**New deliverable:** Add bank-file decoding and controlled admission, initially one qualified camt.053 profile. Plaid windows and provider-revision semantics do not parse a bank statement file.

**Existing owner to extend:** Existing source intake, statement/observation identity, bank-source revision and reconciliation owners.

**Required contracts:** NEXT-09, NEXT-10. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-40: The statement belongs to a native foreign-currency cash account.

**Crosswalk:** PRY-08 and bank-format requirements; canonical family IMP-01/03/04. Structured bank-file decoding reuses NEXT-10 admission instead of duplicating Plaid windows.

**Atomic result:** No journal; bank-source statement/observation admission.

**Evidence:** R03, R05, X08 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Selected profile and source model

`BankStatementFormatRelease` pins actual bank, message/schema version, currency/date/entry rules and complete supported record families. Initial camt.053 support is not automatic camt.052/camt.054, MT940 or every bank's XML. File-based import remains usable without a connected bank feed. Acquire the selected bank's actual message guide and independent sample before claiming compatibility [X08].

Retain whole file hash/occurrence, message ID, account identifier, statement ID, period, opening/closing balance types and complete entry/detail positions. Provider entry IDs and detail IDs are source identities only under the selected provider's documented uniqueness. Missing references remain explicit, not a hash of amount/date presented as an authoritative bank ID.

## Decode amounts once

```text
parseStatement(bytes,profile):
    strict bounded XML parse with external entities/network resolution disabled
    verify namespace/schema and exact bank/profile selectors
    select the qualified booked statement balance types
    for entry:
        retain entry amount/currency, direction, status, reversal indicator and dates
        parse nested details without counting entry PLUS details as separate money
        if detail sums reconcile under profile:
            emit supported detail observations with link to parent entry
        else:
            retain entry-level money and unresolved-detail diagnostic
        apply direction/reversal semantics exactly once under the format rule
    prove opening + qualified movements == closing per currency and interval
    retain unknown/nonbooked/balance entries separately
```

Available, booked, credit-limit and forward-available balances are not interchangeable. Pending entries may be retained without being admitted as final booked observations. A returned payment can be a real opposite cash movement rather than deletion of the original. Dates keep bank booking and value meanings separate.

## Admission and overlap

Prepare a complete immutable import plan with source controls and duplicates/overlap candidates against existing file and feed observations. Actual matching uses current bank-source owner identities, including same-event adoption where established. Identical amounts are not enough to deduplicate. Changed bytes under an identical provider statement identity are a revision/conflict, not silent replacement.

Admit observations in bounded complete groups through NEXT-10's application port. It creates neither journal nor automatic invoice settlement. Store source/provenance links, published version and command receipt together. Correction of an already reviewed/matched source raises the existing impact lifecycle; it does not automatically reverse accounting.

For long statements, fixed captured membership and final control totals govern paging. Do not label the first successful chunk as a complete reconciled period. Independent file controls cannot be adjusted to make native loaded rows agree.

## Views and completion

Show source file, exact message/profile, account, balance types, entry/detail tree, all exceptions and coverage. A rejected row remains visible with its amount. The bookkeeping work queue may subsequently propose matching or recognition, but file import itself does not decide tax treatment.

Synthetic statement opening100000, entry debit30000 with two details10000/20000 and credit5000 yields closing75000. Count the debit once, not60000. A second file containing the same confirmed entries links existing occurrences. An unqualified reversal flag is a diagnostic, not an extra negation guessed by the parser.

Complete with an actual selected-bank file, independent amount/control check, duplicate/overlapping file+feed delivery, detail mismatch, pending-to-booked event and corrected statement. Native foreign account support depends on NEXT-40 only where applicable; SEK-only import does not wait for foreign-cash implementation.


---

<a id="part-23"></a>

# NEXT-71: Bank-qualified payment exports and status reconciliation

Priority: **P0 when applicable**. Lane: **PAYMENTS**.

**New deliverable:** Qualify a selected bank payment-file profile and its status-to-settlement journey. Reuse the existing synthetic pain.001 exporter, instruction reservations and recovery owner instead of creating another payment system.

**Existing owner to extend:** Existing supplier-payment batch/export, payee verification, instruction resolution and bank-settlement application owners.

**Required contracts:** NEXT-08, NEXT-10, NEXT-70. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-17: The chosen bank profile supports foreign-currency obligation settlement. NEXT-59: Transfers select invoice installments.

**Crosswalk:** Bank payment-format and recovery requirements; canonical family COM-03, OPS-03. Qualify the actual bank format/status channel around existing export and NEXT-08 capacities.

**Atomic result:** No cash posting on export/status; actual payment uses existing allocation owner.

**Evidence:** R03, R05, R07, X08 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Profile and identity

`BankPaymentProfile` pins bank/product, exact message guide and XSD versions, supported currencies/payment types, execution-calendar rules, debtor/beneficiary fields, address requirements and authentic status meanings. The inspected exporter produces a bounded pain.001.001.03 document [R07]. That proves an existing serialization owner, not acceptance by any bank.

Select one real bank profile first. SEB publishes current migration guides and payment-infrastructure changes, including address-format transition material [X08]. Acquire its actual selected schema/guide bytes and a bank-approved test path. Do not assume the generic ISO schema captures every bank restriction or that an old message version is the correct version for all execution dates.

Retain `PaymentOccurrence`, `ExportManifest`, `TransferIdentity` and `StatusObservation` with the existing instruction owner. An end-to-end identity belongs to one payment occurrence, not only an invoice. Two partial payments of one invoice require distinct identities. Retrying the same exported instruction preserves its original identity. A truncated invoice ID alone is not a sufficient unique payment key.

## Preparation and rendering

```text
prepareBankExport(selection,debtor,executionDate,profile):
    capture exact remaining invoice/instalment capacities and active reservations
    validate current independently reviewed beneficiary details
    validate bank calendar, profile date and actual external mandate
    allocate stable message/group/transfer identifiers with collision refusal
    build complete semantic transfer manifest with exact currency amounts
    render outside financial locks and validate XSD plus bank-specific rules
    independently compare every XML transfer to the approved semantic manifest
    seal exact bytes hash, beneficiary revisions, totals and source relationships
```

The existing approval/reservation owner commits the reviewed manifest and capacity reservations together. A failed render does not consume financial principal. Another key cannot create another live reservation for the same capacity. No supplier expense, VAT or bank cash movement is posted when the export is generated.

## Status and settlement

Dispatch uses the existing outbox/attempt lifecycle. File download for manual bank upload is an observed handoff, not a bank submission receipt. For a connected bank channel, admit one exact attempt under current authority, call it outside the transaction and retain the returned correlation. Unknown outcomes cannot be retried with new message IDs merely to obtain a response.

```text
observeBankStatus(raw,statusProfile):
    authenticate and retain original status document
    match message/group/transfer references to the exact export
    reject unknown or conflicting identities into an investigation case
    record per-transfer observed state using the selected provider semantics
    do not upgrade every transfer from one group-level acknowledgment
    accepted or processing means instruction status, not booked cash

recordObservedPayment(bankEvent,instruction):
    require exact supported final payment evidence and current allocation capacities
    post/adopt bank-versus-payable settlement through the existing owner
    consume instruction and invoice capacity in that same transaction
    retain real bank source relationship and receipt
```

A pain.002 partial acceptance does not release every rejected or unresolved transfer by inference. NEXT-08 evaluates the actual proof that a particular instruction cannot execute. Cancellation requests and expired queue leases alone do not establish that. Returns after actual payment are separate cash events with their correct reopened obligation or refund consequences, not deletion of the original payment.

## Proof and visible workflow

Show prepared, approved, exported, handoff, accepted, processing, booked, returned and unknown states only where the selected profile supports the distinction. Display status evidence and unresolved transfers beside the exact exported bytes. Customer/payroll batch use is a later explicit profile, not a hidden widening of this supplier profile.

For two instructions40000 and60000, a status accepting40000 and rejecting60000 cannot mark the invoice paid100000. Actual booked40000 leaves60000 principal, with reservation release requiring the rejected instruction's own proof. A replayed source payment produces the original settlement receipt. A new partial payment uses a new payment occurrence but cannot exceed the current60000 residual.

Completion requires the actual selected bank format and an authorized import/status/settlement exercise. Local XML validation and download remain useful independently, but must retain their lower evidence state.


---

<a id="part-24"></a>

# NEXT-72: VAT declaration submission and authoritative return history

Priority: **P0 when applicable**. Lane: **TAX-DELIVERY**.

**New deliverable:** Add the filing lifecycle after the existing VAT calculation: exact submission authority, external period/declaration state, safe replacement and authentic outcomes. NEXT-37 remains the separate assessment owner.

**Existing owner to extend:** Existing VAT return snapshots, qualified releases, external attempts, declaration history and obligation fulfillment.

**Required contracts:** NEXT-04, NEXT-49. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-37: Link an actual later VAT assessment; submission itself has no assessment journal.

**Crosswalk:** PRY-57; canonical family VAT-02/04, END-07, OPS-03. Declaration dispatch is distinct from NEXT-04 calculations and NEXT-37 assessment.

**Atomic result:** No journal; declaration attempts and authentic outcomes only.

**Evidence:** R03, R05, X01, X10 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Separate calculation from submission

`VatSubmissionIntent` references the immutable calculated return, entity, exact reporting interval, complete box map, filing-unit semantics, rule release, original or replacement purpose and expected external declaration state. It does not recalculate tax or mark an obligation assessed. `SubmissionAttempt` and append-only `AuthorityObservation` belong to the existing external-outcome system.

The official API inventory and representative guidance identify a Momsdeklaration service and its permission family [X10]. This is evidence that a specific integration can be investigated, not a fetched machine contract. Pin actual current API schemas, credential arrangements, signing/submission steps, idempotency and status meanings before activating a connected profile. A company administrator inside OpenERP is not automatically its authorized tax representative.

## Prepare and authorize

```text
prepareVatSubmission(returnId,selectedChannel):
    load saved return and its explicit supported/profile/currentness state
    require complete applicable source coverage and reviewed period identity
    serialize filing integers from saved reported values, never from today's GL
    distinguish required zero boxes from omitted nonapplicable boxes
    if selected channel can read current authority state:
        capture actual entity/period declaration revision and pending submissions
        diagnose competing submission or inconsistent period before preparing replacement
    seal payload, destination, exact replacement relation and external-state witness

approveVatSubmission(intent):
    current human authority plus actual selected representative/mandate check
    bind exact payload, period, channel and expiry
    retain approval separately from financial-posting approvals
```

A replacement is prepared against the known original authority declaration, not merely the app's newest snapshot. Another accountant or system can submit in parallel. If the service lacks conditional writes, disclose that race and require read-back reconciliation rather than promise compare-and-swap protection it does not provide.

## Dispatch, unknown outcome and later change

```text
admitVatDispatch(intent):
    short tx: replay exact command; recheck approval and relevant local/external witnesses
    create one durable attempt and exact request identity
    outside tx: perform only the selected supported provider action
    short tx: retain authentic raw response and normalized observation

recoverVatAttempt(attempt):
    use retained correlation and documented read-back/idempotency contract
    if outcome cannot be established: keep unknown and block duplicate replacement
    never treat timeout or a successful upload as signed submission
```

Local preparation, service validation, transfer, signed submission, accepted declaration record, assessment and payment remain separate facts. A new bank transfer does not fulfill submission. Conversely, receiving a submission receipt posts no bank payment or tax-account assessment. NEXT-37 consumes actual assessment events later through its own operation.

Ledger changes after a committed submission do not make its historical receipt disappear. They create a new impact review and, if required by the qualified treatment, an explicitly linked amended return/submission. Original bytes and authority references remain accessible. Same-key recovery returns the original result even after a new calculation exists.

## UI, manual channel and completion

Provide a comparison of saved boxes, prior external declaration, proposed change and exact authorization. Current external access can fail without preventing an authorized read of already retained receipts. A manual official-channel handoff can retain the exact payload and independently reviewed outcome evidence; label that evidence honestly instead of claiming the connector fetched it.

An obligation advances only through NEXT-49's typed same-scope outcome predicate. An API success that merely creates a draft cannot satisfy a submitted/accepted requirement. The app must not invent an unavailable automatic signing mechanism to make the workflow appear complete.

Required cases include original submission, exact retry after response loss, external declaration changed before replacement, wrong entity/period receipt, revoked representative, prepared zero return, rejected boxes and later amended return with old artifacts intact. The connected packet is complete only when its selected channel has authentic observed outcomes; no current API credential or tax position is granted by this specification.


---

<a id="part-25"></a>

# NEXT-73: AGI submission and stable individual correction outcomes

Priority: **P1 when applicable**. Lane: **PAYROLL-DELIVERY**.

**New deliverable:** Add actual employer-declaration delivery and period/item outcome tracking after the existing AGI producer. Do not recalculate payroll, repeat paid-payroll correction or equate file preparation with signing.

**Existing owner to extend:** Existing payroll declaration/pay-run owners, private payroll admission, external delivery and fulfillment.

**Required contracts:** NEXT-21, NEXT-49. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-36: The selected submission changes previously paid/reportable compensation. NEXT-47: The actual selected protocol uses an independently qualified signature adapter; do not substitute generic signing.

**Crosswalk:** PAY-04 external-outcome requirements; canonical family PAY-04, END-07, OPS-03. AGI submission consumes NEXT-21/36 output and does not replace payroll accounting.

**Atomic result:** No payroll/cash mutation; private declaration-item submissions and outcomes.

**Evidence:** R02, R08, R09, X10, X14 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Exact private declaration manifest

`AgiSubmissionManifest` pins employer, actual reporting period, declaration revision, employer totals, complete selected individual-item identities, exact artifact hash, qualification release and original/replacement purpose. Each item preserves the existing employer/period/payee/specification identity and the prior filed item it replaces. A new request ID is not a new employee specification.

Read, list, replay, status and export all require current private payroll permission before returning sensitive content. Jobs carry references rather than names, salaries or credentials. Aggregate operational dashboards must not expose private employee rows through error details or delta history.

The official service/permission guidance distinguishes preparatory registration rights from rights to sign and submit [X10/X14]. Implement the actual selected permission ceremony. General app membership, a payroll review approval or an API read permission cannot substitute for the external right to submit.

## Build from the existing declaration owner

```text
prepareAgiSubmission(declarationRevision,channel):
    current private scope; capture saved paid/reporting facts and original filed history
    load exact existing AGI artifact and its independent validation result
    require employer totals and individual membership reconcile under the release
    for each corrected item:
        retain original specification identity
        verify the intended replacement or deletion behavior in this exact API/file profile
        preserve every unaffected external item unless the operation explicitly replaces it
    compare current authority period/item state where the service supports it
    seal payload, affected membership, expected external state and signing purpose
```

The original earnings period, adjustment accounting date and declaration reporting period remain independent under ADR0014. An August entitlement corrected in an open September period does not automatically belong in either month's AGI merely from those dates. PAY-04's qualified reporting determination remains authoritative.

Some reported auxiliary facts can have a different correction protocol from financial individual items. The current official guidance, for example, distinguishes absence information handling [X14]. Preserve unsupported correction branches explicitly rather than promise that one replacement action fixes every field.

## Delivery and outcomes

Use the existing admitted external-attempt transaction, outside-transaction call and authentic observation append. Normalize only documented service states. A technical file acceptance, draft registered in the period and signed employer declaration are different outcomes. If the selected channel supports partial item validation, retain per-item results and aggregate completeness; one successful item cannot mark the whole manifest accepted.

```text
reconcileAgiOutcome(attempt,rawOutcome):
    verify service origin, environment, employer and reporting interval
    map returned item identities to the exact submitted membership
    refuse unknown/conflicting item mapping into an investigation case
    record complete/partial/pending/rejected meanings according to actual service contract
    append outcome observation; update fulfillment only for its required predicate
    do not change wage postings, withholding, actual cash or tax-account balance
```

For response loss, recover the same attempt through provider correlation/read-back. If no safe mechanism exists, keep the outcome unknown. Do not append another employee item by changing its specification number. A later original-item correction gets a new declaration revision with the same stable item identity and new explicit authorization.

## Completion and reader behavior

The payroll UI shows paid-source basis, saved declaration values, original/replacement links, individual diagnostics and the next real human action. Retained old declarations remain readable even if current source facts change. Where external signing must happen in Skatteverket's service, link that action without pretending OpenERP signed on the person's behalf.

Prove that correcting one of ten employees does not delete or duplicate the other nine, that an unchanged-key retry adds no item, that private-grant revocation stops historical/replay reads and that submission changes no payroll journal. Exercise the selected schema/service version with authorized test identities. Exact statutory tables and credentials remain input dependencies, not a new payroll calculator inside this packet.


---

<a id="part-26"></a>

# NEXT-74: INK2 filing, signature handoff and assessment attribution

Priority: **P1 when applicable**. Lane: **TAX-DELIVERY**.

**New deliverable:** Complete the external corporate-income-tax filing journey after the existing tax bridge and INK2/SRU artifact. Keep signature, transfer, declaration record and final assessment separate.

**Existing owner to extend:** Existing corporate-tax calculation/declaration, financial closing, retained artifacts, tax-account and external-outcome owners.

**Required contracts:** NEXT-22, NEXT-23, NEXT-49. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** INK2/SRU external-outcome requirements; canonical family END-06/07, OPS-03. Tax filing/signature follows NEXT-22 fields and is not NEXT-48 annual-report registration.

**Atomic result:** No second income-tax expense; tax submission/signature/assessment references.

**Evidence:** R03, R05, X10, X11 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Final filing package

`CorporateFilingManifest` pins legal entity, actual fiscal interval, qualified form edition, final tax calculation, reconciled accounting basis, main form and required annex set, exact filenames/bytes/hashes and selected channel. Validate the fiscal year from its retained dates, not a calendar-year shortcut. Each annex names the same required entity/year and its original source model.

NEXT-22 owns fields and SRU generation. This packet consumes those artifacts rather than copying tax formulas or creating a second form renderer. Preparation can inspect a pre-close draft, but approval for final filing requires the selected final financial/tax basis or a specifically qualified exception. This creates no cycle: the existing pre-close tax calculation does not depend on an external filing.

The official file-transfer service describes a later signing step through Mina sidor [X11]. Official information also identifies an Inkomstdeklaration2-4 API [X10]. Select one actual channel and pin its machine/identity contract; an API read permission is not permission to submit. Do not guess that every field/annex accepted by the file service is supported identically by an API version.

## Preparation and signature authority

```text
prepareCorporateFiling(declarationRevision,channel):
    capture exact fiscal/entity identity and complete required artifacts
    verify main-form/annex totals and declared qualification checks
    compare saved final tax target with the owned current effective tax effects
    require no unresolved material filing blockers in the selected scope
    inspect existing authority declaration/transfer state where supported
    seal original/replacement purpose, artifact manifest and external-state witness

approveCorporateFiling(intent):
    verify current app operator and actual permitted external representative
    bind exact manifest and intended signature/submission action
    do not treat annual-report signing as income-tax declaration signing
```

A corporate return and a Bolagsverket annual report may share financial inputs but remain different submissions with different purposes. NEXT-48 cannot satisfy this tax obligation merely because its report was registered.

## Transfer, signing and receipt

Dispatch follows the shared attempt/recovery model. For manual file handoff retain exact bytes and user action without claiming transfer was observed. For authenticated transfer retain the genuine service receipt and its correspondence to the submitted files. If transfer only stages the declaration for later signature, the current state is `awaiting_external_signature`, not submitted.

```text
advanceCorporateOutcome(attempt,observation):
    verify source, environment, legal entity, fiscal interval and payload relationship
    append only the normalized state justified by the actual service response
    if signing required and unobserved: retain pending human action
    if final declaration outcome evidenced: link it to the specific obligation revision
    if authority assessment later arrives:
        retain assessment as a separate owned event and reconcile to declared target
        route any accounting/tax-account effect to its existing owner
```

Submitting a return does not create another income-tax expense or mark tax paid. Expected tax, declared tax, assessed tax and cash financing remain distinct. A later assessment difference needs its own qualified interpretation; it is not automatically a rounding adjustment to the already filed form.

## Corrections and acceptance

A rejected transfer can be repaired by a new artifact revision only where its actual content changes. Preserve the rejected original. An unknown transfer cannot safely be retried with new identities without documented recovery. A correction after a signed submission follows the supported amended-declaration procedure and its own approval, not replacement of old saved bytes.

The UI shows package completeness, transfer receipt, signature stage, accepted declaration and later assessment separately. A test-environment receipt never fulfills a production obligation. Reviewed manual evidence remains labelled as such.

Completion includes main form plus required annexes, different-than-calendar fiscal interval, wrong-year refusal, transfer-before-signature distinction, unknown-response recovery, competing outside submission and accepted declaration with no duplicate tax journal. It does not require or authorize a real company filing during implementation.


---

<a id="part-27"></a>

# NEXT-75: Accounting-method change with conserved recognition coverage

Priority: **P2 when applicable**. Lane: **TAX-FOUNDATION**.

**New deliverable:** Add a deliberate transition between qualified accounting/VAT methods. NEXT-38 implements cash-method events; it does not authorize changing method or prevent old invoices being reinterpreted by a new global flag.

**Existing owner to extend:** Existing company-profile activation, invoice recognition coverage, fiscal closing and statutory-method evidence owners.

**Required contracts:** NEXT-02, NEXT-03, NEXT-04, NEXT-23, NEXT-38. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-12: Imported open items require historical recognition evidence.

**Crosswalk:** Accounting-method transition extension; canonical family FND-03, COM-02, VAT, END. A reviewed method cutover is distinct from NEXT-38 ordinary cash-method events.

**Atomic result:** Complete qualified transition journal/coverage plus dated profile activation.

**Evidence:** R03, R05, X12 in [SOURCES.md](SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](00-COMMON.md) and [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Three different changes

Distinguish correcting a wrongly recorded registration fact, a legally effective accounting/VAT method change and a software migration between systems using the same method. They require different records. This packet covers the method change only. It must not be used to overwrite old company facts or bypass NEXT-12/25's real-data migration controls.

Retain `MethodTransitionDecision` with old/new qualified methods, entity, actual effective date, authority notification/decision evidence where required, selected financial and reporting policies and complete affected population. Swedish guidance distinguishes the procedures and conditions for the two directions [X12]. No revenue threshold, effective date or approval is inferred here.

## Capture disjoint history

```text
captureMethodTransition(decision):
    establish current official-method witness and permitted target/effective date
    capture complete original invoice-line populations across the boundary
    for each component retain:
        already recognized amount and its tax attribution
        paid but unrecognized anomalies
        unrecognized commercial outstanding
        recognized unpaid positions, credits, advances and unsettled instructions
    require source coverage and all financial/control relationships established
    freeze current population/revisions and known unsupported families
```

An already recognized year-end portion is not unrecognized merely because no cash was paid. An advance's tax history is separate from final invoice recognition. Unknown imported coverage blocks the transition rather than being assumed entirely unpaid or entirely recognized.

## Cash to accrual

For the first supported transition profile, compile the still-unrecognized eligible portion at the policy's permitted transition dates. Prior paid and previously year-end-recognized portions stay unchanged.

```text
compileCashToAccrual(component,transitionPolicy):
    U = qualified unrecognized remaining gross coverage
    if U==0: retain no-effect membership
    else derive source net/tax/deduction under original supported treatment
    purchase: debit cost/asset and eligible input tax; credit payable U
    sale: debit receivable U; credit revenue/deferred revenue and output tax
    append recognition slices with trigger=method_transition
    bind qualified reporting attribution independently from journal date
```

Later payment consumes the resulting recognized open position without another expense/revenue or VAT fact. A transition between periods can have different accounting and VAT timing under the selected policy; do not force them equal merely because one journal is created.

## Accrual to cash

Do not reverse all unpaid invoices or prior VAT automatically. Carry already recognized positions into an explicitly documented transition cohort and settle them once under their original recognition basis. Newly eligible supplies follow the target profile. Any legally required tax adjustment is separately compiled from its qualified rule with original lineage, never implied by flipping a Boolean.

## Activate atomically and preserve history

For a bounded supported book, one reviewed transition aggregate commits required journals, new recognition slices/open positions, cohort membership and the new dated method activation through internal transaction-passing owner functions. Recheck every population and competing payment under the book lock. If no internal activation port exists, obtain that port; two public commits are not an atomic transition.

A wider population needs an explicitly designed fenced cutover with staging and final activation, not an automatic half-switched book. The initial bounded implementation may refuse that scale. A failed transaction leaves the old method active. Historical invoice/report readers use their retained method/release, not today's active method. Existing applied migrations and historical records are not rewritten.

Example: gross125000/net100000/tax25000, paid coverage50000 recognized before transition, remaining75000 unrecognized. The selected cash-to-accrual bridge recognizes net60000/tax15000 once. Later75000 payment posts only settlement. If that75000 had already been recognized at year-end, transition financial delta is zero.

Completion requires both directional policies or an explicitly advertised one-direction release, actual-company applicability evidence before use, original/target control reconciliation, stale-population refusal, late source impact and same-key recovery. Accounting-method change remains optional breadth, not a prerequisite to a stable company's daily bookkeeping.


---

<a id="part-28"></a>

# Integration and delivery map

This is a new-capability wave, NEXT-51 through NEXT-75. The previous fifty work IDs retain their unfinished application, correction and proof obligations. New IDs below are not migration numbers and are not added to the repository's independent 53-core-packet denominator.

The source basis is `116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5`. The current progress record reports many pure leaves and selected integrated/observed journeys. A proposal in this dossier does not certify those dependencies. Reconcile exact current exports, schema versions and dirty ownership before assignment.

## What “new” means here

Each packet states an economic or external workflow absent from the prior NEXT scope, or a named parity requirement now resolved into a concrete delivery unit. This is not an exhaustive current-source absence audit. Some generic scaffolding may already exist. Reuse it. A PRY finding supplies requirements; it does not become a competing implementation owner.

Do not repeat PDF extraction adapter work, credit rendering, SIE dimension repair, payroll run integration, Cash forecasting or the original VAT/FX/impairment work. Those stay with their existing owners. New source facts flow into their released APIs.

## Required versus conditional

Required contracts below are the minimum interfaces needed for the packet's complete selected workflow. Conditional integrations apply only to their named cases. An empty accounting profile is not proof of inapplicability, but a genuinely services-only business need not wait for goods code.

| New packet | Required NEXT contracts | Conditional integration |
|---|---|---|
| [NEXT-51](packets/NEXT-51.md) | NEXT-02, NEXT-04, NEXT-15 | No additional NEXT-specific edge |
| [NEXT-52](packets/NEXT-52.md) | NEXT-02, NEXT-04, NEXT-15, NEXT-51 | NEXT-17: The selected sale is in foreign currency and needs the existing monetary-item representation. |
| [NEXT-53](packets/NEXT-53.md) | NEXT-02, NEXT-03, NEXT-04, NEXT-15, NEXT-51 | No additional NEXT-specific edge |
| [NEXT-54](packets/NEXT-54.md) | NEXT-02, NEXT-03, NEXT-04 | No additional NEXT-specific edge |
| [NEXT-55](packets/NEXT-55.md) | NEXT-04, NEXT-49 | NEXT-52: The selected statement includes general-rule cross-border services. NEXT-53: The selected statement includes qualifying intra-EU goods. |
| [NEXT-56](packets/NEXT-56.md) | NEXT-02, NEXT-04, NEXT-30, NEXT-51 | No additional NEXT-specific edge |
| [NEXT-57](packets/NEXT-57.md) | NEXT-02, NEXT-03, NEXT-07 | No additional NEXT-specific edge |
| [NEXT-58](packets/NEXT-58.md) | NEXT-02, NEXT-15 | NEXT-29: The originating invoice is a recurring occurrence. NEXT-31: The shared schedule contract is being extended together with expense deferral; no duplicate schedule owner. |
| [NEXT-59](packets/NEXT-59.md) | NEXT-15, NEXT-30 | NEXT-50: Include installment and promise summaries in agent context. |
| [NEXT-60](packets/NEXT-60.md) | NEXT-07, NEXT-15, NEXT-30 | NEXT-17: The settlement includes foreign-currency principal or a separately evidenced FX difference. |
| [NEXT-61](packets/NEXT-61.md) | NEXT-04, NEXT-15, NEXT-30 | No additional NEXT-specific edge |
| [NEXT-62](packets/NEXT-62.md) | NEXT-28, NEXT-30, NEXT-59 | No additional NEXT-specific edge |
| [NEXT-63](packets/NEXT-63.md) | NEXT-02, NEXT-15, NEXT-51 | No additional NEXT-specific edge |
| [NEXT-64](packets/NEXT-64.md) | NEXT-30, NEXT-39 | NEXT-59: A link covers a selected installment rather than the entire residual. |
| [NEXT-65](packets/NEXT-65.md) | NEXT-13, NEXT-30 | NEXT-59: Portal displays installment-level due amounts and payment promises. NEXT-64: Portal offers a separately authorized payment link. |
| [NEXT-66](packets/NEXT-66.md) | NEXT-03 | NEXT-26: Invoice source matching uses extraction suggestions. NEXT-31: Accepted but unbilled service is recognized through an accrued-cost decision. |
| [NEXT-67](packets/NEXT-67.md) | NEXT-13, NEXT-14, NEXT-66 | No additional NEXT-specific edge |
| [NEXT-68](packets/NEXT-68.md) | NEXT-02, NEXT-13, NEXT-49 | NEXT-14: Account changes affect active dimension requirements. |
| [NEXT-69](packets/NEXT-69.md) | NEXT-02, NEXT-27 | No additional NEXT-specific edge |
| [NEXT-70](packets/NEXT-70.md) | NEXT-09, NEXT-10 | NEXT-40: The statement belongs to a native foreign-currency cash account. |
| [NEXT-71](packets/NEXT-71.md) | NEXT-08, NEXT-10, NEXT-70 | NEXT-17: The chosen bank profile supports foreign-currency obligation settlement. NEXT-59: Transfers select invoice installments. |
| [NEXT-72](packets/NEXT-72.md) | NEXT-04, NEXT-49 | NEXT-37: Link an actual later VAT assessment; submission itself has no assessment journal. |
| [NEXT-73](packets/NEXT-73.md) | NEXT-21, NEXT-49 | NEXT-36: The selected submission changes previously paid/reportable compensation. NEXT-47: The actual selected protocol uses an independently qualified signature adapter; do not substitute generic signing. |
| [NEXT-74](packets/NEXT-74.md) | NEXT-22, NEXT-23, NEXT-49 | No additional NEXT-specific edge |
| [NEXT-75](packets/NEXT-75.md) | NEXT-02, NEXT-03, NEXT-04, NEXT-23, NEXT-38 | NEXT-12: Imported open items require historical recognition evidence. |

## Existing owner crosswalk

| New packet | Source requirement | Canonical owner | Delta |
|---|---|---|---|
| NEXT-51 | PRY-47, PRY-51, PRY-55 | COM-02/04, VAT-02 | Domestic standard-rate owner gains new mixed/reduced/exempt profiles, not a second issue engine. |
| NEXT-52 | PRY-47, PRY-11 | COM-02/04, VAT-02 | Sale-side general-rule B2B services are distinct from NEXT-05 purchase-side services. |
| NEXT-53 | PRY-47, PRY-55/56 | COM-02/04, VAT-02 | Goods movement/acquisition/supply treatment is not inferred from the service profile. |
| NEXT-54 | PRY-55/56 | COM-02, VAT-02 | Customs import decisions and landed-cost attribution extend purchase recognition, not inventory custody. |
| NEXT-55 | PRY-47/55 and EU reporting requirements | VAT, END-06/07 | EU statement artifacts and correction history are not the ordinary VAT return. |
| NEXT-56 | Advance concepts in ERPNext review | COM-02/03/04, VAT | Customer advance tax timing differs from NEXT-30 refundable overpayments. |
| NEXT-57 | Advance concepts in ERPNext review | COM-02/03/04, VAT | Supplier cash prepayment is not NEXT-31 expense deferral or a credit of an unrecognized purchase. |
| NEXT-58 | PRY-52 | COM-02/04, AST | Revenue liability/service recognition differs from NEXT-31 prepaid costs and NEXT-29 billing dates. |
| NEXT-59 | Payment-term schedules in ERPNext review | COM-03/06, Cash readers | Legal installment residuals and payment promises extend one native obligation, not recurring billing. |
| NEXT-60 | PRY-34, PRY-51 | COM-03/04, IMP | Explicit price/fee/rounding difference decisions are not a generic tolerance plug or a new FX owner. |
| NEXT-61 | Receivable lifecycle extension | COM-04/06, VAT | Accounting allowance and confirmed tax loss are not customer credits or disputes alone. |
| NEXT-62 | PRY-49 | COM-04/05/06 | Creates qualified monetary interest/fee claims; NEXT-28 only owns reminder dispatch. |
| NEXT-63 | PRY-48 | COM-02/04 | Buyer-issued sale acceptance preserves external numbering and seller revenue ownership. |
| NEXT-64 | PRY-131 | COM-03/05, OPS-03 | An invoice payment link precedes settlement; NEXT-39 remains processor-event accounting. |
| NEXT-65 | PRY-53 | COM-05/06, FE, OPS | Customer-facing constrained artifact/current-balance access is not general book access. |
| NEXT-66 | Purchase/acceptance bridges in ERPNext review | COM-02, IMP, Cash readers | Commitment/acceptance records precede AP and do not implement a warehouse or a second accrual owner. |
| NEXT-67 | Budget Stop/Warn mechanisms in ERPNext review | COM authorization, report readers | Discretionary commitment control adds no balance ledger and must not prevent recording reality. |
| NEXT-68 | PRY-24/30 and chart foundations | FND-03, IMP, VAT, END | Versioned chart adoption maintains stable native identities and retained historical meaning. |
| NEXT-69 | PRY-27/28 | IMP, COM master data | Spreadsheet master-data staging differs from NEXT-12/44 financial-history imports. |
| NEXT-70 | PRY-08 and bank-format requirements | IMP-01/03/04 | Structured bank-file decoding reuses NEXT-10 admission instead of duplicating Plaid windows. |
| NEXT-71 | Bank payment-format and recovery requirements | COM-03, OPS-03 | Qualify the actual bank format/status channel around existing export and NEXT-08 capacities. |
| NEXT-72 | PRY-57 | VAT-02/04, END-07, OPS-03 | Declaration dispatch is distinct from NEXT-04 calculations and NEXT-37 assessment. |
| NEXT-73 | PAY-04 external-outcome requirements | PAY-04, END-07, OPS-03 | AGI submission consumes NEXT-21/36 output and does not replace payroll accounting. |
| NEXT-74 | INK2/SRU external-outcome requirements | END-06/07, OPS-03 | Tax filing/signature follows NEXT-22 fields and is not NEXT-48 annual-report registration. |
| NEXT-75 | Accounting-method transition extension | FND-03, COM-02, VAT, END | A reviewed method cutover is distinct from NEXT-38 ordinary cash-method events. |

## Execution lanes, not 25 concurrent writers

**Sales and VAT:** 51 establishes the shared multi-treatment invoice/credit representation. 52 and 53 add explicitly different service/goods evidence. 55 consumes the applicable reporting source sets. 54 is an independent customs-accounting branch over supported purchases. Do not add three new mutable tax ledgers.

**Revenue and receivables:** 56, 58, 59, 60, 61 and 62 share the invoice/capacity owner. Agree the source-component and residual contract before concurrent changes. An advance application, term change, cash discount and confirmed loss are not the same mutation. 57 uses the supplier side with its own original deduction capacities. 63 retains buyer-issued identity while calling the seller's normal financial owner.

**Customer service and payments:** 65's read-only portal can ship without 64. A whole-invoice payment link does not require installments. Both use current native residuals and already retained document bytes. 70 is a bank-source format admission; 71 turns actual bank status into the existing payment lifecycle, never into a second payment engine.

**Operating controls:** 66 adds purchase commitments and acceptance. 67 consumes their unreplaced exposure. A budget stop is for discretionary authorization, not permission to omit an existing obligation. Neither is required for a small company that does not use procurement commitments. 68 and 69 improve chart/master-data operations without rewriting financial history.

**External statutory completion:** 72, 73 and 74 consume existing declaration producers and the same durable-attempt substrate. They need separate actual provider profiles and mandate semantics. Do not build a tax API framework before delivering one real selected channel. 75 changes recognition regime only after independent qualification of the effective transition.

## Suggested implementation sequence

Start with **51, 58, 68 and 70** when those profiles apply. They cover sales breadth, revenue timing, chart maintenance and actual bank-file work. **52 and 55** follow for a business selling general-rule B2B services across the EU. **64 and 65** create a more useful customer-facing collection experience once the processor and invoice owners work end to end. **71 and 72** complete the selected bank/tax operating channels when access is available.

This is sequencing advice, not a universal release checklist. Inventory/customs profiles, budget control, self-billing and method changes should follow actual customer demand or company facts. External signing/access delays do not stop independent deterministic preparation, but they do remain external release gates.

## Root integration deliverables

Root reviews shared field shapes and meaning before domain merge: stable source IDs, separate source/deductible tax, exact money versus reporting integers, explicit half-open service intervals, independent approved-plan/body digests and one authoritative residual contribution map. Retain genuine zero semantic facts without zero monetary lines.

For each financial packet, require the actual command path to persist a complete group and reject stale/duplicate requests. Run an authorized schema/application exercise before treating a new persistence interface as a satisfied dependency. A schema string, module export or source-only leaf is not that evidence.

For each external packet, require the real selected interface/format release, configured authority, retained exact payload and authentic outcome/recovery evidence. Simulation can qualify internal state transitions only. Missing mandates or input tables are explicit gates, not code defaults.

## Per-packet completion record

Use separate states: `designed`, `leaf_present`, `integrated`, `journey_observed`, `company_qualified`, `external_accepted`. A packet can also be blocked at any state with a specific owner/input. Record exact revision, declared case set and artifacts. “Everything is implemented” is not a replacement for these distinctions.

The diagram in dependency-graph.json covers the declared new-wave edges, including optional integrations. It does not assert that the previous fifty form a newly validated full graph or that each optional case must be enabled.


---

<a id="part-29"></a>

# Design decisions resolved for NEXT-51..75

These are original implementation choices to qualify under the selected profiles. They do not change repository source or activate legal/accounting support. The source map identifies the current requirements and primary external facts.

## Separate recognition from billing, payment and reports

Mixed-rate and cross-border documents extend the original invoice/credit owner. Customer advances, revenue deferral and installment due dates remain different components of one financial story. A recurring invoice determines billing occurrence, not when all revenue is earned. A payment link does not issue another invoice. VAT, EU sales statements and employer/corporate returns consume their owned financial facts rather than reconstructing the books independently.

## Customer advance conservation

For a qualified taxable advance `GA=NA+TA`, receipt debits cash GA and credits advance liability NA plus VAT TA. A final supply `GF=NF+TF` can consume that advance under a compatible rule:

```text
Dr AR                    GF-GA
Dr advance liability        NA
Cr revenue/deferred         NF
Cr newly recognized VAT  TF-TA
```

The journal balances because GA=NA+TA and GF=NF+TF. Lifetime VAT is TA+(TF-TA), not TA+TF. Different rates, partial supplies or incompatible tax attribution require their own qualified branch. A security deposit and an overpayment are not forced into this model.

## Supplier advance conservation

A paid supplier advance GA with already deducted VAT DA carries asset GA-DA. Final invoice GF with eligible deduction DF creates cost GF-DF, new deductible VAT DF-DA, advance release GA-DA and payable GF-GA. Those components balance exactly. Gross advance carrying with deferred initial deduction is another explicit supported state, not an inferred missing tax value.

## Revenue deferral is net of its separate tax history

The schedule consumes the net revenue liability under the agreed service recognition rule. It does not postpone or repeat the invoice's independently qualified VAT. A contract change recomputes future recognition from actual remaining source capacity. A credit allocates earned and unearned consideration and retires the affected future schedule authority atomically.

## Payment terms partition one debt

Installments sum to the existing face/residual amount. A payment promise can move expected cash timing without editing legal due dates. Credits, discounts and write-offs update the same native obligation; reports cannot each derive a different outstanding amount. A customer portal shows saved statement facts separately from live residuals.

## Settlement differences need a cause

A small residual may be an agreed price discount, a bank fee, FX, cash rounding, tax change or unpaid principal. Size alone selects none of them. For a qualified customer discount P=C+dN+dT, debit cash C, discount/revenue dN and tax reduction dT against AR P. Without discount entitlement, the same short payment leaves principal outstanding.

## Allowance, loss and recovery are distinct

An allowance changes book valuation without forgiving the legal claim. A confirmed write-off consumes the appropriate AR and eligible VAT relief. For gross G, tax relief T and previously provided allowance A, the remaining loss expense is G-T-A. It can be negative when an earlier allowance needs release. Later cash recovery links the old written-off capacity and restores only tax actually relieved under the applicable treatment.

## Commitments never become duplicate actual spend

Budget exposure is actual recognized cost plus unreplaced order commitment plus requests not yet replaced by orders. The same source amount is not counted at all three stages. Hard budget stops apply before new discretionary commitments. A real supplier obligation must still be recorded with the appropriate breach/exception evidence rather than made invisible.

## Bank messages are evidence, not accounting commands

A statement parent entry and its nested transaction details describe the same money. The importer proves the selected decomposition or retains the parent with a diagnostic. A payment-file status can authorize no inference beyond the bank's actual semantics. Accepted instruction is not booked payment. Bank settlement has its own retained source and once-only allocation.

## External tax transfer, signature and outcome are independent

A VAT or AGI API draft may still require signature/submission. A corporate tax-file transfer may still await signature. The exact service profile determines what occurred. The obligation is fulfilled only by the required same-scope outcome, not a successful network request or a nonempty reference. A pending or unknown attempt cannot be duplicated with a new key to manufacture certainty.

## Method changes preserve recognized coverage

At a qualified cash-to-accrual transition, only the eligible unrecognized remaining portions receive new recognition. Previously paid or year-end-recognized portions stay untouched. In the opposite direction, old recognized open items remain a retained cohort; the app does not reverse them all or change historical VAT by flipping a current method field. Activation and its necessary coverage/financial effects form one controlled transition.

## Not selected

No new lending/card platform, inventory engine, consolidation suite, alternative SQL workflow layer, arbitrary rule interpreter or separate job runtime is added. Managed services and third-party production access remain explicit product/provider decisions. Original reference code has not been copied.


---

<a id="part-30"></a>

# Coordinator handoff: NEXT-51 through NEXT-75

Implement the selected new packets against the actual current OpenERP checkout. Start with its current AGENTS.md, ADR0010/0009 and the existing owner plans. The review basis for this dossier is `116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5`. Record current HEAD and dirty ownership before any edits. Search for an already landed equivalent and extend it rather than duplicating it.

Do not count an unfinished NEXT-01..50 integration as a new NEXT-51..75 feature. The old packet keeps its application/persistence/proof obligation. Read the new packet's required and conditional integrations separately. A services-only reporting profile does not wait for goods support, SEK bank import does not wait for foreign cash and a customer portal need not wait for payment-link checkout.

Select work by actual company/customer need. Ordinary mixed-rate/service sales, deferred revenue, controlled chart adoption and bank files are useful early profiles. Procurement/budgets, goods/customs and method switching are optional breadth. Keep the first reviewed period and daily usable journey ahead of expanding enums or collecting more unused pure modules.

For each new work item, bind the proposed records/functions to existing owners. Use Effect application operations, exact domain calculations and explicit transaction passing. No new generic financial interpreter, duplicate residual balance, speculative rules engine or queue system. SQL remains schema/grants/relational integrity plus the reviewed narrow accounting backstop. Normal journals, tax components, register consequences, approval consumption and receipts must commit as the complete named group.

Root owns shared schemas, lock/admission primitives, capability composition, migrations/grants and top-level routing. Assign domain-local changes to one lane and agree shared contracts before parallel edits. Register precise field shapes, source IDs, calculation units and digest meanings at the handoff. Arrays must remain arrays, compiler IDs must be the persisted IDs and imported money must not change its scale merely because a field is named Minor.

Every packet is delivered as a vertical workflow. A pure leaf is an intermediate result, not completion. Include application commands, persistence, native financial/report/currentness readers, usable UI or an explicit authorized official-channel handoff and observed recovery for the selected supported profile. Provider-specific claims require actual authorized provider evidence; local doubles prove only local behavior.

Keep existing test authorization. This task supplies designs and independent example checks, not permission to modify repo tests, submit tax returns, initiate real payments, reset a retained book or deploy. Do not weaken static rules or remove failed integrity checks. Manifest changes include the corresponding lockfile and frozen-install verification. Run permitted checks at current repository limits without stacking duplicate processes.

A worker handoff contains: exact changed files, named operations, shared contract/schema requirements, selected supported cases, actual evidence, refused/remaining cases, external dependencies and the next integration action. Do not flood the coordinator with full transcripts. The coordinator reconciles evidence by revision and the exact workflow, not by quantity of source files or passing document links.

Release acceptance follows the integration map. The first external exercise must use authorized test/recipient scope. Historical receipts and artifacts stay recoverable under current access even when new-work profiles are disabled or provider configuration changes.


---

<a id="part-31"></a>

# Sources, provenance and limits

Targeted repository basis: `116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5`, read on 28 September 2026. Current code search is not an exhaustive absence test and some search results resolved an earlier indexed revision; those are not substituted for the pinned file reads below. No full reference-code audit or application execution was performed.

The repository establishes the existing owners, scope and reported progress. Financial algorithms and delivery choices in NEXT-51..75 are proposed original designs. Where a prior requirement is unsafe or contradictory, the packet explicitly selects a different contract rather than pretending the reference proved it. Reference claims such as "unowned" or "better" are not new findings here.

No paid lending/card product or general consolidation project is adopted. The old fifty packets, Cash, document intelligence and their outstanding integrations keep their current owners. The current task expands ordinary supported accounting workflows. No license grant is inferred for copying reference source or commercial chart annotations.

## Repository evidence

### R01: Pinned main branch

Main resolved to 116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5 on 28 September 2026. Later branch changes are not silently included.

Source: https://api.github.com/repos/erik-kroon/openERP/branches/main

### R02: Current NEXT implementation progress

Selected progress rows distinguish merged source, pure leaves, integration and observed journeys. The requested range was partly truncated, so this is not an independently verified count of completed packets.

Source: https://github.com/erik-kroon/openERP/blob/116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5/docs/plans/next-packet-progress.md

### R03: Reference parity requirements

Requirements and PRY deliverables include broader sales/tax, advances-related workflows, deferred revenue, payment links, workbook import and bank formats. Old unowned/superiority claims and preserved recipes are not adopted as verified findings.

Source: https://github.com/erik-kroon/openERP/blob/116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5/docs/plans/11-parity-backlog.md

### R04: Repository-authored ERPNext/Frappe concept review

Planning input naming concepts such as advances, payment schedules, budgets and deferred revenue. This work did not independently clone/review ERPNext or establish the report's correctness. No reference code is copied.

Source: https://github.com/erik-kroon/openERP/blob/116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5/docs/plans/17-erpnext-reference-review.md

### R05: Book Zero, daily work and read-only Cash

First reviewed period and daily journeys govern priority. Cash already has an owner and must not double count instructions, invoices or commitments. Company facts are proposed inputs, not validated defaults.

Source: https://github.com/erik-kroon/openERP/blob/116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5/docs/plans/15-book-zero-workflow-cash.md

### R06: Current comparison reconciliation

Records ownership and several earlier completed source/qualified local improvements. Prior credit-renderer, SIE-dimension and fulfillment defects are not reassigned here. Attributed prior proof was not rerun.

Source: https://github.com/erik-kroon/openERP/blob/116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5/docs/plans/16-comparison-reconciliation.md

### R07: Current supplier payment document producer

Existing pain.001.001.03 serialization emits SEK and an invoice-derived end-to-end identity. Used to define selected-bank qualification as an extension, not to claim payment export is absent.

Source: https://github.com/erik-kroon/openERP/blob/116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5/apps/api/src/application/purchases/payment-document.ts

### R08: Current repository contributor rules

Effect/Drizzle tx passing, existing UI, scoped DB integrity, forward source discipline, explicit approval for test additions and frozen lockfile checks.

Source: https://github.com/erik-kroon/openERP/blob/116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5/AGENTS.md

### R09: Open-period retro-payroll working decision

Read in latest commit diff. Original payroll attribution, open accounting adjustment and declaration period are distinct. This remains NEXT-36/PAY-04 work, not a new correction project.

Source: https://github.com/erik-kroon/openERP/blob/116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5/docs/adr/0014-retro-payroll-open-period-adjustments.md

## Primary external evidence

These are narrow current-source observations, not ready-to-install legal data. Rates, eligibility and exact API/format contracts remain qualified inputs. Examples in the packets are synthetic arithmetic. No PDF specifications were analyzed and no unavailable linked bundles are claimed to have been read.

### X01: Skatteverket: VAT declaration fields

Official field guidance used for the distinction between supply categories, imports, output VAT and deductible input VAT. It is not an activated complete rule release.

Source: https://www.skatteverket.se/foretag/moms/deklareramoms/fyllaimomsdeklarationen.4.3a2a542410ab40a421c80004214.html

### X02: Skatteverket: periodisk sammanställning

Qualifying intra-EU goods/services reporting is a separate statement obligation. Company applicability and complete categories remain qualified inputs.

Source: https://www.skatteverket.se/foretag/moms/deklareramoms/periodisksammanstallningforvarorochtjanster.4.58d555751259e4d661680001093.html

### X03: Skatteverket: corrections and reporting periods

Distinguish original erroneous buyer/period totals from later price adjustments and selected goods/services reporting cadence. Exact format/API bundles were not acquired.

Source: https://www4.skatteverket.se/rattsligvagledning/edition/2026.12/431344.html

Related official source: https://www4.skatteverket.se/rattsligvagledning/edition/2026.9/446472.html

Related official source: https://www4.skatteverket.se/rattsligvagledning/edition/2026.7/325747.html

### X04: Skatteverket: import taxable amount

Customs amount and eligible duties/ancillary charges need evidence and no duplicate inclusion. Import VAT calculation is not another recognition of the supplier purchase.

Source: https://www4.skatteverket.se/rattsligvagledning/edition/2026.10/394064.html

### X05: Skatteverket: advances and reporting timing

Advances can require distinct paid/received VAT timing. This is not a rule that every deposit has VAT or that every printed advance request supports deduction.

Source: https://www4.skatteverket.se/rattsligvagledning/edition/2026.4/394189.html

### X06: Skatteverket: customer losses

Invoice-specific confirmed-loss evidence and VAT adjustment must be distinguished from a general accounting allowance. Qualification for an actual loss remains open.

Source: https://www4.skatteverket.se/rattsligvagledning/edition/2026.13/394227.html

### X07: Skatteverket: invoicing identity and applicable invoicing rules

Numbering responsibility and buyer-issued documents depend on the selected legal invoicing case. Historical superseded statements are not used as current permission.

Source: https://www4.skatteverket.se/rattsligvagledning/edition/2026.13/436123.html

Related official source: https://www4.skatteverket.se/rattsligvagledning/edition/2026.10/394082.html

### X08: SEB: Swedish payment infrastructure and address transition

Bank-specific implementation guides and date-sensitive address rules exist. Exact selected MIG/XSD ZIP bundles were not downloaded or exercised; bank compatibility is not established.

Source: https://sebgroup.com/our-offering/cash-management/cash-management-news/new-payment-infrastructure-in-sweden

Related official source: https://sebgroup.com/sv/vart-erbjudande/cash-management/nyheter-om-cash-management/avveckling-av-ostrukturerade-adresser

### X09: BAS: chart releases and changes

Versioned chart and comparison information is available. Its licensing/use conditions and supporting explanatory content must be handled separately; naming changes alone do not establish tax policy.

Source: https://www.bas.se/kontoplaner/

Related official source: https://www.bas.se/kontoplaner/jamfor-kontoplaner/

Related official source: https://www.bas.se/2025/12/04/andringar-i-kontoplanen-2026/

### X10: Skatteverket: API families and representative permissions

Official pages distinguish VAT, AGI and income-tax API families plus their permissions. No actual OpenAPI schema, access certificate, service idempotency or signing protocol was acquired.

Source: https://www.skatteverket.se/omoss/digitalasamarbeten/utvecklingsomraden/ombudochbehorigheter.4.7c708f0e16bed42cd05557a.html

Related official source: https://www.skatteverket.se/omoss/digitalasamarbeten/omvaraapier/behorighetertillsammansmedorganisationslegitimation.4.3129d65419ef1497c064787.html

Related official source: https://www.skatteverket.se/omoss/digitalasamarbeten/utvecklingsomraden/inkomstdeklaration.4.339cd9fe17d1714c0773300.html

### X11: Skatteverket: file transfer and later signature

Official tax-file handoff and subsequent signing are distinct steps. Complete SRU form qualification and actual authority acceptance remain required.

Source: https://www.skatteverket.se/filoverforing

### X12: Skatteverket: change of reporting method

The directions of method change have different conditions/procedures. The dossier does not infer permission, a turnover threshold or an effective date.

Source: https://www4.skatteverket.se/rattsligvagledning/edition/2026.7/394195.html

### X13: Riksbank: dated reference-rate history

The reference rate has dated half-year history. Actual interest/fee enforceability, spread and contractual basis still need separate qualification. No statutory fee or rate is hard-coded by the packet.

Source: https://www.riksbank.se/sv/statistik/rantor-och-valutakurser/referensranta/

Related official source: https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/tillkannagivande-20261490-av-uppgift-om_sfs-2026-1490/

### X14: Skatteverket: AGI technical format and signing/auxiliary-data boundaries

The technical index is versioned. Registration-agent permission does not itself grant signing/submission. Absence information has distinct handling/correction constraints. Complete schema/treatment qualification was not performed.

Source: https://www.skatteverket.se/foretag/arbetsgivare/lamnaarbetsgivardeklaration/tekniskbeskrivningochtesttjanst/tekniskbeskrivning1118.4.7eada0316ed67d7282a791.html

Related official source: https://www.skatteverket.se/privat/etjansterochblanketter/blanketterbroschyrer/blanketter/info/4796.4.41f1c61d16193087d7f8fd9.html

Related official source: https://www4.skatteverket.se/rattsligvagledning/edition/2026.14/368347.html

## Inherited scope

NEXT-01..50 are the prior user-requested designs, now partly represented by integrated code and partly by leaves or remaining proof. This package does not rewrite their files or certify their completion. Dependencies reference those existing contracts. An existing implementation discovered during the next coding pass should be extended/qualified instead of duplicated.
