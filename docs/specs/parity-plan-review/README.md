# OpenERP parity-plan review and revised planning package

**Review target:** `ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb`, “parity backlog”. This package critiques and improves that existing plan. It does not add another NEXT task wave, modify GitHub or implement the accounting product.

## Read in this order

1. [REVIEW.md](REVIEW.md): verdict, concrete defects and sequencing recommendations.
2. [11-parity-backlog.REVISED.md](11-parity-backlog.REVISED.md): proposed replacement preserving all 85 finding IDs and subject groups.
3. [RULE-CORRECTIONS.md](RULE-CORRECTIONS.md): all 25 preserved-rule audits, with corrected contracts and counterexamples.
4. [COORDINATOR-HANDOFF.md](COORDINATOR-HANDOFF.md): apply the corrected plan through the existing owners.

The [proposed ADR](ADR-0011.REVISED.md) and [companion edits](COMPANION-EDITS.md) keep documentation consistent. [parity-register.json](parity-register.json) preserves original versus proposed prerequisites, canonical owner links and classification decisions. [rule-review.json](rule-review.json) records the R1-R25 disposition. [SOURCES.md](SOURCES.md) and [source-manifest.json](source-manifest.json) identify the actual reviewed evidence.

## What changes

The parity list becomes a source/owner-aware inventory feeding existing operations. Deterministic formulas are not assumed safe. Policy-bearing order and thresholds are qualified, unsafe recipes are rejected and code/credential/company gates are separated. Core packet progress remains a separate metric from complete selected-release eligibility.

The source review disproves several absence claims about existing plans. It does not prove the runtime implementation of every referenced capability or reproduce the unpinned Accounted comparison. The new register deliberately states those limits rather than inventing evidence.

## Validation

The local [design checker](checks/check_review.py) checks this dossier and its illustrative counterexamples. [CHECKS.md](CHECKS.md) and [checks/results.json](checks/results.json) report what was actually run. No repository test suite, migration, provider integration or company transaction is exercised by this package. No font or third-party source implementation is included.
