# NEXT-87: Pension invoice reconciliation and SLP annual basis

**Priority when applicable:** P2. **Lane:** PAYROLL.

**New work:** Add actual pension provider charges, reconciliation against accrued obligations and separate special-payroll-tax basis. Regular pay calculations do not implement this evidence lifecycle.

**Use existing owners:** Payroll provisions, purchasing, tax bridge, private personnel scope and tax-account assessment owners.

**Required earlier contracts:** NEXT-03, NEXT-20, NEXT-22.

**Conditional gates:** NEXT-35: payroll accruals already include pension provisions.

**Evidence basis:** R03, X03. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Contract and source components

```text
PensionCharge {providerDocument, employmentOrPolicyRef,
  coveragePeriod, components:[premium|riskInsurance|adminFee|other],
  exactAmounts, taxTreatmentWitness, correctionOf?}
PensionAccrualAllocation {payrollProvisionId, chargeComponentId, consumedProvision}
SLPBasisComponent {sourceIdentity, effectiveDate, statutoryCategory,
  signedIncludedAmount, exclusionReason?, reportingYear, ruleVersion}
```

A provider total may include pension premiums, risk cover and fees with different treatment. Neither all payroll cost nor all amounts on the invoice are automatically SLP basis. The official guidance distinguishes SLP and ordinary employer reporting [X03]; use the selected dated component rules and actual provider statements.

## Reconcile before recognizing twice

```text
compilePensionCharge(charge, accruals):
  require complete component classification and original provider identity
  for component:
    A = explicitly matched available prior pension provision
    C = qualified actual component cost excluding separately recoverable VAT
    debit pension provision A
    addSigned corresponding cost C-A
  V = separately qualified deductible VAT on supported fee components only
  debit input VAT V through the purchase tax owner if nonzero
  require sum(C)+V == retained invoice gross
  credit supplier payable sum(C)+V
  publish supported SLP-basis components from qualified recognition facts
```

Tax/deductibility is a separate component decision. A VAT-bearing provider fee uses the purchase tax owner where supported; do not subtract input VAT merely because a provider supplies pensions. A payment later settles AP only. Repeated payroll accrual and supplier-invoice intake cannot both own the same principal expense.

## Annual SLP computation

```text
prepareAnnualSLP(year):
  capture qualified included/excluded source components and prior carry basis
  reconcile provider statements, financial costs and documented timing differences
  B = sum(category-directed contributions under the selected statutory formula)
  T = qualified rounding and rate computation on supported taxable basis
  if negative/carry-forward treatment not supported by release: explicit blocker
  delta = T - priorEffectiveSLPExpenseLiabilityForYear
  debit SLP expense delta
  credit SLP liability delta
```

A corrected provider statement revises the supported target and produces only the delta. It does not post another full annual tax. The tax-account owner records actual assessed charges later. A calculated SLP liability is not provider payment, AGI submission or observed tax-account balance.

NEXT-22/74 consume exact declared SLP basis and its source/GL bridge through a dedicated form mapping. Keep this distinct from the ordinary contribution calculation and avoid adding pension components again as salary merely to reach a declaration.

## Atomicity, dates and privacy

Charge recognition, prior-provision release, supported basis facts and receipt are one transaction. Final annual SLP execution rechecks complete membership and prior targets. Retroactive corrections use the approved accounting date while preserving original coverage/reporting attribution; closed history is not rewritten.

Only permitted payroll users inspect individual pension details. Shared reports can show aggregate controls without granting raw employee access. No automatic provider certificate or contract entitlement is inferred from a received invoice.

```text
provision10000; actual premium11000 -> provision debit10000, cost debit1000, AP11000
synthetic SLP basis50000 at1/5 -> target10000; prior8000 -> adjustment2000
provider total contains unsupported fee -> named exclusion/blocker, not blanket inclusion
payment11000 -> AP settled, pension cost and SLP basis not recreated
```

Acceptance includes reconciled provider/GL/payroll contributions and the corporate-return consumer. Complete official tables, private facts and real provider access remain separately qualified inputs.
