# Desktop journey delivery

Status: active. The acceptance ledger in `docs/frontend.md` remains incomplete. Continue through its journeys without treating a completed route, API operation or build as whole-task completion. No test additions are authorized.

## Current focus: core daily workflows

The priority is unfinished customer screens and ordinary daily work. Banking and Home/To do now have an implemented first pass, recorded in the checkpoint below. Continue with contextual bank report/undo and the source-to-purchase workflow, then Books/Reports/period and Firm. Keep remaining Sales acceptance gaps visible; do not let unusual local-edit or recovery cases prevent progress on the core application.

## Sales baseline

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

Remaining Sales work (required, not optional polish; updated after the draft checkpoint below):

1. Finish payment discovery/history pagination with longer lists. The populated Sales register, date basis, page/search/empty/read-error recovery and record return are now observed; remaining sort/Back combinations belong to the final interaction pass.
2. The versioned demo invoice layout is implemented and its preview/download is observed, with original artifact bytes preserved. Include the document in the remaining visual/reference acceptance. The supported file is HTML; production legal issuance, PDF and delivery are not established.
3. Finish remaining failure/scope observations and recovery UX: storage denial/corruption, competing local editing sessions and switched actor; expired approval and multi-invoice undo. Ordinary draft close/reload/discard, two-stage save recovery and server revision conflict are now observed. A competing local session is prevented from overwriting storage, but its current generic storage message and retry-only path need a clearer recovery choice.
4. Perform the remaining visual/reference acceptance and overall customer interaction review before marking Sales accepted. The core-workflow priority above supersedes the earlier requirement to finish every Sales recovery case before starting Banking and Home.

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


## Invoice payment checkpoint — 23 September 2026

Implemented a scoped invoice payment projection, separate 25-row candidate/history pages and invoice-sheet payment workspace. Candidate rows name their posted voucher, date, description and available amount. Selecting a payment opens a focused form with its source, exact decimal amount and match rationale. Review names the invoice and shows the proposed amount, invoice remainder and unused payment remainder. Existing prepare/approve/apply commands remain the authority; each now uses the actor/book/record-scoped retained request mechanism. Saved reviews are URL-addressable and reachable from history. Invoice detail and register use consistent settled/partly settled language. No new posting or payment instruction was introduced by the matching UI.

Observed in the real application on port 3107, synthetic local book, 1600 × 900 viewport:

- Empty payment discovery explains which posted payments can appear. Two synthetic fixtures were posted through the existing evidence/journal/approval/execution APIs: 400 SEK (A 1) and 550 SEK (A 2). These are local synthetic data, not real payments.
- Open SYN-2 → Payments → choose A 1 → inspect retained source → enter 401 SEK: review is disabled with the balance-bound message. Enter 400 SEK, confirm the source and prepare. The saved review survives a full reload.
- Approve and confirm A 1. After reload, 400 SEK is matched, 550 SEK remains, A 1 appears in history and only A 2 remains available. Retained read: `payment-proof-partially_allocated.json`; capture: `invoice-partial-payment.png`.
- Choose A 2, inspect source, prepare and approve the remaining 550 SEK. Review shows both remaining amounts as zero. Capture: `invoice-payment-review.png`.
- The loopback observation proxy forwarded final apply successfully and hid that one response with HTTP 502. UI showed uncertain outcome. Reload showed server-settled state plus an explicit retained retry; no POST was sent automatically. Retrying reused key `db1a0f82-037f-4b0b-849c-bfd5f28af23e` and returned the original result. Exactly two matched history rows remain, totaling 950 SEK; outstanding is zero. Proxy control is null again.
- Close → filter Settled → search SYN-2 → open invoice → Payments → close: search, status, sort and page remain in the URL and the single matching register row remains. Registered invoice says Settled/Reglerad after reload.

Invoice: `invoice_277403429e514ac3ae4a4fd69c73606e`. Partial review: `allocation_959c2b5331244531af8d9776ca558393`. Final review: `allocation_12c992018eaa476eb3e1e55ede848c68`; receipt `allocation_receipt_deb6dbd75f7c4e0cb8c37e89cf455afa`. Each review opens with `stage=payments&allocation=<id>` alongside the invoice `record` and `kind=invoice`.

Evidence lives in `.cache/customer-frontend/`: `payment-fixtures.json`, `payment-proof-partially_allocated.json`, `payment-proof-allocated.json`, `recovery-wire.jsonl`, and the captures above plus `invoice-settled-payments.png`. `bun .cache/customer-frontend/payment-proof.ts` repeats the scoped reads and records current invoice, discovery, history and review receipts. It contains no credentials. Local migrations 4300 and forward repair 4301 are applied; 4301 separates pagination ordinal from journal ordinal and uses the unallocation table's actual key. Concurrent work committed 4300 during implementation, so its checked-in body was preserved and the correction is forward-only. The shared checkout may again include these changes in another task's commit; do not infer missing work from an empty diff.

Still not accepted: whole Sales journey, longer payment lists, switched-actor/storage-denial/corrupt retained requests, expired/stale match review, and invoice-context undo. The older undo route remains linked without claiming it is polished. Next implementation should start with that undo flow, then draft recovery/conflict/unsaved-close and the remaining Sales ledger items. No production identity facts were invented, no test files added, no full-journey completion claimed.

Final verification for the payment checkpoint: `bun run lint`, full `bun run check-types`, `bun run build`, and `git diff --check` passed after the final UI changes. Logs: `payments-lint.log`, `payments-types.log`, `payments-build.log` under `.cache/customer-frontend`. Earlier full type checks encountered unfinished concurrent report wiring; the final check passed. No test files were added or modified. Final captures were visually inspected, including the focused review with its primary action above the fold and the settled history with two readable rows.

### Invoice-context undo — failure contract before implementation

Undo must stay on the original invoice and match, preserve the filtered register, and bind every prepared review to that exact receipt and invoice. It releases the entire original allocation, including every invoice when a match was split; it must never suggest a partial release or refund. Show all affected invoice amounts and the refreshed payment balance before approval. Wrong scope, receipt, digest, currency or invoice binding is an error. A changed invoice, payment, period or authority must block fresh execution, while an uncertain retained request remains explicitly retryable with the original key. Approval expiry and withdrawal must not be treated as completed release. After release and reload, the original matching history stays visible as released, outstanding/payment capacity comes from refreshed reads, and the same receipt cannot be released again. No new ledger posting or payment is created. New prepare/approve/execute/revoke controls use existing commands and same-tab recovery. Verify release and reload in the browser, inspect stale/withdrawn review behavior, and retain API/visual proof.


## Invoice-context undo checkpoint — 23 September 2026

Implemented: undo preparation, review, approval, withdrawal and confirmation now stay inside the invoice sheet. Review names the invoice, shows the exact released amount, invoice balance before/after and available payment after undo; source and technical history are behind disclosure. Split allocations list every affected invoice. Copy explicitly distinguishes releasing the match from changing the original posting or refunding money. Saved reviews have a URL, stay reachable from matching history and use existing commands with record-scoped retained requests. The old Accounts entry point shares the same review component. Fresh scope/identity/digest checks and dependency status gate actions. A stale review offers a new review only while the original receipt remains active.

Observed in the real local application, synthetic book, 1600 × 900:

- SYN-2 → Payments → A 2 (550 SEK) → Undo. Preparation shows current outstanding zero; review shows 550 SEK becoming outstanding and available again. Prepared review `unallocation_9deafb773fab4c118012b6a41479a075`.
- Approved, withdrew approval with a reason, then approved again. Fixed the form reset so withdrawal returns directly to a fresh approval action; approval history remains visible.
- Confirmation succeeded upstream and its response was deliberately hidden by the loopback proxy. Reload showed the completed server state and explicit recovery. Retry reused key `7d1d715f-1f3f-4706-b45d-e20f75dc4f86`, received the original success and did not duplicate the release. No POST happened automatically on reload. Drop control is null again.
- After reload, A 2 remains in history as released, is available for 550 SEK, and SYN-2 has 400 SEK matched / 550 SEK outstanding. The entire ledger snapshot, including sequence 5 and account amounts, is unchanged before/after.
- A separate A 1 / 400 SEK undo review was prepared before the A 2 release. Its dependency status changed from current to stale. The browser displays the stale warning without approval/confirmation controls. Create a new review uses the current balance: 550 → 950 SEK, releasing 400 SEK. New review `unallocation_f6c8ed108ed9471985419ede530afb37` was left unapproved and unexecuted.
- Closing the sheet retains search SYN-2, Settled status, Newest sort and page 1. The filtered register correctly has no matching rows after the invoice becomes partly settled.

Evidence: `.cache/customer-frontend/invoice-undo-proof.json`, `undo-proof-before.json`, `undo-proof-after.json`, `recovery-wire.jsonl`; captures `invoice-undo-review.png`, `invoice-undo-complete.png`, `invoice-payment-after-undo.png`, `invoice-undo-stale.png`, `invoice-undo-refreshed.png`. Repeat the read-only inspection with `bun .cache/customer-frontend/undo-proof.ts current`; this preserves the earlier before/after evidence. No production transactions or test files were added.

Next implementation: draft save recovery, revision conflicts and unsaved-close. `EvidenceCommandForm` currently retains the draft's final command only in component state and keeps its input builder in a closure; the source operation has its own durable owner, but a reload loses the final draft request. `DraftEditor` and its parent dialogs have no dirty-close handling. Preserve entered facts, authoritative revision/digest checks and exact-request retries when addressing these gaps. The fuller register, downloadable invoice artifact, remaining failure observations and visual acceptance still prevent Sales acceptance. All later journeys remain open.


Final undo verification: `bun run lint`, full `bun run check-types` (including web build/prerender, infra and existing API test type checks), `bun run build`, and `git diff --check` passed. Logs: `undo-final-lint.log`, `undo-final-types.log`, `undo-final-build.log` in `.cache/customer-frontend`. The refreshed-review capture was visually inspected: named invoice, formatted balances, full effect and primary action are visible together. Removed unused compact-mode/copy branches after moving the owning review. No test files added. Current task tab 10 is at the filtered Sales register and retained for continuation; other tasks/previews remain untouched.

### Draft editing — failure contract before implementation

Retain authoring values, selected customer, line identities and original revision/digest under the authenticated actor and book. Unsaved editor data is local work, not a server-saved invoice. A close/navigation choice must preserve or explicitly discard those edits; unknown command outcomes cannot be discarded as a new request. Capture the source, exact form facts and original command key before any save request; reload exposes an explicit retry, never an automatic mutation. Persist the validated final command before sending it. A failed read/write of local storage must be visible and must prevent sending unretained work. Revision conflicts must keep the entered invoice and allow inspection of the latest saved revision; adopting that baseline is explicit and only follows a definitive refusal. Never merge invoice facts or change the expected digest silently. Source-operation recovery and the existing accounting commands remain authoritative. Verify unsaved close/reopen/reload, interrupted save/retry and concurrent revision conflict in the browser.


## Draft editing and recovery checkpoint — 23 September 2026

Implemented a scoped local editing session for new and existing invoices. It keeps the selected customer, entered fields, stable line identities and calculations, original invoice facts and revision basis. The close dialog offers keep editing, close and keep local edits, or explicitly discard unsaved edits. Browser Back uses the same choice. Local edits are labelled as unsaved; reopening restores them. Pending saves cannot be discarded as a new request. Before sending, the editor retains the exact source/form facts and command key; after source confirmation it retains the validated final command. Reload and reopening offer an explicit Continue saving action in the persistent footer. No mutation occurs on load. Local storage read/write failures stop sending; competing state is not silently overwritten. This is local browser recovery, not cross-device draft sync.

A definitive revision refusal keeps the entered invoice and offers the latest saved document for inspection. Continue with my changes updates only the expected revision/digest after explicit selection. Original invoice facts, including less-visible tax identity fields, remain separate; the user must press Save draft again. The persistent footer links to the conflict section. Existing accounting commands, immutable revision history and source retention remain authoritative. The older generic evidence form remains for other domains; invoice editing now has its own serializable two-stage save.

Observed in the real local application, 1600 × 900, synthetic demo data:

- Existing draft revision 3: changed title, terms, quantity and reason. Close and keep → full reload → reopen restored all fields and the calculated 27,000 SEK total. The server invoice stayed at its original 15,000 SEK until Save. Quantity was restored to 1 before saving.
- Final revision save succeeded upstream but its response was hidden. Reload/reopen displayed the captured request. Explicit retry reused key `f7fcc805-c017-4ae4-87f8-1b1afa195146`; the server remained at revision 4 before and after retry, with no duplicate revision. No automatic POST occurred on reload.
- Concurrent synthetic revision 5 changed title/terms while the editor held revision 4. Save refused; the UI retained the user's fields, displayed the latest document and allowed explicit continuation. A later focused check changed a seller tax field in concurrent revision 7. Continuing against revision 7 preserved the editor's original tax field and saved revision 8. Final original draft: `invoice_draft_129205be69ad49809ea69531c6ceb27e`, revision 8, title September design retainer, 30 days, 15,000 SEK, original seller tax ID null. The competing synthetic tax value was not silently merged.
- New invoice: title Workshop · lokalt utkast, customer Linden Design AB, Design workshop line, 100 SEK, explicit zero tax. Browser Back opened the close choice; Keep editing retained the form and restored its URL. Full reload restored the unsaved new invoice.
- Interrupted the source-retention stage before the draft command existed. Reload exposed explicit recovery; the same source key `195ded97-e3d3-40a9-823c-742f48c70bb2` resumed, then exactly one draft creation completed. New draft `invoice_draft_822bb3eea0654369b5bd4380b52a6858`, revision 1, 100 SEK. Missing address/date/tax-treatment details remain visible as draft blockers.
- Edited the new draft title, explicitly discarded, reopened: original title returned with no restored-edit banner. No server revision was created by discard. Pristine editor close returned directly to detail.

Evidence: `.cache/customer-frontend/draft-recovery-proof.json` consolidates request attempts, immutable revisions and final results; `draft-proof-before.json`, `draft-proof-after-hidden-response.json`, `draft-proof-after-retry.json`, `concurrent-draft-proof-6.json`, `draft-proof-final-conflict.json`, `draft-proof-new-recovered.json`. Repeat scoped reads with `bun .cache/customer-frontend/draft-proof.ts current [draftId]`. Captures: `draft-restored.png`, `draft-save-recovery.png`, `draft-conflict.png`, `draft-close-choice.png`. No test files were added.

During implementation, a non-canonical serialized record comparison produced a false local-storage conflict after updating the expected revision. Fixed by comparing decoded/canonical records. A development hot reload then held an older in-memory session; a fresh task tab read the retained state correctly and completed the save. Task tab 10 was closed after recovery; current task tab 11 (`draftVerifyTab`) is on the new saved draft and retained for continuation. The true competing-tab/storage-failure recovery UX remains a required follow-up, not a completed observation. Proxy drop control is null and preview ports are unchanged.

Next implementation unit: fuller Sales register, sort/page/empty/error interaction and clearer date basis, then customer invoice download presentation. Close remaining failure/recovery and rendered-reference gaps before accepting Sales. All later acceptance journeys remain open. The shared checkout may contain these changes in another task's commit; preserve unrelated work and do not infer missing changes from an empty diff.

Final checks for the draft checkpoint: `bun run lint`, full `bun run check-types`, `bun run build`, and `git diff --check` passed. Logs: `.cache/customer-frontend/draft-final-lint.log`, `draft-final-types.log`, `draft-final-build.log`. Removed a redundant recovery branch, unused session property and a one-line indirection after implementation. Browser captures of recovery and conflict were visually inspected; the recovery/Review changes action is in the persistent footer. No whole journey is accepted by this checkpoint.

### Register volume and invoice document presentation — failure contract before implementation

A long register must preserve status/search/sort/page through record inspection and Back; controls must remain reachable without scrolling through every row. An out-of-range page must offer a direct return to the first page instead of claiming there are no invoices. Draft update dates and issued invoice dates must be labelled honestly. Counts on a failed read must not look current. Outstanding amounts must remain distinct from original invoice totals.

A new document layout needs a new generator version. Previously captured/sealed documents and their exact bytes remain unchanged and downloadable. The new artifact must contain the full captured customer/seller, dates, lines, exact totals and terms in a readable invoice layout with a clear demo/nonlegal boundary. No live balance, later company data, external assets, scripts, payment instructions or delivery claims may be introduced. Escape source text, validate all immutable source bindings, retain the complete accounting provenance and reject oversize content rather than truncate. Generate and download through the existing capture/render/seal owner and verify retained bytes/hash in the browser.


## Register and invoice file checkpoint — 23 September 2026

The register now has pagination above and below long lists, distinct draft-save and invoice-date labels, a remaining amount for partly settled invoices, and a direct first-page action for out-of-range URLs. Failed reads hide counts and rows and expose retry. Invoice detail now also offers Refresh when its first read fails and does not display cached details after a failure. Normal loading no longer shows technical permission copy.

New invoice files use generator `openerp-synthetic-invoice-html-v2`, with seller/customer blocks, dates, line items, terms and exact totals. The full captured accounting record remains available in the file's disclosure. It is a self-contained English HTML demo document with no remote assets or scripts, not a legal invoice, PDF or delivery. Migration `5600-invoice-document-presentation.sql` permits the second version and returns both captures in history; it does not change previous captures or sealed bytes. The original renderer is retained for version 1. The UI can create the new file, preview/download it and inspect the earlier file separately.

Observed on the real local 1600 × 900 desktop application:

- Register populated with 54 additional synthetic drafts and eight named counterparties, including long names, Swedish text, missing details and varied amounts. Total 58 records, 56 drafts. Draft pages contain 50 and 6 disjoint rows. Page two → open draft → reload → close retains page two.
- Customer sorting returns Alva first; search for Nordic Circular returns seven matches with matching status counts. An unmatched search has zero counts and clear-filter recovery. Page 99 shows a direct return to page one and no impossible page counter. The outstanding row distinguishes original 950 SEK from 550 SEK remaining.
- One-shot local GET failures: register hides counts/rows and Retry reloads the 58 records; invoice first-read failure exposes Refresh, which restores SYN-2 and its document controls. The loopback proxy passed upstream reads through and hid only the selected responses; its control is null again. Proxy process session is now 77050 on port 18791.
- SYN-2 file created through browser controls: capture `invoice_document_1455087ed20448e58d2f64c055643f0c`, filename `invoice-SYN-2.html`, 12,791 bytes. The browser-downloaded file exactly matches retained bytes and SHA-256. Both generator outputs reproduce their sealed bytes exactly. Original version-1 capture `invoice_document_c9c6346171574ada99dfd31e93faff4c` remains 7,679 bytes with unchanged hash. Original/new file selection and both previews were observed.

Repeatable scoped read: `bun .cache/customer-frontend/register-document-proof.ts`; result `register-document-proof.json` includes register pages, document identities, hashes, render equivalence and downloaded-file equivalence. Captures: `register-volume.png`, `register-read-error.png`, `invoice-file-preview.png`. Synthetic fixture identities are in `register-fixtures.json`. These are local observations; no test files were added. The saved document and register were visually inspected; rendered upstream reference acceptance is still pending.

Current task-owned browser tab 11 remains on SYN-2. Web 3107 and API 18790 remain available; web uses the 18791 observation proxy. Other tasks share this checkout and may commit changes concurrently. Do not infer missing implementation from an empty diff.

Next required work: competing-local-edit recovery, then the remaining payment/scope observations and visual/reference pass. Sales is still in progress; Banking and all later journeys remain open. No whole journey is accepted by this checkpoint.

Final checks for this checkpoint: `bun run lint`, full `bun run check-types`, `bun run build`, and `git diff --check` passed. Logs: `.cache/customer-frontend/register-doc-final-lint.log`, `register-doc-final-types.log`, `register-doc-final-build.log`. The shared checkout contains unrelated active accounting changes; this task did not commit, deploy or modify test files.


## Banking, Home and voucher checkpoint — 23 September 2026

Implemented:

- A named bank-account register replaces the routine six-tab entry. The account workspace keeps date interval, transaction view, search, pagination and selected matching review in the URL. Statement and ledger balances state their dates; a difference is shown only for the same closing date. Transaction rows show signed decimal amounts, partial matching and remaining capacity.
- Matching opens from a bank transaction. The customer selects a posted entry, reviews the amount and reason, prepares, approves and confirms using the existing accounting owners. Saved reviews show both transaction descriptions, the amounts after that match and the retained statement evidence. Voucher links open the exact record in a sheet with a compact debit/credit table; source material and technical details are disclosed beneath it.
- Overview and To do separate overdue invoices, account matching and accounting/expense reviews from saved invoice drafts. Counts come from their domain reads. The overview replaces the raw ledger with dated bank-account balances and unpaid customer invoices. It does not present ledger balances as a live bank feed or infer revenue, runway or statutory readiness.

Observed in the local synthetic book through the browser:

1. Opened Business account, selected Customer receipt, chose the posted 550 SEK entry and completed prepare → approve → confirm.
2. Receipt remaining changed from 15,000 SEK to 14,450 SEK and its row showed Partly matched. Unmatched ledger entries decreased from two to one. This bank match does not change the separate invoice payment allocation.
3. Opened the saved matching review from account history and followed it to voucher A2. Browser Back returned to the same account, interval and review.
4. Opened the account from Overview: 1 January–23 September was retained, statement balance was 14,000 SEK, ledger balance 950 SEK and their difference −13,050 SEK. The overview showed one unpaid/overdue customer invoice and separate resumable drafts.

Repeatable inspection: use `/entities/entity_customer_demo/books/book_customer_demo/overview`; open Business account, then the saved matching history. Saved plan: `bankplan_8757faca55064a438a9325ad23b8afee`. Voucher: `voucher_4977835904664bcfaafa98215280c66b`. The mutation walkthrough used existing synthetic records only. No external payment, invoice delivery or production activation occurred.

Artifacts in `.cache/customer-frontend`: `bank-account-workspace.png`, `bank-match-completed.png`, `bank-voucher-detail.png`, `company-overview.png`. The screenshots are real app captures, not design mockups. Migration `6200-bank-workspace.sql` is applied to the isolated preview database and must remain immutable there. No new test files were added.

Remaining core work: multi-entry selection and contextual undo/report completion in accounts; document-to-purchase composition; complete report/record/period navigation; the firm's daily client-work flow. Home/work assignment and filtered return need an integrated pass. The existing specialist bank panels remain reachable, so this checkpoint does not claim complete bank, home or application acceptance. Production D-01 and D-04 remain open.

Further observations in this checkpoint: statement import opens from the selected account and closing its upload dialog preserves the account/date URL, with a return-to-account action. To do → overdue invoices opened the one overdue invoice register; selecting SYN-2 retained its overdue/due-date view and showed 400 SEK matched and 550 SEK outstanding. The bank matching operation did not mark that invoice paid. Posted-voucher inspection now uses one full-width debit/credit table and collapsible evidence instead of repeated headings and a narrow stacked review table.

Read-only snapshot: `bun .cache/customer-frontend/bank-home-observation.ts` refreshes `bank-home-observation.json` from the authorized local APIs. This supplements the browser walkthrough and does not replay mutations. Verification: `bun run lint`, `bun run check-types`, `bun run build`, and both staged/unstaged `git diff --check` passed. Logs: `banking-home-final-lint.log`, `banking-home-final-types.log`, `banking-home-build.log`. The shared checkout was committed by another task during this work; this task did not create a commit or push.


## Tax layout and everyday review — 23 September 2026

This pass addresses the tax and expense review screens. Short choices use an owned native radio control; variable source lists and the longer treatment list remain selects. VAT entry groups source/amounts and assessment side by side, accepts decimal currency amounts, and saves entered assessment evidence through the existing command owner. A new manual source may cite existing evidence through the optional references section; imported expense sources retain their identity and revision digests. Unknown eligibility is not inferred from imported amounts. Decimal fields use aligned tabular numerals. The expense original stays beside the scrolling review form.

VAT facts, VAT drafts and saved expense reviews have record URLs. Saved expense periods have a dedicated list and compact creation dialog. Revision selection is a visible list, and the current expense assessment is readable immediately after saving. VAT detail leads with totals and dates; draft calculations and unresolved controls share a row. Technical references remain available separately. No new tests, dependencies, commits or deployments were made by this pass.

Observed through the real local desktop application (Swedish, 1600 × 900):

- A manual synthetic VAT record saved decimal input `1000,00 + 250,00 = 1250,00` as exact minor values `100000`, `25000`, `125000`; its detail reopened after reload.
- A September synthetic VAT draft saved and opened its record URL. Unknown other boxes remained unknown and box 49 remained unavailable.
- The retained demo receipt was reviewed through the visible registration/method/profile/rounding choices. The source detail changed to Reviewed and retained revision 2.
- A September expense period review saved with one included synthetic source, `100000` total minor units and `20000` VAT minor units, displayed as 1,000.00 and 200.00 SEK.
- The current reviewed expense prefills and saves as a linked VAT fact; amounts, source identity, source/review digests and explicit unknown eligibility survive the command.

Repeatable read-only observation: `bun .cache/customer-frontend/tax-layout-observation.ts`, output `tax-layout-observation.json`. Screenshots: `tax-assessment-editor.png`, `tax-period-editor.png`, `tax-assessment-detail.png`, `tax-draft-detail.png`, `expense-assessment-editor.png`, `expense-period-review.png`. These are synthetic local observations, not production acceptance. The existing local preview lacked expense withdrawal, VAT lineage and snapshot-list overload migrations; the checked-in migrations were applied with receipts so current reads decode correctly. The general local migration sweep encountered a separate pre-existing subledger migration conflict; no migration source or receipt was rewritten.

Scope of layout/polish inspection: the desktop tax entry, saved fact/draft, expense review and saved-period journeys in React/StyleX. Inspected grouping, action placement, field density, selected states, numeric alignment, loading and saved states. Motion was not added; no animation timing review was needed. Mobile, RTL and 200% zoom were not verified in this implementation-focused pass. The wider frontend acceptance remains open; this pass does not establish full application parity or production company readiness.

Verification completed: `bun run lint`, `bun run check-types`, `bun run build`, and staged/unstaged `git diff --check` passed. Logs are `tax-polish-final-lint.log`, `tax-polish-final-types.log`, and `tax-polish-final-build.log`. The sticky original remained visible while the dates/reasoning portion scrolled; `expense-review-sticky-source.png` records that state. The selected saved draft correctly became stale after the later linked fact was added; its captured basis and unavailable box 49 remained unchanged.

Layout/polish decisions in this scope:

| Principle | Before | Implemented result |
| --- | --- | --- |
| Group related work | One long VAT field column, internal identifiers mixed with amounts | Source/amounts and assessment columns; dates grouped; optional references separate |
| Make short choices visible | Registration, method, profile and mode require opening menus | Native radio choices show the alternatives and selected state |
| Put the next action beside its context | Edit below the full VAT detail; create snapshot nested below expenses | Edit at the record heading; saved periods have their own page and creation dialog |
| Preserve useful context | Original scrolls out of expense review | Original remains beside dates and assessment while scrolling |
| Make amounts readable | VAT inputs require integer minor units; period totals display raw integers | Decimal entry, exact retained minor units, aligned tabular figures and currency-unit period totals |
| Flatten history | Nested revision disclosures and record-navigation chevrons | Visible revision selectors and ordinary record buttons with dedicated URLs |

Considered and rejected: turning the full expense treatment list into radio cards would crowd the review column; long source/treatment lists remain selects. Adding animation to every selection would add repeated visual noise; selected borders/backgrounds provide immediate feedback. Changing the global palette or typography was outside this pass.
