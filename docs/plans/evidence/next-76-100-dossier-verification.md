# Fourth NEXT dossier import observation — 2026-09-28

Scope: importing one externally supplied design dossier covering NEXT-76 … NEXT-100 into `docs/specs/next-76-100/`, and recording what was actually checked. No application code, database, Worker, queue, browser or provider workflow was executed, and no packet was implemented. This is provenance and integrity evidence for a vendored document. It is not implementation, runtime, company-readiness or legal evidence.

Source: `openerp-next-76-100.zip` (41 entries) supplied from `~/Downloads`, extracted and vendored as `docs/specs/next-76-100/` by byte-identical copy. The archive's own `README.md` records its planning checkpoint as `66355b62b23e3b8007c2d324f3739fbbcc96cdc0` and its preparation date as 2026-09-28. The machine-readable form of this record is [next-76-100-dossier-verification.json](next-76-100-dossier-verification.json).

This is a separate record from [next-dossier-verification.md](next-dossier-verification.md) (first two waves, 2026-09-26) and [next-51-75-dossier-verification.md](next-51-75-dossier-verification.md) (third wave, 2026-09-28). Both are left as written.

## What was run

| Check | Command | Result |
| --- | --- | --- |
| Archive checksums | `cd docs/specs/next-76-100 && shasum -a 256 -c SHA256SUMS.txt` | 40 of 40 covered files OK, 0 mismatches |
| Archive self-check | `python3 checks/validate.py` | 264 of 264 passed, 0 failed — 131 structure, 69 document, 64 arithmetic, matching the archive's own `CHECKS.md` breakdown |
| Manifest coverage | file walk compared against `SHA256SUMS.txt` | 41 files on disk; the only entry not listed is `SHA256SUMS.txt` itself, which no manifest can cover |
| Pinned-revision ancestry | `git merge-base --is-ancestor 66355b6… HEAD` | ancestor: yes — and it **is** the observed head, so this wave is pinned to the tree observed at import |
| Planning integrity | `python3 docs/plans/check-plan.py` | passes; mandated index unchanged at 53 packets, 101 edges, 0 cycles, denominator unchanged |

The checksum and checker results above were produced against the copy in `docs/specs/next-76-100/`, not against the extracted original. Both were also run against the extracted original before the copy and produced the same results.

## The checker is not read-only, and this wave's results file is not byte-reproducible

`checks/validate.py` ends by writing its own `checks/results.json`. All four vendored checkers do this, and the reproduction note in [the specifications index](../../specs/README.md#verify-the-vendored-copy) covers the general hazard. This wave is the one where it is visible:

- re-running the checker in the vendored tree produced the same 264 results with the same pass/fail counts, but `checks/results.json` then **failed** its own manifest entry;
- diffing the archived and regenerated files showed the only difference is the **order** of the named document checks, which the checker emits in filesystem enumeration order rather than sorted order. The generating machine enumerated the tree differently;
- the archived bytes were restored from the archive and the manifest re-verified at 40 of 40 before this record was written.

For the first three waves the regenerated `results.json` is byte-identical to the archived one, which was confirmed by running each checker against a throwaway copy. The practical rule is therefore: verify checksums first, and run this wave's checker in a copy if the vendored tree must stay untouched.

This is a property of the archive's tooling, not evidence for or against any packet. It does mean the vendored copy's integrity check is order-sensitive for this one tree, which is why the restore was performed and re-verified rather than assumed.

## What the pinned revision means for a claim

`66355b6…` is the observed head, so nothing in this dossier is stale in the way the earlier waves are. That makes it the best-pinned of the four and, by the archive's own account, the least audited:

- its `README.md` states that "current repository reading was targeted to plans, operations and the candidate entry point" and that "no complete source audit or runtime qualification is claimed";
- its `solution-index.json` records `prior_status: "not assumed complete"` and states that only the new-wave graph is checked, with the earlier seventy-five as an external contract dependency rather than a revalidated hundred-task graph;
- its `INTEGRATION-MAP.md` gives a per-packet "new versus already designed" statement instead of a source-requirement crosswalk, and reserves the same owners under names that "identify the original reservations, not a claim they are still unfinished".

Read the packets as design input. A well-pinned proposal from a targeted read is still a proposal, and the absence claims in particular are the weakest part of it.

## What this observation does not establish

- That any fourth-wave packet is implemented, integrated, runtime-observed, company-qualified or externally accepted. None has a row in [next-packet-progress.md](../next-packet-progress.md).
- That the design is correct. `checks/validate.py` is a document and arithmetic check over the archive's own content: packet identity, dependency ordering, source references, file hashes, code-fence and link structure, and synthetic state/arithmetic examples. The archive's `CHECKS.md` says it does not import OpenERP, compile Effect, apply SQL, run a browser, qualify a statutory rule or call a provider.
- Any statutory or company position. Rates, tables, reporting boxes, statement and declaration schemas, deadlines, pension and tax-reserve parameters, bank formats and provider contracts remain qualified inputs under D-04, D-08 and D-10. The archive's `01-QUALIFIED-INPUTS.md` lists them; none was qualified here. Its conditional profiles — grants, dividends, termination, pension, ROT/RUT, tax allocations, operating leases — are conditional by the archive's own statement and are not launch prerequisites.
- Any authority. No test was added, no data was reset, nothing was deployed, and no provider, payment or filing action was taken. The archive states that it creates no test, browser, provider, production-data or deployment permission, which matches [D-09](../../open-decisions.md) and [D-10](../../open-decisions.md) as they already stand.

## Reproduce

```bash
cd docs/specs/next-76-100 && shasum -a 256 -c SHA256SUMS.txt
cp -R docs/specs/next-76-100 /tmp/next-76-100-check && cd /tmp/next-76-100-check && python3 checks/validate.py
python3 docs/plans/check-plan.py
```
