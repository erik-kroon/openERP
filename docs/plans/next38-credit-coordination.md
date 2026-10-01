# NEXT-38 credit integration ports (working, unverified)

Credit owner creates `packages/contracts/src/cash-credits.ts`. Parent/year-end owner:
add `export * from "./cash-credits";` to `cash-method.ts`, then add three endpoints
to its existing group and handlers to its existing route chain:

| Operation | POST path under book | Payload | Success | Application export |
| --- | --- | --- | --- | --- |
| `prepareCashCredit` | `/commerce/cash-method/credits` | `PrepareCashCredit` | `CashCreditPlan` | `prepareCashCredit` |
| `approveCashCredit` | `/commerce/cash-method/credits/:id/approvals` | `ApproveCashCredit` | `CashCreditApproval` | `approveCashCredit` |
| `executeCashCredit` | `/commerce/cash-method/credits/:id/execute` | `ExecuteCashCredit` | `CashCreditReceipt` | `executeCashCredit` |

Application exports live in `application/commerce/cash-credits.ts`; command shapes
match year-end's token/scope/id/idempotencyKey/input port. The revised credit input
is `{invoiceId,draftId,expectedRevision,expectedDigest,accountingPeriodId,series,
lineMappings:[{creditLineId,sourceLineId,treatment}],rationale}`. No amount, date,
number or evidence assertion is accepted. The source owner reads the current
retained supplier draft, validates every mapped line through the existing purchase
compiler and original reviewed treatment, and derives source amounts/date/number/
evidence. A consumed credit draft is sealed by the existing draft-admission port.
Supplier drafts have no kind field; this owner designates the retained positive
credit original through the independently approved credit review, rather than
claiming a nonexistent draft discriminator. Parent may separately adopt a shared
invoice/credit discriminator; that is not implemented here.

The credit owner extended the real shared VAT schema in
`packages/contracts/src/vat-returns.ts`: `VatFactInput.netMinor`, `vatMinor`,
`grossMinor` now use signed exact minor-unit fields, and `VatFact` has optional
`cashMethodCredit`:

```ts
Schema.Struct({
  creditLineId: A.Identifier,
  originalRecognitionId: A.Identifier,
  originalVatFactId: A.Identifier,
  policy: Schema.Literal("tax_first_cumulative_v1"),
  originalGrossMinor: A.MinorUnits,
  originalTaxMinor: A.MinorUnits,
  recognizedBeforeMinor: A.MinorUnits,
  recognizedAfterMinor: A.MinorUnits,
})
```

The credit owner did not edit shared `cash-method.ts`; the year-end owner integrated
its reexport and HTTP contracts. The credit owner extended the real SE calculator
with `cash_credit` date basis, `after < before`, gross delta `after-before`, and
the negative cumulative tax delta. Ordinary manual negative facts are blocked
unless they carry the owned linked credit metadata. The original positive fact is kept;
only the linked negative fact is appended, never a simultaneous subtraction or
withdrawal of the original.

Credits dated at/before an executed fiscal cutoff refuse `StaleDependency`; receipt
and membership stay immutable. Later credits post in their own open qualified
period. Locked credit periods refuse `PeriodLocked`. Amendment workflow itself
remains year-end/closing-owned.

The credit owner now extended the native projection in `db/commerce/invoices.ts`:
cash credits contribute their gross to credited/effective totals and their count
to creditCount/allocationVersion. Commercial-only null-voucher credits remain in
the sum. Recognized corrections validate the current voucher/control amount,
their original recognition/coverage link and their owned negative VAT component.
Execution rechecks native outstanding against all retained coverage lines before
commit. The HTTP scenario then pays the remaining100000 and expects VAT20000 and
native outstanding0, rather than paying the original125000 again.

Retained credit components are now kept through capture, not reduced to gross.
Both unrecognized and recognized credits must match the original commercial
suffix's cumulative net/tax/deduction split. Independent refusal vector:
originalN5/VAT1/G6 and creditN2/VAT1/G3; the actual suffix is net3/VAT0, so the
retained source refuses without writes both before and after year-end.

The source alias adoption fence is now present in `db/commerce/cash-invoices.ts`:
both `readSourceAdoption` and `readCashOriginalAdoption` return executed
`cash_method_credits` whose `evidence_id` matches, so another labelled draft cannot
accrue or re-admit the retained credit source. Original draft reuse is already blocked by the extended
`readSealedDraft` query. Application/posting admission protects the sealed credit
action and its correction voucher; VAT component edits/withdrawals and tax-line
copying recognize the new credit ownership via `db/commerce/cash-payments.ts`.

## Handoff, unverified

No credit checks, tests, commits or migrations were executed by this agent. Parent
reported API type checks passing before the final shared schema/proof additions;
that does not verify this final source or behavior. Parent serializes all gates.

The new HTTP/PostgreSQL scenarios cover unrecognized commercial-only25000,
recognized-unpaid25000=N20000+VAT5000 after sealed year-end, exact replay/fresh-key
refusal, paid-principal refusal, backdated amendment refusal with sealed receipt
preservation, posted-credit-source reuse, malformed component writes, and late
post-journal/post-VAT failure followed by original-key recovery. The negative fact
is exposed by the existing VAT fact read and manual withdrawal must refuse.
The credit E2E file now also specifies negative January2027 synthetic box48=-5000,
wrong-plan approval refusal, revoked reviewer refusal, retained-draft revision
staleness, and a concurrent credit/payment race with one commit and one stale
refusal. These scenarios are added source, not passing runtime proof.

The combined-run HTTP500s recorded in `test-results/next38-complete/worker.json`
for requests `4daa9e69-b11b-41e4-b895-86a7bf3849e7`,
`f604f79f-51c5-484e-8fb1-c8fb5a30f627`, and
`55a343b7-d00a-4afb-bdc2-4650f319c36f` all report a missing
`evidenceRefs[0].locator`. Credit posting actions now supply retained draft and
invoice locators, matching the existing year-end posting boundary. Root's extracted
`creditAssignments` helper is unchanged. No checks or reruns were made here.

Exact narrow real-surface command after parent integration:

```sh
OPENERP_E2E_ARTIFACTS=test-results/next38-credit bun run test:e2e apps/api/tests/cash-credit.e2e.test.ts
```

The existing global setup owns disposable PostgreSQL/workerd and repeatable
results/source-integrity artifacts. This command has **not** been run here.
