# Cloudflare delivery

Objective: isolate stages; verify the hosted web → API service binding → uncached Hyperdrive → PostgreSQL path; expand retained evidence through R2 with access/hash/restore controls; connect durable preparation to an execution mechanism while preserving PostgreSQL authority and idempotency. Production/company readiness remains separate.

## Failure scenarios before implementation

- Stages resolve to the same Worker or share database credentials; reject any claim of isolated environments without distinct resources and origins.
- A build passes while deployed assets, login cookies, service binding or Hyperdrive fails; exercise the public web origin with a synthetic book.
- A posting response is lost or retried; recover the same receipt with one voucher/sequence/outbox effect and immediate fresh reads.
- A browser session or membership is revoked; later reads and commands fail without returning retained content.
- An oversized, interrupted or hash-mismatched upload is admitted; reject it before committing a reference.
- Object storage succeeds but reference commit fails; preserve a discoverable orphan, never a financial reference to missing bytes.
- Cross-book object identifiers disclose bytes; authorize using the database before accessing the store.
- Backup/restore omits a referenced object or restores corrupt bytes; fail completeness and retain diagnostics.
- A job starts before its database admission commits, or enqueue fails afterward; PostgreSQL intent and rediscovery preserve work.
- Duplicate delivery, workflow restart, expiry or stale execution repeats a preparation effect; checkpoint and idempotent identities converge.
- Job authority is revoked, cancelled or blocked; infrastructure cannot silently resume or post accounting entries.

## Decisions and evidence

| Date | Unit | Decision / observation | Status | Next action |
| --- | --- | --- | --- | --- |
| 2026-09-22 | Baseline | Existing user changes include domain SQL/docs; retain them. API has a fixed physical name; Alchemy's installed WorkerName implementation returns explicit names unchanged. | Observed | Remove the override and check infrastructure types. |
| 2026-09-22 | Verification | Asked for E2E-change approval under AGENTS.md and the account/stage/isolated database/jurisdiction details. No live resource mutation yet. | Pending user input | Prepare independent implementation; do not infer deployment settings. |
| 2026-09-22 | Stage isolation | Removed the API name override, allowing the same stage-derived naming as the web Worker. Documented separate PostgreSQL origins and existing deployment migration. | Implemented, unverified | Run infrastructure type check. |

No completion claim is made by this record. Hosted proof, R2 and durable execution remain open.
