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

### Historical-register recovery by plan

Added GET `/sie-plans/:id/historical-items`, backed by migration 8320 and the restricted SQL function. Existing plans without admission return JSON null; nonexistent plans return NotFound after authorization. The staging screen reads this endpoint, checks the source-plan ID and digest, and displays saved register item count without implying ledger posting. Refresh reloads both staging and admission.

Verification: repository `bun run check-types` passed (including its build steps), targeted Oxlint and diff whitespace checks passed. Migration applied to the owned PostgreSQL instance on port 56339. Runtime-role calls verified null for the known unadmitted plan, NotFound for a missing plan, and Unauthorized for an invalid token. Saved-admission recovery and browser rendering remain to verify; admission creation UI remains to implement. No tests added.

### Open-item register save control

Added `historical-intake/admission.tsx` using TanStack Form. The staged-run consumer shows it only after successful admission recovery returns null and staging is complete. It requires a rationale and an explicit open-items-only scope confirmation, sends unknown chronology with empty payment/match arrays, and states that the register is immutable and has no ledger posting effect. Uncertain writes lock editing and retry the exact original mutation variables/key. Successful saves populate the scoped recovery cache.

Web check-types/build passed and targeted lint passed. Browser submission and reload recovery remain to exercise against the updated API. This implements only the explicit no-payment-history branch; supplied payment/match editing remains unfinished, as do broader goal requirements.

### Browser proof: staged open-item register and reload

Using the owned synthetic review company and plan `sieplan_4a07c42df6b1487188e697e165504f22`, the browser started staging, staged its one voucher, rejected save without scope confirmation, then saved the one-item register after explicit confirmation. A full reload recovered “Historical register saved: 1. No financial posting effect.” and removed the creation form. Fixed the invalid-submission message to use TanStack Form submissionAttempts rather than isSubmitted; visibly verified the feedback before saving.

The old review API was serving pre-change routes (404 on recovery). Restarted only owned review servers: API session 86896 at http://127.0.0.1:52167; web session 18833 remains http://127.0.0.1:56341. Database unchanged at 56339. Retained preview staging and admission succeeded after restart. Original R2 byte persistence across restart has not been independently checked. Targeted lint and whitespace checks passed; no tests added. Payment/match entry, financial cutover, profile seeding, bank onboarding and broader readiness remain open.

### Saved admission disclosure

The recovered register now displays its saved rationale and explicit known/unknown payment chronology, with an expandable receipt containing admission ID/time and supplied payment/match records. Browser reload verified the synthetic receipt `historical_691e02f7dc9f485aacba77f93f23ccb8`, unknown chronology, and zero supplied payments/matches. Targeted lint and web TypeScript checks passed. This does not complete payment-history entry or financial cutover.

### Fiscal-year basis inventory and full-history selection

Added migration 8330 and scoped GET `/historical-bases`, returning fiscal-year dates and existing decisions (including opening posting status). The staging screen now consumes it. TanStack Form provides full-history selection for an unselected year only after source staging; independent account balances and source basis start blank, with an explicit cutover date and rationale. The existing SQL workflow enforces one source year, exact complete mapped controls, no conflicting posted history, operator authority and immutable selection. Unknown write retries retain the original payload/key.

API and web TypeScript checks and targeted lint passed; migration applied to local DB. Runtime-role inventory read returned fy_2026, its exact dates and null basis. Browser selection remains unverified; the local API harness needs reload for the added inventory route. Opening-set proposal/approval integration remains unfinished. All six original goal areas remain in scope.

### Basis verification uncovered a transport contract defect

The new inventory and full-history form rendered through the HTTP server. Native date entry did not accept the automation fill, and opening its picker crashed the in-app browser; browser submission remains unverified. Direct HTTP inspection then found selection rejected before reaching SQL: its route inherited ChangePath (requiring `id`) although POST `/historical-bases` has no `:id`. Corrected that endpoint to Scope parameters. The API harness must reload to verify the fix, incorrect-control rejection, successful selection and replay. No basis was saved by these attempts.

Owned current runtime handles: API session 69172 at 52921; web session 51544 at 56341. PostgreSQL remains 56339. Do not treat the interrupted browser attempt as a successful validation test.

### Full-history posting and opening-balance paths

Implemented a substantial historical-import slice, preserving the full original goal:
- Migration 8340 retains source-voucher→ledger-proposal links and exposes a financial workspace by source run. Preparation derives exact ordered TRANS amounts and mapped accounts server-side, ties evidence to the source hash/plan/voucher, and requires the current fenced cursor. No browser-supplied journal amounts are accepted by this preparation endpoint.
- Browser controls start/pause/resume, prepare, explicitly review/approve, and post each voucher using existing accounting approval and receipt authority. Reload recovers the current proposal and posted receipts. New proposals can replace stale dependency snapshots; uncertain writes retain their payload/key.
- Migration 8350 atomically prepares an independent opening journal and selects its opening-set basis. The TanStack basis form now offers both full history and opening balances. Opening proposals link to the existing review/posting screen. Zero controls are explicitly omitted from opening journal lines.
- Migration 8360 compares complete native closing balances (including accounts absent from source controls) against mapped independent source closing controls. It holds the book barrier so balances and ledger sequence agree. It does not claim source completeness or tax correctness.

Runtime evidence in `/tmp/openerp-sie-inventory.VF9ZG4`: basis-proof.json, financial-proof.json, opening-proof.json, closing-proof.json. Full-history HTTP: wrong controls422, correct selection200, identical replay; stale prepare409; prepare/approval/post200; repeated preparation/post return same receipts; workspace recovery. Opening HTTP in separate synthetic book: unbalanced422, prepare+select200, identical replay, approve/post200, recovered posted basis. Closing comparison returned two exact zero differences at sequence1.

Browser in synthetic book_browser_import: started financial import, paused, reloaded paused state, resumed, prepared source voucher, reloaded proposal, rejected approval without review confirmation, explicitly approved, posted, reloaded, and recovered source A:1→voucher1 receipt. Native date-picker crash from prior basis-form attempt remains a browser limitation; basis submission itself has HTTP proof but not full browser proof.

Root check-types (including builds and API tests typecheck) passed before the small approval-renewal UX edit; targeted lint passes. No new repository tests or fixtures added. Current API owned session90644 uses reloadable review-server.mjs (TTY; send `reload` to update source), URL55207. Web remains56341 after restart. Remaining historical gaps include supplied payment/match entry, stale opening proposal recovery, responsive craft, and expanded failure/tenant proof. Real-profile registry/seeding, banking setup and operation-scoped readiness remain required.

### Supplied payment history, opening recovery and posting guards

- Completed the supplied-payment branch with TanStack Form entry for payments, matches and independent totals. Unadded drafts block save. Review displays dates, account/currency and match references. The immutable saved receipt includes payment and match controls.
- Browser proof on plan `sieplan_abc8ec505ca547678a71d6adc47ee9ef`: an unfinished payment draft blocked admission; a payment without its independent control was rejected; one payment and one match of 5000 minor SEK, with independently entered matching totals and dated chronology, saved successfully. Reload recovered receipt `historical_5e5c6c6f6f4f4fb4a3ae2842804fdf71`, all records, dates, references and totals. HTTP artifact: `/tmp/openerp-sie-inventory.VF9ZG4/payment-recovery.json`.
- Migration 8370 adds opening-proposal replacement with an expected-current-proposal guard, retained replacement link, fresh approval and a voucher trigger permanently rejecting superseded proposals. The basis decision, balances and cutover remain unchanged. TanStack Form exposes period, series and replacement rationale beside the unposted opening review link.
- `refresh-proof.json` in the same scratch directory records wrong/stale expected IDs409, replacement200, identical retry200, browser-created replacement recovery, approval/post200, old proposal after posting409, replacement after posting409, and foreign-book read/write403. Browser reload showed the posted opening and removed replacement controls.
- Migration 8380 protects prepared source-voucher proposals from direct ledger execution while their run is paused or finished. `guard-proof.json` records two prepared/approved proposals, paused direct execution409, resume and owning-run posting200, duplicate rejection409, and closing comparison at sequence1 with zero differences. The completed duplicate was rejected by the existing economic-posting uniqueness guard; the paused attempt exercised the new trigger.
- Browser closing comparison for the earlier full-history import now verified. Responsive inspection at actual CSS viewport320 found no document overflow or overflowing input/button/textarea in the expanded payment form. Viewport restored afterward. Browser content export is unsupported; structured runtime receipts are retained instead.
- Root `bun run check-types` passed after payment/recovery changes, including builds and existing test typechecks. Targeted Oxlint passed. SQL migrations8370/8380 applied to the disposable PostgreSQL database. No repository tests or fixtures added.
- Current handles: PostgreSQL56339; API55207 session90644 (TTY reload supported); web56341 session82816. CUA `reviewTab` is tab3, now on entity_opening_refresh/book_opening_refresh; marked for handoff. Browser handles `proofBrowser` and original reviewTab remain available.
- Full goal remains open. Next broad work: supported profile registry/chart and period seeding, optional banking consent/mapping/sync UI with honest provider status and manual continuation, and company/period/operation readiness. Existing connector contracts record operator-attested consent with providerConfigured:false; do not label that a live bank connection. New companies still have no seeded chart/periods and cannot post under company-setup-v1.
