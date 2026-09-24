# Accounting completion: active implementation wave

Status: in progress. This record keeps source delivery, observed checks and external readiness separate. The maintained domain plans remain the requirement owners.

## Requested scope and current boundary

| Capability                | Current implementation boundary                                                                                                                                        | Remaining work                                                                                                          |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Bank reconciliation       | Exact matches, approved partial/many-to-many allocations and reviewed unmatch in source; retained CSV preview/admission                                                | Runtime acceptance, complete source coverage and broader recovery proof                                                 |
| Invoice registers         | Evidence-backed registration, approved payment allocation and frozen ageing/GL controls                                                                                | Historical open items, credits/refunds/corrections, completeness and domain proof                                       |
| Invoice issuance/delivery | Immutable commercial drafts and bounded synthetic issue with atomic recognition, internal numbering and customer registration in source; no legal issuance or delivery | Runtime acceptance, reviewed legal/tax profiles, legal numbering, credits/corrections and durable delivery              |
| Asset schedules           | Synthetic schedules, linked basis guards, evidenced future-date/remaining-basis/count changes and no-proceeds disposal in source                                       | Runtime acceptance, complete inventory/reconciliation, broader lifetime/impairment/proceeds policies and reviewed rules |
| MCP                       | Shared schema-backed tool catalog, scoped handlers, no approval tools                                                                                                  | Complete operation-specific parity/recovery proof; catalog-key coverage now enforced by types                           |
| Internal reports          | Trial-balance snapshots and retained accountant-review JSON/CSV packs                                                                                                  | Reviewed opening basis, further report families and independent domain proof                                            |
| Technical closing         | Evidenced family declarations, domain dependency blockers and retained close/reopen certificates                                                                       | Complete applicable family controls, broader failure/concurrency proof and separate financial-close semantics           |
| VAT returns               | Tax facts/withdrawals, synthetic draft comparisons and exact tax-account registers/matching/controls in source; actual-company amounts excluded                        | Reviewed real tax profile, settlement roles/obligations, financial-close semantics and filing authority                 |
| Bank feeds                | No connected feed; file intake is not a feed                                                                                                                           | Provider contract/consent, cursors/revisions, durable synchronization and reconciliation                                |
| SIE                       | Synthetic SIE4I capture, CP437 encoding, immutable artifacts and download in source                                                                                    | Runtime/semantic/destination acceptance; separate full-book 4E and loss-preserving import profiles                      |
| Payroll/AGI               | Not implemented                                                                                                                                                        | Private scoped inputs, reviewed calculation profiles, approval/posting, settlement and declarations                     |
| Statutory reports         | Not implemented; review packs are not statutory output                                                                                                                 | Financial close/openings, tax bridge, K2/K3 facts, mappings/schema validation and actual required outcomes              |
| Peppol/payment files      | Not implemented                                                                                                                                                        | Exact format profiles, immutable artifacts, validation, authority and provider-specific delivery/recovery               |

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

| Domain                    | Implemented and source-integrated slice                                                                                      | Unapplied forward migration               |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| Bank matching             | Reviewed whole-allocation or retained exact-match unmatch; immutable originals and effective released capacity               | `1300-bank-match-reversals.sql`           |
| Invoice issuance          | Sealed review, same-operator approval/execution and atomic synthetic numbering, kernel recognition and customer registration | `1400-invoice-issuance.sql`               |
| Asset schedules           | Evidence-backed acquisition/imported carrying basis and immutable declared-account GL controls                               | `1500-subledger-controls.sql`             |
| Closing/review dependency | Whole asset-control dependency, mandatory coverage blockers, historical decoding and accountant-review-v3 exports            | `1510-closing-subledger-dependencies.sql` |

All slices have shared contracts exports, API/handler composition, database dispatch and permitted MCP bindings. Human approval and basis-review commands are not ordinary agent approval tools. The routed interface exposes matching/unmatch under Accounts, synthetic issuance and live issue-aware draft inspection under Sales, and asset controls under Reports. Tools workspace composition is also connected. Existing unrelated UI changes are preserved.

Source review found and corrected an invoice aggregate escape through a different event key on the same retained evidence. Ownership now binds both the event and evidence references; pre-existing posting on the retained draft source refuses issuance. Approval usability is caller-specific. Issued drafts are frozen; retained draft flags are historical, while a fresh issue-history overlay controls the editor. These are source observations, not runtime proof.

Asset controls link existing posted lines; they do not create acquisitions or authorize future schedule posting. Original cost, accumulated recognition and carrying value are conserved separately. Every declared-account GL contribution and unexplained row remains visible, including offsetting differences. Missing/reversed bases and due occurrence gaps remain explicit. Whole-source coverage and financial-close readiness remain false. Forward1510 preserves the latest VAT dependencies and active-bank hooks while making new bases or report inventories stale older closing/review scopes. Historical bytes are not rewritten.

Implementation notes: [bank unmatch](../../apps/api/docs/BANK-MATCH-REVERSALS.md), [synthetic invoice issue](../../apps/api/docs/INVOICE-ISSUANCE.md), and [subledger controls](../../apps/api/docs/SUBLEDGER-CONTROLS.md). The source handoff is retained in `.agents/work/domain-implementation-2026-09-23/`. No tests, lint/type/build commands, browser sessions, database execution or migration application were performed for this wave. All new behavior remains runtime-unverified; legal profiles, external delivery and complete accounting readiness remain open.

## Continuous implementation follow-up

The user asked to keep implementing without focusing on tests, browser or mobile work. The next source-only packet is assigned to the retained domain owners:

-1600: read-only bank match candidates are source-integrated using effective capacities, explicit heuristic reasons and unresolved ambiguity. No automatic match or posting.
-1700: reviewed whole-allocation payment unallocation is source-integrated with immutable originals, once-only capacity release and forward updates to effective commerce consumers. Accounts → Payment allocation exposes the workflow; historical receipts and reports now show separate live status. Independent source review found no concrete blocker; runtime proof remains open.
-1800: linked carrying-basis validity is implemented and source-integrated at preparation, shared validation and physical posting, including already-prepared/generic paths and known correction ancestry. Standalone synthetic schedule semantics remain. Runtime proof is open.
-1900: evidence-backed manual exchange rates and exact immutable conversion review are source-integrated under Reports → Exchange rates. Rates are directional, evidence-backed operator decisions; conversion reviews retain exact quotient/remainder, named synthetic rounding and signed residuals. No cross-currency posting, revaluation or legal-rate activation is included. Uncertain forms now retain their captured revision and retry keys across rate refreshes. Failed or pending currentness refreshes show unknown status while keeping verified historical artifacts available.

1900 integration and request-recovery fixes are present.2000 bank statement interval coverage is source-integrated under Accounts → Statement coverage, reusing the existing reviewed closing inventory and exposing gaps, overlaps and independent balance continuity without satisfying closing gates.2100 immutable synthetic invoice documents are source-integrated beside issued reviews: fixed escaped HTML, resumable capture/render/seal and integrity-checked historical downloads, never legal issuance or delivery. Independent source reviews found no concrete blocker in1900 arithmetic,2000 interval controls or2100 document safety; they are not runtime/security proof.1600–2100 remain runtime-unverified.

Candidate-to-allocation identifier handoff is source-integrated in routed and tools matching workspaces. Only explicit discard/start adopts the seed; no amount, rationale, acknowledgment or approval is inferred.2300 evidence-backed permanent withdrawal of erroneous manual rate observations is source-integrated through the existing exchange-rate group. Retained revisions and artifacts remain readable; successful old-key replay remains available while new revisions/conversions refuse. Independent source review found no concrete blocker; execution remains unverified.2200 native synthetic invoice cancellation is source-integrated beside issued reviews. Its exact reversal and immutable cancellation aggregate require the same approving current operator, open periods, and no active payment/bank/owner/schedule or carrying-basis conflicts. New register snapshots retain and explain original recognition and economically dated cancellation contributions; historical issue/document/report bytes remain unchanged. Independent source review found no remaining concrete blocker after the basis-ownership refusal. Stable approval-bound form instances retain uncertain requests when later approvals arrive. The package/API/query/capability registrations omitted in the initial partial handoff are now connected. Type, SQL and runtime verification remain outstanding. Root owns shared integration and preserves concurrent UI work. No historical migration, test or external system is changed by this authority.

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

## Earlier implementation-only checkpoint

The user stopped tests and test writing. At this checkpoint, further validation commands were paused; work continued through implementation and source review. The later parallel continuation below permits narrow static checks, but not tests or runtime exercises. Before this instruction, the frozen0920/0930 checkpoint passed types/build and17/20 existing E2E cases, including MCP; the same three baseline failures remain. This is not acceptance of new report/closing scenarios. Receipts and the exact source/migration manifest are in `.agents/work/accounting-completion-wave-01/`. Unknown concurrent0940 was excluded. A frozen lint attempt selected zero files and is not a pass; formatting did not run. Later VAT/SIE/invoice work remains unvalidated.

## Existing-workflow recovery: source-only follow-up

Forward migrations `2600-preparation-job-recovery.sql` and `2700-source-upload-replay.sql` repair existing workflows; they add no financial execution or posting authority. Historical0940/0910 remain unchanged.

- A new authorized preparation-job admission can atomically stop an obsolete ready job and admit its replacement under the book lock. A changed configured executor, lost original authority or changed run audit can establish obsolescence. An unchanged active job still refuses replacement. Cancelled/blocked runs still require explicit resume. Exact old-key replay returns its original receipt; changing executor identity requires a new explicit command. The UI offers a replacement request, retains uncertain requests for exact-key retry, and reads live job status separately from admission receipts.
- Completed object-backed source uploads return the exact saved occurrence from authorized, input-matched admission before acquiring, writing or reading object storage. New/pending uploads still require canonical input, digest/length verification and separately authorized completion. Receipt replay does not establish current object availability. Public contracts and inline-source behavior are unchanged.

Both migrations are source-reviewed only, unapplied and runtime-unverified. No test, type, lint, browser or SQL execution was performed for this follow-up. Concurrent workspace/firm migrations are outside this repair's ownership.

### Stored submitter identity admission

Forward `2800-preparation-identity-admission.sql` carries the identity-disable rule into durable preparation jobs. Provisioning revokes browser sessions, but can leave an API credential and book membership intact; those alone no longer authorize another queued step for a disabled submitter. Delivery checks the original identity admission between credential/session and membership/book locks. An existing admission row remains locked through the step; an absent row keeps the authentication layer's earlier behavior. Authorized replacement admission can also recognize the disabled original submitter without reversing lock order.

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

Forward3100 future-date schedule amendments,3200 source-preview reparse/supersession
and3300 internal VAT draft amendment reviews are source-integrated. Original schedule
amounts/identities, retained source bytes and historical draft/receipt artifacts remain
immutable. Existing posting/admission guards reject superseded authority. Root source
review found no concrete blocker after superseded preview currentness was made false;
this is not SQL/runtime proof. Bank reconciliation signoff and VAT fact withdrawal are
now integrated as described below. Retained workers continue quarantined recovery
inventory, the tax-account statement register and portable source review artifacts.

No tests, migration application, deployment or provider action is authorized by this
continuation. Narrow static checks are allowed; financial behavior remains unverified.

### Integrated follow-up and static observations

Forward3500 adds evidenced operator signoff of one declared bank account's source
coverage and active-capacity reconciliation. It pins both exact report bases,
independent controls and immutable signed JSON; stale status remains separate from
saved bytes. Forward3700 adds permanent VAT fact withdrawal, explicit retained
exclusions in new v2 drafts, revision refusal and unchanged historical v1/v2 reads.
Both are source-integrated and unapplied. Independent source reviews found no
concrete blocker in3100 schedule posting authority or3500 signoff basis/currentness;
these reviews are not runtime or concurrency proof.

API, contracts and Swedish-domain type checks passed after3500/3700 integration.
Targeted type-aware lint passed on the integrated backend/contracts/calculation and
required VAT-blocker copy consumer. Direct web TypeScript checking was blocked by
concurrent `apps/web/src/components/commerce/command-recovery.ts` generic-schema
property errors; that file was not changed by this backend work. No test, database,
migration, browser or provider exercise ran. Later recovery, tax-account and source
review-artifact work must receive their own integration and static checks.

### Durable-work recovery inventory

The existing local backup/inspect/restore commands now capture and consume exact,
bounded outbox counters, preparation run/job checkpoints and saved posting outcomes.
Snapshot bindings, complete family counts, file hashes and restored semantic equality
are checked by the implementation. A separately hashed suspension report records the
observed database quarantine and expressly withholds worker/provider resumption.
Bundles without the new inventory report missing inventory rather than an empty queue. No migration or
new application authority was needed; see [durable-work recovery](../operations/durable-work-recovery.md).

API (including operations scripts), contracts and Swedish-domain type checks passed
after this integration and the in-progress tax-account/source-review API composition.
This is static evidence only. Backup, restore, quarantine and financial execution have
not been exercised under this continuation.

### Portable source interpretation reviews

Forward3900 is source-integrated through capture/get/list REST and MCP operations.
The saved canonical JSON binds exact original content identity, complete selected-preview
rows/diagnostics and historical review/admission summaries. Approval bearer identifiers
and command material are deliberately absent from review/admission summaries. Reads
return retained bytes, not a reconstruction from current state; bounded complete input
is required. Source review found no concrete blocker. This migration is unapplied and
runtime-unverified; see [source-review artifacts](../../apps/api/docs/SOURCE-REVIEW-ARTIFACTS.md).

The ongoing3800 tax-account integration found a closing dependency gap: represented
tax-account sources must block a tax-family inapplicability claim. Forward3950 is being
implemented to bind that inventory into existing closing/accountant dependencies and
controls.3800 must not be treated as integrated financial readiness before that closure.

### Tax-account closure and explicit schedule estimates

Forward3950 now binds the complete tax-account statement/control dependency into closing
and accountant artifacts. Root comparison against1510 found only the intended tax inventory,
coverage wording and unavailable-provider read guards; existing subledger and other controls
remain. Known tax records cannot be waived by declaring the family inapplicable. Retained
artifact reads remain separate from currentness. The earlier3800 integration gap is addressed
in source, not runtime-proven.

Forward4000 adds evidenced remaining-basis estimates through the existing schedule revision
and posting owners. It preserves occurrence identities and historical prefix, uses explicit
positive future amounts and residual, and conserves net recognized plus future plus residual.
A later reversal makes the estimate unusable until reviewed; ordinary posting preserves peer
captures. Independent source review is in progress. Exact tax-account matching4100 and bounded
asset-disposal work4200 are separate work in progress, not delivered financial authority.

Latest static checkpoint after3950/4000 integration: API (including operations scripts),
contracts and Swedish-domain type checks passed. Direct web TypeScript checking also
passed; the earlier concurrent `commerce/command-recovery.ts` errors no longer reproduced.
This backend work did not edit that file. No web build, browser, test, SQL or runtime
exercise is implied. Integrated recovery/source-review type-aware lint passed on13 files
with zero warnings/errors.4100/4200 remain in progress and need their own completed review.

Independent4000 source review found no concrete blocker in reversed-prefix funding,
correction-replacement exclusion, conservation, stale posting authority or peer-plan
stability. The narrower3100 date-only command still refuses a reversed prefix; such
history requires another explicit estimate review. This distinction is preserved rather
than silently broadening the date-only workflow. No runtime/concurrency proof was produced.

Forward4100 exact tax-account matching is source-integrated, including read-only shared
MCP bindings and the optional historical-compatible matching dependency contract. Human
match/unmatch remains operator-only. Root source review found no concrete blocker in
capacity reservations/conservation, symmetric owner guards, correction fencing or v2
control consumption. New static checks are in progress; no SQL/concurrency acceptance
is implied. Asset disposal4200 and declared-bank-inventory aggregate signoff4300 remain
in progress. A bounded existing-effect VAT settlement link4400 is under feasibility review;
no settlement or new financial authority is delivered by that assignment.

Forward4300 whole-declared-bank-inventory signoff is source-integrated. It composes one
current already-signed account plan for every account in the latest nonempty required
inventory, verifies a common period/cutoff and exact individual artifact identities, and
retains exact prepared/signed aggregate bytes. It rejects peer source gaps and known
undeclared accounts. This is declared-inventory review, not actual-company completeness
or financial close. Root source review found no concrete blocker in membership, scope,
currentness or replay;4300 remains unapplied and runtime-unverified.

Integrated API/scripts/contracts/Swedish-domain type checks passed after4300 composition.
The prior4100 type attempt encountered only the then-uncomposed4300 route; that shared
integration is now resolved. Targeted type-aware lint on tax matching, shared matching
dependencies, subledger contracts/routes/statements and shared capability bindings passed
with zero warnings/errors. No tests or runtime exercises were run.

Independent4100 source review found no actionable financial/security blocker in active
capacity uniqueness/conservation, symmetric bank/owner/commerce guards, correction refusal,
v2 residual consumption or bounded dependency propagation. Runtime proof remains open.

VAT settlement4400 was deliberately not implemented: saved net VAT and existing journal
purposes do not establish the required accounting-effect role, signed comparison or
single-obligation identity. [The decision record](../../apps/api/docs/VAT-SETTLEMENT-FEASIBILITY.md)
identifies those missing semantics without treating an equal amount or tax-account payment
as settlement evidence. No4400 migration or settlement endpoint exists. Work continues on
expense-source withdrawal4500 and saved-report comparison4600 instead of inventing this policy.

Latest source integration includes4200 synthetic no-proceeds disposal,4500 permanent
expense-source withdrawal with linked VAT v3 exclusion, and4600 saved-report comparisons.
Root4200 review found and the owner fixed a missing refusal for declared tax-account
controls; independent financial source review remains in progress. Independent4600 source
review found no actionable correctness/security blocker, including frozen scale, exact
signed differences, missing-side semantics and full-source versus paged totals. Old
reports lacking retained currencyScale remain readable but cannot be compared by guessing
from live metadata. No source history was backfilled.

API/scripts/contracts/Swedish-domain and direct web TypeScript checks passed for this
integrated checkpoint. Root UI edits are limited to exhaustive English/Swedish blocker
copy required by the new withdrawal codes. No tests, browser/build, SQL compilation,
migration application, database workflow, provider action or financial execution occurred.
4200 and4500 independent/source review and all runtime acceptance remain open.

Independent4200 review found no remaining actionable financial/security blocker after
the tax-account control refusal. It traced exact imported-basis/recognition conservation,
same-operator approval, native kernel/deferred aggregate enforcement, disposal correction
fences and effective-date control/closing behavior. This remains source review only; no
journal, disposal, migration or concurrency scenario was executed.

4500 independent review identified a missing SQL authority check: the Effect calculator
excluded facts linked to withdrawn expense sources, but the runtime-granted draft sealer
only fenced direct VAT-fact withdrawal. The owner added both an inclusion refusal and an
explicit excluded/null-contribution/withdrawal-blocker requirement against the live basis.
Root diff review and independent fresh-source recheck confirm that gap is closed. No
remaining blocker was found in the bounded4500 source review. Targeted integration lint
passed with zero warnings/errors. None of this establishes SQL/runtime acceptance.

Next reserved source work is4700 tax-account correction-impact closure and4800 saved
closing-proposal discovery.4900 disposal correction-impact closure follows4700 so the
shared correction resource owner cannot lose either domain contribution. These extend
existing admission/recovery consumers; they add no financial roles or external authority.

4700 tax-account correction-impact resources are source-integrated through the existing
correction contract/owner; no new transport registry is needed. Root compared the complete
function against1700 and4100's actual match basis/view and found only the intended exact
reservation contribution and composition.4800 closing-proposal discovery is source-wired
through the existing closing API/capability/handler groups plus its statement and binding.
It returns50 captured summaries per live page without approval tokens or live provider
checks.4900 terminal-disposal impact disclosure is being added after4700, not in parallel
with replacement of the shared owner. Static checks for the new checkpoint are pending.

4900 is source-integrated with no new registry or contract surface. Root full-function
comparison against4700 confirms only the intended terminal-disposal resource additions.
Independent4800 review found no concrete authorization, cursor, disclosure or historical
recovery blocker. Backend/scripts/contracts/jurisdiction TypeScript checks passed at
`/tmp/openerp-correction-discovery-types.log`. The same checkpoint's web TypeScript check
failed in untouched sales-workspace.tsx: InvoicePaymentNavigation lacks releaseId at
line418 and the line420 id parameter has implicit any. Those separate frontend changes
were preserved; this checkpoint does not claim a clean web check. Runtime/SQL acceptance
remains unverified for all three forward packets.

Metadata-only source occurrence recovery is source-integrated as
`GET /api/v1/entities/:entityId/books/:bookId/source-occurrences/:id/metadata` and
`source_get_occurrence_metadata`. It reuses the existing scoped storage-metadata owner,
then returns an allowlisted public occurrence/admission summary with complete bounded
preview IDs and originalAvailability=not_checked. The existing original-content read is
unchanged and still verifies fetched bytes. No migration, storage adapter change or UI
expansion was added. Independent confidentiality/recovery source review is in progress;
no object-store outage scenario has been executed.

Financial FX remains deferred after inspection of the actual single-currency commerce
owners. FX-01 conversions cannot silently create paired foreign/book-currency capacities
or select settlement/remeasurement effect policy. The maintained open decision and focused
feasibility handoff record the missing choices without inventing an architecture.

5000 retained VAT fact lineage is source-integrated through the existing getVatFact
consumer. Independent review found no actionable blocker in exact fact membership,
version-specific saved assessments/amendment deltas, original field compatibility,
allowlisted disclosure or complete-response bounds. Metadata-only occurrence recovery
also passed independent source review, including preservation of the original download's
integrity failures and absence of storage/approval material in the new projection.

API/scripts/contracts/Swedish-domain and direct web TypeScript checks passed at
`/tmp/openerp-metadata-vat-lineage-types.log` and
`/tmp/openerp-metadata-vat-lineage-web-types.log`. The previous unrelated sales-workspace
errors no longer reproduce; root did not change that component. SQL migrations remain
unapplied. No storage outage, runtime workflow or financial execution was exercised.

5100 exact preparation-job stopping is source-integrated through REST and
`runs_stop_background`. Independent lifecycle review found no blocker in exact identity,
authorization/replay/lock order, terminal safe no-op semantics or the unchanged2800
terminal-delivery fence. The command changes only ready-job state/reason/check time;
it does not cancel the run, remove prepared work or promise remote Workflow termination.

5200 optional expense-source membership is source-integrated through the existing snapshot
list and explicit four-argument statement. Unfiltered requests delegate to0710 unchanged;
filtered requests inspect25 saved snapshots before filtering and continue after empty
matching pages while holding a fixed captured ceiling. Saved v1/v2 assessment semantics
remain separate from live source state. Independent pagination/history review is pending.

Backend/scripts/contracts/jurisdiction TypeScript checks passed at
`/tmp/openerp-job-stop-expense-lineage-types.log`. The web check at this checkpoint failed
in untouched invoice-draft-save.tsx: save.error nullable/code access at line60, plus the
Effect typed-decoder suggestion at line72. These separate frontend edits were not changed.
No SQL/runtime/concurrency/provider execution occurred.

Independent5200 source review found no actionable blocker in scan-before-filter bounds,
empty-page continuation, fixed-ceiling/source/mode isolation, earlier delegation or exact
saved v1/v2 semantics. No runtime paging or concurrency scenario was executed.

5300/5400 source-integrated public reads disclose exact subledger-basis/tax-match line
references. Investigation did not establish a duplicate-posting bypass or a universal
exclusive capacity contract, so no new refusal/role policy was invented. Private helpers,
immutable bodies/digests and financial eligibility stay unchanged.5300 independent review
found no actionable blocker;5400 final independent review and integrated static checks are
pending. No SQL/runtime operation was executed.

Independent5400 review found no actionable blocker. Its getter-only detail schema preserves
unchanged shared match views for lists and saved controls. Exact nullable basis references
remain factual even after unmatch, while5300 discloses only active reservations; neither
side selects a compatibility or exclusive-capacity policy. Root full-function diffs confirm
public wrappers only. Backend/scripts/contracts/jurisdiction and web type checks passed at
`/tmp/openerp-cross-register-references-types.log` and
`/tmp/openerp-cross-register-references-web-types.log`; targeted lint passed with zero
warnings/errors. Prior unrelated invoice-draft-save web errors no longer reproduce, without
root edits to that component. A lexical source comparison of255 TypeScript SQL calls found
no declaration-name/argument-count mismatch (Drizzle table declarations were excluded).
This source comparison is not SQL compilation or execution evidence.

### Commerce admission and saved-intent recovery fixes

5500 aligns shared payment capacity and invoice candidate selection with4100's existing
whole-line tax reservation fence. It does not change capacity arithmetic, stored plans,
receipts, unallocation or policy. Independent source review found no actionable blocker.

Backup/restore evidence controls now treat only uncommitted saved posting command input
as intent: absent/refused outcome AND no scoped reserved-key command receipt. Earlier
kernel execution without an outcome remains strict. Other evidence owners, all syntactic
reference counts, external-pointer refusal, fingerprints and quarantine remain unchanged.
Independent source review found no actionable blocker. Backend/scripts/contracts/jurisdiction
type checks and targeted lint passed at `/tmp/openerp-commerce-recovery-fixes-types.log`
and `/tmp/openerp-commerce-recovery-fixes-lint.log`. No SQL, backup/restore or runtime
execution was performed.

### Bank reservation admission alignment

5600 extends the existing4100 reservation rule to selected-leg preparation, approval,
execution and separate saved-plan currentness. Discovery retains reserved lines and their
unchanged monetary residuals, with an explicit `tax_account_reserved` blocker and required
EN/SV labels in the existing copy map. No private bank amount/version, reconciliation,
signoff or unmatch owner changes. Independent source review found no actionable blocker.
Backend/scripts/contracts/jurisdiction and web type checks passed at
`/tmp/openerp-bank-admission-fix-types.log` and
`/tmp/openerp-bank-admission-fix-web-types.log`; targeted lint passed with zero warnings/errors.
No SQL compilation, execution or concurrency proof was performed.

The owner-register counterpart needs no extra tax check: allocation helpers consume existing
immutable owner effects, and4100 fences both admission orders. Owner allocation never releases
that source-line ownership. No redundant owner-helper patch was added.

### Case ownership, explanation cursors and source mapping

5700 captures exact correction-bundle ownership for case/plan references and replaces
misleading standalone REST/MCP guidance for owned plans with complete-bundle recovery.
Old snapshots and no-owner outputs are preserved. The hardcoded browser review handoff
remains unresolved; this is not a complete web-flow repair.

5800 binds report explanation cursors to their saved report/account and a real included
opening or movement row. The earlier two-part cursor is invalid; omitting `after` starts page1.
Stored reports, accounting values, ordering and other cursor families are unchanged.

5900 makes conflicting retained-source/account mappings stale preview GET and new review
captures and refuses fresh approval/admission, using the importer's existing exact rule.
Unrelated mappings, saved dependency shapes, history and successful-key recovery remain
unchanged. All three packets passed independent source review without an actionable blocker.
Backend/scripts/contracts/jurisdiction and web types passed at
`/tmp/openerp-case-report-source-fixes-types.log` and
`/tmp/openerp-case-report-source-fixes-web-types.log`; targeted lint passed with zero warnings
or errors. No SQL compilation/application, runtime/concurrency or external-provider proof
was performed.

6000 repairs only the automatic preparation-job stop branch's PL/pgSQL local binding.
The former function-qualified local could fail before persisting `stopped`; the distinct
`stop_reason` variable removes that source defect without changing stop reasons, authority,
locks, checkpoint/results or step idempotency. Root and independent full-function diffs
found only the intended identifier/binding substitution. SQL compilation/execution remains
unverified; prior TypeScript checks are not evidence for this SQL branch.

Forward6100 adds explicit future installment-count changes through the existing estimates
command. It preserves posted/full-reversed prefix bytes and immutable carrying basis/accounts,
assigns fresh never-reused keys to the replacement future suffix, and independently enforces
complete old/new suffix validation and exact conservation in the physical revision guard.
Preparation state follows pinned evidence/ordinal/key identity; ordinal attempt counters still
span every generation. Existing posting/dependency guards and all-history retired-key fences
remain unchanged. No automatic/legal lifetime, zero cessation or fully posted reopening was
added. See [the estimate handoff](../../apps/api/docs/SUBLEDGER-ESTIMATE-AMENDMENTS.md).

Root and both independent6100 source reviews found no concrete blocker. API/scripts,
contracts, Swedish-jurisdiction and direct web type checks passed; targeted subledger-contract
lint reported zero warnings/errors. SQL remains unapplied and uncompiled; no runtime,
concurrency, financial outcome or actual-company proof is implied.

6300 adds actor/book/key-bound recovery of committed source-retention results without original
bytes or storage access. It returns only the frozen occurrence result for the two retention
operations. Pending or absent results remain non-final; no completion or new-key authority is
implied.

6400 binds accountant row cursors to pack, section and a real saved ordinal, leaving
list cursors, complete JSON/CSV and SIE artifacts unchanged. Numeric-only cursors are invalid;
omitting `after` restarts the section.

6500 recovers the exact consumed commerce allocation approval through its receipt FK;
uncommitted latest-approval behavior stays unchanged.

All three changes passed root and independent source review. API/scripts/contracts/Swedish
jurisdiction and direct web type checks passed; targeted lint found zero warnings/errors on
five integration/contract files. No tests, SQL compilation/application, runtime or concurrency
checks were performed. External6200 bank workspace work was preserved, not owned by this slice.

Forward6600 repairs owner-allocation consumed-approval recovery only. Applied reads follow
and validate their retained receipt's exact approval; pending reads keep their old selection.
Root and independent source review found no blocker. No write, authority, capacity, replay,
schema or UI change was made; SQL remains unapplied and runtime-unverified.

Similar-looking bank getters were deliberately not changed: their approval field represents
current pending authority, while executed callers use the immutable execution first. Closing
receipts/certificates already retain exact consumed approval identity; disposal returns the
bounded full approval history and explicit winning review. No grounded defect was found there.

Forward6700 completes a one-shot operator classification resolution for originally unknown
tax-account events. The new REST command/read and read-only MCP getter are integrated. Matching
pins an immutable resolution reference; controlv3 uses effective unknown classifications while
retaining original statement bytes and all financial calculations. Account/closing dependencies
include resolution inventory only when nonempty. No reclassification, capacity release, legal
role, financial posting or readiness claim is introduced.

Root and two focused implementation reviews found no blocker. Backend/scripts/contracts/
Swedish-jurisdiction and web type checks passed; targeted lint found zero warnings/errors on
five files. Nine owned files were formatted. SQL remains unapplied/uncompiled; no tests,
application/runtime/concurrency or provider execution was performed.

Forward6800 integrates the live unresolved tax-event worklist with the existing classification
resolution flow. The50-row scan window precedes classification filtering;51st-row lookahead,
real retained anchors and book/account-bound cursors prevent skipped sparse-window work.
Membership is live, not frozen; callers follow non-null next even for empty items and restart
for new arrivals. No saved artifact or financial transition is introduced. Root and focused
peer source review found no blocker. Backend/contracts/jurisdiction type checks and lint pass.
The initial web check encountered unrelated invoice UI pagination edits; the follow-up shared
web check passed without changes to those files by this slice. No SQL/runtime/provider/test
execution was performed.

Forward6900 adds unaccepted supplier-invoice draft create/revise/get/list/history and three
read-only MCP capabilities. It reuses exact customer line calculations through a private role
parameter while keeping supplier storage and sales/issue resources separate. Original source
number/evidence, asserted identities, nullable tax and mismatches are preserved; recognition
elsewhere is not assessed. No acceptance, posting, numbering, VAT, capacity or provider effect
is introduced. Backend/contracts/jurisdiction and web type checks pass, and targeted lint is
clean. Customer-branch source normalization reconstructs1200 byte-for-byte. No SQL/runtime/
financial execution proof is claimed.
