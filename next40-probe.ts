// NEXT-40 foreign-cash failure contract. Written before any production edit.
// It exercises only the public exported schema and function surface of
// packages/domain/src/foreign-cash.ts. New reviewed inputs (scales, target
// currency) are supplied from the outset; the pre-repair signatures ignore
// them, so one command runs before and after. Every case is recorded.

import * as Result from "effect/Result";
import * as Schema from "effect/Schema";

import { MinorUnits, SignedMinorUnits } from "./packages/domain/src/money.ts";
import * as Cash from "./packages/domain/src/foreign-cash.ts";

type Report = { readonly pass: boolean; readonly actual: string };

let passed = 0;

let failed = 0;

const observedCodes = new Set<string>();

function record(name: string, pass: boolean, actual: string) {
  if (pass) {
    passed += 1;
  } else {
    failed += 1;
  }

  console.log(JSON.stringify({ name, pass, actual }));
}

function run(name: string, report: () => Report) {
  try {
    const result = report();
    record(name, result.pass, result.actual);
  } catch (error) {
    record(
      name,
      false,
      JSON.stringify({ threw: error instanceof Error ? error.message : String(error) }),
    );
  }
}

function outcome<A>(result: Result.Result<A, Cash.ForeignCashFailure>) {
  const detail = Result.isFailure(result)
    ? { code: result.failure.code, message: result.failure.message }
    : { code: "succeeded", value: JSON.stringify(result.success) };

  if (detail.code !== "succeeded") observedCodes.add(detail.code);

  return detail;
}

function refuses<A>(result: Result.Result<A, Cash.ForeignCashFailure>, expected: string): Report {
  const detail = outcome(result);

  return { pass: detail.code === expected, actual: JSON.stringify(detail) };
}

function journal(
  result: Result.Result<Cash.ForeignCashJournalLines, Cash.ForeignCashFailure>,
  expected: ReadonlyArray<ReadonlyArray<string>>,
): Report {
  const detail = outcome(result);

  if (Result.isFailure(result)) return { pass: false, actual: JSON.stringify(detail) };

  const emitted = result.success.map((line) => [line.accountId, line.debitMinor, line.creditMinor]);

  const bounded = Schema.is(Cash.ForeignCashJournalLines)(result.success);

  const singleSide = result.success.every((line) => {
    const debit = BigInt(line.debitMinor);
    const credit = BigInt(line.creditMinor);

    return (debit > 0n && credit === 0n) || (debit === 0n && credit > 0n);
  });

  const net = result.success.reduce(
    (sum, line) => sum + BigInt(line.debitMinor) - BigInt(line.creditMinor),
    0n,
  );

  const same = JSON.stringify(emitted) === JSON.stringify(expected);

  return {
    pass: bounded && singleSide && net === 0n && same,
    actual: JSON.stringify({ bounded, singleSide, balanced: net === 0n, same, lines: emitted }),
  };
}

function plan(
  result: Result.Result<Cash.CashWithdrawalPlan, Cash.ForeignCashFailure>,
  nativeConsumed: string,
  carryingReleased: string,
): Report {
  const detail = outcome(result);

  if (Result.isFailure(result)) return { pass: false, actual: JSON.stringify(detail) };

  const valid = Schema.is(Cash.CashWithdrawalPlan)(result.success);

  const same =
    result.success.nativeConsumedMinor === nativeConsumed &&
    result.success.carryingReleasedMinor === carryingReleased;

  return { pass: valid && same, actual: JSON.stringify({ valid, same, plan: result.success }) };
}

function valuation(
  result: Result.Result<
    { readonly targetMinor: string; readonly deltaMinor: string },
    Cash.ForeignCashFailure
  >,
  target: string,
  delta: string,
): Report {
  const detail = outcome(result);

  if (Result.isFailure(result)) return { pass: false, actual: JSON.stringify(detail) };

  const same = result.success.targetMinor === target && result.success.deltaMinor === delta;
  const signedDelta = Schema.is(SignedMinorUnits)(result.success.deltaMinor);
  const unsignedTarget = Schema.is(MinorUnits)(result.success.targetMinor);

  return {
    pass: same && signedDelta && unsignedTarget,
    actual: JSON.stringify({ same, signedDelta, unsignedTarget, valuation: result.success }),
  };
}

const account = {
  sourceAccountId: "cash_eur",
  nativeCurrency: "EUR",
  bookCurrency: "SEK",
  nativeScale: 2,
  reviewedOpeningNativeMinor: "10000",
  reviewedOpeningCarryingMinor: "110000",
};

const basis = {
  originalNativeMinor: "10000",
  originalCarryingMinor: "110000",
  consumedNativeMinor: "0",
  releasedCarryingMinor: "0",
  capacityVersion: "cv_1",
};

const afterPartial = { ...basis, consumedNativeMinor: "4000", releasedCarryingMinor: "44000" };

const maximum = "9".repeat(38);

console.log("capture");

run("account_not_denominated_away_from_book_currency", () =>
  refuses(
    Cash.captureCashBasis({ ...account, nativeCurrency: "SEK" }, basis),
    "NotForeignCashAccount",
  ),
);

run("capture_opening_native_mismatch", () =>
  refuses(
    Cash.captureCashBasis(account, { ...basis, originalNativeMinor: "10001" }),
    "OpeningMismatch",
  ),
);

run("capture_opening_carrying_mismatch", () =>
  refuses(
    Cash.captureCashBasis(account, { ...basis, originalCarryingMinor: "109999" }),
    "OpeningMismatch",
  ),
);

run("capture_remaining_after_partial_withdrawal", () => {
  const result = Cash.captureCashBasis(account, afterPartial);

  const detail = outcome(result);

  const valid = Result.isSuccess(result) && Schema.is(Cash.RemainingHolding)(result.success);

  const same =
    Result.isSuccess(result) &&
    result.success.nativeUnitsMinor === "6000" &&
    result.success.carryingMinor === "66000" &&
    result.success.capacityVersion === "cv_1";

  return { pass: valid && same, actual: JSON.stringify({ valid, same, remaining: detail }) };
});

run("capture_residual_carrying_without_units_refused", () =>
  refuses(
    Cash.captureCashBasis(account, {
      ...basis,
      consumedNativeMinor: "10000",
      releasedCarryingMinor: "50000",
    }),
    "ResidualCarryingWithoutUnits",
  ),
);

run("capture_negative_holding_refused", () =>
  refuses(
    Cash.captureCashBasis(account, { ...basis, consumedNativeMinor: "12000" }),
    "NegativeHolding",
  ),
);

run("account_and_basis_schema_bounds", () => {
  const accountValid = Schema.is(Cash.ForeignCashAccount)(account);

  const basisValid = Schema.is(Cash.CashHoldingBasis)(basis);

  const oversized = Schema.is(Cash.ForeignCashAccount)({
    ...account,
    reviewedOpeningNativeMinor: "1".repeat(39),
  });

  return {
    pass: accountValid && basisValid && !oversized,
    actual: JSON.stringify({ accountValid, basisValid, oversizedAccepted: oversized }),
  };
});

console.log("withdrawal");

run("withdraw_releases_exact_proportional_share", () =>
  plan(Cash.planCashWithdrawal(basis, "4000", "exact"), "4000", "44000"),
);

run("withdraw_all_remaining_releases_all_carrying", () =>
  plan(Cash.planCashWithdrawal(afterPartial, "6000", "exact"), "6000", "66000"),
);

run("withdraw_over_remaining_units_refused", () =>
  refuses(Cash.planCashWithdrawal(afterPartial, "6001", "exact"), "OverWithdrawal"),
);

run("withdraw_zero_refused", () =>
  refuses(Cash.planCashWithdrawal(basis, "0", "exact"), "NonPositiveAmount"),
);

run("withdraw_negative_refused", () =>
  refuses(Cash.planCashWithdrawal(basis, "-4000", "exact"), "NonPositiveAmount"),
);

run("withdraw_exact_rounding_residual_refused", () =>
  refuses(
    Cash.planCashWithdrawal(
      { ...basis, originalNativeMinor: "3", originalCarryingMinor: "100" },
      "1",
      "exact",
    ),
    "UnsupportedRounding",
  ),
);

run("withdraw_consumed_past_original_refused", () =>
  refuses(
    Cash.planCashWithdrawal({ ...basis, consumedNativeMinor: "20000" }, "1000", "exact"),
    "NegativeHolding",
  ),
);

run("withdraw_release_past_remaining_carrying_refused", () =>
  refuses(
    Cash.planCashWithdrawal(
      { ...basis, consumedNativeMinor: "3000", releasedCarryingMinor: "105000" },
      "4000",
      "exact",
    ),
    "OverWithdrawal",
  ),
);

run("withdraw_maximum_bounded_amounts", () =>
  plan(
    Cash.planCashWithdrawal(
      { ...basis, originalNativeMinor: maximum, originalCarryingMinor: maximum },
      maximum,
      "exact",
    ),
    maximum,
    maximum,
  ),
);

run("withdraw_malformed_amount_refused", () =>
  refuses(Cash.planCashWithdrawal(basis, "1000.00", "exact"), "AmountOutOfRange"),
);

run("withdraw_oversized_amount_refused", () =>
  refuses(Cash.planCashWithdrawal(basis, "1".repeat(39), "exact"), "AmountOutOfRange"),
);

run("withdraw_plan_echoes_capacity_version", () => {
  const result = Cash.planCashWithdrawal(basis, "4000", "exact");
  const same = Result.isSuccess(result) && result.success.capacityVersion === "cv_1";

  return { pass: same, actual: JSON.stringify({ same, plan: outcome(result) }) };
});

console.log("settlement");

run("settle_payable_realizes_gain", () =>
  journal(Cash.compilePayableFromForeignCash("payable", "cash", "gain", "loss", "45000", "44000"), [
    ["payable", "45000", "0"],
    ["cash", "0", "44000"],
    ["gain", "0", "1000"],
  ]),
);

run("settle_payable_realizes_loss", () =>
  journal(Cash.compilePayableFromForeignCash("payable", "cash", "gain", "loss", "44000", "45000"), [
    ["payable", "44000", "0"],
    ["cash", "0", "45000"],
    ["loss", "1000", "0"],
  ]),
);

run("settle_payable_without_difference", () =>
  journal(Cash.compilePayableFromForeignCash("payable", "cash", "gain", "loss", "44000", "44000"), [
    ["payable", "44000", "0"],
    ["cash", "0", "44000"],
  ]),
);

run("settle_negative_payable_release_refused", () =>
  refuses(
    Cash.compilePayableFromForeignCash("payable", "cash", "gain", "loss", "-5000", "1000"),
    "NonPositiveAmount",
  ),
);

run("settle_oversized_payable_release_refused", () =>
  refuses(
    Cash.compilePayableFromForeignCash("payable", "cash", "gain", "loss", "1".repeat(39), "1000"),
    "AmountOutOfRange",
  ),
);

run("settle_malformed_release_refused", () =>
  refuses(
    Cash.compilePayableFromForeignCash("payable", "cash", "gain", "loss", "1000,00", "1000"),
    "AmountOutOfRange",
  ),
);

run("settle_reference_outside_the_account_codec_refused", () => {
  const tooShort = refuses(
    Cash.compilePayableFromForeignCash("ar", "cash", "gain", "loss", "44000", "44000"),
    "UnbalancedJournal",
  );

  const tooLong = refuses(
    Cash.compilePayableFromForeignCash("a".repeat(200), "cash", "gain", "loss", "44000", "44000"),
    "UnbalancedJournal",
  );

  return {
    pass: tooShort.pass && tooLong.pass,
    actual: JSON.stringify({ tooShort, tooLong }),
  };
});

run("receipt_realizes_gain", () =>
  journal(Cash.receiveForeignCash("cash", "receivable", "gain", "loss", "105000", "100000"), [
    ["cash", "105000", "0"],
    ["receivable", "0", "100000"],
    ["gain", "0", "5000"],
  ]),
);

run("receipt_negative_book_value_refused", () =>
  refuses(
    Cash.receiveForeignCash("cash", "receivable", "gain", "loss", "-1000", "1000"),
    "NonPositiveAmount",
  ),
);

console.log("transfer");

run("transfer_moves_the_identical_pair", () =>
  journal(Cash.transferForeignCash("sender", "receiver", "1000", "11500"), [
    ["sender", "0", "11500"],
    ["receiver", "11500", "0"],
  ]),
);

run("transfer_without_carrying_has_no_zero_line", () =>
  journal(Cash.transferForeignCash("sender", "receiver", "1000", "0"), []),
);

run("transfer_zero_native_refused", () =>
  refuses(Cash.transferForeignCash("sender", "receiver", "0", "1000"), "NonPositiveAmount"),
);

run("transfer_negative_carrying_refused", () =>
  refuses(Cash.transferForeignCash("sender", "receiver", "1000", "-11500"), "NonPositiveAmount"),
);

run("transfer_oversized_carrying_refused", () =>
  refuses(
    Cash.transferForeignCash("sender", "receiver", "1000", "1".repeat(39)),
    "AmountOutOfRange",
  ),
);

console.log("exchange");

run("exchange_realizes_gain_on_the_net_receipt", () =>
  journal(
    Cash.exchangeToBookCash(
      "foreign",
      "bookcash",
      "fee",
      "gain",
      "loss",
      "44000",
      "105000",
      "500",
      true,
    ),
    [
      ["bookcash", "104500", "0"],
      ["fee", "500", "0"],
      ["foreign", "0", "44000"],
      ["gain", "0", "61000"],
    ],
  ),
);

run("exchange_fee_above_receipt_refused", () =>
  refuses(
    Cash.exchangeToBookCash(
      "foreign",
      "bookcash",
      "fee",
      "gain",
      "loss",
      "44000",
      "105000",
      "105001",
      true,
    ),
    "NonPositiveAmount",
  ),
);

run("exchange_negative_fee_refused", () =>
  refuses(
    Cash.exchangeToBookCash(
      "foreign",
      "bookcash",
      "fee",
      "gain",
      "loss",
      "44000",
      "105000",
      "-500",
      true,
    ),
    "NonPositiveAmount",
  ),
);

run("exchange_to_a_second_foreign_account_refused", () =>
  refuses(
    Cash.exchangeToBookCash(
      "foreign",
      "otherforeign",
      "fee",
      "gain",
      "loss",
      "44000",
      "105000",
      "500",
      false,
    ),
    "UnsupportedExchange",
  ),
);

run("exchange_oversized_receipt_refused", () =>
  refuses(
    Cash.exchangeToBookCash(
      "foreign",
      "bookcash",
      "fee",
      "gain",
      "loss",
      "44000",
      "1".repeat(39),
      "500",
      true,
    ),
    "AmountOutOfRange",
  ),
);

console.log("valuation");

run("valuation_same_scale_pair", () =>
  valuation(Cash.valueCashHolding("6000", "66000", "23", "2", false, 2, 2), "69000", "3000"),
);

run("valuation_scale_asymmetric_pair", () =>
  valuation(Cash.valueCashHolding("6000", "66000", "115", "10", false, 0, 2), "6900000", "6834000"),
);

run("valuation_negative_delta_is_preserved", () =>
  valuation(Cash.valueCashHolding("6000", "80000", "23", "2", false, 2, 2), "69000", "-11000"),
);

run("valuation_result_matches_a_declared_schema", () => {
  const result = Cash.valueCashHolding("6000", "66000", "23", "2", false, 2, 2);
  const valid = Result.isSuccess(result) && Schema.is(Cash.CashValuation)(result.success);

  return { pass: valid, actual: JSON.stringify({ valid, valuation: outcome(result) }) };
});

run("valuation_after_a_withdrawal_refused", () =>
  refuses(
    Cash.valueCashHolding("6000", "66000", "23", "2", true, 2, 2),
    "ConsumedHistoryValuation",
  ),
);

run("valuation_zero_rate_denominator_refused", () =>
  refuses(Cash.valueCashHolding("6000", "66000", "23", "0", false, 2, 2), "UnsupportedRate"),
);

run("valuation_negative_rate_numerator_refused", () =>
  refuses(Cash.valueCashHolding("1000", "110000", "-11", "1", false, 2, 2), "UnsupportedRate"),
);

run("valuation_fractional_minor_refused", () =>
  refuses(Cash.valueCashHolding("3", "7", "10", "4", false, 2, 2), "UnsupportedRate"),
);

run("valuation_outside_the_money_codec_refused", () =>
  refuses(Cash.valueCashHolding(maximum, maximum, maximum, "1", false, 2, 2), "AmountOutOfRange"),
);

run("valuation_negative_native_balance_refused", () =>
  refuses(Cash.valueCashHolding("-6000", "66000", "23", "2", false, 2, 2), "NegativeHolding"),
);

run("valuation_malformed_native_units_refused", () =>
  refuses(Cash.valueCashHolding("6e3", "66000", "23", "2", false, 2, 2), "AmountOutOfRange"),
);

console.log("failure contract");

run("every_observed_failure_matches_the_declared_failure_schema", () => {
  const undeclared = [...observedCodes].filter(
    (code) => !Schema.is(Cash.ForeignCashFailureCode)(code),
  );

  return {
    pass: undeclared.length === 0,
    actual: JSON.stringify({ observed: [...observedCodes].sort(), undeclared }),
  };
});

console.log(JSON.stringify({ passed, failed }));

if (process.env.EXPECT_REPAIRED === "1" && failed > 0) process.exitCode = 1;
