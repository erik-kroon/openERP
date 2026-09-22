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
