# Recovery VAT receipt constraint validation

Forward migration `0050-validate-vat-receipt-match.sql` validates the narrow `(book_id, match_ref)` foreign key left unvalidated by historical migration0031. It preserves the FK definition, nullable match/voucher fields, wider event/voucher FK, immutable triggers and runtime grants. Historical migrations are unchanged.

The failure-first E2E at `17e7856` reproduced strict `databaseInventory` refusal on a fresh template0 database with onlyplpgsql. Exactly `openerp.vat_assessment_receipts_match_fkey` was unvalidated. Real constraint probes inside rolled-back fault transactions accepted nullmatch and an existing match with nullvoucher, and refused an orphan match with nullvoucher using23503 and the exact narrow constraint name. Fault-only replication settings and rows never persist.

At `04df81d`, the actual migration runner made strict source inventory succeed. Catalog constraint comparison changed only the target validation flag and its NOT VALID suffix. Schema dump comparison changed only that suffix; roles and grants remained identical. All retained table fingerprints remained identical except the appended migration receipt. Repeating the runner preserved full inventory and all fingerprints. An unrelated unvalidated constraint and a wrong migration hash still produced strict refusals.

Exact restore qualification remains blocked. Actual pg_dump/pg_restore preserved all397 table fingerprints but changed the deparsed text of `rule_change_notices_selectors_check` from nested to flattened AND grouping. Its predicates are unchanged; the unmodified recovery inventory hashes their text differently. Source schema hash is `582fea00e65092b77162300f9224c8a3e0e8b1d02cacc72233168946073fa46a`; restored hash is `c0ce03987c53f545b726d6f3bbda370e44bc1e34f5de2f76dec9c13cd745b081`. The exact equality assertion remains failing and no normalization or restore policy change is included.

Repeat on disposable synthetic infrastructure:

```sh
OPENERP_E2E_ARTIFACTS=test-results/recovery-constraint-unique bun run test:e2e apps/api/tests/recovery-constraint-validation.e2e.test.ts
```

Artifacts retain actual catalogs, refusals, source/migration hashes, data fingerprints and the restore difference. The final diagnostic run has stable source identity and no changed paths. Evaluation0049 is absent from this isolated branch; combined qualification requires a new coordinator run. This proves the0050 schema prerequisite, not complete application-recovery admission, production migration safety or actual-company readiness.
