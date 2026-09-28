# NEXT-38 leaf repair evidence

## Scope and status

Final verification: the isolated fast and full static gates passed, as did all
30 recorded domain probes after synchronization. See the isolated-gate receipt
below for exact paths, commands and the final source fingerprint. Application
integration remains open.

Bounded repair authorized on 2026-09-28. Owned files are this note and
`packages/domain/src/cash-method.ts`. Baseline: `21796374050134a1a6fb08b67bd60c30def53002`;
the leaf is unchanged at the start of this repair. No application consumers were
found at that revision. This is a breaking, unconsumed **leaf-only** contract change,
not application integration, accounting-profile activation or persistence proof.
The implementing worker was limited to these owned files and focused probes;
the coordinating integrator owns static verification and commits to main.

## Failure contract recorded before source changes

All numbers below are minor units. Purchase vectors use full original VAT
deductibility unless stated otherwise; sales must mirror signs and release no
input deduction. Each cash event has a distinct evidence ID.

1. Original net 100000 + VAT 25000: first payment 50000 releases net 40000 and
   VAT 10000. A second payment 50000 must do the same, without settling AP that
   never existed. Year-end then recognizes only 25000 (net 20000, VAT 5000).
   Baseline instead settles AP 50000 on the second payment and leaves year-end
   recognition at 75000.
2. Net 100 + VAT 12, payment 14 of gross 112 under half-up: a qualified
   gross-conserving split must succeed. Baseline independently rounds net to 13
   and VAT to 2 and refuses the unbalanced 15-versus-14 result.
3. An unpaid credit 75000 against gross 125000 leaves only 50000 eligible for
   later credit, payment or year-end recognition. Baseline cannot carry credit
   consumption in its original-line state and recognizes all 125000 at year-end.
4. Recognized gross 50000 implies released deductible 10000 for that fully
   deductible original. Retained deduction 9000 (or 11000) must be refused, not
   silently reconciled. Baseline accepts 9000 and releases 15000 more.
5. Duplicate year-end source-line IDs must be refused, not recognized twice.
6. Year-end position settlement must emit bank/control only, VAT delta zero.
   Once paid or credited in full, a line/position cannot be consumed again.
7. Stale checks must include effective paid/credited and deduction state, even
   if a caller has failed to advance the opaque recognition version.

## Selected data meaning (before implementation)

Original `netMinor`, `taxMinor` and `originalDeductibleMinor` remain immutable.
The line carries:

- `creditedGrossMinor` (C): effective unpaid credit coverage; never paid refunds.
- `paidGrossMinor` (P): historical effective cash principal consumed, including
  later settlement of year-end recognition. No reversal/refund is synthesized.
- `recognizedGrossMinor` (R): cumulative effective recognition after recognized
  credit corrections, including the paid portion.
- `releasedDeductibleMinor`: cumulative effective deduction after corrections.
- `recognizedVersion`: caller-owned revision witness, retained in proposed
  returned state; the application must assign a fresh revision when persisting.

For original gross G, require `0 <= P <= R <= G-C <= G`. Derive, rather than
store competing copies:

```text
commercial unpaid       = G - C - P
recognized unpaid       = R - P
unrecognized outstanding = G - C - R
```

The qualified scalar-coverage policy keeps paid and recognized coverage as
prefixes of original gross, and unpaid credits consume the remaining suffix.
A credit first removes unrecognized suffix coverage, then recognized-unpaid
coverage; it never removes the paid prefix. Its supplied recognized portion must
equal that split. Arbitrary interior coverage, paid-principal refunds and
historical corrections that break this ordering are unsupported, not guessed.
This policy preserves original component identity without rescaling the invoice.

The explicit input literal `componentPolicy: "tax_first_cumulative_v1"` selects
this new leaf's component allocation. At effective coverage x:

```text
tax(x)        = round(originalTax * x / originalGross)
net(x)        = x - tax(x)
deductible(x) = round(originalDeductible * tax(x) / originalTax)
```

Zero original tax implies zero deduction. Full coverage releases exact original
totals. `rounding` remains explicitly `exact` or `half_up`. Deduction is split
within released tax so its incremental release cannot exceed incremental tax;
no tax rate or deduction entitlement is invented. At gross 14 of 112, the selected
split is net 12, tax 2. Retained deduction must match this **named** policy;
incompatible histories are refused, never coerced. Prior net/tax histories and
the policy/version witness still require application qualification before use.

Payment returns updated line state, advancing P by principal and R only by new
recognition. Year-end advances R to G-C. Credit returns updated line state and
the exact net/tax/deduction correction derived from old minus new cumulative
recognition. This is a correction vector, not a posted credit or tax fact.
The standalone recognized-position helper remains a separate no-tax compiler;
it must carry consumed/credited position state forward and cannot independently
update an application's line projection or establish cash-event identity.

## Verification plan

Before changing source, run bounded public-domain probes and record their exact
results. After changes, repeat the baseline vectors using the new explicit input
contract, feed returned state into each next call, and verify credit/correction,
sale signs, stale-state and consumed-position controls. Retain commands here.
No database, network, shared check runner or application writes are involved.

### Repeatable public-domain regression command

Run from `/Users/admin/openERP`. The following command executes the JavaScript
fence below directly from this note, without creating a test file. Prefix it with
`NEXT38_BASELINE=1` to load the pinned old leaf and purchasing dependency entirely
in memory; omit the prefix to load the working leaf. Baseline state adapters only
carry the old function's returned recognition forward; they do not repair it.
The baseline is expected to exit 1. The repaired leaf must exit 0.

```sh
bun -e 'const note = await Bun.file("docs/plans/evidence/next-38-leaf-review.md").text(); const script = note.split("```javascript\n")[1].split("\n```")[0]; await import("data:text/javascript;base64," + Buffer.from(script).toString("base64"));'
```

```javascript
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { pathToFileURL } from "node:url";

const root = process.cwd() + "/packages/domain/src";
const baseline = process.env.NEXT38_BASELINE === "1";
const transpiler = new Bun.Transpiler({ loader: "ts" });
function pinned(file, overrides = {}) {
  const source = execFileSync("git", ["show", "2179637:packages/domain/src/" + file], { encoding: "utf8" });
  const js = transpiler.transformSync(source).replace(/from "([^"]+)"/g,
    (_, name) => "from " + JSON.stringify(overrides[name] ?? pathToFileURL(Bun.resolveSync(name, root)).href));
  return "data:text/javascript;base64," + Buffer.from(js).toString("base64");
}
const m = await import(baseline
  ? pinned("cash-method.ts", { "./purchasing": pinned("purchasing.ts") })
  : pathToFileURL(root + "/cash-method.ts").href);
const original = {
  sourceLineId: "line_1", netMinor: "100000", taxMinor: "25000",
  originalDeductibleMinor: "25000", releasedDeductibleMinor: "0",
  recognizedGrossMinor: "0", paidGrossMinor: "0", creditedGrossMinor: "0",
  recognizedVersion: "v1", componentPolicy: "tax_first_cumulative_v1", rounding: "half_up",
};
const base = {
  direction: "purchase", rounding: "half_up", settlementControlAccountId: "payable",
  expenseOrRevenueAccountId: "expense", taxAccountId: "vat", bankAccountId: "bank",
  cashEvidenceId: "cash1", knownCashEvidenceIds: [],
};
const payment = (line, paid, extra = {}) => m.applyCashPayment({ ...base, lines: [line],
  allocations: [{ sourceLineId: "line_1", paidGrossMinor: paid }], ...extra });
const year = (lines, extra = {}) => m.prepareYearEnd({ ...base, fiscalYearId: "year_1",
  accountingCutoff: "2026-12-31", complete: true, invoiceCount: 1, expectedInvoiceCount: 1,
  lines, ...extra });
const credit = (line, gross, recognized = "0", extra = {}) => m.applyCashCredit({
  direction: "purchase", line, creditGrossMinor: gross, recognizedPortionMinor: recognized,
  paidPrincipal: false, ...extra });
function value(result) {
  if (result._tag === "Failure") throw new Error(result.failure.code);
  return result.success;
}
function failure(result) { return result._tag === "Failure" ? result.failure.code : "Success"; }
function balanced(journal) {
  assert.equal(journal.reduce((sum, row) => sum + BigInt(row.debitMinor) - BigInt(row.creditMinor), 0n), 0n);
}
function paymentAfter(line, result) {
  const plan = value(result), slice = plan.slices[0];
  balanced(plan.journal);
  return slice.lineAfter ?? { ...line, recognizedGrossMinor: slice.recognizedGrossAfterMinor,
    paidGrossMinor: String(BigInt(line.paidGrossMinor) + BigInt(plan.cashPrincipalMinor)),
    releasedDeductibleMinor: String(BigInt(line.releasedDeductibleMinor) + plan.journal
      .filter(row => row.accountId === "vat").reduce((sum, row) => sum + BigInt(row.debitMinor), 0n)) };
}
function yearAfter(line, result) {
  const plan = value(result); balanced(plan.journal);
  return plan.slices[0]?.lineAfter ?? { ...line,
    recognizedGrossMinor: String(BigInt(line.recognizedGrossMinor) + BigInt(plan.recognizedMinor)),
    releasedDeductibleMinor: String(BigInt(line.releasedDeductibleMinor) + plan.journal
      .filter(row => row.accountId === "vat").reduce((sum, row) => sum + BigInt(row.debitMinor), 0n)) };
}
function paymentAmounts(result) {
  const plan = value(result); balanced(plan.journal);
  const s = plan.slices[0];
  return [s.settledRecognizedMinor, s.newNetMinor, s.newTaxMinor, s.recognizedGrossAfterMinor];
}
function yearAmounts(result) {
  const plan = value(result); balanced(plan.journal);
  return [plan.recognizedMinor, plan.slices[0]?.newNetMinor ?? "0", plan.slices[0]?.newTaxMinor ?? "0"];
}
let failures = 0, checks = 0;
function check(name, read, expected) {
  checks++;
  let actual;
  try { actual = read(); } catch (error) { actual = { error: error.message }; }
  try { assert.deepEqual(actual, expected); console.log("PASS", name, JSON.stringify(actual)); }
  catch { failures++; console.log("FAIL", name, JSON.stringify({ actual, expected })); }
}
const first = payment(original, "50000");
const afterFirst = paymentAfter(original, first);
const second = payment(afterFirst, "50000", { cashEvidenceId: "cash2", knownCashEvidenceIds: ["cash1"] });
const afterSecond = paymentAfter(afterFirst, second);
check("first-50000", () => paymentAmounts(first), ["0", "40000", "10000", "50000"]);
check("successive-50000", () => paymentAmounts(second), ["0", "40000", "10000", "100000"]);
check("year-end-25000", () => yearAmounts(year([afterSecond])), ["25000", "20000", "5000"]);
const atYearEnd = yearAfter(afterSecond, year([afterSecond]));
const settlement = payment(atYearEnd, "25000", { cashEvidenceId: "cash3" });
check("line-settlement-no-second-VAT", () => paymentAmounts(settlement), ["25000", "0", "0", "125000"]);
check("line-overpayment-refused", () => failure(payment(paymentAfter(atYearEnd, settlement), "1")), "UnrecognizedCoverageExceeded");
const small = { ...original, netMinor: "100", taxMinor: "12", originalDeductibleMinor: "12" };
check("14-of-112-at-12pct", () => paymentAmounts(payment(small, "14")), ["0", "12", "2", "14"]);
check("remaining-98-of-112", () => {
  const next = paymentAfter(small, payment(small, "14"));
  return paymentAmounts(payment(next, "98", { cashEvidenceId: "cash2" }));
}, ["0", "88", "10", "112"]);
const firstCredit = value(credit(original, "75000"));
const afterCredit = firstCredit.lineAfter ?? original;
check("credit-state", () => [afterCredit.netMinor, afterCredit.taxMinor,
  afterCredit.creditedGrossMinor, afterCredit.recognizedGrossMinor], ["100000", "25000", "75000", "0"]);
check("credit-reduces-year-end", () => yearAmounts(year([afterCredit])), ["50000", "40000", "10000"]);
check("second-credit-over-capacity", () => failure(credit(afterCredit, "75000")), "InsufficientLineCapacity");
check("credited-line-pay-remaining", () => paymentAmounts(payment(afterCredit, "50000")), ["0", "40000", "10000", "50000"]);
check("paid-and-credited-overpayment", () => failure(payment(paymentAfter(afterCredit, payment(afterCredit, "50000")), "1")), "UnrecognizedCoverageExceeded");
check("fully-credited-year-end", () => yearAmounts(year([value(credit(original, "125000")).lineAfter ?? original])), ["0", "0", "0"]);
const recognized = yearAfter(original, year([original]));
check("recognized-credit-components", () => {
  const c = value(credit(recognized, "75000", "75000"));
  return [c.recognizedCorrectionMinor, c.correctionNetMinor, c.correctionTaxMinor,
    c.correctionDeductibleMinor, c.lineAfter?.recognizedGrossMinor, c.lineAfter?.releasedDeductibleMinor];
}, ["75000", "60000", "15000", "15000", "50000", "10000"]);
check("recognized-credit-then-settlement", () => {
  const c = value(credit(recognized, "75000", "75000"));
  return paymentAmounts(payment(c.lineAfter ?? recognized, "50000"));
}, ["50000", "0", "0", "50000"]);
check("bad-credit-coverage-partition", () => failure(credit(recognized, "75000", "0")), "InsufficientLineCapacity");
check("underreleased-history", () => failure(year([{ ...afterFirst, releasedDeductibleMinor: "9000" }])), "StaleCoverage");
check("overreleased-history", () => failure(year([{ ...afterFirst, releasedDeductibleMinor: "11000" }])), "StaleCoverage");
check("duplicate-year-end-line", () => failure(year([original, original])), "DuplicateSourceUse");
check("duplicate-payment-line", () => failure(payment(original, "1", { lines: [original, original] })), "DuplicateSourceUse");
check("consumed-history-version-guard", () => failure(m.assertCoverageVersion(recognized, { ...recognized, paidGrossMinor: "1" })), "StaleCoverage");
check("changed-release-version-guard", () => failure(m.assertCoverageVersion(afterFirst, { ...afterFirst, releasedDeductibleMinor: "9000" })), "StaleCoverage");
const position = { recognitionSliceId: "slice_1", initialGrossMinor: "75000", settledGrossMinor: "0", creditedGrossMinor: "0" };
const positionSettlement = m.settleRecognizedPosition(position, "75000", "bank", "payable", "purchase");
check("position-full-settlement", () => {
  const s = value(positionSettlement); balanced(s.journal);
  return [s.settledMinor, s.taxDeltaMinor, s.journal.map(row => row.accountId)];
}, ["75000", "0", ["payable", "bank"]]);
check("position-overpayment", () => failure(m.settleRecognizedPosition(
  value(positionSettlement).positionAfter ?? { ...position, settledGrossMinor: "75000" }, "1", "bank", "payable", "purchase")), "UnrecognizedCoverageExceeded");
check("position-credit-capacity", () => failure(m.settleRecognizedPosition(
  { ...position, creditedGrossMinor: "75000" }, "1", "bank", "payable", "purchase")), "UnrecognizedCoverageExceeded");
check("paid-credit-profile-refusal", () => failure(credit(afterFirst, "1", "1", { paidPrincipal: true })), "UnsupportedProfile");
check("sale-successive-payments", () => {
  const sale = { ...original, originalDeductibleMinor: "0" };
  const one = payment(sale, "50000", { direction: "sale" });
  const two = payment(paymentAfter(sale, one), "50000", { direction: "sale", cashEvidenceId: "cash2" });
  return [paymentAmounts(two), value(two).journal.map(row => [row.accountId, row.debitMinor, row.creditMinor])];
}, [["0", "40000", "10000", "100000"], [["bank", "50000", "0"], ["expense", "0", "40000"], ["vat", "0", "10000"]]]);
check("partial-deduction-tax-first", () => {
  const l = { ...original, netMinor: "8", taxMinor: "2", originalDeductibleMinor: "1" };
  const one = payment(l, "3");
  const next = paymentAfter(l, one);
  const two = payment(next, "2", { cashEvidenceId: "cash2" });
  return [next.releasedDeductibleMinor, paymentAmounts(two), paymentAfter(next, two).releasedDeductibleMinor];
}, ["1", ["0", "2", "0", "5"], "1"]);
check("unknown-component-policy", () => failure(payment({ ...original, componentPolicy: "unknown" }, "50000")), "UnsupportedProfile");
check("exact-rounding-refusal", () => failure(payment({ ...small, rounding: "exact" }, "14", { rounding: "exact" })), "InsufficientLineCapacity");
console.log(JSON.stringify({ mode: baseline ? "baseline-2179637" : "working-leaf", checks, failures }));
process.exitCode = failures ? 1 : 0;
```

### Before-source observation

The command above with `NEXT38_BASELINE=1` ran before editing the leaf and exited
1: `{"mode":"baseline-2179637","checks":30,"failures":22}`. Exact observed
failures (expected values are fixed in the command):

| Probe | Baseline actual |
| --- | --- |
| successive-50000 | `["50000","0","0","50000"]` |
| year-end-25000 | `["75000","60000","15000"]` |
| line-overpayment-refused | `Success` |
| 14-of-112-at-12pct | `UnbalancedJournal` |
| remaining-98-of-112 | `UnbalancedJournal` |
| credit-state | `["100000","25000","0","0"]` |
| credit-reduces-year-end | `["125000","100000","25000"]` |
| second-credit-over-capacity | `Success` |
| paid-and-credited-overpayment | `Success` |
| fully-credited-year-end | `["125000","100000","25000"]` |
| recognized-credit-components | `["75000",undefined,undefined,undefined,undefined,undefined]` |
| recognized-credit-then-settlement | `["50000","0","0","125000"]` |
| underreleased-history | `Success` |
| overreleased-history | `InsufficientLineCapacity` |
| duplicate-year-end-line | `Success` |
| duplicate-payment-line | `Success` |
| consumed-history-version-guard | `Success` |
| changed-release-version-guard | `Success` |
| position-credit-capacity | `Success` |
| sale-successive-payments | `[["50000","0","0","50000"],[["bank","50000","0"],["AP","0","50000"]]]` |
| partial-deduction-tax-first | `["0",["2","0","0","3"],"0"]` |
| unknown-component-policy | `Success` |

The other eight probes passed their exact expected values: first payment,
line-settlement zero new VAT, payment of the remaining amount in isolation,
bad credit partition refusal, full position settlement, consumed position refusal,
paid-credit profile refusal and exact-rounding refusal. These isolated passes do
not cure the failed histories above. New-policy/shape probes intentionally fail
against the old contract; they are not additional claims of old runtime defects.

The first after-source run stopped before assertions with `StaleCoverage`: the
original probes used display IDs `L`/`Y1`, which do not satisfy the existing
`Identifier` schema now enforced on line/position state. The fixture identities
were corrected to `line_1`/`slice_1` and schema-valid account/year names, without
changing amounts, scenarios or expected financial outcomes. Baseline output above
retains its original display account names. This was a probe-fixture correction,
not a relaxation of state validation.

## After-source observations

The corrected-identity baseline was rerun in memory against `2179637` and again
exited 1 with 30 checks / 22 failures. Only display account names changed in its
output. The final working-leaf run on Bun 1.4.0 (macOS arm64) exited 0. Exact output:

```text
PASS first-50000 ["0","40000","10000","50000"]
PASS successive-50000 ["0","40000","10000","100000"]
PASS year-end-25000 ["25000","20000","5000"]
PASS line-settlement-no-second-VAT ["25000","0","0","125000"]
PASS line-overpayment-refused "UnrecognizedCoverageExceeded"
PASS 14-of-112-at-12pct ["0","12","2","14"]
PASS remaining-98-of-112 ["0","88","10","112"]
PASS credit-state ["100000","25000","75000","0"]
PASS credit-reduces-year-end ["50000","40000","10000"]
PASS second-credit-over-capacity "InsufficientLineCapacity"
PASS credited-line-pay-remaining ["0","40000","10000","50000"]
PASS paid-and-credited-overpayment "UnrecognizedCoverageExceeded"
PASS fully-credited-year-end ["0","0","0"]
PASS recognized-credit-components ["75000","60000","15000","15000","50000","10000"]
PASS recognized-credit-then-settlement ["50000","0","0","50000"]
PASS bad-credit-coverage-partition "InsufficientLineCapacity"
PASS underreleased-history "StaleCoverage"
PASS overreleased-history "StaleCoverage"
PASS duplicate-year-end-line "DuplicateSourceUse"
PASS duplicate-payment-line "DuplicateSourceUse"
PASS consumed-history-version-guard "StaleCoverage"
PASS changed-release-version-guard "StaleCoverage"
PASS position-full-settlement ["75000","0",["payable","bank"]]
PASS position-overpayment "UnrecognizedCoverageExceeded"
PASS position-credit-capacity "UnrecognizedCoverageExceeded"
PASS paid-credit-profile-refusal "UnsupportedProfile"
PASS sale-successive-payments [["0","40000","10000","100000"],[["bank","50000","0"],["expense","0","40000"],["vat","0","10000"]]]
PASS partial-deduction-tax-first ["1",["0","2","0","5"],"1"]
PASS unknown-component-policy "UnsupportedProfile"
PASS exact-rounding-refusal "InsufficientLineCapacity"
{"mode":"working-leaf","checks":30,"failures":0}
```

`git diff --check -- packages/domain/src/cash-method.ts docs/plans/evidence/next-38-leaf-review.md`
also exited 0. The source content's Git blob hash (without writing an object) is
`14e6b444731769dd98d0f3a9174afc926548a6ef`, obtained with
`git hash-object packages/domain/src/cash-method.ts`.

These observations exercise the exported domain operations and journal balances.
The commands write no financial data or test files. Shared format/lint/type gates
were not run under the explicit worktree-check ownership restriction. Bun loading
proves execution/transpilation here, not TypeScript or lint acceptance.

## Leaf-only integration handoff

- `CashMethodLine` now requires `paidGrossMinor`, `creditedGrossMinor`,
  `componentPolicy` and per-line `rounding`. Payment/year-end no longer choose
  rounding at operation level. Original totals and the selected policy must be
  pinned by the future caller, not relabeled for an existing incompatible history.
- Payment and year-end slices return `newDeductibleMinor` and `lineAfter`;
  payment retains `recognizedGrossAfterMinor`. Credit returns `lineAfter` and
  positive reversal magnitudes `correctionNetMinor`, `correctionTaxMinor` and
  `correctionDeductibleMinor`. Their use still needs the owned credit-date and
  tax-fact correction path; the leaf creates no credit journal or tax fact.
- The `recognizedPortionMinor` credit assertion must match suffix allocation.
  Fully unrecognized credits only revise commercial capacity; recognized credits
  reduce both effective recognition and the exact associated components. Paid
  history stays intact. Paid refunds and arbitrary interior coverage remain
  unsupported rather than being reinterpreted through changed originals.
- `RecognizedPosition` now includes effective `creditedGrossMinor`, and settlement
  returns `positionAfter`. This position compiler and `applyCashPayment` are
  **alternative journal paths for the same payment**, never two postings. A future
  caller must update position history and the corresponding line's paid coverage
  together, consume each recognized slice once, and use one bank/clearing effect.
- Returned versions are preparation witnesses, not generated persisted revisions.
  The application must lock/reload authoritative state, check the full sealed
  basis, assign fresh revisions and persist line/position/source/tax/journal
  changes atomically. Pure calls cannot distinguish a faithfully reloaded state
  from a stale copy supplied again by a caller.
- Complete year-end membership, eligible profiles, payment evidence identity,
  real credit relationships, cash-posting adoption, tax periods, amendments and
  concurrency/replay proof remain with commerce/register and VAT owners. Counts
  and `complete=true` are assertions supplied by those owners, not a population
  proof performed by this leaf.

No application consumer, shared export, migration or other owner's module was
changed. The implementing worker performed no commit or staging. NEXT-38 remains an unintegrated leaf;
the observed result is the bounded repaired state/calculation contract above.

## Isolated static-gate receipt — 2026-09-28

The coordinator subsequently assigned static verification in:

```text
/var/folders/50/zdx6l4px2wg7wh8q7_78g2qr0000gn/T/opencode/overnight-integration
HEAD: 844f68085c0c2c99274eaae3daed024fb0994dcc
```

Inspected that worktree's `AGENTS.md`, `package.json` and
`scripts/check-changed.ts` before running checks. Its runner executes formatting,
lint and incremental TypeScript sequentially, uses two native workers, enforces
a 60-second deadline per tool and cleans process groups and temporary configs.
Only `packages/domain/src/cash-method.ts` was replicated there with `apply_patch`.
The runner selected it and the user's existing uncommitted `customer-credits.ts`.

| Command, in the isolated worktree | Observed result |
| --- | --- |
| First `bun run check:changed` | Exit 1: cash-method had two five-binding destructures and 20 readable-spacing lint errors. TypeScript passed. |
| `bun run check:changed`, after owned lint fixes | Exit 0: formatter 0.08s; normal lint 0.30s; domain TypeScript 0.29s. |
| `bun run check:changed:full`, run after fast passed | Exit 0: formatter 0.05s; type-aware lint 0.56s; domain TypeScript 0.28s. |

No timeouts, overlapping check runs, extended deadlines or abandoned-process
cleanup were needed. Fixes were limited to cash-method: use direct property access
for the fifth destructured value, add required blank lines, and retain the
runner's formatting. The selected financial/state model did not change.

Those exact changes were applied back to
`/Users/admin/openERP/packages/domain/src/cash-method.ts`. The recorded domain
probe command was rerun there and exited 0 with the same exact PASS outcomes
printed above:

```json
{"mode":"working-leaf","checks":30,"failures":0}
```

The final equality command exited 0 and printed no diff:

```sh
git diff --no-index /Users/admin/openERP/packages/domain/src/cash-method.ts /var/folders/50/zdx6l4px2wg7wh8q7_78g2qr0000gn/T/opencode/overnight-integration/packages/domain/src/cash-method.ts
```

Both final cash-method files have Git blob hash
`4af18fe441ad0982a9672a382b0add6f9d727a1e` (superseding the pre-static fingerprint
above). The isolated `customer-credits.ts` hash was
`2e8c5d4b20f70cd3e68cde3feec364f8efc0811b` both before and after all gate runs;
the file was byte-identical, not merely semantically preserved.

This closes the leaf's static-verification gap. No shared-main check command,
commit, staging, package/schema/export edit or application integration occurred.
The commerce/register and VAT handoffs listed above remain open.
