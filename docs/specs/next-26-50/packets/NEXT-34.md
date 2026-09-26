# NEXT-34: Mileage reimbursement with exact tax and payout partition

**Priority:** P2. **Owner lane:** PAYROLL. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Employee claim and payroll handoff owners. Add trip evidence and qualified rate calculation without altering receipt matching or inventing a universal mileage rate.

**New scope, not repeated work:** The first wave does not calculate trips. This adds distance-based reimbursement with distinct entitlement, tax-free limit and taxable excess.

**Dependencies:** NEXT-33. **Integrate after:** APP-SLICE-READY(payroll-foundation).

**Conditional gates:** NEXT-20: the selected entitlement includes taxable compensation; NEXT-21: payout/reporting uses payroll.

**Evidence:** R03, R10 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Inputs and release contract

```text
TripRevision {
  id, claimantId, businessPurpose, departure/arrival local dates,
  routeEvidence, origin, destination, distanceInMeters,
  vehicleIdentity, ownershipKind, fuelPaymentFacts,
  passengersOrOtherRelevantFacts, recordClass, previousRevision
}
MileageRuleRelease {
  applicability, distanceUnit, entitlementRule,
  exemptionRule, taxableExcessRule, roundingPolicy,
  requiredVehicleAndPayerFacts, evidenceSourceHash
}
TripAward immutable {
  tripRevision, ruleRelease, distanceWitness,
  entitlement, exemptionCeiling, exemptPaidPart, taxablePart,
  qualifiedTaxComponents, payoutRoute, receipt
}
```

Distance is an exact unit-bearing value. A displayed kilometre is not a Swedish mile, and decimals are not silently truncated. Route estimates are suggestions until reviewed. Use a selected legal/employment entitlement and a separately selected tax exemption profile; neither is inferred from the other.

## Pure calculation

```text
calculateMileage(trip, facts, release):
  require trip dates, business purpose, distance and required vehicle facts established
  require no duplicate or overlapping same economic trip claim
  require release supports this claimant/vehicle/payer/date combination
  distance = exactRational(trip.distanceInMeters, metersPerReleaseUnit)
  entitlement = round(distance * release.entitlementRate, entitlementRounding)
  ceiling = round(distance * release.taxExemptRate, taxRounding)
  exemptPaidPart = min(entitlement, ceiling)
  taxablePart = entitlement-exemptPaidPart
  require entitlement>=0 and exemptPaidPart+taxablePart==entitlement
  return all inputs, exact intermediates and outputs
```

The simple min formula applies only to a qualified profile whose exemption is a per-distance ceiling. Other car/fuel/benefit arrangements must supply a different explicit supported profile or refuse. Rates below are synthetic test inputs, not statutory rates.

## Financial handoff

```text
prepareTripAward(input):
  capture trip revision, prior awards, payroll/claim capacity and rule witness
  compute split; require current reviewed route
  if taxablePart>0: require the corresponding payroll profile exists
  seal exempt component and taxable component as disjoint source identities

executeTripAward(plan): FinancialTx
  append award and exclusive handoff manifest
  exempt part:
    record reimbursable employee liability/cost through NEXT-33's owner
  taxable part:
    debit qualified taxable-travel compensation expense
    credit accrued taxable-award liability
    create one payroll instruction referencing that EXISTING entitlement liability
    payroll later consumes the liability instead of expensing the award again
    no direct-payment route exists for this component
  append receipt and preparation outbox
```

The first supported accrual profile recognizes the taxable entitlement at award time. Payroll remains the sole owner of withholding, employer contributions and paid reporting for that component. Its gross-pay calculation includes the taxable amount while its journal debits the existing award liability, not wage expense again. A different recognition policy would require a separately qualified profile, not a caller flag.

A mileage award does not generate deductible invoice VAT merely from its tax-free status. Separate actual parking/toll receipts use purchase/claim rules with separate source identities. Do not add them to distance or reimburse them twice.

## Correction, payouts and controls

Revising distance after approval does not edit the award. Before handoff is consumed, prepare an exact replacing award. After payment or payroll reporting, produce a delta with an owned employee/payroll correction and the original trip reference. An overclaim does not become an unexplained negative net salary. Require the relevant lawful recovery/offset basis.

A trip can be paid through a bank payable or payroll, never both. Retain each attempted handoff and cancellation evidence. Claim totals reconcile to exempt liability plus taxable payroll instructions; settled instructions then reconcile to actual payment evidence.

## UI and vectors

Show unit, route, distance evidence, vehicle facts, entitlement, exempt part, taxable part and the selected payroll/direct route before approval. A missing vehicle fact blocks calculation but not trip capture.

```text
synthetic distance15000m, unit1000m, entitlement300 minor/unit,
exempt ceiling250 minor/unit -> entitlement4500, exempt3750, taxable750
same trip under second key -> no second award
missing fuel-payer fact required by profile -> incomplete, not private-car default
trip changed after pay-run approval -> old award retained + correction case
direct-payout selection with taxable component but no payroll owner -> refuse
```

The packet is complete only with the selected payroll/claim handoff and its controls. A mileage total displayed without downstream exclusive ownership is not the delivered workflow.
