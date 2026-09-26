# Application-owned replacement: review repairs

2026-09-25. This records repairs and local verification of the reviewed replacement work. It does not close the complete replacement or clean-baseline gates in ADR 0010. The working tree continued changing during verification; this is not acceptance evidence for an immutable release revision.

## Fixes present

- Saved-request save and execution enforce the operator-only command boundary. Refused commands roll back their savepoint and release it once, preserving the refusal receipt.
- Correction execution rejects disabled approvers rather than enabled ones.
- FX execution retains command receipts in the financial transaction. Fully settled items report `settled`; correction checks compare the economic lines while preserving sealed line IDs. Account dependencies are matched by ID. Settlement snapshots retain remaining original units and carrying value.
- Runtime grants cover the FX and supporting slices. Permission probes distinguish reads, inserts and column updates; payroll pointer updates are limited to `revision_id`. SQL text arrays use array constructors rather than Drizzle tuple interpolation.
- Journal insertion checks each ordinal against the immutable expected count. One deferred parent check verifies count and balance; redundant per-line aggregate triggers are removed. Account dependency reads are batched.
- Queue dispatch survives enqueue defects, derives the same record ID as effect-mq, rearms failed deliveries within a retained-attempt budget, and stops exhausted or cancelled deliveries without changing an advanced checkpoint. Queue and application pools use their required date parsers. Preparation writes take the book write lock during admission, and progress audit entries retain the advanced cursor.
- CSV preview, reparse and admission, recurring activation, closing inventory/approval, and VAT fact/basis/history operations have application implementations. CSV admission writes the statement and observations in its caller's transaction instead of invoking `import_bank_statement`.
- VAT draft preparation accepts the current v3 calculator. Its captured basis includes fact and expense-source withdrawals; withdrawn sources must remain excluded. Draft retrieval compares the saved basis with the live basis.

## Verification

No test files were added or edited. The existing `bun run test:e2e` suite passed all 23 tests across four files against workerd and a fresh PostgreSQL database, including the new migrations. Full typechecking and lint were run; their logs and final targeted checks are retained with the artifact below.

Additional manual checks used a separate disposable PostgreSQL database and the restricted runtime role:

| Scenario | Observed result |
| --- | --- |
| FX recognition, full settlement and correction | 10,000 EUR minor units carried at 110,000 SEK minor units; 112,000 settlement retained a 2,000 gain. Correction restored the open amounts. |
| Partial FX settlement and correction | 4,000 original units released 44,000 carrying units against 45,000 cash. Remaining original units were 6,000; correction restored 10,000. |
| FX retry and account ordering | Same-key and concurrent retries returned one receipt. Different account versions did not create false stale dependencies. |
| Saved refusal | An unbalanced journal produced a retained `refused` result; retry returned the same result. |
| Saved authority command | An agent could not save an authority command through the ordinary endpoint or run an admin-seeded authority request. No approval was created. |
| Maximum voucher | 500 lines committed with debit and credit totals of 25,000 each. An attempted later line at ordinal 501 was rejected. The local execution took about 80 ms; this is not a throughput benchmark. |
| Source intake | Retain, preview, reparse, approve, admit and exact-key replay returned successful HTTP responses. Admission retained one statement and its observations. |
| Recurring activation | An operator activated a reviewed simulation for the admitted source. |
| Closing | Inventory declaration and approval of a reopen proposal succeeded. The locked-period setup was an explicit fixture change, not a claim that the entire close journey passed. |
| VAT | Fact recording, basis, history, v3 draft preparation and draft readback succeeded. Draft readback reported the current basis. |
| Queue outage and exhaustion | Denying queue INSERT caused logged dispatch failures. Restoring the grant allowed the same live process to enqueue again. Five retained attempts were rearmed; fifteen retained attempts stopped the domain job. These fault fixtures ran with the queue paused. |
| Real preparation worker | The Bun runner completed an admitted job and retained an unposted proposal requiring separate approval. Further runs exercised recovery of that proposal and concurrent deliveries; see `runner-outcomes.json`. |

Artifacts are saved in `test-results/replacement-review/`: command logs, the existing E2E result/manifest, sanitized manual HTTP responses, database observations, queue outcomes and a source-file hash manifest. The directory is ignored by Git; this document is the maintained summary. `/tmp/openerp-repair-proof/` contains the original local captures.

## Repeating the checks

1. Run `bun run check-types`, `bun run lint` and `bun run test:e2e`. The existing suite creates and removes its own database and writes `test-results/e2e/`.
2. For the additional checks, provision a disposable synthetic book using `apps/api/scripts/provision.ts`, with operator and agent credentials and accounts for cash, receivables, revenue, FX gain and FX loss. Run workerd with a login granted only `openerp_runtime`.
3. Retain evidence and exercise the FX review/approval/execution HTTP routes with the amounts above. Repeat execution using the identical idempotency key, including concurrent requests. Read item state after settlement and correction and compare retained receipts and balanced vouchers.
4. Save an unbalanced journal, run it twice and compare the refused outcomes. With an admin fixture, retain an authority request owned by the agent and attempt ordinary execution as that agent; expect `Forbidden` and no approval.
5. Prepare and execute 500 balanced lines. Attempt ordinal 501 as the runtime role in a transaction and verify rejection/rollback.
6. Retain a CSV with `Date,Description,Amount,ID` and one row `2026-09-25,Synthetic payment,100.00,repair_row_1`. Preview and reparse with explicit UTF-8/LF/comma settings, 0 opening and 10,000 closing minor units. Approve/admit as the operator and replay the admission key.
7. Propose, simulate and activate a recurring rule matching that observation. Create a preparation run, admit background work, and start `bun run jobs:preparation` with an agent executor credential. Verify completion, one retained proposal, no voucher, and matching run/audit cursors. Repeat with concurrent runs over the same observation.
8. On the disposable database only, pause the preparation queue and seed failed delivery histories at five and fifteen attempts. Run dispatch and inspect retry/stopped outcomes. Temporarily revoke queue INSERT, restore it, and observe subsequent dispatch in the same process. Restore permissions and stop the fixture processes afterwards.

## Remaining acceptance work

At the time of this pass, the old migration chain, SQL dispatch registry and feature functions remained. The [follow-up review](application-owned-review-followup.md) records subsequent dispatch removal and additional repairs. Other replacement modules still contain unsupported operations. The three-file baseline, complete caller removal, browser journeys, restore qualification and release-revision concurrency/failure coverage remain open. This repair pass does not establish actual-company accounting applicability or production readiness. The complete multi-voucher correction bundle was source-checked here; the existing E2E reversal case is not proof of every bundle scenario.
