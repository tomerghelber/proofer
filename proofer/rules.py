from abc import ABC, abstractmethod
from itertools import chain
import typing

from sqlalchemy import and_, select
from sqlalchemy.orm import Query, aliased

from proofer.informations import Angle, Vector

          
class Rule(ABC):
    @abstractmethod
    def execute(self, session):
        pass


class SimpleRule(Rule):
    def __init__(self, query, name: typing.Optional[str] = None):
        self.__query = query
        self.__name = "SimpleRule" if name is None else name

    def execute(self, session):
        print(self.__query)
        session.connection().execute(self.__query)
        session.commit()

    def __repr__(self):
        return "{}({})".format(self.__name, str(self.__query))


def SumAngles():
    """Sum angles.
    INESET INTO angles (point1, angle_point, point2, size)
    SELECT angles1.point1 as point1, angles1.angle_point as angle_point, angles2.point2 as point2, angles1.size + angles2.size as size
    FROM angles angles1, angles angles2
    WHERE angles1.angle_point == angles2.angle_point AND angles1.point2 == angles2.point1;
    """
    angle1 = aliased(Angle)
    angle2 = aliased(Angle)
    query = Angle.__table__.insert().from_select(
        ["point1", "angle_point", "point2", "size"],
        select([angle1.point1.label("point1"), angle1.angle_point.label("angle_point"), angle2.point2.label("point2"), (angle1.size + angle2.size).label("size")])
            .where(and_(angle1.angle_point == angle2.angle_point, angle1.point2 == angle2.point1))
    )
    return SimpleRule(query, "SumAngles")


def SumVectors():
    vector1 = aliased(Vector)
    vector2 = aliased(Vector)
    angle = aliased(Angle)
    query = Vector.__table__.insert().from_select(
        ["start_point", "end_point", "length"],
        select([vector1.start_point.label("start_point"), vector2.end_point.label("end_point"), (vector1.length + vector2.length).label("length")])
            .where(and_(angle.size == 180, angle.point1 == vector1.start_point, angle.angle_point == vector1.end_point, angle.angle_point == vector2.start_point, angle.point2 == vector2.end_point))
    )
    return SimpleRule(query, "SumLines")
