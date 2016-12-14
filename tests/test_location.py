import math

from people.location import Vector, distance, same_location


def test_distance_between_equal_vectors():
    v1 = Vector(10, 10)
    v2 = Vector(10, 10)
    assert distance(v1, v2) == 0


def test_distance_between_vectors_shifted_on_x():
    v1 = Vector(101, 0)
    v2 = Vector(0, 0)
    assert distance(v1, v2) == 101


def test_distance_between_vectors_shifted_on_y():
    v1 = Vector(10, -65)
    v2 = Vector(10, -64)
    assert distance(v1, v2) == 1


def test_distance_between_vectors():
    v1 = Vector(10, 10)
    v2 = Vector(-10, -10)
    assert math.isclose(distance(v1, v2), 28.2843, abs_tol=0.001)


def test_distance_is_absolute():
    v1 = Vector(3234, 12)
    v2 = Vector(-8632, 2345)
    assert math.isclose(distance(v1, v2), distance(v2, v1))


def test_equality():
    v1 = Vector(234, 422)
    v2 = Vector(234, 422)
    assert same_location(v1, v2)


def test_almost_equality():
    v1 = Vector(234, 422)
    v2 = Vector(234, 422.05)
    assert same_location(v1, v2)


def test_inequality():
    v1 = Vector(234, 422)
    v2 = Vector(233, 422)
    assert not same_location(v1, v2)
