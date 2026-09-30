# DF-04 — saved-request refusals preserve retry identity

Implemented and observed 2026-09-30 on the worktree based on `a2e4883`.
This closes the saved-request refusal defect for the existing synthetic posting
profile. It does not activate company accounting or change approval requirements.

## Root cause and repair

Two boundaries made every retained refusal absorbing: the saved-request runner
returned any prior outcome, and the shared kernel rejected reserved keys with a
historical refused outcome. The browser then offered a new key for the same body.

The runner now distinguishes request content from referenced state using the
existing pure `validatePostingLines` validator. A journal whose saved lines cannot
balance, have an invalid side or violate the pure line contract cannot succeed
with those bytes; its refusal remains terminal. Other business refusals are
conservatively nonabsorbing. `retryableRefusal` means the original identity may be
run again; it does not promise that a stale plan or unsupported profile can become
valid without new reviewed input. Failure-code names alone do not decide this.

Forward `0043-posting-request-attempts.sql` adds immutable attempt observations
under the existing saved body and kernel key. New attempts append; old
`posting_request_outcomes` rows are neither changed nor deleted. Reads prefer a
committed result, otherwise the latest attempt, falling back to old outcomes.
The admitted book update lock serializes attempts with the kernel writes, and a
partial unique index admits at most one new committed observation per request.
The runtime has only SELECT/INSERT on the new table. No stored feature workflow
or baseline migration change was added.

The kernel still rejects actor, operation and body substitutions. It no longer
uses a historical refusal as permission to reject the exact reserved command.
Current authority, dependencies, approval and economic-identity checks remain
with their existing owners. Unexpected infrastructure failures abort the whole
transaction instead of becoming durable business refusals.

The saved-work screen now explains state retry and runs the unchanged request.
Content-invalid requests require corrected input and cannot be rerun from that
screen. Unknown results also keep their identity. The separate explicit human
approval-renewal gesture remains available for a previously committed approval;
it is not a refusal retry or a new execution command.

## Observed proof

The pre-change HTTP reproduction passed the content-refusal case and failed both
state-refusal recovery cases: restoring reviewer authority and recovering a
legacy refusal both returned the same refusal permanently.

The delivered six E2E cases observe:

- Reviewer authority is removed after approval. The saved execution refuses with
  `ApprovalRequired` and posts nothing. Restoring authority and racing two runs of
  the same saved key produces one voucher and one identical committed outcome.
  Exactly two immutable attempt rows remain: refused, then committed.
- An unbalanced `12501` debit against `12500` credit remains terminal; repeating
  its run returns the same outcome. Changed bytes under the saved key refuse
  `IdempotencyConflict`.
- An injected failure while inserting the final attempt record rolls back the
  voucher, approval consumption and kernel receipt. Removing the injected fault
  lets the original saved request commit once under the same kernel key.
- A legacy immutable `PeriodLocked` outcome is recovered into a new committed
  attempt without changing its original state/message.
- An agent retries its own refused preparation through MCP after the period is
  reopened. The command key is unchanged and no voucher is created. Existing
  MCP authority tests still exclude human approval capabilities.
- Chromium signs in through Better Auth, opens retained work, inspects the refusal,
  reviews the exact body and activates **Run this saved request** with keyboard
  Enter. Only the original-key run endpoint is called; no new saved request is
  created. The current outcome becomes committed and no page errors are observed.
  Screenshots were inspected. No screen-reader or 200% zoom claim is made.

Final verification passed `check:changed:full`, `check:integration`, and the full
E2E suite: **182 tests across 46 files** on PostgreSQL 17.11, local workerd and the
restricted runtime role, with real Chromium for the browser journeys. Both the
DF-04 and NEXT-97 journeys passed in that run. The tested source inventory remained
stable at `ef5a6df60cb4d8df96408cae22df9f438fff70f959a2d8adaf7c868d7d0c6334`.
This identifies the tested source before the subsequent documentation update;
no implementation or test code changed after that run.

## Repeatable artifacts

```sh
bun run check:changed:full
bun run check:integration
bun run test:e2e apps/api/tests/saved-posting-retry.e2e.test.ts apps/api/tests/posting.e2e.test.ts apps/api/tests/mcp-authority.e2e.test.ts apps/api/tests/persistence.e2e.test.ts
```

`test-results/e2e` retains `manifest.json`, `source-integrity.json`, `results.json`,
`junit.xml`, `df-04-same-key-retry.json`, `df-04-mcp-retry.json`,
`df-04-browser.json`, retry/committed screenshots and the browser server log.
`bun run test:e2e` reproduces the broader regression run. The harness uses only
synthetic fixtures and disposable systems and archives earlier evidence under
`test-results/e2e-history`.
