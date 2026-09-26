# Companion edits to apply with the revised parity plan

Proposed documentation changes only. They are not applied to GitHub. Keep the reviewed original commit as provenance. Read current source and AGENTS.md before making the actual changes.

## docs/adr/0011-reference-parity-backlog.md

Use `ADR-0011.REVISED.md` as the proposed replacement for review. It deliberately preserves the PRY namespace and core historical denominator while adding truthful ownership and stage-specific release gates. Remove unsubstantiated claims that every reference constant was correct for some company/year or that every class-A algorithm was validated on real data.

The accepted ADR is not retroactively rewritten by this artifact. The maintainer records review/adoption through the repository's normal decision history.

## docs/plans/11-parity-backlog.md

Replace with the revised plan once adopted. Preserve the original full finding descriptions in the commit history or a dated source snapshot and retain the stable PRY IDs. The revised scope explicitly rejects bad recipes rather than silently treating the original as correct.

Do not paste the old R1-R25 recipes below the revised governance without their corrections. Keep `RULE-CORRECTIONS.md` as the detailed audit until a qualified executable specification supersedes each rule. No R rule is labelled upstream-verified while the source repository/ref/file is missing.

## docs/open-decisions.md

### D-04: applicability

Keep actual company facts as onboarding/release inputs. Clarify that required product behavior may be developed and qualified with suitable independent examples before those facts are supplied. Existing core plans already own cash method, tax treatments and payroll. Link parity as refinement/profile detail, not a claim that those product intentions were absent.

### D-06: prior-system material

Name the actual source system, registers and file formats required for the selected migration. PRY-03 may contain several candidate adapters, but the existence of six names is not a reason to implement all six. Known reviewed file imports and preserved source mappings can proceed without a live provider account. Source completeness remains a separate acceptance gate.

### D-08: rules and formats

Expand “dated parameters” to include formula structure, computation/rounding order, grouping scope, permitted format grammar and applicability. A is not a legal or correctness exemption. No missing current rule is supplied by a prior-year fallback, a tolerance or a reference result unless the actual qualified rule permits it.

### D-10: external authority and provider access

Replace the blanket prohibition on writing an adapter before PRY-01/02 with:

> Implement pure mappings, parsers, offline artifact generation and unauthenticated supported calls against explicit contracts without unnecessary credential dependencies. Integrate authenticated providers only through the reviewed credential and request-lifecycle boundary that their operation requires. Exercise live or sandbox access only with actual authorized configuration. A local adapter or simulated response is not provider acceptance, and an ambiguous remote write cannot be retried without its actual idempotency/read-back rules.

Public-rate selection does not require an OAuth vault. BankID signing does not require a general email adapter. SIE decoding does not establish workbook parsing. Credential requirements remain real for operations that need them.

## docs/plans/README.md and progress reporting

Keep the core packet count and historical scope. Add a sentence next to progress metrics:

> Core packet progress, supplemental-finding disposition and selected-release eligibility are separate measures. Applicable unresolved supplemental requirements are explicit release gates even though they are not counted as additional core packets.

Do not say all parity is necessarily scheduled after full baseline delivery. Leaf development and core-gap refinements can proceed once their actual dependencies are available. The current application replacement completion record is not reopened by an old historical code paragraph.

## docs/plans/check-plan.py / planning validator

The existing checker is expressly outside PRY semantic coverage. A documentation change can propose an additional register validator; any actual test change still follows repository authorization.

Required checks for the maintained planning artifacts:

```text
one record per stable PRY identifier and preserved rule identifier
known canonical owner / reviewed unowned status
original finding distinct from revised scope and implementation evidence
reference pin or explicit unverified/independent-requirement status
per-component A/B/C plus policy/evaluation status
known typed dependency targets
acyclic execution/readiness edges for the selected profile
no refines/relatedTo edge misinterpreted as execution precedence
conditional release gates cannot disappear from the selected readiness result
independent acceptance cases specified before an executable slice is called ready
```

A regex cannot prove tax rules correct or discover every bad recipe. Structural checking and semantic review remain separate. Do not make a huge checker itself the next platform project; one small maintained register and existing docs tooling are enough.

## Source and acceptance records

A finding's `reference_system` is currently only the named Accounted comparison. Before claiming parity, add the exact source repository/ref/path/symbol and target operation/ref. If that source is unavailable, qualify the needed behavior independently and label it as such.

Preserve actual application evidence by code/contract/runtime scope. No prior test result, source filename or proposed packet proves the new rule behavior. A document checker passing here is not a run of the repository's validation commands.
