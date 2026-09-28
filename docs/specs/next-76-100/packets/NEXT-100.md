# NEXT-100: Scoped integration event subscriptions and delivery receipts

**Priority when applicable:** P1. **Lane:** INTEGRATIONS.

**New work:** Add a concrete read-only outbound event subscription capability for external consumers. Existing outbox jobs are internal delivery, not a client-facing event contract.

**Use existing owners:** Existing scoped API authority, application outbox, effect-mq, immutable receipts and guarded outbound transport.

**Required earlier contracts:** Existing core operation owners.

**Evidence basis:** R04. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Finite public event surface

```text
SubscriptionRevision {book, subscriberPrincipal, endpointProfile,
  allowedEventTypes, payloadVersion, fieldProjection, secretRef,
  enabled, activationVersion, retentionAndReplayPolicy}
PublicEvent {eventId, book, type, ownerIdentity, ownerRevision,
  committedAt, minimalPermittedData, immutablePayloadHash}
DeliveryAttempt {eventId, subscriptionRevision, attemptId, targetDigest,
  admittedAt, responseEvidence, status}
```

Begin with a small explicit catalogue such as invoice issued, payment allocation committed, review requested and report ready. Event handlers do not execute supplied code or grant a financial write privilege. Sensitive payroll events are a separately scoped profile, absent by default. An integration marketplace/runtime is out of scope.

## From financial transaction to subscriber

```text
originatingOperation(tx):
  write actual domain effect and stable outbox intent in same transaction
  # A public event cannot exist as committed before the financial group commits.

publishEvent(intent):
  load exact committed owner result
  map through the versioned explicit event schema and authorised field projection
  retain payload once with stable event identity
  create delivery work for currently eligible subscriptions
```

No queue enqueue is performed while the financial lock is held. Duplicate outbox delivery produces the same event, not a second financial action. A consumer must treat event ID as idempotency identity; arrival order is not a global chronological guarantee. Provide an authorised read/snapshot path for gap recovery and a bounded retained replay range.

## Current authorization and transport

Before dispatch, check current subscription, subscriber/book permissions and endpoint/cancellation version. A revoked subscription cannot publish newly read private data. Retained historical payloads still require current permission to replay. Already delivered data cannot be retracted by deleting a subscription.

Use HTTPS and a reviewed endpoint policy. Reject credentials in URLs, unapproved private/internal destinations and redirect/DNS-rebinding escapes. A self-hosted internal endpoint requires a separate explicit allowlist, not a global insecure-mode flag. Resolve and connect under the guarded transport's verified destination contract.

A proposed v1 signature contract binds exact raw payload bytes, event ID, subscription ID, timestamp and key ID through HMAC-SHA256. Define canonical header formatting and freshness windows; never claim compatibility with another provider's webhook signature. Keep secrets in the credential owner, not queue payloads/logs.

```text
admitDelivery -> short scoped tx with current permission and attempt identity
send -> network outside tx with exact retained bytes
observe -> short tx retains bounded response and delivery outcome
```

A response success means the remote endpoint acknowledged transport, not that its business action completed. Lost response permits at-least-once redelivery of the same event identity, not a new financial command. Retry budget, backoff and dead-letter state remain explicit and inspectable.

## Rotation, disable and proof

Secret/endpoint rotation creates a subscription revision. In-flight attempts retain their admitted target/key identity; new admission uses current authority. Late ambiguous responses stay linked to the original attempt. Disabling stops unstarted dispatch and replay, while committed domain receipts remain recoverable independently.

```text
one invoice issue +3 transport retries -> one eventId, three attempts, one invoice
subscription loses book access before admission -> no outgoing payload
HTTP200 but consumer did nothing -> acknowledged transport only
same amount on two legitimate invoices -> distinct owner/event identities
queue history pruned -> domain idempotency and retained authorised replay policy still govern
```

Completion includes a documented receiver-verification example and an authorised test endpoint exercise. It does not require a new event broker or confer write access on webhook subscribers.
