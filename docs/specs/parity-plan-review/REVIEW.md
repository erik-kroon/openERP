# Review of the parity-backlog commit

**Reviewed commit:** `ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb` (`parity backlog`, 26 September 2026, 12:17:09 UTC). **Status:** proposed review and revised planning documents. No repository files were changed. No application, database or provider test was executed.

## Verdict

Keep the parity inventory, the PRY namespace, the exact-money boundary and the distinction between implementation and evidence. **Do not dispatch the preserved recipes unchanged.** Several contain internally contradictory or financially unsafe instructions, and some “unowned” assertions are contradicted by the existing maintained plans.

The plan is a useful requirements notebook. It is not yet a reliable execution contract. Its largest problems are not insufficient detail or too few tasks; they are inaccurate ownership, unsafe algorithm adoption and dependencies that turn a useful comparison into a parallel roadmap.

The remedy is to retain all 85 finding IDs while attaching them to existing owners, rejecting bad reference behavior and qualifying genuinely new profiles. Do not create 85 independent implementations on top of the 53 core packets and previous NEXT work.

## What is worth preserving

The plan explicitly says reference presence is not correctness, prohibits floating-point money adoption, separates dated data/legal judgment and keeps proposed work distinct from execution and acceptance. It also values refusal behavior and provenance. These are the right principles. [P01]

The application-owned architecture is already the selected baseline: Effect owns decisions and transaction composition, PostgreSQL holds narrow integrity and effect-mq runs in a separate Bun process. Current repository evidence reports the local replacement completed with scoped runtime observations. This review does not rerun or independently certify those observations; it also does not reopen that migration merely because older sections still mention historical SQL. [C01, C06]

## Stop-ship issues in the plan text

“Stop-ship” here means do not supply that instruction to an implementing agent as a normative algorithm. It does not mean the current application was observed shipping that defect.

| Finding | Basis | Required change |
|---|---|---|
| Detector failure becomes permission | PRY-39 says failure never passes; R11 returns CLEAR when detection fails without force. | Fail closed for the guarded financial action; retain unavailable/incomplete diagnostics and allow unrelated reads/preparation. Bind conflict resolution to full current facts and authority. |
| Skipped source history is balanced away | PRY-25 asks for an adjustment voucher absorbing skipped/unmappable vouchers. | Retain the incomplete source and block the affected admission. Only a separate evidenced accounting correction or reviewed reduced-history opening may change the recognized basis. |
| Bank movements can disappear from totals | PRY-35 calls ignoring a legal escape hatch and excludes ignored rows from account totals. | Suppress suggestions or link proven duplicate observations, not genuine statement movements. Independent opening/movement/closing controls remain intact. |
| Cash-method algorithm loses year-end recognition | PRY-50/R23 use payment-date-only logic and a single existing-voucher flag. | Use disjoint recognition coverage, eligible unpaid year-end recognition and no duplicate tax when later settled. This already belongs to COM-02. |
| Sick-pay formula combines first-day removal and karens | R9 excludes a day from sick pay and adds a waiting deduction. | Quarantine the formula, rederive the applicable schedule/entitlement/deduction case and validate independently. New percentages alone do not fix it. |
| Peppol totals omit required terms | R21 conflates line/document allowances and excludes tax/prepaid parts from its due calculation. | Use the full exclusive/tax/inclusive/prepaid/rounding graph and semantic validation. |
| VAT formula is circular/unnamed | R15 defines an “investment-return box” by subtracting itself. | Replace with a named qualified acyclic box graph and exact contribution lineage. Do not silently guess the intended formula. |
| Correction receipts contradict each other | PRY-72 says not the original receipt; R20 says the original, not the correction. | Separate stable reporting item, immutable declaration revision and each attempt's own receipt; retain originals as baseline/history. |
| Zero-net payroll can be dropped | R24 says a zero-amount run posts nothing after discussing zero employee net. | Omit zero cash instructions only. Gross earnings, withholding, contributions and benefits can still require accounting and reporting. |
| Search determinism is mistaken for uniqueness | R6 retains one best cover and discards equal alternatives; caps are not returned as coverage limits. | Return ambiguity and search-completeness information. Existing allocation execution revalidates selected legs. No auto-apply from tie-breaking alone. |

The exact diagnoses and replacement contracts are in [RULE-CORRECTIONS.md](RULE-CORRECTIONS.md). Current official sources were used for the narrow sick-pay, cash-method and Peppol comparisons; remaining statutory mechanisms are marked for qualification rather than presented as newly verified law. [E01–E04]

## 1. Correct ownership before creating implementation work

### Payroll is planned already

The parity document says no pay-run record exists “in the code or in any plan”. The existing payroll design explicitly names `PayRunRevision`, `PayRunPosting`, `PaymentInstruction` and `PayrollDeclaration`; PAY-03 owns frozen run approval/posting and correction. That contradicts the claim about plans, whether or not runtime payroll implementation is complete. [P03, C03]

Correct wording:

> The employee foundation does not establish full payroll delivery. Refine PAY-02/03 with a concrete frozen-run contract and supported calculation profile; verify the current source implementation before assigning the remaining delta.

PRY-59 can remain as a traceable refinement. It must not own a second pay-run state machine. Its `paid` and `booked` states should be independent, not a forced ordering in which payment must precede accrual posting.

### Providers are not wholly absent as requirements or infrastructure

OPS-03 already owns durable provider attempts and uncertain outcomes, and the bank connector has scoped consent, source retention and cursor behavior. This does not prove a production token vault or every accounting-provider adapter exists. It does refute “no cross-cutting infrastructure is named anywhere.” [C04, C05]

Reframe PRY-01/02 around the missing credential and call-policy deltas for a selected provider. Keep provider-specific contracts instead of forcing every anonymous public data source through a vault. Do not add another queue/fencing runtime beside effect-mq.

### Ordinary accounting, credits, cash method and reporting already have owners

COM-02 names recognition under accrual/cash profiles. COM-04 owns credits and owner corrections. END-06 owns format-specific exports. IMP-04/05 own allocation and independent reconciliation. These are not all green implementations, but they are not ownerless product intentions. [C02, C07, C08]

The revised register lists the canonical owner for every PRY finding. Those owner relationships are proposals grounded in the existing plan and must be checked against the actual current code before dispatch. They are not hidden new edges in the mandated dependency DAG.

## 2. A/B/C must classify the decision, not only the numbers

The current distinction between algorithms, dated parameters and legal judgment is valuable but applied inconsistently. Bank clearing ranges are classed A. Statutory rounding/aggregation order is treated as A. Match thresholds are called A. Fiscal-year maximum spans are grouped with pure parser behavior. Those are not all externally unauthoritative algorithms. [P02–P08]

Keep A/B/C, but classify a component as:

- **A mechanism:** a reviewed exact sum, graph traversal, immutable merge or check-digit arithmetic with its preconditions.
- **B rule-bearing behavior/data:** formula shape, aggregation/rounding order, format grammar, date adjustment, bank ranges, threshold meaning and rates.
- **C judgment/applicability:** whether this employee, document, taxpayer, event or signature qualifies.

Record product policy and empirical heuristics separately from statutory authority. A confidence floor may be an acceptable product policy after evaluation; it is never automatically legal permission. Even an A algorithm needs correctness review, boundedness and independent examples before adoption. The phrase “the reference algorithm was validated on real data” needs actual cited evidence, not an assumption of reference maturity.

## 3. Stabilize reporting metrics without hiding real prerequisites

Keeping the 53 core IDs and their historical completion denominator is reasonable. It is not reasonable to freeze all operational dependency edges while placing new blocking prerequisites only in prose. That yields a core graph which can say “ready” while an applicable prerequisite outside it is unfinished. [P01, C02]

Use three views:

```text
Core implementation progress:     existing 53 IDs, unchanged historical scope
Reference finding disposition:    85 PRY IDs, owned/refined/new/deferred/rejected parts
Release eligibility:              all applicable core + supplemental acceptance gates
```

A company/profile release cannot use the first percentage as its readiness predicate. A separate typed gate graph records `refines`, `requires_contract`, `requires_implementation`, `requires_qualified_rule`, `requires_external_access` and `blocks_release_when_applicable`. Validate that graph alongside the baseline index. Do not represent all relation types as one directionless prerequisite column.

The existing parity file explicitly says `check-plan.py` does not see the supplemental packets. A passing core checker is therefore not evidence that the PRY graph, rule references, ownership or contradictory states are coherent. [P09]

## 4. Remove false serial blockers

The provider section forbids writing an adapter until credential storage and shared calls exist. That blocks offline Peppol generation, local document reading and anonymous rates unnecessarily. A native SIE exporter also need not wait for multi-year import undo, nor does an opening parser fundamentally need workbook support. [P02–P05]

Separate gates:

| Stage | Required evidence |
|---|---|
| Specification/leaf implementation | Known input/output semantics, supported cases and ownership |
| Application integration | Released tx-passing ports, schema/permissions and dependencies |
| Qualified calculation/format | Pinned rule/data/schema and independent expected outputs |
| Connected provider exercise | Actual credentials, environment, consent and documented outcomes |
| Real-company release | Actual applicability, full source coverage and independent reconciliation |

This permits useful independent work without pretending missing credentials or legal facts have been solved. Do not replace these explicit gates with an all-encompassing framework-first task.

## 5. Reference scope must be reproducible

Folder names and pseudocode are not adequate evidence for adopting exact rules. The reviewed root tree contains no committed `references/` directory; attempting `references/accounted/lib` at this pin did not resolve. This does not say the author lacked a local checkout. It means the plan does not provide enough source identity to reproduce that comparison from the reviewed commit. [C09]

Each adopted finding needs the reference repository, exact commit, path, symbol/range and intended behavior; the target operation/file/profile and inspected commit; observed implementation versus documented requirement; and the precise new delta. Where upstream evidence is missing, retain the finding as a candidate and use independently reviewed requirements to implement needed core behavior. Do not claim verified parity with an unspecified target.

## 6. Use complete journeys, not 85 independent foundations

A practical first priority is still a usable accounting loop around the already matched documents:

```text
Existing retained source/match
→ correct native recognition or settlement operation
→ exact approved effects
→ current bank/control reconciliation
→ supported VAT/report artifact
→ known remaining cases
```

Prioritize PRY-05/24/31 only where source linkage/mapping is missing; PRY-41 for correct comparable values; PRY-33/39/42 for assisted discovery routed into existing accounting owners; PRY-55/56 for the selected tax profile; and PRY-32/85 for truthful usable outputs. Correct the dangerous import/ignore/residual recipes before they become shortcuts in this path.

Treat supporting pure helpers as small components within those journeys. Select one actually required accounting/bank adapter rather than implementing six providers at once. Payroll and ROT/RUT are conditional company profiles, not mandatory waits for every AB. The improved register preserves broad future scope without claiming every row belongs in the first release.

## 7. Agent efficiency should be measured, not imposed through extraction cost

R25 mandates two readings at different tiers and calls them independent. The plan provides no evidence of their statistical independence or superiority for every input. Native XML, text or reviewed receipt associations should not incur two model passes by default. [P09]

Preserve the genuinely useful part: field-level provenance, separate conflicting/unknown states, no model self-confidence as authority and immutable reviewed history. Add staged extraction: structured/native first, deterministic checks, then targeted escalation for ambiguous/high-risk fields under a recorded budget. Measure field error, unresolved review work, tokens and latency on independent cases. Never optimize by concealing unreadable facts.

## What was produced

- A revised parity plan preserving PRY-01 through PRY-85 and the original group organization.
- A source/owner-aware 85-row machine-readable register with proposed dispositions and dependency changes.
- A complete R1–R25 audit and corrected contracts for the critical rules.
- A proposed ADR 0011 replacement and narrow companion edits.
- A coordinator handoff and local document/counterexample checker.

These artifacts are proposed replacements, not applied commits. The checker verifies this dossier's identities, dependency consistency and illustrative arithmetic only. It does not run the repository's `check-plan.py`, application tests, migrations or provider integrations. The full upstream comparison and all statutory rule sets remain unverified; the review states exactly where its evidence comes from.
