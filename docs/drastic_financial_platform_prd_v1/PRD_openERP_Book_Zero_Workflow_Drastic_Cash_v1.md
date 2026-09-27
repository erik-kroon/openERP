# PRD: openERP för Drastic AB
## Book Zero, dagligt bokföringsarbete och Drastic Cash

| Dokumentfält | Värde |
|---|---|
| Version | 1.0 |
| Datum | 2026-09-27 |
| Status | Produktkrav och föreslagen leveransordning. Inte en implementations- eller driftsättningsrapport. |
| Produktägare | Drastic |
| Primär användare | Ägare/operatör i ett mindre svenskt aktiebolag |
| Första verifieringsbolag | Drastic AB |
| Repository | `erik-kroon/openERP` |
| Inspekterad GitHub-revision | `41410fd75e96361b7c2f407d456019500f39bfbe` |
| Föreslagen placering i repo:t | `docs/product/book-zero-workflow-cash-prd.md` |

**Produktlöfte:** Företagaren ser vad som återstår, godkänner förberedda bokföringsförslag och förstår hur kommande betalningar påverkar likviditeten. Varje relevant belopp går att förklara tillbaka till underlaget.

**Leveransens huvudresultat:** Drastic AB kan behandla verkliga underlag i openERP, få en oberoende granskad period och lämna ett användbart bokslutsunderlag. Samma data driver ett dagligt arbetsflöde och en spårbar betalningsprognos.

**Inte målet:** maximal funktionsparitet med ett generellt ERP, en ny arkitektur eller ett finansbolag.

---

## 1. Beslut och prioritering

Den här PRD:n omfattar en produkt i tre delar:

1. **Book Zero:** bevisa bokföringen för Drastic med verkliga underlag och oberoende kontroller.
2. **Arbetsflödet:** göra det möjligt att slutföra normalt ekonomiarbete genom produktens vanliga gränssnitt.
3. **Drastic Cash:** beräkna och förklara likviditet från observerade saldon, återstående betalningar och uttryckliga antaganden.

Book Zero och arbetsflödet ska utvecklas som sammanhängande kundresor. Cashs kontrakt och beräkningsfall kan utvecklas parallellt. Att Cash kan rita en prognos innebär inte att underlaget är fullständigt för ett verkligt bolag.

Prioriteringsregel: ett arbete får ingå när det krävs för Drastics faktiska bokföring, för att slutföra en prioriterad kundresa eller för att förklara Cashs saldon och betalningar korrekt. Generell plattformsutbyggnad kräver ett separat produktbeslut.

Kravord:

- **SKA:** obligatoriskt inom den angivna leveransen.
- **VILLKORAT SKA:** obligatoriskt när bolagets dokumenterade förhållanden gör området tillämpligt.
- **SENARE:** inte en blockerare för denna leverans och inte något som produkten får påstå är färdigt.

Krav-ID:n i dokumentet är spårbarhets-ID:n. De ersätter inte repo:ts befintliga paket, milstolpar eller färdigställanderäkning.

## 2. Problem och användarvärde

Problemet är inte att företagaren saknar ytterligare ett register. Problemet är att underlag, beslut, bokföring och betalningsläge måste sättas samman manuellt för att besvara:

> Vad behöver jag göra nu? Är perioden korrekt? Hur mycket likviditetsmarginal har bolaget de närmaste månaderna?

Produkten ska minska manuellt arbete utan att dölja osäkerhet eller avskaffa granskningen. Användaren ska inte behöva förstå interna tillståndsmaskiner för att hitta nästa handling. En redovisningskunnig granskare ska däremot kunna inspektera de exakta besluten och deras konsekvenser.

Den kommersiella hypotesen är att kombinationen av mindre rutinadministration och bättre likviditetsöverblick är värdefull för andra små svenska AB med en liknande profil. Betalningsvilja och pris är ännu inte verifierade. Den här PRD:n låser därför ingen prislista och kräver inte abonnemangsinfrastruktur före Book Zero.

## 3. Nuläge, källor och vad som inte är verifierat

### 3.1 Inspekterad grund

GitHub `main` pekade vid kontrollen på revisionen ovan. Detta är en selektiv produkt- och källgranskning, inte en fullständig kodrevision eller en egen körning av applikationen. [R01]

| Område | Observerad grund | Konsekvens för PRD:n |
|---|---|---|
| Applikationsgräns | `AGENTS.md` lägger policy, behörighet och bokföringsoperationer i Effect-applikationen. PostgreSQL äger lagring, constraints och den smala integritetsgränsen. [R02] | Behåll den gränsen. Återinför inte feature-dispatch i SQL. |
| Företagsöversikt | `company-work.ts` sammanställer bankarbete, öppna kundfakturor och förberedande uppgifter. [R03] | Utöka befintliga läsningar och kompositioner. Bygg inte en andra startsida med konkurrerande totaler. |
| Kundresor | Frontendplanen skiljer existerande skärmar från verifierade, sammanhängande kundresor. Den begränsar också vad översikten får påstå om fullständighet och likviditet. [R04] | Acceptans ska ske genom verkliga användarresor, inte antal komponenter. |
| Bokföringskärna | Ett daterat implementationsunderlag redovisar lokala runtime-observationer för bland annat import, inköp, bokföring, återförsök och återställning. Bolags- och leverantörsgodkännande är separata frågor. [R05] | Återanvänd arbetet men reproducera relevant bevisning mot aktuell leverans. |
| Leveransplan | P2 gäller verkligt avstämd period, P4 moms/skatt, P5 tillämpligt djup, P6 årsarbete och P7 drift/övergång. [R06] | Den här PRD:n organiserar kundutfallet över befintliga ägare. Den stänger ingen gate genom dokumentation. |
| Bolagsfakta och externa indata | D-01 till D-10 skiljer identitet, bolagsprofil, import, regler och leverantörsbehörighet. [R07] | Saknade indata blockerar berörd faktisk användning, inte all oberoende utveckling. |
| Historiskt kassaflöde | NEXT-45 beskriver historisk kassaflödesklassificering och avstämning, uttryckligen inte prognos. [R08] | Cash ska inte duplicera eller döpa om det historiska rapportarbetet. |

Äldre statusstycken och senare implementationsunderlag kan avse olika tillstånd. Före varje implementationspaket ska ägaren jämföra aktuell kod, migrationer och relevant bevisning. Formuleringen ”finns i plan” är inte samma sak som ”saknas i kod”.

### 3.2 Drastics utgångspunkt

Tidigare lämnade bolagsuppgifter anger SEB, normalt räkenskapsår 1 maj till 30 april och första räkenskapsår **2025-05-17 till 2026-04-30**. Tidigare arbete omfattade även privata utlägg och ägaröverföringar. Detta används som utgångspunkt för onboarding och omfattning. De underliggande originalfilerna har inte återgranskats i arbetet med denna PRD.

Första historiska provet ska vara en avgränsad period inom detta år, vald utifrån tillgången till kompletta kontrollunderlag. Därefter utökas granskningen till hela första året för bokslutsöverlämningen. En likviditetsprognos för dagens bolag kräver ett separat, aktuellt observationsunderlag. Det historiska årsslutet är inte dagens banksaldo.

Momsmetod, momsperiod, redovisningsmetod, K2/K3-tillämplighet, eventuell lön och redan inlämnade deklarationer ska hämtas ur bolagets faktiska uppgifter. De får inte ersättas av antaganden baserade på exempel i denna PRD.

## 4. Användare och ansvar

| Roll | Huvuduppgift | Gräns |
|---|---|---|
| Företagare/operatör | Tillföra underlag, besvara frågor, granska och godkänna där rollen har rättighet. | Företagsåtkomst innebär inte automatiskt rätt att godkänna varje slags åtgärd. |
| Ekonomiarbetare | Bereda ärenden, avstämma och hantera avvikelser. | Tilldelning av en uppgift ger inte ny bokföringsbehörighet. |
| Redovisningsgranskare | Kontrollera behandlingar, avstämningar och granskningspaket. | Ett granskningsutlåtande ersätter inte extern inlämningsbekräftelse. |
| Agent | Läsa tillåtna uppgifter, föreslå behandlingar och förbereda avgränsat arbete. | Får inte ge sig själv godkännande eller utöka sina behörigheter. |
| Driftansvarig | Hantera installation, säkerhetskopior, återställning och teknisk övergång. | Teknisk administratör är inte automatiskt redovisningsgodkännare. |

Cash ska respektera bolags-, bok- och uppgiftsbehörighet. Löneuppgifter ska inte exponeras på individnivå för en användare som endast får se godkända aggregerade betalningsbehov.

## 5. Omfattning

### 5.1 Ingår

Import och bevarande av verkliga underlag, bankavstämning, kund- och leverantörsfakturor, privata utlägg, ägarflöden, godkänd bokföring, rättelser, momsunderlag, skattekonto, tillämpliga periodiseringar och bokslutsunderlag. Lön, tillgångar och valutaflöden ingår när Drastics faktiska transaktioner kräver dem.

Produkten ska även innehålla en sammanhängande arbetslista, en granskningsyta, periodkontroller, export till granskaren och en läsande Cash-funktion med sparade prognoser och scenarier.

### 5.2 Ingår inte i första leveransen

Egen utlåning, factoring, kreditbeslut, företagskort, finansiell marknadsplats, fri investeringsrådgivning, koncernkonsolidering och stöd för godtyckliga länder eller bolagsformer.

Cash initierar inga betalningar och skickar inga deklarationer. Direkta bank- och myndighetsanslutningar är inte förutsättningar för den första periodens filbaserade verifiering. En befintlig anslutning får användas först när dess verkliga behörighet och beteende är verifierat.

Fullständig egen produktion och inlämning av INK2, årsredovisning och iXBRL är inte automatiskt ett krav för den första avstämda perioden. Årsöverlämningen ska däremot täcka allt granskaren behöver inom vald ansvarsfördelning. Befintliga bredare P6/P7-krav kvarstår och får inte markeras klara av denna begränsning.

## 6. Book Zero: funktionella krav

### BZ-01: En uttrycklig och versionerad bolagsomfattning

Systemet SKA spara juridisk identitet, redovisningsvaluta, räkenskapsår, metodval, momsregistrering och perioder samt tillämpliga områden. Varje kvalificerande uppgift ska ha källa, uppgiftslämnare och relevant giltighetstid.

Bolagsprofilen ska också ange omfattade bankkonton, skattekonto, ägarflöden, tillgångar, eventuell lön och valutor. Ett område kan vara tillämpligt, inte tillämpligt med grund eller fortfarande okänt. Avsaknad av data betyder inte att området saknas i verksamheten.

**Acceptans:** En okänd momsmetod hindrar påståendet att momsunderlaget är klart. Den hindrar inte att bankfiler bevaras eller att ett annat oberoende ärende förbereds.

### BZ-02: Källinventering och bevarande

Varje import SKA behålla originalets bytes, hash, källa, importtillfälle och koppling till konto/period. Innehållsidentitet och importförekomst ska vara skilda begrepp. Samma fil kan förekomma flera gånger utan att händelserna bokförs flera gånger.

Inventeringen ska omfatta bankutdrag, befintlig bokföring, reskontror, kund- och leverantörsfakturor, kvitton, privata utlägg, ägaröverföringar, skattekontohistorik och eventuella tidigare deklarationer.

Redan utförda matchningar ska importeras med ursprung och granskningsstatus. De ska inte kastas bort eller behandlas som verifierade bara för att de finns i en tidigare sammanställning.

**Acceptans:** Återimport av samma bankfil ändrar inte verifikationsantalet. Två filer med överlappande perioder ger bevarade förekomster och identifierade överlapp, inte dubbla ekonomiska händelser.

### BZ-03: Källornas fullständighet

För varje källa SKA systemet visa omfattat intervall, kända luckor, senaste observation och oberoende kontrolltotaler. Bankkonton ska ha granskad start, slut och rörelser. Okända konton och dokumenterade periodluckor ska vara synliga i periodarbetet.

En nollskillnad i bankavstämningen är nödvändig men inte tillräcklig. Transaktioner som saknas på båda sidor eller felklassificerade rörelser kan fortfarande finnas.

**Acceptans:** En saknad bankmånad får inte ge ”period klar” även om de importerade raderna balanserar. En transaktion får inte ignoreras för att dölja en differens.

### BZ-04: Två separata historiska prov

Systemet SKA stödja skillnaden mellan:

- **Rekonstruktionsprov:** råunderlag och granskade ingångsvärden behandlas i en isolerad provbok. Resultatet jämförs med oberoende förväntningar.
- **Migrationsprov:** befintlig bokföring, ingående värden, öppna poster och länkar överförs utan att samma historiska affärshändelser bokförs en gång till.

Den gamla huvudboken får inte både generera hela resultatet och vara det enda facit som bevisar att nya bokföringsbedömningar är korrekta. Om tidigare bokföring är fel ska avvikelsen utredas, inte kopieras för att få lika totaler.

**Acceptans:** En kostnad i importerad historik och samma kostnads kvitto resulterar inte i två kostnader. Rekonstruktionsboken är märkt som prov och kan inte skicka fakturor eller deklarationer.

### BZ-05: Ingående värden och periodgränser

Ingående saldon, öppna fakturor, ägarskulder, skattepositioner och tillämpliga tillgångsregister SKA kunna spåras till granskade kontrollunderlag. Balansimport ska kompletteras med de öppna poster som krävs för kommande betalningsmatchning och Cash.

Importläget ska uttryckligen vara full historik eller granskad reducerad historik. Samma års ingående balans får inte kombineras med en redan inkluderad historik på ett sätt som fördubblar saldot.

**Acceptans:** En ingående kundfordran kan senare delbetalas utan att en ny intäkt uppstår enbart på grund av migrationen. Ett avgränsningsfel håller berört kontrollområde öppet.

### BZ-06: Från underlag till bokförd händelse

Normalflödet SKA vara: bevarat underlag, tolkade fakta, föreslagen behandling, validering, behörig granskning, godkännande, genomförande och beständigt kvitto.

Matchning och bokföring är separata handlingar. Förslaget ska ange vilka belopp, konton, datum och källor som påverkas. En allmän bokföringsoperation får inte kringgå den domän som äger exempelvis en faktura eller ett importerat historikblock.

**Acceptans:** Agenten kan förbereda arbetet men inte godkänna sig själv. Ändrat relevant underlag kräver ny granskning. Samma genomförandenyckel ger samma resultat vid återförsök.

### BZ-07: Fakturor, betalningar och rättelser

Kund- och leverantörsflöden SKA stödja de betalnings- och rättelsefall som finns i den verifierade profilen: delbetalning, samlingsbetalning, avgift, kredit och återförd matchning. Överbetalning ska hanteras som ett uttryckligt rest-/förskottsfall, inte klämmas till noll och försvinna.

Historiska fakturor ska inte skickas på nytt av en import. Utställd, skickad, bokförd och betald ska ha skilda betydelser.

**Acceptans:** En faktura på 10 000 kr med 4 000 kr betalt har 6 000 kr kvar. En senare kredit eller återförd betalningsallokering ändrar rätt restbelopp med bevarad historik.

### BZ-08: Privata utlägg och ägarflöden

Dessa är obligatoriska i Drastics provomfattning eftersom de finns i tidigare lämnade bolagsuppgifter. Systemet SKA skilja privat betalt bolagsutlägg, ersättning till ägaren, ägarfinansiering och privata köp med bolagets pengar. Klassificering och eventuell skattemässig behandling ska granskas, inte härledas från att betalaren är ägare.

Privata bankrörelser ska inte tas med i bolagets Cash-kontomängd. Endast bolagets faktiska betalningar och granskade återstående ersättnings-/finansieringsförpliktelser ska påverka bolagets likviditet.

**Acceptans:** Ett privat betalt utlägg och dess ersättning blir inte två kostnader. En ägarinsättning blir inte en försäljningsintäkt. Ett okänt återbetalningsdatum blir inte automatiskt en betalning idag.

### BZ-09: Moms, skatt och tidsbestämda regler

Tillämplig momsberäkning SKA använda granskade bolagsfakta och regler för den berörda perioden. Regler och parametrar ska ha källor och versioner. Nuvarande skattesats eller tabell får inte utan kontroll användas på ett historiskt år.

Underlag, beräkning, granskad deklarationsversion, inlämning, externt besked och skattekontohändelse ska hållas isär. Beräkningens rutor och belopp ska kunna härledas till redovisade behandlingar och verifikationer.

Skattekontot ska avstämmas med eget saldo och egna händelser. En överföring från banken till skattekontot ska inte ensamt bevisa att en särskild skatt är reglerad. Skatteverket anger att en inbetalning inte är avsedd för en viss enskild skatt eller avgift. [E02]

**Acceptans:** En ändrad momsberäkning skriver inte över tidigare inlämnad version. En lokalt skapad fil visas inte som inlämnad. En betalning räknas inte både som separat momsutbetalning och som överföring till skattekontot.

### BZ-10: Periodisering, tillgångar, valuta och lön

VILLKORAT SKA: varje transaktionstyp som faktiskt förekommer ska få korrekt behandling, registerpåverkan och oberoende kontroll. Avskrivningar och periodiseringar ska vara skilda från betalningar. Valutabelopp ska behålla originalvaluta, bokföringsvärde och relevant kursgrund.

Löneområdet ska inte påstås vara stött enbart för att anställdas grunduppgifter finns. Den tillämpliga löneberäkningen, betalningsunderlaget och AGI-underlaget behöver var sitt bevis. Lön från ett externt system kan användas med bevarad källa och en uttalad ansvarsfördelning. Det får inte marknadsföras som openERP:s egen verifierade löneberäkning.

**Acceptans:** Saknat stöd för ett faktiskt förekommande fall blockerar det berörda bolagsutfallet. Fallet flyttas inte till ”utanför scope” enbart för att implementationen är svår.

### BZ-11: Periodkontroller och avslut

Systemet SKA visa kontroller för huvudbok, bank, reskontror, skattekonto, moms, ägarflöden och tillämpliga register. Varje kontroll har status, verifierad omfattning, källa, ansvarig och väg till avvikelsen.

En periodbedömning ska bindas till bokföringsgräns, källomfattning och relevanta versioner. Senare rättelser ska skapa ny bedömning eller markera tidigare slutsats som inaktuell. Tekniskt periodlås är inte samma sak som fullständigt redovisningsmässigt godkännande.

**Acceptans:** Inga oförklarade monetära differenser accepteras som noll. En verklig avrundning är en dokumenterad behandling med egen grund, inte en generell tolerans som döljer fel.

### BZ-12: Granskningspaket och årsöverlämning

Systemet SKA kunna skapa ett versionsbundet paket med resultat- och balansrapport, saldobalans, huvudbok, verifikationslista, tillämplig SIE-export, öppna poster, bankavstämningar, skattekonto, momsunderlag, tillämpliga scheman och ägaravräkning. Paketet ska även ha källindex, kvarstående frågor, metodval och manifest med filhashar.

För årspaketet avses en fullständig bokföringsexport för vald omfattning med kontoplan, ingående/utgående saldon och verifikationer i kvalificerad SIE-profil, inte enbart ett fragment med nya transaktioner. Formatversion, teckenkodning och mottagarens importbeteende ska ingå i exportprovet.

En SIE-fil är inte ensam hela arkivet. Originalunderlag och kompletterande register ska kunna följas via ett läsbart index. En lokalt genererad export bevisar inte kompatibilitet: importen ska provas i granskarens avsedda program eller en oberoende relevant läsare med kontroll av saldon och transaktioner.

Granskaren ska inte behöva skriva egen kod, förstå interna primärnycklar eller manuellt återskapa standardrapporter. Granskning av ovanliga behandlingar är däremot normalt arbete och ska understödjas.

**Acceptans:** Granskaren kan dokumentera att första provperioden stämmer. Vid årspaketets acceptans täcks hela 2025-05-17 till 2026-04-30 och tillämpliga bokslutsposter. Ett accepterat överlämningspaket påstår inte att årsredovisning eller deklaration redan har lämnats in.

### BZ-13: Ny period i kontrollerad parallell drift

Efter historiskt prov SKA en ny, verklig period genomföras genom det ordinarie gränssnittet. Det ska finnas en uttalad källa för officiell bokföring och en enda ägare av externa utskick/inlämningar under parallellkörningen.

OpenERP:s provflöde ska få möta sena underlag, fel, revideringar och återförsök. Automatisk historikimport får inte användas för att dölja att den nya behandlingskedjan inte fungerar.

**Acceptans:** Normalt ekonomiarbete kan slutföras utan SQL-korrigeringar, utvecklarverktyg eller odeklarerade sidokalkyler. Eventuella supportåtgärder registreras som produktgap.

### BZ-14: Säker övergång och avveckling

Övergång SKA vara ett separat beslut efter granskning av omfattning, exporter, åtkomst, återställning och eventuella externa skyldigheter. Beslutet ska ange övergångstidpunkt, sista officiella bokföring i det gamla systemet, första skrivning i det nya och ansvarig.

Återställning ska verifiera databas, originalobjekt, krypterings-/åtkomstberoenden, verifikationer, kvitton och register. En återställd miljö får inte börja köra leverantörsåtgärder eller ekonomiska jobb innan återupptagande uttryckligen har godkänts. Återställning till gammal data efter nya officiella händelser kräver avstämning, inte blind återgång.

Räkenskapsinformation ska bevaras enligt tillämpliga regler. BFN beskriver sju år efter kalenderåret då räkenskapsåret avslutades. För ett år som avslutades 2026 innebär den generella beräkningen bevarande till och med 2033; andra skyldigheter eller bevarandestopp kan kräva längre tid. [E01]

**Acceptans:** Det gamla abonnemanget kan avvecklas utan att original, läsbarhet eller nödvändigt arbetsflöde förloras. Detta är inte uppnått bara för att en månad stämmer eller en backupfil existerar.

## 7. Det dagliga arbetsflödet

### WF-01: Startsidan ska svara på tre frågor

Startsidan SKA visa ”Behöver dig”, ”Förberett” och ”Slutfört”, tillsammans med en separat daterad ekonomisk överblick. Siffror ska komma från sina ägande domäner och ha samma omfattning som detaljvyn.

Exempel på språk, inte låst marknadsföringstext:

```text
Behöver dig
  3 transaktioner behöver förklaring
  2 underlag saknas
  Momsunderlaget kan granskas

Förberett
  12 förslag väntar på granskning

Slutfört denna period
  28 händelser bokförda efter godkännande
  8 kundfakturor betalningsmatchade

Likviditet
  Observerat banksaldo per [datum]
  Prognos och dess täckning
```

”AI har förberett” får inte visas som ”bokfört”. Alla antal ska ha en definition. Ärenden, verifikationer och bankrader är inte utbytbara räknare.

### WF-02: En sammanhållen arbetslista

Varje arbetsobjekt SKA ha stabil identitet, orsak, primärt objekt, belopp när det är känt, tillstånd, nästa handling, ansvarig och eventuellt datum. Ett samlat ärende kan ha flera delproblem, exempelvis saknat kvitto och osäker behandling, utan att dubblas som oberoende huvuduppgifter.

Arbetslistan är en projektion. Den ska inte äga fakturans status, bokföringseffekt eller ytterligare finansiella saldon. Filter, sortering och antal ska fungera över hela sökresultatet, inte bara första laddade sidan.

**Acceptans:** Rättad faktura uppdaterar tillhörande ärende. Att ”markera som läst” eller tilldela någon en uppgift kan inte stänga ett bokföringsproblem.

### WF-03: Prioritering med begriplig orsak

Prioriteringsordningen SKA vara möjlig att förklara: passerad eller nära deadline, blockerad period, saknat underlag, granskningsklart arbete och sedan övrigt. Belopp kan användas som sekundär prioritet men ska inte dölja små regulatoriskt relevanta poster.

Tystade påminnelser ska ha giltighetstid och ansvarig. De ändrar inte den underliggande skyldigheten eller periodens fullständighet. Undvik ett odokumenterat AI-poängtal som ensam prioriteringsgrund.

### WF-04: Granskning i sammanhang

När ett ärende öppnas SKA original, tolkade fakta, förslag, exakt effekt och eventuella varningar visas i samma resa. Tekniska kvitton och revisionsdetaljer ska finnas under begriplig fördjupning.

Användaren ska kunna rätta fakta utan att tappa originalets ursprung. Ett misslyckat sparande ska behålla inmatningen. Vid ändrad version ska gränssnittet förklara vad som ändrats innan ett nytt godkännande är möjligt.

### WF-05: Exakt batchgranskning

Gränssnittet SKA erbjuda ”Godkänn N granskade förslag” endast för en uttryckligt vald och synlig mängd. Första leveransen begränsar en batch till högst 25 förslag som ett produktval, inte ett juridiskt tröskelvärde.

Manifestet ska binda objekt, versioner, digest och användarens omfattning. Om något redan är inaktuellt när batchgodkännandet skapas ska användaren få rätta urvalet. Vid senare genomförande ska varje finansiell grupp återvalideras och ha eget beständigt resultat. Oberoende grupper får lyckas eller blockeras var för sig; beroende grupper ska följa sina domänkontrakt.

**Acceptans:** 11 genomförda och 1 blockerad ska visas just så. Batchen får inte ge ett falskt ”allt klart” eller skapa en enda jättetransaktion över flera oberoende arbeten. Återförsök får inte upprepa de 11 effekterna.

### WF-06: Återhämtning efter okänt utfall

Systemet SKA skilja säkert avvisad handling från okänt genomförandeutfall. Vid tappat svar behålls ursprunglig begäran och idempotensnyckel. Produkten ska kunna återfinna kvittot innan en ny åtgärd erbjuds.

**Acceptans:** Dubbelklick, omladdning eller nätverksavbrott efter commit ger en bokföringseffekt. Användaren ska kunna återuppta ärendet från vanlig navigation.

### WF-07: Navigation och tillgänglighet

Valt bolag, bok, period, filter och position SKA bevaras vid öppning och återgång. Direktlänk och omladdning ska öppna samma objekt. Tangentbord, tydligt fokus, 200 procents zoom och smal skärm ska ingå i de prioriterade kundresornas acceptans.

Ett byte av bolag får inte behålla föregående bolags innehåll som om det hörde till det nya. Rättigheter ska kontrolleras igen vid relevanta återbesök och genomföranden.

### WF-08: Ingen falsk tomhet eller framgång

Tom arbetslista, saknade källor, fel vid inläsning och faktiskt genomfört arbete SKA ha olika tillstånd. En misslyckad dataläsning får inte bli siffran noll.

Det ska finnas tydlig väg från ”källor saknas” till rätt import- eller konfigurationssteg. Intern statuskod får inte vara den enda instruktionen till företagaren.

## 8. AI-förberedelse och mänsklig kontroll

### AI-01: AI:s tillåtna arbetsuppgifter

Agenten SKA kunna förbereda tillåtna dokumenttolkningar, föreslå matchningar, sammanställa frågor och skapa förslag via befintliga applikationsoperationer. Den får beskriva ett sparat resultat men inte hitta på bokförda belopp.

Genomförande av ett redan mänskligt godkänt förslag får ske via en befintlig tillåten applikationsoperation, även genom agent eller jobb när aktörens rättighet medger det. Samma granskade version, giltiga godkännande och idempotensnyckel ska krävas. Detta är inte självständigt godkännande eller ett nytt generellt exekveringsmandat.

Den ska inte ha direkt databasåtkomst, godkännanderätt, rätt att ändra behörigheter eller fritt tillträde till externa tjänster. Ett dokument med instruktioner till modellen är underlag, inte en betrodd order.

### AI-02: Ursprung och osäkerhet

Tolkade fält SKA skiljas från bekräftade fakta. Spara källreferens, plats i dokumentet när tillgänglig, modell-/extraktionsversion och efterföljande användarrättningar. Modellens säkerhetstal är inte ett godkännande och ska inte presenteras som en verifierad sannolikhet utan kalibrering.

Ett fält som inte går att läsa ska lämnas okänt. Ingen standardvaluta, skattesats eller leverantörsidentitet får sättas för att tvinga ett komplett förslag.

### AI-03: Begränsad och återupptagbar körning

Förberedelser SKA ha avgränsat urval, budget, tidsgräns, cancellation och beständigt framsteg. Upprepade leveranser eller omstart får inte skapa flera förslag med oavsiktliga ekonomiska följder.

Modell- och nätverksanrop får inte ligga inne i en finansiell databastransaktion. Om AI-tjänsten inte är tillgänglig ska redan förberett arbete vara åtkomligt och manuellt arbete fortsätta.

### AI-04: Behörigheten lever i applikationen

Tillåten AI-förberedelse ska använda samma behandlingar som gränssnitt och REST/MCP. Godkännande ska knytas till en verkligt behörig människa och rätt förslag. Ett chattmeddelande, ett tidigare beteendemönster eller en modellbedömning är inte ett sådant godkännande.

Unattended bokföring under stående mandat är SENARE. PRD:n ändrar inte befintliga framtida mandatkrav men introducerar dem inte som genväg till första produktens automation.

## 9. Drastic Cash: produktdefinition

Cash är en förklarbar betalningsprognos, inte en alternativ huvudbok, ett kreditbeslut eller ett besked om utdelningsutrymme. Den visar ett scenario givet sparat underlag och antaganden, inte en garanti för framtida likviditet.

De centrala frågorna är:

> Vad har vi observerat? Vilka betalningar återstår? När blir marginalen som lägst? Vad händer om en kund betalar senare?

Den första beräkningsmotorn ska arbeta per dag och stödja 30 dagar, 90 dagar och 13 veckor. 13 veckor är 91 dagar. Gränssnittet ska visa faktiska start- och slutdatum och inte behandla 90 dagar och 13 veckor som samma intervall.

### CASH-01: En granskad kontomängd och ett gemensamt startläge

Prognosen SKA bindas till en juridisk enhet, relevant bok och uttryckligt valda likvidkonton. Kontonamnet eller ett BAS-kontonummer räcker inte ensamt för att bestämma om ett konto är disponibelt.

Första sammanlagda prognosen avser stödd SEK-likviditet. Privata konton, spärrade medel, tillgängliga men outnyttjade krediter och skattekontot får inte automatiskt räknas som fritt banksaldo.

Varje startobservation ska innehålla källa, konto, valuta, observerad tid, uppgiftsdatum, saldotyp och täckning. ”Bokfört banksaldo”, ”saldo enligt bankutdrag” och ”disponibelt saldo enligt bank” är olika observationer.

V1 ska beräkna från ett gemensamt avgränsat bokfört/observerat startläge. Ett realtidsfält för disponibelt saldo får inte användas i beräkningen förrän dess hantering av reservationer och kredit är känd. Det kan visas separat med rätt etikett.

**Acceptans:** Två konton med olika observationsdatum får inte summas som ”saldo idag” utan en fullständig brygga till samma tidpunkt. Saknas bryggan får produkten visa observationerna var för sig och en ofullständig prognos, inte ett påstått aktuellt totalbelopp.

### CASH-02: Startögonblick, kunskapstid och horisont

En prognos SKA spara både den ekonomiska startpunkten `asOf` och vilka uppgifter som fanns tillgängliga vid `recordedCutoff`. Alla historiska betalningar som redan ingår i startobservationen ska uteslutas från framtida flöden med bevarad koppling.

Det ska gå att öppna en gammal prognos utan att dagens fakturastatus skrivs in i den. Senare uppgifter producerar en ny prognos och en jämförelse, inte en ändrad historik.

**Acceptans:** En betalning som kom till systemets kännedom efter att en prognos sparats får inte användas för att få den gamla prognosen att se mer träffsäker ut i efterhand.

### CASH-03: En betalningsidentitet, flera källor

Varje projekterad betalning SKA ha en stabil ekonomisk identitet och ett samband med sin ägande förpliktelse eller fordran. Faktura, betalningsinstruktion, bankobservation, allokering och verifikation kan vara olika bevis för samma händelse.

Deduplicering ska använda domänägda relationer. Samma datum och belopp är bara en matchningskandidat. Två lika stora betalningar får inte slås ihop utan stöd.

En betalning kan fördelas på flera fakturor och en faktura kan ha flera delbetalningar. En sådan gruppering får inte få hela fakturabeloppet att försvinna efter en liten delbetalning.

**Acceptans:** Faktura 50 000 kr, redan betalt 20 000 kr som ingår i startbanken: framtida inflöde 30 000 kr. Varken 50 000 kr eller 10 000 kr är korrekt.

### CASH-04: Kundinbetalningar

Kundfordrans återstående belopp SKA hämtas från reskontrans ägare, inklusive betalningar, krediter och återförda allokeringar. Förfallodatum, kundens dokumenterade betalningslöfte och antaget betalningsdatum ska vara separata fält.

En faktura som redan förfallit och fortfarande är obetald får inte bara läggas på ett passerat datum och därmed försvinna ur prognosen. Den ska kräva ett uttryckligt framtida datum, ett bevarat scenarioantagande eller visas som odaterad osäker fordran.

V1 använder dokumenterade förfallodatum och manuellt granskade datumantaganden. Den uppfinner ingen sannolikhetsmodell. Inbetalningarna är fortfarande förväntningar, även om själva fordran är fastställd.

Kundkredit och överbetalning kan innebära kvittning eller återbetalning. Det ska framgå vilket. En kreditnota är inte automatiskt en kontantinbetalning eller kontantutbetalning.

### CASH-05: Leverantörsbetalningar och återkommande kostnader

Återstående leverantörsskulder SKA hämtas från deras ägande register. Godkännande av en faktura och genomförande av en betalning är olika tillstånd. En skickad betalningsfil är inte bevis för att banken har belastats.

Återkommande framtida kostnader ska vara granskade prognosåtaganden med belopp, datum, källa och giltighet, inte bokförda skulder bara för att de behövs i prognosen. När en verklig faktura ersätter ett sådant åtagande ska en explicit serie-/förekomstkoppling förhindra dubbelräkning.

Okända eller ofullständigt granskade leverantörsfakturor ska ingå i täckningsrisken. De får inte döljas för att bara ”godkända” fakturor projiceras. Ett oförklarat framtida utflöde ska göra uppskattningen ofullständig tills belopp eller avgränsning är kvalificerad.

**Acceptans:** En granskad månadshyra och den senare fakturan för samma månad räknas en gång. Samma belopp nästa månad är en annan förekomst.

### CASH-06: Lön och personalrelaterade betalningar

Cash SKA skilja nettolön, innehållen personalskatt, arbetsgivaravgifter och övriga faktiska betalningar. Lönens kostnadsredovisning ska inte användas som en extra betalning ovanpå löneutbetalning och skattekontofinansiering.

Fastställd lönekörning, granskad extern lönefil och uppskattad kommande lönekörning ska ha olika källa och säkerhet. När en uppskattning ersätts av en fastställd körning ska den inte summeras ovanpå den.

Exempel med enbart illustrativa belopp, inte skattesatser: bruttolön 50 000 kr, innehållen skatt 10 000 kr och arbetsgivaravgift 15 000 kr ger nettolön 40 000 kr och 25 000 kr i relaterade skatteposter. Det är inte ett framtida flöde på 50 000 + 40 000 + 25 000 kr. Skattekontots tillgängliga saldo påverkar sedan det ytterligare bankbehovet.

### CASH-07: Skattekontots finansieringsbehov

Skattekontot SKA modelleras som en separat avstämd position. Cash ska projicera kända och uppskattade debiteringar, kvalificerade krediteringar, redan gjorda överföringar och återstående finansieringsbehov.

En granskad debitering kan ha flera representationer: beräknat momsunderlag, inlämnad deklaration och extern skattekontohändelse. Relationerna ska avgöra om dessa beskriver samma skyldighet. Välj aktuell kvalificerad representation utan att radera tidigare versioner. En ändringsdeklaration kan också innebära en uttrycklig differens; den får inte alltid behandlas som vare sig ett extra helt belopp eller en total ersättning.

Prognosen ska rulla skattekontots saldo i datumordning. Ytterligare överföringar från bank beräknas bara för otäckta behov enligt den valda finansieringspolicyn. Ränta, anstånd, återbetalningar och andra poster ska tas med när de är relevanta och kvalificerade. Saknad kunskap visas som lucka.

Planerad banköverföring och skattekontokreditering ska ha en känd relation och ett kvalificerat tillgänglighetsdatum. Bankdagar och senaste betalningsdag är daterade regler eller uttryckliga granskade indata, inte ”minus en dag” hårdkodat för alla fall.

**Exempel:** Bank 100 000 kr, skattekonto 30 000 kr och framtida skattedebiteringar 50 000 kr. Med dessa avgränsade antaganden behövs ytterligare 20 000 kr från bank. Bankprognosen ska inte också dras med hela 50 000 kr. Ett senare verkligt genomförande ersätter den planerade överföringen.

Skatteverkets beskrivning av att inbetalningar inte avser en enskild skatt ligger till grund för denna åtskillnad. Modellen ovan är produktdesign, inte en fullständig specifikation av alla skattekontoregler. [E02]

### CASH-08: Övriga betalningar och ägarflöden

Försäkring, investering, amortering, ränta, återbetalning av utlägg och ägarfinansiering SKA få separata, spårbara prognosflöden när de gäller bolaget. Amortering och ränta får inte förväxlas med kostnad respektive hela skuldens saldo.

Planerad investering ska inte automatiskt få samma likviditetsprofil som en redan betald tillgångs avskrivningar. En odaterad ägarskuld ska visas med belopp och datumlucka, inte krävas fullt idag eller uteslutas utan varning.

Nya lån, outnyttjad kredit, ännu inte beslutade ägarinsättningar och försäljningsmöjligheter får bara läggas in som tydligt separata scenarier. De får inte döljas i det ordinarie bankstartsaldot.

### CASH-09: Interna överföringar och medel under överföring

En verifierad överföring inom samma likvidkontomängd SKA vara neutral för sammanlagd likviditet. Om pengarna befinner sig under överföring vid start eller slut måste kontomängd och observationsbrygga hantera detta uttryckligt.

Endast en importerad sida, två likadana motriktade belopp eller en otydlig banktext är inte tillräckligt för att hävda att en intern överföring är fullständigt avstämd. Inkludering av ett transitkonto måste ha kvalificerad grund och får inte skapa ”disponibla” medel som inte går att använda.

Skattekontot är utanför den första disponibla bankkontomängden. Överföring dit är därför ett bankutflöde i denna prognos även om skattekontot också är en tillgångspost i bokföringen.

### CASH-10: Reservationer och väntande betalningar

Håll isär bankens observerade saldo, bokförda betalningar, väntande instruktioner och spärrade medel. Startmodellens behandling av varje kategori SKA vara definierad så att samma reservation inte dras både i startsaldot och igen som framtida utflöde.

V1:s huvudberäkning använder den definierade bokförda/observerade startmodellen. Ett bankfält för disponibelt saldo med okänd reservationssemantik ska inte ersätta den modellen. Oklara reservationer hindrar en komplett uppskattning men ska vara synliga.

**Acceptans:** Om 5 000 kr redan är avdraget i ett kvalificerat disponibelt saldo och samma reservation senare bokförs ska det inte uppstå ytterligare ett nettoavdrag på 5 000 kr för samma ekonomiska effekt. Alternativt ska produkten vägra använda den saldotypen tills sambandet kan bevisas.

### CASH-11: Daglig prognos och likviditetsutrymme

Alla beräkningar SKA använda exakta heltal i minsta valutaenhet. Belopp i API:er överförs med repo:ts gemensamma pengakontrakt. Avrundning får ske endast med uttrycklig policy där omräkning eller presentation kräver det.

För ett scenario `s`, ett gemensamt startögonblick `t0` och varje dag `d` gäller:

```text
B_s(d) = B0 + summa(projekterade inflöden efter t0 till och med d)
              - summa(projekterade utflöden efter t0 till och med d)

M_s(H) = min(B0 och alla dagssaldon fram till horisonten H)

L_s(H) = M_s(H) - vald likviditetsbuffert
```

`B0` innehåller bara kvalificerade medel inom den valda kontomängden. Varje betalning ingår exakt en gång. Reserv för skatt som redan finansieras av ett prognostiserat bankutflöde får inte dras igen efteråt.

`L_s(H)` är **beräknat likviditetsutrymme**, inte redovisningens kassaflöde, fritt eget kapital eller en juridisk distributionsprövning. Bufferten är ett explicit produkt-/användarantagande, inte en lagstadgad gräns. Negativa värden ska visas som underskott och får inte klippas till noll.

För betalningar samma dag ska produkten kunna visa ett konservativt stressläge där utflöden föregår inflöden när intradagsordningen är okänd. Dagsmodellen är inte en garanti för att en bank kan verkställa en viss betalning under dagen.

### CASH-12: Täckning, färskhet och okända belopp

Varje prognos SKA ha fyra separata kvalitetsdimensioner: källtäckning, uppgifternas aktualitet, avstämningsstatus och antagandenas osäkerhet. De får inte ersättas med ett enda godtyckligt ”AI confidence”-värde.

En översiktsstatus kan vara:

| Status | Betydelse | Tillåten presentation |
|---|---|---|
| Tillräckligt underlag för vald omfattning | Kontomängd och tillämpliga betalningsfamiljer är kontrollerade. | Beräknat utrymme med datum, scenario och antaganden. Inte garanti. |
| Ofullständigt underlag | Tillämplig källa, belopp eller avgörande datum saknas. | Kända flöden och namngivna luckor. Inget obetingat ”du kan spendera”. |
| Inaktuellt underlag | Tidigare observationer kan visas men når inte vald aktualitetspolicy. | Sparad prognos med datum och tydlig inaktualitet. |
| Tekniskt fel/ej tillgängligt | Beräkning eller läsning kunde inte slutföras. | Fel och återhämtning. Aldrig noll som ersättningsvärde. |

Kända framtida löne- och skattebehov måste täckas genom fastställda data eller granskade uppskattningar. En prognos med bara dagens fakturor är ett särskilt ”kända poster”-scenario, inte automatiskt en fullständig 90-dagarsprognos.

**Acceptans:** Ett okänt tillämpligt momsbelopp kan inte representeras som 0 kr. Ett uteblivet inflöde får inte bli godtyckligt ”konservativt noll” utan att antagandet redovisas. Systemet ska visa även odaterade belopp utanför grafen.

### CASH-13: Scenarier utan ändrad bokföring

Användaren SKA kunna flytta en förväntad kundinbetalning, ändra ett uttryckligt prognosåtagande och lägga in en hypotetisk investering. Scenariot ska binda till en grundprognos och spara ändring, skapare, datum och motivering.

Scenarier får inte ändra fakturans juridiska förfallodatum, löneunderlag eller bokföring. En skattepåverkande händelse måste visa om följdeffekten beräknas av en kvalificerad regel eller inte ingår. V1:s rena betalningsdatumscenario ska inte beskrivas som en fullständig företagsbudget.

Vid nya verkliga uppgifter ska användaren kunna skapa en ombaserad scenariojämförelse. Den gamla prognosen och scenarioversionen bevaras.

### CASH-14: Förklaring och bidrag per belopp

Varje total, dag och betalningsrad SKA kunna öppnas till dess bidrag. Där ska framgå objekt, restbelopp, valuta, datumgrund, inkluderingsbeslut, källa och relevant antagande.

AI kan formulera en förklaring utifrån den sparade prognosens bidrag. Det numeriska svaret och dess hänvisningar ska komma från beräkningsresultatet. Saknade uppgifter eller svag täckning ska följa med till svaret.

**Acceptans:** Frågan ”Varför är lägsta saldot 30 000 kr?” leder till de exakta betalningar och datum som gav resultatet. En modelltjänst som ligger nere hindrar inte den deterministiska förklaringsvyn.

### CASH-15: Valuta och rapporterad täckning

SEK är första sammanlagda profil. En skyldighet i annan valuta kan ingå först med stödd kurs-, datum- och avrundningspolicy samt bevarat originalbelopp. Saknad kurs ska inte bli 1:1.

Om Drastic faktiskt har en sådan förpliktelse ska antingen dess nödvändiga omräkningsstöd levereras eller prognosen märkas ofullständig för bolaget. Det är inte tillåtet att få ”fullständig” genom att tyst utelämna utländska betalningar.

### CASH-16: Kompletterande nyckeltal

V1 SKA ge förfallna kundfordringar, kundkoncentration i öppna fordringar och datum för första prognostiserade buffert-/nollpassage. Definitioner och nämnare ska visas.

Kundkoncentration i fordringar är kundens öppna fordran dividerad med totala öppna fordringar vid samma snapshot. Det är inte samma mått som omsättningskoncentration. Noll nämnare ger ”ej tillämpligt”, inte en felaktig procentsats.

Runway ska i första hand beskrivas som första dag under vald gräns i det valda scenariot. Ingen passage inom 13 veckor betyder ”ingen passage inom visad period”, inte obegränsad runway. Historiskt kassaflöde och resultatmått ska behålla sina befintliga rapportägare.

### CASH-17: Sparande, delning och export

Sparade prognoser SKA innehålla källgränser, beräkningsversion, scenarioversion, kontomängd, bidrag, uteslutningar, kvalitetsstatus och exakta resultat. JSON/CSV-export ska återge samma semantiska innehåll som gränssnittet.

Behörighet ska kontrolleras även vid export och återöppning. En aktör vars åtkomst återkallats ska inte kunna hämta ett gammalt snapshot via en ny begäran bara för att länken eller ID:t är känt.

## 10. Föreslagna datakontrakt och tillstånd

Följande namn är **föreslagna produktbegrepp**, inte påståenden om befintliga exportnamn, tabeller eller endpoints. Implementationen ska först binda varje begrepp till repo:ts faktiska ägare.

| Begrepp | Minsta semantik | Äger inte |
|---|---|---|
| `CompanyScope` | Bolag, bok, giltighet, metodval, tillämpliga familjer och källförteckning. | Ett nytt parallellt bolagsregister. |
| `WorkItem` | Projekterad nästa handling, ekonomiskt objekt, orsak, ansvarig och länkar. | Fakturans eller verifikationens auktoritativa status. |
| `ReviewBatch` | Förslagsidentiteter, exakta versioner, manifest och resultat per grupp. | Rätt att kringgå ordinarie godkännande. |
| `PeriodAssessment` | Kontrollomfattning, bokföringsgräns, källrevisioner, slutsats och granskare. | Att deklarationen är inskickad. |
| `CashBasis` | Kontoobservationer, gemensam tidpunkt, kvalificerade bryggor och begränsningar. | Bokföringens bankkonto eller bankens saldo. |
| `CashEvent` | Stabil betalningsidentitet, ägande förpliktelse, restbelopp, datumgrund och referenser. | Ny bokförd fordran eller skuld. |
| `ForecastAssumption` | Hypotes, ersättningsrelation, giltighet, skapare och granskningsstatus. | Verifierad faktisk affärshändelse. |
| `CashForecast` | Fryst underlag, bidrag, resultat, kvalitetsdimensioner och beräkningsversion. | Rätt att disponera eller överföra pengar. |
| `CashScenario` | Grundprognos och explicit uppsättning alternativa antaganden. | Ändring av den underliggande bokföringen. |
| `AcceptanceRecord` | Vad som prövats, mot vilken revision, av vem och med vilka begränsningar. | Automatiskt godkännande av andra bolag eller miljöer. |

### 10.1 Betalningspostens minimum

```text
CashEvent
  scope: juridisk enhet + bok
  economicIdentity: ägande objekt + betalningsförekomst
  sourceReferences: versionsbundna referenser
  amountMinor: exakt återstående belopp
  currency: originalvaluta
  direction: inflöde eller utflöde
  dueDate: avtals-/regelgrund när känd
  expectedDate: separat prognosdatum när känt
  amountBasis: fastställt / granskat estimat / okänt
  dateBasis: dokumenterat / explicit antagande / okänt
  executionState: planerad / instruerad / okänt utfall / observerad / avbruten
  representedInOpening: kvalificerat ja/nej/okänt med referens
  supersedesOrSettles: exakta ersättnings- och avräkningsrelationer
  inclusion: med / utan / blockerad, med skäl
```

Belopp, datum, genomförandestatus och prognosinkludering är separata dimensioner. En fastställd faktura betyder exempelvis inte att pengarna säkert kommer på förfallodagen.

### 10.2 Viktiga tillståndsgränser

Förberedande arbete kan gå från saknade uppgifter till berett, granskningsklart och godkänt. Genomförande har separat tillstånd för genomfört, avvisat och okänt utfall. Rättelse länkar till ett nytt förslag, inte till redigering av bokförd historik.

Arbetslistan visar dessa tillstånd från ägande domäner. Skapa inte en global statusmaskin som ersätter alla faktura-, moms-, bank- och bokföringslivscykler.

## 11. Kundresor och skärmacceptans

| Resa | Start | Förväntat avslut |
|---|---|---|
| Första period | Bolag med dokumenterad profil och råunderlag. | Sparad periodbedömning och ett granskningspaket som kan öppnas oberoende. |
| Saknat kvitto | Arbetslistans namngivna bankhändelse. | Underlag kopplat, fakta granskade och relevant nästa steg slutfört. |
| Förslag från agent | Förberedd behandling. | Människa granskar exakt effekt och kan återfinna resultatet efter omladdning. |
| Samlingsgranskning | Valda förslag. | Varje grupp har tydligt resultat och blockerade grupper kan tas om hand. |
| Delbetalning | Kundfaktura och bankobservation. | Avstämt restbelopp i faktura, bank och ny Cash-prognos. |
| Periodavvikelse | Periodens namngivna kontrollgap. | Korrigerat underlag eller godkänd rättelse, följt av ny kontroll. |
| Likviditetsfråga | Daterat Cash-läge med kvalitetsstatus. | Öppnade bidrag och förstådd lägsta likviditet. |
| Försenad kund | Sparad prognos. | Separat scenario med jämförbara dagssaldon och oförändrad faktura. |
| Granskaröverlämning | Sparat årspaket. | Granskaren öppnar det i avsedd miljö och dokumenterar kontrollen. |

Varje prioriterad resa ska innehålla tomt läge, inläsning, sparat läge, fel, omladdning och återgång där tillståndet är relevant. Ett screenshot bevisar inte att operationen fungerar. En lyckad API-körning bevisar inte att gränssnittet fungerar.

Cash-skärmen ska visa observerat saldo och datum överst, därefter lägsta prognostiserade saldo med datum, likviditetsutrymme efter buffert och tillgänglig täckning. Graf och tabell ska ha samma siffror. Kunden ska kunna se alla inkluderade och uteslutna betalningar utan att chatta med en modell.

## 12. Arkitektur och integration

### 12.1 Bevara befintlig ägarfördelning

| Ägare i repo:t | Arbete i denna leverans |
|---|---|
| `apps/web` | Startsida, arbetslista, granskning, periodresa och Cash-vyer. Utöka befintlig komposition och behåll URL-scope. |
| `apps/web/src/lib/company-work.ts` | Startpunkt för företagsöversiktens befintliga domänläsningar. Undvik klientberäknade konkurrerande finansiella totaler. |
| `apps/api/src/application` | Beredning, behörighet, periodbedömning, snapshot-orkestrering och läsande prognosoperationer. |
| `apps/api/src/db` | Befintlig scoped anslutning, transaktioner, persistens och kontrollerade läsningar. |
| `packages/domain` | Exakta värden, rena prognosberäkningar och domänfel där de har konkreta konsumenter. |
| `packages/contracts` | Gemensamma input/output-kontrakt, scope, kvalitetsstatus och fel. |
| `jurisdictions/se` | Tillämpliga svenska moms-/skatteberäkningar och SIE-funktioner. Cash konsumerar deras kvalificerade resultat. |
| `packages/ui` | Befintliga StyleX-baserade komponenter, beloppspresentation och gemensamma tillstånd. |
| Befintlig Bun/effect-mq-process | Avgränsad beredning och omberäkning genom befintligt beständigt arbetsflöde. |
| `infra/alchemy` och vald driftkomposition | Produktens verkliga körmiljö och driftbevis. Inget driftval görs om bara för Cash. |

Dessa gränser följer repo:ts dokumenterade ägarskap. [R02] Specifika nya funktionsnamn och filplaceringar ska bestämmas efter ägarinventering, inte genom att kopiera begreppstabellen ovan till en ny plattform.

### 12.2 Snapshot och samtidighet

Samla ett versionsbundet underlag med tydlig bokförings- och kunskapsgräns. Beräkna utanför långvariga finansiella lås. Kontrollera sedan relevanta beroenden innan snapshot förseglas. Ett resultat som inte längre kan bindas till de granskade versionerna ska sparas som inaktuellt eller räknas om enligt kontraktet, inte presenteras som aktuellt.

Långvariga jobb ska använda befintlig outbox och återupptagning. Läsprojektioner ska ha versions-/aktualitetsmarkör. En gammal webhook eller jobbkörning får inte skriva över ett nyare resultat. Ingen separat balans ska finnas i modellen, kön eller webbläsaren.

### 12.3 Gemensamma gränssnitt

Den gemensamma applikationsoperationen ska ge samma semantik för UI, REST och de MCP-läsningar som faktiskt exponeras. Cashs läsning och förklaring kan exponeras för agenten. Policyförändring eller godkännande får inte bli tillgängligt för agenten bara för att motsvarande UI-operation finns.

Behåll befintliga återhämtningsvägar tills de ersatts med verifierade användarresor. Skapa inte parallella importörer, granskningsmotorer, skatteberäkningar eller rapporttotaler för att få en ny vy klar snabbare.

### 12.4 Vad som inte ska införas

Ingen grafdatabas, mikrotjänstuppdelning, ny stylinglösning, modellberoende bokföringsmotor eller generell regelplattform är ett krav. Bend-verifiering kan bidra med oberoende räknebevis men ersätter inte bolagsunderlag, runtime-kontroller eller skatteprofilens giltighet.

## 13. Icke-funktionella produktkrav

### NFR-01: Korrekthet och spårbarhet

Alla ekonomiska belopp ska vara exakta enligt gemensamt kontrakt. Varje påverkan ska kunna återfinnas från sitt kvitto och underlag. Spårbarhet ska finnas även efter rättelse och omberäkning. Ekonomiska integritetsfel är releaseblockerare.

### NFR-02: Åtkomst och integritet

Bolags- och bokscope kontrolleras på servern vid läsning, export och mutation. Behörigheter för agent, operatör, granskare och drift hålls isär. Loggar ska inte innehålla fullständiga kvitton, personnummer, löneuppgifter eller bankhemligheter för produktanalysens skull.

Extern dokumenttolkning kräver ett dokumenterat beslut om databehandling, leverantör och tillåtna uppgifter. Produkten får inte påstå att data stannar inom en viss geografi utan verifierad drift- och leverantörsgrund.

### NFR-03: Återställning och okända utfall

Avbrott, omstart, dubbelleverans och timeout ska ge kontrollerat och återupptagbart beteende. Ett genomförandekvitto och den finansiella effekten ska inte kunna divergera. Driftmål för tillåten dataförlust och återställningstid ska beslutas under D-07 och mätas före verklig övergång.

### NFR-04: Svarstid som mätbart mål

För den första användbarhetsmätningen används en uttryckligt definierad provprofil med upp till 5 bankkonton, 10 000 bankrader per år, 2 000 öppna fakturor och 5 000 framtida betalningsposter. Detta är en föreslagen testprofil, inte ett mätt kapacitetslöfte eller ett tak för bokföringen.

Mål i vald testmiljö: första användbara startsida inom 2 sekunder på p95, öppning av sparad prognos inom 2 sekunder på p95 och normal omberäkning inom 5 sekunder på p95. Längre arbete ska få ett beständigt jobb-ID och ärlig framstegsstatus. Målbrist ska redovisas med uppmätt profil, inte döljas genom tyst kapning av poster.

### NFR-05: Tillgänglighet och återanvändning

Prioriterade resor ska fungera med tangentbord, begriplig fokusordning, smal skärm och 200 procents zoom. Använd befintliga komponenter och översättningssystem. Pengar, datum, tidszon och tecken ska presenteras konsekvent. Tekniska tidpunkter ska inte användas som svenska bokföringsdatum utan explicit datumsemantik. Den svenska användarvyn använder Europe/Stockholm när en tidpunkt behöver omvandlas till ett lokalt datum. Ett redan fastställt bokförings- eller förfallodatum är ett kalenderdatum och får inte förskjutas av UTC-omvandling.

### NFR-06: Arkiv och exportbarhet

Original, rapporter och manifest ska kunna öppnas utan ett aktivt abonnemang hos det gamla systemet. Arkivets retention och åtkomst ska vara explicit konfigurerade och förenliga med tillämpliga regler. BFN:s generella tidsregel är en grund, inte ett fullständigt godkännande av valfri lagringsplats eller molntjänst. [E01]

## 14. Oberoende acceptansfall

Fallen nedan är krav på bevisning, inte en rapport om redan utförda tester. Förväntningarna ska härledas oberoende av produktionsberäknaren. Tillämplighet ska kvalificeras separat från aritmetiken.

Repo:ts `AGENTS.md` kräver uttryckligt godkännande för ändrade eller nya tester. Den här dokumentleveransen skapar inte sådana repoändringar och utvidgar inte tidigare behörighet. Scenarierna ska ändå finnas i acceptansplanen och verifieras inom faktiskt godkänd test-/körningsomfattning. Saknad behörighet eller saknade original ska registreras som namngiven blockerare, inte som passerat prov. [R02, R07]

### 14.1 Bokföring, arbetsflöde och behörighet

| ID | Fall | Oberoende förväntat resultat | Huvudkrav |
|---|---|---|---|
| AT-01 | Samma bankfil importeras två gånger. | Två importförekomster kan bevaras. Ingen extra ekonomisk effekt. | BZ-02 |
| AT-02 | Två utdrag överlappar delvis. | Överlapp klassificeras; en ekonomisk händelse räknas en gång. | BZ-02, BZ-03 |
| AT-03 | En hel månad saknas men laddade rader balanserar. | Källlucka kvarstår och perioden är inte fullständigt avstämd. | BZ-03 |
| AT-04 | Historik innehåller en kostnad vars kvitto senare laddas upp. | Källkoppling förbättras utan ny kostnad. | BZ-04 |
| AT-05 | Provboken rekonstruerar rådata. | Kontroll görs mot granskade förväntningar, inte enbart mot importerad facitbok. | BZ-04 |
| AT-06 | Ingående öppen faktura betalas efter migration. | Restbelopp minskar korrekt och ingen dubblerad historisk intäkt uppstår. | BZ-05 |
| AT-07 | Privat utlägg 1 000 kr ersätts av bolaget. | En kostnadsbehandling och en ersättnings-/avräkningskedja, inte två kostnader. | BZ-08 |
| AT-08 | Ägaröverföring och motsvarande bankinsättning importeras. | En ekonomisk överföring, inte försäljningsintäkt eller dubbla insättningar. | BZ-08 |
| AT-09 | Kundfaktura 10 000 kr delbetalas med 4 000 kr. | Återstående 6 000 kr och spårbar allokering. | BZ-07 |
| AT-10 | Agent försöker godkänna eget förslag. | Avslag utan förändrat godkännande eller ekonomisk effekt. | BZ-06, AI-04 |
| AT-11 | Underlaget ändras efter godkännande. | Gammalt godkännande kan inte användas för den ändrade effekten. | BZ-06 |
| AT-12 | Två samtidigt skickade genomföranden med samma identitet. | En finansiell effekt och återfunnet gemensamt kvitto. | WF-06 |
| AT-13 | Svar tappas efter commit. | Vanliga gränssnittet återfinner utfallet med ursprunglig nyckel. | WF-06 |
| AT-14 | Batch med 12 grupper, en blir inaktuell före genomförande. | 11 oberoende giltiga kan genomföras, en blockeras. Sann status per grupp. | WF-05 |
| AT-15 | Användarens rättighet återkallas under arbetet. | Nytt genomförande nekas även om sidan fortfarande är öppen. | NFR-02 |
| AT-16 | Samma ärende har saknat kvitto och osäker behandling. | En huvuduppgift med två förklarade delproblem. | WF-02 |
| AT-17 | Arbetslistans API ger fel. | Felstatus, inte ”0 uppgifter” eller ”allt klart”. | WF-08 |
| AT-18 | Granskare importerar SIE och öppnar underlagsindex. | Rätt saldo/transaktioner och fungerande spårbarhet utan specialkod. | BZ-12 |
| AT-19 | Återställning till en ny isolerad miljö. | Matchade kontrolltotaler och original. Inga externa jobb aktiveras av sig själva. | BZ-14 |
| AT-20 | Lön, valuta eller tillgång är faktisk men stödet saknas. | Berört verkligt bolagsutfall blockeras och luckan namnges. | BZ-10 |

### 14.2 Cash och dubbelräkning

Samtliga belopp i tabellen är illustrativa SEK-belopp. De är inte Drastics verkliga saldon eller svenska schabloner.

| ID | Fall | Oberoende förväntat resultat | Huvudkrav |
|---|---|---|---|
| AT-21 | Faktura 50 000, 20 000 betalt före start och med i bank. | Framtida inflöde 30 000. | CASH-02, CASH-03 |
| AT-22 | Leverantörsbetalning finns redan i startbanken. | Inget andra avdrag för samma betalning i framtiden. | CASH-03, CASH-05 |
| AT-23 | Banköverföring 10 000 mellan två inkluderade konton. | Sammanlagd nettoeffekt 0, med verifierad relation. | CASH-09 |
| AT-24 | Två orelaterade poster +10 000 och -10 000. | Får inte automatiskt döpas till intern överföring. | CASH-03, CASH-09 |
| AT-25 | Skattekonto 30 000, kommande debiteringar 50 000. | Ytterligare bankfinansiering 20 000 enligt antagen datumordning. | CASH-07 |
| AT-26 | Momsutkast, inlämnad version och skattekontopost avser samma 20 000. | En kvalificerad skyldighet, inte 60 000 i framtida utflöde. | CASH-07 |
| AT-27 | Momsrättelse ändrar en skyldighet 20 000 till 25 000. | Rätt total/differens enligt kvalificerad ändringsrelation, inte blind summering. | CASH-07 |
| AT-28 | Nettolön 40 000, personalskatt 10 000, avgift 15 000. | Löneflöde 40 000 och skattepositioner 25 000, inte dessutom bruttolönen. | CASH-06 |
| AT-29 | Avskrivning 2 000 utan betalning. | Framtida kassaflöde 0 för just avskrivningen. | CASH-08 |
| AT-30 | Privat utlägg 1 000 ännu inte ersatt. | Privat betalning ingår inte i bankstarten. En kvalificerad återbetalning kan ge -1 000 framåt. | CASH-08 |
| AT-31 | Granskad återkommande hyra och faktisk faktura för samma månad. | En förekomst via ersättningsrelation. Nästa månad bevaras separat. | CASH-05 |
| AT-32 | Förfallen kundfordran saknar nytt datum. | Synlig odaterad osäker fordran, inte försvunnen eller automatiskt betald idag. | CASH-04, CASH-12 |
| AT-33 | Valutaskuld saknar kursgrund. | Ingen 1:1-omräkning och ingen falskt fullständig total. | CASH-15 |
| AT-34 | Ett konto är observerat en vecka tidigare än övriga. | Ingen obryggad ”saldo idag”-summa. | CASH-01 |
| AT-35 | Betalning samma dag som start men redan med i saldot. | Bevisad startinkludering styr, inte enbart datumjämförelse. | CASH-02 |
| AT-36 | Bankens disponibla saldo inkluderar reservation 5 000. | Ingen dubbel reducering, eller explicit avvisning av okvalificerad saldotyp. | CASH-10 |
| AT-37 | Senare bankuppgift laddas efter att prognosen sparats. | Nytt snapshot. Det gamla behåller sin dåvarande kunskapsgräns. | CASH-02, CASH-17 |
| AT-38 | Scenariot flyttar en kundbetalning 14 dagar. | Annan prognoskurva, samma riktiga faktura och verifikationer. | CASH-13 |
| AT-39 | Prognos har positivt slutsaldo men negativt lägsta saldo. | Underskott och datum visas. Slutsaldo får inte ensamt styra utrymmet. | CASH-11 |
| AT-40 | Alla öppna kundfordringar är 0. | Koncentrationsmått ”ej tillämpligt”, ingen division med noll. | CASH-16 |
| AT-41 | Ingen nollpassage inom 91 dagar. | ”Ingen passage inom visad period”, inte oändlig runway. | CASH-16 |
| AT-42 | Löne-/momsuppgifter saknas för tillämplig framtida period. | Ofullständigt underlag, inte tysta nollbetalningar. | CASH-12 |
| AT-43 | En äldre omberäkning avslutas efter en nyare. | Nyare aktuellt resultat ersätts inte av äldre. | NFR-03 |
| AT-44 | En aktör försöker exportera annat bolags prognos. | Avslag även med korrekt gissat snapshot-ID. | NFR-02 |
| AT-45 | Samma underlag, regler och scenarioversion används två gånger. | Samma semantiska bidrag och exakta totalsummor. | CASH-11, CASH-17 |

### 14.3 Genomräknat 30-dagarsexempel

Antaganden: ett fullständigt gemensamt startläge, endast SEK, inga ytterligare betalningar, buffert 10 000 kr och kvalificerade betalningsdatum. Beloppen är oberoende exempel, inte en körning av openERP eller ett skatteexempel.

Startbank är 100 000 kr. Skattekontot har separat 30 000 kr. Skattedebiteringar på 50 000 kr dag 12 finansieras därför av en ytterligare banköverföring på 20 000 kr dag 11 i just detta exempel. Datumet dag 11 är ett givet exempelvärde, inte en generell bankdagsregel.

| Dag | Bankpåverkande händelse | Belopp | Bank efter händelsen |
|---|---|---:|---:|
| 0 | Observerat startsaldo | 100 000 | 100 000 |
| 5 | Återstående leverantörsbetalning | -40 000 | 60 000 |
| 8 | Återstående kundinbetalning A | 30 000 | 90 000 |
| 10 | Nettolön | -40 000 | 50 000 |
| 11 | Ytterligare finansiering av skattekontot | -20 000 | 30 000 |
| 12 | Skattedebitering sker på skattekontot | 0 i bank | 30 000 |
| 20 | Kundinbetalning B | 60 000 | 90 000 |
| 30 | Periodens slut | 0 | 90 000 |

Grundscenario: lägsta banksaldo 30 000 kr, slutsaldo 90 000 kr och likviditetsutrymme efter buffert 20 000 kr.

Flytta endast kundinbetalning A från dag 8 till dag 22. Då blir saldot 20 000 kr efter lönen dag 10 och 0 kr efter skatteöverföringen dag 11. Efter kund B dag 20 finns 60 000 kr och efter kund A dag 22 åter 90 000 kr.

Förseningsscenario: **samma slutsaldo 90 000 kr**, men lägsta banksaldo 0 kr och likviditetsutrymme efter buffert **-10 000 kr**.

Detta är det centrala användarvärdet: två scenarier kan ha samma månadsslut men helt olika betalningsmarginal under månaden. Cash ska visa båda fakta utan att ändra den riktiga fakturan.

## 15. Leveranspaket och beroenden

Leveranspaketen nedan är en kundutfallsordning över befintliga ägare. För varje paket ska implementationen först ange befintligt krav/paket, vad som redan finns, kvarvarande delta och hur resultatet ska verifieras. Skapa ingen ny parallell ”done”-räkning.

| Paket | Leverans | Beroende | Relation till befintliga ägare/gates |
|---|---|---|---|
| L0: Scope och nulägesavstämning | Dokumenterad Drastic-profil, källinventering, ägarmappning och verifieringsplan. | Tillgängliga bolagsuppgifter och aktuell kod. | D-04/D-06/D-08 samt repo:ts maintained plans. |
| L1: Första hela periodresan | Råunderlag till avstämning och granskningspaket i vanlig UI. | L0 samt relevanta P0/P1-gränser. | Befintlig import, bank, bokföring, moms och periodgranskning. P2/P4/P5 i tillämplig omfattning. |
| L2: Arbetslistan som produkt | Sammanhängande arbete, tydliga statusar, exakt batch och återhämtning. | L1:s domänoperationer. Delar utvecklas direkt med L1. | Frontendresor, P3 och befintliga cases/review-ägare. |
| L3: Cash-underlag | Kontomängd, startbrygga, restposter, kvalitetsstatus och förklarbara bidrag. | Relevanta verifierade domänläsningar, inte visst antal kunder. | Befintlig bank/reskontra/skatt/lön. Ny projektion vid faktisk lucka. |
| L4: Cash-prognos | 30/90 dagar, 13 veckor, datumrisk och frysta scenarier. | L3 och oberoende aritmetiska/semantiska fall. | Läsande prognosägare. Inte NEXT-45:s historiska rapport. |
| L5: Årsöverlämning och ny period | Hela första årets underlag granskas. Ny period genomförs i parallell drift. | Tillämpligt redovisningsdjup och granskare. | P4/P5/P6 samt kundresor. |
| L6: Övergångsprov | Export, återställning, operativa rutiner och godkänd single-writer-övergång. | Relevant bolagsomfattning klar, D-01/D-07/D-10 där tillämpligt. | P7. |
| L7: Book One | En liten extern pilot med samma verifierade profil. | L1/L2 och avgränsat drift-/bolagsgodkännande. Cash säljs bara med verifierad omfattning. | Inte generell öppning för alla svenska bolag. |

Parallellt arbete får ske på rena beräkningar, UI med tydligt märkta syntetiska uppgifter och dokumenterade gränssnitt. Verkliga regler, underlag eller leverantörsutslag får aldrig ersättas av syntetiska värden när ett bolagsgodkännande ska ges.

En blockerad integration ska inte stoppa ett filbaserat kontrollflöde som uppfyller samma definierade behov. En saknad bokföringsförmåga som faktiskt krävs får däremot inte döljas som en ”integrationsfråga”.

## 16. Godkännanden och vad de betyder

| Gate | Krav för godkännande | Vad den inte betyder |
|---|---|---|
| G0: Omfattning klar | Källor och bolagsprofil fastställda för provet, okända uppgifter namngivna. | Inte bokföringsmässigt godkännande. |
| G1: Historisk period verifierad | Rådataresan har oberoende kontroller, inga oförklarade differenser och granskarens versionsbundna bedömning. | Inte hela året, produktion eller alla svenska AB. |
| G2: Vardagsflödet verifierat | Prioriterade UI-resor, behörighetsfall och återhämtning fungerar på angiven revision/miljö. | Inte fullständig bolagsdata eller skatteprofil. |
| G3: Cash verifierat för vald profil | Start, betalningsidentiteter, skatt/lön, datagap, scenarier och acceptansfall är verifierade. Aktuell bolagstäckning visas separat. | Inte garanterad framtida betalningsförmåga eller kreditbedömning. |
| G4: Årsunderlag accepterat | Hela första året och tillämpligt bokslutsunderlag fungerar i granskarens arbetsflöde. | Inte automatiskt INK2/årsredovisning inlämnad. |
| G5: Ny period verifierad | En verklig ny period klarar normalt arbete utan specialkorrigeringar i databasen och med en tydlig officiell källa. | Inte tillstånd att dubbelskriva eller dubbelinlämna. |
| G6: Övergång godkänd | Omfattning, drift, arkiv, export, återställning och externa skyldigheter är hanterade. En skrivande källa aktiveras uttryckligen. | Inte generell certifiering av produkten. |
| G7: Extern pilot redo | Profilmatchning, tillåtna dataflöden, åtkomst, support och ärligt erbjudande finns. | Inte bevisad betalningsvilja eller bred marknadspassning. |

G1 och G2 kan avslutas före ett fullständigt eget årsredovisningssystem. G6 får bara avslutas när den verkliga ansvarsfördelningen för årsarbete och andra skyldigheter är fungerande. Extern granskare kan vara ansvarig för vissa slutprodukter, men det ska vara dokumenterat och praktiskt verifierat.

Varje godkännande ska ha krav-ID:n, exakt kodrevision, migrationsläge, miljö, dataperiod, källmanifest, genomförda steg, oberoende förväntningar, observerat resultat, granskare och kvarstående begränsningar. Senare ändring i en relevant beräknings- eller behörighetsgräns kräver ny riktad verifiering.

## 17. Mätning och kommersiell prövning

### 17.1 Huvudmått

**Primärt produktmått:** mänsklig aktiv arbetstid för att få en komplett, granskad period, inklusive rättningar och nödvändig support.

Mät samma definierade material och redovisningsomfattning före och efter. Väntan på underlag eller granskare ska registreras separat från aktiv arbetstid. En snabb period med fel ska aldrig vara en framgång.

| Mått | Definition | Krav eller hypotes |
|---|---|---|
| Kontrollutfall | Antal och summa oförklarade differenser inom verifierad omfattning. | Releasekrav: 0. |
| Dubbla ekonomiska effekter | Felaktigt extra bokföring eller betalningsbidrag efter återförsök/import. | Releasekrav: 0 i prövade fall. |
| Spårbarhet | Andel verifieringspliktiga ekonomiska bidrag med fungerande källa och beslutshistorik. | Releasekrav: 100 procent inom accepterad omfattning. |
| Aktiv periodtid | Arbetstid inklusive support och rättningar för samma material. | Hypotes: minst 30 procents förbättring efter en inlärningsperiod. Inte mätt. |
| Förberedelse utan faktarättning | Förslag som kan granskas utan ändrade indata dividerat med alla förberedda förslag. | Utforskande mått. Rapportera avvisade och ej stödda fall separat. |
| Tid till första avstämda period | Från att nödvändigt material är komplett till granskat resultat. | Baslinje etableras i Book Zero. |
| Självbetjäning | Prioriterade kundresor slutförda utan utvecklarhjälp. | Alla prioriterade resor före berörd acceptans. |
| Prognosfel | Skillnad mellan sparad prognos och kvalificerat faktiskt saldo vid samma horisont/kontomängd. | Mät efter 7 och 30 dagar; 90 dagar när utfallet finns. |
| Missade likviditetsproblem | Faktisk gränspassage som sparad tillräckligt täckt prognos inte visade. | Utred varje fall. Ingen påhittad träffsäkerhet före utfall. |
| Betalningsvilja | Externa pilotbolag som accepterar ett konkret pris för definierad omfattning. | Valideras, inte antas från användning. |

Prognosutvärdering ska skilja datumfel, beloppsfel, ny information efter prognosen och rena modellfel. Använd inte procentuellt saldo-fel som ensamt mått nära noll. Det kan ge missvisande slutsatser. Bevara de prognoser som faktiskt visades, även de dåliga.

### 17.2 Produkttelemetri

Föreslagna händelser: `source_import_completed`, `work_item_opened`, `proposal_prepared`, `proposal_revised`, `approval_recorded`, `execution_receipt_recovered`, `period_assessment_saved`, `review_pack_exported`, `forecast_saved`, `forecast_explained`, `scenario_saved` och `cutover_authorized`.

Ekonomiska auditposter är inte samma sak som produktanalys. Analys får använda pseudonyma objekt-/scope-ID:n, status och tidsmått men ska inte kopiera kvittotext, lönebelopp på individnivå eller fulla bankuppgifter till ett analysverktyg.

### 17.3 Extern pilot

Efter verifierad egen användning prövas produkten med 3 till 5 externa bolag inom samma stödda profil. Antalet är en föreslagen undersökningsomfattning, inte en förutsättning för att utveckla Cash. Varje bolag behöver sin egen käll- och profilkontroll.

En pilot får inte lovas ett komplett skatte-/lönesystem när den valda leveransen bygger på accepterad extern handoff. Onboarding, supportinsats, korrekthet och konkret betalningsvilja ska avgöra nästa expansion, inte enbart antal registrerade användare.

## 18. Risker och hantering

| Risk | Produktkonsekvens | Hantering |
|---|---|---|
| Fastna i generell funktionsparitet. | Ingen färdig kundresa trots mycket kod. | Prioritera Drastics verkliga familjer och definierade slutresultat. |
| Stale dokumentation tolkas som nuläge. | Dubbla implementationer eller felprioritering. | Ägarmappa mot aktuell kod och daterad bevisning före varje paket. |
| Gamla kontrollsiffror används utan original. | Ett historiskt fel blir ”facit”. | Oberoende kvalificering av underlag och kontrollförväntningar. |
| Tom kö förväxlas med färdig period. | Företagaren missar arbete. | Visa källa, aktualitet och periodkontroller separat. |
| Cash dubbelräknar betalningar. | Felaktigt likviditetsbeslut. | Ekonomisk identitet och AT-21 till AT-38. |
| Prognosen saknar framtida kostnader. | För optimistiskt utrymme. | Täckningskrav och uttryckliga återkommande åtaganden. |
| LLM blir sifferauktoritet. | Oförklarliga och inkonsekventa resultat. | Exakta domänberäkningar och källbundna förklaringar. |
| Testmiljö används som bolagsbevis. | För tidig driftsättning. | Separata gates för kod, faktisk period och externa utfall. |
| Uppsägt abonnemang förstör åtkomst. | Arkiv och granskning kan inte fortsätta. | Export-/återställningsprov och eget läsbart index före G6. |
| Parallell drift ger dubbel bokföring eller inlämning. | Felaktig officiell historik. | Explicit officiell källa och avstängda externa provåtgärder. |

## 19. Saknade indata och beslut som ska lösas vid rätt tidpunkt

| Fråga | Redan känd utgångspunkt | Vad som fortfarande ska finnas | Blockerar |
|---|---|---|---|
| Bolag och räkenskapsår | Drastic AB, första året 2025-05-17 till 2026-04-30 enligt tidigare uppgifter. | Kvalificerad profil i systemet, juridisk identitet och metodval. | Verklig bolagsacceptans. |
| Bank och källor | SEB och tidigare arbete med bolags-/privata underlag. | Exakta original, kontoperimeter, exportformat, fullständighet och användningstillstånd. | Verklig importkontroll och aktuellt Cash-läge. |
| Moms, skatt och redovisningsmetod | Inte fastställda av denna PRD. | Faktiska registreringar, perioder, metod och relevanta historiska deklarationer. | Berörd skatteberäkning och årsacceptans. |
| Lön, tillgångar och valutor | Tillämplighet ska avgöras av verkligt material. | Profil och underlag för varje faktisk familj. | Berörd behandling och fullständig likviditet. |
| Oberoende granskning | Extern redovisningskunnig ska kunna verifiera. | Utsedd granskare, mottagande program och godkännandets omfattning. | G1/G4 och övergångens ansvarsfördelning. |
| Produktionsidentitet | Befintlig auth-arkitektur behålls. | Verkliga användare, bokrättigheter och driftkonfiguration. | Exponering av verkliga bolagsuppgifter. |
| Arkiv och drift | Befintlig stack behålls. | Lagringsplats, retention, nycklar, återställningsmål och ansvarig. | Faktiskt arkiv och G6. |
| Direkta anslutningar | Inte nödvändiga för filbaserad första verifiering. | Godkända avtal, scope, credentials och leverantörsutslag när anslutning väl används. | Endast den anslutna handlingen och dess påstådda stöd. |

Dessa frågor ska knytas till D-01 till D-10 där de redan hör hemma. De är inte en anledning att starta om arkitekturarbetet eller att stoppa alla oberoende implementationer. [R07]

## 20. Definition av färdig leverans

Leveransen är färdig för den avtalade första omfattningen när:

**Book Zero:** en verklig period har oberoende kontroller och kan granskas utan specialkod. Årsutökningen ger ett accepterat underlag för hela första räkenskapsåret och lämnar tillämpliga externa skyldigheter hos en dokumenterad ägare.

**Vardagsprodukten:** företagaren kan upptäcka, förstå och slutföra prioriterat arbete i vanliga gränssnittet. Tillstånd, godkännande och återförsök är sanningsenliga. Ingen central resa behöver databaspatchning.

**Cash:** den valda bolagsprofilens betalningar räknas exakt en gång, lägsta likviditet beräknas över tid och osäkerhet samt täckningsluckor visas. Gamla prognoser och scenarier går att återöppna med sina ursprungliga indata.

**Övergången:** uppsägning av tidigare system sker först när arkiv, export, återställning och den officiella skrivande källan har verifierats och godkänts separat.

En godkänd PRD, en lyckad build, ett stort antal verktyg, en snygg skärmbild eller många syntetiska assertioner ersätter inget av dessa resultat.

---

## Källregister och versionsgrund

Källhänvisningar i dokumentet stödjer observerat nuläge och externa sakuppgifter. De nya kravens exakta produktval, exempel, mål och leveransordning är designförslag i denna PRD.

### Repository

Alla nedanstående repohänvisningar avser `erik-kroon/openERP` vid `41410fd75e96361b7c2f407d456019500f39bfbe`. Sökresultat från andra revisioner ska inte användas för att påstå att en funktion saknas vid denna revision.

| Källa | Sökväg/observation | Användning |
|---|---|---|
| R01 | GitHub `branches/main`, läst 2026-09-27. | Fixerar granskningsrevisionen. |
| R02 | `AGENTS.md`, ägarskap, dataregler, gränssnitt och kvalitetsregler. | Arkitektur, gemensamma kontrakt, rollgränser och faktisk testbehörighet. |
| R03 | `apps/web/src/lib/company-work.ts`. | Befintlig komposition av bank, öppna fakturor och uppgifter. |
| R04 | `docs/frontend.md`. | Kundresor, accepterad UX-riktning och kvarstående begränsningar. |
| R05 | `docs/plans/evidence/application-owned-replacement-complete.md`, daterad 2026-09-26. | Rapporterad lokal bevisning, inte egen reproduktion eller bolagsgodkännande. |
| R06 | `docs/roadmap.md`, avsnitt om faser och exit gates. | P2 till P7 och åtskillnaden mellan implementation och faktisk acceptans. |
| R07 | `docs/open-decisions.md`. | D-01 till D-10 samt company/provider/rule-gränser. |
| R08 | `docs/specs/next-26-50/packets/NEXT-45.md`. | Historisk kassaflödesrapport är separat från prognos. |

Repo-URL: `https://github.com/erik-kroon/openERP`

Länkmönster för versionsbundna dokument: `https://github.com/erik-kroon/openERP/blob/41410fd75e96361b7c2f407d456019500f39bfbe/<sökväg>`

### Externa primärkällor

**E01: Bokföringsnämnden, frågor och svar om arkivering.** Kontrollerad 2026-09-27. Stöd för den generella regeln att räkenskapsinformation ska sparas sju år efter det kalenderår då räkenskapsåret avslutades. Den källan ensam godkänner inte en viss molnregion, ett visst arkivformat eller alla bolagsspecifika bevarandekrav.

`https://www.bfn.se/fragor-och-svar/arkivering/`

**E02: Skatteverket, Skattekonto: betala och få tillbaka.** Kontrollerad 2026-09-27, avsnitt ”Ingen avräkningsordning”. Stöd för att en inbetalning inte kan vara avsedd för en viss enskild skatt eller avgift. Cashs finansieringsmodell är ett separat produktförslag som ska verifieras mot bolagets verkliga positioner.

`https://www.skatteverket.se/foretag/skatterochavdrag/skattekontobetalaochfatillbaka.4.6a6688231259309ff1f800029122.html`

Den här PRD:n gör inga uttömmande påståenden om skattesatser, K2/K3-tillämplighet, SIE-versioners alla detaljer, deklarationsschema eller regulatorisk klassificering av framtida finansiella tjänster. Sådana val ska kvalificeras under befintliga godkännandekrav under D-04/D-08/D-10 innan berörd verklig funktion accepteras.
