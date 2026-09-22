# Initial runtime checkpoint

Observed on 2026-09-22, following the maintained documentation checkpoint `52bd1117` and the initial accounting commit `e5fe3e69`. This records a manual development observation, not an automated test suite or production acceptance. No test files were added.

## Scope and environment

The public REST API ran in local workerd through Wrangler 4.136.2, with compatibility date `2026-09-22` and `nodejs_compat`. PostgreSQL was 17.11 (Homebrew). The database was newly initialized, isolated, loopback-only and contained only the explicitly synthetic book from [`examples/synthetic-book.json`](../../examples/synthetic-book.json). Requests used a random, locally provisioned operator token. No real bookkeeping, provider or company data was used.

The maintenance connection used the cluster owner. The Worker connected as `openerp_app`, a login role granted `openerp_runtime`. It did not use the maintenance connection.

The working tree was changing concurrently during the observation. The source was not a fixed release artifact. The migration hashes below identify the database functions actually applied; this checkpoint cannot certify all code at `e5fe3e69` or the eventual final working tree. Repeat the complete verification scenarios against a fixed revision before closing a phase.

## Observed result

The expected journal was specified before the requests: debit `account_bank` by `12500` minor SEK and credit `account_clearing` by `12500`, dated `2026-09-22`, series `A`, with no tax treatment. The expected initial sequence and voucher number were both `1`.

| Operation                                               | Result                                                                                                                                                     |
| ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| List books and read book setup                          | HTTP 200; only the synthetic workspace was returned, with explicit unsupported-production and tax/report blockers.                                         |
| Retain text evidence                                    | HTTP 200; immutable evidence identity and SHA-256 returned.                                                                                                |
| Prepare, validate and approve the journal               | HTTP 200 for each operation; validation and approval matched the sealed proposal digest.                                                                   |
| Execute after applying the current forward migrations   | HTTP 200; voucher number `1`, sequence `1`, durable receipt.                                                                                               |
| Read ledger                                             | Bank debit/balance `12500`; clearing credit `12500`, balance `-12500`; sequence `1`. All amounts remained strings.                                         |
| Recover receipt by execution key                        | HTTP 200; same receipt, voucher, digest and sequence as execution.                                                                                         |
| Four concurrent repetitions of the successful execution | Four HTTP 200 responses with the original receipt identity. This covers concurrent replay of an already committed operation, not competing first attempts. |
| Reuse the execution key with a different approval ID    | HTTP 409, `IdempotencyConflict`.                                                                                                                           |
| List books without identity                             | HTTP 401, `Unauthorized`.                                                                                                                                  |
| Request another book using the operator token           | HTTP 403, `Forbidden`.                                                                                                                                     |

The execution key was `proof-execute-0001`. The durable receipt was:

```json
{
  "id": "receipt_0e6c0cfd178e4e45918f688512cac28e",
  "changeSetId": "change_a8c7d087ba9b4e7f94b337ad3dbb5fd6",
  "voucherId": "voucher_cdf079765a864cbe9822ae1bdddca8c6",
  "planDigest": "sha256:67a3b5917768d3fc7cf6c979b110decbe190ccc095ad3ff058828bdf7c6211ab",
  "sequence": "1",
  "voucherNumber": "1",
  "committedAt": "2026-09-22T14:31:10.445588Z"
}
```

A subsequent maintenance read found one voucher, two journal lines, one execution receipt, one outbox row and one consumed approval. The book's committed sequence was `1`. There were zero connections with application name `open-erp-api` at that read; this is evidence of cleanup after these successful requests, not cancellation or failed-connection coverage.

## Failures retained in the record

The first migration attempt failed at the `voucher_body` function's `row` argument. The migration transaction rolled back. A concurrent source correction renamed the argument to `voucher`; the next migration succeeded. Do not attribute the initial failure to a successful migration.

The first execution returned HTTP 500, `InternalError`. At that point the database contained zero vouchers and zero execution receipts. Applying the newly available `0003` and `0004` migrations allowed the same execution request and key to succeed. Those migrations adjust deferred balance-check privileges, ledger query binding and reversal-source binding. This observation did not independently isolate which change accounted for each failure.

The live Worker also temporarily failed to rebuild while an import's target file was being created concurrently. This is another reason the run cannot certify a fixed revision.

| Applied migration                      | SHA-256                                                            |
| -------------------------------------- | ------------------------------------------------------------------ |
| `0001-accounting.sql`                  | `0d8f9853c9f5d69804221602f13739c42268726361d7040727bf07deaad5fa9d` |
| `0002-posting-action-binding.sql`      | `e343c433850bf8476c473aaa70e2a071f12fe769ef0b8e8a1cc7f3b95d91e9ee` |
| `0003-deferred-balance-and-ledger.sql` | `8ddd0d717d983c68936fa3b4fbd84d26baa221bdf76288d5773f20ca54712aac` |
| `0004-reversal-source-binding.sql`     | `d4423f760b70c0b1440b8275a68a9f64f408c2e1e03d3bd233b8681ab32eabde` |

Rerunning the migration command reported `0001` and `0002` as already applied before applying `0003` and `0004`. A full no-op rerun of all four was not observed in this checkpoint.

## Repeating the observation

Use a fresh isolated PostgreSQL instance, a free loopback port and a new database. Do not point these commands at an existing company database. PostgreSQL tools must be on `PATH`. The paths and ports below are those used for this observation; choose new ones when reproducing it.

```bash
initdb -D /tmp/openerp-ledger-proof.GRi8jJ/data --no-locale --encoding UTF8 --auth trust
pg_ctl -D /tmp/openerp-ledger-proof.GRi8jJ/data \
  -l /tmp/openerp-ledger-proof.GRi8jJ/postgres.log \
  -o '-p 15439 -h 127.0.0.1 -k /tmp/openerp-ledger-proof.GRi8jJ' start
psql postgres://admin@127.0.0.1:15439/postgres -c 'CREATE DATABASE openerp_proof'

# From apps/api; the initialized cluster owner was admin in this environment.
DATABASE_ADMIN_URL=postgres://admin@127.0.0.1:15439/openerp_proof bun run db:migrate
psql postgres://admin@127.0.0.1:15439/openerp_proof \
  -c 'CREATE ROLE openerp_app LOGIN; GRANT openerp_runtime TO openerp_app;'

# Supply OPENERP_ACCESS_TOKEN securely in the process environment, without logging it.
DATABASE_ADMIN_URL=postgres://admin@127.0.0.1:15439/openerp_proof \
  bun run db:provision ../../examples/synthetic-book.json

bun x wrangler dev --local --ip 127.0.0.1 --port 18788 --inspector-port 19239 \
  --var DATABASE_URL:postgres://openerp_app@127.0.0.1:15439/openerp_proof
```

Use `Authorization: Bearer <local token>` and `Content-Type: application/json` on requests. Use a distinct stable `Idempotency-Key` for each mutation, retaining the execution key for replay and receipt lookup. Do not save the token with evidence artifacts.

The book URL is `/api/v1/entities/entity_synthetic/books/book_synthetic`. Retain text evidence at `POST /evidence`, then submit the following at `POST /change-sets`, replacing the evidence ID with the returned identity:

```json
{
  "kind": "manual_journal",
  "evidenceId": "<returned evidence ID>",
  "eventKey": "proof-movement-0001",
  "accountingPeriodId": "period_synthetic_2026",
  "postingDate": "2026-09-22",
  "series": "A",
  "description": "Synthetic bank movement",
  "rationale": "Prove exact review and posting boundary",
  "taxAssessment": "not_applicable",
  "lines": [
    {
      "accountId": "account_bank",
      "debitMinor": "12500",
      "creditMinor": "0",
      "description": "Synthetic bank debit"
    },
    {
      "accountId": "account_clearing",
      "debitMinor": "0",
      "creditMinor": "12500",
      "description": "Synthetic clearing credit"
    }
  ]
}
```

Post `{}` to `/change-sets/<id>/validate`. Post the returned `planDigest` and `version: 1` to `/change-sets/<id>/approvals`. Post those same values plus the returned `approvalId` to `/change-sets/<id>/execute`. Read `/ledger` and `/receipts/<execution-key>`. Compare exact ledger amounts and receipt identities with the expectations above. Newly generated IDs, digests and timestamps will differ between fresh runs.

Inspect the durable tables through the maintenance connection and confirm the counts stated above. Stop the Worker process launched for the observation, then stop only its PostgreSQL cluster:

```bash
pg_ctl -D /tmp/openerp-ledger-proof.GRi8jJ/data stop -m fast
```

## Open gates

This is partial evidence for [E-01, E-03, E-04 and E-20](../verification.md). It leaves competing first executions, agent approval refusal, stale dependencies, corruption attempts, cancellation, commit-response loss, restart, correction and transport parity unverified. It does not establish approval by a real human identity provider.

The current draft uses separate debit/credit strings while [ADR 0002](../adr/0002-exact-posting-and-approval.md) selects side plus minor units for posted lines. Resolve that contract discrepancy deliberately; this checkpoint does not silently amend the ADR. Reversal alone does not establish the planned atomic reversal-plus-replacement correction. An all-book ledger total does not establish the explicit OpeningSet and fiscal-period report semantics.

The browser workflow, MCP adapter, source drill-through, accessibility, complete P0/P1 gates and later company-specific phases require their own evidence. Keep those gates open even when static checks pass.
