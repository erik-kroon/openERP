# Design decisions for NEXT-101 through NEXT-125

These decisions define new bounded product behavior. They do not establish that the first 100 packets are implemented, qualify a statutory profile or authorize an actual financial operation. The shared Effect transaction contract and the earlier financial owners remain in force.

## 1. Delegation is an intersection of permissions, not an account copy

A firm employee can act for a client only when the client's active grant, the firm's role, the particular employee's assignment and the selected book/period/privacy permissions all allow the operation. A client grant cannot turn every firm employee into an operator. Payroll access remains separately scoped.

Portfolio views run authorized per-book reads and identify each capture's cutoff. They do not imply a cross-book transaction or consolidated financial statement. Current access is required even when reading a saved client report. A revoked relationship must not leave a confidential stale cache visible through an old portfolio selection.

## 2. Uploading a response does not resolve the accounting question

An evidence request has a fixed requested scope and a reply relationship. A submitted file is a response, not proof that it answers the request or establishes the asserted fact. The reviewer selects and confirms the relevant source evidence through the owning accounting/case operation. The request then records the exact resolution evidence.

A new reply to a previously resolved question can create an impact review. It does not overwrite a posted invoice, signed artifact or old review acceptance. Guest tokens grant access only to their request and permitted response operation.

## 3. Substantiation and analytical allocation have separate purposes

A substantiation schedule explains a selected balance at a frozen financial cutoff using its original components and genuinely independent evidence. Another query over the same ledger can establish arithmetic consistency but is not independent evidence that the transaction occurred.

Shared-cost attribution is an analytical partition. Every source cost is counted once, either directly or through its selected allocation shares. It creates no new expense or VAT entry. For an exact source amount of 10,001 and weights 1:2, the declared largest-remainder policy yields 3,334 and 6,667. The unfiltered total stays 10,001.

A financial reclassification of an account or tax treatment is not disguised as an analytical allocation. It remains an approved operation at the original financial owner.

## 4. Project margin uses recognized revenue, not whichever cash figure is available

The project view identifies billed consideration, earned revenue, unbilled assets, deferred revenue, cash and recognized costs separately. These are joined through retained source coverage, not assumed to be interchangeable.

A useful reconciliation is:

```text
recognized revenue = billed net
                   + movement in earned-unbilled revenue
                   - movement in deferred revenue
```

The actual qualified recognition events remain the authority. The equation is a reconciliation witness, not permission to manufacture missing revenue. Cash collection and customer credit are separate views. Shared analytical costs come from NEXT-104 without duplicating direct costs.

## 5. Service retainers consume entitlement and financial coverage together

A retainer covers a finite nontransferable service entitlement under a specific contract. It is not a generic financial wallet or gift-card scheme. The advance, tax and deferred-revenue owners retain their earlier financial effects.

Using 150 of a retained 600-minute entitlement funded by net consideration of 100,000 releases 25,000 of that deferred consideration under the illustrative proportional policy. The remaining entitlement is 450 minutes and the remaining deferred amount is 75,000. The same work component cannot also become an ordinary billable time entry.

Expiry does not automatically turn the remaining liability into revenue. Refund, extension, cancellation and enforceable expiry use the applicable reviewed contract and qualified recognition policy.

## 6. Provision targets are remeasured against effective prior provisions

The onerous-contract and warranty packets are qualified provision profiles, not extensions that every K2 company automatically needs. Eligibility, unavoidable cost, recoveries and actual obligation evidence must be established before measurement.

For a supported onerous remaining contract, the target is the reviewed unavoidable net loss. A later measurement posts target less the effective remaining provision, after recorded consumption. The actual fulfillment cost is not the same thing as the provision release. For warranty cohorts, the target must reflect claims already settled and the remaining eligible exposure rather than reusing the original unit count forever.

A valid provision cannot become an automatic smoothing reserve. Independently justified estimate changes retain their evidence, rate/model version and effect history. Repairs, invoices and payroll that consume a provision reuse their existing recognition owners rather than create the cost twice.

## 7. Insurance and debt forgiveness preserve the underlying event

Damage, disposal or repair is accounted for separately from insurance recovery. A claim request is not automatically an asset. Recognize a recovery only when the selected profile's entitlement/evidence threshold is met. Direct insurer payment of a supplier invoice reduces the payable and insurance receivable without inventing a bank movement.

Loan rescheduling retains outstanding principal and accrued interest. Legally effective forgiveness identifies the exact recognized components being extinguished. Cancelling unaccrued future interest is not a gain equal to all of those hypothetical payments. An amended bank instruction must resolve existing reservations and unknown outcomes before replacement.

## 8. Annual VAT true-up changes deduction, not supplier consideration

Select the complete eligible common-cost population and the qualified final allocation method. Do not apply one turnover ratio to every purchase. Directly attributable costs, disallowed costs, capital-goods adjustments and private-use questions have their own treatment.

For each selected original component:

```text
new deduction adjustment = qualified final target
                         - effective deduction already recognized
```

An additional deduction for an already fully expensed cost debits input VAT and credits the attributable non-deductible cost. Supplier payable and cash remain unchanged. Repeating the same target produces zero additional deduction. A source credit or changed driver requires a fresh complete basis; the existing VAT amendment owner handles declaration consequences.

## 9. Specialized VAT families do not borrow domestic return identity

Domestic construction reverse charge requires the supported service and customer facts. Ordinary invoicing with a zero tax rate is not equivalent because the required reverse-charge basis, notices and buyer-side effects still exist.

Union OSS keeps country/scheme liabilities, original-sale identity and reporting-currency conversion distinct from ordinary domestic VAT. The book carrying value and euro reporting target can legitimately differ; their reconciliation requires its own qualified conversion/settlement effects. One economic sale cannot appear as two recognitions because both the order and processor deliver records.

Foreign EU input-VAT recovery is also distinct. A foreign tax amount is not deductible Swedish input VAT merely because it appears on an invoice. Initial recovery eligibility, a recognized approved entitlement and the actual refund are separate stages.

## 10. Payroll sources have different cash, tax and expense effects

Travel-allowance reduction and a taxable meal benefit are independently classified. A meal can affect one or both according to its applicable facts; the calculation cannot assume they are the same amount or event. Mileage remains its existing separate award.

A recurring car benefit is a noncash tax/reporting base, not another purchase cost. An actual qualified net payment by the employee may reduce that base. A gross salary reduction is not automatically the employee paying for the benefit.

Prospective salary exchange changes the agreed future cash salary and creates the corresponding pension entitlement under the actual agreement. It does not also subtract the exchanged amount as a net-pay deduction. The pension provider invoice consumes already accrued obligations; it must not duplicate the pension expense. Retrospective paid cases use the existing correction owner.

## 11. Tax statements and capital events use real identities and conditions

KU20 and KU25 have different reporter/recipient obligations. A company paying interest to its bank is not automatically required to create a KU25 for itself. Accrual, reportable availability, cash payment and withholding are retained separately under the qualified reporting profile. Replacement preserves the required statement identity.

A cash share subscription has actual resolution, payment, allotment and registration conditions. Cash received is not proof of registered share capital. Under the selected illustrative profile, pending funds transition into unregistered nominal/premium components, then into their registered classifications when evidenced. Overpaid cash does not silently issue more shares.

## 12. Preliminary-tax estimates do not alter assessed installments

The estimated annual tax and the authority's currently effective preliminary schedule are separate records. A lower forecast does not reduce the next legal installment until a qualifying decision changes it. Actual tax-account debits and payments remain their respective source-backed effects.

The annual current-tax expense is not calculated by subtracting bank payments from the expected tax amount. Estimated expense, prepayments, assessed liabilities and settlement controls must reconcile without collapsing into a single net number.

## 13. A standing mandate is a new, explicit authority kind

Book Zero keeps exact human approval as its default. NEXT-121 introduces a deliberately separate opt-in contract for one narrow stable purchase-recognition case. It excludes payment, refunds, legal issue, payroll, closing, correction and filing.

The initial exposure measure is gross recognized purchase amount, not the sum of debit and credit lines. Supplier, daily and lifetime limits share atomic consumption rows. Renewing or replacing a mandate cannot reset the shared budget. A credit does not automatically replenish exposure in the initial policy.

The financial effect and budget consumption commit together. Current admission is still checked, but successful identical replay precedes new-work limit and expiry checks. With a limit of 100,000, used amount 70,000 and a new event of 25,000, usage becomes 95,000. A replay stays 95,000; another 10,000 is refused. Two competing 20,000 events cannot both fit.

## 14. Cash-constrained proposals preserve creditors' rights

The payment planner searches a finite declared set of permitted dates, complete payments and authorized installment amounts. It never invents a smaller permissible payment because available cash is low. Candidate obligations already represented in Cash are removed once before the chosen alternatives are inserted.

Results distinguish optimal within the declared model, feasible within a search budget, proved infeasible, exhausted search and incomplete financial inputs. The deterministic objective does not turn missing source coverage into certainty. A proposal still needs fresh exact bank-payment authorization and current residual checks.

## 15. Provider continuity and refunds have their own bridges

Changing a bank-feed provider does not create a new bank account, opening balance or economic transaction. The new stream is retained and reviewed against the same account. Only proved source aliases or reviewed same-event relationships allow reuse of existing bank observations and financial capacity.

Autogiro payer consent and the company's collection authority are distinct from accounting recognition. An accepted collection instruction does not settle AR. Returned cash restores the supported original capacity through an owned correction, subject to later credits/refunds and exact source evidence.

A processor refund reserves customer entitlement before dispatch. Processor cash can leave before the customer liability is qualified as discharged. The selected transit model records those stages separately. Pending or unknown outcomes cannot justify an alternative bank refund. The processor source owner routes the same balance transaction to this refund owner instead of posting a second generic refund journal.

## Scope discipline

These are delivery contracts, not a mandate to add every specialized profile before a release. Firm workflows and service-retainer/project reporting are broad product improvements where relevant. Specialist VAT, provision, benefits, capital and collection profiles follow actual customer requirements. Existing unfinished first-wave behavior remains with its existing packet, rather than being renamed to inflate this wave.
