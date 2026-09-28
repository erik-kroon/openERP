# NEXT-84: Book-to-tax depreciation cohorts and excess-depreciation bridge

**Priority when applicable:** P2. **Lane:** TAX.

**New work:** Add a tax-value and deduction calculation linked to book assets. Ordinary book depreciation and income-tax calculation remain separate owners.

**Use existing owners:** Asset register, qualified tax release, corporate-tax bridge and appropriation/reserve journal owners.

**Required earlier contracts:** NEXT-02, NEXT-13.

**Conditional gates:** NEXT-22: the annual tax bridge consumes the selected deduction; NEXT-81: new commissioned assets enter the eligible tax pool.

**Evidence basis:** R03, P22. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Separate bases, not parallel ledger books

```text
TaxAssetCohort {taxPool, acquisitionTaxYear, eligibleCost,
  disposalAdjustment, sourceBookAssetRefs, qualificationWitness}
TaxDepreciationCalculation {year, openingTaxValue, currentEligibleMovements,
  methodCandidates, selectedDeduction, closingTaxValue,
  bookCarryingBasis, requiredBookLinkage, priorEffectiveAppropriation, digest}
```

Start with a qualified ordinary machinery/equipment pool. Land, goodwill, special property, immediate deductions and mixed unsupported tax methods remain explicit cases. Imported tax opening values need prior-return evidence; do not derive them from book carrying alone.

## Exact calculation graph

```text
B = openingTaxValue + eligibleAdditions - qualifiedDisposalBasisAdjustment
require B>=0 or route to the separately supported recapture/disposal-tax profile
candidateDecliningClosing = roundRatio(B*(denominator-rate),denominator,rule)
candidateCohortClosing = sum(eligible cohort costs * qualified remaining factor by tax year)
validate each candidate's applicability and required accounting linkage
maximumDeduction = B - lowest permitted candidate closing
require 0 <= selectedDeduction <= maximumDeduction
closingTaxValue = B-selectedDeduction
```

The disposal adjustment and year factors come from the actual qualified method; neither necessarily equals book carrying or cash proceeds. For rules with book linkage, a tax choice cannot be finalized without the associated permitted book depreciation/appropriation. Selecting an unavailable method because it gives lower tax is refused. The operator chooses a permitted deduction rather than the app always maximizing it.

## Bridge and financial effect

For the specifically qualified excess-depreciation reserve profile:

```text
targetReserve = bookCarryingAfterOrdinaryDepreciation - closingTaxValue
require targetReserve>=0 and legal/book linkage satisfied
reserveDelta = targetReserve-priorEffectiveReserve
addSigned appropriation expense +reserveDelta
addSigned untaxed reserve -reserveDelta
```

Do not apply this formula to every framework or temporary difference. A negative/unsupported relationship requires its own treatment rather than a negative reserve default. Ordinary asset depreciation remains unchanged. Tax adjustments consumed by NEXT-22 distinguish book ordinary depreciation, appropriation and allowed deduction so the same deduction is not counted twice.

## Persistence and annual rollforward

Preparation captures actual asset events, tax cohorts, prior filings and book/tax computation versions. Execution of an approved appropriation posts only its delta and retains the chosen tax closing movement in the same tx. A draft does not consume tax capacity. Final year selection is linked to the actual tax/close record, never merely the last calculated preview.

Subsequent disposal or corrected acquisition creates impact on the cohort and affected tax years. Preserve submitted returns and book journals; generate reviewed target deltas or amendment work. Do not rebuild earlier years from today's asset labels.

## Examples and UI

Synthetic rates only: B1000000, permitted closing alternatives700000 and760000 yields maximum deduction300000. Selected deduction250000 gives tax closing750000. If qualified book carrying is800000, target reserve50000; prior reserve30000 gives a20000 appropriation, not another50000.

The view shows every cohort, candidate method, chosen deduction, remaining tax value and exact form/GL bridge. Delivery includes the tax-bridge consumer and independent controls. A second writable general ledger labelled tax is out of scope.
