fix-python:
	ruff check --fix **/*.py

check-config:
	@echo "Checking configuration system..."
	@python -c "from config_loader import load_config; config = load_config(); print('Configuration loaded successfully')"
	@echo "Configuration system check passed!"

check-python:
	ruff check **/*.py

check-scad:
	uv run sca2d .

check: check-python check-config check-scad

test:
	python -m unittest discover tests/ -v

.PHONY: check check-python check-config check-scad test
