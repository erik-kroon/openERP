# NEXT-70: Structured bank-statement ingestion with exact entry lineage

Priority: **P0 when applicable**. Lane: **BANKING**.

**New deliverable:** Add bank-file decoding and controlled admission, initially one qualified camt.053 profile. Plaid windows and provider-revision semantics do not parse a bank statement file.

**Existing owner to extend:** Existing source intake, statement/observation identity, bank-source revision and reconciliation owners.

**Required contracts:** NEXT-09, NEXT-10. These refer to released integration contracts, not an assumption that prior packets are complete.

**Conditional integrations:** NEXT-40: The statement belongs to a native foreign-currency cash account.

**Crosswalk:** PRY-08 and bank-format requirements; canonical family IMP-01/03/04. Structured bank-file decoding reuses NEXT-10 admission instead of duplicating Plaid windows.

**Atomic result:** No journal; bank-source statement/observation admission.

**Evidence:** R03, R05, X08 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Selected profile and source model

`BankStatementFormatRelease` pins actual bank, message/schema version, currency/date/entry rules and complete supported record families. Initial camt.053 support is not automatic camt.052/camt.054, MT940 or every bank's XML. File-based import remains usable without a connected bank feed. Acquire the selected bank's actual message guide and independent sample before claiming compatibility [X08].

Retain whole file hash/occurrence, message ID, account identifier, statement ID, period, opening/closing balance types and complete entry/detail positions. Provider entry IDs and detail IDs are source identities only under the selected provider's documented uniqueness. Missing references remain explicit, not a hash of amount/date presented as an authoritative bank ID.

## Decode amounts once

```text
parseStatement(bytes,profile):
    strict bounded XML parse with external entities/network resolution disabled
    verify namespace/schema and exact bank/profile selectors
    select the qualified booked statement balance types
    for entry:
        retain entry amount/currency, direction, status, reversal indicator and dates
        parse nested details without counting entry PLUS details as separate money
        if detail sums reconcile under profile:
            emit supported detail observations with link to parent entry
        else:
            retain entry-level money and unresolved-detail diagnostic
        apply direction/reversal semantics exactly once under the format rule
    prove opening + qualified movements == closing per currency and interval
    retain unknown/nonbooked/balance entries separately
```

Available, booked, credit-limit and forward-available balances are not interchangeable. Pending entries may be retained without being admitted as final booked observations. A returned payment can be a real opposite cash movement rather than deletion of the original. Dates keep bank booking and value meanings separate.

## Admission and overlap

Prepare a complete immutable import plan with source controls and duplicates/overlap candidates against existing file and feed observations. Actual matching uses current bank-source owner identities, including same-event adoption where established. Identical amounts are not enough to deduplicate. Changed bytes under an identical provider statement identity are a revision/conflict, not silent replacement.

Admit observations in bounded complete groups through NEXT-10's application port. It creates neither journal nor automatic invoice settlement. Store source/provenance links, published version and command receipt together. Correction of an already reviewed/matched source raises the existing impact lifecycle; it does not automatically reverse accounting.

For long statements, fixed captured membership and final control totals govern paging. Do not label the first successful chunk as a complete reconciled period. Independent file controls cannot be adjusted to make native loaded rows agree.

## Views and completion

Show source file, exact message/profile, account, balance types, entry/detail tree, all exceptions and coverage. A rejected row remains visible with its amount. The bookkeeping work queue may subsequently propose matching or recognition, but file import itself does not decide tax treatment.

Synthetic statement opening100000, entry debit30000 with two details10000/20000 and credit5000 yields closing75000. Count the debit once, not60000. A second file containing the same confirmed entries links existing occurrences. An unqualified reversal flag is a diagnostic, not an extra negation guessed by the parser.

Complete with an actual selected-bank file, independent amount/control check, duplicate/overlapping file+feed delivery, detail mismatch, pending-to-booked event and corrected statement. Native foreign account support depends on NEXT-40 only where applicable; SEK-only import does not wait for foreign-cash implementation.
