# Current foundation and Book Zero reconciliation

2026-10-03. This continues the historical [FND-01 inventory](fnd01-reconciliation.md)
against implementation revision `4c591511a5df48454ac392a06dc8eb976b843ee8`.
It does not assign the old SQL-dispatch evidence to the application-owned runtime.
The [focused observation](evidence/foundation-core-20261003.json) binds the current
source and migration bytes to 31 passing existing E2E cases, with stable source
integrity. Company acceptance and operational cutover remain open.

## Live owners and evidence

| Packet | Current owner and caller | Established result | Remaining acceptance |
| --- | --- | --- | --- |
| FND-01 | `packages/contracts/src/api.ts`, `apps/api/src/index.ts`, `application/capabilities/index.ts`; REST and MCP compose named application operations. | The application-owned replacement supersedes SQL dispatch. The capability registry satisfies the shared declared key set. Current core REST/MCP execution and reads pass. | Inventory every supported operation/profile against its actual caller and packet evidence; a registered handler is not a verified workflow. |
| FND-02 | Better Auth; `db/identity.ts` and `application/identity.ts`; trusted HTTP/MCP admission. | Current focused cases refuse cross-book access, agent approval, revoked credentials, deleted sessions and lost approver membership; runtime scoped DML and protected history behave as required. | The authority requirement is operator/agent plus owner-specific guards, not the full separate-power catalogue. Full contention and production identity/profile qualification remain open. |
| FND-03 | `application/company-profiles.ts`, its database owner and shared contracts. | Immutable fact/review/rule/account-role/activation records have a real owner. [Activation admission](evidence/company-profile-activation-admission.md) records its bounded synthetic journey. | Real company facts, reviewed rule releases, complete mandatory-check coverage and profile combinations remain unqualified. Configuration does not establish accounting completeness. |
| FND-04 | `tests/support/global-setup.ts`; disposable PostgreSQL, restricted runtime role and real workerd. | The focused run applies the current migration chain, tests populated rerun/checksum refusal and retains source/migration hashes, assertions and sanitized financial receipts. Cleanup reports unchanged source. | This run does not exercise Bun self-host, browser accessibility, complete restore or every forward-migration upgrade. Retained replacement proof has its own revision bounds. |
| PST-01–PST-04 | `application/posting.ts`, `posting-admission.ts`, `posting-recovery.ts`; accounting and recovery HTTP, shared MCP and web review callers. | Exact values beyond JavaScript safe integers, duplicate-key admission, read-only review, concurrent first execution, receipt replay, late-write rollback and actual response loss pass in the focused run. | Full approval-revocation contention, all review/recovery browser states and complete all-channel scenarios need their own evidence. |
| PST-05 | Preparation/effect-mq and period-work owners. | [Batch recovery](evidence/approval-batch-recovery.md) proves bounded supplier-recognition mixed results and receipt recovery at its recorded revision. Preparation does not confer posting authority. | Full durable-run/stop/restart scope and any enabled mandate need exact family-specific proof. No automatic posting is adopted. |
| COR-01/COR-02 | `application/posting-corrections.ts`; correction HTTP/MCP and owned review UI. | Reversal remains immutable and balances cancel in the focused run. Bundle execution composes both children and the aggregate receipt in the caller's transaction. | Source composition is not full bundle atomicity proof. Child refusal, faults after the first child, concurrent bundle execution, expiry/revocation and aggregate recovery need explicit observations. |

The focused repeat command and artifact hashes are in the observation JSON. Raw
synthetic artifacts remain in `test-results/foundation-core-20261003`; no real
company material was used. The PostgreSQL runtime role is trusted application
infrastructure and intentionally holds scoped DML, not arbitrary end-user access.

## Drastic AB acceptance scope

The user selects Drastic AB as the first real acceptance company, not as a global
product profile. Import actual retained history from the evidenced start of its
current fiscal year through **2026-09-30**. Fully reconcile Book Zero
**2026-09-01–2026-09-30**, beginning from the authoritative incumbent closing state
at **2026-08-31**. September transactions cannot reconstruct that opening basis.
**2026-10-01** is only a candidate live boundary until incumbent ledger, bank,
receivable/payable and applicable tax controls agree and operational gates pass.

Real originals and exports belong outside this repository and committed fixtures.
Use a configurable private `OPENERP_COMPANY_SOURCE_ROOT`; the suggested private
location is `/private/openERP/company-source/drastic-ab`, not a code default.
Separate company facts/registrations/fiscal-year/policy, ledger/SIE/incumbent
exports, bank statements, sales, purchases, tax, applicable payroll, other
originals and a source manifest. Private manifests and reconciliation receipts
also remain private. Public fixtures stay synthetic.

At this observation no company-source root is configured and the suggested
location is absent. Actual fiscal-year start, accounting method, registrations,
source population and independent controls are **not supplied**. This blocks
actual history admission, September opening/reconciliation, applicability,
year-end qualification and cutover, while synthetic engineering can continue.
The examples in the user's profile comparison do not establish Drastic's values.

Company facts select versioned supported rules and capabilities. Unsupported
combinations remain explicit; no fallback substitutes another method/framework.
Native payroll remains commercially deferred. An evidenced payroll obligation
still requires supported treatment or a specialist handoff.

## Next dependency frontier

Complete the current foundation/core evidence and permission gaps before assigning
a whole-packet exit. Then reconcile retained source/commercial owners and their
existing tests, extend the first-period controls, qualify only applicable accounting
families, and complete the year/artifact chain and operational gates. Company
source absence does not imply these engineering paths are absent from source.
Keep implemented, synthetic-verified, company-reconciled and externally accepted
results separate for every packet.
