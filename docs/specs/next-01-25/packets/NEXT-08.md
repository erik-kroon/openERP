# NEXT-08: Payment instruction resolution and replacement

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/payments/resolutions.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/payments/resolutions.ts` or the existing equivalent owner |
| Pure calculation | Proof-qualified instruction release and successor eligibility |
| Atomic scope | Reservation release, dispatch fencing and receipt share a non-journal tx. |
| Prerequisites | None |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Extend existing supplier payment-batch/export ownership. An XML file is not a paid invoice. It can nevertheless be submitted later, so absence of local success is not no-execution proof.

## Records

```text
Instruction immutable {
  id, batchId, exportHash, endToEndId, beneficiaryRevision,
  originalAmount, currency, invoiceAllocationIntents, disclosedOrDownloaded
}
OutcomeObservation immutable {
  instructionId, sourceEvidence, sourceKind,
  authenticatedProviderIdentity?, externalStatus, observedAt, amountScope?
}
NoExecutionProof immutable {
  instructionId, exportHash, providerContractVersion,
  exactAmountProvenNotExecuted, evidenceRefs,
  finalityScope, permitsResubmissionOfOldIdentity: false | unknown
}
Resolution immutable {instructionId, proofDigest, releasedAmount, receipt}
Replacement immutable {newInstructionId, predecessorId, resolutionId, approvedNewDigest}
```

Keep both external outcome and local accounting status. A provider may prove execution before the corresponding bank accounting is posted. That amount stays reserved against duplicate instructions until the payment is accounted for or separately resolved.

## Proof evaluation

```text
evaluateNoExecution(instruction, observations, proposedEvidence):
    if proposedEvidence.kind == operatorReportedRejected:
        fail InsufficientExternalProof
    if proposedEvidence.kind == controlledNeverDispatched:
        require channel controlled exclusively by this system
        require no bytes exposed/downloaded/copied outside that controlled channel
        require dispatch fence proves no admitted/inflight provider request
        require immutable revocation preventing future dispatch
        return exact undispatched amount
    if proposedEvidence.kind == qualifiedProviderFinalCancellation:
        require retained authentic response identifies this exact instruction/export scope
        require provider contract establishes no execution for stated amount
        require known accepted/settled history reconciles with cancellation
        require old identity cannot later execute under that contract
        return exact finally cancelled amount
    fail OutcomeUnknown
```

An ordinary downloaded manual file cannot satisfy the controlled-never-dispatched branch. Do not manufacture that proof from HTTP access logs, user assertion or a timeout. Such cases remain reserved until an actually applicable external cancellation/no-execution resolution is available.

## Exact capacity and atomic release

```text
prepareResolution(instruction):
    availableReservation = originalAmount
                         - alreadyAccountedExecutedAmount
                         - effectiveNoExecutionReleases
    release = qualified proof amount not previously consumed
    require 0 < release <= availableReservation
    require proven executed-but-not-accounted amounts excluded from release
    capture outcomeInventoryVersion, reservationVersion, invoice capacities, proof digest
    seal review and approval requirement

executeResolution(command):
    return withAdmittedPrincipal(access, scope, resolutionPermission, (tx, principal) =>
        lock book; replay exact command first
        lock affected instruction/reservation and dispatch-intent rows in stable order
        load exact resolution plan and current outcome/proof inventory
        PaymentDomain.assertNoExecutionProof(plan, current)
        require no admitted or in-flight request can later execute the released amount
        require stale workers are fenced by domain dispatch/cancellation version
        approval = validate exact current resolution approval using C5
        resolution = PaymentDb.insertInstructionCapacityRelease(tx, plan)
        PaymentDb.invalidateSuccessorEligibility(tx, affected allocations)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: [], resolution}, approval)
    )
```

Release is not a cancellation journal or supplier credit. It frees instruction capacity only. Existing financial payment allocations remain unchanged.

## Replacement and late outcomes

```text
prepareReplacement(resolution, currentInvoices):
    require resolution effectively released exactly this capacity
    re-read live outstanding and other reservations
    revalidate beneficiary evidence/revision and independent verification
    assign NEW immutable instruction identity with predecessor relation
    compile file from current approved amounts, never edit old bytes
    fresh approval; export through existing owner

onLateOldExecution(observation):
    append raw observed evidence
    if conflicts with released capacity:
        create high-priority duplicate-execution case
        stop any not-yet-dispatched successor for this capacity
        if successor may already have executed: keep both outcomes unknown/observed precisely
        do not silently allocate two payments to one invoice
        reconcile real cash separately, using overpayment/recovery treatment only when supported
```

All release/dispatch/admission mutations use one instruction-reservation authority and lock discipline. A stale worker cannot dispatch after release by holding a cached approval. External reality can still disagree with a provider report; retain the conflict instead of rewriting history.

Vectors: unknown -> no release; reported rejection -> no release; final no-execution100 -> release100 once; invoice paid while review open -> stale; same-key replay -> same resolution; late old debit -> conflict, not silent success.

Evidence baseline: S09. Real proof must come from the chosen provider contract, not from this pseudocode.
