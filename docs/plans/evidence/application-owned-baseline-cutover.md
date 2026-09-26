# Application-owned baseline cutover

Historical checkpoint. Its open replacement items are superseded by the later [completion record](application-owned-replacement-complete.md); the observations below remain unchanged.

2026-09-26. This completes the three-file baseline cutover following the [application review](application-owned-review-followup.md). It does not close the remaining domain ports or every gate in [ADR 0010](../../adr/0010-application-owned-accounting-replacement.md).

## Result and repairs

- The active migration directory contains only `0001-schema.sql`, `0002-integrity.sql` and `0003-roles.sql`. The superseded 198-file chain is removed. Its exact files and SHA-256 manifest were retained in the ignored local verification artifacts before deletion.
- A fresh reference database applied every old migration, including the final SIE staging grants. Its 68 direct function roots expand to 105 retained functions when calls inside function bodies are followed to a fixed point. The baseline contains exactly that closure; `openerp.fail` and the other indirectly called helpers are present. Catalog dependencies alone cannot establish the closure of PL/pgSQL bodies.
- Runtime grants now match the reference: accounts and periods permit reads and their existing `active`/`locked` column updates, but no inserts; SIE staging tables have their required reads/inserts and four scoped progress-update columns; VAT reclassification contributions allow reads as well as inserts.
- Ten trigger entrypoints called private helpers as the runtime role, producing `42501` instead of the intended accounting refusal. They now run as the migration owner with a fixed search path ending in `pg_temp`. Helper bodies are unchanged and remain inaccessible to direct runtime calls. The immutable-row probe now returns `P0001` with `Forbidden`, preserving the original row.
- The runtime can execute only `canonical` and `digest`; PUBLIC can execute no OpenERP function. The maintenance owner's default function privileges also revoke PUBLIC execution, preserving the old chain's rule for future migrations. Application source refers to those two SQL helpers only. Feature SQL dispatch and its statement modules remain deleted.
- Sixty-two API feature notes now link to their current application owner and all three baseline DDL files. Earlier SQL handoffs and their observed results are explicitly historical. API setup, development commands, the replacement plan and ADR progress now describe the installed baseline.

## Observed results

Verification used owned, disposable PostgreSQL 17 clusters. No existing company database was opened or modified. The comparison includes `openerp`, `openerp_auth` and `public`, including queue tables and the migration ledger.

| Check | Result |
| --- | --- |
| Fresh installation | Real Bun migrator applies exactly three files. |
| Structural catalog | No differences in relations, columns/defaults, constraints, indexes, triggers, views, sequences or domain types against the fully applied reference. |
| Effective grants | No differences in runtime schema, table, column or sequence privileges, or default object privileges, against the reference. A newly created probe function is private. |
| Function closure | Exactly 105 retained functions; bodies and language/volatility/strictness/parallel flags match the reference. Ten definer flags and fixed search paths are deliberate privilege repairs. |
| Guard refusal | A real immutable-row trigger rejects mutation with the accounting error, not a missing-function or permission error; the retained row is unchanged. |
| Runtime negative checks | Private helper calls, account/period inserts, TRUNCATE, trigger disabling and schema DDL are refused. Existing E2E checks also reject posted-history mutation and appended lines. |
| Rerun and drift | Repeated migration is a no-op; the existing E2E journey preserves posted state across rerun and checksum rejection. |
| Old installation | The migrator refuses the reference database's old receipts before applying baseline SQL; all old receipts remain unchanged. |
| Existing E2E suite | All 23 tests in four files pass against a fresh baseline and real workerd Worker. |
| Static/build checks | Full typechecking, type-aware lint and web/API build pass. Changed API documentation passes formatting. |

The first typecheck ran alongside a build and failed when both wrote the web build output during prerendering. Running typecheck alone passed. Full-repository formatting reports 99 existing source/document files outside this baseline edit; those unrelated formatting changes were not applied. No tests or test helpers were added or edited in this cutover.

Artifacts are in `test-results/baseline-cutover/`: old-chain manifest and backup, function closure, before/after grant differences, reference and baseline catalogs, SQL refusal results, migration logs, final baseline hashes, check logs and cleanup receipts. Existing E2E artifacts are in `test-results/e2e/`.

## Repeat

Run from the repository root with PostgreSQL 17 tools and the installed dependencies:

```bash
node test-results/baseline-cutover/verify.mjs
bun run check-types
bun run lint
bun run build
bun run test:e2e
```

The local verification artifact validates the saved old-chain hashes, creates fresh reference and baseline databases, compares catalogs/grants, checks helper execution and migration refusals, and tears down its cluster in `finally`. It requires the ignored backup captured during this cutover; it does not use a live database. The checked-in E2E suite independently creates its own fresh database and Worker. Run typecheck and build sequentially because both can build the web output.

## Remaining replacement scope

The previously identified 28 placeholders remain: 16 historical-import operations, ten impairment/disposal operations and two schedule amendments. The retained trigger closure still includes SQL policy guards, so function reachability and catalog parity do not establish the final narrow integrity boundary promised by ADR 0010. Those ports and the remaining browser, durable-delivery, recovery and company acceptance gates are separate from this completed baseline installation and cleanup.
