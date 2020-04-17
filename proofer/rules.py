from abc import ABC, abstractmethod
from itertools import chain
import typing

from sqlalchemy import and_
from sqlalchemy.orm import Query, aliased

from proofer.informations import Angle, Line

          
class Rule(ABC):
    @abstractmethod
    def execute(self, session):
        pass


class SimpleRule(Rule):
    def __init__(self, query: set, name: typing.Optional[str] = None):
        self.__query = query
        self.__name = "SimpleRule" if name is None else name

    def execute(self, session):
        self.__query.with_session(session)

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
    query = Angle.insert().from_select(
        Query([angle1.point1, angle1.angle_point, angle2.point2, angle1.size + angle2.size])
            .select_from(angle1)
            .join(angle2, and_(angle1.angle_point == angle2.angle_point, angle1.point2 == angle2.point1))
    )
    return SimpleRule(query, "SimpleRule")
