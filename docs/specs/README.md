# Vendored implementation dossiers

Status: **vendored design material, not implementation status**. Added 2026-09-26; the third and fourth NEXT waves added 2026-09-28. The NEXT trees are byte-identical copies of externally supplied NEXT-packet dossiers. The two review trees are byte-identical copies of externally supplied review packages for plans this repository already maintains. All six are kept outside the maintained plan namespace so that no maintained requirement, roadmap claim or acceptance count inherits their status. The maintained bridges are [the NEXT dossier plan](../plans/12-next-implementation-dossier.md) and [the plan review adoption record](../plans/14-plan-review-adoption.md); the decision to vendor the NEXT dossiers this way is [ADR 0012](../adr/0012-next-implementation-dossier.md).

## NEXT packet dossiers

| Tree | Packets | Pinned review | Archive self-check | Re-verified on import |
| --- | --- | --- | --- | --- |
| [`next-01-25/`](next-01-25/README.md) | NEXT-01 … NEXT-25, application-owned Effect edition v2 | architecture context `422276ae5ed9d0ca146447d92bb3d27c99f8c48a`; inherited task/source baseline `bb628452196a55ceef7516f76fc3cd6471ae4d91` | `checks/check_design.py`: 7,465 assertions, 0 failures | `shasum -a 256 -c SHA256SUMS.txt` — 37 of 37 files OK; checker re-run passed |
| [`next-26-50/`](next-26-50/README.md) | NEXT-26 … NEXT-50, second wave | repository review pinned to `5ac3433e3e75ef7fc0229cbe00107003b63aa32d`, review date 2026-09-26, plus the limited late observation `4671a2fbaea88bcab613b28b967971469548834365` | `checks/validate.py`: 90 of 90 named design checks passed | `shasum -a 256 -c SHA256SUMS.txt` — 41 of 41 files OK; checker re-run passed |
| [`next-51-75/`](next-51-75/README.md) | NEXT-51 … NEXT-75, third wave | repository review pinned to `116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5`, prepared 2026-09-28 | `checks/validate.py`: 80 of 80 named design checks passed | `shasum -a 256 -c SHA256SUMS.txt` — 40 of 40 files OK; checker re-run passed |
| [`next-76-100/`](next-76-100/README.md) | NEXT-76 … NEXT-100, fourth wave | planning checkpoint `66355b62b23e3b8007c2d324f3739fbbcc96cdc0`, prepared 2026-09-28; targeted reading, not a source audit | `checks/validate.py`: 264 of 264 named design checks passed (131 structure, 69 document, 64 arithmetic) | `shasum -a 256 -c SHA256SUMS.txt` — 40 of 40 files OK; checker re-run passed, see the ordering caveat below |

The recorded import observations, including the commands and their limits, are [next-dossier-verification.md](../plans/evidence/next-dossier-verification.md) for the first two waves, [next-51-75-dossier-verification.md](../plans/evidence/next-51-75-dossier-verification.md) for the third and [next-76-100-dossier-verification.md](../plans/evidence/next-76-100-dossier-verification.md) for the fourth.

## Plan review packages

These review plans this repository already maintains and propose **replacements that have not been adopted**. The maintained plans, and ADR 0011, are unmodified.

| Tree | Reviews | Reviewed commit | Archive self-check | Re-verified on import |
| --- | --- | --- | --- | --- |
| [`parity-plan-review/`](parity-plan-review/README.md) | the [reference parity backlog](../plans/11-parity-backlog.md) and [ADR 0011](../adr/0011-reference-parity-backlog.md) | `ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb` | `checks/check_review.py`: 36 of 36 passed | supplied `SHA256SUMS.txt` — all files OK; checker re-run passed |
| [`testing-plan-review/`](testing-plan-review/README.md) | the [test suite design](../plans/test-suite-design.md) and [pseudologic](../plans/test-suite-pseudologic.md) | `8bff9fadbcacf9d369758b967971469548834365`, read at `ac9e1a91` | none supplied; `CHECKS.json` records illustrative arithmetic only | manifest **computed on import** — 8 of 8 files OK |

The testing archive ships no checksum manifest and no `checks/` directory, so its `SHA256SUMS.txt` was generated during import. Do not read it as archive-supplied provenance. Adoption of either replacement is an open maintainer decision recorded in [14-plan-review-adoption.md](../plans/14-plan-review-adoption.md).


## Book Zero PRD

The openERP-specific [Book Zero, Workflow and Drastic Cash PRD v1](book-zero-v1/PRD_openERP_Book_Zero_Workflow_Drastic_Cash_v1.md), dated 2026-09-27, is imported from `Drastic_Financial_Platform_PRD_v1.zip`. Only that source document is vendored here. The broader platform PRD and its `DR-*`/`ES-AT-*` registers are not adopted as openERP scope.

The document is byte-identical to the archive entry and matches the archive manifest's SHA-256. Its [SHA256SUMS.txt](book-zero-v1/SHA256SUMS.txt) was generated on import for convenient rechecking; it is not a second archive-supplied file. [Provenance and document checks](../plans/evidence/book-zero-docs-verification.md) record the archive/source identities and limits. Verify with:

```bash
cd docs/specs/book-zero-v1 && shasum -a 256 -c SHA256SUMS.txt
```

The source's selective repository review is pinned to `41410fd75e96361b7c2f407d456019500f39bfbe`; reconcile current code before interpreting its observations. Its proposed file paths, agent-facing instructions and legal/company statements are source material, not execution authority or newly verified facts. The user requested a documentation update. The maintained [Book Zero plan](../plans/15-book-zero-workflow-cash.md), [product scope](../product.md), [frontend](../frontend.md) and [verification plan](../verification.md) carry the relevant requirements without changing the original.

## What each tree contains

| File | Role |
| --- | --- |
| `README.md` | The archive's own packet index and dispatch instruction. |
| `00-COMMON.md` | The wave's shared implementation contract: boundary, exact values, evidence/authority records, preparation and approval, atomic execution, lock and query discipline, external attempts and queue delivery. |
| `01-RULE-AND-PROVIDER-DATA.md` | The qualified external inputs each packet needs, and the release-selection algorithm that refuses rather than defaults. |
| `MASTER-PSEUDOCODE.md` | The coordinator document: the common contract followed by every packet body in full. |
| `INTEGRATION-MAP.md` | Dependency and handoff table, reserved work, cross-owner contracts and shared-file conflicts. |
| `packets/NEXT-nn.md` | One work packet: existing owner, new scope, dependencies, records, algorithms, transaction behavior, UI and required vectors. |
| `SOURCES.md` | Source anchors, prior-wave identifiers and what the review did not establish. |
| `solution-index.json` | Machine-readable index: identity, priority, lane, dependencies, existing owner, new scope, status and per-packet checksum. |
| `DECISIONS.md` (second, third and fourth waves), `CHANGES.md` (first wave), `REVISION-NOTE.md`, `COORDINATOR-HANDOFF.md`, `CHECKS.md` | Wave-specific decision, rewrite, late-movement and check records. |
| `checks/`, `SHA256SUMS.txt` | The archive's own reproducible structural/arithmetic checker and the checksums that prove this copy is unmodified. |

## Verify the vendored copy

```bash
cd docs/specs/next-01-25 && shasum -a 256 -c SHA256SUMS.txt && python3 checks/check_design.py
cd docs/specs/next-26-50 && shasum -a 256 -c SHA256SUMS.txt && python3 checks/validate.py
cd docs/specs/next-51-75 && shasum -a 256 -c SHA256SUMS.txt && python3 checks/validate.py
cd docs/specs/next-76-100 && shasum -a 256 -c SHA256SUMS.txt && python3 checks/validate.py
cd docs/specs/parity-plan-review && shasum -a 256 -c SHA256SUMS.txt && python3 checks/check_review.py
cd docs/specs/testing-plan-review && shasum -a 256 -c SHA256SUMS.txt
```

All checkers are document and arithmetic checks. They import no application source, compile no TypeScript, run no SQL, Worker, queue or provider call, and use no company data. They cannot establish that any packet is implemented or correct.

Every one of these checkers **writes** its own `checks/results.json` when it runs, so running a checker inside a vendored tree is a write to that tree. Verify the checksums first. For `next-01-25`, `next-26-50` and `next-51-75` the regenerated file is byte-identical to the archived one, so the order above is safe. For `next-76-100` it is not: the same 264 checks pass with the same counts, but the document checks are emitted in filesystem enumeration order, which differs from the machine that produced the archived file, so `checks/results.json` then fails the manifest until the archived bytes are restored from the archive. Run that checker in a copy if you want to leave the vendored tree untouched.

Do not edit a file inside any vendored tree. A packet that no longer matches its recorded checksum is no longer the reviewed artifact; record a change as a new dated plan revision instead. The provenance notes maintained by this repository live in [the dossier plan](../plans/12-next-implementation-dossier.md), the [plan review adoption record](../plans/14-plan-review-adoption.md) and the [ADR](../adr/0012-next-implementation-dossier.md), not inside the vendored trees.

## How an implementing agent uses a packet

1. Read the current `AGENTS.md`, [ADR 0009](../adr/0009-effect-mq-background-jobs.md), [ADR 0010](../adr/0010-application-owned-accounting-replacement.md) and the owning area plan. The repository instructions win on any conflict with a packet.
2. Reconcile the pinned review against the actual checkout. A path, function or module named in a packet is a proposed contract to bind to real code, not a claim that the name exists.
3. Resolve the packet's `APP-SLICE-READY(...)` prerequisites and reserved handoffs. A missing port is a prerequisite to raise, not a second owner to build.
4. Implement the pure calculation and the named application operation; pass the caller's transaction into every nested journal, tax, register, approval-use and receipt write.
5. Return the worker's own evidence and blockers. The archive's vectors are design obligations, not repository tests, and they grant no test, deployment, provider or company-data authority.

## Limits of the vendored material

- The first wave's v2 rewrite names an attached ownership amendment and the earlier 25-packet archive as its inputs. Those inputs are **not** part of the supplied tree; only the rewritten outputs are vendored. Claims traceable only to those inputs cannot be checked here.
- The second wave states that its source review was targeted rather than an every-file audit, and that it did not run application tests, migrations, financial operations or provider requests. Its "missing capability" statements describe a pinned revision, not the current checkout.
- The third wave states that its new packets describe economic or external workflows absent from the *prior NEXT scope*, and explicitly that this is not an exhaustive absence audit of current source: some scaffolding may already exist and must be extended rather than duplicated. Its "new deliverable" wording is therefore a claim about the earlier packets, not proof of absence in this checkout.
- The fourth wave is pinned to this repository's current head, and says so: its reading was "targeted to plans, operations and the candidate entry point", with "no complete source audit or runtime qualification" claimed. It is therefore the best-pinned and the least-audited of the four at once. Its conditional profiles — grants, dividends, termination, pension, ROT/RUT, tax allocations, operating leases — require actual company applicability and are explicitly not launch prerequisites.
- All four waves record that the repository moved during preparation, or are pinned to a revision this repository has since moved past. A statement of absence at a pinned revision is not a statement of absence now.
- Statutory rates, tax tables, provider schemas, employment agreements and credentials remain explicit qualified inputs. Nothing in these trees activates a rule, rate, provider or legal profile.
