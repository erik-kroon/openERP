# NEXT-10: Provider revisions to reviewed bank observations

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/banking/source-admission.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/banking/source-admission.ts` or the existing equivalent owner |
| Pure calculation | Exact provider revision mapping and same/different economic-event decisions |
| Atomic scope | Source admission and provenance commit together; no automatic posting or matching. |
| Prerequisites | NEXT-09 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-09. Interpret only published generations. Raw provider delivery is not already a statement, a reviewed bank observation or accounting.

## Source and admission model

```text
ProviderIdentity := (book, provider, stream, providerTransactionId)
Revision immutable {
  identity, publicationVersion, changeKind, rawLocator, rawDigest,
  providerPendingReference?, normalizedFacts, parserVersion
}
ObservationHead {identity, latestRevision, eligibilityVersion}
BankAdmission immutable {
  sourceRevision, economicObservationId, reviewDigest, existingBankObservationId
}
OverlapDecision immutable {
  evidenceBasedRelation: same_event | different_events,
  identities[], reviewer, originalEvidence
}
```

The revision order is the ordered published update stream, not a guessed timestamp or hash ordering. For conflicting changes to one ID within a window, use only the provider's documented application order. If it does not resolve the ambiguity, keep raw facts and block normalization for that identity.

## Exact interpretation

```text
interpretPlaidChange(change, rawPage, streamProfile):
    require published generation, account matches exact configured account filter
    require known change kind and supported account/currency profile
    if removed:
        return Removed(providerId, rawLocator)  # Do not require an amount absent in removal schema.
    x = parse raw JSON amount lexeme as rational decimal, not JS Number
    scale = qualified currency metadata; reject unknown unofficial currency
    providerMinor = exactConvertToMinor(x, scale)  # fractional minor units refuse
    cashMovementMinor = -providerMinor
        # Transactions API positive means money leaving the account [X03].
        # Initial admission profile is a supported deposit/cash account, not arbitrary investment data.
    dates = retain provider date, authorization date and datetime independently
    postingDateCandidate = explicit profile's reviewed booking-date mapping
    return Revision(..., amount=cashMovementMinor, dates,
                    pending=provider.pending, pendingRef=provider.pending_transaction_id)
```

Descriptions and counterparty enrichment are source assertions. They do not establish accounting purpose, account ownership or VAT.

## Material changes

```text
applyPublishedRevision(revision):
    inside withAdmittedPrincipal(..., (tx, principal) => ...) with the book lock:
        recover same source revision if already retained
        old = current head for exact provider identity
        append revision; advance head/version
        if pending:
            retain as nonfinancial pending observation
            no final bank admission or accounting preparation
        else if provider explicitly links a pending predecessor:
            link pending lineage; preserve predecessor bytes
            require predecessor cannot already be a separately accepted final economic observation
            otherwise raise overlap case, do not silently combine financial capacities
        if old admitted or matched:
            if amount/currency/booking-date/removal materially changes meaning:
                append source-change impact case with old admission/match/voucher refs
                mark current matching/coverage eligibility stale
                preserve old bank observations, matches and vouchers
            else retain nonfinancial metadata change without rewriting old snapshots
```

## Reviewed admission and file overlap

```text
prepareBankAdmission(revision, overlapDecision?):
    require terminal supported observation, current revision, no unresolved material conflict
    if an evidenced CSV/feed same-event relation exists:
        adopt existing economic observation with additional provenance
        require amount/currency/date semantics reconcile under explicit decision
        do not create a second observation or cash capacity
    else if unresolved lookalike exists:
        show candidates and require same/different decision; do not deduplicate automatically
    else:
        prepare exact ordinary bank observation through existing intake owner

executeBankAdmission(command):
    return withAdmittedPrincipal(access, scope, bankAdmissionPermission, (tx, principal) =>
        lock book; replay exact command first
        load plan, source revision, publication and overlap-decision dependencies
        BankSourceDomain.assertCurrentReviewedAdmission(plan, current)
        approval = validate required source-review authority using C5
        if plan adopts existing economic observation:
            observation = existing exact same-book observation
        else:
            observation = BankIntakeApp.admitWithinTransaction(tx, plan.normalizedObservation)
        BankSourceDb.insertAdmissionAndProvenance(tx, plan, observation)
        BankSourceDb.bumpAffectedMembership(tx, plan)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: [], observation}, approval)
    )
    # No journal or bank match is created by ingestion.
```

A provider feed page contains no guaranteed independent opening/closing balance. Require real statement/coverage evidence for reconciliation signoff. A removed transaction that had already been booked becomes an investigation/correction workflow, never an automatic deletion or reversal.

UI distinguishes pending, source-reviewed, admitted, matched and accounting-complete. An outdated match stays visible with its original basis and a material-source-change warning.

Vectors: repeated source revision -> one observation; two identical legitimate IDs -> two; pending predecessor + evidenced posted successor -> one final observation; changed matched amount -> impact case; removed matched observation -> no automatic ledger delta.

Evidence baseline: S10/S11; external sign/schema behavior [X03].
