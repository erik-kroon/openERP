# Accountant review package — root integration handoff

## Release

END-03 bounded synthetic first-year accountant-review/export slice is source-complete. No worker database writes, migrations, servers, builds, tests, fixtures, dependency additions or Git operations occurred. Root owns integration and native/runtime validation. Source presence/static checks are not financial, crash, concurrency or browser proof.

## Owned files

- `packages/contracts/src/accountant-review.ts` and internal `closing-providers.ts`
- `packages/contracts/src/closing.ts` — optional provider coverage permits decoding original0800 historical payloads
- `apps/api/src/accountant-review.ts`
- `apps/api/migrations/0810-accountant-review-packs.sql` — NEW, still-unapplied source extended with0610/0710 provider capture
- `apps/api/migrations/0820-closing-owner-tax-dependencies.sql` — NEW forward replacement of private closing basis only
- `apps/api/CLOSING.md`; `apps/web/src/components/closing/copy.ts`, `review.tsx` — new check scope and explicit narrower-scope display
- `apps/api/ACCOUNTANT-REVIEW.md` — risk/acceptance cases were recorded before transition implementation; concrete behavior/limits now documented
- `apps/web/src/components/accountant-review/panel.tsx`, `inspector.tsx`, `copy.ts`
- `docs/plans/06-year-end-reports-filing.md` — bounded END-03 source status, not acceptance completion

Applied migrations, including0800, were not edited.0810 additionally requires0610 owner-register and0710 expense-tax providers;0820 requires those providers and0800. Root must confirm0810 is still unapplied before applying the updated source.0890 is reserved for the correction owner and was not used.0900 Better Auth admission is reused through the current `authenticate`/`authorize` functions; numeric filename ordering is not a request to replay applied migrations.

## Shared composition (root only)

1. Export `./accountant-review` from the contracts package.
2. Add `AccountantReviewApi` to the shared API and spread `AccountantReviewCapabilities` into the shared capability catalog.
3. Add fixed parameterized Drizzle `sql` expressions to `database.ts` as mapped below. Keep the existing scoped Effect connection, errors and response-schema decoder.
4. Bind the ordinary capability names below through existing `bindCapability`. All operations use current scoped auth; no approval or posting authority is introduced.
5. Provide `AccountantReviewHandlers` from `apps/api/src/accountant-review.ts` in Worker HTTP composition. REST and MCP use the same capability handlers.
6. Lazy-mount `AccountantReviewPanel` from `@/components/accountant-review/panel` with `{book, locale}`, keyed by `book.id`. No new shared translations, router state, QueryClient or auth implementation is needed.

### Fixed database statements

Each expression returns `AS result`; every variable is a bound template parameter, never `sql.raw`.

| Operation key | PostgreSQL function / parameter types | Ordered parameters |
| --- | --- | --- |
| `prepareAccountantReview` | `openerp.prepare_accountant_review(text,jsonb,text,jsonb)` | token, scope, idempotencyKey, input JSON |
| `listAccountantReviews` | `openerp.list_accountant_reviews(text,jsonb,text)` | token, scope, after or empty string |
| `getAccountantReview` | `openerp.get_accountant_review(text,jsonb,text)` | token, scope, packId |
| `accountantReviewRows` | `openerp.accountant_review_rows_page(text,jsonb,text,text,text)` | token, scope, packId, section, after or empty string |
| `getAccountantReviewArtifact` | `openerp.get_accountant_review_artifact(text,jsonb,text,text)` | token, scope, packId, format |

### Capability bindings

All arrays below are **after token**. Use `scopeParameter(input.scope)` for scope.

| Capability | Operation | Parameter array |
| --- | --- | --- |
| `accountant_review_prepare` | `prepareAccountantReview` | `[scope, input.idempotencyKey, JSON.stringify(input.input)]` |
| `accountant_review_list` | `listAccountantReviews` | `[scope, input.after ?? ""]` |
| `accountant_review_get` | `getAccountantReview` | `[scope, input.packId]` |
| `accountant_review_rows` | `accountantReviewRows` | `[scope, input.packId, input.section, input.after ?? ""]` |
| `accountant_review_artifact` | `getAccountantReviewArtifact` | `[scope, input.packId, input.format]` |

The contract exports exact schemas and endpoint names. Paths are book-scoped `/accountant-review-packs`, `/:id`, `/:id/rows/:section`, and `/:id/artifacts/:format`. Artifact GET returns a validated JSON envelope with exact UTF-8 content, descriptor and pack identity; the browser checks length/hash and offers an actual downloaded `.json` or `.csv` file. No custom streaming route is needed for this bounded slice.

## Implemented

- Current report → one locked ledger/config/source/evidence basis → immutable materialized rows and exact bytes.
- Opening explanation/evidence are explicitly **not verified**, even with no prior vouchers or a first-year claim.
- All captured-prefix voucher lines include exact amounts, opening/movement/excluded-later classification and receipt/approval/evidence lineage. Original and reversal remain visible.
- Every retained evidence record is included in the source inventory, including unlinked and later-excluded records; source-only documents are not blindly treated as missing postings.
- All source/control coverage is separately visible. Missing expected bank accounts and declarations are explicit. Stable bank/commerce/schedule hooks are captured, but empty modules never become not applicable. Released0610/0710 source/review/control contracts are captured directly, never inferred from table presence. Every owner source/current review is retained, including after-end exclusions; provider control bodies retain exact registered positions/effects/allocation links and unexplained account differences. Every expense source/current review retains all actual-review control differences and exclusions without emitting tax contributions.
- JSON plus balances/journal/evidence/coverage/owner_sources/owner_controls/expense_tax CSV artifacts are persisted atomically, with file hashes and byte sizes. Every CSV starts with a manifest row carrying scope, opening status and complete coverage/provider digests; all cells use documented spreadsheet-safe text encoding.
- Pack reads separate live unchanged-dependency observation from immutable history. Reopen/new postings do not rewrite old rows or bytes.
- English/Swedish workbench creates a fresh internal report and pack, recovers saved packs, inspects pages/evidence/coverage and saves validated files. Existing request-scoped TanStack Query and Better Auth browser path are reused.

##0820 closing integration

No new public closing route/capability/dispatcher operation is required. Existing locked prepare/approve/execute/read calls use the replaced private basis. `OwnerSourceReview` blocks unresolved/unlinked sources through end date; `ExpenseReviewCurrentness` checks only book-wide missing/stale reviews. Independent `ExpenseControlCoverage` blocks every known expense source because this provider does not supply posting/reconciled close coverage; current all-unknown reviews do not resolve it. `ownerSourceDigest` and `expenseTaxBasisDigest` are captured/rechecked by existing complete-basis comparisons. Unpaid linked claims are not errors. `ownerTaxStatus` supplies exact counts; earlier payloads omit it and the UI identifies their narrower historical scope.

Old proposals/approvals and certificates keep original bytes/digests. New-basis inequality makes old unexecuted approvals stale and old certificates noncurrent. Already committed commands still replay exactly. No migration updates journals, lock state or retained certificates. New explicit reopen remains available for repair.

The accountant-review API's operation names/parameters are unchanged. `ReviewSection` and artifact format enums now include the three provider sections/formats. The internal `closing-providers.ts` module needs no public package export. No shared composition files were edited by this owner.

## Intentional limits / blocked claims

Only native `synthetic-core-v1` is supported. No actual company activation, opening approval, zero-VAT assumption, owner loan/equity classification, result transfer, SIE/iXBRL, annual report, filing or Visma compatibility is implemented. Company completeness and statutory readiness remain unestablished/false.

Creation is bounded to1000 vouchers,5000 lines,1000 accounts,1000 evidence records,2 MiB original evidence and8 MiB per artifact, plus100 owners/1000 owner sources/1000 effects/5000 allocation legs/200 expense sources; refusal rolls back the entire pack. Pages contain25 rows. This is not a large-book background exporter. CSV's one leading apostrophe per data cell is an explicit transport convention, not original source content; the JSON artifact preserves original values. UI retry keys last for the mounted form; retained-pack listing recovers results after remount. Explicit “new version” starts a new capture and preserves previous versions.

## Next root action

Confirm existing shared integration, run native types plus lint/format, review updated0810 and new0820, then apply only those unapplied migrations in the authorized synthetic database. Manually exercise create/read/page/download/replay/historical-currentness. Include missing/stale tax review, unresolved/unlinked owner sources, unpaid linked claims, provider mutation after proposal/pack capture and earlier certificate/approval decoding. Check downloaded UTF-8 hashes and amounts/lineage independently. Use existing retained synthetic data; no new tests/fixtures are authorized. Capture observations separately from static checks. No production or external action is requested.


Exact source hashes and owned static-check outputs: `.agents/work/accountant-review-static-checks.json`. No native type, SQL execution, migration, race, browser or financial validation was performed by this worker. The static receipt must not be cited as those results.

### Review follow-up

Zero stale reviews now means only review currentness. A separate `ExpenseControlCoverage` check fails whenever any expense source is represented:0710 does not provide supported posting/reconciliation coverage, even for an all-unknown but digest-current review. Pack coverage likewise marks known expense sources missing, while preserving all assessments/exclusions. Owner/tax counts are bounded **before** provider aggregation. Accountant pack reads skip a now-oversized live basis and report noncurrent without hiding retained metadata/pages/files. Closing rejects oversized live bases entirely (including reopen); that unsupported-size limit does not create a partial digest.
