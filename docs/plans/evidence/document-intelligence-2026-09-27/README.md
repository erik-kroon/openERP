# Document Intelligence integration evidence

Observed 2026-09-27, isolated branch `codex/document-intelligence`, base
`0965a661c30505f343162fcf2ba9b91a0c3d8ce4`. These are synthetic fixtures and a
loopback provider simulator, not live OCR accuracy or company verification.

## Results

- Eight E2E tests passed in 98.06 seconds: native compatibility/replay; PDF reading
  and review/draft creation; partial pages and unknown submission; disabled reader,
  invalid quotes and cancellation; PNG sparse lines and page cap; late-result
  cancellation; duplicate JSON/provider failures; durable queue polling.
- Queue proof: one submission, two polls, one successful retained attempt.
- Browser: opened PDF from the inbox row, inspected two-page coverage and quotes,
  saved “retain reviewed value”, and opened the draft with `HUMAN-CORRECTION` and
  matching 1,250.00 SEK totals. Inbox and draft lists loaded successfully.
- Full changed-file checks, production web build and frozen dependency install passed.

The E2E harness uses PostgreSQL 17.11 with a restricted runtime role. Native/API
setup includes workerd; document-reader requests use the real API and application
through Bun with filesystem originals and the local HTTP provider fixture. The
queue scenario uses the actual effect-mq worker and PostgreSQL store.

## Repeat

```sh
bun install --frozen-lockfile
bun run check:changed:full
bun run --cwd apps/web build
bun run test:e2e apps/api/tests/document-reader.e2e.test.ts
```

For the optional browser proof, prefix the last command with
`DOCUMENT_BROWSER_PROOF=1`. Open the loopback URL emitted in
`test-results/e2e/document-reader-browser.json`; complete the walkthrough above
within 180 seconds, save a screenshot and write the observed checks to
`test-results/e2e/document-reader-browser.done`. This is a manual browser evidence
step, not an automated screenshot assertion. The ordinary suite needs no browser.

## Retained artifacts and identity

[Results](results.json), [source manifest](manifest.json),
[source integrity](source-integrity.json), [web source inventory](web-source-inventory.json),
[native result](document-reader-native.json), [PDF result](document-reader-pdf.json),
[review and draft result](document-reader-review.json), [queue result](document-reader-queue.json),
[browser observations](document-reader-browser.done), and [browser screenshot](document-reader-review.png).

The manifest identifies the pre-commit source by file hashes, base revision and
diff hash; the source inventory remained stable during the run. Its default
inventory excludes web source, so the separate web inventory was captured after
the browser proof without intervening frontend changes. Documentation was updated
after the run. No live provider credentials or company originals were used.

See the [delivery contract and remaining gates](../../document-intelligence-delivery.md).
