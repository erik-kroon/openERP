# NEXT-74: INK2 filing, signature handoff and assessment attribution

Priority: **P1 when applicable**. Lane: **TAX-DELIVERY**.

**New deliverable:** Complete the external corporate-income-tax filing journey after the existing tax bridge and INK2/SRU artifact. Keep signature, transfer, declaration record and final assessment separate.

**Existing owner to extend:** Existing corporate-tax calculation/declaration, financial closing, retained artifacts, tax-account and external-outcome owners.

**Required contracts:** NEXT-22, NEXT-23, NEXT-49. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** INK2/SRU external-outcome requirements; canonical family END-06/07, OPS-03. Tax filing/signature follows NEXT-22 fields and is not NEXT-48 annual-report registration.

**Atomic result:** No second income-tax expense; tax submission/signature/assessment references.

**Evidence:** R03, R05, X10, X11 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Final filing package

`CorporateFilingManifest` pins legal entity, actual fiscal interval, qualified form edition, final tax calculation, reconciled accounting basis, main form and required annex set, exact filenames/bytes/hashes and selected channel. Validate the fiscal year from its retained dates, not a calendar-year shortcut. Each annex names the same required entity/year and its original source model.

NEXT-22 owns fields and SRU generation. This packet consumes those artifacts rather than copying tax formulas or creating a second form renderer. Preparation can inspect a pre-close draft, but approval for final filing requires the selected final financial/tax basis or a specifically qualified exception. This creates no cycle: the existing pre-close tax calculation does not depend on an external filing.

The official file-transfer service describes a later signing step through Mina sidor [X11]. Official information also identifies an Inkomstdeklaration2-4 API [X10]. Select one actual channel and pin its machine/identity contract; an API read permission is not permission to submit. Do not guess that every field/annex accepted by the file service is supported identically by an API version.

## Preparation and signature authority

```text
prepareCorporateFiling(declarationRevision,channel):
    capture exact fiscal/entity identity and complete required artifacts
    verify main-form/annex totals and declared qualification checks
    compare saved final tax target with the owned current effective tax effects
    require no unresolved material filing blockers in the selected scope
    inspect existing authority declaration/transfer state where supported
    seal original/replacement purpose, artifact manifest and external-state witness

approveCorporateFiling(intent):
    verify current app operator and actual permitted external representative
    bind exact manifest and intended signature/submission action
    do not treat annual-report signing as income-tax declaration signing
```

A corporate return and a Bolagsverket annual report may share financial inputs but remain different submissions with different purposes. NEXT-48 cannot satisfy this tax obligation merely because its report was registered.

## Transfer, signing and receipt

Dispatch follows the shared attempt/recovery model. For manual file handoff retain exact bytes and user action without claiming transfer was observed. For authenticated transfer retain the genuine service receipt and its correspondence to the submitted files. If transfer only stages the declaration for later signature, the current state is `awaiting_external_signature`, not submitted.

```text
advanceCorporateOutcome(attempt,observation):
    verify source, environment, legal entity, fiscal interval and payload relationship
    append only the normalized state justified by the actual service response
    if signing required and unobserved: retain pending human action
    if final declaration outcome evidenced: link it to the specific obligation revision
    if authority assessment later arrives:
        retain assessment as a separate owned event and reconcile to declared target
        route any accounting/tax-account effect to its existing owner
```

Submitting a return does not create another income-tax expense or mark tax paid. Expected tax, declared tax, assessed tax and cash financing remain distinct. A later assessment difference needs its own qualified interpretation; it is not automatically a rounding adjustment to the already filed form.

## Corrections and acceptance

A rejected transfer can be repaired by a new artifact revision only where its actual content changes. Preserve the rejected original. An unknown transfer cannot safely be retried with new identities without documented recovery. A correction after a signed submission follows the supported amended-declaration procedure and its own approval, not replacement of old saved bytes.

The UI shows package completeness, transfer receipt, signature stage, accepted declaration and later assessment separately. A test-environment receipt never fulfills a production obligation. Reviewed manual evidence remains labelled as such.

Completion includes main form plus required annexes, different-than-calendar fiscal interval, wrong-year refusal, transfer-before-signature distinction, unknown-response recovery, competing outside submission and accepted declaration with no duplicate tax journal. It does not require or authorize a real company filing during implementation.
