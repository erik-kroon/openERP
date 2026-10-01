# DF-11 — Voucher dates within retained accounting periods

Observed 2026-10-01 on disposable local PostgreSQL and the normal self-host HTTP
posting application. Synthetic fixtures only; no company data or external action.

## Failure before repair

`apps/api/tests/voucher-period-date.e2e.test.ts` first ran before production edits.
Both out-of-period cases failed: a write fault changed the otherwise valid
voucher date to `2025-12-31` or `2027-01-01` against period
`2026-01-01`–`2026-12-31`, and the HTTP application returned a committed receipt.
The period foreign key did not enforce date containment.

## Delivered owner

Forward migration `0044-voucher-period-date.sql` adds relational integrity, not a
database financial workflow. An after-insert guard checks the final voucher row
against its exact book/year/period bounds under book and period locks. A period
boundary update guard prevents existing vouchers from falling outside those
bounds. Immutable voucher identity already prevents later voucher-date edits.
The helper has a fixed search path and no public execute grant. Runtime period
permissions remain limited to the existing `locked` column.

Preflight refuses inconsistent existing history with `InvalidJournal`; no history
is rewritten. Missing referenced periods also refuse rather than passing a null
comparison. Both date endpoints are inclusive.

All application posting consumers already insert into the guarded table. Existing
Effect transaction rollback and shared accounting-error contracts carry the refusal
to callers; no duplicate posting, transport or UI owner was introduced.

## Repeatable proof

```sh
bun run test:e2e apps/api/tests/voucher-period-date.e2e.test.ts apps/api/tests/voucher-completeness.e2e.test.ts
bun run check:changed:full
```

Observed: seven tests pass across two files. The out-of-period cases return HTTP
422 with `InvalidJournal`; persisted financial counts stay unchanged, then the
same request key commits successfully after removing the fault. Both inclusive
endpoints commit. Moving the corresponding period boundary past the retained
voucher refuses with PostgreSQL `P0001` / `InvalidJournal`, and the original date
remains intact. DF-01 late-append, deferred balance/count rollback and recovery
coverage continues to pass.

The integrated `bun run test:e2e` replacement run passed 200 tests across 53
files in 351.70 seconds, including migration rerun/checksum refusal, REST/MCP,
browser, financial close and shared transaction recovery. Its source inventory
remained stable. An earlier full-suite attempt was cancelled by the outer
120-second deadline and is not passing evidence; its identified disposable
PostgreSQL process was stopped before the replacement run.

Artifacts in `test-results/e2e`: `df-11-2025-12-31.json`,
`df-11-2027-01-01.json`, `df-11-endpoint-2026-01-01.json`,
`df-11-endpoint-2026-12-31.json`, plus suite JSON and JUnit results.

## Limits

The fault deliberately exercises the database guarantee beneath normal posting
admission. It is not a new user-facing ability to choose inconsistent dates.
Concurrent privileged calendar maintenance and migration against inconsistent
historical fixtures are not separately exercised by these cases. No actual-company
qualification, statutory acceptance or reopening policy is claimed.
