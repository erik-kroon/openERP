# NEXT-12: Historical open-item adoption

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/imports/historical-items.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/imports/historical-items.ts` or the existing equivalent owner |
| Pure calculation | Historical residual and existing-control-pool conservation |
| Atomic scope | Live obligation adoption and pool assignment commit without new recognition. |
| Prerequisites | NEXT-02 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-02. Financial basis already belongs to the historical import/OpeningSet owner. Adoption adds live settlement identity, not another journal.

## Data model

```text
ControlPool immutable {
  id, book, historicalBasisId, cutoverDate, direction: AR|AP,
  currency, scale, controlAccount, exactReviewedResidual,
  supportingGLBasisRefs, independentSourceControlDigest
}
HistoricalAdoption immutable {
  sourceItemIdentity UNIQUE per book/source system,
  historicalBasisId, controlPoolId, residualAtCutover,
  originalFaceAmount: Known(amount)|Unknown,
  priorPayments: EvidencedReferences|Unknown,
  sourceIssueDate: Known(date)|Unknown,
  liveObligationId, receiptId
}
PoolAssignment immutable {controlPoolId, adoptionId, amount}
```

The pool is a partition of an existing reviewed GL basis. It is not a new ledger balance. Construct separate AR/AP and debit/credit-direction pools where needed; do not use one net account balance to hide offsetting supplier/customer credit positions.

## Adoption

```text
prepareAdoption(sourceItem, pool):
    require source item is from the selected reviewed historical inventory
    require exactly one selected financial basis: full_history XOR opening_set
    require pool's GL identity and independent source total verified
    require item currency/direction/control account match pool
    residual = exact evidenced outstanding at cutover
    require residual >0; zero items remain historical evidence without live capacity
    require item not already adopted or represented by an existing native obligation
    used = sum(effective pool assignments)
    require residual <= pool.exactReviewedResidual-used
    require source item belongs to complete reviewed control partition
    seal adoption with pool/version/source digests and unknown-history fields intact

executeAdoption(command):
    return withAdmittedPrincipal(access, scope, historicalAdoptionPermission, (tx, principal) =>
        lock book; replay exact command first
        load adoption plan, reviewed source item, control pool and effective assignments
        require source/basis versions current and no duplicate native obligation
        HistoricalDomain.assertConservedPoolAssignment(plan, current)
        approval = validate exact adoption approval using C5
        obligation = CommerceApp.adoptHistoricalItemWithinTransaction(tx, {
            openingResidual: plan.residual,
            sourceHistory: immutable source references,
            kind: historical_open_item_v1
        })
        adoption = HistoricalDb.insertAdoptionAndPoolAssignment(tx, plan, obligation)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: [], obligation, adoption}, approval)
    )
    # No new recognition journal and no financial ledger sequence increment.
```

If native full-history import already established the same live obligation, adopt provenance onto that identity rather than create another. A per-line recognition amount100000 is not automatically a40000 residual pool after60000 historical payments; prove the complete net basis first.

## Later lifecycle

```text
historicalObligationRemaining(item, cutoff):
    return openingResidual
           - effective NEW settlements through cutoff
           - supported NEW credit reductions through cutoff
           + supported owned correction effects
    # Do not subtract historical payments again.

settleAdoptedItem(item, newPayment):
    use current commerce settlement owner with historical_open_item adapter
    conserve new payment and residual capacities
    create only payment accounting if cash is not already posted
    preserve source original amount/history as metadata, not current capacity
```

A credit requiring original line-level tax amounts cannot be compiled from residual alone. Missing detail is a specific unsupported-credit blocker; it does not prevent a separately supported payment settlement.

## Controls

```text
adoptedTotal + explicitlyUnadoptedResidual == independentlyReviewedPoolTotal
liveResidual + postCutoverSettlements + supportedCredits == adopted opening residual
```

Any unexplained control difference blocks complete-register readiness. Partial adoption is allowed with a named unadopted bucket, not labeled full migration. Avoid universal line exclusivity; enforce conflict only when the same financial basis would supply duplicate AR/AP capacity.

Vectors: original100000, evidenced prior settled60000, residual40000 -> live40000 and GL delta0; new payment10000 -> remaining30000; missing original face but evidenced residual -> payment may be supported, credit may not; duplicate adoption -> same-key replay or AlreadyApplied.

Evidence baseline: S13.
