# NEXT-112: Domestic construction reverse-charge sales and purchases

**Priority when applicable:** P2. **Owner lane:** TAX.

**New scope:** Add a qualified domestic construction reverse-charge profile. Cross-border services and ROT/RUT claims do not establish the seller/buyer conditions for this treatment.

**Existing owner to extend:** Existing invoice issue, purchase recognition, tax-fact and credit-note owners.

**Earlier contracts:** NEXT-03, NEXT-04, NEXT-51, NEXT-15. **This-wave dependencies:** None.

**Basis:** R02, X02, P03, P51 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Eligibility is an evidence decision

```text
ConstructionTreatmentWitness {
  actualSupplier, actualBuyer, serviceDescription,
  propertyOrWorkLocation, supportedServiceClass,
  buyerQualifyingActivityOrIntermediaryEvidence,
  contractualCompositeSupplyAssessment, effectiveDate,
  sourceTaxPresentation, selectedRuleRelease
}
```

Official guidance makes the nature of the supplied service and the purchaser's qualifying activity important [X02]. A company name, registration number, account code or industry-code label is not sufficient proof. Mixed material/service arrangements require a supported supply classification. Unsupported property, intermediary or incorrectly charged tax cases stay visible.

## Compile a valid qualified sale

```text
compileConstructionSale(witness, lines):
  require all mandatory conditions supported and reviewed at the relevant date
  require no incompatible supplier-charged VAT for this selected treatment
  net = exact supported consideration
  debit customer receivable net
  credit service revenue net
  publish sale tax basis with explicit reverse-charge role and required report mapping
  output VAT charged by seller =0
  freeze mandatory invoice wording, buyer identifiers and treatment evidence
```

Zero seller VAT is not absence of a tax fact. Preserve the taxable-activity basis and its separate report role. The invoice owner still allocates the legal number and records the issue once. A subsequent delivery through Peppol or PDF cannot change the approved treatment.

## Compile a valid qualified purchase

```text
compileConstructionPurchase(witness, source):
  require selected invoice has supported no-supplier-VAT presentation
  N = exact source consideration
  O = qualified self-assessed tax(N, taxPoint, rateRelease)
  D = qualified deductible portion of O
  debit construction expenseOrQualifiedAssetCost (N+O-D)
  debit reverse-charge input VAT D
  credit reverse-charge output VAT O
  credit supplier payable N
  publish separate basis, output and deductible components
```

The rule release supplies precise return-box identities and calculation order. They are not guessed from the ordinary domestic sales-rate mapping. The same component cannot later be admitted again as foreign-service reverse charge or domestic supplier-charged VAT.

The first profile refuses incorrectly charged supplier VAT rather than dropping it from the payable or automatically deducting it. A later supplier correction must preserve the original actual document and follow a qualified incorrect-invoice treatment. Such evidence is not converted to synthetic to pass admission.

## Credit, correction and application

A legal customer credit or supplier credit references original source-line coverage and the supported tax-period policy. It reverses the exact appropriate basis and tax components once. Partial credits release original qualified rounding residuals rather than independently changing rates. A buyer-status change after a posted transaction creates an impact/correction case, not a retroactive toggle that rewrites every invoice.

Use one capture/compiler per transaction direction and existing named application execution. Journal, invoice/payable, tax facts, exact source identities and receipt share the same transaction. Profile activation is a separate reviewed company/rule decision and cannot be performed by an invoice-issuing agent.

## Review and controls

The UI shows the ordinary-treatment alternative, the specific condition that selects reverse charge, evidence and exact financial differences. Only a selected qualified treatment can become executable; uncertainty is not resolved by always choosing the treatment with less tax due.

```text
synthetic N100000, output self-tax25000, deduction25000:
  buyer cost100000 + input25000 - output25000 - AP100000 =0
seller same N -> AR100000/revenue100000 and retained basis, no seller VAT line
half deduction -> buyer cost112500/input12500/output25000/AP100000
buyer evidence missing -> source retained, financial plan blocked
new key and other tax family for same recognized source -> duplicate refusal
```

This is a conditional specialist profile. No new VAT engine, journal owner or automatic company-wide reverse-charge flag is introduced.
