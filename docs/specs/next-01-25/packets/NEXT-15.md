# NEXT-15: Legal customer credit notes

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/sales/credit-notes.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/sales/credit-notes.ts` or the existing equivalent owner |
| Pure calculation | Qualified legal credit, source-line limits and tax corrections |
| Atomic scope | Number, journal, AR reduction, tax facts, semantic document and outbox share one tx. |
| Prerequisites | NEXT-02 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-02; actual return integration follows NEXT-04. Preserve WIP webshop/order/catalog ownership. Reuse current legal-issue policy and native accounting boundary, never synthetic cancellation.

## Credit record

```text
CustomerCreditPlan {
  originalLegalIssueId, originalDocumentHash,
  sourceCreditDecisionIdentity, reason, creditDate, datePolicy,
  selectedLines: [{originalLineId, creditedNet, creditedTax,
                  priorCreditedNet, priorCreditedTax}],
  currentUnpaidCapacity, legalPolicyWitness, taxCorrectionWitness,
  semanticCreditDocument, expectedInvoiceVersion
}
UNIQUE(book, sourceCreditDecisionIdentity)
UNIQUE(book, creditSeries, creditNumber)
```

Credit-note numbering belongs to the reviewed issue policy. Allocate it during the atomic issue transaction. Never fetch today's catalog price or re-open converted-order quantity just because a credit is issued.

## Compiler

```text
compileCustomerCredit(original, capacity, input, profile):
    require original belongs to existing supported legal domestic sale family
    require each original source line appears at most once in request
    for credit line:
        require n>=0, t>=0 and n+t>0
        require n <= original.net-priorCreditedNet
        require t <= original.tax-priorCreditedTax
        require credit evidence and qualified original-rate/rounding contract hold
        # Full final line credit uses its exact remaining original tax.
        Journal.addSigned(original.revenueRole, +n)
        Journal.addSigned(original.outputVatRole, +t)
        append tax correction with base=-n, outputTax=-t,
               adjusts=original recognition component and qualified tax period
    g = sum(n+t)
    require g <= current unpaid balance
    Journal.addSigned(original.receivableRole, -g)
    finish()
    freeze legal document fields, original references and reason
```

The bounded path rejects paid-principal excess. It does not secretly create a customer credit balance or cash refund. Foreign tax, mixed treatments or unsupported credit chronology receive specific profile failures.

## Atomic issue plus asynchronous rendering

```text
executeLegalCredit(command):
    return withAdmittedPrincipal(access, scope, legalCreditPermission, (tx, principal) =>
        lock book; replay exact command first
        load exact plan and current original issue/line/payment/tax-policy basis
        require issue-date boundary still valid, including required day-rollover refusal
        CreditDomain.assertLineCapacityAndUnpaidConservation(plan, current)
        approval = validate exact legal-credit approval using C5
        creditNumber = CounterDb.allocateRollbackSafeNumber(tx, plan.legalSeries)
        journal = JournalApp.postWithinTransaction(tx, plan.journal)
        credit = SalesDb.insertCreditAndReceivableEffects(tx, plan, creditNumber, journal)
        tax = TaxFactApp.recordAdjustmentsWithinTransaction(tx, plan.taxFacts, journal)
        document = SalesDb.insertImmutableCreditSemanticRevision(tx, plan, creditNumber)
        OutboxDb.insert(tx, render intent referencing document and renderer version)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journal.ids, credit, tax, document}, approval)
    )
    # Bytes are rendered afterward by the Bun job handler. Issuance does not repeat.
```

If rendering fails, the legal credit and journal still exist and recover by their receipt. Rendering resumes from the retained semantic revision. It never issues another number or recalculates tax from newer customer details. The UI distinguishes issued-but-artifact-pending from not issued.

Reflect credit effects in ageing, statements, collection eligibility and reminder dispatch rechecks. Existing invoice bytes and prior payments remain unchanged. Dispatch of a reminder sees current unpaid/dispute status rather than the old statement's historical outstanding amount.

For existing legal invoices without owned tax-fact publication, require an explicit original-recognition adoption through NEXT-04 before producing tax corrections. Do not fabricate an original fact, and do not call a partial bookkeeping-only path complete statutory credit support.

Vectors: original10000+2500, credit4000+1000 -> remaining7500 before payments; second credit beyond remaining source tax -> refusal; day rollover -> no numbering/posting; duplicate key -> same receipt; new key same economic credit -> AlreadyApplied; credit does not restore order-to-invoice conversion capacity.

Evidence baseline: S17/S07/S03.
