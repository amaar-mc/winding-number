# winding-number

[![CI](https://github.com/amaar-mc/winding-number/actions/workflows/ci.yml/badge.svg)](https://github.com/amaar-mc/winding-number/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

Winding number and point-in-polygon for arbitrary (non-convex, self-intersecting) polygons.
Pure Python, zero dependencies.

## What is the winding number?

The **winding number** of a closed polygon around a point is the integer count of how many
times the polygon winds around that point. A CCW polygon around an interior point has
winding number +1; a CW polygon gives -1; an exterior point gives 0.

This is the basis of the **nonzero rule**: a point is inside iff `winding_number != 0`. The
nonzero rule works correctly for non-convex and self-intersecting polygons, unlike simple
ray-casting (which can misclassify points in self-intersecting regions).

## Why zero-dependency vs. shapely or matplotlib?

The correct alternatives require heavy C extensions:

- `shapely.geometry.Point.within(polygon)` requires shapely, which depends on GEOS (a C/C++ library).
- `matplotlib.path.Path.contains_point` pulls in all of matplotlib (rendering, fonts, backends).

This library implements Sunday's winding-number algorithm in pure Python with zero runtime
dependencies. No compilation, no GEOS, no plotting overhead.

## Install

```sh
pip install winding-number
```

> PyPI release pending. Install from source in the meantime:
> ```sh
> git clone https://github.com/amaar-mc/winding-number
> cd winding-number
> pip install -e .
> ```

## Quick start

```python
from winding_number import winding_number, point_in_polygon, signed_area, orientation, is_convex

# CCW unit square.
square = [(1, -1), (1, 1), (-1, 1), (-1, -1)]

winding_number((0, 0), square)      # 1  (inside, CCW)
winding_number((2, 0), square)      # 0  (outside)
point_in_polygon((0, 0), square)    # True
point_in_polygon((2, 0), square)    # False

signed_area(square)                 # 4.0  (positive = CCW)
orientation(square)                 # "CCW"
is_convex(square)                   # True

# Non-convex L-shape.
l_shape = [(0,0),(2,0),(2,1),(1,1),(1,2),(0,2)]
is_convex(l_shape)                  # False
point_in_polygon((1.0, 0.5), l_shape)  # True  (inside the bottom bar)
point_in_polygon((1.5, 1.5), l_shape) # False (the notch)
```

## API

| Function | Description |
|---|---|
| `winding_number(point, polygon)` | Signed winding number (Sunday's algorithm with isLeft) |
| `point_in_polygon(point, polygon)` | True iff `winding_number != 0` (nonzero rule) |
| `signed_area(polygon)` | Shoelace formula; positive = CCW, negative = CW |
| `orientation(polygon)` | "CCW" or "CW"; raises ValueError on degenerate zero-area polygon |
| `is_convex(polygon)` | True iff all edge-pair cross products share the same sign |

A `point` is `tuple[float, float]` and a `polygon` is `Sequence[tuple[float, float]]`.
All functions raise `ValueError` if the polygon has fewer than 3 vertices.

### On-edge convention

A point exactly on a non-horizontal polygon edge is counted as **inside**
(`winding_number` returns +/-1). A point on a horizontal edge is counted as **outside**
(winding number 0). This is deterministic and requires no epsilon. See
[docs/architecture.md](docs/architecture.md) for the full derivation.

## License

MIT. Copyright (c) 2026 Amaar Chughtai.
