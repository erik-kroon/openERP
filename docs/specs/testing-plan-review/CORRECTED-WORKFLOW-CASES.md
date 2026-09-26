# Corrected workflow pseudologic

These revisions preserve the five families and the existing SO/CB/SA/HI/AB/XC identifiers. They supersede the conflicting expectations listed below, not the product's accepted financial contracts. New suffixes identify leaf variants; do not infer an executable case count from prose headings.

Source basis: `ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb`. These are proposed cases, not observed passing tests. Exact endpoint/error mappings and fixture graph builders must bind to the current shared contracts. See the review for source locations.

## 0. Common notation

```text
T = retained database date/instant for a runtime fixture
scope = accessible entity/book for this caller
observe() = exact scoped rows and actual counters from a fresh observer connection
financialFootprint = journal rows + counter rows + register/capacity effects
                     + approval use + successful receipts + required outbox intent
prepareFootprint = the separately declared nonfinancial records for this operation
alias(name) = captured generated identity, not a guessed ID
```

Every R-case has a valid independent neighbor, one isolated invalid predicate and a scoped before/after assertion. Do not build R2 by relying on R1 or H1 having run. Existing successful fixture postings are part of the baseline: `zero additional vouchers` is not the same as `zero vouchers in the database`.

## 1. SO: sales-order write path

### SO-H1 / create quote

Use valid `DraftContent` from the current schema with one declared synthetic line, customer and supported profile.

```text
before = observe(scope)
result = POST createSalesDocument(validQuote)
alias('quoteA') = result.id

assert result.kind == quote
assert result.state == draft
assert result.revision == "1"
assert result.scope == scope
assert result.sourceQuoteId == null
assert result.sourceQuoteRevision == null
assert receipt carries this command key, operation and caller
assert exactly one document head and one revision were added
assert declared exact draft amounts agree with the fixture
assert no financial counter, voucher, approval use or outbox change
assert stored/returned IDs and digest bindings agree
```

Do not expect `receipt.documentId`, a literal generated ID or unconditionally 201. The current `SalesDocument` schema returns `id` and a command receipt. Use the actual success mapping from `SalesOrdersApi`.

### SO-H2 / revise draft

Create the initial quote inside this case's fixture builder. Revise with its captured revision/digest. Expect revision `"2"`, changed declared fields and both immutable revision bodies. Do not require a `previousDigest` field that the current sales schema does not expose. Verify the original revision is unchanged through its retained row and document/revision identity.

### SO-H3 / accepted quote to order

Accept the fixture quote first. Convert its exact accepted revision to a new order and assert the source quote ID/revision, copied commercial facts and zero ledger delta. Repeat with the same key and recover the same order.

Keep once-only quote consumption as a business invariant to verify, not a statement that the inspected code demonstrably provides it. The visible `writeDocument` path creates a new order without changing the quote head. Inspect the actual persistent owner/constraint and run distinct-key sequential plus overlapping attempts. If the accepted product contract allows only one order and both land, report a product defect rather than rewriting the test to accept duplicates. Do not infer a specific conversion-table row from Accounted's implementation.

### SO-R2 / body-size boundary

Generate two otherwise schema-valid requests whose encoded input is exactly 65536 and 65537 bytes at the size boundary being tested. Do not use a 700-line array if the shared schema rejects the line count before that boundary. Check UTF-8 byte length independently, including a multibyte variant. If the public schema makes the application boundary unreachable, label it as a direct application admission case instead of claiming an HTTP guard test.

### SO-R4 / missing and stale

With all other fields current:

```text
wrong digest -> StaleDependency
correct digest + stale expected revision -> StaleDependency
absent child document under accessible scope -> NotFound
foreign child document substituted under accessible local scope -> same child-not-found contract
inaccessible top-level scope -> declared authorization error, not an invented universal 404
```

### SO-R5 / document bound

199 existing valid documents -> creation of document 200 succeeds.
200 existing valid documents -> next creation refuses and adds no document/revision/receipt.

The bound is a tested current profile limit, not an endorsement that 200 is adequate product capacity.

### SO-R6 / revision bound

A current draft at revision 49 can become revision 50. Another revision request at current revision 50 refuses. Do not decrement revision 50 to 49. Retain all previous revision bodies. Seed the bounded history only through a declared valid builder.

### SO-R9 / transition eligibility

Wrong kind or non-accepted quote, with the expected digest/revision otherwise current, returns `InvalidJournal` in the inspected source. Stale digest returns `StaleDependency` earlier and therefore cannot be used to prove this branch. Keep those cases separate.

### SO-X1/2/3 / concurrency and recovery

SO-X1: same key/input/current actor, observed overlap -> identical order/document result and one command result. Financial sequence change is exactly zero, not 'at most once'.

SO-X2: same key with different input -> conflict and original result unchanged.

SO-X3: distinct keys targeting the same accepted quote -> test the selected once-only conversion contract. Retain the actual allowed loser error from that owner; do not derive it solely from Accounted. Run a sequential duplicate before the race so a deterministic missing uniqueness rule is not mislabeled a timing bug.

## 2. CB: supplier credit basis and execution

### Fixture families must be internally valid

```text
ZERO:
  accepted profile = synthetic-manual-supplier-v1
  one supported zero-tax expense12500 / AP12500
  review tax0, unpaid12500

GROSS_COST:
  accepted profile = synthetic-gross-cost-supplier-v1
  original source net10000 + tax2500 = gross12500
  expense12500 / AP12500 under this profile
  asserted source tax retained separately

PURCHASE:
  accepted profile = swedish-purchase-v1 in the supported synthetic scope
  expense8000 + inputVAT2000 / AP10000
  original line identity and tax capacity retained
```

These are mechanical fixtures under the named current profiles. They are not an assertion of a company's real tax eligibility. A zero-tax happy fixture should not carry unexplained deductible VAT from a different acceptance path.

### CB-H1/2/3 / preparation variants

For ZERO, prepare credit12500 with tax0. Expect the expense role and zero tax. With tax1 and all else valid, refuse the profile mismatch.

For GROSS_COST, specify required tax metadata and assert the gross-cost snapshot's exact declared meaning. Do not reinterpret the retained metadata as a new input VAT posting.

For PURCHASE full credit, prepare10000 with tax2000 and no partial-line selection. Assert `originalLines` and the original input-VAT role. Assert the actual `creditLines` key is absent in this version's full-credit snapshot. The original prose's singular `creditLine` is not the contract field. Inspect the raw persisted/returned object before any decoder could strip unexpected keys.

All three preserve the pre-existing invoice journal and add only declared preparatory rows. No unpaid capacity is consumed merely by preparation.

### CB-H4 / original-line residual regression

```text
A: net1000, VAT250
B: net1000, VAT250
initial unpaid2500
execute the supported full credit of A:1250
now unpaid1250, A credit capacity0, B capacity1250

prepare A net200 + tax50 -> InvalidJournal
prepare B net200 + tax50 -> valid proposal
```

Read cumulative usage through the actual executed-credit to immutable-review relationship. Before each branch, refresh expected invoice/allocation versions so a stale global expectation does not conceal the line-capacity guard. After executing the B credit, expect unpaid1000 and exactly the B line's new usage250.

### CB-H5 / rounding tolerance isolated from original-line capacity

Use a sufficiently large original line, such as net8000/tax2000, with no prior usage. For each fresh scenario use credit net1600 and set its gross and optional tax total consistently:

```text
credit tax398 -> refuse: outside tolerance
credit tax399 -> accept preparation under this qualified synthetic policy
credit tax400 -> accept preparation
credit tax401 -> accept preparation
credit tax402 -> refuse: outside tolerance
credit tax500 -> refuse
```

This tests the current integer tolerance; it does not certify a universal VAT tolerance. Give each scenario distinct evidence and command identity. Otherwise prior credit use or duplicate number detection can hide the intended arithmetic predicate.

### CB-R3 / corrected number scope

```text
CB-R3-local:
  used number CN-1 for same supplier in book A
  another local credit with CN-1 -> IdempotencyConflict

CB-R3-foreign-number:
  used number CN-1 only in book B
  otherwise valid credit CN-1 for supplier in book A -> succeeds
  no B identifiers appear in response

CB-R3-foreign-target:
  authorized book-A request substitutes B's invoice/evidence ID
  -> applicable child lookup refusal, no state change in either book
```

Different supplier identities within one book receive their own scope test. Similar names are not identical suppliers.

### CB-X1 / replacement: proposals do not reserve capacity

```text
fixture: purchase net10000 + VAT2500 = gross12500, all unpaid
P1: distinct credit evidence/number, net5600 + VAT1400 = gross7000
P2: another distinct credit evidence/number, same amounts

prepare P1 and P2 before any execution
assert both are proposals over the original12500 basis if current admission permits
assert actual executed usage remains0
approve exact proposals as permitted by the owner
race EXECUTION using observed overlap

assert one complete credit of7000
assert payable remaining5500
assert exactly one executed credit and one financial receipt
assert loser consumes no approval, number, domain effect or source-line capacity
assert loser returns the maintained stale/capacity contract, not an arbitrary accepted error set
```

If a future explicit reservation owner changes preparation semantics, that is a new contract and needs its own tests. It is not present merely because a plan was sealed.

CB-X2 keeps same-key preparation replay. Add same-key execution replay, distinct-key economic duplicate and failure after journal but before credit/register completion. Verify both amounts and linked identities after recovery.

## 3. SA: schedule amendment

### SA-H1 / corrected dates-only happy path

Runtime builder chooses T from the database and provisions valid periods on both sides of T:

```text
cost120000, residual0, prior impairment0
12 occurrences, each10000
occurrences1..4 posted, dates before T
occurrences5..12 unprepared/prepared but not posted, dates after T
basis current, accounts active, old/new future periods open

firstOrdinal5
replace exactly8 future dates with strictly increasing valid future dates
keep all8 original amounts and occurrence identities
remainingMinor80000
```

Expect:

```text
new revision = old + 1
occurrence count12
prefix1..4 byte-identical
suffix5..12 new dates with old amounts/identities
recognized40000
future80000
allocatedMinor120000
future_dates_v1 amendment excludes recognizedMinor and reversedMinor keys
no additional journal, voucher number or approval consumption
old revision unchanged
```

The eight future installments sum80000. All twelve sum120000. Do not assert that existing ledger rows have become 80000. This command changes the schedule, not previously posted depreciation.

### SA-H2 / remaining estimate or lifetime

Using the same posted prefix, replace the suffix with four explicit installments of20000 if that lifetime profile is supported. Count becomes8, remaining80000 and allocated120000. Expect `remaining_lifetime_v1`, `recognizedMinor40000` and the separately defined `reversedMinor` field. Keep a same-count estimate case separately for `remaining_estimate_v1`.

### SA-R1 / boundaries

Expand each bound into its own leaf ID. For dates-only, both adding and removing a suffix occurrence refuse. For a positive neighbor keep the total count unchanged. The revision limit is the actual profile constant in this owner, not the sales-document limit.

### SA-R2 / prefix versus suffix

```text
SA-R2-prefix:
  firstOrdinal5
  occurrence3 prepared instead of posted
  all remaining prerequisites valid
  -> UnsupportedProfile in the prefix branch

SA-R2-suffix:
  firstOrdinal1
  occurrence3 already posted
  -> AlreadyPosted in the suffix branch
```

Do not claim the second fixture tested a prepared prefix.

### SA-R3 / two date families

An existing unconsumed suffix date on/before database today hits the inspected old-suffix `UnsupportedProfile` rule. A replacement date on/before today, on/before last consumed date, on/before basis effective date or outside its period hits `InvalidJournal` with the earlier prerequisites valid. Locked selected period yields `PeriodLocked`.

Test each independently. Do not accept a union of those errors as the oracle.

### SA-R4/5 and SA-X1/2

Off-by-one remaining amount or conservation mismatch -> refusal and no revision. Exact no-op -> refusal. Distinct-key amendments to the same retained digest -> one new revision and one stale loser. Same-key replay returns the old result even after later unrelated work, provided current access remains valid. A later new revision does not mutate the earlier command receipt.

## 4. HI: historical item admission

### HI-H1 / concrete source inventory

For one account/currency control group:

```text
item A: original100000, outstanding40000, partly_paid
item B: original50000, outstanding30000, partly_paid
payment P1:60000
payment P2:20000
match M1: P1->A 60000
match M2: P2->B 20000
payment control80000
match control80000
```

Use a valid staged plan and compatible open-item controls. Dated matches occur on/after their payment dates. Admit the complete source snapshot. Expect one admission with retained source identities and `financialEffect: none`. No new recognition, live capacity, bank allocation or GL movement is inferred from this source record alone.

An `unknown` assertion retains uncertainty. A bounded example such as original100000/outstanding40000 can be admitted as unknown when other requirements hold, but does not establish a current settlement right. Unknown does not waive absolute bounds or create a made-up payment history.

### HI-R2/3 / chronology

Null source date is refused in `dated_source` and can be retained in the actual non-dated enum variant. Copy that enum from the contract instead of assuming it is named `undated`. If any date is present, it must still be a real date. Match before payment refuses when the dated policy applies; equal dates are a valid neighbor.

### HI-R4 / explicit conservation

```text
one payment1000, two match legs600 and600 -> refuse total1200
one payment1000, two match legs600 and400 -> allowed if item capacities permit
one payment1000, one match1001 -> refuse
one item original1000, matches from two different payments600 and600 -> refuse
```

The last case prevents checking only payment capacity. A valid many-to-many case should separately demonstrate two payments applied to two permitted items.

### HI-R5 / controls

Break payment and match totals by one independently. Also test missing required control, duplicate control key, unexpected extra key and a wrong account/currency whose numeric total happens to agree. The controls compare the exact group membership, not only grand totals.

### HI-X1/2 / distinguish keys

Same key/input/current actor -> both recover the same saved admission.
Distinct keys targeting the same already admitted plan -> only one admission; the other follows the owner conflict contract.
Missing staged plan, stale digest and unauthorized scope are independent negative cases, each with zero new financial effect.

## 5. AB: asset basis capture

### AB-H1 / unconsumed impairment basis

Use a supported clean asset whose unconsumed occurrence dates all lie after the intended impairment date and whose proposed new suffix is valid under the owner:

```text
original cost100000
opening ordinary accumulation0
effective posted ordinary recognition0
prior impairment0
new impairment5000
residual0
current carrying100000
post-impairment carrying95000
future total95000
```

Twelve exact positive future values can be eight7917 and four7916, if that explicit reviewed allocation is supported. Their sum is95000. The case must supply actual required source/review evidence, valid accounts, current basis and schedule digests.

Preparation changes no posted carrying value. Owned execution, after its WIP handoff, must commit the5000 impairment and new95000 suffix together. Failure between those writes leaves both unchanged.

### AB-H2 / disposal basis

Use a separate disposal-eligible fixture. Do not reuse an impairment fixture containing overdue unposted installments and presume it is valid for disposal. Assert the gross, ordinary contra, impairment and carrying fields independently. Input admission rejects fields unsupported by the selected union member through its defined contract.

### AB-R1 / recognition and reversal

With a posted10000 occurrence later reversed and another10000 occurrence still effectively posted:

```text
recognizedMinor10000
reversedMinor10000
current carrying = original carrying -10000 - prior impairment
```

Reversed is not subtracted again. Wrong reversal purpose, missing reversal identity or an unsupported correction relationship each has a separate invalid neighbor. If a qualified later-history correction is not yet supported, preserve that limitation instead of inventing a simple inverse.

### AB-R2 / corrected consumed-prefix cases

```text
AB-R2a:
  posted1..3, prepared4, unprepared5..12
  all suffix dates valid and after the chosen date
  -> contiguous consumed prefix and unconsumed suffix
  not a prefix/suffix rejection merely because4 is prepared

AB-R2b:
  posted1..3, prepared4, posted5, unprepared6..12
  -> impairment scan refuses a consumed occurrence after suffix start

AB-R2c:
  disposal with any unprepared/prepared occurrence strictly before disposal date
  -> UnsupportedProfile in the inspected disposal rule
```

The old plan's claim that the same R2b fixture necessarily passes disposal is removed. A monotonically dated overdue unconsumed installment can make both profiles refuse for different reasons. To test a particular branch, establish all other prerequisites; do not seed impossible public schedule chronology to force a desired result.

### AB-R3/4/5/6/7

Keep separate account-role conflicts, basis date floor, later impairment date, complete/over impairment, future-total mismatch, missing evidence and disposal polarity cases. For a boundary-success neighbor such as impairment one unit below carrying, also ensure the required positive future installments and residual allow it. A valid arithmetic subtotal alone does not make the whole plan valid.

These tests can use explicit synthetic role accounts. Choosing every real company's BAS account is not a prerequisite for proving the arithmetic. Actual-company classification remains separately qualified.

## 6. XC: revised cross-cutting cases

### XC-1 / exact no-effect and rollback observation

Read actual book/series counters plus rows, approval use, command results, outbox intent and each operation's register effects. For nonfinancial operations require financial delta exactly zero. For a refused mutation require no successful command receipt. Use the declared audit-attempt policy rather than pretending every table in the database must be unchanged.

### XC-2 / authority matrix

Per supported workflow test legitimate operator, ordinary agent where allowed, disallowed agent action, accessible local scope with foreign child, inaccessible top-level scope and current credential/member revocation. Validate the current shared contract's error envelope. Denying all requests is not successful authorization.

### XC-3 / exact money

Keep9007199254740993, add line-bound maximum and maximum+1, aggregate beyond line bound, fractional lexical values, exponent text, negative zero and numeric JSON input. Exercise actual line credit/partial capacity arithmetic, not only a pass-through large-money post. String transport plus exact DB observation are both required.

### XC-4 / digest and variant shape

Use the independent canonical bytes in `ORACLE-EXAMPLES.json` as microvectors. Hash the exact schema-defined body without self-digest where applicable. Object-key permutation must preserve it; changing array order, meaningful amount or identity must change it. Assert full/partial credit and date/estimate variant keys individually. Unknown optional keys cannot be silently treated as part of the approved payload.

### XC-5 / required additions to the original scope

Add observed execution races, late failures after domain writes, actual commit-time rejection, response-loss recovery, snapshot completeness and current authorization after waits. Use the detailed protocols in `REVISED-TEST-PLAN.md` rather than a fresh timing scheme per worker.

## 7. How to treat disagreements

When the fixture violates the contract, fix the fixture. When implementation violates an accepted financial invariant, record a product defect and retain the failing test. When policy is genuinely unsettled, mark a contract decision and do not claim a passing oracle. Accounted examples can inspire scenarios but do not decide this application's tenant, approval, rounding or correction semantics.
