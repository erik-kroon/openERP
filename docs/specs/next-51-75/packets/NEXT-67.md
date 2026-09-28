# NEXT-67: Commitment-aware budgets with stop and warn decisions

Priority: **P2 when applicable**. Lane: **PROCUREMENT**.

**New deliverable:** Add controlled expense/commitment budgets. Existing reports show actuals and Cash forecasts liquidity; neither is a spend-budget admission rule.

**Existing owner to extend:** Existing dimensions, purchase commitment, approval and report contribution owners.

**Required contracts:** NEXT-13, NEXT-14, NEXT-66. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** Budget Stop/Warn mechanisms in ERPNext review; canonical family COM authorization, report readers. Discretionary commitment control adds no balance ledger and must not prevent recording reality.

**Atomic result:** No journal; commitments and enforcement decision for discretionary authorization.

**Evidence:** R04, R05 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Budget semantics

Retain `BudgetRevision` for book, interval, cost category/dimensions, exact amount, currency and one policy: stop, warn or observe. A budget is a management control, not available bank cash, legal authorization or an expense journal. One native source component belongs to a defined budget classification; reject ambiguous double membership unless an explicit split totals100 percent.

`BudgetExposure` is a derived projection of approved requests, unconsumed orders and recognized actual cost. It references the existing economic component identities and their replacements. No new writable actual-spend ledger is created.

## Exclusive stage calculation

```text
exposure(budget,cutoff):
    actual=sum(qualified posted cost contributions net of owned credits)
    ordered=sum(approved order commitment not yet replaced by actual)
    requested=sum(approved/request-reserved amount not yet replaced by order or actual)
    consumed=actual+ordered+requested
    headroom=budgetAmount-consumed
    return complete source membership and exceptions

checkProposedSpend(proposal,current):
    delta=proposed new exposure - exact replaced earlier-stage exposure
    after=current.consumed+delta
    compare annual AND relevant cumulative-period limits under policy
    stop -> refuse new discretionary authorization when exceeded
    warn -> require reviewed acknowledgment tied to current digest
    observe -> record decision without refusing
```

Do not include the full request after its order exists or the full order after invoicing. Taxes, FX conversion and non-deductible components follow the reviewed budget basis. An allowance credit and a payment are not new cost reductions unless their accounting effects actually change cost. Zero headroom does not authorize accessing private payroll detail to compute a result.

## Where stopping is legitimate

Apply hard stops before committing discretionary procurement or new spend authorization. A company may already have a real obligation from received goods/service. Budget exhaustion must not cause its mandatory bookkeeping to disappear. Capture the source, raise a breach and record the real liability through the authorized accounting path; any exception to a policy gate is explicit, independently approved and evidenced.

A budget override never supplies missing financial approval, invalidates tax evidence or permits an unbalanced journal. The override binds exact proposal, amount, budget versions, resource scope, reason and expiry. A changed budget or competing commitment requires a new currentness check.

## Atomic integration

Request/order approval and its budget reservation happen together in the existing operation transaction. Releasing or replacing a commitment consumes the exact reservation. Use the shared book lock initially to serialize competing budget consumers. A background report cache cannot authorize spending from stale headroom.

Invoice recognition consumes corresponding commitment budget rights while recording actual cost. If actual exceeds the accepted commitment, preserve the actual financial truth and report the difference with required accounting/procurement authority. A returned item, voided order or corrected invoice changes exposure through the relevant original owner, not a manual adjustment to cached headroom.

## UI, reporting and example

Show budget, actual, unconsumed orders, request exposure, remaining headroom and every override. Distinguish budget date from payment due/expected date. Cash may display budget assumptions as a separate scenario but cannot treat an unused budget as a committed cash payment.

Example budget100000, actual30000, open order20000 and independent reserved request10000 gives consumed60000/headroom40000. Turning that request into an order of10000 changes its stage, not total exposure. A new proposal45000 would exceed by5000 under stop. Two concurrent30000 proposals cannot both spend the same40000 headroom.

Complete with those transitions, a legitimate over-budget invoice, reviewed warning/override, cancellation release and a restarted request. A dashboard traffic-light calculation without atomic commitment admission is not the packet.
