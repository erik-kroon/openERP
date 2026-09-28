# NEXT-120: Preliminary income-tax revisions and authoritative installment schedules

**Priority when applicable:** P1. **Owner lane:** TAX.

**New scope:** Annual current-tax calculation and final INK2 filing already have owners. Add a separately labelled forecast-based preliminary declaration, its revised authority decision and the payment-schedule impact.

**Existing owner to extend:** Existing corporate-tax calculator, immutable Cash forecast/scenario, tax-account events and external obligations.

**Earlier contracts:** NEXT-22, NEXT-49. **This-wave dependencies:** None.

**Conditional:** NEXT-74: linking final annual filing outcomes; NEXT-99: later scoring the retained estimate against actual tax outcomes.

**Basis:** X10, P22, P99 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Actual forecast versus actual obligation

```text
PreliminaryTaxEstimateRevision {
  fiscalYear, actualToDateBasis, remainingForecastScenario,
  corporateTaxProfile, forecastAdjustments, completeAssumptions,
  estimatedFullYearBases, existingAuthorityDecision, digest
}
PreliminaryDeclarationIntent {estimateRevision, officialFormProfile, applicantAuthority, attempt}
PreliminaryTaxDecision {
  originalAuthorityEvidence, fiscalYear, assessedScope,
  installmentSchedule, replacesDecisionRef?, effectiveDate
}
```

A forecast can estimate a proposed full-year tax basis. It is not a finalized tax computation or a permission to reduce payments unilaterally. The official preliminary-tax service separates submitted declarations from decisions on debited tax [X10]. Continue to represent the currently authoritative obligations until an effective replacement or other actual authority evidence changes them.

## Estimate without contaminating the books

```text
preparePreliminaryEstimate(actualBasis, selectedForecast):
  require same company/year and explicit split between actual and hypothetical periods
  require no overlap between actual recognized components and scenario projections
  re-use the qualified corporate-tax pure calculator with inputMode=forecast
  retain every assumed revenue, cost, tax adjustment and unsupported family
  compute fullYearTarget and compare with existing debited schedule
  output estimate/uncertainty, not a current-tax journal or filed-return fact
```

Known losses, reserve choices, pensions and other tax adjustments must have supported actual facts or labelled scenario inputs. A missing mandatory tax adjustment cannot become zero to make the estimate look precise. A historical Cash forecast's expected tax contributions are not independent source evidence for recalculating the same tax.

The planning view can show a hypothetical remaining-installment amount, but it must not label an equal split as the authority's future decision. The real installment dates, catch-up effects and effective scope are taken from the actual returned decision.

## Request and decision lifecycle

Create a fixed application/form payload or official-service handoff from the approved estimate. Use actual applicant/representative authority and retained external-attempt identity. The available public entry point is not proof a supported API exists; never invent one. Capture authentic receipt and later decision separately.

```text
admitNewDecision(observation):
  verify company/year, original evidence and exact replaced decision scope
  retain every assessed installment/date and any retroactive adjustment
  compare with already posted tax-account charges and actual payments
  append decision revision and intended current obligation schedule
  do not reverse old booked bank payments or alter final current-tax expense
```

When actual assessed tax-account events arrive, their owner posts/matches them using this decision as supporting evidence. A decision changing future debits is not automatically a new cash payment. Overpayments/refunds follow actual authority and bank events rather than a formula guessed from the annual estimate.

## Cash and reporting integration

Cash selects one authoritative schedule for each still-outstanding obligation and keeps the hypothetical estimate as a scenario. Existing tax-account funding, charges and already reserved payment instructions must be reconciled so the schedule does not subtract the same expected outflow twice. An old exported instruction cannot be cancelled merely by changing a forecast; its external outcome remains with the payment owner.

Final INK2/current tax later reconciles against actual provisional tax history. It does not become dependent on every preliminary estimate having been submitted. Old estimates remain useful for forecast-error evaluation through NEXT-99.

```text
estimated annual tax120000, later scenario90000 -> proposed reduction30000,
    actual payable schedule unchanged until evidence of replacement
received decision revises future installment10000 to6000 -> exact new schedule selected,
    prior bank payments unchanged
book current-tax expense90000 and prepaid charges80000 -> separate balances,
    no rule automatically books only10000 as tax expense
submission accepted but new decision unavailable -> status pending decision
```

Completion requires an estimate with honest assumptions, a supported official handoff and versioned actual decision/payable/Cash consumers. It does not certify tax advice or external acceptance through a screenshot of a local form.
