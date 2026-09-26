# NEXT-14: Original dimension assignments

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/dimensions/assignments.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/dimensions/assignments.ts` or the existing equivalent owner |
| Pure calculation | Original assignment eligibility and dimension projection |
| Atomic scope | Original dimensions are inserted using the same tx as journal lines. |
| Prerequisites | None |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Report integration follows NEXT-13. Root coordinates the shared journal union and application posting admission after WIP handoff. This packet does not implement posted retagging or a generic allocation engine.

## Versioned original facts

```text
OriginalAssignment {
  dimensionCode, dimensionRevision,
  valueCode, valueRevision, capturedLabel,
  status: explicit | explicit_unassigned | historical_exemption,
  exemptionEvidence?
}
NewJournalLineV2 {
  existing financial fields,
  originalDimensions: sorted unique-by-dimension list<OriginalAssignment>
}
SourceLineWithoutDimensionEvidence -> originalDimensions = NotRecordedInSource
# The missing state is an explicit import/read fact, not an old-schema execution adapter.
```

Do not add an array to old saved JSON or recalculate its digest. Explicit unassigned, historical unknown and evidenced exemption are different buckets.

```text
validateAssignments(line, postingDate, policy, mode):
    require dimension keys unique, same book and canonical ordering
    if mode == exact_reversal:
        require assignment bytes equal referenced original line's assignments
        allow historically valid but now archived catalog values
        return
    for applicable dimension in policy:
        chosen = line.assignment(dimension)
        if fixed: require chosen == policy.fixedValueRevision
        if required: require chosen is explicit and eligible
        if default:
            resolve default during PREPARATION and retain it explicitly
            # Never insert today's default silently at execution or historical import.
        if historical_exemption: require reviewed exemption applies to this source/date
        if explicit: require dimension/value effective and allowed for new posting
    reject unknown dimensions, ambiguous revisions or incompatible multiple values
```

Plan approval covers the new line shape and policy revision. The application posting service checks exact assignments against approved lines and the supported reversal/new-posting mode before its tx-passing batch inserts. PostgreSQL retains scoped references, immutable original assignments and storage uniqueness, not dimension-default policy. A replacement correction keeps unaffected original assignments and explicitly reviews changed ones; only an exact reversal inherits archived values automatically.

## Projection

```text
projectOneDimension(snapshot, dimension):
    buckets = [each frozen value, explicit_unassigned, not_recorded_in_source, exempt]
    for contribution in snapshot.financialContributions:
        bucket = resolve original assignment or proper missing-state bucket
        append contribution exactly once to bucket
    require sum(bucket amounts) == unfiltered snapshot amount

projectCrossTab(snapshot, dimensions):
    key = ordered tuple(one original assignment state per requested dimension)
    assign each contribution to exactly one tuple
```

Do not sum totals across separate dimension systems: cost-center totals and project totals each independently partition the same money. Also do not require each cost center to have a balanced balance sheet unless a specific complete allocation policy exists. No artificial balancing lines are created to make dimension filters look balanced.

## SIE handoff

```text
freezeObjectMap(catalog, usedAssignments):
    preserve stable exported numeric dimension IDs and original value codes
    require every emitted assignment has a matching declared dimension/object
    preserve historical code aliases explicitly when a native code differs
    refuse unsupported loss rather than emit empty object lists
```

Retagging later needs its own reviewed classification history and `original` versus `reclassified` report modes. It cannot mutate `originalDimensions` or previously exported files.

Vectors: A100+B200+unassigned50+legacy25 -> unfiltered375; archive A then reverse original -> exact -100 in originalA; new posting with archivedA -> refuse; two different dimension partitions both total375, not750.

Evidence baseline: S16/S27/S14.

## In-transaction journal integration

```text
applyOriginalAssignmentsWithinTransaction(tx, validatedJournal, insertedLineIds):
    require validatedJournal was prepared under its pinned dimension policy
    assignments = DimensionDomain.validateAssignmentsForEveryLine(validatedJournal)
    require one immutable assignment state per applicable line/dimension
    DimensionDb.insertOriginalAssignmentsBatch(tx, insertedLineIds, assignments)
    # Caller owns journal, assignments, approval use and receipt in one tx.
    # No public assignment API may append classifications to an already posted line.
```

Historical exemptions and unrecorded source values remain explicit inputs. Exact reversals inherit original assignments even when a catalog value is now archived. Adding dimensions never grants permission to modify posted amounts or bypass the pending WIP owner.
