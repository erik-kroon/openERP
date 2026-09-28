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
The normal self-host API and preparation runner share explicit, default-disabled
reader configuration and private original storage. The adapter has been exercised
only against a loopback HTTP simulator. Native text reading and manual review
remain available. Live provider use remains disabled.

The route retains original bytes, independently counts physical pages, validates
provider identity and source quotes, parses Swedish printed amounts exactly, and
keeps incomplete line candidates sparse. Durable operation receipts prevent a
second submission of the same request; the existing queue polls pending operations.
Unknown dispatch outcomes and exhausted queue attempts stop automatic progress.
Review retains human edits and links the existing draft owner. No automatic posting
or payment is introduced. Inbox pagination, draft summaries and nested review
receipt keys were repaired because they prevented this journey from completing.

Ten E2E scenarios and a browser walkthrough through the normal self-host runtime
passed. Explicit suggestion selection preserves its reading identity, while human
corrections survive draft save and reload. See the
[current verification receipt](evidence/document-intelligence-end-to-end-2026-09-27/README.md).
The [initial receipt](evidence/document-intelligence-2026-09-27/README.md) is historical.
The failure contract above includes rollout requirements beyond this test set;
it must not be read as a claim that every listed failure was exercised.

During integration with the post-migration review fixes, the runner was bound to
the current configured API credential at source capture, provider-disclosure
claim, operation-receipt access and result publication. Requester-session expiry
does not cancel service intent. Cancellation, supersession and executor revocation
remain independent fences. An added real-handler/provider-simulator E2E scenario
revokes the executor before disclosure and during polling, then restores it and
observes the same operation complete without another submission.

Still outside this delivery: live provider activation and qualification,
representative accuracy/cost evaluation, hostile-document process isolation,
SiftX, shadow routing, exact visual highlights, extended capacity, company data,
and production or Book Zero acceptance. JPEG is supported by the adapter but the
retained E2E fixtures cover PDF and PNG. Encrypted/corrupt PDF rejection is
implemented but has no dedicated retained E2E case in this run.

Adapter contract references: [Azure analyze API](https://learn.microsoft.com/en-us/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-v4.0%20(2024-11-30)),
[Azure result API](https://learn.microsoft.com/en-us/rest/api/aiservices/document-models/get-analyze-result?view=rest-aiservices-v4.0%20(2024-11-30)),
[invoice model](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/invoice?view=doc-intel-4.0.0),
and [PDF loading](https://pdf-lib.js.org/docs/api/classes/pdfdocument#load).

## P00 binding — 2026-09-28 (combined main `844f680`)

Revision `844f680` (merge `77d5ab1` + `7c4defb` on `26ba496`); dirty NEXT-07/NEXT-37
files stay owned by `wB:p1G`/`wB:p1C` and are out of document scope. Document owners
now present: `native-text-v1` + `azure-invoice-v1` (`packages/contracts/src/supplier-extraction.ts:21`),
`supplier_document_operations` (`migrations/0024`), default-disabled `DOCUMENT_READER`
(`runtime/document-reader.ts`, `environment.ts`), loopback-only fixture, 5 MiB/20-page
profile with independent page count, sparse quote-locator review into existing drafts,
16 doc/extraction E2Es green per `docs/plans/overnight-review-ledger.md`.

Remaining delta P01–P13: JPEG retained case, corrupt/encrypted rejection case,
SiftX native helper (no binary/ABI — O04/O05), provider budget/tariff/disclosure
policy (O06–O08, all entries unqualified, no paid dispatch), live qualification and
corpus/company acceptance (O12–O13), off/shadow diagnostics (O14), extended profile
disabled (O15). First bounded increment: retained corrupt-PDF rejection case in the
document-owned E2E only; no shared-schema/exports, no live disclosure.

## End-to-end completion contract — 2026-09-27

The completed increment connects the normal self-host API and preparation process to
one explicit, default-disabled reader configuration and the same original store.
The complete local journey is upload, request reading, background polling, inspect
page-backed suggestions, explicitly use selected values, fill remaining facts,
save and reopen the supplier draft. Live access remains disabled.

Failures to exercise before implementation: missing/invalid configuration must
fail closed; loopback simulation must not allow external endpoints; the worker
must read API-retained bytes from shared storage; pending operations must retry
without another disclosure; UI must refresh completion and keep human edits;
unknown candidate fields must not become invented invoice lines. The normal
self-host process and normal preparation runner must be exercised together, not
replaced by an injected application handler.
