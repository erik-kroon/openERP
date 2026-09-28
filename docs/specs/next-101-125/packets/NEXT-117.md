# NEXT-117: Interest statements: KU20 and applicable KU25 identities

**Priority when applicable:** P2. **Owner lane:** TAX.

**New scope:** KU31 covers dividends and AGI covers compensation. Add annual interest reporting with its own reporter/recipient, timing and correction rules rather than treating every loan accrual as a reportable amount.

**Existing owner to extend:** Existing loan interest, actual settlement, tax withholding and versioned information-return artifact owners.

**Earlier contracts:** NEXT-32, NEXT-49. **This-wave dependencies:** None.

**Conditional:** NEXT-62: received late-payment interest creates an applicable reporting obligation.

**Basis:** X07, P32 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Obligation and direction

```text
InterestReportingObligation {
  reportingEntity, incomeYear, family: KU20|KU25,
  recipientOrBorrowerIdentity, actualReportingDutyWitness,
  applicableInstrument/securityFacts, qualifiedRelease
}
ReportableInterestEvent {
  originalInterestComponent, paidOrMadeAvailableDate,
  originalCurrencyAmount, SEKReportingAmount, conversionWitness,
  withholdingIfApplicable, sourcePaymentOrCreditingEvidence
}
InterestStatementRevision {
  obligationId, specificationNumber, selectedEventIds,
  reportedValues, exclusions, previousFiledIdentity, artifactDigest
}
```

The company paying interest on a shareholder loan may have KU20 duties. Its own interest expense paid to a bank is not therefore a KU25 it should issue. KU25 applies only where this entity is the actual qualifying reporter of the recipient individual's interest expense. Late-interest-only and other exceptions need their real rules.

The current official page also has year-specific digital format changes [X07]. Do not reuse an old PDF/field map merely because the form family name remains KU25. Acquire the actual supported year schema and rules before release.

## Select the reportable population

```text
captureInterestStatement(obligation):
  require reporter identity, recipient class and actual reporting duty established
  select interest events by this family's legally relevant paid/available timing rule
  keep accrued but unreported interest in an explicit bridge
  apply instrument, prepaid-interest, security and withholding rules by exact release
  convert using the qualified reporting-date/source rule, not year-end cash remeasurement
  require each economic interest component included once per permitted reporting meaning
```

Cash payment and crediting an available account may have different evidence but can identify the same reportable event. Do not count both. A book interest accrual alone is not assumed available to the recipient. Conversely a genuine availability event is not omitted merely because cash transfer occurs later. The activated rule specifies the distinction.

## Withholding and financial linkage

If the selected KU20 case requires withholding, its actual liability and payment come from the interest-payment operation, not a new journal when exporting the statement. Extend that operation's internal compiler so it splits gross interest into net recipient amount and withholding liability in the same financial group, retaining the applicable authority. No withholding percentage is hardcoded in this packet.

```text
grossInterest = netPaid + actualWithholding
report values = exact captured gross and withholding under the permitted year rules
```

Missing required actual withholding evidence is a reconciliation blocker; the renderer cannot fabricate a tax liability after year end to match an expected formula. Corrections to financial interest stay separate from reporting-only corrections.

## Artifact and correction identity

```text
prepareInterestStatement(command):
  capture complete event/correction population and independent recipient controls
  calculate exact year totals and qualified field mappings
  retain same nonzero specification identity for a replacement of the same item
  seal semantic revision plus schema/calculator version
  render and validate through the existing information-return artifact infrastructure
```

A corrected year amount creates a new revision preserving original submitted bytes. A second specification number can create an additional valid item rather than replace the first, so the operation must distinguish replacement, removal and genuinely distinct reporting items. Exact current submission actions remain external-attempt operations with actual representative authority and receipts.

## Controls and examples

Reconcile: opening accrued interest plus current accruals and supported changes, less actual paid/available components, equals closing accrual. The statement uses its qualified subset of those components and timing bridge, not the complete GL expense sum. Confidential individual identities are protected under the selected tax-reporting grant.

```text
accrued12000, supported reportable paid/available8000 -> report8000,
    remaining4000 shown as timing basis, not silently reported12000
same8000 credited then transferred in cash -> one event8000
gross8000/net6000/actual withheld2000 synthetic -> equality holds
company pays its bank interest -> not automatically an outbound KU25
replacement changes only amount -> same reporter/year/person/specification identity
```

Completion requires correct duty selection, supported-year electronic artifacts, immutable corrections and source controls. This packet does not originate consumer loans or provide personal tax planning.
