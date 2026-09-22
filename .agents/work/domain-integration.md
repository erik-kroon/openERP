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
