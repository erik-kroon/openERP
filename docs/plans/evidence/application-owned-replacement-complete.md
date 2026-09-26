# Application-owned replacement completion

2026-09-26. This closes the replacement defined by [ADR 0010](../../adr/0010-application-owned-accounting-replacement.md). It supersedes the open replacement items in the earlier [review follow-up](application-owned-review-followup.md) and [baseline checkpoint](application-owned-baseline-cutover.md). Company activation, statutory acceptance, hosted provider deployment and archive/key custody remain their own product and operational gates.

## Implemented boundary

All capability dispatch and direct HTTP, MCP, durable-worker and maintenance callers use named application operations. The SQL dispatcher, its statement modules and the superseded 198-file migration chain are removed. The three baseline files are the only installation path; migration receipts and checksums reject an old or changed installation without resetting it.

The remaining 28 historical-import/asset/schedule placeholders and 23 missed commerce/purchase operations now have implementations. That includes historical opening and full-history posting, financial run fencing, historical items, schedule amendments, impairment/disposal, sales order conversion, supplier acceptance/credits/payment exports, invoice cancellation, legal issuance, PDF artifacts and delivery reconciliation. Existing unsupported jurisdiction/company profiles remain explicit refusals; this replacement does not invent unfinished roadmap capabilities.

The application owns current identity and book authority, approval eligibility, calculations, dependencies, source ownership/capacity, account-role admission and register effects. Shared posting admission prevents generic posting from consuming a domain-owned source or bypassing an active historical import. Register writes, approval consumption, numbering, ledger effects and receipts share the caller's financial transaction. Financial counters remain rollback-safe table rows. Private owner context is supplied by the application and is absent from transport inputs.

The baseline now retains 17 functions, reduced from the first checkpoint's 105. The intentional difference is removal of policy guards after their rules moved into application operations; the final catalog is not claimed to be byte-identical to the historical policy catalog.

| Retained responsibility | Functions |
| --- | --- |
| Pure canonical JSON and SHA-256 | `canonical`, `digest` |
| Private refusal and immutable history | `fail`, `immutable_row` |
| Immutable identities and sealed records | `dimension_identity_guard`, `commerce_freeze_identity`, `freeze_preparation_inputs`, `ar_legal_freeze_draft`, `ar_legal_freeze_register`, `invoice_issue_guard_draft`, `supplier_acceptance_guard_draft` |
| Voucher shape, append protection and deferred exact balance | `guard_journal_ordinal`, `voucher_expected_line_count` |
| Sealed approval consumption | `posting_guard_approval_consumption` |
| Relational calendar and storage versions | `check_calendar`, `book_versions`, `bump_version` |

Only `canonical` and `digest` are runtime-callable. All functions revoke PUBLIC execution; private integrity entrypoints use fixed search paths. The runtime has scoped DML grants and cannot create schema objects, disable triggers, truncate tables or rewrite financial history. Application sealing uses the domain canonicalizer; independent byte/hash vectors match the two pure SQL helpers, including scalar strings, Unicode, nested arrays and exact decimal strings.

## Review repairs

This was a self-review and repair pass, without sub-agents. It found and fixed behavior that source-only review and the existing suite had not established:

- Supplier acceptance treated a boolean source/gross match as an object and blocked valid drafts. Permission probes also checked unrelated tables. The application now uses the actual boolean and required table set.
- Invoice projections treated SQL aliases as parameter values and omitted credit/cancellation effects. Currentness, residuals and allocation versions now reflect the retained register and active effects.
- Native scalar-string canonicalization needed JSON quoting before parsing. Schedule/asset seals now use the intended bytes.
- Legal PDF sealing/delivery compared a reduced API projection with the full retained issue. Agreement now checks the immutable retained source.
- Recurring selection omitted its rule from a CTE and used an ambiguous account predicate. Selection now carries the rule, scopes the account and respects active bank matches/allocations.
- Recovery rejected effect-mq's two sequences and encountered an unvalidated baseline constraint. The baseline validates the constraint. Recovery inventory v2 binds all seven queue tables and the two reviewed sequences; it refuses unknown/unowned/cycling sequences and sequence movement during the dump. Schema fingerprints include sequence configuration and grants.
- Bun served a 404 on direct navigation to dynamic review routes. The web build now emits TanStack Start's SPA shell; Bun serves it for HTML navigation while missing assets remain 404. The shell avoids hydrating a review route against the root page's markup.

Complex posting admission and legal issue calculation were split into named local checks. Unused SQL-backed digest access was deleted. No dependencies or new tracked tests were added, and no lint/type rules were weakened.

## Observed real-runtime journeys

Supplemental checks used disposable PostgreSQL 17, separate fixture-maintenance credentials, a login granted `openerp_runtime`, a real workerd Worker and local R2 originals. The durable run used the actual separate Bun/effect-mq process. Browser verification used Chromium, the built web app, the Bun self-host entrypoint and a signed Better Auth session cookie. No external bank, tax or delivery provider was called.

| Journey | Independent observed result |
| --- | --- |
| Sales | Create/revise/accept an order, convert two one-unit portions, reject excess conversion and replay the retained result. |
| Purchases | Accept/post a 1,000-minor-unit supplier invoice, replay, apply a 300 credit and observe 700 remaining; independently verify the payee and export retained payment XML. |
| Cancellation | Issue an invoice, refuse a revoked cancellation approval, approve again, execute/replay and observe cancelled status with zero outstanding. |
| Assets | Register basis, amend dates and estimates, post a 200 impairment and 800 disposal; replay preserves the same receipts. |
| Historical full history | Retain and stage SIE, admit a full-history basis, pause/resume with a new fence, refuse generic execution, approve/post/replay the chunk, compare closing balances and admit a 600-minor-unit historical item. |
| Historical opening | Prepare an aggregate opening, refresh it, approve/post and replay the same effect. |
| Legal invoice and delivery | Independently activate reviewed policy/accounting profile, refuse self-approval, issue/replay, render and seal real PDF bytes, independently approve delivery, start the attempt and reconcile it as confirmed not sent. |
| Queue | Two selected bank observations produce exactly two prepared changes and zero vouchers. Duplicate admission returns one job; a cancelled job stays stopped; restarting the real runner preserves completed results. Earlier dated evidence separately covers submitter revocation after admission. |
| Browser and Bun | Create source, prepare a 12.34/12.34 SEK entry, review, approve, post, restart Bun, navigate directly and reload the retained review. Database observation: one voucher, one execution receipt, zero imbalance. No client errors; missing asset returns 404. |
| Baseline | Fresh three-file install; populated rerun; checksum drift and old receipts refused; exactly the 17 allowlisted functions; runtime/PUBLIC/default-function grant probes behave as specified. |
| Recovery | Real capture-release, preflight, backup, inspect and restore commands reproduce all 266 tables, source objects, financial receipts, migration/schema/grant inventory and queue state. The finalizer confirms disabled database connections, connection limit zero and no permission to resume. |

The existing E2E suite independently covers exact money beyond JavaScript's safe integer bound, concurrent execution/replay, consumed/expired approval replay, linked reversals, cross-book access, agent approval refusal, credential/session/approver revocation, tampered plans, duplicate JSON keys, invalid money, late-write rollback, immutable history, migration rerun/drift and MCP parity. Final collected/executed counts and command exit results are in [the manifest](application-owned-replacement-complete.json).

## Repeat and artifacts

Run from the repository root, with PostgreSQL 17 and installed dependencies. Keep typechecking and build sequential because both generate web output.

```bash
bun run check-types
bun run lint
bun run format:check
bun run build
bun run test:e2e
```

The checked-in E2E runner owns and removes its scratch cluster; it writes `test-results/e2e/`. Preserve that directory before another run overwrites it.

The supplemental packet is in `test-results/replacement-final/`: `runtime.mjs` and the `*-proof.mjs`/`*-proof.ts` replay programs, exact sanitized HTTP requests/results in `http.ndjson`, canonical vectors, payment XML, legal PDF/result descriptors, browser screenshots, baseline/refusal and restore controls, check logs and cleanup record. Start `node test-results/replacement-final/runtime.mjs` from this checkout; import each proof with `await (await import('./<name>-proof.mjs')).proof()` in its input, then run `await close()`. The harness uses the existing global-setup pattern and the retained synthetic `test-results/replacement-completion/fixture.json`; it never opens a company database. Manual scripts/artifacts remain ignored local evidence, not a newly added regression suite.

Restore replay uses private temporary paths, captures the exact source release, restores only to a fresh synthetic name and removes its owned databases/private bundle after saving sanitized controls. It never promotes a writer or enables a provider. The final manifest hashes the implementation, lockfile, baseline and observed artifacts; it names the parent revision because the completion commit includes the manifest itself. Concurrent review-routing edits appeared after verification and are excluded from this commit and its source hash; their files use the verified parent versions in that inventory.

No comparative throughput claim is made. Hosted Hyperdrive behavior, provider acceptance, company facts, statutory applicability and restricted read-only application recovery are not established by these local results.
