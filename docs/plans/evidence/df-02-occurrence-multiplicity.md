# DF-02 — distinct acquisitions of identical originals

Qualified 2026-10-01 through the real source-retention and supplier-inbox APIs.

The older finding treated content-addressed evidence as the acquisition register.
The released acquisition owner instead retains source-system/account/key/revision
identity in `intake_occurrences`, separately from hash-addressed `intake_contents`.
Supplier inbox registration keeps each occurrence identity. No implementation or
DDL change is necessary for the demonstrated path.

## Independently specified journey

The E2E test retains identical synthetic CSV bytes under `acquisition_one` and
`acquisition_two` in one book. It requires distinct occurrence IDs, equal hashes,
two inbox entries and exactly one stored content object. Both occurrence reads
return the exact original bytes. Same-command replay returns the frozen response;
a fresh command for the same source identity converges on its original occurrence.
Changing bytes under that source identity refuses `409 IdempotencyConflict`.

REST and read-only MCP list the same two acquisitions. The book's financial
state remains unchanged. This tests existing owners rather than creating another
content/occurrence abstraction or weakening content uniqueness.

## Verification and boundary

Full changed-file lint/types pass, and the focused real PostgreSQL/workerd E2E
journey passes. This is inline CSV qualification only: external object-store
originals, PDFs, payment links, browser behavior and statutory retention are not
claimed. Legacy `create_evidence` still deduplicates content; callers needing
acquisition provenance must use the occurrence owner.

```sh
bun run check:changed:full
bun run test:e2e apps/api/tests/source-occurrence-multiplicity.e2e.test.ts
```

The harness retains `test-results/e2e/df-02-occurrence-multiplicity.json`, results,
manifest and source-integrity records. Older runs are archived by the harness.
