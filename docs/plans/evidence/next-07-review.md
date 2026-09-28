# NEXT-07 paid supplier credits and cash refunds

## Scope and status

NEXT-07 covers a supplier credit beyond the unpaid residual and the cash refund that settles the resulting receivable. The pure leaf `@open-erp/domain/supplier-refunds` already existed; this work adds the owning application, the persistence and the transport on that unchanged leaf: `apps/api/migrations/0029-next-07.sql`, `packages/contracts/src/supplier-refunds.ts`, `apps/api/src/db/purchases/refunds.ts`, `apps/api/src/application/purchases/refunds.ts`, the HTTP routes, the read-only MCP capabilities, and the paid basis in `apps/api/src/application/purchases/credit-basis.ts`.

Status: the paid-credit and refund HTTP journey is observed against the real Worker and the real restricted-role PostgreSQL chain through `0029-next-07.sql`. Corporate tax, real-company VAT activation, provider settlement and the MCP journey are unobserved.

## Observed vectors

Observed on a synthetic `synthetic-core-v1` SEK book, one recognized line of net `100000` plus asserted tax `25000`:

| Step                                  | Observed                                                                                                   |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| After the `100000` payment allocation | `unpaid 25000`, `refundPrincipal 0`, `refundDue 0`                                                         |
| Paid credit `50000`                   | `apRelease 25000`, `refundPrincipalIncrease 25000`, `unpaid 0`, `refundPrincipal 25000`, `refundDue 25000` |
| Refund receipt `10000`                | `refunded 10000`, `refundDue 15000`                                                                        |
| Refund receipt `15000`                | `refunded 25000`, `refundDue 0`, `refundPrincipal 25000`                                                   |
| Legacy live invoice                   | `creditedMinor 50000`, `outstandingMinor 0`, no blockers                                                   |

The receipt rows, the single principal-increase row (`25000`/`25000`), two allocation legs totalling `25000` and two source usages were read back from the E2E database. The retained artifact is `next-07-paid-credit-refund-journey.json`, with the packet's own G/K/P/Q beside the observed positions.

## Decisions taken

**The paid credit reuses the existing supplier credit rows.** `supplier_credit_reviews`, `supplier_credit_approvals` and `supplier_credits` keep one credit-document identity for both the unpaid and the paid path, so the legacy live invoice keeps counting every credit in its `creditedMinor` and no second register exists. What the paid path adds is one `supplier_refund_principal_increases` row stating the payable release and the receivable increase, and the live invoice's credit-validity check reads that row to accept either shape. The unpaid execute refuses a review that carries the paid marker rather than posting a split as if it were an unpaid credit.

**The refund receivable is an explicit reviewed account, never a negative payable.** Preparation requires an active account that is not the payable, not the input-VAT account and not a reserved bank, control, owner, tax or VAT account, and one payable may only ever carry one such account. The unpaid residual clamps at zero in the live projection and the legacy over-allocation blocker stays silent once a sealed principal increase exists, because the excess is then refund principal rather than an inconsistency.

**A refund receipt posts cash against the receivable, or adopts an already posted compatible refund-control credit and posts nothing.** An adopted receipt carries no voucher, a cash receipt carries no adopted reference, and the database refuses any other combination. No expense reversal and no additional VAT credit is ever produced, because the credit already reversed the expense and released the deduction.

**A payment consumed by the refund cannot be reversed standalone.** `reversalSnapshot` refuses with `StaleDependency` when a supplier invoice's legs carry a posted refund principal or an allocated cash refund. This is the execution-time fence the packet requires; the pure `refuseConsumedHistoryReversal` guard was repaired earlier for the same class of defect.

**Allocation legs settle the refund due exactly.** Unique legs, every leg positive, legs totalling the receipt, and the total within the live refund due. A mismatch refuses whole; there is no partial posting.

## Open questions for owners

**Resolved in the review follow-up: valid credit document numbers now work in both paths.** Four HTTP regressions first reproduced `500 InternalError`: an uppercase paid-credit number, and uppercase, Unicode/punctuation and 128-character unpaid-credit numbers. `credit-basis.ts` now derives the bounded `supplier_credit:` source key from the existing credit recognition identity, which already hashes the exact counterparty/document-number economic key. The supplied document number retains its exact case and spelling, and the tax-component namespace is unchanged. No source-key schema was widened or financial identity lowercased.

**A cash refund source is not required to be a registered bank account.** The first cut required `openerp.bank_sources`, which is only written by the bank statement import and needs retained `application/json` evidence plus a statement window. That would make a refund unreachable on any book that has not imported a statement, which the packet does not ask for: it asks for an evidenced same-currency cash receipt from the supplier. The shipped rule is an active, non-reserved account plus retained refund and cash evidence. If the intended rule is a registered bank source, that is a one-line tightening plus a dependency on the banking owner.

**The payment that creates the refund principal is not a bank settlement.** No company-bank supplier-payment owner exists in this repository, so `P` was produced by a separately posted synthetic journal and the commerce allocation API, exactly as the existing AP evidence does. The refund journey therefore proves the credit and refund arithmetic, not a provider-confirmed payment.

**A reversal or correction of the paid credit or the refund receipt is not implemented.** The packet names an owned correction that restores the payment, credit and refund relationships together. `readProtectedCorrections` now marks both vouchers as owned so the generic correction path refuses them rather than orphaning a receivable, and the packet's case is refused; the restoring correction is future work on the posting-corrections owner.

**The paid path supports only the reviewed purchase profiles.** `swedish-purchase-full-credit-v1` and `swedish-purchase-partial-credit-v1` with the NEXT-03 recognized lines and a real input-VAT account. The synthetic zero-tax and gross-cost profiles, cross-currency obligations, advances and general netting remain out of this first profile, as the packet states.

## Limitations

The evidence is synthetic-book. It does not establish a real-company VAT profile, a legal credit-note document, a bank-confirmed payment, a statutory refund claim or an MCP journey. The refundable and refund-due figures are derived from retained rows at read time; no negative outstanding is ever stored, and the older `outstandingMinor` contract is unchanged.

## Source-identity follow-up verification

`bun run check:changed`, `bun run check:changed:full` and
`bun run test:e2e apps/api/tests/supplier-refund-journey.e2e.test.ts` passed.
All six HTTP cases passed, including both credit paths, exact-key unpaid replay,
the original paid-credit/refund conservation journey and consumed-payment refusal.
Artifacts `supplier-credit-source-uppercase.json`, `supplier-credit-source-unicode.json`
and `supplier-credit-source-maximum-length.json` retain the source keys, exact
document numbers and execution receipts. The paid journey now uses `N07-CN-1`.
Source inventory was stable:
`3d3462c6bb4cc58d7bcab529997642e6d088f78fee9452d1333f7e847150146e`.
