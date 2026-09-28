# NEXT-68: Versioned BAS chart adoption and controlled annual updates

Priority: **P0 when applicable**. Lane: **FOUNDATION-REPORTING**.

**New deliverable:** Add reviewed adoption and upgrade of a reference chart without rewriting historical accounts or silently changing tax/report mappings. Existing account CRUD and historical SIE mapping do not deliver annual chart maintenance.

**Existing owner to extend:** Existing native accounts, role bindings, report mapping and qualified-release owners.

**Required contracts:** NEXT-02, NEXT-13, NEXT-49. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-14: Account changes affect active dimension requirements.

**Crosswalk:** PRY-24/30 and chart foundations; canonical family FND-03, IMP, VAT, END. Versioned chart adoption maintains stable native identities and retained historical meaning.

**Atomic result:** No journal for chart metadata; reclassification requires a separate financial plan.

**Evidence:** R03, R04, X09 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Reference versus native identity

`ChartRelease` retains origin, edition, applicable framework, exact account/code/name data, source hashes, notices and usage rights. A freely downloadable chart does not automatically license every associated instruction or commentary. Preserve source/redistribution conditions rather than bundling copied explanatory books. BAS publishes chart changes separately and emphasizes that names alone do not define full account treatment [X09].

`ChartAdoptionPlan` maps immutable reference identities to native account IDs and selected definitions. Native ID, displayed code, name, account kind, tax default and report mapping are different properties. A code rename is not automatically an economic reclassification.

## Compare and prepare

```text
prepareChartUpdate(currentAdoption,newRelease):
    verify source release/version/hash and selected company applicability
    classify changes: added, renamed, retired, split, merged, semantic_changed
    for each native account:
        retain current posted history, active plans, balance and mappings
        suggest exact/name/class mappings as suggestions only
        require explicit review for split, merge or semantic change
    create prospective accounts/mappings and selected effective dates
    enumerate affected role bindings, defaults, report rules and unexecuted plans
    seal entire change manifest with before/after meanings
```

Never derive VAT deductibility from an account code alone. Reference tax/report suggestions are corroboration for the qualified treatment owner. Do not auto-map a balance-sheet account into a sales VAT box because a source spreadsheet used a familiar label.

## Apply without rewriting history

The application transaction rechecks account and rule dependencies, creates/updates prospective definitions, applies reviewed role/report mappings and appends adoption receipt. Posted journal lines retain their original native IDs and captured meaning. Historical report snapshots retain the exact mapping release used when captured.

An old account with a balance may be closed for new posting only when existing supported settlement/correction access and report interpretation remain coherent. Do not delete the account or refuse historical reads. If the business decision requires moving a balance to a new account, prepare a separate explicit financial reclassification with source reasoning, date and approval. No hidden journal is emitted by metadata adoption.

A split requires selected rules for future postings and a separate decision about existing balances. A merge does not erase source provenance. A renamed account does not cause all old vouchers to be rendered with an invented current historical label.

## Migrations and rollback semantics

Reference release import is data under the current qualified-release owner, not SQL stored logic. Structural schema changes are forward migrations. A mistaken adoption is superseded by a reviewed prospective revision; reversing financial reclassifications, if any, is its own existing correction operation. Replaying the exact adoption returns the same result.

Existing SIE accounts and mappings remain first-class. User-defined accounts can stay outside BAS with explicit meaning and mapping, subject to the selected company/report requirements. A missing BAS adoption cannot be resolved by silently renumbering all accounts.

## UI and validation

The preview shows additions, name-only changes, semantic changes, affected balances and report/role effects. Export a human-readable mapping history and exact machine manifest. NEXT-49 receives the impacted identities, not a blanket 'all books changed' event.

Example: native account A code5000 with old expense30000 survives a reference rename. Its journal count and balance remain unchanged. A reviewed future split into A1/A2 requires a new posting rule; no historical30000 is arbitrarily divided. A proposed mapping with active unpaid plans exposes those stale dependencies.

Finish with a release import, reviewed adoption, next-edition change, preserved historical report, compatible ongoing settlement and an explicit optional reclassification. Matching account names alone does not qualify a chart migration.
