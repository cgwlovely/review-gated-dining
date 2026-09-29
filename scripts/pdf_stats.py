#!/usr/bin/env python3
"""Report what is actually in the built PDF, so no document has to hard-code it.

    python3 scripts/pdf_stats.py            # human-readable
    python3 scripts/pdf_stats.py --check    # non-zero exit if a page is near-blank

Counts come from the file itself. Written because METHOD.md and both READMEs
carried "45-page PDF, 389 clickable links" long after the PDF had grown past it.
"""
import argparse, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDF = ROOT/'docs'/'pdf'/'Brisbane_2026_餐厅指南.pdf'
# a page holding less than this much text and no image is a stranded fragment
MIN_TEXT = 300


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true',
                    help='exit non-zero if any page is near-blank')
    args = ap.parse_args()

    if not PDF.exists():
        print('%s not built' % PDF.relative_to(ROOT), file=sys.stderr)
        return 2
    raw = PDF.read_bytes()

    try:
        import fitz
    except ImportError:
        # no PyMuPDF: the object counts alone still beat a hard-coded number
        print('pages  %d' % len(re.findall(rb'/Type\s*/Page[^s]', raw)))
        print('links  %d' % len(re.findall(rb'/Subtype\s*/Link', raw)))
        print('size   %.1f MB' % (len(raw)/1e6))
        print('(install PyMuPDF for the near-blank page check)')
        return 0

    doc = fitz.open(PDF)
    thin = [i for i, p in enumerate(doc, 1)
            if len(p.get_text().strip()) < MIN_TEXT and not p.get_images()]
    print('pages  %d' % doc.page_count)
    print('links  %d' % len(re.findall(rb'/Subtype\s*/Link', raw)))
    print('size   %.1f MB' % (len(raw)/1e6))
    print('near-blank pages (<%d chars, no image)  %d%s'
          % (MIN_TEXT, len(thin), ('  ' + str(thin)) if thin else ''))
    if args.check and thin:
        print('\nnear-blank pages are stranded section tails - check the print CSS',
              file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
