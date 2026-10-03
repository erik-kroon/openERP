# Commercial draft failure contract

P02 adds a server calculated commercial purpose to the existing customer draft lifecycle. Source transcription keeps its original asserted amounts. UI work is limited to caller wiring while Paper redesign continues.

Before implementation, the public HTTP E2E specifies these failures and independent expectations.

- Twenty units at 100000 minor units produce net 2000000, VAT 500000, and gross 2500000 with the retained qualified 25% policy.
- Two lines with net 2 minor units each produce VAT 1 each and gross 6 in total. Tax rounds per line with the retained half-up rule.
- An unresolved treatment returns unknown VAT and gross. Saving is allowed, but legal prepare refuses.
- A client cannot submit base, VAT, gross, or source totals on commercial input. Excess fields fail boundary parsing.
- Fractional minor-unit base, duplicate line identity, overflow, or discount beyond base refuses without a revision write.
- A stale draft revision or customer/policy dependency refuses. Unsaved browser edits remain local.
- A committed save retried with the original key returns the same receipt and revision. A changed payload with that key refuses.
- Commercial saved revisions retain their exact commercial inputs and calculated facts. They never label derived amounts as original source amounts.
- Legal prepare binds the exact commercial revision and retained policy. Execute rechecks dependencies and current authority before consuming a number or writing financial effects.
- The current draft view reports canonical legal or synthetic issue ownership. Issued drafts remain immutable even when revisited by their old draft URL.
- Existing source-transcription revisions retain their asserted values and digest.
- A delayed preview cannot own totals for newer input. The response carries the canonical input digest and the expected draft target.

Actual company qualification, customer cash-method issuance, external delivery, and layout redesign are outside this functional slice. The existing customer legal issue owner supports the bounded domestic accrual profile. Supplier cash admission is a different owner.

## Implemented behavior and proof

The implementation uses one existing draft aggregate, an additive purpose constraint in migration 0061, and unchanged source contracts consumed by supplier and recurrence owners. Commercial input excludes asserted and calculated amount fields. Effect HTTP payload parse options reject excess input fields; schema annotations alone do not enforce that HTTP boundary in Effect 4.

`apps/api/tests/invoice-composer.e2e.test.ts` exercises the real HTTP Worker and isolated PostgreSQL database. Its browser scenario uses the existing editor, keeps calculated amount fields read-only, delays an older preview, and reads a saved revision back through HTTP. Artifacts include `commercial-revisions.json`, `commercial-legal-journey.json`, `commercial-editor.json`, a browser screenshot, and the runner's source-integrity and result manifests. No live provider, deployment or company-data acceptance is claimed. The selected legal profile is the existing bounded domestic Swedish accrual profile.

Repeat with `OPENERP_E2E_ARTIFACTS=test-results/product-P02 bun run test:e2e apps/api/tests/invoice-composer.e2e.test.ts`. The fixture expectations explicitly state the exact amounts; production calculation output is not used as its own oracle. Draft failures compare the complete draft inventory before and after refusal.

Material decisions followed pstack principles: Model the Domain keeps commercial calculation and source transcription distinct inside the owning lifecycle; Boundary Discipline binds current retained customer and tax-policy revisions; Make Operations Idempotent reuses retained request receipts; Test Behavior Not Implementation and Prove It Works require public HTTP and browser journeys with repeatable artifacts; Sequence Verifiable Units keeps calculation, save and legal issue independently reviewable. Customer cash issuance and Paper visual design remain separate work.

### Verified local checkpoint · 2026-10-03

The combined isolated Worker/PostgreSQL/browser lane passed all 14 tests across commercial drafts, source invoice issuance, supplier draft history, supplier cash adoption and pdfcn. The commercial browser journey also legally issued its saved revision, reopened the old draft URL, observed the legal number and found no edit or save control. Results and stable source fingerprints are retained under `test-results/product-P02-verified`; the source inventory hash is `4b14471039743a8daf14eb2bfb8e37a16693bec220dee1235df7bf147fb4a397`.

The full changed-file gate, the primary checkout's current Effect/type-aware lint, frozen dependency installation, and domain-leaf integration declaration passed. A previous contention-induced compiler timeout and earlier failed browser/test assertions remain failed historical evidence; they are not included as successful checks. The final serialized run finished with no remaining worktree test or compiler children.
