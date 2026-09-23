# Customer frontend continuation — 23 September 2026

Working implementation record. Desktop UX is the requested priority. No test files are authorized or added. Existing company/provider release gates remain independent.

Completed implementation phases so far:
- Direct invoice entry; automatic retention of entered facts; inline customer creation.
- Original document → expense creation, decimal amounts, immutable source reference, addressable detail and review.
- One scoped attention projection for journal proposals, invoice drafts and expense reviews, with matching counts, bounded pagination and URL filters.
- Named statement register/upload/preview flow, readable reconciliation amounts, named invoice issue accounts and periods.
- Addressable report registers and focused review-pack preparation.

Before adding workspace coordination, failure cases to preserve:
- A user cannot read another book's members, views or assignments through changed scope/record IDs.
- A saved personal view is visible only to its owner; a team view can only be authored by an operator in that book.
- Assignment accepts an existing record and current member in the same book. It grants no accounting authority.
- Removed membership must not be blocked by coordination data; stale assignees are labelled unavailable.
- A stale expected assignment revision cannot overwrite a newer handoff.
- Retrying the same request replays its result; reusing its key with another payload fails.
- Notes and filter state persist remotely; no financial payload or evidence is stored in browser preferences.
- List bounds are explicit; failure does not turn unknown assignment state into unassigned.

Persisted coordination, desktop creation/edit/review and queue transitions, statement import, report preparation and the integration pass are implemented. The maintained frontend plan is reconciled below. Production identity, legal tax activation and provider submission remain externally gated; no frontend implementation implies them.


## Final implementation and observed journeys

Local preview: `http://127.0.0.1:3107`, API `127.0.0.1:18790`, local PostgreSQL database `frontend_20260923_ui2`. The previous preview database was preserved. All observations use the synthetic **Northstar Studio · Demo** book (`entity_customer_demo` / `book_customer_demo`), SEK with two decimal places. Credentials are local ignored runtime data and are not included here.

The shared checkout also had concurrent domain work. The final source manifest identifies the actual files; a Git commit alone does not identify this run. No commit, push or deployment was performed by this frontend task. No test files were added or edited by this task.

| Journey | Observed result |
| --- | --- |
| Customer → invoice draft | Created Linden Design AB inside the invoice dialog; the customer was selected on return. Saved September design retainer with 12,000 net, 3,000 VAT and 15,000 SEK gross, including agreed totals. Entered facts were retained automatically. Missing billing details remained visible; the invoice was not issued. |
| Saved view | Saved personal view **Open work** and found it after reload. The first write exposed an ambiguous SQL variable; forward migration 2401 repaired it, and retrying the same captured request succeeded. |
| Assignment | Assigned the draft to Demo operator, due 2026-09-30, with a billing-address handoff note. Reopened the dialog after reload and saw the saved member, date and note. Forward migration 2402 repaired the initial SQL local-reference error without rewriting an applied migration. |
| Document → expense | Uploaded receipt-demo.txt, opened the original and prepared a 1,000 SEK expense (800 net, 200 tax) from that source. The saved detail retained the original beside the facts. |
| Expense review → source edit | Saved a review while leaving registration and accounting method unconfirmed. The attention read showed the expense in completed review work. Editing its description created a new source revision and restored **Needs review**; the older note is labelled as a previous review. |
| CSV → retained statement | Uploaded a two-row CSV, received editable Date/Description/Amount/Reference suggestions, selected the account/sign convention and explicitly supplied interval, balances and coverage. Preview showed -1,000 and +15,000 SEK, with closing balance 14,000. Approval/import succeeded and opened the saved statement. No ledger posting or payment was made. |
| Statement → possible matches | Opened the first row's **Find match** action. The result showed the named bank account, -1,000 original/remaining, zero allocated, and no posted entry in the selected account/interval. No candidate was auto-selected. Positive-candidate allocation was not exercised in this fixture. |
| Review pack | Created a January–December pack with explicit unverified opening explanation and accountant notes. It contained six account balances and zero journal lines. Review gaps retained missing/stale source issues. Sections and readable labels were inspected in the browser. |
| Review file | Clicked the complete JSON file's download action; the app fetched and verified the retained identity, byte count and SHA-256 and showed verification success. The browser download event timed out, so an operating-system saved file is **not verified**. |
| Invoice register report | Created a report at 2026-09-23 and opened its saved URL. It correctly reported no declared invoice control accounts; it did not turn that into “no invoices”. |

Manual API observations in [coordination-observations.json](coordination-observations.json) record stale handoff rejection, nonmember rejection, wrong-scope denial, identical-request replay, conflicting-payload rejection, and personal view create/remove. [expense-review-observation.json](expense-review-observation.json) records the completed expense attention read. These are observed responses, not an automated test suite or broad security proof.

## Repeatable inspection

Use the running local preview and the synthetic book. These IDs identify the retained records; they contain no production data:

- Invoice draft: `invoice_draft_129205be69ad49809ea69531c6ceb27e` (Invoicing → drafts).
- Receipt original: `source_dec6033c938942f79ee4631e6b84c3c8` (Purchases → documents).
- Expense: `taxsource_14025e4226ad4a25a9a43de3f83b36bf` (Purchases → expenses).
- Statement source: `source_a9efd8694f554376bc128487ed855b97` (Accounts → statement imports).
- Imported statement: `statement_2422dd03f87b470ea918f248db13b0e7` (Accounts, `view=bank&record=statement:<id>`).
- Review pack: `review_pack_41512d9362de4f89b1a169155819b8e9` (Reports, `view=export&record=<id>`).
- Invoice register report: `register_report_8fda82ee28244cf0ba92e5391b8a7f69` (Reports, `view=register&record=<id>`).

To replay the meaningful transitions, create a new invoice or expense through the same visible controls; do not reuse mutation keys with changed data. To inspect persistence without adding data, reload the saved draft, saved work view, assignment dialog, expense, statement and report URLs. No fixture/setup script needs to be rerun for inspection.

## Polish review

| Category | What was reviewed and changed | Evidence and limit |
| --- | --- | --- |
| Typography | Kept the owned font system; quiet labels and stronger record values; exact locale-formatted decimal amounts, named periods and shorter section headings. Removed incorrect “minor units” headings from decimal reports. | Desktop invoice, expense, bank and report screens inspected. Long-text localization and 200% zoom acceptance not claimed. |
| Surfaces | Registers stay flat with structural separators; record summaries share a leading edge; source and facts use owned two-column layouts; small secondary tasks use compact dialogs. Raw request/digest details are disclosures. | Desktop screenshot observations in the active browser, not persisted screenshot files. Light theme inspected; dark theme acceptance not claimed. |
| Animation | Retained existing press feedback and static options for repeated queue/section actions. No recurring entrance animation, width animation or new motion dependency added. | Code review and ordinary interaction only. No 10%-speed, interruption or reduced-motion acceptance run claimed. |
| Icons | Reused Lucide for create/back/refresh/download, paired with labels. No icon-only financial action added. | Inspected in registers, record headings and dialogs. |
| Performance | Reused scoped TanStack queries, lazy-selected domains and bounded projection/list contracts. Originals and candidate/report detail load when entered. No dependency or blanket virtualization added. | Structural review, lint/types/build and ordinary browser interaction. No timing or representative-load improvement claimed. |

| Before | Implemented result | Why it matters |
| --- | --- | --- |
| Journal-only work summary | Journal, invoice and expense attention share a bounded server projection | Home and work list report the same declared coverage |
| No persisted work views | Personal/team filters persist per authorized book | Finance can return to its work context |
| No handoff record | Member, date and note persist with revision checks | Assignment survives reload without granting accounting permission |
| Invoice required a manually created source note | Direct entry retains submitted facts automatically | A founder can create a draft in one flow |
| Customer setup interrupted invoice work | Compact inline customer dialog | New customer returns selected to the draft |
| Expense preparation separated from its source | Original beside decimal entry and review | Reviewer can compare facts with retained evidence |
| Legacy unknown currency implicitly problematic | Explicit currency/scale establishment before editing | The UI does not silently reinterpret unknown amounts |
| Old review could look current after source edit | Needs-review state plus previous-review label | A stale assessment is not presented as current |
| Unknown direct-save outcome had weak recovery | Captured request download and same-request retry | The entered operation remains recoverable |
| CSV required every format field manually | Conservative editable format/header suggestions | Simple imports take fewer steps without guessing financial meaning |
| Preview led with bytes and digests | Account, interval, balances and transactions lead | A person can review the actual import effect |
| Imported statement used internal IDs and minor units | Named account, decimal summary, row match actions and a stable URL | Imported records can be read and revisited |
| Match discovery exposed the technical comparison first | Transaction summary, exact money, clear result and scope disclosure | Empty or blocked matching is understandable |
| Reports mixed capture forms and retained records | Report registers, bounded dialogs and focused detail | Creation and inspection have distinct places |
| Review files were large hash cards and two-stage actions | Compact named files with verified one-click download request | The common action is clear while integrity checks remain |
| Review gaps were raw codes and long repeated messages | Readable control/reason labels, visible states, full explanation on demand | Accountants can scan gaps without losing the retained basis |

Rejected changes: replacing fonts/colors or adding a styling system; animating routine list and tab changes; making a card for every row; guessing sign convention, statement completeness or zero openings; treating the authorized-book directory as a real firm/client relationship. Each would introduce unnecessary inconsistency or unsupported meaning.

## Verification scope and remaining boundaries

The check results and source hashes are recorded in `final-verification.json`. Lint, full type checks and build are integration checks, not financial validation. No automated tests were added or run for this continuation. Existing test sources are included in the repository's type-check command; that is not an E2E run.

The concrete desktop flows above are implemented and locally observed. Production membership/revocation policy (D-01), actual company facts and source coverage (D-04), activated legal profiles and external acceptance remain external/domain gates. A true firm/client relationship model and client-request workflow are not represented by fake controls. Broad release checks for mobile, assistive behavior, themes, stress localization, performance, real-provider output and positive match allocation are not claimed. Advanced recovery routes are retained deliberately because they still have supported consumers.

Verdict: customer workflow implementation and focused desktop polish delivered; production release acceptance remains separate. This record does not claim complete accounting parity, statutory readiness, or that every future frontend acceptance criterion has been verified.
