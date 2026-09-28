# NEXT-75: Accounting-method change with conserved recognition coverage

Priority: **P2 when applicable**. Lane: **TAX-FOUNDATION**.

**New deliverable:** Add a deliberate transition between qualified accounting/VAT methods. NEXT-38 implements cash-method events; it does not authorize changing method or prevent old invoices being reinterpreted by a new global flag.

**Existing owner to extend:** Existing company-profile activation, invoice recognition coverage, fiscal closing and statutory-method evidence owners.

**Required contracts:** NEXT-02, NEXT-03, NEXT-04, NEXT-23, NEXT-38. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-12: Imported open items require historical recognition evidence.

**Crosswalk:** Accounting-method transition extension; canonical family FND-03, COM-02, VAT, END. A reviewed method cutover is distinct from NEXT-38 ordinary cash-method events.

**Atomic result:** Complete qualified transition journal/coverage plus dated profile activation.

**Evidence:** R03, R05, X12 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Three different changes

Distinguish correcting a wrongly recorded registration fact, a legally effective accounting/VAT method change and a software migration between systems using the same method. They require different records. This packet covers the method change only. It must not be used to overwrite old company facts or bypass NEXT-12/25's real-data migration controls.

Retain `MethodTransitionDecision` with old/new qualified methods, entity, actual effective date, authority notification/decision evidence where required, selected financial and reporting policies and complete affected population. Swedish guidance distinguishes the procedures and conditions for the two directions [X12]. No revenue threshold, effective date or approval is inferred here.

## Capture disjoint history

```text
captureMethodTransition(decision):
    establish current official-method witness and permitted target/effective date
    capture complete original invoice-line populations across the boundary
    for each component retain:
        already recognized amount and its tax attribution
        paid but unrecognized anomalies
        unrecognized commercial outstanding
        recognized unpaid positions, credits, advances and unsettled instructions
    require source coverage and all financial/control relationships established
    freeze current population/revisions and known unsupported families
```

An already recognized year-end portion is not unrecognized merely because no cash was paid. An advance's tax history is separate from final invoice recognition. Unknown imported coverage blocks the transition rather than being assumed entirely unpaid or entirely recognized.

## Cash to accrual

For the first supported transition profile, compile the still-unrecognized eligible portion at the policy's permitted transition dates. Prior paid and previously year-end-recognized portions stay unchanged.

```text
compileCashToAccrual(component,transitionPolicy):
    U = qualified unrecognized remaining gross coverage
    if U==0: retain no-effect membership
    else derive source net/tax/deduction under original supported treatment
    purchase: debit cost/asset and eligible input tax; credit payable U
    sale: debit receivable U; credit revenue/deferred revenue and output tax
    append recognition slices with trigger=method_transition
    bind qualified reporting attribution independently from journal date
```

Later payment consumes the resulting recognized open position without another expense/revenue or VAT fact. A transition between periods can have different accounting and VAT timing under the selected policy; do not force them equal merely because one journal is created.

## Accrual to cash

Do not reverse all unpaid invoices or prior VAT automatically. Carry already recognized positions into an explicitly documented transition cohort and settle them once under their original recognition basis. Newly eligible supplies follow the target profile. Any legally required tax adjustment is separately compiled from its qualified rule with original lineage, never implied by flipping a Boolean.

## Activate atomically and preserve history

For a bounded supported book, one reviewed transition aggregate commits required journals, new recognition slices/open positions, cohort membership and the new dated method activation through internal transaction-passing owner functions. Recheck every population and competing payment under the book lock. If no internal activation port exists, obtain that port; two public commits are not an atomic transition.

A wider population needs an explicitly designed fenced cutover with staging and final activation, not an automatic half-switched book. The initial bounded implementation may refuse that scale. A failed transaction leaves the old method active. Historical invoice/report readers use their retained method/release, not today's active method. Existing applied migrations and historical records are not rewritten.

Example: gross125000/net100000/tax25000, paid coverage50000 recognized before transition, remaining75000 unrecognized. The selected cash-to-accrual bridge recognizes net60000/tax15000 once. Later75000 payment posts only settlement. If that75000 had already been recognized at year-end, transition financial delta is zero.

Completion requires both directional policies or an explicitly advertised one-direction release, actual-company applicability evidence before use, original/target control reconciliation, stale-population refusal, late source impact and same-key recovery. Accounting-method change remains optional breadth, not a prerequisite to a stable company's daily bookkeeping.
