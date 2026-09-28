# NEXT-96: Multi-human approval routing and segregated review policies

**Priority when applicable:** P1. **Lane:** AUTHORITY.

**New work:** Add finite, versioned multi-reviewer routing for exact plans. Existing human approvals remain the financial authority; this is not unattended posting or an agent mandate.

**Use existing owners:** Current principal/role admission, exact approval records, task routing and final operation execution owners.

**Required earlier contracts:** Existing core operation owners.

**Conditional gates:** NEXT-67: budget classifications contribute to routing only, not permission to hide liabilities.

**Evidence basis:** R04, P16. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## Policy, not a new financial interpreter

```text
ApprovalPolicyRevision {book, operationFamily, effectiveScope,
  exactRiskMeasure, thresholds, requiredRoleSlots, distinctHumanRules,
  conflictRestrictions, expiry, delegationRules}
ApprovalCase {planId, planDigest, policyRevision, riskBasis,
  slots:[{role, eligibleScope, decision?}], currentState}
ApprovalDecision {caseId, slotId, humanId, approve|reject, digest,
  currentMembershipWitness, recordedAt, supersedes?}
```

Routing depends on the actual operation's risk measure, not merely net journal total, which is always zero. For a payment batch, use gross approved disbursement; for a credit, use the affected claim reduction. Cross-currency threshold conversion requires a pinned reviewed policy and exact rate basis; otherwise refuse. A plan cannot be split into artificial fragments to evade a rule that explicitly covers one business request aggregate.

## Select and collect

```text
openApprovalCase(plan):
  choose exactly one applicable qualified routing policy
  derive risk and required slots from retained plan effects
  require enough currently eligible distinct reviewers or return UnstaffedPolicy
  persist case bound to exact plan+policy digests

recordDecision(case, slot, human):
  authorize current private/book role; lock case and declared authority resources
  require plan and policy still applicable and exact digest unchanged
  reject self-approval/conflicts required by the policy
  append immutable decision; never let one human fill two distinct-person slots
  reevaluate rejection/quorum state, save receipt
```

A delegate must be explicitly eligible for the slot under the same restrictions. Delegation does not copy the previous person's signature or bypass independence. A source/model suggestion can notify a reviewer but cannot fill a slot.

## Execute through the existing owner

An approval case reaching quorum is not itself a posting. It provides a supported approval-set reference to the ordinary named operation. At execution that owner rechecks exact plan binding, every required nonrevoked decision, current membership/role eligibility and expiry under the root lock protocol. A person losing authority before consumption can invalidate the quorum. Same-key recovery of an already committed result remains possible under current requester access, even if a former reviewer later leaves.

If the current single-approval schema cannot express the set, root introduces one explicit new supported approval contract/version. Do not fake quorum by having a service account mint the old single-human approval. No blanket shared policy engine gets raw arbitrary ledger writes.

## Change and UI

A material plan change requires a new case over a new digest. A policy change has explicit effective scope: urgent retroactive revocation can stop unexecuted cases, but it cannot undo a committed receipt. Historical decisions remain readable. Rejection and withdrawal are append-only, not deletion of an inconvenient review.

UI shows required roles, eligible assignees, conflicts, exact financial content and missing decisions. The amount explained to reviewers is the same risk basis used to select the policy.

```text
policy requires preparer-excluded finance+director, distinct humans
one person with both roles -> cannot supply two signatures
payment total1200000 in two legs600000 -> route by1200000, not each leg
reviewer revoked before execute -> unconsumed case loses valid quorum
committed command replay after reviewer exit -> same receipt, no reapproval/reposting
```

Complete one real operation family end to end before broadening. This packet does not grant agents approval rights or create standing execution budgets.
