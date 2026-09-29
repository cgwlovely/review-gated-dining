# Build summary

- snapshot date: **2026-09-29**
- built from commit: `68aae2c` (HEAD at build time — a commit cannot contain its own SHA)
- **unique_venues: 25**  ·  **display_rows: 25**
- gates defined: 14
- through their gate: **25**

## Confidence

- high: 2
- medium: 8
- low: 15

## Price source

- official: 16
- menu_photo: 3
- none: 3
- google_reported: 3

## Borderline (hard gate passed, small-sample proxy not)

- **18 of 25** venues through the gate
- `conservative_rating_proxy` is a **heuristic small-sample penalty, not a confidence
  interval**: Google publishes a mean and a count, not the 1-5 vote distribution, so no
  strict interval can be computed from what we have.
- Read this count as: with the gate at 4.7 and ratings rounded to one decimal, most passers
  sit close enough to the line that a modest sample penalty pushes them under. It is a
  prompt to re-check, not a claim that they fail.
- The hard gate stays the reader-facing rule; `shrunk_rating` orders the main table.

  - The Fifty Six: 4.7/207 -> proxy 4.523 (gate 4.7)
  - Joy: 4.7/215 -> proxy 4.527 (gate 4.7)
  - Chocolate Elements: 4.7/241 -> proxy 4.539 (gate 4.7)
  - Unbearable Bagels: 4.7/333 -> proxy 4.566 (gate 4.7)
  - Naldham House: 4.7/432 -> proxy 4.585 (gate 4.7)
  - Ngon Brisbane: 4.7/648 -> proxy 4.608 (gate 4.7)
  - Montrachet: 4.7/890 -> proxy 4.623 (gate 4.7)
  - Smoked Paprika: 4.7/924 -> proxy 4.625 (gate 4.7)
  - Vegeme: 4.7/1,001 -> proxy 4.628 (gate 4.7)
  - Rothwell's Bar & Grill: 4.7/1,067 -> proxy 4.631 (gate 4.7)
  - Beccofino: 4.7/1,220 -> proxy 4.635 (gate 4.7)
  - hôntô: 4.7/1,603 -> proxy 4.644 (gate 4.7)
  - NAÏM: 4.7/1,849 -> proxy 4.648 (gate 4.7)
  - Hashtag Burgers and Waffles: 4.7/2,154 -> proxy 4.652 (gate 4.7)
  - 1889 Enoteca: 4.7/2,341 -> proxy 4.654 (gate 4.7)
  - Nekoland Ramen & Bar: 4.8/229 -> proxy 4.654 (gate 4.7)
  - Sono Japanese: 4.7/2,388 -> proxy 4.655 (gate 4.7)
  - Farm House: 4.7/2,981 -> proxy 4.66 (gate 4.7)

## Two-person totals

- derivable: 10
- à la carte (not derivable): 12
- no price recorded: 3

## Validation

- errors: **0**
- warnings: 2

  - ⚠ row 18 (bne-joy): review_count 215 is within 10% of the main threshold - a handful of reviews either way flips it
  - ⚠ row 19 (bne-the-fifty-six): review_count 207 is within 10% of the main threshold - a handful of reviews either way flips it
## Counts (issue #1: display rows are not unique venues)

- structured dataset — unique_venues: **25**, display_rows: 25, branch_count: 4
- published page — display_rows_page: **312**, distinct_on_page: **249**, repeated_venues: **33**

