# Architecture

`winding-number` is a collection of pure functions for computational geometry.
There are zero runtime dependencies; only the Python standard library is used.
A point is `tuple[float, float]` and a polygon is `Sequence[tuple[float, float]]`.

## Module layout

- `_core.py`: `winding_number` and `point_in_polygon` (Sunday's algorithm with isLeft).
- `_geometry.py`: `signed_area`, `orientation`, and `is_convex` (shoelace + cross products).
- `__init__.py`: public surface; re-exports all five functions.

## The winding number

The **winding number** `wn(P, C)` of a closed curve `C` around a point `P` is the
integer number of complete counterclockwise turns that `C` makes around `P`. For a
polygon, `wn = 0` means `P` is outside (nonzero rule); `wn != 0` means `P` is inside.
A simple CCW polygon gives `wn = +1` for interior points; a CW polygon gives `wn = -1`.

## Sunday's algorithm

The implementation follows Dan Sunday's ray-independent winding-number algorithm
(see references). Instead of casting a ray and counting crossings, the algorithm
sums signed crossing contributions along the directed edges of the polygon.

### isLeft cross product

For directed edge `v0 -> v1` and query point `P`, define:

```
isLeft(v0, v1, P) = (v1.x - v0.x) * (P.y - v0.y) - (P.x - v0.x) * (v1.y - v0.y)
```

This is the z-component of the cross product `(v1 - v0) x (P - v0)`, which equals
twice the signed area of the triangle `(v0, v1, P)`:

- `isLeft > 0`: P is strictly to the left of v0->v1 (CCW turn).
- `isLeft = 0`: P is exactly on the infinite line through v0 and v1 (collinear).
- `isLeft < 0`: P is strictly to the right (CW turn).

### Crossing rule

For each directed edge `(v[i], v[i+1])` (with the last edge closing back to `v[0]`):

1. **Upward crossing** (`v[i].y <= P.y < v[i+1].y`): the edge crosses the horizontal
   ray leftward. If `isLeft(v[i], v[i+1], P) > 0` (P is to the left, edge is to the
   right of P), increment `wn` by +1. If `isLeft = 0`, P is on the line.
2. **Downward crossing** (`v[i+1].y <= P.y < v[i].y`): the edge crosses rightward.
   If `isLeft(v[i], v[i+1], P) < 0` (P is to the right, edge is to the left), decrement
   `wn` by 1. If `isLeft = 0`, P is on the line.

The half-open interval tests (`<=` on one side, `<` on the other) ensure each
horizontal level is owned by exactly one endpoint, so each crossing is counted exactly
once regardless of where the query point lies relative to a vertex.

## On-edge convention

**Chosen convention: a point on a non-horizontal polygon edge is counted as inside.**

When `isLeft = 0` and the edge is non-horizontal, the point lies on the infinite line
through the edge. With the half-open intervals:

- For an upward crossing: the test uses `isLeft >= 0`, so `isLeft = 0` contributes
  `+1` to the winding number.
- For a downward crossing: the test uses `isLeft <= 0`, so `isLeft = 0` contributes
  `-1` to the winding number.

In both cases the collinear point gets a non-zero winding number (the same as a
nearby interior point), so `point_in_polygon` returns `True`.

**Horizontal edges:** A point on a horizontal edge (`v[i].y == v[i+1].y == P.y`) is
not covered by either half-open interval test (the upward test requires `v[i].y <= P.y
< v[i+1].y` but the two y-values are equal, so neither condition fires). Such a point
falls through with winding number 0 and is counted as **outside**.

This convention is:
- Consistent with the standard numerical approach to the winding number.
- Deterministic: no perturbation or epsilon is needed.
- Documented precisely here so consumers can rely on it.

**Summary:**

| Position | Winding number | point_in_polygon |
|---|---|---|
| Strictly inside | +1 (CCW) or -1 (CW) | True |
| Strictly outside | 0 | False |
| On a non-horizontal edge | +1 or -1 | True |
| On a horizontal edge | 0 | False |
| On a vertex (non-horizontal edges adjacent) | +1 or -1 | True |

## Nonzero rule vs. even-odd rule

`point_in_polygon` uses the **nonzero rule**: inside iff `winding_number != 0`.

An alternative is the **even-odd rule**: inside iff the winding number is odd. For
simple (non-self-intersecting) polygons the two rules give identical results. They
diverge on self-intersecting polygons: with the even-odd rule, regions wound twice
are outside; with the nonzero rule they are inside. This library implements the nonzero
rule because the winding number is directly available and is the more robust choice for
non-convex or complex polygons.

To apply the even-odd rule, use: `winding_number(point, polygon) % 2 != 0`.

## Signed area (shoelace formula)

`signed_area` computes the signed area via the shoelace (Gauss) formula:

```
A = 0.5 * sum_i (x_i * y_{i+1} - x_{i+1} * y_i)
```

Positive for CCW, negative for CW. The formula generalizes to non-convex polygons;
for self-intersecting polygons it yields the net signed area.

## Orientation

`orientation` returns "CCW" if `signed_area > 0`, "CW" if `signed_area < 0`, and
raises `ValueError` for degenerate (zero-area) polygons.

## Convexity

`is_convex` tests that all cross products of consecutive edge pairs have the same sign.
A zero cross product (collinear consecutive edges) is permitted.

## References

- Sunday, D. (2001). Winding number algorithm.
  http://geomalgorithms.com/a03-_inclusion.html
- Shimrat, M. (1962). Algorithm 112: Position of point relative to polygon.
  Communications of the ACM, 5(8), 434.
- O'Rourke, J. (1994). Computational Geometry in C. Cambridge University Press.
