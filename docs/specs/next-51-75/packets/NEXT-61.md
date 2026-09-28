# NEXT-61: Receivable allowances, confirmed losses and later recovery

Priority: **P1 when applicable**. Lane: **COMMERCE-TAX**.

**New deliverable:** Add impaired receivable valuation and confirmed bad-debt disposal without treating every overdue invoice as a credit. Neither normal customer credit nor a collection reminder creates this accounting.

**Existing owner to extend:** Existing AR residual, customer source-line tax, valuation/control and recovery cash owners.

**Required contracts:** NEXT-04, NEXT-15, NEXT-30. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** Receivable lifecycle extension; canonical family COM-04/06, VAT. Accounting allowance and confirmed tax loss are not customer credits or disputes alone.

**Atomic result:** Allowance/loss/VAT recovery effects + original receivable lineage.

**Evidence:** R03, R04, X06 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Three separate states

Retain an invoice-specific `CollectabilityAssessment`, an effective allowance target, a `ConfirmedLossDecision` and any subsequent `RecoveryEvent`. A book allowance changes valuation, not the debtor's legal principal. A credit changes the consideration for the supply. A confirmed bad debt has its own qualification and tax consequences. The official guidance requires the assessment of VAT bad-debt treatment for the particular claim, not merely a pooled age-based estimate [X06].

The first profile is same-currency accrual AR with known original line/tax and payment history. An unrecognized cash-method claim has no previously reported VAT to reverse. Foreign claims require the existing carrying-value owner, not nominal-rate conversion here.

## Calculation

```text
prepareAllowance(invoice,reviewedLossTarget):
    require target between0 and eligible remaining book carrying
    delta=target-effectiveAllowance
    debit loss expense delta
    credit receivable-allowance contra asset delta
    leave contractual AR principal and payment capacity unchanged

compileConfirmedWriteoff(invoice,claimPart,taxDecision):
    G=eligible original principal written off
    T=qualified VAT relief from original components, never inferred from arrears age
    A=allowance released for this exact claim portion
    debit allowance A
    debit loss expense G-T-A   # Negative amount reverses an over-provision.
    debit output-VAT relief T
    credit AR G
    consume native AR principal through one write-off identity
```

Tax relief can be zero or unavailable even when a book loss is justified. In that case, write-off and pending tax assessment are separate reviewed consequences. Do not fabricate a credit note or reduce taxable consideration solely to align reports. A later accepted tax adjustment posts its explicit delta and links to the original loss.

## Actual later payment

Civil recovery rights can remain after book write-off. A recovery record references the written-off principal capacity, not a recreated original invoice. Under a qualified case where recovered consideration restores the previously reduced output tax, receipt `C=NR+TR` posts debit bank `C`, credit loss recovery `NR` and credit output VAT `TR`. Tax restoration cannot exceed the relieved source components attributable to that recovery. Where no VAT was relieved, no restoration is manufactured.

A legally supported forgiveness is different from bad-debt accounting and changes recoverability rights. Record that decision rather than keep offering collection on a discharged claim.

## Atomicity and readers

Each allowance/write-off/recovery operation uses the existing journal plus AR/capacity/tax writers on one transaction. Recheck original-payment and credit consumption before execution. A concurrent customer payment makes an old write-off plan stale; it must not write off already paid principal. Recovering the same bank receipt twice returns the original result or conflicts by economic identity.

Aging shows legal principal, book allowance, written-off amount and collection status separately. Cash does not forecast a write-off as an outflow; forecast assumptions about uncertain receipts remain read-only reviewed scenarios. Controls reconcile gross AR, allowance and net carrying with retained source-level effects.

## Exact illustration and completion

Original claim125000 with eligible VAT25000 and allowance40000: confirmed write-off debits allowance40000, expense60000 and VAT25000, credits AR125000. With allowance125000, expense delta is-25000, releasing the over-provision. Later qualified receipt25000 with restored tax5000 yields recovery income20000, not25000 plus hidden tax.

Finish with partial allowance, increase/release, confirmed loss, late partial recovery and simultaneous-payment refusal. Keep independent evidence for book impairment and VAT qualification. An aging percentage dashboard is not this packet's completed workflow.
