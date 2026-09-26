# NEXT-02: Capability-specific company admission

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/company/profiles.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/company/profiles.ts` or the existing equivalent owner |
| Pure calculation | Effective-date profile selection and overlap validation |
| Atomic scope | Activation, affected membership versions and receipt commit together without a journal. |
| Prerequisites | None |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Extend company setup and existing legal-policy records. Do not change the book's historical synthetic meaning or redesign authentication. Shared records follow C2–C5.

## Records and keys

```text
FactRevision immutable {
  id, entityId, factKind, effectiveInterval, recordedAt,
  value | Unknown | NotApplicable(reason), evidenceRefs, supersedes?
}
FactReview immutable {factRevisionId, digest, reviewer, result, reviewedAt}
RuleRelease immutable {
  id, jurisdiction, family, version, checksum,
  applicabilityPredicate, requiredFactKinds, requiredRoleKinds,
  calculatorVersion, roundingRules, validInterval, sourceManifest,
  qualificationStatus
}
RoleBinding immutable {
  bookId, roleKind, accountId, accountRevision, effectiveInterval,
  evidence, reviewer, supersedes?
}
Activation immutable {
  bookId, family, ruleReleaseId, selectedFactReviews, roleBindings,
  applicabilityScope, effectiveInterval, approvedDigest
}
# Revocation/supersession append records; no editing activated bytes.
```

A `RuleRelease` contains executable code/data already reviewed for that family. It is not a user-supplied prompt or arbitrary code. A book activation selects an existing supported release, not permission to invent a treatment.

## Resolve by the operation's dates

```text
resolveProfile(captured, family, dates, eventFacts):
    needed = requiredFactsForFamily(family)
    facts = {}
    for kind in needed:
        selectorDate = dateBasisFor(family, kind, dates)
        matches = effective reviewed revisions(kind, selectorDate, captured.recordedCutoff)
        require exactly one usable match else MissingFact/AmbiguousFact
        facts[kind] = matches.only
    candidates = active releases and book activations with:
        matching family, jurisdiction, date interval and explicit applicability predicate
    require exactly one candidate
    require candidate qualification supports this case and record class
    roles = resolve explicit reviewed account roles at relevant posting date
    require each role exists, is active for new posting and belongs to book
    return ProfileWitness {
      factRevisionIds, factReviewIds, roleBindingIds,
      ruleReleaseChecksum, activationId, dates,
      dependencies for precisely these selections
    }
```

Date selection is family-specific: posting eligibility uses posting date, VAT uses its qualified tax point/method, payroll uses payment/reporting dates and statements use the fiscal-year framework applicability. An annual rule version is not selected merely by today's date.

## Activation transition

```text
prepareActivation(request):
    capture referenced facts/reviews, rule release, roles and prior activations
    require rule code and schema support exist
    require no contradictory evidence or overlapping ambiguous activation
    return seal exact activation proposal + capabilities it would enable

executeActivation(command):
    return withAdmittedPrincipal(access, scope, operatorPermission, (tx, principal) =>
        BookDb.lockWriter(tx, scope)
        if prior = CommandDb.replay(tx, principal, command): return prior
        plan = ProfileDb.loadActivationPlan(tx, scope, command.planId)
        current = ProfileDb.loadSelectionAndOverlaps(tx, scope, plan)
        ProfileDomain.assertSameFactsRolesReleaseAndScope(plan, current)
        require no contradictory evidence or ambiguous overlapping activation
        approval = ApprovalApp.validateWithinTransaction(tx, principal, plan, command)
        activation = ProfileDb.insertActivation(tx, plan, approval)
        ProfileDb.bumpAffectedFamilyMembership(tx, plan.applicabilityScope)
        CaseDb.insertImpacts(tx, affected unexecuted proposals)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {activation, journalIds: []}, approval)
    )
```

Prior fact selections in committed records remain historical. A retroactive fact correction creates impact cases for already posted work and does not rewrite the old computation. A future-only change need not invalidate a past event's profile witness.

## Integration

```text
canPrepare(family, event) = resolveProfile(...) succeeds
canReportComplete(period) = all applicable families have complete qualified controls
canFile(artifact) = canReportComplete AND format/signature/provider requirements met
```

Never collapse these into `company.productionReady = true`. Let evidence capture run when accounting facts are incomplete. Extend the current legal-AR activation owner rather than making a second authority for the same operation. The clean replacement does not need an old-database adapter. Any meaningful retained activation keeps its original scope and evidence.

UI returns structured missing facts with affected operations. Unknown is not `false`, empty text or zero. Actual company activation needs actual reviewed records; synthetic fixtures are usable only in their explicit class.

Evidence baseline: handoff S02/S03/S17. Framework release selection must follow official applicability guidance [X04 in SOURCES.md].
