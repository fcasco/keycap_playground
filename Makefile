build-numbers:
	python -m src --config configs/numbers.toml

check-python:
	ruff check src/*.py

check-types:
	uv run ty check src

check-scad:
	uv run sca2d .

check: check-python check-types check-scad

fix-python:
	ruff check --fix src/*.py

test:
	python -m unittest discover tests/ -v

.PHONY: check check-python check-scad check-types test
