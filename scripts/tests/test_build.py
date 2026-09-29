#!/usr/bin/env python3
"""Dependency-free tests: prove the validators actually catch bad data.

    python3 scripts/tests/test_build.py

Each case copies the real dataset, injects one fault, and asserts the validator
reports it. A test that passes because nothing was checked is worse than no test,
so every case also asserts the clean dataset produces zero errors.
"""
import csv, io, json, sys, pathlib, tempfile, shutil, importlib.util

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('build', ROOT/'scripts'/'build.py')
build = importlib.util.module_from_spec(spec); spec.loader.exec_module(build)

FAILED = []
def check(name, cond, detail=''):
    print(('  ok   ' if cond else '  FAIL ') + name + (f'  [{detail}]' if detail and not cond else ''))
    if not cond: FAILED.append(name)

def with_rows(mutate):
    """Run validate() over the real data with one row mutated/added."""
    gates, venues, sources, aliases, exemptions = build.load()
    venues = [dict(v) for v in venues]
    mutate(venues)
    return build.validate(gates, venues, sources, aliases, exemptions)

def main():
    print('clean dataset')
    gates, venues, sources, aliases, exemptions = build.load()
    errs, warns = build.validate(gates, venues, sources, aliases, exemptions)
    check('no errors on the committed data', errs == [], f'{errs[:2]}')
    check('at least one venue loaded', len(venues) > 0)

    print('\ninjected faults must be caught')
    e, _ = with_rows(lambda vs: vs.append(dict(vs[0])))
    check('duplicate venue_id', any('duplicate venue_id' in x for x in e))

    def dup_place(vs):
        vs[0]['google_place_id'] = 'ChIJtest'; vs[1] = dict(vs[1]); vs[1]['google_place_id'] = 'ChIJtest'
    e, _ = with_rows(dup_place)
    check('duplicate google_place_id', any('already used by' in x for x in e))

    e, _ = with_rows(lambda vs: vs[0].update(rating_source=''))
    check('rating without a platform label', any('rating_source' in x for x in e))

    e, _ = with_rows(lambda vs: vs[0].update(rating_observed_at=''))
    check('rating without an observation date', any('rating_observed_at' in x for x in e))

    e, _ = with_rows(lambda vs: vs[0].update(price_unit=''))
    check('price without a unit', any('price_unit missing' in x for x in e))

    e, _ = with_rows(lambda vs: vs[0].update(price_source_type=''))
    check('price without a source type', any('price_source_type missing' in x for x in e))

    e, _ = with_rows(lambda vs: vs[0].update(price_observed_at=''))
    check('price without an observation date', any('price_observed_at' in x for x in e))

    e, _ = with_rows(lambda vs: vs[0].update(price_unit='per_head'))
    check('unknown price unit', any('unknown price_unit' in x for x in e))

    e, _ = with_rows(lambda vs: vs[0].update(gate_name='does_not_exist'))
    check('unknown gate name', any('unknown gate_name' in x for x in e))

    e, _ = with_rows(lambda vs: vs[0].update(status='maybe'))
    check('unknown status', any('unknown status' in x for x in e))

    e, _ = with_rows(lambda vs: vs[0].update(review_count=''))
    check('rating present but review_count missing', any('review_count missing' in x for x in e))

    _, w = with_rows(lambda vs: vs[0].update(rating_observed_at='2024-01-01'))
    check('stale observation warns', any('days old' in x for x in w))

    print('\nscenario / cuisine consistency (issue #1 review)')
    def thai_claims_chinese(vs):
        r = next(v for v in vs if v['venue_id'] == 'bne-short-grain')
        r['scenarios'] = 'date;chinese_food'
    e, _ = with_rows(thai_claims_chinese)
    check('a thai venue cannot claim the chinese_food scenario',
          any('claims a cuisine the venue does not have' in x for x in e))
    # A membership assertion would pass even if the exemption mechanism were broken.
    # Drop the exemption -> must error; restore it -> must not.
    g2, v2, s2, a2, ex2 = build.load()
    without = {k: v for k, v in ex2.items() if k != ('bne-longwang', 'chinese_food')}
    e_wo, _ = build.validate(g2, v2, s2, a2, without)
    e_wi, _ = build.validate(g2, v2, s2, a2, ex2)
    check('removing the exemption makes the build fail',
          any('bne-longwang' in x and 'claims a cuisine' in x for x in e_wo),
          f'errors without exemption: {e_wo[:1]}')
    check('restoring the exemption clears it', e_wi == [])
    e, _ = with_rows(lambda vs: vs[0].update(scenarios='brunchy'))
    check('unknown scenario', any('unknown scenario' in x for x in e))

    print('\nbudget bands (issue #1 review)')
    check('every band label says whose price it is and that it is the entry price',
          all(('两人最低' in lab or 'from' in lab.lower()) for _, _, lab in build.BUDGET_BANDS),
          f'labels: {[lab for _, _, lab in build.BUDGET_BANDS]}')
    check('no band label pairs a bound word with 起, which reads as a contradiction',
          not any(('以内起' in lab or '以下起' in lab or '以上起' in lab)
                  for _, _, lab in build.BUDGET_BANDS))
    check('bands are contiguous and ascending',
          all(build.BUDGET_BANDS[i][1] == build.BUDGET_BANDS[i+1][0]
              for i in range(len(build.BUDGET_BANDS)-1)))

    print('\nderived fields')
    recs = build.derive(gates, venues, aliases)
    check('gate_pass is computed, not read',
          'gate_pass' not in venues[0] and all('gate_pass' in r for r in recs))
    r0 = next(r for r in recs if r['venue_id'] == 'bne-exhibition')
    check('shrinkage pulls a small sample toward the mean',
          r0['shrunk_rating'] < r0['rating'], f"{r0['shrunk_rating']} vs {r0['rating']}")
    big = next(r for r in recs if r['review_count'] and r['review_count'] > 4000)
    check('large sample barely shrinks', abs(big['shrunk_rating'] - big['rating']) < 0.05)
    check('conservative proxy sits below the point estimate',
          all(r['conservative_rating_proxy'] < r['rating']
              for r in recs if r['conservative_rating_proxy']))
    check('the proxy is not described as a confidence interval anywhere',
          not any('95%' in (r.get('borderline_reason') or '') for r in recs))
    check('freshness in (0,1]', all(0 < r['freshness'] <= 1 for r in recs if r['freshness']))
    ala = [r for r in recs if r['price_unit'] == 'item']
    check('a la carte gives no two-person total',
          all(r['two_person_total_min'] is None for r in ala), 'must not be invented')
    pp = [r for r in recs if r['price_unit'] == 'per_person_set']
    check('a per-person SET price doubles into a two-person total',
          all(r['two_person_total_min'] == round(float(r['price_min_aud'])*2) for r in pp))
    # a crowd-reported band is not a meal price: doubling $1-20 produced "two people, $2-40"
    rep = [r for r in recs if r['price_unit'] == 'per_person_reported']
    check('a crowd-reported per-person band is NOT doubled into a two-person total',
          all(r['two_person_total_min'] is None for r in rep),
          f'{sum(1 for r in rep if r["two_person_total_min"] is not None)} were doubled')
    check('a venue with no derivable two-person total says why',
          all((r['two_person_basis'] or '').strip()
              for r in recs if r['two_person_total_min'] is None))
    check('venue_id is unique across the dataset',
          len({r['venue_id'] for r in recs}) == len(recs))

    print('\nreview round 4 findings')
    hi = [r for r in recs if r['confidence'] == 'high']
    check('high confidence requires BOTH observations fresh (<=90d)',
          all((r['oldest_observation_days'] or 0) <= 90 for r in hi))

    def stale_price(vs):
        r = next(v for v in vs if v['venue_id'] == 'bne-short-grain')
        r['price_observed_at'] = '2025-01-01'
    g3, v3, a3 = gates, [dict(v) for v in venues], aliases
    stale_price(v3)
    r3 = next(r for r in build.derive(g3, v3, a3) if r['venue_id'] == 'bne-short-grain')
    check('a stale price drags confidence down even when the rating is fresh',
          r3['confidence'] == 'low', f"got {r3['confidence']}")

    def for_two(vs):
        r = next(v for v in vs if v['venue_id'] == 'bne-joy')
        r.update(price_unit='for_two', price_min_aud='200', price_max_aud='260')
    v4 = [dict(v) for v in venues]; for_two(v4)
    r4 = next(r for r in build.derive(gates, v4, aliases) if r['venue_id'] == 'bne-joy')
    check('for_two is not doubled', (r4['two_person_total_min'], r4['two_person_total_max']) == (200, 260))
    check('for_two basis text does not claim x2', 'x2' not in r4['two_person_basis'],
          r4['two_person_basis'])

    e, _ = with_rows(lambda vs: vs[0].update(one_liner_en='trailing comma,'))
    check('a stray trailing comma in a one-liner is rejected',
          any('ends with a stray' in x for x in e))
    check('the committed one-liners are clean',
          all(not (r['one_liner_en'] or '').strip().endswith((',', ';'))
              and not (r['one_liner_zh'] or '').strip().endswith(('，', '；')) for r in recs))

    print('\nreview round 3 findings')
    mir = [r for r in recs if r['rating_source'] == 'google_mirror']
    check('mirror-sourced ratings are confidence=low, as gates.yml states',
          bool(mir) and all(r['confidence'] == 'low' for r in mir),
          f"{len(mir)} mirror rows, confidences={sorted({r['confidence'] for r in mir})}")
    check('cuisines never contain a scenario-only code',
          not any(set(r['cuisines']) & build.SCENARIO_ONLY_CODES for r in recs))
    e, _ = with_rows(lambda vs: vs[0].update(cuisines='chinese_food;italian'))
    check('a scenario code in cuisines is rejected',
          any('cuisines contains scenario code' in x for x in e))
    check('coffee stays legal as a cuisine', 'coffee' not in build.SCENARIO_ONLY_CODES)

    gy = (ROOT/'data'/'gates.yml').read_text()
    main_r = gates['gates']['main']['min_rating']
    for name, g in gates['gates'].items():
        mr = g.get('min_rating')
        if mr is None:
            continue
        txt = (g.get('rationale_en','') + ' ' + g.get('rationale_zh','')).lower()
        if 'goes up' in txt or '上调' in txt or 'not loosened' in txt or '不放宽' in txt:
            check(f'gate {name} claims a tightened bar and delivers one',
                  mr >= main_r, f'min_rating {mr} vs main {main_r}')

    snap = json.loads((ROOT/'build'/'venues.json').read_text())['snapshot']
    check('snapshot display_rows matches the record count', snap['display_rows'] == len(recs))
    check('snapshot unique_venues matches distinct ids',
          snap['unique_venues'] == len({r['venue_id'] for r in recs}))

    frag = (ROOT/'build'/'quickpick.html').read_text()
    import re as _re
    empties = _re.findall(r'本档暂无编辑精选[^<]*</td>', frag)
    spans = _re.findall(r'<td colspan="(\d+)" class="small">本档暂无编辑精选', frag)
    check('empty budget rows span the full table width',
          all(s == '4' for s in spans), f'found colspans {spans or "none"} ({len(empties)} empty bands)')

    gyz = (ROOT/'data'/'gates.yml').read_text()
    check('gates.yml describes freshness as one scalar from the oldest observation',
          'OLDEST observation' in gyz and '最旧' in gyz)

    # --- METHOD gate table must not contradict gates.yml (round-5 P0) ---
    import re as _re2
    main_r = float(_re2.search(r'main:.*?min_rating:\s*([\d.]+)', gyz, _re2.S).group(1))
    # the claim must be the one attached to the RATING bar, not the sample bar
    DIRECTION = {
        # the gap may not step over the *sample* bar on its way to the verb
        'METHOD.md': (r'rating bar(?:(?!sample)[^.|]){0,40}?\b(up|rises|raised)\b'
                      r'|\*\*Not loosened\.\*\*',
                      r'rating bar(?:(?!sample)[^.|]){0,40}?\b(drops|down|lowered)\b'),
        'METHOD.zh.md': (r'评分(?:门槛)?(?:(?!样本)[^。|]){0,12}(?:提高|上调)|不放宽',
                         r'评分(?:门槛)?(?:(?!样本)[^。|]){0,12}(?:降到|下调|放宽)'),
    }
    for doc, (up_re, down_re) in DIRECTION.items():
        text = (ROOT/doc).read_text()
        rows = [l for l in text.splitlines()
                if l.startswith('|') and _re2.search(r'≥\s*([\d.]+)', l) and '---' not in l]
        bad = []
        for line in rows:
            shown = float(_re2.search(r'≥\s*([\d.]+)', line).group(1))
            if _re2.search(up_re, line) and shown < main_r:
                bad.append('claims a raised rating bar but shows %.1f < main %.1f: %s'
                           % (shown, main_r, line[:70]))
            if _re2.search(down_re, line) and shown > main_r:
                bad.append('claims a lowered rating bar but shows %.1f > main %.1f: %s'
                           % (shown, main_r, line[:70]))
        check('%s gate table agrees with gates.yml on which way the rating bar moved' % doc,
              not bad, '; '.join(bad))

    # --- API cost table must be the stated venue count times the stated unit price ---
    for doc in ('METHOD.md', 'METHOD.zh.md'):
        text = (ROOT/doc).read_text()
        n = int(_re2.search(r'7,020', text).group(0).replace(',', ''))
        bad = []
        for line in text.splitlines():
            m = _re2.search(r'US\$(\d+)\s*[/／]\s*1,000.*?≈\s*US\$([\d,]+)', line)
            if not m:
                continue
            unit, shown = int(m.group(1)), int(m.group(2).replace(',', ''))
            want = round(unit * n / 1000)
            if shown != want:
                bad.append('US$%d/1,000 x %d = US$%d, table says US$%d' % (unit, n, want, shown))
        check('%s API cost table is arithmetic on the stated venue count' % doc,
              not bad, '; '.join(bad))

    # --- rank badges must not run into the venue name in the text layer ---
    html = (ROOT/'docs'/'index.html').read_text()
    glued = _re2.findall(r'<span class="pin">\d+</span>(?=\S)', html)
    check('rank badges are separated from the name they precede',
          not glued, '%d badge(s) glued to the following text' % len(glued))

    # --- exactly one booking chip per venue; lead time rides inside it ---
    frag2 = (ROOT/'build'/'quickpick.html').read_text()
    rows2 = _re2.findall(r'<tr>(.*?)</tr>', frag2, _re2.S)
    bad = []
    for tr in rows2:
        bks = _re2.findall(r'<span class="chip bk-[a-z_]+"[^>]*>([^<]*)</span>', tr)
        if len(bks) > 1:
            bad.append('%d booking chips in one row: %s' % (len(bks), bks))
    check('each quick-pick row carries exactly one booking chip', not bad, '; '.join(bad))
    check('the standalone "books ahead" chip is gone from the quick-pick',
          '需提前订位' not in frag2,
          'lead time must ride inside the booking chip, not sit beside it')

    # --- a gate miss is a quiet red dot, never a loud red label ---
    page = (ROOT/'docs'/'index.html').read_text()
    loud = _re2.findall(r'<span class="[^"]*\bwarn\b[^"]*">[^<]*未过[^<]*</span>', page)
    check('gate misses are not rendered as bold red labels',
          not loud, f'{len(loud)} loud label(s), e.g. {loud[:1]}')
    check('the red dot used for gate misses is explained in the legend',
          'class="dot"' in page and 'A red dot marks venues' in page)

    # --- the data package descriptor must describe the CSVs as they are now ---
    import subprocess as _sp
    r = _sp.run([sys.executable, str(ROOT/'scripts'/'make_datapackage.py'), '--check'],
                capture_output=True, text=True)
    check('datapackage.json matches data/*.csv', r.returncode == 0,
          (r.stderr or r.stdout).strip()[:120])
    dp = json.loads((ROOT/'datapackage.json').read_text())
    repo_licence = 'MIT' if 'MIT License' in (ROOT/'LICENSE').read_text() else None
    check('the package licence is the one the repository actually declares',
          dp['licenses'][0]['name'] == repo_licence,
          f"descriptor says {dp['licenses'][0]['name']}, LICENSE says {repo_licence}")
    ven = [r for r in dp['resources'] if r['name'] == 'venues'][0]
    check('every venues.csv column appears in the descriptor',
          {f['name'] for f in ven['schema']['fields']} ==
          set(csv.DictReader((ROOT/'data'/'venues.csv').open(encoding='utf-8')).fieldnames))

    print()
    if FAILED:
        print(f'{len(FAILED)} test(s) failed: ' + ', '.join(FAILED)); return 1
    print('all tests passed'); return 0

if __name__ == '__main__':
    sys.exit(main())
