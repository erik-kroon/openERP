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

## Saved inspection recovery (2026-09-24)

- Added complete bounded SIE preview inventory through migration 8200, Drizzle statement, shared contract and authenticated GET endpoint. History UI lists saved inspections and opens their persistent URLs; capture refreshes the inventory and caches its exact response.
- Contract, API and web type checks all passed on the current worktree. Targeted lint passed. Earlier legal-union errors are no longer present in the latest type-check run.
- Prior scratch database directory no longer exists. Created fresh isolated PostgreSQL at `/tmp/openerp-sie-inventory.VF9ZG4/pgdata`, port 56339, and applied every migration successfully. Database runtime proof: entry function execute allowed, direct preview table select denied, invalid token rejected as Unauthorized. Evidence logs in that scratch directory. This is not full authenticated inventory or browser upload proof.
- Full goal still open: historical mapping/run integration, opening/open-items, real profile seeding/admission, banking connector UI and operation-scoped readiness.
- The new disposable PostgreSQL process was stopped cleanly after verification; its data directory remains for restart. No local review server is claimed live now.

## Plan review and staging (2026-09-24)

- Added plan.tsx (TanStack Form mappings/independent controls/rationale/explicit no-open-items acknowledgement) and run.tsx (start, fenced chunk, pause/resume, same-request retry). Route search includes plan. Saved inventory includes planId/runId via migration8300 and recovers both. Existing run freezes reinspection controls.
- Manual real HTTP proof exposed SQL JSON concatenation precedence failure in 7730. Added forward migration8310 with parentheses in account/year and account/currency compound identities. Never rewrote applied migrations.
- Real HTTP observed: PC8 preview ready, wrong closing balance422, corrected seal200, same-key seal replay identical, start/pause/resume/chunk200, same-key chunk replay identical, final staged count1, saved inventory plan/run IDs. `/tmp/openerp-sie-inventory.VF9ZG4/manual-plan-results.json` contains receipt evidence. No test suite or repository fixtures added.
- CUA browser recovered source -> saved inspection -> plan/run and reloaded final staged status. Full form entry/sealing through browser remains unverified. Targeted lint, web types and diff whitespace check passed before final minor display extraction; latest types log `/tmp/openerp-sie-plan-types.log`.
- Current owned runtime: PostgreSQL56339 at same scratch dir; Node harness session4154, API50216 with local R2 binding; web session86986 at56341. Earlier harnesses34753 and92760 stopped deliberately to add R2/auth bindings. Credentials are disposable and kept out of this record.
- CUA binding reviewTab is IAB tab1, source source_7eb3de7ce0a44c55aa487917d946744f, preview siepreview_6bf11f135e5a4da1990c369b3136f75f, plan sieplan_3558a3478ad449348527a93d4bdb2906, run sierun_a5a96c4d06684abdb90c9e8a2ffb9669; entity_sie_review/book_sie_review. Source original bytes were retained in the first R2-backed harness; availability after harness restart is not claimed.
- Next: open-item editor and reviewed historical-basis/financial admission consumer; source-backed company profile seeding remains necessary for newly created companies to have accounts. Full goal is far from complete.

## Open-item form (2026-09-24)

- Added open-items.tsx with TanStack Form item/control entry and read-only saved details. Parent plan now includes actual supplied openItems/openItemControls instead of hard-coded empty arrays. Each row preserves identity, account, currency, signed original/outstanding amounts, as-of date, asserted payment state, detail availability and basis.
- Unadded draft guards prevent silent omission on sealing; Enter inside child inputs submits that draft rather than the outer plan. Clear draft is explicit. Amounts are labeled minor units throughout.
- Real browser proof on fresh synthetic source: account mappings and independent balances entered; unadded item draft blocked sealing; added item without control produced backend missing-control rejection; adding matching independent total allowed sealing; reload displayed exact source identity, signed amounts, date, unknown payment state, missing detail and independent control basis. Source source_1fdf3798610643c98e9844dc563cd52f, preview siepreview_d428c7e2d856416586ae64831f592027, plan sieplan_4a07c42df6b1487188e697e165504f22.
- Web types, targeted lint and diff whitespace check passed. No automated tests added. Runtime still same API50216/web56341/PG56339. Browser reviewTab still points to this newly sealed plan.
- Next dependency: historical-register admission UI and by-plan recovery. Existing POST /sie-plans/:id/historical-items requires a staged run; GET only accepts admission ID, so add an authorized by-plan read to recover it without exposing internal IDs. Current saved items are in the plan, not yet historical-register admission. Financial basis/cutover and real-company profile registry remain incomplete.
