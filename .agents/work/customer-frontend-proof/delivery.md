# Desktop journey delivery

Status: active. The acceptance ledger in `docs/frontend.md` remains incomplete. Continue through its journeys without treating a completed route, API operation or build as whole-task completion. No test additions are authorized.

## Current unit: Sales

Build a unified customer invoice register with server-owned lifecycle state, URL search/status/sort/page, contextual record inspection, document-shaped editing and record-scoped review. Reuse the existing immutable draft and issuance operations. Do not infer legal issuance, delivery or payment from a rendered preview.

Failure contract chosen before implementation:

- An issued draft must appear once, as its registered invoice; it cannot remain an editable duplicate.
- Authorization must precede rows, search, counts and pagination. Every related record is scoped to the same book.
- Counts must describe the declared search/filter basis, never just a loaded page. Failed reads cannot become an empty register.
- Search, status, sorting and page survive opening/closing a detail, reload and browser back.
- Unknown totals remain unknown; exact money is never converted through floating point.
- Existing draft and invoice deep links continue to open the correct record and recovery controls.
- Saving preserves the existing source retention, immutable revisions and captured-request retry. Preview state cannot mutate accounting.
- Missing legal/provider facts remain explicit at the dependent action. They do not block unrelated UI implementation.

No full journey is accepted yet. The first Sales implementation and its observed paths are recorded below; continue the remaining Sales acceptance before moving to Banking.

Editor failure cases before implementation: totals must not treat blank tax as zero; quantity times unit price must stay exact in minor units (a fractional minor unit needs explicit correction, never silent rounding); an existing explicit line amount, discount and charge must survive editing; removing a row must remove its contribution; collapsed billing fields must remain in the submitted form; a save failure must retain the same entered facts and recovery key. A saved draft still needs the owning server review before issuance.


## Sales checkpoint — 23 September 2026

Implemented: one scoped server projection across current drafts and registered invoices; de-duplication by committed issue; six lifecycle filters and search-wide counts; search/sort/page/record/review in URL; contextual detail sheet; compact document editor with exact live line calculations and total beside the persistent Save button; shared saved-document preview; record-scoped review; successful demo issuance transitions straight to the registered invoice. The invoice read now owns its issue lineage, making document/cancellation controls reachable after reload. Existing identity, evidence, revision, idempotency and approval owners remain authoritative.

Observed in the real local application (web `127.0.0.1:3107`, API `127.0.0.1:18790`, PostgreSQL `frontend_20260923_ui2`, native desktop viewport 1950 × 1134):

- Open draft through the unified register; filter to Drafts and search Linden; open, reload, browser Back and close preserve the intended register and selected record.
- Existing 12,000 + 3,000 invoice: quantity 2 changes net to 24,000; clearing tax leaves tax and total unknown. Restore the original values.
- Add a second line at 2 × 100.25, tax 0: invoice total becomes 15,200.50. Change quantity to 0.5: no silent rounding of fractional minor units. Remove the row: total returns to 15,000.
- Complete local demo billing addresses, collapse both detail groups and save a revision. Saved document shows the entered address and the list removes Needs details. The entered addresses were synthetic local preview data.
- Prepare, approve and execute a separate explicitly zero-tax demo invoice through the visible controls, with the explicit demo receivables/sales mapping. Execution opens registered SYN-1. Reload preserves it and loads its original document and document/cancellation actions.
- Authoritative register after issue: All 2, Drafts 1, Outstanding 1, Overdue 1. The issued draft is absent; the single registered invoice has 950.00 SEK outstanding and due date 2026-09-15. Both general and status-filtered responses agree. An ungranted-book query returns 403 without rows/counts.
- Fixed the row-open failure where the router parsed the page number as a number. Row URLs now use the router serializer so numeric-looking search strings remain strings.

Evidence: local captures `.cache/customer-frontend/sales-register.png`, `invoice-editor.png`, `issued-invoice.png`; API results `.cache/customer-frontend/lifecycle-register-proof.json`; migration logs `sales-migration.log` and `origin-migration.log`. These captures show the real application with retained synthetic data, not live customer/company readiness. Source review is not rendered-reference acceptance.

Repeatable entry points:

- `/entities/entity_customer_demo/books/book_customer_demo/sales`
- Original editable draft: `invoice_draft_129205be69ad49809ea69531c6ceb27e`
- Demo issued register record: `invoice_40e45375ce85423fa68b38ae4c5b1a6c`
- Immutable issue review: `issue_review_619c449c79a94b55b4891605b38ed60c`, original draft `invoice_draft_ee5a19c549414de1a0fa3ce6cb878869`
- For an invoice detail add `?record=<id>&kind=invoice`; for a saved review use its original draft ID with `kind=draft&stage=review&review=<reviewId>`.
- Private preview runtime inputs remain in `.cache/customer-preview/runtime.json`; do not print or copy credentials into evidence.

Remaining Sales work (required, not optional polish):

1. Finish customer document generation/download and cancellation interactions; existing controls are reachable but retain technical form composition.
2. Make settlement/matching reachable from the invoice with context preserved; verify partial/settled/cancelled states after reload.
3. Exercise and improve interrupted/failed command recovery, editing conflicts and unsaved-close behavior. Generic commerce commands currently keep their retry key in mounted state and an explicit downloadable artifact; a reload-safe scoped recovery path remains needed. Command-containing record sheets now require explicit close, preventing accidental backdrop/Escape dismissal.
4. Inspect fuller/longer register content, sorting/pagination, empty/error states and affected shared controls. Clarify the register date basis for drafts versus issued invoices.
5. Perform the remaining visual/reference acceptance and overall customer interaction review before marking Sales accepted. Continue to Banking, Home/To do, Purchases, Books/Reports/period, Firm and integrated navigation in that order.

Production issuance, tax activation and external delivery remain unavailable. Those dependent operations do not block independent frontend work. No test files were added or modified.

Verification checkpoint: `bun run lint`, `bun run check-types` (including the web build/prerender), `bun run build` and `git diff --check` passed. Logs are under `.cache/customer-frontend/sales-final-lint.log`, `sales-final-types.log` and `sales-build.log`. These checks supplement the observed interactions above; they do not close the remaining journey criteria. The checkout is shared with other active work; preserve unrelated changes in database query/commerce transport, supplier duplicate migration and accounting-plan docs.
