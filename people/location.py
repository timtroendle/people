from collections import namedtuple
import math

Point = namedtuple('Point', 'x y')


def distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)