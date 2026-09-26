# NEXT-50: Agent book context, deltas and cross-domain unresolved-work index

**Priority:** P0. **Owner lane:** AGENT. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing shared capability registry, case snapshots, period preparation runs and domain report/read owners.

**New scope, not repeated work:** NEXT-16 prepares a period and NEXT-01 routes a case. Add a compact cross-domain orientation and delta interface so an agent does not rebuild the full book context every turn.

**Dependencies:** NEXT-01, NEXT-16. **Integrate after:** APP-SLICE-READY(capabilities).

**Conditional gates:** NEXT-49: including qualified deadline/impact outcomes; NEXT-33: including employee claim summaries under separate permissions.

**Evidence:** R02, R03, R07, P01, P16 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

**Late source handoff:** NEXT-01 is reported implemented in `4671a2fb` as `cases_resolve_review`. Consume that actual contract, not a proposed ownership-version field it intentionally omits. See [REVISION-NOTE.md](../REVISION-NOTE.md).

## No second accounting authority

```text
BookContextSnapshot {
  id, principalScopeFingerprint, book, requestedGoal,
  coherentRecordedCutoff, ledgerBoundary,
  profile/applicabilityRefs, sourceCoverage,
  moduleStatuses: available | unsupported | unavailable | not_authorized,
  unresolvedWorkRefs, existingPlans/receipts,
  allowedCapabilityRefs, dependencies, contentDigest
}
WorkRef {
  owner, identity, revision, kind, severity, affectedPeriod,
  blockedOperation, missingInputs, nextPermittedPreparation, immutableRef
}
```

Context rows point to existing owners. They are not mutable balances, a second approval register or a vector database of authoritative financial facts. A source quotation is untrusted evidence, not instructions to the agent. General context omits salary details unless the principal has the separate payroll grant.

## Coherent capture

```text
prepareBookContext(goal, scope, key):
  use one admitted repeatable-read capture or equivalent coherent snapshot
  recover identical successful capture first
  for each explicit supported context adapter:
    check capability/scope before querying
    read bounded summary and full count/continuation under the SAME tx
    retain referenced owner versions and exact selected scope
  unknown profile fields remain Unknown
  unavailable owner remains Unavailable, not zero unresolved cases
  abort capture on an unexpected database transaction failure
  # Do not catch failed SQL and keep querying an aborted transaction.
  derive work dependency order and next permitted preparation actions
  materialize immutable context membership and save receipt
```

Read-only retrieval of an existing context creates nothing. A request to refresh context is an explicit capture operation with a key. A large scope returns a bounded context plus continuation to owner-specific pages, not an unlabelled first-page total. Complete ledger boundary excludes half of a multi-voucher group.

## Work selection and compact output

```text
rankWork(context, requestedGoal):
  retain only authorized work relevant to selected goal/period
  order by: prevents selected goal, financial materiality class,
            deadline urgency under verified dates, stable owner/id
  collapse repeated identical missing-fact blockers into one question with affected refs
  do not merge their distinct financial effects
  return concise current facts, unresolved decisions and existing operation links
```

A capability registry identifies read, prepare, human approval and external effects. Progressive exposure chooses a useful authorized subset without inventing another tool implementation. Suggested next actions include exact known IDs and missing required inputs, never a forged approval token. The target operation rechecks authority and dependencies on execution.

## Delta semantics

```text
getContextDelta(baseId, targetId):
  authorize BOTH snapshots and current scope
  if scope/permission fingerprint differs in a way that can disclose revoked content:
      return FreshContextRequired without old private names or values
  require same selected book/goal semantics and supported context versions
  compare by (owner,identity), not display text
  added = target identities absent in base
  changed = same identity with changed semantic revision/digest
  resolved = source owner explicitly reports resolution
  removed = only a confirmed scope/deletion-status change under that owner
  unknownNow = target adapter unavailable or no longer sufficient evidence
  return delta + baseDigest + targetDigest + complete continuation metadata
```

An item absent because a domain adapter failed is not resolved. A receipt remains committed after a queue record is pruned. An expired pending approval can change next actions while its historical approval record remains in the old snapshot.

Optional remembered choices are records with source scope, reviewed applicability and expiry. Recall can suggest an already approved deterministic rule, but it cannot convert an old conversation into current permission or an accounting fact. User corrections propose new rules through the existing review path.

## Agent/UI integration and verification

Expose prepare/get/delta/work-page operations via shared REST/MCP semantics. The UI uses the same context to show “what blocks this period” and exact links to owning review screens. Never call a financial operation merely by rendering the overview.

```text
module contains0 rows + coverage unknown -> do not report complete
payroll grant revoked -> no delta leaking previous employee names
new bank payment for recognized invoice -> settlement suggestion, not new purchase
one shared missing VAT-method fact blocks12 items -> one question +12 references
base3 work items, target2 plus owner reports resolved1 -> precise resolution
owner unavailable in target -> unknownNow, not deleted/resolved
```

Measure returned bytes, tool calls and reproducible task success on the same fixed cases before claiming improved agent efficiency. A shorter context that hides a financial blocker is worse, not better. This packet promises an inspectable interface and proof criteria, not an unmeasured model-performance improvement.
