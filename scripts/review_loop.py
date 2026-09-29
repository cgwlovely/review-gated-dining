#!/usr/bin/env python3
"""Ask an external reviewer model to critique the current state, and post it to the issue.

    python3 scripts/review_loop.py --issue 1                 # dry run: print, do not post
    python3 scripts/review_loop.py --issue 1 --post          # post the review as a comment
    python3 scripts/review_loop.py --issue 1 --post --watch 900
                                                            # re-run every 15 min

Credentials, first match wins:
    $OPENAI_API_KEY                environment variable
    ~/.config/openai.key           a file containing only the key

Nothing is invented: the prompt is assembled from files in this repo plus the issue
thread. Posted comments are signed so nobody mistakes them for a human review.
No third-party packages.
"""
import argparse, json, os, pathlib, subprocess, sys, time, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODEL = os.environ.get('REVIEW_MODEL', 'gpt-5')
SIGN = ('\n\n---\n*Posted by `scripts/review_loop.py` — an external reviewer model '
        '(`%s`) invoked on the repository state at commit `%s`. Not a human review.*')


def key():
    k = os.environ.get('OPENAI_API_KEY', '').strip()
    if k:
        return k, 'OPENAI_API_KEY'
    f = pathlib.Path.home()/'.config'/'openai.key'
    if f.exists():
        k = f.read_text().strip()
        if k:
            return k, str(f)
    return None, None


def sh(*a, **kw):
    return subprocess.run(a, capture_output=True, text=True, cwd=ROOT, **kw).stdout.strip()


def gather(issue):
    """Everything the reviewer needs, straight from the repo and the issue thread."""
    commit = sh('git', 'rev-parse', '--short', 'HEAD') or 'unknown'
    thread = sh('gh', 'issue', 'view', str(issue), '--json', 'title,body,comments')
    try:
        t = json.loads(thread)
    except json.JSONDecodeError:
        print('could not read the issue - is gh authenticated?', file=sys.stderr)
        sys.exit(2)
    convo = [f"# Issue: {t['title']}\n\n{t['body']}"]
    for c in t['comments']:
        convo.append(f"\n\n## Comment by @{c['author']['login']} ({c['createdAt']})\n\n{c['body']}")

    def read(p, limit=None):
        f = ROOT/p
        if not f.exists():
            return f'({p} missing)'
        s = f.read_text()
        return s if limit is None or len(s) <= limit else s[:limit] + f'\n...[truncated, {len(s)} chars total]'

    files = {
        'data/gates.yml': read('data/gates.yml'),
        'data/venues.csv': read('data/venues.csv'),
        'data/scenario_exemptions.csv': read('data/scenario_exemptions.csv'),
        'build/summary.md': read('build/summary.md'),
        'build/main-table.md': read('build/main-table.md'),
        'scripts/build.py': read('scripts/build.py', 24000),
        'scripts/tests/test_build.py': read('scripts/tests/test_build.py', 12000),
    }
    checks = subprocess.run([sys.executable, 'scripts/build.py', '--check'],
                            capture_output=True, text=True, cwd=ROOT)
    tests = subprocess.run([sys.executable, 'scripts/tests/test_build.py'],
                           capture_output=True, text=True, cwd=ROOT)
    return commit, '\n'.join(convo), files, checks.stdout[-3000:], tests.stdout[-3000:]


PROMPT = """You are reviewing a public repository that turns restaurant shortlists into a
reproducible, auditable dataset. You have reviewed it before; the thread below is the full
history, including your own earlier comments and the maintainer's replies.

Review the CURRENT state at commit {commit}. Be specific and adversarial in the way a careful
engineer is: prefer a small number of concrete, checkable defects over general advice.

Ground rules:
- Only raise something you can point at in the supplied files or output. No speculation.
- Say plainly when a previous finding is now fixed - do not re-litigate settled points.
- Prioritise: P0 = wrong or misleading to a reader; P1 = weakens the method; P2 = nice to have.
- For every finding give: what is wrong, where, why it matters, and a check that would catch it.
- If you find nothing at a level, say so rather than padding.
- Write in Chinese, using the same section style as the earlier comments in the thread.
- End with a short list of closing conditions for this issue.

=== ISSUE THREAD ===
{thread}

=== VALIDATOR OUTPUT (make check) ===
{checks}

=== TEST OUTPUT (make test) ===
{tests}

=== REPOSITORY FILES ===
{files}
"""


def call(api_key, prompt):
    req = urllib.request.Request(
        'https://api.openai.com/v1/responses',
        data=json.dumps({'model': MODEL, 'input': prompt}).encode(),
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            body = json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:400]
        print(f'API error {e.code}: {detail}', file=sys.stderr)
        sys.exit(3)
    if 'output_text' in body:
        return body['output_text']
    chunks = []
    for item in body.get('output', []):
        for c in item.get('content', []):
            if c.get('type') in ('output_text', 'text') and c.get('text'):
                chunks.append(c['text'])
    if not chunks:
        print('unexpected API response shape:', json.dumps(body)[:400], file=sys.stderr)
        sys.exit(3)
    return '\n'.join(chunks)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--issue', type=int, default=1)
    ap.add_argument('--post', action='store_true', help='post the review as an issue comment')
    ap.add_argument('--watch', type=int, metavar='SECONDS',
                    help='re-run on an interval instead of once')
    a = ap.parse_args()

    api_key, where = key()
    if not api_key:
        print('No API key found.\n'
              '  export OPENAI_API_KEY=...            (add it to your shell profile to persist)\n'
              '  or write the key to ~/.config/openai.key\n'
              'Then re-run. Nothing was sent.', file=sys.stderr)
        return 2
    print(f'using key from {where}, model {MODEL}')

    while True:
        commit, thread, files, checks, tests = gather(a.issue)
        blob = '\n\n'.join(f'----- {k} -----\n{v}' for k, v in files.items())
        prompt = PROMPT.format(commit=commit, thread=thread, checks=checks, tests=tests, files=blob)
        print(f'prompt {len(prompt):,} chars · commit {commit} · calling {MODEL} …')
        review = call(api_key, prompt) + (SIGN % (MODEL, commit))
        out = ROOT/'build'/f'review-{commit}.md'
        out.parent.mkdir(exist_ok=True)
        out.write_text(review)
        print(f'review saved to {out.relative_to(ROOT)} ({len(review):,} chars)')
        if a.post:
            r = subprocess.run(['gh', 'issue', 'comment', str(a.issue), '--body-file', str(out)],
                               capture_output=True, text=True, cwd=ROOT)
            print(r.stdout.strip() or r.stderr.strip())
        else:
            print('\n' + '=' * 70 + '\n' + review[:2000] + '\n' + '=' * 70)
            print('(dry run — pass --post to publish)')
        if not a.watch:
            return 0
        print(f'sleeping {a.watch}s\n')
        time.sleep(a.watch)


if __name__ == '__main__':
    sys.exit(main())
