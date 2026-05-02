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

- `Seminar_I_2026.ipynb` — finalni notebook za predaju (preimenuje se u `SEM1_TIM##.ipynb` prije submita)
- `pyproject.toml` / `uv.lock` — Python ovisnosti (jupyter, pandas, matplotlib, numpy)
- `PREDLOŽAK SEMINARSKOG RADA.docx` — službeni Word predložak (referenca)

## Pokretanje

Ako nemate `uv` instaliran: `brew install uv` (macOS) ili pratite https://docs.astral.sh/uv/

```bash
uv sync                                           # instaliraj ovisnosti
uv run jupyter lab Seminar_I_2026.ipynb           # ili 'jupyter notebook'
```

Notebook automatski generira sintetski `data.csv` (1 000 000 zapisa) pri prvom pokretanju.
**Cijelo izvršenje notebooka traje ~20–25 min** zbog insertion sorta nad 100k zapisa
(što je upravo ono što spec traži da se vidi N² ponašanje).

## Podatkovni skup

Notebook po defaultu radi nad **vlastitim sintetskim skupom** od 1 000 000 zapisa s hrvatskim
imenima/prezimenima/gradovima (DZS izvori) — to je naš **bonus +3** prijedlog.

Dodijeljeni skup `podatkovni_skup_Bukovina.csv` **nije** u repou (gitignored). `load_dataset()`
ga može učitati bez izmjena (notebook autodetektira sa/bez headera, dd.mm.yyyy/ISO format).
Ako želite testirati nad bukvinom, stavite file u root foldera i u ćeliji 8 promijenite
`csv_path = 'podatkovni_skup_Bukovina.csv'`.

## Bodovi

- Implementacija a)–i) za 3 indeksna ključa (prezime+ime, datum_rođenja, mjesto_stanovanja)
- **+3** crveno-crno stablo (prolazi kroz pun b)–h))
- **+3** vlastiti sintetski podatkovni skup (potrebno odobrenje profesora — Matej u mailu)

## Podjela rada

| Član | Zadaci |
|---|---|
| Matej Fajt (voditelj) | Generator data.csv, a) učitavanje, b) izgradnja, c) min/max |
| Tin Bukovina | d) brojači rotacija, e) ispis razina, **crveno-crno stablo (bonus)** |
| Patrik Ostrunić | f) prefiks pretraga, g) range pretraga |
| Filip Kušer | h) sortiranja, i) ponavljanje za datum + mjesto, integracija notebooka |

(Možete preraspodijeliti — ažurirajte tablicu u headeru notebooka prije predaje.)
