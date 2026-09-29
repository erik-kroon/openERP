# NEXT-34 mileage reimbursement leaf review

Baseline: `16a532c`, with `packages/domain/src/mileage-reimbursement.ts`
unchanged from blob `dbf401dfe8eaa755a234a299ad8504f98e33434f` (353 lines).
Scope is this evidence file and `next34-probe.ts` (217 lines, taken from
`review/next34-mileage` at `f6117a2` with a type-only fixture correction:
`ownershipKind` uses the reviewed `private_car` literal, the required
`previousRevision: null` is supplied, and the stray `overlappingTripIds`
inside `TripRevision` was removed — overlapping ids were already passed
correctly in `PrepareAwardInput`. Runtime behaviour is unchanged.)
No domain source, migration,
application, contract, route or test file was changed.

**No application consumer exists.** `grep -rn "mileage-reimbursement |
calculateMileage | prepareTripAward | replayTripAward | correctTripAward"
apps packages jurisdictions` returns only the domain leaf and the probe.
This is domain verification against the public schema and function surface.
It is **not** a provider, HTTP/MCP, database, posting or UI journey, and it
is **not** statutory compliance evidence for any reporting period.

## Failure contract recorded before source changes

The probe pins the obligations a mileage owner must satisfy. The leaf
already satisfies them, so no repair was made.

```bash
EXPECT_REPAIRED=1 bun next34-probe.ts
```

Result: **11 passed, 0 failed**.

1. A0: the owner surface `calculateMileage`, `prepareTripAward`,
   `replayTripAward`, `correctTripAward` is present.
2. A1: 70 km at 2.50/km is 17500 entitlement; the 1.50/km ceiling is 10500
   exempt and 7000 taxable; the parts conserve the entitlement.
3. A2: an unreviewed route refuses at award time with
   `IncompleteTripFacts`. The pure split is math; a suggestion never
   becomes an award.
4. A3: a trip missing a required vehicle identity refuses with
   `IncompleteTripFacts`; no private-car default is assumed. The same
   holds for a missing fuel payer.
5. A4: award preparation seals two disjoint source identities, one for the
   exempt component and one for the taxable component.
6. A5: a second award key over the same trip refuses with
   `DuplicateTripClaim`; no second award is minted.
7. A6: an overlapping trip claim for the same economic travel refuses with
   `OverlappingTripClaim`.
8. A7: a taxable component without a payroll owner refuses with
   `TaxableWithoutPayroll` instead of falling back to direct payment.
   A `direct_payment` route with a taxable component refuses the same way.
9. A8: replaying the identical command key returns the existing plan; a
   different key over an awarded trip refuses with `AlreadyAwarded`.
10. A9: a correction after the handoff is consumed returns a delta carrying
    the original award reference and a lawful recovery basis; without that
    basis it refuses with `RecoveryBasisMissing`. Before consumption it
    returns a replacing award; it never edits the award.
11. A10: negative distances and rates are unrepresentable in the unsigned
    minor-unit schemas rather than signed surprises.

## Why this stays deferred

`docs/plans/domain-leaf-integration.json` keeps `mileage-reimbursement` at
`deferred`: the packet keeps the payroll handoff with the claim/payroll
owners. Concretely:

- the exempt component hands off through the NEXT-33 employee-claim owner,
  which is itself deferred and has no application owner;
- the taxable component needs a payroll mileage-award owner that persists
  the trip revision, rule release and award plan, creates one payroll
  instruction referencing the existing entitlement liability, and never
  expenses the award twice.

No such owner exists in `apps/api/src/application/payroll`,
`apps/api/src/application/payroll-foundation.ts` or elsewhere. Wiring the
leaf to the wrong owner to clear the check would be false delivery.

No migration was landed. A `0036-next-34-mileage.sql` draft (trip
revisions, rule releases, award plans — 75 lines, blob
`2e6d754ae60d7b0fbf17496df778a908e378a259`) is preserved on the
`review/next34-mileage` branch as `2256e19` with the message "Draft
NEXT-34 mileage tables, not for main: no owner consumes them yet". It is
intentionally not merged: tables without an owning transaction are dead
DDL. The future owner picks it up from that commit, reviews it against
the then-current `payroll_employees` key and grant baseline, and lands it
in the same merge as the application/db/contract/route/E2E files.

## Not proven

- No provider, HTTP/MCP, database, transaction, posting, payroll or UI
  journey was run. There is no consumer to run one against.
- The `exemptSourceIdentity` / `taxableSourceIdentity` values are
  `${awardId}-exempt` / `${awardId}-taxable` distinct strings, not retained
  records. Exclusivity of the handoff, once-only award identity under
  concurrency, and reconciliation of claim totals to exempt liability plus
  taxable payroll instructions are caller duties and are unproven here.
- The packet's accrual profile (taxable entitlement recognised at award
  time, payroll debiting the existing award liability rather than wage
  expense again), the bank-payable-or-payroll exclusivity, retained handoff
  and cancellation evidence, and the corrected-run payslip/declaration
  preservation are unimplemented and unverified.
- Separate parking/toll receipts, non-ceiling exemption profiles, and any
  recognition policy other than the first supported accrual profile refuse
  or are absent; they are not proven here.
- Not statutory compliance, and not evidence for any reporting period.

Only this evidence file and the probe were added. No dependency, shared
export, application persistence, test file or external operation was added.
The leaf is ready for integrator review; packet integration and any runtime
journey remain open.
