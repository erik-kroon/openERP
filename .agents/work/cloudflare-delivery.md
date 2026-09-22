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
| 2026-09-22 | Verification | Latest user reply says skip tests. No tests added or run. Default Cloudflare OAuth profile reports needs-reauth; account/stage/isolated database/jurisdiction remain unspecified. | Hosted proof unavailable | Refresh account authentication and select the isolated environment before live work. |
| 2026-09-22 | Stage isolation | Removed the API name override, allowing the same stage-derived naming as the web Worker. Documented separate PostgreSQL origins and existing deployment migration. | Infrastructure type check passed; no deployment | Inspect the actual deployment plan once an environment exists. |
| 2026-09-22 | Originals | Private retained R2 bucket, explicit jurisdiction, 5 MiB bound, pending upload intents, conditional writes, hash/size checks, scope recheck on retrieval; private atomic filesystem adapter for Bun. CSV interpretation retains 64 KiB bound. | Implemented; runtime unverified | Apply reviewed migration 0910 and exercise original recovery in an isolated environment. |
| 2026-09-22 | Recovery | Same-snapshot object references copied and checked into backup manifest; fenced restore compares exact database/file closure. Unknown external-pointer schemas still refused. | Implemented; runtime unverified | Exercise missing/corrupt originals; R2 re-upload and hosted read admission remain open. |
| 2026-09-22 | Jobs | Migration 0940 admits prepare-only jobs, records submitter/executor identities, fences manual changes and duplicate checkpoints. Workflow runs bounded chunks; Cron rediscovers committed admissions. REST/MCP/UI expose start and status. | Implemented; runtime unverified | Provision dedicated agent credential, deploy Workflow and exercise interruption/revocation/cancel behavior. No Queue/DO added without a producer/consumer need. |
| 2026-09-22 | Static validation | API and web type checks, infrastructure type check, focused type-aware lint and production builds passed. Earlier register-report type failures cleared as concurrent work was integrated. Wrangler dry run reported no bindings, as expected for the local configuration; this is not a hosted binding check. | Static evidence only | Record final whitespace/lint checks; do not convert build results into financial/runtime proof. |

No completion claim is made by this record. No deployment, migration execution, document upload or database operation was performed. Tests were skipped. Hosted proof, live object recovery and live durable execution remain open. See docs/operations/cloudflare.md for the operational handoff. Concurrent frontend/accounting work in this shared checkout was preserved.
