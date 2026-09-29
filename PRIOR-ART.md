# Prior art: who else publishes a dining list this way

*Surveyed 2026-09-29. Facts below were read off each site's own methodology page on that
date; nothing here is inferred from reputation. Where a site does not state something, this
says "not stated" rather than guessing.*

The question was narrow: **does anyone else publish both a stated numeric gate and the data
behind it?** The answer, as far as this survey found, is that the two halves exist separately.

## The comparison

| | Gate / formula published | Per-platform ratings kept apart | Raw data downloadable | Build reproducible | Says what it could not find |
|---|---|---|---|---|---|
| **This project** | Yes — 14 gates in [`data/gates.yml`](data/gates.yml), each with its rationale | Yes, **never averaged** | Yes — CSV + JSON + `datapackage.json` | Yes — `make build` | Yes, its own section |
| [Guidavera](https://guidavera.com/methodology) | **Yes, and in more detail than this project** — a 0–10 Consensus Score, 55% fixed block (Michelin 20%, Repsol 20%, World's 50 Best 10%, other accolades 5%) + 45% city block | Yes — inputs printed on each venue's page | No | Not stated | Not stated |
| [TastyPals](https://tastypals.com/methodology) | No — "directional editorial guidance, not a precise measurement" | Not stated | No | No | No |
| [Michelin](https://guide.michelin.com/) | Criteria named (products, technique, personality, harmony, consistency) but **not numeric** | n/a — single in-house judgement | No, and no public API | No | No |
| [The Good Food Guide](https://www.thegoodfoodguide.co.uk/) | Scoring bands published | n/a — in-house | No | No | No |
| NYC inspection projects on GitHub | n/a — no curation step | n/a | **Yes** (council open data) | Often yes | n/a |

## What this survey changed

**Guidavera is the closest neighbour, and it is ahead on one thing.** It publishes the actual
weights. This project publishes thresholds but has no combination formula at all — because it
deliberately refuses to combine platforms into one number. That refusal is a real choice with a
real cost, and it should be stated as such rather than presented as strictly better:

- *What it buys:* a reader always sees which platform said what, and a mirror lagging behind a
  live rating is visible instead of being blended away.
- *What it costs:* **there is no single ranking number**, so this guide cannot answer "what is
  the best restaurant in Brisbane" in one figure, and Guidavera can.

Two of Guidavera's stated rules were already independently present here — volume-weighted
ratings (Bayesian shrinkage) and professional awards recorded separately from diner ratings.
One is not, and is worth considering: **missing inputs redistributed proportionally rather than
penalising the venue.** This project's equivalent situation is a venue with only a Google
rating and no AGFG or Gourmet Traveller entry; today that venue is simply not eligible for
those categories, which is close to the same outcome, but the rule is nowhere written down.

## Brisbane specifically

*Checked 2026-09-29.* Nothing in Brisbane does what this project does, but the reason is worth
stating precisely: the city's food coverage splits into **editorial writing with no data** and
**council data with no curation**, and the one project that tried to sit between them is dead.

| Source | What it is | Criteria published | Per-venue numbers | Data download |
|---|---|---|---|---|
| **Sunnybank Food Directory** (`sunnybankfood.com.au`) | Billed itself as 布里斯本第一中文美食指南 — the Chinese-language guide to exactly the area this project found English listicles were missing | — | — | — |
| [Broadsheet Brisbane](https://www.broadsheet.com.au/brisbane/food-and-drink) | Editorial listicles | No | **None** — no ratings, no review counts | No |
| [The Weekend Edition](https://theweekendedition.com.au/brisbane/) | Editorial listicles | No | No | No |
| [Good Food](https://www.goodfood.com.au/brisbane) | Critic reviews, hatted-restaurant awards | Award bands published | Hat scores only | No |
| [AGFG](https://www.agfg.com.au/) | Chef-hat awards, used here as a second opinion | Award bands | Hat scores only | No |
| [Brisbane City Council open data](https://data.brisbane.qld.gov.au/) | 2,186 datasets | n/a | n/a | **Yes, CC-BY** |

**The Sunnybank Food Directory is gone.** The domain registration is still `ACTIVE` but it has
no DNS record at all — `sunnybankfood.com.au` returns NXDOMAIN, and both `http://` and
`https://` fail to connect. Only the Facebook page survives. This matters more than a dead link
usually would: it was a **Chinese-language** directory for the precinct this project's own
[Lesson 1](METHOD.md) is about, and its disappearance is part of why that precinct is
under-documented in a searchable, citable form.

### What the council actually publishes

Two food datasets are relevant, and only one of them is usable per venue:

- **`food-safety-permits` — 8,046 records, still live.** This is the denominator this project
  uses. Confirmed present on this date at the record count the guide cites.
- **`food-safety-complaints` — 10,573 records — checked and *rejected*.** It looks like a strong
  signal until you read the fields: `quarter`, `category_nature`, `category_type`,
  `location_suburb`. **There is no venue name and no address**, so it cannot be joined to a
  venue. It could only support suburb-level claims, which would taint every venue in a suburb
  for something one premises did. Not used, and recorded here so the next person does not spend
  the same hour on it.

### Where that leaves this project

Brisbane has a licence register with no opinion and several guides with opinions but no
register. Joining the two — a stated gate applied to an open denominator, with the result
downloadable — is the gap. That is a description of a gap, not a claim of quality: the guides
listed above are written by people who eat in the city professionally, and this project is a
shortlist of 25 structured venues out of 7,020 licensed premises.

## The gap this project sits in

Guides with a published methodology do not publish their data. Projects that publish data are
inspection dumps with no curation step. **No project was found that does both** — but "not
found" is what this is: a search on 2026-09-29 across restaurant-guide methodology pages and
the GitHub `food-data` / `restaurant-data` topics, not a proof that none exists.

Two honest caveats on the comparison above:

- **Scale.** Guidavera covers several cities. This project covers one, and only 25 of its
  venues are in the structured dataset; the rest of the guide is still hand-maintained.
- **The gate is narrow on purpose.** 25 venues out of 7,020 consumer-facing licensed premises
  is about 0.4%. That is a shortlist, not a survey, and it is not comparable to a guide that
  aims to cover a city.
