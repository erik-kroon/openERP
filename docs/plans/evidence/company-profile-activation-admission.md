# Company-profile activation admission

Local synthetic PostgreSQL/workerd verification on 2026-10-01 exercised the ordinary company-profile HTTP owner at implementation revision `cf684fd1fd8c0fcb876057e7644c293f708b6501`. All seven company-profile admission E2E cases passed with stable source integrity. This proves the bounded synthetic owner journey; it does not admit a real company or settle fact supersession policy.

Preparation previously returned HTTP `500 InternalError` because its sealed body omitted the schema-required `createdBy`. The owner now includes the admitted principal's actor ID and database timestamp before sealing. The E2E brackets the timestamp with PostgreSQL clock reads and independently recomputes the plan digest from the returned body.

Execution then exposed an unauthorized `FOR UPDATE` on immutable `change_sets`. The redundant row-lock helper and duplicate digest check were removed. The initial exact digest check, admitted book update lock, live authority checks, family epoch, immutable plan trigger and existing grants remain. Concurrent plans yield one activation and one `409 StaleDependency`; exact concurrent replay returns the same committed receipt.

The HTTP group now uses Effect's supported `HttpApi.PayloadParseOptions` with `onExcessProperty: error`. Schema annotations alone had allowed excess caller actor/time fields to be stripped while returning HTTP `200`. The unchanged E2E expectation now receives HTTP `400` and records its actual empty response body. Other HTTP groups and global parse defaults are unchanged.

The contract census distinguishes the versioned activation plan from the unversioned activation record. Execution now uses the ordinary canonical digest for `CompanyActivation`, matching its public schema and retained SQL digest constraint. Both returned digests are independently recomputed by the E2E without importing production canonicalization or digest functions.

The passing cases cover authenticated preparation and retained schema/digest/body, prepare replay and actor/input mismatch, independent approval, execution recovery after an unread response, exact concurrent replay, account staleness, lost approver membership, revoked executor credentials, late command-receipt rollback and original-key retry, and refusal of overlapping confirmed superseding facts. Successful execution retains one activation, one group receipt, one approval consumption and family epoch `2`. Voucher, journal-line, outbox and voucher-counter values remain zero, and the ledger sequence remains `0`.

Artifacts are under `test-results/company-profile-final-20261001`. The manifest identifies the exact source revision and migration hashes; `source-integrity.json` reports stable source and no changed paths. Per-case JSON files retain observed plans, timestamps, canonical bytes, digests, responses and database counts. The earlier schema, unauthorized lock, strict parsing and unversioned digest failures remain in separate `company-profile-red-20261001`, `company-profile-fixed-20261001`, `company-profile-execution-red-20261001` and `company-profile-complete-20261001` directories. Gate logs and the rerunnable before/after contract census are under `test-results/company-profile-gates-20261001`.

Repeat the owner journey with an unused artifact directory.

```sh
OPENERP_E2E_ARTIFACTS=test-results/company-profile-repeat bun run test:e2e apps/api/tests/company-profile-admission.e2e.test.ts
```

Frozen installation, fast and type-aware changed-source checks passed. No migration, grant, fact kind, company data, provider, deployment or evaluation workflow changed. Independent integration review and broader application qualification remain separate.

Independent source review accepted the bounded owner at `cf684fd`; final worker revision `abd4911` adds only this evidence document. The coordinator integrated it at `818f790` and repeated all seven cases with stable source in `test-results/integrated-company-profile-20261001`. Fast and type-aware checks against `6711199` passed.

Evidence has three limits. The independent activation-digest assertion and digest repair share one commit, although the preceding execution failure is retained. The rollback JSON omits the immediate post-fault counts; the passing in-test equality establishes that observation, while the JSON retains before and post-recovery counts. Raw manifests hash local configuration and raw artifacts are not a sanitized publication package. These qualifications do not establish Swedish applicability, actual-company admission or complete evaluation coverage.
