# Incoming document work

Status: implemented with local synthetic HTTP E2E observations on 2026-10-03. Visual composition remains with the Paper redesign.

## Ownership and behavior

`workspace` derives document and supplier tasks from retained intake occurrences, supplier inbox registration, current immutable draft revisions and acceptance/adoption receipts. Generic archived originals do not become tasks until routed into supplier intake. Acquisitions of identical bytes stay distinct.

Source review completes the document task and exposes its supplier draft. Preparing acceptance transfers actionable work to the journal review. Replacing a review or revising its source removes the obsolete journal from attention, generic work, assignment lookup and agent context. Posted acceptance and supplier cash adoption complete the source draft task. Legal customer issuance now also completes its customer draft task. None of these task states asserts that a payment occurred.

`RetainSource.destination = supplier_inbox` retains the occurrence and registers inbox work in one book transaction for an authorized operator. The existing supplier upload uses this path. Destination participates in retry identity; generic retention remains available through the same owner. Forward migration `0060-document-work-assignments.sql` admits the new assignment kinds.

External retention verifies an existing deterministic object before completing its transaction. This permits recovery after object storage succeeded but database completion did not. Exact hash and length are required; corrupt objects are never overwritten. Storage errors remain failures. Acquisition identity remains separate from shared bytes.

Undated document tasks are included in a selected work period with explicit copy. Upload time is not presented as invoice date; unknown document amount/currency remains unknown.

## Local verification

Run from the repository root:

```sh
OPENERP_E2E_ARTIFACTS=test-results/product-P04 bun run test:e2e apps/api/tests/document-work.e2e.test.ts apps/api/tests/source-retention-recovery.e2e.test.ts apps/api/tests/source-occurrence-multiplicity.e2e.test.ts
bun run check:changed:full
```

Observed 10 passing tests across 3 files using real isolated PostgreSQL17, the restricted runtime role, workerd and a Bun self-host object-storage path. The tests retain JSON journey receipts, results, manifest and source-integrity evidence. The failure contract is [document-work-failure-contract.md](../document-work-failure-contract.md).

Covered: distinct acquisitions and replay; failed reading; atomic supplier routing; assignment and saved-view support; concurrent source review; replacement and revised acceptance review in both attention and agent context; legal AR completion; supplier cash adoption; posted acceptance; pagination after an anchor completes; foreign-book reads/assignments; storage failure/retry; an orphan valid object; corrupt equal-length and wrong-length objects. Non-posting paths compare ledger state before and after.

The passing pre-commit run used base `b2728e83dac626307586cd7b83bcb17b8bc58b77` plus diff SHA256 `a2f50cea33eb5ba2c786b81c7b13e2291e2a8c56fe5c42a9ce14a6139111d2ae`. Source inventory remained stable at `55f1bb01736aeec1fc7f3820e3875e4f95358f1d15c00097e66b4b66d56a60bd`. Full changed checks and the primary checkout's newer Effect lint rules passed. This records the observed uncommitted tree; it is not a later integrated-head verdict.

A 52-original fixture (one reviewed) measured 30 HTTP attention reads after 5 warmups: p50 23.71ms, p95 31.56ms. No parent baseline or 10000-record measurement was taken; this is a smoke measurement, not the broader performance gate.

## Remaining boundaries

No live document provider, company data, production migration or deployment was used. These observations do not establish company readiness, visual acceptance, whole-program performance or external delivery. Searchable business metadata is a separate document-library slice. The forward migration and complete stack need integrated-head verification before landing.
