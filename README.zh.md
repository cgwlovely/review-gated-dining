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

**→ 方法全文见 [`METHOD.zh.md`](METHOD.zh.md)**（[English](METHOD.md)） ——一套闸门表、八条实际踩出来的教训、四个可复用做法。

---

## 两条硬规则 ｜ Two hard rules

1. **平台分开记，绝不混用、绝不取平均。** 一个没标平台的数字是错误，不是省略。
   *Platforms recorded separately, never averaged. A number without a platform label is a bug.*
2. **查不到就写「未查到」并说明卡在哪里。** 不估算、不编造。
   *Anything not found is written as "not found", with the reason. Never estimated.*

---

## 案例：布里斯班 ｜ The worked case: Brisbane

- 🌐 **[网页版 ｜ Web](https://cgwlovely.github.io/review-gated-dining/)**
- 📄 **[PDF（45 页，389 个可点链接）](docs/pdf/Brisbane_2026_餐厅指南.pdf)**
- 🔬 **[完整调查记录 ｜ Full research record](research/brisbane-dining.md)**（19 节，含被否决的候选与未完成项）

收录约 **300 家**，分档：过主闸门 25 家 · 五档价位阶梯 50 条 · 亚洲餐饮按商场楼层与菜系 ·
十余个菜系 · 牛排 · 咖啡 · 奶茶饮品 · 海鲜鱼档 · 精酿啤酒 · 农夫市集 · 俱乐部会员价 · Pub 每周特价。

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

## 仓库结构 ｜ Layout

```text
METHOD.md       方法本体（英文）
METHOD.zh.md    方法本体（中文）：闸门表、八条教训、四个可复用做法
README.md       英文说明
README.zh.md    本文件
docs/        发布站点（GitHub Pages）：index.html + PDF + 地图
research/    完整调查记录 + 市议会持牌名录全量导出（8,046 条）
scripts/     OSM 瓦片地图渲染脚本
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
