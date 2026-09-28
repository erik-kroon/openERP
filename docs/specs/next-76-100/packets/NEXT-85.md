# NEXT-85: Periodiseringsfond cohorts, reversals and annual tax linkage

**Priority when applicable:** P2. **Lane:** TAX.

**New work:** Add optional tax-allocation reserve choices and their cohort history. Current-tax calculation alone does not own reserve deadlines or reversals.

**Use existing owners:** Existing tax bridge, closing, qualified rule releases, deadline and appropriation posting owners.

**Required earlier contracts:** NEXT-22, NEXT-49.

**Evidence basis:** X01, R03, P22. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Qualified cohort model

```text
ReserveCohort {entity, originalTaxYear, originalDeduction,
  bookReserve, taxReleaseBasis, remainingBook, remainingTax,
  mandatoryReleaseYear, vintageRules, sourceReturnRefs}
ReserveDecision {year, orderedReleases, newAllocation,
  preAllocationTaxBasis, eligibleMaximum, imputedIncomeBasis,
  targetEffects, evidence, reviewer}
```

Official guidance makes each year's reserve its own cohort and requires dated release rules [X01]. Tax-year age is not a fixed count of elapsed days. Preserve vintage-specific tax treatment and any mandatory early-release reason. Do not infer an opening reserve of zero merely because the app lacks imported cohort rows.

## Acyclic tax computation

```text
prepareReserveDecision(preReserveBridge, knownCohorts, chosenAllocation):
  determine mandatory and optional releases using qualified order/vintage rules
  bookRelease = sum selected book principal
  taxableRelease = sum each cohort's qualified tax-equivalent release
  imputedIncome = rule's exact computation on its specified opening reserve population
  basis = preReserveTaxResult + taxableRelease + imputedIncome
          + other explicitly ordered eligible adjustments
  maximum = rule's rounded permitted fraction of positive qualified allocation basis
  require 0<=chosenAllocation<=maximum
  return revised taxable basis = basis-chosenAllocation
```

The rule release defines the interaction with loss deductions and other restrictions. Do not use a fixed shortcut when the company's case falls outside that order. Imputed income is a tax-bridge contribution, not automatically accounting revenue. The pre-reserve input must exclude this decision's own book appropriation to avoid self-reference.

## Journals and lifecycle

```text
release prior reserve B: debit reserve B; credit appropriation income B
allocate new reserve A: debit appropriation expense A; credit current-year reserve A
```

Taxable reversal may differ from book B under a vintage rule; retain that difference in the tax bridge, not by changing the reserve's original ledger principal. Preparation is a selectable scenario. Execution consumes the selected old cohort capacities, creates the new cohort and posts its journal effects atomically with exact approval and receipt. Re-running the same year target cannot create another reserve merely under a new key.

A revised tax decision posts a target-minus-effective delta with original cohort identity and relevant correction dates. It never silently moves all reserves into one current-year bucket. Authority filing and assessment remain NEXT-74, not effects of the reserve journal.

## Controls and proof

Book cohort total must equal the qualified reserve GL accounts. Every annual tax bridge lists book changes, taxable changes and nonbook imputed income once. Deadline generation references each real cohort and its applicable tax-year sequence. Complete close refuses unknown old reserve history where material.

```text
synthetic allocation basis1000000 with permitted fraction1/4 -> ceiling250000
operator selects200000 -> current-year reserve200000, not default250000
old book reserve100000 with qualified tax factor104/100 -> book release100000,
    taxable release104000, separate tax adjustment4000
same decision replay -> same cohort effects; new key same target -> no duplicate reserve
```

Synthetic rates/factors are examples, not an activated Swedish rule. This packet does not advise a company to maximize reserves or choose a tax strategy; it makes a reviewed permitted decision traceable and executable.
