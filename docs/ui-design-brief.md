# OpenERP interface design brief

Purpose: give Paper design work one clear product brief before visual exploration begins. OpenERP is an Accounted-derived product, so Accounted is the starting product and interaction reference for this work, not an unrelated competitor. This brief describes the user-facing product OpenERP needs to become; it is not a claim that every route or capability is complete today.

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
5. Perform only the operation the product actually supports, then find its durable result and history again.
6. Reconcile both the account totals and the underlying transaction coverage; investigate differences rather than hiding them.
7. Trace report totals and posted entries back to decisions and evidence.
8. Return to the same company, period, record, and filtered work after navigation or reload.

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
    ├── Tax                    supported review and preparation only
    ├── Reports                saved reports, drilldown, review outputs
    ├── Year-end               period assessment and handoff
    └── Settings               book configuration and access
```

Keep navigation task-based and shallow. Use subnavigation within an area. Show a destination as a normal working area only when its owned workflow is usable; keep unsupported or gated capabilities visible in setup/readiness or at the relevant record, not as a sidebar of disabled future modules. Advanced recovery tools remain reachable for their current users, but should not define the everyday product.

## Page design map

For every page, Paper should explore the useful working state first, then the relevant empty, incomplete, blocked, loading, error, and completed states. The "see" and "do" lists describe intended user needs, not promises that every item is currently available.

| Page / area | What the user needs to see | What the user needs to do |
| --- | --- | --- |
| **Entry and sign-in** (`/`) | Sign-in or the user's authorized destination; clear company access state if no book is available. | Sign in, continue to an authorized book, or choose a company. Never imply a company was silently created. |
| **Companies** (`/companies`) | Authorized books with enough identity and period context to choose the right one. Distinguish no access from loading or failure. | Open a book, switch context, or follow the real access/setup path. |
| **To do / work queue** (`/entities/:entity/books/:book` and `/work`) | Prioritized unresolved work, grouped by meaningful reason and state. Each item shows its source, period, amount when applicable, blocker/next action, and freshness/coverage context. Prepared, blocked, completed, and empty-with-incomplete-coverage must not collapse into one state. | Filter/search/sort, open a review, resume work, follow missing-evidence paths, and return without losing queue context. |
| **Overview** (`/overview`) | The most important unresolved decision first; a small, dated, source-labelled view of cash/receivables/payables where available; period progress and named blockers. No decorative wall of interchangeable KPI cards. | Start the next useful task, inspect a supported summary, or go to the work that explains it. |
| **Review detail** (`/reviews/:plan/:revision`) | Company/book and period; source identity and original; interpreted facts and conflicts; proposed treatment, exact accounting effects, warnings, revision/dependency status, allowed action, history, and durable outcome. A person must be able to inspect evidence before acting. | Review, request a supported change/new revision, approve the exact version, execute only the separately supported operation, or recover its receipt. |
| **Banking / accounts** (`/accounts`) | Named accounts and selected period; statement coverage, ledger balance, statement balance, difference, unmatched items, and import freshness shown as separate facts. Imported data is not a live bank balance. | Choose an account/period, import a supported statement, inspect transactions, review a proposed/manual match, allocate, and reconcile supported items. |
| **Sales** (`/sales`) | Customer and invoice registers with useful status, search, sort, amount, dates, and settlement state. Draft, registered, delivered, paid, and posted are distinct states. | Create/edit a supported invoice, inspect its document and history, follow supported settlement/matching actions, and return to the same register context. Do not imply sending or legal issuance if unavailable. |
| **Purchases** (`/purchases`) | Source documents, supplier invoices, and expense work with original beside entered facts when reviewing. Mark manual/entered facts as such; show missing or conflicting evidence. | Add or inspect an original, prepare/correct a draft, review a supported treatment, and follow its result back from the source. A source tax review is not itself a filing or posting. |
| **Bookkeeping** (`/books`) | Posted vouchers and their source/review lineage; correction history; relevant schedules and period readiness. Put business meaning before technical IDs. | Find a voucher, trace evidence, start a supported correction, inspect schedules, and resolve a named period blocker. Posted history is never silently edited. |
| **Tax** (`/tax`) | Supported tax/VAT review with source population, included/excluded items, calculations, control differences, evidence, and currentness. Unknown applicability or coverage remains explicit. | Inspect a supported calculation, prepare/review an artifact where available, and follow control discrepancies to their owner. Never present prepared as filed, assessed, paid, or accepted. |
| **Reports** (`/reports`) | Searchable report catalogue, selected period/snapshot, source basis and currentness. Totals need a path to accounts, vouchers, decisions, and evidence. | Open or prepare a supported report/review pack, drill into the underlying lines, export available artifacts, and return with report scope intact. |
| **Year-end / closing** (`/closing`) | A period checklist with known coverage, explicit applicability, owner-reasoned blockers, review date, and links to work. Technical lock and statutory completion are visibly different. | Assess supported areas, resolve blockers, prepare the available handoff, and inspect the resulting version. Do not imply filing or acceptance. |
| **Settings** (`/settings`) | Book identity, currency, access, language, accounting periods, chart, and configured choices, with unknown/unverified facts not dressed up as defaults. | Change only settings supported by actual controls and authority; inspect access or configuration paths. |
| **Firm portfolio** (`/firms`) | Client list/matrix with relevant period, work count, freshness, responsible person, review timing, and explicit unknown coverage. One client's status must not imply another's. | Search/filter clients, assign or hand off within supported permissions, open one client in its scoped workspace, and return to the same portfolio filters. Portfolio scanning is not cross-book financial authority. |
| **Advanced tools / recovery** (`/tools`) | Clearly named specialist operations and their context, current status, and recovery steps. Do not expose implementation jargon as the ordinary navigation model. | Reach existing specialist recovery and technical flows without losing their source record or scope. Keep until everyday destinations cover the same operations and recovery. |
| **Local intake preview** (`/intake`) | Clear statement-import preview and the fact that it is an intake/preview surface, not a complete purchase inbox or live bank connection. | Preview supported local inputs and continue only through the available import flow. |

## Shared frame and interaction rules

- Keep company/book identity and selected period visible through lists, review, approval, and result. A company switch clears old scoped content before showing the new one.
- Use real navigation and addressable records. URL state carries the navigable scope, period, filters, sorting, page, and selected record; it never grants access.
- Preserve search, filters, pagination, and position on return. Deep links and reload must resolve to the same authorized object.
- Prefer a useful list with an optional inspector on wide layouts. On narrow layouts, open a full-width detail instead of squeezing list, source, and editor into unusable columns.
- Reuse a few page patterns: overview, filtered register/queue, full record review, and account/period reconciliation. Don't force every domain into the same card dashboard.
- Keep the original legible and unaltered. Show exact amounts with explicit currency, dates with clear meaning, and money aligned for scanning.
- Keep technical identifiers and receipts available but secondary to the object's name, amount, state, and next action.
- Use specific action labels. Preparing, approving, posting, paying, submitting, and acceptance are not synonyms. Show success only after the owning durable result exists.
- Keep the interface useful at desktop and narrow widths, keyboard operable, readable at 200% zoom, localized, and coherent in light/dark themes. Do not rely on color, hover, animation, or a toast alone to convey state.

## Visual direction for Paper exploration

Start with a professional, editorially calm financial workspace: clear typography, precise alignment, confident whitespace, restrained color, and enough density for real registers. Use hierarchy and grouping instead of putting every datum in a card. Make evidence and accounting effects feel like parts of one review, not separate apps.

Keep OpenERP's established palette, fonts, StyleX tokens, and component system as implementation constraints; Paper exploration can challenge composition and hierarchy, not invent a second shipped design system. A distinctive brand expression is welcome if it stays quiet around financial data. Avoid generic SaaS gradients, oversized KPI tiles, decorative charts without a decision behind them, and chat as the primary navigation. Do not redesign a familiar Accounted workflow merely to make OpenERP look different.

Use the Accounted repo to ground comparisons in the actual product: inspect its corresponding page and interaction, not just a screenshot or assumption. For each area, decide whether OpenERP should **keep** the pattern, **adapt** it to OpenERP's workflow, or **omit** it because the capability is outside scope or unsupported. Record the reason when the user-facing behavior differs. Accounted is the product lineage and a strong workflow reference; OpenERP's maintained contracts and product decisions still govern what OpenERP may claim or do.

### Reference capture before redesign

Before drawing new screens, build an exhaustive visual inventory of **every rendered UI route** in the Accounted and OpenERP applications. OpenERP is an Accounted clone, so the goal is to compare the whole route surface, not just a curated set of core workflows. Do not sample, prioritize only major journeys, or stop when the visible navigation is covered. Do not start from memory or assume the currently prominent navigation shows every screen.

Derive the route list from both repos' route definitions, including nested and dynamic routes. Capture every page route and route-backed overlay, including auth, onboarding, public/anonymous pages, settings modals, sandbox/demo pages, and specialist or less-used product surfaces. Dynamic route templates count as routes: open each template with a representative safe record. For routes that cannot be reached without unavailable credentials, data, or setup, record the route and the exact blocker instead of silently omitting it. Inventory API endpoints and non-rendering handlers separately; they are not screenshot targets.

Create one inventory row for every route template in each repo. For every route, record: product, route/template, access class, user job, capture status, viewport, data/state basis, and counterpart mapping. Pair related Accounted and OpenERP routes where possible; mark **no counterpart**, **not implemented**, **intentionally different**, or **blocked** explicitly. Capture at a consistent desktop viewport for the full route inventory. Also capture narrow layouts for every distinct responsive page pattern and for any route whose composition materially changes at narrow width. In addition to each route's representative usable state, capture route-specific empty, incomplete, blocked, error, or completed states when those states exist and materially change the screen. Use only safe synthetic/demo data and do not expose real company or personal data in Paper.

Keep the captures together as a labelled Paper reference page or linked frame set, with a complete route index and Accounted/OpenERP pairing. The inventory is complete only when every discovered route in both repos has a capture or a named, reproducible blocker; an uncaptured or unrecorded route keeps the design step open. The current desktop capture pass and its blockers are recorded in [UI route capture index](ui-route-capture-index.md). Use the full set to make explicit keep/adapt/omit decisions before polishing visual styling. Screenshot evidence documents appearance only; route behavior and current capability status must be checked against OpenERP source and maintained requirements.

After the exhaustive inventory, the first designed Paper canvas should contain one company frame, one To do page, one full review detail, one account reconciliation page, and one firm portfolio. Show desktop and narrow variants and include at least one blocked/incomplete state. These screens set the hierarchy and reusable patterns for the remaining page map; the full route capture remains the baseline for later design coverage.

## Product truth and guardrails

- Unknown is not zero; an empty list is not proof of complete books. Show the basis and gaps behind summaries.
- Preserve the distinction between source evidence, entered facts, proposed treatment, approval, posted result, and external outcome.
- Do not invent company identity, tax/accounting profile, registrations, deadlines, balances, or provider connectivity.
- Cash, when designed, is a dated and explainable read-only forecast. It does not initiate a payment or promise spendable funds.
- Access, approval, and execution are enforced by the owning backend contracts. Presentation preferences, firm membership, and assignments do not create book authority.
- Design only supported operations as active. When a capability is conditional, make its requirement and current state clear without implying it has passed its gate.

## How to use this brief

This is a design-facing map, not a replacement specification. Before finalizing a screen or workflow, use the linked maintained sources:

- [Customer frontend plan](frontend.md): route contract, detailed layout patterns, state behavior, accessibility, migration, and journey acceptance/status.
- [Product scope](product.md): users, outcomes, product boundary, and company-fact caveats.
- [Book Zero plan](plans/15-book-zero-workflow-cash.md): first-period daily workflows and read-only Cash requirements.
- [Operations and review](operations.md): accounting authority, approvals, posting, and recovery semantics.
- [Open decisions](open-decisions.md): facts and release gates that remain unknown.
- [ADR 0006](adr/0006-customer-workspaces.md): decision for one shared customer workspace with different starting views.
- Sibling `/Users/admin/accounted` checkout: inspect the corresponding Accounted pages when mapping inherited workflows and interaction patterns. It is a working product reference, while OpenERP's maintained requirements govern OpenERP behavior.

When these documents describe current code or acceptance, they outrank this summary. Treat the detailed frontend plan as the living source for implementation status; update this brief only when the product's design direction or page map materially changes.
