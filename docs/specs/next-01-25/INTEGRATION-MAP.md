# Integration map: application-owned edition v2

This is a complete replacement ownership map for the same 25 tasks. No task has been renumbered or replaced with a new task. Dependency priorities and all five WIP reservations remain. Earlier SQL function and migration identifiers are historical evidence, not implementation targets.

## Root integration ownership

Root owns shared `packages/contracts` API/capability registration, `packages/domain` unions used across domains, application identity/transaction primitives, the internal journal writer, baseline schema/integrity/grants and common UI/runtime composition. Domain workers own named Effect application services, pure calculations and tx-passing persistence with their local UI.

Do not recreate `db/query.ts` operation-string dispatch. All REST/MCP/worker/script callers reach the same application operation. Public operation IDs can stay stable while internals change. Calls to internal writers pass the same `tx`; calls to another public operation occur with no enclosing financial transaction unless an explicitly supported internal aggregate port is used.

A private `applyWithinTransaction` contract is a real composition boundary, not a second transaction, a public arbitrary posting endpoint or a security boundary against compromised trusted backend code.

## Dependency table

Independent leaf preparation may proceed before final wiring. Conditional dependencies become mandatory only when the selected company/operation uses the relevant case. Do not treat an absent qualified profile as an empty or inapplicable business population.

| Packet | Required | Integrate after | Conditional | Reserved handoff |
|---|---|---|---|---|
| [NEXT-01](packets/NEXT-01.md) | None | None | None | None |
| [NEXT-02](packets/NEXT-02.md) | None | None | None | None |
| [NEXT-03](packets/NEXT-03.md) | NEXT-02 | None | None | None |
| [NEXT-04](packets/NEXT-04.md) | NEXT-02, NEXT-03 | None | None | WIP-VAT03, WIP-VAT04-A1 |
| [NEXT-05](packets/NEXT-05.md) | NEXT-03, NEXT-04 | None | NEXT-17: actual unpaid foreign-denominated supplier obligations occur | None |
| [NEXT-06](packets/NEXT-06.md) | NEXT-02, NEXT-03 | None | None | None |
| [NEXT-07](packets/NEXT-07.md) | NEXT-03 | None | NEXT-08: an exported payment reservation must first be resolved | None |
| [NEXT-08](packets/NEXT-08.md) | None | None | None | None |
| [NEXT-09](packets/NEXT-09.md) | None | None | None | None |
| [NEXT-10](packets/NEXT-10.md) | NEXT-09 | None | None | None |
| [NEXT-11](packets/NEXT-11.md) | NEXT-02, NEXT-13 | None | NEXT-14: dimension assignments occur in the selected book | None |
| [NEXT-12](packets/NEXT-12.md) | NEXT-02 | None | None | None |
| [NEXT-13](packets/NEXT-13.md) | NEXT-02 | None | None | None |
| [NEXT-14](packets/NEXT-14.md) | None | NEXT-13 | None | None |
| [NEXT-15](packets/NEXT-15.md) | NEXT-02 | NEXT-04 | None | None |
| [NEXT-16](packets/NEXT-16.md) | NEXT-01, NEXT-03, NEXT-06 | None | None | None |
| [NEXT-17](packets/NEXT-17.md) | NEXT-02 | NEXT-03 | None | WIP-FX02-P1 |
| [NEXT-18](packets/NEXT-18.md) | NEXT-17 | None | None | WIP-FX02-P1 |
| [NEXT-19](packets/NEXT-19.md) | None | None | NEXT-04: the disposal has a VAT-reporting consequence; NEXT-15: the chosen flow requires a supported legal invoice/credit interaction | WIP-AST03-UI |
| [NEXT-20](packets/NEXT-20.md) | NEXT-02 | None | None | None |
| [NEXT-21](packets/NEXT-21.md) | NEXT-20 | None | None | None |
| [NEXT-22](packets/NEXT-22.md) | NEXT-13 | None | None | None |
| [NEXT-23](packets/NEXT-23.md) | NEXT-13, NEXT-22 | None | NEXT-04: the reviewed company/year inventory makes this treatment applicable; NEXT-05: the reviewed company/year inventory makes this treatment applicable; NEXT-06: the reviewed company/year inventory makes this treatment applicable; NEXT-07: the reviewed company/year inventory makes this treatment applicable; NEXT-12: the reviewed company/year inventory makes this treatment applicable; NEXT-18: the reviewed company/year inventory makes this treatment applicable; NEXT-19: the reviewed company/year inventory makes this treatment applicable; NEXT-21: the reviewed company/year inventory makes this treatment applicable | None |
| [NEXT-24](packets/NEXT-24.md) | NEXT-13, NEXT-23 | None | None | None |
| [NEXT-25](packets/NEXT-25.md) | None | None | NEXT-02: required by the selected real-company rehearsal scope; NEXT-03: required by the selected real-company rehearsal scope; NEXT-04: required by the selected real-company rehearsal scope; NEXT-05: required by the selected real-company rehearsal scope; NEXT-06: required by the selected real-company rehearsal scope; NEXT-11: required by the selected real-company rehearsal scope; NEXT-12: required by the selected real-company rehearsal scope; NEXT-13: required by the selected real-company rehearsal scope; NEXT-16: required by the selected real-company rehearsal scope; NEXT-21: required by the selected real-company rehearsal scope; NEXT-23: required by the selected real-company rehearsal scope; NEXT-24: required by the selected real-company rehearsal scope | None |

## Reserved work

**WIP-VAT03.** VAT-03 qualification of 9120/9130, including migration, Worker/PostgreSQL and outcome/recovery cases. Do not reimplement or take over qualification. Historical migration numbers identify reserved scope only; consume its released application replacement, never restore the retired SQL workflow.

**WIP-FX02-P1.** FX-02-P1 partial settlement extending 9140, including paired release, residuals, gain/loss and replay. Do not implement partial allocation in this wave. Historical migration numbers identify reserved scope only; consume its released application replacement, never restore the retired SQL workflow.

**WIP-AST03-UI.** AST-03 impairment UI/control/disposal closure over 9150, including schedules.tsx and its control views. Do not take these consumers over. Historical migration numbers identify reserved scope only; consume its released application replacement, never restore the retired SQL workflow.

**WIP-VAT04-A1.** VAT-04-A1 financial amendment delta owner. Do not build another target-minus-prior effect calculator or obligation owner. Historical migration numbers identify reserved scope only; consume its released application replacement, never restore the retired SQL workflow.

**WIP-COM2-W1.** COM-2-W1 provider-neutral webshop intake and order/catalog identity. Do not create competing intake, catalog snapshots or order revisions. Historical migration numbers identify reserved scope only; consume its released application replacement, never restore the retired SQL workflow.

## Handoff contract between runtime owners

Each domain handoff must identify its application operations and current source hashes, wire contracts, pure compiler versions, tx-passing persistence methods, expected locks, complete effect membership, receipt identity, required outbox intents and remaining qualification gates. The receiver checks actual exports rather than copying illustrative names literally.

The receiving worker may not create a second financial balance to avoid a missing port. In particular VAT amendments, paired FX consumption and impairment/disposition remain at their existing owners.

## Runtime and baseline

The API runs on the selected Worker/Bun request composition. effect-mq runs in a separate persistent Bun process with its own session-preserving listener connection. Queue delivery invokes the same application operations. Financial transaction authority never lives in a queue payload or connection session variable.

The pre-release clean baseline has the selected schema, narrow integrity and role files. No old-schema compatibility adapter is required for disposable development data. Any actual meaningful data discovered at a target blocks a destructive reset until its preservation is resolved. Real historical company-bookkeeping import remains in scope for NEXT-12 and NEXT-25.

## Implementation lanes

Keep the original owner lanes from the index, with root coordinating shared files. A worker does not add its own generic transaction wrapper, event language or queue framework. Finish a coherent named operation including reads, execution, corrections and recovery before retiring its previous application dispatch path.

NEXT-01, NEXT-02, NEXT-09 and NEXT-13 remain sensible independent starts subject to actual source ownership. NEXT-13 can develop its pure model while waiting for NEXT-02's profile contract. NEXT-04 waits for released VAT owner ports for financial controls. NEXT-17/18 and NEXT-19 wait for the FX and asset owner handoffs respectively.

## Required proof, not a claimed result

For each port, enumerate former accepted cases/refusals and the new application function enforcing each one. Inspect structural DB constraints separately. Observe real one-connection rollback, concurrent capacity use, approval revocation, same-key recovery and handler/version behavior under actually authorized tests. Nothing in this file authorizes taking over the five active assignments or editing repository tests.
