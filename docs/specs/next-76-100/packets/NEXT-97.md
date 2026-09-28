# NEXT-97: Exact covering-set reconciliation with explicit ambiguity

**Priority when applicable:** P1. **Lane:** BANKING.

**New work:** Add bounded one-to-many discovery and cross-proposal conflict analysis. Existing exact matches and reviewed allocation execution remain their owners.

**Use existing owners:** Current banking candidate reads, exact-money comparability and bank-allocation prepare/approve/execute operations.

**Required earlier contracts:** NEXT-09, NEXT-10.

**Conditional gates:** NEXT-70: the selected source is a structured bank file; NEXT-40: native foreign-cash comparability is supported.

**Evidence basis:** R05, P09, P10. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Candidate state

```text
CandidateBasis {observationId, account, currency, selectedDateScope,
  observationRemaining, ledgerCandidates:[{lineId, remaining, date, sourceRefs}],
  populationCount, poolComplete, versions, sourceEligibility}
CoverResult = UniqueWithinDeclaredPool | Ambiguous | NoMatchWithinDeclaredPool
            | IncompleteSearch | Unavailable
```

Compare signed, same-currency amounts only under the existing comparability contract. No stored qualified conversion means not comparable, not a raw numeric match. Candidate lookup failures stay unavailable. Opposite-sign decomposition, fees and generated adjustment vouchers are outside the first exact-sum profile.

## Bounded search

```text
findCovers(basis, maxSetSize, maxCandidates, maxVisited):
  qualify and deduplicate candidate identities; verify one consistent capacity per ID
  retain full population count and any excluded/truncated candidates
  search subset sizes k=1..maxSetSize using exact integer sums
  apply nonnegative remaining-sum bounds to prune, never tolerance plugs
  for each exact sum:
    retain IDs, total, maximum service/date gap and deterministic ranking components
  stop when declared computation budget is exhausted
  if exhausted or candidate pool incomplete: return IncompleteSearch with observed alternatives
  after completely exploring the first successful cardinality k, larger sets need not run
  select best date/other permitted rank within k, retaining all equal-ranked distinct covers
  one -> UniqueWithinDeclaredPool; many -> Ambiguous; none -> NoMatchWithinDeclaredPool
```

Stable ID ordering only makes output repeatable. It does not prove that one equal-ranked economic explanation is correct. A pool capped at40 candidates cannot claim uniqueness among every line in the book. Results name the exact scope searched.

## Several observations

Build a conflict graph over candidate covers sharing any observation or ledger capacity. Present incompatible alternatives together instead of independently labelling each a unique automatic match. A deterministic optimisation can rank whole-set proposals, but it must preserve ties and incomplete-search limits. User review selects the exact intended economic links.

```text
prepareSelectedCover(result, selectedIds):
  require original observation and selected candidate identities match the shown basis
  call existing allocation PREPARE with explicit legs outside any held caller tx
  owning allocation operation recaptures actual capacities and eligibility
  obtain human approval, then execute through that owner
```

This feature posts no fee/residual voucher and consumes no allocation capacity during discovery. For this initial full-residual cover profile, a candidate contributes its selected whole remaining capacity. Partial sub-leg search is a separate supported variant, not an undisclosed change to the search. Two competing selections resolve at the shared allocation owner's transaction. If one side changed, the selected proposal becomes stale rather than silently substituting another cover.

## Proof and operator experience

Show exact total, leftover zero, candidate provenance, search completeness and ambiguity. No confidence percentage is a calibrated probability unless independently evaluated. Requests can expand a bounded scope explicitly, never return an incomplete empty result as no match.

```text
target100; candidates70,30,60,40 -> two exact2-item covers, Ambiguous
max visited reached before alternate branch -> IncompleteSearch, not Unique
same ledger line suggested for two bank rows -> conflict shown, no double allocation
selected cover100 but one line already consumed20 -> owner refuses/reprepares
unsupported currency pair -> explicit exclusion, not 1:1 comparison
```

Delivery includes actual candidate-to-allocation review and two-successive-consumer recovery cases. It does not replace matching receipts or repair a supposed missing SQL rule.
