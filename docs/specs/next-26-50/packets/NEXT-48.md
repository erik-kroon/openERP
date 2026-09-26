# NEXT-48: Bolagsverket submission and authority-outcome lifecycle

**Priority:** P1. **Owner lane:** DELIVERY. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing annual-report semantic models/artifacts, signature records and external attempts. Implement one selected Bolagsverket profile through the provider adapter.

**New scope, not repeated work:** NEXT-24 ends at local generation/validation. Add the actual filing lifecycle while keeping original signatures, adopted copy certification, upload and registration distinct.

**Dependencies:** NEXT-24, NEXT-47. **Integrate after:** APP-SLICE-READY(external-delivery).

**Evidence:** R03, P24, X07, X08 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Obligations and immutable intent

```text
StatutoryObligation {
  entity, reportingFamily, fiscalYear, applicableFramework,
  requiredOutcomePolicy, deadlineRef
}
SubmissionIntent immutable {
  obligationId, reportRevision, copyArtifactHash,
  originalSignedManifest, copyEquivalenceProof,
  actualMeeting/adoptionFacts, authorizedCertifierIdentity,
  providerProfileVersion, environment, predecessorIntent?
}
SubmissionAttempt {intentId, attemptId, stableProviderIdentity?, requestHash, admittedAt}
ProviderObservation immutable {
  attemptId, exactProviderStatus, rawEvidenceRef, receivedAt,
  normalizedMeaning, receiptIdentity?, coveredArtifactHash?
}
```

Bolagsverket's published user workflow separates software upload, an invited authorized person's certification/submission and later authority processing [X07]. Do not equate an upload response with fulfillment. The exact services, fields and legal status mapping must come from the selected current service specification [X08], not a guessed REST interface.

## Prepare and admit

```text
prepareSubmission(reportRevision, governanceFacts):
  require selected report complete under its qualified local profile
  require required original-signature evidence and actual adoption facts for this stage
  require copy faithfully represents signed original under the qualified copy policy
  require correct entity/year and no incompatible active/accepted submission
  verify intended certifier is actually eligible, not merely app administrator
  freeze artifact, signer/certifier, service version and return/deadline relationships
  obtain separate human authorization for external submission

admitSubmission(intent):
  App tx:
    recheck current authority, report/signature/copy facts and intent version
    replay exact successful admission before new-work checks
    refuse unresolved prior same-obligation attempt unless provider-safe continuation exists
    create attempt and outbox with exact bytes hash and stable correlation
```

A signed original and an iXBRL copy need not be byte-identical formats. Their semantic equality is an explicit validated relationship, not permission to sign one set of figures and submit another.

## Provider state machine, without fictitious status names

The application normalizes actual provider observations into these internal distinctions. The adapter mapping is finite and versioned; unsupported raw statuses are retained as `needs_review` rather than assumed success.

```text
prepared
  -> validation_blocked | authorized
  -> upload_admitted
  -> upload_outcome_unknown | copy_uploaded
  -> awaiting_authority_certification
  -> submitted_pending
  -> received | rejected | outcome_unknown
  -> registered_if_required | correction_requested
```

Not every raw API provides every state directly. A missing observation remains unknown. `registered_if_required` is fulfilled only by a receipt/status that actually means it under the selected obligation policy. Copy upload, original signature and authority fastställelse certification are separate recorded events.

```text
advanceSubmission(attempt):
  recover known remote correlation before initiating another request
  call only the action allowed by current provider state and human authorization
  outside tx: upload/query/invite through selected provider contract
  inside short tx: append authentic observation and update derived attempt state
  enqueue bounded follow-up only when its allowed next action is known
```

Where the authority hosts certification, direct the eligible person to that ceremony. Do not simulate it by marking NEXT-47's internal signature complete or using a general accounting-agent credential.

## Rejection, correction and unknown outcomes

A rejection creates a case with the exact artifact and diagnostic. Correcting the report produces new content, validation and signatures where required, then a new linked intent. The old rejected or accepted bytes remain retained. After acceptance, replacement/correction follows an explicitly supported authority procedure, not a blind repeated upload.

A lost upload response is resolved using documented correlation/read-back or supported provider idempotency. If neither exists, freeze the attempt as unknown and require evidenced investigation. Enqueue retry cannot establish an external exactly-once guarantee.

Manual evidence can be retained, but label it as reported/reviewed evidence rather than pretending the backend fetched a provider-verified receipt. The obligation's required outcome policy decides what review can satisfy it.

## UI, controls and vectors

Display original signed content, submission copy, actual meeting/certification facts, all attempts, pending human action and authority receipt. A deadline reminder is not dismissed merely because an upload exists.

```text
HTTP upload200 with copy reference -> copy_uploaded, obligation not fulfilled
original signature valid, authority certification absent -> awaiting human action
same artifact upload outcome unknown -> no new submission identity automatically
rejected report corrected -> new revision linked to original rejection
accepted receipt for other entity/year -> reject linkage, keep raw evidence quarantined
registered required but only received observed -> still pending required outcome
```

No provider credentials, actual meeting facts or acceptance evidence were supplied by this design. Local model/adapter tests can prove the transition machinery; only an authorized provider exercise proves connected filing.
