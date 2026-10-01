# Local main integration — 2026-10-01

At the user's explicit request, merge the retained accounting integration branch
`fc31d060f4155e4845f458ba69ceec7bae130247` with local main
`7e4bbeadc06093ecdd12ee8e694f683be0cb10d5`. Preserve both histories and independent
main changes, including Effect4 stable dependencies, DF-10 recovery responses,
cash-method approver admission, period guards and newer cash-method evidence.
Nothing is pushed or deployed. Packet6 and packet8 completion claims remain open.

Conflict resolutions keep the main recovery transport imports and cash delivery
records; retain the native PostgreSQL registry export and exact settlement
correction admission; delegate generic allocation to the shared transaction port
with main's reviewer-admission check intact; retain the commercial-period E2E.

Verification on the combined source:

- `bun install --frozen-lockfile` passes.
- `CHECK_CHANGED_TIMEOUT_SECONDS=180 bun run check:changed:full` passes all49
  changed source inputs. The initial60-second type-aware lint run timed out and
  its cleanup encountered EPERM; it is not a passing check. Process inspection
  confirmed no abandoned task check remained before the retry.
- `bun run check:integration` passes33 wired/17 declared deferred.
- Focused real runtime proof `test-results/main-merge-focused-20261001` passes3
  selected cases/44 unselected: REST/MCP settlement and cancellation,
  commercial cash invoice in a locked document period, and103-item context
  rediscovery/fresh-state change. Source manifest/integrity are retained there.
- Initial four-file runtime attempt `main-accounting-merge-20261001` exceeded its
  outer120-second deadline. Partial artifacts are preserved but no completed
  test count or green result is claimed for that attempt.

This is merge verification, not a new whole-workspace baseline or whole-packet
acceptance. Earlier proofs retain their exact source/migration bounds.
