# NEXT packet implementation progress

This records implementation state for the application-owned v2 work packets
NEXT-01 through NEXT-25. It separates **implemented source** from **verified
behaviour**, because at the time of writing nothing in this effort has been
observed at runtime. See [Verification limits](#verification-limits) before
relying on any row here.

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
| NEXT-03 … NEXT-25 (20 packets) | — | — | not started | none |

NEXT-01 is complete. NEXT-02, NEXT-11, NEXT-13, NEXT-20 and NEXT-49 are merged.
The remaining 20 first-wave packets are untouched, so the only dependency edges
satisfied by merged source are those NEXT-01, NEXT-02, NEXT-11, NEXT-13, NEXT-20
and NEXT-49 themselves unblock.

## What was implemented

### NEXT-11 — Separate complete-book SIE4E export

A distinct application-owned export, not a second movement-transfer path. One
book-scoped transaction captures the complete book and retains the account,
balance and journal-line membership. Exact bytes are then rendered and
re-parsed by the *existing* inbound SIE parser outside every transaction, and
a short second transaction binds the verified object manifest to the exact
model and renderer. The retained `openerp-sie4i-v1` transaction transfer is
preserved byte-for-byte.

**It refuses rather than approximates.** A book that declares any dimension
effective as-of the capture refuses with `UnsupportedProfile` naming the
dimension and the missing assignment owner; a dimension-free book emits
`#TRANS … {}` and carries an explicit limitation that emptiness means *nothing
is assigned*, not that an assignment was reviewed. No 4E record matrix was
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

## Verification limits

No database, Worker, provider credential or real company data was available
during this work. Therefore:

- `bun run check`, `bun run lint`, `bun run check-types` and `bun run build` all
  pass on the merged tree. That is **source- and type-level evidence only**. A
  typecheck is not a substitute for observing a transaction.
- **Unobserved:** every migration applying cleanly to a fresh database; grant
  matrices matching the runtime role; transaction and rollback behaviour; lock
  ordering under contention; same-key replay, same-key recovery and
  different-key duplicate conflicts; approval expiry and revocation; the
  idempotency conflict path; the empty-filtered-page cursor case; anchor
  validity; stale-dependency branches; and every HTTP and MCP surface end to
  end. No browser session, no `tools/call` and no Worker invocation was made.
- NEXT-13's four packet vectors were evaluated in a throwaway `bun` process
  against the exported pure function. That is **arithmetic evidence only** —
  not a transaction, not concurrency, not a database — and it is not retained
  as a test, because `AGENTS.md` forbids adding tests without explicit approval.
- NEXT-11's unobserved surface is the same in kind: no database, no renderer
  invocation, no re-parse, no HTTP call and no browser session. In particular
  the "exact bytes are re-parsed by the existing inbound SIE parser" step has
  never executed, and no SIE destination or statutory acceptance is
  established or implied.
- No Swedish tax, VAT, payroll or statutory compliance claim is made or
  supported by any of this work.

Closing these gaps requires a real PostgreSQL instance, the 0001–0005
migrations applied under maintenance credentials, an operator-scoped book with
accounts and retained evidence, and — for NEXT-02's activation flow to succeed
at all — a reviewed `rule_releases` row for one family.

## Reserved work

The five reserved WIP assignments remain untouched and were not reimplemented,
requalified or taken over: `WIP-VAT03`, `WIP-FX02-P1`, `WIP-AST03-UI`,
`WIP-VAT04-A1`, `WIP-COM2-W1`. NEXT-02 and NEXT-13 consume none of them.
