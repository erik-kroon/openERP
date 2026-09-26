# OpenERP NEXT-01 through NEXT-25: Effect application-owned edition

**Use this v2 package instead of the previous SQL-owned pseudocode package.** The original 25 task IDs and financial scope are preserved. Every packet's implementation instructions now target Effect application operations and transaction-passing persistence.

Start with [MASTER-PSEUDOCODE.md](MASTER-PSEUDOCODE.md) for the coordinator. For an individual agent provide [00-COMMON.md](00-COMMON.md), [01-RULE-AND-FORM-DATA.md](01-RULE-AND-FORM-DATA.md) and its assigned packet below. [INTEGRATION-MAP.md](INTEGRATION-MAP.md) names dependencies and reserved handoffs. [CHANGES.md](CHANGES.md) explains what was rewritten.

This is a source-grounded design rewrite, not a fresh repository audit or an applied implementation. Architecture context comes from the supplied amendment at `422276ae5ed9d0ca146447d92bb3d27c99f8c48a`. Earlier task evidence is pinned at `bb628452196a55ceef7516f76fc3cd6471ae4d91`. Current local WIP remains unobserved.

## Coordinator instruction

> Implement the assigned NEXT packets from this application-owned v2 specification. Read current AGENTS.md and ADR 0010/0009 first. Retain financial meaning and task identity, but use named Effect operations, pure domain calculations and explicit tx-passing persistence. Keep SQL limited to schema, grants, keys and narrow integrity. Use the existing internal journal owner and the effect-mq Bun composition. Do not rebuild retired feature procedures, nest financial transactions or take over any of the five reserved workstreams. Reconcile actual exports and file ownership before coding, then provide the implementation and observed evidence for the complete supported workflow.

## Packet index

| ID | Priority | Solution |
|---|---|---|
| NEXT-01 | P0 | [Owner-aware case review](packets/NEXT-01.md) |
| NEXT-02 | P0 | [Capability-specific company admission](packets/NEXT-02.md) |
| NEXT-03 | P0 | [Domestic purchasing with owned tax recognition](packets/NEXT-03.md) |
| NEXT-04 | P0 | [Actual domestic VAT return and controls](packets/NEXT-04.md) |
| NEXT-05 | P0 | [General-rule cross-border service purchases](packets/NEXT-05.md) |
| NEXT-06 | P0 | [Owner-paid expenses, reimbursement and funding](packets/NEXT-06.md) |
| NEXT-07 | P1 | [Supplier paid credits and refunds](packets/NEXT-07.md) |
| NEXT-08 | P1 | [Payment instruction resolution and replacement](packets/NEXT-08.md) |
| NEXT-09 | P1 | [Complete Plaid sync windows](packets/NEXT-09.md) |
| NEXT-10 | P1 | [Provider revisions to reviewed bank observations](packets/NEXT-10.md) |
| NEXT-11 | P0 | [Separate complete-book SIE4E export](packets/NEXT-11.md) |
| NEXT-12 | P1 | [Historical open-item adoption](packets/NEXT-12.md) |
| NEXT-13 | P0 | [Semantic P&L and balance-sheet snapshots](packets/NEXT-13.md) |
| NEXT-14 | P2 | [Original dimension assignments](packets/NEXT-14.md) |
| NEXT-15 | P1 | [Legal customer credit notes](packets/NEXT-15.md) |
| NEXT-16 | P0 | [Evidence-aware period preparation](packets/NEXT-16.md) |
| NEXT-17 | P1 | [Payable FX and explicit fees](packets/NEXT-17.md) |
| NEXT-18 | P1 | [Incremental open-item FX remeasurement](packets/NEXT-18.md) |
| NEXT-19 | P1 | [Disposal with proceeds](packets/NEXT-19.md) |
| NEXT-20 | P2 | [Frozen regular-payroll calculation](packets/NEXT-20.md) |
| NEXT-21 | P2 | [Payroll posting, payslip and AGI artifact](packets/NEXT-21.md) |
| NEXT-22 | P1 | [Pre-close tax bridge and INK2/SRU](packets/NEXT-22.md) |
| NEXT-23 | P1 | [Financial close and single-count carry-forward](packets/NEXT-23.md) |
| NEXT-24 | P1 | [K2 annual-report semantic model and iXBRL](packets/NEXT-24.md) |
| NEXT-25 | P0 | [Fixed-revision company rehearsal and restore](packets/NEXT-25.md) |

## Delivery boundaries

Pseudocode functions and paths are proposed contracts. Implement them using the actual current owners rather than copying names as if they already existed. Keep all five WIP assignments reserved; historical migration numbers are provenance only. Missing legal tables, profile facts or provider credentials remain explicit inputs, not fabricated defaults.

The package contains no copied application source, database patch, deployed change, tax-table bundle or font files. Design checks do not override repository restrictions on tests. Financial actions and external submissions remain separately authorized.

See [CHECKS.md](CHECKS.md), [SOURCES.md](SOURCES.md) and [solution-index.json](solution-index.json).
