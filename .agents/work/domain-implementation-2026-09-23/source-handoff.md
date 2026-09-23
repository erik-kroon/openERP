# Domain implementation handoff — 2026-09-23

## Delivered source

- Bank1300: reviewed unmatch for whole allocations and retained exact matches; immutable history and effective capacity views. No ledger reversal or implicit period reopen.
- Invoice1400: synthetic issue review and same-operator approval/execution, atomic kernel posting/internal SYN number/customer register/issue receipt, frozen issued draft and fresh issue-history editor overlay. No legal invoice, delivery or correction workflow.
- Asset1500: evidence-backed original/accumulated/carrying basis linked to posted lines; immutable all-row declared-account controls. Reporting/linkage does not gate existing schedule posting.
- Closing1510: complete asset-control dependency, mandatory missing-basis/coverage blockers and accountant-review-v3 exports. Old artifacts remain decodable and unchanged, with separately stale currentness.
- Shared exports, capability catalog/bindings, SQL dispatch, HTTP handlers and both current routed and legacy UI composition are connected.

## Source review

Independent invoice review found an owned-source escape via a different event key and a caller-usability mismatch. The domain owner bound aggregate ownership to retained evidence as well as event, refused already-posted retained sources, made approval usability actor-specific and added typed counter exhaustion. Root re-read those replacements.

Independent asset1500 review found no concrete blocking defect in conservation, scoped linkage, ordinal-preserving reversal effects, declared-account rows or response schemas. Root compared1510 replacements against the latest prior definitions: VAT clauses and active-bank hook dispatch remain; only new dependency, blockers, generation and historical-read bounds are added. These are source conclusions, not executed proof.

## Boundaries

No test/fixture edits, lint/types/builds, browser/server/database execution, migration application, dependencies, commits, deployment or external actions were performed for this wave. SQL syntax, transactions/deferred constraints, concurrency, response decoding and rendered UI remain unverified. No legal/source-completeness/financial-close readiness is claimed.

The shared worktree has unrelated ongoing UI edits. Preexisting-files.json records the initial reservation only. The source manifest hashes current complete files, including preexisting/concurrent contributions in shared files; it is not a claim of exclusive ownership or a clean/frozen worktree. No historical migration was edited by this wave.

See docs/plans/accounting-completion-wave.md and the three apps/api domain handoffs for contracts, limitations and pending acceptance.
