# Cash commercial-document period repair

Delivered on clean branch `codex/cash-period-admission` at `85898f4c2cfbd710826caeed7e96bbe3b7fe0407` in `/Users/admin/.codex/worktrees/cash-period-admission/openERP`. Base is `b72a463beb5246f9cc805fce62106af10d294456`. No push, PR, merge, deployment, real data or live provider action occurred.

The application-owned commercial cash invoice could not admit because the invoice recognition trigger looked up a voucher even for its explicitly valid null-recognition variant. New forward migration `0048-cash-invoice-recognition-period.sql` recreates only that trigger with `WHEN (NEW.recognition_voucher_id IS NOT NULL)`. The function, voucher trigger, constrained invoice variants and historical migrations are unchanged. No commercial document-period policy was added.

## Changed files and commits

- `apps/api/tests/cash-invoice.e2e.test.ts` adds the independently specified locked commercial-period admission and malformed nullable-row refusals. Commit `0c59dbb` precedes implementation.
- `apps/api/migrations/0048-cash-invoice-recognition-period.sql` contains the four-line forward repair. Commit `5c12de580fa6c4cfc74fc03e68e0a566cf422d25` is the runtime-verified implementation revision.
- `docs/plans/evidence/cash-commercial-period-admission.md` retains the bounded maintained evidence and repeat command. Commit `678da2c962e43542a66b7d98e6730b14eeb9239c` adds only this documentation.

The new migration SHA-256 is `9997994f777c091bfb668c24af3283d4b7cc49a147a71e236983f1d93034fee2`. Direct diff inspection confirmed no changes to the baseline, 0043 or 0046 migration bytes. There was no exact historical migration inventory in the focused test owner to revise.

## Failure expectations before code

The E2E additions preceded the migration. They require HTTP 200 admission in a locked document period, gross 125000, outstanding 125000, retained draft, null recognition, population version 1 and unchanged replay. Admission must produce zero vouchers, journal lines, purchase recognitions, purchase tax facts, cash lines, cash recognition rows and voucher counter.

Four malformed insert variants must return SQLSTATE 23514 from `commerce_recognition_shape` with only the valid invoice retained. They cover ordinary null recognition, a cash invoice missing its draft and each mixed null/nonnull recognition pair. Existing DF-08 must still refuse final voucher and recognized-invoice writes with HTTP 409 PeriodLocked and full rollback. Existing year-end/close sealing assertions remain unchanged.

The first red reproduction is retained in `test-results/cash-period-red-20261001`. The complete test-first commit was also run in `test-results/cash-period-test-first-red-20261001`, with stable source integrity. Both fail at the real HTTP admission before recognition.

```text
{"_tag":"AccountingError","code":"InvalidJournal","message":"The journal is invalid. Review the posting details."}
- Expected
+ Received
- 200
+ 422
Tests  1 failed | 5 skipped (6)
```

## Gate results

| Gate | Status | Retained evidence |
| --- | --- | --- |
| Fresh `bun install --frozen-lockfile` | PASS, exit 0 | `test-results/cash-period-gates-20261001/install.log` |
| `check:changed` after final test edit | PASS, exit 0 | `check-red-ready.log` |
| `check:changed b72a463...` after migration | PASS, exit 0 | `check-fixed.log` |
| `check:changed:full b72a463...` | PASS, exit 0 | `check-full.log` |
| Final `check:changed:full b72a463...` | PASS, exit 0 | `check-final-full.log` |
| `check:integration` | PASS, exit 0 | `integration.log` |
| Seven-file focused PostgreSQL/workerd E2E | PASS, 50/50, exit 0 | `test-results/cash-period-fixed-20261001/results.json`, `junit.xml`, `manifest.json` |
| Fixed-source integrity | PASS, stable, no changed paths | `source-integrity.json` |
| `git diff --check b72a463...` | PASS, exit 0 | Final command observation |
| Clean working tree | PASS | Final `git status --short` returned no entries |

Gate log paths without a directory above are under `test-results/cash-period-gates-20261001`. Initial fast lint identified new test symbol names and spacing. Those local errors were fixed before the migration; their first failed outputs remain in the gate directory. No timeout or financial assertion failed.

The fixed run passed these unchanged owners.

| E2E file | Passing cases |
| --- | --- |
| cash-invoice | 6 |
| cash-payment | 8 |
| cash-year-end | 12 |
| cash-credit | 14 |
| cash-register-report | 5 |
| period-lock-integrity | 2 |
| persistence | 3 |

```text
Test Files  7 passed (7)
Tests  50 passed (50)
Duration  53.61s
```

`cash-commercial-period-admission.json` proves the direct positive case and all four SQL constraints separately from financial qualification. `df-08-vouchers.json` and `df-08-commerce_invoices.json` prove preserved period guards. The focused payment/year-end/credit/register cases passed their literal monetary assertions, stale membership, backdated discovery, empty-year review and complete close receipt gates. Persistence passed migration replay and checksum-drift refusal. Expected injected HTTP 500 failures in rollback tests passed their assertions and are not service qualification failures.

## Decisions and principles

- Model the Domain kept the existing recognized and commercial-only invoice variants and made the trigger predicate match the recognized variant.
- Fix Root Causes changed the repair boundary to the faulty trigger rather than inventing a period field or weakening its function.
- Test Behavior, Not Implementation required real HTTP admission and direct PostgreSQL constraint observations with literal amounts and error codes.
- Sequence Work into Verifiable Units put the test-first commit before the migration and preserved stable red and green artifacts.
- Prove It Works required real disposable PostgreSQL/workerd, retained source inventories and migration receipts, and the focused owners instead of a type-only claim.
- Separate Before Serializing Shared State kept writes in the assigned worktree and serialized all checks and E2E runs.

The independent review accepted the migration and requested the proof-only correction recorded below. The completed review is `/Users/admin/openERP/.codex/pstack-runs/whole-year-proof/baseline-trail-review.md`.

## Exact follow-up

Integrate the four local commits after accepting the narrow proof correction. Freeze the corrected integrated source and repeat the unchanged broad whole-year E2E run with a new artifact directory. The 50 focused passes establish this repair and preserved boundaries; they do not establish broad integrated whole-year qualification, statutory support or company applicability. There is no owned financial blocker from this focused run.


## Independent-review proof correction

Final source is `85898f4c2cfbd710826caeed7e96bbe3b7fe0407`. The additional local commit changes only `apps/api/tests/cash-invoice.e2e.test.ts`. It replaces hard-coded artifact flags and expected refusal codes with the actual replayed invoice, observed population rows before and after replay, the observed locked-period row, and sanitized values caught from each database refusal. The same recorded values must pass the existing literal expectations before serialization. No migration, financial expectation, source fixture or product implementation changed.

The prior 50/50 result remains evidence for implementation revision `5c12de580fa6c4cfc74fc03e68e0a566cf422d25`. It is not claimed as a full-suite result for the new proof source.

The final source passed the one relevant locked-document E2E case with five unrelated cases skipped. Its fresh artifact directory is `test-results/cash-period-observed-proof-20261001`, and its manifest names the final source SHA. `source-integrity.json` reports `stable` and no changed paths. The actual artifact records `documentPeriod=[{locked:true}]`, both population versions `1`, equal original and replayed invoices, four caught SQLSTATE `23514` refusals naming `commerce_recognition_shape`, and the unchanged literal zero financial counts and counter.

```text
Test Files  1 passed (1)
Tests  1 passed | 5 skipped (6)
Duration  5.33s
```

`check:changed 678da2c...` and `check:changed:full 678da2c...` both passed with exit 0. Logs are `test-results/cash-period-gates-20261001/check-proof-fast-final.log` and `check-proof-full.log`. The narrow E2E log is `observed-proof.log`. `git diff --check` passed, and the final working tree is clean. Initial proof-edit lint spacing failures are preserved and were corrected before the passing gates.

Prove It Works changed the artifact to retain observations rather than expected constants. Test Behavior, Not Implementation kept each observed refusal bound to the literal required database code and constraint. The accepted migration and broad integrated follow-up remain unchanged.
