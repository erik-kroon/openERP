# OpenERP testing-plan review package

Focused review of the `test plans` commit `8bff9fadbcacf9d369758b967971469548834365`, using files at observed branch head `ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb`.

This reviews the testing work, not the later Accounted feature-parity backlog. No repository code or tests were changed or run.

## Documents

| File | Use |
|---|---|
| [REVIEW.md](REVIEW.md) | Prioritized findings with source references and proposed resolutions |
| [REVISED-TEST-PLAN.md](REVISED-TEST-PLAN.md) | Revised harness, transaction, race, oracle, evidence and coverage design |
| [CORRECTED-WORKFLOW-CASES.md](CORRECTED-WORKFLOW-CASES.md) | Concrete replacements preserving the five workflow families and original case IDs |
| [COORDINATOR-HANDOFF.md](COORDINATOR-HANDOFF.md) | Coding-agent assignment and integration order |
| [ORACLE-EXAMPLES.json](ORACLE-EXAMPLES.json) | Independently specified illustrative amounts and canonical byte/hash vectors |
| [SOURCES.md](SOURCES.md) | Reviewed sources, ranges and external technical documentation |
| [CHECKS.json](CHECKS.json) | Document structure and example-arithmetic checks, not application test results |

Use the review and corrected cases together. A passing design example is not a passing application test. The financial policies and synthetic role assignments in examples do not activate an actual Swedish company or statutory profile.
