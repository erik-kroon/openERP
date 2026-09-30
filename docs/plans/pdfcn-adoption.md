# pdfcn adoption

The owner selected pdfcn on 2026-09-30 and confirmed that there are no existing customer artifacts, customers or real database to preserve. [ADR 0016](../adr/0016-pdfcn-legal-documents.md) records the decision to replace the synthetic legal-invoice and credit-note templates directly. Takumi remains the renderer; pdfcn supplies the owned React presentation components. Copy upstream source at a pinned revision and retain its MIT notice.

## Failure contract before implementation

- A floating-point conversion must not change an issued amount. Render exact retained minor-unit strings, including values above JavaScript's safe integer range, in Swedish SEK formatting.
- Current party changes must not affect the captured invoice or issued credit. Render only their retained snapshots.
- Descriptions containing Swedish text, quotes, markup characters and newlines must remain literal, complete text.
- Fifty long invoice rows must paginate without losing, duplicating or separating their text and amounts. Every page must carry its actual page number and total. Keep totals and payment terms together; do not produce a footer-only page.
- Unsupported glyphs must fail visibly without producing substituted text or changing issuance, journals or numbering.
- Replay and resume must return the same sealed bytes; conflicting input and another book must refuse the operation.
- Credit checkpoint rollback, retained failure and Bun queue recovery must still work with the pdfcn renderer.

The owner's visual review on 2026-09-30 adds two presentation obligations: retain the credit explanation as a distinct note before the totals, leaving the credited amount as the final summary line; draw row separators before the following row so no page ends with a trailing row rule. Verify the note's position and the vector rules in the public-API E2E PDFs, and retain fresh page previews.

## Delivery and proof

The legal-invoice and credit-note owners now compose the adapted pdfcn components. The renderer IDs are `openerp-se-invoice-pdfcn-v1` and `openerp-se-credit-note-pdfcn-v1`. The previous synthetic legal templates are removed; migration 0042 updates the credit artifact/failure constraints without editing the reviewed baseline. The fixed local theme avoids upstream's mutable module theme state. The [source record](../../apps/api/src/adapters/pdf/pdfcn/UPSTREAM.md) retains the exact upstream revision and MIT notice.

Verification completed on 2026-09-30. All five E2E tests passed through the public Worker APIs, disposable PostgreSQL and real Bun queue. The repeatable command is:

```sh
GOMAXPROCS=2 OPENERP_E2E_ARTIFACTS=test-results/pdfcn bun run test:e2e apps/api/tests/pdfcn.e2e.test.ts apps/api/tests/credit-document.e2e.test.ts
```

PDF.js independently verified the resulting text and A4 geometry. The exact-amount invoice and credit note each have one page; the fifty-row invoice has five pages, with 8, 12, 12, 12 and 6 complete rows. Totals and payment terms remain together on the last page. All seven rendered pages were visually inspected for clipping, overlap, readable text and footer placement.

The ignored `test-results/pdfcn/` directory retains the three PDFs, rendered page PNGs, text/coordinate JSON, journey receipts, source manifest and suite results. `source-integrity.json` reports no source changes during verification. `owned-source-match.json` confirms that the tested implementation, tests, manifests, lockfile and configurations match the primary checkout; it records both revisions because unrelated cash-method work advanced the primary checkout during the isolated run.

The final `bun run check:changed:full`, frozen dependency install, API and scripts TypeScript checks, and Worker dry-run build passed. No deployment or live company-data verification was performed.

The pre-implementation run reached the public invoice request and refused the new renderer ID with HTTP 400. It also encountered host contention and source changes from unrelated cash-method work; it is a failure observation, not fixed-revision acceptance evidence. Final verification uses an isolated checkout of the owned change. Existing E2E fixture setup took almost a minute under that contention; these journeys allow 120 seconds for fixture provisioning and verification. The application's existing render timeout remains unchanged.

## Visual review follow-up

The credit explanation now appears under **Om krediten**, before the totals. **Krediterat belopp** is the final summary line. Table body rules precede the next row, so each page's last row has no rule beneath it; the header and page footer keep their structural rules.

The five E2E tests passed again in the primary checkout on 2026-09-30 with `OPENERP_E2E_ARTIFACTS=test-results/pdfcn-layout` and the same command above. The PDFs and all seven page previews are retained there. Independent extraction now also retains horizontal vector-rule geometry and checks the absence of a rule after each page's last row. The credit journey checks the note's heading and position before the credited amount. All seven previews were inspected. `source-integrity.json` reports a stable inventory, SHA-256 `f4b5a906de702eb8122abea8e09c57735e8e7bf060d4e37015000b68fc513902`. The type-aware changed-file gate passed for this follow-up.

## Owner-requested revert

On 2026-09-30 the owner reverted the subsequent typography and hierarchy trial. The current presentation restores the earlier IBM Plex Mono theme, inline totals and ISO dates. The credit note remains before the totals, and page-end rows retain no trailing separator. The pdfcn adoption and its application workflows remain in place.

All five public-API/Bun-queue E2E tests passed with `OPENERP_E2E_ARTIFACTS=test-results/pdfcn-revert` and the same command above. Every restored renderer, shared presentation component and PDF test matches its previously verified source hash. All seven freshly rendered page previews are byte-identical to `test-results/pdfcn-layout`; `restored-preview-match.json` records their hashes. The fresh source inventory stayed stable, and both changed-file gates passed.
