import math

from people.location import Point, distance


def test_distance_between_equal_points():
    p1 = Point(10, 10)
    p2 = Point(10, 10)
    assert distance(p1, p2) == 0


def test_distance_between_points_shifted_on_x():
    p1 = Point(101, 0)
    p2 = Point(0, 0)
    assert distance(p1, p2) == 101


def test_distance_between_points_shifted_on_y():
    p1 = Point(10, -65)
    p2 = Point(10, -64)
    assert distance(p1, p2) == 1


def test_distance_between_points():
    p1 = Point(10, 10)
    p2 = Point(-10, -10)
    assert math.isclose(distance(p1, p2), 28.2843, abs_tol=0.001)


def test_distance_is_absolute():
    p1 = Point(3234, 12)
    p2 = Point(-8632, 2345)
    assert math.isclose(distance(p1, p2), distance(p2, p1))
