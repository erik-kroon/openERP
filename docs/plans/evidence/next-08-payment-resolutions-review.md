# NEXT-08 payment instruction resolution: wiring and runtime review

Date: 2026-09-28. Packet: [NEXT-08 payment instruction resolution and replacement](../../specs/next-01-25/packets/NEXT-08.md). Scope of this record: what was built, what was actually executed, and what remains unobserved. It is not a company, statutory or provider claim.

## What changed

| File | Role |
| --- | --- |
| `packages/contracts/src/payment-resolutions.ts` (new) | Resolve and replacement contracts; the `paymentResolutions` API group and a read-only agent capability |
| `packages/contracts/package.json` | `./payment-resolutions` subpath export |
| `packages/contracts/src/api.ts` | registers `PaymentResolutionsApi` |
| `apps/api/src/db/purchases/payment-resolutions.ts` (new) | Table-access declaration and tx-passing reads over the existing batch, export, outcome and receipt tables |
| `apps/api/src/application/purchases/payment-resolutions.ts` (new) | The resolution and replacement owner, extending the supplier payment-batch/export owner |
| `apps/api/src/transport/http/routes/payment-resolutions.ts` (new) | `POST …/commerce/supplier-payment-resolutions` and `POST …/resolutions/replacements` |
| `apps/api/src/application/capabilities/payment-resolutions.ts` (new) | Read-only agent capability `payments_resolve_instruction`; replacement stays operator-side |
| `apps/api/src/index.ts` | registers `PaymentResolutionHandlers` |
| `apps/api/tests/payment-resolutions.e2e.test.ts` (new) | Five E2E cases |
| `docs/plans/domain-leaf-integration.json` | `payment-resolutions` moved from `deferred` to `wired` with a real consumer |

**No migration was added and no table was created.** The owner reads the batch owner's retained exports, outcomes and receipts, and writes its own receipts into the shared `command_receipts` table that the batch owner already writes. `bun run check:integration` passes with the leaf genuinely consumed by `apps/api`.

## The decisions the owner owns, and the ones it refuses

The owner extends the batch owner rather than replacing it. It owns three things.

1. **The instruction identity, derived per export item.** The end-to-end identity is the invoice identity's last 32 characters exactly as the retained pain.001 bytes carry it — read from the retained selection, never invented, never one per export. The beneficiary revision must be the reviewed revision the retained selection records. Original amount, currency and allocation intents come from the same retained rows.
2. **What counts as proof.** Only what the retained outcome chain and retained evidence support. A settled instruction cannot be released. An operator-reported rejection is recorded in the inventory and explicitly **not** treated as proof, because the leaf refuses that branch outright.
3. **Whether resubmission is permitted, blocked or unknown.** Unknown is a report with the missing evidence named, not a refusal to answer. A different key over the same proof digest is a duplicate economic effect. Same-key replay returns the saved report.

The refusals are the substance, and each is exercised.

**The central finding, stated plainly because it determines what was built: no proof branch is currently satisfiable, and the owner is written to say so.** The leaf refuses an operator-reported rejection outright. The controlled-never-dispatched branch needs an exclusive channel record, a dispatch fence and a revocation, none of which exists — our exports are retrievable files, so the bytes are exposed by construction. The provider-cancellation branch needs a retained provider-authenticated response, and no such caller exists here. The owner therefore reports unknown with the exact missing proof, gates replacement on an effective release that cannot yet exist, and refuses a settled instruction as a settled payment renamed. When an exclusive channel record or a provider-authenticated cancellation is retained, either branch activates without rewriting this owner.

**Admission is split by design.** Resolution admits any authenticated principal, including an agent: it reads retained state and caches a report, and it posts, allocates and moves nothing. Replacement stays operator-only, because a successor needs a fresh operator-initiated export and this owner must never become a way to move an instruction without one.

## What was actually executed

`bunx vitest run --config vite.config.ts apps/api/tests/payment-resolutions.e2e.test.ts`

| Check | Result |
| --- | --- |
| Tests | 5 passed, 0 failed |
| Runtime | local workerd, real PostgreSQL 17.11 (Homebrew), restricted `e2e_runtime` role |
| Migrations applied | 32, from a fresh `initdb` |
| Source integrity during run | `stable`, no changed source paths |

The harness starts its own PostgreSQL, applies the full migration chain, creates the restricted runtime role and drives the journey over real HTTP. Each test builds a real supplier invoice through counterparty, draft, review, approval and execution, proposes and verifies its payee through two separate operators, previews and exports a batch, and only then exercises the owner. Nothing is seeded except through a public operation, except for the second operator identity which is provisioned by the same admin pattern the fixture itself uses.

### The five cases

1. **Unknown stays unknown, and a recorded rejection does not become proof.** With no retained outcome the instruction stays reserved. After an operator rejection is recorded against retained evidence, the report still carries `releasedAmountMinor 0`, `proofKind none`, `resubmission unknown`, with the reason naming the rejection as retained but insufficient. Same key replays the saved report byte-for-byte; a different key over the same inventory is `IdempotencyConflict`.
2. **A settled instruction cannot be released.** A retained `reported_settled` outcome makes resolution refuse, because there is no capacity to release from an executed instruction.
3. **A replacement without an effective release is not compiled.** With an unknown resolution, the replacement gate refuses even though the successor export is real. A successor covering a different obligation is refused on the invoice identity before the leaf is consulted, and a resolution key naming no retained receipt is refused without inventing it.
4. **Unknown exports and invoices are refused, not invented.** A missing export and a missing invoice are both `NotFound`.
5. **The agent surface.** Over MCP, `tools/list` contains `payments_resolve_instruction` and still contains no approval or activation tool. A `tools/call` returns the same honest unknown the operator sees. The agent cannot assert what the owner did not establish.

## What this does not establish

- **No release has ever been observed**, because no proof branch is satisfiable from currently retained evidence. The release computation, the replacement compiler and the same-key replay of a real proof are correct by construction and dormant. The first real proof — an exclusive channel record or a provider-authenticated cancellation — will exercise them; until then their success paths are unobserved and recorded as such.
- **No provider, bank or filing interaction.** Outcomes are operator reports against retained evidence. `bankVerified`, `paid` and `allocationCreated` remain false by contract literal, and no adapter, credential or connected exercise is claimed.
- **No UI and no export of the resolution itself.** The report is returned over HTTP and MCP with every line of evidence; presentation is not built.
- **Synthetic only.** No company data, no real supplier, no real bank file, and no claim beyond the five journeys run.

## Remaining work on this packet

A retained exclusive-channel record with a dispatch fence and revocation, or a provider-authenticated cancellation path — either activates the proof branches without rewriting the owner. Snapshot or UI presentation of resolutions. And the reviewed treatment of a successor whose beneficiary revision legitimately changed through re-verification, which today must equal the retained revision.
