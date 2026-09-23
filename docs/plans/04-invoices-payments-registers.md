# Invoices, payments and business registers

Owner: commerce domain and its contracts/UI. Phase: P2 for imported open-item controls; P5 for complete native commercial workflows. Reuse kernel plans, approvals, receipts, source occurrences and correction machinery. Commerce owns invoice/open-item↔payment allocation capacity; reconciliation owns bank-observation↔posted-line capacity.

## User results and scope

Create or retain an invoice, issue/recognize it under a selected accounting method, receive or make partial/batched payments, resolve credits and owner-paid expenses, and prove the commercial balances against the ledger. A commercial document can exist without immediate GL recognition under a cash-method profile. “Issued,” “recognized,” “settled” and “delivered” are independent facts.

The scope includes customers/suppliers, evidence-backed sales/supplier invoices, line discounts and charges, credit notes, open items, payments, refunds, prepayments/overpayments, owner reimbursement and control reports. Product catalogues may supply draft defaults but never rewrite issued invoice facts. Bank execution and invoice/email delivery are external side effects with separate authorization/outcomes.

## Owned model

| Record                 | Required fields / invariants                                                                                                                                                                                                        |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Party revision         | Stable party ID; legal identity, addresses, tax identifiers, contact/payment details, evidence and effective dates. Invoice snapshots retain the revision used. Changed bank details invalidate dependent payment approval.         |
| Invoice revision       | Direction, party revision, original/our legal document number, source occurrence/evidence, document/supply/due dates, original currency/scale, line quantities/prices/discounts/charges/treatments, exact totals and rule versions. |
| Issue/acceptance event | Immutable invoice revision and identifier, actor, time and validation/authority basis. Native sales number allocated transactionally; supplier number remains its original source fact.                                             |
| Open item              | Invoice/credit/prepayment identity, commercial currency amount and due basis; recognition state and links separate from settlement state.                                                                                           |
| Recognition link       | Event/purpose/occurrence and voucher lines carrying initial/year-end/subsequent recognition, with accounting method revision. Never infer recognition solely from invoice status.                                                   |
| Payment event          | Independent provider/bank/source identity, gross cash/principal/fee/FX facts, currency/date evidence, voucher reference and uncertainty state.                                                                                      |
| Allocation             | Payment/credit/open-item leg, exact amount in relevant currencies, conversion basis, ordinal, source/destination capacities and reversal link.                                                                                      |
| Register control       | Immutable snapshot of open items, recognition/allocation effects, GL cutoff and reconciliation differences.                                                                                                                         |

Supplier invoice-number duplicate detection is scoped to the identified supplier and entity with source context. It can flag ambiguity; it must not destroy distinct legitimate documents or merge different suppliers. Once issued/accepted, economic document content is immutable; revisions of a draft are editable until sealed, then supersede rather than mutate a reviewed revision.

## Calculation and recognition

Calculate quantity × unit price, discounts, charges, taxable basis and tax using exact decimals and a named rounding policy. Store source amounts and calculated amounts separately with a reconciliation result. A discrepancy is reviewed, not hidden in a balancing plug. Shipping/fees and per-line discounts participate in the same amount model used by the document, ledger proposal, tax facts and report.

| Profile / event             | Planned accounting behavior                                                                                                                                                                                |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Accrual invoice             | On the reviewed recognition event, recognize receivable/payable and revenue/expense/asset/tax under the activated treatment. Payment settles the open item without re-recognizing the same supply.         |
| Cash-method invoice         | Retain the commercial open item; recognize only at the profile's supported trigger. At year-end, explicitly recognize eligible unpaid items. Later payment links to and settles that existing recognition. |
| Historical imported invoice | Retain source asserted state and known recognition/payment links. Missing chronology remains unknown; do not synthesize dates or double recognize.                                                         |
| Advance / deposit           | Separate liability/asset/open item and applicable tax timing under a reviewed treatment; not ordinary invoice recognition by default.                                                                      |
| Owner-paid expense          | Recognize cost/asset/tax and liability to owner; company reimbursement settles the liability. Evidence ties the two events without counting expense twice.                                                 |

No profile is selected from a bank amount, turnover guess or convenience. Cash-method timing, credit allocation, tax deductibility and other legal rules are activated through the rule/profile gate. Unsupported mixed/industry treatments block that invoice's recognition while allowing evidence retention and review.

## Operations

New scoped resources are `parties`, `invoices`, `open-items`, `payment-events`, `payment-allocation-plans` and `register-snapshots`. Typed operations create/revise drafts, validate/seal issue or acceptance, prepare recognition, prepare credit/refund, prepare owner expense/reimbursement, prepare/approve/execute allocations, inspect residuals, and produce controls. The operation result names whether it only retained a document, issued it, posted accounting, recorded an allocation or admitted external delivery.

Issuing a native invoice allocates its number, records immutable revision and any immediately required posting/register effects in one transaction when they form one approved group. The group approval must include both commercial-issue and posting authority where required. Document rendering/delivery follows from the resulting immutable revision through the outbox; a failed email does not issue a second number or post another invoice.

Supplier acceptance preserves the supplier's legal number and creates our internal identity without pretending we issued it. Invoice recognition uses the same economic event identity even if the source document is reparsed. Accepted historical invoice records must link to already imported vouchers or a declared unresolved recognition state.

## Payments and conservation

Under a lock, each allocation checks immutable gross capacity and previous effective allocation/reversal legs. Payment amount equals applied principal plus explicit fees/FX/residual held as unapplied cash according to the selected treatment. Invoice settlement cannot exceed its remaining capacity; a surplus creates an explicit customer credit/deposit rather than a negative residual disguised as “paid.” Partial settlement leaves a visible residual and does not change original due/issue evidence.

One payment can cover several invoices, and one invoice can have several payments. Each batch has deterministic allocation order/residual handling and a sealed result. Cross-currency allocation preserves invoice-currency amount, payment-currency amount and book-currency carrying-value release with an explicit realized FX effect. Do not force all three totals into one scalar field.

A credit note links to the original invoice and its treatment, with its own legal/document identity. Allocation of a credit, repayment of an overpayment and reversal of a mistaken payment are distinct operations. Their register and journal effects commit together. Generic voucher deletion cannot leave a paid invoice or expense claim behind.

Actual bank-payment initiation requires payment authority, verified payee revision, exact artifact/instruction identity and provider result tracking. An exported payment file is not a bank payment. A bank row can provide settlement evidence, but matching it to a GL line does not itself allocate it to an invoice.

## UI and controls

The invoice view shows original evidence, party snapshot, exact amount derivation, issued revision, recognition links, allocation history, residual by currency and delivery/provider state. Lists distinguish draft/issued/recognized/partially settled/settled/credited/disputed without collapsing independent statuses into a misleading single lifecycle.

Payment review shows payee changes, all allocation legs, unapplied remainder, fees, exchange basis and approval scope. Register reports reconcile receivables/payables, cash, owner liabilities and relevant tax/control accounts. Ageing uses an explicit as-of date and historical allocation cutoff, not today's mutable status. A missing recognition/payment link is a named discrepancy; it cannot be solved by toggling paid status.

## Delivery packets

| ID     | Deliverable                                                                                         | Depends on     | Acceptance                                                                                                                |
| ------ | --------------------------------------------------------------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------- |
| COM-01 | Party and invoice revisions, evidence, exact line/totals model and duplicate diagnostics.           | IMP-01, FND-03 | E-02/E-12: per-line discount/charge survives; source amount mismatch blocks; supplier identities remain distinct.         |
| COM-02 | Issue/acceptance and accrual/cash-method recognition profiles with transactional numbers and links. | COM-01, PST-03 | E-03/E-05/E-14: issue replay once; imported/year-end recognition not repeated on payment.                                 |
| COM-03 | Payment events, partial/many-to-many allocations, residual capacity and refunds.                    | COM-02         | E-08/E-13: concurrent allocation cannot overconsume; payment/register/voucher effects roll back together.                 |
| COM-04 | Credits, owner-paid expenses/reimbursements and domain-specific corrections.                        | COM-03, COR-02 | E-09/E-13: immutable issued facts, exact net effects and no phantom paid/owed register state.                             |
| COM-05 | Invoice/payment artifacts and separately authorized external delivery.                              | COM-02, OPS-03 | E-08/E-19: delivery retry does not duplicate issue; exported versus provider-paid state remains distinct.                 |
| COM-06 | Historical open-item admission, ageing and register↔GL control snapshots/workbench.                 | COM-03, IMP-02 | E-12/E-15: source balances, retained matches and recognition links reconcile; unknown chronology blocks derived postings. |

COM-03 first supports same-currency conservation. Cross-currency acceptance additionally requires FX-02; the invoice/payment APIs expose unsupported-currency blockers until then. COM-06 can reconcile historical controls before connected delivery is available. Company release requires whichever branches its inventory actually contains.

## Bounded register-control snapshot slice

The [register-report handoff](../../apps/api/REGISTER-REPORTS.md) describes an implemented-source COM-06 subset over existing synthetic registered recognition and applied payment legs. It freezes current-known invoice revisions, due-date ageing, economic-date allocation identities and all journal contributions for declared commerce control accounts. Nonzero unexplained contributions remain differences even if they offset. Capture is bounded and fails rather than truncates; saved reports can be rediscovered and downloaded.

This is not historical invoice admission, reconstruction of facts known on a past date, company source completeness, native invoice issue, delivery or payment initiation. `coverage: not_established` remains explicit. Shared integration and real runtime/browser/independent-arithmetic evidence remain gates; the source alone does not complete COM-06 acceptance.

## Bounded native customer commercial drafts

The [invoice-draft handoff](../../apps/api/INVOICE-DRAFTS.md) implements a COM-01 subset: operator-scoped unissued drafts, retained asserted seller/customer identities and counterpart revisions, exact explicit line amounts with discounts/charges, unknown tax propagation, source/calculated comparisons, and immutable revisions guarded by expected revision/digest. Complete bounded read/history/list paths and a local edit/reopen/recovery UI are included in source.

This does not establish legally active VAT/rounding profiles, verified legal identity, supplier-document duplicate handling or source-occurrence admission. Saving a draft neither issues a number nor writes the ledger/open-item register. The bounded synthetic issue subset below adds sealing, issue/recognition approval and atomic effects. Legal profiles, rendering and authorized delivery remain COM-02/COM-05 dependencies. The user stopped tests and validation runs during this packet; no runtime, browser or financial verification claim is made here.

## Bounded synthetic issue and recognition

The [invoice-issuance handoff](../../apps/api/INVOICE-ISSUANCE.md) records forward1400 and its shared API/read-capability/UI integration. A current operator reviews an exact draft revision and explicit accounts, approves, then atomically commits kernel recognition, an internal SYN number, customer registration and an immutable issue receipt. Owned retained evidence cannot be posted separately merely by changing its event key. Issued draft heads are frozen; live issue history, not old draft flags, controls the selected-record editor.

This supports only the explicit synthetic profile and evidenced zero asserted tax. `issued` and `recognized` are true on the committed synthetic receipt; `legalInvoice` and `delivered` remain false. It does not establish legal identity/numbering, activate VAT, send an invoice or support issue corrections. The forward migration remains unapplied and runtime-unverified. COM-02 and COM-05 acceptance remain open.
