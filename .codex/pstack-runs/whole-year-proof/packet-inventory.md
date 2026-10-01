# Packet inventory

Read-only investigation on 2026-10-01. Source and historical artifacts were inspected. No packet is marked verified by this inventory. Paths below are relative to apps/api/src unless otherwise indicated. Original task is the attachment named in overview.md.

| Packet | Outcome | Existing owner | Open obligation |
| --- | --- | --- | --- |
| 1 | Stable accounting baseline | Isolated snapshot writer | Running exact snapshot and checks; no pass yet. |
| 2 | Company profile and evaluation contract | application/company-profiles.ts; company-profile-basis.ts | Versioned facts and activation exist. Evaluation assistance and first-pass freeze owner missing. |
| 3 | Custody and recovery | scripts/operations/workflows.ts; source-retention.ts | Closure proof exists. Restricted application reads still blocked by lock admission. |
| 4 | Dated rules | company-profile-basis.ts; closing/rule-impact.ts | Release selection exists. Qualified release intake and stale-plan proof required. |
| 5 | Evidence and economic-event identity | source-retention.ts; evidence-work.ts; purchases/recognition.ts | Byte/occurrence identity exists. Combined overlap recognition proof remains. |
| 6 | Agent context | agent/context.ts | Refuses above 50. Continuation and durable restart discovery missing. |
| 7 | Opening and owner funding | subledger/owner-operations.ts; subledger/owners.ts | Funding modes exist. Combined opening lineage, repayment owner and proof missing. |
| 8 | Company-bank supplier settlement | Missing application owner | Manual journals plus allocations do not close packet. |
| 9 | Privately paid expenses | subledger/owner-operations.ts | Backend modes exist. Owned UI and full reimbursement proof missing. |
| 10 | Privately funded balances | Missing application owner | Invoice deferral schedules are distinct. Valuation qualification remains. |
| 11 | Foreign purchases | purchases/service-purchases.ts; commerce/fx.ts | Service refusal proof exists. Qualified success journey and UI missing. |
| 12 | Equipment/assets | subledger/schedules.ts; asset reviews/basis/execution | Synthetic code exists. Acquisition, policy, disposal and year-control proof incomplete. |
| 13 | Cash method | Commerce document/payment owners | Writers fenced. Qualified commercial-only document and effective recognition prerequisites missing. |
| 14 | Durable agent preparation | period-work.ts; runtime/preparation-queue.ts | HTTP/UI/queue exist. Period-work writes operator-only. Agent policy decision and recovery proof required. |
| 15 | Approval and recovery | Posting and period-work owner | Seals and mixed results exist. UI owner links and per-owner response-loss proof incomplete. |
| 16 | Corrections | posting-corrections.ts and register owners | Bounded correction proof exists. Complete downstream and cross-period propagation incomplete. |
| 17 | Year controls/close | Banking/VAT/tax/financial-close owners | Bounded synthetic close proof exists. Full applicable-family controls incomplete. |
| 18 | Year pack/freeze | Reports/accountant-review/SIE4E/annual-report | Individual report owners exist. Complete immutable pack and first-pass freeze missing. |
| 19 | Accountant comparison | New owner using SIE parsing | Historical closing comparison exists. Separate reference dataset and economic comparison missing. |
| 20 | Difference review/rehearsal | Cases/operations consuming comparison | Complete difference lineage and full synthetic journey missing. |

## Governing evidence

- `docs/README.md` and `docs/open-decisions.md` distinguish implementation, synthetic evidence and real-company qualification.
- `docs/plans/15-book-zero-workflow-cash.md` binds the full-year outcome to maintained financial owners.
- `docs/plans/evidence/df-09-supplier-credit-cap.md` records the unstable-source broader run.
- `docs/operations/local-recovery.md` retains blocked restricted application reads.
- `docs/plans/evidence/next-38-cash-method.md` records fenced writers and their unresolved prerequisites.
- `docs/plans/evidence/next-23-review-repair.md` records bounded synthetic close evidence.

Actual company methods, registrations, framework, fiscal coverage and populations remain unknown in this run. Synthetic profiles must carry explicit labels and cannot activate real-company postings.

## Snapshot caveat

The baseline snapshot admitted additional in-flight NEXT38 source and migrations after the read-only inventory. Its captured untracked-path inventory is `/Users/admin/.codex/worktrees/whole-year-baseline/openERP/test-results/stable-baseline-capture/admitted-untracked.json`. Packet 13 must be reconciled against that snapshot after checks. The earlier fenced-writer finding describes the audit observation and cannot establish the later snapshot behavior.
