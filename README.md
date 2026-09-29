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

Roughly **300 venues**, tiered: 25 through the main gate · a five-band price ladder of 50 ·
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

## Layout

```text
METHOD.md       the method — gate table, eight lessons, four techniques
METHOD.zh.md    中文版
README.md       this file
README.zh.md    中文版
docs/           published site (GitHub Pages): index.html + PDF + 5 OSM maps
research/       full working record + complete council licence register (8,046 records)
scripts/        OSM tile map renderer
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
