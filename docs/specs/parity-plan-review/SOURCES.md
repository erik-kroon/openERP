# Evidence and review coverage

Reviewed repository: `erik-kroon/openERP@ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb`, commit message `parity backlog`.

This review read the new parity document across ranges covering all 854 lines, the added ADR through its commit diff and selected supporting maintained plans/current files. It did not reproduce the original folder-level Accounted comparison, inspect every application file or run the product. The reference repository revision used by the author is not identified in that new document; historical pins elsewhere in the conversation are not silently substituted for it.

Each P/C identifier below is a source reference within this dossier. Proposed owner links and corrected algorithms are review conclusions, not source implementation claims. Line ranges name the repository file ranges requested/read; connector responses wrap most contents in one JSON line.

## Repository sources

### P01

`docs/plans/11-parity-backlog.md`. Reviewed range: 1-79.

Planning scope, A/B/C, folder dispositions and provider gating.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/11-parity-backlog.md)

### P02

`docs/plans/11-parity-backlog.md`. Reviewed range: 80-107.

PRY-01 through PRY-20.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/11-parity-backlog.md)

### P03

`docs/plans/11-parity-backlog.md`. Reviewed range: 174-200.

Pay-run absence claim and PRY-59 through PRY-74.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/11-parity-backlog.md)

### P04

`docs/plans/11-parity-backlog.md`. Reviewed range: 108-173.

PRY-21 through PRY-58.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/11-parity-backlog.md)

### P05

`docs/plans/11-parity-backlog.md`. Reviewed range: 201-246.

PRY-75 through PRY-85 and scope gates.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/11-parity-backlog.md)

### P06

`docs/plans/11-parity-backlog.md`. Reviewed range: 247-425.

R1 through initial R6.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/11-parity-backlog.md)

### P07

`docs/plans/11-parity-backlog.md`. Reviewed range: 426-565.

R6-R11, start R12.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/11-parity-backlog.md)

### P08

`docs/plans/11-parity-backlog.md`. Reviewed range: 566-710.

R12-R19.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/11-parity-backlog.md)

### P09

`docs/plans/11-parity-backlog.md`. Reviewed range: 711-854.

R19-R25 and checker scope.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/11-parity-backlog.md)

### P10

`docs/adr/0011-reference-parity-backlog.md`. Reviewed range: entire added file in commit diff.

Accepted decision under review; not activated by this review.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/adr/0011-reference-parity-backlog.md)

### C01

`AGENTS.md`. Reviewed range: entire file.

Application ownership, tx passing, jobs, UI and test permissions.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/AGENTS.md)

### C02

`docs/plans/README.md`. Reviewed range: 1-170.

53-packet baseline, 101 edges, core/product scope and replacement evidence pointer.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/README.md)

### C03

`docs/plans/05-vat-payroll-assets-fx.md`. Reviewed range: 1-150 returned range.

PayRunRevision, PayRunPosting, PAY-01..04 and other core domain definitions; later historical tail not fully returned.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/05-vat-payroll-assets-fx.md)

### C04

`docs/plans/07-restore-operations-cutover.md`. Reviewed range: 1-125.

OPS-03 provider uncertainty, delivery and operational ownership; includes labelled historical implementation notes.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/07-restore-operations-cutover.md)

### C05

`apps/api/docs/BANK-CONNECTOR.md`. Reviewed range: 1-95.

Current bank-connector owner plus expressly labelled historical details; not a claim of live provider acceptance.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/apps/api/docs/BANK-CONNECTOR.md)

### C06

`docs/plans/evidence/application-owned-replacement-complete.md`. Reviewed range: 1-100.

Repository-reported implementation and local verification; not rerun here.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/evidence/application-owned-replacement-complete.md)

### C07

`docs/plans/03-imports-matching-reconciliation.md`. Reviewed range: 80-150.

Existing IMP-01..06 ownership and independent controls.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/03-imports-matching-reconciliation.md)

### C08

`docs/plans/04-invoices-payments-registers.md`. Reviewed range: 1-120.

Cash-method unpaid year-end, credits and payment/recognition ownership.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/04-invoices-payments-registers.md)

### C09

`Git tree 68880b7ce62b66c790cb81ccf06ba75c62b2aef1`. Reviewed range: complete root listing, truncated=false.

No references directory in the reviewed root; attempted references/accounted/lib returned404.

[Source](https://api.github.com/repos/erik-kroon/openERP/git/trees/68880b7ce62b66c790cb81ccf06ba75c62b2aef1)

### C10

`docs/plans/06-year-end-reports-filing.md`. Reviewed range: 1-125.

END-01..07, complete groups, artifacts and currentness.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/06-year-end-reports-filing.md)

### C11

`docs/plans/evidence/work-packages.json`. Reviewed range: 1-90.

Generated core count and opening packet metadata; full 53-node graph not independently reconstructed here.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/docs/plans/evidence/work-packages.json)

### C12

`apps/api/src/application/banking/allocations.ts`. Reviewed range: 1-180.

Current allocation owner, exact grouping, per-leg capture and source admission import; not full execute audit.

[Source](https://github.com/erik-kroon/openERP/blob/ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb/apps/api/src/application/banking/allocations.ts)

## Narrow primary-source checks

### E01: Forsakringskassan: sick pay

Narrow support for entitlement/waiting-deduction distinction and schedule/agreement exceptions. Not a complete payroll policy qualification.

[Official source](https://www.forsakringskassan.se/arbetsgivare/sjukdom-och-skada/sjuklon)

### E02: Forsakringskassan: karens deduction

20% of average weekly sick pay and collective-agreement relevance; applies only in its stated context.

[Official source](https://www.forsakringskassan.se/arbetsgivare/sjukdom-och-skada/karensavdrag)

### E03: Peppol BIS Billing rule set, May 2026

BR-CO-13/15/16 and related monetary rules. Individual BR-CO-16 also opened; full schema/taxonomy bundles not qualified.

[Official source](https://docs.peppol.eu/poacc/billing/3.0/rules/ubl-tc434/)

### E04: Skatteverket: starting a business and bookkeeping methods

Narrow cash-method/year-end distinction. No company eligibility, complete tax period rule or actual source data verified.

[Official source](https://www.skatteverket.se/foretag/drivaforetag/startaochregistrera/fordigsomvillstartaforetag.4.6e8a1495181dad540842251.html)

## Explicit limits

- No reference-code correctness or real-data validation is established by a statement that a reference is mature. The audit distinguishes flawed plan pseudocode from unknown upstream implementation.
- The application replacement evidence is the repository's own reported observation. Its tests, temporary artifacts and current production behavior were not rerun by this review.
- No source mutation, repository commit, application test, SQL migration, provider request using credentials, financial posting or statutory submission was performed.
- No complete current payroll, VAT, bank-clearing, Peppol schema or other regulatory/data profile was qualified. The review deliberately does not replace incomplete formulas with invented current rates or legal conclusions.
- The local checker validates this generated plan and illustrative counterexamples. It is not the repository's `check-plan.py` and not runtime evidence.
