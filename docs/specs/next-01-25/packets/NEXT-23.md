# NEXT-23: Financial close and single-count carry-forward

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/closing/financial-years.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/closing/financial-years.ts` or the existing equivalent owner |
| Pure calculation | Current close controls, result-transfer delta and single-count opening |
| Atomic scope | Transfer, financial certificate, next opening, locks and receipt share one tx. |
| Prerequisites | NEXT-13, NEXT-22 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-13/22 plus the actually applicable accounting families. Root composes shared control/closing changes after reserved owners release their contracts. Do not require unrelated payroll or webshop features for every company.

## State and stages

```text
FinancialYearStatus = open | preparing | adjustments_pending | ready_for_finalization | closed
Technical period locks remain separate.
ClosePreparation immutable {baseline, applicableFamilies, proposedAdjustmentRefs, openCases}
FinalCloseProposal immutable {
  year, actualAfterAdjustmentBasis, taxBridgeAndReceipt,
  exactCurrentControlManifests, resultTransferPlan,
  nextOpeningSemanticTarget, digest
}
FinancialCloseCertificate immutable {proposalDigest, receipt, closingBasis, openingSetId}
OpeningSet immutable {
  year, version, previousCertificateOrMigrationBasis,
  rawBSBalances, sourceBoundary, priorOpeningVersion?, digest
}
ReopenEvent immutable {certificateId, reason, authorizedImpactManifest}
```

## Acyclic preparation

```text
prepareYearClose(year):
    capture applicable family inventory with independent evidence
    for family:
        Required -> request owned complete control result
        NotApplicable -> verify dated evidence and absence of contradictory retained events
        Unknown/Unsupported -> record blocker
    collect non-tax adjustment plans through each existing domain owner
    return preparation, not a final certificate

advanceClosePreparation(preparation):
    review/approve/execute domain adjustments through their owners
    recapture actual books after non-tax changes
    calculate NEXT-22 pretax bridge and approve/execute required current-tax delta
    recapture actual after-tax books
    require actual adjustment receipts exactly match selected economic effects
    prepare FINAL proposal at this new basis
```

No approval silently survives a changed economic proposal. No model/provider call runs inside the final transaction. If a technically locked period needs a closing adjustment, use an explicit authorized reopen/adjustment workflow first. Do not bypass application period admission or database integrity through an ambient flag.

## Mechanical result transfer

The qualified first closing profile uses a distinct nominal result-transfer role and a year-result equity role. Original ordinary revenue/expense entries are not erased.

```text
P = current after-tax year profit from NEXT-13, excluding OWNED transfers
F = net credit to year-result equity from prior effective transfers for this same year
D = P-F
resultTransferJournal:
    addSigned(nominalResultTransferRole, +D)
    addSigned(yearResultEquityRole, -D)
# A loss makes D negative and reverses the debit/credit direction naturally.
```

For a reopened/reclosed year, post only the additional transfer delta. Do not transfer the whole revised profit on top of an earlier valid transfer. Account mapping identifies which nominal role is technical for statement presentation. Arbitrary manual entries to that account are not automatically ignored.

## Atomic finalization

```text
executeFinalClose(command):
    return withAdmittedPrincipal(access, scope, financialClosePermission, (tx, principal) =>
        lock book; replay exact command first
        load exact final-close plan
        lock all relevant periods/accounts and domain resources in the shared ordering
        load complete required-family/control/source/tax dependency manifests
        require all approved measurements and required current controls satisfied
        require designated year-end posting period eligible for this exact action
        ClosingDomain.assertCurrentTargetAndOpeningConservation(plan, current)
        approval = validate exact financial-close approval using C5
        journal = JournalApp.postWithinTransaction(tx, plan.resultTransferJournal) if nonempty else []
        resultingBalances = ClosingDb.readBalancesWithinSameTransaction(tx, plan.year)
        require resulting raw BS equals sealed next-opening target
        require raw final nominal aggregate closes under selected bridge convention
        certificate = ClosingDb.insertFinancialCertificate(tx, plan, journal)
        opening = ClosingDb.insertDerivedOpeningSet(tx, certificate, plan.nextOpening)
        ClosingDb.applyYearAndPeriodLockStates(tx, plan)
        return finishOwnedWithinTransaction(tx, principal, command, plan,
            {journalIds: ids(journal), certificate, opening}, approval)
    )
    # One acknowledged commit. Artifact rendering/signing/filing occur later.
```

The whole finalization has one receipt. A failure after posting but before opening creation rolls everything back. A zero delta creates no fake voucher, but the certificate/opening/lock result remains atomic.

## Opening semantics

```text
nextYearReport:
    opening = selected authorized OpeningSet
    movement = actual next-year journals, EXCLUDING any journal already representing that opening
    closing = opening + movement
```

In a continuous native ledger, generating the OpeningSet creates no new cash, asset or liability journal. Old year's actual postings already establish those balances. A migration into an empty book may require one explicit opening voucher; use that as the basis once and exclude it from ordinary movements.

Nominal accounts begin a new year's report at0 under the qualified year partition, not with prior-year operating balances. BS balances include the transferred prior profit. Unadopted/missing source opening values are not set to0.

## Reopen and downstream opening impact

```text
prepareReopen(certificate):
    enumerate later openings, reports, tax/artifacts/signatures and subsequent closed years
    if unsupported consumed downstream year requires cascade: refuse with exact dependency list
    seal reason and permitted period changes
executeReopen(command):
    withAdmittedPrincipal(access, scope, reopenPermission, (tx, principal) =>
        lock book; replay exact command first
        load exact reopen plan and complete downstream membership
        require supported cascade scope and current authorized approval
        append ReopenEvent and update permitted lock state through tx
        retain old certificate, opening and files unchanged
        persist downstream invalidation/outbox intent and exact receipt through tx
    )

after corrections and revised close:
    append new OpeningSet revision with delta against old opening for explanation
    continuous ledger => projection replacement, not another opening journal
    require new next-year reports select new basis; old reports stay byte-identical
    do not rewrite already filed returns; create amendment obligations
```

## Vectors

```text
profit60000 -> nominalTransfer+60000/equity-60000; P&L stays60000
next opening cash60000/equity60000 -> no extra60000 cash journal
reopen adds expense10000 -> revisedProfit50000, previousTransfer60000 => delta-10000
reclose transfers back10000, new opening reflects50000; old snapshot remains60000
missing required VAT control -> no certificate, no transfer, no new opening
```

Certificate scope names what was checked. Financial close does not fabricate signature, filing or external acknowledgment.
