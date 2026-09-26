# NEXT-45: Direct cash-flow statement with a full reconciliation bridge

**Priority:** P1. **Owner lane:** REPORTING. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing semantic report snapshots, original financial contributions and owned cash/settlement links.

**New scope, not repeated work:** NEXT-13 produces P&L and balance sheet. Add historical actual cash-flow classification and closing-cash reconciliation, not a forecast or dashboard estimate.

**Dependencies:** NEXT-13. **Integrate after:** APP-SLICE-READY(reports).

**Conditional gates:** NEXT-40: the selected cash perimeter contains foreign-currency holdings; NEXT-39: processor/transit positions belong to the selected cash perimeter.

**Evidence:** R09, R10, P13 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Report definition

```text
CashFlowPolicy {
  cashAndEquivalentPerimeter, effectiveDateBasis,
  operating/investing/financing classification rules,
  tax/interest/dividend policy, internalTransferRoles,
  exchangeEffectRules, perimeterReclassificationRules
}
CashFlowSnapshot {
  ledgerBoundary, recordedCutoff, period,
  openingCash, closingCash, originalCashContributions,
  externalFlowLeaves, internalEliminations, exchangeEffects,
  perimeterChanges, unclassifiedRows, exactReconciliation
}
```

The perimeter is reviewed, not inferred from every account whose name contains bank. Tax accounts, restricted processor reserves and transfer-in-transit positions require explicit inclusion or exclusion. A policy cannot silently change between opening and closing without a disclosed perimeter bridge.

## Trace actual cash components

```text
calculateCashFlow(basis, policy):
  cashRows = all actual posted components in the selected perimeter and cutoff
  for row:
    if owned valuation/exchange effect with no external cash flow:
        assign to exchangeEffect using exact owner witness
    else if owned internal transfer:
        locate complete counterpart relationship and its permitted interval treatment
        eliminate internal movement only to extent both sides/perimeter bridge are explained
    else:
        origin = resolve exact settlement/purchase/payroll/asset/funding relationship
        splits = qualifiedClassification(origin, row.signedCash)
        require splits sum exactly to this original cash component
        if unresolved: keep unclassified with row reference
        else emit operating/investing/financing leaves with lineage
  retain every row once across external flows, eliminations or bridge categories
```

Never infer that two equal opposite amounts are an internal transfer. They may be unrelated customer and supplier payments. Use owned transfer identities. For a mixed payment, allocate using exact invoice/asset/principal/fee relationships rather than split proportionally by account labels.

Direct cash flows use actual receipts/payments, not invoiced revenue or P&L expense. A depreciation entry is noncash. Tax and interest placement follow the chosen reporting policy. No unclassified item defaults to operating just to make the report complete.

## Closing bridge

```text
netExternal = operatingNet + investingNet + financingNet
expectedClosing = openingCash + netExternal + exchangeEffects + perimeterChanges
reconciliationDifference = actualClosing-expectedClosing
complete = noUnclassifiedRows AND noMissingInternalCounterparts
           AND difference==0 AND requiredSourceControlsComplete
```

Internal transfers inside the perimeter contribute zero. Transfers crossing a reporting date may leave a transit balance: include that balance under an explicitly qualified equivalent-cash policy or show its reconciled perimeter treatment. Do not invent an external cash flow or drop the unmatched leg while still claiming a complete bridge.

Foreign-currency cash remeasurement changes book carrying without native cash flow. An exchange between two cash holdings can create a realized carrying difference; attribute it to the exchange bridge, while genuine bank fees remain external flows. Use NEXT-40's exact witnesses instead of recomputing every cash movement at today's rate.

## Snapshot, UI and export

Capture fixed financial membership, classification release and relationship revisions. Calculate outside locks, then seal after relevant currentness checks. The resulting report pages/explanations use its saved classification, not current supplier/customer labels. A later correction creates a new snapshot and comparison.

Provide total operating/investing/financing flows, exchange and perimeter bridges, opening/closing cash and every unresolved item. One click reaches the original cash line, allocation and source. Export the same semantic rows to JSON/CSV. This is not an indirect cash-flow statement until that separate calculator exists.

## Exact vectors

```text
opening100000; customer receipts200000; supplier payments-80000;
asset purchase-50000; loan inflow40000; FX carrying gain2000
operating120000; investing-50000; financing40000; exchange2000
closing=100000+120000-50000+40000+2000=212000

transfer accountA-30000/accountB+30000 inside perimeter -> external0
unexplained +500/-500 -> difference may0 but complete=false
invoice200000 unpaid -> no cash flow200000
foreign cash valuation+2000 -> exchange bridge, not operating receipt
```

The selected statement mapping is original design over the repo's report requirements. Its presentation and statutory applicability need the appropriate company/framework release, not merely balanced arithmetic.
