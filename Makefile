.PHONY: all build check test maps clean

all: check build

build:            ## data -> gates -> build/ and docs/data/
	python3 scripts/build.py

check:            ## validate only; non-zero exit on any error
	python3 scripts/build.py --check

test:             ## prove the validators catch injected faults
	python3 scripts/tests/test_build.py

maps:             ## re-render the OSM maps (needs Pillow + network)
	python3 scripts/build_brisbane_dining_map.py

clean:
	rm -rf build
