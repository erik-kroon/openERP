# Integration map and non-overlap record

NEXT-76..100 supplements the prior75 designs. It does not certify their implementation or replace their outstanding tasks. Only the new-wave dependency graph, including its declared conditional edges, is checked here. Earlier IDs are external contracts to resolve at dispatch.

## Ownership and prerequisites

| Packet | Required earlier contracts | New-wave dependencies | Conditional gates |
|---|---|---|---|
| [NEXT-76](packets/NEXT-76.md) | Existing core owners | None | NEXT-51: issuing invoices with the chosen tax/price profile |
| [NEXT-77](packets/NEXT-77.md) | NEXT-51 | NEXT-76 | NEXT-79: selected work already has unbilled revenue recognition |
| [NEXT-78](packets/NEXT-78.md) | NEXT-51, NEXT-59 | NEXT-76 | NEXT-79: prior earned revenue or conditional contract-asset treatment is selected |
| [NEXT-79](packets/NEXT-79.md) | NEXT-13, NEXT-51, NEXT-58 | NEXT-76 | None |
| [NEXT-80](packets/NEXT-80.md) | NEXT-03, NEXT-07, NEXT-08, NEXT-71 | None | None |
| [NEXT-81](packets/NEXT-81.md) | NEXT-03, NEXT-31 | None | NEXT-54: qualified import/landed-cost components enter the asset basis |
| [NEXT-82](packets/NEXT-82.md) | NEXT-19, NEXT-42 | NEXT-81 | None |
| [NEXT-83](packets/NEXT-83.md) | NEXT-31, NEXT-57, NEXT-59 | None | None |
| [NEXT-84](packets/NEXT-84.md) | NEXT-02, NEXT-13 | None | NEXT-22: the annual tax bridge consumes the selected deduction; NEXT-81: new commissioned assets enter the eligible tax pool |
| [NEXT-85](packets/NEXT-85.md) | NEXT-22, NEXT-49 | None | None |
| [NEXT-86](packets/NEXT-86.md) | NEXT-51, NEXT-15, NEXT-30, NEXT-49 | None | None |
| [NEXT-87](packets/NEXT-87.md) | NEXT-03, NEXT-20, NEXT-22 | None | NEXT-35: payroll accruals already include pension provisions |
| [NEXT-88](packets/NEXT-88.md) | NEXT-20, NEXT-21, NEXT-35, NEXT-36 | None | NEXT-87: pension obligations require a final provider settlement |
| [NEXT-89](packets/NEXT-89.md) | NEXT-02, NEXT-22, NEXT-23, NEXT-49 | None | None |
| [NEXT-90](packets/NEXT-90.md) | NEXT-02, NEXT-03, NEXT-13, NEXT-22 | None | None |
| [NEXT-91](packets/NEXT-91.md) | NEXT-07, NEXT-57, NEXT-71 | None | None |
| [NEXT-92](packets/NEXT-92.md) | NEXT-30, NEXT-07 | None | None |
| [NEXT-93](packets/NEXT-93.md) | NEXT-26, NEXT-50 | None | None |
| [NEXT-94](packets/NEXT-94.md) | NEXT-26 | None | None |
| [NEXT-95](packets/NEXT-95.md) | NEXT-13, NEXT-65 | None | None |
| [NEXT-96](packets/NEXT-96.md) | Existing core owners | None | NEXT-67: budget classifications contribute to routing only, not permission to hide liabilities |
| [NEXT-97](packets/NEXT-97.md) | NEXT-09, NEXT-10 | None | NEXT-70: the selected source is a structured bank file; NEXT-40: native foreign-cash comparability is supported |
| [NEXT-98](packets/NEXT-98.md) | NEXT-13, NEXT-23, NEXT-25, NEXT-49, NEXT-50 | None | NEXT-95: counterparty confirmations are part of the selected review evidence |
| [NEXT-99](packets/NEXT-99.md) | NEXT-13, NEXT-45, NEXT-50 | None | None |
| [NEXT-100](packets/NEXT-100.md) | Existing core owners | None | None |

## Cross-owner financial contracts

| Producer | New consumer | Required preserved meaning |
|---|---|---|
|Sales-order/invoice owner|76-79|Stable accepted component identities, draft reservations, once-only issue and credit history|
|Purchasing and schedules|81-83|Source cost capacity, exact already recognised purchase/tax, retained future schedule state|
|Asset and tax bridge|84-85|Book versus tax basis and pre-appropriation input stage, not a circular final-close prerequisite|
|VAT and external claims|86|Original consideration/tax plus separately qualified authority claim scope|
|Payroll/claims/holiday|87-88|Already accrued liabilities, actual paid facts and immutable prior declaration identity|
|Company evidence/statutory output|89|Actual resolution/availability facts and separate KU31 issuer reporting|
|Payable/refund residual owners|91-92|Noncash consumption included once in shared ageing/payment/Cash readers|
|Evidence/permissions|93-95|Original bytes, exact locators and current access; source assertions cannot approve accounting|
|Existing approval/execution|96|Exact quorum-set semantics supported by a new explicit contract, not forged legacy approval|
|Bank allocations|97|Candidate search is advisory; execution retains source/line capacities and rechecks scope|
|Reports/cases/close|98|Review acceptance of immutable scope, not a second financial certificate or ledger writer|
|Cash/actual source owners|99|Saved forecast vintages and independently reconciled payment identities|
|Outbox/capability owner|100|Minimal versioned public event, current subscriber authority and durable economic idempotency|

## Reservation policy

The historical VAT-03, FX-02-P1, AST-03, VAT-04-A1 and COM-2-W1 owners keep their current tasks. Names/numbers identify the original reservations, not a claim they are still unfinished. The current application migration owner also retains its ports and qualification. New consumers use released internal tx-passing functions or report the exact missing handoff.

No mandatory dependency is created on an optional profile merely because it shares a module. In particular97 may use existing booked native bank data without enabling a new bank-file importer;98 need not require a counterparty confirmation for every engagement;99 consumes an existing Cash forecast rather than forcing any tax strategy;83 does not wait for a finance-lease model.

## New versus already designed

**NEXT-76.** Add reviewed post-acceptance scope/price changes and billing-capacity conservation. This is not another webshop order intake, catalog or recurring-template owner.

**NEXT-77.** Add reviewed billable work capture and conversion into invoice lines. Payroll work facts, recurring invoices and deferred revenue remain separate owners.

**NEXT-78.** Add delivered-milestone acceptance and retained amounts on customer contracts. Invoice installments split due dates; they do not prove a milestone occurred or that retention is unconditional.

**NEXT-79.** Add earned-unbilled recognition before invoice issue. NEXT-58 defers invoiced revenue and is the opposite timing direction.

**NEXT-80.** Add supplier-side documentary dispute and explicitly bounded payment holds. Customer collection disputes and procurement acceptance do not supply this payable workflow.

**NEXT-81.** Add multi-source asset construction/acquisition accumulation and an explicit ready-for-use transition. Existing asset bases and depreciation schedules remain their owners.

**NEXT-82.** Add separately supported asset-component replacement and improvement accounting. Whole-asset impairment and disposal remain unchanged.

**NEXT-83.** Add contract-owned operating-rental commitments and deposit recovery. This is not a finance-lease/right-of-use asset or another recurring expense scheduler.

**NEXT-84.** Add a tax-value and deduction calculation linked to book assets. Ordinary book depreciation and income-tax calculation remain separate owners.

**NEXT-85.** Add optional tax-allocation reserve choices and their cohort history. Current-tax calculation alone does not own reserve deadlines or reversals.

**NEXT-86.** Add the explicitly conditional household-work profile, with labour evidence, split obligors and claim/rejection recovery. Mixed-rate ordinary invoices are not this workflow.

**NEXT-87.** Add actual pension provider charges, reconciliation against accrued obligations and separate special-payroll-tax basis. Regular pay calculations do not implement this evidence lifecycle.

**NEXT-88.** Add a reviewed employment-end event and complete final-pay inventory. This is not another regular salary or generic paid-correction implementation.

**NEXT-89.** Add a company-side dividend lifecycle with real resolution evidence, shareholder entitlements and reporting. It is not owner expense reimbursement or personal K10 optimization.

**NEXT-90.** Add a bounded operating-grant lifecycle separate from sales and loans. This is a proposed accounting expansion, not a finding that a current grant implementation is defective.

**NEXT-91.** Add noncash application of an established supplier refund/credit asset to another invoice. Creating credits/refunds and supplier advances do not yet define this settlement.

**NEXT-92.** Add explicitly agreed same-counterparty AR/AP discharge without cash. This is not applying a customer credit or supplier refund to another invoice.

**NEXT-93.** Add a searchable projection of retained originals and interpretation text with exact source locations. Extraction suggestions and agent context are not a document search index.

**NEXT-94.** Add a real inbound-email source channel to the existing supplier inbox. It does not replace uploads, extraction or reviewed draft creation.

**NEXT-95.** Add requests for customers or suppliers to confirm a frozen balance and investigate differences. It is not merely another statement export or a claim of audit certification.

**NEXT-96.** Add finite, versioned multi-reviewer routing for exact plans. Existing human approvals remain the financial authority; this is not unattended posting or an agent mandate.

**NEXT-97.** Add bounded one-to-many discovery and cross-proposal conflict analysis. Existing exact matches and reviewed allocation execution remain their owners.

**NEXT-98.** Add an in-product accountant review engagement around exact period artifacts and findings. Book Zero already owns the review outcome; this adds its collaborative workflow rather than another close certificate.

**NEXT-99.** Add retrospective evaluation of saved forecasts, not another forecasting engine. Cash scenarios and historical cash-flow statements remain their original owners.

**NEXT-100.** Add a concrete read-only outbound event subscription capability for external consumers. Existing outbox jobs are internal delivery, not a client-facing event contract.

## Practical release sequencing

Evidence93/94, approved contract changes76, acquisition/commissioning81 and exact matching97 are useful independent starts once their existing owners are released. Project77/78/79 require actual service-contract needs and mutually agreed recognition/billing coverage. Tax84/85/86/87/89/90 are conditional capability extensions, not a demand to delay Book Zero until every one exists.

Source presence, a passing pure example and a complete application journey are different statuses. When changing a financial owner, include all its current residual/read/correction consumers in the acceptance evidence. Root owns shared schema/grant migrations and the exact deployment checkpoint.
