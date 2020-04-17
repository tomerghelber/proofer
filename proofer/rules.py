from abc import ABC, abstractmethod
from itertools import chain
import typing

from sqlalchemy import and_
from sqlalchemy.orm import Query

from informations import Angle, Line

          
class Rule(ABC):
    @abstractmethod
    def execute(self, information: Information):
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
    first_angle = aliased(Angle)
    second_angle = aliased(Angle)
    query = Angle.insert().from_select(
        Query([first_angle.point1, first_angle.angle_point, second_angle.point2, angles1.size + angles2.size])
            select_from(first_angle)
            .join(second_angle, and_(first_angle.angle_point == second_angle.angle_point, first_angle.point2 == second_angle.point1))
    )
    return SimpleRule(query, "SimpleRule")
