# Accounting completion: active implementation wave

Status: in progress. This record keeps source delivery, observed checks and external readiness separate. The maintained domain plans remain the requirement owners.

## Requested scope and current boundary

| Capability | Current implementation boundary | Remaining work |
| --- | --- | --- |
| Bank reconciliation | Exact matches and approved partial/many-to-many allocations; retained CSV preview/admission | Reversal/unmatch, complete source coverage and broader recovery proof |
| Invoice registers | Evidence-backed registration against posted recognition; approved payment allocation | Frozen ageing/GL controls (active COM-06 slice), credits/refunds/corrections and completeness |
| Invoice issuance/delivery | Not implemented | Commercial revisions, exact item/tax rules, numbering, issue/recognize/deliver separation and durable delivery |
| Asset schedules | Synthetic exact schedules and kernel occurrence links | Asset acquisition/import basis, ledger reconciliation, amendments/impairment/disposal and reviewed rules |
| MCP | Shared schema-backed tool catalog, scoped handlers, no approval tools | Complete operation-specific parity/recovery proof; catalog-key coverage now enforced by types |
| Internal reports | Trial-balance snapshots and retained accountant-review JSON/CSV packs | Reviewed opening basis, further report families and independent domain proof |
| Technical closing | Bank inventory, domain dependency blockers and retained close/reopen certificates | Explicit family applicability (active END-01 slice), broader failure/concurrency proof |
| VAT returns | Expense source/reviewer facts and excluded/synthetic contributions only | Reviewed dated tax facts, return/box snapshots, tax-account controls, amendments and filing artifacts |
| Bank feeds | No connected feed; file intake is not a feed | Provider contract/consent, cursors/revisions, durable synchronization and reconciliation |
| SIE | Official 4C source review; no encoder/importer | Format-specific immutable artifacts, complete selected profile and independent semantic acceptance |
| Payroll/AGI | Not implemented | Private scoped inputs, reviewed calculation profiles, approval/posting, settlement and declarations |
| Statutory reports | Not implemented; review packs are not statutory output | Financial close/openings, tax bridge, K2/K3 facts, mappings/schema validation and actual required outcomes |
| Peppol/payment files | Not implemented | Exact format profiles, immutable artifacts, validation, authority and provider-specific delivery/recovery |

Missing company/provider facts do not prevent independent synthetic implementation. They do prevent real-company, compliance or external-acceptance claims. No capability is marked complete because an adjacent table, endpoint or outbox exists.

## Active ownership and acceptance

- **COM-06 subset:** immutable same-currency invoice ageing and register-to-GL controls. Root reserves forward migration `0920-commerce-register-snapshots.sql`. The saved basis must bind exact invoice revisions, dated payment allocations and complete selected GL totals. Oversize input is refused rather than truncated. Differences remain visible; source coverage remains unestablished. The consumer includes saved report inspection and JSON download.
- **END-01 subset:** explicit evidenced declarations for each accounting family and a new complete-inventory technical scope. Root reserves forward migration `0930-closing-family-inventory.sql`. Missing declarations and required unavailable/failed checks block new close preparation. No declaration can waive observed domain failures. Historical bank-only plans/certificates retain their interpretation. Technical close never becomes financial/statutory readiness.
- **VAT:** bounded evidence-backed fact revisions and non-filing draft calculation are implemented and connected to API/MCP/workspace in source (`1000-vat-return-drafts.sql`). Actual-company contributions remain excluded; synthetic calculations do not activate a legal profile. Forward `1001-closing-vat-dependencies.sql` now binds this inventory into closing and review-pack currentness in source; represented facts or saved drafts contradict tax non-applicability. No runtime acceptance is claimed.
- **SIE:** the [4C source review](../sources/sie-4c-review.md) distinguishes 4I transaction transfer from 4E bookkeeping export. Immutable SIE4I capture/render/seal and binary-download source is connected under migration1100. Source-review fixes now use voucher-scoped line identities and scope-bound, fixed-cutoff inventory cursors. No runtime or format acceptance is claimed. No full-book export or external acceptance is claimed.
- **Invoice drafts:** native commercial drafts/revisions are in progress under reserved migration1200. Saving a draft does not issue an invoice number, recognize revenue or deliver an invoice.
- **Root:** shared exports, handlers, capability bindings and dispatcher; integration review and serialized native validation. Domain-local modules have separate owners. Existing migrations are immutable.

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
