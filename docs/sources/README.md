# Official sources and rule research

This register keeps primary-source entry points for OpenERP's runtime, accounting rules, formats and provider contracts. These are research inputs, not activated rules or a statement that the linked version is still current. The documentation consolidation did not re-fetch or legally revalidate them. Preserve retrieval dates, source bytes where permitted, hashes, exact versions, effective intervals and access limitations when preparing a release.

The [external-input contract](../plans/10-external-inputs.md) defines D-01–D-10 and the activation process. [Compliance](../compliance.md) defines the required distinctions. A portal, search excerpt or source URL does not replace a complete applicable rule/schema bundle.

## Retained VAT research

The [Swedish VAT manifest](sweden-vat-sources.json) preserves the original dated source URLs, retrieval results, response/excerpt hashes, bounded excerpts, failed accesses and unresolved enablement fields. Its [decision record](../adr/0002-swedish-vat-profile-boundary.md) states the narrow research scope and remaining blockers. Full source response bodies are not archived; a live re-fetch may differ. No approved profile or legal effective interval is supplied by this manifest.

## Source use

Select the applicable version for the actual fiscal year, company and operation. Treat older edition links and dated protocol specifications as candidates to check, not defaults. MCP protocol support is selected through D-05; legal/framework/schema versions through D-04/D-08; actual provider acceptance through D-10. Bolagsverket research includes access limitations recorded in external inputs. No unavailable page is treated as successfully inspected.

Keep the terms and required notices with any dependency, chart data, taxonomy, schema or fixture actually incorporated. A source's availability does not grant redistribution rights or make its example answers an independent oracle.

## Accounting and formats

- [Bolagsverket service specification catalog, source retrieved through indexed official text](https://bolagsverket.se/apierochoppnadata/lamnaforetagsinformation/digitalinlamningavarsredovisningochrevisionsberattelse/gallandeservicespecifikationerfordigitalinlamningavarsredovisning.5938.html)
- [Bolagsverket digital annual-report API](https://bolagsverket.se/omoss/utvecklingavdigitalatjanster/digitalinlamningavarsredovisning.2255.html)
- [Bolagsverket digital annual-report FAQ, source retrieved through indexed official text](https://bolagsverket.se/sjalvservice/etjanster/lamnainarsredovisningendigitalt/vanligafragoromattlamnainarsredovisningendigitalt.1671.html)
- [BankID signing API](https://developers.bankid.com/api-references/auth--sign/sign)
- [SIE Group formats](https://sie.se/format/)
- [English explanation](https://sie.se/in-english/)
- [company connection contact](https://www.bankid.com/foretag/kontakt)
- [BankID signing](https://www.bankid.com/foretag/tjansten/underskrift)
- [2026 changes](https://www.bas.se/2025/12/04/andringar-i-kontoplanen-2026/)
- [BAS chart material](https://www.bas.se/kontoplaner/)
- [BFN K2/K3 changes from 2026](https://www.bfn.se/fragor-och-svar/andringar-i-k2-och-k3-fran-2026/)
- [BFN archive guidance](https://www.bfn.se/fragor-och-svar/arkivering/)
- [BFN version applicability for K2/K3](https://www.bfn.se/vilken-version-av-k-regelverken-ska-jag-tillampa/)
- [Bokföringslag (1999:1078), especially chapters 4, 5 and 7](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/bokforingslag-19991078_sfs-1999-1078/)
- [Skatteverket SRU file transfer and subsequent signing](https://www.skatteverket.se/filoverforing)
- [Skatteverket AGI technical description 1.1.18.2](https://www.skatteverket.se/foretag/arbetsgivare/lamnaarbetsgivardeklaration/tekniskbeskrivningochtesttjanst/tekniskbeskrivning11171.4.7eada0316ed67d7282a791.html)
- [Skatteverket KU technical specifications and schemas](https://www.skatteverket.se/foretag/skatterochavdrag/kontrolluppgifter/testtjanstochtekniskbeskrivning.4.233f91f71260075abe8800073614.html)
- [Skatteverket KU exceptions](https://www4.skatteverket.se/rattsligvagledning/edition/2026.13/325651.html)
- [Skatteverket AGI data requirements](https://www4.skatteverket.se/rattsligvagledning/edition/2026.13/368347.html)

## Runtime and transports

- [Hyperdrive connection pooling](https://developers.cloudflare.com/hyperdrive/concepts/connection-pooling/)
- [Cloudflare Hyperdrive query cache/read-after-write behavior](https://developers.cloudflare.com/hyperdrive/concepts/query-caching/)
- [Hyperdrive supported features](https://developers.cloudflare.com/hyperdrive/reference/supported-databases-and-features/)
- [Cloudflare Queues delivery guarantees](https://developers.cloudflare.com/queues/reference/delivery-guarantees/)
- [R2 data location](https://developers.cloudflare.com/r2/reference/data-location/)
- [Cloudflare TanStack Start guide](https://developers.cloudflare.com/workers/framework-guides/web-apps/tanstack-start/)
- [Effect installation](https://effect.website/docs/v4/getting-started/installation)
- [Effect 4 Layers](https://effect.website/docs/v4/requirements-management/layers)
- [MCP tool contracts, dated specification](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)
- [MCP tools specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [Official MCP TypeScript SDK server transports](https://ts.sdk.modelcontextprotocol.io/server)
- [PostgreSQL's numeric documentation](https://www.postgresql.org/docs/18/datatype-numeric.html)

## Verification tooling

- [testing overview](https://developers.cloudflare.com/workers/testing/)
- [harness guide](https://developers.cloudflare.com/workers/testing/test-harness/get-started/)
- [official API testing guide](https://playwright.dev/docs/api-testing)
- [configuration reference](https://playwright.dev/docs/api/class-testconfig)
- [recording options](https://playwright.dev/docs/test-use-options)
- [Playwright's server support](https://playwright.dev/docs/test-webserver)
