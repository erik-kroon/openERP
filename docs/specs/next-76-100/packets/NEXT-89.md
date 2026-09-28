# NEXT-89: Dividend resolutions, shareholder payables and KU31 preparation

**Priority when applicable:** P2. **Lane:** EQUITY.

**New work:** Add a company-side dividend lifecycle with real resolution evidence, shareholder entitlements and reporting. It is not owner expense reimbursement or personal K10 optimization.

**Use existing owners:** Reviewed company/financial statements, ownership evidence, liability/payment and statutory artifact owners.

**Required earlier contracts:** NEXT-02, NEXT-22, NEXT-23, NEXT-49.

**Evidence basis:** X04, X05, P24. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Decision is not a forecast recommendation

```text
DividendResolution {entity, meetingEvidence, approvedFinancialBasis,
  declaredAmount, shareClassRights, entitledHoldersSnapshot,
  availabilityDate, paymentTerms, requiredBoardAssessment,
  legalProfile, version}
DividendEntitlement {resolutionId, holderIdentity, sharesOrRight,
  grossEntitlement, withholdingTreatment, paidComponents, KUIdentity}
```

The first profile is one supported ordinary AB distribution with actual meeting/board evidence and established shareholder rights. Cash headroom, retained earnings or an AI-generated minute cannot independently authorize a value transfer. Applicable capital-protection and prudence requirements need reviewed evidence [X05], not just a positive bank balance.

## Prepare and record

```text
prepareDividend(resolution):
  require actual authorised resolution and permitted financial/legal basis
  require complete entitled-holder snapshot and known class rights
  compute exact entitlements from the resolution's per-share or fixed allocation rule
  require sum(entitlements)==declaredAmount and all rounding differences explicitly resolved
  reject missing resident/status facts needed for supported withholding/reporting
  debit approved distributable-equity role declaredAmount
  credit dividend-payable role declaredAmount
```

This reclassifies equity into a liability only at the qualified recognition event. A draft distribution proposal remains nonfinancial. The accounting identity is the actual resolution, not its upload or review ID. Execute the journal and entitlement obligations together with independent required review and a receipt.

## Payment and reporting

Actual payout debits dividend payable and credits bank, plus a separately qualified withholding liability if required. Ordinary employee withholding rules are not reused. An instructed transfer or a due date is not cash evidence. Do not automatically assume either withholding or no withholding for every recipient.

KU31 preparation captures recipient identity, entitlement, relevant availability/reporting period and required form fields from the selected profile. It does not simply copy bank payment year if the actual legal reporting trigger differs. Preserve the original stable item identity for replacement reporting and retain exported/submitted evidence separately. Official examples illustrate issuer obligations for supported dividends [X04]; they do not activate every share/residency case here.

## Corrections and controls

A voided/mistaken resolution needs actual legal evidence and the appropriate supported accounting correction. Once distributed, do not silently reverse cash or deduct repayment from future owner expenses. A lawful recovery creates its own receivable and reporting-impact decision. Unsupported unlawful-distribution recovery remains a blocker rather than guessed income.

Reconcile total declared, actual payable, net payouts and withheld liabilities to the GL. Individual shareholder files have explicit private access; the general company view can show aggregate equity/liability effects.

```text
actual declaration100000 across rights3/5 and2/5 -> entitlements60000/40000
pay first holder20000 -> payable80000, equity already reduced100000 only once
same meeting resolution under new key -> AlreadyApplied
forecast shows surplus200000 -> cannot create dividend resolution or approval
```

Deliver issuer-side preparation, approved recognition, payout linkage and qualified KU31 handoff. No personal dividend tax planning, automated company-law conclusion or market-traded share registry is included.
