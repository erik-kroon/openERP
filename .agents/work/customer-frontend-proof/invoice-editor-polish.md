# Invoice editor polish — 23 September 2026

Full review of the invoice draft editor, its billing summaries, line details, payment/total area, and the shared disclosure as rendered in the invoice sidebar. React/TanStack, owned UI components, StyleX and existing tokens. No new dependencies, fonts, colors, test files, or accounting rules. This is a scoped polish result, not a product-wide parity assessment.

## Coverage

| Category | Evidence inspected | Result |
| --- | --- | --- |
| Typography | Editable invoice title, party summaries, numeric headers/inputs, updating totals; Swedish and English rendering | Clear after hierarchy and numeric alignment changes |
| Surfaces | Document, collapsed/expanded billing sections, one/two line states, terms/totals, sticky save footer at the browser's existing 1600 × 900 viewport | Clear; fields and actions remain reachable by normal scrolling |
| Animations | New editor/disclosure source, normal open/close interactions | No custom motion added to these frequent actions. A 10% replay is inapplicable to the new instant transitions |
| Icons | Native summary markers, remaining detail affordances, real customer select, existing add/remove controls | Repeated triangles removed; retained technical disclosures use quiet trailing plus/minus. Real selects retain their chevron |
| Performance | Changed component source, mounted inputs, build, live recalculation | No dependencies, effects, animation layers, or additional network calls. No performance benchmark claimed |

## Changes

| Severity | Location | Before | After | Why |
| --- | --- | --- | --- | --- |
| MEDIUM | `apps/web/src/components/commerce/invoice-drafts.tsx:296`, `packages/ui/src/components/record-layout.tsx:179` | Repeated document heading, company name, and a full-width description control | The editable invoice description is the document title, with a small draft label | Establishes a useful reading hierarchy and removes redundant chrome |
| MEDIUM | `apps/web/src/components/commerce/invoice-draft-party.tsx:10`, `apps/web/src/components/commerce/invoice-drafts.tsx:297`, `apps/web/src/components/commerce/invoice-drafts.tsx:798`, `packages/ui/src/components/record-layout.tsx:184` | Separate billing/sender accordions beneath uneven content | Aligned billing summaries with explicit Edit/Done actions; controlled summary text reflects edits immediately; inputs remain mounted | Secondary editing should be clear without making every section look like navigation |
| HIGH | `packages/ui/src/components/record-layout.tsx:202` | During the revision, collapsing an invalid country field could hide the reason saving was blocked | Done keeps the invalid field visible and invokes native validation | A user can correct the problem where it occurs |
| MEDIUM | `apps/web/src/components/commerce/invoice-editor-lines.tsx:115` | One triangle disclosure for each invoice line | One labeled tax/source-detail action controls the optional line fields, preserving their values when closed | Reduces repeated controls while keeping useful details available |
| MEDIUM | `apps/web/src/components/commerce/invoice-drafts.tsx:326`, `apps/web/src/components/commerce/invoice-editor-lines.tsx:174`, `packages/ui/src/components/record-layout.tsx:67` | Totals, terms, and agreed total occupied separate vertical sections; grid sections stretched their children | Terms/agreed total sit beside totals; section content aligns at the top | Spacing now expresses related groups and keeps invoice lines higher on the screen |
| LOW | `packages/ui/src/components/invoice-lines.tsx:64`, `packages/ui/src/components/invoice-lines.tsx:75`, `apps/web/src/components/commerce/invoice-editor-lines.tsx:224` | Amount fields and their headings were aligned differently | Numeric inputs/headings align right with tabular numerals | Makes amounts easier to compare and prevents digit-width shifts |
| MEDIUM | `packages/ui/src/components/disclosure.tsx:23` | Heavy native triangles and oversized spacing before technical details | Restrained trailing plus/minus, compact spacing, clear hover/focus states | Keeps disclosure understandable without repeating directional arrows |

## Considered but rejected

| Location | Candidate | Rejected because |
| --- | --- | --- |
| Invoice editor | Replace every triangle with another icon | It would preserve the same clutter; ordinary billing details needed a different presentation |
| Billing sections | Display every field permanently | Registration, country, and address fields would push line items farther down during routine edits |
| Billing/line toggles | Animate expansion with height transitions | These actions recur throughout the day; instant, labeled state changes are clearer and add no motion overhead |
| Customer selector | Remove its chevron too | It is a real option menu. Retaining one meaningful menu indicator is useful |

## Verification

Passed:

- Targeted `bunx oxlint --config .oxlintrc.type-aware.json` for the six changed files.
- `bunx tsc --noEmit --project packages/ui/tsconfig.json`.
- `bunx tsc --noEmit --project apps/web/tsconfig.json`. An earlier run caught a concurrently edited, unrelated command-recovery type error; the later run passed.
- `bun run --cwd apps/web build`; log: `.cache/customer-frontend/invoice-polish-build.log`.
- Targeted `bunx oxfmt --check` and `git diff --check`.
- Customer address edit → Done → updated summary → reopen retained the edited value; restored the demo address.
- Enter country `S` → Done kept the editor expanded, focused the field, and showed the native validation message. Correcting it to `SE` allowed closing.
- Open/close the consolidated tax/source details; existing tax treatment and agreed line amount remained present.
- Save with customer, seller, and line details collapsed → dialog closed successfully → revision history showed revision 3 → reopened the draft. API contract validation confirmed both addresses, both country codes, tax description, source gross and agreed total survived. Evidence: `.cache/customer-frontend/invoice-polish-save-proof.json`.
- Add an empty second line → totals show unknown, not zero. Enter price 1,000 and tax 250 → total 16,250 SEK. Remove that unsaved line → total returns to 15,000 SEK.
- New invoice → no customer, missing address caption and unknown totals; Save disabled. Selecting the existing customer produced the billing summary. Closed without saving.
- Shared history disclosure expanded/collapsed and showed the saved revision.
- Source review of hover/focus styles; focus and disabled states observed during interactions. No independent hover recording or motion timing benchmark.

The shared preview briefly failed during concurrent repository changes. An isolated frontend on port 3112 supported rendering and field validation but correctly rejected writes from that origin. No permission settings were changed. The final successful save and screenshots use the normal port 3107.

Screenshots use the real viewport, with no resizing or synthetic image edits:

- `.cache/customer-frontend/invoice-before-polish.png`
- `.cache/customer-frontend/invoice-after-polish.png`
- `.cache/customer-frontend/invoice-payment-details.png`

Repeat: open Invoicing → September design retainer → Edit draft. Exercise Edit/Done and tax details; scroll to payment terms. Save a reason-only revision in this synthetic workspace and reopen to compare the retained fields.

Verdict: **Approve for the inspected invoice editor scope.** Not verified: unrelated consumers of the shared disclosure, mobile, dark mode, 200% zoom, production invoice delivery, and the broader frontend parity plan. No claim of completion for those scopes.
