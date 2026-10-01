# DF-08 — Locked-period financial admission

Implemented and observed 2026-10-01 through normal local workerd HTTP and disposable
PostgreSQL using synthetic fixtures. No company data, external provider or statutory
action is involved.

## Failure before repair

The existing posting owner and `commerce/register.ts` already check current period
locks. A synthetic before-insert fault then set the referenced period to locked
after those checks. Before production edits, both public commands returned HTTP
200: a new voucher, and an invoice anchored to a previously posted recognition
line. `period-lock-integrity.e2e.test.ts` failed both independently expected
409 / `PeriodLocked` assertions.

## Delivered boundary

`0046-period-lock-integrity.sql` adds after-insert integrity on `vouchers` and
`commerce_invoices`. It locks the book, resolves the exact referenced accounting
period (through the retained recognition voucher for invoices), and locks that
period before inspecting `locked`. A missing period refuses `InvalidJournal`;
a locked one refuses `PeriodLocked`. SQL failure cannot become an open-period
success. The helper has a fixed search path and no public execution grant.

All financial posting owners insert through the voucher table. Supplier/customer
recognition anchors use the common commerce invoice register. Existing Effect
transactions, tx-passing persistence, shared accounting errors and REST/MCP/UI
consumers therefore reach the guard without another financial workflow or a new
transport contract. Original-source retention does not create a financial anchor
and is not blocked by this migration.

The guard is prospective. Historical vouchers remain valid when their period is
subsequently locked. A committed receipt can still be replayed after locking;
this performs no new financial insert. There is no bypass parameter. The trusted
runtime keeps its existing lock-column grant because the adopted close/approved
reopen owner requires it. SQL does not authenticate an operator or replicate the
application approval lifecycle; a compromised trusted backend remains outside
the accepted integrity guarantee in ADR 0010.

## Repeatable proof

```sh
bun run test:e2e apps/api/tests/period-lock-integrity.e2e.test.ts apps/api/tests/admission.e2e.test.ts apps/api/tests/financial-close.e2e.test.ts apps/api/tests/cash-method.e2e.test.ts apps/api/tests/persistence.e2e.test.ts apps/api/tests/boundary-failures.e2e.test.ts
bun run check:changed:full
python3 docs/plans/check-plan.py
```

Observed: 26 tests pass across six files. Both final-write faults return the
authentic 409 / `PeriodLocked`. Financial counts, invoice registration, command
receipts and the fault's own lock mutation roll back. Removing the fault lets
the original request key succeed. Locking afterward preserves exact committed
receipt recovery and leaves counts unchanged.

Existing locked-period admission, authority/tampering refusal, financial close,
approved reopen, delta reclose, single opening, zero-delta close, cash-method
relabelling refusal and migration rerun/checksum checks all pass.

During integration, concurrent DF-10A work landed as `18688c5`. The existing
duplicate-key admission assertion still expected only a message and caused two
broader runs to fail despite successful DF-08 cases. Commit `dc00b69` aligned that
assertion with the adopted exact `InvalidRequest` / `permanent` envelope; it did
not loosen the assertion. The final integrated run above passes. Failed runs are
not passing evidence.

The full changed-file gate passed with the DF-08 test and admission assertion.
A later pre-commit full-gate attempt also selected a newly added concurrent DF-09
test and failed on its spacing rules; the DF-08 file passed lint/types. That
separately owned test was not altered, and this later run is not a green global
gate. The local E2E harness archives earlier runs under `test-results/e2e-history`
when another run replaces the active artifact directory.

Artifacts: `test-results/e2e/df-08-vouchers.json`,
`df-08-commerce_invoices.json`, suite JSON/JUnit, migrations log and source inventory.

## Limits

This is synthetic local admission-time integrity, not company reopening policy
or statutory qualification. It does not make period locks irreversible, prevent
a compromised application from clearing them, or retroactively invalidate earlier
postings. A privileged cross-transaction maintenance race is not separately
exercised; normal financial/closing application paths retain their shared book
barrier. No new global full-suite result is claimed for this revision.
