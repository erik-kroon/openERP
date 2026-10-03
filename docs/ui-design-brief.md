# OpenERP interface design brief

Purpose: give Paper design work one clear product brief before visual exploration begins. OpenERP is an Accounted-derived product, so Accounted is the starting product and interaction reference for this work, not an unrelated competitor. This brief describes the user-facing product OpenERP needs to become; it is not a claim that every route or capability is complete today.

Owner direction, 2026-10-01: design how OpenERP should look, function and flow. Accounted is the visual and workflow baseline. Current OpenERP UI and all OpenERP application screenshots, including archived engineering captures, are excluded as design references. Current source completeness is not a design ceiling. Follow the [working prompt](ui-design-prompt.md) and [screen checklist](ui-design-checklist.md); existing Paper frames remain drafts until carefully reviewed.

Later owner steering, 2026-10-01: keep Accounted's sensible approaches without changing them for novelty. Narrow/mobile design is deferred for now. This iteration reviews desktop design and records the deferred scope explicitly; eventual narrow usability and runtime accessibility requirements remain.

## Adopted focus — 2026-10-03

[ADR 0017](adr/0017-bureau-first-product-focus.md) governs the commercial sequence and role split. The bureau is the primary customer: accountants own routine bookkeeping within granted authority; owners approve payments and answer questions. First design the incoming-document, bank-match, invoice and VAT loop, with bureau assignment and exceptions as core work. Keep the owner-operated route.

Att göra is the single source of pending human work. Questions, review, bank missing-evidence, VAT/closing checklists and email are filtered views of the same tasks. Use bounded bulk approval for familiar supported bookkeeping, individual review for exceptions and explicit exact-action approval for payments, messages and filings. Keep technical seals secondary without weakening immutable effects or recovery. No automatic posting is adopted.

Design connected execution after approval: bank feeds, Peppol, VAT filing and BankID, with clear consent and separate submitted/accepted/paid/unknown states. Show assistant rationale and source basis; show learning only for actual authorized rule changes with undo. Onboarding and the adopted synthetic demo/tour reach bank → document → matched proposal before detailed policy. Native payroll is deferred for specialist integration evaluation; Cash and peripheral commercial surfaces follow the core loop. The wider page map below is retained inventory, not first-release navigation or delivery order. Use the new checklist adoption backlog.

## Product in one sentence

OpenERP helps an owner or finance professional turn retained source documents and financial activity into reviewed accounting decisions, reconciled books, and outputs they can trace and trust.

The interface should feel like a calm, capable financial workbench: it brings the next important decision forward, keeps its evidence close, and makes the current state and next safe action clear. It is not a generic ERP dashboard, a spreadsheet skin, or a chat-first AI product.

## Who it serves

- **Owner / founder:** wants to know what needs attention, what the business position is based on, and what decision is needed next.
- **In-house finance / bookkeeper:** wants to move quickly through a dense queue, review exact details, reconcile accounts, and recover unfinished work.
- **Accountant with multiple clients:** wants to spot client-level blockers and deadlines, open the right company and period, then work in that company's normal workspace.
- **Agent or automation:** may prepare scoped, explainable proposals. It does not become the decision-maker or gain authority from a user preference.

These are different starting points into one product, not separate applications. People share the same records, evidence, review history, permissions, and results. A user's role or selected view changes presentation, never accounting authority. When comparing with Accounted, start from the same user job and flow, then preserve familiar behavior unless OpenERP's explicit scope, data model, or workflow calls for a deliberate difference.

## What the product should help someone do

1. See the company, book, period, and source coverage currently in view.
2. Find the next actionable decision, its reason, owner when known, amount when relevant, and due date when supported.
3. Open the original evidence and compare it with interpreted facts and the proposed accounting effect.
4. Review and approve a specific immutable version; understand when a change makes it stale.
5. Complete the intended operation through a clear review and execution flow, then find its durable result and history again. Record missing implementation separately from the target design.
6. Reconcile both the account totals and the underlying transaction coverage; investigate differences rather than hiding them.
7. Trace report totals and posted entries back to decisions and evidence.
8. Return to the same company, period, record, and filtered work after navigation or reload.
9. Find an invoice, voucher, or retained document from one search scoped to the active company and book, with its match reason and access limits clear.

## Information architecture

```text
OpenERP
├── Entry / authorized companies
├── Firm portfolio (for multi-client work)
└── Company workspace (one entity + book at a time)
    ├── To do                 work queue and resumable decisions
    ├── Overview              business position and period progress
    ├── Banking               accounts, imported statements, matching
    ├── Sales                  customers, invoices, settlement
    ├── Purchases              documents, supplier invoices, expenses
    ├── Bookkeeping            vouchers, corrections, schedules, readiness
    ├── Tax                    VAT review, approval and qualified filing
    ├── Reports                saved reports, drilldown, review outputs
    ├── Year-end               period assessment and handoff
    └── Settings               book configuration and access
```

Keep navigation task-based and shallow. Use subnavigation within an area. Design active intended workflows even when their current implementation is missing; put that dependency in the design ledger, not in a sidebar of disabled future modules. Genuine permission, missing-fact and external-service conditions still need clear states. Advanced recovery tools remain reachable for their users, but should not define the everyday product.

## Page design map

For every page, Paper should explore the useful working state first, then the relevant empty, incomplete, blocked, loading, error, and completed states. The "see" and "do" lists describe intended user needs, not promises that every item is currently available.

| Page / area | What the user needs to see | What the user needs to do |
| --- | --- | --- |
| **Entry and sign-in** (`/`) | Sign-in or the user's authorized destination; clear company access state if no book is available. | Sign in, continue to an authorized book, or choose a company. Never imply a company was silently created. |
| **Companies** (`/companies`) | Authorized books with enough identity and period context to choose the right one. Distinguish no access from loading or failure. | Open a book, switch context, or follow the real access/setup path. |
| **To do / work queue** (`/entities/:entity/books/:book` and `/work`) | Prioritized unresolved work, grouped by meaningful reason and state. Each item shows its source, period, amount when applicable, blocker/next action, and freshness/coverage context. Prepared, blocked, completed, and empty-with-incomplete-coverage must not collapse into one state. | Filter/search/sort, open a review, resume work, follow missing-evidence paths, and return without losing queue context. |
| **Overview** (`/overview`) | The most important unresolved decision first; a small, dated, source-labelled view of cash/receivables/payables where available; period progress and named blockers. Where supported, show attention by kind/reason, exact overdue residual by currency, qualified upcoming obligations, and the dated minimum from a retained forecast. Every value needs its own coverage/cutoff and a direct route to its full source population. No decorative wall of interchangeable KPI cards. | Start the next useful task, inspect a supported summary, or open the same filtered queue, invoice register, obligation, or forecast that explains a figure. Unknown residuals and incomplete coverage remain visible; an empty queue never means the books are complete. |
| **Review detail** (`/reviews/:plan/:revision`) | Company/book and period; source identity and original; interpreted facts and conflicts; proposed treatment, exact accounting effects, warnings, revision/dependency status, allowed action, history, and durable outcome. A person must be able to inspect evidence before acting. | Review, request a supported change/new revision, approve the exact version, execute only the separately supported operation, or recover its receipt. |
| **Banking / accounts** (`/accounts`) | Named accounts and selected period; statement coverage, ledger balance, statement balance, difference, unmatched items, and import freshness shown as separate facts. Imported data is not a live bank balance. | Choose an account/period, import a supported statement, inspect transactions, review a proposed/manual match, allocate, and reconcile supported items. |
| **Cash forecast** (addressable Cash view within Overview) | Dated contributions, stated opening observation, coverage and cutoff, included and excluded items, and any gaps in the qualified basis. Show both baseline and conservative same-day ordering where available, plus minimum date/amount and headroom; assumptions remain distinct from observed or booked facts. | Inspect each contribution, adjust a scenario without changing source records, compare its retained result, and return to the overview or source record with context intact. The forecast is read-only and never promises spendable funds or initiates payment. |
| **Sales** (`/sales`) | Customer and invoice registers with useful status, search, sort, amount, dates, and settlement state. Draft, registered, delivered, paid, and posted are distinct states. | Design invoice composition, issuance, delivery, settlement and correction flows. Show when customer terms, currency, language, recipient reference, or article values are copied into new work; expose source/revision and qualification. Unqualified tax inputs cannot authorize a tax treatment, and an unverified recipient reference cannot authorize sending. Later master-data changes never rewrite saved work; replacing values in an existing draft requires an explicit choice. A reusable **content** template copies supported commercial rows, terms and a customer-facing note into a new draft; amounts are recalculated under invoice rules. Keep it distinct from document-layout settings, which control presentation. A recurring schedule creates a draft for a person to review and issue. Reminder review shows the exact recipient/message and separates approval, dispatch, evidenced delivery and recorded outcome; an unknown attempt needs investigation before retry. Inspect the document and history, then return to the same register context. Show the evidence behind each outcome; annotate missing implementation separately. |
| **Purchases and documents** (`/purchases`, `/arkiv`) | Source documents, supplier invoices, and expense work with original beside entered facts when reviewing. Mark manual/entered facts as such; show missing or conflicting evidence. Document search can filter reviewed supplier/date/currency/amount/link facts and labels their source; arbitrary OCR text is outside the initial search scope. | Add or inspect an original, prepare/correct a draft, review a supported treatment, and follow its result back from the source. Make each document occurrence's question and next task clear through intake, supplier-draft preparation, and acceptance review. A source tax review is not itself a filing or posting. |
| **Bookkeeping** (`/books`) | Posted vouchers and their source/review lineage; correction history; relevant schedules and period readiness. Put business meaning before technical IDs. | Find a voucher, trace evidence, start a supported correction, inspect schedules, and resolve a named period blocker. Posted history is never silently edited. |
| **Tax** (`/tax`) | Supported tax/VAT review with source population, included/excluded items, calculations, control differences, evidence, and currentness. Unknown applicability or coverage remains explicit. | Inspect a supported calculation, prepare/review an artifact where available, and follow control discrepancies to their owner. Never present prepared as filed, assessed, paid, or accepted. |
| **Reports** (`/reports`) | Searchable report catalogue, selected period/snapshot, source basis and currentness. Totals need a path to accounts, vouchers, decisions, and evidence. | Open or prepare a supported report/review pack, drill into the underlying lines, export available artifacts, and return with report scope intact. |
| **Year-end / closing** (`/closing`) | A period checklist with known coverage, explicit applicability, owner-reasoned blockers, review date, and links to work. Technical lock and statutory completion are visibly different. | Assess supported areas, resolve blockers, prepare the available handoff, and inspect the resulting version. Do not imply filing or acceptance. |
| **Settings** (`/settings`) | Book identity, currency, access, language, accounting periods, chart, and configured choices, with unknown/unverified facts not dressed up as defaults. | Design the intended configuration and access flows with appropriate authority, validation, save, cancel and recovery behavior. |
| **Firm portfolio** (`/firms`) | Client list/matrix with relevant period, work count, freshness, responsible person, review timing, and explicit unknown coverage. One client's status must not imply another's. | Search/filter clients, assign or hand off within supported permissions, open one client in its scoped workspace, and return to the same portfolio filters. Portfolio scanning is not cross-book financial authority. |
| **Advanced tools / recovery** (`/tools`) | Clearly named specialist operations and their context, current status, and recovery steps. Do not expose implementation jargon as the ordinary navigation model. | Reach existing specialist recovery and technical flows without losing their source record or scope. Keep until everyday destinations cover the same operations and recovery. |
| **Local intake preview** (`/intake`) | Clear statement-import preview, source identity, mapping, validation and the distinction between preview and retained import. | Design source selection, preview, correction, import review and durable result with a clear continuation into the book. |

## Shared frame and interaction rules

- Keep company/book identity and selected period visible through lists, review, approval, and result. A company switch clears old scoped content before showing the new one.
- Use real navigation and addressable records. URL state carries the navigable scope, period, filters, sorting, page, and selected record; it never grants access.
- Preserve search, filters, pagination, and position on return. Deep links and reload must resolve to the same authorized object.
- Provide one visible, book-scoped search across invoices, vouchers, and retained documents. Explain why each result matched, limit results to the active authority, clear old results on a book change, and let the user return to the same result set after opening a record.
- Prefer a useful list with an optional inspector on wide layouts. On narrow layouts, open a full-width detail instead of squeezing list, source, and editor into unusable columns.
- Reuse a few page patterns: overview, filtered register/queue, full record review, and account/period reconciliation. Don't force every domain into the same card dashboard.
- Keep the original legible and unaltered. Show exact amounts with explicit currency, dates with clear meaning, and money aligned for scanning.
- Keep technical identifiers and receipts available but secondary to the object's name, amount, state, and next action.
- Use specific action labels. Preparing, approving, posting, paying, submitting, and acceptance are not synonyms. Show success only after the owning durable result exists.
- Keep the interface useful at desktop and narrow widths, keyboard operable, readable at 200% zoom, localized, and coherent in light/dark themes. Do not rely on color, hover, animation, or a toast alone to convey state.

## Visual direction for Paper exploration

Start with a professional, editorially calm financial workspace: clear typography, precise alignment, confident whitespace, restrained color, and enough density for real registers. Use hierarchy and grouping instead of putting every datum in a card. Make evidence and accounting effects feel like parts of one review, not separate apps.

Use the retained Paper brand foundations and OpenERP token vocabulary as the starting visual language. Refine composition, hierarchy and component treatments for the intended product; do not copy the current application layout or let existing component APIs limit design. StyleX remains the eventual implementation system. A distinctive brand expression is welcome if it stays quiet around financial data. Avoid generic SaaS gradients, oversized KPI tiles, decorative charts without a decision behind them, and chat as the primary navigation. Preserve familiar Accounted behavior when it helps the user, and improve it where there is a clear reason.

Use Accounted to ground design in the actual product: inspect the corresponding screen, its interaction and neighboring steps. Decide what to **keep**, **improve** or **remove** for the intended experience, and explain why. Maintained accounting invariants and explicit product boundaries still apply. Missing current OpenERP implementation is a delivery dependency, not a reason to omit the intended design.

### Reference and screen-by-screen method

The source inventory contains 129 Accounted route templates and 21 OpenERP URLs. Use it to avoid losing secondary workflows, not to produce 150 interchangeable frames. The [screen checklist](ui-design-checklist.md) maps every source route to a target screen or explicit disposition and includes intended flows beyond current routes.

For the next screen in the adoption backlog, then the applicable unchecked inventory item, inspect its actual Accounted working state and relevant interactions with safe synthetic/demo data. Inspect source only to resolve ambiguity. If a record or token is unavailable, record that reference limitation and design the intended flow using labelled synthetic content. An unavailable capture is not automatically a design blocker.

Explain the job and hierarchy before drawing. Build one desktop screen carefully, inspect its Paper screenshot, critique and refine it, then complete the narrow layout, meaningful states and control destinations. Record design decisions before moving on. Do not batch whole product areas or count a frame as finished just because it exists.

Use only Accounted application captures as visual references. Do not capture, open or import current OpenERP application screenshots for this work. The [route capture index](ui-route-capture-index.md) is a historical inventory record; its old OpenERP capture claims are not a visual design basis.

## Product truth and guardrails

- Unknown is not zero; an empty list is not proof of complete books. Show the basis and gaps behind summaries.
- Preserve the distinction between source evidence, entered facts, proposed treatment, approval, posted result, and external outcome.
- Do not invent company identity, tax/accounting profile, registrations, deadlines, balances, or provider connectivity.
- Cash, when designed, is a dated and explainable read-only forecast. It does not initiate a payment or promise spendable funds.
- Access, approval, and execution are enforced by the owning backend contracts. Presentation preferences, firm membership, and assignments do not create book authority.
- Design intended operations as active in synthetic target states. Show genuine authority, missing-fact and service conditions honestly. Annotate absent implementation separately; a design does not prove a release gate or external result.

## How to use this brief

This is a design-facing map, not a replacement specification. Before finalizing a screen or workflow, use the linked maintained sources:

- [Customer frontend plan](frontend.md): route contract, detailed layout patterns, state behavior, accessibility, migration, and journey acceptance/status.
- [Product scope](product.md): users, outcomes, product boundary, and company-fact caveats.
- [Book Zero plan](plans/15-book-zero-workflow-cash.md): first-period daily workflows and read-only Cash requirements.
- [Operations and review](operations.md): accounting authority, approvals, posting, and recovery semantics.
- [Open decisions](open-decisions.md): facts and release gates that remain unknown.
- [ADR 0006](adr/0006-customer-workspaces.md): decision for one shared customer workspace with different starting views.
- Sibling `/Users/admin/accounted` checkout: inspect the corresponding Accounted pages when mapping inherited workflows and interaction patterns. It is a working product reference, while OpenERP's maintained requirements govern OpenERP behavior.

Use the detailed frontend plan for current implementation status, not as a visual template or limit on intended functionality. The owner's Paper design direction governs target composition and flows; accounting invariants and real-fact gates still apply. Keep target design, implemented behavior and verified results distinct.
