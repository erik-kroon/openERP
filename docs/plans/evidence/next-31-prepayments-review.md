# NEXT-31 invoice-linked prepayments and accrued-cost true-up: wiring and runtime review

Date: 2026-09-29. Packet: [NEXT-31 invoice-linked prepayments and accrued-cost true-up](../../specs/next-26-50/packets/NEXT-31.md). Scope of this record: what was built, what was actually executed, and what remains unobserved. It is not a company, statutory or provider claim.

## What changed

| File | Role |
| --- | --- |
| `apps/api/migrations/0039-next-31-prepayments.sql` (new) | Recognition-to-schedule link, accrued costs and accrual resolutions, with narrow grants |
| `packages/contracts/src/prepayments.ts` (new) | Link, record, resolve and read contract; the `prepayments` API group; the read-only agent capability |
| `packages/contracts/package.json`, `api.ts`, `capabilities.ts` | registers the subpath, the group and the capability |
| `apps/api/src/db/subledger/prepayments.ts` (new) | Tx-passing reads and DML, plus the privilege probe for the three new tables |
| `apps/api/src/application/subledger/prepayments.ts` (new) | The owner: cost-basis link, accrual record, invoice resolution, derived read |
| `apps/api/src/application/subledger/schedules.ts` | exports `withSubledgerBook`, `readBook`, `requireScheduleAccess`, `digestValue` so this owner reuses the released access control rather than copying it |
| `apps/api/src/transport/http/routes/prepayments.ts`, `application/capabilities/prepayments.ts` (new) | HTTP handlers and the read-only capability |
| `apps/api/src/index.ts`, `application/capabilities/index.ts` | registration |
| `apps/api/tests/prepayments.e2e.test.ts` (new) | Three E2E cases over real HTTP |
| `docs/plans/domain-leaf-integration.json` | `prepayments` moved from `deferred` to `wired` |

`bun run check:integration` passes at **30 wired, 18 declared deferred, 48 leaves**, up from 29.

## The deferral was stale

The declared reason was *"Packet keeps schedule and invoice resolution with the subledger/commerce owners"*, and the unblock was *"A subledger owner persists a schedule and calls this leaf for allocation"*. That owner has existed for some time: `subledger_schedules`, `subledger_schedule_revisions` and the released `createSchedule` / `prepareScheduleOccurrence` / `reviseSchedule` operations. The packet's own line says it should *"Reuse application/subledger/schedules.ts and controls.ts"* — which is what this does.

**No second scheduling engine was written.** The schedule, its revisions and its occurrences stay exactly where the released owner put them. The three new tables record only two things the released owner could not express: which purchase recognition a deferral belongs to, and which invoice resolved an accrued cost.

## Three decisions the owner makes, and refuses

1. **The cost excludes deductible input VAT, and that is recorded rather than implied.** Deferring changes when accounting expense is recognized; it never moves a VAT tax point, so no tax fact is created. Every basis carries `taxTreatment: "no_tax_fact_defers_expense_timing_only"`, and the E2E case asserts `vat_fact_components` is still empty after the whole flow.
2. **A residual is a computed difference, never a plug.** The true-up is `actual − consumed`, signed in the direction of the error. The E2E exercises both directions: an exact match (`trueUp "0"`), an underestimate (`"+500"`) and the remaining capacity always `original − consumed`, recomputed from the retained resolutions rather than carried on the accrual.
3. **One invoice resolves an accrual once, bound to the invoice's own identity** rather than to a command key. Re-presenting `invoice_001` under a fresh command key still collides, and the owner returns `IdempotencyConflict` *before* touching the unique key, so the refusal is typed rather than a constraint error.

Two further refusals are load-bearing. A deferral naming a schedule that does not exist is `NotFound`, because capacity with no occurrence behind it is not a deferral. And an invoice describing a *different* service is `StaleDependency`: silently combining two services' costs is the failure this exists to prevent.

## What the runtime actually showed

Three cases over real workerd, real PostgreSQL 17.11 and the restricted `e2e_runtime` role:

| Case | What was observed |
| --- | --- |
| Cost basis | 12000 over two daily-weighted periods split `5950` / `6050`, the residual on the designated last installment, and the two halves summing to exactly 12000. A second basis over the same schedule refuses. A basis over a non-existent schedule is `NotFound`. |
| Accrual and resolution | 10000 accrued, then resolved by an 8000-consumed invoice leaving 2000, then by a 2000-consumed invoice at 2500 actual leaving 0 with `trueUp "+500"`. The same invoice twice refuses, a different service identity refuses, and the two resolutions' consumed amounts sum to exactly the original. `vat_fact_components` is empty. |
| Over-consumption | 9000 consumed against 5000 remaining is `ApprovalRequired`, and the refusal rolls back: the accrual still reads 5000 remaining with no resolution. |

The full suite passes alongside it: **167 tests across 41 files**.

## Corrections made during the build, recorded because they change what the code claims

- **Two writes, one command key, one transaction.** The accrual's own receipt and its prepared journal both used the caller's idempotency key and collided on `command_receipts_pkey`. The journal now takes a key derived from the command key, the actor and the operation, exactly as the released schedule owner does for its occurrences.
- **The prepared journal was being discarded.** `recordAccruedCost` prepared a change set and then dropped it, so the accrual had no traceable journal. `accrued_costs` now carries `change_set_id` with a foreign key, and the accrual is explicit that its journal is *prepared, not executed* — the accrual exists before its journal is approved, as every prepared posting in this repository does.
- **The leaf's failure codes were wrong in the owner's map.** The map carried `PeriodOutOfRange`, `DuplicatePeriod`, `UnsupportedAllocation` and `StaleBasis`, which the leaf does not define, and missed the four it does. With `satisfies` over the leaf's own union, a code it does not define can no longer be written.
- **The prepared journal command key was the wrong field.** The released owner takes `input`, not `command`; a copy-paste of the wrong shape compiled only because nothing checked it.
- **The access gate did not cover the new tables.** `requireScheduleAccess` probes the schedule tables only. The owner now additionally probes its own three, so a role without them refuses at the gate instead of on the first write.

## Deliberate omissions, stated rather than smoothed over

- **The schedule's own occurrences are untouched.** This owner links a recognition to a schedule and resolves an accrual; it does not post a schedule occurrence, and it did not take over the released owner.
- **The posted vendor invoice is not imported here.** The resolution names the invoice's retained identity and evidence and carries the amounts the invoice stated. It does not create a supplier document, a payable register row or a VAT return line, because those belong to the purchase and VAT owners.
- **A negative tax amount and an actual cost below zero are refused by the leaf**, and the owner maps them rather than second-guessing them.
- **No UI, no agent write capability, and no real-company or statutory qualification.** The only agent surface is a read of what remains and how it was resolved.
