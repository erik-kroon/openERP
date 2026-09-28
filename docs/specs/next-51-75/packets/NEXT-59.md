# NEXT-59: Installment terms, partial due amounts and payment promises

Priority: **P1 when applicable**. Lane: **COMMERCE**.

**New deliverable:** Partition one invoice receivable into contractual due installments and retain later payment promises without multiplying the invoice or changing legal dates silently.

**Existing owner to extend:** Existing invoice residual/allocations, collection work and read-only Cash contribution adapters.

**Required contracts:** NEXT-15, NEXT-30. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-50: Include installment and promise summaries in agent context.

**Crosswalk:** Payment-term schedules in ERPNext review; canonical family COM-03/06, Cash readers. Legal installment residuals and payment promises extend one native obligation, not recurring billing.

**Atomic result:** No journal for term or promise changes; shared settlement updates remain owned.

**Evidence:** R04, R05 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## One debt, multiple timing components

`PaymentTermRevision` binds the issued invoice, legal agreement, date rule and exact amounts or reviewed weights. `Installment` has a stable ID, contractual due date, initial principal and links to reductions. `PaymentPromise` is a separate expectation with source, promised date/amount, review and expiry. A promise does not replace a contractual due date or change the ledger.

The sum of installment principal equals the invoice's original eligible collectible amount. Installment remaining sums to the SAME live invoice residual after native payments, credits, advance applications and write-offs. These rows are timing/allocation detail, not a second mutable debt ledger.

## Calculation and allocation

```text
prepareTerms(invoice,weightsOrAmounts,dateRule):
    require legal agreement and exact invoice/tax/rounding basis
    amounts=reviewed amounts OR stable residual allocation of total across weights
    require sum(amounts)==invoice principal and each amount>0
    dates=qualified contractual rule with explicit calendar adjustment
    retain original terms and successor revision identity

allocateInvoiceReduction(reduction,selectedInstallments):
    recover existing native financial identity first
    use explicit reviewed mapping OR qualified deterministic waterfall
    require allocation sum==the eligible reduction amount
    require each amount<=current installment remaining
    preserve actual cash, credit and write-off types separately
    append installment allocations in the SAME tx as native invoice consumption
```

Contractual due dates are not assumed to be evenly spaced months. No business-day adjustment is inferred from a date library alone. Rounded residuals use a stable specified installment order. Payment fee/interest obligations remain separate from installment principal.

## Terms change and delinquency

A genuine restructuring records the old arrangement, legal basis, exact unchanged or qualified changed principal and successor unpaid schedule. Previously paid installments remain historical. Replacing dates does not restore principal capacity or clear an existing overdue event as though payment occurred. If the new agreement contains interest, forgiveness or fees, the relevant financial owner commits that consequence with its own approved basis.

A payment promise can move an expected Cash date while leaving arrears based on contractual due date. Expired promises return to a visible undated/overdue expectation, not an invented next business day. Customer communications show the actual legal schedule and separately label promises.

## Atomicity and consumers

Attach terms to an unissued invoice in its issue transaction or append a reviewed timing arrangement to an already issued invoice with no duplicate AR. Credits/advance applications must notify the term owner internally so all residual views remain equal. Concurrent payments share the book/capacity lock; adding installment rows cannot authorize over-allocation.

Update aging to age each unpaid installment, not the whole invoice at its last due date. NEXT-28 reminders select due principal only under the selected stage policy. Cash emits the same installment identities once, replacing an old whole-invoice forecast rather than adding both. Invoice documents and statements retain the exact terms revision they displayed.

## Completion vector

Split original125000 into three equal-weight installments:41667,41667,41666 using stable residual order. A payment50000 consumes41667 from the first and8333 from the second, leaving0,33334,41666 and total75000. A promise to pay the second next week changes expected timing, not the contractual residual or the original due date.

Finish with term issue, cross-installment partial payment, credit allocation, restructuring of only the unpaid remainder and late promise expiry. Reconcile aging, statement, collection eligibility and Cash against one native invoice residual. No new journal should be created solely because due dates changed.
