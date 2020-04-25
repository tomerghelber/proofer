from abc import ABC, abstractmethod
import contextlib

from sqlalchemy import Column, String, Float, CheckConstraint, ForeignKey, Integer, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


class Information(ABC):
    @abstractmethod
    def execute(self, rule):
        pass


Base = declarative_base()


class ProofedObject(Base):
    __tablename__ = "proofed_objects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    discriminator = Column(String(50))

    __mapper_args__ = {'polymorphic_on': discriminator}


class Vector(ProofedObject):
    __tablename__ = "vectors"

    id = Column(Integer, ForeignKey(ProofedObject.id), primary_key=True, autoincrement=True)

    start_point = Column(String, nullable=False)
    end_point = Column(String, nullable=False)
    length = Column(Float, CheckConstraint('0 <= length'), nullable=True, default=None)

    UniqueConstraint(start_point, end_point)
    CheckConstraint('start_point != end_point')
    __table_args__ = (Index('vector_point_index', start_point, end_point),)

    def __repr__(self):
        return f"Vector({self.start_point}, {self.end_point}, {self.length})"


class Angle(ProofedObject):
    __tablename__ = "angles"

    id = Column(Integer, ForeignKey(ProofedObject.id), primary_key=True, autoincrement=True)

    vector_id1 = Column(Integer, ForeignKey(Vector.id), nullable=False)
    vector_id2 = Column(Integer, ForeignKey(Vector.id), nullable=False)
    size = Column(Float, CheckConstraint('0 <= size AND size < 360'), nullable=True, default=None)

    vector1 = relationship(Vector, foreign_keys=vector_id1)
    vector2 = relationship(Vector, foreign_keys=vector_id2)

    UniqueConstraint(vector_id1, vector_id2)
    CheckConstraint('vector_id1 != vector_id2')
    __table_args__ = (Index('angle_point_index', vector_id1, vector_id2),)

    def __repr__(self):
        return f"Angle({self.vector1}, {self.vector2}, {self.size})"


class SqlAlchemyInformation(Information):
    def __init__(self, engine):
        Base.metadata.create_all(engine)
        self.__Session = sessionmaker(bind=engine)

    def execute(self, rule):
        with contextlib.closing(self.__Session()) as session:
            rule.execute(session)
