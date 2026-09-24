# Supplier split-payment HTTP observation

Observed 2026-09-24 through local Wrangler HTTP and a disposable PostgreSQL 17 synthetic book, continuing the [reviewed purchase setup](ap-swedish-purchase-http.md). [Token-free requests and results](ap-split-payment-http.json) give exact public payloads, returned IDs and amounts. Repeat on a new disposable book with fresh evidence, returned digests and idempotency keys; follow [local setup](../../local-development.md) and stop only the processes you start.

1. Retain two distinct supplier originals, review exact 25% line-rate assignments and accept/post invoices for `5000` and `7500` minor units. Their source evidence and supplier numbers differ.
2. Retain independent payment evidence and approve/execute a synthetic journal: payable debit `7000`, bank credit `7000`. This is a posted payment source for the commerce register, not a provider result.
3. An allocation attempt for `6000` against the `5000` invoice returns `409 StaleDependency`. Review one payment line split into `3000` and `4000` legs for the two invoices. Approve and apply it; exact same-key retry returns an identical application receipt.
4. GET both invoices: `5000 − 3000 = 2000` and `7500 − 4000 = 3500` outstanding. GET payment-line capacity: `7000` allocated, zero remaining. Another allocation from the same line returns `409 StaleDependency`.

This proves two-invoice conservation and replay through HTTP, not bank settlement. Reported payment-file status and real payee verification are separate from this posted synthetic evidence. No tests were added.
