# Project Charter

## Mission

`winding-number` provides a correct, well-tested, zero-dependency Python library for
the winding-number computation and point-in-polygon test, supporting arbitrary polygons
including non-convex and self-intersecting shapes.

## Scope

The library covers:
- `winding_number(point, polygon)`: signed winding number via Sunday's algorithm.
- `point_in_polygon(point, polygon)`: nonzero rule, derived from the winding number.
- `signed_area(polygon)`: shoelace formula, positive for CCW.
- `orientation(polygon)`: "CCW" or "CW"; raises on degenerate zero-area polygon.
- `is_convex(polygon)`: cross-product sign consistency test.

Out of scope for the initial release:
- Even-odd rule as a first-class function (users may apply `winding_number % 2 != 0`).
- Polygon clipping, boolean operations, or spatial indexing.
- Floating-point robust arithmetic (e.g., Shewchuk predicates).
- NumPy-accelerated paths.

## Design principles

- Zero runtime dependencies (standard library only).
- Pure functions; strict typing (mypy strict mode).
- A point is `tuple[float, float]`; a polygon is `Sequence[tuple[float, float]]`.
- Deterministic on-edge handling with no epsilon or perturbation. See
  `docs/architecture.md` for the precise convention.
- Clear `ValueError` messages for invalid inputs (fewer than 3 vertices, degenerate
  polygon passed to `orientation`).
- Every function tested with exact golden values and property-based tests.
