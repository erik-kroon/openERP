# NEXT-50 agent book context — delivery evidence

Baseline: `e5121df`. Scope is this evidence file and the eight files listed under
_Changed files_. This delivers a previously deferred leaf: the `agent-context`
entry in `docs/plans/domain-leaf-integration.json` moves from `deferred` to
`wired` because a real application owner now composes it.

## What was wired

The leaf already had correct pure rules (`assertModuleCompleteness`,
`rankWork`, `getContextDelta`, `classifyIncomingPayment`) and **no consumer**.
It now has:

- a named read-only application owner, `apps/api/src/application/agent/context.ts`,
  with one operation: read the retained work inventory, derive the modules and
  the work rows, rank them for the caller's stated goal and seal the snapshot;
- tx-passing persistence reads through the existing workspace owner plus one
  focused boundary query in `apps/api/src/db/agent-context.ts`;
- the wire contract and endpoint in the existing `WorkspaceApi` group, the HTTP
  handler in the existing `WorkspaceHandlers` group, and one line in the
  existing `workspaceCapabilities` object;
- a focused E2E over real workerd, PostgreSQL and the restricted runtime role.

This extends the **existing** workspace owner rather than creating a subsystem,
which is why the packet delivers without a new table or a migration. No
endpoint, capability or table outside the workspace surface was touched.

## What the owner reads and what it computes

Every identity, revision, amount of work and rank below comes from retained
rows or the registered catalog. The caller states only a goal label and an
optional period filter.

- **Work rows** come from the retained `change_sets` (unposted proposals) and
  the attention inventory (drafts, reviews). A completed row is resolved, so it
  is not work; an open row of a shape the index cannot classify refuses the
  whole index rather than entering under a guessed identity or being silently
  dropped.
- **Severity is a retained-state fact.** An item in an accounting period that
  already ended, or with a retained due moment already passed, blocks the goal;
  every other retained unresolved item is material. Nothing retained and
  unresolved is routine, and nothing absent is zero.
- **The blocked operation names a registered capability**, because ranking only
  ranks work its snapshot authorizes. An unposted change-set names
  `changes_execute`. A review has no registered capability that would unblock
  it, so it names none rather than inventing one; the next human step is still
  recorded as preparation.
- **The revision is the retained plan version, not the digest.** The digest is
  the content hash and the two change independently; stuffing the digest into
  the numeric revision field faults the draft decode instead of reporting.
- **Module summaries** group the bounded inventory by kind. `rowCount` is the
  retained unresolved rows and `fullCount` is the retained rows, so an empty
  module with known coverage is claimable and an unknown one refuses.
- **The goal label is caller-stated.** Ranking semantics come from retained
  state and the catalog, not from the label. The leaf's goal-mismatch refusal
  is a property of the pure compiler, exercised in the probe; this endpoint
  builds the snapshot from the same request, so it cannot trigger it.
- **The capability catalog is build configuration, not retained data.** No
  per-actor capability grant table exists, so the index lists what this server
  build exposes and says so.

## A blocked operation must be a registered capability

Building this caught a real defect in my own code: I first set
`blockedOperation: "execute_change_set"`, which is an operation name rather
than a capability key, so `rankWork` correctly dropped every journal row —
ranking only ranks work its snapshot authorizes. The E2E went from 3/5 to 5/5
when the name became `changes_execute`. It is recorded here because the refusal
did its job: an unregistered capability would have made the ranking lie.

## E2E results

`bun run test:e2e apps/api/tests/agent-context.e2e.test.ts` — **5 passed,
0 failed**, exit 0. Real workerd, PostgreSQL with the full migration chain, and
the restricted runtime role.

| Case                        | Observed                                                                                                                                                                                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Empty book                  | No work, empty ranking, no refusal; every reported module is coverage-known; the catalog contains `workspace_list_work`                                                                                                                                       |
| Unposted proposal           | One work row with the retained id and digest from the prepare response; `blockedOperation` is `changes_execute`; `missingInputs` are approval and execution; severity is material in an open period; module `journal` reports rowCount 1; the row ranks first |
| Unposted in an ended period | `blocks_goal`, ranked above the still-postable item, from retained period ends and the database clock                                                                                                                                                         |
| Executed proposal           | Gone from work and from ranking; the module reports rowCount 0, fullCount 1, still coverage-known                                                                                                                                                             |
| Same book reread            | Identical ranked identities and the same principal-scope fingerprint                                                                                                                                                                                          |

Expected values are derived from the retained postings the test made (prepare
response ids and digests, independent database reads). The context compiler is
never used to generate an expectation.

## Leaf probe

`next50-probe.ts` at the repository root of this review branch records the
failure contract written before any production edit: **18 passed, 0 failed**.
Two probe expectations were corrected during development, both my own fixture
bugs, not leaf defects: short test identifiers under the three-character
`Identifier` bound, and a collapse test that gave the third item a different
missing fact so the collapse boundary is exact. The leaf needed no repair.

## Gates

- `bun run check:integration`: passed, 22 wired / 26 declared deferred.
- `bun run check:changed`: passed.
- `bun run check:changed:full`: passed (two remaining items are lint
  suggestions, not errors).
- `bun run format:check`: passed.
- `bun run check:tests` (the E2E type gate): passed.
- No command timed out. No grant, migration or access rule was added or
  weakened.

## Changed files

- `apps/api/src/application/agent/context.ts` (new owner)
- `apps/api/src/db/agent-context.ts` (new; one boundary query)
- `apps/api/src/db/workspace.ts` (one additive column: the retained plan
  version on the work row)
- `packages/contracts/src/workspace.ts` (capability, contract, endpoint)
- `apps/api/src/transport/http/routes/workspace.ts` (one handler)
- `apps/api/src/application/capabilities/workspace.ts` (one line)
- `apps/api/tests/agent-context.e2e.test.ts` (new, 5 cases)
- `docs/plans/domain-leaf-integration.json` (this leaf only)

None of the NEXT-08 registration points is touched: no `api.ts`, no
`contracts/package.json`, no `apps/api/src/index.ts`, and no
`capabilities/index.ts` — the existing spreads pick the new entries up.

## Not proven

- **Deltas are leaf-verified, not owner-exercised.** `getContextDelta` is
  proven by the probe, but no endpoint reads two snapshots and diffs them. An
  agent comparing contexts across calls has no transport for it.
- **Settlement hints are leaf-verified only.** `classifyIncomingPayment` has
  no owner, no endpoint and no E2E; nothing in the product suggests a
  settlement today.
- **No per-actor grants.** The catalog is build configuration. An actor-filtered
  capability set would need a grant table that does not exist.
- **Bounded inventory.** Past 50 attention or work rows the endpoint refuses
  rather than paging, matching the existing workspace reads. A book past that
  bound gets no index at all.
- **The goal is a label, not a verified fact.** See above.
- No posting, approval, migration, provider or filing claim. Synthetic
  fixtures only.
