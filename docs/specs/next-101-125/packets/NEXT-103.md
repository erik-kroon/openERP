# NEXT-103: Versioned balance-sheet substantiation schedules

**Priority when applicable:** P1. **Owner lane:** REVIEW.

**New scope:** Add per-account explained balance schedules and preparer/reviewer certification. This supports an existing close/review; it is not another close certificate or journal reconciliation engine.

**Existing owner to extend:** Existing immutable report snapshots, financial contribution identities and independent evidence/review owners.

**Earlier contracts:** NEXT-13, NEXT-23, NEXT-95, NEXT-98. **This-wave dependencies:** None.

**Conditional:** NEXT-102: missing supporting evidence is requested from a client.

**Basis:** R03, P13, P98 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Schedule basis

```text
SubstantiationTemplate {
  accountRoleOrSelectedAccounts, purpose, requiredEvidenceKinds,
  allowedSupportRelations, ageingRules, independentControlRequirements
}
ScheduleRevision immutable {
  templateVersion, ledgerSnapshotId, balanceDate, recordedCutoff,
  sourceContributionSet, supportLines, unassignedContributionIds,
  independentControlRefs, explanations, preparedBy, digest
}
SupportLine {
  id, economicItemRef, signedAmount, originalCurrency?, bookCarrying,
  attributionShares, evidenceRefs, dueOrReleaseDate?, reviewState
}
ScheduleReview {revisionDigest, reviewer, acceptedScope, unresolvedExceptions, recordedAt}
```

Only the existing GL/report owner supplies the balance. An AP or asset subledger adapter contributes its original item identities, not a second mutable control total. A manually created support line must explicitly distinguish an explanation from independently substantiated value. A manager's assertion is labelled as such.

## Construct and validate

```text
prepareSubstantiation(accountSelection, date):
  capture exact opening/movement/closing contribution identities at one cutoff
  load supported subledger items and independent statement/contract evidence
  map each selected amount to item-level support with exact shares
  reject duplicate physical GL amounts counted under several support lines
  compute:
    explained = sum(valid signed support shares)
    unexplained = authoritativeClosing - explained
    staleEvidence, missingItems, unexplainedRows, unsupportedAllocations
  retain unmatched offsetting rows even when unexplained net is0
  seal complete source membership and template/version
```

For a grouped control account, require each support item's sign and currency/carrying convention to match the role. Positive supplier credits and negative payables may need separate presentation lines rather than hiding behind a net balance. Cross-currency native quantities do not sum into a meaningless total.

A support amount can be split across evidence items only when shares conserve the original component and each relationship is meaningful. Multiple documents corroborating the same receivable increase provenance, not amount. Imported openings require their actual retained basis; no source is invented for an unexplained opening.

## Acceptance is scoped and nonfinancial

```text
reviewSchedule(revision, reviewerDecision):
  recheck exact revision and required reviewer permission/segregation
  require mandatory controls observed and accepted support types
  unresolved material item => qualified exception/refusal, not silently removed
  append review of this specific schedule and cutoff
  notify existing period-review/close owner of the result
  never create an adjusting journal or declare the whole company complete
```

Currentness uses account-specific content and supporting evidence revisions. A new posting to another unrelated account need not invalidate it. A backdated item affecting the selected balance does. Prior accepted revisions remain readable even when current readiness becomes stale.

The schedule can propose a named owned adjustment for a genuine supported discrepancy. It cannot post an arbitrary plug equal to the unexplained difference. Adjustments flow through their domain owner with new approval, then a fresh substantiation revision explains their receipt.

## Interface and evidence

An accountant chooses the balance date and template, sees source items and documents, requests missing support and reviews the complete schedule. Exports use the same fixed rows and review status. A reviewer can restrict the acceptance to a specific account rather than pretending every connected account is substantiated.

```text
closing100000; supported75000+15000 -> unexplained10000 remains
closing0 with unexplained+5000 and-5000 -> not complete
two PDFs prove same receivable20000 -> support20000, not40000
source confirmation from wrong year -> retain reply but reject support relation
new valid posting later recorded for old period -> previous report unchanged,
    current substantiation stale until recaptured
```

Independent evidence is genuinely independent of the computed ledger total where the template requires it. Generating a second report from the same journal does not establish external completeness. Completion includes capture, review, stale-change detection and reproducible exported evidence through the existing workbench.
