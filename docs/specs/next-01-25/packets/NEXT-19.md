# NEXT-19: Disposal with proceeds

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/subledgers/disposals.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/subledgers/disposals.ts` or the existing equivalent owner |
| Pure calculation | Proceeds, tax and post-impairment disposal conservation |
| Atomic scope | Disposal journal, asset/schedule retirement and proceeds usage share one tx. |
| Prerequisites | None |
| Reserved handoff | WIP-AST03-UI |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Wait for WIP-AST03-UI release, including its final impairment/control/disposal consumers. Qualified sale VAT and legal-invoice integration are conditional prerequisites. One asset and book currency initially.

## Snapshot and conservation

```text
basis = AssetDb.captureDispositionBasis(tx, scope, assetId, cutoff)
# Captured consistently before pure compilation, through the released WIP owner.
G = gross cost
A = imported ordinary accumulation + later effective ordinary recognition
I = effective impairment
B = G-A-I
require B>=0 and exact basis current
P = qualified net proceeds, not gross cash including VAT
V = separately qualified output VAT
profit = P-B
```

Proceeds must have a unique economic relationship to this disposal. The first profile rejects allocation of a single undivided invoice line to several assets unless an explicit allocation owner supplies conserved shares.

## Two supported acquisition-of-proceeds modes

```text
compileDisposal(basis, proceeds):
    if proceeds.kind == unposted_cash_sale:
        require observed unposted cash receipt P+V and qualified tax/sale evidence
        Journal.addSigned(cashRole, +(P+V))
        Journal.addSigned(outputVatRole, -V)
        append sale tax fact(base=P, output=V)
    else if proceeds.kind == existing_legal_invoice:
        require exact asset-sale invoice line, legal issue and unused proceeds capacity
        require line.net==P and line.tax==V
        require existing invoice accounting/tax remains valid
        if invoice used a dedicated asset-proceeds clearing role:
            Journal.addSigned(assetProceedsClearingRole, +P)
        else if qualified reclassification of ordinary sale revenue is explicitly supported:
            Journal.addSigned(originalSalesRevenueRole, +P)
            # Offsets existing revenueP, leaving only disposal profit below.
        else: fail UnsupportedProceedsAccounting
        new cash, receivable and VAT facts = NONE
    else: fail UnsupportedProceedsMode

    Journal.addSigned(ordinaryAccumulationRole, +A)
    Journal.addSigned(impairmentContraRole, +I)
    Journal.addSigned(grossAssetRole, -G)
    if profit>0: Journal.addSigned(disposalGainRole, -profit)
    if profit<0: Journal.addSigned(disposalLossRole, -profit)
    return {journal: finish(), removeCarrying:B,
            stopFutureOccurrences:true, usedProceedsIdentity, basisDigest}
```

The original standard sales invoice may have already recognized revenue. Posting full proceeds again would double revenue/cash. The explicit reclassification branch debits that original revenue exactly once and replaces its P&L effect with the disposal gain/loss. It does not reverse the invoice's genuine sales/VAT facts.

Issuing a new receivable invoice and disposing simultaneously needs a single coordinated owner aggregate. Do not approximate it by calling a public invoice-issue endpoint and then an independent disposal transaction. It is outside the two initial modes unless that owner is provided.

```text
executeDisposal(command):
    return withAdmittedPrincipal(access, scope, disposalPermission, (tx, principal) =>
        lock book; replay exact command first
        load plan and released impairment-aware asset basis
        require asset not disposed and no intervening installment, estimate or impairment
        load/recheck exact proceeds identity and unused accounting capacity
        DisposalDomain.assertApprovedConservation(plan, current)
        approval = validate exact disposal approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.journal)
        if unposted sale mode:
            TaxFactApp.recordRecognitionWithinTransaction(tx, plan.saleTaxFacts, journal)
        disposition = AssetApp.applyDispositionWithinTransaction(tx, plan, journal)
        ProceedsDb.insertOwnedUse(tx, plan.proceedsIdentity, disposition)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: journal.ids, disposition}, approval)
    )
```

The WIP asset owner remains responsible for impairment-aware ordinary recognition, controls and disposal reads. This packet adds proceeds behavior only after its handoff.

## Correction and presentation

Latest-unconsumed error correction must reverse the entire financial effect, restore valid asset/schedule state and release proceeds rights together. If a legal credit, later asset action, closed-period consumer or cash refund depends on it, refuse until a complete supported chain exists. A generic journal reversal must not resurrect the asset register alone.

Show original cost, ordinary accumulation, impairment, carrying, net/gross proceeds, VAT and gain/loss. After disposal the gross and contra controls attributable to the asset all clear, not just the carrying subtotal.

## Vectors

```text
G1000000 A300000 I100000 => B600000
P650000 V162500 unposted sale:
    cash+812500, ordinary+300000, impairment+100000,
    gross-1000000, VAT-162500, gain-50000
P550000 with already invoiced proceeds:
    originalRevenueOrClearing+550000, ordinary+300000, impairment+100000,
    loss+50000, gross-1000000
    no second AR/cash/VAT recognition
```

Actual VAT rate/eligibility is a qualified input. The example's1/4 is illustrative, not an automatic rule for every asset sale.
