# NEXT-106: Service-retainer entitlements and once-only drawdown

**Priority when applicable:** P1. **Owner lane:** COMMERCE.

**New scope:** Add unit-denominated contractual service rights and consumption against prepaid retainers. Customer advances track money; recurring invoices track billing dates; neither alone tracks remaining service entitlement.

**Existing owner to extend:** Existing accepted contract, work coverage, advance/deferred-revenue and billing-capacity owners.

**Earlier contracts:** NEXT-56, NEXT-58, NEXT-76, NEXT-77. **This-wave dependencies:** None.

**Basis:** R02, P56, P77 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Scope and retained buckets

The first profile is a named customer's nontransferable entitlement to a defined service at an explicit tax/recognition treatment. This is not a transferable gift-card currency, third-party voucher platform or cash wallet. If the arrangement requires another voucher tax scheme, refuse this profile.

```text
RetainerBucket {
  contractId, customerId, serviceKind, exactGrantedUnits,
  unitDefinition, serviceWindow, cashRefundTerms,
  purchaseInvoiceOrAdvanceRef, netConsiderationBasis,
  existingRevenueOwner, rateAndTaxWitness
}
EntitlementEffect immutable {
  bucketId, grant | accepted_use | release_unused | refunded | corrected,
  sourceWorkIdentity, unitDelta, considerationRelease,
  journalRefs?, creditOrInvoiceRefs?, receipt
}
```

Retainer rights and financial liabilities have different units and owners. A paid receipt can support many service units, but cannot produce another advance liability here if NEXT-56 already recorded it. A bucket referring to already recognized revenue has no remaining deferred-revenue authority; its units may still be operationally tracked under a separately explicit recognition profile.

## Drawdown calculation

```text
prepareRetainerUse(bucket, acceptedWork):
  require work already accepted under its contract and not billed/consumed elsewhere
  q = supported exact service units for this work
  require q>0 and q<=remainingEntitlement
  require within permitted service window or explicit reviewed extension
  C = bucket net consideration subject to this qualified use-based recognition
  release = cumulativeRelease(C, grantedUnits, priorConsumedUnits, q)
  require financial release <= existing deferred consideration remaining
  return workCoverage, unit consumption, release and exact existing-owner refs
```

If a work item exceeds remaining units, split it explicitly into covered and separately billable parts before approval. An implicit negative entitlement or whole extra invoice is not allowed. Use the existing work-coverage authority so a timesheet cannot be charged once through NEXT-77 and again through a retainer.

```text
executeRetainerUse(plan): OwnedTx
  replay and verify bucket, work, contract and deferred-revenue versions
  validate exact qualified use-based recognition and authority
  debit deferred revenue liability release
  credit service revenue release
  call existing deferred-revenue writer with this same tx
  record entitlement/work-capacity consumption and receipt together
  create no new cash, receivable or VAT solely because prepaid service was used
```

Where the qualified revenue policy is time-based or performance-based rather than units used, the first profile refuses financial drawdown and retains operational use only. It does not override NEXT-58's schedule to accelerate revenue.

## Amendments, expiry and refund

Top-ups create a new funded bucket with its own price/tax facts and contractual priorities. Do not add units to an old bucket while retroactively changing the cumulative price paid per consumed unit. A first-expiring-first-use suggestion is a reviewed product policy, not permission to move value between different customers or service classes.

Expiry disables new service use only under the contract's actual terms. It does not automatically make remaining liability income. Breakage, extension or refund requires its qualified decision and the existing revenue/credit owner. A refund consumes unused entitlement and its exact monetary rights once, with original tax corrections where required. Previously earned revenue is corrected only if the reviewed facts justify it.

A reversal after later bucket use needs a complete supported capacity/consideration adjustment. Never delete old consumption or restart its occurrence counter. Preserve original invoices, service evidence and remaining rights in portal views.

```text
600 service minutes, net100000 deferred, use150 -> release25000, remaining450/75000
second work attempts same150 source identity -> AlreadyApplied
another600-minute top-up net120000 -> separate rate bucket, no repricing first150
expired remaining450 without qualified income decision -> liability stays75000
extra200-minute work with150 remaining -> explicit150-covered/50-billable split
```

Completion includes a real accepted-work-to-entitlement-to-revenue path, shared billing conflict refusal and retained rights in client/accountant views. A number called credits in a UI is not financial or service authority.
