from collections import namedtuple
import math

from .vector import Vector

MINIMAL_DISTANCE = 0.1 # distances smaller than that will be considered 0


def distance(vector1, vector2):
    """Determines the distance between two location vectors.

    Parameters:
        * vector1: x,y coordinates in the form of a people.vector
        * vector2: x,y coordinates in the form of a people.vector

    Returns:
        The distance between the two location vectors in [m].
    """
    return (vector2 - vector1).norm()


def same_location(vector1, vector2):
    """Determines whether two location vectors point to the same location.

    Locations are considered the same when their distance is below 0.1m.

    Parameters:
        * vector1: x,y coordinates in the form of a people.vector
        * vector2: x,y coordinates in the form of a people.vector

    Returns:
        True if the two vectors point to the same location, False otherwise.
    """
    return distance(vector1, vector2) < MINIMAL_DISTANCE
