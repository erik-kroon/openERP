# Changes from the SQL-owned dossier

Edition v2 rewrites all 25 packet files, the shared contract and the ownership map. It is not an amendment that must be mentally applied to the old files.

## Shared changes

Named Effect operations now own preparation, approval, execution and recovery. Typed persistence performs explicit reads/DML on the caller's transaction. PostgreSQL retains narrow relational and journal integrity only. Job dispatch uses application outbox intent and the separate effect-mq Bun worker. The clean pre-release baseline replaces the old feature migration/dispatcher architecture under ADR 0010's no-deployed-data condition.

Original financial equations, task IDs, bounded scope and the five WIP exclusions remain. Splitting the reusable line-credit compiler from unpaid-only counterpart selection makes the pre-existing NEXT-03/NEXT-07 reuse contract explicit; it does not change their amounts. External-source IDs in index metadata were aligned with the source dossier's actual registry where an old ID pointed to the wrong subject.

References to meaningful retained source or financial history remain preservation requirements. References requiring a disposable old-schema execution runtime were removed. New wording does not grant data reset, testing or financial authority.

## Per-packet rewrite record

### NEXT-01

Current review ownership is resolved by an application read over one shared snapshot. Ownership refusal moves to application execution.

### NEXT-02

Remove the superseded legacy-schema adapter requirement. Activation is an application-owned non-journal transaction.

### NEXT-03

Purchase journals, payables and tax facts are one application-owned DML group. Separate reusable line credit math from unpaid-only counterpart selection. Retained financial interpretation is preserved without a legacy-schema adapter. Unpaid credits use their own complete application execution; paid credits reuse line math only.

### NEXT-04

Replace permanent legacy runtime retention with explicit semantic versions. Retain meaningful snapshot history without preserving old dispatch. Add complete capture/compile/seal service with same-transaction WIP reads.

### NEXT-05

Cross-border recognition composes qualified purchase, FX/owner and tax writers on one tx.

### NEXT-06

Owner transfers, reimbursements and their counterparty effects share the caller tx.

### NEXT-07

Paid supplier credits keep payable release and refund increase atomic in application code. Refund receipt and its source usage share one app tx without new tax recognition.

### NEXT-08

Payment instruction release is a non-journal application transaction with domain dispatch fencing.

### NEXT-09

Use the selected persistent Bun job runtime rather than a Cloudflare workflow. Window claim is application-owned. Replace SQL publication transition with explicit application tx and outbox intent. Remove obsolete schema compatibility while preserving meaningful external provider history. Clarify transport lease versus domain publication fence.

### NEXT-10

Provider normalization persists in an application transaction. Bank admission composes the current intake app owner on one transaction.

### NEXT-11

Provide application-owned export capture and queued artifact lifecycle.

### NEXT-12

Historical adoption uses one application tx and does not re-recognize opening balances.

### NEXT-13

Remove implication that a legacy runtime is required. Add explicit capture/compile/persist statement service without SQL policy.

### NEXT-14

Move dimension policy to application admission. Preserve unknown source classifications without a disposable-schema interpreter. Replace SQL dimension workflow with app validation and narrow relational constraints. Use source-unknown dimensions rather than legacy-runtime assumptions. Define application journal/assignment composition on the caller transaction.

### NEXT-15

Legal credit issuance is a single app tx followed by outbox-driven rendering.

### NEXT-16

Use effect-mq delivery with separate persisted business versions. Separate public preparation transaction from durable run checkpoint recovery. Batch approval uses one app tx with owner-private approval functions. Apply clean-baseline scope to preparation compatibility. Retain late-handler and acknowledgment-loss domain recovery with effect-mq.

### NEXT-17

Foreign payable recognition is compiled into the purchase aggregate. Consume the released WIP pure calculator, without copying its algorithm. FX settlement consumes released WIP application ports with the same tx as journal and fees.

### NEXT-18

Valuation membership and all carrying deltas commit as one application group.

### NEXT-19

Use transaction-passing asset basis capture. Disposal uses the released asset app port and never independently commits a component.

### NEXT-20

Pay-run capture, pure calculation and sealing live in Effect, not SQL payroll logic.

### NEXT-21

Payroll postings and contribution reservations share one app transaction; outbox replaces inline enqueue. Unpaid payroll correction passes the same tx through reversal, replacement and payroll consequences. Make salary payment/reporting admission atomic and route native artifacts through Bun jobs.

### NEXT-22

Add explicit application execution of tax delta and queued declaration artifact generation.

### NEXT-23

Period policy belongs in the application without introducing context bypasses. Financial finalization performs journal, opening, certificate and lock DML in one app tx. Reopen is a separate application-owned transaction preserving downstream history.

### NEXT-24

Add application finalization plus explicit persistent-Bun native validation and attachment.

### NEXT-25

Acceptance inventories application owners plus narrow integrity rather than old feature functions. Rehearse the accepted clean baseline, not the retired procedural migration chain. Backups include app-owned interpretation. Include application and queue recovery inventories. Fence new persistent job runtime during restore. Require application transaction and effect-mq failure observations instead of SQL workflow proof.

## Coverage and remaining limits

Every individual packet was edited and now identifies an application owner, tx-passing persistence and its atomic scope. The pure financial algorithms and their examples were retained where ownership did not change. These are proposed pseudocode contracts, not runnable Effect code. No claim is made that actual exports match the illustrative method names or that all current application guards already implement this specification.

Source-based audit and arithmetic checks over this dossier are recorded separately in CHECKS.md. They do not execute the ERP, migrations, queues or provider integrations.
