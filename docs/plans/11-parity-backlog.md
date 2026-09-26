# Reference parity backlog and preserved rule logic

Status: **planned scope, high level**. Prepared from a folder-level comparison of the `accounted` reference implementation against this repository. The comparison is a planning input, not a verification of either repository: a surface existing in the reference does not establish correctness, and a surface missing here is only assigned once the live code was checked. This document adds no implementation, test or proof claim and activates no rule, rate, provider or legal profile.

Owner: cross-area integrator, with the per-area owner named by each packet. Phase: sequenced after the seven-area [delivery plan](README.md) baseline; the packets here are **supplemental** and are not added to the 53-packet accounting index.

The decision to keep parity work outside the mandated delivery index, and to classify every adopted rule before implementation, is recorded in [ADR 0011](../adr/0011-reference-parity-backlog.md).

## Purpose

`docs/plans/capability-backlog.md` already reconciles a capability-level comparison. This document answers a narrower question the capability index cannot: for each source folder in the reference, **what is missing, what is the smallest honest unit of work, and which internal logic is worth keeping**.

Three outcomes are possible for a reference capability, and they are recorded distinctly:

| Outcome | Meaning |
| --- | --- |
| Owned | An existing packet in the seven-area plan, or a maintained requirement, already owns it. Nothing is added. |
| Supplemental | Missing here and named in a requirement but without a work unit. Assigned a `PRY-nn` packet here. |
| Unowned | Missing from both the code and the plans. Assigned a `PRY-nn` packet here and, where it depends on a company fact or a primary source, an applicability gate. |

## How to use this backlog

### Packet namespace

`PRY-nn` packets are **supplemental**. They are deliberately not `FND`/`PST`/`IMP`/`COM`/`VAT`/`PAY`/`AST`/`FX`/`END`/`OPS` packets, so they do not enter the mandated dependency index or the delivery denominator. Where a `PRY-nn` packet must complete an existing packet, that packet is named as a prerequisite; where a `PRY-nn` packet is a prerequisite **of** an existing packet, that is recorded as a blocking note on the existing packet. Do not renumber either namespace to merge them.

Each packet states owner, prerequisite, deliverable and the rule-adoption class its implementer must resolve first.

### Rule-adoption classes

This is the part an implementer must read before writing code. The reference encodes Swedish statutory constants next to the algorithms that consume them. **The algorithms are reusable; the constants are not authority.**

| Class | Meaning | Implementer's obligation |
| --- | --- | --- |
| **A — Adopt** | A deterministic algorithm with no external authority: check-digit arithmetic, subset search, reference parsing, tolerance ordering, aggregation order. | Port the algorithm. Preserve its stated failure behaviour. Replace floating point with the exact minor-unit model. Add independent expected results; never obtain them by calling the production code. |
| **B — Structure only** | The *shape* of a rule is reusable but every number, table, date or threshold is a dated external fact: tax tables, contribution rates and caps, VAT boxes, deadlines, schabloner, exchange rates, XML schema versions. | Port the structure. Treat every reference constant as a **test fixture only**. Acquire the parameter set from a dated primary source under [D-08](../open-decisions.md), version it, and refuse rather than default when it is absent. |
| **C — Re-derive** | A legal judgement, eligibility test or applicability decision: taxability, reverse-charge eligibility, ROT/RUT qualification, whether a company may use a method at all. | Do not port. Re-derive from the applicable rule and the company fact under [D-04](../open-decisions.md). The reference's outcome is evidence that a question exists, never the answer. |

A packet that mixes classes is split before implementation, or its class-B/C parameter set is named explicitly in its deliverable.

### Precision and money

Every ported amount rule uses `packages/domain/src/money.ts` minor units and the exact conversion helper in `packages/domain/src/exchange-rates.ts`. Reference implementations frequently use IEEE-754 doubles with a `roundOre` helper; where a rule is genuinely a whole-krona truncation, model the truncation explicitly and record the authority. **A float port of a krona rule is a defect, not a simplification.**

### Non-negotiable refusals

Three behaviours in the reference are load-bearing and must survive the port, because losing them converts a safe refusal into a silent accounting error:

1. **An unreadable input returns null, never a guess.** A wrong voucher link, a wrong payer identity or a wrong unit is written once and becomes räkenskapsinformation that cannot be corrected in place.
2. **A missing rate is no rate.** A fabricated fallback rate is worse than an absent one, because an absent one is repairable and visible.
3. **An override is bound to what was detected now.** An approval issued before the current state cannot authorise an action against a changed state.

## Folder-level coverage

Reference folder → disposition. "Owned" names the requirement that already carries it.

| Reference folder | Disposition |
| --- | --- |
| `invoices/` | Largely owned by [COM-02/04/05/06](../plans/04-invoices-payments-registers.md) and the supplemental commerce sections. **Unowned:** ROT/RUT, reduced/reverse-charge/export rate families, customer credit note, recurring invoice templates, late-payment interest and reminder fee, self-billed sale, mandatory-content gate, cash method, öre rounding, UN/ECE units, per-line posting account, invoice-driven deferral, delivered-byte retention, customer statement artifact → [PRY-44](#external-systems-identity-and-provider-authority) to [PRY-54](#commerce-and-open-item-registers). Peppol → [PRY-12](#external-systems-identity-and-provider-authority). |
| `transactions/` | Matching-only bank surface is owned. **Unowned:** booking a bank row into a new voucher ([PRY-42](#matching-and-reconciliation)), receipt↔bank matching ([PRY-43](#matching-and-reconciliation)), ignoring an imported row ([PRY-35](#matching-and-reconciliation)). |
| `import/` | SIE admission is owned and stronger than the reference. **Unowned:** parser tolerance ([PRY-21](#source-intake-and-migration)), validation rules ([PRY-22](#source-intake-and-migration)), encoding detection ([PRY-23](#source-intake-and-migration)), mapping suggestions ([PRY-24](#source-intake-and-migration)), chart effects ([PRY-25](#source-intake-and-migration)), undo/multi-year/dimensions ([PRY-26](#source-intake-and-migration)), workbook reader ([PRY-27](#source-intake-and-migration)), register importers ([PRY-28](#source-intake-and-migration)), opening-balance cascade ([PRY-29](#source-intake-and-migration)), source chart ([PRY-30](#source-intake-and-migration)), underlag attach ([PRY-31](#source-intake-and-migration)), SIE 4E export ([PRY-32](#source-intake-and-migration)), bank formats ([PRY-08](#external-systems-identity-and-provider-authority)). |
| `documents/` | Retention and review-artifact capture are owned and strong. **Unowned:** read pipeline ([PRY-75](#documents-and-evidence)), extraction engine ([PRY-76](#documents-and-evidence)), classification/provenance/queue ([PRY-77](#documents-and-evidence)), page-text search ([PRY-78](#documents-and-evidence)), unlinked surface and upload path ([PRY-79](#documents-and-evidence)), handling history ([PRY-80](#documents-and-evidence)). |
| `salary/` | Foundation only. Everything from the pay-run record onward is **unowned** → [PRY-59](#payroll-and-declarations) to [PRY-74](#payroll-and-declarations). |
| `reconciliation/` | Allocations, reversals, candidate reads, coverage, sign-off and tax-account matching are owned and several are stronger. **Unowned:** covering set ([PRY-33](#matching-and-reconciliation)), residual and decomposition ([PRY-34](#matching-and-reconciliation)), sweep ([PRY-36](#matching-and-reconciliation)), non-bank and multi-currency scope ([PRY-37](#matching-and-reconciliation)), sign-off semantics ([PRY-38](#matching-and-reconciliation)), already-explained guard ([PRY-39](#matching-and-reconciliation)), confidence ladder ([PRY-40](#matching-and-reconciliation)), comparability ([PRY-41](#matching-and-reconciliation)). |
| `tax/` | Obligation records and the calendar feed are owned. **Unowned:** holiday and banking-day calendar ([PRY-81](#deadlines-calendar-and-currency-reporting)), statutory families ([PRY-82](#deadlines-calendar-and-currency-reporting)), escalation and regeneration ([PRY-83](#deadlines-calendar-and-currency-reporting)), feed conformance ([PRY-84](#deadlines-calendar-and-currency-reporting)). |
| `vat/` | Box arithmetic with exact units and honest blockers is owned. **Unowned:** full box set and account mapping ([PRY-55](#vat-and-tax-account-profiles)), treatment taxonomy ([PRY-56](#vat-and-tax-account-profiles)), period cadence and filing record ([PRY-57](#vat-and-tax-account-profiles)), plausibility and Swedish VAT number ([PRY-58](#vat-and-tax-account-profiles)), VIES and EU tables ([PRY-11](#external-systems-identity-and-provider-authority)). |
| `providers/` | **Entirely unowned.** No reference provider, and no cross-cutting provider infrastructure, is named anywhere in this repository → [PRY-01](#external-systems-identity-and-provider-authority) to [PRY-05](#external-systems-identity-and-provider-authority). |
| `skatteverket/` | Tax-account matching and controls are owned. **The connection is unowned** → [PRY-06](#external-systems-identity-and-provider-authority); file import → [PRY-07](#external-systems-identity-and-provider-authority). |
| `currency/` | Money and scale modelling are owned and ahead of the reference. **The rate source and rate-date policy are unowned** → [PRY-10](#external-systems-identity-and-provider-authority), [PRY-20](#swedish-identifiers-and-payment-primitives), [PRY-54](#commerce-and-open-item-registers), [PRY-85](#deadlines-calendar-and-currency-reporting). |
| `bankgiro/` | **Entirely unowned**, and the cheapest high-value item here → [PRY-16](#swedish-identifiers-and-payment-primitives) to [PRY-18](#swedish-identifiers-and-payment-primitives), [PRY-24](#source-intake-and-migration) (`R19`). |
| `deadlines/` | Obligation identity, outcome history and revocable feed are owned. **Escalation, regeneration and date derivation are unowned** → [PRY-83](#deadlines-calendar-and-currency-reporting), [PRY-82](#deadlines-calendar-and-currency-reporting). |
| `calendar/` | Feed is owned and more conformant than the reference. **Gaps are unowned** → [PRY-84](#deadlines-calendar-and-currency-reporting). |

## External systems, identity and provider authority

Every packet in this section is gated on [D-10](../open-decisions.md) for credentials and authorization. **No adapter may be written before [PRY-01](#external-systems-identity-and-provider-authority) and [PRY-02](#external-systems-identity-and-provider-authority) exist**; an adapter without a credential store cannot be added safely.

| ID | Deliverable | Owner | Prerequisite | Class |
| --- | --- | --- | --- | --- |
| PRY-01 | Book-scoped provider credential and consent store: access and refresh tokens, expiry, granted scope, credential revision, revocation. Rotation is guarded by revision so a concurrent second refresh cannot overwrite a freshly rotated pair; a lost race adopts the winner rather than invalidating it. Token material is encrypted at rest with a documented key-rotation consequence. Provider identity becomes a validated, non-free-text field. | OPS | — | A |
| PRY-02 | Provider call infrastructure: per-provider request budget with fairness ordering, bounded retry honouring `Retry-After` and per-error retryability, a whole-run execution budget threaded through every call and wait, and a provider error taxonomy that separates "reconnect" from "buy the licence" from "this register is closed" from "unreachable". | OPS | PRY-01 | A |
| PRY-03 | Read-only accounting-provider adapters. Per provider: resource list, auth model, the failure that ends onboarding, and the evidence that a voucher is unbooked. Sub-rows: **Fortnox** (invoices, supplier invoices, customers, suppliers, vouchers, accounts with VAT codes, company info, archive attachments; the per-customer integration licence and opt-in attachment/asset scopes); **Visma** (four registers plus vouchers/accounts, authoritative payment status, the split voucher reference, and the company-plan API-module failure that re-auth cannot fix); **Bokio** (separate credit-note resource that must be merged ahead of invoices to win first-seen dedupe, plus upload/receipt download joined through the human journal-entry number); **Björnlunden** (unpaged party arrays, server-rendered SIE export as raw bytes, per-company activation separate from a correct key); **Briox** (user-token exchange where refresh rotates both tokens); **Wint** (password exchange, never stored, both tokens rotate, no supplier register on the partner surface). | OPS | PRY-01, PRY-02, PRY-05 | B |
| PRY-04 | Resumable migration job: phases (discover, import, link, reconcile, settle, completed), per-resource **and per-part** cursors so one cursor can walk a split resource, leases and fencing, bounded retry, an issue taxonomy, and progress capped below complete because discovery has an unknown denominator. Bounded detail hydration reports a shortfall and exposes the unhydrated identifier set so "the provider reported none" is distinguishable from "we never asked". | OPS | PRY-01, PRY-02 | A |
| PRY-05 | Source-voucher reference normalization as the single join key between a provider document and the voucher the source booked it to, including the split series/number form and the "not booked" sentinel. Cross-provider shapes normalize to one value; an unreadable reference is null. Preserved rule: `R4`. | IMP | — | A |
| PRY-06 | Skatteverket skattekonto connection: per-company taxpayer consent, statement retrieval, the interest-accrual date carried separately from the display date, declaration status separating as-filed from decided, and a redovisare identity shared with the declarations it pays. When both a connection and a file import can write the same statement, dedup identity must partition them and promote a pending row over a booked one. | VAT | PRY-01, PRY-02, PRY-19 (`R3`) | B |
| PRY-07 | Skattekonto statement file import: the semicolon/quoted/BOM current export and the legacy text variant, opening and closing balance marker rows, whole-krona amounts, unreadable-row reporting, and a continuity check whose tolerance is explicit. | VAT | PRY-24 | B |
| PRY-08 | Bank statement format framework: an ordered registry with per-format detection and an explicit selection that never parses worse than auto-detection; encoding detection across UTF-16/UTF-8/Windows-1252/CP437 including canonical mojibake re-decode; per-format external-identifier derivation that keeps two identical same-day payments distinct; per-row currency; balance column and running-balance continuity; metadata-row skipping; Unicode-minus normalisation; per-currency totals; and the format adapters. | IMP | PRY-23 | A |
| PRY-09 | Nordic bank feed. The current feed profile is a non-Swedish aggregator exercised by an operator script. A Swedish feed requires a PSD2/aggregator profile with the same consent, cursor, replay and coverage evidence the existing connector already demands. | IMP | PRY-01, PRY-02 | B |
| PRY-10 | Central-bank rate feed plus the rate-date selection policy that makes it operable: exact-date request, and on no published observation a bounded look-back to the latest observation on or before the requested date, because rates publish on banking days only. A `null` answer is a valid answer and is persisted as an absent amount, never a fallback rate. Persist observation date, retrieval date, source and evidence per rate. | FX | PRY-01, PRY-02 | B, preserved rule `R7` |
| PRY-11 | EU VAT-number validation service with per-country format rules, a definitive-versus-unavailable distinction so an unavailable member state is never recorded as invalid, and the EU/non-EU country tables that decide whether reverse charge is permitted at all. | VAT | PRY-02 | B |
| PRY-12 | Peppol core: outbound invoice and credit note in the current BIS Billing profile with monetary totals derived so the business rules hold by construction, participant-identifier schemes, UN/ECE unit codes, tax-category and tax-scheme codes, the Swedish statutory notice strings, and the delivery state machine that separates submission, transport success and business acceptance. Inbound: archive the exact received bytes before any processing, read the document tolerantly, and refuse to create an intake item without the archived original. | COM, INT-1 | PRY-02 | B, `R21` |
| PRY-13 | Access-point transport adapter: recipient capability lookup, idempotent submission, webhook authenticity verification, and a provider-neutral transport contract so the access point is replaceable. Non-terminal versus terminal outcomes are distinguished and terminal failure is not retried blindly. | OPS | PRY-12, PRY-01 | B |
| PRY-14 | Email delivery adapter for invoices, reminders, payment confirmations, payslips and declarations: tracked send, per-recipient outcome without personal data in the status, a reply-to ladder that never uses a platform no-reply address, recipient limits, and template versioning. | OPS | PRY-01, PRY-02 | B |
| PRY-15 | BankID signing and submission authority, kept distinct from authentication. | OPS | PRY-01, PRY-14 | B |

## Swedish identifiers and payment primitives

Pure, dependency-free, high leverage. These gate payment files, tax-account settlement, ROT/RUT and the retained identity rules. **Nothing here needs a provider.** Preserved rules: `R1`, `R2`, `R3`, `R24`.

| ID | Deliverable | Owner | Prerequisite | Class |
| --- | --- | --- | --- | --- |
| PRY-16 | Check-digit and giro primitives: modulus-10 check digit and validation, bankgiro and plusgiro validation and formatting, and OCR reference generation and validation. One implementation, used by every caller. | FND | — | A, `R1` |
| PRY-17 | Swedish clearing and account checksum as a three-valued answer. An unrecognised clearing returns *no opinion*; a recognised clearing with a wrong check digit returns *invalid*. Used as a non-blocking hint only, because a passing check digit does not prove the account exists. | FND | PRY-16 | A, `R2` |
| PRY-18 | Domestic payment file: recipient validation that refuses by name rather than truncating when a field width cannot hold the account, the record layout and character set, and the separation between "instruction exported" and "accepted by the bank". | FND, COM | PRY-16, PRY-17 | B, `R24` |
| PRY-19 | Personnummer lifecycle: format validation including coordination numbers and the century/date offset, birth-date derivation where an age-dependent rule needs it, encryption at rest with a masked display form, and the twelve-digit *redovisare* reduction shared by every declaration and payment that identifies a taxpayer. | FND | PRY-16 | A, `R3` |
| PRY-20 | Currency registry and contract-layer typing: a validated currency reference with name, ordering and active flag, foreign keys from money-bearing records, and replacement of bare string currency fields in contracts with the domain currency types that already exist. Adding or deactivating a currency becomes data, not a migration. | FND | — | A |

## Source intake and migration

The target's SIE financial admission is already stronger than the reference. These packets close the tolerance, automation and reversibility gaps around it. Preserved rules: `R12`, `R13`, `R5`.

| ID | Deliverable | Owner | Prerequisite | Class |
| --- | --- | --- | --- | --- |
| PRY-21 | SIE record tolerance and a three-level severity model, so a renamed account does not render with the same weight as an unbalanced ledger. The standard records the reference accepts and counts must be accepted here rather than failing the whole file, and an unknown tag is informational unless it changes an amount. | IMP | — | A, `R12` |
| PRY-22 | SIE validation rules currently absent: per-voucher debit-equals-credit, fiscal-year record validity and its maximum span, a unique identity for vouchers whose number is blank, the reversal-record twin requirement, comma decimal separators, and an empty-file tripwire that distinguishes an empty ledger from a mis-decoded one. | IMP | PRY-21 | A, `R12` |
| PRY-23 | SIE encoding auto-detection by byte-range discrimination with a replacement-character retry across candidates, plus a mojibake tripwire that warns without blocking. Detection must not trust the encoding declared in the file header. | IMP | — | A, `R12` |
| PRY-24 | Account mapping suggestions against a versioned BAS reference chart: exact, name, class and range tiers with an explicit confidence and match type; group-header redirects; system-account exclusion; a pure preview of which target accounts will be created; and a statistics rollup. Mapping remains an operator decision, but a 400-account migration is no longer 400 blank decisions. | IMP | — | B, `R13` |
| PRY-25 | Chart effects: create mapped target accounts that are absent, rename from the file's own account names, carry the source's standard codes and account types, and derive per-account VAT treatment. Preserve the source's voucher-number series shape with the mapping retained as migration documentation, and post an explicit migration adjustment voucher that absorbs the imbalance from skipped or unmappable vouchers. Report which accounts had no mapping and how many vouchers each excluded. | IMP, VAT | PRY-24 | B |
| PRY-26 | Reversibility and breadth of SIE intake: compensating undo and replace with their own approval, multi-year files with a reviewed year/source partition, whole-dataset merge for preview, and dimension round-trip. Dimension-tagged lines currently fail the whole voucher; the target behaviour must be explicit loss diagnostics before admission, never silent loss. | IMP | PRY-21, PRY-22 | B |
| PRY-27 | Spreadsheet workbook reader for XLSX/XLS/ODS: encoding-aware decode, a best-sheet choice that does not assume the header sheet is first, and the type handling that stops a UTF-8 payload being read as a single-byte codepage. Every register importer below depends on this. | IMP | PRY-23 | A |
| PRY-28 | Register importers for articles, customers and suppliers, each with a scored column detector, encoding-tolerant value normalisation, and a per-register classification step. Supplier import must capture the domestic settlement fields the payment file needs. Party classification decides business versus individual and EU versus non-EU from the identifier itself. | COM | PRY-27, PRY-11 | B |
| PRY-29 | Opening-balance importer with two layout families, validation that rejects a profit-and-loss account as an opening and requires a balanced set, and a cascade that propagates a correction to every later fiscal year while preserving original descriptions, reporting periods it cannot change, and refusing to disturb a closed or signed year. Also names a detected bank format when the uploaded file is plainly a statement. | IMP, END | PRY-27 | B |
| PRY-30 | Source chart-of-accounts import, with the vendor format detected from the file rather than a user selection, per-account tax codes mapped to a treatment by **account number** and not by code alone, and a rejection that keeps a sales-box code off a balance-sheet account. Enrichment only: it must never be a precondition for admission. | IMP, VAT | PRY-27, PRY-24 | B |
| PRY-31 | Underlag attachment: read a source-system voucher reference out of a filename, join on the **importer's preserved** source series and number rather than our own voucher number, and scope every plan to one declared fiscal year because a filename carries no year. Plus post-hoc linking to an already-committed voucher, which must report per-file success or failure and never discard the user's files on a failure. | IMP | PRY-05 | A, `R5` |
| PRY-32 | Full-book SIE export for statutory delivery and for provider-served files, distinct from the existing movement-transfer export, with the dimension and object references round-tripping. | END | PRY-26 | B |

## Matching and reconciliation

The target's allocation, reversal, coverage and tax-account work is stronger than the reference and is not replaced here. The largest single omission is the covering set: a feed can deliver several business events as one row whose components are already booked, and a one-to-one matcher then reports an unexplained difference on money that is fully accounted for. Preserved rules: `R6`, `R10`, `R11`, `R14`.

| ID | Deliverable | Owner | Prerequisite | Class |
| --- | --- | --- | --- | --- |
| PRY-33 | Covering-set detection in the read path, plus a reviewed one-to-many confirmation that revalidates every leg at the moment of confirmation in the account's own currency. Deterministic exact-sum matching, smallest set first then nearest date, capped candidate pool. Restricted to accounts where a proposal can actually be confirmed. | IMP | — | A, `R6` |
| PRY-34 | Residual booking and difference decomposition: a selection that misses by a small amount books the remainder as its own voucher on the account with a per-kind expense/income account; the reported difference separates unmatched source from unmatched ledger and names what remains unexplained. An unconvertible ledger line yields "not reconcilable", not a fake number. | IMP | — | A, `R10` |
| PRY-35 | Ignoring an imported bank row as the legal escape hatch: it writes no voucher, so a closed period does not block it, and ignored rows are excluded from the account total but surfaced separately so they cannot manufacture a permanent difference. Deletion stays restricted to rows this system created. | IMP | — | A |
| PRY-36 | Unattended sweep as a per-cash-account job with a hard confidence floor, per-account failure isolation that fails closed on scope rather than degrading to a pooled run, both arrival orders (rows into a period that already holds vouchers, and vouchers into a period that already holds unlinked rows), a durable single-flight claim, and reporting that states an incomplete sweep is incomplete. | IMP | PRY-33, PRY-40 | A |
| PRY-37 | Reconciliation scope beyond the bank: every other material balance account reconciled against a specification the product already keeps or a balance the signer states, and multi-currency cash accounts reconciled in the account's own currency with unconvertible lines reported rather than converted. A year-end that reconciles only the bank account is not a year-end. | IMP, END | PRY-08, PRY-34 | B |
| PRY-38 | Sign-off semantics: a reconciled-through date rather than a period-wide attestation, an override that records the exact difference, reason and authority, reopening with actor and reason, supersession of a prior sign-off, an outside balance available only where an account has an outside truth, and distinct refusal reasons so the interface can name the remedy. | IMP, END | PRY-34 | A |
| PRY-39 | Already-explained detection as the single place that turns a detector's answer into a decision, so every door that books a bank row refuses, overrides and records identically. Override is honoured only when the caller echoes the exact set detected now. A bypass is written to immutable handling history. Detection failure is never a pass. | IMP | PRY-33 | A, `R11` |
| PRY-40 | Match confidence ladder with ordered passes, an auto-apply floor, and a mandatory downgrade to suggestion when a pass yields more than one equally valid candidate. Ambiguity is a distinct outcome, not a low score. | IMP | — | A, `R14` |
| PRY-41 | One comparability rule for every amount comparison across the matching surface: same currency compares raw magnitudes; different currencies compare only from stored conversions; **no stored conversion means not comparable**, and the candidate is excluded with a named reason rather than compared as a raw number. | IMP, FX | PRY-10 | A, `R10` |
| PRY-42 | Booking a bank row into a new voucher. Today a bank observation can only be matched to an already-posted line, so the ordinary loop of receipts arriving and being booked is outside the product model. This packet makes that loop a reviewed capability, or records the decision that it is deliberately out of scope. **The intent is currently unstated anywhere and must be settled, not assumed.** | IMP, COM | PRY-39, PRY-40 | A |
| PRY-43 | Receipt-to-bank-row matching with a date window wide enough for settlement lag, using the same comparability rule, so an expense claim can be evidenced by the card debit it produced. | IMP, VAT | PRY-41 | A, `R10` |

## Commerce and open-item registers

Existing commerce packets own invoice issuance, payment allocation, credits on the purchase side, collections records and register coverage. These packets add the document families and treatments that make the sales side legally complete. Preserved rules: `R15`, `R16`, `R21`, `R22`, `R23`.

| ID | Deliverable | Owner | Prerequisite | Class |
| --- | --- | --- | --- | --- |
| PRY-44 | ROT/RUT as an explicitly conditional sales and tax profile: qualifying customer, property and work facts; the deduction computed on labour cost **including** VAT with per-person annual ceilings; the deduction shown on the invoice; the split receivable between customer and authority on a dedicated account; the claim artifact and its schema version; rejection and adjustment; and settlement. A rejected claim is recovered from the customer or the receivable is stranded. Not applicable unless a dated company fact establishes it. | COM, VAT | PRY-19, PRY-47 | C, `R16` |
| PRY-45 | Customer credit note as a document with its own number series, its own mandatory-content list that deliberately differs from an invoice, reference to the original, negated lines that preserve the discount and the work classification so the face arithmetic still multiplies out, and cancellation of the original's deferral. | COM | PRY-48 | B |
| PRY-46 | Recurring invoice templates: versioned schedules with effective dates, pause and end state, stable occurrence identity, placeholder substitution at spawn rather than at save, a run-date grid that clamps to the last day of a short month, and a schedule edit that cannot leave a template with no lines. Template edits cannot change issued history and a replayed occurrence issues at most one invoice. | COM | — | A |
| PRY-47 | VAT rate families beyond the domestic standard: the reduced rates, exempt, domestic reverse charge, intra-EU goods and services, non-EU services and export, each with its rate, its reporting-box attribution, its statutory notice text stamped at issuance, and the per-line field that distinguishes where the transaction is performed from what the service is. Reverse charge requires a validated EU business identity, not a country code. | COM, VAT | PRY-11, PRY-55 | B, `R15` |
| PRY-48 | Mandatory-content gate at issuance: the seller's VAT registration number where the seller is registered, the required payment account, the required notices, and the per-document-type exemptions. The gate runs on the same path as booking, so a formally defective document cannot produce a defective input basis for the buyer. Plus the self-billed sale, where a counterparty invoices on our behalf and our own number series must not be consumed. | COM | — | B |
| PRY-49 | Statutory late-payment interest and the reminder fee as separate reviewed treatments: the published reference rate with its effective-date history, the statutory spread, the day-count basis, and a reminder fee booked as a receivable against the customer. Plus the dunning workflow: levels, per-recipient day thresholds, a company toggle with an explicit re-enablement checklist, and idempotent dispatch. Neither an interest charge nor a fee may be inferred. | COM | PRY-10, PRY-14 | B |
| PRY-50 | Cash method as a real profile: no receivable is booked on issuance, the settlement side of a voucher flips from the receivable account to a cash account and from the payable account to a cash account, the payment date becomes the sole year-end cut-off input, and an invoice that already has a voucher is not bookable again. Every surface must derive the flip from the one policy rather than deciding locally. | COM, END | — | B, `R23` |
| PRY-51 | Document-level exactness: öre rounding as a policy with the rounding delta carried on the document and cleared to a rounding account, a sub-unit settlement difference absorbed under a declared bound, unit codes from the international rec20 code list with a documented label mapping, and a per-line posting account restricted by account class so a line can never book to a cost, payroll or financial account. | COM | PRY-12 | B, `R22` |
| PRY-52 | Revenue deferral derived from an issued invoice, with a per-line service period and a balancing account, so a prepaid annual service invoiced in January is not January revenue. | COM, AST | PRY-45 | B |
| PRY-53 | Retained delivered bytes and a customer-facing artifact: the exact document bytes captured before any external send are the retained record, and a later re-render from current settings is a different document and must never be served as the sent one. Plus a customer statement artifact with a revocable scoped link, pinned to an as-of date, so a later payment changes the next statement without rewriting a prior one. | COM, OPS | PRY-14 | A |
| PRY-54 | Currency resolution on the invoice write paths: one resolver every write surface calls, refusing creation rather than persisting an absent rate, because a rate-less foreign purchase cannot be posted and a fabricated one produces a wrong return. The rate date anchors to the document date so money and voucher cannot sit on different days. A caller-supplied rate is honoured but refused when implausible, never silently replaced. | COM, FX | PRY-10, PRY-20 | B |

## VAT and tax-account profiles

| ID | Deliverable | Owner | Prerequisite | Class |
| --- | --- | --- | --- | --- |
| PRY-55 | Full reporting-box set with Swedish labels and the general indirect-tax formula, plus the account-to-box mapping used to cross-check a return against the ledger. Classification comes from the treatment, not from an account number alone; the mapping is corroboration. | VAT | — | B, `R15` |
| PRY-56 | Account VAT treatment taxonomy: domestic, reverse charge, export, intra-EU goods and services, non-EU, import, exempt, vehicle rental and mixed, each with rate derivation and account-class eligibility, and an explicit unsupported outcome that cannot fall back to ordinary domestic handling. | VAT | PRY-25 | B |
| PRY-57 | VAT period cadence and the filing record store: monthly/quarterly/yearly selection restricted to the most recent ended period, deadline-aware seeding, stepping past filed periods, the large-entity branch, marking filed, recording the external reference on acceptance, and unmarking. Preparation, submission and acceptance stay distinct. | VAT | PRY-82 | B |
| PRY-58 | Supplier line plausibility and Swedish VAT number: illegal-rate rows, unflagged foreign zero-rated rows, treatment-to-deductibility consistency, and construction of the company's own VAT registration number. | VAT | PRY-47, PRY-16 | B |

## Payroll and declarations

`PAY-01` through `PAY-06` and the supplemental expense handoffs remain the requirement owners. `apps/api/docs/PAYROLL-FOUNDATION.md` is four tables and four operations: an employee master with an effective-dated revision log, a sensitive-data grant, opening obligations, and an opaque work-input capture. **There is no pay-run record in the code or in any plan.** PRY-59 is therefore a prerequisite of the payroll family, not an enhancement to it. Preserved rules: `R8`, `R9`, `R17`, `R18`, `R19`, `R20`, `R21`.

| ID | Deliverable | Owner | Prerequisite | Class |
| --- | --- | --- | --- | --- |
| PRY-59 | Pay-run record and status machine (draft, review, approved, paid, booked, corrected), a frozen revision, the posting that binds an approved revision to expense and liability effects, and correction as a full reversal naming the original. A run is the object everything else freezes, approves, files against and recovers. | PAY | PRY-61 | B |
| PRY-60 | Calculation engine and a calculation-conventions object: the legally distinct cases (partial-month proration basis, sick rate, long-leave basis, leave context, net rounding, one-off-tax rounding) are named policy, not implicit code. Compute exact component breakdowns and independent control equations; never obtain an expected result by calling the production calculator. | PAY | PRY-59, PRY-61, PRY-62, PRY-63 | B, `R8` |
| PRY-61 | Statutory parameter table, versioned by year: base amount and income base amounts, the state income-tax threshold, contribution ceilings, the full contribution rate stack with its age and youth reductions and their caps, the pension-deduction ceiling, per-diem and mileage schabloner, meal and health-benefit values, and vehicle-benefit rules. Absent parameters block the affected calculation; they never default. | PAY | D-08 | B |
| PRY-62 | Tax table acquisition and selection: the published table set with a dated fallback, the column semantics including the column that varies year to year, and municipality resolution because the table number itself depends on the employee's registered municipality. Column selection is a per-employee legal fact. | PAY | PRY-61, PRY-19 | B, `R20` |
| PRY-63 | Employer contributions and the authority's own recomputation. The declared total must equal what the authority will actually draw: per-employee basis truncated to whole kronor, summed **per rate**, the contribution computed per rate on that sum with the öre dropped per rate, then summed. An öre-exact sum truncated once at the end drifts by kronor on any roster with öre-bearing wages. The same figure must appear in the declaration, the booked liability and the payment file. | PAY | PRY-61 | B, `R8` |
| PRY-64 | Vacation subsystem: the annual roll-forward and year-end settlement as a mandatory yearly procedure with a drift reconciliation against the booked accounts, a per-employee ledger of entitled, taken, saved and lost days with the multi-year expiry, the statutory and agreed pay rates as distinct rates, and the day valuation under both bases. A saved-day expiry must be able to force a payout. | PAY | PRY-59, PRY-66 | B, `R17` |
| PRY-65 | Absence subsystem: sick-pay periods with the waiting-period deduction taken once per period, the reduced-rate band, the transition day where the authority takes over, the calendar-day merge that decides when a new period begins, the long-leave calendar-day pricing rule where a full calendar month deducts exactly the monthly salary, and the parental/VAB reductions by child count. Plus a register lock so a run that has read a register refuses later writes to it. | PAY | PRY-59, PRY-66 | B, `R9` |
| PRY-66 | Work pattern: schedule-to-divisor conversion, degree-adjusted monthly salary applied by every consumer, a worked-days register with shift windows, and a shift premium engine with per-minute priority resolution so overlapping windows never double-count a total. | PAY | PRY-59 | B |
| PRY-67 | Benefits: valuation per type with the current generation of the vehicle-benefit rule and its year gate, standing monthly benefit rows derived into every run in range, and the co-payment rule that reduces a benefit's taxable value and is shared by the engine, the declaration and the annual report so the three can never disagree. | PAY | PRY-61 | B |
| PRY-68 | Register controls: year-to-date aggregates refreshed at approval and booking so a re-opened payslip shows the figures the issued document showed, the deviation period, standing per-employee lines, the manual line catalogue with its per-type tax and contribution flags, and the register write lock. | PAY | PRY-59 | B |
| PRY-69 | Special tax treatments: the adjustment decision, which is inert without **both** a percentage and a valid date interval and therefore needs a constraint rather than a convention; side-income tax; one-off tax grouped by rate before truncation; and the preliminary-tax status that changes both the deduction and whether contributions arise on gross. | PAY | PRY-61, PRY-62 | B |
| PRY-70 | Salary exchange into pension with its factor, its income and contribution threshold, and the employer pension cap; plus per-diem schabloner with the reduced-rate rule after a continuous period and its reset condition, meal deductions, and the separate mileage rates. | PAY | PRY-61 | B, `R18` |
| PRY-71 | Average number of employees as a time-weighted full-time equivalent across the fiscal year, with a manual override, because it is a required note and not a payroll total. | PAY, END | PRY-59 | B, `R19` |
| PRY-72 | Employer contribution declaration: the pinned schema version, the pre-flight validation profile, the correction identity that makes a resubmission a correction rather than a new declaration, the reporting period as the **paid** month rather than the earned month, per-employee absence rows with their field numbers, the individual and control totals, and a submission state machine keyed per period so a correction does not read the original's receipt. | PAY | PRY-59, PRY-63, PRY-65, PRY-19 | B, `R20` |
| PRY-73 | Annual-report underlag for the income statement: its own schema, per-employee annual totals, the required subtotals, and the penalty ladder. Distinct from the monthly declaration in every respect. | PAY, END | PRY-72 | B |
| PRY-74 | Payroll payment files: the domestic dialect with no service level and a single transaction-type code, the giro layout, the effective-net computation, per-employee bank-detail validation that refuses rather than truncates, exclusion of zero-net employees so bank details are never required for them, and a per-employee manual withholding override that shifts the payout and is reflected everywhere. | PAY, FND | PRY-18, PRY-59 | B, `R24` |

## Documents and evidence

Retention, source occurrence identity and review artifacts are owned and strong. What is missing is the ability to **read** a document and turn it into reviewable suggestions. Preserved rules: `R25`, and the `R12` severity model.

| ID | Deliverable | Owner | Prerequisite | Class |
| --- | --- | --- | --- | --- |
| PRY-75 | Document read pipeline: a text layer first and a model only for pages that need it, per-word bounding boxes, a scanned-page heuristic, image normalisation including the formats the platform cannot decode natively, office and rich-text conversion, and read lanes that treat a live document, a document tied to a voucher and a loose untyped document differently. | OPS | PRY-02 | A |
| PRY-76 | Extraction engine: **two independent readings in different tiers with different strategies, merged field by field**; per-document-type field schemas where an enumeration has no "unknown" member, so absent means the document does not say it; every value grounded to a page and a bounding box; per-field checks that send the failing field to a person without failing the document; and confidence that is never taken from the model. | OPS | PRY-75 | A, `R25` |
| PRY-77 | Classification taxonomy covering the finance-native document families including agreements, registrations, minutes and decisions, with a first-class "other" outcome that carries a suggested type so new classes are mined from what actually arrives; extraction provenance recording the parser and model version, the prompt digest and the outcome, so a re-interpretation can be shown to be the same interpretation; and a durable job queue with claim, backoff and attempt semantics. A person is never overwritten. | OPS | PRY-75 | A |
| PRY-78 | Page-text store and Swedish full-text search, with a multi-word query that retries as an alternation when the conjunction finds nothing, and a result that identifies which page a value came from. An archive whose contents cannot be found is not an archive. | OPS | PRY-75 | B |
| PRY-79 | Unlinked-evidence surface and upload path: a retained document reachable from nothing is a compliance gap and an accumulation problem, so the query must be scoped by a media-type allow-list of what an underlag may be rather than by filename exclusion, and must be survivable at production volume. Plus direct-to-storage upload with a short-lived signed URL, a server-side read-back that hashes what was actually stored, and browser-side image downscaling that stays a faithful reproduction. | OPS | PRY-75 | A |
| PRY-80 | Handling history for automated row completion: every record whose fields an automated writer filled records what was processed automatically, when, and by what, with a personal-data boundary, so the history answers the auditor's question. Applies to externally supplied suggestions as well as to internal writers. | OPS | PRY-76 | A |

## Deadlines, calendar and currency reporting

Obligation identity, outcome history and the revocable feed are owned. What is missing is date derivation, escalation and feed conformance. The dependency runs PRY-81 → PRY-82 → PRY-57: obligation derivation needs only the calendar, because the reporting cadence and the entity-size branch are a company fact and a dated rule rather than an implementation output, while the VAT filing store consumes the derived dates.

| ID | Deliverable | Owner | Prerequisite | Class |
| --- | --- | --- | --- | --- |
| PRY-81 | Swedish holiday calendar and banking-day arithmetic: the fixed days, the computable Easter-based days, the two movable days defined by week rather than by date, and the next-banking-day adjustment. Needed by deadlines, shift premiums and absence counting alike. | END | — | B |
| PRY-82 | Statutory obligation derivation: the deadline families with their real dates, including the entity-size branch, the monthly/quarterly/yearly VAT cadence, the contribution declaration, the withholding payments, the statistical returns whose deadline is a banking-day ordinal, the EU-law deadlines that do **not** shift, and deadlines derived from an assessment notice rather than a calendar. A revised rule creates review work and retains the prior basis. | END | PRY-81 | B |
| PRY-83 | Escalation and regeneration: a named due-soon threshold that turns a passive list into a work queue, an attention query split into due-soon and overdue, a recorded transition time, and regeneration of the horizon when a tax-relevant setting changes. A dismissed reminder still cannot fulfil the obligation. | END | PRY-82 | A |
| PRY-84 | Calendar feed conformance: display alarms at configurable offsets, a confirmed status for fulfilled obligations, a bounded date horizon, a description carrying the period and outcome so a subscriber can tell a filed obligation from an open one, feed expiry, and a per-token rate limit because the feed token is an unguessable bearer credential with no other control. | END | PRY-83 | B |
| PRY-85 | Honest partial totals: a foreign amount with no stored conversion is excluded from a book-currency total and **counted**, rather than summed in or silently dropped. Required before any per-currency register can be presented as reconciled. | FX, END | PRY-10, PRY-54 | A |

## Applicability gates

A packet is not activated by this backlog. Each of the following needs a dated company fact and a reviewer before its class-B/C parameter set exists; "not applicable" requires that fact, and "not implemented" remains a blocker while the capability applies.

| Gate | Blocks | Fact required |
| --- | --- | --- |
| D-04 | PRY-44, PRY-47, PRY-48, PRY-50, PRY-56, PRY-57, PRY-58, all of PRY-59 to PRY-74 | Legal entity, fiscal year, accounting and VAT methods, registrations, statement scope, payroll presence and prevalence, currencies in use |
| D-06 | PRY-03, PRY-04, PRY-06, PRY-08, PRY-30 | Which previous system, which version, which registers are complete, permitted data use, full-history versus reduced-history cutover |
| D-08 | PRY-10, PRY-11, PRY-12, PRY-49, PRY-55, PRY-61, PRY-62, PRY-63, PRY-70, PRY-71, PRY-72, PRY-73, PRY-81, PRY-82 | The applicable rule, chart, schema or table version, with provenance for every reused constant |
| D-10 | PRY-03, PRY-06, PRY-09, PRY-13, PRY-14, PRY-15 | Provider account, certificate, sandbox availability, the specific submission capability, and authorization to exercise it |

## What this backlog does not do

- It does not add packets to the mandated 53-packet index, change its dependency edges, or alter the delivery denominator.
- It activates no rule, rate, provider, XML schema, deadline or legal profile. Every class-B and class-C constant is a fixture until its dated source is acquired and versioned.
- It claims no implementation, runtime, company or external-acceptance status. A named reference module is evidence that a question exists.
- It adds no test or fixture change; test scope remains [D-09](../open-decisions.md).
- It does not replace an owned packet. Where a `PRY-nn` packet overlaps an existing one, the existing packet keeps the deliverable and this backlog records the missing rule.
- It does not adopt the reference's architecture, storage, tenancy or transport, and it does not adopt its float-based money handling.

## Preserved rule logic

The following logic was read in the reference and is worth keeping. Each entry states the class, so an implementer knows whether to port the algorithm, port only the shape, or re-derive the decision. **These are specifications for future implementation, not implemented behaviour and not verified results.** Where a value appears, it is a fixture that demonstrates the rule; it is not authority for the current period.

### R1 — Check digits, giro numbers and OCR references

Class **A**. Port as one implementation. Weight alternates 2, 1 from the rightmost digit; a doubled product above 9 has 9 subtracted; the check digit is `(10 - sum mod 10) mod 10`.

```text
function checkDigit(digits):
  sum = 0
  for position from rightmost to leftmost:
    weight = 2 if positionFromRight is even else 1
    product = digit * weight
    if product > 9: product -= 9
    sum += product
  return (10 - (sum mod 10)) mod 10

function validateWithCheckDigit(number):
  return length >= 2 and checkDigit(number without last digit) == last digit

validateBankgiro(digits):  7 or 8 digits and validateWithCheckDigit
validatePlusgiro(digits): 2 to 8 digits and validateWithCheckDigit
validateOcr(digits):      2 to 25 digits and validateWithCheckDigit

function ocrReferenceFrom(anyIdentifier):
  digits = identifier with all non-digits removed
  if digits is empty or longer than 24: refuse, return the input unchanged
  return digits + checkDigit(digits)
```

Refuse rather than repair. A generated reference that the payer cannot read is a payment that does not arrive.

### R2 — Swedish clearing and account checksum

Class **A**. Two structural families. A clearing number that is not mapped yields **no opinion**; it never yields *invalid*, because warning on a valid but unmapped account is worse than silence.

```text
weights11 = [1, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]   // last weight applies to the check digit

function mod11Valid(digits):
  if digits is empty or longer than 11: return false
  w = last 11 - length(digits) + 1 elements of weights11
  total = sum(digit[i] * w[i])
  return total != 0 and total mod 11 == 0

// Ordered resolution: exact-clearing exceptions beat ranges.
function ruleFor(clearing4):
  if clearing4 in {3300, 3782}:        return (family 2, variant mod10)
  if clearing4 in 1100..1199 or 1200..1399 or 1400..2099 or 2400..2499
     or 3000..3299 or 3410..3999 or 5000..5999 or 7000..7999 or 9400..9449:
                                       return (family 1, variant mod11-last10)
  if clearing4 in 4000..4999:           return (family 1, variant mod11-full)
  if clearing4 in 6000..6999:           return (family 2, variant mod11-9)
  if clearing4 in 8000..8999:           return (family 2, variant account+clearing mod10)
  return none                            // -> no opinion

function checksum(clearing, account):
  rule = ruleFor(first four digits of clearing)
  if rule is none: return UNKNOWN
  if account is empty or clearing shorter than 4: return UNKNOWN

  if rule.family == 1:
    if account longer than 7: return UNKNOWN
    full = clearing[0:4] + account left-padded with zeros to 7      // 11 digits
    input = rule.variant == mod11-last10 ? last 10 of full : full
    return mod11Valid(input) ? VALID : INVALID

  if rule.variant == mod10:                                     // 10-digit account
    if account longer than 10: return UNKNOWN
    return validateWithCheckDigit(account padded to 10) ? VALID : INVALID
  if rule.variant == mod11-9:                                   // 9-digit account
    if account longer than 9: return UNKNOWN
    return mod11Valid(account padded to 9) ? VALID : INVALID
  // account 6..10 digits mod10, plus a mod10 clearing when the clearing is 8xxxx
  if account shorter than 6 or longer than 10: return UNKNOWN
  accountOk  = validateWithCheckDigit(account)
  clearingOk = length(clearing) == 5 ? validateWithCheckDigit(clearing) : true
  return accountOk and clearingOk ? VALID : INVALID
```

A passing result is a hint that the number is well-formed. It is never evidence that the account exists at the bank, and it must not gate a payment without a separate authority decision.

### R3 — Taxpayer identity and the tax-account payment reference

Class **A** for the reduction, **B** for the giro destination. The reduction is shared: the payment that pays a declaration and the declaration itself must never disagree about who the taxpayer is.

```text
// Twelve-digit "redovisare" reduction.
function toRedovisare12(identifier, entityType):
  digits = identifier with separators removed
  if length == 12: return digits                       // already reduced
  if entityType is organisation:
     require length == 10
     return "16" + digits                              // 10 + the 12-digit prefix
  if length == 10:                                      // personnummer without century
     resolve the century and prepend it
  refuse otherwise

// Payment reference to the tax account: 12 digits + one check digit = 13.
function taxAccountPaymentReference(identifier, entityType):
  return toRedovisare12(identifier, entityType) + checkDigit(that)
```

Worked fixture: a ten-digit organisation number reduces by the `16` prefix, and the check digit is appended to give thirteen digits. The destination giro number is a dated external fact, not a constant to copy.

### R4 — Source voucher reference

Class **A**. The only safe join key between a provider document and the voucher the source booked it to. An unreadable reference is **null**, because a wrong link is written once and becomes räkenskapsinformation.

```text
pattern = /^(?:([A-Za-zÅÄÖåäö]{1,4})[\s-]*)?(\d{1,9})$/

function parseReference(value):
  if value is a number:  return integer and > 0 ? { series: null, number: value } : null
  if value is not text:  return null
  match = pattern against trimmed value
  if no match:           return null
  number = parsed integer of group 2
  if number <= 0:        return null
  return { series: group 1 uppercased or null, number: number }

function referenceFromParts(series, number):
  // the split form; a zero number means "not booked" in the source system
  number must be a positive integer, else null
  series is optional, trimmed and uppercased, else null
```

The importer renumbers per series but preserves this source pair. Join on the preserved pair, never on our own voucher number.

### R5 — Underlag filename reference

Class **A**. Receipts exported beside a statement are named after the voucher they belong to, so attachment needs no document reading at all. The design rule is that an unrecognised name returns null.

```text
// Optional leading noise: a year, or a word some exporters prepend.
yearNoise    = (?:(?:19|20)\d{2}[-_. ]+)?
// Alternation order matters: the longer word must precede its own prefix,
// or the short branch consumes the prefix and leaves a fragment for the
// series group to swallow as a series.
prefixWords  = "ifikation|ifikation..."   // full words, longest first
// A boundary assertion on the prefix is load-bearing: without it the engine
// backtracks into a shorter alternative and a word like "Verifikation"
// parses as prefix "ver" + "ifikat", leaving "ion" as the series.

function parseFileName(name):
  strip a known extension and any path; Chrome may deliver a relative path
  match, in order:
    series_number : <noise><word>?<series 1-4 letters><separator?><number 1-9>  -> both
    number_only   : <noise><word>?<separator?><number 1-9>                        -> no series
  no match -> null

// Never pre-select these in a bulk plan, even on a single candidate:
//   - a parse with no series, which could belong to any series;
//   - a reference on the collision list, where a short series is far more
//     often a paper size or a blankett than a voucher;
//   - a three-letter series, which is a camera or scanner prefix.
```

Every plan is scoped to one declared fiscal year, because source systems restart voucher numbering each year and a filename carries no year.

### R6 — Exact covering set

Class **A**. Several business events can arrive as **one** bank row whose components are already booked separately. A one-to-one duplicate check then finds nothing while the row is fully explained. An exact sum is a deterministic signal that needs no counterparty text, which is exactly what an aggregate giro row never carries.

```text
findExactCoveringSet(target, candidates, maxSize = 4, maxCandidates = 40):
  target = absolute value, in exact minor units; must be positive
  pool = candidates
           .filter(amount > 0 and amount <= target)
           .sort(by dateDistanceDays asc, then amount desc, then id asc)
           .take(maxCandidates)

  for size in 1 .. min(maxSize, length(pool)):
     best = null                                   // { indices, totalDistance }
     walk(start, remaining, distance):
        if chosen == size:
           if remaining == 0 and (best is null or distance < best.distance):
              best = { indices: chosen, distance }
           return
        slotsLeft = size - chosen
        for i in start .. length(pool) - slotsLeft:      // leave room to complete
           if pool[i].amount > remaining: continue
           // Nothing smaller than the remainder can complete the set while
           // filling the last slot: skip instead of descending.
           if slotsLeft == 1 and pool[i].amount != remaining: continue
           walk(i + 1, remaining - pool[i].amount, distance + pool[i].dateDistanceDays)
     walk(0, target, 0)
     if best is not null: return pool[best.indices]
  return null
```

Ordering is smallest set first, then nearest in date. The candidate pool is capped **before** the search so a busy account cannot make the combinatorics unbounded. The result is a **proposal**: it is revalidated leg by leg, in the account's own currency, at the moment of confirmation. A proposal that cannot be confirmed is worse than no proposal, so restrict the whole capability to accounts where it can be.

### R7 — Reference-rate retrieval ladder

Class **B**. The shape is reusable; every series identifier, endpoint and the look-back window are dated external facts.

```text
resolveRate(currency, rateDate):
  if currency is the book currency: return rate 1, no observation, no cache write

  1. read-through cache on (currency, rateDate); best effort, never throws
  2. request the exact day
     - 429 or 5xx even after one retry: STOP. Do not fire the range request;
       it would hit the same limiter and turn one throttle into two.
     - 204, empty or 404: no observation for this exact day. Rates publish on
       banking days only, so this is the ordinary weekend and holiday case.
  3. bounded look-back range request [rateDate - N days, rateDate], take the
     LAST element: the latest observation on or before the requested day
  4. persist the observation with its own observation date, the requested date,
     the source and the retrieved evidence
  5. on failure: fall back to the most recent cached observation on or before
     rateDate, else return no rate

no rate is ever synthesised. A caller persists the amount without a converted
value and repairs it later; a fallback constant is display-only and must never
reach a posted amount.
```

The look-back is what makes a real deadline calendar operable: "the rate **for** date D" is not "the rate **published on** date D". Without a look-back rule, every deadline landing on a non-banking day has no usable rate.

### R8 — Employer contributions as the authority recomputes them

Class **B** for the rates, **A** for the aggregation order. The aggregation order is the whole point: the declared total must equal what the authority draws.

```text
// Order: truncate per employee -> sum per rate -> compute per rate on that
// sum with the fraction dropped per rate -> sum the rates.
function declaredContributions(rows, rateStack):
  cells = empty map keyed by (category, rate)

  for each row:
     basis = truncateToWholeKronor(row.basis)      // once, per employee
     cells[(row.category, row.rate)].basis += basis

  total = 0
  for each cell:
     cell.amount = truncateToWholeKronor(cell.basis * cell.rate)
     total += cell.amount
  return { cells, total }
```

Worked fixture that shows why the order matters: four hourly employees at an amount carrying öre produce one total when each is computed and rounded individually, and a total one krona different when the basis is summed first and truncated once. The second number is what the authority uses. The declaration, the booked liability and the payment file must all carry it, so this is one function with three callers, not three calculations.

Two approximations are acceptable only if they are declared and bounded to kronor scale: truncating the summed per-employee basis once rather than summing per-field truncated values, and truncating per category-and-rate cell rather than per global rate. The second keeps the category breakdown cross-footing exactly against the total.

### R9 — Sick-pay period

Class **B** for the rates and day counts, **A** for the period structure. A new period starts only after the merge window; within one period the waiting-period deduction is taken **once**.

```text
function sickPay(monthlySalary, sickDays, config, withinMergeWindow, dailyDivisor):
  dailyRate   = roundToOre(monthlySalary / dailyDivisor)      // divisor from the schedule
  weeklyRate  = roundToOre(monthlySalary * 12 / 52 * sickRate)

  karensavdrag = withinMergeWindow ? 0
               : roundToOre(weeklyRate * waitingDeductionFactor)

  // Day 1 is the waiting day unless the period was continued. The employer-paid
  // band is the days after it, capped; beyond the cap the authority pays.
  paidDays = clamp(sickDays - (withinMergeWindow ? 0 : 1), 0, employerPaidDayCap)
  sickPayAmount = roundToOre(dailyRate * sickRate * paidDays)

  // The net reduction is what the employee actually loses against normal pay.
  totalDeduction = roundToOre(dailyRate * sickDays) - sickPayAmount + karensavdrag
  return { karensavdrag, paidDays, sickPayAmount, dailyRate, weeklyRate, totalDeduction }
```

Return the intermediate steps with their formulas. An explainable payroll line is reviewable; a total is not. The merge window, the cap, the rate and the reduction factors are dated facts, and the paid band must also raise the authority-reporting flag on the day the employer stops paying.

### R10 — Amount comparability, and residual booking

Class **A**. One rule, stated once, used by every amount comparison on the matching surface.

```text
function comparable(left, right):
  if left.currency == right.currency:
     return compare magnitudes directly                 // exact, needs no rate
  convertedLeft  = storedConversion(left)
  convertedRight = storedConversion(right)
  if either conversion is absent:
     return NOT_COMPARABLE                            // exclude the candidate,
                                                    // never compare as raw numbers
  return compare both in the book currency

function amountVarianceWithin(left, right, tolerance):
  result = comparable(left, right)
  if result is NOT_COMPARABLE: return not applicable
  return abs(converted difference) <= tolerance
```

A tolerance band expressed in one currency and applied to a column in another is off by orders of magnitude: it either selects nothing or selects an unrelated row. A band around a foreign figure applied to a book-currency column can make a foreign invoice "exactly match" a local receipt. The excluded candidates are **returned with a named reason** so the interface can point at the repair rather than silently dropping them.

Residual booking uses the same discipline. When a selection misses by a small amount, book the remainder as its own voucher on the cash account with a per-kind expense or income account, anchored to the first row through its existing link, and refuse on a zero residual, an implausibly large residual, or a residual in the wrong direction.

### R11 — Already-explained override binding

Class **A**. Every door that books a bank row refuses, overrides and records through this one decision, or a guard that lives in one door only will eventually be bypassed by another.

```text
function guard(detectedNow, callerIntent):
  match detectedNow:
    none:                                   return CLEAR
    found and not callerIntent.force:       return BLOCKED(set)
    found and force and callerIntent.expectedIds == ids detected NOW:
                                            record the bypass in handling history
                                            return OVERRIDDEN(set)
    found and force but ids differ:         return BLOCKED, force rejected
    detector failed and force:              return CHECK_FAILED   // never a pass
    detector failed and not force:          return CLEAR           // fail open;
                                               the caller logs and surfaces it
```

The binding is the point. An approval issued **before** another voucher was posted must not authorise committing against the changed state, and an automation must not be able to sweep through an override without ever consulting the vouchers. A bypass is written to immutable handling history — including the case where the guard found nothing, because "the guard found nothing at that moment" is itself the fact an auditor needs.

### R12 — Intake tolerance, severity and voucher balance

Class **A**. Intake diagnostics need three severities, not two, and the reference's accepted-record set is the minimum.

```text
severity: ACTION   a renamed account      // one line on screen, at most
         NOTICE   an unbalanced ledger
         INFO     an unrecognised or unsupported record

// Unknown or not-yet-supported tags are INFO and are counted. They do not
// fail the file. The standard records to accept and count include the
// opening/closing balance markers, the checksum, the tax-rate summary,
// the accounting year, the period set, the budget/balance projections and
// the per-object balance markers.
accept and count; INFO: "balances per object are not supported yet"

// Per voucher, on block end:
reportMissingReversalTwin()
if abs(sum of voucher amounts) > tolerance:
     severity ERROR, locator = the voucher reference
```

Other rules in the same family, all class **A**: a fiscal-year record must have valid dates with the end not before the start and within the statutory maximum span; a voucher whose number is blank needs a unique **per-file** identity rather than a shared placeholder, or two such vouchers collide and the whole admission is refused; a reversal record must have an identical twin and its absence is reported; amounts accept a comma decimal separator; and a file whose control records are present but whose vouchers parsed to none raises a separator-or-encoding tripwire rather than an empty import.

Encoding detection is class **A** and never trusts the file's own header: discriminate by byte range across the candidate encodings over the whole buffer, then retry across candidates when a replacement character appears. A mojibake tripwire **warns and never blocks**, because the failure it detects has already reached posted entries elsewhere.

### R13 — Account mapping confidence

Class **B** for the reference chart, **A** for the tiering. Mapping stays an operator decision; the point is that the operator is shown a proposal with its basis.

```text
tiers, highest confidence first:
  exact account number in the reference chart
  exact account name
  account class / BAS range fallback            // lower confidence, stated
  group-header redirect
  never: system accounts outside the chart's own numbering

report per account: match tier, confidence, and the reference name
report totals: counts and mean confidence per tier, plus the manual remainder
preview, without writing: which target accounts will be created, and the names
                         the import will apply to existing ones
```

Every referenced account must still be mapped before admission. The suggestions change the effort, not the authority.

### R14 — Match confidence ladder

Class **A** for the ordering and thresholds, **B** for what each tier is allowed to decide. Thresholds are policy and must be recorded as such, with the observed false-positive rate as the thing that moves them.

```text
passes, in order:
  payment reference / OCR exact, against the document's own reference
  exact amount plus a matching giro or clearing identifier
  exact amount inside a window around the document dates
  fuzzy amount plus counterparty text in the description

auto-apply  : passes at or above the apply floor
suggestion  : passes between the suggestion floor and the apply floor
ambiguous   : a pass that matches MORE THAN ONE candidate in its window
```

**Ambiguity is a distinct outcome, not a low score.** A pass that finds two valid candidates is downgraded to a suggestion, never auto-applied, because auto-matching is the labour-saving core of reconciliation and an ambiguity downgrade is what stops it clearing the wrong receivable. Do not add a fuzzy pass to a payout family where the payer pays an exact decided sum.

### R15 — VAT reporting boxes and the account cross-check

Class **B**. The box set, the labels, the account mapping and the general formula are dated external facts. The current implementation computes a small subset and pushes an explicit blocker for the rest, which is honest; the packet is to make the rest implementable.

```text
// Shape only. Every box, label and mapping below is a dated acquisition.
output boxes:
  the domestic standard-rate output box, its domestic input box,
  the import box, and the investment-return box
general investment-return box:
  = sum(its declared component output boxes) - the investment-return box
  // when every component box is declared; otherwise refuse and name the
  // missing components rather than reporting a partial box as complete

// The account cross-check is corroboration, never the source of the
// classification: a treatment plus an account's role determine the box.
```

A return that cannot name its own missing box components is not a return. The blocked case must stay blocked until the corresponding account treatment and rate family exist.

### R16 — ROT/RUT receivable split

Class **C**. This is a legal eligibility judgement with a dated authority, and it applies only to a company with the qualifying facts. The structure is recorded so the decision is visible once eligibility is established.

```text
deduction basis   = qualifying labour cost, and the rate applies to the labour
                    cost INCLUDING VAT, capped per person per year
invoice gross      = the amount the customer pays, with the deduction shown
                    on the document as a reduction
customer receivable = gross - deduction
authority receivable = the deduction, on a dedicated skattereduktion account,
                    NOT netted against the customer
amounts            = truncated to whole kronor; the truncation remainder stays
                    on the skattereduktion account and is attributable to the
                    authority only when it is smaller than one kronor
settlement         = one transfer may settle several claims
rejection          = the refused share moves from the reduction account to the
                    customer receivable and the invoice reopens
```

The customer and the authority are **both** debtors on this invoice. Treating the reduction as a discount strands the receivable permanently when a claim is refused. Reversal mirrors the rejection exactly.

### R17 — Vacation roll-forward

Class **B**. A mandatory yearly procedure, not a payroll total.

```text
for each employee:
  entitled      = statutory entitlement for the employment, by the retained basis
  taken, saved  = from the retained ledger
  unused        = entitled - taken - saved
  // days unused beyond the statutory carry-over window expire
  expired       = saved days past the expiry horizon
  forcedPayout  = days that must be paid out, including the expired ones
  payoutValue   = forcedPayout valued under BOTH bases:
                    - the daily-rate basis, and
                    - the percentage basis at the employee's own rate
  choose        = the company's declared basis, recorded once

reconcile against the booked accounts:
  drift = booked balance - the balance this computation implies
  post ONE adjustment voucher when |drift| exceeds the declared tolerance
  never distribute the drift silently across employees
```

The statutory pay rate and the agreed pay rate are **different rates** and must not be one field. A full carried-over balance expiring forces a payout that no payroll run would otherwise produce.

### R18 — Per-diem reduction rule

Class **B**. Every amount is a dated schabloner; the reduction rule is the reusable part.

```text
perDiem(days, consecutiveDays, hadBreakOfAtLeastTheDeclaredLength):
  if not hadBreak:
     if consecutiveDays beyond the first period:  rate *= reductionFactor1
     if consecutiveDays beyond the second period: rate *= reductionFactor2
  meals: deduct the declared share of the schabloner per meal present
         (breakfast, lunch, dinner, and the combined shares)
```

A continuous stay reduces; a sufficiently long break resets the count. Getting the reset wrong over-charges the company for a trip that was interrupted.

### R19 — Average number of employees

Class **B**. A required note, computed as a time-weighted full-time equivalent across the fiscal year.

```text
for each employment:
  months = overlap(months in the fiscal year, employment start, employment end)
  contribution = months * employmentDegree
average = roundToWholeEmployees( sum(contribution) / 12 )
manual override is permitted, is recorded, and is visible as an override
```

Note the denominator is the fiscal year, not the calendar year, and the rounding is to whole employees.

### R20 — Declaration correction identity and reporting period

Class **B**. Two rules that are easy to get wrong and expensive when wrong.

```text
// Reporting period is the PAID month, not the earned month.
reportingPeriod = year and month of the payment date
// The earned month is retained separately. A correction that changes the paid
// month moves the reporting period with it.

// Correction identity.
if resubmission carries the SAME specification number as a prior submission
   for that period -> it is a CORRECTION of that declaration
if it carries a DIFFERENT one                          -> it is a NEW declaration
// A correction must therefore reuse the number, and a period-keyed state
// machine must resolve the ORIGINAL's receipt, not the correction's.
```

Without the reuse rule the authority cannot distinguish a correction from a fresh filing, and a correction silently becomes a second declaration. Without the paid-month rule the declaration lands in the wrong period. Absence rows are per employee, per date, per specification number, and carry the distinguishing field for the two absence kinds.

### R21 — Peppol monetary totals

Class **B**. Derive the totals so the business rules hold by construction rather than validating them afterwards.

```text
// Allowance/charge lines reduce the line total and carry a reason code;
// a line-level discount is a document allowance, not a negative line.
payableRounding = displayed document total - the sum of its line totals
                  // non-zero only when oere rounding is enabled
payableAmount   = sum of line totals + payableRounding
// Invariant: the tax subtotal equals the sum of its category subtotals, and
// payableAmount equals the tax-subtotal total plus payableRounding.

// Two tax schemes are distinguished on the document: one for VAT and one for
// the income-tax registration statement. A registered seller states its
// registration number; the document carries the statutory notice text for the
// treatment, and the notice is compared byte-for-byte at render.
```

A document whose printed total differs from the sum of its lines is formally defective, which is why the rounding delta is carried explicitly rather than absorbed.

### R22 — Öre rounding and the rounding account

Class **B** for the policy, **A** for the mechanics.

```text
policy: enabled by default; a per-document override beats the company setting
roundingDelta = the displayed document total - the raw computed total
  // per document, not per line, and not distributed across lines
amountToPay   = displayed total - any reduction shown on the document

settlement: a sub-unit difference between the allocation and the outstanding
            balance is settled in full when within the declared bound, and the
            residual is booked to the rounding clearing account
```

The residual must land on a real account. A difference absorbed silently leaves the cash account permanently off by a fraction that no later transaction will explain.

### R23 — Cash-method settlement side

Class **B**. One policy, read by every surface, because the reversal-side flip is exactly the kind of rule that double-books costs when each surface decides locally.

```text
under the cash method:
  on issuance        : no receivable is booked; recognition happens at payment
  on payment         : debit the cash account, credit revenue and output tax
  the settlement side of a customer voucher flips from a receivable credit
                        to a cash debit
  the settlement side of a supplier voucher flips from a payable debit
                        to a cash credit
  the payment DATE, not the invoice date, is the year-end cut-off input
  an invoice that already has a voucher is not bookable again
```

### R24 — Payment file field widths and effective net

Class **B** for the layout, **A** for the refusal. The refusal is the reusable part.

```text
// A recipient whose account cannot be represented in the target field is
// REFUSED BY NAME. It is never truncated: a truncated account is a valid-looking
// payment to a different beneficiary, and a giro record field is a fixed width.
function fitsTargetField(account, fieldWidth): boolean
  return length(account) <= fieldWidth

// Effective net: what actually leaves the bank.
net = gross
    - employeeWithheldTax
    - otherDeductions
    + adjustments
round the net once, under the declared rounding direction
employees whose effective net is zero are EXCLUDED from the file, so no bank
  detail is required for them and no zero-amount instruction is emitted
a zero-amount run posts nothing
```

A per-employee manual withholding override shifts the payout, and every downstream artifact — the run, the file, the declaration — must carry the same effective net.

### R25 — Extraction by double reading and per-field merge

Class **A**. The reusable insight is that a single extraction pass is a single point of failure, and that a document is not accepted or rejected as a whole.

```text
// Two independent readings, in different tiers, with different strategies.
reading1 = extract(document, tier = fast,  strategy = layout_heuristics)
reading2 = extract(document, tier = deep,  strategy = full_page_reasoning)
// merge FIELD BY FIELD, never document by document
for each field in the document type's schema:
   if the readings agree:            value = agreed value, confidence = agreed
   if they disagree:                 value = null, reason = disagreement
                                    // a disagreement is a review item, not a value
   if only one reading produced it:  value = that value, confidence = single_source

// An enumeration member has NO "unknown" option. null means the document does
// not say. Do not widen an enum to make a parse succeed.

// Ground every accepted value to a page and a bounding box, from the word
// boxes the read layer produced. A value with no location is not reviewable.

// Per-field checks, each sending ITS OWN field to a person and never failing
// the document:  required, identifier checksum, non-negative, percent in range,
// date ordering, and an audit plausibility check.
// A failed check revokes that field. It does not revoke the document.

// Confidence is derived from agreement and checks. The model's own stated
// confidence is never asked for and never stored.

// A re-extraction keeps the previous interpretation and its review lineage.
// It may supersede a stored reading only when nothing changed since it was
// read, and it may never silently revise an accepted record.
```

Human review is mandatory before acceptance. A sender, a filename or an instruction inside the document grants no authority.

## Maintaining this document

Add a packet when a comparison finding has no existing owner, and record the outcome as owned, supplemental or unowned. Change a preserved rule only through the ADR that governs it, and update the affected requirement and proof gate together. When a packet completes, replace its scope with what was actually built and where the evidence lives; a delivered packet is not a verified one.

Run `python3 docs/plans/check-plan.py` after any change to this directory. It validates links, anchors, whitespace and the mandated index; it does not execute product tests and it does not see these supplemental packets.
