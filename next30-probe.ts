// NEXT-30 customer unapplied cash, paid credits and refunds — failure contract.
//
// This pins the obligations a surplus/paid-credit/refund OWNER must satisfy.
// The leaf's pure rules are already reviewed, so most cases pass before the
// owner exists; that is expected and is recorded as such. The delivery gap is
// the owner, which `bun run check:integration` proves by holding
// `customer-credits` at `deferred` until a real importer exists.
import * as R from "effect/Result";
import * as S from "effect/Schema";
import * as C from "./packages/domain/src/customer-credits.ts";

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

const legs = [{ invoiceId: "invoice_one", amountMinor: "8000", invoiceRemainingMinor: "8000" }];

// A0: the surface a surplus owner must be able to call.
const surface = Object.keys(C).sort().join(",");

check(
  "A0_owner_surface_present",
  [
    "deriveCustomerPosition",
    "compileCustomerReceipt",
    "compilePaidCustomerCredit",
    "applyCustomerCredit",
    "recordCustomerRefund",
    "refuseConsumedHistoryReversal",
  ].every((name) => surface.includes(name)),
  surface.slice(0, 160),
);

// A1: a receipt split across an invoice leg and a classified surplus. Cash
// 10000 with 8000 allocated leaves 2000 of unapplied cash, not a second sale.
const receipt = C.compileCustomerReceipt({
  customerId: "customer_one",
  currency: "SEK",
  cashMinor: "10000",
  legs,
  surplusClassification: "unapplied_cash",
  source: { kind: "new_cash", bankAccountId: "cash", evidenceId: "evidence_one" },
  receivableControlAccountId: "receivable",
  creditLiabilityAccountId: "liability",
});

const plan = R.isSuccess(receipt) ? receipt.success : undefined;

check(
  "A1_receipt_splits_allocation_and_surplus",
  plan !== undefined && plan.allocatedMinor === "8000" && plan.creditOriginMinor === "2000",
  JSON.stringify(plan ?? code(receipt)),
);

// A2: the journal balances with exactly one positive side per line, and the
// surplus leg lands on the customer-credit liability rather than revenue.
const journal = plan?.journal ?? [];

const debits = journal.reduce((carry, line) => carry + BigInt(line.debitMinor), 0n);

const credits = journal.reduce((carry, line) => carry + BigInt(line.creditMinor), 0n);

check("A2_journal_balances", journal.length > 0 && debits === credits, `${debits}/${credits}`);

check(
  "A2_surplus_leg_on_liability",
  journal.some((line) => line.accountId === "liability" && line.creditMinor === "2000"),
  JSON.stringify(journal),
);

check(
  "A2_every_line_has_one_positive_side",
  journal.every(
    (line) =>
      (line.debitMinor === "0") !== (line.creditMinor === "0") &&
      !line.debitMinor.startsWith("-") &&
      !line.creditMinor.startsWith("-"),
  ),
  JSON.stringify(journal),
);

// A3: an unreviewed taxable advance refuses toward its owner instead of
// becoming unapplied cash by default.
const advance = C.compileCustomerReceipt({
  customerId: "customer_one",
  currency: "SEK",
  cashMinor: "10000",
  legs: [],
  surplusClassification: null,
  source: { kind: "new_cash", bankAccountId: "cash", evidenceId: "evidence_one" },
  receivableControlAccountId: "receivable",
  creditLiabilityAccountId: "liability",
});

check(
  "A3_unclassified_surplus_refuses",
  code(advance) === "UnclassifiedSurplus",
  String(code(advance)),
);

// A4: a leg above its invoice remaining refuses. Over-allocation is not a
// larger credit.
const over = C.compileCustomerReceipt({
  customerId: "customer_one",
  currency: "SEK",
  cashMinor: "10000",
  legs: [{ invoiceId: "invoice_one", amountMinor: "10001", invoiceRemainingMinor: "8000" }],
  surplusClassification: "unapplied_cash",
  source: { kind: "new_cash", bankAccountId: "cash", evidenceId: "evidence_one" },
  receivableControlAccountId: "receivable",
  creditLiabilityAccountId: "liability",
});

check("A4_over_allocation_refuses", code(over) !== null, String(code(over)));

// A5: a receipt that exactly covers its legs creates no credit origin.
const exact = C.compileCustomerReceipt({
  customerId: "customer_one",
  currency: "SEK",
  cashMinor: "8000",
  legs,
  surplusClassification: "unapplied_cash",
  source: { kind: "new_cash", bankAccountId: "cash", evidenceId: "evidence_one" },
  receivableControlAccountId: "receivable",
  creditLiabilityAccountId: "liability",
});

check(
  "A5_exact_receipt_creates_no_credit",
  R.isSuccess(exact) && exact.success.creditOriginMinor === "0",
  JSON.stringify(R.isSuccess(exact) ? exact.success.creditOriginMinor : code(exact)),
);

// A6: the position separates what is still owed from what is credit. Gross
// 10000, credited 1000, paid 9500: 9000 net owed less 9500 paid leaves 0
// unpaid and a 500 credit principal.
const position = C.deriveCustomerPosition({
  originalGrossMinor: "10000",
  creditedMinor: "1000",
  paidMinor: "9500",
  consumedMinor: "0",
});

check(
  "A6_position_separates_owed_from_credit",
  R.isSuccess(position) &&
    position.success.unpaidARMinor === "0" &&
    position.success.creditPrincipalMinor === "500" &&
    position.success.remainingCreditMinor === "500",
  JSON.stringify(R.isSuccess(position) ? position.success : code(position)),
);

// A7: consumed credit beyond the principal refuses. A refund or application
// cannot spend what was never credit.
const overConsumed = C.deriveCustomerPosition({
  originalGrossMinor: "10000",
  creditedMinor: "1000",
  paidMinor: "9500",
  consumedMinor: "501",
});

check(
  "A7_consumed_beyond_principal_refuses",
  code(overConsumed) === "RefundExceedsPrincipal",
  String(code(overConsumed)),
);

// A8: a refund consumes the credit principal it names and no more.
const refund = C.recordCustomerRefund({
  customerId: "customer_one",
  currency: "SEK",
  remainingCreditMinor: "500",
  amountMinor: "200",
  source: { kind: "new_payment", bankAccountId: "cash", evidenceId: "evidence_one" },
  sourceCurrency: "SEK",
  creditLiabilityAccountId: "liability",
});

check(
  "A8_refund_consumes_principal",
  R.isSuccess(refund),
  JSON.stringify(R.isSuccess(refund) ? "accepted" : code(refund)),
);

const overRefund = C.recordCustomerRefund({
  customerId: "customer_one",
  currency: "SEK",
  remainingCreditMinor: "500",
  amountMinor: "501",
  source: { kind: "new_payment", bankAccountId: "cash", evidenceId: "evidence_one" },
  sourceCurrency: "SEK",
  creditLiabilityAccountId: "liability",
});

check("A8_refund_beyond_remaining_refuses", code(overRefund) !== null, String(code(overRefund)));

// A9: unsigned minor-unit amounts throughout, so a negative cash event or a
// negative allocation is unrepresentable rather than a signed surprise.
const negativeCash = S.is(C.CustomerReceiptInput)({
  customerId: "customer_one",
  currency: "SEK",
  cashMinor: "-100",
  legs: [],
  surplusClassification: "unapplied_cash",
  source: { kind: "new_cash", bankAccountId: "cash", evidenceId: "evidence_one" },
  receivableControlAccountId: "receivable",
  creditLiabilityAccountId: "liability",
});

check("A9_negative_cash_unrepresentable", negativeCash === false, String(negativeCash));

console.log(JSON.stringify({ passed, failed }));

if (process.env.EXPECT_REPAIRED === "1" && failed) process.exitCode = 1;
