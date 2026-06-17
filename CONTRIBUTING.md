# Contributing to winding-number

Thanks for your interest. This project values correctness, precise definitions, and zero
runtime dependencies.

## Development

```sh
uv venv
uv pip install -e ".[dev]"
uv run pytest -q
uv run ruff check .
uv run mypy src
```

A standard virtual environment with `pip install -e ".[dev]"` works the same way.

## Guidelines

- No runtime dependencies. The standard library is enough.
- Functions are pure. All parameters are explicit with no default values.
- Every function needs exact-value tests plus property-based tests (Hypothesis).
- A bug fix starts with a failing test.
- Run `uv run ruff format .` before committing.
- Commit messages follow `type(scope): description`.
- No em dash characters in code, comments, or commit messages.
- No TODO or FIXME in committed code; implement it or note the skip explicitly.

## Reporting issues

Open an issue with the polygon vertices, the function called, and what you expected
versus what you observed.
