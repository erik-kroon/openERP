# Document reading end-to-end proof — 2026-09-27

Ten E2E scenarios passed, including the normal self-host server, actual preparation runner, shared private original storage, and real PostgreSQL 17 with a restricted runtime role. Only the external reader is a loopback simulator. No live provider or company data was used.

The browser selected page-backed invoice number and total suggestions, corrected the number to `SELF-HOST-REVIEWED`, completed the line manually, saved the draft and reloaded it. Both totals remained 1,250.00 SEK. The test independently checked the selected reading identity and saved values through the public API. Permanent authorization refusal stopped delivery without another provider submission.

Repeat with `bun run test:e2e apps/api/tests/document-reader.e2e.test.ts`. For browser proof, build the web app first, then set `DOCUMENT_SELF_HOST_BROWSER=1` for that command. Follow the URL emitted in the browser receipt, complete the synthetic draft within the bounded hold, and save the browser completion receipt described by the test. The default run performs draft creation through HTTP.

`results.json`, `junit.xml`, `manifest.json` and `source-integrity.json` retain test results and source identity. `web-source.json` separately records the browser source, which the API harness inventory does not cover. The normal-runtime receipts record the reading, draft and terminal refusal. The screenshot records the reloaded draft. Earlier isolated evidence remains in the adjacent historical directory.

Full changed-branch lint/type checks, frozen dependency installation and the web build passed before this run. This is local integration proof, not live OCR quality, provider qualification, production deployment or Book Zero acceptance. JPEG and encrypted/corrupt PDF handling have no dedicated retained cases. SiftX, shadow routing, hostile-parser process isolation, representative accuracy and cost evaluation remain separate gates.
