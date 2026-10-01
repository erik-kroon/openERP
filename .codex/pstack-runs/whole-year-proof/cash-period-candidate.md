# Cash commercial-document period admission candidate

Proposed repair only. No source changes have been made by the coordinator. The unchanged broad E2E run must finish before any implementation.

## Observed data shape

Migration 0043 introduces a constrained discriminated invoice row. The recognized shape retains recognition voucher/line IDs and has no cash source draft. The commercial-only supplier shape has both recognition IDs NULL, a retained source draft, cash_method_supplier_invoice_v1 kind and NULL body recognition. It creates no accrual voucher. Migration 0046 applies invoice_recognition_period_open to both shapes and its financial-period function expects a recognition voucher for every invoice.

The application cash owner derives issuedOn from the reviewed retained draft document date, qualifies the profile for that date, and refuses admission after a blocking year-end run. There is no retained period ID for commercial-only invoices. Their recognition is owned by effective payment or complete year-end recognition, with posting vouchers subject to the ordinary period guard.

## Candidate

Use a new forward migration after 0047 to replace only the invoice recognition trigger with an explicit predicate for nonnull recognition_voucher_id. Retain the constrained row shape, voucher-period trigger, function logic, locks and refusals. A commercial document is not itself a financial recognition. Continue to protect every actual recognition voucher and recognized invoice link.

## Rejected alternative to compare independently

Introduce a retained commercial-invoice period ID derived from issuedOn and use it for the guard. This adds a separate period admission rule for documents without financial recognition. It risks refusing legitimate historical document intake and duplicates the existing reviewed date/profile and sealed-year membership rules. Select it only if maintained contracts explicitly require commercial-only document creation to share financial posting-period semantics.

## Independent expectations before code

- A reviewed supported cash supplier document for 12500 minor units admits through the real owner, remains linked to its retained draft/original, and changes no vouchers, journal lines or financial counters.
- Replay returns the same commercial identity without duplicate effects.
- Unsupported or mixed nullable recognition shapes remain refused by commerce_recognition_shape.
- A recognized invoice referencing a voucher in a locked period still refuses PeriodLocked with no retained invoice.
- A new posting voucher in a locked period still refuses PeriodLocked with no financial effects.
- Cash recognition on payment or year end still uses its own posting period and refuses stale or locked financial state through ordinary owners.
- A sealed year-end population still rejects later commercial document admission through the existing retained blocking-run rule.
- Forward migration applies and replays without editing the reviewed 0043/0046 migration bytes.

Use existing E2E fixtures first. Define any required additional negative scenarios before implementation. Retain the first fixed-revision failed run, the new migration checksum, literal expected-versus-observed outcomes and a passing fixed-source rerun. Do not change test expectations merely to obtain a pass.
