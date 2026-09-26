# Sources and evidence boundaries

This v2 rewrite uses the attached 25-packet pseudocode archive, its rule-data contract and the attached application-ownership amendment. The amendment records the selected ADR 0010/0009 architecture at `422276ae5ed9d0ca146447d92bb3d27c99f8c48a`; the task/source baseline below is the earlier `bb628452196a55ceef7516f76fc3cd6471ae4d91`.

No fresh repository review, external provider request or legal/regulatory verification was performed in this rewrite. References S01 onward and X01 onward are inherited evidence from the source dossier. Treat words such as “current” in their historical titles as describing that pinned baseline, not a newly observed state. Earlier claims that a document was read directly describe the original dossier's work, not this rewrite.

The old SQL ownership/migration instructions are superseded by the supplied amendment. Financial requirements and bounded example calculations remain design inputs, not proof of correctness for a real company. Rule tables, exact formats and company facts still need qualified evidence.

## Application-owned source inputs

- Attached `APPLICATION-OWNERSHIP-AMENDMENT.md`, based on the prior review at the application-owned revision.
- ADR 0010, `docs/adr/0010-application-owned-accounting-replacement.md`, content supplied in the conversation and summarized by the amendment.
- ADR 0009, `docs/adr/0009-effect-mq-background-jobs.md`, content supplied in the conversation and summarized by the amendment.
- User-supplied allocation source showing application operations, explicit tx-passing reads/writes and receipt recovery. It is supporting design context, not runtime proof or the full implementation specification.

## Repository references

### S01: Repository engineering and test-change constraints

`AGENTS.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/AGENTS.md

Evidence level: instructions. Inherited from the supplied packet evidence registry.

### S02: Adopted design versus remaining facts and proof

`docs/open-decisions.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/docs/open-decisions.md

Evidence level: maintained decision record. Inherited from the supplied packet evidence registry.

### S03: Adopted FX, VAT and impairment contracts

`docs/adr/0008-financial-fx-vat-impairment.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/docs/adr/0008-financial-fx-vat-impairment.md

Evidence level: adopted design, not runtime proof. Directly reread at this commit during this pseudocode task.

### S04: Current Effect, transport and PostgreSQL ownership

`apps/api/README.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/README.md

Evidence level: implementation documentation. Inherited from the supplied packet evidence registry.

### S05: Case review routes a bare latestPlanId

`apps/web/src/components/case-context.tsx`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/web/src/components/case-context.tsx

Evidence level: implementation inspected. Inherited from the supplied packet evidence registry.

### S06: Correction-bundle provenance and unresolved browser handoff

`apps/api/docs/CASES.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/CASES.md

Evidence level: implementation documentation. Inherited from the supplied packet evidence registry.

### S07: Supplier posting and partial credits already exist; actual VAT and paid refunds remain separate

`apps/api/docs/SUPPLIER-ACCEPTANCE-PAYMENTS.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/SUPPLIER-ACCEPTANCE-PAYMENTS.md

Evidence level: implementation documentation with bounded recorded observations. Inherited from the supplied packet evidence registry.

### S08: Actual-profile refusal and synthetic exact-25-percent calculation

`jurisdictions/se/src/vat/calculation.ts`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/jurisdictions/se/src/vat/calculation.ts

Evidence level: implementation inspected. Inherited from the supplied packet evidence registry.

### S09: Offline payment exports stay reserved after reported rejection

`apps/api/docs/PAYMENT-RECOVERY.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/PAYMENT-RECOVERY.md

Evidence level: implementation documentation with bounded recorded observations. Inherited from the supplied packet evidence registry.

### S10: Per-page cursor persistence and unsupported mutation-window recovery

`apps/api/docs/PLAID-CONNECTOR.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/PLAID-CONNECTOR.md

Evidence level: implementation documentation with bounded recorded observations. Inherited from the supplied packet evidence registry.

### S11: Raw connector observations are not bank-accounting admission

`apps/api/docs/BANK-CONNECTOR.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/BANK-CONNECTOR.md

Evidence level: implementation documentation with bounded recorded observations. Inherited from the supplied packet evidence registry.

### S12: Owner facts, effects and allocations; actual treatment and corrections remain bounded

`apps/api/docs/OWNER-REGISTER.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/OWNER-REGISTER.md

Evidence level: implementation documentation; early integration paths may be historical. Inherited from the supplied packet evidence registry.

### S13: Existing staging, financial import and read-only historical items

`apps/api/docs/SIE-HISTORICAL-IMPORT.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/SIE-HISTORICAL-IMPORT.md

Evidence level: implementation documentation with bounded recorded observations. Inherited from the supplied packet evidence registry.

### S14: Existing bounded SIE4I renderer

`jurisdictions/se/src/sie/encoder.ts`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/jurisdictions/se/src/sie/encoder.ts

Evidence level: implementation inspected. Inherited from the supplied packet evidence registry.

### S15: Existing frozen trial balance and earlier-posting opening semantics

`apps/api/docs/REPORTS.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/REPORTS.md

Evidence level: implementation documentation. Inherited from the supplied packet evidence registry.

### S16: Dimension catalog contracts

`packages/contracts/src/dimensions.ts`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/packages/contracts/src/dimensions.ts

Evidence level: implementation inspected. Inherited from the supplied packet evidence registry.

### S17: Bounded legal customer invoice issue; credits remain unsupported

`apps/api/docs/AR-LEGAL-ISSUE.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/AR-LEGAL-ISSUE.md

Evidence level: implementation documentation with bounded recorded observations. Inherited from the supplied packet evidence registry.

### S18: Existing exact-description preparation runs, not general invoice accounting

`apps/api/docs/AUTOMATION.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/AUTOMATION.md

Evidence level: implementation documentation. Inherited from the supplied packet evidence registry.

### S19: 9050 plus 9107 employee/work-input foundation

`apps/api/docs/PAYROLL-FOUNDATION.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/apps/api/docs/PAYROLL-FOUNDATION.md

Evidence level: implementation documentation. Inherited from the supplied packet evidence registry.

### S20: Financial closing, tax bridge and statutory output requirements

`docs/plans/06-year-end-reports-filing.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/docs/plans/06-year-end-reports-filing.md

Evidence level: working plan, not implementation proof. Inherited from the supplied packet evidence registry.

### S21: Product capability inventory and accounting packet aliases

`docs/plans/capability-backlog.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/docs/plans/capability-backlog.md

Evidence level: working plan. Inherited from the supplied packet evidence registry.

### S22: Retained money representation, licensing and deferred Rust extraction

`docs/architecture-followup.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/docs/architecture-followup.md

Evidence level: maintained design record. Inherited from the supplied packet evidence registry.

### S23: Historical implementation checkpoints; compare later feature notes before using

`docs/plans/accounting-completion-wave.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/docs/plans/accounting-completion-wave.md

Evidence level: historical progress log. Inherited from the supplied packet evidence registry.

### S24: Scope and delivery checkpoints

`docs/roadmap.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/docs/roadmap.md

Evidence level: maintained roadmap with historical entries. Inherited from the supplied packet evidence registry.

### S26: Maintained documentation entrypoint

`docs/README.md`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/docs/README.md

Evidence level: repository documentation. Inherited from the supplied packet evidence registry.

### S27: Current journal lines lack dimension assignments; shared action union includes VAT work

`packages/domain/src/ledger.ts`

https://github.com/erik-kroon/openERP/blob/bb628452196a55ceef7516f76fc3cd6471ae4d91/packages/domain/src/ledger.ts

Evidence level: implementation inspected; shared WIP-sensitive contract. Inherited from the supplied packet evidence registry.

## Official external references inherited from the original dossier

X identifiers are scoped to this dossier. They do not inherit the numbering of the earlier handoff. Those prior checks supported narrow source observations, not blanket qualification of Swedish accounting, tax or provider behavior.

### X01: Plaid Transactions errors

https://plaid.com/docs/errors/transactions/

Pagination mutation requires restarting the affected window from its original cursor. Other error classes are not automatically the same recovery.

### X02: Plaid Transactions Sync migration

https://plaid.com/docs/transactions/sync-migration/

Complete-window retrieval and added/modified/removed processing inform staged publication. This dossier makes no live Plaid request.

### X03: Plaid Transactions API

https://plaid.com/docs/api/products/transactions/

Provider update identity, cursor fields, pending relationships and amount semantics must follow the selected response contract. Exact HTTP bytes remain evidence, not proof of complete bank coverage.

### X04: BFN framework-version applicability

https://www.bfn.se/vilken-version-av-k-regelverken-ska-jag-tillampa/

Select the accounting framework by the actual fiscal-year applicability rules and exceptions. A current calendar date is not a universal rule-version selector.

### X05: Skatteverket: services from another EU country

https://www.skatteverket.se/foretag/moms/kopavarorochtjanster/inkopfranandraeulander/kopatjansterfranandraeulander.4.361dc8c15312eff6fd1d011.html

General-rule business service purchases can require basis in box 21, output VAT in the applicable box and separately eligible input deduction. Do not apply this merely from a foreign supplier name.

### X06: Skatteverket: services from outside the EU

https://www.skatteverket.se/foretag/moms/kopavarorochtjanster/inkopfranlanderutanforeu/kopatjansterfranlanderutanforeu.4.361dc8c15312eff6fd33a46.html

The corresponding qualified general-rule service-purchase basis is distinguished through box 22. Exceptions, tax-point conversion and deduction remain explicit.

### X07: SIE Group format family

https://sie.se/format/

Voucher transfer and transaction export with the preceding balance information are distinct format purposes. Exact record grammar/versions still require their own qualified specification.

### X08: Skatteverket machine-readable tax tables

https://www.skatteverket.se/specialversionerforprogramforetagmfl.4.319dc1451507f2f99e86ee.html

Payroll must use the exact dated table/column/formula or an applicable individual decision. No complete table data set was downloaded or qualified here.

### X09: Skatteverket employer contributions

https://www.skatteverket.se/arbetsgivaravgifter

Rates, eligibility and thresholds are effective-dated inputs. The payroll examples in this dossier are synthetic, not actual Swedish contribution rates.

### X10: Skatteverket cash-principle guidance

https://www4.skatteverket.se/rattsligvagledning/edition/2026.7/325040.html

Search-supported guidance on paid/provided compensation, cross-checked with AGI item guidance. Direct retrieval of this legal-guidance page failed; no broader legal interpretation is attributed to it.

### X11: Skatteverket AGI fields and individual identity

https://www.skatteverket.se/agbeskrivning

The reporting identity includes employer, period, payee and specification number. Preserve the same identity for a replacement instead of creating another individual item. The technical portal also surfaced inconsistent 1.1.18.x labels, so exact XSD bytes must be pinned independently.

### X12: Skatteverket AGI corrections

https://www.skatteverket.se/foretag/arbetsgivare/lamnaarbetsgivardeklaration/rattaenarbetsgivardeklaration.4.2cf1b5cd163796a5c8b6698.html

Reported withholding cannot ordinarily be lowered as a routine amendment. The initial profile refuses that change without a separately qualified exception and keeps authority outcomes distinct.

### X13: Skatteverket SRU file transfer

https://www.skatteverket.se/foretag/etjansterochblanketter/allaetjanster/tjanster/filoverforing/informationomsruuppgifter.4.3dfca4f410f4fc63c86800020896.html

Search-supported identification of INFO.SRU and BLANKETTER.SRU. Direct page retrieval was unsuccessful. No exact field-code map, encoding or current grammar bundle is certified here.

### X14: Skatteverket Inkomstdeklaration 2

https://www.skatteverket.se/4.39f16f103821c58f680006188.html

INK2, INK2R and INK2S are distinct parts of the corporate declaration. The calculation and mapped form values must reconcile; obtaining a form is not proof that an exported SRU file is accepted.

## Deliberately not claimed

No current full BAS data release, payroll tax table, SRU field map, AGI XSD bundle, K2 taxonomy or provider agreement was completely ingested and qualified. Those are enumerated data inputs in [the rule/form data contract](01-RULE-AND-FORM-DATA.md), not guessed examples. No production credentials, user documents, vendor raw corpus, source code or fonts are distributed in this dossier.

No repository patch, applied migration, application test, hosted deployment, actual-company posting, payment, declaration filing or provider acceptance was performed by producing this pseudocode.
