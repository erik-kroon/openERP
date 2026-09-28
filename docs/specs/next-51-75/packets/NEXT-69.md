# NEXT-69: Spreadsheet master-data import with staged reconciliation

Priority: **P1 when applicable**. Lane: **INTAKE**.

**New deliverable:** Add typed workbook/CSV onboarding for customers, suppliers and catalog records. NEXT-44 imports accounting history, and NEXT-26 reads supplier documents, not bulk master data.

**Existing owner to extend:** Existing source retention, party/catalog revision and reviewed import-run owners.

**Required contracts:** NEXT-02, NEXT-27. These refer to released integration contracts, not an assumption that prior packets are complete.

**Crosswalk:** PRY-27/28; canonical family IMP, COM master data. Spreadsheet master-data staging differs from NEXT-12/44 financial-history imports.

**Atomic result:** No journal; staged master-data inserts/revisions and per-row receipts.

**Evidence:** R03, R05 in [SOURCES.md](../SOURCES.md). Plans establish requirements, not proven absence or behavior.

Use [00-COMMON.md](../00-COMMON.md) and [01-QUALIFIED-INPUTS.md](../01-QUALIFIED-INPUTS.md). Proposed symbols must bind to real owners. A pure helper alone does not complete this packet.

## Declare a finite source profile

The first release supports CSV and XLSX through a qualified bounded parser. XLS/ODS are explicit additional formats, not claimed because their extensions resemble spreadsheets. Retain original bytes, workbook metadata, selected sheets/ranges, encoding and parse diagnostics. Never evaluate macros, external links or spreadsheet formulas. Formula cells retain raw formula/cached value provenance and require an explicit accepted-value policy.

`MasterDataImportCapture` pins source occurrence, parser release, chosen sheet/header mapping and every source row identity. `MappingDecision` identifies type and normalization per column. `ImportRowDisposition` is create, revise, link_existing, duplicate_candidate, reject or missing_fact. An import job does not silently delete records absent from a later workbook.

## Deterministic interpretation

```text
prepareMasterImport(original):
    parse with cell/sheet/row/byte and archive-expansion bounds
    list candidate tables and headers; preserve ambiguous alternatives
    user selects exact table and column mapping
    for row:
        retain raw typed cell and source coordinate
        normalize using explicit field grammar, not formatted display guesses
        preserve identifier leading zeros and reject lost precision
        resolve existing records by stable source mapping or reviewed identity
        produce proposed typed revision plus field conflicts and missing facts
    freeze complete row count, continuation and decision inventory
```

Numeric cells are not proof of a valid organization number, bank account or postal code. Do not infer business-versus-person or EU-tax status from a guessed pattern. Date cells require a declared workbook epoch and field semantics; a date-only value must not shift timezone. Monetary prices require exact scale/currency and no IEEE-754 round-trip through application amount types.

Supplier bank details enter the existing payee-verification workflow as unverified source assertions. Import cannot activate a payment beneficiary. Catalog tax categories are suggestions until reviewed under their actual treatment profile. Unknown values are not empty strings silently overwriting verified data.

## Commit and recovery

```text
commitReviewedRows(capture,selection):
    require exact reviewed mapping, row identities and current target revisions
    apply one bounded chunk through existing party/catalog internal writers
    write row receipts/checkpoint in same transaction
    replay chunk from original identity after response loss
    record each deliberate rejection and retain source rows
```

Partial success is explicit at chunk boundaries, not catch-and-ignore inside a failed SQL transaction. A row conflict can pause the run without deleting prior successful revisions. The operator can issue a new reviewed resolution for conflicted rows. Current privacy and book scope apply on resume and download.

This packet imports master data only. Opening balances, unpaid invoices, payroll history and journal entries require their existing financial migration owners and independent controls. Selecting a supplier sheet does not grant permission to synthesize payables from a balance column.

## User interface and proof

Provide sheet/table selection, type-aware mapping, sample and whole-dataset statistics, side-by-side field conflicts and explicit complete-versus-partial status. A preview of20 rows is not proof that all2000 rows are clean. CSV export of diagnostics uses safe cells so source formula text is not executed when opened.

Example: source row keys001 and1 remain distinct unless a reviewed source identity rule establishes equality. A supplier whose verified bank details differ from a spreadsheet yields a proposed unverified revision, not an active payee change. A second delivery of the same source/capture recovers row receipts without duplicating parties.

Completion includes actual parser output, two sheets with ambiguous headers, numeric identifier hazards, target revision changes, resumable chunks and an independently reconciled imported record count. An auto-selected 'best sheet' with no review is not the workflow.
