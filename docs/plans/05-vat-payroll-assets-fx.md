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

Snapshots include all bounded retained components, including unknown, stale, foreign, unsupported and outside-interval exclusions. They are accountant review artifacts, not VAT returns, ledger-control reconciliations or source-completeness certificates. See [implementation and integration boundaries](../../apps/api/docs/EXPENSE-TAX.md) and the [pre-implementation risk/acceptance record](../../apps/api/docs/EXPENSE-TAX-RISKS.md). Shared composition and native/runtime validation remain root-owned; source presence does not complete VAT-01's legal or proof gates. Existing asset schedules are unchanged.

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

[Subledger controls](../../apps/api/docs/SUBLEDGER-CONTROLS.md) adds forward1500: immutable acquisition/imported carrying bases linked to existing posted lines, and exact declared-account GL snapshots. Gross cost, prior accumulated recognition and remaining carrying amount are retained separately. Missing/reversed bases, occurrence gaps, all ledger contributions and offsetting unexplained rows remain visible. A clean selected-account difference is not complete source coverage or legal depreciation approval.

Forward1510 binds the whole control dependency into closing and accountant-review-v3 artifacts. Missing bases and unavailable complete controls remain mandatory blockers; new bases or report inventories stale earlier approval scopes without rewriting their bytes. API/MCP/routed UI composition is connected in source. Both migrations remain unapplied and runtime-unverified. Forward1800 now captures linked basis authority on native preparations and checks it during shared validation and physical posting. Known generic occurrence and correction-lineage replacements cannot borrow that authority; genuine full reversals remain separate. Existing standalone synthetic schedules keep their interpretation. This source integration and its routed schedule UI remain runtime-unverified.

## Foreign currency

`ExchangeRateObservation` records source, retrieval and effective dates, currency pair/direction, exact rate, scale and source evidence. `ValuationPolicy` specifies rate-date selection, source hierarchy, precision, rounding and fallback/refusal. No missing rate is silently replaced with 1 or a nearby convenient date. A manual reviewed rate is a distinct evidence-backed decision.

Retain original currency amount, original rate/basis and book-currency carrying value at recognition. Settlement releases the correct carrying portion and records cash, fees and realized FX explicitly. Partial allocations retain both original-currency capacity and book-currency release; the final residual follows a declared exact policy so rounded pieces conserve the original carrying value.

Period remeasurement selects eligible open monetary items from a fixed snapshot, computes new book values and unrealized FX under a reviewed policy, seals the affected item set and posts the revaluation/required future reversal with stable occurrence identities. A new settlement or rate/policy revision stales the proposal. Never revalue a historical immutable voucher in place.

The FX review UI shows source amount/currency, carrying amount, selected rate/source/date, calculated settlement/revaluation, fees and residual. Per-currency registers reconcile to book-currency control accounts through recorded conversion effects; summing unrelated currencies is never presented as a meaningful balance.

### Manual exchange-rate review subset (implemented source; runtime unverified)

[Manual exchange-rate reviews](../../apps/api/docs/EXCHANGE-RATE-REVIEWS.md) adds forward1900:
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
| FX-01 | Versioned rate sources, exact conversion and missing-rate policy.                             | FND-03, IMP-01         | E-02/E-06: exact directional conversion; missing/stale rate blocks affected treatment.                |
| FX-02 | Cross-currency recognition/partial settlement and fee/realized-FX conservation.               | FX-01, COM-03          | E-13: original/payment/book currencies and final residual reconcile independently.                    |
| FX-03 | Period remeasurement/reversal and valuation report controls.                                  | FX-02, END-03          | E-07/E-14: stable selected item set, no duplicate valuation and correct later settlement.             |

Payroll, assets and VAT can progress independently after their foundations; none is falsely dependent on a finished module merely because they share P5. Full-company close depends on whichever rows its reviewed inventory requires. Every activated profile needs both functional proof and current domain/source review; a synthetic schedule or example tax calculation cannot serve as blanket parity.

## Backend continuation: retained amendments

- **AST-02 subset:** forward `3100-subledger-schedule-amendments.sql` adds an
  operator-reviewed future-date amendment for the complete unposted suffix of a
  linked-basis synthetic schedule. Amounts, accounts, occurrence identities, residual
  and posted history stay unchanged. Both old and replacement suffix dates must be
  future and their periods open. The revised schedule digest invalidates pending
  posting authority through the existing shared and physical posting guards; native
  re-preparation requires fresh approval. Controls accept the retained basis lineage
  without rewriting saved artifacts. Forward4000 now adds explicit remaining-amount
  estimates as described below. Forward6100 extends that command with explicit future
  installment-count changes; forward4200 adds a separate no-proceeds disposal profile.
  Impairment and legal lifetime/method policy remain separate work. See
  [the date-amendment boundary](../../apps/api/docs/SUBLEDGER-SCHEDULE-AMENDMENTS.md).
- **VAT-04 subset:** forward `3300-vat-draft-amendments.sql` compares exact later
  same-period synthetic drafts and retains an evidenced operator review of their
  relationship. It preserves fact revisions, assessment/exclusion lineage and exact
  contribution/box deltas; unavailable reported amounts remain null. Review requires
  the exact impact digest and current replacement basis. Successful exact-key replay
  and historical reads preserve both original drafts and the saved review. This is an
  internal amendment, never a filed return or new tax calculation. See
  [VAT amendments](../../apps/api/docs/VAT-AMENDMENTS.md).

Both slices are connected to their existing API groups. Authorized read/compare
operations remain available through shared MCP capabilities; human amendment review
is operator-only REST. Migrations are unapplied and SQL/runtime behavior remains
unverified. No tests or legal/company profiles were added.

Forward `3700-vat-fact-withdrawals.sql` adds permanent, evidenced operator withdrawal
of an erroneous VAT fact identity. New revisions refuse; successful existing command
replay and all retained history remain. Withdrawal metadata participates in the current
basis digest. New `vat-return-draft-v2` calculations retain and explicitly exclude the
withdrawn observation, while active corrected facts can reuse its source/line claims.
Sealing refuses an included withdrawn fact. Saved v1/v2 drafts and amendment comparisons
remain readable without recalculation. Existing closing/review dependency digests stale
through the changed VAT basis; no legal or filing readiness is gained. See
[withdrawal boundaries](../../apps/api/docs/VAT-FACT-WITHDRAWALS.md). This migration also remains
unapplied and runtime-unverified.

### Tax-account statement controls and closing dependency

Forward3800 retains operator-reviewed synthetic tax-account statements and stable event
identities with exact signed opening/movement/closing conservation. Saved control artifacts
include complete selected-account ledger history and expose gaps, overlaps, unknown
classifications and unmatched rows. They do not recognize taxable activity or claim complete
reconciliation. [Tax-account scope](../../apps/api/docs/TAX-ACCOUNT.md) records the actual bounds.

Forward3950 includes statement/control inventories in the existing VAT dependency owner,
without changing VAT fact/draft count meanings. Known tax-account records block an
inapplicable tax-family claim and stale closing/accountant dependencies. Zero differences
cannot satisfy unavailable tax coverage. Historical artifacts stay readable. See
[closing integration](../../apps/api/docs/TAX-ACCOUNT-CLOSING-DEPENDENCIES.md).

### Explicit remaining-basis schedule estimates

Forward4000 reuses the existing immutable schedule revision owner for evidenced operator
amendments under `explicit_remaining_minor_v1`. Gross/imported carrying basis, accounts,
occurrence count and identities stay fixed. Posted and genuinely reversed prefix history
remains unchanged. Net recognized amount plus explicit positive future installments and
nonnegative residual must equal the retained carrying cost. Correction replacement lineage
cannot fund a new estimate. Both old and new suffix dates must be future/open; new dates
follow prefix reversals. Changed captures stale old posting authority through the existing
kernel and physical guards. Later reversals block further recognition until reviewed again;
normal installment posting preserves peer captures.4000 itself does not change count or
add disposal. The narrower additional6100 count-change and4200 disposal profiles are described
below. Zero-value cessation and real legal depreciation policy remain unsupported. See
[estimate boundary](../../apps/api/docs/SUBLEDGER-ESTIMATE-AMENDMENTS.md).

These migrations remain unapplied and runtime-unverified. Source review is not proof of
SQL compilation, concurrent execution, financial outcomes or actual-company readiness.

### Exact tax-account matching

Forward4100 adds evidenced operator match/unmatch of one whole known-classified source
event to one existing posted line with the same date, account, currency and signed amount.
Read-only basis previews confer no authority. Immutable history and a private reservation
projection enforce unique event/line capacity; deferred constraints require an active
reservation or immutable unmatch, never both. Symmetric bank/owner/commerce guards prevent
cross-owner reuse. A matched voucher must be explicitly unmatched before correction.

New v2 controls consume only usable effective pairs, retaining invalid, unknown and unmatched
items plus complete source/GL controls. V1 bytes stay unchanged. Match history and effective
state participate in control/closing/accountant currentness through the connected tax-account
dependency owner. This does not create payments, taxable facts or journals; aggregate or
item agreement still does not establish full source coverage or financial-close readiness.
See [matching scope](../../apps/api/docs/TAX-ACCOUNT-MATCHING.md). Migration4100 remains unapplied
and runtime-unverified.

### Synthetic no-proceeds disposal

Forward4200 adds operator prepare/approve/execute for the explicit
`synthetic_no_proceeds_asset_disposal_v1` profile. It reuses the native journal kernel
and requires represented gross controls, one separate accumulated control, intact basis
and unambiguous effective recognition history. The exact journal releases gross cost and
accumulated recognition, with remaining carrying value charged to an explicit non-control
loss account. Known bank, commerce, owner and tax-account controls cannot be disposal
accounts. Deferred enforcement requires the journal and disposal register consequence to
commit together; generic execution or known correction lineage cannot bypass the owner.
Disposed schedules preserve history, refuse future recognition/amendment, and participate
in actual control and closing dependencies. Full disposal correction, nonzero proceeds
and real legal/tax treatment remain unsupported. See
[disposal boundaries](../../apps/api/docs/SUBLEDGER-DISPOSALS.md). This financial source path
has not been executed or accepted through runtime/concurrency proof.

### Expense-source withdrawal and linked VAT exclusion

Forward4500 retains evidenced permanent operator withdrawal without changing historical
source/review/snapshot bytes. New expense assessment excludes withdrawn sources and
explicit active source-component/shared-voucher ambiguity. It does not infer missing
line identities or release accounting capacity. The current expense basis carries
withdrawal identity; retained source counts remain truthful and active review counts are
separate. Linked VAT observations also expose withdrawal, refuse new revision admission
and are excluded by the new v3 calculator. Saved v1/v2/v3 drafts remain readable and
comparable. See [withdrawal boundaries](../../apps/api/docs/EXPENSE-TAX-WITHDRAWALS.md).
4500 is source-integrated. Independent review found a missing SQL sealer exclusion;
the owner fixed it and a fresh-source recheck confirmed that withdrawn expense links
require exclusion, null contribution and the explicit blocker. No remaining blocker was
found in that bounded source review. Runtime proof remains open.

### Financial FX feasibility boundary

Source inspection of1900/2300 and current commerce owners found no selected financial
consumer for conversion reviews. Existing invoice/allocation capacity represents one
book-currency amount, not paired foreign obligation and book carrying amounts. FX-02/03
was deferred at that checkpoint pending explicit monetary-item/capacity and effect-policy
choices. [ADR 0008](../adr/0008-financial-fx-vat-impairment.md) now adopts those choices; implementation and proof remain open.
The [financial FX feasibility review](../../apps/api/docs/FX-FINANCIAL-FEASIBILITY.md)
records exact source owners and the missing decisions. This is not a new FX architecture
decision and does not change existing commerce meaning. No speculative financial register,
settlement posting or valuation artifact was added.

### Retained VAT fact membership

Forward5000 extends the existing fact read with saved draft and amendment references for
that exact fact identity. Included and excluded captured assessments, revision/digest,
engine/interval and retained amendment changes stay version-specific; the reader does not
recalculate them or infer a legal amendment obligation. Complete500-draft/500-amendment
inventories and an8MiB whole-response bound refuse rather than truncate. Existing fact
history/withdrawal fields remain. See [VAT fact lineage](../../apps/api/docs/VAT-FACT-LINEAGE.md).
The source is integrated. Independent source review found no actionable blocker in exact
membership, saved-version compatibility, disclosure and complete-read bounds. Backend and
web type checks passed. Runtime proof remains open.

### Expense snapshot source membership

Forward5200 adds an optional exact source filter to the existing expense snapshot list.
A fixed25-snapshot window is scanned before membership filtering, so empty items can still
have a continuation. The cursor binds scope, source and captured ceiling; scan progress is
explicit. Saved v1/v2 assessments/revision/review/withdrawal identities are copied without
live recalculation. Previously absent withdrawal metadata stays absent. Unfiltered requests
keep0710 summaries and cursors. See
[expense snapshot membership](../../apps/api/docs/EXPENSE-SNAPSHOT-MEMBERSHIP.md).
Source is integrated and backend type checks pass. Independent source review found no
actionable blocker in sparse paging, cursor isolation or historical assessment semantics.
Runtime proof remains open.

### Cross-register line-reference disclosure

Forward5300 extends the public schedule read with exact active tax-match references on
its retained basis lines. Forward5400 extends the public tax-match read with its exact
retained subledger basis reference, including historical unmatched reviews. These are
factual links outside immutable bodies, not a conflict finding, role classification or
new capacity rule. Private matching/eligibility, posting-basis, control/dependency and
correction owners remain unchanged. Tax matching keeps its original active/usable values;
its new detail schema is limited to the public getter so saved control/list decoding stays
unchanged. See [schedule references](../../apps/api/docs/SUBLEDGER-TAX-MATCH-REFERENCES.md)
and [tax-match disclosure](../../apps/api/docs/TAX-ACCOUNT-SUBLEDGER-DISCLOSURE.md).
No universal account-role exclusivity policy was selected. Both source paths are
integrated; source/static review is separate from unperformed runtime verification.

### Explicit future installment-count changes

Forward6100 extends the existing operator estimates command, without a new endpoint or
financial policy. Different-count requests emit `remaining_lifetime_v1`: every replacement
future occurrence receives a fresh never-reused key, while the posted/full-reversed prefix,
original carrying basis and accounts remain unchanged. Every old suffix entry, including
removed ordinals, and every replacement must be future/open and unposted. Net recognized plus positive future amounts plus residual
must equal retained carrying cost. `usefulPeriods` is the current slot count, not a legal
useful-life recommendation.

The physical revision guard independently checks the whole transition. Preparation display
matches a preparation's pinned revision identity, not ordinal alone. All-generation ordinal
attempts remain capped at100;120 current occurrences and20 revisions permit at most2400
retained identities. Existing1800/4200 posting guards stale prior captures and protect retired
keys. Same-count/date amendments retain current keys; disposal still freezes revisions.

Root and two independent source reviews found no blocker. Backend/scripts/contracts/Swedish
jurisdiction and web type checks passed; targeted contract lint reported zero warnings/errors.
No tests, SQL compilation/application, runtime, concurrency or actual-company validation were
performed. Fully posted reopening, zero cessation, impairment, proceeds and automatic/legal
lifetime policy remain unsupported. See the [complete contract and handoff](../../apps/api/docs/SUBLEDGER-ESTIMATE-AMENDMENTS.md).

### Interim impairment remains a contract decision

The [impairment feasibility review](../../apps/api/docs/SUBLEDGER-IMPAIRMENT-FEASIBILITY.md)
identifies an actual posting/control gap, but existing recognition and terminal disposal
roles do not select an interim impairment credit role. Credit/loss account eligibility,
atomic future reallocation versus an explicit recognition block, and correction/repetition
policy must be selected first. An amount-only annotation or unrelated manual journal would
leave controls and disposal wrong; neither is an implementation substitute. No impairment
profile, migration, endpoint or posting authority has been added. Other backend work continues.

### Resolve an unknown tax-account event

Forward6700 adds an evidenced operator resolution for an originally `unknown` retained event.
The event can receive one existing non-unknown classification; known events cannot be revised
through this command. Original statement/event bytes, dates, amounts, accounts and source
identity stay unchanged. A scoped GET and read-only MCP capability expose the original event,
its resolution and effective classification. Resolution mutation is operator-only REST.

Matching uses the effective classification and pins the immutable resolution reference without
changing capacity, unmatch or correction guards. New v3 controls use effective unknown IDs and
capture compact resolution references. Relevant control/closing dependencies change when a
resolution exists; untouched accounts/books retain their prior dependency shape. Old controls,
statements and successful-key replay remain historical. No financial posting, legal role,
coverage or financial-close readiness is inferred.

The one-shot inventory is bounded at1000/book. Backend/web type checks and targeted lint passed;
SQL compilation/application and runtime behavior remain unverified. See
[classification resolution](../../apps/api/docs/TAX-ACCOUNT-CLASSIFICATION.md).

Forward6800 adds a live unresolved-event worklist for the classification command. A scoped
REST GET and read-only MCP capability scan50 retained event identities before filtering their
effective classifications. Bound book/account cursors advance by the last examined event;
empty result pages may still continue, and resolved anchors remain valid. No control artifact,
receipt or financial state is created. This is not a frozen inventory or completeness claim.
Backend/contracts/jurisdiction type checks and targeted lint pass. The initial web check
encountered separate invoice UI pagination edits; the follow-up shared web check passed without
changes to those files by this slice. SQL and runtime behavior remain unverified.

### Synthetic VAT control reclassification slice (source present; runtime unverified)

Forward `9120-vat-control-reclassifications.sql`, `9130-vat-reclassification-dependencies.sql` and the later tax-account compatibility guard `9170-vat-tax-account-claim-guard.sql` add the synthetic-only `vat_control_reclassification_v1` path. A saved v3 SEK scale-2 synthetic draft resolves to one synthetic reporting obligation and prepares an exact account-role-bound plan. The plan reverses only evidenced output/input VAT-control contribution lines, posts the signed settlement-control line when the exact net is nonzero, and records an explicit no-effect result for an all-zero basis. Reported kronor and residuals remain visible but are not posted or treated as an assessment.

The SQL path pins the draft, current relevant facts, source voucher/line state, reviewed account roles, period and dependency digest without using the whole-book sequence as its reclassification currentness authority. Approval is operator-only; execution can use a current operator approval, commits the journal/effect/receipt atomically, prevents a new-key duplicate per obligation, and recovers the original command by idempotency key. Generic correction, taxable-source admission and tax-account matching cannot consume the owned effect or its source lines. VAT dependencies now retain bounded reclassification and amendment inventories for closing/accountant review. The shared contracts, HTTP handlers, read-only MCP capabilities and Tax workspace are source-integrated in `packages/contracts/src/vat-returns.ts`, `apps/api/src/transport/http/routes/vat-returns.ts`, `apps/api/src/application/capabilities.ts` and `apps/web/src/components/vat-returns/reclassification-panel.tsx`.

This slice is not runtime proof, legal VAT support, assessment, payment, filing, amendment or a complete tax-account control. SQL application, PostgreSQL/Workerd execution, browser interaction, positive/negative/zero/stale/duplicate/recovery scenarios and real-company evidence remain open. Assessment and VAT-04 amendment deltas are separate follow-up work.

## Adopted financial-contract delivery

[ADR 0008](../adr/0008-financial-fx-vat-impairment.md) owns the adopted semantics and supersedes earlier open-design statements for these selected profiles. The [retained proposal](evidence/financial-contract-proposal.md) supplies detailed examples and acceptance scenarios. Existing packet IDs and engineering dependencies remain unchanged; these are bounded stages within them, not a second backlog.

| Stage / canonical packets | Owner and complete outcome | Observable exit / follow-up |
| --- | --- | --- |
| VAT reclassification — VAT-03 | VAT/SQL owner: obligation identity, prepare/approve/execute/read, period contribution roles, control reclassification and receipt recovery. | Positive/negative/zero nets, new-key duplicate refusal, same-key recovery after sequence advance and symmetric taxable-role exclusions; no half journal/obligation effect. Then assessment links and VAT-04 delta amendments. |
| FX recognition/full settlement — FX-02 | Commerce/FX owner: synthetic foreign receivable recognition, paired capacity, book-currency cash settlement, controls and latest-unconsumed correction. | Both balances reach zero; journal/register/receipt commit together; lost response recovers; old invoice interpretation remains unchanged. Then payables, partial settlement and separately evidenced fees. |
| FX remeasurement — FX-03 | Commerce/FX owner after financial capacity: incremental valuation and report/control consequences. | Valuation plus later settlement recognizes only incremental remaining FX; original units stay unchanged; backdated/consumed corrections refuse until supported. No automatic next-period reversal. |
| Impairment — AST-03 | Subledger owner: impairment journal/effect plus complete revised suffix, reads, occurrence guards, controls, closing, disposal and immediate owned correction. | The ADR witness yields carrying 600/future 550 and correct disposal; stale plans refuse; failure commits neither half; prior snapshots stay unchanged. Consumed-history and economic reversals remain explicit follow-up scope. |
| Payroll foundation → calculations — PAY-01/PAY-02 | Payroll owner: qualify existing 9050 records, privacy/revision semantics and required typed inputs; build the chosen dated calculation profile. | Scoped history/recovery and independently expected selected calculations; no assumption that an employee record means payroll is calculated, paid or declared. |
| Actual-company VAT — VAT-01/VAT-02 | VAT/jurisdiction owner: implement and qualify real contribution/calculation/reporting policy before enabling actual-company totals. | Actual supported and unsupported cases, lineage and independent controls; adding company details or removing migration 4500's refusal alone cannot pass. |

Parallel domain work is possible after reconciling shared interfaces, with one integrator owning shared posting-purpose, correction, contract-export and migration composition. Reserve forward migration IDs from the live tree. Impairment must coordinate with any AST-02 schedule work; FX must coordinate with commerce capacity work. Do not overwrite existing applied migrations or bypass generic correction fences.

Before each implementation, inspect the effective function/trigger chain and enumerate the acceptance failures in the proposal. Use existing authorized checks; new tests/fixtures retain D-09 authorization. Retain repeatable fixed-revision evidence for executed financial outcomes. This planning task changes no runtime code, tests or migrations and claims no new runtime result.
