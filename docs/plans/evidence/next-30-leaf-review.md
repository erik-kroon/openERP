# NEXT-30 customer-credit leaf review

The current leaf has no application consumers. Review scope is the pure
`packages/domain/src/customer-credits.ts` contract; financial persistence and
legal credit issuance remain with their existing owners.

## Failure contract recorded before repair

The public schema/compiler was executed through a bounded Bun command before
editing production source. Observed counterexamples:

1. An already-posted receipt of `125000`, with allocation `100000` and surplus
   `25000`, produced only credits to AR and customer liability. Journal balance
   was `-125000`. Expected: debit the evidenced receipt-clearing account `125000`,
   credit AR `100000`, credit liability `25000`; no second bank debit.
2. An already-posted refund payment of `10000` produced an empty journal.
   Expected: debit customer liability `10000`, credit the evidenced refund-clearing
   account `10000`; no second bank credit. Merely recording consumption does not
   settle the posted liability balance.
3. With prior `G125000 K50000 P100000 Q10000`, reversing payment to `P90000`
   succeeded because the posterior formula remained nonnegative. Expected:
   `UnsupportedConsumedHistory`; standalone reversal cannot reduce retained
   credit principal from `25000` to `15000` while its effects remain posted.

The selected bounded repair requires an explicit `clearingAccountId` on adopted
clearing sources, balances their reclassification journals, and makes standalone
reversal compare retained prior and posterior histories. It does not invent an
already-settled-liability adoption mode or infer accounts from source IDs.

## Observed repair and verification

The same source/amount cases were executed after repair. The reversal call now
passes both histories, as required by its changed unconsumed contract.

| Case | Observed after repair |
| --- | --- |
| Adopted receipt | Clearing debit `125000`, AR credit `100000`, liability credit `25000`; balance `0`, no bank line. |
| Adopted refund | Liability debit `10000`, clearing credit `10000`; balance `0`, no bank line. |
| Consumed-principal reversal | `UnsupportedConsumedHistory`. |

`bun run check:changed` and `bun run check:changed:full` passed in the isolated
`overnight-integration` worktree. `git diff --no-index` confirmed identical source
there and in main. The subsequent combined cash-method/customer-credit static
gate also passed. These are domain execution and static observations, not an
HTTP/payment/financial-posting journey.

## Repeatable public-domain probe

Run from `packages/domain`. The input amounts and source identities are the
before-repair cases; the two-history reversal call is the repaired contract.

```bash
bun -e '
import * as S from "effect/Schema";
import * as R from "effect/Result";
import * as C from "@open-erp/domain/customer-credits";
const source = {kind:"adopted_clearing", clearingRef:"clearing_one", clearingAccountId:"account_clearing", unusedCapacityMinor:"125000"};
const receipt = S.decodeUnknownSync(C.CustomerReceiptInput)({customerId:"customer_one", currency:"SEK", cashMinor:"125000", legs:[{invoiceId:"invoice_one", amountMinor:"100000", invoiceRemainingMinor:"100000"}], surplusClassification:"refundable_overpayment", source, receivableControlAccountId:"account_ar", creditLiabilityAccountId:"account_liability"});
const refund = S.decodeUnknownSync(C.CustomerRefundInput)({customerId:"customer_one", currency:"SEK", remainingCreditMinor:"25000", amountMinor:"10000", source:{...source, clearingRef:"clearing_two", unusedCapacityMinor:"10000"}, sourceCurrency:"SEK", creditLiabilityAccountId:"account_liability"});
for (const [name,result] of [["receipt",C.compileCustomerReceipt(receipt)],["refund",C.recordCustomerRefund(refund)]]) {
  console.log(name, R.isSuccess(result) ? JSON.stringify({journal:result.success.journal, balance:result.success.journal.reduce((n,l)=>n+BigInt(l.debitMinor)-BigInt(l.creditMinor),0n).toString()}) : result.failure.code);
}
const prior = {originalGrossMinor:"125000", creditedMinor:"50000", paidMinor:"100000", consumedMinor:"10000"};
const reversed = C.refuseConsumedHistoryReversal(prior,{...prior,paidMinor:"90000"});
console.log("consumed_reversal",R.isFailure(reversed)?reversed.failure.code:reversed.success);
'
```

Before repair, the source codec omitted `clearingAccountId` and the reversal
function accepted only the posterior position. The recorded old results above
come from those old interfaces. Original source belongs to `e94831a`.

Authoritative customer/currency matching, qualified clearing-line identity,
unused source capacity, legal credit issuance, approvals, idempotency and atomic
origin/application/refund persistence remain application-owner obligations.
