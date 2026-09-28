# NEXT-57: Supplier advances and final-purchase settlement

Priority: **P1 when applicable**. Lane: **COMMERCE**.

**New deliverable:** Add prepayment to suppliers before an expense or asset is recognized. NEXT-31 defers already recognized service cost and is not a supplier advance register.

**Existing owner to extend:** Existing supplier payment, purchase recognition, refund and cash-source owners.

**Required contracts:** NEXT-02, NEXT-03, NEXT-07. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** Advance concepts in ERPNext review; canonical family COM-02/03/04, VAT. Supplier cash prepayment is not NEXT-31 expense deferral or a credit of an unrecognized purchase.

**Atomic result:** Cash/clearing + supplier advance/deduction + final purchase/AP.

**Evidence:** R03, R04, X05 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Advance basis

`SupplierAdvanceDecision` identifies the supplier, underlying contract/supply, original currency, authorized payment destination and selected VAT evidence/timing. `SupplierAdvancePosition` stores gross paid, carrying value, claimed input tax and remaining source components. A supplier payment instruction alone does not establish an advance asset or VAT deduction.

The initial slice is same-currency with an explicitly supported tax profile. Foreign advances can be monetary or nonmonetary under their accounting treatment; do not automatically use the foreign payable revaluation algorithm. Missing supported treatment is a named scope limit.

## Pure financial contract

If eligible input VAT `D` is recognized on a paid advance with net `N` and source tax `T`, then gross `G=N+T` creates advance carrying `C=G-D`:

```text
debit supplier-advance asset C
debit deductible input VAT D
credit actual bank/payment clearing G
```

A qualified profile with deduction deferred until valid evidence can retain gross carrying and no claimed tax, with an explicit pending-tax fact. The default is not to invent a deduction from the rate printed on a payment request.

For a final invoice with total gross `GF`, deductible VAT `DF` and cost `GF-DF`, consume a compatible advance gross `GA` whose claimed VAT was `DA` and carrying was `GA-DA`:

```text
debit expense_or_asset GF-DF
debit newly deductible input VAT DF-DA
credit supplier-advance asset GA-DA
credit supplier payable GF-GA
```

This simplified vector requires matching eligible tax and supply coverage. Different tax dates, changed rates, partial applicability or already recognized final invoices require explicit qualified branches. A final invoice that has already generated its full AP uses a separate approved advance-to-AP settlement without recognizing cost or input VAT again.

## Transactions and allocations

Prepare captures the actual original cash, supplier, prior deductions and final source-line membership. Advance applications are allocated to final source components, not to an arbitrary whole-invoice total. The application transaction rechecks remaining capacity and executes journal, advance consumption, payable recognition/settlement, tax facts and receipt together.

Only one native financial owner may consume a given advance component. Store a stable economic identity independent of review ID and enforce at most one original cash recognition. A later supplier refund consumes the remaining advance/recoverable claim through the existing refund cash owner; it is not a purchase credit for an expense that never existed.

If a supplier becomes unable to deliver, create a reviewed advance impairment or recovery case. Do not flip the supplier advance into paid inventory or ordinary expense merely to clear an old balance. Corrections after final application must address the downstream invoice and tax facts, or refuse the unsupported chain.

## Controls and UI

Expose requested, instructed, paid, applied and refunded amounts separately. Reconcile the advance asset to active original positions and the AP residual to the existing shared invoice projection. A positive supplier advance is not a negative payable available for arbitrary netting. Forecast only the remaining committed cash using current native identity.

Synthetic advance: G12500 with D2500 gives carrying10000. Final purchase G37500 with D7500 debits cost30000 and newly deductible VAT5000, credits advance10000 and AP25000. Subsequent payment25000 settles AP with no new purchase tax. With no advance deduction initially, retain carrying12500 and final newly deductible VAT7500 under a qualified evidence-timing branch.

Completion requires one paid advance, partial application, final application, refund and retained controls through the actual HTTP/UI owners. An extra payment category or a negative AP line without component/deduction conservation is not the deliverable.
