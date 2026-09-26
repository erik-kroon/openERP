# NEXT-03: Domestic purchasing with owned tax recognition

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/purchasing/recognition.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/purchasing/recognition.ts` or the existing equivalent owner |
| Pure calculation | Domestic purchase and original-line credit compilers |
| Atomic scope | Journal, payable, source recognition, tax facts and receipt share one tx. |
| Prerequisites | NEXT-02 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-02. Extend supplier acceptance and credit owners, not their WIP VAT settlement/amendment consumers. Start with qualified same-currency SEK accrual cases.

## Immutable recognition result

```text
PurchaseRecognition {
  economicKey, supplierInvoiceRevision, profileWitness,
  lines: [{sourceLineId, net, sourceTax, deductibleTax, nonDeductibleTax,
           expenseRole, taxPoint, recognitionDate, taxComponentId}],
  payableId, voucherId, taxFacts[], receiptId
}
TaxFact {
  identity: (recognitionId, sourceLineId, componentRole),
  signedBase, signedOutputTax, signedDeductibleTax,
  sourceTax, treatment, taxPoint, reportingObligation,
  journalComponentRefs, sourceRefs, ruleRelease, adjustsTaxFactId?
}
UNIQUE recognized purchase economicKey
UNIQUE taxFact(recognitionId, sourceLineId, componentRole)
```

A valid invoice may have zero tax. That requires a supported zero/exempt treatment, not classification as deductible 25% VAT with the amount changed to zero.

## Pure calculation

```text
compileDomesticPurchase(basis, reviewedLines, funding = supplierPayable):
    witness = resolveProfile(basis, domesticPurchase, dates, sourceFacts)
    require complete source-line selection and invoice gross reconciliation
    for line in sourceLines in original order:
        N = exact source net; T = exact asserted source VAT; G = exact source gross
        require N >= 0 AND T >= 0 AND G == N+T
        treatment = witness.classify(line)  # explicit supported table, no brand inference
        expected = roundRational(N*treatment.rate.n, treatment.rate.d,
                                 treatment.invoiceTaxRounding)
        checkSourceTaxDifference(T, expected, treatment.acceptancePolicy)
            # exact-match, qualified tolerance + retained discrepancy, or review-required
        D = roundRational(T*deductionFraction.n, deductionFraction.d,
                          treatment.deductionRounding)
        require 0 <= D <= T
        E = N + T-D
        Journal.addSigned(line.expenseRole, E, sourceLine=line.id)
        Journal.addSigned(inputVatRole, D, taxComponent=line.id)
        taxFacts += signed purchase component(base=N, deductibleTax=D,
                                              sourceTax=T, nonDeductible=T-D)
    totalGross = sum(N+T)
    require totalGross > 0
    Journal.addSigned(funding.controlRole, -totalGross)
    return {journal: finish(), payable: totalGross, lines, taxFacts, witness}
```

A tax fact with zero deductible amount may still carry a required basis/exclusion. Do not manufacture a zero tax journal line. Preserve raw source amounts and the qualified discrepancy result separately. Any material source mismatch creates a review case rather than silently rewriting the invoice to match the calculator.

## Atomic posting

```text
executePurchase(command):
    return withAdmittedPrincipal(access, scope, purchasePermission, (tx, principal) =>
        BookDb.lockWriter(tx, scope)
        if prior = CommandDb.replay(tx, principal, command): return prior
        plan = PurchaseDb.loadExactPlan(tx, scope, command.planId)
        current = PurchaseDb.loadSourcesCapacitiesAndRoleClaims(tx, plan)
        require source revision/profile current and no recognized economic duplicate
        require no conflicting reservation or economic role
        PurchaseDomain.validateStoredAggregate(plan, current)
        approval = ApprovalApp.validateWithinTransaction(tx, principal, plan, command)
        journal = JournalApp.postWithinTransaction(tx, plan.journal)
        payable = PurchaseDb.insertPayableAndLineCapacities(tx, plan, journal)
        taxFacts = TaxFactApp.recordRecognitionWithinTransaction(tx, plan.taxFacts, journal)
        RecognitionDb.insertOwnedIdentity(tx, plan.economicKey, journal, payable, taxFacts)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journal.ids, payable, taxFacts}, approval)
    )
```

Generic manual entry, expense-review and independent tax-fact admission must reject a second recognition of those same economic components. A second evidence document about the purchase is still retainable. Adoption of an already posted purchase is a separate reviewed no-reposting operation, not an extra recognition.

## Partial credit compiler

```text
compilePurchaseCreditLines(original, previousCredits, sourceCredit):
    for selected original line:
        require credit net/tax supported by original treatment and distinct credit evidence
        require cumulative credited net <= original net
        require cumulative credited source tax <= original source tax
        require previouslyReleasedDeduction matches this versioned cumulative policy
            else require an explicit retained-credit basis decision; never conceal a residual
        d = cumulativeRelease(original.deductibleTax, original.sourceTax,
                              priorCreditedTax, newCreditedTax, deductionReleasePolicy)
        e = creditNet + creditTax-d
        Journal.addSigned(original.expenseRole, -e)
        Journal.addSigned(original.inputVatRole, -d)
        append negative TaxFact adjusting original component, with qualified credit taxPoint
    return exact line releases, signed tax adjustments and remaining line capacities
        # No payable/refund counterpart selected in this reusable line compiler.

compileUnpaidPurchaseCredit(original, previousCredits, sourceCredit, current):
    lines = compilePurchaseCreditLines(original, previousCredits, sourceCredit)
    g = sum(lines.creditNet + lines.creditTax)
    require g <= current.unpaidResidual
    journal = lines.expenseAndTaxReversals + debit(payableRole, g)
    return balanced journal, lines.taxAdjustments and updated credit capacities

executeUnpaidPurchaseCredit(command):
    withAdmittedPrincipal(access, scope, creditPermission, (tx, principal) =>
        lock book; replay exact command first
        load sealed credit and current original-line/payment/reservation basis in batches
        validate capacities, qualified tax policy and exact approved effects
        approval = validate current exact credit approval using C5
        journal = JournalApp.postWithinTransaction(tx, approved journal)
        credit = PurchaseDb.insertCreditAndCapacityEffects(tx, plan, journal)
        tax = TaxFactApp.recordAdjustmentsWithinTransaction(tx, plan.taxAdjustments, journal)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journal.ids, credit, tax}, approval)
    )
```

NEXT-07 handles the amount exceeding unpaid principal. It consumes the same credit compiler and capacities rather than duplicating them. A final credit releases exactly the remaining original deduction, not independently rounded fragments with leftover tax.

Payment execution consumes the payable and bank/owner consideration. It calls no purchase-recognition or VAT publisher. Corrections use signed adjusting facts; do not both remove the original tax fact and subtract it again.

## Vectors

```text
N=10000 T=2500 deduction=1 => expense10000 / input2500 / payable12500
same purchase paid later => zero new purchase-tax facts
N=10000 T=2500 deduction=1/2 => expense11250 / input1250 / payable12500
N=101 T=25 G=126 with explicitly allowed half-up => retain126, not126.25
credit N=4000 T=1000 full deduction => AP debit5000 / expense credit4000 / input credit1000
```

New rates/tolerance/deduction releases must be qualified. This pseudocode does not certify every merchant's VAT treatment. Evidence baseline: S07/S08.
