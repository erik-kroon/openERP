# NEXT-38: retained-data cash-method delivery

## Verified isolated workflow — 2026-10-01

The isolated `next38-delivery` worktree resumes baseline
`6b82ed39039fe4e2bf160fed911b474c4fc0065a`. The complete retained-data supplier
workflow passed **50 HTTP/PostgreSQL tests across eight files**. Normal and
type-aware changed-file gates passed. Primary-checkout integration and its
combined-source verification remain pending; the inventory stays deferred until
that integration completes.

The supported input is an explicit synthetic domestic SEK/25%/full-deduction
supplier profile. It does not establish an actual company's accounting method,
VAT qualification or statutory acceptance. Applied `0040` stays byte-identical;
native commercial debt and retained coverage use forward migrations.

### Observed behavior

The named invoice, allocation, year-end and credit application owners compose
retained supplier drafts, effective allocation legs, final posted cash capacity,
reviewed method witnesses and exact original components in the caller's financial
transaction. The legacy write routes delegate to these owners; asserted amount
and witness payloads fail schema admission.

Independent observed vector: original125000=net100000+VAT25000; payment50000
recognizes40000/10000 without another bank entry; complete unpaid year-end75000
recognizes60000/15000 and AP75000; next-year75000 settles AP only, with no new
VAT fact or recognition journal. Commercial and recognized balances reconcile
separately in immutable native register snapshots.

Proof includes complete and empty sealed year-end membership, independent current
approvals, stale membership/method/account/source refusals, year-end/payment and
credit/payment races, rollback after nested journal/VAT writes and original-key
recovery, sealed receipt replay, correction/source reuse fences, and actual
financial-close receipt consumption. Unrecognized unpaid25000 credits change
commercial debt only. Recognized-unpaid25000 credits append net-20000/VAT-5000
with exact linked journal correction; the synthetic return includes box48-5000.
Retained source components incompatible with the original suffix refuse.

Paid-principal refunds, backdated year-end amendments, historical reassessment,
customer cash-method admission and wider tax/currency profiles remain explicitly
unsupported. No statutory or actual-company readiness is claimed.

### Repeatable receipt

Artifacts: `test-results/next38-complete-r4/results.json`, `source-integrity.json`,
`manifest.json`, `migrations.log` and runtime logs. Source integrity is `stable`;
initial and final inventory SHA256 are
`2bf57007c0d4648ace73b812b4f1d34f381da3cf8bb64dd15144d67b4eb2a657`.
The deliberate late-write failures return sanitized HTTP500 before successful
recovery; these are passing rollback scenarios, not ignored failures.

```sh
OPENERP_E2E_ARTIFACTS=test-results/next38-complete-r4 bun run test:e2e apps/api/tests/cash-invoice.e2e.test.ts apps/api/tests/cash-method-admission.e2e.test.ts apps/api/tests/cash-method.e2e.test.ts apps/api/tests/cash-payment.e2e.test.ts apps/api/tests/cash-year-end.e2e.test.ts apps/api/tests/cash-credit.e2e.test.ts apps/api/tests/cash-register-report.e2e.test.ts apps/api/tests/financial-close.e2e.test.ts
```

Earlier combined runs retained authentic failures in `next38-complete`,
`next38-complete-r2` and `next38-complete-r3`. Corrections included missing evidence
locators, numeric report-status interpretation, signed VAT contribution schemas,
credit-side tax-ledger validation, and legitimate fixture calendar/evidence setup.
Assertions were not weakened to obtain the passing result.

The historical fence record below explains the unsafe writer that was removed.
Its statements about absent invoice/payment owners describe the baseline, not
the continuing implementation.

## Historical baseline fence

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

## Historical boundary at baseline

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

## Historical remaining work at baseline

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
