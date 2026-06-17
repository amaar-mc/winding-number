"""Tests for crossing_number and point_in_polygon_even_odd.

Key property being tested:
- For simple (non-self-intersecting) polygons, even-odd and nonzero rules agree.
- For self-intersecting polygons they can disagree.
- The canonical example is a pentagram (5-pointed star, 5-vertex self-intersecting path).
  The central region has winding number -2 (inside by the nonzero rule) and crossing
  number 2 (outside by the even-odd rule).
"""

from __future__ import annotations

import math

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from winding_number import (
    crossing_number,
    point_in_polygon,
    point_in_polygon_even_odd,
)

# CCW unit square, same fixture as the other test files.
CCW_SQUARE: list[tuple[float, float]] = [(1, -1), (1, 1), (-1, 1), (-1, -1)]

# CW unit square.
CW_SQUARE: list[tuple[float, float]] = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

# CCW triangle.
CCW_TRIANGLE: list[tuple[float, float]] = [(0.0, 0.0), (4.0, 0.0), (0.0, 4.0)]

# Non-convex L-shape (CCW).
L_SHAPE: list[tuple[float, float]] = [
    (0.0, 0.0),
    (2.0, 0.0),
    (2.0, 1.0),
    (1.0, 1.0),
    (1.0, 2.0),
    (0.0, 2.0),
]

# Pentagram: 5 outer-tip vertices of a unit-circle star connected in skip-2 order.
# This creates the self-intersecting 5-pointed star path.
# Vertices are placed at 0, 72, 144, 216, 288 degrees from the top (90 deg)
# of the unit circle, then reordered as [0, 2, 4, 1, 3] to produce the crossings.
#
#   [0] = tip at 90 deg  = (0.0,       1.0      )  (top)
#   [1] = tip at 234 deg = (-0.951057, 0.309017 )  (upper-left tip, but 2nd in path)
#   ...
#
# The central region (around (0, 0)) has winding number -2 and crossing number 2,
# which is the canonical disagreement case.
def _make_pentagram() -> list[tuple[float, float]]:
    n = 5
    circle_pts = [
        (math.cos(math.radians(90 - 72 * i)), math.sin(math.radians(90 - 72 * i)))
        for i in range(n)
    ]
    return [circle_pts[i % n] for i in [0, 2, 4, 1, 3]]


PENTAGRAM: list[tuple[float, float]] = _make_pentagram()


# ---------------------------------------------------------------------------
# Golden values: crossing_number for CCW square
# ---------------------------------------------------------------------------


class TestCrossingNumberCCWSquare:
    def test_center(self) -> None:
        # Ray from (0,0) rightward crosses right edge once.
        assert crossing_number((0.0, 0.0), CCW_SQUARE) == 1

    def test_outside_right(self) -> None:
        # (2, 0) is outside; no edges cross the ray to the right.
        assert crossing_number((2.0, 0.0), CCW_SQUARE) == 0

    def test_outside_left(self) -> None:
        # (-2, 0) has two edges to the right: left edge and right edge.
        assert crossing_number((-2.0, 0.0), CCW_SQUARE) == 2

    def test_outside_top(self) -> None:
        # (0, 2) is above the square; no crossings.
        assert crossing_number((0.0, 2.0), CCW_SQUARE) == 0

    def test_pip_center(self) -> None:
        assert point_in_polygon_even_odd((0.0, 0.0), CCW_SQUARE) is True

    def test_pip_outside(self) -> None:
        assert point_in_polygon_even_odd((2.0, 0.0), CCW_SQUARE) is False

    def test_pip_near_corners(self) -> None:
        assert point_in_polygon_even_odd((0.9, 0.9), CCW_SQUARE) is True
        assert point_in_polygon_even_odd((1.1, 1.1), CCW_SQUARE) is False


# ---------------------------------------------------------------------------
# Golden values: crossing_number for CCW triangle
# ---------------------------------------------------------------------------


class TestCrossingNumberTriangle:
    def test_centroid(self) -> None:
        # Centroid (4/3, 4/3) is inside; ray crosses hypotenuse once.
        assert crossing_number((4.0 / 3.0, 4.0 / 3.0), CCW_TRIANGLE) == 1

    def test_outside_far(self) -> None:
        assert crossing_number((5.0, 5.0), CCW_TRIANGLE) == 0


# ---------------------------------------------------------------------------
# Agreement: simple polygons
# ---------------------------------------------------------------------------
# For simple (non-self-intersecting) polygons, even-odd and nonzero agree.


class TestAgreementOnSimplePolygons:
    def test_ccw_square_inside(self) -> None:
        p = (0.0, 0.0)
        assert point_in_polygon_even_odd(p, CCW_SQUARE) == point_in_polygon(p, CCW_SQUARE)

    def test_ccw_square_outside(self) -> None:
        p = (2.0, 0.0)
        assert point_in_polygon_even_odd(p, CCW_SQUARE) == point_in_polygon(p, CCW_SQUARE)

    def test_cw_square_inside(self) -> None:
        p = (0.0, 0.0)
        assert point_in_polygon_even_odd(p, CW_SQUARE) == point_in_polygon(p, CW_SQUARE)

    def test_cw_square_outside(self) -> None:
        p = (2.0, 0.0)
        assert point_in_polygon_even_odd(p, CW_SQUARE) == point_in_polygon(p, CW_SQUARE)

    def test_triangle_inside(self) -> None:
        p = (4.0 / 3.0, 4.0 / 3.0)
        assert point_in_polygon_even_odd(p, CCW_TRIANGLE) == point_in_polygon(p, CCW_TRIANGLE)

    def test_triangle_outside(self) -> None:
        p = (5.0, 5.0)
        assert point_in_polygon_even_odd(p, CCW_TRIANGLE) == point_in_polygon(p, CCW_TRIANGLE)

    def test_l_shape_inside(self) -> None:
        p = (1.0, 0.5)
        assert point_in_polygon_even_odd(p, L_SHAPE) == point_in_polygon(p, L_SHAPE)

    def test_l_shape_outside_notch(self) -> None:
        p = (1.5, 1.5)
        assert point_in_polygon_even_odd(p, L_SHAPE) == point_in_polygon(p, L_SHAPE)

    def test_l_shape_outside_far(self) -> None:
        p = (3.0, 3.0)
        assert point_in_polygon_even_odd(p, L_SHAPE) == point_in_polygon(p, L_SHAPE)


# ---------------------------------------------------------------------------
# Disagreement: pentagram center
# ---------------------------------------------------------------------------
# The pentagram center is the canonical case where the two rules disagree.
# Winding number = -2 (nonzero: inside), crossing number = 2 (even-odd: outside).


class TestPentagramDisagreement:
    def test_center_winding_number_is_minus_two(self) -> None:
        # The center of the pentagram is wound around twice (CW), so winding number = -2.
        from winding_number import winding_number

        wn = winding_number((0.0, 0.0), PENTAGRAM)
        assert wn == -2

    def test_center_crossing_number_is_two(self) -> None:
        # The center has crossing number 2.
        assert crossing_number((0.0, 0.0), PENTAGRAM) == 2

    def test_center_inside_by_nonzero_rule(self) -> None:
        # Nonzero rule: winding number != 0, so inside.
        assert point_in_polygon((0.0, 0.0), PENTAGRAM) is True

    def test_center_outside_by_even_odd_rule(self) -> None:
        # Even-odd rule: crossing number 2 is even, so outside.
        assert point_in_polygon_even_odd((0.0, 0.0), PENTAGRAM) is False

    def test_center_rules_disagree(self) -> None:
        # The two rules give opposite results for the pentagram center.
        center = (0.0, 0.0)
        nonzero_result = point_in_polygon(center, PENTAGRAM)
        even_odd_result = point_in_polygon_even_odd(center, PENTAGRAM)
        assert nonzero_result is True
        assert even_odd_result is False
        assert nonzero_result != even_odd_result

    def test_star_arm_rules_agree(self) -> None:
        # A point in a star spike (between center and outer tip) is inside by both rules.
        # (0, 0.5) is in the top arm: winding = -1, crossing = 1 (both inside).
        arm = (0.0, 0.5)
        assert point_in_polygon(arm, PENTAGRAM) is True
        assert point_in_polygon_even_odd(arm, PENTAGRAM) is True

    def test_exterior_rules_agree(self) -> None:
        # A clearly exterior point is outside by both rules.
        ext = (2.0, 0.0)
        assert point_in_polygon(ext, PENTAGRAM) is False
        assert point_in_polygon_even_odd(ext, PENTAGRAM) is False


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------


class TestValidation:
    def test_crossing_number_too_few_vertices(self) -> None:
        with pytest.raises(ValueError, match="at least 3 vertices"):
            crossing_number((0.0, 0.0), [(0.0, 0.0), (1.0, 0.0)])

    def test_crossing_number_zero_vertices(self) -> None:
        with pytest.raises(ValueError, match="at least 3 vertices"):
            crossing_number((0.0, 0.0), [])

    def test_pip_even_odd_too_few_vertices(self) -> None:
        with pytest.raises(ValueError, match="at least 3 vertices"):
            point_in_polygon_even_odd((0.0, 0.0), [(0.0, 0.0), (1.0, 0.0)])


# ---------------------------------------------------------------------------
# Property test: for convex polygons, even-odd and nonzero agree on interior
# and exterior points (boundary points may differ between the two algorithms)
# ---------------------------------------------------------------------------
# Both fill rules agree at strictly interior and strictly exterior points of
# simple polygons.  On-edge behavior is algorithm-specific: the nonzero rule
# (Sunday's isLeft algorithm) counts a point on a non-horizontal edge as inside,
# while the even-odd rule's strict-< crossing test counts that same point as
# outside.  Points on horizontal edges are outside by both rules.
#
# The property tests below sample points from a range that excludes the polygon
# boundary.  They are not a claim about on-boundary behavior.


@settings(max_examples=500)
@given(
    px=st.floats(min_value=-0.99, max_value=0.99, allow_nan=False, allow_infinity=False),
    py=st.floats(min_value=-0.99, max_value=0.99, allow_nan=False, allow_infinity=False),
)
def test_even_odd_agrees_with_nonzero_ccw_square_interior(px: float, py: float) -> None:
    """For a convex polygon, even-odd and nonzero agree for all interior points.

    Sampled from [-0.99, 0.99] so all points are strictly inside the unit square.
    """
    point = (px, py)
    assert point_in_polygon_even_odd(point, CCW_SQUARE) is True
    assert point_in_polygon(point, CCW_SQUARE) is True


@settings(max_examples=500)
@given(
    px=st.floats(min_value=1.01, max_value=3.0, allow_nan=False, allow_infinity=False),
    py=st.floats(min_value=-3.0, max_value=3.0, allow_nan=False, allow_infinity=False),
)
def test_even_odd_agrees_with_nonzero_ccw_square_exterior(px: float, py: float) -> None:
    """For a convex polygon, even-odd and nonzero agree for clearly exterior points."""
    point = (px, py)
    assert point_in_polygon_even_odd(point, CCW_SQUARE) is False
    assert point_in_polygon(point, CCW_SQUARE) is False


@settings(max_examples=500)
@given(
    # Strictly inside the CCW triangle: x in (0,1), y in (0,1), x+y < 1 guaranteed.
    px=st.floats(min_value=0.01, max_value=0.49, allow_nan=False, allow_infinity=False),
    py=st.floats(min_value=0.01, max_value=0.49, allow_nan=False, allow_infinity=False),
)
def test_even_odd_agrees_with_nonzero_triangle_interior(px: float, py: float) -> None:
    """For the CCW triangle, even-odd and nonzero agree for all interior points.

    Sampled from [0.01, 0.49] x [0.01, 0.49] so all points satisfy x+y < 1 and
    are strictly inside the quarter of the triangle closest to the origin.
    This avoids the hypotenuse and all polygon edges.
    """
    point = (px, py)
    assert point_in_polygon_even_odd(point, CCW_TRIANGLE) is True
    assert point_in_polygon(point, CCW_TRIANGLE) is True
