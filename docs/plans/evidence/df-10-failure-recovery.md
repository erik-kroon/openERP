# DF-10 — stable failure codes and end-to-end recovery semantics

Completed on 2026-10-01 in the isolated `df10-complete` worktree based
on `a626b01`. This completes the obligations left open by DF-10A.

## Contract and real owners

`packages/domain/src/errors.ts` owns an exhaustive recovery classification for
the shared failure-code family. Application `failure` construction and database
error mapping consume it; HTTP, MCP and browser consumers use the same semantics.

| Recovery | Meaning for unchanged automatic retry | Examples |
| --- | --- | --- |
| `permanent` | Repair the stated issue first; repetition alone cannot fix it | Domain refusals, invalid wire input, configuration faults |
| `transient` | A confirmed abort or pre-routing refusal permits a same-key retry | `TransactionRetry`, `RequestTimeout` |
| `outcome-unknown` | Recover durable status/receipts before repeating the original command | `Unavailable`, `InternalError`, unrecognized codes, lost/undecodable responses |

No class authorizes a fresh key, bypasses authority, or proves an interrupted
financial write was absent. In particular, permanent is **not** the saved-request
terminality predicate. That owner still distinguishes immutable content failure
from repairable referenced state and can permit explicit unchanged retries after
the blocker is resolved.

## Remedy codes

The common posting owner now distinguishes `InvalidPostingLine`,
`InvalidPostingLineCount`, `DuplicatePostingLine`, `InvalidPostingSide`,
`UnbalancedPosting`, `AccountingPeriodMissing`, `PostingDateOutsidePeriod`,
`AccountMissing` and `AccountInactive`. `PeriodLocked`, `MissingEvidence`,
`ApprovalRequired` and `StaleDependency` keep their existing names and statuses.
Malformed transport values, including negative/noncanonical monetary strings,
remain HTTP 400 and now carry `InvalidRequest` rather than an empty body.

This preserves `InvalidJournal` for historical records and other invariant
refusals; it does not pretend every independently owned business validation is
a posting-line remedy or reinterpret earlier sealed codes.

PostgreSQL `40001`, `40P01`, `55P03` and `57014` identify aborted attempts and map
to `503 TransactionRetry`. Connection loss and ambiguous service failures remain
outcome-unknown. Missing database configuration and PostgreSQL authentication or
database-name configuration failures map to `503 ConfigurationError`, not a
transient retry or credential revocation. Existing safe correlated diagnostics
retain their SQLSTATE while public messages exclude credentials and SQL values.

## Transport and browser integration

The Worker preserves tagged accounting codes and recovery fields, normalizes
otherwise empty accounting HTTP failures, and emits coded pre-routing refusals.
MCP tool failures expose the same class in JSON text; protocol/authentication
errors retain JSON-RPC numbers and add machine-readable accounting metadata.
Initialization tells clients how to act on each class. Better Auth keeps its own
authentication protocol and is not restyled as an accounting endpoint.

The browser's shared failure consumer uses code classification, not prose or a
caller-supplied retry hint. The current journal draft, review and saved-request
surfaces consume the common status component. It names the remedy code and
distinguishes repair-required, known rollback and uncertain outcome in English
and Swedish. Unknown codes cannot turn a lost response into a definite refusal.
Captured inputs and saved identities remain unchanged across retries.

## Compatibility

The recovery field is optional when decoding retained old errors and saved
refusals. No decode default adds fields to a sealed body. Current emissions
include the field, and older codes can be classified in the client/read view.
The real saved-request E2E journey reads an old `PeriodLocked` refusal without
adding recovery metadata, repairs its referenced state, and checks that the
original persisted outcome was not rewritten after successful recovery.

## Proof obligations and artifacts

The independently specified failing vectors reproduced the coarse-code/missing
recovery behavior before implementation. Real PostgreSQL/workerd journeys cover
REST/MCP remedy parity, inactive accounts, locked/missing periods, invalid balance
and line side, out-of-period dates, a synthetic serialization abort, complete
rollback and original-key receipt recovery. Existing malformed-money vectors
assert the new coded transport refusal. Diagnostics exercise wrong-password and
missing-configuration behavior without exposing secrets.

Chromium exercises a real `40001` evidence-write fault, then an unknown proxy
failure, then successful same-identity recovery. The proxy supplies an unrecognized
code with a misleading transient hint; the UI still presents outcome uncertainty.
Three saved-command submissions keep the same original key. Screenshots were
inspected. Existing saved-refusal browser and immutable-history journeys also run.

Artifacts under `test-results/e2e` (older runs are archived by the harness):

- `df-10-*.json`: exact REST/MCP refusals, retry receipts and browser keys.
- `df-10-transient-browser.png`, `df-10-unknown-browser.png`: rendered states.
- `diagnostics-worker.json`, results, manifest and source-integrity records.

```sh
bun install --frozen-lockfile
bun run check:changed:full
bun run check:integration
bun run test:e2e
```

## Final verification

The final stable-source regression run passed **52 tests across seven files**:
failure recovery, diagnostics (including unreadable and stalled bodies), boundary
failures, admission, saved-posting retries, MCP authority and document reading.
It completed in 206.47 seconds without a source-integrity refusal. Exact responses,
browser screenshots, results and manifest remain under `test-results/e2e`.
`check:changed:full`, the web build and the integration declaration passed.

The attempted full-workspace E2E run exceeded its 600-second outer deadline and
is not a passing gate. Its self-host failures exposed a missing web build
prerequisite; building the web application resolved both in the final regression
run. An earlier combined run also hit a Node socket `setTypeOfService EINVAL` and
diagnostics timeout. Those runs are not delivery evidence. No expectation was
weakened to obtain the final pass. Full-workspace regression remains unverified;
the packet's real-boundary and compatibility acceptance is verified separately.

Repeat the focused proof after `bun run --cwd apps/web build`:

```sh
bun run test:e2e apps/api/tests/failure-recovery.e2e.test.ts apps/api/tests/diagnostics.e2e.test.ts apps/api/tests/boundary-failures.e2e.test.ts apps/api/tests/admission.e2e.test.ts apps/api/tests/saved-posting-retry.e2e.test.ts apps/api/tests/mcp-authority.e2e.test.ts apps/api/tests/document-reader.e2e.test.ts
```
