# OpenERP NEXT-101 through NEXT-125

**25 new application-owned work packets with implementation-level pseudocode.** They supplement the prior 100 design scopes, not renumber incomplete earlier integration or assume those scopes are implemented.

Checkpoint: `66355b62b23e3b8007c2d324f3739fbbcc96cdc0`, 28 September 2026. The attached 76..100 dossier and earlier scope definitions were used to avoid duplicate work. Repository reading was targeted to the branch and shared operations/contracts. Specialist rules/provider facts were checked narrowly against primary sources, not fully qualified.

## Use

Coordinator: [MASTER-PSEUDOCODE.md](MASTER-PSEUDOCODE.md), [COORDINATOR-HANDOFF.md](COORDINATOR-HANDOFF.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md).

Worker: one packet plus [00-COMMON.md](00-COMMON.md), [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md) and [SOURCES.md](SOURCES.md). Helper names are proposed responsibility contracts to bind to actual owners. A pure function or another retained JSON blob is not a completed application journey.

## New packet index

| ID | Priority when applicable | New deliverable |
|---|---|---|
| NEXT-101 | P1 | [Accounting-firm delegation and multi-client workspaces](packets/NEXT-101.md) |
| NEXT-102 | P1 | [Scoped evidence requests and response reconciliation](packets/NEXT-102.md) |
| NEXT-103 | P1 | [Versioned balance-sheet substantiation schedules](packets/NEXT-103.md) |
| NEXT-104 | P1 | [Shared-cost attribution across projects and dimensions](packets/NEXT-104.md) |
| NEXT-105 | P1 | [Project margin with billing, recognition and cash bridges](packets/NEXT-105.md) |
| NEXT-106 | P1 | [Service-retainer entitlements and once-only drawdown](packets/NEXT-106.md) |
| NEXT-107 | P2 | [Onerous service-contract provisions and release on performance](packets/NEXT-107.md) |
| NEXT-108 | P2 | [Warranty cohorts, expected claims and provision consumption](packets/NEXT-108.md) |
| NEXT-109 | P2 | [Insurance-loss claims and gross compensation accounting](packets/NEXT-109.md) |
| NEXT-110 | P2 | [Borrowing reschedules, debt forgiveness and amended obligations](packets/NEXT-110.md) |
| NEXT-111 | P1 | [Annual common-cost VAT deduction true-up](packets/NEXT-111.md) |
| NEXT-112 | P2 | [Domestic construction reverse-charge sales and purchases](packets/NEXT-112.md) |
| NEXT-113 | P2 | [EU B2C destination VAT and Union OSS reporting](packets/NEXT-113.md) |
| NEXT-114 | P1 | [EU foreign input-VAT recovery claims and receipts](packets/NEXT-114.md) |
| NEXT-115 | P2 | [Overnight travel allowances and meal-benefit partition](packets/NEXT-115.md) |
| NEXT-116 | P2 | [Recurring car-benefit valuation and employee payment links](packets/NEXT-116.md) |
| NEXT-117 | P2 | [Interest statements: KU20 and applicable KU25 identities](packets/NEXT-117.md) |
| NEXT-118 | P2 | [Prospective salary exchange into pension contributions](packets/NEXT-118.md) |
| NEXT-119 | P2 | [Cash share subscriptions and registered-capital transition](packets/NEXT-119.md) |
| NEXT-120 | P1 | [Preliminary income-tax revisions and authoritative installment schedules](packets/NEXT-120.md) |
| NEXT-121 | P1 | [Opt-in bounded standing posting mandates](packets/NEXT-121.md) |
| NEXT-122 | P1 | [Cash-constrained payment proposals with explicit optimization bounds](packets/NEXT-122.md) |
| NEXT-123 | P1 | [Autogiro mandates and direct-debit collection outcomes](packets/NEXT-123.md) |
| NEXT-124 | P1 | [Bank-feed provider handover with continuity evidence](packets/NEXT-124.md) |
| NEXT-125 | P1 | [Processor refund initiation with reserved entitlement and outcome recovery](packets/NEXT-125.md) |

## Delivered and not claimed

Every packet supplies records, calculations/decisions, transaction composition, correction boundaries, downstream readers, operator behavior and exact examples. The attached source and current owners remain authoritative where their actual implementation differs; this is proposed additional design, not an instruction to ignore current code.

[DECISIONS.md](DECISIONS.md) explains the major choices. [solution-index.json](solution-index.json) and [dependency-graph.json](dependency-graph.json) expose dependencies and reservations. Only the new-wave graph is checked; no full 125-node graph audit is claimed. [design-examples.json](design-examples.json) and [CHECKS.md](CHECKS.md) describe independent dossier checks, not runtime proof.

No application source, migrations, tests, actual bookkeeping, deployment or external financial action was performed. The package contains original design, JSON metadata and its own local checker, not statutory table bundles, provider credentials or font files.
