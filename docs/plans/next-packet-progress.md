# NEXT packet implementation progress

This records selected application-owned NEXT packets by stable packet ID. It
separates **implemented source**, integration and qualification gates from
**verified behaviour**. Local core E2E runs exercise startup, migrations and
selected posting invariants; they do not establish every packet's financial
journey. See [Verification limits](#verification-limits) and the current
[repair record](evidence/latest-landed-review-repairs.md) before relying on a row.

The packet set is a design specification, not authority. It does not grant
database, deployment, real-company or provider permission, and it does not
override `AGENTS.md`, [ADR 0010](../adr/0010-application-owned-accounting-replacement.md)
or [ADR 0009](../adr/0009-effect-mq-background-jobs.md).

## Status

| Packet | Title | Priority | Source | Runtime proof |
|---|---|---|---|---|
| NEXT-01 | Owner-aware case review | P0 | implemented | none |
| NEXT-02 | Capability-specific company admission | P0 | implemented | none |
| NEXT-11 | Separate complete-book SIE4E export | P0 | implemented | none |
| NEXT-13 | Semantic P&L and balance-sheet snapshots | P0 | implemented | none |
| NEXT-20 | Frozen regular-payroll calculation | P2 | implemented | none |
| NEXT-49 | Rule-change impact and evidence-backed obligation fulfillment | P0 | implemented | none |
| NEXT-03 | Domestic purchasing with owned tax recognition | P0 | implemented | none |
| NEXT-26 | Supplier extraction jobs and field-level reviewed merge | P0 | implemented | none |
| NEXT-15 | Legal customer credit notes | P1 | implemented | none |
| NEXT-06 | Owner-paid expenses, reimbursement and funding | P0 | implemented | none |
| NEXT-14 | Original dimension assignments | P2 | implemented | none |
| NEXT-04 | Actual domestic VAT return and controls | P0 | integrated in `082c418`, with subsequent capture/rounding/control repairs | fresh migration and core Worker suite; qualified VAT journey unobserved |
| NEXT-22 | Pre-close tax bridge and INK2/SRU | P1 | source integrated from `next/NEXT-22`; reviewed corporate-tax release still required | fresh migration and core Worker suite; tax bridge/approval/declaration journey unobserved |
| NEXT-29 | Recurring commercial invoice occurrences | P1 | integrated through `0eaad64`, with schema/materialization/interval repairs | core Worker suite; successive recurring issue journey unobserved |
| NEXT-16 | Evidence-aware period preparation | P0 | implemented; see integration evidence below | changed-file lint/types and 23 existing core E2E tests pass; period-work journey proof remains open |
| NEXT-17 | Payable FX and explicit fees | P1 | source integrated from `next/NEXT-17`; bounded synthetic fee-settlement profile | worker-reported constraint probes; financial application journey unobserved |
| NEXT-07 | Supplier paid credits and refunds | P1 | leaf implemented: `@open-erp/domain/supplier-refunds` paid-position derivation, paid-credit compiler over NEXT-03 line releases, and refund-receipt preparation; application posting/refund persistence remain with the purchase/credit owners | packet vectors executed against the pure compiler; HTTP/MCP journey unobserved |
| NEXT-18 | Incremental open-item FX remeasurement | P1 | leaf implemented: `@open-erp/domain/fx-remeasurement` complete-population valuation compiler, execution-time membership check, and settlement-basis carrying helper; valuation posting/effects persistence remain with the commerce FX owner | packet vectors executed against the pure compiler; HTTP/MCP journey unobserved |
| NEXT-30 | Customer unapplied cash, paid credits and refunds | P1 | leaf implemented: `@open-erp/domain/customer-credits` customer position derivation, receipt compiler with advance refusal, paid-credit compiler, credit application and cash-refund preparation; line compilation stays with the legal-credit owner and posting/persistence with the commerce owners | packet vectors executed against the pure compiler; HTTP/MCP journey unobserved |
| NEXT-08 | Payment instruction resolution and replacement | P1 | leaf implemented: `@open-erp/domain/payment-resolutions` proof-qualified no-execution evaluation, capacity release compiler, same-key replay, replacement preparation and late-execution conflict case; fenced release persistence and export remain with the payment-batch/export owners | packet vectors executed against the pure compiler; HTTP/MCP journey unobserved |

The rows above do not classify every other packet as untouched. Resolve its
current branch, owning source and release gates before starting work. A source
merge is not itself a released cross-owner financial contract.

Source dependency edges are now present for NEXT-05 (NEXT-03 and NEXT-04),
NEXT-16 (NEXT-01, NEXT-03 and NEXT-06), NEXT-23 (NEXT-13 and NEXT-22),
NEXT-43/44 (NEXT-13 and NEXT-14), and NEXT-30/46's NEXT-15 dependency.
Each consumer must still resolve its qualification, owner-port and runtime
obligations. NEXT-25 remains the final fixed-revision company rehearsal, not a
substitute for completing those dependencies.

The current repair record links individual review findings to source changes and
actual checks. Its passing existing-suite result covers only those cases;
reviewed tax content, real-company facts and external acceptance remain open.

## What was implemented

### NEXT-11 — Separate complete-book SIE4E export

A distinct application-owned export, not a second movement-transfer path. One
book-scoped transaction captures the complete book and retains the account,
balance and journal-line membership. Exact bytes are then rendered and
re-parsed by the _existing_ inbound SIE parser outside every transaction, and
a short second transaction binds the verified object manifest to the exact
model and renderer. The retained `openerp-sie4i-v1` transaction transfer is
preserved byte-for-byte.

**It refuses rather than approximates.** A book that declares any dimension
effective as-of the capture refuses with `UnsupportedProfile` naming the
dimension and the missing assignment owner; a dimension-free book emits
`#TRANS … {}` and carries an explicit limitation that emptiness means _nothing
is assigned_, not that an assignment was reviewed. No 4E record matrix was
invented: the locally retained source is the SIE 4C edition 2025-08-06, whose
review distinguishes 4E but does not qualify it, so that same edition checksum
is pinned on the capture and only the record families that can be stated are
emitted, declared in `emittedRecords.recordProfile`. Account codes are bounded
to exactly four digits, a nominal account with a non-zero captured opening
refuses rather than lose it silently, and a first fiscal year with no prior
vouchers and no opening set refuses rather than infer a zero opening.

### NEXT-20 — Frozen regular-payroll calculation

A frozen regular-payroll calculation with **no financial effect until a run
executes**. It posts no journal, pays no salary, makes no declaration and
reserves no monthly contribution capacity. A missing, ambiguous, unreviewed or
inapplicable release refuses with `UnsupportedProfile`; no payroll,
contribution or statutory rate is defaulted anywhere.

Eight gaps were reported by the implementing worker and are recorded here
rather than smoothed over:

- The reviewed account-role vocabulary moved out of
  `contracts/company-profiles.ts` into a `contracts/roles.ts` leaf, and the
  rule-release body gained an **optional** payroll section, so every family
  section can name a role without importing another family's contract module.
  This keeps exactly one rule-release authority rather than adding a second
  payroll release table. Rule-release selection still filters on the release
  row's own `family` column, so a payroll-only release **cannot** satisfy
  another family's admission and NEXT-02's `missing_rule_release` refusal is
  unchanged.
- `RoleKind` has no payroll literal. Salary expense and liability have no role
  kind, so `DeductionComponent.destinationRole` can only name the existing six.
  NEXT-21 owns posting and must extend it; no unused literal was added.
- The packet's `EmploymentForCalculation` **cannot be read from the existing
  9050 contract**, whose body is three free-text strings. The typed
  calculation inputs are therefore taken as the command's reviewed input with
  every evidence reference bound by retained evidence. Gross, hours, net and
  payable are all computed; a caller supplies qualified source facts, never a
  calculated amount. There is no independent second review of the input,
  because the packet defines no approval step for prepare.
- The 9107 `opening.obligation` is free text and is bound by requiring the
  employer-contribution obligation selection's reference to equal it, refusing
  otherwise. That is string equality between two independently captured
  values, and it is the strongest available binding without changing the
  9050/9107 contract, which was not changed.
- `roundingByComponentAndReportingLevel` is only partly implemented.
  Per-component rounding and per-profile contribution/accrual rounding exist;
  **reporting-level (AGI) rounding is NEXT-21's and is absent**. The
  calculator version must change before another level is added.
- Committed run reservations are not observable, because that execution owner
  is NEXT-21 and does not exist. The marginal is evaluated over
  `openingBaseMinor + priorFrozenBaseMinor` only. This is recorded in the basis
  field comments; it is a real gap, not a silent zero.
- The payroll family activation is recorded but **not required**.
  `companyActivationId` may be null. NEXT-21's posting may need it non-null.
- No reviewed `rule_releases` row carrying a payroll section ships, so
  `payroll_prepare_calculation` refuses with `UnsupportedProfile` until a
  reviewed release exists. That is designed behaviour, matching NEXT-02.

### NEXT-49 — Rule-change impact and evidence-backed obligation fulfillment

A frozen rule-change impact snapshot records each affected target with its
execution state, classification and recorded decision. Obligation fulfillment
links an obligation to a verifiable link operation with an amendment path, and
the receipt is a **typed same-scope prepared/submitted/accepted outcome** — not
a nonempty reference string standing in for a real one. The packet's
capabilities extend the existing `closing` capability group rather than
creating a parallel owner. The packet's own model carries no amounts: it holds
digests, checksums, effective dates and evidence references, and its SQL
declares no floating or approximate numeric type.

**`DeadlineInput` is a breaking change and this is the most consequential
consequence of the packet.** `jurisdiction`, `statutoryBasis` and
`requiredEnvironment` are now required, and `DeadlineActivity` lost its
`reference` field. This is required by the rule that a statutory input is a
qualified input and never a default, and there is deliberately no compatibility
runtime. But it **invalidates any pre-existing obligation row and any existing
`saveDeadline` client**. No database has ever applied the migration, so the
retained-data consequence is unobserved rather than measured.

Other reported gaps, recorded rather than smoothed over:

- **NEXT-48's authority-outcome owner does not exist.** There is no
  annual-report, filing or Bolagsverket module anywhere in the tree. The
  `authority_outcome` fulfillment variant therefore carries no owner field and
  its resolver returns
  `pending: no_authority_outcome_owner_is_released_to_confirm_this_receipt`.
  **An accepted obligation cannot be satisfied today.** A provider-accepted
  outcome from legal delivery is deliberately not treated as authority
  acceptance.
- The packet's `RuleChangeNotice.oldReleaseId` reference universe is narrower
  than the packet implies. "Query actual retained dependency references"
  resolves in this tree to exactly two real columns:
  `company_activations.rule_release_id` and
  `deadline_obligations.statutory_basis->>'ruleReference'`. `change_sets.plan`
  records a rule release only inside a `CompanyActivationPlan` witness, not as
  a queryable dependency. The two real ones were selected and the migration
  header says so, rather than inventing a wider set.
- **NEXT-04 and NEXT-21 are not wired in as producers.**
  `application/vat-returns.ts` and `application/payroll-foundation.ts` exist but
  are not producers of retained rule-release references, so nothing selects them
  as impact targets and nothing resolves their artifacts as fulfillment
  references.
- Refusal messages are generic where the packet wants precision. `failure(code)`
  in `application/failures.ts` takes no message, so "selection exceeds the
  partition bound" surfaces as the fixed `InvalidJournal` text. The precise count
  is retained in `totalTargets` and returned in the body, not in the error.
  Fixing this needs the shared `failures.ts` owner, which was not taken over.
- There is no owner-side artifact picker. The operator pastes the retained
  sha256; there is no released picker owner and inventing one would fabricate a
  record.
- `decideTarget` does not create the successor obligation. The amend decision
  stores the reviewer-supplied `ProposedSuccessor` basis and the successor is
  created by an explicit `saveObligation` carrying the amendment, so no due date
  is ever computed inside the decision.
- There is no `record_outcome` compatibility path. The wire field is gone, not
  deprecated; existing rows survive as reported notes through the projection.
- `0010-next-49.sql` depends on `rule_releases` and therefore inherits the
  unverified status of `0004-next-02.sql`, which has never been applied.

### NEXT-03 — Domestic purchasing with owned tax recognition

Purchase journal, payable, source recognition and tax facts as one transaction
group, with mutable original-line capacities that a later supplier credit
consumes. The pure calculation lives in `@open-erp/domain/purchasing`:
`compileDomesticPurchase` returns the exact signed journal group, the payable,
the per-line deductible decision and one tax component per source line, while
`compilePurchaseCreditLines` and `compileUnpaidPurchaseCredit` release the
deduction a recognition actually recorded. Rate, deduction fraction, rounding
mode, acceptance policy, tolerance and deduction basis are **reviewed inputs;
there is no default rate.** The migration declares no function and no tax
calculation, and no floating or approximate numeric type appears in it or in
the application code.

Three ownership decisions are worth recording because each declined to invent
an authority:

- **The purchase tax components are deliberately not written into the existing
  `vat_fact_components` / `vat_fact_revisions`.** Those belong to the VAT
  return owner's manual, evidence-backed admission. This packet publishes its
  own signed components in `purchase_tax_facts`.
- **The existing VAT `recordFact` owner was extended, not replaced.** An
  independent admission of components an owned purchase recognition already
  published is refused with `AlreadyPosted` rather than deduplicated, so one
  economic event cannot be recognized twice. The only read added to that owner
  is `purchase_recognitions`. NEXT-04's VAT-return authority is untouched.
- **The packet's `resolveProfile(basis, domesticPurchase, …)` names a family
  that does not exist.** NEXT-02's families are `posting_eligibility`, `vat`,
  `payroll` and `statements`. The packet's `domesticPurchase` is bound to
  NEXT-02's `vat` family on the tax point date, and an unadmitted family is
  retained as its exact gaps. No `domestic_purchase` family was added, because
  that would be a second admission authority over the same facts.

Two conflicts in the packet's own design were resolved rather than papered
over. `TaxFact.identity = (recognitionId, sourceLineId, componentRole)`
collides with "append a negative TaxFact adjusting the original component" when
the adjustment shares the original recognition id; a recognized credit
therefore gets **its own recognition row** (`event_owner = 'supplier_credit'`
with `original_recognition_id` back to the purchase), which is why
`purchase_recognitions` has nullable `draft_id`/`draft_revision` with a CHECK
tying nullability to the owner, and a unique
`(book_id, payable_id, event_owner)` rather than `(book_id, payable_id)`.

The packet's named ports — `PurchaseDomain`, `RecognitionDb`, `JournalApp`,
`CommandDb`, `BookDb`, `ApprovalApp` — do not exist. The real owners are
`posting.ts` (`prepareJournalInTransaction`, `approveChangeInTransaction`,
`executeChangeInTransaction`, `replay`, `saveCommand`, `digest`) and
`purchases/shared.ts` (`withBook` → `withAdmittedPrincipal`, which already
locks credential/session/membership and then the book writer row). Those are
called directly instead of creating packet-named wrappers. The packet's paths
were likewise bound to the real `purchases/` owners with no rename.

### NEXT-26 — Supplier extraction jobs and field-level reviewed merge

A bounded extraction lifecycle with safe reprocessing and a field-level
reviewed merge, plus the durable path through the existing preparation queue
and effect-mq runner. Extraction produces **suggestions and source locators
only**; the reviewed draft stays with the existing supplier draft owner, and an
accepted economic document is never revised there. The built-in engine reads
**text media only** (`text/csv`, `text/plain`, `application/json`,
`application/xml`); there is no released PDF text-layer or vision adapter in
the checkout, so a PDF or image original is honestly refused with a retained
`media_type_not_supported` diagnostic and the request retained. Inventing a
provider call or a PDF parser would have been a fabricated dependency.

Reported gaps, recorded rather than smoothed over:

- `FieldDecision` had no owner at all — no table, no operation, no contract. It
  was built as new; the reviewed draft stayed with the existing draft owner.
- `ExtractionRequest` had no owner. `supplier_inbox` has no lifecycle columns
  and its `UPDATE` is granted on exactly three columns, so the baseline grant
  was **not widened**; basis and state were split into separate tables the way
  `0004-next-02.sql` does.
- `ExtractionAttempt` did not exist as a distinct type. The real export is
  `supplier_extraction_attempts.body` carrying `RecordSupplierExtraction` with
  `confidence: Schema.Finite` — a model confidence number. **No confidence
  value was invented**; the extended attempt carries result and source
  locators, and confidence is unused by the engine path.
- `reviseSupplierInvoiceDraft` had no internal transaction function although the
  packet requires "the existing internal tx function" for both create and
  revise. It was extracted as a pure de-indent rather than calling the public
  operation from inside a lock.
- **The outbox table is not usable as extraction intent** — its foreign key is
  `execution_receipts`, and a non-financial extraction has no financial receipt.
  The request and state rows are the intent instead.
- Naming deviation: the two new MCP tools take `occurrenceId` where the
  released `supplier_inbox_get` takes `id`. They could not share a name and
  still typecheck. The released tool was **not** changed.
- The correction case is a descriptor, not a financial effect.
  `SupplierExtractionCorrectionCase` names `requiredOwner: "correction_review"`.
  Applying it belongs to `application/posting-corrections.ts`, which is the
  reserved `APPLICATION-REPLACEMENT` owner, and was not touched.
- `readSealedDraft(tx, book, id, "supplier")` is the released accepted-draft
  signal and was used rather than inventing an acceptance predicate.
- All six packet vectors are **implemented, not proven**, and no extraction
  provider was called and no real supplier document processed.

### NEXT-15 — Legal customer credit notes

A legal customer credit note is its own document identity, number series and
journal group: original-line credit capacity, receivable reduction, signed
negative tax effects and the reviewed artifact.

**The shared owners were extended, not bypassed.**
`VoucherPostingAction` in `@open-erp/domain` gains a
`LegalCustomerCreditPostingAction` variant discriminated by a new
`postingPurpose` literal, leaving the synthetic and legal-AR variants
untouched. The legal credit number is treated as **document identity allocated
inside the issuing transaction**, deliberately not as a journal field or a
digest input that would have to be fixed before approval. Posting admission
gains a `legal_credit` owner kind: a credit purpose presented by any other
owner is refused with `UnsupportedProfile`, and a review-id mismatch is a
`StaleDependency`. The legal-purpose gate became an explicit list of purposes
rather than a widened single-purpose test.

Deliberate omissions, reported by the worker and recorded here:

- **No web UI.** The packet mentions distinguishing issued-but-artifact-pending,
  but no route exists and UI is not the named deliverable. The state is carried
  explicitly as `artifactState: "issued_artifact_pending"` in the receipt and
  history.
- **No credit-note renderer.** The outbox intent records
  `requiredRendererVersion: "openerp-se-credit-note-v1"`; no renderer implements
  it and no relay drains the outbox. No released consumer exists for
  `voucher.posted.v1` either.
- **No MCP capabilities for prepare/approve/execute**, matching the released
  `ar-legal-issue` owner, which registers reads only.
- **No VAT return integration, because NEXT-04 is not released.** Each
  correction records the exact negative components a qualified adjustment
  policy would consume, bound to the original recognition component and the
  qualified tax period, with `vatReturnOwner: not_released`. **No VAT return is
  computed and no statutory credit support is claimed.**

The 25% rate and the half-up minor rounding are **carried as reviewed inputs
read back from the activated policy and profile, never as defaults** here, and
a different rate or rounding method is a different profile. The live-invoice
projection was extended because it did not previously know about customer
credits. The extended `liveInvoice` SQL and the bigint parameter casts have
never been parsed by PostgreSQL.

### NEXT-14 — Original dimension assignments

Original dimension assignments are resolved and sealed **before the proposal is
hashed**, so approval covers exactly the assignment set execution will retain,
and they are written in the same transaction as the journal lines they belong
to. Execution re-resolves the sealed set against the current catalogue, so an
archive, an effective-date change or a new requirement between approval and
execution refuses with `changed_since_preparation` instead of re-classifying an
approved posting.

**The obligation is driven by the book's own dimension catalogue, not by the
caller's policy**, which is what closes the obvious bypass: a dimension
effective on the posting date with no entry in the submitted policy refuses
`incomplete_policy`, so omitting `dimensionPolicy` cannot be used to post
unclassified lines. A `required` or `fixed` dimension must carry its value
explicitly, and a reviewed default is resolved during preparation and then
retained explicitly rather than inserted silently at execution or at historical
import. An exact reversal repeats the referenced original line's retained bytes
and needs no policy.

**The local SIE4E dimension profile is verified.** FWD-09 now retains original
opening and movement assignments, emits object opening/closing balances and
checks both native-history and opening-set bases. Conflicting labels and
unsupported text still refuse. [SIE exports](../../apps/api/docs/SIE.md) records
the profile and native proof; the user deferred recipient acceptance.

Unresolved, reported by the worker:

- **The two reserved owners that insert journal lines directly do not call the
  released port.** VAT-03 reclassification and FX-02 write lines without going
  through `resolveAssignmentsInTransaction`, so a posting made through them
  carries no sealed assignment. They are reserved and were not taken over.
- **The historical import paths carry no dimension policy.**
- Recipient acceptance remains open; local dimensional-opening export is verified.
- `dimensionAssignmentReport` reports the **original** assignment only; a
  reclassified report mode does not exist, and classification history is still
  unimplemented.
- `readOriginalAssignmentsInWindow` is book-scoped and single-window, **not
  partitioned by source year**, so NEXT-44's multi-year SIE partition has no
  read to build on yet.

### NEXT-16 — Evidence-aware period preparation

A frozen selection, deterministic routing to the operations that already own each
economic effect, a resumable advance with real checkpoint fencing, and a fixed
approval manifest for one human gesture. This owner posts nothing itself.

**The release resolves to four real owners, and no fifth.** `routeWork` dispatches
only to `purchases.recognition`, `purchases.credits`, `owner.operations` and
`commerce.invoice`, each a real named operation whose prepare and execute are
called. Review cases do not dispatch; a supported domestic supplier credit routes
to `purchases.credits`. The `owner.settlement` route is
**not** dispatched: no operation in this repository posts a company-bank payment
against a recognized supplier obligation, so `purchases.settlement` and
`banking.settlement` were removed from the domain's settlement-owner vocabulary
and the child becomes a review case naming `company_bank_settlement_owner_not_released`.
The database refuses `purchases.settlement` as a routed owner too. Building that
owner is future work, not a second register invented here.

**A period child carries no financial inputs, so a reviewed command is sealed with
the selection.** `WorkChild.prepareInput` is the exact owner command, reviewed
when the operator sealed the manifest. This is the only way the run can call a
real owner without inventing an account, a date, a rate or an amount. A child
without one is recorded as needing review with
`missing_prepare_input_for_owner:<owner>` and nothing is dispatched. An AI may
propose those inputs; it may not supply them.

**The advance runs the owning prepare operation between transactions.** Each child
is claimed in one short transaction, the owner's public prepare is called with
**no transaction held by this owner**, and the plan reference is checkpointed in a
second short transaction. Nesting a prepare inside a held transaction would open a
second financial transaction, which the repository forbids. The command key is
derived from the run, the child and the frozen source revision, so a crash between
prepare and checkpoint is repaired by recovering the same command rather than
minting a second plan. A changed source revision is a different command and
therefore a new preparation, not a silent reuse of an approved plan.

**The fences are columns, compared in the UPDATE's `WHERE` clause.**
`advanceChild` takes the observed `revision` and `cancelVersion` separately from
the new values and returns the updated rows; a handler that captured stale
progress updates zero rows. A terminal child never moves again, so a redelivered
message cannot reopen a committed one. A cancellation that lands while the owner
is preparing keeps the prepared plan as retained evidence and stops the stale
handler publishing it.

**No agent approves anything.** The batch calls the supplier-acceptance,
supplier-credit, owner-operation and invoice-issue approval ports inside one
transaction. Each port enforces its owner's approval rules and creates the actual
approval its execution consumes. A failed member rolls back the whole gesture.
The capability is not agent-callable. Execution marks a stale member as needing a
new review while leaving independent members runnable.

**The batch cannot claim a different owner than the child recorded.** A member's
owner, plan, plan digest and owning review must equal the values the child stored
when it was advanced. A private guard refuses the insert otherwise. Membership is
unique within a batch; approval checks the current child and execution checks its
current batch inside the owning financial transaction. This permits a new review
after a stale batch without letting an old batch execute the replacement. A child
still waiting on a predecessor is refused at batch time
rather than smuggled in.

**Progress is honest and is not a reconciliation claim.** `countChildStates` keeps
pending, waiting, needs-review, prepared, recovered, committed and refused
distinct, and `reconciled` is always `false`. A run whose children were all
visited is still not a reconciled period, and only the separate source and control
inventory can say otherwise.

Deliberate omissions, reported by the worker and recorded here:

- **Transport and runtime:** authenticated HTTP routes expose manifest preparation,
  progress, bounded advance, cancellation, batch preparation, approval and execution.
  Capability dispatch exposes the corresponding operations except cancellation,
  which is HTTP-only. Authority-bearing capabilities are not agent-callable.
  Execution uses `afterOrdinal` / `nextOrdinal`; its command key binds the exact
  batch, digest and page. The effect-mq key includes the retained checkpoint so
  later bounded passes are not deduplicated against an earlier completed pass.
- **No rule-activation owner.** The rules in force at the cutoff are sealed into
  the manifest with the selection, and each rule names the review that qualified
  it. A later rule change produces a new manifest rather than re-deciding a frozen
  child. A separate rule-activation authority is not invented.
- **No source capture.** The children and the rules are handed in from one
  consistent capture, because a selection and a capture must not be two different
  snapshots.
- **`commerce.invoice` and `purchases.credits` are dispatchable but have no
  period-shaped prepare input yet**, so in practice they route to review until a
  manifest seals a command for them.

Runtime evidence, on a real PostgreSQL 17.11 with the whole `0001`-`0018` chain
applied in filename order: a cutoff before the interval it covers is refused; a
routed owner without its owning review is refused, in every partial combination;
a `needs_review` child without named missing facts, a `refused` child without a
reason and a `committed` child without a receipt are each refused; a routed owner
of `purchases.settlement` is refused. The 200th batch member is accepted, which the
previous `ordinal < 200` bound wrongly refused. A member that agrees with its
child is accepted, while a member naming a different owner and a member naming a
tampered plan digest are both refused with `Forbidden` — the allowlisted `P0001`
code `db/transaction.ts` already translates into a typed failure. The runtime role
holds `SELECT, INSERT` on all five tables and a column-limited `UPDATE` on the
  child checkpoint. These are historical constraint observations, not a complete
  period-work journey. The current batch-member index is unique within a batch.

Integration verification on 2026-09-27: frozen installation, changed-file
type-aware lint and TypeScript checks, workspace types/build, lint and formatting
passed. After incorporating main's `494e8ab`, the changed-file full gate and the
existing real PostgreSQL/workerd suite passed again (23 tests); reports
are at `test-results/e2e/results.json` and `test-results/e2e/junit.xml` in the
NEXT-16b worktree. That run applies the migration chain and exercises core posting,
admission, persistence and MCP. It does not exercise the period-work financial
journey, cancellation race, queue restart or owner-specific batch approvals. No
new tests or fixtures were added. The earlier compiler stall was caused by a
duplicate `TableAccess` export in the DB module; removing it restored checks.

A pre-existing merge defect was repaired on this branch:
`packages/domain/package.json` listed `./period-work` without a trailing comma
before main's `./recurrence` entry, which made the manifest invalid JSON and
broke resolution of the whole domain package.
### NEXT-17 — Payable FX and explicit fees

A supplier foreign-currency obligation and its explicit-fee settlement, through
the **existing** commerce FX owner. Migration `0012-next-17.sql` adds one table,
three columns and a `direction` discriminator; it adds no register, no second
balance and no calculation.

**One paired-release capacity, not a payable register.** The original-unit and
book-carrying release is the released WIP-FX02-P1 calculation, unchanged — the
same numerator, denominator, half-up rule and residual the partial settlement
profile already uses. `readItemState` derives the remaining amounts from every
active settlement row of *any* profile, so an explicit-fee leg consumes the same
capacity a partial leg consumes and the existing unique index
`(book_id, item_id, leg_ordinal)` still orders the legs. A correction restores
both amounts from the retained history rather than from a mutable counter.

**A payable is a genuine obligation, not a relabelled receivable.** The
discriminated `synthetic_supplier_foreign_payable_v1` recognition debits the
expense role and credits the payable control from a qualified rate observation.
A book-currency number is never relabelled as foreign units: the profile still
requires `originalCurrency != book.currency` and refuses otherwise.

**One journal carries K, every fee and every cash leg.** The packet's three
vectors are the obligations, and the compiler produces exactly them:

| Vector | Journal | `cash_source_minor` | `realized_gain_minor` |
|---|---|---|---|
| payable b110000 K112000 F1000 | AP+110000, FX loss+2000, fee+1000, cash−113000 | −113000 | −2000 |
| payable b110000 K108000 F1000 | AP+110000, fee+1000, cash−109000, FX gain+2000 | −109000 | +2000 |
| receivable b110000 K112000 F1000 | cash+111000, fee+1000, AR−110000, FX gain−2000 | +111000 | +2000 |

The signed cash carries the settlement's own sign: a receipt is `K − F`, a
payment is `−(K + F)`. An earlier revision of this migration stored the payment
as the *magnitude* `K + F`, which contradicted the sealed `signedCashMinor` the
application writes and would have made every supplier settlement uninsertable.
The direction-aware `CASE` in the profile check is what the compiler's own
`formula` string states.

**Source rights are common, not settlement-local.** A fee or bank observation is
consumed by at most one financial operation, enforced at prepare and again inside
the posting transaction. The shared `readLineOwners` projection gained the
`commerce_fx_settlement_sources` join, so a line this settlement posted cannot
also be admitted as a bank match. This matters because a settlement posts up to
twenty cash legs while its `cash_line_id` names only the first; without the join
the remaining legs were unowned and doubly matchable. A correction releases the
right by its own existence — `readActiveSourceIdentities` excludes any settlement
that has a correction — so nothing is deleted, rewritten or flagged. A reversed
explicit-fee settlement is still listed in `MonetaryItem.feeSettlements`, so
`feeCorrections` states which of them were reversed; without it a reader cannot
tell that a source right is consumable again.

**Refusals are structural, not defaulted.** A fee posts to one reviewed expense
account that is neither a bank account, nor a retained control account, nor an
account the item already binds. Fee tax, foreign cash, hedges and multilateral
netting have no reviewed owner here. A zero gross consideration, a zero fee total
and a cash total that disagrees with the signed cash equation are all refused
before any line is written. The two released receivable settlement profiles
refuse a supplier item with `UnsupportedProfile` rather than posting a receipt
shape for a payment.

Runtime evidence, on a real PostgreSQL 17.11 with the whole `0001`–`0018` chain
applied in filename order: all three packet vectors insert with the values in the
table above, and the pre-fix magnitude is refused by
`commerce_fx_settlements_profile_check`. The corrected ownership read returns
`fx` for the first cash line, the second cash source line and the fee line, and
nothing for an unrelated line on the same voucher. Inserting a correction row
empties the consumed set while both source rows remain. `openerp_runtime` holds
`SELECT, INSERT` on the new table and no `UPDATE` or `DELETE`. **The application
Effect was not run**: no operation, HTTP request or Worker was invoked, so
concurrency, replay and every stale-dependency branch remain unobserved.

Deliberate omissions, reported by the worker and recorded here:

- **No web UI.** The packet names no route, and the released commerce FX
  operations expose no UI today.
- **No MCP capabilities for the new operations**, matching the released
  `commerce/fx` owner.
- **No VAT return integration.** The settlement posts a
  `not_applicable` tax assessment. `D-04`/`D-08` still gate any real-company
  rate, and the packet's `K` is a caller-evidenced amount, never a computed
  default.
- **The evidence baseline S03/S07 is not re-derived here.** `K` stays an input
  with a required evidence reference, exactly as the packet specifies.

### NEXT-06 — Owner-paid expenses, reimbursement and funding

Owner-paid expense, reimbursement and funding effects in one transaction group,
reusing the recognition NEXT-03 already owns rather than re-deriving source
recognition. The pure calculation is `@open-erp/domain/owner-funding`.

**A capital contribution cannot become a loan.**
`shareholder_loan`, `conditional_contribution` and `unconditional_contribution`
are distinct legal forms mapped one-to-one onto their classifications, and an
`unresolved` funding classification produces **evidence only and never a
financial plan**. A funding inflow also requires two distinct accounts.
Migration `0016-next-06.sql` declares no function, no policy and no calculator,
and introduces no floating or approximate numeric type.

Per-diem, mileage and reimbursement amounts are qualified inputs under
D-04/D-08; a missing one is an explicit refusal, never a default. NEXT-16 names
this packet alongside NEXT-01 and NEXT-03 and is now unblocked; NEXT-23, NEXT-32
and NEXT-34 name it conditionally and remain unimplemented or decision-gated.

### NEXT-22 — Pre-close corporate income-tax bridge and INK2/SRU

A sealed pre-close bridge, one approved current-tax effect and one INK2/SRU
declaration lineage, in three records that never share a transaction or a table.
See [CORPORATE-TAX.md](../../apps/api/docs/CORPORATE-TAX.md) for the full
description; the load-bearing points are these.

**The tax journal cannot move the number the tax is calculated from.** The
pre-tax figure is the retained statement result plus the booked current
income-tax effect added back exactly once, so recognising a tax effect never
changes the pre-tax population it was derived from. The retained figure is the
statement snapshot's own untransferred fiscal-year result line; the snapshot does
not retain the transferred movement, and no amount is invented for it.

**Only the delta is posted.** `delta = sealedYearTarget - alreadyRecognized`. A
zero delta is an approved no-effect receipt with no voucher and no consumed
voucher number, not a zero voucher. Preliminary tax paid to a tax account is
never subtracted from the target to make a return agree.

**A duplicate adjustment over one economic component is refused** unless the
reviewed release explicitly establishes the two adjustments as distinct and
non-overlapping. A negative taxable result never becomes a negative cash
receivable: the offset is bounded by the reviewed allowance and the base is
clamped at zero.

**The effect is validated, never self-approved.** `tax_execute_effect` requires a
separate operator's current approval of the sealed plan digest through the shared
change-set approval endpoint and refuses when the approver is the executing
operator. The preserved draft created its own approval inside the same call and
then compared that fresh random identity with the caller-supplied one, so the
operation could never succeed; it also removed the only four-eyes separation the
packet asks for. It now validates through the shared
`readExecutionApprovalInTransaction`, and the whole basis is re-resolved inside
the executing transaction before anything posts.

**The engine and the exported form start from one result.** Which current-tax
figure the form adds back depends on where its declared accounting result came
from: the calculated current tax for a projected after-tax result, the booked
effect inside the retained population for a ledger result. The preserved draft
always used the booked effect, so a projected form could not reconcile. The
declaration now requires the add-back source it actually needs and blocks
otherwise.

**Two further defects in the preserved draft, both found by running the packet's
own vector.** The independent SRU re-parse failed the info file by construction,
because it demanded field values from a file that carries none and then reported
a comparison it could not make; the info file now gets the structural check only
and reports zero compared totals. The record scanner also rejected a per-form
terminator, so no rendered blanket letter could ever be re-parsed.

**No reviewed value is a default.** No rate, rounding policy, loss profile,
journal series, form version, form identifier, field code, record marker, header,
separator, encoding, terminator, filename or size bound is a literal in the
code. The preserved draft hardcoded `#BLANKETT`, `#UPPGIFT` and a `#` info prefix
while claiming no record name was a default; all three are now reviewed bundle
data. The selected profile is the ordinary limited company; NE and the
comprehensive special regimes are refused, not approximated.

**Deliberate deviation.** The packet sketches rendering the SRU files in an
effect-mq Bun job outside the persisting transaction. This implementation renders
and re-parses inline, which commits the semantic fields and the exact verified
bytes together so a retained declaration can never exist without its files. The
render is pure, bounded, in-memory work, so it adds no meaningful lock duration.
See the doc for the full reasoning and what adopting the packet's shape would
require.

**Two more defects that only contract decoding would have caught.** The
pre-tax overlay digested its retained income-tax membership by handing a bare
array to `toJsonObject`, which accepts only JSON objects, so `captureBasis`
failed on every capture including an empty component set. The membership is
now enveloped under its own key, and the envelope is part of the digest. The
SRU record markers were bounded by a pattern that rejected every letter and
digit, which made the hash-led uppercase markers the file-transfer contract
actually uses unrepresentable and every conforming release impossible. The
bound is now the writer's own emittable set without the space, and a marker
that conflicts with the bundle's separators is refused at render time instead.

Both were invisible to the vector run, because that fixture called the pure
functions with plain objects and never went through a contract schema. The
lesson is specific and worth keeping: **arithmetic evidence is not wire-shape
evidence.** A pure-function vector cannot see a decode failure.

**A retained-witness regression this packet introduced and then removed.**
`ProfileDates.taxPeriodOn` was made a required nullable field, but
`ProfileDates` is embedded in every retained `ProfileWitness`, so every witness
sealed before NEXT-22 — the VAT and purchase ones included — would have failed
to decode. The field is now optional and `selectorDate` normalises a missing
value to `null`, so a caller that names no fiscal tax period gets no
corporate-tax family. That also removed five call sites that had been passing
`taxPeriodOn` purely to satisfy the required field: `bookStatus`, payroll
calculation, purchase recognition, the VAT return and the company-admission
panel all had no business selecting a tax release on a date that is not a
fiscal period end.

**Two execution defects found in `executeEffect`.** The retained
`groupReceiptId` was a freshly minted identity that was inserted only on the
zero-delta path, so a nonzero recognition retained a receipt id that existed
nowhere; it now reads back the group receipt the shared primitive committed.
The zero-delta path also bypassed `validatePlan` entirely, so a plan nothing had
checked could be consumed; it now validates its own sealed plan, asserts the
plan carries no group, and only then writes its no-effect receipt.

**The stale-population gap, closed.** Revalidation re-read an immutable
snapshot and compared its digest, which proves the bytes did not change but
not that the population behind them did not. A new or backdated non-tax posting
after the snapshot leaves every retained byte identical, and the shared posting
kernel does not catch it either, because a sealed plan records profile, writer
epoch, period and account dependencies and no committed-sequence boundary. The
bridge now asks the statement owner, at capture and again at execution, using its
own released currentness read: a reopen covering the reported as-of date, or any
voucher after the snapshot's cutoff other than this owner's own current-tax
effects, refuses. That boundary is deliberately conservative — it refuses on a
later posting that provably cannot touch the reported population — because
refusing a proposal costs a fresh snapshot while posting an accrual derived
from a moved population is not recoverable.

The own-tax exclusion is what keeps the boundary from being self-defeating: the
first tax effect is itself a voucher after the cutoff. Ownership is proved by a
committed `corporate_tax_effect` row for the same book and reported fiscal year
whose change set is the voucher's own, never by an event-key prefix — a key is a
naming convention any posting path can choose, so a manual posting that merely
named itself like tax would otherwise escape the guard. An earlier revision used
the prefix and was wrong; the replacement is recorded in the owner document as
the one NEXT-22 query never executed against a database.

**A double-recognition path through the generic posting surface.** Extending
`PostingOwner` with `corporate_income_tax` was not enough. The bridge seals an
ordinary posting plan, so its change set is approvable through the shared
endpoint, and the generic `changes_execute` would have posted that approved plan
with no owner: no `corporate_tax_effects` row, no recorded year target, and the
tax owner free to recognise the same amount again. A generic reversal would have
bypassed the tax register too. `readOwnedSources` now projects
`corporate_tax_bridges` as a `corporate_income_tax` source keyed on the bridge's
change set, with a null `evidence_id` so it matches only that plan and its
correction descendants and nothing else, and `readProtectedCorrections` reports
any voucher a tax effect points at. The zero-delta path needs no pretending: its
plan carries no group, so generic execution refuses on the plan shape and no
voucher exists to reverse.

**A defect in the statement owner's released currentness read, found by running
it.** `readStatementLiveStatus` selected `closing_transitions.committed_at`.
That table has no such column; the transition's time lives in its body as
`committedAt`. The read therefore raised `column t.committed_at does not exist`
on a real database, which means every statement row page read fails today and any
consumer of that read cannot work at all. It is repaired here to
`(t.body->>'committedAt')::timestamptz`, which is NEXT-13's file and NEXT-13's
owner's to ratify. This is the second time in this programme that a query which
looked obviously correct was only caught by executing it.

**A migration defect that only a database could find.** The preserved
`corporate_tax_declarations` constraint compared
`body ->> 'fiscalYear'::text ->> 'id'::text` against `fiscal_year_id`. `->>`
returns `text` and PostgreSQL has no `text ->> text` operator, so the whole
`0001`–`0018` chain aborted at `0013-next-22.sql`. It now uses `->` for the
intermediate step, as `0015-next-04.sql` does. The corrected chain applies clean
on a fresh PostgreSQL 17, and this closes the gap this document records below:
migrations had been checked for the absence of functions and the presence of a
`GRANT`, never parsed. They should be.

**External gate, stated plainly.** The reviewed Swedish corporate-tax rule release
must be loaded into `openerp.rule_releases` before any capability in this group
can succeed. No reviewed INK2 field map, SRU grammar, rate, rounding policy or
journal series ships in this repository, and none was invented. Export is not
filing: no transmission, destination acceptance, signature or statutory claim is
made.

### NEXT-01 — Owner-aware case review

A captured case summary records correction-bundle membership at capture time
only, and the case review button ignored that membership entirely: it handed a
bare `changeSetId` to the posting-recovery route, which refuses with
`UnsupportedProfile` for any correction-bundle constituent. The wire already
carried `bundleId`, `bundleDigest` and `role`; nothing read them.

`cases_resolve_review` is a named Effect read operation that resolves the
current owning review target for one sealed proposal. It reads every current
bundle claiming the plan, and trusts a bundle only when it still names this
book, this original voucher, exactly its two constituents and its own digest.
Review routing resolves first and then selects a destination from a local
route table, so no stored URI drives navigation. Each history row resolves its
own plan. More than one claiming bundle is reported as an unresolved owner
conflict with no review destination and no financial action, which is also the
outcome when owner lookup is unavailable.

### NEXT-02 — Capability-specific company admission

Immutable reviewed fact revisions, independent fact reviews, rule releases,
account role bindings, per-family admission epochs and activations, plus
family-specific effective-date profile selection. The existing legal-AR
activation owner keeps its authority; admission reporting reads that owner's
record instead of keeping a second activation authority. Sealed plans,
approvals and the no-journal receipt reuse the existing `change_sets`,
`approvals` and `posting_group_receipts` identity rather than adding a
parallel set of tables.

**No reviewed `rule_releases` row ships.** The runtime role receives `SELECT`
only on that table. Every family therefore reports a `missing_rule_release`
gap and `prepare_company_activation` refuses. This is designed behaviour, not
a default and not a fixture: a release is reviewed executable data for a
family and this packet does not own its import.

### NEXT-13 — Semantic P&L and balance-sheet snapshots

A deterministic `bigint` semantic model derives P&L and balance-sheet
snapshots from retained ledger facts, sealed into immutable snapshot
membership. Reads separate the saved model from live status, and the empty-page
cursor case returns a next cursor while unscanned members remain.

## Integration debt carried by these merges

These are real and unresolved. None is cosmetic.

**Note on the "never applied by PostgreSQL" statements below.** They were written
before a concurrent agent found that `0010-next-49.sql` could not parse at all
and corrected the chain, and they should be read subject to
[Defects a concurrent agent found](#defects-a-concurrent-agent-found-in-merged-packets-and-what-it-fixed).
Where a bullet says a migration has never been applied, the honest current
statement is that its application is **not this programme's evidence** and was
not reproduced here.

- **Two migrations, never parsed by PostgreSQL.** `0004-next-02.sql` and
  `0005-next-13.sql` were written against the reviewed 0001–0003 baseline but
  have never been applied. Their DDL, CHECK expressions, foreign-key targets,
  `immutable_row` triggers and GRANT statements are unverified SQL. They do not
  overlap in created object names, and neither declares a function.
  `0005-next-13.sql` was renumbered from `0004-next-13.sql` at merge time to
  restore a single migration sequence; nothing had recorded the old name.
- **NEXT-13 leaves `reports_prepare_family` in place.** That existing
  capability also serves `cash_flow`, which this packet does not model, and its
  P&L/balance-sheet projections are a SQL-computed role-bucket view of a saved
  trial balance. That is arguably a second authority for the same statement.
  Retiring those two literals is a real cutover that was **not** performed.
- **NEXT-13 declares four open inputs for NEXT-02** rather than fabricating
  them: `effectiveFiscalRules` is an explicit
  `{ status: "pending_company_profile" }` hole that nothing consumes yet;
  `coverage.companyProfile` is hard-coded `"pending"`; `coverage.statutory`,
  `coverage.financialClose` and `coverage.external` are hard-coded `false` or
  `"not_established"`; and `StatementOpeningBasis.reviewed` is
  `Schema.Literal(false)`, so the model always emits `unreviewed_opening`.
- **NEXT-02 does not implement `canReportComplete` or `canFile`.** Only
  `canPrepare`'s per-family resolution exists. The other two need the
  qualifying-control and format/signature owners this packet excludes.
- **NEXT-02 omits the packet's `CaseDb.insertImpacts`.** No case-impact insert
  owner exists and no posting proposal references a family, so a retroactive
  fact correction records a `company_activation_impact` per affected
  activation instead of a case link.
- **`docs/plans/evidence/planning-integrity.json` was stale for this file.** The
  document-integrity checker records a file list and per-file hashes, so adding
  this note changed that set. It was deliberately not run at the earlier merge,
  because `docs/` had concurrent uncommitted edits and regenerating would have
  clobbered them. **Now reconciled:** `python3 docs/plans/check-plan.py` has
  been run against this change and reports `passed_document_integrity_only`
  with 39 documents and 624 local links and anchors checked, regenerating
  `docs/plans/evidence/planning-integrity.json` and `work-packages.json`. That
  result is a document-integrity result only; it is not a product test.
- **A third migration, also never parsed by PostgreSQL.** `0007-next-11.sql` is
  written against the reviewed 0001–0003 baseline and has never been applied.
  It declares no function, reuses the baseline `immutable_row` guard, and
  carries its own `SELECT, INSERT` runtime grants, but its DDL, CHECK
  expressions, foreign-key targets and trigger wiring are unverified SQL. Note
  the sequence now has a deliberate gap: `0006` is reserved for NEXT-03, which
  is still in flight.
- **NEXT-11 depends on a dimension-assignment owner that does not exist.** The
  baseline has `dimensions` and `dimension_values` but no journal-line dimension
  assignment table at all, so a dimension-bearing book cannot be exported. The
  packet did not take over that owner and did not substitute an empty
  assignment for a reviewed one. NEXT-14 is unmapped in the dependency graph.
- **The 4E record profile is a declared subset, not a qualified matrix.** A
  reader that needs the full 4E mandatory record set still has to qualify it.
  `emittedRecords.recordProfile` is the honest statement of what was emitted.
- **`0008-next-20.sql` has never been parsed by PostgreSQL.** Like 0004, 0005
  and 0007 it is written against the reviewed 0001–0003 baseline and never
  applied. It declares no function and carries its own `SELECT, INSERT` grants,
  but its DDL, CHECK expressions, foreign-key targets and `immutable_row` wiring
  are unverified SQL.
- **NEXT-20's four packet vectors were evaluated in a throwaway `bun` process**
  against the exported pure calculator. That is **arithmetic evidence only** —
  not a transaction, not concurrency, not a database — and it is not retained
  as a test, because `AGENTS.md` forbids adding tests without explicit approval.
- **NEXT-20 left `apps/web/src/components/payroll-foundation.tsx` untouched.**
  The frozen calculation is reachable only through its API. No interface
  surface was added, so nothing here is a completed product path.
- **A concurrent agent, not this programme, owns four dirty files in the main
  worktree**: `apps/api/scripts/preparation-runner.ts`,
  `apps/api/src/application/purchases/extraction.ts`,
  `apps/api/src/application/purchases/extraction-engine.ts` and
  `packages/contracts/src/supplier-extraction.ts`, plus a new untracked
  `apps/api/src/adapters/storage/filesystem-objects.ts`. Those edits were not
  made here and have deliberately not been committed or reverted. They are the
  sole cause of the `bun run lint` failure recorded below, and they also mean
  `bun run check` cannot be run here without `oxfmt --write` reformatting
  another agent's in-progress work. `oxfmt --check` was used instead.
- **`DeadlineInput` changed shape, breaking existing obligation clients.**
  `jurisdiction`, `statutoryBasis` and `requiredEnvironment` are now required
  and `DeadlineActivity.reference` is gone, with no compatibility runtime. Any
  pre-existing obligation row or `saveDeadline` client is invalidated. This is
  intended — a statutory input is a qualified input, never a default — but it
  is a live consequence, not a cosmetic one, and no database has applied
  `0010-next-49.sql` to measure it.
- **`0010-next-49.sql` is a fourth migration never parsed by PostgreSQL**, and
  it additionally depends on `rule_releases` from the never-applied
  `0004-next-02.sql`, so it inherits that unverified status.
- **An accepted obligation cannot be satisfied today.** The `authority_outcome`
  fulfillment variant has no owner because NEXT-48's authority-outcome module
  does not exist, so its resolver returns `pending` with a named reason.
- **NEXT-11 touched a ninth shared registration file.** Beyond the eight the
  coordinator tracked, `jurisdictions/se/package.json` needed a new export
  path for the pure module. That file is now verified on every merge.

## Defects a concurrent agent found in merged packets, and what it fixed

Recorded because it changes what may honestly be claimed about this work. These
were found in packets this programme merged, by an agent working separately, and
fixed in commits `d816c80` and `4d624c4`.

**NEXT-49 was worse than "unobserved".** Three defects, each independently
enough to make the packet non-functional:

- **`0010-next-49.sql` did not parse.** `NOT` applied to a parenthesized `jsonb`
  extraction is not a comparison, and an operator expression in an index column
  list must be parenthesized. Two parse errors stopped the whole chain _before_
  `0010`, so no database had ever applied it.
- **Every write refused.** The database access helpers answered `canInsert
false` for exactly the tables the operation writes, while the application
  guard treats that `false` as a refusal — so the required write tables were the
  only ones denied. The migrations did grant `INSERT`; the privilege predicate
  simply never asked for it. **This is precisely the "documented function that
  refuses every case" that the packet rules forbid calling complete.**
- **The digest call was the wrong kind.** Notice, decision and fulfillment
  bodies were hashed with a versioned canonical-document digest requiring
  version and canonicalization metadata the bodies do not carry, so every call
  failed before hashing. The tables verify `openerp.digest(body - 'digest')`, so
  the ordinary supported JSON digest is what the stored bytes are hashed with.

**NEXT-20 could not function either:**

- It could not decode its own rule release. The shared `RuleRelease` owns one
  nested payroll payload, and payroll decoded the raw row as if the payroll
  fields were at its root, so a release valid under the declared shared schema
  failed to decode and **every calculation was refused**.
- **Monetary bounds were compared as strings**, so `"900"` sorted above
  `"1000"` and an inverted contribution band or withholding row passed its own
  check. They are compared as exact integers now.
- **A rounding helper divided a minor-unit amount by its declared scale and
  kept the minor name**: 3 000 000 minor units at scale 2 came back as 30 000, a
  hundredfold understatement of gross, reimbursement, deduction, payable and
  every fixed or table withholding amount.
- **Private payroll access was weaker on the read path than the write path.**
  The grant check ran only after a saved-command replay could already return a
  record, and get and list performed none at all, so **book membership alone was
  enough to read frozen payroll calculations**. Ordinary identical-command
  recovery still works for an authorized caller.

### What this changes about the verification story

- The earlier claim that the NEXT migrations had **never been parsed** by
  PostgreSQL is superseded. `0010-next-49.sql` could not parse at all, which is
  a stronger failure than never having been run. A concurrent agent reports the
  corrected `0001`–`0011` chain **applies to a fresh PostgreSQL 17**. That
  observation is **not** ours and has not been independently reproduced here, and
  it says nothing about grant matrices, transaction and rollback behaviour, lock
  ordering under contention, replay and duplicate refusal, approval expiry and
  revocation, or any HTTP/MCP surface.
- Two defects in this programme's own merges (`f15c1df`, `5b2c0bb`) were
  cross-packet contract conflicts that only surfaced when two branches met:
  NEXT-15's credit-note line type omitted the assignment field NEXT-14 reads, and
  NEXT-06's wire restatement dropped the `taxFactId` a later credit's adjustment
  names. Each typechecked in isolation because each branch predated the other.
  Both are now fixed, and both were caught only by typecheck, never by review.
- **A gap in how these merges were reviewed, stated plainly.** Each migration was
  checked for the _absence_ of functions and for the _presence_ of a `GRANT`
  statement. None was ever parsed by a database, and no read path was traced for
  a privilege predicate that could return a denial. Those two checks missed
  exactly the defects above. Migration files in this programme should be parsed
  before they are called reviewed.

## Verification limits

The integration at `6f3e27f` passed the changed-file full gate and all 23 existing
PostgreSQL/workerd E2E tests. The suite covers core admission, posting, persistence
and MCP. It includes replay, revocation and rollback cases. It does not cover every
NEXT feature journey. See the NEXT-16 entry for the integration checks and report
paths, and the [landed repair record](evidence/latest-landed-review-repairs.md) for
owner-specific limits.

| Evidence | What it establishes | What remains open |
| --- | --- | --- |
| Lint, types and build | Source consistency at the checked revision. | Runtime behavior and accounting correctness. |
| Existing core E2E suite | The exercised Worker/PostgreSQL operations, migration application and rerun. | Complete period-work, recurring invoice, owner-discharge and credit journeys. |
| Earlier NEXT-16/17 SQL probes | The constraints and grants those probes exercised. | Owner preparation, approval and execution through the real feature callers. Some probes disabled foreign-key triggers; they are not full journey proof. |
| NEXT-13 arithmetic probes | Selected pure-function vectors. | Retained reproducible report, transaction and concurrency evidence. |
| [Bend qualification](../../verification/bend/authority/docs/QUALIFICATION.md) | Recorded synthetic VAT monetary and host observations for the qualified candidate. | Deployment approval, company VAT completeness and external filing acceptance. |
| NEXT-11 source implementation | Capture, rendering and comparison logic exists. | An observed complete export and independent recipient import for the selected profile. |

Earlier statements that no database or Worker checks ran are superseded by the
integration evidence above. The NEXT-16 compiler stall was resolved by removing a
duplicate `TableAccess` export. Old lint failures are historical results, not
current blockers.

For new evidence, pin the code, migration chain, environment and inputs. Use the
current migration set, not an old numbered subset. Record commands, independent
expected results, receipts and limits. Company facts and reviewed rule releases
must come from their owners. New tests require explicit approval. No result here
establishes whole-company or statutory readiness.

## Reserved work

The five reserved WIP assignments remain untouched and were not reimplemented,
requalified or taken over: `WIP-VAT03`, `WIP-FX02-P1`, `WIP-AST03-UI`,
`WIP-VAT04-A1`, `WIP-COM2-W1`. NEXT-02 and NEXT-13 consume none of them.
NEXT-17 **uses** `WIP-FX02-P1` and does not duplicate it: the paired-release
capacity, its half-up rule and its residual handling stay the released owner's,
and the packet's instruction not to copy the WIP partial-release algorithm is
met — the compiler adds K, F and the signed cash equation around the existing
release rather than restating it.
