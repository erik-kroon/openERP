# Parallel domain implementation

User authorizes domain implementation and subagents, excluding focus on tests/browser verification. This wave runs no tests, browsers, builds, migrations or runtime validation. Source review only; all resulting behavior remains runtime-unverified. No external actions or commits.

| Owner | Slice | Forward migration |
|---|---|---|
| core-gap-map | Reviewed bank unmatch/reversal and effective-capacity/currentness integration | 1300-bank-match-reversals.sql |
| commerce-gap-map | Sealed invoice issue review and bounded synthetic issuance where existing contracts support it; legal/recognition gaps stay blocked | 1400-invoice-issuance.sql |
| compliance-gap-map | Evidence-backed schedule basis and immutable register-to-GL controls | 1500-subledger-controls.sql |
| root | Shared schemas/exports/API/catalog/dispatcher and UI mounting; integrated source review | Integration only |

Workers report ready handoffs or material blockers only. Existing dirty UI files are reserved and recorded in preexisting-files.json. No historical migration edits. Domain docs own detailed contracts; this file records current assignment, not acceptance.
