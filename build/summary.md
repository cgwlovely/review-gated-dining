# Build summary

- snapshot date: **2026-09-29**
- built from commit: `725c04a` (HEAD at build time — a commit cannot contain its own SHA)
- **unique_venues: 25**  ·  **display_rows: 25**
- gates defined: 14
- through their gate: **25**

## Confidence

- high: 2
- medium: 23

## Price source

- official: 16
- menu_photo: 3
- none: 3
- google_reported: 3

## Borderline (passes the hard gate, 95% lower bound does not)

- **18 of 25** venues through the gate
- Interpretation: with the gate at 4.7 and Google rounding to one decimal, a venue rated
  exactly 4.7 can never have a lower bound above 4.7. So most passers are **statistically
  indistinguishable from failing**. The hard gate stays the reader-facing rule because it is
  explicable; `shrunk_rating` is what the main table is ordered by.

  - The Fifty Six: 4.7/207 -> lower bound 4.523 (gate 4.7)
  - Joy: 4.7/215 -> lower bound 4.527 (gate 4.7)
  - Chocolate Elements: 4.7/241 -> lower bound 4.539 (gate 4.7)
  - Unbearable Bagels: 4.7/333 -> lower bound 4.566 (gate 4.7)
  - Naldham House: 4.7/432 -> lower bound 4.585 (gate 4.7)
  - Ngon Brisbane: 4.7/648 -> lower bound 4.608 (gate 4.7)
  - Montrachet: 4.7/890 -> lower bound 4.623 (gate 4.7)
  - Smoked Paprika: 4.7/924 -> lower bound 4.625 (gate 4.7)
  - Vegeme: 4.7/1,001 -> lower bound 4.628 (gate 4.7)
  - Rothwell's Bar & Grill: 4.7/1,067 -> lower bound 4.631 (gate 4.7)
  - Beccofino: 4.7/1,220 -> lower bound 4.635 (gate 4.7)
  - hôntô: 4.7/1,603 -> lower bound 4.644 (gate 4.7)
  - NAÏM: 4.7/1,849 -> lower bound 4.648 (gate 4.7)
  - Hashtag Burgers and Waffles: 4.7/2,154 -> lower bound 4.652 (gate 4.7)
  - 1889 Enoteca: 4.7/2,341 -> lower bound 4.654 (gate 4.7)
  - Nekoland Ramen & Bar: 4.8/229 -> lower bound 4.654 (gate 4.7)
  - Sono Japanese: 4.7/2,388 -> lower bound 4.655 (gate 4.7)
  - Farm House: 4.7/2,981 -> lower bound 4.66 (gate 4.7)

## Two-person totals

- derivable: 10
- à la carte (not derivable): 12
- no price recorded: 3

## Validation

- errors: **0**
- warnings: 2

  - ⚠ row 18 (bne-joy): review_count 215 is within 10% of the main threshold - a handful of reviews either way flips it
  - ⚠ row 19 (bne-the-fifty-six): review_count 207 is within 10% of the main threshold - a handful of reviews either way flips it
