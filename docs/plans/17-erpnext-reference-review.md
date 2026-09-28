# ERPNext/Frappe reference review: adoptable concepts

Status: **planning input, not a work order**. Prepared 2026-09-28 from read-only shallow clones. This document adds no implementation, test or proof claim and activates no rule, rate, provider or legal profile. Nothing here is copied code: every nugget below is a concept or algorithm to re-implement clean-room, under the rule-adoption classes in the [parity backlog](11-parity-backlog.md#rule-adoption-classes) and the provenance rules in [LICENSING.md](../../LICENSING.md).

## Source and method

- Reference checkouts (sibling directories, **outside this workspace** — never imported, never a dependency): `/Users/admin/erpnext` at `91dced3` (2026-09-28) and `/Users/admin/frappe` at `4ac9eb1` (2026-09-28). Shallow depth-1 clones; hashes identify the reviewed snapshot, not authenticity.
- Three read passes: the full `erpnext/accounts/` module, the Frappe framework machinery plus cross-cutting mechanics, and the posting bridges (assets, stock, projects, subscriptions, POS, quality gates, payroll/e-commerce extraction points).
- The clones were not built, executed, or fixture-installed. Findings are the readers' observations, not verification of either repository.

## License positions

- ERPNext `license.txt` is **GPLv3**. Concepts and deterministic algorithms may be re-implemented in original code; any verbatim adaptation needs per-file provenance, preserved notices, and a compatibility check before it lands. GPLv3 material is never described as newly licensed project code.
- Frappe `LICENSE` is **MIT** (Copyright Frappe Technologies Pvt. Ltd.). Reusable with attribution under its terms; the same per-file provenance rule applies.
- Swedish statutory content (rates, thresholds, declaration schemas) is class-B/C dated material in all cases: structure may transfer, figures never do without a primary source under [D-08](../open-decisions.md).

## Posting pipeline (accounts + framework)

- **Draft → submit → cancel, amend by copy.** `docstatus` 0/1/2 is terminal on cancel; correction is cancel plus a new document carrying `amended_from` (`frappe/model/docstatus.py`, `frappe/model/document.py` submit/cancel/amend paths; `journal_entry.py` on_submit/on_cancel). Matches the application-owned replacement direction in [ADR 0010](../adr/0010-application-owned-accounting-replacement.md).
- **One central GL sink.** `general_ledger.py make_gl_entries` funnels every voucher through budget check, offsetting entries, period/freeze/dimension validation, cost-center split, similar-entry merge, then save; cancel mirrors with `make_reverse_gl_entries` and flags `is_cancelled` instead of deleting. Candidate pattern for the shared posting operation.
- **Zero-difference gate.** Journal validation refuses unless total debit equals total credit; Payment Entry refuses unless its difference amount is zero after allocations, deductions and taxes. Refuse unbalanced vouchers at validation, not at report time.
- **Four-layer money.** Every line carries company, account, transaction and reporting currency amounts plus both exchange rates. FX stays isolated from exact minor-unit arithmetic.
- **Ledger preview before submit.** `controllers/ledger_preview.py` renders the exact Dr/Cr (plus stock-ledger) lines of a draft. Cheapest exact-money control available: block submit on any imbalance or missing account shown in the preview.
- **Immutable-ledger mode.** A settings flag switches cancel from back-dated reversal to today-dated reversal and forbids opening entries after any period close. Strict append-only versus pragmatic fix-up without forking posting code.
- **Naming series.** Prefix counters with date placeholders plus amend suffixing (`ACC-JV-.YYYY.-`, `-1` amends), concurrency-safe. Human-sortable voucher identity for receipts.

## Close, freeze and periods

- **Contiguous period close.** The close voucher requires start = previous close + 1, no future close, prior year closed, and posts P&L into a balance-sheet closing account plus closing-balance snapshots. A checklist that verifies instead of assuming.
- **Layered locks.** Closed doctypes per accounting period, a freeze date with an explicitly authorized role (administrators not exempt), per-account freeze, and refusal of opening entries once a close exists.
- **Versioned reposts.** `Repost Accounting/Payment Ledger` and item-valuation reposts recompute scoped vouchers as new entries with before/after, never rewrites. Pair with the field-level Version diff journal the framework writes on every save.

## Parallel books and dimensions

- **Finance Book as a tag.** The book is one name record plus a column on GL rows, vouchers and reports — no dual-posting engine. Enough for K3-versus-tax dual reporting views.
- **Declared accounting dimensions.** A dimension definition injects the field into doctypes and GL; P&L accounts must carry axes while balance-sheet accounts must not (which axes mandatory is local policy). Cost-center allocation splits each GL row pro-rata at post time with a 100% sum rule, no chains, and a validity start after the last posted entry. Multi-dimension vouchers get auto-balancing offsetting entries.

## Settlement and bank

- **GL versus payment-ledger split.** GL is valuation truth; a separate payment-ledger subledger owns `outstanding` per voucher pair. Prevents AR/AP drift between reports and collectability.
- **Explicit allocation math.** Unallocated, allocated and difference amounts are first-class; unmatched payouts stay unapplied with a named reason; unlinking is its own logged document, never a silent delete.
- **Priority bank-rule matcher.** Ordered rules on transaction type, amount band, description match and a safe amount formula, with an auto-plug last row and an evaluated flag. Deterministic and portable.
- **Statement import as mapping.** Per-format field maps plus a column-map log, MT940 support, optional submit-after-import. Sits naturally beside the existing bank-format work.

## Currency, budgets, dunning

- **Realised versus unrealised FX split.** Settlement posts an idempotent gain/loss journal (already-booked check, cancel cascades); a revaluation wizard snapshots balances, computes booked-versus-unbooked gain/loss with a rounding allowance, tracks reversal, and refuses empty results. Rate source with a banking-day look-back; a null rate stays null, never a fallback.
- **Budget gate with three actions.** Annual and accumulated-monthly checks against posted plus ordered plus requested amounts, per action Stop, Warn or Ignore. The Stop/Warn split is the adoptable part.
- **Dunning as arithmetic plus state.** Interest equals outstanding times daily rate times overdue days plus fee; payment submission resolves linked dunnings. Rate and fee enforceability stay local legal questions.

## Commerce extras worth a look

- Advances engine with automatic allocation and gain/loss on advance settlement; taxes-and-charges templates with inclusive-tax price backout; deferred revenue/expense via a monthly job posting straight-line journals (invert to propose-then-approve); payment-term schedules splitting due dates; returns as `is_return` plus `return_against` referencing the posted invoice; POS closing that consolidates shift invoices per customer and dimensions with an explicit merge log that can unmerge; subscriptions as schedule-driven invoice proposals (never auto-submit); inter-company mirror journals with totals checks.

## Framework mechanisms (MIT)

Docstatus machine, controller hook pipeline plus external `doc_events` registry, field-level permlevels with row-level user permissions injected into list queries, company restriction tables, naming series, per-save Version diffs, durable submission queue with locks, event-to-notification fan-out with offset alerts, auto-repeat schedules, milestone trackers plus assignment rules as review-queue primitives, print-format artifacts with DRAFT/CANCELLED banners, and the regional plug-in pattern (`get_region` dispatch plus per-country setup modules for custom fields, permissions and reports).

## Posting bridges: what posts and what does not

- Stock posts only under a perpetual-inventory toggle through a stock GL composer; landed costs distribute onto receipts as their own approved voucher; corrections are scoped reposts. Assets post depreciation journals per schedule row with freeze guards, and capitalization/repair composers consume stock and service lines visibly.
- Projects, warranties, quality records and work orders post nothing themselves: projects bill through invoices, warranties link serials to replacement documents, and quality inspection is a typed refusal gate before submit — the cleanest gate pattern found, worth mirroring wherever an acceptance declaration must precede posting.
- Payroll, e-commerce and payment gateways are **extracted to separate apps** (`hrms`, `webshop`, `payments`) in current ERPNext; only stubs and the payment-request/reconciliation seams remain in core. A payroll or gateway review needs those repos, not these clones.
- Subscriptions and scheduled depreciation **auto-submit** upstream; under this repository's authority rules both arrive as proposals and post only through approval.

## Sweden position

No Swedish chart template ships (76 verified plus unverified templates inventoried, none Swedish). Sweden exists only as a tax seed (25/12/6/0 sales and input VAT accounts) and an `sv.po` locale. The BAS chart, mom rules and SIE content remain local class-B/C work; the regional plug-in pattern above is the vehicle, not a fork.

## Adoption verdicts

Reconciled against current code, 2026-09-28. Most of this review confirms decisions already taken rather than adding work; the reversals and additions are named here so a later reader does not re-litigate them.

| Nugget | Verdict | Owner |
| --- | --- | --- |
| Ledger preview before submit | **Owned**, except the block. Exact lines and approval scope are existing frontend requirements; the real gap is [DF-01](13-reference-derived-defects.md), a balance guarantee whose second code path has no trigger. | PST |
| GL/payment-ledger split | **New packet.** "One owner of outstanding" is not yet named anywhere; Cash and ageing each read receivables today. | PRY-133 |
| Immutable-ledger mode flag | **Rejected.** A flag allowing back-dated correction is a weakening; the ledger's absolute immutability is deliberate. Record the reasoning in `docs/domain.md` so the flag is not helpfully re-added. | Domain doc |
| Finance Book as a tag | **Mostly owned** by the report-basis work in PRY-86. At most one optional valuation-basis field on the existing book. | END |
| Contiguous close + layered freeze | **New packet.** The close checklist exists, but the comparison records locked-period write refusal as a database gap: the refusal is application-level today. | PRY-132 |
| Regional plug-in dispatch | **Mostly owned.** `jurisdictions/se` is a compile-time seam, better than a runtime `get_region` dispatch. Missing piece: refuse admission when no BAS chart exists. | jurisdictions/se |
| Typed refusal gates | **Owned.** Refusal discipline is the product's thesis (R-05, R-07, E-01, E-15). | PST, VAT |
| Invert their schedulers | **Owned.** effect-mq has no silent financial effect by design; their auto-submit subscriptions and depreciation are the behaviour being inverted. | OPS, PAY, AST |

Only PRY-132 and PRY-133 were added from this review. The rest is confirmation.

## Suggested homes (pointers, not packets)

No PRY/NEXT packet is created by this review. When the work is scheduled: pipeline items belong with the posting/approval owners, close items with the year-end owner, dimensions and books with the shared-contracts owner, settlement and bank items with the intake/matching owner, FX with the currency owner, and framework mechanics with the operations owner. Regional Swedish content needs a dated company fact and reviewer before any parameter set exists, per the existing applicability gates.

## Maintenance

Run `python3 docs/plans/check-plan.py` after any change here. It validates links, anchors and whitespace. It does not execute product tests, and it does not verify any finding in this document.
