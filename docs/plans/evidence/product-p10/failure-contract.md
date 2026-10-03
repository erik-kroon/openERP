# P10 Cash basis failure obligations

Working design. No implementation or verification claim.

Current-knowledge synthetic SEK captures derive recordedCutoff from database time and asOf from the owned Europe/Stockholm business-date policy. Historical economic or knowledge requests refuse. Clients select reviewed retained evidence and account/report refs, never amounts.

A selected complete capacity interval ends at the current economic boundary. Exact statements/row membership prove closing inclusion, including same-day payments. Coverage reports remain not_established. Full-period coverage gaps beyond the selected interval remain visible without becoming a claim about selected current cash. Old closes, unmatched relationships, missing bridges, unknown eligibility/reservations and conflicting sources produce unavailable opening and retained observations. No bridge workflow is accepted in v1.

Public API cases before implementation cover exact two-account opening150000; unchanged financial state; all seven source-family gaps; immutable retry/read/export; new capture after evidence; historical cutoff and caller amount refusal; cross-book refs and revocation; older and incomplete opening observations; same-day exact settlement versus unmatched control payment; partial payment and credit/reversal residual; unknown/foreign amount without zero or1:1; internal transfer without ordinary owning identity; restricted salary nondisclosure; full invoice population and explicit overflow. Expected values come from independently specified synthetic source amounts and literal arithmetic.

The performance fixture contains10000 unpaid invoice records. It does not require increasing the1000-row reconciliation limit. Five warmups and30 ordinary trials must pass capture p95<=3000ms and the comparable parent shared-read budget max(parent*1.2,parent+50ms). No auto-explain timing establishes acceptance.


The owning supplier-settlement path is an explicit additional public vector. A real accrued10000 payable and same-day4000 settlement leaves canonical6000. Independent opening100000 minus matched4000 closes96000. Qualify the exact retained receipt, plan, bank line, statement row and original evidence; cancellation must preserve the old basis bytes, restore10000 canonical remaining and make the old opening unavailable. No date/amount equality may replace this identity. This vector was authored after the first source composition and before any corrective gate or runtime.


Retained body integrity has its own disposable system vector before adding a DDL constraint. A public capture must prove that its application digest equals actual `openerp.digest(body - 'digest')` for the retained body. A direct isolated fixture INSERT with a changed body.digest but recomputed matching content, raw SHA and byte length must fail with23514. Immutable UPDATE/DELETE must refuse. This does not grant application financial calculations to PostgreSQL. Until the canonical equality is observed, the candidate digest constraint is not accepted.

Reviewed expected payment dates are interpreted calendar dates. Public capture refuses an invalid assumption date such as2026-13-15 with400. The contract uses the existing CalendarDate schema. Canonical owner dueOn remains retained verbatim and does not become an invented valid payment date.
