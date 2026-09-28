# NEXT-119: Cash share subscriptions and registered-capital transition

**Priority when applicable:** P2. **Owner lane:** EQUITY.

**New scope:** Dividends distribute existing equity. Add the company-side record of cash subscriptions, paid allotments and an evidenced capital-registration transition without inventing share rights from bank receipts.

**Existing owner to extend:** Existing company/shareholder facts, bank receipt, equity roles, signed-decision and external-obligation owners.

**Earlier contracts:** NEXT-02, NEXT-13, NEXT-49, NEXT-89. **This-wave dependencies:** None.

**Basis:** X09, P89 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Restrict the first issue profile

Support a reviewed cash issue with fixed subscription terms and explicit nominal/premium allocation. Exclude noncash contributions, convertibles, warrants, mergers, debt conversion and complex conditional instruments until their own legal/accounting profiles exist. Public registration instructions identify a process, not the validity of a particular company resolution [X09].

```text
CashIssueResolutionRevision {
  companyIdentity, actualDecisionEvidence, authorizedScope,
  classAndRightsFacts, maximumShares, subscriptionPrice,
  nominalAmountPerShare, premiumAllocationPolicy,
  subscriptionWindow, paymentAndRegistrationConditions
}
Subscription {subscriberIdentity, acceptedUnits, termsRevision, legalCommitmentEvidence}
SubscriptionCashEffect {sourceBankIdentity, subscriber, amount, accountingRole, receipt}
AllotmentEffect {subscription, units, nominalAmount, premiumAmount, effectiveConditions, receipt}
CapitalRegistrationObservation {authorityReceipt, registeredIssueIdentity, amount, dates, scope}
```

A bank transfer carrying the word shares is not automatically registered share capital. Conditional/refundable money remains in the selected liability/holding role until the reviewed legal/accounting conditions support another classification. Issuance fees and their tax treatment are separate source-backed costs, not deducted from nominal capital without authority.

## Exact money and units

```text
prepareCashAllotment(subscription, paidSources):
  require original valid resolution and subscription conditions established
  units = reviewed accepted/allotted integer units
  require units<=remaining resolution/subscription capacity
  total = units * exactSubscriptionPrice
  nominal = units * exactNominalPerShare
  premium = total-nominal
  require premium>=0 for the selected profile
  require evidenced allocatable payment covers required total
  require no cash source used for another subscription or financial receipt
  capture all remaining conditions and registration state
```

A rounding policy cannot create fractional share units or silently absorb an underpayment. Overpayments are separately refundable/unallocated funds, not additional issued shares. Partial payment/allotment requires a profile that defines exactly which subscription units can be allotted; otherwise the funds stay pending.

## Accounting stages

For the selected refundable-before-allotment profile:

```text
actual receipt P:
  debit bank P
  credit pending subscription funds liability P

qualified effective paid allotment P=N+S:
  debit pending subscription funds liability P
  credit unregistered issue nominal role N
  credit unregistered premium role S

verified registration:
  transfer nominal N to registered capital role
  transfer premium S to its correctly classified paid-in-premium role
  update company/shareholder issue facts through the owning reviewed operation
```

The precise intermediate equity/liability classifications are selected by a qualified framework and legal-condition decision. Do not treat this illustrative profile as a universal rule or post registered capital before the required evidence. Where an initial receipt was already posted correctly, adopt its unused allocation rather than debit bank again.

All source usage, allotted unit capacity, journal and receipt commit atomically per supported stage. Registration consumes the exact allotted issue once. An authority response for another issue or partial amount cannot register the whole plan.

## Failure and correction

If an issue fails or lapses, determine the actual refundable obligation from the retained terms/decision. Restore or reclassify pending equity through the supported complete correction, then separately settle real cash refunds. Never erase the receipt, create negative registered shares or use dividend permission as an issue-cancellation power.

The maintained shareholder register/entitlement owner preserves dates and classes for later dividends. This is not a trading system, cap-table valuation product or authority filing done from an API response alone.

```text
100 units at1000 minor, nominal200 each -> total100000, capital20000, premium80000
bank receives105000 ->100000 subscription capacity +5000 explicit excess
pending funds received but subscription unaccepted -> registered capital0
same registration receipt retried -> one classification transition
registered receipt20000 nominal does not imply another100 units can be allotted
```

Completion includes company/equity control reconciliation, actual source references and an honest registration/return-of-funds state. A generated resolution template does not establish the real decision.
