fix-python:
	ruff check --fix src/*.py

check-python:
	ruff check src/*.py

check-scad:
	uv run sca2d .

check: check-python check-scad

test:
	python -m unittest discover tests/ -v

.PHONY: check check-python check-scad test
