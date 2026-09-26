# Consequential decisions made in this wave

These are proposed financial/application designs for NEXT-26..50. They do not activate a legal profile, change repository code or grant execution authority. Their source anchors and limitations are in SOURCES.md. They preserve the application-owned boundary and the reserved first-wave owners.

## 1. Record extraction suggestions without replacing reviewed facts

Extraction runs against an immutable original and returns source-located suggestions. The review performs a three-way comparison against the draft revision on which extraction started and the current draft. Confirmed human changes win; conflicts stay visible. Accepted invoices receive correction suggestions, never rewritten fields. This closes the useful lifecycle around the existing inbox rather than restarting receipt matching.

## 2. Resolve party identity in a retained overlay

Same legal identity can redirect discovery, but original invoice and payment relationships remain unchanged. Neither legal identity resolution nor a common bank account grants permission to net debts or reuse payment capacity. An erroneous merge is another reviewed identity decision with downstream impact, not mass rewriting of historical foreign keys.

## 3. A recurring cycle is independent of template revision

The occurrence key uses the agreement and stable cycle, while the selected template is retained as input. Changing price or template version cannot generate a second invoice for the same cycle. Service-coverage checks catch cadence changes that might overlap prior billing. Dates are calculated from the original anchor, not successive clamped dates.

## 4. Customer credit is its own liability, not negative AR

For a same-currency invoice, original gross G, effective credits K and paid amount P imply:

```text
unpaidAR = max(G-K-P,0)
creditPrincipal = max(P-(G-K),0)
```

A new credit first clears unpaid AR and then increases a refund/applicable-credit liability. Refunds debit that liability against actual cash. They do not reverse sales or VAT again. Unapplied cash has its own origin and is distinguished from taxable advance receipts. The ordinary invoice capacity cannot become negative to hide either condition.

## 5. Payroll handoffs consume existing liabilities

An employee receipt claim can be recognized once and paid through payroll or direct payment, not both. A taxable mileage award in the initial accrual profile establishes its entitlement liability at award time. Payroll calculates its tax/reporting consequences and debits that existing liability rather than recognizing the cost twice. Variable/holiday pay similarly releases previously accrued holiday and social provisions before expensing only a true difference.

Paid payroll correction distinguishes a new payment, a qualified future-pay adjustment and an actual gross recovery claim. Original withholding and cash do not disappear because a later entitlement is lower. The exact permitted reporting case is a qualified input, with original item identity preserved.

## 6. VAT assessment is not reclassification or payment

The two active VAT owners retain reclassification and amendment effects. NEXT-37 owns authority assessment and an explicitly qualified precision bridge.

```text
N = exact accounting net
R = reported amount represented in minor units
A = actual evidenced assessed charge

initial settlement vector = -N
qualified rounding bridge = +(N-R)
assessment vector = +A
```

If A=R, those settlement vectors clear. An unexplained A-R remains a difference; it is not a rounding plug. Existing tax-account journal/match evidence is adopted without posting/reserving twice. Bank-to-tax-account cash transfer remains separate.

## 7. Cash-method recognition has explicit source coverage

Each invoice line has disjoint recognized portions and unrecognized commercial outstanding. Payment recognizes only the part not already covered by a prior recognition. Year-end records eligible unpaid portions exactly once. Next-year payment settles their AP/AR positions and does not create another cost/revenue or VAT fact. Complete year-end capture must include population changes, not merely the invoices on the first page.

## 8. Processor clearing uses gross events, not net payout revenue

Stripe balance-transaction identities own charge, refund, fee and payout effects. A charge settles an already recognized sale, a refund consumes an owned refund liability and a payout moves processor balance into transit. Bank receipt clears transit. Each event is accounted once even when retrieved through several provider endpoints. Disputes/reserves are not automatic VAT credits or hidden operating costs.

## 9. Foreign cash and foreign obligations are different capacities

Commerce continues to own the foreign payable/receivable. Foreign cash has native quantity and book carrying under its own cash owner. A payable paid with foreign cash consumes both capacities atomically. Their different carrying releases explain realized FX; no second principal expense or cash entry is created. Native and book-currency controls reconcile separately.

## 10. A late FX correction adjusts carrying attribution, not actual cash

Replay the complete supported dependent chain from a known anchor, inserting the corrected valuation and retaining actual quantities, cash and fees. Compare the desired role/date vectors with prior effective vectors and post only the difference.

Example: an AR of110000 was settled for116000 with old realized gain6000. A corrected prior-year valuation to115000 requires:

```text
December: AR+5000 / valuation gain-5000
January:  AR-5000 / realized gain+5000
```

Cash remains unchanged, final AR remains zero and total gain remains6000. Different period attribution is not zero work merely because the lifetime total matches. Unsupported consumers or closed dates stop the complete repair rather than yielding a partial adjustment.

## 11. Economic impairment reversal needs a counterfactual cap

The cap is computed from the qualified without-impairment history, not the current reduced schedule. The approved target cannot exceed that cap or the eligible impairment reversal capacity. Journal, valuation effect and new future schedule commit together. A fully impaired but still-owned asset has explicit zero-carrying state, no fake positive installment and no automatic disposal.

## 12. Analytical restatement does not modify original dimension assignments

Original tags remain financial evidence. Reviewed classification revisions form an overlay with its own cutoff. Every report declares original or reviewed mode and pins exact classification IDs. By-value totals reconcile to the same unfiltered total. A project retag cannot alter tax, account, currency or journal amount.

## 13. Cash-flow classification must explain the entire balance change

Actual cash flows are categorized through owned economic relationships. Internal transfers are eliminated only with evidence. Exchange carrying effects and perimeter changes are explicit bridges:

```text
closing = opening + external net flows + exchange effects + perimeter changes
```

Unknown rows can produce a zero arithmetic difference and still make the statement incomplete. An unpaid invoice or depreciation entry is not a cash movement.

## 14. Upload, signing and fulfillment remain separate

Signing binds a specific purpose and exact content manifest. A successful identity login is not a document signature. The original annual report, a faithful electronic copy and authority-hosted fastställelse certification have separate relationships and evidence. Local upload success does not fulfill a submission obligation.

NEXT-49 therefore verifies typed same-entity/period/revision outcome references. A free-text 'done' can remain a reported note but cannot become a verified authority receipt. Reminder dismissal is not fulfillment.

## 15. Agent context is a read model with explicit unknowns

The cross-domain context snapshots existing owners at a coherent cutoff. It groups repeated questions without merging financial effects. A missing or inaccessible module cannot be represented as no work. Deltas compare owner identities and revisions; unavailable data is unknown, not resolved. Permission changes cannot leak prior private context. Shorter output is valuable only when it preserves the financial blockers and safe next actions.

## Not selected

No second ledger, generic workflow interpreter, arbitrary plugin runtime, new queue infrastructure, general CRM, warehouse/inventory project, Rust extraction or multi-country launch is added. The loan lifecycle is a proposed expansion of existing funding, explicitly labelled rather than falsely attributed to a source defect. Statutory tables and provider schemas remain qualified inputs, not invented constants.
