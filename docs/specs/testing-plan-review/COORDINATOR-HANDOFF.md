# Coding-agent handoff: repair and implement the testing plan

## Assignment

Improve `docs/plans/test-suite-design.md` and `docs/plans/test-suite-pseudologic.md` using this review, then implement only the testing changes explicitly authorized by the user and repository instructions. This review is not authority to modify active financial workstreams, perform production postings or submit anything externally.

Read current `AGENTS.md`, ADR 0010, ADR 0009 and `docs/verification-strategy.md` first. Reconcile the actual checkout with review baseline `ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb`. Preserve dirty work and existing task ownership. The test-plan commit under review is `8bff9fadbcacf9d369758b967971469548834365`, not the later Accounted parity backlog.

## Required decisions

1. The trusted Effect application owns policy, authorization and scoped DML. PostgreSQL owns durable state and narrow structural integrity. Remove function-only runtime assertions and obsolete period-trigger requirements.
2. Keep Vite+/Vitest and the current real-workerd/disposable-PostgreSQL harness. Serial files and zero retries already exist. Extend `apps/api/tests/support` rather than constructing another platform.
3. Test valid current workflows through their public operations. Separate direct-DB integrity/corruption probes from application authorization. Always include legitimate-path positive neighbors.
4. Preserve the SO/CB/SA/HI/AB/XC and E-01 through E-21 terminology. Apply the explicit case corrections before coding them. The old case counts are not an acceptance target.
5. Preparing a credit does not reserve or consume it. Test financial capacity at execution, unless an independently specified reservation owner exists.
6. One real transaction must cover the entire journal/register/approval/receipt group. Observe it from another connection and inject failures late enough to exercise rollback. Do not wrap HTTP E2E in a shared outer rollback.
7. Use the book-row gate and observed blocker graph for races. Missing observed overlap is a harness failure, not a passing concurrency result.
8. Preserve exact amounts and independently specified digest bytes. Do not generate expected results with the production calculator/canonicalizer.
9. Use immutable run directories and generated case coverage. A hash change needs a reviewed explanation, not automatic snapshot acceptance. A required absent/skipped case cannot produce a green release lane.
10. Keep synthetic correctness, application runtime proof, real-company applicability and provider acceptance separate.

## First edits to the documents

Correct HARNESS-1/2/3; SA-H1; CB-R3; CB-X1; SO-H1/H2/R6/R9; SA-R2/R3; AB-R2; HI-R4; XC-1/4 and the reported coverage totals. Use `CORRECTED-WORKFLOW-CASES.md` for the replacement fixtures.

Do not silently change product behavior to match today's guard order. Label each expectation as an accepted invariant, current API contract or current implementation characterization. Report a conflict between them instead of blessing whichever source is easiest to test.

Restore historical source documents byte-exact only without modifying them. Put supersession notes beside them. Prefer commit-pinned repository references over developer-machine paths. Do not vendor reference datasets until reuse terms and privacy are checked.

## Test implementation order after authorization

- **TEST-01:** preflight, fresh scenario fixtures, exact footprint observers, immutable run directories and observed book-gate races.
- **TEST-02:** supported supplier credit prepare/approve/execute/replay and sales create/revise/accept/source-conversion behavior.
- **TEST-03:** corrected schedule prefix/suffix and lifetime cases, historical admission controls and asset basis cases.
- **TEST-04:** competing execution, revocation/expiry, domain-write rollback, deferred commit failure, response loss and stable report boundaries.
- **TEST-05:** minimal real browser review/reload path, negotiated MCP operation and nonempty Bun job recovery; generated case coverage and affected-change gates.

The plan's original no-unit-test policy must be discussed explicitly if pure conformance/regression tests are to be added. Do not call them something else to evade the rule. Small independent domain tests are recommended, but no authorization is inferred from this document.

## Required completion report

Report exact source revision and dirty input hashes; what was changed; leaf case IDs and mapped E-cells; selected/collected/executed/passed counts; source/rule provenance of expected values; financial/register before and after; observed barrier/fault traces; evidence locations and unresolved findings. Separate product failures from fixtures that were themselves invalid.

Do not declare complete coverage of E-02, E-03 or any other family from one passing example. Do not claim browser, managed Hyperdrive or live provider behavior from local Worker success. Preserve first-attempt failures even if diagnostic reruns pass.

Deliver corrected plan documents and the authorized test changes, not another description of what a good harness might look like. Keep the five reserved workstreams and application migration with their existing owners.
