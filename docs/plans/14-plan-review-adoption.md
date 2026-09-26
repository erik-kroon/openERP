# Plan review adoption: reference parity and test plan

Status: **review material vendored; no replacement adopted**. Added 2026-09-26. Two externally produced review packages were imported under [`docs/specs`](../specs/README.md) and are recorded here. Neither the accepted [reference parity backlog](11-parity-backlog.md), [ADR 0011](../adr/0011-reference-parity-backlog.md) nor the [test suite design](test-suite-design.md) / [pseudologic](test-suite-pseudologic.md) has been modified. Adoption of either proposed replacement is a maintainer decision and has **not** been taken.

| Review | Reviewed commit | Files inspected at | Proposed replacement | Adopted |
| --- | --- | --- | --- | --- |
| [Reference parity](../specs/parity-plan-review/README.md) | `ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb` (`parity backlog`) | same | `11-parity-backlog.REVISED.md` (1,503 → 235 lines) + `ADR-0011.REVISED.md` | no |
| [Test plan](../specs/testing-plan-review/README.md) | `8bff9fadbcacf9d369758b967971469548834365` (`test plans`) | `ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb` | `REVISED-TEST-PLAN.md` + `CORRECTED-WORKFLOW-CASES.md` (1,223 → 743 lines) | no |

The vendoring decision follows [ADR 0012](../adr/0012-next-implementation-dossier.md): the material is kept outside the maintained plan namespace so no maintained requirement, dependency edge, completion count or acceptance gate inherits its status. Both packages state this themselves — the parity ADR is labelled *"proposed replacement … for review"* and its companion edits say the accepted ADR *"is not retroactively rewritten by this artifact"*.

## Verdict summary

**Parity.** Keep the inventory, the `PRY-01`…`PRY-85` namespace, the exact-money boundary and the implementation/evidence distinction. Do **not** dispatch the preserved recipes unchanged. The review finds 17 stop-ship rows in the plan text, including recipes that would:

- treat a detector failure as permission to proceed (PRY-39 / R11 returns `CLEAR` when detection fails without force);
- balance away skipped source history with an adjustment voucher (PRY-25);
- let ignored bank movements disappear from independent account totals (PRY-35);
- lose cash-method year-end recognition through payment-date-only logic (PRY-50 / R23);
- double-count sick pay by combining first-day removal with a waiting deduction (R9);
- omit required Peppol terms from the due calculation (R21).

It also finds the plan's "unowned" assertions contradicted by existing maintained plans, and dependencies that turn a comparison into a parallel roadmap. The proposed remedy keeps all 85 IDs, attaches them to existing canonical owners, rejects unsafe reference behavior and qualifies genuinely new profiles — explicitly *not* 85 new independent services.

**Test plan.** Keep the real-Worker / real-PostgreSQL harness, negative neighbors, independent observations, explicit recovery and non-vacuous checks. Do **not** implement the pseudologic verbatim. Of 18 findings, **4 are Critical and 8 High**. The most consequential:

- **TP-01 (Critical)** — `HARNESS-1` reverses the accepted database boundary. It requires the runtime role to be unable to write application tables, which `AGENTS.md` and ADR 0010 explicitly assign to the trusted application. Implemented as written, the harness would **reject the intended installation**, conflating a backend database identity with an end-user identity and inviting RLS/GUC tenant identities back.
- **TP-04 / TP-05 / TP-06 (Critical)** — expected outcomes contradict either the selected application-owned architecture, the same document's own guard ladders, or the inspected implementation. Implemented verbatim they would train tests to reject correct behavior, or prompt changes that weaken accounting controls.

The review's central revision is to make the plan a specification of observable business behavior rather than a transcription of today's `if`-statement order, preserving guard-order assertions only where the order is a real contract (current access before receipt disclosure, replay before new-work expiry, complete validation before committed effects, owner routing before constituent execution).

## Why nothing was replaced

Replacing an accepted ADR and a 1,503-line plan is a material working decision. `docs/README.md` requires such a change to go through its ADR with the affected requirements, operations and proof gates updated together, and both packages defer adoption to the maintainer. The defects above are recorded here so they are not lost, and so the next reader of `11-parity-backlog.md` or `test-suite-design.md` knows a review exists and what it found.

The originals are recoverable in full: the parity backlog at `ac9e1a9`, the test plan at `8bff9fa`, and per-finding original-versus-proposed detail in the vendored `parity-register.json` (85 findings) and `rule-review.json` (R1–R25 dispositions).

## Decision required from the maintainer

1. **Parity backlog.** Adopt `11-parity-backlog.REVISED.md` as the replacement, or reconcile it against the current checkout first? The register is a working scope decision per ID; adopting it makes the register, not the prose, the dispatch surface.
2. **ADR 0011.** Adopt `ADR-0011.REVISED.md`? It adds truthful ownership and stage-specific release gates while preserving the `PRY` namespace and the historical core denominator, and removes unsubstantiated claims that every reference constant was correct for some company/year.
3. **Test plan.** Adopt the revised plan and corrected cases, and separately settle the no-unit-test policy? The handoff states plainly that the plan's original no-unit-test rule *"must be discussed explicitly if pure conformance/regression tests are to be added"* and that *"no authorization is inferred from this document"*. `AGENTS.md` still forbids test changes without explicit approval, so **no test was added, changed or run by this import.**
4. **Companion edits.** Apply the `D-04`, `D-06`, `D-08` and `D-10` amendments in `COMPANION-EDITS.md` to [open decisions](../open-decisions.md), and the separate-measures sentence to [the plans index](README.md)? These are proposed, not applied.
5. **Register validator.** `COMPANION-EDITS.md` proposes a small register validator and nine required checks for the maintained planning artifacts. Not written. A documentation change may propose it; any actual test change still follows repository authorization.

## Import verification

Performed on import, in place, after copying into `docs/specs/`:

```text
docs/specs/parity-plan-review    shasum -a 256 -c SHA256SUMS.txt   -> supplied manifest, all files OK
docs/specs/parity-plan-review    python3 checks/check_review.py     -> 36 total, 36 passed, 0 failed
docs/specs/testing-plan-review   shasum -a 256 -c SHA256SUMS.txt   -> 8 of 8 files OK
```

The parity archive ships its own `SHA256SUMS.txt` and `checks/`. **The testing archive ships neither** — it supplies only a `CHECKS.json` result record, so its manifest was computed on import and is labeled as such. Do not read that manifest as archive-supplied provenance.

Both checkers are document-structure and illustrative-arithmetic checks. They import no application source, compile no TypeScript, run no SQL, Worker, browser, queue or provider call, and use no company data. They cannot establish that any plan, rule or implementation is correct.

## Limits recorded by the reviews themselves

- Neither package changed a repository file, and neither ran an application suite, migration, browser journey, provider integration or company transaction.
- Parity findings name the Accounted comparison as `reference_system`, but the exact upstream repository/ref/path/symbol is **not pinned**. Until it is, no finding may be described as upstream-verified, and absence from a narrow source read is not proof of absence.
- The parity review explicitly does not reopen the application-owned replacement, and does not certify the recorded completion observations.
- Findings describe inspected source at a pinned commit, not reproduced runtime failures. A missing or wrong expectation in the plan is a defect **in the plan**, not evidence that the application misbehaved.
- Statutory rates, tax and contribution tables, reporting boxes, deadlines, per-diem and mileage amounts, declaration schema versions, e-invoicing profiles, provider contracts and credentials remain qualified inputs under [D-04](../open-decisions.md), [D-08](../open-decisions.md) and [D-10](../open-decisions.md). Nothing in either package activates a rule, rate, provider or legal profile, and neither grants test, deployment, payment, filing or production-data permission.

## Effect on packet dispatch

Until adoption is decided, treat the following as **known defects in the maintained plan text**, not as approved work:

- any `PRY-nn` dispatch that follows a preserved R1–R25 recipe verbatim;
- any implementation of `HARNESS-1`, `HARNESS-2` or `HARNESS-3`, or the `SA-H1`, `CB-R3`, `CB-X1`, `SO-H1/H2/R6/R9`, `SA-R2/R3`, `AB-R2`, `HI-R4`, `XC-1/4` expectations, as written;
- any coverage claim computed from the plan's current totals.

The specific first edits the test-plan review names are listed in its `COORDINATOR-HANDOFF.md`; the per-rule corrections are in the parity `RULE-CORRECTIONS.md`. Both are vendored and unmodified.
