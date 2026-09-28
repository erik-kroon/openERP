# NEXT-124: Bank-feed provider handover with continuity evidence

**Priority when applicable:** P1. **Owner lane:** BANKING.

**New scope:** Add operational replacement of a read-only feed provider for the same real bank account. Historic import and one provider sync do not by themselves prove continuous coverage or safe cross-provider identity.

**Existing owner to extend:** Existing bank account identity, source occurrences, sync generations, matching and consent owners.

**Earlier contracts:** NEXT-09, NEXT-10. **This-wave dependencies:** None.

**Conditional:** NEXT-70: independent control comes from a supported structured statement; NEXT-97: ambiguous grouped overlap needs candidate discovery.

**Basis:** R02, P09, P70 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Two streams, one bank-account authority

```text
FeedHandoverPlan {
  realBankAccountId, oldConnection, proposedConnection,
  independentlyVerifiedAccountIdentity, old/newProviderScopes,
  overlapInterval, cutoverPolicy, originalCoverageRefs,
  observationMappingManifest, unmatchedItems, digest
}
ObservationAliasDecision {
  oldSourceOccurrence, newSourceOccurrence, canonicalBankObservation,
  relationshipEvidence, matchingVersion, reviewIdentity
}
FeedSelectionEpoch {bankAccountId, eligibleSourceStreamsByInterval, handoverReceipt}
```

Provider account IDs are namespaced source identities. They are not the actual bank account merely because the strings are similar. Establish ownership, currency and account identity using qualified independent bank evidence. No new GL bank account or opening-balance voucher is created for a provider change.

## Shadow intake and overlap reconciliation

```text
prepareHandover(old,new):
  retain new provider observations in shadow source state
  retrieve a bounded explicit overlap and preserve both originals
  compare account/balance/coverage assertions using independent statements
  identify exact shared bank transaction IDs when both providers genuinely supply them
  otherwise use NEXT-97 only to propose reviewed same/different-event relationships
  seal complete compared memberships and unresolved gaps
```

Equal amount/date/text alone is not an automatic alias. Two legitimate equal purchases remain two movements. Pending-to-booked relations use provider evidence and the existing source owner. A removed/modified observation can produce an impact case on already matched accounting rather than silently deleting the old canonical record.

Alias decisions attach new provenance to an existing canonical bank observation without creating another source capacity. Already reviewed bank matches and financial receipts remain attached to the same economic movement. A genuine new movement is admitted normally. A residual gap remains unknown coverage, not zero activity.

## Cutover transaction

```text
executeHandover(plan): nonfinancial admitted tx
  lock bank-account source-selection identity and relevant stream versions
  replay original command first
  require new consent and complete approved account/overlap witness current
  require reviewed source interval selection has no unacknowledged gaps/duplication
  append source-selection epoch and all validated alias/admission links
  fence old stream from new canonical publication after selected boundary
  retain old originals, cursors and published generations as history
  save handover receipt; invalidate affected live coverage/matching summaries
```

Do not hold a transaction across provider calls. Old in-flight read results may still arrive; they are retained according to the permitted source policy but cannot publish under a superseded epoch. Read-only provider cutover does not cancel unrelated banking payment mandates or external transfers.

A source-selection rule can retain the old stream for historical ranges while selecting the new stream going forward. It does not retroactively rewrite a report snapshot's original provider evidence. Failed new-provider synchronization leaves explicit current unavailability; it cannot quietly revert the source selection and admit duplicate overlap activity.

## Disconnect and restore behavior

Only disconnect the old connection after reviewing its remaining read/recovery needs and current actual consent authority. Revoking a provider token changes retrieval capability, not retention of legitimately held originals. The data-retention policy separately governs private source preservation. A backup restore starts with delivery fenced and must re-establish the selected current consent/epoch before activating either stream.

Rollback before cutover can discard shadow eligibility, not original evidence. After canonical adoption, a return to the old provider is another reviewed source-selection transition, not deletion of the handover or reimport of old balances.

## Controls and examples

```text
old feed balance100000, new feed same real account100000 -> GL opening delta0
oldTxnA/newTxnB proven same bank movement5000 -> one canonical capacity5000
two5000 transactions without unique evidence -> ambiguous, no automatic merge
late old response after cutover -> retained source but stale publication denied
new feed lacks last2 days -> coverage incomplete, not a clean continuity certificate
```

UI shows providers, retained account identity, overlap mappings, unresolved items and which stream covers each interval. Completion requires actual independent control evidence and observed no-duplicate handover in the selected provider pair, not merely saving a new API credential.
