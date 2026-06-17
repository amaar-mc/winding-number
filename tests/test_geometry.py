"""Tests for signed_area, orientation, and is_convex."""

from __future__ import annotations

import pytest

from winding_number import is_convex, orientation, signed_area

# CCW unit square: signed area should be +4.0.
CCW_SQUARE: list[tuple[float, float]] = [(1, -1), (1, 1), (-1, 1), (-1, -1)]

# CW unit square: signed area should be -4.0.
CW_SQUARE: list[tuple[float, float]] = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

# CCW equilateral triangle.
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


# ---------------------------------------------------------------------------
# signed_area: golden values
# ---------------------------------------------------------------------------


class TestSignedArea:
    def test_ccw_square(self) -> None:
        assert signed_area(CCW_SQUARE) == pytest.approx(4.0)

    def test_cw_square(self) -> None:
        assert signed_area(CW_SQUARE) == pytest.approx(-4.0)

    def test_ccw_triangle(self) -> None:
        # Triangle (0,0),(4,0),(0,4): area = 0.5 * 4 * 4 = 8.
        assert signed_area(CCW_TRIANGLE) == pytest.approx(8.0)

    def test_l_shape(self) -> None:
        # L-shape: 2x2 square minus 1x1 square in upper-right = 4 - 1 = 3.
        assert signed_area(L_SHAPE) == pytest.approx(3.0)

    def test_unit_triangle(self) -> None:
        tri: list[tuple[float, float]] = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
        assert signed_area(tri) == pytest.approx(0.5)

    def test_too_few_vertices(self) -> None:
        with pytest.raises(ValueError, match="at least 3 vertices"):
            signed_area([(0.0, 0.0), (1.0, 0.0)])


# ---------------------------------------------------------------------------
# orientation: golden values
# ---------------------------------------------------------------------------


class TestOrientation:
    def test_ccw_square(self) -> None:
        assert orientation(CCW_SQUARE) == "CCW"

    def test_cw_square(self) -> None:
        assert orientation(CW_SQUARE) == "CW"

    def test_ccw_triangle(self) -> None:
        assert orientation(CCW_TRIANGLE) == "CCW"

    def test_l_shape(self) -> None:
        assert orientation(L_SHAPE) == "CCW"

    def test_degenerate_raises(self) -> None:
        collinear: list[tuple[float, float]] = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]
        with pytest.raises(ValueError, match="zero signed area"):
            orientation(collinear)

    def test_too_few_vertices(self) -> None:
        with pytest.raises(ValueError, match="at least 3 vertices"):
            orientation([(0.0, 0.0), (1.0, 0.0)])


# ---------------------------------------------------------------------------
# is_convex: golden values
# ---------------------------------------------------------------------------


class TestIsConvex:
    def test_ccw_square_is_convex(self) -> None:
        assert is_convex(CCW_SQUARE) is True

    def test_cw_square_is_convex(self) -> None:
        assert is_convex(CW_SQUARE) is True

    def test_ccw_triangle_is_convex(self) -> None:
        assert is_convex(CCW_TRIANGLE) is True

    def test_l_shape_is_not_convex(self) -> None:
        assert is_convex(L_SHAPE) is False

    def test_pentagon_is_convex(self) -> None:
        import math

        n = 5
        pentagon: list[tuple[float, float]] = [
            (math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n))
            for i in range(n)
        ]
        assert is_convex(pentagon) is True

    def test_star_polygon_is_not_convex(self) -> None:
        # Simple 5-pointed star outline (non-convex).
        star: list[tuple[float, float]] = [
            (0.0, 1.0),
            (0.2, 0.2),
            (1.0, 0.0),
            (0.2, -0.2),
            (0.0, -1.0),
            (-0.2, -0.2),
            (-1.0, 0.0),
            (-0.2, 0.2),
        ]
        assert is_convex(star) is False

    def test_too_few_vertices(self) -> None:
        with pytest.raises(ValueError, match="at least 3 vertices"):
            is_convex([(0.0, 0.0), (1.0, 0.0)])
