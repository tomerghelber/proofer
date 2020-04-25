import operator as op
from functools import reduce

import pytest

from proofer.parser import parser


def nCk(n: int, k: int) -> float:
    if n < k:
        return 0.0
    k = min(k, n-k)
    numer = reduce(op.mul, range(n, n - k, -1), 1)
    denom = reduce(op.mul, range(1, k + 1), 1)
    return numer / denom


def number_to_char(number):
    return chr(ord('A') + number)


@pytest.mark.parametrize("number_of_points", range(2, 12))
def test_parse_line(number_of_points: int):
    expected_number_of_lines = nCk(number_of_points, 2)
    expected_number_of_angles = nCk(number_of_points, 3)
    expected_number_of_objects = expected_number_of_lines + expected_number_of_angles

    paresd = parser.parse('line ' + ','.join(map(number_to_char, range(number_of_points))))

    assert expected_number_of_objects == len(paresd)


@pytest.mark.parametrize("number_of_points", range(2))
def test_parse_line_not_enough_points(number_of_points: int):
    with pytest.raises(Exception):
        parser.parse('line ' + ','.join(map(number_to_char, range(number_of_points))))


@pytest.mark.parametrize("number_of_points", range(3, 12))
def test_parse_polygon(number_of_points: int):
    parsed = parser.parse('polygon ' + ','.join(map(number_to_char, range(number_of_points))))

    expected_number_of_objects = 2 * number_of_points

    assert expected_number_of_objects == len(parsed)


@pytest.mark.parametrize("number_of_points", range(3))
def test_parse_polygon_not_enough_points(number_of_points: int):
    with pytest.raises(Exception):
        parser.parse('polygon ' + ','.join(map(number_to_char, range(number_of_points))))
