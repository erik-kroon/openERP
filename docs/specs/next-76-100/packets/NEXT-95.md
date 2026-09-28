# NEXT-95: Counterparty balance confirmations with independent evidence

**Priority when applicable:** P1. **Lane:** REVIEW.

**New work:** Add requests for customers or suppliers to confirm a frozen balance and investigate differences. It is not merely another statement export or a claim of audit certification.

**Use existing owners:** Existing statement snapshots, scoped guest access, delivery and reconciliation-review owners.

**Required earlier contracts:** NEXT-13, NEXT-65.

**Evidence basis:** R02, R04, P25. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Freeze the assertion being confirmed

```text
ConfirmationRequest {book, partyIdentity, asOf, currency,
  frozenOpenItemSet, declaredBalance, statementArtifactHash,
  authorizedRecipient, purpose, responseDeadline, requestDigest}
ConfirmationResponse immutable {requestId, respondentIdentityEvidence,
  agrees|disagrees|cannot_confirm, assertedBalance?, differenceItems,
  attachments, receivedAt, verificationState}
```

A supplier's confirmation of one balance does not establish that all suppliers or source accounts were discovered. External response, internal reviewer acceptance and reconciliation signoff are separate stages. Nonresponse is unknown, never agreement.

## Request and receipt

Prepare from one immutable AR/AP statement cutoff and show the exact items/amount the recipient will see. An operator authorises that content, recipient and purpose before dispatch. Use the existing delivery-attempt model and guest portal scopes. A confirmation invitation grants no book-list, payroll, ledger-edit or other-customer access.

```text
submitConfirmationReply(token, typedReply):
  verify token purpose, scope, expiry and exact request revision
  retain source reply and uploaded evidence under request-specific limits
  append immutable response and receipt
  do not change invoice residuals, matched payments or signoff state
```

If identity is unverified or the message arrives outside the portal, retain the actual provenance and label the response accordingly. A matching email address is not a cryptographic corporate-authority guarantee. Never upgrade it silently to externally audited truth.

## Explain differences without auto-posting

```text
prepareDifferenceReview(request, response, currentSource):
  compare against the ORIGINAL as-of item set, not today's reduced balance
  classify evidenced candidates: timing, missing invoice, unapplied cash,
    duplicate statement item, credit in transit, currency/scope difference, unresolved
  retain each candidate link and independently reviewed amount
  require all allocations explain the stated difference without double counting
```

A late payment after the confirmation date belongs to a timing explanation, not a correction of the original statement. A real missing invoice routes to the source/purchase owner. A credit claim routes to the normal credit review. No response can directly generate a balancing voucher.

The reconciliation reviewer may accept the evidenced difference disposition for a named scope and cutoff. That attestation references all response versions and remaining unknowns. It is not a replacement for required bank/source controls or an implicit financial close.

## Revision, control and proof

Corrected requests create new versions with explicit supersession. Historical responses remain tied to the request they answered. A changed recipient invalidates unstarted delivery or needs fresh authorisation; uncertain prior dispatch cannot be assumed unsent.

```text
statement AR100000 asOf June30; July2 payment20000 -> response June30 compared to100000
recipient asserts80000 with evidence of June29 payment -> investigation, not automatic AR-20000
no response by due date -> pending/no response, never balanceConfirmed
unverified forwarded reply -> retained with identity limitation
new statement revision -> old token cannot answer the new amount
```

Provide request, response, differences and reviewer outcome in one usable workflow. Do not claim conformance with an audit standard or universal legal sufficiency from this product mechanism.
