# NEXT-56: Customer advances, deposits and final-invoice application

Priority: **P1 when applicable**. Lane: **COMMERCE**.

**New deliverable:** Handle money received before a supply with its own tax and liability timing. NEXT-30 deliberately distinguishes refundable excess cash from a taxable advance and does not implement that advance.

**Existing owner to extend:** Existing customer-credit, invoice recognition, bank-source and tax-fact owners.

**Required contracts:** NEXT-02, NEXT-04, NEXT-30, NEXT-51. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** Advance concepts in ERPNext review; canonical family COM-02/03/04, VAT. Customer advance tax timing differs from NEXT-30 refundable overpayments.

**Atomic result:** Cash/clearing + advance liability/tax + final AR application.

**Evidence:** R03, R04, X05 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Distinct economic classes

Retain an `AdvanceAgreementDecision` with identified supply, contract, tax classification, payer and application/refund terms. `RefundableSecurityDeposit`, `TaxableSupplyAdvance` and `UnappliedOverpayment` are separate cases. Do not classify them by the bank description. A pro-forma/advance request is not a final sale and does not automatically create revenue or VAT.

`AdvanceReceipt` retains gross principal, net liability carrying, source VAT, tax already reported, cash identity and exact remaining component capacities. It references existing cash and customer liability owners rather than introducing a second cash ledger.

## Receipt and final application

For the qualified taxable advance profile, actual receipt of `G=N+T` posts debit bank `G`, credit customer-advance liability `N` and credit output VAT `T`. The advance VAT timing must follow the selected applicable rule; payment is material under the official advance guidance [X05]. A security deposit profile retains gross liability without VAT until a separately supported tax event occurs.

```text
prepareAdvanceReceipt(source,agreement):
    require actual cash or compatible already-posted clearing source
    classify under reviewed contract and tax release
    derive retained N,T,G under explicit exclusive/inclusive basis
    prove cash event unused for this financial component
    seal journal + liability + tax facts + source relation

compileFinalSupply(invoice,advanceApplications):
    derive original final supply totals NF,TF,GF once
    for each application:
        release exact remaining advance net NA and previously reported tax TA
        require same supported supply/treatment relationship and gross GA=NA+TA
    remainingAR=GF-sum(GA)
    require remainingAR>=0
    debit AR remainingAR
    debit advance liability sum(NA)
    credit earnedRevenue_or_deferredRevenue NF
    credit additional output VAT TF-sum(TA)
```

Tax differences across rate/date changes need a qualified adjustment rule; the first profile can refuse them rather than use the subtraction above without justification. Partial deliveries release original components cumulatively with recorded coverage. The final invoice presents full supply totals, applied advances and amount due, while reporting facts explicitly distinguish prior tax from the newly recognized delta.

## Execution and refund

Issue/application is one transaction with invoice identity, journal, advance capacity use, AR and tax facts. Advancing a deposit does not reserve or consume stock/order quantities outside their own existing owner. An invoice already issued for the full amount needs a reviewed application/reclassification variant, not another issue journal.

An approved refund of unused taxable advance posts debit advance liability `N`, debit qualified output-tax reversal `T` and credit actual bank/refund clearing `G`, with its own source event and correction facts. Refunding already applied value must use the final invoice/credit owner. An unknown external refund outcome keeps its payment reservation and cannot trigger another refund.

Cash forecasts include future unused refunds or final receivables through the native payment identities. They do not include the original advance receipt again after it is already in opening cash.

## UI and completed journey

Show requested versus received, taxable versus security deposit, gross remaining, net liability, tax previously declared, applications and actual refunds. Separate commercial status from paid status. Preparation may be agent-assisted; tax activation, approval and external payments remain appropriately authorized.

Synthetic receipt12500 produces liability10000 and tax2500. Final supply37500, comprising30000+7500, consumes the advance and leaves AR25000: debit AR25000 plus liability10000, credit revenue30000 plus additional tax5000. Lifetime tax remains7500, not10000.

Complete with two partial applications, a final application, an unused balance refund, duplicate cash observation and a changed treatment between prepare/execute. Amounts and tax facts must reconcile to original advance capacities and the final invoice without manual SQL repair.
