---
name: effect-ts
description: Build new Effect 4 TypeScript code in OpenERP. Use for Effect setup, functions, services, layers, schemas, typed errors, HTTP APIs and clients, resource lifetimes, and observability. Focused on new development, not framework migration.
---

# Effect 4 for OpenERP

Adapted from Sellfinity's `effect-ts` skill for new OpenERP development. Repository instructions and the user's scope govern the work. This skill provides implementation guidance; it does not authorize dependency upgrades, deployment, or test additions.

## Establish the installed API

Before Effect implementation:

1. Read the repository instructions and the relevant workspace manifests. Resolve the installed `effect` version through the lockfile and package metadata.
2. Read the installed `node_modules/effect/AGENTS.md` once. With Bun's isolated linker, follow the workspace symlink or locate the package under `node_modules/.bun`.
3. Use `effect-solutions list`, then `effect-solutions show <topic>` for the relevant topic. If it is not on `PATH`, try `~/.bun/bin/effect-solutions`. If unavailable, continue with the installed documentation and source; do not install it just to satisfy this workflow.
4. Confirm uncertain signatures in the installed `effect/src` and declarations. Its `ai-docs` examples are useful when present. The optional shared checkout at `~/.local/share/effect-solutions/effect` is secondary evidence unless its revision matches.

The port was checked against `effect@4.0.0-rc.112`. Recheck after dependency changes. Guides can disagree even within Effect 4: this installed release exposes `Schema.TaggedError` and `Schema.Decoder`. Do not copy a guide's claim that those names are absent.

## Setup within this repository

- Retain Bun workspaces and the selected Effect release. Add a dependency only for a required import; runtime adapters must support the installed Effect release and actual runtime.
- Schema is in `effect/Schema`; HTTP APIs and clients are in `effect/unstable/httpapi` and `effect/unstable/http`. Do not add `@effect/schema` or `@effect/platform` for these capabilities.
- OpenERP uses TypeScript 7 with `@effect/tsgo` and the root `prepare` command `effect-tsgo patch --typescript`. Preserve that setup and the shared strict configuration in `packages/config`; do not apply generic language-service setup instructions over it.
- For a new workspace, follow neighboring manifests, public package exports, TypeScript configuration, and existing check commands. Do not initialize a second project or generate unused service files.

Consult `project-setup` and `tsconfig` only when setup changes are part of the task. Consult the installed `@effect/tsgo` documentation before changing its configuration.

## Place new code at its owner

| Responsibility | Owner |
| --- | --- |
| Accounting models, exact money and domain errors | `packages/domain` |
| HTTP contracts, command schemas and error status mapping | `packages/contracts` |
| Pure Swedish calculations and SIE rendering | `jurisdictions/se` |
| Shared Effect operations | `apps/api/src/application` |
| HTTP/MCP handlers, adapters, database and runtime composition | `apps/api/src/transport`, `adapters`, `db`, `runtime` |
| Product routes, UI state, TanStack Query integration | `apps/web` |
| Reusable controls and StyleX tokens | `packages/ui` |
| Deployment bindings | `infra/alchemy` |

Keep backend workflows as Effects and execute them at the Worker boundary. Pure calculations can remain synchronous functions. Introduce a service when it owns a dependency, resource, or coherent behavior; do not wrap every helper in a service.

TanStack Query owns remote state in the web app, with a QueryClient created per router/request. Use React for local interaction state. Do not introduce Effect Atom as a competing state system.

For company/book access, financial mutations, retryable commands, or background jobs, read [Business operation rules](references/business-operations.md). It applies the Sellfinity lessons on company separation, safe retries, restart recovery, and exact money to OpenERP's accounting boundaries.

## Find the implementation design for assigned work

Requirements, invariants and delivery contracts live in `docs/`. When the assigned work is a `NEXT-nn` packet, the implementation-level design is the [NEXT dossier plan](../../docs/plans/12-next-implementation-dossier.md) plus the vendored packet under `docs/specs/`. Treat it as a contract to bind to real code, not a framework to reproduce:

- Reconcile the packet's named paths, `App`/`Db`/`Domain` symbols and existing owner against the actual checkout. The pinned review behind the packet is older than the tree, so a statement that something was missing is a statement about that revision.
- Resolve the packet's `APP-SLICE-READY(area)` prerequisite before coding. A missing port is a prerequisite to report, not a second owner to build, and the reserved VAT, FX, asset, amendment and webshop-intake owners stay reserved.
- Keep one financial transaction per group: pass the caller's transaction into every nested journal, tax, register, approval-use and receipt write, and never open a second transaction from inside a financial group.
- Keep exact money exact, and satisfy the packet's vectors and replay/stale-approval cases as obligations. The packets add no test and grant no deployment, provider, payment or filing authority; `AGENTS.md` and the open decisions still govern.

## Read only the relevant patterns

| Work | Local reference | Effect Solutions topic |
| --- | --- | --- |
| Functions, SDK bridges, concurrency, cleanup | [Functions and resources](references/functions-and-resources.md) | `basics` |
| Services, layers, configuration | [Services and layers](references/services-and-layers.md) | `services-and-layers`, `config` |
| Drizzle queries, database transactions, connection ownership | [Database access](references/database-access.md) | Installed Drizzle and SQL adapter source |
| Boundary validation, optional fields, failures | [Schemas and errors](references/schemas-and-errors.md) | `data-modeling`, `error-handling` |
| API routes, generated clients, logging, Worker lifetime | [HTTP and observability](references/http-and-observability.md) | Installed HTTP examples |

## Implement and verify within scope

Trace the caller, schema, operation, resource owner, and runtime entrypoint before extending them. Preserve typed failures, cancellation, and current authorization through that path.

Run the smallest existing check that covers the change. OpenERP provides `bun run lint`, `bun run check-types`, `bun run format:check`, and `bun run build`. A Bun build does not establish Worker runtime compatibility. For runtime-sensitive changes, exercise the real authorized request or operation and report what was observed.

Do not add or edit tests, fixtures, or test helpers without explicit approval. A request to use this skill is not test approval. Do not require a new test file to proceed with otherwise authorized work.
