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
| FWD-02 — Swedish company profile | **Blocked on company inputs.** The user directed independent work to continue. Company-profile resolution and dated admission exist; originals, the first period and reviewed releases remain required. | FND-03; BZ-01/BZ-09; L0/G0 | Supply the selected period, company records and reviewer. Keep D-04/D-06/D-08 open; synthetic cases cannot close qualification. |
| FWD-03 — Complete accounting journey | **Proof open.** Core E2E evidence exists. It does not cover the proposed sales, credit, payment, purchase and owner-expense journey. | FND-04 with PST/COM/VAT/IMP owners; BZ-06–BZ-11; L1/G1 | Map one bounded journey to real commands. Compare independent GL, bank and register controls at the same cutoff. Retain receipts and unresolved steps. |
| FWD-04 — Credit and owner-expense VAT | **Implemented and verified in an isolated synthetic run.** Capture reads published owner-purchase and credit components, with exact original-fact lineage, period checks and currentness. | VAT-02–VAT-04 with COM-04; BZ-07–BZ-09 | Keep actual-company and filing qualification separate; see [VAT capture](../../apps/api/docs/VAT-RETURNS.md). |
| FWD-05 — Credit document | **Implemented and E2E-verified in the synthetic exercise.** The retained semantic revision now renders to PDF through HTTP or the Bun consumer, with immutable artifacts and current failure/progress state. | COM-05 with COM-04 and OPS-03; BZ-07, WF-02 | Keep actual-company, VAT-return, delivery and browser qualification separate. See [credit document scope and proof](../../apps/api/docs/CREDIT-DOCUMENTS.md). |
| FWD-06 — Reference-aware matching | **Implemented and E2E-verified for issued synthetic invoice numbers.** Dedicated statement references compare against issued documents through active commerce allocations. | IMP-03 with COM-03; BZ-07, WF-01 | Keep OCR, legal-invoice/provider and actual-company qualification separate. See the [candidate owner](../../apps/api/docs/BANK-MATCH-CANDIDATES.md) for exact scope and artifacts. |
| FWD-07 — PDF/image extraction | **Implementation gap.** The current native extraction path accepts text media and rejects other media. Durable extraction and field review already exist. | IMP-01/PST-05, supplier-intake capability; AI-01–AI-04, BZ-02 | Add the selected adapter to the existing lifecycle. Preserve bytes, attempts, locators and cancellation. Manual review must remain usable without the provider. |
| FWD-08 — Accounted migration | **Conditional.** Native SIE parsing/import ownership exists. An authorized Accounted source export and semantic mapping are not established here. | IMP-02/IMP-06, OPS-05; BZ-04/BZ-05 | Use this proposal only if Accounted is the selected migration source. Keep migration separate from raw-source reconstruction. Qualify correction history, openings, open items and deduplication. |
| FWD-09 — SIE4E dimensions | **Partial, locally verified.** The v2 profile emits original transaction dimensions and exact object codes. Native round-trip checks pass. Dimensional openings and recipient acceptance remain open. | END-03/END-06 with dimension/export owners; BZ-12 | Extend the opening-object representation when needed, then qualify the actual recipient import. Unsupported representations still refuse. |
| FWD-10 — External outcomes | **Partial; old repair closed.** Explicit fulfillment reverification and current-observation checks landed in `ec08945`. Provider/environment acceptance remains separate. | END-07/OPS-03; BZ-09/BZ-12/BZ-14 | Qualify the selected provider path and its evidence. Reuse reverification; do not rebuild it from the older pending note. |
| FWD-11 — Durable consumers | **Partial.** The Bun runner composes preparation, extraction and period-work queues. Invoice delivery still reports simulation/provider-blocked states. | PST-05/OPS-03 with COM-05; WF-03/WF-06, BZ-13 | Inventory event-to-consumer coverage for the selected journey. Complete missing consumers and observe restart, duplicate delivery, cancellation and unknown outcomes. |
| FWD-12 — Paid services | **Deferred service decision.** ADR 0005 keeps core accounting independent of paid entitlement. No entitlement owner was found in the inspected API source. | ADR 0005; provider/service owner once selected | Choose a specific managed service before adding cost gates. It is not a Book Zero prerequisite. Billing must not grant approval or block historical receipts. |
| FWD-13 — Coherent work UI | **Partially implemented in four committed slices; not browser-verified.** The queue announces and counts honestly, returns from a record to the same filtered queue, reads a period-work run with a bounded pass and cancellation, and can now seal, approve and execute an approval batch with its committed and refused members reported separately. | FE-01–FE-04/FE-06 with PST-02/PST-03/PST-05; WF-01–WF-08; L2/G2 | Exercise the whole priority journey in a browser, which needs an approved web test harness. Supplier extraction still has no deep-linkable route of its own and period cancellation is still absent from the MCP catalogue. |
| FWD-14 — Payroll/AGI | **Conditional, partial.** Foundation and frozen payroll calculation exist. The calculation owner explicitly does not post, pay or declare. | PAY packets; BZ-10 and applicable Cash contributions | Establish applicability first. Qualify each required execution/declaration step or an explicit external-payroll handoff. A calculation is not a payroll release. |
| FWD-15 — Restore and archive | **Partial.** Recovery tooling and a local replacement rehearsal exist. Restricted application recovery, custody and production promotion remain open. | OPS-01/OPS-02/OPS-04–OPS-07; BZ-13/BZ-14, NFR-06; L6/G6 | Rehearse the selected deployment's DB, object, key and pending-delivery recovery in quarantine. Preserve one authorized writer and dispatch owner. |
| FWD-16 — Journey proof | **Proof infrastructure implemented and exercised.** The existing runner binds tracked/untracked inputs, checks source stability and preserves prior runs. Journey records and release limits remain in this plan and the verification strategy. | FND-04 and existing verification records; all G gates | Add each later journey's actual evidence. Infrastructure completion does not close unexecuted company or external gates. |
| FWD-17 — Caller authority | **Catalog policy implemented and E2E-verified.** Every write is classified; unclassified writes and human-only operations are withheld. Current owner admission still governs every caller. | FND-02/PST-04; AI-04, NFR-02 | Keep the live inventory and owner checks current. Family-specific financial and job-race proof stays with its owning packet. See [MCP authority](../../apps/api/docs/MCP.md#exposure-policy-and-callers). |
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

### FWD-06 — Failure contract before implementation

The user approved focused E2E tests on 2026-09-27. Company qualification remains blocked; this packet uses synthetic records through the real HTTP owners.

The existing candidate owner compares posted bank lines, not unpaid invoices. Reference evidence must follow a committed commerce allocation from its payment voucher to the retained invoice number. The printed document and the matcher must use that same number. A provider transaction ID or free text is not a payment reference. OCR generation is not present in the inspected invoice owners; OCR must stay a distinct, non-comparable type in this profile.

Required failure cases: equal amounts with different invoice numbers; free text posing as a reference; wrong issuer or reference type; punctuation or leading-zero changes; an unallocated payment; opposite cash direction; unsupported currency; another book; exhausted match capacity; repeated discovery with no financial mutation. A reference match must not override any existing eligibility check or establish identity. Retain the generated document, reference comparisons and match receipts with the E2E artifacts.

### FWD-06 — Delivered profile and observations

The issued synthetic invoice-number profile now retains typed source references, compares exact issuer/type/value and exposes document/allocation provenance. The current UI explains reference matches and non-comparable inputs. The ranking remains advisory; normal eligibility and matching authority still apply.

The E2E journey also exposed and repaired four prerequisites: ordinary draft creation incorrectly required the optional recurrence field; commerce allocation approval checked `digest` instead of `planDigest`; candidate period SQL omitted fields it read; and capacity helpers shadowed the caller's SQL aliases. The last defect assigned another row's matched capacity to unrelated candidates. The shared helpers now use distinct aliases.

Verification on 2026-09-27: fast and full changed-file checks passed, including web and test types. The real PostgreSQL/workerd suite passed all 24 tests. The new journey retains `test-results/e2e/bank-reference-journey.json` and `bank-reference-candidates.json`; the suite retains its source manifest and results. No financial records were seeded directly in SQL. The fixture provisions only synthetic identity, accounts and periods.

This closes the delivered synthetic reference profile, not OCR, legal-invoice/provider qualification, browser acceptance or actual-company readiness. Those limits remain explicit in the owner document.

### FWD-17 — Failure contract before implementation

Inventory the current catalog before changing exposure. Read operations already declare `readOnly`; every write needs an explicit classification. Missing write classification must withhold the tool. An owner's `agentCallable: false` must still override catalog policy.

The current catalog exposes names for human-only company fact review, role binding, firm administration and company setup. Source admission already requires an operator or human session. Hide these unusable authority tools without granting new authority elsewhere. Keep supported preparation and execution of human-approved work available.

E2E cases must cover the advertised catalog, direct calls to hidden names, forged posting-owner fields, wrong-book execution, exact approved agent execution, same-key recovery, changed-input conflict, and revocation before a new effect. Retain the complete classified catalog and observed receipts. Existing HTTP admission tests continue to check the owning boundary; catalog policy does not replace it.

### FWD-17 — Delivered policy and observations

The MCP catalog now requires explicit write classification. Reads retain their declared read policy, and owner exclusions still apply. Human review, administration, activation and operator-only period work are withheld from both discovery and invocation. The existing prepare/approved-execution path remains available under current owner admission.

The new E2E case passed through the real MCP endpoint. It observed catalog exclusions with both agent and operator tokens, rejected forged owner arguments and another book, committed and replayed an approved journal, rejected changed input, and refused a revoked agent before dispatch. An authorized operator recovered the existing receipt. The full PostgreSQL/workerd suite passed all 25 tests; fast and full changed-file checks also passed.

`test-results/e2e/mcp-authority-journey.json` retains every current capability's classification and exposure, the live catalog and financial receipts. The [MCP caller map](../../apps/api/docs/MCP.md#exposure-policy-and-callers) records web/REST, MCP, Bun and operator-script boundaries. This is not a claim that every owner-specific financial journey or background race has been exercised.

### FWD-16 — Failure contract before implementation

The existing E2E manifest records HEAD, a tracked diff hash, lockfile and migrations. `git diff HEAD` omits new untracked source and test files. A passing result can therefore lack the identity of code it actually ran. The next run also deletes the prior artifact directory.

Extend the existing manifest and runner, not a second proof system. Capture tracked and untracked inputs in declared source roots before startup. Record deleted tracked inputs, reject symlinks, and fail if the source inventory changes before teardown. Preserve the previous local run before starting another. The E2E check must verify hashes for the actual test, API and contract files while calling the real Worker. A missing, changed or unrecorded input cannot count as fixed-revision proof. Company and external gates remain open.

### FWD-16 — Delivered evidence contract

The existing runner now captures declared repository inputs before startup, including new untracked files. Its manifest stores per-file hashes and a combined inventory hash. Teardown compares a second inventory and fails if it differs. Previous local runs move into `test-results/e2e-history` instead of being deleted. The [suite evidence contract](../../apps/api/tests/README.md#run-evidence) defines what to inspect and what the inventory excludes.

The new real-Worker E2E case first failed because the old manifest lacked source identity. After implementation it passed, including this test file while it was still untracked. The full suite passed all 26 tests. The observed startup and teardown inventory hashes agreed. Prior-run directories were retained. Symlink refusal and deleted-file representation are source-inspected behavior; this run did not inject those failures or change code during execution.

Use the existing Book Zero gates as the release record:

| Gate | Current result | Evidence or missing prerequisite |
| --- | --- | --- |
| G0 — Company scope | Blocked | FWD-02 needs originals, first period and reviewer; D-04/D-06/D-08 remain open. |
| G1 — Reviewed first period | Open | Synthetic reference and core posting journeys pass. The full company period, credits/VAT coverage and independent controls are not yet observed. |
| G2 — Daily work | Partial technical evidence | FWD-06 and FWD-17 retain HTTP/MCP receipts. Browser workflow, accessibility and complete period-work recovery remain open. |
| G3 — Cash | Open | No Cash forecast qualification is claimed by these packets. |
| G4/G5 — Year handoff and new period | Open | Require the actual period/year basis and independent reviewer acceptance. |
| G6 — Cutover | Open | Local recovery evidence does not establish deployed object/key recovery or authorize writer/provider promotion. |
| G7 — External pilot | Open | Requires the verified profile, permitted data and operating acceptance. |

Bend's retained synthetic qualification remains a separate evidence lane. Neither these E2E results nor documentation checks activate a legal rule, deploy a candidate, file a return or qualify a real company.

### FWD-05 — Failure contract before implementation

Render the existing immutable `CustomerCreditSemanticDocument` as PDF. Preserve the issue receipt's historical `issued_artifact_pending` value; a separate artifact view reports current pending, failed or available state. The renderer must copy retained amounts and parties, not calculate tax or read current customer details. PDF creation is neither delivery nor a refund.

The issued outbox intent must survive an offline runner. The effect-mq Bun consumer must use the same scoped rendering operation as HTTP. Bind document ID, revision, digest and renderer version to one immutable artifact; seal it and acknowledge the exact outbox row in one short transaction after rendering.

Before implementation, the E2E obligations are: three-person policy/review admission on an isolated synthetic book; native issue and credit without direct financial SQL seeds; wrong document digest and wrong book refusal; duplicate render/replay without new numbering or ledger effects; renderer refusal with retained failure state; restart discovery of an unprocessed intent; exact retained parties/amounts; immutable original credit receipt; and downloadable PDF bytes with a verified hash. The synthetic exercise does not qualify Drastic's company facts or change `taxConsequenceObserved`.

### FWD-05 — Delivered artifact and observations

The PDF renderer, immutable artifact/failure storage, HTTP/MCP operations and effect-mq consumer are implemented. Migration `0022-credit-document-artifacts.sql` binds the exact document revision and content hash. Artifact sealing and outbox acknowledgment share one transaction; rendering holds none. The issue receipt remains immutable, while a separate view reports current artifact state.

The native journey and source review found three prerequisites. Private kernel approval needed the credit owner's context. Source admission needed to permit the exact original issue referenced by that retained credit review. Document hashing included an evidence field that its wire schema removed. The fixes preserve public generic-approval refusal and bind the exact original review, issue and digest.

Fast and full changed-file gates passed. The full workerd/PostgreSQL suite passed all 27 tests, including native invoice/credit issue, direct workerd rendering, real Bun consumption of offline intents, unsupported-font failure, scoped download, same-key replay and an injected late acknowledgment fault. The fault rolled back the artifact; retry recovered with no new financial effect. Source integrity remained stable.

The retained PDF was independently parsed through the file reader. It showed `TEST-2`, original invoice `TEST-1`, the frozen customer name, and `20,00` net / `5,00` VAT / `25,00` credited total. Full run artifacts and reproduction commands are listed in the [owner document](../../apps/api/docs/CREDIT-DOCUMENTS.md#verification).

Later FWD work remains open; company-input blockers are unchanged.

### FWD-04 — Failure contract before implementation

Owner-paid purchases already publish `owner_purchase_tax_facts`. Customer credits already publish `customer_credit_tax_corrections`. Capture those records once; do not republish them into the manual fact store.

The original sale remains with the existing reviewed VAT-fact admission owner. A credit requires one current original sale fact linked to the exact original voucher, with the full retained invoice totals and a tax point inside the same selected registered VAT period. Missing, withdrawn or ambiguous originals refuse. This avoids inventing a tax point from invoice or supply dates. Cross-period credits remain unsupported in this slice.

Retain signed source tax separately from deduction. Link owner-purchase components through their retained journal ordinals and credits through their exact output-VAT line IDs. A zero deduction or zero tax needs no invented monetary line. New source membership or changed observations must make an old return stale without rewriting its saved amounts. Duplicate manual/owned representations must not produce a complete return.

Independent synthetic vector: a native sale has net `10000` and VAT `2500`; a credit releases net `2000` and VAT `500`. An owner purchase has source VAT `250` with deduction `125`, plus source VAT `100` with zero deduction. Expected output VAT is `2000`, input VAT `125`, and exact net `1875`. With the fixture's whole-SEK truncation, reported boxes 10/48/49 are `20`/`1`/`19`; net residual is `-25`. A later credit must invalidate currentness and leave the first saved return unchanged.

The test configuration is confined to a disposable synthetic book. It exercises native financial operations and reviewed-input boundaries; it does not supply or qualify Drastic's real company records.

### FWD-04 — Implemented producer boundary

Capture now reads `owner_purchase_tax_facts` and `customer_credit_tax_corrections` directly. It retains source VAT separately from deduction, the credit's original reviewed fact link, exact control-line provenance and producer populations. Currentness includes these inventories, withdrawal state and the current profile witness. Registered windows must match the reviewed cadence; a yearly window must match a retained fiscal year.

The native journey found and repaired three prerequisites: VAT fact admission read a nonexistent voucher `body` column instead of `action`; the economic-key wire pattern rejected valid uppercase supplier document numbers; and owner approval row locking lacked its required column privilege. Existing economic keys remain unchanged. The approval table's immutable trigger still rejects updates. A zero-tax credit also needed the legal posting schema to allow its two real journal lines.

The targeted journey passed its positive and negative cases. All 28 assertions then passed in the shared checkout, but concurrent source changes invalidated that run's fixed-revision evidence. That run was not accepted as proof. The source-integrity guard now also sets a nonzero process exit code before reporting a teardown mismatch.

Final verification used the existing `next/NEXT-16b` worktree at `a99c4dd` plus the order-independent test assertion included with this record. Frozen installation, `bun run check:changed db37fce`, `bun run check:changed:full db37fce` and all 28 PostgreSQL/workerd E2E tests passed. Source integrity was stable at `2a483913b619ed695fdaa23fb6599c51e7af4a0fe847805c6651335f4762a9e6`. The worktree retains `test-results/e2e/owned-vat-journey.json`, its manifest, source-integrity result and suite reports. This proves the committed VAT slice independently of ongoing UI/queue edits on main.

### FWD-13 — Delivered interface slices and observations

Three committed slices, each web-only. No `apps/api` or contract source changed, so the slice did not compete with the FWD-05 and FWD-04 work in progress.

**The queue now says what it is showing.** The result count is a live region. The open and completed split is shown next to it, and it says which scope it reports: the server counts that split across every status inside the filter, while the result total follows the chosen status, so the caption does not present one list as the other. A page that does not show every result says how many of how many it showed, because the read is bounded at 51 rows. The route is a focusable landing region, matching the recovery and review sections, so returning to it can move focus.

**Return navigation closes for every attention kind.** The journal review already carried period, status, sort and search; the type filter was the one part it dropped. The invoice and expense record pages carried nothing and offered no way back at all, so a reviewer who filtered the queue and opened an expense returned to an unfiltered one. Both areas now take the queue's search as one opaque `work` parameter and show a "Back to work" action, and it rides along with the record, the tabs and each row. The parameter is opaque for a real reason: a sales `status` is a draft state, not a work state, so the same name cannot be reused. A page decodes it and re-validates it with the queue's own schema before use, so an edited parameter is dropped by that schema instead of being echoed into a link. The queue cursor is deliberately not carried, so a record returns to the first page of the same filtered list. Accounts, reports, tax and closing are excluded rather than given a parameter their route schemas would drop.

**Period work is readable from the queue.** All seven operations had no web surface. The work route now takes a prepared selection by identifier and reads its progress, the nine child-state counts kept distinct, and each child's routed owner, prepared plan, approval batch, missing facts and refusal reason, with a bounded pass and a cancellation through the owning operations' own paths. It says the run is not a reconciled period and reports whether the captured source population was complete, because a run whose children were all visited is neither claim.

Three limits are deliberate, not omissions of time. The page reads a prepared selection and does not create one: a selection is frozen from a consistent capture and sealed with its rules, and a selection owner in this interface would be a second authority. The bound on one pass is left to the owning operation, whose own maximum is not in any contract, so an out-of-range count is refused there and its reason is shown as it arrived. The carried selection is part of where the queue is and not a filter on the list it shows, so the attention read receives only the fields it filters on.

**A locale leak in the source chain.** The supplier extraction panel showed raw English request states to a Swedish reader and Swedish-only merge states to an English reader. All four word tables are now per locale and stay exhaustive against their contract literals, so a new state cannot be added without a word for it.

**Dead code removed.** The superseded work list had no importer and a second, divergent result announcement. It is deleted rather than kept in step.

**A pre-existing limitation of the changed-file gate, not of these changes.** Its scoped project contains only the selected files and their imports, and the generated route tree is an import of no route file, so `FileRoutesByTo` is empty and every `createFileRoute` path argument errors. This reproduces on an unmodified work route with a comment-only edit on a clean tree, and it applies to every route file in this repository. Each slice was therefore verified with the project's own `apps/web` type check, type-aware lint, formatting and a full `apps/web` build, all of which pass.

**What is not verified.** No browser journey was exercised. No screen, focus order, 200% zoom, narrow width or reduced-motion behaviour was observed, and no period-work financial effect was produced. The repository has no web test harness, `docs/frontend.md` does not authorize new test files, and this packet added none. The return round trip was exercised instead as a computation over the real TanStack search serializer and parser and the real Effect schemas, covering identifiers, spaces, apostrophes, ampersands, hashes, non-ASCII text, a numeric search and JSON-parseable values; every case returned the same filter set, an empty set produced no parameter, an invalid status was dropped and an over-long value was refused by the schema. That is arithmetic and wire-shape evidence, not screen evidence.

### FWD-09 — Failure contract before implementation

The selected slice adds original transaction dimensions to the existing synthetic SIE4E export. Section 6 of the pinned 4C specification makes `#DIM`, `#OBJEKT`, `#OIB` and `#OUB` optional for 4E. Section 8.17 reserves dimension numbers below 20. The export must therefore freeze its own deterministic mapping from native dimension codes to numbers starting at 20, and preserve native object codes as strings. The existing report object-map numbering is not a SIE semantic classification.

Given an established untagged opening and native vouchers carrying two dimensions, preparing an export through the public API must retain the original assignments, emit declarations and exact transaction object groups, and compare the bytes with the independent inbound parser. Leading zeroes, case, Swedish labels, signed amounts and voucher/line identities must survive. Later catalogue edits and archive changes must not rewrite old labels or saved bytes. The renderer release must distinguish new captures from retained v1 captures.

Failures to exercise before accepting the slice: missing or changed object declarations; removed, swapped or duplicated transaction assignments; an unknown object reference; unsupported CP437 text; conflicting retained labels for the same object code; dimension assignments in an opening balance that this transaction-only object profile cannot represent; wrong-book reads; changed input under the same idempotency key. Bounded reads must detect overflow rather than truncate assignments. Non-value assignment states remain distinct in retained membership and never become invented SIE objects. A failed render leaves no attached verified artifact and can be retried against the same frozen capture.

The decisive check is a native PostgreSQL/workerd journey, with API-created postings and catalogue revisions, exact downloaded bytes, independent parse/compare mutations, ledger observations and a retained `sie-dimensions-journey.json`. Run `bun run test:e2e apps/api/tests/sie-dimensions.e2e.test.ts`. Recipient import, company qualification, dimensional opening balances and general SIE certification remain separate gates.

### FWD-09 — Verified transaction-object slice

New captures use `openerp-sie4e-v2`, with a frozen native-code-to-SIE-number map and original assignments on every retained line. The capture reads exact dimension revisions, not current catalogue heads. Codes, labels, source references and non-value states stay in the retained membership. Conflicting labels refuse rather than selecting one silently. The old renderer version remains readable; the selected record family does not emit object balances.

The failure-first journey found two prerequisite defects. Catalogue writes required table-wide UPDATE privileges even on immutable revision and receipt tables; the guard now requires the actual SELECT/INSERT access, while PostgreSQL checks the catalogue heads' existing column grants. The old export also accepted dimension-tagged prior history and lost its opening representation; the v2 capture now refuses that case.

`bun run check:changed:full` and all **31 PostgreSQL/workerd E2E tests** passed in the isolated worktree. Source inventory stayed stable at `0db921ff43a634e1cf43a8e16e71510822215b2ccf06e99b28a15fb5a693107f`. The journey verifies two dimensions mapped to 20/21, exact `0012` and `Case-A` object codes, Swedish quoted labels, native account opening/movement/closing controls, unchanged ledger state, archive-insensitive recapture, replay, wrong-book refusal and changed-input conflict. Six altered byte files fail independent parse/compare. Additional cases reject conflicting labels, dimensional openings and unsupported CP437 text, with failed captures remaining unattached on retry.

Evidence is retained in the worktree's `test-results/e2e/sie-dimensions.SE`, `sie-dimensions-journey.json`, manifest, integrity result and suite reports. These results close the local transaction-object slice, not FWD-09's recipient-import gate, dimensional openings or Book Zero acceptance.

Workspace type checks, the web build they invoke, formatting and document integrity also passed. These structural checks do not add browser or recipient-import evidence.

### FWD-11 — Failure contract before implementation

Four job kinds share one physical queue: preparation, supplier extraction, period work and credit-document render. All four carry a deterministic idempotency key, so the effect-mq store admits a repeat with `ON CONFLICT DO NOTHING` and reports it as a duplicate. That is the correct behaviour for a redelivery and the wrong behaviour for a recovery: after five attempts the job row is terminally `failed`, and every later enqueue is a silent no-op that changes nothing and is not reported anywhere. Only the preparation dispatcher reads the queue state. The other three call `enqueue` unconditionally.

**The extraction case is an availability defect, not an inconvenience.** `claimReadyExtractionRequests` selects `state = 'ready'` and increments `attempts_made` on every poll. The terminal job means the handler never runs again, so the request never leaves `ready`, so the counter grows by one every thirty seconds until it reaches the reviewed ceiling of 1000. That ceiling is a `CHECK`, so the next increment violates it, `claimPendingSupplierExtractions` fails as a whole, and installation-wide extraction dispatch is dead. The runner logs a warning every thirty seconds and nothing else. The three other kinds have the same no-op hole without the ceiling.

**The required failures, before any code:** a handler that raises a typed refusal rather than a defect; five genuine attempts followed by a terminally failed row; a job row deleted between the claim and the enqueue; a record whose `attemptsMade` is already at its maximum on the first sight; a rearm budget already spent; a stop that loses to a handler that advanced in between; a claim query that selects nothing; a stop that must not run for a request another actor owns.

**What the fix must not do.** It must not acknowledge or delete an intent that has no result, because acknowledgement is the statement that the effect happened. It must not widen a bound to make a failure fit. It must not retry a job whose state is not `failed`, because `retry` resets the attempt counter and would let a stuck row loop. It must not turn a runner's inability to deliver into a domain outcome: an exhausted extraction is an unknown outcome, not a completed one, and an exhausted period-work pass is a review case, not a settled child. A cancellation is still a cancellation and must not be rearmed.

**The budget is the same one preparation already uses.** Attempt history survives retries and bounds automatic rearming, so a job may be rearmed a bounded number of times and then stops being enqueued. One constant, one meaning, one place.

**Verification.** The dispatch decision is exercised as a table over the queue snapshot: absent record, `waiting`, `delayed`, `running`, `failed` below the budget, `failed` at the budget, and `cancelled`. The settle is exercised against a real database for the refusal that matters most: a request that has exhausted delivery stops being claimed, and the claim query still returns every other ready request. Credit-document render gets the per-row defect fence the other three already have, because one unreachable queue row currently abandons the whole poll. This packet changes no contract, no state literal, no web copy and no migration; where an honest settle would need one of those, the gap is recorded instead of worked around.

### FWD-13 — Delivered batch gesture and its limits

The fourth slice closes the last period-work operation that had no interface. An operator can now select the reviewed proposals one gesture is about to cover, see what that gesture covers, and read back what a pass actually did.

**Selection mirrors the published rules instead of deciding eligibility.** A member is a prepared child with a sealed plan, a routed owner and that owner's review, read from the child's own retained record, which is the same record the owning operation reads them from. A child waiting on an earlier child, or without a sealed plan or an owning review, states why it cannot be a member instead of offering a checkbox that would be refused. If this page and the owning operation ever disagree, the operation's refusal is displayed.

**The sealed batch is read back, not trusted.** Its members are shown with their owner, plan and owning review, together with the digest the operator is about to approve and the combined figure marked informational, because that figure is never a journal line and never a balancing figure. Approval is gated on an explicit acknowledgement that these are synthetic-only effects and that a member whose owner refuses is left for review rather than retried. Approval and execution are operator-only, and a non-operator reading the same page is told so instead of being offered a dead button.

**Execution reports two separate results.** Committed members with their receipts, refused members with their reason, and the cursor for the next pass, so eleven completed and one blocked read as those two facts. The cursor is the previous result's, so a second press continues rather than restarts, and the identity key binds the exact batch, digest and page, so a lost response recovers that page. It ends by restating that the run is not a reconciled period.

**A path and its body now travel together.** Each period-work command returns its own path and request as one value, so a body cannot be posted to a different path than the one its identity key was derived from. That closed a real seam in the advance and cancel paths, which built their two halves at separate call sites.

**Two exports were added to the period-work contracts, and both are the same value rather than a second one.** The sealed batch shape its own endpoints return, so a client can read back what it is about to approve rather than trust the members it asked for, and the member bound the owning operation already enforces, restated so a selection can be bounded before the operation refuses it. No state literal, no wire field and no stored value changed.

**Verification, and what it does not cover.** The slice type-checks in a scoped project covering exactly its own import closure, and type-aware lint, formatting and the contracts type check pass. The workspace build and the full `apps/web` type check could not be run to completion: two files a concurrent agent was editing at the time fail independently of this change, one of them importing a module `apps/web` does not depend on. Neither a passing build nor a failing one would have been evidence about this slice, which is why the scoped project was used and is reported as what it is. No browser journey was exercised, no batch was sealed, approved or executed, no financial effect was produced, and no test or fixture was added.

**Still open in this packet.** Supplier extraction is still addressed only by an identifier held in component state, so a reload loses which occurrence was open. Period-work cancellation is still absent from the MCP catalogue, so an agent cannot halt a run whose children it cannot otherwise stop. And the whole priority source-to-review-to-receipt journey remains unexercised in a browser, which is the packet's actual proof obligation and needs an approved web test harness.
