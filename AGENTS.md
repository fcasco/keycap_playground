# Keycap Playground - Agent Guidelines

## Essential Commands
- `make check` - Run all validation (Python style, types, OpenSCAD)
- `make fix-python` - Auto-fix formatting with ruff
- `make check-python` - Validate Python style
- `make check-types` - Validate Python types with ty
- `make check-scad` - Validate OpenSCAD files
- `make test` - Run all tests
- Single test: `python -m unittest tests.test_keycap.TestKeycap.test_name -v`

## Code Style (ruff + ty)
- Max line length: 96 chars, 4-space indentation
- Import order: stdlib → third-party → local (sorted alphabetically)
- Use ruff for linting/formatting, ty for type checking
- Python >=3.13 supported, requires type annotations
- Custom exceptions inherit from Exception, use """ docstrings
- Class names: PascalCase, functions/variables: snake_case

## OpenSCAD Files
- Use sca2d for validation: `uv run sca2d .`
- OpenSCAD path: `/home/facundo/bin/openscad`
- Keep OpenSCAD constants in `constants.scad`

## Testing & Validation
- Tests use unittest framework in `tests/` directory
- Run single test with specific test method name
- All changes must pass `make check` before committing

