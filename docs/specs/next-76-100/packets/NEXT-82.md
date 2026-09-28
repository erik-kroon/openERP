# NEXT-82: Component replacement, improvements and partial asset retirement

**Priority when applicable:** P2. **Lane:** ASSETS.

**New work:** Add separately supported asset-component replacement and improvement accounting. Whole-asset impairment and disposal remain unchanged.

**Use existing owners:** Existing asset carrying/impairment/schedule owners and the source-cost owner from NEXT-81.

**Required earlier contracts:** NEXT-19, NEXT-42, NEXT-81.

**Evidence basis:** R03, P19, P42. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Component basis

```text
AssetComponent {assetId, componentId, grossCost, ordinaryAccumulated,
  impairmentAccumulated, remainingSchedule, residual, sourceAllocation}
ComponentEvent {kind: addition|replacement|partial_retirement, affectedComponents,
  exactOldBasis, newCostAllocations, taxTreatmentRefs, effectiveDate}
```

For existing assets without component histories, require a reviewed allocation of gross cost, accumulated depreciation, impairment and residual that reconciles exactly to the parent. Do not allocate only net carrying and invent the missing gross/contra amounts. The classification split itself creates no new total value or depreciation expense.

```text
validateComponentSplit(parent, children):
  for quantity in gross, ordinary, impairment, residual:
    require sum(children.quantity)==parent.quantity
  require each child gross-ordinary-impairment>=0
  require complete original source/history explanation or explicit unresolved split blocker
```

An arbitrary estimated fraction is not sufficient disposal evidence. A qualified historical component estimate can be used only with its reviewed method and applicable policy.

## Replace a component

Let old component values be G, A and I, so B=G-A-I. Let N be the new independently qualified capitalized cost.

```text
compileReplacement(old, newSource):
  require exact supported component identity and current carrying basis
  debit accumulated ordinary A
  debit accumulated impairment I
  debit retirement loss B
  credit old gross asset G
  debit new gross asset N
  credit construction/qualified purchase clearing N
  create new component and approved future schedule
  retire old future occurrences, retaining all posted history
```

If proceeds exist, use the component-specific proceeds branch from NEXT-19 rather than also booking full loss B. If the new purchase was already recognized in construction, consume it; if not, recognition must be part of the same transaction through the purchase owner. No second vendor payable or tax fact is allowed.

## Improvements versus repairs

A reviewed repair expenses its cost through purchasing and does not change gross asset basis. An improvement adds a cost component only when the selected accounting profile permits it. Any changed remaining life or residual is a separate explicit future-schedule decision. Never recompute all previous depreciation from the new larger gross cost.

Execution checks component membership, prior ordinary/impairment changes, source-cost rights and possible proceeds before writing all journal/register/schedule effects together. A concurrent depreciation occurrence makes the old replacement plan stale.

## Readers and correction

The parent aggregates child gross/contra/carrying exactly. Historical reports retain their component revisions. Existing book-level asset controls include one contribution per actual posting, not both the parent amount and duplicated child amounts.

A reversal after the new component has depreciated requires a dependency-aware plan. Until supported, refuse rather than resurrect the old schedule and leave the new one running.

```text
old G100000 A60000 I10000 -> B30000
replace with N80000 -> old gross/contra cleared, loss30000, new carrying80000
parent component split60000+40000 gross -> aggregate100000, no extra asset
simultaneous installment on old component -> stale replacement, no partial posting
```

Deliver the full component basis, atomic retirement/new schedule and controls. A form that posts a manual capital addition without closing the removed component is not this feature.
