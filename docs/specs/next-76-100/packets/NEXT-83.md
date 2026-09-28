# NEXT-83: Operating-rental contracts, refundable deposits and index changes

**Priority when applicable:** P2. **Lane:** PURCHASES.

**New work:** Add contract-owned operating-rental commitments and deposit recovery. This is not a finance-lease/right-of-use asset or another recurring expense scheduler.

**Use existing owners:** Existing purchase, prepayment/accrual, supplier advance, schedule and Cash contribution owners.

**Required earlier contracts:** NEXT-31, NEXT-57, NEXT-59.

**Evidence basis:** R03, P31, P57. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Supported profile

Start with one reviewed rental/operating-lease accounting profile and currency. Financial leases, sale-and-leaseback and uncertain classification refuse before financial admission. Contract dates, base rent, incentives, service charges, refundable deposits and cancellation terms are independent components.

```text
RentalRevision {agreementId, serviceInterval, periodicAmount,
  indexFormula, indexObservationRefs, noticeTerms, taxProfile, depositTerms}
RentOccurrence {agreementId, stableCycle, expectedCost, actualInvoiceRefs,
  accruedCostRefs, plannedPaymentIdentity}
RefundableDeposit {originalPaymentIdentity, principal, appliedToCosts, returned, remaining}
```

A deposit with an unconditional refund right is not rent expense. Where it is actually advance rent or its treatment is uncertain, NEXT-57/31 or a review blocker applies. A supplier calling a fee a deposit does not determine accounting.

## Contract changes and invoice replacement

```text
calculateIndexedRent(revision, observations):
  require specified base/index dates, series, caps/floors and rounding
  rateFactor = exact allowed formula over retained index values
  newAmount = roundRatio(baseRent*factorNumerator,factorDenominator,policy)
  freeze change-effective cycle and contractual notice evidence
```

The formula is a reviewed contract, not a guessed CPI lookup. An index observation change does not edit old invoices or occurrences. Amendments replace only eligible future commitments.

Committed expected rent is a forecast obligation, not automatically a payable. As service is consumed, the selected accrual/deferral owner recognizes expense with the contract evidence. An actual invoice replaces its specific forecast/accrual occurrence, avoiding duplicate Cash outflow and expense. Recurring preparation does not grant unattended posting approval.

## Deposit and termination

```text
payRefundableDeposit(D): debit deposit receivable D; credit cash D
receiveRefund(R): debit cash R; credit deposit receivable R
applyDepositToValidRent(A): debit supplier payable A; credit deposit receivable A
```

The last branch requires an already recognized supported rent obligation and evidence of actual application. If rent was not recognized, the purchase/accrual recognition and deposit application must compose in one approved aggregate. There is no second bank payment. Any forfeiture is a separate reviewed cost/loss with its own tax assessment, not silently treated as returned cash.

Termination ends unperformed commitments but does not reverse valid past expense or waive outstanding debt. Final fees, incentives needing repayment and restored premises costs require explicit reviewed components. Any unresolved obligation remains visible after the agreement is inactive.

## Transaction and output

Each deposit/expense/application operation uses the existing tx-passing owner and records exact source rights. Contract amendment is nonfinancial unless accompanied by explicitly approved accounting effects. Controls reconcile deposit principal and accrued/prepaid rent separately. Cash includes remaining contractual expectations replaced by actual invoices, not both.

```text
deposit30000; valid payable20000; apply15000 -> deposit15000, AP5000, cash delta0
rent10000 indexed by103/100 ->10300 for new cycles only
termination cancels3 future10000 expectations -> forecast-30000, GL delta0
refund12000 after3000 evidenced forfeiture -> deposit clears through separate events
```

UI must expose classification, service dates, index evidence, actual invoices and remaining refundable principal. No blanket K2/K3 lease qualification is claimed.
