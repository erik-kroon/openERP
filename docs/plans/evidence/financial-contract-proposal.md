# OpenERP: resolving the financial-contract blockers

Status: proposed architecture decisions for the product owner to adopt. Not committed to the repository, not an authorization to execute financial actions and not a certification of accounting correctness.

Repository checkpoint: `erik-kroon/openERP@c04dbde62c45e3b9851d5e61454b8e9dad552dc7`.

## 1. Executive decision

Keep the current Effect application boundary, exact paired monetary fields and PostgreSQL authority. Resolve the three financial semantics explicitly rather than commissioning more feasibility reviews of the same questions.

Adopt the following target contracts:

| Area | Proposed decision |
| --- | --- |
| Financial FX | A versioned monetary-item extension owned by commerce, with original-currency quantity and book-currency carrying value conserved together. Settlement and remeasurement have named financial effects and atomic register consequences. |
| VAT | Separate VAT control-account reclassification, authority assessment and treasury transfers. One reporting obligation has many immutable return versions. Do not use equal amounts as settlement identity. |
| Impairment | Preserve original cost. Use an explicitly selected impairment contra role distinct from ordinary depreciation. Commit impairment and the complete revised future schedule atomically. |

These decisions resolve specified design questions if adopted. They do not make code implemented, tests passed, Swedish rules activated or a company ready to close.

## 2. What the current repository actually establishes

`docs/open-decisions.md` and the three financial feasibility reviews explicitly leave FX, VAT settlement and impairment open. Their distinction between missing semantics and missing external facts is justified. [S1-S4]

Some surrounding descriptions are older than the code:

- `9050-employee-foundation.sql` now declares employee identities and immutable employment/work/opening revisions. `PAYROLL-FOUNDATION.md` describes its routes and interface but explicitly withholds runtime proof. Payroll should not be restarted from an assumption that no input-record foundation exists. Its remaining questions include input-schema adequacy, dated calculation rules, execution and verification. [S10-S11]
- `packages/domain/src/ledger.ts` includes a narrow `legal_ar_recognition` variant as well as the generic synthetic adjustment/reversal action. Older statements that all posting purposes are only adjustment/reversal need qualification. Do not widen generic manual-journal authority to add the new financial workflows. [S7]
- The inspected `seal_vat_return_draft` replacement in migration 4500 rejects actual-review totals and requires legal/readiness flags to remain false. Supplying company information cannot turn that reviewed code path into an actual-company VAT calculation. A real-profile implementation is a separate deliverable. [S8]
- `vat_return_basis_body` in the same migration includes the entire book sequence. A settlement posting can therefore stale the draft that motivated it even if taxable facts are unchanged. A new financial operation must handle this explicitly. [S8]
- The inspected schedule getter calculates remaining amount from cost less ordinary posted occurrences, unless disposed. It has no impairment term. The documented impairment issue therefore has a concrete read-side consequence as well as a posting concern. [S9]

This is a targeted source review. It is not an assembled-schema audit of every migration and no upstream runtime test was executed. Later function replacements and trigger composition must be checked when implementing.

## 3. Shared constraints for all three decisions

Preserve current sealed records and `openerp-c14n-v1` interpretation. Retain the existing exact `debitMinor`/`creditMinor` wire format and its bounds. Semantic extensions receive explicit versions; old records are not rehashed or reinterpreted. [S5]

Use named domain operations, not a new general financial-effect language. Effect owns preparation and calculation. Named SQL transitions own final validation, the financial transaction, related register effects and receipts. Do not implement the accounting calculator independently in both TypeScript and SQL. SQL still independently enforces essential conservation and authority constraints. [S5]

Reuse the actual credential/membership lock prefix and book serialization order. Under that boundary, authenticate current access, recover a successful identical request and only then apply freshness conditions for new work. A lost response must recover the original receipt even if the underlying rate or schedule later changes. Revoked access still prevents unauthorized recovery. [S5]

For a new operation, approve an exact saved plan containing financial and register consequences. Commit those consequences and its receipt together. Generic posting or generic reversal must not be able to apply only the journal half of an owned operation.

Preserve evidence separately from recognition and capacity. A document can support several compatible assertions. An already consumed monetary capacity cannot be spent twice. Do not invent a global rule that every journal line may appear in only one register: the repository expressly does not establish that invariant. Choose incompatible roles at the particular domain boundary and enforce them in both admission directions. [S1]

Keep five independent statuses in task records: design adopted, implementation present, runtime verified, company applicable and external outcome verified. A blocker must state which of those it prevents.

## 4. Proposed FX contract

### 4.1 Ownership

Commerce owns the monetary item and its settlement capacity. FX owns rate observations and pure conversion/valuation policy, not a competing receivables register.

Introduce a versioned commerce monetary-item representation for newly admitted foreign-denominated obligations. It may be implemented as a companion relation, but it must have one commerce owner and one allocation authority. It is not an independently mutable FX balance beside existing allocations.

The logical shape is:

```text
MonetaryItem
  bookId + itemId
  source invoice/obligation identity and revision
  side: receivable | payable
  originalCurrency + originalScale
  originalAmountMinor
  bookCurrency + bookScale
  recognitionBookAmountMinor
  recognitionVoucherId + controlLineId
  recognitionRateObservationId and revision
  valuationPolicyId and version
  financialProfileId and version
```

Current remaining amounts are projections of immutable recognition, settlement, credit/correction and remeasurement effects. Cache a projection only if the owner can rebuild and reconcile it. Do not let callers directly overwrite balances.

An existing `synthetic_invoice_v1` retains its book-currency meaning. A rate review does not turn it into a EUR/USD obligation. New representation and allocation paths must reject attempting to attach a second economic identity to an already recognized invoice. A migration/adoption path for an existing foreign item needs explicit original-currency evidence and a no-duplicate-recognition rule.

Mixed-register reads need a discriminated amount model. Do not expose a foreign invoice's face amount as a book-currency `amountMinor` in an old API. Preserve the old subset or reject the broader query until its client supports the versioned representation.

### 4.2 Financial capacities

For a supported positive outstanding item, define:

```text
Q = remaining original-currency minor units
B = remaining book-currency carrying minor units
q = original-currency minor units being settled, 0 < q <= Q
b = book-currency carrying value released
```

Select a named initial allocation policy:

```text
b = B                                    when q = Q
b = round_half_up_nonnegative(B * q / Q)  otherwise

Q_after = Q - q
B_after = B - b
```

Use exact integer/rational calculation and record the allocation input and rounding residual. The final settlement releases the exact remaining carrying amount. No arbitrary balancing plug is permitted.

The partial allocation calculation uses the current carrying value, including committed remeasurements, not always the original invoice recognition rate. A zero carrying release caused by sub-minor rounding is represented at the register level without manufacturing a zero journal line.

A multi-leg settlement consumes capacities under one serialized snapshot. It cannot independently round each leg against the same full starting balance. Duplicate requests recover the same receipt; a different request key cannot re-consume the same settlement source occurrence.

### 4.3 Realized FX and fees

First support settlement into book-currency cash. Let `K` be gross book-currency consideration attributable to the obligation before separately identified bank fees.

```text
receivable realized gain = K - b
payable realized gain    = b - K
```

A negative gain is a loss. The selected account-role profile determines control, cash, gain and loss accounts. Do not infer those roles from an account-number prefix or a UI category.

Illustrative receivable settlement, all posting values in SEK:

```text
EUR 100 receivable has carrying value 1,100
Gross settlement consideration is 1,120
Bank withholds a separately evidenced fee of 10
Cash received is 1,110

Debit cash                     1,110
Debit bank fee                    10
Credit receivable              1,100
Credit realized FX gain            20
```

The EUR 100 obligation is fully consumed. The SEK fee is not foreign-currency principal and is not silently netted into FX gain/loss.

The atomic effect includes the journal, original-currency release, book carrying release, fee allocation, payment-source identity and receipt. Existing bank matching can reference that financial effect; it cannot duplicate it.

A foreign-currency bank balance needs its own monetary-item carrying policy. Do not sneak that into the first book-currency-cash settlement workflow by treating foreign cash as if it were SEK.

### 4.4 Rate selection and history

Rate observations remain directional and exact. Missing dates or unsupported sources cause a named refusal. There is no implicit rate of one, silent inversion or current-date conversion of a historical event.

The application must distinguish recognition rate, actual settlement consideration and reporting-date valuation. Known actual cash amounts should not be replaced with a public reference rate merely for convenience.

A later withdrawal of a rate observation makes it unavailable for new decisions and creates an impact case for affected historical decisions. It does not rewrite a committed carrying value. Settlement can release the historically recorded carrying basis while using its own current payment evidence; correction of the earlier recognition is a separate owned operation. A reviewed material defect can block affected finalization without deleting history.

### 4.5 Remeasurement decision

Choose incremental carrying-value adjustments as the first remeasurement policy. Do not automatically reverse every valuation next period.

At a pinned reporting cutoff, capture all eligible open monetary items and their current paired capacities. For each item:

```text
T = exact policy-rounded reporting-date value of remaining foreign units
D = T - B
```

For a receivable, positive `D` increases its carrying debit and creates an FX gain. For a payable, positive `D` increases its carrying credit and creates an FX loss. Original units do not change.

Future settlement consumes the updated `B`. A later remeasurement uses the then-current outstanding item, not the historical full face amount. This avoids counting the same economic gain twice.

Record realized/unrealized attribution in the owned effects. Do not reclassify prior-period profit by rewriting closed-period vouchers. Additional within-period presentation transfers, where required by the selected reporting policy, must be explicit effects rather than hidden recalculation.

Choose uniqueness at the economic operation level: book, valuation policy, cutoff and selected item revision. A same-key retry is recovery. A new valuation proposal for an unchanged basis cannot duplicate the previous adjustment.

Backdated settlement into an already valued interval is not a free mutation. Re-evaluate the affected valuation population and create a correction plan or refuse until that correction path exists. The first implementation can forbid backdating across an effective valuation cutoff.

BFN's reviewed K2 guidance includes closing-rate treatment for short-term foreign receivables and foreign liabilities, with exceptions such as forward-covered portions. The general carrying model supports that direction, but activating a company profile still needs the applicable version and treatment. [P1-P2]

### 4.6 Delivery boundary and corrections

The first FX packet should complete one synthetic customer receivable and full settlement into book-currency cash without fees. It must include recognition ownership, settlement posting, receipt recovery and register reconciliation. This is a genuine vertical slice, not the whole FX-02 package.

Follow with payables, partial settlement and evidenced fees, then FX-03 remeasurement. Foreign cash, netting, hedges, credit impairment and more complex instruments stay explicitly unsupported until their own semantics are implemented.

Never apply existing no-journal unallocation to a settlement that also recognized FX. An FX settlement correction reverses the journal and both capacity consequences together. Initially permit the latest unconsumed settlement only. Later consumed history, valuation or credits require a dependency-aware correction plan; block a bare reversal in the meantime.

### 4.7 Required acceptance scenarios

Recognition and settlement cannot occur without their register effects. EUR units and SEK carrying value both end at zero on full settlement. Partial settlement and final residual conserve the starting carrying amount. Fees never change original obligation units. A later rate withdrawal does not change posted historical values. Valuation followed by settlement recognizes only the incremental gain/loss after valuation. Legacy invoices remain byte- and meaning-compatible. Same-key recovery succeeds after the state advances; a new-key duplicate financial effect fails.

## 5. Proposed VAT contract

### 5.1 Three different economic operations

Do not implement one ambiguous `settle VAT` action.

Separate:

1. VAT control-account reclassification into the reporting-period liability/receivable.
2. Recognition or evidenced linkage of the authority's VAT assessment on the tax account.
3. Cash transfer between the bank and tax account.

Submission and acknowledgement are separate documentary states, not one of these accounting operations.

Skatteverket distinguishes assessed tax/credit entries from payments. Its published guidance also states that payments are generally applied to the total tax-account debt, not earmarked to a particular tax. An internal payment plan may express intent, but cannot prove that one bank deposit paid one particular VAT return. [P3-P4]

### 5.2 One reporting obligation, many immutable versions

Create an owned reporting-obligation identity scoped to:

```text
book / legal entity
VAT registration identity
jurisdiction and scheme
reporting interval
```

A synthetic registration uses an explicitly synthetic namespace. It is not evidence of real registration.

Multiple saved drafts and filed/amended versions attach to that identity. The identity does not include the draft ID. Two numerically identical drafts cannot create two underlying obligations.

Financial effects link the obligation, selected immutable return version, effect type and source evidence. Current state derives from unreversed effects and adjustments, with unique admission against duplicate application. Do not overwrite a prior financial effect when selecting a newer return.

### 5.3 Select the initial reclassification effect

Name the first effect `vat_control_reclassification_v1`. It transfers the relevant period's recognized VAT-control contributions to the selected VAT settlement control role. It is not a bank payment or evidence of tax-account assessment.

For the current narrow synthetic calculator only, let:

```text
O = saved box10.exactMinor
D = saved box48.exactMinor
N = saved box49.exactMinor = O - D
```

That formula is not the full Swedish return equation. Use it only when the saved profile explicitly excludes the other boxes and every required contribution is supported.

Let `b_i` be the debit-minus-credit signed balance of each selected VAT-control contribution. Require exact agreement between contribution lineage, reviewed account roles and the saved calculation. Do not clear an account's entire live balance containing other periods.

The reclassification posts:

```text
each VAT-control role: -b_i
VAT settlement role:  sum(b_i) = -N
```

Thus positive `N` produces a credit liability; negative `N` produces a debit receivable. Bind the liability-role line or its exact owned effect, not whichever line happens to have an equal amount.

Illustrative positive-net example, in SEK:

```text
Output VAT                              5,000
Deductible input VAT                    2,000
Exact net payable                      3,000

Debit output VAT control               5,000
Credit input VAT control               2,000
Credit VAT settlement control          3,000
```

For a negative net, use the debit side of the settlement role. If the net is zero but nonzero output/input balances remain, clear those balances without creating a zero settlement line. If every contribution is zero, record an explicitly zero-effect resolution receipt instead of a zero-valued voucher.

The named profile must declare permissible account roles and evidence. Account role selection is not inferred solely from BAS numbers. All constituent accounting and obligation effects commit with the receipt.

### 5.4 Assessment and treasury are separate

Let `A` be the signed assessed amount: positive for a VAT charge and negative for a VAT credit. The proposed assessment posting has:

```text
VAT settlement control debit-minus-credit = +A
tax-account control debit-minus-credit     = -A
```

For a 3,000 SEK charge:

```text
Debit VAT settlement control          3,000
Credit tax-account control            3,000
```

A subsequent 3,000 SEK deposit is:

```text
Debit tax-account control             3,000
Credit bank                           3,000
```

The assessment operation requires an explicitly reviewed VAT assessment identity, reporting-period association and underlying authority evidence. An undifferentiated `tax_charge` classification plus a matching amount is insufficient.

When a source-to-ledger tax-account match already exists, link its owned relation instead of reserving the same source and financial capacity again. Evidence reuse and capacity consumption must remain distinct.

Imported existing journals need a reviewed role-adoption workflow with lineage and eligibility checks. Do not mutate an old generic journal's purpose or automatically bless it because it has the right number.

### 5.5 Exact, reported and assessed amounts

Retain three separate values:

```text
exact accounting net N
reported return net under the selected reporting policy
observed assessed amount A
```

The initial synthetic profile uses exact accounting amounts and refuses unsupported differences. Do not infer a settlement rounding policy from the calculator's displayed whole-krona field.

A production policy must state the applicable box-level reporting rule, how reported net is derived and which evidenced residual is posted. An assessment difference may be an amendment, interest, penalty, misclassification or arithmetic error rather than rounding. Do not book all differences to rounding expense.

Amendments calculate a target liability and subtract already applied accounting effects for the same obligation. They do not reapply the full replacement return on top of the original one. Preserve filed payloads and assessment history.

### 5.6 Avoid the draft/settlement currentness cycle

The inspected legacy VAT basis includes `bookSequence`. Posting a settlement advances it. Do not remove that field from existing snapshots or relabel a stale old draft as current. [S8]

For the named posting workflow, validate the saved input basis before execution under the book lock. Commit the effect with a receipt stating exactly which approved input it consumed. That receipt remains valid as historical execution evidence even though a current-book query now has a later sequence. A committed operation is not re-executed merely because its original input is no longer the latest book snapshot.

For subsequent current return checks, introduce an explicitly versioned dependency basis that includes the taxable fact population, contributing voucher/reversal states, evidence withdrawals, profile/rule versions, account-role configuration and reporting selection. Keep ledger/control reconciliation and settlement inventory as distinct dependencies.

A supposedly non-tax effect may only be omitted from the taxable population because the owned operation and source-admission guards establish that role. New taxable sources, corrections, withdrawals and unexplained tax-control movements still invalidate or block the affected assessment. Keep this proof local and do not skip arbitrary ledger changes by convention.

During transition, retain the legacy global-sequence check for old artifacts. A post-commit refreshed review may become the current assessment without changing or reauthorizing the already committed operation.

### 5.7 Symmetric exclusion and completeness

Settlement effects cannot later be introduced as sales/purchase tax facts or expense-tax source effects. Taxable source effects cannot be adopted as settlements. Enforce both directions in the actual source owners and the named financial operation. Include later source revisions and correction ancestry.

Do not block merely attaching supporting evidence. The forbidden behavior is double economic/tax recognition, not two records pointing to the same PDF.

The public capability should say exactly what it accomplished: reclassified, assessment-linked, treasury-reconciled or filed. No generic `paid=true` inferred from an equal bank transfer.

### 5.8 Required acceptance scenarios

Positive, negative and zero nets preserve exact signs. Duplicate drafts share one obligation. The same settlement cannot be applied twice under new keys. Reclassification does not enter taxable totals. Actual assessment differences remain explained or blocked. Payment alone does not assert filing or assessment. The original receipt survives self-induced book-sequence changes. Amendment applies only the remaining required delta. A lost response recovers without a duplicate journal.

Real-company support additionally needs a real VAT profile. Removing synthetic guardrails alone is not implementation.

## 6. Proposed impairment contract

### 6.1 Select separate impairment accounting

For the first profile, use an explicit impairment contra role separate from accumulated ordinary depreciation/recognition, with an explicit impairment-loss role.

```text
Debit impairment loss
Credit accumulated impairment
```

This is a product-model decision, not a claim that every company must use separate physical accounts. The first supported profile requires distinct reviewed accounts. A combined-contra variant can be separately implemented later with its own control equations.

Preserve acquisition gross amount and imported opening recognition. Do not reduce original cost in place, hide impairment as an ordinary installment or borrow the no-proceeds disposal role.

Initially restrict this profile to appropriate depreciable asset schedules. Do not automatically apply it to prepayments, loans, inventory, goodwill or other asset classes with different rules.

### 6.2 Conservation and atomic revision

Use the repository's existing basis notation:

```text
G = original gross basis
O = imported accumulated ordinary recognition
C = G - O
R = effective ordinary recognition after import
I = effective net impairment
S = approved residual
F = remaining ordinary installments

carrying value B = C - R - I
R + I + F + S = C
```

`I` is separate from ordinary `R`. Imported histories with prior impairment need explicitly separated opening evidence or remain unsupported; do not relabel imported ordinary recognition retrospectively.

Commit the journal, owned impairment event and complete approved future schedule revision in one transaction. An impairment amount without a valid new suffix does not post in this initial profile. A first bounded partial case requires positive post-impairment carrying value, at least one positive future installment and a valid nonnegative residual.

The complete suffix and residual are inputs to approval. The model does not infer a new useful life from the impairment amount. Posted ordinary occurrences and their identifiers remain unchanged. Superseded unposted plans become stale.

### 6.3 Worked conservation witness

Using the repository's synthetic minor-unit witness:

```text
G = 1000
O = 100
C = 900
R = 200
S = 50
old F = 650
new I = 100

old carrying = 900 - 200 = 700
new carrying = 900 - 200 - 100 = 600
new F = 900 - 200 - 100 - 50 = 550
```

The resulting check is `200 + 100 + 550 + 50 = 900`.

The following no-proceeds disposal consumes the new carrying amount:

```text
Debit accumulated ordinary recognition    300
Debit accumulated impairment              100
Debit disposal loss                        600
Credit original gross asset basis        1000
```

Leaving disposal unaware of impairment would not complete the feature.

### 6.4 Every consumer changes together

The implementation packet must cover current schedule reads, future estimate conservation, occurrence eligibility, declared-account controls, closing dependencies, correction-impact disclosure and disposal basis/release.

For a control snapshot at cutoff `t`, derive effective impairment from owned effects with explicit accounting date and recorded-at cutoff, consistent with the rest of the report contract. Do not add current impairment to an old snapshot or recompute a retained old report in place.

Under the selected distinct-contra profile, declared controls independently expect gross `G`, ordinary accumulated amount `O + R` and impairment accumulated amount `I`. Unexplained GL movements remain discrepancies even when their net accidentally looks right.

### 6.5 Repetition, corrections and economic reversals

Allow repeated partial impairments through distinct reviewed decisions, each bound to the current basis and schedule. Each must be strictly below the then-current carrying value for this bounded profile. Stable source-decision identities prevent new-key retries from posting the same impairment again.

An erroneous-entry correction and a later economic reversal are not the same operation.

For an immediate error with no dependent recognition, estimate, impairment, disposal or closed-period consumption, an owned correction can atomically reverse the journal and impairment effect and install a new valid future schedule revision. Do not revive an old schedule by mutating its history.

Once later activity consumes the impairment, refuse a generic reversal. A subsequent supported correction must include the dependent register/schedule consequences. The first narrow implementation may return an explicit unsupported correction case, but cannot advertise full impairment lifecycle support until it has a usable correction path for its promised scenarios.

A later economic reversal under an applicable Swedish profile needs separate evidence that the reason no longer exists and the appropriate carrying-value cap. The reviewed K2 guidance calls for future depreciation from the impaired carrying value and restricts reversals by the no-impairment depreciation counterfactual; goodwill has a separate restriction. Consequently, a permanent policy of “impairments can never reverse” is not a complete K2 implementation. [P1-P2]

Do not treat book impairment as automatically tax-deductible. Book valuation, tax basis and tax-return adjustment are separate policy outputs.

### 6.6 Required acceptance scenarios

The witness above conserves the original basis and updates disposal. A stale old recognition plan cannot post after impairment. Failed execution writes neither the voucher nor the schedule revision. Read/control/disposal results agree on `I` at the same cutoff. Repeated impairments preserve original `C` and consume current carrying value. Corrections cannot reverse only the GL half. Economic reversals use their own evidence and cap. Retained prior snapshots stay unchanged.

## 7. What still requires external inputs or proof

A provider credential is needed to exercise the provider environment, not to write an internal state machine. Specification and sandbox access should be sought early because external semantics can change the adapter design. A local fake does not prove a provider behavior.

The operator's concrete input packet should name the provider/product, supported operation, environment, account/application identifiers, authorization/consent, required certificates, scopes and a permitted exercise. Secrets belong in the intended secret mechanism, not in a task document. The resulting proof records what was attempted, what was observed and its exact receipt/status.

Company facts should be an evidence-backed profile: legal identity, fiscal year, accounting method, VAT registration/period, framework applicability, currencies, payroll applicability and a source inventory with coverage. Missing required facts block that company's affected workflow. A field being configured does not itself establish source completeness or reconcile a period.

For payroll, reconcile and verify the existing 9050 foundation first. Freeze required typed work/employment input semantics for the chosen calculation profile; do not make optional free-form fields stand in for required facts. Calculation development can use permitted synthetic fixtures. Real payroll additionally needs real records and applicable rules. [S10-S11]

BFN publishes different applicable guide versions. Rule selection is tied to reporting circumstances, not simply the newest available PDF or the current date. [P1]

## 8. Implementation handoff

After the product owner adopts these decisions:

1. Record the three chosen domain contracts in maintained decision documents and update `docs/open-decisions.md` to distinguish adopted semantics from remaining code, proof and company gates.
2. Reconcile the actual later migration/function/trigger chain for each named owner. Preserve applied migration history and existing sealed artifacts. Allocate forward migration identifiers from the current tree rather than assuming an old proposed number remains available.
3. Implement named prepare/approve/execute/read operations inside the existing Effect/SQL ownership pattern. The operation must produce a useful financial outcome, not only a new review table.
4. Wire all downstream controls and correction guards before marking the operation implemented.
5. Record verification per fixed revision and environment. Do not infer proof from the presence of a test file, a README status or a successful typecheck.

A practical priority is the first complete VAT-control reclassification and obligation lifecycle, the first full FX settlement and the impairment-with-disposal slice. These can proceed in parallel where ownership does not conflict. Payroll can progress against its input foundation while provider and company evidence is gathered independently.

The repository's AGENTS.md restricts new test changes without explicit scope authorization. This document supplies acceptance scenarios, not permission to add tests. Use existing authorized checks and obtain any required permission for missing regression coverage. Do not convert that permission gate into a reason to stop unrelated design or implementation. [S12]

Do not introduce Rust, another authoritative ledger or a new service boundary to resolve these blockers. Their cause is missing financial semantics and lifecycle integration, not language throughput.

## 9. Replace the generic blocker label with an actionable record

Use the existing delivery documents. No new task platform is required.

```text
ID: FX-02-carrying-owner
Class: design
Exact question: which owner conserves original units and book carrying value?
Proposed resolution: versioned commerce monetary item
Owner: product/domain contract owner
Adoption evidence: accepted decision revision
Blocks: financial settlement implementation
Does not block: rate review, source retention, existing book-currency workflows
After adoption: implementation open; runtime proof open; company activation open
```

The recurring status report should say which concrete action advances each gate. Avoid “blocked pending clarity” after the contract is already adopted. Conversely, avoid “unblocked” as a synonym for implemented or production-ready.

## Sources and review scope

All repository paths below are at the pinned checkpoint. Documentation was read as a description of intended/observed behavior, not automatically accepted as runtime proof.

[S1] `docs/open-decisions.md`.

[S2] `apps/api/docs/FX-FINANCIAL-FEASIBILITY.md`.

[S3] `apps/api/docs/VAT-SETTLEMENT-FEASIBILITY.md`.

[S4] `apps/api/docs/SUBLEDGER-IMPAIRMENT-FEASIBILITY.md`.

[S5] `docs/adr/0004-complete-accounting-delivery-contract.md`.

[S6] `docs/plans/README.md` and relevant returned sections of `docs/plans/05-vat-payroll-assets-fx.md`.

[S7] `packages/domain/src/ledger.ts`.

[S8] `apps/api/migrations/4500-expense-tax-source-withdrawals.sql`, especially reviewed lines 245-380; the earlier returned range was partially truncated. Not a claim to have reviewed all later replacements.

[S9] `apps/api/migrations/5300-subledger-tax-match-references.sql`.

[S10] `apps/api/docs/PAYROLL-FOUNDATION.md`.

[S11] `apps/api/migrations/9050-employee-foundation.sql`, lines 1-100.

[S12] `AGENTS.md`.

[S13] Partial returned range from `apps/api/migrations/1700-commerce-allocation-reversals.sql`; read as evidence of allocation/unallocation ownership, not a full effective-schema review.

Pinned repository source root:
https://github.com/erik-kroon/openERP/tree/c04dbde62c45e3b9851d5e61454b8e9dad552dc7

[P1] BFN, current index of applicable guidance versions:
https://www.bfn.se/informationsmaterial/vagledningar/

[P2] BFN, K2 consolidated guidance updated 2025-06-16. Reviewed relevant text and rendered PDF pages 216, 246 and 280 (PDF indices 215, 245 and 279), including paragraphs 10.38-10.39, 13.5 and 17.8. These observations do not establish which K framework/version applies to the user's company:
https://www.bfn.se/wp-content/uploads/vl16-10-k2ar-kons2025.pdf

[P3] Skatteverket, what is registered on the tax account:
https://www4.skatteverket.se/rattsligvagledning/edition/2026.12/325081.html

[P4] Skatteverket, business tax-account guidance and allocation within the tax account:
https://www.skatteverket.se/foretag/skatterochavdrag/skattekontobetalaochfatillbaka/
https://www4.skatteverket.se/rattsligvagledning/edition/2026.12/325092.html
