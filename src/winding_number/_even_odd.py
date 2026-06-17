"""Even-odd (crossing-number) point-in-polygon test.

The even-odd rule is an alternative fill rule to the nonzero (winding) rule.
A point is inside iff the number of times a horizontal ray from the point
crosses the polygon boundary is odd.

The two rules agree for simple (non-self-intersecting) polygons and disagree
for self-intersecting ones.  The canonical example is a five-pointed star
(pentagram) traced as the self-intersecting 5-vertex path: the central region
has winding number 2 (inside by the nonzero rule) but crossing number 2
(outside by the even-odd rule).

Edge-crossing convention (PNPOLY / Sunday):
    An edge (v0, v1) is counted as crossing the rightward ray from ``point``
    when exactly one endpoint is strictly above the ray and the other is at or
    below it, AND the crossing x-coordinate is to the right of the point.

    Formally: count the crossing when
        (v0.y > point.y) != (v1.y > point.y)
        and point.x < v0.x + (point.y - v0.y) / (v1.y - v0.y) * (v1.x - v0.x)

    This half-open interval (one endpoint strictly above, the other at-or-below)
    ensures that each vertex is owned by exactly one of its two incident edges,
    so a ray passing exactly through a vertex is counted once, not twice.
    Horizontal edges (v0.y == v1.y) are skipped entirely (both endpoints have
    equal y, so neither satisfies the strict-above condition).

On-edge behavior:
    A point exactly on a non-horizontal edge may fall on the crossing x
    calculation boundary.  In practice the floating-point test places such
    points consistently: the x-coordinate equality check uses strict >, so a
    point on the edge line is classified as inside (crossing count increments)
    when its x equals the crossing x precisely.  This matches the nonzero rule
    for non-horizontal edges.  Points on horizontal edges are classified as
    outside by both rules (horizontal edges are skipped).
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeAlias

Point: TypeAlias = tuple[float, float]
Polygon: TypeAlias = Sequence[tuple[float, float]]


def crossing_number(point: Point, polygon: Polygon) -> int:
    """Return the crossing number of ``polygon`` with respect to ``point``.

    The crossing number counts how many times a horizontal ray from ``point``
    pointing in the +x direction crosses the polygon boundary.  An odd crossing
    number means the point is inside under the even-odd rule; an even crossing
    number (including 0) means outside.

    Edge-crossing convention: an edge (v0, v1) contributes one crossing when
    exactly one of {v0.y, v1.y} is strictly above ``point.y`` and the other is
    at or below it, and the crossing x-coordinate is strictly greater than
    ``point.x``.  This half-open interval assigns every vertex to exactly one
    incident edge, so a ray through a vertex counts once.  Horizontal edges
    (both endpoints at the same y) are never counted.

    Parameters
    ----------
    point:
        The query point as (x, y).
    polygon:
        A sequence of (x, y) vertices. The polygon may be non-convex or
        self-intersecting.  The closing edge from the last vertex back to the
        first is implicit; do not repeat the first vertex.  Must have at least
        3 vertices.

    Returns
    -------
    int
        The non-negative crossing number.

    Raises
    ------
    ValueError
        If ``polygon`` has fewer than 3 vertices.

    Examples
    --------
    >>> square = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
    >>> crossing_number((0, 0), square)
    2
    >>> crossing_number((2, 0), square)
    0
    """
    n = len(polygon)
    if n < 3:
        raise ValueError(
            f"polygon must have at least 3 vertices, got {n}"
        )

    cn = 0
    px, py = point

    for i in range(n):
        v0 = polygon[i]
        v1 = polygon[(i + 1) % n]

        # Half-open interval: one endpoint strictly above the ray, the other
        # at-or-below.  This convention assigns each vertex to exactly one of
        # its two incident edges so a ray through a vertex is counted once.
        if (v0[1] > py) != (v1[1] > py):
            # x-coordinate of the intersection of edge (v0, v1) with y = py.
            x_intersect = v0[0] + (py - v0[1]) / (v1[1] - v0[1]) * (v1[0] - v0[0])
            if px < x_intersect:
                cn += 1

    return cn


def point_in_polygon_even_odd(point: Point, polygon: Polygon) -> bool:
    """Return True iff ``point`` is inside ``polygon`` by the even-odd rule.

    A point is inside when ``crossing_number(point, polygon)`` is odd.  This is
    the even-odd winding rule (also called the alternating rule or the ray-casting
    rule).

    For simple (non-self-intersecting) polygons the even-odd rule produces the
    same result as the nonzero rule (``point_in_polygon``).  The rules diverge
    for self-intersecting polygons: a region wound twice is inside by the nonzero
    rule but outside by the even-odd rule.

    The canonical example is a five-pointed star (pentagram) traced as a
    5-vertex self-intersecting path.  Its central region has winding number 2,
    so ``point_in_polygon`` returns True for the center.  The same center has
    crossing number 2, so this function returns False.

    On-edge convention: a point exactly on a non-horizontal polygon edge is
    counted as inside.  A point on a horizontal edge is counted as outside.
    This matches the behavior of ``point_in_polygon`` for non-horizontal edges.

    Parameters
    ----------
    point:
        The query point as (x, y).
    polygon:
        A sequence of (x, y) vertices.  Must have at least 3 vertices.

    Returns
    -------
    bool
        True iff the crossing number is odd.

    Raises
    ------
    ValueError
        If ``polygon`` has fewer than 3 vertices.

    Examples
    --------
    >>> square = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
    >>> point_in_polygon_even_odd((0, 0), square)
    True
    >>> point_in_polygon_even_odd((2, 0), square)
    False
    """
    return crossing_number(point, polygon) % 2 == 1
