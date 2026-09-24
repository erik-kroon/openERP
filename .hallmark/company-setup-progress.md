# Company setup and Accounted parity delivery

Objective: complete the journey from company creation through configuration, historical intake, optional banking and operation-scoped readiness. See the user-supplied goal objective. Customer facts are runtime inputs.

## Current contract

- Preserve existing work (active backend invoice, SIE, banking and payment changes were present before this task and continue in this shared checkout).
- User requested Hallmark and TanStack Form. Audience: founders/accountants; job: company creation and setup; tone: calm/utilitarian. Keep existing StyleX/UI tokens.
- Explicit approval to add E2E tests is pending. No tests or fixtures have been added. Existing checks and manual real-surface verification are allowed.
- Company setup facts do not activate legal accounting rules. New books use `company-setup-v1`, which current posting admission rejects. Real-profile support is still required by the overall objective.

## Delivery phases

1. Company creation and resumable setup (in progress): contracts/API/MCP/SQL and TanStack Form UI. Browser verified creation, retained choices, invalid input, save/reload and cross-step invalid-field focus. Tenant/replay/failure checks remain.
2. Versioned profile registry and seeding: review Swedish primary sources, choose bounded supported scenarios, implement capability-specific admission and seed charts/periods. Not started.
3. Connect historical SIE/opening/open-item and optional banking workflows to setup. Existing implementations need inspection/integration, not parallel substitutes. Not started.
4. Operation-scoped readiness and full journey verification. Not started.

## Decisions and evidence

| Date | Decision / observation | Evidence | Next action |
| --- | --- | --- | --- |
| 2026-09-24 | Company creation is a signed-in-human command; current book operator grants control edits. Same legal identifier is not a tenant key. | 8000-company-setup.sql | Exercise authentication/isolation/replay. |
| 2026-09-24 | Nullable setup fields retain incomplete work; methods and legal forms are facts, not a capability activation. | company-setup contracts and SQL | Complete profile consumer separately. |
| 2026-09-24 | New company/UI contracts and web build/type check passed; targeted lint found raw div, corrected to Box. | /tmp/openerp-company-web-check.log | Rerun lint and browser verification. |
| 2026-09-24 | Existing admission test initially failed before setup migration in prior legal-issue migration. After concurrent migration ordering changes, full migration succeeded on isolated local PostgreSQL. | /tmp/openerp-company-setup.3fGsrr/migrations.log | Run existing admission suite again after integration. |

## Local review runtime

Owned isolated PostgreSQL: `/tmp/openerp-company-setup.3fGsrr/pgdata`, port 56329; disposable data only. Node API harness session 93277 at port 64776; web session 19190 at port 56331. Old Bun API session 29391 was stopped because it hung requests. Stop only owned processes and PostgreSQL after proof. Do not commit this progress record or scratch runtime credentials.

## Latest verification (2026-09-24)

- TanStack Form owns creation and all setup fields; shared Effect Standard Schema validation is active. Reload failures now use a visible Query mutation error. Invalid submission navigates to and focuses the affected field, verified in browser by entering an invalid identity number then submitting from accounting settings.
- Targeted lint passed. Earlier full web build/types passed; latest full type check is blocked by concurrent legal_ar_recognition union changes in corrections/posting recovery, not setup files. Log: `/tmp/openerp-company-types.log`.
- Existing admission E2E suite: 10 passed, 2 failed (immutable approval test mutation; old session route 404). Log: `/tmp/openerp-company-admission-check.log`. No test changes added.
- Narrow browser measured 375 CSS pixels with no horizontal overflow. The browser clamps the narrower requested override to 375; 320 remains unverified. Screenshot rendering had duplicate compositing regions, so do not treat it as a clean visual artifact. Viewport reset afterwards.
- Saved demo company has a roughly two-year fiscal date range; current setup validates date existence and ordering only. Profile eligibility must reject unsupported lengths; do not imply legal validity.
- Browser tab 1 retained for continuation at the setup route, signed into disposable local data. Company scope is entity_1248009e8fab42ba9606d8989f7905e6 / book_67ddb39bfd7e4bb8a67c14eb63c3a0ed.
- Next: source-backed profile eligibility/seeding and operation-scoped readiness, then connect existing history/bank workflows. Riksdagen BFL source opened on 2026-09-24; no new legal activation decision made.

## Historical intake slice (2026-09-24)

- Added `/history` route and `components/historical-intake/panel.tsx`: retained source upload, source inventory, explicit PC8/UTF-8/Windows-1252 selection using TanStack Form, SIE preview capture, diagnostics and reloadable source/preview URL. Reused DocumentUpload with an explicit SIE mode (512 KiB) and existing API contracts. Setup review links chosen SIE intake and manual bank statement paths.
- Production build succeeded; targeted lint passed. Full types remain blocked in concurrent correction/journal/posting-recovery legal union consumers. `/tmp/openerp-history-web-check.log`. Own decoder suggestion corrected after this run.
- Browser confirmed history route renders upload limits, retained-file section and return link. Navigation initially timed out but same live tab subsequently rendered successfully; no process restarted. Upload/preview execution still needs actual browser proof.
- Remaining intake: durable preview inventory (current URL preserves selected preview, but source inventory does not recover prior SIE previews), mapping/controls/plan/run/financial integration, opening/open-item workflow. Do not call this full migration support.
- Next action: implement authenticated SIE preview inventory for a retained occurrence, then use it in the source screen so reload/recovery does not create unnecessary new previews. Existing SQL limits each occurrence to 50 immutable previews.
