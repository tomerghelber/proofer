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
            vectors = [Vector(start_point=point1, end_point=point2) for point1, point2 in combinations(points, 2)]
            angles = [Angle(vector1=vec1, vector2=vec2, size=180) for vec1, vec2 in combinations(vectors, 2)]
            res = frozenset(chain(vectors, angles))
            return res
        elif shape == 'polygon':
            if len(points) < 3:
                raise ValueError("The shape 'polygon' should have 3 points or more")
            vectors = [Vector(start_point=points[i], end_point=points[(i + 1) % len(points)])
                       for i in range(len(points))]
            angles = [Angle(vector1=vectors[i], vector2=vectors[(i + 1) % len(vectors)]) for i in range(len(vectors))]
            res = frozenset(chain(vectors, angles))
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
