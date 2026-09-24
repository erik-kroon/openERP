# Swedish document classification and field selection

2026-09-24. **Research and proposed design only.** No classifier, extraction provider, benchmark, or product integration was implemented or run.

This refines the document-reading part of the [agent preparation proposal](agent-preparation-proposal.md). The first experiment tests whether a narrow Jev classifier and field selector can reduce manual document review. The intended product outcome is a retained original with a suggested document type and source-linked invoice fields in the existing review screen.

The classifier should also be callable by the external preparation agent. It does not require an embedded chat assistant.

## Observed integration boundary

The [document inbox](../../apps/web/src/components/document-inbox.tsx) already uploads and lists retained originals. [Source retention](../../apps/api/src/application/source-retention.ts) owns bytes, digests and scoped retrieval. The [supplier inbox](../../packages/contracts/src/supplier-inbox.ts) owns extraction attempts and operator review into a supplier draft. Its existing suggestions are free-form strings with a source location and confidence; they do not establish typed field selection or a model execution record.

No Jev adapter or PDF/OCR extraction dependency was found in the inspected API manifest and runtime bindings. Kyoto's native PDF helpers cannot simply be placed in the Worker. Classification receives extracted text; text extraction is a separate dependency with its own failure results.

Inspection began at HEAD `c04dbde62c45e3b9851d5e61454b8e9dad552dc7`. Concurrent, uncommitted supplier-inbox discovery changes include migration `9100-supplier-inbox-discovery.sql`, paginated discovery and metadata-only inbox records. Those files were left untouched. Implementation must reconcile with their final contract, preserving separate authenticated original-byte retrieval.

## Product scope

First evaluate Swedish and English text-bearing PDFs. Scans, photographs, unreadable PDFs and mixed-document bundles must be represented in the corpus, but can yield an explicit manual-review result. Supporting automated extraction from images requires a separately selected and evaluated OCR reader. Do not label a text-only pilot as image support.

The proposed initial registry is:

| Kind | Distinguishing evidence | Suggested destination |
| --- | --- | --- |
| `invoice` | Supplier/customer, invoice identifier and billed goods or services | Invoice review; determine direction separately. |
| `credit_note` | Explicit credit/correction tied to an earlier charge | Credit review. |
| `receipt` | Evidence of a completed purchase/payment with purchase details | Expense review. |
| `bank_statement` | Account activity over an interval, often with opening/closing balances | Statement review; no automatic import. |
| `tax_account_statement` | Tax-account transaction/balance record | Tax-account review. |
| `payment_confirmation` | Confirmation of a transfer/payment rather than the underlying supply | Supporting payment evidence. |
| `payment_reminder` | Request for payment of an existing obligation | Link/review against an existing invoice. |
| `other_tax_document` | Other recognizable tax correspondence or forms | Document review. |
| `supporting_document` | Attachment, terms, specification or explanatory material | Document review. |
| `unknown` | Insufficient evidence or none of the supported kinds | Manual selection. |

These are proposed routing labels, not judgments about a document's authenticity or legal effect. A destination is offered only when OpenERP supports that workflow; otherwise use document review with the classification retained.

Classify page role separately as `main`, `continuation`, `supporting`, `blank`, or `unknown`. A text extraction failure does not prove a page is blank. In the first version, conflicting document kinds or uncertain page grouping send the complete original to manual review. Do not split or discard pages automatically.

Invoice direction requires the selected company's identity and extracted parties. An unresolved buyer/seller match stays unknown. A document cannot select its own tenant or book.

## Jev's responsibility

TypeSafe's [Choice API](https://docs.typesafe.ai/api) accepts a bounded option set and returns a selected option, probabilities and confidence. Use one question per decision, with descriptions and confusing alternatives in a versioned registry. Keep `unknown` or `none` in every decision where the input may be insufficient. Pin a concrete model version and retain the version actually returned.

For invoice fields, enumerate candidate spans first and ask Jev to select their IDs. TypeSafe publishes this [candidate-selection approach](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook). A selected value can still be the wrong span, and source text can contain OCR errors. The selected ID therefore points back to text and coordinates rather than becoming an accepted fact.

Start with printed invoice number, invoice date, due date, currency, supplier/buyer identifiers, and document-level net/VAT/gross amounts. Full line-item extraction is a later extension. The current supplier-draft contract requires lines, so header suggestions alone cannot create a complete draft: the operator still enters or verifies line details through the existing editor.

Do not create a synthetic single line from document totals. Classifying printed VAT text does not establish rate eligibility, deductibility, accounting period or an account selection.

Example:

```text
span-01: "1 000,00" near "Exkl. moms"
span-02: "250,00"   near "Moms"
span-03: "1 250,00" near "Att betala"

Jev selects gross amount → span-03
Code copies raw text → "1 250,00"
Code normalizes explicit SEK/scale 2 → "125000" minor units
Code checks independently selected net + VAT against gross
Human compares the suggestion with the original
```

Keep identical printed values at different positions as distinct candidate IDs. Otherwise an amount repeated in a prior balance or explanatory example loses its meaning and provenance. Date and amount arithmetic remain in code. Ambiguous numeric formats, missing currency, uncertain signs and conflicting candidates produce diagnostics rather than guessed normalization.

## Proposed contracts and ownership

The following are conceptual contract sketches, not source added to the application:

```text
DocumentTextManifest
  original: { occurrenceId, sourceSha256 }
  reader: { name, version, configurationDigest }
  pages: [{ number, state: read | unreadable | not_processed,
            textDigest, retainedTextReference, sourceMapReference }]

CandidateSpan
  id, page, textDigest, start, end, rawText
  optional original-page bounding box

FieldSelection
  selected: { candidateId, normalizedValue, normalizationVersion }
  OR missing: { reason }
  OR ambiguous: { candidateIds, reason }

DocumentAnalysis
  original + text-manifest digest
  criteriaVersion, requestedModel, returnedModel
  page decisions, document-kind suggestion, field selections
  provider probabilities/confidence, diagnostics, usage
  actor, createdAt, immutable analysis digest
```

Use discriminated Effect Schemas, existing exact-money/date schemas and canonical strings. Text offsets must use a declared convention and refer to the exact retained text bytes/representation; normalized display text cannot silently replace the indexed text.

General classification belongs to **source intake**, before a source is known to be a supplier invoice. Add an immutable analysis owner tied to the existing occurrence rather than registering bank/tax documents in `supplier_inbox`. Keep large text/source maps in the existing retained-artifact storage with scoped immutable references. SQL owns admission, identity, revisions and receipts.

Supplier review can select a particular analysis and project its fields into the existing extraction-attempt contract, retaining `analysisId` and digest. That projection must not become a competing source of truth. Operator edits and acceptance retain their existing authority; earlier attempts and accepted draft history remain unchanged.

Likely code locations after the experiment:

| Responsibility | Proposed owner |
| --- | --- |
| Text/analysis/field-selection wire contracts | `packages/contracts/src/document-analysis.ts` |
| Classification criteria and direct orchestration | `apps/api/src/application/document-analysis.ts` and a local criteria data file |
| Jev request/response validation | `apps/api/src/adapters/documents/jev.ts` |
| Scoped SQL dispatch and analysis persistence | Existing database statement pattern plus a forward migration |
| User action, result and original comparison | Existing document inbox and supplier editor |

Use the existing Effect HTTP facilities and validate the external response at the adapter. A new SDK, workspace package or general AI framework needs a demonstrated benefit. Do not move Swedish accounting calculations into this adapter.

## Caller, lifecycle and review

The proposed product caller starts analysis with `(scope, occurrenceId, sourceSha256, idempotencyKey)`, receives a durable analysis/run reference, and can read or rediscover it after reload. REST and MCP call the same owning operation.

```mermaid
sequenceDiagram
    participant UI as Document review
    participant API as Effect operation
    participant DB as PostgreSQL
    participant Reader as Document reader
    participant Jev
    UI->>API: Analyze retained original
    API->>DB: Admit scoped run and record source identity
    API->>Reader: Read verified bytes outside transaction
    Reader-->>API: Text manifest or explicit failure
    API->>Jev: Text + criteria / candidate IDs
    Jev-->>API: Decisions and distributions
    API->>DB: Recheck authority; retain exact result
    UI->>API: Read saved analysis
    API-->>UI: Suggestions, citations and diagnostics
```

Before model execution, enforce file/page/text/candidate limits and a configured provider budget. Persist pending and completed stages, with fenced claims for concurrent resumes. Existing recurring preparation jobs are an example of the durability pattern, not a ready-made document-analysis job. Selecting and implementing the hosted document reader and runtime adapter is required before the product button is complete.

A retry of an already saved command returns the same result. A crash after a provider call but before persistence can require another provider request and charge; do not claim exactly-once provider execution. A fencing token prevents an older attempt overwriting the chosen result. Explicit reanalysis creates a new immutable analysis.

After source replacement, the UI keeps the older result visible as history and requests analysis of the new original. A new result must never overwrite a user's edited fields. The operator explicitly selects which suggestions to apply, checks line details, and saves through the existing supplier draft workflow.

First-release UI copy should describe suggestions: “Suggest document type and fields”, “Review suggestions”, and “Enter manually”. Show loading, unreadable, unknown, failed, stale and saved states. Preserve entered work across retries. Use the existing original preview, StyleX primitives, scoped QueryClient and localization pattern. A model score is not a “verified” badge.

## Experiment before product integration

Compare three candidates on the same frozen text manifests:

1. Deterministic labels/regular expressions as the inexpensive baseline.
2. Jev classification and candidate selection.
3. A selected general-purpose model constrained to the same labels and candidate IDs.

The first implementation artifact should be a small Bun evaluation command with versioned criteria and result output, not a new user-facing service. This experiment buys the decision to use Jev. It is not completion of the upload-to-review feature.

Use independently labeled Swedish and English documents, with held-out suppliers/layouts. Keep related pages and near-duplicate templates in the same split. Include invoices, reminders copying invoice totals, credit notes, duplicate amounts, mixed bundles, scans, negative/ambiguous formats and injected document instructions. Record permitted corpus use; synthetic documents alone cannot establish real-world extraction accuracy.

Measure document and page classification, candidate recall before Jev, field selection conditional on candidate availability, end-to-end field accuracy, abstention, manual corrections, review time, latency and whole-pipeline cost. OCR, retries and fallback calls belong in that cost. TypeSafe notes that [English currently performs best](https://docs.typesafe.ai/models); measure Swedish separately.

Tune routing thresholds on a development split and freeze them before the holdout. [Confidence](https://docs.typesafe.ai/confidence) summarizes the output distribution; it is not a guarantee that a result with confidence 0.95 is correct 95% of the time on our documents. Report precision and coverage together. Initial product results remain suggestions requiring review; automatic routing is a later, separately evaluated behavior.

Retain a manifest, source/text hashes, criteria/model versions, per-document expectations/results, confusion matrix, abstentions, costs, failure logs and an exact replay command. Model-based steps require their configured provider access and usage budget. No provider was called or account provisioned during this research.

## Failure specification before implementation

| Failure | Required result |
| --- | --- |
| Unreadable or omitted page | Explicit text-manifest gap; no blank-page or complete-document claim. |
| Correct value absent from candidates | Missing result; measure candidate-recall failure separately. |
| Same number occurs in several places | Preserve candidate IDs and citations; select the role, not just the string. |
| Reminder resembles an invoice | Manual/relationship review; no second draft or financial effect from classification alone. |
| OCR corrupts a number | Original stays visible; mismatch remains diagnostic; arithmetic cannot silently repair it. |
| Forged candidate ID or malformed provider response | Reject at the adapter; no fabricated field or success state. |
| Book mismatch or authority revoked during external work | No result disclosure or accepted write under revoked authority. |
| Provider timeout or budget exhausted | Recoverable stopped/failed result and manual entry. |
| Response loss, concurrent resume, or explicit reanalysis | Recover saved identity; one selected result per command; retain distinct reanalysis history. |
| Suggestions arrive after human edits | Preserve human input and offer an explicit comparison. |

When test/fixture work is authorized under AGENTS.md/D-09, write these scenarios before code. The real E2E proof must exercise retained bytes → analysis → cited suggestions → human-edited supplier draft → reload recovery through Worker/PostgreSQL and browser boundaries. Recorded provider responses can prove integration failures; a separate live evaluation proves model behavior.

## Decision and remaining gates

Proceed first with the frozen-text experiment. Select Jev only if it improves measured review effort/cost at an acceptable error and abstention rate against the alternatives. Thresholds and representative data are experiment inputs to resolve, not facts established by this report.

After that decision, implement the document reader, durable analysis operation and review integration together. The first product release may support text-bearing PDFs explicitly, with manual fallback for scans; image automation needs its own reader and evidence. Full line-item extraction, automatic splitting, account/VAT treatment and autonomous posting remain outside this classifier slice.
