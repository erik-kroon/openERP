# NEXT-28: Authorized collection reminders and dispatch recovery

**Priority:** P1. **Owner lane:** DELIVERY. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** apps/api/src/application/commerce/collections.ts and existing invoice-delivery/legal-delivery adapters; existing dispute and statement records.

**New scope, not repeated work:** The inspected reminder action explicitly records sendAuthorized=false. Add exact-message approval, dispatch admission and outcome recovery without recreating statements or disputes.

**Dependencies:** No new first-wave financial feature is a hard prerequisite. **Integrate after:** APP-SLICE-READY(commerce/collections), APP-SLICE-READY(durable-delivery).

**Conditional gates:** NEXT-15: the selected invoice has credit-note adjustments; NEXT-30: customer-credit balances affect the reminder amount.

**Evidence:** R03, R04 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Durable intent

```text
ReminderIntent immutable {
  id, invoiceIds, customerRevision, recipientRevision,
  balanceSnapshotId, disputeEpoch, templateRevision,
  exactMessageArtifact, amountByCurrency, asOf, stage,
  occurrenceIdentity, contentDigest, expiresAt
}
ReminderApproval {intentId, digest, operator, expiry}
DispatchAttempt {
  id, intentId, channel, providerProfile, externalKey,
  admittedAt, cancellationVersion, exactPayloadHash
}
DispatchObservation immutable {
  attemptId, source, rawRef, observedOutcome, providerCorrelation, receivedAt
}
```

The first profile adds no collection fee or interest. A later fee is its own evidenced financial operation, not a number inserted into an email. One intent corresponds to one approved reminder occurrence, not every queue retry.

## Prepare and authorize

```text
prepareReminder(customer, selectedInvoices, template):
  capture current supported invoices and effective payments/credits at one cutoff
  require positive collectible residual and no applicable dispute hold
  resolve intended recipient with reviewed address revision
  require no active ambiguous send for the same occurrence
  render exact content outside financial locks using frozen statement values
  seal recipient + subject + body + attachments + residual digest

approveReminder(command):
  validate exact digest and permitted stage/recipient
  recheck disputed/settled status and expiry
  append operator approval; append durable send intent in same tx
```

Do not approve a variable template that will pick a different amount or recipient at send time. Changes require another exact preview unless the original approval explicitly covers a finite alternative that the selected profile supports.

## Dispatch boundary and race semantics

```text
admitReminderDispatch(intentId):
  App tx:
    authorize current service identity and book
    lock reminder and referenced live invoice/dispute resources
    recover existing attempt or definitive receipt first
    require exact approval current and not cancelled
    require collectible amounts and recipient still equal the approved basis
    require no live dispute hold and no superseding reminder resolution
    create immutable attempt with stable provider identity
    append dispatch-admitted receipt
  return admitted exact payload

sendAttempt(attempt):
  perform provider call OUTSIDE tx
  persist authenticated/raw outcome evidence
  reduce outcomes using the provider's documented state semantics
  if outcome unknown:
      read back using correlation or retry SAME provider identity only if supported
      otherwise require investigation, never create a new send to probe success
```

If payment or a dispute commits before admission, sending is refused as stale. If admission wins first, the external message can still arrive afterward. Expose that order honestly. Do not hold a database lock across email I/O or claim an impossible atomic transaction with the provider. A known late payment may create a follow-up notification, not rewrite the already sent statement.

Queue claim expiry is not proof no email was sent. Provider idempotency retention can be finite; an ancient unknown attempt cannot be retried merely because its queue job is new. Capture that limit in the selected channel profile.

## Current state and historical evidence

A reminder history separates prepared, approved, dispatch-admitted, provider-accepted, delivered if evidenced, failed and unknown. SMTP/API acceptance is not evidence the customer read it. Collection disputes remain in their existing append-only owner. Dismissing a reminder neither cancels an invoice nor marks its debt paid.

A new deliberate reminder stage gets a new occurrence identity after checking the old outcome, cadence and policy. It does not overwrite the old artifact. Follow-up worklists use current residuals; saved statements keep their prior values.

## Interfaces and required outcomes

Use existing collection read APIs and add named reminder prepare/approve/dispatch-status operations. Only operator approval admits sending. Ordinary agents may propose and inspect. Show exact recipient, invoice references, as-of balance, hold reason and any unknown attempt before a send action.

```text
invoice10000, later paid4000 before dispatch -> stale10000 reminder, no call
new6000 reminder -> approved exact bytes, one external attempt on retry
hold added before admission -> refusal
provider accepted, response lost -> recover same external identity, no second reminder
payment after admission -> retain sent-as-of history and current paid status separately
```

Completion includes a configured adapter's observed send/recovery in an authorized environment. Local state simulation alone does not prove external delivery.
