# NEXT-38: Cash-method recognition and unpaid year-end cutover

**Priority:** P0. **Owner lane:** TAX. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Commerce invoice/open-item and tax-fact owners, with a cash-method profile beside the existing accrual profile.

**New scope, not repeated work:** NEXT-03/04 start with accrual. Add paid recognition and once-only year-end unpaid recognition, not another invoice or VAT ledger.

**Dependencies:** NEXT-03, NEXT-04. **Integrate after:** APP-SLICE-READY(commerce/register).

**Conditional gates:** NEXT-23: the reviewed unpaid population is consumed by financial year-end.

**Evidence:** R09, R10, X03 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Keep commercial balance separate from recognition

Start with qualified domestic same-currency invoices and explicitly supported ordinary tax treatments. Do not infer cash-method eligibility from company size or switch the book by relabeling existing accrual effects. Method changes need a separately reviewed cutover.

```text
CashMethodInvoice {
  originalGross, originalLineComponents, commercialIssueOrAcceptance,
  paidAllocations, creditRelationships, profileWitness
}
RecognitionSlice immutable {
  invoiceId, sourceLineId, componentCoverage,
  trigger: actual_payment | unpaid_year_end,
  grossCoverage, netExpenseOrRevenue, taxComponents,
  journalRefs, taxPeriod, economicIdentity
}
RecognizedOpenPosition {
  recognitionSliceId, initialGross, laterSettlements, remainingGross
}
```

Per source line, disjoint recognized coverage prevents paid and year-end paths from recognizing the same portion. A receipt number or invoice issue is not itself the cash-method recognition trigger. Retain unrecognized commercial debt visibly.

## Partial payment compiler

```text
prepareCashMethodPayment(invoice, explicitLineAllocations, cashEvidence):
  require actual final cash event with supported timing and no duplicate source use
  for selected line in frozen original order:
    p = gross amount paid against this line
    s = min(p, existing recognized-unpaid coverage allocated by approved policy)
    r = p-s
    require r <= this line's unrecognized outstanding coverage
    if purchase:
        debit payable control s
        recognize remaining r as expense + deductible tax under original treatment
        credit bank p
    if sale:
        debit bank p
        credit receivable control s
        recognize remaining r as revenue + output tax
    publish tax facts ONLY for newly recognized r
    consume recognized position s and claim new recognized coverage r
```

Split source-line net/tax components by cumulative exact gross coverage using the qualified rounding rule; final consumption releases exact residuals. The operator-selected line allocations sum to the cash principal. Fees are separate sources/effects. Do not round each partial payment as an unrelated invoice.

All cash, recognition, tax facts, commercial settlement and source rights commit in one named application transaction. When a compatible cash posting already exists, adopt its clearing-side capacity and create no duplicate bank entry.

## Year-end population

```text
prepareCashMethodYearEnd(year, cutoff):
  capture complete eligible issued/received unpaid invoice population
  pin registration/method, fiscal interval, source coverage and membership epoch
  for every original line:
    u = commercial unpaid coverage not already recognized
    derive exact remaining cost/revenue and tax components for u
    purchase: debit cost/input VAT; credit payable u
    sale: debit receivable u; credit revenue/output VAT
    append recognition slices(trigger=unpaid_year_end)
  seal entire supported group and unresolved exclusions
```

Skatteverket describes unpaid invoices as recognized at year-end under cash bookkeeping; later payment must not repeat their VAT [X03]. The exact legal dates and special cases must be supplied by the qualified profile. The app must not call an incomplete selected page a complete year-end population.

```text
executeYearEndRecognition(plan): FinancialTx
  recheck membership and every outstanding/recognized capacity
  reject new relevant invoices/payments or changed treatment
  post aggregate and tax facts; create recognized open positions
  save complete membership receipt, including valid no-effect items
```

Payment in the next year then consumes those positions. It posts bank versus AP/AR only for the previously recognized amount. It does not create new revenue, expense or tax facts.

## Credits and correction boundary

An unpaid credit consumes explicitly linked source-line coverage. If that portion was unrecognized, revise the commercial residual with no reversal of nonexistent accounting. If it was recognized at year-end, create the exact recognized credit/tax correction under the applicable credit-date rule. Do not subtract both the original tax fact and another negative fact. Paid-principal credits route to the qualified customer/supplier refund extension; until cash-method reporting there is qualified, refuse that branch explicitly.

A backdated payment or newly discovered prior-year invoice invalidates the relevant year-end assessment. Preserve the old receipt and create the required owned amendment/closing impact, not silently undo year-end recognition.

## Controls and vectors

```text
original gross125000 = net100000 + VAT25000
first payment50000 -> net recognition40000, VAT10000
year-end unpaid75000 -> net60000, VAT15000, AP/AR75000
next-year payment75000 -> only AP/AR settlement, VAT delta0
payment and year-end compete for same coverage -> one wins; other stale/recomputes
invoice recorded but no payment and before year-end -> commercial debt, GL recognition0
```

Reports distinguish all commercial outstanding from the recognized GL-controlled portion. Unknown or unsupported invoices block complete year-end readiness, not source retention or independent supported work.
