# DF-10A — machine-readable outer Worker failures

Implemented and observed 2026-10-01. This is the outer-boundary slice of DF-10,
not completion of its domain-wide recovery taxonomy or remedy-code split.

## Reproduction and repair

A duplicate-key JSON request reached the real Worker's pre-routing body guard
and returned HTTP 400 with only `{ message }`. The same outer response helper
discarded the stable accounting code on unexpected failures.

The body guard now exposes stable `InvalidRequest`, `RequestTooLarge` and
`RequestTimeout` codes. Its outer responses preserve the existing status/message
and identify recovery as `permanent` for unchanged malformed/oversized bodies or
`transient` for a pre-routing timeout. These requests have not reached a workflow;
this classification does not imply that an interrupted financial command is safe
to repeat under a new key. Unexpected accounting failures retain the existing
tagged accounting error and status instead of being reduced to prose.

Only the owned `BodyError` receives this treatment. Arbitrary thrown objects
with `status` and `message` no longer qualify as safe public errors. Existing
request correlation, safe diagnostics and infrastructure classification remain.

## Observed proof and limits

The unchanged failing duplicate-key vector passes after repair. An oversized
body also returns `413 RequestTooLarge`; neither reflects private input, and
both retain a generated request ID. The boundary and existing diagnostics
suites pass five real Worker E2E cases, including safe schema/database/connection
failures. `test-results/e2e/df-10-boundary-failures.json` retains the responses.
The timeout code follows the existing 15-second timeout branch; a timed-stream
runtime test is not claimed here.

The full changed-file gate subsequently passed against base `88b49d0`, including
the committed implementation and test. Its first attempt was blocked by spacing
in a separately owned concurrent DF-08 test; that work was not altered to obtain
a green result.

```sh
bun run check:changed:full
bun run test:e2e apps/api/tests/boundary-failures.e2e.test.ts apps/api/tests/diagnostics.e2e.test.ts
```

Remaining DF-10 work: shared domain recovery semantics, compatibility of sealed
error records, consumer behavior, and remedy-specific accounting codes. A stable
HTTP status alone must not stand in for those contracts.
