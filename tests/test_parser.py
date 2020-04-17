def test_parse_line_2_points(self):
    paresd = parse_line('line A,B')

    expected = set([Point("A"), Point("B"), Line(point_a, point_b)])

    assert expected == paresd

def test_parse_triangle(self):
    pass
