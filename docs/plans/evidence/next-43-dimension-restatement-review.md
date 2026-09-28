# NEXT-43 reviewed dimension restatement — delivery evidence

Baseline: `7650fe6`. Scope is this evidence file and the nine files listed under
_Changed files_. This is the delivery of a previously deferred leaf: the
`dimension-restatement` entry in `docs/plans/domain-leaf-integration.json` moves
from `deferred` to `wired` because two real importers now exist.

## What was wired

The leaf already had correct pure rules (`prepareRestatement`,
`classificationAt`, `appendRevision`) and **no consumer**. It now has:

- a named application owner, `apps/api/src/application/dimensions/restatement.ts`,
  with three operations: prepare, apply, and a report-time read;
- tx-passing persistence in `apps/api/src/db/dimensions.ts`;
- three new tables in `apps/api/migrations/0032-next-43-dimension-restatement.sql`;
- the wire contract and endpoints in `packages/contracts/src/dimensions.ts`;
- the HTTP handlers in `apps/api/src/transport/http/routes/dimensions.ts`;
- two read-only capabilities, `dimensions_classification_view` and
  `dimensions_restatement_view`;
- a focused E2E over real workerd, PostgreSQL and the restricted runtime role.

This extends the **existing** NEXT-14 dimension owner rather than creating a new
subsystem, which is why the packet could be delivered without inventing an owner.

## The analytical view, and what it proves

`analyticalView` is a pure read added to the leaf to deliver the packet's
"original-versus-reviewed analytical view". For each requested dimension it
partitions **the same selection** twice, and the property it enforces is
conservation: every bucket of a dimension sums to the unfiltered selection total
in both views. A line with no assignment for a dimension lands in an explicit
`unassigned` bucket rather than vanishing, which is what makes the partition
complete. Two dimensions are never added together.

The E2E proves this over real data with an expectation derived from the retained
posting (one debited line, 12500 minor units):

- the original view holds 12500 in `Department:0012` and the reviewed view holds
  12500 in `Department:0099`, so the money moved between buckets and was not
  duplicated;
- the original view has no `0099` bucket and the reviewed view has no `0012`
  bucket;
- per dimension and per view, the buckets sum to 12500;
- the unchanged Project dimension is identical in both views;
- a cutoff before the revision makes the two views identical, because "as at
  when" is part of the question.

Building this surfaced a real bug in my own code: `originalValueKey` already
returns a dimension-qualified key, and I prefixed it a second time, which nested
the dimension inside the value and split one bucket into two. The conservation
check caught it. It is recorded here because the check did its job.

## A restatement never edits a posting

The counterfactual that matters is stated per case, and the E2E observes it
directly:

- the retained `journal_lines` row is captured before the restatement and
  compared after it — `debit_minor`, `credit_minor` and `account_id` must be
  byte identical;
- the original classification still resolves to the original tag after the
  restatement, while the reviewed view resolves the new one, so history was
  added beside rather than over the original;
- the reviewed view is resolved _as at a cutoff_, so a saved report keeps the
  view it was built from.

## What the request may and may not state

The request names posted lines (`voucherId` + `lineId`) and a desired reviewed
assignment set. It carries **no** amount, account, currency, tax point or
economic owner. The exact signed amount and the financial digest of every
selected line are read from retained `journal_lines`/`vouchers` rows inside the
transaction and are never taken from the request, so the compiler's
`FinancialChangeRejected` guard compares retained facts against retained facts.

One input is a **reviewed configuration witness, not a financial fact**: the
analytical `dimensionPolicy`, which the catalogue does not retain. NEXT-14 takes
the same kind of policy witness on a posting action. It is sealed into the plan
the reviewer approves, and it is recorded here explicitly so it is not mistaken
for a derived value.

## Tables and their guards

- `dimension_restatement_plans` is immutable; it retains the sealed plan, its
  digest, and the selection, because the plan keys a line by its line id and the
  voucher must not be reconstructed at apply time.
- `dimension_classification_revisions` is immutable history and references a real
  posted line through `journal_lines`. The reviewed baseline requires a JSON
  array with at most 64 entries, so a partial set cannot be stored as a scalar.
- `dimension_classification_heads` is the only mutable row, and a trigger refuses
  any move that is not exactly one revision and one version. A concurrent
  restatement therefore aborts rather than merging.

A line id is only unique inside its voucher and the plan keys a line by its line
id, so a selection reusing one line id across two vouchers is refused at
prepare rather than silently collapsing two lines into one.

## E2E results

`bun run test:e2e apps/api/tests/dimension-restatement.e2e.test.ts` — **6 passed,
0 failed**, exit 0. Real workerd, PostgreSQL with the full migration chain, and
the restricted runtime role.

| Case                                                         | Observed                                                                                                                           |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| Restate beside the original tag                              | `appendedCount` 1, revision 1; reviewed view resolves `0099`, original view still resolves `0012`; retained journal line unchanged |
| Apply a plan whose digest does not match                     | `StaleDependency`                                                                                                                  |
| Second restatement naming head revision 0 when the head is 1 | `StaleDependency` at **prepare**, so no plan a reviewer could approve is sealed against a moved head                               |
| Replay an identical desired set                              | `appendedCount` 0, `replayedCount` 1, head does not advance, one revision retained                                                 |
| Restate a line no posting carries                            | `NotFound`                                                                                                                         |

Expected values are derived independently from the retained posting rows. The
production compiler is never used to generate an expectation.

## Gates

- `bun run check:integration`: passed, 20 wired / 28 declared deferred.
- `bun run check:changed:full`: passed.
- `bun run check:changed`: passed.
- `bun run format:check`: passed.
- No command timed out. The database role used the applied grants; no grant or
  migration was weakened to make a case pass.

## Changed files

- `apps/api/migrations/0032-next-43-dimension-restatement.sql` (new)
- `apps/api/src/db/schema.ts` (three table mappings)
- `apps/api/src/db/dimensions.ts` (tx-passing reads and DML)
- `apps/api/src/application/dimensions/restatement.ts` (new owner)
- `apps/api/src/application/capabilities/dimensions.ts` (read-only capability)
- `apps/api/src/transport/http/routes/dimensions.ts` (three handlers)
- `packages/contracts/src/dimensions.ts` (contract and endpoints)
- `apps/api/tests/dimension-restatement.e2e.test.ts` (new, 6 cases)
- `docs/plans/domain-leaf-integration.json` (this leaf only)

No file shared with the NEXT-45 cash-flow work is modified: this change touches
neither `packages/contracts/src/api.ts`, `packages/contracts/package.json` nor
`apps/api/src/index.ts`, because the three endpoints join the existing
`DimensionsApi` group and the existing `DimensionHandlers` group.

## Not proven

- **Packet scope not delivered.** NEXT-43 also describes explicit removal
  (becoming `unassigned`), evidenced exemptions, and the original-versus-reviewed
  analytical view across a whole reporting selection. The leaf implements those
  rules, and the three delivered operations exercise preparation, application,
  head fencing, replay and cutoff resolution. What is **not** proven here is a
  report that renders both views side by side for a full selection.
- The analytical `dimensionPolicy` is a reviewed request witness, not retained
  data, as described above.
- One reviewed profile only: a single-scope, single-currency book. Multi-currency
  restatement, cross-scope conflicts and archived-value handling are not
  exercised.
- No concurrency test runs two writers simultaneously. The head is fenced by a
  database trigger and re-checked in the transaction, and that is verified only
  sequentially.
- No provider, filing, tax or statutory claim. Synthetic fixtures, a synthetic
  company, and a synthetic catalogue only.
- `evaluateValidationRun` and `checkSignatureScope` remain unconsumed across the
  repository; this packet does not change that.
