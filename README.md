# The Review-Gate Method ｜ 评分闸门法

*[中文版 ｜ Chinese version](README.zh.md)*

Building restaurant shortlists from **verifiable review data** instead of relaying blog roundups —
plus one fully worked case (Brisbane, 300+ venues).

---

## The idea

Most restaurant lists relay whatever the internet recommends. This inverts it:
**state a hard gate first, and only what survives goes in.**

**Main gate: Google ≥ 4.7 AND ≥ 200 reviews**

You find out quickly that **one gate is not enough**. Coffee shops sit at 4.8 up and down the
street. Licensed clubs score 4.2 because the rating covers the whole venue, gaming room included.
Restaurants serving a migrant community have structurally fewer English reviews whatever the food
is like.

So the method became: **one stated gate per category, with the reason it was loosened or tightened
written into the output.**

**→ Full method: [`METHOD.md`](METHOD.md)** — the gate table, eight lessons learned the hard way,
four reusable techniques.

---

## Two hard rules

1. **Platforms are recorded separately, never averaged.** A number without a platform label is a
   bug, not shorthand.
2. **Anything not found is written as "not found", with the reason.** Never estimated.

---

## The worked case: Brisbane

- 🌐 **[Web ｜ 网页版](https://cgwlovely.github.io/review-gated-dining/)**
- 📄 **[PDF — 45 pages, 389 clickable links](docs/pdf/Brisbane_2026_餐厅指南.pdf)**
- 🔬 **[Full research record ｜ 完整调查记录](research/brisbane-dining.md)** — 19 sections, including
  rejected candidates and unfinished work

The page shows roughly **300 display rows**; one venue can appear in several sections (price band,
cuisine, occasion), so **display rows ≠ unique venues**. The structured dataset reports both —
see [`build/summary.md`](build/summary.md) and the [data browser](https://cgwlovely.github.io/review-gated-dining/data.html).

Tiered as: 25 through the main gate · a five-band price ladder of 50 ·
pan-Asian dining indexed by mall floor and by cuisine · a dozen cuisines · steak · coffee ·
bubble tea · seafood markets · craft breweries · farmers markets · club member pricing ·
pub weekday specials.

**Every venue links to Google Maps. Every price carries its source label** (official site /
crowd-reported band / review photo / third-party / not found).

> The case-study page is written in Chinese — venue names, addresses and prices are in English
> throughout, and the section headings are bilingual. The method documents are fully bilingual.

### The findings that generalise

- **The language of your candidate pool decides your result.** English listicles produced the
  conclusion that one suburb's Chinese restaurants "almost all fail the gate"; searching in Chinese
  by regional cuisine surfaced a set of 4.6–4.9 venues in the same streets.
- **Third-party set-menu prices are systematically stale** — every one that could be checked
  against the venue's own site was too low.
- **Big sample ≠ high score.** One of Australia's best-known croissant bakeries fails the gate at
  both local branches.
- **Use the official licence register as the denominator.** Council open data shows **8,046
  licensed records, 7,020 consumer-facing venues** city-wide; this list covers about 2% — because
  the main gate is deliberately a narrow sieve.
- **Random sampling shows how narrow your pool really is**: 13 sampled venues yielded 2 that
  cleared the main gate and were missing from the list.

---

## Reproducible build ｜ 可复现构建

The venue data is no longer embedded in prose. It lives in [`data/`](data/) and everything else is
generated from it.

```bash
make check    # validate only — non-zero exit on any error
make build    # data -> gate evaluation -> build/ and docs/data/
make test     # prove the validators catch injected faults (21 cases)
```

| File | What it is |
|---|---|
| `data/venues.csv` | one row per venue: rating + platform + observation date, price + unit + source type + date, lat/lon, gate, status |
| `data/gates.yml` | **every gate threshold and its rationale.** `gate_pass` is computed from this file and is never hand-entered |
| `data/sources.csv` | source URL, kind, licence, access date |
| `data/venue_aliases.csv` | licence-holder name / trading name / branch aliases — this is what makes register-to-Google matching possible |

The build derives three audit signals alongside the hard gate, as
[issue #1](https://github.com/cgwlovely/review-gated-dining/issues/1) asked:

- **`shrunk_rating`** — Bayesian shrinkage toward the city mean, so a 4.9 from 34 reviews cannot
  outrank a 4.8 from 9,015. The main table is ordered by this.
- **`wilson_lower`** + **`borderline`** — the 95% lower bound. **18 of the 25 gate-passers are
  flagged borderline**, because with the gate at 4.7 and Google rounding to one decimal a venue
  rated exactly 4.7 can never have a lower bound above 4.7. The hard gate stays the reader-facing
  rule because it is explicable; this flag exists so the ambiguity is visible rather than hidden.
- **`freshness`** — `0.5 ** (age_days / 180)`, so old and new observations are never weighted alike.

**Price units are not mixed.** `price_unit` is one of `per_person_set`, `per_person_reported`,
`item`, `for_two`, `set_menu`, `whole_dish`. A normalised **two-person food total** is derived only
where it can be derived honestly — à la carte venues are left blank rather than given an invented
range.

**Browse or download:** [data browser](https://cgwlovely.github.io/review-gated-dining/data.html)
(filter by suburb, cuisine, gate, budget, confidence, verification age) ·
[CSV](https://cgwlovely.github.io/review-gated-dining/data/venues.csv) ·
[JSON](https://cgwlovely.github.io/review-gated-dining/data/venues.json)

Every generated artefact carries its **snapshot date and commit SHA**.

---

## Layout

```text
METHOD.md       the method — gate table, eight lessons, four techniques
METHOD.zh.md    中文版
README.md       this file
README.zh.md    中文版
docs/           published site (GitHub Pages): index.html + PDF + 5 OSM maps
research/       full working record + complete council licence register (8,046 records)
data/            venues.csv · gates.yml · sources.csv · venue_aliases.csv
build/           generated: venues.json/csv · main-table.md · summary.md
scripts/         build.py (data -> gates -> outputs) · tests/ · OSM map renderer
Makefile         make check | build | test | maps
```

---

## Data boundaries

Read this before using any figure.

- **Everything expires.** Prices, hours and ratings change daily. Collection dates are recorded
  throughout; re-verify against the venue's own page before you travel.
- **Ratings are labelled by platform.** Live Google values and third-party mirrors can differ
  enough to cross a tier — a 4.6-on-mirror / 4.5-live case actually occurred.
- **"Not found" means the search genuinely failed.** It is never a placeholder for a guess.
- **This selects "worth a special trip", not "everything"** — about 300 venues out of 7,020.
- **Residual bias remains** against venues with thin English-language review ecosystems; Chinese
  platforms (Dianping, Xiaohongshu) could not be retrieved — they gate on CAPTCHA, and this
  project does not solve CAPTCHAs.

---

## Sources

- [Brisbane City Council · Food Safety Permits (Eat Safe)](https://data.brisbane.qld.gov.au/explore/dataset/food-safety-permits/) — CC-BY, 8,046 records, full export archived in `research/`
- Google Maps venue entries (rating, review count, crowd-reported price band, menu photos)
- [Australian Good Food Guide Chef Hat Awards](https://www.agfg.com.au/awards/brisbane) · [Gourmet Traveller Restaurant Guide](https://www.gourmettraveller.com.au/dining-out/restaurant-guide/best-restaurants-queensland-20148/)
- Venues' own websites and official ordering pages
- Map tiles © OpenStreetMap contributors

---

## Licence

Method, code and prose: [MIT](LICENSE).
Council data keeps its CC-BY licence; map tiles keep OpenStreetMap's ODbL.
