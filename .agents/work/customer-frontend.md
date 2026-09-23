# Customer frontend implementation

Goal: implement `docs/frontend.md` and ADR 0006, preserving all six delivery slices and their acceptance requirements.

Started 2026-09-22 in the shared `/Users/admin/openERP` worktree. Existing dirty API/domain/infra changes belong to concurrent work and must be preserved. Frontend planning documents from this task are already present.

## Current slice

FE-01: scoped workspace navigation, existing preparation/review/posting/recovery, immutable review links, company isolation and responsive shared primitives.

## Remaining scope

- FE-02 authoritative work projections, queue filters and founder Overview.
- FE-03 documents, banking, sales/purchase registers and source-led review.
- FE-04 books, corrections, schedules, report lineage and period readiness.
- FE-05 persisted preferences, team work and authorized firm/client views.
- FE-06 integrated runtime/browser evidence and removal of the superseded composition.

## Verification and authority

The existing browser E2E targets an obsolete access-token login. Requested explicit authorization for E2E changes, required by AGENTS.md, via the pending question. No tests have been changed. Actual production membership and company/provider facts remain the existing D-gates; synthetic implementation and proof can proceed.

Source observations: home currently selects a book in local component state; the workspace mounts all domain sections; recovery detail checks book scope and retains command identities; plan version is currently literal 1 and its digest identifies immutable content. Use the digest for a review revision link.

No implementation completion claim yet. The first goal turn is in progress; the preceding planning turn produced the plan and ADR.

## FE-02 failure cases before implementation

- A different entity/book or continuation must not expose items, counts or identities.
- Counts must use the same scoped period/search observation as rows, before page truncation; status facets deliberately ignore the selected status and are labelled accordingly.
- Pending means unposted at the observation, not approved or safe to execute. Another proposal's posting is completed with a distinct state.
- Cursor ties use created time and ID; changing filters clears the cursor. New page observations may have newer counts and disclose their checked time/sequence.
- Amounts sum exact minor-unit strings; no browser number conversion or mixed-currency total.
- Unsupported/incomplete domain coverage stays explicit, including an empty result.
- Invalid periods/search/status/sort and cross-scope cursors fail before returning a success-shaped empty page.
- Mutation authority stays in original operations. Reading a queue cannot approve or execute.

FE-01 current evidence: web build including prerender succeeds after an explicit IPv4 loopback preview binding. Web/UI type checks and lint were run during development; the most recent web type check passes. Runtime/browser verification remains pending. No test changes yet.

## Journal usability pass

User rejected the old technical form inside the new frame. The real journal path now gets a compact company header, light default, constrained surfaces, labelled source/entry/review steps and progressive disclosure for record identities. Verification remains in progress.

Before decimal input changes, failure cases: unknown currency scale disables preparation; decimal parsing uses exact integer arithmetic; reject grouping, signs, exponents and excess precision; blank amount means zero only on a journal side; never infer SEK scale for another currency; validation still requires balanced nonzero lines; remove-line updates totals; retries preserve the original saved operation identity.

## Latest outcome

User correction after reviewing status: the implemented journal is still far from a good customer-facing experience. Treat it as functional technical groundwork, not an accepted customer journey. The earlier 20–25% estimate was an implementation-coverage judgement and overstated customer readiness. No customer journey is accepted. `docs/frontend.md` now records the concrete workflow gap; the paused implementation goal has not been resumed by this assessment.

The actual source → decimal journal → immutable review → approval → posting → reloaded receipt flow now works in the isolated synthetic runtime. UI uses a light default, compact company context, linked section tabs, source/entry/review steps, grouped form surfaces, compact account rows with live exact totals, side-by-side source and effects, and disclosed technical history. Work filters survive review navigation. See `customer-frontend-proof/journal-flow.md` for identities, receipts, commands and gaps.

No full frontend completion claim. FE-01 has its first full successful posting journey; denial/race/recovery and broad accessibility/theme checks remain. FE-02 has the authoritative journal projection and working filtered queue, while the founder overview remains basic. FE-03 through FE-06 remain. More tools still exposes the old composition and is not the intended final customer interface.

Additional integration repair: two new VAT SelectField consumers used unsupported `onChange`; changed only those callbacks to the existing `onValueChange` contract. Other concurrent domain work is preserved. Full web/UI lint currently fails in other newly added VAT/invoice files; focused checks and web/UI types pass, and the production build passes.

## Company workspace implementation

The company frame, grouped navigation, task home, voucher register and journal modal use the existing stack and OpenERP's palette/fonts. The current working decision and route coverage are recorded in docs/frontend.md and ADR 0006. The verified scope covers the journal-to-review flow and narrow layouts; the older domain forms still need customer-facing workflow work.

The isolated preview remains on web 3106 / worker 18789 / PG 63180. It preserves the original A1 voucher and one newly prepared, unapproved 10.00 SEK proposal. New invoice drafts/VAT pages were not promoted into the new navigation because migration 0940's checksum mismatch correctly blocks the old preview schema's upgrade. Do not rewrite the receipt or weaken the migrator. The shared backend restructure and commit happened concurrently; preserve those changes. No tests were added or modified, and this task did not create a commit or deploy.
