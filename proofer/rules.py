from abc import ABC, abstractmethod
import typing

from sqlalchemy import and_, select
from sqlalchemy.orm import aliased

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
    """
    angle1 = aliased(Angle)
    angle2 = aliased(Angle)
    query = Angle.__table__.insert().from_select(
        ["start_point1", "end_point1", "start_point2", "end_point2", "size"],
        select([angle1.start_point1.label('start_point1'), angle1.end_point1.label('end_point1'),
                  angle2.start_point2.label('start_point2'), angle2.end_point2.label('end_point2'),
                  (angle1.size + angle2.size).label('size')])
            .where(and_(angle1.start_point2 == angle2.start_point1, angle1.end_point2 == angle2.end_point1))

    )
    return SimpleRule(query, "SumAngles")


def SumVectors():
    vector1 = aliased(Vector)
    vector2 = aliased(Vector)
    angle = aliased(Angle)
    query = Vector.__table__.insert().from_select(
        ["start_point", "end_point", "length"],
        select([angle.start_point1.label("start_point"), angle.end_point2.label("end_point"), (vector1.length + vector2.length).label("length")])
            .where(and_(angle.size == 180, angle.end_point1 == angle.start_point2,
                        angle.start_point1 == vector1.start_point, angle.end_point1 == vector1.end_point,
                        angle.start_point2 == vector2.start_point, angle.end_point2 == vector2.end_point))
    )
    return SimpleRule(query, "SumLines")
