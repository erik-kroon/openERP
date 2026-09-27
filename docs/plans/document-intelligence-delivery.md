# Document Intelligence first journey

Base: `0965a66`; isolated from the active main checkout. User authorization on
2026-09-27 includes implementation and new E2E coverage. Live provider use stays
disabled. The source is Drastic's preserved Document Intelligence End State v2.

## Contract before implementation

Deliver one supplier-document reading route through the existing extraction job,
retained attempt, human review and supplier draft owners. Preserve native-text-v1
and its original-byte spans. PDF/image observations use page/quote references and
sparse line candidates; missing amounts, quantity and tax treatment stay missing.
The first scope is one complete PDF, PNG or JPEG within the existing 5 MiB limit,
at most 20 physical pages, and an explicit Swedish printed-amount profile. No
selected-page disclosure, automatic bookkeeping, new queue or shadow routing.

Use the combined Azure invoice response contract as the first adapter boundary.
The application will be exercised with a local simulator and synthetic originals.
This establishes integration only. No live account, pricing, privacy, reader
accuracy, SiftX qualification or company-period acceptance is inferred.

## Failure cases fixed before code

- Disabled reader cannot dispatch; manual work and native text remain available.
- Corrupt, encrypted, oversized or unsupported originals produce named failures.
- Original bytes and hash are verified; physical page count is independently read.
- Missing/duplicate/out-of-range provider pages cannot become a complete result.
- Wrong API/model identity, malformed JSON, invalid source spans or ungrounded
  fields are rejected; model numeric values cannot replace printed amount tokens.
- Partial fields and lines remain sparse; no default quantity, zero tax or total.
- Retry/restart cannot submit the same request twice; a lost submission response
  is unknown, while a known operation can be polled again.
- Cancellation, a newer generation, changed source or revoked authority prevents
  selecting a late result. No financial transaction stays open during reading.
- Concurrent human edits survive; accepted invoices require correction review.
- Reload reads the same retained attempt, review and draft identities.
- Native historical receipts retain their schema and original-byte semantics.

## Verification and remaining gates

Use real PostgreSQL, public HTTP admission/review, the actual application runner,
and a local provider simulator. Retain exact source identity, synthetic original
hashes, requests, independent expectations, observed results and replay commands.
Exercise the browser review separately. Live provider rollout, corpus evaluation,
SiftX isolation, shadow diagnostics and extended capacity remain separate gates.

## Observed delivery — 2026-09-27

Implemented on `codex/document-intelligence` in the isolated product checkout.
The normal runtime has no document-reader binding: live reading stays disabled.
The injected adapter is exercised only against a loopback HTTP simulator. Native
text reading and manual review remain available.

The route retains original bytes, independently counts physical pages, validates
provider identity and source quotes, parses Swedish printed amounts exactly, and
keeps incomplete line candidates sparse. Durable operation receipts prevent a
second submission of the same request; the existing queue polls pending operations.
Unknown dispatch outcomes and exhausted queue attempts stop automatic progress.
Review retains human edits and links the existing draft owner. No automatic posting
or payment is introduced. Inbox pagination, draft summaries and nested review
receipt keys were repaired because they prevented this journey from completing.

Eight E2E scenarios and a browser walkthrough passed. See the
[dated verification receipt](evidence/document-intelligence-2026-09-27/README.md).
The failure contract above includes rollout requirements beyond this test set;
it must not be read as a claim that every listed failure was exercised.

Still outside this delivery: live provider configuration and qualification,
representative accuracy/cost evaluation, hostile-document process isolation,
SiftX, shadow routing, exact visual highlights, extended capacity, company data,
and production or Book Zero acceptance. JPEG is supported by the adapter but the
retained E2E fixtures cover PDF and PNG. Encrypted/corrupt PDF rejection is
implemented but has no dedicated retained E2E case in this run.

Adapter contract references: [Azure analyze API](https://learn.microsoft.com/en-us/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-v4.0%20(2024-11-30)),
[Azure result API](https://learn.microsoft.com/en-us/rest/api/aiservices/document-models/get-analyze-result?view=rest-aiservices-v4.0%20(2024-11-30)),
[invoice model](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/invoice?view=doc-intel-4.0.0),
and [PDF loading](https://pdf-lib.js.org/docs/api/classes/pdfdocument#load).
