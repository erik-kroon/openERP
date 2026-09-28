# NEXT-73: AGI submission and stable individual correction outcomes

Priority: **P1 when applicable**. Lane: **PAYROLL-DELIVERY**.

**New deliverable:** Add actual employer-declaration delivery and period/item outcome tracking after the existing AGI producer. Do not recalculate payroll, repeat paid-payroll correction or equate file preparation with signing.

**Existing owner to extend:** Existing payroll declaration/pay-run owners, private payroll admission, external delivery and fulfillment.

**Required contracts:** NEXT-21, NEXT-49. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-36: The selected submission changes previously paid/reportable compensation. NEXT-47: The actual selected protocol uses an independently qualified signature adapter; do not substitute generic signing.

**Crosswalk:** PAY-04 external-outcome requirements; canonical family PAY-04, END-07, OPS-03. AGI submission consumes NEXT-21/36 output and does not replace payroll accounting.

**Atomic result:** No payroll/cash mutation; private declaration-item submissions and outcomes.

**Evidence:** R02, R08, R09, X10, X14 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Exact private declaration manifest

`AgiSubmissionManifest` pins employer, actual reporting period, declaration revision, employer totals, complete selected individual-item identities, exact artifact hash, qualification release and original/replacement purpose. Each item preserves the existing employer/period/payee/specification identity and the prior filed item it replaces. A new request ID is not a new employee specification.

Read, list, replay, status and export all require current private payroll permission before returning sensitive content. Jobs carry references rather than names, salaries or credentials. Aggregate operational dashboards must not expose private employee rows through error details or delta history.

The official service/permission guidance distinguishes preparatory registration rights from rights to sign and submit [X10/X14]. Implement the actual selected permission ceremony. General app membership, a payroll review approval or an API read permission cannot substitute for the external right to submit.

## Build from the existing declaration owner

```text
prepareAgiSubmission(declarationRevision,channel):
    current private scope; capture saved paid/reporting facts and original filed history
    load exact existing AGI artifact and its independent validation result
    require employer totals and individual membership reconcile under the release
    for each corrected item:
        retain original specification identity
        verify the intended replacement or deletion behavior in this exact API/file profile
        preserve every unaffected external item unless the operation explicitly replaces it
    compare current authority period/item state where the service supports it
    seal payload, affected membership, expected external state and signing purpose
```

The original earnings period, adjustment accounting date and declaration reporting period remain independent under ADR0014. An August entitlement corrected in an open September period does not automatically belong in either month's AGI merely from those dates. PAY-04's qualified reporting determination remains authoritative.

Some reported auxiliary facts can have a different correction protocol from financial individual items. The current official guidance, for example, distinguishes absence information handling [X14]. Preserve unsupported correction branches explicitly rather than promise that one replacement action fixes every field.

## Delivery and outcomes

Use the existing admitted external-attempt transaction, outside-transaction call and authentic observation append. Normalize only documented service states. A technical file acceptance, draft registered in the period and signed employer declaration are different outcomes. If the selected channel supports partial item validation, retain per-item results and aggregate completeness; one successful item cannot mark the whole manifest accepted.

```text
reconcileAgiOutcome(attempt,rawOutcome):
    verify service origin, environment, employer and reporting interval
    map returned item identities to the exact submitted membership
    refuse unknown/conflicting item mapping into an investigation case
    record complete/partial/pending/rejected meanings according to actual service contract
    append outcome observation; update fulfillment only for its required predicate
    do not change wage postings, withholding, actual cash or tax-account balance
```

For response loss, recover the same attempt through provider correlation/read-back. If no safe mechanism exists, keep the outcome unknown. Do not append another employee item by changing its specification number. A later original-item correction gets a new declaration revision with the same stable item identity and new explicit authorization.

## Completion and reader behavior

The payroll UI shows paid-source basis, saved declaration values, original/replacement links, individual diagnostics and the next real human action. Retained old declarations remain readable even if current source facts change. Where external signing must happen in Skatteverket's service, link that action without pretending OpenERP signed on the person's behalf.

Prove that correcting one of ten employees does not delete or duplicate the other nine, that an unchanged-key retry adds no item, that private-grant revocation stops historical/replay reads and that submission changes no payroll journal. Exercise the selected schema/service version with authorized test identities. Exact statutory tables and credentials remain input dependencies, not a new payroll calculator inside this packet.
