# Accounting completion: active implementation wave

Status: in progress. This record keeps source delivery, observed checks and external readiness separate. The maintained domain plans remain the requirement owners.

## Requested scope and current boundary

| Capability | Current implementation boundary | Remaining work |
| --- | --- | --- |
| Bank reconciliation | Exact matches, approved partial/many-to-many allocations and reviewed unmatch in source; retained CSV preview/admission | Runtime acceptance, complete source coverage and broader recovery proof |
| Invoice registers | Evidence-backed registration, approved payment allocation and frozen ageing/GL controls | Historical open items, credits/refunds/corrections, completeness and domain proof |
| Invoice issuance/delivery | Immutable commercial drafts and bounded synthetic issue with atomic recognition, internal numbering and customer registration in source; no legal issuance or delivery | Runtime acceptance, reviewed legal/tax profiles, legal numbering, credits/corrections and durable delivery |
| Asset schedules | Synthetic schedules, evidence-backed carrying bases and immutable declared-account GL controls in source | Runtime acceptance, complete inventory/reconciliation, basis-aware posting authority, amendments/impairment/disposal and reviewed rules |
| MCP | Shared schema-backed tool catalog, scoped handlers, no approval tools | Complete operation-specific parity/recovery proof; catalog-key coverage now enforced by types |
| Internal reports | Trial-balance snapshots and retained accountant-review JSON/CSV packs | Reviewed opening basis, further report families and independent domain proof |
| Technical closing | Evidenced family declarations, domain dependency blockers and retained close/reopen certificates | Complete applicable family controls, broader failure/concurrency proof and separate financial-close semantics |
| VAT returns | Evidence-backed tax facts and synthetic draft box snapshots; actual-company amounts excluded | Reviewed real tax profile and ledger controls, tax-account reconciliation, amendments and filing artifacts |
| Bank feeds | No connected feed; file intake is not a feed | Provider contract/consent, cursors/revisions, durable synchronization and reconciliation |
| SIE | Synthetic SIE4I capture, CP437 encoding, immutable artifacts and download in source | Runtime/semantic/destination acceptance; separate full-book 4E and loss-preserving import profiles |
| Payroll/AGI | Not implemented | Private scoped inputs, reviewed calculation profiles, approval/posting, settlement and declarations |
| Statutory reports | Not implemented; review packs are not statutory output | Financial close/openings, tax bridge, K2/K3 facts, mappings/schema validation and actual required outcomes |
| Peppol/payment files | Not implemented | Exact format profiles, immutable artifacts, validation, authority and provider-specific delivery/recovery |

Missing company/provider facts do not prevent independent synthetic implementation. They do prevent real-company, compliance or external-acceptance claims. No capability is marked complete because an adjacent table, endpoint or outbox exists.

## Active ownership and acceptance

- **COM-06 subset:** immutable same-currency invoice ageing and register-to-GL controls. Root reserves forward migration `0920-commerce-register-snapshots.sql`. The saved basis must bind exact invoice revisions, dated payment allocations and complete selected GL totals. Oversize input is refused rather than truncated. Differences remain visible; source coverage remains unestablished. The consumer includes saved report inspection and JSON download.
- **END-01 subset:** explicit evidenced declarations for each accounting family and a new complete-inventory technical scope. Root reserves forward migration `0930-closing-family-inventory.sql`. Missing declarations and required unavailable/failed checks block new close preparation. No declaration can waive observed domain failures. Historical bank-only plans/certificates retain their interpretation. Technical close never becomes financial/statutory readiness.
- **VAT:** bounded evidence-backed fact revisions and non-filing draft calculation are implemented and connected to API/MCP/workspace in source (`1000-vat-return-drafts.sql`). Actual-company contributions remain excluded; synthetic calculations do not activate a legal profile. Forward `1001-closing-vat-dependencies.sql` now binds this inventory into closing and review-pack currentness in source; represented facts or saved drafts contradict tax non-applicability. No runtime acceptance is claimed.
- **SIE:** the [4C source review](../sources/sie-4c-review.md) distinguishes 4I transaction transfer from 4E bookkeeping export. Immutable SIE4I capture/render/seal and binary-download source is connected under migration1100. Source-review fixes now use voucher-scoped line identities and scope-bound, fixed-cutoff inventory cursors. No runtime or format acceptance is claimed. No full-book export or external acceptance is claimed.
- **Invoice drafts:** native commercial drafts/revisions are implemented in source under migration1200; runtime acceptance remains open. Saving a draft does not issue an invoice number, recognize revenue or deliver an invoice.
- **Root:** shared exports, handlers, capability bindings and dispatcher; integration and source review. Validation remains paused under the latest instruction. Domain-local modules have separate owners. Existing migrations are immutable.

## Parallel domain implementation after the gap review

The user authorized implementation across selected domains without focusing on browser verification or tests. This wave uses source review only; no validation commands or database migrations are run.

| Domain | Implemented and source-integrated slice | Unapplied forward migration |
| --- | --- | --- |
| Bank matching | Reviewed whole-allocation or retained exact-match unmatch; immutable originals and effective released capacity | `1300-bank-match-reversals.sql` |
| Invoice issuance | Sealed review, same-operator approval/execution and atomic synthetic numbering, kernel recognition and customer registration | `1400-invoice-issuance.sql` |
| Asset schedules | Evidence-backed acquisition/imported carrying basis and immutable declared-account GL controls | `1500-subledger-controls.sql` |
| Closing/review dependency | Whole asset-control dependency, mandatory coverage blockers, historical decoding and accountant-review-v3 exports | `1510-closing-subledger-dependencies.sql` |

All slices have shared contracts exports, API/handler composition, database dispatch and permitted MCP bindings. Human approval and basis-review commands are not ordinary agent approval tools. The routed interface exposes matching/unmatch under Accounts, synthetic issuance and live issue-aware draft inspection under Sales, and asset controls under Reports. Legacy workspace composition is also connected. Existing unrelated UI changes are preserved.

Source review found and corrected an invoice aggregate escape through a different event key on the same retained evidence. Ownership now binds both the event and evidence references; pre-existing posting on the retained draft source refuses issuance. Approval usability is caller-specific. Issued drafts are frozen; retained draft flags are historical, while a fresh issue-history overlay controls the editor. These are source observations, not runtime proof.

Asset controls link existing posted lines; they do not create acquisitions or authorize future schedule posting. Original cost, accumulated recognition and carrying value are conserved separately. Every declared-account GL contribution and unexplained row remains visible, including offsetting differences. Missing/reversed bases and due occurrence gaps remain explicit. Whole-source coverage and financial-close readiness remain false. Forward1510 preserves the latest VAT dependencies and active-bank hooks while making new bases or report inventories stale older closing/review scopes. Historical bytes are not rewritten.

Implementation notes: [bank unmatch](../../apps/api/BANK-MATCH-REVERSALS.md), [synthetic invoice issue](../../apps/api/INVOICE-ISSUANCE.md), and [subledger controls](../../apps/api/SUBLEDGER-CONTROLS.md). The source handoff is retained in `.agents/work/domain-implementation-2026-09-23/`. No tests, lint/type/build commands, browser sessions, database execution or migration application were performed for this wave. All new behavior remains runtime-unverified; legal profiles, external delivery and complete accounting readiness remain open.

## Continuous implementation follow-up

The user asked to keep implementing without focusing on tests, browser or mobile work. The next source-only packet is assigned to the retained domain owners:

-1600: read-only bank match candidates are source-integrated using effective capacities, explicit heuristic reasons and unresolved ambiguity. No automatic match or posting.
-1700: reviewed whole-allocation payment unallocation is source-integrated with immutable originals, once-only capacity release and forward updates to effective commerce consumers. Accounts → Payment allocation exposes the workflow; historical receipts and reports now show separate live status. Independent source review found no concrete blocker; runtime proof remains open.
-1800: linked carrying-basis validity is implemented and source-integrated at preparation, shared validation and physical posting, including already-prepared/generic paths and known correction ancestry. Standalone synthetic schedule semantics remain. Runtime proof is open.
-1900: evidence-backed manual exchange rates and exact immutable conversion review are source-integrated under Reports → Exchange rates. Rates are directional, evidence-backed operator decisions; conversion reviews retain exact quotient/remainder, named synthetic rounding and signed residuals. No cross-currency posting, revaluation or legal-rate activation is included. Uncertain forms now retain their captured revision and retry keys across rate refreshes. Failed or pending currentness refreshes show unknown status while keeping verified historical artifacts available.

1900 integration and request-recovery fixes are present.2000 bank statement interval coverage is source-integrated under Accounts → Statement coverage, reusing the existing reviewed closing inventory and exposing gaps, overlaps and independent balance continuity without satisfying closing gates.2100 immutable synthetic invoice documents are source-integrated beside issued reviews: fixed escaped HTML, resumable capture/render/seal and integrity-checked historical downloads, never legal issuance or delivery. Independent source reviews found no concrete blocker in1900 arithmetic,2000 interval controls or2100 document safety; they are not runtime/security proof.1600–2100 remain runtime-unverified.

Candidate-to-allocation identifier handoff is source-integrated in routed and legacy matching workspaces. Only explicit discard/start adopts the seed; no amount, rationale, acknowledgment or approval is inferred.2300 evidence-backed permanent withdrawal of erroneous manual rate observations is source-integrated through the existing exchange-rate group. Retained revisions and artifacts remain readable; successful old-key replay remains available while new revisions/conversions refuse. Independent source review found no concrete blocker; execution remains unverified.2200 native synthetic invoice cancellation is source-integrated beside issued reviews. Its exact reversal and immutable cancellation aggregate require the same approving current operator, open periods, and no active payment/bank/owner/schedule or carrying-basis conflicts. New register snapshots retain and explain original recognition and economically dated cancellation contributions; historical issue/document/report bytes remain unchanged. Independent source review found no remaining concrete blocker after the basis-ownership refusal. Stable approval-bound form instances retain uncertain requests when later approvals arrive. The package/API/query/capability registrations omitted in the initial partial handoff are now connected. Type, SQL and runtime verification remain outstanding. Root owns shared integration and preserves concurrent UI work. No historical migration, test or external system is changed by this authority.

## Observed baseline

The baseline `bun run check-types` passed, including the web build and existing test-source compilation. The existing `bun run test:e2e` run passed **17 of 20** cases:

- Existing MCP negotiation/catalog/no-approval/same-ledger behavior passed.
- Exact amounts, concurrent retry/receipt recovery, linked reversal, restricted writes, late-fault rollback and migration replay/drift checks passed.
- The approval-expiry case stopped when its fixture attempted to mutate an immutable approval.
- The cookie-login case targets a removed token-login endpoint rather than Better Auth.
- Browser execution stopped because the installed Playwright Chromium executable was absent.

Local receipts were preserved under `.agents/work/accounting-completion-baseline/`. They pin the actual revision and working-tree digest; they do not verify later domain edits. No test files or fixtures were changed. Updating the stale tests and adding domain scenarios still needs explicit user approval (D-09).

After the root MCP change, API types passed and native imports showed identical declared/bound catalog keys. A focused MCP rerun then failed during Worker startup because an in-progress closing schema called an API absent from the installed Effect version. That run executed no scenario and is not a pass. The issue was sent to the domain owner; integrated runtime verification remains open.

## Release gates

No deployment, production migration, real-company posting, external filing, payment, provider connection, commit or push is authorized by this work. D-04 supplies reviewed company/profile facts; D-08 supplies rule/format applicability and independent vectors; D-10 supplies provider contracts and explicit external-action authority. The original multi-capability goal remains incomplete.

## Latest implementation-only instruction

The user stopped tests and test writing. No further validation commands are running or planned; work continues through implementation and source review. Before this instruction, the frozen0920/0930 checkpoint passed types/build and17/20 existing E2E cases, including MCP; the same three baseline failures remain. This is not acceptance of new report/closing scenarios. Receipts and the exact source/migration manifest are in `.agents/work/accounting-completion-wave-01/`. Unknown concurrent0940 was excluded. A frozen lint attempt selected zero files and is not a pass; formatting did not run. Later VAT/SIE/invoice work remains unvalidated.

## Existing-workflow recovery: source-only follow-up

Forward migrations `2600-preparation-job-recovery.sql` and `2700-source-upload-replay.sql` repair existing workflows; they add no financial execution or posting authority. Historical0940/0910 remain unchanged.

- A new authorized preparation-job admission can atomically stop an obsolete ready job and admit its replacement under the book lock. A changed configured executor, lost original authority or changed run audit can establish obsolescence. An unchanged active job still refuses replacement. Cancelled/blocked runs still require explicit resume. Exact old-key replay returns its original receipt; changing executor identity requires a new explicit command. The UI offers a replacement request, retains uncertain requests for exact-key retry, and reads live job status separately from admission receipts.
- Completed object-backed source uploads return the exact saved occurrence from authorized, input-matched admission before acquiring, writing or reading object storage. New/pending uploads still require canonical input, digest/length verification and separately authorized completion. Receipt replay does not establish current object availability. Public contracts and inline-source behavior are unchanged.

Both migrations are source-reviewed only, unapplied and runtime-unverified. No test, type, lint, browser or SQL execution was performed for this follow-up. Concurrent workspace/firm migrations are outside this repair's ownership.

### Stored submitter identity admission

Forward `2800-preparation-identity-admission.sql` carries the identity-disable rule into durable preparation jobs. Provisioning revokes browser sessions, but can leave an API credential and book membership intact; those alone no longer authorize another queued step for a disabled submitter. Delivery checks the original identity admission between credential/session and membership/book locks. An existing admission row remains locked through the step; an absent row keeps the authentication layer's legacy behavior. Authorized replacement admission can also recognize the disabled original submitter without reversing lock order.

No new posting, identity-management or run-resume authority is introduced. Existing checkpoints, terminal replay and saved receipts remain intact. Migration2800 is source-only, unapplied and runtime-unverified; concurrent identity provisioning and historical migrations were not changed.

## Supplier-invoice duplicate diagnostics

The [COM-01 diagnostic lookup](04-invoices-payments-registers.md#supplier-invoice-duplicate-diagnostics)
is implemented through shared contracts, REST/MCP dispatch and forward
`3000-supplier-invoice-duplicates.sql`. It pages same-supplier registrations matching
an exact document number or original evidence content, with explicit reasons and
live invoice details. It does not merge records, post, relax registration guards
or claim source completeness. Other suppliers and customer invoices are excluded.

API/contracts type checks and targeted type-aware lint/format checks passed for
this follow-up. No tests were added or run. The migration remains unapplied;
SQL/runtime acceptance and broader COM-01 work remain open. Concurrent sales and
frontend work was preserved.

## Parallel backend continuation

The user authorized continued parallel backend implementation without test work.
Domain ownership is split between source intake, asset schedules and VAT, with
shared API/MCP wiring and reporting owned by the root integrator. Forward migration
prefixes3100,3200,3300 and3400 separate these changes from the concurrent sales work.

Forward `3400-report-general-ledger.sql` adds the [snapshot-bound general ledger
account view](06-year-end-reports-filing.md#snapshot-bound-general-ledger-account-view)
through REST and MCP. It uses frozen account labels/opening totals, exact signed
running balances, retained voucher/correction/evidence links and report/account-bound
continuation. It does not change historical snapshots or infer fiscal openings.
Source implementation is present; SQL/runtime acceptance remains open.

VAT amendment read/compare dispatch is connected while its domain implementation
is in progress. Asset and source-intake implementation/integration remain in progress.
No tests, migration application, deployment or provider action is authorized by this
continuation. Narrow static checks are allowed; financial behavior remains unverified.
