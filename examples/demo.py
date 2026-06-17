"""Example: test a few points against polygons using winding_number."""

from winding_number import is_convex, orientation, point_in_polygon, signed_area, winding_number

# CCW unit square with vertices at (+/-1, +/-1).
ccw_square = [(1.0, -1.0), (1.0, 1.0), (-1.0, 1.0), (-1.0, -1.0)]

print("CCW square")
print(f"  signed_area  = {signed_area(ccw_square)}")   # 4.0
print(f"  orientation  = {orientation(ccw_square)}")   # CCW
print(f"  is_convex    = {is_convex(ccw_square)}")     # True
print()

test_points = [
    ((0.0, 0.0), "center (inside)"),
    ((2.0, 0.0), "to the right (outside)"),
    ((0.5, 0.5), "upper-right quadrant (inside)"),
    ((-1.5, 0.0), "left of square (outside)"),
]
for point, label in test_points:
    wn = winding_number(point, ccw_square)
    pip = point_in_polygon(point, ccw_square)
    print(f"  point {point} ({label}): winding={wn}, inside={pip}")

print()

# Non-convex L-shape.
l_shape = [
    (0.0, 0.0),
    (2.0, 0.0),
    (2.0, 1.0),
    (1.0, 1.0),
    (1.0, 2.0),
    (0.0, 2.0),
]

print("L-shape (non-convex CCW)")
print(f"  signed_area  = {signed_area(l_shape)}")   # 3.0
print(f"  orientation  = {orientation(l_shape)}")   # CCW
print(f"  is_convex    = {is_convex(l_shape)}")     # False
print()

l_test_points = [
    ((1.0, 0.5), "bottom bar (inside)"),
    ((0.5, 1.5), "vertical bar (inside)"),
    ((1.5, 1.5), "notch region (outside)"),
    ((3.0, 3.0), "far outside"),
]
for point, label in l_test_points:
    wn = winding_number(point, l_shape)
    pip = point_in_polygon(point, l_shape)
    print(f"  point {point} ({label}): winding={wn}, inside={pip}")
