# NEXT-38 delivery working contract

Baseline: detached `6b82ed39039fe4e2bf160fed911b474c4fc0065a` in the isolated
`next38-delivery` worktree. This records design and failure obligations before
financial implementation; it is not verification evidence.

## Owners and intended flow

```text
qualified retained company facts + dated posting/VAT witnesses
  -> commerce document admission
       commerce_invoices: commercial debt; recognition = null
       original source components: frozen, same invoice owner
  -> commerce allocation preparation + independent approval
  -> allocation application transaction
       derive final principal/identity/evidence from retained effective allocation
       recognize only uncovered components
       release posted clearing capacity; never post bank again
       commit journal, tax facts, coverage, allocation and receipts together
  -> complete year-end population preparation + independent approval
  -> year-end transaction
       recheck complete membership, original components, method witnesses,
       effective allocations, period/account authority and coverage
       recognize remaining unpaid coverage exactly once
  -> next-year allocation: control settlement, no new tax fact
```

The old caller-assertion register/payment/year-end writes stay fenced until the
real owners replace their paths. Migration `0040` is immutable. Forward DDL uses
`0043` or later; `0042` is reserved outside this worktree. Root owns final evidence,
packet progress and domain-leaf inventory.

## Independent financial expectations

All amounts below are integer minor units, specified without calling production
calculators. Both customer and supplier directions must conserve these amounts.

| Stage | Commercial unpaid | Recognized unpaid | New net | New VAT | New bank posting |
| --- | ---: | ---: | ---: | ---: | ---: |
| Document G125000=N100000+VAT25000 | 125000 | 0 | 0 | 0 | 0 |
| Final payment allocation 50000 | 75000 | 0 | 40000 | 10000 | 0 |
| Complete unpaid year-end cutover | 75000 | 75000 | 60000 | 15000 | 0 |
| Next-year final allocation 75000 | 0 | 0 | 0 | 0 | 0 |

The payment source owner's original bank posting remains exactly 50000 and then
75000. Recognition adopts its compatible clearing side. For sales the first
recognition debits clearing 50000 and credits revenue40000/VAT10000; purchases
reverse these signs and use the qualified deductible input VAT component.
Year-end sales debit AR75000 and credit revenue60000/VAT15000; purchases debit
cost60000/inputVAT15000 and credit AP75000. Later settlement reverses the owned
clearing capacity against AR/AP75000 only.

## Failure-first HTTP/PostgreSQL obligations

Each refusal must compare independently captured database state before and after:
vouchers/lines, tax facts, coverage, allocations, approval use, counters, command
receipts and year-end membership. No half-success or claimed financial receipt.

1. Unknown, unreviewed, accrual, overlapping or stale accounting-method facts;
   missing dated posting/VAT release or activation; caller witness alone: refuse.
2. Existing accrual voucher, invented source line, second label for the same gross,
   unsupported currency/tax treatment or incompatible account role: refuse.
3. Commercial issue/acceptance alone creates no voucher, revenue, cost or tax fact;
   the existing invoice read and statement expose full commercial debt honestly.
4. Missing, reversed, corrected, wrong-book, wrong-invoice, wrong-direction or
   nonfinal payment allocation: refuse. Request-supplied amount/evidence/identity
   must never substitute for retained payment facts.
5. Overcapacity, duplicate source allocation, stale allocation/coverage/profile,
   revoked authority, absent/expired/consumed approval or locked period: refuse.
6. Same key and immutable command replays the same receipt. Changed input with
   same key conflicts. A fresh key cannot repeat an economic payment or cutover.
7. Failure after nested posting but before allocation/coverage/tax receipt writes
   rolls the entire transaction back, including numbering and approval use.
8. Year-end captures every eligible native invoice through the fiscal cutoff,
   including zero-effect items. Unknown unsupported members block completeness.
   Voluntary registered-line subsets, pages and truncation cannot establish it.
9. A relevant new invoice, payment, credit, changed treatment or reviewed method
   revision after preparation invalidates execution without financial effects.
10. Payment versus year-end competing for the same coverage: one wins; the other
    refuses stale or recomputes under a new review. Combined VAT stays25000.
11. Backdated discovery after executed year-end preserves the receipt and refuses
    silent reassessment, exposing the owned amendment/closing impact boundary.
12. Unrecognized unpaid credit changes commercial residual without reversing
    nonexistent accounting. Recognized-unpaid credit creates one exact linked
    correction and negative VAT effect. Paid-principal credit/refund refuses
    until its cash-method treatment is qualified. Generic posting correction and
    allocation reversal cannot bypass these owned coverage protections.
13. Next-year payment settles the recognized position with zero new VAT facts,
    including replay and source-capacity checks.
14. Restricted runtime-role migration grants admit only required writes. Posted
    history and sealed receipts remain immutable; direct malformed coverage fails.

## Initial mapping checkpoint (superseded below)

Required instructions, baseline evidence, packet and transaction ADRs read.
No financial source changed and no verification executed at this checkpoint.
The parent owns the frozen dependency installation before checks.

## Baseline continuation map

Repository facts inspected after the failure obligations above:

- `packages/contracts/src/commerce.ts`: `CreateInvoice` requires the two posted
  recognition identifiers. `Invoice.recognition` and `AllocationLeg.recognition`
  are nonnullable `Recognition` structs. `Invoice.kind` admits only synthetic
  accrual and legal-customer kinds. No honest commercial-only variant exists.
- `apps/api/src/application/commerce/register.ts`:
  `createInvoiceInTransaction` at line632 requires a retained recognition line,
  checks current posting/evidence/gross agreement, claims the account and line,
  inserts the native invoice and revision, then returns `liveInvoice`.
  `invoicePayments` at line1059 reads recognition event/date without a null guard.
- `apps/api/src/db/commerce/invoices.ts`: the live projection's blocker at
  line197 calls `recognitionAccounted(i.recognition_voucher_id)`. A commercial-only
  invoice needs an explicit validated branch, not a missing-voucher blanket skip.
  `activeLegTotal` excludes allocation receipts with an owned reversal.
- `apps/api/migrations/0001-schema.sql` lines425–451: the invoice's posted
  recognition columns are mandatory; the journal-line composite FK and posted
  identity uniqueness already exist. `0002-integrity.sql` has the invoice
  identity freeze trigger. Extend through forward migration, never the baseline.
- `apps/api/src/application/commerce/allocation-reversals.ts`:
  `allocationSelection` at1208 captures current payment capacity, invoice
  revision/allocation version, account/period/writer versions and evidence.
  It currently compares `invoice.recognition.eventId/postingDate`. Its sealed
  selection is recomputed by `currentAllocation` before application.
  `applyAllocation` at1468 locks the book, validates the digest/current selection,
  checks approval/current operator membership, claims the posted payment line,
  then inserts the receipt and legs at1589–1606. This is the financial composition
  point; nested recognition must share its `transaction`.
- `apps/api/src/db/commerce/allocations.ts`: `readPaymentCapacity` at186 reads
  the *clearing/control* journal line, current voucher and direction from
  `commerce_control_accounts`; it rejects no bank line by itself. Its
  `allocatedMinor`/`capacityVersion` count all historical legs, while the invoice
  projection counts only effective legs. Preserve existing source rights and
  reversal semantics when binding the cash-method capacity projection.
- `apps/api/src/application/company-profiles.ts`:
  `resolveCompanyProfileInTransaction(transaction, scope, recordClass, dates)`
  resolves reviewed fact revisions/reviews, dated releases, role bindings and
  activations. `company-profile-basis.ts` selects posting on `postingOn` and VAT
  on `taxPointOn`; accounting-method facts gate both families. Its witness is the
  existing qualification owner. Do not use company-setup's editable summary as
  financial method authority.
- `apps/api/src/application/purchases/recognition.ts`: `readVatWitness` at137
  uses that resolver; `compilePurchasePlan` at197 derives original source-line
  net/tax from retained draft lines and explicit reviewed treatment assignments.
  It namespaces source tax components by recognition identity. The cash branch
  must freeze these components without publishing their accrual effect first.
- `apps/api/src/application/purchases/acceptance.ts`:
  `executeSupplierAcceptance` at885 approves/executes its sealed posting plan,
  registers the posted payable, writes owned recognition/tax facts and commits
  its receipt. Its receipt currently reports `recognized: true` and a mandatory
  posting receipt. Branch its admitted method before this posting, and carry an
  honest commercial-only receipt through its contract/read surfaces.
- `apps/api/src/application/posting.ts` exports
  `prepareJournalInTransaction` at703, `approveChangeInTransaction` at951,
  `readExecutionApprovalInTransaction` at1084 and
  `executeChangeInTransaction` at1136. The executor writes voucher/lines,
  dimensions, execution/group receipts, approval consumption, counters and
  outbox through the passed transaction. It calls `admitPosting` with the
  optional named `PostingOwner`; new cash-method effects must be owned/sealed
  against generic direct execution and correction bypass.
- Nullable invoice recognition affects these existing accrual consumers:
  `purchases/credit-basis.ts`, `commerce/credit-notes.ts`,
  `commerce/cancellations.ts`, `commerce/register.ts` and
  `commerce/allocation-reversals.ts`. Their accrual-only paths need explicit
  refusal or a narrowed recognized invoice; no fake placeholder identifier.
- `0040` enforces monotonic paid/recognized prefixes and grants only those prefix
  updates plus version. Recognized-unpaid credit lowers effective recognized
  coverage in the leaf, so forward integrity and correction storage must permit
  the owned correction without editing original rows/receipts or silently
  weakening the fence. The immutable recognition row currently requires a
  `change_set_id`, even for a next-year no-new-recognition settlement; use the
  actual settlement plan rather than a fabricated change set.

Continuation should first write the executable HTTP/PostgreSQL scenarios for
these failure obligations using the existing fixtures/harness, then implement
the document variant, profile-qualified admission and its native read projection.
Next compose allocation recognition and tax facts; then complete year-end
prepare/approval/execute membership, correction fences and next-year settlement.
Do not advertise delivery after only the document variant.

Initial tooling receipt: `effect-solutions` is not on PATH; the existing executable at
`/Users/admin/.bun/bin/effect-solutions list` succeeded. The root manifest pins
`effect@4.0.0-rc.112`. At this checkpoint the isolated worktree has no
`node_modules`; installed Effect guidance/signatures and any checks remain
pending the parent's frozen installation. No source, contract, migration or
test files have been modified; no tests, checks, commits or pushes were run.

## Bounded prerequisite delivered

The subsequent request bounded this invocation to commercial-only invoice
admission. It is implemented for **retained domestic SEK supplier drafts under
the explicit `synthetic-cash-method-domestic-v1` profile**, standard 25% source VAT,
full deduction, exact source-tax agreement and half-up component rounding. This
does not activate an actual company's method or a statutory Swedish VAT profile.

### HTTP and shared shapes

`POST /api/v1/entities/:entityId/books/:bookId/commerce/invoices/cash-method`
(`admitCashMethodInvoice`, operator-only REST; no new MCP mutation) accepts
`CashMethod.AdmitCashInvoice`:

```text
profile = synthetic-cash-method-domestic-v1
draftId, expectedRevision, expectedDigest
controlAccountId, inputVatAccountId
lineAssignments[] = {lineId, expenseAccountId, treatment: ReviewedTreatment}
reason, acknowledgeSyntheticOnly = true
```

The command carries no amount, document number, counterparty, evidence identifier,
method witness or payment claim. The owner reads those facts from the retained
current supplier draft and validates the treatment through the existing pure
purchase compiler. It does not persist that compiler's prospective journal or
tax-fact output.

The response uses the existing `Commerce.Invoice`: its kind is
`cash_method_supplier_invoice_v1`, `recognition` is **null**, and `cashMethod` holds
the frozen basis. Original gross remains the native commercial amount and live
outstanding; acceptance creates no payable-control journal. The invoice schema
checks that only this kind may have null recognition, and that recognized kinds
cannot carry a cash-method basis. `AllocationLeg.recognition` is nullable for the
next integration, but current allocation preparation still refuses null recognition.

`CashMethod.CashInvoiceBasis` is the typed schema for the frozen `cashMethod`
object. It carries:

- profile/direction and draft ID, exact revision and digest;
- confirmed `methodFactRevisionId`, current posting and VAT `ProfileWitness`;
- `vatMethod: cash`, tied to the named reviewed synthetic cash calculator release,
  not guessed from an independent actual-company VAT-method summary;
- control/VAT accounts, `tax_first_cumulative_v1`, `half_up`;
- original-order lines with `sourceLineId`, expense account, exact `netMinor`,
  `taxMinor`, `grossMinor`, `deductibleMinor` and reviewed treatment.

Both family witnesses must select the same confirmed cash accounting-method fact.
The qualified releases must explicitly constrain cash accounting and registered
VAT, use the named synthetic calculator and admit the transaction's source date.
Commerce/VAT account choices must match their current witnessed role bindings.

### Transaction interfaces for allocation/year-end work

Exports from `apps/api/src/application/commerce/cash-invoices.ts`:

```text
admitCashInvoiceInTransaction(tx, principal, {scope, idempotencyKey, input})
  -> Effect<Commerce.Invoice, AccountingError>

readCashInvoiceBasisInTransaction(tx, scope, invoiceId)
  -> Effect<CashMethod.CashInvoiceBasis, AccountingError>

resolveCashInvoiceProfileInTransaction(tx, scope, date)
  -> Effect<{methodFactRevisionId, postingWitness, vatWitness}, AccountingError>

admitCashMethodInvoice(token, command)
  -> admitted, book-locked transaction wrapper for HTTP
```

Internal callers own current principal admission and the book writer lock before
calling the tx-passing admission. Readers never open another connection or runtime.
Future recognition owners must compare the retained witness/revision with current
resolution at their trigger date, and read invoice `evidence` (the frozen original,
not replaceable metadata evidence) alongside this basis. No cash recognition rows
are inserted by admission; allocation/year-end consumers still own those prefixes.

DB functions in `db/commerce/cash-invoices.ts` retain the invoice in the existing
`commerce_invoices` table and expose book-scoped basis/draft/source identity reads.
Forward migration `0043-cash-method-commercial-invoices.sql` permits null posted
recognition only for this commercial kind with a native supplier-draft FK. Unique
draft and original-evidence identities prevent a fresh command key, another draft
label or another source-line label from adopting the same original twice. Existing
invoice identity freeze protects the frozen body and source pointer. No baseline
or applied `0040` bytes changed; `0042` remains reserved.

Accepted drafts are sealed against revision and against later ordinary accrual
acceptance. Invoice payment discovery/allocation, accrual credits/cancellation,
owner-paid discharge, supplier payment batches and refund workflows explicitly
refuse unsupported null-recognition invoices. Original register reads continue to
expose commercial debt. The three old cash recognition writes remain fenced.

### Executed proof

The parent reported a passing frozen dependency installation. This work ran:

- `bun run check:changed`: passed.
- `bun run check:changed:full`: passed (normal/type-aware lint and API, contracts,
  E2E TypeScript projects).
- Invoice/refusal E2E plus supplier-register paging regression: six tests passed
  across four files on disposable PostgreSQL and the real workerd HTTP transport.

The accepted vector proves G125000=N100000+VAT25000, native commercial outstanding
125000, null recognition references, and **zero vouchers, journal lines, purchase
recognitions, purchase tax facts and cash recognition lines**. Other observations:
exact receipt replay, changed-command conflict, duplicate draft/original refusal,
cross-book refusal, stale source refusal, unreviewed/accrual-method refusal,
incompatible accounts, agent mutation refusal, accepted-draft freeze and accrual
acceptance refusal. The original accrual relabelling and three old write-refusal
tests remain passing.

Retained artifacts are under `test-results/next38/`: `results.json`,
`source-integrity.json`, `manifest.json`, `migrations.log` and runtime logs. The
final run retained `status: stable` with identical initial/final source inventory
hashes: `14f944360d49f8e27a7b95e70a51c65d8779d5f1604cef279d443c0111533aa1`.
The migration log records successful application through `0043`. Although the
CLI announced a JUnit path, no `junit.xml` was retained; it is not cited as proof.
An earlier run exposed a missing initial native invoice revision; the insert was
fixed, and the final repeat passed rather than weakening its acceptance assertions.

Payment recognition, complete year-end membership, owned correction effects and
next-year settlement remain the root's next integration. No wired declaration,
packet progress, final evidence document, commit or push was made here.

## Allocation-owned payment slice delivered

The next bounded slice now runs through the existing allocation
prepare/approval/application HTTP operations. No year-end implementation was
started. The original assertion-based cash line registration, payment recognition
and year-end commands still refuse `UnsupportedProfile`; replacing those public
contracts remains pending. Payment recognition is owned by allocation application,
not by the old payment command.

### Sealed financial effect and retained source

`Commerce.AllocationPlan.cashEffect` carries a JSON object decoded by the typed
`CashMethod.CashAllocationPrepared` schema:

```text
selection:
  source: current posted voucher/clearing line + matched bank line,
          event/fiscal year/period/series, original evidence/hash,
          statement/observation identity and original cash principal
  accounts: exact current account versions
  invoices: original basis/evidence, current method and role witnesses,
            original-order before/after coverage, actual paid slices,
            new net/tax/deduction and exact tax-journal positions
  journal: exact new recognition effect, with no bank entry
postingPlan: sealed posting-kernel change set, or null for no new recognition
```

The allocation digest includes both selection and the complete posting plan.
Cash approval requires an independent operator and creates the linked kernel
approval in the same approval transaction; its ID is returned as
`AllocationApproval.cashPostingApprovalId`. A client cannot execute that nested
plan through generic posting: the named `cash_allocation` owner is required and
the action must equal the retained sealed effect.

Application inserts the allocation receipt and legs first. In that same financial
transaction it reads their effective retained amounts and source identities,
re-captures the current source/coverage/profile, compares the complete selection,
then composes `applyCashPayment`. It adopts the posted clearing-side capacity.
The existing bank entry and any already-recognized AP settlement are not posted
again. Journal, tax facts, coverage, allocation, approval use, counters, receipts
and outbox all roll back together.

This source profile is deliberately bounded: a current two-line SEK cash/clearing
voucher, a real execution receipt, one compatible active bank match to a retained
synthetic booked statement/observation, complete declared source, matching amount
and date, original event evidence/hash, and no provider-pending row. Unposted,
nonfinal, corrected, unmatched, fee/multi-line and incompatible sources refuse.
Caller-selected allocation evidence is not the financial cash evidence.

Financial qualification remains the explicit reviewed synthetic cash profile.
Nullable activation IDs are preserved as nullable; they are not treated as an
actual-company activation. Real-company activation and other source profiles
remain outside this bounded proof.

### Transaction ports for the next owner

`apps/api/src/application/commerce/cash-payments.ts` exports:

```text
readCashCoverageInTransaction(tx, scope, invoiceId)
  -> {basis: CashInvoiceBasis, lines: [{lineId, line: CashMethodLine}]}

readFinalCashSourceInTransaction(tx, scope, voucherId, clearingLineId)
  -> CashPaymentSource

captureCashAllocationInTransaction(tx, scope, {voucherId, lineId},
                                  [{invoiceId, ordinal, amountMinor}])
  -> CashAllocationSelection

prepareCashAllocationInTransaction(tx, principal, scope, planId, selection)
  -> CashAllocationPrepared

approveCashAllocationInTransaction(tx, principal, scope, allocationPlan)
  -> kernel approval or null for no-effect/noncash

cashAllocationReceiptSummary(effect, receiptId)
  -> {recognitionIds, vatFactIds, changeSetId, sourceVoucherId}

applyCashAllocationInTransaction(tx, principal, scope, plan, approval, receiptId)
  -> atomic recognition/tax/coverage writes over effective retained legs
```

The caller owns admission and the book barrier. These ports receive the caller's
transaction and never open a second connection/runtime. Coverage reads return
honest zero prefixes for admitted originals without a physical coverage row.
They preserve original line order and expose released deduction and coverage
versions needed by the year-end owner.

When previously recognized-unpaid coverage absorbs the whole payment, the compiler
returns no new journal or VAT fact and only advances paid coverage. The history
then links the actual existing settlement voucher/change set. This is implemented
compatibility, not an observed next-year/year-end journey: that integrated proof
requires the next year-end slice.

`application/vat/cash-method-facts.ts` exports
`recordCashMethodFactInTransaction`. It publishes linked components/revisions in
the existing `vat_fact_components` / `vat_fact_revisions` owner, with original
invoice and cash provenance, payment tax point and cumulative coverage metadata.
It is payment-specific. The year-end owner must extend the existing VAT owner
with its genuine year-end trigger; it must not invent a bank source to call this
payment port. The synthetic VAT return owner captures these facts and validates
their cumulative rounding plus exact ledger tax link. Actual-company returns
continue to distinguish synthetic records.

Forward `0044` retains immutable allocation-effect metadata, adds original and
released component columns to cash coverage, and links recognition history to
effective allocation legs, source cash lines, posted effects and existing VAT
facts. No second invoice or tax ledger was created, and `0040` remains unchanged.

### Correction/source protections

Accepted cash-original evidence is reserved in posting admission. Only a named
cash owner with the exact retained original basis, sealed action and source event
may consume it. Ordinary supplier acceptance now checks original-evidence adoption
on preparation and execution, including second-labelled drafts and prior reviews.
Generic posting/correction cannot reuse that original or rewind a consumed cash
effect/source. Allocation reversal, consumed bank-match reversal, manual VAT
revision/withdrawal and tax-line copying refuse pending an owned correction path.

The register-report snapshot omission found by review remains root-owned. No
report files were changed in this slice.

### Observed payment proof

Final source checks passed: `check:changed`, `check:changed:full`, and diff whitespace
inspection. The final real HTTP/workerd/PostgreSQL run passed **10 tests across
four files**, including the five payment tests and prior invoice/refusal tests.

Independent observed vector: G125000=N100000+VAT25000; retained final allocation
50000 produces expense40000/inputVAT10000 and adopted clearing50000. Existing bank
credit remains exactly50000; commercial unpaid is75000 and recognized unpaid is0.
The existing VAT basis and synthetic return capture one contribution of10000.

Observed refusals/recovery include self-approval, generic nested execution and
source correction, original-evidence reuse, second-labelled ordinary acceptance
(including a previously approved review), duplicate application/source use,
unposted/no-bank/nonfinal/overcapacity sources, stale accounts, cross-book references,
locked period, revoked approver authority, VAT copying/withdrawal and consumed
bank-match reversal. A deliberately injected failure on the final coverage update,
after nested financial/VAT writes, left counters, approval consumption, allocation
legs/receipts, tax facts and coverage unchanged; the original request key then
committed and replayed the same receipt.

Retained artifacts: `test-results/next38-payment/results.json`, `manifest.json`,
`source-integrity.json`, `migrations.log`, and runtime logs. Source integrity is
`stable`, with identical hashes
`f2b08dcdf60437247d83019e63f0a280d4fd3d4861374e2dde659ff8a21b5509`.
The migration log confirms application through `0044`. The expected forced rollback
produced a sanitized HTTP500 in the worker log; it is part of the passing test.

No inventory/wired declaration, final evidence/progress update, report work,
year-end implementation, commit or push was made in this slice.

## Resumed complete delivery — 2026-10-01 (unverified)

The interrupted year-end files are retained and being completed, not restarted.
Independent bounded owners handle: posting-admission/rounded VAT regressions;
register snapshot commercial-versus-recognized reporting; sealed year-end and
financial-close consumption; and unpaid supplier credit consequences. The
integrator owns serialized checks, the route aliases, evidence and final merge.

The legacy assertion-based line/payment write bodies are replaced only with
delegation to real retained-data owners: line admission uses the supplier draft
command, payment execution names an independently approved allocation plan, and
year-end names the complete fiscal-year preparation. Old amount/witness bodies
must fail schema admission; no caller-assertion financial writer returns.

Final proof must run after all source writers stop, with a stable source inventory.
The earlier invoice/payment receipts do not prove the resumed source. Integration
into `/Users/admin/openERP` must use the baseline plus the current primary bytes
for shared files: primary already contains newer committed PDF and other work.
Do not replace those shared files wholesale. No commit or push is authorized by
this checkpoint, and none has been made by this continuation.

The first resumed fast gate failed on unfinished credit schema wiring, style and
two over-complex owner functions; it did not time out. A read-only independent
review also found two required financial fixes: later-dated unpaid credits must
block an earlier year-end assessment until a historical correction is owned, and
register credit attribution must read the posting kernel's real grouped actions,
not a nonexistent `postingPlan.action`. These findings remain proof obligations.
Credit amounts must come from a retained reviewed supplier credit draft, never
from a caller-stated gross amount plus an evidence identifier.

Further integrated review obligations: historical preparation must refuse a
later-dated recognition that already consumed the same original; an empty
qualified cash-method year still needs a sealed complete assessment; retained
credit net/tax components must agree with the qualified original suffix policy
or refuse; and native invoice outstanding/allocation versions must consume the
same owned cash-credit history as snapshots and coverage. These are required
owner corrections, not reasons to weaken financial assertions or bypass gates.
