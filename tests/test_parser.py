import operator as op
from functools import reduce
from random import randint

from proofer import parse_line, Point, Line

def nCk(n, k):
    k = min(k, n-k)
    numer = reduce(op.mul, range(n, n - k, -1), 1)
    denom = reduce(op.mul, range(1, k + 1), 1)
    return numer / denom


def test_parse_line_2_points():
    paresd = parse_line('line A,B')

    point_a = Point("A")
    point_b = Point("B")
    expected = set([point_a, point_b, Line(point_a, point_b)])

    assert expected == paresd

def test_parse_line():
    for number_of_points in range(2, 12):
        expected_number_of_lines = nCk(number_of_points, 2)
        expected_number_of_angles = nCk(number_of_points, 3)
        expected_number_of_objects = number_of_points + expected_number_of_lines + expected_number_of_angles

        paresd = parse_line('line ' + ','.join(map(str, range(number_of_points))))
        
        assert expected_number_of_objects == len(paresd)

def test_parse_triangle():
    pass
