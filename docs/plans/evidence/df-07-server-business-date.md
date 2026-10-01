# DF-07 — Server-owned Stockholm business date

Implemented and observed 2026-10-01 using synthetic sources, disposable PostgreSQL,
normal workerd REST/MCP, the real web application and the Effect setup owner.

## Reproduction and scope reconciliation

The dated register's claim that no Stockholm conversion existed was stale. The
shared platform formatter and backend book-status admission already used it.
However, `useBusinessDate` still read the browser clock, setup had no business
date, and bank/company-admission defaults still used UTC or the last period.

Before production edits, the public setup-date vector failed for its missing
`today` field. The application-owner cases, with an injected Effect clock and
real restricted-role PostgreSQL, failed for the same absent field. The real
browser vector independently failed: with its clock set to `2026-01-01`, the
overview requested that day rather than the server's `2026-10-01`.

## Delivered owner and consumers

`posting.bookSetup` obtains `DateTime.now` through Effect's replaceable Clock and
uses the existing `swedishBusinessDate` platform formatter. Shared `BookSetup.today`
is required response metadata, served by the existing REST and MCP capability.
It is not a sealed historical accounting record or a client-supplied financial
amount/date. No public time-control option or new timezone dependency exists.

The existing request-scoped TanStack setup query owns frontend refresh: every
60 seconds while active and on focus. `useBusinessDate` reads that shared server
basis rather than scheduling another browser clock. Existing authority/error
handling remains in `BookWorkspace`. Overview, readiness, bank defaults, company
admission and cancellation defaults consume server dates. Bank navigation prefetch
and the visible workspace reuse the same parameter owner; explicit date filters
are not overwritten. A cancellation input remains editable and its real operation
still supplies an explicit posting date.

Plain-date addition, distances and fiscal-period arithmetic remain UTC. The DB's
credential/approval expiry and transaction clock are not replaced by the injected
application clock. FX operations retain explicit supplied dates rather than an
invented implicit exchange-rate date.

## Repeatable acceptance

```sh
bun run test:e2e apps/api/tests/setup-business-date.e2e.test.ts apps/api/tests/business-date.e2e.test.ts apps/api/tests/mcp.e2e.test.ts
bun run check:changed:full
bun run check:integration
python3 docs/plans/check-plan.py
```

Observed: nine E2E cases pass across three files. HTTP setup agrees with independent
PostgreSQL Stockholm wall time; MCP's setup date agrees with HTTP. Six fixed
instant vectors exercise the real setup application with real restricted-role DB
reads: winter midnight just before/after year rollover, late winter/summer instants
and both DST transition dates. Their expected dates were specified before edits.

Chromium runs in `America/Los_Angeles` with a clock deliberately set to January
while the server is in October. Overview requests keep the server day. Advancing
browser timers produces a new shared setup read; changing browser wall time,
focus and visibility never supplies a different date. The bank workspace chooses
the actual server-containing `2026` period rather than the last `2027` fixture
period. An explicit March interval remains exact. Company-admission requests use
the server day. Supplier paging/search still finds the 201st synthetic draft at
390px width. Browser errors remain empty.

`test-results/e2e` retains `df-07-setup-date.json`, date-named injected-clock
vectors, `business-date-browser.json`, `server-business-date-desktop.png`,
`supplier-search-mobile.png`, suite JSON/JUnit and source integrity. Repeated runs
archive prior artifacts under `test-results/e2e-history`.

## Limits

The browser does not control the API or PostgreSQL clock. An actual live server
midnight is not awaited by the browser test; boundary vectors exercise the owning
application with an injected clock instead. A failed refresh retains the last
observed setup alongside the existing error surface, not a fabricated client day.
No actual-company readiness, rate-feed qualification or statutory outcome is
claimed. The earlier full-suite DF-11 result is not promoted to this revision.
