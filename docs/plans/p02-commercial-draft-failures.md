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
