# P05 document library delivery checkpoint

Documents forwards retained owner search filters through validated URLs and exact minor amounts. Its opaque traversal cursor, selected original and return context survive owner navigation. Supplier history, expense source history and expense reviews open the named retained revision and survive reload. Detail metadata queries the exact occurrence, including originals outside the legacy capped owner list. Missing original bytes preserve readable owner metadata and an explicit retry.

The voucher modal closes through its accessible button. That button says **Back to documents** for a Documents origin. Specialized review and report labels keep their precedence. Its existing owner return destination preserves the original filters and selected record. The modal background remains inaccessible while the sheet is open.

The archive query limits immutable filename candidates before enrichment, materializes validated reference keys once and uses migration `0064-document-library-source-evidence.sql` for supplier revision lookup. Qualification still requires a known reference kind, string occurrence ID, complete SHA-256 and the same book. Malformed JSONB, arrays, scalars, lone surrogates, NUL escapes, foreign references and wrong hashes cannot create an owner relationship.

## Observed verification

[Gate output](remainder-checks.txt) records passing fast, full and current primary strict Effect lint over the changed source. The full gate passed after the browser fixture waited for metadata while retaining the literal two-source-link expectation. No lint or type rule was weakened.

The three library and six cash owner scenarios passed in `test-results/product-P05-remainder-green`. [Owner search measurements](owner-search-final.json) use five warmups and thirty trials over 10002 occurrences and 10000 supplier revisions. Median was 480.001333 ms and p95 was 538.339875 ms, below the fixed 1000 ms added-operation budget.

The ordinary filename comparison passed at p50 44.274334 ms and p95 47.018041 ms. Parent `96247e3` measured p95 25.283875 ms under the same five-warmup/thirty-trial protocol. The unchanged allowed budget was 75.283875 ms. [Raw measurements](filename-scalar-green.json) and [the investigation](performance-investigation.md) retain failed attempts and their limits. These fixtures use explicit ANALYZE and do not establish latency for arbitrary populations without statistics.

The full [Documents browser journey](browser-journey.json) passed in 24.18 seconds. It exercised filtered search, exact amount validation, matching page export, voucher return and focus, historical supplier/source/review reloads, Tax history reload, 320-pixel keyboard use without horizontal overflow, and missing-original recovery. [Browser results](browser-results.json) retain the test result. [The modal red receipt](voucher-modal-red.json) established the inaccessible background header and wrong close label before the fix. [The green modal receipt](voucher-modal-green.json) and [return receipt](voucher-return-green.json) show the accessible return and preserved URL.

The existing archive navigation scenario passed in 17.51 seconds. Its three unrelated navigation cases were excluded by the targeted run. [Navigation journey](navigation-journey.json) and [results](navigation-results.json) retain filter, cursor, detail and focus assertions. Both browser and navigation runs retain the same stable source inventory `9e891c3d4f1c434c6011012cd3c6631ff5f808f15f1640a7656b09435fe8a282` in their linked source receipts.

Repeat the browser proof with `OPENERP_E2E_ARTIFACTS=test-results/product-P05-browser-final bun run test:e2e apps/api/tests/document-library-browser.e2e.test.ts`. Repeat archive navigation with `OPENERP_E2E_ARTIFACTS=test-results/product-P05-navigation-final bun run test:e2e apps/api/tests/navigation-context.e2e.test.ts -t 'archive URL preserves'`.

## Remaining integration and limits

Root owns integration onto current main and its resulting checks. This worktree checkpoint does not prove that later integration. Native 200% browser zoom was not observed. Screenshots record the current implementation's behavior. OCR body search remains outside this library contract.
