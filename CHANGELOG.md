# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- PyPI release (pending quota reset)

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
