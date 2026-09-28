// NEXT-50 agent book context and work index — failure contract.
//
// This pins the obligations a read-only context OWNER must satisfy. The leaf's
// pure rules already exist, so many cases pass before the owner does; that is
// expected and is recorded as such. The delivery gap is the owner, which
// `bun run check:integration` proves by holding `agent-context` at `deferred`
// until a real importer exists.
import * as R from "effect/Result";
import * as S from "effect/Schema";
import * as A from "./packages/domain/src/agent-context.ts";

let passed = 0;

let failed = 0;

function check(name: string, ok: boolean, actual: string) {
  if (ok) passed++;
  else failed++;
  console.log(JSON.stringify({ name, pass: ok, actual }));
}

type Refusal = { readonly code: string };

function code(result: R.Result<unknown, Refusal>): string | null {
  return R.isFailure(result) ? result.failure.code : null;
}

const complete: A.ModuleSummary = {
  owner: "ledger",
  status: "available",
  rowCount: "3",
  fullCount: "3",
  hasContinuation: false,
  coverageKnown: true,
  ownerVersion: "owner_v1",
};

// A0: the surface a context owner must be able to call.
const surface = Object.keys(A).sort().join(",");

check(
  "A0_owner_surface_present",
  ["assertModuleCompleteness", "rankWork", "getContextDelta", "classifyIncomingPayment"].every(
    (name) => surface.includes(name),
  ),
  surface.slice(0, 140),
);

// A1: a module reporting zero rows with UNKNOWN coverage must not read as
// complete. Unknown coverage is an explicit unknown, never zero unresolved.
const zeroUnknown = A.assertModuleCompleteness({
  ...complete,
  rowCount: "0",
  fullCount: "0",
  coverageKnown: false,
});

check(
  "A1_zero_with_unknown_coverage_refuses",
  code(zeroUnknown) === "IncompleteCoverageClaimed",
  String(code(zeroUnknown)),
);

const zeroKnown = A.assertModuleCompleteness({
  ...complete,
  rowCount: "0",
  fullCount: "0",
  coverageKnown: true,
});

check("A1_zero_with_known_coverage_accepted", R.isSuccess(zeroKnown), String(code(zeroKnown)));

// A2: an unavailable module contributes no work rows at all. A row count above
// zero from an unavailable module is a claim that cannot be true.
const unavailableWithRows = A.assertModuleCompleteness({
  ...complete,
  status: "unavailable",
  rowCount: "2",
});

check(
  "A2_unavailable_with_rows_refuses",
  code(unavailableWithRows) === "UnavailableAsZero",
  String(code(unavailableWithRows)),
);

const unavailableEmpty = A.assertModuleCompleteness({
  ...complete,
  status: "unavailable",
  rowCount: "0",
});

check(
  "A2_unavailable_empty_accepted",
  R.isSuccess(unavailableEmpty),
  String(code(unavailableEmpty)),
);

const notAuthorizedEmpty = A.assertModuleCompleteness({
  ...complete,
  status: "not_authorized",
  rowCount: "0",
});

check(
  "A2_not_authorized_empty_accepted",
  R.isSuccess(notAuthorizedEmpty),
  String(code(notAuthorizedEmpty)),
);

// A3: ranking needs the snapshot's own goal. A caller cannot rank one goal's
// work under a different goal's label.
const work = (
  identity: string,
  severity: A.WorkSeverity,
  missingInputs: ReadonlyArray<string> = ["approval"],
): A.WorkRef => ({
  owner: "ledger",
  identity,
  revision: "1",
  kind: "unposted_change_set",
  severity,
  affectedPeriod: "period_2025",
  blockedOperation: null,
  missingInputs: [...missingInputs],
  nextPermittedPreparation: "approve_change_set",
  immutableRef: `${identity}_ref`,
  digest: `sha256:${"a".repeat(64)}`,
});

const snapshot: A.BookContextSnapshot = {
  id: "context_one",
  principalScopeFingerprint: `sha256:${"b".repeat(64)}`,
  bookId: "book_one",
  goal: "close_the_year",
  recordedCutoff: "2026-01-01T00:00:00.000Z",
  ledgerBoundary: "sequence_1",
  contextVersion: "1",
  modules: [complete],
  work: [
    work("work_blocking", "blocks_goal"),
    work("work_material", "material"),
    work("work_routine", "routine"),
  ],
  allowedCapabilities: ["workspace_list_work"],
  contentDigest: `sha256:${"c".repeat(64)}`,
};

const ranked = A.rankWork({ snapshot, goal: "close_the_year", period: null, deadlineUrgency: [] });

check("A3_ranking_succeeds_for_the_snapshot_goal", R.isSuccess(ranked), String(code(ranked)));

const order = R.isSuccess(ranked) ? ranked.success.orderedIdentities.join(",") : "";

check("A3_goal_prevention_orders_first", order.startsWith("work_blocking,"), order);

const wrongGoal = A.rankWork({
  snapshot,
  goal: "pay_a_supplier",
  period: null,
  deadlineUrgency: [],
});

check(
  "A3_ranking_refuses_another_goal",
  code(wrongGoal) === "GoalSemanticsMismatch",
  String(code(wrongGoal)),
);

// A4: repeated identical missing-fact blockers collapse into ONE question, and
// the distinct effect count travels with it, so collapsing never merges two
// different financial effects.
// Two items share the same missing fact, so they collapse into one question.
// The third has a DIFFERENT missing fact, so it must stay its own question:
// collapsing across distinct blockers would hide a question.
const duplicated: A.BookContextSnapshot = {
  ...snapshot,
  work: [
    work("work_one", "material"),
    work("work_two", "material"),
    work("work_three", "routine", ["source_document"]),
  ],
};

const collapsed = A.rankWork({
  snapshot: duplicated,
  goal: "close_the_year",
  period: null,
  deadlineUrgency: [],
});

const questions = R.isSuccess(collapsed) ? collapsed.success.questions : [];

const blockerQuestion = questions.find((question) => question.affectedRefs.length === 2);

check("A4_identical_blockers_collapse", blockerQuestion !== undefined, JSON.stringify(questions));

check(
  "A4_collapsed_question_keeps_effect_count",
  blockerQuestion !== undefined && blockerQuestion.distinctEffects === "2",
  blockerQuestion === undefined ? "none" : blockerQuestion.distinctEffects,
);

check(
  "A4_distinct_blocker_keeps_its_own_question",
  questions.some(
    (question) =>
      question.affectedRefs.length === 1 && question.question !== blockerQuestion?.question,
  ),
  questions.map((question) => `${question.question}=${question.affectedRefs.length}`).join(" | "),
);

// A5: a delta never leaks a different principal's context. A changed scope
// fingerprint returns FreshContextRequired with no old names or values.
const otherPrincipal: A.BookContextSnapshot = {
  ...snapshot,
  id: "context_two",
  principalScopeFingerprint: `sha256:${"d".repeat(64)}`,
};

const crossPrincipal = A.getContextDelta({
  base: snapshot,
  target: otherPrincipal,
  ownerReportedResolved: [],
  confirmedScopeChanges: [],
});

check(
  "A5_fresh_context_for_another_principal",
  R.isSuccess(crossPrincipal) && crossPrincipal.success.kind === "fresh_context_required",
  JSON.stringify(crossPrincipal),
);

// A6: the same principal and goal but a different version is a version
// mismatch, not a silent merge.
const bumped: A.BookContextSnapshot = { ...snapshot, id: "context_two", contextVersion: "2" };

const versionMismatch = A.getContextDelta({
  base: snapshot,
  target: bumped,
  ownerReportedResolved: [],
  confirmedScopeChanges: [],
});

check(
  "A6_version_mismatch_refuses",
  code(versionMismatch) === "ContextVersionMismatch",
  String(code(versionMismatch)),
);

// A7: a new bank payment against a recognized OUTSTANDING invoice suggests a
// settlement, never a new purchase.
const settled = A.classifyIncomingPayment({
  recognizedInvoiceIdentity: "invoice_one",
  newBankPaymentIdentity: "payment_one",
  invoiceOutstanding: false,
});

check(
  "A7_settled_invoice_takes_no_suggestion",
  code(settled) === "GoalSemanticsMismatch",
  String(code(settled)),
);

const outstanding = A.classifyIncomingPayment({
  recognizedInvoiceIdentity: "invoice_one",
  newBankPaymentIdentity: "payment_one",
  invoiceOutstanding: true,
});

check(
  "A7_outstanding_invoice_suggests_settlement",
  R.isSuccess(outstanding) && outstanding.success.paymentIdentity === "payment_one",
  JSON.stringify(outstanding),
);

// A8: the input schemas must be the owner-buildable shapes. A context owner
// that cannot express an unknown revision or an unbounded work list is not
// buildable.
const snapshotAccepted = S.is(A.BookContextSnapshot)(snapshot);

check("A8_snapshot_shape_accepted", snapshotAccepted, String(snapshotAccepted));

const unsignedRefAccepted = S.is(A.WorkRef)(work("work_ref_one", "routine"));

check("A8_work_ref_shape_accepted", unsignedRefAccepted, String(unsignedRefAccepted));

console.log(JSON.stringify({ passed, failed }));

if (process.env.EXPECT_REPAIRED === "1" && failed) process.exitCode = 1;
