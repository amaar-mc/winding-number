"""Polygon geometry helpers: signed area, orientation, and convexity."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeAlias

Point: TypeAlias = tuple[float, float]
Polygon: TypeAlias = Sequence[tuple[float, float]]


def signed_area(polygon: Polygon) -> float:
    """Return the signed area of ``polygon`` via the shoelace formula.

    The shoelace (Gauss) formula computes the signed area in O(n) time:

        A = 0.5 * sum over i of (x_i * y_{i+1} - x_{i+1} * y_i)

    The sign encodes orientation: positive for counterclockwise (CCW) vertices,
    negative for clockwise (CW) vertices, following the right-hand rule in a
    standard coordinate system (y increasing upward). The formula generalizes
    to non-convex and self-intersecting polygons; for self-intersecting
    polygons the result is the net signed area (regions wound twice count
    twice).

    Parameters
    ----------
    polygon:
        A sequence of (x, y) vertices. The closing edge is implicit. Must have
        at least 3 vertices.

    Returns
    -------
    float
        The signed area. Positive means CCW; negative means CW; zero means
        degenerate (collinear vertices or self-cancelling).

    Raises
    ------
    ValueError
        If ``polygon`` has fewer than 3 vertices.

    Examples
    --------
    >>> square = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
    >>> signed_area(square)
    4.0
    """
    n = len(polygon)
    if n < 3:
        raise ValueError(
            f"polygon must have at least 3 vertices, got {n}"
        )

    total = 0.0
    for i in range(n):
        x0, y0 = polygon[i]
        x1, y1 = polygon[(i + 1) % n]
        total += x0 * y1 - x1 * y0

    return total / 2.0


def orientation(polygon: Polygon) -> str:
    """Return the orientation of ``polygon`` as "CCW" or "CW".

    Orientation is determined by the sign of ``signed_area``: positive signed
    area means the vertices are ordered counterclockwise (CCW); negative means
    clockwise (CW). A zero signed area indicates a degenerate polygon.

    Parameters
    ----------
    polygon:
        A sequence of (x, y) vertices. Must have at least 3 vertices.

    Returns
    -------
    str
        "CCW" if the polygon is counterclockwise, "CW" if clockwise.

    Raises
    ------
    ValueError
        If ``polygon`` has fewer than 3 vertices, or if the signed area is
        zero (degenerate polygon with collinear vertices or self-cancellation).

    Examples
    --------
    >>> square = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
    >>> orientation(square)
    'CCW'
    >>> cw_square = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
    >>> orientation(cw_square)
    'CW'
    """
    area = signed_area(polygon)
    if area > 0.0:
        return "CCW"
    if area < 0.0:
        return "CW"
    raise ValueError(
        "polygon has zero signed area (degenerate: vertices are collinear or self-cancelling)"
    )


def is_convex(polygon: Polygon) -> bool:
    """Return True iff ``polygon`` is convex.

    A polygon is convex if all cross products of consecutive edges have the
    same sign (all non-negative for CCW, all non-positive for CW). Zero cross
    products (collinear consecutive edges) are allowed.

    The cross product at vertex i is:
        (v[i+1] - v[i]) x (v[i+2] - v[i+1])

    which equals the signed area of the triangle times two and is positive
    when the turn at that vertex is left (CCW) and negative when the turn is
    right (CW).

    Parameters
    ----------
    polygon:
        A sequence of (x, y) vertices. Must have at least 3 vertices.

    Returns
    -------
    bool
        True iff the polygon is convex (all cross products share one sign).

    Raises
    ------
    ValueError
        If ``polygon`` has fewer than 3 vertices.

    Examples
    --------
    >>> square = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
    >>> is_convex(square)
    True
    >>> l_shape = [(0,0),(2,0),(2,1),(1,1),(1,2),(0,2)]
    >>> is_convex(l_shape)
    False
    """
    n = len(polygon)
    if n < 3:
        raise ValueError(
            f"polygon must have at least 3 vertices, got {n}"
        )

    got_positive = False
    got_negative = False

    for i in range(n):
        x0, y0 = polygon[i]
        x1, y1 = polygon[(i + 1) % n]
        x2, y2 = polygon[(i + 2) % n]

        # Cross product of edges (v1 - v0) and (v2 - v1).
        cross = (x1 - x0) * (y2 - y1) - (y1 - y0) * (x2 - x1)

        if cross > 0:
            got_positive = True
        elif cross < 0:
            got_negative = True

        if got_positive and got_negative:
            return False

    return True
