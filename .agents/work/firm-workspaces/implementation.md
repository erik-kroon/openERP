# Firm workspaces and explicit identity mapping

Working implementation record, 2026-09-23. Scope: finish the missing client/team workflow on the existing customer frame and make production identity provisioning concrete. No test files, dependencies, deployments, external invitations or messages are authorized by this task. Existing concurrent checkout changes are preserved.

## Caller and ownership

A signed-in human opens Firms, creates/selects a firm, links a book they can operate, and enters the same company workspace. Firm membership organizes work and does not grant financial book access. A client relationship carries a responsible firm member, a next review date and an internal note. A responsible member must also have access to that book. Team changes use existing provisioned identities. An explicit operator provisioning path owns identity/book grants; email similarity and firm membership never infer them.

`packages/contracts` owns the wire shapes; named PostgreSQL functions own scoped authorization, optimistic revisions, replay and persistence; Effect exposes them through the existing HTTP/MCP capability owners. TanStack Query owns the frontend reads and invalidation. Existing shared UI primitives own presentation.

## Alternatives and decision

1. Use an accessible-book list as the firm portfolio. Rejected: there is no persisted relationship, team boundary or client work context.
2. Let every firm member automatically inherit all client books. Rejected: joining a team would silently expand accounting authority.
3. Persist firm/team/client relationships and intersect every client read with live book membership. Selected: useful portfolio and handoffs without inventing financial grants. Separate explicit book access management remains authoritative.

OIDC is the selected production admission architecture. The actual provider/issuer is pending user input. No production credentials or external identity account will be created. Installed Better Auth 1.7.5 is the auth owner; provider subject mapping must be explicit and automatic email-based account linking must not confer authority.

## Failure contract before implementation

- An unauthenticated request, expired session or revoked identity cannot read firm data.
- Firm membership alone cannot reveal an ungranted client's books, summaries or notes.
- Client link and unlink require firm administration and current operation authority for the selected book.
- A responsible accountant must be an active firm member with current access to the linked book. Revoked memberships must not leave a selectable assignee.
- Team changes must not remove the final administrator, or allow an accountant to self-promote.
- Only existing provisioned human identities can be added. New email/domain matching must never bootstrap authority.
- Stale client or team revision cannot overwrite newer work.
- Same-request retries replay; the same key with a changed operation/payload is rejected.
- Firm mutations lock the firm before firm membership; book membership remains an independent authority check. Do not acquire a financial book barrier while changing authority.
- Requests have explicit list bounds. Unknown reads are not reported as zero or no access.
- Any production auth mode with incomplete provider configuration fails closed; local password sign-in remains available for the existing synthetic preview.
