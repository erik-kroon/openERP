# Drastic Financial Platform: PRD-paket v1.0

**Datum:** 27 september 2026. **Status:** produktmålbild, inte implementation.

## Börja här

Läs [huvud-PRD:n](PRD_Drastic_Financial_Platform_End_State_v1.md). Den omfattar 28,383 ord, 40 kapitel och 243 produktkrav över 20 områden. [Acceptansbilagan](ACCEPTANCE.md) har 100 detaljerade scenarier. Varje krav har dessutom ett eget acceptansvillkor i huvudtexten.

Produktkartan omfattar Accounting, Money, Revenue, Drastic Risk och Capital. Tillkommande stöd omfattar inköp, gemensamt arbete, agenter, integrationer och finansoperationer. Partnerbaserad drift kan vara den fullständiga målbilden. Eget finansiellt risktagande är ett separat valfritt spår.

## Filer

| Fil | Innehåll |
|---|---|
| `PRD_Drastic_Financial_Platform_End_State_v1.md` | Fullständig produktmålbild med krav, resor, dataägarskap, regleringsgränser, affärsmodell och leverans. |
| `ACCEPTANCE.md` | 100 scenarier med givet, när, förväntat och kravreferenser. |
| `requirements.json` | Samma 243 krav i maskinläsbar form med gräns och acceptans. |
| `acceptance.json` | Samma 100 acceptansscenarier i maskinläsbar form. |
| `traceability.json` | Relation mellan kravens egna acceptansvillkor och kompletterande scenarier. |
| `modules.json` | De 20 produktområdena och föreslagen första leveransnivå. |
| `sources.json` | Primärkällor, repoanknytning och originalfilens hash. |
| `numerical_examples.json` | Elva syntetiska räkneexempel och utförd dokumentaritmetik. |
| `document_validation.json` | Kontroller av dokumentstruktur, referenser, antal och exempel. |
| `manifest.json` | SHA-256 för paketerade underlag. |
| `PRD_openERP_Book_Zero_Workflow_Drastic_Cash_v1.md` | Föregående Book Zero-PRD, bevarad byteidentisk. |

## För en implementerande agent

Läs först repo:ts aktuella instruktioner och verkliga ägare. Den selektivt granskade revisionen var `09fdb19837bb1535b1b4c060e68a0b237858b0a5`. Inspektera senare ändringar innan ett gammalt frånvaropåstående används. Mappa nya krav till befintliga Book Zero-, P-, NEXT- och PRY-ägare. Skapa inte en konkurrerande huvudbok eller en andra plan bara för att denna PRD använder andra produktnamn.

Följ befintlig auktorisation för kod, teständringar, deploy och externa handlingar. Denna dokumentleverans ändrar inga sådana rättigheter. Krav och scenarier har status specificerade och ej verifierade. Giltig juridisk produktroll, partneravtal och faktisk bolagsverifiering måste fortfarande etableras.

## Vad som faktiskt gjorts

Föregående Markdown har lästs och bevarats. Selektiv repo- och primärkällsgranskning har använts för målbilden. Dokumentstruktur, interna kravreferenser och syntetisk aritmetik har kontrollerats. Inga applikationstester, bankbetalningar, kreditbeslut, myndighetsinlämningar eller ändringar i GitHub utfördes för denna leverans.
