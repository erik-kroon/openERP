# NEXT-39 processor-clearing leaf repair

Baseline: `cbf4db9`, with `processor-clearing.ts` unchanged from the reviewed
`55cf929` blob `728e736ca196d7ecc82c916f5727bfc52307fa1b`. Scope is this evidence
file and `packages/domain/src/processor-clearing.ts`. No application consumer
exists. This is domain verification, not a provider or persistence journey.

## Failure contract recorded before source changes

1. Ordinary negative provider refund/payout amounts must pass the public input
   schema. Signed opening/effect/closing amounts must remain representable.
2. Every supported observation must conserve its signed processor movement:
   `processor debits - credits = net`. A recoverable hold recognizes principal
   separately from fees; a release cannot exceed the linked receivable.
3. Identity must distinguish account, mode, currency and actual occurrence.
   Payout movements and resolutions must retain the provider payout relationship.
   Equal amounts must not collapse separate bank or failure occurrences.
4. Fee-bearing payouts must refuse until an explicit supported profile exists.
5. Zero components are omitted. Journal sides are nonnegative, bounded minor
   units; each emitted line has exactly one positive side. Negative and zero
   failed-payout reversals refuse.
6. Replay must verify the returned effect's identity, not merely two supplied
   strings. Changed-source content and durable uniqueness remain caller duties.
7. Every schema-accepted source ID must produce a schema-valid effect; escaped
   and maximum-length IDs must not overflow an arbitrary concatenation limit.
8. Refund capacity consumption is principal only. NEXT-39 already releases the
   customer liability; a caller must not also post NEXT-30's refund journal.
9. Transit totals are signed diagnostics, including over-resolution. Summation
   does not prove complete, unique, partitioned, independently reconciled data.

## Repeatable public-schema/compiler probe

Run the following from the repository root, before and after the repair. It
records all cases rather than stopping at the first failure. `EXPECT_REPAIRED=1`
makes any failed expectation exit nonzero. New reviewed-input fields are supplied
from the outset; the old schemas ignore them. No test file is created.

```bash
EXPECT_REPAIRED=1 bun -e '
import * as S from "effect/Schema";
import * as R from "effect/Result";
import * as P from "./packages/domain/src/processor-clearing.ts";
const accounts={processorControlAccountId:"processor",feeCostAccountId:"fee",receivableAccountId:"receivable",customerCreditLiabilityAccountId:"liability",payoutTransitAccountId:"transit",disputeReceivableAccountId:"dispute"};
const payout={accountId:"acct",liveMode:true,currency:"SEK",providerPayoutId:"po_one"};
const base={observation:{accountId:"acct",liveMode:true,balanceTransactionId:"txn",rawSourceRef:"raw",eventType:"charge",currency:"SEK",currencySupported:true,grossMinor:"125000",feeMinor:"3000",netMinor:"122000",availableOn:"2026-09-28",providerPayoutId:null},accounts,accountLiveMode:true,recognizedSaleRelationship:true,remainingRefundCapacityMinor:"125000",dispute:null};
let passed=0,failed=0;
function check(name,ok,actual){if(ok)passed++;else failed++;console.log(JSON.stringify({name,pass:ok,actual}));}
function summarize(r){return R.isFailure(r)?r.failure.code:{identity:r.success.sourceIdentity,consumed:r.success.consumedRefundCapacityMinor,lines:r.success.journal.map(l=>[l.accountId,l.debitMinor,l.creditMinor])};}
function compile(name,o,extra,expected){const i={...base,...extra,observation:{...base.observation,...o}};const r=P.compileProcessorEffect(i);const valid=S.is(P.CompileEffectInput)(i);const ok=typeof expected==="string"?R.isFailure(r)&&r.failure.code===expected:R.isSuccess(r)&&S.is(P.ProcessorEffect)(r.success)&&JSON.stringify(r.success.journal.map(l=>[l.accountId,l.debitMinor,l.creditMinor]))===JSON.stringify(expected);check(name,valid&&ok,{inputSchema:valid,result:summarize(r)});return r;}
const charge=compile("charge",{},{},[["processor","122000","0"],["fee","3000","0"],["receivable","0","125000"]]);
const refund=compile("refund",{eventType:"refund",grossMinor:"-125000",netMinor:"-128000"},{},[["liability","125000","0"],["fee","3000","0"],["processor","0","128000"]]);
check("refund_principal_only",R.isSuccess(refund)&&refund.success.consumedRefundCapacityMinor==="125000",summarize(refund));
compile("refund_capacity",{eventType:"refund",grossMinor:"-125001",feeMinor:"0",netMinor:"-125001"},{},"RefundCapacityExceeded");
compile("payout",{eventType:"payout",providerPayoutId:"po_one",grossMinor:"-122000",feeMinor:"0",netMinor:"-122000"},{},[["transit","122000","0"],["processor","0","122000"]]);
compile("payout_fee_refusal",{eventType:"payout",providerPayoutId:"po_one",grossMinor:"-122000",feeMinor:"3000",netMinor:"-125000"},{},"UnsupportedObservationType");
compile("payout_link_required",{eventType:"payout",grossMinor:"-100",feeMinor:"0",netMinor:"-100"},{},"UnsupportedObservationType");
compile("zero_net_charge",{grossMinor:"3000",feeMinor:"3000",netMinor:"0"},{},[["fee","3000","0"],["receivable","0","3000"]]);
compile("negative_net_charge_refusal",{grossMinor:"100",feeMinor:"150",netMinor:"-50"},{},"UnsupportedObservationType");
compile("hold",{eventType:"dispute_hold",grossMinor:"-100",feeMinor:"10",netMinor:"-110"},{dispute:{disputeId:"dp_one",remainingReceivableMinor:"0"}},[["dispute","100","0"],["fee","10","0"],["processor","0","110"]]);
compile("hold_wrong_sign",{eventType:"dispute_hold",grossMinor:"110",feeMinor:"10",netMinor:"100"},{dispute:{disputeId:"dp_one",remainingReceivableMinor:"0"}},"UnsupportedObservationType");
compile("hold_existing_principal",{eventType:"dispute_hold",grossMinor:"-100",feeMinor:"0",netMinor:"-100"},{dispute:{disputeId:"dp_one",remainingReceivableMinor:"100"}},"UnsupportedObservationType");
compile("won",{eventType:"dispute_won",grossMinor:"100",feeMinor:"0",netMinor:"100"},{dispute:{disputeId:"dp_one",remainingReceivableMinor:"100"}},[["processor","100","0"],["dispute","0","100"]]);
compile("won_capacity",{eventType:"dispute_won",grossMinor:"101",feeMinor:"0",netMinor:"101"},{dispute:{disputeId:"dp_one",remainingReceivableMinor:"100"}},"DisputeCapacityExceeded");
compile("won_fee_refusal",{eventType:"dispute_won",grossMinor:"100",feeMinor:"10",netMinor:"90"},{dispute:{disputeId:"dp_one",remainingReceivableMinor:"100"}},"UnsupportedObservationType");
compile("dispute_link_required",{eventType:"dispute_won",grossMinor:"100",feeMinor:"0",netMinor:"100"},{},"UnsupportedObservationType");
compile("arithmetic_guard",{netMinor:"1"},{},"ArithmeticMismatch");
compile("sale_guard",{},{recognizedSaleRelationship:false},"MissingSaleRelationship");
compile("currency_guard",{currencySupported:false},{},"UnsupportedCurrency");
compile("mode_guard",{liveMode:false},{},"TestModeMismatch");
const identity=(o,extra={})=>P.compileProcessorEffect({...base,...extra,observation:{...base.observation,...o}});
const keys=[identity({}),identity({currency:"USD"}),identity({liveMode:false},{accountLiveMode:false}),identity({accountId:"acct_two"}),identity({balanceTransactionId:"txn_two"})];
check("partition_identities",keys.every(R.isSuccess)&&new Set(keys.map(r=>R.isSuccess(r)?r.success.sourceIdentity:null)).size===5,keys.map(summarize));
for(const id of ["t".repeat(256),"\u0000".repeat(256),"\"|\\".repeat(85)]){const i={...base,observation:{...base.observation,balanceTransactionId:id}};const r=P.compileProcessorEffect(i);check("accepted_id_output",S.is(P.CompileEffectInput)(i)&&R.isSuccess(r)&&S.is(P.ProcessorEffect)(r.success),{length:id.length,outputValid:R.isSuccess(r)&&S.is(P.ProcessorEffect)(r.success)});}
const bank={payout,payoutAmountMinor:"100",transitCapacityMinor:"100",currencyMatches:true,providerBankRelationship:true,adoptsExistingPosting:false,adoptedPostingRef:null,bankObservationId:"bank_one",bankAccountId:"bank",payoutTransitAccountId:"transit"};
const banks=[P.recordBankPayoutReceipt(bank),P.recordBankPayoutReceipt({...bank,bankObservationId:"bank_two"}),P.recordBankPayoutReceipt({...bank,payout:{...payout,providerPayoutId:"po_two"}})];
check("bank_occurrence_and_payout",banks.every(r=>R.isSuccess(r)&&S.is(P.ProcessorEffect)(r.success))&&new Set(banks.map(r=>R.isSuccess(r)?r.success.sourceIdentity:null)).size===3,banks.map(summarize));
const adopted=P.recordBankPayoutReceipt({...bank,adoptsExistingPosting:true,adoptedPostingRef:"posting_one"});
check("bank_adoption",R.isSuccess(adopted)&&adopted.success.journal.length===0&&R.isSuccess(banks[0])&&adopted.success.sourceIdentity===banks[0].success.sourceIdentity,summarize(adopted));
const failure={payout,payoutAmountMinor:"100",transitCapacityMinor:"100",cashSettled:false,nonSettlementEvidenceRef:"evidence_one",failureBalanceTransactionId:"failure_one",transitAccountId:"transit",processorControlAccountId:"processor"};
const f=P.reverseFailedPayout(failure),f2=P.reverseFailedPayout({...failure,failureBalanceTransactionId:"failure_two"});
check("failed_payout_occurrence",S.is(P.PayoutFailureInput)(failure)&&R.isSuccess(f)&&R.isSuccess(f2)&&S.is(P.ProcessorEffect)(f.success)&&f.success.sourceIdentity!==f2.success.sourceIdentity,{a:summarize(f),b:summarize(f2)});
for(const [name,r,code] of [["bank_capacity",P.recordBankPayoutReceipt({...bank,payoutAmountMinor:"101"}),"TransitCapacityExceeded"],["failure_capacity",P.reverseFailedPayout({...failure,payoutAmountMinor:"101"}),"TransitCapacityExceeded"],["settled_failure",P.reverseFailedPayout({...failure,cashSettled:true}),"PayoutFailureUnproven"],["negative_failure_direct",P.reverseFailedPayout({...failure,payoutAmountMinor:"-100"}),"NonPositivePayout"],["zero_failure",P.reverseFailedPayout({...failure,payoutAmountMinor:"0"}),"NonPositivePayout"]])check(name,R.isFailure(r)&&r.failure.code===code,summarize(r));
if(R.isSuccess(charge)){const own=charge.success.sourceIdentity;const wrong=P.replaySameSourceEffect({existingSourceIdentity:"unrelated",sourceIdentity:"unrelated",existingEffect:charge.success});const same=P.replaySameSourceEffect({existingSourceIdentity:own,sourceIdentity:own,existingEffect:charge.success});check("replay_wrong_effect",R.isFailure(wrong),summarize(wrong));check("replay_same_effect",R.isSuccess(same)&&same.success===charge.success,summarize(same));}
const ci={reviewedOpeningMinor:"0",netEffectsMinor:["122000","-122000"]};const c=P.processorClosing(ci);check("signed_closing",S.is(P.ClosingInput)(ci)&&R.isSuccess(c)&&c.success==="0",c);
const ti={payoutsMovedOutMinor:"100",bankReceiptsMinor:"100",supportedFailuresMinor:"100"};const t=P.payoutTransitClosing(ti);check("negative_transit_diagnostic",S.is(P.TransitClosingInput)(ti)&&R.isSuccess(t)&&t.success==="-100",t);
const max="9".repeat(38);const overflow=P.compileProcessorEffect({...base,observation:{...base.observation,eventType:"refund",grossMinor:`-${max}`,feeMinor:"1",netMinor:`-${BigInt(max)+1n}`},remainingRefundCapacityMinor:max});check("journal_bound_direct",R.isFailure(overflow)&&overflow.failure.code==="ArithmeticMismatch",summarize(overflow));
const signedOverflow={...base,observation:{...base.observation,grossMinor:"1".repeat(39)}};check("provider_bound",!S.is(P.CompileEffectInput)(signedOverflow),{inputSchema:S.is(P.CompileEffectInput)(signedOverflow)});
const bigClosing=P.processorClosing({reviewedOpeningMinor:max,netEffectsMinor:[max]});check("aggregate_closing",R.isSuccess(bigClosing)&&bigClosing.success==="199999999999999999999999999999999999998",bigClosing);
compile("fee_only",{eventType:"fee_only",grossMinor:"-100",feeMinor:"0",netMinor:"-100"},{},[["fee","100","0"],["processor","0","100"]]);
compile("unclassified_dispute_loss",{eventType:"dispute_lost",grossMinor:"0",feeMinor:"0",netMinor:"0"},{},[]);
const repeated=identity({rawSourceRef:"raw_two"});check("same_event_other_fetch",R.isSuccess(charge)&&R.isSuccess(repeated)&&charge.success.sourceIdentity===repeated.success.sourceIdentity,summarize(repeated));
console.log(JSON.stringify({passed,failed}));if(process.env.EXPECT_REPAIRED==="1"&&failed)process.exitCode=1;
'
```

## Results

The first pre-repair execution observed 10 passing and 26 failing expectations
(exit 1). The final probe above added monetary-boundary and source-fetch controls
before production edits and observed **14 passing, 28 failing, exit 1**. The
identical final probe after repair observed **42 passing, 0 failing, exit 0**.
The initial failing run is a diagnosis, not a passing verification claim.
Verified repaired source blob: `aafade57cb337dbb974642b90bf9c21e2bd93099`.

Executed artifact command (runs the first fenced shell block in memory):

```sh
bun -e 'const artifact = await Bun.file("docs/plans/evidence/next-39-leaf-review.md").text(); const command = artifact.match(/```bash\n([\s\S]*?)\n```/)?.[1]; if (!command) throw new Error("Missing NEXT-39 probe"); const result = Bun.spawnSync(["bash", "-c", command], {stdout:"inherit", stderr:"inherit"}); process.exit(result.exitCode);'
```

Amounts in the following table are exact minor units. `D` and `C` identify the
paired debit and credit fields, not signed values in journal output.

| Vector | Before repair | After repair |
| --- | --- | --- |
| Charge `125000 / 3000 / 122000` | Valid, correct journal | Processor D122000, fee D3000, AR C125000; no sale/tax fact |
| Refund `-125000 / 3000 / -128000` | Schema rejects; direct math succeeds | Schema accepts; liability D125000, fee D3000, processor C128000; consumed principal 125000 |
| Refund `125001` against `125000` capacity | Schema rejects; direct call refuses excess | Schema accepts signed observation; `RefundCapacityExceeded` |
| Payout `-122000 / 0 / -122000` | Schema rejects; direct math succeeds | Schema accepts; transit D122000, processor C122000 |
| Payout with fee 3000 | Direct call puts 125000 into transit | `UnsupportedObservationType` |
| Payout missing originating payout ID | Succeeds | `UnsupportedObservationType` |
| Charge `3000 / 3000 / 0` | `ArithmeticMismatch` | Fee D3000, AR C3000; no zero processor line |
| Charge `100 / 150 / -50` | Direct call emits negative debit | `UnsupportedObservationType` |
| Hold `-100 / 10 / -110`, linked remaining principal 0 | Rejects | Dispute D100, fee D10, processor C110 |
| Hold with positive gross, or existing linked principal 100 | Wrong-sign hold succeeds; valid negative hold rejects for wrong reason | Both `UnsupportedObservationType` |
| Won dispute `100 / 0 / 100`, linked remaining principal 100 | Rejects | Processor D100, dispute C100 |
| Won dispute 101 against principal 100 | Wrong-sign refusal | `DisputeCapacityExceeded` |
| Won dispute with fee, or missing dispute link | Wrong-sign refusal | Both `UnsupportedObservationType` |
| Arithmetic, missing sale, unsupported currency and mode guards | Correct refusals | Same respective failure codes |
| Account/mode/currency/occurrence identity partition | Five observations produce only three identities | Five distinct identities |
| IDs: 256 plain characters, 256 NUL characters, 255 mixed quote/backslash/separator characters | Success with schema-invalid effects | All accepted inputs produce schema-valid effects |
| Two bank occurrences; same occurrence under another payout | All `bank\|100` | Three distinct identities |
| Adopt exact bank/transit posting | No journal, but different amount-only identity | No journal; same economic identity as posting this bank occurrence |
| Two failed payout balance transactions of 100 | Both `failed\|100` | Distinct balance-transaction identities |
| Bank receipt 101 against transit 100 | `TransitCapacityExceeded` | Same refusal |
| Failed payout 101 against transit 100 | Succeeds | `TransitCapacityExceeded` |
| Settled payout failure | `PayoutFailureUnproven` | Same refusal |
| Failed payout -100 (direct call), or zero | Negative sides succeed; zero fails as arithmetic | Both `NonPositivePayout` |
| Replay supplied identities agree but retained effect differs | Returns unrelated effect | `DuplicateSourceEffect` |
| Exact same-effect replay | Returns original effect | Same original effect |
| Processor closing `0 + 122000 - 122000` | Input schema rejects | Schema accepts; result `0` |
| Transit `100 - 100 - 100` | Returns `-100` under unsigned result declaration | Returns `-100` under signed diagnostic contract |
| Direct refund journal requiring a 39-digit side | Success with out-of-codec journal | `ArithmeticMismatch` |
| 39-digit provider gross | Schema rejects | Schema rejects |
| Two maximum 38-digit amounts summed | Arithmetic succeeds | Exact aggregate `199999999999999999999999999999999999998`, now under signed aggregate contract |
| Fee-only `-100 / 0 / -100` | Schema rejects | Schema accepts; fee D100, processor C100 |
| Unclassified dispute loss, zero observation | Empty unclassified effect | Same unclassified effect; not proof of reconciliation |
| Same event from another retained fetch | Same identity | Same identity; raw fetch reference remains outside occurrence identity |

### Static gates

- First `bun run check:changed`: failed the existing complexity limit (39 versus
  30) and readable-spacing rule; TypeScript passed. Dispute compilation was moved
  to a private local function and the spacing fixed; no rule was changed.
- Subsequent `bun run check:changed`: passed formatting, lint and incremental
  domain TypeScript checks.
- `bun run check:changed:full`: passed formatting, type-aware lint and incremental
  domain TypeScript checks. It selected only `processor-clearing.ts`.
- `git diff --check`: passed. No tool timed out. No provider, database, HTTP/MCP
  or application posting journey was run.

## Changed leaf contracts

No application consumers were found. These are explicit new inputs, not
compatibility defaults or a migration of retained financial effects.

- Provider gross/net reuse `SignedMinorUnits` with the existing 38-digit posting
  magnitude bound. Fees, capacities and journal sides retain `MinorUnits`.
  Closings use unbounded `SignedMinorUnits` for exact aggregate diagnostics.
- `ProcessorObservation.providerPayoutId` is required and nullable. It is
  non-null only for the originating payout transaction, mandatory for a supported
  payout, and never an automatic-payout membership tag on a charge/refund.
  Adapters normalize the same balance transaction identically across fetch APIs.
- `CompileEffectInput.dispute` is required and nullable. A recoverable hold needs
  `{disputeId, remainingReceivableMinor: "0"}` for a reviewed fresh receivable.
  Its principal is `-gross`; fee expense is separate; processor credit is `-net`.
  The supported release has positive gross, zero fee and principal at most the
  linked `remainingReceivableMinor`. Further holds, fee adjustments and loss/VAT
  decisions are outside this first profile. The caller retains this reviewed
  dispute link with the plan and atomically updates that receivable.
- Payouts are fee-free only. Negative-net charges are refused rather than
  inventing a provider profile. Zero journal components are omitted; a genuine
  zero effect does not authorize a zero voucher.
- `PayoutReference` contains account, mode, currency and provider payout ID.
  Bank receipts now require it and `bankObservationId`. `adoptedPostingRef`
  replaces `adoptsExistingPosting`: null posts the bank/transit journal; a
  qualified existing posting reference produces no journal. Both paths name the
  same bank occurrence, preventing a second identity from an adoption flag.
- Failed reversals now require `payout`, `failureBalanceTransactionId`,
  `nonSettlementEvidenceRef` and current `transitCapacityMinor`, in addition to
  the existing amount, accounts and `cashSettled` input. Positive amount,
  non-settlement and supplied transit capacity are checked locally. Evidence
  qualification and original-payout lookup remain application duties.
- `sourceIdentity` is the existing canonicalizer's JSON for version, source kind,
  account, mode, currency, actual occurrence ID and nullable originating payout
  ID. Balance transactions (including failure returns) share one source kind;
  retained bank observations use another. Amount, raw fetch reference and
  post/adopt choice are not identity. The shared 4096-character effect/replay
  bound covers the object plus a 128-character account and two 256-character
  provider IDs even at six escaped characters per code unit. Invalid Unicode
  refuses with `InvalidSourceIdentity`, rather than throwing or emitting an
  unusable identity.
- Replay checks the retained effect's own identity as well as both supplied
  identities. It does not compare source contents: the future caller must reject
  changed input under a retained occurrence using its immutable source/plan
  digest and source-key uniqueness.
- `payoutTransitClosing` intentionally preserves negative over-resolution as a
  signed diagnostic. Neither closing helper is a reconciliation certificate.

## Integration obligations and limits

The leaf remains unconsumed. Its booleans and references are reviewed inputs,
not proof of provider account access, fee qualification, same-book ownership or
non-settlement. A future application owner must:

1. Retain raw observations and pinned provider/currency profiles; resolve current
   authorized book/account/mode/currency scope. Preserve unsupported observations
   and their differences. NEXT-40 still owns non-book-currency integration.
2. Qualify the exact sale/refund liability/dispute/payout/bank relationships. Load
   authoritative capacities and serialize all competing consumers, corrections,
   bank receipts and failures through the shared financial transaction.
3. Enforce source-occurrence uniqueness independently of caller keys or changed
   linkage, compare retained source content, and commit the journal, customer or
   dispute/transit effect, authority use and once-only receipt atomically.
4. Consume NEXT-30's customer liability/refund capacity in that same transaction
   without posting its refund journal as a second liability debit. NEXT-39's
   refund consumes only `-gross`, not the fee. Existing NEXT-30 clearing-source
   and reversal fixes at `a4ca539` are unchanged.
5. Prove cash did not settle before reversing transit. Settled-then-returned cash
   retains both bank events. A reference or a `cashSettled: false` assertion alone
   does not qualify that evidence.
6. Establish complete, unique, currency/source-partitioned closing membership and
   compare with independent provider/bank evidence. A zero result or a completed
   pagination loop is not that proof.

Only the two authorized paths were edited. No dependencies, shared exports,
application persistence, test files, staging, commits or external operations were added.
The pre-existing `.hallmark/*` and `licenses/accounted-LICENSE` deletions remain
untouched. The repaired leaf is ready for integrator review and commit; packet
integration and runtime/provider acceptance remain open.
