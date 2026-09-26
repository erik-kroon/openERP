# Reference parity ledger

Status: **a coverage record, not a completion claim.** Prepared 2026-09-26 from an exhaustive folder-by-folder comparison of the `accounted` reference against this repository. Every reference area was inventoried with a denominator and examined; every extracted capability carries one of four verdicts. This document claims no implementation, test, runtime, company-readiness or external-acceptance status, and it activates no rule, rate, provider or legal profile.

It is the answer to one question: **for every part of the reference, are we at parity, better, or short — and if short, is the shortfall owned?**

Read with the [parity backlog](11-parity-backlog.md), which owns the deliverables, and the [defect register](13-reference-derived-defects.md), which owns what is already shipped but wrong. Placement rules are in [ADR 0011](../adr/0011-reference-parity-backlog.md) and [ADR 0013](../adr/0013-reference-derived-defects.md).

## Verdicts

| Verdict | Meaning |
| --- | --- |
| **PARITY** | We implement it, or a plan owns it, equivalently. |
| **BETTER** | We do it at least as well. Where it matters, the row says why. |
| **GAP** | Neither implemented nor planned. Every row names the owner, or says **unowned** — and **unowned** is the actionable category. |
| **N/A** | Presentation, plumbing or architecture that does not transfer. Grouped, with size, so the denominator is auditable. |

A **short** is not a criticism of the plan. Most shortfalls are a capability the plans already carry with the *rule content* unnamed, and the whole point of this ledger is to hand that content to whoever implements it.

## Coverage

Denominators are non-test, non-build-output files unless stated. Every row was read, not inferred from filenames.

| Reference area | Files | LOC | Examined | Verdict mix |
| --- | --- | --- | --- | --- |
| `src/lib/` (14 originally named folders) | 1,196 | 288,501 | all | 47 PARITY · 69 BETTER · 181 GAP · 42 N/A across the whole reference |
| `src/lib/` (26 further directories) | ~290 | ~55,000 | all | see [lib stragglers](#lib-stragglers) |
| `src/app/` (701 route handlers, 909 methods) | 907 | 155,897 | all inventoried; ~62 logic-bearing read in full | see [route layer](#route-layer) |
| `src/extensions/` | 273 | 101,012 | all | see [extensions](#extensions) |
| `src/components/` | 603 | 153,260 | judged as one surface | N/A — visible product behavior is `apps/web` + `packages/ui`; no accounting consequence |
| `supabase/migrations/` | 999 | 553,986 | every `ADD CONSTRAINT`, every unique index on journal/voucher/invoice/idempotency/observation, ~30 accounting-critical triggers | see [database invariants](#database-invariants) |
| `tests/` (integration surface) | 279 | 62,499 | 12 files in full, ~250 by title | see [test-pinned invariants](#test-pinned-invariants) |
| `scripts/` | 97 | 15,322 | all | see [operations](#operations-and-configuration) |
| `DECISIONS.md` (762 entries) | 1 | 402,527 | **all**, whole file | see [decision log](#decision-log-and-dependencies) |
| `CLAUDE.md`, `AGENTS.md`, `README.md`, configs | 12 | ~29,000 | all constraint-bearing lines | N/A except where noted |
| `docker/`, `.compliance/`, `.github/`, `.env.example` | 37 | ~15,000 | all | see [operations](#operations-and-configuration) |
| `packs/`, `registry/` | 28 | — | manifests and validators | see booking templates |
| Root `package.json`, `next.config.ts`, `vercel.json`, `vitest.config.ts`, `eslint.config.mjs` | 7 | ~25,000 | accounting-relevant lines | see [decision log](#decision-log-and-dependencies) |

**Not examined, and why.** The reference's 2,109 `src/lib/**/__tests__` files were not read; `tests/` is the integration surface and the unit tests would yield pure-calculation edge cases that overlap rules `R1`–`R47`. `src/components/` was judged rather than read, because visible product behavior is owned by `apps/web` and `packages/ui` and carries no accounting consequence. Both are stated so the completeness claim is not overstated.

## The four headline results

1. **We are genuinely ahead in the parts that decide whether figures are right.** 69 BETTER verdicts, concentrated in money representation, immutability, idempotency, tenant scoping, lock ordering, refusal discipline and the approve/prepare/execute split. The reference's own 999-migration chain needed layered triggers plus four session escape hatches to approximate our grant-level append-only.
2. **The largest single shortfall is not a feature, it is proof.** 4 test files and 18 cases against the reference's 2,361 test files. Roughly 47 of the 58 test-pinned shortfalls are things our schema and triggers **already implement and nothing verifies**. This is the cheapest large gap to close and the most embarrassing to leave.
3. **There is a whole capability area with no owner at all: data protection.** A records-of-processing register, a DPIA screening discipline, a data-subject-request runbook, a data-classification inventory and an authorization decision record. Repo-wide, our maintained docs contain **zero** hits for GDPR, records of processing, lawful basis or data-subject concepts. Plan 07 owns backup and retention; the data-protection subset has no owner.
4. **We have no clock.** The reference runs 43 scheduled jobs — retention enforcement, evidence re-verification, bank and tax-authority sync, accounting operations, webhook dispatch — and we have no scheduled trigger anywhere in `infra/alchemy` or the runtime. Every capability the backlog assigns to a schedule is currently unrunnable, including the bank and tax-account feeds.

## Verdicts by area

Each area's denominator and verdict mix. The four headline results above are the ones that change what we do; these are the accounting detail behind them.

### Lib stragglers

The 26 `src/lib` directories not named in the original brief.

| Verdict | Count | Notes |
| --- | --- | --- |
| PARITY | 11 | mail, events, rules, export, firm cockpit, articles, customers, suppliers, supplier invoices, expenses, mileage — every rule already sits inside an owned packet, several line for line |
| BETTER | 4 | mail: sign-loss becomes a typed refusal; authority: segregation of duties is an identity binding, not a scope heuristic; notifications: delivery intent is claimed deterministically before send; firm: portfolio summaries carry no mutation authority |
| GAP | 1 | The reusable posting-pattern catalogue, plus one cross-module rule cluster: no legal-form-conditioned treatment binding exists |
| N/A | 19 | ~12,200 LOC of proxy, entitlement gating, hooks, white-label branding, support, browser, analytics, observability, trusted-host, agent panel, sandbox, navigation, dashboard, lists, UI state, theme, rate limits, XML escape |

### Extensions

| Verdict | Count | Notes |
| --- | --- | --- |
| PARITY | 9 | Filing lifecycles, declaration submit/recovery, taxpayer identity, delivery truth vs send acknowledgement, mail-parse strictness, VAT completeness single-owner, card mirror, POS intake |
| BETTER | 6 | Approval unreachable from the agent surface; receipts permanent rather than a 24-hour cache; one completeness gate by construction; exact money makes relabelling impossible; fail closed on scope rather than park; canonical admission rejects duplicate keys and invalid scalars before sealing |
| GAP | 34 | Concentrated in: the tool-catalog scale problem, the per-tool authority map, filing-specific settlement and period resolvers, intake channel ownership, card-mirror and lookback rules, processor fee mechanics, and the extension manifest |
| N/A | 6 | Widgets, prompt library, calendar and push extensions, example branding |

**The scale finding is the one that changes our plans.** The reference deliberately hides part of its tool catalog behind a search bridge and enforces a byte-size watchdog on the advertised list. We advertise every capability with full input and output schemas in one uncursored list. That is a correctness problem for clients at some size, not a style one, and it belongs with the parity-artifact and allowlist work rather than as a separate concern.

### Route layer

701 route handlers; ~62 carry real logic; 26 read in full.

| Verdict | Count | Notes |
| --- | --- | --- |
| PARITY | 5 | VAT-period completeness, failed sub-aggregate surfacing, foreign-amount partial totals, projection minimisation |
| BETTER | 24 | The majority. Our authority is locked in the same transaction; refusals are codes not message matching; write authority is a two-actor protocol not a flag; concurrency races are closed by lock construction rather than detected and repaired; a failed commit cannot burn a number; cross-tenant links are structurally impossible; dry-run cannot drift from commit because prepare **is** the preview |
| GAP | 27 | 11 already named in a plan; 15 need an owner. The heaviest: the number of per-capability scopes, credential issuance, the SSRF-guarded webhook surface, cash-method booking-basis sequencing and its refusals, and the payment-side duplicate guard |
| N/A | 3 | Scope echoing, a one-off repair endpoint, storage-proxy mechanics |

**Largest remaining uncertainty in the sweep:** roughly 40 provider-callback, OAuth, sandbox-seed and agent routes (~13,000 LOC) were sampled by search rather than read, and are recorded as carrying no accounting rules. That is an inference, not a verification.

### Database invariants

Read the reference's constraints, unique indexes and accounting-critical triggers; compared against our three baseline files plus two forward migrations.

| Verdict | Count | Notes |
| --- | --- | --- |
| BETTER | 13 | The reference needs 999 migrations, layered triggers and four session escape hatches to approximate our grant-level append-only, exact minor-units domain, one-sided line shape, permanent idempotency receipt, content-addressed sealing, encoded lock ordering, immutable book monetary units and single typed refusal channel |
| GAP | 6 | Locked-period write refusal, month-boundary period shape, voucher-date-in-period, credit aggregate cap, bank-anchor settlement/sign, and the one live defect: a balance guarantee whose second code path has no trigger attached |
| REJECT | ~130 row-level policies | Our book-scoped composite keys make cross-book reads structurally impossible without them, which is the better mechanism and was a deliberate choice |
| N/A | 5 | Retention expiry (our absolute immutability dominates a seven-year floor); insert-shape and writer-role triggers (platform-specific bypasses); session escape hatches; retained-annotation path |

### Test-pinned invariants

The reference's integration surface, read against ours.

| Verdict | Count | Notes |
| --- | --- | --- |
| PARITY | 11 | Exact money; same-key replay under concurrency; late-fault rollback; migration rerun and checksum drift; counters unconsumed on refusal; runtime-role append-only; reversal preserves the original; agent admission; cross-book scoping; credential revocation |
| BETTER | 9 | A zero-value line is refused structurally and needed a data repair there; bigint versus numeric; digest-bound idempotency; approval expiry is not absorbing; grant-level append-only proven with the real runtime login; wire-level numeric and duplicate-key admission; full row-count receipts |
| GAP | 58 | **~47 are implemented and unverified.** Our schema and triggers already carry the credit cap trigger target, FX residual, VAT totals and drill-down, tax-account settlement shape, closing detach, allocation bands, payroll opening locks, asset depreciation atomicity and report basis. The remaining ~11 are neither implemented nor tested |
| N/A | 6 | Storage-bucket policies, identity erasure classification, the null-guard pattern they needed, migration reset, company-level rather than book-level twin healing |

**This is the most actionable section in the ledger.** We have the mechanisms and not the proofs, and the cheapest transfer is the eight schema ratchets: they are catalogue queries, not financial fixtures, and they give permanent coverage of a 400-table schema that nothing currently sweeps.

### Operations and configuration

| Verdict | Count | Notes |
| --- | --- | --- |
| PARITY | 11 | Connector delegation, object-store credential, deployment variables, unset-means-nobody gates, retention rule text, backup-to-restore coupling, key custody, quarantine guards, release evidence |
| BETTER | 12 | Database and session secret separation; no browser-visible database credential; column-scoped runtime role; setup-time refusal; startup validation; zero-baseline lint; rounding designed out; no third-party telemetry; credential hygiene |
| GAP | 47 | Headline: no clock; no backup/restore with a privilege-manifest diff; no yearly immutable-backup run; no container hardening; no shipped response headers; no supply-chain gates; no CI database gates; no security-disclosure policy; and the five data-protection artefacts, which have no owner in any plan |
| N/A | 4 | Model-inference credentials, analytics credentials, a counsel-facing data-use clause, machine compliance config |

The credential inventory is worth keeping as a standalone artifact: roughly 150 variables in their example environment against about 25 in ours, and **every one of theirs is either a capability or a credential**. Ours is smaller mostly because we have not built the external integrations.

### Decision log and dependencies

All 762 entries of the reference's decision record, read whole.

| Verdict | Count | Notes |
| --- | --- | --- |
| BETTER | 14 | Rounding, falsy-zero defaults, document immutability, no posted/reversed split, attested-negative facts, contra-account treatment, per-account tax role binding, party-merge discipline, untrusted-source discipline, text storability, no fabricated balances, report basis stored in the snapshot, charset admission, ratchet-and-flip lint |
| GAP | 14 | 4 substantive and 10 narrow. The substantive ones: voucher-gap explanations, the rounding default (**which contradicted one of our own preserved rules — see the correction in `R22`**), the class 3–8 transfer bound, and the externally-closed period case |
| PARITY | 0 new | Every accounting rule the reference decided that we match is already inside a preserved rule, a packet, a defect row or a domain document. This sweep found no accounting rule that is neither implemented nor planned |
| N/A | 4 | Their series-letter preset, which they themselves superseded; a contracted vendor's code treated as a rule; and the date library, which our own defect register rules out deliberately |

**The highest-value output of this area is the incident record**, because that is what makes a rule survive. The reference documents being wrong in ways that generalise: an epsilon nudge that silently degenerated, a raw double sum that filed a rounded figure one unit low, a substring number match that misdirected 31 payments, a keyword-scrape cleanup that flipped the sign of a stored amount, a scheduler threshold that slid an hour every day, a guard whose predicate was a proxy for the thing it protected and therefore excluded a real case, a wire type that lied in one direction and failed loudly in the other, and a bundler constant-fold that disabled a feature in production. Our preserved rules currently carry the **rule** and drop the **reason**, and the reference's own invariants guide says a rule without a recorded reason gets re-litigated within a quarter.

## Unowned shortfalls

Every row is absent from our code **and** from every plan. These need a home before implementation; that decision is not made here.

### Data protection — no owner at all

| Reference artefact | Obligation | Verdict |
| --- | --- | --- |
| Records-of-processing register: 16 activities with purpose, lawful basis, special-category basis, controller/processor, data subjects, categories, recipients with country and transfer mechanism, retention duration **plus basis** and the tables stored in, and named security measures per activity | The whole record-keeping obligation, tied to physical tables | GAP — unowned |
| Impact-screening record with named **re-screen triggers** (before adding message search, analytics, special-category content, cross-customer profiling) | A screening discipline, not a document | GAP — unowned |
| Data-subject-request runbook: access, correction, restriction, portability, erasure, with the **statutory-retention exception documented in the response**, masked-only exports | How we answer a request | GAP — unowned |
| Data-classification and handling: classification tiers, a control list per tier, and a **complete client-side storage inventory** with a per-key deletion trigger and a review trigger | The enumeration discipline | GAP — unowned |
| Authorization decision record: canonical multi-tenant model, shared-resource default with justifying scenarios, compensating controls, and a **deviation protocol** requiring Decision/Why/Compensating-audit before merge | One authoritative record. Our *mechanism* is better; the record does not exist | GAP (document) — unowned |

### Proof and durable-work verification

| Shortfall | Why it matters | Verdict |
| --- | --- | --- |
| **Eight schema ratchets**: every company-scoped table triaged into disjoint buckets; no phantom columns; every emitted processing-event type registered **and** every registered type accepted; the operation-type list closed but complete; foreign-key indexes leading with the FK column; no client-reachable delete under **any** policy name; null-safe tenant guards; the ratchet detector itself tested | 400+ tables, 232 triggers, 70 grants, and **zero** ratchets. A new table silently escapes backup, erasure and export | GAP — unowned |
| Recovery-work verification for the durable queue: claim fencing, terminal rows never swept, concurrent-loser codes | Every concurrent loser is a double-payment path | GAP — unowned |
| No PostgreSQL service in CI: no apply-all-migrations gate, no merge-base upgrade gate, no coverage gate requiring a case per trigger | Our DDL is the enforcement layer and nothing verifies it | GAP — unowned |
| `package.json` `check`/`lint`/`format` reference `apps/web/tests`, which does not exist | A command naming a path that is not there | GAP — small, unowned |

### Accounting rules with no owner

| Shortfall | Reference basis | Verdict |
| --- | --- | --- |
| **Voucher-number gap explanations.** Numbering is sequential and stays so; a gap requires a recorded written explanation, and an unexplained gap is a year-end blocker. The check must enumerate **every registered series**, not only the default one | Statutory audit-trail continuity | GAP — unowned |
| **A future-dated payment is not a business event.** A payment date in the future is a scheduling artefact and must be refused on any posting or settlement path | Statutory event recognition | GAP — unowned |
| **A payment-side duplicate detector.** On full settlement, a business bank row of the same amount near the payment date carrying the counterparty name returns a conflict with the candidates — and the guard runs **before** any preview branch, so a green preview cannot mask it | Our `PRY-39` owns the override half; the detector and the ordering are unnamed | GAP — unowned |
| **Booking templates as pure data.** A reusable posting pattern is data, never executable code; line types are mutually exclusive (a tax line carries a rate and not a ratio, and vice versa), and a pack that does not balance through the real engine is refused. Crucially: a fictitious-tax line is computed as total × rate, not total × rate/(1+rate) — everywhere else it is the latter | A catalogue of reviewed posting shapes, each carrying its own statutory limit | GAP — unowned |
| **Absent is not zero at a provider boundary.** An amount-less provider invoice is not a zero-value invoice and is declined and **counted**; a number-less one is keyed by supplier, date and amount, never by a stand-in number | Provider data is incomplete, not zero | GAP — unowned |
| **Legal form selects the treatment.** An expense liability for a sole-trader owner posts to an equity account, not a liability, and payout grouping skips that account entirely because the firm owes its owner nothing | A legal-form-conditioned binding. May be correctly out of scope while the product is scoped to one company type | GAP — unowned, possibly N/A |
| **Migration scope predicate.** A paid invoice issued **and** settled before the imported years is declined, because its payment voucher already sits in the imported opening balance. Unpaid kept from any year; an unreadable issue date is **kept**, never dropped | Cut-over double-count avoidance | GAP — nearest owner is the historical-adoption packet |
| **A reader that cannot load must not stamp the document.** A document read result is an outcome about the document; a binary the runtime cannot load is an outcome about the environment. Choosing a portable reader over a native one is a real decision, and it is unmade | Retention validity, not ergonomics | GAP — unowned decision |
| **Retention that purges content but keeps the audit skeleton**, and crypto-shreds a revoked secret's ciphertext while keeping its hash and masked form | Preserves the audit trail without keeping the content | GAP — nearest owner is retention |

### Operations

| Shortfall | Verdict |
| --- | --- |
| No scheduled trigger at all, so no retention enforcement, no evidence re-verification, no feed synchronisation, no accounting operations, no webhook dispatch | GAP — unowned scheduling decision |
| No database backup and restore with an **access-control equivalence proof**; the seven-year immutable-backup window as a yearly coordinated run with application and jobs stopped so database and documents are one consistent set | GAP — plan 07 owns the shape; the WORM run and the privilege-manifest diff are unnamed |
| Container hardening: digest-pinned base, unprivileged user, read-only root filesystem, all capabilities dropped, no-new-privileges, resource and process limits, healthcheck bound to the loopback address | GAP — unowned |
| Shipped web response headers: HSTS, frame denial, content-type sniffing denial, a permissions policy, and a strict content-security policy | GAP — unowned |
| Supply-chain gates: SBOM, provenance, an image vulnerability scan on the **published** artifact, dependency scanning, static analysis, pinned action references | GAP — unowned |
| A security-disclosure policy naming period locks, journal immutability and retention in scope, with response times and a safe harbour | GAP — unowned |
| Scheduled-job threshold derivation: a threshold must be strictly less than the period and computed from the **actual fire time**, or it slides every day | GAP — narrow, unowned |
| Migration hazard: before replacing an existing database function, check the other open branches for the same function name; each is green alone and the loss appears only when branches combine | GAP — one clause, unowned |

## Already-better, recorded so it is not regressed

The comparison's most useful output for a product that intends to be better is the list of places where the reference is worse, because that list is what stops a later reader porting its approach.

- **Money.** Exact integer minor units end to end, with a one-sided line shape that makes a zero line and a both-sides line structurally impossible. The reference needed a not-valid constraint plus an approved data repair, and its constraint still accepts a zero line because the engine refuses those instead.
- **Rounding.** A decimal-string exponent shift there, because a fixed epsilon degenerates above two units as the double gap doubles per power of two. Ours never reaches that problem.
- **Document immutability.** Ours is absolute. Theirs needs a name-agnostic ratchet because a production policy existed in no migration file.
- **No posted/reversed split.** A reversal is a separate balanced entry, so the class of bug where a storno double-counts and a loan balance reads wrong cannot arise.
- **Authority in the same transaction as the write.** Row locks on admission, membership and book, credential expiry checked against **database** time, and a per-capability privilege re-assertion. Theirs reads membership separately and repairs races afterwards.
- **Refusals as codes with a named remedy.** Theirs matches Swedish engine sentences in strings, with a comment admitting the brittleness.
- **Coverage as literal types.** `not_established`, `financialCloseReady: false`, `statutoryReady: false` — it is impossible to compile a completeness claim we have not earned. Theirs achieves the same honesty on one endpoint through a best-effort fetch.
- **Segregation of duties as an identity binding.** Ours requires a different preparer and reviewer and tests it; theirs is a scope-pairing heuristic on one key, evadable with two keys.
- **Firm membership confers no book access.** Theirs grants it as a side effect of team sync.
- **Approval separation.** No agent path can reach approval at all, and the agent cannot even self-attest an irreversibility acknowledgement. Theirs can, with a scope.
- **Setup-time refusal.** Independent random secrets written with exclusive-create and owner-only permissions, refusing to overwrite. Theirs copies a template and rewrites one value in place.
- **Migration safety.** A checksum ledger, refusal on drift, and a non-zero exit so the application never starts on an unknown schema. Theirs had to add a prefix to win alphabetical trigger ordering, then re-run a full-table repair.
- **Sign loss is a refusal, not a correction.** Theirs silently rewrites a minus sign because the bundled font lacks the glyph, and a loss prints as a profit. Ours throws on any character outside the fixed font and states that no fact was omitted or replaced.
- **No third-party telemetry at all**, and no browser-visible database credential.

## Maintaining this ledger

A reference area is added only with its denominator. A verdict changes only with evidence from a named file. A row marked unowned moves to a plan when a plan takes it, and the move is recorded here rather than the row disappearing. A finding the comparison surfaced that turns out to be already-owned is corrected in place with a dated note, as happened when the semantic-statement work landed between two passes — a ledger that outruns the code it describes is worse than no ledger.

Run `python3 docs/plans/check-plan.py` after any change here. It validates links, anchors and whitespace. It does not execute product tests, and it does not verify any verdict in this document.
