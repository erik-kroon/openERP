# Post-migration review fixes: local verification

Date: 2026-09-27. Scope: the five concrete findings in the supplied review of
`1e632b93c758aa81550d61455f288a24b3c461d0`, bounded duplicate loading and the
adjacent defects exposed by the approved supplier journeys.

## Executed checks

Concurrent source edits made main-worktree runs unsuitable as fixed-source
evidence. Final verification used a detached worktree at `831df6c`, with the
remaining review changes applied. All task-owned source and test files were
compared byte-for-byte with the main worktree after the run; they matched.

- `bun install --frozen-lockfile`: passed in both worktrees.
- `bun run check:changed`: passed in the verification worktree.
- `bun run check:changed:full 0fb4feb`: passed in the verification worktree,
  covering the committed review implementation as well as remaining edits.
- `bun run test:e2e`: **44 tests passed in 12 files**, exit 0, 122.68 seconds.
- `source-integrity.json`: **stable**, no changed paths. Source inventory SHA-256:
  `435c9f3e4d7598f1f149372b5e960f2ba7d64c134e9245cc7e324ef671e2c597`.

The isolated worktree is retained locally at
`/var/folders/50/zdx6l4px2wg7wh8q7_78g2qr0000gn/T/opencode/review-verification`.
Its `test-results/e2e/` directory contains the manifest, JSON/JUnit results,
source-integrity receipt, journey JSON and screenshots. These local files are
repeatable verification artifacts, not a production retention archive.

## Observed behavior

- Fresh migrations retain SELECT/INSERT-only immutable extraction requests and
  column-limited mutable lifecycle grants. Admission, execution, human review,
  cancellation and redelivery work under the restricted runtime login. Removing
  lifecycle UPDATE privileges produces the supported-capability refusal.
- Executor credential revocation, book-membership removal and identity disabling
  each prevent capture before object access and prevent publication when applied
  during a paused object read. Reinstating authority resumes the durable request.
  Unauthorized terminal settlement is refused. A deleted requester session does
  not cancel service intent; explicit cancellation still fences publication.
- The HTTP journey creates and accepts 201 historical supplier drafts, creates
  another draft, reads 200/2-head pages and reads accepted revision history.
  Listing leaves posting state unchanged. Both generated duplicate cursor kinds
  resume, and wrong-context or malformed cursors fail. Nonzero, zero and unknown
  totals remain exact strings or null as specified.
- Chromium drives the real web app and authenticated Worker from a Los Angeles
  browser timezone. Stockholm midnight changes overview requests without reload.
  Summer/winter month and year boundaries and DST dates agree with independent
  PostgreSQL timezone conversions. Focus and visibility refresh a suspended page.
  Supplier listing follows its next page and server-side search finds the 201st
  fixture at a 390px viewport. Browser errors: none.

The backend uses the same tested instant conversion for book-status admission;
PostgreSQL's live wall clock was not replaced with the browser's controlled clock.
The extraction race seam uses the real Bun queue handler and a retained-file
object adapter. It does not certify remote object-store or effect-mq failure modes.

## Query and lock observations

Five requests per workload, one local PostgreSQL 17.11/workerd installation:

| Workload | Runtime statements per request | Median HTTP latency | Total SQL execution time, five requests |
| --- | ---: | ---: | ---: |
| 50-candidate duplicate page | 14 | 51.94 ms | 76.63 ms |
| One-candidate continuation | 15 | 48.03 ms | 55.78 ms |

The continuation validates its retained anchor with one additional statement.
The larger page does not add one database round trip per candidate. The artifact
retains every sample; these figures are observations, not an old/new benchmark or
a production latency guarantee. SQL execution time is not transaction wall time.

An intentionally blocked read was observed waiting on the book lock. The sampled
blocked-query age was 50.98 ms and the complete request took 103.11 ms after the
fixture released its lock. This confirms the retained reader/writer barrier; it
does not justify removing it.

## Limits

No deployment, real-company accounting, provider certification, broad concurrency
benchmark or narrowed production credential rollout was performed. Verification
covers the fixed snapshot and the compared task files, not unrelated changes made
concurrently afterward. The maintained implementation decisions are in
[architecture follow-up](../../architecture-followup.md#post-migration-review-september-2026)
and the repeatable commands and failure contracts are in
[the E2E guide](../../../apps/api/tests/README.md).
