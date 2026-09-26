# NEXT-06: Owner-paid expenses, reimbursement and funding

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/owners/operations.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/owners/operations.ts` or the existing equivalent owner |
| Pure calculation | Owner expense, existing-payable transfer, funding and reimbursement compilers |
| Atomic scope | Relevant journal, owner/commerce capacities and source usage commit together. |
| Prerequisites | NEXT-02, NEXT-03 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-02/03. Extend the existing owner register. Tax classification comes from the qualified purchase compiler, not from bank description or owner identity.

## Explicit modes

```text
OwnerOperation =
    NewOwnerPaidPurchase {purchaseSource, payerOwner, paidEvidence}
  | OwnerPaysExistingPayable {payableId, originalUnits, owner, paidEvidence}
  | ReimburseOwner {claimAllocations, cashSource}
  | OwnerLendsToCompany {lender, principal, bankEvidence, reviewedLoanTerms}
  | OwnerCapitalContribution {contributor, amount, reviewedLegalClassification, evidence}
```

Existing owner identities, effects and receipts remain authoritative. New modes do not reinterpret old synthetic data. A contribution does not acquire repayment rights because the UI calls it funding.

## New versus previously recognized purchase

```text
prepareOwnerPaidPurchase(input):
    recognition = find economic source recognition using preserved invoice/payment matches
    if none:
        require explicit evidence owner paid this company purchase
        compiled = compileDomesticPurchase(..., funding = ownerLiability(owner))
        bind same purchase economic key and tax identities as supplier-paid path
        return seal owner aggregate + new owner claim
    if recognition is supplier payable:
        return prepareOwnerPaymentOfPayable(recognition, input)
    if recognition already owner-paid:
        return AlreadyApplied(owner receipt)
    otherwise:
        return UnsupportedExistingRecognition with exact references

prepareOwnerPaymentOfPayable(payable, input):
    require current payable capacity >= amount and compatible same-currency profile
    require payment source not already consumed by a supplier/bank/owner settlement
    Journal.addSigned(supplierPayableControl, +amount)
    Journal.addSigned(ownerLiabilityControl, -amount)
    return plan {
      original invoice unchanged,
      supplier obligation consumption: amount,
      new owner claim: amount,
      new tax facts: []
    }
```

This transfer is not a second purchase. It creates no company-bank movement when the owner used a private account. An existing accounted owner payment can instead be adopted through an explicitly checked posted-control-line link, without duplicating the transfer.

## Reimbursement

```text
prepareReimbursement(owner, selectedClaims, cashSource):
    require all claims same owner, control role, currency and current version
    require claims have recognized owned effects, not merely a reviewed description
    require every requested leg >0 AND <= claim.remaining
    total = sum(legs)
    require total <= cashSource.unconsumedOwnerReimbursementCapacity
    if cashSource is unposted evidenced bank event:
        journal = debit owner liability(total), credit bank(total)
        action = post_and_allocate
    else if cashSource is existing compatible posted owner-control debit:
        action = adopt_existing_payment_and_allocate; journal = []
    else: fail UnsupportedSource
    seal complete legs, source identity and affected capacities

executeOwnerOperation(command):
    return withAdmittedPrincipal(access, scope, ownerOperationPermission, (tx, principal) =>
        lock book; replay exact command first
        plan = OwnerDb.loadExactPlan(tx, scope, command.planId)
        current = OwnerDb.loadSourcesClaimsAndCompatibleCapacities(tx, plan)
        OwnerDomain.assertCurrentCompleteOperation(plan, current)
        approval = validate exact current approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal) if nonempty else []
        if new purchase:
            TaxFactApp.recordRecognitionWithinTransaction(tx, plan.taxFacts, journal)
            RecognitionDb.insertOwnedIdentity(tx, plan.economicKey, journal)
        if payment of existing supplier payable:
            CommerceApp.applySettlementWithinTransaction(tx, plan.payableConsumption, journal)
        effects = OwnerDb.insertClaimSettlementAndAllocationEffects(tx, plan, journal)
        OwnerDb.bumpAffectedControlVersions(tx, plan)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: ids(journal), effects}, approval)
    )
```

For partial reimbursement, one payment may consume several claims. Every claim keeps its original source and prior allocations. A receipt replay restores neither capacity nor an old live view. It returns its original immutable result.

## Funding

```text
compileFunding(input, witness):
    require explicit classification supported by witness
    require observed company cash inflow or qualified existing posting adoption
    if loan:
        debit bank; credit shareholderLoanLiability
        create principal obligation; interest is separate and unsupported unless qualified
    if supported capital contribution:
        debit bank; credit reviewedEquityRole
        create contribution record, NOT a reimbursable owner claim
    if classification unknown or conditional rights unresolved:
        retain evidence/review only; no financial plan
```

Correct a consumed claim, liability transfer or reimbursement only through an owned aggregate reversal/replacement. If its downstream obligations cannot be restored together, refuse with an impact list. Do not create a new source key to bypass the refusal.

Controls use reviewed opening amounts plus owned current movements. A missing opening remains unknown. Company-bank reconciliation references the bank-side line independently of owner claim allocation; do not consume the same bank event twice by introducing a second matching authority.

## Vectors

```text
new owner-paid N10000 T2500 fully deductible:
    expense+10000, inputVAT+2500, ownerLiability-12500
reimburse5000:
    ownerLiability+5000, cash-5000; claim remaining7500; no new tax
already recognized AP12500 paid by owner:
    AP+12500, ownerLiability-12500; expense/tax delta0
capital contribution12500:
    bank+12500, qualified equity-12500; reimbursement capacity0
```

Evidence baseline: S12/S07.
