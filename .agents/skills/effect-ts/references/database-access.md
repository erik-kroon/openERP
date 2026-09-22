# Drizzle with Effect 4

OpenERP uses `drizzle-orm/effect-postgres` with `@effect/sql-pg` and `pg`. Reuse the `Database` service and `databaseLayer` in `apps/api/src/db/connection.ts`. The checked pairing is Drizzle `1.0.0-rc.5-169397b` with Effect and `@effect/sql-pg` `4.0.0-rc.112`; inspect installed signatures before changing it.

Drizzle is the query layer. PostgreSQL still needs to be provisioned and configured separately. Installing the package or defining a table does not create a database.

Better Auth is a Promise SDK boundary: use its official Drizzle adapter with `drizzle-orm/node-postgres` and the shared `acquirePostgres` resource in `src/better-auth.ts`. Do not pass the native Effect database to an adapter that awaits Promise queries. Its auth tables live in `src/db/auth-schema.ts`; application accounting queries still yield the native Effect database.

## New queries

- Yield Drizzle queries directly inside Effect workflows. Do not wrap native Effect queries in `Effect.tryPromise` or call `Effect.runPromise` inside a transaction.
- Use `db.select`, `db.insert`, `db.update` and `db.delete` with owned table mappings when the database role permits those operations. The synthetic provisioning script shows typed inserts.
- Use the parameterized `sql` template for named accounting transitions. Bind every request value; never interpolate it with `sql.raw`, `sql.identifier` or string concatenation.
- Decode function results with shared Effect Schema contracts. A TypeScript result annotation does not validate database output.
- `db.transaction((tx) => Effect.gen(...))` owns one connection and commits or rolls back the complete Effect. Use `tx` throughout the callback; do not start another runtime or independent connection within it.

## Resources, values and failures

- Construct the connection layer within the request or CLI invocation. Never memoize the first request's Hyperdrive binding or keep Worker sockets in global state.
- Preserve scoped cleanup, connection and statement timeouts. Interruption closes the owned connection; do not assume a lost response proves that a financial command rolled back. Recover through its persisted idempotency receipt.
- Keep SQL query logging and caching disabled: bound parameters include credentials and accounting content. The production Hyperdrive binding must also disable query caching.
- The adapter leaves date/time parsing to Drizzle. Use string-mode date columns for accounting dates, exact strings for numeric money and bigint/string representations for database integers beyond JavaScript's safe range. Never use number-mode numeric money columns.
- The installed native Effect driver returns rows, including in raw execution mode; it does not return node-postgres's `{ rows }` wrapper. Prefer explicit `"objects"` mode for function results.
- Drizzle wraps SQL failures in `EffectDrizzleQueryError`, whose cause contains an Effect Cause and then a `SqlError`. Follow `queryFailure` in `apps/api/src/database.ts` to recover intentional domain errors. Never return or log the wrapper's SQL or parameters.

## Database authority

The runtime role may execute approved accounting functions but cannot write accounting tables. Using Drizzle does not change that authority. Permission checks, lock order, balanced posting, idempotency receipts and durable state remain governed by the business operation rules and database constraints.

The table mappings in `src/db/schema.ts` cover direct maintenance queries. They are not the complete database definition. Checked-in SQL setup owns DDL, grants, triggers and accounting functions, and `scripts/migrate.ts` applies it using Drizzle transactions. Do not run `drizzle-kit push` against these partial mappings or create a second migration ledger.
