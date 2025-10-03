#### Ovaj file ću koristit za pisanje bilješki i zapažanja kad krenen detaljnije istraživat materiju i čitat resources koje iman

Neuromorphic Electronic Systems, Carver Mead, 1990
- https://hasler.ece.gatech.edu/Published_papers/Technology_overview/MeadNeuro1990.pdf

- Potrošnja energije je velik problem kod računala
- Obična računala ne mogu imitirati mozak, pa ni njegove najjednostavnije procese
- Mozak je i 10 milijuna puta efikasniji nego računala iz 90-ih
- Funkcije u mozgu se mogu djeliti na: jednostavne elementarne funkcije, reprezentacije informacija i najkompleksnije organizacijske principe 
- Ideja je pokušati reverse-engineerati mozak
- Kompleksno je rastavljati fizikalne principe u bitove i onda ih rekreirati s AND i OR gatesima
- Mozak se može gledati kao distribuirani sustav s više nodesa koji primaju električne impulse
- Sigurno se radi o nelinearnim funkcijama
- Napon u sinapsama neurona za osnovne funkcije raste eskponencijalno s naponom
- Mozak ima i sustave za dugotrajno učenje i memoriju
- Dobro izgrađen sustav može simulirati učenje i pamćenje (silicon chips)
- Neuromorphic sustavi su sustavi koji implementiraju iste operacija poput živčanog sustava
- Zero-cost addition using Kirchhoff's Law => ISTRAŽIT ČA JE TO
- Zjenica oka se, pri direktom osvjetljenju čini svjetlijom/tamnijom u odnosu na okolinu, ovisno o okolini
- Zjenica stvara napon po primitku inputa (svjetlosti)
- Računa se prosjek prostorno weighted inputa (ne vrijedi svaki input jednako, ovisno o poziciji)
- Cilj je napraviti senzor sličan oku koji može reagirati na sve inpute, neovisno od kud dolaze i koji im je intenzitet (zato se koriste weightovi)
- Koriste se amplifieri kako bi se bolje simulirao pravi potencijal živčanog sustava
- Laplacian filter => ISTRAŽIT MALO DETALJNIJE
- Pomaže u lokalizaciji objekata (odredimo di su u prostoru pomoću edge detectiona)
- Bitno je napravit da se broj kalkulacija u oku/mozgu prilagodi broju vanjskih evenata (MOZAK NE PROCESIRA ISTU KOLIČINU PODATAKA AKO GLEDA U BIJELI ZID I AKO -GLEDA U NEŠTO POKRETNO I DINAMIČNO) => dali je to maybe event-based princip??
- Cilj: više kalkulacija za više evenata; manje kalkulacija za manje evenata
- Važnost napona pojedinog eventa slabi s protokom vremena i dolaskom novih evenata
- Ni jedan senzor u oku i mozgu nije 100% isti kao neki drugi i zato koriste adaptivne mehanizme da kompenziraju manjak preciznosti
- U mraku zjenica ne mora niš procesirat jer ne vidi niš
- Uzima se input. Radi se predikcija inputa (ča mozak misli da vidi). Ako je ok, ne dela nikakav dodatan tuning. Ako pogriješi, mora opet kalkulirat i malo prilagodit parametre (primjer: zjenice se šire u tami da bolje vidimo)
- Isti princip je i za situaciju: nešto gledamo i delamo predikciju ča će se desit. Ako pogriješimo, radi se tuning, ako pogodimo, sve je ok
- Adaptation feedback
- Mozak računa average od svih viđenih piksela da se bolje adaptira i da vidi bitno, a izbacuje nebitno
- Problem simuliranog mozga pomoću čipova: ako 1 čip crkne, sve zgori. Stvara se jako puno topline i troši se puno energije
- Naš mozak nije u potpunosti spojen (x nodeova spojeno sa x nodeova, nego su spojeni lokalno i onda se to nadoveže, ali ne svaki sa svakin, jer bi to zauzimalo previše mista)
- Lokalno spajanje je ključno za efikasnost
- Ako imamo nepravilne inpute, treba nam neuromorphic computing 
- I do 10x efikasnije u performansama + 10000 x manje power consumptiona


 A 128x128 120 db 15 µs Latency Asynchronous Temporal Contrast Vision Sensor, Patrick Lichsteiner, Cristopher Posch, Tobi Debruck
- https://www.ifi.uzh.ch/dam/jcr:18928364-d16b-4403-9217-2098aaad72bd/lichtsteiner_dvs_jssc08.pdf
- 128x128 pikselni CMOS vision senzor
- Svaki piksel zasebno i kontinuirano generira spike evente na temelju lokalnih promjena intenziteta
- brži od milisekunde
- "mrežnica od silcija"

- PROS and CONS FRAME BASED VISIONA
- PROS: mali i jednostavni pikseli -> visoka rezolucija
                                   -> viskok fill factor i nizak imager cost (istražit dodatno)
- CONS: - baziran na serijama snapshota -> pikseli se ponovno obrađuju čak i ako su nepromijenjeni iz framea u frame -> JAKO BITNO
        - limitirani bandwith (FRAME RATE/2)
        - limitirani dynamic range (ograničen broj piksela po frameu)

IDEJA: senzor koji prati promjene inteziteta u okolini i pretvara ih u asinkrone promjene piksela
output: asinkroni stream pixel address evenata (AEs) => smanjuje se redundantnost (ignoriramo nepromijenjene piksele)
imitiranje biološkog vida i odbacivanje frame-based principa

KONCEPT ADDRESS-EVENT: svaki piksel dobije svoju koordinatnu adresu (lokalni array)
                       kontinuirano; slično kao moždani impulsi
                       jako high speed

PROBLEM S PROTOTIPOVIMA: uopće ne smanjuju redundantnost podataka, nego samo prostornu redundantnost
- puno noisea
- spori response
- limitirani dynamic range
- mala osjetljivost na kontrast

POLJE JE BILO NERAZVIJENO ZBOG NEZNANJA O ASINKRONOSTI I ZBOG BEZNAČAJNE UNIFORMNOSTI RESPONZIVNIH KARAKTERISTIKA PIKSELA

1) AER senzor -> MAHOWALD I MEAD
   - silikonska mrežnica s adaptivnim fotoreceptorima, spatial smoothing mrežom i self-timed komunikacijom
   DEMO UREĐAJ BEZ IKAKVE REAL-WORLD PRIMJENE

2) Spatial+temporal filtering -> ZAGHOUL I BOAHEN
   - puno malih tranzistora i el. krugova usko spojenih diffusor networksima
   - veliki mismatch -> GOTOVO 50% PIKSELA NE OSTVARUJE SPIKE

3) CSEM NEUCHATEL -> ostvaren spatial kontekst -> transisija evenata high-low
  - moguće zaustaviti ranije
  - ne smanjuje redundantnost, ograničena rezolucija zbog frame ratea

4) CULURCIELLO-ANDREON -> inter-event interval / mean frequency
   (+) - mala količina piksela
   (-) - bandwith ovisi o osvjetljenju
   nema reset mehanizma (puno tamnih piskela)

5) ETIENNE-CUMMING
   - temporal change detection imager
   - može detektirati apsolutnu promjenu osvjetljenja
   - sinkrono -> FIFO pristup
  
VISION SENSOR DESIGN
a) PIXEL DESIGN
 - cilj je: minimizacija mismatcheva
 - široki dynamic range
 - low latency
BRZI LOGARITAMSKI PHOTORECEPTOR CIRCUIT -> pojačava promjene
- kontrolira pojedine piksele + brzo odgovara/reagira na promjene osvjetljenja
- mana: tranzistori uzrokuju mismatch među pikselima zbog varijacija u thresholdu
- potrebna je dodatna kalibracija
KALIBRACIJA : balansiranje outputa na reset level nakon generiranja eventa (nekon ča se zabilježi event, senzor se resetira => fadeout u onima mojima testnima kodovima...)
!differencing circuit! -> pikseli su osjetljivi na temporal contrast -> ima formula u paperu; bitno

RECEPTOR CIRCUIT SADRŽI: fotodiodu, tranzistor, amplifier -> "TRANSIMPEDANCE CONFIGURATION" -> logaritamska pretvorba photocurrenta u NAPON

Povećan bandwith -> veća brzina
adaptive biasing -> znatno manja potrošnja energije
reset switch -> OKIDA input i output zajedno i tako resetira napon

OVO OPISUJE ONAJ PROCES KADA SE EVENT POJAVI NA KAMERI I ONDA SAMO IZBLJEDI I RESETIRA SE

ON i OFF eventi -> circuit ih emitira u periferiju
Pixel more emitat ili ON ili OFF event (NIKAD OBA ISTOVREMENO) prema periferiji
Proces "komunikacije" kreće kad event trigerira piksel, a završava kada se piksel resetira na 0 (vrati u početno stanje)
Prijevod na glupo: ON event -> nešto se miče i pikseli reagiraju; OFF event -> niš se više ne miče, pikseli miruju

ograničava se "fire-rate" za piksele kako pojedini pikseli ne bi zauzeli sve resurse za obradu
omogućava da se više resursa posveti aktivnijim područjima (procesiraš ono di se nešto dešava; di ima evenata)
Cilj je da se circuit ne pregrijava pretjerano, da ne troši resurse nepotrebno, da radi samo kad se nešto događa

KARAKTERISTIKE NAJVAŽNIJIH ASPEKATA:

Uniformity of response - vraća razliku u osvjetljenju piksela -> bitno je uniformno i standardizirano evaluirati promjene
Dynamic range - razlika imzeđu maksimalnog i minimalnog osvjetljenja u "sceni" kroz piksele; reliable and reproducible events
Pixel bandwith - iznos raspona jačine najjačeg i najslabijeg intenziteta koji 1 piksel "prepozna"/"odradi". Stariji i noviji eventi se razlikuju u intenzitetu; intenzitet opada protokom vremena (fade-out)
Latency&Latency jitter - ideja: ča je osvjetljenje manje, latencija je veća => proporcionalna recipročnom osvjetljenju (ča je škurije, teže se skuže eventi i promjene u svjetlosti kod piksela)
Utvrđeno je kako je latencija ipak jako mala u svim uvjetima (SUPER ZA REAL-TIME PROCESSING)


### Synaptic modifications in cultured hippocampal neurons:
### Dependence on spike timing, synaptic strength and postsynaptic cell type
### Guo-qiang Bi&Mu-ming Poo

Eksperimenti rađeni na hipokampusnim neuronima štakora
Postsinaptički i presinaptički neuroni

Presinaptički neuron = onaj koji šalje signal.

Njegov akson završava na sinapsi i otpušta neurotransmitere (npr. glutamat).

To je “pošiljatelj poruke”.

Postsinaptički neuron = onaj koji prima signal.

Na svojim dendritima ima receptore koji hvataju neurotransmitere i reagira (može spajkati ako se dovoljno pobudi). => procesira nešto samo ako dobije dovoljno inputa i skuži da se nešto desilo

To je “primatelj poruke”.

Spike neurona => registrira dovoljno ulaznih signala i pređe threshold aktivacije => ako je input dovoljno "jak", aktivira se spike
Okine strujni električni impuls (par milisekundi) i otpušta neurotransmitere

U kontekstu event based visiona => spike je event
Nema stalnih signala kao kod običnih CNN-ova nego samo triger kad se dogodi dovoljno jaka promjena
Troši se energija samo kada se nešto stvarno događa
Spike => kratki električni event kojim neuron javlja da je aktivan
Npr. Ako se detektira dovoljno pokreta, onda se input procesira, a ako ima malo/niš pokreta, ne procesiramo niš

LTP i LTD = dugotrajno jačanje ili slabljenje sinapsi, inducirano ponavljanom električnom aktivnošću.

Klasični protokoli: obično uključuju repetitivnu presinaptičku stimulaciju (razne frekvencije) + često dodatnu depolarizaciju postsinaptičkog neurona.

U nekim eksperimentima trebalo je blokirati spontane spikeove (npr. tetrodotoksin) ili smanjiti Mg²⁺ da bi LTP uspio.

Novija istraživanja (in vitro slices) pokazala su da precizno tempirani back-propagating action potentials (postsynaptic spike koji se vraća kroz dendrite) mogu inducirati LTP ili LTD.

Ključna nova ideja: nije samo važna frekvencija stimulacije → relativno vrijeme između presinaptičkog i postsinaptičkog spikea odlučuje smjer plastičnosti.
Ni bitno koliko je 1 event jak, nego je za spike bitno da se dešava više evenata u kratkom vremenu

Rezultati ove studije:

Postsinaptički spike <20 ms nakon presinaptičkog → LTP.

Postsinaptički spike <20 ms prije presinaptičkog → LTD.

Postoji uska prijelazna zona od samo ~5 ms između LTP i LTD.

Ovisnost o početnoj snazi sinapse:

Slabe sinapse = visoka šansa za LTP.

Jake sinapse = manje podložne daljnjem jačanju.

Specifičnost ciljne stanice:

Glutamatergičke sinapse na GABA neurone ne pokazuju ovu vrstu plastičnosti.

Implicira target cell–specific mehanizme.


---

* **LTP i LTD** = dugotrajno jačanje ili slabljenje sinapsi, inducirano ponavljanom električnom aktivnošću.
* **Klasični protokoli**: obično uključuju **repetitivnu presinaptičku stimulaciju** (razne frekvencije) + često dodatnu depolarizaciju postsinaptičkog neurona.

  * U nekim eksperimentima trebalo je blokirati spontane spikeove (npr. tetrodotoksin) ili smanjiti Mg²⁺ da bi LTP uspio.
* **Novija istraživanja (in vitro slices)** pokazala su da **precizno tempirani back-propagating action potentials** (postsynaptic spike koji se vraća kroz dendrite) mogu inducirati LTP ili LTD.
* **Ključna nova ideja**: nije samo važna frekvencija stimulacije → **relativno vrijeme između presinaptičkog i postsinaptičkog spikea odlučuje smjer plastičnosti**.
* **Rezultati ove studije**:

  * Postsinaptički spike **<20 ms nakon** presinaptičkog → **LTP**.
  * Postsinaptički spike **<20 ms prije** presinaptičkog → **LTD**.
  * Postoji uska prijelazna zona od samo **~5 ms** između LTP i LTD.
* **Ovisnost o početnoj snazi sinapse**:

  * **Slabe sinapse** = visoka šansa za LTP.
  * Jake sinapse = manje podložne daljnjem jačanju.
* **Specifičnost ciljne stanice**:

  * Glutamatergičke sinapse na **GABA neurone** ne pokazuju ovu vrstu plastičnosti.
  * Implicira **target cell–specific mehanizme**.

STDP je biološki mehanizam učenja kojim se jačina veze (sinaptička težina) između dva neurona mijenja ovisno o vremenskom razmaku između njihovih spikeova (akcijskih potencijala).

Drugim riječima:
Nije samo važno da neuroni spajkaju zajedno, nego točno kada to rade.

Pravilo (u osnovnoj formi):

Presinaptički neuron spajka PRVI → Postsinaptički ubrzo nakon (do ~20 ms)

LTP (Long-Term Potentiation): sinapsa se ojača.

Značenje: presinaptički neuron je vjerojatno pridonio aktivaciji postsinaptičkog – mozak to “nagradi” jačanjem veze.

Postsinaptički neuron spajka PRVI → Presinaptički tek kasnije (do ~20 ms)

LTD (Long-Term Depression): sinapsa se oslabi.

Značenje: presinaptički neuron nije uzrokovao aktivaciju postsinaptičkog, pa mozak smatra da je ta veza nebitna.

Ako su spikeovi previše udaljeni u vremenu (> ~20 ms)

 Nema promjene – mozak zaključuje da nema uzročno-posljedične veze.
 
 U mozgu (STDP):

Ako presinaptički spike dođe, i postsinaptički spike se dogodi ubrzo nakon → mozak zaključi da ovaj input uzrokuje ovaj output.

Rezultat = ojačaj tu sinapsu (nauči asocijaciju).

Ako je obrnuto (postsinaptički prije presinaptičkog) → veza se smatra nebitnom → oslabi sinapsu.

Analogija s event-based kamerom:

Ako se u kratkom vremenu i prostoru javi više evenata → sustav zaključuje da pripadaju istoj stvari (npr. kretanje osobe).

Ako eventi dolaze previše razdvojeni u vremenu/prostoru → nisu povezani, ignoriraš ih.

1. “Postsinaptički spike slijedi EPSP unutar ~15 ms → LTP”

EPSP (Excitatory Post-Synaptic Potential) = mali električni signal u postsinaptičkom neuronu, nastao kad presinaptički neuron otpusti glutamat.

Ako taj EPSP uspije “pogurati” postsinaptički neuron do praga i on okine spike vrlo brzo nakon toga (~15 ms) → mozak zaključi:

“Ovaj presinaptički input je doprinos postsinaptičkoj aktivaciji.”

Rezultat: ojačaj tu sinapsu (LTP).

To je zapravo biološki dokaz Hebbove ideje: neuroni koji spajkaju zajedno, povezuju se zajedno, ali uz precizan timing.

2. “I slabe i jake sinapse mogu se ojačati ako je spike timing pozitivno koreliran”

“Slaba sinapsa” = EPSP sam po sebi nije dovoljan da izazove spike u postsinaptičkom neuronu.

“Jaka sinapsa” = EPSP dovoljno velik da sam digne neuron do spikea.

Pokus pokazao: i slabe i jake veze se mogu ojačati, ako se pobrineš da postsinaptički spike padne unutar tog prozora (npr. kod slabih sinapsi su ručno injektirali malu struju da potaknu spike nakon EPSP).

Zaključak: bitan je timing, a ne samo jačina veze.

“NMDA receptori su ključni”

NMDA receptor = poseban tip glutamatnog receptora koji je osjetljiv na napon i omogućuje ulazak Ca²⁺ iona u neuron.

Taj Ca²⁺ signal je “molekularni prekidač” koji pokreće plastičnost (LTP/LTD).

Kad su ih blokirali s lijekom D-AP5 → nije bilo LTP-a → dakle, bez NMDA nema učenja.

LTP (long-term potentiation) = trajno jačanje sinapse (povećava se vjerojatnost da će signal proći).

EPSP (excitatory postsynaptic potential) = mali "plusić" napona na postsinaptičkom neuronu, kao mini podražaj.

Evo paralela s event-based kamerom 

---

### U mozgu (neuroni):

* **Presinaptički spike** = dolazni signal → EPSP.
* **Postsinaptički spike** = izlaz neurona.
* **STDP / LTP** = ako ulazni event stigne malo prije nego neuron ispali, veza se jača.
* **NMDA receptor** = “gatekeeper” koji kaže: *event se računa samo ako su se ulaz i izlaz poklopili u vremenu*.

---

### U event-based kameri:

* **Pixel event** = presinaptički spike (svaki event je mala promjena → mini EPSP).
* **Kamera/algoritam detektira pokret** = postsinaptički spike (output).
* **STDP logika**:

  * Ako više pixela (ulaznih evenata) **u kratkom vremenu i prostoru** “okine” i to dovede do registriranog pokreta (output), sustav zaključi: *ti eventi su povezani, pojačaj im značaj*.
* **NMDA paralela** = kao filter koji ne pušta “random šum”, nego traži da se više evenata poklopi u pravom trenutku → tek onda priznaje da je stvarno detekcija.

---

 Ukratko:
U mozgu – sinapsa se jača ako ulaz brzo dovede do izlaza.
U kameri – grupa evenata se tretira kao značajan pokret samo ako se prostorno-vremenski poklope i generiraju detekciju.

---

Pozitivno korelirani spikeovi (pre → post, unutar ~20 ms)
→ rezultira LTP (ojačavanje sinapse).

Negativno korelirani spikeovi (post → pre, unutar ~20 ms)
→ rezultira LTD (slabljenje sinapse).

Prozor djelovanja (temporal window):

Potencijacija = post-sinaptički spike unutar +20 ms nakon EPSP.

Depresija = post-sinaptički spike unutar −20 ms prije EPSP.

Izvan ±40 ms = nema značajne promjene.

NMDA receptori su obavezni i za LTP i za LTD (bez njih nema sinaptičke plastičnosti).

Jačina početne sinapse utječe na plastičnost:

Slabe sinapse = lakše jačaju (LTP).

Jako jake sinapse = manje podložne daljnjem jačanju.

Tip postsinaptičkog neurona:

Glutamatergički = pokazuju STDP (LTP/LTD).

GABA neuroni = nema STDP efekta.

Uloga Ca²⁺ kanala:

L-type Ca²⁺ kanali pomažu kod LTP, ali nisu nužni.

Za LTD (depresiju) jesu nužni.

STDP je asimetričan:

Ako ulaz dođe prije izlaza → učenje = “ovo je korisno” (LTP).

Ako izlaz dođe prije ulaza → učenje = “ovo nije korisno” (LTD).
Sve to ovisi o NMDA receptorima, vremenskom prozoru (~±20 ms) i jačini same sinapse.

Ako se više evenata dogodi vrlo brzo jedan nakon drugog (unutar “STDP prozora” od ~20 ms), sustav ih tretira kao povezane.

Kao posljedica, postsynaptički spike je jači nego kada bi ti eventi došli pojedinačno i razdvojeni u vremenu.

Biološki mozak → pojačava sinapsu (LTP).

Event-based sustav → grupira događaje i “pojačava signal”, što olakšava detekciju stvarnih objekata/pokreta.

Ok, ovo je sad super sažeto i profesionalno – ovo su **ključni zaključci cijelog rada**, izvučeni za tvoj event-based vision kontekst:

---

### Ključne točke / natuknice:

1. **STDP vremensko pravilo je vrlo precizno i usko**:

   * Potencijacija (LTP) se događa kada **postsynaptički spike slijedi EPSP unutar +20 ms**.
   * Depresija (LTD) se događa kada **postsynaptički spike prethodi EPSP unutar −20 ms**.
   * Izvan ±40 ms → nema značajne sinaptičke promjene.
   * Prelaz između LTP i LTD je **oštra, samo ~5 ms**.

2. **Jačina sinapse utječe na plastičnost**:

   * Slabe sinapse = lako potenciraju (LTP).
   * Jako jake sinapse = mogu biti “saturirane” i ne reagiraju više na pozitivno korelirane spikeove.

3. **Tip postsinaptičkog neurona je ključan**:

   * Glutamatergički neuroni → pokazuju LTP i LTD.
   * GABAergički neuroni → nema sinaptičke modifikacije (nije osjetljivo).

4. **NMDA receptori i Ca²⁺ su kritični**:

   * NMDA receptori → obavezni i za LTP i za LTD.
   * L-type Ca²⁺ kanali → potrebni za LTD, pomažu za LTP.
   * Lokalni Ca²⁺ spikeovi unutar dendrita omogućuju preciznu temporalnu detekciju.

5. **Temporalni slijed spikeova implementira Hebbovu logiku**:

   * Ako **ulaz (presynaptički spike) uzrokuje izlaz (postsynaptički spike)** → veza se jača (LTP).
   * Ako je redoslijed obrnut → veza se slabije aktivira (LTD).
   * Ovo je prirodni “causality detector” → neuronska mreža može učiti sekvence i predviđati događaje.

6. **Spontana aktivnost može “saturirati” sinapse** → starije sinapse u kulturi možda ne mogu dodatno potencirati.

7. **Implications for event-based systems:**

   * **Brzo slijedeći eventi → tretiraju se kao povezani → jači output**.
   * Sustavi poput spiking CNN-a mogu koristiti STDP logiku da detektiraju obrasce u vremenskim eventima i odluče što je relevantno.
   * Temporalna asimetrija omogućuje “prediktivno kodiranje” → slično onome što mozak radi kod navigacije i sekvencijalnog učenja.



A million spiking-neuron integrated circuit with a scalable communication network and interface
Paul A.Merolla&co.

- inspirirano strukturom mozga
- efikasna, skalabilna, fleksibilna, non-von Neumannova arhitektura
- suvremena silikonska tehnologija
- čip od 5.4 milijardi tranzistora s 4096 neurosinaptičkih jezgri međusobno povezanih preko intrachip networka
- network se sastoji od milijun programabilnih spiking neurona i 256 milijuna konigurabilnih sinapsi (sinapse su veze među neuronima; zato ima više sinapsi nego neurona jer veze nisu 1:1)
- čipovi se mogu povezati u 2 dimenzije pomoću interchip komunikacijskog interfacea -> skaliranje na razinu cortexlike sheeta proizvoljne veličine (cortex => vanjski dio mozga..."kora")
- omogućava korištenje kompleksnih neuronskih mreža u realnom vremenu (npr. multiobject detekcija i klasifikacija)
- 400 px x 240px video input brzine 30 fps-a na čipu troši 63 miliwatta
Chatgpt:
Da, ako to stavimo u perspektivu, ovo je **prilično efikasno**, pogotovo za embedded ili edge AI čipove. Hajde da to raščlanimo:

* Video ulaz: **400 × 240 px** → 96.000 piksela po okviru.
* Brzina: **30 fps** → 2.880.000 piksela obrađeno u sekundi.
* Potrošnja: **63 mW** → 0,063 J po sekundi.

Ako računamo **energiju po pikselu**:

E_per_pixel = 0.063 / (400 * 240 * 30) = 21.875e-9 J = 21.875 nJ/pixel

Za usporedbu, moderni edge AI čipovi (npr. za male kamere ili IoT senzore) često ciljaju **10–100 nJ/piksel** za video obrade pri visokoj efikasnosti.

Zaključak: **63 mW za 400×240 @ 30 fps je vrlo dobar rezultat**. Ovo je tipično u rangu ultra-low-power AI kamera čipova.

Cilj je stvoriti višenamjenski kompjuter efikasan u vidu prostora i potrošnje resursa, skalabilan za velike neuronske mreže i sinapse, dovoljno fleksibilan da odrađuje bihevioralne modele cortexa mozga

Takva računala 2014. nisu postojalaa

Von Neumannova arhitektura je neefikasna i neskalabilna te ne može kvalitetno reprezentirati masivne, međusobno povezane neuronske mreže
Koristi se miks analognih i digitalnih neuromorfnih signala => imitacija neurobioloških procesa korištenjem:
- silicijskih neurona
- winner-take-all strujnih krugova (pogledat detaljnije)
- senzorskih strujnih krugova

- Digitalno implementirani spiking neuroni su efikasniji od svih dosadašnjih dizajna
- omogućavaju one-to-one correspondence između softvera i hardvera => Ča znači one-to-one?
Svaka funkcija softvera (npr. određeni algoritam, neuronski sloj, procesiranje piksela) ima direktno odgovarajući hardverski resurs koji ju izvršava.
Nema posrednog sloja ili generičkog procesora koji simulira funkciju — hardware je dizajniran točno za tu operaciju.

- stvoreni su event driven komunikacijski frameworkovi => komunikacija se dešava samo kad se dogodi event
- na taj način se emulira unutarnja povezanost unutar mozga

Colocated memory and computation + event driven communication nadilazi von Neumann bottleneck

Colocated memory and computation + event driven communication nadilazi von Neumann bottleneck

Von Neumann bottleneck

* Klasična arhitektura računala (CPU + RAM) ima **odvojen procesor i memoriju**.
* Podaci i instrukcije se stalno šalju između memorije i CPU-a preko **jedne sabirnice**.
* **Problem:** sabirnica je usko grlo → CPU često čeka podatke iz memorije → sporije i manje energetski efikasno.
* To je tzv. **von Neumann bottleneck**.

Colocated memory and computation

* “Colocated” znači da **memorija i procesiranje stoje zajedno**, na istom čipu ili blizu.
* Prednost: podatke **ne treba stalno pomjerati preko sabirnice** → manje čekanja, manja potrošnja energije.
* Primjer: **neuromorfni čipovi**, gdje svaki “neuronski element” ima svoje “local memory” i logiku za izračun.


Event-driven communication

* Sustav **reagira samo kad se dogodi event** (npr. piksel se promijeni).
* Za razliku od stalnog pollanja, **samo se šalju podaci koji su relevantni**.
* Prednost: još manja potrošnja i brži prijenos informacija.


Zaključak

* Kombinacija **lokalne memorije + event-driven komunikacije** znači:

  * Nema stalnog čekanja na podatke između procesora i memorije.
  * Podaci se šalju **samo kad je potrebno**.
* Dakle, sustav **nadilazi von Neumann bottleneck** → brže, efikasnije, manje energije troši, posebno kod neuromorfnih i edge AI sustava.

Ključna arhitektura => mreža neurosinaptičkih jezgri koja može izgraditi velike spiking neural networke koji su efikasni, skalabilni i fleksibilni

Osnovna građevna jedinica je "core" -> samostojeća neuronska mreža s 256 inputa (aksona) i 256 outputa (neurona) povezanih preko 256x256 usmjerenih, programabilnih sinaptičkih veza
Od više coreva mogu se graditi složenije mreže pomoću globalne, distribuirane on- and off-chip povezivosti
Svaki neuron na svakom coreu može se povezati s bilo koji aksonom na bilo kojem drugom coreu (jako dobra povezanost više neuronskih mreža)

Aksionski branching je implementiran hijerarhijski u 2 stadija:

Najprije 1 konekcija putuje od starta (prvog corea) skoro do cilja (drugog corea), ali se po dolasku do aksona razdvaja u puno manjih konekcija koje prolaze još kratku udaljenost unutar samog corea

Neuroni se kreću u stepsima od 1ms (orkestrirano pomoću globalnog 1-kHz clocka)

Uz opisani globalni sinkronizacijski clock (koji osigurava 1-1 konekciju softvera i hardvera), coresi koriste i paralelni  i event driven način rada
Osnovni napon upravlja potpuno asiknronom intercore komunikacijom i event-driven intracore komunikacijom. Taj napon radi po principu all-or-nothing spike evenata koji predstavljaju aktivaciju pojednih neurona

Efikasno zato jer se neuroni klasteriraju u klastere koji izvlače svoje inpute iz sličnih poolova aksona (neuroni se grupiraju prema aksonima)
Samo spike eventi se šalju komunikacijom između jezgri . Što su eventi jači, to se češće šalju

Ta je arhitektura skalabilna jer jezgre na čipu, kao i sami čipovi imaju mogućnsot slaganja u 2 dimenzije (slično kao cortex sisavaca)
Svaki spike event  cilja točno određeni "pool" neuorna na ciljanoj jezgri i tako smanjuje broj long-range spike evenata koji predstavljaju ključni bottleneck (event se ne šalje svuda nego točno određenim neuronima koji ga trebaju primiti)
Fault tolerance -> povremene greške u core-u i na čipovima ne oslabljuju rad cijelog sustava

Arhitektura je fleksibilna jer je svaki neuron individualno konfigurabilan i imitira prave neurone podržavajući razne funkcije i biološki relevantne spiking mehanike
Svaka sinapsa se može individualno "paliti i gasiti" i može joj se dodjeliti relativna snaga (slično kao weighted metrike)
Svaka neuron-axon veza je programabilna s uključenim axonal delayom
Neuroni i sinapse mogu prikazivati programirano stohastičko (nasumično, ali s predvidivim obrascem) ponašanje korsteći pseudo-random number generator (1 po jezgri)
Arhitektura podržava imitaciju psihološke dinaimke i anatomske povezanosti.
Ima: feed-forward, reccurent i lateral veze

---

### **1️. Feed-forward veze**

* Informacija ide **jednosmjerno od ulaza prema izlazu**.
* Nema povratnih veza → signal ne vraća se unatrag.
* Tipično u **klasičnim perceptronima i CNN-ovima**.
* Prednost: jednostavno, stabilno, brzo računanje.
* Mana: ne može modelirati vremenske sekvence ili stanje memorije.

---

### **2️. Recurrent veze**

* Informacija se **vraća unatrag unutar mreže** → stvaraju **petlje**.
* Omogućuju mreži da **pamti prethodne ulaze** → modeliranje sekvenci, npr. tekst, govor, vremenske serije.
* Primjeri: RNN, LSTM, GRU.
* Mana: teže trenirati (problem “exploding/vanishing gradients”).

---

### **3️. Lateral veze**

* Veze **između neurona unutar istog sloja**.
* Omogućuju **modulaciju aktivnosti susjednih neurona**, konkurenciju ili potporu.
* Tipično u **biološkim mrežama** → lateralna inhibicija pomaže kod detekcije rubova, kontrasta, itd.
* U umjetnim mrežama rjeđe, ali se koristi za **attention, normalizaciju ili interneuron modulaciju**.

---

Core ima individualno adressable aksone, konfigurabilni synaptic crossbar array i programabilne neurone

Core (u neuromorfnom čipu)

Individualno addressable aksone

Svaki aksone (put kojim ide signal od neurona) može se posebno adresirati i kontrolirati.

Znači možeš poslati signal točno određenom neuronu ili grupi neurona, bez da utječeš na ostatak mreže.

Konfigurabilni synaptic crossbar array

Mreža sinapsi (kao matrica) gdje možeš konfigurirati težine veze između neurona.

Omogućuje da jedan neuron šalje signal više neurona s različitim jačinama → ključno za učenje i prilagodbu.

Programabilni neuroni

Neuroni čipa se mogu programirati: npr. prag aktivacije, dinamiku spike-a, reakciju na inpute.

To omogućuje simulaciju različitih tipova bioloških neurona i različitih algoritama unutar istog hardwarea.

Ukratko:

Aksone = kontrola kamo signal ide

Crossbar = kontrola koliko je signal jak između neurona

Programabilni neuroni = kontrola kako neuron reagira na signal

Unutar corea informacija teče od presinaptičkih aksona kroz aktivne sinapse u crossbaru kako bi stvarala inpute za sve povezane postsynaptic neurone

Aksioni se aktiviraju pomoću input spike evenata koje generiraju neuroni bilo gdje u sustavu i šalju se dalje nakon definiranog axonal delaya (od 1 do 15 vremenskih jedinica)
Mozak ima dedicated "žicu" za svaku konekciju; čip ima time-multiplexed žice koje povezuju 2-d mesh network rutera
Svaki ruter ima 5 portova (sjeverni, južni, istočni, zapadni i lokalni)
Ruteri su osnova 2-d mesh networka koji povezuje 64x64 array coresa

Kada neuron u coreu spike-a, u lokalnoj memoriji traži axonal delay (4 bita) i adresu destinacije (8 bitova apsolutne adrese za target aksone i dvije 9-bitne relativne adrese koje predstavlaju core "skokove" u svakoj dimenziji ciljanog corea)
Te se informacije enkodiraju u paket koji se šalje pomoću mesha od corea do corea (prvo po x-u, pa po y-u) => takva je komunikacije deadlock free
Za implementaciju feedback veza u coreu, gdje se neuron spaja na akson isto corea, paket se dostavlja koristeći lokalne kanale rutera (efikasno jer se ne napušta core)
Za skaliranje opisanog sustava (2-d mesh) u kojem je broj interchip konekcija ograničen, koristi se merge-split struktura na 4 ruba mesha da bi se postojeći spikeovi serijalizirali, a izlazeći deserijalizirali. Svakom spikeu se da labela njegovog reda (ako putuje istok-zapad) ili stupca (ako putuje sjever-jug) prije nego se spoje u shared link koji postoji na čipu
Također, spikeovi koji ulaze na čip iz shared linka, razdvajaju se u odgovarajući redak ili stupac koristeći info sa tagova

Objašnjenje:

---

### 1️.Osnovni tok informacija unutar corea

* **Presinaptički aksone** šalju spike događaje kroz **aktivne sinapse u crossbar**.
* Crossbar distribuira signal prema **postsynaptičkim neuronima** unutar corea.
* **Input spike event** = signal od nekog neurona bilo gdje u sustavu.
* **Axonal delay** = vremensko kašnjenje prije nego spike stigne do target neurona (1–15 jedinica).

**Ukratko:** neuron spike-a → signal ide kroz aksone i sinapse → dolazi do drugih neurona, uz kašnjenje.

---

### 2️.Razlika između mozga i čipa

* **Mozak:** svaka veza ima svoju “žicu” → fizički dedicated.
* **Čip:** koristi **time-multiplexed žice** → jedna fizička veza prenosi spikeove od više neurona koristeći redoslijed i vrijeme.
* Spikeovi putuju kroz **2-d mesh network**: mreža rutera koji povezuju coreove u x i y dimenziji.

---

### 3️.Ruter i 2-d mesh network

* Svaki ruter ima **5 portova**: sjever, jug, istok, zapad, lokalni (core unutar kojeg se nalazi).
* Spike ide kroz mesh tako da prvo ide **po x osi, pa po y osi** → deadlock-free (nema zastoja u mreži).
* Mreža povezuje **64×64 corea**.

---

### 4️.Paket spike-a

* Kada neuron spike-a:

  * Traži se **axonal delay** (4 bita).
  * Traži se **adresa destinacije** (8-bit apsolutna + 2×9-bit relativne za target core).
  * Ove informacije se enkodiraju u **paket** i šalju kroz mesh.

* **Feedback veze unutar corea** → spike ostaje unutar corea, koristi lokalni kanal rutera → efikasno.

---

### 5️.Skaliranje i interchip komunikacija

* Problem: broj veza između čipova je ograničen.

* Rješenje: **merge-split struktura**:

  * Spikeovi se **serijaliziraju** prije slanja kroz shared link.
  * Na odredištu se **deserijaliziraju**.
  * Svakom spikeu se dodaje **labela reda (x)** ili **stupca (y)** → omogućuje pravilan routing.

* Spikeovi koji dolaze iz shared linka se **razdvajaju u odgovarajući redak/stupac** prema tagu.

---

###  Ukratko, što se događa

1. Neuron spike-a → lokalno traži delay i adresu.
2. Spike se enkodira u paket → ide kroz 2D mesh network rutera.
3. Ako je intra-core feedback → koristi lokalni kanal, nema routing po meshu.
4. Ako ide na drugi čip → spikeovi se serijaliziraju, šalju shared linkom, zatim deserializiraju i rasporede po target coreu.

**Cilj:**

* Efikasna, skalabilna, deadlock-free komunikacija između 64×64 coreova + interchip povezanost.
* Omogućuje **tisuće paralelnih spike događaja** da se prenesu brzo i precizno.

---

Implementacija: milijun spiking neurona i 256 milijuna sinapsi i 5.4 milijarde tranzistora na prostoru od 4.3 cm2
Ima 428 milijuna bitova on-chip memorije
Svaki core ima 104,448 bitova lokalne memorije za pohranu stanja sinapsi (65,536), stanja neurona i parametre (31,232), adrese destinacija (6656) i axonal delays (1024)
Energija: 20 mW po cm2, dok CPU troši 50-100 W po cm2
Active power density je nizak zbog arhitekture
Passive power density je nizak zbog tranzistora s malim leakegom

4096 puta više coreva na 15 puta manje površine, sa 100 puta manje potrošnje energije u odnosu na prethodna rješenja

Omogućava event driven asinkrono-sinkroni pristup => implementirano koristeći: offline learning (CNN, liquid state machines, restricted Boltzman machines, hidden Markov models, support vector machines, optical flow i multimodal classification)
Offline learning metode

CNN (Convolutional Neural Network)

Ekstrahira prostorne značajke iz slika/video koristeći konvolucijske filtere.

Liquid State Machines (LSM)

Vrsta recurrent spiking neural network; pamti kratkoročne temporalne obrasce → dobro za vremenske serije i neuromorfne spike podatke.

Restricted Boltzmann Machines (RBM)

Probabilistički model za učenje distribucija i reprezentacija podataka; često se koristi za feature extraction i pretreniravanje dubljih mreža.

Hidden Markov Models (HMM)

Model sekvencijalnih podataka gdje stanja nisu direktno vidljiva, ali generiraju opažene događaje → koristi se za govor, signale i vremenske serije.

Support Vector Machines (SVM)

Supervised learning metoda koja pronalazi optimalnu granicu između klasa u feature prostoru.

Optical Flow

Tehnika za praćenje kretanja objekata u video sekvencama prema promjeni intenziteta piksela kroz vrijeme.

Multimodal Classification

Kombinacija više tipova podataka (npr. video + audio + senzori) za preciznu klasifikaciju.
Čip vrti te iste algoritme bez da ih treba modificirati

Za dodatno testiranje, razvijena je i dodatna multiobject detekcija i klasifikacija s fiksnom kamerom
Zadaci: detekcija ljudi, auti, i ostalih vozila na slikama gdje se pojavljuju rijetko s ciljem minimizacije false detekcija (sustav spikea samo kad se nešto stvarno pojavi; ne troši eneriju bezveze)
Radi na 400x240 piksela. Čip je trošio 63 mW na 30-fps videu u 3 boje koji je zatim bio skaliran na 1920x1080. Bilo je potrebno konvertirati piksele u spike evente jer je video bio snimljen standarndom kamerom
dobre performanse

Moguće koristiti i spike-based retinal cameru
Implementirana je vizualna "mapa" orijentacijsko selektivnih filtera inspiriranih ranim procesiranjem u coretexu sisavaca koji se često koristi u CV za feature extraction

Svih milijun neurona dobilo je feedforward inpute s orientation biasima iz vizualnog prostora skupa s rekurzivnim konekcijama među bliskim featuresima

Standardni benchmark u arhitekturi računala je: energy per operation
U domeni konfigurabilnih neuralnih arhitektura, osnovna operacija je "sinaptički event" koji predstavlja source neuron koji šalje spike event target neuronu putem posebne (non-zero) sinapse
Sinaptički eventi su atomične jedinice mjerenja jer se količina računanja, memorija, komunikacija, snaga, površina i brzina proporcionalno povećavaju s brojem sinapsi

Koristeći rekurzivno poveane mreže, izmjeren je total power i energy per synaptic event
Power consumption  je funkcija spike rate-a, prosječne udaljenosti koju spikeovi prolaze i prosječnog broja aktivnih sinapsi po neuronu (synaptic density)

Ako je "fire" u prosjeku 20 hz uz 128 aktivnih sinapsi, ukupna izmjerena snaga iznosila je 72mW (na naponu od 0.775 V), što odgovara 26pj po sinaptičkom eventu

U usporedbi s standarnim računalom, troši se 176000 x manje energije po eventu
Omogućava se individualno programiranje neurona i njihovih konekcijama
SPOS -> sinaptičke operacije po sekundi u ovom sustavu
Standardna superračunala -> FLOPS (floating point operations per second)

Slaganjem više TrueNorth brainchipova, mogu nastati superračunala sa stotinama tisuća jezgri, stotinama milijuna neurona i stotinama milijardi sinapsi

Arhitektura -> slika -> svaki node je spojen sa svakim (node = core, edge = neural connection)
