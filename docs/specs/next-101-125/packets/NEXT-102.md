# NEXT-102: Scoped evidence requests and response reconciliation

**Priority when applicable:** P1. **Owner lane:** EVIDENCE.

**New scope:** Add an explicit request/reply workflow for missing facts or documents. Search, upload and a review finding alone do not say who was asked, what they supplied or whether the request was satisfied.

**Existing owner to extend:** Existing source occurrence/inbox, permission-scoped sharing and review-case owners.

**Earlier contracts:** NEXT-26, NEXT-65, NEXT-93, NEXT-98. **This-wave dependencies:** None.

**Conditional:** NEXT-101: the requester uses firm-to-client delegated access.

**Basis:** R02, P93, P98 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Request contract

```text
EvidenceRequestRevision {
  id, book, originatingCaseRefs, recipientIdentity, requestedItems,
  permittedPurpose, accountingPeriod, deadline, revision, supersedes?
}
RequestedItem {
  stableItemId, question, acceptableEvidenceKinds,
  requiredFactSchema, sourceRelationship, privacyClass
}
ReplyEnvelope immutable {
  requestId, requestRevision, authenticatedOrVerifiedResponder,
  receivedAt, originalMessageRef, retainedOccurrenceIds, assertedFacts
}
ItemResolution immutable {
  requestItemId, replyRefs, reviewer, outcome: satisfied|partial|rejected|waived,
  acceptedFactRefs, remainingQuestions, evidenceDigest
}
```

Request state distinguishes sent, viewed if evidenced, replied, reviewed and resolved. A file arriving is not proof that every question is answered. A waiver preserves the missing/failed requirement and can never masquerade as verified evidence in a mandatory accounting check.

## Prepare and send

Capture the exact originating case and missing fields, then prepare a minimized message with recipient scope and a revocable request-specific upload token. The token permits only viewing this request's authorized content and submitting replies; it confers no book search, ledger read or posting authority. Mask private salary/party details unless necessary and explicitly permitted.

Use the existing authorized delivery/outbox for the message. Persist attempt identity before network I/O. An unknown delivery outcome is not a reason to create another request ID. A reminder references the same request revision, not a new obligation. Redaction happens before message sealing, not as mutable view-time replacement of approved bytes.

## Receive and link without automatic fact confirmation

```text
acceptReply(requestToken, envelope):
  authorize token, intended recipient and current request visibility
  retain original message and files with safe media/size handling
  do not execute document macros or obey instructions embedded in attachments
  in short application tx:
    replay exact message/source identity
    append reply-to-request relationship and source occurrences
    label matches to requested items as proposed
    queue supported extraction through NEXT-26
```

A legitimate duplicate byte file can answer more than one distinct evidence purpose while sharing content storage. Economic recognition remains with the financial owner. Source revision or email routing alone cannot move evidence into another client's book.

```text
reviewReply(request, selectedItems, decision):
  capture original item requirements, reply revisions and current case facts
  compare actual supplied facts/documents with each required field and period
  preserve partial, contradicted and unrelated replies explicitly
  reviewer selects the accepted evidence and resolves discrepancies
  App tx:
    recheck request/item/reply/case revisions and current reviewer authority
    append item decisions and accepted fact references through owning fact operations
    update the original case only for the exact fulfilled requirements
    store receipt; do not post, approve a financial plan or auto-close period
```

When a request is revised, old replies remain linked to the old questions. They can be explicitly adopted to a new item if semantically applicable; the app does not silently mark new questions answered. A later invalidation of accepted evidence reopens the affected case/current readiness while retaining the prior resolution.

## Workspace and vectors

Show request items beside original replies, provenance, extraction suggestions and accepted decisions. The firm/client queue can group identical missing facts without merging distinct evidence scope. A private respondent sees only their own request; an authorized accountant can see case effects across selected items.

```text
asked invoice and business-purpose explanation; only invoice uploaded -> partial
new request adds foreign-establishment fact -> old reply does not satisfy it
recipient token revoked after upload -> retained authorized evidence survives,
    new request views/submissions denied
same inbound message retried -> one reply envelope and original occurrences
review accepts a document already used in purchase -> no new expense or payable
```

Completion includes one real UI request, retained response, reviewed fact/case resolution and uncertainty/revocation recovery in an authorized environment. Message delivery and accounting completeness are independently evidenced.
