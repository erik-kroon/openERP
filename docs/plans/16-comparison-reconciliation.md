# Accounted comparison: current work and evidence

Status: source and planning review, 2026-09-27. This review maps all 18 FWD proposals to existing work owners. It adds no implementation, tests, company qualification or external acceptance.

## Source and method

- Supplied archive: `drastic_accounted_openerp_deep_comparison_2026-09-27.zip`.
- Archive SHA-256: `9077de3bea5cb7b9dd486e48773f7bc277818ea9a885a0fe598b87e2866098e2`.
- Archive's OpenERP revision: `41410fd75e96361b7c2f407d456019500f39bfbe`.
- Archive's Accounted revision: `a7f0885da2300275225132fa2a648c48fc77bbb0`.
- Current OpenERP review baseline: `d014634ba9ae944d2e08802f9da7e5b9ebd03d58`. The working tree was clean at capture.

The review read the archive's introduction, provenance, findings, common contract, execution order and all FWD packets. It checked the relevant current owners and changes since the archive's OpenERP revision. It did not audit every caller, rerun Accounted, execute the archive's tools or run financial journeys.

The archive remains outside the workspace. Its patch, fixtures and tools are not installed. The hash identifies the reviewed archive; it is not an authenticity check. Accounted findings remain the archive author's observations.

## Decisions

1. Keep the application-owned accounting boundary in [ADR 0010](../adr/0010-application-owned-accounting-replacement.md).
2. Use [Book Zero](15-book-zero-workflow-cash.md) for delivery order. Its first reviewed period and daily work take priority.
3. Assign each remaining task to an existing packet. FWD identifiers are references, not another implementation backlog or completion count. The 53-packet index is unchanged.
4. Keep implementation, observed results, company qualification and external acceptance separate.
5. Preserve the Cash requirements. The comparison does not replace them or make paid services, Accounted migration or payroll mandatory for every company.

## FWD disposition

“Partial” means source exists but some requested behavior or proof remains open. A source observation does not establish runtime correctness.

| Proposal | Current disposition | Existing owner and Book Zero requirement | Remaining task |
| --- | --- | --- | --- |
| FWD-01 — Architecture and readiness | **Completed source change.** README architecture is fixed. Setup warnings now distinguish the manual-journal profile from other operations and from missing company evidence. `bookStatus` retains installed/admitted status and `productionReady: false`. | FND-03; BZ-01, WF-01 | Company qualification continues under FWD-02. No old README patch or readiness override is needed. |
| FWD-02 — Swedish company profile | **Qualification open.** Company-profile resolution and dated admission exist. Company originals and reviewed releases remain required. | FND-03; BZ-01/BZ-09; L0/G0 | Select the first period and applicable families. Bind facts, dates, evidence and reviewers. Exercise missing, ambiguous, withdrawn and stale basis. |
| FWD-03 — Complete accounting journey | **Proof open.** Core E2E evidence exists. It does not cover the proposed sales, credit, payment, purchase and owner-expense journey. | FND-04 with PST/COM/VAT/IMP owners; BZ-06–BZ-11; L1/G1 | Map one bounded journey to real commands. Compare independent GL, bank and register controls at the same cutoff. Retain receipts and unresolved steps. |
| FWD-04 — Credit and owner-expense VAT | **Partial.** Actual-return capture reads admitted facts and purchase components. Customer credit reports `taxConsequenceObserved: false`. The repair record keeps customer-credit and owner-purchase producers open. | VAT-02–VAT-04 with COM-04; BZ-07–BZ-09 | Trace producer-to-return coverage. Complete missing owner links once, with original fact, period and signed tax provenance. Do not repeat the landed source/deductible-tax repairs. |
| FWD-05 — Credit document | **Implementation gap.** Credit issue records `issued_artifact_pending` and a required renderer version. | COM-05 with COM-04 and OPS-03; BZ-07, WF-02 | Render the retained semantic revision. Bind the artifact through an idempotent job. Retry must not issue another credit or number. |
| FWD-06 — Reference-aware matching | **Implementation gap.** Candidate evidence reports `providerReferenceComparison: "unavailable"`. | IMP-03 with COM-03; BZ-07, WF-01 | Resolve ownership of the printed and bank references. Compare typed references without changing approval or residual-capacity rules. |
| FWD-07 — PDF/image extraction | **Implementation gap.** The current native extraction path accepts text media and rejects other media. Durable extraction and field review already exist. | IMP-01/PST-05, supplier-intake capability; AI-01–AI-04, BZ-02 | Add the selected adapter to the existing lifecycle. Preserve bytes, attempts, locators and cancellation. Manual review must remain usable without the provider. |
| FWD-08 — Accounted migration | **Conditional.** Native SIE parsing/import ownership exists. An authorized Accounted source export and semantic mapping are not established here. | IMP-02/IMP-06, OPS-05; BZ-04/BZ-05 | Use this proposal only if Accounted is the selected migration source. Keep migration separate from raw-source reconstruction. Qualify correction history, openings, open items and deduplication. |
| FWD-09 — SIE4E dimensions | **Partial.** Dimension assignments and object-map capture exist. The current exporter refuses a nonempty map because its renderer emits no object records. | END-03/END-06 with dimension/export owners; BZ-12 | Add the required representation when the selected book uses dimensions. Preserve refusal until render/parse/compare and recipient import prove fidelity. |
| FWD-10 — External outcomes | **Partial; old repair closed.** Explicit fulfillment reverification and current-observation checks landed in `ec08945`. Provider/environment acceptance remains separate. | END-07/OPS-03; BZ-09/BZ-12/BZ-14 | Qualify the selected provider path and its evidence. Reuse reverification; do not rebuild it from the older pending note. |
| FWD-11 — Durable consumers | **Partial.** The Bun runner composes preparation, extraction and period-work queues. Invoice delivery still reports simulation/provider-blocked states. | PST-05/OPS-03 with COM-05; WF-03/WF-06, BZ-13 | Inventory event-to-consumer coverage for the selected journey. Complete missing consumers and observe restart, duplicate delivery, cancellation and unknown outcomes. |
| FWD-12 — Paid services | **Deferred service decision.** ADR 0005 keeps core accounting independent of paid entitlement. No entitlement owner was found in the inspected API source. | ADR 0005; provider/service owner once selected | Choose a specific managed service before adding cost gates. It is not a Book Zero prerequisite. Billing must not grant approval or block historical receipts. |
| FWD-13 — Coherent work UI | **Partial.** The work route already uses `AttentionList`, `SavedWorkViews` and `PostingRecoveryPanel`. NEXT-16 now supplies bounded batch APIs. | FE-01–FE-04/FE-06 with PST-02/PST-03/PST-05; WF-01–WF-08; L2/G2 | Complete the priority source-to-review-to-receipt journey in the existing UI. Prove book context, return navigation, partial results, recovery and accessibility. |
| FWD-14 — Payroll/AGI | **Conditional, partial.** Foundation and frozen payroll calculation exist. The calculation owner explicitly does not post, pay or declare. | PAY packets; BZ-10 and applicable Cash contributions | Establish applicability first. Qualify each required execution/declaration step or an explicit external-payroll handoff. A calculation is not a payroll release. |
| FWD-15 — Restore and archive | **Partial.** Recovery tooling and a local replacement rehearsal exist. Restricted application recovery, custody and production promotion remain open. | OPS-01/OPS-02/OPS-04–OPS-07; BZ-13/BZ-14, NFR-06; L6/G6 | Rehearse the selected deployment's DB, object, key and pending-delivery recovery in quarantine. Preserve one authorized writer and dispatch owner. |
| FWD-16 — Journey proof | **Partial; evidence model exists.** Book Zero already specifies gate records. Bend now has retained synthetic host-qualification evidence as well as offline checks. | FND-04 and existing verification records; all G gates | Extend the existing evidence record for each journey. Do not create a second proof ledger. Preserve the distinction between synthetic host qualification, deployment approval and company acceptance. |
| FWD-17 — Caller authority | **Inventory open.** MCP includes capabilities unless `agentCallable` is false. This confirms the catalog policy, not an authorization bypass. | FND-02/PST-04; AI-04, NFR-02 | Classify current callers and explicit capability exposure. Check owner admission and recovery before changing defaults. Cover human-only operations and internal posting authority. |
| FWD-18 — Capture size | **Conditional qualification.** Register capture has explicit record/byte bounds; VAT capture also refuses excess populations. NEXT-16 execution has a cursor, which does not solve report completeness. | FND-04 and each capture owner; BZ-03/BZ-11, NFR-04 | Measure the selected source population. Change only a bound that blocks the selected profile. Pin membership, cutoff, count and final digest across pages. |

## One execution order

Use these groups to schedule existing owners. They are not new packet IDs.

The order governs release decisions. Independent engineering and synthetic checks can start while company inputs are still missing.

| Order | Deliverable | FWD references | Exit condition |
| --- | --- | --- | --- |
| 1 — Scope and truthful status | FND-03 establishes the first period, applicable families, sources and missing facts. Correct stale setup copy within the same work. | 01, 02 | Book Zero G0: named scope, evidence, reviewer and unknowns. A selected profile is not yet a verified period. |
| 2 — Complete the selected journey | COM/VAT/IMP owners close required credit, document and intake gaps. FE owners connect the same operations through the current work UI. | 04, 05, 06, 07, 13 | Each required step has a real owner operation and a usable review/recovery path. Reference matching can proceed independently. PDF/image work needs a selected adapter and provider terms where applicable. |
| 3 — Prove behavior and authority | FND-04 coordinates one journey; FND-02/PST-04 check caller authority; PST-05/OPS-03 check delivery and recovery. Start this work alongside order 2. | 03, 11, 16, 17 | G1/G2: independent controls, immutable receipts and observed failure/recovery cases for the declared scope. Test changes need separate approval. |
| 4 — Year handoff and operation | END and OPS owners qualify export, restore and any required external outcome. | 09, 10, 15 | G4/G5/G6 as applicable: accepted review pack, new-period operation and separately authorized cutover. File-based review need not wait for a bank connector. |
| Conditional work | Source-specific migration, managed services, payroll and larger captures. | 08, 12, 14, 18 | Start when source choice, service scope, company applicability or measured volume requires it. Do not hide an applicable gap as “not applicable.” |

Book Zero L3/L4 still owns Cash basis and forecasting. It can proceed when its authoritative reads are qualified. The archive's synthetic golden journey is a proposed oracle, not the company's source inventory or permission to add tests.

## Evidence and source reading order

| Area | Current source or maintained record | Review limit |
| --- | --- | --- |
| Architecture and admission | [README](../../README.md), [posting setup/status](../../apps/api/src/application/posting.ts), [company basis](../../apps/api/src/application/company-profile-basis.ts), [posting admission](../../apps/api/src/application/posting-admission.ts) | Setup/status and owner boundaries checked; no new company activation performed. |
| Credits and VAT | [credit notes](../../apps/api/src/application/commerce/credit-notes.ts), [actual-return workflow](../../apps/api/src/application/vat/actual-return.ts), [capture reads](../../apps/api/src/db/vat/actual-return.ts), [landed repairs](evidence/latest-landed-review-repairs.md) | Retained flags and capture inputs checked. Complete producer/caller qualification remains work. |
| Intake and matching | [extraction](../../apps/api/src/application/purchases/extraction.ts), [text engine](../../apps/api/src/application/purchases/extraction-engine.ts), [candidates](../../apps/api/src/application/banking/candidates.ts) | Media refusal and reference-comparison status checked; no provider exercised. |
| Source history and export | [SIE parser](../../apps/api/src/application/sie-import-parser.ts), [SIE4E workflow](../../apps/api/src/application/sie4e.ts), [renderer/comparison](../../jurisdictions/se/src/sie/sie4e.ts) | Source representations and dimension refusal checked; no Accounted import or recipient export acceptance. |
| Work and authority | [work route](../../apps/web/src/routes/entities.$entityId.books.$bookId.work.tsx), [period work](../../apps/api/src/application/period-work.ts), [MCP catalog](../../apps/api/src/transport/mcp.ts) | Existing composition and catalog predicate checked; not a complete authority or browser audit. |
| Jobs and external outcomes | [runner](../../apps/api/scripts/preparation-runner.ts), [invoice delivery](../../apps/api/src/application/commerce/invoice-delivery.ts), [fulfillment](../../apps/api/src/application/closing/fulfillment.ts) | Queue composition, simulation states and reverification checked; no live provider result inferred. |
| Payroll and scale | [payroll calculation](../../apps/api/src/application/payroll/calculations.ts), [register reports](../../apps/api/src/application/register-reports.ts) | Calculation-only boundary and capture limits checked; applicability and volume not supplied. |
| Recovery and services | [recovery CLI](../../apps/api/scripts/operations/cli.ts), [local recovery](../operations/local-recovery.md), [ADR 0005](../adr/0005-open-accounting-and-managed-services.md) | Existing tooling and recorded rehearsal identified; no restore or entitlement release performed. |
| Proof | [NEXT integration evidence](next-packet-progress.md#verification-limits), [Bend qualification](../../verification/bend/authority/docs/QUALIFICATION.md), [Book Zero gates](15-book-zero-workflow-cash.md#acceptance-and-verification-record) | Prior results are attributed records. This review did not rerun those financial checks. |

## Maintenance

Update implementation and proof status in the existing owner records. Update this mapping only when ownership or scope changes. Keep dated evidence and external source files unchanged unless a correction is clearly marked.

Use direct verbs, short sentences and one term for each concept. Keep exact API names and necessary accounting terms. Remove duplicate guidance instead of adding another summary. These are Orwell and ASD-STE100-style writing principles, not a claim of certified ASD-STE100 compliance.

## Documentation checks

Run `python3 docs/plans/check-plan.py` after edits. It validates local links, anchors, packet ownership tables and dependency order, then updates [planning integrity](evidence/planning-integrity.json). This review preserves FWD-01 through FWD-18 in the disposition table and leaves the 53 accounting packets unchanged. Documentation checks do not execute the proposed financial cases.

## Execution record

### FWD-01 — Readiness communication

Completed on 2026-09-27 against baseline `122cf94`. The remaining source change corrects `bookSetup` warnings in `apps/api/src/application/posting.ts`. It removes the false claim that tax treatment and statutory reporting have no implementation. It states the manual-journal profile limit and the separate evidence required for live company use.

Source review confirmed that `bookStatus` already reports installed and admitted families separately. Its unresolved-family blockers and `productionReady: false` remain intact. The README architecture and fulfillment reverification fixes were already present; this packet does not repeat them.

Verification: `bun run check:changed` and `bun run check:changed:full` passed. This is a copy and source-consistency result, not company qualification or a new financial-journey observation. No tests or fixtures were changed.
