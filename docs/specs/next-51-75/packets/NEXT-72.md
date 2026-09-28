# NEXT-72: VAT declaration submission and authoritative return history

Priority: **P0 when applicable**. Lane: **TAX-DELIVERY**.

**New deliverable:** Add the filing lifecycle after the existing VAT calculation: exact submission authority, external period/declaration state, safe replacement and authentic outcomes. NEXT-37 remains the separate assessment owner.

**Existing owner to extend:** Existing VAT return snapshots, qualified releases, external attempts, declaration history and obligation fulfillment.

**Required contracts:** NEXT-04, NEXT-49. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-37: Link an actual later VAT assessment; submission itself has no assessment journal.

**Crosswalk:** PRY-57; canonical family VAT-02/04, END-07, OPS-03. Declaration dispatch is distinct from NEXT-04 calculations and NEXT-37 assessment.

**Atomic result:** No journal; declaration attempts and authentic outcomes only.

**Evidence:** R03, R05, X01, X10 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Separate calculation from submission

`VatSubmissionIntent` references the immutable calculated return, entity, exact reporting interval, complete box map, filing-unit semantics, rule release, original or replacement purpose and expected external declaration state. It does not recalculate tax or mark an obligation assessed. `SubmissionAttempt` and append-only `AuthorityObservation` belong to the existing external-outcome system.

The official API inventory and representative guidance identify a Momsdeklaration service and its permission family [X10]. This is evidence that a specific integration can be investigated, not a fetched machine contract. Pin actual current API schemas, credential arrangements, signing/submission steps, idempotency and status meanings before activating a connected profile. A company administrator inside OpenERP is not automatically its authorized tax representative.

## Prepare and authorize

```text
prepareVatSubmission(returnId,selectedChannel):
    load saved return and its explicit supported/profile/currentness state
    require complete applicable source coverage and reviewed period identity
    serialize filing integers from saved reported values, never from today's GL
    distinguish required zero boxes from omitted nonapplicable boxes
    if selected channel can read current authority state:
        capture actual entity/period declaration revision and pending submissions
        diagnose competing submission or inconsistent period before preparing replacement
    seal payload, destination, exact replacement relation and external-state witness

approveVatSubmission(intent):
    current human authority plus actual selected representative/mandate check
    bind exact payload, period, channel and expiry
    retain approval separately from financial-posting approvals
```

A replacement is prepared against the known original authority declaration, not merely the app's newest snapshot. Another accountant or system can submit in parallel. If the service lacks conditional writes, disclose that race and require read-back reconciliation rather than promise compare-and-swap protection it does not provide.

## Dispatch, unknown outcome and later change

```text
admitVatDispatch(intent):
    short tx: replay exact command; recheck approval and relevant local/external witnesses
    create one durable attempt and exact request identity
    outside tx: perform only the selected supported provider action
    short tx: retain authentic raw response and normalized observation

recoverVatAttempt(attempt):
    use retained correlation and documented read-back/idempotency contract
    if outcome cannot be established: keep unknown and block duplicate replacement
    never treat timeout or a successful upload as signed submission
```

Local preparation, service validation, transfer, signed submission, accepted declaration record, assessment and payment remain separate facts. A new bank transfer does not fulfill submission. Conversely, receiving a submission receipt posts no bank payment or tax-account assessment. NEXT-37 consumes actual assessment events later through its own operation.

Ledger changes after a committed submission do not make its historical receipt disappear. They create a new impact review and, if required by the qualified treatment, an explicitly linked amended return/submission. Original bytes and authority references remain accessible. Same-key recovery returns the original result even after a new calculation exists.

## UI, manual channel and completion

Provide a comparison of saved boxes, prior external declaration, proposed change and exact authorization. Current external access can fail without preventing an authorized read of already retained receipts. A manual official-channel handoff can retain the exact payload and independently reviewed outcome evidence; label that evidence honestly instead of claiming the connector fetched it.

An obligation advances only through NEXT-49's typed same-scope outcome predicate. An API success that merely creates a draft cannot satisfy a submitted/accepted requirement. The app must not invent an unavailable automatic signing mechanism to make the workflow appear complete.

Required cases include original submission, exact retry after response loss, external declaration changed before replacement, wrong entity/period receipt, revoked representative, prepared zero return, rejected boxes and later amended return with old artifacts intact. The connected packet is complete only when its selected channel has authentic observed outcomes; no current API credential or tax position is granted by this specification.
