.PHONY: help init update test cov lint

help:
	@echo "Available targets:"
	@echo "  init       - Set up dependencies and pre-commit hooks."
	@echo "  update     - Check outdated dependencies and update hooks."
	@echo "  test       - Run tests with pytest."
	@echo "  cov        - Run tests and generate coverage reports"
	@echo "  lint       - Format and check code."


init:
	uv sync --all-extras
	uv run pre-commit install

update:
	uv sync --upgrade
	uv run pre-commit autoupdate

test:
	uv run pytest

cov:
	uv run coverage run --source=app -m pytest
	uv run coverage report --show-missing
	uv run coverage html

lint:
	uv run ruff format
	uv run ruff check --fix || true
	uv run pyright
