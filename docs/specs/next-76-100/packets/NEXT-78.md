# NEXT-78: Milestone certificates and retained contract consideration

**Priority when applicable:** P1. **Lane:** SALES.

**New work:** Add delivered-milestone acceptance and retained amounts on customer contracts. Invoice installments split due dates; they do not prove a milestone occurred or that retention is unconditional.

**Use existing owners:** Existing sales agreement, acceptance evidence, invoice and installment owners.

**Required earlier contracts:** NEXT-51, NEXT-59, NEXT-76.

**Conditional integration:** NEXT-79 when selected work was already recognised as unbilled revenue or requires its qualified contract-asset treatment.

**Evidence basis:** R02, P59, P66. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Required distinctions

```text
Milestone {contractComponentId, acceptanceCriteria, contractualNet,
  evidenceRequirements, billableTrigger, retentionTerms}
AcceptanceRevision {milestoneId, completedQuantity, customerAcceptance,
  exceptions, effectiveDate, reviewedBy}
RetentionSlice {sourceInvoiceLine, amount, legalStatus:
  unconditional_debt_due_later | conditional_right, releaseConditions,
  expectedReleaseDate?, evidenceRefs, currentRevision}
```

Initial financial support covers an accepted fixed-price milestone and an enforceable invoice receivable with a retained amount due later. If payment remains contingent on additional performance such that no unconditional debt exists, refuse that AR branch; use NEXT-79's separately qualified contract-asset treatment when available. Calling every withheld amount an installment would overstate receivables.

## Billing proposal

```text
prepareMilestoneInvoice(milestone, acceptance):
  require actual acceptance/entitlement evidence and unused milestone coverage
  gross = qualified net + VAT from existing invoice compiler
  retention = exact contractually supported amount, not a discretionary rounding remainder
  require 0 <= retention <= gross
  dueNow = gross-retention
  freeze milestone coverage + invoice semantic lines
  create due components(dueNow, retainedAmount) through installment owner
```

The chosen tax profile establishes the tax point independently. A retained cash amount does not automatically postpone VAT or reduce the invoiced supply. Recognition follows the revenue profile, not the date the customer releases retention.

One tx creates/reserves the milestone-linked draft. Issue atomically consumes milestone/order coverage and records the invoice and due components. If revenue was already recognized from this performance, consume the corresponding NEXT-79 recognition rights inside that issue tx; do not post the same revenue twice.

## Retention release and disputes

```text
releaseRetention(retentionId, proof):
  require current contract condition, acceptance and independent approval
  require retained invoice slice still outstanding
  reclassify its due status/date in the installment owner
  append release evidence and receipt, no new invoice/revenue/VAT
```

A revised expected date used by Cash does not itself satisfy legal release conditions. A paid retained amount consumes its existing AR slice. A dispute reduces collectible status or adds a hold, not the legal invoice principal. A negotiated price reduction uses the normal credit owner with original-line capacity.

If a mistaken release has already been paid, do not reverse the cash to restore a future due date. Record a linked correction or refund obligation only when evidence and the selected profile justify it.

## Visible workflow and vectors

The milestone screen shows acceptance, issued amount, immediately due balance, retained balance, release evidence and actual settlement independently. Contract totals and Cash use one underlying obligation identity and cannot add a retention twice.

```text
net100000 VAT25000 gross125000; retention12500 -> dueNow112500 + retained12500
release12500 -> AR total unchanged, revenue/VAT delta0
unaccepted milestone -> cannot issue from the accepted-milestone path
retention already paid -> release changes no cash balance
```

Completion requires two-stage collection and credit/currentness behavior against actual application owners. It does not add a construction-industry legal profile by default.
