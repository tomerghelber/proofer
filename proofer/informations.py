from abc import ABC, abstractmethod
import contextlib

from sqlalchemy import Column, String, Float, CheckConstraint, create_engine
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
    
    point1 = Column(String, primary_key=True, nullable=False)
    angle_point = Column(String, primary_key=True, nullable=False)
    point2 = Column(String, primary_key=True, nullable=False)
    size = Column(Float, CheckConstraint('0 <= size AND size <= 360'), nullable=True, default=None)
    
    CheckConstraint('point1 != point2 AND point1 != angle_point AND point2 != angle_point')


class SqlAlchemyInformation(Information):
    def __init__(self, engine):
        Base.metadata.create_all(engine)
        self.__Session = sessionmaker(bind=engine)

    def execute(self, rule):
        with contextlib.closing(self.__Session()) as session:
            rule.execute(session)
