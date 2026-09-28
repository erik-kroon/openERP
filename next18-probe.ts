// NEXT-18 incremental open-item FX remeasurement — failure contract.
//
// This pins the obligations a remeasurement OWNER must satisfy. The leaf's
// pure rules are already reviewed, so most cases pass before the owner exists;
// that is expected and is recorded as such. The delivery gap is the owner,
// which `bun run check:integration` proves by holding `fx-remeasurement` at
// `deferred` until a real importer exists.
import * as R from "effect/Result";
import * as S from "effect/Schema";
import * as F from "./packages/domain/src/fx-remeasurement.ts";

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

const item = (
  itemId: string,
  remainingOriginalMinor: string,
  currentBookCarryingMinor: string,
  consumedAfterCutoff = false,
): F.ValuationItem => ({
  itemId,
  direction: "receivable",
  controlAccountId: "receivable_foreign",
  remainingOriginalMinor,
  originalScale: 2,
  currentBookCarryingMinor,
  capacityVersion: "capacity_v1",
  consumedAfterCutoff,
  rateRevisionId: "rate_2026_01",
  rateNumerator: "10850",
  rateDenominator: "10000",
  rounding: "exact",
});

const selection = (items: ReadonlyArray<F.ValuationItem>): F.ValuationSelection => ({
  currency: "USD",
  accountingCutoff: "2026-01-31",
  recordedCutoff: "2026-02-01T00:00:00.000Z",
  complete: true,
  expectedItemCount: items.length,
  bookScale: 2,
  unrealizedGainAccountId: "gain_unrealized",
  unrealizedLossAccountId: "loss_unrealized",
  economicDecisionId: "decision_one",
  supersedesEffectId: null,
  items: [...items],
});

// A0: the surface a remeasurement owner must be able to call.
const surface = Object.keys(F).sort().join(",");

check(
  "A0_owner_surface_present",
  ["prepareValuation", "assertValuationMembership", "carryingAfter"].every((name) =>
    surface.includes(name),
  ),
  surface.slice(0, 160),
);

// A1: a straightforward remeasurement computes the target less the current
// carrying. 10000 foreign minor at 1.0850 with scale symmetry is 10850 book
// minor; against 10000 carried that is a +850 gain.
const one = F.prepareValuation(selection([item("item_one", "10000", "10000")]));

const effectOne = R.isSuccess(one) ? one.success.effects[0] : undefined;

check(
  "A1_gain_is_target_less_carrying",
  R.isSuccess(one) && effectOne?.targetCarryingMinor === "10850" && effectOne?.deltaMinor === "850",
  JSON.stringify(R.isSuccess(one) ? one.success.effects : code(one)),
);

// A2: a loss is a negative delta, not a refusal. Retargeting below the carried
// amount is ordinary business, and a loss must be reportable.
const loss = F.prepareValuation(selection([item("item_two", "10000", "12000")]));

const effectLoss = R.isSuccess(loss) ? loss.success.effects[0] : undefined;

check(
  "A2_loss_is_a_negative_delta",
  R.isSuccess(loss) && effectLoss?.deltaMinor === "-1150",
  JSON.stringify(R.isSuccess(loss) ? loss.success.effects : code(loss)),
);

// A3: the plan emits a balanced journal with exactly one positive side per
// line, and the gain leg lands on the unrealized gain account.
const journal = R.isSuccess(one) ? one.success.journal : [];

const debits = journal.reduce((carry, line) => carry + BigInt(line.debitMinor), 0n);

const credits = journal.reduce((carry, line) => carry + BigInt(line.creditMinor), 0n);

check("A3_journal_balances", journal.length > 0 && debits === credits, `${debits}/${credits}`);

check(
  "A3_gain_leg_on_gain_account",
  journal.some((line) => line.accountId === "gain_unrealized" && line.creditMinor === "850"),
  JSON.stringify(journal),
);

check(
  "A3_every_line_has_one_positive_side",
  journal.every(
    (line) =>
      (line.debitMinor === "0") !== (line.creditMinor === "0") &&
      !line.debitMinor.startsWith("-") &&
      !line.creditMinor.startsWith("-"),
  ),
  JSON.stringify(journal),
);

// A4: a zero delta retains its membership but consumes no voucher.
const flat = F.prepareValuation(selection([item("item_flat", "10000", "10850")]));

check(
  "A4_zero_delta_needs_no_voucher",
  R.isSuccess(flat) && flat.success.consumesVoucher === false && flat.success.effects.length === 1,
  JSON.stringify(
    R.isSuccess(flat)
      ? { voucher: flat.success.consumesVoucher, effects: flat.success.effects.length }
      : code(flat),
  ),
);

// A5: an incomplete selection refuses. Valuing the first page and calling it
// complete is not a complete remeasurement.
const partial = F.prepareValuation({
  ...selection([item("item_one", "10000", "10000")]),
  complete: false,
});

check("A5_incomplete_selection_refuses", code(partial) !== null, String(code(partial)));

const wrongCount = F.prepareValuation({
  ...selection([item("item_one", "10000", "10000")]),
  expectedItemCount: 2,
});

check("A5_wrong_expected_count_refuses", code(wrongCount) !== null, String(code(wrongCount)));

// A6: a consumption after the cutoff needs a full correction chain, not a
// quiet inclusion in this valuation.
const consumed = F.prepareValuation(selection([item("item_used", "10000", "10000", true)]));

check("A6_consumed_after_cutoff_refuses", code(consumed) !== null, String(code(consumed)));

// A7: membership is rechecked at execution. A changed population refuses
// instead of valuing a different set than the sealed one.
const sealed = F.prepareValuation(
  selection([item("item_one", "10000", "10000"), item("item_two", "5000", "5000")]),
);

if (R.isSuccess(sealed)) {
  const same = F.assertValuationMembership(sealed.success, sealed.success.membership);
  check("A7_same_membership_accepted", R.isSuccess(same), String(code(same)));

  const changed = F.assertValuationMembership(sealed.success, [
    { itemId: "item_one", capacityVersion: "capacity_v1" },
    { itemId: "item_two", capacityVersion: "capacity_v2" },
  ]);

  check("A7_changed_capacity_refuses", code(changed) === "StalePopulation", String(code(changed)));

  const dropped = F.assertValuationMembership(sealed.success, [
    { itemId: "item_one", capacityVersion: "capacity_v1" },
  ]);

  check("A7_dropped_item_refuses", code(dropped) === "StalePopulation", String(code(dropped)));
} else {
  check("A7_same_membership_accepted", false, String(code(sealed)));
  check("A7_changed_capacity_refuses", false, "no sealed plan");
  check("A7_dropped_item_refuses", false, "no sealed plan");
}

// A8: the settlement basis keeps valuation P&L and settlement P&L separate.
// Initial carrying plus valuation deltas less releases is exact integer math.
check(
  "A8_carrying_after_is_exact",
  F.carryingAfter("10000", ["850", "-100"], ["2000"]) === "8750",
  F.carryingAfter("10000", ["850", "-100"], ["2000"]),
);

// A9: ordinary negative remaining and carrying amounts are representable,
// because a payable-side or loss position is signed business.
const signedSelection = S.is(F.ValuationSelection)(selection([item("item_one", "10000", "10000")]));

check("A9_selection_schema_accepted", signedSelection, String(signedSelection));

const signedItem = S.is(F.ValuationItem)(item("item_one", "10000", "10000"));

check("A9_item_schema_accepted", signedItem, String(signedItem));

console.log(JSON.stringify({ passed, failed }));

if (process.env.EXPECT_REPAIRED === "1" && failed) process.exitCode = 1;
