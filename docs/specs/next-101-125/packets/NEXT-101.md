# NEXT-101: Accounting-firm delegation and multi-client workspaces

**Priority when applicable:** P1. **Owner lane:** IDENTITY.

**New scope:** NEXT-98 owns a period review. Add firm membership, client-granted scopes and a multi-client queue without turning a reviewer into a book administrator.

**Existing owner to extend:** Existing verified-principal admission, client memberships, capability registry and review engagements.

**Earlier contracts:** NEXT-50. **This-wave dependencies:** None.

**Conditional:** NEXT-98: a client delegates an accountant period-review engagement.

**Basis:** R02, R03, P98 in [SOURCES.md](../SOURCES.md). References identify requirements, prior designs or narrow external facts, not proof that a feature is missing or implemented.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed helpers bind to existing Effect/application owners. Do not create a second ledger, framework or stored-procedure workflow.

## Records and authority intersection

```text
FirmMembership {firmId, actorId, role, activeRevision, expiresAt}
ClientDelegation immutable {
  clientEntity, permittedBooks, firmId, grantedOperationFamilies,
  sensitiveDataScopes, periodBounds, permitsStaffAssignment,
  designatedStaffOrAssignmentPolicy, clientAuthorizer, revision, expiry
}
StaffAssignment {delegationId, actorId, permittedSubset, revision, active}
DelegationEvent immutable {grant | narrow | revoke | expire, evidence, recordedAt}
```

A client approves the firm's exact access envelope. Firm administrators may assign only the subset that envelope expressly permits. They cannot extend periods, add a book or turn read/prepare into signing/payment. Payroll and evidence access are separately named. Professional engagement acceptance is not technical delegation or authority to represent the company externally.

```text
resolveDelegatedAccess(actor, targetBook, operation):
  verify current actor credential and active firm membership
  resolve current client delegation and staff assignment
  allowed = operation in intersection(
      clientGrant, firmRole, staffAssignment, periodScope, sensitiveScope)
  require allowed and every layer unrevoked/unexpired
  return Principal(actor, viaFirm, delegationRevision, exactPermissionWitness)
```

Do not synthesize a permanent client operator token or copy firm membership into every client with broader grants. User identity remains the actual human, with delegation provenance appended. Nested domain operations use the resulting scoped principal through existing admission.

## Creation, revocation and lock discipline

An invitation alone creates no client access. The client authorizer chooses an explicit book and permission set, reviews it and activates it through the identity owner. Firm acceptance records contractual participation without widening that set. Initial activation is one client delegation at a time.

The root identity owner defines the lock ordering over credential, firm membership, delegation and assignment before book admission. Exclusive revocation uses that same authority hierarchy without acquiring a financial book lock afterward. If implementation needs new multi-row authority locking, prove the complete ordering before support. Do not bolt a book-first `revokeFirm` onto authority-first financial commands.

An admitted action holding the current authority locks can complete before revocation wins. Revocation that wins first blocks new admission. Already committed financial receipts survive removal of the firm's access; authorized client administrators retain them. A former firm member receives no continued access just because the receipt names them.

## Multi-client overview

```text
captureFirmQueue(actor, selection):
  obtain current authorized delegation IDs under firm identity scope
  fan out bounded, separate READ operations to each permitted client book
  retain book-specific contextId, cutoff, coverage and authorization revision
  aggregate only permitted counters/status summaries
  recheck active permission envelope before returning/retaining a shared view
  on scope loss, remove affected private content; do not return stale client names
```

Each book can have a different cutoff; display that fact. A dashboard is not a consolidated balance sheet. Do not hold a database transaction over every client or execute one cross-book financial batch. Optional firm-wide task actions are individual admitted client commands with separate receipts and partial-progress status.

## UI and operational result

Provide client grant/withdrawal, firm assignment, per-client outstanding tasks and an explicit scope switch. Query keys include firm actor identity, client entity/book and delegation revision. Changing clients cancels stale reads and cannot reattach an old mutation result to a new scope. Existing review98 still controls which period pack was accepted.

Client offboarding produces an inventory of retained review outputs and active delegated delivery jobs. Jobs reauthorize against current client permission; they cannot use a cached employee credential. Offboarding changes no financial balances or external authorizations by implication.

```text
client grants read+prepare; firm gives employee operator role -> still no approval
staff removed during queue capture -> no private client rows in new response
two clients both have invoiceId='x' -> queries remain book-scoped
firm action across10 clients fails on3 ->7 separate receipts, not global atomicity
review engagement accepted but delegation expired -> reads refused
```

Completion requires observed client-to-firm grant, staff use, scope reduction, revocation races and client switching through UI/API. This is a new collaboration control, not a replacement authentication provider.
