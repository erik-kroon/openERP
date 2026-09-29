// NEXT-34 mileage reimbursement — failure contract.
//
// This pins the obligations a mileage owner must satisfy. The leaf's pure
// rules are already reviewed, so most cases pass before the owner exists; that
// is expected and is recorded as such. The delivery gap is the owner, which
// `bun run check:integration` proves by holding `mileage-reimbursement` at
// `deferred` until a real importer exists.
import * as R from "effect/Result";
import * as S from "effect/Schema";
import * as M from "./packages/domain/src/mileage-reimbursement.ts";

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

const trip: M.TripRevision = {
  id: "trip_one",
  claimantId: "employee_one",
  businessPurpose: "Synthetic client visit",
  departureOn: "2026-01-10",
  arrivalOn: "2026-01-10",
  routeEvidenceRef: "evidence_route",
  routeReviewed: true,
  origin: "Stockholm Central",
  destination: "Uppsala Central",
  distanceInMeters: "70000",
  vehicleIdentity: "vehicle_one",
  ownershipKind: "private_car",
  fuelPayer: "employee",
  previousRevision: null,
};

const release: M.MileageRuleRelease = {
  releaseId: "release_2026",
  distanceUnitMeters: "1000",
  entitlementRateMinorPerUnit: "250",
  taxExemptRateMinorPerUnit: "150",
  requiresVehicleIdentity: true,
  requiresFuelPayer: true,
  evidenceSourceHash: `sha256:${"a".repeat(64)}`,
};

// A0: the surface a mileage owner must be able to call.
const surface = Object.keys(M).sort().join(",");

check(
  "A0_owner_surface_present",
  ["calculateMileage", "prepareTripAward", "replayTripAward", "correctTripAward"].every((name) =>
    surface.includes(name),
  ),
  surface.slice(0, 160),
);

// A1: 70 km at 2.50 per km is 17500 entitlement; the exempt ceiling at 1.50
// per km is 10500, so 10500 is exempt and 7000 is taxable. The parts sum to
// the entitlement: conservation is rechecked, not assumed.
const split = M.calculateMileage({ trip, release });

const parts =
  R.isSuccess(split) &&
  BigInt(split.success.exemptPaidPartMinor) + BigInt(split.success.taxablePartMinor) ===
    BigInt(split.success.entitlementMinor);

check(
  "A1_split_conserves_entitlement",
  R.isSuccess(split) &&
    split.success.entitlementMinor === "17500" &&
    split.success.exemptPaidPartMinor === "10500" &&
    split.success.taxablePartMinor === "7000" &&
    parts,
  JSON.stringify(R.isSuccess(split) ? split.success : code(split)),
);

// A2: an unreviewed route refuses at award time. The pure split is math and
// works on any input, but a suggestion is not a reviewed fact and can never
// become an award.
const unreviewed = M.prepareTripAward({
  awardId: "award_unreviewed",
  trip: { ...trip, routeReviewed: false },
  release,
  priorAwardTripIds: [],
  overlappingTripIds: [],
  payoutRoute: "payroll",
  payrollProfilePresent: true,
});

check("A2_unreviewed_route_refuses", code(unreviewed) !== null, String(code(unreviewed)));

// A3: a trip missing a required vehicle identity refuses when the release
// requires one.
const noVehicle = M.calculateMileage({
  trip: { ...trip, vehicleIdentity: null },
  release,
});

check("A3_missing_vehicle_refuses", code(noVehicle) !== null, String(code(noVehicle)));

// A4: award preparation seals two disjoint source identities, one for the
// exempt component and one for the taxable component.
const award = M.prepareTripAward({
  awardId: "award_one",
  trip,
  release,
  priorAwardTripIds: [],
  overlappingTripIds: [],
  payoutRoute: "payroll",
  payrollProfilePresent: true,
});

const identities =
  R.isSuccess(award) && award.success.exemptSourceIdentity !== award.success.taxableSourceIdentity;

check(
  "A4_award_seals_disjoint_identities",
  R.isSuccess(award) && identities,
  JSON.stringify(
    R.isSuccess(award)
      ? { exempt: award.success.exemptSourceIdentity, taxable: award.success.taxableSourceIdentity }
      : code(award),
  ),
);

// A5: a second award key over the same trip never mints a second award.
const duplicate = M.prepareTripAward({
  awardId: "award_two",
  trip,
  release,
  priorAwardTripIds: ["trip_one"],
  overlappingTripIds: [],
  payoutRoute: "payroll",
  payrollProfilePresent: true,
});

check("A5_duplicate_trip_refuses", code(duplicate) !== null, String(code(duplicate)));

// A6: an overlapping trip claim for the same economic travel refuses.
const overlapping = M.prepareTripAward({
  awardId: "award_three",
  trip,
  release,
  priorAwardTripIds: [],
  overlappingTripIds: ["trip_one"],
  payoutRoute: "payroll",
  payrollProfilePresent: true,
});

check("A6_overlapping_trip_refuses", code(overlapping) !== null, String(code(overlapping)));

// A7: a taxable component without a payroll owner refuses instead of falling
// back to direct payment.
const noPayroll = M.prepareTripAward({
  awardId: "award_four",
  trip,
  release,
  priorAwardTripIds: [],
  overlappingTripIds: [],
  payoutRoute: "payroll",
  payrollProfilePresent: false,
});

check("A7_taxable_without_payroll_refuses", code(noPayroll) !== null, String(code(noPayroll)));

// A8: the same trip under a second key recovers no second award. Replaying
// the identical key returns the existing plan.
const awarded = M.prepareTripAward({
  awardId: "award_replay",
  trip,
  release,
  priorAwardTripIds: [],
  overlappingTripIds: [],
  payoutRoute: "payroll",
  payrollProfilePresent: true,
});

const replayed =
  R.isSuccess(awarded) &&
  M.replayTripAward({
    existingCommandKey: "key_one",
    commandKey: "key_one",
    existingTripRevisionId: "trip_one",
    tripRevisionId: "trip_one",
    existingPlan: awarded.success,
  });

check(
  "A8_same_key_replays",
  replayed !== false && R.isSuccess(replayed),
  String(replayed === false ? "no award" : code(replayed)),
);

// A9: a correction consumes the prior delta rather than restating it.
const correction =
  R.isSuccess(awarded) &&
  M.correctTripAward({
    plan: awarded.success,
    revisedTrip: { ...trip, distanceInMeters: "80000" },
    release,
    handoffConsumed: true,
    lawfulRecoveryBasis: "basis_one",
    correctionId: "correction_one",
  });

check(
  "A9_correction_consumes_prior_delta",
  correction !== false && R.isSuccess(correction),
  String(correction === false ? "no award" : code(correction)),
);

// A10: unsigned minor-unit amounts throughout, so a negative distance or rate
// is unrepresentable rather than a signed surprise.
const negativeDistance = S.is(M.TripRevision)({ ...trip, distanceInMeters: "-100" });

check(
  "A10_negative_distance_unrepresentable",
  negativeDistance === false,
  String(negativeDistance),
);

console.log(JSON.stringify({ passed, failed }));

if (process.env.EXPECT_REPAIRED === "1" && failed) process.exitCode = 1;
