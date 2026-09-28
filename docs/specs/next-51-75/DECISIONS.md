# Design decisions resolved for NEXT-51..75

These are original implementation choices to qualify under the selected profiles. They do not change repository source or activate legal/accounting support. The source map identifies the current requirements and primary external facts.

## Separate recognition from billing, payment and reports

Mixed-rate and cross-border documents extend the original invoice/credit owner. Customer advances, revenue deferral and installment due dates remain different components of one financial story. A recurring invoice determines billing occurrence, not when all revenue is earned. A payment link does not issue another invoice. VAT, EU sales statements and employer/corporate returns consume their owned financial facts rather than reconstructing the books independently.

## Customer advance conservation

For a qualified taxable advance `GA=NA+TA`, receipt debits cash GA and credits advance liability NA plus VAT TA. A final supply `GF=NF+TF` can consume that advance under a compatible rule:

```text
Dr AR                    GF-GA
Dr advance liability        NA
Cr revenue/deferred         NF
Cr newly recognized VAT  TF-TA
```

The journal balances because GA=NA+TA and GF=NF+TF. Lifetime VAT is TA+(TF-TA), not TA+TF. Different rates, partial supplies or incompatible tax attribution require their own qualified branch. A security deposit and an overpayment are not forced into this model.

## Supplier advance conservation

A paid supplier advance GA with already deducted VAT DA carries asset GA-DA. Final invoice GF with eligible deduction DF creates cost GF-DF, new deductible VAT DF-DA, advance release GA-DA and payable GF-GA. Those components balance exactly. Gross advance carrying with deferred initial deduction is another explicit supported state, not an inferred missing tax value.

## Revenue deferral is net of its separate tax history

The schedule consumes the net revenue liability under the agreed service recognition rule. It does not postpone or repeat the invoice's independently qualified VAT. A contract change recomputes future recognition from actual remaining source capacity. A credit allocates earned and unearned consideration and retires the affected future schedule authority atomically.

## Payment terms partition one debt

Installments sum to the existing face/residual amount. A payment promise can move expected cash timing without editing legal due dates. Credits, discounts and write-offs update the same native obligation; reports cannot each derive a different outstanding amount. A customer portal shows saved statement facts separately from live residuals.

## Settlement differences need a cause

A small residual may be an agreed price discount, a bank fee, FX, cash rounding, tax change or unpaid principal. Size alone selects none of them. For a qualified customer discount P=C+dN+dT, debit cash C, discount/revenue dN and tax reduction dT against AR P. Without discount entitlement, the same short payment leaves principal outstanding.

## Allowance, loss and recovery are distinct

An allowance changes book valuation without forgiving the legal claim. A confirmed write-off consumes the appropriate AR and eligible VAT relief. For gross G, tax relief T and previously provided allowance A, the remaining loss expense is G-T-A. It can be negative when an earlier allowance needs release. Later cash recovery links the old written-off capacity and restores only tax actually relieved under the applicable treatment.

## Commitments never become duplicate actual spend

Budget exposure is actual recognized cost plus unreplaced order commitment plus requests not yet replaced by orders. The same source amount is not counted at all three stages. Hard budget stops apply before new discretionary commitments. A real supplier obligation must still be recorded with the appropriate breach/exception evidence rather than made invisible.

## Bank messages are evidence, not accounting commands

A statement parent entry and its nested transaction details describe the same money. The importer proves the selected decomposition or retains the parent with a diagnostic. A payment-file status can authorize no inference beyond the bank's actual semantics. Accepted instruction is not booked payment. Bank settlement has its own retained source and once-only allocation.

## External tax transfer, signature and outcome are independent

A VAT or AGI API draft may still require signature/submission. A corporate tax-file transfer may still await signature. The exact service profile determines what occurred. The obligation is fulfilled only by the required same-scope outcome, not a successful network request or a nonempty reference. A pending or unknown attempt cannot be duplicated with a new key to manufacture certainty.

## Method changes preserve recognized coverage

At a qualified cash-to-accrual transition, only the eligible unrecognized remaining portions receive new recognition. Previously paid or year-end-recognized portions stay untouched. In the opposite direction, old recognized open items remain a retained cohort; the app does not reverse them all or change historical VAT by flipping a current method field. Activation and its necessary coverage/financial effects form one controlled transition.

## Not selected

No new lending/card platform, inventory engine, consolidation suite, alternative SQL workflow layer, arbitrary rule interpreter or separate job runtime is added. Managed services and third-party production access remain explicit product/provider decisions. Original reference code has not been copied.
