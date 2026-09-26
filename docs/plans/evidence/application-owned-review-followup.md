# Application-owned replacement: follow-up review

2026-09-26. Review and repair of the work following the [first repair pass](application-owned-review-repairs.md). This is local evidence for specific paths, not acceptance of the complete replacement. The checkout was dirty and changed concurrently during this pass; file hashes accompany the local artifacts.

## Repairs

- Report, register, case and recurring-rule permission checks now request INSERT only for the records they create. The runtime can create company books and memberships, but cannot insert accounts or periods merely to satisfy report probes.
- Company creation returns the retained revision; partial company details accept explicit unknown values. Firm creation replays its original result. Firm accountants with book operator authority can update existing client engagements.
- Owner reviews and allocation approvals have native application implementations. Source revisions retain one digest over the intended source/revision pair. The previous double hash made their posting guards reject valid sources.
- Carrying-basis registration validates the schedule digest, retained evidence, posted voucher, exact selected lines, amount conservation and duplicate claims before writing the basis and command receipt in one transaction.
- SIE source capture, preview history, plan sealing and fenced staging runs have native implementations and scoped grants. Independent opening/closing and open-item controls use exact integer arithmetic. Staging supports bounded chunks, pause/resume, stale-fence rejection and receipt replay. Financial import remains a separate unfinished workflow.
- HTTP handlers pass only entity/book identifiers as scope. Resource path identifiers no longer enter sealed scope objects and disappear during later schema decoding.
- JSON identity comparisons use canonical values, preserving array order while ignoring object property order. This fixes retention-upload metadata, invoice currentness and document retry checks against PostgreSQL JSONB.
- Invoice draft validation accepts omitted catalog selections. Issue reviews retain the full evidence contract. Approval expiry queries correctly apply the timezone conversion to the timestamp plus interval.
- Mutations in the reviewed commerce, correction, dimension and exchange-rate ports request a book write lock at admission instead of upgrading a shared lock. Known stale dependency failures make legal review currentness false rather than true; unexpected failures propagate.
- Register snapshots compare the voucher identifier with the referenced row's identifier. Whole-book case snapshots accept the omitted optional case filter.
- Accountant-review captures use the new application dependency providers and owner/expense calculations in the caller's transaction. Balance validation includes zero-balance accounts without journal entries.

## Observed journeys

All supplemental checks used a disposable PostgreSQL database, a real workerd Worker and a login granted `openerp_runtime`. Synthetic fixture setup used separate administrative access. No test files were added or changed.

Final checks passed: full typechecking, lint, the API dry-run build, and all 23 existing E2E tests across four files against a fresh database. Source hashes did not change during those final checks. The manual Worker/database were closed and their scratch directory removed.

| Journey | Observed result |
| --- | --- |
| Company and firm | Company revision 1, partial update to revision 2, exact replay and stale-write rejection; firm creation replay and accountant client update succeeded. |
| Owner claim and settlement | Reviewed and posted a 1,000-minor-unit claim and settlement, approved/applied their allocation, and observed zero claim remainder. Agent review/approval and stale requests were refused. |
| Carrying basis | Retained a 10,000-minor-unit acquisition basis for a two-occurrence schedule. Agent, mismatched amount and duplicate basis attempts were refused; exact replay returned the saved basis. |
| SIE retention and staging | Used local R2 retention. A valid source passed independent control checks; wrong controls and agent sealing were refused. Pause/resume advanced the fence; an old fence failed. A 201-voucher source staged in chunks of 200 and 1, retaining exactly 201 vouchers. Concurrent identical chunk requests returned one result. |
| Invoice | Created a manual draft, prepared and approved issuance, posted it and generated a sealed HTML review document. Same-key and new-key document recovery returned the same capture; conflicting reuse was refused. |
| Concurrent invoice | Four simultaneous calls at each of prepare, approve and execute returned one review, one approval and one invoice numbered `SYN-2`. Agent approval was refused. |
| Reports and review | Trial balance, register and whole-book case snapshots succeeded without account INSERT permission. Accountant review retained eight balances, ten journal lines, owner controls and eight export formats. Readback reported current dependencies and replay returned the same pack. |
| Independent ledger observation | Five vouchers and five execution receipts; committed sequence 5; aggregate debit minus credit 0. SIE staging created no financial vouchers. |

Artifacts are in `test-results/replacement-completion/`: exact HTTP inputs/results, sanitized runtime logs, fixture configuration, independent database observations, the exported accountant JSON artifact, check logs, the existing E2E artifacts, cleanup results and source hashes. Failed diagnostic attempts remain in the HTTP log; the table above describes successful final observations, not every recorded request.

## Repeat the checks

1. Run `bun run check-types`, `bun run lint`, `bun run --cwd apps/api build` and `bun run test:e2e`. The existing suite owns its database and writes repeatable results to `test-results/e2e/`.
2. For the supplemental journeys, use the existing E2E global setup to create a separate disposable database and Worker. Provision `fixture.json` with `apps/api/scripts/provision.ts`; create fresh operator/agent credentials and a provisioned human session. Supply a local R2 `EVIDENCE_BUCKET` binding for source upload. Never use an existing company database.
3. Follow the recorded HTTP requests with fresh returned identifiers and the synthetic values above. `manual-http.ndjson` records path, input, idempotency key, status and response without authentication secrets. Replay the identical key/input and submit parallel copies at each concurrent step.
4. Compare the resulting ledger, staged-voucher counts and grants with `manual-outcomes.json`. Verify accountant-export hashes against their descriptors. Close the Worker and remove the owned scratch database after collection.

The supplemental journey record is not a newly added automated regression suite. The existing E2E suite does not establish browser, full supplier/AP, historical migration or actual-company acceptance.

## Open replacement gates

There are still 28 unconditional placeholders: 16 historical-import operations, ten impairment/disposal operations and two schedule amendments. Their exact names are listed in `remaining-placeholders.json` beside the artifacts. The old feature-function dispatch registry is gone, but the migration chain, remaining function grants, SQL policy triggers and SQL-backed helpers/providers are not the clean baseline promised by ADR 0010. Complete these ports and the database-boundary review before claiming the replacement finished. Release-pinned browser, failure/concurrency and restore qualification also remain open.
