# Navigation context: local regression evidence

Verified source head: `79d10a6b0a87a828336c6fde4eb9f45d239eb045`, based on main `96247e350b405022c08f8c86fa6d547567c68a27`.

The sales register retains the selected search while a record is open. Closing a record waits for an outstanding register refresh before restoring focus. If the original row no longer matches the search, focus returns to the register. A callback from an obsolete book or an already reopened record cannot move focus on the current screen.

The committed navigation E2E covers a removed opener after a saved title change and a delayed old-book archive response across workspace selection, in addition to the existing return journeys. The final run passed **5/5**, with source inventory unchanged throughout. Total duration was 98.19 seconds; test execution was 89.26 seconds.

```sh
bun run check:changed 96247e3
bun run check:changed:full 96247e3
OPENERP_E2E_ARTIFACTS=test-results/product-P01-router-guard bun run test:e2e apps/api/tests/navigation-context.e2e.test.ts
```

The fast/full gates and the current primary Effect lint configuration passed. Local logs are `/tmp/p01-router-guard-fast.log`, `/tmp/p01-router-guard-full.log`, `/tmp/p01-router-guard-primary.log` and `/tmp/p01-router-guard-e2e.log`. Runtime artifacts are in `test-results/product-P01-router-guard`; the stable source receipt is retained in [product-p01/source-integrity.json](product-p01/source-integrity.json).

A preexisting bank connector feed HTTP 500 remains visible in the fixture's diagnostics. This navigation result establishes neither connector health nor a live provider outcome. Paper remains the visual design owner.
