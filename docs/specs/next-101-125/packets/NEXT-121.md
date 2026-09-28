# NEXT-121: Opt-in bounded standing posting mandates

**Priority when applicable:** P1. **Owner lane:** AGENT.

**New scope:** Multi-human approval covers exact plans. Add an explicitly enabled later-scope authority for a narrowly allowed recurring purchase pattern, with atomic cumulative limits. Book Zero remains exact-human-approval by default.

**Existing owner to extend:** Existing admission, rule activation, plan execution and financial receipts; extend only explicitly allowlisted application operations.

**Earlier contracts:** NEXT-02, NEXT-03, NEXT-16, NEXT-96. **This-wave dependencies:** None.

**Basis:** R02, R03, P96 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## A new authority kind, never a forged approval

```text
ExecutionAuthority = ExactApprovalRef | SupportedStandingMandateRef
StandingMandateRevision {
  book, allowedOperationAndCompilerVersions,
  reviewedSupplierAndServiceIdentities, permittedSourceEvidenceClasses,
  specificRuleReleaseIds, accounts, currency,
  postingDate/periodRestrictions, perEventLimit,
  sharedBudgetPoolIds, maxCount, validity, authorizingHumans,
  revocationEpoch, explicitExcludedCases
}
MandateConsumption {
  mandateRevision, originalEconomicEvent, planDigest, receiptId,
  chargedBudgetBuckets, grossRiskAmount, eventCount
}
```

Default feature state is off. First supported operation is qualified same-currency purchase recognition for an evidenced recurring service pattern. Exclude payments, refunds, legal document issue, payroll, tax adjustments, corrections, filing, period close and signing. A later scope extension needs its own explicit qualified authority contract.

The plan is still calculated and sealed by the real purchase owner. The mandate authorizes execution only when its exact eligibility predicate and bounds hold. A model probability or previous approval frequency cannot satisfy source truth or grant power.

## Human activation and eligibility

```text
prepareMandate(candidate):
  require narrow stable supplier/service/source pattern and supported rule versions
  evaluate against retained independently reviewed examples and adverse cases
  list every operation excluded and every shared budget affected
  freeze exact conditions, limits and effective interval
activateMandate:
  require configured independent human/role quorum through NEXT-96
  grant only the scope approved; agents cannot activate or expand it
```

Required input fields come from verified structured sources or actual human review under the stated evidence policy. Newly inferred supplier identity, changed tax treatment, missing invoice, changed rate or conflicting credit becomes human review. Never approve a free-form prompt whose semantic scope can widen later.

## Atomic budgets and financial effect

Use cumulative gross recognized purchase exposure for the first profile, not debit-plus-credit totals or net tax. Currency is fixed. Buckets include per supplier/window, mandate lifetime and any shared book risk pool. An amendment/new mandate references the existing pool rather than resetting its consumed amount.

```text
executePurchaseUnderMandate(command): OwnedTx
  current actor/service permission and book lock
  replay original command BEFORE new-work limit/expiry checks
  load exact sealed plan, mandate revision and current authority witnesses
  validate plan facts/rules/versions against complete allowed pattern
  now = trusted database instant after potentially blocking locks
  bucketKeys = selected calendar windows in declared book timezone
  lock all shared budget rows in deterministic order
  require used+newGross<=eachLimit and count+1<=eachCountLimit
  require unrevoked mandate and current authorizer policy as selected
  call existing PurchaseApp.applyWithinTransaction(tx, validatedPlan)
  append consumption for original economic identity and all budget increments
  append receipt and outbox; commit everything together
```

Preparation does not consume capacity. An unsuccessful transaction consumes none. A lost successful response must replay before checking the now-full budget; it cannot count the event again. No automatic credit/reversal restores budget headroom in this first policy, because that would permit cycling exposure. Human-reviewed budget amendments remain possible and auditable.

Backdating the accounting date cannot choose yesterday's empty risk bucket. Budget time is the selected trusted execution calendar; accounting eligibility has its separate approved date rule. A task waiting beyond mandate expiry is no longer eligible merely because its plan was prepared earlier.

## Rollout, suspension and output

Begin shadow mode: evaluate proposed executions and reasons without any new authority use. Promotion needs actual supported journey/race evidence and human activation, not just a passing mean score. Suspension blocks new admissions; it does not erase receipts or imply admitted work failed. The authority owner must prove ordering with revocation, shared budget consumption and other human executors using the same pool.

```text
limit100000, consumed70000, eligible event25000 -> consumed95000
another10000 -> refused, no journal or partial budget increment
same25000 request after commit/expiry -> original receipt, still consumed95000
two concurrent events20000 at used70000 -> at most one fits
new mandate same supplier/pool -> existing pool usage retained
```

UI shows exact scope, expiration, remaining limits, each autonomous receipt and the human who activated the rule. No existing operation gains this authority simply because a default permission annotation was omitted.
