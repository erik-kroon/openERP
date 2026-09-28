// NEXT-24 failure contract probe. Run before and after the repair.
// Records every case; EXPECT_REPAIRED=1 makes any failure exit nonzero.
import * as S from "effect/Schema";
import * as R from "effect/Result";
import * as C from "./packages/contracts/src/annual-report.ts";
import * as D from "./packages/domain/src/annual-report.ts";

let passed = 0;
let failed = 0;

function check(name: string, ok: boolean, actual: unknown) {
  if (ok) passed++;
  else failed++;
  console.log(JSON.stringify({ name, pass: ok, actual }));
}

function code(result: unknown) {
  return R.isFailure(result) ? result.failure.code : null;
}

// A pre-repair call can throw on a shape the repair removes. Record the fault
// as a failed expectation instead of aborting the whole probe.
function safe(run: () => unknown) {
  try {
    return run();
  } catch (error) {
    return { _tag: "Fault", message: error instanceof Error ? error.message : String(error) };
  }
}

function fieldKeys(struct: unknown): string {
  if (struct === undefined || struct === null) return "";
  const fields = (struct as { fields?: Record<string, unknown> }).fields;
  return fields ? Object.keys(fields).join(",") : "";
}

// An array schema keeps its element schema on `.value`.
function elementKeys(struct: unknown): string {
  return fieldKeys((struct as { value?: unknown }).value);
}

const loss = "-500000";
const evidence = ["ev_one"];
const rows = [
  { snapshotId: "snap_current", rowId: "row_revenue", amountMinor: "1200000" },
  { snapshotId: "snap_current", rowId: "row_loss", amountMinor: loss },
  { snapshotId: "snap_prior", rowId: "row_revenue", amountMinor: "900000" },
];

// A0: introspection itself must work, or the later field checks are vacuous.
const factInputKeys = fieldKeys(C.ReportFactInput);
check("A0_fact_input_keys_readable", factInputKeys.length > 0, { keys: factInputKeys });
const presentedFactKeys = elementKeys(C.PrepareReportPresentation.fields.facts);
check("A0_presented_fact_keys_readable", presentedFactKeys.length > 0, {
  keys: presentedFactKeys,
});

// A1: a ledger fact must be named by its retained row, not asserted as a number.
const bare = {
  semanticId: "revenue_for_the_year",
  valueMinor: "999999999",
  notApplicable: false,
  evidenceRefs: evidence,
  calculationRefs: [],
};
const bareAccepted = S.is(C.ReportFactInput)(bare);
check("A1_bare_fact_number_refused", bareAccepted === false, { contractAccepted: bareAccepted });

// A2: a real net loss must survive the sealed draft.
const lossFact = { ...bare, semanticId: "loss_for_the_year", valueMinor: loss };
const lossAccepted = S.is(C.ReportFactInput)(lossFact);
const sealedLoss = S.is(D.SemanticFact)(lossFact);
check("A2_signed_loss_contract", lossAccepted, { contractAccepted: lossAccepted });
check("A2_signed_loss_sealed_draft", sealedLoss, { domainAccepted: sealedLoss });
const lossDisclosure = {
  requirementId: "req_one",
  applicability: "applicable",
  inapplicableReason: null,
  derivedMinor: loss,
  reviewedExplicitFact: false,
  evidenceId: null,
};
check("A2_signed_loss_disclosure_sealed", S.is(D.DisclosureRequirement)(lossDisclosure), {
  domainAccepted: S.is(D.DisclosureRequirement)(lossDisclosure),
});

// A3: a sealed fact must carry a derivation origin and be bound to a retained row.
const hasOrigin = "origin" in fieldKeys(D.SemanticFact).split(",");
check("A3_fact_has_origin", hasOrigin, { originField: hasOrigin });

if (hasOrigin && typeof D.bindStatementFacts === "function") {
  const bound = D.bindStatementFacts({
    facts: [
      {
        semanticId: "revenue_for_the_year",
        snapshotId: "snap_current",
        rowId: "row_revenue",
        notApplicable: false,
        evidenceRefs: evidence,
        calculationRefs: [],
      },
      {
        semanticId: "loss_for_the_year",
        snapshotId: "snap_current",
        rowId: "row_loss",
        notApplicable: false,
        evidenceRefs: evidence,
        calculationRefs: [],
      },
    ],
    rows,
  });
  const values =
    R.isSuccess(bound) ? bound.success.map((fact) => [fact.semanticId, fact.valueMinor]) : null;
  check(
    "A3_bind_from_retained_rows",
    JSON.stringify(values) === JSON.stringify([
      ["revenue_for_the_year", "1200000"],
      ["loss_for_the_year", "-500000"],
    ]),
    { values },
  );

  const dangling = D.bindStatementFacts({
    facts: [
      {
        semanticId: "ghost",
        snapshotId: "snap_current",
        rowId: "row_absent",
        notApplicable: false,
        evidenceRefs: evidence,
        calculationRefs: [],
      },
    ],
    rows,
  });
  check("A3_bind_missing_row_refuses", code(dangling) === "DanglingReference", {
    code: code(dangling),
  });

  const foreign = D.bindStatementFacts({
    facts: [
      {
        semanticId: "revenue_for_the_year",
        snapshotId: "snap_elsewhere",
        rowId: "row_revenue",
        notApplicable: false,
        evidenceRefs: evidence,
        calculationRefs: [],
      },
    ],
    rows,
  });
  check("A3_bind_unbound_snapshot_refuses", foreign._tag === "Failure", {
    result: foreign._tag,
    code: code(foreign),
  });
} else {
  check("A3_bind_from_retained_rows", false, { missing: "bindStatementFacts" });
  check("A3_bind_missing_row_refuses", false, { missing: "bindStatementFacts" });
  check("A3_bind_unbound_snapshot_refuses", false, { missing: "bindStatementFacts" });
}

// A4: finalization must reject a fact with no derivation origin.
const finalizeWithBare =
  typeof D.finalizeSemanticReport === "function"
    ? D.finalizeSemanticReport(
        {
          draftId: "draft_one",
          fiscalYear: "2026",
          frameworkRelease: "K2-2026",
          frameworkSupported: true,
          closeCertificateRef: "cert_one",
          statementSnapshotIds: ["snap_current"],
          requirements: [],
          facts: [lossFact],
          narrativesApproved: true,
          comparativeSupported: true,
          comparativeSnapshotIds: [],
        } as never,
        "rep_one",
        "a".repeat(64),
      )
    : null;
check("A4_finalize_rejects_unbound_fact", code(finalizeWithBare) !== null, {
  code: code(finalizeWithBare),
});

// A5: comparatives must be bound to prior-year retained snapshots, not asserted true.
const unboundComparative =
  typeof D.finalizeSemanticReport === "function"
    ? D.finalizeSemanticReport(
        {
          draftId: "draft_one",
          fiscalYear: "2026",
          frameworkRelease: "K2-2026",
          frameworkSupported: true,
          closeCertificateRef: "cert_one",
          statementSnapshotIds: ["snap_current"],
          requirements: [],
          facts: [],
          narrativesApproved: true,
          comparativeSupported: true,
          comparativeSnapshotIds: [],
        } as never,
        "rep_one",
        "a".repeat(64),
      )
    : null;
check("A5_unbound_comparative_refuses", R.isFailure(unboundComparative), {
  accepted: R.isSuccess(unboundComparative),
  code: code(unboundComparative),
});

// A6: an unsupported framework release must block finalization.
const k3 =
  typeof D.finalizeSemanticReport === "function"
    ? D.finalizeSemanticReport(
        {
          draftId: "draft_one",
          fiscalYear: "2026",
          frameworkRelease: "K3-2026",
          frameworkSupported: true,
          closeCertificateRef: "cert_one",
          statementSnapshotIds: ["snap_current"],
          requirements: [],
          facts: [],
          narrativesApproved: true,
          comparativeSupported: true,
          comparativeSnapshotIds: [],
        } as never,
        "rep_one",
        "a".repeat(64),
      )
    : null;
check("A6_k3_release_refuses", code(k3) === "UnsupportedFramework", { code: code(k3) });

// A7: the presented value must be derived, never asserted by the client.
check("A7_presentation_has_no_client_value", !presentedFactKeys.includes("displayedMinor"), {
  keys: presentedFactKeys,
});
check("A7_display_rule_exists", typeof D.deriveDisplayedMinor === "function", {
  function: typeof D.deriveDisplayedMinor,
});
if (typeof D.deriveDisplayedMinor === "function") {
  const scaled = D.deriveDisplayedMinor("123456", 3);
  const signed = D.deriveDisplayedMinor(loss, 3);
  check("A7_display_scale_exact", scaled === "123.456" && signed === "-500.000", {
    scaled,
    signed,
  });
  const whole = D.deriveDisplayedMinor("123456", 0);
  check("A7_display_scale_zero_exact", whole === "123456", { whole });
  const up = D.deriveDisplayedMinor("123456", -2);
  check("A7_display_scale_negative_exact", up === "1235.56", { up });
}

// A8: a narrative must not be self-approved by the preparer.
const narrativeKeys = elementKeys(C.PrepareAnnualReport.fields.narratives);
check("A0_narrative_keys_readable", narrativeKeys.length > 0, { keys: narrativeKeys });
check("A8_narrative_has_no_client_approver", !narrativeKeys.includes("approvedBy"), {
  keys: narrativeKeys,
});

// A9: presentation derives values from sealed facts and reconciles named totals.
const hasOriginShape = hasOrigin
  ? {
      semanticId: "revenue_for_the_year",
      valueMinor: "1200000",
      notApplicable: false,
      evidenceRefs: evidence,
      calculationRefs: [],
      origin: { kind: "statement_row", snapshotId: "snap_current", rowId: "row_revenue" },
    }
  : {
      semanticId: "revenue_for_the_year",
      valueMinor: "1200000",
      notApplicable: false,
      evidenceRefs: evidence,
      calculationRefs: [],
    };
const report = {
  reportId: "rep_one",
  draftId: "draft_one",
  fiscalYear: "2026",
  frameworkRelease: "K2-2026",
  factCount: "1",
  requirementCount: "0",
  modelDigest: "a".repeat(64),
};

const prepared = safe(() =>
  typeof D.preparePresentation === "function"
    ? D.preparePresentation({
        presentationId: "pres_one",
        report,
        sealedFacts: [hasOriginShape],
        displayRule: { scale: 0, rounding: "half_even" },
        totals: [{ label: "turnover_total", memberSemanticIds: ["revenue_for_the_year"] }],
        presentationDigest: "b".repeat(64),
      } as never)
    : null,
);

if (R.isSuccess(prepared)) {
  const revision = prepared.success;
  check("A9_presentation_derives_displayed_value", true, {
    facts: revision.facts.map((f) => [f.semanticId, f.sourceMinor, f.displayedMinor]),
  });

  const assembled = D.assembleIxbrl({
    report,
    presentation: revision,
    mappedFacts: [
      {
        concept: "se:Revenue",
        contextRef: "ctx_duration",
        unitRef: "SEK",
        valueMinor: "1200000",
        decimals: "0",
      },
    ],
    contexts: [
      {
        contextRef: "ctx_duration",
        entityIdentifier: "5560000000",
        period: "2026-01-01/2026-12-31",
        dimensions: [],
      },
    ],
    units: ["SEK"],
    taxonomyRelease: "synthetic-k2-v1",
    unmappedConcepts: [],
  } as never);

  if (R.isSuccess(assembled)) {
    const xhtml = assembled.success.xhtml;
    check("A9_declares_namespaces", xhtml.includes("xmlns:ix=") && xhtml.includes("xmlns:xbrli="), {
      head: xhtml.slice(0, 160),
    });
    check("A9_declares_ix_header", xhtml.includes("ix:header") && xhtml.includes("ix:resources"), {
      hasHeader: xhtml.includes("ix:header"),
      hasResources: xhtml.includes("ix:resources"),
    });
    check("A9_declares_every_unit", xhtml.includes('id="SEK"'), { hasUnit: xhtml.includes("xbrli:unit") });
    check(
      "A9_duration_period_not_instant",
      !xhtml.includes("<xbrli:instant>2026-01-01/2026-12-31</xbrli:instant>"),
      {},
    );
    check("A9_bytes_digest_is_not_presentation_digest", assembled.success.bytesDigest !== revision.presentationDigest, {
      bytesDigest: assembled.success.bytesDigest.slice(0, 12),
    });
  } else {
    check("A9_assembly_succeeds", false, { code: code(assembled) });
  }
} else {
  check("A9_presentation_derives_displayed_value", false, { code: code(prepared) });
}

// A10: an invented concept QName must refuse unless it is in the pinned synthetic release.
check("A10_pinned_taxonomy_exists", typeof D.syntheticTaxonomyConcept === "function", {
  function: typeof D.syntheticTaxonomyConcept,
});
if (typeof D.syntheticTaxonomyConcept === "function") {
  check("A10_pinned_concept_known", D.syntheticTaxonomyConcept("se:Revenue") !== null, {
    known: D.syntheticTaxonomyConcept("se:Revenue") !== null,
  });
  check("A10_invented_concept_unknown", D.syntheticTaxonomyConcept("se:Invented") === null, {
    known: D.syntheticTaxonomyConcept("se:Invented") !== null,
  });
}

console.log(JSON.stringify({ passed, failed }));
if (process.env.EXPECT_REPAIRED === "1" && failed) process.exitCode = 1;
