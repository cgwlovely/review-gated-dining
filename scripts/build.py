#!/usr/bin/env python3
"""Data -> gate evaluation -> outputs. One command, no third-party dependencies.

    python3 scripts/build.py           build everything
    python3 scripts/build.py --check   validate only; exit 1 on any error

Reads   data/venues.csv, data/gates.yml, data/sources.csv, data/venue_aliases.csv
Writes  build/venues.json, build/venues.csv, build/summary.md, build/main-table.md,
        docs/data/venues.json, docs/data/venues.csv   (download + filter on the site)

gate_pass is ALWAYS computed here from gates.yml. It is never read from the input.
"""
import csv, json, math, sys, re, datetime, pathlib, hashlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA, BUILD, DOCSDATA = ROOT/'data', ROOT/'build', ROOT/'docs'/'data'
TODAY = datetime.date(2026, 9, 29)          # snapshot date; override with --today=YYYY-MM-DD

# ---------------------------------------------------------------- tiny YAML subset
def load_yaml(path):
    """Enough YAML for gates.yml: nested maps, scalars, quoted strings, comments."""
    try:
        import yaml                                    # use the real thing if present
        return yaml.safe_load(path.read_text())
    except ImportError:
        pass
    root, stack = {}, [(-1, {})]
    stack[0] = (-1, root)
    for raw in path.read_text().split('\n'):
        if not raw.strip() or raw.lstrip().startswith('#'):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if ':' not in line:
            continue
        key, _, val = line.partition(':')
        key, val = key.strip(), val.strip()
        while stack and stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1]
        if val == '':
            node = {}
            parent[key] = node
            stack.append((indent, node))
        else:
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val in ('null', '~'):
                val = None
            elif re.fullmatch(r'-?\d+', val):
                val = int(val)
            elif re.fullmatch(r'-?\d*\.\d+', val):
                val = float(val)
            parent[key] = val
    return root

# ---------------------------------------------------------------- helpers
def num(s):
    s = (s or '').strip()
    if s == '': return None
    try: return float(s)
    except ValueError: return None

def days_since(d):
    if not d: return None
    try: return (TODAY - datetime.date.fromisoformat(d)).days
    except ValueError: return None

def conservative_rating_proxy(rating, n, z=1.96):
    """A HEURISTIC penalty for small samples - NOT a confidence interval.

    Google exposes a mean star rating and a count, not the 1-5 vote distribution, so a
    Wilson interval (which is defined for a binomial proportion) has no strict statistical
    reading here. We keep the shape of the formula because it penalises small n in a
    defensible, monotonic way, and we name it for what it is. A real interval needs the
    star histogram or review-level data.
    """
    if not rating or not n: return None
    p = (rating - 1) / 4.0                         # map 1..5 -> 0..1
    d = 1 + z*z/n
    centre = p + z*z/(2*n)
    margin = z * math.sqrt((p*(1-p) + z*z/(4*n)) / n)
    return round(((centre - margin) / d) * 4 + 1, 3)

def shrunk(rating, n, prior_mean, prior_weight):
    """Bayesian shrinkage toward the city mean: a 4.9/34 must not outrank a 4.8/9015."""
    if rating is None or n is None: return None
    return round((rating*n + prior_mean*prior_weight) / (n + prior_weight), 3)

def freshness(dates, half_life):
    ages = [days_since(d) for d in dates if d]
    ages = [a for a in ages if a is not None]
    if not ages: return None
    return round(0.5 ** (max(ages) / half_life), 3)

FLAGS = {
    'booking_ahead':      ('需提前订位', 'books well ahead'),
    'weekend_surcharge':  ('周末/公假加价', 'weekend or PH surcharge'),
    'member_price':       ('会员价', 'member pricing'),
    'veg_friendly':       ('素食友好', 'vegetarian-friendly'),
    'price_stale':        ('价格可能过期', 'price may be stale'),
}
SCENARIOS = {
    'first_timer': ('第一次来：值得记住的一顿晚餐', 'First visit: a dinner worth remembering'),
    'chinese_food':('想吃中餐', 'Chinese food'),
    'date':        ('约会', 'Date night'),
    'family':      ('家庭聚餐', 'With family'),
    'cheap_eat':   ('便宜吃饱', 'Cheap and filling'),
    'coffee':      ('咖啡与甜点', 'Coffee and sweets'),
    'late_night':  ('夜宵', 'Late night'),
    'celebration': ('庆祝', 'Celebration'),
}
# Bands are ENTRY price ("from"): a venue joins a band on its two-person minimum.
# Every label must therefore say 起 / from - a test enforces it.
BUDGET_BANDS = [(0, 60, '两人最低 $60 以下'), (60, 120, '两人最低 $60–119'),
                (120, 250, '两人最低 $120–249'), (250, 10**9, '两人最低 $250 起')]

# A scenario that makes a cuisine claim must be backed by the cuisine field.
# Codes that name an occasion, never a cuisine. 'coffee' is deliberately absent: it is a
# legitimate cuisine value as well as a scenario, so it must not be rejected.
# 'cheap_eat' is the one scenario that makes a PRICE promise, so the price has to back it:
# a banquet at $62.5pp was surfacing there on rating alone, i.e. $125 for two.
CHEAP_EAT_MAX_FOR_TWO = 100      # AUD, food only
CHEAP_EAT_MAX_PER_ITEM = 40      # AUD, for a la carte venues

SCENARIO_ONLY_CODES = {'first_timer', 'chinese_food', 'date', 'family', 'cheap_eat',
                       'late_night', 'celebration'}

SCENARIO_REQUIRES_CUISINE = {
    'chinese_food': {'chinese', 'cantonese', 'sichuan', 'hunan', 'yum_cha', 'taiwanese', 'northern_chinese'},
}

# per-unit multiplier to reach "estimated total for two, food only, no alcohol"
TWO_PERSON = {
    'per_person_set':      lambda lo, hi: (lo*2, hi*2),
    'per_person_reported': None,   # a crowd-reported band is not a meal price - see below
    'item':                None,      # a la carte: cannot be derived honestly -> left null
    'for_two':             lambda lo, hi: (lo, hi),
    'whole_dish':          None,
    'set_menu':            lambda lo, hi: (lo*2, hi*2),
}

# ---------------------------------------------------------------- load
def load():
    gates = load_yaml(DATA/'gates.yml')
    venues = list(csv.DictReader((DATA/'venues.csv').open()))
    sources = {r['source_id']: r for r in csv.DictReader((DATA/'sources.csv').open())}
    aliases = list(csv.DictReader((DATA/'venue_aliases.csv').open()))
    ex_path = DATA/'scenario_exemptions.csv'
    exemptions = {(r['venue_id'], r['scenario']): r['reason']
                  for r in csv.DictReader(ex_path.open())} if ex_path.exists() else {}
    return gates, venues, sources, aliases, exemptions

# ---------------------------------------------------------------- validate
def validate(gates, venues, sources, aliases, exemptions=None):
    exemptions = exemptions or {}
    errors, warnings = [], []
    seen_id, seen_place = {}, {}
    gate_names = set(gates['gates'])
    src_types = {'official', 'google_reported', 'menu_photo', 'third_party'}
    units = set(TWO_PERSON)

    for i, v in enumerate(venues, 2):
        vid, where = v['venue_id'], f"row {i} ({v['venue_id'] or '?'})"
        if not vid:
            errors.append(f'{where}: venue_id is empty'); continue
        if vid in seen_id:
            errors.append(f'{where}: duplicate venue_id, first seen at row {seen_id[vid]}')
        seen_id[vid] = i

        pid = (v.get('google_place_id') or '').strip()
        if pid:
            if pid in seen_place:
                errors.append(f'{where}: google_place_id {pid} already used by row {seen_place[pid]}')
            seen_place[pid] = i

        if v['gate_name'] not in gate_names:
            errors.append(f"{where}: unknown gate_name '{v['gate_name']}'")

        # every rating needs a platform AND an observation date
        if num(v['rating']) is not None:
            if not v['rating_source']:
                errors.append(f'{where}: rating has no rating_source (platform label)')
            if not v['rating_observed_at']:
                errors.append(f'{where}: rating has no rating_observed_at')
            if num(v['review_count']) is None:
                errors.append(f'{where}: rating present but review_count missing')

        # every price needs a unit, a source type AND an observation date
        has_price = num(v['price_min_aud']) is not None or num(v['price_max_aud']) is not None
        if has_price:
            if not v['price_unit']:
                errors.append(f'{where}: price present but price_unit missing')
            elif v['price_unit'] not in units:
                errors.append(f"{where}: unknown price_unit '{v['price_unit']}'")
            if not v['price_source_type']:
                errors.append(f'{where}: price present but price_source_type missing')
            elif v['price_source_type'] not in src_types:
                errors.append(f"{where}: unknown price_source_type '{v['price_source_type']}'")
            if not v['price_observed_at']:
                errors.append(f'{where}: price present but price_observed_at missing')
            if v.get('price_source_type') != 'google_reported' and not v.get('price_source_url'):
                warnings.append(f'{where}: price has no source URL')
        if v['status'] not in ('active', 'uncertain', 'closed'):
            errors.append(f"{where}: unknown status '{v['status']}'")
        if v.get('recommendation_tier') not in ('editors_pick', 'conditional', 'directory'):
            errors.append(f"{where}: unknown recommendation_tier '{v.get('recommendation_tier')}'")
        if v.get('booking') not in ('required', 'recommended', 'walk_in'):
            errors.append(f"{where}: unknown booking '{v.get('booking')}'")
        for fld in ('one_liner_zh', 'one_liner_en'):
            s = (v.get(fld) or '')
            if s != s.strip():
                errors.append(f'{where}: {fld} has leading/trailing whitespace')
            if s.strip() and s.strip()[-1] in ',;，；':
                errors.append(f'{where}: {fld} ends with a stray {s.strip()[-1]!r}')
        if not (v.get('one_liner_zh') or '').strip():
            errors.append(f'{where}: one_liner_zh is empty - every recommended venue needs a reason')
        if not (v.get('one_liner_en') or '').strip():
            errors.append(f'{where}: one_liner_en is empty')
        for fl in (v.get('flags') or '').split(';'):
            if fl and fl not in FLAGS:
                errors.append(f"{where}: unknown flag '{fl}'")
        vcui = {c for c in (v.get('cuisines') or '').split(';') if c}
        leaked = vcui & SCENARIO_ONLY_CODES
        if leaked:
            errors.append(f"{where}: cuisines contains scenario code(s) {sorted(leaked)} - "
                          f"cuisines and scenarios are different vocabularies")
        for sc in (v.get('scenarios') or '').split(';'):
            if not sc:
                continue
            if sc not in SCENARIOS:
                errors.append(f"{where}: unknown scenario '{sc}'")
                continue
            need = SCENARIO_REQUIRES_CUISINE.get(sc)
            if need and not (vcui & need) and (v['venue_id'], sc) not in exemptions:
                errors.append(f"{where}: scenario '{sc}' claims a cuisine the venue does not have "
                              f"(cuisines={sorted(vcui)}); add an entry to data/scenario_exemptions.csv "
                              f"if this is deliberate")
            if sc == 'cheap_eat':
                lo, hi = num(v['price_min_aud']), num(v['price_max_aud'])
                unit = v['price_unit']
                too_dear = None
                if unit in ('per_person_set', 'set_menu') and lo is not None and lo * 2 > CHEAP_EAT_MAX_FOR_TWO:
                    too_dear = f"set price is ${lo}pp, i.e. ${lo*2:g} for two"
                elif unit == 'for_two' and lo is not None and lo > CHEAP_EAT_MAX_FOR_TWO:
                    too_dear = f"${lo:g} for two"
                elif unit == 'item' and hi is not None and hi > CHEAP_EAT_MAX_PER_ITEM:
                    too_dear = f"dishes run to ${hi:g}"
                if too_dear and (v['venue_id'], sc) not in exemptions:
                    errors.append(f"{where}: scenario 'cheap_eat' promises a cheap meal but "
                                  f"{too_dear} (limit ${CHEAP_EAT_MAX_FOR_TWO} for two / "
                                  f"${CHEAP_EAT_MAX_PER_ITEM} a dish) - drop the scenario or "
                                  f"add an entry to data/scenario_exemptions.csv")

        # staleness + borderline warnings
        age = days_since(v['rating_observed_at'])
        if age is not None and age > 90:
            warnings.append(f'{where}: rating is {age} days old (>90)')
        g = gates['gates'][v['gate_name']] if v['gate_name'] in gate_names else None
        if g and g.get('min_reviews'):
            n = num(v['review_count'])
            if n is not None and 0 <= n - g['min_reviews'] < g['min_reviews']*0.1:
                warnings.append(f"{where}: review_count {int(n)} is within 10% of the {v['gate_name']} threshold "
                                f"- a handful of reviews either way flips it")

    known = set(seen_id)
    for a in aliases:
        if a['venue_id'] not in known:
            errors.append(f"venue_aliases.csv: unknown venue_id '{a['venue_id']}'")
        if a['source'] and a['source'] not in sources:
            warnings.append(f"venue_aliases.csv: source '{a['source']}' not in sources.csv")
    return errors, warnings

# ---------------------------------------------------------------- derive
def derive(gates, venues, aliases):
    hl = gates['freshness']['half_life_days']
    pm, pw = gates['shrinkage']['prior_mean'], gates['shrinkage']['prior_weight']
    by_id = {}
    for a in aliases:
        by_id.setdefault(a['venue_id'], []).append(a['alias'])

    out = []
    for v in venues:
        g = gates['gates'][v['gate_name']]
        r, n = num(v['rating']), num(v['review_count'])
        rec = dict(v)
        rec['rating'], rec['review_count'] = r, (int(n) if n is not None else None)
        rec['lat'], rec['lon'] = num(v['lat']), num(v['lon'])
        rec['cuisines'] = [c for c in (v['cuisines'] or '').split(';') if c]
        rec['aliases'] = by_id.get(v['venue_id'], [])

        # gate_pass is computed here, never read from input
        if g.get('min_rating') is None:
            rec['gate_pass'] = None
            rec['gate_reason'] = 'no rating gate for this category'
        else:
            ok = r is not None and n is not None and r >= g['min_rating'] and n >= g['min_reviews']
            rec['gate_pass'] = bool(ok)
            rec['gate_reason'] = f"{v['gate_name']}: >={g['min_rating']} and >={g['min_reviews']}"
        rec['gate_min_rating'], rec['gate_min_reviews'] = g.get('min_rating'), g.get('min_reviews')

        rec['shrunk_rating'] = shrunk(r, n, pm, pw)
        rec['conservative_rating_proxy'] = conservative_rating_proxy(r, n)
        # Borderline: passes the hard gate, but the small-sample proxy does not clear it.
        # The hard gate stays the reader-facing rule; this flag is for auditing.
        # 硬闸门仍是对读者的规则；这个标记只用于审计与「边界候选」。
        mr = g.get('min_rating')
        if mr is not None and rec.get('conservative_rating_proxy') is not None:
            rec['borderline'] = bool(r is not None and r >= mr
                                     and rec['conservative_rating_proxy'] < mr)
            rec['borderline_reason'] = (f"passes on {r}, but the small-sample proxy is "
                                        f"{rec['conservative_rating_proxy']} (heuristic, not a CI)"
                                        if rec['borderline'] else '')
        else:
            rec['borderline'], rec['borderline_reason'] = False, ''
        rec['freshness'] = freshness([v['rating_observed_at'], v['price_observed_at']], hl)

        lo, hi = num(v['price_min_aud']), num(v['price_max_aud'])
        fn = TWO_PERSON.get(v['price_unit'])
        if fn and lo is not None and hi is not None:
            a, b = fn(lo, hi)
            rec['two_person_total_min'], rec['two_person_total_max'] = round(a), round(b)
            op = 'already priced for two' if v['price_unit'] == 'for_two' else 'x2'
            rec['two_person_basis'] = (f"{v['price_unit']} {op}, food only, "
                                       f"excludes alcohol and weekend/PH surcharges")
        else:
            rec['two_person_total_min'] = rec['two_person_total_max'] = None
            rec['two_person_basis'] = {
                'item': 'a la carte - not derivable from a price range',
                'per_person_reported':
                    'crowd-reported per-person band; doubling it does not give a meal budget',
                'whole_dish': 'priced per dish, not per person',
            }.get(v['price_unit'], 'no price recorded')

        # These mirror data/gates.yml:confidence_rules exactly. If you change one, change both.
        # gates.yml says "any observation", so BOTH the rating and the price date count.
        ages = [a for a in (days_since(v['rating_observed_at']),
                            days_since(v['price_observed_at'])) if a is not None]
        oldest = max(ages) if ages else None
        has_full_price = all([lo is not None, v['price_unit'],
                              v['price_source_type'], v['price_observed_at']])
        if (v['status'] != 'active'
                or v['rating_source'] == 'google_mirror'
                or (oldest or 0) > 180):
            rec['confidence'] = 'low'
        elif (has_full_price and v['price_source_type'] == 'official'
              and (oldest or 0) <= 90):
            rec['confidence'] = 'high'
        else:
            rec['confidence'] = 'medium'
        rec['oldest_observation_days'] = oldest
        out.append(rec)
    return out


# ---------------------------------------------------------------- quick pick (P0)
def quickpick_html(recs, snapshot):
    """The 3-minute front section, GENERATED from data - never hand-edited."""
    def maps(r):
        import urllib.parse
        return ('https://www.google.com/maps/search/?api=1&query='
                + urllib.parse.quote(f"{r['name']} {r['address']} Brisbane QLD"))
    def budget(r):
        # only a SET price may be called a two-person budget. The other two kinds
        # print what they actually are, so a $1-20 crowd band stops reading as "$2-40 for two".
        lo, hi = r['two_person_total_min'], r['two_person_total_max']
        if lo is None:
            if r['price_unit'] == 'item':
                return ('<span class="small">单点 · 两人预算未计算</span>'
                        + (('<br><span class="small" style="opacity:.75">菜品 $%s–%s</span>'
                            % (r['price_min_aud'], r['price_max_aud']))
                           if r.get('price_min_aud') not in (None, '') else ''))
            if r['price_unit'] == 'per_person_reported':
                return ('<span class="small">平台众报人均 $%s–%s</span>'
                        '<br><span class="small" style="opacity:.75">非套餐，未换算两人总价</span>'
                        % (r['price_min_aud'], r['price_max_aud']))
            return '<span class="small">价格不足以估算</span>'
        return f'<b>${lo}–{hi}</b>' if lo != hi else f'<b>${lo}</b>'
    def chips(r):
        # exactly ONE booking chip per venue, on a three-level scale. The lead time
        # rides inside it: a separate "books well ahead" chip next to "建议订位" read
        # as a contradiction, and next to "必须订位" as a repetition.
        flags = set((r.get('flags') or '').split(';'))
        out = []
        for fl in (r.get('flags') or '').split(';'):
            if fl in FLAGS and fl != 'booking_ahead':
                zh, en = FLAGS[fl]
                cls = 'chip warnchip' if fl in ('price_stale', 'weekend_surcharge') else 'chip'
                out.append('<span class="%s" title="%s">%s</span>' % (cls, en, zh))
        bk = {'required': '必须订位', 'recommended': '建议订位', 'walk_in': '可直接去'}[r['booking']]
        title = {'required': 'booking required', 'recommended': 'booking recommended',
                 'walk_in': 'walk in'}[r['booking']]
        if 'booking_ahead' in flags:
            bk += ' · 提前订'
            title += ', books well ahead'
        out.insert(0, '<span class="chip bk-%s" title="%s">%s</span>' % (r['booking'], title, bk))
        return ' '.join(out)
    def card(r):
        br = ' <span class="small">%s</span>' % r['branch_name'] if r['branch_name'] else ''
        rc = '{:,}'.format(r['review_count']) if r['review_count'] is not None else '—'
        # the suburb rides along under the name instead of taking a column of its own,
        # and the English line is web-only: in print it doubles the height of every row
        return ('<tr><td><b><a href="%s">%s</a></b>%s'
                ' <span class="small" style="opacity:.7">%s</span>'
                '<br><span class="small">%s</span>'
                '<span class="en-only"><br><span class="small" style="opacity:.75">%s</span></span></td>'
                '<td>%s</td><td class="small">%s</td>'
                '<td class="small">%s／%s<br>'
                '<span style="opacity:.75">核验 %s</span></td></tr>'
                % (maps(r), r['name'], br, r['suburb'], r['one_liner_zh'], r['one_liner_en'],
                   budget(r), chips(r), r['rating'], rc, r['rating_observed_at']))

    picks = [r for r in recs if r['gate_pass'] and r['recommendation_tier'] == 'editors_pick']
    rank = lambda rs: sorted(rs, key=lambda r: -(r['shrunk_rating'] or 0))
    H = ['<div class="card" id="quickpick">',
         '<h3>3 分钟选好 ｜ Pick in three minutes</h3>',
         '<p class="small">本节由 <code>data/venues.csv</code> 自动生成，与后面的详细资料库同源，'
         '不会各说各话。<b>两人预算＝食物总价，不含酒、不含周末与公假加价</b>；无法诚实换算的写明「按菜品计价」，不硬塞进档位。<br>'
         '<span style="opacity:.8">Generated from the dataset. Two-person budget = food only, excluding alcohol and '
         'weekend/public-holiday surcharges; venues that cannot be converted honestly say so instead of being forced into a band.</span></p>',
         '<div class="note"><b>这一页只从已进入结构化数据的 %d 家里挑，而那 %d 家全部是过了主闸门的正餐。</b>'
         '所以它<b>覆盖不到</b>平价小店、社区餐饮、俱乐部与 Pub 特价——那些在后面的章节里，但还没有数据化到能自动推荐。'
         '<b>「第一次来」这一档尤其要注意：它挑出来的都是内城的正餐，不代表全城的饮食面貌</b>；'
         '想看社区那一面，直接去 <a href="#sec3">§3 按区域吃</a>。</div>'
         % (snapshot['unique_venues'], snapshot['unique_venues'])]

    ft = rank([r for r in picks if 'first_timer' in r['scenarios']])[:5]
    H += ['<h4>%s ｜ %s</h4>' % SCENARIOS['first_timer'],
          '<div style="overflow-x:auto"><table><tr><th>店 ｜ 为什么选</th><th>两人预算</th><th>提示</th><th>Google</th></tr>']
    H += [card(r) for r in ft] + ['</table></div>']

    BUDGET_COLS = 5   # 档位 | 店（含区） | 预算 | 提示 | Google
    H += ['<h4>按两人预算 ｜ By two-person budget</h4>',
          '<p class="small"><b>档位按「最低两人消费」划分，所以每个标签都带「起」。</b>'
          '右侧显示的是完整区间——套餐跨度大时，最高价可能远高于档位上限，这是刻意显示出来的。<br>'
          '<span style="opacity:.8">Bands are entry price, hence "from" on every label. The column '
          'shows the full range: a wide set-menu spread can exceed the band ceiling, and is shown rather than hidden.</span></p>',
          '<div style="overflow-x:auto"><table><tr><th>档位（起）</th><th>店 ｜ 为什么选</th><th>两人预算（完整区间）</th><th>提示</th><th>Google</th></tr>']
    any_band = False
    for lo, hi, label in BUDGET_BANDS:
        # Banding is by ENTRY price (the two-person minimum). Labels carry 起/from, and each
        # row prints the full range, so a wide set-menu spread cannot read as the whole cost.
        band = rank([r for r in picks if r['two_person_total_min'] is not None
                     and lo <= r['two_person_total_min'] < hi])[:3]
        if not band:
            H.append('<tr><td><b>%s</b></td><td colspan="%d" class="small">'
                     '本档暂无编辑精选 | no editor pick in this band yet</td></tr>'
                     % (label, BUDGET_COLS - 1))
            continue
        any_band = True
        for i, r in enumerate(band):
            c = card(r)
            H.append(c.replace('<tr><td>', '<tr><td rowspan="%d"><b>%s</b></td><td>' % (len(band), label), 1)
                     if i == 0 else c)
    H.append('</table></div>')

    H += ['<h4>按场景 ｜ By occasion</h4>',
          '<div style="overflow-x:auto"><table><tr><th>场景</th><th>店 ｜ 为什么选</th><th>两人预算</th><th>提示</th><th>Google</th></tr>']
    for key, (zh, en) in SCENARIOS.items():
        if key == 'first_timer':
            continue
        grp = rank([r for r in picks if key in r['scenarios']])[:3]
        if not grp:
            grp = rank([r for r in recs if r['gate_pass'] and key in r['scenarios']])[:2]
        if not grp:
            continue
        for i, r in enumerate(grp):
            c = card(r)
            H.append(c.replace('<tr><td>', '<tr><td rowspan="%d"><b>%s</b><br>'
                               '<span class="small">%s</span></td><td>' % (len(grp), zh, en), 1) if i == 0 else c)
    H.append('</table></div>')

    s = snapshot
    H += ['<p class="small">本节的 <b>%d 家</b>已进入结构化数据（编辑精选 <b>%d 家</b>）。'
          '全书另有 <b>%d 家独立门店</b>、<b>%d 条门店链接</b>，其中 <b>%d 家</b>出现在一个以上的章节；'
          '这部分尚未迁入数据——见 '
          '<a href="https://github.com/cgwlovely/review-gated-dining/issues/1">issue #1</a>。</p>'
          % (s['unique_venues'], len(picks), s.get('distinct_on_page', 0),
             s.get('display_rows_page', 0), s.get('in_two_sections', 0)),
          '</div>']
    return '\n'.join(H)

# ---------------------------------------------------------------- emit
def check_page_refs():
    """Cross-references must survive a section being renamed or merged.

    Two ways they rot, both of which actually happened:
      - "§3 <old title>" keeps the old title after the section is renamed
      - href="#secN" points at a section that no longer exists
    """
    import re
    page = ROOT/'docs'/'index.html'
    if not page.exists():
        return [], []
    h = page.read_text()
    titles = {sid: re.sub('<.*?>', '', zh).strip() for sid, zh, _en in
              re.findall(r'<h2 id="(sec\d+)">(.*?)\s*<span class="h2en">(.*?)</span></h2>', h)}
    errs, warns = [], []
    ids = set(re.findall(r'id="([^"]+)"', h))
    for a in sorted(set(re.findall(r'href="#([^"]+)"', h))):
        if a not in ids:
            errs.append('docs/index.html: href="#%s" points at nothing' % a)
    # "§N 名称" must agree with that section's real title
    for num, named in re.findall(r'§(\d+)\s*([^<，。；、：:（）()【】「」]{2,24})', h):
        sid = 'sec' + num
        if sid not in titles:
            errs.append('docs/index.html: §%s referenced but there is no %s' % (num, sid))
            continue
        named = named.strip()
        real = titles[sid]
        if named and not (named in real or real.startswith(named) or named.startswith(real[:4])):
            warns.append('docs/index.html: "§%s %s" but §%s is titled "%s"' % (num, named, num, real))
    return errs, warns


def page_stats(recs):
    """Count what the published page actually shows, so the cover can stop saying '300+'."""
    import re, urllib.parse
    page = ROOT/'docs'/'index.html'
    if not page.exists():
        return {'display_rows_page': 0, 'repeated_venues': 0, 'distinct_on_page': 0,
                'in_two_sections': 0}
    h = page.read_text()
    qs = re.findall(r'maps/search/\?api=1&query=([^"\']+)', h)
    names = []
    for q in qs:
        s = urllib.parse.unquote(q)
        s = re.split(r'\s(?=(?:Shop|Level|Unit|Basement|L1|G\d|\d+[A-Za-z]?[/,]?\s))', s, maxsplit=1)[0]
        names.append(s.strip().lower())
    from collections import Counter
    c = Counter(names)
    # "linked twice" and "in two sections" are different numbers; the page used to
    # mix them, so both are computed here and neither is ever typed by hand
    sec_of = {}
    for part in re.split(r'(?=<h2 id="sec\d+">)', h):
        m = re.match(r'<h2 id="(sec\d+)">', part)
        sid = m.group(1) if m else 'front'
        for q in re.findall(r'maps/search/\?api=1&query=([^"\']+)', part):
            s = urllib.parse.unquote(q)
            s = re.split(r'\s(?=(?:Shop|Level|Unit|Basement|L1|G\d|\d+[A-Za-z]?[/,]?\s))', s, maxsplit=1)[0]
            sec_of.setdefault(s.strip().lower(), set()).add(sid)
    return {'display_rows_page': len(names),
            'distinct_on_page': len(c),
            'repeated_venues': sum(1 for n, k in c.items() if k > 1),
            'in_two_sections': sum(1 for n, ss in sec_of.items() if len(ss) > 1)}


def inject(fragment, marker, path):
    """Replace the block between <!--marker:start--> and <!--marker:end-->, creating it if absent."""
    a, b = f'<!--{marker}:start-->', f'<!--{marker}:end-->'
    h = path.read_text()
    if a in h and b in h:
        i, j = h.index(a), h.index(b) + len(b)
        h = h[:i] + a + '\n' + fragment + '\n' + b + h[j:]
        path.write_text(h)
        return 'replaced'
    return 'marker-missing'


def emit(recs, gates, sources, errors, warnings):
    BUILD.mkdir(exist_ok=True); DOCSDATA.mkdir(parents=True, exist_ok=True)
    try:
        sha = subprocess.run(['git','rev-parse','--short','HEAD'], cwd=ROOT,
                             capture_output=True, text=True).stdout.strip() or 'uncommitted'
    except Exception:
        sha = 'unknown'
    # NOTE: this is HEAD at build time, i.e. the commit the build ran *from*.
    # A commit cannot contain its own SHA, so a rebuild after committing will show a
    # one-commit difference. That is the only non-determinism in the build.
    ps = page_stats(recs)
    branches = sum(1 for r in recs if (r.get('branch_name') or '').strip())
    snapshot = {'snapshot_date': TODAY.isoformat(), 'built_from_commit': sha, 'commit': sha,
                'gates_version': gates.get('version'),
                'unique_venues': len({r['venue_id'] for r in recs}),
                'display_rows': len(recs),
                'branch_count': branches,
                'display_rows_page': ps['display_rows_page'],
                'distinct_on_page': ps['distinct_on_page'],
                'repeated_venues': ps['repeated_venues'],
                'in_two_sections': ps['in_two_sections']}

    payload = {'snapshot': snapshot, 'gates': gates['gates'], 'venues': recs}
    for p in (BUILD/'venues.json', DOCSDATA/'venues.json'):
        p.write_text(json.dumps(payload, ensure_ascii=False, indent=1))

    cols = ['venue_id','name','branch_name','suburb','address','lat','lon','category_primary',
            'cuisines','rating','review_count','rating_source','rating_observed_at',
            'shrunk_rating','conservative_rating_proxy','borderline','oldest_observation_days','gate_name','gate_pass','confidence','freshness',
            'price_min_aud','price_max_aud','price_unit','price_source_type','price_observed_at',
            'two_person_total_min','two_person_total_max','status','price_source_url']
    for p in (BUILD/'venues.csv', DOCSDATA/'venues.csv'):
        with p.open('w', newline='') as f:
            w = csv.writer(f); w.writerow(cols)
            for r in recs:
                w.writerow([';'.join(r[c]) if isinstance(r.get(c), list) else r.get(c, '') for c in cols])

    passed = [r for r in recs if r['gate_pass']]
    ranked = sorted(passed, key=lambda r: (-(r['shrunk_rating'] or 0), -(r['review_count'] or 0)))
    lines = [f"# Main table — {len(passed)} venues through the gate", '',
             f"snapshot {snapshot['snapshot_date']} · commit {sha} · ranked by shrunk rating", '',
             '| # | Venue | Suburb | Google | Shrunk | Two-person (food) | Price source | Confidence |',
             '|---|---|---|---|---|---|---|---|']
    for i, r in enumerate(ranked, 1):
        tp = (f"${r['two_person_total_min']}–{r['two_person_total_max']}"
              if r['two_person_total_min'] is not None else '—')
        lines.append(f"| {i} | {r['name']} | {r['suburb']} | {r['rating']}/{r['review_count']:,} | "
                     f"{r['shrunk_rating']} | {tp} | {r['price_source_type'] or '—'} | {r['confidence']} |")
    (BUILD/'main-table.md').write_text('\n'.join(lines) + '\n')

    conf = {}
    for r in recs: conf[r['confidence']] = conf.get(r['confidence'], 0) + 1
    psrc = {}
    for r in recs: psrc[r['price_source_type'] or 'none'] = psrc.get(r['price_source_type'] or 'none', 0) + 1
    s = [f"# Build summary", '',
         f"- snapshot date: **{snapshot['snapshot_date']}**",
         f"- built from commit: `{sha}` (HEAD at build time — a commit cannot contain its own SHA)",
         f"- **unique_venues: {snapshot['unique_venues']}**  ·  **display_rows: {snapshot['display_rows']}**",
         f"- gates defined: {len(gates['gates'])}",
         f"- published page: **{snapshot.get('distinct_on_page', 0)} distinct venues** / "
         f"{snapshot.get('display_rows_page', 0)} venue links / "
         f"{snapshot.get('in_two_sections', 0)} appearing in more than one section",
         f"- through their gate: **{len(passed)}**",
         '', '## Confidence', '']
    for k in ('high','medium','low'):
        if k in conf: s.append(f"- {k}: {conf[k]}")
    s += ['', '## Price source', '']
    for k, n in sorted(psrc.items(), key=lambda x: -x[1]):
        s.append(f"- {k}: {n}")
    bl = [r for r in recs if r.get('borderline')]
    s += ['', '## Borderline (hard gate passed, small-sample proxy not)', '',
          f"- **{len(bl)} of {len(passed)}** venues through the gate",
          "- `conservative_rating_proxy` is a **heuristic small-sample penalty, not a confidence",
          "  interval**: Google publishes a mean and a count, not the 1-5 vote distribution, so no",
          "  strict interval can be computed from what we have.",
          "- Read this count as: with the gate at 4.7 and ratings rounded to one decimal, most passers",
          "  sit close enough to the line that a modest sample penalty pushes them under. It is a",
          "  prompt to re-check, not a claim that they fail.",
          "- The hard gate stays the reader-facing rule; `shrunk_rating` orders the main table.", '']
    for r in sorted(bl, key=lambda r: r['conservative_rating_proxy'] or 0):
        s.append(f"  - {r['name']}: {r['rating']}/{r['review_count']:,} -> proxy "
                 f"{r['conservative_rating_proxy']} (gate {r['gate_min_rating']})")
    s += ['', '## Two-person totals', '',
          f"- derivable: {sum(1 for r in recs if r['two_person_total_min'] is not None)}",
          f"- à la carte (not derivable): {sum(1 for r in recs if r['price_unit']=='item')}",
          f"- no price recorded: {sum(1 for r in recs if not r['price_unit'])}",
          '', '## Validation', '',
          f"- errors: **{len(errors)}**", f"- warnings: {len(warnings)}", '']
    for w in warnings: s.append(f"  - ⚠ {w}")
    for e in errors: s.append(f"  - ✗ {e}")
    frag = quickpick_html(recs, snapshot)
    (BUILD/'quickpick.html').write_text(frag)
    status = inject(frag, 'quickpick', ROOT/'docs'/'index.html')
    # the cover used to carry a second, hand-kept copy of these numbers that had
    # drifted apart from the generated one; there is now a single source
    counts = ('<span id="counts">独立门店 <b>%d</b> 家 · 门店链接 <b>%d</b> 条 · '
              '出现在一个以上章节 <b>%d</b> 家 · 已迁入结构化数据 <b>%d</b> 家</span>'
              % (snapshot.get('distinct_on_page', 0), snapshot.get('display_rows_page', 0),
                 snapshot.get('in_two_sections', 0), snapshot['unique_venues']))
    status_counts = inject(counts, 'counts', ROOT/'docs'/'index.html')
    print(f'  quick-pick section: {status}')
    print(f'  cover counts: {status_counts}')

    s2 = ['', '## Counts (issue #1: display rows are not unique venues)', '',
          f"- structured dataset — unique_venues: **{snapshot['unique_venues']}**, "
          f"display_rows: {snapshot['display_rows']}, branch_count: {snapshot['branch_count']}",
          f"- published page — display_rows_page: **{snapshot['display_rows_page']}**, "
          f"distinct_on_page: **{snapshot['distinct_on_page']}**, "
          f"repeated_venues: **{snapshot['repeated_venues']}**", '']
    (BUILD/'summary.md').write_text('\n'.join(s) + '\n'.join(s2) + '\n')
    return snapshot, len(passed)

def main():
    global TODAY
    for a in sys.argv[1:]:
        if a.startswith('--today='):
            TODAY = datetime.date.fromisoformat(a.split('=',1)[1])
    gates, venues, sources, aliases, exemptions = load()
    errors, warnings = validate(gates, venues, sources, aliases, exemptions)
    pe, pw = check_page_refs()      # cross-references rot when a section is renamed
    errors.extend(pe); warnings.extend(pw)
    for w in warnings: print(f'warning: {w}')
    for e in errors:   print(f'ERROR:   {e}', file=sys.stderr)
    if '--check' in sys.argv:
        print(f'\n{len(errors)} error(s), {len(warnings)} warning(s)')
        return 1 if errors else 0
    if errors:
        print('\nbuild aborted: fix the errors above', file=sys.stderr); return 1
    recs = derive(gates, venues, aliases)
    snap, npass = emit(recs, gates, sources, errors, warnings)
    print(f"\nbuilt: {snap['unique_venues']} unique venues / {snap['display_rows']} rows, "
          f"{npass} through their gate, snapshot {snap['snapshot_date']} @ {snap['commit']}")
    print('  build/venues.json  build/venues.csv  build/main-table.md  build/summary.md')
    print('  docs/data/venues.json  docs/data/venues.csv')
    return 0

if __name__ == '__main__':
    sys.exit(main())
