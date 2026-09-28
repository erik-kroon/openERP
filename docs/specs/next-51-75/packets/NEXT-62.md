# NEXT-62: Dunning interest and enforceable reminder fees

Priority: **P2 when applicable**. Lane: **COMMERCE**.

**New deliverable:** Add financial interest and fee claims. NEXT-28 deliberately sends exact reminders without inventing those charges.

**Existing owner to extend:** Existing collections, contract/party evidence, AR and reminder-delivery owners.

**Required contracts:** NEXT-28, NEXT-30, NEXT-59. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** PRY-49; canonical family COM-04/05/06. Creates qualified monetary interest/fee claims; NEXT-28 only owns reminder dispatch.

**Atomic result:** Qualified interest/fee claim + receipt allocation, not implicit invoice repricing.

**Evidence:** R03, R04, X13 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Inputs and enforceability

A `DunningChargePolicy` is a reviewed contractual/statutory profile with applicability, rate-source periods, grace and accrual rules, day-count convention, claim dates, fee conditions and maximum supported amounts. Its legal basis is not a product toggle. Capture invoice/instalment principal history and actual payments/credits in economic order.

Separate `InterestAccrual`, `InterestClaim`, `ReminderFeeClaim`, `ChargeWaiver` and actual settlement. An unissued internal estimate is not necessarily an enforceable receivable. The selected accounting treatment determines when a book claim is recognized. No default reference rate, spread, fee or administrative charge ships in the compiler [X13].

## Exact segmented computation

```text
calculateInterest(claimScope,[start,endExclusive),policy):
    boundaries=principal changes + rate changes + applicable year/day-count boundaries
    exact=0
    for segment:
        P=eligible overdue principal under qualified date/order rule
        rate=one evidenced applicable rate
        exact += P*rate*dayCountFraction(segment)
    target=qualifiedCumulativeRound(exact)
    effective=previously recognized interest for the SAME coverage chain
    return target-effective with full segment witness
```

Do not compound interest or charge interest on fees unless a separately qualified profile permits it. A payment on a boundary follows an explicit contract convention. Repeated daily jobs calculate an incremental target rather than rounding and posting every day independently.

A fee becomes eligible only on its specified event/evidence. Retain one fee occurrence identity per legally supported event, not per failed delivery or retry. A reminder API's successful request does not by itself prove a legal charging condition.

## Financial application and settlement

An approved recognized charge debits a separate interest/fee receivable and credits the corresponding income role, with any applicable tax treatment explicitly selected. It does not amend original invoice principal or original sales VAT. A synthetic no-VAT example is not authority that every fee is outside VAT.

Payment allocation identifies original principal, interest and fee parts separately. Use explicit customer evidence or a reviewed legally appropriate waterfall. The amounts must sum to actual consideration, and each consumption is bounded by its own current capacity. A refund/waiver reverses the correct charge effect rather than creating a sale credit for the underlying invoice.

NEXT-28 renders the exact approved amount from these saved charge records. A stopped/cancelled message leaves the accounting event unchanged unless the selected charge condition actually depends on successful delivery. If it does, use a pending conditional claim and the evidenced outcome, not a fictional cross-system atomic transaction.

## Views and acceptance

Statements show original invoice residual plus separate charges and their basis/date. A debtor dispute may put collections on hold without deleting recognized receivables. A late backdated payment creates a target recalculation and reviewed adjustment, preserving prior charge documents. Cash lists only the qualified expected receipts, not all automatically calculated interest as certain income.

Synthetic ACT/365F interest on100000 at an input rate1/10 for30days rounds to822 minor under half-up. If principal drops to60000 halfway through, calculate two exact segments and round their sum, not two separately rounded daily batches. Re-running the same cumulative coverage yields zero new effect.

Complete with changing rates, partial principal payment, a legitimately chargeable fee, a waived fee, duplicate dispatch and payment allocation across claim types. Deliver the actual collection/AR integration and history, not just an interest formula.
