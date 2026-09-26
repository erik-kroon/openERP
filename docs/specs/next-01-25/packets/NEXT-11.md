# NEXT-11: Separate complete-book SIE4E export

**Edition v2: application-owned Effect implementation.** Replaces this packet in the earlier SQL-owned dossier. Read [the common contract](../00-COMMON.md), especially C4 through C10. Existing financial algorithms and bounded scope below are retained; implementation ownership is revised.

## Application and persistence boundary

| Responsibility | Owner |
|---|---|
| Named Effect operations | `apps/api/src/application/reports/sie4e.ts` or the existing equivalent owner |
| Tx-passing reads and DML | `apps/api/src/db/reports/sie4e.ts` or the existing equivalent owner |
| Pure calculation | Complete-book SIE encoding and semantic comparison |
| Atomic scope | Capture is consistent; rendering/validation is external to financial tx; attachment is a short tx. |
| Prerequisites | NEXT-02, NEXT-13 |
| Reserved handoff | None; all five exclusions still apply |

Paths are proposed responsibility targets, not a demand to rename current modules. Root alone integrates shared contracts, identity/transaction primitives, schema/integrity/grants, capability dispatch and common UI/runtime composition. SQL is limited to typed persistence and the common narrow integrity rules. Do not restore feature procedures or add nested transactions.

Depends on NEXT-02/13 and on NEXT-14 where the selected book has dimensions. Preserve the current `openerp-sie4i-v1` renderer and old bytes. Format qualification remains tied to the actual SIE specification [X07].

## Frozen capture

```text
FullBookSieCapture immutable {
  profile: supported_sie4e_version, fiscalYear, asOf,
  entityRevision, openingBasisId, ledgerBoundary, recordedCutoff,
  completeAccounts, originalDimensions, completeVoucherMembership,
  rawOpeningByAccount, rawClosingByAccount, nominalPeriodMovements,
  objectAndPeriodBalancesWhereRequired, source/nativeIdentityMap,
  independentChecks, coverageLimitations, rendererRelease, generationDate
}
```

The capture is a complete selected-book export through `asOf`, not a assertion that the fiscal year is closed or all external source events are known. If `asOf` precedes year end, disclose year-to-date scope. Do not fabricate future activity. Empty but genuinely established books may export required metadata/balances without dummy vouchers.

```text
captureFullBook(year, asOf):
    under consistent snapshot / shared book barrier:
        resolve reviewed entity and fiscal dates
        resolve one opening representation from NEXT-13
        select complete committed groups through asOf and cutoff
        capture all accounts, including inactive accounts used by selected history
        capture original dimensions and all referenced object declarations
        calculate raw account balances from opening plus included actual journal lines
        capture full original descriptions and voucher identifiers, not display truncations
        if any required source cannot be represented: block export with precise diagnostics
        persist fixed membership and financial rows; page later from this snapshot only
```

## Renderer

```text
renderSie4E(capture, formatRelease):
    require capture profile supported by exact formatRelease checksum
    require source text representable in chosen declared encoding
    w = strict record writer using that specification's quoting/escaping/line ending rules
    w.record('#FLAGGA', 0)
    w.record('#PROGRAM', retainedProgramName, rendererRelease.version)
    w.record('#FORMAT', selectedEncodingToken)
    w.record('#GEN', capture.generationDate)
    w.record('#SIETYP', 4)
    w.record('#FNAMN', capture.entityRevision.legalName)
    w.record('#ORGNR', qualifiedOrganizationNumberRepresentation)
    w.record('#RAR', 0, fiscalYear.start, fiscalYear.end)
    w.record('#VALUTA', functionalCurrency)
    w.record('#PROSA', exact as-of and known completeness limitations)
    for account in stable numeric-code ordering:
        w.record('#KONTO', account.code, account.frozenName)
        emit supported type/SRU metadata only from qualified mappings
    for dimension/value in frozen supported object map:
        emit '#DIM' and '#OBJEKT' records using retained numeric dimension mapping
    for balance-sheet account:
        emit '#IB' for established opening and '#UB' for captured closing
    for nominal account:
        emit '#RES' using RAW specified result-account balance semantics
        # Not a copied presentation P&L. Mechanical result-transfer lines remain in raw data.
    emit required object/period balance record families from same capture
        # '#OIB', '#OUB', '#PSALDO' or other records only under the pinned specification.
    for complete voucher in native fiscal-year/series/number ordering:
        emit '#VER' with frozen native identity, dates and full description
        begin block
        for original line in exact ordinal order:
            emit '#TRANS', code, original object bag, signed decimal amount,
                 applicable date, original description, supported quantity/sign fields
        end block
    require every captured voucher and line emitted exactly once
    require every required record family present or validly omitted under format profile
    return strict bytes without substitution/transliteration
```

Native voucher IDs/numbers describe the target ledger. Source voucher identifiers remain separate provenance, not silently substituted for native identities. Where historical native numbering differs, include the permitted source description/reference and a sidecar identity map.

`#RES` must not be replaced by the adjusted financial-statement display of annual profit. After a result-transfer bridge, the raw nominal transfer account and all ordinary nominal balances still describe the ledger. Independent format validation establishes their correct encoding.

## Reconciliation and artifact lifecycle

```text
checkSemanticExport(capture, independentlyParsedOutput):
    match entity/year/currency and required account/object declarations
    compare every native voucher identity, ordered line amount and dimension assignment
    compare record counts and exact opening/movement/closing control totals
    assert opening[a] + actualMovements[a] == closing[a] for each supported account
    assert no omitted nonzero account or unknown historical opening silently became0
    reject unexpected parser loss warnings even if parsing returned success
```

Generate bytes outside the financial transaction. Store immutable content and then attach the verified digest/length to the capture. Repeated downloads return those bytes, not a newly rendered file with today's date. A failure to store/validate leaves a captured or rendered-but-unvalidated export, never an accepted format.

A dimension-bearing book is blocked until object mapping is supported. No empty `{}` substitution. A parser that accepts a subset is an independent check of that subset, not blanket destination compatibility.

Evidence baseline: S13/S14/S15 and official format-family description [X07].

## Application capture, rendering and attachment

```text
prepareFullBookExport(command):
    withAdmittedPrincipal(access, scope, exportPermission, (tx, principal) =>
        lock book for a consistent capture; replay the command
        rows = SieDb.loadCompleteSelectedYear(tx, scope, selection)
        basis = ReportDomain.selectOpeningAndRawMovements(rows)
        SieDomain.validateRepresentableCompleteSelection(basis, qualifiedFormatRelease)
        capture = SieDb.insertCaptureAndMembership(tx, basis)
        OutboxDb.insert(tx, render request bound to capture + renderer version)
        return CommandDb.save(tx, principal, command, capture)
    )

renderFullBookExport(job):
    capture = application read of exact saved capture under current authority
    bytes = SieDomain.renderSie4E(capture, pinnedFormatRelease)
    validation = independent exact-profile format/semantic check outside financial tx
    objectManifest = retain immutable verified bytes
    withAdmittedPrincipal(serviceAccess, scope, artifactPermission, (tx, principal) =>
        lock book; replay artifact attachment key
        require exact capture/renderer/format identities and verified byte hash
        insert artifact attachment and validation result through tx
        save receipt; do not infer destination acceptance
    )
```

The Bun effect-mq handler runs rendering/validation outside financial transactions. An already captured historical export remains renderable without changing it to current balances. Future account labels or tax profiles do not replace captured values. The database supplies bounded joins, storage and integrity, not a SIE feature procedure.
