# NEXT-13: Semantic P&L and balance-sheet snapshots

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/reports/statements.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/reports/statements.ts` or the existing equivalent owner |
| Pure calculation | P&L/BS mapping, opening selection, virtual result and subtotal graph |
| Atomic scope | Immutable snapshot membership and calculation persist through the reporting app owner. |
| Prerequisites | NEXT-02 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-02. Extend the frozen report/contribution authority. A correct arithmetic statement and complete company records are separate statuses.

## Mapping and contribution model

```text
StatementMappingRelease immutable {
  framework, effectiveFiscalRules, checksum,
  accountRoleRules,
  leafRows: [{rowId, statement, side, contributionPredicate, presentationSign}],
  subtotalDAG, mechanicalTransferRoles, comparativePolicy
}
SemanticSnapshot immutable {
  ledgerBoundary, recordedCutoff, fiscalYear, selectedInterval,
  openingBasisId, mappingRelease, factRevisions,
  leafContributions, rows, calculationNodes, diagnostics, coverage
}
```

Only a reviewed mapping may assign a financial contribution to a row. Require exactly one ordinary leaf destination per relevant account/component for a statement. Subtotals are calculations over leaves, not additional financial contributions. Contra accounts keep their signed effects. Do not infer every8xxx account as an expense.

## Opening and movement selection

```text
selectStatementBasis(year, asOf, cutoff):
    opening = latest authorized immutable OpeningSet for year at cutoff
        OR explicitly reviewed prior native balance basis for initial implementation
    require opening representation selected exactly once
    movements = complete committed journal groups with accountingDate in year..asOf
                and commitBoundary <= cutoff.boundary
    if opening is represented by an opening voucher:
        exclude that voucher from movements, retain it as opening provenance
    require no other overlap between opening coverage and selected movement identities
    return {opening, movements, cutoff}
```

A captured report is never filled later from current account labels, live profile facts or a newer movement cutoff.

## Calculation

```text
calculateStatements(basis, mapping, requestedPLInterval):
    rawClosing[a] = opening[a] + sum(actual movement debits-credits[a])
    periodActivity = movement components within requestedPLInterval
    yearOrdinaryPL = all year movements classified as nominal activity by mapping,
                     excluding only OWNED mechanical result-transfer components
    ordinaryPL = yearOrdinaryPL restricted to requestedPLInterval
    profitForInterval = -sum(ordinaryPL.signedAmount)
    fiscalYtdProfit = -sum(yearOrdinaryPL.signedAmount)
    transferredYtd = net credit to year-result equity from owned result-transfer receipts
    virtualUntransferredResult = fiscalYtdProfit-transferredYtd

    for component in ordinaryPL:
        leaf = require exactly one mapped P&L leaf
        add contribution(component.id, rawSigned, presentationSign)
    for balance-sheet account:
        leaf = require exactly one mapped BS leaf
        add opening and actual movement contributions with their original signs
    add a COMPUTED equity row for virtualUntransferredResult
        # No journal entry; explanation points to P&L and actual transfer receipts.
    evaluate subtotalDAG in topological order
    require all nonzero unassigned/ambiguous accounts remain in diagnostics
    check assets == liabilities + equity including virtual result
```

The BS virtual result is fiscal-year-to-date, not the P&L's arbitrary one-month slice. Retained earnings brought forward belongs to the opening basis. A first year does not imply that its opening is zero.

For a result-bridge closing style, ordinary revenue/expense entries remain in place and a separate nominal transfer role balances the year-result equity posting. Report exclusion uses the owned financial role, not merely a suspicious account number or text label. An unexplained manual entry to that account remains visible and cannot silently erase P&L.

## API/UI

```text
POST statement-snapshots -> capture + calculate + seal immutable model
GET snapshot -> rows, complete-scope totals, diagnostics, basis
GET row/:id/explanation -> frozen contribution IDs or computed child nodes
GET comparison(left,right,mode) -> same-unit signed changes and mapping differences
```

Comparison either uses each original mapping with an explicit classification-change display, or a separately retained comparative-reclassification model. Do not edit the older statement to make the graphs match. Every page refers to one frozen snapshot, including opening and calculated virtual-result explanations.

Internal reports may be shown with arithmetic pass and coverage unknown. Complete/statutory readiness requires all mapped and external completeness conditions. Export JSON/CSV from the same semantic rows, not another UI-side calculation.

## Vectors

```text
cash+100000 / revenue-100000; expense+40000 / cash-40000
    => profit60000; cash60000; virtual equity60000
owned transfer nominal+60000 / year-result equity-60000
    => profit still60000; virtual result0; actual equity60000
unmapped nonzero account => visible diagnostic, complete readiness false
new backdated posting after cutoff => old snapshot unchanged
```

Evidence baseline: S15/S20. A retained report keeps its exact semantic version. No parallel legacy SQL report runtime is required for disposable development snapshots.

## Effect snapshot service

```text
prepareStatements(command):
    capture = withAdmittedPrincipal(access, scope, reportingPermission, (tx, principal) =>
        lock book for consistent capture; replay committed preparation key first
        basis = StatementDb.captureRowsAndCompleteMembership(tx, scope, selection)
        return retained fixed basis or a captured typed value with complete version witness
    )
    if capture is replay: return saved snapshot
    result = StatementDomain.calculateStatements(capture, capturedMapping, requestedInterval)
    return withAdmittedPrincipal(access, scope, reportingPermission, (tx, principal) =>
        lock book; replay exact command first
        verify retained capture identity OR recheck captured dependency witness
        snapshot = StatementDb.insertModelRowsAndContributions(tx, capture, result)
        return CommandDb.save(tx, principal, command, snapshot)
    )
```

Once the basis has been retained, later activity does not make rendering its historical statement invalid. Report currentness is a separate query. SQL computes efficient scoped raw sums and retrieves contribution rows; the pure application calculator owns opening representation, transfer exclusions, mapping selection, virtual result and subtotal DAG. Browser components render the saved model rather than recomputing totals.
