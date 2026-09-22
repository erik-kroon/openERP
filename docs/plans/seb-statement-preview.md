# Local SEB statement preview

Working scope: inspect an owner-selected SEB CSV in the browser before any book import. The first supplied export has the columns `Bokförd,Valutadatum,Text,Typ,Insättningar/uttag,Bokfört saldo`, newest movements first, UTF-8 encoding and decimal-point amounts. This profile does not claim support for other SEB exports.

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
