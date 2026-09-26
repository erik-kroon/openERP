# NEXT-44: Multi-year SIE partition and dimension-preserving import

**Priority:** P1. **Owner lane:** REPORTING. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing bounded SIE parser, retained source staging, historical basis and financial run owners.

**New scope, not repeated work:** Extend the single-year/dimension-restricted import boundary. Do not rebuild byte retention, opening selection, financial admission or the historical open-item bridge.

**Dependencies:** NEXT-12, NEXT-14. **Integrate after:** APP-SLICE-READY(historical-migration).

**Conditional gates:** NEXT-11: independent roundtrip export is part of acceptance.

**Evidence:** R09, R10, P11, P12, X09 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Immutable partition model

```text
SourceYearPartition {
  sourceOccurrence, parsedRevision, sourceYearOrdinal,
  exactFiscalStart/End, accountControls, voucherMembership,
  dimensionDeclarations, sourceObjectMap, unsupportedRecords
}
ImportPlan {
  sourceHash, partitionsInChronologicalOrder,
  nativeFiscalMapping, accountMappings, dimensionMappings,
  selectedHistoryModeByYear, independentControls,
  completeMembershipDigest, exclusionDecisions
}
```

SIE source-year ordinal is not a year inferred from today's calendar. A native voucher identity includes book/fiscal year/series/number. Identical series and number in two different fiscal years are not duplicates.

## Parse and partition

```text
partitionParsedSource(parsed, reviewedFiscalMap):
  retain all records and original byte/line locators
  read explicit source #RAR intervals with real date validation
  require each mapped interval unambiguous and native fiscal boundaries agree
  for complete #VER block:
    choose the unique source year containing its accounting date
    if no match or multiple matches: blocking diagnostic
    retain final #TRANS lines separately from #RTRANS/#BTRANS history
    never add historical correction records to final transaction totals again
  attach year-indexed #IB/#UB/#RES and dimension/object balances to their own year
  retain unassigned or unsupported records visibly
```

If source line dates imply a financially unsupported cross-year voucher, do not split a balanced source voucher silently or move dates. Either the qualified format mapping preserves them as non-posting metadata or the plan refuses that block with its location.

## Dimensions and source controls

```text
resolveObjectAssignments(line, declarations, reviewedMapping):
  require each source dimension/value pair is declared or diagnosed
  map source dimension numeric ID to one stable native dimension
  map object code to reviewed native value preserving original source code
  retain explicit no-assignment, unknown and allowed historical exemptions
  reject dropped, duplicate or ambiguous assignments
```

Do not import current default dimensions onto historical lines. Unknown/unsupported dimensions must stop financial admission of affected vouchers rather than becoming an empty object list. Use NEXT-14's original assignment schema.

Missing zero control rows can be interpreted only when the exact supported format and independent source coverage establish that omission means zero. Otherwise absent remains unknown. Check each year's reviewed opening plus final financial movements against closing controls, then check the next year's balance-sheet opening relationship with explicit result-transfer/migration semantics. Never add an opening voucher on top of the same earlier history.

## Durable multi-year admission

```text
startMultiYearRun(plan):
  authorize operator; freeze complete partitions and per-year controls
  require one supported writer/cutover authority and no competing financial run
  retain current year/ordinal and domain fence

advanceYear(run, boundedChunk):
  select only the next reviewed source partition and exact source voucher membership
  prepare/approve through the existing owning financial-run flow
  execute a bounded group in one tx with source/native links and checkpoint receipt
  after all vouchers in year:
      independently compare native year closing to reviewed source controls
      require exact complete agreement or stop with retained diagnostics
      authorize the next partition's opening relationship; do not post it twice
```

Do not hold a transaction open for the entire source file. Already committed chunks remain accounting history if a later partition fails. Resume at the saved fence/checkpoint; rollback of the entire business migration requires an explicit supported correction/cutover procedure, not deleting earlier chunks.

Historical receivable/payable facts are admitted and bridged by NEXT-12 after the correct basis is established. SIE alone need not contain enough invoice-level detail to reconstruct those obligations. Missing detail stays a separate blocker, not an invented invoice.

## UI and vectors

Show source years, native year mapping, controls, object mappings, unsupported records and staged-versus-posted counts. A public exercise file parsing successfully does not establish destination or real-company migration acceptance.

```text
A/1 in source year-1 and A/1 in year0 -> two scoped voucher identities
prior UB matches next IB -> link basis once, no extra opening movement
source #TRANS100 plus historical #RTRANS-100 -> final amount remains100
dimension1='DEP-A' -> original mapped tag retained on journal/export
missing control row with unknown completeness -> unknown, not zero
failure in year2 after year1 committed -> recoverable paused run, no silent reset
```

Source-format grammar, encoding and allowed omitted records require the pinned specification [X09]. This packet does not invent support for SIE5 or all exporter-specific extensions.
