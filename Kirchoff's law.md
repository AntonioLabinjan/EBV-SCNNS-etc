Kirchoff's law by chatgpt

# Zadatak (primjer)

Imamo dvostruki petljični krug (dva loopa koja dijele srednji otpornik):

* Lijevi izvor (V_1 = 10\ \text{V}) u lijevom krugu.
* Desni izvor (V_2 = 5\ \text{V}) u desnom krugu.
* Otpornici: (R_1 = 2\ \Omega) (lijevo), (R_2 = 3\ \Omega) (desno), (R_3 = 4\ \Omega) (zajednički između petlji).
* Smjer struja: pretpostavimo smjerove petlji kao (I_1) u lijevom krugu (sat. smjer) i (I_2) u desnom krugu (sat. smjer).

Cilj: naći (I_1) i (I_2), i struju kroz zajednički otpornik (R_3).

ASCII shema (pojednostavljeno):

```
     +---R1---+---R3---+---+
V1 --|        |        |   |-- V2 (drugi izvor u drugom krugu)
     +--------+--------+---+
         (lijevi)   (desni)
```

(Ovo je samo skica; važno su jednadžbe.)

---

# 1. Postavljanje jednadžbi — Kirchhoffova naponskog zakona (KVL)

Za svaki loop napišemo KVL (zbrajanje padova napona = suma izvora).

**Lijevi loop (loop 1):**
Padovi: (R_1 I_1) kroz (R_1) i pad na zajedničkom (R_3) koji ovisi o relativnom smjeru (nakon konvencije pad na (R_3) pri protoku (I_1) je (R_3(I_1 - I_2))). Izvor (V_1) je u suprotnom smjeru u jednadžbi pa:

[

* V_1 + R_1 I_1 + R_3 (I_1 - I_2) = 0
  ]

Središnje sređivanje:

[
(R_1 + R_3) I_1 - R_3 I_2 = V_1
]

**Desni loop (loop 2):**

[

* V_2 + R_2 I_2 + R_3 (I_2 - I_1) = 0
  ]

Središnje:

[

* R_3 I_1 + (R_2 + R_3) I_2 = V_2
  ]

---

# 2. Ubaci brojeve

Imamo (R_1=2), (R_2=3), (R_3=4), (V_1=10), (V_2=5).

Jednadžbe postaju:

(1) ( (2 + 4) I_1 - 4 I_2 = 10 )  → ( 6 I_1 - 4 I_2 = 10)

(2) ( -4 I_1 + (3 + 4) I_2 = 5 ) → ( -4 I_1 + 7 I_2 = 5)

To je linearni sustav dvije jednadžbe za dvije nepoznanice.

---

# 3. Rješenje sustava

Riješimo:

[
\begin{cases}
6 I_1 - 4 I_2 = 10[4pt]
-4 I_1 + 7 I_2 = 5
\end{cases}
]

Rješenje (računskom metodom, npr. Gauss ili algebraično) daje:

[
I_1 = \frac{45}{13}\ \text{A} \approx 3.4615\ \text{A}
]
[
I_2 = \frac{35}{13}\ \text{A} \approx 2.6923\ \text{A}
]

---

# 4. Struja kroz zajednički otpornik (R_3)

Struja kroz (R_3) (odnosno neto smjer lijevo→desno ako (I_1 - I_2 > 0)):

[
I_{R_3} = I_1 - I_2 = \frac{45-35}{13} = \frac{10}{13}\ \text{A} \approx 0.7692\ \text{A}
]

Dakle, kroz (R_3) struja ide iz lijevog kruga prema desnom (jer (I_1>I_2)).

---

# 5. Dodatne korisne veličine (opcionalno)

Napon na (R_3):
[
V_{R_3} = R_3 I_{R_3} = 4 \cdot \frac{10}{13} = \frac{40}{13}\ \text{V} \approx 3.0769\ \text{V}
]

Snaga disipirana na primjer na (R_1):
[
P_{R_1} = I_1^2 R_1 \approx (3.4615)^2 \cdot 2 \approx 23.95\ \text{W}
]

Isto možeš izračunati i za ostale otpornike.

---

# 6. Kratka interpretacija i savjeti

* Ključ: pravilo postavljanja jednadžbi — uvijek jasno definiraj smjer struja (pretpostavke), zatim dosljedno primijeni KVL (uz oznake polariteta padova i izvora). Ako rješenje daje negativnu struju, znači da stvarno teče suprotnim smjerom od pretpostavljenog.
* Kod mreža s više čvorova umjesto petlji često je praktičnije koristiti **Kirchhoffov čvorovski zakon (KCL)** i metode kao nodalna analiza. Za petlje je loop/KVL pristup često intuitivniji.
* Ako imaš više petlji, dobivaš veću matricu linearnih jednadžbi — rješavaj numerički (numpy / sympy) ili simbolički.

---

Ako želiš, mogu:

* poslati kratki Python snippet koji riješi sustav automatski i ispiše vrijednosti (ako voliš reproducibilnost),
* napraviti varijantu s drugim polaritetima izvora (da vidiš zamjenu znakova),
* pokazati isto rješenje koristeći **KCL / nodalnu analizu** da usporedimo rezultate.

