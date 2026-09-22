# Local SEB statement preview

Implemented scope: inspect an owner-selected SEB CSV in the browser before any book import. The first supplied export has the columns `Bokförd,Valutadatum,Text,Typ,Insättningar/uttag,Bokfört saldo`, newest movements first, UTF-8 encoding and decimal-point amounts. This profile does not claim support for other SEB exports.

The `/intake` route reads a selected local file and displays original row identities, dates, text, type, exact amounts and balances. The user explicitly selects SEK because this CSV has no currency field. No accounting API receives the file. Closing or reloading the page clears its in-memory state. A downloaded review records the source hash, selected currency, parsed rows and diagnostics; retain the original CSV alongside it.

## Failure cases recorded before implementation

- A private-account export, wrong header, unsupported encoding, malformed quoting, wrong column count, blank record, invalid date or malformed amount must fail with a useful locator. Never skip the row or return a partial success.
- Limit file size before reading and row count before rendering; reject oversize files without truncation.
- Preserve quoted commas, escaped quotes, multiline text, original source ordinals and repeated equal transactions. Never deduplicate or reorder movements.
- Parse money exactly with integer minor units. Values above JavaScript's safe integer range must not change during parsing, arithmetic, display or review download.
- Require newest-first booking dates. If running balances disagree, show the affected source rows and distinguish that failure from missing statement coverage.
- An inferred opening balance and the latest recorded balance do not establish full fiscal-year coverage or an independently verified closing balance. Unknown source account and coverage remain explicit.
- A file read/hash failure must not leave old results attached to a new filename. A later selection or reset must supersede an earlier pending file read.
- Preview, changing language, downloading and resetting must not create evidence, journal entries, matches or other backend writes. Company records must not enter source code, static assets, browser storage or shared caches.
- Keep every row reachable on narrow screens and by keyboard; pagination and errors must be named and accessible.

## Verification approach

Run existing lint, type and build commands, and drive the real route with the supplied export. Independently observed controls are retained privately under ignored `output/company-intake/`. Exercise visible error/recovery states and exact downloaded review contents through the browser. Save a local screenshot and a repeatable verification recipe with the observed results. No test or fixture changes are authorized by this packet.

This is the first local inspection slice of IMP-02. Durable source retention, document relationships, reviewed classification, real-company posting and complete reconciliation remain separate delivery work. The production-readiness and synthetic-profile contracts stay authoritative.

## Observed verification, 22 September 2026

The production-built `/intake` route displayed all rows from the first owner-supplied company export. Its generated review preserved every original booking date, value date, text, type, amount, balance and source ordinal; a separate decimal calculation and SHA-256 comparison agreed with the browser result. English and Swedish rendering, keyboard currency selection/submission, reset, and rejection of an unrelated file with a source-line error were observed. The private review, comparison and screenshots are kept under ignored `output/company-intake/`.

Type-aware lint passed, including the full repository lint command. The web build and both prerendered routes passed with `NODE_OPTIONS=--dns-result-order=ipv4first bun run build` from `apps/web`; an earlier default-DNS attempt timed out reaching the prerender server. Full type checking was not green: concurrent changes in API correction/expense-tax and web posting-recovery code produced errors outside this slice. This observation does not certify those modules.

The review export was captured and independently checked from the real browser's generated download link. The in-app browser did not report a native download event, so native download completion is unverified. Narrow stacked rows and a wide layout were visually observed; the attempted explicit minimum-width measurement was inconclusive, and 200% zoom, assistive technology and the full parser failure matrix were not exercised. No tests or fixtures were added or changed. This checkout lacks Git metadata; the private verification record pins the changed source files by SHA-256.
