# Reusable invoice content templates

Working design and failure contract authored before implementation. Visual presentation stays with Paper.

CRM defaults remain independent. This owner retains a book-scoped, currency-qualified template with immutable named revisions, active/archive state, supported commercial rows, payment terms, title and customer-facing note. Actual seller/customer identity, dates, recipients and legal numbers are supplied by the owning draft workflow. Candidate A (independent template lifecycle composing existing draft transactions) was selected after independent review; whole-draft cloning would carry financial identity and coverage fields that do not belong to reusable defaults.

Create and apply use retained command receipts. Revision/archive check current revision/digest; apply selects the exact current active revision. A replay of an earlier committed apply succeeds even after archive, whereas a new selection refuses. Apply to an existing commercial draft requires expected revision/digest plus explicit replacement acknowledgement and cannot revise a sealed draft. Template origin is part of the immutable draft revision/digest, not merely a mutable pointer. Later ordinary edits preserve that origin without asserting continued equality to template content.

Before production code, public E2E expectations cover:

- Two deliberate applications produce distinct normal drafts; repeated same command produces one identical receipt, including after template archive.
- Two hours at 100000 minor units and the retained 25% policy produce net200000, tax50000, gross250000. Changing template price to150000 changes only later applications, yielding gross375000.
- Changed payload under one idempotency key and stale template/draft revisions refuse; refusals write no draft or ledger effects.
- Existing draft replacement requires acknowledgement, keeps selected parties/dates, and retains exact template provenance. An issued draft cannot be replaced.
- Foreign books, currency mismatch, unknown revision/digest and unauthorized writes refuse. No guessed recipient or legal number appears in a template.
- Unresolved tax treatment remains reviewable with unknown VAT/gross and cannot issue.
- Bounded list/archive/history survives earlier applied drafts. User note is copied and actually carried by the document renderer.
- Existing composer save/start/apply controls call the same scoped owner; applying over entered fields requires explicit replacement.

Migration0063 is reserved for the immutable template owner. Run `OPENERP_E2E_ARTIFACTS=test-results/product-P07 bun run test:e2e apps/api/tests/invoice-templates.e2e.test.ts`; retain public responses, source integrity and measured operation timings. No live provider, production migration or delivery.

Independent source review added two admission vectors before their correction: the ordinary agent's MCP catalog must expose the classified new-draft preparation operation, and that same agent must receive `Forbidden` when targeting an operator's existing draft. Existing replacement retains the normal draft owner's operator boundary. Template revisions containing stale or archived article selections must obey P06's new-selection checks; an existing template is not authority to fabricate a previous draft snapshot.

Performance uses five warmups and thirty measured trials through public HTTP. The portable probe compares the existing draft read on parent/head separately from new template application. It retains raw timings and literal expected totals; missing feature responses on the parent remain explicit.

P06 integration E2E requires a current scoped article for first application, refuses a fresh draft after article revision and archive, recovers an earlier committed apply receipt, and allows replacing the actual existing target while preserving its canonical historical selection and note. The original draft revision remains unchanged. These are public-boundary expectations authored before integration.

The integrated ten-test cohort retained seven passes and three failures at source inventory `a08745e3ce84dfaf16d6e2ccb5f03289e0c3bf4eb18abbe66d8eea57b2bdcd60`. Current article application exposed a native bigint/string mismatch in the catalog pointer query. Legal issue succeeded, but its PDF renderer incorrectly required source-document totals on a commercial draft. The canonical legal issue owner already distinguishes those calculation bases; the renderer must preserve exact calculated/issued line and total checks while retaining source-total checks for transcription. The oversized-body refusal returned HTTP500 rather than413; its cause remains under investigation.

The same stable cohort measured existing draft reads at p95 11.228ms against parent09cb6b6 at11.662ms, with a61.662ms budget. New template application p95 was32.510ms against1000ms. Five warmups and thirty measured samples were retained for both operations. This timing receipt does not qualify the failed admission/PDF/body behaviors.

The bounded body-only diagnostic passed unchanged admission code, including HTTP413, in4.68s at stable source `5007765147f00746d678d7f9e3e2e73aafc22f7700e02d3593509d0d814e82fd`. The original combined HTTP500 was not reproduced and remains unexplained. The assertion now retains the safe response body when status disagrees; no limit, timeout, or expectation was changed.

The current article revision also owns its unit. A reference with the retained code/revision/digest and price but an altered unit must refuse fresh application. This public failure expectation was added before any unit-admission correction.

The bounded article check confirmed that the existing snapshot guard already refuses an altered unit. It then exposed a fixture mismatch: the selected article description differed from the template line description, which the owning calculator correctly rejects. The positive fixture now uses the exact retained description. No unit guard was added or weakened. SQL text normalization still makes the declared catalog pointer type explicit.

The source hypothesis that the catalog pointer native bigint needed text normalization was disproved by a bounded counterfactual. The full article lifecycle case passed with the original pointer query and corrected retained-description fixture in7.11s. The unnecessary SQL cast was removed. The observed positive failure was the fixture description mismatch, while the existing price/unit/reference safeguards remained intact.
