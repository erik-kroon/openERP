# Whole-year accounting proof

1. **Frame.** State the done predicate as something countable ("all 126 units merged, each ledger-verified `unit-test-verified` or better"). Quantify scope: units, rough effort, expected stacks, and the wall-clock budget. If one agent could finish inside that budget, stop here and run Autonomous run instead. Collapsing must not depend on another document being present. It means do the work directly in this session, plain workers where they help, verification inline, landing as you go, and none of the store, register, or pilot machinery below. Schedule landing against the budget. By roughly 70% of it, stop spawning and land what is verified. Name the tracks per project. A contested decomposition or one-way door goes through the arena skill before the pilot. Present the framing once. Reversible prep proceeds without waiting.
2. **Install the runtime.** Run `orch init`. Open the trail via the show-me-your-work skill, write the standing orders before any spawn, and seed `frontier.json` from existing PRs with `orch frontier set --repo <repo-dir>`.
3. **Pilot.** Push one unit through the whole path: brief, worker, verification, stack entry, ledger row, merge. The pilot exists to falsify the brief template, the verify recipe, and the unit size while that costs one agent instead of fifty. Fix the contract from pilot evidence before any fan-out. Scale the pilot to the unit. On programs of near-identical cheap units, the first unit is the pilot, run as a normal unit with its verify command inline, and fan-out starts the moment it lands. The dedicated pilot pipeline (separate verifier agent, audit gate) is for expensive or novel unit shapes, not for clone-units where a serialized pilot has nothing to falsify.
4. **Scale.** Spawn a rolling window of workers up to the in-flight cap, refilling as children finish. Blocking batches pay the slowest child of every batch. Spawn track sub-coordinators only past the one-drain threshold in Roles. Recompute ready work after each drain. Relay upstream reports into downstream briefs. Keep sibling communication upward only. The sampled brief audit runs alongside the wave it samples and stops the next refill on failure, not the current one.
5. **Drain.** Run the queue discipline below at every drain point.
6. **Land.** Landing is continuous, never a terminal phase. Integration starts with the first verified unit and runs alongside the remaining waves. On heavy repos the stacker is a standing role from wave one, integrating as units verify. On repos where local git is cheap, the coordinator lands verified units itself per Roles. Keep the frontier green before upper-stack work. Stack safety governs. Advance `frontier.json` only on merge or reported new head SHAs.
7. **Close.** Drain the final inbox, reconcile every spawned agent to a terminal row (done, abandoned, zombie-reconciled), confirm the predicate on the real artifact, confirm every landed PR has a verdict for its current head SHA, audit the trail per show-me-your-work including its cross-model review, encode recurring corrections into `preferences.md` or the brief template. Leave the store intact. It is the postmortem.


## Current work

- Packet 1. Capture an isolated exact snapshot and verify frozen install, integration, changed-file checks and broad runtime E2E.
- Map packets 2 through 20 to real owners and proof obligations.
- Bind company facts to unknown or supported synthetic profiles without inventing actual registrations or methods.

## Throughput checkpoint

The owner inventory is complete as source grounding. Cash admission is locally verified and integrated into the isolated baseline. Runtime compatibility repair and proof-tool provenance repair have separate writers and artifact ownership. Company-profile grounding incorporates the owner's reported facts without real activation. Checks serialize per worktree. Integrated passing runtime evidence still gates downstream implementation. No PR or merge claim exists yet.

## Ownership swarm

1. Frame
2. Fan out
3. Aggregate
4. Report

The three partitions are baseline checks, packets 2 through 10, and packets 11 through 20. All agents are read-only. The baseline writer owns only its isolated worktree.

## Recovery architecture

1. Ground
2. Sketch
3. Agree
4. Implement
5. Scrap

Ground the existing recovery refusal before choosing two candidate designs. The required outcome is application-level restricted read recovery with writer/provider activation still separately controlled.

## Superseding throughput checkpoint

Packet1 verified269/269 unchanged-source runtime, independent acceptance retained. Company-profile prerequisite accepted and integrated at818f790, fast/full and seven focused E2E passed; docs qualification addedbfb8a0b. Evaluation capture prerequisitec999c78 awaits independent review and strict recovery qualification. Separate0050 forward FK validation underway after two independent authentic NOT VALID refusals. Restricted recovery prototype supports selected limited read mechanism; combined confinement prototype underway. Root runs no current checks. Original checkout product edits preserved. Shared0049/0050 identities are disjoint; final combined qualification is sequential. No packet2/3 completeness or PR merge claim.
