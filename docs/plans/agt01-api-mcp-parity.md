# AGT-1 API and MCP parity inventory

Status: source inventory at this revision, not observed transport acceptance. D-05 remains open until real authenticated REST and MCP calls, including failed writes and recovery, are captured at a fixed revision.

## Supported surface and exceptions

| Surface | Executable source of operation inventory | Admission / result |
| --- | --- | --- |
| REST | `packages/contracts/src/api.ts` and its imported area API groups; `apps/api/src/transport/http/routes/` registers handlers | Generated `/api/openapi.json` describes request, success and accounting-error schemas. REST resolves scoped session or bearer authority and validates payloads through Effect Schema. |
| MCP | `Object.entries(capabilities)` in `apps/api/src/transport/mcp.ts`, backed by `apps/api/src/application/capabilities.ts` and `packages/contracts/src/capabilities.ts` | `tools/list` generates each input/output JSON Schema from the same capability contract. `tools/call` validates excess input fields, executes the same owning capability, and returns `{ result }` as structured content. Tool errors carry the accounting code and message in `isError` content. |
| Human-only / operator | REST `approveChange` in `apps/api/src/transport/http/routes/accounting.ts`; other operator or identity commands are not automatically exported to MCP | Human approval cannot be minted by an agent tool. An agent can prepare and execute only under its existing backend grants and an independently approved exact plan. |

This is **shared-operation parity**, not a promise that every REST endpoint has an MCP tool: REST-specific operator actions and HTTP-only provider/bootstrap surfaces are intentional exceptions. Derive the current tool names from authenticated `tools/list`; do not copy a static count into client code. Newly registered REST operations do not become MCP tools unless their shared contract and capability execution are also registered. Conversely, a capability without a REST route must not be described as REST-supported.

The current read-only MCP surface also includes catalog article revision reads, dimension catalogue/history reads, CRM directory/export reads, bounded collection-history reads, deadline list reads, and supplier-inbox list/get reads. Their operator mutations, approvals, feed creation, directory annotations, legal activation, issuance and delivery remain REST-only or human/provider-gated as declared by their owning contracts.

## Failure and recovery contract

MCP protocol errors (bad JSON-RPC shape, unknown method, invalid tool arguments) are not accounting failures. An accounting refusal is a successful JSON-RPC response containing a tool result with `isError: true` and its `code` and `message`; callers must not treat HTTP 200 as business success. Successful tool calls return `isError: false`, text JSON and typed `structuredContent.result`. Credential failures remain HTTP authentication/authorization errors. `Unavailable` or `InternalError` on a mutation can leave its commit outcome unknown: inspect the matching status/receipt operation, and retry only the unchanged input and original idempotency key. A missing receipt at one point in time is not proof of rollback. Do not retry a conflict as a new command.

The server supports stateless JSON MCP protocol versions `2025-06-18` and `2025-11-25`; it has no SSE, session, subscription or MCP background-task transport. Durable preparation jobs are ordinary capabilities, not protocol background tasks. Tool output schemas describe success, not error content; clients must branch on `isError` before interpreting `structuredContent`. Book scope and permission are checked in the backend, not inferred from a tool listing.

## Remaining proof

Capture a versioned inventory of OpenAPI operations, MCP `tools/list`, their common owning capabilities and deliberate exclusions; exercise each affected path under matching book grants. Include validation failures, forbidden access, stale/conflict handling, response loss and original-key recovery across REST, MCP and job callers. Source inspection alone does not close D-05, and synthetic operator credentials do not close D-01. Provider and legal acceptance remain separate gates.
