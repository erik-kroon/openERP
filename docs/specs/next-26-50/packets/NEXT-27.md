# NEXT-27: Reviewed party identity resolution without balance merging

**Priority:** P1. **Owner lane:** COMMERCE. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** apps/api/src/application/commerce/crm-master.ts and commerce/register.ts; existing party revisions, invoice snapshots and payee verification.

**New scope, not repeated work:** Extend the existing directory and annotations with reviewed duplicate identity resolution. Do not build general CRM or silently merge financial capacity.

**Dependencies:** No new first-wave financial feature is a hard prerequisite. **Integrate after:** APP-SLICE-READY(commerce/crm-master).

**Conditional gates:** NEXT-02: legal identity facts or payment-role qualification are needed.

**Evidence:** R03, R05 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Identity model

```text
PartyResolution immutable {
  id, book, members: [{partyId, partyRevision}], canonicalPartyId,
  kind: same_legal_entity | related_but_distinct | not_duplicate,
  legalIdentityWitness, evidence, memberDigest, approvedAt
}
ResolutionChange immutable {resolutionId, replaces?, reason, reviewRef, receipt}
PartyIdentityHead {book, partyId, activeResolutionId?, identityEpoch}
```

Only `same_legal_entity` creates a lookup redirect. Related companies and similar trading names remain separate legal counterparties. Unknown identity can produce a possible-duplicate case, not an irreversible merge. No original party, invoice, payment verification or ledger reference is rewritten.

## Prepare and validate

```text
prepareResolution(selectedIds, chosenCanonical, suppliedEvidence):
  capture all selected party revisions and their current redirect closures
  reject cross-book membership and cycles
  require chosenCanonical belongs to the full resolved member set
  classify identifiers by jurisdiction and legal-identifier scheme
  if incompatible verified legal identities:
      permit related_but_distinct/not_duplicate only
  if same_legal_entity:
      require reviewed evidence establishing identity, not name/email similarity
  capture open obligation IDs, payment reservations and unissued dependent drafts
  report duplicates as candidates; do not net AR against AP
  seal exact member set, revisions, classification and downstream invalidation list
```

A tax registration number or bank account is not universally equivalent to legal identity. Scheme-specific qualification decides which evidence proves identity. Cross-border branches and represented entities need explicit treatment.

## Atomic resolution

```text
executeResolution(command): FinancialTx without journal
  recheck current scope, replay and exact approved resolution
  lock selected identity heads in stable ID order
  require full closures and all member epochs equal prepared basis
  append resolution and advance each affected identity head
  invalidate dependent UNEXECUTED payee/payment and party-sensitive plans
  preserve issued document snapshots and all existing allocations
  append identity_changed outbox event and receipt
```

Discovery for new documents follows the canonical identity but still selects a current legal revision explicitly. The old IDs remain searchable. New supplier duplicate checks search the entire resolved group, while returning the original invoice owner and source identity. They must not merge two invoices merely because the parties now resolve together.

## Financial reads and reversal

```text
resolvedDirectoryBalances(group, cutoff):
  retrieve each ORIGINAL obligation once by stable obligation ID
  group by legal identity and currency for presentation
  retain per-source-owner detail and control-account classification
  never sum different currencies or cancel AR with AP implicitly

settleExistingInvoice(invoiceId):
  use original invoice and its existing capacity owner
  identity resolution is provenance/discovery, not extra payment capacity
```

An erroneous identity resolution is replaced by a reviewed resolution change. It does not undo financial operations that used the grouping. Any unissued plans based on it become stale. Already issued invoices and verified payee facts remain historical and receive impact cases when relevant. Before splitting a group, identify any newer records that actually depended on its legal identity; missing evidence blocks their further use, not the ability to inspect history.

Runtime reads must avoid redirect recursion. Resolve a bounded member set under an epoch and reject cycles/oversize data. A materialized current lookup can accelerate discovery but is rebuildable from retained decisions and never owns ledger values.

## API/UI and completion

Add prepare/approve/apply/read/history operations under party resolution. The UI shows original and proposed identities, evidence, invoices affected and explicit statements that balances/issued bytes do not change. Directory exports name their resolution basis and retained original IDs. Existing annotation APIs remain unchanged.

```text
A and B same reviewed legal entity, each has one invoice100 -> total200, not100
A customer and B supplier related but distinct -> no redirect or automatic netting
concurrent A->B and B->C -> one serialized current closure or stale refusal
bank details change while merge review open -> stale payment-dependent witness
undo redirect after invoice issue -> issued party snapshot unchanged
```

Evidence supports an existing directory/annotation owner [R05]. A complete equivalent resolution service was not established by this bounded inspection; reconcile live source before creating its records.
