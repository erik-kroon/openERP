# Customer journal flow — manual runtime evidence

Observed 22 September 2026 in the isolated local development runtime. This is a partial implementation/proof record, not completion of `docs/frontend.md`.

Base Git revision: `c242855a31bc9e0adb067f7592f781b23496b322`, with the shared working tree dirty. Core file SHA-256 values at verification:

- draft.tsx: `23c310b5b475df416c5e183c98311c85602b441fdeee7196e394844b0aa743c6`
- review.tsx: `cf8481c4b5aca60c552a04d12eb76c18c3fd5944da12129cc1b74a57355e35fc`
- review-entry.tsx: `12a948bb6bba0190172711be5dae89b572b78f4ffbce25ee42c8b5234d9fa56a`
- workflow.tsx: `2d557830440458e86f339184b550ecb7204a5181cff2a3fa203762ad04d3c97e`

## Runtime and scope

Web: http://127.0.0.1:3106. API: loopback port 18789. PostgreSQL: isolated port 63180. Entity `entity_automation`, book `book_automation`, actor `actor_automation`, profile `synthetic-core-v1`. Uses the existing synthetic automation book config. No production accounting or external bank action occurred. Secrets remain in the private `.cache/customer-frontend` runtime state; none are included here.

## Observed through the real UI

1. Saved source titled “September clearing adjustment”, origin “Synthetic reconciliation note · 22 September 2026”, with a synthetic explanation of a no-VAT clearing adjustment.
2. Entered date 2026-09-22, series A, accounting period 2026, bank account 1930 debit `125.50`, clearing account 2999 credit `125,50`. Totals showed 125.50 SEK on each side, difference zero, and enabled Review entry. The original server balance validation remained in effect.
3. Prepared the proposal and reached its immutable digest URL. The review loaded the retained source alongside the exact accounting lines, both formatted as 125.50.
4. Reviewed, approved, reviewed the current observation again and posted. The UI showed the server's committed receipt and ledger sequence 1.
5. Reloaded the digest URL. “Posted · Voucher 1” remained, with the same receipt; no posting action remained available.
6. Filtered To do by Completed and search “September”. One matching proposal showed 125.50 SEK and Posted. Opened its review and used Back to work; Completed, search and sort were preserved in both URL and controls.
7. Inspected desktop two-column review and source layouts. At narrow sizes the sidebar becomes an expandable navigation and the source/review panes stack. DOM width/scrollWidth matched at 320 CSS pixels for the English queue; Swedish source was also observed without horizontal overflow at 352 and 291 CSS pixels. Viewport overrides differ from CSS dimensions under the host browser's zoom; these are measured DOM widths, not claimed device sizes.
8. Switched to Swedish, checked source headings, controls and the long primary action, then restored English and the normal browser viewport. One preview connection stall during the locale change recovered after reload; do not count that attempt as seamless locale-switch proof.

## Durable outcome

- Proposal: `change_d7f43494bd64439ab1b3fd77fc844a56`
- Digest: `sha256:0883636aec11c1fffb16361120071639bfdf27a747ca6c18526c577acc959673`
- Receipt: `receipt_cd8987b915a04a2e832453260a8d3bec`
- Voucher: `voucher_66e423ec33ac43899423e83be6906a70`, number 1
- Committed: `2026-09-22T20:41:06.213474Z`
- [Open the retained review](http://127.0.0.1:3106/entities/entity_automation/books/book_automation/reviews/change_d7f43494bd64439ab1b3fd77fc844a56/sha256%3A0883636aec11c1fffb16361120071639bfdf27a747ca6c18526c577acc959673)

To repeat the read proof, start the recorded local runtime, sign in with its provisioned account, open the retained review, reload, and filter the completed queue as above. To repeat preparation, create a distinct, clearly labelled synthetic event in the same isolated environment; do not treat re-entering an already posted event with a fresh reference as a recovery procedure.

## Commands and limits

- `bunx tsc --project apps/web/tsconfig.json --noEmit`: passed.
- `bunx tsc --project packages/ui/tsconfig.json --noEmit`: passed.
- Focused Oxlint for changed journal, route and shared UI files: passed, log adjacent.
- `bun run --filter web build`: passed, including prerender. Log: `.cache/customer-frontend/frontend-build.log`.
- `git diff --check`: passed.
- Full web/UI Oxlint: failed in concurrently added VAT/invoice files (destructuring, raw layout elements, widened dictionary). Log: `.cache/customer-frontend/frontend-lint.log`. No lint rules were weakened.
- No tests or test helpers added. Explicit approval for E2E changes remains unanswered.
- Not verified: lost-response recovery, cross-company switching races/revocation, precision refusal via browser, all supported width boundaries, actual 200% browser zoom, RTL/pseudo-localization, dark/system preference, full keyboard/assistive traversal, performance under representative volume, and the remaining domain/customer journeys.

Final visual pass: moved the record description/date/exact amount above the review panes, made current status and refresh one row, and adapted the shared stacked DataGrid to its container width. At the normal preview width, the debit and credit now remain visible in the narrow accounting pane. The preceding 36rem table minimum had caused horizontal scrolling within that pane. The final grid/layout and posting files pass focused lint; web typecheck passes.
