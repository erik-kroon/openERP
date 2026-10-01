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

## DF-02 — Two legitimate identical documents cannot both be retained

**Severity: highest.** The schema directly contradicts our own written requirement.

**Evidence.** `apps/api/migrations/0001-schema.sql:288`:

```sql
CONSTRAINT evidence_book_id_sha256_key UNIQUE (book_id, sha256)
```

Our requirement in [capability-backlog](capability-backlog.md#supplier-inbox-and-extraction) says the opposite: *"Deduplicate retries by source identity without collapsing distinct documents merely because their bytes match."*

**Consequence.** Two genuinely distinct occurrences of a byte-identical document in one book — the same receipt filed twice, the same invoice PDF attached to two payments — cannot both exist. The second is either rejected or silently merged. This is exactly the BFL retention case the requirement was written for, and it is worse for documents than for vouchers because a document is the *evidence*, not the assertion: losing one occurrence loses the audit trail that the transaction happened twice, or that two payments shared one invoice.

**Fix.** Separate **content** from **occurrence**, which the domain already does elsewhere (`intake_occurrences` exists and is a distinct table). Deduplicate on a source identity that names the occurrence, and let identical content be referenced by more than one occurrence. The content-addressed artifact tables (`accountant_review_artifacts` and friends) are the right model and already bind an exact `octet_length` — copy that shape.

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

## DF-08 — A locked period has no database-level guard, and the runtime role can set the flag

**Severity: high.** Class A.

**Evidence.** `apps/api/migrations/0001-schema.sql:319` — `locked boolean DEFAULT FALSE NOT NULL`. `apps/api/migrations/0003-roles.sql:214` grants `UPDATE (locked)` on `openerp.periods`. No trigger and no check constraint reads the column; `0002-integrity.sql` has 210 triggers and none of them is a period lock. Enforcement is application-only, e.g. `apps/api/src/application/commerce/cancellations.ts:69`.

**Consequence.** A closed Swedish accounting year that can still receive vouchers is a restatement with no annual meeting behind it. The integrity layer is described as preventing "malformed or damaged history", and a voucher in a locked period is exactly that — so this sits inside the existing allowlist rather than extending it. Separately, the runtime role can both set and clear the flag with no constraint on either, in a schema that is otherwise scrupulous about column-scoped grants.

**Fix.** A period-lock guard on the voucher and document-anchor paths, reading the flag and refusing. The shape already exists in our own `check_calendar` and it already takes the book lock first, which matches the ADR lock order. The guard must have **no bypass**: locking is a voluntary internal control with no legal deadline, while the business events it would strand do have one. And a guard whose own query fails must leave the period **open** — never treat a failed check as a pass.

---

## DF-09 — No aggregate cap on credits against one invoice

**Severity: high.** Class A. Named explicitly in ADR 0010 as a database responsibility ("aggregate integrity").

**Evidence.** `apps/api/migrations/0001-schema.sql:2963` gives `supplier_credits` only `CHECK (amount_minor > 0)`. Nothing relates the **sum** of credits referencing one invoice to that invoice's amount.

**Consequence.** A supplier invoice can be credited a hundred times for its full amount and the database is silent. Partial credit is legally permitted, so a naive total cap is wrong too — the invariant is that the sum may not exceed the original.

**Fix.** Take the lock on the original row **before** summing, because under read-committed two concurrent credits would each read the pre-insert sum. Two supporting rules from the same comparison, both worth keeping: a null status counts as **live**, never as cancelled, because that is the direction to fail in; and the refusal message must not carry the original's figures, because it can then be read by a caller who should not see them.

Related and worth stating in the same change: `invoice_cancellations` carries `UNIQUE (book_id, register_invoice_id)`, a hard one-to-one cap. That is defensible for a **full** cancellation and wrong for a **partial** credit. Confirm which the record is meant to be and record the answer in the domain document.

---

## DF-10 — Failures carry no machine code at the boundary and no retry class anywhere

**Severity: high.** Class A.

**Evidence.** `apps/api/src/index.ts:167-182` (`boundaryResponse`) emits `{ message }` with no `code` for any failure raised outside a declared error channel. `packages/contracts/src/accounting-errors.ts` has thirteen codes mapped to seven statuses. `PeriodLocked` and `StaleDependency` are both 409; `InvalidJournal` and `UnsupportedProfile` are both 422. There is no retryable/permanent bit in the domain, the contract, or the transport.

**Consequence.** An HTTP client or an agent cannot tell "do not retry" from "retry", and a 503 from a misconfiguration is body-identical to a 503 from a transient deadlock. `InvalidJournal` alone conflates at least eight distinct remedies — account not in the chart, lines unbalanced, a line carrying both sides, a negative side, no covering period, period closed, period locked — so no caller can name the fix. Several packets already require the opposite: a named reason on excluded candidates, and distinct refusal reasons so the interface can name the remedy.

**Fix.** Three changes, in order of value. **Every** boundary response carries the stable code. The domain failure type gains a three-valued recovery class — permanent, transient, outcome-unknown — assigned per code and never inferred from prose, with an unrecognised code defaulting to outcome-unknown rather than to either extreme. And split the coarse codes so each has one remedy; keep the existing status map, which is correct.

One discipline worth recording alongside it: an **infrastructure** failure must never be reported as a credential revocation. We get this right centrally today, in the database failure mapping, because a spurious 401 makes a client delete its entire cached grant.

---

## DF-11 — No voucher-date-inside-its-period guarantee

**Severity: medium-high.** Class A. Both products miss it; we can do it cleanly.

**Evidence.** `openerp.vouchers` carries `posting_date` and a foreign key to its period, and the two are never reconciled. The reference only checks it inside function bodies, repeated in roughly twenty later migrations.

**Consequence.** A voucher can be dated outside the period it belongs to. The roll-forward arithmetic and every continuity check read the date, so this silently misstates opening balances and makes a year look continuous when it is not.

**Fix.** A guard on the voucher path that the date lies inside the referenced period, using the same overlap test and the same book lock that `check_calendar` already uses. A date-range overlap test is a few lines.

---

## DF-12 — A bank match need not point at the settlement account, and its sign is unchecked

**Severity: medium-high.** Class A.

**Evidence.** `bank_matches` is `PRIMARY KEY (book_id, statement_id, row_ordinal)` plus `UNIQUE (book_id, voucher_id, line_id)` — one observation to one line, which is structurally excellent. But nothing requires the matched line to sit on the cash settlement account, and nothing requires its sign to agree with the observation amount, which is a **signed** minor-unit value.

**Consequence.** A match can point at a revenue line. Under the cash method, where no receivable is booked and the settlement side is the only cash anchor, that is the difference between a reconciled account and a wrong one.

**Fix.** Require the matched line to be on the settlement account with the matching sign. Check the **direction**, not the whole amount: one payment can consume part of a transaction, and an invoice-currency amount is not the bank-currency amount.

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
