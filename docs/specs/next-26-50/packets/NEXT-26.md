# NEXT-26: Supplier extraction jobs and field-level reviewed merge

**Priority:** P0. **Owner lane:** INTAKE. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** apps/api/src/application/purchases/inbox.ts; application/purchases/drafts.ts; existing source-retention adapters and supplier-inbox contracts.

**New scope, not repeated work:** The current inbox can record extraction attempts and bind a reviewed draft. Add the actual bounded extraction lifecycle and safe reprocessing, not another inbox, matcher or purchase engine.

**Dependencies:** No new first-wave financial feature is a hard prerequisite. **Integrate after:** APP-SLICE-READY(purchases/inbox).

**Conditional gates:** NEXT-03: a reviewed draft is subsequently accepted and posted.

**Evidence:** R03, R08 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Records and selection

```text
ExtractionRequest {
  id, book, occurrenceId, originalHash, parserOrModelRelease,
  selectedPages, dataUsePolicy, generation, cancelVersion, requestedBy
}
ExtractionAttempt immutable {
  requestId, attemptId, sourceHash, engineRelease, outputSchema,
  result: succeeded | rejected_output | failed | unknown,
  fields: [{fieldKey, proposedValue, sourceLocators[], diagnostics}],
  candidateLines: [{candidateLineId, sourceLocators, fields}], retainedOutputHash
}
FieldDecision immutable {
  occurrenceId, draftRevision, fieldKey, decisionKind,
  selectedValue, attemptId?, evidenceLocators, reviewer, priorDecisionId?
}
UNIQUE(book, requestId, attemptIdentity)
UNIQUE(book, occurrenceId, acceptedDraftOwner)  # reuse the existing actual owner
```

A field key is a semantic identity, not a model array position. A proposed invoice line must have an unambiguous mapping to retained original source locations or receive a new candidate identity for review. Two equal lines are not automatically the same line.

## Preparation and extraction

```text
requestExtraction(input):
  App tx:
    current scope + exact command replay
    require authorized use of this original and chosen engine
    load occurrence metadata and current review/draft state
    capture exact source hash, page selection and engine version
    insert request and outbox intent; save receipt

runExtraction(requestId, expectedGeneration):
  read current request and cancellation/data-use permissions
  fetch original; verify its retained hash and length OUTSIDE tx
  extract existing native text first where supported
  only use selected document/vision provider when necessary and authorized
  enforce bounded bytes/pages/time/cost; no financial tools available to extractor
  decode output strictly: money remains exact source assertions, never JS float
  reject unknown fields, invented source locators and duplicate field IDs
  retain raw interpretation and normalized suggestions
  App tx:
    recover result for this exact source/attempt
    require current generation and cancellation fence
    verify original hash unchanged
    append attempt and receipt; do not change reviewed facts or post anything
```

A provider timeout is an extraction outcome, not a reason to delete the original. Repeated execution can produce different suggestions. Preserve each attempt; only one explicitly selected attempt enters a review. Cancellation after remote computation can discard publication while retaining a diagnostic attempt under the data policy. It cannot erase an already accepted invoice.

## Three-way merge instead of replacing a draft

Use `B` for the reviewed draft revision on which extraction was requested, `L` for the current draft and `S` for suggestions. Compare typed values, not formatted display text.

```text
mergeField(B, L, S, decisions):
  if S has no supported source locator: return needs_review(missing_provenance)
  if a human explicitly confirmed L after B:
      keep L; show S as an alternative, never silently overwrite
  if L != B:
      if L == S: retain convergent provenance, no value change
      else: return conflict(base=B, current=L, suggestion=S)
  if S == B: return unchanged
  return proposed_change(S)  # NOT automatically accepted

prepareExtractionReview(selection, expectedDraftRevision):
  load exact attempt, original and B/L values consistently
  require expected current draft revision matches
  map candidate lines explicitly; retain unmapped/deleted/duplicate-line conflicts
  calculate proposed source totals with existing draft calculator
  expose discrepancy list and exact chosen values
  require human selects each affected conflict and confirms the resulting review
```

For a new inbox record, reuse its existing reviewed-draft creation function inside the caller's transaction. For an unaccepted existing draft, create one new revision with a field-decision manifest. For an already accepted/issued invoice, create a correction-review case referencing suggestions; never revise the original economic document.

## Review transaction and consumers

The review transaction rechecks occurrence, attempt, draft and field-decision versions. It appends decisions, creates/revises the draft through the existing internal tx function and stores the binding/receipt together. A competing review either returns its identical receipt or fails stale; it cannot create another payable. Acceptance and tax preparation remain NEXT-03.

REST/MCP can request extraction and inspect suggestions under the existing permitted prepare role. Human confirmation stays operator-only. The UI places original evidence beside proposed changes and labels fields as source, suggested or reviewed. It displays job failure separately from source validity.

## Required vectors

```text
same request delivered twice -> one recorded result identity, no second draft
model returns 100.00 as numeric JSON -> reject monetary encoding, retain diagnostic
operator changes account after extraction start -> keep operator value + conflict
invoice accepted while extraction runs -> correction suggestions only
two legitimate identical lines -> two source-located line identities
request cancelled before publication -> no draft change or accounting effect
```

Close this packet with a runnable request -> extraction -> human merge -> recoverable draft path. Recording another caller-supplied JSON attempt alone does not satisfy the new scope.
