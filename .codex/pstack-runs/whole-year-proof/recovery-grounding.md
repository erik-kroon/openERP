# Recovery grounding

Read-only trace of dirty source at HEAD 50c745dfc268c51b6fa4075683d71018f0adf125. No runtime reproduction was performed. Rebind paths to the frozen baseline before implementation.

`apps/api/scripts/operations/workflows.ts` restores into a fresh quarantined database. It compares reconstructed tables, schema, migrations, roles, originals, evidence, receipts and durable work using maintenance authority. Final quarantine requires `NOT datallowconn` and connection limit zero. The restore receipt and `packages/contracts/src/operations.ts` fix applicationRecovery to blocked-restricted-read-admission. Provider progress and writer activation remain separately controlled.

`apps/api/src/application/identity.ts` invokes ordinary authority admission in `apps/api/src/db/identity.ts`. Credentials or sessions, identity admission and membership use FOR SHARE. The exact book is locked share or update. Expiry is checked after locks. Recheck repeats admission. Changing the book lock alone does not remove the read-only incompatibility. PostgreSQL read-only transactions reject locking reads. The current `db/transaction.ts` has no explicit read-only/isolation config, and `db/connection.ts` has no recovery connection mode.

Retained read owners are posting.getEvidence/getReceipt, source-retention.getSourceOccurrence, reports saved report reads, and posting-corrections correction bundle reads. Original object reads verify size/hash and recheck authority. prepareReport creates a new snapshot and is not a recovery read. getReceipt accepts execute_change receipts only.

The runtime group has substantial table writes and is not a restricted inspection role. Better Auth has mutable rate limits and session/account state despite disabled refresh on the token read. Recovery must not bootstrap ordinary writer/provider access.

`docs/operations/application-recovery.md` requires distinct inspection identity, exact restored book/environment scope, explicit DB/application read allowlists, genuine read-only native Effect/Drizzle transactions, unchanged live authority locks, blocked ordinary runtime/auth mutation/queue/provider work/other books, independent original/receipt/saved-report controls and final quarantine. Those requirements are the design constraint. Actual production custody remains open.

Existing reusable proof lives in `apps/api/tests/assurance/excellence/recovery.recovery.test.ts`, restore-host.ts and assurance/database-support.ts. The default vite config includes only *.e2e.test.ts, so the recovery test is not in the broad default gate. Existing exercise enables an ordinary login and destination Worker and therefore does not establish restricted inspection. global-setup.ts binds runtime results to source and migration hashes.

The recovery doc references historical Applied0210/0900 admission. Current owners are the TypeScript application/identity.ts and db/identity.ts. DB inventory refuses RLS policies and most role/database settings, with a narrow read-only quarantine exception. A proposed new enforcement policy must reconcile that exact inventory contract.
