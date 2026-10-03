# Reusable invoice templates. Local verification.

Verified on2026-10-03 against main parent `7e9d89e`. Source inventory `ef03eb3e4f46c5ce87dbb9f84afc273e4abfca23d74e695d94f1de531f889430` remained stable throughout the final runtime.

## Delivered behavior

Book-scoped immutable template revisions retain reusable content, qualified currency and note. They exclude customer identity, dates, recipient and legal numbering. Exact selection creates an ordinary commercial draft or explicitly replaces an unissued operator draft. Replays recover committed receipts after archive, while fresh selection must be current and active. Applied draft history retains template provenance, and ordinary edits preserve it.

The existing saved invoice composer can save, start and replace template content. Automation can prepare a new draft but cannot replace an operator draft. Retained articles must match their exact reference, description, unit, price and treatment; fresh selections require current active revisions.

Commercial legal PDFs preserve the canonical legal issue owner's exact calculated/issued totals and lines. They require source-total equality for source transcription, while commercial drafts retain their separate calculation basis. A customer-facing note remains in the actual issued PDF after its template changes. No external delivery occurred.

## Proof

Fast and full changed-file gates passed against `7e9d89e`. Type-aware lint using the current primary configuration passed with warnings denied. The final four-file E2E cohort passed13/13 in32.24s. It includes eight template journeys, three existing pdfcn regressions, body-refusal regression and performance. The browser exercises keyboard editing, explicit replacement and320px width. Paper visual composition and native200% zoom were not observed.

Five warmups and thirty samples measured parent draft-read p95 at11.662ms, final read at12.025ms against61.662ms budget, and new application at28.926ms against1000ms budget. Raw samples and machine details are retained beside this record. Parent deliberately asserts template route absence.

Independent source review covered authorization, transaction composition, P06 snapshot preservation and commercial PDF qualification. Root performed the final diff cleanup. The original combined body-refusal500 was not reproduced in the bounded diagnostic or final cohort; its cause remains unknown. The article pointer normalization hypothesis was disproved by a passing counterfactual and the unnecessary cast was removed. The earlier positive article failure was an incorrect fixture description, corrected without changing snapshot expectations. See [failure contract](../../p07-invoice-template-failures.md).

## Repeat

```sh
OPENERP_P07_READ_BASELINE_P95_MS=11.661957999999913 OPENERP_PERF_LABEL=corrected-integrated-head OPENERP_E2E_ARTIFACTS=test-results/product-P07-final bun run test:e2e apps/api/tests/invoice-templates.e2e.test.ts apps/api/tests/boundary-failures.e2e.test.ts apps/api/tests/invoice-template-performance.e2e.test.ts apps/api/tests/pdfcn.e2e.test.ts
bun run check:changed:full 7e9d89e
```

All fixtures were synthetic disposable local PostgreSQL/workerd/browser systems. Migration0063 was qualified locally, not applied to production.
