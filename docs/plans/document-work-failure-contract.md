# Document work failure contract

The work list must keep each retained acquisition distinct, preserve an unfinished supplier draft after source review, and expose the next owning decision. Source review completion does not mean posted accounting.

Before implementation, the public HTTP journey must establish these observations.

- A generic retained original is absent until routed to supplier intake. Repeated registration produces one task for that occurrence.
- Two acquisitions of identical bytes produce two document tasks. No amount or invoice date is guessed from upload metadata.
- A failed reading remains actionable. Assignments and saved views accept the document identity and preserve book authorization.
- Committed review completes document work and exposes one supplier draft before any acceptance review exists. Concurrent review retries produce one draft.
- Preparing acceptance transfers the actionable task to its journal review. Posted acceptance completes that task. A new draft revision invalidates an older review and makes the draft actionable again.
- Synthetic and legal customer issuance both complete customer-draft work. Supplier cash adoption completes supplier-draft work through its own owner.
- Page counts and cursors use the same projection. A completed anchor remains usable. Unauthorized reads and assignments reveal no record.
- Agent context recognizes the new work owners and does not mislabel document review as expense review.

Run `OPENERP_E2E_ARTIFACTS=test-results/product-P04 bun run test:e2e apps/api/tests/document-work.e2e.test.ts`. Retain the fixture references, responses, source manifest and independent ledger comparison. Visual composition is deferred to the ongoing Paper redesign.

## External object recovery

The following cases precede the recovery fix. Use the real Bun self-host filesystem object adapter through public retention requests.

- A verified object left behind without a database commit is reused, then same-key replay returns the same acquisition.
- A second acquisition of identical external bytes has a distinct occurrence and task while retaining one unchanged object.
- An existing object with wrong bytes of equal length, or wrong length, refuses publication with MissingEvidence and remains unchanged.
- Read and write storage failures retain Unavailable; reuse is permitted only after verifying expected length and SHA-256.

Run the focused `apps/api/tests/source-retention-recovery.e2e.test.ts` and retain its orphan recovery and corrupt refusal JSON artifacts with the run manifest and source integrity result.

## Direct inbox selection

Failure vectors authored before the fix: an explicit scoped original must open even when absent from the loaded first twenty inbox rows; an atomic upload must immediately open its retained occurrence; missing, unauthorized and interrupted reads must keep their actual errors and a close action without automatically registering anything. `supplier-inbox-selection.e2e.test.ts` covers these public browser boundaries and retains a journey receipt.
