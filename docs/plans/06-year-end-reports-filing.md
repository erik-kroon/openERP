# Year-end, statutory reports and filing

Owner: closing, reports and obligations, consuming explicit domain dependencies. Phase: P6/P7. Reuse the current technical close/reopen and trial-balance snapshot drafts; technical locking remains distinct from statutory readiness.

## Outcome and state boundaries

The user can establish that every applicable period/year obligation is accounted for, approve necessary adjustments, close a reviewed basis, derive the next opening once, generate reproducible reports and statutory files, sign the intended bytes and record the actual external result. A reopened year preserves its previous close evidence and artifacts; it does not make old filings disappear.

Separate states for period mutation lock, reconciliation signoff, financial close certificate, artifact validation, signature, submission and authority acceptance. Each state identifies a revision and evidence. A report can remain valid historical evidence while being stale for current books. A successful technical lock cannot claim completeness of missing payroll, tax, inventory or disclosures.

## Close inventory and dependency contract

The reviewed inventory declares required bank/source accounts, invoice/open-item registers, tax periods/accounts, payroll runs/declarations, assets/deferrals, FX populations, owner balances, other material balances, external schedules and required disclosures. Every family has required, not-applicable-with-evidence or unsupported/unknown status. No rows in a module never means the module is irrelevant.

Each domain provides a bounded dependency snapshot: owning revision/watermark; required versus executed checks; unresolved cases; control balances; applicable rule/profile versions; and exact readiness/blockers. Closing consumes that contract and does not inspect guessed table presence to decide completeness. Relevant source/register changes invalidate current readiness. Unrelated later activity outside the selected scope can leave historical artifacts intact.

`CloseProposal` binds inventory, period/year boundaries, ledger cutoff, opening basis, all domain dependencies, adjustment/transfer plans and check results. `CloseApproval` binds digest and authority. `CloseCertificate` retains approved basis, applied effects, effective cutoffs and receipt. `OpeningSet` binds the preceding approved close or declared migration basis, account balances, source provenance and approved version.

## Close, reopen and opening algorithm

Prepare diagnostics and adjustments outside the transaction. Commit approved adjustment groups through their owning domain; repeat readiness against the resulting cutoffs. Under the book barrier, lock the relevant periods, recheck the full dependency manifest, verify required checks and approval, apply permitted mechanical close effects, change lock state, persist certificate/receipt and outbox together. A failed recheck leaves the previous lock/certificate state intact.

A mechanical result transfer has explicit posting purpose, separate from operating activity. Income-statement/report rules include ordinary and correcting activity while handling transfers according to the selected report basis. They cannot erase the year's activity merely because balance-sheet closing entries were posted.

Generate the next OpeningSet from the approved balance-sheet basis exactly once. Choose a single reporting representation: opening set plus within-year movements. An imported opening voucher that already represents the set is mapped as that basis, not added again. New prior-year corrections invalidate dependent current readiness and require an explicit opening-impact proposal; old snapshots remain reconstructable.

Reopen is a separate approved action with reason and downstream impact list: certificates, opening sets, report versions, signatures and submitted artifacts. Reopening permits new work but does not silently rewrite their states to “never existed.” If a filed period is affected, create a review/amendment obligation. External cancellation/resubmission follows the provider's actual contract and separate authority.

## Reports and lineage

Extend the current `ReportSnapshot` and contribution model with opening-set version, company/year/profile, source/register cutoffs, mappings/rules, required-check coverage and non-ledger facts. Retain immutable semantic rows, formula/rounding basis and included/excluded contribution locators. For each displayed figure, explanation returns the same computation's inputs at the same snapshot, with stable paginated continuation and full totals.

Accept only complete committed group boundaries as ledger cutoffs, following the posting contract. An intermediate sequence is an explicit `InvalidSnapshotBoundary` refusal with permitted alternatives. A snapshot and its pagination cursor pin the chosen boundary; later pages cannot acquire a newer cutoff.

Report families cover trial balance, general ledger/journal register, balance sheet, income statement, receivable/payable ageing, bank/tax/asset/payroll control reports, cash-flow where applicable, tax bridge and statutory statements. Each family states date/cutoff/opening/transfer semantics. A UI filter creates a new view/snapshot identity; it does not silently alter the meaning of an old report ID.

Compare independently expected controls, previous periods and original source evidence. Coverage is not inferred from balanced columns. Two offsetting missing transactions, a missing bank account or unclassified tax facts prevent a complete-readiness label.

## Tax bridge and annual-report model

`TaxBridge` links accounting result to each reviewed taxable-result adjustment, temporary/permanent difference, supporting schedule/rule and exact statutory field. Carry forwards, reserves and other company-required treatments have distinct evidence and history. A valid SRU code is not proof that a figure belongs there. Rule/mapping corrections identify all affected prior artifacts.

`AnnualReportModel` combines immutable financial statements, comparatives, framework-specific disclosures, entity/profile facts, governance/meeting/adoption evidence and proposed signer roles. Required non-ledger facts cannot be fabricated from bookkeeping entries. K2 and K3 are separate applicability/disclosure matrices; a partial K3 draft cannot be released as a complete annual report. The [BFN rule catalogue](https://www.bfn.se/redovisningsregler/vagledningar/k-regelverk/) publishes different framework versions and applicability periods; selecting and reviewing the correct complete rule bundle is a release input, not a date default.

The UI presents unresolved disclosures, source/assumption evidence and comparative changes before finalization. Signature inputs are explicit: which semantic content and exact rendered bytes are covered; which later metadata may change; and what invalidates the signature. A changed financial fact, mapping, disclosure or signer authority produces a new version requiring appropriate review.

## Artifact and filing contracts

`ArtifactManifest` includes semantic snapshot/model ID, generator version, mapping/schema/taxonomy/entry-point versions, exact content hash/size/media type, storage version, validation runs and allowed use. Render readable and machine-readable outputs from the same semantic model. SIE 4/4i/5, INK2/SRU, payroll declaration files and iXBRL each have independent structure and semantic gates; one parser pass cannot establish the others.

Independent validation is pinned to validator binary/container, configuration and schema/taxonomy bytes. Unavailable or incomplete validation cannot pass a required gate. Retain negative examples that are structurally valid but semantically wrong. The Bolagsverket [technical documentation entry point](https://bolagsverket.se/apierochoppnadata/lamnaforetagsinformation/digitalinlamningavarsredovisningochrevisionsberattelse/tekniskdokumentationfordigitalinlamningavarsredovisning.5937.html) was discoverable but returned an access challenge during planning; no exact current provider state graph or certification is claimed from that page. D-10 must obtain the actual contract before connected filing.

An `Obligation` names the entity, family, reporting period, applicable rule/deadline source and fulfillment evidence required. `SubmissionAttempt` binds exact artifact and authorized signer/submitter, provider/environment, correlation/idempotency identity and request time. Append provider observations verbatim or by verified retained reference; validate their scope and authenticity. Local states are prepared, validation-blocked/validated, awaiting-signature, signed, admitted-for-submission, submitted-pending, outcome-unknown, rejected, accepted and superseded, with transitions mapped to the selected provider contract. Do not assume that every provider implements every state identically.

If the provider accepts and the response is lost, first recover by correlation/artifact identity. A later retry is allowed only under the provider's duplicate semantics or after reviewed resolution. Required signature/adoption/acceptance events remain separate; an HTTP 200 upload never implies the whole legal obligation is fulfilled. Acknowledgments and prior submitted bytes are archived with the books.

## Delivery packets

| ID     | Deliverable                                                                                  | Depends on             | Acceptance                                                                                                               |
| ------ | -------------------------------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| END-01 | Complete technical close/reopen with explicit inventory and domain dependency contracts.     | PST-03, IMP-05, FND-03 | E-07/E-10: close/post race ordered; missing family inventory blocks; certificate states exact technical scope.           |
| END-02 | Financial close, result-transfer semantics, opening sets and prior-period impact.            | END-01, COR-02, COM-06 | E-14/E-16: openings counted once, activity preserved and old snapshots unchanged; applicable domain gates also required. |
| END-03 | Extend current snapshot/explanation engine to explicit opening and source/register coverage. | PST-03, IMP-01         | E-10/E-15: concurrent pagination reconstructs one prefix; excluded/missing contributions remain visible.                 |
| END-04 | Reviewed tax bridge and exact field lineage with historical mapping impact.                  | END-02, VAT-04         | E-16/E-18: independently expected adjustments/fields and retained prior artifacts.                                       |
| END-05 | Complete selected K2/K3 statement/disclosure/compare/signature model.                        | END-02, END-03         | E-16: missing disclosure cannot finalize; financial/non-ledger facts and signer scope versioned.                         |
| END-06 | Format-specific generation, pinned validation and portable artifact manifests.               | END-03, IMP-02         | E-18: roundtrip/semantic negatives for each released format. Tax formats also require END-04; annual formats END-05.     |
| END-07 | Obligation, signature, submission and provider outcome/amendment workflow.                   | END-06, OPS-03, FND-02 | E-19: lost response and pending signature remain honest; exact bytes and actual acknowledgment bound.                    |

END-03 can proceed early and serves VAT/FX without waiting for year-end. END-01 is a technical gate; END-02 adds every applicable VAT/payroll/asset/FX/control completion before company close. Export families progress independently once their own semantic model exists. No cycle is created by requiring every statutory family before a simple trial balance.

## Bounded first-year review package

The END-03 source slice in [ACCOUNTANT-REVIEW.md](../../apps/api/ACCOUNTANT-REVIEW.md) adds retained accountant-review packs over current internal trial-balance snapshots. It materializes exact balances, voucher/receipt/evidence lineage, original retained evidence and separate missing/excluded coverage. JSON and CSV bytes are retained with hashes; old packs survive later changes and reopen.

This is synthetic review tooling, not company activation or full END-03 acceptance. Opening explanations remain unverified, owner-funding and expense-tax source/review controls are captured while legal treatment and complete openings remain unverified, and first year never implies zero opening or zero VAT. No Visma compatibility, result transfer, annual-report/SIE/iXBRL generation or filing is claimed. Root integration, native/runtime observations and the concurrency/browser/independent-correctness gates remain separate from source delivery.

Forward0820 binds the released owner-register and expense-review provider digests into technical closing. Unresolved/unlinked owner sources, missing/stale expense reviews and unsupported/unreconciled known expense sources block new technical close proposals; unpaid linked claims do not. Historical0800 approvals/certificates keep their original meanings and bytes and cannot silently acquire the new dependency coverage.
