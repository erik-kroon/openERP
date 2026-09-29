# NEXT-10 provider revisions to reviewed bank observations: wiring and runtime review

Date: 2026-09-29. Packet: [NEXT-10 provider revisions to reviewed bank observations](../../specs/next-01-25/packets/NEXT-10.md). Scope of this record: what was built, what was actually executed, and what remains unobserved. It is not a provider, company or statutory claim.

## What changed

| File | Role |
| --- | --- |
| `apps/api/migrations/0037-next-10-source-revisions.sql` (new) | Immutable interpreted revisions, the version-guarded observation head, cases and admissions, with narrow grants |
| `packages/contracts/src/bank-source-revisions.ts` (new) | Apply, admit and read contract; the `bankSourceRevisions` API group; the read-only agent capability |
| `packages/contracts/package.json`, `api.ts`, `capabilities.ts` | registers the subpath, the group and the capability |
| `apps/api/src/db/banking/source-revisions.ts` (new) | Tx-passing reads: retained page bytes, staged candidates, publication, head lock, lookalikes, cases, admissions, state |
| `apps/api/src/application/banking/source-revisions.ts` (new) | The owner: interpretation from retained bytes, revision application, reviewed admission, derived state |
| `apps/api/src/transport/http/routes/bank-source-revisions.ts` (new) | `POST …/banking/provider-observations` plus `/admissions` and `/state` |
| `apps/api/src/index.ts`, `application/capabilities/index.ts` | registers the handlers and the capability |
| `apps/api/src/db/banking/shared.ts`, `application/banking/shared.ts` | the four new tables in the access probe and the head's mutable columns |
| `apps/api/tests/provider-revisions.e2e.test.ts` (new) | Six E2E cases over real HTTP |
| `docs/plans/domain-leaf-integration.json` | `bank-source-revisions` moved from `deferred` to `wired` |

`bun run check:integration` passes at **29 wired, 19 declared deferred, 48 leaves**, up from 28.

## The deferral was stale, and that is the finding

The declared reason was *"Bank intake persists provider observations, then its application owner composes this leaf"*. Bank intake **does** exist: the connector owner retains provider observations, and NEXT-09, landed the day before, retains the exact provider bytes behind every published change. The missing piece was never a prerequisite. It was the owner.

## The load-bearing decision: the amount is never taken from the request

The caller names a page ordinal, a record ordinal, a provider transaction identity and the profile's currency scale. It states **no amount and no status**. The owner reads the retained provider bytes for that page, parses the exact decimal lexeme as a rational decimal, converts it to whole minor units at the scale, and flips the sign because the Transactions API's positive means money leaving the account.

Three refusals make that real rather than claimed:

- A caller naming a transaction the retained bytes do not carry is `IdempotencyConflict`, not an empty match.
- A lexeme with no whole-minor-unit representation (`"12.505"` at scale 2) refuses.
- A currency outside the profile's qualified scale refuses; nothing is defaulted.

The pending case proves the point from the other side: the test's request claims `pending: false` while the retained bytes say `pending: true`, and the **bytes win**. The returned outcome is `pending_observation`, which is not admitted and not banked.

## Admission adopts; it never creates

This is a structural finding, not a preference. `bank_observations` is keyed by `statement_id` with a foreign key to `bank_statements`, so a provider change on its own **cannot** be a bank observation in this schema. Rather than invent a second observation register to work around that, the admission table carries a foreign key to `bank_observations` and the owner refuses anything else:

- Admitting an observation that was never retained is `NotFound`.
- Admitting without cited retained evidence is `MissingEvidence`.
- Admitting the same revision twice is `AlreadyPosted`, checked **before** the insert so the refusal is typed rather than a constraint collision.

`resolvedObservationCount` is read back from the retained heads, not asserted: it is the difference between one observation and a duplicated cash capacity.

## Nothing posts, and a removal is an investigation

Every receipt carries `journalIds: []`. A removal of an already-booked observation produces a `removed_booked_observation` case with `bookedBefore` and a retained `ledgerEffect: "none_no_automatic_deletion_or_reversal"`; the observation, its admission and every journal survive untouched. The test asserts exactly that against the database: one observation, one admission, **zero vouchers**, before and after.

## What the runtime actually showed

Six cases over real workerd, real PostgreSQL 17.11 and the restricted `e2e_runtime` role:

| Case | What was observed |
| --- | --- |
| Interpretation | `"12.50"` at scale 2 → `-1250`; `"0.05"` → `-5`, a value a float would have rounded away. Digests recomputed in the test over the same bytes. |
| Refusals | Fractional minor unit, identity absent from the bytes, and a staged generation with no publication marker all refuse. |
| Admission | Missing observation, missing evidence and a repeated revision all refuse. The success path adopts once with `resolvedObservationCount: 1`, `journalIds: []`, and the database holds one admission, one observation and zero vouchers. |
| Removal | `removal_investigation`, `cashMovementMinor: null` (a removal schema carries none), one open case, and the observation and admission both still retained. |
| Pending | The retained bytes' pending flag overrides the request's; the observation is not admitted and nothing is banked. |
| Read | The agent-facing read returns the revision history and no admission, and an agent has no interpret or admit route. |

The full suite passes alongside it: **164 tests across 40 files**.

## Corrections made during the build, recorded because they change what the code claims

- **The publication version was the change count.** The revision's `publicationVersion` was taken from the publication's `changeCount`, so two windows carrying the same number of changes collided on the unique identity key and the second silently became a replay. The stream's real publication version is now read instead; a change count is not a version.
- **A shared-lock read took a row lock**, and the state read used the response shape as its request shape. Both are the same class of mistake NEXT-09 hit, and both are fixed here by separate request/response schemas and a plain consent read.
- **JSON projection columns were read through an object-only helper.** `Shared.arrayField` narrows a `JsonObject`, but the projection returns a `Json` array, so every read returned empty. The read now narrows the `Json` union directly.
- **A removal was made to carry a record body.** Requiring `records[n]` for a removal refused every real removal, because a removal schema has no body. A removal now reads nothing and is therefore given no amount — `null`, never a zero.
- **A repeated admission hit a unique constraint before its own check.** The existing-admission check fell through to the insert. It now returns the typed refusal first.
- **The window lease stranded a published stream.** NEXT-09's claim refused a second window while a lease was held, even after the previous generation had published and there was nothing left to protect. The lease now blocks only while an incomplete generation is resumable. NEXT-09's own fence test still passes, because its lease protects an unpublished generation.

## Deliberate omissions, stated rather than smoothed over

- **No provider call, no job and no external acceptance.** This owner reads bytes a previous window retained. Nothing here contacts Plaid.
- **No posting, matching, coverage or reconciliation signoff.** A published window is a coverage claim about provider changes; a provider identity is what its admission and open cases say it is. Neither is a statement.
- **Pending lineage is not wired to a real predecessor.** `providerLinksPendingPredecessor` reaches the leaf, but no released owner retains a pending predecessor observation to link, so the branch is unreachable rather than exercised.
- **The lookalike overlap case is implemented but unobserved.** It fires when a statement-backed observation exists on the same account, date and amount. The E2E cases do not create that coincidence, so the branch is verified only against the leaf.
- **The consent is operator-attested, not provider-verified**, and this packet does not change that.
