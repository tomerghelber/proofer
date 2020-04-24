from abc import ABC, abstractmethod
import contextlib

from sqlalchemy import Column, String, Float, CheckConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Information(ABC):
    @abstractmethod
    def execute(self, rule):
        pass


Base = declarative_base()


class Vector(Base):
    __tablename__ = "vectors"

    start_point = Column(String, primary_key=True, nullable=False)
    end_point = Column(String, primary_key=True, nullable=False)
    length = Column(Float, CheckConstraint('0 <= length'), nullable=True, default=None)

    CheckConstraint('start_point != end_point')


class Angle(Base):
    __tablename__ = "angles"

    start_point1 = Column(String, ForeignKey(Vector.start_point), primary_key=True, nullable=False)
    end_point1 = Column(String, ForeignKey(Vector.end_point), primary_key=True, nullable=False)
    start_point2 = Column(String, ForeignKey(Vector.start_point), primary_key=True, nullable=False)
    end_point2 = Column(String, ForeignKey(Vector.end_point), primary_key=True, nullable=False)
    size = Column(Float, CheckConstraint('0 <= size AND size < 360'), nullable=True, default=None)

    # vector1 = relationship(Vector, foreign_keys=[start_point1, end_point1])
    # vector2 = relationship(Vector, foreign_keys=[start_point2, end_point2])

    CheckConstraint('start_point1 != start_point2 OR end_point1 != end_point2')


class SqlAlchemyInformation(Information):
    def __init__(self, engine):
        Base.metadata.create_all(engine)
        self.__Session = sessionmaker(bind=engine)

    def execute(self, rule):
        with contextlib.closing(self.__Session()) as session:
            rule.execute(session)
