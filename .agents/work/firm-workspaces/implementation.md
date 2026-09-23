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

## Implemented behavior

- `/firms` now owns the firm picker, client portfolio and team. Client search, assigned-to-me, review-due and unassigned filters use the authorized result. Visible rows show current period, responsible person, review date, work count and its observation time. Ten rows load period/work observations at a time. Company links enter the existing scoped workspace.
- A firm administrator creates client links and manages already provisioned people. Current book operators in the firm can update an existing client handoff; linking and unlinking still require firm administration. This distinction lets accountants do daily work without receiving team-management authority.
- OIDC authorization-code/PKCE configuration is wired through Better Auth, the browser sign-in control and deployment bindings. The provider namespace includes exact issuer and application registration; immutable `sub` maps to the approved actor. Signup and linking stay disabled. Provider discovery is excluded from routine session reads.
- `provision-identity.ts plan|apply` validates a reviewed manifest and applies immutable identity mapping and explicit company/book grants with expected-role checks, an audit receipt and session revocation. Disabled identities retain their binding and cannot obtain usable sessions or accounting access.
- The local preview uses `frontend_20260923_ui2`, API 18790 and web 3107. Synthetic firm `firm_a15959e5b9e04443b2debc387923ea75` links `book_customer_demo`, with `actor_firm_colleague` responsible. No hosted identity, production permission or external message was created.

## Observed results

JSON artifacts in this folder retain the local API observations:

- `observations.json`: create/link and identical replay return 200; stale revision and changed-payload request key return 409; removing the last administrator returns 422.
- `isolation.json`: a nonmember receives 403; after joining the firm without book grants, the colleague receives a valid firm with zero clients. Direct book access and self-promotion both return 403.
- `admission-observations.json`: reviewed provisioning and identical replay succeed; a book grant makes exactly one client visible and allows the accountant handoff. Old sessions return 401 after grant/revoke. Stale expected roles and identity rebinding fail without applying. A removed book disappears. Disabling the identity rejects existing sessions and new sign-in. The local password endpoint returns a generic 500 when the session-admission trigger rejects creation; no session is admitted. The real OIDC error callback remains unverified.
- `firm-revocation.json`: removing firm membership returns 200, then firm reads return 403 while the independently granted book remains readable. The removed lead becomes unavailable. The synthetic membership was restored.
- `oidc-configuration.json`: local password configuration succeeds; production configuration without a provider fails; attempting production password mode fails; complete synthetic OIDC configuration validates. Different issuer/application registrations produce different provider namespaces. This is configuration validation, not a live OIDC login.

Browser observations: firm/client/team rendering; compact picker/filter layout; named client and member forms; client note save and reopen; team save with disabled fields and visible pending state; team return after completion; search empty state; assigned-to-me exclusion for a client assigned to the colleague. The final portfolio retains readable columns with horizontal overflow at a constrained panel width. No tests or fixtures were added. Root lint, type checks, build, owned-file formatting and diff whitespace checks are recorded in the final verification manifest.

## Replay outline

1. Apply all migrations to a disposable database, provision one synthetic operator/book and sign in through the local password mode.
2. Create a firm through `/api/v1/firms`; link that operator's book with expected revision 0. Repeat the same request key/payload, then try an altered payload and an old revision under a fresh key.
3. Provision a second synthetic human with the reviewed identity command and no book grants. Add the person to the firm. Compare their firm client list and direct book response with the first operator's.
4. Apply an explicit book grant with expected role null. Confirm the old session fails, sign in again, and update the client as the accountant. Revoke the book with expected role operator, then repeat the read. Disable and re-enable the same immutable identity through separate reviewed requests.
5. Remove and restore the second person's firm membership, confirming independent book access and lead availability. Open `/firms`, save/reopen a note, save a team member and use the client filters.

## Interface polish review

Full mode, bounded to the new firm screens, firm forms, sign-in mode selection and the table-width extension. React/TanStack Query with owned StyleX primitives. Existing financial screens and provider-hosted screens are outside this review.

| Category | Evidence | Result |
| --- | --- | --- |
| Typography | Client/team screenshots; owned record headings, table cells and caption styles | Readable column widths retained; existing type system reused |
| Surfaces | Client modal, team modal, picker/filter rows, pending save state | Existing dialog radii/elevation and structured table borders reused |
| Animations | New render paths and owned button/tab primitives | No custom entrance or per-row animation added; no new motion to replay at 10% |
| Icons | Firm/company navigation | Existing Lucide icons, currentColor and consistent regular-text stroke |
| Performance | Query owners, visible-row observations and rendered pending state | Bounded server results; only ten clients request period/work details per page |

| Severity addressed | Location | Before | After | Why |
| --- | --- | --- | --- | --- |
| HIGH | `apps/web/src/components/firms/index.tsx` and firm contracts | Accessible books had no firm/team relationship | Persisted client and team boundaries intersect book permissions | Visible context must represent actual authority |
| MEDIUM | `apps/web/src/components/firms/client-dialog.tsx`, `team.tsx`, `form.tsx` | No firm handoff or team commands | Named bounded forms, revision feedback and disabled pending controls | Make the action and its outcome clear |
| MEDIUM | `apps/web/src/components/firms/index.tsx`, `portfolio.tsx` | Select controls stretched across the page | Owned compact filter wrappers | Preserve hierarchy and useful density |
| MEDIUM | `packages/ui/src/components/data-grid.tsx`, `data-table.tsx`, firm portfolio | Six columns could break headers and dates into fragments | Opt-in wider minimum table width with contained scrolling | Keep structured information readable |
| MEDIUM | `apps/web/src/components/accounting-access.tsx` | Password-only sign-in UI | Configured organization sign-in, local password mode and unavailable/error feedback | Present the admission method the server actually supports |

Considered and rejected: automatic client grants for firm members (silently expands financial authority); a new branded dashboard/card system (existing company frame already owns hierarchy and density); animated portfolio row entrances (repetitive accounting work needs stable feedback).

Verdict: inspected firm interactions are usable and locally verified. Not verified: live OIDC callback/provider MFA, production roster acceptance, animation slow playback of unchanged shared primitives, deployment, or a broad mobile/accessibility audit. No production-readiness claim follows from the synthetic observations.
