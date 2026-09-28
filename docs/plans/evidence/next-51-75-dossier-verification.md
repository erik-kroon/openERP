# Third NEXT dossier import observation — 2026-09-28

Scope: importing one externally supplied design dossier covering NEXT-51 … NEXT-75 into `docs/specs/next-51-75/`, and recording what was actually checked. No application code, database, Worker, queue, browser or provider workflow was executed, and no packet was implemented. This is provenance and integrity evidence for a vendored document. It is not implementation, runtime, company-readiness or legal evidence.

Source: `openerp-next-51-75.zip` (41 entries) supplied from `~/Downloads`, extracted and vendored as `docs/specs/next-51-75/` by byte-identical copy. The archive's own `README.md` records the pinned source revision as `116a5ca6b5fb9ec9fb08ee55c3beaad5af6b8fa5` and its preparation date as 2026-09-28. The machine-readable form of this record is [next-51-75-dossier-verification.json](next-51-75-dossier-verification.json).

This is a separate record from [next-dossier-verification.md](next-dossier-verification.md), which observed the first two waves on 2026-09-26 and is left as written.

## What was run

| Check | Command | Result |
| --- | --- | --- |
| Archive checksums | `cd docs/specs/next-51-75 && shasum -a 256 -c SHA256SUMS.txt` | 40 of 40 covered files OK, 0 mismatches |
| Archive self-check | `python3 checks/validate.py` | `named_checks: 80`, `passed: 80`, `failed: 0` |
| Manifest coverage | file walk compared against `SHA256SUMS.txt` | 41 files on disk; the only entry not listed is `SHA256SUMS.txt` itself, which no manifest can cover |
| Pinned-revision ancestry | `git merge-base --is-ancestor 116a5ca6… HEAD` | ancestor: yes |
| Planning integrity | `python3 docs/plans/check-plan.py` | passes; mandated index unchanged at 53 packets, edges and denominator |

The checksum and checker results above were produced against the copy in `docs/specs/next-51-75/`, not against the extracted original. Both were also run against the extracted original before the copy and produced the same results.

## What the pinned revision means for a claim

`116a5ca6…` is an ancestor of the observed head, so a statement in the dossier that a capability is missing describes that revision and not this checkout. Two of the dossier's own statements narrow its absence claims further, and both are recorded here because they bound how much weight the "new deliverable" column can carry:

- its `INTEGRATION-MAP.md` says a packet describes a workflow "absent from the prior NEXT scope", and states plainly that "this is not an exhaustive current-source absence audit" — some generic scaffolding may already exist and must be extended rather than duplicated;
- its `README.md` states that it "does not claim all fifty earlier tasks are complete or that every new capability is wholly absent from unreviewed code".

So the third wave is the weakest of the three as evidence of absence, and the strongest as a statement of what its authors intended to build. Reconcile against the checkout before treating any packet as new work.

## What this observation does not establish

- That any third-wave packet is implemented, integrated, runtime-observed, company-qualified or externally accepted. None has a row in [next-packet-progress.md](../next-packet-progress.md).
- That the design is correct. `checks/validate.py` is a document and arithmetic check over the archive's own content: packet identity, declared conditional dependencies, file hashes, document links and synthetic state/arithmetic examples. The archive's own `CHECKS.md` says so and says it cannot prove transaction atomicity, access policy, legal applicability or live acceptance.
- Any statutory position. Rates, tables, reporting boxes, statement and declaration schemas, deadlines, per-diem and mileage amounts, bank formats and provider contracts remain qualified inputs under D-04, D-08 and D-10. The dossier's `01-QUALIFIED-INPUTS.md` lists them; none was qualified here.
- Any provider or company fact. No mandate, credential, sandbox or company record was obtained or used, and the first external exercise, if one is ever authorized, must use authorized test or recipient scope.
- Any authority. No test was added, no data was reset, nothing was deployed, and no provider, payment or filing action was taken.

## Reproduce

```bash
cd docs/specs/next-51-75 && shasum -a 256 -c SHA256SUMS.txt && python3 checks/validate.py
python3 docs/plans/check-plan.py
```
