# NEXT-77: Time-and-materials billing with once-only work coverage

**Priority when applicable:** P1. **Lane:** SALES.

**New work:** Add reviewed billable work capture and conversion into invoice lines. Payroll work facts, recurring invoices and deferred revenue remain separate owners.

**Use existing owners:** Existing employee/project references, source occurrences, sales-order capacity and invoice draft/issue owners.

**Required earlier contracts:** NEXT-51, NEXT-76.

**Conditional integration:** NEXT-79 when selected work was already recognised as unbilled revenue or requires its qualified contract-asset treatment.

**Evidence basis:** R02, P35, P58. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Distinct work and billing meaning

```text
WorkEntryRevision {entryId, personOrContractorRef, contractComponentId,
  serviceInterval, exactUnits, unit, workEvidence, billableDecision, revision}
PriceWitness {contractRevision, rateRevision, unitConversion, currency,
  roundingRule, negotiatedCap, review}
BillingSlice {workEntryId, reviewedRevision, unitRangeOrQuantity,
  reservedByDraft?, issuedByInvoice?, correctedBy?, economicCoverageIdentity}
```

Time recorded for payroll is not automatically billable and client acceptance is not payroll approval. Role-limited project views must not expose employee salary or private payroll fields. One original work item can be split, but its effective issued plus reserved quantities cannot exceed its reviewed billable quantity.

## Calculate and reserve

```text
compileTimeBilling(entries, acceptedContract):
  reject overlaps/duplicate economic work and unsupported mixed units
  for selected entry:
    quantity = reviewed available units after effective coverage
    rate = exact accepted price at the contract's agreed date basis
    net = roundRatio(quantityNumerator * rateMinor,
                     quantityDenominator * rateUnitDivisor, priceRounding)
    retain work locations, service dates and exact calculation residual
  enforce contract cap from NEXT-76 and qualified invoice-tax calculation from NEXT-51
  freeze selected work revisions, quantities and resulting invoice line identities
```

For example,90 minutes at120000 minor units/hour produces180000 net minor units before the separately qualified tax calculation. Neither a floating-hour approximation nor a later edited hourly rate may change that retained proposal.

`reserveAndCreateDraft` uses one application tx to recheck work and contract coverage, append reservations and create the ordinary invoice draft. Final legal issue consumes those exact reservations through the existing invoice transaction. Issue failure rolls back consumption; a lost response recovers the original invoice receipt. Do not consume work in a job after invoice issue, since that admits duplicate billing during the gap.

## Changes and exceptions

Editing unissued work invalidates dependent drafts. Abandoning a draft can release its reservation only through an owned state transition that proves it was not issued. Issued work is immutable financial evidence; later corrected time produces a credit or replacement-billing proposal referencing the original coverage. A credit does not automatically make the same hours billable again.

Write-downs and nonbillable decisions retain reason and actual quantities but create no invoice. Where work was already recognized as unbilled revenue, NEXT-79 supplies the exact asset-release branch so billing does not recognize revenue again. Otherwise normal issue recognition remains in force. Do not route the same work through both branches.

## Operator journey and proof

The user reviews person/task/service period, billable units, contract price, retained approvals and cap usage, then opens the normal invoice review. Reports distinguish recorded, accepted, reserved, billed and written-down work.

```text
reviewed10h, issued4h, reserved2h -> selectable4h
same work selected in two drafts -> second reservation fails or becomes stale
client disputes2h after issue -> retain10h original; create linked credit proposal
invoice issue commits before timeout -> replay returns it with coverage consumed once
```

Finish with real draft/issue/residual integration, not just a timesheet table or pure invoice calculator. No employee wage liability is created by billability.
