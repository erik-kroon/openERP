# NEXT-24 K2 annual-report semantic model and iXBRL review

Baseline: `abb24c2` (probe commit; source identical to `61c92c5` for all four
files below). Scope is `packages/domain/src/annual-report.ts`,
`packages/contracts/src/annual-report.ts`,
`apps/api/src/application/reports/annual-report.ts`,
`apps/api/src/db/reports/annual-report.ts` and this evidence file.

This is domain, contract and application review under the synthetic profile.
It is **not** statutory compliance, **not** a qualified native validator pass,
and **not** Bolagsverket acceptance. No E2E journey was run; see *Not proven*.

## Failure contract recorded before the source changes

1. A client may name evidence and a retained row, never a financial amount. A
   monetary semantic id declared as a "reviewed" fact is a manufactured fact.
2. A request carrying a row **and** an amount, or neither, refuses. The branch
   is decided from the exact key set so the invariant does not depend on the
   decoder's excess-property policy.
3. A real net loss is representable end to end. The contract already accepted
   `SignedMinorUnits` while the sealed draft shapes were unsigned, so a loss
   passed HTTP and then faulted the draft decode instead of reporting.
4. Every sealed fact carries an origin. A named row no retained snapshot
   carries is `DanglingReference`, never a zero.
5. Comparatives are distinct retained **prior** fiscal years, never the current
   year and never a current-year snapshot, and each comparative fact binds
   inside that basis without repeating a current-year semantic id.
6. An unsupported framework release blocks finalization. K2 output never
   implies K3 support.
7. Narratives need a retained approval, not a client-supplied approver id.
8. The presentation derives every displayed value from the sealed fact. The
   client asserts no amount, and the named totals must partition the sealed
   fact set exactly once each.
9. The encoded iXBRL value is the exact sealed source amount with the display
   rule's scale, so the rendered number is never a second rounded value.
10. The document is well-formed XHTML: declared namespaces, `ix:header` and
    `ix:resources`, every referenced `<xbrli:unit>` declared, and a duration
    period never emitted as an instant.
11. Concept QNames resolve only against a pinned **synthetic** release; an
    invented concept refuses.
12. No field named `bytesDigest` claims a digest the application owns over the
    exact retained bytes.

## Repeatable public-schema/domain probe

Run from the repository root. It records every case and prints one JSON line
each. `EXPECT_REPAIRED=1` exits nonzero on any failure.

```sh
EXPECT_REPAIRED=1 bun next24-probe.ts
```

`next24-probe.ts` at the repository root is the committed probe. It targets the
public exported schema and function surface, so it exercises the real wire
contract rather than a private path. Calls to functions the repair introduces
are wrapped in `attempt()`, so a pre-repair run records the absence as a failed
expectation instead of aborting.

## Results

| Run | Passed | Failed | Reached | Exit |
| --- | --- | --- | --- | --- |
| Pre-repair, `abb24c2` source | 5 | 31 | 36 of 45 | 1 |
| Post-repair | 45 | 0 | 45 of 45 | 0 |

The pre-repair run is a diagnosis, not a passing claim. The nine unreached
cases are the nested iXBRL structure checks inside the A9 block, which is
skipped once presentation cannot be prepared at all.

Amounts are exact minor units.

| Vector | Before repair | After repair |
| --- | --- | --- |
| Client states `revenue_for_the_year = 999999999` | Accepted and sealed verbatim | `ManufacturedFact`; only a pinned non-financial id may be reviewed |
| Request carries `rowId` and `valueMinor` | Accepted by the union | `ManufacturedFact`; branches never overlap |
| Row-bound fact `revenue_for_the_year` | No row-bound shape existed | Sealed `1200000` from the retained row |
| Row-bound fact `loss_for_the_year` | No row-bound shape existed | Sealed `-500000`; a loss is reportable |
| Signed amount on the wire (`-500000`) | Contract accepted, sealed draft rejected | Accepted and sealed end to end |
| `auditor_signing_count = 1` (pinned non-financial) | No reviewed origin existed | Accepted with `reviewed_explicit` origin and evidence |
| Reviewed fact with empty `evidenceRefs` | n/a | Rejected by the contract's minimum length |
| Fact naming a row no snapshot carries | n/a | `DanglingReference`, never zero |
| `frameworkRelease: "K3-2026"` | Finalizes; `frameworkSupported` hardcoded true | `UnsupportedFramework` |
| `frameworkRelease: "K2-2026"` | Finalizes | Finalizes |
| Comparative = the current-year snapshot id | Accepted; `comparativeSupported` hardcoded true | `UnsupportedComparison` |
| Comparative fiscal year equal to the current year | Accepted | `UnsupportedComparison` |
| Two comparatives sharing one fiscal year | Accepted | `UnsupportedComparison` |
| Comparative bound to a genuine prior year | n/a | Accepted |
| Narrative approval | `narrativesApproved` = "client set a non-null approvedBy" | `narrativeApprovalRef` = the retained four-eyes approval; null is `UnapprovedNarrative` |
| Presented fact amount | Client asserted `sourceMinor` and `displayedMinor` | Derived from the sealed fact by `deriveDisplayedMinor` |
| `expectedTotalMinor` | Client declared a grand total over unrelated concepts | Removed; totals name their member set and must partition the model |
| Totals leaving one fact uncovered | Accepted | `PresentationMismatch` |
| Displayed value, scale 3 | No display rule existed | `1200000` → `1200.000`; `-500000` → `-500.000` |
| Displayed value, scale 0 / -2 / 5→`0.005` | No display rule existed | `123456`, `123456`, `0.005`; exact scaling, never rounded |
| Encoded iXBRL value | `presented.displayedMinor` (client-influenced) | `presented.sourceMinor` with `displayDecimals(displayRule)` |
| Declared `decimals` per fact | Client chose per fact | Must equal `displayDecimals(displayRule)` |
| Document namespaces | `xbrli:`/`ix:` prefixes never declared, not well-formed | `xmlns:ix`, `xmlns:xbrli` and the rest declared |
| `ix:header` / `ix:resources` | Absent | Present, with schema and linkbase refs |
| `<xbrli:unit>` elements | Never emitted, so every `unitRef` dangled | Every referenced unit declared |
| Duration period `2026-01-01/2026-12-31` | Emitted as `<xbrli:instant>`, invalid | `<xbrli:startDate>`/`<xbrli:endDate>` |
| Duration concept over an instant context | Accepted | `FinancialMismatch` |
| Invented concept `se:Invented` | Emitted verbatim | `UnknownConceptMapping` |
| `bytesDigest` | Set to the **presentation** digest | Field removed; the application stores the real `contentHash` |

### Corrected probe expectations

Two expectations were corrected after the probe was first committed, and both
are recorded here rather than silently applied:

1. `A7_display_scale_negative_exact` originally expected `1235.56`, assuming a
   half-even rounding mode. The repaired profile scales exactly and never
   rounds — the stricter reading of the packet, since a rounding row is what
   would let a displayed number differ from its source. The case now asserts
   exact scaling (`123456`).
2. `A9_no_fake_bytes_digest` originally expected `bytesDigest` to be a real
   digest. The repair deletes the field instead, because the application owns
   the content hash over the exact bytes it retains. The case now asserts the
   field is absent.

No other expectation was weakened, removed or relaxed.

### Static gates

- `bun run check:changed`: passed. The first attempt failed on the existing
  complexity limit (34 versus 30) in `prepareAnnualReport`; the row-collection
  loops were moved into `collectRowAmounts`. No rule was changed.
- `bun run check:changed:full`: passed, including type-aware lint.
- `git diff --check`: passed. No command timed out.

### NUL-byte hazard

A first attempt at the repair left a raw NUL byte in the map-key separator of
`packages/domain/src/annual-report.ts`. A raw control byte makes git treat the
file as binary, which silently destroyed a saved diff and lost the work. The
separator is now the six-character escape `\u0000`, and every changed file is
audited:

```sh
for f in $(git diff --name-only HEAD); do printf "%s: " "$f"; perl -0777 -ne 'print scalar(()=/\x00/g),"\n"' "$f"; done
```

All five changed files report `0`.

## Changed contracts

These are explicit changes, not compatibility defaults. No migration was added.

- `SemanticFact` now carries `valueMinor: NullOr(SignedMinorUnits)` and a
  required `origin`. `DisclosureRequirement.derivedMinor` is signed.
- `SemanticFactRequest` is a union: a row-bound request states no amount; a
  reviewed request states an amount and non-empty evidence. `ReportFactInput`
  is this union.
- `NonLedgerSemanticIds` pins the only semantic ids that may be reviewed.
- `NarrativeSection` drops `approvedBy`; the draft carries
  `narrativeApprovalRef`, which stays null until the retained approval exists.
- `AnnualReportDraft` drops `frameworkSupported` and `narrativesApproved`, and
  gains `comparativeFacts`, `comparativeSupported` and `narrativeApprovalRef`.
- `PrepareAnnualReport` gains `comparativeFacts`.
- `PrepareReportPresentation` carries only `displayRule` and `totals`.
- `PresentationRevision` drops `presentationOnlyRows` and gains `displayRule`
  and `totals`.
- `ConceptMapping` drops the client-chosen `decimals`; `RenderReportArtifact`
  and `ReportArtifact` carry `taxonomyRelease`.
- `IxbrlDocument` drops `bytesDigest`.
- `annualReportTables` gains `report_statement_rows`. The runtime role already
  holds SELECT on it from migration `0005-next-13.sql`, so **no migration was
  required**; this was verified against the grant list.

## Not proven

- **No E2E journey.** The repository has no annual-report E2E at all, and none
  was added here. The application path — sealed-row reads, four-eyes approval,
  finalization, presentation and render — is verified by types, the static
  gates and the domain probe only. The claim that the HTTP surface behaves as
  described is **unverified**.
- **No qualified native validator exists.** `validationState` remains
  `pending_qualified_validator` by design. `evaluateValidationRun` and
  `checkSignatureScope` remain unconsumed: no application or worker owner
  records a validation run or a signature event, so the packet's independent
  validation and signature-scope obligations are still unimplemented. They were
  kept rather than deleted because the contract's pending state refers to them;
  neither can currently be exercised.
- **The taxonomy is synthetic and non-statutory.** `synthetic-k2-v1` and the
  `se:` namespace under `open-erp.invalid` are an explicit placeholder, not
  reviewed taxonomy data. No concept QName here may be used for a real filing.
- **No rendering, filing or statement output.** `assembleIxbrl` produces
  well-formed XHTML carrying no readable statement or note text; the packet's
  "readable statements/notes from the same presentation data" is still
  unimplemented, and narratives never reach the artifact.
- **Comparatives are bound but not presented.** Comparative facts are sealed
  and validated, and the artifact maps concepts by context, but no comparative
  column is rendered.
- **Rounding is not supported at all.** A report that needs a rounding
  difference must use another permitted precision or refuse; the packet's
  "presentation-only row" allowance is deliberately unused.
- `taxonomyRelease` is client-declared within the synthetic pattern. It is not
  proof that the named taxonomy exists.
- No real company, no real period, and no statutory judgement is claimed.
