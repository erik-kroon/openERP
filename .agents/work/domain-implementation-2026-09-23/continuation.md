# Continuous implementation — next packet

User objective: keep implementing; do not focus on tests, browser or mobile.

Source-only work continues with three retained owners. No test/fixture edits, validation commands, migration application, servers, dependencies, commits or external actions.

| Owner | Slice | Forward migration |
| --- | --- | --- |
| core-gap-map | Read-only bank match candidates with effective capacities, ambiguity and reasons; never automatic matching |1600-bank-match-candidates.sql |
| commerce-gap-map | Reviewed whole-allocation payment unallocation, immutable history and effective restored capacities |1700-commerce-allocation-reversals.sql |
| compliance-gap-map | Linked carrying-basis validity enforced at schedule preparation and posting, including stale prepared paths |1800-subledger-basis-posting-guards.sql |

Root owns shared registration, current/legacy composition, cross-domain source integration and maintained status docs. Historical migrations through1510 are not rewritten. New private commerce effective-allocation views must propagate to capacity/report/correction consumers without replacing active-bank semantics. Existing standalone synthetic schedules keep their interpretation; linked bases are not legal-policy activation. No new source-completeness or readiness claim follows from these slices.

Workers report final source handoffs or real blockers only. Source review and runtime proof remain distinct. No task is marked verified from source alone.

## Integrated follow-up

1600 shared composition and Accounts/Matching + legacy UI mounts complete in source.1700 shared composition, Accounts/Payment allocation and legacy UI mounts complete; existing receipts/reports show live release/allocation-freshness overlays. Independent1700 source review found no concrete blocker.1800 source reviewed and routed schedule UI mounted. No runtime validation.

Next retained assignments: compliance-gap-map1900 exchange-rate reviews; core-gap-map2000 bank interval coverage; commerce-gap-map2100 immutable synthetic issue documents. All forward/source-only, root integration still owns shared files.

1900 rates/conversion review registered in domain+contracts/API/MCP/SQL and mounted under Reports/Exchange rates plus legacy workspace. Owner is fixing form recovery when observed rate revision changes.2100 invoice artifacts wired through Effect workflow only and mounted beside committed synthetic issue receipts; independent security source review assigned.2000 source coverage still active.
