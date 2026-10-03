# Open decisions and missing facts

Status: remaining configuration, company facts, authority and proof gates. Technical choices selected in [ADR 0004](adr/0004-complete-accounting-delivery-contract.md), the application-owned replacement in [ADR 0010](adr/0010-application-owned-accounting-replacement.md) and durable delivery in [ADR 0009](adr/0009-effect-mq-background-jobs.md) are no longer unspecified design work; their implementation/evidence gates can still be open. These are timed gates, not a request to answer everything before useful work can proceed. [External inputs](plans/10-external-inputs.md) specifies the required fields and owner artifact for every row.

Each row below separates four things that were previously blurred together: the **chosen design** (decided, and therefore no longer an open question), the **current configuration and facts** (what is true now, including reported-but-unverified company facts), the **observed implementation and evidence** (what has actually been exercised), and the **remaining affected-stage gate** (the specific evidence that still blocks the specific stage it blocks, and nothing broader).

A design is decided. A fact is not decided, it is unknown until evidenced. An evidence gap is not a decision. Keeping them in separate columns is what stops a decided design from being read as permission to assert a company fact or a runtime result.

The rows were selected by the [owner-delegated decision pass](adr/0015-owner-delegated-decision-pass.md) on 2026-09-28. The vendored record is [decision-pass-2026-09-28](specs/decision-pass-2026-09-28/README.md); it is the handoff, and this register is the authority. Every gate in that pass carries `independently_verified_by_this_pass: false`, and **no row below is closed by the decision that selected it.**

### D-01 — Identity, authentication and authorisation

- **Chosen design.** Private single-operator use through the existing loopback Better Auth password path, selected because the code already supports it: `apps/api/src/adapters/auth/configuration.ts` selects `password` on a loopback hostname and `oidc` otherwise. Eight-hour server sessions and disabled public signup are retained (`apps/api/src/adapters/auth/better-auth.ts`). Explicit memberships and revocable agent tokens. Financial approval stays outside ordinary MCP. Local authentication is not to be exposed remotely.
- **Current configuration and facts.** Actual operator identity, book grants, and secret custody are not established. Hosted mode keeps its real OIDC requirement, which is a **hosted-access** gate.
- **Observed implementation and evidence.** The mode selection, session length and signup restriction are read from source. No runtime authentication or authorisation acceptance was executed.
- **Remaining affected-stage gate.** Before trusted production approval and real accounting-data exposure: actual local actor and book grants, actual secrets, and observed authentication/authority acceptance. Before hosted access: real OIDC registration. Rejected as unnecessary: external OIDC registration as a prerequisite to local development, agent self-approval, hardcoded company identity or auth bypass.

### D-02 — Application/DB boundary and runtime proof

- **Chosen design.** [ADR 0010](adr/0010-application-owned-accounting-replacement.md) is retained unchanged, including the narrow SQL allowlist and the clean three-file baseline. No return to SQL-owned business procedures, and no reclassifying every absent duplicate trigger as a defect — inspect composed constraints before claiming a missing redundant trigger is a failure.
- **Current configuration and facts.** The migration chain and privilege boundary are the reviewed three-file baseline with forward migrations after release.
- **Observed implementation and evidence.** The [2026-09-26 replacement completion](plans/evidence/application-owned-replacement-complete.md) supplies local evidence for admission, rollback/replay, scoped grants, the fresh baseline and canonical byte/hash vectors. That evidence is revision-scoped. A documented pass is not current universal proof.
- **Remaining affected-stage gate.** Per revision: actual PostgreSQL/workerd/Bun results for changed schema, authority and transaction paths, a clean locked dependency install, and applied restricted-role migrations. Before calling a contract integrated, exercise one complete selected workflow and retain authentic failure, race, rollback and recovery records.

### D-03 — Independent expected values

- **Chosen design.** Expected amounts, byte vectors and finite laws are specified independently, in addition to end-to-end tests. Expected values are written **before** production results are inspected. [Accounted](plans/17-erpnext-reference-review.md) is a pinned comparison system, never the sole source of expected truth.
- **Current configuration and facts.** The reference is pinned at `erp-mafia/accounted` `7ebea94fb3968c126e67e6cfe7efab695cc65b2f`, isolated and nonauthoritative.
- **Observed implementation and evidence.** Several pure-domain vectors have been executed for individual packets; [NEXT packet progress](plans/next-packet-progress.md) records each row's actual proof level.
- **Remaining affected-stage gate.** Executable vectors across the actual runtimes, and adjudication of any reference disagreement against source facts and qualified rules. Rejected: generating expected output with the function under test, a majority vote between repeated model answers, and changing assertions to copy a faulty reference result.

### D-04 — Company identity, methods and applicability

- **Chosen design.** Two native accounting-method profiles — accrual and cash method — as explicit profiles with independent VAT-method configuration. **K2 is the first annual-report target for actually eligible companies.** For the first reported year beginning 2025-05-17, the applicable BFN version is selected from its start/end conditions, not from the most recent publication date.
- **Current configuration and facts.** The company name Drastic AB, 1 May–30 April fiscal year, first year 2025-05-17 → 2026-04-30, and SEB are **reported facts**, retained but not promoted to verified configuration. The owner's 2026-10-01 report says the fiscal year was confirmed with Bolagsverket and the company was registered on 2025-05-17. It reports VAT accounting by bokslutsmetoden (cash method) and annual VAT reporting for a full tax year from 2025-05-09, F-tax and VAT registration from 2025-06-18, and no employer registration. Preserve the VAT-method/period date and registration date separately; original records and effective history have not been admitted here. Cash accounting is indicated by the registration, but the bookkeeping method still needs confirmation. K2/K3 remains unconfirmed. Prior declarations, complete account set, prior official ledger and the payroll/asset/FX case population are **not established**. Engineering references are synthetic: a Swedish AB/SEK/accrual baseline plus a cash-method case with partial payment, unpaid year-end recognition and later settlement without repeated recognition. Both remain engineering profiles, not actual-company activation.
- **Observed implementation and evidence.** The treatment matrix in the [VAT/payroll/assets/FX plan](plans/05-vat-payroll-assets-fx.md) names the supported families; no actual company activation has been performed.
- **Remaining affected-stage gate.** Before a real affected financial action: the actual methods and effective history, cadence and registrations, framework applicability and prior declarations, and the complete account/source population, evidenced from original registration and change records. These block **only** the affected real financial action. They do not block source retention, review, synthetic implementation, or testing both supported methods. Rejected: guessing historical registrations, silently defaulting an unknown method, and blocking all development behind optional company facts.

### D-05 — Contract/capability inventory and transport parity

- **Chosen design.** Retain the current shared capabilities and stateless JSON MCP contract. **No SSE or tasks redesign.** The catalogue is generated from source metadata, and each allowed UI/REST/MCP/job route is qualified individually.
- **Current configuration and facts.** Supported MCP version and transport are the current emitted contract; see [agt01-api-mcp-parity](plans/agt01-api-mcp-parity.md).
- **Observed implementation and evidence.** A source inventory exists at its pinned revision, not observed transport acceptance.
- **Remaining affected-stage gate.** Actual route, permission and output observations, plus an explicit exposure classification per new capability, before advertising it. Rejected: counting a planned tool as a supported transport, and advertising every schema symbol as an executable agent capability.

### D-06 — Prior bookkeeping source and cutover

- **Chosen design.** File-first full-history import when an authoritative prior ledger and complete material exist; otherwise a separately identified original-source reconstruction with an evidenced opening. Reduced-history cutover is an explicit exception. No invented previous system.
- **Current configuration and facts.** Whether an official prior ledger exists, and its actual export and version, are not established. An unavailable export does not prove that none existed.
- **Observed implementation and evidence.** Generic SIE/opening/open-item admission and synthetic validation exist; no actual-company import has been performed.
- **Remaining affected-stage gate.** The prior source inventory, original statements and account set, prior filings and openings, and the candidate review interval, before a P2 actual import. Independent opening/movement/closing controls must be inspectable. Rejected: six predecessor adapters before a file-based period, duplicating full history alongside opening balances, destroying matches to re-run extraction, and undocumented cutover assumptions.

### D-07 — Hosting, retention, backup and recovery

- **Chosen design.** The existing self-host Bun API, PostgreSQL and filesystem original store form the first private operating profile, with data on encrypted operator-controlled storage **outside the repository**. Worker/Cloudflare and R2 ports are retained for hosted operation without becoming a first-use dependency. Engineering recovery targets: **RPO ≤ 24 hours, RTO ≤ 4 hours** — targets to demonstrate, not results.
- **Current configuration and facts.** Actual persistent paths, storage location, access, backup destination and recovery-key custody are not established.
- **Observed implementation and evidence.** Local restore design and portable adapters exist; no independent encrypted backup and no observed restore have been performed.
- **Remaining affected-stage gate.** Before relying on this as the sole live ledger: an **independent encrypted backup** and a demonstrated restore covering database, originals and recovery configuration together, with the achieved RPO/RTO measured rather than asserted. Automatic deletion stays disabled until record-class retention is qualified. Rejected: a second folder on the same device as disaster recovery, an invented bucket or production credential, a claimed completed backup, and a book dependent on an unretained chat or download link.

### D-08 — Rules, charts, schemas and provenance

- **Chosen design.** Primary-source rule research and specification review are performed by AI and coding agents. No nonexistent outside accountant is the default engineering prerequisite. Normative rules come from legislation, BFN/Skatteverket and official format specifications; pinned Accounted code is implementation and case evidence. Only the complete bounded scenario whose rules and tests are established is activated.
- **Current configuration and facts.** Specific dated releases remain unqualified: tax tables and column semantics, the employer-contribution rate stack and caps, the reporting-box set, statutory obligation dates, per-diem and mileage amounts, benefit rules, declaration and statement schema versions, e-invoicing profile bindings and the rate feed. The Swedish VAT research profile remains a bounded candidate.
- **Observed implementation and evidence.** Rule research and version records exist with recorded limitations; see [10-external-inputs.md](plans/10-external-inputs.md) and the [VAT research ADR](adr/0002-swedish-vat-profile-boundary.md).
- **Remaining affected-stage gate.** Per scenario, the period-specific rule inputs and rights/provenance for any copied code or data, before advertising that scenario as supported. Material factual or rule ambiguity in an actual case is a blocker, not a default. Rejected: declaring all reference features legally correct, requiring every Swedish rule family before the ordinary selected workflow, and fabricated expert review or source authority.

### D-09 — Test and fixture scope

- **Chosen design.** **Resolved as a bounded standing permission**, not a per-test approval request. Focused unit, property/conformance, regression and integration/E2E tests for existing or explicitly adopted workflows are authorised, with synthetic fixtures and disposable isolated local/CI systems, and real local PostgreSQL, workerd, Bun and selected browser/REST/MCP journeys in scope. The rule is stated in [AGENTS.md](../AGENTS.md).
- **Current configuration and facts.** No test was added, changed or run by the decision pass itself.
- **Observed implementation and evidence.** Existing checks and the current E2E suite remain the repository's instruments. **HARNESS-1 is rejected**: the trusted runtime role must hold the scoped writes its architecture requires, and tests target unauthorised end-user operations at their real admission boundary instead. That is a contradiction in the accepted test plan, not a new policy.
- **Remaining affected-stage gate.** None for ordinary tests. The permission is bounded and does **not** extend to real company data, live provider credentials, customer contact, production migration or reset, deployment, payments or statutory submissions, or invented company records. Stricter task-specific restrictions still govern where they exist — the dated document-intelligence authorisation and its no-live-provider limit are retained. Unrelated test work needs separate task authority, and expectations may not be weakened to obtain green output.

### D-10 — Providers, signatures and external outcomes

- **Chosen design.** [ADR 0017](adr/0017-bureau-first-product-focus.md) adopts connected execution after human approval as the commercial target: live bank feeds, Peppol delivery, direct VAT filing and BankID login/signing. File/manual handoffs remain supported fallbacks and valid first local engineering paths. This revises the earlier file/manual-first commercial sequence. Offline parsers, artifacts and documented adapter contracts remain buildable **without** credentials. Connected actions remain disabled until each selected provider capability has qualified consent, authority, contracts, configuration and observed outcomes; this direction grants no live-action permission. Employer-declaration connectivity follows the specialist-first payroll decision.
- **Current configuration and facts.** Provider accounts, certificates, sandbox availability, signing and submission capabilities are not established, and remain so by decision.
- **Observed implementation and evidence.** Local adapters, immutable artifacts and recovery states exist; no provider has been exercised, and no live credential is held.
- **Remaining affected-stage gate.** Credentials and contracts only for a **selected** connected exercise, plus observed submission, assessment and payment outcomes. Missing credentials do not forbid an offline parser, artifact or local adapter contract; they forbid unauthorised live use and any external-acceptance claim. Rejected: a credential vault before every public parser, simulated submitted/paid/accepted states, and automated real filings, payments or contact inferred from this delegation.


## Book Zero company and review inputs

The [Book Zero PRD](specs/book-zero-v1/PRD_openERP_Book_Zero_Workflow_Drastic_Cash_v1.md) reports earlier company information; its originals were not rechecked for the document. These inputs refine existing D-gates rather than close them or create a competing decision list.

| Existing gate | Reported starting point | Required qualification and timing |
| --- | --- | --- |
| D-04 / D-08 | Drastic AB; normal 1 May–30 April year; first year 2025-05-17–2026-04-30. | Legal identity and sourced profile; accounting/VAT methods, registrations, reporting framework, prior declarations and actual payroll/asset/currency applicability before their company claims. |
| D-06 | SEB; prior work with company/private evidence and owner transfers. | Original exports and permitted use, exact company-account set, retained matches, complete intervals and independent controls. September 2026 is the user-selected acceptance period; obtain its independent controls and authoritative August closing state, retain current-fiscal-year history, and qualify a separate current Cash basis. Private accounts stay outside company liquidity. |
| D-04 / D-06 / D-08 | A reconciled period and a first-year handoff are required outcomes. **A named outside accountant and unrelated commercial receiving software are no longer required to begin engineering or to accept an owner-operated first release** ([ADR 0015](adr/0015-owner-delegated-decision-pass.md)). | **Removed as a gate:** naming the accounting reviewer, and naming unrelated receiving software. **Kept, and still required before G1/G4:** the independent expectations and review scope themselves, proven full SIE import plus a readable original/register index, source-to-ledger relationships, independent account controls, and assignment of any remaining annual/tax deliverables. Where the company is legally subject to an external audit or reporting obligation, that obligation is unaffected by this product decision and is not waived by it. |
| D-01 / D-07 | Existing identity/runtime design is retained. | Actual users and book rights before real-data exposure; archive location, retention basis, keys, recovery targets and operating owner before retained production data and G6. |
| D-10 | Direct connections are not prerequisites to the first file-based period. | Qualify actual provider contracts, credentials, scope and outcomes only when the connected action is used. Cash itself initiates no payment or filing. |

Company unknowns block their dependent acceptance, not independent synthetic product work. Source values are not verified defaults, and the wider financial platform's commercial or regulated-product decisions are not added to openERP by this update.

**Ownership and the acceptance standard.** The owner/operator is a single person and makes the product and engineering decisions; the analysis and decision role resolves them and coding agents implement them. For acceptance, "independent" means independent inputs and independently derived expectations — computed from primary rule sources and the source documents, never by calling the production function or a second model. It does not mean professional certification, and the word is not used interchangeably with certification anywhere in the maintained documents. The owner remains the person who confirms business facts and authorises real company actions; a guessed registration, a synthesised signature or a simulated bank payment is not evidence. The user-selected first acceptance interval is Drastic AB September 2026, with retained history from the evidenced current fiscal-year start and authoritative 2026-08-31 closing state as its opening basis (see [the current reconciliation](plans/current-foundation-reconciliation.md)); 2026-10-01 remains a candidate cutover boundary until comparisons and operational gates pass, and a separate current Cash basis needs its own actual coverage — historical cash is not today's liquidity, and due or tax dates are never modified to simplify a test.

The company-facts ledger seed in [the vendored decision record](specs/decision-pass-2026-09-28/company-facts.seed.json) is deliberately incomplete: it keeps methods, registrations and populations explicitly unknown and separates reported facts from synthetic engineering profiles. Filling a missing value with a synthetic default does not activate a posting; it only destroys the signal that the fact is missing.

## Resolved for the working design

[ADR 0014](adr/0014-retro-payroll-open-period-adjustments.md) selects open-period linked adjustments as the retro-payroll default, with original payroll attribution retained and declaration corrections separate. PAY-03 / NEXT-36 and PAY-04 own delivery; PRY-132 retains locked-period refusal without a payroll exception. D-04/D-08 still require company applicability and current Swedish accounting/employer-declaration treatment, including any permitted reopening policy. Implementation and end-to-end proof remain open.

The repository settles the Effect major, application names, shared schemas and styling system ([ADR 0001](adr/0001-checkout-runtime-and-accounting-boundary.md)). The accounting design uses one PostgreSQL relational authority, exact minor-unit posting values, sealed approval and transactional receipts ([ADR 0002](adr/0002-exact-posting-and-approval.md)), plus a native target without a speculative previous-system bridge ([ADR 0003](adr/0003-native-accounting-and-migration.md)). [ADR 0004](adr/0004-complete-accounting-delivery-contract.md) retains the paired monetary shape, source-occurrence separation, production admission shape and physically fenced first cutover. [ADR 0010](adr/0010-application-owned-accounting-replacement.md) settles the application-owned trust boundary, clean three-file baseline, narrow SQL allowlist, caller cutover and no-compatibility path. [ADR 0009](adr/0009-effect-mq-background-jobs.md) settles durable delivery on a separate effect-mq Bun process. These choices do not resolve actual company/provider facts or substitute for proof.

When closing a decision, record the chosen behavior, rejected alternative, evidence and affected verification scenarios. Do not mark a question resolved merely because an example file contains a value.

## Adopted financial contracts; delivery gates remain open

[ADR 0008](adr/0008-financial-fx-vat-impairment.md) adopts the FX, VAT and impairment contracts after the user's confirmation on 2026-09-24. Their ownership, signs and atomic lifecycle decisions are no longer unspecified blockers. The earlier feasibility reviews remain historical context, not current instructions to defer the adopted scope.

| Record | Class / owner | Selected decision and next action | Remaining gate / independent work |
| --- | --- | --- | --- |
| FX-02-carrying-owner | Design adopted; commerce/FX owner | Implement commerce-owned original units and carrying value, then full synthetic receivable settlement and owned correction. | Code and runtime proof open; D-03/D-04/D-08 qualify compatibility/company policy. Existing rate reviews and book-currency workflows continue. |
| VAT-03-effect | Design adopted; VAT/tax-account owner | Implement obligation-owned control reclassification with signed roles, exact lineage and receipt recovery; stage assessment/amendment separately. | Source implementation is present in forward 9120/9130 with API/UI wiring; SQL, runtime, browser and financial-outcome proof remain open. Actual-company VAT still needs a real calculation profile plus D-04/D-08, and D-10 for connected outcomes. Tax-account matching can continue independently. |
| AST-03-impairment | Design adopted; subledger owner | Implement distinct impairment contra and complete future suffix atomically, including controls, disposal and bounded correction. | Code and proof open; broader asset classes, consumed-history corrections and economic reversal qualification remain scoped follow-up work. Ordinary schedules continue. |
| PAY-01-foundation | Source present; payroll owner | Qualify migration 9050 and typed employment/work/opening inputs, then implement the selected PAY-02 calculation profile. | Runtime proof and input adequacy remain open; company rules and actual records remain D-04/D-08 gates. Do not restart from “no employee records.” |
| Provider exercise | External input/proof; integration/operator owner | Obtain documented provider behavior and authorized sandbox access; import/replay/recover a deliberately interrupted sync. | D-10 access/consent and actual outcome evidence; adapter work against documented behavior remains available. |
| Company readiness | Facts/implementation/proof; company and domain owners | Establish profile/applicability, process real material and independently reconcile the period. | D-04/D-06/D-08 plus implemented workflows; configuration alone cannot close readiness. |

Track design adoption, implementation, runtime verification, company applicability and external outcome separately. No new financial implementation, legal activation or provider acceptance is claimed by this decision update. The [delivery plan](plans/05-vat-payroll-assets-fx.md#adopted-financial-contract-delivery) turns each adopted contract into bounded work and proof requirements.

## External inputs named by the NEXT dossiers add no new decision

The [NEXT dossier plan](plans/12-next-implementation-dossier.md) indexes one hundred twenty-five implementation packets, each of which lists the qualified data it cannot invent: statutory rates and tax tables, reporting-box semantics and period cadence, employer-contribution parameter sets, mileage and per-diem amounts, declaration and statement schema versions, bank file formats, e-invoicing and access-point specifications, document-signing protocols, filing service specifications, extraction provider and model identities, and provider credentials. Every one of those is an instance of an existing row, so none is recorded again here: company identity, method and applicability facts remain **D-04**, dated rule, table, format and schema parameters remain **D-08**, provider accounts, consent, sandbox and authorization remain **D-10**, and any new or changed test or fixture remains **D-09**.

Three consequences follow for the packets themselves. A missing qualified input blocks the affected claim of support, not the implementation of the pure calculation and internal state machine, and it prohibits a real-company or provider acceptance statement. Where a packet depends on a company fact that has not been established — the cash method, a loan agreement, employment terms, lending, ROT/RUT, and the goods/customs, credit-loss, method-transition, project-billing, lease, tax-depreciation, pension, dividend, grant, setoff, confirmation, provision, B2C/OSS, foreign-VAT-recovery, car-benefit, share-subscription and direct-debit profiles added by the third, fourth and fifth waves — the case stays an explicit conditional edge rather than an assumed population. The scope dispositions themselves were settled separately and are recorded in the dossier plan, not as D-rows.

## Product-scope dispositions are not decision rows

[ADR 0015](adr/0015-owner-delegated-decision-pass.md) dispositioned 23 product-scope capabilities that the maintained index did not own: adopted bounded accounting capabilities, adopted optional product work, adopted limited profiles, or deferred. Those are **product decisions, not missing facts**, and they are recorded with their identifiers and owners in [the dossier plan](plans/12-next-implementation-dossier.md) rather than here, because this register is for facts and gates that remain unevidenced.

Three distinctions survive the transfer and are stated here so they cannot be flattened later. *Adopted conditional accounting* means the company case decides whether it is required for that release — it is not optional forever, and it is now a question about the company rather than about the product. *Adopted optional* means sequenced later and does not all precede the first usable accounting period. *Deferred* — grants and multi-reviewer quorum — means beyond the first release, and it is not permission to ignore a real transaction or to invent another human signature; an actual unsupported case stays visible. A positive workflow may not be advertised without a clearly supported correction boundary and a truthful refusal and recovery path outside it.

**Eleven capabilities the decision pass does not reach remain open.** The pass was written against a register one dossier wave behind, and its 23 items correspond exactly to the gaps surfaced by waves one to four. The fifth wave added eleven more, and the pass does not mention them: onerous and warranty provisions, insurance loss and recovery, common-cost VAT deduction true-up, EU B2C destination VAT and Union OSS, EU foreign input-VAT recovery, car-benefit valuation, interest-statement identities, share subscriptions, direct debit, and balance-sheet substantiation. They are carried forward open in the dossier plan. Silence is not a decision, and no agent may read this register as closing them.

## Cross-register line references do not establish role exclusivity

Source inspection found that a retained subledger carrying-basis line and a tax-account
match can reference the same posted book/voucher/line. Subledger linkage promises line
uniqueness inside its own register; the current contracts do not establish a universal
exclusive financial capacity or legal account classification for those references.
The overlap is not, by itself, evidence of duplicate posting. Public read views may disclose
exact related records for review, but this does not change matching/posting eligibility or
assess role compatibility. A future exclusivity policy requires an explicit contract choice
and both-direction admission plus existing-record handling; no such policy is selected here.

## Historical feasibility evidence

The [FX](../apps/api/docs/FX-FINANCIAL-FEASIBILITY.md), [VAT settlement](../apps/api/docs/VAT-SETTLEMENT-FEASIBILITY.md) and [impairment](../apps/api/docs/SUBLEDGER-IMPAIRMENT-FEASIBILITY.md) reviews explain why implementation was deferred. ADR 0008 supersedes their unresolved choices for the selected first profiles. Their source findings must still be reconciled against the live migration chain before implementation; adoption does not establish that any new financial operation exists.

The [2026-09-26 replacement completion](plans/evidence/application-owned-replacement-complete.md) supplies local evidence for D-02 and D-03: current admission/rollback/replay, scoped grants, the fresh baseline and canonical byte/hash vectors. These observations do not waive the company/profile, external provider, custody or hosted deployment gates above.

## Document Intelligence task authority — 2026-09-27

For [this isolated delivery](plans/document-intelligence-delivery.md), the user
explicitly approved E2E coverage for PDF/image reading, review, draft creation,
missing pages, failures, retries and human edits (D-09). The user also instructed
that live provider use remain disabled (D-10). The loopback-tested HTTP adapter
is connected to the normal self-host API and preparation runner through explicit,
default-disabled configuration. No live credentials, connection or rollout are
enabled. This task-specific scope
does not authorize other provider exercises or remove D-10's deployment gates.
