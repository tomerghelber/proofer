from abc import ABC, abstractmethod
import typing

from sqlalchemy import and_, select
from sqlalchemy.orm import aliased, Session

from proofer.informations import Angle, Vector


class Rule(ABC):
    """Base interface to create executable rules for proofer."""
    @abstractmethod
    def execute(self, session: Session):
        """The main function to execute logic.

        Args:
            session: An SqlAlchemy session.

        """
        pass


class SumAngles(Rule):
    def execute(self, session: Session):
        angle1 = aliased(Angle, name="angle1")
        angle2 = aliased(Angle, name="angle2")
        angles = session.query(angle1.vector_id1, angle2.vector_id2, angle1.size + angle2.size).filter(
            and_(angle1.vector_id2 == angle2.vector_id1, angle1.size != None, angle2.size != None)).all()

        mapper = lambda ang: Angle(vector_id1=ang[0], vector_id2=ang[1], size=ang[2])
        new_angles = list(map(mapper, angles))
        session.add_all(new_angles)
        session.commit()


class ReverseAngle(Rule):
    def execute(self, session: Session):
        angle = aliased(Angle, name="angle1")
        angles = session.query(angle.vector_id2, angle.vector_id1, 360 - angle.size).filter(angle.size != None).all()
        mapper = lambda ang: Angle(vector_id1=ang[0], vector_id2=ang[1], size=ang[2])
        new_angles = list(map(mapper, angles))
        session.add_all(new_angles)
        session.commit()


class SumVectors(Rule):
    def execute(self, session: Session):
        vector1 = aliased(Vector, name="vector1")
        vector2 = aliased(Vector, name="vector2")
        angle = aliased(Angle)
        vectors = session.query(vector1.start_point, vector2.end_point, vector1.length + vector2.length)\
        .filter(and_(angle.size == 180, vector1.end_point == vector2.start_point,
                     angle.vector_id1 == vector1.id, angle.vector_id2 == vector2.id,
                     None != vector1.length, None != vector2.length
                     )).all()
        mapper = lambda vec: Vector(start_point=vec[0], end_point=vec[1], length=vec[2])
        new_vectors = list(map(mapper, vectors))
        session.add_all(new_vectors)
        session.commit()


class ReverseVector(Rule):
    def execute(self, session: Session):
        vectors = session.query(Vector).all()
        mapper = lambda vec: Vector(start_point=vec.end_point, end_point=vec.start_point, length=vec.length)
        new_vectors = list(map(mapper, vectors))
        session.add_all(new_vectors)
        session.commit()
