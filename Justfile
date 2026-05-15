default:
    just --list

lint:
    uv run ruff check --fix
    uv run ruff format
    uv run ty check

tests:
    uv run pytest
