# NEXT-71: Bank-qualified payment exports and status reconciliation

Priority: **P0 when applicable**. Lane: **PAYMENTS**.

**New deliverable:** Qualify a selected bank payment-file profile and its status-to-settlement journey. Reuse the existing synthetic pain.001 exporter, instruction reservations and recovery owner instead of creating another payment system.

**Existing owner to extend:** Existing supplier-payment batch/export, payee verification, instruction resolution and bank-settlement application owners.

**Required contracts:** NEXT-08, NEXT-10, NEXT-70. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-17: The chosen bank profile supports foreign-currency obligation settlement. NEXT-59: Transfers select invoice installments.

**Crosswalk:** Bank payment-format and recovery requirements; canonical family COM-03, OPS-03. Qualify the actual bank format/status channel around existing export and NEXT-08 capacities.

**Atomic result:** No cash posting on export/status; actual payment uses existing allocation owner.

**Evidence:** R03, R05, R07, X08 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Profile and identity

`BankPaymentProfile` pins bank/product, exact message guide and XSD versions, supported currencies/payment types, execution-calendar rules, debtor/beneficiary fields, address requirements and authentic status meanings. The inspected exporter produces a bounded pain.001.001.03 document [R07]. That proves an existing serialization owner, not acceptance by any bank.

Select one real bank profile first. SEB publishes current migration guides and payment-infrastructure changes, including address-format transition material [X08]. Acquire its actual selected schema/guide bytes and a bank-approved test path. Do not assume the generic ISO schema captures every bank restriction or that an old message version is the correct version for all execution dates.

Retain `PaymentOccurrence`, `ExportManifest`, `TransferIdentity` and `StatusObservation` with the existing instruction owner. An end-to-end identity belongs to one payment occurrence, not only an invoice. Two partial payments of one invoice require distinct identities. Retrying the same exported instruction preserves its original identity. A truncated invoice ID alone is not a sufficient unique payment key.

## Preparation and rendering

```text
prepareBankExport(selection,debtor,executionDate,profile):
    capture exact remaining invoice/instalment capacities and active reservations
    validate current independently reviewed beneficiary details
    validate bank calendar, profile date and actual external mandate
    allocate stable message/group/transfer identifiers with collision refusal
    build complete semantic transfer manifest with exact currency amounts
    render outside financial locks and validate XSD plus bank-specific rules
    independently compare every XML transfer to the approved semantic manifest
    seal exact bytes hash, beneficiary revisions, totals and source relationships
```

The existing approval/reservation owner commits the reviewed manifest and capacity reservations together. A failed render does not consume financial principal. Another key cannot create another live reservation for the same capacity. No supplier expense, VAT or bank cash movement is posted when the export is generated.

## Status and settlement

Dispatch uses the existing outbox/attempt lifecycle. File download for manual bank upload is an observed handoff, not a bank submission receipt. For a connected bank channel, admit one exact attempt under current authority, call it outside the transaction and retain the returned correlation. Unknown outcomes cannot be retried with new message IDs merely to obtain a response.

```text
observeBankStatus(raw,statusProfile):
    authenticate and retain original status document
    match message/group/transfer references to the exact export
    reject unknown or conflicting identities into an investigation case
    record per-transfer observed state using the selected provider semantics
    do not upgrade every transfer from one group-level acknowledgment
    accepted or processing means instruction status, not booked cash

recordObservedPayment(bankEvent,instruction):
    require exact supported final payment evidence and current allocation capacities
    post/adopt bank-versus-payable settlement through the existing owner
    consume instruction and invoice capacity in that same transaction
    retain real bank source relationship and receipt
```

A pain.002 partial acceptance does not release every rejected or unresolved transfer by inference. NEXT-08 evaluates the actual proof that a particular instruction cannot execute. Cancellation requests and expired queue leases alone do not establish that. Returns after actual payment are separate cash events with their correct reopened obligation or refund consequences, not deletion of the original payment.

## Proof and visible workflow

Show prepared, approved, exported, handoff, accepted, processing, booked, returned and unknown states only where the selected profile supports the distinction. Display status evidence and unresolved transfers beside the exact exported bytes. Customer/payroll batch use is a later explicit profile, not a hidden widening of this supplier profile.

For two instructions40000 and60000, a status accepting40000 and rejecting60000 cannot mark the invoice paid100000. Actual booked40000 leaves60000 principal, with reservation release requiring the rejected instruction's own proof. A replayed source payment produces the original settlement receipt. A new partial payment uses a new payment occurrence but cannot exceed the current60000 residual.

Completion requires the actual selected bank format and an authorized import/status/settlement exercise. Local XML validation and download remain useful independently, but must retain their lower evidence state.
