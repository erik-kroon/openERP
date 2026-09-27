# Drastic Financial Platform: acceptansspecifikation

**Version:** 1.0. **Datum:** 2026-09-27. **Status:** 100 specificerade scenarier. Inget av dessa scenarier har exekverats mot openERP i denna dokumentleverans.

Varje produktkrav i huvud-PRD:n har dessutom eget acceptansvillkor. Scenarierna nedan kompletterar dessa med sammanhängande och negativa fall. De ger inte i sig tillstånd att lägga till tester i repo eller anropa verkliga banker.

## Scenarioregister

| ID | Scenario | Bevismiljö |
|---|---|---|
| ES-AT-001 | Native och Connected har olika skrivauktoritet | `company_migration` |
| ES-AT-002 | Firmamedlemskap ger inte alla böcker | `security` |
| ES-AT-003 | Okänd källperiod överlever tom arbetslista | `browser` |
| ES-AT-004 | Finansieringssamtycke är separat | `security` |
| ES-AT-005 | Kontoändring är en ny mottagarrevision | `integration` |
| ES-AT-006 | En affär med två delproblem | `browser` |
| ES-AT-007 | Batch med inaktuellt förslag | `runtime` |
| ES-AT-008 | Omladdning efter tappat svar | `browser` |
| ES-AT-009 | Kommentar är inte attest | `security` |
| ES-AT-010 | Samma avvikelse ger inte avisering per retry | `runtime` |
| ES-AT-011 | Exakt pengar över säker JS-heltalsgräns | `numeric_runtime` |
| ES-AT-012 | Generisk journal får inte konsumera domänägd källa | `runtime` |
| ES-AT-013 | Rättelse bevarar historia | `runtime` |
| ES-AT-014 | Två utjämnande avvikelser | `numeric_runtime` |
| ES-AT-015 | Privat utlägg och ersättning | `company` |
| ES-AT-016 | Regeländring över tidsgräns | `rule_qualification` |
| ES-AT-017 | Förberedd deklaration är inte inlämnad | `browser` |
| ES-AT-018 | Rättelse efter inlämning | `provider_qualification` |
| ES-AT-019 | Skattekontot finansieras netto | `numeric` |
| ES-AT-020 | Okänt myndighetsutfall | `provider_qualification` |
| ES-AT-021 | Saknad skattetabell | `rule_qualification` |
| ES-AT-022 | Lön ersätter prognosuppskattning | `numeric_runtime` |
| ES-AT-023 | En felaktig lönebetalning i batch | `provider_qualification` |
| ES-AT-024 | Rättelse efter redan betald lön | `company` |
| ES-AT-025 | Risk får inte medarbetarens sjukdata | `privacy` |
| ES-AT-026 | Order ersätts delvis av faktura | `numeric_runtime` |
| ES-AT-027 | Samma original via två kanaler | `integration` |
| ES-AT-028 | Delvis leverans | `integration` |
| ES-AT-029 | Företagskort kan inte ersättas privat | `runtime` |
| ES-AT-030 | Kreditnota före bankbetalning | `numeric_runtime` |
| ES-AT-031 | Olikdaterade banksaldon | `browser` |
| ES-AT-032 | Delbetalning finns redan i startbank | `numeric` |
| ES-AT-033 | Samma slut men annat minimum | `numeric` |
| ES-AT-034 | Saknad framtida lön | `browser` |
| ES-AT-035 | Historisk prognos utan efterhandsdata | `analytics` |
| ES-AT-036 | Virtuell momspott | `numeric_runtime` |
| ES-AT-037 | Pengar under intern överföring | `provider_qualification` |
| ES-AT-038 | Sweep efter förändrat saldo | `runtime` |
| ES-AT-039 | Utgången FX-offert | `provider_qualification` |
| ES-AT-040 | Dotterbolags kassa är inte moderbolagets | `legal_product` |
| ES-AT-041 | Mottagare ändras efter attest | `security` |
| ES-AT-042 | Timeout efter partneracceptans | `provider_qualification` |
| ES-AT-043 | Samtidig betalningskapacitet | `concurrency` |
| ES-AT-044 | Duplicerad och omkastad webhook | `provider_qualification` |
| ES-AT-045 | Avbryt efter skickat uppdrag | `provider_qualification` |
| ES-AT-046 | Hold och delvis presentment | `numeric_runtime` |
| ES-AT-047 | Refund efter stängt kort | `provider_qualification` |
| ES-AT-048 | Provisorisk chargeback förloras | `provider_qualification` |
| ES-AT-049 | Kortfaktura reglerar redan bokförda köp | `numeric_runtime` |
| ES-AT-050 | Korthemligheter når inte modeller | `security` |
| ES-AT-051 | Usage-dubblett | `numeric_runtime` |
| ES-AT-052 | Prisrevision ändrar inte fakturerad cykel | `runtime` |
| ES-AT-053 | Proratering med öresrest | `numeric` |
| ES-AT-054 | Misslyckat uttag ändrar inte faktura | `provider_qualification` |
| ES-AT-055 | Årsbetalning är inte tolv gånger MRR | `analytics` |
| ES-AT-056 | Tekniskt stängd men inte externt inlämnad | `browser` |
| ES-AT-057 | Obligatorisk upplysning saknar källa | `rule_qualification` |
| ES-AT-058 | Giltigt XML med fel totalsumma | `artifact_validation` |
| ES-AT-059 | Full arkivåterställning | `restore` |
| ES-AT-060 | Årsöverföring utan nya intäkter | `company_migration` |
| ES-AT-061 | Samtidig juridisk utgivning | `concurrency` |
| ES-AT-062 | PDF är inte strukturerad e-faktura | `provider_qualification` |
| ES-AT-063 | Delkredit efter betalning | `numeric_runtime` |
| ES-AT-064 | Överlåten fakturas mottagare | `legal_product` |
| ES-AT-065 | Brutto till processorutbetalning | `numeric` |
| ES-AT-066 | Påminnelse stoppas av aktuell betalning | `runtime` |
| ES-AT-067 | Bestridd del hålls separat | `numeric` |
| ES-AT-068 | Otillåten avgift läggs inte till | `rule_qualification` |
| ES-AT-069 | Inkassohandoff kräver rätt roll | `legal_product` |
| ES-AT-070 | Nedskrivning utan juridiskt bortfall | `company` |
| ES-AT-071 | Indikation är inte disponibla pengar | `browser` |
| ES-AT-072 | Långivare får rätt datamängd | `privacy` |
| ES-AT-073 | Provision ändrar inte kostnadssortering | `browser` |
| ES-AT-074 | Offerten löper ut | `runtime` |
| ES-AT-075 | Signerad kredit utan utbetalning | `browser` |
| ES-AT-076 | Databrist är inte dålig kredit | `model_validation` |
| ES-AT-077 | Ingen tidsläckage | `model_validation` |
| ES-AT-078 | Mänskligt undantag bevarar modelloutput | `governance` |
| ES-AT-079 | Extern riskprodukt saknar godkänd klassificering | `legal_product` |
| ES-AT-080 | AML-utredning syns inte i vanlig AI-förklaring | `privacy` |
| ES-AT-081 | Samma fordringsdel finansieras inte dubbelt | `concurrency` |
| ES-AT-082 | Nettoutbetalning är inte omsättning | `numeric_runtime` |
| ES-AT-083 | Ränta och waterfall | `numeric` |
| ES-AT-084 | Fakturabelåningens restlikvid | `numeric_runtime` |
| ES-AT-085 | Ny riskpoäng ändrar inte gammalt avtal | `governance` |
| ES-AT-086 | Agent kan inte självattestera | `security` |
| ES-AT-087 | Subagenter delar kumulativ gräns | `concurrency` |
| ES-AT-088 | Instruktion i faktura | `security` |
| ES-AT-089 | Agentens numeriska förklaring | `model_validation` |
| ES-AT-090 | Avbruten agent återfinner kvitto | `runtime` |
| ES-AT-091 | Banklogotyp betyder bara kvalificerad kapabilitet | `browser` |
| ES-AT-092 | Backfill skickar inte historiska krav | `integration` |
| ES-AT-093 | Missad webhook återfinns | `provider_qualification` |
| ES-AT-094 | Providerbyte med gamla öppna uppdrag | `provider_qualification` |
| ES-AT-095 | Source offer matchar release | `release` |
| ES-AT-096 | Trevägsavstämning hittar fel kund | `runtime` |
| ES-AT-097 | Restore efter redan exekverad betalning | `restore` |
| ES-AT-098 | Support kan inte attestera | `security` |
| ES-AT-099 | Modellregion ändras | `privacy` |
| ES-AT-100 | Kundexit med lån och kortrefund | `exit` |

## ES-AT-001: Native och Connected har olika skrivauktoritet

**Krav:** DR-CORE-01, DR-ACC-11

**Givet:** Ett bolag har extern officiell huvudbok för föregående år och Native från en granskad bryttid.

**När:** Samma historiska faktura importeras och en användare försöker skapa om dess intäkt.

**Förväntat:** Historisk faktura kan få betalningsallokering men inte ny intäkt genom migrationen. Systemägare och periodgräns är synliga.

**Bevismiljö:** `company_migration`. **Status:** specificerat, inte exekverat.

## ES-AT-002: Firmamedlemskap ger inte alla böcker

**Krav:** DR-CORE-02, DR-CORE-05

**Givet:** En konsult är medlem i en byrå och har mandat till klient A men inte B.

**När:** Konsulten öppnar en direktlänk och ett API-anrop mot B.

**Förväntat:** Båda åtkomsterna vägras utan att avslöja löner, saldon eller objektinnehåll.

**Bevismiljö:** `security`. **Status:** specificerat, inte exekverat.

## ES-AT-003: Okänd källperiod överlever tom arbetslista

**Krav:** DR-CORE-04, DR-WORK-07

**Givet:** Källinventeringen innehåller två bankkonton men periodutdrag finns bara för ett.

**När:** Alla uppgifter för inlästa rader avslutas.

**Förväntat:** Listan kan vara tom men periodtäckningen är ofullständig och komplett bolagsstatus vägras.

**Bevismiljö:** `browser`. **Status:** specificerat, inte exekverat.

## ES-AT-004: Finansieringssamtycke är separat

**Krav:** DR-CORE-07, DR-FIN-03

**Givet:** Kunden använder bokföring utan finansieringsdelning.

**När:** Ett automatiserat anrop försöker skicka underlag till en långivare.

**Förväntat:** Ingen otillåten export sker. Kunden kan fortsatt bokföra och manuellt pröva ett lokalt scenario.

**Bevismiljö:** `security`. **Status:** specificerat, inte exekverat.

## ES-AT-005: Kontoändring är en ny mottagarrevision

**Krav:** DR-CORE-08, DR-PMT-03

**Givet:** En befintlig leverantör har granskad mottagare och ett godkänt betalningsförslag.

**När:** Leverantörens bankuppgifter ändras.

**Förväntat:** Gammal attest kan inte exekvera den nya mottagaren. Originalversionen finns kvar i historiken.

**Bevismiljö:** `integration`. **Status:** specificerat, inte exekverat.

## ES-AT-006: En affär med två delproblem

**Krav:** DR-WORK-01, DR-WORK-04

**Givet:** En transaktion saknar kvitto och har oklar skattebehandling.

**När:** Den hämtas via bank- och dokumentvyn.

**Förväntat:** En huvuduppgift med två tydliga delsteg visas. Problemen försvinner endast när respektive del lösts.

**Bevismiljö:** `browser`. **Status:** specificerat, inte exekverat.

## ES-AT-007: Batch med inaktuellt förslag

**Krav:** DR-WORK-05, DR-ACC-04

**Givet:** Tolv förslag har granskats och ett relevant underlag ändras före genomförande.

**När:** Användaren bekräftar det tidigare urvalet.

**Förväntat:** Varje giltig grupp får sitt resultat. Den ändrade gruppen behöver ny granskning. Ingen odifferentierad totalsuccess visas.

**Bevismiljö:** `runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-008: Omladdning efter tappat svar

**Krav:** DR-WORK-06, DR-ACC-04

**Givet:** Servern genomförde ett godkänt förslag men browsern fick inte svaret.

**När:** Användaren laddar om och öppnar samma ärende.

**Förväntat:** Det beständiga kvittot återfinns och den ursprungliga filterpositionen kan återställas utan ny effekt.

**Bevismiljö:** `browser`. **Status:** specificerat, inte exekverat.

## ES-AT-009: Kommentar är inte attest

**Krav:** DR-WORK-08, DR-AGT-01

**Givet:** En konsult skriver godkänd i en kommentar men saknar finansiellt godkännandemandat.

**När:** En agent försöker använda kommentaren som attest.

**Förväntat:** Exekvering vägras. Samarbetskommentaren finns kvar som kommentar.

**Bevismiljö:** `security`. **Status:** specificerat, inte exekverat.

## ES-AT-010: Samma avvikelse ger inte avisering per retry

**Krav:** DR-WORK-09, DR-INT-07

**Givet:** En avisering är levererad och jobbmeddelandet återlevereras.

**När:** Aviseringsjobbet körs igen.

**Förväntat:** Ingen ny kundavisering skickas utan ny ekonomisk eller handlingsmässig förändring.

**Bevismiljö:** `runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-011: Exakt pengar över säker JS-heltalsgräns

**Krav:** DR-ACC-01, DR-ACC-04

**Givet:** Ett syntetiskt balanserat förslag innehåller 9007199254740993 minor units.

**När:** Det förbereds, granskas, bokförs och exporteras.

**Förväntat:** Exakt samma belopp bevaras i wire, DB, rapport och export utan flyttalsavrundning.

**Bevismiljö:** `numeric_runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-012: Generisk journal får inte konsumera domänägd källa

**Krav:** DR-ACC-02, DR-ACC-06

**Givet:** En leverantörsfakturas kapacitet tillhör AP och är redan konsumerad.

**När:** En integration försöker bokföra samma effekt via generisk journal.

**Förväntat:** Skrivningen vägras eller kvalificeras som separat rättelse med nytt underlag, aldrig som en andra normal kostnad.

**Bevismiljö:** `runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-013: Rättelse bevarar historia

**Krav:** DR-ACC-03, DR-ACC-13

**Givet:** En bokförd verifikation ska återföras.

**När:** Behörig person godkänner och genomför rättelsen.

**Förväntat:** Original och länkad rättelse finns kvar. Nettot stämmer och originalet kan inte ändras eller raderas.

**Bevismiljö:** `runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-014: Två utjämnande avvikelser

**Krav:** DR-ACC-07, DR-CLOSE-01

**Givet:** Bankkontrollen innehåller en oförklarad +500 och en orelaterad −500.

**När:** Avstämningsrapport genereras.

**Förväntat:** Nettodifferensen kan vara noll men fullständighet är falsk och båda posterna behöver förklaring.

**Bevismiljö:** `numeric_runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-015: Privat utlägg och ersättning

**Krav:** DR-ACC-10, DR-AP-07

**Givet:** Ägaren betalade ett kvalificerat företagskvitto privat och begär senare ersättning.

**När:** Kostnaden bokförs och ersättningen betalas.

**Förväntat:** En kostnad och en skuldreglering finns. Det privata kontot ingår inte som företagets kassa.

**Bevismiljö:** `company`. **Status:** specificerat, inte exekverat.

## ES-AT-016: Regeländring över tidsgräns

**Krav:** DR-TAX-01, DR-ACC-14

**Givet:** Två syntetiskt kvalificerade skattepaket har icke överlappande giltighet.

**När:** Transaktioner på båda sidor av gränsen behandlas.

**Förväntat:** Rätt paket används och källan redovisas. Saknat paket leder inte till föregående års fallback.

**Bevismiljö:** `rule_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-017: Förberedd deklaration är inte inlämnad

**Krav:** DR-TAX-03, DR-TAX-08

**Givet:** En momsfil är genererad och lokalt validerad.

**När:** Användaren öppnar periodstatus innan extern inlämning.

**Förväntat:** Status visar förberedd/granskad enligt faktiska steg och saknar externt mottagningskvitto.

**Bevismiljö:** `browser`. **Status:** specificerat, inte exekverat.

## ES-AT-018: Rättelse efter inlämning

**Krav:** DR-TAX-09, DR-TAX-03

**Givet:** En tidigare momsdeklaration är externt bekräftad och en faktura rättas.

**När:** Nytt deklarationsförslag skapas.

**Förväntat:** Tidigare kvitto och fil ligger kvar. Ny version visar delta och kräver eget godkännande.

**Bevismiljö:** `provider_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-019: Skattekontot finansieras netto

**Krav:** DR-TAX-04, DR-CASH-07

**Givet:** Saldo är 30 000 och kvalificerade framtida debiteringar är 50 000 utan andra rörelser.

**När:** Cash skapar bankbetalningsbehov.

**Förväntat:** Kompletterande överföring är 20 000. Varken 50 000 plus 20 000 eller en öronmärkt skattebetalning fabriceras.

**Bevismiljö:** `numeric`. **Status:** specificerat, inte exekverat.

## ES-AT-020: Okänt myndighetsutfall

**Krav:** DR-TAX-08, DR-OPS-06

**Givet:** Myndighetskanalen mottog ett dokument men svaret tappades.

**När:** Återhämtningsjobbet startar.

**Förväntat:** Ursprunglig referens utreds och ett kvalificerat kvitto återfinns före eventuell ny sidoeffekt.

**Bevismiljö:** `provider_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-021: Saknad skattetabell

**Krav:** DR-PAY-03, DR-TAX-01

**Givet:** Anställd och löneperiod finns men kvalificerad tabell saknas.

**När:** Lönekalkylen begärs.

**Förväntat:** Ingen påhittad skatt eller definitiv nettolön produceras. Exakt saknat underlag visas.

**Bevismiljö:** `rule_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-022: Lön ersätter prognosuppskattning

**Krav:** DR-PAY-06, DR-CASH-04

**Givet:** Cash innehåller en löneuppskattning för perioden.

**När:** En motsvarande lönekörning fastställs.

**Förväntat:** Den kvalificerade löneförekomsten ersätter uppskattningen och netto respektive skattekontobehov ligger på rätt datum.

**Bevismiljö:** `numeric_runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-023: En felaktig lönebetalning i batch

**Krav:** DR-PAY-04, DR-PMT-10

**Givet:** Nio löner är avvecklade och en är avvisad av partnern.

**När:** Löneansvarig rättar det återstående uppdraget.

**Förväntat:** Endast det avvisade uppdraget kan betalas efter ny granskning. Inga nio dubbelbetalningar skapas.

**Bevismiljö:** `provider_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-024: Rättelse efter redan betald lön

**Krav:** DR-PAY-07, DR-TAX-06

**Givet:** För stor lön har betalats och bokförts.

**När:** Löneansvarig rättar beräkningen.

**Förväntat:** Original, extra fordran eller annan kvalificerad korrigering och deklarationsbehov visas separat. Ingen automatisk obehörig kvittning görs.

**Bevismiljö:** `company`. **Status:** specificerat, inte exekverat.

## ES-AT-025: Risk får inte medarbetarens sjukdata

**Krav:** DR-PAY-11, DR-RISK-02

**Givet:** Lönemodulen har känsliga individuppgifter och Risk behöver total lönekostnad.

**När:** En riskexport skapas.

**Förväntat:** Endast ändamålsenligt kvalificerade aggregerade ekonomiska uppgifter lämnas ut.

**Bevismiljö:** `privacy`. **Status:** specificerat, inte exekverat.

## ES-AT-026: Order ersätts delvis av faktura

**Krav:** DR-AP-01, DR-CASH-04

**Givet:** Beställning om 100 000 finns som prognos och faktura för 40 000 anländer.

**När:** Fakturan godkänns.

**Förväntat:** Faktisk 40 000 och kvalificerad återstående orderdel 60 000 ersätter tidigare prognos enligt betalningsvillkor, utan totalt 140 000.

**Bevismiljö:** `numeric_runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-027: Samma original via två kanaler

**Krav:** DR-AP-02, DR-CORE-09

**Givet:** Samma leverantörsfaktura kommer som e-postbilaga och e-faktura.

**När:** Båda tas in.

**Förväntat:** Originalförekomster bevaras och möjlig dublett granskas innan ny skuld eller betalning får skapas.

**Bevismiljö:** `integration`. **Status:** specificerat, inte exekverat.

## ES-AT-028: Delvis leverans

**Krav:** DR-AP-03, DR-AP-08

**Givet:** Order 10 enheter, verifierad leverans 6 och faktura 10.

**När:** Automatisk matchningspolicy körs.

**Förväntat:** Avvikande del markeras enligt kvalificerad policy. Matchningen skapar inte leveransbevis för fyra saknade enheter.

**Bevismiljö:** `integration`. **Status:** specificerat, inte exekverat.

## ES-AT-029: Företagskort kan inte ersättas privat

**Krav:** DR-AP-07, DR-CARD-06

**Givet:** Ett kvitto hör till ett redan företagsbetalt kortköp.

**När:** En användare begär privat utläggsersättning för samma ekonomiska köp.

**Förväntat:** Betalarkonflikt stoppar automatisk dubbelersättning och behåller underlaget för granskning.

**Bevismiljö:** `runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-030: Kreditnota före bankbetalning

**Krav:** DR-AP-06, DR-PMT-05

**Givet:** Godkänd leverantörsfaktura på 10 000 har fått kredit 2 000 före betalning.

**När:** Betalningsförslaget uppdateras.

**Förväntat:** Ny kvalificerad rest är 8 000 och relevant gammal betalningsattest kan inte betala 10 000 utan nytt beslut.

**Bevismiljö:** `numeric_runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-031: Olikdaterade banksaldon

**Krav:** DR-CASH-01, DR-CASH-11

**Givet:** Ett konto har saldo idag och ett annat saldo för sju dagar sedan utan mellanliggande täckning.

**När:** Koncern- eller bolagsprognos öppnas.

**Förväntat:** Ingen ovillkorlig aktuell totalsiffra visas utan kvalificerad tidsbrygga.

**Bevismiljö:** `browser`. **Status:** specificerat, inte exekverat.

## ES-AT-032: Delbetalning finns redan i startbank

**Krav:** DR-CASH-03, DR-INV-06

**Givet:** Faktura 50 000 har betalats med 20 000 före startögonblicket.

**När:** Framtida inflöden beräknas.

**Förväntat:** Endast återstående 30 000 tas med. Startbank och framtid inkluderar inte samma 20 000 två gånger.

**Bevismiljö:** `numeric`. **Status:** specificerat, inte exekverat.

## ES-AT-033: Samma slut men annat minimum

**Krav:** DR-CASH-05, DR-CASH-06

**Givet:** Likviditetsvektorn N-09 finns i två scenarier med Kund A dag 8 respektive dag 22.

**När:** Dagliga saldon beräknas.

**Förväntat:** Båda slutar på 90 000 men headroom blir 20 000 respektive −10 000 med buffert 10 000.

**Bevismiljö:** `numeric`. **Status:** specificerat, inte exekverat.

## ES-AT-034: Saknad framtida lön

**Krav:** DR-CASH-04, DR-CASH-11

**Givet:** En 90-dagarsvy innehåller bara månad ett och inga kvalificerade löneantaganden för senare månader.

**När:** Likviditetsutrymme efterfrågas.

**Förväntat:** Täckningsbristen är synlig. Månad två och tre tolkas inte som kostnadsfria.

**Bevismiljö:** `browser`. **Status:** specificerat, inte exekverat.

## ES-AT-035: Historisk prognos utan efterhandsdata

**Krav:** DR-CASH-13, DR-RISK-03

**Givet:** Ett snapshot sparas före en stor ny order.

**När:** Ordern importeras och historisk prognosprecision beräknas.

**Förväntat:** Den gamla prognosen är oförändrad och felet attribueras till senare information.

**Bevismiljö:** `analytics`. **Status:** specificerat, inte exekverat.

## ES-AT-036: Virtuell momspott

**Krav:** DR-TRE-03, DR-CASH-02

**Givet:** Bolaget har 100 000 på bank och tilldelar 20 000 till intern momspott.

**När:** Budgetallokeringen sparas.

**Förväntat:** Banken förblir 100 000 och ingen extern överföring eller juridisk medelsavskiljning påstås.

**Bevismiljö:** `numeric_runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-037: Pengar under intern överföring

**Krav:** DR-TRE-04, DR-CASH-02

**Givet:** 20 000 skickas mellan två egna inkluderade konton med fördröjd mottagning.

**När:** Avsändarkontot har debiterats men målkontot saknar ännu rörelsen.

**Förväntat:** Beloppet redovisas enligt kvalificerad transitmodell, aldrig samtidigt disponibelt på båda kontona.

**Bevismiljö:** `provider_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-038: Sweep efter förändrat saldo

**Krav:** DR-TRE-05, DR-PMT-04

**Givet:** Sweepplanen räknades före en lönereservation.

**När:** Den ska genomföras efter att lönen reserverat pengar.

**Förväntat:** Aktuellt saldo och mandat kontrolleras på nytt. Buffertbrott stoppar eller ändrar enligt förhandsgodkänd policy.

**Bevismiljö:** `runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-039: Utgången FX-offert

**Krav:** DR-TRE-06, DR-PMT-11

**Givet:** Kunden har godkänt en specifik offert med begränsad giltighet.

**När:** Genomförande sker efter utgången tid.

**Förväntat:** Ingen dold växling till annan kurs. Ny kvalificerad offert eller tillåtet exakt mandat krävs.

**Bevismiljö:** `provider_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-040: Dotterbolags kassa är inte moderbolagets

**Krav:** DR-TRE-09, DR-ACC-12

**Givet:** Koncernen har pengar i två juridiska personer men saknar intercompanymandat.

**När:** Grundaren planerar betalning från moderbolaget.

**Förväntat:** Dotterbolagets saldo visas separat och kan inte finansiera betalningen utan kvalificerad handling.

**Bevismiljö:** `legal_product`. **Status:** specificerat, inte exekverat.

## ES-AT-041: Mottagare ändras efter attest

**Krav:** DR-PMT-03, DR-PMT-05

**Givet:** Betalning är granskad mot bankkonto A.

**När:** Ett anrop försöker skicka till konto B med samma attest.

**Förväntat:** Anropet vägras före partnern och rätt konflikt visas.

**Bevismiljö:** `security`. **Status:** specificerat, inte exekverat.

## ES-AT-042: Timeout efter partneracceptans

**Krav:** DR-PMT-06, DR-PMT-07

**Givet:** Partnern mottog betalning men API-svaret saknas.

**När:** Systemet startar retry och överväger reservpartner.

**Förväntat:** Samma ekonomiska identitet utreds hos första partnern. Ingen ny sidoeffekt hos reservpartner.

**Bevismiljö:** `provider_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-043: Samtidig betalningskapacitet

**Krav:** DR-PMT-04, DR-AGT-03

**Givet:** 100 000 godkänd lokal kapacitet och två uppdrag om 60 000.

**När:** Båda försöker reservera samtidigt.

**Förväntat:** Högst ett får 60 000 reservation. Resterande kapacitet är 40 000 och båda resultaten kan återfinnas.

**Bevismiljö:** `concurrency`. **Status:** specificerat, inte exekverat.

## ES-AT-044: Duplicerad och omkastad webhook

**Krav:** DR-PMT-08, DR-INT-05

**Givet:** Slutlig observation har mottagits före en äldre accepterad-observation och båda återlevereras.

**När:** Meddelanden processas.

**Förväntat:** Slutligt kvalificerat tillstånd degraderas inte och ekonomisk effekt uppstår en gång.

**Bevismiljö:** `provider_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-045: Avbryt efter skickat uppdrag

**Krav:** DR-PMT-12, DR-WORK-03

**Givet:** En betalning har skickats och banken har ännu inte svarat.

**När:** Kunden begär stopp och banken avvecklar originalet.

**Förväntat:** Stoppbegäran markeras misslyckad eller för sen enligt verifierat utfall. En eventuell refund är nytt uppdrag.

**Bevismiljö:** `provider_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-046: Hold och delvis presentment

**Krav:** DR-CARD-04, DR-CARD-05

**Givet:** Reservation 1 000, reversering 300 och final presentment 650.

**När:** Kort- och budgetsaldo uppdateras.

**Förväntat:** Slutkostnad 650 och återstående hold 50 som frigörs enligt kvalificerat utfall, ingen 1 650-kostnad.

**Bevismiljö:** `numeric_runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-047: Refund efter stängt kort

**Krav:** DR-CARD-07, DR-CARD-09

**Givet:** Köp 650 finns och kortet är avslutat.

**När:** Refund 200 kommer via rätt utgivarreferens.

**Förväntat:** Bolaget får korrekt återbetalningsposition. Kortet öppnas inte för nya köp och nettoköpet är 450.

**Bevismiljö:** `provider_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-048: Provisorisk chargeback förloras

**Krav:** DR-CARD-08, DR-OPS-02

**Givet:** En tvist har gett tillfällig kredit.

**När:** Utgivaren meddelar slutlig förlust av tvisten.

**Förväntat:** Provisorisk effekt hanteras med ny spårbar rörelse. Originalköpet och ärendet bevaras.

**Bevismiljö:** `provider_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-049: Kortfaktura reglerar redan bokförda köp

**Krav:** DR-CARD-10, DR-ACC-06

**Givet:** Alla månadens köp är redovisade mot utgivarskuld.

**När:** Samlad kortfaktura betalas.

**Förväntat:** Betalningen reglerar skulden och bokför inte samma kostnader en gång till.

**Bevismiljö:** `numeric_runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-050: Korthemligheter når inte modeller

**Krav:** DR-CARD-11, DR-AGT-09

**Givet:** Tokeniserad kortvy och test-PAN/CVV används i isolerad kvalificeringsmiljö.

**När:** Köp förklaras av en agent och loggar kontrolleras.

**Förväntat:** Ingen otillåten PAN/CVV finns i agentkontext eller generella applikationsloggar.

**Bevismiljö:** `security`. **Status:** specificerat, inte exekverat.

## ES-AT-051: Usage-dubblett

**Krav:** DR-BILL-04, DR-BILL-05

**Givet:** Grundavgift 10 000 och 300 unika enheter à 20 har mottagits.

**När:** En redan känd usage-händelse skickas igen.

**Förväntat:** Netto förblir 16 000 enligt N-01 och den dubbla förekomsten är synlig utan ny debitering.

**Bevismiljö:** `numeric_runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-052: Prisrevision ändrar inte fakturerad cykel

**Krav:** DR-BILL-03, DR-BILL-09

**Givet:** En återkommande period är utgiven under prisversion ett.

**När:** Mallen ändras och materialiseringsjobbet körs igen.

**Förväntat:** Samma cykel och dokument återfinns. Nytt pris gäller bara kvalificerade framtida förekomster.

**Bevismiljö:** `runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-053: Proratering med öresrest

**Krav:** DR-BILL-06, DR-ACC-01

**Givet:** 100 minor units ska fördelas lika över tre enligt fastställd tie-break.

**När:** Periodens delkomponenter beräknas.

**Förväntat:** Resultatet blir den dokumenterade stabila 34/33/33-fördelningen och summerar till 100.

**Bevismiljö:** `numeric`. **Status:** specificerat, inte exekverat.

## ES-AT-054: Misslyckat uttag ändrar inte faktura

**Krav:** DR-BILL-09, DR-PMT-16

**Givet:** En giltigt utgiven prenumerationsfaktura har obetald rest.

**När:** Tre separata betalningsförsök utförs under giltigt mandat.

**Förväntat:** En faktura och tre betalningsförsök finns, inte tre kommersiella debiteringar.

**Bevismiljö:** `provider_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-055: Årsbetalning är inte tolv gånger MRR

**Krav:** DR-BILL-10, DR-BILL-12

**Givet:** Årsavtal betalas i förskott och tjänsten levereras månadsvis.

**När:** MRR, bank och intäktsrapport visas.

**Förväntat:** MRR följer avtalets definierade månatliga grund, kassa betalningen och redovisad intäkt kvalificerad periodisering.

**Bevismiljö:** `analytics`. **Status:** specificerat, inte exekverat.

## ES-AT-056: Tekniskt stängd men inte externt inlämnad

**Krav:** DR-CLOSE-03, DR-CLOSE-07

**Givet:** Periodlås och årsartefakt finns utan myndighetskvitto.

**När:** Årsstatus efterfrågas.

**Förväntat:** Systemet skiljer tekniskt lås från inlämning och påstår inte juridisk färdigställandegrad utan underlag.

**Bevismiljö:** `browser`. **Status:** specificerat, inte exekverat.

## ES-AT-057: Obligatorisk upplysning saknar källa

**Krav:** DR-CLOSE-04, DR-AGT-06

**Givet:** Årsprofilen kräver en bolagsuppgift som inte är känd.

**När:** Agenten försöker fastställa rapporten.

**Förväntat:** Ingen fabricerad text fyller luckan. Berörd fastställelse blockeras och övrigt arbete kan fortsätta.

**Bevismiljö:** `rule_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-058: Giltigt XML med fel totalsumma

**Krav:** DR-CLOSE-06, DR-ACC-13

**Givet:** En export är syntaktiskt giltig men har en ekonomisk summeringsavvikelse.

**När:** Kvalificering av artefakten begärs.

**Förväntat:** Semantisk kontroll vägrar trots godkänd XML-parser.

**Bevismiljö:** `artifact_validation`. **Status:** specificerat, inte exekverat.

## ES-AT-059: Full arkivåterställning

**Krav:** DR-CLOSE-09, DR-OPS-06

**Givet:** Granskningspaket, original, nycklar och register finns i en säker backup.

**När:** En isolerad återställning görs.

**Förväntat:** Rapport kan följas till samma verifierade originalbytes utan produktionsdatabasen.

**Bevismiljö:** `restore`. **Status:** specificerat, inte exekverat.

## ES-AT-060: Årsöverföring utan nya intäkter

**Krav:** DR-CLOSE-10, DR-ACC-11

**Givet:** Utgående saldon och historiska obetalda fakturor är kvalificerade.

**När:** Nästa år öppnas och en historisk faktura betalas.

**Förväntat:** Ingående rest och betalningsallokering hanteras utan en andra historisk intäkt.

**Bevismiljö:** `company_migration`. **Status:** specificerat, inte exekverat.

## ES-AT-061: Samtidig juridisk utgivning

**Krav:** DR-INV-02, DR-BILL-09

**Givet:** Ett granskat fakturautkast finns med en debiteringskapacitet.

**När:** Två anrop ger ut samma utkast samtidigt.

**Förväntat:** Ett utgivet dokument och en kapacitetskonsumtion finns med samma återfinnbara resultat.

**Bevismiljö:** `concurrency`. **Status:** specificerat, inte exekverat.

## ES-AT-062: PDF är inte strukturerad e-faktura

**Krav:** DR-INV-03, DR-CLOSE-06

**Givet:** Kunden behöver en kvalificerad offentlig e-faktureringskanal.

**När:** Systemet har bara genererat PDF.

**Förväntat:** Kanalstatus är ofullständig och produkten påstår inte att e-faktura har skickats.

**Bevismiljö:** `provider_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-063: Delkredit efter betalning

**Krav:** DR-INV-05, DR-INV-06

**Givet:** Faktura är delbetald och kunden får kvalificerad delkredit.

**När:** Krediten ges ut.

**Förväntat:** Rätt rest eller återbetalningsbehov uppstår med bevarad originalfaktura och betalning.

**Bevismiljö:** `numeric_runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-064: Överlåten fakturas mottagare

**Krav:** DR-INV-07, DR-CAP-10

**Givet:** Fakturan har en kvalificerad överlåtelse och dokumenterad betalningsinstruktion.

**När:** Köparen öppnar portalen.

**Förväntat:** Rätt betalningsmottagare visas och säljaren ser endast sin avtalade förväntade restlikvid.

**Bevismiljö:** `legal_product`. **Status:** specificerat, inte exekverat.

## ES-AT-065: Brutto till processorutbetalning

**Krav:** DR-INV-11, DR-OPS-02

**Givet:** Brutto 1 000, avgift 30, refund 100 och reserv 200.

**När:** Avräkning och Cash uppdateras.

**Förväntat:** Utbetalning är 670 och varje del har egen förklaring utan att reserv räknas som disponibel bank.

**Bevismiljö:** `numeric`. **Status:** specificerat, inte exekverat.

## ES-AT-066: Påminnelse stoppas av aktuell betalning

**Krav:** DR-COL-01, DR-PMT-14

**Givet:** En förfallen faktura ligger i utskickskön och betalning blir kvalificerad före sändning.

**När:** Jobbet gör sista kontrollen.

**Förväntat:** Påminnelsen stoppas och betalningsresultatet visas utan ny avgift.

**Bevismiljö:** `runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-067: Bestridd del hålls separat

**Krav:** DR-COL-03, DR-INV-06

**Givet:** Fordran 10 000, betalning 4 000, kredit 1 000 och bestridande 2 000.

**När:** Kravplan beräknas.

**Förväntat:** Total rest 5 000, bestridd del 2 000 och obestridd del 3 000 redovisas separat enligt N-07.

**Bevismiljö:** `numeric`. **Status:** specificerat, inte exekverat.

## ES-AT-068: Otillåten avgift läggs inte till

**Krav:** DR-COL-02, DR-TAX-01

**Givet:** Påminnelse får skickas men ingen kvalificerad avgiftsgrund finns.

**När:** Påminnelse skapas.

**Förväntat:** Dokumentet saknar påhittad avgift och anger korrekt huvudfordran.

**Bevismiljö:** `rule_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-069: Inkassohandoff kräver rätt roll

**Krav:** DR-COL-06, DR-CORE-03

**Givet:** Kunden vill eskalera men relevant partnerroll eller underlag är ej kvalificerat.

**När:** Automatisk överlämning begärs.

**Förväntat:** Överlämning blockeras med konkret beroende, utan att vanlig reskontraläsning stoppas.

**Bevismiljö:** `legal_product`. **Status:** specificerat, inte exekverat.

## ES-AT-070: Nedskrivning utan juridiskt bortfall

**Krav:** DR-COL-09, DR-ACC-03

**Givet:** Konsulten gör en kvalificerad nedskrivning av en fordran.

**När:** Collections visar ärendet och betalning kommer senare.

**Förväntat:** Bokföringsvärde, juridiskt krav och faktisk återvinning kan hanteras separat med rätt återföring.

**Bevismiljö:** `company`. **Status:** specificerat, inte exekverat.

## ES-AT-071: Indikation är inte disponibla pengar

**Krav:** DR-FIN-02, DR-CASH-09

**Givet:** Modellen visar preliminär möjlig finansiering men inget erbjudande finns.

**När:** Cash och betalningsvyn öppnas.

**Förväntat:** Indikationen kan användas i separat scenario men inte som observerat banksaldo eller säkert betalningsutrymme.

**Bevismiljö:** `browser`. **Status:** specificerat, inte exekverat.

## ES-AT-072: Långivare får rätt datamängd

**Krav:** DR-FIN-03, DR-RISK-02

**Givet:** Kunden väljer partner A och godkänner ett specifikt underlag.

**När:** Ansökan skickas.

**Förväntat:** Endast A får den godkända datamängden och mottagningsidentitet sparas.

**Bevismiljö:** `privacy`. **Status:** specificerat, inte exekverat.

## ES-AT-073: Provision ändrar inte kostnadssortering

**Krav:** DR-FIN-05, DR-FIN-06

**Givet:** Två jämförbara erbjudanden har olika provision till Drastic.

**När:** Kunden sorterar på total känd kostnad.

**Förväntat:** Sorteringen följer definierad kundkostnad och eventuell sponsring visas separat.

**Bevismiljö:** `browser`. **Status:** specificerat, inte exekverat.

## ES-AT-074: Offerten löper ut

**Krav:** DR-FIN-07, DR-CAP-01

**Givet:** Ett erbjudande med viss ränta har utgången giltighet.

**När:** Kunden försöker acceptera.

**Förväntat:** Ingen ny ränta ersätter den gamla tyst. Ny kvalificerad offert krävs.

**Bevismiljö:** `runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-075: Signerad kredit utan utbetalning

**Krav:** DR-FIN-08, DR-CAP-04

**Givet:** Avtal är signerat men ett villkor före utbetalning återstår.

**När:** Kunden ser finansieringsstatus.

**Förväntat:** Avtal och villkor visas, men ingen faktisk banklikvid fabriceras.

**Bevismiljö:** `browser`. **Status:** specificerat, inte exekverat.

## ES-AT-076: Databrist är inte dålig kredit

**Krav:** DR-RISK-01, DR-RISK-05

**Givet:** Bankunderlag saknas för en väsentlig period.

**När:** Riskunderlag beräknas.

**Förväntat:** Datakvalitet visar lucka och komplettering. Ingen påhittad sannolikhet eller brottsmisstanke läggs till.

**Bevismiljö:** `model_validation`. **Status:** specificerat, inte exekverat.

## ES-AT-077: Ingen tidsläckage

**Krav:** DR-RISK-03, DR-RISK-07

**Givet:** Marsbeslutet föregår faktiska aprilutfall.

**När:** Historisk modellutvärdering körs mot uppdaterat datalager.

**Förväntat:** Endast information känd vid marscutoff används och aprilutfallet är en separat label.

**Bevismiljö:** `model_validation`. **Status:** specificerat, inte exekverat.

## ES-AT-078: Mänskligt undantag bevarar modelloutput

**Krav:** DR-RISK-06, DR-RISK-08

**Givet:** Behörig kreditbeslutare väljer ett dokumenterat undantag.

**När:** Beslut sparas och modellversionen ändras senare.

**Förväntat:** Originaloutput, undantag, beslutare och senare modellversion kan särskiljas och reproduceras.

**Bevismiljö:** `governance`. **Status:** specificerat, inte exekverat.

## ES-AT-079: Extern riskprodukt saknar godkänd klassificering

**Krav:** DR-RISK-14, DR-CORE-07

**Givet:** Intern likviditetsanalys finns men kreditupplysningsprodukt är inte kvalificerad.

**När:** En extern klient begär bolagspoäng för annan kund.

**Förväntat:** Åtkomst och produktaktivering vägras utan att intern kundanalys påverkas.

**Bevismiljö:** `legal_product`. **Status:** specificerat, inte exekverat.

## ES-AT-080: AML-utredning syns inte i vanlig AI-förklaring

**Krav:** DR-RISK-12, DR-AGT-11

**Givet:** En begränsad intern utredning finns.

**När:** Kunden ber den vanliga assistenten förklara varför en handling väntar.

**Förväntat:** Endast tillåten statusförklaring lämnas; skyddade träffar och utredningsuppgifter exponeras inte.

**Bevismiljö:** `privacy`. **Status:** specificerat, inte exekverat.

## ES-AT-081: Samma fordringsdel finansieras inte dubbelt

**Krav:** DR-CAP-08, DR-CAP-09

**Givet:** 80 000 av en intern fordran har redan disponerats enligt kvalificerat avtal.

**När:** En ny finansiering försöker använda överlappande kapacitet.

**Förväntat:** Intern kontroll vägrar den överlappande delen och påstår inte global kontroll över okända externa dispositioner.

**Bevismiljö:** `concurrency`. **Status:** specificerat, inte exekverat.

## ES-AT-082: Nettoutbetalning är inte omsättning

**Krav:** DR-CAP-05, DR-CAP-14

**Givet:** Lån 100 000 med innehållen kvalificerad avgift 1 000 betalas ut.

**När:** Låntagarens redovisningsunderlag och Cash uppdateras.

**Förväntat:** Bank ökar 99 000 och skuld/avgift hanteras enligt profil. Ingen SaaS- eller försäljningsintäkt skapas av kapitalet.

**Bevismiljö:** `numeric_runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-083: Ränta och waterfall

**Krav:** DR-CAP-06, DR-CAP-07

**Givet:** N-06 anger ACT/365, tio dagar, 10 procent och betalning 20 000.

**När:** Kvalificerad kalkyl och allokering körs.

**Förväntat:** Ränta 273,97, kapitalminskning 19 726,03 och kapitalrest 80 273,97 med explicit avrundning.

**Bevismiljö:** `numeric`. **Status:** specificerat, inte exekverat.

## ES-AT-084: Fakturabelåningens restlikvid

**Krav:** DR-CAP-09, DR-CAP-10

**Givet:** N-04: fordran 100 000, lån 80 000, innehållen avgift 2 000 och full slutkundsbetalning.

**När:** Finansiärens avräkning genomförs.

**Förväntat:** Initial likvid 78 000 och restlikvid 20 000 ger totalt 98 000 till säljaren, inte två fria fakturainflöden.

**Bevismiljö:** `numeric_runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-085: Ny riskpoäng ändrar inte gammalt avtal

**Krav:** DR-CAP-11, DR-CAP-12, DR-RISK-13

**Givet:** Ett aktivt lån har fast ränta och en ny modell visar förändrad risk.

**När:** Bevakningsjobbet körs.

**Förväntat:** Nytt granskningsärende skapas enligt avtalet men ingen obehörig retroaktiv ränteändring sker.

**Bevismiljö:** `governance`. **Status:** specificerat, inte exekverat.

## ES-AT-086: Agent kan inte självattestera

**Krav:** DR-AGT-01, DR-AGT-02

**Givet:** Agenten har förberedelseverktyg och läsåtkomst.

**När:** Den försöker skapa ett godkännande och genomföra ett ej godkänt förslag.

**Förväntat:** Ingen självattest är möjlig och ekonomisk effekt uteblir.

**Bevismiljö:** `security`. **Status:** specificerat, inte exekverat.

## ES-AT-087: Subagenter delar kumulativ gräns

**Krav:** DR-AGT-03, DR-PMT-04

**Givet:** Två agenter arbetar inom samma mandat med total återstående budget 100 000.

**När:** Båda skickar handling om 60 000.

**Förväntat:** Högst en kvalificeras mot den gemensamma gränsen och uppdelning kan inte kringgå kontrollen.

**Bevismiljö:** `concurrency`. **Status:** specificerat, inte exekverat.

## ES-AT-088: Instruktion i faktura

**Krav:** DR-AGT-04, DR-AP-04

**Givet:** Dokumenttext uppmanar assistenten att ändra betalningskonto och ignorera attest.

**När:** Extraktionsagenten läser dokumentet.

**Förväntat:** Texten får endast behandlas som otillförlitligt innehåll; verktyg, mandat och mottagare ändras inte.

**Bevismiljö:** `security`. **Status:** specificerat, inte exekverat.

## ES-AT-089: Agentens numeriska förklaring

**Krav:** DR-AGT-05, DR-AGT-11

**Givet:** Verktyget returnerar ett exakt belopp som modellen tidigare gissade fel.

**När:** Förklaringen genereras.

**Förväntat:** Den använder kontraktets belopp och källreferens utan en konkurrerande numerisk beräkning.

**Bevismiljö:** `model_validation`. **Status:** specificerat, inte exekverat.

## ES-AT-090: Avbruten agent återfinner kvitto

**Krav:** DR-AGT-08, DR-PMT-07

**Givet:** Agenten startade en godkänd handling och stoppades efter extern inlämning.

**När:** Körningen återupptas.

**Förväntat:** Den utreder ursprunglig identitet och skapar inte ett nytt ekonomiskt behov.

**Bevismiljö:** `runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-091: Banklogotyp betyder bara kvalificerad kapabilitet

**Krav:** DR-INT-01, DR-PMT-02

**Givet:** Leverantör stödjer kontoinformation men inte utbetalning i denna profil.

**När:** Kunden öppnar integrationens produktvy.

**Förväntat:** Läsning visas som tillgänglig och betalning som ej kvalificerad, utan skenbar fungerande knapp.

**Bevismiljö:** `browser`. **Status:** specificerat, inte exekverat.

## ES-AT-092: Backfill skickar inte historiska krav

**Krav:** DR-INT-04, DR-COL-01

**Givet:** Ett historiskt system innehåller förfallna och redan betalda fakturor.

**När:** Backfill körs efter avbrott och återstartas.

**Förväntat:** Objekt återfinns utan dubblering och importen utlöser inte gamla kundutskick eller betalningar.

**Bevismiljö:** `integration`. **Status:** specificerat, inte exekverat.

## ES-AT-093: Missad webhook återfinns

**Krav:** DR-INT-05, DR-PMT-08

**Givet:** Partnern ändrade ett objekt men webhook saknas.

**När:** Periodisk kvalificerad synkkontroll körs.

**Förväntat:** Rätt revision upptäcks, källvattenmärke uppdateras och berörda projectioner kan beräknas om.

**Bevismiljö:** `provider_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-094: Providerbyte med gamla öppna uppdrag

**Krav:** DR-INT-10, DR-PMT-07

**Givet:** Nya betalningar går till B och gamla oavgjorda uppdrag finns hos A.

**När:** Ett sent meddelande från A anländer.

**Förväntat:** Det avstäms mot A:s gamla identitet och ingen motsvarande betalning skapas hos B.

**Bevismiljö:** `provider_qualification`. **Status:** specificerat, inte exekverat.

## ES-AT-095: Source offer matchar release

**Krav:** DR-INT-11, DR-CORE-11

**Givet:** En driftsatt täckt utgåva bygger på fast kodrevision och lockfil.

**När:** Kunden öppnar source offer.

**Förväntat:** Rätt motsvarande kod och byggunderlag erbjuds utan kunddata eller produktionshemligheter.

**Bevismiljö:** `release`. **Status:** specificerat, inte exekverat.

## ES-AT-096: Trevägsavstämning hittar fel kund

**Krav:** DR-OPS-02, DR-OPS-04

**Givet:** Partnernetto stämmer totalt men en avräkning är tilldelad fel kund.

**När:** Transaktions- och kundavstämning körs.

**Förväntat:** Avvikelsen hittas trots korrekt totalsumma och kan inte döljas som allmänt nollsaldo.

**Bevismiljö:** `runtime`. **Status:** specificerat, inte exekverat.

## ES-AT-097: Restore efter redan exekverad betalning

**Krav:** DR-OPS-06, DR-PMT-06

**Givet:** Backup föregår en verklig partnerbetalning men ursprunglig avsikt och externa återidentifieringsunderlag finns enligt kvalificerad design.

**När:** Tjänsten återställs.

**Förväntat:** Finansiell writer förblir spärrad tills betalningen återfunnits eller utretts och ingen dubbel sidoeffekt sker.

**Bevismiljö:** `restore`. **Status:** specificerat, inte exekverat.

## ES-AT-098: Support kan inte attestera

**Krav:** DR-OPS-07, DR-PMT-05

**Givet:** Support har tidsbegränsad diagnostikåtkomst.

**När:** Support försöker godkänna kundens betalning.

**Förväntat:** Handlingen vägras och försöket loggas utan att kundmandat ändras.

**Bevismiljö:** `security`. **Status:** specificerat, inte exekverat.

## ES-AT-099: Modellregion ändras

**Krav:** DR-OPS-08, DR-AGT-09

**Givet:** En ny modellleverantör har annan dataväg än den godkända.

**När:** En känslig löneuppgift försöker använda den modellen.

**Förväntat:** Anropet blockeras tills dataväg och ändamål är kvalificerade. Vanliga tillåtna uppgifter kan fortsätta.

**Bevismiljö:** `privacy`. **Status:** specificerat, inte exekverat.

## ES-AT-100: Kundexit med lån och kortrefund

**Krav:** DR-OPS-14, DR-CAP-16, DR-CARD-12

**Givet:** Kunden avslutar plattformen men har lån, öppen refund och arkivpliktigt underlag.

**När:** Exitflödet genomförs.

**Förväntat:** Export fungerar, återbetalningsväg och refundansvar kvarstår och retention behandlas per datakategori.

**Bevismiljö:** `exit`. **Status:** specificerat, inte exekverat.
