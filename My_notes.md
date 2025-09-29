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
