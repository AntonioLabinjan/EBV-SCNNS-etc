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

 
