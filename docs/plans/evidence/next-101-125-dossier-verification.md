# Fifth NEXT dossier import observation — 2026-09-28

Scope: importing one externally supplied design dossier covering NEXT-101 … NEXT-125 into `docs/specs/next-101-125/`, and recording what was actually checked. No application code, database, Worker, queue, browser or provider workflow was executed, and no packet was implemented. This is provenance and integrity evidence for a vendored document. It is not implementation, runtime, company-readiness or legal evidence.

Source: `openerp-next-101-125.zip` (41 entries) supplied from `~/Downloads`, extracted and vendored as `docs/specs/next-101-125/` by byte-identical copy. The archive's own `README.md` records its planning checkpoint as `66355b62b23e3b8007c2d324f3739fbbcc96cdc0` and its preparation date as 2026-09-28. The machine-readable form of this record is [next-101-125-dossier-verification.json](next-101-125-dossier-verification.json).

This is a separate record from [next-dossier-verification.md](next-dossier-verification.md) (first two waves, 2026-09-26), [next-51-75-dossier-verification.md](next-51-75-dossier-verification.md) (third wave) and [next-76-100-dossier-verification.md](next-76-100-dossier-verification.md) (fourth wave). All three are left as written.

## What was run

| Check | Command | Result |
| --- | --- | --- |
| Archive checksums | `cd docs/specs/next-101-125 && shasum -a 256 -c SHA256SUMS.txt` | 40 of 40 covered files OK, 0 mismatches |
| Archive self-check | `python3 checks/validate.py` | 741 of 741 passed, 0 failed |
| Group breakdown | group totals read from the checker's own output | 572 structure + dependency + document + link (132/77/94/269), 169 arithmetic + model + published-vector (58 arithmetic, 12 mandate, 76 published vectors, 8 refund, 6 planner, 3 access, 3 accounting, 3 provider) |
| Manifest coverage | file walk compared against `SHA256SUMS.txt` | 41 files on disk; the only entry not listed is `SHA256SUMS.txt` itself, which no manifest can cover |
| Pinned-revision ancestry | `git merge-base --is-ancestor 66355b6… HEAD` | ancestor: yes — and it **is** the observed head |
| Planning integrity | `python3 docs/plans/check-plan.py` | passes; mandated index unchanged at 53 packets, 101 edges, 0 cycles, denominator unchanged |

The 741 total and the 572/169 split are the archive's own figures and they reproduce exactly here. The checksum and checker results were produced against the copy in `docs/specs/next-101-125/`, not against the extracted original; both were also run against the extracted original before the copy and produced the same results.

## The checker is not read-only, and this wave's results file is not byte-reproducible

`checks/validate.py` ends by writing its own `checks/results.json`. All five vendored checkers do this, and [the specifications index](../../specs/README.md#verify-the-vendored-copy) covers the general hazard. This wave is the second where it is visible, and for a different reason than the fourth:

- re-running the checker in the vendored tree produced the same 741 results with the same pass/fail counts, but `checks/results.json` then **failed** its own manifest entry;
- diffing the archived and regenerated files showed the only difference is the ordering of a `set` of task IDs rendered into one check's `detail` string. String-set iteration order in CPython depends on the interpreter's hash seed, so the same script emits a different string on a different run or under a different seed;
- the archived bytes were restored from the archive and the manifest re-verified at 40 of 40 before this record was written.

This is a property of the archive's tooling, not evidence for or against any packet. It does mean the vendored copy's integrity check is run-dependent for this tree, which is why the restore was performed and re-verified rather than assumed. The `next-76-100` tree has the same symptom from a different cause — filesystem enumeration order — and both are documented in the specifications index.

## What the pinned revision means for a claim

`66355b6…` is the observed head, so nothing in this dossier is stale. That is the same position as the fourth wave, and it carries the same limit:

- its `README.md` states that "repository reading was targeted to the branch and shared operations/contracts" and that specialist rules and provider facts "were checked narrowly against primary sources, not fully qualified";
- its `solution-index.json` records `prior_status: "not assumed complete"` and states that "all new-wave edges are checked" while "earlier IDs are external contracts; no full 125-node acyclicity claim is made";
- its `README.md` states the package is "proposed additional design, not an instruction to ignore current code", and its `COORDINATOR-HANDOFF.md` states that "a pure function or another retained JSON blob is not a completed application journey".

A well-pinned proposal from a targeted read is still a proposal. Treat the packets as design input and reconcile each against the checkout.

## One item in this wave deserves a maintainer decision on its own

NEXT-121 is opt-in bounded standing posting mandates. This repository has **already** stated the governing contract in [the operations plan](../../operations.md): explicit operation/book/period/account scope, currency, validity, revocation and cumulative limits, with shared budgets reserved and consumed atomically, and the rule that "a mandate never implicitly authorizes payment, closure, signature or filing". The same plan already places unattended posting under a standing mandate outside the Book Zero delivery as later scope. NEXT-121 is therefore mostly design for a contract this repository has adopted, and the packet's own proposed profile — a single qualified recurring purchase-recognition pattern, excluding payments, refunds, payroll, invoice issuance, corrections, tax adjustments, closing, signatures and filing — is narrower than the contract allows.

That is a favourable finding, not a scope reduction: it means the packet needs an authorization decision before implementation, not an ownership decision. The operations plan's wording is the maintained authority; see [the dossier plan](../12-next-implementation-dossier.md) and the `NEXT-121` row there.

## What this observation does not establish

- That any fifth-wave packet is implemented, integrated, runtime-observed, company-qualified or externally accepted. None has a row in [next-packet-progress.md](../next-packet-progress.md).
- That the design is correct. `checks/validate.py` is a document, dependency, link and arithmetic check over the archive's own content, including finite-model and published-vector examples. The archive's `CHECKS.md` says it does not import OpenERP, compile Effect, apply SQL, run a browser, qualify a statutory rule or call a provider.
- Any statutory or company position. Rates, tables, reporting boxes, statement and declaration schemas, deadlines, benefit and per-diem parameters, bank and direct-debit formats and provider contracts remain qualified inputs under D-04, D-08 and D-10. The archive's `01-QUALIFIED-INPUTS.md` lists them; none was qualified here. Its specialist profiles — provisions, B2C/OSS, foreign VAT recovery, car benefit, share subscriptions, direct debit, standing mandates — are conditional by the archive's own statement and are not launch prerequisites.
- Any authority. No test was added, no data was reset, nothing was deployed, and no provider, payment or filing action was taken. The archive states that it creates no permission of any kind, which matches [D-09](../../open-decisions.md) and [D-10](../../open-decisions.md) as they already stand.

## Reproduce

```bash
cd docs/specs/next-101-125 && shasum -a 256 -c SHA256SUMS.txt
cp -R docs/specs/next-101-125 /tmp/next-101-125-check && cd /tmp/next-101-125-check && python3 checks/validate.py
python3 docs/plans/check-plan.py
```
