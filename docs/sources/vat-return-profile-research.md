# Swedish VAT return preparation: field and rounding research

Status: primary-source research and a proposed bounded implementation contract. **No legal profile is activated.** No company facts are accepted, no return is filed, and no tax/payment action is authorized by this document.

Research date: 2026-09-22 UTC. This supplements, but does not silently amend, [the earlier VAT research ADR](../adr/0002-swedish-vat-profile-boundary.md) and [source manifest](sweden-vat-sources.json). The existing expense-tax module remains a review foundation, not a return engine.

## Result

The main tax-amount rounding gap has a direct primary source: **Skatteförfarandeförordning (2011:1261), 22 kap. 1 § says to report whole kronor so that öre fall away.** This rules out rounding tax amounts to the nearest krona. The XML page independently fixes whole-number format, field names, period encoding, box 48/49 signs and full-return replacement for amendments.

There are still narrower interpretation and release gates:

- The sources describe period totals and integer fields, not a worked multi-invoice rounding example. Aggregate exact, reviewed amounts into each period box before discarding öre. This is the engineering interpretation of those sources, not a quoted algorithm from Skatteverket.
- 22 kap. 1 § expressly addresses tax/fee amounts. The form also says “Ange endast kronor, ej ören” for its fields, but this review found no explicit worked rule for fractional **taxable basis** in box 05. The narrowest implementation can require box 05's exact aggregate to be whole kronor, avoiding that remaining question rather than guessing.
- The XML instructions explicitly permit a negative box 48 after purchase credits. The signed truncation interpretation is to discard the fractional magnitude, not floor toward negative infinity. No official worked negative-öre example was found. Keep credit-note calculations and negative component boxes outside the first active scope until that interpretation and correction-period rules receive domain approval. A negative box 49 caused by ordinary positive deductible input exceeding output is explicitly supported.
- Page metadata and the XML version are not legal validity intervals. Current-source and company-specific review still precede activation. Exported XML is not signed, filed, accepted or paid.

## Proposed first actual preparation profile

Candidate name only: `se-domestic25-accrual-return-preparation-v1`. This is a recommendation for a real return-preparation slice, **not** another input-placeholder workspace and **not** permission to change `actual_company` expense exclusions into supported contributions.

### Eligibility and source contract

1. One identified Swedish legal entity/book, SEK accounting and invoice currency, scale 2, accepted VAT registration and explicit `faktureringsmetoden` covering the source dates and exact registered reporting interval. Read the real period; never infer registration, method, due date or the fiscal year from a filename.
2. Reviewed ordinary domestic standard-rate supplies and purchases only. Evidence must establish place of supply, supplier VAT liability, applicable 25% treatment and full purchase deductibility. “Domestic”, a Swedish address, a BAS account or a printed rate alone is insufficient.
3. Freeze immutable, source-backed sales and purchase facts with invoice/component identity, evidence digest, source and reviewed net/VAT/gross minor units, issue/receipt/supply/accounting/tax-point dates, reviewed period basis, treatment/rule revision and ledger references. Unknown is not zero. Source/reviewer differences and duplicate or unreconciled facts block readiness.
4. Use already evidenced and reviewed invoice VAT; this profile **does not choose invoice-level fractional-öre rounding**, calculate a net/VAT split from gross, or repair disputed invoice amounts. If the first implementation also validates net × 25%, either require exact division in minor units or retain a separately reviewed invoice calculation basis. A return-rounding rule does not resolve invoice-tax rounding.
5. Exclude advances, cash accounting, cross-border supplies, reverse charge/imports, exemptions, reduced rates, special schemes, partial/private deduction, foreign currency, credit notes, bad debts, late/disputed timing and tax-account movements. An excluded applicable transaction blocks a complete return; it must remain visible in a partial worksheet.
6. Establish source coverage and ledger-control reconciliation separately. An empty retained inventory or zero supported contributions is not proof of a zero return. Pin the reviewed coverage basis, cutoff, selected facts, explicit exclusions and independent control results in the snapshot.
7. Before activating a dated release, review all applicable clauses and transitions for a selected interval. The observed 2026:118/119 transitions alone do not prove that all standard-rate eligibility rules remain unchanged until 2028. A first release can deliberately restrict itself to a reviewed 2026 reporting interval rather than promise historical or future coverage.

### Calculation contract proposed for review

```text
reviewed facts at fixed period and ledger cutoff
  -> exact period sums in öre, separately for 05, 10 and 48
  -> preserve each fact's contribution and every exclusion
  -> convert tax totals 10 and 48 to whole kronor by dropping öre
  -> 49 = reported box 10 - reported box 48
  -> preserve exact totals, reported totals and each signed difference
  -> immutable draft snapshot / separately approved preparation artifact
```

For this nonnegative first scope, dropping öre means integer division by 100. Preserve `exactMinor - reportedKrona * 100` for each rounded component. Do not truncate each invoice before summing. Do not calculate box 10 by applying 25% to the already rounded box 05. Do not round the exact net VAT independently into box 49: the official instruction defines 49 from the reported tax boxes. A nonzero exact-to-reported difference is an explained reporting residual, not a silently altered source or an automatically approved rounding voucher.

For the strict first release, require the exact box 05 sum to be divisible by 100. That restriction is a product boundary, not a claim that Swedish law rejects fractional sales bases. A reviewer can later approve the broader basis-truncation interpretation without changing old snapshots.

The general box 49 formula is `10 + 11 + 12 + 30 + 31 + 32 + 60 + 61 + 62 - 48`. Reduction to `10 - 48` requires reviewed absence of every other contribution. The application must not simply ignore other boxes.

### Wire contract directly observed

| Meaning | XML / requirement |
| --- | --- |
| Header | `<?xml version="1.0" encoding="ISO-8859-1"?>` then `<eSKDUpload Version="6.0">` |
| Entity | `<OrgNr>`; 10 digits in `xxxxxx-xxxx` format for the registered identity described by the source |
| Period | `<Moms><Period>YYYYMM</Period>`; month itself, last month of a registered quarter, or last month of the taxable year |
| Box 05 | `<ForsMomsEjAnnan>` |
| Box 10 | `<MomsUtgHog>` |
| Box 48 | `<MomsIngAvdr>`; ordinary input deduction has no leading minus; net repayment of input deductions has a leading minus |
| Box 49 | `<MomsBetala>`; payable has no leading sign, refund has `-` immediately before the digits; always required |
| End | `</Moms></eSKDUpload>` |

Use the page's numbered-table order: within this narrow subset 05, 10, 48, 49. The page says this order controls, but its **all-fields example orders groups differently** from its numbered tables. That is a real source inconsistency for broader profiles; this narrow subset has the same relative order in both. Do not generalize the serializer to every field from the example alone.

The page's “Övriga fel” character sentence says only A–Z, `<`, `>` and `/` are allowed, while its own valid header, identity and amount examples contain digits, quotation marks, hyphens and other required syntax. Do not turn that prose into a document-wide character whitelist. Use valid XML and the field-specific rules. Optional free text (maximum 300 characters) is unnecessary for the first deterministic artifact; omit it rather than invent an encoding fallback. No public XSD was linked from the inspected instructions. Portal acceptance remains a separate, unperformed check.

An amendment file replaces the **whole return for the original reporting period**, not only changed fields and not a delta posted into the current period. Preserve original snapshot/artifact bytes, period, digest and any external receipt; prepare a new complete version with explicit lineage and separate approval. The first profile can model this artifact relationship without pretending to support all credit-note/tax-timing calculations.

## Independent arithmetic examples (documentation only)

These are hand-derived acceptance candidates, not test/fixture code and not legal certification. Values are SEK unless marked öre. Tax amounts below are assumed accepted invoice facts; their legal eligibility is a separate prerequisite.

| Case | Exact period inputs | Reported result and deciding observation |
| --- | --- | --- |
| Ordinary payable | Sales net 1,000.00, output 250.00; deductible input 100.00 | 05 = 1,000; 10 = 250; 48 = 100; 49 = 150. |
| Refund, not payment receipt | Same sale; deductible input 300.00 | 49 = -50. XML uses `<MomsBetala>-50</MomsBetala>`; nothing proves a refund was paid. |
| Aggregate before dropping öre | Two sales: net 202.40/output 50.60 and net 203.60/output 50.90 | 05 exact = 406.00; output exact = 101.50; 10 = 101. Per-invoice truncation would incorrectly produce 50 + 50 = 100. |
| Box equation versus rounding the net | Same sales: output 101.50; purchase deductible input 100.60 (net 402.40 at 25%) | 10 = 101; 48 = 100; 49 = 1. Exact net VAT is 0.90. Truncating that net would produce 0 and violate the declared box equation. Preserve net residual `90 - 100 = -10` öre; no silent ledger posting. |
| Ordinary deduction sign | Output 250.00, input 100.00 | Box 48 is +100 conceptually, serialized `100`, not `-100`; 49 = 150, not 350. |
| Non-whole basis boundary | Sales net 100.04/output 25.01 | Tax rule gives 10 = 25; strict first profile refuses final preparation because 05 has a 4-öre basis remainder. It may display the exact worksheet and the explicit unsupported basis-rounding boundary. |
| Purchase-credit sign, future scope | Output 0, positive input 20.00 and input reduction 50.00 | Net 48 = -30; formula gives 49 = +30. XML sign semantics are explicit; credit eligibility and period handling still need their own approved profile. |
| Negative fractional component, unresolved worked-source proof | Future-scope net input -30.99 | Proposed truncation gives -30, not floor(-30.99) = -31. This is an interpretation candidate, not an activated expected result. First scope rejects it. |
| Replacement, not delta | Old same-period boxes 05=1,000, 10=250, 48=100, 49=150; corrected eligible values 05=1,200, 10=300, 48=100 | Replacement contains 1,200 / 300 / 100 / 200, not only the differences 200 / 50 / 0 / 50. Old bytes remain unchanged. |
| Missing versus true zero | No records retained, coverage unknown | Not ready; never automatically create a zero return. Only an independently reviewed complete zero-activity period can produce 49=0. |

Every real fixture must independently establish invoice facts, source coverage, registration and period applicability. These numbers cannot substitute for that evidence. No tests were created or changed by this research.

## What remains before approval and verification

1. Domain/accounting reviewer accepts or corrects the explicit period-aggregation interpretation, box 49 equation treatment and ledger residual/control policy. Resolve fractional box 05 bases before relaxing the conservative restriction. Confirm signed truncation with a worked primary example or qualified review before negative component support.
2. Select and archive the applicable rule release and supported interval. Review registration, accrual attribution, standard-rate eligibility, full deduction and all changed exception clauses. No `approvedProfileId` or validity range is set here.
3. Owner supplies actual company/period/source facts (D-04). Neither this research nor an operator role proves their truth. Full source coverage and GL reconciliation need implementation and independent review.
4. Implement immutable tax facts/return snapshots and required controls (VAT-01/02); do not reinterpret expense-tax synthetic totals as a company return. Preserve amendments and exact artifact lineage separately from tax-account settlement (VAT-03/04).
5. Obtain user approval before adding/changing tests. Run independently specified browser/HTTP/real-database scenarios and retain repeatable artifacts. No financial behavior was run by this research.
6. If XML export is offered, verify actual ISO-8859-1 bytes, exact snapshot binding and schema/semantic constraints. Authority acceptance requires its own authorized portal/provider exercise; no credentials, accounts, uploads, signatures, submissions or payments were used here.

## Provenance and limits

Direct anonymous HTTPS retrieval of official Skatteverket and Riksdagen sources. Response hashes below are SHA-256 of `httpx` response content bytes after HTTP content decoding. For HTML excerpts, BeautifulSoup `get_text("\n", strip=True)` supplies a deterministic bounded textual view; excerpt hashes are SHA-256 of the exact UTF-8 text inside the following fenced blocks, excluding the code-fence newlines. Line breaks from HTML extraction are preserved. Form text is a labelled visual transcription, not OCR or an HTML quote.

Only the excerpts and hashes below are retained in this document. Complete response bodies were read transiently and **are not archived in the repository**. A future request can differ; a hash is not legal authentication, proof of current applicability or a complete source archive. No executable official schema, example code or fixture dataset is incorporated. Short attributed quotations support the research; redistribution rights for any later full schema/data bundle must be reviewed separately.

Search discovery limits: Serper is not configured; direct Google discovery returned a consent page. Skatteverket's public site search and direct official links were usable. No search snippets or third-party calculator results are used as rule authority. No inaccessible legal-guidance page was treated as verified.

## Retrieved sources

### `sff` — Riksdagen — Skatteförfarandeförordning (2011:1261)

- URL: https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/skatteforfarandeforordning-20111261_sfs-2011-1261/
- Retrieved: `2026-09-22T20:02:50.014286+00:00`; HTTP `200`.
- Response SHA-256: `97a5335c70cbbef73f0131d1b5ef4472b1738d4f11f69b94302d87128c668030`.
- Version/effective-date evidence: Consolidation label: SFS 2026:1570. Relevant clause: 22 kap. 1 §; no amendment marker is shown on that clause. Original transition: commencement 2012-01-01; first VAT application distinguishes ordinary periods beginning 2012-01-01 and annual periods beginning 2012-02-01. These are not this candidate profile's release dates.
- Page date metadata: none captured. Page dates are not legal commencement.

### `skv_returnfile` — Skatteverket — Lämna momsdeklaration via fil i e-tjänsten

- URL: https://www.skatteverket.se/foretag/moms/deklareramoms/lamnamomsdeklarationviafilietjansten.4.2fb39afe18dabf1e4d223cc.html
- Retrieved: `2026-09-22T20:02:13.543861+00:00`; HTTP `200`.
- Response SHA-256: `b6aaa21e7bc0a9c92fd24d395f1bdc5a71f4fa90763835dadf6b93b83f755b07`.
- Version/effective-date evidence: Wire version shown: eSKDUpload Version="6.0", XML 1.0, ISO-8859-1. No schema-release commencement date or downloadable XSD was found on this page.
- Page date metadata: {"DC.Date.Created": "2024-03-14", "DC.Date.Modified": "2026-07-20"}. Page dates are not legal commencement.

### `skv_boxes` — Skatteverket — Fylla i momsdeklarationen

- URL: https://www.skatteverket.se/foretag/moms/deklareramoms/fyllaimomsdeklarationen.4.3a2a542410ab40a421c80004214.html
- Retrieved: `2026-09-22T20:02:25.099253+00:00`; HTTP `200`.
- Response SHA-256: `f67e04141f72ee516ca689d0959f6b3a38759e6859fd505f328e1a00db907636`.
- Version/effective-date evidence: No numbered release or legal effective interval is stated on the inspected public page.
- Page date metadata: {"DC.Date.Created": "2006-05-11", "DC.Date.Modified": "2026-09-21"}. Page dates are not legal commencement.

### `skv_form` — Skatteverket — SKV 4700 paper-form illustration, linked from box guidance

- URL: https://www.skatteverket.se/images/18.e100f5918ab3d546d4974/1695816777554/skv-4700-sida-3.png
- Retrieved: `2026-09-22T20:04:16.306987+00:00`; HTTP `200`.
- Response SHA-256: `e33e8144fddb6d38ca11c35d482232da329318d3275c7df03c56a9e78cabf5c4`.
- Version/effective-date evidence: Illustration visibly reads SKV 4700 22 06 and prg 23-04. It says it is a copy and must not be used as the declaration. Its edition markings and image URL timestamp are not legal effective dates.
- Page date metadata: none captured. Page dates are not legal commencement.

### `sfs_taxprocedure` — Riksdagen — Skatteförfarandelag (2011:1244)

- URL: https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/skatteforfarandelag-20111244_sfs-2011-1244/
- Retrieved: `2026-09-22T20:02:26.448594+00:00`; HTTP `200`.
- Response SHA-256: `d6cfaf5a1f86c6592834ad6a63c4afb2902bf03b98721945bfa0a639cce68a01`.
- Version/effective-date evidence: Consolidation label: SFS 2026:1305. 26 kap. 21 § cites Lag (2023:208). No whole-document historical validity interval is established here.
- Page date metadata: none captured. Page dates are not legal commencement.

### `sfs_vat` — Riksdagen — Mervärdesskattelag (2023:200)

- URL: https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/mervardesskattelag-2023200_sfs-2023-200/
- Retrieved: `2026-09-22T20:02:25.633312+00:00`; HTTP `200`.
- Response SHA-256: `43765498e0091e85ccf585d8f4e2aa8a136576c5a3f3897bffa8e2183c174fe6`.
- Version/effective-date evidence: Consolidation label: SFS 2026:1025. 9 kap. 2 § displays both the pre-2028 clause under 2026:118 and the successor effective 2028-01-01 under 2026:119. Their transitions preserve older provisions for earlier taxable events. Do not use the consolidation label as transaction applicability.
- Page date metadata: none captured. Page dates are not legal commencement.

### `skv_when` — Skatteverket — När ska jag deklarera moms

- URL: https://www.skatteverket.se/foretag/moms/deklareramoms/narskajagdeklareramoms.4.6d02084411db6e252fe80008988.html
- Retrieved: `2026-09-22T20:02:24.931579+00:00`; HTTP `200`.
- Response SHA-256: `f1228f2aa148dd80adf67af4e80ceaaefcd7dcd0c876b102249cc1c1cd468332`.
- Version/effective-date evidence: No numbered release or legal effective interval is stated on the inspected public page.
- Page date metadata: {"DC.Date.Created": "2008-12-04", "DC.Date.Modified": "2026-07-20"}. Page dates are not legal commencement.

### `skv_input` — Skatteverket — Köpa varor eller tjänster till företaget

- URL: https://www.skatteverket.se/foretag/moms/kopavarorochtjanster/kopavarorellertjanstertillforetaget.4.7459477810df5bccdd480005156.html
- Retrieved: `2026-09-22T20:05:11.343969+00:00`; HTTP `200`.
- Response SHA-256: `5db443c68342a0fb8d6014aff46d40c881ff447bfa0bae9ea0b5bee0bfbf3e1d`.
- Version/effective-date evidence: No numbered release or legal effective interval is stated on the inspected public page.
- Page date metadata: {"DC.Date.Created": "2006-10-25", "DC.Date.Modified": "2026-07-20"}. Page dates are not legal commencement.

### `skv_corrections` — Skatteverket — Rätta en momsdeklaration

- URL: https://www.skatteverket.se/foretag/moms/deklareramoms/rattaenmomsdeklaration.4.3684199413c956649b552c4.html
- Retrieved: `2026-09-22T20:02:25.131316+00:00`; HTTP `200`.
- Response SHA-256: `79b389ce783f5586011de004d8955440f5e66270214e799e48048917adec003a`.
- Version/effective-date evidence: No numbered release or legal effective interval is stated on the inspected public page.
- Page date metadata: {"DC.Date.Created": "2013-02-05", "DC.Date.Modified": "2026-07-20"}. Page dates are not legal commencement.

### `skv_invoice` — Skatteverket — Momslagens regler om fakturering

- URL: https://www.skatteverket.se/foretag/moms/saljavarorochtjanster/momslagensregleromfakturering.4.58d555751259e4d66168000403.html
- Retrieved: `2026-09-22T20:05:11.411497+00:00`; HTTP `200`.
- Response SHA-256: `72925efc2f8c34824817df14e18082c3c2c030ba097c23b8f4fdb17a63cae91f`.
- Version/effective-date evidence: No numbered release or legal effective interval is stated on the inspected public page.
- Page date metadata: {"DC.Date.Created": "2009-12-30", "DC.Date.Modified": "2026-03-19"}. Page dates are not legal commencement.

## Exact relevant excerpts

### E01 — 22 kap. 1 §: discard öre

Source: `sff`. UTF-8 excerpt SHA-256: `f3f53d3f9c839fbf2a8e8c22e8be8852bd5ddab047d161374e558a3e81a9b2d8`.

```text
1 §
Belopp som avser skatt eller avgift enligt skatteförfarandelagen (2011:1244) ska anges i hela krontal så att öretal faller bort.
```

### E02 — Transition 2011:1261, commencement and first VAT application

Source: `sff`. UTF-8 excerpt SHA-256: `46ed05e135e066113b56ee4f4d643f8836fd856b02107d66557eb6e04c3d2ff3`.

```text
2011:1261
1. Denna förordning träder i kraft den 1 januari 2012.
Förordningen tillämpas första gången enligt följande uppställning:
När det gäller                  tillämpas förordningen första
gången på
a) F-skatt, särskild A-skatt
och slutlig skatt               skatt som avser beskattningsår
som börjar den 1 februari 2012
b) arbetsgivaravgifter          avgifter som avser
redovisningsperioden januari
2012
c) skatteavdrag                 skatt som ska dras av från
ersättningar som betalas ut
efter utgången av 2011
d) mervärdesskatt och punktskatt:
- för redovisningsperioder      skatt som avser
redovisningsperioder som
börjar den 1 januari 2012
eller, om redovisningsperioden
är ett beskattningsår, den
redovisningsperiod som börjar
den 1 februari 2012
- för förvärv och händelser som medför skattskyldighet och som inte ska hänföras
till redovisningsperioder       skatt som avser förvärv och
händelser som genomförs
respektive inträffar efter
utgången av 2011
```

### E03 — XML header, identifier and period encoding

Source: `skv_returnfile`. UTF-8 excerpt SHA-256: `4d1ec9564006a844fd42f9b550f3782e7db8fef037a5d8a4115a4c7466a46eaf`.

```text
Inledning (Header)
I filens inledning är alla uppgifter obligatoriska. Om någon av uppgifterna saknas eller om du anger dem på fel sätt kan du inte ladda upp filen.
Obligatoriska uppgifter
Radnummer
XML-tagg
Information
Rad 1
<?xml version="1.0" encoding="ISO-8859-1"?>
Måste finnas med.
Rad 2
<eSKDUpload Version="6.0">
Måste finnas med.
Rad 3
<OrgNr>556000-0175</OrgNr>
Den momsregistrerades person-, samordnings- organisations- eller representantnummer. Ange numret med 10 siffror enligt formatet xxxxxx-xxxx, med bindestreck. Organisationsnumret i exemplet är påhittat.
Rad 4
<Moms>
Måste finnas med.
Rad 5
<Period>202501</Period>
Redovisningsperiod. Använd följande format.
Månadsredovisning: År och månad, 202501 (januari 2025)
Kvartalsredovisning: År och den sista månaden i aktuellt kvartal, 202503 (första kvartalet 2025)
Helt beskattningsår: År och den sista månaden i beskattningsåret, 202512 (om beskattningsår motsvaras av ett kalenderår motsvarar exemplet januari–december 2025).
```

### E04 — Input VAT sign; total sign

Source: `skv_returnfile`. UTF-8 excerpt SHA-256: `15d4b2a44e0991f94c8107c4f9883353b0d9c4d2aecc9656baf19c6b0d002bc4`.

```text
Ingående moms
Radnummer
XML-tagg
Avser
Rad 33
<MomsIngAvdr>1000</MomsIngAvdr>
Ruta 48: Ingående moms att dra av.
När beloppet avser ingående moms att få tillbaka ska du inte ange något inledande tecken framför beloppet.
Om du däremot tagit emot en ändringsfaktura som innebär en kreditering av en tidigare utfärdad faktura ska du minska tidigare avdrag för ingående moms. Om en sådan minskning resulterar i att redovisningsperiodens sammanlagda ingående moms innebär att du har ingående moms att betala redovisar du det genom att ange ett minustecken (-) direkt innan beloppet, det vill säga utan mellanrum.
Summering
Radnummer
XML-tagg
Avser
Rad 34
<MomsBetala>225500</MomsBetala>
Ruta 49: Moms att betala eller få tillbaka
Ange moms att betala med endast belopp (utan inledande tecken).
Ange moms att få tillbaka genom att skriva ett minustecken (-) direkt innan beloppet (inget mellanslag mellan minustecken och belopp).
```

### E05 — Integer amounts

Source: `skv_returnfile`. UTF-8 excerpt SHA-256: `887a7e2261037c68266fa2e16bd4d4133c15ab1e4c62f62653c2c40215aa9fdd`.

```text
Beloppsuppgifter är angivna i fel format. Endast siffror (0–9) samt inledande plustecken (+) eller minustecken (-) tillåts. Belopp måste anges i heltal utan decimaler.
```

### E06 — Amendment replaces full same-period return

Source: `skv_returnfile`. UTF-8 excerpt SHA-256: `8e866b4784ac221ecc1e65c46e62feade131a2bb7d7056ed1e4c81ac16d70f66`.

```text
Rätta fel i en inlämnad momsdeklaration via filöverföring
Om du upptäcker att du har gjort fel i en redan inlämnad momsdeklaration kan du skapa en ny fil för den perioden och lämna in på samma sätt som beskrivits ovan. Du behöver göra om hela deklarationen, inte bara de uppgifter som har ändrats.
```

### E07 — Box 49 formula

Source: `skv_boxes`. UTF-8 excerpt SHA-256: `2d540e11283a88d31e3da8d38479c65c3abce8e5f7607fc43dfb7e75f319c5af`.

```text
Fält 49 – Moms att betala eller få tillbaka
Här redovisar du hur mycket moms du ska betala eller få tillbaka för perioden. Beloppet är summan av fälten 10, 11, 12, 30, 31, 32, 60, 61 och 62 minus beloppet i fält 48. Fält 49 ska du alltid fylla i.
Om du inte har någon moms att redovisa för perioden:
tryck på knappen Deklarera noll i e-tjänsten
skriv 0 i fält 49 om du deklarerar på pappersblankett.
```

### E08 — 26 kap. 21 §: return fields

Source: `sfs_taxprocedure`. UTF-8 excerpt SHA-256: `2113d2ef9976bddb82eb78da8ea21d980de486795bfd26fcdf5041e764760468`.

```text
En mervärdesskattedeklaration ska innehålla uppgift om
1. utgående skatt,
2. ingående skatt, och
3. leveranser, förvärv och överföringar av varor som  transporteras mellan EU-länder.
En mervärdesskattedeklaration som ska lämnas av en  grupphuvudman ska innehålla uppgifter för hela gruppen.
Lag (2023:208)
.
```

### E09 — 9 kap. 2 §: pre-2028 and future standard-rate clauses

Source: `sfs_vat`. UTF-8 excerpt SHA-256: `2cb7db5962c67bbde861564e53a478893678cbfd25da74d943e0992a9fcf73cf`.

```text
Normalskattesats - 25 procent
2 §
/Upphör att gälla U:2028-01-01/
Skatt enligt denna lag tas ut med 25 procent av  beskattningsunderlaget om inte annat följer av 4-19 §§.
Lag (2026:118)
.
2 §
/Träder i kraft I:2028-01-01/
Skatt enligt denna lag tas ut med 25 procent av  beskattningsunderlaget om inte annat följer av 3-18 §§.
Lag (2026:119)
.
```

### E10 — Accrual period basis and advances

Source: `skv_when`. UTF-8 excerpt SHA-256: `945a681fcfba3784094b6e0219875262e3d3159cb9c006f346712a8893a46064`.

```text
Faktureringsmetoden
Är du bokföringsskyldig och har en årsomsättning som överstiger 3 miljoner kronor ska du löpande bokföra dina affärshändelser i företaget. Då använder du faktureringsmetoden för din momsredovisning.
Rätt period för momsredovisningen
Du tar upp momsen i din momsdeklaration i den redovisningsperiod när försäljningen eller inköpet har bokförts eller skulle ha bokförts.
Huvudprincipen är att du ska bokföra och redovisa
- utgående moms i samband med att du ställer ut en faktura till köparen, vanligtvis på fakturadagen
- ingående moms när du tar emot inköpsfakturan från din leverantör, vanligtvis på ankomstdagen.
Redovisa förskott
Har du tagit emot eller lämnat förskott eller à conto (delbetalning i förskott) ska du redovisa den utgående momsen när du får betalt och den ingående momsen när du betalar. Du får inte dra av momsen förrän förskottsfakturan är betald.
```

### E11 — Declared XML ordering

Source: `skv_returnfile`. UTF-8 excerpt SHA-256: `775e260f269f6f0bf7b74f68e8dcf798eee2a71edef4ba899013f3f359996836`.

```text
De radnummer som står i tabellerna här nedanför visar vilken ordning XML-taggarna ska ha i den färdiga filen.
```

### E12 — Narrow profile tag mappings

Source: `skv_returnfile`. UTF-8 excerpt SHA-256: `87d4f9631fbecfc6dac252622821935969229facf7ad81129d3f0e0397cf0c80`.

```text
Rad 6
<ForsMomsEjAnnan>100000</ForsMomsEjAnnan>
Ruta 05: Momspliktig försäljning som inte ingår i ruta 06, 07 eller 08.
Rad 7
<UttagMoms>200000</UttagMoms>
Ruta 06: Momspliktiga uttag.
Rad 8
<UlagMargbesk>300000</UlagMargbesk>
Ruta 07: Beskattnings­-underlag vid vinstmarginal-beskattning.
Rad 9
<HyrinkomstFriv>400000</HyrinkomstFriv>
Ruta 08: Hyresinkomster vid frivillig beskattning.
Rad 10
<MomsUtgHog>200000</MomsUtgHog>
Ruta 10: Utgående moms 25 %.
```

### E13 — Upload, sign and receipt are separate

Source: `skv_returnfile`. UTF-8 excerpt SHA-256: `6fa8b3060be358e2bf84f35038503f1b6b8485b8bf367022735bd59e66e5b936`.

```text
När du laddat upp och granskat din fil, och den inte innehåller felaktigheter som hindrar inlämning, kan du signera och skicka in momsdeklarationen. Då får du en kvittens.
```

### E14 — Transitions 2026:118 and 2026:119

Source: `sfs_vat`. UTF-8 excerpt SHA-256: `6eba1957597c9f361f196057f7934b65d690fb22f4eac2f0b653c64dde26bcac`.

```text
2026:118
1. Denna lag träder i kraft den 1 april 2026.
2. Äldre föreskrifter gäller fortfarande för mervärdesskatt  som avser beskattningsbara transaktioner för vilka den  beskattningsgrundande händelsen inträffat före  ikraftträdandet.
2026:119
1. Denna lag träder i kraft den 1 januari 2028.
2. Äldre föreskrifter gäller fortfarande för mervärdesskatt  som avser beskattningsbara transaktioner för vilka den  beskattningsgrundande händelsen inträffat före  ikraftträdandet.
```

### E15 — Invoice evidence supports deduction

Source: `skv_input`. UTF-8 excerpt SHA-256: `2a98653109ac0002e81bfb87a0f7eb27195ea08a00b116b8641ea4d4cfe1e587`.

```text
Underlaget ska normalt vara en faktura eller kvitto där momsen är specificerad. Spara därför alltid faktura, kvitto eller liknande på de varor eller tjänster du köper i din bokföring.
För att du ska få göra avdrag för moms är det viktigt att fakturan innehåller de uppgifter som måste finnas med på en faktura. Det finns särskilda regler om totalbeloppet på fakturan eller kvittot inte är högre än 4 000 kronor inklusive moms.
```

### E16 — SKV 4700 illustration: global amount instruction (visual transcription)

Source: `skv_form`. UTF-8 excerpt SHA-256: `a4f8f4f559462cfc6d9acbb1f0c28a444d226344b52647084b6a732a98dcbd44`.

```text
Ange endast kronor, ej ören
```

### E17 — 13 kap. 6 §: taxable-use deduction condition

Source: `sfs_vat`. UTF-8 excerpt SHA-256: `e462fd2d80ffc9dc4968dc0bf288a8d3cffa8cfa90c5552275294dfdc5f39f31`.

```text
Avdragsrättens omfattning
Huvudregel
6 §
I den utsträckning en beskattningsbar person använder  varorna och tjänsterna för sina beskattade transaktioner inom  landet får denne, från den mervärdesskatt som ska betalas, dra  av ingående skatt som hänför sig till
1. leverans av varor eller tillhandahållande av tjänster till  den beskattningsbara personen,
2. sådana unionsinterna förvärv av varor som görs av den  beskattningsbara personen,
3. sådana överföringar som enligt 5 kap. 23-25 §§ likställs  med unionsinterna förvärv av varor mot ersättning och som görs  av den beskattningsbara personen, och
4. import av varor.
```
