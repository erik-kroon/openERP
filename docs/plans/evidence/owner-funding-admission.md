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

`test-results/owner-funding-loan-multirow-acceptance-20261001`:12/12 real PostgreSQL/workerd
E2E cases, no failures/skips, stable source inventory
`26d23023b62175c3861e59dda2a8b6d4bf8334c0d28860b99430aa63a67f9bc9`.
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

## Remaining packet7 acceptance

- Share-capital subscription/allotment/registration has no released application
  owner. Loans/contributions do not substitute for paid or registered capital.
- Funding from already-posted cash needs reviewed unused-capacity adoption; this
  slice refuses rather than debiting cash twice.
- Complete opening-transfer lineage and correction/recovery still need
  end-to-end qualification. No whole-packet or five-packet completion is claimed.
- No live bank/provider, real company fact, registration submission or deployment.
