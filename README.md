# NTAS — 1. seminarski rad 2026

**Kolegij:** Napredna teorija algoritama i sustava (FERIT, 2025./2026.)
**Rok predaje:** 7. svibnja 2026. u 23:59 (LMS)

## Tim

| # | Član | Uloga |
|---|---|---|
| 1 | Matej Fajt | voditelj tima |
| 2 | Tin Bukovina | član |
| 3 | Patrik Ostrunić | član |
| 4 | Filip Kušer | član |

## Sadržaj

- `Seminar_I_2026.ipynb` — završni notebook za predaju (prema potrebi preimenovati u `SEM1_TIM02.ipynb`)
- `pyproject.toml` / `uv.lock` — Python ovisnosti (jupyter, pandas, matplotlib, numpy)
- `PREDLOŽAK SEMINARSKOG RADA.docx` — službeni Word predložak (referenca)

## Pokretanje

Instalacija alata `uv`: https://docs.astral.sh/uv/

```bash
uv sync                                           # instaliraj ovisnosti
uv run jupyter lab Seminar_I_2026.ipynb           # ili 'jupyter notebook'
```

Notebook automatski generira sintetski `data.csv` (1 000 000 zapisa) pri pokretanju.
**Cijelo izvršenje notebooka traje ~20–25 min** zbog algoritma insertion sort nad 100 000 zapisa
(što prikazuje očekivani N² rast).

## Podatkovni skup

Notebook radi nad **vlastitim sintetskim skupom** od 1 000 000 zapisa s hrvatskim
imenima/prezimenima/gradovima iz DZS izvora.

Dodijeljeni skup `podatkovni_skup_Bukovina.csv` **nije verzioniran u repozitoriju**. `load_dataset()`
ga može učitati bez izmjena; automatski prepoznaje sa/bez headera i dd.mm.yyyy/ISO format datuma.
Za pokretanje nad dodijeljenim skupom dovoljno je postaviti
`csv_path = 'podatkovni_skup_Bukovina.csv'`.

## Dodatni dijelovi

- Implementacija a)–i) za 3 indeksna ključa (prezime+ime, datum_rođenja, mjesto_stanovanja)
- Crveno-crno stablo provedeno kroz postupke b)–h)
- Vlastiti sintetski podatkovni skup istog reda veličine kao dodijeljeni skup

## Podjela rada

| Član | Zadaci |
|---|---|
| Matej Fajt (voditelj) | Generator data.csv, a) učitavanje, b) izgradnja, c) min/max |
| Tin Bukovina | d) brojači rotacija, e) ispis razina, crveno-crno stablo |
| Patrik Ostrunić | f) prefiks pretraga, g) range pretraga |
| Filip Kušer | h) sortiranja, i) ponavljanje za datum + mjesto, integracija notebooka |
