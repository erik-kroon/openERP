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

-1600: read-only bank match candidates using effective capacities, explicit heuristic reasons and unresolved ambiguity. No automatic match or posting.
-1700: reviewed whole-allocation payment unallocation with immutable originals, once-only capacity release and forward updates to effective commerce consumers.
-1800: linked carrying-basis validity is implemented and source-integrated at preparation, shared validation and physical posting, including already-prepared/generic paths and known correction ancestry. Standalone synthetic schedule semantics remain. Runtime proof is open.
-1900: evidence-backed manual exchange rates and exact immutable conversion review are assigned next. No cross-currency posting, revaluation or legal-rate activation is included.

1600,1700 and1900 remain active assignments;1800 is source-integrated but unverified. Root owns shared integration and preserves concurrent UI work. No historical migration, test or external system is changed by this authority.

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
