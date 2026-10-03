# Customer invoice defaults local verification

Implemented customer-owned immutable reviewed email recipients and invoice defaults, exact calendar payment terms, explicit application/override, and qualified catalog article snapshots. New article/default selections use current retained facts; previously copied values survive revision and archive. The application derives article price from the retained revision. Recipient review does not claim mailbox verification or provider delivery. Payment terms language does not localize the complete legal PDF.

The existing customer directory and invoice composer call the same scoped owners. Independent source review found no new narrating comments, suppressions or workaround paths, and traced authorization, current selection and immutable snapshot preservation.

At original checkpoint d2adf927, four feature/performance cases passed. Five warmups and thirty public-boundary trials measured defaults application p95 14.926 ms. Shared pre-feature base 96247e3 measured directory/articles p95 13.610/11.249 ms; head measured 12.424/12.155 ms. The original parent was aafbfbe; the explicitly labelled shared baseline includes P04. See the failure contract for commands and retained artifacts.

After clean integration onto externally advanced main ee971a3, production checkpoint 4e7e38e retained stable patch identity f2f7328408b6eabb7a8eb5ce649bdf9428a42c08. Full changed gate and current primary strict Effect lint passed. Three feature E2Es passed in 27.09 seconds, including real PostgreSQL/workerd admission and the browser composer. Source inventory was stable at fa732407e82575b9a01445cfc21bb7099c47f9cf648fc0689cc88e7e8283188d. Receipts are test-results/product-P06-integrated, /tmp/p06-integrated-full.log and /tmp/p06-integrated-primary.log. A subsequent diff cleanup removes only a blank final SQL line.

An earlier browser timeout remains inconclusive; subsequent diagnostic and integrated runs passed without a behavior fix or increased timeout. This evidence uses synthetic fixtures and disposable local systems. It does not qualify actual-company activation, live email or deployment.
