# NEXT-07: Supplier paid credits and refunds

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/purchasing/credits-and-refunds.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/purchasing/refunds.ts` or the existing equivalent owner |
| Pure calculation | Shared line credit math plus payable/refund counterpart allocation |
| Atomic scope | Paid credit and refund receipt each have one complete owned tx. |
| Prerequisites | NEXT-03 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-03. NEXT-08 is conditional when an exported instruction still reserves the affected amount. Reuse original-line credit/tax capacity. No FX, advances or general netting in this first profile.

## State derived from immutable effects

```text
G = original gross obligation
K = effective cumulative credits
P = effective payments allocated under this bounded profile
Q = refunds already allocated to the linked refund receivable

require 0 <= K <= G
require 0 <= P <= G  # pre-existing overpayment profiles need their own admission
unpaid = max(G-K-P, 0)
refundPrincipal = max(P-(G-K), 0)
refundDue = refundPrincipal-Q
require 0 <= Q <= refundPrincipal
```

Do not store negative values in old nonnegative `outstandingMinor`. Add an explicit refund-receivable projection and preserve the older contract. The formula assumes effective payments/credits have not been reversed through an unsupported consumed-history path.

## Credit beyond unpaid capacity

```text
compilePaidSupplierCredit(original, history, creditDocument):
    creditLines = compile original-line net/source-tax/deduction releases from NEXT-03
    g = sum(creditLines.net + creditLines.sourceTax)
    require g <= remaining original-line gross capacity
    require no unresolved export reservation over affected payable
    before = derive(G,K,P,Q)
    apRelease = min(g, before.unpaid)
    newRefund = g-apRelease
    Journal.addSigned(payableControl, +apRelease)
    Journal.addSigned(supplierRefundReceivableControl, +newRefund)
    for line in creditLines:
        Journal.addSigned(originalExpenseRole, -(line.net + line.tax-line.deductible))
        Journal.addSigned(originalInputVatRole, -line.deductible)
    require before.refundPrincipal+newRefund == max(P-(G-(K+g)),0)
    return plan with credit tax facts, apRelease and refundPrincipalIncrease
```

The refund control is an explicit reviewed role, not an automatically inferred account or negative payable. A full paid credit is allowed only within the original line/tax limits and supported credit treatment.

```text
executePaidCredit(command):
    return withAdmittedPrincipal(access, scope, supplierCreditPermission, (tx, principal) =>
        lock book; replay exact command first
        load approved paid-credit plan and all original credit/payment/reservation capacities
        require current source-line basis, economic credit identity and exact approved digest
        RefundDomain.assertCreditConservation(plan, current)
        approval = validate exact current approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal)
        credit = PurchaseDb.insertCreditAndLineCapacityEffects(tx, plan, journal)
        refund = RefundDb.insertPrincipalIncrease(tx, plan, credit, journal)
        tax = TaxFactApp.recordAdjustmentsWithinTransaction(tx, plan.taxFacts, journal)
        bump owned credit/refund/control versions through tx
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journal.ids, credit, refund, tax}, approval)
    )
```

## Refund receipt

```text
prepareSupplierRefund(refundReceivable, source, allocations):
    require amount>0 AND sum(allocations)<=refundDue
    require source is evidenced same-currency cash receipt from supplier
    if source unposted:
        journal = debit bank(amount), credit supplierRefundReceivable(amount)
    else:
        require source references existing compatible posted refund-control credit
        require exact unused source capacity; journal=[]
    seal expected refund version + source capacity + exact allocation legs

executeRefund(command):
    return withAdmittedPrincipal(access, scope, refundPermission, (tx, principal) =>
        lock book; replay exact command first
        load approved refund plan and current cash-source/refund capacities
        validate scope, current source and every requested allocation
        approval = validate exact current approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal) if postNewCash else []
        refund = RefundDb.insertRefundAllocation(tx, plan, journalOrAdoptedComponents)
        SourceClaimDb.insertFinancialUsage(tx, plan.sourceBindings)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: ids(journal), refund}, approval)
    )
    # No expense reversal or additional VAT credit.
```

If a payment is reversed after a refund receivable or cash refund depends on it, the resulting formula could become negative. Reject the standalone reversal. An owned correction must restore the payment, credit and refund relationships together or give an explicit unsupported-consumed-history response.

Read views expose original invoice, credits, historical payments, current payable, refund principal and received refunds separately. Report cutoffs use accounting dates AND recorded cutoffs so later credits do not enter earlier saved statements.

## Vectors

```text
G125000 P100000 K0 Q0 => unpaid25000 refund0
credit50000 => AP debit25000 + refundAR debit25000 + original cost/tax credits50000
G125000 P100000 K50000 Q10000 => unpaid0 refundDue15000
another refund16000 => CapacityExceeded, no partial posting
new key for same credit-note identity => AlreadyApplied, not another refund entitlement
```

Evidence baseline: S07/S09. These equations are the chosen bounded design, not a universal receivables model.
