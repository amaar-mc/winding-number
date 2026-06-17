# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- PyPI release (pending quota reset; new-project quota was exhausted at v0.1.0 and has not
  yet reset; builds pass twine check and are ready to upload once the window clears)

## [0.2.0] - 2026-06-17

### Added
- `crossing_number(point, polygon)` -> int: counts rightward ray crossings using the
  PNPOLY half-open edge convention (one endpoint strictly above the ray, the other
  at-or-below), ensuring each vertex is owned by exactly one incident edge.
- `point_in_polygon_even_odd(point, polygon)` -> bool: even-odd (alternating) fill rule;
  inside iff `crossing_number` is odd.
- Both new functions are exported from `winding_number` and validated the same way as
  existing functions (ValueError for fewer than 3 vertices, no default params).
- New test module `tests/test_even_odd.py` with golden crossing_number values, agreement
  tests for simple polygons, and the canonical pentagram disagreement case: the pentagram
  center has winding number -2 (inside by the nonzero rule) and crossing number 2 (outside
  by the even-odd rule).  Hypothesis property tests verify the two rules agree on all
  strictly interior and exterior points of convex polygons.

## [0.1.0] - 2026-06-17

### Added
- `winding_number(point, polygon)`: signed winding number via Sunday's ray-independent
  algorithm with the isLeft cross-product test.
- `point_in_polygon(point, polygon)`: nonzero rule, True iff `winding_number != 0`.
- `signed_area(polygon)`: shoelace formula; positive for CCW, negative for CW.
- `orientation(polygon)`: returns "CCW" or "CW"; raises ValueError for degenerate
  zero-area polygons.
- `is_convex(polygon)`: cross-product sign consistency test for all edge pairs.
- Deterministic on-edge handling: non-horizontal edge points are inside; horizontal
  edge points are outside.
- Full test suite with golden values, structural invariants, and Hypothesis property tests.
