# DF-06 — Shared calendar-date admission

Implemented and observed 2026-10-01 with synthetic sources, local workerd,
real PostgreSQL under the restricted runtime role, and the native Oxlint CLI.

## Failure before repair

Before production edits, public bank-workspace queries for `0000-06-15`,
`2025-02-29` and `2026-04-31` returned HTTP 500 `InternalError` instead of
HTTP 422 `InvalidJournal`. The owner checked only interval ordering before
passing dates to SQL. The native lint probe also admitted another round-trip
validator without a diagnostic. These failures are retained in E2E history.

## Delivered boundary

`packages/domain/src/values.ts` owns `CalendarDate` and `isCalendarDate`.
The real-calendar range is inclusive `0001-01-01`–`9999-12-31`, with one
schema validation message: `Enter a valid calendar date.` Company/payroll
contracts reuse the refinement. Existing application owners, document
interpretation, SEB parsing and SIE encoding use the predicate while retaining
their established failure codes and source diagnostics.

`AccountingDate` remains the deliberately loose lexical transport/storage
contract. Source occurrence retention does not interpret or rewrite original
bytes. Wrappers still return their original null/undefined/date/epoch shapes.
UTC month-end arithmetic is not date admission and remains unchanged.

The error-level `anti-slop/no-duplicate-calendar-date` rule rejects the
ISO-date round-trip comparison idiom throughout product source. It permits
exactly one comparison in the central owner and exactly the existing payroll
and VAT month-end comparisons. Another copy inside any of those files fails
too. This is a bounded idiom/count ratchet, not a claim that lint can recognize
every possible alternate implementation of a calendar validator.

## Repeatable focused proof

```sh
bun run test:e2e apps/api/tests/calendar-date-admission.e2e.test.ts
bun run test:e2e apps/api/tests/calendar-date-admission.e2e.test.ts apps/api/tests/sie-account-codes.e2e.test.ts apps/api/tests/sie-dimensions.e2e.test.ts apps/api/tests/supplier-extraction.e2e.test.ts apps/api/tests/bank-covers.e2e.test.ts
bun run check:changed
bun run check:changed:full
bun run check:integration
python3 docs/plans/check-plan.py
```

Nine focused E2E cases pass:

- `0000-06-15`, `1900-02-29`, `2025-02-29` and `2026-04-31` return
  HTTP 422 `InvalidJournal` with no financial-state change.
- `0001-01-01`, `2000-02-29`, `2024-02-29` and `9999-12-31` are admitted
  and returned exactly.
- Invalid dates inside an uninterpreted CSV remain byte-identical in the
  retained occurrence, without financial-state change.
- A new round-trip copy fails the actual native Oxlint gate. Each allowed owner
  admits one exact comparison but rejects a second.

The focused run's source-integrity status is `stable`, with matching inventory
hash `cccd95d92f548adcfaa9df4a4bff63c0d82824cc91c950c986ab4373b06068a6`.
Its archived receipts are in
`test-results/e2e-history/2026-10-01T09-55-15.465Z-0d4ada3b/`:
`df-06-calendar-admission.json`, `results.json`, `junit.xml`, the manifest
and source-integrity record. Reruns produce equivalent receipts under
`test-results/e2e` and archive older runs.

The final shorter regression run passes 32 cases across those five files,
including exact SIE bytes, original account/object identifiers, extraction
authority/replay and the real banking browser journey. Its source integrity is
`stable`, with matching hash
`b045cbaebd6b623caf9c00c31fcbd5963cc6fb826af3347348876097f0678a72`.
The normal JSON/JUnit, manifest, domain receipts and browser artifacts are retained
under `test-results/e2e`.

Both changed-file gates pass, including type-aware lint and TypeScript checks.
A separate native lint scan across application, contracts, domain and Swedish
jurisdiction source passes and finds no remaining unapproved round-trip copies.
The planning checker passes document integrity only.

## Verification limits

The checkout contains independent concurrent dependency and cash-method work;
this packet does not adopt or commit it. An initial E2E attempt failed during
database setup. Earlier broad document/SIE/banking runs were stopped at the
outer 120-second deadline and are not passing evidence. Earlier changed-file
timeouts likewise are not successes; subsequent complete gates pass.

A completed broader run observed 44 passes and two document-worker failures:
durable polling timed out, and normal self-host preparation had no succeeded
attempt. Its source-integrity guard detected concurrent changes, so neither its
passes nor its failures establish fixed-revision behavior. The later stable
32-case regression run excludes those document-worker scenarios; it does not
claim they were repaired or qualified by this date consolidation.

`check:integration` currently fails because the independent cash-method leaf
is declared deferred despite having consumers. DF-06 adds no domain leaf and
does not change that declaration; the cash-method owner must reconcile it.

No full-workspace E2E success, company qualification, live document-provider
acceptance, deployment or statutory outcome is claimed.
