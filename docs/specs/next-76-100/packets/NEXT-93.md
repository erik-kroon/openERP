# NEXT-93: Source-located evidence search and retained-page retrieval

**Priority when applicable:** P1. **Lane:** EVIDENCE.

**New work:** Add a searchable projection of retained originals and interpretation text with exact source locations. Extraction suggestions and agent context are not a document search index.

**Use existing owners:** Original evidence/content store, extraction attempts, permissions and existing artifact/retention owners.

**Required earlier contracts:** NEXT-26, NEXT-50.

**Evidence basis:** R02, R04. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Search is a projection, not evidence authority

```text
TextRevision {originalContentHash, extractorRelease, representation,
  pageOrSectionLocators, textHash, extractionWarnings, recordedAt}
SearchDocument {book, evidenceIdentity, sourceRevision, textRevision,
  accessClass, tokenizationVersion, indexedAt}
SearchHit {originalRef, sourceRevision, locator, exactSnippet,
  textRevision, interpretationState, score, limitations}
```

Use the existing database's suitable text index for the first bounded implementation before adding another search service. Source text, OCR/model interpretation and reviewed facts have separate labels. A search result does not confer authority on the original prose or prove the accounting treatment.

## Build and query

```text
indexOriginal(version):
  read authorised immutable source and supported native/extracted text
  retain source-located text revision with engine/version and known gaps
  outbox job stages index entries keyed by exact content/text revision
  publish only after complete selected representation is retained and validated
  old text revisions remain historical; current index pointers may advance

searchEvidence(scope, query, filters):
  validate bounded query grammar, book and permitted private scopes
  perform access-filtered search over selected index revision
  return snippets only from authorised hits with exact original locators
  distinguish partial index coverage from an exhaustive no-match result
```

A payroll original must not appear as a snippet to a user who only has aggregate accounting permission. Filtering after fetching/displaying snippets is too late. Search history, autocomplete counts and exports must follow the same scope rules.

## Reprocessing and navigation

Reindexing an original does not change accepted purchase fields, amounts or existing citations. Return the text revision used by the hit. The page/section viewer loads that exact original revision and highlights its locator; a locator that cannot be reproduced is shown as unavailable, never silently moved to similar current text.

Same-byte content may be associated with several legitimate source occurrences. Results can group identical content for convenience while exposing occurrence identities and their separate financial links. Do not merge those economic events in the index.

## Access and failure

Current authority is rechecked on opening/downloading an old hit. Revocation removes future access even if the browser cached a reference. Previously delivered bytes cannot be retracted; do not promise otherwise. Search suppression, retention expiry and legal retention remain governed by the existing evidence owner, not a delete button that destroys bookkeeping information.

Index lag or extractor failure appears as coverage diagnostics. The user can still open originals manually. An unavailable index returns an explicit degraded result; it cannot report that no invoice exists.

## Completion examples

```text
one PDF, two text revisions -> old hit still names old text/source hash
phrase only in unauthorised payroll -> no snippet, count or existence leak
text extraction fails on page3 -> search coverage incomplete, original remains usable
identical invoice bytes in two legitimate occurrences -> grouped content with both source IDs
new parser changes numbers -> suggestions may change; reviewed accounting facts do not
```

Provide keyword/filter search, original-page navigation and evidence-link drilldown through shared REST/MCP/UI. No vector search or expensive model is required to complete the initial indexed text workflow. Search scores are not accounting confidence.
