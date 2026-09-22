# Owner expense and funding foundation — working handoff

Status: source package complete for root integration. No SQL, API, browser or failure behavior has been run by this owner.
Reserved migration: `0610-owner-register.sql` (new; every existing migration through0900 is immutable).
No Git operation, dependency, test, fixture, migration, database write, server or build is authorized here.

## Accepted boundary

Retain evidence-backed owner identities and source records without claiming accounting activation.
Explicitly distinguish `company_record` from `synthetic_example`; nature is immutable and never
inferred from the book profile. Company records remain available for review but cannot use the
synthetic accounting bridge. No real-company readiness, VAT, deductibility, opening completeness,
shareholder-law conclusion, payment initiation or native sales operation is introduced.

Register privately paid expenses, funding and settlement sources. Classification is separately
unreviewed/unknown, owner expense, owner reimbursement, shareholder loan, loan repayment,
conditional contribution or unconditional contribution. Contributions never imply repayment rights.
An operator records the accountant-reviewed classification, evidence and explicit control account;
operator status is not proof of professional credentials or legal correctness.

Source identity, owner, currency/scale, exact gross amount and original date/evidence are immutable.
Description, proposed classification and opening/current/unknown origin append revisions. Source
identity is unique both by supplied source key and retained evidence+locator. Errors in immutable
financial identity require a future linked correction, not deletion or a new guessed identity.

## Design

- New scoped immutable owner identity records; no dependency on synthetic-only commerce counterparties.
- Retained records and immutable classification revisions. Reviews bind the exact revision digest.
- Synthetic-only bridge to explicitly selected existing kernel proposals/posted control lines.
  No direct ledger writes or automatic account/tax choices. Require matching source evidence/locator,
  amount, currency/scale, control account and classification side. Real/unreviewed records block it.
- Domain triggers gate kernel preparation/posting for matching registered source occurrences.
  Posting requires an exact current reviewed proposal attachment. Old attachments become stale after
  a revision/review/configuration change; the ordinary kernel still owns approval/execution/receipts.
- Posted links are immutable effects. A posted effect locks classification and revision changes.
  Correction/reversal of a linked voucher is blocked until a supported linked release exists.
- Owner/commerce posted-control-line claims are mutually exclusive. Bank observation matching remains
  a separate authority. Bank accounts cannot be declared owner control accounts.
- Reimbursement/loan repayment allocation plans reference one posted settlement effect and 1–50
  compatible recognized claims for the same owner, classification, control account and currency.
  Separate exact operator approval/application; immutable legs conserve claim and settlement capacity.
  Conditional/unconditional contributions cannot be reimbursed through ordinary allocations.
- Owner net recorded effects, outstanding claims and unapplied settlement remain separate quantities.
  No mutable paid flag. No automatic advance, refund, equity or loan inference from differences.
- Immutable as-of control snapshots distinguish registered opening, prior-current and current movements.
  Opening completeness and source coverage remain unknown. Account controls compare the whole posted
  account to all registered owner effects, not only one owner's subset; zero difference is not proof
  of completeness. Preserve separate funding classes and exact minor-unit strings.
- Scoped saved-ID reads and same-actor idempotency-key receipt recovery. Browser capture must survive
  query refresh and warn that reload loses unsaved inputs/keys; do not imply automatic persistence.

## Risks and acceptance cases (documentation, not tests)

Before release, root must observe these through the real boundaries:

1. Wrong-book, revoked/expired token/session and removed membership deny reads/writes under admission locks.
2. Company nature cannot be changed to synthetic. Unknown facts/classification/origin/control account
   and missing synthetic tax declaration block accounting preparation/attachment/posting, not retention.
3. Agent credentials cannot classify-review or approve allocations. Current review/approval operator
   authority is checked for new transitions; leaving later does not erase historical posted effects.
4. Exact retries recover original results; changed actor/input/operation under one key conflicts.
   Same-actor recovery never reveals other-domain command receipts.
5. Duplicate source keys, evidence locators and posted line claims reject without partial persistence.
6. Review/plan digests bind immutable source, revision, chosen account and configuration. Changing a
   revision/account/profile or losing authority after preparation blocks posting/application atomically.
7. Existing posted references must match exact source occurrence, ledger amount, currency/scale and side.
   Wrong source, bank line, reversal, foreign currency, reused commerce/owner line and wrong account reject.
8. Reimbursements and loan repayments allocate only their compatible class and owner. Contributions
   remain separate. Different owners, source-before-claim timing, duplicate targets and over-allocation reject.
9. Concurrent allocation plans may inspect the same capacity; only fresh approved application succeeds.
   Deferred constraints bind receipt/legs and enforce both capacities. Failure leaves no partial receipt/leg.
10. Both posting-first and registration-first paths keep one economic event identity. Corrections of
    linked effects are blocked, including already-prepared reversal and paired-correction paths.
11. Snapshot cutoffs exclude later movements. Opening unknown is null/explicit, never silently zero.
    Later relevant records/effects/allocations invalidate freshness; unrelated future-period work does not.
12. Lists/history are bounded and page explicitly. UI exposes original evidence, exact reviewed digest,
    all selected allocation legs, unknown coverage, recovery keys and current server refusal reasons.

## Known prerequisites

Existing scoped book/membership, retained evidence, kernel plans/vouchers and0600 private helpers.
Current Better Auth and Drizzle Effect boundary are reused; no independent DB client or auth flow.
Real-company accounting remains blocked pending authoritative company/treatment/profile activation.
Root owns all shared composition and native validation. Exact integration maps follow implementation.


## Final handoff

Exact owned paths,18 REST/SQL operations,16 capabilities, fixed Drizzle dispatch entries and capability
bindings are in `apps/api/OWNER-REGISTER.md`. The source package is complete; all shared composition and
native validation remain root-owned. UI export: named `OwnerRegisterPanel`, existing `{book,locale}` props.
The migration0610 is new and unapplied. Existing0600 content remains unchanged in source comparison.
Operator review and allocation approval remain REST-only. The private closing hook requires a separate
root/year-end integration decision and forward change; existing0800 was not edited.

Final bounded formatting and Oxlint passed. No full type, database, browser, concurrency, recovery or
financial proof is claimed. The reported Effect4 `isBetween` signature issue is fixed in source.
The final static observation artifact is `.agents/work/owner-register-static.json`.
