from itertools import chain, combinations

from lark import Lark, Transformer
from ordered_set import OrderedSet

from proofer.informations import Vector, Angle


class MYTransformer(Transformer):
    def point(self, args):
        return str(args[0])

    def points(self, args):
        result = OrderedSet(args)
        if len(args) != len(result):
            raise ValueError(f"The same point is used in the element: {args}")
        return result

    def shape(self, args):
        shape = args[0]
        points = args[1]
        if shape == 'line':
            if len(points) < 2:
                raise ValueError("The shape 'line' should have 2 points or more")
            res = frozenset(chain(
                map(lambda points: Vector(start_point=points[0], end_point=points[1]), combinations(points, 2)),
                map(lambda points: Angle(start_point1=points[0], end_point1=points[1],
                                         start_point2=points[1], end_point2=points[2], size=180), combinations(points, 3)),
            ))
            return res
        elif shape == 'polygon':
            if len(points) < 3:
                raise ValueError("The shape 'polygon' should have 3 points or more")
            res = frozenset(chain(
                [Vector(start_point=points[i], end_point=points[(i + 1) % len(points)]) for i in range(len(points))],
                [Angle(start_point1=points[i], end_point1=points[(i + 1) % len(points)],
                       start_point2=points[(i + 1) % len(points)], end_point2=points[(i + 2) % len(points)])
                 for i in range(len(points))],
            ))
            return res
        raise ValueError(f"Unknown shape: '{shape}'")

    def start(self, args):
        return frozenset(chain.from_iterable(args))

grammar = r"""
start: _NEWLINE* shape (_NEWLINE+ shape)* _NEWLINE*
shape: SHAPE_TYPE points
points: point (_POINT_SEPARATOR point)*
point: WORD

_POINT_SEPARATOR: ","
SHAPE_TYPE: "line" | "polygon"

COMMENT: "#" /[^\n]/*

%import common (WORD, WS_INLINE)
%import common.NEWLINE -> _NEWLINE

%ignore COMMENT
%ignore WS_INLINE
"""

parser = Lark(grammar, parser="lalr", transformer=MYTransformer())
