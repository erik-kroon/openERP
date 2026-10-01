# Reference-derived defect register

Status: **dated reference findings with subsequent repair records.** Prepared
2026-09-26 by reading the cited source. Fixed rows name their later implementation
and observed evidence; unclosed rows retain the original finding and must be
reconciled against the current checkout before work starts. This defect register
is separate from the forward [parity backlog](11-parity-backlog.md), which is new scope.

Placement is governed by [ADR 0013](../adr/0013-reference-derived-defects.md): every fix is a **forward migration or a forward packet**. The reviewed three-file baseline is never edited.

Severity is accounting risk, not effort.

## How to read a row

Each row names what is wrong, the evidence, the consequence in accounting terms, and the smallest honest fix. `Class` reuses the [parity backlog](11-parity-backlog.md#how-to-use-this-backlog) rule-adoption classes: **A** adopt an algorithm, **B** structure only with dated parameters, **C** re-derive a legal judgement.

Two rows are not defects but **contradictions between our own files**. Those are the most dangerous kind, because a reader of either file in isolation is right.

---

## DF-01 — Voucher balance remains closed after commit — qualified

**Original severity: highest.** Class A. **Qualified 2026-10-01: the claimed
post-commit hole is not reachable under the composed reviewed constraints.**

**Composition.** The deferred voucher check admits exactly N balanced lines;
positive bounded ordinals and per-voucher ordinal uniqueness then exhaust every
permitted slot. Immutable voucher count/identity and journal lines prevent reopening
that set. The missing second trigger and unused function branch are not, by
themselves, a missing guarantee. No redundant integrity trigger was added.

**Observed acceptance.** [The qualification record](evidence/df-01-voucher-completeness.md)
contains real late-insert and mutation refusals, deferred missing-line/unbalanced
commit faults, complete rollback and same-key recovery. The full local suite passes
195 tests across 51 files.

**Actual repair.** Direct commit-time Effect SQL errors now use the same PostgreSQL
classification as wrapped Drizzle failures, preserving authentic `InvalidJournal`
instead of misreporting it as `Unavailable`. The reviewed baseline is unchanged.

---

## DF-02 — Identical supplier acquisitions retain distinct occurrences — qualified

**Original severity: highest. Qualified 2026-10-01 for the served source-retention
and supplier-inbox owners.**

**Evidence.** `apps/api/migrations/0001-schema.sql:288`:

```sql
CONSTRAINT evidence_book_id_sha256_key UNIQUE (book_id, sha256)
```

Our requirement in [capability-backlog](capability-backlog.md#supplier-inbox-and-extraction) says the opposite: *"Deduplicate retries by source identity without collapsing distinct documents merely because their bytes match."*

**Corrected scope.** Legacy evidence is content-addressed, not an acquisition
register. The served source-retention owner already separates `intake_contents`
from `intake_occurrences`; supplier inbox entries reference occurrences rather
than merging acquisitions by hash. Evidence uniqueness alone does not prove
that this acquisition path loses provenance.

**Observed acceptance.** [The qualification record](evidence/df-02-occurrence-multiplicity.md)
proves two identical inline originals, distinct source identities and inbox entries,
one shared content object, exact original-byte retrieval, retry convergence,
changed-byte conflict and REST/MCP discovery parity without financial effects.
No duplicate retention owner or schema change was needed.

**Limits.** This proof covers synthetic inline CSV acquisitions. It does not
claim external object-storage/PDF qualification, two payment bindings, or that
the legacy evidence endpoint itself records distinct acquisition events.

---

## DF-03 — Derived P&L excludes captured result transfers — fixed

**Severity: high.** Class A. **Implemented and observed 2026-10-01.**

**Corrected scope.** Raw trial balance must include the whole ledger. The actual
current close posts a mechanical result-account transfer rather than clearing
every nominal account. The served family reader incorrectly treated that transfer
as ordinary cost, and its role catalogue also failed SQL projection before the
financial mismatch could be observed.

**Repair.** New P&L families consume the statement owner's admitted transfer
classification at their saved source cutoff, retain exact transfer membership,
and expose a signed bridge. Ordinary cost on the same account is retained. Raw
trial balance, ledger drill-down and older family interpretation remain intact;
legacy families receive a truthful read-view limitation instead of rewritten data.

**Observed acceptance.** [The delivery record](evidence/df-03-profit-transfer-bridge.md)
records the served failure and real close/report/MCP/browser journey. Expense
`61000` is explained as ordinary cost `5000` plus mechanical transfer `56000`;
income `75000` and tax `14000` remain exact. Frozen and legacy snapshots retain
their own bases. Seventeen focused E2E tests pass.

**Boundary.** The retained family surface reuses the released statement
classification; it does not introduce another financial transfer owner, rewrite
the raw trial-balance basis or claim statutory/company qualification.

---

## Revision note

This register was first written against an earlier revision. Re-verification against the current one confirmed every other row unchanged, and corrected this one: the semantic profit-and-loss and balance-sheet snapshot work landed between the two, and it already solves the underlying problem in a way this register's original recommendation would have duplicated. A defect row that outruns the code it describes is worse than no row, because it sends an implementer to fix something that is already right.

---

## DF-04 — Saved-request state refusals preserve their identity — fixed

**Severity: high.** Class A.

**Implemented and verified 2026-09-30.** Forward `0043-posting-request-attempts.sql`
adds immutable attempts beside the existing saved body/kernel identity. The
application uses the pure posting-line validator to prove content-invalid
journals terminal, permits explicit unchanged retry of referenced-state refusals,
and retains old outcomes untouched. The shared kernel no longer blocks reserved
keys merely because they have a historical refusal; actor/operation/body identity
checks remain. The UI runs the original key rather than replacing it.

**Observed acceptance.** [The repair record](evidence/df-04-saved-request-retry.md)
includes restored reviewer authority, concurrent same-key execution, legacy
refusal preservation, pure-content terminal replay, identity conflict, late-write
rollback and original-key recovery, MCP preparation retry and the real browser
flow. The complete local synthetic suite passed 182 tests across 46 files.

**Boundary.** Retryability does not bypass current authority or make an obsolete
plan current. A changed command still needs new reviewed bytes. Committed outcomes
and request-content refusals remain absorbing; unexpected infrastructure failures
remain unknown rather than fabricated refusals. No company readiness is claimed.

---

## DF-05 — SIE account-code width is consistent — fixed

**Severity: high.** Internal contradiction.

**Implemented and verified 2026-09-30.** The domain `AccountCode` owns the
one-to-eight ASCII-digit lexical contract consumed by the parser, mapping/control
schemas and movement renderer. Source prefixes remain strings, not numeric
normalization. Malformed account declarations retain their original bytes and
diagnostics. The separate complete-book export keeps its explicit four-digit
profile and no BAS or financial-admission policy is inferred from code shape.

**Observed acceptance.** [The repair record](evidence/df-05-sie-account-codes.md)
contains real movement export, retained interpretation, reviewed mapping and
staging for `1`, `19301`, `19301234` and `0012`, plus malformed identifier refusal
and preserved UTF-8 byte locations. Fourteen local E2E cases pass, including the
existing SIE4E dimension and retained-version recovery cases.

**Boundary.** This fixes format disagreement, not financial import or chart
classification. Source staging creates no destination vouchers and does not
establish actual-company or external-recipient acceptance.

---

## DF-06 — Thirty-three hand-rolled copies of the calendar-date rule, in three disagreeing versions

**Severity: high.** Class A.

**Evidence.** `grep` for the `T00:00:00Z` round-trip idiom across `apps/*/src`, `packages/*/src` and `jurisdictions/se/src` (excluding build output) returns **33 occurrences across 27 files**. They implement three different accepted ranges:

| Where | Accepted year range | Mechanism |
| --- | --- | --- |
| `packages/contracts/src/company-setup.ts:12-23`, `payroll-foundation.ts:12-19` | `>= "0001-01-01"` | `Date.parse` plus round-trip |
| `jurisdictions/se/src/sie/encoder.ts:22` | rejects a leading `"0000"` | prefix check |
| the remaining application files | **no lower bound at all** | `Date.parse(v + "T00:00:00.000Z")` plus round-trip |

**Consequence.** `0000-06-15` is a valid date to the application and invalid to the contract and to the SIE encoder. A value can be accepted by a capability, stored, and then rejected by a different surface with no way to explain why.

**Fix.** One implementation, one accepted range, one message, imported everywhere. Keep the two types distinct: a **shape** contract that is deliberately loose, because it is the transport and storage format, and a **real calendar date** refinement used at human entry. Blurring them would reject legitimately retained source bytes that are not yet interpreted. Then add a **count ratchet** to the existing anti-slop checks so a thirty-fourth copy fails the build — the reference has exactly this and it is the only mechanism that actually holds.

---

## DF-07 — There is no Swedish business date anywhere

**Severity: high.** Class A.

**Evidence.** `grep "Europe/Stockholm"` across `apps`, `packages`, `jurisdictions` and `infra` returns **one** hit, which is not a business-date computation. `apps/web/src/lib/company-work.ts:12` computes the current period as:

```ts
const today = new Date().toISOString().slice(0, 10);
const period = setup.periods.find((p) => p.startsOn <= today && p.endsOn >= today) ?? setup.periods.at(-1);
```

**Consequence.** A Swedish company whose fiscal year contains the 31st, viewed at 00:30 CET on the 1st, is placed in the **previous year** on the company overview, and the default bank-workspace query window is a day out. More seriously, that value anchors the exchange rate for a foreign invoice, so it silently selects **the wrong day's rate** on a deadline.

**Fix.** Arithmetic on dates stays UTC — adding days and measuring day distance must not move across a daylight-saving boundary. **Today** is the Stockholm calendar day, resolved server-side through an injectable clock so it is testable, and **sent to the client in the setup payload** so a browser in any timezone renders the same day the server scoped the period to. Never ship a timezone library for this: it is one zone and one platform call.

---

## DF-08 — Locked periods refuse new financial writes and invoice anchors — fixed

**Severity: high.** Class A.

**Implemented and observed 2026-10-01.** Existing application owners already refuse
locked-period posting and recognition anchors. Before repair, synthetic final-write
faults could lock the period after application admission and still commit a voucher
or a new `commerce_invoices` recognition anchor.

**Repair.** Forward `0046-period-lock-integrity.sql` checks the current referenced
period under the book and period locks after both final inserts. Locked periods
refuse `PeriodLocked`; missing periods refuse rather than passing a null check.
There is no trigger bypass flag. Retained vouchers in a later-locked period remain
valid, and committed receipt replay stays available without new writes.

**Observed acceptance.** [The repair record](evidence/df-08-period-lock-integrity.md)
contains both real HTTP failure vectors, complete transaction rollback, original-key
recovery and receipt replay after locking. Twenty-six focused E2E tests pass across
admission, close/reopen, accrual/cash-method refusal, persistence and outer-boundary
integration.

**Corrected authority scope.** The trusted application intentionally retains
`UPDATE (locked)` for its reviewed closing and reopening workflows under ADR 0010.
Removing that grant would break the adopted owner, not improve end-user authority.
This guard protects a currently locked period; it does not turn SQL into a second
approval engine or defend against a compromised backend clearing the flag. Source
retention is not a financial anchor and remains outside the guard. Actual-company
reopening and statutory readiness remain separate qualification gates.

---

## DF-09 — Retained supplier credits respect original capacity — fixed

**Severity: high.** Class A. Named explicitly in ADR 0010 as a database responsibility ("aggregate integrity").

**Implemented and observed 2026-10-01.** Forward `0047-supplier-credit-cap.sql`
locks the book and original supplier invoice before checking all retained credit
amounts. It admits partial credits through the exact original cap and refuses
existing excess during migration preflight. [The delivery record](evidence/df-09-supplier-credit-cap.md)
corrects the earlier public-workflow claim: the application already checks capacity;
the injected final-write overflow previously caused a later schema failure and
rollback, not demonstrated successful over-credit. It now refuses `InvalidJournal`
at the retained integrity boundary. Eleven E2E cases cover exact capacity,
rollback/recovery, competing credits and related supplier/persistence regressions.

**Evidence.** `apps/api/migrations/0001-schema.sql:2963` gives `supplier_credits` only `CHECK (amount_minor > 0)`. Nothing relates the **sum** of credits referencing one invoice to that invoice's amount.

**Invariant.** The sum of all retained supplier credits must not exceed the
original gross amount; equality and partial credits are valid.

**Boundary.** No nullable status excludes retained credits, and refusal messages
do not expose original figures. Financial policy and approval remain application-owned.

The separate `invoice_cancellations` owner reverses the full original amount;
its one-to-one constraint is not the partial supplier-credit model and is unchanged.

---

## DF-10 — Failures carry no machine code at the boundary and no retry class anywhere

**DF-10A delivered 2026-10-01.** [Outer boundary codes](evidence/df-10-boundary-codes.md)
now preserve tagged accounting errors and expose stable body-refusal codes with
pre-routing recovery semantics. Five real Worker boundary/diagnostics E2E cases
pass. The domain-wide recovery taxonomy and remedy-code split below remain open;
this row is not marked fully repaired.

**Severity: high.** Class A.

**Evidence.** `apps/api/src/index.ts:167-182` (`boundaryResponse`) emits `{ message }` with no `code` for any failure raised outside a declared error channel. `packages/contracts/src/accounting-errors.ts` has thirteen codes mapped to seven statuses. `PeriodLocked` and `StaleDependency` are both 409; `InvalidJournal` and `UnsupportedProfile` are both 422. There is no retryable/permanent bit in the domain, the contract, or the transport.

**Consequence.** An HTTP client or an agent cannot tell "do not retry" from "retry", and a 503 from a misconfiguration is body-identical to a 503 from a transient deadlock. `InvalidJournal` alone conflates at least eight distinct remedies — account not in the chart, lines unbalanced, a line carrying both sides, a negative side, no covering period, period closed, period locked — so no caller can name the fix. Several packets already require the opposite: a named reason on excluded candidates, and distinct refusal reasons so the interface can name the remedy.

**Fix.** Three changes, in order of value. **Every** boundary response carries the stable code. The domain failure type gains a three-valued recovery class — permanent, transient, outcome-unknown — assigned per code and never inferred from prose, with an unrecognised code defaulting to outcome-unknown rather than to either extreme. And split the coarse codes so each has one remedy; keep the existing status map, which is correct.

One discipline worth recording alongside it: an **infrastructure** failure must never be reported as a credential revocation. We get this right centrally today, in the database failure mapping, because a spurious 401 makes a client delete its entire cached grant.

---

## DF-11 — Voucher dates remain inside their accounting periods — fixed

**Severity: medium-high.** Class A. **Implemented and observed 2026-10-01.**

**Reproduced.** Synthetic write faults through the real HTTP posting owner committed
vouchers dated before and after their referenced period. The baseline foreign key
establishes period identity, not date containment.

**Repair.** Forward `0044-voucher-period-date.sql` checks the final inserted voucher
against the book/year/period bounds and refuses period-boundary edits that would
strand retained vouchers. It locks the book and referenced period, admits both
endpoints, and fails migration preflight on inconsistent existing history rather
than rewriting it. Financial workflow and approval remain application-owned.

**Observed acceptance.** [The repair record](evidence/df-11-voucher-period-date.md)
records authentic `InvalidJournal` HTTP refusals, complete financial rollback,
original-key recovery, endpoint admission and retained-date protection. Seven
focused E2E tests pass, including DF-01 completeness regression coverage.

**Boundary.** No new UI or transport owner is needed: all posting consumers reach
the guarded voucher table and existing shared refusal mapping. This is synthetic
local integrity proof, not company readiness or a period-reopening policy.

---

## DF-12 — Bank matches retain the settlement account and observed direction — fixed

**Severity: medium-high.** Class A. **Implemented and observed 2026-10-01.**

**Corrected scope.** The current application already admits only whole-row exact
matches on the statement account, with the exact signed amount and statement
interval. The genuine missing layer was retained relational integrity: synthetic
final-write faults could redirect an admitted match to the wrong account or sign
while the public command still returned success.

**Repair.** Forward `0045-bank-match-integrity.sql` checks the final match against
the retained statement account and observation direction. It refuses inconsistent
existing matches during migration preflight rather than rewriting them. The
immutable source, journal and match records preserve this relationship afterward.

**Observed acceptance.** [The repair record](evidence/df-12-bank-match-integrity.md)
records separate same-sign/wrong-account and correct-account/opposite-sign HTTP
refusals, source-revision and receipt rollback, exact-key recovery and retained
target verification. Existing reference ranking, partial capacity and migration
rerun/checksum coverage passes with the repair.

**Boundary.** The SQL guard compares direction, not magnitude. Exact-match
application admission remains exact; partial consumption remains owned by reviewed
allocation plans. No foreign-currency equivalence, payment authority, new match
workflow or company readiness is claimed.

---

## Observed but not yet defects

Three more findings are recorded here because they will become defects, and the decision belongs to an owner rather than to a comparison.

**A payroll revision cannot move its effective date.** `apps/api/migrations/0001-schema.sql:2319` puts `effective_on` on **both** sides of the `payroll_revision_predecessor_fk` composite key, so `supersedes` can only point at a revision with an identical effective date. Either that is deliberate — a correction is same-date, a change is a new revision — or the column is a copy from the logical-identity key beside it. **Do not change blind.** Compare the sibling counterparty current-revision foreign key, which correctly does not repeat the discriminator.

**The minor-units ceiling is stated twice, differently.** The domain says `1e38`; two signed bank columns carry a 37-digit literal. Cosmetic, but in a file whose whole claim is reviewed DDL it reads as drift rather than intent.

**Every runtime binding is optional.** `apps/api/src/runtime/environment.ts:5-17` declares them all with `?`, and `apps/api/src/index.ts:185` falls back with `||` on the **database connection string**. If both sources are absent, the failure surfaces as a connection error on the first financial request instead of a typed configuration failure at start. Model the bindings as a validated construction that fails with a named code.

---

## What is already better here, and must not regress

Recording this so a later reader does not "fix" the target toward the reference. On money, immutability, idempotency, tenant scoping and revision chains, our baseline is ahead of what the reference's 999 migrations arrived at. Specifically: one exact minor-units domain against scattered rounding expressions; a one-sided line shape enforced declaratively, which the reference has no equivalent of; grant-level append-only, where the reference needs layered triggers plus four session escape hatches; idempotency as a permanent immutable receipt rather than an expiring cache; content-addressed sealed records with a canonical JSON digest; lock ordering encoded in the schema rather than fought for in twenty migrations; immutable book monetary units; and a single typed refusal channel instead of free-text exceptions the application has to pattern-match.

The reference is a **rule catalogue**, not an architecture to converge on. Take the rules; keep the design.

## Maintaining this register

A row closes when its fix is implemented and its acceptance is met, and is then replaced by a statement of what was built and where the evidence lives. A row that is judged not to be a defect moves to the [parity backlog](11-parity-backlog.md) as forward scope, with the reason recorded. Add a row when a comparison, a review or a runtime observation surfaces one, and record the evidence line so a later reader can tell a current fact from a proposal.

Run `python3 docs/plans/check-plan.py` after any change to this directory. It validates links, anchors and whitespace; it does not execute product tests and it does not verify any row in this register.
