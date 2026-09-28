# Overnight packet review and integration

The user requested review, improvement and merge of the overnight Muse Spark
implementations, with coordinated packet ownership and explicit approval for
focused regression tests/fixtures. Source presence and reported vector runs are
not evidence that an application journey is complete.

## Integration queue

| Scope | Owner | Current review disposition |
| --- | --- | --- |
| Main/origin reconciliation and document reading | Integrator, Herdr `wB:p19` | Merged into local main through `77d5ab1` and `7c4defb`, retaining remote `c859d9b` and reviewed guard repair `26ba496`. Builds/full static gate and affected runtime scenarios pass; detailed run scope below. |
| NEXT-07 | Integrator | `398c213` adds the paid-credit/refund journey. Follow-up repairs the bounded source identity for uppercase/Unicode/128-character document numbers in both credit paths; six HTTP cases and static gates pass. Cash-source/correction limits remain in the [evidence note](evidence/next-07-review.md). |
| NEXT-37 | Integrator review queue | Agent committed `c828603`; residual bridge/adopted-match journey passes. New-assessment posting still refuses and must be completed; the whole packet is not verified. |
| NEXT-05, NEXT-24 | Review queue | Committed source at `cc726bb`, `bac876c`; packet-specific financial journeys remain unverified. Earlier worker has closed; review before claiming complete support. |
| NEXT-23 | Integrator | `a03aca4` repairs thirteen findings plus the independently discovered prior-year opening drift. [Real HTTP proof](evidence/next-23-review-repair.md) covers close/reclose/approved reopen, raw openings, current authority, rollback and replay. Combined NEXT-07/37 gate passes. |
| NEXT-18 | Integrator | Five confirmed leaf defects repaired; before/after public-domain probes and both changed-file gates pass. [Evidence](evidence/next-18-leaf-review.md). No current valuation application caller exists. |
| NEXT-30 | Integrator | Adopted clearing receipts/refunds and consumed-principal reversal repaired; [domain probes and static gates](evidence/next-30-leaf-review.md) pass. No application consumer exists. |
| NEXT-38 | Integrator | Separated paid/recognized/credited coverage, selected an explicit gross-conserving component policy, preserved credit-adjusted state and strengthened history/membership checks. [Thirty domain probes and static gates](evidence/next-38-leaf-review.md) pass; application integration remains open. |
| NEXT-39 | Integrator review queue | Independent source/schema probes found signed-value rejection, reversed dispute signs, amount-only/under-scoped identities, unqualified payout fees, journal validation and replay-effect identity defects. Leaf remains unconsumed; repair before integration. |
| Other overnight leaves | Unassigned review queue | Maintain existing leaf-only status until inspected against the packet and real owners. |

## NEXT-18 failure obligations, before repair

- A complete mixed AR/AP population must post each item to its owned control
  account. Two `110000 → 115000` items require AR debit/gain credit `5000` and
  AP credit/loss debit `5000`, not offsetting both control entries in AR.
- Approved membership `[A@1, B@1]` must reject current membership `[A@1, A@1]`.
- A target above the 38-digit minor-unit bound must fail even when its delta is
  still within the bound. With `M=10^38−1`, `Q=M`, carrying `M` and rate `2/1`,
  target `2M` cannot be published as valid.
- Original scale 3 and book scale 2 are valid: `1000 × 11/1` represents target
  `1100` book minor units. Scale conversion must not reject this combination.
- A complete empty population must be schema-valid and produce a no-voucher
  decision with empty membership/effects/journal.
- Eventual settlement must consume valuation-adjusted carrying: initial
  `110000`, valued `115000`, settlement `116000` means unrealized gain `5000`
  plus realized gain `1000`, never a second realized gain of `6000`.

The current FX owner has no valuation application consumer and still derives
carrying from initial recognition less settlement releases. Fixing a pure leaf
does not enable valuation posting; persistence, current qualified rates, complete
scope recapture, approval, replay and settlement consumption must land together.

The follow-up integration of `26ba496` passed its seven isolated defect checks
and three existing real supplier/credit journeys. An earlier combined invocation
timed out before tests produced results; it was not counted as passing. Its owned
PostgreSQL process was identified through the run log and stopped before the
bounded successful reruns. Main was then fast-forwarded during an agreed
no-check/no-commit window, preserving the NEXT-07/NEXT-37 owners' dirty files.

## Merge discipline

The integrator owns branch reconciliation. Agents stage only owned files and
coordinate shared-main checks. Independent integration checks run in an isolated
worktree; no worker may use a whole-tree commit to collect sibling changes.
Existing migration names and receipt histories are retained. Provider activation,
production data and external filing/payment authority remain separate decisions.

## Document-reading merge verification, 2026-09-28

- Frozen dependency install passed; the merged lockfile retains both the browser
  test dependency and PDF reader dependency.
- `bun run build` passed for the API dry-run and web application.
- `bun run check:changed:full` passed after final code changes.
- The focused document-reader/extraction run passed 16 cases, including a real
  queue, normal self-host/preparation processes and executor revocation.
- The broader 55-case run passed 53 and found two integration regressions:
  remote source had restored first-page-only draft listing, and extracting the
  JSON-key validator had lost its specific public duplicate-key error message.
  Both were repaired without changing their existing behavioral assertions.
- The two affected suites then passed all 16 cases. Final source inventory was
  stable: `aa29368a85f92ab059fe2e5f3ecd9c689541d49601ccbaa07247e2805749d293`.
  This is combined verification evidence, not a claim of a single final green
  55-case run.

Artifacts remain in the isolated `overnight-integration` worktree under
`test-results/e2e` and `test-results/e2e-history`. The full-run failure receipt is
preserved alongside the passing targeted receipts. Independent Herdr review of
the authorization, operation recovery and request/session boundaries raised no
additional demonstrated failure; its JSON-error compatibility concern was
confirmed and repaired. Unknown submission remains a retained unknown outcome
requiring an explicit new request, never automatic redisclosure.
