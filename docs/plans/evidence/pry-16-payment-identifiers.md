# PRY-16 — giro, check-digit and OCR primitives

Implemented and observed 2026-09-30 on the worktree based on `442ca12`.
The class-A R1 algorithm is delivered through the supplier-payment workspace,
scoped REST and ordinary read-only MCP. No provider or financial write is involved.

## Ownership and scope

`packages/domain/src/payment-identifiers.ts` owns modulus-10 calculation and
validation, giro formatting and explicit OCR candidate generation. All of those
paths use the same `mod10CheckDigit` implementation. Whole references remain
strings and preserve zero prefixes; only individual digits participate in scalar
arithmetic.

`apps/api/src/application/purchases/payment-identifiers.ts` composes that leaf
under current book admission. Shared contracts, HTTP composition and the actual
capability dispatcher expose `POST …/commerce/payment-identifiers` and
`payments_check_identifier`. The leaf is declared wired against those real imports.
The Supplier payment files page provides an explicit **Check giro and OCR
identifiers** disclosure using existing UI primitives and remote-state handling.
It checks only after user action and clears an obsolete result when input changes.

Supported checks and limits:

- Bankgiro: seven or eight ASCII digits, with its modulus-10 check digit; optional
  presentation spacing and a correctly placed giro hyphen are accepted.
- Plusgiro: two through eight digits, formatted with a hyphen before its check digit.
- OCR validation: two through 25 digits. It never repairs a wrong check digit.
- Check-digit calculation: a digit-only base; unusable input remains unchanged.
- Explicit OCR generation: extract ASCII digits from the supplied source identifier,
  require one through 24 source digits, then append the check digit. Missing digits
  or an overlong base returns `unsupported` with the original input unchanged.
- The wire input is bounded to 200 characters. Invalid validation input returns
  `invalid`, preserving its original output rather than silently repairing it.

The view separates raw input, normalized representation, status and output.
`accountVerified` and `paymentAuthorized` are always false. A passing checksum is
not an account-existence result, payee review, invoice-reference assignment or
payment mandate. The existing independently verified payee and payment-export
owners retain their contracts. PRY-17 clearing checks and PRY-18 domestic files
remain separate work; this utility does not advertise giro-based payment export.

Only package exports were added. No dependency or migration was added, `bun.lock`
is unchanged, and `bun install --frozen-lockfile` passed.

## Independent proof

The pre-implementation public call returned 404. The final E2E uses independently
specified arithmetic: `123456` has weighted sum 24 and check digit `6`;
`1234567` has sum 26 and digit `4`; `00012` has sum 5 and digit `5`. A 24-digit
base consisting of `1` followed by 23 zeros has sum 1 and digit `9`.

HTTP cases cover seven/eight-digit bankgiros, two/eight-digit plusgiros, minimum
and maximum OCR length, zero prefixes, wrong digits, malformed hyphens, letters,
full-width digits, empty/unusable generation and overlong source/wire inputs.
The agent's MCP result equals the HTTP result. Retained financial counts stay
unchanged throughout the checks.

Chromium signs in through Better Auth, opens the supplier-payment page, activates
a giro check with keyboard Enter, observes invalid input after editing, selects
OCR generation and obtains `000125` from `Invoice-00012`. At 390×844 it edits and
submits again, obtaining `000133` from `Invoice-00013`. The settled narrow layout
has no horizontal document overflow; desktop and narrow screenshots were inspected.
No page errors or vouchers are created. Screen-reader, physical touch-device and
200% browser-zoom qualification are not claimed.

The final focused regression run passed **22 tests across five files**, including
MCP authority, payment-resolution and both SIE suites. It used PostgreSQL 17.11,
local workerd, the restricted runtime role and real Chromium. Source inventory
remained stable at
`0e061a2f4309ef39a9ecb6d315407d0412705fa6946e66133b5121f31e64f9b9`.
Full changed-file lint/types and integration declarations also passed. An initial
API compiler timeout was a failed check; its process group was inspected and no
abandoned compiler remained before the subsequent successful checks.

## Repeatable artifacts

```sh
bun install --frozen-lockfile
bun run check:changed:full
bun run check:integration
bun run test:e2e apps/api/tests/payment-identifiers.e2e.test.ts apps/api/tests/mcp-authority.e2e.test.ts apps/api/tests/payment-resolutions.e2e.test.ts apps/api/tests/sie-account-codes.e2e.test.ts apps/api/tests/sie-dimensions.e2e.test.ts
```

The harness retains `pry-16-payment-identifiers.json`, `pry-16-browser.json`,
`pry-16-layout.json`, desktop/narrow screenshots, results and source-integrity
records in `test-results/e2e`, archiving earlier runs under `test-results/e2e-history`.
