# NEXT-01: Owner-aware case review

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/cases/review-targets.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/cases/review-targets.ts` or the existing equivalent owner |
| Pure calculation | Typed ownership resolution and safe local route selection |
| Atomic scope | A read transaction captures the exact owner. It creates no journal or approval. |
| Prerequisites | None |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Implement in the existing case components and their current-owner lookup. Shared workspace composition stays root-owned. No change to financial approval powers. See C1–C10 in `00-COMMON.md`.

## Contract

```text
ReviewResolution =
    Standalone {changeSetId, planDigest, resolvedAt, ownershipVersion}
  | Correction {bundleId, bundleDigest, constituentId, role, resolvedAt}
  | OtherOwner {ownerKind, ownerId, safeInspectionRef}
  | Ambiguous {conflictingOwnerRefs}

resolveReviewTarget(access, scope, changeSetId):
    return withAdmittedPrincipal(access, scope, readPermission, (tx, principal) =>
        BookDb.lockForShare(tx, scope)
        plan = PlanDb.loadSameBook(tx, scope, changeSetId)
        owners = OwnershipDb.loadExactConstituentOwners(tx, scope, plan.id)
        # Both reversal and replacement membership, not just latest case metadata.
        if >1 incompatible owner: return Ambiguous(authorized safe references)
        if one correction:
            require exact scope, constituent and bundle digest relationship
            return Correction(bundle.id, bundle.digest, plan.id, exactRole)
        if one other owner: return OtherOwner(owned read target)
        return Standalone(plan.id, plan.digest, databaseTime, ownershipVersion)
    )
```

Use a current read operation when available. If the only current resolver is targeted case capture, invoke it as an explicit preparation mutation with its own idempotency key, then read the new snapshot. Never mislabel that fallback as a harmless GET. An unavailable resolver leaves inspection enabled and financial routing unavailable.

```text
CaseContextPanel.onReviewClicked(planId):
    set resolutionState = loading(planId)
    resolution = await resolveReviewTarget(book.scope, planId)
    discard response if selection or book changed while request was in flight
    match resolution:
      Standalone -> onReview({kind: 'standalone', id, planDigest})
      Correction -> onReview({kind: 'correction', bundleId, bundleDigest})
      OtherOwner -> display existing owned inspector; do not expose standalone execution
      Ambiguous -> show conflict; no financial button
    after actual destination mounts:
        focus destination's review heading

renderReview(target):
    switch target.kind:
      standalone: existing PostingRecoveryReview(target.id)
      correction: existing CorrectionBundleReview(target.bundleId)
    # Each review rechecks live owner/approval state. The resolution is not a capability token.
```

The latest-plan button resolves the latest plan. Each history-row button resolves its own plan. Do not apply the latest plan's owner to all alternatives. Ignore stored arbitrary URIs for navigation; select from a local route table. Query keys include entity, book and plan. Abort previous reads when selection changes.

A bundle created after resolution is still protected by the application execute-time aggregate-owner validation. Show the resulting owned-operation refusal and route through a fresh resolution rather than retrying the constituent.

## Design vectors

```text
historical snapshot has no optional owner + current reversal belongs to bundle B
    => open B, not standalone
history has standalone P1 and replacement P2 in B
    => P1 and P2 resolve independently
owner lookup unavailable
    => source/history inspection works, execution routing is blocked
book changes during lookup
    => discard stale response
```

Evidence baseline: original handoff S05/S06. Proposed resolver name is not an assertion that an endpoint already exists.
