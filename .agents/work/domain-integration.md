# Domain integration checkpoint

## Current user directive

The requested cleanup is committed in f7475e41 and90db69b4. Full types, lint, format and builds passed. The bounded commerce UI for the existing0600 API is integrated and statically checked; all retained owners are frozen. Root owns shared composition and serialized local observations. No new tests, deployment, push or production action is authorized by this checkpoint.

## Integrated source

| Domain | Owner | State |
|---|---|---|
| Posting/approval/receipts | accounting-api | Recovery REST/MCP/UI integrated;0300 applied. Manual posted/unposted/request recovery observed. Draft preparation keys remain mounted-only. |
| Corrections | corrections-domain | Paired correction REST/MCP/UI integrated;0400/0401 applied. Synthetic paired posting and receipt replay observed; full failure/concurrency proof absent. |
| Imports/matching/reconciliation | bank-reconciliation | Partial allocation REST/MCP/UI integrated;0500–0502 applied. SQL ordinal collision corrected before application. Existing recurring proposals get a posting-time consumed-source guard. Partial500 allocation from source row2 observed without consuming row1; pre-approved recurring execution rejected after consumption; remaining1000+500 many-to-one allocation produced a complete report. Ledger did not change during matching. |
| Invoices/payments/registers | accounting-ui | Contracts/API/SQL integrated;0600 applied. Register reads observed. Dedicated lazy-loaded UI integrated; types/lint/format/build pass. Revision-editor capture is stable across query refresh. Browser and complete mutation/recovery proof remain absent; no end-to-end release claim. |
| VAT/payroll/assets/FX | tax-subledgers-domain | Synthetic asset/deferral schedules REST/MCP/UI integrated;0700 applied after id qualification fix. List observed. VAT/payroll/FX unsupported. |
| Year-end/statutory/filing | year-end-domain | Technical close/reopen REST/MCP/UI integrated;0800 applied. Technical close/reopen observed: locked-period preparation rejected; reopening invalidates old certificate/report and requires fresh bank/report evidence. Explicit ordinal avoids unsupported backup sequence state. Statutory readiness remains false. |
| Restore/operations/cutover | operations-domain | Local-only CLI integrated into normal script typechecks. Tagged errors/schema construction fixed. No backup/restore run, production action or archive compliance claim. |

## Checks

Full types (including existing test sources) pass. Root lint passes with zero warnings/errors. The UI Box primitive now supports typed native labels; optional panels use lazy chunks instead of weakening bundle warnings. Full build and formatting checks pass, with no bundle-size warning. Exact outputs and local read observations are retained in precommit-checks.json. Staged whitespace validation precedes the commit.

Migrations through0800 are applied and immutable in the owned local database. Existing external processes remain untouched. No automated test suite or browser interaction was run in this checkpoint. Existing test changes from the checkout are preserved; no test implementation was added by this root.

Manual records under `.agents/work/openerp-implementation/` are observations, not independent acceptance. Current original book is sequence5, bank-700/clearing700 after the paired correction. Recurring book is now sequence1, bank2000/clearing-2000, from the explicitly approved combined synthetic posting. Both source rows are fully allocated. Its period is reopened/unlocked at version3; earlier closing report/bank evidence requires refresh before another close. Old zero-balance and reconciliation receipts are historical snapshots, not current closing readiness.

## Boundaries retained

- Settlements owns bank-observation↔bank-line capacity; commerce owns invoice↔payment capacity.
- Required-source declarations belong to closing, not inferred imported-source inventory.
- Operator approval and activation remain outside ordinary MCP tools.
- Full-system goal remains incomplete; missing company, legal, operational and failure/recovery proof is not replaced with a status flag.

## Active large-package integration

Root received/reviewed source handoffs for posting recovery0310, corrections0410, source intake0510, expense-tax facts0710, accountant-review0810 and recovery tooling v2. Posting/corrections/intake/tax/review shared contracts, fixed Drizzle dispatch/capability bindings and workspace mounts are integrated. Authority-only posting actions, source approval/admission and expense-tax review remain outside ordinary MCP. Correction report-resource path is fixed to `/report-snapshots/:id` before application. Source/schema review continues; none of these new migrations is claimed applied or runtime-accepted.

Recovery v2 owned formatting, dedicated operations TypeScript and bounded Oxlint pass. Full application restore remains blocked by the distinct read-only admission/permission boundary; no backup/restore rehearsal or real-company operation was run. Owner expenses/funding0610 remains with its autonomous owner. Do not migrate an unreviewed draft prefix. Root is validating contracts and will review a dependency-complete SQL batch before native application. Current repo was recreated by the user on main; origin is erik-kroon/openERP and main was successfully pushed after user-approved GitHub workflow scope. Current domain work remains uncommitted/unpushed.

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
