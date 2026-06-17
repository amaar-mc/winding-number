"""Winding-number computation and point-in-polygon test using Sunday's algorithm.

The winding number counts the number of times a polygon winds around a point.
A non-zero winding number means the point is inside (the nonzero rule).

On-edge convention: a point exactly on a polygon edge produces a winding
number of 1 (for a CCW polygon) or -1 (for a CW polygon), so it is treated
as inside by ``point_in_polygon``. See docs/architecture.md for the precise
derivation.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeAlias

Point: TypeAlias = tuple[float, float]
Polygon: TypeAlias = Sequence[tuple[float, float]]


def _is_left(p0: Point, p1: Point, p2: Point) -> float:
    """Return the signed area of the triangle (p0, p1, p2) times two.

    Positive means p2 is strictly to the left of the directed line p0 -> p1.
    Zero means p2 is exactly on the line.
    Negative means p2 is to the right.

    This is the cross product (p1 - p0) x (p2 - p0).
    """
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])


def winding_number(point: Point, polygon: Polygon) -> int:
    """Return the winding number of ``polygon`` around ``point``.

    The winding number counts (with sign) how many full counterclockwise turns
    the polygon makes around the point. Positive means net CCW rotation;
    negative means net CW rotation; zero means the point is outside under the
    nonzero rule.

    Uses Dan Sunday's ray-independent algorithm with the isLeft cross-product
    test. The algorithm processes each directed edge (v[i], v[i+1]) and sums
    crossing contributions:
    - An upward crossing (v[i].y <= point.y < v[i+1].y) that passes strictly
      to the right of point contributes +1.
    - A downward crossing (v[i+1].y <= point.y < v[i].y) that passes strictly
      to the left of point contributes -1.

    On-edge handling: when isLeft returns exactly 0 the point lies on the
    infinite line through the edge. The half-open interval tests [v.y, v.y+1)
    mean that a point on a non-horizontal edge is counted by exactly the one
    crossing that owns that endpoint. A point on a horizontal edge is not
    covered by either crossing test and falls through with winding number 0
    (outside). See docs/architecture.md for the full derivation.

    Parameters
    ----------
    point:
        The query point as (x, y).
    polygon:
        A sequence of (x, y) vertices. The polygon may be non-convex or
        self-intersecting. The closing edge from the last vertex back to the
        first is implicit; do not repeat the first vertex. Must have at least
        3 vertices.

    Returns
    -------
    int
        The signed winding number.

    Raises
    ------
    ValueError
        If ``polygon`` has fewer than 3 vertices.

    Examples
    --------
    >>> square = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
    >>> winding_number((0, 0), square)
    1
    >>> winding_number((2, 0), square)
    0
    """
    n = len(polygon)
    if n < 3:
        raise ValueError(
            f"polygon must have at least 3 vertices, got {n}"
        )

    wn = 0
    _px, py = point

    for i in range(n):
        v0 = polygon[i]
        v1 = polygon[(i + 1) % n]

        # Upward crossing: v0 is at or below P, v1 is strictly above P.
        # The edge passes to the right of P when isLeft >= 0.
        # isLeft == 0 means P is on the edge line (on-edge: counts as inside).
        if v0[1] <= py and v1[1] > py and _is_left(v0, v1, point) >= 0:
            wn += 1
        # Downward crossing: v0 is strictly above P, v1 is at or below P.
        # The edge passes to the left of P when isLeft <= 0.
        # isLeft == 0 means P is on the edge line (on-edge: counts as inside).
        elif v0[1] > py and v1[1] <= py and _is_left(v0, v1, point) <= 0:
            wn -= 1

    return wn


def point_in_polygon(point: Point, polygon: Polygon) -> bool:
    """Return True iff ``point`` is inside ``polygon`` by the nonzero rule.

    A point is inside when ``winding_number(point, polygon) != 0``. This is
    the nonzero winding rule, which classifies all points inside a simple
    polygon and gives intuitive results for self-intersecting polygons (all
    regions with non-zero winding count as inside).

    On-edge convention: a point exactly on a non-horizontal polygon edge is
    counted as inside (the winding number is +/-1). A point on a horizontal
    edge is counted as outside. See docs/architecture.md.

    Parameters
    ----------
    point:
        The query point as (x, y).
    polygon:
        A sequence of (x, y) vertices. Must have at least 3 vertices.

    Returns
    -------
    bool
        True iff the winding number is non-zero.

    Raises
    ------
    ValueError
        If ``polygon`` has fewer than 3 vertices.

    Examples
    --------
    >>> square = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
    >>> point_in_polygon((0, 0), square)
    True
    >>> point_in_polygon((2, 0), square)
    False
    """
    return winding_number(point, polygon) != 0
