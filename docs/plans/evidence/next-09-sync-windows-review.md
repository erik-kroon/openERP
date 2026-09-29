# NEXT-09 complete provider sync windows: wiring and runtime review

Date: 2026-09-29. Packet: [NEXT-09 complete Plaid sync windows](../../specs/next-01-25/packets/NEXT-09.md). Scope of this record: what was built, what was actually executed, and what remains unobserved. It is not a provider, company or statutory claim.

## What changed

| File | Role |
| --- | --- |
| `apps/api/migrations/0036-next-09-sync-windows.sql` (new) | Stream pointer, generation header, page chain, staged candidates and the publication marker, with narrow grants |
| `packages/contracts/src/bank-sync-windows.ts` (new) | Claim, page, publication and window-state contract; the `bankSyncWindows` API group; the read-only agent capability |
| `packages/contracts/package.json` | `./bank-sync-windows` subpath export |
| `packages/contracts/src/api.ts`, `capabilities.ts` | registers `BankSyncWindowsApi` and `BankSyncWindowsCapabilities` |
| `apps/api/src/db/banking/sync-windows.ts` (new) | Tx-passing reads and DML: stream lock, generation, page chain, candidates, publication, state projection |
| `apps/api/src/application/banking/sync-windows.ts` (new) | The window owner: claim, page append, publication and the derived state read |
| `apps/api/src/transport/http/routes/bank-sync-windows.ts` (new) | `POST …/banking/sync-windows`, `/pages`, `/publications`, `/state` |
| `apps/api/src/index.ts`, `application/capabilities/index.ts` | registers the handlers and the capability |
| `apps/api/src/db/banking/shared.ts`, `application/banking/shared.ts` | the five new tables in the access probe, and the stream's mutable columns |
| `apps/api/tests/sync-windows.e2e.test.ts` (new) | Seven E2E cases over real HTTP |
| `docs/plans/domain-leaf-integration.json` | `bank-sync-windows` moved from `deferred` to `wired` with a real consumer |

`bun run check:integration` passes at **28 wired, 20 declared deferred, 48 leaves**, up from 27 wired. The ratchet failed first, correctly, with *"declared deferred, but 1 consumer(s) exist"*, and only passed once the entry was made honest.

## The gap this closed

The connector owner retained a cursor and a page batch per delivery, but **nothing recorded where a window began**. A crashed run could not be resumed, and a partial page chain was indistinguishable from a complete one. That is exactly the limitation the existing feed reported as `PAGINATION_START_NOT_RETAINED`.

The window is now the unit of truth. A claim fences the stream and either resumes the incomplete generation with its base cursor and staged pages, or opens a new one at the published cursor. A page append retains the exact response bytes under the current fence. A publication marks one complete generation visible.

## Decisions the owner makes, and refusals it makes instead

1. **The published cursor moves only with a publication marker.** Page retention alone never moves it, so an unfinished window leaves the stream exactly where it was. The marker is unique per generation *and* per stream per from-version, so a generation publishes once and a stream cannot advance twice from one base.
2. **The caller's fence, not the current one.** Publication takes the fence the caller proved. Without it a superseded worker could publish over a newer claim, which is the single thing the fence exists to prevent. The stream `UPDATE` additionally names the expected version, the expected fence and the generation's base cursor, and **returns the affected row count** — a guarded update matching nothing rolls the whole transaction back rather than leaving a marker nothing published.
3. **The raw digest is recomputed here**, from the bytes the request actually carries. A caller cannot assert a digest about content it does not prove, and the page row indexes the existing `intake_contents` bytes rather than copying them.
4. **A staged generation is never canonical.** The state read reports `acknowledgement: "staged_only_no_publication_marker"` and `canonical: false` while candidates are staged, and the read model deliberately excludes the candidate rows so no reader can present them as a statement.
5. **An unchanged cursor publishes honestly.** A provider that reports no changes produces a real zero-change marker with `coversHistory: false`. It is never a claim that historical coverage is complete.
6. **Consent revocation blocks new pages**, not just publication, and it does not erase the pages already retained.

The leaf is composed at four boundaries: `claimWindow`, `appendPage`, `publishGeneration` and `replayPublication`. Each leaf refusal code maps to a typed failure with the leaf's own message retained as the cause, so an operator sees which bound refused rather than one generic "invalid journal".

## What the runtime actually showed

Seven cases over real workerd, real PostgreSQL 17.11 and the restricted `e2e_runtime` role, with the whole migration chain applied and the source inventory stable:

| Case | What was observed |
| --- | --- |
| Two-page window | One marker, `pageCount "2"`, `changeCount "3"`, cursor advanced `""` → `C2`, `coversHistory: true`. Read back independently: 2 page rows, 3 candidate rows, exactly 1 publication, 2 content rows. |
| Superseded fence | An unexpired lease blocks a second claim. After lease lapse the takeover bumps the fence and **resumes** the same generation with `requestCursor: "C1"`. The old fence is refused at the page boundary *and* at publication; the published cursor stays `null`. |
| Page conflict | The same page re-offered verbatim returns `replayed: true`; a different raw response for the same ordinal is `IdempotencyConflict` and the stored digest is unchanged. |
| Mutation restart | A new generation opens at the **published** cursor, not the failed page cursor: both generations carry `base_cursor ""`, with attempts `0` and `1`. The abandoned generation keeps both its pages. |
| Unchanged empty poll | A real publication with `changeCount "0"` and `coversHistory: false`. |
| Incomplete window | A non-terminal page refuses publication; consent revocation then refuses the next page while the retained page survives. |
| Repeated command | The same key returns its own publication id; a different key is `AlreadyPosted`; the stream advanced exactly one version. |

The full suite passes alongside it: **155 tests across 38 files**.

## Corrections made during the build, recorded because they change what the code claims

- **A cursor sentinel was wrong and was removed.** The first wire contract carried `isMinLength(1)` and the owner substituted an `"empty"` token. That is a real collision: a provider may legitimately issue that token. The contract now carries the empty string verbatim, because a first window genuinely has no cursor.
- **The manifest agreement check was a tautology, then wrong, then removed.** The leaf's `assertManifestAgreement` expects both digest lists to be the same family; the raw page digest and the normalized-change digest never match, so it refused every publication. The stronger property is now computed directly: each page's change digest is **recomputed from the staged candidate rows** and compared to what the page committed to. A page whose staged rows no longer hash to its own commitment refuses. `assertManifestAgreement` is no longer called, because the recomputation subsumes it and the leaf's shape does not fit this storage.
- **The request and response shapes were the same schema**, so a read request had to carry a `streamId` it cannot know. They are now `ReadSyncWindow` (request) and `SyncWindowState` (derived answer).
- **The candidate insert wrote NULL ordinals.** The `jsonb_to_recordset` column names are the table's own `snake_case`, and the encoded keys were `camelCase`. Every candidate insert hit a constraint error.
- **A read path took a row lock.** The state read called `readConsentForUpdate` under a shared lock, which the runtime role cannot do. It now uses the connector owner's plain consent read.
- **Counts were widened to JavaScript numbers on the way out.** The leaf returns exact counts as canonical integer strings, so `pageCount` and `changeCount` are strings on `WindowPublication`; they are only `Int` inside the state projection, where they index retained rows rather than money.

## Deliberate omissions, stated rather than smoothed over

- **No provider call, and no job.** Claim, page and publication are three short transactions with no remote call inside them, exactly as the packet requires. The persistent Bun job that owns the HTTP call and the page loop does not exist. Nothing here has contacted Plaid or any provider.
- **The consent is operator-attested, not provider-verified**, and the existing connector owner already says so. This packet does not change that.
- **The candidate rows are staged, not canonical.** NEXT-10 is what turns a published generation into reviewed bank observations; until then a published window is a coverage claim about the provider's changes, not a statement.
- **No admission, matching or posting.** Nothing in this packet creates a bank observation, a match or a voucher.
- **The lease has a fixed 300-second bound** and no renewal operation, because the job that would renew it is not released. A window longer than that must be re-claimed; the resume path keeps its base cursor and staged pages, so re-claiming is not data loss.
- **Real-company, provider and reconciliation signoff remain unobserved.** Nothing here qualifies a provider against retained statement or coverage evidence.
