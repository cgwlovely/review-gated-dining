#!/usr/bin/env python3
"""Emit a Frictionless Data Package descriptor for data/, derived from the CSVs.

    python3 scripts/make_datapackage.py           # write datapackage.json
    python3 scripts/make_datapackage.py --check   # non-zero exit if it is out of date

The descriptor is GENERATED, never hand-edited: a hand-written schema drifts from
the data the first time a column is added. Field types are inferred from the values
actually present, and field descriptions come from data/field_notes.csv where one
is recorded, so the meaning of a column lives next to the data rather than in prose.
"""
import argparse, csv, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT/'data'
OUT = ROOT/'datapackage.json'

RESOURCES = [
    ('venues',              'venues.csv',              'One row per venue: identity, rating, price and its source.'),
    ('sources',             'sources.csv',             'Every external source the dataset draws on, with its licence.'),
    ('venue_aliases',       'venue_aliases.csv',       'Alternate names a venue is listed under elsewhere.'),
    ('scenario_exemptions', 'scenario_exemptions.csv', 'Deliberate exceptions to the scenario/cuisine rule, each with a reason.'),
]

INT = re.compile(r'^-?\d+$')
NUM = re.compile(r'^-?\d+(\.\d+)?$')
DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def infer(values):
    vals = [v for v in values if v not in ('', None)]
    if not vals:
        return 'string'
    if all(DATE.match(v) for v in vals):
        return 'date'
    if all(INT.match(v) for v in vals):
        return 'integer'
    if all(NUM.match(v) for v in vals):
        return 'number'
    if all(v.lower() in ('true', 'false', 'yes', 'no', '0', '1') for v in vals):
        return 'boolean'
    return 'string'


def field_notes():
    f = DATA/'field_notes.csv'
    if not f.exists():
        return {}
    with f.open(encoding='utf-8') as fh:
        return {(r['resource'], r['field']): r['description'] for r in csv.DictReader(fh)}


def build():
    notes = field_notes()
    resources = []
    for name, fname, desc in RESOURCES:
        path = DATA/fname
        if not path.exists():
            continue
        with path.open(encoding='utf-8') as fh:
            rows = list(csv.DictReader(fh))
        cols = list(rows[0].keys()) if rows else []
        fields = []
        for c in cols:
            f = {'name': c, 'type': infer([r[c] for r in rows])}
            if (name, c) in notes:
                f['description'] = notes[(name, c)]
            fields.append(f)
        resources.append({
            'name': name,
            'path': 'data/' + fname,
            'profile': 'tabular-data-resource',
            'format': 'csv', 'mediatype': 'text/csv', 'encoding': 'utf-8',
            'description': desc,
            'schema': {'fields': fields,
                       **({'primaryKey': 'venue_id'} if name == 'venues' else {})},
            'rowCount': len(rows),
        })
    return {
        'profile': 'tabular-data-package',
        'name': 'review-gated-dining-brisbane',
        'title': 'Review-gated dining — Brisbane',
        'description': ('Venues that clear a stated review gate, with every rating and price '
                        'carrying the platform and date it was observed on. Gates and their '
                        'rationale live in data/gates.yml. The MIT licence covers this compilation '
                        'only: upstream terms differ per source and are recorded in the `sources` '
                        'resource - one of them explicitly forbids redistribution, so ratings are '
                        'stored as dated observations with attribution, not republished in bulk.'),
        'homepage': 'https://cgwlovely.github.io/review-gated-dining/',
        'licenses': [{'name': 'MIT',
                      'path': 'https://opensource.org/licenses/MIT',
                      'title': 'MIT License (this compilation; see `sources` for upstream terms)'}],
        'contributors': [{'title': 'review-gated-dining maintainers',
                          'path': 'https://github.com/cgwlovely/review-gated-dining',
                          'role': 'author'}],
        'sources': sources_list(),
        'resources': resources,
    }


def sources_list():
    f = DATA/'sources.csv'
    if not f.exists():
        return []
    out = []
    with f.open(encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            s = {'title': r.get('name') or r.get('source') or r.get('title') or 'source'}
            for k in ('url', 'homepage', 'link'):
                if r.get(k):
                    s['path'] = r[k]; break
            if r.get('licence') or r.get('license'):
                s['licence'] = r.get('licence') or r.get('license')
            out.append(s)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    text = json.dumps(build(), indent=2, ensure_ascii=False) + '\n'
    if args.check:
        current = OUT.read_text(encoding='utf-8') if OUT.exists() else ''
        if current != text:
            print('datapackage.json is out of date - run: make datapackage', file=sys.stderr)
            return 1
        print('datapackage.json is up to date')
        return 0
    OUT.write_text(text, encoding='utf-8')
    d = json.loads(text)
    print('wrote %s: %d resources, %d fields, %d sources'
          % (OUT.name, len(d['resources']),
             sum(len(r['schema']['fields']) for r in d['resources']), len(d['sources'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
