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
| NEXT-13 | Semantic P&L and balance-sheet snapshots | P0 | implemented | none |
| NEXT-03 … NEXT-25 (22 packets) | — | — | not started | none |

NEXT-01 is complete. NEXT-02 and NEXT-13 are merged. The remaining 22 packets
are untouched, so no dependency edge in the packet graph is yet satisfied by
merged source except those NEXT-01, NEXT-02 and NEXT-13 themselves unblock.

## What was implemented

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
- **`docs/plans/evidence/planning-integrity.json` is stale for this file.** The
  document-integrity checker records a file list and per-file hashes. Adding
  this note changes that set. The checker was deliberately not run, because
  `docs/` had concurrent uncommitted edits at merge time and regenerating would
  have clobbered them. Run `python3 docs/plans/check-plan.py` and reconcile
  `docs/plans/README.md` in a separate change.

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
