from abc import ABC, abstractmethod

from sqlalchemy import Column, String, Float, CheckConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Information(ABC):
    @abstractmethod
    def find_all(self, query):
        pass


Base = declarative_base()


class Line(Base):
    __tablename__ = "lines"
    
    point1 = Column(String, primary_key=True, nullable=False)
    point2 = Column(String, primary_key=True, nullable=False)
    size = Column(Float, nullable=True, default=None, CheckConstraint('0 =< size AND size <= 360'))
    
    CheckConstraint('point1 != point2')


class Angle(Base):
    __tablename__ = "angles"
    
    point1 = Column(String, primary_key=True, nullable=False)
    angle_point = Column(String, primary_key=True, nullable=False)
    point2 = Column(String, primary_key=True, nullable=False)
    size = Column(Float, nullable=True, default=None, CheckConstraint('0 =< size AND size <= 360'))
    
    CheckConstraint('point1 != point2 AND point1 != angle_point AND point2 != angle_point')


class SqlAlchemyInformation(Information):
    def __init__(self):
        self.__engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)

    def find_all(self, query):
        connection = self.__engine.connect()
        select = query.select()
        result = connection.execute(select)
        return result.fetchall()