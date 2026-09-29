# 评分闸门法 ｜ The Review-Gate Method

*[English version ｜ 英文版](README.md)*

用**可核验的评分数据**筛餐厅，而不是转述攻略文章。
方法本体 + 一份用它做出来的完整案例（布里斯班，300+ 家）。

A reusable method for building restaurant shortlists from **verifiable review data**
instead of blog roundups — plus one fully worked case (Brisbane, 300+ venues).

---

## 这套方法在做什么 ｜ The idea

多数餐厅清单是「把网上推荐的抄一遍」。这里反过来：**先定一条写死的闸门，活下来的才进表。**

Most restaurant lists relay whatever the internet recommends. This inverts it:
**state a hard gate first, and only what survives goes in.**

**主闸门 ｜ The main gate：Google ≥ 4.7 AND ≥ 200 reviews**

但很快会发现**一条闸门不够**——咖啡店遍地 4.8，俱乐部整体分只有 4.2，族裔餐馆英文点评天然稀少。
所以方法的核心变成：**每个品类各立一条闸门，并写明门槛与放宽／收紧的理由。**

One gate is not enough: coffee shops sit at 4.8 everywhere, licensed clubs at 4.2, and
community-facing restaurants have structurally fewer English reviews. So the method became:
**one stated gate per category, with the reason it was loosened or tightened written down.**

**→ 方法全文见 [`METHOD.zh.md`](METHOD.zh.md)**（[English](METHOD.md)） ——一套闸门表、九条实际踩出来的教训、六个可复用做法。

---

## 两条硬规则 ｜ Two hard rules

1. **平台分开记，绝不混用、绝不取平均。** 一个没标平台的数字是错误，不是省略。
   *Platforms recorded separately, never averaged. A number without a platform label is a bug.*
2. **查不到就写「未查到」并说明卡在哪里。** 不估算、不编造。
   *Anything not found is written as "not found", with the reason. Never estimated.*

---

## 案例：布里斯班 ｜ The worked case: Brisbane

- 🌐 **[网页版 ｜ Web](https://cgwlovely.github.io/review-gated-dining/)**
- 📄 **[PDF](docs/pdf/Brisbane_2026_餐厅指南.pdf)** —— 页数与链接数用 `make pdf-stats` 现算
- 🔬 **[完整调查记录 ｜ Full research record](research/brisbane-dining.md)**（19 节，含被否决的候选与未完成项）

页面上共 **350 条门店链接**、**284 家独立门店**，其中 **27 家**出现在一个以上的章节——都是刻意的交叉列（例如同时出现在价位档与主表），每一处都在行内写明原因。这三个数由 `make build` 解析已发布页面得出，写进 [`build/summary.md`](build/summary.md) 并注入封面；**没有一个是手写的**，封面也不再另存一份会漂移的副本。结构化数据里两个数都会输出——见 [`build/summary.md`](build/summary.md) 与[数据浏览页](https://cgwlovely.github.io/review-gated-dining/data.html)。

十节，每节回答一个问题：按预算 · 值得专程去 · **按区域**（商场楼层、街区、社区餐饮带）· **按菜系（含覆盖全书的 35 行索引）** · 按想吃的东西 · 咖啡饮品轻食 · 市场鱼档采购 · 会员餐与 Pub 特价 · 订位与出发前检查 · 方法口径来源。

**贯穿全书一条规则：每家店的完整记录只出现在一个章节里**，其余章节一律只做指向。见方法第 6 个做法。

**每家店都链到 Google 地图；每个价格都标了来源**（官网 / Google 众报 / 评论照片 / 第三方 / 未查到）。

### 案例里最有价值的几条发现

- **候选池的语言决定结果。** 用英文榜单会得出「某片区华人餐饮集体不过闸门」的错误结论；
  改用中文按菜系搜，同一片区冒出一批 4.6–4.9 的店。
- **第三方盘点的套餐价系统性过期**——凡能与官网对上的，无一例外偏低。
- **样本量大 ≠ 分数高。** 全澳最有名的可颂店在本地两家分店都没过闸门。
- **官方持牌名录当分母。** 市议会开放数据显示全市 **8,046 条持牌记录、7,020 家面向食客**，
  本清单只覆盖约 2%——因为主闸门本就是极窄的筛子。
- **随机抽样能验证候选池有多窄**：抽 13 家就有 2 家是原清单漏掉的过闸门店。

---

## 可复现构建 ｜ Reproducible build

Venue data is moving out of prose into [`data/`](data/). **Scope today: the quick-pick section, the
main-gate table and the data browser are generated from it; the rest of the guide is still
hand-maintained.** Migration of the remaining venues is tracked in
[issue #1](https://github.com/cgwlovely/review-gated-dining/issues/1).

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
- **`conservative_rating_proxy`** + **`borderline`** — a **heuristic small-sample penalty, not a
  confidence interval**. Google publishes a mean and a count, not the 1–5 vote distribution, so no
  strict interval is computable from what we have; the field is named for what it is. 18 of the 25
  gate-passers trip it, which reads as "most passers sit close enough to the line that a modest
  sample penalty pushes them under" — a prompt to re-check, not a claim that they fail.
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

### 呈现层（issue #1 第二条评论）

The front of the guide is now **generated from the dataset**, not hand-written:

- **A three-minute quick-pick section** — first-timer picks, two-person budget bands, and
  by-occasion picks — regenerated by `make build` between `<!--quickpick:start/end-->` markers,
  so it can never drift from the tables behind it.
- **`recommendation_tier`** (`editors_pick` / `conditional` / `directory`) is a data field, not
  something inferred from `gate_pass`. Every venue also carries a one-line reason in both languages.
- **Counts are measured, not asserted.** The cover reports **distinct venues / display rows /
  venues repeated across sections**, computed by parsing the published page. The old unexplained
  "300+" is gone.
- **Flags** (`booking_ahead`, `weekend_surcharge`, `member_price`, `veg_friendly`, `price_stale`)
  and a booking chip render as scannable labels.
- **Budget bands never absorb a price that cannot be converted.** À la carte venues print
  "按菜品计价 · à la carte" instead of being forced into a band.

### 评审循环

The method has been sharpened more by adversarial review than by adding venues. Two rounds of
outside review caught three defects the maintainer had not seen: a Thai restaurant tagged into a
Chinese-food shortlist, budget bands assigned on entry price while labelled as full ranges, and a
small-sample heuristic described as a 95% confidence interval it was not.

That loop is now a script:

```bash
make review        # dry run - print the critique, post nothing
make review-post   # post it to issue #1, signed as a model review
```

`scripts/review_loop.py` assembles the prompt from the repository itself — `gates.yml`,
`venues.csv`, the exemptions file, `build/summary.md`, the build and test output, and the full
issue thread — asks an external model to find concrete, checkable defects, and posts the result
**signed**, so no one mistakes it for a human review. It needs `OPENAI_API_KEY` in the environment
or a key in `~/.config/openai.key`; with no key it prints what to do and sends nothing.

Reviews are archived at `build/review-<commit>.md`, so every critique stays pinned to the commit
it was made against.

---

## 仓库结构 ｜ Layout

```text
METHOD.md       方法本体（英文）
METHOD.zh.md    方法本体（中文）：闸门表、九条教训、六个可复用做法
README.md       英文说明
README.zh.md    本文件
docs/        发布站点（GitHub Pages）：index.html + PDF + 地图
research/    完整调查记录 + 市议会持牌名录全量导出（8,046 条）
data/           venues.csv · gates.yml · sources.csv · venue_aliases.csv
build/          构建产物：venues.json/csv · main-table.md · summary.md
scripts/        build.py（数据→闸门→产出）· tests/ · 地图渲染脚本
Makefile        make check | build | test | maps
```

---

## 数据边界 ｜ Data boundaries

用这里任何一个数字之前，先读这一段。

- **一切都会过期。** 价格、营业时间、评分每天在变。文中标注了采集日期，出行前必须复核。
- **评分一律标平台。** Google 实时值与第三方镜像会差到跨档（镜像 4.6 / 实时 4.5 的情况真实出现过）。
- **「未查到」表示确实检索未果**，不是猜测的占位符。
- **本清单挑的是「值得专程去」，不是全部**——全市 7,020 家，这里约 300 家。
- **对英文点评生态薄弱的餐馆仍有残余偏差**；中文平台（大众点评／小红书）因人机验证未取到。

---

## 数据来源 ｜ Sources

- [Brisbane City Council · Food Safety Permits（Eat Safe）](https://data.brisbane.qld.gov.au/explore/dataset/food-safety-permits/) — CC-BY，8,046 条，全量留档于 `research/`
- Google Maps 各店条目（评分、评论数、众报价位带、菜单照片）
- [AGFG 澳洲美食指南帽子奖](https://www.agfg.com.au/awards/brisbane) · [Gourmet Traveller 餐厅指南](https://www.gourmettraveller.com.au/dining-out/restaurant-guide/best-restaurants-queensland-20148/)
- 各餐厅官网与官方点单页
- 地图底图 © OpenStreetMap contributors

---

## 许可 ｜ Licence

方法、代码与文字采用 [MIT](LICENSE)。
市议会数据沿用其 CC-BY 授权；地图底图沿用 OpenStreetMap 的 ODbL。

The method, code and prose are MIT. Council data keeps its CC-BY licence;
map tiles keep OpenStreetMap's ODbL.
