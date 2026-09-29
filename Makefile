.PHONY: all build check test maps pdf-stats datapackage review review-post clean

all: check build

build:            ## data -> gates -> build/ and docs/data/
	python3 scripts/build.py

check:            ## validate only; non-zero exit on any error
	python3 scripts/build.py --check
	python3 scripts/make_datapackage.py --check

test:             ## prove the validators catch injected faults
	python3 scripts/tests/test_build.py

pdf-stats:        ## report the built PDF's real page/link counts; --check fails on blanks
	python3 scripts/pdf_stats.py

datapackage:      ## regenerate the Frictionless descriptor from the CSVs
	python3 scripts/make_datapackage.py

review:           ## ask the external reviewer model to critique HEAD (dry run)
	python3 scripts/review_loop.py --issue 1

review-post:      ## same, but post the review to issue #1
	python3 scripts/review_loop.py --issue 1 --post

maps:             ## re-render the OSM maps (needs Pillow + network)
	python3 scripts/build_brisbane_dining_map.py

clean:
	rm -rf build
