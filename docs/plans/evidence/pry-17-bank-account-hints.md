# PRY-17 — non-blocking clearing/account checksum hints

Implemented and observed 2026-09-30 on the worktree based on `dc12ca4`.

## Delivered profile and owners

The existing payment-identifier leaf now owns the R2 checksum families, reusing
PRY-16's modulus-10 implementation. The purchases inspection owner exposes
`POST …/commerce/payment-identifiers/bank-account` and read-only MCP
`payments_check_bank_account`. The supplier-payment workspace has a real
**Check clearing and account number** disclosure using those shared contracts.

The request must explicitly name `reference_r2_v1`, and the result repeats that
basis. The ranges are the retained R2 comparison profile, not an independently
qualified current bank catalogue. Current bank-specific applicability remains a
D-08 qualification gate. This is a bounded calculation hint, not bank validation.

The profile selects exact clearing exceptions `3300` and `3782` before range
rules, then supports modulus-11 last-ten, full-eleven and nine-digit families,
ten-digit padded modulus-10, and the account-plus-clearing modulus-10 family.
Original input and normalized strings are retained in the response; virtual
padding for calculation never rewrites the user's account or drops zero prefixes.

- Recognized clearing and supported input shape: `valid` or `invalid` according
  to the selected checksum calculation.
- Unmapped clearing, unusable input or unsupported length: `unknown`, with its
  reason and any selected rule. Unknown is never presented as invalid.
- Four-digit clearing numbers are supported. A fifth digit is supported only
  for the `8xxx` reference family and is checked using PRY-16. Extra digits in
  other families remain no opinion rather than being silently ignored.
- Clearing/account inputs are bounded to 20 characters each. Spaces may be
  ignored for calculation; hyphens, signs and non-ASCII digits are not repaired.
- `nonBlocking` is always true; `accountVerified` and `paymentAuthorized` are
  always false. No payment gate, payee verification or file admission consumes
  this hint. It creates no financial or verification record.

No migration, dependency or new domain leaf was added. Existing package exports,
capability composition and application admission are reused.

## Independent observations

The pre-implementation HTTP reproduction returned 404. Final checks passed
`check:changed:full`, `check:integration` and five E2E tests across the new hints,
existing PRY-16 and MCP-authority suites. The run used PostgreSQL 17.11, local
workerd, the restricted runtime role and real Chromium. Source inventory remained
stable at `9dbee03798f6dae401caf739e59bcb74846b8778e0b621a736bc1e0b76637027`.

Independently specified weighted sums establish the positive vectors:

- Clearing `1100`, account `1`: last-ten sum `10 + 1 = 11`.
- Clearing `4000`, account `7`: full-eleven sum `4 + 7 = 11`.
- Clearing `6000`, account `19`: padded nine-digit sum `1×2 + 9 = 11`.
- Both exact exceptions use the PRY-16 `18` modulus-10 vector.
- Clearing `80002` and account `000018` each pass their independently specified
  modulus-10 checks; changing the fifth clearing digit to `1` refuses the checksum.

HTTP cases also cover wrong digits, zero modulus-11 total, all family length
limits, empty/malformed details, extra clearing digits, unrecognized clearing,
missing profile and overlong wire input. MCP preserves the same no-opinion result
for clearing `9100`. Financial counts remain unchanged.

Chromium signs in through Better Auth, checks a valid account using keyboard
Enter, preserves `000018` in the field, clears the old result on editing, then
observes invalid and no-opinion outcomes. At 390×844 the settled document has no
horizontal overflow. The narrow screenshot was inspected and no page errors or
vouchers were observed. No screen-reader, physical-device, current-bank acceptance
or 200% browser-zoom qualification is claimed.

## Repeatable evidence

```sh
bun run check:changed:full
bun run check:integration
bun run test:e2e apps/api/tests/bank-account-hints.e2e.test.ts apps/api/tests/payment-identifiers.e2e.test.ts apps/api/tests/mcp-authority.e2e.test.ts
```

`test-results/e2e` retains `pry-17-bank-account-hints.json`, `pry-17-browser.json`,
the narrow screenshot, results, manifest and source-integrity records. Earlier
runs are archived under `test-results/e2e-history`.
