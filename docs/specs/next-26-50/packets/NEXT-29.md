# NEXT-29: Recurring invoice occurrences without duplicate billing

**Priority:** P1. **Owner lane:** COMMERCE. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing commerce invoice drafts, legal issuance and application preparation/job owners. Add recurrence beside them without editing webshop intake or order conversion.

**New scope, not repeated work:** NEXT-16 prepares accounting from existing evidence. This packet owns recurring COMMERCIAL invoice occurrences and billing coverage, not recurring manual journals.

**Dependencies:** NEXT-02. **Integrate after:** APP-SLICE-READY(commerce/invoice-lifecycle).

**Conditional gates:** NEXT-15: an issued recurring invoice needs a credit.

**Evidence:** R03, R09 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Stable identity

```text
RecurringAgreement {
  id, book, customerId, anchorLocalDate, timeZone,
  cadenceKind, billingWindowRule, firstCycleOrdinal
}
TemplateRevision immutable {
  agreementId, revision, effectiveFromCycle,
  lines, price/tax defaults, customer snapshot policy, issueDatePolicy
}
AgreementEvent immutable {pause | resume | end | amend, effectiveCycle, evidence}
InvoiceOccurrence {
  agreementId, cycleOrdinal, serviceInterval, chargeComponentKeys,
  selectedTemplateRevision, draftId?, issuedInvoiceId?, status
}
UNIQUE(book, agreementId, cycleOrdinal)
UNIQUE approved billing coverage for a component/service interval
```

Template revision is deliberately absent from occurrence identity. Otherwise editing a template can bill the same cycle twice. Service coverage has its own conflict check to catch frequency changes whose new ordinal scheme would overlap an already billed interval.

## Calendar algorithm

```text
cycleDate(agreement, k):
  if monthly:
    targetMonth = anchor year/month + k*monthInterval
    targetDay = lastDay(targetMonth) if anchorPolicy=end_of_month
                else min(anchorDay, lastDay(targetMonth))
    return localDate(targetMonth, targetDay)
  if fixed_day_interval:
    return anchorLocalDate + k*declaredDayInterval
  otherwise: UnsupportedCadence
```

Always derive from the original anchor. Never repeatedly add one month to a clamped February date. DST changes affect due instants, not the service-cycle identity. Missing/skipped local times use the selected calendar policy or require review; no implicit UTC-month billing.

```text
planDueOccurrences(now, horizon):
  capture agreement state and last materialized cycles
  generate bounded cycle ordinals deterministically up to horizon
  select effective template revision BY CYCLE
  exclude paused/ended cycles according to explicit event policy
  disclose skipped cycles; do not turn resume into catch-up billing by default
  return complete bounded candidate set and continuation
```

## Materialization and issuance

```text
materializeOccurrence(agreementId, cycleOrdinal):
  App tx:
    authorize job, lock book/agreement
    replay exact command first
    if occurrence already has draft/issue: return its owned result
    recheck cadence/template/pause versions and service overlap
    create occurrence with chosen revision and service interval
    draft = InvoiceApp.createDraftWithinTransaction(tx, frozen fields,
             sourceIdentity=agreement+cycle+component)
    link draft and save receipt atomically
```

Creating a draft is not permission to issue. The normal human prepare/approve/execute issue flow applies. The invoice owner must enforce occurrence uniqueness at issuance too, so copying or editing a draft cannot bypass billing coverage. The narrow occurrence reference is part of the approved issue plan; the originating job never mints human approval.

Template defaults become explicit draft values. Current customer facts required for legal issue are revalidated there; frozen service/price facts are not silently replaced. If tax applicability changed, show the recalculated draft and require new review.

## Amendments, pauses and credit

A template amendment names the first affected unissued cycle and the billing boundary. Already issued cycles are immutable. A prepared but unissued draft needs explicit supersession and reapproval when amounts change. A pause that wins before issue admission blocks issuance; a pause after committed issue does not undo it.

A credit through NEXT-15 reduces the issued invoice but does not reopen the recurrence occurrence or permit rebilling the same coverage. Corrected replacement billing is a separate approved relationship, with a once-only replacement identity and net coverage check. Do not decrement an order's converted quantity or modify WIP webshop/catalog ownership.

## Controls and vectors

Report due, skipped, draft, approved, issued and delivered independently. Link every issued cycle to its legal number and ledger receipt. A schedule ending does not delete past invoices or waive their receivable.

```text
Jan31 monthly anchored -> Feb28 -> Mar31, not Mar28
same cycle twice with template v1/v2 -> one occurrence and one issue
pause after draft before issue -> blocked until explicit resume/review
resume after three paused cycles -> gaps disclosed, no surprise catch-up
change monthly to quarterly -> reject overlapping already-billed service coverage
queue failure after draft commit -> recover linked draft, no second occurrence
```

This packet is independent of order intake. Any future order-based recurring contract must consume the existing order owner's capacity rather than infer it from recurrence.
