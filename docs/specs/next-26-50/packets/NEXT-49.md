# NEXT-49: Rule-change impact and evidence-backed obligation fulfillment

**Priority:** P0. **Owner lane:** REPORTING. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing rule releases, retained plan/report dependencies and closing/deadlines.ts manual obligations/calendar feeds.

**New scope, not repeated work:** Do not rebuild deadlines or rule activation. Add exact affected-record analysis and require meaningful fulfillment evidence instead of treating any nonempty reference string as proof.

**Dependencies:** NEXT-02. **Integrate after:** APP-SLICE-READY(closing/deadlines).

**Conditional gates:** NEXT-04: VAT calculations are impacted; NEXT-21: payroll declarations are impacted; NEXT-48: annual-report authority outcomes fulfill deadlines.

**Evidence:** R03, R06, P02 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Impact inventory

```text
RuleChangeNotice immutable {
  oldReleaseId, newReleaseId, effectiveScope,
  reason, qualificationEvidence, affectedSemanticSelectors
}
ImpactSnapshot {
  noticeId, recordedCutoff, completeTargetMembership,
  targets: [{owner,id,revision,usedRule,basisDigest,impactKind}]
}
ImpactDecision immutable {
  targetRevision, kind: unaffected_with_reason | reprepare | amend | human_review,
  evidence, proposedSuccessor?, reviewer
}
```

Query actual retained dependency references. Do not grep free-text documents or invalidate every book because a new rate table exists. Historical correctness and current executability are distinct: a future-only rule change need not invalidate a past calculation. A retroactive correction identifies affected original periods without rewriting their reports.

## Bounded impact calculation

```text
captureRuleImpact(notice):
  require newly qualified release and explicit effective-scope relationship
  select exact plans, calculations, declarations and deadlines referencing old release
  intersect each target's semantic dates/case with notice's applicability change
  freeze target IDs/revisions and cutoff before paging
  if full selection exceeds bound: partition explicitly, retain total/continuation

classifyImpact(target, notice):
  if outside changed applicability: unaffected_with_reason
  if prepared/unexecuted: require fresh computation and approval when effects differ
  if committed/unfiled: create owned financial/control review, no automatic reversal
  if filed/accepted: create amendment obligation retaining original receipt/artifact
  if missing old facts prevent determination: needs_evidence, not unaffected
```

A background handler may compute prospective replacements or comparisons through the owning prepare operation. It cannot approve them, mutate old artifacts or call a generic arbitrary financial correction. Freeze child identity by notice+target+revision so restarts do not create duplicate amendment cases.

## Typed fulfillment evidence

```text
FulfillmentReference =
    LocalPreparedArtifact {owner, artifactId, revision, digest}
  | SubmittedAttempt {owner, attemptId, artifactDigest, environment}
  | AuthorityOutcome {owner, observationId, receiptIdentity, coveredScope}
  | ReviewedExternalEvidence {originalRef, reviewer, assertedMeaning, limitations}

verifyFulfillment(obligation, reference):
  resolve reference under current book/role access
  require same entity, family, period and intended revision/supersession relation
  require exact required outcome predicate, not a numeric status ranking
  require environment appropriate to obligation; sandbox cannot fulfill production
  require artifact integrity and relevant source/outcome evidence
  return satisfied OR pending/mismatch with precise reason
```

Keep existing arbitrary operator references as historical `reported` observations. Do not silently upgrade them to verified authority evidence. A required `prepared` deliverable can be satisfied by its valid local artifact; a required authority outcome cannot.

## Transactions and calendar behavior

```text
linkFulfillment(command):
  App tx:
    reauthorize; lock book/obligation; recover exact command
    check expected obligation revision and required-outcome policy
    validate referenced retained outcome/artifact from its own owner
    append fulfillment link with validation witness
    update derived current state and calendar revision
    save receipt
```

Dismissed reminder and fulfilled obligation remain separate. A revised due date changes the existing calendar event's revision while retaining stable identity. Genuine withdrawal needs a reason/evidence and explicit cancellation output; successful fulfillment is not automatically a cancellation of historical obligation. Use the existing feed revocation and renderer rather than another calendar service.

Statutory date rules are selected by actual reporting period and jurisdiction plus the applicable holiday/timezone release. Do not invent due dates from a generic “monthly plus30days” shortcut. An override retains the original basis and its reason.

## UI and vectors

Show what rule changed, exactly which records are affected, old/new calculation differences, owner action and fulfillment evidence. Sensitive payroll impacts obey payroll scope even when displayed in a shared work index.

```text
new rate effective next year -> prior-year accepted artifact not silently stale
retroactive mapping fix affects3 returns -> exactly3 retained impact targets
nonempty string 'done' -> reported note only, not verified authority acceptance
sandbox receipt matches production period -> wrong environment, unfulfilled
due-date revision -> same calendar identity, higher revision
reminder dismissed -> required submission still outstanding
```

This completes the backlog's impact/fulfillment semantics. It does not automatically decide that a legally filed document must be amended merely because a code version changed; the notice must specify the actual corrected rule and affected cases.
