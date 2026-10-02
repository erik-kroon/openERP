# Packet7 — retained-source owner funding admission

Status: implemented and runtime-verified funding prerequisite; packet7 remains open.
Application owner: `apps/api/src/application/subledger/owner-operations.ts`.

Funding preparation names a retained bank statement/row, evidence, reviewed owner,
accounts and legal form. The owner derives positive incoming cash from the retained
observation, checks its account/date/currency/evidence and refuses matched or
allocated capacity. It does not accept a caller-stated amount. Legacy amount-only
review schemas remain readable, but fresh approval/execution refuses their missing
source admission; no old immutable receipt is rewritten.

Approval and execution revalidate source capacity under the existing book-scoped
transaction. Native posting, bank match, owner record/effect and receipt commit
together. Exact replay recovers the receipt. A second approved preparation loses
its capacity after the first commits and refuses StaleDependency.

New receipts distinguish `recordedAmountMinor` from `ownerClaimMinor`:
contribution funding remains recorded at its full amount but creates no repayable
claim. Migration0058 binds both new fields to the table amount and mode, preserving
the original exact check for historical receipts without the new field. Historical
contribution receipts must not be treated as repayment authority merely because
their older informational field was named ownerClaimMinor.

## Repeatable proof

`test-results/owner-funding-posted-history-final-20261001`:12/12 real PostgreSQL/workerd
E2E cases, no failures/skips, stable source inventory
`138ec770794e179bd88954f8c0bd7dbc984c488033b8683f3228f63f970c6ff6`.
Three funding cases cover shareholder loan, conditional contribution and
unconditional contribution, each with independently retained100000 incoming cash.
Both contribution cases have0 repayable claim and use reviewed2093 equity; the loan
uses2893 liability. Each creates one bank match and exact100000 debit/credit, rejects
asserted999999, wrong posting date, absent foreign source and duplicate admission.
A separately approved competing plan refuses after source use. Real P0001 fault at
bank-match insertion rolls the loan voucher back to0; same-key retry then commits
once. The other9 cases preserve the verified approval-batch lifecycle.

Migration0059 admits native `repay_owner_loan`. Its amount derives from one unused
negative bank row and consumes only a current original shareholder-loan effect for
the same owner, control account and currency. A retained40000 payment consumes
100000 loan capacity and leaves60000 in both register and ledger. Same-key replay
preserves the receipt; ordinary MCP reads recover it. Both contribution types
refuse loan repayment, and a140000 source payment refuses overconsumption of the
100000 loan. The overcapacity fixture's bank original has independently declared
cash beyond this loan; this is not a reconciled whole-book bank balance claim.

Each funding original also contains an independent30000 second row. That row
remains admissible after the100000 first row commits. Retained owner locators are
bank row ordinals within evidence, not operation-mode labels; bank matches fence
reused row capacity atomically. The whole-evidence duplicate-recognition fence
continues unchanged for noncash document owners. Final owner/ledger controls have
0 unexplained differences,90000 remaining loan or130000 contribution equity.

The follow-up posted-source probe exposed a missing fence at the earlier multi-row
revision. Current admission also inspects all voucher history referencing the
original: only prior native funding/repayment receipts with source-linked bank
matches permit further unused rows. An independently posted50000 cash source
without that native lineage refuses AlreadyPosted, not a second funding debit.
This negative fixture intentionally leaves a generic unregistered owner posting;
the earlier0-difference control is not claimed to cover that later unsupported
posting. Adoption remains separate work. The failing probe and its forward repair
are retained; the earlier source inventory does not prove this newer boundary.

## Remaining packet7 acceptance

- Share-capital subscription/allotment/registration has no released application
  owner. Loans/contributions do not substitute for paid or registered capital.
- Funding from already-posted cash needs reviewed unused-capacity adoption; this
  slice refuses rather than debiting cash twice.
- Opening transfer, proposal refresh and its reviewed correction now have
  [retained REST proof](opening-capital-transfer.md). Historical loan-to-owner
  capacity adoption and native funding/repayment correction remain open.
  No whole-packet or five-packet completion is claimed.
- No live bank/provider, real company fact, registration submission or deployment.
