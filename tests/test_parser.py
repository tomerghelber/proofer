from proofer import parse_line, Point, Line

def test_parse_line_2_points(self):
    paresd = parse_line('line A,B')

    point_a = Point("A")
    point_b = Point("B")
    expected = set([point_a, point_b, Line(point_a, point_b)])

    assert expected == paresd

def test_parse_triangle(self):
    pass
