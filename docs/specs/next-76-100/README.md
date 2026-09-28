# OpenERP NEXT-76 through NEXT-100

**25 new application-owned work packets with implementation-level pseudocode.** This wave supplements NEXT-01..75, with explicit new scope and dependencies. It does not assume the preceding 75 are done.

Planning checkpoint: `66355b62b23e3b8007c2d324f3739fbbcc96cdc0`, 28 September 2026. The attached 51..75 dossier was read for scope and architecture. Current repository reading was targeted to plans, operations and the candidate entry point. No complete source audit or runtime qualification is claimed.

## Use

Coordinator: [MASTER-PSEUDOCODE.md](MASTER-PSEUDOCODE.md), [COORDINATOR-HANDOFF.md](COORDINATOR-HANDOFF.md) and [INTEGRATION-MAP.md](INTEGRATION-MAP.md).

Worker: its individual packet plus [00-COMMON.md](00-COMMON.md), [01-QUALIFIED-INPUTS.md](01-QUALIFIED-INPUTS.md) and [SOURCES.md](SOURCES.md). Proposed names bind to actual existing owners; do not build a new framework to reproduce the notation.

## Packet index

| ID | Priority when applicable | New deliverable |
|---|---|---|
| NEXT-76 | P1 | [Accepted contract changes and sales-order billing limits](packets/NEXT-76.md) |
| NEXT-77 | P1 | [Time-and-materials billing with once-only work coverage](packets/NEXT-77.md) |
| NEXT-78 | P1 | [Milestone certificates and retained contract consideration](packets/NEXT-78.md) |
| NEXT-79 | P1 | [Earned but unbilled service revenue and later invoicing](packets/NEXT-79.md) |
| NEXT-80 | P1 | [Supplier disputes with partial payment holds and release](packets/NEXT-80.md) |
| NEXT-81 | P1 | [Asset work-in-progress and commissioning from purchase costs](packets/NEXT-81.md) |
| NEXT-82 | P2 | [Component replacement, improvements and partial asset retirement](packets/NEXT-82.md) |
| NEXT-83 | P2 | [Operating-rental contracts, refundable deposits and index changes](packets/NEXT-83.md) |
| NEXT-84 | P2 | [Book-to-tax depreciation cohorts and excess-depreciation bridge](packets/NEXT-84.md) |
| NEXT-85 | P2 | [Periodiseringsfond cohorts, reversals and annual tax linkage](packets/NEXT-85.md) |
| NEXT-86 | P2 | [ROT/RUT split claims and customer-authority settlement](packets/NEXT-86.md) |
| NEXT-87 | P2 | [Pension invoice reconciliation and SLP annual basis](packets/NEXT-87.md) |
| NEXT-88 | P2 | [Employment termination and final-pay obligation closure](packets/NEXT-88.md) |
| NEXT-89 | P2 | [Dividend resolutions, shareholder payables and KU31 preparation](packets/NEXT-89.md) |
| NEXT-90 | P2 | [Conditional grants, earned funding and repayment obligations](packets/NEXT-90.md) |
| NEXT-91 | P1 | [Apply supplier credit balances to other payable invoices](packets/NEXT-91.md) |
| NEXT-92 | P2 | [Documented bilateral receivable-payable setoff](packets/NEXT-92.md) |
| NEXT-93 | P1 | [Source-located evidence search and retained-page retrieval](packets/NEXT-93.md) |
| NEXT-94 | P1 | [Read-only mailbox intake and scoped attachment routing](packets/NEXT-94.md) |
| NEXT-95 | P1 | [Counterparty balance confirmations with independent evidence](packets/NEXT-95.md) |
| NEXT-96 | P1 | [Multi-human approval routing and segregated review policies](packets/NEXT-96.md) |
| NEXT-97 | P1 | [Exact covering-set reconciliation with explicit ambiguity](packets/NEXT-97.md) |
| NEXT-98 | P1 | [Accountant period-review engagements and versioned acceptance](packets/NEXT-98.md) |
| NEXT-99 | P1 | [Cash forecast vintage scoring and error attribution](packets/NEXT-99.md) |
| NEXT-100 | P1 | [Scoped integration event subscriptions and delivery receipts](packets/NEXT-100.md) |

## What is delivered

Each packet specifies owned records, exact decisions/calculations, transaction composition, corrections, downstream controls, UI/API behaviour and concrete acceptance cases. Qualified legal tables, company facts and real provider access remain explicit inputs. Hypothetical examples are not current statutory rates.

The [decisions](DECISIONS.md) and [machine-readable index](solution-index.json) make the cross-packet boundaries explicit. [checks/results.json](checks/results.json) and [CHECKS.md](CHECKS.md) report local dossier validation only. [design-examples.json](design-examples.json) retains compact independently checked examples. Source and file hashes are supplied for reproducibility.

No application code, database patch, external submission or real company posting is included. A pure module alone does not complete any packet. All current WIP/source owners and test-change permissions remain in force.
