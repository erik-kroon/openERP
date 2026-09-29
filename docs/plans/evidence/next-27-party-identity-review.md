# NEXT-27 reviewed party identity resolution: wiring and runtime review

Date: 2026-09-29. Packet: [NEXT-27 reviewed party identity resolution](../specs/next-26-50/packets/NEXT-27.md). Scope of this record: what was built, what was actually executed, and what remains unobserved. It is not a company, statutory or identity-verification claim.

## What changed

| File | Role |
| --- | --- |
| `packages/contracts/src/party-identity.ts` (new) | Resolution prepare, balance view and read-only agent capability contracts; the `partyIdentity` API group |
| `packages/contracts/package.json` | `./party-identity` subpath export |
| `packages/contracts/src/api.ts` | registers `PartyIdentityApi` |
| `apps/api/src/db/commerce/party-identity.ts` (new) | Table-access declaration and tx-passing reads: counterparty heads, invoice identities, reservations, unissued drafts, evidence presence, saved resolutions |
| `apps/api/src/application/commerce/party-identity.ts` (new) | The resolution and balance-view owner, extending the party directory |
| `apps/api/src/transport/http/routes/party-identity.ts` (new) | `POST …/commerce/party-identity` and `POST …/party-identity/balances` |
| `apps/api/src/application/capabilities/party-identity.ts` (new) | Read-only agent capability `directory_read_balances`; prepare stays operator-side |
| `apps/api/src/index.ts` | registers `PartyIdentityHandlers` |
| `apps/api/tests/party-identity.e2e.test.ts` (new) | Three E2E cases |
| `docs/plans/domain-leaf-integration.json` | `party-identity` moved from `deferred` to `wired` with a real consumer |

**No migration was added and no table was created.** The owner reads retained counterparties, invoices, drafts and receipts, and writes its own receipts into the shared `command_receipts` table. `bun run check:integration` passes with the leaf genuinely consumed by `apps/api`.

## The decisions the owner owns, and the ones it refuses

The owner extends the party directory rather than replacing it. It owns three things.

1. **The member set, from retained records only.** Every named party must exist in the book, and the canonical party must belong to the set. Identifiers are derived from the retained counterparty revision — external key, display name and role — and **every one is marked unverified**, because the retained record carries `legalIdentityVerified: false`. A bank account from a verified payee proposal would still be unverified as identity, per the leaf's own rule that an account alone never proves it.
2. **Whether the claimed kind may be recorded.** A `same_legal_entity` resolution additionally requires cited retained evidence that a human reviewed; without it the owner refuses with `ApprovalRequired`. The leaf then enforces that conflicting verified identifiers can only resolve as related or not a duplicate. `related_but_distinct` and `not_duplicate` need no evidence, because they assert less.
3. **What the resolution invalidates.** Open obligations from the live invoice view, payment reservations from retained batch items, and unissued drafts from both draft families — each read from retained tables, each filtered to exactly the resolved parties, with the two obligation lists defined so they cannot double-count the same economic event.

The refusals are the substance. An unknown party is `NotFound`, not a placeholder member. A canonical party outside the member set is refused, not reinterpreted. A mapping that names no retained account is refused rather than reported around. A stale resolution — one whose members' revisions moved since it was recorded — groups nothing. And a mapping that cannot be satisfied from retained data is never completed by guessing.

**Two corrections made during this build are recorded because they change what the code claims.** First, the contract's `partyRevision` is a revision string (`/^[1-9][0-9]{0,17}$/`), not an `Identifier`: a revision number is a version, and the domain `Identifier` pattern rejects single digits, so typing it as an identity would have made every real revision fail its own contract. Second, the owner composes the invoice owner's live view for outstanding balances rather than computing its own, because a duplicated outstanding formula is how two readers come to disagree about the same invoice.

## What was actually executed

`bunx vitest run --config vite.config.ts apps/api/tests/party-identity.e2e.test.ts`

| Check | Result |
| --- | --- |
| Tests | 3 passed, 0 failed |
| Runtime | local workerd, real PostgreSQL 17.11 (Homebrew), restricted `e2e_runtime` role |
| Migrations applied | 32, from a fresh `initdb` |
| Source integrity during run | `stable`, no changed source paths |

Each test builds real counterparties through the retained directory operations, posts real supplier invoices through draft, review, approval and execution where the case needs an obligation, and only then exercises the owner. Nothing is seeded except through a public operation, except for the second operator identity which is provisioned by the same admin pattern the fixture itself uses.

### The three cases

1. **Same-entity resolution on reviewed evidence, with refusal without it.** Two supplier records resolve as the same entity when retained evidence is cited: the report carries the canonical identity, the reviewed flag, the evidence reference, a digest, and the retained invoice as an invalidated obligation. Every derived identifier is unverified. The same request without evidence is refused. Same key replays the saved report byte-for-byte. The balance view then groups the one retained obligation under the canonical identity with no netting.
2. **Related classification and the three refusals.** `related_but_distinct` records without evidence. An unknown party is `NotFound`. A canonical party outside the member set is refused rather than reinterpreted.
3. **The agent surface.** Over MCP, `tools/list` contains `directory_read_balances` and no prepare, approval or activation tool for identity decisions. A `tools/call` returns grouped balances with their obligation identities and control accounts. Recording that two parties are the same legal entity stays a reviewed human decision; name similarity never substitutes for it.

## What this does not establish

- **No legal identity was verified.** Every identifier the system derives is unverified, and the one same-entity resolution in the suite rests on synthetic evidence reviewed by a test, not a real identity check. Nothing here establishes that any two real parties are the same entity.
- **No balance was merged and no payee fact was rewritten.** Grouping is presentation over retained obligations. Settlement capacity is untouched.
- **No redirect closures exist.** The system retains no redirect records, so every closure is empty. A future merge-with-redirect feature would need its own retained records and its own cycle guards; the leaf already owns the cycle rules for when that day comes.
- **No UI.** The report and the view are returned over HTTP and MCP with every line of evidence; presentation is not built.
- **Synthetic only.** No company data, no real supplier, no real identity document, and no claim beyond the three journeys run.

## Remaining work on this packet

UI presentation of resolutions and grouped balances; a retained redirect/merge record with the leaf's cycle guards if merges become product scope; and the reviewed treatment of bank-account identifiers when a verified payee proposal exists, which today are correctly left as unverified identity evidence rather than promoted.
