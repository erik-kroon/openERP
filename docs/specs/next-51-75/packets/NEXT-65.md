# NEXT-65: Scoped customer document and statement portal

Priority: **P1 when applicable**. Lane: **COMMERCE-UX**.

**New deliverable:** Let a customer view exact issued documents and a frozen statement through revocable scoped access. Existing accountant book access and artifact rendering do not provide this external customer workflow.

**Existing owner to extend:** Existing immutable document/statement artifacts, customer identity, access and delivery owners.

**Required contracts:** NEXT-13, NEXT-30. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-59: Portal displays installment-level due amounts and payment promises. NEXT-64: Portal offers a separately authorized payment link.

**Crosswalk:** PRY-53; canonical family COM-05/06, FE, OPS. Customer-facing constrained artifact/current-balance access is not general book access.

**Atomic result:** No financial writes; exact authorized customer artifact/current-data views.

**Evidence:** R03, R05, R06 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Narrow sharing manifest

Create `CustomerShareGrant` with issuer book, reviewed recipient, selected document IDs or customer statement scope, expiry, token hash, revocation version and allowed actions. Store only a hash of a cryptographically random bearer token. Prefer an authenticated recipient binding for sensitive multi-document portals. Link possession never grants general book-list, search, payroll, supplier, reviewer or accounting-write capability.

`StatementShareArtifact` pins the same native invoice/credit/payment residual snapshot and as-of/recorded cutoff used by the statement owner. It contains exact issued identities, terms and payment applications. Future payments change a new statement, not old shared bytes.

## Share and read

```text
prepareCustomerShare(selection,recipient):
    current operator access; prove every selected artifact belongs to this customer scope
    require issued/allowed document kinds, not internal review materials by default
    bind exact artifact hashes, frozen statement basis and expiry
    record approved share manifest and revocation head
    retain outward-delivery intent separately if a message is sent

readSharedArtifact(token,artifactId):
    resolve current grant by token hash in trusted server scope
    verify unexpired/unrevoked grant and optional recipient authentication
    require artifactId in the retained allowed manifest
    return exact stored bytes and minimal metadata
    do not rerender from current logo, address, tax settings or invoice totals
```

A direct object URL must not bypass future revocation. Use a mediated download or a deliberately short-lived signed URL with an explicitly disclosed revocation window. Revocation cannot erase bytes a recipient already legitimately obtained; do not promise it can.

## Current versus historical views

The default portal displays immutable document history and labels each statement's cutoff. A separately requested current outstanding view is generated through the native residual owner under the grant's permitted scope, with current data clearly separated from frozen statement values. It must not silently replace an invoice's printed original amount with the amount still due.

A payment promise is a proposed claim from the customer requiring the existing collection policy and authenticated scope. It is not payment evidence or a ledger mutation. NEXT-64 checkout links are optional actions over the server-selected invoice/instalment intent, not arbitrary amounts accepted from the page.

The customer cannot discover the existence of another party's artifact by guessing IDs. Guest errors should avoid disclosing denied names or numbers. Access audit records describe grant/artifact activity without placing credentials or sensitive document contents in logs.

## Cancellation and delivery evidence

Expiry or revocation changes only sharing eligibility. It does not cancel an invoice, reverse a payment or delete retained accounting evidence. Sending a link records delivered content/destination through the existing transport owner; a successful link page view does not prove the customer accepted the invoice legally.

A corrected document is another legal artifact with explicit relationship and its own inclusion decision. A broad grant that automatically includes future artifacts requires an explicitly reviewed bounded policy; the initial slice uses an exact static manifest.

## Complete workflow

UI supports selection, recipient preview, expiry, revoke, guest statement/document navigation and return to the exact shared list. Use accessible layouts and localized dates/amounts without changing semantic bytes. The guest has no accounting sidebar because no general book scope was granted.

Synthetic original invoice100000, shared statement residual80000 at T1 and later payment30000: original invoice stays100000; T1 statement stays80000; new authorized current view shows50000. Revocation blocks new mediated reads but does not erase the retained artifacts.

Finish with actual guest views/downloads, another-customer refusal, expiry/revocation, a changed current balance and recovery of the original shared bytes after application restart. An unsigned public bucket link is not the packet.
