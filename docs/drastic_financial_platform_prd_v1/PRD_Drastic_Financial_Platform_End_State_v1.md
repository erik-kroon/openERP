# PRD: Drastic Financial Platform
## Optimal målbild för Accounting, Money, Revenue, Risk och Capital

| Dokumentfält | Värde |
|---|---|
| Version | 1.0 |
| Datum | 2026-09-27 |
| Status | Extremt detaljerad produktmålbild och föreslagen leveransstrategi. Inte en implementationsrapport eller ett tillståndsbesked. |
| Produktägare | Drastic |
| Första marknad | Svenska aktiebolag och deras redovisningspartners. Därefter kvalificerade nordiska och europeiska profiler. |
| Teknisk utgångspunkt | `erik-kroon/openERP` |
| Selektivt kontrollerad revision | `09fdb19837bb1535b1b4c060e68a0b237858b0a5` |
| Föregående PRD | `PRD_openERP_Book_Zero_Workflow_Drastic_Cash_v1.md`, bevarad oförändrad i paketet |
| Föreslagen placering | `docs/product/drastic-financial-platform-end-state-prd.md` |
| Kapitalpremiss | Första externa finansieringen ska finansiera produkt, verifiering, distribution och organisation. Den ska inte förutsätta en egen kreditbok. |

> **Produktlöfte:** Drastic hjälper företaget att förstå sin ekonomi, avsluta arbetet och genomföra godkända finansiella handlingar. Bokföring, pengar och affärsåtaganden hålls ihop utan att deras betydelser blandas ihop. Varje beslut och varje ekonomiskt utfall kan förklaras.

**Målbilden är ett ekonomiskt operativsystem för företag, inte en samling oberoende appar och inte ett krav på att Drastic ska bli bank.** Kunden ska kunna välja Drastic som ekonomisystem eller ansluta sin befintliga redovisning och använda kvalificerade delar av plattformen. Finansiella tjänster kan långsiktigt tillhandahållas av partners. Egen reglerad verksamhet är ett separat investeringsbeslut när kontroll, kundvärde och nettobidrag motiverar det.

### Hur dokumentet ska läsas

Produktbeslut och numeriska mål är föreslagna krav. Externa regler och observerade repoegenskaper har källhänvisningar. Alla pengar i räkneexemplen är syntetiska. De är inte Drastics verkliga saldon, kreditvillkor eller skattesatser.

`SKA` gäller inom en aktiverad produktprofil. `VILLKORAT SKA` blir obligatoriskt när land, bolag, avtal eller vald roll gör området tillämpligt. Ett område får inte få status ”ej tillämpligt” bara för att implementationen saknas. `VALFRITT STRATEGISKT SPÅR` betyder att även den optimala partnerbaserade plattformen kan vara komplett utan att Drastic aktiverar spåret.

Krav-ID:n `DR-*`, acceptansfall `ES-AT-*` och leveransnivåer `ES-*` tillhör denna PRD. De ersätter inte Book Zeros krav, repo:ts P0–P8, D-01–D-10 eller existerande NEXT-/PRY-ägare. En implementation ska mappas till befintlig ägare innan ett nytt paket skapas.

### Innehåll och läsvägar

Börja med kapitel 1–5 för produktens mål och gränser. Kapitel 6–25 innehåller de 243 produktkraven. Kapitel 26–30 beskriver tillstånd, kontrakt, kompletta resor och UX. Kapitel 31–38 behandlar reglering, partners, affärsmodell, leverans och kvalitetsmål. Kapitel 39–40 anger bevisplan och källor.

Fullständiga scenarier finns i [ACCEPTANCE.md](ACCEPTANCE.md). Maskinläsbara krav, scenarier och källor ligger i JSON-filerna.

1. [Produktstrategi och målbild](#chapter-1)
2. [Förhållande till Book Zero och observerat nuläge](#chapter-2)
3. [Hur den färdiga produkten upplevs](#chapter-3)
4. [Produktkonstitution](#chapter-4)
5. [Ekonomisk modell och ansvar](#chapter-5)
6. [Plattform, bolag och etablering](#chapter-6)
7. [Dagligt arbete och beslutsupplevelse](#chapter-7)
8. [Accounting: openERP och redovisningskärnan](#chapter-8)
9. [Accounting: Tax och skyldigheter](#chapter-9)
10. [Accounting: Payroll](#chapter-10)
11. [Inköp, leverantörsskulder och utlägg](#chapter-11)
12. [Money: Drastic Cash](#chapter-12)
13. [Money: Treasury](#chapter-13)
14. [Money: Payments](#chapter-14)
15. [Money: Cards och kortutgifter](#chapter-15)
16. [Revenue: Billing och kommersiella avtal](#chapter-16)
17. [Accounting: Close, rapportering och årsarbete](#chapter-17)
18. [Revenue: Invoicing och kundreskontra](#chapter-18)
19. [Revenue: Collections och kravhantering](#chapter-19)
20. [Revenue: Financing och kundens finansieringsresa](#chapter-20)
21. [Drastic Risk: beslutsunderlag och riskstyrning](#chapter-21)
22. [Capital products och kreditförvaltning](#chapter-22)
23. [Agentoperativsystem och mänsklig kontroll](#chapter-23)
24. [Integrationer, API och ekosystem](#chapter-24)
25. [Finansoperationer, drift och förtroende](#chapter-25)
26. [Ekonomiska tillstånd, kommandon och invariants](#chapter-26)
27. [Informationsmodell och föreslagna kontrakt](#chapter-27)
28. [Kompletta tvärgående kundresor](#chapter-28)
29. [Systemarkitektur och utvecklingsgränser](#chapter-29)
30. [UX-kontrakt och informationshierarki](#chapter-30)
31. [Regulatorisk produktkarta och aktiveringsgränser](#chapter-31)
32. [Partnerstrategi och upphandlingskrav](#chapter-32)
33. [Affärsmodell, produktpaket och kapitaldisciplin](#chapter-33)
34. [Leveransnivåer och releasebeslut](#chapter-34)
35. [Kvalitetsmål, kapacitetsbudget och mätning](#chapter-35)
36. [Numeriska referensfall](#chapter-36)
37. [Riskregister och medvetna avvägningar](#chapter-37)
38. [Öppna beslut och nödvändiga externa underlag](#chapter-38)
39. [Acceptansplan och bevispaket](#chapter-39)
40. [Källor, avgränsningar och dokumentstatus](#chapter-40)

<a id="chapter-1"></a>

## 1. Produktstrategi och målbild

### 1.1 Vad ”optimal” betyder

Optimal betyder maximal varaktig kundnytta och god ekonomi per betjänat bolag, under bibehållen korrekthet, tydlig ansvarsfördelning och hanterbar komplexitet. Det betyder inte maximalt antal tillstånd, egna betalsystem eller en produkt för varje tänkbart branschfall.

Drastic ska äga arbetsflödet, sambanden mellan ekonomiska objekt, kvaliteten i beslutsunderlaget och den synliga kontrollen. Drastic ska köpa eller samarbeta om standardiserad infrastruktur där en partner kan leverera bättre räckvidd, ansvar och driftsekonomi. Ett partneravtal är dock inte ett generellt regulatoriskt frikort. Roll och skyldigheter ska prövas för den faktiska tjänsten. [E01, E02]

Den primära värdekedjan är:

```text
Affär inträffar
  → underlag fångas
  → rätt behandling förbereds
  → befogenhet och villkor kontrolleras
  → godkänd handling genomförs
  → externt utfall verifieras
  → redovisning och prognos uppdateras
  → avvikelse löses
  → period kan avslutas
```

Redovisningens värde är inte bara låg kostnad för registrering. Den ger ett sammanhängande underlag för att få betalt, betala rätt mottagare, planera likviditet och bedöma finansieringsbehov. Detta är produktens strategiska hypotes, inte ett påstående om redan verifierad betalningsvilja.

### 1.2 Produktkartan

```text
                               Drastic
                                  │
                        Financial Platform
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
         Accounting             Money               Revenue
             │                    │                    │
          openERP            Drastic Cash            Billing
          Tax                Treasury                Invoicing
          Payroll            Payments                Collections
          Close              Cards                   Financing
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  │
                             Drastic Risk
                                  │
                           Capital products

Gemensamt: bolag och behörighet · underlag · motparter · avtal
           godkännanden · källsamband · anslutningar · drift och support
```

Diagrammet är en produktkarta. Risk får underlag från alla tre pelarna men står inte på den kritiska bokföringsvägen för varje verifikation. Godkända betalningar går genom Payments, även när de kommer från Treasury, Payroll eller Capital. Finansiering under Revenue är kundens ingång och ansökningsresa. Capital äger produktvillkor, finansieringskapacitet och låne-/fordringslivscykel. Dessa ska inte bli två skilda kreditmotorer.

### 1.3 Målgrupper

| Segment | Huvudproblem | Primär start | Utökning |
|---|---|---|---|
| Ägarlett tjänste-AB | Underlag, moms, tid och otydlig likviditet. | Bookkeeping, arbetslista och Cash. | Fakturering, betalningar och enkel lön. |
| Byrå eller konsultbolag | Återkommande fakturering, personalkostnader och kundfordringar. | Revenue och Cash. | Payroll, projektmarginaler och rörelsekapital. |
| SaaS-/abonnemangsbolag | Avtal, användningsbaserad debitering, kreditnotor och intäktsperiodisering. | Billing och Invoicing. | Treasury, FX och kvalificerad finansiering. |
| Handels-/projektbolag | Leverantörsfakturor, inköpsåtaganden och varierande inbetalningar. | AP, Payments och Cash. | Order-/lagerintegration och fordringsfinansiering. |
| Ekonomiteam med flera bolag | Bolagsbyten, attest, kontostruktur och avstämningar. | Gemensamt arbetsflöde och koncernöversikt. | Intercompany, konsolidering och treasury-policy. |
| Redovisningsbyrå | Kundinsamling, granskningsarbete och periodstatus över flera klienter. | Byråportfölj och bokslutsarbete. | Standardiserad onboarding och kvalificerad rådgivningsvy. |

Segmenten är produktprofiler, inte legala företagsstorleksdefinitioner. En extern granskare och kundens egna ekonomiansvariga är samarbetande användare, inte störande undantag från en ”helt automatisk” produkt.

### 1.4 Två ingångar, en definierad redovisningsauktoritet

**Native-läge:** openERP är officiell bokföringskälla för de angivna böckerna och perioderna. Drastic äger bokföringsförslag, godkännande, verifikationer och export.

**Anslutet läge:** ett annat ekonomisystem är officiell bokföringskälla. Drastic importerar kvalificerade observationer och driver uttryckligen valda arbetsflöden. Ett internt analysunderlag får inte presenteras som en andra officiell bokföring. Eventuella externa bokföringsskrivningar har egen behörighet, extern identitet och återförsöksmodell.

En kund kan börja med fakturering och Cash utan att migrera hela sin bokföring. På objektnivå ska en ägarmatris ange vilket system som äger fakturan, leverantörsposten, betalningen och den officiella verifikationen. Ett byte sker genom en granskad övergång, inte genom automatisk dubbelriktad ”senaste uppdatering vinner”.

**Gemensam funktionalitet får inte förutsätta att native-läge har full källtäckning eller att en ansluten bank ger fullständiga kreditdata.** Kvalitet måste mätas i båda lägena.

### 1.5 Vad vi väljer bort även i målbilden

Drastic ska inte vara ett fullständigt CRM, tillverkningssystem, lageroptimeringssystem, rekryteringssystem eller konsumentbank. Relevanta affärsobjekt integreras i stället. Konsumentutlåning, kryptoförvaring, spekulativ handel och allmän investeringsrobot ingår inte. En framtida produkt inom dessa områden kräver en egen PRD och separat rättslig analys.

Ett internt kreditunderlag ska inte marknadsföras som ett offentligt kreditbetyg. Ett automatiskt saldoöverskott ska inte marknadsföras som lagligt utdelningsutrymme. En återkommande bokföringsregel ska inte bli ett generellt bankmandat.

<a id="chapter-2"></a>

## 2. Förhållande till Book Zero och observerat nuläge

Föregående PRD för Book Zero, dagligt arbete och Cash ligger kvar oförändrad i paketet. Den definierar den första verifieringsomfattningen. Den nya målbilden utökar produkten men sänker inte dess krav på faktiska bolagsunderlag, oberoende kontroll, exportsäkerhet eller en uttrycklig systemövergång. [B00]

Den selektivt lästa README:n vid `09fdb198...` beskriver befintliga utvecklingsytor inom bland annat bokföring, fakturor, lön, skatt, import/export och redovisningsbyråarbete. Den säger samtidigt att modulerna har olika verifieringsnivåer och att systemet ännu inte är validerat för verkliga bolagsböcker eller myndighetsinlämning. Detta arbete har inte kört produkten, reproducerat verifieringen eller granskat varje källfil. [R01]

`AGENTS.md` lägger applikationspolicy och finansiella arbetsflöden i Effect. PostgreSQL äger data, integritetsregler och transaktionsgränser. Bakgrundsarbete använder en separat Bun-process med effect-mq. Dessa gränser ska bevaras tills ett dokumenterat produkt- eller driftsbehov motiverar en ändring. [R02]

`LICENSING.md` beskriver AGPL-3.0-only för projektägd kod och anger att separata processer eller HTTP-gränser inte automatiskt undantar en kombinerad lösning från licensvillkor. Ett kommersiellt erbjudande ska därför bygga på betald drift, service och tydligt rättighetsgranskade utökningar, inte på ett antagande att en ny katalog gör koden proprietär. Kunddata är inte källkod. [R03]

### Kontinuitetskarta

| Första PRD | Målbildens fortsättning | Behållen gräns |
|---|---|---|
| BZ-01–BZ-05 | Plattformsonboarding, källinventering och övergång mellan system. | En faktisk period kan inte godkännas från syntetiska underlag. |
| BZ-06–BZ-11 | Accounting, Tax, AP, Payroll och periodkontroller. | Godkänd ekonomisk effekt och bevarad rättelsehistorik. |
| BZ-12–BZ-14 | Close, arkiv, export och kontrollerat systembyte. | Teknisk export är inte ett bevis på myndighetsgodtagande. |
| WF-01–WF-08 | Gemensamt arbete för företagare, ekonomiteam och byrå. | Ingen falsk tomhet, ingen falsk framgång. |
| AI-01–AI-04 | Avgränsade agenter och senare uttryckliga stående mandat. | Agenten kan aldrig bevilja sitt eget mandat. |
| CASH-01–CASH-17 | Cash, treasury-planering och finansieringsscenarier. | Inget belopp räknas dubbelt och antaganden är inte fakta. |
| NFR-01–NFR-06 | Plattformens drift, säkerhet och finansoperativa krav. | Verifierbar återställning och kvarvarande tillgång till historik. |

Bolagsuppgifter i det äldre dokumentet används bara för dess namngivna prov. Målbildens kundmodell ska inte hårdkoda Drastics bank, räkenskapsår eller ägarförhållanden.

<a id="chapter-3"></a>

## 3. Hur den färdiga produkten upplevs

### 3.1 Företagarens måndagsmorgon

Företagaren öppnar ”Översikt” och ser tre saker: beslut som behöver fattas, ekonomins senaste kvalificerade läge och viktiga datum. Tolv rutinärenden är förberedda. Två leverantörsfakturor behöver förklaring. En kund har bestridit en del av en faktura. Cash visar att marginalen blir lägst före nästa löneutbetalning.

Företagaren öppnar avvikelsen, ser original, föreslagen behandling och konsekvens. Ett betalningsförslag kan granskas i samma resa, men att godkänna kostnaden flyttar inte pengarna. En betalningsgodkännare ser mottagare, kontoversion, belopp, valuta, datum och exakt betalningsmandat.

Vid likviditetsrisk visas först orsaker och operativa alternativ: följ upp en kundbetalning, flytta en utgift inom avtalade villkor eller använda tillgänglig likviditet på ett annat konto. Finansiering kan visas som ett separat, genomlyst alternativ. Prognosen får inte medvetet överdriva underskott för att sälja kredit.

### 3.2 Ekonomiteamets arbetsdag

Teamet arbetar från en gemensam kö med ansvar, förfallodatum, belopp, källtäckning och nästa handling. Ett dokument, en betalning och en bokföringsåtgärd är länkade men har varsin verklig status. Fakturor kan granskas i ett sidopanelssammanhang, medan komplicerade skatte- eller lönebedömningar får full arbetsyta.

Vid slutet av dagen kan teamet se genomförda handlingar, öppna undantag och okända externa utfall. En grön sammanställning får aldrig bygga på att en bankanslutning har slutat leverera data.

### 3.3 Redovisningsbyråns månadsslut

Byrån ser klienter med tillämpliga kontrollområden, senaste avstämning och underlag som saknas. Granskaren öppnar en klient utan att förlora portföljens filter. Åtkomst ges genom både byrårelation och klientens aktuella behörighet. Byråanställning i sig öppnar inte en kundbok.

Rapporten går från total till verifikation, beslut och original. En granskningsmarkering avser ett fast underlag och blir inaktuell om ett materiellt beroende ändras. Den gamla granskningen bevaras som historik. Årsarbetet samlar nödvändiga signaturer och inlämningskvitton utan att förväxla ett uppladdat dokument med ett slutfört myndighetsärende.

### 3.4 Kunden som får en faktura

Mottagaren ser vem som kräver betalning, vad som levererats, förfallodatum, saldo och tillåtna betalsätt. Kunden kan betala, hämta faktura, lämna betalningsreferens eller bestrida en identifierad del. En invändning öppnar ett granskningsärende och stoppar berörd automatisk eskalering, inte all ekonomisk historik.

Om fordran överlåtits ska rätt betalningsmottagare och rätt instruktion visas. Ett gammalt fakturalänkformat får inte leda till dubbel uppmaning att betala både ursprunglig säljare och finansiär.

### 3.5 Anställdas minsta gränssnitt

Anställda ser sina kort, egna utlägg, relevanta policyer och egna lönedokument. De kan frysa ett kort och lämna underlag utan att få insyn i företagets fullständiga likviditet eller andra personers löner. Ett saknat kvitto är en uppgift, inte ett skäl att uppfinna ett underlag.

<a id="chapter-4"></a>

## 4. Produktkonstitution

1. **En bokföringsauktoritet per bok och period.** Projektioner och partnerkopior får inte bli alternativa huvudböcker.
2. **En ekonomisk händelse kan ha flera bevis.** Filhash, bankrad, faktura och leverantörswebhook är inte automatiskt fyra ekonomiska händelser.
3. **Observerat, bokfört, avtalat och prognostiserat är skilda klasser.** Skillnaden ska synas i kontrakt och gränssnitt.
4. **Pengar är exakta värden med valuta.** Belopp, ränta, kvantitet och växelkurs har uttrycklig precision och avrundningspolicy.
5. **Mänsklig befogenhet kontrolleras vid handlingen.** En gammal skärmbild eller en agentplan ger ingen aktuell rättighet.
6. **Godkännande binds till vad som faktiskt sker.** Ändrad mottagare, källa, belopp eller materiellt villkor kan kräva nytt godkännande.
7. **Externt utfall kräver externt belägg.** API-acceptans är inte alltid utbetalning, avveckling, myndighetsinlämning eller slutlig leverans.
8. **Okänt utfall är ett förstklassigt tillstånd.** Det får inte omvandlas till misslyckande för att förenkla återförsök.
9. **Historik rättas framåt.** Ingen tyst omskrivning av utställda dokument, bokförda belopp eller gamla kreditbeslut.
10. **Rättighet, tillgänglighet och kommersiellt abonnemang är olika kontroller.** En betald modul ger inte bankmandat eller legalt tillstånd.
11. **Kunden äger inte andra kunders data.** Gemensam teknik skapar inte en fri global databas över motparters betalningsbeteende.
12. **Finansiering är ett separat val.** En bra produkt ska även fungera för företag som aldrig lånar.
13. **Drift är en del av produkten.** Avstämning, klagomål, incidenthantering och leverantörsbyte ingår i målbilden.
14. **Ingen kosmetisk fullständighet.** Ett balanserat delunderlag eller en tom kö kan fortfarande vara ofullständigt.
15. **Regelverk är versionsbundna indata.** Nya skatteregler, bankformat och behörighetskrav ska kvalificeras innan de aktiveras.
16. **Optimal omfattning aktiveras profilvis.** Nytt land, ny kreditprodukt eller ny lönefamilj får egna prov och stödgränser.

<a id="chapter-5"></a>

## 5. Ekonomisk modell och ansvar

### 5.1 Fem skilda perspektiv på samma företag

| Perspektiv | Auktoritativ ägare | Exempel | Får inte sammanblandas med |
|---|---|---|---|
| Bokföring | Företagets valda huvudbok. | Verifikation, redovisat saldo och periodresultat. | Bankens disponibla saldo eller en prognos. |
| Kommersiella åtaganden | Avtals-, faktura-, löne- och skatteägare. | Återstående fordran eller kommande lönebetalning. | Att pengar redan har flyttats. |
| Betalningsgenomförande | Payments för kommandot, leverantören för sitt externa utfall. | Godkänd betalningsorder, bankreferens och avvecklingsbelägg. | Automatisk kostnads- eller intäktsbokning. |
| Finansiell tjänst | Namngiven bank, utgivare eller långivare enligt avtal. | Kontobehållning, kortreservation och lånesaldo. | Drastics egna rörelsemedel. |
| Analys och prognos | Reproducerbar projektion över kvalificerade källor. | Likviditet, riskfaktorer och scenario. | Officiell bokföring eller ett bindande kreditlöfte. |

Ett operativt register för pengar eller en kreditreskontra får behövas för en reglerad tjänst. Det ska då ha uttalat ändamål, bokföringskoppling och avstämning. Regeln ”ingen andra huvudbok” förbjuder konkurrerande sanningar om samma bok, inte separata väl avgränsade delregister eller olika juridiska parters böcker.

### 5.2 Tid och historik

Varje väsentlig observation ska skilja mellan händelsedatum, bokföringsdatum, leverantörens tidsstämpel, registreringstid och den tidpunkt då Drastic kunde känna till uppgiften. Ett månadsslut och en prognos använder inte nödvändigtvis samma tidsgräns.

Ett scenario bygger på ett fryst underlag. Senare erhållna uppgifter ska skapa en ny version. Försenade webhooks kan komplettera verklig historik men får inte ändra vad en tidigare användare såg utan spårbar versionsändring.

### 5.3 Mandat och roller

| Roll | Typiskt tillåtet | Uttrycklig begränsning |
|---|---|---|
| Bolagsadministratör | Medlemskap och godkända produktinställningar. | Får inte automatiskt läsa alla löner eller godkänna egna utbetalningar. |
| Beredare | Underlag, förslag och avstämningsarbete. | Ingen självbeviljad attest eller bankbehörighet. |
| Bokföringsgodkännare | Godkänna exakta bokföringseffekter. | Ingen automatisk betalningsrätt. |
| Betalningsgodkännare | Godkänna betalningsorder inom mandat. | Får inte ändra den granskade mottagaren i samma godkännande. |
| Löneansvarig | Anställningsdata och lönekörningar. | Persondata skyddas från generella ekonomivyer. |
| Kreditanalytiker | Granska underlag och föreslå beslut. | Kan inte ensam ändra riskpolicy och bevilja sitt eget undantag. |
| Långivare/kreditbeslutare | Fatta och bära avtalat kreditbeslut. | Plattformens datakvalitetsflagga ersätter inte beslutet. |
| Drift/support | Diagnostik eller tidsbegränsad delegerad åtkomst. | Ingen tyst supportinloggning eller rätt att skapa kundens finansiella handlingar. |
| Agent | Delegerad läsning och avgränsad förberedelse/genomförande. | Får aldrig skapa eller utöka det mandat som används. |
| Extern granskare | Definierad granskningsomfattning. | Ingen generell fullmakt genom att en delningslänk öppnas. |

Separation mellan beredare och godkännare ska vara policybar. Ett ensamt ägarlett AB kan ha en dokumenterat tillåten rollkombination, men ingen sådan kombination får ärvas som standard i en betal- eller kreditverksamhet som kräver oberoende funktioner.

### 5.4 Gemensam godkännandemodell

Ett godkännande ska bära bolag, handlingstyp, berörda objektrevisioner, belopp/valuta, mottagarversion när relevant, effektdigest, giltighetstid och den policy som gjorde personen behörig. Betalningssignering och eventuell stark kundautentisering är ytterligare steg när leverantör och regelverk kräver dem. Ett BankID-resultat ska inte tolkas som generell firmateckningsrätt.

För ett stående mandat tillkommer tillåtna motparter, konton, beloppsgräns per handling, kumulativ gräns, tidsfönster, undantag, giltighetsperiod och återkallelseväg. Kontroll av kvarvarande budget måste vara atomisk. Agenten får inte kringgå en gräns genom att dela upp ett belopp i flera små kommandon.


<a id="chapter-6"></a>

## 6. Plattform, bolag och etablering

**Första leveransnivå:** ES-1. **Ändamål:** Ge varje kund en begriplig väg in utan att blanda juridisk identitet, bokföringsansvar och behörighet.

**Huvudresa:** Välj användningssätt → identifiera bolaget → fastställ omfattning → anslut eller importera → kontrollera → aktivera kvalificerade funktioner.

**Ägda begrepp:** Tenant, legal entity, book, legal profile, membership, source inventory, product activation och consent grant.

### DR-CORE-01: Två vägar in

Onboarding ska erbjuda Native, där openERP är officiell huvudbok, och Connected, där ett externt system behåller detta ansvar. Valet ska sparas per bolag, bok och tidsintervall. Kunden ska se vad som läses, vad som kan skrivas och var rättelser utförs.

**Gräns och undantag:** Connected får inte skapa en tyst kopia som konkurrerar om officiella verifikationsnummer.

**Acceptans:** En ansluten kund kan öppna en faktura, se dess systemägare och ledas till rätt rättelseväg utan dubbla bokningar.

### DR-CORE-02: Bolag och koncern

Ett konto ska kunna administrera flera juridiska personer med skilda böcker, bankrelationer, perioder och avtal. Koncerntillhörighet modelleras tidsbundet. Koncernöversikten visar både separata värden och kvalificerade aggregat.

**Gräns och undantag:** Samma ägare innebär inte att pengar eller behörigheter är fritt överförbara mellan bolagen.

**Acceptans:** En medlem med åtkomst till moderbolaget men inte dotterbolaget ser inte dotterbolagets underlag eller löner.

### DR-CORE-03: Produktprofil och aktivering

Aktivering ska beskriva land, bolagsform, redovisningsmetod, rapporteringsramverk, valuta, relevanta registreringar och stödda transaktionstyper. Varje funktion har status tillgänglig, behöver konfiguration, behöver granskning, externt blockerad eller ej stödd.

**Gräns och undantag:** En ifylld inställning får inte automatiskt innebära verifierad regelefterlevnad.

**Acceptans:** En momsprofil kan vara aktiv för en period samtidigt som en ny transaktionstyp uttryckligen blockeras.

### DR-CORE-04: Källinventering

Kunden ska registrera förväntade bankkonton, fakturakällor, betalningsförmedlare, lönekällor och historiska system. Inventeringen ska mäta periodtäckning och ansvarig för varje saknad källa. Upptäckta nya konton blir granskningsärenden.

**Gräns och undantag:** Noll importerade transaktioner är inte bevis för att ett konto saknar aktivitet.

**Acceptans:** En tom arbetslista visar ändå att kontoutdrag för ett inventerat konto saknas.

### DR-CORE-05: Identitet och mandat

Inloggning, organisationsmedlemskap, firmateckningsunderlag och operativa mandat ska vara separata begrepp. Återkallelse ska slå igenom vid nästa skyddade handling. Stegrad autentisering begärs för känsliga förändringar.

**Gräns och undantag:** En lyckad identitetskontroll eller ett BankID-resultat ger inte i sig betalnings- eller kreditmandat.

**Acceptans:** En inloggad person vars betalningsmandat återkallats kan läsa tillåtna rapporter men inte bekräfta en väntande betalning.

### DR-CORE-06: Kundkännedom per tjänst

KYB/KYC ska samordna insamling av bolagsuppgifter, verklig huvudman, företrädare och tjänstens syfte när aktuell roll kräver detta. Kunden får återanvända redan kvalificerade uppgifter där det är tillåtet. Varje reglerad tjänsteleverantörs beslut och kvarvarande krav visas.

**Gräns och undantag:** Kundkännedom hos en leverantör är inte automatiskt giltig hos alla andra.

**Acceptans:** Kort kan vara tillgängligt medan finansiering väntar på komplettering, med rätt leverantör och skäl synliga.

### DR-CORE-07: Samtycke och ändamål

Behörighet till datakällan, rättslig grund för behandling och ändamål för användning ska dokumenteras separat. Finansieringsdelning ska visa mottagare, uppgiftskategorier, omfattning och varaktighet. Återkallelse stoppar framtida användning enligt tillämpliga skyldigheter.

**Gräns och undantag:** Ett allmänt produktgodkännande är inte fri rätt att träna modeller eller sälja riskdata.

**Acceptans:** En kund kan använda bokföring utan att aktivera extern kreditbedömning eller generell modellträning.

### DR-CORE-08: Partregister och identitetskonflikter

Kunder, leverantörer, anställda och långivare ska länkas med granskningsbara identiteter. Sammanfogning ska bevara ursprungliga dokumentidentiteter och historiska adresser. Kontoändringar hanteras som separata känsliga revisioner.

**Gräns och undantag:** Namnlikhet eller samma e-postdomän räcker inte för att slå ihop juridiska motparter.

**Acceptans:** Två leverantörer med samma namn behåller separata fordringar och betalningsmottagare efter sökning och import.

### DR-CORE-09: Ekonomisk identitet över gränser

Varje händelsekedja ska kunna länka affärsåtagande, källdokument, bokföringsbeslut, betalningsavsikt och leverantörsutfall. Relationerna ska ange del, helhet, ersättning, rättelse eller avräkning. Ursprungliga IDs ska behållas vid migration.

**Gräns och undantag:** Ett dokumenthash är inte ensam identitet för affärshändelsen eftersom identiska bytes kan förekomma i skilda sammanhang.

**Acceptans:** En leverantörsfaktura från både e-post och e-faktura identifieras som möjlig dublett utan att legitima separata fakturor försvinner.

### DR-CORE-10: Versionerade företagsfakta

Bolagsfakta och policyer ska ha giltighetsintervall och när de blev kända. Ändring ska visa vilka öppna förslag, prognoser eller deklarationer som påverkas. Redan slutna resultat bevaras och kan jämföras med en ny bedömning.

**Gräns och undantag:** En retroaktiv rättelse får inte tyst ändra ett tidigare beslutsunderlag.

**Acceptans:** Ändrad momsmetod ger ett avgränsat konsekvensärende i stället för omräkning av all historik utan godkännande.

### DR-CORE-11: Portabilitet och produktavslut

Bolaget ska kunna exportera original, register, transaktionshistorik, revisionskedjor och rapporter i dokumenterade format. Exporten ska ange omfattning, bryttid och sådant som inte kan flyttas utan ny leverantörsprövning.

**Gräns och undantag:** Ett avslutat abonnemang upphäver inte pågående låneavtal, kortreklamationer eller lagstadgad arkivering.

**Acceptans:** En exitövning lämnar ett läsbart paket och en lista över återstående externa relationer utan att kräva produktdatabasen.

### DR-CORE-12: Produktåtkomst skild från befogenhet

Abonnemang och funktionspaket ska styra vilka erbjudanden som finns, medan backendmandat styr vem som får använda dem. Uppgradering får öppna onboarding men aldrig direkt ge en användare betalnings- eller kreditbefogenhet.

**Gräns och undantag:** Prissättning får inte låsa kunden ute från nödvändig historik, rättelseinformation eller avtalad exit.

**Acceptans:** En användare som köper Payments kan inte signera förrän både tjänsten och personens mandat har kvalificerats.


<a id="chapter-7"></a>

## 7. Dagligt arbete och beslutsupplevelse

**Första leveransnivå:** ES-1. **Ändamål:** Göra plattformens bredd begriplig genom arbete som faktiskt går att avsluta.

**Huvudresa:** Se avvikelsen → förstå källan → granska förslaget → godkänn rätt handling → följ utfallet → återgå till samma sammanhang.

**Ägda begrepp:** Work item, exception, review bundle, assignment, saved view, decision receipt och activity timeline.

### DR-WORK-01: En sammanhållen arbetslista

Startsidan ska prioritera blockerande arbete, kommande skyldigheter och faktiska ekonomiska avvikelser. Varje rad ska förklara varför den finns, vilket bolag och objekt som berörs, känd ekonomisk effekt, ansvarig och nästa handling.

**Gräns och undantag:** Antal ärenden får inte manipuleras genom att slå ihop olika skyldigheter eller räkna samma problem flera gånger.

**Acceptans:** Ett saknat kvitto och en osäker behandling visas samlat med två tydliga delsteg och en beständig objektlänk.

### DR-WORK-02: Rollanpassad start

Grundare ska se beslut och ekonomiskt läge, ekonomiteam arbetsköer och avstämning, redovisningsbyråer klientportfölj och anställda egna ärenden. Användaren ska kunna byta vy utan att ekonomiska fakta eller befogenheter ändras.

**Gräns och undantag:** En ledningsvy får inte avslöja individuella löner via aggregering av små grupper.

**Acceptans:** Samma faktura kan öppnas från grundarvyn och ekonomivyn med samma revisions- och betalningsstatus.

### DR-WORK-03: Status på rätt nivå

Förberett, godkänt, skickat, externt mottaget, genomfört, bokfört och avstämt ska visas som separata relevanta tillstånd. En objektöversikt kan förenkla språket men ska bevara distinktionerna i detaljerna.

**Gräns och undantag:** En grön bock för tekniskt skickat får inte antyda att kunden har betalat eller att myndigheten accepterat innehållet.

**Acceptans:** Ett skickat betalningsuppdrag med okänt utfall visas som pågående kontroll, inte som betalt eller misslyckat.

### DR-WORK-04: Kontextuell granskning

Granskning ska visa affärsobjekt, original, tolkade fakta, föreslagna effekter och relevanta avvikelser tillsammans. Användaren ska kunna korrigera fakta utan att förlora originalet eller tidigare bedömningar.

**Gräns och undantag:** Ett tekniskt JSON-utdrag är inte den primära granskningsupplevelsen.

**Acceptans:** En ovanlig momsbehandling kan granskas med underlag och kontoeffekt inom samma resa på desktop och mobil.

### DR-WORK-05: Exakt batchgodkännande

Batchgranskning ska namnge urval, versioner och belopp. Användaren ska kunna ta bort en rad och granska undantag separat. Resultat redovisas per finansiell grupp med återupptagning av endast kvarvarande arbete.

**Gräns och undantag:** En batch är inte en distribuerad allt-eller-inget-transaktion mot banker eller myndigheter.

**Acceptans:** Tolv förslag där ett blivit inaktuellt ger elva redovisade resultat och ett nytt granskningsbehov, aldrig en oklar totalsuccess.

### DR-WORK-06: Beständig återgång

Filter, bolag, period, sortering och markerat objekt ska kunna återskapas efter omladdning eller djup länk. Sparade men ofullständiga användarinmatningar ska återställas med tydlig versionskontroll.

**Gräns och undantag:** Lokal cache får inte visa en gammal behörighet eller en optimistiskt lyckad ekonomisk mutation.

**Acceptans:** Efter ett tappat svar öppnas samma kvitto eller samma oavgjorda handling och användaren återgår till rätt arbetslista.

### DR-WORK-07: Tomt, ofullständigt och otillgängligt

Ingen kvarvarande uppgift, ofullständigt källunderlag, ej konfigurerad modul och tjänsteavbrott ska ha skilda visuella tillstånd. Täckning ska beskrivas på samma nivå som det påstådda resultatet.

**Gräns och undantag:** Ingen generell produktbanner får ersätta en varning vid det belopp som påverkas.

**Acceptans:** En tom betalningslista bredvid en frånkopplad bank ger ingen uppgift om att alla betalningar är genomförda.

### DR-WORK-08: Samarbete och ansvar

Ärenden ska kunna tilldelas, kommenteras och begäras kompletterade. Kommentarer, kundförfrågningar och attest är olika aktiviteter. Byte av ansvarig får inte överföra ett personligt ekonomiskt mandat.

**Gräns och undantag:** En kommentar som säger godkänd är inte en ekonomisk attest.

**Acceptans:** Redovisningskonsulten kan be ägaren om ett underlag och återuppta arbetet utan att få bankrättigheter.

### DR-WORK-09: Aviseringar och uppmärksamhet

Aviseringar ska sammanfatta nya eller förändrade handlingsbehov, med prioritet baserad på tidsfrist och påverkan. Tystnadstider och kanalval ska finnas. Kritiska drift- och avtalsmeddelanden följer sin separata policy.

**Gräns och undantag:** Återförsök och duplicerade webhooks får inte skapa en serie identiska kundaviseringar.

**Acceptans:** En försenad faktura med oförändrat läge ger inte flera dagliga påminnelser till ägaren utan uttrycklig policy.

### DR-WORK-10: Handlingsbar ekonomisk förklaring

Varje viktigt saldo, rekommendation och riskflagga ska kunna förklaras genom bidrag, datum och underlag. Förklaringen ska kunna leda till faktisk rättelse eller komplettering, inte bara visa en textsammanfattning.

**Gräns och undantag:** Modellens interna resonemang är inte revisionsbevis; källor, regler och registrerade beslut är det.

**Acceptans:** Kunden kan gå från lägsta prognossaldo till de tre största betalningarna och ändra ett scenario utan att ändra bokföringen.


<a id="chapter-8"></a>

## 8. Accounting: openERP och redovisningskärnan

**Första leveransnivå:** ES-1. **Ändamål:** Vara en komplett redovisningsgrund inom kvalificerade bolagsprofiler och ett spårbart underlag för övriga produkter.

**Huvudresa:** Underlag → behandling → förslag → attest → bokföring → register → avstämning → rapport.

**Ägda begrepp:** Book, account, journal, voucher, accounting proposal, tax fact, settlement allocation, schedule och correction.

### DR-ACC-01: Exakta värden

Bokförda belopp ska använda exakta minor units i respektive valuta. Kvantitet, pris, ränta och valutakurs ska ha egna exakta skalor och explicit avrundningspolicy. Summering ska ske före den avrundning som den kvalificerade regeln föreskriver.

**Gräns och undantag:** JavaScript-flyttal eller modellgenererade numeriska strängar får inte vara monetär auktoritet.

**Acceptans:** Belopp över Number.MAX_SAFE_INTEGER kan förberedas, bokföras och exporteras utan förlust av en minor unit.

### DR-ACC-02: Gemensam bokföringsväg

UI, REST, MCP, importer och bakgrundsarbeten ska använda samma namngivna bokföringsoperationer. Behörighet, källa, period, konto och domänägarskap ska kontrolleras innan en finansiell grupp genomförs.

**Gräns och undantag:** Ett integrationskonto får inte kringgå källkapacitet genom generisk verifikation.

**Acceptans:** Försök att bokföra samma domänägares underlag via två transportvägar ger högst en tillåten ekonomisk effekt.

### DR-ACC-03: Oföränderlig historik

Bokförda verifikationer, numrering och underlagskopplingar ska bevaras. Rättelse skapar identifierade följdhändelser med hänvisning till originalet och aktuell periodpolicy. Historik ska kunna granskas i kronologisk och systemmässig ordning.

**Gräns och undantag:** Radering av ett affärsutkast får inte ta bort redan bokförd eller utgiven historik.

**Acceptans:** Efter en återföring visas både original, rättelse och deras nettokonsekvens i register och rapport.

### DR-ACC-04: Transaktion och återförsök

Registereffekter, huvudbok, attestförbrukning, finansiella räknare och genomförandekvitto ska dela samma transaktion. Återförsök med samma identitet ska återge ursprungligt resultat. Ändrat kommando med gammal identitet ska vägras.

**Gräns och undantag:** En HTTP-timeout bevisar inte rollback.

**Acceptans:** Samtidiga genomföranden av samma godkända förslag lämnar en verifikation och ett återfinnbart resultat.

### DR-ACC-05: Kontoplan och dimensioner

Kontoplan, kontoroller, verifikationsserier, kostnadsställen och projekt ska vara versionsstyrda. Förslag ska använda aktuell kvalificerad kontoroll. Rapportgruppering får utvecklas utan att historiska konton skrivs om.

**Gräns och undantag:** Ett BAS-liknande kontonummer är inte tillräckligt för att avgöra skattebehandling eller juridisk tillämplighet.

**Acceptans:** Bytt rapportgruppering kan jämföras mellan versioner medan originalkontot i varje verifikation förblir oförändrat.

### DR-ACC-06: Reskontror och kapacitet

Kund- och leverantörsposter ska bevara ursprungligt belopp, krediter, betalningsallokeringar och återstående kapacitet. En rättelse ska återställa rätt konsumtion genom sin egen historiska handling.

**Gräns och undantag:** Överbetalning får inte döljas som negativ fakturarest om den är ett separat tillgodohavande.

**Acceptans:** Delbetalning, kredit och återförd matchning ger korrekta belopp samtidigt i reskontra, huvudbok och Cash.

### DR-ACC-07: Bank och övriga avstämningar

Avstämning ska ange konto, period, kontoutdragsidentitet, bokföringsgräns och oförklarade poster. Bank, skattekonto, betalningsförmedlare, kortavräkning och lånesaldon ska ha sina egna kontroller.

**Gräns och undantag:** Matchad text eller samma slutsaldo räcker inte när transaktionskedjan är ofullständig.

**Acceptans:** Två orelaterade motsatta avvikelser som tar ut varandra lämnar kontrollen ofullständig.

### DR-ACC-08: Valutor och valutadifferenser

Ursprungliga valutaenheter och bokföringsvalutans värde ska bevaras tillsammans. Uppgörelse frigör rätt bokfört värde och beräknar kvalificerad valutadifferens. Omvärdering är skild från en faktisk betalning eller växling.

**Gräns och undantag:** Dagens kurs får inte återanvändas som historiskt anskaffningsvärde.

**Acceptans:** En delbetalning i EUR minskar rätt ursprungsbelopp och bokfört restvärde med spårbar differens och separat bankavgift.

### DR-ACC-09: Periodisering och tillgångar

Förutbetalda kostnader, upplupna poster, intäktsperiodisering och tillgångsscheman ska härledas från dokumenterade grunder. Ändrade uppskattningar bevarar förbrukad historik och skapar en kvalificerad framtida plan.

**Gräns och undantag:** Ett generiskt schema får inte automatiskt välja avskrivningsmetod eller ekonomisk nyttjandeperiod.

**Acceptans:** En ändrad nyttjandeperiod ger en tydlig jämförelse och ändrar inte tidigare godkända perioder utan rättelseförfarande.

### DR-ACC-10: Ägartransaktioner

Privata utlägg, ersättningar, aktieägarlån, kapitaltillskott och utdelningsrelaterade händelser ska ha särskilda underlag och roller. En privat betalning ska kunna styrka en företagskostnad utan att ett privat konto läggs in som företagets bank.

**Gräns och undantag:** Likviditetsutrymme från Cash är inte utdelningsutrymme.

**Acceptans:** Ett ägarbetalt kvitto och senare ersättning ger en kostnad och en reglering av skulden, inte två kostnader.

### DR-ACC-11: Import och byte av officiell källa

Historisk import ska separera ursprungliga verifikationer, ingående saldon och öppna poster. Migration ska ha låst omfattning, kontrollsummor, source IDs och en bryttid. Native aktiveras först när en enda officiell skrivande källa är utsedd.

**Gräns och undantag:** Att läsa från ett externt system ger inte rätt att ändra dess historik eller köra två officiella böcker parallellt.

**Acceptans:** En migrerad obetald faktura kan senare regleras utan att dess historiska intäkt bokförs igen.

### DR-ACC-12: Interna affärer och koncern

Transaktioner mellan bolag ska registreras i respektive juridiska persons bok med matchbara relationer, valutor och avtal. Elimineringar hör till en koncernrapport och ska kunna spåras utan att radera bolagens poster.

**Gräns och undantag:** Koncernnetto får inte användas för att kringgå bank-, skatte- eller kapitalrestriktioner.

**Acceptans:** En intern försäljning syns i båda böckerna och kan elimineras separat med en förklarad avstämningsdifferens.

### DR-ACC-13: Rapporter och förklaringskedja

Rapporter ska frysa medlemskap, versioner och klassificering. Balans- och resultaträkning, huvudbok, reskontrarapporter och historiskt kassaflöde ska kunna drillas till källposter. Omklassificering ger en ny rapportversion.

**Gräns och undantag:** Framtidsprognos får inte presenteras som historisk kassaflödesanalys.

**Acceptans:** En sparad rapport visar samma bidrag efter att leverantörsnamn, kontogruppering eller prognosantaganden ändrats.

### DR-ACC-14: Stödda profiler och vägran

Transaktionstyper ska vara tillgängliga först när bolagsprofil, regler och implementation är kvalificerade. Systemet ska kunna föreslå en manuell expertgranskning utan att förlora arbetsunderlaget.

**Gräns och undantag:** Fler fält i gränssnittet innebär inte automatiskt fullständigt stöd för en ny jurisdiktion.

**Acceptans:** En ej stödd skattebehandling sparas som ett öppet ärende men kan inte bokföras som en kvalificerad standardbehandling.


<a id="chapter-9"></a>

## 9. Accounting: Tax och skyldigheter

**Första leveransnivå:** ES-1 till ES-2. **Ändamål:** Knyta skatteunderlag, deklaration, betalningsbehov och extern bekräftelse till samma spårbara skyldighet.

**Huvudresa:** Kvalificera regel → samla skattefakta → kontrollera → granska → signera eller överlämna → verifiera inlämning → stäm av skattekonto.

**Ägda begrepp:** Rule release, tax fact, obligation, return snapshot, amendment, submission attempt och tax-account observation.

### DR-TAX-01: Daterade regelpaket

Varje skatteberäkning ska binda land, period, regelversion, källproveniens och bolagsfakta. Regler ska kunna introduceras före ikraftträdande utan att bli retroaktiv standard. Saknade eller motstridiga parameteruppgifter ska stoppa den berörda beräkningen.

**Gräns och undantag:** Värden från referensrepo, LLM eller föregående år är inte auktoritativa skatteregler.

**Acceptans:** En transaktion på vardera sidan av en regeländring använder rätt paket och visar skillnaden.

### DR-TAX-02: Momsbehandling vid källan

Momsfakta ska bära transaktionstyp, belopp, valuta, datum, underlag och bedömd behandling. Omvänd skattskyldighet, EU-handel, export, reducerade satser och avdragsbegränsningar ska vara kvalificerade profiler, inte en fri procentsats.

**Gräns och undantag:** Systemet får inte inferera skattskyldighet enbart från leverantörens land eller kontonummer.

**Acceptans:** Ett gränsöverskridande köp med ofullständiga fakta blir en tydlig bedömningsfråga innan deklarationsunderlag fastställs.

### DR-TAX-03: Momsdeklarationens kedja

Deklarationsförslag ska ha fryst transaktionsmängd, boxbidrag och avstämning mot huvudboken. Tillägg och borttag ska skapa reviderat förslag. Inlämnad version bevaras tillsammans med underlag och mottagningskvitto.

**Gräns och undantag:** Framställd XML eller PDF betyder inte inlämnad eller godkänd deklaration.

**Acceptans:** En rättad transaktion efter inlämning skapar en jämförelse mot den faktiskt inlämnade versionen.

### DR-TAX-04: Skattekonto och likviditet

Observerat skattekontosaldo, bokförda kontrollkonton och framtida skatteskulder ska hållas isär. Cash ska använda den kompletterande överföring som behövs, med datum och täckning, i stället för att samtidigt dra av skatt och samma förskottsinbetalning.

**Gräns och undantag:** En överföring till skattekontot får inte ensam öronmärka eller bekräfta en särskild skatt. [E12]

**Acceptans:** 30 000 i kvalificerat skattekontosaldo och 50 000 i framtida debiteringar ger 20 000 i ytterligare bankbehov under det uttryckliga scenariot.

### DR-TAX-05: Bolagsskatt och skattebrygga

Skatteunderlag ska förklara övergången från redovisat resultat till beskattningsbart underlag genom versionsbundna justeringar. Aktuell skatt, preliminära inbetalningar och eventuell uppskjuten skatt enligt tillämpligt ramverk ska hållas separata.

**Gräns och undantag:** Redovisat resultat multiplicerat med en procentsats är inte en generell komplett bolagsskatteberäkning.

**Acceptans:** En icke avdragsgill post kan följas till underlag, justering och påverkan på skatteberäkning utan att originalkostnaden försvinner.

### DR-TAX-06: Arbetsgivardeklarationer

Löneunderlag ska produceras av Payroll med bestämda betalnings- och rapporteringsperioder. Tax äger deklarationsversion, kontroll, överlämning och myndighetsutfall. Individuppgifter ska skyddas genom separat åtkomst.

**Gräns och undantag:** En lönekörning som bokförts men inte betalats får inte utan kvalificerad regel behandlas som ett redan inträffat rapporteringsunderlag.

**Acceptans:** En korrigerad lön visar exakt vilka individuppgifter och perioder som behöver rättas.

### DR-TAX-07: Tidsfrister

Skyldighetskalendern ska härleda förfallodag från aktuell bolagsprofil, period och kvalificerad kalender. Frister för förberedelse, godkännande, banköverföring och myndighetsinlämning ska skiljas åt.

**Gräns och undantag:** Sista bankdag eller klipptid får inte gissas från en generell måndag-fredag-kalender.

**Acceptans:** En regel- eller registreringsändring skapar nya framtida skyldigheter med jämförelse och behåller historiska beslut.

### DR-TAX-08: Inlämning och okänt utfall

Varje extern inlämning ska ha exakt filhash, personligt eller delegerat mandat, försök och extern referens. Vid oklart utfall ska systemet först återfinna status hos leverantören och stoppa okontrollerad dubbelsändning.

**Gräns och undantag:** Teknisk nätverksfelkod innebär inte att myndigheten saknar handlingen.

**Acceptans:** En timeout efter mottagning återhämtar samma externa kvitto och lämnar en officiell version.

### DR-TAX-09: Rättelse och jämförelse

Rättelser ska visa tidigare inlämnad version, nya fakta, beloppsdelta och eventuellt ändrad betalningsprognos. Positiva och negativa skillnader ska behandlas symmetriskt. Behörig person godkänner rättelsen separat.

**Gräns och undantag:** En ny beräkning får inte ersätta tidigare myndighetskvitto.

**Acceptans:** Två rättelser i samma period kan jämföras i ordning med olika kvitton och en aktuell ekonomisk konsekvens.

### DR-TAX-10: Experthandoff

Kunden ska kunna lämna över komplett underlag till redovisningskonsult eller skattespecialist och registrera verifierad extern behandling. Handoff ska ha ägare, omfattning och öppna frågor samt kunna återtas utan förlust av historik.

**Gräns och undantag:** Extern granskning får inte visas som genomförd bara för att ett paket delats.

**Acceptans:** En konsult kan lämna tillbaka granskade justeringar som nya förslag utan direkt skrivåtkomst till huvudboken.

**Primär regelkälla är alltid den tillämpliga myndigheten och den daterade regelversionen.** Detta dokument fastställer inte skattesatser, bolagets deklarationsskyldigheter eller en viss inlämningskanals aktuella schema.


<a id="chapter-10"></a>

## 10. Accounting: Payroll

**Första leveransnivå:** ES-2. **Ändamål:** Göra lönearbete, arbetsgivarkostnader och utbetalningar sammanhängande utan att blanda redovisning med personalbedömning.

**Huvudresa:** Anställningsvillkor → periodens underlag → löneförslag → granskning → fastställelse → betalning → AGI och avstämning.

**Ägda begrepp:** Employment revision, pay input, benefit, absence, payroll calculation, payslip, pay run och payroll correction.

### DR-PAY-01: Tidsbundna anställningar

Anställning, sysselsättningsgrad, ersättningar, avtal och lönevillkor ska ha giltighetstid och dokumenterad källa. Villkorsändringar ska visa vilken löneperiod som påverkas. Anställdas privata data ska endast exponeras för nödvändiga roller.

**Gräns och undantag:** Systemet ska inte ge generella anställningsrättsliga bedömningar utifrån en vald mall.

**Acceptans:** Ändrad månadslön mitt i en period ger en kvalificerad beräkning eller en uttrycklig granskningsspärr.

### DR-PAY-02: Underlag och frånvaro

Tid, frånvaro, semester, förmåner, utlägg och engångsbelopp ska kunna importeras eller registreras med underlagsidentitet och attest. Dubbletter och sena ändringar ska skapa avgränsat arbete.

**Gräns och undantag:** Sjuk- och andra känsliga uppgifter får inte spridas i vanliga bokföringskommentarer eller riskmodeller.

**Acceptans:** Samma tidfil importerad två gånger förändrar inte den fastställda lönen eller antal ersättningsposter.

### DR-PAY-03: Brutto till netto

Löneberäkning ska använda kvalificerade skattetabeller, avgiftsregler, avtalsgrunder och exakta belopp. Varje del ska kunna förklaras genom indata, parameter och avrundning. Resultatet ska innehålla netto, innehållen skatt, arbetsgivaravgifter och bokföringsförslag.

**Gräns och undantag:** Saknad skattetabell får inte ersättas med en typisk procentsats.

**Acceptans:** Oberoende granskat lönefall reproduceras till rätt minsta enhet och visar alla beräkningssteg som produktdata.

### DR-PAY-04: Fastställd körning

En lönekörning ska frysa personer, villkor, beräkningsversion och belopp. Fastställelse, bokföring och betalningsattest ska vara separata handlingar. Godkännare ska se totalsumma och avvikelser från föregående period.

**Gräns och undantag:** Ett godkänt lönebesked innebär inte att lönen har betalats.

**Acceptans:** En förändrad bankmottagare efter fastställd körning kräver betalningsgranskning utan att automatiskt ändra bruttolönen.

### DR-PAY-05: Lönebesked och medarbetarportal

Medarbetaren ska kunna se sina egna lönebesked, underlag som får delas och status på utlägg. Besked ska vara beständiga versionsbundna dokument med säker åtkomst och tydlig rättelsehistorik.

**Gräns och undantag:** E-post ska inte bära okrypterade känsliga lönefiler som standard.

**Acceptans:** En anställd som byter avdelning får inte tillgång till tidigare eller nya kollegors individuella uppgifter.

### DR-PAY-06: Utbetalning och Cash

Payments ska skapa ett separat betalningsuppdrag per nettoutbetalning eller kvalificerad lönebatch. Cash ska inkludera netto, skatteöverföringsbehov och relevanta externa avgifter vid deras faktiska planerade datum.

**Gräns och undantag:** Brutto plus netto plus innehållen skatt får inte summeras som tre separata betalningsbehov.

**Acceptans:** Fastställd lön ersätter periodens uppskattade lönebetalning utan att fördubbla prognosen.

### DR-PAY-07: Korrigering efter betalning

Rättad lön ska bevara ursprunglig beräkning, utbetalning och deklaration. Extra utbetalning, återkrav eller senare justering ska modelleras uttryckligt med avtalad och kvalificerad behandling.

**Gräns och undantag:** Systemet får inte automatiskt dra en tidigare överbetalning från framtida lön utan godkänd grund.

**Acceptans:** En rättelse skapar separata förslag för bokföring, betalning och deklaration med gemensam spårbar länk.

### DR-PAY-08: Semester, pension och försäkring

Tillämpliga semesteråtaganden, pensionspremier och försäkringar ska kunna följas som beräknade kostnader, skulder och externa betalningar. Varje avtal och regelversion måste anges.

**Gräns och undantag:** En upplupen semesterkostnad är inte samma sak som en betalning i nästa prognosvecka.

**Acceptans:** Förändrad pensionspremie slår igenom på kvalificerad betalningsförekomst och kostnad utan att äldre perioder skrivs om.

### DR-PAY-09: Avslut och specialperioder

Slutlön, extra körning, retroaktiv ersättning och frånvaro över periodgräns ska behandlas som särskilda sammanhängande resor. Ej stödda kombinationer ska kunna exporteras för expertberäkning.

**Gräns och undantag:** Anställningsavslut får inte radera korttransaktioner, återbetalningar eller lönehistorik.

**Acceptans:** En avslutad anställd kan få en efterföljande tillåten korrigering utan återställd generell produktåtkomst.

### DR-PAY-10: Arbetsgivarkontroller

Payroll ska ge avstämning mellan körning, bokförda löneskulder, utbetalningar och rapporterade individuppgifter. Differenser ska fördelas på identifierade personer och poster endast för behörig lönefunktion.

**Gräns och undantag:** En total som stämmer döljer inte en omkastning mellan två mottagare.

**Acceptans:** Två löner med samma belopp men fel mottagarallokering ger en blockerande kontroll.

### DR-PAY-11: Ingen personalprofilering

Modeller får hjälpa till med underlag och begriplig löneförklaring men ska inte bedöma arbetsprestation, rekrytering, befordran eller uppsägning. Drastic Risk ska endast få de aggregerade löneåtaganden som behövs för bolagets kvalificerade ekonomiska ändamål.

**Gräns och undantag:** Personliga beteende- eller hälsodata får inte bli kreditvariabler för bolaget av bekvämlighet.

**Acceptans:** En riskexport innehåller kvalificerad lönekostnad och betalningsåtagande men inga diagnoser eller individuella prestationsetiketter.


<a id="chapter-11"></a>

## 11. Inköp, leverantörsskulder och utlägg

**Första leveransnivå:** ES-1 till ES-2. **Ändamål:** Göra hela utgiftskedjan hanterbar, från ett beslutat köp till en avstämd betalning.

**Huvudresa:** Köpbehov → beställning eller avtal → leverans → faktura → granskning → betalning → avstämning.

**Ägda begrepp:** Purchase commitment, purchase order, receipt, supplier invoice, expense claim, supplier credit och payment request.

### DR-AP-01: Inköpsåtaganden

Godkända beställningar och löpande avtal ska kunna skapa uppskattade ekonomiska åtaganden före faktura. Belopp, valuta, leveransperiod och förväntad betalning ska kunna revideras. Ägaren ska se hur åtagandet påverkar budget och Cash.

**Gräns och undantag:** En order är inte en bokförd leverantörsskuld eller en genomförd betalning.

**Acceptans:** När fakturan anländer ersätts rätt prognosförekomst och resterande ej fakturerad del behålls.

### DR-AP-02: En dokumentinkorg

Fakturor, kvitton, kreditnotor och avtalsunderlag ska kunna tas emot genom uppladdning, e-post, API och kvalificerad e-faktura. Original och transportmetadata ska bevaras. Extraherade fält ska länka till underlaget och mänskliga rättelser.

**Gräns och undantag:** Ett e-postmeddelande med betalningsinstruktioner är inte en betrodd kontoändring.

**Acceptans:** Samma faktura mottagen via två kanaler skapar ett granskat sammanslagningserbjudande i stället för två automatiska betalningar.

### DR-AP-03: Beställning, leverans och faktura

När kunden använder inköpsorder ska matchning kunna jämföra beställd kvantitet, mottagen leverans och fakturerat belopp. Tillåtna differenser och godkännanderoller ska vara policybara.

**Gräns och undantag:** En lyckad trevägsmatchning ersätter inte skattebedömning eller bankattest.

**Acceptans:** En delvis levererad order blockerar endast den berörda fakturadelen enligt godkänd policy och bevarar resten.

### DR-AP-04: Leverantör och mottagaruppgifter

Leverantörens juridiska identitet, fakturautställare och betalningsmottagare ska kunna skiljas åt genom dokumenterad relation. Nya eller ändrade bankuppgifter ska verifieras genom en fristående kvalificerad kontroll och bindas till betalningsförslaget.

**Gräns och undantag:** Faktura-PDF, e-post och samma kontaktkanal får inte ensamma bekräfta en ändring som kan vara bedräglig.

**Acceptans:** Byte av IBAN efter granskning invalidiserar gammal betalningsattest och visar tidigare samt ny mottagarversion.

### DR-AP-05: Kostnadsfördelning

En faktura ska kunna fördelas på konton, projekt, kostnadsställen, perioder och tillgångar. Fördelningar ska bevara summan och skattekomponenternas korrekthet. Utfallet ska vara granskningsbart före bokföring.

**Gräns och undantag:** En föreslagen proportionell fördelning får inte ersätta en kvalificerad moms- eller tillgångsbedömning.

**Acceptans:** Tre radfördelningar med öresavrundning summerar exakt till fakturans bokförda nettobelopp och skatt.

### DR-AP-06: Krediter och kvittning

Leverantörskrediter ska länkas till ursprunglig faktura eller separat avräkningsgrund. Kvittning, kontant återbetalning och framtida tillgodohavande ska vara olika vägar med beständigt saldo.

**Gräns och undantag:** En kreditnota innebär inte att pengarna redan återbetalats.

**Acceptans:** En kredit minskar en väntande betalning eller skapar återbetalningsfordran utan att samma belopp räknas två gånger.

### DR-AP-07: Privata utlägg och ersättningar

Ägare och anställda ska kunna lämna in utlägg, ange vem som faktiskt betalade och begära ersättning. Kostnadsgranskning och ersättningsbetalning ska vara separata beslut med samma källkoppling.

**Gräns och undantag:** Kortköp på företagets kort får inte samtidigt ersättas som privat utlägg.

**Acceptans:** Ett redan företagsbetalt kvitto ger ett synligt betalarkonfliktärende vid en ersättningsbegäran.

### DR-AP-08: Förfalloplan och betalningsförslag

Betalningslistan ska gruppera fakturor efter förfallodag, bank, valuta och verifierad mottagare. Förslag ska visa restbelopp, krediter, avtalade rabatter och likviditetseffekt. Val av betalningsdag sparas som ett separat beslut.

**Gräns och undantag:** Likviditetsoptimering får inte tyst skjuta en avtalsenlig förfallodag framåt.

**Acceptans:** En användare kan föreslå senare betalning men ser avtalsavvikelse och kan inte presentera den som leverantörsgodkänd.

### DR-AP-09: Budget och attest

Budget ska kunna begränsa nya åtaganden och kräva extra granskning vid avvikelse. Inköpsattest, kostnadsattest och betalningsattest ska ha separata policyer. Samtidiga förfrågningar ska konsumera tillgänglig budget atomiskt när hård gräns används.

**Gräns och undantag:** Budgetgodkännande är inte likviditet, kredit eller ett banklöfte.

**Acceptans:** Två samtidiga inköp över återstående hårda gräns ger inte två godkända reservationer.

### DR-AP-10: Kostnadsinsikt

Kunden ska kunna analysera leverantörer, återkommande abonnemang, projektkostnader och faktiska besparingsförslag med källor. Dubbla abonnemang eller oväntade prisändringar blir förslag till granskning.

**Gräns och undantag:** Systemet ska inte säga upp avtal automatiskt enbart på grund av låg identifierad användning.

**Acceptans:** En uppmärksammad prisökning visar jämförbara avtalsperioder och kan leda till ett dokumenterat beslut.


<a id="chapter-12"></a>

## 12. Money: Drastic Cash

**Första leveransnivå:** ES-1. **Ändamål:** Visa vad företaget kan förvänta sig att kunna betala, när marginalen blir lägst och varför.

**Huvudresa:** Kvalificera startläge → samla framtida betalningar → kontrollera täckning → beräkna → förklara → jämför scenario med faktiskt utfall.

**Ägda begrepp:** Cash perimeter, observed balance, economic cash event, coverage assessment, assumption, forecast snapshot och scenario.

### DR-CASH-01: Kvalificerat startläge

Varje prognos ska ha ett gemensamt startögonblick och definierade konton. Saldotyp, källa, observationstid och avstämningsstatus ska visas. Olikdaterade saldon behöver en verifierbar brygga innan de summeras som ett aktuellt startläge.

**Gräns och undantag:** Bokfört saldo, bankens bokförda saldo och bankens disponibla saldo är inte samma sak.

**Acceptans:** Ett konto med utdrag från föregående vecka förhindrar en okvalificerad etikett saldo idag för hela bolaget.

### DR-CASH-02: Likviditetsomfattning

Kundens inkluderade pengar ska klassificeras som disponibla, reserverade, spärrade, under överföring eller utanför prognosen. Skattekonto, betalningsförmedlarreserver och krediter ska ha explicita regler.

**Gräns och undantag:** Koncernbolags pengar och privata konton får inte bli automatiskt disponibla medel.

**Acceptans:** En processorreserv visas som ett separat möjligt framtida inflöde enligt verifierat frigivningsvillkor, inte som bankpengar nu.

### DR-CASH-03: En ekonomisk betalning

Faktura, delbetalning, bankhändelse, korttransaktion och bokföring ska kunna beskriva samma flöde utan att skapa flera prognosbidrag. Varje bidrag ska ha ekonomisk identitet, återstående kapacitet och källa till tidsplaceringen.

**Gräns och undantag:** Liknande belopp och datum är inte tillräckligt för att slå ihop flöden.

**Acceptans:** En faktura på 50 000 med 20 000 redan i startsaldot ger 30 000 i framtida inflöde.

### DR-CASH-04: Kända poster och förväntat verksamhetsflöde

Cash ska skilja avtalsbundna betalningar, kvalificerade uppskattningar och rena scenarier. Återkommande lön, hyra och drift kan fylla framtiden enligt tydliga antaganden. En faktisk händelse ska ersätta sin uppskattade förekomst.

**Gräns och undantag:** Tom reskontra för månad tre innebär inte noll kostnader den månaden.

**Acceptans:** En framtida månad utan kvalificerad löneuppskattning markeras som ofullständig även om inga löneposter finns.

### DR-CASH-05: Daglig beräkning och horisonter

Kärnan ska beräkna per dag och stödja 30 dagar, 90 dagar och 13 veckor. Vecko- och månadsvisning är aggregeringar av samma underlag. Förfallodag, förväntad betalningsdag och observerad betalningsdag ska hållas isär.

**Gräns och undantag:** 13 veckor får inte etiketteras 90 dagar; exakt datumintervall ska visas.

**Acceptans:** Byte mellan dag- och veckovy förändrar inte horisontens lägsta dagliga saldo.

### DR-CASH-06: Minsta saldo och buffert

Cash ska visa lägsta prognostiserade saldo, datum och likviditetsutrymme efter vald buffert. Startsaldot ingår i minimiunderlaget. Negativa värden visas som underskott. Scenariot ska visa hur mycket extra utbetalning idag som ryms under de antaganden som används.

**Gräns och undantag:** Detta är inte utdelningsutrymme, solvensbedömning eller en garanti för att pengar kan spenderas.

**Acceptans:** Positivt slutsaldo men negativt saldo före en kundbetalning ger en tydlig likviditetsvarning.

### DR-CASH-07: Lön och skatter utan dubbelräkning

Lönens nettobelopp, skattens finansieringsbehov och kvalificerade avgifter ska hamna på sina egna betalningsdatum. Skattekontots befintliga saldo och planerade överföringar ska beaktas. Samma skatt får inte ingå som både full skuld och extra överföring.

**Gräns och undantag:** Bruttolön och nettolön får inte dras parallellt för samma löneförekomst.

**Acceptans:** En fastställd körning ersätter uppskattningen och ändrar bara skillnaden i den återstående prognosen.

### DR-CASH-08: Betalningsosäkerhet

Förväntad kundbetalning ska ha källa: avtalad dag, kundlöfte, kvalificerad historik eller användarantagande. Förfallna fakturor får inte automatiskt flyttas till idag. Osäkra inflöden ska kunna exkluderas i ett försiktigt scenario.

**Gräns och undantag:** En statistisk förväntan är inte ett säkert belopp eller ett bindande betalningslöfte.

**Acceptans:** En förfallen faktura utan ny bedömning visas som osäker tidsplacering och påverkar täckningsbeskedet.

### DR-CASH-09: Kredit och finansierade fakturor

Utnyttjad kredit, outnyttjad limit, finansieringsutbetalning och framtida återbetalning ska vara separata poster. En finansierad fakturas framtida betalning ska följa avtalad betalningsmottagare och avräkning.

**Gräns och undantag:** En preliminär kreditmöjlighet räknas inte som disponibla pengar.

**Acceptans:** Ett fakturaförskott ökar likviditet en gång och kundbetalningen skapar inte ett andra fullt inflöde till låntagaren.

### DR-CASH-10: Valutaflöden

Varje flöde behåller sin valuta och kontraktsbelopp. Omräknade prognoser ska visa kurskälla, datum, spread och scenariovillkor. En bokföringsmässig omvärdering ska inte skapa en kassahändelse.

**Gräns och undantag:** En indikativ kurs är inte en accepterad växlingsaffär.

**Acceptans:** Ett EUR-konto och en EUR-skuld kan analyseras i originalvaluta utan en artificiell SEK-växling.

### DR-CASH-11: Täckning och ofullständiga resultat

Täckning ska bedömas per källa, åtagandefamilj och tidsintervall. Ett delresultat får visas med tydlig begränsning. Nyckeltalet likviditetsutrymme ska märkas villkorat eller utebli när en materiell okänd post gör siffran missvisande.

**Gräns och undantag:** Okända belopp får aldrig normaliseras till noll enbart för att beräkningen ska slutföras.

**Acceptans:** En okänd kommande skattebetalning ger synligt informationsbehov och ingen ovillkorlig grön spendera-siffra.

### DR-CASH-12: Scenarier

Användaren ska kunna flytta betalningar, lägga till investering, ändra försäljningsantagande och pröva finansiering i en separat scenarioyta. Baslinje och skillnader ska visas med samma monetära modell.

**Gräns och undantag:** Scenarioändringar får inte skriva om fakturor, avtal eller godkända betalningsuppdrag.

**Acceptans:** En två veckor senare kundbetalning ändrar prognosen men lämnar ursprungligt förfallodatum oförändrat.

### DR-CASH-13: Historiska prognoser och utfall

Varje sparad prognos ska frysa vad som var känt, datamedlemskap, antaganden och beräkningsversion. Utvärdering ska jämföra med faktiskt observerat utfall utan att ändra den historiska prognosen. Fel ska delas upp i belopp, tid och saknad källa.

**Gräns och undantag:** Senare tillgängliga fakturor får inte smygas in i en äldre prognos för att förbättra träffsäkerheten.

**Acceptans:** En prognos skapad före en ny order visar fortsatt sitt ursprungliga underlag i historisk jämförelse.

### DR-CASH-14: Beslut och uppföljning

Cash ska kunna skapa ett arbetsärende för att kontakta en kund, granska en utgift eller utvärdera finansiering. Förklaringen ska ange vilka poster som driver risken och vilken åtgärd användaren själv behöver godkänna.

**Gräns och undantag:** Prognosmotorn får inte initiera en betalning eller låneansökan utan rätt mandat.

**Acceptans:** Klick på en likviditetsrisk öppnar de relevanta objekten och ett scenario, inte en automatiskt skickad kreditansökan.


<a id="chapter-13"></a>

## 13. Money: Treasury

**Första leveransnivå:** ES-3 till ES-5. **Ändamål:** Orkestrera företagets faktiska likviditet och motpartsexponering inom godkända regler.

**Huvudresa:** Se konto- och valutaexponering → välj likviditetspolicy → simulera åtgärd → godkänn → genomför via Payments eller reglerad leverantör → stäm av.

**Ägda begrepp:** Treasury policy, liquidity buffer, account allocation, transfer plan, FX quote, counterparty limit och sweep mandate.

### DR-TRE-01: Kontokatalog och juridisk relation

Varje bank-, betal- eller e-pengakonto ska beskriva kontohavare, tjänsteleverantör, kontotyp, valuta, åtkomst och begränsningar. Kunden ska kunna skilja insättning, e-pengar, depåtillgång och ren intern budget.

**Gräns och undantag:** Ett marknadsnamn som konto får inte dölja vem som håller pengarna eller vilket skydd som faktiskt gäller.

**Acceptans:** Kontodetaljer visar korrekt leverantör och produktvillkor utan att tillskriva alla produkter insättningsgaranti.

### DR-TRE-02: Likviditetspolicy

Kunden ska kunna fastställa miniminivåer, betalningsprioriteringar, buffertar, koncentrationsgränser och tillåtna destinationer. Systemet ska simulera policyn mot kvalificerade Cash-scenarier innan aktivering.

**Gräns och undantag:** Maximal ränta får inte prioriteras framför förfallande skyldigheter eller kundens riskgränser.

**Acceptans:** Ett förslag att flytta pengar stoppas om återstående saldo bryter den valda bufferten under prognoshorisonten.

### DR-TRE-03: Reserver och verkliga medel

En intern reservation för moms eller lön ska visas som en budgetallokering tills pengar faktiskt flyttats eller spärrats. Kunden ska kunna se både faktisk bankfördelning och planerad användning.

**Gräns och undantag:** En virtuell pott ger inte juridiskt separerade medel eller ett nytt bankkonto.

**Acceptans:** Att flytta 20 000 till potten moms ändrar inte banksaldot eller skapar en ny banktransaktion.

### DR-TRE-04: Överföringsplaner

Treasury ska kunna planera överföringar mellan bolagets konton och finansiera kommande betalningsbatcher. Källkonto, målkonto, valuta, avgift och tillgänglighetstid ska bindas till planen.

**Gräns och undantag:** Ett internt kontoägarsamband är inte bevis för att överföringen är momentan eller avgiftsfri.

**Acceptans:** En överföring med en dags fördröjning syns som pengar under överföring och räknas inte på båda kontona.

### DR-TRE-05: Automatiska sweeps

Stående regler får flytta överskott endast inom uttryckligt mandat med tillåtna konton, beloppsgränser, kumulativ budget, tidsfönster och återkallelse. Förutsättningar ska kontrolleras på nytt vid varje faktisk handling.

**Gräns och undantag:** Tidigare godkänt saldo eller gårdagens prognos får inte ensamt utlösa en ny överföring.

**Acceptans:** Två samtidiga sweep-körningar konsumerar samma budgetkontroll och kan inte tömma kontot dubbelt.

### DR-TRE-06: Valutaväxling

Systemet ska visa indikativa kurser separat från bindande offerter. En accepterad affär ska bära offerthash, köpt/såld valuta, belopp, spread, avgift, giltighet och avräkning. Utgången offert ska kräva nytt godkännande där villkoren ändras.

**Gräns och undantag:** Ingen automatisk acceptans av sämre kurs över kundens uttryckliga slippagelimit.

**Acceptans:** En förfallen offert skapar inte en växling till aktuell okänd kurs vid återförsök.

### DR-TRE-07: Motpartsexponering

Treasury ska kunna visa likviditet och tillgodohavanden per bank, partner, kontotyp och juridisk motpart. Gränser ska mäta vald ekonomisk exponering, inte bara användargränssnittets konton.

**Gräns och undantag:** Flera varumärken får inte antas vara oberoende riskmotparter.

**Acceptans:** En koncentrationsvarning kan förklaras med juridisk motpart och underliggande kontosaldon.

### DR-TRE-08: Ränte- och placeringsalternativ

Jämförelser ska visa bindning, åtkomsttid, avgifter, valuta, motpart och produktspecifikt skydd. Investeringar och rådgivning får bara aktiveras efter egen rollklassificering och kvalificerat partnerupplägg.

**Gräns och undantag:** Målbilden kräver inte att Drastic erbjuder värdepappersplacering eller individuell investeringsrådgivning.

**Acceptans:** En likviditetsplan kan använda ett kvalificerat bankkonto utan att automatiskt erbjuda en fond som likvärdig kontantposition.

### DR-TRE-09: Koncernlikviditet

Cash pooling och intercompany-finansiering ska kräva dokumenterade avtal, bolagsmandat, valutor och bokföringsbehandling i varje juridisk person. Rapportering ska visa både disponibla och rättsligt begränsade belopp.

**Gräns och undantag:** Koncernsaldo är inte moderbolagets fria kassa.

**Acceptans:** En intern överföring kan bokföras i två separata böcker med avstämningsärende vid försenat motpartsutfall.

### DR-TRE-10: Förfallostruktur och stresstest

Treasury ska visa bankmedels åtkomst, kreditförfall, leverantörsskulder och skattebehov i en tidsstruktur. Stress ska kunna pröva partneravbrott, försenade kundbetalningar och valutaförändring.

**Gräns och undantag:** Stressresultat är scenarier, inte sannolikhetsbedömningar utan kalibrering.

**Acceptans:** Ett tre dagars uttagsstopp hos en partner visar vilka godkända betalningar som saknar finansiering.

### DR-TRE-11: Genomförande och redovisning

Alla verkliga rörelser ska överlämnas till Payments eller den kvalificerade leverantörens affärsägare. Treasury äger beslut och policy, inte en alternativ saldoauktoritet. Ränta och avgifter bokförs efter rätt observerat underlag.

**Gräns och undantag:** Ett optimeringsförslag får inte direkt skriva en bankverifikation som om överföringen skett.

**Acceptans:** Misslyckad sweep lämnar faktisk bank oförändrad och skapar ett åtgärdsärende i stället för fiktiv likviditet på målkontot.


<a id="chapter-14"></a>

## 14. Money: Payments

**Första leveransnivå:** ES-3. **Ändamål:** Genomföra rätt betalning till rätt mottagare med ett återfinnbart resultat även när nätverk och leverantörer fallerar.

**Huvudresa:** Betalningsbehov → mottagarkontroll → finansieringskontroll → godkännande → leverantörsinlämning → extern avveckling → bokföring och avstämning.

**Ägda begrepp:** Payment intent, beneficiary revision, payment approval, execution attempt, provider reference, settlement och return.

### DR-PMT-01: Betalningsavsikt

Alla utbetalande produkter ska skapa en gemensam betalningsavsikt med bolag, juridisk betalare, källa, mottagare, belopp, valuta, betalningsdag och affärsreferens. En avsikt ska kunna representera leverantörsbetalning, lön, skatt, återbetalning eller låneutbetalning.

**Gräns och undantag:** Ett internt förslag till betalning är inte en instruktion som banken redan tagit emot.

**Acceptans:** Samma invoice-payment-behov från AP och en agent återfinns som samma avsikt eller en uttrycklig konflikt.

### DR-PMT-02: Behörighet och tjänsteroll

Produktaktivering ska binda kvalificerad leverantör, land, valuta, tjänsteroll och betalningsmetod. Rätt att förbereda, signera och skicka ska kontrolleras separat. Reglerad roll ska vara beslutad före lansering. [E02]

**Gräns och undantag:** En allmän FI-registrering eller ett leverantörs-API ger inte automatisk rätt att tillhandahålla betalningstjänsten.

**Acceptans:** En tekniskt fungerande integration kan vara synlig i test men blockeras i produktion när tjänsterollen saknar godkännande.

### DR-PMT-03: Mottagarbindning

Godkännandet ska binda mottagarens granskade juridiska relation och kontoversion. Ny mottagare och kontoändring ska kunna kräva extra oberoende granskning. Mottagarkontroller ska visa resultatets källa och begränsning.

**Gräns och undantag:** Kontrollsiffergodkänt IBAN är inte bevis för rätt kontohavare.

**Acceptans:** Manipulerad mottagare mellan granskning och exekvering leder till vägran före extern anropning.

### DR-PMT-04: Saldo och reservationskontroll

Tillgängliga medel, interna budgetreservationer och redan inskickade uppdrag ska kontrolleras enligt kontots faktiska leverantörsmodell. Lokal reservation ska förhindra att samma mandat eller lokalt planerade finansiering konsumeras flera gånger.

**Gräns och undantag:** En lokal reservation garanterar inte att externa uttag på banken inte förändrar disponibelt saldo.

**Acceptans:** Två uppdrag om 60 000 mot 100 000 tillåten lokal betalningskapacitet kan inte båda reserveras.

### DR-PMT-05: Exakt attest och autentisering

Belopp, valuta, avgiftstak, mottagare, källkonto och senaste genomförandedag ska omfattas av attesten. Där leverantören kräver stark autentisering ska kunden genomföra den i kvalificerat flöde. Signeringens resultat ska återkopplas till exakt avsikt.

**Gräns och undantag:** Bokföringsattest eller godkänd budget ersätter inte betalningsattest.

**Acceptans:** En signering för ett uppdrag kan inte återanvändas för ett annat belopp eller en annan mottagare.

### DR-PMT-06: Beständig inlämning

Innan en extern sidoeffekt kan inträffa ska avsikt, godkännande och exekveringsidentitet vara beständigt registrerade. Leverantörsanrop ska ske utanför huvudbokens transaktion med en dokumenterad idempotens- och återhämtningsmodell.

**Gräns och undantag:** En leverantör som saknar säker återidentifiering kräver ett kvalificerat manuellt eller alternativt flöde.

**Acceptans:** Avbrott efter leverantörsanrop men före lokalt svar lämnar tillräcklig referens för att utreda samma uppdrag.

### DR-PMT-07: Okänt utfall

Okänt ska vara ett eget finansiellt tillstånd. Systemet ska utreda via leverantörsreferens, statusläsning, avräkning och kontoutdrag. Den ekonomiska avsikten ska förbli spärrad mot ny sidoeffekt tills utfallet kvalificerats.

**Gräns och undantag:** Automatisk fallback till en annan bank eller partner får inte ske bara för att första anropet tog för lång tid.

**Acceptans:** En mottagen betalning med tappat svar leder inte till dubbelt genomförande hos en reservleverantör.

### DR-PMT-08: Leverantörsmeddelanden

Webhooks ska autentiseras, tids- och återuppspelningskontrolleras enligt leverantörens protokoll och kopplas till rätt scope. Äldre observationer ska bevaras men får inte skriva över ett senare styrkt tillstånd. Periodisk avstämning ska fånga uteblivna meddelanden.

**Gräns och undantag:** En webhook är en observation, inte obegränsad behörighet att bokföra valfritt belopp.

**Acceptans:** Duplicerade och omkastade meddelanden skapar en avveckling och en tydlig observationshistorik.

### DR-PMT-09: Betalningsdag och rail

Inhemska överföringar, autogiro, SEPA, internationella betalningar och andra betalningsmetoder ska aktiveras genom separata kvalificerade profiler. Format, klipptid, kalender, referenslängd, signering och statusmappning ska versionsbindas.

**Gräns och undantag:** Ett generiskt fält requestedDate får inte garantera mottagarens tillgänglighetsdag.

**Acceptans:** En betalning efter klipptid visar ny möjlig genomförandedag och kräver ny bedömning när avtalsvillkoren påverkas.

### DR-PMT-10: Batcher med partiella utfall

Batcher ska bevara varje betalningsavsikt och dess separata resultat. Kunden ska kunna filtrera godkänd, inskickad, avvecklad, returnerad och okänd. Ny batch får bara inkludera sådant som säkert kan utföras igen.

**Gräns och undantag:** Ett lyckat filuppladdningskvitto är inte bevis för att alla rader betalats.

**Acceptans:** En lönebatch med nio avvecklade och ett avvisat uppdrag kan rättas utan nio nya löneutbetalningar.

### DR-PMT-11: Avgifter och växling

Betalningsprofilen ska specificera huvudbelopp, avgiftsbärare, förväntat mottagarbelopp och valutavillkor där känt. Slutligt utfall ska bevara verkliga avdrag och växling utan att skriva om den godkända avsikten.

**Gräns och undantag:** En nettoutbetalning från partner ska inte bokföras som fakturans brutto utan avräkning.

**Acceptans:** Kundfordran kan regleras med separat avgiftskostnad och kontrollerad differens när faktisk mottagen summa skiljer sig.

### DR-PMT-12: Återkallelse och returnering

Begäran att stoppa ett skickat uppdrag ska ha eget tillstånd tills leverantören bekräftat resultat. Returnering, återbetalning och chargeback ska vara nya identifierade ekonomiska händelser med hänvisning till originalet.

**Gräns och undantag:** En användare som klickar avbryt får inte omedelbart se att externa pengar inte längre kan röra sig.

**Acceptans:** Ett uppdrag som avvecklas trots sen stopbegäran förblir avvecklat och får en separat möjlig återbetalningsresa.

### DR-PMT-13: Matchning mot verkliga pengar

Avvecklad status ska kvalificeras per leverantör och följas av avstämning mellan uppdrag, leverantörsavräkning och bank-/kontorörelse. Bokföring använder korrekt affärsgrund och bankhändelse utan dubbelt effektuttag.

**Gräns och undantag:** Bankbokföring får inte skapas två gånger från både webhook och senare kontoutdrag.

**Acceptans:** Samma betalning kan följas från faktura till avsikt, partnerreferens, bankrad, verifikation och avstämning.

### DR-PMT-14: Inkommande betalningar

Kundinbetalning ska kunna matchas via verifierad referens, virtuellt konto eller kvalificerat betalningsunderlag. Delbelopp, överbetalning, oidentifierad betalare och betalning för flera fakturor ska få egna förklarbara allokeringar.

**Gräns och undantag:** En oidentifierad inbetalning får inte automatiskt räknas som ny försäljning.

**Acceptans:** En gemensam inbetalning för två fakturor kan fördelas med exakt kvarvarande oförklarad del.

### DR-PMT-15: Felsäker drift

Betalningsköer ska kunna pausas per partner, land, bolag eller risktyp utan att stoppa läsning och återhämtning. Pågående uppdrag ska fortfarande följas. Återstart ska kräva aktuell auktoritet och säkert utfall för berörda kommandon.

**Gräns och undantag:** Driftstopp ska inte följas av en blind återuppspelning av alla gamla betalningsmeddelanden.

**Acceptans:** Efter incident kan operatören återställa observationer och fortsätta endast ostartade godkända uppdrag.

### DR-PMT-16: Återkommande betalning och autogiro

Mandat för återkommande betalning ska bära betalare, mottagare, omfattning och uppsägningsvillkor. En kommersiell prenumeration och ett betalningsmandat ska kunna sluta vid olika tidpunkter utan att skapa oklar debiteringsrätt.

**Gräns och undantag:** Ett aktivt abonnemang ger inte automatiskt ett giltigt autogiromedgivande.

**Acceptans:** Återkallat betalningsmandat stoppar nya uttag men bevarar faktura och avtalad fordran med en alternativ betalningsväg.


<a id="chapter-15"></a>

## 15. Money: Cards och kortutgifter

**Första leveransnivå:** ES-3. **Ändamål:** Ge företag kontrollerade kortköp med korrekt hantering från auktorisation till slutlig avräkning.

**Huvudresa:** Fastställ kortpolicy → utfärda via partner → auktorisera köp → hämta underlag → avräkna → granska kostnad → hantera reklamation.

**Ägda begrepp:** Card programme, card token, cardholder, authorisation, hold, presentment, refund och dispute.

### DR-CARD-01: Produkt och utgivare

Varje kortprogram ska beskriva utgivare, debit/charge/credit-modell, finansieringskonto, ansvar, avgifter, geografisk täckning och användarvillkor. Kortinnehavare ska ha ett uttryckligt bolagsmandat.

**Gräns och undantag:** Ett kort med månatlig faktura får inte beskrivas som debit om en kreditrelation faktiskt finns.

**Acceptans:** Kunden kan se vem som är kortutgivare och vem som bär obetalda kortskulder.

### DR-CARD-02: Fysiska och virtuella kort

Utgivning, aktivering, leverans, ersättningskort och avslut ska ske med leverantörens verifierade tillstånd. Virtuella kort kan begränsas till leverantör, inköp eller återkommande ändamål där programmet stödjer det.

**Gräns och undantag:** Ett lokalt kortobjekt betyder inte att utgivaren har skapat ett användbart kort.

**Acceptans:** Ett skapat men ännu ej aktivt kort visas inte som tillgängligt för köp.

### DR-CARD-03: Köpgränser och samtidighet

Gränser per kort, anställd, team, valuta och tidsfönster ska kunna kombineras med godkända köpbudgetar. Auktorisationer ska reservera kapacitet och hänvisa till rätt policyversion.

**Gräns och undantag:** Två kort får inte kringgå en gemensam teamgräns genom samtidiga köp.

**Acceptans:** Samtidiga auktorisationer testas mot en gemensam atomisk gräns inom den auktoritativa utgivningsmodellen.

### DR-CARD-04: Reservation och avräkning

Auktorisation, inkrementell auktorisation, delvis återföring, slutlig presentment och frigjord reservation ska vara separata poster. Systemet ska kunna hantera flera presentments enligt programregler och sena avräkningar.

**Gräns och undantag:** Förfallen reservation bevisar inte att en senare avräkning är omöjlig.

**Acceptans:** Reservation 1 000, återföring 300 och avräkning 650 ger 50 i återstående frigörelse och 650 i faktiskt köp.

### DR-CARD-05: Avvikande köpbelopp

Hotell, drivmedel, dricks och valutaavvikelser ska följa kvalificerade kortregler. Skillnaden mellan reserverat och slutligt belopp ska förklaras för kunden och uppdatera budget samt bokföringsunderlag.

**Gräns och undantag:** En tidigare godkänd reservation får inte låtsas vara en exakt godkänd slutkostnad när leverantören tillåter justering.

**Acceptans:** Ett slutbelopp över den ursprungliga reservationen blir korrekt avräkning och ett policyärende där så krävs.

### DR-CARD-06: Kvitto och kostnadsgrund

Kortköp ska kunna samla kvitto, ange affärsändamål och koppla till beställning eller redan registrerad leverantörsfaktura. Systemet ska skilja bank-/kortbevis från det underlag som krävs för redovisning och skatt.

**Gräns och undantag:** Kortavräkning ensam får inte fabricera avdragsgill moms.

**Acceptans:** Ett kvitto länkat till redan bokförd leverantörsfaktura skapar inte en andra kostnad.

### DR-CARD-07: Återbetalningar

Refund ska ha egen identitet och koppling till köp eller en dokumenterad fristående återbetalning. Återbetalning till ersatt eller avslutat kort ska hanteras enligt utgivarens faktiska kanal och avstämmas till bolaget.

**Gräns och undantag:** Avslutat kort innebär inte att en väntad refund får tappas bort.

**Acceptans:** Köp 650 och senare refund 200 ger netto 450 med oförändrad originalhistorik.

### DR-CARD-08: Reklamationer och chargebacks

Tvister ska ha belopp, skäl, tidsfrister, dokument, ansvarig och leverantörsstatus. Provisorisk kreditering ska skiljas från slutligt vunnen reklamation. Sena motbesked ska kunna återföra provisoriska effekter.

**Gräns och undantag:** Drastic ska inte lova att alla reklamationer ger ersättning eller att en tillfällig kredit är slutgiltig.

**Acceptans:** En förlorad tvist efter provisorisk kreditering skapar tydlig ny skuld utan att originalköpet dupliceras.

### DR-CARD-09: Kortspärr och anställningsavslut

Kunden ska kunna begära spärr snabbt och se utgivarens bekräftelse. Avslutad medarbetare ska förlora nya köprättigheter men historiska köp, refunds och reklamationer ska fortsätta följas.

**Gräns och undantag:** En lokal knappstatus är inte bevis för att offline- eller redan godkända transaktioner inte kan avräknas.

**Acceptans:** Efter spärr nekas nya tillåtlighetsbeslut medan en tidigare auktoriserad presentment hanteras korrekt.

### DR-CARD-10: Valuta och kortavgifter

Korttransaktionen ska bära köpvaluta, avräkningsvaluta, faktisk kurs och avgifter. Kostnad, skuld till utgivare och bankreglering ska ha olika roller när kortmodellen kräver det.

**Gräns och undantag:** Månatlig kortfaktura får inte bokföra om alla redan redovisade kortkostnader.

**Acceptans:** Samlad kortbetalning reglerar kortskulden medan enskilda köp behåller sina konton och underlag.

### DR-CARD-11: Kortdata och tokenisering

Kortnummer och verifieringsuppgifter ska hanteras av kvalificerad utgivare eller kortdatamiljö. Appen ska använda tokens och begränsade visningskomponenter. Loggar, analys och modeller får inte få fullständiga kortuppgifter.

**Gräns och undantag:** Outsourcing är inte bevis för att alla PCI-relaterade skyldigheter försvinner. [E11]

**Acceptans:** Sökning i applikationsloggar och agentunderlag efter testkortdata hittar inga otillåtna PAN- eller CVV-värden.

### DR-CARD-12: Utgivaravbrott och programavslut

Drastic ska dokumentera hur auktorisation, spärr, återbetalning och historik fungerar vid partneravbrott eller avslutat program. Ett nytt kortprogram kräver ny produkt- och kundmigrering med bevarad gammal avräkning.

**Gräns och undantag:** Kort kan inte transparent flyttas mellan utgivare som om token och mandat vore portabla.

**Acceptans:** Programbyte lämnar gamla tvister hos rätt ansvarig och nya köp på den nya utgivaren utan historikförlust.


<a id="chapter-16"></a>

## 16. Revenue: Billing och kommersiella avtal

**Första leveransnivå:** ES-2. **Ändamål:** Översätta avtal och faktisk leverans eller användning till rätt debitering utan att blanda faktura med intäktsredovisning.

**Huvudresa:** Offert → accepterat avtal → prisrevision och faktureringsplan → kvalificerat användningsunderlag → fakturautkast → utgivning → betalning och periodisering.

**Ägda begrepp:** Product, price version, quote, subscription, usage event, billing period, charge component och billing coverage.

### DR-BILL-01: Produkt- och priskatalog

Katalogen ska stödja engångsbelopp, återkommande belopp, kvantitetsbaserat pris och kvalificerade användningsmodeller. Pris, valuta, skatteklassificering och giltighet ska versionsbindas. Kundspecifika villkor ska vara spårbara avtal, inte överstyrningar utan historia.

**Gräns och undantag:** Ett katalogpris är inte ett godkänt kundavtal.

**Acceptans:** Prisändring i katalogen ändrar inte en redan accepterad offert eller historisk faktura.

### DR-BILL-02: Offerter och avtal

Offert ska kunna accepteras med dokumenterade villkor, kundidentitet och giltighetsgräns. Acceptans ska skapa exakt överenskommet åtagande och faktureringsplan. Orderändring ska visa ekonomisk skillnad.

**Gräns och undantag:** Elektronisk acceptans ersätter inte kontroll av vem som har rätt att binda kunden i känsliga avtal.

**Acceptans:** Accepterad offert kan omvandlas till order och deldebiteringar utan att totalsumman konsumeras mer än en gång.

### DR-BILL-03: Återkommande fakturering

Prenumerationer ska ha beständig cykelidentitet oberoende av mallrevision. Paus, återupptagning, slut och ändrad ankardag ska vara explicit historik. Redan materialiserade eller fakturerade cykler får inte återidentifieras.

**Gräns och undantag:** Ett ändrat mall-ID får inte skapa en andra faktura för samma avtalsperiod.

**Acceptans:** Retry av periodgenerering efter prisändring återfinner samma redan debiterade cykel.

### DR-BILL-04: Användningsmätning

Usage-händelser ska bära kund, resurs, enhet, tid, källidentitet och rättelserelation. Systemet ska kunna redovisa sen rapportering, dubbletter och negativa rättelser inom en kvalificerad modell.

**Gräns och undantag:** Saknade usage-data ska inte bli noll utan en uttrycklig täckningsbedömning.

**Acceptans:** Dubbletter påverkar inte debiterbar kvantitet och sen usage hamnar i en synlig tilläggs- eller nästa-periodsbehandling.

### DR-BILL-05: Prisberäkning och trappor

Prismotorn ska skilja volympris från trappstegspris och ange inkluderade enheter, minimibelopp, tak och avrundning. Varje debiteringsrad ska kunna reproduceras från fryst prisversion och usage-mängd.

**Gräns och undantag:** Texten upp till eller från får inte användas utan exakt definierad tröskelsemantik.

**Acceptans:** En kund vid exakt prisgräns får samma belopp vid återberäkning och ett oberoende handräknat jämförelsefall.

### DR-BILL-06: Perioddelning och proratering

Proratering ska ange kalendergrund, tidszon, inkluderade gränser och avrundningsfördelning. Uppgradering eller nedgradering mitt i period ska producera explicit kredit och ny debitering enligt avtalet.

**Gräns och undantag:** En teknisk månad på 30 dagar får inte antas när avtalet anger kalenderdagar.

**Acceptans:** Tre delperioder bevarar totalen inklusive öresrest och samma dag faktureras inte två gånger.

### DR-BILL-07: Rabatter och krediter

Rabatt ska ha kvalificeringsregel, varaktighet, tillämpliga komponenter och maxanvändning. Krediter ska skiljas mellan marknadsrabatt, prisrättelse, återbetalning och återstående kundtillgodohavande.

**Gräns och undantag:** En rabattkod får inte retroaktivt ändra redan utgivna dokument.

**Acceptans:** Avslutat introduktionspris återgår till rätt avtalade prisversion med förhandsvisad nästa debitering.

### DR-BILL-08: Förskott och användningssaldon

Förbetalda tjänstevolymer och kundförskott ska ha tydliga avtalsrättigheter, förbrukning och redovisningsprofil. Köp av tjänstepaket, återbetalningsbara pengar och e-pengaliknande funktioner ska klassificeras separat.

**Gräns och undantag:** Ett fält wallet balance får inte introducera oklassificerad förvaring eller e-pengautgivning. [E03]

**Acceptans:** Förbrukning av förbetalda enheter ändrar rätt åtagande utan att skapa ny kontant inbetalning.

### DR-BILL-09: Faktureringskontroll

Billing ska förbereda debiteringskomponenter och lämna till Invoicing för juridisk utgivning. Komponenternas debiteringskapacitet ska konsumeras atomiskt med den kvalificerade utgivningshandlingen.

**Gräns och undantag:** Betalningsretry får aldrig generera en ny kommersiell debitering av samma period.

**Acceptans:** Ett misslyckat kortuttag lämnar en faktura och flera separata försök att betala den.

### DR-BILL-10: Intäktsredovisning

Faktureringsperiod, leveransperiod och redovisad intäkt ska kunna skiljas åt. Avtalets kvalificerade leveransåtaganden ska kunna skapa periodiseringsunderlag till Accounting utan egen parallell resultaträkning.

**Gräns och undantag:** Årsfaktura betald i januari innebär inte att all intäkt måste redovisas i januari.

**Acceptans:** Förutbetald årsavgift kan följas till faktura, betalning, skuld/periodisering och månatlig intäktsfördelning.

### DR-BILL-11: Kundportal

Kunden ska kunna se avtal, kommande debitering, usage-underlag, fakturor, betalningsmetoder och avslutsvillkor inom sin egen relation. Ändringar med ekonomisk effekt ska bekräftas och sparas.

**Gräns och undantag:** Avsluta abonnemang får inte döljas bakom finansierings- eller merförsäljningsflöden.

**Acceptans:** En uppsägning stoppar framtida avtalsenlig debitering men bevarar redan utgivna fakturor och rättelser.

### DR-BILL-12: Kommersiella mätetal

MRR, ARR, churn, expansion och återkommande intäkt ska ha definierade beräkningsregler. De ska kunna skiljas från fakturering, kassainbetalningar och redovisad intäkt. Historiska kohorter ska gå att reproducera.

**Gräns och undantag:** Engångsavgifter eller kreditutbetalningar får inte räknas som återkommande intäkt.

**Acceptans:** En årsbetalning förändrar kassa enligt betalningen och MRR enligt avtalet utan att ge tolv gånger högre månatlig intäkt.

### DR-BILL-13: Drastics egen debitering

Plattformens egna abonnemang och transaktionsavgifter ska kunna använda Billing men ligga i Drastics egen bok och kundrelation. Kundens ekonomidata får inte muteras genom plattformens kommersiella backend.

**Gräns och undantag:** Intern superuser får inte skapa avgifter i kundens huvudbok utan samma dokumenterade import- och granskningsväg.

**Acceptans:** En plattformsavgift blir en vanlig verifierbar leverantörsfaktura för kunden och en separat fordran för Drastic.


<a id="chapter-17"></a>

## 17. Accounting: Close, rapportering och årsarbete

**Första leveransnivå:** ES-1 till ES-2. **Ändamål:** Avsluta perioder och år med verifierbara kontroller, användbar överlämning och rätt externa kvitton.

**Huvudresa:** Samla periodens arbete → stäm av → granska uppskattningar → fastställ rapporter → signera eller överlämna → verifiera inlämning → arkivera.

**Ägda begrepp:** Close checklist, control result, financial statement snapshot, review pack, annual-report artifact och filing receipt.

### DR-CLOSE-01: Löpande periodavslut

Periodarbete ska samla källtäckning, bankavstämning, reskontror, skatter, löner, scheman och relevanta externa saldon. Varje kontroll ska ha omfattning, ansvarig, underlag, resultat och återöppningsvillkor.

**Gräns och undantag:** Gröna kontroller för ej berörda områden får inte dölja en tillämplig men ej implementerad kontroll.

**Acceptans:** En period med oidentifierade processorutbetalningar kan inte få komplett avstämningsstatus enbart för att banktotalen stämmer.

### DR-CLOSE-02: Finansiella uppskattningar

Periodisering, nedskrivning, reservering och andra bedömningsposter ska visa metod, antagande, källa och behörig granskare. Reviderad uppskattning ska visa historisk jämförelse och vilka perioder den påverkar.

**Gräns och undantag:** AI får föreslå men inte fabricera affärsfakta för att slutföra ett bokslut.

**Acceptans:** En kundförlustbedömning kan spåras till faktura och dokumenterad bedömning utan att påstå att skulden juridiskt upphört.

### DR-CLOSE-03: Periodlås och återöppning

Tekniskt periodlås, färdig intern granskning och färdig extern rapportering ska vara olika tillstånd. Återöppning ska kräva behörighet och konsekvensanalys för rapporter, ingående saldon och inlämnade versioner.

**Gräns och undantag:** Ett periodlås är inte bevis för ett juridiskt korrekt årsbokslut.

**Acceptans:** En godkänd återöppning skapar en ny kontrollomgång och bevarar tidigare fastställt material.

### DR-CLOSE-04: Årsredovisningsunderlag

Årsarbete ska sammanställa finansiella rapporter, noter, bolagsuppgifter och kvalitativa upplysningar enligt en kvalificerad ramverksversion. Manuell uppgift ska markeras som lämnad av ansvarig och behöva granskning.

**Gräns och undantag:** Frånvaro av data får inte ersättas med påhittad förvaltningsberättelse eller standardpåstående om verksamheten.

**Acceptans:** En obligatorisk upplysning utan källa blockerar fastställelse men inte fortsatt arbete i andra delar.

### DR-CLOSE-05: Skatte- och redovisningsöverlämning

Kunden ska kunna välja egen produktion av kvalificerade årsartefakter eller accepterad överlämning till redovisningspartner. Båda vägarna ska ha tydligt ansvar för deklarationer, signering och inlämning.

**Gräns och undantag:** Hela den första plattformslanseringen ska inte villkoras av att alla tänkbara årsprofiler byggs internt.

**Acceptans:** En extern redovisningspartner kan slutföra året med levererat standardunderlag och återlämna verifierade justeringar.

### DR-CLOSE-06: Format och semantisk validering

SIE, SRU och iXBRL ska använda versionsbundna format och kvalificerade klassificeringar. Validering ska skilja teknisk form, finansiell semantik och bolagstillämplighet. Genererade bytes och validatorversion ska bevaras.

**Gräns och undantag:** Att en fil går att parsa innebär inte att uppgifterna är korrekta eller accepterade av mottagaren.

**Acceptans:** Ett schema-giltigt dokument med fel summering ska fortfarande vägras av den finansiella kontrollen.

### DR-CLOSE-07: Signering och inlämning

Årsartefakt, signerande personer, firmatecknings- eller fastställelsegrund och myndighetskanal ska bindas till rätt dokumentversion. Uppladdning, signering och mottagning ska ha egna kvitton och återhämtningsvägar.

**Gräns och undantag:** En förberedd iXBRL-fil är inte en inlämnad årsredovisning. Bolagsverkets aktuella kanal ska kvalificeras. [E14]

**Acceptans:** Ändrad årsartefakt efter signering kräver nytt kvalificerat signeringsflöde.

### DR-CLOSE-08: Koncernrapportering

Valbar konsolidering ska behålla bolagens egna rapporter, ägarandelar, valutaomräkning, elimineringar och koncernjusteringar med explicit metod och scope. Tidsskillnader mellan bolagsstängningar ska visas.

**Gräns och undantag:** En enkel summering av saldon får inte etiketteras fullständig koncernredovisning.

**Acceptans:** Ett internt saldo som inte stämmer mellan bolag ger en synlig differens innan eliminering godkänns.

### DR-CLOSE-09: Arkiv och återställning

Avslutsunderlag, original, beslut, rapportversioner och kvitton ska kunna återställas till läsbart och granskningsbart skick med rätt relationer. Arkivpolicy ska följa tillämplig retention och förvaring. [E13]

**Gräns och undantag:** Backup av en databas utan originalfiler och nycklar uppfyller inte produktens arkivkrav.

**Acceptans:** Ett återställningsprov öppnar en årsrapport och följer bidraget till samma underlagsbytes utan aktiv produktionsdatabas.

### DR-CLOSE-10: Följande år och cutover

Fastställda utgående saldon, öppna poster och schemafortsättning ska ligga till grund för nästa år. Systembyte ska ha verifierad export, importerad kontroll och en bestämd officiell skrivande källa från bryttiden.

**Gräns och undantag:** En godkänd månad stänger inte automatiskt års- eller cutover-gaten.

**Acceptans:** Nästa år öppnas med kontrollerade saldon utan att historiska fakturor eller låneutbetalningar bokförs som nya intäkter.


<a id="chapter-18"></a>

## 18. Revenue: Invoicing och kundreskontra

**Första leveransnivå:** ES-1 till ES-2. **Ändamål:** Ge kunden en komplett fakturalivscykel där juridiskt dokument, leverans, fordran och betalning inte blandas ihop.

**Huvudresa:** Utkast från avtal eller arbete → granska → ge ut → leverera → följ betalning → rätta eller kreditera → avsluta.

**Ägda begrepp:** Invoice draft, legal invoice, invoice line, tax treatment, credit note, delivery attempt och receivable.

### DR-INV-01: Fakturautkast

Utkast ska kunna skapas från Billing, order, projektunderlag eller direkt registrering. Kunden ska se säljare, köpare, rader, leveransperiod, valuta, betalningsvillkor och skatt i ett sammanhängande dokument.

**Gräns och undantag:** Ett sparat utkast ska inte konsumera juridiskt fakturanummer eller påstå att en fordran är utgiven.

**Acceptans:** Utkast kan ändras och återupptas utan att generera flera fakturor för samma avtalade komponent.

### DR-INV-02: Kvalificerad utgivning

Utgivning ska verifiera den aktuella dokumentprofilens obligatoriska uppgifter, skattebehandling, mottagare och debiteringskapacitet. Utgiven revision och nummer ska vara beständiga. Accounting får rätt underlag genom sin egen operation.

**Gräns och undantag:** Ett fält issued=true får inte kringgå bolags- och skatteprofil.

**Acceptans:** Två samtidiga utgivningsförsök konsumerar en debiteringsförekomst och återfinner samma dokument.

### DR-INV-03: Strukturerad e-faktura och PDF

Systemet ska stödja läsbart fakturadokument och kvalificerat strukturerat format när kunden behöver det. Kanalprofil ska ange validering, accesspunkt, mottagaridentifiering och avvikelsehantering. Exakta levererade bytes ska sparas.

**Gräns och undantag:** En PDF är inte samma sak som en strukturerad e-faktura. Krav för offentlig fakturering ska kvalificeras separat. [E15]

**Acceptans:** Mottagaravvisad e-faktura kan rättas genom rätt dokumentprocess utan att originalleveransen raderas.

### DR-INV-04: Leverans och kommunikation

E-post, e-faktura och portal ska ha separata försök och mottagningsobservationer. Fakturans kontaktinformation och historiska leveransadress ska behållas. Oklart leveransutfall ska utredas med samma leveransidentitet.

**Gräns och undantag:** Levererad faktura är inte accepterad prestation eller betalad fordran.

**Acceptans:** Återförsök vid e-postfel skickar samma utgivna dokument och skapar inte ny fakturanumrering.

### DR-INV-05: Krediter och rättelser

Kreditnota ska ange berörd faktura, rader, belopp, skatt och anledning. Delkredit och full kredit ska konsumera rätt återstående rättelsekapacitet. Kreditens finansiella och betalningsmässiga effekt ska följas separat.

**Gräns och undantag:** En ändrad PDF på befintligt fakturanummer är inte en accepterad kreditprocess.

**Acceptans:** En redan delbetald faktura kan krediteras med ett korrekt kvarvarande krav eller återbetalningsbehov.

### DR-INV-06: Betalningsallokering

Reskontran ska stödja delbetalning, flera fakturor per inbetalning, kundtillgodohavande och oidentifierade betalningar. Summor ska följa allokeringshistoriken med rättelser som egna händelser.

**Gräns och undantag:** Banktext eller OCR-referens är en matchningssignal, inte en obegränsad order att bokföra.

**Acceptans:** En inbetalning på 12 000 kan reglera 10 000 i faktura och lämna 2 000 som spårbart tillgodohavande.

### DR-INV-07: Överlåtelse och betalningsinstruktion

Finansierad eller överlåten fordran ska visa faktisk rättighetsinnehavare, vilken mottagare som ska få betalning och dokumenterad underrättelse när tillämpligt. Ändrade instruktioner ska ha separat granskning.

**Gräns och undantag:** Att en faktura är finansieringsbar är inte att den redan har överlåtits.

**Acceptans:** Efter kvalificerad överlåtelse visar portalen rätt betalningsmottagare och Cash räknar inte hela fordran som fritt inflöde till säljaren.

### DR-INV-08: Kundportal och tvist

Mottagaren ska kunna läsa rätt dokument, se betalningsstatus och ställa en tydlig fråga eller bestrida viss del. Åtkomst ska begränsas till den egna kundrelationen. Identiteten bakom känslig ändring ska verifieras.

**Gräns och undantag:** En innehavd fakturalänk får inte ge åtkomst till säljarens bokföring, andra kunder eller riskanalys.

**Acceptans:** Bestridande av en rad ger ett spårbart delbelopp och pausar relevant påminnelseflöde.

### DR-INV-09: Inhemska och internationella profiler

Valuta, språklig presentation, referenser, enheter och skatteuppgifter ska kunna variera enligt kvalificerad fakturaprofil. Den ekonomiska betydelsen ska inte ändras mellan PDF, portal och strukturerat dokument.

**Gräns och undantag:** Översättning får inte skapa en annan betalningsskyldighet eller totalsumma.

**Acceptans:** Samma faktura har identiskt brutto och skatteunderlag i alla genererade kanaler.

### DR-INV-10: Registrens meningsfulla status

Fakturaregistret ska stödja sökning, period, förfall, kund, valuta och statusaxlar för dokument, leverans och betalning. Totalsummor ska ange urval och valuta. Restbelopp ska visas även vid kredit, tvist och överlåtelse.

**Gräns och undantag:** Ett sammanslaget statusfält får inte dölja att en levererad faktura är delbetald och delvis bestridd.

**Acceptans:** Filterval och sidposition bevaras när användaren öppnar faktura, granskar en betalning och återgår.

### DR-INV-11: Avtalad intäkt och avräknad försäljning

Faktura ska länka till Billing-avtal och relevant intäktsperiodisering men behålla egen juridisk identitet. Processoravräkning, marknadsplatsavgift och nettoinsättning ska kunna förklaras som delar av bruttokedjan.

**Gräns och undantag:** Nettoinsatt belopp är inte automatiskt hela försäljningen.

**Acceptans:** Bruttoförsäljning, avgift, refund och reserv kan stämmas av till faktisk utbetalning utan extra intäktspost.


<a id="chapter-19"></a>

## 19. Revenue: Collections och kravhantering

**Första leveransnivå:** ES-2 till ES-4. **Ändamål:** Minska obetalda fordringar med korrekt kundkommunikation, tvistprocess och kvalificerad inkassohandoff.

**Huvudresa:** Upptäck försenad post → kontrollera betalning och tvist → kommunicera → dokumentera löfte eller plan → lämna vidare vid rätt villkor → avsluta eller rätta.

**Ägda begrepp:** Collection case, reminder, dispute, payment promise, payment plan, collection handoff och recovery outcome.

### DR-COL-01: Kontroll före kontakt

Varje utskick ska kontrollera aktuell rest, pågående betalning, kredit, bestridande och tidigare kontakt. Regler ska kunna definieras per kundrelation och fordranstyp med mänskliga undantag.

**Gräns och undantag:** Förfallodag ensam räcker inte när betalning redan är under verifiering.

**Acceptans:** En sent inläst betalning före utskicksögonblicket stoppar en felaktig påminnelse.

### DR-COL-02: Kommunikation och avgifter

Kunden ska kunna skicka tydliga påminnelser med fakturareferens, restbelopp och nästa steg. Avgift eller dröjsmålsränta kräver kvalificerad rättslig och avtalsmässig grund, egen beräkning och spårbar post.

**Gräns och undantag:** En generell påminnelsemall får inte automatiskt lägga till alla tänkbara avgifter.

**Acceptans:** En påminnelse utan tillåten avgiftsgrund skickas utan avgift och med oförändrad huvudfordran.

### DR-COL-03: Bestridda delar

Bestridande ska kunna avse viss fakturarad eller ett belopp. Den bestridda delen ska hållas isär från obestridd rest, kreditbeslut och redovisad fordran. Processen ska dirigera ärendet till rätt handläggare.

**Gräns och undantag:** Bestridande är inte automatisk kreditnota, avskrivning eller bevis på bedrägeri.

**Acceptans:** Fordran 5 000 med 2 000 bestritt visar högst 3 000 som obestridd del för kvalificerat automatiskt påminnelsearbete.

### DR-COL-04: Betalningslöfte

Ett löfte ska registrera vem som lämnade det, datum, belopp och dokumentation. Cash kan använda löftet som ett uttryckligt antagande. Brutet löfte ska skapa nytt granskningsbehov.

**Gräns och undantag:** Betalningslöfte är inte kontant inbetalning eller en garanterad framtida betalning.

**Acceptans:** Löfte om fredag förändrar inte historiskt förfallodatum och ger ingen bokförd bankpost.

### DR-COL-05: Avbetalningsplan

Plan ska ange kvarvarande kapital, tillåtna avgifter, ränta, datum och hur betalningar allokeras. Avtalad plan och en föreslagen plan ska skiljas åt. Ändring ska bevara tidigare villkor och påverka Cash transparent.

**Gräns och undantag:** Programmet får inte anta att kunden accepterat planen för att en länk öppnats.

**Acceptans:** Betalning på en plan kan fördelas enligt godkänt avtal utan att originalfordran dubbleras.

### DR-COL-06: Inkassohandoff

Handoff ska kvalificera behörig inkassopartner eller egen godkänd verksamhet, rätt fordringsägare, dokument, betalningar och tvister. Överlämning, mottagning, handläggning och återtag ska ha egna statusar. [E04]

**Gräns och undantag:** Vanlig SaaS eller FI-registrering för företagskredit ska inte behandlas som generell inkassobehörighet.

**Acceptans:** Ett ofullständigt eller bestridet ärende lämnas inte automatiskt till en kanal som saknar kvalificerad hantering.

### DR-COL-07: Kontaktpolicy och kundskydd

Kontaktfrekvens, kanaler, språk och eskalering ska vara granskningsbara och kunna begränsas. Automation får inte skicka hotfull, vilseledande eller upprepande kommunikation. Kontakt med fel mottagare ska kunna stoppas omedelbart.

**Gräns och undantag:** AI-genererat kravspråk måste hålla sig till godkända fakta och rätt process.

**Acceptans:** En dubblerad köleverans skickar inte ett andra krav och skapar inte ny avgift.

### DR-COL-08: Återvinning och avräkning

Återvunna belopp ska fördelas på fordringsägare, avtalade avgifter, ränta och huvudfordran med underlag från partner. Drastics intäkt ska skiljas från kundens återvunna kapital.

**Gräns och undantag:** Inkassopartnerns nettoöverföring får inte dölja kvarvarande fordran eller egen avgift.

**Acceptans:** En delvis återvinning lämnar rätt skuldrest och en spårbar avgiftskostnad.

### DR-COL-09: Förlust och insolvens

Konstaterad eller befarad förlust ska skapa bedömningsunderlag till Accounting. Betalningskrav, rättsligt anspråk, redovisningsmässig nedskrivning och eventuell momsrättelse ska vara skilda beslut.

**Gräns och undantag:** En riskflagga eller ett missat betalningsdatum räcker inte som bevis för konkurs eller slutlig förlust.

**Acceptans:** Nedskriven faktura som senare betalas kan hanteras med korrekt återföring och verkligt kassaflöde.

### DR-COL-10: Stängning och insyn

Ärendet ska avslutas med exakt grund: betalt, krediterat, rättat, överlämnat eller annan dokumenterad disposition. Kunden ska kunna se tidslinjen och granska onödiga avgifter eller felaktiga kontakter.

**Gräns och undantag:** Ett stängt arbetsärende betyder inte alltid att fordran juridiskt upphört.

**Acceptans:** En återöppning vid returnerad betalning behåller tidigare historik och skapar rätt nytt handlingsbehov.


<a id="chapter-20"></a>

## 20. Revenue: Financing och kundens finansieringsresa

**Första leveransnivå:** ES-4. **Ändamål:** Göra finansiering begriplig och relevant när bolaget har ett faktiskt behov, utan att dölja kostnad eller ansvar.

**Huvudresa:** Identifiera behov → pröva alternativ → godkänn datadelning → ansök → få kvalificerat erbjudande → jämför → signera → verifiera utbetalning → följ återbetalning.

**Ägda begrepp:** Funding need, eligibility indication, application, lender request, offer, customer decision och facility handoff.

### DR-FIN-01: Behovsbaserad ingång

Finansieringsingången ska kunna börja i Cash, en faktura, ett inköpsåtagande eller ett manuellt behov. Kunden ska först se belopp, tid och möjliga icke-kreditåtgärder som att invänta eller följa upp en kundbetalning.

**Gräns och undantag:** Försäljningsoptimering får inte presentera kredit som enda lösning eller fabricera brådska.

**Acceptans:** En likviditetsrisk visar både underliggande betalningar och ett frivilligt finansieringsscenario.

### DR-FIN-02: Preliminär möjlighet

Indikativ lämplighet ska ange datakälla, giltighet, omfattning och att slutligt kreditbeslut återstår. Beräknad möjlighet, godkänd limit och tillgängligt uttag ska vara skilda belopp.

**Gräns och undantag:** Texten du har 500 000 tillgängligt får inte användas för en okvalificerad modelluppskattning.

**Acceptans:** En preliminär matchning påverkar inte Cash som faktiska pengar och kan inte användas för betalning.

### DR-FIN-03: Datadelning och ansökan

Ansökan ska visa långivare, efterfrågade uppgifter, ändamål, bolagets företrädare och delat snapshot. Kunden ska kunna förhandsgranska och rätta faktiska fel innan delning. Varje partner får endast nödvändigt kvalificerat underlag.

**Gräns och undantag:** Allmän bokföringsåtkomst innebär inte automatiskt rätt att skicka ägaruppgifter till alla långivare.

**Acceptans:** En ansökan kan skickas till en vald partner utan att hela datarummet sprids till övriga.

### DR-FIN-04: Intermedieringsroll

Innan Drastic förmedlar företagskredit ska faktisk roll och relevanta registrerings- eller tillståndskrav klarläggas. Avtal ska ange vem som marknadsför, samlar ansökan, fattar beslut och tar ansvar. [E01]

**Gräns och undantag:** Regleringsanalys får inte skjutas upp tills Drastic börjar låna ut egna pengar.

**Acceptans:** Ett rent läsande finansieringsscenario kan lanseras separat från en blockerad förmedlingsfunktion.

### DR-FIN-05: Erbjudandets fulla ekonomi

Erbjudandet ska visa huvudbelopp, nettoutbetalning, avgifter, ränteberäkning, återbetalningsschema, säkerheter, garantier, uppsägningsvillkor och möjliga ändringar. Jämförbara kassaflödesmått ska ha explicit antagande och metod.

**Gräns och undantag:** En låg annonserad räntesats får inte dölja väsentliga avgifter eller ett mindre faktiskt utbetalt belopp.

**Acceptans:** Kunden kan jämföra två erbjudanden på faktiskt mottagna pengar, betalningsdatum och total känd kostnad.

### DR-FIN-06: Ranking och intressekonflikt

Sortering ska kunna göras efter kundvalda dimensioner som nettobelopp, betalningsprofil, säkerhet och total känd kostnad. Provision, sponsring och egen långivarroll ska redovisas där de påverkar presentationen.

**Gräns och undantag:** Ett alternativ får inte kallas billigast om urvalet är begränsat eller kassaflödena inte är jämförbara.

**Acceptans:** Ett högre provisionsavtal ändrar inte den kundvalda kostnadssorteringen utan synlig markering och separat placering.

### DR-FIN-07: Bindande acceptans

Acceptans ska binda erbjudandets exakta revision, låntagare, firmamandat och giltighet. Nya villkor eller gammal kreditinformation ska kräva kvalificerat nytt beslut före signering när erbjudandet kräver det.

**Gräns och undantag:** En accepterad indikativ offert är inte automatiskt ett ingånget och utbetalt lån.

**Acceptans:** Förfallen offert kan inte signeras genom återförsök som tyst använder en ny ränta.

### DR-FIN-08: Utbetalning och tillgänglighet

Efter signering ska kunden se villkor före utbetalning, pågående betalning och verifierat utfall. Capital äger avtalet och Payments eller långivaren äger den faktiska rörelsen. Cash uppdateras från rätt milstolpe.

**Gräns och undantag:** Signerad kredit räknas inte som banksaldo innan faktiska pengar observerats eller rätt kvalificerat tillgänglighetsbegrepp används.

**Acceptans:** Misslyckad låneutbetalning lämnar tydlig status och inga fiktiva bankmedel.

### DR-FIN-09: Pågående relation

Kunden ska kunna se uttag, ränta, avgifter, nästa betalning, säkerhetsvillkor och kvarvarande limit. Ansökan om ändring och extra återbetalning ska vara egna godkända handlingar.

**Gräns och undantag:** Datadelning som avslutas får inte få ett existerande låneavtal att försvinna ur gränssnittet.

**Acceptans:** Kunden kan exportera avtal och betalningshistorik även när nya erbjudanden inte längre tillhandahålls.

### DR-FIN-10: Klagomål och omprövning

Finansieringsärenden ska ge rätt ansvarig part för faktarättelse, kreditbeslut, avtalstvist och plattformsfel. Beslutsförklaring ska vara saklig och tillåten. Omprövning ska behandlas av behörig person med verkligt handlingsutrymme.

**Gräns och undantag:** En kundsupportbot får inte vara enda slutliga instans för ett betydande individuellt beslut.

**Acceptans:** Ett felaktigt bokföringsunderlag kan rättas och leda till nytt daterat beslut utan att den gamla historiken raderas.


<a id="chapter-21"></a>

## 21. Drastic Risk: beslutsunderlag och riskstyrning

**Första leveransnivå:** ES-1 för datakvalitet, ES-4 för kredit. **Ändamål:** Ge förklarbara och ändamålsbundna beslutsunderlag utan att göra en universell poäng till ersättning för ekonomiskt eller juridiskt ansvar.

**Huvudresa:** Kvalificera ändamål → frys data → beräkna egenskaper → tillämpa policy/modell → granska → fatta beslut → följ utfall → ompröva.

**Ägda begrepp:** Data-quality assessment, feature snapshot, model release, policy release, risk decision, override, monitoring observation och appeal.

### DR-RISK-01: Separata riskfamiljer

Datakvalitet, likviditet, kreditförlust, bedrägeri, AML/sanktioner och operativ risk ska ha egna definitioner, ägare och åtkomst. De får dela kvalificerade fakta men inte presenteras som en enda oförklarad riskpoäng.

**Gräns och undantag:** En svag källtäckning är inte samma sak som hög kreditrisk eller misstänkt brottslighet.

**Acceptans:** Saknat kontoutdrag ger ofullständigt underlag och en kompletteringsuppgift, inte automatiskt sämsta kreditklass.

### DR-RISK-02: Ändamålsbunden datamängd

Varje riskprodukt ska registrera syfte, tillåtna källor, användare, mottagare och lagringsgrund. Funktioner ska bara få använda nödvändiga fält. Bolagets bokföringsrelation, långivarens bedömning och extern riskdataförsäljning ska vara separata produkter.

**Gräns och undantag:** Kunddata blir inte Drastics fria immateriella egendom genom att data finns i en gemensam databas.

**Acceptans:** En modell för företagslikviditet kan köras utan tillgång till anställdas personliga lönebesked eller sjukuppgifter.

### DR-RISK-03: Punkt-i-tid-egenskaper

Feature snapshots ska bindas till när informationen var känd, avsedd period, originalkälla och transformation. Senare korrigeringar ska bevaras som nya observationer. Historisk validering ska kunna återge då tillgänglig information.

**Gräns och undantag:** Framtida betalningar, beslut eller rättelser får inte läcka in i träning eller historisk prestation.

**Acceptans:** Ett kreditbeslut i mars reproduceras utan apriluppgifter trots att datasetet senare uppdaterats.

### DR-RISK-04: Definierade ekonomiska egenskaper

Omsättning, kundkoncentration, AR-aging, likviditetsbuffert, säsong och återbetalningsförmåga ska ha specificerade nämnare, perioder, skattebehandling och valuta. Varje värde ska kunna öppnas till bidragen.

**Gräns och undantag:** Noll nämnare ger ej definierat, inte nollrisk eller oändlig återbetalningsförmåga.

**Acceptans:** Kundkoncentration på en tom reskontra redovisas som ej tillämpligt för den mätningen och med separat omsättningskoncentration där underlag finns.

### DR-RISK-05: Kreditmodellens semantik

En modell ska ange vilken händelse den bedömer, horisont, population, defaultdefinition och begränsningar. PD, LGD och EAD får bara visas med kvalificerade definitioner och kalibrering. Tidiga produkter ska kunna använda transparenta regler och verklig långivarbedömning.

**Gräns och undantag:** En LLM-genererad siffra eller några goda pilotkunder räcker inte för en validerad sannolikhet för kreditförlust.

**Acceptans:** Ett tunt dataset ger regelbaserat underlag med okalibrerad status och ingen påhittad PD med två decimaler.

### DR-RISK-06: Modell- och policyregister

Varje modellversion, featuredefinition och beslutspolicy ska ha ägare, avsedd användning, godkännande, validering, utrullningsstatus och återställningsväg. Modellbyte ska kunna köras i skuggläge innan det påverkar nya beslut.

**Gräns och undantag:** En utvecklare får inte ändra produktionsgränsen och samma stund godkänna sitt eget undantag.

**Acceptans:** Ett beslut anger exakt modell- och policyversion och kan reproduceras efter en senare release.

### DR-RISK-07: Oberoende validering

Validering ska pröva tidsseparerade data, relevanta kundgrupper, kalibrering, missade förluster, felaktiga avslag och praktisk mänsklig användning. Urvalsbias från att bara finansierade ansökningar får observerade utfall ska dokumenteras.

**Gräns och undantag:** Avsaknad av observerad förlust bland ett fåtal godkända lån bevisar inte att avslag var riktiga.

**Acceptans:** En valideringsrapport skiljer teknisk träffsäkerhet från ekonomiskt utfall och anger populationer där modellen inte är kvalificerad.

### DR-RISK-08: Mänskliga beslut och undantag

Kreditbeslut ska registrera fakta, förslag, behörig beslutsfattare, villkor och skäl. Undantag ska ha separat policy och uppföljning. Granskaren ska kunna förstå, ändra eller avvisa förslaget och begära ytterligare fakta.

**Gräns och undantag:** Att klicka godkänn utan verkligt utrymme för omprövning ska inte beskrivas som meningsfull mänsklig kontroll.

**Acceptans:** Ett dokumenterat undantag sparar originalförslag, beslut och ansvarig utan att skriva om modellens ursprungliga output.

### DR-RISK-09: Personuppgifter och betydande beslut

När beslut rör fysiska personer, borgensmän eller enskilda näringsidkare ska produktrollen och skydden för automatiserat beslutsfattande kvalificeras. Individens faktarättelse och tillämpliga möjlighet till mänsklig prövning ska vara fungerande. [E06, E17]

**Gräns och undantag:** B2B-etikett är inte ett generellt undantag när produkten behandlar eller påverkar identifierbara personer.

**Acceptans:** En ansökan med personlig borgen får en separat rättslig och datamässig bedömning innan personbaserad scoring aktiveras.

### DR-RISK-10: AI-regulatorisk klassificering

Varje AI-system ska ha dokumenterad avsedd användning, roll som leverantör eller användare, tillämplig klass och ikraftträdandeversion. Intern governance ska finnas före skarp användning även när en viss lagfrist ligger senare. [E07]

**Gräns och undantag:** En allmän hänvisning till AI Act eller en historisk tidslinje får inte vara produktens aktuella juridiska beslut.

**Acceptans:** En ny användning för fysiska personers kreditvärdighet kan inte aktiveras med godkännandet för en äldre kassaflödesförklarare.

### DR-RISK-11: Bedrägerisignaler

Signaler som ändrad mottagare, ovanlig betalning eller dokumentkonflikt ska ange verifierbara observationer och kvalificerad kontrollåtgärd. Hög risk kan kräva extra autentisering eller manuell granskning enligt mandat.

**Gräns och undantag:** En misstanke får inte presenteras som ett bevisat brott eller en delbar kundetikett.

**Acceptans:** En leverantör med nytt konto får en mottagarkontroll utan att felaktigt klassificeras som kreditförlust.

### DR-RISK-12: AML och sanktioner

Tillämplig kundkännedom, transaktionsövervakning, sanktionskontroll och utredning ska ha ansvarig reglerad funktion. Träff, verifierad identitet, utredning och beslut ska hållas separata. Skyddad information ska ha begränsad synlighet. [E09]

**Gräns och undantag:** Sanktionsträff eller liknande namn är inte automatiskt samma person. Kunden ska inte få skyddade interna utredningsuppgifter via generella förklaringar.

**Acceptans:** En träff granskas av rätt funktion medan kundens vy bara visar den lagligen tillåtna statusinformationen.

### DR-RISK-13: Löpande bevakning

Bevakning ska registrera nya data, avtalsvillkor och faktisk exponering. Förändring kan skapa granskningsärende eller stoppa ett nytt uttag enligt avtal. Befintligt avtal ska inte retroaktivt omskrivas av ny modellversion.

**Gräns och undantag:** Försämrad modellpoäng är inte ensam rätt att ändra ränta, säga upp kredit eller debitera avgift.

**Acceptans:** Ett nytt riskutfall länkas till ett separat behörigt avtalsbeslut med oförändrad tidigare lånehistorik.

### DR-RISK-14: Risk-API och extern kreditupplysning

Riskprodukter till externa mottagare ska ha eget beslutat ändamål, dataavtal, upplysningsinnehåll och regulatorisk klassificering. IMY:s krav på kreditupplysningsverksamhet ska prövas innan en sådan tjänst säljs. [E05]

**Gräns och undantag:** En FI-registrering för kreditverksamhet eller en allmän API-nyckel är inte ett generellt kreditupplysningstillstånd.

**Acceptans:** Risk-API för intern egenkundsanalys kan vara separat från en blockerad extern kreditupplysningsprodukt.

### DR-RISK-15: Stress och koncentration

Risk ska kunna producera scenarier för intäktsbortfall, betalningsförsening, sektor- och motpartskoncentration samt partneravbrott. Scenarioantaganden ska vara synliga och får inte utges för kalibrerade prognoser.

**Gräns och undantag:** Stressutfall får inte omvandlas till automatiskt individuellt pris eller avslag utan kvalificerad beslutsmodell.

**Acceptans:** En portföljrapport kan visa ett hypotetiskt kundbortfall och berörda exponeringar utan att ändra låneavtal.

### DR-RISK-16: Klagomål, rättelse och modellincident

Användare och berörda personer ska få en fungerande väg att rätta faktiska fel och få relevant prövning. Modellincident ska kunna frysa nya automatiserade beslut och identifiera berörd population och återprövningsbehov.

**Gräns och undantag:** Frysning av ny kreditbedömning får inte stoppa kundens möjlighet att betala tillbaka eller läsa avtalet.

**Acceptans:** En felaktig featureversion kan spåras till berörda beslut och ersättas av kvalificerad manuell hantering.


<a id="chapter-22"></a>

## 22. Capital products och kreditförvaltning

**Första leveransnivå:** ES-4 med partner, ES-6 valfritt eget risktagande. **Ändamål:** Tillhandahålla finansieringsprodukter med full livscykel, tydlig fordringsägare och en ekonomi som håller efter finansieringskostnad och förluster.

**Huvudresa:** Produktmandat → kreditbeslut → avtal → villkor före utbetalning → uttag → servicing → avräkning → förlängning, avslut eller workout.

**Ägda begrepp:** Capital product, facility, draw, loan movement, receivable assignment, collateral, covenant, repayment schedule och portfolio.

### DR-CAP-01: Produktmallar

Varje kapitalprodukt ska definiera långivare, låntagare, kapitalägare, rättslig form, valuta, limit, löptid, säkerhet, avgifter, beräkningsmetod och servicedelar. Företagslån, revolverande kredit, fakturaförskott och fakturaköp ska vara olika kvalificerade mallar.

**Gräns och undantag:** Ett generiskt financing-objekt får inte dölja skillnaden mellan fordringsköp och belåning.

**Acceptans:** Avtalsmallens val styr synlig rättighetskedja, återbetalningsplan och redovisningsunderlag.

### DR-CAP-02: Beslut och finansieringskälla

Beviljande ska binda kreditbeslut, tillgänglig finansieringskälla, eventuell garanti och villkor. Drastic ska visa vem som faktiskt bär kreditrisk, likviditetsrisk, bedrägeriförlust och regress i det aktuella upplägget.

**Gräns och undantag:** En partneretikett betyder inte att Drastic saknar garanti-, återköps- eller förlustansvar.

**Acceptans:** En produkt kan inte aktiveras utan en dokumenterad risk- och betalningsansvarsmatris.

### DR-CAP-03: Facility och tillgänglig limit

Signerad limit, disponibel avtalslimit, låst reserv, utnyttjat kapital och möjligt nytt uttag ska skiljas åt. Samtidiga uttag ska reservera limit atomiskt med aktuell behörighet och avtalsvillkor.

**Gräns och undantag:** En signerad limit är inte nödvändigtvis omedelbart uttagbar.

**Acceptans:** Två uttag om 60 000 mot kvarvarande 100 000 kan inte båda kvalificeras och skickas.

### DR-CAP-04: Villkor före utbetalning

Kundkännedom, säkerhet, avtalssignatur, finansieringskälla, betalningsmottagare och andra avtalade villkor ska ha verifierade uppfyllelseposter. Utbetalning ska förberedas först när alla obligatoriska villkor gäller.

**Gräns och undantag:** Ett uppladdat dokument är inte automatiskt en fullgjord säkerhetsåtgärd.

**Acceptans:** Ett ändrat bankkonto efter signering stoppar utbetalning tills rätt mottagarversion godkänts.

### DR-CAP-05: Uttag och faktisk utbetalning

Uttag ska skapa en identifierad kapitalrörelse och ett avgränsat betalningsuppdrag. Kontraktuellt kapitalbelopp, innehållen avgift och nettoutbetalning ska särredovisas. Okänt betalningsutfall ska hanteras utan nytt blinduttag.

**Gräns och undantag:** Drastic får inte bokföra lånets nettoutbetalning som omsättning hos låntagaren.

**Acceptans:** 100 000 kapital och 1 000 innehållen avgift ger 99 000 i observerad utbetalning enligt den kvalificerade produktprofilen.

### DR-CAP-06: Ränta och avgifter

Beräkning ska definiera räntesats, day-count, kapitaliseringsvillkor, ränteperiod, värdedag, avrundning och kontraktsversion. Variabel ränta kräver kvalificerad referens och omprissättningsregel. Upplupen ränta och betald ränta ska vara olika rörelser.

**Gräns och undantag:** Daglig avrundning får inte införas om avtalet kräver precision fram till periodslut.

**Acceptans:** Ett handräknat avtal kan reproduceras vid normal betalning, förtida återbetalning och sen betalning.

### DR-CAP-07: Betalningsplan och waterfall

Betalningar ska allokeras enligt avtalad prioritering mellan avgifter, ränta och kapital. Ursprunglig plan, faktisk betalning och reviderad framtida plan ska behållas. Överbetalning ska ge eget tillgodohavande eller återbetalningsbehov.

**Gräns och undantag:** En betalning får inte godtyckligt minska den komponent som gör portföljrapporten snyggast.

**Acceptans:** Delbetalning ger exakt komponentrest och samma resultat vid replay.

### DR-CAP-08: Fakturafinansiering och rättigheter

Faktura ska prövas mot ursprung, leverans, återstående belopp, tvist, kredit och känd tidigare pantsättning eller överlåtelse. Avtal ska definiera rättighetsövergång, regress, betalningsmottagare och avräkning.

**Gräns och undantag:** Plattformen kan inte lova global kontroll över extern dubbelbelåning utan verklig informationskälla och rättslig grund.

**Acceptans:** Samma kända fordringsdel kan inte samtidigt disponeras för två interna finansieringsavtal.

### DR-CAP-09: Fakturaköp kontra lån

Kvalificerad true-sale-produkt ska ha egen köpeskilling, initial likvid, innehållen del och efteravräkning. Belåningsprodukt ska i stället bevara fordran och låneskuld enligt rätt redovisningsprofil. Riskövergång och redovisningsmässig bortbokning ska bedömas separat.

**Gräns och undantag:** Produktnamnet factoring bestämmer inte automatiskt redovisningen.

**Acceptans:** Två avtal med samma initiala utbetalning kan ge olika men korrekt förklarade rättigheter och bokföringsunderlag.

### DR-CAP-10: Kundbetalning och avräkning

Betalning från slutkunden ska allokeras till rätt fordringsägare och avräkning. Säljarens restlikvid, långivarens kapital, ränta och avgift ska särredovisas. Felriktad betalning ska skapa en utredning, inte försvinna.

**Gräns och undantag:** Finansieringsutbetalning och hela kundfakturan får inte båda räknas som fria framtida inflöden till säljaren.

**Acceptans:** Efter ett förskott på fakturan räknas bara avtalad återstående likvid som säljarens nästa inflöde.

### DR-CAP-11: Covenants och begränsningar

Avtalsvillkor ska ha mätdefinition, källor, kontrollperiod och konsekvensprocess. Databrist, faktisk överträdelse och pågående rättelse ska skiljas åt. Konsekvenser ska följa avtalet och behöva rätt beslut.

**Gräns och undantag:** Saknade data ska inte automatiskt likställas med ekonomiskt avtalsbrott om avtalet inte ger sådan grund.

**Acceptans:** En ändrad rapportversion skapar ny kvalificerad covenantbedömning med bevarat tidigare resultat.

### DR-CAP-12: Ändring och förtida avslut

Förlängning, extra uttag, ränteskifte, amorteringsfrihet och förtida lösen ska vara versionsbundna avtalsändringar. Kunden ska se belopp och kvarvarande skyldigheter innan acceptans.

**Gräns och undantag:** En ny intern modellpolicy får inte omskriva historiskt avtal eller betalningswaterfall.

**Acceptans:** Förtida lösen ger en kvotering med giltighet och kan avstämmas till slutligt nollsaldo eller förklarad rest.

### DR-CAP-13: Arrears och workout

Försenad betalning ska ge rätt kommunikation, manuellt handlingsutrymme och dokumenterad plan. Omstrukturering, regress, säkerhetsåtgärd, nedskrivning och juridisk kravhantering ska ha kvalificerade ägare.

**Gräns och undantag:** Automatisering får inte utnyttja personlig borgen eller vidta indrivningsåtgärd utan rätt process.

**Acceptans:** En omförhandlad plan bevarar originalskuld och visar ny fördelning av framtida betalningar utan att fabricera återvinning.

### DR-CAP-14: Portfölj och kapitalekonomi

Portföljvyer ska skilja utestående kapital, inflöden, intäkter, upplupna belopp, funding cost, kreditförlust, bedrägeriförlust och operativ kostnad. Vintage, segment, koncentration och lånekällor ska vara tydliga.

**Gräns och undantag:** Utbetalat lånekapital, factoringvolym och låntagarens återbetalning av kapital är inte Drastics omsättning.

**Acceptans:** Portföljens intäkt kan härledas utan att räkna samma kapitalrörelse som både finansieringsvolym och försäljning.

### DR-CAP-15: Finansiering, SPV och separata böcker

En framtida egen kreditbok ska ha dokumenterad finansieringsstruktur, kapital- och likviditetspolicy, eventuella SPV-relationer, investerarvillkor och separata juridiska böcker. Servicing ska kunna avstämmas mot långivarens redovisning.

**Gräns och undantag:** Kundmedel eller operativ SaaS-kassa får inte antas vara tillgängligt utlåningskapital.

**Acceptans:** En långivarportfölj kan stämmas av mot dess egen huvudbok utan att använda låntagarnas böcker som långivarens balansräkning.

### DR-CAP-16: Partnerexit och back-up servicing

Avtal ska ange hur lånehistorik, dokument, betalningar, säkerheter och öppna ärenden förvaltas om partner eller Drastic upphör. Kunden ska ha fortsatt betalningsväg och kontakt med ansvarig fordringsägare.

**Gräns och undantag:** Ett avslutat plattformsabonnemang får inte hindra amortering eller tillgång till avtalet.

**Acceptans:** En kontinuitetsövning kan lämna över en aktiv facility och dess avräkningar till kvalificerad ersättare utan dubbel kravhantering.


<a id="chapter-23"></a>

## 23. Agentoperativsystem och mänsklig kontroll

**Första leveransnivå:** ES-1 till ES-5. **Ändamål:** Låta agenter utföra mycket arbete med tydlig delegation och mätbar kvalitet, utan egna obegränsade finansiella befogenheter.

**Huvudresa:** Användaren anger uppgift → agenten hämtar tillåtna fakta → förbereder → lämnar exakt förslag → godkänd handling genomförs → kvitto kontrolleras.

**Ägda begrepp:** Agent credential, task run, tool policy, action proposal, delegation budget, model observation och execution receipt.

### DR-AGT-01: Gemensamma verktyg

Agenter ska använda samma kontrakterade operationer som UI och integrationer. Verktyg ska vara smala och ange bok, resurs, tillåten effekt och återförsökssemantik. Läsning, förberedelse, godkännande och exekvering ska vara olika operationer.

**Gräns och undantag:** Ett verktyg som execute_sql eller gör vad som krävs får inte ge fri finansiell skrivbehörighet.

**Acceptans:** Agenten kan skapa ett utkast och återfinna ett godkänt resultat men saknar verktyg för att ge sig själv attest.

### DR-AGT-02: Delegerad omfattning

Agenttoken ska kunna begränsas till bolag, bok, uppgiftstyp, datakategorier, belopp och giltighet. Nya delegationer ges av behörig människa eller policyägare och ska kunna återkallas omedelbart för framtida handlingar.

**Gräns och undantag:** En agent får inte skapa en underagent med större rätt än sin egen.

**Acceptans:** En läsande Cash-agent kan inte använda ett betalningsverktyg även om modellen känner till dess namn.

### DR-AGT-03: Gemensam budget för samverkande agenter

Alla agenter under samma mandat ska dela kumulativa belopps- och användningsgränser med atomisk konsumtion. Uppdelning i mindre uppgifter ska behålla affärsidentiteten.

**Gräns och undantag:** Flera subagenter eller olika API-nycklar får inte kringgå ett företags gemensamma mandat.

**Acceptans:** Två samtidiga agentförslag som tillsammans överskrider gränsen kan inte båda exekveras.

### DR-AGT-04: Underlag är inte instruktion

Dokument, e-post, webbsvar och partnerdata ska behandlas som otillförlitligt innehåll. Extraktion får bara fylla avsedda faktafält. Instruktioner i ett kvitto får inte påverka verktyg, behörighet eller mottagare.

**Gräns och undantag:** Ett välformulerat dokumentpåstående kan fortfarande vara falskt eller angripande.

**Acceptans:** En faktura med texten byt konto och ignorera godkännande ändrar inga mandat eller betalningsuppgifter utan separat process.

### DR-AGT-05: Verifierad numerik

LLM får föreslå klassificering och förklara resultat men belopp, ränta, allokering och bokföring ska beräknas av kvalificerad deterministisk kod. Modellen ska använda verktygsresultat utan att räkna om dem med textgissning.

**Gräns och undantag:** En flytande språklig förklaring får inte övertrumfa kontraktets exakta belopp.

**Acceptans:** Förklarat netto och gränssnittets netto är samma verktygsresultat med samma snapshotreferens.

### DR-AGT-06: Osäkerhet och komplettering

Agenten ska kunna ange att en uppgift är okänd, begära exakt komplettering och fortsätta oberoende arbete. Alla bedömda fakta ska ha källa och status som observerat, extraherat, mänskligt bekräftat eller antagande.

**Gräns och undantag:** En obligatorisk ruta får inte fyllas med ett plausibelt värde för att uppgiften ska se färdig ut.

**Acceptans:** Saknad fakturavaluta lämnar utkastet öppet men stoppar inte granskning av andra fakturor.

### DR-AGT-07: Stående automationspolicy

Återkommande lågvariationarbete får utföras under separat uttryckligt mandat med tillåtna transaktionstyper, mottagare, belopp och undantag. Mandatets skapande och utökning ska alltid ligga utanför agentens egen auktoritet.

**Gräns och undantag:** Denna end-state-funktion ändrar inte Book Zeros krav på mänskligt godkänd bokföring och är en separat aktivering.

**Acceptans:** Avvikande mottagare eller gränsöverskridande belopp går till människa även om föregående månader hanterats automatiskt.

### DR-AGT-08: Återhämtning och stopp

Agentkörning ska behålla uppgiftsidentitet, redan utförda handlingar och oavgjorda externa resultat. Avbryt ska stoppa nytt arbete och synliggöra sådant som redan kan ha skickats.

**Gräns och undantag:** Avbruten agentprocess betyder inte att genomförda pengarörelser rullas tillbaka.

**Acceptans:** Återstart hittar ett befintligt betalningskvitto i stället för att skapa ett nytt betalningsbehov.

### DR-AGT-09: Modellval och dataminimering

Val av modell och region ska följa uppgiftens dataklass, avtal och tillåtna leverantörer. Känsliga fält ska maskeras när de inte behövs. Loggning och eventuell träningsanvändning ska vara separat reglerade.

**Gräns och undantag:** En EU-endpoint ensam är inte bevis för att all underbehandling stannar inom godkänd jurisdiktion.

**Acceptans:** En dokumentförklaring skickar inte personnummer, bankhemligheter eller råa löner när redigerat underlag räcker.

### DR-AGT-10: Kvalitetsmätning

Agentkvalitet ska mätas på korrekt behandling, mänskliga rättelser, falska säkerhetsbesked, tid till färdigt resultat och total kostnad. Jämförelser ska använda samma underlag och stödda profil.

**Gräns och undantag:** Antal automatiserade verktygsanrop eller tokens är inte ett kundvärdemått.

**Acceptans:** En ny modell släpps inte enbart för lägre pris om den ökar felaktiga bokföringsförslag i kritiska fall.

### DR-AGT-11: Förklaring och revisionsspår

Kunden ska se vilka källor och regler som användes, föreslagen effekt, mandat och verkligt resultat. Modellidentitet, promptmallversion och verktygsobservationer kan behållas enligt policy för felsökning.

**Gräns och undantag:** Intern tankekedja behövs inte som revisionsbevis och ska inte ersätta källor eller beslut.

**Acceptans:** En granskare kan förklara ett agentförberett förslag utan tillgång till hemlig modellimplementation.

### DR-AGT-12: Oberoende kontroll

Agenter kan granska andra agenters förslag men sådan kontroll ska klassificeras som maskinell. Kritiska produkt- och kreditbeslut som kräver oberoende mänsklig funktion får inte delegeras till en andra modell och beskrivas som uppfyllda.

**Gräns och undantag:** Två modeller med samma underlag är inte automatiskt oberoende redovisnings- eller compliancegranskning.

**Acceptans:** Releasebeslutet skiljer dokumenterad modellkontroll från behörig persons godkännande.


<a id="chapter-24"></a>

## 24. Integrationer, API och ekosystem

**Första leveransnivå:** ES-1 till ES-5. **Ändamål:** Ansluta externa system med tydliga ägare, säkra återförsök och en portabel produktkärna.

**Huvudresa:** Välj kvalificerad anslutning → ge rätt åtkomst → hämta första underlag → kontrollera → följ förändringar → rätta avvikelse → förnya eller avsluta.

**Ägda begrepp:** Provider capability, connection, consent, credential reference, sync cursor, import occurrence och reconciliation checkpoint.

### DR-INT-01: Kapabilitetsregister

Varje integration ska ange stödda objekt, läs-/skrivoperationer, jurisdiktioner, valutor, datatäckning, begränsningar och observerad verifieringsnivå. Produktgränssnittet ska styras av denna kvalificerade kombination.

**Gräns och undantag:** En banklogotyp får inte antyda stöd för betalning om anslutningen endast läser konton.

**Acceptans:** Samma leverantör kan vara kvalificerad för kontodata men blockerad för lönebetalning med tydlig produktstatus.

### DR-INT-02: Ägarskap per objekt

Connected mode ska bestämma ägare per faktura, kundpost, leverantörsfaktura, bokföringsperiod och betalning. Konfliktlösning ska visa källan och följdeffekter. Objekt som skapas i Drastic ska ha definierad export- eller synkväg.

**Gräns och undantag:** Senaste timestamp är inte en generell konfliktlösare för ekonomiskt betydelsefulla fält.

**Acceptans:** Extern kreditnota på en Drastic-finansierad faktura skapar uppföljning i rätt ägare utan tyst överskrivning.

### DR-INT-03: Credential- och samtyckesförvaring

Hemligheter ska förvaras separat med kryptering, rotation, minsta scope och kontrollerad åtkomst. Förnyelse och återkallelse ska ha driftmässiga processer. Kundens samtyckesstatus ska kunna visas utan att token exponeras.

**Gräns och undantag:** Driftloggar, agentprompter och klientlagring får inte innehålla återanvändbara provider credentials.

**Acceptans:** En återkallad anslutning stoppar nya hämtningar och lämnar bevarade lagligt lagrade historiska uppgifter läsbara.

### DR-INT-04: Första synk och backfill

Initial hämtning ska ha tydligt datumintervall, sidor, kontrollantal, dubblettidentitet och återupptagning. Historisk backfill ska kunna ske utan att återutlösa utskick, betalningar eller gamla påminnelser.

**Gräns och undantag:** Import av ett historiskt paid-fält får inte instruera en ny bankbetalning.

**Acceptans:** Avbruten import av sida tre återupptas utan fördubblade öppna poster eller dolda luckor.

### DR-INT-05: Förändringar och watermarks

Integration ska följa ändringar med dokumenterade cursors, versioner och eftersläpning. Projectioner ska visa vilken källa och revision de nått. Fullständig kontrollhämtning ska kunna upptäcka bortfall och korrigeringar.

**Gräns och undantag:** Webhooks utan fullständig leveransgaranti ersätter inte återkommande avstämning.

**Acceptans:** En utebliven webhook hittas genom periodisk kontroll och skapar en spårbar uppdatering.

### DR-INT-06: Kontraktsversioner

Offentliga APIer ska ha versionsstyrda scheman, stabil felklassning, exakta pengar, idempotens och cursorbaserad paginering. Breaking changes ska ha migreringsperiod och kundsynligt underlag. Export- och webhookkontrakt ska omfattas.

**Gräns och undantag:** Ett TypeScript-typnamn är inte en komplett wire-specifikation.

**Acceptans:** En gammal stödd klient kan läsa sparat kvitto efter serveruppgradering utan att belopp feltolkas.

### DR-INT-07: Utgående webhooks

Kundwebhooks ska signeras och bära händelseidentitet, scope och referens till beständigt objekt. Återleverans ska vara möjlig med tydlig retention och köstatus. Mottagaren ska upplysas om at-least-once och separat ekonomisk idempotens.

**Gräns och undantag:** En webhook-ack hos kund ersätter inte vårt interna bokföringskvitto.

**Acceptans:** Kundens långvariga 500-svar tappar inte ekonomiskt resultat och kan hanteras utan dubbla effekter vid replay.

### DR-INT-08: Lokal utveckling och sandbox

Utvecklare ska ha syntetiska exempel, deklarerad sandbox och kontraktdokumentation för relevanta scenarier. Sandboxutfall ska markeras skilt från verklig leverantörsacceptans. Produktionscredentials ska aldrig krävas för grundläggande lokal redovisning.

**Gräns och undantag:** En lyckad sandboxbetalning är inte bevis för produktionens alla rails eller klipptider.

**Acceptans:** En utvecklare kan köra bokföringskärnan utan att koppla riktiga bankmedel eller få betalningsmandat.

### DR-INT-09: Tillägg och ekonomiska kommandon

Tillägg ska kunna läsa kvalificerade resurser och föreslå handlingar under uttryckligt scope. Manifest ska ange dataanvändning, externa destinationer och möjliga sidoeffekter. Ägaren ska kunna dra tillbaka tilläggets åtkomst.

**Gräns och undantag:** Ett installerat tillägg får inte få obegränsad åtkomst till alla bolag eller direkt DB-skrivning.

**Acceptans:** Ett fakturatillägg kan skapa ett utkast men inte ge sig självt rätt att signera betalningar.

### DR-INT-10: Partnerbyte

Byte av leverantör ska skilja nya operationer från gamla pågående avtal och utfall. Referenser, historik, öppna tvister och ansvar ska behållas tills de är slutligt hanterade.

**Gräns och undantag:** En abstrakt adapter gör inte gamla kort, bankmedgivanden eller kreditavtal automatiskt flyttbara.

**Acceptans:** Gamla uppdrag avstäms mot tidigare partner samtidigt som nya uppdrag går till en ny kvalificerad partner.

### DR-INT-11: Licens och källutgåva

Utgåvor ska dokumentera införlivad kod, beroenden, licenser och exakt motsvarande källversion för den driftmodell som används. Tilläggens kommersiella gränser ska inte antas utgöra undantag från openERP:s AGPL-policy. [R03]

**Gräns och undantag:** Separat process eller API bevisar inte att en kombinerad produkt kan slutas licensmässigt.

**Acceptans:** Kundens source offer leder till den faktiskt driftsatta täckta utgåvan utan kunddata eller credentials.


<a id="chapter-25"></a>

## 25. Finansoperationer, drift och förtroende

**Första leveransnivå:** ES-1 till ES-5. **Ändamål:** Driva produkten så att pengar, ansvar och återställning fungerar även när den normala kundresan bryts.

**Huvudresa:** Observera → upptäck avvikelse → klassificera påverkan → stoppa risk → utred → korrigera med rätt mandat → stäm av → kommunicera → lär.

**Ägda begrepp:** Operational case, reconciliation exception, incident, control attestation, retention policy, access review och exit plan.

### DR-OPS-01: Finansiell operationskonsol

Behörig operationsfunktion ska se åldrande okända betalningar, oförklarade avräkningar, otilldelade inflöden, kreditvillkor och partneravbrott. Varje avvikelse ska ha pengar i risk, källa, prioritet och ansvarig.

**Gräns och undantag:** Konsolen ska inte ge generell rätt att manuellt ändra kundens saldo.

**Acceptans:** En operatör kan hitta en okänd utbetalning och säkert eskalera utan att skriva en godtycklig korrigeringspost.

### DR-OPS-02: Trevägsavstämning

Uppdragsregister, partnerns avräkning och observerade kontorörelser ska jämföras med förklarade differenser. Relevanta belopp, fees, värdedatum och utfall ska kunna stämmas på transaktions- och totalsnivå.

**Gräns och undantag:** Ett nettosaldo som stämmer räcker inte om två kundmedelspositioner blandats.

**Acceptans:** Avräkningen upptäcker fel kundallokering trots att partnerns totalsumma är korrekt.

### DR-OPS-03: Oidentifierade medel och rättelser

Mottagna men oförklarade belopp ska ligga i ett explicit gransknings- eller avräkningstillstånd med juridisk ägare. Rättelse ska kräva underlag och behörighet samt länkas till original.

**Gräns och undantag:** En suspensepost är inte en tillåten permanent plats att dölja förluster eller kundmedelsbrist.

**Acceptans:** Åldersrapporten visar oförklarade medel och en rättelse lämnar ursprunglig händelse spårbar.

### DR-OPS-04: Separation mellan kundmedel och egen ekonomi

Där Drastic eller partner håller kundmedel ska produktens kontomodell och kontroller återspegla det kvalificerade upplägget. Egen SaaS-intäkt, partnerfordran, lånekapital och kundtillgodohavande ska ha olika juridiska ägare.

**Gräns och undantag:** Kundmedel får inte behandlas som rörelsekapital eller outnyttjad lånefinansiering.

**Acceptans:** Finansrapporten kan visa var varje medelskategori finns och vilka kunder eller motparter den tillhör.

### DR-OPS-05: Incidentstyrning

Incident ska klassificeras efter dataläckage, felaktig ekonomisk effekt, otillgänglighet och reglerad skyldighet. Kill switches ska kunna begränsas till en operation, provider eller population. Bevis ska bevaras och kommunikation ha ansvarig.

**Gräns och undantag:** Bred avstängning får inte i onödan hindra återbetalning, spärr eller läsning av historik.

**Acceptans:** En felaktig mottagarkontroll kan stoppa nya betalningar medan pågående utfall fortsätter avstämmas.

### DR-OPS-06: Återställning med finansiell kontroll

Återställning ska omfatta databas, original, nycklar, kontraktsversioner, köläge och externa referenser. Återstart av finansiell skrivning ska kräva en fenced writer och avstämning av externa handlingar efter senaste säkra punkt.

**Gräns och undantag:** Återställning av gårdagens databas får inte orsaka ny betalning för en handling som banken redan utförde.

**Acceptans:** En återställningsövning återskapar eller utreder externa kvitton innan gamla kommandon tillåts göra sidoeffekt.

### DR-OPS-07: Säker åtkomst och support

Supportåtkomst ska vara behovsprövad, tidsbegränsad och loggad. Privilegierad åtkomst ska ha step-up och relevant separation. Kunden ska kunna se tillämplig supportaktivitet utan att få känsliga interna säkerhetsuppgifter.

**Gräns och undantag:** Support får inte tyst impersonera kundens attest eller signering.

**Acceptans:** En supportmedarbetare kan diagnostisera fel men kan inte godkänna kundens betalning.

### DR-OPS-08: Dataregion och underleverantörer

Datakategorier ska ha dokumenterade lagrings- och behandlingsvägar, underleverantörer, åtkomst och överföringsmekanismer. Marknadsföringspåståenden om dataregion ska verifieras mot hela kedjan, inklusive modeller, support och telemetri.

**Gräns och undantag:** En svensk databasnod är inte ensam bevis för att all kunddata behandlas i Sverige.

**Acceptans:** En ny modellleverantör kan inte aktiveras för löneunderlag utan godkänd dataväg.

### DR-OPS-09: Retention och radering

Retention ska skilja räkenskapsinformation, avtal, AML-underlag, säkerhetsloggar och tillfälliga modellindata. Laglig radering eller minimering ska samordnas med skyldigheter att bevara vissa uppgifter. [E13, E17]

**Gräns och undantag:** Rätten till radering innebär inte att all bokförings- och avtalshistorik kan raderas direkt.

**Acceptans:** En stängd kund får dokumenterad behandling per datakategori med bevarat nödvändigt arkiv och borttagna onödiga arbetskopior.

### DR-OPS-10: Leverantörsrisk och DORA

Drastic ska ha inventering av kritiska externa beroenden, koncentration, avtal, incidentvägar, test och exit. Direkt DORA-tillämplighet respektive skyldigheter genom reglerade partners ska kvalificeras per verksamhet. [E08]

**Gräns och undantag:** All SaaS omfattas inte automatiskt direkt av samma regulatoriska skyldigheter.

**Acceptans:** En kritisk partners exitplan och kontaktväg kan användas i en genomförd övning, inte bara visas i ett avtal.

### DR-OPS-11: Kontrollbevis och release

Release ska beskriva kodrevision, aktiverade profiler, kända begränsningar, genomförda verifieringar och godkännande. Känsliga förändringar ska ha rollback- eller framåträttelseplan och observerad påverkan.

**Gräns och undantag:** Godkänd lint, modellbenchmark eller sandbox är inte i sig verifierad finansiell produktion.

**Acceptans:** En release kan rullas tillbaka funktionellt utan att redan bokförd historik eller accepterade avtal skrivs om.

### DR-OPS-12: Klagomål och ansvar

Kunden ska kunna rapportera bokföringsfel, felbetalning, obehörig åtkomst, avgiftstvist och kreditfråga. Systemet ska fördela ansvar mellan Drastic och partner med tidsfrister och eskalering enligt kvalificerade regler och avtal.

**Gräns och undantag:** Kunden ska inte skickas i en cirkel mellan två supportorganisationer utan utsedd ärendeägare.

**Acceptans:** Ett ärende som berör både betalpartner och Drastic behåller en sammanhängande kundsynlig tidslinje.

### DR-OPS-13: Bemanning och tillgänglighet

Produktens öppettider, jour och incidentåtaganden ska motsvara faktisk bemanning och partneravtal. Automatisering kan minska arbete men ska inte ersätta nödvändig oberoende compliance, kreditgranskning eller akut spärrhantering.

**Gräns och undantag:** En ensam utvecklares telefon ska inte marknadsföras som en färdig dygnet-runt-finansoperationsfunktion.

**Acceptans:** Reglerad Money-lansering har dokumenterad ansvarig och reserv för varje kritisk incidenttyp.

### DR-OPS-14: Kundexit och kontinuitet

Exit ska samordna export, senaste kontroller, öppna betalningar, kort, tvister, lån och arkiv. Efter tjänstens slut ska nödvändig läsning och betalningsväg bestå genom rätt ansvarig part.

**Gräns och undantag:** Ett omedelbart raderat tenantobjekt får inte förstöra en kunds fortfarande levande ekonomiska relation.

**Acceptans:** En testkund kan lämna produkten med fullständigt paket och tydligt fördelat ansvar för kvarvarande finansiella avtal.


<a id="chapter-26"></a>

## 26. Ekonomiska tillstånd, kommandon och invariants

### 26.1 En affär har flera tillstånd samtidigt

Drastic ska inte försöka komprimera all ekonomi till `status = done`. En faktura kan vara juridiskt utgiven, levererad, delbetald, delvis bestridd, finansierad och bokförd i en stängd period samtidigt. Det är en normal affärssituation, inte ett schemafel.

| Perspektiv | Typisk tillståndsmodell | Auktoritativ ägare | Ska inte förväxlas med |
|---|---|---|---|
| Bokföringsförslag | draft → prepared → validated → approved → executed; stale och revoked som explicita spärrar | Accounting work | Betalning eller deklarationsinlämning. |
| Fakturadokument | draft → reviewed → issued; credit/correction som egna dokument | Invoicing | Inbetalning och leveransbevis. |
| Leverans | queued → attempted → acknowledged/rejected/unknown | Delivery | Att köparen accepterat prestation eller betalat. |
| Reskontra | ursprung + krediter + allokeringar + återföringar = rest | Receivables/payables | Lån som säkrar eller köper samma fordran. |
| Betalningsavsikt | prepared → approved → reserved → submitted → outcome pending/unknown → externally qualified outcome | Payments | Bokföringsstatus och budget. |
| Avveckling | separata observerade kapitalrörelser, avgifter, returns och refunds | Kvalificerad partner samt intern avstämning | Ett förändrat boolean-fält på originaluppdraget. |
| Kort | issued/active/frozen/closed, plus separata authorisations och presentments | Utgivare och kortadapter | Att kortet är stängt betyder inte att all ekonomisk efterhistoria är slut. |
| Kredit | indicated → applied → approved → offered → signed → conditions satisfied → active → repaid/closed/workout | Långivare/Capital | Likvida medel på banken. |
| Deklaration | prepared → reviewed → signed → submitted → acknowledged/rejected/unknown; amendment som ny version | Tax/filing owner | Skattekontodebitering eller skattebetalning. |
| Prognos | computing → qualified/partial/blocked → saved → superseded | Cash | Ny bokföring eller ny betalningsrätt. |

Ordlistan är en produktmodell, inte en instruktion att införa alla dessa exakta strängar i befintliga enums. Implementationen ska återanvända ägarnas kontrakt och dokumentera mappningen.

### 26.2 Extern handling i fyra delar

**Plan.** Beräkna avsedd effekt med relevanta revisionsberoenden. Modellanrop, dokumenthämtning och rendering sker här utanför ekonomiska lås.

**Tillåt och registrera.** Kontrollera aktuell person, rätt bolag, objektrevision, mandat, budget, mottagare och begränsningar i en kort transaktion. Spara beständig avsikt, idempotensidentitet och köavsikt innan extern sidoeffekt får inträffa.

**Genomför och observera.** Gör anropet utanför DB-transaktionen. Partnerreferens, svarkod, autentiserad webhook och kontoutdrag är olika observationer. Systemet får inte anta att ett saknat svar innebär att inget hände.

**Kvalificera och avstäm.** Den domänägande operationen avgör vilken ekonomisk effekt observationerna styrker. Bokföring och registeruppdatering sker med de vanliga kontrollreglerna. Okända eller motstridiga observationer blir avvikelser med blockerad ny sidoeffekt.

Det finns ingen atomisk transaktion som samtidigt omfattar Drastics databas, kundens bank och en långivare. Produktkravet är beständig avsikt, idempotens, verifierat utfall och kontrollerad kompensation där en sådan är möjlig. En refund är en ny betalning, inte databasrollback av en redan avvecklad betalning.

### 26.3 Invariants som inte får försvagas

| Invariant | Kontrollerad betydelse |
|---|---|
| Bokföringsbalans | Debet och kredit stämmer inom varje finansiell grupp och bokföringsvaluta enligt den godkända exakta modellen. |
| Beloppsbevarande | Delar, avgifter, krediter och allokeringar summerar till rätt ursprung eller redovisad återstående kapacitet. |
| En ekonomisk identitet | Retry, webhookreplay eller ny UI-session skapar inte en andra effekt av samma handling. |
| Aktuell befogenhet | Ett tidigare godkännande kan inte användas efter relevant återkallelse eller ändrad beroenderevision. |
| Separat rättighet | Att få bokföra, flytta pengar, godkänna kredit och lämna deklaration är skilda rättigheter. |
| Underlagets ursprung | Import eller tolkning får inte ändra originalets bytes eller göra en osäker uppgift till verifierad. |
| Likviditetsbevarande | En förflyttning inom samma kvalificerade pengaomfattning ökar inte bolagets sammanlagda pengar. |
| Fordringskapacitet | Samma kända fordringsdel får inte betalas, krediteras eller disponeras ekonomiskt utöver sina tillåtna kapaciteter. |
| Ägarrättigheter | Låntagares huvudbok, långivares fordran och medelsförvarares skuld får inte sammanblandas i samma saldo. |
| Fryst kunskap | Ett sparat beslut bevarar vad som var känt då, även när dagens rättade fakta ser annorlunda ut. |
| Okänt utfall | Ett oklart externt resultat är ett handlingskrävande tillstånd och inte en ursäkt att göra om betalningen. |
| Inte tillämpligt | Tillämplighet bestäms av fakta och regler, inte av vilka moduler utvecklaren hunnit bygga. |

### 26.4 Tvärbokshandlingar

En intercompany-betalning, koncernfinansiering eller partneravräkning kan påverka flera böcker. Varje juridisk person har sin egen giltiga bokföringsgrupp. En koordinator kan hålla samman förloppet men får inte upphäva lokal periodlåsning eller befogenhet.

När ena sidan lyckas och andra sidan väntar ska produkten visa en avstämningsdifferens. Den får inte backa verkligt flyttade pengar genom att radera första sidans bokföring. Ny rättelse eller senare komplettering ska ske i rätt bok och med spårbar referens till den gemensamma händelsen.

<a id="chapter-27"></a>

## 27. Informationsmodell och föreslagna kontrakt

### 27.1 Gemensam identitet och tidsaxel

Alla ekonomiskt relevanta resurser behöver ett explicit scope och tillräckliga tidsbegrepp. Tenant är kundrelationen, legal entity är den juridiska personen och book är den officiella eller uttryckligt analyserade bokföringsomfattningen. Samma bankkonto får inte okontrollerat anslutas som två oberoende saldon i samma scope.

```text
Scope {
  tenantId
  legalEntityId
  bookId?                 // endast när objektet faktiskt hör till en bok
  jurisdictionProfileId
}

TemporalBasis {
  effectiveAt            // när händelsen ekonomiskt gäller
  observedAt?            // när en extern källa uppgav den
  recordedAt             // när Drastic beständigt registrerade den
  knownAtCutoff          // vilken kunskap ett snapshot får använda
}

Money {
  currency               // kvalificerad valutakod
  minor                  // kanonisk signerad heltalssträng
}

ExactRate {
  numerator
  denominator            // strikt positiv
  unitBasis              // valutapar, årsränta, pris per enhet eller annan definierad grund
  sourceRevision
  effectiveInterval
}
```

Valutans skala ska komma från kvalificerat kontrakt. En generell extra `scale` som varje klient får ändra ska inte kunna omtolka ett bokfört belopp. Kommersiella priser kan behöva annan precision än slutliga pengar och ska därför ha egna modeller. Alla presenterade procenttal ska kunna skiljas från de exakta värden som används i beräkningen.

### 27.2 Ekonomisk händelse och bevis

```text
EconomicRelation {
  id, scope, relationType
  fromOwner, fromObjectId, fromRevision
  toOwner, toObjectId, toRevision
  componentId?
  amountCapacity?
  effectiveAt, recordedAt
  provenance
}

EvidenceReference {
  evidenceId, importOccurrenceId
  originalObjectId, contentDigest, mimeType
  assertedBy, sourceSystem, sourceObjectId?
  observedAt, receivedAt
  coverageDescriptor
}
```

Relationstyper ska vara namngivna och begripliga: `settles`, `credits`, `reverses`, `replaces_forecast_occurrence`, `finances`, `assigns`, `repays`, `evidences`, `internal_transfer_leg` och `delivers`. Detta är inte krav på ett universellt relationsbord. Befintliga domäntabeller bör behålla auktoriteten. En samlad läsmodell får komponera dessa relationer för sökning och förklaring.

### 27.3 Betalningskontrakt

```text
PaymentIntent {
  id, scope, economicPurpose
  sourceOwner, sourceObjectId, sourceRevision
  payerLegalEntityId
  fundingAccountRef, beneficiaryRevisionRef
  principal, maximumFee?, requestedExecutionDate
  latestPermittedExecutionDate?
  approvalBasisDigest
  productProfileRef, providerRouteRef
  idempotencyKey
}

ExecutionAttempt {
  intentId, attemptOrdinal
  allowedSideEffectIdentity
  providerId, providerIdempotencyKey?
  requestDigest, authorityRevision
  admittedAt, submittedAt?
  providerReference?
  responseObservationRef?
  uncertaintyReason?
}

ProviderObservation {
  id, providerId, externalEventId, externalObjectId
  authenticationResultRef
  observedAt, receivedAt, providerSequence?
  rawEvidenceRef
  interpretedType, interpretedVersion
  linkedIntentId?, qualifiedOutcomeRef?
}
```

`attemptOrdinal` är ett tekniskt försök, inte en ny ekonomisk betalning. Två leverantörsrutter får inte samtidigt vara fria att göra samma sidoeffekt när första rutten är okänd. Mottagarreferens ska peka på en oföränderlig granskad version, inte på en muterbar kontaktpost.

### 27.4 Cash och framtida åtaganden

```text
CashEvent {
  economicOccurrenceId
  scope, cashPerimeterRef
  sourceOwner, sourceObjectId, sourceRevision
  flowKind, nativeMoney
  dueDate?, expectedDate?, dateRange?
  amountBasis: fixed | qualified_estimate | scenario
  dateBasis: contract | verified_promise | reviewed_model | manual_assumption
  availabilityClass
  replacementRelationRefs[]
  outstandingCapacityRef?
  exclusionReason?
}

CashSnapshot {
  id, scope, asOf, horizonEnd
  bankObservations[], sourceWatermarks[]
  sourceMembershipDigest
  cashPerimeterRevision
  ruleVersion, calculationVersion
  assumptions[], coverageGaps[]
  dailyBalances[], minimumBalance, minimumDate
  buffer, liquidityHeadroom
  qualification: qualified | conditional | partial | blocked
}
```

En ersättningsrelation är viktigare än ett generellt `deduplicated=true`. Användaren ska kunna se att ett uppskattat lönebelopp ersattes av en fastställd lönekörning och att samma lönekörning senare ersattes av verkliga betalningar i startsaldot.

### 27.5 Risk och beslut

```text
RiskSnapshot {
  id, purposeId, subjectScope
  subjectType: legal_entity | natural_person | portfolio
  lawfulDataUseRef
  knownAtCutoff, sourceMembershipDigest
  featureSetVersion, featuresWithProvenance[]
  dataQuality, missingMaterialInputs[]
  modelVersion?, policyVersion
  resultsByRiskFamily
  qualifications[], expiryOrRefreshPolicy
}

DecisionRecord {
  id, decisionType, subjectScope
  riskSnapshotRef?, economicPlanRef
  authorisedDecisionMaker
  decision, conditions[], reasonCodes[], permittedExplanation
  overrideRef?, effectiveAt, expiresAt?
  previousDecisionRef?
}
```

En sekretessbegränsad AML-utredning får inte läcka via `permittedExplanation`. Riskresultat ska inte kunna återanvändas för ett nytt ändamål bara för att samma bolag är subject. Ett scoresvar utan rätt ändamål och datalicens ska vägras.

### 27.6 Capital och servicing

```text
Facility {
  id, borrowerLegalEntityId, lenderLegalEntityId
  productRevision, agreementDigest, signedArtifactRefs[]
  currency, committedLimit, availableToDrawBasis
  conditionsPrecedent[], securityRefs[], assignmentRefs[]
  interestPolicyRef, feePolicyRef, repaymentWaterfallRef
  effectiveDate, maturityDate, servicingOwner
}

LoanMovement {
  id, facilityId, drawId?, movementType
  principalDelta, interestDelta, feeDelta
  effectiveDate, valueDate?, recordedAt
  sourcePaymentOrAssessmentRef
  originalMovementRef?, correctionReason?
  lenderBookPostingRef?, borrowerBookEvidenceRef?
}

ReceivableAssignment {
  id, originalReceivableRef, assignedComponentScope
  assignorLegalEntityId, assigneeLegalEntityId
  agreementRevision, notificationEvidenceRef?
  legalQualificationRef, accountingQualificationRef
  assignedAmount, reserveOrResidualTerms
  paymentDestinationRevision
}
```

Dessa kontrakt är en ansvarskarta. De ska inte implementeras som dubbla register om befintlig ägare redan har motsvarande ekonomiska identiteter. `borrowerBookEvidenceRef` betyder inte att långivarens servicingfunktion får skriva i låntagarens bok utan behörighet.

### 27.7 Redovisningsexempel och registerperspektiv

Kontonummer är medvetet inte hårdkodade här. Varje faktiskt bokföringsförslag ska använda bolagets granskade kontoroller och regelprofil.

| Händelse | Låntagarens/säljarens perspektiv | Långivarens/partnerns perspektiv | Cash |
|---|---|---|---|
| Lån betalas ut | Bank ökar; skuld och kvalificerad avgiftsbehandling registreras. | Fordran och utbetalning enligt egen redovisning. | Nettoutbetalning en gång. |
| Faktura belånas | Kundfordran består om profilen kräver det; lånerelation tillkommer. | Säkerhet och lån, inte automatiskt köpt försäljning. | Förskott och framtida reglering enligt kontrakt. |
| Kvalificerat fakturaköp | Avyttring/fortsatt engagemang bedöms enligt avtalet och redovisningsregler. | Köpt fordran och köpeskillingsskuld enligt egen profil. | Initial likvid plus eventuell restlikvid, inte hela kundbetalningen igen. |
| Kortköp | Kostnad/tillgång och rätt betalnings- eller kortskuld. | Utgivarens egna fordringar och settlement. | Tillgänglighet påverkas av rätt hold/presentment, utan dubbel avräkning. |
| Refund | Ny inbetalning eller reducerad skuld med länk till ursprung. | Ny utgående eller återförd position. | Verklig återbetalning, inte raderat historiskt köp. |

<a id="chapter-28"></a>

## 28. Kompletta tvärgående kundresor

### J-01: Ägarlett AB blir Native-kund

**Ingång:** bolaget vill ersätta sitt nuvarande bokföringsprogram. **Förutsättning:** faktisk bolagsprofil, historisk källa, åtkomst och planerad granskare är kända.

Kunden väljer period och källor. Drastic visar en inventering med fullständiga, saknade och osäkra underlag. Rekonstruktionsprovet behandlar verkliga källor genom normala arbetsytor. Migrationsprovet verifierar separat att tidigare bokföring och öppna poster överförs rätt. Granskaren får standardunderlag och källindex. Efter parallell drift och återställningsprov beslutas bryttid.

**Ekonomiska effekter:** inga dubbla intäkter vid import av öppna fakturor och inga externa inlämningar bara för att perioden räknats om. **Felväg:** differens blockerar endast berörd färdigställandestatus och skapar en konkret uppgift. **Avslut:** avstämd omfattning med accepterat granskningspaket och senare separat cutovergodkännande. Ägare: CORE, ACC, CLOSE, WORK.

### J-02: Ett företag använder Cash ovanpå befintlig bokföring

**Ingång:** kunden vill se likviditet men inte byta huvudbok. Drastic ansluter en läsande profil och inventerar bank, fakturor, lön och skattekonto. Källsystemet behåller officiell bokföring. Ett gemensamt datum och kända luckor kvalificerar prognosen.

Kunden ser en utgiftsrisk om tre veckor och flyttar en väntad kundbetalning i ett scenario. Ändringen sparas inte i källfakturan. En felaktig fakturarest leder till rättelse i dess systemägare och en ny prognos efter synk.

**Felväg:** förnyelse av samtycke misslyckas. Senaste data går att läsa med datum, men ny aktuell prognos etiketteras inte komplett. **Avslut:** verklig beslutsnytta utan migrationstvång eller dubbla officiella böcker. Ägare: CORE, INT, CASH.

### J-03: Från leverantörsfaktura till betalning

En ny faktura anländer. Document intake bevarar original. AP länkar beställning och eventuell leverans. Skattefakta granskas och Accounting förbereder rätt effekt. En ny mottagaruppgift ger separat kontroll. Kostnaden kan bokföras medan betalningen fortfarande väntar på attest.

Kunden granskar exakt belopp, datum, konto och mottagare. Payments registrerar avsikten före anrop. Partnern tar emot men svaret tappas. Gränssnittet visar okänt utfall och blockerar ny betalning. Avstämning hittar partnerreferensen och bankraden. En enda betalning reglerar restbeloppet och försvinner från framtida Cash när den redan ingår i startbank.

**Avslut:** original, kostnad, skuld, betalning och kvitto kan följas i båda riktningar. Ingen orderstatus ersätter mottagarverifiering. Ägare: AP, TAX, ACC, PMT, CASH, OPS.

### J-04: Prenumeration med usage, prisändring och misslyckat uttag

Avtal anger grundavgift och användningspris. Usage-händelser tas emot med idempotens. Kunden ser periodens debiteringsgrund före faktura. En avtalsändring gäller från en framtida tidsgräns och kan inte återidentifiera föregående cykel.

Billing skapar ett utgivningsunderlag som Invoicing ger ut en gång. Ett kortuttag misslyckas. Fakturan finns kvar och Payments gör ett separat kvalificerat retryförsök enligt mandat. Om kunden bestrider viss usage får den delen en tvist och eventuell senare kredit. Intäktsperiodisering följer leveransen, inte antalet betalningsförsök.

**Avslut:** en ekonomisk debitering, separata betalningsförsök och exakt slutrest. Ägare: BILL, INV, PMT, COL, ACC.

### J-05: Kortköp på resa med ändrat belopp

En anställd har ett godkänt resekort med bolagsgräns. Hotellet reserverar 1 000, frigör 300 och avräknar 650. Kvarvarande hold frigörs enligt utgivarens observation. Anställd laddar upp kvitto. Skattebedömning och affärsändamål granskas innan kvalificerad bokföring.

Efter anställningsavslut kommer en refund på 200. Kortet förblir spärrat för nya köp, men återbetalningen följs till bolaget. Nettoköp är 450. En tillfällig reklamationskredit hade i stället fått egen provisorisk klass tills beslut kommit.

**Avslut:** budgetsaldon, kortskuld, kassa och kostnad kan förklaras utan att återbetalningar tappas vid kortavslut. Ägare: CARD, AP, PMT, ACC, OPS.

### J-06: Lön, skattekonto och betalningsbehov

Payroll fastställer netto, skatt, avgifter och bokföringsförslag med rätt regelpaket. Fastställd körning ersätter Cashs löneuppskattning. Betalningsgodkännaren ser nettobatchen och signerar separat. En mottagare avvisas av banken medan övriga löner avvecklas.

Rättelse av den avvisade mottagaren påverkar bara den individens utbetalningsuppdrag. Tax förbereder relevanta deklarationsversioner och skattekontots framtida finansieringsbehov. Redan innestående medel på skattekontot dras från top-up, inte från kostnaden.

**Avslut:** körning, nettobetalningar, kontrollkonton och myndighetsunderlag stämmer. Betald status är inte samma sak som inlämnad AGI. Ägare: PAY, TAX, CASH, PMT, CLOSE.

### J-07: Likviditetsrisk leder till partnerfinansiering

Cash visar att 150 000 behövs före kundbetalning. Kunden prövar först scenario för senare investering och tidigare kundbetalning. Kunden väljer sedan att ansöka om finansiering hos namngiven partner och granskar datadelningen.

Risk kvalificerar faktaunderlag. Långivaren ger ett tidsbegränsat erbjudande. Kunden ser netto, kostnad, återbetalningsdatum och säkerheter samt Drastics eventuella ersättning. Signering skapar avtal, inte bankmedel. Först verifierad utbetalning ger observerad likviditet. Planerade amorteringar och räntor ingår samtidigt i Cash.

**Avslut:** finansieringen har minskat det specifika underskottet utan att dölja nästa betalningsbelastning. Ägare: CASH, FIN, RISK, CAP, PMT.

### J-08: Faktura finansieras och slutkunden betalar delvis

Säljaren väljer en kvalificerad fordran. Avtalet bestämmer om det är ett lån med säkerhet eller ett köp. En intern kapacitetskontroll och dokumenterad extern rättighetsprövning genomförs. Betalningsinstruktion och eventuell underrättelse bevaras.

Efter utbetalningen bestrider slutkunden en del och betalar resten till rätt finansieringsmottagare. Collections hanterar tvisten, Capital uppdaterar avräkning och eventuell regress enligt avtalet. Cash visar endast de belopp som säljaren faktiskt väntas få. Bokföringsrättelser följer separat kvalificerad profil.

**Avslut:** finansieringskapital, kundfordran, kvarstående tvist och eventuell restlikvid går att stämma av. Samma slutkundsbetalning ökar inte både långivarens och säljarens bank fiktivt. Ägare: INV, FIN, CAP, COL, CASH, ACC.

### J-09: Grundaren flyttar överskottslikviditet

Treasury hittar ett föreslaget överskott efter buffert och skyldigheter. Kunden ser tillgänglighet, bindning, avgifter, leverantör och motpartsexponering. Destinationen är kvalificerad. Planen godkänns och aktuell bankposition kontrolleras igen innan handling.

Om en lönebetalning hunnit reservera medel stoppas eller minskas förslaget enligt mandatet. En växlingsquote som löpt ut behöver ny kvalificering. Under överföring räknas pengar inte på både källa och destination.

**Avslut:** bättre fördelning utan ändrad total kassa bortsett från verkliga fees/FX och utan att sena skatter finansieras med osäker tillgänglighet. Ägare: TRE, CASH, PMT.

### J-10: Redovisningsbyrån stänger fem klienter

Byråportföljen visar period, ansvarig och blockerande områden för varje klient. En konsult begär underlag från en kund och granskar en annan klients färdiga period. Firmamedlemskap ger inte automatiskt bokåtkomst. Ett ifyllt notfält kräver källa och ansvarig innan årsartefakt fastställs.

En klient har en partnerlånerest som inte stämmer. Konsulten öppnar servicingunderlag och avstämning utan åtkomst till långivarens andra kunder. Den avvikande klienten förblir öppen medan andra kan avslutas. Exporterna provas i det avsedda granskningsverktyget.

**Avslut:** produktiv portföljhantering med samma kvalitet per klient, inte en blankettsignering av alla. Ägare: WORK, CLOSE, ACC, CAP, CORE.

### J-11: Återställning efter allvarlig driftincident

Finansiell skrivning pausas. Databas, original och kölägen återställs till senaste verifierade punkt. Observerade externa betalningar som inträffat därefter jämförs med bevarade avsikter och leverantörsutdrag. De får inte återutföras.

Operatören följer exakt vilka uppdrag som återfunnits, fortfarande är okända eller aldrig skickats. Ekonomiskt beslutsfattande är blockerat tills rätt scope är avstämt och en enda writer aktiverats. Kunden får korrekt information om dataaktualitet och pågående betalningskontroll.

**Avslut:** en övad, bevisad återkomst till drift utan förlorad eller dubblerad extern sidoeffekt. Ägare: OPS, PMT, INT, ACC.

### J-12: Kunden lämnar Drastic med aktiva finansiella produkter

Kunden får export av bokföring, original, avtal och öppna poster. Nya kortköp och nya lån kan stoppas, medan refunds, reklamationer och återbetalningar fortsätter hos rätt partner. Följande officiella redovisningssystem får avgränsade ingående uppgifter.

Avslutet specificerar läsåtkomst, retention, kostnader och ansvar. Partnerrelationer sägs inte upp genom att tenantflaggan ändras. Kunden ska ha kvar korrekt betalningsmottagare för sitt lån och kunna rätta tidigare bokföring genom rätt process.

**Avslut:** inga fängslande beroenden, borttappade pengar eller historiska anspråk. Ägare: CORE, OPS, INT, CAP, CARD, CLOSE.


<a id="chapter-29"></a>

## 29. Systemarkitektur och utvecklingsgränser

### 29.1 Fortsätt från openERP

Den selektivt granskade revisionen använder Effect för applikationsoperationer, PostgreSQL med native Effect/Drizzle-adapter, TanStack och StyleX för produkten samt en separat effect-mq/Bun-process för beständigt bakgrundsarbete. Denna PRD väljer att fortsätta där, inte att starta om i en ny stack. [R01, R02]

```text
                           Kund / redovisningspartner
                                    │
                    Web + REST + MCP med samma kontrakt
                                    │
                 Identitet, bolagsscope och aktuell auktoritet
                                    │
                     Namngivna Effect-operationer
                                    │
      ┌─────────────────┬───────────┼──────────┬─────────────────┐
      │                 │           │          │                 │
 Accounting work      Revenue      Money      Risk            Capital
      │                 │           │          │                 │
      └─────────────────┴───────────┼──────────┴─────────────────┘
                                    │
          PostgreSQL: relationsdata, integritet, receipts och outbox
                         │                       │
                   Originalarkiv          Separat Bun-worker
                                                 │
                       kvalificerade banker, betalpartners,
                       långivare, myndigheter och validators
```

Skissen visar logiska ansvar. Den betyder inte att varje ruta ska bli en microservice. Börja med modulär monolit. Separera runtime när latens, säkerhetsklass, tillstånd, operativt ägarskap eller oberoende skalning verkligen kräver det.

### 29.2 Ägarmappning innan kod skrivs

| Föreslaget ansvar | Utgå från | Utvidgningens gräns |
|---|---|---|
| Företagsprofil och aktivering | Befintliga company profile- och identitetsägare. | Lägg inte en andra capability flag-motor i frontend. |
| Arbetslista och kundresor | `apps/web` och befintlig attention-/work-komposition. | Samma objektlänkar, fel och receipts i alla vyer. |
| Bokföring | Befintliga Effect-operationer och transaktionspasserad persistence. | Ingen återinförd generell SQL-featuredispatcher. |
| Svenska regler | Befintlig `jurisdictions/se` och kvalificerade domänägare. | Produktberedskap kräver faktiska regelprofiler, inte bara rena räknare. |
| Cash | Befintliga läsägare plus ny avgränsad prognosägare där den saknas. | Historisk kassaflödesrapport behåller sin ägare. |
| Payments | Befintliga export-, leverantörs- och betalningsoperationer där de finns. | Ny extern exekveringsägare ska ha tydligt mandat och receipts. |
| Cards | Ny kvalificerad kortprogramsadapter och kortlivscykel. | Kortkostnaden bokförs via samma Accounting/AP, inte en ny kostnadsmotor. |
| Billing | Befintliga återkommande fakturor och kommersiell kapacitet. | Usage/prissättning utvidgar verkliga ägare och får inte omidentifiera cykler. |
| Risk | Kvalificerade läsmodeller och separat modell-/policyregister. | Ingen generell alternativ företagsdatabas utan ändamål och proveniens. |
| Capital | Ny eller utvidgad avtals-/servicingägare efter kartläggning. | Partner- och låntagarbok hålls isär. |
| Integrationslager | Befintlig credential-, provider- och runtimeinfrastruktur. | Adaptrar ska inte innehålla egen dold bokföringspolicy. |
| Plattformens avgifter | Billing i Drastics egen juridiska bok. | Kundens data är inte Drastics bokföringsutrymme. |

Nuvarande implementation ska inspekteras vid genomförandet. Tabellen är inte en frånvaroförteckning. Ett redan implementerat eller planägt område ska kompletteras där, inte dupliceras bara för att denna PRD använder ett nytt produktnamn.

### 29.3 PostgreSQL och integritet

Applikationen äger affärspolicy, beräkningar, behörighet och scoped writes. PostgreSQL äger transaktioner, lås, relationer, constraints och det smala integritetslagret. Read models, model caches och köstatus är inte fristående finansiella auktoriteter.

Låsordning ska följa befintligt kontrakt. Nya domäner behöver dokumentera var deras resurser hamnar i ordningen. Ingen extern nätverksbegäran, LLM-körning, filrendering eller stor analys ska hållas inne i finansiella transaktioner. Beräkna utanför lås och bekräfta relevanta revisioner innan ett nytt resultat förseglas.

Innan en sparad Cash- eller Risk-beräkning betecknas aktuell ska det kontrolleras att de materiella beroendena inte ändrats. Ett gammalt sparat snapshot förblir läsbart som historiskt även om det inte längre är aktuellt för en ny handling.

### 29.4 Asynkronitet och läsmodeller

Outbox beskriver avsedd leverans efter commit. Kömotorn hanterar försök och leases. Domänen äger ekonomisk identitet, cancellation, aktuell auktoritet och effektkvitto. Dubbelleverans är ett normalt designfall.

Projectioner ska kunna byggas om från sina auktoritativa ägare. Varje projection behöver versionsgräns och källvattenmärke. Om en användare just godkänt ett förslag ska nästa vy antingen läsa rätt auktoritet eller visa att sammanställningen ännu inte nått det kvittot. Den får inte ge ett falskt felbesked bara för att sökindexet ligger efter.

### 29.5 Isolation och juridiska gränser

All kunddata ska ha serverhärlett bolagsscope. Koncernrapportering och byråportfölj kräver en uttrycklig mängd tillåtna bolag. Ett API får inte acceptera fritt bytt `legalEntityId` i ett redan förseglat resursobjekt.

Egen reglerad kreditverksamhet kan motivera separat juridisk person, databehandling, nätverksåtkomst och deployment. Separation ska grundas i risk och skyldighet. Den ska inte användas som argument för att dela kunddata fritt mellan bolag eller för att licensskyldigheter automatiskt försvinner.

### 29.6 Inga spekulativa plattformsbyggen

Ett generellt event-sourcingramverk, egen grafdatabas, eget identitetssystem, global regelspråksmotor, cross-cloud aktiv-aktiv-finansiell writer och egen betalrail är inte krav för första versionerna. Varje sådant beslut kräver mätt problem, definierad konsument och ett dokumenterat alternativ.

Bend-verifiering eller andra formella hjälpmedel kan ge extra bevis för rena kalkylkärnor. De ersätter inte aktuell regelkvalificering, PostgreSQL-transaktioner, browserresor eller riktig partneracceptans. Ingen förändring av finansiell beräkningsägare följer automatiskt av denna PRD.

<a id="chapter-30"></a>

## 30. UX-kontrakt och informationshierarki

### 30.1 Navigation

En föreslagen huvudnavigation är **Översikt, Att göra, Pengar, Försäljning, Inköp, Bokföring, Lön, Skatt, Rapporter och Inställningar**. Redovisningsbyråer börjar i Klienter. Finansiering finns både kontextuellt och i Pengar. En stor separat Risk-flik är inte obligatorisk för företagaren; Risk är främst bakomliggande förklaring, kontroll och specialistyta.

Oaktiverade funktioner ska presenteras som tydliga möjligheter eller döljas beroende på sammanhang. Produktens startsida får inte bli ett rutnät med tomma moduler. Företag som bara använder Cash ska inte behöva navigera en låtsasaktiv huvudbok.

### 30.2 Information före handling

Ett betalningskort ska i första nivån visa mottagare, belopp, valuta, källa, datum och vad som händer efter bekräftelse. En kreditacceptans ska visa nettoutbetalning, total känd kostnad, betalningsprofil och väsentliga säkerhetsvillkor. Långa avtalsdetaljer får vara fördjupning men får inte ersätta begriplig sammanfattning av det som accepteras.

Färger ska stödja betydelse utan att vara enda bärare. Grönt reserveras inte för allt som är tekniskt lyckat. Ett neutralt färdigställt beredningssteg ska inte förväxlas med verifierad extern avveckling.

### 30.3 Tydliga mikrotexter

| Undvik | Använd i rätt tillstånd |
|---|---|
| Bokfört automatiskt, när det bara finns ett förslag | Förberett för granskning. |
| Betalt, när partnern bara mottagit uppdraget | Betalningsuppdrag mottaget. Utfall kontrolleras. |
| Dina pengar, när det är indikativ kredit | Preliminär finansieringsmöjlighet. Kreditbeslut återstår. |
| Skatt betald, när pengar förts till skattekontot | Överföring till skattekontot genomförd. |
| Allt klart, när en källa saknas | Inget mer arbete i inlästa uppgifter. Underlag från konto X saknas. |
| Godkänn allt säkert | Godkänn dessa 12 granskade förslag. |
| AI säger att kunden är dålig | Försenade betalningar i angiven period. Underlag och beräkning. |
| Konto skyddat, utan produktgrund | Kontotyp och skydd enligt namngiven leverantörs villkor. |

### 30.4 Tillgänglighet

Alla prioriterade kundresor ska fungera med tangentbord, synlig fokusordning och 200 procents zoom. Mobila vyer ska tillåta granskning av dokument, belopp och primär handling utan att gömma väsentliga uppgifter. Kritiska kontroller ska inte kräva hover.

Långa listor ska ge serverbaserat urval, läsbar summa för just urvalet och tydlig paginering. Delvis inläst lista får inte presentera en totalsumma för hela bolaget. Valutabelopp ska ha rätt valuta och minsta precision även i kompakta kort.

### 30.5 Specialisternas ytor

Finansoperationskonsol, modellregister, juridiska profiler och regulatorisk rapportering ska ha egna roller och navigation. Dessa ytor får inte belasta vardagskunden men ska vara verkliga produkter med ägare, tidslinje och verifierad återhämtning.

En avancerad funktion får inte gömma sin enda fungerande felväg i utvecklarkonsolen. Specialiståtgärder som korrigerar ekonomiskt läge ska använda kontrollerade operationer med samma audit trail som vanliga kundhandlingar.

<a id="chapter-31"></a>

## 31. Regulatorisk produktkarta och aktiveringsgränser

### 31.1 Separata verksamheter, inte en enda FI-status

Detta är en produktkarta för juridisk kvalificering, inte ett tillståndsbesked. Bedömningen ska göras för faktisk tjänst, avtal, marknadsföring och medelsflöde. Ett tekniskt partnerupplägg kan förändra rollen men avgör inte ensamt om Drastic är teknisk leverantör, ombud, förmedlare eller själv tillhandahållare.

| Produkt eller beteende | Kontrollerad extern utgångspunkt | Produktens lanseringsvillkor |
|---|---|---|
| Ren programvara för bokföring | Ska skiljas från att faktiskt bedriva redovisnings- eller skatterådgivningsverksamhet. Sådana tjänsteutövare har AML-frågor att hantera. [E10] | Tjänsteroll och ansvar i erbjudandet ska prövas; AI är inte en klassificering. |
| Företagskredit och förmedling | FI beskriver registrering för yrkesmässig verksamhet som lämnar eller förmedlar företagskredit och medverkar vid factoring/leasing. [E01] | Prövning sker före faktisk förmedling, inte först när Drastic lånar ut eget kapital. |
| Kontoinformation | FI beskriver en särskild registreringsväg för den som endast tillhandahåller kontoinformationstjänster. [E02] | Read-only är inte ett automatiskt undantag. Partnerroll eller egen registrering ska vara kvalificerad. |
| Betalningsinitiering och andra betaltjänster | FI beskriver tillstånd för betaltjänster och särskild ombudsmodell. [E02] | Kundavtal, huvudman, anmälan/tillstånd och faktisk ansvarsfördelning ska verifieras. |
| E-pengar eller värdebärande wallet | Utgivning av e-pengar har en separat tillståndsram. [E03] | Intern budget ska inte glida över till förvaring eller utgivning utan ny klassificering. |
| Kortprogram | Utgivning och betalningsfunktioner måste kvalificeras i faktiskt program. [E02, E11] | Utgivare, scheme/processoransvar, datamiljö och avvikelsehantering ska vara fastställda. |
| Inkasso | FI beskriver tillstånd för indrivning åt andra eller fordringar som övertagits för indrivning samt särskilda undantag. [E04] | Påminnelseprodukt och inkassotjänst skiljs; undantag antas inte från en allmän registrering. |
| Extern kreditupplysning | IMY har separat tillståndsprocess för kreditupplysningsverksamhet. [E05] | Risk-API och delning ska bedömas som egen verksamhet innan försäljning. |
| Personbaserade automatiserade beslut | GDPR:s regler kan beröra betydande helt automatiserade beslut om individer. [E06, E17] | Personroller, rättslig grund och fungerande prövning ska kvalificeras. |
| AI-baserad personkreditbedömning | AI Act behandlar kreditvärdighet/kreditpoäng för fysiska personer som en särskild hög-riskanvändning, med avgränsningar. [E07] | Dokumenterad AI-klassificering och tillämplig tidsversion före användning. |
| Operativ motståndskraft | DORA berör finansiella aktörers IKT-risk och externa leverantörer på olika sätt. [E08] | Direkt tillämplighet och partneravtalade skyldigheter hålls isär. |
| Treasuryplaceringar | Kontoallokering, växling, värdepappersförmedling och rådgivning är inte samma aktivitet. | Separat juridiskt beslut för faktisk tjänst; investeringstjänster är inte automatiskt aktiverade av denna målbild. |

### 31.2 AI-reglernas version är viktig

Den kontrollerade EUR-Lex-sidan avser konsolideringen från **27 juli 2026** och visar ändringen genom förordning **2026/1744**. Produktteamet ska därför inte använda en gammal förenklad lanseringskalender som enda rättslig grund. Tillämplighet och tidsfrister ska bindas till aktuell artikel 113 och den berörda användningen. [E07]

Drastics produktkrav på proveniens, mänskligt beslutsansvar, validering och incidenthantering gäller från den egna produktaktiveringen. En senare rättslig tillämpningsdag är inte ett skäl att lansera en okontrollerad modell.

### 31.3 Vad en reglerad release behöver

En kvalificerad release ska ha en skriftlig rollbedömning, utsedd ansvarig juridisk person, verifierade partnerbehörigheter, kundvillkor, ändamåls- och datamatris, AML/sanktionsprocess när relevant, incident- och klagomålsprocess, avstämning, exit samt observerad leverantörsfunktion.

Dessa underlag ska vara versionsbundna till produktens faktiska land, kundtyp, valuta och handling. Om en ny produkt börjar förvara pengar, förmedla kredit eller använda persondata på annat sätt är det en ny kvalificering, inte bara en feature flag.

### 31.4 Faktiska företagsregler

Bokföring och skatt kräver daterade, tillämpliga regelprofiler. BFN:s generella arkiveringsregel innebär sju år efter kalenderåret då räkenskapsåret avslutades. Denna skyldighet är inte samma sak som ett abonnemangs livslängd. Förvaringsplats, läsbarhet och återställning ska kvalificeras för den verkliga driftmodellen. [E13]

Bolagsverkets digitala inlämning och relevanta e-fakturaformat ska användas genom kvalificerade aktuella kanaler. En fil som skapats lokalt är inte externt mottagen. Krav som gäller offentlig e-fakturering ska inte felaktigt generaliseras till alla svenska B2B-fakturor. [E14, E15]

<a id="chapter-32"></a>

## 32. Partnerstrategi och upphandlingskrav

### 32.1 Vad Drastic ska äga

Drastic ska äga den synliga kundresan, källrelationerna, domänkontrakten, kvalificerad beräkning, kundens behörigheter, ekonomiska förklaringar och oberoende avstämning. Drastic ska kunna upptäcka att en partner lämnat ofullständiga eller motsägande utfall.

Bank-, betal-, kort- och kreditinfrastruktur ska kunna levereras av partners med tydliga gränser. Partnern kan vara systemet för faktisk medelsförvaring, kortauktorisation eller kreditbeslut. Drastic får inte låtsas vara samma juridiska tjänsteleverantör genom ett mer sammanhållet gränssnitt.

### 32.2 Föreslagen ansvarsmatris

Bokstäverna betyder A: ytterst ansvarig enligt det valda avtalet, R: praktiskt utförande och C: medverkande. Matrisen är ett förslag att kvalificera, inte ett faktiskt ingånget avtal.

| Funktion | Kund | Drastic | Reglerad partner / specialist |
|---|---|---|---|
| Bokföringsunderlag och bolagsfakta | A/R | Verktyg och kontroller | C där redovisningspartner anlitats. |
| Plattformens operationer och åtkomst | C | A/R | C vid delegerad identitet. |
| Kundens betalningsbeslut | A/R genom behörig person | R för exakt förberedelse och delegation | R för bank-/leverantörssignering enligt modell. |
| Avveckling och medelsförvaring | C | R för observation och kundvy | A/R där tjänsten tillhandahålls av partner. |
| Kortutgivning och schemahantering | C | R för upplevelse, kostnadsflöde och avstämning | A/R enligt program. |
| Kreditbeslut och finansiering | R för korrekta ansökningsfakta | R/C enligt förmedlar-/servicingroll | A/R för partnerkredit. |
| AML-utredning och rapportering | C när uppgift behöver lämnas | Eget ansvar enligt faktisk roll | Eget ansvar enligt faktisk roll, inte generellt delegerbart bort. |
| Klagomål | Initierar | R för sammanhängande ärende och egna fel | A/R för sina beslut och tjänster. |
| Myndighetsdeklaration | A enligt bolags-/företrädarroll | Verktyg och avtalad leverans | R där behörig specialist eller kanal används. |
| Felaktig betalning och ekonomisk förlust | Enligt avtal och tillämpliga regler | Eget avtalat/faktiskt ansvar | Eget avtalat/faktiskt ansvar. |

### 32.3 Partner-RFI

Innan en partner väljs ska följande frågor besvaras med underlag, inte säljlöften.

| Område | Krävt svar |
|---|---|
| Roll | Vem är kundens avtalspart, kontohållare, utgivare, långivare och betalningsutförare? |
| Tillåtelse | Vilka länder, kundtyper, produkter och roller omfattas av aktuell behörighet? |
| Pengar | Vem äger varje saldo, var förvaras medel och vad händer vid insolvens? |
| Identitet | Vem gör KYB/KYC, firmamandat, omprövning och samtyckesförnyelse? |
| Kommandon | Vilka operationsidentiteter och idempotensgarantier finns, och hur länge gäller de? |
| Okänt utfall | Hur återfinns ett mottaget kommando när svaret tappats? |
| Observationer | Finns stabila event-ID:n, signaturer, sekvenser, statusläsning och fullständig avräkningsfil? |
| Redovisning | Kan brutto, netto, avgifter, FX, reserver, refunds och returns förklaras separat? |
| Försening | Vilka klipptider, helgdagar, settlementfördröjningar och meddelandefördröjningar gäller? |
| Kort | Hur hanteras offlineauktorisation, sena presentments, tokenbyte och refund till stängt kort? |
| Kredit | Vem sätter villkor, bär kapitalförlust, kräver återköp och hanterar regress? |
| Support | Vilka incidenter har bemannad jour, vem äger kundärendet och hur ser eskaleringen ut? |
| Data | Vilka underleverantörer, regioner, retentionstider och modelländamål används? |
| Ekonomi | Fast avgift, minimivolym, rörlig avgift, reserver, garantier, bindning och exitkostnad? |
| Avslut | Hur flyttas data, aktiva avtal, öppna utfall och fortsatt kundservice vid uppsägning? |
| Ändringar | Hur långt förvarsel ges för schema, pris, landstöd och produktavslut? |

**Diskvalificerande för automatisk betalningsdrift:** avsaknad av säker återidentifiering av externt utfall, oklar juridisk ägare av medel, avräkning som inte kan förklara kundpositioner eller avsaknad av fungerande incidentväg. En partner kan ändå passa för ett mer begränsat manuellt eller läsande användningsfall efter kvalificering.

### 32.4 Multi-provider utan oärlig portabilitet

Avtals- och datamodellen ska kunna bära flera providers men första genomförandet bör kvalificera en konkret väg åt gången. Vid byte kan nya uppdrag routas till annan partner medan gamla fortsätter avstämmas hos den förra. En gemensam adapter betyder inte att gamla konton, medgivanden, korttokens eller lån kan flyttas utan kundhandling och ny prövning.

<a id="chapter-33"></a>

## 33. Affärsmodell, produktpaket och kapitaldisciplin

### 33.1 Värde som kan betalas för

Drastic ska kunna ta betalt för en kvalificerad driftad arbetsprodukt: mindre manuell ekonomiadministration, bättre avstämning, sammanhållen försäljning och förklarbar likviditet. Den kommersiella hypotesen ska prövas i verkliga pilotbolag innan stora breddinvesteringar motiveras med antagen finansieringsintäkt.

En möjlig paketering är **Core**, **Operations**, **Money** och **Capital access**. Core omfattar driftad bokföring eller ansluten ekonomivy. Operations tillför bredare automation, billing och byråarbete. Money tillför kvalificerade betal- och korttjänster. Capital access tillför frivillig finansieringsresa. Dessa namn och gränser är hypoteser, inte fastställd prissättning.

Self-hostad redovisningskärna och agentåtkomst ska respektera repo:ts nuvarande licens- och produktprinciper. Hosting, support och kvalificerade managed services kan ha tydligt värde utan att grundläggande bokföring görs till gisslan. [R01, R03]

### 33.2 Intäkter som ska hållas isär

| Intäktstyp | Redovisat och operativt mått | Inte samma sak som |
|---|---|---|
| SaaS | Intäkt enligt levererad tjänst och kvalificerad periodisering. | Fakturerat totalbelopp eller kassa inklusive skatt. |
| Integrations-/användningsavgift | Faktiskt avgiftsgrundande användning enligt avtal. | Alla försök, retries eller webhookleveranser. |
| Betal- och kortersättning | Nettorätt till avtalad avgift/provision med korrekt principal/agent-bedömning. | Hela kundens betalnings- eller kortvolym. |
| Finansieringsförmedling | Avtalad provision när intjäningsvillkor är uppfyllda. | Utbetalat lånekapital. |
| Egen finansiering | Kvalificerad ränta och avgiftsintäkt med finansierings- och förlustkostnader separat. | Bruttoränta som garanterad marginal. |
| Redovisningstjänst | Avtalad tjänsteleverans och ansvar. | Att kunden själv använder ett verktyg. |

### 33.3 Bidragsekonomi

Det grundläggande produktmåttet bör vara nettobidrag per aktivt bolag och produktkohort:

```text
Nettobidrag
= kvalificerad SaaS- och tjänsteintäkt
+ intjänad nettodel av partneravgifter
− moln och modellkostnad
− provider- och datakostnader
− hänförlig support och granskningskostnad
− faktiska avtalade fraud-/garanti-/återköpskostnader
− funding cost och kreditförlust där Drastic faktiskt bär dem
```

Denna formel är ett operativt mått, inte en komplett redovisningsstandard. Beloppen behöver periodiseras och principal/agent-bedömas korrekt. Kapitalbindning, kreditförlust och partnersäkerheter får inte gömmas genom att bara rapportera en hög bruttotransaktionsvolym.

Vid prövning av finansiering ska teamet dokumentera kundfördel, realiserad provision, stödärenden, avslag, datakompletteringar och eventuell riskexponering. En produkt som ger hög provision men hög support och negativ kundlikviditet är inte automatiskt attraktiv.

### 33.4 Första kapitalet

Första finansieringen ska finansiera verifierad bokföringsprodukt, användarresor, distribution, specialistgranskning och säkra partnerintegrationer. Den ska inte användas som oplanerad reserv för ett växande lånebestånd.

En finansieringsplan ska redovisa två helt separata behov: **rörelsekapital för teknikbolaget** och **eventuellt framtida kapital/funding för finansiella exponeringar**. Ett investeraråtagande till SaaS-bolaget är inte samma sak som en långivare som åtagit sig att finansiera kundlån.

Kapitalanskaffningens bevis bör vara: en verkligt granskad kundperiod, kortare arbete på samma underlag, externa kunder som kan onboardas, hållbar kostnad per kund och konkreta partnerunderlag. Modellpoäng utan kreditutfall, ett stort antal kodrader eller en oklassificerad FI-badge ersätter inte dessa bevis.

### 33.5 Distribution

Börja med bolag vars ekonomiska profil överlappar Book Zero. Redovisningspartners kan ge granskning och distribution om produkten faktiskt minskar deras arbete. Connected Cash och Revenue kan vara en mindre förändring för kunden än ett fullständigt huvudboksbyte.

Distribution ska testas med observerad aktivering, betalningsvilja och supportåtgång. Ingen specifik prisnivå, konverteringsgrad eller förväntad marknadsandel antas i denna PRD. Sådana hypoteser ska registreras, prövas och revideras utan att påverka bokföringens kvalitetsgränser.


<a id="chapter-34"></a>

## 34. Leveransnivåer och releasebeslut

### 34.1 En målbild, flera kvalificerade leveranser

End-state ska vara komplett på papper men byggas genom sammanhängande fungerande resor. Ett steg är inte en tidsestimering och det ska inte översättas till att alla funktioner i hela plattformen måste vara färdiga innan någon kund får nytta.

| Nivå | Produktutfall | Obligatoriskt bevis | Vad nivån inte ger rätt att påstå |
|---|---|---|---|
| ES-0: ägarskap och scope | Gemensam målbild mappad till verkligt repo och Book Zero. | Revisionspinning, kravägare, faktiska öppna frågor och valda bolagsprofiler. | Ingen funktionsberedskap genom dokumentation ensam. |
| ES-1: verifierad ekonomigrund | Book Zero, sammanhängande vardagsarbete och läsande Cash. | Oberoende granskad period, förklarbar prognos, export och relevant återhämtning. | Inga otestade bankbetalningar eller fullständiga årsprofiler. |
| ES-2: repeterbar produkt | Externa kunder, Revenue, AP, kvalificerad lön/skatt/Close och Connected-resa. | Flera riktiga onboardingar med mätt tid, korrekthet och supportkostnad. | Att en kundprofil innebär stöd för alla svenska företag. |
| ES-3: partner-Money | Betalningar, kort och kvalificerad treasuryväg. | Rollbeslut, partneravtal, extern utfallsåterhämtning, avstämning och bemannad incidentväg. | Att partnern övertagit alla skyldigheter eller risker. |
| ES-4: partner-Capital | Relevant finansieringsresa, punkt-i-tid-underlag och riktig servicing. | Behörig förmedlingsmodell, verkligt långivarbeslut, avtal, utbetalning och återbetalningskontroller. | Egen validerad kreditmodell eller egen kreditbok utan ytterligare bevis. |
| ES-5: mogen plattform | Integrerad multi-entity, policybar automation, robusta partners och god bidragsekonomi. | Stabil produktion inom valda profiler, återkommande kontroller, exitövningar och hållbar operationsfunktion. | Att alla jurisdiktioner eller finansiella produkter automatiskt stöds. |
| ES-6: valfritt eget risktagande | Egen kvalificerad betal-/kreditverksamhet där affärsfallet motiverar det. | Separat finansiering, tillstånd/registrering, specialistorganisation, riskstyrning och kontrollerade ekonomiska exponeringar. | Att bankstatus är ett mål i sig eller att ES-6 krävs för framgång. |

Mogen partnerbaserad ES-5 kan vara den optimala slutprodukten. ES-6 ska beslutas mot alternativet att fortsätta med bättre partneravtal. Egen reglerad drift får inte vara en prestigeinvestering som förstör mjukvarubolagets ekonomi.

### 34.2 Parallellisering som är tillåten

Efter ägarskapskartläggning kan rena räknare, UX, kontrakt och syntetiska providerflöden utvecklas parallellt. Faktiska bolagsuppgifter behövs för bolagsverifiering men ska inte stoppa oberoende produktarbete. En saknad bankpartner blockerar skarpa betalningar, inte att AP, mottagargranskning och Cash byggs färdigt.

Den tekniska integrationsordningen ska fortfarande följa verkliga beroenden: beviskedja och ekonomisk identitet före att fler exekverare får skriva, kvalificerad betalningsavsikt före automatisk providerfailover och servicingkontrakt före löften om aktiv finansiering.

### 34.3 Releasegrindar

Varje aktiverad produktprofil ska ha fem separata bedömningar:

1. **Implementerad:** nödvändiga operationer och kundresor finns.
2. **Verifierad:** rätt körningar har observerats vid namngiven revision.
3. **Tillämplig:** bolagsfakta, regler och format är kvalificerade.
4. **Operativ:** återhämtning, bemanning, avstämning och incidentväg fungerar.
5. **Extern:** relevant bank, myndighet eller partner har gett ett verkligt kvalificerat utfall.

En manuell expertövergång kan vara en giltig lösning för en sällsynt kvalificerad profil, men den ska vara en verkligt fungerande tjänst med ansvar och tidsram. Ett otestat TODO som sägs kunna lösas av en konsult räknas inte som levererat.

### 34.4 Exakta utvecklingspaket

Varje paket ska ange krav-ID, befintlig domänägare, förändrade konsumenter, kontraktsdelta, finansiella invariants, migrationsbehov, UX-slutpunkt och bevis. Åtgärda redan ägda NEXT-/PRY-/P-krav där de hör hemma.

Denna PRD är en dokumentleverans. Den ger inte i sig tillstånd till produktionsskrivningar, nya testfiler i repo, provideranrop, commits eller publicering. Repo:ts explicita regler för teständringar och aktuellt genomförandeuppdrag ska följas. [R02]

### 34.5 Arbetsfördelning i en liten organisation

Grundaren kan initialt äga produkt och teknisk implementation. Redovisningskvalificering behöver en verklig redovisningskunnig granskare. Money behöver namngiven betal-/säkerhetskompetens och incidentansvar. Capital behöver faktisk kreditkompetens, compliance och servicingkapacitet enligt den valda modellen.

En funktion kan köpas externt eller delas med partner där det är tillåtet, men rollen måste ha mandat, kapacitet och oberoende när så krävs. AI kan minska arbetsvolymen. AI kan inte göra en saknad ansvarig person till en bemannad funktion.

<a id="chapter-35"></a>

## 35. Kvalitetsmål, kapacitetsbudget och mätning

### 35.1 Föreslagna tekniska serviceklasser

Nedanstående är produktmål för kvalificering, inte observerade resultat eller redan erbjudna SLAer. Innan de säljs ska faktisk driftmodell, last och partnerberoenden mätas.

| Klass | Föreslaget mål | Mätgräns och villkor |
|---|---|---|
| Normal ekonomiläsning | p95 under 2 sekunder för vanlig paginerad vy. | Definierad datamängd och varm tjänst, exklusive användarens nät och extern långsam källa. |
| Förbereda normalt bokföringsförslag | p95 under 5 sekunder efter tillgängligt kvalificerat underlag. | Dokumentextraktion kan vara separat asynkront steg med egen status. |
| Acceptera ett ekonomiskt kommando | Snabb beständig mottagning och återfinnbar identitet. | Ingen falsk löfte om omedelbar extern avveckling. |
| Cash 13 veckor | Normal kundprofil får resultat inom 30 sekunder eller ett beständigt asynkront jobb. | Ingen lång DB-transaktion eller blockering av huvudboksarbete. |
| Managed Core tillgänglighet | Målsatt 99,9 procent per månad efter kvalificerad produktion. | Stödda läs- och arbetsoperationer, tydligt definierad mätning. |
| Skarp Money-kommandogräns | Målsatt 99,95 procent för intern upptagning/status efter uppgraderad drift. | Partneravveckling mäts separat och kan ha annan tillgänglighet. |
| Incidentupptäckt | Materiala finansiella invariants ska larma automatiskt. | Alarmets mottagare och responstid måste ha faktisk bemanning. |
| Återställning Core | Initialt kvalificeringsmål RTO 4 timmar och RPO högst 15 minuter för vanlig appdata. | Ett affärsförslag, inte ett bevisat återställningslöfte. |
| Finansiella externa sidoeffekter | Ingen godkänd handling får bli okontrollerat dubblerad efter restore. | Bekräftade handlingar måste återfinnas eller utredas med extern referens före ny skrivning. |

Ett generellt påstående om RPO noll över alla katastrofer ska inte användas utan en faktiskt verifierad lagrings- och failovermodell. För extern betalningsdrift krävs att avsiktens beständighet och leverantörens återidentifiering tillsammans säkrar återhämtning. Kan detta inte bevisas ska profilen inte aktiveras för automatisk sidoeffekt.

### 35.2 Kapacitetsprofil för kvalificering

Definiera minst en mindre kundprofil, en större transaktionsprofil och en byråprofil. Mät import, dagligt arbete, rapporter och prognos med verklig datadistribution. Som första föreslagen testbudget kan en profil omfatta 100 000 verifikationsrader, 10 000 öppna eller historiska fakturaobjekt och 13 veckors betalningshändelser. Detta är en föreslagen dimensionering, inte ett påstående om uppnådd prestanda.

Varje jobb ska ha gräns för rader, objektstorlek, beräkningstid och kostnad samt kunna fortsätta från checkpoint. Rättvis schemaläggning ska skydda små kundjobb från en stor import. Ingen kapacitetsoptimering får byta exakt pengar mot flyttal eller skippa oberoende kontrollsummor.

### 35.3 Kundvärde och kvalitet

| Område | Primärt mått | Skyddsmått |
|---|---|---|
| Onboarding | Tid och manuellt arbete till första kvalificerade period eller Cash-basis. | Andel senare upptäckta källluckor och felaktiga ingående värden. |
| Accounting | Aktiv mänsklig tid per komplett granskad period. | Felbehandling, rättelser, oidentifierade poster och extern granskaracceptans. |
| Workflow | Andel ärenden avslutade utan utvecklarhjälp. | Oklara statusar, återöppnade felaktigt stängda ärenden och stödbehov. |
| Cash | Belopps- och tidsfel jämfört med sparad prognos. | Missade faktiska underskott, täckning och övertro i ofullständig data. |
| Billing | Rätt debitering per avtalsförekomst. | Dubbeldebitering, felaktig proration och krediter på grund av systemfel. |
| Payments | Andel kvalificerat avstämda uppdrag och tid i unknown. | Dubbla betalningar, fel mottagare, oförklarade avräkningar och förlust. |
| Cards | Tid från köp till komplett kostnadsunderlag. | Dubbla kostnader, borttappade refunds och oavstämda holds. |
| Collections | Verkligt återvunnet nettobelopp och tid till korrekt lösning. | Felaktiga krav, kundklagomål, tviståteröppning och otillåtna avgifter. |
| Financing | Kundens finansierade behov och hållbar återbetalningsprofil. | Missförstådda villkor, återköpsrisk, klagomål och ekonomiskt nettobidrag. |
| Risk | Kvalificerad kalibrering och beslutskvalitet där data räcker. | Databrist, temporal läckage, diskriminerande effekt och felaktig automatisering. |
| Platform | Nettobidrag per kund och verifierad bibehållen användning. | Supportbelastning, partnerkoncentration och compliancekostnad. |

En hög andel agentförberedda förslag är ett sekundärt mått. Den ska endast räknas som förbättring om den slutliga periodens kvalitet och arbetsinsats också förbättras.

### 35.4 Mätning utan dataläckage

Produkttelemetri ska använda pseudonymiserade resursreferenser och händelsetyper. Fullständiga fakturor, bankuppgifter, personnummer och löner ska inte kopieras in i analysverktyg. Ekonomiska kvalitetsmätningar behöver en avgränsad kontrollmiljö med rätt ändamål.

A/B-test ska inte randomisera juridiska skyldigheter, bokföringsriktighet, kritiska säkerhetskontroller eller avtalsvillkor utan kvalificerat separat upplägg. UI-test får inte göra det svårare att säga nej till finansiering eller att förstå en avgift.

<a id="chapter-36"></a>

## 36. Numeriska referensfall

Fallen är oberoende syntetiska räkneexempel för PRD:ns interna precision. De utgör inte skattebedömning, verifiering av openERP eller produktionsbevis. Tillämplig redovisnings- och avtalsprofil väljer slutlig bokföring.

### N-01: Billing med usage och kredit

Antag grundavgift 10 000, 300 enheter à 20 och en uttryckligt syntetisk skatt på 25 procent. Netto är 16 000, skatt 4 000 och brutto 20 000. En kredit på 1 000 netto och 250 skatt lämnar 18 750. Dubblerad usage-händelse ändrar ingen summa. Ett betalningsretry ändrar inte debiteringen.

### N-02: Kortreservation och refund

Reservation 1 000. Delvis återföring 300. Slutlig avräkning 650. Återstående reservation som ska frigöras är 50. Därefter refund 200. Totalt faktiskt köp efter refund är 450. Reservationen är inte en extra kostnad utöver avräkningen.

### N-03: Betalningsförmedlarens netto

Bruttoförsäljning 1 000, avgift 30, refund 100 och ny reserverad del 200 ger utbetalning 670. Bevarad avräkningsförklaring: 670 bank + 30 avgift + 100 refund + 200 reserv = 1 000. Reserven kan vara en separat fordran eller annan kvalificerad position, inte nya fritt tillgängliga bankpengar.

### N-04: Fakturabelåning

Kundfordran 100 000. Lånekapital 80 000 med avtalad innehållen avgift 2 000 ger initialt 78 000 till säljaren. Om slutkunden betalar 100 000 till långivarens kvalificerade mottagarkonto och 80 000 reglerar lånekapitalet blir restlikvid 20 000 enligt detta förenklade avtal. Säljarens totala kontantlikvid är 98 000. Fordrings- och lånebokföring följer sin egen profil. Det är inte två försäljningar eller 178 000 i säljarinbetalning.

### N-05: Kvalificerat fakturaköp

En alternativ juridiskt kvalificerad köpprodukt har köpeskilling 98 000 för en fordran på 100 000, med initial likvid 78 000 och avtalsbunden rest 20 000. Likviditeten kan se likadan ut som N-04 men rättighets- och redovisningsmodellen kan skilja sig. Detta exempel bestämmer inte om bortbokning är tillåten.

### N-06: Lån och amortering

Antag 100 000 kapital, fast årsränta 10 procent, ACT/365 för exakt tio dagar och avrundning av periodräntan till två decimaler. Ränta blir 273,97. Betalning 20 000 allokeras enligt antagandet först till denna ränta och därefter kapital: kapitalminskning 19 726,03 och återstående kapital 80 273,97. Eventuell uppläggningsavgifts redovisning är separat. Detta är ett kontraktsexempel, inte en föreslagen kundränta.

### N-07: Delbetalning, kredit och bestridande

Ursprunglig fordran 10 000, betalning 4 000 och kredit 1 000 lämnar 5 000. Av detta är 2 000 bestritt. Obestritt belopp för kvalificerat automatiskt påminnelsearbete är 3 000. Redovisad rest är fortfarande 5 000 tills separat rättelse eller nedskrivningsbehandling beslutas.

### N-08: Skattekontots kompletterande finansiering

Kvalificerat saldo 30 000 och framtida debiteringar 50 000 ger ytterligare överföringsbehov 20 000, förutsatt att inga andra medelsrörelser eller åtkomstbegränsningar finns i detta scenario. Bankprognosen drar inte både 50 000 och 20 000 för samma skyldigheter.

### N-09: Likviditetsrisk trots samma slutsaldo

Start 100 000 och buffert 10 000. Utbetalning dag 5 är 70 000. Kund A betalar 60 000 dag 8. Utbetalning dag 15 är 30 000. Annan kund betalar 30 000 dag 28. Slutsaldo är 90 000, lägsta saldo 30 000 och utrymme 20 000. Om Kund A i stället betalar dag 22 är slutsaldot fortfarande 90 000 men lägsta saldo är 0 och utrymmet är −10 000.

### N-10: Samtidig limit

Kvarvarande godkänd kapacitet är 100 000. Två samtidiga avsikter om 60 000 får inte båda reserveras. Efter första lyckade reservationen återstår 40 000. Vilket uppdrag som vinner är ett samtidighetsutfall, men totalsumman får aldrig överstiga tillåten kapacitet.

### N-11: Proportionell öresrest

Ett totalbelopp på 100 minor units fördelat lika över tre kvalificerade komponenter ska ge en dokumenterad fördelning, exempelvis 34, 33 och 33 under en bestämd tie-breakregel. Summan är alltid 100. Regelns ordning ska vara stabil och inte bero på slumpmässig databasordning.

<a id="chapter-37"></a>

## 37. Riskregister och medvetna avvägningar

| Risk | Tidig signal | Produkt- eller organisationsåtgärd | Kvarstående osäkerhet |
|---|---|---|---|
| Bredd före färdig kundresa | Många moduler men ingen komplett period. | ES-1 och befintliga Book Zero-grindar prioriteras. | Hur mycket bredd första kundprofilen faktiskt kräver. |
| Förväxlad ekonomisk auktoritet | Samma saldo beräknas i flera domäner. | Namngivna ägare och avstämning mellan perspektiv. | Externa system kan ha ofullständiga identiteter. |
| Partnerberoende | Samma leverantör krävs för alla läsningar och handlingar. | Bevarad lokal historik, kvalificerad exit och separat observation. | Vissa avtal och rails är inte portabla. |
| Oväntat reglerad verksamhet | Ny produkt flyttar pengar eller delar riskbedömning. | Rollanalys innan aktivering. | Slutlig bedömning beror på faktiska avtal och utförande. |
| Falsk precision i Cash | Grön siffra trots saknade löner eller bankdata. | Täckning per horisont och villkorade resultat. | Framtida affärshändelser är alltid osäkra. |
| Övertro på kreditmodell | PD visas trots liten observerad population. | Transparent reglering och verklig partnerbedömning före egen modell. | Kreditutfall tar tid att observera. |
| Dubbla externa sidoeffekter | Timeout följs av nytt providerkommando. | Unknown-spärr, stabil identitet och avstämning. | Leverantörer utan tillräcklig återidentifiering begränsar automation. |
| Mottagarbedrägeri | Kontoändring godkänns i samma e-postkedja. | Separat granskad mottagarrevision och oberoende kontroll. | Social engineering kan inte elimineras helt. |
| Negativ finansieringsmarginal | Hög volym men ökande garantikrav och stöd. | Nettobidrag efter alla risk- och kapitalposter. | Partnerpriser och förluster varierar över tid. |
| Felaktig datamonetisering | Kunddata antas fri att återanvända. | Ändamålsstyrd behandling och separat riskprodukt. | Tillämplig rätt beror på data och mottagare. |
| Licensmissförstånd | Separat API antas tillåta sluten kärna. | Rättighetsinventering och repo:ts licenspolicy. | Slutlig kombinationsbedömning är juridisk. |
| Personberoende | En grundare kan ensam ändra policy och flytta pengar. | Separata kritiska mandat och verkliga reservfunktioner. | Liten organisation behöver köpa viss kompetens. |
| Legalt läckande kundförklaring | AML-träff eller persondata syns i vanlig dashboard. | Fältnivåbehörighet och tillåten förklaringsmodell. | Exakt disclosure följer ärendets rättsliga ram. |
| Felaktig koncernlikviditet | Alla bolags pengar summeras som fria. | Juridisk scope och intercompanyvillkor. | Avtalade restriktioner måste hållas aktuella. |

De centrala avvägningarna är att välja kvalificerad produktnytta framför maximal automation, faktiska partnergarantier framför abstrakt portabilitet och förklarbar begränsning framför en övertygande men osäker siffra.

<a id="chapter-38"></a>

## 38. Öppna beslut och nödvändiga externa underlag

| Beslut | Ansvarig roll | Behövs före | Oberoende arbete som kan fortsätta |
|---|---|---|---|
| Första externa kundprofil och transaktionstyper. | Produktägare + redovisningsgranskare. | Marknadsförd bredd och skarp onboarding. | Book Zero, generiska kontrakt och källinventering. |
| Driftad Native, Connected eller båda i första kommersiella erbjudandet. | Produktägare. | Första prissatta paketet. | Gemensamma domän- och UX-ägare. |
| Faktisk tjänsteroll för automatiserad bokföringsleverans. | Juridik/compliance + produktägare. | Managed accounting som tjänst. | Ren programvara och avgränsade verifieringsresor. |
| Bankdata- och betalningspartner med rätt kvalificerad roll. | Integrationsansvarig + juridik. | Skarpa anslutningar och pengarörelser. | Filbaserad import, Payments-kontrakt och syntetisk återhämtning. |
| Kortprogram, ansvar och finansieringsmodell. | Money-ägare + utgivare. | Kortutgivning. | Kortlivscykel, kostnadsflöde och avstämningsspecifikation. |
| Finansieringspartner, provision, regress och kapitalägare. | Capital-ägare + juridik. | Förmedling och bindande erbjudande. | Behovsanalys, datarum och läsande scenarier. |
| Fakturaköp eller belåning samt redovisningsprofil. | Kredit/juridik/redovisning. | Första fakturafinansierade affären. | Gemensam identitet, kapacitet och syntetiska avräkningar. |
| Riskmodellens population och tillåtna källor. | Riskägare + dataskydd. | Kalibrerad scoring eller externa riskprodukter. | Datakvalitet, proveniens och manuell beslutsresa. |
| AI-systemens klassificering och aktuell rättsversion. | Juridik + AI-ansvarig. | Relevant skarp användning. | Säker tool-policy och deterministisk numerik. |
| Dataplacering, nycklar, retention och underleverantörer. | Säkerhet + dataskydd. | Riktiga kundoriginal och bred produktion. | Portabel lokal drift och återställningsdesign. |
| Bemanning, jour och klagomålsansvar. | Operativt ansvarig. | Skarpa Money- och Capital-åtaganden. | Produktutveckling, kontrakt och externa specialistavtal. |
| Exakt serviceklass, kapacitet och återställningsmål. | Teknik + operations. | Kundlöfte eller SLA. | Belastningsprofilering och isolerade övningar. |
| Äganderätt och licensbehandling av framtida moduler. | Maintainer + rättighetsgranskare. | Distribution/kommersiell release av kombinerad produkt. | Arkitektur inom den befintliga licensen. |
| Egen balansräkning eller fortsatt partnerdrift. | Styrelse + finansiering + risk/compliance. | ES-6. | Hela partnerbaserade målbilden ES-1–ES-5. |

Ingen okänd bolagsuppgift, produktsats eller partnergaranti får ersättas med ett plausibelt värde. Samtidigt ska en extern lucka bara blockera sitt verkliga beroende, inte användas som skäl att skjuta upp all övrig produktutveckling.


<a id="chapter-39"></a>

## 39. Acceptansplan och bevispaket

### 39.1 Två lager av acceptans

Varje `DR-*`-krav har ett eget konkret acceptansvillkor. Dessutom innehåller paketet **100 tvärgående acceptansfall** i `ACCEPTANCE.md` och `acceptance.json`. Fallen beskriver förutsättningar, handling, förväntat resultat, berörda krav och typ av bevismiljö. Alla är specificerade, inte exekverade.

Ett finansiellt krav är inte verifierat bara för att statisk typkontroll eller en skärmbild passerar. Rätt bevis kan kräva exakt kalkyl, riktig databastransaktion, vanlig browserresa, behörighetsvägran, oberoende redovisningsgranskning och verklig provideracceptans. Vilka delar som behövs beror på påståendet.

### 39.2 Oberoende kontroll

Förväntade belopp ska definieras före implementation och beräknas oberoende av produktionsräknaren. En kopia av samma algoritm i en annan fil är inte automatiskt ett oberoende facit. Kvalificerade finansiella exempel ska ange regelversion, avtalsantaganden, indata och avrundning.

Syntetiska fall är viktiga för samtidighet, återförsök och svåråtkomliga fel. De ersätter inte Book Zeros verkliga period eller en produkts riktiga myndighets- eller bankgräns. Riktiga kunduppgifter får inte publiceras i repo eller generella loggar som testdata.

### 39.3 Krav på varje verifieringspost

En faktisk verifieringspost ska ange krav, scenario, kodrevision, miljö, migrationer, tillåtelse, inputhash, förväntat resultat, observerat resultat, externa referenser där relevanta, fel samt kvarstående begränsningar. Status ska skilja specificerad, implementerad, lokalt verifierad, bolagsverifierad och externt kvalificerad.

När ett fel rättas ska den tidigare observationen ligga kvar. Ett nytt godkänt resultat ska peka på den revision som faktiskt kördes. Tidigare bevis får återanvändas endast där oförändrade relevanta beroenden gör det giltigt.

### 39.4 Färdig end-state

Partnerbaserad end-state är uppnådd när valda kundprofiler kan onboardas, arbeta, få betalt, betala, använda kvalificerade kort, planera likviditet, avsluta perioder och hantera relevant partnerfinansiering genom sammanhängande resor med hållbar driftsekonomi.

Samtliga aktiverade produkter ska ha rätt ägare, faktisk ansvarsfördelning, acceptansbevis, fungerande avvikelsehantering och kundexit. Inga dolda manuella utvecklarsteg, okvalificerade finansiella löften eller saknade operationsroller får vara nödvändiga för normal drift.

Egen balansräkning är en separat möjlig utvidgning. Den optimala produkten är inte den som gör mest själv utan den som kan leverera de utlovade ekonomiska resultaten och hantera hela livscykeln på ett kontrollerat sätt.


<a id="chapter-40"></a>

## 40. Källor, avgränsningar och dokumentstatus

Källorna nedan användes för avgränsade externa sakuppgifter och repoanknytning. Övriga produktkrav, föreslagna mål, kundresor och kontrakt är utformade för denna PRD. De är inte påståenden om att en leverantör eller myndighet godkänt Drastic. Källkontroll avser 27 september 2026. Ingen heltäckande juridisk granskning, fullständig kodgranskning eller faktisk bolagsverifiering utfördes i denna dokumentleverans.

Den ursprungliga Book Zero-filen ligger kvar byteidentisk. Där den innehåller bolagsspecifika eller historiska uppgifter behåller den sin egen namngivna provomfattning. Den nya PRD:n gör inte dessa uppgifter till generella kundfakta.

### [B00] Föregående PRD: Book Zero, Workflow och Drastic Cash

Oförändrad första verifieringsomfattning och kravkontinuitet. Inte en ny runtimegranskning.

Fil: `PRD_openERP_Book_Zero_Workflow_Drastic_Cash_v1.md`
SHA-256: `6dee5e41e75373722a443f23b2aa6f3b3329dcad862b3c6284a07ac1aa263afd`

### [R01] openERP README vid granskad revision

Beskriven utvecklingsfunktionalitet, teknisk grund och uttryckliga begränsningar i produktions-/myndighetsvalidering.

Källa: `https://github.com/erik-kroon/openERP/blob/09fdb19837bb1535b1b4c060e68a0b237858b0a5/README.md`

### [R02] openERP AGENTS.md vid granskad revision

Applikationsägarskap, Effect/Drizzle, transaktionsgränser, UI-regler och separat auktorisation för teständringar.

Källa: `https://github.com/erik-kroon/openERP/blob/09fdb19837bb1535b1b4c060e68a0b237858b0a5/AGENTS.md`

### [R03] openERP LICENSING.md vid granskad revision

Projektets AGPL-3.0-only-policy, källutgåva vid hosted drift och avgränsning mot kunddata.

Källa: `https://github.com/erik-kroon/openERP/blob/09fdb19837bb1535b1b4c060e68a0b237858b0a5/LICENSING.md`

### [E01] Finansinspektionen: Viss finansiell verksamhet

Registrering för bland annat yrkesmässigt lämnande och förmedling av företagskredit samt factoring/leasing. Inte universellt finansiellt tillstånd.

Källa: `https://www.fi.se/sv/betalningar/sok-tillstand/viss-finansiell-verksamhet/`

### [E02] Finansinspektionen: Betaltjänster

Betaltjänsttillstånd, kontoinformationsregistrering och kvalificerad ombudsmodell.

Källa: `https://www.fi.se/sv/betalningar/sok-tillstand/betaltjanster/`

### [E03] Finansinspektionen: Elektroniska pengar

Separat ram för e-pengautgivning och varför faktisk värdebärande wallet behöver prövas.

Källa: `https://www.fi.se/sv/betalningar/sok-tillstand/elektroniska-pengar/`

### [E04] Finansinspektionen: Inkasso

Tillståndsram för indrivning åt andra eller vissa övertagna fordringar samt särskilda undantag som måste bedömas.

Källa: `https://www.fi.se/sv/bank/sok-tillstand/inkasso/`

### [E05] IMY: Ansöka om kreditupplysningstillstånd

Separat tillståndsbedömning för kreditupplysningsverksamhet och framtida extern Risk-produkt.

Källa: `https://www.imy.se/verksamhet/utfora-arenden/ansoka-om-kreditupplysningstillstand/`

### [E06] IMY: Automatiserade beslut

Individers rättigheter vid helt automatiserade betydande beslut, med tillämpliga undantag och skydd.

Källa: `https://www.imy.se/privatperson/dataskydd/dina-rattigheter/automatiserade-beslut/`

### [E07] EUR-Lex: AI Act, konsolidering 27 juli 2026

Versionsbunden AI-klassificering, kreditvärdighetsbedömning av fysiska personer och krav att kontrollera aktuella övergångsbestämmelser. Konsoliderad text är dokumentationshjälp; officiella rättsakter och faktisk tillämplighet styr.

Källa: `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02024R1689-20260727`

### [E08] Finansinspektionen: Om Dora

Finansiell IKT-risk, motståndskraft och skillnaden mellan reglerad aktör och extern tjänsteleverantör.

Källa: `https://www.fi.se/sv/betalningar/it-risker-dora/om-dora/`

### [E09] Finansinspektionen: Penningtvätt och finansiering av terrorism

Behovet av kvalificerat ansvar och process för penningtvättsrisk inom berörd verksamhet.

Källa: `https://www.fi.se/sv/betalningar/penningtvatt2/`

### [E10] Länsstyrelsen Stockholm: Redovisningskonsulter och skatterådgivare uppmärksammas på signaler om penningtvätt

Redovisnings- och skatterådgivningstjänster behöver skiljas från ren programvara vid AML-rollbedömning.

Källa: `https://www.lansstyrelsen.se/stockholm/om-oss/om-lansstyrelsen-stockholm/nyheter/nyheter---stockholm/2025-03-24-redovisningskonsulter-och-skatteradgivare-uppmarksammas-pa-signaler-om-penningtvatt.html`

### [E11] PCI Security Standards Council: PCI DSS

Kortsäkerhet och behov av kvalificerad kortdatamiljö. Inget påstående om PCI-certifiering av Drastic.

Källa: `https://www.pcisecuritystandards.org/standards/pci-dss/`

### [E12] Skatteverket: Skattekonto, betala och få tillbaka

Inbetalning till skattekonto kan inte öronmärkas som en viss enskild skatt eller avgift.

Källa: `https://www.skatteverket.se/foretag/skatterochavdrag/skattekontobetalaochfatillbaka.4.6a6688231259309ff1f800029122.html`

### [E13] Bokföringsnämnden: Arkivering

Generell sjuårsregel efter kalenderåret för räkenskapsårets slut samt behov att kvalificera förvaring och läsbarhet.

Källa: `https://www.bfn.se/fragor-och-svar/arkivering/`

### [E14] Bolagsverket: Digital inlämning av årsredovisning

Extern digital årsredovisningskanal som behöver kvalificeras med aktuella format, roller och kvitton.

Källa: `https://bolagsverket.se/omoss/utvecklingavdigitalatjanster/digitalinlamningavarsredovisning.2255.html`

### [E15] Upphandlingsmyndigheten: Regler för e-handel och e-faktura

Kvalificerad offentlig e-fakturering och strukturerade format. Inte ett generellt krav på alla svenska B2B-fakturor.

Källa: `https://www.upphandlingsmyndigheten.se/digitalisering-och-e-handel/e-handel/regler-for-e-handel-och-e-faktura/`

### [E17] IMY: Dataskyddsförordningen i fulltext

Rättslig grund, ändamål, uppgiftsminimering och relevanta rättigheter behöver bedömas för faktisk behandling.

Källa: `https://www.imy.se/verksamhet/dataskydd/det-har-galler-enligt-gdpr/introduktion-till-gdpr/dataskyddsforordningen-i-fulltext/`

### Vad som faktiskt har kontrollerats i paketet

Dokumentgeneratorn kontrollerar unika krav-ID:n, referenser från acceptansfallen, källhänvisningar, bevarande av föregående fil och de syntetiska aritmetiska exemplen. Resultatet ligger i `document_validation.json`. Detta är dokumentkontroll. Det är inte verifiering av applikationen, något bank-API, myndighetsinlämning, kreditmodell eller verklig ekonomisk bokföring.

**Nästa genomförande ska börja med aktuell repo- och ägarkartläggning samt Book Zeros verkliga period. Denna målbild styr vart varje vidare leverans ska leda utan att skapa en konkurrerande huvudbok, betalningsmotor eller kravbacklog.**
