# NEXT-37: VAT assessment ownership and exact-to-assessed bridge

**Priority:** P0. **Owner lane:** TAX. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing VAT obligations, released reclassification/amendment effects and tax-account statement/match owners.

**New scope, not repeated work:** Add the evidenced authority-assessment lifecycle. Do not reimplement or requalify the reserved reclassification or target-minus-prior amendment operations.

**Dependencies:** NEXT-04. **Integrate after:** WIP-VAT03, WIP-VAT04-A1, APP-SLICE-READY(tax-account).

**Evidence:** R10, R11, P04 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Three amounts and one reporting obligation

```text
VatObligationState {
  obligationId, effectiveReturnRevision,
  N: exact accounting net in minor units,
  R: declared net represented in minor units,
  effectiveReclassificationRefs, effectiveAmendmentRefs
}
VatRoundingBridge immutable {
  obligationId, returnRevision, exactNet, reportedNet,
  bridgeDelta, roundingRelease, journalRefs, receipt
}
AuthorityAssessment immutable {
  providerAssessmentIdentity, obligationId, authorityPeriod,
  signedChargeMinor, sourceTaxAccountEvent, replacesOrAdjusts?, evidence
}
AssessmentEffect immutable {
  assessmentIdentity UNIQUE, linkedTaxMatchOrNewPosting,
  settlementControlVector, taxAccountVector, receipt
}
```

Use positive amounts for an assessed tax charge and negative for a credit/refund entitlement. Cash arriving at a bank is still a separate event. A generic tax-charge classification or equal amount does not prove which VAT obligation an event assesses.

## Separate legitimate filing precision from disagreement

For a complete current reclassification target, the settlement control contribution is `-N` in debit-positive notation. If the qualified filing rule legitimately reports `R`, a separate bridge can change that to `-R`.

```text
compileRoundingBridge(obligation, release):
  require exact and reported values derived by this qualified return rule
  targetBridge = N-R
  delta = targetBridge - effectivePriorBridgeEffectsForSameObligation
  require every component of delta explained by retained rounding lineage
  addSigned VAT settlement control +delta
  addSigned designated rounding gain/loss role -delta
  preserve original reclassification/amendment receipts
```

Use the proper debit/credit gain or loss role for the sign. Never use a tolerance such as “less than 100 means rounding” without the qualified formula. An actual assessment `A` different from `R` remains an assessment discrepancy, pending amendment or separate evidenced authority decision. It is not automatically included in this bridge.

## Assessment capture and financial effect

```text
prepareAssessment(sourceEvent, obligationRelation):
  require original retained tax-account event and independent authority identity
  confirm registered period, legal entity and exact charge/credit relationship
  require same assessed identity not already financially represented
  determine whether event has a compatible existing journal + owned tax-account match
  if already posted:
      require exact settlement/tax-account role vectors and unused assessment relationship
      mode = adopt_existing_effect
  else:
      mode = new_assessment_posting
  retain amount difference to expected remaining assessed amount as explained/pending
  seal exact source, prior assessments and role relationship

executeAssessment(plan): FinancialTx
  replay and recheck obligation/source/outcome memberships
  if new_assessment_posting:
      addSigned VAT settlement control +A
      addSigned tax-account control -A
      post journal and call the existing tax-account match owner in this same tx
  else:
      reference the existing owned match/entry; do not reserve its line again
  append assessment effect and once-only identity; save receipt
```

If the match owner has no released internal tx port, do not approximate atomicity with two public calls. Request that exact integration port. Old manual journals can be adopted only through explicit reviewed role evidence, never equal-amount inference.

## Later reassessment and payment

A corrected authority decision is a new source event or a proven delta under the provider's contract. Never overwrite the old assessment. Tie it to the same obligation and leave previous return/bridge/assessment revisions readable. The VAT amendment owner calculates reclassification changes; this owner posts only assessment changes and qualified precision bridges.

```text
expected VAT settlement control =
    all owned reclassification and amendment vectors
    + all qualified rounding bridge vectors
    + all signed assessment vectors
```

A residual can be legitimate while assessment is pending. It is not “reconciled and paid” merely because a bank deposit equals the declared VAT. A payment to the tax account posts between bank and tax-account control without this packet reallocating it to a particular tax.

## UI and vectors

Show exact net, reported net, assessed events, rounding witnesses and pending differences. A zero return may have a no-effect assessment relationship, but no zero journal is manufactured.

```text
N12349 R12300 -> bridge debit settlement49 / credit rounding49
assessment A12300 -> debit settlement12300 / credit tax account12300
combined settlement control: -12349+49+12300 == 0
N=-12349 R=-12300 -> bridge -49; assessment -12300; net control0
A differs from R by500 -> visible discrepancy, never rounding plug500
existing posted assessment matched already -> adoption journal delta0
same assessment under a different command key -> AlreadyApplied
```

Financial design follows the adopted separation [R11]. Exact filing precision and authority proof remain qualified external inputs. This new owner must not take over either active VAT packet.
