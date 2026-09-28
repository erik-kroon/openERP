# Architecture follow-up and distribution setup

This compares the third supplied architecture package and the subsequent open-accounting proposal with the live repository. The supplied prose is design input, not evidence that a feature exists or authority to create accounts, deploy, publish, use customer data or add tests.

## Earlier architecture recommendations

| Recommendation                                                                                                     | Current disposition                                                                                                                                                                                              |
| ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| One PostgreSQL authority, exact money, immutable approval, transactional receipts and shared REST/MCP/UI semantics | Already retained in architecture, domain, shared contracts and posting plans. Implementation and full acceptance remain separate.                                                                                |
| Capture consistent inputs, compile pure calculations, persist the exact plan and commit through one owner          | Superseded for implementation ownership by [ADR 0010](adr/0010-application-owned-accounting-replacement.md). Application operations now own capture, calculation, persistence and scoped writes; SQL keeps only the narrow integrity layer. The earlier sequence remains useful context, not a function-only authority. |
| Distinguish posting eligibility from period content so independent proposals do not stale each other               | The narrow-versus-aggregate requirement existed; explicitly name the two dependency versions and their mutation rules. This is a required future implementation/proof detail, not a new claim about current SQL. |
| Consider dimensions, tax and register meaning when checking a correction for no change                             | Add the explicit rule to the correction plan. Comparing only debit/credit account totals is insufficient once those effects are supported.                                                                       |
| Frozen bulk-import manifest and exclusive progress fence                                                           | Chunk identities and leases already exist in the import plan; make competing-writer exclusion and fixed membership explicit. General historical import remains planned.                                          |
| Signed journal amounts and proposed alternate API/package names                                                    | Do not adopt: ADR 0004 reconciles the existing paired debit/credit contract and existing callers. Preserve sealed-record interpretation.                                                                         |
| Newer Effect source version, broader schemas and money example                                                     | Reference material only. Keep the installed Effect version, owned Effect contracts and existing precision guards. No reference module or tests are imported wholesale.                                           |
| Assume a live previous-system migration                                                                                     | Not a gate for this unreleased replacement. The clean baseline has no old-schema upgrade; keep actual source/version and company inputs as a separate D-06 gate for any later import or first-company cutover.                                                                                            |

## Application-owned replacement reconciliation

[ADR 0010](adr/0010-application-owned-accounting-replacement.md) supersedes the earlier implementation/compatibility portions of ADRs 0001, 0002, 0004, 0007 and 0008 without changing their financial meaning. The current checkout still contains the pre-replacement SQL dispatch and Cloudflare preparation path, so those source observations remain historical implementation context until cutover. The target has one application transaction owner, a three-file clean baseline, direct scoped application writes, no old-schema adapter, no dual writer and no fallback dispatch. [ADR 0009](adr/0009-effect-mq-background-jobs.md) supplies the separate effect-mq Bun delivery path; its listener is not an API or financial transaction dependency. The maintained [application-owned replacement plan](plans/application-owned-accounting.md) contains the live caller inventory and proof gates.

## Open-accounting setup

The new [ADR 0005](adr/0005-open-accounting-and-managed-services.md) records open accounting and jurisdiction/agent layers, optional managed operations, current module ownership and deferred Rust extraction. [LICENSING.md](../LICENSING.md) records the user's AGPL-3.0-only choice for all project-owned code; package metadata and the full license agree. Third-party terms remain intact.

[CONTRIBUTING.md](../CONTRIBUTING.md) supplies contributor entry points and scope/provenance rules. [The self-host package](../infra/self-host/README.md) adds the Bun runtime, local configuration and PostgreSQL Compose recipe. It does not implement unavailable accounting, archive, provider or regulatory capabilities merely by packaging the current application.

The later [layout decision](adr/0007-domain-and-jurisdiction-layout.md) extracts shared models and existing Swedish calculations into real workspace packages and separates API internals by responsibility. It adds no new accounting capability. No managed-service repository, hosted billing, credential vault, Rust crate, additional country or cloud deployment is created. These require real consumers or external arrangements. Runtime evidence and container verification limits are recorded alongside the self-host package.

## Post-migration review, September 2026

The supplied review of `1e632b93c758aa81550d61455f288a24b3c461d0`
retains the Effect/application-owned modular monolith. Its concrete fixes now use
the existing owners:

| Finding | Implemented behavior |
| --- | --- |
| F01: immutable extraction request locking | Plain request reads; current scoped book authority and mutable lifecycle locks serialize execution, review and cancellation. No widened grants. |
| F02: extraction executor authority | Service-intent requests survive requester-session expiry. Current executor API credential, identity and entity/book membership are required at capture, publication and terminal settlement. Cancellation and supersession remain independent fences. Dispatch filters the executor's books. |
| F03: duplicate cursors | Named context/kind/id/revision fields, validated kind/revision combinations and retained scoped anchor checks. Both draft and registered continuations are exercised by the E2E journey. |
| F04: retained-history ceiling | Creation has no lifetime draft quota. HTTP/MCP/UI use live 200-head keyset pages, with bounded search input. The list's count is page-local, next continues it, and complete is true only when the initial page contains the whole matching collection. History is preserved. |
| F05: Swedish business date | One Europe/Stockholm instant conversion feeds backend admission and frontend dates. Overview and status queries change across midnight; focus and visibility changes refresh suspended pages. |

Draft summaries take decoded revision contracts. Unknown calculated tax/gross
amounts stay null, while zero stays the exact string `"0"`. The full supplier
journey also exposed and repaired nested draft/parent command-receipt collisions,
missing extraction-result projection fields and registered duplicate results that
had omitted the live invoice projection. Nested command receipts use distinct
keys and remain atomic with their owning review receipt.

Duplicate body loading now needs at most two bounded queries: candidate draft
bodies and a batch through the existing live invoice owner. Read operations in
the touched draft/extraction paths reuse the authority owner's book lock instead
of repeating an unused book query. The book-wide consistency boundary remains.
The approved E2E workload measures statement count, PostgreSQL execution time,
HTTP latency and an intentionally contended book read; those local measurements
do not establish production throughput or justify finer-grained locking.

Run commands, failure contracts and artifact names are maintained in
[the E2E guide](../apps/api/tests/README.md). Static checks, local runtime results,
browser observations and actual-company acceptance remain distinct. Static DDL
capability caching and narrower worker credentials remain deployment design work;
mutable principal authority is never cached with database capabilities.

[Local verification](plans/evidence/post-migration-review-fixes.md) records the
fixed-source 44-test pass, runtime-role and revocation journeys, 201 accepted
historical drafts, browser date/pagination observations and query/lock samples.
