# NEXT dossier import observation — 2026-09-26

Scope: importing two externally supplied design dossiers into `docs/specs/` and recording what was actually checked. No application code, database, Worker, queue, browser or provider workflow was executed, and no packet was implemented. This is provenance and integrity evidence for vendored documents. It is not implementation, runtime, company-readiness or legal evidence.

Sources: `openerp-next-25-effect` (extracted directory) and `openerp-next-26-50-effect.zip` (extracted for the import), supplied from `~/Downloads`. Vendored as `docs/specs/next-01-25/` and `docs/specs/next-26-50/` by byte-identical copy. The machine-readable form of this record is [next-dossier-verification.json](next-dossier-verification.json).

## What was run

| Check | Command | Result |
| --- | --- | --- |
| First-wave checksums | `cd docs/specs/next-01-25 && shasum -a 256 -c SHA256SUMS.txt` | 37 of 37 files OK, 0 mismatches |
| First-wave self-check | `python3 checks/check_design.py` | 7,465 assertions, 0 failures, 25 packets, `passed: true` |
| Second-wave checksums | `cd docs/specs/next-26-50 && shasum -a 256 -c SHA256SUMS.txt` | 41 of 41 files OK, 0 mismatches |
| Second-wave self-check | `python3 checks/validate.py` | 90 of 90 named design checks passed, 0 failed |
| Pinned-revision ancestry | `git merge-base --is-ancestor <pinned> HEAD` for `5ac3433e…`, `4671a2fb…`, `422276ae…`, `bb628452…` | all four are ancestors of `ac9e1a9` |
| Planning integrity | `python3 docs/plans/check-plan.py` | passes; mandated index unchanged at 53 packets |

The vendored trees were not modified after the copy; the checksum results above were produced against the copies in `docs/specs/`, not against the originals.

## What the pinned revisions mean for a claim

Both dossiers describe a repository state that this repository has moved past. The second wave pins its review at `5ac3433e…` and separately records, in its own `REVISION-NOTE.md`, that a later commit `4671a2fb…` reported NEXT-01 implemented with static checks passing and explicitly no PostgreSQL or Worker requests for its runtime vectors. Both commits are ancestors of the current checkout, so:

- a statement in either dossier that a capability, module or operation was missing describes that pinned revision, not the current tree;
- NEXT-01 may be partly or wholly implemented, and its execution-time owner checks — not the proposed `ownershipVersion` field — are the authority;
- the second wave's own statement that its source review was targeted rather than an every-file audit still holds, and its first-wave prerequisites are not assumed complete.

The first wave names an attached ownership amendment and the earlier SQL-era 25-packet archive as its inputs. Neither was supplied with the tree, so claims traceable only to those inputs cannot be checked here.

## What this observation does not establish

- That any packet is implemented, integrated, runtime-observed, company-qualified or externally accepted.
- That the design is correct. Both checkers are document and arithmetic checks over the archives' own content: packet identity, declared dependency graphs, link and source-reference consistency, code-fence balance, exact illustrative arithmetic and selected state distinctions. Several state examples are deliberate assertions of the chosen model, not concurrency or network simulations.
- Any statutory position. Rates, tables, reporting boxes, deadlines, declaration schema versions, provider contracts and credentials remain qualified inputs under D-04, D-08 and D-10.
- Any authority. No test was added, no data was reset, nothing was deployed, and no provider, payment or filing action was taken.

## Reproduce

```bash
cd docs/specs/next-01-25 && shasum -a 256 -c SHA256SUMS.txt && python3 checks/check_design.py
cd docs/specs/next-26-50 && shasum -a 256 -c SHA256SUMS.txt && python3 checks/validate.py
python3 docs/plans/check-plan.py
```
