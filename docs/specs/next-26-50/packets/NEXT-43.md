# NEXT-43: Reviewed dimension restatement without editing journals

**Priority:** P1. **Owner lane:** REPORTING. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing original dimension assignments, report snapshots and contribution identities. Add classification history beside them.

**New scope, not repeated work:** NEXT-14 deliberately excludes posted retagging. Add the explicitly planned original-versus-reviewed analytical view without changing financial amounts, original tags or old exports.

**Dependencies:** NEXT-14, NEXT-13. **Integrate after:** APP-SLICE-READY(dimensions).

**Evidence:** R03, P14 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Classification history

```text
DimensionRestatementPlan {
  scope, selectedJournalLines, financialRecordedCutoff,
  originalAssignmentDigest, currentClassificationHeads,
  desiredAssignmentsByLine, effectiveAccountingScope,
  policyRelease, reason, evidence, digest
}
ClassificationRevision immutable {
  lineId, originalFinancialDigest, fullReviewedAssignmentSet,
  predecessorClassificationId?, effectiveScope, approvedPlan, recordedAt
}
ClassificationHead {book, lineId, revisionId, version}
```

A revision describes the complete reviewed assignment set for a line at its scope. Explicit removal becomes `unassigned`, not omission that accidentally inherits today's default. Unknown original history and an evidenced exemption remain distinct. The raw original line and tax/source relationships never change.

## Review and application

```text
prepareRestatement(selection, requestedChanges):
  capture complete selected line membership and current classification heads
  require no amount/account/currency/tax-point/economic-owner change in request
  resolve target dimension/value revisions and validity for chosen analytical scope
  validate required/fixed analytical policies and explicit exceptions
  require each selected line's financial digest matches retained original
  calculate before/after per-value totals and unassigned buckets
  require unfiltered signed totals unchanged
  seal exact selection, full assignments, reasons and policy witnesses

executeRestatement(plan): App transaction, no journal
  current access, book lock and exact replay
  lock classification heads in stable line order
  require original line digests and expected heads unchanged
  recheck relevant classification policy and approved target values
  append immutable revisions and advance heads
  append classification_changed event and receipt
  do not alter vouchers, original dimension tables or legal artifacts
```

The initial implementation can conservatively stale an entire line if another classification changed, rather than silently merge conflicting edits. Refining to independent dimension-level concurrency requires explicit combined-policy validation.

## Report semantics

```text
classificationAt(line, mode, classificationCutoff):
  if mode==original: return original assignments
  if mode==reviewed:
    return latest approved applicable revision recorded at/before cutoff
           or explicit original/unknown state

captureRestatedReport(selection):
  freeze ledger boundary, classification cutoff and selected revision IDs
  use those assignments throughout all pages and artifacts
  report includes mode and full classifier basis digest
```

Each financial contribution appears once in each chosen dimension partition. A cross-tab uses one tuple of assignments per contribution. Separate project and cost-center totals are two views of the same money, not additive totals. A single cost center need not balance the company balance sheet, so no balancing journal is created.

Original SIE export remains original accounting data. A separately requested analytically restated export must identify its altered classification basis and satisfy the format/recipient contract. Never silently replace the original dimension bag in the statutory/accounting archive.

## Subsequent reversal and explanation

Undoing a classification creates another reviewed revision restoring the desired assignment set. It does not delete prior history. Old saved reports retain old classification cutoffs. A new report can compare classification-only differences separately from new financial postings.

The source journal's exact reversal inherits original dimensions. Analytical reporting can optionally propagate a reviewed classification to the related reversed contribution only under an explicit linked classification decision; do not rewrite the financial correction itself to match today's analytics.

## API/UI and vectors

The bulk-review screen shows selected rows, original tags, current reviewed tags, proposed tags, total effect and missing/exempt values. Scope changes invalidate the preview rather than keeping approval for a different selection. Ordinary agents can propose and inspect; authorized humans approve the restatement.

```text
A100 + B200 + unassigned50 =350
move original A100 to reviewed B -> original report A100/B200/U50,
    reviewed report A0/B300/U50; both total350
old saved report before restatement -> unchanged
attempt to change account while retagging -> rejected as financial correction
same revision replay -> same receipt; concurrent changed head -> stale
```

This resolves the backlog's classification-storage gate with immutable overlays and fixed report bases. It does not introduce a second financial ledger or permission to alter VAT attribution via project tagging.
