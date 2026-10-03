# Product focus review — 2026-10-03

Status: adopted product direction, 2026-10-03, under [ADR 0017](../adr/0017-bureau-first-product-focus.md). The owner accepted the recommendation, including keeping automatic posting separate. This record gives design detail; the ADR resolves scope precedence. Implementation and Paper coverage remain unverified by this adoption.

## Adopted commercial focus

Make the bureau the primary customer and distribution channel. The accountant owns routine bookkeeping within assigned book authority; the business owner answers questions and approves payments. Role labels never grant authority. Preserve an owner-operated path for Book Zero.

Concentrate the first commercial experience on incoming documents, bank matching, invoicing and VAT, with bureau work across clients as a core workflow. Demonstrate a complete loop: evidence arrives, the assistant proposes treatment, the accountant reviews or approves a bounded batch, and the posted result retains its source basis. L02/L03 review, K22 numbers’ basis and K20/M32 unknown outcomes are strengths to preserve.

Sequence quotes, orders, incoming orders, recurring billing extensions, currency extensions, ROT/RUT, native payroll, advanced assets/dimensions, intraday cash forecasting and broad ERP surfaces behind that loop. Evaluate a specialist payroll integration instead of promising a partial native compliance product. Historical import and closing remain necessary where they enable onboarding or a complete accounting period; a smaller sales wedge cannot conceal unsupported actual transactions.

This commercial sequence is adopted. Book Zero reconciliation and applicable accounting obligations remain required; Cash and native payroll product expansion move later. Existing packets retain their technical contracts and vectors, with commercial sequencing governed by ADR 0017.

## One place for human work

Use Att göra as the canonical queue for every task needing a person. Questions, review, missing bank evidence, VAT and closing checklists, email and bureau views should show filtered references to the same task rather than create competing copies. The actions log remains history; it may link to a current task but is not itself another pending queue.

Define task identity, company/book scope, responsible role, blocking dependencies, status, destination and durable completion. A question answered in one view must update every other view; answering it does not by itself approve or post the resulting treatment. Bureau views need assignment, client context, due work and exceptions without losing scope.

## Approval at realistic volume

Use three levels of review ceremony, with exact thresholds and eligibility still to decide:

| Work | Proposed experience | Required boundary |
| --- | --- | --- |
| Familiar, low-risk bookkeeping | Explainable proposals and bounded bulk approval | Each item retains exact effects, sources, authority, validation and receipt; changed items leave the approved batch. |
| New suppliers, unusual treatment, missing evidence or material amounts | Individual review or question | Show what needs judgment and why; uncertainty must not disappear into a confidence score. |
| Payments, external messages and filings | Explicit approval of the exact action and recovery state | Preserve frozen content, current dependencies, scoped execution, receipts and unknown-outcome handling. |

Bulk review can reduce clicks without removing immutable financial approval. Avoid presenting checksums and revision machinery as routine user work. A low amount alone does not make an accounting treatment safe.

Automatic posting after repeated unchanged matches is a separate proposed policy change to [R-05](../product.md) and the [approval contract](../adr/0002-exact-posting-and-approval.md). Repetition is evidence, not authority. Before adoption, specify activation permission, eligible transactions, amount and aggregate limits, corrections, suspension, revocation, rule versions and audit evidence. No match-count threshold or autonomous posting permission is established here.

## Automation after approval

The adopted commercial target combines human authority with execution convenience. Prioritize evaluation of live bank feeds, Peppol delivery, direct VAT filing and BankID login/signing. Employer declarations depend on the selected payroll strategy. These are target capabilities, not verified support, legal conclusions or selected providers.

Keep approval, dispatch, submission, acceptance and payment distinct. A timeout after dispatch must produce an unknown outcome and reconciliation path rather than a blind retry. Provider contracts, current official specifications, consent and observed outcomes must qualify each claim. [D-10](../open-decisions.md) now records connected execution as the commercial target under ADR 0017, with file/manual fallbacks and the existing gates for credentials, real filings, payments and live provider exercises. D-08 still governs dated rule qualification.

## Assistant and first value

Show the proposed account, its reason, the evidence used and what remains uncertain beside the review action. Show learned preferences only when a retained, authorized rule actually changed: name its scope, future effect and how to undo it. Do not invent confidence percentages or imply that unchanged approvals prove statutory correctness. Keep connecting a personal assistant through W13/W16 as an advanced path.

Build onboarding around connecting a bank, forwarding a few invoices, then reviewing proposals matched to bank evidence. Ask for detailed assistant policy after the user sees its effect; use conservative defaults with visible authority limits. The demo tour U29/U30 should reach this same moment using clearly synthetic facts. U16 policy setup and O03 manual import need reconsideration; retain file import as a truthful fallback while connections are unavailable.

## Success measures

Define measurement before claiming improvement. Segment by company, transaction type and review mode; report missing evidence and unresolved work alongside completed items.

| Measure | Proposed definition |
| --- | --- |
| Document-to-booking time | Elapsed time from durable document receipt to posting receipt; report median, tail and still-unposted age. |
| Proposals approved unchanged | Share of reviewed proposals approved without edits to their accounting effects; distinguish individual, batch and any future automatic mode. Track later corrections separately. |
| Month-close time | Time from period end to a defined reconciled close; disclose missing source coverage and reopening. |
| Human touches per transaction | Count meaningful review, edit, question and approval interactions; batch clicks must disclose how many transactions they cover. Track corrections so fewer touches cannot hide worse outcomes. |

## Design follow-through

The wedge, bureau priority, later Cash sequence, specialist-first payroll direction, role split and canonical queue are adopted. Specify task identity/lifecycle, permission mappings, batch eligibility and materiality policy before activating them. No payroll provider or automatic posting policy is selected.

Review V01–V19 bureau work, the home queue and L02/L03 first, then K22 provenance, K20/M32 recovery and U16/U29/U30 onboarding. Work one screen and its surrounding flow at a time under the [Paper prompt](../ui-design-prompt.md). Existing frames are drafts, and screen identifiers here describe feedback targets rather than inspected or completed designs.

Treat OpenERP as a provisional name. Evaluate a replacement before public branding, including current name availability and association checks. No new name or clearance is claimed.
