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
- Zero-cost addition using Kirchhoff's Law

Kirchhoffov zakon (struja): u jednom čvoru zbroj svih struja koje ulaze = zbroj svih struja koje izlaze.

Ako više izvora struje spojiš na isti čvor → automatski se saberu (nema dodatnih komponenti).

Zero-cost addition = zbrajanje bez dodatnog sklopa → priroda elektronike sama radi računanje.

Kapacitet čvora (parazitski ili namjerni kondenzator) integrira ukupnu struju tijekom vremena → dobiješ napon koji predstavlja zbroj.

U digitalnim sklopovima bi ti za zbrajanje trebao adder (logika, tranzistori, energija).

U neuromorfnim sklopovima: samo spojiš sinaptičke struje na čvor i dobiješ sabiranje “besplatno”.

To je ultra-bitno jer neuron = integrator sinaptičkih ulaza → Kirchhoff + kapacitet daju ti točno tu funkcionalnost prirodno.

Mead je rekao: iskoristi fiziku (Kirchhoffov zakon) umjesto da je “nadograđuješ” kompleksnim digitalnim adderima.

👉 Ukratko: više sinapsi šalje spikeove kao struje → struje se automatski zbroje na membrani neurona → kondenzator integrira → izlaz = ponašanje biološkog neurona, i to praktički bez troška.

Evo kako ide “story” u neuromorfnom hardveru i u mozgu:

Više sinapsi šalje svoje “signale” (u elektronici kao struje, u mozgu kao ionski tokovi).

Te sve struje ulaze u jedan čvor (membrana neurona).

Po Kirchhoffovom zakonu → struje se automatski zbroje (ništa ne moraš posebno računati).

Kondenzator membrane integrira taj ukupni signal kroz vrijeme → to daje membranski potencijal.

Ako potencijal pređe određeni threshold → neuron ispali spike (akcijski potencijal).

👉 Ukratko: Neuron radi kao prirodni zbrajač + integrator.

Sabira ulaze (Kirchhoff).

Pamti ih kroz vrijeme (kapacitor = integracija).

Triggera izlaz kad sve skupa dosegne kritičnu vrijednost (threshold).

- Zjenica oka se, pri direktom osvjetljenju čini svjetlijom/tamnijom u odnosu na okolinu, ovisno o okolini
- Zjenica stvara napon po primitku inputa (svjetlosti)
- Računa se prosjek prostorno weighted inputa (ne vrijedi svaki input jednako, ovisno o poziciji)
- Cilj je napraviti senzor sličan oku koji može reagirati na sve inpute, neovisno od kud dolaze i koji im je intenzitet (zato se koriste weightovi)
- Koriste se amplifieri kako bi se bolje simulirao pravi potencijal živčanog sustava
- Laplacian filter => edge detction filter

Ajmeee, top što pitaš za Laplacian filter! 🔥 To ti je jedan od najpoznatijih **edge detection filtera** u računalnom vidu i obradi slika.

Evo ti jasno u natuknicama:

---

### 🔹 Što je Laplacian filter?

* **Matematički temelj:** koristi **Laplacian operator** (druga derivacija funkcije).
* **Poanta:** pronalazi mjesta gdje se intenzitet slike brzo mijenja → tj. rubove (*edges*).
* Za razliku od Sobel/Prewitt (koji koriste prvu derivaciju i detektiraju smjer ruba), Laplacian gleda **drugu derivaciju** → pa je osjetljiv na *naglu promjenu nagiba*.

---

### 🔹 Kako radi na slici?

* Sliku gleda kao **matricu piksela**.
* Na svaki piksel primjenjuje kernel (konvolucijsku masku) koji aproksimira Laplacian operator.
* Tipični kernel izgleda npr. ovako:
Laplacian filter kerneli:
```
0  -1   0
-1  4  -1
0  -1   0
```

i "jača" verzija:
```
-1  -1  -1
-1   8  -1
-1  -1  -1
```

* Kad se primijeni, filter daje visoke vrijednosti na mjestima gdje postoji jaka promjena intenziteta → tj. rub.

---

### 🔹 Zašto je koristan?

* Detektira rubove **neovisno o smjeru** (Sobel detektira horizontalne/vertikalne, Laplacian je “isotropic”).
* Jako dobar za **naglašavanje struktura** i **detekciju kontura**.
* Često se koristi nakon blura (npr. Gaussian blur + Laplacian = *Laplacian of Gaussian*, LoG) → to pomaže da se smanji šum.

---

### 🔹 Intuicija

* Ako piksel izgleda “sličan” susjedima → rezultat ≈ 0.
* Ako je piksel jako različit od susjeda → rezultat velik (pozitivan ili negativan) → to je rub.

---

👉 Ukratko: **Laplacian filter je edge detector baziran na drugoj derivaciji, hvata rubove u svim smjerovima i jako se koristi u računalnom vidu.**


PRIMJER PRIMJENE by ChatGPT:

Ajmo brutalno jednostavno da odmah sjedne 🔥

---

### 📌 Primjer matrice (mala “slika” 5×5 piksela)

Zamisli da imaš grayscale sliku, gdje su vrijednosti piksela:

```text
10  10  10  10  10
10  10 100  10  10
10  10 100  10  10
10  10 100  10  10
10  10  10  10  10
```

👉 To ti je slika gdje imaš **vertikalnu bijelu crtu** (100) na sredini crne pozadine (10).

---

### 📌 Laplacian kernel (klasični)

```text
0  -1   0
-1  4  -1
0  -1   0
```

---

### 📌 Primjena filtera (konvolucija)

1. Uzimamo kernel 3×3 i stavljamo ga iznad piksela u centru (recimo sredina je `100`).
2. Pomnožimo element po element i zbrojimo:

```
Kernel:          Dio slike:       Rezultat = sum(kernel * dio_slike)

 0  -1   0       10  100  10
-1   4  -1   *   10  100  10   =   (0*10) + (-1*100) + (0*10) +
 0  -1   0       10  100  10       (-1*10) + (4*100) + (-1*10) +
                                    (0*10) + (-1*100) + (0*10)

= -100 -10 +400 -10 -100
= 180
```

👉 Dakle u centru bijele crte izlazni piksel je **jako velik (180)** → filter ga označi kao rub.

3. Ako isti kernel stavimo na dio pozadine (gdje su sve vrijednosti 10):

```
 0  -1   0       10  10  10
-1   4  -1   *   10  10  10   = (0*10) + (-1*10) + (0*10) +
 0  -1   0       10  10  10      (-1*10) + (4*10) + (-1*10) +
                                  (0*10) + (-1*10) + (0*10)

= -10 -10 +40 -10 -10
= 0
```

👉 Rezultat = **0** → pozadina nema rub, pa filter ništa ne detektira.

---

### 📌 Zaključak

* Na rubu (gdje se vrijednost naglo mijenja) dobiješ **visok rezultat**.
* Na ravnom dijelu slike → rezultat ≈ **0**.

---

Primjenjuje se na cijelu sliku, dio po dio
Evo kako to ide u praksi:

Imaš cijelu sliku (npr. 512×512 piksela).

Uzmemo kernel (mala matrica, npr. 3×3 ili 5×5).

Kernel “klizi” po slici – piksel po piksel, red po red (to se zove konvolucija).

Za svaki položaj:

Uzmeš “komadić” slike iste veličine kao kernel.

Pomnožiš element po element (kernel × slika).

Zbrojiš sve rezultate → to je novi izlazni piksel u filtriranoj slici.

Rezultat cijelog procesa = nova slika gdje su naglašeni rubovi (ili što god kernel radi).

👉 Dakle, da, filter se primjenjuje na cijelu sliku, dio po dio, i rezultat je feature map (slika s naglašenim značajkama).

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
                                   -> viskok fill factor i nizak imager cost
---

### 🎯 **Fill Factor**

**Definicija:**
Fill factor = **udio površine piksela koji stvarno prima svjetlo** u odnosu na **ukupnu površinu piksela**.

Zamisli da svaki piksel ima određenu površinu (npr. 10×10 µm). Dio te površine zauzimaju fotodetektor i elektronički sklopovi (tranzistori, kondenzatori, žice...).
Samo **fotodetektor** (photo diode) zapravo skuplja svjetlo — i to je efektivna "korisna površina".

👉 Formula:
[
\text{Fill Factor} = \frac{\text{Površina osjetljiva na svjetlo}}{\text{Ukupna površina piksela}} \times 100%
]

---

**Primjer:**

* Ako je piksel 10×10 µm, ali samo 5×5 µm hvata svjetlo → fill factor = 25%.
* Ako se koristi **mikro-leće** koje fokusiraju svjetlo na aktivni dio → fill factor raste.

---

**Zašto je bitan:**

* **Veći fill factor = bolja osjetljivost na svjetlo (viši SNR)**
* **Manji fill factor = više šuma, lošiji kontrast u slabom svjetlu**

---

**U kontekstu frame-based senzora:**
Frame-based senzori imaju **jednostavnije piksele**, pa mogu imati **veći fill factor** i time hvataju više svjetla — to je njihov *PRO*.

**Kod DVS-a (event-based):**
Pikseli imaju više elektronike (detekcija promjene intenziteta, threshold komparator itd.) — pa često **fill factor pada**.
Zato se često dodaju **mikroleće** i posebni layouti da se fill factor poboljša.

---

### ⚡ **Imager Noise (šum senzora)**

**Definicija:**
To je **neželjena varijacija** u električnom signalu piksela koja **nije rezultat stvarne promjene svjetla**.

---

**Glavne vrste šuma u imagerima:**

1. **Photon shot noise** – dolazi od same prirode svjetlosti (nasumičan broj fotona).
2. **Thermal noise (Johnson noise)** – termičke fluktuacije u elektronici.
3. **Read noise** – šum koji nastaje pri čitanju signala s piksela (ADC, bufferi...).
4. **Fixed pattern noise (FPN)** – razlike između piksela zbog proizvodnog procesa.

---

**Zašto je bitan:**

* Visok šum → senzor ne može točno detektirati male promjene svjetla.
* Kod **DVS-a**, šum direktno utječe na točnost generiranja eventa —
  ako je noise previsok, senzor može “lažno” detektirati promjenu i emitirati spike event iako svjetlo nije stvarno promijenjeno.

---

**Balans kod DVS-a:**

* Ako se threshold za promjenu intenziteta postavi **prenisko**, šum će stvarati lažne evente.
* Ako se postavi **previsoko**, senzor će ignorirati male, ali bitne promjene u sceni.

---

### 🔍 Ukratko:

| Pojam            | Objašnjenje                                                               | Posljedica                              |
| ---------------- | ------------------------------------------------------------------------- | --------------------------------------- |
| **Fill Factor**  | Postotak površine piksela koji hvata svjetlo                              | Viši = bolja osjetljivost               |
| **Imager Noise** | Nasumične elektroničke varijacije koje uzrokuju greške u mjerenju svjetla | Viši = više lažnih eventa, niža točnost |

---

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

- Povećan bandwith -> veća brzina
- adaptive biasing -> znatno manja potrošnja energije
- reset switch -> OKIDA input i output zajedno i tako resetira napon

OVO OPISUJE ONAJ PROCES KADA SE EVENT POJAVI NA KAMERI I ONDA SAMO IZBLJEDI I RESETIRA SE

ON i OFF eventi -> circuit ih emitira u periferiju
- Pixel more emitat ili ON ili OFF event (NIKAD OBA ISTOVREMENO) prema periferiji
- Proces "komunikacije" kreće kad event trigerira piksel, a završava kada se piksel resetira na 0 (vrati u početno stanje)
- Prijevod na glupo: ON event -> nešto se miče i pikseli reagiraju; OFF event -> niš se više ne miče, pikseli miruju
- Bitna napomena: ON event označava da je piksel posvjetlio, OFF event da je potamnio

- ograničava se "fire-rate" za piksele kako pojedini pikseli ne bi zauzeli sve resurse za obradu
- omogućava da se više resursa posveti aktivnijim područjima (procesiraš ono di se nešto dešava; di ima evenata)
- Cilj je da se circuit ne pregrijava pretjerano, da ne troši resurse nepotrebno, da radi samo kad se nešto događa

KARAKTERISTIKE NAJVAŽNIJIH ASPEKATA:

- Uniformity of response - vraća razliku u osvjetljenju piksela -> bitno je uniformno i standardizirano evaluirati promjene
- Dynamic range - razlika imzeđu maksimalnog i minimalnog osvjetljenja u "sceni" kroz piksele; reliable and reproducible events
- Pixel bandwith - iznos raspona jačine najjačeg i najslabijeg intenziteta koji 1 piksel "prepozna"/"odradi". Stariji i noviji eventi se razlikuju u intenzitetu; intenzitet opada protokom vremena (fade-out)
- Latency&Latency jitter - ideja: ča je osvjetljenje manje, latencija je veća => proporcionalna recipročnom osvjetljenju (ča je škurije, teže se skuže eventi i promjene u svjetlosti kod piksela)
- Utvrđeno je kako je latencija ipak jako mala u svim uvjetima (SUPER ZA REAL-TIME PROCESSING)


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
- winner-take-all strujnih krugova 
- senzorskih strujnih krugova


Winner-take-all circuits by Gepetto

Apsolutno brate 💪🔥 — ajmo to sad složit **jasno, sažeto i profesionalno**, ali da ti sjedne odmah u glavu kad čitaš.
Evo ti **natuknice o Winner-Take-All (WTA)** koje možeš doslovno ubacit i u rad ako želiš:

---

## 🧠 Winner-Take-All (WTA) circuits — natuknice

### 🔹 Osnovna ideja

* WTA (Winner-Take-All) krugovi su **neuromorfni elektronički sustavi** koji oponašaju **konkurenciju među neuronima** u mozgu.
* Cilj im je da **odaberu samo najaktivniji (najjači) signal** među više ulaznih neurona ili kanala.
* Samo “pobjednički” neuron ostaje aktivan → ostali se **inhibiraju** (isključe).

---

### 🔹 Biološka inspiracija

* Temeljeni su na principu **lateralne inhibicije** u biološkim neuronskim mrežama.
* U mozgu aktivni neuron **koči (inhibira)** susjedne neurone → rezultat je **pojačan kontrast i selektivnost percepcije**.
* Ovaj mehanizam omogućuje **fokus pažnje** i efikasnu obradu informacija (npr. u ljudskoj mrežnici).

---

### 🔹 Kako WTA krug radi

1. **Ulaz:** više analognih signala (npr. struja ili napon iz različitih neurona/piksela).
2. **Natjecanje:** svi ulazi se natječu u istom krugu.
3. **Inhibicija:** slabiji ulazi se potiskuju putem inhibicijskog feedbacka.
4. **Izlaz:** samo najjači signal ostaje aktivan → “winner takes all”.

---

### 🔹 Implementacija u hardveru

* Realizira se korištenjem **MOS tranzistora** i **strujnih zrcala** (current mirrors).
* Krug se ponaša poput “strujnog tržišta” — ulaz s najvećom strujom **privuče sve resurse** i “pobijedi”.
* Tipično se koristi u **neuromorfnim procesorima** (npr. Intel Loihi, IBM TrueNorth, DYNAP-SE).

---

### 🔹 Prednosti

* **Smanjuje redundanciju** — aktivan je samo najvažniji neuron.
* **Povećava kontrast** i selektivnost u prepoznavanju uzoraka.
* **Štedi energiju** jer se ne obrađuju svi ulazi.
* Omogućuje **sparse coding** — mali broj neurona aktivan u danom trenutku.

---

### 🔹 Primjene

* **Računalni vid (event-based senzori):** bira piksele s najvećom promjenom kontrasta.
* **Prepoznavanje uzoraka:** odabir najrelevantnijeg neurona u skupu.
* **Klasifikacija i clustering:** određuje koji neuron najbolje “predstavlja” ulazni uzorak.
* **Roboti i edge sustavi:** koristi se za brze odluke uz minimalnu potrošnju energije.

---

### 🔹 Ukratko

| Pojam                     | Objašnjenje                                                         |
| ------------------------- | ------------------------------------------------------------------- |
| **Winner-Take-All (WTA)** | Sustav koji aktivira samo najjači ulaz, ostale potiskuje            |
| **Biološki ekvivalent**   | Lateralna inhibicija među neuronima                                 |
| **Ključna funkcija**      | Odabir dominantnog signala i smanjenje redundancije                 |
| **Prednosti**             | Učinkovitost, energetska štednja, bolja selektivnost                |
| **Upotreba**              | Neuromorfni čipovi, senzori vida, robotski sustavi, AI akceleratori |

---



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

#####################################################################################################
- Naša san video SNN in 5 minutes...pa zaš ne hitit oko
- Mozak jako efikasno procesira informacije
- SNNovi su novi tip AI inspiriran komunikacijom mozga
- Obične neuronske mreže baziraju se na kontinuiranim signalima, SNNovi koriste spikeove kao mozak
- Spikes => diskretni eventi koji se javljaju kroz vrijeme
- Realitičniji i efikasniji za obradu temporalnih informacija (informacije koji nisu statične, nego imaju vremensku "dimenziju"...videa, signali, živčani signali, eventi za event kamere i sl.)
- Real time procesiranje, event based vision, robotika, autonomna vozila

Komponente SNN-ova:
- međusobno povezani neuroni
- svaki neuron prima input od drugih
- inputi su električni impulsi koje zovemo "spikes"

- Kad neuron primi dovoljno spikeova u kratkom periodu, "fire-a" svoj spike
- Tako neuroni komuniciraju
- Timing spikeova je ključan => enkodira informacije o inputu
- Ča je jači input, jači je i spike
- Sinapse - veze između neurona
- Synaptic plasticity - sposobnost da sinapsa jača ili slabi kroz vrijeme => tako se SNN-ovi adaptiraju i uče kroz vrijeme
- Primjer: spečemo se na peć, pain receptori pošalju spikeove mozgu, to pojačava vezu među neuronima zaduženim za točno taj proces (osjet boli zbog vruće peći), idući put kad smo blizu vrućeg objekta, mozak će brže prepoznati opasnost i brže ćemo reagirati => synaptic plasticity IRL - "neurons that fire together, wire together"

Encoding information => kako pretvorit real-world data u spike patterne?
- Pretvorba našeg jezika u jezik neurona



- Rate coding -> frequency spikeova predstavlja intenzitet inputa => ča je input jači, to ima više spikeova...tipa...video koji prikazuje high-speed let drona stvara više spikeova nego video bijelega zida na kojemu se niš ne dešava

- Najklasičniji i najčešće korišten model.

- Frekvencija spikeova = intenzitet podražaja.

- Tvoj primjer s dronom je savršen — ako kamera “vidi” puno promjena → neuroni će ispucavati puno spikeova. Ako je scena statična (bijeli zid), spikeova gotovo da nema.
👉 Ograničenje: sporije reagira jer se čeka da se skupi određeni broj spikeova da bi se dobila jasna slika intenziteta.

- Temporal coding -> koristi se precizni timing spikeova za prijenos informacija. Točno vrijeme kad se spike dogodi može biti ključno; posebno za taskove gdje je bitno vrijeme i praćenje sekvenci

- Tu je važan točan trenutak kad spike dođe.

- Čak i ako je broj spikeova isti, različit raspored u vremenu može nositi različite informacije.

- Super za event-based senzore i zadatke gdje redoslijed i precizno vrijeme imaju smisla (npr. prepoznavanje govora, ritma, ili točno kada je objekt ušao u vidno polje).
👉 Prednost: može biti ekstremno energetski efikasno, jer mali broj spikeova može nositi puno info.

- Population coding -> koristi se grupa neurona da predstavlja 1 input. Svaki neuron u populaciji predstavlja specifični feature inputa. Potpuni pattern aktivnosti kroz populaciju predstavlja potpunu informaciju; npr. različiti neuroni mogu "fire-ati" za različite boje unutar slike

- Radi se o skupinama neurona — svaki neuron se “pali” za određeni feature (npr. specifičnu boju, kut linije, smjer kretanja).

- Informacija se dobiva iz kolektivnog uzorka aktivnosti svih neurona.

- Primjer: u vidnom korteksu mozga različiti neuroni su specijalizirani za različite orijentacije linija → cijela populacija ti daje kompletnu reprezentaciju slike.
👉 Ovo je “robustnije” jer se informacija ne oslanja na jedan neuron nego na distribuciju aktivnosti kroz cijelu populaciju.

- Neuron model
- LIFT model => matematički model toga kako neuroni procesiraju spikeove
- Kanta s vodom => neuron
- Kapljice vode => nadolazeći spikeovi
- Svaki spike dodaje malo vode u kantu/napona u neuron

- Kanta ima malu škulju koja uzorkuje da sporo gubi vodu kroz vrijeme => to predstavlja slabljenje napona u neuronu s prolaskom vremena (ono kad na kameri event izblijedi)
- Ako se kanta napuni i prelije, to je ekvivalentno temu kad neuron dobije dovoljno napona da postigne spike i resetira se  da bi mogao obrađivati novu rundu inputa => neuron fireing

- Moremo prilagođavat koliko se voda gubi i potrebnu količinu vode da se kanta napuni (dakle; tunable parametri su threshold za spike i vrijeme slabljenja eventa)

- Za slaganje SNN-ova => neuroni + sinapse + definiranje kako sinapse uče + layeri neurona + broj neurona u layeru

RATE VS TEMPORAL: 
https://github.com/AntonioLabinjan/Simulation-of-rate-and-temporal-coding/tree/master




Opportunities for neuromorphic computing algorithms and applications

Catherine D. Schuman & co.

Tehnologije neuromorfnog computinga bit će važne u budućnosti. Puno rada posvećeno je hardverskom djelu
Pregled nedavnih neuromorfnih algoritama i njihovih primjena

Bliži se kraj Moorovog zakona i Dennardovog scalinga. Traže se nove tehnologije za nastavak napredovanja performansi.

Chatgpt explained:
---

### 💡 **Moorov zakon (Moore’s Law)**

**Definicija:**
Gordon Moore (suosnivač Intela) 1965. je primijetio da se **broj tranzistora na integriranom krugu otprilike udvostručuje svake dvije godine**, dok se **cijena po tranzistoru smanjuje**.

**Što to znači:**

* Više tranzistora = **veća računalna snaga**
* Manji tranzistori = **manja potrošnja energije i niži troškovi**
* Dakle, računala postaju **brža, manja i jeftinija** svake 1–2 godine

**Primjer:**
Procesor iz 2000. imao je možda 30 milijuna tranzistora.
Danas ih high-end čip ima **preko 100 milijardi!**

**Ali…**
Danas smo došli do **fizičkih granica minijaturizacije** — tranzistori su već veličine par **nanometara** (manji od virusa!), pa se dalje teško ide klasičnim litografskim metodama.

---

### ⚙️ **Dennardov scaling (Dennard scaling)**

**Definicija:**
Robert Dennard (IBM) 1974. rekao je da kad se tranzistori smanjuju,
**napon i struja se proporcionalno smanjuju**, tako da **snaga po površini ostaje konstantna**.

**Drugim riječima:**
Ako smanjiš tranzistor 2x u svemu — visinu, širinu, napon —
on troši **isto energije po kvadratnom milimetru**, ali ima **dvostruko više tranzistora** → performanse rastu bez povećanja potrošnje energije ili topline.

**To je omogućilo:**
👉 Više tranzistora + veća brzina + ista potrošnja = eksplozija performansi od 80-ih do ranih 2000-ih.

**Ali…**
Oko **2005. scaling se raspao.**

* Naponi više ne mogu padati proporcionalno (fizičke granice — “leakage current”, tuneliranje elektrona kroz tanke gate-oxide slojeve).
* Snaga i temperatura su počele **drastično rasti**.
  ➡️ Zbog toga su frekvencije CPU-a stale oko 3–4 GHz i pojavila se era **višejezgrenih procesora** i **energetske optimizacije**.

---

### 🧠 Ukratko:

| Zakon                 | Ideja                                                 | Što je omogućio                  | Zašto više ne vrijedi                      |
| --------------------- | ----------------------------------------------------- | -------------------------------- | ------------------------------------------ |
| **Moorov zakon**      | Broj tranzistora se udvostručuje svake 2 god.         | Eksponencijalni rast performansi | Fizičke granice minijaturizacije           |
| **Dennardov scaling** | Manji tranzistori troše proporcionalno manje energije | Više brzine bez više topline     | Gubitak proporcionalnosti, previše topline |

---

💥 **Što sad?**
Kako se približavamo kraju oba zakona, istražuju se nove paradigme:

* **3D čipovi** (vertikalno slaganje tranzistora)
* **Neuromorfni čipovi** (poput IBM TrueNorth, Intel Loihi)
* **Kvantno računarstvo**
* **Optički procesori**
* **Spintronika i memristori**

---

Neuromorfna računala su jedna od tih novih tehnologija
Pojam "neuromorphic" je osmislio Carver Mead kasnih '80-ih
Odnosio se na: miks analogno-digitalnih implementacija računarstva inspiriranog mozgom
Sada ipak obuhvaća veći raspon raznovrsnih hardverskih implementacija

Neuromorfna računala - non-von Neumann računala čija struktura i funkcionalnosti su inspirirane mozgom i sastoje se od neurona i sinapsi
Von Neumann računala sastoje se od odvojenih jedinica za CPU i memoriju gdje se posebno pohranjuju podaci i instrukcije
U neuromorphic računalima i procesiranjem i memorijom upravljaju neuroni i sinapse
Programi u neuromorphic računalima definirani su strukturom neural networka i njihovih parametara, a ne eksplicitnim instrukcijama kao što je slučaj kod von Neumann računala
Von Neumann računala enkodiraju informacije kao numeričke vrijednosti u binarnom sustavu, a neuromorphic računala primaju spikeove kao input
Koristi se vrijeme pojave spikea, intenzitet i oblik za enkodiranje numeričkih informacija
Binarne vrijednosti mogu se pretvoriti u spikeove i obratno

Neuromorfna računala se u velikoj mjeri koriste paralelizmom gdje se izračuni obavljaju korištenjem više neurona i sinapsi istovremeno
No, izračuni koje neuroni i sinapse rade su relativno jednostavni u usporedbi s von Neumann sistemima
Collocated processing and memory (procesi i memorija su na istom mjestu). Iako se nekad neuroni smatraju processing unitima, a sinapse memorijom, u većini implementacija i neuroni i sinapse predstavljaju i memoriju i procese
Pomaže izbjeći von Neumann bottleneck (odvojenost procesora i memorije uzrokuje usporavanje u maksimalnom mogućem throughputu)
Pomaže izbjeći pristup podacima iz glavne memorije što inače troši puno energije

Ključne značajke neuromorfnih računala:

1. Inherentna skalabilnost

Neuromorfna računala su prirodno skalabilna – dodavanjem novih čipova povećava se broj neurona i sinapsi koje sustav može realizirati.

Više fizičkih neuromorfnih čipova može se povezati u jedan veliki sustav za izvođenje većih mreža.

To je već uspješno ostvareno kod sustava kao što su SpiNNaker i Intel Loihi.

2. Računanje temeljeno na događajima (event-driven computation)

Sustav obrađuje samo kada postoje podaci → ogromna energetska učinkovitost.

Neuroni i sinapse rade samo kada ima spikeova (impulsa) za obraditi.

Aktivnost mreže je vremenski rijetka (temporalno rijetka), što dodatno štedi resurse.

3. Stohastičnost (slučajnost)

Neuromorfni sustavi mogu uključivati elemente nasumičnosti u ponašanju neurona (npr. u njihovom okidanju).

Ova “šumovitost” (noise) može biti korisna – omogućuje robustnije i prirodnije ponašanje sustava, slično biološkom mozgu.

Neuromorfna računala troše ektremno malo energije => event driven & parallel => u bilo kojoj vremenskoj točki, samo mali dio sustava je aktivan, a ostatak je "idle"
Implementiraju "neural-network style" računanja => prirodna platforma za rad s brojnim primjenama machine learninga i AI
Trenutno se iz mozga najviše koriste neuroni i sinapse, ali još se istražuje mogu li se još neki koncepti mozga koristiti
Tehnologije su silicon-based, ali istražuju se novi materijali popur phase-change, ferroelectric, non-filamentary topological insulatora ili chanell-doped biomembrana
Razni neuromorfni uređaji imaju razne ciljeve i pristupe korištenja tehnologije


---

### 🧠 **Sažetak – Trenutno stanje i smjer razvoja neuromorfnih računala**

**1. Neuromorfni hardver već postoji i razvija se brzo**

* Za razliku od nekih drugih budućih tehnologija, **neuromorfni čipovi već postoje** i **dostupni su istraživačima**.
* Više **velikih sustava** razvijeno je s različitim pristupima i ciljevima.

---

**2. Glavni postojeći sustavi i projekti**

* **EU Human Brain Project** → razvio **SpiNNaker** i **BrainScaleS** za velike neuronske simulacije.
* **ODIN** – digitalni spiking neuromorfni procesor s podrškom za složenije neuronske modele.
* **Tianjic chip** – kombinira **neuromorfne SNN-ove** i **klasične umjetne neuronske mreže (ANN)** → omogućuje širu primjenu.
* Industrijski primjeri: **IBM TrueNorth**, **Intel Loihi**
* Akademski projekti: **DYNAPs**, **Neurogrid**, **IFAT**, **BrainScaleS-2**
* **BrainScaleS-2** dokazano ubrzava “learning-to-learn” procese — **uči mnogo brže od bioloških mreža**.

---

**3. Tehnologije i materijali za implementaciju**

* Svi ovi sustavi su trenutno **temeljeni na siliciju** (klasična CMOS tehnologija).
* Istražuju se **nove vrste materijala**, poput:

  * **Phase-change**, **feroelektrični** materijali
  * **Topološki izolatori**
  * **Biomembrane s dopiranim kanalima**
* **Memristori** su posebno popularni – omogućuju **spajanje memorije i obrade** (“collocated processing and memory”), čime se **smanjuje kašnjenje i potrošnja energije**.
* Koriste se i **optoelektronički uređaji** za još bržu i energetski efikasniju obradu.

---

**4. Raznolikost uređaja = prilagodljivost**

* Svaki materijal i uređaj ima **vlastite karakteristike** (brzina, potrošnja energije, biološka sličnost).
* Ta raznolikost omogućuje da se **neuromorfni hardver prilagodi specifičnim aplikacijama**.

---

**5. Povezanost s algoritmima i aplikacijama**

* Trenutno se većina istraživanja fokusira na **hardver**, ali pravi napredak zahtijeva **spajanje s algoritmima i primjenama**.
* Da bi se iskoristile sve prednosti neuromorfnog računanja, potrebno je razviti **neuromorfne algoritme** koji u potpunosti koriste potencijal te arhitekture.

---

**6. Definicija korištena u radu**

* Ovaj rad pod pojmom **“neuromorfno računanje”** obuhvaća sve vrste implementacija:

  * **digitalne**,
  * **mješovite analogno-digitalne**,
  * **analogne** sustave,
    ali se **posebno fokusira na one koji koriste spikeove** — tj. **spiking neuromorphic computers (SNN)**.

---

Programiranje neuromorfnih računala često uključuje kreiranje spiking neural networka koji se mogu deployati na neuromorfno računalo

---

### ⚡ **Ključne značajke Spiking Neural Networks (SNN-ova):**

**1. Biološka inspiracija s dodatnom dimenzijom vremena**

* SNN-ovi su **najbiološkiji oblik umjetnih neuronskih mreža**.
* Za razliku od klasičnih ANN-ova, **uključuju pojam vremena** u izračune.
* Neuroni i sinapse imaju **vremenske konstante i kašnjenja (delaye)**.

  * Npr. neuron **“curi” (leak)** naboj kroz vrijeme dok ne dosegne prag i ispali “spike”.

---

**2. Modeli neurona u SNN-ovima**

* Mogu biti **jednostavni** (npr. *Integrate-and-Fire*) – akumuliraju naboj do praga.
* Ili **složeni i biološki vjerniji**, poput *Hodgkin–Huxley modela* koji modelira ionske kanale u stvarnim neuronima.
* Dakle, razina biološke točnosti ovisi o potrebama i složenosti sustava.

---

**3. Dvije glavne skupine algoritama u neuromorfnom računanju:**
1️⃣ **Algoritmi za učenje/trening SNN-a** – optimiziraju mrežu da bi se koristila na neuromorfnom čipu (učeni pristup).
2️⃣ **Ručno konstruirani SNN-ovi** – dizajnirani bez strojnog učenja, već **ručno prilagođeni za određeni zadatak** (heuristički pristup).

---

**4. Suštinska razlika od tradicionalnih ANN-ova:**

* ANN-ovi → rade s **kontinuiranim vrijednostima** i *bez pojma vremena*.
* SNN-ovi → **obrađuju impulse (spikeove)** koji se događaju u **vremenu**.
  ➡️ Time bolje **imitiraju način na koji mozak obrađuje informacije**.

---


---

## ⚡ **Detaljan sažetak: Funkcioniranje Spiking Neural Networks (SNN)**

---

### 🧩 **1. Neuroni u SNN-u**

* **Akumulacija naboja:**

  * Neuroni **skupljaju električni naboj** tijekom vremena.
  * Naboj dolazi iz:

    * **okoline** → vanjski ulazni podaci, senzori itd.
    * **unutarnjih komunikacija** → spikeovi iz drugih neurona.

* **Prag (threshold):**

  * Svaki neuron ima **definiranu prag-vrijednost**.
  * Kad se akumulirani naboj **dosegne ili premaši prag**, neuron **ispali spike** (signal).
  * Spike se šalje **svim izlaznim sinapsama** tog neurona.

* **Leak (curenje naboja):**

  * Ako neuron ne dosegne prag, dio naboja **postupno nestaje kroz vrijeme**.
  * Ova **vremenska degradacija naboja** modelira ponašanje stvarnih bioloških neurona.

* **Axonal delay (aksonska odgoda):**

  * Kad neuron ispali spike, signal može biti **odgođen** prije nego što stigne do sinapsi.
  * Ova odgoda simulira **vremensko kašnjenje u prijenosu impulsa** kroz akson.

---

### 🔗 **2. Sinapse u SNN-u**

* **Povezuju neurone:**

  * Svaka sinapsa ima **pre-sinaptički** (izvorni) i **post-sinaptički** (ciljni) neuron.

* **Težina (weight):**

  * Sinapse imaju **numeričku težinu** koja određuje snagu veze.
  * Težine mogu biti:

    * **pozitivne** → *poticajne (excitatory)*, pojačavaju aktivnost
    * **negativne** → *inhibitorne*, smanjuju aktivnost

* **Sinaptička odgoda (delay):**

  * Signal iz pre-sinaptičkog neurona može imati **kašnjenje prije nego stigne do post-sinaptičkog**.
  * To doprinosi **asinkronom vremenskom ponašanju** mreže.

* **Učenje kroz promjenu težina:**

  * Sinapse **mijenjaju svoje težine** ovisno o aktivnosti mreže.
  * To omogućuje **učenje tijekom vremena** (npr. kroz mehanizme poput STDP – Spike-Timing Dependent Plasticity).

* **Rekonfigurabilnost:**

  * Neuromorfni čipovi omogućuju **paljenje/gašenje sinapsi** unutar fizičke mreže, čime se dinamički definira struktura mreže.

* **Programabilni parametri:**

  * U modernim neuromorfnim arhitekturama moguće je podešavati:

    * **threshold neurona**
    * **težine sinapsi**
    * **aksonske i sinaptičke odgode**
  * Time se omogućuje **potpuna fleksibilnost** mrežnih parametara.

---

### 🧠 **3. Asinkroni prijenos informacija**

* **Razlika u odnosu na klasične ANN-ove:**

  * U klasičnim ANN-ovima → informacije se **sinkrono prenose sloj po sloj**.
  * U SNN-ovima → zbog vremenskih odgoda i razlika u kašnjenju, **informacije se šire asinkrono** – svaki spike može stići u drugo vrijeme.

* **Posljedica:**

  * Svaki neuron može reagirati **u različitim trenucima**, ovisno o tome **kad mu spikeovi stignu**.
  * Mreža tako radi u **realnom vremenu** i ima **vremensku dinamiku** sličnu mozgu.

* **Prednost za neuromorfni hardver:**

  * Ova asinkronost **savršeno odgovara** neuromorfnim čipovima koji rade u **event-driven režimu** – obrađuju samo kada spike stigne.
  * Time se **štedi energija** i omogućuje **visoka paralelizacija**.

---

### ⏱️ **4. Vremenska domena rada mreže**

* Aktivnost mreže se može promatrati **po vremenskim koracima (t, t+1, t+2, …)**.
* U svakom vremenskom trenutku mijenja se:

  * koji neuroni su “ispalili” spike,
  * koliko naboja su drugi neuroni akumulirali,
  * koje sinapse su aktivne i kada njihovi signali dolaze.
* Dakle, mreža ima **dinamično stanje koje se evolucijski mijenja kroz vrijeme**.

---

### 📊 **5. Ukratko – ključni koncepti**

| Element            | Funkcija                     | Ključne karakteristike                                  |
| ------------------ | ---------------------------- | ------------------------------------------------------- |
| **Neuron**         | Akumulira i ispušta naboj    | Prag, curenje, aksonska odgoda                          |
| **Sinapsa**        | Povezuje neurone             | Težina (pozitivna/negativna), sinaptička odgoda, učenje |
| **Signal (spike)** | Diskretni impuls             | Prenosi informaciju u vremenu                           |
| **Obrada**         | Asinkrona, događajima vođena | Energetski učinkovita, vremenski osjetljiva             |

---
DNN = umjetna neuronska mreža s više slojeva koja uči iz velike količine podataka pomoću backpropagationa i gradijentnog spuštanja.
---

## 🔹 1. Problem s klasičnim treniranjem SNN-ova

* **Backpropagation i SGD (stochastic gradient descent)** su jako uspješni u deep learningu,
  ali **ne mogu se direktno primijeniti na SNN-ove** jer:

  * Spiking neuroni imaju **nediferencijabilne aktivacijske funkcije** (threshold funkcije).
  * SNN-ovi obrađuju **vremenske informacije**, što dodatno komplicira učenje.
* Potrebne su **prilagodbe** (npr. surrogate gradients, smoothed activation functions),
  ali to često **smanjuje točnost** u odnosu na klasične ANN-ove.

---

## 🔹 2. Mapiranje klasičnih DNN-ova na SNN-ove

* Umjesto treniranja SNN-a od nule, često se:

  1. **Trenira DNN**,
  2. **Zatim se mapira (pretvori)** u SNN za **inference**.
* Ove metode daju:

  * Blizu **state-of-the-art točnost**
  * Uz **veliko smanjenje potrošnje energije** (jer SNN obrađuje samo spikeove).
* Dataseti korišteni: **MNIST, CIFAR-10, ImageNet**.
* Ključne tehnike:

  * Normalizacija težina i aktivacija
  * Zamjena max-poolinga s average poolingom
  * "Few Spikes" neuron model (FS-neuron) — složene aktivacije predstavljene s 1–2 spikea.
* Primjene: **keyword spotting, medicinska analiza, detekcija objekata** (na Loihi, TrueNorth).
* Problem: **mapiranje može smanjiti točnost** zbog:

  * razlike DNN ↔ SNN
  * hardverskih ograničenja (npr. **memristori** imaju nižu preciznost težina i varijacije po ciklusu).

---

## 🔹 3. Reservoir computing (Liquid State Machines)

* Ne zahtijeva klasično treniranje SNN-a.
* Sastoji se od:

  * **"tekućeg" (liquid) dijela** – nasumična mreža spike neurona (recurrent, sparse)
  * **readout sloja** – trenira se (npr. linearnom regresijom)
* Dvije ključne osobine:

  * **Input separability** – različiti ulazi daju različite izlaze
  * **Fading memory** – stari signali nestaju s vremenom
* Prednosti:

  * Nema treniranja samog SNN-a
  * Dobro radi s vremenskim podacima
* Primjene:

  * obrada **bio-signala**, **prosthetic control**, **audio/video analiza**
  * koristi **hijerarhijske slojeve** tekućih mreža

---

## 🔹 4. Evolucijski pristupi

* Koriste **evolucijske algoritme** (mutacija, selekcija, reprodukcija) za:

  * Optimizaciju **parametara** (thresholds, delays)
  * Dizajn **strukture mreže** (koliko neurona, kako su povezani)
* Prednosti:

  * Ne zahtijevaju diferencijabilnost
  * Mogu raditi s bilo kojom topologijom mreže
* Nedostatak:

  * **Sporo konvergiraju**
* Primjene:

  * **Kontrola robota**, **video igre**, **autonomna navigacija**

---

## 🔹 5. Plastičnost (biološki inspirirano učenje)

* Temelji se na **aktivnosti neurona i promjenama sinaptičke jačine**.
* Najpoznatije: **STDP (Spike-Timing-Dependent Plasticity)**

  * Težine se mijenjaju prema vremenskom odnosu pre- i post-sinaptičkih spikeova.
* Korišteno na: **MNIST, CIFAR-10, ImageNet**
* Prednosti:

  * Može **približiti klasične ML metode** (klasteriranje, Bayes inference)
  * Kombinira se s **reservoir computingom** (npr. NeuCube)
* Primjene:

  * **EEG analiza**, **detekcija stanja spavanja**, **prostetičke kontrole**
* Varijante:

  * **Rekurentne SNN mreže s kašnjenjima i plastičnošću**
  * **Polychronization networks** – klasifikacija vremensko-prostorno varijabilnih uzoraka
  * **Winner-take-all** modeli
  * Učenje **tajminga spikeova** (precizna klasifikacija prema vremenu)

---

## 🔹 6. Nemachine learning algoritmi

* Neuromorfni hardver može rješavati **ne-ML probleme**:

  * **Graf algoritmi** (npr. shortest path)
  * **Random walks** i **Markov chains**
  * **NP-kompletni problemi** (SAT, QUBO, graph partitioning)
* Primjeri:

  * **IBM TrueNorth**, **Intel Loihi**, **SpiNNaker** rješavaju NP probleme
  * Neuromorfni pristupi ponekad **precizniji od D-Wave kvantnog računala!**
* Prednosti:

  * Paralelna, niskoenergetska obrada
  * Odlična primjena u **grafovima, relacijskim strukturama**, **Bayesovim mrežama**

---

## 🔹 7. Trenutno stanje i izazovi

* **SNN-ovi i neuromorfni hardver još nisu u stvarnim aplikacijama.**
* Fokus je zasad na **benchmark datasetima i demonstracijama**.
* Glavni izazov:

  * Još **nema kombinacije algoritma i aplikacije** gdje SNN nadmašuje deep learning u točnosti.
  * Prednost je zasad **u energetskoj učinkovitosti**, ne u performansama.
* Potrebno:

  * Širiti fokus **izvan backpropagationa**
  * Razvijati **novije, biološki inspirirane algoritme**
  * Iskoristiti **vremensku i događajnu prirodu** SNN-ova

---

## 🔹 8. Zaključna poruka

> Neuromorfni sustavi ne bi trebali pokušavati samo *imitirati* deep learning,
> nego razviti **nove algoritme** koji koriste **njihovu biološku i vremensku prirodu** —
> evoluciju, plastičnost, događajnu obradu i inherentnu paralelizaciju.

---


Savršeno — ovo je važan dio teksta koji govori o **ograničenjima pristupa i skalabilnosti u neuromorfnom računanju**.
Evo ti **jasne i detaljne natuknice** na hrvatskom:

---

### ⚙️ **Širi pristup neuromorfnom hardveru i simulatorima – ključni izazovi i rješenja**

#### 🔒 Trenutni problemi:

* **Ograničen pristup hardveru:**

  * Postoji **malo dostupnih neuromorfnih sustava** (poput Loihi, TrueNorth, SpiNNaker).
  * **Dostupni su samo putem ograničenog cloud pristupa**, što usporava istraživanje i razvoj.

* **Softver i simulacije nisu dovoljno pristupačni:**

  * Postoji nekoliko **open-source simulatora** (npr. **NEST**, **Brian**, **Nengo**), ali svaki je:

    * specijaliziran za **određenu zajednicu** ili **vrstu zadataka**,
    * teško primjenjiv izvan tih specifičnih područja.
  * **NEST** je fokusiran na **računalnu neuroznanost**,
    **Nengo** na **Neural Engineering Framework (NEF)**,
    što ograničava njihovu **širu upotrebljivost** u računarstvu i industriji.

* **Slaba skalabilnost i performanse simulatora:**

  * Mnogi simulatori **nisu dovoljno brzi** pri radu u velikim razmjerima.
  * Zbog **eksplozije količine podataka**, potrebno je procesirati informacije **brže nego što se generiraju**,
    što trenutni simulatori **ne mogu pratiti**.
  * Posljedica: **sporo treniranje SNN-ova** i **teško testiranje novih algoritama**.

---

#### 🚀 Preporuke i budući smjer:

* **Razviti pristupačnije i univerzalnije alate** koji bi omogućili:

  * **širu upotrebu u računalnoj znanosti i industriji**,
  * **brže eksperimentiranje i inovaciju** u algoritmima.
* **Poboljšati performanse simulatora** kako bi mogli:

  * **raditi u realnom vremenu**,
  * **skalirati** na **velike podatkovne setove i HPC (high-performance computing)** sustave.
* **Omogućiti bržu evaluaciju algoritama** čak i kada fizički hardver nije dostupan —
  time bi se ubrzao **razvoj i testiranje novih neuromorfnih rješenja**.

---

### 💡 Ukratko:

> Napredak neuromorfnog računarstva trenutno koči **ograničen pristup hardveru** i **slaba skalabilnost simulatora**.
> Rješenje je razvoj **brzih, skalabilnih i univerzalnih softverskih alata** koji omogućuju brzu inovaciju i širu dostupnost zajednici.

---

---

### 🔹 Glavna ideja:

U budućnosti, **neuromorfna računala** neće raditi sama za sebe, nego će biti **dio većeg ekosustava** — zajedno s **klasičnim računalima**, **GPU-ovima**, pa čak i **kvantnim računalima**.
Svako od njih ima svoju **specijalnost**:

* CPU – dobar za opće zadatke
* GPU – moćan za paralelne izračune
* Neuromorfni čip – izuzetno energetski učinkovit za obradu u stilu mozga (event-based, SNN, itd.)
* Kvantni čip – jak za specifične optimizacijske i probabilističke probleme

Dakle, ideja je: **kombinirati sve njih pametno**, tako da svaka komponenta radi ono što najbolje zna.

---

### 🔹 Problem:

Ali — postoji **ogroman izazov** u tome da sve te različite arhitekture **rade zajedno**.

Trenutno:

* Neuromorfna računala **ovise o klasičnim računalima** (tzv. *host machines*) za:

  * programiranje samog neuromorfnog čipa (definiranje mreže i pravila)
  * komunikaciju sa senzorima i uređajima u stvarnom svijetu
  * primanje i slanje podataka

Ta ovisnost ima **visoku cijenu** — i **u vremenu** i **u energiji**.
Dakle, čak i ako neuromorfni čip radi ultraefikasno, ako mora stalno čekati ili komunicirati s klasičnim računalom, **gubi se njegova prednost**.
Na kraju, kad se uračunaju svi “overheadi” (komunikacija, prijenos podataka, CPU obrada), koristi od neuromorfnog pristupa mogu **potpuno nestati**.

---

### 🔹 Rješenje koje autori predlažu:

Treba razviti **nove modele programiranja i arhitekture** koje će:

* **smanjiti ovisnost** neuromorfnih računala o klasičnim hostovima,
* **optimizirati komunikaciju** između njih (da ne troši više nego što vrijedi),
* i omogućiti **jedinstveno programiranje** heterogenog sustava — tako da programer ne mora ručno "spajati" CPU + GPU + neuromorfni čip.

---

### 🔹 Ukratko:

➡️ Buduća računala neće biti samo "brža", nego **pametno organizirana** kombinacija različitih tehnologija.
➡️ Glavni izazov: **kako natjerati neuromorfna, kvantna i klasična računala da učinkovito surađuju** bez da troše previše energije i vremena na međusobnu komunikaciju.

🔹 Glavna ideja:

Ovaj dio govori o nedostatku standardiziranih benchmarka i metrika u području neuromorfnog računarstva.
To je OGROMAN problem — jer bez njih ne možeš objektivno usporediti:

koji hardver radi bolje,

koji algoritam je učinkovitiji,

ili koja metoda ima stvarne prednosti u praksi.

🔹 Zašto su benchmarki važni?

Usporedi to s deep learningom:

Kad se pojavio ImageNet dataset, svi su znali:
“Ako tvoj model pobijedi na ImageNetu — imaš dobru arhitekturu.”

Taj izazov je pokrenuo eksploziju napretka — AlexNet, ResNet, EfficientNet...
Benchmark je bio zajednički cilj cijele zajednice.

➡️ Neuromorfno računarstvo nema takav “ImageNet moment”.
Ne postoji jedan zajednički izazov ili set jasnih metrika koji bi usmjerio istraživanja i omogućio fer usporedbe.

🔹 Trenutna situacija:

Postoji nekoliko pokušaja benchmark setova i datasetova specifičnih za spike-based i event-based pristupe:

Neuromorphic MNIST (N-MNIST) — spike verzija klasičnog MNIST-a

DVS Gesture Dataset — gesta prepoznata pomoću Dynamic Vision Sensor (event kamera)

Spiking Heidelberg Audio Dataset (SHD) — zvučni događaji za spike mreže

Ali...
➡️ nisu široko prihvaćeni u zajednici,
➡️ nemaju status “standardnog testa”,
➡️ i često ne iskorištavaju pravu prednost neuromorfnih sustava — temporalnu obradu događaja u stvarnom vremenu.

Zato se često koriste stari ML datasetovi poput MNIST, CIFAR-10 i ImageNet, ali oni:

nemaju vremensku dimenziju,

nisu event-based,

pa zapravo ne pokazuju pun potencijal neuromorfnih sustava.

🔹 Problem jedinstvenog benchmarka:

Autori upozoravaju — nije ni idealno imati samo jedan zadatak (kao što je bio ImageNet u ML-u).
Zašto?
Jer to može dovesti do “uske optimizacije” — svi algoritmi se prilagođavaju samo da bi bili bolji na tom jednom zadatku, a gubi se šira primjena.

🔹 Rješenje:

👉 Umjesto jednog “svetog grala” benchmarka,
treba napraviti suite (set) različitih izazova i metrika koji će:

pokrivati razne tipove zadataka (vizualne, auditivne, motorne, biološke simulacije itd.),

uključivati različite tipove algoritama (ML i non-ML pristupe),

i omogućiti fer usporedbe između različitih arhitektura (CPU, GPU, neuromorfni, kvantni...).

🔹 Ukratko:

🧠 Problem: Nema zajedničkih benchmarka → teško usporediti performanse i napredak.

⚙️ Posljedica: Razvoj ide sporije jer svatko radi na svom datasetu, s vlastitim metrikama.

🚀 Rješenje: Napraviti skup različitih izazova koji potiču inovaciju u više smjerova — ne samo jedan “ImageNet za neuromorfne”.

Brutalan i važan odlomak — ovo ulazi pravo u **“softverske” izazove neuromorfnog računarstva**! 💥
Evo ti **detaljno, ali jasno strukturirane natuknice** koje hvataju sve bitno:

---

## 🧠 Ključna tema: “Defining programming abstractions”

➡️ Problem: **Nema jednostavnog, apstraktnog načina za programiranje neuromorfnih sustava.**
Trenutno programeri moraju **ručno definirati svaki neuron, sinapsu, parametre i veze**.
To je:

* sporo,
* komplicirano,
* sklono pogreškama,
* i potpuno drugačiji način razmišljanja od klasičnog programiranja.

---

### 🔹 1. Trenutni način rada

* Programer mora **ručno dizajnirati SNN (Spiking Neural Network)** za zadatak.
* Definira se:

  * svaki neuron,
  * svaka sinapsa,
  * njihove veze,
  * parametri (threshold, delay, weight…).
* To traži **mikro-razinu kontrole** → usporedivo s pisanjem “assembly koda za mozak”.

➡️ **Posljedica:** ogroman trud, mala fleksibilnost, visoka mogućnost greške.
➡️ Zato razvoj *non-ML* algoritama na neuromorfnim sustavima ide jako sporo.

---

### 🔹 2. Zašto se najviše koriste graf algoritmi

* Neuromorfne mreže imaju prirodnu analogiju s grafovima:

  * **Čvorovi (nodes)** → neuroni
  * **Bridovi (edges)** → sinapse
* Zato je **jednostavno mapirati graf strukturu** u SNN.
  ➡️ Zato su mnogi *non-machine learning* algoritmi fokusirani upravo na graf probleme (npr. pretraživanje grafa, optimizacija).

---

### 🔹 3. Postojeći pokušaji apstrakcije (viša razina)

Postoje neki modeli koji pokušavaju “olakšati” programiranje:

* **Neural Engineering Framework (NEF)** →
  omogućuje definiranje apstraktnih izračuna pomoću neurona (često korišten za biološki realistične modele).
* **Dynamic Neural Fields (DNF)** →
  fokusiran na *embodied cognition* (npr. simulacije kognitivnih procesa u robotici).

➡️ Ali problem:
Ovi pristupi su **ograničeni na specifične slučajeve**.
Ne postoji **opća apstrakcija** koja bi omogućila programiranje neuromorfnih računala za *razne* zadatke (ne samo neuronske modele ili robotiku).

---

### 🔹 4. Moguće rješenje: Subnetworks kao “programske primitive”

Zamišlja se ideja da bi se mogli definirati **mali, standardizirani “spike subnetworks”** koji obavljaju osnovne zadatke poznate programerima:

* logičke operacije (**AND, OR, XOR**),
* uvjeti (**if / else**),
* petlje (**loops**),
* binarne operacije itd.

➡️ Takvi “neuronski blokovi” mogli bi se **sastavljati u veće sustave**, baš kao što se funkcije i moduli spajaju u normalnim programima.

* Postoji istraživanje (Plank et al.) koje pokazuje kako spike mreže mogu realizirati **AND, OR, XOR** logiku.
* Ali to je tek početak — ogroman prostor za razvoj **“neuromorfnih programskih konstrukata”**.

---

### 🔹 5. Problem: nedostatak svijesti u široj zajednici

Dok ne postoje jasne apstrakcije i dok se šira programska zajednica **ne upozna s konceptima spike-računarstva**, razvoj *non-ML* neuromorfnih algoritama bit će spor.

➡️ Dakle, **nije samo hardverski problem**, već i **problem edukacije i alata**.

---

### 🔹 6. Bitno upozorenje: Neuromorfno ≠ za sve

Autori naglašavaju:

* Da, moguće je implementirati razne algoritme na neuromorfnim računalima,
  **ali ne znači da sve treba**.
* Neuromorfni sustavi su **specijalizirani procesori**, ne “opće namjene” (kao CPU).
* Treba ih koristiti tamo gdje imaju **prirodnu prednost** — u:

  * real-time obradi događaja,
  * energetski učinkovitim simulacijama,
  * biološkim modelima,
  * adaptivnim i vremenski ovisnim sustavima.

---

### 🔹 7. Zaključak:

* 🧩 **Problem:** nema jednostavnog načina za programiranje neuromorfnih sustava.
* ⚙️ **Trenutno:** sve se definira ručno, na neuronskoj razini.
* 💡 **Postoje pokušaji:** NEF i DNF — ali ograničeni.
* 🚀 **Budućnost:** stvaranje “neuromorfnih programskih apstrakcija” (npr. neuronskih modula za osnovne operacije).
* ⚠️ **Napomena:** neuromorfni čipovi su specijalizirani — nisu za svaki problem.

---

## 🧩 **OUTLOOK — Budućnost neuromorfnog računarstva**

### 🔹 1. Ogroman potencijal izvan Mooreovog zakona

* Neuromorfni procesori su:

  * **energetski izuzetno učinkoviti**,
  * **sposobni za strojno učenje i neke nestrojne (non-ML) izračune**,
  * **velika nada za post-Moore eru** – omogućuju napredak performansi bez tradicionalnog skaliranja tranzistora.
* Nude **nove paradigme obrade podataka** inspirirane biologijom (asinkrono, događajno, paralelno).

---

### 🔹 2. Tri glavna buduća **use-casea** za neuromorfne procesore

#### 🟢 (1) **Edge computing** — uređaji na rubu mreže

* Idealni zbog **niskog energetskog troška**.
* Primjene:

  * autonomna vozila i dronovi,
  * robotika,
  * udaljeni senzori,
  * nosivi uređaji,
  * Internet of Things (IoT).
* Fokus: **ekstremno niska potrošnja i real-time obrada**.

#### 🟠 (2) **AI akceleratori i koprocesori** u osobnim uređajima

* Mogu postati **ko-akceleratori** u:

  * pametnim telefonima,
  * laptopima,
  * stolnim računalima.
* Slični današnjim GPU/NPU akceleratorima, ali s **reda veličine manjom potrošnjom energije**.
* Mogu značajno **produžiti trajanje baterije** i ubrzati AI zadatke.

#### 🔵 (3) **Koprocesori u heterogenim HPC sustavima**

* U budućim **heterogenim superračunalima**, neuromorfni čipovi će:

  * izvršavati **spike-based simulacije**,
  * pokretati **graf algoritme**,
  * **rješavati diferencijalne jednadžbe**,
  * **aproksimirati NP-kompletne probleme** učinkovito.
* Fokus: **reconfigurability** i **trening ubrzanje** za kompleksne znanstvene izračune.

➡️ **Napomena:** implementacije će se razlikovati:

* Edge uređaji – visoka specijalizacija, minimalna potrošnja.
* HPC okruženja – veća fleksibilnost i mogućnost treniranja.

---

### 🔹 3. Trenutno stanje i smjer razvoja

* Već postoji **nekoliko velikih neuromorfnih sustava** dostupnih istraživačima (npr. Loihi, SpiNNaker).
* Aktivno se razvijaju i **nove vrste materijala i uređaja** za fizičku implementaciju (npr. memristori, analogni elementi).
* Ovo stvara **ogromnu priliku za “hardware–software co-design”** — zajednički razvoj od materijala do aplikacija.

---

### 🔹 4. **Hardware–software codesign pristup**

Trenutno:

* Razvoj ide **odozdo prema gore** → prvo materijali i uređaji, pa tek onda algoritmi.

Bolji pristup:

* **“Cijeli stack codesign”** – paralelno oblikovati sve slojeve:

  * materijali i uređaji,
  * arhitektura,
  * algoritmi,
  * aplikacije.

➡️ Time bi algoritmi mogli **utjecati na dizajn samog hardvera** i obrnuto.

---

### 🔹 5. **Primjeri suvremenog codesign pristupa**

* **Bayesian optimization** i **Neural Architecture Search (NAS)** koriste se za optimizaciju cijelog sustava.
* Primjer:

  * kod **memristive crossbar** akceleratora,
  * automatski se određuje broj i veličina crossbara kako bi se **maksimizirala točnost i energetska učinkovitost**.

---

###  6. **Biologija ↔️ Materijali: novi smjer razvoja**

* Trenutno se u sinaptičkoj plastičnosti ide “odozgo prema dolje”:

  * inspiracija iz biologije → implementacija u uređajima → prilagodba algoritma.
* Novi smjer:

  * **učiti iz fizičkih svojstava novih materijala** kako bi se razvili *novi algoritmi plastičnosti* (bottom-up).
* Ideja: možda postoje **fizičke pojave u materijalima** koje mogu nadahnuti *potpuno nove modele učenja*.

---

###  7. **Paradigm shift – promjena načina razmišljanja**

* Uspješno korištenje neuromorfnih računala zahtijevat će **promjenu paradigme programiranja**.
* Istraživači moraju **razmišljati u terminima događaja, vremena i paralelizma**, a ne samo sekvencijalnog koda.

---

###  8. **Potencijalni najveći dobitnici**

* Osim klasičnog ML-a, dvije skupine algoritama koje bi mogle **najviše profitirati**:

  * **Graf algoritmi** (dijagrami, mreže, optimizacija veza)
  * **Optimizacijski zadaci** (posebno NP-teški problemi)
* Oboje imaju koristi od:

  * **masivne paralelizacije**,
  * **asinkronosti**,
  * **stohastične prirode neuromorfnih sustava**.

---

###  9. **Zaključna vizija**

* Neuromorfno računarstvo je još u ranoj fazi, ali:

  * ima **ogroman potencijal** za redefiniranje računarstva,
  * omogućuje **energetski učinkovite i paralelne izračune**,
  * **nadopunjuje** postojeće paradigme (ne zamjenjuje ih).
* Vrijeme je da **šira računalna znanstvena zajednica** počne uključivati neuromorfne računare kao **dio buduće računalne infrastrukture**.

---

Event-based vision: A Survey, Guillermo Gallego & co.
- Event kamere - bio-inspired senzori koji, za razliku od standarnih frame-based kamera, asinkrono mjere per-pixel promjene svjetline i kao output izbacuju stream evenata (svaki se sastoji od: vremena, lokacija i oznake promjene svjetline)
- Features: high temporal resolution, high dynamic range, low power consumption, high pixel bandwith, reduced motion blur, low latency, high speed
- Koriste se za sve levele CV-a (od feature detectiona i trackinga, optical flowa do rekonstrukcije, segmentacije i recognitiona)
- Postoje posebne tehnologije za to (npr. SCNNs)


- Započelo 1986. - Carver Mead => spoj inženjerske i bioliške perspektive
- 1991. - Silicijska zjenica => oponašanje prirodne arhitekture oka
- Cilj: shvatiti kako mozak radi i složiti ga na računalnom čipu
- Bio-inspired tehnologija silikonskih zjenica/event kamera
- Vid je najdominantniji ljudski osjet => najjači signali
- Event based senzori riješavaju neke probleme frame-based visiona (high speed motion estimation; high dynamic range)
- Asinkroni senzori => sampling scene na temelju dinamike u istoj, a ne na temelju internog clocka koji nema veze s događajima na sceni (kao kod frame based di se koristi sampling u k fps)
- Visok temporal resolution; niska latencija; visok dynamic range, niska potrošnja energije
- Robotika, wearable uređaji + situacije di standarnde kamere ne delaju dobro (high speed&dynamic range)...nekontrolirano osvjetljenje, latencija + područja di je važno očuvanje električne energije
- AR/VR, video igre

- Rade znatno drukčije nego standarne kamere (asinkrono mjere promjene u intenzitetu svjetlosti by-pixel) pa su potrebne nove metode za procesiranje outputa

- Object tracking, surveillance and monitoring, object/gesture recognition, depth estimation, structured light 3d scanning, optical flow estimation, image reonstruction, localization&mapping, image deblurring, star tracking

Glavna razlika u odnosu na standardne frame based kamere:
- standardne kamere koriste full images at a rate specified by external clock (npr. 30fps)
- event kamere reagiraju na promjene svjetlosti u sceni asinkrono i neovisno za svaki piksel
- output event kamere je varijabilna data-rate sekvenca digitalnih evenata (spikeova)

- Svaki spike predstavlja promjenu osjvetljenja u određenom pikselu u određenom vremenskom trenutku => spiking nature biološkog vida
- Svaki piksel pamti log intenziteta za svaki eent i kontinuirano prati promjenu intenziteta u odnosu na upamćenu vrijednost
- Kada promjena pređe threshold, kamera šalje event koji se šalje (x,y koordinate lokacije, t timestamp, 1-bitni polaritet promjene (ON ako se svjetlost povećala, OFF ako se smanjila)
- Eventi se šalju od pixel arraya prema periferiji i onda van iz kamere koristeći shared digital output bus (Address-event representation; AER)
- Rate od 2 MHz do 1200 Mhz ovisno o čipu i hardveru

- Event kamere su data-driven senzori (output im ovisi o količini kretanja ili promjeni svjetlosti u sceni)
- Ča je kretanje brže/češće/intenzivnije, više evenata po sekundi se generira
- Svaki piksel ima vlastiti sampling rate i prati intenzitet evenata koji signalizira
- Eventi imaju timestampove na razini mikrosekunde => šalju se s latencijom manjom od milisekunde
- Senzori brzo reagiraju na stimulans 

- Incident light => produkt osvjetljenja scene i odsjaja površine koja se "snima"
- Ako je osvjetljenje otprilike konstantno, incident light je minimalan i nastaje samo kada se ovjekt gledanja pomiče
- DVS pikesli imaju konačan bandwith; ako su nadolazeće promjene u intenzitetu prečeste, photoreceptor "filtrira" varijacije u njima i ne registrira ih => ukratko; dvs pikseli imaju fizički limit maksimalne brzine kojom reagiraju na promjene
- Ako su eventi prebrzi; senzor praktički lovi manje evenata nego ako su u "normalnoj brzini"

- Najčešći event camera dizajni:
- first silicon retina: Mahowald&Mead (1986-1992)
- logaritamski pikesli => output spike eventi nastaju koristeći AER protokol
- Problem: treba precizno ušzimavati svaku pojedinu žicu (bias parametri); mismatch u responsevima za različite piksele; pikseli su preveliki

- DVS event camera => utemeljena na frame-based silicon mrežnici (continous-time fotoreceptor + redout circle koji se resetira svaki put kad se pixel samplira)
- Uviđeno je da je potreban i neki oblik statičkog outputa ("absoulute brightness")
- Ideja: kamera koje concurrently daju i statički i dinamički output)

- ATIS => asinkroni time based image sensor => pikesli sa DVS subpikselima
- Okidač resetira kondenzator na visoki napon; sturja se odvodi iz kondenzatora pomoću diode; što je input svjetliji, to se kondenzator brže prazni
- Samo pikseli koji se stvarno mijenjaju imaju utjecaj na napon
- Ča je svjetliji event; to su promjene češće
- Neodostatak: jako veliki pikesli; u mraku je jako sporo i novi eventi mogu prekinuti očitavanje starih...nepraktično

- DAVIS => spoj aktivnog pixel senzora (APS) i DVS-a
- puno manji pikseli
- dijeljena fotodioda
- frameovi se obrađuju u konstantom rateu
- problem: ograničeni dynamic range; redundancija ako se pikseli ne promjene

Prednosti event kamera
High temporal resolution:
 - praćenje promjena osvjetljenja je brzo
 - iščitavanje evenata je digitalno, s 1MHz clockom (eventi su detektirani i timestampirani u roku mikrosekunde)
 - mogu snimati jako brze pokrete, bez da dolazi do blura koji je standardan za frame-based kamere

Low latency:
 - svaki piksel radi zasebno; ne treba se čekati global exposure za cijeli frame
 - čim se event detektira, transmitted je (latencija ispod milisekunde u realnom okruženju)

Low power:
 - transmitaju se samo promjene u osvjetljenju; nema redundantnih podataka
 - struja se troši samo za procesiranje piksela koji se mijenjaju

High dynamic range:
 - i više nego duplo bolje nego kod najkvalitetnijih frame-based kamera
 - mogu captureati informacije u svim uvjetima..od mjesečine do sunca
 - fotoreceptori rade logaritamski i svaki piksel radi zasebno, bez da čeka "zatvarač" kamere
 - poput zjenice, prilagodljivi su i jakom mraku i jakoj svjetlosti

Izazovi:
- dizajn novih korisnih softverskih algoritama i hardverskih metoda
1) space-time output
   Output event kamera je fundamenatalno drukčiji od outputa standardnih kamera; eventi su asinkroni i prostorno sparse (rijetki), dok su frameovi sinkroni i dense (frame točno prati tijek onoga ispred kamere)
2) different photometric sensing
   Standardne kamere daju grayscale info, dok eventi u sebi sadrže binarni (increase/decrease) info o promjeni svjetlosti. Promjene svjetlosti ne ovise samo o trenutnom osvjetljenju scene nego i o trenutnim i prošlim kretnjama u sceni
3) noise and dynamics
   Svi vision senzori su noisy jer postoji neizbježan noise u česticama sjvetlosti i u samim el. krugovima u tranzistorima. Problem ze event based kamere: kako kvantizirati temporal contrast

---

### **Kvantizacija temporalnog kontrasta – sažetak**

**1. Temporalni kontrast (C):**

* Mjeri promjenu svjetline kroz vrijeme:
  [
  C(t) = \frac{I(t) - I(t - Δt)}{I(t - Δt)}
  ]
* DVS piksel reagira samo kad ta promjena prijeđe određeni prag (θ).

**2. Generiranje eventa:**

* Ako |C(t)| > θ → generira se event (ON za porast, OFF za pad svjetline).
* Male promjene ispod praga se ignoriraju.

**3. Problem kvantizacije:**

* Potrebno je definirati kako pretvoriti kontinuirane promjene svjetline u diskretne događaje.
* Ključno je odabrati prag koji daje dovoljno informacija, ali bez previše šuma.

**4. Izazovi:**

* **Previsok prag:** gube se male, ali važne promjene.
* **Prenizak prag:** nastaje previše šuma (previše eventova).
* **Fizičko ograničenje:** pikseli imaju ograničen odziv (RC krug → bandwidth limit), pa ne mogu detektirati ekstremno brze promjene.

**5. Logaritamska kvantizacija:**

* U praksi se koristi logaritamska razina svjetline:
  [
  \log(I(t)) - \log(I(t - Δt))
  ]
* Time se postiže bolja stabilnost u različitim uvjetima osvjetljenja.

**6. Zaključak:**
Kvantizacija temporalnog kontrasta je proces kojim DVS senzor pretvara kontinuirane promjene svjetline u diskretne, informativne događaje pomoću praga i logaritamske transformacije, uz fizičko ograničenje brzine odziva piksela.

---

Nove metode trebaju uzeti u obzir: space-time, photometričku i stohastičku prirodu podataka
Kako najefikasnije izvući info iz evenata da bude relevantno za task koji se riješava?
Kako se noisy i neidealni efekti mogu modificirati da se lakše izvlače korisne informacije



---

## 🔹 Osnovni koncept

Event-based kamera (DVS) ima piksele koji **ne snimaju frameove**, nego reagiraju *neovisno i asinkrono* na **promjene u logaritmu svjetlosnog toka** (fotostruke).

Definicija:
[
L = \log(I)
]
gdje je ( I ) – fotostruja (intenzitet svjetlosti), a ( L ) logaritamska svjetlina (“brightness”).

---

## 🔹 Kada se generira event

Svaki piksel ima svoju zadnju pohranjenu vrijednost svjetline.
Event se generira kad promjena svjetline **od zadnjeg eventa** prijeđe određeni prag ( C ):

[
L(x_k, t_k) - L(x_k, t_k - \Delta t_k) = p_k C \quad (1)
]

* ( x_k ): koordinate piksela koji je ispalio event
* ( t_k ): trenutak događaja
* ( p_k \in {+1, -1} ): **polarnost** eventa

  * ( +1 ) = porast svjetline (**ON event**)
  * ( -1 ) = pad svjetline (**OFF event**)
* ( C ): **temporalni kontrastni prag** (threshold) — minimalna promjena log-svjetline potrebna da piksel reagira

Dakle:
svaki piksel *pamti zadnju vrijednost L* i *emitira event* kad se promijeni za ±C.

---

## 🔹 Značenje praga C

* Prag ( C ) postavljaju **bias struje** u tranzistorima piksela.
* Te struje definiraju **osjetljivost** i **brzinu detekcije**.
* Prag se može softverski podesiti (tipično 10–50% promjene osvjetljenja).
* Niži prag → veća osjetljivost, ali i više šuma.
* Donja granica (~1%) postiže se samo pri jakom svjetlu i niskom šumu.

---

## 🔹 Povezanost s derivacijom svjetline

Ako su promjene male (tj. kratko vrijeme između dva eventa), promjenu svjetline možeš aproksimirati derivacijom (Taylorova ekspanzija):

[
L(x_k, t_k) - L(x_k, t_k - \Delta t_k) \approx \frac{\partial L}{\partial t}(x_k, t_k) , \Delta t_k
]

Ubacimo to u prethodnu formulu (1):

[
\frac{\partial L}{\partial t}(x_k, t_k) \approx \frac{p_k C}{\Delta t_k} \quad (3)
]

To znači da **frekvencija eventova (1/Δt)** indirektno kodira **brzinu promjene svjetline**.
Drugim riječima: više eventova u jedinici vremena = brža promjena u sceni.

---

## 🔹 Fizikalno značenje

* DVS ne mjeri **apsolutnu svjetlinu**, nego **promjene** u njoj.
* Klasična kamera daje “kadrove svjetline”, dok DVS daje “spikeove kontrasta”.
* To je *asinkrono mjerenje derivacije u vremenu*.

---

## 🔹 Povezanost s gibajućim rubovima

Ako pretpostavimo da je ukupna svjetlina scene konstantna, promjene svjetline proizlaze iz **kretanja rubova**.
Linearizacijom i primjenom *brightness constancy assumption* dobiješ:

[
\frac{\partial L}{\partial t} = -\nabla L \cdot v
]

* ( \nabla L = (\partial_x L, \partial_y L) ) je **gradijent svjetline** (smjer ruba).
* ( v = (v_x, v_y) ) je **brzina kretanja točke na slici**.

Dakle:

* Ako je gibanje **paralelno s rubom** ((v \perp \nabla L)) → nema promjene → nema eventa.
* Ako je gibanje **okomito na rub** ((v \parallel \nabla L)) → maksimalna promjena → mnogo eventova.

To objašnjava zašto DVS detektira **ruba u pokretu**, a ne teksture koje miruju.

---

## 🔹 Probabilistički model generiranja eventa

Idealna jednadžba (1) pretpostavlja savršen senzor bez šuma.
U stvarnosti postoje:

* **Slučajni šum** (shot noise u fotostruji)
* **mismatch** između tranzistora
* **varijacije praga** između piksela

Zbog toga je prag **stohastičan**, tj. nije uvijek točno C, nego varira oko njega prema **normalnoj raspodjeli**:

[
P(C) \sim \mathcal{N}(C, \sigma_C)
]
gdje je tipična širina distribucije (σ) oko 2–4% kontrasta.

---

## 🔹 Dodatni efekti

* **Refraktorni period:** kratko vrijeme nakon emitiranja eventa u kojem piksel *ignorira nove promjene* (ograničava brzinu).
* **Bus congestion:** kad previše piksela istovremeno šalje evente, nastaje “zagušenje” na sabirnici.
* **Fixed Pattern Noise (FPN):** varijacija praga i odziva između piksela (standardna devijacija 2–4%).

---

## 🔹 Zaključak

Event-based kamera:

1. Radi u log-svjetlosnoj domeni.
2. Generira event kad promjena svjetline prijeđe prag ( C ).
3. ( p_k ) označava polaritet (ON/OFF).
4. Derivacija svjetline ( \frac{\partial L}{\partial t} ) povezana je s frekvencijom eventova.
5. Eventi nastaju najviše na pokretnim rubovima, kad je ( v \parallel \nabla L ).
6. Prag ( C ) je stohastičan zbog šuma, a fizički ga ograničavaju bias struje, shot noise i osvjetljenje.

---



---

### **Napredne event kamere – sažetak ključnih točaka**

**1. Opći kontekst**

* Trenutno su dostupne samo kroz **znanstvene suradnje** s razvojnim timovima.
* Fokus istraživanja je na **proširenju funkcionalnosti**: boja, osjetljivost, dinamički raspon.

---

**2. Event kamere s bojom (Color event cameras)**

* Cilj: omogućiti *color vision* u event kamerama (kao kod ljudi i običnih kamera).
* **Rani pokušaji** koristili “*vertacolor principle*” (različite valne duljine svjetla različito prodiru u silicij).

  * Pionir: **Foveon senzori**.
  * Problem: **slaba separacija boja** (nema čiste razlike između R, G, B kanala).
* **Noviji pristupi:**

  * **Color Filter Arrays (CFA)** – integrirani RGB filteri iznad piksela.
  * **Color-splitter prizme** – optički razdvajaju boje na odvojene senzore.

    * Prednost: bolja separacija boja.
    * Mana: **veća cijena** i složenost.

---

**3. Povećana kontrastna osjetljivost (Higher Contrast Sensitivity)**

* Cilj: **detektirati manje promjene svjetline** (veća osjetljivost).
* Eksperimentalni senzori postigli osjetljivost do **~1% promjene osvjetljenja** (u laboratorijskim uvjetima).
* Tehnika:

  * Temeljeno na ideji **bolometra** – pojačanje signala *prije detektora promjene*.
  * To smanjuje **Fixed Pattern Noise (FPN)** i povećava preciznost detekcije.
* Problem: preamplifikacija zahtijeva **aktivnu kontrolu pojačanja** da se izbjegne zasićenje (“clipping”).
* Kompromis: **veća osjetljivost → manji dinamički raspon**.

---

**4. Ključna ograničenja**

* Trenutni napredni modeli su **eksperimentalni**, nisu komercijalno dostupni.
* Balans između **osjetljivosti, dinamičkog raspona i troška** još nije optimalno riješen.

---


---

### **Ekstrakcija informacija iz event podataka – sažetak ključnih točaka**

**1. Ključno pitanje:**
Kako izvući *značajne informacije* iz asinkronih, rijetkih i vremenski preciznih event podataka — ovisi o konkretnoj **aplikaciji** (npr. praćenje, rekonstrukcija, prepoznavanje).
To pitanje određuje **dizajn algoritma**.

---

**2. Svojstva event podataka:**

* **Asinkroni** – svaki piksel šalje event neovisno.
* **Sparse** – većina piksela u datom trenutku ne generira event.
* **Visoka vremenska rezolucija** i **niska latencija**.

---

**3. Dvije osnovne kategorije algoritama:**

| Kategorija                            | Opis                                                  | Latencija | Napomena                                  |
| ------------------------------------- | ----------------------------------------------------- | --------- | ----------------------------------------- |
| **(i) Event-by-event**                | Svaki dolazni event odmah ažurira stanje sustava      | Minimalna | Najniža latencija, ali veća složenost     |
| **(ii) Event-packet (grupne metode)** | Obrada blokova (paketa) događaja u vremenskom prozoru | Viša      | Uvodi kašnjenje, ali stabilniji rezultati |

*Napomena:*
Granica između kategorija nije stroga – prozori mogu “kliziti” po jedan event, pa se stanje može ažurirati i kontinuirano.

---

**4. Ključna spoznaja:**
Jedan event sam po sebi **nije dovoljan** za pouzdanu procjenu —
potrebno je dodatno znanje ili povijest prošlih događaja.

---

**5. Orijentacijska (ortogonalna) klasifikacija algoritama:**
Prema **načinu obrade događaja:**

| Tip pristupa                 | Opis                                                                            |
| ---------------------------- | ------------------------------------------------------------------------------- |
| **Model-based**              | Koristi fizikalne ili geometrijske modele (npr. optički tok, geometriju kamere) |
| **Model-free / Data-driven** | Uči reprezentacije iz podataka (npr. deep learning, ML pristupi)                |

---

**6. Prema tipu funkcije cilja (loss function):**

* **Geometrijska** – temelji se na položaju i pokretu točaka u prostoru.
* **Vremenska (temporal)** – koristi vremenski slijed i kašnjenja između eventova.
* **Fotometrijska** – temelji se na polaritetu i aktivnosti događaja (ON/OFF).

---

**7. Trenutni fokus istraživanja:**
Istražuju se prednosti i mane svake kategorije (event-by-event vs. group, model-based vs. ML) te kombinacije koje optimiziraju balans između **točnosti, brzine i robusnosti**.

---
KONCEPT POSITIVE I NEGATIVE EVENATA:
| Type           | Meaning            | Triggered when  | Color in visualization |
| -------------- | ------------------ | --------------- | ---------------------- |
| Positive Event | Pixel got brighter | ΔL ≥ +threshold | Green                  |
| Negative Event | Pixel got darker   | ΔL ≤ -threshold | Red                    |


Eventi se procesiraju i često se transformiraju u alternativne reprezentacije (npr. events in space time, event frames, time surface s timestampovima po pikselu, voxel grid, motion compensated event image, reconstrcted intensity image itd.)

---

### **1. Events in space–time (prostorno-vremenski događaji)**

* Svaki event se predstavlja trojkom *(x, y, t, p)* → pozicija, vrijeme i polaritet.
* Vizualno: “točkice” u 3D prostoru gdje je Z-os vrijeme.
* Koristi se za analizu *temporalne dinamike* (kretanje objekata, optical flow).
* To je najosnovnija forma — ništa agregirano, čista sirova temporalna informacija.

---

### **2. Event frame (akumulirani događaji u sliku)**

* Najjednostavnije: “broji” koliko se pozitivnih i negativnih događaja dogodilo u određenom vremenskom prozoru.
* Dobiješ 2D sliku (kao frame) gdje intenzitet piksela = broj događaja.
* Gubiš preciznu vremensku informaciju, ali možeš koristiti standardne CNN-ove.
* Korisno za vizualizaciju ili klasične detekcijske mreže.

---

### **3. Time surface**

* Svaki piksel sadrži **vrijeme posljednjeg događaja**.
* Dobiješ “mapu svježine” — noviji eventi imaju veće vrijednosti.
* Koristi se za *motion detection* i *feature tracking*, jer pokazuje gdje se *nedavno* nešto promijenilo.
* Može se eksponencijalno “zaboravljati” starije evente → time decay.

---

### **4. Voxel grid**

* Događaje rasporediš u 3D mrežu (x, y, vrijeme).
* Vremenska dimenzija se diskretizira u N binova (npr. 5–10 vremenskih slojeva).
* Dobiješ “3D tensor” koji CNN ili transformer može direktno obrađivati.
* Zlatni standard u deep-learning pristupima za event kamere (npr. EV-FlowNet, E2VID).

---

### **5. Motion-compensated event image**

* Pokušava “poravnati” događaje tako da izgleda kao da su snimljeni istovremeno.
* Radi *kompenzaciju gibanja* objekata ili kamere na temelju pretpostavljenog optic flow-a.
* Kad to ispravno napraviš, svi eventi od istog ruba poravnaju se → oštra rekonstruirana slika.
* Koristi se kod rekonstrukcije scene i odvajanja pozadine/predmeta u pokretu.

---

### **6. Reconstructed intensity image**

* Koristi sve događaje (često + početni “key frame”) da rekonstruira standardnu RGB ili grayscale sliku.
* Ideja: integrira promjene svjetline tijekom vremena.
* Koristi se u **E2VID** i sličnim mrežama koje rade “frame-like output” iz event streama.
* Super za situacije s visokim dinamičkim rasponom ili slabim osvjetljenjem.


Metode za event processing

Preprocessing (input adaptation)
Core processing (feature extraction and analysis)
Postprocessing (output creation)

U preprocessingu koristi se event packet
Motion-compensated event images se koriste u core processingu

Metoda obrade ovisi o tome kako su eventi reprezentirani i koji je hardver dostupan

| **Aspekt**                 | **Event-by-Event obrada**                                                | **Event-Packet obrada**                                                       |
| -------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| **Opis**                   | Svaki događaj se procesira individualno, odmah po dolasku.               | Događaji se grupiraju u vremenske pakete i procesiraju zajedno.               |
| **Tipične reprezentacije** | Sparse (rijetke) reprezentacije, vremenski točne (x, y, t, p).           | Dense reprezentacije poput event framea, voxel grida, time surfacea.          |
| **Hardverska platforma**   | Neuromorfni čipovi i SNN arhitekture.                                    | Standardni CPU/GPU procesori.                                                 |
| **Tipični algoritmi**      | Spiking neuronske mreže (SNN), deterministički i probabilistički filtri. | DNN-ovi, CNN-ovi, ručno dizajnirani feature extractori.                       |
| **Prednosti**              | Vrlo niska latencija, energetska učinkovitost, prirodno asinkrono.       | Jednostavnije za implementaciju, kompatibilno s postojećim ML frameworkovima. |
| **Nedostaci**              | Zahtijeva specijalizirani hardver i kompleksniju arhitekturu.            | Gubi vremensku preciznost i povećava latenciju.                               |
| **Tipične primjene**       | Real-time kontrola, robotika, edge sustavi, ultra-brzi odziv.            | Analiza scene, rekonstrukcija slike, učenje iz događajnih podataka.           |

---


---

## 🧠 Event-by-Event metode

### 🔹 1. Deterministički filteri

* **Primjeri:** prostorno-vremenske konvolucije, activity filteri.
* **Koriste se za:**

  * Redukciju šuma
  * Ekstrakciju značajki (feature extraction)
  * Rekonstrukciju slike
  * Filtriranje svjetline
* **Prednost:** savršeno prirodni za asinkrone podatke — omogućuju minimalnu latenciju i iskorištavaju svojstva senzora.

---

### 🔹 2. Probabilistički (Bayesovski) filteri

* **Primjeri:** Kalman filter, particle filter.
* **Koriste se za:**

  * Praćenje položaja i orijentacije (pose tracking) u SLAM sustavima.
* **Zahtijevaju dodatne informacije:**

  * Npr. grayscale slike, mapu scene ili povijesne evente.
* **Način rada:** svaki novi event uspoređuje se s postojećom "appearance" informacijom → razlika (innovation) ažurira stanje filtra.
* **Prednosti:** mogu kombinirati podatke iz više izvora i raditi s djelomičnim informacijama.

---

### 🔹 3. Višeslojni neuronski modeli (ANN / SNN)

* **Dvije glavne grane:**

  * **SNN (Spiking Neural Networks)** – prirodno procesiraju evente jedan po jedan.
  * **Klasične DNN mreže** – često trenirane na event-paketima, kasnije konvertirane u SNN.

---

### 🔹 4. Učenje i treniranje

* **Nesupervizirano učenje:**

  * Koristi se za ekstrakciju značajki (feature extraction).
  * Rezultat se često šalje u klasični klasifikator (npr. SVM).
  * Ipak, i dalje je potrebna određena količina označenih podataka (labeled data).

* **Supervizirano učenje:**

  * Ako ima dovoljno označenih podataka, može se direktno trenirati ANN/SNN bez dodatnog klasifikatora.
  * **Rezultat:** viša točnost nego kod nesuperviziranog pristupa.

---

### 🔹 5. Kombinirani pristupi

* Tijekom treniranja: koriste **pakete eventa** (frame-based deep learning).
* Nakon treniranja: model se pretvara u **SNN koji procesira evente jedan po jedan**.
* Ova kombinacija koristi prednosti i klasičnih GPU mreža i neuromorfnih sustava.

---

### 🔹 6. Glavne primjene

* **Klasifikacija objekata**
* **Prepoznavanje akcija / pokreta**
* **Embedded sustavi** – optimizirani za efikasnost i nisku latenciju, često koriste **custom SNN hardver**.

---

### 🔹 7. Trendovi i budući razvoj

* Povećan interes za:

  * **Supervizirano učenje direktno u SNN-ovima**
  * **Ugradnju takvih sustava u embedded uređaje** radi brzine i energetske učinkovitosti.

---

Naravno — ovo je jako bogat odlomak, pa sam ti izvukao **sve ključne koncepte i ideje** u pregledne, tematski grupirane natuknice u **markdown formatu**.
Sve bitno o **"Methods for Groups of Events"** (tj. grupnom procesiranju eventa) je ovdje sažeto i jasno 👇

---

## ⚙️ Methods for Groups of Events

*(Metode koje procesiraju više događaja zajedno — grupno, a ne pojedinačno)*

---

### 🔹 1. Osnovna ideja

* **Razlog:** pojedinačni eventi nose premalo informacija i puno šuma.
* **Rješenje:** grupiranjem više eventa postiže se bolji **signal-to-noise ratio**.
* **Proces:** više eventa se kombinira u **reprezentacije** poput:

  * event packet
  * event frame
  * time surface (TS)
  * voxel grid
* Takve reprezentacije omogućuju korištenje klasičnih CV (computer vision) metoda.

---

### 🔹 2. Event Frames

* Vrlo praktična reprezentacija jer omogućuje ponovnu upotrebu klasičnih CV alata.
* **Koristi se za:**

  * stereo viziju (dobri, ali skromni rezultati)
  * estimaciju položaja kamere (pose estimation)
  * optical flow (block matching)
  * input za DNN, SVM, Random Forest klasifikatore
* **Posebna prednost:** adaptivni frame rate (ovisno o sceni).
* **Napomena:** rijetki radovi uzimaju u obzir fotometrijsko značenje eventa (npr. promjenu svjetline).

---

### 🔹 3. Intensity Increment Images

* Koriste **inkremente svjetline** između događaja.
* **Primjene:**

  * praćenje značajki (feature tracking)
  * deblurring (odstranjivanje zamućenja slike)
  * praćenje kamere (camera tracking)

---

### 🔹 4. Time Surfaces (TS)

* **Opis:** mapa koja bilježi *vrijeme zadnjeg eventa po pikselu*.
* **Osjetljive su na:** rubove i smjer gibanja objekta.
* **Primjene:**

  * analiza gibanja i prepoznavanje oblika
  * iz TS-a se može izvesti **optical flow** (fitanjem ravnina kroz prostor-vrijeme)
  * ulaz za **CNN-e** koji računaju optical flow i brzinu
  * **corner detection** (Harris, FAST, ili noviji ML pristupi)
  * stereo vizija pomoću **temporalnog podudaranja** (event concurrence & timestamp similarity)
* **Problem:** degradacija performansi u teksturiranim scenama → **motion overwriting** (novi eventi brišu tragove starih).

---

### 🔹 5. Voxel Grids

* **Opis:** 3D volumetrijska reprezentacija (x, y, t).
* **Prednosti:** bolje čuva vremensku informaciju.
* **Nedostatak:** troši više memorije i računske snage.
* **Koristi se za:**

  * optical flow (varijacijska optimizacija)
  * DNN ulaze/izlaze s više kanala (multi-channel input/output)
* **Način obrade:**

  * konvolucije nad voxelima
  * optimizacija po kriteriju minimalne greške (objective function)

---

### 🔹 6. Korištenje konvencionalnih CV alata

* Kad se eventi pretvore u grid/frame formu — mogu se koristiti svi klasični alati:

  * **CNN feature extractori**
  * **Sličnosne metrike (cross-correlation, event alignment)** za:

    * klasifikaciju (SVM, CNN)
    * klasteriranje
    * detekciju pokreta (motion estimation)
* U **neuroscience** zajednici postoje i metrički pristupi koji rade direktno na *spikeovima* — bez konverzije u slike.

---

### 🔹 7. Deep Learning pristupi

* Koriste **DNN** nad različitim reprezentacijama:

  * event images
  * time surfaces (TS)
  * voxel grids
  * point sets
* **Primjene:**

  * klasifikacija
  * rekonstrukcija slike
  * predikcija kuta upravljanja (steering angle)
  * optical flow, depth, ego-motion estimacija
* **Supervizirano učenje:**

  * koriste *ground truth* (npr. pozu kamere, grayscale sliku)
  * mjere *photoconsistency*
* **Nesupervizirano učenje:**

  * koristi samo input evente (nema oznaka)
  * loss funkcije za to su istražene u [99]
* **Arhitektura:**

  * najčešće *encoder-decoder*
  * koristi samo konvolucije (manje parametara)
  * gubitak (loss) se može primijeniti na svaku razinu dekodera.

---

### 🔹 8. Motion Compensation

* **Ideja:** pronaći parametre gibanja koji najbolje "poravnaju" skup eventa u vremenu.
* **Prednost:** koristi *kontinuirani vremenski model* — iskorištava visoku temporalnu rezoluciju senzora.
* **Primjene:**

  * ego-motion estimacija
  * optical flow
  * procjena dubine
  * segmentacija pokreta
  * feature motion za VIO (Visual-Inertial Odometry)
* **Algoritmi:** koriste optimizacijske metode kao što su **Gauss-Newton** i **Conjugate Gradient**.

---

### 🔹 9. Odabir veličine grupe eventa

* Ključni **hiperparametar** – koliko eventa ulazi u jednu grupu.
* **Strategije odabira:**

  1. **Fiksni broj eventa**
  2. **Fiksno vrijeme promatranja** (konstantni frame rate)
  3. **Adaptivni pristupi** — npr. threshold prema gustoći eventa u regiji.
* **Trade-off:**

  * Fiksni broj eventa = jednostavno, ali ne uzima u obzir varijacije po slici.
  * Fiksno vrijeme = broj eventa se mijenja (nekad premalo, nekad previše).
  * Adaptivno = najbolje rješenje, ali složenije za dizajnirati.

---

* Dizajn event kamera temelji se na biološkim principima i računalnim primitivima, poput Spiking Neural Networks (SNN).
* DVS (Dynamic Vision Sensor) je inspiriran biološkim vizualnim putevima, posebno “transient” (privremenim) putevima koji obrađuju dinamičke vizualne informacije u “where” (gdje) putu.
* Transient put postoji kod mnogih životinja, uključujući ljude, i čini oko 30% ljudskog vizualnog sustava.
* Počinje s transient ganglijskim stanicama u retini (izvan fovee), zatim prolazi kroz magno slojeve talamusa i pod-slojeve područja V1, te završava u područjima MT i MST (dio dorzalnog puta, povezanog s prepoznavanjem pokreta).
* DVS senzor odgovara dijelu tog transient puta do razine retinalnih ganglijskih stanica.
* ATIS (senor koji bilježi i svjetlinu) generira grayscale događaje koji odgovaraju “sustained” ili “what” (što) putu kroz parvo slojeve mozga.

Transient - dio vizualnog sustava koji reagira na brze promjene i pokret u vidnom polju; obrađuje dinamičke informacije poput gibanja ili promjene kontrasta; brza, ali kratkotrajna reakcija.
Fovea - središnji dio mrežnice oka gdje je vidna oštrina najveća; sadrži gusto raspoređene čunjiće koji detektiraju boje; odgovorna za detaljno i precizno gledanje.
Magno slojevi talamusa - dio lateralnog genikulatnog tijela (LGN) u talamusu; obrađuju informacije o pokretu, kontrastu i svjetlini; povezani su s transient putem (gdje put).
V1 - primarno vidno područje u okcipitalnom režnju mozga; prvi korak obrade vizualnih informacija iz oka; analizira osnovne značajke slike kao što su rubovi, orijentacija i smjer kretanja.
MT - područje srednjeg temporalnog režnja (Middle Temporal area); specijalizirano za percepciju kretanja; sadrži stanice osjetljive na smjer i brzinu gibanja.
MST - područje medijalno od MT (Medial Superior Temporal area); obrađuje složenije oblike kretanja poput rotacije, ekspanzije i optičkog toka (npr. kretanje kroz prostor).
Ganglijske stanice - stanice mrežnice koje primaju signale od fotoreceptora (čunjića i štapića) i prosljeđuju ih mozgu putem vidnog živca; postoje različiti tipovi (npr. transient i sustained).
What put - ventralni (što) vizualni put; obrađuje informacije o obliku, boji i identitetu objekata; odgovoran za prepoznavanje i kategorizaciju onoga što vidimo.
Parvo slojevi mozga - parvocelularni slojevi LGN-a u talamusu; prenose informacije o boji i finim detaljima slike; povezani s what putem i sporijom, ali preciznijom obradom.

Umjetni neuroni, poput Leaky-Integrate and Fire ili Adaptivnih Eksponencijalnih su inspirirani neuronima pronađenima u vizualnom kortexu sisavaca
Oni su osnovne gradivne jedinice SNN-ova
Neuron prima input spikeove (evente) iz malog područja vidokruga (receptive field)
Spikeovi modificiraju membranski potencijal i stvaraju output spike (action potencijal) kada napon nadmaši threshold
Neuroni su povezani hijerarhijski i stvaraju SNN-ove
Spikeove mogu stvarati ili pikseli event kamere ili neuroni SNN-a

* Prvi slojevi vizualnih modela koriste receptive fields temeljene na **Difference of Gaussians** (osjetljivost na kontrast između središta i okoline), **Gabor filterima** (osjetljivost na orijentirane rubove) ili njihovim kombinacijama.
* Kako informacija prolazi dublje kroz mrežu, receptive fields postaju **sve složeniji**.
* U umjetnim neuronskim mrežama (ANN), obrada u unutarnjim slojevima često se **aproksimira konvolucijom**.
* U umjetnim spiking neuronskim mrežama (SNN), često se pretpostavlja da neuron **ne generira izlazne spikeove** ako nije primio ulazne spikeove iz prethodnog sloja.
* Ta pretpostavka omogućuje **preskakanje izračuna** za neaktivne neurone, čime se povećava učinkovitost.
* Rezultat vizualne obrade u takvim sustavima pojavljuje se **gotovo istovremeno s podražajem**, za razliku od klasičnih CNN-ova gdje se konvolucije računaju istodobno u svim točkama i u fiksnim vremenskim intervalima.

* Bio-inspirirani modeli koriste se za **niz niskorazinskih vizualnih zadataka**.
* **Event-based optical flow** može se izračunati pomoću **spatio-temporalno orijentiranih filtera** koji oponašaju rad receptive fields u primarnom vidnom korteksu.
* Ti isti filteri koriste se i za **spike-based modele selektivne pažnje**, temeljene na biološkim principima.
* **Modeli inspirirani binokularnim vidom** (s rekurzivnim lateralnim vezama te ekscitacijsko-inhibicijskim neuronskim vezama) primijenjeni su za **event-based stereo korespondenciju** i **kontrolu konvergencije očiju kod humanoidnih robota**.
* Vizualni korteks poslužio je kao inspiracija za **hijerarhijski model ekstrakcije značajki**, implementiran u SNN-ovima i korišten za **prepoznavanje objekata**.
* Učinkovitost takvih mreža raste ako **bolje iskorištavaju precizno vremensko usklađivanje spikeova**.
* Rani modeli bili su **ručno dizajnirani** (npr. pomoću Gabor filtera), dok noviji koriste **učenje temeljeno na STDP-u (Spike-Timing Dependent Plasticity)** za samostalno formiranje receptive fields, što daje bolje rezultate.
* Novija istraživanja uključuju i **supervizirane metode učenja** poput **backpropagationa** za implementaciju **spiking dubokih konvolucijskih mreža**.
* Prednosti bio-inspiriranih metoda u odnosu na klasične: **niža latencija** i **veća učinkovitost**.
* **Vid kukaca** također je izvor inspiracije — razvijeni su **event-based sustavi za izbjegavanje prepreka i brzo prepoznavanje meta** u malim robotima, temeljeni na neuronima koji reagiraju na nadolazeće objekte i pokreću **reflekse izbjegavanja**.


Primjene:
	Low-level:
		- detekcija značajki
		- praćenje objekata
		- optical flow estimation
	3d scene structure related:
		- procjena dubine
		- vizualna odometrija
		- intensity image reconstruction
	Higher-level:
		- segmentacija gibanja
		- prepoznavanje i povezivanje percepcije s kontrolom pokreta
		
* **Detekcija i praćenje značajki** ključni su elementi mnogih vizualnih zadataka poput **vizualne odometrije** (Odometrija je metoda za **mjerenje prijeđenog puta i položaja u prostoru** na temelju informacija o **kretanju senzora ili kamere**.

U kontekstu **vizualne odometrije**, to znači da se **računa koliko se kamera (ili robot) pomaknula** analizom promjena u slikama — dakle, prati se kako se točke u okolini pomiču između kadrova ili događaja, pa se iz toga procijeni **putanja i orijentacija**.
), **segmentacije objekata** i **razumijevanja scene**.
* **Event kamere** omogućuju **asinkrono praćenje** koje se prilagođava dinamici scene, uz **nisku latenciju**, **velik dinamički raspon** i **malu potrošnju energije**.
* Time se omogućuje **praćenje i tijekom “slijepog vremena”** između okvira standardne kamere.
* Za to je potrebno razviti metode koje uzimaju u obzir **prostorno-vremenske** i **fotometrijske** karakteristike event podataka, jer oni bilježe samo **promjene svjetline**.
* **Glavni izazovi:**

  * Promjene u izgledu scene uzrokovane **ovisnošću o smjeru gibanja**, što otežava detekciju i praćenje značajki.
  * Potreba za **povezivanjem događaja kroz vrijeme** (data association) unatoč promjenama izgleda.
  * **Šum senzora** i **event clutter** (višak događaja) uzrokovan **pokretom kamere**.

* **Rani event-based algoritmi** za detekciju značajki bili su vrlo jednostavni i služili su za demonstraciju **niske latencije** i **male računske složenosti** event sustava.
* Pretpostavljali su **statičnu kameru** i pratili **pokretne objekte** kao skupove događaja (blobs), **krugove** ili **linije**.
* Obrada se radila samo na pikselima koji su generirali događaje.
* **Gaussian filteri** i **mješavine Gaussovih funkcija** koristili su se za detekciju i praćenje takvih blobova.
* Svaki novi događaj bio je **povezan s najbližim postojećim blobom** i asinkrono je **ažurirao njegove parametre** (poziciju, veličinu, itd.).
* Ovi pristupi korišteni su u **nadzoru prometa**, **praćenju robota visoke brzine** i **praćenju čestica u tekućinama ili mikrorobotici**, ali su **ograničeni na jednostavne oblike**.
* Kasnije su razvijene metode za **praćenje složenijih, visokokontrastnih oblika**, temeljene na algoritmima kao što su **ICP (Iterative Closest Point)**, **gradient descent**, **Mean-Shift**, **Monte Carlo metode** i **particle filtering**.
* **Iterativne metode** (npr. ICP) koristile su **najbližeg susjeda** za povezivanje događaja s ciljanim oblikom i ažuriranje njegove transformacije, omogućujući **vrlo brzo praćenje (do 200 kHz)**.
* Drugi radovi koristili su **rotirane i skalirane verzije oblika (kernels)** s ugrađenim mehanizmom **odbijanja** kako se ne bi preklapali.
* **Složeni objekti** poput lica ili tijela praćeni su pomoću **modela sastavljenih od više dijelova** povezanih elastičnim “opružnim” vezama koje simuliraju fizički sustav.
* Većina metoda tretira događaje kao **pojedinačne točke bez polariteta** i ažurira stanje sustava **asinkrono**, s vrlo **malom latencijom**.
* Uspješnost metoda ovisi o **finoj prilagodbi parametara**, koji se obično podešavaju **eksperimentalno** za određeni objekt.
* Ove metode traže **prethodno znanje ili korisnički unos** o tome što se prati, što je pogodno za specifične zadatke (npr. automobili ili lopte), ali nije praktično za općenite scene.
* Noviji pristupi definiraju **realističnije značajke** temeljene na **lokalnim rubnim uzorcima** (edge patterns), predstavljene kao skupovi točaka.
* Dolazni događaji se s njima **usklađuju pomoću ICP-a**.
* Neki pristupi koriste **klasične detektore i trackere** na **motion-compensated event slikama**, što daje dobre rezultate u prirodnim scenama i omogućuje **procjenu vlastitog gibanja (ego-motion)**.
* Značajke izvedene iz **motion-compensated događaja** pružaju dobru reprezentaciju rubova, ali su **ovisne o smjeru kretanja**, pa s vremenom dolazi do **drifta (odmicanja praćenja)**.
* Za **praćenje bez drifta** potrebne su **motion-invariant značajke** koje nisu osjetljive na promjenu smjera kretanja.



* **Kombinacija događaja i frameova** (npr. kod senzora poput **DAVIS-a**) omogućuje **jednostavnije povezivanje podataka (data association)**, jer su dostupne **apsolutne vrijednosti svjetline** — dakle, “mapa” značajke ne ovisi o smjeru kretanja.
* Ovi pristupi koriste **prednosti oba svijeta**: stabilnost i kontekst frameova + brzinu i nisku latenciju event podataka.
* Algoritmi automatski **detektiraju rubne uzorke (edge patterns)** na frameovima, a zatim ih **asinkrono prate događajima**.
* **Pozicija značajke** dobiva se pomoću **Harris corner detektora**, a **deskriptor značajke** temelji se na **rubovima oko tog kuta**.
* U nekim metodama (npr. [125], [126]) **Canny rubovi** se pretvaraju u **skupove točaka (templates)** koje se koriste za **ICP praćenje** — pretpostavlja se da se događaji javljaju **na jakim rubovima**.
* U radu [64], rubni uzorci se temelje izravno na **intenzitetima framea**, a praćenje se provodi tako da se traže **parametri gibanja** koji **minimiziraju fotometrijsku pogrešku** između događaja i predviđene slike iz generativnog modela.
* Usporedba pet metoda praćenja (iz [64]) pokazuje da **generativni model** daje **najveću točnost (čak i sub-pikselnu)**, ali je **računski zahtjevan**.
* Ključno otkriće: **frameovi nisu nužni** — mogu se **rekonstruirati iz samih događaja**, a rezultati detekcije i praćenja ostaju **gotovo jednako dobri**.

Ukratko:
→ **Spajanje event + frame podataka** daje točno, robusno i brzo praćenje značajki.
→ **Generativni pristupi** nude najbolju preciznost.
→ **Event-only sustavi** mogu postići slične rezultate rekonstrukcijom frameova iz događaja — što otvara put potpuno **frame-free sustavima**.

* **Event kamere** prirodno reagiraju na **rubove** u sceni, što ubrzava **detekciju nižerazinskih značajki** poput **ključnih točaka (keypoints)** ili **kutova (corners)**.
* Takve točke omogućuju **pouzdano praćenje** jer ne pate od **aperture problema** i služe kao lokalni orijentiri za ekstrakciju značajki.
* Metoda iz [186] detektira kutove kao **sjecišta dvaju pokretnih rubova**, dobivenih **aproksimacijom ravnina** u **prostorno-vremenskom toku događaja**.

  * Za ublažavanje šuma koristi se **least-squares + RANSAC-slična metoda uzorkovanja**.
  * Ta lokalna aproksimacija ravnina korisna je i za **procjenu optičkog toka** i **trajanja događaja** (event lifetime).
* Razvijene su i **event inačice poznatih detektora kutova**, poput **Harris** i **FAST**, koje rade nad **time surface (TS)** reprezentacijom događaja.

  * U [114] se **TS binarizira**, pa se na nju primjenjuju **derivacijski filtri Harris detektora**.
  * U [115] se derivacijski filtri zamjenjuju **piksel-po-piksel usporedbama** na **dvije koncentrične kružnice** oko događaja; kutovi se detektiraju tamo gdje **TS pokazuje dvije odvojene regije** (nova vs. stara događanja).
* **[111]** poboljšava ovaj pristup i uvodi **praćenje kutova** — pretpostavlja da kutovi prate **kontinuirane putanje**, a povezuju se po **blizini** pomoću **grafova hipoteza**.
* Glavni problem TS-baziranih metoda: **ovisnost o smjeru gibanja**, jer promjena smjera mijenja izgled TS-a.
* **[112]** uvodi **data-driven pristup** — uči izgled TS-a za kutove koristeći **nadzirano učenje** (labeliranje prema sivim slikama iz DAVIS/ATIS kamere).

  * Kao kompromis između točnosti i brzine koristi se **random forest klasifikator**.
* **Kutovi iz događaja** imaju praktične primjene u **vizualnoj odometriji** i **segmentaciji vlastitog gibanja (ego-motion segmentation)**, iako ih je zasad **relativno malo primijenjenih rješenja**.

* Opisane metode zahtjevaju da točno znamo ča pratimo + još se traži neki standardni način evaluacije performansi

Optical flow estimation
Izračun brzine objekata na image planeu bez da znamo išta o geometriji scene ili samom kretanju objekta
Pokušava izračunati brzinu kretanja piksela između 2 framea (kako se svjetlina piksela mijenja)
Problem: samo iz promjene svjetline ne možemo znati kako se objekt stvarno kreće
Ne znamo stvarnu brzinu ni smjer (aperture problem)
Treba nam neka regularizacija (npr. pretpostavka da se susjedni pikseli miču sličnu, da se brzina glatko mijenja, da se svjetlina ne mijenja tijekom kretanja itd.)

Kod standardnih frame based kamera optical flow saznajemo iz analize 2 uzastopna framea (dobijemo prostorne (promjena svjetline u prostoru) i vremenske derivacije(promjena svjetline u vremenu))
U kombinaciji s:

Pretpostavkom konstantne svjetline (brightness constancy assumption - piksel zadržava istu svjetlinu dok se kreće)

Pretpostavkom glatkoće (susjedni pikseli imaju sličan flow)

Daje dovoljno jednadžbi za izračun flowa u svakoj točki slike.

Event kamere:

Ne daju apsolutnu svjetlinu — samo događaje (evente) kad se promijeni svjetlina.

Podaci nisu kontinuirani u prostoru — samo diskretni eventi (x, y, t, polaritet).

Jedan event sam po sebi ne nosi dovoljno informacija da se izračuna flow.
Moraš grupirati više evenata (u vremenu i prostoru) da dobiješ procjenu smjera i brzine.

Postavlja se pitanje:
“Gdje u x-y-t prostoru uopće računati flow?”

Idealno: flow polje kroz cijeli prostor (skupo!).

U praksi: računa se na lokacijama evenata ili na umjetno odabranim vremenskim presjecima.

Prednosti event-based flowa:

Eventi predstavljaju rubove (edges) — mjesta gdje je kretanje najmanje dvosmisleno.

Imaju vrlo precizno vremensko označavanje (timestamp) → mogu mjeriti vrlo brze pokrete.

Cilj istraživanja:
Napraviti biološki plauzibilan algoritam, tj. da imitira obradu pokreta u vizualnom korteksu primata (V1, MT) i da se može efikasno izvesti na neuromorfnom hardveru.

Raniji radovi pokušavali su primjeniti klasične CV pristupe na event based podatke
Utemeljeno na pretpostavci o konstantnom osvjetljenju
Diskusija o tome imaju li pojedini eventi u sebi dovoljno info. za procjenu flowa

---

##  **Optical Flow u event-based viziji — sažetak ključnih ideja**

---

###  **1. Osnovni problem**

* Cilj: Izračunati **brzinu kretanja objekata** u ravnini slike — **bez poznavanja geometrije scene**.
* Problem je **ill-posed** → nema dovoljno informacija, pa se mora **regularizirati** (dodati pretpostavke).

---

###  **2. Razlike naspram klasičnih metoda**

* Klasične metode koriste **prostorne i vremenske derivacije svjetline (Lx, Ly, Lt)** i **pretpostavku konstantne svjetline**.
* Kod **event kamera**, nema apsolutne svjetline ni kontinuiranih podataka → teško je dobiti stabilne derivacije.
* Rješenje: **agregirati više evenata** kroz prostor i vrijeme da bi se procijenio pokret.

---

###  **3. Geometrijski pristupi — timesurface & plane fitting (npr. metoda [21])**

* Promatra se **lokalna distribucija evenata** u 3D prostoru (x, y, t).
* Kako se rub (edge) miče, generira **timesurface** (površinu u prostoru-vremenu).
* **Nagib površine (slope)** u x-t i y-t presjecima daje smjer i brzinu kretanja.
* Flow se računa **fittingom ravnine (plane fitting)** na lokalni skup evenata → koeficijenti ravnine = komponente brzine.
* Dobiva se **normalni flow** (okomit na rub).
* Kvaliteta ovisi o veličini lokalne regije:

  * premala → nepouzdan fit
  * prevelika → gubi se lokalnost.

---

###  **4. Biološki inspirirani pristupi**

* Metoda inspirirana **vizualnim sustavom primata** (V1–MT).
* Koristi **spatio-temporalne filtre** (poput **Gabor filtera**) za detekciju:

  * različitih **brzina** i **smjerova** gibanja
  * uz **rijetku (sparse)** reprezentaciju evenata.
* Filtri djeluju kao **korelacijski detektori pokreta**.
* Primjeri:

  * SNN s **odgodom signala** kroz sinapse → neuroni kao **coincidence detektori**

    * osjetljivi na **8 brzina × 8 smjerova = 64 vektora brzina**
    * receptive field: 5×5 piksela
    * moguće implementirati na **neuromorfnom hardveru** (low-power, real-time)
  * postoji i metoda koja koristi **STDP (Spike-Timing-Dependent Plasticity)** za *učenje filtera iz event podataka*
  * u drugim metodama postoje ručno dizajnirani filteri, ali konceptualno jednaki princip.

---

###  **5. Gabor + Event frame pristupi (klasična signalna obrada)**

* Metoda:

  * Pretvara evente u **event frame** (projekciju događaja).
  * Primjenjuje **Gabor filter bank** → dobiva **fazu**.
  * Optical flow = **gradijent faze** filter banke.
  * Ograničenje: može izračunati samo **komponentu brzine u smjeru gradijenta** (zbog aperture problema).

---

###  **6. Kombinirani pristupi — optical flow + druge veličine**

* metode procjenjuju optical flow **zajedno s intenzitetom slike** (brightness).

  * Koriste više jednadžbi (brightness constancy, smoothness, penalizacija, varijacijski pristup).
  * Cilj: pronaći **flow + intenzitet** koji **najbolje objašnjava distribuciju evenata**.
  * Rezultat: **gusto (dense)** flow polje (vrijednost za svaki piksel).
  * Flow u zonama bez evenata je **manje pouzdan** (jer proizlazi samo iz glatkoće).

---

###  **7. Block-matching pristupi (video encoding analogija)**

* računa optical flow uspoređujući **dva skupa evenata (“blokove”)**.

  * Pretvara ih u **event frameove** na adaptivnoj stopi.
  * Mjeri sličnost blokova (npr. suma apsolutnih razlika).
  * Radi u stvarnom vremenu, može se implementirati na **FPGA-u** (velika efikasnost, manja preciznost).

---

###  **8. Motion compensation i “sharpness maximization”**


  * Warpaju (transformiraju) *cuboid* evenata tako da budu oštriji (motion-compensated images).
  * Maksimiziraju **oštrinu slike** → time pronalaze pravilan smjer gibanja.
  * Ponašaju se kao **adaptivni filteri** koji uče optimalnu spatio-temporalnu orijentaciju.

---

###  **9. Deep learning pristupi**

* Pojavom većih datasetova + DAVIS senzora:

  *  **Encoder-decoder CNN**, treniran **self-supervised**, koristi **time surfaces + event frames**.

    * Loss = greška između grayscale frameova poravnatih pomoću predviđenog flowa.
    * Može predvidjeti gusti flow samo iz evenata.
  * prva **monokularna ANN arhitektura** koja istodobno uči:

    * **gusti optical flow**,
    * **dubinu (depth)** i
    * **ego-motion** (vlastito gibanje kamere).
    * Ulaz: višeslojni eventi (frames + TS s prosječnim timestampovima).
    * Trenirano **unsupervised**, koristi **motion compensation loss**.
  *  postoje i metode koje su također unsupervised, ali koriste **time-surface loss**.

---

###  **10. Evaluacija & izazovi**

* Optical flow = **računski skup zadatak**:

  * Deep metode → zahtijevaju **GPU**.
  * Lakše metode → **manje točne**, ali real-time.
* Nekoliko metoda je implementirano u **hardverskoj logici** za **minimalnu latenciju**.
* Nedostatak:

  * **Nema dovoljno datasetova s točnim ground truth flowom** u različitim uvjetima (tekstura, brzina, parallax, svjetlo itd.).
  * Teško dobiti **realne ground truth podatke** — pogotovo za pokretne objekte koji se ne kreću istim smjerom kao kamera.
* Zaključak:

  * Potrebna **standardizacija evaluacijskih metoda** i **kvantitativna usporedba** postojećih pristupa.
  * Cilj: pronaći ključne ideje koje vode prema **efikasnijem i točnijem optical flowu iz evenata**.

---

3D rekonstrukcija (MONO I STEREO)
Firstly, zabija san koja je razlika između mono i stereo, pa ću pitat Gepetta

Monocular ANN (npr. [153]) → koristi samo jedan event senzor, ali uči dubinu i pokret kroz vrijeme.

Stereo event kamera (npr. DVS stereo setup) → koristi dva event senzora i može direktno dobiti disparity + depth iz sinkroniziranih evenata.

 Mono vs. Stereo u kontekstu kamera i vizije
 Monokularni sustav (mono)

Koristi jednu kameru.

Gleda svijet iz jedne perspektive → nema direktnu informaciju o dubini (koliko je nešto daleko).

Sve što može vidjeti su projekcije 3D točaka na 2D sliku.

Da bi procijenio dubinu, mora “nagađati” pomoću:

gibanja kamere (motion parallax),

perspektive (veličine objekata),

naučenih uzoraka (deep learning).

Tipično koristi se kod:

ego-motion estimacije (koliko se kamera sama pomaknula),

monokularne depth estimacije (predviđa dubinu “naučeno” iz podataka),

SLAM (monokularni varijant koristi samo jednu kameru i temporalne tragove).

 Ukratko: jeftinije, jednostavnije, ali dubina nije direktno mjerljiva — mora se procjenjivati.

 Stereoskopski sustav (stereo)

Koristi dvije kamere postavljene jedna pored druge (poput naših očiju 👀).

Obje vide istu scenu iz malo različitih kutova.

Time se može izračunati paralaksna razlika (disparity) → razlika u poziciji iste točke na dvije slike.

Iz disparityja se izravno dobiva dubina (Z-koordinata) pomoću jednostavne geometrije.

Stereo sustavi su idealni za:

depth map rekonstrukciju,

3D scene understanding,

autonomnu vožnju, robote itd.

 Ukratko: skuplje i složenije za kalibraciju, ali daju preciznu 3D dubinu u realnom vremenu.

 Sažetak razlika
Značajka	Monokularni	Stereoskopski
Broj kamera	1	2 (ili više)
Dubina	Neizravno, procjenjuje se	Izravno, iz geometrije
Kalibracija	Jednostavna	Potrebna precizna stereo kalibracija
Trošak	Manji	Veći
Primjeri upotrebe	Mobilni telefoni, monokularni SLAM	Autonomna vozila, 3D rekonstrukcija, industrijski roboti

Stereo direktno more skužit dubinu, mono ne more nikako


---

###  **Instantaneous Stereo (s event kamerama)**

* Cilj: **Procjena dubine (3D rekonstrukcija)** pomoću **dva ili više sinkroniziranih event kamera**.
* Rekonstrukcija se radi u **vrlo kratkom vremenu** — idealno **po svakom eventu**.
* Kamere su **rigidno spojene** i **sinkronizirane** → dijele **zajednički sat (clock)**.

---

### **Klasična dvostupanjska stereo metoda:**

1. **Event correspondence problem** — pronaći koji event s jedne kamere odgovara eventu s druge (tzv. **epipolar matching**).
2. **Triangulacija** — iz tih parova izračunati 3D položaj točke.

---

###  **Glavni izazov:**

* **Pronalaženje korespondencija** između eventova → vrlo **računalno zahtjevno**.

---

###  **Načini podudaranja (matching):**

* (i) Korištenje **klasičnih stereo metrika** poput:

  * *Normalized Cross-Correlation (NCC)*
  * primijenjeno na **event frameove** ili **time surfaces**.
* (ii) **Iskorištavanje vremenske simultanosti i korelacija** između senzora.

---

###  **Dodatne značajke metoda:**

* Pristup je **lokalan** — uspoređuju se **susjedstva eventova**, jer pojedini timestamp nije dovoljan za podudaranje.
* Dodaju se **ograničenja** kako bi se smanjila dvosmislenost:

  * **Epipolarno ograničenje**
  * **Redoslijed događaja (ordering)**
  * **Jedinstvenost (uniqueness)**
  * **Orijentacija rubova (edge orientation)**
  * **Polarnost (polarity)**

---

###  **Poboljšanja:**

* Radi se i **usporedba lokalnih deskriptora** koji opisuju **prostornu raspodjelu eventova** na obje slike.

---
Global Approaches for Event-Based Stereo Depth Estimation
Osnovna ideja:

Globalni pristupi daju točnije i manje dvosmislene procjene dubine od lokalnih.

To postižu dodavanjem regularizacijskih ograničenja (regularity constraints).

 Ključne metode i inspiracija:

Temelje se na proširenju Marr & Poggio cooperative stereo algoritma za event kamere.

Uključuju mrežu neurona osjetljivih na disparitet koji:

primaju evente s obje kamere

provode operacije poput pojačanja (amplification) i inhibicije (inhibition)

implementiraju ograničenja podudaranja:

jedinstvenost (uniqueness)

kontinuitet (continuity)

rezultat je globalno optimalno rješenje nakon iterativnih nelinearnih operacija.

 Ostale globalne metode:

Korištenje Belief Propagation na Markov Random Field (MRF) modelima.

Semi-global matching tehnike.

Sve se temelje na optimizaciji — definiranju energetske funkcije čiji je minimum ispravna mapa korespondencija.

 Prednosti i kompromisi:

Veća robusnost i manja osjetljivost na dvosmislenosti od lokalnih metoda.

Cijena: veća računalna složenost (više resursa i vremena).

 Ostali doprinosi i eksperimenti:

U [214] predložen je brute-force space-sweeping pristup na GPU-u:

Dubina se očituje kao “in-focus” voxeli u Disparity Space Image.

Drugi pristupi koriste neuromorfne procesore → niska potrošnja (100 mW), visoka brzina (1 kHz).

Još nije kvantificiran trade-off između točnosti i efikasnosti.

 Ograničenja eksperimentalnih radova:

Testovi uglavnom na statičnim kamerama i jednostavnim scenama (malo pokretnih objekata).

Time se olakšava traženje korespondencija zbog manje “šuma” u eventima.

 Zaključak:

Event kamere omogućuju brze (1 kHz), energetski učinkovite i precizne 3D rekonstrukcije,
posebno pogodne za pokretne objekte i nezačepljene (uncluttered) scene.

Multi-perspective panoramas:
Cilj: Instantaneous stereo → dobivanje dubinskih mapa (depth maps) u vrlo kratkim vremenskim intervalima.

Razlika od standardnog instant stereo: kamere nisu sinkronizirane, tj. događaji se ne bilježe u isto vrijeme.

Metoda koristi kontrolirani hardverski setup: dvije rotirajuće event kamere s poznatom putanjom/motion.

Takav setup omogućuje:

(i) Rekonstrukciju intenzitetskih slika (brightness images)

Na tim slikama se zatim može primijeniti klasični stereo algoritam.

Ukratko:
Umjesto dvije paralelne, sinkronizirane kamere, koristi se konfiguracija s rotacijom i poznatom putanjom kamera da bi se dobile dubinske informacije čak i kad kamere ne snimaju u isto vrijeme. Ovo omogućuje panoramske i multi-perspektivne dubinske rekonstrukcije.

Monocular depth estimation
Koristi se 1 event kamera
Ne može se uočiti temporal correlation između evenata kroz više image planesa
Potrebna je semi-dense 3d rekonstrukcija scene (3D edge map) => intergracija informacija iz evenata dobivenih iz kamere koja se micala kroz vrijeme (zato nam treba info o tome kako se kamera micala)
Kombinacija: pozicija event kamere + 3d mapa scene + intenzitet slike

Intenzitet slike (brightness image) nije nešto što event kamera izravno bilježi u obliku “klasične slike” (jer ona registrira samo promjene svjetline, tj. evente).

Ovdje intenzitet slike znači aproksimaciju ili rekonstruiranu sliku svjetline scene u tom trenutku, koju se može koristiti za klasične stereo algoritme.

Drugim riječima:

Eventi daju samo promjene svjetline (delta),

Pozicija kamere + prethodni eventi + model scene → može se “napuniti” slika s intenzitetom piksela koja je najbliža onome što bi obična kamera snimila.

Ta rekonstruirana slika ne prikazuje pokrete kao događaje, već apsolutnu svjetlinu svakog piksela, što omogućuje primjenu klasičnih stereo metoda (poput epipolar matching, block matching).

Ukratko: intenzitet slike = rekonstruirana “klasična” slika iz event streama, koja sadrži apsolutnu svjetlinu piksela za trenutni snapshot scene.

* **Stereo Depth za SLAM:**

  * Nova metoda inspirirana **small-baseline multi-view stereo**.
  * Dobiva **semi-dense 3D rekonstrukciju scene** optimiziranjem **lokalne spatio-temporalne konzistentnosti eventa** preko slika (time surfaces).
  * Ne koristi klasični pristup **event matching + triangulacija**, već **forward-projection** za procjenu dubine bez eksplicitnih korespondencija eventa.
  * Omogućuje primjenu prednosti **event kamera u stereo SLAM** sustavima, npr. autonomna vozila.

* **Procjena dubine koristeći strukturirano svjetlo (Structured Light):**

  * Aktivne metode: emitiraju svjetlo i mjere refleksiju event kamerom.
  * Primjer: **DVS + pulsni laserski linijski skener** → brza 3D rekonstrukcija terena (3D line scanner).
  * **Motion Contrast 3D scanning:** visoka rezolucija, brzina i robusnost u izazovnim uvjetima (jako osvjetljenje, reflektivne ili pokretne površine).
  * Aktivni sustavi koriste **visoku vremensku rezoluciju i suppression redundancije** event kamera.
  * Ograničenje: specifične primjene i moguće sigurnosne zabrane (ovisno o laserskoj snazi).

* **Opportunities / izazovi:**

  * Teško je usporediti metode jer nisu evaluirane na istim datasetovima.
  * Potrebno:

    * Sveobuhvatan **dataset i testbed** za event-based depth evaluaciju.
    * Benchmarking postojećih metoda radi usporedbe performansi.


* **Izazov:**

  * Konvencionalne metode za kamere (feature detection, matching, iterative alignment) **ne rade** s event kamerama.
  * Potrebno je razviti **nove SLAM tehnike** koje koriste prednosti event kamera: **niska latencija, asinkrono ažuriranje stanja** po svakom eventu.

* **Karakteristike event-based SLAM:**

  * Svaki event **ne sadrži dovoljno informacija** za procjenu stanja od nule (npr. 6-DOF kamera).
  * Cilj: svaki event **asinkrono ažurira stanje sustava**.
  * Popularni pristupi: **probabilistički/Bayesian filtri**, prilagođeni event generation procesu.

* **Mapiranje scene:**

  * Većina mapa iz event-based SLAM sustava su **semi-dense maps** → samo rubovi scene.
  * Event kamera mjeri **temporalne promjene**, ne direktno intenzitet.
  * Potrebno je **procijeniti prisutnost, orijentaciju i jačinu rubova** zajedno s kretanjem kamere.
  * Jačina intenziteta rubova korelira s **firing rate** eventa → pouzdano praćenje.

* **Kompleksnost problema:**

  * Tri osi kompleksnosti:

    1. **Dimenzionalnost problema** (3-DOF vs. 6-DOF)
    2. **Tip kretanja** (rotacija, planarno, slobodno 6-DOF)
    3. **Tip scene** (umjetna vs. prirodna, photometry i struktura)
  * Literaturu dominiraju metode koje prvo rješavaju **lokalizaciju/motion estimation**, jer je jednostavnija.
  * Neke metode zahtijevaju dodatne senzore (RGB-D), ali to uvodi **latenciju i motion blur**.

* **Cilj istraživanja:**

  * Postepeno rješavanje problema s **rastom kompleksnosti** scena i kretanja.
  * Razvoj metoda koje omogućuju **full 6-DOF SLAM u prirodnim 3D scenama** koristeći event kamere.

Radi se o **praćenju položaja (pose tracking)** pomoću **event kamera**.
Cilj je znati **kako se kamera (ili robot) kreće kroz prostor**, koristeći samo događaje (events) umjesto običnih frameova.

---

### 📘 Glavne metode iz teksta

1. **Prva metoda ([101])**

   * Koristi **particle filter** (statistički model) za praćenje kretanja robota.
   * Scena je **plosnata (planarna)** i sadrži **crno-bijele linije**.
   * Glavna inovacija: **likelihood funkcija** računa vjerojatnost da su detektirani eventi u skladu s trenutnim položajem robota.
   * To radi usporedbom između **mjesta eventa i najbližeg ruba** u mapiranoj sceni (reprojection error).

2. **Druga metoda ([75])**

   * Kombinira **standardnu grayscale kameru** i **DVS (event kameru)**.
   * Koristi **Bayesov filter** za procjenu malih pomaka između događaja i prethodnog framea s obične kamere.
   * Ograničeno na **planarno kretanje** i **crno-bijele scene**.
   * Likelihood funkcija proporcionalna je **jačini gradijenta slike** na lokaciji eventa → što je jači rub, veća vjerojatnost da event ima smisla.

3. **Treća metoda ([227])**

   * Radi **pose tracking** pod **planarnim i ne-holonomnim kretanjem** (znači kretanje s ograničenjima, kao auto ili robot s kotačima).
   * Podržava **loop closure** (zatvaranje petlje) i **topološki točne trajektorije**.
   * Pretvara **evente u frameove** i onda koristi klasični **SeqSLAM** algoritam (poznat iz vizualne navigacije) da prepozna poznate lokacije.

---

### 🧠 Ukratko u 3 natuknice:

* Sve metode pokušavaju **procijeniti položaj kamere (pose)** koristeći **evente umjesto klasičnih frameova**.
* Koriste **statističke filtre (particle / Bayesian)** i pametno dizajnirane **likelihood funkcije** koje procjenjuju koliko su eventi konzistentni s mapom.
* Neke metode čak **kombiniraju event kameru s običnom kamerom** ili **pretvaraju evente u frameove** da iskoriste postojeće SLAM tehnike (npr. SeqSLAM).

---

znači mi imamo k događaja i njihove pozicije i cilj je skužiti kako se objekt kretao na temelju promjene položaja događaja?

Bravo! 💥 Točno to!
Pogodio si srž cijelog koncepta **pose trackinga s event kamerama**.

Event kamera ti ne daje frameove kao klasična kamera, nego niz **događaja (events)**:
👉 svaki event = `(x, y, t, polarity)` → lokacija piksela, vrijeme, i smjer promjene svjetline.

---

### 🔍 Cilj:

Na temelju **tih događaja kroz vrijeme** želiš **procijeniti kako se kamera (ili objekt) pomicala**.
Drugim riječima, gledaš **kako se uzorak događaja “pomaknuo”** između trenutaka → to ti otkriva **translaciju, rotaciju i orijentaciju** kamere.

---

### 🧩 Kako to funkcionira (intuicija):

1. **Eventi nastaju kad se nešto pomakne** → znači događaji već implicitno sadrže info o pokretu.
2. Ako imaš **mapu scene** (npr. gdje su rubovi, linije, kontrasti), možeš izračunati:

   * Ako je kamera bila na poziciji A i sada vidi događaje na poziciji B → pomak je Δpose.
3. Koristiš **matematički model** (npr. particle filter, Kalman filter ili Bayesian filter) da testiraš:

   * "Ako pretpostavimo da se kamera pomaknula ovako, koliko bi vjerojatno generirala baš ove evente?"
   * To je tzv. **likelihood funkcija**.
4. Na temelju toga se **ažurira procjena položaja (pose)**.

---

### ⚙️ U praktičnim terminima:

* Imaš niz događaja `[(x1, y1, t1), (x2, y2, t2), ..., (xk, yk, tk)]`.
* Cilj je pronaći **trajektoriju kamere** koja **najbolje objašnjava** gdje i kada su ti događaji nastali.

---

### 🚁 Primjena (npr. u dronu):

* Dron leti iznad tla s uzorkom (npr. crne linije).
* Kamera bilježi događaje svaki put kad linija prođe ispod nekog pixela.
* Iz pomaka tih događaja kroz vrijeme, dron može **procijeniti vlastitu brzinu, smjer i rotaciju** – bez klasične kamere i frameova!

---

Pokušavaju procijeniti orijentaciju (rotaciju) kamere samo iz događaja, bez frameova.

Koriste particle filter, minimizaciju photometric errora i motion compensation optimizaciju.

Ograničeni su na rotacijsko gibanje, ali su važni jer otvaraju put prema punim 3D motion estimation metodama.

---

### 🔹 1. **Particle filter**

* Radi se o **probabilističkom pristupu** — umjesto da izračunaš točno rješenje, generiraš **više mogućih hipoteza** (tzv. čestice = “particles”) o položaju/orijentaciji kamere.
* Svaka čestica ima svoju “vjerojatnost” da predstavlja stvarni položaj kamere.
* Likelihood funkcija govori koliko se dobro *trenutni događaji* slažu s mapom scene — tj. ako kamera u toj orijentaciji “vidi” iste rubove gdje su eventi nastali → velika vjerojatnost.
* Na kraju se prosječno (ili najvjerojatnije) stanje čestica uzima kao rezultat.
  ➡️ Ukratko: koristi **nasumično uzorkovanje i vjerojatnosti** da procijeni rotaciju kamere.

---

### 🔹 2. **Minimizacija photometric errora**

* Ovdje se radi o **determinističkom optimizacijskom pristupu** — tražiš onu rotaciju kamere kod koje je **razlika između očekivane i stvarne svjetline (intenziteta)** najmanja.
* Koristi se **mapa vjerojatnosti rubova** scene, a eventi (koji nastaju kod promjena svjetline) se uspoređuju s tim mapiranim rubovima.
* Ako je event tamo gdje bi, prema pretpostavljenoj rotaciji, trebao biti jaki rub → mala greška, dobra orijentacija.
  ➡️ Ukratko: traži **rotaciju koja minimizira fotometrijsku pogrešku** između događaja i modela scene.

---

### 🔹 3. **Motion compensation optimizacija**

* Ovaj pristup ne procjenjuje izravno rotaciju, nego **kutnu brzinu** (tj. kako se orijentacija mijenja u vremenu).
* Ideja: ako znaš kutnu brzinu, možeš “kompenzirati” kretanje — tj. pomaknuti događaje unatrag u vremenu tako da bi se svi poravnali ako je model točan.
* Ako su svi događaji poravnati u istu strukturu (rubovi izgledaju “oštri”) → pronašao si dobru kutnu brzinu.
  ➡️ Ukratko: traži **brzinu rotacije** koja najbolje “poravnava” događaje kroz vrijeme.

---

💡 **Razlika ukratko:**

| Pristup             | Što traži    | Kako radi                         |
| ------------------- | ------------ | --------------------------------- |
| Particle filter     | Rotaciju     | Probabilistički, s mnogo hipoteza |
| Photometric error   | Rotaciju     | Optimizacija greške svjetline     |
| Motion compensation | Kutnu brzinu | Poravnava događaje kroz vrijeme   |

---

---

## 🔹 Što znači **6-DOF**?

“6 Degrees of Freedom” = kamera se može kretati:

* **3 translacije:** naprijed–nazad (x), gore–dolje (y), lijevo–desno (z)
* **3 rotacije:** pitch (nagib), yaw (okretanje lijevo-desno), roll (kotrljanje osi)

Znači, **puno praćenje poze (pose tracking)** = znamo *i gdje je kamera u prostoru* + *kako je okrenuta* u svakom trenutku.
To je daleko teže nego samo rotacija jer uključuje i **dubinu i perspektivu**.

---

## 🔹 Ukratko što rade pojedini pristupi iz odlomka:

### 🧩 [226] – *Hand-crafted metoda, B&W linije*

* Radi s **umjetnim crno-bijelim mapama s linijama** (nema probabilistike, sve ručno podešeno).
* Pretpostavlja da **svaki event dolazi s najbliže linije** u mapi.
* Te linije se **prate i njihovi presjeci daju 3D točke**.
* Zatim se koristi **PnP (Perspective-n-Point)** algoritam za računanje **poze kamere** iz poznatih točaka.
  ➡️ Ukratko: *ručno izrađena metoda* koja koristi geometriju linija da prati kameru kroz 3D prostor.

---

### 🧠 [228] – *Continuous-time nadogradnja prethodne*

* Umjesto da računa svaku pozu posebno, modelira **kontinuiranu putanju** kamere kroz vrijeme.
* Optimizira **event-to-line reprojection error** → znači: prilagođava cijelu putanju da bi svaki event “sjeo” što bliže svojoj liniji u mapi.
  ➡️ Ukratko: *kontinuirana optimizacija putanje kamere*, preciznija i glađa od frame-by-frame pristupa.

---

### ⚙️ [7] i [65] – *Realni 6-DOF tracking u prirodnim scenama*

* Ovi su već **real deal** — rade s **prirodnim scenama**, ne samo crno-bijelim linijama.
* [7] koristi **generativni probabilistički filter** (kao particle filter, ali robusniji):

  * Likelihood funkcija je **mješavina gustoća (mixture densities)** → bolje hvata nesigurnost i šum eventa.
* [65] koristi **nelinearnu optimizaciju photometric errora** između:

  * “Brightness increment images” (sinteza događaja u slike svjetline)
  * i njihove predikcije prema mapi scene.
* [65] daje malo bolje rezultate jer photometric optimizacija bolje hvata fine detalje svjetline.
  ➡️ Ukratko: *moderni 6-DOF trackeri* koji kombiniraju fiziku eventa + optimizaciju slike za full 3D tracking.

---

## 🔸 Ukratko sve skupa:

| Pristup | Tip                                 | Ključna ideja                                                  | Ograničenje                  |
| ------- | ----------------------------------- | -------------------------------------------------------------- | ---------------------------- |
| [226]   | Hand-crafted                        | Pretpostavlja da eventi dolaze s najbliže linije i koristi PnP | Radi samo za B&W linije      |
| [228]   | Continuous optimization             | Optimizira cijelu trajektoriju pomoću reprojekcije događaja    | Još uvijek jednostavne scene |
| [7]     | Probabilistički model               | Filter s mješavinom gustoća za robustnost                      | Zahtjevan za implementaciju  |
| [65]    | Nelinearna photometric optimizacija | Usklađuje svjetlosne promjene s mapom scene                    | Zahtjeva mapu scene          |

---

6 DOF ima određene izazove:
- promjena orijentacije mijenja kut gledanja,

- promjena pozicije mijenja paralaksu i dubinu,

- sve to moraš povezati s asinkronim eventima koji ne dolaze u “frameovima” nego neprekidno.

---


Ovaj tekst pokriva **evoluciju SLAM algoritama** za **event kamere** – od jednostavnih 2D verzija (samo rotacija, crno-bijele mape) do **pravih 3D 6-DOF sustava** koji rade u **realnim scenama bez pomoći dodatnih senzora** (RGB-D, IMU itd.).

Cilj svih:
👉 Istovremeno **pratiti pozu kamere** (tracking)
👉 I **graditi mapu scene** (mapping)
s pomoću *samo događaja* umjesto frameova.

---

## 🔹 Rani radovi (2D SLAM i rotacijski modeli)

### 🧠 Cook et al. [23]

* Koristili **message-passing algoritam** za zajedničku procjenu:

  * kretanja kamere (ego-motion),
  * slike (intensity),
  * i optical flowa.
* Ali: ograničeno samo na **rotacije**.
  ➡️ Ideja: simultana procjena više povezanih veličina → više jednadžbi = bolja stabilnost.

---

### 📏 [224] – 2D Event-based SLAM

* Baziran na [101], ali sad **gradi mapu scene dok prati kameru**.
* Koristi **particle filter** za praćenje poze.
* Likelihood = obrnuto proporcionalan **reprojection erroru** događaja prema mapi.
* Mapa = **occupancy map** (vjerojatnost da je pixel aktivan/edge).
  ➡️ Prvi pravi “SLAM” korak za event kamere, ali još **planarni (2D)** i za **visoki kontrast** scene.

---

### 🧍‍♂️ [225] – 3D SLAM, ali uz pomoć RGB-D senzora

* Nadogradnja [224], ali sad s **3D mapom** (dubina iz RGB-D senzora).
* Problem: RGB-D **ubija prednost event kamere** (sporo, visoka latencija).
  ➡️ Dakle, radi, ali *više nije pravi event-based sistem* jer se oslanja na vanjski senzor.

---

## 🔹 Bolji modeli za rotaciju i panorame

### 🌀 [24] – Filter-based pristup

* Dva **probabilistička filtera** rade paralelno:

  1. Praćenje orijentacije kamere.
  2. Gradnja panoramske mape.
* Koristi **Kalman filter po pixelu** → svaka točka ima svoju procjenu orijentacije i jačine edgea.
* Zatim se ta panorama pretvara u **HDR intenzitetnu mapu** (Poisson integracija).
  ➡️ Ultra-pametno: koristi evente da izgradi **super-resolution HDR panoramu** i orijentaciju istovremeno!

---

### 🧭 [103] – Photometric error pristup

* Koristi **minimizaciju photometric errora** između eventa i probabilističke edge mape.
* I mapa i praćenje rade zajedno (SLAM).
  ➡️ Stvara **panoramsku occupancy mapu** — svaki “map point” ima vjerojatnost stvaranja događaja (koliko je jaka ivica).

---

## 🔹 Pravi 3D Event-based SLAM (6-DOF napokon!)

### 💥 [25] – Full probabilistic 6-DOF SLAM

* Proširenje [24], sad s **tri filtera** koji istovremeno rade:

  1. Praćenje poze (pose tracking).
  2. Procjena dubine.
  3. Procjena svjetline (intensity).
* Problem: slabija robusnost kod inicijalizacije.
* Pretpostavlja da su dubina, intenzitet i gibanje **nekorelirani**, što nije točno.
* Radi u realnom vremenu, ali traži **GPU**.
  ➡️ Prvi “all-in-one” SLAM koji radi sve — ali skup i osjetljiv.

---

### ⚙️ [26] – Geometrijski (semi-dense) SLAM

* Dokazuje da **nije nužno rekonstruirati intenzitet slike** da bi se dobila dubina i poza.
* Koristi:

  * **Space sweeping** za 3D rekonstrukciju (čista geometrija).
  * **Edge-map alignment** (nelinearna optimizacija između događaja i mapa).
* Radi **u realnom vremenu na CPU-u!**
  ➡️ Učinkovit, precizan i jednostavniji — *vjerojatno najpraktičniji pristup za dronove*.

---

## 🔹 Zaključci i izazovi

* Još uvijek **nema loop-closurea** (popravljanje pogreške kad se kamera vrati na istu lokaciju).
* Radi samo na **malim scenama** (za sada).
* Ali! Cilj nije nužno zamijeniti frame-based SLAM, nego **biti komplementaran**:

  * Event kamera = visoka brzina, bez zamućenja, velika dinamika.
  * Frame kamera = precizni detalji i teksture.
* **Stereo event SLAM** još je neistraženo područje.
* **Fusion s IMU-om** (žiroskop, akcelerometar) značajno bi povećao robusnost.

---

## ⚡ TL;DR – Mega sažetak

| Pristup | Glavna ideja                                 | Prednosti               | Ograničenja                 |
| ------- | -------------------------------------------- | ----------------------- | --------------------------- |
| [23]    | Joint estimation (motion + flow + intensity) | Teoretski elegantno     | Samo rotacija               |
| [224]   | 2D particle filter SLAM                      | Simple i efektno        | Samo 2D, visoki kontrast    |
| [225]   | 3D SLAM + RGB-D                              | Radi u 3D               | Spor i kompleksan           |
| [24]    | Probabilistički filter + panorame            | HDR mapa i orijentacija | Samo rotacija               |
| [103]   | Photometric error + edge mapa                | Učinkovito mapiranje    | Nema translaciju            |
| [25]    | 6-DOF probabilistički SLAM                   | Full SLAM               | GPU heavy, nestabilan start |
| [26]    | Geometrijski semi-dense SLAM                 | Brz i robustan          | Još nema loop closure       |

---
---

### 💡 Što je Visual-Inertial Odometry (VIO)?

VIO = **fuzija kamere i IMU-a (akcelerometar + žiroskop)** → zajedno daju **pouzdaniju procjenu kretanja u 6-DOF-u**.

---

### 1️⃣ Visual Odometry (VO) sama po sebi...

* Koristi samo kameru da procijeni **kako se kamera pomaknula** između frameova.
* Dobra je kad ima dovoljno teksture, svjetla i stabilnog videa.
* Ali ako kamera brzo rotira, ako je scena monotona ili zamagljena → *VO gubi tracking*.

---

### 2️⃣ A Visual-Inertial Odometry (VIO)…

* Dodaje **IMU podatke (akceleracije, brzine rotacije)**.
* Kad kamera “oslijepi” (npr. u mraku ili pri velikim brzinama), **IMU i dalje zna da se tijelo kreće**.
* Zato **VIO nikad ne padne potpuno** — uvijek ima izlaz, iako s vremenom može **driftati** (lagano odlutati od stvarne pozicije).

---

### 3️⃣ Ključni izazov → *Temporalna fuzija*

Event kamera daje **asinkrone evente** (svaki pixel ima svoj timestamp),
dok IMU daje **sinkrone uzorke** npr. svakih 1 ms (1000 Hz).
👉 Problem: *kako spojiti ta dva izvora vremena u zajednički model?*

---

### 4️⃣ Tri pristupa koja koriste znanstvenici:

#### (i) **Asinkroni probabilistički filter**

* Koristi se **Bayesov filter (npr. EKF)** koji asinkrono prima evente i IMU mjerenja.
* Svaki novi podatak ažurira procjenu stanja → *state = pozicija, brzina, orijentacija*.
* Super precizan, ali računalno zahtjevan.

#### (ii) **Pre-integracija IMU-a**

* IMU podatke integriraš unaprijed između dva eventa ili framea → dobiješ “kompaktne” podatke.
* Time se smanji učestalost IMU updatea i lakše ih sinkroniziraš s eventima.
* Koristi se u većini modernih VIO sustava (npr. VINS-Mono, OKVIS, Basalt).

#### (iii) **Continuous-time model**

* Umjesto da imaš diskretne frameove, modeliraš poziciju kamere kao **kontinuiranu funkciju vremena**.
* Svi senzori (kamera, IMU, event kamera) se referenciraju na tu zajedničku vremensku os.
* Idealno za event kamere, jer i one rade kontinuirano.
* Ali zahtjeva napredne nelinearne optimizacije (spline modeli, Gaussian Processes itd.).

---

### 5️⃣ Zaključak

* VO = brza, ali može “puknuti”.
* VIO = otpornija, radi i bez slike, ali lagano drift-a.
* U event-based kamerama VIO je **game changer**, jer:

  * Eventi su brzi (mikrosekunde)
  * IMU je brz (1 kHz)
  * Kombinacijom dobivaš **precizno praćenje i pri ludim brzinama, bez zamućenja!** ⚡




---

### 🚀 1️⃣ Što znači *feature-based* VIO

* Umjesto da se koristi svaki pojedinačni event (što bi bilo kaotično), sustav **detektira i prati feature točke** kroz vrijeme.
* Te točke su “sidra” — stabilni detalji u slici (rubovi, kutovi, uzorci) koji se mogu pratiti kroz sekvence eventa.

---

### ⚙️ 2️⃣ Dvije glavne faze

1. **Frontend** → iz eventa se izvuku i prate feature točke (npr. Harris corneri ili FAST featurei).
2. **Backend (VIO fuzija)** → te trajektorije featurea se kombiniraju s IMU podacima da bi se procijenila 6-DOF putanja kamere i mapa okoline.

---

### 📸 3️⃣ Frontend: pretvaranje eventa u “feature trakove”

* Event kamera ne daje frameove, nego samo promjene osvjetljenja (x, y, t, polaritet).
* Sustavi poput [130] koriste algoritme za praćenje tih promjena kroz vrijeme → dobivaš **feature tracks** (trajektorije točaka kroz frameove).
* To je kao kad u običnom videu gledaš kako se kut zgrade miče kroz frameove — samo što se ovdje to radi *event po event*.

---

### 🧠 4️⃣ Backend: spajanje s IMU-om pomoću Kalman filtera

* Svaki track ima svoju procijenjenu poziciju i brzinu → to se kombinira s IMU mjerenjima (ubrzanje, rotacija).
* Kalman filter ili njegova varijanta (Extended/Unscented KF) koristi oba izvora informacija da bi “ispeglao” šum i procijenio precizniji položaj.
  👉 Ovo je kao kad kombiniraš *oči (kamera)* i *unutarnji osjet ravnoteže (IMU)* da znaš gdje si u prostoru.

---

### 🔄 5️⃣ Motion-compensated event images (spominje se u [129])

* Umjesto da koristi “raw” evente, metoda ih **kompenzira za gibanje** — znači “zarotira” i “pomakne” ih tako da se sve točke usklade s trenutnim kretanjem kamere.
* Time se dobiva **oštrija, stabilnija slika** iz niza eventa → i tada se mogu koristiti klasični feature detektori (npr. FAST, Harris).

---

### 🧩 6️⃣ Keyframe-based optimizacija

* Sustav ne optimizira svaki frame → prevelik trošak.
* Umjesto toga, koristi **keyframe pristup** → uzme ključne frameove i među njima optimizira:

  * Poze kamere (R, t)
  * 3D pozicije landmarka (točke u prostoru)
* Sve to radi preko **nelinearne optimizacije** (npr. Bundle Adjustment) kako bi smanjio ukupnu reprojection grešku.

---

### 📈 7️⃣ Spajanje i event + intensity frameova

* Kasniji radovi ([27]) spajaju event kameru i običnu (intensity) kameru u isti sustav.
* Time dobiješ najbolje od oba svijeta:

  * Event kamera = visoka brzina i HDR (ne zaslijepljuje se)
  * Obična kamera = bogata tekstura
* Zajedno omogućuju rad i u **mraku, jakoj svjetlosti, ili brzoj rotaciji** (npr. dron koji leti u sumrak).

---

### 🧮 8️⃣ Optimizacija = procjena putanje i mape

* Cilj sustava:

  * Rekonstruirati **trajektoriju kamere** u 6-DOF-u (pozicija + orijentacija)
  * Stvoriti **sparse 3D mapu** svijeta oko nje (landmarki u prostoru).
* Sve se optimizira kako bi **reprojection error bio minimalan** → da se projekcije 3D točaka poklapaju s njihovim promatranim mjestima na slici.

---

### 📊 9️⃣ Benchmarking

* Sve te metode se testiraju na **6-DOF datasetima** (npr. [98]) — obično realni pokreti kamere s ground truthom.
* Svaka nova verzija metode poboljšava prethodnu po brzini, preciznosti i otpornosti na šum.

---

### ⚡ 10️⃣ Glavni takeaway

Feature-based event VIO =
➡️ *pretvori evente u točke koje možeš pratiti*,
➡️ *spoji s IMU-om da dobiješ robustnu procjenu kretanja*,
➡️ *optimiziraj poze i mapu kroz keyframe-based nelinearnu optimizaciju.*
➡️ Rezultat: **precizan, robustan, high-speed 3D tracking — čak i u mraku ili ekstremnim uvjetima!**

---

Continuous-time framework – kamera se modelira kao kontinuirana funkcija vremena, ne samo diskretne frameove, što je prirodnije za event kamere koje daju asinkrone događaje.

Reprojection error – umjesto samo feature trackova, svaka predviđena lokacija događaja se reprojektira u sliku, i razlika između stvarnih i predviđenih događaja je mjera pogreške.

Fuzija s IMU – inertialni podaci se uključuju u istu optimizaciju, tj. objektivna funkcija minimizira i vizualnu (event) i inercijalnu pogrešku.

Event-based bundle adjustment – slično klasičnom BA za standardne kamere, ali sada optimiziramo trajektoriju kamere i poziciju točaka (scene structure) iz samih eventa.

Izbjegavanje konverzije u feature tracks – klasični feature-based pristup prvo pretvara evente u geometrijske featuree; reprojection-based metoda direktno koristi raw evente, što potencijalno daje precizniju rekonstrukciju.

Photometric error / firing rate – događaji imaju intenzitet pokretanja (event rate) koji se može koristiti kao fotometrijski signal za optimizaciju, slično VI-DSO za standardne kamere.

Stereo event VIO – još nije istraženo, ali kombiniranje stereokamera + event-based depth može dovesti do full SLAM + VIO sistema s real-time mapiranjem.

Learning-based alternative – trenutno literatura je model-based (klasične optimizacijske metode), ali deep learning bi mogao direktno mapirati raw evente + IMU u 6-DOF poziciju.

Ključna prednost – kontinuirana optimizacija po segmentima trajektorije daje glatkije i robusnije pozicije, drastično smanjujući drift u usporedbi sa čistim feature-based ili jednostavnim Kalman filter pristupom.

Izazov implementacije – zahtjeva složenije numeričke metode, nelinearnu optimizaciju, te dobar model kamere i IMU kalibracije. Ovo nije trivialno za real-time CPU implementaciju, ali GPU i batch optimizacije čine to izvedivim.

Image reconstruction

Event = promjena svjetline – svaki event kodira samo kada se svjetlina promijeni iznad nekog praga, s polaritetom (+/-).

Ne-redundantno kodiranje – unlike obična kamera koja zapisuje cijeli frame, event kamera šalje samo promjene, pa je podatak “komprimiran” po prirodi.

Integracija eventa = vraćanje svjetline – kad integriraš sve promjene po pikselima kroz vrijeme, dobiješ “aproksimativnu” originalnu svjetlinu scene.

Rekonstrukcija slika – ovaj proces integracije eventa naziva se image reconstruction; efektivno decompressaš event stream natrag u brightness mapu.

Visoka temporalna rezolucija – eventi dolaze u mikrosekundama, pa možeš rekonstruirati frameove na tisuće Hz (2–5 kHz) ili kontinuirano.

Prednosti – nema motion blur-a jer se integrira u realnom vremenu; možeš dobiti “trenutnu sliku” čak i pri velikim brzinama objekata.

Metode rekonstrukcije – od jednostavne akumulacije eventa (dodan +1/-1 po pikselu) do sofisticiranih algoritama koji uključuju regularizaciju, optimizaciju i rekonstrukciju visoke kvalitete.

Continuous-time reconstruction – neke metode (npr. [62]) ne čekaju frame, nego kontinuirano ažuriraju brightness mapu dok dolaze eventi.

Noise & sensor limitations – u stvarnom svijetu eventi imaju šum, dead pixels, i neidealni response, pa rekonstrukcija često koristi filtering i denoising.

Primjena – high-speed tracking, HDR scena u realnom vremenu, robotika, AR/VR, pa čak i predobuka za SLAM ili VIO sustave.

Event = promjena svjetline – svaki event kodira samo kada se svjetlina promijeni iznad nekog praga, s polaritetom (+/-).

Ne-redundantno kodiranje – unlike obična kamera koja zapisuje cijeli frame, event kamera šalje samo promjene, pa je podatak “komprimiran” po prirodi.

Integracija eventa = vraćanje svjetline – kad integriraš sve promjene po pikselima kroz vrijeme, dobiješ “aproksimativnu” originalnu svjetlinu scene.

Rekonstrukcija slika – ovaj proces integracije eventa naziva se image reconstruction; efektivno decompressaš event stream natrag u brightness mapu.

Visoka temporalna rezolucija – eventi dolaze u mikrosekundama, pa možeš rekonstruirati frameove na tisuće Hz (2–5 kHz) ili kontinuirano.

Prednosti – nema motion blur-a jer se integrira u realnom vremenu; možeš dobiti “trenutnu sliku” čak i pri velikim brzinama objekata.

Metode rekonstrukcije – od jednostavne akumulacije eventa (dodan +1/-1 po pikselu) do sofisticiranih algoritama koji uključuju regularizaciju, optimizaciju i rekonstrukciju visoke kvalitete.

Continuous-time reconstruction – neke metode (npr. [62]) ne čekaju frame, nego kontinuirano ažuriraju brightness mapu dok dolaze eventi.

Noise & sensor limitations – u stvarnom svijetu eventi imaju šum, dead pixels, i neidealni response, pa rekonstrukcija često koristi filtering i denoising.

Primjena – high-speed tracking, HDR scena u realnom vremenu, robotika, AR/VR, pa čak i predobuka za SLAM ili VIO sustave.

Image reconstruction iz evenata zahtjeva regularizaciju. 
Event kamere imaju neovisne piksele koji "reportiraju" promjene u osvjetljenju. Per-pixel integracija takvih promjena kroz vrijeme rezultira samo slikama s inkrementiranom svjetlošću

ključni detalj u image reconstruction iz eventa – sam event stream ti daje samo promjene svjetline, ne apsolutne vrijednosti. Evo kako to možemo objasniti u natuknicama:

Event = brightness change, ne apsolutna vrijednost – svaki piksel šalje +1/-1 ili neku sličnu oznaku promjene.

Integracija po pikselu daje brightness increment image, tj. koliko se svjetlina promijenila u nekom vremenskom intervalu, ali ne i stvarnu svjetlinu scene.

Offset image = početna svjetlina – da bi dobio stvarnu brightness mapu, trebao bi dodati početnu sliku intervala na integrirane promjene.

Problem – u praksi često nemamo tu početnu sliku (offset), posebno u potpuno event-based sustavima.

Rješenje: regularizacija – koristi se prostorno i/ili vremensko glatkanje (smoothing) kako bi se rekonstruirala brightness slika iz nule.

Spatial smoothing – pikseli se “pomažu” susjedima; izbjegava se ekstremno šum i lokalne nepravilnosti.

Temporal smoothing – koristi informacije iz prethodnih intervala; stabilizira brightness mapu kroz vrijeme.

Learning-based regularization – deep learning modeli mogu naučiti statistiku prirodnih scena i rekonstruirati realistične brightness slike iz event streama.

Prednosti – omogućuje HDR rekonstrukciju, pod visokim brzinama i u sceni s velikim kontrastom (npr. izlazak iz tunela, eksplozija).

Rezultat – dobivaš kontinuiranu brightness mapu, visoke dinamičke širine, bez motion blur-a i s očuvanjem detalja, što je ključno za event-based SLAM, VIO ili tracking.

Summary:

Kvaliteta slike – jako ovisi o noise-u u contrast threshold-u piksela; pikseli nisu savršeno identični zbog manufacturing mismatcha i promjena svjetla/dinamike.

Spatial resolution – viša rezolucija senzora → bolja reconstructed slika, niža → gubi detalje.

Integracija events → brightness image – principijelno se evente može “dekomprimirati” u brightness frame koji se koristi kao obična slika.

Mature CV pipelines – rekonstruirani frameovi omogućuju korištenje svih standardnih computer vision algoritama (prepoznavanje objekata, SLAM, optical flow…).

Prednosti – može hvatati high-speed motion i HDR scene; scene koje bi obična kamera teško snimila.

Trošak – rekonstrukcija je računalno intenzivna, ima latenciju i povećanu potrošnju energije.

Nije uvijek nužno – za neke zadatke poput feature tracking, SLAM-a ili optical flowa, ne mora se rekonstruirati frame; eventi sami često daju dovoljno informacije.

Scenska reprezentacija – rekonstruirane slike daju stabilniji prikaz scene od same sekvence eventa; manje osjetljiv na noise i kratkotrajne promjene.

Facilitacija korrespondencija – rekonstruirani frameovi pomažu u povezivanju istih featurea između eventa, što je ključno za tracking i VIO.

Dodatna vrijednost – osim praktičnih zadataka, rekonstruirane slike služe i kao appearance maps, što je korisno za vizualizaciju scene i eventualnu fuziju s drugim senzorima.

Motion segmentation

Segmentacija pokretnih objekata koje promatra stacionarna event kamera je jednostavna
Eventi su vezani samo uz kretanje objekata (pod pretpostavkom konstantnog osvjetljenja)
U slučaju pokretne kamere javljaju se izazovi jer se eventi događaju svuda u vidokrugu kamere
Stvaraju ih pokretni objekti i prividno pokretna scena (scena je statična, ali se čini da se miče zbog micanja kamere)
Cilj je za svaki event razaznati je li uzrokovan pokretom objekta na sceni ili pokretom scene zbog kamere
Izazovno je to odraditi jer svaki event u sebi nosi jako malo informacija
Ukratko: vidimo kako se globalno kreće scena (global flow) i onda to oduzmemo od pojedinih kretanja u svakom eventu

Način istraživanja: segmentacija motiona u scenarijima koji postaju progresivno sve kompleksniji, zbog smanjivanja dodatnih informacija za rješavanje problema
Primjeri dodatnih informacija: algoritam ima info o tome koji oblik ili koji način kretanja mora očekivati (ča očekujen vidit i kako će se kretat)

Ako nemaš dodatne informacije (kao što su flow kamere ili dubinska mapa), problem postaje unsupervised – moraš se osloniti samo na eventi.

Osnovna ideja: pokretni objekti stvaraju distinktivne tragove eventa na slici. Ti tragovi se mogu pratiti kroz vrijeme da bi se rekonstruirale putanje objekata.

Rezultat: segmentacija objekata se dobiva istovremeno s procjenom njihove putanje.

Ovo je u osnovi joint optimization problem:

tražiš parametre pokreta objekata (kao “klastere”)

dok istovremeno određuješ koji event pripada kojem objektu.

U praksi se ovo često rješava iterativno:

prvo inicijalna grupa eventa u klastere

zatim optimizacija parametara pokreta i reassignment eventa

ponovi dok se ne konvergira

Ukratko: čak i bez dodatnih senzora, segmentacija može uspjeti tako što iskoristi prostorno-vremenske obrasce eventa.

Poznavanje oblika objekta pomaže:

[13] detektira i prati krug čak i kad pokret kamere stvara puno “cluttera”.

Koristi Hough transform i optical flow iz vremenskih prozora eventa.

Robusnost praćenja:

[181] proširuje metodu s particle filterom, dinamički prilagođava trajanje prozora za praćenje naglih promjena gibanja.

Općeniti oblici objekata:

[188] koristi event corners kao geometrijske primitive.

Zahtijeva dodatno znanje o robot joints koji pokreću kameru.

Segementacija pomoću motion-compensated event images:

[132], [154], [155] koriste ovu ideju: evente warpaju prema hipotezi pokreta da bi se dobile oštre konture objekata.

Jednostavne hipoteze pokreta:

Linearni modeli (konstantni optical flow) često su dovoljni za kratka vremena.

Scene se opisuju kao kolekcije objekata s različitim linearnim modelima pokreta.

Greedy pristupi segmentaciji:

[154] prvo uklanja dominantne evente (pozadinu), zatim fitira linearni model na ostatak (objekti).

[132] otkriva pokretne objekte detektiranjem odstupanja od dominantnog pokreta (background).

Iterativni pristupi:

[155] iterativno optimizira event-object assignments i motion parameters, daje bolje rezultate od greedy metoda.

Omogućuje general parametric motion models za svaki objekt.

Learning-based pristupi:

[133] koristi ANN za procjenu depth, ego-motion, segmentation masks i 3D brzine objekata.

Dataset s pixel-wise motion maskama omogućuje nadzirano učenje.

Prednosti event-based segmentacije:

Daje robusno praćenje čak i u HDR i high-speed scenama gdje standardne kamere ne mogu.

Zaključak:

Segmentacija je ključna u frame-based vision, ali je još nedovoljno istražena u event-based vision.

Kako se razvijaju napredniji event-based algoritmi, očekuje se rast radova na ovom izazovnom problemu.



Recognition (4.8)


* **Algoritmi prepoznavanja** za event kamere postaju sve složeniji.
* Razvili su se od **jednostavnog template matchinga** (prepoznavanje osnovnih oblika) do **klasifikacije složenih uzoraka rubova**.
* U početku su se koristili **klasični ML pristupi** s ručno definiranim značajkama (hand-crafted features).
* Danas se sve više koriste **deep learning metode** za automatsko učenje reprezentacija.
* Glavni cilj tog razvoja je **povećati izražajnost (expressibility)** sustava prepoznavanja i **otpornost na izobličenja podataka (robustness to distortions)**.

Rana istraživanja event based senzora -> praćenje moving objecta pomoću statičnog senzora
Praćenje pozicije i oblika objekta (usporedba s poznatim jednostavnim oblicima...blob, circle, line)
Opcija je i matching s predefiniranim templateima (onda nam ne treba da znamo geometriju objekta, nego samo matching)
Korištenje konvolucija u ranim hardverima

Za kompleksnije objekte, templates se kroiste za povezivanje low-level featurea, a ne cijelih objekata
Nakon toga, klasifikator donosi odluke na temelju distribucije promatranih featurea
Koriste se nearest neighbor klasifikatori => udaljenosti u feature spaceu
Preciznost se može povećati s dodavanjem feature invariancea (hijerarhijski model gdje se kompleksnost featurea diže u svakom layeru)
Uz dobre featurese, treba trenirati samo finalni klasifikator pri promjeni zadataka
Problem: koje featurese odabrati
U ranim radovima koriste se hand-crafted features, ali bolje je učiti featurese iz samih podataka
U najboljem slučaju, svaki template može nastati iz pojedinog samplea, ali takav pristup je osjetljiv na noise u podacima
Moguće je učiti featurese pomoću unsupervised učenja, clusteringa event podataka i korištenjem centra svakog clustera kao featurea
Svaki novi event povezuje se s najbližim featureom
Koristi se back propagation 
Prednost: ne treba nam poseban klasifikator za output
Nedostatak: potrebno je jako puno labeliranih podataka za treniranje
Problem je i nedostatak spremnih labeliranih podataka za trening (većinom treba raditi custom dataset)

Wormhole learning:
Problem: nedostatak kvalitetnih trening podataka u event domenu otežava učenje modela.

Rješenje: koristi se wormhole learning, semi-supervised metoda koja povezuje RGB i event domenu.

Prvi korak: model treniran na RGB slikama (teacher) uči detektor za event podatke.

Drugi korak: event model postaje učitelj — dio robustnosti na promjene osvjetljenja (illumination invariance) prenosi se natrag na RGB model.

Na taj način se iskorištava snaga oba senzora — bogatstvo podataka iz RGB i otpornost event kamere.

Većinom se u learning-based pristupima eventi/spikeovi konvertiraju u dense vektore => mogu se koristiti u hijerarhijskim modelima (npr. ANN)

Različiti načini evaluacije vektora (tensora)

Summary:

---

###  **1. Metode za pretvaranje event podataka**

* Najjednostavnije metode koriste **time surfaces** (karte vremena događaja) ili **event histograme**.
* Naprednije varijante dodaju **eksponencijalni decay** [109] ili **prosječne vremenske oznake** [113] za bolju robusnost.
* Alternativa: koristiti **rekonstrukciju slike** (Section 4.6) za dobivanje klasične slike iz event streama.
* Neki pristupi **pretvaraju spikeove u frameove** tijekom inferencije [150], [235].
* Drugi konvertiraju **trenirani ANN** u **spiking neural network (SNN)** koji direktno radi s eventima [137].
* Slične ideje koriste se i za druge zadatke osim prepoznavanja [22], [108].

---

###  **2. Uloga neuromorfičkog hardvera**

* Razvijaju se **SNN-ovi** koji mogu **učiti izravno** iz event podataka [143].
* Neki eksperimenti čak **treniraju modele direktno na neuromorfičkom čipu** [144].
* Ovaj pristup otvara vrata **super brzim, energetski učinkovitim** sustavima prepoznavanja.

---

###  **3. Razvoj zadataka prepoznavanja**

* Prvi radovi: prepoznavanje **jednostavnih oblika** (krug, kvadrat) sa statičnom kamerom.
* Kasnije: **kompleksniji objekti** — znakovi na kartama (card pips), **slova**, **lica**, itd.
* **Najpopularniji test**: event-verzije **MNIST** dataset-a (rukom pisane znamenke).
* Moderni modeli postižu **>98% točnosti**, ali to nije pravi pokazatelj snage event kamera — ti zadaci su prejednostavni.

---

###  **4. Napredniji i realniji zadaci**

* Teži datasetovi: **Caltech-101**, **Caltech-256** (još uvijek “lagani” za CV, ali teži za event kamere).
* **Recognition s pokretne kamere** (npr. na vozilu) — rijetko istraženo područje.
* Većina metoda ipak koristi **pretvaranje u frameove** i klasične **deep learning modele**.

---

###  **5. Ključni izazovi**

* Event kamere **reagiraju samo na promjenu** → trebaju **pokret** (objekta ili kamere).
* To znači da **ne mogu učinkovito prepoznati statične objekte**.
* Izgled event slike **ovisi o relativnom gibanju**, pa bi **kontrolirano gibanje kamere** moglo pomoći u stabilnijem prepoznavanju [242].

---

###  **6. Pogodne aplikacije**

* Idealne za **prepoznavanje prema načinu gibanja** (gesture, action recognition).
* Odlične za **dinamične scene** i **brze pokrete**, gdje klasične kamere zamućuju sliku.
* Posebno korisne na **mobilnim platformama** (npr. dronovi, roboti) gdje su uvjeti svjetla i brzine izazovni.

---

###  **7. Ograničenja trenutnog stanja**

* Iako event kamere imaju sjajne karakteristike, **još su daleko od konkurencije s frame-based metodama**.
* Moraju pronaći **nišne zadatke** koji **maksimalno koriste njihove prednosti** — a ne kopirati frame-based pristupe.

---

###  **8. Dataseti i anotacije**

* Kvaliteta event-based dataseta **se poboljšava**, ali **anotacije su i dalje veliki problem**.
* Nema **standardnog alata ni formata** za označavanje event podataka.
* Većina postojećih dataseta dolazi iz **frame-based videa**, što **nije optimalno** jer ne iskorištava pravu prirodu event kamera.
* Velika prilika: napraviti **alat/pipeline za lako prikupljanje i označavanje event podataka**, čak i od strane laika.

---
Neuromorphic control
- Kod živih bića, većina informacija se procesira pomoću spike-based reprezentacije
Spikeovi enkodiraju senzorske (osjetilne) podatke
Spikeovi obavljaju izračune
Spikeovi odrađuju "aktuatorske naredbe"
Dakle, event-based paradigma primjenjiva je i na kontrolu, a ne samo percepciju i inference

Neurmorphic-vision-driven Control Architecture
- komponente: neuromorfni senzor, event-based estimator i tradicionalni kontroler

Estimator računa "state", a kontroler računa potrebnu kontrolu na temlju tog "statea"
Kontroler "nije svjestan" asinkronosti arhitekture

Prednosti: niska latencija i visoka efikasnost
Primjeri: spike-based konvolucijski target tracker, robotski "golman", robot koji balansira kemijsku
Latencija manja od 1ms + jednostavna ugradnja u embedded sustave (može raditi i na prilično ograničenim resursima)

Event based control theory
Control&decision => više informacija omogućuje bolje odluke, ali ako su troškovi vezani za dobivanje informacija preveliki, racionalnije je donijeti odluku na temelju parcijalne informacije
U event-based kontroli, signal se mijenja asinkrono 
Postoji više varijacija, ovisno o tome kako se generiraju control events

Najbitnije: event-triggered control i slef-triggered control

Osnovna ideja

Kod živih bića većina senzorne i motoričke obrade odvija se u spike-based formatu (tj. event-based).

Spikeovi enkodiraju senzorske podatke, računaju stanja, i pokreću akcije — percepcija, odluka i reakcija u jedinstvenom okviru.

Dakle, event-based paradigma nije samo za percepciju (vid, sluh...), nego i za kontrolu (pokret, akcije, regulaciju).

Neuromorphic Vision–Driven Control Architecture
Komponente:

Neuromorfni senzor (event camera) → proizvodi asinkrone događaje.

Event-based estimator → procjenjuje trenutno stanje sustava (“state”).

Klasični kontroler → generira kontrolne naredbe na temelju tog stanja.

Kontroler nije svjestan asinkronosti — on samo prima ažuriranja kad ih ima.

Takva arhitektura kombinira biološki realizam s inženjerskom jednostavnošću.

Prednosti:

Ultra-niska latencija (ispod 1 ms).

Visoka energetska i računska efikasnost.

Može raditi na embedded platformama i mikrokontrolerima s ograničenim resursima.

Pogodno za brze, reaktivne zadatke:

spike-based target tracking,

robotski “golman”,

balansiranje fizikalnih sustava (npr. kemijska epruveta).

Event-Based Control Theory
Konceptualna osnova:

Utemeljeno na control i decision teoriji.

Inspirirano ekonomskim principom “rational inattention” [247]:

Više informacija = bolje odluke,

ali ako je skupljanje ili obrada informacija skupa, racionalno je donositi odluke s parcijalnim znanjem.

Dakle, kontrolni signal se mijenja samo kad je to potrebno, a ne u fiksnim vremenskim koracima.

Način rada:

Kontrolni signali se ažuriraju asinkrono — samo kad događaji to opravdaju.

Postoje dvije glavne paradigme:

Event-triggered control –

događaj pokreće reakciju izvana (“exogenously”),

npr. ponovno izračunaj kontrolu kad pogreška u praćenju pređe prag.

Self-triggered control –

kontroler sam odlučuje kada će ponovno izračunati izlaz,

npr. “spava” duže ako je stanje stabilno, reagira brže ako se sustav mijenja.

Trade-off i motivacija:

Cilj: balansirati između performansi i računalnog troška.

Idealno bi bilo stalno recomputati kontrolu (beskonačno često) → ali to je računski neizvedivo.

Event-based pristup daje jednaku kontrolnu kvalitetu s puno manje računanja, ili bolju kontrolu s istim brojem izračuna.

U nekim slučajevima (npr. linear Gaussian sistemi) taj se trade-off može izračunati analitički.

Ograničenja i izazovi

Klasična event-based control teorija bavi se malim, niskodimenzionalnim sistemima (npr. mrežna kontrola).

Neuromorphic control sustavi (npr. robotika, vozila) su visokodimenzionalni i nelinearni.

To otežava zatvorene (closed-form) matematičke rezultate → potrebno je empirijsko i heurističko modeliranje.

Otvoreni istraživački problemi
1. Task-driven sensing

U prirodi, percepcija ima smisla samo ako vodi akciji.

Cilj: kontroler koji dinamički modulira senzorski ulaz ovisno o zadatku i kontekstu.

Potencijal: integracija s region-of-interest (ROI) mehanizmima i promjenjivim bias postavkama kamere → efikasniji sensing i kontrola.

2. Thinking Fast and Slow

Trenutni fokus: brza, niskolatencijska kontrola (“fast thinking”).

Problem: kako to integrirati s višerazinskom kognitivnom arhitekturom (npr. planiranjem, učenjem)?

Biološka analogija prema Kahnemanu [257]:

“System 1” – brzo, instinktivno, refleksno (event-based).

“System 2” – sporo, svjesno, deliberativno.

Cilj: spojiti oba sustava u jedinstvenu, adaptivnu kontrolnu arhitekturu.

Chapter 5. -> event based systems&applications
Neuromorphic computing

Neuromorfno inženjerstvo pokušava koristiti kombinaciju računalne snage i efikasnosti mozga kombinirajući njegovu strukturu i funkciju
Paralelni hardverski akceleratori za SNN-ove => definicija neuromorfnog procesora

Neuronski spikeovi unutar procesora su asinkroni i zato je neuromorfno procesiranje idealno za koristiti s event kamerama
Neuromorfni procesori reagiraju na evente koje šalje event kamera, bez dodatne konverzije => jako dobro spatially i temporally lokalno procesiranje podataka
Low power consumption & low latency

Kriterij kategorizacije neuromorfnih procesora može biti način implementacije modela neurona
Analogni neuroni, digitalni neuroni i software neuroni.
Neke arhitekture omogućavaju i on-chip learning

Pri evaluaciji neuromorfnog procesora za ebv sustav, u obzir treba uzeti:
- funkcionalnost i performanse procesora
- ekosustav u kojem je software razvijen (minimum je: API za komponirati i trenirati network, kompajler za pripremu networka za hardver, runtime library za deployment networka na harddver
- event based vision sustavi tipično zahtjevaju da je procesor dostupan kao zasebni sustav koji se može pokretati na edge devices, a da nije samo hostan na nekom remote serveru
- dostupnost neuromorphic procesora

Da bi se neuromorfni procesori šire koristili, nužno je:
- razviti više user-friendly ekosustav (lakši način za isprogramirati ono što želimo deployat na hardver)
- omogućiti veće procesne mogućnosti na hardverskoj platformi
- povećati dostupnost uređaja

Najbolji trenutni procesori:

---

###  **SpiNNaker (Spiking Neural Network Architecture)**

* Koristi **ARM jezgre** (general-purpose procesore).
* Ne koristi fizičke neurone, već ih **simulira softverski** → **maksimalna fleksibilnost**, ali **manje ubrzanje**.
* Primjene s event kamerama:

  * **Stereo depth estimation**
  * **Optic flow**
  * **Object tracking i recognition**
* Fokus: **biološki realistične simulacije** mozga.

---

###  **TrueNorth (IBM)**

* Ima **digitalne neurone** — svaka čip simulira:

  * **1 milijun neurona**
  * **256 milijuna sinapsi**
  * **4096 neurosinaptičkih jezgri**
* **Nema učenja na čipu** → mreže se treniraju **offline (GPU)**.
* Primjene s event kamerama:

  * **Gesture recognition**
  * **Stereo rekonstrukcija**
  * **Optical flow**
* Fokus: **real-time inference**, **niska potrošnja**, **niska latencija**.

---

###  **Loihi (Intel)**

* Ima **digitalne neurone** s **real-time inference + online learning**.
* Jedan čip:

  * **131 tisuća neurona**
  * **130 milijuna sinapsi**
* Ima **learning engine** koji podržava:

  * **STDP** (Spike-Timing Dependent Plasticity)
  * **Reinforcement learning**
* Može trenirati obične mreže u **TensorFlowu**, pa ih konvertirati u spiking verziju pomoću **Nengo DL toolkita**.
* Planiran sustav **Pohoiki Springs** s:

  * **768 Loihi čipova**, ~**100 milijuna neurona**, **100 milijardi sinapsi**.
* Fokus: **online učenje i fleksibilnost**, ali još uvijek daleko od biološkog mozga (koji ima ~800 trilijuna sinapsi).

---

### ️ **DYNAP (Dynamic Neuromorphic Asynchronous Processor) – aiCTX**

* Dvije varijante:

  * **Dynap-se** → optimiziran za **inference (skalabilno izvođenje)**
  * **Dynap-le** → optimiziran za **online learning**
* Fokus: **asinkrono, energetski učinkovito procesiranje**.

---

###  **Braindrop**

* Prototip jedne jezgre sustava **Brainstorm** (planiran s 1M neurona).
* Programira se pomoću **Nengo** i koristi **Neural Engineering Framework (NEF)**.
* Razvijen na **Stanfordu**, nasljednik je **Neurogrid** procesora.
* Fokus: **istraživanje modela neuronskih mreža**, **jednostavna integracija u softver**.

---



---

| **Procesor**                | **Broj neurona (≈)**                    | **Sinapse (≈)**       | **Učenje na čipu**       | **Fokus / Namjena**                         | **Primjene s event kamerama**                   | **Posebne značajke**                                                      |
| --------------------------- | --------------------------------------- | --------------------- | ------------------------ | ------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------- |
|  **SpiNNaker**            | Fleksibilno (ovisno o broju ARM jezgri) | Softverski definirano |  Da (softverski modeli) | Biološki realizam, simulacija mozga         | Stereo depth, optic flow, tracking, recognition | Neuronski modeli u softveru → maksimalna fleksibilnost                    |
|  **TrueNorth (IBM)**      | 1 milijun                               | 256 milijuna          |  Ne                     | Real-time inference, niska potrošnja        | Gesture recognition, stereo, optical flow       | 4096 neurosinaptičkih jezgri, trenira se offline (GPU)                    |
|  **Loihi (Intel)**        | 131 tisuća (po čipu)                    | 130 milijuna          |  Da (STDP, RL)          | Online učenje, adaptivnost                  | Eksperimentalno za učenje u hodu                | TensorFlow + Nengo DL integracija, projekt Pohoiki Springs (100M neurona) |
| ️ **DYNAP (aiCTX)**        | Tisuće po čipu (ovisno o verziji)       | Nepoznato             |  Da (u Dynap-le)        | Energetska učinkovitost, inference/learning | -                                               | Asinkron dizajn, dvije varijante: SE (inference), LE (learning)           |
|  **Braindrop (Stanford)** | 1 jezgra prototip (~1M planirano)       | -                     |  Da                     | Istraživanje neuronskih modela              | -                                               | Koristi Neural Engineering Framework (NEF), Nengo programiranje           |

---


---

### Real-time on-board robotika s event kamerama

**Glavna ideja:**
Event kamere generiraju znatno manje podataka po vremenskom intervalu nego klasične frame-based kamere.
Zbog toga obrada može biti izvedena u stvarnom vremenu na samom uređaju, bez potrebe za snažnim računalom ili USB prijenosom podataka.

---

### Konkretni primjeri:

1. **Wheeled robot (s ARM mikrokontrolerom)**

   * Dual-core ARM mikrokontroler na 200 MHz s 136 KB RAM-a obraduje evente u stvarnom vremenu.
   * Radi potpuno samostalno, bez vanjskog računala.
   * Izvodi zadatke poput praćenja linije, aktivnog i pasivnog praćenja objekata, procjene udaljenosti i jednostavnog mapiranja prostora.
   * Ovaj primjer pokazuje da su event kamere iznimno učinkovite i prikladne za robote s vrlo niskom potrošnjom energije.

2. **SpeckSoC11 (edge computing primjer)**

   * Sustav kombinira DVS (Dynamic Vision Sensor) i Dynap-se neuromorfni CNN procesor.
   * Potrošnja energije manja je od 1 mW, a latencija ispod 30 ms.
   * Primjene uključuju kontinuiranu detekciju objekata, sustave nadzora i automobilske aplikacije poput detekcije prepreka ili pješaka.

3. **Quadrotori (dronovi)**

   * Event kamere integrirane su u dronove s ograničenim računalnim resursima.
   * Koriste se za autonomno slijetanje, navigaciju i let u zahtjevnim uvjetima, poput slabog osvjetljenja ili velikih brzina kretanja.
   * Glavna prednost je vrlo niska latencija i otpornost na zamućenje slike pri brzom kretanju.

---

### Zaključak:

- Event kamere omogućuju obradu vizualnih informacija izravno na senzoru, u stvarnom vremenu i s minimalnom potrošnjom energije.
- Zbog toga su idealne za primjenu u mobilnim i energetski ograničenim sustavima, poput autonomnih robota, dronova i IoT uređaja.


DISCUSSION & CONCLUSION
- EBV = computer vision + robotika + neuromorphic engineering
- Omogućava low power consumption (always ON uređaji)
- Korisno za embedded aplikacije na platformama s ograničenim resursima
- Niska latencija za visoku reaktivnost sustava
- Visoka dostupnost informacija za bolju percepciju okoline
- Troši se malo računalnih resursa

- Ne zna se još koji je najbolji način za procesiranje i reprezentaciju evenata (jer ovisi o use case-u)
Više trade-off slučajeva:
- latency vs power consumption
- accuracy&sensitivity vs bandwith&processing capacity

npr. Smanjenje kontrast thresholda i/ili povećanje rezolucije kreira više evenata (te evente procesira algoritam na platformi s ograničenim resursima)
Izazov:
- kvantifikacija opisanih tradeoffova i razvoj tehnika za dinamičku prilagodnu senzora i/ili algoritamskih parametara za optimalne performanse
- razvoj bio-inspired sustava koji su event based od početka do kraja (od percepcije do kontrole i aktuacije (uporabe aktuatora))
- različito u odnosu na mainstream deep learning metoda computer visiona (ideja: probati adaptirati postojeće koncepte ili razviti sustave za određene probleme od nule uz ča bolje performanse)
- active vision -> percepcija + kontrola; posebno relevantno za event kamere jer eventi ovise o pokretima
- event kamera + hardver na istom senzorskom uređaju (efikasno, near-sensor procesiranje, samo high level ne-redundantne informacije se šalju; smanjenje bandwitha, latencije i potrošnje energije)

########################################################################################################################
Fast-Classifying, High-Accuracy Spiking Deep Networks Through Weight and Threshold Balancing

Duboke neuronske mreže poput CNN-ova i DBN-ova su zlatna stvar za klasifikaciju u CV-u

CNNs
Main features:
- inspirirane ljudskim vidnim sustavom
- koriste konvolucijske slojeve (filters/kernel) koji klite preko slike i oktrivaju lokalne uzorke (rubovi, teksture etc.)
- imaju pooling slojeve za smanjenje dimenzionalnosti i fully connected slojeve na kraju za klasifikaciju
- dobre za: obradu slika, videa, object recognition, face detection etc.
- uče prostorne hijerarhije featurea (from simpler to more complex)

DBNs
Main features:
- sastoje se od više slojeva RBM-ova (Restricted Boltzmann Machines)
- unsupervised learning (prvo uče reprezentacije podataka (features), pa se kasnije mogu tunirati za klasifikaciju
- Stohastičke neuronske jedinice (probabilistički pristup)
- popularne PRIJE pojave CNN-ova (posebno za generative learning i dimensionality reduction)

Similarities:
- obadvoje su multi-layered deep neural networks
- uče data representations hijerarhijski
- mogu se koristiti za klasifikaciju, feature extraction i pattern recognition

| Značajka            | CNN                                     | DBN                                  |
| ------------------- | --------------------------------------- | ------------------------------------ |
| Tip učenja          | Najčešće **supervizirano**              | **Nesupervizirano** (pre-trening)    |
| Struktura           | Konvolucijski slojevi + pooling + dense | Hijerarhija RBM-ova                  |
| Područje primjene   | Obrada slika, videa                     | Generativni modeli, feature learning |
| Način rada          | Deterministički                         | Probabilistički                      |
| Brzina i efikasnost | Brži, lakše trenira                     | Sporiji, teže trenira                |

- SNN-ovi omogućavaju da nadiđemo velike computational troškove kod običnih CNN-ova

- Spiking deep networks su predloženi kako bi se smanjio veliki računski trošak dubokih mreža

- Iskorištavaju specijalizirani hardver za spiking neural networks (SNNs)

- Konverzija iz analognih neuralnih mreža (ANNs) u SNNs uzrokuje gubitke performansi

- Glavni razlog gubitaka je prelazak s kontinuiranih (bez pojma vremena) ANNs na rijetko aktivirane, event-driven SNNs

- Analizira se utjecaj konverzije ANNs u SNNs u odnosu na parametre spike neurona, poput frekvencije aktivacije (firing rate) i praga aktivacije (threshold)

- Postoji set optimizacijskih tehnika za minimizaciju gubitka performansi u procesu konverzije za CNN-ove i fully connected deep networks
- Takve mreže nadmašuju sve prethodne SNN-ove rađene na MNISTU i jako dobro rade u vidu performansi

- Koristi se ReLU (rectified linear units) bez biasa za vrijeme treniranja, koristeći novu weight normalizaciju za reguliranje fire-ratea

- Cilj: fast&efficient pattern recognition

- Duboke neuronske mreže (konvolucijske) su fully connected feed forward neural networks
- Trenutno su jedna od najuspješnijih arhitektura za image classification

Record-breaking results za: handwriting recognition, scene labeling, CIFAR i ImageNet benchmarkse

Networks inspired by hierarchies of cortical visual information processing
Uspješne su, ali ima značajan trošak resursa pri treniranju i runnanju
Stoga, potreban je specijalizirani hardver + akcelaracija istog
Potreba za razvojem novih računalnih paradigmi koji će omogućiti uporabu deep networka za real-time praktične primjene

SNN-ovi su primarni kandidati za omogućavanje takve akceleracije

Nova metoda optimizacija za Spiking deep arhitekture ( i za full connected feed forward networke i za conv. networks)
Niska latencija + manje potrebnih računskih operacija u usporedbi s konvencionalnim computingom
Cilj: izgraditi biologically realistic neuarl networks

Neuromorphic plathorms => emuliranje brain-like spike-based računanja na analognom ili digitalnom hardveru
Puno efikasnije od CPUova i GPUova (posebno za spiking networkse)
Omogućavaju distribuirano, asinkrono event-based računanje
Skalabilno i s minimalnom latencijom
Sustavi se fokusiraju na trenutno aktivne djelove networka i tako štede energiju na drugim djelovima networka
Koriste input neuromorfnih senzora (poput silicon retine)
Kreiraju se sparse, frame-free, precizno tempirani streamovi evenata s puno manje latencije u usporedbi s frame-based pristupima

Treniranje spiking deep networka tipično ne koristi spike-based learning pravila, nego počinje s konvencionalnim ANN-ovima treniranima pomoću backpropagacije
Zatim se taj rate-based model konvertira u model sačinjen od jednostavnih spiking neurona

Malo je teško trenirati SNN-ove.
Teorija pokazuje da su SNN-ovi barem jednako računski moćni kao i njihovi analogni ekvivalenti (ANN-ovi), ali je u praksi teško postići ekvivalentne rezultate
Jedan pristup trenira spiking DBN-ove pomoću Siegert aproksimacije srednje brzine aktivacije (mean-firing-rate) LIF neurona kako bi se aproksimirale vjerojatnosti tijekom treniranja
Drugi pristup zahtijeva podešavanje parametara poput "leak" i "refractory period" u spiking mreži
Oba pristupa pate od značajnog gubitka točnosti klasifikacije u usporedbi s ne-spiking mrežama slične arhitekture
Nedavno je predložena metoda konverzije spiking ConvNet mreža koja uzima u obzir razlike između spiking i ne-spiking mreža, te postiže bolje performanse od prijašnjih metoda
Glavni izazovi su reprezentacija negativnih vrijednosti i bias-a u spiking neuronima
Ti problemi se izbjegavaju korištenjem ReLU aktivacija i postavljanjem svih bias vrijednosti na nulu
Max-pooling se zamjenjuje prostornim linearnim subsamplingom
I dalje postoji manji gubitak performansi nakon konverzije
Autori analiziraju izvore tih gubitaka i predlažu alate za optimizaciju
Zaključuju da ako se SNN-ovi pokreću u odgovarajućem režimu, mogu postići gotovo bezgubitnu konverziju i vrlo brzu klasifikaciju uz samo nekoliko izlaznih spikeova

* U potpuno povezanim feed-forward neuronskim mrežama (FCNs), svaki neuron u jednom sloju povezan je sa svim neuronima u sljedećem sloju, bez veza unutar istog sloja
* Nedavna istraživanja ponovno su pobudila interes za ovu arhitekturu zbog natjecateljskih rezultata
* Ključne točke uspješnog treniranja FCN-a su pravilna inicijalizacija težina kako bi se očuvao gradijent pogreške i regularizacija radi sprječavanja overfittinga
* Kombinacija dropout tehnike i ReLU aktivacija dovela je do značajnih poboljšanja performansi
* ReLU (Rectified Linear Unit) je nelinearna funkcija definirana kao xi = max(0, Σ(wij * xj))
* ReLU omogućuje jednostavnu i učinkovitu propagaciju signala kroz mrežu
* Aktivacije se iterativno ažuriraju sloj po sloj kako bi se ulaz propagirao do izlaznih neurona koji označavaju predikciju klase

* Trening se nastavlja pomoću standarne backpropagacije greške
* Gradijent funkcije greške se propagira unazad po layerima
* Računaju se lokalne derivacije da bi se updateali lokalni weightovi i minimizirala greška
* Trening služi za prilagodbu nasumično inicijalizirani matrice weightova koji opisuju veze između layera da bi se greška minimizirala koristeći stohastički gradijentni spust

* Konvolucijske neuronske mreže (ConvNets ili CNNs) su višeslojne feed-forward arhitekture koje koriste konvolucijske jezgre (kernels) kao detektore značajki
* Tipično se sastoje od naizmjeničnih slojeva konvolucije i prostornog subsamplinga (poolinga), uz nelinearnu aktivaciju između njih
* Svaki konvolucijski sloj generira skup feature mapa konvoluiranjem prethodnih aktivacija s jezgrama Wk i dodavanjem bias termina bk
* Aktivacija svakog feature mapa definira se kao xk = f(Wk * xl + bk), gdje je f nelinearna funkcija (ovdje ReLU)
* Jezgre reagiraju samo na male lokalne dijelove ulazne slike i primjenjuju se pomicanjem preko cijelog ulaza (weight sharing)
* Nakon konvolucije slijedi pooling ili subsampling sloj koji kombinira odgovore više feature detektora u jednu vrijednost
* U ovom radu korišten je **average pooling** radi bolje prenosivosti ConvNeta u SNN
* ConvNet smanjuje dimenzionalnost podataka dok istovremeno generira apstraktnije značajke
* Zbog manjeg broja težina u odnosu na potpuno povezane mreže, manja je mogućnost overfittinga
* Izlaz CNN-a čini spajanje svih feature mapa iz zadnjeg sloja, što se zatim koristi kao ulaz u jednostavnu potpuno povezanu mrežu za klasifikaciju
* Treniranje se vrši stohastičkim gradijentnim spuštanjem i backpropagacijom, uz dijeljenje težina u konvolucijskim slojevima

* Overfitting je čest problem kod velikih i dubokih neuronskih mreža
* Dropout tehnika djeluje kao regularizator koji sprječava overfitting
* Dropout slučajno isključuje određene neuronske jedinice (ulaze ili skrivene neurone) tijekom treniranja
* Na taj način se izbjegava prevelika specijalizacija i međusobna ovisnost skrivenih jedinica
* U ovom radu dropout se koristi u sklopu ReLU aktivacijske funkcije kao maska koja slučajno isključuje određene ReLU aktivacije
* Formula za ReLU s dropoutom: xi = max(0, Σ(wij * xj)) s vjerojatnošću dr, ili 0 inače
* Dropout stopa (dr) određuje udio jedinica koje se isključuju pri svakom trening koraku
* Tipična vrijednost dr je 0.5, što znači da se nasumično isključi polovica veza tijekom svake iteracije treninga
* Rezultat je povećana robusnost mreže i bolja generalizacija na nove podatke

Arhitektura FCN (Fully Connected Feed-forward Neural Networks)
* Svaki neuron u jednom sloju povezan je sa svim neuronima u sljedećem sloju.

* Nema poveznica unutar istog sloja (nema intra-layer konekcija).

* Takva mreža se zove feed-forward jer se informacija kreće samo u jednom smjeru – od ulaza prema izlazu

Dobre performanse
Ključni faktori:
- dobra inicijalizacija weightove => stabilno širenje gradijenta (bez gubitka signala kroz layere)
- regularizacija => spriječava overfittinga

Bitne tehničke komponente:

Dropout (regularizacijska tehnika)

Nasumično isključuje određene neurone tijekom treniranja → sprečava njihovu međusobnu ovisnost.

Time se model uči robustnije, smanjuje overfitting i poboljšava generalizaciju.
---

## 🔹 **ReLU-temeljene feed-forward neuronske mreže (FCN)**

### 🧠 Osnovna ideja

* **Feed-forward neuronska mreža (FCN)** je tip mreže u kojoj:

  * Svaki **neuron iz jednog sloja povezan je sa svim neuronima sljedećeg sloja** (*fully connected*).
  * **Nema veza unutar istog sloja** (*no intra-layer connections*).
* Informacija teče **jednosmjerno — od ulaza prema izlazu**.

---

### ⚙️ **Razlozi ponovne popularnosti**

* Nedavni uspjesi u istraživanjima pokazali su da FCN-ovi mogu **postići vrlo konkurentne rezultate**.
* Ključni preduvjeti za visoke performanse:

  * **Dobra inicijalizacija težina** → sprječava problem nestajanja ili eksplozije gradijenata i osigurava stabilno učenje.
  * **Regularizacija** → smanjuje rizik od **overfittinga** (prenaučenosti).

---

### 🔸 **Najvažnija poboljšanja**

1. **Dropout tehnika**

   * Tijekom treniranja **nasumično "isključuje" neke neurone**, tako da mreža ne postane previše ovisna o određenim značajkama.
   * Rezultat: **robustniji i generaliziraniji model**.

2. **ReLU (Rectified Linear Unit)**

   * Vrlo jednostavna, ali učinkovita **nelinearna aktivacijska funkcija**:
     [
     x_i = \max(0, \sum_j w_{ij}x_j)
     ]
   * Značenje:

     * ( x_i ): aktivacija neurona *i*
     * ( w_{ij} ): težina između neurona *j* i *i*
     * ( x_j ): izlaz neurona *j* iz prethodnog sloja
   * **Prednosti ReLU-a:**

     * Ubrzava učenje
     * Sprječava problem saturacije gradijenata
     * Daje **rijetke aktivacije** (mnogi neuroni imaju 0 → učinkovitija mreža)

---

### 🔹 **Kako se informacije šire**

* Mreža **sloj po sloj izračunava aktivacije** na temelju prethodnog sloja.
* Na kraju se **aktiviraju izlazni neuroni** koji predstavljaju rezultat modela (npr. klasnu oznaku).

---

### 🔧 **Proces treniranja**

* Koristi se **standardni algoritam povratnog širenja pogreške (backpropagation)**:

  * Pogreška na izlazu **propagira se unazad kroz mrežu**, sloj po sloj.
  * Računaju se **lokalne derivacije** za svaki neuron.
  * **Težine se ažuriraju** u smjeru koji minimizira ukupnu pogrešku.
* Optimizacija se izvodi pomoću **stohastičkog gradijentnog spusta (SGD)**.
* Težine su u početku **nasumično inicijalizirane**, a zatim se uče kroz iteracije.

---

### ✅ **Zaključak**

* Kombinacijom **ReLU aktivacija**, **dropout regularizacije**, i **dobro inicijaliziranih težina**,
  FCN-ovi mogu postići **vrlo visoke performanse** na standardnim skupovima podataka.
* Takva kombinacija je postala **temelj suvremenih dubokih neuronskih mreža**.

---

## 🔹 **Konvolucijske neuronske mreže (ConvNets / CNNs)**

### 🧠 **Osnovna ideja**

* **CNN** je **višeslojna feed-forward arhitektura** (kao FCN), ali:

  * Umjesto punih veza, koristi **konvolucijske filtre (kernels)** kao detektore značajki (feature detectors).
* Sastoji se od **izmjeničnih slojeva konvolucije i prostornog poduzorkovanja (subsampling/pooling)**, s **nelinearnom funkcijom aktivacije** između njih.

---

### ⚙️ **Konvolucijski sloj**

* Svaki konvolucijski sloj stvara **više “feature mapa”**.

* Svaka mapa ( x_k ) dobiva se **konvolucijom** aktivacija prethodnog sloja s odgovarajućim kernelom ( W_k ):
  [
  x_k = f(l * W_k + b_k)
  ]
  gdje je:

  * ( f ): aktivacijska funkcija (ovdje ReLU)
  * ( l ): aktivacija prethodnog sloja
  * ( * ): 2D konvolucijska operacija (valid-region)
  * ( b_k ): bias (pomak)

* Kernel (filter) **"klizi" po cijelom ulaznom prostoru** i reagira samo na **mala lokalna područja** (lokalna receptivna polja).
  → Time se mreža fokusira na **lokalne uzorke** (rubove, teksture, oblike).

---

### 🔸 **Pooling (subsampling) sloj**

* Slijedi iza konvolucijskog sloja.
* **Smanjuje dimenzionalnost podataka** kombiniranjem odgovora više detektora značajki u jedan izlaz.
* U ovom radu koriste se **average pooling slojevi** (prosječni kernel) — umjesto max poolinga — kako bi se mreža lakše prenijela u **spiking neuronsku mrežu (SNN)**.
* Aktivacija pooling sloja je kao i u jednadžbi (2), ali s fiksnim težinama:
  [
  W_{kij} = \frac{1}{\text{size}(W_k)}
  ]
  gdje je *size(Wk)* broj piksela u kernelu.

---

### 🔹 **Ključne prednosti CNN-ova**

1. **Smanjena dimenzionalnost podataka**

   * Naizmjenični slojevi konvolucije i pooling-a **postupno reduciraju prostorne informacije**, dok povećavaju **apstrakciju značajki**.

2. **Manji broj težina**

   * Zbog **dijeljenja težina (weight sharing)** u konvolucijskim slojevima, CNN-ovi imaju **znatno manje parametara** od potpuno povezanih mreža (FCN).
   * To **smanjuje overfitting** i ubrzava treniranje.

3. **Učinkovito učenje reprezentacija**

   * Donji slojevi uče **jednostavne uzorke** (rubovi, boje, teksture).
   * Viši slojevi kombiniraju te uzorke u **složenije značajke** (oblici, dijelovi objekata, cijeli objekti).

---

### 🔧 **Treniranje CNN-a**

* Izvodi se pomoću **stohastičkog gradijentnog spusta (SGD)** i **backpropagationa** — isto kao kod FCN-a.
* **Težine konvolucijskih filtera (Wk)** i težine završnog **klasifikacijskog sloja (FC sloj)** uče se zajedno.
* **Dijeljenje težina (weight sharing)** dodatno smanjuje broj parametara i stabilizira učenje.

---

### 🧩 **Izlaz mreže**

* **Sve feature mape iz posljednjeg konvolucijskog sloja se spajaju (concatenate)**.
* Dobiveni vektor ulazi u **jednostavnu potpuno povezanu mrežu (FCN)** koja služi kao **klasifikator**.

---

### ✅ **Zaključak**

* CNN-ovi kombiniraju **konvolucijske slojeve + pooling + ReLU + weight sharing**,
  čime:

  * smanjuju broj parametara,
  * ublažavaju overfitting,
  * i proizvode **sve apstraktnije značajke**.
* Na kraju, FC sloj klasificira izlaz → čitav sustav se trenira putem **SGD + backpropagation**.

---


---

## 🔹 **Dropout tehnika**

### ⚠️ **Problem: Overfitting**

* **Overfitting (prenaučenost)** je čest problem kod **velikih i dubokih neuronskih mreža**.
* Dogodi se kad se mreža **previše prilagodi trening podacima**, pa loše generalizira na nove (testne) podatke.

---

### 💡 **Rješenje: Regularizacija**

* Da bi se izbjegao overfitting, uvode se **regularizacijske metode**.
* Jedna od najuspješnijih i najpopularnijih je upravo **dropout tehnika**.

---

### 🧠 **Što je dropout**

* Tijekom učenja, **nasumično se “isključuju” (onemogućuju) određene jedinice (neuroni)**.
* Time se sprječava da se neuroni **međusobno previše “naviknu” jedni na druge** (tj. sprječava **ko-adaptacija**).
* To tjera mrežu da nauči **robustnije značajke**, koje bolje generaliziraju.

---

### 🔧 **Kako se dropout primjenjuje**

* Dropout se u ovom radu koristi **unutar ReLU aktivacijske funkcije**, kao **maska** koja slučajno onemogućuje dio ReLU aktivacija.
* Time se **povećava robusnost mreže**.

---

### 🔹 **Matematički prikaz (jednadžba 3)**

[
x_i =
\begin{cases}
\max(0, \sum_j w_{ij}x_j), & \text{s vjerojatnošću } (1 - d_r) \
0, & \text{inače}
\end{cases}
]
gdje je:

* ( x_i ) → aktivacija neurona *i*
* ( w_{ij} ) → težina između neurona *j* i *i*
* ( x_j ) → aktivacija prethodnog neurona
* ( d_r ) → **dropout stopa (dropout rate)**, tj. vjerojatnost da će se neuron isključiti

---

### 🔁 **Mehanizam učenja**

* Na **svakom trening koraku** (iteraciji), **donosi se nova nasumična odluka za svaki neuron** — hoće li biti aktivan ili ne.
* Tijekom inferencije (testiranja), dropout se **isključuje**, ali se izlazi **skaliraju** tako da reflektiraju prosječan učinak tijekom treniranja.

---

### 🔢 **Tipične vrijednosti**

* U praksi se često koristi **dropout rate ( d_r = 0.5 )**
  → znači da se **polovica veza nasumično isključi** u svakom koraku treniranja.

---

### ✅ **Ključne prednosti**

* Smanjuje overfitting.
* Potiče mrežu da nauči **distribuirane i stabilnije reprezentacije**.
* Poboljšava **generalizaciju i otpornost** na šum u podacima.
* Jednostavan i vrlo učinkovit dodatak koji se može koristiti s bilo kojom aktivacijom (ali ReLU + dropout = zlatna kombinacija).

---

- U klasičnim ANN-ovima, cijeli input vector "unosi" se istovremeno, pa procesira layer po layer i stvara 1 output vrijednost
- U SNN-ovima, inputi su tipično streamovi evenata i neuroni stvaraju spikeove na temelju tih evenata
- Spikeovi služe za komunikaciju sa svim layerima i na kraju dovode do "firea" kod output neurona
- Fire se sumira kroz vrijeme
- Input i output su pseudosimultani
- Time-varying inputi se mogu efikasno procesirati
- super za račuanje na specijaliziranim hardverima

---

## 🔹 **Spiking neuron model – Integrate-and-Fire (IF)**

### 🧠 **Osnovna ideja**

* Koristi se **jednostavni Integrate-and-Fire (IF)** model neurona.
* To je **biološki inspiriran model**, gdje neuron akumulira (integrira) ulazne impulse i ispaljuje *spike* kad dosegne određeni prag.

---

### ⚙️ **Evolucija membranskog napona**

* Membranski napon neurona označava se kao ( v_{mem}(t) ).
* Njegova promjena kroz vrijeme opisana je diferencijalnom jednadžbom:
  [
  \frac{dv_{mem}(t)}{dt} = \sum_i w_i \sum_s \delta(t - s_i)
  ]
  gdje je:

  * ( w_i ) → težina *i*-tog dolaznog sinapsnog spoja
  * ( \delta(t - s_i) ) → **Dirac delta funkcija** koja predstavlja dolazak spike-a u trenutku ( s_i )
  * ( S_i = {t^0_i, t^1_i, ...} ) → skup vremena kada *i*-ti presinaptički neuron puca (emitira spike)

---

### ⚡ **Način rada neurona**

1. **Integracija:**

   * Neuron **zbraja dolazne impulse** (spikes) ponderirane težinama ( w_i ).
   * Time se povećava njegov membranski potencijal ( v_{mem} ).

2. **Ispaljivanje spike-a (Fire):**

   * Kad ( v_{mem} ) **prijeđe prag pobude ( v_{thr} )** → neuron **generira spike** (akcijski potencijal).

3. **Resetiranje:**

   * Nakon što neuron ispali spike, njegov membranski napon se **resetira na vrijednost ( v_{res} )**.
   * Zatim ciklus integracije počinje iznova.

---

### ⏱️ **Diskretizacija u simulacijama**

* U simulacijama se ovaj **kontinuirani model** aproksimira **diskretnim vremenskim koracima od 1 ms**.
  → To znači da se napon i spike-ovi ažuriraju u **milisekundnim intervalima**.
  → Takva aproksimacija olakšava digitalnu implementaciju modela (npr. u PyTorch-u ili simulacijskim alatima).

---

### ✅ **Ključne značajke IF modela**

* Jednostavan, ali učinkovit model neuronskog ponašanja.
* Hvata osnovnu dinamiku biološkog neurona (integracija i ispaljivanje).
* Koristi se kao **temelj za izgradnju složenijih SNN arhitektura** (npr. LIF – Leaky Integrate-and-Fire).
* Idealno za **simulacije s vremenskom diskretizacijom** i **neuralne čipove (neuromorfne sustave)**.

---

- Spiking network conversion

- Konverzija deep ANN-ova u SNN-ove
- Redukcija gubitka perfomransi tijekom konverzije
- Normalizacija + analiza firing rateova i thresholda

---

## 🔹 **Veza između ReLU ANNs i SNN-ova**

1. **ReLU ≈ firing rate IF neurona**

   * ReLU može se smatrati **aproksimacijom broja spike-ova IF neurona** u zadanom vremenskom prozoru.
   * Bez refraktornog perioda, izlaz ReLU-a je proporcionalan broju spike-ova.

2. **Prednosti ReLU-a za treniranje**

   * Njihova **piecewise linear derivacija** omogućuje **jednostavne i stabilne update-e težina**.
   * Za klasifikacijske zadatke, važna je samo **maksimalna aktivacija izlaznog sloja**, pa se **sve stope može skalirati konstantom**.

3. **Skala težina je važna**

   * Ako je bias fiksiran na 0, jedino što utječe su **omjeri težina među neuronima i njihov prag (threshold)**.

---

## 🔹 **Recept za konverziju ANN → SNN**

1. Koristiti **ReLU aktivacije** za sve jedinice mreže.
2. Fiksirati **bias na nulu** i trenirati mrežu normalnim **backpropagationom**.
3. **Izravno mapirati težine** iz ReLU mreže u IF neuronsku mrežu.
4. Primijeniti **normalizaciju težina** (weight normalization) → postiže se **skoro bez gubitka točnosti i brža konvergencija**.

> Ove metode rade za **FCN i ConvNet** arhitekture.

---

## 🔹 **Potencijalni gubici performansi nakon konverzije**

1. **Nedovoljno ulaza za spike**

   * Neuron ne prelazi prag → njegova frekvencija spike-ova je manja od očekivane.

2. **Previše ulaza / over-aktivacija**

   * ReLU predviđa više od jednog spike-a po timestepu.
   * Može se dogoditi zbog:

     * Previše spike-ova u jednom timestepu.
     * Težine ulaza veće od praga neurona.

3. **Probabilistička priroda spike-ova**

   * Spike-trains nisu uniformni → može doći do **prekomjerne ili nedovoljno jake aktivacije određenih značajki**.

---

## 🔹 **Kako ublažiti probleme**

* **Smanjiti timestep simulacije** → smanjuje broj spike-ova po timestepu.
* **Povećati trajanje simulacije** → sprječava nedovoljnu aktivaciju.
* **Pronaći ravnotežu između:**

  * Spiking threshold (prag za spike)
  * Težina ulaznih sinapsi
  * Firing rate ulaza

> Visok prag (ili niske ulazne težine) → smanjuje over-aktivaciju, ali povećava under-aktivaciju.
> Nizak prag (ili visoke težine) → smanjuje under-aktivaciju, ali povećava over-aktivaciju.

* **Ključ:** Samo **omjer praga i ulaznih težina** određuje integriranu vrijednost do spike-a, ne njihove apsolutne vrijednosti.

---

## 🔹 **Rješenje za preciznu konverziju**

* Umjesto ručnog podešavanja:

  * **Izračunati faktore reskaliranja težina** → smanjuju greške iz **tri gore navedena uzroka** (under-aktivacija, over-aktivacija, neidealni spike-trains).

---

- Smanjenje timestampa u simulaciji može pomoći za smanjenje broja input spikeova po timestepu i povećanje trajanja simulacije pomaže izbjeći nedovoljne aktivacije

- Bitno je izbalansirati spiking thresholdse, input weights i input firing rates
- Visoki spiking threshold (ili niski input weights) smanjuju errore uzrokovane over-aktivacijom i ne-idealnim spikre trainovima, ali povećava greške zbog under-aktivacije i obratno

- samo omjer spiking thresholda i input weightova određuje akumuliranu količinu inputa za spiking, ali ne i vrijednosti pojedinih impulsa

🔹 Glavni doprinos rada

Uvedena je nova metoda normalizacije težina (weight normalization).

Cilj: dovesti mrežu u stabilan režim rada, gdje se izbjegavaju problemi poput:

neuroni koji previše spikaju (overactivation),

neuroni koji premalo spikaju (underactivation),

netočne procjene izlaza zbog previsokih ReLU aktivacija.

🔹 Ideja normalizacije

Želimo ograničiti aktivacije tako da:

ReLU ne precjenjuje izlaz neurona.

Neuron ne može proizvesti više od jednog spike-a u istom trenutku.

🔹 Model-based normalizacija (konzervativna metoda)

Za svaki sloj razmatraju se sve moguće pozitivne aktivacije.

Izračuna se maksimalni mogući pozitivni ulaz u sloj.

Sve težine u tom sloju se skaliraju tako da taj maksimalni ulaz proizvede najviše jedan spike.

🔹 Prednosti

Mreža postaje robustna na vrlo visoke ulazne stope (input rates).

Eliminiraju se gubici zbog previše ulaznih spike-ova.

🔹 Nedostatak

Potrebno više vremena da neuron akumulira dovoljno dokaza za spike.
→ dulje vrijeme simulacije, sporija reakcija.

🔹 Kada koristiti

Ako je visoka točnost klasifikacije prioritet.

Ako su dulja vremena uzorkovanja prihvatljiva.

🔹 Naziv metode

Zove se Model-Based Normalization jer koristi samo težine mreže —
ne zahtijeva podatke iz stvarnih uzoraka (temelji se na modelu, ne na podacima).

Savršeno! Evo ti **detaljne natuknice** iz tog dijela o **data-based normalizaciji težina** — jasno i sažeto:

---

## 🔹 **Data-Based Normalization (normalizacija temeljena na podacima)**

### 🔸 Osnovna ideja

* Umjesto najgoreg mogućeg slučaja (kao kod model-based metode),
  koristi se **stvarno ponašanje mreže na trening skupu** za procjenu tipičnih aktivacija.
* Time se dobiva **manje konzervativna** metoda koja čuva točnost, ali ubrzava obradu.

---

### 🔸 Postupak

1. Nakon što se trenira ReLU mreža,
   **propagira se cijeli trening skup** kroz mrežu.
2. Pohranjuju se **ReLU aktivacije** za sve neurone.
3. Težine se **normaliziraju** prema **maksimalnoj aktivaciji** koja se pojavila u trening skupu,
   tako da ta aktivacija proizvede **samo jedan spike**.
4. U obzir se uzima i **maksimalna pojedinačna ulazna težina** —
   da se spriječi situacija gdje **jedan spike nosi previše težine**,
   prisiljavajući neuron da spike-a više puta u istom timestepu.

---

### 🔸 Prednosti

* **Manje konzervativna** od model-based metode → **brža konvergencija**.
* **Zadržava gotovo svu točnost** (minimalan gubitak performansi).
* **Znatno kraće vrijeme integracije dokaza** (kraće trajanje simulacije).
* Idealna za **ravnotežu između točnosti i brzine reakcije**.

---

### 🔸 Ograničenja

* **Nema jamstva** da će performanse biti jednake na test skupu,
  ali ako je trening skup **reprezentativan**, rezultati su **vrlo pouzdani**.

---

### 🔸 Kada koristiti

* Kad želiš **visoku točnost** + **kratke latencije** (brz rad).
* Odlična za **praktične implementacije** gdje trebaš balans performansi i brzine.

---

### 🔸 Ključna razlika od model-based metode

| Značajka          | Model-Based Normalization   | Data-Based Normalization                  |
| ----------------- | --------------------------- | ----------------------------------------- |
| Temelj            | Na težinama modela          | Na stvarnim aktivacijama iz trening skupa |
| Konzervativnost   | Visoka (sigurna, ali spora) | Niska (brža, ali s rizikom)               |
| Brzina simulacije | Spora                       | Brza                                      |
| Točnost           | Vrlo visoka                 | Gotovo jednaka, uz manju latenciju        |
| Naziv             | Model-based                 | Data-based                                |

---
Odlično! 👏
Ovo što si zalijepio su pseudokodovi za **model-based** i **data-based** normalizaciju težina — i točno tako se u radu i predstavljaju (Algorithm 1 i Algorithm 2).
Sad ću ti ih **prepisati i pojasniti korak po korak na hrvatskom**, da dobiješ jasan intuitivan osjećaj što svaka verzija radi i u čemu se razlikuju.

---

## 🔹 **Algorithm 1 – Model-Based Weight Normalization**

### 💡 Ideja

Cilj: osigurati da **nijedan neuron ne može proizvesti više od jednog spike-a** za maksimalni mogući ulaz.
→ Mreža postaje vrlo stabilna i robusna, ali zahtijeva dulju simulaciju.

### 🧠 Logika pseudokoda

```python
for layer in layers:
    max_pos_input = 0

    # 1️⃣ Nađi maksimalni mogući pozitivan ulaz u sloj
    for neuron in layer.neurons:
        input_sum = 0
        for input_wt in neuron.input_wts:
            input_sum += max(0, input_wt)
        max_pos_input = max(max_pos_input, input_sum)

    # 2️⃣ Normaliziraj sve težine u sloju
    for neuron in layer.neurons:
        for input_wt in neuron.input_wts:
            input_wt = input_wt / max_pos_input
```

### 🔍 Objašnjenje

* Za svaki sloj se traži **najveća moguća suma pozitivnih težina** (pretpostavlja se da svi ulazi mogu biti maksimalno aktivni).
* Sve težine se potom **skaliraju** tako da ta maksimalna kombinacija proizvodi **jedan spike**.
* Dakle: sigurnije, ali sporije — treba više vremena da neuron „nabere” dovoljno energije za spike.

---

## 🔹 **Algorithm 2 – Data-Based Weight Normalization**

### 💡 Ideja

Koristi **stvarne aktivacije iz trening skupa** umjesto najgoreg slučaja.
→ Brža mreža, zadržava točnost, ali malo manje konzervativna.

### 🧠 Logika pseudokoda

```python
previous_factor = 1

for layer in layers:
    max_wt = 0
    max_act = 0

    # 1️⃣ Pronađi najveću težinu i najveću ReLU aktivaciju u sloju
    for neuron in layer.neurons:
        for input_wt in neuron.input_wts:
            max_wt = max(max_wt, input_wt)
        max_act = max(max_act, neuron.output_act)

    # 2️⃣ Izračunaj faktor skaliranja
    scale_factor = max(max_wt, max_act)
    applied_factor = scale_factor / previous_factor

    # 3️⃣ Skaliraj težine u sloju
    for neuron in layer.neurons:
        for input_wt in neuron.input_wts:
            input_wt = input_wt / applied_factor

    # 4️⃣ Spremi faktor za sljedeći sloj
    previous_factor = scale_factor
```

### 🔍 Objašnjenje

* Nakon treniranja ReLU mreže, kroz nju se propušta **trening skup** i bilježe se stvarne **ReLU aktivacije**.
* Računa se **maksimalna aktivacija** i **maksimalna težina** u sloju.
* Na temelju toga se određuje faktor skaliranja koji osigurava da ni najjača aktivacija neće proizvesti više od jednog spike-a.
* Svaki sloj koristi svoj **“applied_factor”**, ali i **prenosi informaciju o prethodnom sloju** da očuva proporcionalnost.

---

## ⚖️ **Sažetak razlika**

| Značajka           | Model-Based                 | Data-Based                           |
| ------------------ | --------------------------- | ------------------------------------ |
| Na čemu se temelji | Maksimalni mogući ulaz      | Stvarne aktivacije s trening skupa   |
| Konzervativnost    | Visoka (sigurna, ali spora) | Niska (brža, ali može malo varirati) |
| Vrijeme simulacije | Dulje                       | Kraće                                |
| Točnost            | Vrlo visoka                 | Gotovo identična                     |
| Pogodno za         | Eksperimentalnu robusnost   | Praktične implementacije             |

---


---

## 🔹 **Eksperimentalni setup — A. Dataset**

### 🧠 **Korišteni skup podataka**

* Odabran je **MNIST dataset** — najpoznatiji i najčešće korišten skup u *machine learningu*.
* Sastoji se od **ručno pisanih znamenki (0–9)**, svaka u formatu **28×28 piksela**, **sivih tonova** (grayscale).

---

### 📊 **Struktura podataka**

* **Trening skup**:

  * 60.000 slika ručno pisanih znamenki.
  * Slike su prikupljene iz **poštanskih kodova (postal codes)**.
  * Svaka slika ima pripadajuću oznaku (label) od **0 do 9**.
* **Testni skup**:

  * 10.000 slika znamenki, korištene isključivo za evaluaciju modela.

---

### 🏆 **Referentne točnosti (baseline rezultati)**

* **Najveća točnost klasične (nespiking) mreže**:

  * **99.55%**, postignuto pomoću **Maxout Networks** ([23]).
  * Ova vrijednost je “state-of-the-art” bez korištenja data augmentationa.

* **Najveća točnost prethodne spiking implementacije**:

  * **98.30%**, postignuto pomoću **spiking konvolucijskih mreža (spiking ConvNets)** ([24]).

---

### 📈 **Zaključak**

* MNIST je izabran jer je:

  * **standardiziran** → omogućuje lako uspoređivanje s drugim modelima,
  * **dovoljno jednostavan** za brze eksperimente,
  * ali i **dovoljno izazovan** da pokaže učinkovitost konverzije ANN → SNN.

---


---

### 🔹 Eksperimentalne arhitekture

#### 1. **Fully-connected network (FCN)**

* Struktura: **784–1200–1200–10** (2 skrivena sloja po 1200 neurona).
* Svi neuroni su **povezani između slojeva**.
* **Trening setup:**

  * Learning rate: **1**
  * Momentum: **0.5**
  * Batch size: **100**
  * Epochs: **50**
  * Dropout: **50%**
  * Random inicijalizacija težina u rasponu **[-0.1, 0.1]**
* **Rezultati:**

  * Train accuracy: **99.87%**
  * Test accuracy: **98.68%**

---

#### 2. **Convolutional neural network (ConvNet)**

* Arhitektura: **28x28–12c5–2s–64c5–2s–10o**

  * 12 konvolucijskih jezgri 5x5
  * 2x2 prosječno subsampliranje
  * 64 konvolucijske jezgre 5x5
  * 2x2 prosječno subsampliranje
  * Potpuno povezani izlazni sloj od 10 neurona (za 10 klasa znamenki)
* **Trening setup:**

  * Learning rate: **1**
  * Batch size: **50**
  * Momentum: **0**
  * Dropout: **50% na kernelima**
  * Bias: **0**
  * Epochs: **50**
  * **Bez augmentacije** dataset-a
* **Rezultati:**

  * Train accuracy: **99.19%**
  * Test accuracy: **99.14%**

---

### 🔹 Pretvorba u Spiking IF mreže

* Najbolji ReLU modeli iz obje arhitekture su **konvertirani** u **spiking IF (Integrate-and-Fire)** mreže.
* **Grid search** je korišten za pronalazak optimalnih kombinacija:

  * **Input rate**: {25, 50, 100, 200, 400, 1000 Hz}
  * **Threshold (v_thr)**: {0.25, 0.5, 1, 2, 4, 10, 20}

---

### 🔹 Normalizacija težina

#### a) **Model-based normalization (algoritam 1)**

* Znatno smanjuje težine svakog sloja.
* FCN težine smanjene za:

  * Faktor 0.08 (prvi sloj)
  * Faktor 0.045 (drugi sloj)
* **Nije primijenjena na izlazni sloj**.
* ConvNet težine:

  * Conv1: 0.1657
  * Conv2: 0.1238

#### b) **Data-based normalization (algoritam 2)**

* Lagano prilagođava težine, čini mrežu otpornijom na visoke input rateove.
* FCN faktori:

  * 0.37, 1.25, 0.8
* ConvNet faktori:

  * Conv1: 0.1657
  * Conv2: 1.0021
  * Output: 1.19
* Povećanje težina u izlaznom sloju zbog **premale aktivacije** tijekom treninga.

---

Spiking input
Vrijednosti intenziteta na MNIST slikama su bile normalizirane u vrijednostima između 0 i 1.
Na temelju tih vrijednosti, korištenjem Poissonove distribucije, spike trains su bili generirani za svaki piksel u slici, s firing rateom proporcionalnim s intenzitetom piksela

Što znači „spiking input“ za MNIST slike (detalnije)

Normalizacija piksela

Intenzitet piksela 
𝐼
𝑖
𝑗
I
ij
	​

 je skaliran u raspon 
[
0
,
1
]
[0,1].

0 = potpuno crno (nema svjetla), 1 = maksimalna svjetlina.

Pretvaranje intenziteta u firing rate

Za svaki piksel definiramo firing rate (stopu pucanja) 
𝑟
𝑖
𝑗
r
ij
	​

 proporcionalnu intenzitetu:

𝑟
𝑖
𝑗
=
𝐼
𝑖
𝑗
×
𝑟
max
r
ij
	​

=I
ij
	​

×r
max
	​


𝑟
max
r
max
	​

 je maksimalna stopa (npr. 100 Hz, 400 Hz, 1000 Hz — ovisno o eksperimentu).

Dakle, bijeli piksel intenziteta 1 generira spike-ove sa stopom 
𝑟
max
r
max
	​

, tamni piksel intenziteta 0 ne generira spikes.

Poissonov proces za spike-train

Spike-ovi se modeliraju kao Poissonov proces s intenzitetom 
𝑟
𝑖
𝑗
r
ij
	​

.

U kontinuiranom vremenu: broj spike-ova u intervalu 
[
0
,
𝑇
]
[0,T] slijedi Poissonovu distribuciju s parametrom 
𝑟
𝑖
𝑗
𝑇
r
ij
	​

T.

Diskretna aproksimacija (korisna za simulacije): s vremenskim korakom 
𝑑
𝑡
dt (npr. 
𝑑
𝑡
=
1
 ms
=
0.001
 s
dt=1 ms=0.001 s), u svakom koraku generiraš Bernoullijevu odluku s vjerojatnošću:

𝑝
=
𝑟
𝑖
𝑗
⋅
𝑑
𝑡
p=r
ij
	​

⋅dt

tj. u svakom timestepu piksel puca s vjerojatnošću 
𝑝
p. Ovo je standardna i vrlo dobra aproksimacija Poisson procesa.

Zašto Poisson?

Poisson spike-trains imaju nezavisne inter-spike intervale i stohastičnost nalik biologiji.

Daje varijaciju u ulazu (ne determinističke spike-ove) što testira robusnost SNN-a

Evo kako to možemo izvući i objasniti na hrvatskom, korak po korak:

---

### **Evaluacija rezultata konverzije ReLU → SNN**

1. **Cilj**

   * Provjeriti koliko dobro spiking IF mreže mogu replicirati performanse originalnih ReLU mreža.

2. **Postupak evaluacije**

   * Originalna ReLU mreža je trenirana i postavlja ciljnu točnost (`target performance`) za spiking mrežu.
   * Spike-based mreže se simuliraju za **0.5 s po slici**.
   * Parametri spike mreže (input rate i threshold) su podešavani **grid searchom** za najbolje performanse.

3. **Vrste spiking mreža koje se evaluiraju**

   1. **Najbolja spiking IF mreža** – dobivena grid searchom parametara.
   2. **Data-normalized mreža** – težine su prilagođene prema stvarnim aktivacijama trening seta, bez podešavanja hyperparametara.
   3. **Model-normalized mreža** – težine su skalirane prema maksimalnim mogućim aktivacijama (konzervativnija metoda).

4. **Zaključci iz rezultata**

   * **Data-normalized mreža** gotovo replicira točnost originalne ReLU mreže **bez potrebe za grid searchom**.
   * U praksi, **dovoljno je simulirati samo nekoliko desetaka milisekundi** po slici da se postigne performansa usporediva s originalnom mrežom.
   * Model-normalized mreža je konzervativnija, često zahtijeva duže simulacije zbog smanjenih težina, ali eliminira probleme s previše spike-ova u jednom timestepu.

5. **Praktična implikacija**

   * Data-based normalizacija omogućuje **brzu i preciznu konverziju ReLU mreža u SNN**.
   * Spike simulacije mogu biti vrlo kratke (`tens of milliseconds`) i i dalje postižu visoku točnost.
   * Pokazuje da SNN-ovi mogu biti gotovo jednako učinkoviti kao i standardne ANN-ovi, ali koriste **temporalnu kodiranu informaciju** i stohastičke spikeove.

---


Brainchip.com
---

## 🧠 BrainChip Akida – Neuromorfni AI procesor

### 🔍 Što je Akida?

* **Neuromorfni čip** inspiriran ljudskim mozgom.
* **Event-based arhitektura**: obrađuje samo značajne podatke, čime se postiže visoka energetska učinkovitost i niska latencija.
* Omogućuje **učenje u stvarnom vremenu** na uređaju, bez potrebe za stalnom vezom s oblakom ([BrainChip][1]).

### ⚙️ Ključne značajke

* **Sparsity princip**: obrađuje samo podatke koji donose vrijednost, ignorirajući nule i neaktivne informacije ([BrainChip][2]).
* **Spiking Neural Networks (SNNs)**: neuronske jedinice aktiviraju se samo kada je to potrebno, slično ljudskom mozgu ([eejournal.com][3]).
* **On-chip učenje**: omogućuje treniranje modela direktno na uređaju, smanjujući potrebu za obradom u oblaku ([BrainChip][1]).

### 🧩 Arhitektura

* **Modularna struktura**: do 256 čvorova povezano u mrežu, svaki s četiri Neural Processing Unit-a (NPU).
* **Fleksibilnost**: NPUs mogu biti konfigurirani kao konvolucijski ili potpuno povezani slojevi.
* **Skalabilnost i kompaktnost**: omogućuje primjenu u različitim uređajima, od IoT senzora do autonomnih sustava ([BrainChip][4]).

### 🌐 Primjene

* **Edge AI**: obrada podataka na uređaju u stvarnom vremenu.
* **Industrijska automatizacija**: nadzor proizvodnih linija i prediktivno održavanje.
* **Pametni gradovi i IoT**: analiza podataka s senzora za optimizaciju resursa.
* **Zdravstvo**: detekcija anomalija u medicinskim uređajima i nosivim tehnologijama.

---

BrainChip nudi vlastiti razvojni alat pod nazivom **Akida Development Environment (ADE)**, koji je sada besplatan i dostupan za preuzimanje. 🎉

---

## 🧰 Akida Development Environment (ADE)

### 🔧 Što je ADE?

* **MetaTF** je glavni okvir unutar ADE-a, temeljen na Pythonu i inspiriran Keras API-jem. Omogućuje razvoj, treniranje i testiranje neuronskih mreža na Akida neuromorfnoj platformi.
* Uključuje:

  * **Akida Simulator**: softverska implementacija Akida NSoC-a za simulaciju modela.
  * **CNN2SNN**: alat za konverziju konvolucijskih modela u spiking neuronske mreže.
  * **QuantizeML**: alat za kvantizaciju modela s niskobitnim težinama i aktivacijama.
  * **Akida Model Zoo**: zbirka unaprijed obučenih modela za jednostavan početak rada. ([doc.brainchipinc.com][1])

### 🧠 Radni tok u ADE-u

1. **Izgradnja modela**: Koristi Keras ili model iz BrainChip Model Zoo.
2. **Kvantizacija**: Primijeni QuantizeML za smanjenje preciznosti modela.
3. **Konverzija**: Upotrijebi CNN2SNN za prilagodbu modela Akida platformi.
4. **Simulacija i testiranje**: Pokreni model u Akida Simulatoru ili na stvarnom AKD1000 hardveru. ([doc.brainchipinc.com][2])

### ☁️ Akida Cloud

Za brži početak, BrainChip nudi **Akida Cloud** – platformu koja omogućuje razvoj i testiranje modela bez potrebe za lokalnim hardverom. Idealno za prototipiranje i eksperimentiranje. ([BrainChip][3])

---

- Uklanjaju se podaci, weightovi i aktivacije koje ne donose značajne informacije

- Sparse princip => sparse data, sparse weights, sparse activations
- Sparse = rijedak / razrijeđen

- U neuronskim mrežama, “sparse” znači da većina neurona ili konekcija ne šalje signal u svakom trenutku.

- Samo oni neuroni koji su stvarno “aktivni” zbog značajnog inputa zapravo šalju spike (impuls).

- Prednost sparse pristupa

- Manja potrošnja energije – čip ne troši resurse na nepotrebne izračune.

- Brža obrada – jer se procesira samo mali dio podataka.

- Efikasno u stvarnom vremenu – idealno za edge AI i senzore koji stalno prikupljaju podatke.

- Kako to izgleda u praksi

- Recimo da kamerom snimaš scenu: ako se većina scene ne mijenja, neuroni koji “prate” neaktivne dijelove ne šalju spike.

- Samo neuroni koji detektiraju pokret ili promjenu podataka šalju signal i aktiviraju daljnju obradu.

- Veza sa Spiking Neural Networks (SNN)

- Sparse priroda Akida čipova se savršeno uklapa u SNN: spikeovi se događaju samo kad je potrebno, slično ljudskom mozgu.

- Za razliku od klasičnih CNN ili DNN gdje se cijela matrica propagira kroz mrežu, ovdje većina neurona miruje dok ne dođe do bitnog događaja.

- Sparse data => streaming inputi konvertiraju se u eventa na hardverskoj razini, smanjuje se obujam podataka za čak 10 puta prije nego procesiranje počne. Tradicionalni CNN-ovi procesiraju svaki ulazni datapoint, neovisno o promjeni. Brainchip filtrira input na hardverskoj razini i reagira samo na nove relevantne podatke
- Sparse weights => nepotrebni weightovi se uklanjaju i komprimiraju, smanjuje se veličina modela i računalna složenost za čak 10x
- Sparse activations => Samo ključne aktivacijske funkcije šalju podatke u sljedeće slojeve, smanjujući računanje u narednim slojevima do 10 puta.

- BITNI PRINCIPI:
- event-driven
- process only when needed (computation se obavlja samo kad se event treba obraditi; smanjuje se potrošnja energije i workload)
- communicate essentials (nodevi u neuralnoj mreži dijelie podatke samo kad je potrebno; izbjegava se komunikacijski overhead koji bezveze troši energiju)
- keep data close to compute (memorije je distribuirana i nalazi se blizu računalnih nodeva da se smanji latencija i potrošnja struje)
- focus on development, not owerhead (intelligent runtime + simple API...navodno lako za koristit...vidit ćemo :D )
- learn and adapt on device (on-chip learning...uređaji se mogu personalizirati i adaptirati bez clouda)
- reduce CPU load (smanjenje ili uklanjanje potrebe za uporabom CPU-a)
- fully digital and proven in silicon (u potpunosti digitalan dizajn; skalabilan, portabilan i spreman za produkciju)
- built-in privacy (podaci su privatni jer se svi računi obavljaju lokalno i samo weights se spremaju za učenje)
- podržava rad s CNN-ovima, DNN-ovima, RNN-ovima i sl. Omogućava pretvorbu istih u SCNN-ove
- more se pokrenut na FPGA, AKIDA hardveru ili u simulatorima

- Podržavaju razne arhitekture:
---

### 🖼️ CNNs and Spatio-Temporal CNNs

* Optimizirane za **prostorne (spatial) i vremenski ovisne (time-aware) zadatke**.
* Idealne za: **prepoznavanje slika**, **detekciju gesta**, **analizu vibracija**.
* Rade s podacima koji imaju i **prostorne i vremenske dimenzije**.

---

### ⏱️ State Space Models (SSMs)

* Nova klasa neuronskih mreža koja **kombinira temporalnu svijest i efikasnost u treniranju**.
* **Bolje performanse od tradicionalnih RNNs** (LSTM, GRU) u skalabilnosti i brzini treniranja.
* Pogodne za **zadace gdje treba pratiti stanje kroz vrijeme**.

---

### 🎯 Temporal Event-Based Neural Networks (TENNs™)

* Idealne za **sve što uključuje kretanje** – prate streaming podatke kroz vrijeme.
* Poboljšavaju SSMs dodavanjem **event-based awareness**.
* Pojednostavljuju: **motion tracking**, **object detection**, **audio processing**.
* Koriste **manje memorije i računanja** od transformera.

---

Zašto su opisani SCNN-ovi bolji nego tradicionalni?
- Parallel training => izrazito brži od konkurencije s arhitekturama dizajniranima za paralelni rad
- Efficiency => manji modeli s manje parametara i manje memorijskog overheada
- Stable and reliable => konzistentan trening i lakši deployment na edge devices

################################################## BRAINCHIPS ##########################################################
Dmitry Ivanov&co - Neuromorphic AI systems
- Moderni AI sustavi bazirani na von Neumann arhitekturei i klasičnim neural mrežama imaju mnoge nedostatke u usporedbi s mozgom
- Pregled dostupnih neuromorfnih čipova => TrueNorth, Loihi, Tianjic, SpiNNaker, BrainScaleS, NeuronFlow, DYNAP, Akida
- Klasifikacija neuromorfnih sustava na temelju brain featuresa koji koriste
- Neuronske mreže, paralelizam i asinkronost, prijenos informacija pomoću impulsa, lokalno učenje, sparsity, analogni in-memory computing

- Bitno je brzo obavljanje brojnih repetitivnih paralelnih operacija
- Bilo bi idealno kreirati AI algoritme spojene s hardverom na kojem rade (zato jer zapravo hardver određuje dostupnost i efektivnost AI algoritama

- Glavni problem Von Neumann Arhitekture => odvajanje memorije i operacija
- Operacije se izvršavaju u obliku programa (sekvence strojnih uputa)
- Procesor obavlja instrukcije => više argumenata koje prima od procesnih registara (male, ali brze memorijske ćelije locirane na procesoru)
- Instrukcije i većina podataka se pohranjuju u memoriju koja je odvojena od procesora
- Procesor i memorija spojeni su data busem preko kojeg procesor prima instrukcije i podatke iz memorije

- Prvi bottleneck: ograničena propusnost podataka između memorije i procesora
- Data bus većinom šalje privremene izračuna prema RAM-u/iz RAM-a tijekom rada programa
- Throughtput data busa je puno manji od brzine kojom procesor može procesirati podatke (u prijevodu: brža obrada ne pomore, kad svakako bus ne more brzo slat podatke)
- RAM i procesni registri nisu jednako brzi => uzrokuje se latencija i processor downtime => procesor ne dela niš dok čeka podatke iz memorije => VON NEUMANN BOTTLENECK
- Troši se jako puno energije => čak i više energije za sam prijenos podataka nego za obradu istih => čisti overhead
- npr. u operaciji zbrajanja 2 broja više energije se troši za dovlačenje i čitanje brojeve iz memorije nego za samo zbrajanje

- Neuralne mreže temeljene na Von Neumann arhitekturi

- namijenjene za riješavanje kognitivnih problema na računalu
- utemeljene na perceptronu i metodi backpropagacije
- Perceptron => pojednostavljeni matematički model neronske mreže u kojem neuroni računaju weighted zbroj input signala i generiraju output signal koristeći aktivacijsku funkciju
- Proces treniranja svodi se na prilagdobe weightova s ciljem smanjenja errora

- Pošto večina modernih neuronskih mreža ima layered arhitekturu, najviše računalno zahrjevana operacija je svakako množenje matrica vektorima (y = Wx)
- Da bi se taj proces odradio, potrebno je najprije dohvatiti podatke iz memorije (m*n weightova za W i n vrijednsoti vektora x) => vrijednosti m*n weigthova koriste se jednom po množenju, dok se vrijendosti vektora x koriste ponovno

- Da bi računao, procesor treba primiti weightove i input podatke iz memorije
- Propusnost (throughtput) data busa i latencija u primanju podataka ograničavaju brzinu dobivanja weightova
- broj weightova raste u O(n^2) di je n veličina inputa
- Throughtput se izrazito jako troši za množenje matrica vektorom

- Kako ublažiti navedena ograničenja?

- CPU => korištenje kompleksnog multi-level cache sistema
- U modernim procesorima, cache zna činiti i do 40% površine čipa
- deseci megabajta ultra-brze memorije
- često, neuronske mreže ne dozvoljavaju pohranu svih weightova u cache
- Ne trebaju nam neka super kompleksna rješenja jer u množenju matrica unaprijed znamo redoslijed operacija
- CPU je u ANN-ovima zadovoljavajuć samo za male neuronske mreže, ali ne i za moderne velike arhitekture od više stotina MB

- GPU => više strategija za riješavanje memorijske latencije
- svakom streaming multiprocesoru daje se veliki file registar koji sprema execution context za puno threadova i omogućava brzi switch između njih (za svaki thread se zna ča točno dela)
- koristi se computation scheduler koji upotrebljava upravo taj feature s više threadova
Visoka latencija instrukcija

Neke instrukcije, poput pristupa podacima iz glavne memorije, imaju značajno vrijeme čekanja (latenciju).

Tijekom tog čekanja, procesor ne može odmah nastaviti s izvršavanjem te instrukcije.

Prebacivanje između threadova (warp switching)

Kada GPU detektira da trenutni thread (npr. SIMD thread 1) čeka na podatke, scheduler automatski prebacuje izvršavanje na drugi thread (SIMD thread 2).

Ako i taj thread naiđe na latenciju, GPU može nastaviti s trećim threadom (SIMD thread 3), i tako redom.

Ovo prebacivanje je vrlo brzo i odvija se bez značajnog overheada.

Sakrivanje latencije (latency hiding)

Dok jedan thread čeka podatke iz memorije, drugi threadovi koriste računalne resurse (ALU, FPU itd.).

Na taj način, ukupna iskoristivost GPU-a ostaje visoka, iako su pojedini threadovi privremeno blokirani.

Velik broj paralelnih threadova

GPU arhitektura podržava istovremeno izvođenje velikog broja threadova (često tisuće).

Ti threadovi su grupirani u streaming multiprocesore (SM) – svaka jedinica SM sadrži vlastiti scheduler i skup jezgra.

Brojni SM-ovi zajedno omogućuju kontinuirano izvođenje i ravnomjernu raspodjelu opterećenja.

Efekt

Zahvaljujući ovom mehanizmu, latencija memorije se "skriva" jer se u međuvremenu obavlja koristan rad na drugim threadovima.

Time GPU postiže visoku propusnost i efikasnost u paralelnom procesiranju podataka.

Uz samu latenciju, ključan je i memory throughtput => makismalna količina podataka koja se može primiti iz memorije u određenoj vremenskoj jedinici 

TPU => smanjuje efekte latencije i low memory throughtputa koristeći systoličke matrice i software controlled memoriju umjesto cache-a.

Ideja systolic računanja je kreiranje velike matrice (256x256 za TPUv1) računalnih jedinica

Svaka jedinica pohranjuje weightove i odrađuje 2 operacije. PRvo množi broj x koji je došao iz jedinice lijevo. Zatim šalje broj x primljen od jedinice gore, jedinici dole i prosljeđuje primljenu sumu na desno
Weigthovi su pohranjeni u računalnim jedinicama, a ne u memoriji => EFIKASNO :D

TPU štedi energiju jer ima mnogo ALU jedinica koje mogu ponovno koristiti ulazne vrijednosti bez stalnog pristupa registrima, za razliku od CPU-a i GPU-a koji to stalno rade.

Neuromorphic approach

CPU, GPU i TPU su supercool, ali ni blizu legit biološkim conterpartovima.
Posebno u: potrošnji energije, fleksibilnosti (mogućnost da riješavaju različite zadatke), adaptibilnosti i skalabilnosti
Implementacija ključnih funkcionalnosti i principa mozga mogle bi riješiti taj gap

Mozak je tehnički gledano, veliki fundamentalno drukčiji, non von Neumann kompjuter
- Za razliku od everyday kompova, u mozgu:
- neuroni šalju informacije koristeći diskretne impulse (spikeove)
- svi eventi se događaju asinkrono (nema 1 centralnog procesa koji eksplicitno orkestrira rad svih neurona)
- Learning procesi su lokalni
- Network topologije su neslojevite
- Nema zajedničke memorije s kojom bi univerzalni procesori radili
- Umjesto toga, postoji ogroman broj jednostavnih agenata koji funkcioniraju samoorganizacijski

Neuromorfni pristupi u računalnim sustavima
- Danas se mnogi akceleratori neuronskih mreža nazivaju **neuromorfnim AI sustavima** kako bi privukli pažnju.
- Kako bi se **smanjila nejasnoća u klasifikaciji** AI sustava kao neuromorfnih, autori predlažu **popis svojstava** koja su korisna pri izradi računalnih sustava.
- Ta svojstva su se **pokazala učinkovitima u stvarnim projektima**.

- Neural network-based approach: sposobnost učenja (ne treba postavljati parametre eksplicitno) => povezivanje velikog broje relativno jednostavnih elemenata u network => zajednički obavljaju složene zadatke
- Paralelizam: paralelni rad neurona i simultana provedba više zadataka
- Asinkronost: nema posebnog procesa koji sinkronizira ostale
- Impulsna priroda transmisije informacija: minimalni overhead za transimisiju i procesiranje signala na primateljskom neuronu => resistance to noise
- Local learning: manji overhead za transfer podataka tijekom učenja; mogućnost kreiranja neograničeno velikih sustava; kontinuirano inkrementalno učenje
- Sparse data streamovi=> podaci stižu rijetko, ali smisleno
- GPT SAID:
Znači da se podaci generiraju samo kada se dogodi neki događaj (event), umjesto kontinuiranog slanja ogromne količine informacija (kao u klasičnim kamerama ili senzorima).

Takav event-driven signal processing omogućuje da se obrada i prijenos podataka odvijaju samo kad je to potrebno, čime se:

smanjuje overhead (opterećenje) kod prijenosa i obrade,

štedi energija,

i povećava učinkovitost cijelog sustava.
- Analog computing: efikasna implementacija hardvera
- in-memory computing: nema overheada za transfer privremenih međupodataka; nema kompetitivnog pristupa memoriji

- PARALELIZAM:
- svaki biološki neuron je neovisno računalo, ali puno sporiji nego silicijski procesori
- U mozgu ima i više od 87 milijardi neurona
- Potrebno je puno paralelnog rada da bi svi oni mogli raditi

- ASINRKONOST:
- paralelizam sam po sebi ne daje uvjek dovoljan efekt jer je ipak potrebna sinkronizacija između nodeva
- Po Amdahlovom zakonu, sinkronizacijski owerhead raste nelinearno kako se povećava broj kompjutera i tako limitira dobrobiti paralelizma
- Čini se da mozak nema mehanizam koji eksplicitno sinkronizira rad svih neurona
- biološki neuroni rade asinkrono i omogućavaju da se nadiđu ograničenja Amadhlovog zakona

- IMPULSNA PRIRODA TRANSMISIJE INFORMACIJA
---

### **Ključne ideje o Spiking Neural Networks (SNN):**

* **Način prijenosa informacija:**

  * U mozgu se informacije prenose u obliku impulsa (spikeova) — kratkih, naglih promjena potencijala.
  * SNN modelira upravo tu prirodu — neuroni međusobno razmjenjuju *spikeove* koji sadrže **samo informaciju o vremenu nastanka**.

* **Vremenska komponenta:**

  * Prijenos spikea nije trenutan — svaka sinapsa ima **težinu (w)** i **vremensko kašnjenje (d)**.
  * **Vrijeme spikea i kašnjenje** služe za **eksplicitno uvođenje vremena** u model obrade informacija.

---

### **Prednosti SNN-a nad klasičnim neuronskim mrežama:**

* **Asinkroni prijenos podataka:**
  Omogućuju prijenos informacija između neurona *bez potrebe za globalnim sinkronizacijama*.

* **Rad s dinamičkim podacima:**
  Zahvaljujući vremenskoj komponenti, SNN može obrađivati **signale koji se mijenjaju u vremenu**, jer informacija ovisi o **vremenu generiranja spikea** i **kašnjenju propagacije**.

* **Nelinearna dinamika:**
  SNN su **kompleksni nelinearni dinamički sustavi**, što omogućuje bogatiju i realističniju obradu informacija.

* **Energetska učinkovitost:**
  Neuroni troše energiju samo kada reagiraju na dolazni spike, a zatim prelaze u **neaktivno stanje**.
  U svakom trenutku samo **mali broj neurona radi**, što dramatično **smanjuje potrošnju energije**.

---

### **Ograničenja danas:**

* Malo praktičnih primjena zbog **ograničenja hardvera** i **težine treniranja**.
* Klasične mreže još uvijek **postižu bolje rezultate** u većini zadataka.
* Trening algoritmi i topologije SNN-a su još uvijek **otvoreni istraživački problemi**.

---

