# NEXT-90: Conditional grants, earned funding and repayment obligations

**Priority when applicable:** P2. **Lane:** INCOME.

**New work:** Add a bounded operating-grant lifecycle separate from sales and loans. This is a proposed accounting expansion, not a finding that a current grant implementation is defective.

**Use existing owners:** Source evidence, qualified recognition rules, GL, grant receivable/deferred-income and tax-bridge owners.

**Required earlier contracts:** NEXT-02, NEXT-03, NEXT-13, NEXT-22.

**Evidence basis:** R03, P31. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Conditions and earned coverage

```text
GrantAward {funder, agreementRevision, fundingCap, eligiblePeriod,
  eligibleCostCategories, milestones, evidenceRequirements,
  paymentSchedule, repaymentConditions, accounting/taxProfile}
GrantEntitlementSnapshot {awardId, recognizedEligibleCosts,
  reviewedAchievementEvidence, earnedTarget, cashReceived,
  previousRecognition, disputedOrUnknownConditions}
```

Start with a qualified cost-related operating grant. Customer consideration, asset-cost grants, state loans and uncertain funding awards are different profiles. Receiving money does not by itself establish income. A submitted application does not establish a receivable.

## Recognition graph

```text
eligibleCost = sum explicitly qualified actual cost components allocated to this award
require no source cost allocated beyond its permitted funding coverage
T = min(cap, qualified reimbursementFraction * eligibleCost)
require all recognition conditions evidenced before selecting earnedTarget T
D = T - previouslyEffectiveEarnedIncome
```

The profile fixes gross-income versus expense-offset presentation. It cannot switch based on which result looks better. The first implementation uses an explicit grant-income role so original expenses remain visible, unless the activated policy requires and implements another treatment.

Cash received before earning debits bank and credits deferred grant liability. As conditions are met, debit deferred liability to the available extent and debit a qualified grant receivable for any excess entitlement, with one credit to earned grant income. Later cash consumes the receivable first; genuinely unearned excess remains deferred rather than extra income.

```text
recognizeNewEarned(D):
  fromDeferred = min(D, unearnedCashLiability)
  debit deferredGrant fromDeferred
  debit grantReceivable D-fromDeferred
  credit grantIncome D
```

For a supported negative entitlement revision D=priorEarned-newEarned, first identify the matching uncollected entitlement U. Credit its receivable by min(D,U), debit grant income D and credit deferred or repayment liability by D-min(D,U). The selected award policy and actual funder decision determine which liability is correct; an unsupported classification blocks execution. All amounts refer to the same affected entitlement components, not unrelated receivables. Actual repayments debit that liability and credit cash with no second income reversal. Never leave a rejected receivable in place merely to preserve an expected dashboard balance.

## Atomic ownership and reporting

Each entitlement revision freezes award, cost and condition membership. Journal, recognised entitlement effects and cost-coverage claims commit together. A new review cannot earn the same cost twice under the same award. Multiple grants funding one cost need explicit allowed stacking limits; otherwise refuse overlapping funded coverage rather than double counting support.

Provider certification/submission and received funds are separate records. The corporate-tax bridge uses a qualified tax treatment and timing, not the assumption every grant is tax-free. Unknown conditions block complete recognition but not evidence capture or a cash receipt into deferred liability under the supported policy.

## UI and vectors

Show awarded cap, eligible cost, earned amount, unearned cash, receivable, repayments and outstanding conditions. Open work is tied to exact evidence gaps rather than a generic confidence score.

```text
cash advance50000 -> bank50000/deferred50000
eligible cost60000 at synthetic1/2 -> earned30000; deferred remains20000
later earned target70000 -> additional40000: deferred debit20000,
    receivable debit20000, income credit40000
cash receipt20000 -> receivable0, no new grant income
rejected condition -> supported entitlement reversal/repayment plan, not automatic tax exemption
```

Completion includes negative revisions, cash adoption and independent GL controls. This packet does not search for subsidies, promise funding or decide a real agreement's recognition terms without qualification.
