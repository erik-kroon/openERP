# NEXT-45 direct cash-flow statement: wiring and runtime review

Date: 2026-09-28. Packet: [NEXT-45 direct cash-flow statement with a full reconciliation bridge](../../specs/next-26-50/packets/NEXT-45.md). Scope of this record: what was built, what was actually executed, and what remains unobserved. It is not a company, statutory or framework claim.

## What changed

| File | Role |
| --- | --- |
| `packages/contracts/src/cash-flow.ts` (new) | Reviewed mapping, request and report contract; the `cashFlow` API group |
| `packages/contracts/package.json` | `./cash-flow` subpath export |
| `packages/contracts/src/api.ts` | registers `CashFlowApi` |
| `apps/api/src/db/reports/cash-flow-statement.ts` (new) | Table-access declaration and the tx-passing reads: book, accounts, journal components with voucher `ownedTransfer`, retained periods |
| `apps/api/src/application/reports/cash-flow-statement.ts` (new) | The report owner: basis validation, balance derivation, classification, leaf composition, report |
| `apps/api/src/transport/http/routes/cash-flow.ts` (new) | `POST /v1/entities/:entityId/books/:bookId/cash-flow` |
| `apps/api/src/index.ts` | registers `CashFlowHandlers` |
| `apps/api/tests/cash-flow-statement.e2e.test.ts` (new) | Four E2E cases |
| `docs/plans/domain-leaf-integration.json` | `cash-flow-statement` moved from `deferred` to `wired` with a real consumer |

**No migration was added.** The owner is read-only over retained postings, so `bun run check:integration` passes at **20 wired, 28 declared deferred, 48 leaves**, up from 19 wired. The leaf is no longer dead code: the importer is `apps/api`, and the declaration names it.

## The decisions the owner owns, and the ones it refuses

The owner owns three things and refuses everything else.

1. **Which accounts are cash.** The caller supplies a reviewed perimeter; the owner refuses a mapping naming any account that does not exist in the retained chart. Nothing is inferred from an account name.
2. **How each cash leg is classified.** Derived here, from the reviewed role of that leg's counterpart inside the same voucher. `other_income` and `other_expense` are deliberately **excluded** from the role sets, because either can carry an FX remeasurement that is not an external cash flow; a mapping that wants one classified as operating must say so in a role that says so.
3. **Whether the result is complete.** It reports `complete` only when nothing is unclassified, no internal counterpart is missing, the reconciliation difference is zero, and the reported interval is fully covered by retained periods.

The refusals are the substance of the packet, and each is exercised:

- **A caller cannot state an amount.** `openingCashMinor` is absent from the request payload by design. Both opening and actual closing cash are derived by summing the retained debit and credit postings of the perimeter accounts. A request that tried to supply them would not compile against the contract.
- **A transfer needs its owned identity.** A cash-to-cash movement is eliminated only when the voucher's `posting_purpose` is `result_transfer_v1`. Equal and opposite amounts prove nothing, because an unrelated customer receipt and supplier payment look identical. Without the owned purpose the row stays unclassified.
- **Nothing defaults to operating.** A cash leg whose counterpart role does not determine exactly one activity is retained as an unclassified row carrying the reason.
- **A mixed payment splits by exact relationship.** Splits follow the counterpart postings and are keyed by activity and account; they must conserve the original cash component exactly or the whole component is unresolved rather than partially reported.
- **A broken basis is refused.** A perimeter, role or exchange-effect id naming no retained account is `UnsupportedProfile`, not a statement reported around.

One correction worth recording, because the test found it and a reviewer's eye had not: the cash movement a counterpart funds is the **negation** of the counterpart's own signed movement, since a balanced voucher's two sides carry opposite signs. Attributing the counterpart's raw sign makes every split fail its conservation check, which is a loud failure rather than a plausible wrong number.

## What was actually executed

`bunx vitest run --config vite.config.ts apps/api/tests/cash-flow-statement.e2e.test.ts`

| Check | Result |
| --- | --- |
| Tests | 4 passed, 0 failed |
| Runtime | local workerd, real PostgreSQL 17.11 (Homebrew), restricted `e2e_runtime` role |
| Migrations applied | 32, from a fresh `initdb` |
| Node | v26.4.0 |
| Source integrity during run | `stable`, no changed source paths |

The harness starts its own PostgreSQL, applies the full migration chain, creates the restricted runtime role and drives the journey over real HTTP, so the results are fixed-revision evidence rather than a unit-level claim.

### The four cases

1. **The packet's exact vector, reconciled.** Opening funding on 2026-01-15 is deliberately outside the requested interval, so opening cash of `100000` must be derived from retained history. Then a customer receipt `200000`, a supplier payment `80000`, an asset purchase `50000`, a loan drawdown `40000` and an FX remeasurement `2000`. The owner reports `operatingNet 120000`, `investingNet -50000`, `financingNet 40000`, `exchangeEffects 2000`, `expectedClosing 212000`, `actualClosing 212000`, `reconciliationDifference 0`, `complete true`, `sourceControlsComplete true`. These are the packet's own numbers, and the expectation is written in the test by hand from the posted amounts — the test never calls `calculateCashFlow`, and the owner is never used as its own oracle. The assertion also reaches the individual lines: one financing flow of `40000`, one investing flow of `-50000`, and one valuation effect carrying a non-null witness.
2. **An unclassifiable counterpart.** A `500` receipt against `other_income` is retained with `activity: null` and the reason `counterpart account has no reviewed activity role`. `unclassifiedRowIds` has one entry, the difference is `500`, and `complete` is `false`. The arithmetic is shown and the claim is not.
3. **A cash-to-cash movement without the owned identity.** A `30000` movement between two perimeter accounts is reported as an `internal_transfer` row with `transferId: null` and the reason `cash-to-cash movement without an owned transfer identity`, and the report is incomplete.
4. **A basis naming no retained account.** A perimeter of `account_does_not_exist` is `UnsupportedProfile` (422), not a 200 over an account the owner cannot see.

## What this does not establish

- **No owned-transfer journey was executed.** Case 3 proves the *refusal*. The positive case — a `result_transfer_v1` voucher whose two cash legs eliminate to zero external flow — is not exercised, because the public `manual_journal` path cannot set that posting purpose. Exercising it needs a direct seeded voucher, which is honest setup rather than a public capability, and is recorded as outstanding rather than claimed.
- **No persisted snapshot, no UI, no MCP surface, no export.** The packet asks for a captured snapshot with fixed membership, a UI, and JSON/CSV export of the same semantic rows. This slice delivers the classification and the bridge, computed live, and the owner returns every row with its evidence. Snapshot capture would need a migration; the report is currently recomputed per request.
- **Not an indirect statement, and not a statutory cash-flow statement.** Presentation and statutory applicability need the company and framework release. The reviewed roles are the existing `ReportRole` vocabulary, and this owner adds no new role.
- **The `sourceControlsComplete` signal is period coverage only.** It checks that the retained periods tile the reported interval with no gap. It does not prove source coverage, evidence completeness or a bank reconciliation, and it is not a substitute for them.
- **Synthetic only.** No company data, no provider, no real bank statement, and no claim beyond the four journeys run. The book is a synthetic SEK accrual profile created by the test fixture.

## Remaining work on this packet

Snapshot capture with fixed membership and a comparison against a later correction; the positive owned-transfer journey; MCP exposure; UI and export; and the reviewed treatment of `other_income`/`other_expense` when it is not a valuation carrier. The perimembership digest is returned today, which is the first piece the snapshot would need.
