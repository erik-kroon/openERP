# Packet15 — approval-bound batch results and receipt recovery

Owner: `apps/api/src/application/period-work.ts`, composing the existing native
supplier/credit/owner/invoice dispatch ports, never posting batch totals itself.

## Implemented

- Progress omits unrecorded optional values. It no longer emits null where the
  shared REST/MCP schema permits only absent fields or actual values.
- REST/MCP read exact sealed batches and completed execution results by original
  command key. Reads do not prepare, approve, execute or change child state.
- Migration0057 retains immutable mixed execution results, linked to the batch,
  command receipt and actor. The native Effect/Drizzle owner returns the original
  result on exact replay, even after later chunks change run counts.
- Financial member commands still use their original stable owner keys. An
  aggregate-checkpoint failure leaves committed child receipts intact. Retrying
  recovers those receipts and retained refusal reasons instead of posting again.
- Missing aggregate results are not proof of nonexecution. Inspect child progress
  or retry the original command. An incompatible retry key/input remains refused.
- Existing operator-only preparation/approval/execution and per-owner fresh
  authority/dependency checks remain. Ordinary MCP gets read-only recovery tools.

## Observed proof

`test-results/period-batch-eight-acceptance-20261001` passes8/8 real
PostgreSQL/workerd E2E cases, zero skips/failures, stable source inventory
`7b9f4d9b8de1ea69c3a70706768318f5db9a65368c04ec83f78beb4c807081cd`.

Independent sources each assert10000 minor units. The mixed journey invalidates
one member account after exact approval: one voucher/10000 debit/10000 credit
commits, one member refuses stale. A real PostgreSQL P0001 fault prevents aggregate
checkpointing after child effects; the HTTP response is500 InternalError with
outcome-unknown classification. Aggregate lookup is then404 while the voucher
exists. Same-key retry reconstructs the mixed result; later replay and REST/MCP
lookup return exactly that result with one voucher, not a second effect.

A second journey removes the independent reviewer's membership after approval:
both native members refuse ApprovalRequired, zero vouchers. A third executes
two independent members over separate bounded ordinal chunks: two vouchers;
replaying the first chunk preserves its original committed count1 even when the
run has reached count2. A separate real fault refuses child checkpoint publication
after native posting; original-key retry recovers the owner receipt without another
voucher. Supplier-credit dispatch applies6000 against a10000 payable, retains one
credit and leaves4000 outstanding after replay. Owner-paid purchase dispatch uses
an independently authorized reviewer:10000 expense debit and10000 owner-liability
credit, with no company-cash line. Same-author owner approval correctly refused
before supplying that independent reviewer. Wrong approval digest, ordinary-agent approval,
foreign-book result read and incompatible execution replay all refuse.

Two additional journeys revise a retained supplier draft or cancel its manifest
after exact human approval. Revision refuses the affected member while the other
independent member commits; cancellation refuses both members with zero vouchers.
Neither stale selection is silently rewritten or widened.

Artifacts include exact batch/owner/receipt identities, literal expected controls,
bounded chunk results, reviewer refusal, migration/runtime manifest and unchanged
source inventory. Initial failures are preserved, including the optional-null
projection defect, missing read surfaces, and a fixture that correctly failed
duplicate-source recognition before its independent source bytes were corrected.

## Boundaries

This is real qualification of the retained supplier-recognition batch path and its
shared result lifecycle, not all dispatch families or whole-year acceptance.
The invoice dispatch port has no admitted domain route (`ownerForTarget` does not
return `commerce.invoice`); adding that route is not established by this batch proof.
Owner reimbursement/funding and general correction journeys remain separate work.
No financial owner guards were
relaxed, no source receipt was rewritten, and no real company/provider operation
was performed. Five whole packets are not established by this evidence.
