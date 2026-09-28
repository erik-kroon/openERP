# Dossier checks and limits

The local checker completed with **741/741 checks passing** and zero failures. That comprises **572 structure, dependency, document and link checks** plus **169 independent arithmetic, finite-model and published-vector checks**.

The dependency review covers this new 25-node wave, including its declared conditional edges. Earlier task IDs are validated references to external contracts, not a newly audited 125-node implementation graph. A distinct `new_scope` field records the intended non-overlap; that does not prove there is no equivalent unreviewed code or uncommitted work.

## What the model checks establish

The examples evaluate exact rounding, conserved cost splits, retainer release, provision targets, tax adjustments, payroll/capital examples and small explicit authority/payment states. A serialized mandate-budget model checks both possible orderings of two consumers. This is **not PostgreSQL concurrency proof**. A finite payment search demonstrates bounded result semantics, not a production optimization or real bank-liquidity guarantee. Refund and provider models contain no network calls.

[The machine-readable report](checks/results.json) records each named assertion. [The standalone checker](checks/validate.py) runs with Python's standard library:

```bash
python3 checks/validate.py
```

The checker is delivered in this design package only. It has not been added to the application repository. It does not import OpenERP, compile Effect, execute SQL, launch a Worker/Bun handler, use company records, contact providers or qualify legal rule releases.

No application, database, browser or external acceptance result is inferred from these checks. Use the packet's required supported/refusal/replay/race/correction observations when implementing it under the actual repository authorization.
