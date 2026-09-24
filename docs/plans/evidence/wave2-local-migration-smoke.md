# Wave 2 local migration smoke — 2026-09-24T08:32:00Z

This is an isolated local PostgreSQL 17.11 schema check, not a financial, browser, concurrency, legal or provider acceptance result. The working tree was dirty and contains concurrent work; this artifact does not identify a committed revision.

## Repeatable procedure

1. Initialize and start a **new isolated** PostgreSQL cluster with `initdb -D <tempdir> --auth=trust --no-instructions` and `pg_ctl -D <tempdir> -o "-p <free-port>" -l <log> start`.
2. Create an empty `openerp_wave2` database. Set `DATABASE_ADMIN_URL` to its direct maintenance URL.
3. From the repository root run `bun run --cwd apps/api db:migrate` twice.
4. Query `SELECT count(*) FROM public.openerp_migrations` and stop the isolated cluster.

## Observed

- First migration run: exit 0; all 120 `.sql` migrations applied, including 6900, 7000, 7100, 7110, 7120, 7200–7202, 7300, 7400 and concurrent 7500.
- Second run: exit 0; all 120 migrations reported `already applied`.
- Receipt count: 120. No database fixtures, API requests or financial transitions were exercised.
- Earlier worker attempts hit migration syntax errors in 4000/6100; the current dirty tree had changed those files before this isolated full-chain run. Their final review and applied-checksum compatibility remain separate gates.
