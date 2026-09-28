// NEXT-24 failure contract probe. Run before and after the repair.
// Records every case; EXPECT_REPAIRED=1 makes any failure exit nonzero.
//
// The defect expectations were written and committed BEFORE any production
// edit (abb24c2). Two expectations were corrected afterwards, with reasons
// recorded in the evidence file:
//  - the negative-scale case originally assumed a half-even rounding mode.
//    The repaired profile scales exactly and never rounds, which is the
//    stricter reading of the packet, so the case asserts exact scaling.
//  - the bytes-digest case now asserts the field is ABSENT, because the
//    application owns the real content hash over the exact retained bytes.
import * as S from "effect/Schema";

import * as R from "effect/Result";

import * as C from "./packages/contracts/src/annual-report.ts";

import * as D from "./packages/domain/src/annual-report.ts";

let passed = 0;

let failed = 0;

function check(name: string, ok: boolean, actual: string) {
  if (ok) passed++;
  else failed++;

  console.log(JSON.stringify({ name, pass: ok, actual }));
}

type Refusal = { readonly code: string };

type Attempt<A> =
  | { readonly ok: true; readonly value: A }
  | { readonly ok: false; readonly message: string };

// A pre-repair call can throw on a shape the repair removes. Record the fault
// as a failed expectation instead of aborting the whole probe.
function attempt<A>(run: () => A): Attempt<A> {
  try {
    return { ok: true, value: run() };
  } catch (error) {
    return { ok: false, message: error instanceof Error ? error.message : String(error) };
  }
}

function refusalOf(result: R.Result<unknown, Refusal>): string | null {
  return R.isFailure(result) ? result.failure.code : null;
}

type WithFields = { readonly fields: Readonly<object> };

type ArrayOf<A> = { readonly value: A };

function fieldKeys(struct: WithFields): string {
  return Object.keys(struct.fields).join(",");
}

function elementKeys(array: ArrayOf<WithFields>): string {
  return fieldKeys(array.value);
}

const loss = "-500000";

const evidence = ["ev_one"];

const rows: ReadonlyArray<D.StatementRowAmount> = [
  { snapshotId: "snap_current", rowId: "row_revenue", amountMinor: "1200000" },
  { snapshotId: "snap_current", rowId: "row_loss", amountMinor: loss },
  { snapshotId: "snap_prior", rowId: "row_revenue", amountMinor: "900000" },
];

function rowRequest(semanticId: string, snapshotId: string, rowId: string) {
  return {
    semanticId,
    snapshotId,
    rowId,
    notApplicable: false,
    evidenceRefs: evidence,
    calculationRefs: [],
  };
}

const baseDraft: D.AnnualReportDraft = {
  draftId: "draft_one",
  fiscalYear: "2026",
  frameworkRelease: "K2-2026",
  closeCertificateRef: "cert_one",
  statementSnapshotIds: ["snap_current"],
  requirements: [],
  facts: [],
  narrativeApprovalRef: "approval_one",
  comparativeSupported: true,
  comparativeSnapshotIds: [],
};

const report: D.FinalSemanticReport = {
  reportId: "rep_one",
  draftId: "draft_one",
  fiscalYear: "2026",
  frameworkRelease: "K2-2026",
  factCount: "1",
  requirementCount: "0",
  modelDigest: "a".repeat(64),
};

const sealedRevenue: D.SemanticFact = {
  semanticId: "revenue_for_the_year",
  valueMinor: "1200000",
  notApplicable: false,
  evidenceRefs: evidence,
  calculationRefs: [],
  origin: { kind: "statement_row", snapshotId: "snap_current", rowId: "row_revenue" },
};

// The display rule is new in the repair, so a pre-repair run has no function
// to call. Record the absence as a failed expectation instead of aborting.
function displayed(amount: string, scale: number): string {
  if (typeof D.deriveDisplayedMinor !== "function") return "missing";

  return D.deriveDisplayedMinor(amount, scale);
}

// A0: introspection itself must work, or the later field checks are vacuous.
const sealedKeys = fieldKeys(D.SemanticFact);

check("A0_sealed_fact_keys_readable", sealedKeys.includes("valueMinor"), sealedKeys);

const narrativeKeys = elementKeys(C.PrepareAnnualReport.fields.narratives);

check("A0_narrative_keys_readable", narrativeKeys.length > 0, narrativeKeys);

const presentationKeys = fieldKeys(C.PrepareReportPresentation);

check("A0_presentation_keys_readable", presentationKeys.includes("displayRule"), presentationKeys);

// A1: a ledger fact must be named by its retained row, never asserted as a number.
const bareNumber = {
  semanticId: "revenue_for_the_year",
  valueMinor: "999999999",
  notApplicable: false,
  evidenceRefs: evidence,
  calculationRefs: [],
};

const bareSeal = attempt(() => D.bindStatementFacts({ facts: [bareNumber], rows }));

check(
  "A1_bare_fact_number_refused",
  bareSeal.ok && refusalOf(bareSeal.value) === "ManufacturedFact",
  bareSeal.ok ? String(refusalOf(bareSeal.value)) : bareSeal.message,
);

const mixedSeal = attempt(() =>
  D.bindStatementFacts({
    facts: [{ ...bareNumber, snapshotId: "snap_current", rowId: "row_revenue" }],
    rows,
  }),
);

check(
  "A1_fact_cannot_carry_row_and_amount",
  mixedSeal.ok && refusalOf(mixedSeal.value) === "ManufacturedFact",
  mixedSeal.ok ? String(refusalOf(mixedSeal.value)) : mixedSeal.message,
);

const nonLedgerSeal = attempt(() =>
  D.bindStatementFacts({
    facts: [
      {
        semanticId: "auditor_signing_count",
        valueMinor: "1",
        notApplicable: false,
        evidenceRefs: evidence,
        calculationRefs: [],
      },
    ],
    rows,
  }),
);

check(
  "A1_non_ledger_reviewed_fact_accepted",
  nonLedgerSeal.ok && R.isSuccess(nonLedgerSeal.value),
  nonLedgerSeal.ok
    ? R.isSuccess(nonLedgerSeal.value)
      ? "accepted"
      : "refused"
    : nonLedgerSeal.message,
);

const rowBoundAccepted = S.is(C.ReportFactInput)(
  rowRequest("revenue_for_the_year", "snap_current", "row_revenue"),
);

check("A1_row_bound_fact_accepted", rowBoundAccepted, String(rowBoundAccepted));

const evidenceFree = S.is(C.ReportFactInput)({
  semanticId: "board_member_count",
  valueMinor: "1",
  notApplicable: false,
  evidenceRefs: [],
  calculationRefs: [],
});

check("A1_reviewed_fact_needs_evidence", evidenceFree === false, String(evidenceFree));

// A2: a real net loss must survive the sealed draft.
const lossRowAccepted = S.is(C.ReportFactInput)(
  rowRequest("loss_for_the_year", "snap_current", "row_loss"),
);

check("A2_signed_loss_row_accepted", lossRowAccepted, String(lossRowAccepted));

const signedNonLedger = S.is(C.ReportFactInput)({
  semanticId: "prior_year_restatement_delta",
  valueMinor: loss,
  notApplicable: false,
  evidenceRefs: evidence,
  calculationRefs: [],
});

check("A2_signed_amount_accepted", signedNonLedger, String(signedNonLedger));

const boundLoss = attempt(() =>
  D.bindStatementFacts({
    facts: [rowRequest("loss_for_the_year", "snap_current", "row_loss")],
    rows,
  }),
);

const lossSealed =
  boundLoss.ok && R.isSuccess(boundLoss.value) && S.is(D.SemanticFact)(boundLoss.value.success[0]);

check("A2_signed_loss_sealed_draft", lossSealed, String(lossSealed));

const lossDisclosure = {
  requirementId: "req_one",
  applicability: "applicable",
  inapplicableReason: null,
  derivedMinor: loss,
  reviewedExplicitFact: false,
  evidenceId: null,
};

const lossDisclosureAccepted = S.is(D.DisclosureRequirement)(lossDisclosure);

check("A2_signed_loss_disclosure_sealed", lossDisclosureAccepted, String(lossDisclosureAccepted));

// A3: a sealed fact carries a derivation origin bound to a retained row.
check("A3_fact_has_origin", sealedKeys.includes("origin"), sealedKeys);

const boundAll = attempt(() =>
  D.bindStatementFacts({
    facts: [
      rowRequest("revenue_for_the_year", "snap_current", "row_revenue"),
      rowRequest("loss_for_the_year", "snap_current", "row_loss"),
    ],
    rows,
  }),
);

const boundValues =
  boundAll.ok && R.isSuccess(boundAll.value)
    ? boundAll.value.success.map((fact) => [fact.semanticId, fact.valueMinor])
    : null;

check(
  "A3_bind_from_retained_rows",
  JSON.stringify(boundValues) ===
    JSON.stringify([
      ["revenue_for_the_year", "1200000"],
      ["loss_for_the_year", "-500000"],
    ]),
  JSON.stringify(boundValues),
);

const dangling = attempt(() =>
  D.bindStatementFacts({
    facts: [rowRequest("ghost", "snap_current", "row_absent")],
    rows,
  }),
);

check(
  "A3_bind_missing_row_refuses",
  dangling.ok && refusalOf(dangling.value) === "DanglingReference",
  dangling.ok ? String(refusalOf(dangling.value)) : dangling.message,
);

// A4: finalization refuses a monetary fact that was reviewed instead of derived.
const manufactured: D.SemanticFact = {
  semanticId: "revenue_for_the_year",
  valueMinor: "999999999",
  notApplicable: false,
  evidenceRefs: evidence,
  calculationRefs: [],
  origin: { kind: "reviewed_explicit", evidenceRefs: evidence },
};

const finalizeManufactured = D.finalizeSemanticReport(
  { ...baseDraft, facts: [manufactured] },
  "rep_one",
  "a".repeat(64),
);

check(
  "A4_finalize_rejects_unbound_fact",
  refusalOf(finalizeManufactured) === "ManufacturedFact",
  String(refusalOf(finalizeManufactured)),
);

const originlessAccepted = S.is(D.SemanticFact)(bareNumber);

check(
  "A4_originless_fact_rejected_by_schema",
  originlessAccepted === false,
  String(originlessAccepted),
);

const boundFacts = boundAll.ok && R.isSuccess(boundAll.value) ? boundAll.value.success : [];

const finalizeBound = D.finalizeSemanticReport(
  { ...baseDraft, facts: boundFacts },
  "rep_one",
  "a".repeat(64),
);

check(
  "A4_finalize_accepts_bound_fact",
  R.isSuccess(finalizeBound),
  R.isSuccess(finalizeBound) ? "accepted" : String(refusalOf(finalizeBound)),
);

const unapprovedNarrative = D.finalizeSemanticReport(
  { ...baseDraft, narrativeApprovalRef: null, facts: boundFacts },
  "rep_one",
  "a".repeat(64),
);

check(
  "A4_narrative_needs_retained_approval",
  refusalOf(unapprovedNarrative) === "UnapprovedNarrative",
  String(refusalOf(unapprovedNarrative)),
);

// A5: comparatives must be distinct prior fiscal years, never asserted true.
const comparativeAsCurrent = D.finalizeSemanticReport(
  { ...baseDraft, comparativeSnapshotIds: ["snap_current"] },
  "rep_one",
  "a".repeat(64),
);

check(
  "A5_current_year_as_comparative_refuses",
  refusalOf(comparativeAsCurrent) === "UnsupportedComparison",
  String(refusalOf(comparativeAsCurrent)),
);

const sameYear = attempt(() =>
  D.deriveComparativeSupport({
    currentFiscalYear: "2026",
    currentSnapshotIds: ["snap_current"],
    currentFacts: boundFacts,
    comparatives: [{ snapshotId: "snap_prior", fiscalYear: "2026" }],
    comparativeFacts: [],
  }),
);

const sameYearCode = sameYear.ok ? refusalOf(sameYear.value) : "missing";

check(
  "A5_same_year_comparative_refuses",
  sameYearCode === "UnsupportedComparison",
  String(sameYearCode),
);

const duplicateYears = attempt(() =>
  D.deriveComparativeSupport({
    currentFiscalYear: "2026",
    currentSnapshotIds: ["snap_current"],
    currentFacts: boundFacts,
    comparatives: [
      { snapshotId: "snap_prior", fiscalYear: "2025" },
      { snapshotId: "snap_prior_two", fiscalYear: "2025" },
    ],
    comparativeFacts: [],
  }),
);

const duplicateYearsCode = duplicateYears.ok ? refusalOf(duplicateYears.value) : "missing";

check(
  "A5_duplicate_comparative_year_refuses",
  duplicateYearsCode === "UnsupportedComparison",
  String(duplicateYearsCode),
);

const priorYear = attempt(() =>
  D.deriveComparativeSupport({
    currentFiscalYear: "2026",
    currentSnapshotIds: ["snap_current"],
    currentFacts: boundFacts,
    comparatives: [{ snapshotId: "snap_prior", fiscalYear: "2025" }],
    comparativeFacts: [],
  }),
);

check(
  "A5_prior_year_comparative_accepted",
  priorYear.ok && R.isSuccess(priorYear.value),
  priorYear.ok
    ? R.isSuccess(priorYear.value)
      ? "accepted"
      : String(refusalOf(priorYear.value))
    : "missing",
);

// A6: an unsupported framework release must block finalization.
const k3 = D.finalizeSemanticReport(
  { ...baseDraft, frameworkRelease: "K3-2026" },
  "rep_one",
  "a".repeat(64),
);

check("A6_k3_release_refuses", refusalOf(k3) === "UnsupportedFramework", String(refusalOf(k3)));

const k2 = D.finalizeSemanticReport(baseDraft, "rep_one", "a".repeat(64));

check(
  "A6_k2_release_accepted",
  R.isSuccess(k2),
  R.isSuccess(k2) ? "accepted" : String(refusalOf(k2)),
);

// A7: the presented value is derived, never asserted by the client.
check(
  "A7_presentation_has_no_client_value",
  !presentationKeys.includes("facts") && !presentationKeys.includes("expectedTotalMinor"),
  presentationKeys,
);

check("A7_display_rule_exists", typeof D.deriveDisplayedMinor === "function", "checked");

check(
  "A7_display_scale_exact",
  displayed("123456", 3) === "123.456" && displayed(loss, 3) === "-500.000",
  `${displayed("123456", 3)} ${displayed(loss, 3)}`,
);

check("A7_display_scale_zero_exact", displayed("123456", 0) === "123456", displayed("123456", 0));

check(
  "A7_display_scale_negative_exact",
  displayed("123456", -2) === "123456",
  displayed("123456", -2),
);

check("A7_display_small_amount_scale_exact", displayed("5", 3) === "0.005", displayed("5", 3));

// A8: a narrative must not be self-approved by the preparer.
check("A8_narrative_has_no_client_approver", !narrativeKeys.includes("approvedBy"), narrativeKeys);

// A9: presentation derives values and the document is well-formed iXBRL.
const presentationInput: D.PreparePresentationInput = {
  presentationId: "pres_one",
  report,
  sealedFacts: [sealedRevenue],
  displayRule: { scale: 0, rounding: "exact" },
  totals: [{ label: "turnover_total", memberSemanticIds: ["revenue_for_the_year"] }],
  presentationDigest: "b".repeat(64),
};

const prepared = attempt(() => D.preparePresentation(presentationInput));

if (prepared.ok && R.isSuccess(prepared.value)) {
  const revision = prepared.value.success;

  const presented = revision.facts[0];

  const derived =
    presented !== undefined &&
    presented.sourceMinor === "1200000" &&
    presented.displayedMinor === "1200000";

  check(
    "A9_presentation_derives_displayed_value",
    derived,
    presented === undefined ? "no facts" : `${presented.sourceMinor}/${presented.displayedMinor}`,
  );

  const partial = D.preparePresentation({
    presentationId: "pres_two",
    report,
    sealedFacts: [
      sealedRevenue,
      { ...sealedRevenue, semanticId: "loss_for_the_year", valueMinor: loss },
    ],
    displayRule: { scale: 0, rounding: "exact" },
    totals: [{ label: "turnover_total", memberSemanticIds: ["revenue_for_the_year"] }],
    presentationDigest: "b".repeat(64),
  });

  check(
    "A9_totals_must_partition_every_fact",
    refusalOf(partial) === "PresentationMismatch",
    String(refusalOf(partial)),
  );

  const durationContext: D.IxbrlContext = {
    contextRef: "ctx_duration",
    entityIdentifier: "5560000000",
    period: "2026-01-01/2026-12-31",
    dimensions: [],
  };

  const instantContext: D.IxbrlContext = {
    contextRef: "ctx_instant",
    entityIdentifier: "5560000000",
    period: "2026-12-31",
    dimensions: [],
  };

  const revenueFact: D.IxbrlFact = {
    concept: "se:Revenue",
    contextRef: "ctx_duration",
    unitRef: "SEK",
    valueMinor: "1200000",
    decimals: "0",
  };

  const assembled = attempt(() =>
    D.assembleIxbrl({
      report,
      presentation: revision,
      mappedFacts: [revenueFact],
      contexts: [durationContext],
      units: ["SEK"],
      taxonomyRelease: "synthetic-k2-v1",
      unmappedConcepts: [],
    }),
  );

  if (assembled.ok && R.isSuccess(assembled.value)) {
    const xhtml = assembled.value.success.xhtml;

    check(
      "A9_declares_namespaces",
      xhtml.includes("xmlns:ix=") && xhtml.includes("xmlns:xbrli="),
      xhtml.slice(0, 90),
    );

    check(
      "A9_declares_ix_header",
      xhtml.includes("ix:header") && xhtml.includes("ix:resources"),
      `header=${xhtml.includes("ix:header")} resources=${xhtml.includes("ix:resources")}`,
    );

    check("A9_declares_every_unit", xhtml.includes('<xbrli:unit id="SEK">'), "unit");

    check("A9_duration_period_not_instant", xhtml.includes("<xbrli:startDate>"), "startDate");

    check(
      "A9_taxonomy_release_retained",
      assembled.value.success.taxonomyRelease === "synthetic-k2-v1",
      assembled.value.success.taxonomyRelease,
    );

    check(
      "A9_no_fake_bytes_digest",
      !("bytesDigest" in assembled.value.success),
      Object.keys(assembled.value.success).join(","),
    );

    const wrongPeriod = D.assembleIxbrl({
      report,
      presentation: revision,
      mappedFacts: [{ ...revenueFact, contextRef: "ctx_instant" }],
      contexts: [instantContext],
      units: ["SEK"],
      taxonomyRelease: "synthetic-k2-v1",
      unmappedConcepts: [],
    });

    check(
      "A9_duration_concept_over_instant_refuses",
      refusalOf(wrongPeriod) === "FinancialMismatch",
      String(refusalOf(wrongPeriod)),
    );

    const invented = D.assembleIxbrl({
      report,
      presentation: revision,
      mappedFacts: [{ ...revenueFact, concept: "se:Invented" }],
      contexts: [durationContext],
      units: ["SEK"],
      taxonomyRelease: "synthetic-k2-v1",
      unmappedConcepts: [],
    });

    check(
      "A9_invented_concept_refuses",
      refusalOf(invented) === "UnknownConceptMapping",
      String(refusalOf(invented)),
    );
  } else {
    check(
      "A9_assembly_succeeds",
      false,
      assembled.ok ? String(refusalOf(assembled.value)) : assembled.message,
    );
  }
} else {
  check(
    "A9_presentation_derives_displayed_value",
    false,
    prepared.ok ? String(refusalOf(prepared.value)) : prepared.message,
  );
}

// A10: concept QNames come from the pinned synthetic release only.
check("A10_pinned_taxonomy_exists", typeof D.syntheticTaxonomyConcept === "function", "checked");

function conceptKnown(qname: string): boolean | "missing" {
  if (typeof D.syntheticTaxonomyConcept !== "function") return "missing";

  return D.syntheticTaxonomyConcept(qname) !== null;
}

check(
  "A10_pinned_concept_known",
  conceptKnown("se:Revenue") === true,
  String(conceptKnown("se:Revenue")),
);

check(
  "A10_invented_concept_unknown",
  conceptKnown("se:Invented") === false,
  String(conceptKnown("se:Invented")),
);

console.log(JSON.stringify({ passed, failed }));

if (process.env.EXPECT_REPAIRED === "1" && failed) process.exitCode = 1;
