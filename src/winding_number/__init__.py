"""Winding number and point-in-polygon for arbitrary polygons, pure Python, zero dependencies."""

from ._core import point_in_polygon, winding_number
from ._geometry import is_convex, orientation, signed_area

__all__ = [
    "is_convex",
    "orientation",
    "point_in_polygon",
    "signed_area",
    "winding_number",
]
__version__ = "0.1.0"
