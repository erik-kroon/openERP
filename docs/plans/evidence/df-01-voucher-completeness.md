# DF-01 — composed voucher completeness and deferred SQL refusals

Qualified and observed 2026-10-01 on the worktree based on `6c96c90`.

## Disposition of the claimed hole

The missing journal-table balance trigger is not a reachable post-commit bypass
under the composed reviewed constraints:

1. Voucher insertion schedules a deferred check requiring exactly N balanced lines.
2. Journal ordinals are positive and at most the voucher's sealed N.
3. `(book, voucher, ordinal)` is unique, so N lines exhaust every permitted slot.
4. Voucher count/identity and existing journal lines cannot be updated or deleted.

After a successful commit there is therefore no free ordinal, and neither the
slot bound nor the occupied history can be reopened. The unused alternate branch
in the existing deferred-check function does not establish a missing guarantee.
No redundant trigger or baseline migration change was added.

Real PostgreSQL probes exercise ordinals 0, 1, 2 and 3 after a two-line API posting:
the lower bound, unique occupied slots and upper-bound trigger refuse all inserts.
Runtime UPDATE/DELETE restrictions and maintenance-side immutable-row triggers
refuse changing N or removing lines. The original posting remains unchanged.

## Actual defect found and repaired

Deferred commit checks return direct Effect SQL errors. `databaseFailure` previously
classified every direct SQL error as `Unavailable`, while its wrapped Drizzle path
recognized PostgreSQL `P0001` accounting details. Thus an authentic commit-time
`InvalidJournal` became HTTP 503 instead of its stable business refusal.

The common mapper now extracts either direct or wrapped SQL errors and applies
the same PostgreSQL-code classification. Known accounting refusals retain their
code without leaking database text. Infrastructure, connection, interruption and
unexpected defect handling keep their established distinctions; they do not become
credential revocation or successful empty results.

Synthetic fault triggers drop a selected debit line or add one minor unit to a
credit only in the disposable test book. The deferred count/balance guard rejects
both at commit. HTTP now returns `422 InvalidJournal`, all attempted posting
effects and kernel receipts roll back, and the original execution key succeeds
once after the injected fault is removed. These triggers are test instrumentation,
not shipped integrity logic, and are removed in `finally`.

## Observed proof

Full changed-file lint/types and integration checks pass. The full local E2E
suite passed **195 tests across 51 files**, covering the shared transaction mapper,
rollback/replay, authority, close/report, bank capacity, documents and browser
journeys on PostgreSQL 17.11, local workerd and the restricted runtime role.
Source inventory remained stable at
`e7ded834d46715eb3c1e06ba924806d691e2d3b3bff945685e093b641202ca6e`.

That full run is retained under
`test-results/e2e-history/2026-10-01T08-04-44.727Z-4d287cdb`.
After strengthening the test to explicitly assert the returned accounting code,
the three focused DF-01 cases passed again with stable source inventory
`cb7322eb5e6540a0e2a9265a166a62788bcfa33ae2ed34cb95a8022748961011`.
Implementation code did not change between those runs.

This qualifies the reviewed constraint composition and fixes failure transport;
it does not certify production data, company accounting or hostile administrators
who disable triggers or rewrite reviewed DDL.

## Repeatable evidence

```sh
bun run check:changed:full
bun run check:integration
bun run test:e2e apps/api/tests/voucher-completeness.e2e.test.ts apps/api/tests/persistence.e2e.test.ts apps/api/tests/diagnostics.e2e.test.ts
```

The harness retains `df-01-late-append.json`, `df-01-missing_line.json`,
`df-01-unbalanced.json`, results, manifest and source-integrity records.
`bun run test:e2e` reproduces the broader regression run in disposable systems.
