# NEXT-16: Evidence-aware period preparation

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/automation/period-work.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/automation/period-work.ts` or the existing equivalent owner |
| Pure calculation | Evidence-aware routing, rule selection and fixed approval manifest |
| Atomic scope | Public prepares/executes own their tx; separate run checkpoint recovery bridges calls. |
| Prerequisites | NEXT-01, NEXT-03, NEXT-06 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-01/03/06. Extend existing recurring run/checkpoint ownership. Keep automatic posting mandates out of this packet.

## Rules and manifest

```text
PreparationRule immutable {
  legalSupplierIdentity, supportedDocumentClass, currency,
  qualifiedTreatmentId, acceptedEvidenceRequirements,
  operationFamily, approvedExamples, negativeExamples,
  version, activationReview
}
PeriodWorkManifest immutable {
  scope, requestedInterval, cutoff, sourceCoverage,
  children: [{workIdentity, economicIdentity, sourceRevision,
             existingRecognitionRef?, existingMatchRefs, intendedOwner}],
  digest
}
WorkChild state {
  pending | waiting_predecessor | needs_review | prepared(planRef)
  | recovered(receiptRef) | committed(receiptRef) | refused(reason)
}
```

Frozen membership excludes later arrivals. A new manifest can select them explicitly. Do not copy a bank row into a new purchase identity when a matched invoice already establishes its recognition.

## Deterministic routing

```text
routeWork(child, currentEvidence, activeRules):
    identity = resolve reviewed economic relationships using preserved matches
    if committed purchase exists AND child is new bank/owner payment:
        return existing obligation's settlement owner
    if expense was paid by owner and not recognized:
        return OwnerPaidPurchase
    if new supported supplier invoice:
        return SupplierRecognition
    if source revises already recognized facts:
        return owned correction/credit review, not new recognition
    otherwise:
        return ReviewCase(exactMissingFacts)

selectRule(event):
    candidates = exact active conditions matching invoicing entity, class, currency and treatment
    require one unambiguous candidate and required evidence
    changed supplier entity, eligibility or source amounts -> needs_review
    # AI may propose missing facts/rules. It cannot supply confirmed facts or approval.
```

## Resumable preparation

```text
advanceManifest(runId, expectedFence, boundedCount):
    # Invoked by the effect-mq Bun handler, not a new queue implementation.
    for next pending child in fixed order:
        claim/check child business revision in a short application tx
        require current run cancellation/checkpoint version
        # Queue claims belong to effect-mq; child version fences domain result publication.
        re-read current source/recognition dependencies
        target = routeWork(...)
        if already posted: store recovered receipt, no new proposal
        if needs evidence/decision: store precise case; continue independent children
        if prerequisite child uncommitted: waiting_predecessor; continue independent children
        otherwise:
            key = stable key derived from run child and requested immutable revision
            plan = call existing domain PREPARE application operation with this key
                # No caller DB transaction is held while this public operation runs.
            in a new short run-owned application tx:
                replay checkpoint command
                recheck child revision and run cancellation version
                persist planRef + child checkpoint + receipt together
            # Crash between domain preparation and checkpoint is repaired by domain-key recovery.
```

No current agent tool approves on behalf of a human. Rule activation approves a treatment-selection rule, not every future journal.

## Fixed-manifest human approval

```text
prepareApprovalBatch(selectedPreparedChildren):
    require each child has an existing sealed plan and explicit owning operation
    require selected children independently executable or one existing atomic domain aggregate
    manifest = [(owner, planId, digest, inputIdentity) in deterministic order]
    show exact journals, source references and combined informational totals
    seal batch digest

approveBatch(command, humanAccess):
    return withAdmittedPrincipal(humanAccess, scope, batchApprovalPermission, (tx, principal) =>
        lock book; replay exact command first
        load exact sealed batch and batch member plans in a bounded set
        lock dependency/approval resources in the complete shared ordering
        for member:
            require exact digest, owner-specific approver rules and current basis
        approvals = for each member:
            owner.approveWithinTransaction(tx, principal, exact member plan)
            # Internal operation only. It never opens a new transaction or calls HTTP.
        persist batch-to-child-approval memberships and receipt through tx
        return exact batch result
    )
    # One human gesture approves exact members, not future arrivals or ordinary-agent powers.

executeApprovedBatch(batch):
    for member:
        dispatch ONLY to member's owning execution with stable captured request/key
        on response loss: recover same member; do not move to a new key
        on stale member: mark needs new review, keep other independent members runnable
        persist each receipt and honest partial progress
```

A child whose financial effects depend on an unknown predecessor result cannot be smuggled into the preapproved batch. Prepare it after the predecessor commits, then obtain the required new approval, unless an existing single aggregate explicitly owns both effects.

New narrow-dependency plans may avoid unrelated global-sequence staleness. Plans retained in the released replacement keep their exact approved dependency interpretation. Disposable old-schema fixtures do not require a fallback SQL workflow.

Counts distinguish prepared, committed, blocked and unresolved. A run with all children visited is not a reconciled period. That requires the separate source/control inventory.

UI focus is exceptions and exact approvals. Return compact structured context with source/case/plan references; let agents fetch evidence only for unresolved cases. Existing retained operations remain the recovery authority after reload.

Vectors: known recurring invoice -> same plan as manual purchasing; invoice already recognized + bank debit -> settlement; rule ambiguity -> review; crash after prepare -> recover same plan; stale one member -> other independent children continue; approval of batch never approves later added child.

Evidence baseline: S18/S05/S07.

The job's queue acknowledgment may be lost after the domain operation succeeds. Recover the prepared/committed child through the same domain command identity before changing progress. A cancellation after preparation keeps the prepared plan as retained evidence but prevents the stale handler from publishing new work or executing anything. Financial execution, when separately authorized, still goes through each owner's public execute service with its existing approval and economic receipt.
