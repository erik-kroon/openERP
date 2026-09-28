# NEXT-40 foreign-cash leaf repair

Baseline: `61c92c5`, with `foreign-cash.ts` unchanged from the reviewed
`cbf4db9` blob `328a460d22c45aa96acebfd0ef93c66f23869fff`. Scope is this
evidence file, `next40-probe.ts` and `packages/domain/src/foreign-cash.ts`.
Repaired leaf blob: `f427526f80de62ce6fd06c509be84d4de27df948`.

**No application consumer exists.** `grep -rn "foreign-cash" apps packages`
returns only the `packages/domain/package.json` export map and one passing
comment in `fx-chain-repair.ts`. This is domain verification against the
public schema and function surface. It is **not** a provider, HTTP/MCP,
database, posting or UI journey, and it is **not** statutory compliance
evidence for any reporting period.

## Failure contract recorded before source changes

Committed as `48b47ea` before any edit to `foreign-cash.ts`.

1. A cash account denominated in the book currency, a basis that does not
   fold from the account's reviewed opening, an empty native balance with
   leftover carrying and a negative holding each refuse, and each refusal
   names its own condition instead of borrowing a balance code.
2. The captured remaining holding and the withdrawal plan carry the capacity
   version they were computed against, so a later plan can be bound to it.
3. A withdrawal releases carrying through the shared exact paired release, and
   a rounding refusal is not reported as an over-withdrawal. A corrupt basis
   and a release past the remaining book carrying each refuse.
4. Every monetary input is an exact bounded minor-unit integer string. A
   malformed, oversized, zero or negative settlement, receipt, fee or release
   refuses; none of them reverses into the opposite entry and none of them
   throws.
5. Every emitted line satisfies the journal line schema, carries exactly one
   positive side, and the group balances. A 39-digit amount and a
   non-conforming account reference never produce a journal.
6. A same-currency transfer without carrying has no zero-sided line.
7. Foreign-to-book exchange is supported; a foreign-to-foreign exchange
   refuses with `UnsupportedExchange` rather than posting a book-currency
   result to a second foreign account.
8. Valuation needs a qualified positive reporting rate and a reviewed pair of
   currency scales. Target carrying and the signed difference stay inside the
   money codec, a fractional book minor refuses, a negative delta is preserved
   as a signed diagnostic, and a negative native balance is refused.
9. Every observed failure code validates against the declared failure schema.

## Repeatable public-schema probe

Run from the repository root, before and after the repair. It uses only the
exported schemas and functions, records every case as one JSON line, and
prints a final `{"passed":N,"failed":M}`. New reviewed inputs (the two scales
and the target-currency flag) are supplied from the outset; the pre-repair
signatures ignore them. No test file is created.

```bash
EXPECT_REPAIRED=1 bun next40-probe.ts
```

The probe records a throw as a failed expectation, so a pre-repair crash
cannot abort the run. It is the whole artifact; there is no separate test
suite.

## Results

| Run | Cases | Passed | Failed | Exit |
| --- | --- | --- | --- | --- |
| Pre-repair, `foreign-cash.ts` at blob `328a460` | 50 | 23 | 27 | 1 |
| Post-repair, `foreign-cash.ts` at blob `f427526` | 50 | 50 | 0 | 0 |

The pre-repair run is a diagnosis, not a passing verification claim. It was
produced by restoring `git show 61c92c5:packages/domain/src/foreign-cash.ts`
over the repaired file and running the identical final probe.

## Vectors

Amounts are exact minor units. `D` and `C` are the paired debit and credit
fields of a journal line, not signed values.

| Vector | Before repair | After repair |
| --- | --- | --- |
| EUR account denominated in the SEK book | `NegativeHolding` | `NotForeignCashAccount` |
| Basis original native 10001 against a reviewed opening of 10000 | Succeeds with remaining 10001 | `OpeningMismatch` |
| Basis original carrying 109999 against 110000 | Succeeds with remaining 109999 | `OpeningMismatch` |
| Capture after consuming 4000 of 10000 native and 44000 of 110000 carrying | `6000` / `66000`, capacity version dropped | `6000` / `66000` with `capacityVersion: "cv_1"` |
| Empty units with 60000 carrying left (consumed 10000, released 50000) | `ResidualCarryingWithoutUnits` | Unchanged |
| Consumed 12000 against 10000 original | `NegativeHolding` | Unchanged |
| Account and basis schema bounds, 39-digit opening | Rejects 39 digits | Unchanged |
| Withdraw 4000 of 10000 against 110000, `exact` | `4000` / `44000` | Unchanged arithmetic, plan echoes `cv_1` |
| Withdraw the last 6000 after a 44000 release | `6000` / `66000`, no residual | Unchanged arithmetic, no residual öre |
| Withdraw 6001 against 6000 remaining | `OverWithdrawal` | Unchanged |
| Withdraw 0 or -4000 | `NonPositiveAmount` | Unchanged |
| Basis `3` native / `100` carrying, withdraw 1, `exact` | `OverWithdrawal` with a rounding message | `UnsupportedRounding` |
| Basis consumed 20000 against a 10000 original | `OverWithdrawal` | `NegativeHolding` |
| Basis consumed 3000, released 105000, withdraw 4000 | Succeeds releasing 44000 against 5000 remaining | `OverWithdrawal` |
| Withdraw a 38-digit maximum from a 38-digit maximum | `999…9` released | Unchanged |
| Withdraw `1000.00` | Throws `Failed to parse String to BigInt` | `AmountOutOfRange` |
| Withdraw a 39-digit amount | `OverWithdrawal` | `AmountOutOfRange` |
| Settle payable 45000 against cash 44000 | Payable D45000, cash C44000, gain C1000 | Unchanged |
| Settle payable 44000 against cash 45000 | Payable D44000, cash C45000, loss D1000 | Unchanged |
| Settle payable 44000 against cash 44000 | Two lines, no result line | Unchanged |
| Settle payable -5000 against cash 1000 | Credits payable 5000, credits cash 1000, debits loss 6000 | `NonPositiveAmount` |
| Settle payable `1`×39 | Debit of 39 digits, outside the codec | `AmountOutOfRange` |
| Settle payable `1000,00` | Throws | `AmountOutOfRange` |
| Payable account `ar` or 200 characters | Emits a line that fails the journal schema | `UnbalancedJournal` |
| Receipt 105000 releasing receivable 100000 | Cash D105000, receivable C100000, gain C5000 | Unchanged |
| Receipt book value -1000 | Credits cash 1000, debits receivable 1000, debits loss 2000 | `NonPositiveAmount` |
| Transfer 1000 native / 11500 carrying | Sender C11500, receiver D11500 | Unchanged |
| Transfer 1000 native / 0 carrying | Two lines with both sides `0` | No lines |
| Transfer 0 native, or -11500 carrying | `NonPositiveAmount` | Unchanged |
| Transfer 39-digit carrying | 39-digit sides | `AmountOutOfRange` |
| Exchange releasing 44000, receipt 105000, fee 500 | Book cash D104500, fee D500, foreign C44000, gain C61000 | Unchanged |
| Exchange fee 105001 above the receipt | `NonPositiveAmount` | Unchanged |
| Exchange fee -500 | `NonPositiveAmount` | Unchanged |
| Exchange 44000/105000/500 into a second foreign account | Posts the same book-currency journal | `UnsupportedExchange` |
| Exchange with a 39-digit receipt | 39-digit sides | `AmountOutOfRange` |
| Value 6000 units at `23/2`, scales 2/2, carrying 66000 | `69000` / `3000` | Unchanged |
| Value 6000 JPY units at `115/10`, scales 0/2, carrying 66000 | `69000` / `3000`, a factor of 100 low | `6900000` / `6834000` |
| Value 6000 units at `23/2` against carrying 80000 | `69000` / `-11000` | Unchanged, signed |
| Valuation result schema | No declared schema; `Schema.is(undefined)` throws | `CashValuation` validates |
| Valuation with `withdrawnAfterCutoff: true` | `ConsumedHistoryValuation` | Unchanged |
| Valuation with rate denominator `0` | `ConsumedHistoryValuation` | `UnsupportedRate` |
| Valuation with rate numerator `-11` | Target `-11000`, delta `-121000` | `UnsupportedRate` |
| Valuation 3 units at `10/4` | `ConsumedHistoryValuation` | `UnsupportedRate` |
| Valuation 38-digit units at a 38-digit rate over 1 | 76-digit target and delta | `AmountOutOfRange` |
| Valuation of -6000 native units | Target `-69000`, delta `-135000` | `NegativeHolding` |
| Valuation with units `6e3` | Throws | `AmountOutOfRange` |
| Every observed failure against the failure schema | Passes | Passes |

## Defects found

1. `foreign-cash.ts:84` (pre) returned `NegativeHolding` for an account whose
   native currency equals the book currency, a qualification failure reported
   as a negative balance.
2. `foreign-cash.ts:80` never compared the basis against the account's
   `reviewedOpeningNativeMinor` / `reviewedOpeningCarryingMinor`, so a basis
   from another account state computed a remaining holding silently.
3. `foreign-cash.ts:65` declared `capacityVersion` and no code ever read it;
   `captureCashBasis` and `planCashWithdrawal` both dropped it, so a stale
   basis could not be detected from the result.
4. `foreign-cash.ts:144` remapped every `cumulativeRelease` failure to
   `OverWithdrawal`, so an exact-rounding residual was reported as an
   over-withdrawal.
5. `foreign-cash.ts:131` checked the requested withdrawal against the
   *original* holding rather than the captured remaining one, and never
   checked the released carrying against the remaining carrying.
6. `foreign-cash.ts:125` (and `:91`, `:212`, `:246`, `:279`, `:316`, `:368`)
   fed every monetary parameter straight to `BigInt`, so `"1000.00"` and
   `"6e3"` threw instead of refusing, and `"+5"`, `" 5"` and `"007"` were
   silently accepted.
7. `foreign-cash.ts:188` `balanced` never validated its own lines, so a
   38-digit input produced a 39-digit journal that violates the declared
   `ForeignCashJournalLines`.
8. `foreign-cash.ts:273` `transferForeignCash` bypassed `balanced` and hand-built
   its lines, emitting two lines with both sides `0` when carrying was zero.
9. `foreign-cash.ts:212` accepted a negative payable release and produced a
   balanced journal that credited the payable control; `foreign-cash.ts:246`
   did the same for a negative receipt book value.
10. `foreign-cash.ts:306` `exchangeToBookCash` had no way to refuse a
    foreign-to-foreign exchange, so `UnsupportedExchange` (declared at
    `foreign-cash.ts:25`) could never be returned.
11. `foreign-cash.ts:368` reported a non-positive rate denominator, a negative
    rate numerator and a fractional result all as `ConsumedHistoryValuation`.
12. `foreign-cash.ts:374` valued native units with no scale conversion while
    the FX owner's `targetCarrying` (`fx-remeasurement.ts:165`) applies
    `10^bookScale / 10^nativeScale`, so a scale-asymmetric pair was valued a
    factor of 100 wrong and `ForeignCashAccount.nativeScale` was dead.
13. `foreign-cash.ts:360` returned two untyped `string` values with no schema,
    so a 76-digit target and a negative target both left the leaf unchecked.
14. `foreign-cash.ts:229` and its three siblings wrote
    `signedMinor: gain >= 0n ? -gain : -gain`, an identical pair of branches
    duplicated four times.
15. `UnbalancedJournal` was unreachable before the repair: `balanced` only
    summed amounts that were balanced by construction.

## Verified correct, not defects

- Sign conventions. The payable settlement debits the payable release, credits
  the cash release, and credits gain when `payableRelease - cashRelease` is
  positive. The receipt realizes `K - bR`, and the exchange realizes `K - b`
  on the gross receipt while the fee is a separate debit, exactly as the
  packet specifies.
- The paired release is the shared `cumulativeRelease` from `purchasing`, and a
  final consume releases the remainder with no residual öre.
- The initial profile's nonnegative-balance rule matches the packet, and no
  clamp hides a negative balance: negatives refuse.
- Every arithmetic path is exact `bigint`; no `number` touches a money value
  and no apportionment invents a rounding rule.
- Equal amounts do not collide, because nothing in the leaf keys a result by
  amount.

## Static gates

- First `bun run check:changed`: failed. Oxlint rejected two probe helpers and
  `tsc` rejected `Result.isFailure` narrowing (`Failure<A, E>` is not
  assignable to `Checked<B>`) and `CurrencyScale` used as a type. The
  narrowing now returns `Result.fail(...failure)` as the sibling leaf does, the
  scale parameters use `typeof CurrencyScale.Type`, `remainingHolding` became
  a total function, and the probe gained its blank lines. No rule was changed,
  disabled or reconfigured.
- `bun run check:changed`: passed formatting, lint and incremental TypeScript
  for `next40-probe.ts` (root project) and `packages/domain/src/foreign-cash.ts`
  (domain project).
- `bun run check:changed:full`: passed formatting, type-aware lint and the same
  incremental TypeScript checks.
- `git diff --check`: passed. No command timed out.

## Changed leaf contracts

No application consumers were found, so nothing is migrated. These are explicit
required-and-reviewed inputs, not compatibility defaults.

- `ForeignCashFailureCode` gains `NotForeignCashAccount`, `OpeningMismatch`,
  `AmountOutOfRange`, `UnsupportedRounding` and `UnsupportedRate`. Each names a
  condition the leaf previously misreported or silently accepted. All twelve
  codes are reachable; before the repair `UnsupportedExchange` and
  `UnbalancedJournal` were not.
- Every monetary parameter is validated as an exact `SignedMinorUnits` string
  bounded by the 38-digit `MinorUnits` posting magnitude. A malformed or
  oversized value is `AmountOutOfRange`; a well-formed negative or zero where a
  magnitude is required is `NonPositiveAmount`; a negative native balance is
  `NegativeHolding`.
- `captureCashBasis` refuses a basis whose originals disagree with the
  account's reviewed opening (`OpeningMismatch`) and returns the basis
  `capacityVersion` in `RemainingHolding`. `CashWithdrawalPlan` also carries
  `capacityVersion`. The capacity version field is hoisted into a named
  `CapacityVersion` schema.
- `planCashWithdrawal` checks the request against the remaining native units
  and the release against the remaining carrying, refuses a negative holding
  first, and reports a shared-calculation rounding refusal as
  `UnsupportedRounding`.
- `RemainingHolding` and `CashWithdrawalPlan` gained a required
  `capacityVersion`; the packet's `return {Q,B,capacityVersion,…}` is now
  honoured for the part this leaf owns.
- `exchangeToBookCash` takes a new required `targetIsBookCurrency: boolean`.
  A reviewed `false` refuses with `UnsupportedExchange`; nothing is inferred
  from an account identifier. The packet's `valuationBoundary` and
  `sourceCoverage` are not part of this leaf.
- `valueCashHolding` takes two new required `CurrencyScale` parameters after
  `withdrawnAfterCutoff` and returns the new `CashValuation` schema, whose
  `targetMinor` is `MinorUnits` and whose `deltaMinor` is `SignedMinorUnits`.
  The rate parts are the owner's `PositiveRatePart`, so zero, negative and
  out-of-codec rates refuse as `UnsupportedRate`. For a same-scale currency
  pair the arithmetic is bit-identical to before, so the packet's own vectors
  are unchanged; for a scale-asymmetric pair the conversion now matches the
  FX owner. The packet does not state the rate convention, so this is recorded
  as a packet/code disagreement resolved in favour of the owner contract.
- Every emitted journal goes through one chokepoint that requires each line to
  satisfy `ForeignCashJournalLine`, to carry exactly one positive side, and
  the group to balance. `transferForeignCash` no longer bypasses it, and a
  transfer without carrying emits no line. The duplicated gain/loss ternary is
  now a single `realized` helper.

## Not proven

- No provider, HTTP/MCP, database, transaction, posting or UI journey was run.
  There is no consumer to run one against.
- The leaf has no occurrence identity, no effect envelope, no replay guard and
  no once-only receipt. Two equal transfers of 1000/11500 produce byte-identical
  journals, so **the returned effect carries no discriminator and once-only
  source identity cannot be enforced or even keyed from this leaf's output**.
  Building an identity subsystem would be a redesign, not a repair; the packet's
  `CashHoldingEffect.sourceIdentity`, `kind`, `actualNativeDate`,
  `rateOrSettlementWitness` and `journalRefs` remain unimplemented.
- `ForeignCashJournalLine.sourceLineId` is always `null`; the leaf never
  populates it, so a line cannot be attributed to a native-unit occurrence.
- `transferForeignCash` does not prove the sender and receiver are distinct,
  same-book, owned accounts, and it does not check the transferred carrying
  against any sender basis. Ownership, same-book scope and the native-side
  state update are caller duties.
- A reviewed `capacityVersion` is not proof of completeness. Nothing here
  proves that a capture is complete, unique or current.
- The boolean `targetIsBookCurrency` is a caller assertion, not proof that the
  receiving account is book-currency cash.
- `balanced` enforces a bounded account reference and one positive side per
  line, but the net-balance branch is reached by no probe case: every emitter
  is balanced by construction, so that branch is a construction-time guard.
- No reconciliation exists. The packet's requirement that a zero SEK difference
  cannot explain missing native units, and its prohibition on summing
  currencies into one native total, are unimplemented and unverified.
- The packet's `ForeignCashAccount.cashControlAccount` and `valuationPolicy`
  fields are still absent; the control accounts are passed to the journal
  functions instead. This is recorded, not repaired.
- `nativeScale` is now load-bearing only in `valueCashHolding`. A caller that
  supplies a rate already expressed as a book-minor ratio over native minor
  units, rather than a currency quote, will now be scaled twice. That caller
  has no other correct interpretation to choose, but the hazard is real.
- The rounding modes `toward_zero`, `floor`, `half_up` and `half_even` are
  accepted for a withdrawal; only `exact` and the packet's own vectors were
  probed.
- Not statutory compliance, and not evidence for any reporting period.

Only this evidence file, the probe and the reviewed leaf were changed. No
dependency, shared export, application persistence, test file or external
operation was added. The leaf is ready for integrator review; packet
integration and any runtime journey remain open.
