# NEXT-97 — bounded exact bank covers

Observed 2026-09-30 on the worktree based on `3d51dd6`. This is local synthetic
integration and browser evidence, not provider or actual-company qualification.

## Delivered path

`bank_discover_match_candidates` and `POST …/bank-match-candidates` compose
`@open-erp/domain/bank-cover-search` inside the existing bank candidate owner's
book-locked read transaction. Amounts, remaining capacities, dates, account and
currency eligibility come from retained statement and journal rows. Discovery
creates no journal, allocation, reservation or receipt.

The Accounts matching sheet shows exact grouped alternatives and their scope.
Choosing a group pre-fills its whole residual legs in the existing allocation
review form. The operator supplies a reason, reviews the evidence, prepares,
approves and executes through the existing bank allocation owner. This preserves
its capacity recapture, approval, atomic execution and original-key recovery.
There is no second allocation writer and no migration.

## Search contract and limits

- Same-account, same-currency, same-sign, eligible whole residuals only. Fees,
  opposite-sign decomposition, conversion and partial-subleg search are excluded.
- The declared pool is the retained statement's date interval at the captured
  ledger cutoff, not the entire book. Existing candidate admission refuses an
  interval exceeding 1,000 journal lines.
- Defaults and maximum configurable bounds: 40 candidates, four lines per set,
  10,000 visited search states. Search explores the first successful cardinality
  completely, ranks by smallest maximum day gap and retains every equally ranked
  explanation. Stable IDs determine output order, never economic preference.
- Candidate truncation, visit-budget exhaustion or more than 100 equal-ranked
  alternatives produces `incomplete_search`, with observed alternatives retained.
  A complete empty search means no match **within the declared bounds**.
- Conflict analysis searches at most ten other observations in the same retained
  statement. It reports their full population count and shared ledger identities.
  Truncated peers or an incomplete cover search mark the conflict check incomplete.
  Other statements are outside this conflict scope; uniqueness is never a promise
  that another observation cannot compete for capacity.

The wire `coverLimits` permits an explicit smaller budget. The current UI uses
the default limits and does not expose budget controls. It displays incomplete
search and conflict states and keeps manual selection available.

## Independent observations

The focused E2E run passed five tests across `bank-covers.e2e.test.ts` and the
existing `bank-references.e2e.test.ts`, using real workerd, disposable PostgreSQL
and the restricted runtime role. Source inventory remained stable throughout:
`c62ece3795791d123cbd49f308d188f3dc8dc8872c53fe72bdfc0729459abbd4`.

1. Target `100`, candidates `70`, `30`, `60`, `40`, equal dates: exactly two
   equally ranked two-line covers, each totaling `100` with zero leftover.
   Discovery leaves retained posting/receipt state unchanged.
2. Smaller visit and candidate budgets produce `incomplete_search`; they never
   report an observed first cover as unique. Target `101` has no exact cover.
3. Two statement rows targeting `100` disclose shared ledger capacity. The first
   reviewed `70 + 30` allocation executes and same-key recovery returns its receipt.
   A pre-approved competing allocation then refuses `StaleDependency`. Fresh
   discovery finds the unused `60 + 40` cover; a second reviewed allocation executes
   and its original-key recovery returns the same second receipt.
4. The agent receives the same read-only cover search; discovery grants no approval
   or execution authority. Out-of-range search limits fail request validation.
5. Chromium signs in through Better Auth, renders both alternatives, activates a
   group with keyboard Enter, then prepares, approves and confirms it using the
   real controls. The retained bank residual is `0` afterwards. Desktop 1440×900
   and narrow 390×844 screenshots were inspected; the narrow document has no
   horizontal overflow and no page errors were observed. This does not claim
   screen-reader or 200% browser-zoom qualification.

## Repeatable proof

```sh
bun install --frozen-lockfile
bun run check:changed:full
bun run check:integration
bun run test:e2e apps/api/tests/bank-covers.e2e.test.ts apps/api/tests/bank-references.e2e.test.ts
```

The harness retains `test-results/e2e/results.json`, `junit.xml`,
`source-integrity.json`, `next-97-cover-discovery.json`,
`next-97-cover-allocation.json`, `next-97-browser.json` and desktop/narrow/saved
screenshots. Subsequent runs archive earlier results under `test-results/e2e-history`.
The domain manifest adds only an export; dependency resolution and `bun.lock`
remain unchanged, and the frozen install passed.
