# NEXT-98: Accountant period-review engagements and versioned acceptance

**Priority when applicable:** P1. **Lane:** REVIEW.

**New work:** Add an in-product accountant review engagement around exact period artifacts and findings. Book Zero already owns the review outcome; this adds its collaborative workflow rather than another close certificate.

**Use existing owners:** Book-scoped membership, review packs, existing cases, corrections and period-readiness owners.

**Required earlier contracts:** NEXT-13, NEXT-23, NEXT-25, NEXT-49, NEXT-50.

**Conditional gates:** NEXT-95: counterparty confirmations are part of the selected review evidence.

**Evidence basis:** R02, R04, P25. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Engagement scope

```text
ReviewEngagement {entity/book, period, purpose, assignedReviewers,
  authorizedSourceClasses, financialSnapshotSet, evidenceManifest,
  requestedProcedures, limitations, revision}
ReviewFinding {engagementRevision, sourceRefs, claimedIssue,
  severity, proposedResolutionOwner, replyEvidence, disposition}
ReviewAcceptance {exactEngagementDigest, reviewerAuthority,
  selectedFindingsAndDispositions, coverageLimitations,
  acceptedAt, currentnessState}
```

An accountant's access is explicitly delegated through existing membership rules. Being assigned a review does not automatically grant payroll details, payment initiation or authority to approve their own proposed corrections. Do not introduce a second identity system or call this an audit opinion.

## Capture and review

```text
prepareEngagement(period):
  retain exact financial reports, controls, open items, coverage and source manifest
  record all required procedures and unresolved inputs for selected scope
  grant only reviewed existing read permissions to the assigned reviewer
  send invitation through authorised delivery, without exposing unrelated books

replyToFinding(finding, evidence):
  retain versioned response and source links
  classify proposed financial correction, missing evidence or explained difference
  route financial changes to their existing prepare/approve/execute owners
  never modify the ledger directly from a comment or mark a fix complete from text alone
```

After a correction commits, a new engagement revision captures the affected reports and receipt. Old findings remain linked to what the reviewer actually saw. A reply may resolve an explanation without a journal; that outcome still requires the assigned review policy and evidence.

## Acceptance

```text
acceptReview(command):
  admitted tx: current reviewer scope, book/review locks and exact replay
  require exact engagement revision, completed selected procedures and no hidden mandatory finding
  verify resolution receipts and relevant source/control dependencies
  append acceptance with explicit limitations and digest
  update current readiness links, not financial period locks
```

Financial close, review acceptance, signature and external filing are distinct events. A local policy may require an accepted review before a particular close operation, but that is an explicit scope dependency, not a universal statutory claim.

A new material source or posting can stale the current acceptance. Irrelevant metadata changes need not invalidate it when the selected dependency model proves they do not affect scope. Never re-sign an old acceptance with the new reports' hash or hide unresolved findings behind a refreshed dashboard.

## Interface and outcomes

The accountant sees assigned engagements, required work, concise differences since prior review and direct source/report links. The owner sees actionable requests with preserved draft responses and one current acceptance state. Exports reproduce exact reviewed bytes and all limitations.

```text
review snapshotA accepted -> later correction produces snapshotB, A remains historical
owner writes 'fixed' but no required receipt -> finding not financially resolved
reviewer has no payroll grant -> cannot open private payroll original through a finding link
missing bank month -> engagement incomplete despite balanced trial balance
review accepted -> does not submit VAT or unlock a period
```

Completion is a real invitation, scoped review, correction/reply, recapture and accepted-result journey. Existing first-period qualification remains a separate observed company outcome, not assumed complete by installing this workflow.
