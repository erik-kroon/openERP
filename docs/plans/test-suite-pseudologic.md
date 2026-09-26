# Test pseudologic for the refactored workflows

Status: **pseudologic for review. Not test code.** No test file is created by this document, and
no expectation here was produced by running our own calculator — every literal is derived from the
contract, from BAS, or is marked in §9 as needing a domain owner. Per `docs/verification.md:7` these
outcomes are specified *before* implementation, which is the only order in which they are worth
anything.

Scope: the five workflows refactored in commit `5ac3433`, which have **zero** automated coverage
today. Context and evidence-gathering rationale: `docs/plans/test-suite-design.md`.

## 0. How to read this

Each workflow opens with its **guard ladder** — the ordered sequence of rejections as the code
actually executes them, extracted from source. The ladder is the spine, because *ordering* is the
thing a refactor can silently break and the thing no type checker sees.

```
G<n>  <condition>                                   →  <FailureCode>
```

Then cases are written against the ladder. Three case kinds:

- **H** happy path — asserts the committed financial effect, exact.
- **R** rejection — asserts the code *and* that nothing was written.
- **X** exclusivity — asserts which of two mutually exclusive outcomes can land (races, replays).

A case never asserts only a status code. Every rejection case also asserts the write-set is
unchanged: no voucher, no journal line, no sequence increment, no outbox row, no approval
consumption.

Notation: `SEK` amounts are **minor units as exact decimal strings** (our `MinorUnits`), never
floats. `→` is the public HTTP call. `DB:` is an independent observation on a separate connection
using maintenance credentials, never the caller's session.

## 1. Standing preconditions and harness requirements

Applies to every case below. These are the four things our harness lacks today and that
`accounted`'s `tests/pg/setup.ts` has; without them the cases are theatre.

**HARNESS-1 — Caller/runtime-role split is asserted, not assumed.**
Before any authorization case runs, the harness proves the simulation landed:
```
ASSERT  maintenance role CAN write openerp.commerce_invoices
ASSERT  runtime role   CANNOT write openerp.commerce_invoices
```
Rationale: if the runtime role *can* write, every "refused" case passes vacuously. This is
`withUserContext`'s assert-the-simulation-landed step, and it is the single highest-value thing to
copy.

**HARNESS-2 — Schema/migration sanity gate in `beforeAll`.**
```
ASSERT  every migration recorded in openerp_migrations is applied
ASSERT  named invariants exist: period lock trigger, journal immutability trigger,
        receipt immutability trigger, scoped grants on runtime role
FAIL LOUDLY with "did every migration apply cleanly" if not
```
Rationale: one loud error beats 100 cryptic *"relation does not exist"*.

**HARNESS-3 — Determinism.**
```
CLOCK         frozen at 2026-03-17T00:00:00Z for all cases; no case may read wall time
IDS           every fixture id is a literal, assigned by the fixture builder, never generated
KEYS          every idempotency key is a literal unique to its case
SEED          fresh book per case file; TRUNCATE CASCADE is an explicit table list, so adding a
              table without adding it here fails loudly
PARALLELISM   serial across files; no two cases share a book
```

**HARNESS-4 — Evidence artifact per run** (`verification-strategy.md:47`), into `test-results/e2e`:
case IDs executed, expected vs observed, fixture provenance + profile/rule/schema versions,
migration set hash, runtime + PostgreSQL versions, clock/locale/timezone, and the **independent DB
observation dump**. Fixture tokens excluded.

**STANDING-1 — Every guard gets a firing case AND a non-firing neighbour.** Taken from
`accounted-bench`'s `scripts/selftest-ledger-env.ts`: seed a known-bad state, assert the guard
*fires*, then move one field to make it valid and assert it now *passes*. A guard never proven to
fire is not a guard. This is also how `verification-strategy.md:33` is satisfied — *"Demonstrate
that a deliberately wrong expectation fails, without weakening product validation."*

**STANDING-2 — Idempotency is asserted on every happy path.** Same key + same payload → one
receipt, byte-identical on replay, and no second write. Same key + different payload → explicit
conflict, original receipt untouched.

**STANDING-3 — Cross-tenant refusal is indistinguishable from not-found** (T3), and the case
asserts the state is unchanged *as well as* the error shape.

---

## 2. Sales order write path — `commerce/sales-orders.ts`

### 2.1 Guard ladder

`writeDocument` after replay:

```
G1   book currency missing OR authority != "native"        → Forbidden
G2   encoded request body > 65536 bytes                    → InvalidJournal
G3   id present AND document row absent                    → NotFound
G4   expectedDigest present AND (head absent OR digest mismatch
                                    OR revision mismatch)  → StaleDependency
G5   create AND book already holds >= 200 documents        → InvalidJournal
G6   NOT create AND head.revision >= 50                    → InvalidJournal
G7   head AND action in {revise, accept} AND state != draft → InvalidJournal
G8   action == cancel AND head.state == cancelled          → InvalidJournal
G9   action == cancel AND head.kind == order
                       AND >=1 conversion exists          → InvalidJournal
G10  action == order_from_quote AND (kind != quote
                                 OR state != accepted)    → InvalidJournal
G11  resolved content absent                               → InvalidJournal
```

Pre-ladder: `replay` on `(idempotencyKey, operation="sales_document_command")`. On hit, return the
stored receipt immediately and **skip G1–G11 entirely** — that skip is itself a case.

`create` is `NOT head OR action == "order_from_quote"` (note: an `order_from_quote` action on an
existing quote is still a *create*, producing a new document id).

### 2.2 Cases

**SO-H1 — create quote, then order from it (exercises the whole ladder clean).**
```
GIVEN  book with authority=native, 0 sales documents, one counterparty
WHEN  create quote  { kind: quote, content: 1 line × 10000 SEK net + 2500 VAT, rate 25 }
THEN  201, receipt.documentId = <literal>, revision = "1", state = draft
      DB: 1 row in sales documents; digest = sha256 over canonical JSON of the stored body
          (recompute independently, do NOT read the digest back and compare to itself)
      DB: voucher_sequences for this series UNCHANGED  (a quote is not a voucher)
```
*Independence note:* the digest assertion must be recomputed from the returned body using
`canonicalizeJson`, then compared. Reading `row.digest` and comparing it to `response.digest` only
proves the response echoes the row.

**SO-H2 — revise a draft; revision increments and prior revision is retained.**
```
GIVEN  SO-H1's quote, state=draft
WHEN  revise { id, expectedDigest: <H1 digest>, expectedRevision: "1", content: +1 line }
THEN  revision = "2", previousDigest = H1 digest
      DB: 2 revision rows, both present, both independently re-digestable
```

**SO-H3 — accept transitions draft → accepted; order_from_quote on an accepted quote creates the order.**
```
GIVEN  accepted quote with revision R
WHEN  transition { action: order_from_quote, expectedDigest, expectedRevision: R }
THEN  new document, kind=order, state=accepted, revision="1"
      sourceQuoteId = quote id, sourceQuoteRevision = R
      DB: exactly 1 conversion-guard invariant holds — quote is now consumed
```

**SO-R1 → G1** — book authority is `imported`, not `native`.
```
WHEN  any write on that book
THEN  403 Forbidden
      DB: 0 documents, 0 revisions, sequences unchanged, no receipt row for the key
```

**SO-R2 → G2** — request body exceeds 65536 bytes *after* encoding (a 700-line content array).
```
THEN  422 InvalidJournal
      DB: write-set identical to pre-call snapshot, INCLUDING no receipt row
```
*Why it matters:* G2 is a size check on the serialized input. Assert the boundary both ways —
65536 bytes accepted, 65537 rejected. A test at 10× the limit proves nothing about the edge.

**SO-R3 → G3** — revise a document id that does not exist in this book.
```
THEN  404 NotFound
      DB: unchanged. AND: an id that exists in ANOTHER book must also give NotFound,
          not Forbidden — a distinguishable code here leaks book existence.
```

**SO-R4 → G4, the digest ladder** — three cases, one per disjunct, because a compound guard
hides behind any single one:
```
G4a  expectedDigest = wrong sha256, revision correct     → StaleDependency
G4b  expectedDigest correct, expectedRevision = "1" when head is "2"  → StaleDependency
G4c  revise against a document that does not exist      → NotFound (G3 fires first, not G4)
```
G4c is the important one: it proves G3 precedes G4 in the ladder, i.e. **ordering is asserted, not
assumed.**

**SO-R5 → G5** — 200 documents already exist, attempt a 201st.
```
THEN  422 InvalidJournal
      DB: still exactly 200. This is the off-by-one witness: 199 must SUCCEED and produce 200.
```

**SO-R6 → G6** — drive revision to 50, attempt 51.
```
THEN  422 InvalidJournal, DB: revision still "50", and 50→49 must be allowed (guard is >= 50,
      not > 50 — prove the boundary from both sides)
```

**SO-R7 → G7** — revise an *accepted* quote. And the neighbour: revise a *draft* must succeed.
```
THEN  422 InvalidJournal, DB: revision unchanged
```

**SO-R8 → G8/G9** — cancel a cancelled quote; cancel an order that already has a conversion.
```
THEN  422 InvalidJournal in both, DB: state unchanged
```

**SO-R9 → G10** — order_from_quote against a *draft* quote (wrong state), and against an
*order* (wrong kind). Both → StaleDependency-shaped rejection; DB unchanged.
Neighbour: an **accepted quote** must succeed (SO-H3).

**SO-X1 — replay returns one receipt.**
```
WHEN  same key + same payload twice, concurrently
THEN  both responses carry the SAME documentId and digest
      DB: exactly 1 document row, exactly 1 receipt, sequence incremented at most once
```
Mechanism per `verification-strategy.md:35`: a **test-owned barrier**, not `Promise.all` — the
harness observes the first request reaching the write lock before releasing the second. Assert the
overlap was observed, or the case proves nothing.

**SO-X2 — same key, different payload** → `IdempotencyConflict`, original receipt and balances
unchanged.

**SO-X3 — two concurrent order_from_quote on the same accepted quote.** Only one may land
(accounted's `quote-source-conversion-guards` serialises on the quote row). The loser observes
`StaleDependency`; DB shows exactly one order and one conversion.

---

## 3. Supplier credit basis — `purchases/credit-basis.ts`

The longest ladder in the refactor, and the one where my refactor moved the most code. Highest
priority.

### 3.1 Guard ladder (as executed, verified against source)

```
 1  book.profile != synthetic-core-v1 OR authority != native  → UnsupportedProfile
 2  invoice.direction != supplier                             → NotFound
 3  no acceptance row for invoice                             → UnsupportedProfile
 4  profile ↔ acceptance.profile mismatch                    → UnsupportedProfile
      (purchase  → swedish-purchase-v1
       zero-tax  → synthetic-manual-supplier-v1
       gross-cost→ synthetic-gross-cost-supplier-v1)
 5  staleness: ANY of
      invoice.blockers non-empty
      invoice.outstandingMinor is null
      outstandingMinor != expectedOutstandingMinor
      allocationVersion != expectedAllocationVersion
      currentRevision.revision != expectedInvoiceRevision
      acceptance.digest != acceptanceDigest                  → StaleDependency
 6  no credit-conflict row                                    → InternalError
 7  conflicts.exported                                        → StaleDependency
 8  conflicts.numberUsed                                      → IdempotencyConflict
 9  conflicts.evidencePosted                                  → AlreadyPosted
10  amount <= 0 OR amount > outstandingMinor                  → StaleDependency
11  credit evidence row absent                                → MissingEvidence
12  voucher absent OR creditDate < issuedOn
                    OR creditDate < voucher.postingDate      → InvalidJournal
13  creditDate not a real calendar date                       → InvalidJournal
14  control line absent OR accountId mismatch
      OR creditMinor != invoice.amountMinor OR debitMinor != 0 → StaleDependency
--- branch on profile ---
S1  creditLines present (non-purchase)                        → InvalidJournal
S2  gross-cost profile without taxMinor                      → InvalidJournal
S3  review tax total is null                                  → UnsupportedProfile
S4  zero-tax profile with tax != 0 OR tax > amount
      OR tax + prior tax > review tax total                   → InvalidJournal
S5  expense line absent OR action.lines.length != 2           → UnsupportedProfile
S6  expense account is reserved                               → StaleDependency
P1  originalLines empty OR inputVatAccountId absent           → UnsupportedProfile
P2  full credit: amount != invoice total OR prior credits exist
      OR creditLines present                                  → UnsupportedProfile
P3  posted action lines do not reconcile against originalLines→ StaleDependency
P4  duplicate lineIds in creditLines                         → InvalidJournal
P5  unknown lineId, or net/tax outside tolerance, or
    net+tax over the original line, or over prior usage      → InvalidJournal
P6  creditLines total != amount, or taxMinor disagrees        → InvalidJournal
```

### 3.2 Cases

**CB-H1 — synthetic zero-tax, full amount.** The clean synthetic path.
```
GIVEN  supplier invoice 10000 net + 2500 VAT = 12500 gross, accepted, no blockers,
       outstanding 12500, acceptance review tax total 2500
WHEN  prepare { profile: synthetic-zero-tax-supplier-credit-v1, amountMinor: "12500",
                taxMinor: "0", creditDate: 2026-03-17, new evidence, new key }
THEN  200, snapshot.expenseAccountId = the non-control debit line's account,
      snapshot.taxMinor = "0", snapshot.outstanding unchanged
      DB: 0 posted rows (prepare is not execute), receipt row exists
```
Neighbour proving S4's first disjunct: the same request with `taxMinor: "1"` must be rejected.

**CB-H2 — synthetic gross-cost with tax.** Distinct code path, must produce a different snapshot
shape (includes `expenseAccountId` + non-zero `taxMinor`).

**CB-H3 — swedish full credit** (purchase, not partial).
```
GIVEN  accepted purchase invoice 8000 net + 2000 tax = 10000, outstanding 10000
WHEN  prepare { profile: swedish-purchase-full-credit-v1, amountMinor: "10000", taxMinor: "2000" }
THEN  200, snapshot.originalLines present, snapshot.creditLine ABSENT (the key-omission rule),
      snapshot.inputVatAccountId = review's, taxMinor = "2000"
```
*This case is the direct regression witness for the conditional-spread change.* The original code
omitted `creditLines` via `...(partial ? { creditLines } : {})`; my version omits it via an early
return. The assertion that matters is not "creditLines is absent" but **"the decoded snapshot's key
set equals the contract's key set"** — because a decode of an unknown-or-missing optional key can
succeed either way. Assert the exact key set, and assert the digest recomputes.

**CB-H4 — swedish partial line credit, per-line capacity.**
```
GIVEN  two-line purchase, line A 1000 net + 250 tax, line B 1000 net + 250 tax,
       line A already credited in full
WHEN  prepare partial crediting line A again for 200 net + 50 tax
THEN  422 InvalidJournal   (P5: no unpaid capacity on line A)
WHEN  prepare partial crediting line B for 200 net + 50 tax
THEN  200, creditLines = [line B only]
```
*Provenance:* this is `docs/plans/evidence/ap-partial-line-credit-http.md` step 4, which records the
real prior defect — 200/50 was refused *despite* invoice residual 1250, because prior line usage
was read from an execution receipt that does not retain the line snapshot. The fixed forward
migration reads the immutable review instead. **This case must fail if that regression returns.**

**CB-H5 — tax rounding tolerance ±1.** The real artifact: 1600 net with 500 tax at an accepted 25%
line rate → `422`, because 1600×0.25 = 400 ± 1 ≠ 500.
```
1600 / 500 → 422   (documented, from the evidence artifact)
1600 / 400 → 200   (exact)
1600 / 401 → 200   (within +1)
1600 / 399 → 200   (within -1)
1600 / 398 → 422   (outside -1)
```
The ±1 boundary must be probed from both sides; a single "within tolerance" case proves nothing.

**CB-R1 → 5, one per disjunct.** Six cases, because the guard is a 6-way OR and a compound guard
hides behind whichever disjunct you happened to break:
```
blockers non-empty                    → StaleDependency
outstandingMinor forced null          → StaleDependency
wrong expectedOutstandingMinor         → StaleDependency
wrong expectedAllocationVersion       → StaleDependency
wrong expectedInvoiceRevision         → StaleDependency
wrong acceptanceDigest                → StaleDependency
```
All six: DB unchanged.

**CB-R2 → 4, profile compatibility, all four profiles.** Acceptance profile mismatch for each of
purchase / zero-tax / gross-cost → `UnsupportedProfile`. Neighbour: matching pair succeeds.

**CB-R3 → 8 — the un-leakable conflict.**
```
GIVEN  supplier credit number already used, in ANOTHER book
WHEN  prepare with that supplierCreditNumber
THEN  IdempotencyConflict whose body does NOT reveal the other book's invoice id, counterparty,
      or totals.  Assert the response body key set and that no foreign identifier appears in it.
```
This is the T3 property: the *absence of leaked data* is the assertion.

**CB-R4 → 12/13 — date ladder.**
```
creditDate before invoice.issuedOn                → InvalidJournal
creditDate before the recognition voucher date    → InvalidJournal
creditDate == issuedOn == voucher date            → 200   (both comparisons are strict <)
creditDate = 2026-02-30                           → InvalidJournal (G13, real-calendar check)
creditDate = 2026-03-17, not a leap day, fine     → 200
```

**CB-R5 → 14 — control-line mismatch, four disjuncts.** control line absent; wrong account;
`creditMinor != invoice.amountMinor`; `debitMinor != "0"`. All → `StaleDependency`, DB unchanged.

**CB-R6 → P4 — duplicate lineIds in one request.**
```
THEN  422, and specifically NOT silently deduplicated.
```
A dedupe implementation would also "pass" a happy-path case; only the duplicate case distinguishes.

**CB-X1 — concurrent prepares of the same credit.** Independent of the DB, this is
`readPriorCreditLines` racing. Assert with a barrier: at most one snapshot sees zero prior usage,
and the two snapshots' combined capacity does not exceed the invoice.

**CB-X2 — same key twice** → one receipt, byte-identical snapshot digest.

---

## 4. Schedule amendment — `subledger/schedules.ts`

`amendSchedule` covers both `amendFutureDates` and `amendEstimate`.

### 4.1 Guard ladder

```
context:  basis row absent                                    → UnsupportedProfile
          schedule.digest != expectedDigest
            OR basis.digest != expectedBasisDigest
            OR basis does not match revision
            OR a reversal exists for the basis voucher        → StaleDependency
          a disposal exists                                    → AlreadyPosted
          dates amendment AND posting basis unsupported        → StaleDependency
          review evidence absent                               → MissingEvidence
bounds:   current.revision >= revisionBound                   → UnsupportedProfile
          firstOrdinal < 1 OR > occurrence count
            OR replacement empty OR newCount > occurrenceBound
            OR (dates AND newCount != count)                  → InvalidJournal
accounts: not exactly 2 accounts, or either inactive          → InvalidJournal
states:   occurrence state count mismatch                     → UnsupportedProfile
prefix (per already-consumed occurrence, ordinal < firstOrdinal):
          state not posted (and not reversed for estimate)    → UnsupportedProfile
          reversed but voucher wrong/absent, wrong purpose,
            or a correction already exists for it             → UnsupportedProfile
suffix (per replacement period):
          not a calendar date, or <= today, or <= last
            consumed date, or <= effectiveOn, or period/year
            missing, or outside the fiscal year               → InvalidJournal
          period locked                                       → PeriodLocked
          amount missing or <= 0                              → InvalidJournal
          eventKey unresolvable                               → InternalError
reconcile: remaining != input.remainingMinor
            OR remaining + recognized + residual + impaired
               != current cost                                 → StaleDependency
no-op:     occurrence digest unchanged AND (dates OR estimate
            unchanged)                                         → InvalidJournal
```

### 4.2 Cases

**SA-H1 — future-dates amendment, happy path.**
```
GIVEN  asset schedule, 12 monthly occurrences from 2026-04, none posted,
       cost 120000, residual 0, basis effectiveOn 2026-01-01,
       recognized 0, impaired 0
WHEN  amendFutureDates { firstOrdinal: 5, remainingMinor: "80000",
                        periods: [2026-08-01, 2026-09-01, 2026-10-01, 2026-11-01],
                        new evidence, new key }
THEN  200, revision = N+1, occurrences 1–4 unchanged byte-for-byte,
      occurrences 5–12 replaced, newCount = 4 + 4 = 8,
      allocatedMinor = "80000", amendment.kind = future_dates_v1,
      amendment carries NO recognizedMinor/reversedMinor keys
      DB: revision row inserted; prior revision rows untouched
      DB: the 8 ledger occurrence rows reconcile: sum(amountMinor) == "80000"
```
*Direct regression witness* for the conditional-spread change: `recognizedMinor`/`reversedMinor`
must be **absent** for a dates amendment. Assert the amendment's exact key set, not just its
absence of a value.

**SA-H2 — estimate amendment** produces `recognizedMinor`, `reversedMinor`, and
`allocationPolicy: explicit_remaining_minor_v1`, and `amendment.kind = remaining_estimate_v1`
(or `remaining_lifetime_v1` when `newCount != count`).

**SA-R1 → bounds, seven cases, one per disjunct.** 0, count+1, empty replacement, newCount over the
cap, and dates-amendment-that-changes-the-count. Each → `InvalidJournal`, DB unchanged. The last
one is the interesting rule: **a future-dates amendment may not change the occurrence count** —
probe it with newCount = count+1 and count−1.

**SA-R2 → prefix, an occurrence already consumed.** Post occurrence 3, then amend from ordinal 1.
The prefix scan hits a *prepared* occurrence → `UnsupportedProfile`, and specifically **not**
`AlreadyPosted`. This distinction is the whole point of the prefix/suffix split my refactor
created.

**SA-R3 → suffix, a period already in the past.**
```
period.postingDate <= today      → UnsupportedProfile or InvalidJournal (assert the exact code)
period.postingDate <= last consumed date  (non-monotonic replacement) → InvalidJournal
period.postingDate <= effectiveOn         → InvalidJournal
replacement period outside its fiscal year → InvalidJournal
replacement period locked                 → PeriodLocked
```
The first one's code differs from the rest — assert it explicitly rather than folding it in.

**SA-R4 → reconcile.** `remainingMinor` in the request that does not equal the sum of the
replacement amounts → `StaleDependency`. Neighbour: exact match → 200. This is the arithmetic the
reconciliation guard exists for; assert it from both sides.

**SA-R5 → no-op rejection.** An amendment that changes neither occurrences nor the estimate must be
refused with `InvalidJournal`. This is a real product rule (accounted has the analogue in
`quote-source-conversion-guards`' frozen-decision logic) and it is easy to lose in a refactor.

**SA-X1 — concurrent amendments on the same schedule.** Assert with an observed barrier: exactly
one lands, the loser is `StaleDependency`, and only one revision row is added. Per
`verification-strategy.md:35`, `Promise.all` alone does not prove overlap — the harness must
observe the lock.

**SA-X2 — replay** of the same amendment key returns the original receipt and adds no revision.

---

## 5. Historical item admission — `sie/historical-items.ts`

### 5.1 Guard ladder

```
plan digest != input.planDigest                    → StaleDependency
plan not staged                                    → StaleDependency
items already admitted for this plan               → IdempotencyConflict
duplicate sourceIdentity in items, payments, or
  matches                                           → InvalidJournal
per open item:
  assertedState=unpaid       and original != outstanding        → InvalidJournal
  assertedState=partly_paid  and (original==0 or outstanding==0
                            or |outstanding| >= |original|)     → InvalidJournal
  assertedState != unknown   and original*outstanding < 0       → InvalidJournal
  |outstanding| > |original|                                   → InvalidJournal
per payment:
  amount <= 0                                                   → InvalidJournal
  sourceDate missing while chronology == dated_source           → InvalidJournal
  no open item with that sourceAccount+currency                 → InvalidJournal
per match:
  item or payment unknown                                       → InvalidJournal
  amount <= 0                                                   → InvalidJournal
  sourceDate missing while dated                                → InvalidJournal
  account or currency mismatch between item and payment         → InvalidJournal
  match.sourceDate < payment.sourceDate (both dated)            → InvalidJournal
totals:
  matched > payment amount, or matched > |item original|        → InvalidJournal
control totals: paymentControls and matchControls both reconcile → InvalidJournal
```

### 5.2 Cases

**HI-H1 — clean admission.** 2 items, 2 payments, 2 matches, controls that sum exactly.
```
THEN  200, financialEffect = "none", admittedBy = the caller's actor id,
      digest recomputes from the returned body
      DB: item admission row inserted; financial tables UNTOUCHED
          (this workflow must have zero ledger effect — assert that explicitly)
```

**HI-R1 → item-state ladder, five cases.** `unpaid` with original≠outstanding; `partly_paid` with
outstanding ≥ original; `partly_paid` with original 0; a signed mismatch; over-payment. Each →
`InvalidJournal`, DB unchanged. Neighbour: `unknown` state with *any* consistent numbers must be
accepted — that is what `unknown` means, and losing it would be an over-tightening regression.

**HI-R2 → the chronology switch.** Same payment with no `sourceDate`, run twice:
```
chronology = dated_source        → InvalidJournal
chronology = undated             → 200
```
Both directions, because the guard is `!validDate(date, dated)` and the flag is easy to invert.

**HI-R3 → the date-ordering rule.** Dated chronology, match dated *before* its payment → refused.
Equal dates → accepted (comparison is strict `<`). Both sides.

**HI-R4 → over-match.** Two payments of 600 against a single payment of 1000 is fine; a single
match of 1001 against a payment of 1000 → `InvalidJournal`. And a match totalling more than the
item's original → `InvalidJournal`. These are conservation properties; assert them as arithmetic,
not as codes.

**HI-R5 → control totals.** Deliberately break `paymentControls` by 1 minor unit → `InvalidJournal`.
Neighbour: exact → 200. And break `matchControls` independently, to prove both are checked.

**HI-X1 — concurrent admission of the same plan.** Exactly one lands; the other
`IdempotencyConflict`; exactly one admission row.

**HI-X2 — replay** returns the original admission, no second row.

---

## 6. Asset basis capture — `subledger/asset-basis.ts`

Shared by impairment and disposal, so most cases run twice with a profile switch.

### 6.1 Guard ladder

```
capture:
  book profile != synthetic-core-v1 or authority != native   → UnsupportedProfile
  schedule revision absent                                    → NotFound
  basis absent OR terms.kind != asset                         → UnsupportedProfile
  a disposal already exists                                   → AlreadyPosted
  schedule.digest != expectedDigest OR basis.digest != expectedBasisDigest
    OR basis does not match revision
    OR a reversal exists for the basis voucher                → StaleDependency
  postingDate < basis.effectiveOn                             → InvalidJournal
  occurrence state count != schedule occurrence count         → UnsupportedProfile
scanConsumed (per occurrence):
  state not in {unprepared, prepared, posted, reversed}       → UnsupportedProfile
  a correction exists for its voucher                         → UnsupportedProfile
  posted/reversed AND impairment profile AND already in suffix → UnsupportedProfile
  posted/reversed AND postingDate > input.postingDate         → UnsupportedProfile
  reversed AND reversal voucher absent, wrong purpose,
    or dated after input.postingDate                          → UnsupportedProfile
  unprepared/prepared in the consumed prefix AND disposal
    profile AND postingDate < input.postingDate               → UnsupportedProfile
  an impairment is dated after input.postingDate              → StaleDependency
  source or review evidence absent                            → MissingEvidence
  any referenced account inactive or reserved                 → InvalidJournal
impairment only:
  not in suffix, or posting basis unsupported                 → StaleDependency
  impaired <= 0, or >= carrying, or future <= 0,
    or futureMinor mismatch, or installments don't sum        → InvalidJournal
  loss account == contra account, or either already on the
    schedule, or an impairment used a different contra        → InvalidJournal
disposal only:
  carrying < 0, or gross != opening + cost, or retained lines
    disagree, or a line's polarity is wrong, or a retained
    line is missing                                           → UnsupportedProfile
  loss account is a carrying account or an impairment's contra → InvalidJournal
  more than one distinct contra account across impairments     → UnsupportedProfile
```

### 6.2 Cases

**AB-H1 — impairment on a clean asset, nothing posted yet.**
```
GIVEN  asset cost 100000, opening accumulated 0, 12 monthly occurrences from 2026-04,
       basis effectiveOn 2026-01-01, carrying 100000
WHEN  prepareAssetImpairment { postingDate 2026-07-15, impairmentMinor 5000,
                              futureMinor 95000, residualMinor 0,
                              installments summing to 95000, loss + contra accounts,
                              two fresh evidence ids }
THEN  200, carryingBasis/currentCarryingMinor = "100000",
      postImpairmentCarryingMinor = "95000", futureMinor = "95000",
      recognizedMinor = "0", reversedMinor = "0", priorImpairmentMinor = "0"
```
Assert every money field as a literal string, not as "a number".

**AB-H2 — disposal on the same asset** produces the disposal shape and must **not** accept the
impairment-only fields.

**AB-R1 → the reversal rule.** Pre-reverse one posted occurrence, then impair.
```
THEN  200, reversedMinor = that occurrence's amount, recognizedMinor = the posted one's,
      lastConsumed = max(postingDate, reversalVoucher.postingDate)
```
Neighbour: make the reversal voucher's `postingPurpose` something other than `reversal` →
`UnsupportedProfile`. And attach a correction to the reversed voucher → `UnsupportedProfile`.
Both of these are three-line guards that a refactor can quietly drop.

**AB-R2 → the prefix/suffix rule.** Impair after occurrence 6, where 1–5 are posted:
```
AB-R2a  occurrences 1–5 posted, 6–12 unprepared  → 200, recognized = sum(1..5),
        prefixCount = 5
AB-R2b  occurrences 1–3 posted, 4 PREPARED, 5–12 unprepared, impairment profile
        → UnsupportedProfile      (the prefix/suffix boundary: a prepared occurrence
                                   inside the consumed prefix is not consumable)
AB-R2c  same shape, disposal profile            → 200
```
R2b vs R2c is the sharpest test in this workflow: the *same fixture* is accepted under disposal and
refused under impairment. If a refactor loses the `input.profile ===` qualification, both pass and
the case is worthless.

**AB-R3 → account conflicts.** loss account is a reserved account → `InvalidJournal`. loss account
equals the contra account → `InvalidJournal`. loss account is already the schedule's debit account
→ `InvalidJournal`. Two existing impairments with *different* contra accounts, then a third
request → `InvalidJournal`.

**AB-R4 → date ceiling.** `postingDate` before `basis.effectiveOn` → `InvalidJournal`. An existing
impairment dated after the new `postingDate` → `StaleDependency`. Both from both sides.

**AB-R5 → arithmetic guards, impairment.** `impairmentMinor == carrying` → `InvalidJournal`.
`impairmentMinor > carrying` → `InvalidJournal`. `futureMinor` off by 1 from the derived value →
`InvalidJournal`. Installments summing to `future ± 1` → `InvalidJournal`. Each needs a passing
neighbour at the exact value.

**AB-R6 → disposal polarity.** A basis line with a positive debit on the schedule's *credit*
account → `UnsupportedProfile`. A line whose retained counterpart is missing → `UnsupportedProfile`.
Disposal with `carrying < 0` → `UnsupportedProfile`.

**AB-R7 → missing evidence.** Omit the review evidence id → `MissingEvidence`. Omit the source
evidence id → `MissingEvidence`. (Two separate disjuncts.)

---

## 7. Cross-cutting proofs

These four are not per-workflow; they are properties of the whole suite and each is where our
current 16 tests are thinnest.

**XC-1 — A refusal must not burn a sequence number.** (T4's key negative, from
`definer-function-grants`: *"the refusal has to land before the two UPDATEs, not after one."*)
For every R-case above that could plausibly allocate a number first, additionally assert:
```
DB: max(sequence) for the affected series is unchanged
DB: no outbox row was inserted
DB: no approval was marked consumed
```

**XC-2 — Cross-tenant, both directions, per workflow.** For each of the five:
```
GIVEN  book A and book B, each with a valid document/schedule/invoice
WHEN  operator of book B targets a book-A id with a valid body
THEN  refusal indistinguishable from not-found; no row in A or B changed;
      no sequence moved; response body leaks no A identifier
```

**XC-3 — Exact money beyond double precision, once, globally.** Our 38-digit minor units are an
asset `accounted` does not have. One case, at the boundary:
```
WHEN  post an amount of 9007199254740993 minor units
THEN  debit/credit strings round-trip byte-identically through HTTP, the receipt,
      and an independent DB read as text (never as a float)
      DB: the numeric column read with text formatting returns the same digits
```
And the aggregate case from `verification-strategy.md:31`: the `10^38 − 1` line boundary, and
overflow *beyond* it being refused rather than truncated.

**XC-4 — Digest order-insensitivity, and key-set exactness.** Because my refactors moved objects
between literals, two properties must hold for every returned body:
```
ASSERT  recomputing digest(canonicalize(body)) == returned digest
ASSERT  canonicalize(body) is byte-identical when the object's keys are permuted
ASSERT  the body's key set equals the contract's key set for that schema
        (catches an optional key silently added or dropped — the exact risk in
         credit-basis CB-H3 and schedules SA-H1)
```

## 8. Coverage ledger

| Workflow | Happy | Rejection | Exclusivity | Direct regression witnesses |
| --- | ---: | ---: | ---: | --- |
| sales-orders | 3 | 9 | 3 | 2 (digest ladder G4c, cap off-by-one G5) |
| credit-basis | 5 | 16 | 2 | 2 (CB-H3 key omission, CB-R3 no-leak) |
| schedules | 2 | 5 | 2 | 3 (SA-H1 key omission, SA-R2 prefix/suffix, SA-R5 no-op) |
| historical-items | 1 | 5 | 2 | 1 (HI-R1 `unknown` must stay accepted) |
| asset-basis | 2 | 7 | 0 | 2 (AB-R2b profile-qualified boundary, AB-R1 reversal qualifiers) |
| cross-cutting | 4 | — | — | — |
| **total** | **17** | **42** | **9** | **12** |

59 cases against 5 workflows. For scale: the evidence artifacts recorded roughly that many
distinct observations per workflow by hand, once.

## 9. What I could not specify independently

Per `verification-strategy.md:27` expectations must not come from our own calculator. These need a
domain owner or an external source, and I have marked them rather than inventing them:

| Item | Why it needs an owner |
| --- | --- |
| Which BAS accounts a *specific* impairment/disposal loss and contra should map to | `accounted-bench`'s `results/gold-audit.json` records a real finding here: reverse charge was judged correct, but *"4531 är det mest träffsäkra BAS-kontot … medan 5420 kan försvaras"* — their `acceptable_accounts` list exists because of exactly this. Asserting one "right" account is a trap |
| Whether `reversedMinor` polarity mirrors between supplier and customer | `accounted`'s `match-batch-allocate` mirrors öresavrundning polarity per side, but that is their decision, not law |
| The SIE 4C record-type rules and which validation errors are fatal | `swedish-accounting-skills` documents SIE 4C (2025-08-06) with a severity table; we should take their classification, not invent one. Also unresolved: **do we implement `#KSUMMA` (CRC-32 control total)?** I have not verified this |
| K2 vs K3 for årsredovisning, and the ÅRL 1:3 § större företag thresholds | From `swedish-accounting-skills`; a company-fact decision, not a code decision |
| Whether a 200-document and 50-revision cap are the right *numbers* | I can prove the guards fire at the boundary. Whether the boundary is correct is `docs/open-decisions.md` territory |

## 10. Honest limits of this document

- **No case here has been run.** Every expected value is a derivation, not an observation. The
  first execution will likely find at least one wrong literal — that is the correct outcome of
  specifying before implementing, not a failure of the specification.
- **The guard ladders are extracted from source as of `5ac3433`.** If the other agent is still
  editing these files, re-derive before writing cases. My own refactor is the thing most likely to
  have shifted an order, which is why XC-4 and the ordering-specific cases (G4c, R2b) exist.
- **No concurrency case specifies a barrier implementation.** `verification-strategy.md:35`
  requires observed locks or test-owned barriers with bounded timeouts; how we observe a lock
  against our Worker (rather than a bare `pg` client) is undecided. Until it is, the six X-cases
  are specified but not implementable.
- **Coverage is per-workflow, not per-scenario.** E-05, E-07, E-10 and E-21 have no cases here at
  all; they are in the gap table in `test-suite-design.md` §7 and remain open.
