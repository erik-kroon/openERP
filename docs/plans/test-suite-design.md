# Accounted test-suite map and our suite design

Status: **analysis for decision, not a test plan and not test code.** No test file was added or
run for this document. Everything below was read from source. Where a number is approximate it
says so.

Purpose: we are about to design an E2E suite for OpenERP. `accounted` (erp-mafia) is the closest
product we have, and it has a mature, real-database test suite. This document maps that suite,
separates the techniques that transfer to our stack from the ones that do not, maps the gap
against our own acceptance scenarios, and ends with the decisions that have to be made before
anyone writes a test.

## 1. Provenance

| Source | Where | State |
| --- | --- | --- |
| `accounted` clone | `/Users/admin/accounted` @ `c3ffec04a` | live, remote `erp-mafia/accounted.git` |
| 17 other reference repos | `~/.codex/worktrees/fnd01-reconciliation/openERP/references/` | live source trees, no Effect/Workers |
| `docs/references/test-suite-review.md` | same worktree | **recovered byte-exact**, sha256 `2979d3c4…` matches `docs/plans/evidence/planning-baseline.json` |

The recovered `test-suite-review.md` (58,106 bytes) is the earlier proposal from Codex thread
*Review test suite strategy* (2026-09-22). It is a **survey and recommendation**, not an
inventory, and it is now partly superseded:

- It recommends **Playwright Test as the single initial runner**. You overrode that with "use
  vitest". Do not restore it unamended.
- Its 19 reference links point at `references/…`, which does not exist in our tree.
- `docs/references/` was deleted from our repo; four files recorded in `planning-baseline.json`
  are gone (`documentation-review.md`, `design-reconciliation.md`,
  `initial-runtime-checkpoint.md`, `test-suite-review.md`).

## 2. Our current state, measured

| Thing | Count |
| --- | --- |
| E2E tests | **16**, 4 files, 1,313 LOC, `apps/api/tests/` |
| Paths they touch | `/change-sets`, `/evidence`, `/ledger` only |
| Browser tests | **0** — `apps/web/tests/` is an empty directory |
| Acceptance scenarios designed | 21 (`E-01`–`E-21`) + 12 `R-xx` invariants + 12 `I-xx` notes |
| Plan documents | 222 lines total (`verification.md` 48, `verification-strategy.md` 61, `09-acceptance.md` 85, `apps/api/tests/README.md` 28) |
| One-time evidence artifacts | 39 entries, 2.8 MB — 20 write-ups, 11 JSON, 21 screenshots, all dated 2026-09-24 |

Our suite is a **single-area posting-kernel suite**. `apps/api/tests/README.md` already states the
distinction: *"Existing local HTTP/browser proof artifacts are not recurring regression coverage.
A green kernel suite is not browser or AP acceptance."*

The five workflows refactored in `5ac3433` (sales orders, supplier credit basis, schedule
amendment, historical item admission, asset basis capture) have **zero** automated coverage.

## 3. Accounted's test architecture

`vitest.config.ts` declares three projects, each env-gated so a bare `vitest run` never touches a
database it cannot reach.

| Project | Glob | Gate | Parallelism | Timeout | setup |
| --- | --- | --- | --- | --- | --- |
| `unit` | `**/*.test.ts` (excl. `.pg.`, `.tool.`, `.next/`, `.claude/`) | — | default | default | — |
| `pg-real` | `**/*.pg.test.ts` | `DATABASE_URL` | **`fileParallelism: false`** | 15 s | `tests/pg/setup.ts` |
| `tool-pg` | `**/*.tool.test.ts` | `TOOL_PG_REST_URL` | `fileParallelism: false` | 30 s | `tests/tool-pg/setup.ts` |

Measured size:

| Layer | Files | Cases | LOC |
| --- | ---: | ---: | ---: |
| unit (`*.test.ts`) | 2,037 | ~25,000 (24.7k–27.3k by counting method) | ~498,000 |
| `tests/pg/*.pg.test.ts` | 249 (+9 harness) | 2,426 | — |
| `src/**/*.pg.test.ts` | 57 | — | — |
| `supabase/migrations/__tests__/` | 14 | — | — |
| `*.tool.test.ts` (MCP) | 4 | 16 | — |
| **total** | **2,361** | — | **~576,000** |

Baseline: 999 migrations in `supabase/migrations/`. 143 pg files use `withUserContext`; 26 use
`runAsServiceRole`.

### 3.1 The two harness pillars

`tests/pg/setup.ts` (170 lines) is the whole harness. It is worth reading in full; four decisions
in it are the reason their suite is trustworthy.

**Superuser pool for seeding, RLS only where explicitly opened.** `getPool()` connects as
`postgres`, which bypasses RLS. `tests/pg/fixtures.ts:13` says so: *"All inserts go through the
pool (superuser `postgres`), which bypasses RLS: that is intentional for seeding. RLS is exercised
only where a test explicitly opens a user context."*

**`withUserContext(userId, fn)`** — `BEGIN` → set **both** claim GUC styles → `SET LOCAL ROLE
authenticated` → **assert the simulation landed** → `fn` → always `ROLLBACK`.

```ts
await client.query(`SELECT set_config('request.jwt.claims', $1, true)`,
  [JSON.stringify({ sub: userId, role: 'authenticated' })])
await client.query(`SELECT set_config('request.jwt.claim.sub', $1, true)`, [userId])
await client.query('SET LOCAL ROLE authenticated')
const authCheck = await client.query(`SELECT auth.uid()::text AS uid`)
if (authCheck.rows[0]?.uid !== userId) throw new Error(`withUserContext: auth.uid() resolved to …`)
```

Two comment blocks explain why this is not ceremony:

> "Set both the whole-claims object and the individual `sub` claim: different versions of
> Supabase's `auth.uid()` read one or the other."

> "the CI image (`supabase/postgres:15.8.1.060`) ships the **LEGACY** auth shim, where
> `auth.role()` reads ONLY `request.jwt.claim.role` … Setting only the JSON works against
> hosted-style shims and **silently leaves `auth.role()` NULL in CI**, which is exactly the
> failure mode that broke the service-actor suites."

And the reason for the assertion itself: *"otherwise RLS policies return empty and the real test
failure points at an unrelated assertion."*

**`runAsServiceRole(fn)`** — same shape, `SET LOCAL ROLE service_role`, asserts
`auth.role()='service_role' AND auth.uid() IS NULL`, and **COMMITs on success** (their SIE
bulk-delete suites assert persisted effects over the plain pool afterwards). The commit/rollback
asymmetry is load-bearing and is used as evidence: because `runAsServiceRole` commits and
`withUserContext` rolls back, a surviving row *proves* which path wrote it.

**Schema sanity gate in `beforeAll`.** Queries `pg_trigger`/`pg_proc`/`pg_tables` for 11 named
objects (`enforce_period_lock`, `audit_log_no_update`, `commit_journal_entry`,
`user_company_ids`, `audit_log_immutable`, `journal_entries`, `companies`, `company_members`,
`fiscal_periods`, `audit_log`, `voucher_sequences`) and throws *"Did every migration in
`supabase/migrations/` apply cleanly to …?"*. A partially applied migration set produces **one
loud error**, not 249 cryptic *"relation does not exist"* failures.

## 4. Technique catalogue — what actually transfers

This is the core of the document. Each entry: the technique, the mechanics, where it lives, and
whether it survives the move to our stack.

### 4.1 Transfers directly

**T1 — RLS / authority simulation with a self-check.** `tests/pg/setup.ts`. *Transfers in spirit;
needs rework.* We have no Supabase auth shim; our equivalent is Better Auth + the runtime DB role.
The transferable core is the **assert-the-simulation-landed** step, because our equivalent failure
mode is identical: if the runtime role does not actually lack write access, RLS-dependent
assertions pass vacuously.

**T2 — The 3-way cross-tenant matrix.** `securitydefiner_write_rpc_tenant_guards.pg.test.ts`.
Every write path gets three probes:
1. **cross-tenant → refused** (and the guard fires *before* any work — a burned voucher number is
   a failure, not a detail);
2. **own-tenant → allowed** ("a guard that also blocks the legitimate path is still a bug");
3. **trusted service path → still allowed**, disambiguated *by message* when a different 42501
   fires first.

**T3 — Refusal indistinguishable from not-found.** `link-voucher-rpcs-tenant-guard.pg.test.ts`
returns `LINK_VOUCHER_INVOICE_NOT_FOUND` for a cross-tenant row, then asserts nothing was mutated.
The *state* assertion is the real test: `invoices.status` unchanged, zero payment rows.

**T4 — Prove the runtime role cannot write protected tables, by catalogue sweep, not a hand
list.** `definer-function-grants.pg.test.ts` sweeps `pg_proc` for `SECURITY DEFINER` writers and
asserts `anon` has no EXECUTE — with three details worth stealing verbatim:
- a **sanity floor** (`expect(rows.length).toBeGreaterThan(10)`) *"otherwise an empty offender list
  proves nothing about the schema"*;
- resolution through `to_regprocedure($1)` so *"a signature that drifted out of the schema fails
  on `exists` instead of silently returning NULL privileges"*;
- the key negative: a refused call must leave the **counter untouched**, because *"the refusal has
  to land before the two UPDATEs, not after one of them."*

**T5 — Ratchet plus a test of the ratchet.** `null-safe-tenant-guards.pg.test.ts` sweeps
`pg_proc.prosrc` for the raw `NOT IN (SELECT public.user_company_ids())` pattern that skips the
deny branch on NULL — and then **plants a probe function containing the pattern, asserts the
sweep now finds it, and drops it.** *"A ratchet that silently stops matching proves nothing."*
This is the single most important idea in their meta-layer.

**T6 — Expected constraint violation by SQLSTATE *and* constraint name.** Used across the suite,
e.g. `23514` + `chart_of_accounts_vat_box_check`, `42501` + `CASH_ACCOUNT_COMPANY_WRITE_DENIED`.
Asserting only the code is how "failed for the wrong reason" hides.

**T7 — `SAVEPOINT` / `ROLLBACK TO SAVEPOINT` scenario isolation.** `BEGIN` once in `beforeAll`,
`SAVEPOINT scenario` / `ROLLBACK TO SAVEPOINT scenario` per test, so an expected violation cannot
poison the transaction for the next case.

**T8 — Real concurrency via two connections and `lock_timeout`.** Not `Promise.all`. The mechanism:

```ts
const a = await getPool().connect(); const b = await getPool().connect()
await a.query('BEGIN'); await b.query('BEGIN')
await a.query("SET LOCAL lock_timeout = '500ms'")
await b.query("SET LOCAL lock_timeout = '500ms'")
// A takes pg_advisory_xact_lock(...) and deliberately does NOT commit
await expect(postOnB).rejects.toMatchObject({ code: '55P03' })   // blocked by A's uncommitted lock
await a.query('SAVEPOINT held'); await a.query('RESET ROLE')
await expect(postOnA).rejects.toMatchObject({ code: '55000' })   // own-transaction exclusion
await a.query('ROLLBACK TO SAVEPOINT held')
```

The distinction is the point: **`55P03` (lock_not_available) = someone else holds it; `55000`
(object_not_in_prerequisite_state) = your own transaction's state excludes you.** Both orderings
are tested, using `RESET ROLE` to get both branches out of one connection. Adversarial
primitives: `pg_advisory_xact_lock(hashtextextended('sie-company:' || id, 0))` and
`SELECT … ORDER BY id FOR UPDATE`. One file verifies a wait really happened via
`pg_stat_activity.wait_event_type='Lock'`.

**T9 — Migration replay and idempotency, reading the migration off disk.** `list-company-accounts.pg.test.ts`
re-runs `MIGRATION_SQL` against the live schema and asserts the RPC still works;
`account-vat-treatment-reconciliation.pg.test.ts` replays the real DDL against a
`CREATE TEMP TABLE … ON COMMIT DROP` probe and compares `pg_constraint.oid` + `pg_get_constraintdef`
before/after; backfills are run twice and asserted **byte-equal including `updated_at`**.

**T10 — Cross-language parity, in both directions.** `voucher-series-standard-default.pg.test.ts`
asserts the DB default map equals the TypeScript `STANDARD_VOUCHER_SERIES_MAP` **and** that it names
every literal the DB `CHECK` accepts, so a new source type cannot silently fall back to `A`.
`source-type-constraint.pg.test.ts` is the incident version: a value present in the Zod enum was
missing from the DB CHECK, and every "Bokför direkt" failed with 23514.

**T11 — Immutability with a *narrowed* bypass.** `document-immutability.pg.test.ts` proves a GUC
bypass still refuses the fields it must refuse. Before the narrowing, the GUC was a blanket bypass
that disarmed the trigger. Also the **bundled-change** case: `SET notes=…, entry_date=…` in one
statement is rejected whole and neither column moves.

**T12 — Fail-closed guards, with the error/verdict distinction pinned.** `period-service.test.ts`:
*"refuses to lock when the untriaged count query errors, rather than waving the lock through"*,
*"a half-run guard is no guard"*, *"the infra failure message is NOT mapped to the
unbooked-transactions code"*.

**T13 — Money-exactness including the sub-krona plug.** `match-batch-allocate.pg.test.ts`:
invoice 1000.40 paid 1000 → Cr 1510 1000.40 / **Dr 3740 0.40** / Dr 1930 1000, with
`paid_amount=1000.4`. The rounding residual is an explicit line on a named account, asserted.

**T14 — Service-actor / spoofed-identity handling.** `bulk-book-transactions-service-actor.pg.test.ts`:
a `service_role` caller passing a member's `p_user_id` commits *and attributes the voucher to that
user*; a **missing** `p_user_id` is rejected and a **spoofed** one is ignored. Their GDPR note:
*"the JWT sub is authoritative for payment-row attribution."*

**T15 — `projectRow` in mocks.** The one place a mock was upgraded to honour projections, added
*because a bug hid*: *"It used to hand back the whole fixture whatever was selected, so a route
that forgot a column the VAT rule reads still saw it and the test passed on broken code. That is
how #2783 hid."*

### 4.2 Accounted's meta-layer — the best part of their repo, and cheap for us

- **`tests/schema/no-phantom-columns.test.ts` (650 lines) + `schema-guard.ts` (~1,700).** Replays
  all migrations into a column/constraint model, then walks **every query-builder chain in the
  codebase through the TypeScript AST**, asserting named columns exist, literal filter values are
  members of the column's `CHECK` set, and `onConflict` targets a real unique set. It exists
  because a chainable mock cannot catch this class, and it names the cost: *"that blind spot kept
  article delete broken for ten days, hid sixteen more phantom-column sites, two phantom `CHECK`
  values … and one `onConflict` naming a dropped unique constraint, which raised 42P10 on every
  call."* It has shrink-only baselines, a **floor** on resolved references
  (`RESOLVED_COLUMN_FLOOR = 13_500`) — *"guards the guard"* — a **ceiling** on unresolvable
  expressions with a per-increment changelog, and ~15 self-tests of the scanner.
- **`scripts/check-pg-test-coverage.mjs`** — a PR touching a migration that changes a trigger,
  function, RLS policy or DEFERRABLE constraint **must** add or extend a `*.pg.test.ts`, or carry a
  greppable `-- pg-test: covered-by …` comment. Their own verdict on why it exists: *"Previously
  instruction-only, which means it got skipped."*
- **`scripts/checks/no-new-antipatterns.mjs` + `antipatterns-baseline.json`** — shrink-only
  ratchets over source, tracked **per exported handler** because *"a wrapped PATCH next to a
  hand-rolled DELETE in the same file is still a violation (that exact shape hid two MFA bypasses
  until 2026-08-26)"*. 602 open `naive-ore-round` findings remain — the baseline is allowed to be
  large, only to shrink.
- **Gaps they admit:** no coverage gate at all, no lint rule against `.only`/`.skip` (they simply
  have zero occurrences), and stale CI comments quoting suite sizes nobody reconciles.

### 4.3 Does not transfer

**The unit suite's mock infrastructure.** `createMockSupabase()` is a `Proxy` that answers
everything with **one** pre-set `pendingResult`:

```ts
const handler = { get(_t, prop) {
  if (prop === 'then') return (resolve) => resolve(pendingResult)
  return (..._args) => buildChain()
}}
```

`.select()`, `.eq()`, `.single()`, a misspelled `.eqq()` — all resolve to the same object. There is
no `auth`. `createQueuedMockSupabase()` improves only this: results are consumed **positionally**,
one per `.from()`/`.rpc()` at chain creation. Reordering two `.from()` calls silently reassigns
their answers.

~880 files / 10,934 cases (43% of all unit cases) drive that queue, concentrated in
`src/app/api/**` (539 files, 5,445 cases, only 8 mock-free). **That third is the part to discard,
and it is the part that looks impressive on a dashboard.** Our `verification.md` already forbids
this direction: *"No unit tests are to be added after code."*

**Two genuinely important negatives for us.** `accounted` has **no exact-money / minor-unit
layer at all** — amounts are JS `number` and Postgres `numeric`; grepping `1e38`,
`10n ** 38n`, `MAX_SAFE_INTEGER` finds only date sentinels. And **no canonical-JSON module, no
duplicate-key rejection, no Unicode normalization tests.** So for our two strongest domain
assets — 38-digit minor units and `canonicalizeJson` — accounted has nothing to copy. Our
advantage is real and must be protected by our own tests.

**Their canonicalization is a `JSON.stringify().sort()` on a fixed-key preview object** with one
order-invariance test. Ours (`packages/domain/src/canonicalization.ts`, sorts entries by key
bytes, `open-erp-c14n-v1`) is materially stronger and needs its own adversarial suite.

## 5. The `tests/pg/` map — 249 files by domain

| Domain | Files | What it proves |
| --- | ---: | --- |
| Tenancy / RLS / roles / security | 42 | A viewer cannot write; a non-member cannot see; a `SECURITY DEFINER` writer cannot be called cross-tenant; account erasure is complete |
| Bank, cash & transaction booking | 37 | Booking is atomic, anchored to the right ledger, released when its last voucher dies, never double-booked |
| Journal / voucher core (`verifikat`) | 24 | A posted entry is immutable except through named carve-outs; period locks gate every write path; series numbering is gapless and single-writer |
| Sales invoices, credit notes, quotes, orders | 24 | You cannot over-invoice an order, over-credit an invoice, or convert one quote into both an order and an invoice |
| Supplier invoices & payments | 14 | Settlement evidence, arrival numbering, overdue cron and batch payment cannot outrun the invoice lifecycle |
| External integrations | 14 | Connection rows are member-read/service-write; PEPPOL/WhatsApp ledgers are immutable and idempotent |
| Salary, payroll & employees | 12 | A booked run locks opening balances; payslip files are WORM; utlägg settle through the run, not a second voucher |
| Parties / customers / suppliers | 10 | One live party per org number per company; merge/undo/promote/undo leave a logged, reversible decision |
| Reporting & ledger read models | 10 | Trial balance, KPI and VAT totals exclude exactly the entries they promise, in numeric not float |
| VAT, moms & skattekonto | 9 | Kontantmetoden cut-offs are singly live and mirror-paired; one Skatteverket event cannot produce two vouchers |
| Dimensions, tags, templates | 8 | A dimension value referenced by a posted line cannot be deleted; retag never touches amounts |
| SIE import | 7 | Holds, leases and repair races serialize so an import cannot interleave with bookkeeping |
| Pending operations & history | 7 | Terminal states are immutable; stuck claims are recoverable |
| Arkiv (compliance knowledge base) | 7 | Facts are bitemporal and append-only; only the service writes |
| ROT / RUT | 6 | A begäran is settled once, reclaimed up to the deduction, released on reversal |
| Documents & storage | 6 | The `documents` bucket is WORM **by catalogue ratchet**, company-scoped, service-only queue |
| Assets, depreciation & accruals | 5 | A posted depreciation row cannot be deleted; register link and voucher are one transaction |
| Audit / retention | 5 | BFL 7-year retention expiry; årsredovisning version finalization; audit triggers |
| Company lifecycle & sandbox | 2 | Sandbox teardown never reaches a real tenant |

Two entries deserve their own note because they are meta-tests that generalise:

- **`documents-bucket-worm.pg.test.ts`** — sweeps `pg_policy` for any client-reachable
  `DELETE`/`UPDATE`/`FOR ALL` policy covering the bucket, **and proves the ratchet is non-vacuous
  by planting a `FOR ALL` policy and a bucketless `USING (auth.uid() = owner)` policy and watching
  the second one actually delete a real object.**
- **`full-archive-coverage.pg.test.ts`** — every `public` table with a `company_id` must be
  classified as dumped / covered-elsewhere / explicitly excluded; the three buckets are disjoint;
  classified tables must still exist; every dump query orders by columns that exist.

### 5.1 Migration and schema tests

14 files in `supabase/migrations/__tests__/`, 57 co-located `src/**/*.pg.test.ts`. The
higher-leverage ones:

- **`no-phantom-columns`-style replay onto a temp probe.** Reads the migration off disk,
  `.replaceAll('public.chart_of_accounts', 'pg_temp.vat_constraint_probe')`, compares
  `pg_constraint` before/after.
- **`legal-form-profiles.pg.test.ts`** — asserts the SQL `supported_entity_types()` list equals the
  TypeScript `ENTITY_TYPES` array, then per form seeds the chart and asserts the expected account
  numbers are present. Cross-language parity over a *set*, both directions.
- **`seed-chart-of-accounts.pg.test.ts`** — 24 account names asserted **byte-for-byte with
  å/ä/ö**, plus an encoding tripwire: `octet_length(account_name) > char_length(account_name)` on six
  accounts, because *"if a future regression strips å/ä/ö again the lengths would become equal and
  this fails loudly."* Header explains why it exists: *"The engine and the VAT-rutor mapping both
  route by account number, so a mislabel in this function never breaks any other test … This test
  is the canary."*
- **`commit-actor.pg.test.ts`** — asserts every pre-existing 2-arg/4-arg call shape is
  byte-identical after adding actor columns.
- **`source-type-constraint.pg.test.ts`** — `it.each` over the Zod enum against the DB `CHECK`.

### 5.2 What they do NOT test, and it matters to us

- **No checksum-drift refusal test, and structurally cannot be one.** They apply migrations with
  raw `psql` in filename order, so no version+checksum ledger is written; grepping the repo for
  "checksum" finds only prose about SIE `#KSUMMA` CRC-32. **We do have this**
  (`persistence.e2e.test.ts`: "migration rerun preserves posted state and checksum drift stops the
  migrator"), so this is a gap we have already closed.
- Their `pg-upgrade` CI job reads migrations from the **merge-base tree**, not the working tree, so
  "a PR that EDITS a shipped migration … still gets the original applied here, so the edit shows up
  as a failure below."

### 5.3 The MCP / `tool-pg` project

4 files, 16 cases. Real `supabase-js` against a real PostgREST, kept separate from `pg-real`
because *"that project holds a `pg` Pool and writes SQL, which cannot see the half of a tool that
PostgREST resolves: the `.select()` column strings, the resource embeds, the `or=(...)` grammar."*
A worthwhile idea: it is the only layer that can catch a malformed PostgREST filter, which is
invisible to both mocks and raw SQL.

## 6. The other 16 references — what is worth what

Three facts that reframe the question, all verified across the whole tree:

1. **No repo here uses Effect.** `grep -rl 'from "effect"'` over every `.ts` in `references/`
   returns nothing. There is **no Effect Layer/Service/Schema pattern to copy.**
2. **No repo targets Cloudflare Workers.** No `wrangler*` anywhere; `midday`'s `apps/worker` is a
   Bun/BullMQ process.
3. **Only `midday` uses Drizzle; only `bigcapital` ships Playwright. No repo combines Playwright
   with real Postgres. There is not one concurrency/serialization/deadlock test in all 16**
   (`SERIALIZABLE`, `SKIP LOCKED`, `deadlock` → zero hits in any test file).

So the value in that tree is **domain truth and measurement discipline**, not stack-shaped
architecture. Take the former.

| Rank | Repo | Value | Take |
| --- | --- | --- | --- |
| 1 | `gredor-frontend` | Very high | Bolagsverket K2 calculation linkbase as JSON (`src/data/taxonomy/k2/2021-10-31/calculation.json`) — the arithmetic oracle for the whole statement set; `src/data/taxonomy/k2/2021-10-31/sieMappings.ts` (~1,200 derived BAS-range → XBRL mappings, *generated* with an explicit exclusion list, not hand-maintained); `src/util/sieUtils.ts:360` `fixSumsAndCheckForRoundingErrors` with a **two-tier** warning (rounding error vs missing account mapping); `cypress/fixtures/input/gredor/README.md` — six **negative fixtures named by error class** (`avrundningfel`, `ogiltiga-underskrifter`, `verksamhetsar-datum-saknas`, `verksamhetsar-fel-intervall`, `utan-datering`, `utan-orgnr`), each with a dedicated assertion; `cypress/e2e/xbrloutput.cy.ts:145` golden-XML comparison that **normalizes volatile ids** so the diff tests facts, not generated identifiers |
| 2 | `accounted-bench` | Very high | `scripts/selftest-ledger-env.ts` — the **oracle self-test**: seeds a known-bad state, asserts each assertion program **fails** on it, then simulates the correct action and asserts it now passes. *"Proves the oracle can actually detect failure (a harness whose invariants never fire will happily report every model as compliant)."* Also `src/ledger-tasks.ts` end-state **balance** assertions rather than transcript grading, chosen so *every account not named must net to zero*; `src/ledger-env.ts:44` **fresh tenant per trial instead of a shared reset**; `scripts/freeze.ts` SHA-256 over the task set so gold edits are a visible diff event; `src/aggregate.ts` `isHarnessError` (a run that never reached the model is *not run*, not *failed*) |
| 3 | `swedish-accounting-skills` | High | `data/bas-2026-accounts.json` — 1,283 BAS 2026 accounts (cross-check against `accounted-bench/vendor/bas/` and `sie-parser`'s CSV for a free chart-divergence test); `scripts/check_skills.py` fails CI if any account number cited in prose is not in the chart, with an annotated allowlist — the cheapest portable drift guard we could adopt; SIE **4C (2025-08-06)** record types and a severity-classified validation table; ÅRL 1:3 § thresholds; SRU/INK2 field tables; VAT and invoice rule references |
| 4 | `midday` | High | `packages/db/src/test/calculations-e2e.test.ts` (3,016 lines) real-Postgres E2E where **test names are arithmetic statements** (*"January: R1(5000) + R2(4400) + R3(2000) + FX1(2500) + FX2(1650) = 15550"*) with the FX-fallback SQL written out in a comment; `helpers/seed.ts` fixed UUIDs + `SEED_REFERENCE_DATE` + `setSystemTime`; `transaction-matching.golden.test.ts` golden dataset **validated for well-formedness in `beforeAll`** with an `id`-keyed exception list; `providers/fortnox.test.ts` (930 lines) asserting the **exact outbound** call, including broken-fiscal-year handling. Read `packages/db/src/test/reports.test.ts` as the counter-example: 1,896 lines of in-memory mocks proving nothing about SQL |
| 5 | `beancount` | High | `parser/cmptest.py` `assertEqualEntries(expected_text, actual)` — the expected value is **a short piece of the domain's own text**, and failure output is a **set diff** ("present in expected and not in actual"), not a repr dump; entries in assertions may not use interpolation and any parse error raises `TestError("Unexpected errors in expected")`. `core/interpolate.py:97` `infer_tolerances` — tolerance inferred from the quantization precision actually used in the postings; `:72` `compute_residual`; `ops/balance.py:24` balance assertions get **twice** the multiplier. `ops/validation.py` — validations are plain composable functions, and `validate_check_transaction_balances` runs *after* plugins because *"unbalancing input is legal, as those types of transactions may be 'fixed up' by a user-plugin"* — the parses-but-is-wrong seam, drawn correctly |
| 6 | `arelle` | High, narrow | `ValidateXbrlCalcs.py:139` — **do not compare values, compare value intervals**: derive each fact's interval from its lexical form and `decimals`, sum the children's intervals, and flag when the intersection with the reported fact's own interval is empty. Plus **unreported contributing items** — concepts in the arc with no fact at that context, which catches a filing that is self-consistent but silently omits a line. `tests/integration_tests/validation/test_conformance_suites.py` asserts an **exact set of validation-code suffixes** per document (`actual == expected`); a valid document expects `[]`. This is the right shape for E-16/E-18 |
| 7 | `unified-accounting-api` | Medium | `tests/api/pipeline.test.ts` — stub `fetch`, drive the **real** app, assert **both** the upstream request and the canonical response; the Fortnox case-sensitivity trap asserted explicitly (`toContain('lastmodified=')` / `not.toContain('lastModified=')`). `src/providers/types.ts` provider-abstraction flags worth inventorying: `yearScoped`, `modifiedFilterStyle: 'param' \| 'odata-filter'`. `src/types/dto.ts` `AmountType { value: number }` is a **float** — read as a counter-example |
| 8 | `fortnox-mcp` | Medium | Cleanest MCP tool design in the tree, zero tests: `.strict()` schemas with domain refinements (`rows.min(2)` "debit must equal credit"); `annotations: { readOnlyHint, destructiveHint, idempotentHint, openWorldHint }` on every tool; traps documented **in the tool description** (*"the financial_year parameter uses Fortnox sequential IDs (1, 2, 3…), NOT calendar years"*); `response_format: 'markdown' \| 'json'` for token efficiency. Plus a vendored `fortnox_api.json` |
| 9 | `byrokrat-accounting` | Medium | `integrations/Sie4/parserdata/` — **53 real SIE files from named vendors** (Fortnox, Visma, Mammut, Norstedts, Bokslut) plus hand-made single-feature files, and 5 **sidecar `.assertions` files**: fixture and expectations as one reviewable unit, so a file with no assertions is a smoke test and one with assertions is a semantic test. Vendor this corpus into our fixtures |
| 10 | `account-financial-tools` | Medium | OCA modules: `account_spread_cost_revenue/tests/test_compute_spread_board.py:105` — 12 monthly lines, `83.33` for eleven and `83.37` for the twelfth, every date asserted, **"the residual cent is absorbed in the last period"** stated as the policy. `account_journal_lock_date` — a **two-level** period lock (`fiscalyear_lock_date` vs `period_lock_date`; a group manager is governed only by the former, everyone else by the max), refusing `write` *and* `button_cancel`, with `bypass_journal_lock_date` as the escape hatch and a role-escalation test that strips the group and asserts both refusals. That maps directly onto our "lock authority before the book, then periods/accounts" |
| 11 | `sie-parser` | Low-med | Dead parser, but vendors the **authoritative artifacts**: `SIE4 spec/SIE_filformat_ver_4B_ENGLISH.txt` (the official 39-page spec in English — the completeness checklist for any SIE reader) and `Kontoplan-BAS-2025.csv`, which carries the SIE-Gruppen markers **`|`** changed/added, **`*`** konteringsinstruktion changed, **`■`** in the minimal set. Those two markers are in no plain account list and are exactly what a booking-suggestion engine needs. Also: check whether we implement `#KSUMMA` (CRC-32 control total) |
| 12 | `bigcapital` | Low | **Dead end, and mildly dangerous.** 59 supertest e2e files of `POST → 201`, `GET → 200`; **not one accounting assertion in the entire e2e suite**; `jest.retryTimes(3)` set globally as a flakiness mask — copying that would be a regression; MariaDB with per-tenant databases, the architectural opposite of ADR 0010. Its Playwright `e2e/global-setup.ts` (sign up → create org → **poll until the async build settles** → persist `storageState`) and `AGENTS.md` "Key gotchas" section are worth reading |
| 13 | `erpnext` | Low | **No Swedish localization in this tree** — `erpnext/regional/` has australia, italy, south_africa, turkey, uae, us; Sweden lives in a separate `l10n_se` app that is not vendored. 526 test files all requiring a live Frappe site; no concurrency tests. One stealable idea: `test_gl_entry.py:14` `test_round_off_entry` — a sub-krona residual must land **explicitly** on the round-off account, never silently vanish |
| 14 | `compliancemaxx` | Low | An OSS-license/ISO-27001 scanner. Nothing in it knows what a voucher is; its 8 Vitest files test tool-output parsers. Only a generic finding-schema/SARIF pattern |
| 15 | `claude-for-swedish-small-business` | Low | Prompt markdown. Two dense domain checklists, the rest is sales copy |
| 16 | `gredor-backend` | Very low | Kotlin/JAX-RS. Two vendored Bolagsverket OpenAPI specs |
| 17 | `sie4` | None | A 241-line PHP SIE4 *writer* base class from ~2010 |

## 7. Gap analysis against our own scenarios

Our `E-01`–`E-21` are broader than accounted's coverage in one direction and narrower in another.

| Our scenario | Accounted analogue | Our automated coverage | Highest-value model |
| --- | --- | --- | --- |
| E-01 authority | 42 tenancy files | **partial** (one test) | T2 3-way matrix, T3 indistinguishable refusal |
| E-02 exact money / precision | none — they have no exact-money layer | **yes** (one test) | nothing to copy; protect our advantage |
| E-03 plan → post → receipt | posting kernel | **yes** | — |
| E-04 replay / concurrency | `same-key replay` | **yes** | T8 (we lack true lock-based concurrency) |
| E-05 rebooking vs legitimate duplicates | — | **no** | T6 |
| E-06 staleness after approval | `security-role-gates` | **partial** | T14 |
| E-07 readiness vs posting race | — | **no** | T8 |
| E-08 failure/rollback/recovery | `persistence.e2e` | **yes** | — |
| E-09 correction & reversal | `linked reversal` | **partial** | T11, `test_round_off_entry` |
| E-10 read snapshots under competing commits | — | **no** | T8 |
| E-11 REST/MCP parity | `mcp.e2e` | **partial, no real client** | `tool-pg` project separation |
| E-12 repeat/overlapping import | 7 SIE files | **no** | T8, `sie-observer-concurrency` |
| E-13 partial payments, installments, FX | `match-batch-allocate`, `accrual-schedules` | **no** | T13, OCA spread test |
| E-14 year transition / opening basis | `opening-balance-replacement` | **no** | T9 |
| E-15 coverage / reconciliation | 37 bank files | **no** | — |
| E-16 filings, snapshots, lineage | `arkiv-*` | **no** | arelle conformance-suite shape |
| E-17 recurring rules, delivery | `pending-operations-*` | **no** | T5 |
| E-18 SIE / iXBRL semantics | `sie-artifact-scan`, `ValidateXbrlCalcs` | **no** | **arelle intervals + unreported-items** |
| E-19 provider unknown/pending | — | **no** | `unified-accounting-api` both-directions test |
| E-20 worker failure, migration baseline | `persistence.e2e` | **yes** | their merge-base upgrade job |
| E-21 restore / obsolete writer | — | **no** | — |

**Zero coverage:** E-05, E-07, E-10, E-12–E-19, E-21 — 11 of 21 scenarios. That is the real
number, and it lines up almost exactly with the five workflows `5ac3433` refactored.

## 8. Design implications

1. **Keep one runner, and it should be Vitest.** We already run Vite+/Vitest. `accounted` uses
   three Vitest projects; the same three-way split maps onto us as
   `unit`-free / `pg-real` / `mcp`. No case for Playwright as a second runner *yet* — the browser
   gate in `verification-strategy.md:53` is unsatisfiable today regardless of runner, and
   `bigcapital`'s `global-setup.ts` is the only browser-harness pattern in the references worth
   copying when we get there.
2. **Our harness needs the four things `tests/pg/setup.ts` has and we don't:** an
   assert-the-simulation-landed check, a schema/migration sanity gate in `beforeAll` (we have
   `check:infra` but nothing in-suite), a superuser-vs-runtime-role split stated in a comment, and
   explicit serial execution.
3. **Adopt `accounted-bench`'s oracle self-test as the shape of every E-scenario.** For each
   scenario: assert the guard fires on a known-bad state *before* asserting the happy path. This
   is compatible with our `verification-strategy.md:33` requirement to *"Demonstrate that a
   deliberately wrong expectation fails, without weakening product validation."*
4. **Adopt a freeze tripwire on the scenario corpus.** Hash fixtures + expected outcomes; fail CI
   on drift. We already have the instinct — `planning-baseline.json` records sha256s — but nothing
   enforces them.
5. **Adopt the migration-coverage gate.** A change to a migration that alters a trigger, grant or
   constraint must add or extend a case, or carry a greppable escape comment.
6. **Two domains need techniques, not ports.** For E-18, arelle's *value-interval* comparison plus
   *unreported contributing items* is the only rigorous answer we have for "parses but is wrong."
   For E-16, the conformance-suite shape (exact expected set of defect codes per fixture) fits our
   21-scenario discipline.
7. **Our two unique assets need adversarial suites nobody can give us:** 38-digit minor-unit
   arithmetic and `canonicalizeJson`. accounted has no equivalent because it does not have the
   problem. `beancount`'s domain-text expected values and set-diff output are the right ergonomics.
8. **Name negative fixtures by error class**, as `gredor` does, rather than by scenario number.

## 9. Open decisions

| # | Decision | Recommendation |
| --- | --- | --- |
| D1 | Restore `docs/references/test-suite-review.md`? | Restore it **byte-exact** (verifiable against `planning-baseline.json`) but with a status header recording that its Playwright recommendation was superseded by your Vitest decision, and that its 19 reference links are dead. Also decide what to do about the three sibling files it tracked that are also gone |
| D2 | Restore the `references/` tree into our repo (18 repos, ~700 MB)? | No. Cite paths in the Codex worktree instead. If we need the artifacts — K2 taxonomy JSON, BAS CSVs, SIE 4B spec, the 53-file SIE corpus — **copy those specific files** into our fixtures with provenance, not the repos |
| D3 | First implementation slice | The 5 refactored workflows, because they are unverified and already committed. Start with `credit-basis.ts` (4 profiles × a long guard sequence) and `sales-orders.ts` (the write path) |
| D4 | Do we add a `pg-real`-style project, or extend the existing 4 files? | Extend, but split the harness out of `apps/api/tests/` first. 16 tests in 4 files with all harness inline in `support/` will not absorb 100+ cases |
| D5 | Unit tests at all? | No, per `verification.md:7`. Adopt only the **parity** tests (T10) and the pure-domain ones with no mock dependency — those are not "tests added after code", they are drift guards |
| D6 | Browser suite now or later? | Later, and it is the larger piece. The gate is currently unsatisfiable; flag it rather than half-build it |
| D7 | Who owns the E-scenario expected values? | They must be **independently specified** before implementation (`verification.md:7`, `verification-strategy.md:27`). Not derived from our own calculator. This is the hardest constraint and the easiest to violate under time pressure |

## 10. What this document does not establish

- No test was written or run. No claim here is a passing run.
- The `tests/pg/` per-file invariants for roughly 200 of 249 files were read from test titles plus
  mechanical technique scans, not full reads. They are title-faithful; their assertion details are
  unverified.
- Suite-size figures for `accounted`'s unit project differ by counting method (24,703 `it(`/`test(`
  call sites vs 27,317 by line-anchored match). Treat ~25,000 as approximate.
- Nothing here establishes that *our* refactored code is correct. It establishes what to test and
  with what technique.
