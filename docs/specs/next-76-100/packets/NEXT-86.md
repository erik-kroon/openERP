# NEXT-86: ROT/RUT split claims and customer-authority settlement

**Priority when applicable:** P2. **Lane:** TAX.

**New work:** Add the explicitly conditional household-work profile, with labour evidence, split obligors and claim/rejection recovery. Mixed-rate ordinary invoices are not this workflow.

**Use existing owners:** Existing invoice/tax facts, receivable allocations, customer credit and external declaration-attempt owners.

**Required earlier contracts:** NEXT-51, NEXT-15, NEXT-30, NEXT-49.

**Evidence basis:** R02, X02. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Original consideration remains complete

```text
HouseholdWorkCase {customerPersonRefs, property/workFacts, workCategory,
  performedCoverage, labour/material/travelLineBreakdown,
  customerPaymentRefs, applicableRelease, reportedAllowanceEvidence}
AuthorityClaimSlice {caseId, person, performedAndPaidCoverage,
  eligibleAmount, priorClaimedAmount, claimArtifact, outcome, authorityReceivableRef}
```

Invoice gross revenue and VAT do not shrink because a customer requests relief. Labour, materials and other charges retain their original economic meaning. Shared per-person caps need sourced information and a clear limitation when other providers' usage is unknown; this book cannot guarantee the customer's total national allowance.

## Calculation and financial admission

```text
prepareHouseholdInvoice(case):
  use ordinary qualified invoice arithmetic for full consideration and VAT
  calculate conditional relief only for eligible performed labour and person/date facts
  display planned customer payment and conditional authority share distinctly
  recognition uses the selected qualified receivable policy, not a fictional grant discount

prepareClaim(case, paidAndPerformedScope):
  require work and customer-payment prerequisites for selected rule
  compute eligible gross labour share with exact cumulative partial-payment allocation
  apply qualified person caps/rates/date rules and prior effective claim coverage
  newClaim = eligibleCumulativeClaim - priorEffectiveClaims
  require newClaim>=0 and no duplicated labour/payment entitlement
```

Official guidance distinguishes work/payment eligibility and partial-payment claim coverage; authority payment is not simply a tax-account deposit [X02]. Do not implement a generic current-rate multiplier independent of payment year or scope. No fixed statutory rates are activated here.

When the profile's recognition threshold for a claim receivable is established, reclassify its exact amount from the customer receivable to the authority claim receivable. Until then, retain the conditional split without an unsupported financial transfer. The customer and authority positions must jointly reconcile to recognized invoice principal after actual collections; never create both full customer debt and an additional full authority asset.

## Claim, outcome and rejection

A human approves the exact claim and scope. Persist one submission attempt before the external action and use documented outcome recovery. Registered/submitted claims do not mean paid. Actual bank receipt debits bank and credits the authority claim; a documented authority offset uses its actual destination obligation, not an invented bank receipt.

```text
onRejectedClaim(amount):
  retain authority decision and original claim
  if reviewed customer agreement supports additional customer debt:
      debit customer AR; credit authority claim amount
  else:
      prepare supported loss/dispute treatment with evidence
  do not create new sale revenue or VAT
```

Revisions reduce or replace explicit claim slices. Credits to the original invoice propagate through its relieved labour, claim/repayment and customer capacities using one complete owned plan. A cash-method case needs its own supported tax-recognition profile rather than silently borrowing accrual behavior.

## Complete journey

Show full invoice, customer payments, eligible labour, already claimed, accepted/rejected and collected amounts. Deadlines and identity use the qualified rule release. Keep sensitive person/property facts out of general summaries.

```text
synthetic invoice gross125000; supported claim25000; customer pays100000
reclass claim25000 -> combined remaining25000, revenue/VAT unchanged
claim accepted and bank25000 -> both receivables0
claim rejected -> customer debt or evidenced loss, never stranded invisible amount
same paid/work slice requested twice -> capacity refusal
```

Delivery requires actual claim artifact validation and an authorized official-channel outcome for the external stage. A plausible relief calculation is not legal/company qualification.
