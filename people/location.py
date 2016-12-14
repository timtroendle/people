from collections import namedtuple
import math

from .vector import Vector

MINIMAL_DISTANCE = 0.1 # distances smaller than that will be considered 0


def distance(vector1, vector2):
    return (vector2 - vector1).norm()


def same_location(vector1, vector2):
    return distance(vector1, vector2) < MINIMAL_DISTANCE
