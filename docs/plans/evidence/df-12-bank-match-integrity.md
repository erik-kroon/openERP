# DF-12 — Retained bank-match account and direction

Observed 2026-10-01 through the normal local workerd HTTP application and disposable
PostgreSQL, using synthetic sources and reviewed synthetic postings only.

## Scope and reproduction

`application/banking/matches.ts` already checks the statement settlement account,
exact signed amount and statement interval before inserting a whole-row match.
Both explicit match commands and imported existing matches use that owner. Partial
consumption uses reviewed allocation plans, not relaxed exact matches.

The missing guarantee was below application admission. Before production changes,
`bank-match-integrity.e2e.test.ts` failed in both cases: a synthetic before-insert
fault redirected an otherwise valid match to a same-sign line on another account,
or to an opposite-sign bank line on a second voucher. The public command returned
HTTP 200 instead of the independently expected `InvalidJournal` refusal.

## Repair and consumers

`0045-bank-match-integrity.sql` adds an after-insert check of the final retained
match against the referenced immutable observation, statement account and journal
line. It uses exact PostgreSQL numeric sign comparisons and the book lock, with
a fixed search path and no public helper execution grant. Existing inconsistent
matches fail migration preflight; no retained record is rewritten.

The guard compares direction, never magnitude. The Effect application still owns
exact matching, approval, capacity, retries and transaction-passing persistence.
REST/MCP/UI consumers retain their existing shared application owner and error
contract; every match insert reaches the guarded table. Reviewed allocations are
not bank matches and keep their independent partial-capacity contract.

## Repeatable acceptance

```sh
bun run test:e2e apps/api/tests/bank-match-integrity.e2e.test.ts apps/api/tests/bank-references.e2e.test.ts apps/api/tests/assurance/bank-capacity.e2e.test.ts apps/api/tests/persistence.e2e.test.ts
bun run check:changed:full
python3 docs/plans/check-plan.py
```

The wrong-account case preserves the observed sign, and the wrong-sign case
preserves the settlement account, so neither check can hide behind the other.
Both final-write faults now produce HTTP 422 / `InvalidJournal`. No match,
command receipt, source revision or financial count is committed. Removing the
fault lets the original request key recover one correct match; an exact retry
returns the same receipt and the stored target agrees with it.

The focused run passes thirteen tests across four files, including reference
ranking and concurrent exact-match replay, partial allocation residuals and
rollback, restricted-role persistence, and migration rerun/checksum refusal.
Artifacts: `test-results/e2e/df-12-wrong_account.json`,
`df-12-opposite_sign.json`, suite JSON/JUnit, migration logs and source inventory.

## Limits

This is local synthetic relational-integrity evidence. It does not establish
company acceptance, foreign-currency equivalence, a payment action or an expanded
partial-match API. Migration preflight against a separately manufactured corrupt
historical installation and privileged concurrent maintenance are not separately
exercised. The prior full-suite DF-11 result belongs to that earlier revision;
the DF-12 claim uses its focused banking and persistence checks.
