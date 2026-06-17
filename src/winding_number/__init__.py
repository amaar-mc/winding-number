"""Winding number and point-in-polygon for arbitrary polygons, pure Python, zero dependencies."""

from ._core import point_in_polygon, winding_number
from ._even_odd import crossing_number, point_in_polygon_even_odd
from ._geometry import is_convex, orientation, signed_area

__all__ = [
    "crossing_number",
    "is_convex",
    "orientation",
    "point_in_polygon",
    "point_in_polygon_even_odd",
    "signed_area",
    "winding_number",
]
__version__ = "0.2.0"
