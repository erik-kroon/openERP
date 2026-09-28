# NEXT-58: Invoice-driven deferred revenue and service-period changes

Priority: **P0 when applicable**. Lane: **SCHEDULES**.

**New deliverable:** Add the sales-side unearned-revenue lifecycle. NEXT-31 owns prepaid expenses/accrued costs, while recurring invoice occurrences do not establish when revenue is earned.

**Existing owner to extend:** Existing sales issue/credit and schedule recognition owners; reuse exact weighted allocation machinery.

**Required contracts:** NEXT-02, NEXT-15. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-29: The originating invoice is a recurring occurrence. NEXT-31: The shared schedule contract is being extended together with expense deferral; no duplicate schedule owner.

**Crosswalk:** PRY-52; canonical family COM-02/04, AST. Revenue liability/service recognition differs from NEXT-31 prepaid costs and NEXT-29 billing dates.

**Atomic result:** Revenue/deferral journal + schedule occurrence ownership.

**Evidence:** R03, R04 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Contract and source coverage

Retain a `RevenueRecognitionBasis` linked to immutable invoice lines and their approved service interval, performance evidence, net amount, residual treatment and method. The first profile covers a clearly defined time-based service using reviewed equal-period or day-weighted allocation. Milestone/percentage-of-completion accounting needs its own profile and is not inferred from a project label.

A service schedule, commercial billing schedule and payment schedule are different objects. A recurring invoice can bill services already provided or services yet to be provided. A security deposit is not deferred revenue. If NEXT-56 already carries an advance liability, final supply application must use that same carrying basis rather than recognize a second unearned liability.

## Calculation and issue integration

```text
compileDeferredRevenue(invoiceLine,cutoff,qualifiedMethod):
    slices=intersect([serviceStart,endExclusive),supported accounting periods)
    weights=qualifiedWeights(slices)
    shares=exact allocation of original NET consideration across slices
    require sum(shares)==original net
    earned=qualified consumed shares at cutoff
    unearned=originalNet-earned
    if issue not yet posted:
        allocate invoice net credit between revenue earned and deferred liability unearned
    else:
        debit original revenue unearned
        credit deferred revenue unearned
        create no new AR, cash or VAT
    retain schedule and future occurrence identities
```

Do not defer VAT merely because revenue is deferred. Tax facts stay on the applicable tax-point rule. Source tax and discount adjustments remain linked to original invoice components. Journal and schedule admission share a transaction at initial issue or the reviewed reclassification.

Each later occurrence debits deferred revenue and credits revenue for its approved retained amount. Compute due target less effective already-recognized amount. A queue retry cannot recognize a month twice. Human approval binds a fixed schedule batch or exact occurrence under the current owner policy, not an arbitrary future auto-post.

## Cancellation, credits and changes

A service-period amendment changes only the eligible unrecognized remainder. Allocate from current carrying, not the original full invoice again. Preserve previously recognized occurrences. If a correction to past recognition is needed, route a complete approved correction rather than editing old schedule rows.

A credit identifies whether it reduces earned service, unused future service or both. The qualified credit journal debits the corresponding revenue and/or deferred liability, debits eligible output-tax correction and credits AR/customer-credit liability. Retire or revise the future schedule atomically with the legal credit. The old schedule cannot continue recognizing refunded service.

Existing credit-number, source capacity and refund behavior remain NEXT-15/NEXT-30. This packet supplies the revenue-recognition counterpart and schedule effect, not a second credit document.

## Views and proof

Show invoice net, service interval, earned-to-date, remaining liability, recognized occurrences and pending future actions. Report explanations reach the exact source line and approved timing rule. Cash uses the remaining invoice/advance payment identity, not monthly revenue as monthly cash.

Synthetic annual net120000 with12 equal months produces10000 per month. After three months, revenue30000 and deferred liability90000. A credit for six unused months consumes deferred60000 plus its qualified original tax correction, leaving deferred30000. No extra cash event occurs until a refund or settlement is actually observed.

Complete with initial issue, first recognition, later month, future service shortening and a credit after partial recognition. Verify both the GL rollforward and retired future authority. General schedule creation without invoice/credit integration remains a leaf, not completed revenue deferral.
