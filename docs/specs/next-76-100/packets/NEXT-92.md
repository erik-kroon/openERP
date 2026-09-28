# NEXT-92: Documented bilateral receivable-payable setoff

**Priority when applicable:** P2. **Lane:** TREASURY.

**New work:** Add explicitly agreed same-counterparty AR/AP discharge without cash. This is not applying a customer credit or supplier refund to another invoice.

**Use existing owners:** Existing receivable/payable settlement and current party/authority owners.

**Required earlier contracts:** NEXT-30, NEXT-07.

**Evidence basis:** R02, P30, P07. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Bound the legal and financial case

```text
SetoffAgreement {entity, counterpartyLegalIdentity, signedOrReviewedEvidence,
  effectiveDate, identifiedClaims, permittedAmount, currency, legalBasis}
SetoffPlan {agreementId, receivableLegs, payableLegs,
  exactGrossDischarge, currentHoldsReservations, basisDigest}
```

Initial support is the same legal counterparty, book currency and already recognised accrual invoices. Related companies, group treasury, disputed eligibility, insolvency cases and foreign-currency release require separate qualified treatment. Never infer setoff rights from a directory merge or matched amounts.

Cash-method tax recognition on noncash settlement is not automatically the accrual result. Refuse that branch until its method owner supplies a qualified recognition contract; do not silently omit a possible tax trigger.

## Compilation

```text
prepareSetoff(agreement, selectedLegs):
  capture exact claim identities and legally eligible outstanding capacities
  require sums(receivableLegs)==sums(payableLegs)==X and X>0
  require X<=agreementPermittedAmount
  require no unhandled payment, refund, hold or assignment reservations
  debit payable controls by their exact selected legs
  credit receivable controls by their exact selected legs
  retain each claim's effective date and documentary release relationship
```

Different VAT treatments on the underlying invoices do not justify recomputing tax in this recognised-accrual settlement. A settlement discount or waiver is a different financial event and must be separately compiled by its owner.

## One atomic discharge

`executeSetoff` follows C4: current authority, receipt recovery, one book lock, stable claim-resource ordering, exact approval and current mutuality/evidence witnesses. It writes the balanced journal and both AP/AR noncash allocation sets on the same transaction, then one receipt. It must use the existing internal settlement ports, not call two public allocation commands that can commit separately.

Setoff blocks conflicting outgoing instructions before effect admission. An instruction with unknown remote outcome cannot be safely ignored; resolve or explicitly partition an unreserved amount. A later actual bank payment does not undo the setoff automatically; it becomes an overpayment against the updated obligation.

## Reversal and reconciliation

Both sides' histories retain the agreement and receipt. Reversal restores both claim capacities and its journal together only if downstream credits/payments permit it. Otherwise identify the consumed closure and refuse a one-sided reversal. An actual invalidated agreement is not merely a UI unmatch.

Reports distinguish noncash discharge from collections/payments. Cash excludes this amount from future incoming and outgoing contributions using the same linked event, not by creating equal forecast cash entries. Tax/AR/AP controls still trace to original recognised invoices.

```text
AR150000 and AP100000; agreed setoff80000 -> AR70000/AP20000
journal AP+80000/AR-80000; cash delta0
remaining invoice paid20000 later -> ordinary cash settlement on remaining leg
one side changes after approval -> whole setoff stale, no partial discharge
same agreement/claim slice under another key -> no duplicate use
```

Delivery is a narrow enforceable-setoff workflow with all shared readers updated. It is not an automatic treasury netting service or legal opinion about a company's right to withhold money.
