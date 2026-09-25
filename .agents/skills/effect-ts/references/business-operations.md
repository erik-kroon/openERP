# Business operation rules

Use these rules when building company/book access, financial mutations, retryable commands, or background work. They adapt the four Sellfinity lessons to OpenERP. They are implementation guidance, not a claim that a capability exists or has been verified.

The maintained [domain model](../../../../docs/domain.md), [operation contract](../../../../docs/operations.md), and [posting decision](../../../../docs/adr/0002-exact-posting-and-approval.md) own accounting meaning. Reuse their contracts and existing code; this reference does not create a second model or require a generic framework. The [application-owned replacement decision](../../../../docs/adr/0010-application-owned-accounting-replacement.md) owns the current trust boundary and caller cutover. It keeps the financial requirements but removes the old feature-function dispatcher and compatibility path. PostgreSQL owns only the reviewed DDL, constraints, grants and narrow integrity layer; application operations own authorization, policy, calculations and scoped writes. Financial transactions use no session-level tenant context or advisory locks. Durable handlers call the same application operations through the selected effect-mq Bun path in [ADR 0009](../../../../docs/adr/0009-effect-mq-background-jobs.md), which owns queue claims, retries and leases rather than accounting truth.

## Keep each company's data separate

Establish identity from a trusted session or credential. Resolve current membership and permission on the server. A selected company, book ID, browser role, or hidden button does not authorize an operation.

- Verify that the requested book belongs to the requested legal entity and that the actor can perform the specific action in that book.
- Scope reads before filtering, counting, pagination, aggregation, or export. A total or search result can disclose another company's data even when individual records are hidden.
- Scope related records as well as the root record: evidence, accounts, plans, approvals, receipts, and jobs must belong to the same authorized book. Enforce persisted relationships with the owning database constraints.
- Recheck authority at the mutation boundary. Use the established transaction and lock order so a permission check cannot become stale while the operation waits to write. Do not retain a stale role snapshot as permanent authority.
- Give background workers only the operations and resources they need. A queued job does not preserve a user's revoked access or let infrastructure impersonate an unrestricted user.
- Include entity/book identity in TanStack Query keys. On identity or book changes, cancel relevant pending requests and clear or partition sensitive cached records and local drafts so the previous context cannot reappear.

Concrete check: changing an authorized request's book or evidence ID to another company's ID must not expose a record, affect a total, or write anything. Removing permission must affect later requests, including receipt reads and queued execution where that permission is required.

## Make repeated requests safe

Give each logical command a stable request identity. Store its scoped identity, normalized request fingerprint, and result durably. Include the operation, relevant actor context, target, and immutable content/version references in the identity check.

- The same scoped key and matching request returns the recorded result. Reusing that key for different content or an operation conflicts explicitly.
- Serialize competing uses of the key with the established database transaction/locking mechanism and a uniqueness constraint. A read-then-insert check alone cannot prevent concurrent duplicates.
- Commit the financial mutation, approval consumption, numbering, receipt, and required outbox admission in one transaction. Failure rolls back the whole group.
- Preserve the same identity after a timeout or lost response. An uncertain response is not proof that the write failed. Retrieve the receipt or repeat the same command; do not create a fresh key as an automatic retry strategy.
- If the UI supports resuming after navigation or restart, retain a safe operation reference that can recover the server result. An in-memory map alone cannot provide that guarantee. Keep credentials out of persisted recovery metadata.
- Recheck current permission before returning a receipt. A completed replay returns its original outcome without consuming another approval or requiring the already-consumed approval to become unused again.

Request deduplication and business uniqueness solve different problems. A new key must still not post the same semantic accounting effect twice. Preserve the book/event/posting-purpose/occurrence identity required by the domain model.

Approve immutable proposed effects. Execution loads that stored revision and digest, checks the relevant dependencies, and rejects stale approval; it never accepts replacement journal lines under an old approval.

Concrete check: lose the response after commit, then repeat the request. There must be one posting and the original receipt. Changing the payload under the same key conflicts; changing a relevant dependency before execution rejects the approval.

## Remember unfinished jobs

Use a persisted job or operation record when work must survive a Worker restart. An Effect fiber, timer, `forkDetach`, or `waitUntil` alone is not durable admission. If a domain write requires later work, record that work in the same transaction as the write.

- Add a job only for a real producer and consumer. An outbox table without dispatch, handling, recovery, and an observable result is not a working background feature.
- Store stable scoped IDs, progress, attempts, next eligible time, and bounded diagnostic outcomes. Fetch sensitive content from its authorized owner when needed; do not copy credentials or document bodies into orchestration metadata.
- Use one authority for claims and execution ownership. If the existing queue owns leases, use its mechanism. For database-owned claims, make claiming atomic and require the current lease token for renewal, completion, and failure updates.
- Permit reclaim after lease expiry. Reject a stale worker's completion after another worker acquires the job. Keep attempt limits and retry delays explicit; retry only failures the operation classifies as transient.
- Keep failed or exhausted work visible and recoverable through an authorized action. Do not silently drop it or mark a job complete merely because it was scheduled.
- Keep the accepted financial result separate from later delivery. Failed notification or export delivery does not undo or repost the voucher.

External effects need reconciliation as well as local receipts. The provider may succeed just before a connection drops or the worker stops. Reuse a stable provider idempotency key where supported, or look up the remote operation before resending. When its outcome cannot be established, expose an unknown/conflict state and the required recovery action; do not claim exactly-once external delivery.

Show useful progress through the owning operation's states: waiting, working, completed, retry scheduled, or needing attention. These are meanings to represent in the domain contract, not an instruction to add a second generic status system.

Concrete check: stop a worker after it claims work and before completion. Another worker must resume after expiry without accepting the old worker's claim or repeating a confirmed external effect. Exhausted retries must remain visible for recovery.

## Calculate money consistently

Keep one owner for each monetary calculation and use its result in the API, UI, posting, and generated documents. Pure exact calculations remain synchronous and independent of Effect, React, and provider clients.

- Use the shared contract's canonical integer strings for posted minor units and carry the currency explicitly. Convert to `bigint` or an appropriate exact representation for arithmetic; do not pass large values through JavaScript `number`.
- Take currency scale from the book/profile metadata. Do not assume every currency has two decimal places.
- Keep rates, fractional quantities, original-currency values, and intermediate amounts in exact decimal or rational form until a named rounding boundary.
- Define the rounding mode, precision, treatment of ties and negative values, and whether rounding happens per line or at the total. Preserve the relevant rule/profile version with the result. Do not infer these choices from Sellfinity's limited order calculator.
- Reject invalid precision and out-of-range values before storage coercion. A numeric column that rounds on insertion does not prove the input was valid integer minor units.
- Require debit and credit totals to agree exactly. A floating-point tolerance cannot repair an unbalanced posting. Model legitimate rounding differences explicitly under the applicable accounting rule.
- Allocate fractional remainders deterministically so installments or splits conserve the original amount. Corrections use the stored original amounts and append the required linked effects.

Formatting is presentation. Do not parse a formatted display string back into the calculation, use `toFixed` as the calculation policy, or recalculate an approved result from mutable inputs in the browser.

Concrete check: splitting 100 minor units into three allocations must still total exactly 100 under the selected remainder policy. Values beyond JavaScript's safe integer range must retain every digit. Invalid fractional minor units must fail before they can be rounded into a valid posting.

## Verification scope

Use the concrete checks above to identify the real caller and failure outcome worth observing. Exercise existing authorized application/database paths and report the evidence. These scenarios do not authorize new test files, fixtures, or helpers. Keep implementation, observed behavior, and remaining provider/runtime uncertainty distinct.
