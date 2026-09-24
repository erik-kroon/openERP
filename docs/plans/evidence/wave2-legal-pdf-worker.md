# Synthetic legal issue → Takumi PDF through the Worker

Observed on 2026-09-24 with a disposable local PostgreSQL 17 cluster and local Cloudflare Worker. This is a **synthetic** scenario; it is not Drastic AB data, legal approval, delivery, or provider acceptance. The original SQL issuer fixture was prepared by the AR ledger workstream and run only in the disposable database. No test source or credential is committed.

## Reproduce the public boundary

1. Follow [`docs/local-development.md`](../../local-development.md) with a fresh disposable database and restricted `openerp_app` role. Run `bun run --cwd apps/api db:migrate`. Create three synthetic operators and the evidence, counterparty, draft, reviewed seller policy, accounting profile, issue review and independent approval described in [`apps/api/AR-LEGAL-ISSUE.md`](../../../apps/api/docs/AR-LEGAL-ISSUE.md). Execute that issue in the same UTC day; retain its returned `id` and `digest`. For this observation the synthetic issue had number `AR-1`, net `10000`, VAT `2500`, gross `12500` minor units, and one immutable ledger/register recognition. This setup is required; a missing issue correctly returns 404.
2. Start the local Worker with a temporary Wrangler config and `.dev.vars` **outside** the checkout, bound to that restricted local database. Do not reuse a real tenant or an existing `.dev.vars`. Set `BASE=http://127.0.0.1:<worker-port>/api/v1/entities/entity_synthetic/books/book_synthetic/commerce` and the synthetic operator bearer token.
3. Call the real route; the response contains `capture`, `artifact`, and an exact `contentBase64` PDF. Retry with the same key, GET the returned capture ID, and POST `.../render` with the same bearer token.

```bash
curl -fS -X POST "$BASE/legal-invoice-pdfs" \
  -H "Authorization: Bearer $OPENERP_ACCESS_TOKEN" \
  -H 'idempotency-key: ar_pdf_prepare_positive_001' \
  -H 'content-type: application/json' \
  --data '{"issueId":"<saved-issue-id>","issueDigest":"<saved-issue-digest>","rendererVersion":"openerp-se-invoice-takumi-v1"}'
```

Verify the returned PDF begins `%PDF-`, its decoded byte length equals `artifact.byteLength`, and SHA-256 equals `artifact.sha256`. With the maintenance connection to **that disposable database**, verify `select count(*) from openerp.ar_legal_pdf_captures` and `select count(*) from openerp.ar_legal_pdf_artifacts` are each `1`. Retry the same `POST` and `GET /legal-invoice-pdfs/<capture-id>`: both must return the same capture and PDF bytes. Cross-book reads with that token must fail `403`. Re-run the migration command to check checksum replay. Shut down and delete the temporary Worker/database after inspection.

## Red → green observation

- Before [`8210-ar-legal-pdf-digest-fix.sql`](../../../apps/api/migrations/8210-ar-legal-pdf-digest-fix.sql), a real Worker `POST` returned HTTP `500`, with **zero** PDF capture/artifact rows. The same SQL function called directly reported PostgreSQL `operator is not unique: unknown - unknown` at the draft snapshot digest check. The already-versioned `7610` cannot be edited in place.
- The forward migration replaced only that function with explicit parentheses around the JSONB snapshot expression. SHA-256 of the migration source: `7180aac81e80c83221e6efffa1bc7b065aac00c73ece5dca250ff664286d748d`. Migration replay reported `already applied`; this disposable database applied 134 migrations including an unrelated in-progress `8200` slice.
- Retrying the **same** Worker request returned HTTP `200`, `capture.id=ar_pdf_d9de821e7af84c41a4e2ae2e6e7514b9`, one `AR-1.pdf` artifact of `9997` bytes with SHA-256 `15fd8f0e97cc8e5524638d19c091bb0f370e2bb40adcd15afbc4ad791c18c15d`. `artifact.legalInvoice=true` and `artifact.delivered=false` remain distinct. The returned PDF bytes matched the descriptor hash. Retry, GET, and `POST /render` returned the identical view; PDF capture/artifact/issue table counts were `1/1/1`.
- The rendered real-Worker artifact was inspected at 595×842 pixels. The issue date, seller, customer, line, exact `125,00 kr` payable amount and page footer are visible. [PDF](wave2-legal-pdf-worker/issued-AR-1.pdf) · [white-background PNG](wave2-legal-pdf-worker/issued-AR-1.png). `sha256sum` of the PDF reproduces the descriptor hash above.

This proves a synthetic one-line issue-to-PDF application path and replay, not an actual-company invoice, emailed receipt, Peppol acceptance, browser flow, long-table pagination, screen-reader behavior, or Cloudflare deployment performance. The separate 50-line Takumi artifact still has a footer-only page and splits row detail across pages.
