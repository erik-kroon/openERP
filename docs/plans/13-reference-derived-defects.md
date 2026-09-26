# Reference-derived defect register

Status: **findings from a reference comparison, verified against the current checkout.** Prepared 2026-09-26. Every row was confirmed by reading the cited file in this repository; the evidence line is the current state, not a proposal. This document claims no fix, no test and no runtime observation. It is a register of things the comparison surfaced that are wrong, contradictory or silently unsafe **now**, and it is deliberately separate from the forward [parity backlog](11-parity-backlog.md), which is new scope.

Placement is governed by [ADR 0013](../adr/0013-reference-derived-defects.md): every fix is a **forward migration or a forward packet**. The reviewed three-file baseline is never edited.

Severity is accounting risk, not effort.

## How to read a row

Each row names what is wrong, the evidence, the consequence in accounting terms, and the smallest honest fix. `Class` reuses the [parity backlog](11-parity-backlog.md#how-to-use-this-backlog) rule-adoption classes: **A** adopt an algorithm, **B** structure only with dated parameters, **C** re-derive a legal judgement.

Two rows are not defects but **contradictions between our own files**. Those are the most dangerous kind, because a reader of either file in isolation is right.

---

## DF-01 — The voucher balance guarantee can be bypassed after commit

**Severity: highest.** Class A.

**Evidence.** `apps/api/migrations/0002-integrity.sql:660` attaches the balance guarantee to exactly one table:

```sql
CREATE CONSTRAINT TRIGGER voucher_expected_line_count_voucher
  AFTER INSERT ON openerp.vouchers DEFERRABLE INITIALLY DEFERRED
  FOR EACH ROW EXECUTE FUNCTION openerp.voucher_expected_line_count();
```

The function itself is written for two tables — `0002-integrity.sql:406-416` branches on `TG_TABLE_NAME = 'vouchers'` and an `ELSE` that reads `NEW.voucher_id` and looks the expected count up on the parent. **No trigger is ever attached to `openerp.journal_lines`.** That `ELSE` branch is unreachable. `journal_lines` carries only `immutable_line` (`BEFORE DELETE OR UPDATE`) and `journal_ordinal_bound` (`BEFORE INSERT`).

**Consequence.** The commit-time check that ADR 0010 names as the centrepiece of the SQL allowlist runs **once, when the voucher row is inserted**. A voucher whose lines are added in a later committed transaction is never re-checked for line count or for `debit = credit`. The `ordinal` bound is a real mitigation and must be checked against the intended fix rather than assumed sufficient; the point that is certain is that the balance invariant is not re-established, so `immutable_row` on lines turns a *soft* guarantee into a *permanent* one.

**Fix.** Attach the same function to `journal_lines` as a deferred constraint trigger. The `ELSE` branch is already written and is correct. Confirm against `guard_journal_ordinal` whether a gap in the ordinal sequence is reachable, because that determines whether this is defence-in-depth or a live hole, and record which.

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

## DF-03 — The legacy trial-balance reader will zero the income statement once a result transfer is posted

**Severity: high, and narrowing.** Class A. **Corrected 2026-09-26** — see the revision note; the original finding overstated the scope.

**Evidence.** `apps/api/src/db/reports.ts:208-232` (`readReportTotals`) and `:262-295` (`insertTrialBalanceLines`) still sum **every** voucher in `[startsOn, endsOn]` against a `sequence` cutoff, with no posting-purpose filter and no basis parameter. A search of that file for a basis parameter returns nothing.

**What already fixed the real problem.** The semantic statement path added since the first version of this register does **not** need a basis parameter, and this is a better answer than the one originally proposed here. `packages/domain/src/statements.ts` derives a virtual untransferred result from *owned transfer receipts* — a mechanical transfer is excluded from ordinary profit and loss only when a receipt that owns it retains it — and reports the balance identity residual explicitly. So on that path the income statement is correct whether or not a transfer has been posted, the balance sheet closes on the whole fiscal year to date, and a first year does not imply a zero opening.

**Consequence that remains.** The legacy trial-balance snapshot reader is a separate surface with the original defect. A result transfer mirrors every profit-and-loss account into the result account inside the same fiscal period, so on that reader the income statement reads zero across the board while the balance sheet still ties — a failure no total reveals. Whether it is reachable depends on whether anything still calls it once the semantic path is the served one.

**Fix.** Do **not** add a basis enum to the legacy reader. First establish whether the legacy trial-balance snapshot is still a served surface; if it is, the correct fix is to route statement consumers to the semantic path and retire the duplicate reader rather than to maintain two report conventions. If it must stay, its exclusion rule must reuse the semantic path's owned-receipt test instead of introducing a second, divergent notion of what a transfer is.

---

## Revision note

This register was first written against an earlier revision. Re-verification against the current one confirmed every other row unchanged, and corrected this one: the semantic profit-and-loss and balance-sheet snapshot work landed between the two, and it already solves the underlying problem in a way this register's original recommendation would have duplicated. A defect row that outruns the code it describes is worse than no row, because it sends an implementer to fix something that is already right.

---

## DF-04 — A state-dependent refusal permanently burns a saved request

**Severity: high.** Class A.

**Evidence.** `apps/api/migrations/0001-schema.sql:2360-2371` gives `posting_request_outcomes` a primary key on `(book_id, key)` plus `posting_outcome_immutable`. `isPersistableRefusal` in `apps/api/src/application/posting-recovery.ts:152-164` places `ApprovalRequired`, `StaleDependency`, `PeriodLocked`, `AlreadyPosted` and `NotFound` in the persistable set.

**Consequence.** A grant that is activated afterwards, a period that is reopened, or an approval that arrives a moment later **cannot be applied to the original request**. The stored refusal is returned for ever and the caller must mint a new idempotency key. That contradicts [ADR 0010](../adr/0010-application-owned-accounting-replacement.md) ("never creates a fresh economic command automatically") and instructs the UI in `docs/frontend.md` not to do it. The identity is absorbing on a *committed* outcome; it should not be absorbing on a refusal that only referenced domain state.

**Fix.** Split refusal kinds deterministically from the request bytes alone. A refusal determined by the **content** of the request needs new bytes and consumes the identity. A refusal determined only by **referenced state that could change** leaves the identity runnable, so the same bytes succeed later. The decision must not be a hand-maintained list at the call site.

---

## DF-05 — Our own two files disagree on how wide an account number is

**Severity: high.** Internal contradiction.

**Evidence.**
- `packages/contracts/src/sie-import.ts:76` — `sourceAccount: Schema.String.check(Schema.isPattern(/^[0-9]{4}$/))`
- `apps/api/src/application/sie-import-parser.ts` uses the same four-digit rule
- `jurisdictions/se/src/sie/encoder.ts:73` — `if (!/^[1-9][0-9]{0,7}$/.test(account.code) || codes.has(account.code))`

**Consequence.** We refuse to **import** a chart containing an account number we will happily **export**. A migration that legitimately carries a five-to-eight digit account fails at intake with no explanation, and the failure looks like a corrupt file rather than a schema disagreement.

**Fix.** One named account-code schema owned by the domain, referenced by the contract, the parser and the encoder. The widest supported form wins, because a narrower importer is a data-loss risk and a wider importer is a validation risk we can name. Two supporting rules from the same comparison, both class A: an account number is an **identifier, never a number** (arithmetic on one is always a bug, and a numeric type invites it), and the BAS account class is read **positionally** from the leading digit in exactly one place.

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
