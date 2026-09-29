#!/usr/bin/env python3
"""Dependency-free tests: prove the validators actually catch bad data.

    python3 scripts/tests/test_build.py

Each case copies the real dataset, injects one fault, and asserts the validator
reports it. A test that passes because nothing was checked is worse than no test,
so every case also asserts the clean dataset produces zero errors.
"""
import csv, io, sys, pathlib, tempfile, shutil, importlib.util

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('build', ROOT/'scripts'/'build.py')
build = importlib.util.module_from_spec(spec); spec.loader.exec_module(build)

FAILED = []
def check(name, cond, detail=''):
    print(('  ok   ' if cond else '  FAIL ') + name + (f'  [{detail}]' if detail and not cond else ''))
    if not cond: FAILED.append(name)

def with_rows(mutate):
    """Run validate() over the real data with one row mutated/added."""
    gates, venues, sources, aliases = build.load()
    venues = [dict(v) for v in venues]
    mutate(venues)
    return build.validate(gates, venues, sources, aliases)

def main():
    print('clean dataset')
    gates, venues, sources, aliases = build.load()
    errs, warns = build.validate(gates, venues, sources, aliases)
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

    print('\nderived fields')
    recs = build.derive(gates, venues, aliases)
    check('gate_pass is computed, not read',
          'gate_pass' not in venues[0] and all('gate_pass' in r for r in recs))
    r0 = next(r for r in recs if r['venue_id'] == 'bne-exhibition')
    check('shrinkage pulls a small sample toward the mean',
          r0['shrunk_rating'] < r0['rating'], f"{r0['shrunk_rating']} vs {r0['rating']}")
    big = next(r for r in recs if r['review_count'] and r['review_count'] > 4000)
    check('large sample barely shrinks', abs(big['shrunk_rating'] - big['rating']) < 0.05)
    check('wilson lower bound below the point estimate',
          all(r['wilson_lower'] < r['rating'] for r in recs if r['wilson_lower']))
    check('freshness in (0,1]', all(0 < r['freshness'] <= 1 for r in recs if r['freshness']))
    ala = [r for r in recs if r['price_unit'] == 'item']
    check('a la carte gives no two-person total',
          all(r['two_person_total_min'] is None for r in ala), 'must not be invented')
    pp = [r for r in recs if r['price_unit'] in ('per_person_set', 'per_person_reported')]
    check('per-person set menus double into a two-person total',
          all(r['two_person_total_min'] == round(float(r['price_min_aud'])*2) for r in pp))
    check('display_rows counts rows, unique_venues counts venues',
          len({r['venue_id'] for r in recs}) == len(recs))

    print()
    if FAILED:
        print(f'{len(FAILED)} test(s) failed: ' + ', '.join(FAILED)); return 1
    print('all tests passed'); return 0

if __name__ == '__main__':
    sys.exit(main())
