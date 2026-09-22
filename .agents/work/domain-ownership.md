# OpenERP domain ownership

User directive: one subagent per listed area/domain. Seven retained owners; no nested delegation. Each domain owns contracts, backend and its local UI rather than a technical layer.

| Area | Retained session | Migration range | Current slice |
|---|---|---|---|
| Posting, approval, receipts | accounting-api | 0300–0399 | Durable proposal/approval/execution recovery across reloads and uncertain responses |
| Corrections | corrections-domain | 0400–0499 | Atomic linked reversal plus replacement, sealed bundle review and receipt |
| Imports, matching, reconciliation | bank-reconciliation | 0500–0599 | Reviewed partial/many-to-many bank observation↔posted-line capacity |
| Invoices, payments, business registers | accounting-ui | 0600–0699 | Counterpart registers, evidence-backed invoices/open items and payment allocation |
| VAT, payroll, assets, FX | tax-subledgers-domain | 0700–0799 | Exact durable asset/deferral schedules; legal/profile-dependent capabilities fail closed |
| Year-end, statutory reports, filing | year-end-domain | 0800–0899 | Explicit technical period close/reopen, separate from statutory readiness |
| Restore, production operations, cutover | operations-domain | 0910–0999 (0900 is auth) | Safe local backup/fresh-destination restore tooling and read-only cutover preflight |

The first three session names are retained for context, not technical-layer ownership. accounting-ui now owns commerce, not other UI. accounting-api now owns posting/recovery, not all API. bank-reconciliation no longer owns recurring automation or broad auth reviews.

## Root ownership and validation

Root owns shared contracts exports/API composition/accounting base schemas/error/capability registry, the single database dispatcher, authentication/MCP/Worker boundary, shared web routing/workspace/lib and translation catalogs, root manifests and infra composition. Domain workers provide exact integration mappings or request narrow handoffs; no concurrent edits to these shared files.

Workers use dedicated domain-local component subdirectories and copy modules. Existing migrations through0900-better-auth.sql are treated as immutable; local observations had applied through0800 before the concurrent authentication work. Reserved new ranges do not imply dependency ordering: root reviews dependencies and applies only approved files. Workers do not run migrations, DB changes, servers, builds or repo-wide validation. Root serializes native validation and owned local resources. Bounded owned-file lint and source review are permitted.

User still requests no new tests. No test files/fixtures, commits/pushes/deployment, real-company postings, external submissions, dependency additions, secret disclosure or credential overwrites. Static checks and manual observations never stand in for complete failure/recovery or compliance proof. Unsupported business/legal/provider facts remain explicit blockers.

## Domain interfaces

- Posting and corrections coordinate before changing the base single-voucher kernel. New correction bundles must not silently weaken old identities or replace approved content.
- Settlements owns bank observation↔posted-line matching capacity. Commerce owns invoice/open-item↔posted-payment capacity and residuals. Bank matching is not invoice payment; immutable matching receipts may be referenced without creating duplicate invoice residual authorities.
- Subledgers owns schedule state and remaining balances; year-end consumes explicit dependencies, not guessed completeness.
- Operations owns operational artifact/preflight semantics; year-end does not treat local backup checksum as verified retention/restore.
- Every worker messages only ready integration slices, material cross-domain dependencies or blockers. No routine acknowledgments/polling.

## Active autonomous packages

The user explicitly resumed large parallel domain tasks with quiet orchestration. `.agents/work/current-domain-wave.md` is the current assignment record and supersedes the earlier freeze/current-slice descriptions. All seven retained owners were assigned substantive packages without waiting for each other. Root owns integration, shared company-fact boundaries and serialized validation. No acknowledgment/status polling; report ready work, material blockers or safety decisions only.

Reported company context: first year, approximately50 events, no employees/income, company/private expenses and shareholder funding; parents are accountants using unspecified Visma software. No legal/tax configuration or transaction classification is inferred. Real-company execution remains unauthorized. Git metadata was removed by the user; workers and root must not silently reconstruct it or claim new commits.
