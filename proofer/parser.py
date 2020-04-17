from dataclasses import dataclass
from itertools import combinations, chain
import typing

from ordered_set import OrderedSet


@dataclass(order=True, frozen=True)
class Point:
    name: str


@dataclass(unsafe_hash=True)
class Line:
    point1: Point
    point2: Point
    size: typing.Optional[float] = None


@dataclass(unsafe_hash=True)
class Angle:
    point1: Point
    angle_point: Point
    point2: Point
    size: typing.Optional[float] = None


def is_same_line(l1: Line, l2: Line):
    return (l1.point1 == l2.point1 and l1.point2 == l2.point2) or (l1.point1 == l2.point2 and l1.point2 == l2.point1)


def parse_points(points_string: str) -> typing.Sequence[Point]:
    parsed = list(map(Point, points_string.split(',')))
    result = OrderedSet(parsed)
    if len(parsed) != len(result):
        raise ValueError("The same point is used in the element: " + str(parsed))
    return result


def parse_line(line: str):
    shape, points_string = line.split()
    points = parse_points(points_string)
    if shape == 'line':
        if len(points) < 2:
            raise ValueError("The shape 'line' should have 2 points or more")
        return set(chain(
            map(lambda points: Line(*points), combinations(points, 2)),
            map(lambda points: Angle(*points, 180), combinations(points, 3)),
            points
        ))
    elif shape == 'polygon':
        if len(points) < 3:
            raise ValueError("The shape 'polygon' should have 3 points or more")
        return set(chain(
            [Line(points[i], points[(i + 1) % len(points)]) for i in range(len(points))],
            [Angle(points[i], points[(i + 1) % len(points)], points[(i + 2) % len(points)]) for i in range(len(points))],
            points
        ))