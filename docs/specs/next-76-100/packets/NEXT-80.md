# NEXT-80: Supplier disputes with partial payment holds and release

**Priority when applicable:** P1. **Lane:** PURCHASES.

**New work:** Add supplier-side documentary dispute and explicitly bounded payment holds. Customer collection disputes and procurement acceptance do not supply this payable workflow.

**Use existing owners:** Existing payable residual, supplier credit, payment reservation and invoice evidence owners.

**Required earlier contracts:** NEXT-03, NEXT-07, NEXT-08, NEXT-71.

**Evidence basis:** R02, P28, P66. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Separate debt, disputed amount and payment eligibility

```text
SupplierDisputeRevision {invoiceId, sourceLineScope, disputedGross, reason,
  supplierCommunications, owner, openedAt, resolution?}
PaymentHold {disputeId, coveredComponents, blockedAmount,
  effectiveFrom, releaseDecision?, sourceVersion}
```

Opening a dispute creates no accounting entry and does not remove a valid recognized payable. Commercial rejection, an invoice mistake, a credit and an invalid liability are different outcomes. Any change to expense/VAT/debt requires its qualified financial correction owner.

```text
paymentEligibility(invoice, currentScope):
  outstanding = shared payable owner's current residual
  held = union of effective held monetary components, not sum of overlapping hold labels
  reserved = current live instruction reservations
  availableForNewInstruction = outstanding - held - distinctReservedUnheldAmount
  require each capacity counted exactly once and result>=0
```

Hold definitions reference stable source components or disjoint amount slices. Overlapping holds must be merged deterministically or refused at preparation; taking `min(totalHolds,outstanding)` hides conflicting instructions and is not the selected design.

## Opening and resolving

`openSupplierDispute` captures payable/source/hold versions, checks permitted evidence and writes the dispute, hold inventory change and receipt under the book lock. It invalidates unexecuted payment preparations for the affected capacity. It does not claim to cancel an exported or remotely admitted instruction: those routes stay outcome-unknown until NEXT-08/71 proves cancellation or execution.

```text
resolveDispute(decision):
  if supplier confirms full amount: release exact held capacity with evidence
  if valid credit issued: call/prepare existing credit owner; keep hold until effects reconcile
  if partial settlement agreed: qualified discount/credit owner determines financial effect
  if unsupported legal outcome: retain hold and named unresolved obligation
```

A release and replacement payment preparation can be separate deliberate steps. Final payment execution checks current hold/credit/reservation state, so a dispute opened after preparation cannot be ignored by a stale UI.

## Partial payments and historical views

Known undisputed slices can remain eligible when the selected contractual policy permits partial payment. The app cannot universally assume withholding is legally permitted. Legal due date is not rewritten; Cash may show an expected-delay assumption while retaining contractual exposure. Independent source coverage still includes disputed invoices.

A dispute added after a payment commits cannot unpay it. It records a refund/credit pursuit and links real cash history. Removing a hold does not mark an invoice settled.

## Journey and cases

The supplier workspace exposes recognized residual, held components, reservation/outcome state and actually available payment capacity. All payment paths, not only the new screen, consume this owner. History shows the original dispute and every resolution.

```text
invoice100000; held30000; no reservations -> eligible70000
another hold over the same30000 -> union30000, not60000
payment reservation70000 + hold30000 -> new eligible0
exported instruction now disputed -> no fake cancellation; create outcome/recovery work
credit10000 agreed on held portion -> post via credit owner, then re-evaluate remaining hold
```

The packet is complete only when manual, batch and provider payment admissions observe the same hold inventory. It is not a general legal-dispute or procurement system.
