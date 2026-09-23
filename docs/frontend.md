# Customer frontend plan

Status: working design and implementation record, 2026-09-23. The implementation section distinguishes delivered surfaces from the remaining customer application. [ADR 0006](adr/0006-customer-workspaces.md) records the choice. Accounting behavior and release gates remain owned by the [area plans](plans/README.md) and [open decisions](open-decisions.md).

**Customer UX delivery is incomplete.** Existing routes, forms and persisted operations establish capability coverage. They do not establish that the customer journeys below are finished. The journey acceptance ledger is the completion authority for this frontend work; the implementation inventory is not a completion checklist. Active execution and repeatable observations are recorded in [desktop journey delivery](../.agents/work/customer-frontend-proof/delivery.md).

Build one application around the work people need to finish. Founders start with decisions and business position. In-house finance starts with the work queue. Accountants working across clients start with a portfolio and enter the same company workspace. Every view opens the same evidence, revisions, approvals and receipts.

## Implementation status — 23 September 2026

The desktop application has scoped customer workspaces, source-led preparation and persisted coordination using the existing interface tokens and accounting contracts. Implementation, observed behavior and production readiness remain separate. Earlier observations are in [desktop workspace evidence](../.agents/work/customer-frontend-proof/desktop-workspaces.md); the continued journeys, checks and limitations are in [the continuation record](../.agents/work/customer-frontend-proof/continuation.md).

| Area | Implemented surface | Remaining boundary |
| --- | --- | --- |
| Company overview and work | One bounded attention projection for journal proposals, invoice drafts and expense reviews; matching counts, search, period/status/type/sort filters, scoped detail links and explicit coverage | Other domains retain their own workspaces. This feed does not establish company completeness, live cash or runway |
| Contacts and invoices | Unified server-filtered invoice register, contextual detail/review URLs, compact document editor with exact live totals and persistent save action, inline customer creation, immutable revisions and registered-invoice document lineage | No OCR or invented customer/legal facts. Production tax activation and external invoice delivery retain their domain gates |
| Documents and purchases | Original upload/search/preview/download; document-to-expense preparation with original beside entered facts; addressable expense detail, revision and review; stale review shown after source changes | Entered and reviewed amounts remain explicit. Unconfirmed currency in legacy records requires a choice; tax review does not imply tax eligibility or posting |
| Banking | Named account/period, statement upload, simple CSV format suggestions, editable mapping, balance/transaction preview, explicit approval/import, addressable statement detail, match discovery and reconciliation | Complex or ambiguous CSV uses explicit mapping. Account, signs, balances and completeness are never inferred. No live feed or payment initiation |
| Reports and period work | Report catalogue and snapshots, decimal trial balance/drilldown, invoice register reports, focused review-pack preparation, readable gap list, verified artifact bytes, readiness and technical closing | Saved report scope and currentness remain explicit. Advanced accounting controls retain their domain contracts; files and technical locks do not establish statutory acceptance |
| Coordination | Persisted personal/team filter views; record assignment to current book members with due date and note; revision checks and replay; removed members display as unavailable | These records grant no accounting authority. Client-request messaging is not implemented; firm relationships are persisted separately |
| Company directory and settings | Authorized books, period and attention summary, scoped entry/search; named book, currency, access, language, periods and chart in settings | Directory access is book membership. The separate firm workspace has explicit client links and team membership; production admission configuration remains D-01 |
| Firm clients and team | Persisted client links; responsible accountant, next review and shared note; search, assigned-to-me and review-due views; current period/work observations and work freshness; team add/change/remove and company drill-in | Firm membership confers no book access. Links require firm admin and book operator authority; existing handoffs require book operator authority. Actual production identities and provider configuration remain D-01 |

Registers, detail pages and bounded creation dialogs use the same company frame. Routine creation uses named choices and decimal currency amounts. Original documents, source references, immutable histories and technical receipts remain inspectable. Unknown mutation outcomes retain the captured request identity and recovery data; no optimistic financial success is shown.

FE-01–04 have integrated customer compositions but remain open for the journey acceptance below. FE-05 has persisted book-level views and handoffs, an authorized-book directory and a firm client/team workspace; its portfolio experience also remains open. Identity admission has explicit OIDC subject mapping and reviewed book grants. Actual provider configuration, company membership facts and release acceptance remain open boundaries. The legacy tools route stays available for existing specialist recovery consumers; deleting it before those paths are replaced would remove supported behavior.

This continuation added no test files. Desktop creation, revision, review, import, handoff and report journeys were observed against a synthetic local database. Lint, full type checks and build are recorded separately from those observations. Mobile, accessibility, theme and performance acceptance were not expanded or claimed.

## Journey acceptance ledger

Work through complete customer journeys in the order below. Shared frame and primitive repairs belong to the first journey that needs them, followed by an inspection of their other consumers. Do not replace these outcomes with route counts, API coverage or a list of components created.

| Journey | Observable finish condition | Current gap and state |
| --- | --- | --- |
| Sales register and invoice lifecycle | One invoice register exposes meaningful status views, search and sorting. Create, edit, review and inspect an invoice in its own context. Return to the same filtered register. Issuance and settlement status remain accurate after reload; actions appear at the record that needs them. | **In progress.** One server-owned register now combines drafts and registered invoices, with status counts, search, sort and pagination. Detail/review stays in context; document editing and a complete local demo issue/reload have been observed. Document creation/download and cancellation/reload have now been observed with local demo data; a retained approval request was recovered after a deliberately interrupted response and reload. Invoice-context payment selection, source review, partial and full matching, reload and exact retry after an interrupted confirmation are now observed locally. Undo now remains in the invoice context; release/reload, approval withdrawal, stale-review replacement and exact retry after an interrupted confirmation are observed locally, with the ledger unchanged. Draft close/reload/discard, interrupted source and final-save recovery, and explicit resolution of server revision conflicts are also observed locally. Longer lists, the downloadable document presentation, competing local-edit recovery and remaining failure/scope cases are still required before journey acceptance. |
| Account reconciliation | Start with named accounts and their period status. Open one account with statement balance, book balance, difference and unresolved transactions. Review a proposed or manual match beside its evidence, finish the supported operation, and return to the same account and period. Import and recovery are reachable within that flow. | **Incomplete.** Reconciliation, matching, coverage, allocation and imports are separate panels/tabs. There is no integrated account work surface. |
| Founder home and finance queue | The home separates decisions from resumable work without duplicating an item. The finance queue exposes the reason, amount, owner and next action. Opening, completing and returning from a record preserves context and updates the relevant work. Empty and incomplete-source states are distinct. | **Incomplete.** The same draft appears in both home sections; a raw ledger occupies the business summary area. Work coverage and queue-to-record continuity need an integrated review. |
| Documents and purchases | Open an original from the inbox, enter or correct its facts with the original visible, review the accounting effect, complete the supported operation and find its durable result from the source again. Preserve entered work on an error. | **Incomplete.** Upload, preparation and review exist; the complete source-to-result journey has not passed the current composition and interaction acceptance. |
| Books, reports and period work | Find a voucher, trace its evidence, make a supported correction and see the linked history. Drill from a report total to its records and return with scope intact. Period work names its blockers and leads directly to their resolution. Routine users do not need the legacy tools page to finish or recover. | **Incomplete.** Focused screens exist, but specialist recovery still depends on legacy tools and the complete report/record/period navigation has not passed acceptance. |
| Firm portfolio | Scan clients by period, outstanding work, responsibility and review date. Open a client's blocking work in the correct scope, hand it off, and return to the same filtered portfolio. Changes and access revocation remain correct after reload. | **Incomplete.** Client/team persistence and isolation have observations; the full accountant workday has not passed composition and interaction acceptance. |
| Integrated application | Finish the founder, finance and multi-client journeys through the ordinary navigation. Recheck affected shared controls and remove superseded entry points only after their operations and recovery are covered. | **Incomplete.** No integrated customer UX acceptance has been recorded. |

For each journey, select its concrete list, detail, editor and result states before changing code. Review page hierarchy, density, alignment, action placement and progressive disclosure against the accepted design. Preserve the existing fonts, colors, styling system and accounting authority. Match supported interactions without presenting unavailable domain operations as working.

### Invoice and record interaction direction

Use a document-shaped invoice editor: seller and customer blocks, dates, compact editable line items, payment terms and an immediately visible amount summary. Editing and preview share the same entered facts. Optional tax/source detail belongs beside the affected field or behind a clearly labelled disclosure. Do not make the ordinary invoice editor a sequence of unrelated accounting forms. Keep save state and the next available action visible, preserve edits after a failed save, and never claim an autosave until it has persisted.

Keep the invoice register in context when inspecting a record. At a useful desktop width, a detail panel can show customer, status, amount, dates, the document and activity without discarding the register's search, sort, filters or position. Opening a full editor or accounting review remains available when the task needs more space. Closing or returning restores the same register; direct links and reload resolve the same record. Apply this pattern to other record lists only where it helps the task, rather than forcing every workflow into a narrow panel.

Lead record details with the business object and its next action. Put technical receipts, identifiers and immutable history beneath the main summary in labelled detail sections. Invoice delivery, payment and posting states must come from their owning contracts. A polished preview does not imply that an invoice has been legally issued, delivered or paid. Keep unsupported actions explicit at the point of use without making internal implementation stages the main navigation.

The implementation owner must exercise the real browser controls and review the resulting screens before marking a journey verified. Record the revision, local environment, representative data, exact actions, observed results and useful screen captures. Include loading, empty, error and saved states where reachable, plus return navigation and reload. A source-only comparison leaves appearance unverified; a screenshot alone leaves the operation unverified. Use existing checks and manual browser verification within current authorization. This ledger does not authorize new test files or fixtures.

A journey may be **incomplete**, **implemented but unverified**, **verified**, or **blocked by a named external dependency**. Each unresolved finding keeps its owning journey open. A known layout or interaction mismatch cannot be reclassified as optional polish to close it. Passing lint, types or build cannot close a UX finding. An unavailable provider or company fact blocks only its dependent operation; continue the remaining frontend work and preserve the blocked operation in the ledger.

After a verified journey, advance to the next incomplete journey under the existing implementation request. A progress report is not whole-task completion. If execution is interrupted, retain the current finding, next action and still-valid evidence so continuation resumes implementation instead of restarting the plan. Declare frontend UX delivery complete only when every journey is verified and no required UI or recovery path remains unfinished. Production activation and broader release checks retain their separate gates; neither can substitute for this desktop UX acceptance.

## Design basis

Apply **better-layout**, **make-interfaces-feel-better** and **better-ui**, together with the repository's software-engineering guidance. Better-layout replaces taste at the user's request. Preserve StyleX, existing tokens, Inter/system fonts, Lucide, Base UI, TanStack Start/Router/Query and the owned table components. Do not introduce a second design system or animation dependency.

Build the customer interface around grouped company navigation, a to-do home, structured review, account reconciliation and a firm portfolio. Each screen must expose supported operations and make its data coverage clear.

| Surface | Customer purpose | Implementation boundary |
| --- | --- | --- |
| Company navigation | Familiar areas for bank accounts, sales, purchases, bookkeeping and reports | Expose a destination when its underlying workflow is available; omit unsupported payroll, payment or filing actions |
| Company home | Work first, with reasons and a useful next action | Incomplete sources and unavailable domains must remain visible, even when the queue is empty |
| Pending approvals | Structured proposals, evidence and review | Preserve immutable revisions, exact effects, distinct authority and receipt recovery |
| Reconciliation workspace | Account overview followed by a focused account flow; selection in the URL | Begin with supported statement imports and existing allocations; distinguish imported coverage from a live bank balance |
| Firm portfolio | Client overview, urgency and explicit drill-in | Persisted client links and firm membership intersect live book grants; period and work observations load for visible clients |

### What exists here

The [home route](../apps/web/src/routes/index.tsx) signs in and enters the only authorized book or shows the company directory. [BookWorkspace](../apps/web/src/components/book-workspace.tsx) owns the company frame. Addressable area routes load their selected domain; the prior [AccountingWorkspace](../apps/web/src/components/accounting-workspace.tsx) remains behind the tools route for advanced recovery consumers. Posting/recovery, corrections, source intake, reconciliation, reports, commerce, schedules and closing keep their owning contracts.

The owned [workspace](../packages/ui/src/components/workspace.tsx), [data grid](../packages/ui/src/components/data-grid.tsx), [buttons](../packages/ui/src/components/button.tsx), fields, tabs, disclosure, status, empty and loading components provide the base. The [router](../apps/web/src/router.tsx) already creates a request-scoped QueryClient. The [API client](../apps/web/src/lib/accounting-api.ts) already includes entity/book query keys and contract decoding. Extend these owners.

The customer composition now includes addressable journeys, a shared attention list, focused source review and audience-appropriate starting views. Production activation depends on actual identity inputs and acceptance evidence. Invoice registers are not invoice issuance or delivery; statement imports are not bank feeds; technical locks are not statutory year-end; source tax review is not a VAT return.

## One workspace, three starting views

| Audience | Default entry | First screen | Main actions | Details available |
| --- | --- | --- | --- | --- |
| Founder / owner | Overview | Up to five prioritized decisions, missing evidence, upcoming supported obligations; compact cash and receivable/payable summaries with source dates | Review a proposal, provide a receipt, inspect an overdue invoice, open an exception | Original evidence, accounting entries, approvals, audit and reports |
| In-house finance | To do | Dense, filterable work queue with status, source, amount, reason, period and next action | Prepare, review, reconcile, follow up, inspect completed work | Full accounting detail, registers, schedules, period readiness and recovery |
| Accountant with several clients | Clients | Client and period matrix: source coverage, reconciliation, review backlog, blockers and known deadlines | Open a client, find blocking work, prepare a handoff | The same company workspace, with explicit client/book/period scope |

Starting view and density are preferences. They confer no permission. An owner can use the detailed finance workspace; an internal accountant need not enter a firm cockpit. Production membership and action permissions remain D-01. Personal/team views and book-level handoffs now have persisted contracts. Firm/client relationships and team roles now have persisted contracts. Client-request messaging remains outside the implemented controls.

For the founder home, lead with the highest-impact unresolved decision, then the remaining work. Put business summaries alongside or below it; avoid a wall of equal KPI cards. Label the balance's source and date. Do not calculate runway without an explicit method and sufficient inputs, or imply that booked cash equals current spendable cash.

For finance, prioritize scan speed: stable columns, exact amounts, explicit exception reasons, persistent URL filters and keyboard access. Review is never accessible only through hover. Assignment and due-date columns appear only when authoritative data exists.

For firms, show each client's period and freshness in the row. Unknown coverage is visible. A portfolio summary is never authority to mutate multiple books. First delivery is read-only across clients, then a scoped drill-in for action. Cross-client bulk financial actions are outside this plan.

## Navigation and routes

The company frame has a company/book switcher, selected period, main navigation and a stable action area. Company identity remains visible during review and confirmation. Settings, account preferences and help are secondary. Assistance opens in the context of a record; it is optional to every core journey.

| Main destination | Customer purpose | Secondary destinations |
| --- | --- | --- |
| Overview | Understand position and decisions | Attention list, cash/source status, period progress |
| To do | Work through unresolved items | Review, missing evidence, exceptions, completed work |
| Banking | Inspect statement coverage and reconcile | Accounts, statement imports, matches and allocations |
| Sales | Track customer invoices and settlement | Customer register, invoice register and invoice detail |
| Purchases | Handle supplier documents and expenses | Document inbox, supplier invoice register, owner expenses |
| Books | Inspect and maintain the accounting | Vouchers, corrections, journals, schedules, assets, period readiness and locks |
| Reports | Understand and substantiate totals | Internal reports, drilldown and accountant review exports |

Use subnavigation inside each area instead of adding every domain to the main sidebar. Initially expose only usable children. Keep reasons for unavailable capabilities in setup/readiness or the relevant record; avoid a menu full of disabled future modules. VAT, payroll, invoice sending, payments and filing enter the navigation when their owning capabilities meet their gates.

Implemented route contract (record, period and filter state use validated search parameters where appropriate):

```text
/                                           sign-in or authorized book entry
/companies                                  authorized-book directory
/entities/$entityId/books/$bookId            to-do home
/entities/$entityId/books/$bookId/overview   founder overview
/entities/$entityId/books/$bookId/work       filtered work queue
/entities/$entityId/books/$bookId/reviews/$planId/$revision
/entities/$entityId/books/$bookId/accounts
/entities/$entityId/books/$bookId/sales
/entities/$entityId/books/$bookId/purchases
/entities/$entityId/books/$bookId/books
/entities/$entityId/books/$bookId/reports
/entities/$entityId/books/$bookId/tax
/entities/$entityId/books/$bookId/closing
/entities/$entityId/books/$bookId/settings
/entities/$entityId/books/$bookId/tools      retained advanced recovery tools
/intake                                    existing local statement preview
```

Detail destinations use the owning resource's identity and immutable revision where applicable. Period, filters, sort and pagination stay in validated search parameters. URLs carry no document contents, secrets or financial payloads. Server authorization resolves both scope IDs; neither a URL nor a preference grants access. The firm workspace uses `/firms?firm=<id>&tab=clients|team`; each client links into these same scoped company routes.

With one authorized book, entry can open its preferred view. With several, offer the last still-authorized context or a chooser. With none, show the actual setup/access state. Do not silently create a company or assume its legal profile. Preserve return destinations through sign-in only after validating them.

Navigation uses real links with current-page state, so reload, browser back, opening a new tab and shared links work. Changing company clears the selected record and book-specific selection, cancels old reads, and resolves an authorized destination. Never briefly paint the previous company's data under the new company's heading.

## Four layout templates

Use a small number of recurring page structures. Keep each product composition in `apps/web`; reuse primitives through `packages/ui`.

### 1. Overview

```text
Company / book                       Period       Account
Navigation   Overview                         [Review next]
             Most important decision          Source status
             Remaining attention items        Cash / obligations
             Period progress and blockers
```

The reading order is title and scope, urgent work, supporting position, then progress. Use one primary action. On a narrow container, supporting information follows the work list in DOM order. Keep explanatory text to a readable measure while lists use the available space.

### 2. Work list with an optional inspector

```text
Company / book                       Period
Navigation   To do                  Search / filters / view
             Item list                         Selected item
             Source | reason | amount          Summary / source
             Status | next action              Exact effect
                                               [Open full review]
```

The default list is useful without selecting a row. A selected record has an addressable destination. The inspector is a quick view; full review uses the same record presentation and owning operations. Preserve list filters and scroll on return. Avoid a three-column evidence/list/editor arrangement that leaves all three too narrow.

Use a split view only while both panes meet their minimum content measure. As an initial implementation constraint, budget about 32rem for the work list, 24rem for an inspector and 1.5rem between them. Validate that boundary with actual Swedish strings and source documents. Below it, open the record as a full-width detail view with a visible return link. Component adaptation depends on its container, not a device label.

### 3. Full record review

```text
Back to filtered list   Company / period   Proposal revision
Supplier / document / exact amount        Review status

Original evidence                         Proposed business effect
Page controls and download                Why this treatment
Source facts and conflicts                Accounting lines / blockers

History and durable outcome               [Specific permitted action]
```

On wide containers, evidence and effects sit alongside each other. On narrow containers, put the short decision summary first, then labelled Source and Accounting sections or tabs, with history below. A visible disclosure exposes hidden detail. A user can inspect all evidence before acting. Use the same record body for founder and finance views; vary the initial disclosure, not the approved content.

Keep the action area in normal flow or stable sticky chrome with reserved space and safe-area padding. It must survive long content, the software keyboard and 200% zoom. Do not pin an approval button over the last accounting line. A dialog is reserved for a bounded confirmation or secondary task, not the only way to reach the record.

### 4. Reconciliation and period work

Start reconciliation with an account/coverage table, then focus on one account and period. Show imported statement coverage, ledger amount, unmatched items and unexplained differences separately. A zero balance difference cannot hide missing or offsetting items. Keep the selected account and period in the URL. A match is previewed before applying it; partial allocations remain visible.

Period readiness is a checklist with an owner reason and links to blocking work. Current technical locks must be labelled as such. Reports show their period, snapshot/source basis and drilldown to lines, decisions and evidence. Keep internal, prepared, signed, submitted and accepted states distinct.

## Layout and visual rules

| Area | Implementation rule |
| --- | --- |
| Grouping | Use space first. Keep inter-group gaps at least twice intra-group gaps: existing 8px within a group and 16px or 24px between groups. Dense tables may use quiet structural separators. Avoid putting every field or row in a separate card. |
| Alignment | Share leading edges across title, toolbar, content and action area. Text aligns to the leading edge; amounts to the trailing edge. Use StyleX logical properties so spatial hierarchy mirrors under RTL. |
| Frame | Reuse the current 14rem sidebar and 16px/32px content gutters as starting tokens. Keep the existing collapse boundary until real content demonstrates a better one. Provide an accessible mobile navigation control whenever the sidebar is hidden. |
| Width | Dense registers may use the existing wide workspace. Constrain prose and forms within it. Keep evidence large enough to inspect, with explicit zoom/download controls instead of stretching the whole page. |
| Controls | Interactive controls have a shape, border, underline or consistent action zone. Prefer one primary action and at most two or three visible secondary actions; overflow uses a labelled menu when needed. Noninteractive statuses must not resemble buttons. |
| Narrow layouts | Wrap toolbar groups and labels. Use the existing grid's stacked presentation for simple work lists. Preserve columns and a labelled horizontal-scroll region for true debit/credit tables; include a visible cue to additional columns. No page-level horizontal overflow. |
| Targets | Preserve compact professional density while providing at least 40 by 40px desktop and 44 by 44px touch targets. Expanded hit areas cannot overlap adjacent actions. Keep content buttons inset, with safe-area padding around sticky controls. |
| Typography | Preserve the existing font system and root smoothing. Use tabular figures for money, dates where useful and changing counts. Balance short headings and use readable wrapping for explanations. Text containers grow; no fixed-height clipping or English-sized labels. |
| Values | Use shared exact-money contracts and locale formatting without lossy conversion to JavaScript numbers. Show currency explicitly when ambiguous. Distinguish accounting dates from timestamps. Never turn unavailable values into zero. |
| Surfaces | Reuse the neutral light/dark surfaces, restrained blue accent and semantic status colors. Preserve borders for structure, focus and selection; use existing layered shadows for elevation. Check contrast in both themes. |
| Corners | For tightly nested surfaces, outer radius equals inner radius plus inset. Preserve existing radius tokens for independent panels. Do not apply the formula to unrelated elements merely because one contains another. |
| Evidence | Preserve original page colors. Give rendered source images a 1px outline: `oklch(0 0 0 / 0.1)` in light mode and `oklch(1 0 0 / 0.1)` in dark mode. Do not invert scanned documents with the theme. |
| Icons | Use Lucide with `currentColor`; outline by default. Match 1.5px stroke to regular text and 2px to semibold contexts consistently. Correct optical padding only after inspection. Use labels for ambiguous actions. |

Swedish and English use the existing Paraglide flow. Implementation verification must include pseudo-localization and an RTL mirror; the latter is a layout stress check, not a claim of new language support. Test smallest and largest supported widths first, then around each observed collapse point. Keep DOM reading order aligned with visual priority.

### Motion and interaction

- Repeated navigation, tabs, row selection and keyboard traversal are instant, or use at most 150ms opacity/color feedback. Do not animate table reordering, counts or repeated page entrances.
- Keep the existing `scale(0.96)` button press. Add the prescribed `static` option for high-frequency controls where scaling distracts; reduced motion also removes it. Name transition properties explicitly.
- Avoid sliding/width animation on the finance workspace's tab indicator. The current shared indicator uses 250ms; decide the shared component's consumers before changing its default.
- Use CSS transitions for interruptible state changes. An infrequent contextual icon swap can use the skill's exact opacity 0 to 1, scale 0.25 to 1 and blur 4px to 0px with `cubic-bezier(0.2, 0, 0, 1)`. Routine queue actions need only static feedback.
- Suppress transitions for a theme swap, force reflow, then remove the temporary rule on the next frame. Preserve a system/light/dark preference without a flash of the wrong theme; actual theme-control behavior still needs implementation verification.
- Add `will-change` only after observing a first-frame problem. No broad GPU hints, animated background decoration or new motion library.
- A changed state always has a persistent label, icon or color cue. Announce important outcomes accessibly; motion and toasts never carry the only evidence of success.

## Review and state contracts

Each review presents: company/book and period; source identity and original evidence; proposed business effect; rule/fact basis and unresolved assumptions; exact accounting lines; immutable revision and dependency status; allowed action; approval history and durable outcome.

The default founder explanation answers what happened, the amount, the period and why attention is needed. Finance can open accounting lines immediately. Both approve the same immutable content. Edited content requires a new revision. The interface must not create a simplified substitute seal.

Preparing, approving, posting, paying and filing are distinct transitions. Buttons name the actual operation: for example, “Approve proposal” followed by “Post approved entries” where those are separate supported calls. Success appears only after the owning receipt. Rejection or correction explains the next available step. Do not add an all-purpose “Done” action that conflates these operations.

| State or failure | Required visible behavior |
| --- | --- |
| Loading | Stable layout, named loading region and disabled dependent action. No fabricated balances or counts. |
| Empty and complete | Explain what is empty and the coverage used to establish it; offer the next relevant action. |
| Empty with incomplete coverage | Show missing source/domain coverage. Never say the books are complete because no queue items loaded. |
| Partial read failure | Retain independently valid sections, mark failed sections and retry only affected reads. Summary completeness remains unknown. |
| Blocked / unsupported | Name missing evidence, capability or profile fact and link to the owning remedy. No misleading financial CTA. |
| Stale revision / changed dependency | Mark the proposal out of date, prevent consumption of stale authority and offer refreshed preparation for review. |
| Denied / revoked session | Remove unauthorized cached content, preserve safe return context and explain sign-in/access recovery. The server still enforces every operation. |
| Save failed | Keep the entered draft in memory and show retry/copy recovery. Durable draft saving appears only when a backing contract exists. Do not store evidence in localStorage. |
| Outcome unknown after a mutation | Keep the original operation identity and offer receipt lookup/recovery. A fresh idempotency key or blind new submission is not a remedy. |
| Partial multi-group completion | Show each group's status and receipt; recovery resumes eligible unfinished work without hiding committed groups. |
| Completed | Show the durable receipt, timestamp and affected records. The user can reload and find the outcome again. |

Bulk review comes after reliable single-record review. It requires a defined eligible set, explicit exclusions and exact group scope. Selecting “all” means a specified query/revision set, not just the visible rows. No optimistic financial success or frontend-only authorization.

## Data and ownership

| Owner | Responsibility |
| --- | --- |
| `apps/web/src/routes` | Scoped routes, validated search state, loaders, pending/error boundaries and navigation |
| `apps/web/src/components` | Customer page compositions and domain review sections; move existing panels incrementally into their destinations |
| `apps/web/src/lib/accounting-api.ts` and domain clients | Contract decoding, query options and existing mutation/recovery semantics; include scope, filters and revision/snapshot in keys |
| `packages/ui` | Workspace/link integration, owned Base UI overlays where first needed, buttons, tables and reusable visual primitives |
| `packages/contracts` | Any new work-list, capability, preference, membership or firm-summary wire shapes |
| `apps/api` and existing domain/SQL owners | Authoritative projections, scoped permissions, actual transitions, persisted assignments and durable outcomes |

Keep server state in TanStack Query. URL state owns navigable scope and filters; local component state owns transient disclosure, focus and unsaved edits. Do not add a general client store or feature-hook abstraction simply to relocate state. Keep existing lint rules and module ownership.

A cross-domain work list needs an owned read contract. Start with existing posting/review/recovery resources, then add domains incrementally. Each item needs a stable kind and source reference, scope, reason, state, exact amount when applicable, available action and detail destination. Return pagination and coverage/freshness explicitly. Counts and rows must describe the same filter and declared observation basis; do not sum overlapping domain items or treat a partially fetched page as a global total.

This projection describes work; the original domain retains approval and execution authority. Reuse each operation's existing input and result schemas. Do not invent a universal writable “task” that duplicates financial state. Workspace views and assignments are separate persisted records; they do not duplicate financial transitions. Client messaging remains a separate need; firm membership and client links have their own contracts. Assignment accepts a current member and a record in the same book, checks the expected revision and preserves command replay.

Performance follows the journey: load the selected domain, bound/paginate lists, cancel obsolete reads and lazy-load source previews and heavy reports. Avoid mounting and fetching every accounting panel at startup. Use existing table capabilities; introduce virtualization only if measured volume and rendering cost justify it. Capture timings and request counts on a representative dataset before claiming improvement.

## Migration map

| Current workspace section | Target home |
| --- | --- |
| Journal draft | Books > New journal, with review reachable from To do |
| Posting recovery | To do > In progress / recovery, plus the originating review detail |
| Posted records | Books > Vouchers, with receipt and evidence drilldown |
| Corrections | Voucher detail > Correct, retaining the linked history |
| Source intake | Purchases > Documents; bank statement intake also enters from Banking |
| Bank reconciliation | Banking > selected account and period |
| Internal reports | Reports |
| Accountant review | Reports > Review export and its lineage |
| Expense tax review | Source/proposal review > Tax treatment and blockers |
| Case snapshots | Record detail > Facts and decision history |
| Recurring preparation | Books > Recurring work and schedules |
| Bank allocations | Banking matching flow; linked from invoice settlement detail |
| Commerce | Sales and Purchases registers, reusing the existing operation owners |
| Owner register | Purchases > Owner expenses and funding |
| Subledgers | Books > Assets and schedules |
| Technical closing | Books > Period readiness and technical locks |
| Book readiness | Overview summary with a full checklist under Books |

During migration, retain a labelled route to remaining current tools for authorized users. Link old entry points to their moved destination where possible. Remove each old section only when its consumer, errors and recovery path work in the new destination. Delete the old all-sections composition once this map is covered; do not maintain two competing applications.

## Delivery sequence

These are frontend delivery slices, not replacements for the existing accounting work packets. The table defines the full acceptance target. Implementation status is recorded above; it is not implied by these exit criteria. Desktop UX was the priority for this continuation. Release evidence beyond that scope remains open.

| Slice | Deliverable and owner | Dependencies | Observable exit |
| --- | --- | --- | --- |
| FE-01: Review in the real frame | Web/UI: scoped navigation, real links, company/period context, existing journal preparation, immutable review, approval/posting and receipt recovery in focused routes | Existing auth/book list, posting and recovery contracts; D-01 still bounds production use | A permitted synthetic user prepares, reviews, posts and reloads a receipt through the new frame; back/deep links work; another book never leaks into the view |
| FE-02: Work list and founder home | Contracts/API/Web: bounded work projection, honest counts/coverage, queue filters and compact Overview | FE-01; posting/review projection first, supported sources added explicitly | The same item appears consistently in home, queue and detail; blocked/incomplete coverage remains visible; empty states make no false completeness claim |
| FE-03: Documents, banking and registers | Web/domain owners: evidence-led document review, account reconciliation flow, sales/purchase register detail and allocations | FE-01; relevant existing domain APIs, source-retention rules; FE-02 integration as each domain is added | A source can be traced through review to posting and settlement; unmatched/partial items remain visible; current invoice registers are accurately labelled |
| FE-04: Books, reports and period work | Web/domain owners: vouchers/corrections, schedules, reports with lineage, review exports, readiness and technical locks | Relevant accounting packets; FE-01 frame and FE-03 where records depend on source flow | A reported total drills to its evidence; corrections preserve history; readiness lists actual blockers; exports/locks do not imply statutory acceptance |
| FE-05: Team and firm work | Contracts/API/Web: persisted personal/team views, assignments/handoffs, firm client matrix and authorized company drill-in | D-01 actual membership mapping; owned firm/client and assignment contracts; reliable per-book summaries from FE-02/04 | A firm user sees only permitted clients, enters the right book/period, and can find an assigned item after reload; revoked access removes data |
| FE-06: Integrated release proof and removal | Web/UI/runtime: exercise full migrated journeys, reconcile accessibility/theme/layout/performance evidence and remove superseded composition | FE-01 through FE-05 for the release's promised audiences; applicable D-gates | Repeatable artifacts identify revision, environment and exact passed/failed scenarios; no hidden legacy-only recovery path remains |

FE-01 and FE-02 form the first customer-facing milestone. FE-03 and FE-04 progressively cover the current accounting tools. FE-05 completes the promised multi-client audience. Visual polish is part of every slice; FE-06 verifies integration rather than postponing accessibility to the end.

No reliable calendar estimate follows from route counts. FE-01 mostly reorganizes supported behavior; FE-02 and FE-05 introduce material read-model and identity work. VAT, payroll, bank feeds, invoice issuance/delivery and external filing remain domain projects with their own acceptance gates. Frontend completion does not establish those domain capabilities.

## Acceptance and verification

Choose the failure cases before implementing each slice. This documentation change adds no tests. Under AGENTS.md and D-09, adding or extending tests needs explicit authorization within the implementing task. Prefer approved E2E journeys with repeatable artifacts; do not write unit tests after implementation.

| Scenario | Evidence required for implementation acceptance |
| --- | --- |
| Founder decision | Start at Overview, inspect evidence and exact effects, finish the permitted transition, reload the durable outcome |
| Finance queue | Filter/sort, open a record by keyboard, return without losing context, process an exception and recover a lost mutation response without duplication |
| Firm isolation | Visit permitted and denied client URLs; switch company with outstanding reads; revoke access; verify scoped data and actions |
| Accounting integrity | Changed revision, locked period, missing source, partial allocation and partial multi-group completion produce the owning refusal/recovery state |
| Layout | Inspect 320px, 390px, 768px, 960px, 1280px, 1440px and 1920px plus either side of actual collapse boundaries; those are probes, not prescribed breakpoints |
| Accessibility | Real 200% browser zoom, keyboard-only navigation, visible focus, overlay focus restoration, status/error announcements, touch targets and reduced motion |
| Localization and themes | Swedish, English, pseudo-localized labels and RTL mirror; light, dark and system preference; long names/amounts, missing values and empty/failed/loading states |
| Performance | Representative list size, request count and interaction timings; no all-domain startup fetch, blocked input, repeated motion or unbounded document rendering |

Retain a run manifest with commit and dirty-tree identity, environment, synthetic data identity, commands, outcomes, screenshots and trace/receipt references. Include replay steps and failures; a screenshot alone does not prove posting or access control. Run repository lint, type and build checks appropriate to implementation, alongside the authorized journeys.

### Source inspection and remaining proof

Planning coverage includes the current route/composition and shared workspace, data grid, buttons, tabs, links and tokens. Typography has existing smoothing and tabular-number support; surfaces have owned light/dark and elevation tokens; motion inspection found existing press/reduced-motion handling and a 250ms tab indicator; icons use the installed Lucide base. Performance was assessed structurally, not timed.

Real links at the navigation boundary and optional static button feedback are implemented. Repeated queue and section controls use immediate state feedback. Compact creation dialogs, record summaries, source/effect columns and progressive disclosure are owned primitives. No new motion library or repeated page entrance animation was introduced.

Rejected changes: replacing the font/design system or application stack, animating recurring work-list entrances, giving every row a card, and treating a frontend audience selector as authorization. Each adds inconsistency or complexity without serving these workflows.

The earlier interactive audience sketches use fictional data and illustrate the proposed workflows. They do not verify the application. The continuation record documents observed desktop routes and workflows. Responsive layouts, actual 200% zoom, RTL, both themes, assistive behavior, slowed motion and measured performance are **Not verified** for this continuation. Full release acceptance remains open until its required evidence exists.
