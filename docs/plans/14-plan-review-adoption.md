# Plan review adoption: reference parity and test plan

Status: **decisions adopted 2026-09-28; textual reconciliation incomplete**. Added 2026-09-26 as import-only material. The five adoption questions were open maintainer decisions; the [owner-delegated decision pass](../adr/0015-owner-delegated-decision-pass.md) resolved all five on 2026-09-28.

**The decisions are taken. The files are not yet rewritten, and the two must not be conflated.** A decision to adopt a corrected model is not a decision to overwrite a 1,503-line plan with a 235-line replacement. Each row below records what was decided, what the integration requires, and the honest current state. Neither the accepted [reference parity backlog](11-parity-backlog.md), [ADR 0011](../adr/0011-reference-parity-backlog.md) nor the [test suite design](test-suite-design.md) / [pseudologic](test-suite-pseudologic.md) has been modified by this integration.

| Review | Reviewed commit | Files inspected at | Proposed replacement | Decisions adopted 2026-09-28 | Textual state |
| --- | --- | --- | --- | --- | --- |
| [Reference parity](../specs/parity-plan-review/README.md) | `ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb` (`parity backlog`) | same | `11-parity-backlog.REVISED.md` (1,503 → 235 lines) + `ADR-0011.REVISED.md` | ADOPT-1, ADOPT-2, ADOPT-4 | not yet merged |
| [Test plan](../specs/testing-plan-review/README.md) | `8bff9fadbcacf9d369758b967971469548834365` (`test plans`) | `ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb` | `REVISED-TEST-PLAN.md` + `CORRECTED-WORKFLOW-CASES.md` (1,223 → 743 lines) | ADOPT-3, ADOPT-5 | not yet merged |

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

## What was decided on 2026-09-28

The owner/operator has now taken both decisions. They are recorded in [ADR 0015](../adr/0015-owner-delegated-decision-pass.md) and summarised here. The defects above are retained as history and as the reason each decision was made; they are not deleted, and the accepted files are not yet rewritten.

| ID | Question | Decision | Integration requirement | State |
| --- | --- | --- | --- | --- |
| ADOPT-1 | Revised parity backlog | Adopt the corrected ownership, evidence and per-rule safety model. | Reconcile the proposed older replacement against **current** source; preserve every later valid requirement and all stable `PRY-nn` identifiers. No wholesale old-file overwrite, no verbatim unsafe R1–R25 recipe. | decision taken; merge outstanding |
| ADOPT-2 | Revised ADR 0011 | Adopt the separation of design coverage, implementation, observed evidence and selected-release readiness. | Retain the core historical denominator; derive a separate selected-scope release result rather than moving the denominator. | decision taken; ADR text outstanding |
| ADOPT-3 | Revised test plan | Adopt the corrected observable-business cases and bounded unit/property/conformance testing; retain real-PostgreSQL/workerd integration. | Derive current expected behaviour from accepted contracts and primary-source facts, not by copying an older patch. Guard-order assertions survive only where the order is a real contract — current access before replay disclosure, replay before new-work expiry, complete validation before committed effects, owner routing before constituent execution. | decision taken; cases outstanding |
| ADOPT-4 | Companion D-register edits | Apply this pass as the resolution of scope and process choices. | Replaced blanket facts/provider/reviewer blocks with affected-stage gates in the [D-register](../open-decisions.md). Preserve real facts and operational outcomes as unresolved until evidenced, and keep one authoritative register. | **done** |
| ADOPT-5 | Register validator | Implement a small derived validator — or recognise the existing one. | A passing metadata checker is not monetary, database or company-readiness proof. | **already satisfied** |

**ADOPT-5 is already satisfied and was not rebuilt.** `docs/plans/check-plan.py` validates known identifiers, owners, dependency cycles, conditional-gate references, traceability coverage, counters, trailing whitespace, local links and anchors, and `git diff --check`. That is the derived metadata validator the decision asks for, and it runs on every planning change. Building a second one would duplicate it and add a second place for planning metadata to drift. Its success proves metadata consistency only, exactly as the decision states.

**HARNESS-1 is rejected, and the reason is architectural.** It requires the runtime role to be unable to write application tables, which [ADR 0010](../adr/0010-application-owned-accounting-replacement.md) and `AGENTS.md` explicitly assign to the trusted application. Implemented as written it would reject the intended installation, conflate a backend database identity with an end-user identity, and invite RLS/GUC tenant identities back. Tests must establish that unauthorised callers cannot misuse those operations at their real admission boundary, not that valid application writes are forbidden.

**Two classifications must not be merged.** A test-plan error is a defect **in the plan**, not a proven runtime defect. And a planning defect is not automatically a code defect: inspect composed constraints before claiming a missing redundant trigger is a failure, and do not add a trigger for an invariant the application already enforces.

The originals are recoverable in full: the parity backlog at `ac9e1a9`, the test plan at `8bff9fa`, and per-finding original-versus-proposed detail in the vendored `parity-register.json` (85 findings) and `rule-review.json` (R1–R25 dispositions).

## Questions closed, and the work they leave behind

The five questions below were open when this file was written on 2026-09-26. They were answered on 2026-09-28 and the answers are in the table above. They are kept here as the record of what was actually asked, because the shape of the questions shows what the review was for.

1. **Parity backlog.** *Adopted as a decision, reconciled rather than copied.* The register is a working scope decision per ID, which makes the register, not the prose, the dispatch surface. What remains is the textual merge: bring the corrected ownership, evidence and safety model into the current file without losing requirements added since `ac9e1a9`.
2. **ADR 0011.** *Adopted in principle.* It adds truthful ownership and stage-specific release gates while preserving the `PRY` namespace and the historical core denominator, and it removes unsubstantiated claims that every reference constant was correct for some company/year. What remains is the ADR text.
3. **Test plan, and the no-unit-test policy.** *Both settled.* The revised plan and corrected cases are adopted; the policy question is resolved as a bounded standing permission recorded in `AGENTS.md` and D-09. The original handoff's condition — that the no-unit-test rule "must be discussed explicitly if pure conformance/regression tests are to be added" — was that discussion, and it happened. **No test was added, changed or run by the import**, and the decision pass itself executed no test.
4. **Companion edits.** *Applied.* The D-04, D-06, D-08 and D-10 amendments are now in the [D-register](../open-decisions.md) as affected-stage gates, and the separate-measures sentence is in [the plans index](README.md). Proposed is no longer the word for them.
5. **Register validator.** *Already satisfied.* `docs/plans/check-plan.py` performs the derived metadata checks. Nothing further is written.

### Remaining integration work, and its order

This is documentation work, sequenced so the planning gate keeps passing:

1. Merge the corrected parity model into `11-parity-backlog.md`, preserving all `PRY-nn` identifiers and every requirement added since the review's revision.
2. Write the revised ADR 0011 as a dated amendment of the existing record rather than a replacement file, so the original decision text and its denominator survive.
3. Bring the corrected observable-business cases into the test plan, deriving current expectations from accepted contracts and primary-source facts.
4. Build the selected-case release view, which includes required conditional edges without changing the historical 53-packet count or 101-edge DAG.

Until steps 1–3 land, **the accepted files remain the authority for text and the adopted decisions remain the authority for intent**, and an implementer must read both. The contradictions listed under *Effect on packet dispatch* below still stand as live constraints.

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
