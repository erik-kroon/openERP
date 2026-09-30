# NEXT-38: unsafe financial writer fenced

**Status: leaf retained; financial integration deferred.** The pure
`packages/domain/src/cash-method.ts` leaf models exact payment/year-end coverage.
It is not currently composed by a financial owner. The old application writer
was removed after tracing its claimed payment and invoice inputs through the
real commerce owner.

## Why the former green journey was not a cash-method journey

`commerce_invoices` requires an executed recognition voucher and line. Both
synthetic invoice registration and legal customer issue post that voucher first;
the register has no admitted invoice with commercial debt but no accrual
revenue/expense and VAT effect. Registering its posted gross again as a
cash-method line could lead to duplicate effects when the prepared journal is
executed.

The former payment command took `paidGrossMinor`, `paymentRef` and
`cashEvidenceId` from the caller. It did not read a final, effective commerce
allocation to that invoice or derive the settled amount in the owning
transaction. A retained evidence row does not prove cash was paid. The
year-end path scanned only voluntarily registered rows, not the complete
eligible invoice population. The previous E2E tests proved arithmetic over
caller assertions and insertion into synthetic tables, not these prerequisites.

## Current boundary

The three write routes — register, payment recognition and year-end cutover —
now refuse `UnsupportedProfile` after scoped operator admission, before any
financial or register write. The read-only route still inspects any retained
rows, deriving unpaid balances from exact prefixes; its year-end flag uses an
unbounded existence query rather than a truncated recognition page.

`0040-next-38-cash-method.sql` remains in the migration chain; no applied
migration was rewritten. The integration inventory records the leaf as
deferred with its actual owner prerequisites. Before any future writer is
enabled, its invoice identity must be fenced against a second caller-chosen
source-line label for the same gross.

## To deliver the packet

Extend the commerce issue/acceptance owner to retain a qualified cash-method
document without immediate revenue/expense and VAT posting, while preserving
the commercial open item. Then compose the leaf in the **same transaction** as
the effective payment-allocation owner, deriving principal, evidence and
identity from its retained posted cash event. Adopt existing cash capacity
without posting bank a second time. Seal complete eligible year-end membership
and the accounting method/profile revision, and make correction and next-year
settlement use the same source capacity and tax-fact owner. Prove payment,
year-end, correction, replay and rollback through HTTP/PostgreSQL before
changing the integration declaration back to wired. No actual-company method
or statutory tax treatment is inferred from a synthetic fixture.
