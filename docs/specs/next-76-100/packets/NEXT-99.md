# NEXT-99: Cash forecast vintage scoring and error attribution

**Priority when applicable:** P1. **Lane:** CASH.

**New work:** Add retrospective evaluation of saved forecasts, not another forecasting engine. Cash scenarios and historical cash-flow statements remain their original owners.

**Use existing owners:** Existing immutable Cash forecasts, payment-occurrence identities, actual bank/control observations and report snapshots.

**Required earlier contracts:** NEXT-13, NEXT-45, NEXT-50.

**Evidence basis:** R06, P45. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Preserve what was actually known

```text
ForecastVintage {forecastId, createdAt, economicAsOf, recordedCutoff,
  accountPerimeter, currency, predictedOpening, events, assumptions, horizon}
ActualOutcomeBasis {cutoff, observedCoverage, matchedPaymentOccurrences,
  actualOpening, datedSignedCashEvents, correctionsKnownAtEvaluation}
ForecastScore {vintageId, actualBasisId, identityLinks,
  dailyErrorComponents, metrics, incompleteOutcomeCases, version}
```

The original forecast is never rerun using later facts and labelled historical accuracy. Restated actuals can be used in a separately labelled score revision. Missing bank coverage or an unelapsed horizon remains incomplete, not a zero outcome.

## Conserved decomposition

Define error as actual balance minus forecast balance. Align events through the existing payment/economic identity, not amount/date similarity alone. For one matched same-sign aggregate P forecast and A actual, let W=min(abs(P),abs(A)) and s=their sign.

```text
timingError(d) = s*W*(indicator(actualDate<=d)-indicator(predictedDate<=d))
amountError(d) = s*((abs(A)-W)*indicator(actualDate<=d)
                    -(abs(P)-W)*indicator(predictedDate<=d))
```

Their sum equals that event's actual-minus-predicted cash contribution. Opposite-sign/unmatched events are explicit classification or scope cases, not forced into the timing formula. Partial payments first partition by the owner's conserved allocations; an individual payment cannot be matched to two predicted events.

Add opening-balance differences, actually absent/present economic events, scope/perimeter changes and documented FX valuation differences as nonoverlapping components. Every unexplained residual remains a score diagnostic. Do not attribute a changed account perimeter to customer lateness.

## Metrics and query

```text
scoreVintage(vintage, actualBasis):
  require same supported cash semantics or an explicit reconciliation bridge
  compute daily actual/forecast curves over the fully observed intersection
  compute exact signed error and sum of decomposed effects per day
  require decomposition == actualCurve-forecastCurve exactly
  report MAE as exact rational minor-units/day, maximum error, minimum-balance error,
         first-buffer-crossing difference and unmatched-event coverage
  leave percentage metrics undefined where zero/negative denominators make them misleading
```

Use held-out saved forecasts and report sample size/horizon/coverage. A correct closing balance does not imply correct liquidity timing. A credit not committed at the forecast cutoff may legitimately be a later event, not evidence that the forecast ignored known information.

## Persistence and readers

Capture actual memberships under a fixed recorded cutoff, calculate outside locks and persist the score with immutable identity links. A later payment/reconciliation change produces another score revision. This is read-only financial analysis; it does not change due dates, probabilities, legal balances or payment plans.

The UI shows original forecast assumptions and each explainable error. Any suggested model/heuristic improvement becomes a separately evaluated policy version, not an automatic rewrite of future invoice expected dates. Restricted payroll contributions stay aggregated unless the evaluator has permission to inspect them.

```text
forecast +100 on day5; actual+80 on day7
at day5: timing -80 + amount -20 = balance error-100
at day7: timing0 + amount-20 = balance error-20
forecast closing correct but day5 liquidity shortfall -> timing error still visible
actual statement missing last week -> horizon incomplete, no full-horizon score
```

Deliver one retained vintage-to-realized-outcome comparison with exact decomposition and coverage. No claim of improved predictive accuracy follows from the existence of a scoring module.
