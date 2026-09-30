# DF-05 — consistent lexical SIE account codes

Implemented and observed 2026-09-30 on the worktree based on `ab40383`.

## Delivered boundary

`AccountCode` in `packages/domain/src/values.ts` owns the one-to-eight ASCII-digit
lexical contract. The inbound SIE parser, source mapping/opening/open-item controls
and movement-transfer renderer consume it. Account codes remain strings;
zero prefixes are preserved, and signed, fractional, alphabetic, non-ASCII and
overlong identifiers are not repaired into another account.

This unifies the widest movement-transfer width with inbound interpretation.
Existing four-digit source codes, including zero prefixes, remain readable.
The movement renderer now preserves those prefixed source identifiers too.
Decimal-magnitude ordering uses string comparison rather than numeric conversion;
the ordering of previously supported positive codes remains the same.

Malformed `#KONTO` declarations retain their original record and gain an
`account_code` diagnostic. Transaction and balance-control grammar uses the same
contract. UTF-8 offsets use the platform TextEncoder, removing the parser's Node
Buffer dependency without changing byte semantics.

A lexical code is not BAS classification, a chart-adoption decision or financial
import permission. The complete-book SIE4E owner keeps its separately documented
four-digit profile. Source staging still reports `financialAdmission: unsupported`;
the historical financial-admission owner remains a separate reviewed operation.
No migration, provider, company fact or dependency was added.

## Independent proof

Before the change, real movement transfers containing `1`, `19301` and `19301234`
rendered but their retained inbound previews rejected the transaction. A retained
`0012` source identifier was rejected by the movement renderer. Invalid account
declarations had no account-code diagnostic.

After the change, 14 E2E tests across the account-code and existing dimension suites
passed using disposable PostgreSQL 17.11, local workerd and the restricted runtime
role. The source inventory remained stable at
`c6f3f82cf01536b703ea503cd27324d8f871eb55e0ae45b219e0e8dd0d2cfc56`.

For each of `1`, `19301`, `19301234` and `0012`, the actual posting/report/review-pack
owners produce a movement transfer containing the exact source code and the
independently specified `125.00` debit and `-125.00` credit. A second book retains
and parses those exact bytes without diagnostics. A separately retained synthetic
derivative adds independently specified opening/closing controls, then passes
reviewed mapping and source-run staging while preserving the source code and
creating zero destination vouchers. The test does not claim the original movement
transfer supplied those opening controls or represented full history.

Empty, nine-digit, signed, alphabetic and full-width-digit mapping identifiers
fail HTTP validation. Malformed declarations/transactions remain inspectable
diagnostics, including exact UTF-8 transaction byte locations. The existing SIE4E
suite also passes its object-balance, original-tag, CP437 refusal and retained
v1/v2 recovery cases. No new browser layout or statutory recipient acceptance is
claimed.

## Repeatable evidence

```sh
bun run check:changed:full
bun run check:integration
bun run test:e2e apps/api/tests/sie-account-codes.e2e.test.ts apps/api/tests/sie-dimensions.e2e.test.ts
```

All commands passed. The harness retains `df-05-1.json`, `df-05-19301.json`,
`df-05-19301234.json`, `df-05-0012.json`, results, manifest and source-integrity
records in `test-results/e2e`, archiving prior runs under `test-results/e2e-history`.
