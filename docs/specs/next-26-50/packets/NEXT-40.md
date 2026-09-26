# NEXT-40: Foreign-currency cash holdings and transfers

**Priority:** P1. **Owner lane:** TREASURY. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Bank/processor cash account owner with existing FX pure arithmetic and commerce obligation settlement.

**New scope, not repeated work:** First-wave FX owns receivables/payables. Add native-currency CASH balances and their book carrying values, not a duplicate invoice FX register.

**Dependencies:** NEXT-17, NEXT-18. **Integrate after:** WIP-FX02-P1, APP-SLICE-READY(banking).

**Evidence:** R09, R10, R11, P17, P18 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Cash representation

```text
ForeignCashAccount {
  sourceAccountId, book, nativeCurrency, nativeScale, bookCurrency,
  cashControlAccount, reviewedOpeningNative, reviewedOpeningCarrying, valuationPolicy
}
CashHoldingEffect immutable {
  sourceIdentity, nativeDelta, carryingDelta,
  kind: deposit | withdrawal | internal_transfer | exchange | valuation | correction,
  actualNativeDate, rateOrSettlementWitness, journalRefs
}
CashHoldingState = fold(reviewed opening + effective effects)
```

The initial profile permits nonnegative balances only. An overdraft changes liability and valuation semantics and requires another qualified profile. A SEK-denominated bank account receiving a foreign invoice payment is not a foreign-cash account merely because its source invoice used EUR.

## Capture and release

```text
captureCashBasis(account, cutoff):
  retrieve complete native and book movements at accounting/recorded cutoff
  Q = remaining native units; B = book carrying value
  require Q>=0 and B>=0
  if Q==0: require B==0
  return {Q,B,capacityVersion,valuationBoundary,sourceCoverage}

planCashWithdrawal(basis, q):
  require 0<q<=Q and policy permits the selected weighted carrying release
  use the shared exact paired-release pure calculation with this CASH basis
  b = B when q==Q, otherwise selected exact proportional release
  return {nativeConsumed:q, carryingReleased:b, witness}
```

The pure arithmetic can be reused from the FX owner. Cash mutation remains owned here; do not call a commerce-obligation mutation with a cash account ID or copy an invoice's remaining balance. Repeated reads of each selected account are batched.

## Settlement using foreign cash

For an already recognized same-native-currency payable, capture both independent capacities. Let `bP` be the payable carrying release and `bC` the cash holding release.

```text
compilePayableFromForeignCash(q):
  payableRelease = existing FxDomain release(payableBasis,q)
  cashRelease = planCashWithdrawal(cashBasis,q)
  debit payable control bP
  credit foreign-cash control bC
  gain = bP-bC
  credit gain if positive; debit loss if negative
  apply both native/carrying consumptions in ONE tx with same journal references
```

An incoming receivable settlement similarly increases cash at the qualified receipt-date book value `K`, releases AR carrying `bR` and recognizes gain `K-bR`. Subsequent cash valuation is a different holding effect. A payment already posted to a qualified foreign-cash clearing account is adopted without another cash movement.

## Transfers, exchanges and valuation

Same-currency transfer between two owned foreign accounts consumes native units/carrying from the sender and adds exactly the same pair to the receiver, absent separately evidenced fees. There is no economic gain from moving identical owned currency between accounts under that profile.

```text
exchangeForeignForBookCash(source,q,actualBookReceipt K,fee F):
  b = released foreign carrying
  debit book-currency cash K-F
  debit qualified fee cost F
  credit foreign-cash control b
  credit realized gain K-b or debit corresponding loss
```

Foreign-to-foreign exchange requires both native quantities and a qualified transaction-date book consideration. It cannot be inferred by independently rounded current quotes. Initial implementation may refuse that branch while delivering foreign-to-book exchange correctly.

For reporting-date valuation, compute target carrying from native units and the qualified reporting rate, then post only target minus current carrying. Native units remain unchanged. No automatic next-period reversal. Late valuation after a later cash withdrawal is a consumed-history case for NEXT-41, not a blind rewrite.

## Transactions, controls and vectors

Every journal plus sender/receiver/obligation effect commits on one supplied tx. Source cash identity is once-only across bank import, processor intake and native cash operations. Reconciliation compares native statement balance to native holding and book-currency GL to carrying independently. A zero SEK difference cannot explain missing native units.

```text
cash Q10000 EUR-minor, B110000 SEK-minor; withdraw q4000 -> b44000
payable same q releases45000 -> AP+45000, cash-44000, gain-1000
remaining cash Q6000/B66000; reporting target69000 -> cash+3000/gain-3000
same-currency internal transfer q1000,b11500 -> sender/receiver net book effect0
withdraw all -> consume all remaining carrying, no residual öre
```

UI displays native balance, book carrying, selected valuation and independent reconciliation. Summing currencies into one native total is prohibited; consolidated book values identify their valuation cutoff.
