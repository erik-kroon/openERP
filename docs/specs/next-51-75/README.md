# OpenERP NEXT-51 through NEXT-75

**25 new work packets with implementation-level pseudocode, ownership and completion criteria.** This wave supplements NEXT-01..50 instead of renumbering their remaining integration work.

Pinned source: `116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5`, 28 September 2026. The current progress record distinguishes source, pure leaves and observed journeys. This package does not claim all fifty earlier tasks are complete or that every new capability is wholly absent from unreviewed code.

## Use the package

Coordinator: [MASTER-PSEUDOCODE.md](MASTER-PSEUDOCODE.md), [COORDINATOR-HANDOFF.md](COORDINATOR-HANDOFF.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md).

Individual worker: its packet, [00-COMMON.md](00-COMMON.md), [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md) and relevant [SOURCES.md](SOURCES.md) sections. Bind proposed names to existing owners rather than creating a parallel framework.

**A pure module is not completion.** The supported slice must reach its intended application, storage, report/currentness and user-facing result. Actual provider/authority claims need their own authorized evidence. Independent work can continue while a company fact or external credential is missing, with that gate left explicit.

## Packet index

| ID | Priority when applicable | New deliverable |
|---|---|---|
| NEXT-51 | P0 | [Mixed-rate domestic sales and tax-inclusive prices](packets/NEXT-51.md) |
| NEXT-52 | P1 | [Cross-border B2B service sales and customer-status evidence](packets/NEXT-52.md) |
| NEXT-53 | P2 | [Intra-EU goods acquisition and supply accounting](packets/NEXT-53.md) |
| NEXT-54 | P2 | [Customs imports, import VAT and landed-cost attribution](packets/NEXT-54.md) |
| NEXT-55 | P1 | [Periodisk sammanställning with correction lineage](packets/NEXT-55.md) |
| NEXT-56 | P1 | [Customer advances, deposits and final-invoice application](packets/NEXT-56.md) |
| NEXT-57 | P1 | [Supplier advances and final-purchase settlement](packets/NEXT-57.md) |
| NEXT-58 | P0 | [Invoice-driven deferred revenue and service-period changes](packets/NEXT-58.md) |
| NEXT-59 | P1 | [Installment terms, partial due amounts and payment promises](packets/NEXT-59.md) |
| NEXT-60 | P1 | [Payment discounts and evidenced settlement differences](packets/NEXT-60.md) |
| NEXT-61 | P1 | [Receivable allowances, confirmed losses and later recovery](packets/NEXT-61.md) |
| NEXT-62 | P2 | [Dunning interest and enforceable reminder fees](packets/NEXT-62.md) |
| NEXT-63 | P2 | [Self-billed sales and buyer-issued invoice acceptance](packets/NEXT-63.md) |
| NEXT-64 | P1 | [Invoice payment links with outstanding-bound settlement](packets/NEXT-64.md) |
| NEXT-65 | P1 | [Scoped customer document and statement portal](packets/NEXT-65.md) |
| NEXT-66 | P2 | [Purchase commitments and three-way invoice matching](packets/NEXT-66.md) |
| NEXT-67 | P2 | [Commitment-aware budgets with stop and warn decisions](packets/NEXT-67.md) |
| NEXT-68 | P0 | [Versioned BAS chart adoption and controlled annual updates](packets/NEXT-68.md) |
| NEXT-69 | P1 | [Spreadsheet master-data import with staged reconciliation](packets/NEXT-69.md) |
| NEXT-70 | P0 | [Structured bank-statement ingestion with exact entry lineage](packets/NEXT-70.md) |
| NEXT-71 | P0 | [Bank-qualified payment exports and status reconciliation](packets/NEXT-71.md) |
| NEXT-72 | P0 | [VAT declaration submission and authoritative return history](packets/NEXT-72.md) |
| NEXT-73 | P1 | [AGI submission and stable individual correction outcomes](packets/NEXT-73.md) |
| NEXT-74 | P1 | [INK2 filing, signature handoff and assessment attribution](packets/NEXT-74.md) |
| NEXT-75 | P2 | [Accounting-method change with conserved recognition coverage](packets/NEXT-75.md) |

## Supporting material

[DECISIONS.md](DECISIONS.md) resolves the main financial distinctions. [solution-index.json](solution-index.json) carries all task metadata and conditional dependencies. [dependency-graph.json](dependency-graph.json) provides the acyclic new-wave order. [design-examples.json](design-examples.json) supplies compact exact expected values.

[CHECKS.md](CHECKS.md) and [checks/results.json](checks/results.json) report only local document/arithmetic checks. No OpenERP runtime, transaction, browser or provider was exercised by generating this package. No repository files were changed, no real company action was performed and no statutory/format release was activated.

The archive contains original design text, JSON metadata and a standalone checker. It does not contain cloned reference source, commercial chart text, statutory table bundles, credentials or font files. SHA256SUMS.txt identifies the final delivered bytes.
