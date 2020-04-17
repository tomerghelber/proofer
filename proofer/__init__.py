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
    return OrderedSet(map(Point, points_string.split(',')))


def parse_line(line: str):
    shape, points_string = line.split()
    points = parse_points(points_string)
    if shape == 'line':
        return set(chain(map(lambda points: Line(*points), combinations(points, 2)), map(lambda points: Angle(*points), combinations(points, 3)), points))
    if shape == 'triangle':
        if len(points) == 3:
            pass
        else:
            raise ValueError('The shape triangle should have exactly 3 points')


def main():
    point_a = Point("A")
    point_b = Point("B")
    point_c = Point("C")
    line_ab = Line(point_a, point_b)
    line_bc = Line(point_b, point_c)
    line_ac = Line(point_a, point_c)
    hand = set([point_a, point_b, point_c, line_ab, line_bc, line_ac])
    paresd = parse_line('triangle A,B,C')
    assert hand == paresd


if __name__ == "__main__":
    main()
