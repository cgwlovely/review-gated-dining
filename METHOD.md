# The Review-Gate Method

*[中文版 ｜ Chinese version](METHOD.zh.md)*

Building restaurant shortlists from **verifiable review data** instead of relaying blog roundups.

This file is the method itself. [`research/brisbane-dining.md`](research/brisbane-dining.md) is the
full working record; [`docs/`](docs/) is the finished output (web page and PDF).

---

## 1. The core idea: one gate is never enough

It starts with a single hard gate:

> **Main gate: Google ≥ 4.7 AND ≥ 200 reviews.**

That works inside one category — "proper restaurants". Apply it anywhere else and it breaks
immediately. Coffee shops sit at 4.8 up and down the street. Licensed clubs score 4.2 because the
rating covers the whole venue. Restaurants serving a migrant community have structurally fewer
English-language reviews, whatever the food is like.

**So the rule became: one stated gate per category, with the reason it was loosened or tightened
written into the output.**

| Category | Gate | Why this one |
|---|---|---|
| Restaurants (main gate) | ≥4.7 and ≥200 | The baseline |
| Budget tier | ≥4.5 and **≥1,000** | Rating bar drops 0.2; **sample bar rises 5×** as compensation. Better "lots of people said 4.5" than "a few said 4.8" |
| Coffee | ≥4.7 and ≥200 | **Not loosened.** Coffee ratings run high everywhere; the sample bar is what filters out "fifteen people gave it 5" |
| Bubble tea / drinks | **≥4.5** and ≥200 | Ratings are inflated as with coffee, but samples are far smaller, so the rating bar **drops to 4.5** while the sample bar stays at 200. Looser than coffee (4.7), tighter than the community-cuisine gate (4.3) |
| Community cuisines (Chinese, Vietnamese, East African…) | ≥4.3 and **≥150** | Customers are mostly from that community; **English reviews are structurally scarcer** |
| Other cuisines (Indian, Italian, French, Greek, Middle Eastern…) | ≥4.5 and ≥300 | Trading rating width for sample size |
| Licensed clubs, and ethnic community clubs | ≥4.0 and ≥500 | The score rates the **whole venue** — gaming room, function rooms, live music — not the bistro. Seven European communities keep their food in a club rather than a restaurant, so this row is not a niche |
| Steak | ≥4.2 and ≥500, **split into two tables** | Old steak pubs: 4.2–4.3, samples in the thousands, A$40–60. Fine-dining steakhouses: 4.4–4.8, A$80–200+. **The two groups cannot share a ranking** |
| Seafood retail | ≥4.2 and ≥150 | Buying raw fish is not eating out; sold by weight, so there is no "per person" |
| Pub weekly specials | **No rating gate at all** | This tier is about price, not score (see Lesson 6) |
| Community precinct venues (East African, Pacific Islander) | **No gate clears them** — published as *recorded, not recommended* | Ratings are 4.6–4.9; review counts are 25–284. Lowering the bar to fit them would let weak venues through everywhere else, so the category is published with its limit stated instead (see Lesson 9) |

**Two hard rules run through all of it:**

1. **Platforms are recorded separately, never averaged, never substituted.** A number without a
   platform label is a bug, not shorthand.
2. **Anything not found is written as "not found", with the reason it failed.** Never estimated,
   never filled in to complete a row.

---

## 2. Nine lessons, all learned the hard way

### 1. The language of your candidate pool decides your result

The first pass drew candidates from English "best restaurants in Brisbane" listicles and concluded
that **the Chinese restaurants in one suburb "almost all fail the gate"** — the evidence being a
well-known yum cha hall at 3.2.

**That conclusion was wrong.** Searching Google Maps directly **in Chinese, by regional cuisine**
(hotpot, Sichuan, Hunan, Lanzhou noodles, malatang, bubble tea) surfaced a whole set of
high-rated, high-sample venues in the same streets: 4.9/590, 4.8/802, 4.8/1,551, 4.8/1,186, 4.7/620.

The sharpest comparison is two yum cha restaurants on the same road:
**3.2/1,291 versus 4.7/2,296.**

> **The bias was not in the ratings. It was in the language used to build the candidate pool.
> For any multilingual food scene, search once in each community's own language.**

Repeating this for other communities — Korean, Japanese, Middle Eastern, East African, Pacific
Islander, Filipino, Latin American — found **five more precincts of the same shape**, each clustered
on one or two streets, none of them present in any English listicle. See lesson 9 for what happened
when the gate was applied to them.

### 2. The *type* of your candidate pool biases it too

A second pass found five more venues that cleared the same main gate and had simply never appeared:
a coffee bar at 4.8/1,120, a burger shop at 4.7/2,154, a vegetarian place at 4.7/1,001, a
Vietnamese diner at 4.7/648, a Japanese restaurant at 4.7/2,388.

The cause: every candidate came from "best restaurants / best places to eat" lists, and
**those lists structurally exclude burger shops, cafés, vegetarian diners and neighbourhood
noodle bars.**

> **Draw candidates from at least five kinds of list — fine dining, budget, coffee, single cuisine,
> single dish — before applying any gate.**

### 3. Chains must be checked branch by branch

The list carried one café at **4.5/3,313**. The same brand's other branch, in a different suburb,
is **4.7/1,514** — 0.2 higher.

> **A 0.2 gap between branches of one brand is common, and a listicle will only ever include one
> of them.**

### 4. Third-party set-menu prices are systematically stale

Every third-party price that could be checked against the venue's own site was **too low, without
exception**:

| Venue | Third-party listing | Actual (venue's own site) |
|---|---|---|
| Japanese restaurant | $84 pp | **$89 / $130, two tiers** |
| Fire-cooking restaurant | $100 pp | **$89 / $139** (different structure entirely) |
| Thai restaurant | $84 pp | **$89 / $130** |
| 10-seat tasting counter | $205 / $175 | **$220** |
| Degustation restaurant | $247 | **$255 weekday / $335 weekend** |

> **Only "official site" prices can be used for a budget. Treat every third-party price as a floor.**

### 5. Big sample ≠ high score

- One of Australia's most famous croissant bakeries: both local branches sit at **4.2/1,155 and
  4.3/614 — neither clears the gate.**
- The largest-sample Spanish restaurant in the city: **4.4/4,182 — does not clear.**
- Meanwhile the single largest sample in the whole project, **4.8/9,015**, belongs to a burger shop.

> **Sample size and rating are two separate dimensions. Read them separately.**

### 6. Rating and "deal strength" are often inversely correlated

The two pubs with the hardest weekly specials scored **lowest** (3.8/1,092 with a 200g rump at
A$19.90; 3.9/1,606 with a A$21 parmi), while the highest-rated pub in the same area — **4.6/2,900** —
**runs no weekly specials at all.**

> **If you want cheap, stop reading the score. If you want the experience, stop expecting a special.**

### 7. Mirrored ratings lag far enough to cross a tier

Third-party mirrors of Google ratings typically lag 1–2% on review count — but that is enough to
move a borderline venue: one café showed **4.6 on the mirror and 4.5 live**.

> **Any venue sitting on a 4.5 / 4.7 or 200 / 1,000 boundary must be re-checked against the live
> value before you rely on it.**

### 8. When you cannot get it, say you cannot get it

- **Dianping (Chinese review platform)** redirects to a slider CAPTCHA. **This project does not
  solve CAPTCHAs** — not retrieved.
- **TripAdvisor** returns a blank page to automated access — not retrieved.
- **"Open 24 hours" cannot be searched.** Opening hours are a *field*, not a keyword; text search
  cannot reach them.
- **Guessing cuisine from business names failed**: 52% were unclassifiable, and Chinese restaurants
  came out at 1.6% — obviously wrong, because they are named with proper nouns, not the word
  "Chinese".

> **The output must carry the empty cells. Never quietly pretend the question was not asked.**

---

### 9. A review-count gate is a blind spot for community-supported venues

Seven East African restaurants sit within 54 street numbers of each other on one road. Their Google
ratings are **4.6 to 4.9**. **Not one of them clears any gate in this project**, because their review
counts are 25, 39, 52, 80, 271 and 284.

The same held for an entire Pacific Islander precinct: four venues, 51–146 reviews, zero passes.

Nothing here says the food is worse. It says the venues are supported by a community that **eats
there without writing English reviews**. A minimum-review-count gate silently converts
"how much English-language review volume has accumulated" into "quality", and those two things come
apart hardest exactly where the food is least like everything else on the list.

There is a second way the same communities go missing, and it is not about counts at all.
Searching European cuisines surfaced **seven communities whose food lives in a member club, not a
restaurant** — German, Ukrainian, Polish, Czech, Danish, Serbian, Portuguese. A club is not
categorised as a restaurant, so cuisine searches reach it only by accident, and its rating covers
the whole venue rather than the kitchen. **Search by venue type as well as by cuisine**, and keep
club ratings in their own column.

> **State this limit rather than lowering the threshold.** Lowering it would let genuinely weak
> venues through everywhere else. The honest output is a separate section marked *recorded, not
> recommended* — and an admission that evaluating this category needs a method that does not depend
> on review accumulation at all. This project does not have one.

## 3. Seven reusable techniques

### 1. Use the official licence register as the denominator, and ratings as the quality signal

Councils usually publish a **register of licensed food premises**. Brisbane City Council's
[Food Safety Permits (Eat Safe)](https://data.brisbane.qld.gov.au/explore/dataset/food-safety-permits/)
is a complete, CC-BY list: **8,046 records, of which 7,020 are consumer-facing venues.**

- The **register** answers *how many exist, where, in what categories*.
- **Ratings** answer *which ones are worth going to*.
- **Neither substitutes for the other** — the register has no cuisine and no word-of-mouth; Google
  has no complete roll.

It also carries a **fourth, independent rating system**: food-safety stars. Only **282 venues
(6.8%) hold 5 stars**, and half are unrated — a *narrower* filter than Google 4.7, but one that
measures kitchen hygiene, not whether the food is good. **Stackable, not interchangeable.**

### 2. Read menus out of Google review photos

When a venue's own menu link dies (404 PDF, blank menu page), **the "Menu" album in Google Maps
holds photographs of the physical menu taken by customers**. Download at full resolution and read
the prices off it.

This recovered two venues in the case study: a A$134 Beef Wellington, and a complete bilingual yum
cha list with per-item prices.

**Limits: the photo may be an old menu (date unknown), and out-of-focus regions produce misreads.**
So these prices carry their own source label — more reliable than third-party, less than official.

### 3. Keep multiple review systems strictly apart

Beyond Google (long-run public scoring), the case study used two **professional-panel** systems:
a 20-point chef-hat guide, and an anonymous-reviewer restaurant guide.

**Only two venues in the entire city are named by all three.** Of the 25 venues clearing the main
gate, only 7 appear in the chef-hat list — and that guide's third-ranked restaurant appears
nowhere in the Google-gated tables.

> **This is not one of them being wrong. They measure different things. Never merge a hat score
> with a Google score into one ranking.**

### 4. Sample first, then decide whether to pay for the API

Matching a full register against Google needs the Places API (paid). Before paying, **sample**:

15 random venues looked up one by one → **13 clean matches (87%)**. Both failures had the same
cause: **the register stores the licence holder's legal name (Pty Ltd), not the trading name**;
a `T/As` field recovers some of them.

More importantly: **2 of the 13 clean matches cleared the main gate and were missing from the
existing list.**

> **That is the real finding — the ceiling was never the gate being too strict, it was the
> candidate pool being too narrow.**

**Full-run cost** (Google Places API; `rating` and `userRatingCount` are Enterprise-SKU fields,
review text is Enterprise + Atmosphere, and a request bills at the highest tier it asks for):

| Route | Unit price | 7,020 venues, one full pass |
|---|---|---|
| Text Search Enterprise | US$35 / 1,000 | ≈ US$246 |
| Essentials for IDs (free) + Place Details Enterprise | US$20 / 1,000 | ≈ US$140 |
| As above, plus review text | US$25 / 1,000 | ≈ US$176 |

**Covering only the four suburbs with the densest community dining (506 venues) costs about US$10 —
right at the edge of the free tier. That is the highest-value one-off spend.**

---

### 5. Find precincts by street, not by keyword

Keyword search returns a ranked list scattered across the city, which hides the single most useful
fact about migrant food: **it clusters**. The procedure that actually surfaced it is two-step and
cheap.

1. Search the cuisine — in the community's own language where there is one — and take **the address**
   of any hit, not just its name.
2. **Re-search that street.** Then read the street numbers.

Step 2 is what turned one Ethiopian restaurant into **seven East African venues between 147 and 201
Beaudesert Rd**, and one Yemeni restaurant into a Middle Eastern row on Kingston Rd. Neither is
reachable by ranking: the neighbours are smaller, lower-sampled, and never in the first twenty
results.

It also corrects the write-up. Re-searching Kingston Rd turned up a Bosnian café at number 200,
which meant the precinct could no longer honestly be labelled "Middle Eastern" without qualification.

> **Two checks before a street becomes a precinct in the output.** Confirm each venue's **local
> government area** — half of these sit in a neighbouring council, outside whatever register you used
> as a denominator. And confirm the **city**: the highest-rated Macedonian result in this project's
> European sweep was 70 km away in another city entirely, and would have been published if the
> address had not been read.

### 6. Give every venue exactly one home; everything else is an index

A list like this grows by adding axes. Budget, then area, then ethnicity, then cuisine, then food
type, then gate result — each one reasonable on its own. Six axes later nothing says **which axis
owns a venue's full record**, and the document starts answering the same question in three places
with three different subsets.

The fix is one sentence, applied everywhere: **a venue's full record — address, price, rating,
source, notes — appears in exactly one section. Every other mention is a pointer.** Then add a
single generated index that maps "I want X" to the section that owns it.

Two things this forces you to decide, and both are improvements:

- **Which axis is primary.** Here it is area, because the reader's real question is "I am here,
  what is nearby". Cuisine became the index.
- **What to do with the venues the primary axis does not cover.** A French restaurant belongs to no
  community precinct. So the rule is: *area owns it if it sits in a mapped precinct, otherwise its
  cuisine card owns it.* Stated once, it decides every case.

> **Generate the index, never type it.** Derive it from the tables that already exist — cuisine,
> top venue by rating, owning section. Typed by hand it is wrong within two edits.

> **Before reordering a published document, prove the transform is lossless.** Parse it into
> blocks, reassemble in the original order, and require the result to match the source byte for
> byte. Only then reorder. Doing this caught a card emitted twice and a correction that would have
> been deleted along with the section that happened to hold it.

### 7. Publish the dataset so someone can query it without installing anything

A downloadable CSV is not the same as a queryable dataset. Two standard pieces close
that gap and neither needs a server:

- **A Frictionless [Data Package](https://specs.frictionlessdata.io/data-package/) descriptor**
  (`datapackage.json`) declaring each CSV's fields, types, row count, primary key and
  upstream sources. **Generate it from the CSVs**; a hand-written schema is wrong the first
  time a column is added, so a test here fails the build when the two disagree.
- **[Datasette Lite](https://github.com/simonw/datasette-lite)**, which runs Datasette in the
  reader's browser over a CSV URL (`?csv=https://…`). A static host that sends
  `access-control-allow-origin: *` — GitHub Pages does — is the only requirement, so full SQL
  over the published data costs one link.

> **Check the licence claim before you write one.** The first draft of this descriptor
> declared CC-BY over the whole package. The repository is MIT, and one upstream source is
> explicitly *not redistributable*. The descriptor now states MIT **for the compilation only**
> and points at the per-source terms, and a test compares it against `LICENSE`.


## 4. What the output should look like

A list built this way should carry all five of these:

1. **Every figure labelled by platform** — `4.8/1,186 (Google, live)`, never a bare number.
2. **Every price labelled by source** — official site / crowd-reported band / review photo /
   third-party / not found.
3. **Cleared and not-cleared listed separately**, with the failing scores shown so the reader can
   judge.
4. **Every venue linked to a map**, one tap to navigate.
5. **Known gaps given their own section** — what could not be found, could not be retrieved, and
   has not been done.

See [`docs/index.html`](docs/index.html) (web) and [`docs/pdf/`](docs/pdf/) (PDF build; page and link counts are printed by `make pdf-stats`, not hard-coded here).

---

## 5. Limits of this method

- **Everything expires.** Prices, hours and ratings change daily. Collection dates are recorded
  throughout; re-verify before you rely on anything.
- **It selects "worth a special trip", not "everything".** Roughly 300 venues out of 7,020 — the
  main gate is deliberately a very narrow sieve.
- **It cannot measure your taste.** A rating is a crowd's average judgement, not yours.
- **Residual bias remains** against venues with thin English-language review ecosystems; the
  Chinese-language platforms could not be retrieved (CAPTCHA).
