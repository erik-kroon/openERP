# VAT, payroll, assets and foreign currency

Owner: dated accounting/tax profiles and subledgers, with separate typed modules for each family. Phase: P4/P5; synthetic schedule mechanics may precede legal profile activation. Shared source, plan, approval, receipt and register contracts apply throughout. A generic balanced journal is not proof that any treatment below is legally supported.

## Common rule release

Each family first records required company facts, primary authorities, applicable intervals, calculations/rounding, supported and unsupported cases, independently reviewed examples, schema/mapping versions and reviewer activation. Rules are immutable after activation; new versions produce impact cases for prior calculations without overwriting them. Missing facts block the affected calculation, not evidence retention.

The [Swedish VAT research ADR](../adr/0002-swedish-vat-profile-boundary.md) remains a candidate narrow profile. This plan does not activate it or broaden it through inference. [External-input acquisition](10-external-inputs.md) defines how legal sources and company facts become implementation inputs. No tax percentage, salary table, allowance, depreciation lifetime or deadline is invented here.

## VAT and tax account

### Model and treatment coverage

`TaxFact` binds the causal event and invoice/line revision to supplier/customer jurisdiction and registration evidence, supply type/place/date, tax point, method, currency, basis, rate/rule revision, output/input amounts, deductibility basis, reverse-charge/import classification and reporting-period attribution. Store gross, net, calculated tax, deductible tax and non-deductible portion separately. Classification is explicit, effective-dated and auditable; it is not reconstructed solely from BAS account shape.

The planned treatment matrix includes ordinary domestic rates, exempt/out-of-scope cases, domestic reverse charge, intra-EU goods/services, non-EU services/imports, advances, credit/correction cases and mixed/partial deduction. Special schemes/industry rules require their own profile row with eligibility and acceptance before support. A treatment marked unsupported cannot fall back to ordinary domestic handling. A company containing such activity cannot pass full-return readiness until the applicable row is implemented or the accounting obligation is handled through an explicitly reconciled external workflow.

`VatReturnSnapshot` pins registered reporting interval, company/profile, ledger/tax-fact cutoff, mapping release, box contributions/exclusions, source coverage and checks. `VatAdjustment` links an amended fact to the original period/artifact. `TaxAccountEvent` preserves statement source identity, charge/credit/interest/payment classification and matching basis independently of the VAT return. `VatSettlement` links the return version to a distinct accounting effect; its report role prevents it from re-entering the taxable-activity totals.

### Operations and controls

Classify/review source facts; prepare recognition effects; prepare/validate return snapshot; explain a box to contributing facts/lines; approve settlement; prepare an amendment; ingest/reconcile tax-account statements; and prepare a submission artifact. REST/MCP/UI share these operations. Human rule activation, return approval and external submission authority remain separate powers.

Required controls compare independently expected box values, tax-control account rollforwards, return settlement, source completeness and prior filing versions. Reverse charge must preserve both tax and required basis semantics even where net tax is zero. A valid balanced voucher with missing basis is not ready. Tax-account transfers/charges are not assumed to be taxable sales/purchases. Explicit reviewed overrides preserve history and affect both totals and drilldown through the same calculation graph.

If a mapping changes after filing, identify affected snapshots by mapping/fact lineage, produce a new artifact and an amendment case, preserve the old submitted bytes and external receipt, and require the appropriate approval. A current return cannot claim completeness while a mandatory source/check is unavailable. The UI shows each box, its rules, contributing/excluded items, unresolved treatments and filing state separately.

### Expense review foundation (implemented source; runtime not verified)

The VAT-01 expense foundation is implemented in forward migration0710, the `expense-tax` contract/API module and a domain-local review UI. It retains separate immutable source observations and operator review facts, exact source/review discrepancies, and immutable contribution/exclusion snapshots. Every actual-company contribution remains excluded: no production legal profile, effective interval or rounding policy is activated. Only the explicit `synthetic-expense-tax` version1 profile may demonstrate caller-supplied rational rates and deduction fractions with exact-division refusal.

Snapshots include all bounded retained components, including unknown, stale, foreign, unsupported and outside-interval exclusions. They are accountant review artifacts, not VAT returns, ledger-control reconciliations or source-completeness certificates. See [implementation and integration boundaries](../../apps/api/EXPENSE-TAX.md) and the [pre-implementation risk/acceptance record](../../apps/api/EXPENSE-TAX-RISKS.md). Shared composition and native/runtime validation remain root-owned; source presence does not complete VAT-01's legal or proof gates. Existing asset schedules are unchanged.

## Payroll and declarations

### Model

`EmploymentRevision` carries person identity, jurisdiction/residency facts, effective contract/pay/working-schedule terms, required tax facts and evidence. Restrict personal/salary evidence to explicit payroll access. `WorkInputRevision` retains hours, absence, holiday, benefits, expenses, adjustments and period/date basis. Changes after approval produce new revisions rather than editing the old pay run.

`PayRunRevision` freezes employees, employment/work inputs, rule/tax-table releases, gross components, benefits, deductions/withholding, net pay, employer liabilities and exact rounding/residuals. `PayRunPosting` binds the approved revision to expense/liability effects and individual/control totals. `PaymentInstruction` retains exact employee payee revision and exported/submitted bytes. `PayrollDeclaration` is a separate period/person-specific artifact with its own schema, validation and external outcome; AGI and KU remain distinct families.

### Calculation scope

Plan salaried/hourly pay; ordinary variable pay; benefits and expense reimbursements; absence/sick pay with actual work pattern; holiday accrual/pay; deductions/adjustments; employer contributions; withholding; termination and retroactive corrections. Each legally/materially distinct case is a reviewed rule profile. Irregular workweeks use the retained calendar/schedule rather than a five-day assumption. Tax tables, age/status eligibility and interval limits come from dated releases. Pensions/collective-agreement obligations are explicit company inputs; absence of a configured obligation is not evidence it does not apply.

Compute exact component breakdowns and independent control equations. Never obtain expected test answers by calling the production calculator. Approved pay runs remain stable if an employee later changes address, schedule, tax status or salary. Corrections name the original run and distinguish replacement/catch-up pay from declaration amendments.

### Workflow and proof

Collect inputs → validate completeness → calculate draft → freeze/review → approve → commit payroll/register effects → authorize/export or submit payment → observe settlement → prepare/validate/approve declaration → record external outcome. The same UI can guide these steps without conflating their authority. A prepared payroll does not mean salaries were paid or a declaration accepted.

The official [Skatteverket technical description](https://www.skatteverket.se/foretag/arbetsgivare/lamnaarbetsgivardeklaration/tekniskbeskrivningochtesttjanst/tekniskbeskrivning11171.4.7eada0316ed67d7282a791.html) publishes a versioned AGI file contract. Pin the exact applicable schema/specification and validate person/period meaning as well as XML structure before enabling that profile; the portal observation does not activate a schema here.

## Assets and deferrals

`AssetRevision` records acquisition/disposal sources, ownership/use dates, category, cost components, book/original currencies, residual value, useful-life/method decision and rule/evidence basis. `ScheduleRevision` defines exact installments and stable occurrence identities. `OccurrenceEffect` links each prepared/posted/reversed installment to its plan/voucher/register effect. `AssetEvent` records addition, transfer, impairment, estimate change, disposal or correction. Accounting depreciation, tax treatment and tax adjustments are separate records/calculations.

The current exact equal-allocation synthetic schedule is retained as a named policy. It is not automatically an approved depreciation method. Import opening carrying value and accumulated depreciation with their source evidence; do not restart depreciation from original acquisition cost. Register/control reconciliation compares retained asset balances and effective schedule postings against GL accounts at a fixed cutoff.

A future estimate/amendment creates a new schedule revision for the explicitly remaining basis and future periods. Posted occurrences and their identities never change. Prepared but unposted occurrences are superseded with new approval where their effects change. Deterministic residual allocation ensures installments sum to the intended basis exactly; no last-period amount is guessed from floating-point subtraction.

Post an installment and its schedule/register link in one transaction. Disposal seals the asset's current carrying basis, proceeds, tax treatment, accumulated depreciation release and gain/loss, including all register consequences. Direct/cascade deletion of a posted schedule or asset is refused. Deferrals use the same occurrence/receipt machinery but separate recognition/amortization semantics; no duplicate speculative schedule framework is needed.

### Bounded carrying basis and declared-account controls (implemented source)

[Subledger controls](../../apps/api/SUBLEDGER-CONTROLS.md) adds forward1500: immutable acquisition/imported carrying bases linked to existing posted lines, and exact declared-account GL snapshots. Gross cost, prior accumulated recognition and remaining carrying amount are retained separately. Missing/reversed bases, occurrence gaps, all ledger contributions and offsetting unexplained rows remain visible. A clean selected-account difference is not complete source coverage or legal depreciation approval.

Forward1510 binds the whole control dependency into closing and accountant-review-v3 artifacts. Missing bases and unavailable complete controls remain mandatory blockers; new bases or report inventories stale earlier approval scopes without rewriting their bytes. API/MCP/routed UI composition is connected in source. Both migrations remain unapplied and runtime-unverified. Forward1800 now captures linked basis authority on native preparations and checks it during shared validation and physical posting. Known generic occurrence and correction-lineage replacements cannot borrow that authority; genuine full reversals remain separate. Existing standalone synthetic schedules keep their interpretation. This source integration and its routed schedule UI remain runtime-unverified.

## Foreign currency

`ExchangeRateObservation` records source, retrieval and effective dates, currency pair/direction, exact rate, scale and source evidence. `ValuationPolicy` specifies rate-date selection, source hierarchy, precision, rounding and fallback/refusal. No missing rate is silently replaced with 1 or a nearby convenient date. A manual reviewed rate is a distinct evidence-backed decision.

Retain original currency amount, original rate/basis and book-currency carrying value at recognition. Settlement releases the correct carrying portion and records cash, fees and realized FX explicitly. Partial allocations retain both original-currency capacity and book-currency release; the final residual follows a declared exact policy so rounded pieces conserve the original carrying value.

Period remeasurement selects eligible open monetary items from a fixed snapshot, computes new book values and unrealized FX under a reviewed policy, seals the affected item set and posts the revaluation/required future reversal with stable occurrence identities. A new settlement or rate/policy revision stales the proposal. Never revalue a historical immutable voucher in place.

The FX review UI shows source amount/currency, carrying amount, selected rate/source/date, calculated settlement/revaluation, fees and residual. Per-currency registers reconcile to book-currency control accounts through recorded conversion effects; summing unrelated currencies is never presented as a meaningful balance.

### Manual exchange-rate review subset (implemented source; runtime unverified)

[Manual exchange-rate reviews](../../apps/api/EXCHANGE-RATE-REVIEWS.md) adds forward1900:
operator-reviewed directional rational rates, immutable evidence-backed revisions and exact
nonnegative conversion review artifacts. New capture requires the exact current revision and
matching effective date. Source scale is explicit; book scale comes from metadata. The named
synthetic half-up policy retains the exact fraction, quotient, remainder, rounded minor units and
signed residual. Missing/stale rates never default to1 or invert silently. Historical JSON bytes
remain unchanged, with separate live dependency currentness. Forward2300 adds permanent,
operator-reviewed observation withdrawal without rewriting those bytes. New revisions/conversion
captures refuse withdrawn observations; successful old command replay and historical reads remain
available. Live usability is separate from retained rate facts, and withdrawal makes saved review
currentness false. Pinned UI drafts retain their exact-key recovery path after withdrawal.

Shared composition and runtime proof remain root-owned. No legal/company profile, foreign-currency
invoice/payment recognition, settlement gain/loss, carrying register or revaluation posting is
activated. This is a bounded FX-01 review subset, not completed FX-02/03 or financial-close readiness.

## Delivery packets

| ID     | Deliverable                                                                                   | Depends on             | Acceptance                                                                                            |
| ------ | --------------------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------------------------------------------------------- |
| VAT-01 | Dated treatment/profile matrix and source-backed TaxFacts with explicit unsupported cases.    | FND-03, COM-02         | E-02/E-13: classification/date/deduction facts required; no guessed net/tax split.                    |
| VAT-02 | Return snapshots, contribution/exclusion lineage and independent box controls.                | VAT-01, IMP-05         | E-15/E-16: reverse-charge basis retained, settlement excluded deliberately, unavailable check blocks. |
| VAT-03 | Tax-account source events, matching, settlement and control rollforward.                      | VAT-02, IMP-04         | E-05/E-13: feed/import overlap cannot recognize twice; tax-account movement not taxable by default.   |
| VAT-04 | Return amendment/version impact and approved artifact handoff.                                | VAT-03, END-03         | E-16/E-19: original filing retained; exact new snapshot/artifact and honest external state.           |
| PAY-01 | Employment/work/obligation revisions, privacy scope and dated rule inputs.                    | FND-02, FND-03, IMP-01 | E-01/E-06: sensitive access and historical input stability; required facts cannot default.            |
| PAY-02 | Exact calculation profiles for the declared payroll case matrix.                              | PAY-01, PST-01         | E-02/E-13: independent gross/net/liability outcomes including irregular schedules and boundary dates. |
| PAY-03 | Frozen run approval/posting, payment instructions and register-aware correction.              | PAY-02, PST-03, COR-02 | E-08/E-09: no partial payroll posting; old run unaffected by current employee changes.                |
| PAY-04 | AGI/KU artifact profiles, individual/control checks, amendment and delivery state.            | PAY-03, OPS-03         | E-16/E-18/E-19: exact schema and semantic identity; exported, paid and accepted remain distinct.      |
| AST-01 | Evidence-backed asset/deferral register and imported opening carrying basis.                  | IMP-02, FND-03         | E-12/E-14: prior depreciation/recognition retained and control basis explained.                       |
| AST-02 | Complete current schedule/occurrence slice and atomic posting/linkage with future amendments. | AST-01, PST-03         | E-08/E-13: installments conserve basis; no orphan posting or lost posted occurrence.                  |
| AST-03 | Disposal, impairment/estimate profiles, reversals and register controls.                      | AST-02, COR-02         | E-09/E-13: exact gain/loss/basis and immutable historical schedule.                                   |
| FX-01  | Versioned rate sources, exact conversion and missing-rate policy.                             | FND-03, IMP-01         | E-02/E-06: exact directional conversion; missing/stale rate blocks affected treatment.                |
| FX-02  | Cross-currency recognition/partial settlement and fee/realized-FX conservation.               | FX-01, COM-03          | E-13: original/payment/book currencies and final residual reconcile independently.                    |
| FX-03  | Period remeasurement/reversal and valuation report controls.                                  | FX-02, END-03          | E-07/E-14: stable selected item set, no duplicate valuation and correct later settlement.             |

Payroll, assets and VAT can progress independently after their foundations; none is falsely dependent on a finished module merely because they share P5. Full-company close depends on whichever rows its reviewed inventory requires. Every activated profile needs both functional proof and current domain/source review; a synthetic schedule or example tax calculation cannot serve as blanket parity.
