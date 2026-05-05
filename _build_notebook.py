#!/usr/bin/env python3
"""
Skripta za reproducibilnu izgradnju notebooka `Seminar_I_2026.ipynb`
iz tekstualnih predložaka i komponenti u `_components.py`.
"""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path

ROOT = Path("/Users/filipkuser/Developer/Programs/Faculty/Active/ntas-seminar")
NB_PATH = ROOT / "Seminar_I_2026.ipynb"
COMPONENTS = ROOT / "_components.py"


# ----------------------------------------------------------------------------
# Parsiranje _components.py u sekcije po "# =====" banner-ima.
# ----------------------------------------------------------------------------


def parse_sections(src_path: Path) -> dict[str, str]:
    """Vraća dict {title_normalized: code_block} po sekcijama _components.py.

    Sekcija počinje s tri linije:
        # ============================================================================
        # Naslov (može biti više linija)
        # ============================================================================
    i traje do sljedeće takve trojke ili kraja datoteke.
    """
    text = src_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    sections: dict[str, str] = {}

    banner_re = re.compile(r"^# =+$")
    i = 0
    current_title = None
    current_buf: list[str] = []
    while i < len(lines):
        if banner_re.match(lines[i]):
            j = i + 1
            title_parts: list[str] = []
            while j < len(lines) and not banner_re.match(lines[j]) and lines[j].startswith("# "):
                title_parts.append(lines[j][2:].rstrip())
                j += 1
            if j < len(lines) and banner_re.match(lines[j]) and title_parts:
                if current_title is not None:
                    sections[current_title] = "\n".join(current_buf).strip("\n") + "\n"
                current_title = " ".join(p.strip() for p in title_parts)
                current_buf = []
                i = j + 1
                continue
        if current_title is not None:
            current_buf.append(lines[i])
        i += 1

    if current_title is not None:
        sections[current_title] = "\n".join(current_buf).strip("\n") + "\n"

    return sections


# ----------------------------------------------------------------------------
# Konstrukcija ćelija
# ----------------------------------------------------------------------------


def md_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": uuid.uuid4().hex[:12],
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "id": uuid.uuid4().hex[:12],
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


# ----------------------------------------------------------------------------
# Sadržaj narrative ćelija (zamjene u zaglavlju notebooka)
# ----------------------------------------------------------------------------


HEADER_MD = """# PRVI SEMINARSKI RAD 2026

#### KOLEGIJ: Napredna teorija algoritama i sustava

#### Datum predaje rada: 7. svibnja 2026.

#### Broj tima: TIM_02

#### Ime i prezime članova tima

| # | Član | Uloga | Obrađeni dijelovi zadatka |
|---|---|---|---|
| 1 | **Matej Fajt** | voditelj tima | generator sintetskog skupa, a) učitavanje, b) izgradnja, c) min/max |
| 2 | Tin Bukovina | član | d) brojači rotacija, e) ispis po razinama, implementacija crveno-crnog stabla |
| 3 | Patrik Ostrunić | član | f) prefiks pretraga, g) range pretraga |
| 4 | Filip Kušer | član | h) sortiranja, i) primjena na datum rođenja i mjesto stanovanja, integracija notebooka |
"""


OPIS_IMPLEMENTACIJE_MD = """U seminaru je implementirano AVL balansirano binarno stablo za indeksiranje
zapisa o osobama (`ime`, `prezime`, `spol`, `datum_rođenja`, `mjesto_stanovanja`)
iz CSV datoteke koja sadrži **1 000 000 sintetskih zapisa s hrvatskim
imenima/prezimenima/gradovima** (atomski podaci preuzeti iz javnih izvora
DZS-a, kombinacije nasumične sa `random.seed(42)`).

**Napomena o podatkovnom skupu.** Kao dodatni dio rada koristi se
**vlastiti sintetski skup** umjesto dodijeljenog
`podatkovni_skup_Bukovina.csv` (1 000 000 zapisa). Sintetski skup
**strukturno i veličinski odgovara dodijeljenom skupu**:

- broj zapisa: 1 000 000 (isto)
- redoslijed stupaca: `ime, prezime, spol, datum_rođenja, mjesto_stanovanja`
- format datuma: `dd.mm.yyyy` (HR), kao u dodijeljenom
- bez header retka, kao u dodijeljenom

`load_dataset()` podržava sintetski skup i dodijeljeni
`podatkovni_skup_Bukovina.csv` iste sheme bez izmjena —
prepoznaje (ne)postojanje header retka i normalizira datum u ISO format
za korektno leksikografsko sortiranje.

Cijela implementacija nalazi se u ovom Jupyter notebooku, organizirano u
sljedeće logičke cjeline:

1. **Pomoćni razred `PersonRecord`** — `dataclass` s 5 polja koja
   odgovaraju shemi CSV-a.
2. **Indeksirani čvorovi (`IndexedNode` + tri varijante)** — nasljeđuju
   već zadani razred `BinaryNode` te nadjačavaju `compareTo` tako da uspoređuju
   ključ umjesto cijele vrijednosti. Tri varijante odgovaraju trima
   indeksnim ključevima:
   - `PrimaryKeyNode` — ključ `(prezime, ime)`
   - `DateKeyNode` — ključ `(datum_rodjenja, prezime, ime)`
   - `CityKeyNode` — ključ `(mjesto, prezime, ime)`
   Sekundarni dijelovi ključa služe kao tiebreaker da inorder traversal
   ostane deterministički.
3. **Obično (nebalansirano) BST** (`PlainBSTNode` mixin) — koristi isti
   `BinaryTree` infrastrukturu, ali nadjačava `add()` tako da preskoči
   AVL rotacije. Time se može direktno usporediti visine i vremena
   izgradnje s AVL-om, kako traži zadatak b).
4. **AVL s brojačima rotacija** (`make_counting_tree(...)`) — tvornička
   funkcija koja iz bilo koje `IndexedTree` podklase tvori varijantu
   koja prebrojava lijeve i desne rotacije pri umetanju (zadatak d).
   `LR` rotacija broji se kao 1 lijeva + 1 desna, `RL` analogno.
5. **Crveno-crno stablo** (`RBTree`, dodatni zadatak) — vlastita implementacija
   po CLRS varijanti, sa `NIL` sentinelom i postupkom popravljanja nakon
   inserta. Iste 3 ključne varijante (`RBPrimaryKeyTree`, `RBDateKeyTree`,
   `RBCityKeyTree`). Provedena je kroz cijeli set zadataka b)–h)
   paralelno s AVL-om.
6. **Sortiranja po prezimenu i imenu** — `insertion_sort`, `merge_sort`,
   `quick_sort` (s nasumičnim pivotom, iterativno radi izbjegavanja
   recursion limita), `tree_sort` (preko AVL-a). Svi su provjereni da
   daju **identičan rezultat na istom ulazu**.
7. **Generator sintetskog skupa** — koristi hardcodirane liste hrvatskih
   imena (M/Ž), prezimena i gradova preuzete iz DZS-a (Državni zavod za
   statistiku) te ih nasumično kombinira u zapise.
8. **Pomoćna funkcija `run_full_suite(...)`** — izvršava cijeli set
   zadataka b)–h) za zadani indeksni ključ. Poziva se 3× u notebooku:
   za primarni ključ (prezime+ime), za datum rođenja te za mjesto
   stanovanja (zadatak i, za 4-člani tim oba dodatna ključa).

**Analiza složenosti.** AVL i RB stablo imaju visinu *O(log N)*, pa su
operacije umetanja, pretrage i range-pretrage *O(log N)* po čvoru,
odnosno *O(log N + k)* za range-pretragu gdje je k broj rezultata.
Obično BST u prosječnom slučaju ima visinu *O(log N)* na slučajnim
ulazima ali bez garancije; u najgorem slučaju (sortirani ulaz) degradira
u *O(N)*. Sortiranja su *O(N²)* (insertion), *O(N log N)* (merge,
quick s nasumičnim pivotom u prosjeku, tree-sort).
"""


PRIKAZ_REZULTATA_MD = """Ispitno okruženje provedeno je nad sintetskim skupom od **1 000 000
zapisa** generiranih sa `random.seed(42)`. Za svaki od triju indeksnih
ključeva (`prezime+ime`, `datum_rodjenja`, `mjesto_stanovanja`) izvedeni
su sljedeći testovi. Rezultati su prikazani u izvršenim ćelijama za
pojedini indeksni ključ.

- **b)** Izgradnja običnog BST-a, AVL-a i RB stabla; ispis visina i
  mjerenje vremena izgradnje (preko `time.perf_counter()`).
  Provjera AVL svojstva preko `assertAVLProperty()` — uvijek vraća
  `True`.
- **c)** Ispis najmanje i najveće vrijednosti indeksa (leftmost i
  rightmost u stablu) zajedno s pripadnim cjelovitim zapisima.
- **d)** Brojači lijevih i desnih rotacija pri izgradnji AVL stabla.
  LR rotacija = 1L + 1R; RL = 1R + 1L.
- **e)** Ispis stabla po razinama, prvih 10 razina; svaka razina u
  zasebnom retku. Pri svakoj razini ograničeno je na prvih 8 čvorova
  radi čitljivosti, s ispisom ukupnog broja čvorova na razini.
- **f)** Prefiks pretraga indeksom (uključujući prazno ime — npr.
  `'Horvat'` ili `'Horv*'`); usporedba vremena obična BST vs AVL vs RB.
- **g)** Range pretraga (npr. `'D'` do `'I'`); usporedba istih triju
  struktura.
- **h)** Sortiranje na rastućim podskupovima
  (1k, 2k, 5k, 10k, 20k, 50k, 100k) algoritmima insertion / merge /
  quick / tree-sort (preko AVL-a) / tree-sort (preko RB stabla kao
  dodatne usporedbe).
  Sve veličine pokrenute su za sve algoritme — insertion sort na 100k
  traje nekoliko minuta, što je u skladu s kvadratnom složenošću.

Ispitni slučajevi su izabrani da pokažu i tipične upite (česta hrvatska
prezimena/imena/gradovi) i rubne (kratki prefiksi koji vraćaju mnogo
rezultata, te potpuno specificirani upiti).
"""


ZAKLJUCAK_MD = """Implementirana je AVL i crveno-crna varijanta balansiranog stabla,
te obična (nebalansirana) varijanta nad istim `BinaryTree` razredom.
Za ulaz od 1 000 000 sintetskih zapisa hrvatskih osoba dobivene su
sljedeće stvarne visine stabala i vremena izgradnje za svaki indeksni ključ:

- **Primarni ključ (prezime+ime)**: obični BST visina 134 i vrijeme
  10.863 s; AVL visina 23 i vrijeme 7.850 s; RB visina 25 i vrijeme
  4.955 s.
- **Datum rođenja**: obični BST visina 53 i vrijeme 11.052 s; AVL
  visina 23 i vrijeme 7.899 s; RB visina 24 i vrijeme 4.764 s.
- **Mjesto stanovanja**: obični BST visina 49 i vrijeme 9.971 s; AVL
  visina 23 i vrijeme 7.430 s; RB visina 23 i vrijeme 4.551 s.

AVL visina 23 za sva tri ključa vrlo je blizu teoretskoj donjoj granici
`⌈log₂(1 000 000)⌉ ≈ 20`; AVL svojstvo `|h(L) − h(R)| ≤ 1` provjereno je
preko `assertAVLProperty()` i u svim pokretanjima vraća `True`. RB visine
od 23 do 25 također su daleko ispod dopuštene gornje granice
`2·log₂(N+1)`. Obično BST stablo ima raspon visina 49–134, pri čemu je
najveća visina kod primarnog ključa jer popularna prezimena stvaraju mnogo
duplikata koji u nebalansiranoj varijanti idu u lijevo podstablo
(`compareTo ≥ 0` → lijevo) i tvore duže lance.

Vremena izgradnje sva su *O(N log N)*; na 1 000 000 zapisa mjerenja
u svim trima slučajevima favoriziraju RB stablo nad AVL-om. RB se gradi
za 4.551–4.955 s, dok AVL treba 7.430–7.899 s, jer RB ima manje strogo
održavanje visine i kraće postupke popravljanja nakon umetanja. Pretrage (prefiks i
range) traju ispod 1 ms u prikazanim mjerenjima na svim trima strukturama; razlika je
zanemariva u apsolutnim vrijednostima, ali bi pri patološki sortiranom
ulazu obična BST degradirala u *O(N)* po pretrazi, dok AVL/RB i tada
drže *O(log N)*.

Rezultati sortiranja odgovaraju očekivanoj složenosti pojedinih
algoritama. Insertion sort raste znatno brže od ostalih algoritama i za
100 000 zapisa traje nekoliko minuta, što je u skladu s kvadratnom
složenošću. Merge sort, quick sort i tree-sort ponašaju se znatno bolje
na većim ulazima. Za 100 000 zapisa quick sort se izvodi za
0.224–0.300 s, merge sort za 0.274–0.284 s, tree-sort preko AVL stabla
za 0.559–0.587 s, a tree-sort preko RB stabla za 0.281–0.294 s. RB
varijanta tree-sorta u prikazanim mjerenjima ostvaruje kraća vremena
izvođenja od AVL varijante, dok obje varijante sortiraju zapise
umetanjem u balansirano stablo i obilaskom stabla u rastućem redoslijedu.

Indeksi nad svim trima atributima (prezime+ime, datum rođenja, mjesto
stanovanja) pokazuju iste trendove, pa se može zaključiti da
je odabir indeksnog ključa stvar primjenske semantike, a ne
algoritamske složenosti.
"""


LITERATURA_MD = """[1] Adelson-Velsky, G. M.; Landis, E. M. (1962). *An algorithm for the
organization of information*. Proceedings of the USSR Academy of
Sciences. (originalni AVL rad)

[2] Bayer, R. (1972). *Symmetric binary B-Trees: Data structure and
maintenance algorithms*. Acta Informatica 1(4). (preteča crveno-crnog
stabla)

[3] Guibas, L.; Sedgewick, R. (1978). *A dichromatic framework for
balanced trees*. 19th Annual Symposium on Foundations of Computer
Science. (formalizacija RB stabla)

[4] Cormen, T. H.; Leiserson, C. E.; Rivest, R. L.; Stein, C. (2022).
*Introduction to Algorithms*, 4th edition. MIT Press. (poglavlja 12 — BST,
13 — RB stablo, 6–8 — sortiranja)

[5] Knuth, D. E. (1998). *The Art of Computer Programming, Vol. 3:
Sorting and Searching*, 2nd edition. Addison-Wesley.

[6] Goodrich, M. T.; Tamassia, R.; Goldwasser, M. H. (2013). *Data
Structures and Algorithms in Python*. Wiley.

[7] Skripta i predavanja kolegija "Napredna teorija algoritama i
sustava", FERIT, akademska godina 2025./2026.

[8] Državni zavod za statistiku Republike Hrvatske, *Popis stanovništva
2021.* — https://podaci.dzs.hr/ (izvor lista hrvatskih imena, prezimena
i naselja korištenih za sintetski skup).
"""


# ----------------------------------------------------------------------------
# Sadržaj novih ćelija (nakon početka sekcije "IMPLEMENTACIJA ISPITNOG KODA")
# ----------------------------------------------------------------------------


SETUP_MD = """## 0) Postavke izvršavanja

Postavke importa i parametara koji se koriste kroz cijeli notebook.
Notebook je razvijen i testiran pod Pythonom 3.13 u `uv`-managed
virtualnom okruženju (vidi `pyproject.toml`).
"""

SETUP_CODE = """import csv
import random
import sys
import time
from dataclasses import dataclass
from datetime import date, timedelta

import matplotlib.pyplot as plt

# Veće stablo i obični BST mogu uzrokovati duboke rekurzije pri obilasku.
sys.setrecursionlimit(200_000)

# Veličina sintetskog skupa — 1 000 000 zapisa, podudarno s dodijeljenim
# skupom 'podatkovni_skup_Bukovina.csv' radi zadovoljavanja uvjeta
# Veličina odgovara uvjetu za dodatni sintetski skup.
N_RECORDS = 1_000_000
RANDOM_SEED = 42

print(f"Python: {sys.version.split()[0]}")
print(f"Veličina skupa N = {N_RECORDS:,}, seed = {RANDOM_SEED}")
"""


def make_run_cell(label: str, plain_cls: str, avl_cls: str, count_cls: str, rb_cls: str,
                  key_fn: str, prefix_examples: list[str], range_examples: list[tuple[str, str]]) -> str:
    pe = ", ".join(repr(s) for s in prefix_examples)
    re_ = ", ".join(f"({lo!r}, {hi!r})" for lo, hi in range_examples)
    return f"""results_{label} = run_full_suite(
    key_label={label!r},
    records=records,
    plain_tree_cls={plain_cls},
    avl_tree_cls={avl_cls},
    counting_tree_cls={count_cls},
    rb_tree_cls={rb_cls},
    key_fn={key_fn},
    prefix_examples=[{pe}],
    range_examples=[{re_}],
    sort_sizes=[1000, 2000, 5000, 10000, 20000, 50000, 100000],
    # insertion_sort_max=None znači: izvršavamo insertion sort i na 50k i 100k
    # iako je kvadratno spor (procijenjeno 50k≈45s, 100k≈3min — u skladu sa specifikacijom).
    insertion_sort_max=None,
    plot=True,
)
"""


# ----------------------------------------------------------------------------
# Glavna funkcija — sastavlja notebook
# ----------------------------------------------------------------------------


def main() -> None:
    sections = parse_sections(COMPONENTS)
    print("Sekcije pronađene u _components.py:")
    for name in sections:
        print(f"  - {name[:80]}")

    code_cells_spec: list[tuple[str, str]] = [
        (
            "## 1) Razred zapisa i indeksirani čvorovi\n\n"
            "`PersonRecord` modelira jedan redak iz `data.csv`. `IndexedNode`\n"
            "nasljeđuje `BinaryNode` i nadjačava `compareTo` tako da uspoređuje\n"
            "**ključ** umjesto cijele vrijednosti. Tri varijante (`PrimaryKeyNode`,\n"
            "`DateKeyNode`, `CityKeyNode`) odgovaraju trima indeksnim ključevima\n"
            "(zadaci b–h za primarni ključ; zadatak i za datum i mjesto).\n",
            sections["PersonRecord + indeksirani čvorovi (3 ključne varijante)"],
        ),
        (
            "## 2) Obično (nebalansirano) BST\n\n"
            "Razred `_PlainAddMixin` nadjačava `add()` tako da preskoči AVL\n"
            "rotacije, čime od istog `BinaryNode` dobijemo običan BST insert.\n"
            "Koristi se preko `PlainPrimaryKeyTree` / `PlainDateKeyTree` /\n"
            "`PlainCityKeyTree`.\n",
            sections["Obično (nebalansirano) BST — preskače rotacije"],
        ),
        (
            "## 3) AVL s brojačima rotacija (zadatak d)\n\n"
            "Tvornička funkcija `make_counting_tree` od bilo koje\n"
            "`IndexedTree` podklase tvori varijantu koja broji lijeve i desne\n"
            "rotacije pri umetanju. **LR** se broji kao 1L + 1R, **RL** kao\n"
            "1R + 1L (svaka kompozitna rotacija sastoji se od jedne lijeve i\n"
            "jedne desne).\n",
            sections["AVL s brojačima rotacija (zadatak d)"],
        ),
        (
            "## 4) Crveno-crno stablo (dodatni zadatak)\n\n"
            "Klasična CLRS implementacija RB stabla s `NIL` sentinelom i\n"
            "postupkom popravljanja nakon umetanja. Tri ključne varijante prate\n"
            "AVL pandane (`RBPrimaryKeyTree` / `RBDateKeyTree` /\n"
            "`RBCityKeyTree`). RB stablo prolazi kroz cijeli set b)–h)\n"
            "paralelno s AVL-om.\n",
            sections["Crveno-crno stablo (dodatni zadatak)"],
        ),
        (
            "## 5) Sortiranja (zadatak h)\n\n"
            "Vlastite implementacije četiri algoritma. `quick_sort` koristi\n"
            "nasumičan pivot i iterativan stog (umjesto rekurzije) kako bi\n"
            "izbjegao Python recursion limit pri velikim ulazima.\n"
            "`tree_sort` koristi AVL stablo: ubaci sve, pa inorder prolaz.\n",
            sections["Sortiranja"],
        ),
        (
            "## 6) Generator sintetskog skupa hrvatskih osoba (dodatni zadatak)\n\n"
            "Unaprijed definirane liste hrvatskih **imena** (M i Ž), **prezimena** i\n"
            "**gradova** preuzete iz javnih izvora DZS-a (popis stanovništva\n"
            "2021.). Atomski podaci su stvarni; kombinacije\n"
            "(koje ime + prezime + grad + datum) su nasumične sa fiksnim\n"
            "seed-om radi reproducibilnosti.\n",
            sections["Generator sintetskog skupa hrvatskih osoba"],
        ),
        (
            "## 7) Pomoćna funkcija `run_full_suite` — izvršavanje zadataka b)–h)\n\n"
            "Pomoćna funkcija koja za zadani indeksni ključ izvrši cijeli\n"
            "set zadataka b)–h) (mjerenje izgradnje, ispis visina, min/max,\n"
            "rotacije, ispis razina, pretrage, sortiranja s grafom).\n"
            "Poziva se 3× u nastavku — jednom za svaki indeksni ključ.\n",
            sections["Pomoćna funkcija run_full_suite — izvodi cijeli set zadataka b)–h) za zadani indeksni ključ (poziva se 3x u notebooku: za prezime, datum, mjesto)."],
        ),
    ]

    new_cells: list[dict] = []
    new_cells.append(md_cell(SETUP_MD))
    new_cells.append(code_cell(SETUP_CODE))
    for md, code in code_cells_spec:
        new_cells.append(md_cell(md))
        new_cells.append(code_cell(code))

    new_cells.append(md_cell(
        "## 8) Generiranje sintetskog skupa i učitavanje (zadatak a)\n\n"
        "Generiramo `data.csv` (svaki put iznova radi reproducibilnosti).\n"
        "Učitavamo ga u listu `PersonRecord` zapisa koja se onda koristi\n"
        "kroz ostatak notebooka.\n"
    ))
    new_cells.append(code_cell(
        "csv_path = 'data.csv'\n"
        "\n"
        "# Uvijek regeneriraj radi reproducibilnosti rezultata.\n"
        "# Time postojeći data.csv ne utječe na sintetski skup za mjerenja.\n"
        "t0 = time.perf_counter()\n"
        "generate_dataset(N_RECORDS, seed=RANDOM_SEED, out_path=csv_path)\n"
        "print(f'Generirano {N_RECORDS:,} zapisa u {csv_path} '\n"
        "      f'({time.perf_counter()-t0:.2f} s, seed={RANDOM_SEED})')\n"
        "\n"
        "t0 = time.perf_counter()\n"
        "records = load_dataset(csv_path)\n"
        "print(f'Učitano {len(records):,} zapisa za {time.perf_counter()-t0:.2f} s')\n"
        "print(f'Primjer prvog zapisa: {records[0]}')\n"
        "\n"
        "# Napomena: load_dataset podržava nazive stupaca iz specifikacije\n"
        "# (datum_rođenja, mjesto_stanovanja) kao i ASCII varijante — pa ovaj\n"
        "# notebook radi i nad eventualno dodijeljenim CSV-om iste\n"
        "# sheme.\n"
    ))

    new_cells.append(md_cell(
        "## 9) Pokretanje za primarni ključ (prezime + ime)\n\n"
        "Sve točke b)–h) zadatka za prvi indeksni ključ.\n"
    ))
    new_cells.append(code_cell(make_run_cell(
        label="primarni",
        plain_cls="PlainPrimaryKeyTree",
        avl_cls="PrimaryKeyTree",
        count_cls="CountingPrimaryKeyTree",
        rb_cls="RBPrimaryKeyTree",
        key_fn="key_primary",
        prefix_examples=["Horvat", "Horv*", "Mar*", "Iva*", "Žagar"],
        range_examples=[("D", "I"), ("Horv", "Ivo"), ("Mar", "Per")],
    )))

    new_cells.append(md_cell(
        "## 10) Zadatak i.1) Pokretanje za datum rođenja\n\n"
        "Ponavljanje zadataka b)–h) s `datum_rodjenja` kao indeksnim\n"
        "ključem. Prefiks `'1985*'` pronalazi sve rođene 1985. godine,\n"
        "`'2000-01*'` sve rođene u siječnju 2000. itd.\n"
    ))
    new_cells.append(code_cell(make_run_cell(
        label="datum",
        plain_cls="PlainDateKeyTree",
        avl_cls="DateKeyTree",
        count_cls="CountingDateKeyTree",
        rb_cls="RBDateKeyTree",
        key_fn="key_date",
        prefix_examples=["1985*", "2000-01*", "1970-06-15"],
        range_examples=[("1980", "1990"), ("1995-01", "1995-07"), ("2000", "2010")],
    )))

    new_cells.append(md_cell(
        "## 11) Zadatak i.2) Pokretanje za mjesto stanovanja\n\n"
        "Ponavljanje zadataka b)–h) s `mjesto_stanovanja` kao indeksnim\n"
        "ključem.\n"
    ))
    new_cells.append(code_cell(make_run_cell(
        label="mjesto",
        plain_cls="PlainCityKeyTree",
        avl_cls="CityKeyTree",
        count_cls="CountingCityKeyTree",
        rb_cls="RBCityKeyTree",
        key_fn="key_city",
        prefix_examples=["Z*", "Sp*", "Zagreb", "Ri*"],
        range_examples=[("A", "M"), ("R", "Z"), ("Pula", "Split")],
    )))

    nb = json.loads(NB_PATH.read_text(encoding="utf-8"))
    cells = nb["cells"]

    replacements = {
        "de048573": HEADER_MD,
        "852e6d1f": OPIS_IMPLEMENTACIJE_MD,
        "dfc54eec": PRIKAZ_REZULTATA_MD,
        "1c4ae5c2": ZAKLJUCAK_MD,
        "a790ddae": LITERATURA_MD,
    }
    for c in cells:
        if c.get("id") in replacements:
            c["source"] = replacements[c["id"]].splitlines(keepends=True)
            c["cell_type"] = "markdown"
            c.setdefault("metadata", {})

    keep_until_id = "9c251b06"
    keep_idx = None
    for idx, c in enumerate(cells):
        if c.get("id") == keep_until_id:
            keep_idx = idx
            break
    if keep_idx is None:
        raise RuntimeError(f"Ne nalazim ćeliju s id-om {keep_until_id}")

    cells[:] = cells[: keep_idx + 1] + new_cells

    nb["metadata"]["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb["metadata"]["language_info"] = {
        "name": "python",
        "version": "3.13",
    }

    NB_PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nNapisano {len(cells)} ćelija u {NB_PATH}")


if __name__ == "__main__":
    main()
