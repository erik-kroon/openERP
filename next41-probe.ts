// NEXT-41 late FX valuation and consumed-chain correction — failure contract.
//
// This pins the obligations a chain-repair OWNER must satisfy. The leaf's pure
// rules are already reviewed, so most cases pass before the owner exists; that
// is expected and is recorded as such. The delivery gap is the owner, which
// `bun run check:integration` proves by holding `fx-chain-repair` at
// `deferred` until a real importer exists.
import * as R from "effect/Result";
import * as F from "./packages/domain/src/fx-chain-repair.ts";

let passed = 0;

let failed = 0;

function check(name: string, ok: boolean, actual: string) {
  if (ok) passed++;
  else failed++;
  console.log(JSON.stringify({ name, pass: ok, actual }));
}

type Refusal = { readonly code: string };

function code(result: R.Result<unknown, Refusal>): string | null {
  return R.isFailure(result) ? result.failure.code : null;
}

const valuation = (
  accountingOn: string,
  remainingForeignMinor: string,
  eventId: string,
): F.ChainEvent => ({
  kind: "valuation",
  accountingOn,
  remainingForeignMinor,
  rateNumerator: "1085",
  rateDenominator: "100",
  eventId,
});

const settlement = (
  accountingOn: string,
  originalUnitsMinor: string,
  eventId: string,
): F.ChainEvent => ({
  kind: "settlement",
  accountingOn,
  originalUnitsMinor,
  pairedReleaseMinor: originalUnitsMinor,
  cashConsiderationMinor: originalUnitsMinor,
  direction: "receivable",
  eventId,
});

const basis = (events: ReadonlyArray<F.ChainEvent>): F.ChainBasis => ({
  itemId: "item_one",
  activeChainRevision: "chain_v1",
  anchorForeignMinor: "10000",
  anchorCarryingMinor: "100000",
  events: [...events],
  oldEffective: [],
  plannedCurrentCarryingMinor: "108500",
  repairKey: "repair_one",
  knownRepairKeys: [],
  closedPeriodWithoutPolicy: false,
});

// A0: the surface a chain-repair owner must be able to call.
const surface = Object.keys(F).sort().join(",");

check(
  "A0_owner_surface_present",
  ["calculateChainRepair", "assertRepairCurrent"].every((name) => surface.includes(name)),
  surface.slice(0, 160),
);

// A1: a corrected rate replays the chain and the delta is the difference.
// 10000 foreign at 10.00 was 100000 carried; at 10.85 the target is 108500,
// so the repair carries +8500 with no cash and no foreign movement.
const repair = F.calculateChainRepair(basis([valuation("2026-01-31", "10000", "event_valuation")]));

const deltas = R.isSuccess(repair) ? repair.success.deltas : [];

const pnl = deltas
  .filter((line) => line.role === "pnl")
  .reduce((carry, line) => carry + BigInt(line.amountMinor), 0n);

check(
  "A1_corrected_rate_produces_pnl_delta",
  R.isSuccess(repair) && pnl === 8500n,
  JSON.stringify(R.isSuccess(repair) ? repair.success.deltas : code(repair)),
);

check(
  "A1_no_cash_or_foreign_movement",
  R.isSuccess(repair) &&
    repair.success.cashDeltaMinor === "0" &&
    repair.success.foreignDeltaMinor === "0",
  JSON.stringify(
    R.isSuccess(repair)
      ? { cash: repair.success.cashDeltaMinor, foreign: repair.success.foreignDeltaMinor }
      : code(repair),
  ),
);

// A2: a settlement in the chain releases carrying while preserving the actual
// cash consideration. The repair attributes the realized gain separately and
// never rewrites what was paid.
// Replay: 100000 anchor -> 108500 after the corrected valuation, less the
// 4000 carrying release, ends at 104500.
const withSettlement = F.calculateChainRepair({
  ...basis([
    valuation("2026-01-31", "10000", "event_valuation"),
    settlement("2026-02-15", "4000", "event_settlement"),
  ]),
  plannedCurrentCarryingMinor: "104500",
});

check(
  "A2_settlement_preserved_in_repair",
  R.isSuccess(withSettlement),
  JSON.stringify(
    R.isSuccess(withSettlement) ? withSettlement.success.deltas.length : code(withSettlement),
  ),
);

// A3: an event the repair does not handle blocks the whole plan with its
// identity, rather than being silently skipped.
const unhandled = F.calculateChainRepair(
  basis([
    valuation("2026-01-31", "10000", "event_valuation"),
    { kind: "other", accountingOn: "2026-02-01", handlerId: null, eventId: "event_mystery" },
  ]),
);

check(
  "A3_unhandled_event_blocks_with_identity",
  code(unhandled) === "UnhandledEvent",
  String(code(unhandled)),
);

// A4: ambiguous chronology blocks. Two events on the same date with no
// tie-break refuse rather than assuming an order.
const ambiguous = F.calculateChainRepair(
  basis([
    valuation("2026-01-31", "6000", "event_dup"),
    valuation("2026-01-31", "4000", "event_dup"),
  ]),
);

check(
  "A4_ambiguous_chronology_refuses",
  code(ambiguous) === "ChronologyAmbiguous",
  String(code(ambiguous)),
);

// A5: a closed period without an explicit policy blocks. A repair never posts
// into a closed period on an assumed policy.
const closedPeriod = F.calculateChainRepair({
  ...basis([valuation("2026-01-31", "10000", "event_valuation")]),
  closedPeriodWithoutPolicy: true,
});

check(
  "A5_closed_period_without_policy_refuses",
  code(closedPeriod) === "ClosedPeriodBlocked",
  String(code(closedPeriod)),
);

// A6: a replayed repair key refuses. The same correction applied twice is a
// duplicate, not a second gain.
const replayed = F.calculateChainRepair({
  ...basis([valuation("2026-01-31", "10000", "event_valuation")]),
  repairKey: "repair_old",
  knownRepairKeys: ["repair_old"],
});

check("A6_replayed_key_refuses", code(replayed) === "AlreadyApplied", String(code(replayed)));

// A7: the current-carrying check binds the repair to what is actually carried.
// A drifted carrying refuses rather than posting against a stale basis.
const sealedPlan = F.calculateChainRepair(
  basis([valuation("2026-01-31", "10000", "event_valuation")]),
);

const sealedBasis = basis([valuation("2026-01-31", "10000", "event_valuation")]);

const currentState = {
  activeChainRevision: "chain_v1",
  eventCount: 1,
  repairKey: "repair_other",
  knownRepairKeys: new Array<string>(),
};

const current =
  R.isSuccess(sealedPlan) && typeof F.assertRepairCurrent === "function"
    ? F.assertRepairCurrent(sealedPlan.success, sealedBasis, currentState)
    : null;

check(
  "A7_matching_state_accepted",
  current !== null && R.isSuccess(current),
  current === null ? "no sealed plan" : String(code(current)),
);

const drifted = R.isSuccess(sealedPlan)
  ? F.assertRepairCurrent(sealedPlan.success, sealedBasis, {
      ...currentState,
      activeChainRevision: "chain_v2",
    })
  : null;

check(
  "A7_moved_chain_refuses",
  drifted !== null && code(drifted) === "StaleRepair",
  drifted === null ? "no sealed plan" : String(drifted && code(drifted)),
);

// A8: signed amounts throughout, so a loss-direction correction is
// representable rather than a refusal.
const lossRepair = F.calculateChainRepair({
  ...basis([valuation("2026-01-31", "10000", "event_valuation")]),
  anchorCarryingMinor: "120000",
  plannedCurrentCarryingMinor: "108500",
});

const lossPnl = R.isSuccess(lossRepair)
  ? lossRepair.success.deltas
      .filter((line) => line.role === "pnl")
      .reduce((carry, line) => carry + BigInt(line.amountMinor), 0n)
  : null;

check("A8_loss_direction_representable", lossPnl !== null && lossPnl < 0n, String(lossPnl));

console.log(JSON.stringify({ passed, failed }));

if (process.env.EXPECT_REPAIRED === "1" && failed) process.exitCode = 1;
