check-python:
	ruff check **/*.py

check-scad:
	uv run scad2 .

check: check-python check-scad

test:
	python -m unittest discover tests/ -v

test-unit:
	python -m unittest discover tests/ -v

.PHONY: check check-python check-scad test test-unit
