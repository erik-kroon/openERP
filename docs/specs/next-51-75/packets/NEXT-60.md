# NEXT-60: Payment discounts and evidenced settlement differences

Priority: **P1 when applicable**. Lane: **COMMERCE**.

**New deliverable:** Add economically classified discounts and small-difference settlement, without a general rounding plug. Existing exact allocation correctly refuses these unmodelled residuals.

**Existing owner to extend:** Existing customer/supplier settlement, credit, tax adjustment and bank-source owners.

**Required contracts:** NEXT-07, NEXT-15, NEXT-30. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-17: The settlement includes foreign-currency principal or a separately evidenced FX difference.

**Crosswalk:** PRY-34, PRY-51; canonical family COM-03/04, IMP. Explicit price/fee/rounding difference decisions are not a generic tolerance plug or a new FX owner.

**Atomic result:** Explicit discount/fee/FX/rounding journal + exact principal settlement.

**Evidence:** R03, R04 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Classify before calculating

`SettlementDifferenceDecision` selects one finite supported meaning: contractual cash discount, separately evidenced payment fee, qualified minor rounding, accepted commercial reduction or unresolved short payment. They are not interchangeable. Difference magnitude alone never decides tax or expense treatment. An unresolved short payment remains an outstanding amount.

Retain original invoice/source components, actual cash/clearing identity, declared deduction terms, deadline/payment proof, counterpart role, required credit-document relationship and tax adjustment basis. A foreign-currency difference is split by the existing FX owner before any commercial discount is considered.

## Compile the selected branch

```text
compileSettlement(invoice,actualCash,reviewedDifference):
    P=eligible principal to settle
    C=actual principal consideration from cash/clearing, excluding separate fees
    diff=P-C
    classify using evidence and a supported explicit profile
    if unresolved: settle only C, leave diff outstanding
    if cash_discount:
        require contractual eligibility on actual qualifying payment date
        derive net/tax release from ORIGINAL remaining source components
        require netRelease+taxRelease==diff
        require required legal-credit condition satisfied or create its owned credit atomically
    if fee: use the fee owner and do not reduce invoice price/tax without its evidence
    if rounding: require explicit economic and profile bound, record residual as such
    return journal + native principal consumption + adjustment provenance
```

A customer discount vector can be debit bank `C`, debit sales reduction `dN`, debit qualified output-VAT reduction `dT` and credit AR `P`, where `P=C+dN+dT`. Supplier discounts invert the commercial roles: debit AP `P`, credit bank `C`, credit purchase cost reduction `dN` and credit eligible input-tax correction `dT`. A profile where tax is unaffected uses its own qualified vector rather than those formulas.

When a legal credit was already issued, settlement consumes the reduced invoice balance. It must not post the same discount/tax correction again. Payment allocations reference the credit/discount event's once-only identity.

## Execution and correction

The named settlement operation rechecks invoice residual, actual bank/cash capacity, discount eligibility and document status before committing all journal, allocation, tax and source-usage effects. No raw difference account is accepted from an ordinary model payload. New account roles are selected/reviewed through the existing role owner.

A returned payment reverses actual settlement consumption and its dependent discount only under the qualified legal condition. Some discounts remain granted even if payment later fails; do not hard-code reactivation. If a credit/refund subsequently consumed the adjusted basis, an unsupported standalone reversal is refused with the impact chain.

The difference record, failed eligibility and remaining residual appear in the work queue. Operator override can establish a reviewed treatment, never bypass conservation, same-currency comparison or source uniqueness.

## UI, controls and examples

Preview shows invoice residual, actual paid amount, fee, FX, discount, tax correction and still-unpaid balance separately. API output must not label everything 'rounding'. Aging and Cash reflect the same effective principal; GL control and adjustment components reconcile independently.

Synthetic customer invoice10000, actual cash9800 and an eligible gross discount200 with original quarter-rate split160+40 yields bank debit9800, sales reduction debit160, output-tax debit40 and AR credit10000. Without qualified discount evidence, only9800 settles and200 remains due. A processor fee200 is not that price discount.

Finish with a qualifying and nonqualifying payment date, a pre-issued credit adoption, a later payment reversal, duplicate source delivery and two competing residual consumers. Never use a tolerance to declare the unmatched amount nonexistent.
