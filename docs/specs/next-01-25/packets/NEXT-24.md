# NEXT-24: K2 annual-report semantic model and iXBRL

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/reports/annual.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/reports/annual.ts` or the existing equivalent owner |
| Pure calculation | K2 requirements, semantic model, presentation and iXBRL |
| Atomic scope | Final semantic approval/receipt and render intent are atomic; native validation runs later. |
| Prerequisites | NEXT-13, NEXT-23 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-13/23. Select the company's applicable framework version, not whichever template was newest when development began [X04]. Native XBRL validation is a narrow artifact-worker capability.

## Records

```text
AnnualReportRevision immutable {
  entityRevision, fiscalYear, financialCloseCertificate,
  statementSnapshotIds, comparativeBases,
  frameworkRelease, disclosureRelease, taxonomyMappingRelease,
  facts: [{semanticId, typedValue|Unknown|NotApplicable,
           evidenceRefs, calculationRefs, reviewedBy?}],
  narrativeSections, signerRoles, completionStatus, digest
}
PresentationRevision immutable {
  annualReportDigest, displayUnitAndPrecision,
  displayedFacts, roundingExplanations, rendererRelease, digest
}
ArtifactManifest immutable {
  modelDigest, presentationDigest, contentHash, mediaType, size,
  taxonomyVersion, entryPointHash, transformRegistryVersion,
  validationRuns, financialSignatureScopeDigest
}
```

Financial facts, narratives, governance assertions and actual signature events are distinct. An agent may draft prose but cannot turn an unsupported statement into a verified fact.

## Required disclosure evaluation

```text
prepareAnnualReport(year):
    witness = resolveProfile(..., K2AnnualReport, fiscalDates, entityFacts)
    require eligibility supports chosen K2 release, else explicit unsupportedK3/applicability blocker
    statements = exact approved financial snapshots
    for requirement in disclosureRelease:
        applicability = evaluate known entity/year facts
        if applicability unknown: retain required question
        if applicable:
            value = derive from retained financial/source evidence where supported
            otherwise require reviewed explicit non-ledger fact
        if inapplicable: retain reason and fact evidence, not an empty default
    compare periods using explicitly mapped comparable facts and known missing-history limits
    seal draft with complete requirement checklist

finalizeSemanticReport(draft):
    require no missing mandatory disclosure, unsupported comparison or financial mismatch
    require narratives contain only approved statements, with unknown drafts excluded
    freeze exact model approved for rendering
```

Meeting dates, signatures, dividend decisions and directors are never inferred from ledger balances. A prior year absent because the company is newly formed is established by company evidence, not by an empty export.

## Presentation and semantic numeric consistency

```text
preparePresentation(model, presentationRules):
    for numeric fact:
        displayed = exact rounding/unit transformation permitted by presentationRules
        retain source exact value, displayed value and rounding provenance
    validate arithmetic of displayed totals and permitted presentation differences
    if discrepancy needs an allowed rounding row: retain explicit presentation-only row
    otherwise use another permitted precision or refuse final rendering
    # No balancing journal is created for display rounding.
```

Rendered numeric facts must agree with their displayed values and declared units/precision. Do not display one rounded number but encode a different undisclosed XBRL value.

## iXBRL rendering

```text
renderIxbrl(model, presentation, taxonomyBundle):
    require all required concepts resolve to pinned entry point/DTS and qualified mapping
    build contexts keyed by (entity identifier, instant OR duration, dimensions)
    build units keyed by the actual ISO currency / other supported unit
    for semantic fact:
        mapping = exact concept, context rule, datatype, sign/unit/precision mapping
        require mapping applicable to this model/framework and disclosure role
        numeric -> emit ix:nonFraction with strict contextRef, unitRef,
                   sign, decimals/scale and supported transformation
        nonnumeric -> emit ix:nonNumeric with escaped approved content
        null/unknown -> do not manufacture0 or a fact; mandatory unknown blocks finalization
    emit readable statements/notes from SAME presentation data and stable templates
    reject duplicate concept/context/unit facts with inconsistent values
    add all referenced contexts/units; reject dangling references
    return deterministic XHTML bytes
```

The exact concept QNames, taxonomy packages and XBRL transformations are required qualified data, not names invented by this document. Comparatives use their proper periods/contexts and retained disclosures, not current-year labels pasted onto last year's amounts.

## Independent validation and immutable retention

```text
validateArtifact(bytes, bundle, validatorRelease):
    execute pinned native validator with local hashed taxonomy dependencies
    record actual document load, chosen entry points, complete DTS resolution,
           required validation stages executed, errors/warnings and run environment
    require documentLoaded
    require every required stage actually ran
    require no fatal/error and no unreviewed blocking warnings
    independently extract facts and compare to finalized semantic/presentation model
    require count/identity/value/context matches, including missing/duplicate fact checks
    store immutable validation report
    # A process exit0 with skipped document validation is NOT a pass.
```

Upload bytes and attach the verified manifest using C6. Validation unavailable preserves draft artifacts but blocks the required final state. No claim of Bolagsverket acceptance follows from a local validator pass.

## Signature/adoption boundaries

```text
FinancialSignatureEvent -> exact financial-report content and signer authority
AdoptionEvent -> actual meeting decision/evidence
AdoptionCertificate -> actual adoption facts and authorized attester
SubmissionAttempt -> exact submitted artifact variant plus external outcome
```

If an adoption certificate is added after the financial report was signed, verify the signed financial content remains identical and preserve its original signature scope. Never treat a signature over one digest as covering arbitrary later content. Different required signing/filing events remain separate even when shown in one UI wizard.

Vectors: changed note -> new semantic/presentation/artifact digest; unknown mandatory fact -> draft only; bad context date -> validation failure; exit0 but document not loaded -> failure; prior model/model after governance change -> old signed bytes retained; K2 output does not imply K3 support.

## Application model and native validation runtime

```text
finalizeAnnualReport(command):
    withAdmittedPrincipal(access, scope, annualReportPermission, (tx, principal) =>
        lock book; replay exact command first
        load exact report draft and captured close/statements/disclosure revisions
        AnnualReportDomain.assertCompleteApprovedSemantics(draft, current)
        approval = validate exact report-finalization authority using C5
        final = AnnualReportDb.insertFinalSemanticRevision(tx, draft)
        OutboxDb.insert(tx, render request with model/renderer/taxonomy identities)
        return finishOwnedWithinTransaction(tx, principal, command, draft,
            {journalIds: [], final}, approval)
    )

annualReportArtifactJob(job):
    establish scoped service permission and current artifact-work revision
    load exact finalized semantic/presentation model and hashed taxonomy bundle
    bytes = AnnualReportDomain.renderIxbrl(model, presentation, taxonomy)
    validation = run qualified native validator and independent extraction on Bun worker
    # No open financial tx, no native executable assumption inside API Worker.
    retain bytes and validation artifact with their exact hashes
    short application tx: reauthorize, replay, verify model/job versions and attach manifests
```

The job cannot mutate financial statements, finalize missing disclosures or mint signatures to make validation pass. A failed validation is retained as a failed result; it is not a thrown-and-ignored error that becomes an accepted artifact. No extra general-purpose execution service is required.
