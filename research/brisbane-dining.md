# Brisbane 餐厅打卡点扫查

> **English abstract** — This is the full working record behind the Brisbane case study:
> every gate applied, every candidate rejected, every source that could not be retrieved, and the
> method lessons that came out of each mistake. Written in Chinese; venue names, addresses, ratings
> and prices are in English throughout. The distilled method is in
> [`METHOD.md`](../METHOD.md) (English) / [`METHOD.zh.md`](../METHOD.zh.md) (中文).
> The finished, readable output is [`docs/index.html`](../docs/index.html).
>
> Nineteen sections: three independent rating systems kept apart · the source-language bias that
> invalidated an early conclusion · menus recovered from Google review photos · a city-wide census
> of 8,046 licensed premises used as the denominator · a 15-venue sampling study measuring
> register-to-Google match rate (87%) · Places API cost modelling · and every category's gate with
> its rationale.

> **这份是完整调查记录**（含被否决的候选、取不到的口径、方法学教训）。
> 只想要能直接用的清单，看干净版网页：[`docs/index.html`](../docs/index.html)（或 [PDF](../docs/pdf/Brisbane_2026_餐厅指南.pdf)，19 页，地址链接可点）。

**评分核查 2026-09-28（Google／Wanderlog 镜像 + Google Maps 实时 + AGFG 帽子奖 + Gourmet Traveller 指南）。菜单价格逐家进官网／官方点单页／Google 评论照片核查 2026-09-28。**
沿用本仓库方法（见 [`METHOD.md`](../METHOD.md)）：

- **闸门：Google ≥4.7 且评论 ≥200** 进主表；未过闸门的另列一段，写明为什么仍然可能去。
- **评分一律标平台，绝不混用、不取平均。** Google 评分与评论数取自 Wanderlog 对 Google Maps 的镜像页（**会比 Google Maps 实时值滞后**），下文统一记为「Google／Wanderlog 镜像」。
- **价格一律以商家自己的页面为准。** 本轮逐家打开官网／官方点单页／官方菜单 PDF 取价，出处逐条标注；**取不到的写「未查到」并说明卡在哪里**，不估算、不编造。
- 地图坐标由各店**自己公布的街道地址**经 Nominatim 反查得到，脚本见 [`scripts/build_brisbane_dining_map.py`](../scripts/build_brisbane_dining_map.py)。

---

## ⚠️ 本轮最重要的发现：第三方盘点的套餐价系统性过期

进官网核价之前，这份文档用的是 Sitchu、Urban List 等本地媒体的套餐盘点。**逐家核完之后，凡是能对上的，第三方价格全部偏低**：

| 店 | 第三方盘点价 | 官网实际价（2026-09-28） | 差 |
|---|---|---|---|
| hôntô | $84/人（Sitchu） | **$89 / $130 两档** | +$5 起 |
| Agnes | $100/人（Sitchu） | **$89 / $139 两档** | 结构完全不同 |
| sAme sAme | $84/人（Sitchu） | **$89 / $130 两档** | +$5 起 |
| Joy | $205（Urban List）／$175（TripAdvisor） | **$220** | +$15～45 |
| Exhibition | $247（Urban List） | **$255 平日／$335 周末** | +$8～88 |

**结论：本文档里凡标「官网」的价格才可直接用于预算；标「第三方」的一律视为下限，订位时必须重算。** 这条对整个仓库通用——`research/nsw-roadtrip/pricing/` 下的价格轮也应该按同一标准复核。

---

## 一、第二、第三套测评口径（平台分开记，绝不混用）

Google 只是一套口径。本轮又核到两套**独立、专业评审制**的数据，以及两套**取不到**的。

### A. AGFG 澳洲美食指南 2026 帽子奖（布里斯班 49 家，20 分制）

评审打分，不是本项目投票。分数直接从 AGFG 官网 2026 布里斯班榜单读取（核查日 2026-09-28）。

| 分数 | 布里斯班入选（按官网顺序） |
|---|---|
| **18** | **Exhibition** |
| **17** | **Joy** |
| **16** | Rogue Bistro |
| **15** | Deer Duck Bistro · Attimi by Dario Manca · Essa · SUUM · **Montrachet** |
| **14** | C'est Bon · Agnes · e'cco bistro · Perspective Dining · Fatcow on James St |
| **13** | Rich & Rare · Ach Wine Bar · Layla · **hôntô** · Ippin · **Longwang** · August · Komeyui · Otto Brisbane · The Wolf · sAme sAme · Clarence · Marlowe · Bosco · Rosmarino · The Lodge · Sokyo |
| **12** | Herve's · Dark Shepherd · Donna Chang · Firma Italian · Azteca · Moo Moo · Pompette · Mosconi · Stanley · The Balfour · Pilloni · Central Restaurant · **The Brasserie at Naldham House** · Sono Portside · Ramona Trattoria · Hellenika · Hideki · Melrose · Winnifred's |

（**加粗**＝同时过了本文的 Google 闸门。）

### B. Gourmet Traveller 2026 餐厅指南（全澳 100 家，昆州 15 家）

匿名到访、自费结账的评论员制。昆州 15 家里布里斯班占 9 家：
**Agnes · August · Clarence · Essa · Exhibition · Joy · Pilloni · Supernormal Brisbane · +81 Sushi Kappo**。
昆州年度餐厅是 Noosa 腹地的 **The Woodshed**（不在布里斯班）。

### C. 三套口径分歧有多大（这是本节的重点）

| 比较 | 结果 |
|---|---|
| 本文 Google 闸门的 23 家 ∩ AGFG 49 家 | **只有 6 家**：Exhibition(18)、Joy(17)、Montrachet(15)、hôntô(13)、Longwang(13)、Naldham House 的 The Brasserie(12)、Sono Portside(12) |
| 本文主表里 **AGFG 完全没收录** | **The Fifty Six、Short Grain、1889 Enoteca、Beccofino、Rothwell's、Longtime Dining、Farm House、NAÏM、Smoked Paprika、Little Black Pug、Oh Boy、Unbearable Bagels、Hashtag、Vegeme、Ngon、John Mills Himself** |
| AGFG 第 3 名 Rogue Bistro（16 分） | 在 Google 口径下**没进本文任何一张表** |
| GT 布里斯班 9 家 ∩ 本文 Google 闸门 | **只有 2 家**：Exhibition、Joy（Agnes、Essa 都没过 Google 闸门） |
| **三套口径同时点名的** | **只有 Exhibition 和 Joy** |

**怎么用这条：** 想要「专业评审认可」就看 AGFG／GT；想要「大量真实顾客长期打分」就看 Google。**两者只在 Exhibition 和 Joy 上完全重合**，其余地方分歧巨大——这不是谁错了，是两套口径在测不同的东西。**永远不要把帽子分和 Google 分混着排名。**

### D. 取不到的两套（照实记录）

- **TripAdvisor**：页面对自动访问返回空白，**未取到**。
- **大众点评**：跳转到滑块人机验证。**本仓库不做验证码**，因此**未取到**；小红书同理未尝试。
  → 这意味着**第七节说的 Sunnybank 中文口径缺口，本轮仍然没有补上**。

### E. 一处人物更正

Gourmet Traveller 2026 明确写 **Exhibition 是 Tim Scott 带队**，「20 道以上」。结合 Joy 店方「Tim Scott 已离开三年半」的澄清，两条现在能对上了：**Tim Scott 在 Exhibition，Sarah Baldwin 在 Joy**——两家恰好是三套口径里唯一都点名的两家。

---

## 二、原表漏了 5 家（来源列表有偏差）

**问题出在我自己的取样上。** 第一轮的候选全部来自 Wanderlog 的「best restaurants／best places to eat」类榜单，这类榜单天然排除汉堡店、咖啡馆、素食小馆、越南小馆。改用「cheap eats／cafes／Vietnamese／dumplings」几张榜单重扫后，**又找出 5 家同样过了「Google ≥4.7 且 ≥200」这条原闸门的店**：

| # | 店 | 类型 | Google（实时） | Google 众报人均 | 地址 |
|---|---|---|---|---|---|
| 19 | **John Mills Himself** | 咖啡／小酒吧 | **4.8**／1,120 | **$1–20** | [40 Charlotte St, CBD](https://www.google.com/maps/search/?api=1&query=John%20Mills%20Himself%2040%20Charlotte%20St%2C%20Brisbane%20City%20QLD%204000) |
| 20 | **Hashtag Burgers and Waffles** | 汉堡／华夫 | **4.7**／2,154 | **$20–40** | [Shop 3/477 Brunswick St, Fortitude Valley](https://www.google.com/maps/search/?api=1&query=Hashtag%20Burgers%20and%20Waffles%20Shop%203/477%20Brunswick%20St%2C%20Fortitude%20Valley%20QLD%204006) |
| 21 | **Sono Japanese** Portside Wharf | 日料 | **4.7**／2,388 | 未显示 | 39 Hercules St, Hamilton（AGFG 12 分） |
| 22 | **Vegeme** | 素食／越南素 | **4.7**／1,001 | **$1–20** | [Shop 9/220 Melbourne St, South Brisbane](https://www.google.com/maps/search/?api=1&query=Vegeme%20Shop%209/220%20Melbourne%20St%2C%20South%20Brisbane%20QLD%204101) |
| 23 | **Ngon Brisbane** | 越南 | **4.7**／648 | **$20–40** | [183 Given Tce, Paddington](https://www.google.com/maps/search/?api=1&query=Ngon%20Brisbane%20183%20Given%20Tce%2C%20Paddington%20QLD%204064) |

**这条教训比这 5 家店本身更重要：闸门再严，也挡不住候选池本身的偏差。** 下次做任何城市，候选池必须从至少 5 类榜单取（正餐、平价、咖啡、单一菜系、单一品类），再过闸门。

### 两家的完整菜单（本轮新取）

**Hashtag Burgers and Waffles**（菜单取自 Google 评论照片，见第三节）
汉堡：Cheeky Tuesday $15.5 · Your Dirty Uncle $15.5 · Morning Wood $17.5 · Dirty Wood $22 · P-BJ $23.5（双肉双芝士＋花生酱＋辣椒酱）· **Get Litt Burger $35**（双肉双芝士双培根＋洋葱圈，夹在芝士吐司里）
Loaded fries：Loaded Totts $19 · Fried Chook $21 · Smashy $22.5 · BBQ Lock N Load $23
华夫 MMMMM…Waffles $16.5（换成炸鸡＋枫糖 +$5）；奶昔一律 $10。

**Ngon Brisbane**（官网 PDF，链接由 Google Maps 提供）
小盘 $16–18：槟榔叶和牛卷(3) $18 · 鸭肉春卷(4) $18 · 椒盐鱿鱼 $18 · 五香爆米花鸡 $18 · 米纸卷(3) $18 · 猪肉饺(3) $16 · 椒盐豆腐 $16 · 越式茄子 $16 · 烤玉米 $16
大盘 $26–32：**姜汁焦糖鸭 $32** · 罗望子脆皮猪腩 $30 · 香茅辣椒鸡 $28 · 越式煎饼 $28 · 素咖喱 $28 · 炒面 $26
汤面／沙拉 $24–28：牛肉河粉 $24 · 云吞面 $24 · 青木瓜沙拉 $24 · 鸭肉沙拉 $28
配菜 $4–14；甜点：黄金流沙包 $9 · 班兰布丁 $14 · 炸冰淇淋 $16

---

## 三、把 Google 评论照片当菜单来源（本轮新方法，有效）

上一轮有两家标了「未查到」，原因都是**官网菜单链接失效**。这轮改从 **Google Maps 的「Menu」照片**取——顾客拍的实体菜单照片——两家都拿到了。

### Rothwell's Bar & Grill（官网 PDF 两个版本都 404）

Google Maps 上另有一个 2025-10 版 PDF 链接，实测同样 404；但「Menu」相册里有 12 张照片，第 1 张是完整菜单页：

| 主菜 | 价 | 配菜 | 价 | 甜点 | 价 |
|---|---:|---|---:|---|---:|
| Gold Band 鲷鱼 | $60 | 薯条 | $12 | 榛子焦糖布丁 | $19 |
| 鱼派（带子、虾、海鲈） | $59 | 生菜沙拉 | $12 | Eton mess | $19 |
| 油封鸭腿 cassoulet | $49 | 土豆泥 | $18 | 玛德琳配威士忌焦糖 | $19 |
| 烤羊肉配茄子泥 | $49 | 奶油菠菜 | $17 | 巧克力 trifle | $19 |
| **Beef Wellington 600g（共享）** | **$134** | 蜂蜜百里香胡萝卜 | $16 | 巧克力熔岩（需 20 分钟） | $19 |
| | | 培根雪莉醋炒抱子甘蓝 | $16 | 三款奶酪配苹果与腌核桃 | $27 |

刷卡加收 1.4%。
⚠️ **GRILL（牛排）区照片对焦不清**：五款分别约 $55–69，**800g 六周干式熟成肋眼约 $155**——数字不确定，**到店确认**。Google 众报人均 **$80–200**，Google 实时 **4.7／1,067**。

### Longtime Dining（官网菜单页渲染为空白）

Google Maps「Menu」相册第 1 张是**完整饮茶单，中英对照**：

| 蒸点 | 价 | 蒸点 | 价 |
|---|---:|---|---:|
| 朗廷八寶（八件，四款各两件） | **$47** | 蝶豆花海鮮餃(3) | $23 |
| 蝦餃皇(3) | $20 | 火鴨鮮蝦餃(3) | $22 |
| 墨魚汁芥末蝦餃(3) | $25 | 黑鬆露野菌餃(3) | $23 |
| 魚籽豬蝦燒賣(4) | $23 | 羅漢齋素餃(3) | $21 |
| 黑鬆露雞燒賣(4) | $23 | 珍珠荷葉糯米雞(2) | $22 |
| 小籠包(3) | $18 | 豉汁蒸排骨 | $20 |
| 魚籽菠菜帶子餃(3) | $25 | 豉汁蒸鳳爪 | $23 |
| 鮮蝦韭菜餃(3) | $21 | 蜜汁叉燒包(3) | $24 |
| 金黃流沙包(3) | $25 | 豬仔包(2) | $15 |
| 馬拉糕 | $18 | | |

菜单上印着：**刷卡 +2%、周末 +10%、公共假日 +20%**；**饮茶点心不接受因饮食需求改配**。Google 众报人均 **$40–120**，Google 实时 **4.8／4,821**。

### 这个方法的边界

- **能用**：官网挂了、菜单只在店内、或 PDF 链接失效时。照片里带价格的实体菜单是可核验的一手材料。
- **不能用**：照片可能是**旧版菜单**（拍摄日期不明），对焦不清时数字会读错（Rothwell's 的牛排区就是）。
- **因此本文对这两家的标注是「Google 评论照片」，不是「官网」**——可信度介于官网与第三方之间，**订位前仍需确认**。

---

## 四、Wanderlog 镜像 vs Google 实时：滞后有多大

本轮顺手用 Google Maps 实时值复核了 19 家，结论：**镜像通常只滞后 1–2% 的评论数，但足以让边缘店跨档**。

| 店 | Wanderlog 镜像 | Google 实时（2026-09-28） |
|---|---|---|
| Longtime Dining | 4.8／4,749 | 4.8／**4,821** |
| Eat Street Northshore | 4.6／15,597 | 4.6／**15,638** |
| Julius Pizzeria | 4.6／3,985 | 4.6／**4,009** |
| Chu The Phat | 4.5／3,410 | 4.5／**3,477** |
| **Andonis Cafe & Bar** | **4.6**／3,283 | **4.5**／3,313 ← **掉了一档** |
| Vegeme | 4.7／**995** | 4.7／**1,001** ← 刚跨过 1,000 |
| Rothwell's | 4.7／1,048 | 4.7／1,067 |
| Ngon | 4.7／628 | 4.7／648 |
| Sono Portside | 4.7／2,369 | 4.7／2,388 |
| Hashtag Burgers | 4.7／2,136 | 4.7／2,154 |

**结论：主表的评分可以先用镜像做筛选，但任何卡在 4.5/4.7 边界或 200/1,000 条边界的店，订位前必须看一次 Google 实时值。**

---

## 五、过闸门的 23 家（Google ≥4.7 且 ≥200）

排序：评分降序，同分按评论数降序。编号与地图上的针号一致（19–23 是第二节补进来的 5 家）。

| # | 店 | 菜系 | Google／Wanderlog | 价格（出处已标） | 地址 |
|---|---|---|---|---|---|
| 1 | **Exhibition** | 现代澳菜 omakase | **4.9**／397 | **$255/人**（平日）· **$335/人**（周末，含 $80 餐饮额度）；酒水配对 $90–$340 — **官网** | [Basement 2/109 Edward St, CBD](https://www.google.com/maps/search/?api=1&query=Exhibition%20Basement%202/109%20Edward%20St%2C%20Brisbane%20City%20QLD%204000) |
| 2 | **Longtime Dining** | 精致粤菜／点心 | **4.8**／4,749 | **未查到** — 官网 longtimedining.com 菜单页渲染为空白 | [L1, 226 Queen St（Queens Plaza）](https://www.google.com/maps/search/?api=1&query=Longtime%20Dining%20L1%2C%20226%20Queen%20St%2C%20Brisbane%20City%20QLD%204000) |
| 3 | **Longwang** | 现代泛亚 | **4.8**／2,118 | Jade **$88/人**｜Dragon's **$122/人**｜Claw Feast **$149/人**；单点 $7–22 — **官网**。周末 +10%，公假 +20% | [144 Edward St, CBD](https://www.google.com/maps/search/?api=1&query=Longwang%20144%20Edward%20St%2C%20Brisbane%20City%20QLD%204000) |
| 4 | **Oh Boy, Bok Choy!** | 东南亚（越/泰/马/中） | **4.8**／1,991 | Banquet **$62.5/人**；Bubbles & Bao 周五至周日午餐 **$89/人**（含 2 小时气泡酒、house wine、啤酒）；单点 $12.9–42.5 — **官网 PDF**。周末 +5%，公假 +16.5% | [264 Stafford Rd, Stafford](https://www.google.com/maps/search/?api=1&query=Oh%20Boy%2C%20Bok%20Choy%21%20264%20Stafford%20Rd%2C%20Stafford%20QLD%204053) |
| 5 | **Little Black Pug** | Brunch | **4.8**／1,663 | 单点 **$9–31**（招牌 Dog's Breakfast $31）— **官网 PDF** | [Logan Rd, Mount Gravatt Central](https://www.google.com/maps/search/?api=1&query=Little%20Black%20Pug%20Logan%20Rd%2C%20Mount%20Gravatt%20Central%20QLD%204122) |
| 6 | **Short Grain** | 泰菜 | **4.8**／606 | 套餐 **$55／$85／$125 每位**（素食 $55／$85）；咖喱 $55–75 — **官网**。周日 +10%，公假 +15% | [15 Marshall St, Fortitude Valley](https://www.google.com/maps/search/?api=1&query=Short%20Grain%2015%20Marshall%20St%2C%20Fortitude%20Valley%20QLD%204006) |
| 7 | **Farm House, Kedron** | 全日咖啡馆 | **4.7**／2,981 | 主食 **$25.5–28.5** — **官网 PDF**。周末 +5%，公假 +16.5% | [9 Somerset Rd, Kedron](https://www.google.com/maps/search/?api=1&query=Farm%20House%2C%20Kedron%209%20Somerset%20Rd%2C%20Kedron%20QLD%204031) |
| 8 | **1889 Enoteca** | 罗马菜／意大利自然酒 | **4.7**／2,341 | 意面 **$25–38**、前菜 $21–35、主菜 $39–100 — **官方点单页（取餐口径）** | [10–12 Logan Rd, Woolloongabba](https://www.google.com/maps/search/?api=1&query=1889%20Enoteca%2010-12%20Logan%20Rd%2C%20Woolloongabba%20QLD%204102) |
| 9 | **NAÏM** | 中东（多素、清真友好） | **4.7**／1,849 | 早午餐 **$14–29** — **官方点单页**；晚餐 Chef's Banquet 官网未上价 | [14 Collingwood St, Paddington](https://www.google.com/maps/search/?api=1&query=NA%C3%8FM%2014%20Collingwood%20St%2C%20Paddington%20QLD%204064) |
| 10 | **hôntô** | 现代日料 | **4.7**／1,603 | Banquet **$89/人** 或 **$130/人**；单点 $6–110 — **官网**。周末 +10%，公假 +15% | [Alden St, Fortitude Valley](https://www.google.com/maps/search/?api=1&query=h%C3%B4nt%C3%B4%20Alden%20St%2C%20Fortitude%20Valley%20QLD%204006) |
| 11 | **Beccofino** | 意式柴烧披萨 | **4.7**／1,220 | 披萨 **$28.5–36.5**、意面 $35–39.5、主菜 $48.5–60 — **官网 PDF**。周日 +10%，公假 +15% | [10 Vernon Tce, Teneriffe](https://www.google.com/maps/search/?api=1&query=Beccofino%2010%20Vernon%20Tce%2C%20Teneriffe%20QLD%204005) |
| 12 | **Rothwell's Bar & Grill** | 老派 grill | **4.7**／1,048 | **未查到** — 官网「Dining Menu（2026-03）」PDF 链接实测 **404** | [235 Edward St, CBD](https://www.google.com/maps/search/?api=1&query=Rothwell%27s%20Bar%20%26%20Grill%20235%20Edward%20St%2C%20Brisbane%20City%20QLD%204000) |
| 13 | **Smoked Paprika** | 匈牙利式早餐 | **4.7**／924 | 早餐 **$13.9–29.9**、午餐 $16.9–27.9 — **官网** | [2/5 Nash St, Paddington（Rosalie）](https://www.google.com/maps/search/?api=1&query=Smoked%20Paprika%202/5%20Nash%20St%2C%20Paddington%20QLD%204064) |
| 14 | **Montrachet** | 法餐 | **4.7**／890 | 单点：前菜 **$26–33**、主菜 **$46–82**、甜点 $20–26 — **官网 PDF**；6 道 degustation $150（**第三方**）。公假 +15% | [1/30 King St, Bowen Hills](https://www.google.com/maps/search/?api=1&query=Montrachet%201/30%20King%20St%2C%20Bowen%20Hills%20QLD%204006) |
| 15 | **Naldham House** | Brasserie／酒吧（一栋四店） | **4.7**／432 | **未查到** — The Brasserie 无独立菜单页 | [Mary St × Felix St, CBD](https://www.google.com/maps/search/?api=1&query=Naldham%20House%20Mary%20St%20%26%20Felix%20St%2C%20Brisbane%20City%20QLD%204000) |
| 16 | **Unbearable Bagels** | 贝果＋黑咖啡 | **4.7**／333 | 贝果 **$17–20**、抹酱款 $6–13 — **官方点单页** | [39 Vernon Tce, Teneriffe](https://www.google.com/maps/search/?api=1&query=Unbearable%20Bagels%2039%20Vernon%20Tce%2C%20Teneriffe%20QLD%204005) |
| 17 | **Joy** | 10 座位品尝菜单 | **4.7**／215 | **$220/人** — **官网**（写明随市价变动） | [Shop 7, 694 Ann St, Fortitude Valley（Bakery Lane）](https://www.google.com/maps/search/?api=1&query=Joy%20Shop%207%2C%20694%20Ann%20St%2C%20Fortitude%20Valley%20QLD%204006) |
| 18 | **The Fifty Six** | 现代粤菜 | **4.7**／207 | Short Set **$82/人**（配酒 +$80）｜Long Set **$120/人**（配酒 +$118）；单点点心 $18–20、主菜 $32–62 — **官网 PDF** | [Level 2/33 Felix St（Naldham House 顶层）](https://www.google.com/maps/search/?api=1&query=The%20Fifty%20Six%20Level%202/33%20Felix%20St%2C%20Brisbane%20City%20QLD%204000) |
| 19 | **John Mills Himself** | 咖啡／小酒吧 | **4.8**／1,120（实时） | Google 众报人均 **$1–20**；单价未查到 | [40 Charlotte St, CBD](https://www.google.com/maps/search/?api=1&query=John%20Mills%20Himself%2040%20Charlotte%20St%2C%20Brisbane%20City%20QLD%204000) |
| 20 | **Hashtag Burgers and Waffles** | 汉堡／华夫 | **4.7**／2,154（实时） | 汉堡 **$15.5–35**、loaded fries $19–23、华夫 $16.5、奶昔 $10 — **Google 评论照片** | [Shop 3/477 Brunswick St, Fortitude Valley](https://www.google.com/maps/search/?api=1&query=Hashtag%20Burgers%20and%20Waffles%20Shop%203/477%20Brunswick%20St%2C%20Fortitude%20Valley%20QLD%204006) |
| 21 | **Sono Japanese** Portside | 日料 | **4.7**／2,388（实时） | 未查到（AGFG 12 分） | [39 Hercules St, Hamilton](https://www.google.com/maps/search/?api=1&query=Sono%20Japanese%20Portside%2039%20Hercules%20St%2C%20Hamilton%20QLD%204007) |
| 22 | **Vegeme** | 素食／越南素 | **4.7**／1,001（实时） | Google 众报人均 **$1–20**；单价未查到 | [Shop 9/220 Melbourne St, South Brisbane](https://www.google.com/maps/search/?api=1&query=Vegeme%20Shop%209/220%20Melbourne%20St%2C%20South%20Brisbane%20QLD%204101) |
| 23 | **Ngon Brisbane** | 越南 | **4.7**／648（实时） | 小盘 **$16–18**、大盘 **$26–32**、汤面／沙拉 $24–28 — **官网 PDF** | [183 Given Tce, Paddington](https://www.google.com/maps/search/?api=1&query=Ngon%20Brisbane%20183%20Given%20Tce%2C%20Paddington%20QLD%204064) |

**15 与 18 是同一栋楼**：Naldham House 是一栋历史建筑，里面有四家店——底层 The Brasserie、底层 Naldham Terrace、一层 Club Felix、**顶层 The Fifty Six**。地图上合并成一个针。

---

## 六、值得单独说的 8 家（故事＋怎么点）

### 1. The Fifty Six — 最该由华人食客去吃的一家

**菜系：** 现代粤菜（带新加坡影响），主厨 Gerald Ong。
**在哪：** Level 2/33 Felix Street（Naldham House 顶层）。周二至周六 12:00–15:00、17:30 起。

**故事：** 店名直接来自**昆士兰第一批华人移民——1848 年抵达布里斯班的 56 名劳工**。这不是装饰性的东方符号，是把一段本地华人史写进了招牌。主厨 Gerald Ong 履历包括堪培拉的 Chairman & Yip（香港 The Chairman 的堪培拉分支）以及悉尼的 Porteño、Automata——这条履历解释了为什么这里是「粤菜底子＋现代餐厅手法」，不是茶楼。主厨在菜单上自己写了一句：**「我们的菜是按它该配的酱汁和佐料设计的。」**

**官网单点价（3 件／份）：**

| 点心 | 价 | 主菜 | 价 |
|---|---:|---|---:|
| 虾多士 | $18 | 脆皮柠檬鸡 | $34 |
| 猪肉春卷 | $18 | 椒盐烤菌 | $32 |
| 带子鲜虾烧卖（配 avruga 鱼子） | $20 | 咕咾肉（Bangalow 猪） | $40 |
| 虾饺 | $20 | 蜜汁叉烧（Oria 猪腩） | $40 |
| 小笼包 | $20 | 黑椒牛柳带子 | $58 |
| 田菌水晶饺（素） | $20 | 港式清蒸 Murray 鳕 | $60 |
| | | **招牌烧鸭（半只，Wollemi 鸭＋五香＋Davidson 李酱）** | **$62** |

**两套 banquet（官网 PDF）：**
- **Short Set $82/人**：春卷、小笼包、黑椒带子、凉拌青瓜、椒盐鱿鱼、咕咾肉、蚝油芥兰、茉莉饭、荔枝玫瑰奶冻。配酒 **+$80/人**（含阿根廷 Torrontés、Eden Valley 雷司令、**宁夏西鸽酒庄「玉鸽」马瑟兰**、托卡伊晚收）。
- **Long Set $120/人**：虾多士、带子烧卖、虾饺、天妇罗豆腐、火油炙鰤鱼刺身、木须鸭卷饼、黑椒牛柳带子、蚝油芥兰、茉莉饭、炸冰淇淋配叉烧焦糖。配酒 **+$118/人**（含 Bugey-Cerdon 气泡桃红、**新疆吐鲁番蒲昌麝香**、Haut-Médoc 2006、Beechworth 西拉，以及**瓦罐客家米酒**）。

**值得注意：** 配酒单里塞进了宁夏和新疆的酒，还有客家米酒——这在澳洲的粤菜馆里并不常见，**是这家值得单独写一笔的地方**。海鲜来源按澳洲 AIM 规定逐条标注 a／i／m。

---

### 2. hôntô — 找不到门的那家

**菜系：** 现代日料。**Google／Wanderlog 4.7／1,603。**

**故事：** 入口是 Fortitude Valley 后街 The Wickham Hotel 背后、家具店（Lounge Lovers）卸货口旁的一扇黑门，穿过一条弯曲的黑色隧道才进到全黑墙的空间里。它还握着**南半球规模最大的日本威士忌收藏之一**。**第一次去请留 10 分钟找门。**

**官网价（已核，$84 那个数字是旧的）：**
- **Banquet $89/人**：青瓜 sunomono、毛豆慕斯、白身鱼 taco、吞拿鱼 tataki、唐扬鸡汉堡、猪肉煎饺、**MB9 和牛牛腩**、西洋菜沙拉、饭、黑芝麻巴斯克。
- **Banquet $130/人**：三文鱼 tostada、辣吞拿鱼 taco、鰤鱼配松露醋、**和牛他他**、脆饭配辣鰤鱼、唐扬鸡、MB9 和牛牛腩、白菜、饭、四川菠萝配抹茶椰子雪芭。
- 单点区间：Bites $8–15／件、刺身拼 $55–90、寿司卷 $18–45、主菜 $40–110（**MB9 Kiwami 和牛肋眼 $110**）、甜点 $16–18。
- **周末 +10%，公共假日 +15%。** 周一至周四 17:30 起，周五至周日 17:00 起。

---

### 3. Short Grain — 悉尼 Longrain 主厨的布里斯班第二次开始

**菜系：** 泰菜。**Google／Wanderlog 4.8／606。** 15 Marshall St, Fortitude Valley。

**故事：** 主厨 Martin Boetz 就是悉尼 Longrain 的那个 Boetz。他卖掉 Hawkesbury 的 Cooks Shed 搬来布里斯班时，**本来只想开一家泰国食材店**，不打算做餐厅——结果在一栋历史保护建筑（早年的制衣厂、后来的亚洲食品店）里做成了「店＋餐厅」：进门左手仍然是食材店，卖他自己做的咖喱酱、酱料和即食餐。**这是唯一一家你可以把当天吃到的味道打包带回家的。**

**官网价：**
- 鸭肉 **Massaman 咖喱 $66**（半份 $42）｜大虾红咖喱 $75｜市场鱼绿咖喱 $55｜猪肉 Panang $58
- 脆皮猪肉沙拉 $48｜海鳟 larb $47｜茶熏鹌鹑 $42｜酸辣菌菇 $32
- 焦糖猪肘 $43（半份 $26）｜炖牛肋 $58｜整条脆皮鱼 时价
- 生蚝 $8/只｜香料鸡脆饼 $15/件
- **套餐 $55／$85／$125 每位**（素食 $55／$85）
- **周日 +10%，公共假日 +15%**（官网明示）
- 午餐 周五、周日 12:00–16:00、周六 12:00–15:00；晚餐 周三至周六 17:00–21:30、周日 17:00–20:30。**周一、周二休。**

---

### 4. Exhibition — 全城 Google 分最高的正餐

**菜系：** 现代澳菜 omakase，CBD 地下室，24 座。**Google／Wanderlog 4.9／397**（本次扫查最高分）。

**故事／定位：** 不出菜单，按当日「活海鲜、标杆级肉类、昆士兰生物动力与可持续农场的时令物产」排菜，最多可到 15 道。这是**食材主导**而不是主厨签名菜主导的一家。

**官网价（最硬的一条）：**
- 2026-10-01 起：平日 **$255/人**，周末 **$335/人**（含 $80 餐饮额度）；此前为 $250／$330。
- 酒水配对五档：无酒精 $90–95、Unorthodox $120–125、Koji $150、Discovery $150、Premium $330–340。
- **两人平日不配酒约 $510，配 Koji 约 $810。**

---

### 5. Joy — 10 个位子，老板就是主厨

**菜系：** 时令品尝菜单。**Google／Wanderlog 4.7／215**（评论数刚过闸门）。地址 Shop 7, 694 Ann St（Bakery Lane），仅接受预约。

**故事：** 全店**只有 10 个座位，每晚两轮**，吧台一条，主厨兼老板 **Sarah Baldwin** 亲自掌勺。两件先知道的事：**提前三个月放位，基本秒光**；网上把 Tim Scott 当现任主厨的资料已经过时——店方公开澄清「Tim Scott 已经离开三年半，Sarah Baldwin 才是我的名字」。转述旧攻略前注意这条。

**官网价：$220/人**，并写明随市价与菜单变动。官网还明确：**一人厨房、空间有限，无法做全素、纯素、无麸质、无海鲜或无乳制品**，只能提供低麸质和部分鱼素替代，且必须在订位时写明由他们回邮确认。

---

### 6. Longwang — 名字是龙王，藏在 Edward Street

**菜系：** 现代泛亚。**Google／Wanderlog 4.8／2,118。** 144 Edward St。

**故事：** 店名取自**龙王**——掌管雨水与一切水域的中国水神。这是 Tassis Group（第二代餐饮人 Michael Tassis）2024 年开的第一家现代亚洲菜，行政主厨兼合伙人 Jason Margaritis 此前分别执掌过 **sAme sAme** 和 **Donna Chang** 的厨房——**这家把布里斯班两家最知名泛亚餐厅的厨房经验合在了一处。**

**官网三套 banquet（最少 2 人，整桌同点）：**
- **Jade $88/人**：龙王面包片（XO 菌菇韭花）、吞拿鱼配樱桃番茄 nahm jim、猪腩青木瓜沙拉、牛肉水饺配牛骨汤辣油、酥炸鱿鱼、**宫保 bug 尾**（朝天椒＋花椒＋麻辣汁＋腰果）、茶熏鸭胸、避风塘炒饭、巧克力 delice。
- **Dragon's $122/人**：面包片、nam jim 生蚝、吞拿鱼、炸猪肉鲜虾云吞、牛他他、龙王鸡包、**南极犬牙鱼 150g**（白酱油＋姜＋日本威士忌）、**MB5+ 纯血安格斯西冷 250g**、黑醋炒时蔬、米饭、芝麻费南雪。
- **Claw Feast $149/人**（每日限量售完即止）：面包片、红 nam jim 生蚝、牛肉水饺、炸云吞、**整只活昆士兰泥蟹（新加坡辣椒蟹做法）**、**和牛臀盖 MB8-9 250g**、时蔬、米饭、香茅焦糖布丁。
- 加菜：nam jim 生蚝 $7/人、龙王鸡包 $10/人、炸云吞 $5/人。
- **周末 +10%，公共假日 +20%**（全表最高的假日加价）。

---

### 7. 1889 Enoteca — 把 Trastevere 搬进 Woolloongabba

**菜系：** 罗马菜＋意大利自然酒。**Google／Wanderlog 4.7／2,341。**

**故事：** 开在 1889 年的 Moreton Rubber Works 历史建筑里（10–12 Logan Rd，Woolloongabba 的古董街区），按罗马 enoteche（酒馆）的形制做。店方自述：**「我们大概是 Woolloongabba 里的一小块 Trastevere。」**

**官方点单页价（取餐口径，堂食可能略有不同）：**
- **Cacio e Pepe $25**（两年陈 Pecorino Romano DOP ＋黑胡椒，罗马经典）｜**Carbonara $27**（guanciale＋蛋＋Parmigiano，原版做法）｜Bucatini all'Amatriciana $32｜手工 Gnocchi $32（猪肉茴香肠＋帕玛森奶油＋黑松露）｜蟹肉 Tagliatelle $38｜松露菌菇 Risotto $35
- 前菜：**Fiori di Zucca $21**（马苏里拉与凤尾鱼酿西葫芦花）｜Vitello Tonnato $24｜Burrata alla Panzanella $26｜生蚝半打 $32｜Antipasti 双人拼盘 $35｜**Carciofo alla Giudia（犹太区炸朝鲜蓟）核查当日显示售罄**
- 主菜：Saltimbocca alla Romana $39｜市场鱼 $45｜Tagliata（Cape Grim 西冷）$50｜**Moreton Bay bugs 500g $60**｜**Bistecca 1kg Cape Grim T 骨 $100**（需提前 40 分钟）
- 甜点 $15；配菜 $6–9
- 营业：周二至周四 17:30–21:00；周五六 12:00–14:30 及 17:30–21:30；周日 12:00–14:30 及 17:30–21:00

---

### 8. Rothwell's — 布里斯班最像「老派 grill」的一间（但菜单没拿到）

**菜系：** 经典 grill。**Google／Wanderlog 4.7／1,048。** 235 Edward St。

**故事：** 开在 Edward Street 一栋 1885 年的历史保护建筑底层，店名来自当年拥有这栋楼的裁缝 **Thomas James Rothwell**；概念对标伦敦 Savoy Grill 和洛杉矶 Musso & Frank Grill。90 座空间的中心是一条白色意大利大理石 **Marble Bar**，穿白外套的厨师在那里开生蚝，**托盘是在伦敦专门为它手工定制的银盘**。招牌是 **Beef Wellington**。

**价格：未查到。** 官网 Dining 页挂着「Dining Menu（2026-03 版）」的下载链接，**实测该 PDF 返回 404**；酒单标的是 2025-10 版。**这家必须打电话或到店问价。** 营业 周二至周六。

---

## 七、未过闸门、但你仍然会看到它们被推荐（附为什么）

**这一段的意义：不是把它们抹掉，而是标清楚「它们没过我们自己的闸门」。**

| 店 | 菜系 | Google／Wanderlog | 价格 | 怎么看待 |
|---|---|---|---|---|
| **Agnes** | 全柴火烧烤 | 4.6／1,360 | 套餐 **$89 / $139 每位**（官网）；单点主菜 $38–380 | 全店**没有燃气灶、没有常规烤箱**，只有木柴、炭与明火。评分 4.6 只差一点但样本量大，**「闸门边缘、名气极大」的典型**。菜单顶端那道 **9+ Kiwami 和牛短腰脊 $380** 是全城本次扫查里最贵的单道菜 |
| **sAme sAme** | 泰菜 | 4.5／1,868 | Banquet **$89 / $130 每位**（官网）；咖喱 $38–69 | 与 Agnes、hôntô 同属 Anyday 集团；主厨 Arté Assavakavinvong。**$130 那档里有蟹肉 lon、鸭胸、姜黄咖喱虾** |
| **GRECA** | 希腊／地中海 | 4.6／3,342 | 单点 $9–240（官网）：**整条炭烤珊瑚鳟 1.1kg $240**、半条 $120、烤羊肩大份 $118 | Howard Smith Wharves 河边，景观是主要卖点。周日 +10%，公假 +15%，**8 人以上另加 7% 服务费** |
| **Julius Pizzeria** | 那不勒斯披萨 | 4.6／3,985 | 未查到 | Fish Lane，炉子是从那不勒斯运来的 Stefano Ferrara 定制柴窑 |
| **Pawpaw Cafe** | Brunch | 4.6／3,459 | 三道晚餐 $48/人（第三方） | Woolloongabba，早午餐里样本量最大 |
| **e'cco bistro** | 现代澳菜 | 4.6／686 | 三道 $79/人；5 道／4 道 $120／$105（第三方） | 布里斯班老牌帽子餐厅，已迁至 Newstead |
| **Libertine** | 法越 | 4.6／833 | 未查到 | Petrie Terrace |
| **Andonis Cafe & Bar** | Cafe/Bar | 4.6／3,283 | 未查到 | Fortitude Valley |
| **Yoko Dining** | 日式居酒屋 | 4.5／1,946 | 套餐 $60/人（第三方） | CBD |
| **Chu The Phat** | 港/韩/台 | 4.5／3,410 | 未查到 | South Brisbane |
| **Essa** | 现代澳菜 | 4.5／425 | 未查到 | Fortitude Valley |
| **Biànca** | 意大利 | 4.5／1,062 | 未查到 | Howard Smith Wharves |
| **Gerard's Bistro** | 中东／北非 | 4.5／1,183 | 未查到 | James St |
| **Donna Chang** | 粤菜／川菜 | 4.4／1,816 | 未查到 | CBD 老银行大楼，空间是最大看点 |
| **Happy Boy** | 粤式烧腊＋港式镬气 | 4.4／1,493 | Banquet $50/人（**第三方，按本轮经验应视为下限**） | East St；本表里名义上最便宜的 banquet |
| **SK Steak & Oyster** | 牛排／生蚝 | 4.4／650–708 | 未查到 | The Calile 酒店内 |
| **Stanley** | 粤菜 | 4.3／1,389 | 未查到 | Howard Smith Wharves |
| **Hellenika** | 希腊 | 4.2／1,398 | 未查到 | The Calile 酒店内 |
| **OTTO Ristorante** | 意大利 | 4.2／1,456 | 未查到 | 河景（Story Bridge 方向） |
| **TakashiYa** | 日本 omakase | 未查到 | 约 20 道 $280/人（第三方） | South Brisbane，本次扫查里最贵的品尝菜单 |
| **The Golden Pig** | 现代澳菜 | 未查到 | 9 道 $74/人（第三方） | Newstead，带烹饪学校 |
| **Tartufo** | 意大利 | 未查到 | 6 道 $95/人（第三方） | Fortitude Valley |
| **Bacchus** | 现代澳菜 | 4.5／686 | 7 道 $140/人（第三方） | South Brisbane |

**状态存疑，去之前务必确认：**
- **Restaurant Dan Arnold**（4.4／583）与 **Gum Bistro**（4.8／113）在 Wanderlog 上被标为 **Closed**；Gum Bistro 即便营业，评论数 113 也**不过闸门**。
- Rogue Bistro 5 道 $120、Perspective Dining 9 道 $195、Attimi by Dario Manca $198／$148、Deer Duck Bistro $105–165、C'est Bon 6 道 $90、Pneuma 6 道 $125、Da Biuso $180／$150 —— 价格来自第三方盘点，**Google 评分本次未逐条核到，不进任何一表**。

---

## 八、平价档（人均 $20–40）——另一套明确标注的闸门

主闸门（Google ≥4.7 且 ≥200）在这个价位段会把几乎所有店删掉，所以这里**另开一套口径，并写明它是另一套**：

> **平价档闸门：Google ≥4.5 且评论 ≥1,000，且 Google 众报人均在 $20–40。**
> 评分门槛下调 0.2，**样本量门槛从 200 提到 1,000 作为补偿**——宁可要「很多人打 4.5」，不要「少数人打 4.8」。
> 价位带取自 Google Maps 的「$X–Y per person · reported by N people」众报数据，**和评分一样标平台、绝不与菜单实价混为一谈**。

| # | 店 | 菜系 | Google（实时） | Google 众报人均 | 地址 |
|---|---|---|---|---|---|
| B1 | **Julius Pizzeria** | 那不勒斯披萨 | 4.6／**4,009** | $20–40 | [77 Grey St, South Brisbane（Fish Lane）](https://www.google.com/maps/search/?api=1&query=Julius%20Pizzeria%2077%20Grey%20St%2C%20South%20Brisbane%20QLD%204101) |
| B2 | **Pawpaw Cafe** | 早午餐／东南亚 | 4.6／**3,470** | $20–40 | [898 Stanley St E, Woolloongabba](https://www.google.com/maps/search/?api=1&query=Pawpaw%20Cafe%20898%20Stanley%20St%20E%2C%20Woolloongabba%20QLD%204102) |
| B3 | **Andonis Cafe & Bar** | 咖啡馆／全日 | **4.5**／3,313 | $20–40 | [28/32 Robertson St, Fortitude Valley](https://www.google.com/maps/search/?api=1&query=Andonis%20Cafe%20%26%20Bar%2028/32%20Robertson%20St%2C%20Fortitude%20Valley%20QLD%204006) |
| B4 | **Harajuku Gyoza** | 日式煎饺／居酒屋 | 4.5／2,237 | $20–40 | [141 Queen St, CBD（Albert Lane）](https://www.google.com/maps/search/?api=1&query=Harajuku%20Gyoza%20141%20Queen%20St%2C%20Brisbane%20City%20QLD%204000) |
| B5 | **Cafe O-Mai** | 越南／咖啡馆 | 4.5／1,882 | $20–40 | [15 Cracknell Rd, Annerley](https://www.google.com/maps/search/?api=1&query=Cafe%20O-Mai%2015%20Cracknell%20Rd%2C%20Annerley%20QLD%204103) |
| B6 | **remy's** | 汉堡／早午餐 | 4.5／1,326 | $20–40 | [106 Latrobe Tce, Paddington](https://www.google.com/maps/search/?api=1&query=remy%27s%20106%20Latrobe%20Tce%2C%20Paddington%20QLD%204064) |
| B7 | **Ben's Burgers** | 汉堡 | 4.5／1,283 | $20–40 | [5 Winn St, Fortitude Valley](https://www.google.com/maps/search/?api=1&query=Ben%27s%20Burgers%205%20Winn%20St%2C%20Fortitude%20Valley%20QLD%204006) |
| B8 | **Sushi Kotobuki** | 寿司 | 4.6／1,042 | $20–40 | [3/53 Lytton Rd, East Brisbane](https://www.google.com/maps/search/?api=1&query=Sushi%20Kotobuki%203/53%20Lytton%20Rd%2C%20East%20Brisbane%20QLD%204169) |
| B9 | **Eat Street Northshore** | 夜市（80 个货柜摊） | 4.6／**15,638** | 未显示（另收入场费） | [221D MacArthur Ave, Hamilton](https://www.google.com/maps/search/?api=1&query=Eat%20Street%20Northshore%20221D%20MacArthur%20Ave%2C%20Hamilton%20QLD%204007) |

完整的五档价位名单（每家都带 Google 地图链接）见第九节「价位阶梯」。

**这一档里最该先去的三家**（评分×样本量同时最好）：**B1 Julius（4.6／4,009）、B2 Pawpaw（4.6／3,470）、B8 Sushi Kotobuki（4.6／1,042）**。

**B9 Eat Street 的 15,638 条是全城最大样本**，但它是夜市不是餐厅：**只在特定夜晚开，且要另买入场票**——出发前必须查当期开放日与票价，别按餐厅的思路排进行程。

**⚠️ B3 Andonis 刚掉档**：Wanderlog 镜像仍是 4.6，Google 实时已经是 **4.5**。它现在踩在这张表的下边缘。

### 同样便宜、但评分更高的三家已经在主表里

**22 Vegeme（4.7／1,001，$1–20）**、**19 John Mills Himself（4.8／1,120，$1–20）**、**20 Hashtag Burgers（4.7／2,154，$20–40）**——它们过的是**主闸门**，不必降标准。**想省钱又不想降要求，先看这三家。**

### 价位更高、不进任一表的（记录备查）

| 店 | Google（实时） | Google 众报人均 |
|---|---|---|
| Chu The Phat | 4.5／3,477 | **$40–80** |
| Bird's Nest（West End） | 4.5／1,736 | **$40–60** |
| Southside Restaurant | 4.5／1,268 | **$60–140** |
| Madame Wu | 4.5／2,385 | **$80–160** |

### 主表各家的 Google 众报价位（方便横向比价）

Rothwell's **$80–200** · Longtime Dining **$40–120** · Hashtag Burgers **$20–40** · Ngon **$20–40** · John Mills Himself **$1–20** · Vegeme **$1–20**。
其余各家本轮以**官网菜单实价**为准（见第四节），不再引用众报价位——**两者不能混着用**。

---

## 九、价位阶梯 · 五档 50 条

价位有两种来源，**分开标、不混用**：「官网」＝商家菜单实价；「Google 众报」＝Google Maps 的 「$X–Y per person · reported by N people」；「评论照片」＝Google 评论里的实体菜单照片。每家店名都链到 Google 地图。**★ ＝过了主闸门（Google ≥4.7 且 ≥200）**。

### $1–20 · 口袋档

咖啡、素食、快食。**前四家都过了主闸门（Google ≥4.7 且 ≥200）——最便宜的一档反而不用降标准。**

| 店 | 菜系 | Google | 价格 | 来源 | 备注 |
|---|---|---|---|---|---|
| [**John Mills Himself**](https://www.google.com/maps/search/?api=1&query=John%20Mills%20Himself%2040%20Charlotte%20St%2C%20Brisbane%20City%20QLD%204000)<br>40 Charlotte St, Brisbane City QLD 4000 | 咖啡／小酒吧 | **4.8**／1,120 | $1–20 | Google 众报 | CBD 老砖巷里的小店，白天咖啡晚上酒 |
| [**Vegeme**](https://www.google.com/maps/search/?api=1&query=Vegeme%20Shop%209/220%20Melbourne%20St%2C%20South%20Brisbane%20QLD%204101)<br>Shop 9/220 Melbourne St, South Brisbane QLD 4101 | 素食／越南素 | **4.7**／1,001 | $1–20 | Google 众报 | South Brisbane，全城最便宜的过闸门正餐 |
| [**Death Before Decaf**](https://www.google.com/maps/search/?api=1&query=Death%20Before%20Decaf%203/760-766%20Brunswick%20St%2C%20New%20Farm%20QLD%204005)<br>3/760-766 Brunswick St, New Farm QLD 4005 | 咖啡（24 小时） | **4.7**／1,571 | $1–20 | Google 众报 | New Farm，本档样本量最大 |
| [**Bunker Coffee**](https://www.google.com/maps/search/?api=1&query=Bunker%20Coffee%2021%20Railway%20Ter%2C%20Milton%20QLD%204064)<br>21 Railway Ter, Milton QLD 4064 | 咖啡 | **4.7**／721 | $1–20 | Google 众报 | Milton，铁路旁 |
| [**Vege Rama**](https://www.google.com/maps/search/?api=1&query=Vege%20Rama%20Shop%201/241%20Adelaide%20St%2C%20Brisbane%20City%20QLD%204000)<br>Shop 1/241 Adelaide St, Brisbane City QLD 4000 | 素食／纯素 | **4.6**／646 | $1–20 | Google 众报 | ANZAC Square 地下，午市快食；**4.6 未过主闸门** |

### $20–40 · 平价档

本档用**另一套明确标注的闸门**：Google ≥4.5 且 ≥1,000 条（评分降 0.2，样本量从 200 提到 1,000 作补偿）。带 ★ 的是过了主闸门、不必降标准的。

| 店 | 菜系 | Google | 价格 | 来源 | 备注 |
|---|---|---|---|---|---|
| [**Hashtag Burgers and Waffles**](https://www.google.com/maps/search/?api=1&query=Hashtag%20Burgers%20and%20Waffles%20Shop%203/477%20Brunswick%20St%2C%20Fortitude%20Valley%20QLD%204006) ★<br>Shop 3/477 Brunswick St, Fortitude Valley QLD 4006 | 汉堡／华夫 | **4.7**／2,154 | 汉堡 $15.5–35 · loaded fries $19–23 · 奶昔 $10 | 评论照片 | 过主闸门 |
| [**Ngon Brisbane**](https://www.google.com/maps/search/?api=1&query=Ngon%20Brisbane%20183%20Given%20Tce%2C%20Paddington%20QLD%204064) ★<br>183 Given Tce, Paddington QLD 4064 | 越南 | **4.7**／648 | 小盘 $16–18 · 大盘 $26–32 · 汤面 $24 | 官网 | 过主闸门；姜汁焦糖鸭 $32 |
| [**Little Black Pug**](https://www.google.com/maps/search/?api=1&query=Little%20Black%20Pug%20Logan%20Rd%2C%20Mount%20Gravatt%20Central%20QLD%204122) ★<br>Logan Rd, Mount Gravatt Central QLD 4122 | Brunch | **4.8**／1,663 | $9–31 | 官网 | 过主闸门；Dog's Breakfast $31 |
| [**Unbearable Bagels**](https://www.google.com/maps/search/?api=1&query=Unbearable%20Bagels%2039%20Vernon%20Tce%2C%20Teneriffe%20QLD%204005) ★<br>39 Vernon Tce, Teneriffe QLD 4005 | 贝果 | **4.7**／333 | 贝果 $17–20 · 抹酱 $6–13 | 官网 | 过主闸门 |
| [**Farm House, Kedron**](https://www.google.com/maps/search/?api=1&query=Farm%20House%2C%20Kedron%209%20Somerset%20Rd%2C%20Kedron%20QLD%204031) ★<br>9 Somerset Rd, Kedron QLD 4031 | 全日咖啡馆 | **4.7**／2,981 | $25.5–28.5 | 官网 | 过主闸门 |
| [**Smoked Paprika**](https://www.google.com/maps/search/?api=1&query=Smoked%20Paprika%202/5%20Nash%20St%2C%20Paddington%20QLD%204064) ★<br>2/5 Nash St, Paddington QLD 4064 | 匈牙利早餐 | **4.7**／924 | 早餐 $13.9–29.9 · 午餐 $16.9–27.9 | 官网 | 过主闸门 |
| [**NAÏM**](https://www.google.com/maps/search/?api=1&query=NA%C3%8FM%2014%20Collingwood%20St%2C%20Paddington%20QLD%204064) ★<br>14 Collingwood St, Paddington QLD 4064 | 中东 | **4.7**／1,849 | 早午餐 $14–29 | 官网 | 过主闸门；晚餐 banquet 未上价 |
| [**Julius Pizzeria**](https://www.google.com/maps/search/?api=1&query=Julius%20Pizzeria%2077%20Grey%20St%2C%20South%20Brisbane%20QLD%204101)<br>77 Grey St, South Brisbane QLD 4101 | 那不勒斯披萨 | **4.6**／4,009 | $20–40 | Google 众报 | 本档样本量最大 |
| [**Pawpaw Cafe**](https://www.google.com/maps/search/?api=1&query=Pawpaw%20Cafe%20898%20Stanley%20St%20E%2C%20Woolloongabba%20QLD%204102)<br>898 Stanley St E, Woolloongabba QLD 4102 | 早午餐／东南亚 | **4.6**／3,470 | $20–40 | Google 众报 |  |
| [**Sushi Kotobuki**](https://www.google.com/maps/search/?api=1&query=Sushi%20Kotobuki%203/53%20Lytton%20Rd%2C%20East%20Brisbane%20QLD%204169)<br>3/53 Lytton Rd, East Brisbane QLD 4169 | 寿司 | **4.6**／1,042 | $20–40 | Google 众报 | East Brisbane |
| [**Andonis Cafe & Bar**](https://www.google.com/maps/search/?api=1&query=Andonis%20Cafe%20%26%20Bar%2028/32%20Robertson%20St%2C%20Fortitude%20Valley%20QLD%204006)<br>28/32 Robertson St, Fortitude Valley QLD 4006 | 咖啡馆／全日 | **4.5**／3,313 | $20–40 | Google 众报 | ⚠️ 镜像还是 4.6，实时已掉到 4.5 |
| [**Harajuku Gyoza**](https://www.google.com/maps/search/?api=1&query=Harajuku%20Gyoza%20141%20Queen%20St%2C%20Brisbane%20City%20QLD%204000)<br>141 Queen St, Brisbane City QLD 4000 | 日式煎饺 | **4.5**／2,237 | $20–40 | Google 众报 | CBD Albert Lane |
| [**Cafe O-Mai**](https://www.google.com/maps/search/?api=1&query=Cafe%20O-Mai%2015%20Cracknell%20Rd%2C%20Annerley%20QLD%204103)<br>15 Cracknell Rd, Annerley QLD 4103 | 越南／咖啡馆 | **4.5**／1,882 | $20–40 | Google 众报 | Annerley，要专程开车 |
| [**remy's**](https://www.google.com/maps/search/?api=1&query=remy%27s%20106%20Latrobe%20Tce%2C%20Paddington%20QLD%204064)<br>106 Latrobe Tce, Paddington QLD 4064 | 汉堡／早午餐 | **4.5**／1,326 | $20–40 | Google 众报 | Paddington |
| [**Ben's Burgers**](https://www.google.com/maps/search/?api=1&query=Ben%27s%20Burgers%205%20Winn%20St%2C%20Fortitude%20Valley%20QLD%204006)<br>5 Winn St, Fortitude Valley QLD 4006 | 汉堡 | **4.5**／1,283 | $20–40 | Google 众报 | Fortitude Valley |
| [**Eat Street Northshore**](https://www.google.com/maps/search/?api=1&query=Eat%20Street%20Northshore%20221D%20MacArthur%20Ave%2C%20Hamilton%20QLD%204007)<br>221D MacArthur Ave, Hamilton QLD 4007 | 夜市（80 个货柜摊） | **4.6**／15,638 | 另收入场费 | Google 众报 | **全城最大样本**，但只在特定夜晚开，要另买票 |

### $40–80 · 中档

一顿正经晚餐、但不到「纪念日」的价位。这一档里官网套餐价最透明。

| 店 | 菜系 | Google | 价格 | 来源 | 备注 |
|---|---|---|---|---|---|
| [**Short Grain**](https://www.google.com/maps/search/?api=1&query=Short%20Grain%2015%20Marshall%20St%2C%20Fortitude%20Valley%20QLD%204006) ★<br>15 Marshall St, Fortitude Valley QLD 4006 | 泰菜 | **4.8**／606 | 套餐 $55／$85／$125 · 咖喱 $55–75 | 官网 | 过主闸门；周日 +10% |
| [**Oh Boy, Bok Choy!**](https://www.google.com/maps/search/?api=1&query=Oh%20Boy%2C%20Bok%20Choy%21%20264%20Stafford%20Rd%2C%20Stafford%20QLD%204053) ★<br>264 Stafford Rd, Stafford QLD 4053 | 东南亚 | **4.8**／1,991 | banquet $62.5 · 周末长午餐 $89（含 2 小时酒水） | 官网 | 过主闸门 |
| [**1889 Enoteca**](https://www.google.com/maps/search/?api=1&query=1889%20Enoteca%2010-12%20Logan%20Rd%2C%20Woolloongabba%20QLD%204102) ★<br>10-12 Logan Rd, Woolloongabba QLD 4102 | 罗马菜 | **4.7**／2,341 | 意面 $25–38 · 主菜 $39–100 | 官网 | 过主闸门；cacio e pepe $25 |
| [**Beccofino**](https://www.google.com/maps/search/?api=1&query=Beccofino%2010%20Vernon%20Tce%2C%20Teneriffe%20QLD%204005) ★<br>10 Vernon Tce, Teneriffe QLD 4005 | 意式柴烧披萨 | **4.7**／1,220 | 披萨 $28.5–36.5 · 意面 $35–39.5 | 官网 | 过主闸门 |
| [**Longtime Dining**](https://www.google.com/maps/search/?api=1&query=Longtime%20Dining%20L1%2C%20226%20Queen%20St%2C%20Brisbane%20City%20QLD%204000) ★<br>L1, 226 Queen St, Brisbane City QLD 4000 | 精致粤菜／点心 | **4.8**／4,821 | $40–120（众报）· 点心 $15–47（照片） | 评论照片 | 过主闸门；朗廷八寶 $47 |
| [**Chu The Phat**](https://www.google.com/maps/search/?api=1&query=Chu%20The%20Phat%20111%20Melbourne%20St%2C%20South%20Brisbane%20QLD%204101)<br>111 Melbourne St, South Brisbane QLD 4101 | 港／韩／台 | **4.5**／3,477 | $40–80 | Google 众报 | 未过主闸门 |
| [**Bird's Nest**](https://www.google.com/maps/search/?api=1&query=Bird%27s%20Nest%202%20Edmondstone%20St%2C%20South%20Brisbane%20QLD%204101)<br>2 Edmondstone St, South Brisbane QLD 4101 | 日式串烧 | **4.5**／1,736 | $40–60 | Google 众报 | 未过主闸门 |
| [**Happy Boy**](https://www.google.com/maps/search/?api=1&query=Happy%20Boy%20East%20St%2C%20Fortitude%20Valley%20QLD%204006)<br>East St, Fortitude Valley QLD 4006 | 粤式烧腊 | **4.4**／1,498 | $20–80（众报）· banquet $50（第三方） | Google 众报 | 未过主闸门 |
| [**El Camino Cantina**](https://www.google.com/maps/search/?api=1&query=El%20Camino%20Cantina%20153%20Stanley%20St%2C%20South%20Brisbane%20QLD%204101)<br>153 Stanley St, South Brisbane QLD 4101 | 墨西哥 | **4.5**／5,548 | $20–100 | Google 众报 | 未过主闸门，但样本量极大 |

### $60–160 · 高档

河景、酒店、大型宴席都在这一档。**注意：这一档里过主闸门的只有 5 家。**

| 店 | 菜系 | Google | 价格 | 来源 | 备注 |
|---|---|---|---|---|---|
| [**The Fifty Six**](https://www.google.com/maps/search/?api=1&query=The%20Fifty%20Six%20Level%202/33%20Felix%20St%2C%20Brisbane%20City%20QLD%204000) ★<br>Level 2/33 Felix St, Brisbane City QLD 4000 | 现代粤菜 | **4.7**／207 | Short Set $82 · Long Set $120（配酒 +$80／+$118） | 官网 | 过主闸门 |
| [**Longwang**](https://www.google.com/maps/search/?api=1&query=Longwang%20144%20Edward%20St%2C%20Brisbane%20City%20QLD%204000) ★<br>144 Edward St, Brisbane City QLD 4000 | 现代泛亚 | **4.8**／2,118 | Jade $88 · Dragon's $122 · Claw Feast $149 | 官网 | 过主闸门；公假 +20% |
| [**hôntô**](https://www.google.com/maps/search/?api=1&query=h%C3%B4nt%C3%B4%20Alden%20St%2C%20Fortitude%20Valley%20QLD%204006) ★<br>Alden St, Fortitude Valley QLD 4006 | 现代日料 | **4.7**／1,603 | banquet $89／$130 · 单点 $6–110 | 官网 | 过主闸门 |
| [**Montrachet**](https://www.google.com/maps/search/?api=1&query=Montrachet%201/30%20King%20St%2C%20Bowen%20Hills%20QLD%204006) ★<br>1/30 King St, Bowen Hills QLD 4006 | 法餐 | **4.7**／890 | 前菜 $26–33 · 主菜 $46–82 | 官网 | 过主闸门 |
| [**Sono Japanese Portside**](https://www.google.com/maps/search/?api=1&query=Sono%20Japanese%20Portside%2039%20Hercules%20St%2C%20Hamilton%20QLD%204007) ★<br>39 Hercules St, Hamilton QLD 4007 | 日料 | **4.7**／2,388 | 未查到 | 未查到 | 过主闸门；AGFG 12 分 |
| [**Agnes**](https://www.google.com/maps/search/?api=1&query=Agnes%2022%20Agnes%20St%2C%20Fortitude%20Valley%20QLD%204006)<br>22 Agnes St, Fortitude Valley QLD 4006 | 全柴火烧烤 | **4.6**／1,376 | 套餐 $89／$139 · 单点主菜 $38–380 | 官网 | 未过主闸门；AGFG 14 分、GT 收录 |
| [**GRECA**](https://www.google.com/maps/search/?api=1&query=GRECA%203/5%20Boundary%20St%2C%20Brisbane%20City%20QLD%204000)<br>3/5 Boundary St, Brisbane City QLD 4000 | 希腊 | **4.6**／3,353 | $60–140（众报）· 整条珊瑚鳟 $240 | Google 众报 | 未过主闸门；8 人以上 +7% 服务费 |
| [**Yoko Dining**](https://www.google.com/maps/search/?api=1&query=Yoko%20Dining%202/5%20Boundary%20St%2C%20Brisbane%20City%20QLD%204000)<br>2/5 Boundary St, Brisbane City QLD 4000 | 日式居酒屋 | **4.5**／1,954 | $60–140 | Google 众报 | 未过主闸门 |
| [**Southside Restaurant**](https://www.google.com/maps/search/?api=1&query=Southside%20Restaurant%2063%20Melbourne%20St%2C%20South%20Brisbane%20QLD%204101)<br>63 Melbourne St, South Brisbane QLD 4101 | 亚洲 tapas | **4.5**／1,268 | $60–140 | Google 众报 | 未过主闸门 |
| [**Hellenika**](https://www.google.com/maps/search/?api=1&query=Hellenika%20Level%201/48%20James%20St%2C%20Fortitude%20Valley%20QLD%204006)<br>Level 1/48 James St, Fortitude Valley QLD 4006 | 希腊 | **4.2**／1,416 | $60–160 | Google 众报 | 未过主闸门；The Calile 酒店内 |
| [**Donna Chang**](https://www.google.com/maps/search/?api=1&query=Donna%20Chang%20Suite%203/171%20George%20St%2C%20Brisbane%20City%20QLD%204000)<br>Suite 3/171 George St, Brisbane City QLD 4000 | 粤菜／川菜 | **4.4**／1,830 | $40–160 | Google 众报 | 未过主闸门；老银行大楼 |
| [**Madame Wu**](https://www.google.com/maps/search/?api=1&query=Madame%20Wu%20Upper%20Plaza%20Level%2C%2071%20Eagle%20St%2C%20Brisbane%20City%20QLD%204000)<br>Upper Plaza Level, 71 Eagle St, Brisbane City QLD 4000 | 泛亚 | **4.5**／2,385 | $80–160 | Google 众报 | 未过主闸门 |
| [**Supernormal Brisbane**](https://www.google.com/maps/search/?api=1&query=Supernormal%20Brisbane%20443%20Queen%20St%2C%20Brisbane%20City%20QLD%204000)<br>443 Queen St, Brisbane City QLD 4000 | 现代亚洲 | **4.5**／468 | $80–180 | Google 众报 | 未过主闸门；GT 2026 收录 |
| [**OTTO Ristorante**](https://www.google.com/maps/search/?api=1&query=OTTO%20Ristorante%20River%20Quay%2C%20Shop%201%20Sidon%20St%2C%20South%20Brisbane%20QLD%204101)<br>River Quay, Shop 1 Sidon St, South Brisbane QLD 4101 | 意大利 | **4.2**／1,471 | $80–200 | Google 众报 | 未过主闸门；河景 |
| [**Rothwell's Bar & Grill**](https://www.google.com/maps/search/?api=1&query=Rothwell%27s%20Bar%20%26%20Grill%20235%20Edward%20St%2C%20Brisbane%20City%20QLD%204000) ★<br>235 Edward St, Brisbane City QLD 4000 | 老派 grill | **4.7**／1,067 | $80–200（众报）· Beef Wellington 600g $134（照片） | 评论照片 | 过主闸门 |

### $150+ · 顶级

品尝菜单与高端牛排。**三套评分口径同时点名的两家（Exhibition、Joy）都在这一档。**

| 店 | 菜系 | Google | 价格 | 来源 | 备注 |
|---|---|---|---|---|---|
| [**Exhibition**](https://www.google.com/maps/search/?api=1&query=Exhibition%20Basement%202/109%20Edward%20St%2C%20Brisbane%20City%20QLD%204000) ★<br>Basement 2/109 Edward St, Brisbane City QLD 4000 | 现代澳菜 omakase | **4.9**／397 | $255 平日／$335 周末 · 配对 $90–340 | 官网 | 主闸门第一 · AGFG 18 分 · GT 收录 |
| [**Joy**](https://www.google.com/maps/search/?api=1&query=Joy%20Shop%207%2C%20694%20Ann%20St%2C%20Fortitude%20Valley%20QLD%204006) ★<br>Shop 7, 694 Ann St, Fortitude Valley QLD 4006 | 10 座品尝菜单 | **4.7**／215 | $220 | 官网 | 过主闸门 · AGFG 17 分 · GT 收录 |
| [**SK Steak & Oyster**](https://www.google.com/maps/search/?api=1&query=SK%20Steak%20%26%20Oyster%20The%20Calile%20Hotel%2C%20G.12/48%20James%20St%2C%20Fortitude%20Valley%20QLD%204006)<br>The Calile Hotel, G.12/48 James St, Fortitude Valley QLD 4006 | 牛排／生蚝 | **4.4**／717 | $200+ | Google 众报 | 未过主闸门；The Calile 酒店内 |
| [**Longwang**](https://www.google.com/maps/search/?api=1&query=Longwang%20144%20Edward%20St%2C%20Brisbane%20City%20QLD%204000) ★<br>144 Edward St, Brisbane City QLD 4000 | 现代泛亚（Claw Feast） | **4.8**／2,118 | $149（整只活泥蟹＋和牛） | 官网 | 本档最便宜的「大菜」 |
| [**Agnes**](https://www.google.com/maps/search/?api=1&query=Agnes%2022%20Agnes%20St%2C%20Fortitude%20Valley%20QLD%204006)<br>22 Agnes St, Fortitude Valley QLD 4006 | 全柴火烧烤（长餐） | **4.6**／1,376 | $139 · 9+ Kiwami 和牛短腰脊 $380 | 官网 | 单道菜全城最贵 |

---

## 十、这条闸门在布里斯班暴露的两个问题（必须写下来）

**Sunnybank 一带的华人餐饮，在 Google 口径下几乎集体不过闸门。**

- Landmark Restaurant Sunnybank（布里斯班最知名的饮茶之一）：**Google／Wanderlog 仅 3.2／1,269**。
- 同一扫查里，New Shanghai（Queens Plaza）3.3／1,166、Leon 3.4／230、Ben's 3.7／591。

也就是说：**如果只用「Google ≥4.7 且 ≥200」，Sunnybank 会被整片删掉**，而这恰恰是布里斯班华人吃饭最密集的地方。这不是这些店不好吃，而是**这条闸门对以华人顾客为主、英文点评生态薄弱的餐馆有系统性偏差**。

**建议的处理（不改主闸门，另开一张表）：** 去 Sunnybank 时改用「同一商圈内相对排序＋中文点评（大众点评／小红书）交叉验证」，并把那张表**明确标注为另一套口径**，绝不和主表的 Google 分混排。本次未做这项扫查，**这是本文档已知的空白**。

同一逻辑下，主表里能代表中餐的只有 **Longtime Dining（4.8／4,749）**、**The Fifty Six（4.7／207）** 和泛亚的 **Longwang（4.8／2,118）**——三家都是 CBD 的现代中餐，**不能替代 Sunnybank 的家常与茶楼**。

**问题二：本轮想补的中文口径，没补成。**

原计划用大众点评做交叉验证，实测**跳转到滑块人机验证**。本仓库**不做验证码**，这条路直接终止；小红书同理未尝试；TripAdvisor 则对自动访问返回空白页。也就是说：

- 本文现在有 **Google（本项目打分）＋ AGFG（评审 20 分制）＋ Gourmet Traveller（匿名评论员）** 三套口径，
- 但**三套全部长在英文生态里**。Sunnybank 的缺口不但没补上，还被证明**用自动化手段补不上**——只能人工查中文点评，或到场判断。

这一条值得写进 METHOD：**「另一套口径」有时不是没想到，而是取不到；取不到就要在成果里标出来，不能装作那一格不存在。**

---

## 十一、按场景怎么挑（不构成行程，只给取舍）

| 场景 | 首选 | 两人预算（官网价，未含酒水加价） | 备选 |
|---|---|---|---|
| 只有一顿「必须记住」的晚餐 | **Exhibition** | **$510**（平日，不配酒） | Joy **$440**（需提前三个月） |
| 想吃中餐但不想去 Sunnybank | **The Fifty Six** Short Set | **$164** | Long Set $240；Longwang Jade $176 |
| 想吃到活蟹和和牛 | **Longwang** Claw Feast | **$298** | 含整只活昆士兰泥蟹 |
| 控制预算、两人吃好 | **Oh Boy, Bok Choy!** banquet | **$125** | hôntô $89 档 = $178 |
| 周末长午餐、想喝 | **Oh Boy** Bubbles & Bao | **$178**（含 2 小时酒水） | 周五至周日 12:00–15:00 |
| 泰菜一顿吃透 | **Short Grain** $85 套餐 | **$170** | sAme sAme $89 档 = $178 |
| 意面／披萨 | **1889 Enoteca**（cacio e pepe $25） | 约 **$90–130** | Beccofino 披萨 $28.5–36.5 |
| 早餐／咖啡 | **Unbearable Bagels**（$17–20/个） | 约 **$50** | Smoked Paprika $25.9 招牌早餐、Farm House $25.5–28.5 |
| 河景 / 拍照 | GRECA 或 Biànca | 按单点，珊瑚鳟整条 $240 | **都未过闸门**——选它们是为景，不是为分 |
| 离市区远但值得开车 | **Oh Boy, Bok Choy!**（Stafford） | $125 | Little Black Pug（Mount Gravatt）$9–31 |

**一条顺路的小发现：** **Farm House（Kedron，#7）和 Oh Boy, Bok Choy!（Stafford，#4）是同一对老板 Amanda & John Scott**。Farm House 2017 年 3 月开在老店「Farmer Joe's」原址上，两人的父亲分别来自昆士兰 Taroom 以西和美国密苏里小麦带的农场，店名由此而来；疫情期间的「lockdown specials」长成了 Oh Boy, Bok Choy!。两家直线距离约 2 公里，**早餐吃 Farm House、晚餐吃 Oh Boy 是同一趟车能完成的**。

---

## 十二、出发前复核清单

- [ ] **Exhibition**：确认当期价格（10/1 起 $255／$335）与配对档位；周末含 $80 餐饮额度的规则是否仍在。
- [ ] **Joy**：提前三个月开放订位，先确认放位日期再定行程日；订位时写清饮食限制并等他们回邮确认（他们**不做**全素／无麸质／无海鲜／无乳）。
- [ ] **Rothwell's**：官网菜单 PDF 链接 404，**必须电话或到店问价**。
- [ ] **Longtime Dining**：官网菜单页空白，**价格必须现场或电话确认**。
- [ ] **Naldham House（The Brasserie）**：无独立菜单页；若只想上顶层吃 The Fifty Six，直接按 The Fifty Six 的订位走。
- [ ] **加价一定要算进去**：Longwang 公假 **+20%**、Oh Boy／Farm House 公假 **+16.5%**、hôntô／Agnes／sAme sAme／Beccofino／Short Grain／GRECA 周末或周日 **+10%**、公假 **+15%**；GRECA 8 人以上另 **+7% 服务费**；多数店刷卡另收手续费。
- [ ] **hôntô**：入口是 Alden Street 上 Lounge Lovers 卸货口旁的黑门，**第一次去务必留 10 分钟找门**。
- [ ] **Short Grain 周一、周二休**；1889 Enoteca 周一休；Rothwell's 周二至周六；The Fifty Six 周二至周六。
- [ ] **Restaurant Dan Arnold、Gum Bistro**：出发前确认是否仍在营业。
- [ ] 所有 Google 评分取自 Wanderlog 镜像，**出发前用 Google Maps 实时值复核**，尤其是卡在边缘的 Joy（215）、The Fifty Six（207）、Unbearable Bagels（333）。

---

## 十三、俱乐部与会员价（另一套闸门）

**这是一类完全不同的餐饮。**持牌俱乐部（RSL／联赛／体育会）的 Google 分评的是**整个场馆**——博彩厅、酒吧、演出、宴会厅、儿童游乐区都算在内，**不是 bistro 的分**。用主闸门（≥4.7）会把这一整类删光：本次查到的 10 家全部落在 4.1–4.6。

> **本类闸门：Google ≥ 4.0 且评论 ≥ 500。**评分门槛大幅下调，但它只用来判断「这家俱乐部整体不烂」，**不能和餐厅横向比分**。真正该看的是每周特价表。

**一个更正：** Wynnum Manly Leagues Club **不是赌场**，是持牌联赛俱乐部，内设 gaming（老虎机）厅；布里斯班真正的赌场是 The Star Brisbane（Queen's Wharf）。澳洲俱乐部的低价餐食很大程度由博彩与酒水收入交叉补贴——这也是同样一份 250g 牛排在俱乐部 $19.90、在市区餐厅 $50+ 的原因。gaming 区域 18+。

| # | 俱乐部 | Google（实时） | 官网有没有写餐饮特价 | 会员费 |
|---|---|---|---|---|
| C1 | [**Easts Leagues Club**](https://www.google.com/maps/search/?api=1&query=Easts%20Leagues%20Club%2040%20Main%20Ave%2C%20Coorparoo%20QLD%204151)<br>40 Main Ave, Coorparoo QLD 4151 | **4.3**／2,227 | ✅ 四晚全套，且写明非会员差价 | 未标 |
| C2 | [**Wynnum Manly Leagues Club**](https://www.google.com/maps/search/?api=1&query=Wynnum%20Manly%20Leagues%20Club%2092%20Wondall%20Rd%2C%20Manly%20West%20QLD%204179)<br>92 Wondall Rd, Manly West QLD 4179 | **4.3**／1,080 | ✅ 六档＋每日会员午餐 $16 | 未标 |
| C3 | [**Kedron-Wavell**](https://www.google.com/maps/search/?api=1&query=Kedron-Wavell%2021%20Kittyhawk%20Dr%2C%20Chermside%20QLD%204032)<br>21 Kittyhawk Dr, Chermside QLD 4032 | **4.2**／2,690 | ⚠️ 只有月度主厨特价，标 Members 价 | 未标 |
| C4 | [**Carina Leagues Club**](https://www.google.com/maps/search/?api=1&query=Carina%20Leagues%20Club%201390%20Creek%20Rd%2C%20Carina%20QLD%204152)<br>1390 Creek Rd, Carina QLD 4152 | **4.2**／2,147 | ❌ 官网未列菜价特价 | $2 |
| C5 | [**Greenbank Services Club**](https://www.google.com/maps/search/?api=1&query=Greenbank%20Services%20Club%2054%20Anzac%20Ave%2C%20Hillcrest%20QLD%204118)<br>54 Anzac Ave, Hillcrest QLD 4118 | **4.2**／4,714 | ❌ 「餐饮促销」页全是抽奖 | $5 |
| C6 | [**Broncos Club**](https://www.google.com/maps/search/?api=1&query=Broncos%20Club%2098%20Fulcher%20Rd%2C%20Red%20Hill%20QLD%204059)<br>98 Fulcher Rd, Red Hill QLD 4059 | **4.1**／1,676 | ❌ 「促销」页全部是博彩抽奖，一条菜价都没有 | $2 |
| C7 | [**The Sunny（前 Sunnybank Community & Sports）**](https://www.google.com/maps/search/?api=1&query=The%20Sunny%20470%20McCullough%20St%2C%20MacGregor%20QLD%204109)<br>470 McCullough St, MacGregor QLD 4109 | **4.1**／932 | ⚠️ 网页只有图片轮播，文字价未取到 | 未标 |
| C8 | [**Souths Sports Club**](https://www.google.com/maps/search/?api=1&query=Souths%20Sports%20Club%20174%20Mortimer%20Rd%2C%20Acacia%20Ridge%20QLD%204110)<br>174 Mortimer Rd, Acacia Ridge QLD 4110 | **4.3**／418 | ❌ 未列；样本 418 条未过本类闸门 | 未标 |
| C9 | [**Wynnum R.S.L Club**](https://www.google.com/maps/search/?api=1&query=Wynnum%20R.S.L%20Club%20174%20Tingal%20Rd%2C%20Wynnum%20QLD%204178)<br>174 Tingal Rd, Wynnum QLD 4178 | **4.1**／521 | ❌ 未列 | 未标 |
| C10 | [**Manly Hotel （酒吧，非俱乐部）**](https://www.google.com/maps/search/?api=1&query=Manly%20Hotel%2054%20Cambridge%20Pde%2C%20Manly%20QLD%204179)<br>54 Cambridge Pde, Manly QLD 4179 | **4.6**／2,900 | ❌ 官网无每周特价 | 不适用 |

评分与地址取自 Google Maps 实时条目（核查 2026-09-29）。**俱乐部普遍不显示 Google 众报价位带**——这一类的价格只能从官网特价页取。

### Easts Leagues Club — 全城把特价写得最清楚的一家

The Brasserie · 午餐 12:00–14:00、晚餐 17:30–20:30（周五六到 21:00）· **非会员一律 +$3** · 公共假日特价可能停供。

| 星期 | 内容 | 会员价 |
|---|---|---:|
| **周一 牛排夜** | Nolan Private Selection **250g 臀腰肉排**＋薯条＋沙拉＋自选酱（加蒜香面包 +$2；加面包＋冰淇淋 +$5） | **$19.90** |
| **周二 披萨夜** | 2 个窑烤披萨＋混合沙拉 ／ 单个披萨（无麸质饼底 +$4） | **$35** ／ $17.50 |
| **周三 肋排夜** | 大份肋排＋薯条＋玉米＋凉拌 ／ 双人餐含酒水 | **$18.90** ／ $43.90 |
| **周四 Parmi 夜**（17:30–20:30） | 经典炸鸡排 ／ 鸡排帕尔马 ／ 墨西哥版或 BBQ 版，均配薯条与沙拉 | **$16.50** ／ $17.50 ／ $18.90 |

官网写着：「特价与菜品经常变动，来之前打 07 3397 8885 问当天有什么。」

### Wynnum Manly Leagues Club — 本地那家

The Grill · 午餐 11:30 起、晚餐 17:30 起 · **以下全部是会员价，官网未印非会员价**。

| 星期 | 内容 | 会员价 |
|---|---|---:|
| **周一 午餐** | 烤肉 | **$13**／两份 **$22** |
| **周一 晚餐** | **250g 安格斯西冷**＋薯条＋沙拉＋酱 | **$26** |
| 周二 | 鸡排帕尔马／炸鸡排／当周特色 parmi | $20 |
| 周三 | 羊腿配土豆泥、青豆与肉汁（加一根 +$10） | $25 |
| 周四 | Reef & Beef：200g 臀肉排＋蒜香虾 | $26 |
| 周日 | 烤肉（咸牛肉或当日烤肉） | $20 |
| **每天午市** | **会员午餐特价**，七天供应 | **$16**／份 |

官网明写「Offers are for members only, T&C's apply」。

### Kedron-Wavell — 月度主厨特价，只印会员价

The Kitchen（另有 Bravo Brewhouse、The Shack）· 全周 10:00–20:45，周五六宵夜到 21:45。

- Chef Karl 慢烤猪里脊，配焖甜菜叶、花椰菜饭、红酒汁 —— **会员 $33.9**
- Nutella 芝士蛋糕华夫碗 —— **会员 $18.9**
- Mr. Whippy 超级圣代（三款）—— **会员 $11.90**

这是**月度**特价（本次核查为 9 月档），不是固定的每周特价夜。

### 这一类的三条结论

1. **「Promotion」在俱乐部语境下有两种意思，完全不同。**一种是**餐饮特价**（牛排夜、parmi 夜），一种是**博彩抽奖**。Broncos 和 Greenbank 的「促销」页面**整页都是抽奖，一条菜价都没有**；Kedron-Wavell 的 Promotions 页同样如此，餐饮特价另挂在餐厅页上。**找吃的别看 Promotions，去看 Specials 或各餐厅页。**
2. **非会员差价非常小，会员费一顿就回本。**Easts 明写**非会员 +$3**；多数俱乐部只印会员价。会员费本次查到 **Broncos $2、Carina $2、Greenbank $5**。
3. **俱乐部的 Google 分不能和餐厅横向比。**4.1–4.3 在餐厅表里是不及格，在俱乐部里是正常水平——因为这个分包含博彩厅、宴会、演出和游乐区。**单列一节、单列一套闸门，就是为了不让这两组数字混排。**

### 就近（Wynnum–Manly 湾区）

**C2 Wynnum Manly Leagues** 就在本地。同区评分最高、样本最大的餐饮场所是 **C10 Manly Hotel（4.6／2,900）**——但它是酒吧不是俱乐部，**官网没有每周特价**，价格要到店问。**C9 Wynnum RSL（4.1／521）刚过本类闸门，官网未列特价。**

---

## 十四、华人菜系／饮品／海鲜／Pub（2026-09-29 补）与一条方法更正

### 方法更正：上一版关于 Sunnybank 的结论，错在候选池的语言

第十节写「Sunnybank 的华人餐饮在 Google 口径下几乎集体不过闸门」，依据是 Landmark 3.2、New Shanghai 3.3。**这个结论只对了一半，而且错的是方法。**

当时的候选池全部来自 Wanderlog 的英文 "best restaurants / best Chinese food" 榜单，这类榜单只会捞到几家老牌大茶楼。本轮改成**直接用中文关键词在 Google Maps 里按菜系搜**（火锅／川菜／湘菜／兰州拉面／麻辣烫／饮茶／珍珠奶茶），结果：

| 店 | Google 实时 |
|---|---|
| Mountain Hot Pot 蜀道山老火锅 | **4.9／590** |
| Miss 7 Noodle House 柒彩 | **4.8／802** |
| HAIDILAO 海底捞 | **4.8／1,551** |
| Orange Tea Sunnypark | **4.8／1,186** |
| 胖辣椒 市井湘菜 | **4.7／620** |
| Master Lanzhou 兰州拉面 | **4.7／548** |
| 食味 Luo's Place | **4.6／1,221** |

**偏差不在 Google 的评分，在我取候选池的语言。** 用中文搜，Google Maps 连分类都返回中文（火锅、川菜、珍珠奶茶）。

> **应写进 METHOD 的一条：闸门再严，也救不了一个选错语言的候选池。做多语言社区的餐饮时，候选池必须用该社区自己的语言各搜一轮。**

同一条街上的对照最能说明问题：Landmark 饮茶 **3.2／1,269**，而 Goodtime Bistro 的饮茶 **4.7／2,296**——「Sunnybank 饮茶分低」不是地域问题，是店的问题。

### 四套新增闸门（各自写明）

| 板块 | 闸门 | 放宽/收紧的理由 |
|---|---|---|
| 华人餐厅按菜系 | **Google ≥4.3 且 ≥150** | 顾客以华人为主，英文点评天然更少 |
| 奶茶饮品酸奶 | **Google ≥4.5 且 ≥200** | 饮品店评分普遍虚高、样本小，**评分门槛反而提高** |
| 海鲜市场鱼档 | **Google ≥4.2 且 ≥150** | 买生鲜不是吃正餐，评价维度不同；多数按重量卖，没有「人均」 |
| Pub 每周特价 | 不设评分闸门 | 这一档看的是价格不是分数（见下条发现） |

### 发现：Pub 的评分与特价强度基本反相关

- 特价最硬的两家：Manly Harbour Boat Club（周四 200g rump **$19.90**）**3.8／1,092**、Waterloo Bay Hotel（周一 parmi $21）**3.9／1,606**——湾区评分最低。
- 评分最高的 Manly Hotel **4.6／2,900**，**没有每周特价**（本轮核官网确认）。
- Gabba 方向同理：RedBrick **4.4／978** 分最高、人均带也最高（$40–60）；Woolloongabba Hotel **4.0／327** 分最低、特价最多。

**要便宜就别看分，要体验就别指望特价。**

### 数据来源分工

- **Pub 的菜价来自一份 2026 年的本地长期记录**（Manly／Wynnum 与往 Gabba 方向的 weekday night specials），本轮**沿用、未重新核价**；本轮补了 Google 实时评分，并核实 Manly Hotel 官网确实没有固定 weekday steak special。
- 华人菜系、饮品、海鲜三节的评分、样本量、价位带与地址，全部取自 **Google Maps 实时条目**（2026-09-29，中文关键词检索）。

---

### 补充（2026-09-29 第二轮）：按商场楼层重排，并补全泛亚

按菜系分类仍不完整，而实际逛街时人是**按商场和楼层**记店的。因此把这一节从「按菜系」改成**「按商场楼层 ＋ 按菜系」双索引**，并把片区扩到整个泛亚。

**Market Square（341 Mains Rd，商场本身 4.3／4,070）**——本项目描述的那一栋，核到 15 家：
Level 2 有 **Goukai Japanese 4.7／233**（楼上的日本菜）与 **Seoul Garden 韩式烤肉 4.3／2,018**；
Shop 50 **Wil's Resto 菲律宾 4.5／455**（同层的菲律宾菜）；Shop 51 **Lert Rod Thai 4.6／543**；
Shop 38 **Malaya Corner 旺角 3.7／1,174**（俗称「旺角」，样本大但分数低）；
Shop 21g **Woka Woka 3.1／866** 是本栋最低分。

**Sunny Park（342 McCullough St）**——9 家里 6 家过闸门，**平均分明显高于另两栋**：
Miss 7 柒彩 4.8／802、Orange Tea 4.8／1,186、Nan Hot Pot 4.7／177、Mui G Kitchen 梅姑 4.7／740、
YORI 日本 4.7／560、食味 Luo's 4.6／1,221；台式热炒 **百家千味 Glamorous Wok 4.1／705**（台式热炒）。

**Sunnybank Plaza（358 Mains Rd）**——老牌大茶楼集中地，**饮茶三家 3.2–3.8 全部不过闸门**
（Landmark 3.2／1,291、Golden Lane 金都 3.6／866、Sunnybank Oriental 3.8／536），
反而麻辣烫与炸鸡更稳（Love Malatang 4.5／331、Korean Chicken & 4.4／430）。

**Inala（越南）**——Sunnybank 是华／韩／日的集中地，**越南菜的集中地在 Inala**：
PHO BA NGA **4.7／331、人均 $1–20**（本片区同时最高分且最便宜）、Pho An Skylark 4.5／771（样本最大）、
TRONGAN 4.7／145、Phở Queen 4.3／343（Saigon Plaza）。

**「柏林酒楼」未能确认。** 常被提到的「柏林酒楼」，最接近的是 **Parkland Restaurant（407 Mains Rd，3.3／677）**
——Google 描述为「经典中菜加饮茶，老式装潢」，与描述吻合，但**本轮未在任何官方来源确认这个中英文名对应关系**，
因此在成果里只标为「中文常被称作柏林酒楼，未确认」。

**商场表的一个口径调整：** 这几张表**连未过闸门的也一并列出并标红**，因为逛商场时需要知道**整层楼有什么**，
而不只是过闸门的那几家。这与主表「只列过闸门的」是两种不同用途，已在页面上写明。

---

## 十五、全市普查：8,046 条持牌记录（2026-09-29）

目标是「把全布里斯班的餐饮场所收齐，看看到底有多少条」。**这件事用 Google 做不到，也不该做**：
Maps 每次搜索最多返回约 20 条、没有列出全部的接口；Places API 需付费密钥；大规模抓取违反其服务条款。

改用**布里斯班市议会持牌食品经营场所登记册**（[Food Safety Permits / Eat Safe 开放数据](https://data.brisbane.qld.gov.au/explore/dataset/food-safety-permits/)，CC-BY），
全量导出留档于 `research/brisbane-food-permits-2026-09-29.json`。**覆盖布里斯班市辖区**，Logan（Greenbank、Springwood）不在内。

| 拆分 | 数量 |
|---|---:|
| **总登记数** | **8,046** |
| 面向食客的场所 | **7,020** |
| 　· 固定门店 | 6,213 |
| 　· 流动摊／市集摊 | 808 |
| 非食客（工厂／托幼／养老／医院／宴会承办等） | 1,026 |

按持证类别（可多重持证）：Cafe/Restaurant **4,152** · Takeaway **2,002** · Bakery **555** · Food Stall 476 ·
Mobile Food 332 · Food Shop 253 · Delicatessen 175 · Accommodation Meals 56。

**Eat Safe 星级（第四套口径，测食品安全不测口味；仅 4,152 家 Cafe/Restaurant）**：
5 星 **282（6.8%）** · 4 星 1,057（25.5%）· 3 星 711（17.1%）· **未评级 2,102（50.6%）**。
→ 「Eat Safe 5 星」比 Google 4.7 更窄，但筛的是厨房卫生。**可叠加，不可替代。**

**地理集中度（208 个郊区）**：Brisbane City（CBD）**1,299（18.5%）** · Fortitude Valley 277 · South Brisbane 206 ·
Sunnybank 161 · Upper Mount Gravatt 158 · West End 156 · Chermside 142 · Woolloongabba 114 · Hamilton 109 ·
Sunnybank Hills 108 · Newstead 88 · Indooroopilly 83 · Inala 79。
→ **Sunnybank ＋ Sunnybank Hills ＋ Upper Mt Gravatt ＋ Inala ＝ 506 家，多于 Fortitude Valley ＋ South Brisbane 之和。**

### 按店名关键词分菜系失败了——而且是同一个偏差的第二次出现

登记册没有菜系字段，只能按店名关键词猜。结果：**52.2%（3,665 家）无法按店名判断**；
更糟的是**中餐只数出 113 家（1.6%）**，韩餐 31 家、奶茶 46 家——**明显是错的**。

原因：中餐、韩餐、奶茶店大量使用专有名词命名（食味 Luo's Place、Mui G Kitchen、Miss 7 柒彩、胖辣椒），
店名里根本没有 "Chinese"、"wok"、"bubble tea"。

> **这是第十四节那条教训的第二次出现，换了个形式：**
> 先是「用英文榜单取候选池 → 漏掉 Sunnybank」，现在是「用英文关键词猜菜系 → 漏掉所有用专有名词命名的店」。
> **凡是按语言或关键词去切一个多语言社区的餐饮，都会系统性地少数一大块。**
> 要真正按菜系统计，只能逐条读 Google 的分类字段（中文检索时会返回「火锅」「川菜」「珍珠奶茶」）——
> **7,020 家逐条查不现实，本轮未做，照实记为未完成。**

### 覆盖率

本指南收录 150 家（去重店名），与登记册粗匹配约 90 家 ≈ **面向食客场所的 2%**。
匹配不上的 60 家两个原因：①登记册用持证主体名，与招牌名不同；②不在布里斯班市辖区。

**2% 不是缺陷，是闸门的定义**——主闸门 Google ≥4.7 且 ≥200 本就是极窄的筛子。
**指南的作用是「从 7,020 里挑出值得专程去的 150」，不是做名录。**
要名录就用市议会登记册（官方、免费、可下载），**但它只有食品安全星级，没有菜系、没有口碑。**

---

## 十六、能不能和 Google 对上？抽样结果、API 成本、其他数据源（2026-09-29）

### 1. 能对上——随机抽 15 家，13 家干净命中

从 6,180 家固定门店里用固定随机种子抽样，逐条在 Google Maps 查：

| # | 登记册名称 | Google 命中 | 评分／样本 | 判定 |
|---|---|---|---|---|
| 1 | Bong's Donburi（St Lucia） | BoNG's Donburi | 4.6／124 | ✅ |
| 2 | Canvas（Woolloongabba） | Canvas Club | 4.6／781 | ✅ |
| 3 | Gather Bistro（CBD） | Gather | 4.2／110 | ✅ |
| 4 | Boost Juice Garden City | Boost Juice | 3.5／168 | ✅ 连锁，分店不易分辨 |
| 5 | Cultivate Design Co（Wynnum） | 同名 | 4.9／34 | ✅ |
| 6 | Cafe Valsapori（Heathwood） | 同名 | 4.3／69 | ✅ |
| 7 | Eat at Billys（Paddington） | 同名 | 4.8／144 | ✅ |
| 8 | The Cake Bar（South Brisbane） | THE CAKE BAR | 4.5／57 | ✅ |
| 9 | Italian Street Kitchen West End | 同名 | 4.0／1,393 | ✅ |
| 10 | **ISS Facility Management Pty Ltd**（Wacol） | ISS Facility Services | 4.3／16 | ❌ **假匹配**——匹配到清洁公司总部，不是餐饮点 |
| 11 | **Toiseach Pty Ltd T/As Chocolate Elements** | Chocolate Elements | **4.7／241** | ✅ 靠 `T/As`（trading as）字段救回 |
| 12 | **Grill & Roll Pty Ltd**（Upper Mt Gravatt） | 只返回搜索结果列表 | 3.9／323？ | ⚠️ **不确定，未采信** |
| 13 | Neko Land（West End） | Nekoland Ramen & Bar | **4.8／229** | ✅ |
| 14 | Sizzling Braised Pot（Sunnybank Hills） | 同名 | 3.1／242 | ✅ |
| 15 | Mitsuki Sushi George St | Mitsuki Sushi | 4.6／185 | ✅ |

**命中率 13/15 ≈ 87%。两类失败来自同一个原因：登记册用的是持证主体名（Pty Ltd），不是招牌名。**
`T/As`（trading as）字段能救回一部分——第 11 条就是靠它。**全量匹配前必须先解析 `T/As` 并剔除公司后缀。**

### 2. 随机抽样就抓出两家本指南漏掉的过闸门店

13 家干净样本里，有 **2 家过主闸门（Google ≥4.7 且 ≥200）**：

- **Chocolate Elements 4.7／241**（South Brisbane，巧克力店）
- **Nekoland Ramen & Bar 4.8／229**（West End，拉面）

**两家本指南都没有。** 命中率 2/13 ≈ 15%，样本太小、置信区间很宽（约 2%–45%），
但足以支撑一个数量级判断：**全市过主闸门的店在几百家量级，不是几十家。本指南收录的 23 家远不是全部。**

> 这条把前面「覆盖 2%」的说法说得更准确了：不是「7,020 家里只有 23 家够格」，
> 而是「**我只在一个偏窄的候选池里找过**」。真要找齐，必须逐条查。

### 3. 全量逐条查要多少钱

Google Places API (New) **按字段档位计费**：`rating` 与 `userRatingCount` 属 **Enterprise** SKU，
**评论正文 `reviews` 属 Enterprise + Atmosphere**。计费规则是**整次请求按所请求字段里的最高档计价**。

| 路线 | 单价 | 7,020 家一次全量（已扣免费额度） |
|---|---|---|
| Text Search Enterprise（一次调用直接返回评分） | US$35／1,000 | **≈ US$210** |
| Text Search Essentials 取 ID（IDs-only 免费）＋ Place Details Enterprise 取评分 | US$20／1,000 | **≈ US$120** |
| 同上，但要**评论正文**（Enterprise + Atmosphere） | US$25／1,000 | **≈ US$150** |

**一次全量约 US$120–210（约 A$185–320）**；每月刷新就是每月这个数。
免费额度：Essentials 每月 10,000 次、Pro 5,000 次、Enterprise 1,000 次。

**只做华人餐饮密集的四个区**（Sunnybank + Sunnybank Hills + Upper Mt Gravatt + Inala，506 家）：
**约 US$10**，基本压在免费额度边缘——**这是性价比最高的一次性投入。**

### 4. 别的评论网站与数据源

**A. 免费开放的地点名录——有 POI，没有评分**

| 数据源 | 许可 | 说明 |
|---|---|---|
| [Foursquare Open Source Places](https://opensource.foursquare.com/os-places/) | **Apache 2.0，可商用** | 1 亿+ 全球 POI，22 个核心字段，每月更新，Parquet 放在 S3 |
| [Overture Maps Foundation](https://overturemaps.org/) | CDLA Permissive 2.0 | Meta／微软／AWS／TomTom 主导，含 places 主题 |
| OpenStreetMap | ODbL | 免费，但澳洲餐饮覆盖不完整 |

→ 这些能替代「名录」，**替代不了评分**。而我们已经有更好的本地名录（市议会 8,046 条）。

**B. 有评分，但要申请或付费**

- **TripAdvisor Content API** —— 有免费档但需审批；**本项目实测其网页端对自动访问返回空白页**。
- **Yelp Fusion** —— 澳洲数据稀薄，基本不可用。
- **Foursquare Places API（商用版）** —— 有评分与到访热度，付费。

**C. 本地／垂直口径**

- **Eat Safe（市议会）** —— 官方食品安全星级，**已用**，免费且完整。
- **AGFG 帽子奖（20 分制）**、**Gourmet Traveller 指南** —— **已用**，专业评审口径。
- **外卖平台（UberEats／DoorDash／Menulog）** —— 有评分，而且是**另一套人群**（外卖客 vs 堂食客），
  **无公开 API**。
- **大众点评／小红书** —— 华人口径，**人机验证挡住，本项目不做验证码**。

> **一个现成的口子：** 当前工作环境里挂着一个 **UberEats 连接器，但尚未授权**（同一环境还有 resy、stayingapi 两个未授权连接器）。
> 在 claude.ai 的连接器设置里完成授权后，就能多一套**外卖评分**口径——那是和 Google 堂食评分完全不同的人群，
> 对平价档和外卖店尤其有用。**本会话无法代为完成授权。**

### 5. 结论

**能匹配，成本不高（全量 A$185–320，重点四区约 A$15），但必须先解决持证主体名的问题。**
真正的收益不在「补齐名录」，而在**把候选池从榜单换成全量**——
随机抽 13 家就冒出 2 家本指南漏掉的过闸门店，说明现在这份名单的天花板不是闸门定得太严，是**候选池太窄**。

---

## 十七、牛排与咖啡（2026-09-29 补）

本轮补查「牛排餐厅 Norman Morrison」和「咖啡排行」——**这两类之前都没有单独查过**，
牛排只零散出现在主表（Rothwell's）和未过闸门表（SK Steak），**Norman、Morrison、Breakfast Creek 完全没有**。

### 牛排分成两个世界，分数不能混比

| 类型 | 评分区间 | 样本 | 人均 |
|---|---|---|---|
| 老牌牛排酒吧 | **4.2–4.3** | **2,000–7,800** | **$40–60** |
| 精致牛排馆 | **4.4–4.8** | 300–3,500 | **$80–200+** |

**本类闸门：Google ≥4.2 且 ≥500**（分两张表排）。

**老牌酒吧组**：Breakfast Creek Hotel **4.2／7,782**（<b>全指南样本最大的一家</b>，Albion，1889 年建筑、木炭烤架）、
Norman Hotel **4.3／3,536**（Woolloongabba，以「布里斯班最差的素食餐厅」自嘲，自助烤架）、
Morrison Hotel **4.3／2,235**（Woolloongabba，与 Norman 步行 10 分钟）。
→ **正好在往 Gabba 方向的常走路线上，但它们靠牛排本身，不是 weekday special。**

**精致组**：Fatcow on James St 4.8／1,272（**$200+**，AGFG 14）、Rich & Rare 4.8／3,494（AGFG 13）、
Walter's Steakhouse 4.5／2,048、Moo Moo 4.5／1,830（AGFG 12）、Rothwell's 4.7／1,067（已在主表）、
SK Steak & Oyster 4.4／717（$200+）。

**未过闸门**：San Telmo 4.8／**150**（阿根廷炭烤，$100–200，分数极高但样本不足）、
Deery's 4.8／308、Black Hide Queen's Wharf 4.4／431、Black Hide by Gambaro 4.0／1,084。
**Cha Cha Char 与 Black Hide by Gambaro 的查询只返回搜索结果列表、未取到门店卡片，数字标为未确认。**

### 咖啡：评分门槛必须调高，不是调低

咖啡店评分普遍虚高（一条街上 4.8 很常见），所以**本类闸门用和主闸门一样严的 ≥4.7，靠 ≥200 的样本门槛挡住「十几个人打 5 分」**。

过闸门 10 家：John Mills Himself 4.8／1,120（已在主表）、Ricochet 4.8／325、Percolate 4.8／248、
Roasting Warehouse 4.8／226、The Tiller 4.8／216、Black Sheep 4.8／296、
Death Before Decaf **4.7／1,571**（本类样本最大，24 小时）、Bunker 4.7／721、Told You So 4.7／502（在 Moreton Bay，远）、
Unbearable Bagels 4.7／333（已在主表）。

**观察名单（分数更高但样本 <200）**：FAVE **5.0／156**、Coffee on Constance 5.0／35、
The Hideout 4.9／118、General Coffee 4.9／114、**Joe Tom Coffees 4.9／49（423 Wondall Rd, Manly West）**、
Coffee Mentality 4.8／167、Foster & Black 4.7／100。

> 这一组的意义：**分数比过闸门那张表还高，只是评论数没到**。单列出来，而不是当作「不够格」丢掉——
> 小店往往就是这样起步的。**Joe Tom 就在 Wynnum Manly Leagues Club 同一条路上。**

---

## 十八、其余菜系全扫（2026-09-29）

按第十四节确立的方法（Google Maps 按菜系检索 → 抓 评分／样本／众报价位／地址 → 套一条写明的闸门 → 过与不过分列）
把剩下的菜系补完：**印度／意大利／法／希腊／中东／墨西哥／西班牙／汉堡／烘焙／素食／东非**。

**统一闸门：Google ≥4.5 且评论 ≥300**——比主闸门低 0.2、样本从 200 提到 300，**用样本量换评分宽度**。

### 两条新发现

**① Moorooka 的 Beaudesert Rd 是第三个族裔餐饮聚集区。**
197–201 号一带至少四家东非（埃塞俄比亚／厄立特里亚）餐厅：
Arhibu **4.9／284** · Ethiopian Village 4.6／271 · Eliza Eritrean 4.9／80 · Salina 4.9／72 · Afro 4.9／39。
**分数全在 4.6–4.9，样本全部偏小**，按 ≥300 几乎全军覆没（全组只有 West End 的 Mu'ooz 4.5／556 过闸门）。

> 继 **Sunnybank（华／韩／日）**、**Inala（越南）** 之后，这是**第三个靠族裔社群支撑、被英文餐饮榜单完全忽略的片区**。
> 三次都是同一个结构：**社群支撑 → 分数高 → 英文样本少 → 榜单不收录**。
> 这条现在可以写成规律，而不是个案。

**② 名气与分数经常不是一回事。**
- **Lune Croissanterie**（全澳最有名的可颂店之一）布里斯班两家：**4.2／1,155（South Brisbane）、4.3／614（CBD）——都没过闸门**。
- 西班牙菜里样本最大的 **Olé 4.4／4,182** 同样没过。
- 反过来，**Milky Lane Newstead 4.8／9,015** 成为全指南样本最大的一家（超过 Breakfast Creek 的 7,782）。

**样本量大只说明人多，不说明分高——这两个维度必须分开看。**

### 各组要点

- **印度**：Bagicha 4.9／578 最高分；**Indian Curry Hutt 4.8／864 人均 $1–20 最便宜**；**Namaste Manly 4.8／317 湾区一侧最近**。
- **意大利**：Antica 4.8／1,534、Italia Lane 4.8／1,068、La Favolosa 4.9／690、Toscano 4.7／1,194。
- **法餐**：**À la Bonne Franquette 5.0／464 是全指南唯一一家 5.0 且样本过 300**；Pompette 4.8／1,817（AGFG 12）。
- **希腊**：Opa Bar & Mezze 4.8／**4,239**（本组样本最大）；**Lemoni Tingalpa 4.8／1,635，人均 $20–80，离湾区最近**。
- **中东／土耳其**：**Pera Palace（Wynnum）4.8／675** 就在湾区；Mado 4.5／2,904 样本最大。
- **墨西哥**：Poca Madre 4.8／1,837；**El Planta 4.7／859 是纯素墨西哥**。
- **西班牙**：只有 Moda 4.7／1,643 与 Botellon 4.7／803 过闸门。
- **汉堡**：Milky Lane **4.8／9,015**；Sue's 4.5／2,076。
- **烘焙**：Christian Jacques 4.8／1,524、Riser 4.8／471、C'est Du Gateau 4.8／376。
- **素食**：The Green Edge 4.7／1,630 样本最大；Vegan Restaurant West End、Dicki's、Vega 均 4.8。

---

## 十九、按框架回扫：九类遗漏（2026-09-29）

用当前框架对照自查，找出**框架本身没覆盖的品类**，逐一补扫：

| 补的品类 | 闸门 | 过闸门要点 |
|---|---|---|
| 精酿啤酒厂 | ≥4.5／≥200 | Range 4.8／522 · **Crafty Monk 4.8／328（Tingalpa，离湾区最近）** · Hiker 4.8／253 |
| 农夫市集 | ≥4.2／≥200 | Brisbane City Markets 4.5／642 · Carseldine 4.5／1,154 · **Jan Powers Manly 4.4／280** · Saturday Fresh Market 4.3／**2,317** |
| 早午餐 | ≥4.7／≥500 | **Clove n Honey 4.8／2,502** · Dovetail Social 4.8／507 · Blue Bear 4.7／767 |
| 炭烤鸡·炸鱼薯条 | ≥4.2／≥200 | Sizzling Birds 4.6／327 · Charcoal Chooks 4.5／338 · **Stanley's 4.2／205，人均 $1–20** |
| 冰淇淋·Gelato | ≥4.7／≥200 | **Shiro Gelato 4.9／1,832** · Matilda 4.8／348 |
| 清真·自助 | ≥4.5／≥500 | **LouLan 楼兰清真 4.6／969（新疆菜）** · Ariala Kippa-Ring 4.5／2,317 |
| 亚洲超市 | ≥4.3／≥100 | Sunlit Valley 4.5／149 · Davely's CBD 4.5／148；**Yuen's Market 4.0／1,145 未过** |
| 深夜餐饮 | — | **扫不成，见下** |
| 页面结构 | — | 17 节、40 页，**没有目录**——已补 |

### 一处更正：Andonis 列错了分店

平价档里列的是 **Andonis Fortitude Valley 4.5／3,313**。
但同一品牌在 **Manly 还有一间：191 Stratton Tce，4.7／1,514**——**分数高 0.2，且在湾区**。

原因还是候选池：当初是从 Fortitude Valley 的榜单取的，**只查了一间**。
> **规律补充：连锁品牌必须逐个分店查。同名不同分店的评分差 0.2 很常见，而榜单只会收录其中一家。**

### 深夜餐饮扫不成的原因

**Google Maps 的文本检索查不出「24 小时营业」**——搜 late night / 24 hours open 只返回一家不相关的 kebab 店。
**营业时间是字段不是关键词**，只能逐条读 Place Details（即第十六节那套 API 成本）。
本轮只能照实写沿途已知的三条：Death Before Decaf 24 小时、Wynnum Manly Leagues 9:00–翌日 3:00、hôntô 周五六较晚。**其余未查，不做推测。**

---

## 资料依据

**专业评审口径**
[AGFG 2026 布里斯班帽子奖榜单](https://www.agfg.com.au/awards/brisbane)（20 分制，49 家） ·
[Gourmet Traveller 2026 昆州最佳餐厅](https://www.gourmettraveller.com.au/dining-out/restaurant-guide/best-restaurants-queensland-20148/)（全澳 100 家里的昆州 15 家）

**实时评分、众报价位带、菜单照片**
Google Maps 各店条目（2026-09-28 逐家读取：评分、评论数、「$X–Y per person · reported by N people」、Menu 相册第一张照片） ·
[Ngon 官网菜单 PDF](https://static1.squarespace.com/static/5cd8c0ddb10f252dce3b0a20/t/69e60d4f1cdc912231e2c0eb/1776684456727/ngon_menu.pdf)（链接由 Google Maps 提供）

**评分与评论数（Wanderlog 镜像 Google Maps，用于初筛）**
[50 家最佳餐厅](https://wanderlog.com/list/geoCategory/75441/where-to-eat-best-restaurants-in-brisbane) ·
[50 家最佳吃处](https://wanderlog.com/list/geoCategory/71872/best-places-to-eat-in-brisbane) ·
[50 家最佳早午餐](https://wanderlog.com/list/geoCategory/11182/best-breakfast-and-brunch-in-brisbane) ·
[50 家最佳中餐](https://wanderlog.com/list/geoCategory/23677/best-chinese-food-in-brisbane) ·
[Longtime Dining 详情页](https://wanderlog.com/place/details/1826409/longtime-dining)

**价格（官方来源，2026-09-28 逐家取）**
[Exhibition 菜单](https://www.exhibitionrestaurant.com/menu) ·
[The Fifty Six 菜单](https://www.thefiftysix.com.au/menu)与[banquet PDF](https://www.thefiftysix.com.au/s/260624_TheFiftySix_Banquets_With-wine-pairings-A5_web.pdf) ·
[Longwang banquets](https://www.longwang.com.au/banquets) ·
[Oh Boy, Bok Choy! 菜单 PDF](https://www.ohboybokchoy.com.au/) ·
[Short Grain 菜单](https://www.shortgrain.com.au/menu) ·
[hôntô 菜单](https://anyday.com.au/honto-menus) ·
[Agnes 菜单](https://anyday.com.au/agnes-menus) ·
[sAme sAme 菜单](https://anyday.com.au/same-same-menus) ·
[GRECA 菜单](https://www.greca.com.au/menus) ·
[Beccofino 菜单 PDF](https://www.beccofino.com.au/s/Beccofino_menu.pdf) ·
[Montrachet 菜单 PDF](https://www.montrachet.com.au/s/Menu-Back.pdf) ·
[Joy 菜单页](https://www.joyrestaurant.com.au/new-page-1) ·
[Smoked Paprika 菜单](https://smokedpaprika.com.au/menu-classic/) ·
[Farm House 菜单 PDF](https://www.farmhousekedron.com.au/) ·
[Little Black Pug 菜单 PDF](https://www.littleblackpug.com.au/) ·
[1889 Enoteca 点单页](https://bopple.app/5324/menu) ·
[NAÏM 点单页](https://bopple.app/naim-restaurant) ·
[Unbearable Bagels 点单页](https://bopple.app/unbearablebagels)

**背景与故事**
[Broadsheet · The Fifty Six](https://www.broadsheet.com.au/brisbane/restaurants/the-fifty-six) ·
[Broadsheet · Short Grain](https://www.broadsheet.com.au/brisbane/fortitude-valley/restaurants/short-grain) ·
[Broadsheet · Longwang](https://www.broadsheet.com.au/brisbane/restaurants/longwang) ·
[Broadsheet · Rothwell's](https://www.broadsheet.com.au/brisbane/restaurants/rothwells-bar-grill) ·
[Qantas Travel Insider · hôntô](https://www.qantas.com/travelinsider/en/explore/australia/queensland/brisbane/honto---restaurant-review.html) ·
[Uber 专访 · Joy 的 10 个座位](https://www.uber.com/en-AU/blog/this-10-seater-restaurant-is-choosing-customer-satisfaction-over-industry-accolades) ·
[Kedron Today · Oh Boy, Bok Choy!](https://kedrontoday.com.au/new-restaurant-oh-boy-bokchoy-stafford/) ·
[Concrete Playground · 布里斯班最佳餐厅 2026](https://concreteplayground.com/brisbane/best-of/best-restaurants-brisbane/)

**第三方套餐盘点（本轮已证明会过期，仅作下限参考）**
[Sitchu · 最佳套餐](https://sitchu.com.au/brisbane/restaurants/best-set-menus-brisbane) ·
[Urban List · 最佳品尝菜单](https://www.theurbanlist.com/brisbane/a-list/best-degustations-brisbane)

**俱乐部特价（官网，2026-09-29）**
[Easts Leagues · The Brasserie](https://eastsleagues.com.au/dining-and-bars/the-brasserie/) ·
[Wynnum Manly Leagues · Specials](https://www.wynnummanlyleagues.com.au/specials/) ·
[Wynnum Manly Leagues · The Grill](https://www.wynnummanlyleagues.com.au/gulls-restaurant/) ·
[Kedron-Wavell · The Kitchen](https://kedron-wavell.com.au/the-kitchen-best-chermside-cafe/) ·
[Broncos Club · Promotions](https://broncosclub.com.au/promotions/)（全部为博彩抽奖） ·
[Greenbank · Bar & Dining Promotions](https://greenbankservicesclub.com.au/Eat-Drink/Bar-Dining-Promotions)（同上）

**API 与替代数据源**
[Google Places API (New) 计费文档](https://developers.google.com/maps/documentation/places/web-service/place-details) ·
[Places 字段档位对照](https://developers.google.com/maps/documentation/places/web-service/data-fields) ·
[Foursquare Open Source Places（Apache 2.0）](https://opensource.foursquare.com/os-places/) ·
[Overture Maps Foundation](https://overturemaps.org/)

**官方名录与食品安全星级**
[Brisbane City Council · Food Safety Permits（Eat Safe）](https://data.brisbane.qld.gov.au/explore/dataset/food-safety-permits/)，8,046 条，CC-BY，全量导出留档 `research/brisbane-food-permits-2026-09-29.json`

**地图
底图 © OpenStreetMap contributors；坐标由各店公布地址经 Nominatim 反查，脚本 [`scripts/build_brisbane_dining_map.py`](../scripts/build_brisbane_dining_map.py)。
