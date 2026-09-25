# Dependency-ordered delivery

This is the implementation map for the existing P0–P7 roadmap. Packet IDs, deliverables, dependencies and acceptance are defined in their owning area documents and indexed in [work-packages.json](evidence/work-packages.json). That index is derived from the tables; it is not a second manually maintained backlog. Packet completion requires its observable result, not just a merged migration or a UI stub. The application-owned replacement in [ADR 0010](../adr/0010-application-owned-accounting-replacement.md) changes implementation ownership, the clean baseline and the durable runner without changing the domain packet IDs or financial requirements.

The [repository comparison reconciliation](capability-backlog.md#repository-comparison-reconciliation) maps the supplied assignment aliases and payroll/FX ID conflicts to these owners. Supplemental inbox, party, recurring-sales and deadline scope follows the dependencies stated there; it does not create a competing packet sequence.

The [adopted financial-contract stages](05-vat-payroll-assets-fx.md#adopted-financial-contract-delivery) turn FX, VAT reclassification and impairment decisions into implementation and proof work. Payroll builds on the existing 9050 foundation. Provider and company gates remain separate from these selected design choices.

## Ready order

| Wave                               | Packets / outcomes                                                                                                              | Exit and next consumer                                                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| 0 — reconcile the live foundation  | FND-01–FND-04; current schema/contract/status inventory, production identity design and existing suite/evidence reconciliation. | Actual callers and plan agree; authorized proof work can use a fixed revision.                                           |
| 1 — complete the core              | PST-01–PST-05; COR-01/COR-02.                                                                                                   | Exact review, trusted approval, atomic effects/correction and durable recovery across supported surfaces.                |
| 2 — sources and commercial records | IMP-01/IMP-02; COM-01–COM-03; early END-03 and OPS-01/OPS-03.                                                                   | Real sources can be retained/interpreted; invoices/payment facts and stable report/backup boundaries have owners.        |
| 3 — first reconciled period        | IMP-03–IMP-06; COM-04/COM-06; technical END-01; OPS-02/OPS-04.                                                                  | Supplied history, relationships and independent controls reconcile; current incomplete profiles remain explicit.         |
| 4 — applicable accounting depth    | VAT, PAY, AST and FX packets; COR-03/COR-04; COM-05 as needed.                                                                  | Each selected treatment and its register correction passes independent cases; no inapplicable family silently assumed.   |
| 5 — year and artifact chain        | END-02/END-04–END-07 with selected domain/control gates.                                                                        | Financial close, opening, tax/annual-report facts, artifact validation and required external outcomes agree.             |
| 6 — operational release            | OPS-05–OPS-07.                                                                                                                  | Frozen/reconciled source, fully restored target, one fenced writer, accepted recovery objectives and observed operation. |

Waves are useful review checkpoints, not additional dependency edges. END-03 can start as soon as its kernel/source inputs exist; payroll does not need VAT implementation; a synthetic restore can run before statutory output. Domain packet tables remain the detailed dependency authority.

## Mandatory versus conditional dependencies

The graph records engineering prerequisites. A **company release gate** is a separate set selected by reviewed applicability, not a reason to introduce circular implementation dependencies.

| Consumer                         | Conditional gate                                                                                                                                                            |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| COM-03 cross-currency allocation | FX-02; same-currency payment machinery can be completed first.                                                                                                              |
| COR-03 register-aware correction | Each supported register's own posting/capacity contract; plain-journal correction does not wait for them.                                                                   |
| END-02 company financial close   | IMP-06, relevant COM controls, and every applicable VAT/PAY/AST/FX/control profile.                                                                                         |
| END-06 tax-file branch           | END-04; the SIE branch can proceed from its own IMP-02/END-03 inputs.                                                                                                       |
| END-06 annual-report branch      | END-05; a complete selected framework and disclosures are required.                                                                                                         |
| END-07 provider family           | Its exact validated artifact profile, D-10 provider contract and required signature/authority; provider families are independent.                                           |
| OPS-06 production cutover        | All applicable company gates and required fulfillment evidence. END-07 connected delivery is required only if that connector is part of the selected operating arrangement. |

The tax bridge is calculated from a frozen **pre-close** year snapshot, then its approved adjustments produce a new basis for final close. END-04's dependency on END-02 means the close/opening machinery and contracts exist; it does not require final close before tax adjustments. This keeps the runtime sequence coherent.

## Ownership and integration

Use the existing repository/domain ownership. Each domain owns contracts, named application operations, transaction-passing persistence and its local UI. Shared composition has one integrator: contract exports/API groups/capability registry, admission/authentication, the transaction and database boundary, web routing/query glue, translations, the effect-mq runner and deployment wiring. No two owners independently redefine amount, actor, receipt or allocation semantics.

The current `.agents/work/domain-ownership.md` documents reserved migration ranges and ongoing work. Inspect its current integration state before implementation, but do not treat its historical session names as new tasks created by this plan. Migration sequence numbers are allocation namespaces, not dependency proofs. Integrate only a dependency-complete prefix and never rewrite applied history.

Every handoff supplies: exact changed paths; caller-visible behavior; operation/schema additions; migration prerequisites; evidence and checks not run; affected domain dependencies; and the next integration action. A contract alone is not ready to register as an advertised capability. Register handlers and schemas together; the UI can expose the operation only when its actual support/readiness state is honest.

## Existing implementation reconciliation

Start each packet with the current source and retained artifacts. Classify its acceptance criteria as satisfied with linked evidence, implemented but unverified, incomplete, or blocked by named external input. Do not rewrite the original research dossier to pretend its older snapshot described today's checkout.

| Existing material                              | How to use it                                                                                                                                      |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Synthetic core, recovery and correction drafts | Complete the selected contract and fault cases; preserve receipts, supported routes and financial meaning, then replace the old implementation path.                                           |
| Bank/source capacity and case views            | Extend source occurrence/coverage and preserve existing exact-match identities; do not create a second matching authority.                         |
| Trial-balance snapshots and explanations       | Add explicit opening/profile/coverage semantics; retain old snapshot interpretation.                                                               |
| Recurring preparation                          | Preserve prepare-only authority; add durable group execution/mandates only under explicit policy and proof.                                        |
| Synthetic asset/deferral schedules             | Reuse occurrence identity and exact allocation, then add reviewed register/legal semantics.                                                        |
| Technical close/reopen                         | Keep its limited certificate label; add full domain inventory and financial-close semantics separately.                                            |
| Local backup/fresh restore tools               | Retain refusal boundaries; extend supported data/object/privilege closure deliberately before production use.                                      |
| Existing E2E files and artifacts               | Inspect revision/environment/coverage and authorization; reuse valid observations, add approved missing scenarios before dependent implementation. |

## Packet completion record

Use one record per packet: selected scope/profile; code and migration revisions; implemented operations/consumers; independently expected acceptance cases; environment/fixture provenance; actual observations; remaining limitations; and release status. Link it from the roadmap. A source inspection can establish implementation presence, a synthetic E2E can establish bounded behavior, and a provider acknowledgment can establish a specific external outcome. They are different evidence types.

Avoid calendar estimates until the core fault/recovery checkpoint and actual-source inventory are complete. Thereafter estimate from demonstrated throughput and the selected treatment matrix. “Full parity” is not a single denominator: track completed company workflows and declared capability/profile coverage rather than source-file counts.

## Change control

A changed business requirement or newly discovered source family updates its owning area, the packet dependencies, applicable rule/approval gate and acceptance evidence together. A new implementation convenience does not silently expand the supported profile. Resolve technical tradeoffs locally when they preserve the contract; record a new ADR only when changing ownership, invariants, public semantics or operational authority.

The [FND-01 reconciliation](fnd01-reconciliation.md) is complete for its pinned pre-replacement checkpoint and remains historical input. The next frontier is FND-02/FND-03/FND-04, with the clean-baseline and no-compatibility decisions in [ADR 0010](../adr/0010-application-owned-accounting-replacement.md). Compare subsequent implementation changes against both records before assigning its evidence to another revision. Packet progression does not itself authorize deployment, provider action, test additions or production migration.
