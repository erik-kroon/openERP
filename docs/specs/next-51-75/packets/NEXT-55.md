# NEXT-55: Periodisk sammanställning with correction lineage

Priority: **P1 when applicable**. Lane: **TAX-REPORTING**.

**New deliverable:** Add EU-sales-list preparation, versioning and delivery handoff. VAT-return calculations and generic annual filing do not supply this distinct reporting obligation.

**Existing owner to extend:** Existing reporting snapshots, qualified releases, deadline/fulfillment and external-delivery infrastructure.

**Required contracts:** NEXT-04, NEXT-49. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-52: The selected statement includes general-rule cross-border services. NEXT-53: The selected statement includes qualifying intra-EU goods.

**Crosswalk:** PRY-47/55 and EU reporting requirements; canonical family VAT, END-06/07. EU statement artifacts and correction history are not the ordinary VAT return.

**Atomic result:** No journal; statement artifact, correction membership and submission observations.

**Evidence:** R03, X02, X03 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Scope and identities

Consume the exact qualifying sale facts produced by the EU service/goods owners. A service-only company needs NEXT-52, not implemented goods handling; NEXT-53 is conditional on goods activity. The combined dependency list is a coverage map, not permission to block a service-only release on irrelevant goods work.

Retain a `SalesListPeriodDecision`, a complete frozen source set and a `BuyerCategoryTotal` keyed by reporting entity, period, buyer VAT identity and reporting category. Reporting cadence is determined independently from VAT-return cadence using the qualified company/activity history. The official guidance distinguishes goods, services and combined activity and their correction rules [X02/X03]. Do not copy a VAT period ID and assume equivalence.

## Calculation and correction

```text
prepareSalesList(period):
    decide period/cadence from applicable rule and actual activity history
    capture all qualifying sources at one recorded cutoff
    require all necessary buyer identities/conversions and exclusions explained
    group exact book-currency consideration by buyer identifier and category
    apply the selected reporting-rounding rule at its specified grouping level
    retain raw sums, filing integers, residuals and source membership

prepareCorrection(originalFiled,changedFacts):
    for each affected buyer/category:
        if original source was wrong:
            compute corrected TOTAL for original reporting period
            retain original filed row and explicit replacement identity
        if later consideration changes:
            emit the qualified delta in the applicable later period
    require no implicit conversion of a later credit into an original-error correction
```

The official rule distinguishes replacing an erroneous original buyer total from reporting a later consideration adjustment [X03]. Zero and negative rows, identifier changes and empty-period obligations follow the selected format/rule. Do not silently drop negative values or send a nil list merely to mark the task done.

No journal is produced. This report consumes tax/supply facts without recognizing another sale. If a source correction requires accounting, that source owner completes the approved financial change before the successor report capture.

## Artifact and external outcome

Seal exact reporting data and the selected official file/service format. Render and validate outside financial locks, then attach immutable bytes and validation results. The first operational slice can provide an authorized official file-transfer handoff with actual retained receipt evidence. A direct API is used only when its actual specification and access are qualified. No guessed endpoint or screen automation is introduced.

Prepare, reviewed, transferred, submitted and authority receipt are separate states. Duplicate transfer uses the same external attempt identity where the provider supports it; an uncertain outcome stays unknown. Replacement/correction submissions link to the original scope and proof. NEXT-49 verifies typed receipts rather than accepting a text 'filed' flag.

## Reconciliation and completion

Reconcile qualifying sale totals to the corresponding VAT/supply facts at the same cutoff, with an explicit bridge for differences in reporting period, foreign conversion or correction treatment. Totals that happen to agree do not prove complete buyer membership. Show excluded categories, missing identifiers and a buyer drilldown to issued invoices and credits.

Synthetic example: buyerA services60000+40000 yields100000 for that category. An original source correction to the second supply at35000 produces a replacement total95000 for the original period, not a new35000 sale. A later contractual credit5000 instead follows the later-period adjustment rule. These amounts illustrate identity semantics, not reporting thresholds or due dates.

Completion requires actual capture, retained file, one original and one correction path, access after revocation and an observed authorized handoff outcome. A CSV grouped by buyer without cadence, correction lineage and source reconciliation is only a leaf.
