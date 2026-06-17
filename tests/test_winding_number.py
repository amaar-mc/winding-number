"""Tests for winding_number and point_in_polygon."""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from winding_number import point_in_polygon, winding_number

# CCW unit square: vertices travel counterclockwise.
# Signed area = +4.0, winding number around center = +1.
CCW_SQUARE: list[tuple[float, float]] = [(1, -1), (1, 1), (-1, 1), (-1, -1)]

# CW unit square: same vertices in clockwise order.
CW_SQUARE: list[tuple[float, float]] = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

# CCW triangle with hand-picked interior and exterior points.
CCW_TRIANGLE: list[tuple[float, float]] = [(0.0, 0.0), (4.0, 0.0), (0.0, 4.0)]

# Non-convex L-shape (CCW).
# Vertices trace the outline of an L in counterclockwise order.
L_SHAPE: list[tuple[float, float]] = [
    (0.0, 0.0),
    (2.0, 0.0),
    (2.0, 1.0),
    (1.0, 1.0),
    (1.0, 2.0),
    (0.0, 2.0),
]


# ---------------------------------------------------------------------------
# Golden values: CCW square
# ---------------------------------------------------------------------------


class TestCCWSquareGolden:
    def test_winding_center(self) -> None:
        assert winding_number((0.0, 0.0), CCW_SQUARE) == 1

    def test_winding_outside(self) -> None:
        assert winding_number((2.0, 0.0), CCW_SQUARE) == 0

    def test_winding_outside_negative_x(self) -> None:
        assert winding_number((-2.0, 0.0), CCW_SQUARE) == 0

    def test_winding_outside_top(self) -> None:
        assert winding_number((0.0, 2.0), CCW_SQUARE) == 0

    def test_winding_outside_bottom(self) -> None:
        assert winding_number((0.0, -2.0), CCW_SQUARE) == 0

    def test_pip_center(self) -> None:
        assert point_in_polygon((0.0, 0.0), CCW_SQUARE) is True

    def test_pip_outside(self) -> None:
        assert point_in_polygon((2.0, 0.0), CCW_SQUARE) is False

    def test_pip_near_corners(self) -> None:
        assert point_in_polygon((0.9, 0.9), CCW_SQUARE) is True
        assert point_in_polygon((1.1, 1.1), CCW_SQUARE) is False


# ---------------------------------------------------------------------------
# Golden values: CW square
# ---------------------------------------------------------------------------


class TestCWSquare:
    def test_winding_center(self) -> None:
        assert winding_number((0.0, 0.0), CW_SQUARE) == -1

    def test_winding_outside(self) -> None:
        assert winding_number((2.0, 0.0), CW_SQUARE) == 0

    def test_pip_center(self) -> None:
        assert point_in_polygon((0.0, 0.0), CW_SQUARE) is True

    def test_pip_outside(self) -> None:
        assert point_in_polygon((2.0, 0.0), CW_SQUARE) is False


# ---------------------------------------------------------------------------
# Triangle tests
# ---------------------------------------------------------------------------


class TestTriangle:
    def test_inside_centroid(self) -> None:
        # Centroid of (0,0),(4,0),(0,4) is (4/3, 4/3).
        cx = 4.0 / 3.0
        cy = 4.0 / 3.0
        assert winding_number((cx, cy), CCW_TRIANGLE) == 1
        assert point_in_polygon((cx, cy), CCW_TRIANGLE) is True

    def test_outside_far(self) -> None:
        assert winding_number((5.0, 5.0), CCW_TRIANGLE) == 0
        assert point_in_polygon((5.0, 5.0), CCW_TRIANGLE) is False

    def test_outside_right(self) -> None:
        assert winding_number((3.0, 3.0), CCW_TRIANGLE) == 0
        assert point_in_polygon((3.0, 3.0), CCW_TRIANGLE) is False

    def test_inside_near_hypotenuse(self) -> None:
        # (1, 2.5) is strictly below the line x + y = 4 (sum = 3.5 < 4).
        assert point_in_polygon((1.0, 2.5), CCW_TRIANGLE) is True

    def test_outside_below_hypotenuse(self) -> None:
        # (2, 2.5): sum = 4.5 > 4, so outside.
        assert point_in_polygon((2.0, 2.5), CCW_TRIANGLE) is False


# ---------------------------------------------------------------------------
# L-shape tests (non-convex)
# ---------------------------------------------------------------------------


class TestLShape:
    def test_inside_bottom_bar(self) -> None:
        # (1.0, 0.5) is in the bottom horizontal bar of the L.
        assert winding_number((1.0, 0.5), L_SHAPE) == 1
        assert point_in_polygon((1.0, 0.5), L_SHAPE) is True

    def test_inside_vertical_bar(self) -> None:
        # (0.5, 1.5) is in the left vertical bar of the L.
        assert point_in_polygon((0.5, 1.5), L_SHAPE) is True

    def test_outside_notch(self) -> None:
        # (1.5, 1.5) is in the notch region of the L (upper right), outside.
        assert winding_number((1.5, 1.5), L_SHAPE) == 0
        assert point_in_polygon((1.5, 1.5), L_SHAPE) is False

    def test_outside_far(self) -> None:
        assert point_in_polygon((3.0, 3.0), L_SHAPE) is False

    def test_outside_left(self) -> None:
        assert point_in_polygon((-1.0, 1.0), L_SHAPE) is False


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------


class TestValidation:
    def test_too_few_vertices(self) -> None:
        with pytest.raises(ValueError, match="at least 3 vertices"):
            winding_number((0.0, 0.0), [(0.0, 0.0), (1.0, 0.0)])

    def test_zero_vertices(self) -> None:
        with pytest.raises(ValueError, match="at least 3 vertices"):
            winding_number((0.0, 0.0), [])

    def test_pip_too_few_vertices(self) -> None:
        with pytest.raises(ValueError, match="at least 3 vertices"):
            point_in_polygon((0.0, 0.0), [(0.0, 0.0), (1.0, 0.0)])


# ---------------------------------------------------------------------------
# Property test: pip consistent with winding number
# ---------------------------------------------------------------------------


@settings(max_examples=500)
@given(
    px=st.floats(min_value=-3.0, max_value=3.0, allow_nan=False, allow_infinity=False),
    py=st.floats(min_value=-3.0, max_value=3.0, allow_nan=False, allow_infinity=False),
)
def test_pip_equals_winding_nonzero_ccw_square(px: float, py: float) -> None:
    """point_in_polygon must equal (winding_number != 0) for every sampled point."""
    point = (px, py)
    wn = winding_number(point, CCW_SQUARE)
    pip = point_in_polygon(point, CCW_SQUARE)
    assert pip == (wn != 0)


@settings(max_examples=500)
@given(
    px=st.floats(min_value=-3.0, max_value=3.0, allow_nan=False, allow_infinity=False),
    py=st.floats(min_value=-3.0, max_value=3.0, allow_nan=False, allow_infinity=False),
)
def test_pip_equals_winding_nonzero_cw_square(px: float, py: float) -> None:
    """Property holds for a CW square."""
    point = (px, py)
    wn = winding_number(point, CW_SQUARE)
    pip = point_in_polygon(point, CW_SQUARE)
    assert pip == (wn != 0)


@settings(max_examples=500)
@given(
    px=st.floats(min_value=-1.0, max_value=5.0, allow_nan=False, allow_infinity=False),
    py=st.floats(min_value=-1.0, max_value=5.0, allow_nan=False, allow_infinity=False),
)
def test_pip_equals_winding_nonzero_triangle(px: float, py: float) -> None:
    """Property holds for the CCW triangle."""
    point = (px, py)
    wn = winding_number(point, CCW_TRIANGLE)
    pip = point_in_polygon(point, CCW_TRIANGLE)
    assert pip == (wn != 0)


@settings(max_examples=500)
@given(
    px=st.floats(min_value=-1.0, max_value=3.0, allow_nan=False, allow_infinity=False),
    py=st.floats(min_value=-1.0, max_value=3.0, allow_nan=False, allow_infinity=False),
)
def test_pip_equals_winding_nonzero_l_shape(px: float, py: float) -> None:
    """Property holds for the L-shape."""
    point = (px, py)
    wn = winding_number(point, L_SHAPE)
    pip = point_in_polygon(point, L_SHAPE)
    assert pip == (wn != 0)
