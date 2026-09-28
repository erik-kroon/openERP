# NEXT-115: Overnight travel allowances and meal-benefit partition

**Priority when applicable:** P2. **Owner lane:** PAYROLL.

**New scope:** Mileage reimburses distance. Add overnight business-travel allowance eligibility, country/day classification and separate meal reductions/benefit inputs without reusing the mileage rate formula.

**Existing owner to extend:** Existing employee trip, claim, payroll earning/benefit and payout-handoff owners.

**Earlier contracts:** NEXT-33, NEXT-20, NEXT-21. **This-wave dependencies:** None.

**Conditional:** NEXT-34: the same retained trip also includes a mileage award.

**Basis:** X05, P34 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Facts and independent classifications

```text
TravelStayRevision {
  employee, departure/return instants, actual business locations,
  ordinary workplace/home facts, overnight evidence,
  itinerary segments, accommodationPayer, mealEvents,
  continuousLocationHistory, employmentAgreementAllowance
}
MealDecision {
  mealType, actualProvider/Payer, mandatoryInTransportOrHotelPrice,
  external/internalRepresentationWitness, sourceReceipt,
  reducesAllowance, createsTaxableBenefit, ruleWitness
}
TravelAward {
  exact day/country/night classifications, agreedEntitlement,
  exemptLimitAfterReductions, exemptPaidPart, taxableExcess,
  mealBenefitComponents, alreadyRecognizedCostRefs, payoutRoute
}
```

The official guidance distinguishes allowance reduction from taxable meals: they are not always the same condition [X05]. Do not encode `freeMeal => reduce allowance and create benefit` for every meal. A compulsory hotel breakfast, for example, needs its own reviewed branch. Keep the actual source and chosen rule evidence.

## Calendar and calculation

```text
calculateTravelAward(trip, profile):
  require actual business-trip/overnight eligibility and complete itinerary
  split using the profile's day, country and travel-time attribution rules
  include continuous prior stays for reduced-rate thresholds; new tripId cannot reset duration
  for eligible segment:
    baseLimit = dated qualified country/day/night allowance
    reduction = exact supported meal/accommodation reductions
    remainingExemptLimit = max(baseLimit-reduction,0)
    entitlement = employment/travel agreement amount for this segment
    exemptPaid = min(entitlement,remainingExemptLimit)
    taxableExcess = entitlement-exemptPaid
    mealBenefits = independent qualified benefit valuation for applicable meals
  retain exact intermediates and aggregate under the rule's prescribed rounding order
```

Country changes, arrival/departure classification and long-term assignment exceptions need their actual release data. Do not multiply elapsed24-hour blocks by a universal rate, reset a continuous stay at fiscal year end or treat employee overnight assertions as verified accommodation evidence.

The first implementation can support one domestic short-stay profile with explicit boundaries. Foreign/long-duration cases are then named unsupported rather than guessed from the nearest country's amount. Evidence intake remains usable while the calculation is blocked.

## Exclusive handoff and posting

Use distinct component identities for mileage, per diem, actual hotel receipts and taxable meals so the same trip can legitimately contain all without paying a receipt twice. The exemption is a tax classification, not employer contractual entitlement or a deductible VAT invoice.

The exempt reimbursement reaches NEXT-33's recognized employee liability and one payroll/direct route. Taxable excess is one payroll earning component. Taxable noncash meals reach the benefit owner without creating another cash reimbursement. If meal costs were already purchased by the company, they are not expensed again when the benefit is reported.

```text
executeTravelAward(plan): OwnedTx
  recheck trip/meal/continuous-stay/rate and payout-owner versions
  recognize only the supported reimbursement/earning liabilities assigned to this owner
  create exact existing-liability payroll instructions where already accrued
  publish meal-benefit facts separately from cash entitlement
  commit source-component capacities and receipt together
```

A changed itinerary after payment follows NEXT-36's qualified recovery/adjustment path. An expired queue claim is not proof the old allowance was never paid. Route replacement requires the prior route's actual unconsumed/released status.

## Views and examples

Show each day/night, country, supplied meals, contract amount, exemption ceiling, excess and noncash benefit. Employee explanations omit other employees' data. Payroll reports expose the actual paid/provided period rather than the request date.

```text
synthetic agreed allowance3000, base limit2500, qualified meal reduction500
  => exempt2000 + taxable cash1000
separate supplied meal benefit400 -> noncash payroll base400, not extra400 cash
mandatory hotel breakfast case -> apply its distinct reduction/benefit rule
same meal also entered as employee-paid receipt -> payer conflict requiring review
same stay split into two requests -> continuous duration preserved
```

The amounts are hypothetical design vectors. Actual tables, timing thresholds, eligibility and meal exceptions must be qualified before the selected company uses the calculation.
