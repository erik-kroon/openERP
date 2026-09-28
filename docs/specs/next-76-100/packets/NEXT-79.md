# NEXT-79: Earned but unbilled service revenue and later invoicing

**Priority when applicable:** P1. **Lane:** SALES.

**New work:** Add earned-unbilled recognition before invoice issue. NEXT-58 defers invoiced revenue and is the opposite timing direction.

**Use existing owners:** Existing contract, revenue schedules, GL, invoice and tax-fact owners.

**Required earlier contracts:** NEXT-13, NEXT-51, NEXT-58, NEXT-76.

**Evidence basis:** R02, R03, P58. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Recognition coverage

```text
PerformanceComponent {contractId, stableServiceCoverage, exactSupportedMeasure,
  earnedEvidence, collection/acceptanceConditions, valuationRelease}
EarnedRevenueTarget {componentId, asOf, earnedNetTarget, previouslyEffectiveNet,
  basisRefs, ruleVersion, accountingDate}
UnbilledEffect {componentId, recognizedNet, invoicedReleaseNet,
  correctionRefs, journalRefs, sourceCoverageIdentity}
```

Start with one reviewed service-recognition profile under the applicable framework. Do not equate hours worked, cost incurred or a forecast milestone with legally/accountingly earned revenue. An uncertain entitlement produces a review case rather than a manufactured contract asset. Construction percentage-of-completion and loss-making contracts need their own qualified profiles.

## Target calculation and posting

```text
prepareEarnedRevenue(component, qualifiedMeasure):
  target = exact contractual price * qualified earned fraction, rounded per release
  require target <= supported total contract consideration
  delta = target - totalEffectiveRevenueRecognizedForThisCoverage
  determine whether delta changes unbilled asset or an already invoiced/deferral component
  initial path permits only the currently unbilled portion
  debit unbilled contract asset delta
  credit service revenue delta
  no invoice, customer AR or tax fact unless a separate qualified tax trigger exists
```

SQL reads return exact prior effects; the domain computes the target/delta. A new target revision does not post the entire target again. Negative deltas may reduce existing unbilled carrying only to its available amount. Reductions of already invoiced amounts require the proper credit/deferral owner rather than a negative contract-asset shortcut.

## Issue without re-recognizing revenue

```text
compileInvoiceWithPriorEarnings(invoiceLines, coverage):
  N = invoice net; V = independently qualified invoice tax
  E = exact earlier earned-unbilled carrying released for this invoice coverage
  require 0 <= E <= N and available unbilled capacity
  debit customer AR N+V
  credit unbilled asset E
  credit revenue or deferred-revenue owner for remaining N-E, per supported treatment
  credit output VAT V unless already represented by qualified earlier tax facts
```

Already recognized tax also has coverage and must be released/adopted exactly once; the initial profile can refuse earlier-tax cases instead of assuming every unbilled asset is tax-free. The combined invoice issue consumes unbilled coverage on the same tx as numbering, financial posting and tax/open-item effects.

## Controls and correction

Reconcile unbilled opening plus recognition deltas less invoiced releases to the GL. Keep recognized revenue and commercially billable amounts distinct. An invoice claim is not another cash event. Expired collection rights or disputed earned values go through a reviewed correction/impairment profile, not silent source deletion.

Views show supported earned amount, already invoiced amount, remaining asset, tax status and evidence. Closed-date refusal never changes the proposed posting date automatically. Historical reports keep their captured target revisions.

```text
earned60000 -> asset+60000/revenue-60000
invoice net80000 tax20000 -> AR+100000, asset-60000, revenue-20000, VAT-20000
lifetime revenue80000, not140000
same coverage target revised70000 before billing -> additional recognition10000
```

Delivery must include invoice consumption and fixed-cutoff controls. A standalone accrued-income journal generator is not completion.
