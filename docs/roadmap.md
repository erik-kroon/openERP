# Delivery plan

Status: the documentation-first checkpoint is committed in `52bd1117`. All seven requested areas now have a [complete working delivery plan](plans/README.md). Implementation has advanced, but no complete phase exit is established by this planning review.

## Document reading integration

The [Document Intelligence first journey](plans/document-intelligence-delivery.md) has ten passing synthetic E2E scenarios, including the normal self-host API and preparation runner, and a browser suggestion-to-draft proof. This is local integration evidence; live provider qualification and company acceptance remain open.

## Current checkout

[DF-03 P&L transfer bridge](plans/evidence/df-03-profit-transfer-bridge.md) fixes
the served report-family catalogue and excludes frozen owned result transfers
from ordinary mapped amounts while preserving raw ledger drill-down. Real
close/report/MCP/browser evidence passes with seventeen focused E2E cases.

[PRY-17 clearing/account hints](plans/evidence/pry-17-bank-account-hints.md) now
uses an explicit retained reference profile through the supplier workspace and
shared REST/MCP. Valid, invalid and no-opinion outcomes are observed; checksum
hints remain non-blocking and verify no account or payment authority. Five
focused E2E tests pass, including the earlier giro/OCR and MCP-authority journeys.

[PRY-16 payment identifiers](plans/evidence/pry-16-payment-identifiers.md) is wired
through the supplier-payment workspace and shared REST/MCP. Giro/OCR checks and
explicit OCR candidates preserve source identifiers without verifying payees or
authorizing payments. Twenty-two focused E2E cases pass, including both DF-05 SIE
suites; this does not establish company or provider readiness.

[DF-05 SIE account-code consistency](plans/evidence/df-05-sie-account-codes.md)
has real movement-export-to-retained-staging proof for one-, five- and eight-digit
codes and preserved zero prefixes. Fourteen focused E2E cases pass; financial
admission, actual-company history and external receiving software remain separate.

[NEXT-97 exact grouped bank matching](plans/evidence/next-97-exact-covers.md) has
local synthetic HTTP and Chromium proof: bounded discovery preserves ambiguity
and shared-capacity conflicts, and a selected group follows the existing
prepare/approve/execute flow. This is a matching slice, not a P2 actual-period exit.

[DF-04 saved-request retry](plans/evidence/df-04-saved-request-retry.md) preserves
the original identity after referenced-state refusals, with immutable attempt
history and shared REST/MCP/browser behavior. The integrated local synthetic
suite passed 182 tests across 46 files, including NEXT-97. This is revision-scoped
engineering evidence, not actual-company readiness.

The synthetic accounting workflow began at `e5fe3e69`. The planning capture at `1965622afa65285fa8e9013ccdd98a47ebe86dfb` includes further accounting workflows and recovery tooling. The [dated source manifest](plans/evidence/planning-baseline.json) records that revision, working-tree status and inspected-file hashes. Active correction, matching, commerce, subledger, closing and recovery work continues in the shared tree. Reconcile the live diff and its evidence before each packet; source presence does not change a whole milestone to verified.

An isolated local Worker/PostgreSQL observation exercised evidence retention, proposal, validation, operator approval, posting and receipt lookup. One journal produced the independently expected debit and credit; repeated execution returned the same receipt. [The runtime checkpoint](evidence/initial-runtime-checkpoint.md) records the environment, actual results, migration failures and remaining gaps. This is partial evidence for E-01, E-03, E-04 and E-20, not completion of those scenarios. No browser, provider, restore or actual-company proof was performed in that observation.

The [design coverage map](design-coverage.md) links requirements and detailed edge cases to their owning specifications and acceptance gates. The [verification strategy](verification-strategy.md) defines repeatable runtime evidence. [BANK-1 local synthetic evidence](plans/evidence/bank1-local.md) records multi-entry matching, whole-match reversal, saved-report scope and account/period behavior; it does not close the P2 actual-period gate.

## Book Zero direction received 2026-09-27

The [Book Zero delivery plan](plans/15-book-zero-workflow-cash.md) integrates the openERP-specific PRD from the supplied Drastic archive. The first priority is a reviewed Drastic period plus a complete daily workflow; read-only Cash consumes the same qualified sources and obligations. The original source is retained byte-identical under [vendored specifications](specs/README.md#book-zero-prd). The broader platform PRD is not included in this scope.

L0–L2 organize profile/current-owner reconciliation, the first period and usable daily work across P0–P5 and frontend owners. L3/L4 add the Cash basis and daily forecast. L5 expands to full-year handoff and a new real period; L6 retains P7's independent transition decision; L7 is a bounded external pilot. G0–G7 distinguish scope, historical-period proof, daily-work proof, Cash, year handoff, new-period proof, cutover and pilot readiness. [The delivery/gate map](plans/15-book-zero-workflow-cash.md#delivery-and-independent-gates) states their dependencies without changing the existing packet index.

Only documentation provenance, requirements/acceptance references, links and illustrative arithmetic are checked in this update; see the [document verification record](plans/evidence/book-zero-docs-verification.md). No new implementation, real-period assessment, application E2E, company qualification, external outcome or completed L/G/P gate is claimed. The PRD's company facts need original evidence, and its older inspection revision is not a current absence audit.

## Phases and exit gates

P0/P1 and parts of later phases have initial implementation or active drafts; complete exit gates remain open. The [dependency-ordered backlog](plans/08-delivery.md) turns the seven areas into scoped packets with named acceptance criteria. A later row's position never permits omission of an obligation that applies to the company. Scope large commits around capabilities whose required consumers work together.

| Phase                             | Coherent deliverable                                                                                                                                                     | Entry dependencies                                                                            | Observable exit                                                                                                                                                                                          |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P0 — runtime foundation           | Exact wire types and scoped PostgreSQL transaction adapter; migration and restricted-role path.                                                                          | D-02, D-03 and D-09 for new tests.                                                            | Existing app passes checks; real workerd and Bun commit/rollback/cleanup verified; migration rerun safe.                                                                                                 |
| P1 — posting lifecycle            | Evidence-backed single-group proposal, inspect/validate, trusted approval, atomic posting, receipt lookup, ledger query and correction; UI/REST/thin MCP share handlers. | P0, D-01, D-05.                                                                               | E-01–E-11 and E-20 relevant cases pass through real boundaries; no stale approval, duplicate effect, editable posted amount or cross-book write.                                                         |
| P2 — first reconciled period      | Import existing matches/history, establish profile, preserve source identities, reconcile items and balances, and drill through a period report.                         | P1, D-04, D-06 and relevant D-08 rules.                                                       | Supplied material accounted for; independent control totals, source coverage and preserved links; unresolved differences prevent completion. Synthetic proof cannot substitute for the actual-data gate. |
| P3 — recurring work               | Cases, bounded batch review, deterministic rules, scoped standing mandates where approved, durable multi-group runs and delivery.                                        | P1/P2 contract and actual supported patterns.                                                 | Changed relevant facts block affected groups; unchanged groups resume; duplicate delivery produces one result; measure efficiency on identical cases.                                                    |
| P4 — VAT and tax account          | Dated tax semantics, return snapshots, statement reconciliation and comparison/correction of prior filings.                                                              | P2 and reviewed applicable rules.                                                             | Independently expected box totals, ledger lineage and prior filed artifacts preserved; preparation never implies submission.                                                                             |
| P5 — company-required depth       | FX, settlements, owner flows, assets/schedules and payroll/AGI/KU as applicable.                                                                                         | P1/P2 plus each module's facts/rules; may overlap P4.                                         | Each required transaction family conserves amounts and reconciles to controls with reviewed expected outcomes.                                                                                           |
| P6 — year and statutory artifacts | Close/opening impact, tax bridge, INK2, annual report, required SIE and iXBRL.                                                                                           | Required P4/P5 capabilities and D-08.                                                         | Complete year reconciles; no fabricated disclosure facts; reproducible semantic output and pinned independent validation.                                                                                |
| P7 — operations and cutover       | Required provider signing/submission, portable self-host packaging, archive/restore, rehearsed single-writer migration.                                                  | D-07, D-10, all company-required earlier capabilities and separate external-action authority. | Actual scope-appropriate receipts, unknown-outcome recovery, full restore and reconciled authorized cutover.                                                                                             |
| P8 — expansion                    | Hosted operational scaling and additional jurisdictions when demanded.                                                                                                   | Verified first-company product.                                                               | Isolation and fair resource use remain intact; each new profile has its own coverage evidence.                                                                                                           |

[FND-01](plans/fnd01-reconciliation.md) is complete as a source/contract reconciliation at `90db69b4`. Its [inventory](plans/evidence/fnd01-inventory.json) maps the pre-replacement REST/MCP/database registrations and applied migration definitions. The [verification record](plans/evidence/fnd01-verification.json) reports passing types/lint/format and 19 of 20 existing E2E checks; browser sign-in was refused and cleanup masked the original failure. This is not a completed P0/P1 exit, and the evidence does not cover later concurrent adapter/UI changes or the application-owned replacement.

[ADR 0010](adr/0010-application-owned-accounting-replacement.md) is implemented. Application-owned operations, the clean three-file baseline and the effect-mq Bun worker replace SQL feature dispatch and Cloudflare preparation. The [completion record](plans/evidence/application-owned-replacement-complete.md) records the final domain, boundary, browser/runtime, queue and restore observations. This closes the replacement work without promoting unrelated company or hosted-provider gates.

Continue from FND-02/FND-03/FND-04 in the [shared plan](plans/00-shared-contracts.md). Reconcile current implementation and evidence before changing financial code:

1. Use the [application-owned replacement inventory](plans/application-owned-accounting.md#domain-slices-and-complete-caller-coverage) to compare the live adapter/UI changes with every planned caller. Preserve supported routes, public contract IDs and financial requirements; classify the old SQL chain, Workflow/Cron path and direct statement dispatch for deletion.
2. Resolve the observed browser admission failure without weakening origin protection, and make harness cleanup reliable within actual test authority. Complete restricted-role, clean-baseline, fault/recovery and runtime-lifetime gaps against fixed revisions; do not treat a prior successful happy path as complete proof.
3. Establish the transaction and identity foundation, then complete PST-01–PST-05 and COR-01/COR-02 in dependency order. Durable rediscovery, aggregate correction atomicity, all-channel semantics and the effect-mq restart/duplicate cases are part of the core exit.
4. Record the exact revision/environment/results and limitations for each accepted packet, then follow the domain dependency graph. Implementation presence, synthetic proof, actual-company reconciliation and external acknowledgment receive separate status.

The first UI must display evidence, exact lines, approval scope and receipt state. A local fixed identity is not proof of human authorization; any development-only identity mode must be explicitly bounded and cannot satisfy the authenticated-approval gate.

## Current accounting completion wave

The [active implementation record](plans/accounting-completion-wave.md) covers the requested bank, commerce, schedules, MCP, reporting, tax, payroll and interchange gaps. The continuous wave now includes reviewed bank unmatch and candidate handoff, bounded synthetic invoice issue with immutable document artifacts, payment unallocation, asset carrying bases and posting guards, manual exchange-rate review and withdrawal, and diagnostic bank interval coverage. Closing and accountant-review dependencies include the complete asset-control inventory. Shared API/MCP and routed UI integration is present in source for1300–2300; these migrations remain unapplied.2200 native synthetic invoice cancellation retains original history, records an exact recognition reversal and updates live register consequences. Independent source review is not executed financial proof. No tests, browser sessions or validation commands ran for this wave. Earlier baseline checks do not verify these changes. This is not a phase exit, legal issuance, complete financial control or company-readiness claim.

The synthetic VAT control-reclassification slice is now source-integrated through forward `9120`/`9130`, shared contracts, HTTP/MCP reads and the Tax workspace. It remains unapplied and runtime-unverified: exact positive/negative/zero, stale, duplicate and same-key recovery outcomes still require PostgreSQL/Workerd/browser evidence. Assessment, payment, filing and VAT-04 amendment deltas remain separate.

## Implementation dossiers received 2026-09-26

Two externally produced dossiers specifying implementation-level design for fifty work items were vendored under [`docs/specs`](specs/README.md) and indexed by the [NEXT dossier plan](plans/12-next-implementation-dossier.md). They cover NEXT-01…25 as an application-owned Effect rewrite and NEXT-26…50 as a second wave, and they are aligned with ADR 0009 and ADR 0010.

What was actually observed: the vendored copies match their recorded checksums (37 of 37 and 41 of 41 files) and each archive's own structural and arithmetic checker passes when re-run — 7,465 assertions and 90 of 90 named design checks. All four pinned review revisions are ancestors of this checkout, so both dossiers' statements of absence describe revisions the repository has moved past; the second wave separately records that NEXT-01 was reported implemented with static checks only and no runtime proof. [The import record](plans/evidence/next-dossier-verification.md) states the commands and the limits. No application, database, worker, queue, browser or provider workflow was run, and no packet is implemented by this entry.

They are not new scope. Each packet names the existing owner and its delta, most requirements are already owned by the [delivery plan](plans/README.md), the [capability backlog](plans/capability-backlog.md) or the [parity backlog](plans/11-parity-backlog.md), and the packets stay outside the 53-packet index and its completion denominator. Six requirements the index does not yet own — loan lifecycle, late FX chain repair, economic impairment reversal, foreign-currency cash holdings, a direct cash-flow statement and paid-payroll recovery — are named there with the decision each requires. Implementation must still resolve each packet's `APP-SLICE-READY` prerequisite and the reserved VAT, FX, asset, amendment and webshop-intake owners against the actual tree.

## Third implementation dossier received 2026-09-28

A third externally produced dossier, specifying implementation-level design for twenty-five further work items, was vendored under [`docs/specs/next-51-75`](specs/next-51-75/README.md) and indexed by the same [NEXT dossier plan](plans/12-next-implementation-dossier.md) under [ADR 0012](adr/0012-next-implementation-dossier.md) as amended. It covers NEXT-51…75 — mixed-rate and cross-border sales, advances, deferred revenue, installment terms, receivable loss, collection charges, a customer portal, purchase commitments and budgets, chart adoption, bank files, and VAT/AGI/INK2 submission — and it states that it supplements rather than renumbers the earlier fifty. Seventy-five supplemental packets now exist; all seventy-five remain outside the 53-packet index and its completion denominator.

What was actually observed: the vendored copy matches its recorded checksums (40 of 40 covered files) and the archive's own checker passes when re-run at 80 of 80 named design checks. Its pinned review revision `116a5ca6` is an ancestor of this checkout. [The import record](plans/evidence/next-51-75-dossier-verification.md) states the commands and the limits. No application, database, worker, queue, browser or provider workflow was run, and no third-wave packet is implemented by this entry.

Its absence claims are the weakest of the three waves, by its own statement: it defines "new" as absent from the **prior NEXT scope** and says it is not an exhaustive current-source absence audit. Read its packet designs as design input and reconcile each against the checkout before treating anything as new work. A dated search of the maintained plans found no owner for five lifecycles it names — the EU sales statement, the receivable allowance/confirmed-loss/recovery lifecycle, purchase commitments, budget control and accounting-method change — and the plan records each with the decision it needs rather than adopting it.

## Fourth implementation dossier received 2026-09-28

A fourth externally produced dossier, covering twenty-five further work items, was vendored under [`docs/specs/next-76-100`](specs/next-76-100/README.md) and indexed by the same [NEXT dossier plan](plans/12-next-implementation-dossier.md). It covers NEXT-76…100 — project and contract billing, supplier disputes, asset construction and component replacement, operating leases, book-to-tax depreciation, tax allocation reserves, ROT/RUT claims, pension and termination, dividends, grants, supplier-credit application, bilateral setoff, evidence search, mailbox intake, counterparty confirmations, multi-reviewer approval, covering-set matching, accountant review engagements, forecast scoring and outbound event subscriptions. One hundred supplemental packets now exist; all one hundred remain outside the 53-packet index and its completion denominator.

What was actually observed: the vendored copy matches its recorded checksums (40 of 40 covered files) and the archive's own checker passes when re-run at 264 of 264 named design checks — 131 structure, 69 document, 64 arithmetic, matching the archive's own breakdown. [The import record](plans/evidence/next-76-100-dossier-verification.md) states the commands and the limits. No application, database, worker, queue, browser or provider workflow was run, and no fourth-wave packet is implemented by this entry.

This wave is pinned to this repository's head, so nothing in it is stale — and it states that its repository reading was targeted rather than a source audit, with no runtime qualification claimed. Best-pinned and least-audited at once. Its conditional profiles — grants, dividends, termination, pension, ROT/RUT, tax allocations, operating leases — are explicitly not launch prerequisites, and a dated search of the maintained plans found no owner for twelve further lifecycles it names, from earned-but-unbilled revenue to multi-reviewer quorum routing. Those are recorded in the plan with the decision each needs.

One verification caveat is worth knowing before re-running anything: every vendored dossier checker writes its own `results.json`, and this wave's is not byte-reproducible — its document checks are emitted in filesystem order, so running the checker inside the tree breaks the manifest until the archived bytes are restored. The import record documents the restore that was performed.

## Fifth implementation dossier received 2026-09-28

A fifth externally produced dossier, covering twenty-five further work items, was vendored under [`docs/specs/next-101-125`](specs/next-101-125/README.md) and indexed by the same [NEXT dossier plan](plans/12-next-implementation-dossier.md). It covers NEXT-101…125 — firm delegation and multi-client workspaces, evidence requests, balance-sheet substantiation, shared-cost attribution, project margin, retainer entitlements, provisions, insurance, loan reschedules, specialist VAT including B2C/OSS and foreign recovery, payroll benefits, interest and preliminary-tax statements, share subscriptions, standing posting mandates, cash-constrained payment proposals, direct debit, bank-feed handover and processor refunds. One hundred twenty-five supplemental packets now exist; all one hundred twenty-five remain outside the 53-packet index and its completion denominator.

What was actually observed: the vendored copy matches its recorded checksums (40 of 40 covered files) and the archive's own checker passes when re-run at 741 of 741 named design checks — 572 structure, dependency, document and link checks and 169 arithmetic, model and published-vector checks, which reproduces the archive's own figures exactly. [The import record](plans/evidence/next-101-125-dossier-verification.md) states the commands and the limits. No application, database, worker, queue, browser or provider workflow was run, and no fifth-wave packet is implemented by this entry.

This wave maps onto existing owners better than the two before it, and one packet is design for a contract this repository has already adopted: **NEXT-121**, bounded standing posting mandates, is governed by the mandate scope, cumulative limits, atomic budget consumption and the rule that a mandate never implicitly authorizes payment, closure, signature or filing already stated in [the operations plan](operations.md), which also already places unattended posting outside the Book Zero delivery. It therefore needs an authorization decision rather than an owner. A dated search of the maintained plans found twelve further lifecycles it names with no owner at all — onerous and warranty provisions, insurance, common-cost VAT true-up, B2C/OSS, foreign VAT recovery, car benefit, interest statements, share subscriptions, direct debit, substantiation — plus three that compound gaps already recorded rather than adding new questions.

The same verification caveat recurs: this wave's checker also rewrites `results.json`, and the regenerated file differs from the archived one because a set of task IDs is rendered into a detail string in interpreter-hash-seed order. Same 741 results, same counts; the manifest fails on that file until the archived bytes are restored.

## Owner-delegated decision pass, 2026-09-28

The open register was resolved by decision rather than by waiting for a maintainer, accounting department or security team that does not exist. [ADR 0015](adr/0015-owner-delegated-decision-pass.md) records what was selected, and the [D-register](open-decisions.md) is the authority afterwards.

What changed: the first release is **owner-operated private local use**, and the engineering release gate is owner acceptance plus independently derived source, rule and runtime evidence instead of a named external accountant. `AGENTS.md` now carries a **bounded standing test permission** in place of the blanket prohibition, and the accepted test plan's HARNESS-1 expectation is rejected because it would forbid the trusted runtime role from the scoped writes its architecture requires. Both accounting methods are built as explicit profiles with K2 as the first annual-report target for actually eligible companies, and the reference comparison is pinned and non-authoritative. 23 product-scope capabilities moved from undecided to dispositioned, with `adopted conditional`, `adopted optional`, `adopted limited profile` and `deferred` kept distinct.

What did **not** change, and what remains open: the application-owned architecture, exact-money and approval contracts, and the AGPL-3.0-only position are untouched. Every company method, registration, credential, provider outcome and legal qualification is still unevidenced, and the D-register now separates chosen design from remaining affected-stage gate so that a decided design is never read as a verified fact. **Eleven capabilities the pass does not reach** — the fifth wave's provisions, insurance, VAT true-up, B2C/OSS, foreign recovery, car benefit, interest statements, share subscriptions, direct debit and substantiation — stay open and are listed as such. The five review-adoption questions are decided, but the parity and test-plan text merges are outstanding work; the decisions and the file rewrites are not the same thing and are recorded separately.

## Evidence and checkpoints

A [local SEB statement preview](plans/seb-statement-preview.md) is available at `/intake` before authentication or book selection. It reads an owner-selected file in browser memory and exposes exact movements, running-balance checks and a review export. The observed owner-supplied export agrees with its independent controls. This is source inspection only: no retained bank-statement import, document archive, journal posting or P2 company-readiness claim is established. See the packet for verification and current limitations.

Follow the repository's existing formatter, lint, type and build commands without weakening rules. Write approved E2E scenarios before their implementation; do not add unit tests afterward. Retain repeatable verification artifacts as described in [verification](verification.md).

At each exit, update this document with requirement/scenario IDs, code commit, environment, results and unresolved limitations. Keep receipts/logs/screenshots at stable linked locations when they prove a material claim. Apply the actual implementation task's authorization to commits, publication and external actions; a planning document does not grant additional authority.

## Adopted financial contracts and corrected source baseline

On 2026-09-24 the user adopted [ADR 0008](adr/0008-financial-fx-vat-impairment.md) as the working design for commerce-owned financial FX, VAT reclassification/assessment separation and atomic impairment/schedule revision. These decisions close the named design questions only. Follow the [delivery stages](plans/05-vat-payroll-assets-fx.md#adopted-financial-contract-delivery); no financial implementation or runtime proof was added by this update.

Payroll input records already exist under migration 9050 and [PAY-01 documentation](../apps/api/docs/PAYROLL-FOUNDATION.md); qualify and extend them rather than restart employee records. Conversely, actual-company VAT requires real calculation/profile implementation: migration 4500 still forbids supported actual-review totals and keeps legal/readiness flags false. Company configuration alone does not unlock that path. Earlier dated checkpoints remain historical evidence.
