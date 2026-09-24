# Reviewed partial supplier line credit after payment

Observed 2026-09-24 on the **same disposable synthetic book** as [the purchase and payment HTTP run](ap-swedish-purchase-http.md), after applying forward `8770-supplier-partial-line-credit.sql`. The [token-free request record](ap-partial-line-credit-http.json) has exact input bodies, status codes, digest and voucher IDs, with no credentials. To repeat, first build a new book and reproduce the prior purchase/payment sequence using fresh returned identities; then send these requests with new evidence and idempotency keys.

Against the second accepted purchase (`8000` net, `2000` asserted tax, `10000` gross) with an already applied `4000` payment:

1. Supply a distinct retained credit source. `swedish-purchase-partial-credit-v1` with net `1600`, tax `500` returns `422 InvalidJournal` because the tax does not match the accepted 25% line rate.
2. Submit the exact source line `1600` net + `400` tax = `2000` gross. Review, approve and execute its digest. GET voucher: payable debit `2000`, expense credit `1600`, input-VAT credit `400`. Invoice outstanding becomes `4000`; the payment allocation remains `4000`.
3. Submit a second distinct source line `3200` net + `800` tax = `4000` gross, approve and execute. GET voucher: payable debit `4000`, expense credit `3200`, input-VAT credit `800`. Invoice reports original `10000`, retained payment allocation `4000`, posted credits `6000`, outstanding `0`. Database holds two partial-credit rows against this invoice and one allocation receipt.
4. A further credit `100` net + `25` tax returns `409 StaleDependency` because no unpaid capacity remains. Only the reviewed source lines and unapplied payable capacity can be credited; a paid amount is not refunded.

No provider, production tenant or legal VAT profile was activated. The exact credit-note line amounts and rates are synthetic reviewed assertions tied to retained credit evidence. They do not independently certify statutory validity or recover paid principal. No test files were added.

## Per-line capacity repair (forward 8771)

The first partial-credit implementation read prior line usage from a credit execution receipt, which does not retain the line snapshot. Forward `8771-supplier-partial-credit-line-capacity.sql` reads each committed credit's immutable review instead. In the same isolated book, a new two-line invoice had two `1000` net + `250` tax lines. Crediting line A in full left invoice residual `1250`; trying another `200` net + `50` tax on A returned `422 InvalidJournal` **despite** that residual. Crediting line B in full succeeded and reduced the invoice to zero. Exact requests and IDs are in the `lineCapacity` section of the JSON artifact. No over-capacity line credit was executed.
