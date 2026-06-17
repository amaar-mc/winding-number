# winding-number

Pure-Python winding-number computation and point-in-polygon test for arbitrary
(non-convex, self-intersecting) polygons. Zero runtime dependencies.

## Commands

- Create env and install: `uv venv && uv pip install -e ".[dev]"`
- Test: `uv run pytest -q`
- Lint: `uv run ruff check .` (format with `uv run ruff format .`)
- Types: `uv run mypy src`
- Build: `uv build` (then `uv run --with twine twine check dist/*` before publishing)

## Architecture

`src/winding_number/`:
- `_core.py`: `winding_number` and `point_in_polygon` (Sunday's algorithm with isLeft).
- `_geometry.py`: `signed_area`, `orientation`, `is_convex` (shoelace + cross products).
- `__init__.py`: public surface.

See `docs/architecture.md` for the precise algorithm, isLeft derivation, on-edge
convention, and references (Sunday, Shimrat).

## Conventions

- A point is `tuple[float, float]`; a polygon is `Sequence[tuple[float, float]]`.
- All parameters are explicit with no default values.
- Validate inputs and raise clear ValueError messages.
- Pure functions, strict typing, zero runtime dependencies (standard library only).
- On-edge: non-horizontal edge points are inside; horizontal edge points are outside.

## Testing rules

- Golden values for both CCW and CW squares, triangle, and L-shape.
- Hypothesis property tests: `point_in_polygon(P) == (winding_number(P) != 0)` for
  sampled bounding-box points across all test polygons.
- Bug fixes start with a failing test.

## Release

- Semantic versioning; update CHANGELOG.md and __version__.
- Gates: `uv run pytest && uv run ruff check . && uv run mypy src && uv build && uv run --with twine twine check dist/*`.
- Do NOT publish to PyPI (pending quota reset). Tag vX.Y.Z and GitHub release.

## Style

- No em dash characters in docs, comments, or commit messages.
- Comments explain non-obvious reasoning only.
- No TODO or FIXME in committed code.
