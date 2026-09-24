# Wave 2 local Worker route smoke — 2026-09-24T11:03:19+00:00

This is a **synthetic, isolated** PostgreSQL 17 and local Cloudflare Worker observation, not a legal invoice issue, provider send, real-company validation, or production acceptance. Source state: `75432e0` plus the AR binding and PDF renderer changes recorded with this evidence; this is not a pristine `75432e0` observation.

## Repeat

1. Follow [`docs/local-development.md`](../../local-development.md) to start a disposable PostgreSQL 17 cluster, set `DATABASE_ADMIN_URL`, run `bun run --cwd apps/api db:migrate`, configure the restricted `openerp_app` role, and provision `examples/synthetic-book.json` with a new 32+ character `OPENERP_ACCESS_TOKEN`. Use only a fresh disposable database; `db:provision` is not a replay command.
2. Start `wrangler dev` with a temporary config and `.dev.vars` **outside** the repository, pointing `main` at `apps/api/src/runtime/cloudflare.ts`, `DATABASE_URL` at that restricted local role, `BETTER_AUTH_URL` at the chosen local port, and a fresh `BETTER_AUTH_SECRET`. This avoids reading or changing the checkout's existing `apps/api/.dev.vars`. Let `BASE=http://127.0.0.1:<worker-port>/api/v1/entities/entity_synthetic/books/book_synthetic/commerce`.
3. Drive the public HTTP routes with an actual provisioned bearer token. These examples contain no credential value:

```bash
curl -i -H "Authorization: Bearer $OPENERP_ACCESS_TOKEN" "$BASE/legal-sales-policies"
curl -i "$BASE/legal-sales-policies"
curl -i -H "Authorization: Bearer $OPENERP_ACCESS_TOKEN" "$BASE/legal-sales-policies/missing_policy"
curl -i -H "Authorization: Bearer $OPENERP_ACCESS_TOKEN" "$BASE/legal-invoice-pdfs/missing_pdf"
curl -i -H "Authorization: Bearer $OPENERP_ACCESS_TOKEN" "$BASE/legal-invoice-issues/missing_issue/pdfs"
curl -i -H "Authorization: Bearer $OPENERP_ACCESS_TOKEN" "$BASE/legal-invoice-pdfs/missing_pdf/deliveries"
curl -i -X POST -H "Authorization: Bearer $OPENERP_ACCESS_TOKEN" -H 'idempotency-key: wave2localproof2026' -H 'content-type: application/json' --data '{"issueId":"missing_issue","issueDigest":"sha256:0000000000000000000000000000000000000000000000000000000000000000","rendererVersion":"openerp-se-invoice-takumi-v1"}' "$BASE/legal-invoice-pdfs"
```

Use the same policy-history GET with a different `entityId`/`bookId` to check scope denial. Run `bun run --cwd apps/api db:migrate` again against the same disposable database to check migration replay. Shut down the Worker and disposable database afterward.

## Observed

- Fresh migrations applied through `8100-ar-legal-issue.sql`: `132` rows in `public.openerp_migrations`. A second migration run reported those migrations `already applied`.
- Authorized legal-policy history: HTTP `200`, `{"scope":{"entityId":"entity_synthetic","bookId":"book_synthetic"},"complete":true,"items":[]}`.
- No bearer token: HTTP `401`. Another book/entity under the same token: HTTP `403` (`Forbidden`).
- Nonexistent legal policy, PDF, issue PDF history and PDF delivery history: HTTP `404` (`NotFound`), not a Worker `500`.
- Valid POST shape for an absent legal issue: HTTP `404`, `Legal issue was not found in this book.` Counts in `openerp.ar_legal_policies`, `openerp.ar_legal_pdf_captures`, and `openerp.ar_legal_pdf_artifacts` remained `0`.

This checks Worker route composition, authentication, book access, read/error schemas and absence of an unintended PDF write. It does **not** exercise the successful issue-to-PDF path, long-document pagination, email/Peppol provider behavior, or actual company evidence.
