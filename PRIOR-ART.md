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
