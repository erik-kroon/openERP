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

The table below is a **selected** record, not a complete index. It covers
NEXT-01 … NEXT-50; the third, fourth and fifth waves NEXT-51 … NEXT-125,
all vendored 2026-09-28, have **no rows and no implementation state**, and the absence of a row is not a finding that the work
is missing from source. See the [dossier plan](12-next-implementation-dossier.md)
for the full packet index and the reserved owners.

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
| NEXT-07 | Supplier paid credits and refunds | P1 | implemented end to end on the released leaf: `0029-next-07.sql` principal-increase/review/approval/receipt/allocation/source-usage tables, `contracts/supplier-refunds` paid-credit and refund-receipt operations plus the position and cutoff history, `purchases/refunds` prepare/approve/execute owner and `db/purchases/refunds` tx-passing reads and DML, HTTP routes and read-only MCP capabilities; the paid split reuses the existing supplier credit rows and the next 07 domain leaf unchanged | G125000 P100000 K50000 Q25000 split into apRelease 25000 and refund 25000, two cash refunds 10000 then 15000, over-capacity 16000 refused, duplicate credit identity refused and a standalone payment reversal after the posted refund refused, exercised over real HTTP against the restricted-role chain through 0029 with `next-07-paid-credit-refund-journey.json`; corporate tax, real-company VAT and provider settlement remain unobserved |
| NEXT-18 | Incremental open-item FX remeasurement | P1 | leaf implemented and reviewed: per-item control binding, unique execution membership, bounded money, all supported scale pairs and empty-population decisions repaired; valuation posting/effects persistence remain with the commerce FX owner | [Before/after domain probes and fast/full static gates](evidence/next-18-leaf-review.md) pass; HTTP/MCP valuation journey unobserved |
| NEXT-30 | Customer unapplied cash, paid credits and refunds | P1 | leaf implemented and reviewed: adopted receipt/refund clearing journals balance without repeated cash, and reversals compare retained prior/posterior credit consequences; legal issuance and posting/persistence remain with the commerce owners | [Before/after domain probes and fast/full static gates](evidence/next-30-leaf-review.md) pass; HTTP/MCP journey unobserved |
| NEXT-38 | Cash-method recognition and unpaid year-end cutover | P0 | **deferred at the commerce owner**: the former financial writer took the cash amount from the request and reused an already-posted accrual invoice. Its three write routes now refuse `UnsupportedProfile`; the read-only route remains available for retained rows. The leaf and migrations are retained, with the missing invoice/payment/year-end owner contract recorded in `domain-leaf-integration.json` | [Boundary and delivery prerequisites](evidence/next-38-cash-method.md); no valid financial recognition or final-cash E2E claim |
| NEXT-05 | General-rule cross-border service purchases | P0 | implemented: `@open-erp/domain/service-purchases` compiler, `vat` release general-rule section, `0025-next-05.sql` recognition/review/approval tables, `purchases/service-purchases` prepare/approve/execute owner, HTTP routes plus read-only MCP capabilities, and actual-return capture of boxes 21/22/30/31/32 with 48 | packet vectors plus a pure return vector executed; 0001–0025 chain applies on fresh PostgreSQL with DDL/grant probes; 9 existing E2E tests pass with 0025 applied; service financial journey unobserved |
| NEXT-43 | Reviewed dimension restatement without editing journals | P1 | leaf implemented: `@open-erp/domain/dimension-restatement` sealed restatement preview with financial-immutability guard, report-time `classificationAt` resolution, and revision-append with replay/stale semantics; overlay persistence and report capture remain with the dimension/report owners | packet vectors executed against the pure compiler; HTTP/MCP journey unobserved |
| NEXT-31 | Invoice-linked prepayments and accrued-cost true-up | P1 | **wired and observed 2026-09-29**: the declared deferral was stale — the subledger schedule owner has existed and this packet names it as the thing to reuse. Leaf plus owner `apps/api/src/application/subledger/prepayments.ts` extending that owner, not a second scheduling engine, with tx-passing reads `apps/api/src/db/subledger/prepayments.ts`, contract `packages/contracts/src/prepayments.ts` and forward `0039-next-31-prepayments.sql`. The released schedule, its revisions and its occurrences stay where they are; the new tables record only the recognition-to-schedule link and the invoice resolution. The cost excludes deductible input VAT, so deferring changes expense timing and never a VAT tax point. Read-only MCP capability `subledger_read_accrued_cost` | [Real E2E over workerd + PostgreSQL 17.11 + restricted `e2e_runtime` role, source inventory stable](evidence/next-31-prepayments-review.md): 12000 over two daily-weighted periods splits `5950`/`6050` with the residual on the last installment and the halves summing to exactly the cost; a second basis over one schedule and a basis over a missing schedule both refuse; a 10000 accrual resolves to 0 remaining across two invoices with true-ups `0` and `+500`; the same invoice under a new key, a different service identity and over-consumption all refuse, the last rolling back with the accrual untouched; `vat_fact_components` stays empty. 167 tests across 41 files pass. No vendor invoice import, schedule-occurrence posting or VAT return line exists |
| NEXT-37 | VAT assessment ownership and exact-to-assessed bridge | P0 | reviewed/repaired in `c5075fe`, forward `0031-next-37-review.sql`: obligation-owned posted effects, current independent approval, actual tax-owner adoption and atomic new posting/matching, server-derived discrepancies and renewable unexecuted proposals | [Real HTTP/MCP and integrated E2E proof](evidence/next-37-review-repair.md): 35 focused integration cases, then 38 including the NEXT-07 document-number repairs, pass; signed synthetic statement movements only, real-company/provider qualification remains open |
| NEXT-33 | Employee expense claims with one financial handoff | P1 | leaf implemented: `@open-erp/domain/employee-claims` claim review with single-meaning components, exclusive payout-route selection, guarded route replacement, and the pre/post-payment correction boundary; purchase posting, payroll execution and payment instruction remain with their owners | packet vectors executed against the pure compiler; HTTP/MCP journey unobserved |
| NEXT-35 | Variable pay, absence and holiday-liability reconciliation | P2 | leaf implemented: `@open-erp/domain/variable-pay` work-timeline normalization, exact variable components with multi-base routing, holiday rollforward with qualified valuation, control adjustment, and liability release on payment; withholding/contribution calculation and pay-run posting remain with their owners | packet vectors executed against the pure compiler; HTTP/MCP journey unobserved |
| NEXT-45 | Direct cash-flow statement with a full reconciliation bridge | P1 | **wired and observed 2026-09-28**: leaf plus owner `apps/api/src/application/reports/cash-flow-statement.ts`, tx-passing read `apps/api/src/db/reports/cash-flow-statement.ts`, contract `packages/contracts/src/cash-flow.ts` and HTTP `POST /v1/entities/:entityId/books/:bookId/cash-flow`. Owner derives opening and actual closing cash from retained journal lines, resolves each cash leg from the reviewed role of its counterpart inside the same voucher, and never infers a transfer from equal and opposite amounts without the owned `result_transfer_v1` posting purpose. Read-only: no new migration | [Real E2E over workerd + PostgreSQL 17.11 + restricted `e2e_runtime` role, 32-migration chain, source inventory stable](evidence/next-45-cash-flow-review.md): the packet's exact vector reconciles to a zero difference, an unclassifiable counterpart stays unclassified with its reason and `complete: false`, a cash-to-cash movement without the owned identity refuses, and a mapping naming no retained account is refused. Read-only MCP capability `reports_cash_flow_statement` added and observed; no persisted snapshot and no UI in this slice. The owned-transfer **success** path is unreachable today: `result_transfer_v1` is admission-gated to the financial close and never moves cash, so no operation can produce a cash-to-cash owned transfer |
| NEXT-36 | Paid payroll recovery and retroactive compensation | P1 | leaf implemented: `@open-erp/domain/paid-payroll-recovery` gross recovery with untouched withholding, future-pay adjustment without simultaneous receivable, same-claim idempotency, original-specification AGI identity and reporting-only revision; run/reporting persistence and filing remain with the payroll owners | packet vectors executed against the pure compiler; payroll journey unobserved |
| NEXT-48 | Bolagsverket submission and authority-outcome lifecycle | P1 | leaf implemented: `@open-erp/domain/filing-lifecycle` governance-gated preparation, replay-first admission, the honest provider state table, and rejection/correction linkage with receipt quarantine; provider calls and persistence remain with the external-delivery owners | packet vectors executed against the pure compiler; authorized provider exercise unobserved |

| NEXT-40 | Foreign-currency cash holdings and transfers | P1 | reviewed/repaired: bounded minor-unit input validation at one journal chokepoint, capacity and remaining-carrying checks, both currency scales in reporting valuation (a scale-asymmetric pair had been valued 100x low), explicit book-currency and capacity-version assertions, and refusals for foreign-to-foreign exchange and consumed history | [50 before/after schema/domain probes and static gates](evidence/next-40-foreign-cash-review.md) pass (23/27 failing before, 50/50 after); no HTTP/provider/database journey exists, and the leaf still has no occurrence identity or replay guard |
| NEXT-08 | Payment instruction resolution and replacement | P1 | **wired and observed 2026-09-28**: leaf plus owner `apps/api/src/application/purchases/payment-resolutions.ts` extending the supplier payment-batch/export owner, tx-passing reads `apps/api/src/db/purchases/payment-resolutions.ts`, contract `packages/contracts/src/payment-resolutions.ts` and HTTP `POST …/commerce/supplier-payment-resolutions` plus replacements. Owner derives the instruction per export item from retained bytes, evaluates only satisfiable proof branches, and refuses everything else. Read-only MCP capability `payments_resolve_instruction`; replacement stays operator-side. No migration | [Real E2E over workerd + PostgreSQL 17.11 + restricted `e2e_runtime` role, 32-migration chain, source inventory stable](evidence/next-08-payment-resolutions-review.md): unknown stays unknown with the missing proof named, a recorded rejection does not become proof, settled refuses, replacement without release refuses, unknown exports refuse, and the agent receives the same honest state. No proof branch is currently satisfiable, so no release has been observed; the success paths activate when an exclusive channel record or provider-authenticated cancellation is retained |
| NEXT-09 | Complete provider sync windows | P1 | **wired and observed 2026-09-29**: leaf plus owner `apps/api/src/application/banking/sync-windows.ts` extending the bank connector owner, tx-passing reads `apps/api/src/db/banking/sync-windows.ts`, contract `packages/contracts/src/bank-sync-windows.ts`, forward `0036-next-09-sync-windows.sql` and HTTP `POST …/banking/sync-windows` plus `/pages`, `/publications` and `/state`. The published cursor moves only with its publication marker, so a staged generation is never a reviewed bank observation. Publication takes the caller's own fence and the stream `UPDATE` names the expected version, fence and base cursor and checks the affected row count. Read-only MCP capability `banking_read_sync_window` | [Real E2E over workerd + PostgreSQL 17.11 + restricted `e2e_runtime` role, 37-migration chain, source inventory stable](evidence/next-09-sync-windows-review.md): one marker per complete window with the cursor advanced once, a resumed generation keeping its base and staged pages, a superseded fence refused at both the page and publication boundaries, a page re-offer replayed and a different raw response refused as a conflict, a mutation restart opening at the published cursor rather than the failed page cursor, and an unchanged empty poll publishing `coversHistory: false`. 155 tests across 38 files pass. No provider call and no job exist, so no Plaid behaviour is observed |
| NEXT-10 | Provider revisions to reviewed bank observations | P1 | **wired and observed 2026-09-29**: the declared deferral was stale — bank intake already retains provider observations, and NEXT-09 retains the exact provider bytes behind every published change. Leaf plus owner `apps/api/src/application/banking/source-revisions.ts`, tx-passing reads `apps/api/src/db/banking/source-revisions.ts`, contract `packages/contracts/src/bank-source-revisions.ts` and forward `0037-next-10-source-revisions.sql`. The caller names a page ordinal, a record ordinal and a provider transaction identity; the owner reads the retained provider bytes, parses the exact decimal lexeme as a rational decimal, converts it to whole minor units at the profile's scale and flips the sign, so no amount and no status is ever taken from the request. Admission adopts an existing statement-backed observation with cited evidence and never creates a second one, because `bank_observations` is keyed by statement. Read-only MCP capability `banking_read_provider_observation` | [Real E2E over workerd + PostgreSQL 17.11 + restricted `e2e_runtime` role, source inventory stable](evidence/next-10-provider-revisions-review.md): `"12.50"` at scale 2 interprets to `-1250` and `"0.05"` to `-5`; a fractional minor unit, an identity absent from the retained bytes and an unpublished generation all refuse; a pending flag in the bytes overrides the request's; admission refuses a missing observation, missing evidence and a repeated revision, and succeeds once with `resolvedObservationCount: 1`; a removal produces a case with `cashMovementMinor: null` and leaves the observation, its admission and zero vouchers untouched. 164 tests across 40 files pass. No provider call, posting, matching or reconciliation signoff exists |
| NEXT-27 | Reviewed party identity resolution without balance merging | P1 | **wired and observed 2026-09-29**: leaf plus owner `apps/api/src/application/commerce/party-identity.ts` extending the party directory, tx-passing reads `apps/api/src/db/commerce/party-identity.ts`, contract `packages/contracts/src/party-identity.ts` and HTTP `POST …/commerce/party-identity` plus balances. Owner derives members from retained counterparty revisions with all identifiers honestly unverified, requires cited retained evidence for same-entity claims, and groups retained open obligations by resolved identity without netting across parties, roles or currencies. Read-only MCP capability `directory_read_balances`; resolution prepare stays operator-side. No new table; receipts in command_receipts | [Real E2E over workerd + PostgreSQL 17.11 + restricted `e2e_runtime` role, source inventory stable](evidence/next-27-party-identity-review.md): same-entity resolution on reviewed evidence with refusal without it, related classification, unknown-party and outside-canonical refusals, staleness-safe balance grouping, and the agent receiving grouped balances without an identity-decision tool |
| NEXT-39 | Processor balance and payout clearing, Stripe first | P1 | leaf reviewed/repaired: signed observations, explicit dispute/payout capacity, scoped occurrence identities and balanced bounded journals; closing helpers remain arithmetic diagnostics, with fetching/profiles/persistence owned by treasury/banking | [42 before/after schema/compiler probes and static gates](evidence/next-39-leaf-review.md) pass; provider/storage journey unobserved |
| NEXT-34 | Mileage reimbursement with exact tax and payout partition | P2 | leaf implemented: `@open-erp/domain/mileage-reimbursement` exact distance split with half-up rounding, disjoint exempt/payroll handoff identities, same-trip idempotency, unreviewed-route and missing-fact refusal, and consumed-delta correction with lawful basis; handoff execution stays with the claim/payroll owners | packet vectors executed against the pure compiler; payroll journey unobserved |
| NEXT-50 | Agent book context, deltas and cross-domain unresolved-work index | P0 | leaf implemented: `@open-erp/domain/agent-context` module-completeness guard, goal-ordered work ranking with blocker collapsing, owner/identity delta semantics with fresh-capture on grant change, and payment settlement hints; capture, adapter reads and receipts remain with the capability owners | packet vectors executed against the pure compiler; HTTP/MCP journey unobserved |
| NEXT-39 | Processor balance and payout clearing, Stripe first | P1 | leaf reviewed/repaired: signed observations, explicit dispute/payout capacity, scoped occurrence identities and balanced bounded journals; closing helpers remain arithmetic diagnostics, with fetching/profiles/persistence owned by treasury/banking | [42 before/after schema/compiler probes and static gates](evidence/next-39-leaf-review.md) pass; provider/storage journey unobserved |
| NEXT-46 | Peppol invoice and credit exchange through a selected access point | P1 | leaf implemented: `@open-erp/domain/peppol-exchange` BIS amount reconciliation with credit structure and original reference, stable dispatch admission with semantic-buyer check and lost-response recovery, and inbound envelope handling with integrity incidents and duplicate candidates; transport, validation and persistence remain with the delivery owners | packet vectors executed against the pure compiler; network journey unobserved |
| NEXT-24 | K2 annual-report semantic model and iXBRL | P1 | reviewed/repaired: financial facts are sealed from the retained statement rows they name instead of copied from client input, signed amounts reach the sealed draft so a loss is reportable, comparatives must be distinct prior fiscal years, the K2 release is pinned, narrative approval is the retained four-eyes approval, the presentation derives every displayed value, and the renderer emits well-formed XHTML over a pinned synthetic taxonomy | [45 before/after schema/domain probes and static gates](evidence/next-24-annual-report-review.md) pass (5/31 failing before, 45/45 after); no E2E journey exists or was run, no qualified validator, synthetic non-statutory taxonomy only |
| NEXT-25 | Fixed-revision company rehearsal and restore | P0 | leaf implemented: `@open-erp/domain/rehearsal-verification` acceptance inventory with unknown-blocking and waiting handoffs, backup-manifest verification with no certificate on gaps, field-by-field restore comparison with retained differences, drift refusal and dispatch-fence proof; actual checkpoint capture, backup, restore and exercise remain with the operations owner under separate authority | packet vectors executed against the pure compiler; rehearsal exercise unobserved |
| NEXT-47 | Document signatures bound to exact content and purpose | P1 | leaf implemented: `@open-erp/domain/document-signatures` purpose-bound intent freezing, authentic completion with digest/signer/environment checks and replay, distinct signer-set coverage, revocation-split eligibility, and unknown-start retention; provider protocol and receipts remain with the signing adapter owners | packet vectors executed against the pure compiler; cryptographic journey unobserved |
| NEXT-12 | Historical open-item adoption | P1 | leaf implemented: `@open-erp/domain/historical-adoptions` residual adoption with full_history/opening_set exclusivity, pool capacity conservation and unknown-history preservation, execution-time conservation check, new-settlement remaining math without double-subtracting history, residual-credit refusal, and pool/live control assertions; journals stay empty with GL delta 0 and persistence remains with the sie/historical and commerce settlement owners | packet vectors executed against the pure compiler; HTTP/MCP journey unobserved |
| NEXT-19 | Disposal with proceeds | P1 | leaf implemented: `@open-erp/domain/asset-disposals` post-impairment carrying removal with unposted-cash and invoiced-proceeds modes, clearing-or-qualified-reclassification branch with no second AR/cash/VAT recognition, gain/loss legs, double-proceeds refusal and execution-time conservation; schedule retirement and disposition persistence remain with the reserved asset owner | packet vectors executed against the pure compiler; HTTP/MCP journey unobserved |
| NEXT-23 | Financial close and single-count carry-forward | P1 | reviewed/repaired in `a03aca4` with forward `0030-next-23-review.sql`: current executed tax/control basis, independent current approval, raw account openings, exact delta reclose, approved/durable reopen and prior-year posting fence | [Real HTTP close/reclose/opening/reopen proof](evidence/next-23-review-repair.md): 27 focused cases and 26 combined NEXT-07/37/admission/persistence cases pass; synthetic qualification only |
| NEXT-21 | Payroll posting, payslip and AGI artifact | P1 | leaf implemented: `@open-erp/domain/payroll-runs` pay-run journal with derived net payables and no benefit double-expense, same-key single posting, full-payment evidence with paid-period reporting, AGI aggregation over recorded withholding with reconciliation bridge, same-identity amendment with withholding-decrease review, and unpaid-only correction; cash movement, rendering and submission remain with the payroll owners | packet vectors executed against the pure compiler; HTTP/MCP journey unobserved |
| NEXT-44 | Multi-year SIE partition and dimension-preserving import | P1 | leaf implemented: `@open-erp/domain/sie-partitions` scoped voucher identities, unique-year partition with blocking diagnostics, final-versus-history totals, declaration-bound object mapping with source-code retention, unknown-control refusal, UB/IB single link and paused-run checkpoints; parsing, staging and admission remain with the SIE owners | packet vectors executed against the pure compiler; migration journey unobserved |
| NEXT-28 | Authorized collection reminders and dispatch recovery | P1 | leaf implemented: `@open-erp/domain/collection-reminders` exact-message sealing and approval, stale-basis admission refusal, idempotent single-attempt recovery on retry, dispute-hold refusal and same-identity unknown-outcome recovery; statements, disputes and provider calls remain with the commerce/delivery owners | packet vectors executed against the pure compiler; external-delivery journey unobserved |
| NEXT-32 | Loan principal, interest accrual and repayment allocation | P2 | leaf implemented: `@open-erp/domain/loan-lifecycle` principal timeline, exact-rational segmented accrual with single half-up rounding and idempotent cumulative targets, accrual/repayment journals and posted-principal adoption; schedules, persistence and the D-04 lending-scope decision remain open with the future subledger/owners port | packet vectors executed against the pure compiler; treasury journey unobserved |
| NEXT-41 | Late FX valuation and consumed-chain correction | P1 | leaf implemented: `@open-erp/domain/fx-chain-repair` frozen-fact replay with corrected-rate valuation, owner-supplied paired releases, per-date/role desired-versus-old diffs, cash/foreign conservation and final-carrying agreement, staleness and closed-period refusals; posting, revision advance and downstream review remain with the owning transaction while accepted scope stays open | packet vectors executed against the pure compiler; FX journey unobserved |
| NEXT-42 | Economic impairment reversal and zero-carrying assets | P1 | leaf implemented: `@open-erp/domain/impairment-reversal` role-reconciled carrying, without-impairment counterfactual, capped economic reversal with footing schedule, qualified zero-carrying write-down, loss-free zero disposal, revival refusal and consumed-correction guard; schedule persistence and disposal records remain with the asset owners | packet vectors executed against the pure compiler; valuation journey unobserved |

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

### NEXT-05 — General-rule cross-border service purchases

A general-rule service purchase is its own economic event with its own sealed
plan, journal group, book-currency payable and signed reverse-charge
components. The pure calculation lives in
`@open-erp/domain/service-purchases`: `classifyGeneralService` binds the
service kind and origin class to the qualified release selection, and
`compileCrossBorderService` converts the original liability and the SEK tax
base through separate explicit witnesses, derives the output tax from the
qualified rate and the deductible input from the reviewed fraction, and posts
cost, reverse-charge input, reverse-charge output and payable as one balanced
group. All three packet vectors hold exactly, and a nonzero source tax, an
unsupported kind or class, a special place-of-supply exception and a duplicate
line are refused.

**The release carries the section; nothing defaults it.** The `vat` rule
release gains an optional `generalRuleServices` section with the supported
kinds, origin classes, exact rate rows with their 30/31/32 output boxes, and
the tax and deduction rounding. A release without the section cannot recognize
a service and is refused. Report boxes 21/22/30/31/32 join the shared box
vocabulary; the net payable now adds reverse-charge output alongside domestic
output, which changes no existing return.

**Reuse, not a second register.** The owner binds the existing supplier draft
and evidence workflow, the shared journal kernel with a new `service_purchase`
posting owner kind, and `createInvoiceInTransaction` for the supplier payable,
which stays book-currency. The payable control and the input VAT account
resolve to the same retained controls the domestic purchase owner uses, so the
VAT return already reconciles them; only the reverse-charge output account is
operator-placed, and the return's control reconciliation is the backstop for
it. The original currency amount and both conversion witnesses are retained in
the sealed body. No FX register is written: foreign-currency original-unit
obligation tracking stays NEXT-17's, and a first implementation that books the
payable in book currency with retained witnesses is exactly what the packet
allows. The actual return reads each sealed component once and declares the
21/22 basis, the 30/31/32 output and the 48 input from it, with the sealed
boxes cross-checked against the qualified rate row.

Deliberate omissions, recorded rather than smoothed over:

- **No web UI.** State is carried explicitly in the review, approval and
  receipt records, matching the NEXT-15 precedent.
- **MCP exposes reads only** (review, history, recognition). Mutations are
  HTTP operator operations, matching the acceptance and FX owners.
- **No service-credit follow-up.** Per-line originals are retained in the
  sealed body for a later credit owner; no mutable capacity table was added
  for a writer that does not exist yet.
- **A received-date tax point is refused.** Supplier drafts carry no received
  date evidence in this owner, so only document and supply bases are
  supported.
- **No reviewed general-rule release ships.** Until one exists every command
  is refused with `UnsupportedProfile`, which is designed behavior, not a
  default.

Runtime evidence, kept as observations rather than committed tests: the three
packet vectors plus refusal cases executed against the pure compiler in a
throwaway process; the full `0001`–`0025` chain applies on a fresh PostgreSQL
with the new tables, widened box/origin checks, immutable triggers and
runtime grants probed; a pure actual-return vector declares 21/30/48 with a
zero net and `filingReady: true` on reconciled controls; the existing
credit-document, posting and persistence E2E suites pass (9 tests) with 0025
applied. The service prepare/approve/execute financial journey itself remains
unobserved.

### NEXT-23 — Financial close and single-count carry-forward

The full owning transaction on top of the released leaf compilers, which are
consumed unchanged. `prepareYearClose` seals the applicable-family inventory
(statements and corporate tax verified natively against the sealed NEXT-13
snapshot and NEXT-22 bridge; any other family claimed required is a blocker
and only dated not-applicable evidence is retained), the after-tax profit
from the snapshot's own untransferred result line, and the close basis
version. `advanceYearClose` recaptures the basis, seals the domain final
proposal with the transfer delta D = P - F, and retains the balance-sheet
opening target. `approveFinalProposal` is a separate human approval with
expiry; `executeFinalClose` enforces four-eyes separation, rechecks the
conservation boundary inside the same transaction after the transfer posts,
then commits the transfer effect, the derived opening set, the certificate
and the year period locks atomically. A zero delta posts no voucher but still
seals the no-effect transfer, opening, certificate and locks.

**The transfer is recognizable, not a plain adjustment.** A new
`result_transfer_v1` posting purpose travels on the transfer vouchers through
a dedicated action variant, gated to the `financial_close` owner in admission
and validation; the statement owner recognizes exactly that purpose as an
owned transfer, which is the handoff its read anticipated with the empty
purpose list. The nominal transfer and year-result equity accounts are
reviewed operator input verified active and distinct; the statement mapping
identifies the technical transfer role, which this owner never assigns.

**Status is derived, never stored.** Closed, ready, preparing,
adjustments-pending and open follow from the preparation/proposal/
certificate/reopen rows, so no status column can drift. Reopen is one atomic
step rather than the packet's prepare/execute split: the downstream
enumeration (later openings, certificates and statement snapshots) and the
period unlock must see the same membership, and a consumed downstream year
refuses with its exact dependency list retained on the sealed refusal record.

Deliberate omissions, recorded rather than smoothed over:

- **No web UI and MCP exposes reads only**, matching the service-purchase
  precedent. Mutations are HTTP operator operations.
- **No reviewed transfer-account mapping is verified.** The operator's
  statement release must map the nominal account technical; the owner checks
  activity, not mapping.
- **Cascade reopen is refused.** Any consumed downstream year blocks with its
  list; multi-year cascade repair is future work.
- **No reviewed fiscal year, snapshot, bridge or release ships.** Every
  command is refused until those qualified inputs exist.

Runtime evidence, kept as observations rather than committed tests: all
packet vectors and refusal cases executed against the leaf compilers in a
throwaway process; the full `0001`–`0026` chain applies on a fresh PostgreSQL
with the seven tables, immutable triggers and runtime grants probed; the
existing posting, persistence and supplier-drafts E2E suites pass (8 tests)
with 0026 applied. The close financial journey itself remains unobserved.

### NEXT-24 — K2 annual-report semantic model and iXBRL

The full owning pipeline on top of the released leaf compilers, which are
consumed unchanged. `prepareAnnualReport` seals the draft against the active
NEXT-23 close certificate and the exact NEXT-13 snapshots, with the K2
framework release, disclosure requirements, taxonomy concept mappings and
every non-ledger fact as reviewed sealed input. Unknown mandatory facts keep
the report a draft; only K2 exists as a profile and anything else is refused
rather than templated. `approveAnnualReport` is a separate human approval
with expiry; `finalizeAnnualReport` enforces four-eyes separation, seals the
semantic model and commits the render intent to the outbox atomically — no
journal posts. `prepareReportPresentation` checks every displayed value
against its sealed source and reconciles the declared total through explicit
presentation-only rows. `renderReportArtifact` assembles deterministic XHTML
from the same presentation data through reviewed concept mappings and retains
the bytes with their content hash.

**Validation pending is a retained state, not a pass.** No qualified native
XBRL validator is released, so every artifact carries
`pending_qualified_validator`: preserved draft evidence that blocks artifact
acceptance, exactly as the packet requires. A process exit code with a
skipped document stage could never pass here because no stage is ever
claimed. Signatures stay NEXT-47's: the manifest carries a null signature
scope until a signature event exists, and an adoption after signing is that
owner's verification, never this one's assumption.

Deliberate omissions, recorded rather than smoothed over:

- **No web UI and MCP exposes reads only**, matching the close precedent.
  Mutations are HTTP operator operations.
- **Duration contexts are refused by the assembler.** The leaf emits instant
  contexts only; a duration period fails its validation rather than rendering
  a wrong context.
- **No cascade rendering service.** The render intent commits to the generic
  outbox and the same named render operation serves an artifact worker later;
  in this release the operator invokes it directly, which the packet's
  no-extra-service rule permits.
- **No reviewed taxonomy, framework data or company facts ship.** Concept
  QNames, contexts, units and the framework release are qualified operator
  input on every command.

Runtime evidence, kept as observations rather than committed tests: all
packet vectors and refusal cases executed against the leaf compilers in a
throwaway process; the full `0001`–`0027` chain applies on a fresh PostgreSQL
with the five tables, immutable triggers and runtime grants probed; the
existing posting and persistence E2E suites pass (7 tests) with 0027 applied.
The report financial journey itself remains unobserved.

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
