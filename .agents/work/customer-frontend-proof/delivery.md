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

Document/cancellation failure cases before this pass: a document must be bound to the opened issue, including on reload; no preview/download before source identity, exact byte length and SHA-256 validation; a failed read must hide cached download controls; an interrupted render resumes its retained capture and does not reissue; a download stays HTML and is never labelled PDF or delivery. Cancellation must identify the opened invoice, show formatted reversal amounts and account names, preserve unresolved request identities, distinguish stale/expired approval from completion, and keep the cancelled invoice/document/history available after reload.

Reload recovery failure cases before implementation: persist the validated command and its original key before sending; isolate it by authenticated actor, book, endpoint and owning record in this browser tab; validate stored data before exposing a retry; never execute automatically on load; never rotate an unknown outcome's key; do not display new form values as the retained input; a storage read/write failure blocks a new send; a definitive server refusal can be explicitly replaced, while a timeout or malformed response cannot. Successful server history stays authoritative if a request's local cleanup fails. This step covers opted-in commerce actions; it does not claim recovery of unsaved draft edits or recovery after closing the tab.

Production issuance, tax activation and external delivery remain unavailable. Those dependent operations do not block independent frontend work. No test files were added or modified.

Verification checkpoint: `bun run lint`, `bun run check-types` (including the web build/prerender), `bun run build` and `git diff --check` passed. Logs are under `.cache/customer-frontend/sales-final-lint.log`, `sales-final-types.log` and `sales-build.log`. These checks supplement the observed interactions above; they do not close the remaining journey criteria. The checkout is shared with other active work; preserve unrelated changes in database query/commerce transport, supplier duplicate migration and accounting-plan docs.

## Sales document, cancellation and recovery checkpoint — 23 September 2026

Implemented: automatic identity/byte-length/SHA-256 validation before saved-document preview or download; concise Create/Download HTML controls; interrupted rendering can resume its retained capture; source metadata is behind disclosure. The existing retained HTML generator and its historical/demo boundaries are unchanged. A historical audit HTML download is not a polished legal invoice or PDF, and production delivery remains unresolved.

Cancellation now leads with invoice, exact formatted amount, cancellation date, reason and named reversal accounts. It defaults to the current open period/date while keeping both editable, restores the latest saved review from authoritative history, separates approval from final cancellation, and keeps completed/cancelled records and their documents inspectable. Request forms remain mounted when authority changes so an uncertain request can still be recovered. Completed actions do not leave rows of disabled primary buttons in the customer flow.

Opted-in issuance, document and cancellation commands now retain validated input plus their original idempotency key in session storage before sending. Recovery is scoped by server-returned actor ID, entity/book, endpoint and owning record. A reload exposes an explicit exact-request retry; no mutation runs automatically. Corrupt/unavailable recovery storage prevents a new request; timeout/unknown outcomes cannot be reset as a new action. Definitive server refusals may be explicitly replaced. This is recovery within the same browser tab, not a promise of unsaved-editor recovery or recovery after the tab closes. Other commerce forms have not yet been opted in.

Observed:

- SYN-1: created saved document `invoice_document_574fc4b53d8a496387deab8c8dd263b6`; automatically verified, previewed, downloaded and found again after reload. Downloaded 7,661 bytes and SHA-256 exactly match the retained artifact. Browser download-event observation timed out, but the actual file existed in Downloads and was checked against the API.
- Prepared cancellation, approved, reloaded and resumed the saved review, then cancelled through visible controls. Registered invoice and register show cancelled and zero outstanding after reload. The retained original document still has the same exact bytes. Cancellation ID `invoice_cancellation_1ecedea51f5d48a48ebf69ec33f59f7d`; reversal voucher `voucher_40015c93b847449dadbeb0de2ad3b17c`.
- Created a separate zero-tax demo draft for response-recovery observation. Prepared review `issue_review_601c341d74e646aaa868fe41d5192641` for draft `invoice_draft_4bd6c023849840528b272b5516e68db6`.
- A local loopback proxy forwarded approval, observed upstream HTTP 200, then intentionally replaced that one response with 502. The UI showed an unknown outcome. After reload, the retained request appeared; explicit retry used the **same key**, `2fda3fa7-5a2b-423a-9c17-5b0bbdfdceb9`, and received the original successful result. The proxy log contains both attempts. No automatic retry was sent on reload.
- Completed issuance after recovery. The next settlement work can use open demo invoice `invoice_277403429e514ac3ae4a4fd69c73606e` (SYN-2), 950.00 SEK, from that review.

Evidence: `.cache/customer-frontend/document-cancellation-proof.json`, repeatable read-only `.cache/customer-frontend/document-proof.ts`, `.cache/customer-frontend/recovery-proof.json`, `.cache/customer-frontend/recovery-wire.jsonl`, and `.cache/customer-frontend/cancellation-review.png`.

Preview continuity: web remains on 3107 and API on 18790. During recovery observation web proxies through loopback 18791 (`.cache/customer-frontend/recovery-proxy.ts`); its one-shot drop control is now null, so it passes responses through. It strips decoded transport headers correctly. Current Vite config `.cache/customer-frontend/vite.config.ts` uses a separate cache directory to avoid interference with other live previews in this shared checkout. CUA tab 9 stopped responding during a Vite module timeout; fresh task-owned tab 10 works and is marked for continuation. Do not disturb other previews/tabs.

Next required unit: invoice-to-settlement/matching with invoice context retained; observe partial and fully settled state after reload. Then finish editor conflict/unsaved-close behavior, remaining recovery failure/scope checks, search/sort/page/empty/error and longer-register review before accepting Sales. Banking and the remaining ledger journeys are still pending. No full journey is accepted by this checkpoint.

Final verification for this checkpoint: `bun run lint`, `bun run check-types` (all workspaces plus infra and existing API test type checks), `bun run build`, and `git diff --check` passed. An earlier full type check saw unfinished concurrent tax-account wiring; the final full check passed once those shared edits were complete. No test files were added or modified by this work. Logs: `sales-followup-lint.log`, `sales-followup-types.log`, `sales-followup-build.log` under `.cache/customer-frontend`.

The second invoice's document was also created through the new retained-request path. Download is now visible above the invoice paper; preview/verification disclosures share a compact toolbar. Latest real-app capture: `.cache/customer-frontend/invoice-document-actions.png` (the app's current 1600 × 900 desktop viewport). Current task tab 10 is on SYN-2's registered invoice detail. Preview process sessions at this checkpoint: web 16122, observation proxy 74756. Storage-corruption/denial and switched-actor cases remain to be exercised; they are not implied by the observed interrupted-approval success.

### Invoice payment matching — failure contract before implementation

The invoice view must not require pasted voucher, journal-line or invoice IDs. Payment discovery is a scoped read of current opposite-side control lines with remaining capacity, not proof of payer identity. The user must inspect the posted source and explain the match. Preparation, approval and application remain the existing accounting commands; no “mark paid” shortcut or new posting occurs.

Reject or visibly stop on wrong book/invoice/direction/currency bindings, stale invoice/payment capacity, corrected or reversed vouchers, locked payment periods, inactive accounts, cancelled/blocked invoices, missing sources and expired approvals. Keep decimal input exact. Show partial and fully matched balances only from refreshed authoritative reads. Never automatically resend a command after reload; retained prepare/approve/apply requests must retry the original key and input. A saved review must remain reachable after reload; matched and released history must not disappear when available payment capacity changes. Paginate discovery/history with scoped totals. Failure to load a fresh projection must not leave actionable cached choices. Closing the sheet must preserve register filters. Acceptance requires real-browser partial and final matching plus reload, and a retained verifiable result; this checkpoint does not accept the whole Sales journey.
