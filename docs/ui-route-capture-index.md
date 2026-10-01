# UI route capture index

Capture date: 2026-10-01  
Viewport: consistent desktop browser viewport  
Data policy: Accounted's disposable sandbox and OpenERP's local synthetic book only

This index records the exhaustive route-capture pass requested by the design brief. The route lists were derived from the applications' route definitions rather than from their visible navigation.

## Coverage

| Product | Discovered rendered route templates | Captured or redirected state | Named blocker |
| --- | ---: | ---: | ---: |
| Accounted | 129 | 118 | 11 |
| OpenERP | 21 | 19 | 2 |
| **Total** | **150** | **137** | **13** |

`Captured or redirected state` includes a route whose own guard intentionally redirected to sign-in, the sandbox dashboard, or the public documentation host. Those redirects were captured because they are the route's observable UI behavior in the safe test context. Dynamic templates were opened with real synthetic record IDs whenever the sandbox supplied one.

## Accounted capture basis

The pass covers authentication, MFA guards, onboarding, company selection, the sandbox and sandbox journey, dashboard, assistant and knowledge, accounts and reconciliation, transactions and parties, invoicing and its registers, purchasing, documents, bookkeeping, tax, payroll, reporting, year-end, extensions, settings, public pages, and API documentation.

Representative synthetic dynamic captures include:

- invoice detail, edit, and credit attempt;
- customer and article detail;
- journal-entry detail;
- supplier detail;
- salary-run, run-employee, and employee detail;
- extension sector, extension detail, and extension runtime page;
- report slug, API cookbook slug, and API reference slug.

### Accounted blockers

| Route template | Access class | Capture status | Reproducible blocker | Counterpart |
| --- | --- | --- | --- | --- |
| `/arkiv/avtal/[id]` | Authenticated | Blocked | Disposable sandbox contains no agreement record or reachable agreement ID. | No OpenERP counterpart |
| `/arkiv/dokument/[id]` | Authenticated | Blocked | Disposable sandbox contains no document record or reachable document ID. | OpenERP purchases/document work is intentionally different |
| `/assets/[id]/dispose` | Authenticated | Blocked | Disposable sandbox contains no fixed-asset record. | No direct OpenERP route |
| `/chat/[id]` | Authenticated | Blocked | Sandbox AI is disabled and exposes no conversation ID. | No counterpart; chat is intentionally omitted as primary navigation |
| `/rules/[id]` | Authenticated | Blocked | Disposable sandbox contains no automation rule. | No OpenERP counterpart |
| `/sales-orders/[id]` | Authenticated | Blocked | Disposable sandbox contains no sales order. | OpenERP sales area, not a dedicated route |
| `/sales-orders/[id]/edit` | Authenticated | Blocked | Disposable sandbox contains no sales order. | OpenERP sales area, not a dedicated route |
| `/supplier-invoices/[id]` | Authenticated | Blocked | Disposable sandbox contains no supplier invoice detail record. | OpenERP purchases area, not a dedicated route |
| `/invite/[token]` | Public token | Blocked | No safe, valid invitation token exists; fabricating one would capture only an invalid-token state. | No OpenERP counterpart |
| `/invoice-action/[token]` | Public token | Blocked | No safe, valid invoice-action token exists. | No OpenERP counterpart |
| `/payslip/[token]` | Public token | Blocked | No safe, valid payslip token exists. | No OpenERP counterpart |

## OpenERP capture basis

The local application was run against a provisioned synthetic company and book. Captures cover entry/sign-in, companies, firm portfolio, intake, the book landing page, overview, work queue, accounts, banking setup, sales, purchases, bookkeeping, tax, reports, closing, settings, setup, history, and specialist tools.

### OpenERP blockers

| Route template | Access class | Capture status | Reproducible blocker | Counterpart |
| --- | --- | --- | --- | --- |
| `/entities/:entityId/books/:bookId/reviews/:planId` | Authenticated | Blocked | The synthetic book has no review plan ID. | Accounted uses domain-specific detail/review routes |
| `/entities/:entityId/books/:bookId/reviews/:planId/:revision` | Authenticated | Blocked | The synthetic book has no review plan or revision ID. | Accounted uses domain-specific detail/review routes |

## Important observed states

- Accounted's sandbox clearly labels that external services and AI are disabled and that data is deleted after 24 hours.
- Accounted's invoice credit route produced a meaningful blocked state for an invoice that was not eligible for credit.
- OpenERP's banking-setup route exposed an `InternalError` in feed-evidence recovery while the remainder of the setup UI rendered; this is retained as captured evidence, not normalized away.
- Empty states were captured where the synthetic data had no records, including OpenERP work, accounts, sales, and purchases.

## Remaining design step

The desktop route inventory is complete at the route-template level subject to the blockers above. Narrow captures still need to be produced for each distinct responsive page pattern before Paper layout work is considered complete.
