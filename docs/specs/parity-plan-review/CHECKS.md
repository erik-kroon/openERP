# Checks actually performed

Ran the local design checker against this generated package: **36/36 named checks passed**. It checks stable identifiers, the proposed 85-row supplemental DAG, references, Markdown structure and explicitly illustrative counterexamples to the written recipes.

It does not run OpenERP, PostgreSQL, workerd, providers or the repository's `check-plan.py`. It does not reproduce the upstream comparison or qualify a current statutory profile. The original 53-packet graph plus all release gates was not independently reconstructed; this is recorded rather than claimed as passed.

Reproduce with `python checks/check_review.py`. Exact results are in [checks/results.json](checks/results.json). The checker is local to this artifact and was not added to the application repository.
