# DF-03 — frozen result-transfer bridge for derived P&L

Implemented and observed 2026-10-01 on the worktree based on `bd6403c`.

## Reproduction and corrected finding

The served `report-family-snapshots` path first failed with HTTP 500: its SQL
catalogue dereferenced record fields from `jsonb_array_elements`, which exposes
one JSON value instead. It now uses a typed `jsonb_to_recordset` projection.

The current close owner does not mirror every nominal account to zero, contrary
to the original DF-03 description. Its mechanical result transfer uses the
reviewed result account. The remaining defect was reproduced with real owners:
income `75000`, an ordinary expense `5000` on that same account, synthetic tax
`14000`, and an owned close transfer `56000`. The legacy family reported expense
`61000`, treating the result transfer as another operating cost. Excluding the
whole account would also hide the genuine `5000` expense.

## Delivered basis and trace

New P&L families capture the released statement owner's admitted result-transfer
classification at the **saved trial-balance cutoff**, under the owning transaction.
They retain complete voucher membership in the immutable report header as
`resultTransferVoucherIds` and identify `profitBasis` as
`owned_result_transfer_exclusion_v1`. The existing statement port derives its
ownership flag from the application-reserved `result_transfer_v1` purpose; this
slice consumes that classification, not a second account-number heuristic or an
independent certification of hostile/out-of-band database changes.

The read computes a signed `resultTransferMinor` per mapped role from the retained
journal lines named by those frozen identities. P&L presentation uses the declared
side and `ordinary movement = raw movement - result transfer`. Entire references
and exact monetary strings remain scoped; no amount comes from the caller.

Trial-balance lines, opening/movement/closing figures, contributing-entry reads
and general-ledger drill-down remain the complete posted record. The family UI
shows the transfer bridge beside the mapped amount and explains that distinction.
In the reproduced row, raw movement/closing is `61000`, the transfer is `56000`,
and ordinary expense is `5000`. The semantic statement independently reports net
result `56000` from `75000 - 5000 - 14000`.

Before-close snapshots retain empty transfer membership and never change after
a later close. A new family requested later from an earlier source still uses
that source's cutoff. Legacy families without the new basis keep their original
raw-movement interpretation and numbers, with an explicit read-view limitation;
their sealed bodies are not rewritten. Balance-sheet/cash-flow families retain
their existing basis. No migration or financial write was added.

Capture refuses more than 20,000 source components or 1,000 transfer vouchers;
it never certifies a truncated membership. This is still the bounded synthetic
reviewed-mapping family, not statutory output or actual-company readiness.

## Observed verification

Full changed-file lint/types and integration checks pass. Seventeen E2E tests
across report-family close, financial close, SIE account-code and cash-flow suites
pass using PostgreSQL 17.11, local workerd, the restricted runtime role and real
Chromium. The tested source inventory remained stable at
`a979a737a8bd56ad44dd641768c2d4f754ccdaf5e563cfad6faa1a13d3fd17d4`.

The new journey exercises actual tax recognition, approval and close before
recapturing the derived family. It checks ordinary cost preservation, the exact
transfer bridge, unchanged raw trial balance and both contributing debits, frozen
earlier snapshots, recapture from an old cutoff and read-only MCP parity. A seeded
legacy-format family remains at `61000` with a truthful limitation. Chromium opens
the real saved P&L and displays the bridge without page errors; its screenshot
was inspected. Narrow/zoom and screen-reader proof are not claimed for this change.

## Repeatable artifacts

```sh
bun run check:changed:full
bun run check:integration
bun run test:e2e apps/api/tests/report-family-close.e2e.test.ts apps/api/tests/financial-close.e2e.test.ts apps/api/tests/sie-account-codes.e2e.test.ts apps/api/tests/cash-flow-statement.e2e.test.ts
```

`test-results/e2e` retains `df-03-family-close.json`, `df-03-transfer-bridge.png`,
the browser log, results, manifest and source-integrity records. Older runs are
archived under `test-results/e2e-history`.
