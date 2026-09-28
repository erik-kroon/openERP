# NEXT-18 bounded leaf repair

## Scope and status

Reviewed baseline: `0bebac545bafd0c823a5df87e3d75dbedb9081b6`. The leaf was unchanged from that commit when the pre-edit probe ran. This repair changes only `packages/domain/src/fx-remeasurement.ts` and this evidence note.

Repository search for `fx-remeasurement`, `prepareValuation`, `assertValuationMembership` and `ValuationSelection` found the leaf, its package export and documentation, with no application consumers. The input contract now requires `items[].controlAccountId` instead of a selection-level control account. `AmountOutOfRange` replaces the obsolete `UnsupportedScale` failure: all schema-supported scale pairs use one rational conversion and one rounding operation.

```text
decoded complete selection
  → per-item control binding + bounded target/delta
  → pure plan (including an empty no-effect population)
approved membership ↔ unique current membership with identical IDs/versions
```

Status: focused public-domain runtime probes observed before and after repair. The integrator ran `bun run check:changed` and `bun run check:changed:full` in the isolated `overnight-integration` worktree; both passed. `git diff --no-index` confirmed that its repaired source matches the main-worktree source byte-for-byte. This is still an unconsumed leaf, not end-to-end valuation support. No new test file was added for this bounded repair.

## Observed counterexamples and regression outcomes

Both executions of the command below exited 0 within the 20-second tool deadline. It prints observed results rather than treating an expected pre-repair defect as a process failure. The exact observed financial fields are recorded below; `M = 99999999999999999999999999999999999999` (`10^38 − 1`). Journal tuples are `[account, debit, credit]`; all amounts are decimal strings.

| Case | Before repair | After repair / expected outcome |
| --- | --- | --- |
| `mixed_controls` | Targets `[115000,115000]`, deltas `[5000,5000]`; journal `[[ar_control,5000,0],[fx_gain,0,5000],[ar_control,0,5000],[fx_loss,5000,0]]` | Same targets/deltas; journal `[[ar_control,5000,0],[fx_gain,0,5000],[ap_control,0,5000],[fx_loss,5000,0]]` |
| `overflow` | Success: target `199999999999999999999999999999999999998`, delta `M`; journal `[[ar_control,M,0],[fx_gain,0,M]]`; `validPlan:false` | `AmountOutOfRange` |
| `coarser_scale` | `UnsupportedScale` | Target `1100`, delta `100`; journal `[[ar_control,100,0],[fx_gain,0,100]]` |
| `empty` | `SchemaRejected` | Empty targets, deltas, predecessors, journal and membership; `voucher:false` |
| `duplicate_current` | `Success` for approved `[A1,B1]`, current `[A1,A1]` | `StalePopulation` |
| `duplicate_plan` | `Success` for approved/current `[A1,A1]` | `StalePopulation` |
| `boundary` | Target/delta `M`; journal `[[ar_control,M,0],[fx_gain,0,M]]` | Identical success at the codec ceiling |
| `zero_delta` | Target `115000`, delta `0`; empty journal, one member, `voucher:false` | Identical success |
| `half_up` | `UnsupportedScale` | `1005 × 10² / 10³ = 100.5` rounds once to `101`; delta `1`; journal `[[ar_control,1,0],[fx_gain,0,1]]` |
| `inexact` | `UnsupportedScale` | `UnsupportedRate` because exact rounding cannot represent `100.5` |
| `incomplete` | `IncompletePopulation` | Identical refusal |
| `duplicate_items` | `DuplicateItem` | Identical refusal |
| `later_consumption` | `UnsupportedLaterConsumption` | Identical refusal |
| `supersession` | Target `120000`, delta `5000`, predecessor `effect_one`; journal `[[ar_control,5000,0],[fx_gain,0,5000]]` | Identical success: subtract current `115000`, not initial `110000` |
| `reordered` | `Success` for `[B1,A1]` | Identical success |
| `changed_version` | `StalePopulation` for `[A1,B2]` | Identical refusal |
| `replacement` | `StalePopulation` for `[A1,C1]` | Identical refusal |
| `new_member` | `StalePopulation` for `[A1,B1,C1]` | Identical refusal |

All successful post-repair plans passed `Schema.is(ValuationPlan)`. All pre-repair successful plans except `overflow` passed it. Successful nonempty financial journals consume a voucher; mixed controls retain two members and all other nonempty cases retain one. Predecessors are null except for `supersession`.

The target bound is checked against the existing `MinorUnits` schema, not a separate copied numeric limit. The absolute journal delta is checked against the same schema. Membership comparison first rejects duplicate approved IDs, then consumes each matching ID/version exactly once; equal initial lengths therefore establish set equality without rejecting reorderings. The shared purchasing validator was not edited.

## Repeatable command

Run from `/Users/admin/openERP/packages/domain` using `bun -e` below. This exact probe was executed before editing production code and again afterward. For the old result, use the baseline leaf at `0bebac5` in a separately coordinated checkout; do not overwrite an active worktree. The probe deliberately supplies both the old selection-level and new item-level control fields so the same command works across the contract change. Effect Schema strips fields absent from the schema; the repaired schema requires each item binding.

```bash
bun -e '
import * as S from "effect/Schema";
import * as R from "effect/Result";
import * as F from "@open-erp/domain/fx-remeasurement";
const item = { itemId: "item_aaa", direction: "receivable", controlAccountId: "ar_control", remainingOriginalMinor: "10000", originalScale: 2, currentBookCarryingMinor: "110000", capacityVersion: "1", consumedAfterCutoff: false, rateRevisionId: "rate_one", rateNumerator: "23", rateDenominator: "2", rounding: "exact" };
const base = { currency: "EUR", accountingCutoff: "2026-09-30", recordedCutoff: "2026-09-30T12:00:00Z", complete: true, expectedItemCount: 1, bookScale: 2, controlAccountId: "ar_control", unrealizedGainAccountId: "fx_gain", unrealizedLossAccountId: "fx_loss", economicDecisionId: "decision_one", supersedesEffectId: null, items: [item] };
const other = { ...item, itemId: "item_bbb", direction: "payable", controlAccountId: "ap_control" };
const max = (10n ** 38n - 1n).toString();
const cases = [
  ["mixed_controls", { ...base, expectedItemCount: 2, items: [item, other] }],
  ["overflow", { ...base, items: [{ ...item, remainingOriginalMinor: max, currentBookCarryingMinor: max, rateNumerator: "2", rateDenominator: "1" }] }],
  ["coarser_scale", { ...base, items: [{ ...item, remainingOriginalMinor: "1000", originalScale: 3, currentBookCarryingMinor: "1000", rateNumerator: "11", rateDenominator: "1" }] }],
  ["empty", { ...base, expectedItemCount: 0, items: [] }],
  ["boundary", { ...base, items: [{ ...item, remainingOriginalMinor: max, currentBookCarryingMinor: "0", rateNumerator: "1", rateDenominator: "1" }] }],
  ["zero_delta", { ...base, items: [{ ...item, currentBookCarryingMinor: "115000" }] }],
  ["half_up", { ...base, items: [{ ...item, remainingOriginalMinor: "1005", originalScale: 3, currentBookCarryingMinor: "100", rateNumerator: "1", rateDenominator: "1", rounding: "half_up" }] }],
  ["inexact", { ...base, items: [{ ...item, remainingOriginalMinor: "1005", originalScale: 3, currentBookCarryingMinor: "100", rateNumerator: "1", rateDenominator: "1" }] }],
  ["incomplete", { ...base, complete: false }],
  ["duplicate_items", { ...base, expectedItemCount: 2, items: [item, item] }],
  ["later_consumption", { ...base, items: [{ ...item, consumedAfterCutoff: true }] }],
  ["supersession", { ...base, supersedesEffectId: "effect_one", items: [{ ...item, currentBookCarryingMinor: "115000", rateNumerator: "12", rateDenominator: "1" }] }]
];
for (const [name, input] of cases) {
  const decoded = S.decodeUnknownResult(F.ValuationSelection)(input);
  if (R.isFailure(decoded)) { console.log(name, "SchemaRejected"); continue; }
  const result = F.prepareValuation(decoded.success);
  if (R.isFailure(result)) { console.log(name, result.failure.code); continue; }
  const p = result.success;
  console.log(name, JSON.stringify({ validPlan: S.is(F.ValuationPlan)(p), targets: p.effects.map(e => e.targetCarryingMinor), deltas: p.effects.map(e => e.deltaMinor), predecessors: p.effects.map(e => e.predecessorEffectId), journal: p.journal.map(l => [l.accountId, l.debitMinor, l.creditMinor]), members: p.membership.length, voucher: p.consumesVoucher }));
}
const planned = F.prepareValuation(S.decodeUnknownSync(F.ValuationSelection)({ ...base, expectedItemCount: 2, items: [item, other] }));
if (R.isFailure(planned)) throw new Error(planned.failure.code);
const plan = planned.success;
const [a, b] = plan.membership;
for (const [name, saved, current] of [
  ["duplicate_current", plan, [a, a]],
  ["duplicate_plan", { ...plan, membership: [a, a] }, [a, a]],
  ["reordered", plan, [b, a]],
  ["changed_version", plan, [a, { ...b, capacityVersion: "2" }]],
  ["replacement", plan, [a, { ...b, itemId: "item_ccc" }]],
  ["new_member", plan, [a, b, { ...b, itemId: "item_ccc" }]]
]) {
  const result = F.assertValuationMembership(S.decodeUnknownSync(F.ValuationPlan)(saved), S.decodeUnknownSync(S.Array(F.ValuationMembership))(current));
  console.log(name, R.isFailure(result) ? result.failure.code : "Success");
}
'
```

## Remaining integration obligations

No application consumes this leaf. Complete database capture, real calendar and currency/purpose scope validation, approved reporting-rate qualification/withdrawal checks, population/version staleness under locks, atomic effects/journal/receipt persistence and economic uniqueness remain application-owner work. Later settlement must consume valuation-adjusted carrying through the existing commerce owner. `carryingAfter` remains an unchecked arithmetic helper, not a release-capacity validator. This repair provides no HTTP/MCP, PostgreSQL or end-to-end valuation evidence.
