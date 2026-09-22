# OpenERP end-to-end execution

## Accepted outcome
Implement and verify the system in `docs/plans/README.md`. A prerequisite or synthetic demonstration is not whole-product completion. No production write, deployment, filing, or external spend is authorized by this implementation request.

## Baseline
- Initial working tree: untracked `docs/` supplied by the user; preserve it.
- Existing runtime: Bun, Effect `4.0.0-rc.112`, TanStack Start/Query, Cloudflare Workers, StyleX.
- Existing product: public health/status endpoints and a connection screen. No accounting persistence or accounting workflows.
- Keep `apps/api` as Core owner rather than rename it to the proposed `apps/core-worker`.
- Retain the deliberate Effect 4 baseline. Do not mix Effect 3 adapters.
- Local PostgreSQL tools are installed. A dedicated disposable test database must be isolated from any existing data.

## Sequence and observable exits
1. Runtime/source baseline: source provenance, version/ownership decisions, real Worker-to-PostgreSQL transaction with rollback and cleanup.
2. Accounting kernel: exact amounts, sealed proposals, approval, atomic posting/receipt/outbox, correction, equivalent REST/MCP/direct results; concurrency and retry proof.
3. Complete synthetic period: preserved evidence matches, case context, posting, bank reconciliation, ledger report drilldown with no unexplained differences.
4. Durable automation: rule simulation, conflicts, bounded approvals and recoverable delivery.
5. Swedish profile modules: reviewed dated rules; VAT, tax account and required subledgers, each independently reconciled.
6. Year-end outputs: close, tax, annual report, SIE/iXBRL with provenance and independent validators.
7. Production readiness: actual company facts, migration source, archive/restore and provider gates. Deployment and cutover need separate authorization.
8. Hosted expansion only after the internal profile passes its gates.

## Current blockers and next action
- User requested implementation without new tests. No tests added. Static checks and manual development receipts are not the adversarial evidence required to pass all design gates.
- Actual company profile, historical data, reviewed dated legal rules and authority/provider access are missing. Unsupported profiles and production claims remain blocked.
- G1 is implemented and manually exercised locally. G2 bank import/matches/reconciliation and immutable trial balance/drilldown are implemented and manually exercised. Case context and the expanded UI are being integrated.
- Root owns integration and report module. `accounting-api` owns new0110 case contexts; `accounting-ui` owns bank/report UI; `bank-reconciliation` owns new0200 recurring preparation (not auto-posting).

## Decision trail
| Unit | Decision | Reason | Evidence | Status |
| --- | --- | --- | --- | --- |
| Runtime | Keep Effect 4 and `apps/api` | Intentional checkout contract overrides proposed layout/default | `AGENTS.md`, `README.md`, package manifests | Baseline inspected |
| Verification | Request explicit E2E test approval before implementation | Repository forbids unapproved test additions | `AGENTS.md` | Awaiting user |

| Runtime proof | Use isolated API port 18788 and inspector 19239 | Default launch failed with address in use; leave other processes alone | `.agents/work/openerp-baseline/worker.txt` | Health/status/OpenAPI observed in local workerd; owned Worker stopped |
| Static baseline | Existing lint, types, build and formatting pass | Establish starting state before implementation | `.agents/work/openerp-baseline/` | Passed; no accounting behavior proved |

## Repeat the existing API observation

From `apps/api`, run `bun x wrangler dev --local --port 18788 --inspector-port 19239`. Wait for the ready message. From another terminal call `curl -i http://127.0.0.1:18788/api/health`, `curl -i http://127.0.0.1:18788/api/v1/system`, and `curl http://127.0.0.1:18788/api/openapi.json`. Observed health/status HTTP 200 with `Cache-Control: no-store`; OpenAPI describes the two existing operations. Stop the owned dev process afterward. No new test or test helper was added.

PostgreSQL CLI reports version 17.11. No database was created or modified. Worker-to-PostgreSQL transaction proof remains unimplemented and unverified, pending approved tests.

The maintained specification starts at `docs/README.md`; domain delivery contracts are in `docs/plans/README.md`.

## Implementation phase (supersedes test-approval blocker)

User explicitly requested “skip tests and focus on impl”, then asked to use available depth. No tests added. Existing static checks and manual local development execution are permitted; no automated correctness/concurrency claims.

- Root owns shared accounting schema, PostgreSQL kernel, migration/provision commands, root manifests, infra and integration.
- `accounting-api` child implemented REST/MCP/session and is now read-only reviewing kernel safety.
- `accounting-ui` child implemented posting/review screen and is adding original evidence inspection and correction preparation.
- `bank-reconciliation` child owns new reconciliation contracts, module and migration0100; integrate shared dispatcher/group/manifest after completion.
- Maintained design and delivery contracts live at `docs/plans/README.md`.

### Current behavior and evidence

Migrations0001..0005 applied to isolated development PostgreSQL17.11. Maintenance role owns schema; runtime login inherits only openerp_runtime. Existing API posted synthetic manual journal, retrieved execution receipt, prepared/approved/executed exact linked reversal, and read ledger sequence2 with both sides12500 and net0 per account. MCP initialize succeeded via same Worker. Receipt artifact: `.agents/work/openerp-implementation/manual-development-receipts.json`. This is manual development use, not adversarial proof or compliance evidence.

Initial real-runtime failures corrected with forward migrations: SQL action-variable ambiguity, deferred balance trigger requiring SECURITY DEFINER after transaction function exits, ledger watermark variable binding, reversal action argument binding. No acknowledged postings were removed. Proposal request timed out during hot reload but retry with same key recovered it.

### Owned local resources (private, ignored)

- PostgreSQL data `.cache/openerp-development/data`, host127.0.0.1 port55472; owner openerp_maintenance; database openerp_development.
- Maintenance password `.cache/openerp-development/maintenance-password`; operator token `.cache/openerp-development/operator-token`, mode0600. Never print these.
- Runtime URL in `apps/api/.dev.vars` created by root, mode0600, ignored.
- Root Worker port19788 inspector20239. Port18788 was owned by another external process pointed at PG15439; do not stop or reuse it.
- Stop only root-owned Worker handle and `pg_ctl -D .cache/openerp-development/data stop` when no longer needed. Development data retained for user.

### Next actions

Finish G1 integration: review child MCP/UI, run root existing lint/types/build/format, recover evidence and correction UI. Await kernel read-only findings; fix concrete issues in forward migrations. Integrate G2 child after core is stable. No deployment, commit, production data or authority action authorized.

### G2 integration checkpoint

Applied0006 (global default PUBLIC function EXECUTE revoke),0100 bank reconciliation,0120 internal trial balance. Existing migrations are immutable. Separate case migration0110 is still being prepared; numeric ordering is not used as a substitute for explicit dependency review.

Manual account/year2026 synthetic bank import preserved both original and reversal rows and supplied existing matches. Reconciliation reports zero opening/closing differences, no unmatched rows/lines and complete declared source coverage for that one synthetic bank source. This is not whole-company readiness. Trial balance pins sequence2 and exposes both posted vouchers/evidence through contribution drilldown. MCP bank_get_reconciliation succeeded through the same capability handler. Artifact: `.agents/work/openerp-implementation/manual-period-receipts.json`.

Latest complete static lint passed. Root types currently blocked by in-flight cases schema isBetween argument; assigned owner to fix. Earlier G1 full root types/build passed. Expanded code checks will be rerun after integration. No tests, commits, deploys, filings or real-company data touched.

### Case contexts and recurring-preparation handoff

Case REST/MCP adapters now share named handlers. Applied0110 and forward0111; manual snapshot/list/evidence/history continuation succeeded with1 reversed case,2 posted plans and full gross turnover25000 per side. Artifact `.agents/work/openerp-implementation/manual-case-context-receipts.json`. Applied0130 readiness endpoint, available via REST /status and MCP book_get_status. Applied0101 bounds synchronous bank report to1000 combined rows/100 statements without partial results; local accepted source still reconciles complete.

Case module source review revealed another invalid function-qualified unlabeled local; fixed captured_snapshot_id in0111, not applied0110. Root has scheduled a narrow local harness lesson. Migration CLI now accepts an optional exact last-reviewed filename, currently0130-book-readiness.sql, to avoid applying in-progress0200.

`accounting-api` has released case files and researches official dated Swedish VAT/skattekonto prerequisites into source manifest + ADR only; must not enable production. `accounting-ui` completed bank and trial-balance screens and now adds case/readiness panels. `bank-reconciliation` owns in-progress0200 recurring preparation, not applied yet. No other files shared with these tasks.

Root prepared a second local synthetic entity/book for recurring development: entity_automation/book_automation with actor_automation, same scoped account/period IDs as original example. Private `.cache/openerp-development/automation-operator-token`, config `.cache/openerp-development/automation-book.json`; do not print token. Runtime same Worker19788/PG55472. Retained and imported two distinct identical positive1000 bank rows, no matches, source total2000. Original synthetic journal/reversal period remains untouched. Python automation_http/base/input/response variables hold this development session. Next root action: integrate released0200 contracts/handlers via common capabilities, apply migration, manually prepare/simulate/operator-activate/resume proposals and record receipts without tests; every posting still needs normal approval.

### Swedish source research boundary

Research-only `docs/sources/sweden-vat-sources.json` and `docs/adr/0002-swedish-vat-profile-boundary.md` now record10 official sources,24 short excerpt/hash records and2 explicitly failed legal-guidance accesses. No active Swedish profile, effective-date approval, rounding algorithm or authority submission is established. Narrow domestic25% faktureringsmetoden preparation can be designed; production remains blocked by company/transaction facts, clause-version applicability, rounding/aggregation, coverage and qualified review. Tax-account transfer and assessment remain distinct. `accounting-api` is retained without further implementation assignment. Root will not enable a real-company tax profile from research alone.

### Recurring preparation integrated and manually observed

0200 applied after a pre-application syntax fix renamed reserved OVERLAPS local to rule_conflicts; no applied checksum was changed. Forward0201 rejects extra fields on all recurring mutators and checks effective activation membership in reads. All REST mutation payload schemas now reject excess fields as MCP already did. Forward0210 serializes scoped admitted credentials/memberships against revocation using shared row locks; admission-time expiry uses clock_timestamp. It also prevents changing book entity/currency/scale. Revocation maintenance must not acquire book/config locks; see README. No concurrent-revocation verification was run. Forward0211 adds recurring preparation to readiness.

REST and MCP now share all ordinary recurring capability handlers; operator-only activation/deactivation remain outside MCP. Manual rule proposal→simulation of2 equal positive1000 rows→operator activation→run→one-row chunk→cancel→resume succeeded. Both identities yielded distinct sealed events/proposals; ledger remained sequence0 with zero balances. Those proposals are deliberately unapproved/unposted for the user to inspect. Artifact `.agents/work/openerp-implementation/manual-recurring-preparation-receipts.json`. All database migrations through0211 applied to the owned local DB.

Case/readiness UI and report UI are complete with child static checks passing. Recurring UI is in progress with accounting-ui. Backend reviewers are retained, no outstanding review assignment. Root full lint/types/format checks are running; final API dry-run build and diff check follow. No tests, deployment, submission, production accounting, commits or pushes.

Remaining target work is not disguised as done: no automatic posting delegation budgets, external outbox relay/scheduler, Swedish compliance profile, real-company tax/subledger/year-end module, SIE/iXBRL output, external archive/restore proof, migration/cutover or hosted production gate. Actual company facts determine required next modules. Research ADR0002 identifies additional legal applicability/rounding/qualified-review blockers. Goal stays active and must not be marked complete from this synthetic slice.

### Latest checked implementation checkpoint

All assigned UI work is released: bank, trial-balance, case/readiness and recurring preparation are connected. Root final `bun run check-types` (including web build/prerender and infra types), `bun run lint`, `bun run format:check`, API Wrangler dry-run build and `git diff --check` pass. Repeatable command outputs and source hashes: `.agents/work/openerp-implementation/implementation-checks.json`. Browser behavior, concurrency/crash paths and compliance are not verified; no new tests were authorized or written.

Workers are retained with no outstanding assignments. Full-system goal is NOT achieved. Next real-company implementation scope requires explicit entity/accounting-method/VAT-period and required subledger facts, alongside unresolved legal rounding/applicability review. Synthetic local resources and both unapproved recurring proposals remain available; private credentials stay in ignored0600 files. No commit, push or deployment was performed.

## New user-authorized domain-parallel phase

User requested one subagent per each of seven listed areas. Ownership now follows `.agents/work/domain-ownership.md`. Three retained sessions were reassigned by domain and four domain sessions started, for exactly seven owners. Prior statements that all workers were idle no longer apply. Root retains shared composition and serial validation. No tests/deploy/production action newly authorized. Current code includes bounded synthetic imports/matching/reconciliation and recurring preparation; broader formats, allocations and complete failure proof remain incomplete.

### Seven-domain integration: first released slices

Posting/recovery0300 now applied and immutable; REST/MCP share three read-only recovery capabilities. Manual original-book lists/details/history recover committed receipts; absent key reports not_observed; recurring book lists two unposted proposals. Artifact manual-posting-recovery-receipts.json. Recovery UI mounted; durable browser keys cover approve/execute but shared draft keys remain mounted-only, with server proposal discovery for committed drafts. No failure/crash/concurrency/browser proof claimed.

Local-only operations CLI/tooling released. Root operations TypeScript check passes; parent script configuration includes it. Source review fixed broad pg_% wildcard exclusions and Effect tagged error/typed-decoder diagnostics. No operational backup/restore executed; no production readiness inferred. Remaining five domain implementations/releases are in progress. Consult domain-integration.md, not older checkpoint status.

### Correction bundle observed locally

0400 and forward0401 applied/immutable. First manual prepare exposed nested JSON operator precedence;0401 parenthesizes extraction before key-array subtraction. Synthetic original500 posted at sequence3, then one bundle committed reversal500 and replacement700 at sequences4/5. Same-key and new-key recovery returned identical paired receipt. Original book is NOW sequence5, bank-700/clearing700; previous zero-balance/reconciled state was an earlier checkpoint only. Old reports/reconciliation remain immutable at earlier cutoff and are not current readiness evidence. Recurring book remains intentionally unposted. Corrections UI composed. Artifact manual-correction-bundle-receipts.json. No standalone-half/crash/concurrency/browser proof asserted.

## User-requested freeze, error cleanup and commit

User now explicitly authorized committing all code before continuing feature work. Seven owners frozen. All delivered backend groups are composed; commerce UI remains absent rather than fabricated. Reviewed0600/0700/0800 applied; all migrations through0800 are immutable in this local DB. Schedules, commerce registers, closing readiness/history and capacity reports return200 for correctly scoped requests. Earlier403/404 manual calls used wrong credentials/path and were corrected without weakening access control.

Full types pass after missing commerce export and typed Box label support fixes. Optional bank allocation/schedule/closing UI panels now use lazy chunks rather than raising the bundle warning threshold. Lint passes after narrowing the closing form value to string. No new automated tests/browser checks/production actions performed. Build/format/diff and credential-safe staging precede the authorized commit. Original book sequence5; recurring book sequence0. See domain-integration.md for exact scope and remaining gaps.

Final precommit checks: full types (including existing test source), lint, full web/API dry-run build and format check pass. Zero lint warnings/errors and no client bundle-size warning. Evidence `.agents/work/openerp-implementation/precommit-checks.json`. No automated suite/browser run and no production deployment. Credential/generated-path scan found no private files among commit candidates. This is the user-authorized integration/error-fix checkpoint, not completion of the full design.

## Post-cleanup bounded integration observations

Cleanup commits: f7475e41 (code/integration) and90db69b4 (late documentation); working tree was clean afterward. Active full-system goal is not complete. Commerce owner resumed only existing0600 UI, other retained domain owners remain frozen.

Owned synthetic recurring book: approved/posted one combined2000 journal at sequence1. Allocated500from bank source row2 to that existing line; row1 retained1000and row2 retained500. A recurring row2 proposal approved before allocation then failed execution409StaleDependency; ledger remained sequence1. A fresh simulation excluded the partially consumed row. Remaining1000+500 allocation completed the source↔line matching with no ledger write. See manual-partial-bank-capacity-receipts.json.

Declared explicit synthetic bank inventory and prepared current internal trial balance. Technical close became allowed while statutoryReady remained false. Close locked the period at version2; preparation into it failed409PeriodLocked. Reopen changed it to unlocked/version3, invalidated1certificate and1report. Old certificate is not current; another close is blocked until new trial-balance and bank evidence. History has two transitions; ledger stays sequence1. See manual-technical-close-reopen-receipts.json.

These are local API observations, not automated tests, independent accounting acceptance, browser/failure/concurrency proof or statutory readiness. Original correction book remains sequence5; recurring book is now sequence1 with bank2000/clearing-2000. Old sequence0 and complete-close observations are historical, not current authority.

## Commerce UI integration checkpoint

Mounted the existing0600 synthetic register UI lazily in the accounting workspace and added section navigation. Supports counterpart/current/historical reads and revisions, registration against existing recognition, invoice metadata/history/evidence, posted payment capacity, 1–50 allocation legs, explicit operator approval/application, saved-ID lookup and captured-request export/retry. It neither issues invoices nor posts accounting or initiates payments. No automatic browser persistence is claimed.

Review fixed revision-key remounts that discarded captured requests after query refresh. Current revision inputs remain stable until explicit new-command reset. Typecheck findings fixed with the supported border token and typed schema decoder. Root full types, lint, format and web/API dry-run builds pass. Current Worker ledger/register/closing-readiness reads return200; the old recurring proposal still refuses execution with409StaleDependency. Evidence: commerce-integration-checks.json.

No browser interaction or full commerce mutation/recovery/concurrency proof. Concurrent Drizzle adapter/setup/dependency/instruction/documentation changes are preserved; they are outside this UI checkpoint and are not covered by an adapter-migration acceptance claim. All seven retained domain owners remain frozen after this bounded handoff. Full-system goal remains incomplete.

## Large domain implementation wave resumed

User explicitly authorized continued multi-domain implementation with large autonomous packages and quiet root orchestration. Seven retained owners assigned concurrently: posting/request recovery; correction impacts/chains; evidence-preserving reviewed CSV intake; owner expenses/funding register; expense VAT facts and review controls; immutable accountant review/export pack; backup/restore completeness and operational verification tooling. Full briefs are in current-domain-wave.md. No nested agents, new tests/fixtures, real-company postings, provider submissions, deployment or Git reconstruction. Root owns shared integration/company-fact boundaries and serialized native validation. Missing company/VAT/funding facts remain explicit rather than defaulted. Earlier all-owner freeze is superseded by these assignments.

## Correction workbench source review

Received the complete corrections-domain package and integrated five fixed Drizzle/capability bindings for impact snapshots, chain history, bundle discovery and actor-scoped request recovery. Root checked the forward migration's intent binding, live guards, retained chain totals and compatibility with0400/0401 receipts. One report resource link was sent back for correction: use `/report-snapshots/:id`, not `/reports/:id`.

0410 is not applied or runtime-accepted. It references later stable domain schema including0900. The current ordered migration runner would also encounter concurrently drafted0310 and other files; do not apply an unreviewed prefix simply to exercise0410. Root will apply only a dependency-complete reviewed batch after the remaining releases and schema checks. Existing SQL files remain immutable. No new tests, real-company operations or production actions were performed.

## Complete source composition and remaining integration

All seven source packages are handed off. Owner-register0610 is now exported and composed through18 fixed statements,16 ordinary capabilities, REST handlers and a lazy scoped workspace panel. Classification review/allocation approval remain REST-only. Root full `bun run check-types` passed, including existing test sources; the command also ran its configured web-build prerequisites. No test suite was run. Full lint initially found two unsafe object-to-string conversions in owner/tax UI; owners narrowed them, and root full lint then passed with zero warnings/errors.

Local maintenance read confirmed database `openerp_development` at55472 and all applied migration checksums match current files.0900 Better Auth is not yet applied there. No new-wave migration is applied.0310 malformed qualifiers were fixed before application; current SHA256 d8e0b4b5fefe3752db81402d27bcc000fe48a834dcbeda8ed39fa4f92208daec.0510 now explicitly accesses SQL composite arguments and starts approval expiry after lock/validation; current SHA256 af448df45946719d89e4e23f7a53d5b4ab0b81de43a50c4d953abb3cb873f43d.

Year-end owner is completing available owner/tax provider capture in still-unapplied0810 and a new0820 closing dependency hook. Root explicitly reserved0890-owner-correction-impact.sql for corrections owner (exception to original ranges): its released private resource reader includes owner records, effects, proposals and allocation digests.0610 already guards posting, but0410 alone omitted these known preflight blockers.0890 source is reviewed, not runtime-accepted; historical rows/replays are not rewritten.

Root closed the raw duplicate-JSON-member gap in the shared Worker body boundary. An unchanged non-mutating MCP ping returned200 before and400 after. Escaped/nested duplicate keys, invalid UTF-8 and129 containers were refused; distinct-object keys/quoted evidence and128 containers passed. API/script types and bounded type-aware lint pass. See `openerp-implementation/manual-json-admission.json` and `json-admission.md`. This is bounded manual transport evidence, not full REST/auth/browser/concurrency or accounting acceptance. The body change and0890 require the next integrated check checkpoint. No real-company action, new test/fixture, deployment, commit or push occurred.

## Root local application checkpoint

All seven packages and their shared surfaces are integrated. Complete native typecheck (including existing test source), full type-aware lint, whole-repository formatting check and web/API dry-run build passed. Formatting-only cleanup preserved the reported files' content/rules; no test suite was run and no dependencies or lint exceptions were added.

All nine pending migrations0310/0410/0510/0610/0710/0810/0820/0890/0900 are now applied to the owned local `openerp_development` PostgreSQL at127.0.0.1:55472. All34 applied file hashes match. Initial0610 application failed on an unparenthesized CASE in a PL/pgSQL IF condition; its transaction rolled back. Root parenthesized two CASE expressions in that still-unapplied file and resumed successfully. Final0610 SHA256:64128afc85cc1a50132b78f5c05227eb351ae565f3fd49baa2c6ba69552c00b4. Every applied migration is now immutable; further SQL fixes require new forward files. No ledger posting/reversal was created during this pass: automation sequence remains1 and original sequence5.

Nine discovery/read surfaces returned decoded200 responses. A server-saved execution request first retained unknown outcome, then recorded the expected stale-period refusal. Recovery and explicit rerun returned the exact terminal outcome; changed-body reuse of its key returned409. This is not proof of timeout/crash/revocation races or new successful financial posting.

A fresh original-book report and immutable accountant pack were created through the API from existing synthetic records. Exact command replay returned the same pack. Its7 sections contain2 balance rows,10 journal rows,3 evidence rows,14 coverage rows and empty owner/tax sections. All8 downloaded JSON/CSV artifacts match independent SHA256 and byte-length calculations. Independently summed exported journal debits/credits are26700/26700 minor units. Opening status remains not_verified and company completeness/statutory acceptance remain unestablished. Exact downloaded bytes live under `.cache/openerp-development/accountant-review/review_pack_0e38180b595141b09bcbc1762d395e17/` (private/ignored local artifacts).

Evidence: `openerp-implementation/domain-wave-preflight.json`, `manual-domain-wave-receipts.json`, `manual-json-admission.json`. Populated owner/tax workflows, CSV admission, successful new saved posting, approval revocation/concurrency/crash handling, browser flows, backup/restore and independent accountant acceptance remain unobserved. Known expense-tax sources conservatively block technical close because the provider lacks supported posting/reconciliation, even after a current fact review. Oversized live closing/reopen remains outside the bounded provider scope. Real-company setup facts, approved treatment/profile authority, statutory features and production readiness are not supplied by these observations. No new fixtures/tests, real-company posting, deployment, or new commit/push occurred. Goal remains open. Owners are retained for concrete integration fixes; no new autonomous wave was assigned.
