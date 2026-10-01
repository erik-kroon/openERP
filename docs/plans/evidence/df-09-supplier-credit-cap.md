# DF-09 — retained supplier-credit aggregate capacity

Implemented and observed 2026-10-01. Forward migration
`0047-supplier-credit-cap.sql` adds the narrow retained aggregate invariant.

## Corrected finding and ownership

The current application already checks remaining supplier-credit capacity and
serializes book writes. The original claim that its public command can credit
an invoice repeatedly without refusal is too broad. A final-write fault that
inflated the second partial credit produced a later schema failure and rollback,
not a demonstrated successful over-credit. The missing SQL invariant still
left that write to be detected indirectly as `InternalError`.

The new AFTER INSERT guard checks the final retained values, locks the book then
the original supplier invoice before summing, and refuses `InvalidJournal` when
the aggregate exceeds the original gross amount. Every retained credit counts:
there is no nullable cancellation status to interpret or exclusion to guess.
Partial credits and equality remain valid. Financial compilation, current
authority, approval and allocation remain application-owned.

Migration preflight refuses existing excess rather than rewriting history.
The runtime cannot update the original amount or mutate retained credits under
its reviewed grants. The guard's public message carries no original figures.
Maintenance users who disable safeguards remain outside this guarantee.

`invoice_cancellations` is the separate full-cancellation workflow: its receipt
uses the original invoice amount, so its one-to-one cap is not the partial-credit
model and was not changed.

## Observed acceptance

A real synthetic supplier draft is accepted as a `10000` invoice. Credits `6000`
and `4000` consume it exactly. Injecting one additional minor unit into the
second retained credit refuses `422 InvalidJournal`, rolls back financial state,
and permits the same execution key after fault removal. Two reviewed competing
credits of `6000` yield one success and one stale-state refusal, with one retained
credit totaling `6000`, not `12000`.

Eleven real PostgreSQL/workerd E2E cases pass across this journey, existing
paid/unpaid supplier-credit/refund behavior and persistence/migration replay.
Full changed-file lint/types pass. The migration was applied by the disposable
harness; no production migration or company data was used. Browser, hostile
administrator and direct simultaneous SQL insert proof are not claimed.

```sh
bun run check:changed:full
bun run test:e2e apps/api/tests/supplier-credit-cap.e2e.test.ts apps/api/tests/supplier-refund-journey.e2e.test.ts apps/api/tests/persistence.e2e.test.ts
```

Artifacts: `test-results/e2e/df-09-supplier-credit-cap.json`,
`df-09-credit-race.json`, results, manifest and source-integrity records.

## Broader run limitation

A later full E2E run observed 207 passing assertions across 57 files, but exited
with failure because nine source inputs changed during execution. That run is
**not fixed-revision evidence** and is not a passing integration gate. The
focused observations above remain the delivered proof; the broader run cannot
replace a stable-source rerun.
