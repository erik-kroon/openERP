# Book Zero, daily work and Drastic Cash

Status: working product requirements integrated on 2026-09-27 from the supplied [Book Zero PRD v1](../specs/book-zero-v1/PRD_openERP_Book_Zero_Workflow_Drastic_Cash_v1.md). This is a documentation update, not implementation or acceptance. The user identified this file as the openERP input; the archive's broader Drastic Financial Platform end-state is context and is not adopted as openERP scope here.

The [Accounted comparison reconciliation](16-comparison-reconciliation.md) maps the later FWD proposals to these outcomes and existing work owners. It records current gaps and superseded findings without adding another packet index.

## Outcome and scope

Deliver three connected outcomes: an independently reviewed Drastic accounting period (**Book Zero**), ordinary work that the owner can finish through the product, and a read-only, explainable payment forecast (**Drastic Cash**). Extend the period to the first financial year, then prove a new period and a separately approved transition from the old system. Work qualifies when it is needed for the actual company, a priority customer journey or a correct Cash explanation.

The existing accounting plans retain financial ownership. This plan owns the Book Zero outcome sequence and the supplemental forecasting requirements. `BZ-*`, `WF-*`, `AI-*`, `CASH-*`, `NFR-*`, `AT-*`, `L0`–`L7` and `G0`–`G7` are source traceability identifiers, not new migration numbers, additions to the 53-packet index or a second completion denominator. References to `AT-*` here mean the Book Zero cases, not the broader platform's `ES-AT-*` cases.

The first release includes sources, bank reconciliation, AP/AR, owner expenses and funding, approval/posting/corrections, applicable VAT/tax and period/year handoff. Payroll, assets, deferrals and foreign currency are required when actual company activity makes them applicable. Unknown applicability remains visible; an implementation gap cannot be declared inapplicable.

Cash initiates no payment and submits no filing. Lending, factoring, credit decisions, cards, a financial marketplace, investment advice and consolidation are outside this first delivery. File-based verification can proceed without a bank connector. Native production of every annual/tax filing is not a prerequisite to the first reviewed period; the full P6/P7 requirements remain open, with any expert handoff assigned and demonstrated in practice.

## Company basis and open inputs

The source reports **Drastic AB**, **SEB**, a normal **1 May–30 April** financial year and a first year of **2025-05-17–2026-04-30**, based on previously supplied information. Its author did not recheck the originals, and this documentation update does not qualify them. Treat these as onboarding inputs under [D-04/D-06](../open-decisions.md#book-zero-company-and-review-inputs), never system defaults or verified company facts. Owner-paid expenses and owner transfers are explicitly included in the proposed trial.

Select the first bounded historical period for complete independent controls, then cover the entire first year for handoff. Current Cash needs a separate current observation basis: the historical year-end balance is not today's bank balance. Accounting/VAT methods, VAT periods, registrations, K2/K3 applicability, payroll, currencies and prior submissions still require originals and dated rules.

## Requirement ownership

Read the full source requirement and its acceptance condition as well as the owner below. These mappings identify where to extend and verify behavior; they do not assert that the current code lacks or satisfies it. Existing NEXT/PRY material remains subject to its maintained adoption and reconciliation rules.

| Source requirements | Maintained owner | Required outcome or delta |
| --- | --- | --- |
| BZ-01 | [Shared contracts](00-shared-contracts.md), FND-03; D-04/D-08 | Versioned company scope with sourced effective facts and applicable, inapplicable-with-basis or unknown families. |
| BZ-02, BZ-03 | [Imports](03-imports-matching-reconciliation.md), IMP-01–IMP-05 | Originals, occurrences, retained matches, account/period coverage and independent controls. A missing month blocks readiness despite balanced loaded rows. |
| BZ-04, BZ-05 | [Imports](03-imports-matching-reconciliation.md), IMP-06; [commerce](04-invoices-payments-registers.md), COM-06; NEXT-12/NEXT-44 design | Separate raw-source reconstruction from history migration; reviewed openings/open items must not repeat recognition. |
| BZ-06 | [Posting](01-posting-approval-receipts.md), PST-01–PST-04 | Evidence → facts → treatment → validation → human review/approval → execution → durable receipt. |
| BZ-07, BZ-08 | [Commerce](04-invoices-payments-registers.md), COM-02–COM-06; [corrections](02-corrections.md); NEXT-06/NEXT-30 design | Partial/combined payments, credits, fees, undo, explicit overpayments and distinct expense/reimbursement/funding chains. |
| BZ-09 | [Accounting profiles](05-vat-payroll-assets-fx.md), VAT-01–VAT-04; [year-end](06-year-end-reports-filing.md) | Dated tax treatments, immutable return versions and separate tax-account, payment and external outcomes. |
| BZ-10 | [Accounting profiles](05-vat-payroll-assets-fx.md), applicable PAY/AST/FX packets | All actual transaction families have qualified treatment and independent proof. External payroll input is labelled by its real owner. |
| BZ-11 | [Year-end](06-year-end-reports-filing.md), END-01/END-02; IMP-05 and register-control owners | Version-bound period assessment across applicable controls; later relevant changes invalidate currentness. |
| BZ-12 | [Year-end](06-year-end-reports-filing.md), END-03/END-06; NEXT-11/NEXT-13 design | Complete readable year pack, full selected SIE profile and independent recipient import. |
| BZ-13, BZ-14 | [Operations/cutover](07-restore-operations-cutover.md), OPS-01–OPS-07; [frontend](../frontend.md) | A real new period, declared official writer, quarantined restore and separately authorized transition/old-system exit. |
| WF-01, WF-02, WF-03, WF-04, WF-05, WF-06, WF-07, WF-08 | [Frontend Book Zero journeys](../frontend.md#book-zero-daily-work-and-cash), FE-01–FE-04/FE-06; PST-02/PST-03/PST-05 | Coherent work projection, contextual review, exact bounded batch, receipt recovery, accessible return navigation and honest coverage/error states. |
| AI-01, AI-02, AI-03, AI-04 | [Operations](../operations.md#book-zero-agent-preparation), PST-05/FND-02; existing [agent preparation proposal](agent-preparation-proposal.md) | Scoped preparation with provenance, budget, cancellation and human authority; manual work survives model outage. |
| CASH-01, CASH-02, CASH-03 | [Cash contract below](#cash-basis-and-payment-identity); bank, commerce and source owners | A qualified common opening, knowledge cutoff and domain-owned payment identities. |
| CASH-04, CASH-05, CASH-06, CASH-07, CASH-08, CASH-09, CASH-10 | [Cash contributions below](#cash-contributions-and-no-double-counting); COM/VAT/PAY/AST/FX owners | Remaining payment amounts, explicit replacement/settlement links and qualified timing, without repeated tax, salary, transfer or reservation effects. |
| CASH-11, CASH-12, CASH-13, CASH-14, CASH-15, CASH-16, CASH-17 | [Cash results below](#cash-results-quality-and-scenarios); [architecture](../architecture.md#book-zero-and-read-only-cash) and [frontend](../frontend.md#book-zero-daily-work-and-cash) | Exact daily forecast, honest gaps, immutable scenarios, contributions, scoped exports and defined metrics. NEXT-45 remains the historical cash-flow report. |
| NFR-01, NFR-02, NFR-03 | [Domain](../domain.md), [operations](../operations.md), [recovery](07-restore-operations-cutover.md) | Exact provenance, server scope on every access/export, privacy and controlled interruption/recovery. |
| NFR-04, NFR-05 | [Frontend](../frontend.md#book-zero-daily-work-and-cash), [verification](../verification.md#book-zero-acceptance) | Measured latency on the declared profile; keyboard, narrow widths, real 200% zoom, localization and civil-date semantics. |
| NFR-06 | [Operations/cutover](07-restore-operations-cutover.md), D-07/D-08 | Readable retained originals, reports and manifests independent of the old subscription; qualified retention and restore. |

## Book Zero proof and handoff

Run two distinct historical exercises. **Reconstruction** starts from raw evidence and reviewed openings in an isolated trial book, with independent expected results. **Migration** transfers existing accounting, openings, open items and relationships without repeating historical recognition. The old ledger cannot both generate the reconstructed answer and be its only oracle. Trial books cannot send invoices or filings.

The first period must reconcile the ledger, bank item coverage and balances, AP/AR, owner flows, tax account, VAT and every applicable register. A technical lock or an empty work list is not a period assessment. Each assessment pins source coverage, ledger cutoff, relevant revisions and reviewer; later relevant changes produce a new assessment or mark the old one stale. Unexplained monetary differences remain blockers, not rounding tolerances.

The review pack must contain P&L, balance sheet, trial balance, general ledger, vouchers, a complete qualified SIE export, open items, bank controls, tax-account and VAT basis, applicable schedules, owner settlement, source index, unresolved questions, method choices and a file-hash manifest. The full-year SIE export includes chart, opening/closing balances and vouchers; a movement-only export is insufficient. Qualify format, encoding and actual recipient import, including transaction and balance comparisons. Original evidence and supplemental registers remain accessible outside the SIE file.

The reviewer must be able to use the package without custom code or manual reconstruction of standard reports. A reviewer's accepted handoff does not establish filing, signature or authority acceptance.

**Who reviews, and what "independent" means here.** The first operating mode is **owner-operated**: the owner/operator reviews their own period in the ordinary UI. A named outside accountant and unrelated commercial receiving software are **not** required to begin engineering or to accept a first release — that gate was unachievable in a one-operator repository and has been replaced by [ADR 0015](../adr/0015-owner-delegated-decision-pass.md). What replaced it is a substantive standard, not a waiver: actual original documents, explicit applicable rules, exact expected accounting effects, working application transactions, independently reconciled balances, and the owner's explicit approval of real actions. For acceptance, "independent" means independent inputs and independently derived expectations — computed from primary rule sources and the source documents, never by calling the production function or a second model. It is not professional certification, and nothing in this plan or in the product states or implies that a product decision waives a statutory audit or reporting obligation that applies to the company.

The substantive checks are unchanged by that. A complete source inventory, exact original-to-ledger relationships, independent account controls, real runtime failure and recovery, qualified affected rules, readable retained originals and an observed restore are all still required, and a period with unexplained monetary differences is still a blocker rather than a rounding tolerance. What changed is who may sign the assessment, not how much must be reconciled first.

**The first selected historical interval** is the earliest complete independently controlled interval from the actual supplied source. A separate current Cash basis needs its own actual coverage; historical cash is not today's liquidity, and due or tax dates are never modified to simplify a test. **Private local operation only:** use the existing Better Auth loopback password configuration, Bun API, PostgreSQL and retained-object filesystem port, on encrypted operator-controlled storage outside the repository. That authentication mode is not to be made internet-accessible, and the existing cloud and hosted adapters are preserved for their later explicit deployment gate. An independent encrypted backup and a demonstrated restore of database, originals and recovery configuration are required before this becomes the sole live ledger; a second folder on the same disk is not a backup. The next real period must work through normal UI with late evidence, corrections and retries; SQL repairs and hidden side calculations are recorded as product gaps. During parallel operation, identify one official accounting source and one owner of external dispatch. Retirement of the old subscription waits for export/readability, database-plus-object/key recovery, pending obligations and the separate cutover decision.

## Cash basis and payment identity

Cash is a forecast over authoritative reads. It owns assumptions and saved results, not journal balances, receivables, payables, tax calculations or payment execution. The first combined profile is **SEK** over an explicitly reviewed legal-entity/book account set. Private accounts, restricted funds, unused credit and the tax account are not automatically spendable opening cash.

Every opening observation retains account, currency, source/version, observation time, effective date, balance type and coverage. Booked ledger balance, statement balance and bank-reported available balance are distinct. Qualify a common `asOf` and any complete bridge from older observations. Without a bridge, show individual dated observations and an incomplete forecast rather than “balance today.” An available balance with unknown reservation/credit semantics cannot replace the v1 booked/observed basis.

Save both the economic `asOf` and the knowledge boundary `recordedCutoff`. Prove which payments are already represented in the opening, including same-day payments; a date comparison alone is insufficient. Later discoveries produce a new snapshot. Historical forecast accuracy cannot be improved by importing today's facts into an old result.

The proposed `CashEvent` contract carries the following semantics; these are not existing API or table names:

| Field group | Meaning |
| --- | --- |
| Scope and identity | Trusted entity/book; owning obligation plus payment occurrence; versioned source references. |
| Amount | Exact remaining minor units, original currency, direction and established/reviewed-estimate/unknown basis. |
| Time | Contractual due date, distinct expected date and documented/assumed/unknown date basis. |
| State | Planned, instructed, outcome unknown, observed or cancelled; separate from forecast inclusion. |
| Relationships | Qualified yes/no/unknown opening inclusion with evidence; exact supersession and settlement links. |
| Inclusion | Included, excluded or blocked with a visible reason. |

An invoice, instruction, bank observation, allocation and voucher may be evidence of one payment. Use owning relationships for deduplication; equal date and amount are only candidates. Preserve many-to-many allocations and remaining capacity. New identity or source revision must not repeat the economic contribution.

### Current cash basis implementation under review

P10 introduces an API preparation workflow in `application/cash/basis.ts`. Its public capture, read and JSON export use `/cash-bases`; MCP exposes `cash_capture_basis` and `cash_get_basis`. The bounded public capture, HTTP/MCP read and immutable export path passed with an independently specified opening150000. Two boundary defects were reproduced and corrected in source. Actual retained digest equality was proved before adding the database integrity constraint; excess historical cutoff acceptance was reproduced before applying HTTP payload parsing options. The corrected three-case public run passed capture, full amount/cutoff/cross-book/revocation refusal and retained digest tamper/immutability checks. Its exact receipts are retained in `docs/plans/evidence/product-p10/boundary-corrected/`. The remaining workflow cohort and performance are still unverified in this branch. This is a retained basis for a later forecast owner, not an implemented forecast curve or a company readiness decision.

The first capture accepts the current Stockholm civil date and retained account, capacity reconciliation and coverage report references. Reviewed eligibility and balance-type assumptions cite retained evidence. Financial amounts and historical knowledge cutoffs are rejected. Authority is checked before the book write lock; the owning transaction derives the database capture time, bank witnesses and canonical invoice residuals.

A selected current opening requires every selected account to qualify. Native full-period coverage remains `not_established`; gaps outside the selected current interval remain visible. Older closes have no accepted bridge in this profile and cannot be combined with current residuals into an invented opening. The source provides no bank observation timestamp, so each observation retains `observedAt=null`, its economic date and the reconciliation capture timestamp separately.

Invoice contributions keep contractual due dates separate from reviewed expected dates. Exact cash-method and supplier-settlement owning relationships can establish payment membership in the selected opening. A generic control payment without that relationship blocks inclusion. Foreign monetary items retain their original units and an explicit unqualified conversion reason. Tax, payroll, owners, assets and financing remain named source gaps without invented zero values or individual payroll data. The basis is labelled `known_items` and company coverage remains incomplete.

Saved JSON bytes are immutable. A new discovery or assumption creates a new capture. Reads and exports recheck current authority and preserve the original bytes. Dependency status distinguishes current, changed and unavailable. Later source population overflow prevents a new bounded capture and makes the old basis comparison unavailable; it does not erase the retained export. Conservative bank coverage freshness includes the book posting sequence, so callers may need a new actual coverage report after other financial postings.

## Cash contributions and no double counting

| Contribution | Required treatment |
| --- | --- |
| Receivables | Read remaining amounts after payments, credits and allocation reversals from commerce. Due date, payment promise and forecast date stay separate. Overdue undated items remain visible outside the dated curve. V1 uses reviewed date assumptions, not invented payment probabilities. |
| Payables and recurring costs | Read remaining payables from their register. A sent payment file is not settlement. Forecast commitments are not booked liabilities; link the actual invoice to the specific series occurrence it replaces. Unknown applicable outflows keep coverage incomplete. |
| Payroll | Separate net pay, withheld tax and employer charges. A reviewed estimate is replaced by the established run or qualified external payroll source. Do not add gross expense to net pay and tax financing. Restrict individual salary data independently of aggregate Cash access. |
| Tax account | Roll a separately reconciled position in date order using qualified debits, credits and transfers. Link calculation, filed version, assessment and amendment to the same obligation; preserve valid deltas. Project only the additional bank financing needed after available tax-account funds. Bank-day and availability dates require reviewed inputs/rules. |
| Owners, assets and financing | Keep reimbursement, owner funding, loan principal, interest and investment payments distinct. Depreciation is not another payment. Undated owner liabilities remain gaps. Uncommitted borrowing, credit or owner injections belong to separate scenarios. |
| Internal transfers | A verified transfer inside the selected liquid-account set is net neutral. A single observed leg or equal/opposite amounts cannot prove the relationship. Qualify in-transit funds and their availability. Transfer to the excluded tax account is a bank outflow. |
| Reservations | Define whether the opening already includes the reservation. Deduct its economic effect once, or refuse an unqualified balance type and show the gap. Pending instructions and unknown outcomes stay distinct from bank-observed settlement. |
| Foreign currency | Preserve original amount and qualified rate/date/rounding policy. No default 1:1 conversion. An applicable unsupported foreign obligation makes company coverage incomplete. |

## Cash results, quality and scenarios

Use exact minor-unit arithmetic and the repository's shared money codecs. Calculate each day for **30 days**, **90 days** and **13 weeks (91 days)**, showing actual start/end dates. For scenario `s`:

```text
B_s(d) = qualified opening B0 + inflows after t0 through d - outflows after t0 through d
M_s(H) = minimum of B0 and all daily balances through H
L_s(H) = M_s(H) - explicit liquidity buffer
```

Show the minimum and its date as well as the closing balance. Preserve negative headroom. Do not subtract a tax reserve again when its bank funding is already a contribution. The buffer is a reviewed assumption, not a statutory threshold; forecast headroom is not distributable equity or a guarantee that a payment can execute. Offer a conservative outflows-before-inflows stress view when intraday order is unknown.

Keep four quality dimensions: **source coverage, freshness, reconciliation and assumption uncertainty**. The summary distinguishes sufficient-for-selected-scope, incomplete, stale and unavailable/error. Unknown applicable salary/tax amounts cannot become zero. A forecast of known invoices alone is labelled “known items”; undated amounts and excluded contributions remain visible. Never infer “you can spend” from incomplete coverage.

Scenarios pin a base forecast and save explicit changes, creator, time and reason. Moving a receipt, revising a commitment or adding a hypothetical investment cannot edit legal due dates, payroll or the ledger. Explain whether resulting tax effects are qualified or omitted. Rebase into a new version when facts change, preserving the original scenario and forecast.

Every total, day and row opens its exact contributions, residuals, original currency, date basis, inclusion reason, evidence and assumptions. AI may explain those saved results; deterministic drilldown works without it. Save source boundaries, calculation/scenario versions, account set, contributions, exclusions, quality and exact results. JSON/CSV exports reproduce the same semantics and recheck current access, including after revocation.

Report overdue receivables, customer concentration in **open receivables at the same snapshot**, and the first forecast buffer/zero crossing. Zero total receivables means concentration is not applicable. No crossing within 91 days means no crossing in the displayed horizon, not infinite runway. Historical cash-flow and profit measures remain with their existing report owners.

## Delivery and independent gates

The source sequence organizes customer outcomes across current owners. These are planned targets; no row is completed by this update. L0 requires current code/evidence reconciliation before implementation, not a restart from the source's older inspection revision.

| Sequence | Observable result | Dependencies and existing gates |
| --- | --- | --- |
| L0 — scope | Qualified profile, source inventory, current owner map and proof plan. | D-04/D-06/D-08; G0 records scope and named unknowns, not accounting correctness. |
| L1 — first period | Raw evidence to reconciliation and independent review pack through ordinary UI. | L0 and relevant P0/P1; P2/P4/P5 in applicable scope; G1 needs independent controls and reviewer assessment. |
| L2 — daily work | Coherent queue, exact batch results, context-preserving review and receipt recovery. | Develop with L1's operations; FE/P3 owners; G2 needs actual priority journeys and authority/recovery proof. |
| L3 — Cash basis | Common opening, remaining payments, quality and explainable contributions. | Qualified bank, commerce, tax and applicable payroll reads; no external-customer-count prerequisite. |
| L4 — Cash forecast | Daily horizons, minimum/headroom, immutable scenarios and scoped export. | L3 plus independent numerical/semantic cases; G3 qualifies the selected profile and shows actual-company coverage separately. |
| L5 — year and new period | Reviewer accepts the entire first-year basis; a real new period works in parallel operation. | Applicable P4/P5/P6 and reviewer; G4 is year handoff, G5 is new-period proof, neither implies external filing. |
| L6 — transition | Readable export/archive, tested restore, operational responsibility and explicitly activated single writer. | P7, company scope, D-01/D-07/D-10 where applicable; G6 is a separate cutover approval. |
| L7 — Book One | Bounded external pilot in the verified profile with honest support and product claims. | L1/L2 and appropriate operating/company acceptance; G7 adds profile matching, permitted data flows and support. Cash is offered only within its proven scope. |

The proposed 3–5 pilot companies and 30% active-work-time improvement are research hypotheses, not release evidence or prerequisites to Cash development. Measure active time including corrections/support separately from waiting for evidence or review. Within accepted scope, unexplained differences and duplicate effects must be zero and required contribution provenance complete. Compare forecasts to qualified outcomes after 7/30 days, and 90 days when available, separating timing, amount, new-information and model errors.

## Acceptance and verification record

The source's **49 requirements** and **45 AT cases** are specified, not executed. Every requirement's own acceptance remains relevant; the case list is not an exhaustive replacement. The [verification plan](../verification.md#book-zero-acceptance) groups all cases by real boundary and preserves the source's independent 30-day example. Test additions require the implementing task's authority under AGENTS.md; choose failure cases and independent expectations before code, prefer E2E, and retain replayable evidence.

For each accepted gate record requirements/cases, exact code and dirty-tree identity, migration state, environment, data period, input/source hashes, steps, independent expected and observed outcomes, receipts/artifacts, reviewer and remaining limitations. No synthetic test, static check, screenshot or imported PRD closes an actual-company or external acceptance gate.

The [document verification record](evidence/book-zero-docs-verification.md) records provenance and checks for this documentation change only. Current technical and accounting ownership is preserved; no new financial computation owner, runtime, legal rule, provider or operational authority follows from the source document.
