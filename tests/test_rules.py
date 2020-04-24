from contextlib import closing

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from proofer.informations import SqlAlchemyInformation, Vector, Angle
from proofer.rules import SumAngles, SumVectors, ReverseAngle

import pytest


@pytest.fixture
def memory_engine():
    return create_engine('sqlite:///:memory:')


@pytest.fixture
def memory_session(memory_engine):
    with closing(sessionmaker(memory_engine)()) as session:
        yield session


@pytest.fixture
def sqlalchemy_information(memory_engine):
    return SqlAlchemyInformation(memory_engine)


def test_SumAngles(sqlalchemy_information, memory_session):
    angle1 = Angle(start_point1='A', end_point1='B', start_point2='C', end_point2='D', size=30)
    angle2 = Angle(start_point1=angle1.start_point2, end_point1=angle1.end_point2, start_point2='E', end_point2='F', size=60)

    memory_session.add_all([angle1, angle2])
    memory_session.commit()

    tested_rule = SumAngles()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Angle).all()) == 3
    result = memory_session.query(Angle).get([angle1.start_point1, angle1.end_point1, angle2.start_point2, angle2.end_point2])
    assert result.size == angle1.size + angle2.size


def test_SumAngles_on_first_empty_adds_nothing(sqlalchemy_information, memory_session):
    angle1 = Angle(start_point1='A', end_point1='B', start_point2='C', end_point2='D')
    angle2 = Angle(start_point1=angle1.start_point2, end_point1=angle1.end_point2, start_point2='E', end_point2='F', size=60)

    memory_session.add_all([angle1, angle2])
    memory_session.commit()

    tested_rule = SumAngles()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Angle).all()) == 2


def test_SumAngles_on_second_empty_adds_nothing(sqlalchemy_information, memory_session):
    angle1 = Angle(start_point1='A', end_point1='B', start_point2='C', end_point2='D', size=30)
    angle2 = Angle(start_point1=angle1.start_point2, end_point1=angle1.end_point2, start_point2='E', end_point2='F')

    memory_session.add_all([angle1, angle2])
    memory_session.commit()

    tested_rule = SumAngles()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Angle).all()) == 2


def test_ReverseAngle(sqlalchemy_information, memory_session):
    angle = Angle(start_point1='A', end_point1='B', start_point2='C', end_point2='D', size=30)

    memory_session.add(angle)
    memory_session.commit()

    tested_rule = ReverseAngle()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Angle).all()) == 2
    result = memory_session.query(Angle).get([angle.start_point2, angle.end_point2, angle.start_point1, angle.end_point1])
    assert result.size == 360 - angle.size


def test_ReverseAngle(sqlalchemy_information, memory_session):
    angle = Angle(start_point1='A', end_point1='B', start_point2='C', end_point2='D')

    memory_session.add(angle)
    memory_session.commit()

    tested_rule = ReverseAngle()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Angle).all()) == 1


def test_SumVectors(sqlalchemy_information, memory_session):
    vector1 = Vector(start_point='A', end_point='B', length=2)
    vector2 = Vector(start_point=vector1.end_point, end_point='C', length=3)
    angle = Angle(start_point1=vector1.start_point, end_point1=vector1.end_point, start_point2=vector2.start_point, end_point2=vector2.end_point, size=180)

    memory_session.add_all([angle, vector1, vector2])
    memory_session.commit()

    tested_rule = SumVectors()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Angle).all()) == 1
    assert len(memory_session.query(Vector).all()) == 3
    result = memory_session.query(Vector).get([vector1.start_point, vector2.end_point])
    assert result.length == vector1.length + vector2.length


def test_SumVectors_on_first_empty_adds_nothing(sqlalchemy_information, memory_session):
    vector1 = Vector(start_point='A', end_point='B')
    vector2 = Vector(start_point=vector1.end_point, end_point='C', length=3)
    angle = Angle(start_point1=vector1.start_point, end_point1=vector1.end_point, start_point2=vector2.start_point, end_point2=vector2.end_point, size=180)

    memory_session.add_all([angle, vector1, vector2])
    memory_session.commit()

    tested_rule = SumVectors()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Angle).all()) == 1
    assert len(memory_session.query(Vector).all()) == 2


def test_SumVectors_on_second_empty_adds_nothing(sqlalchemy_information, memory_session):
    vector1 = Vector(start_point='A', end_point='B', length=2)
    vector2 = Vector(start_point=vector1.end_point, end_point='C')
    angle = Angle(start_point1=vector1.start_point, end_point1=vector1.end_point, start_point2=vector2.start_point, end_point2=vector2.end_point, size=180)

    memory_session.add_all([angle, vector1, vector2])
    memory_session.commit()

    tested_rule = SumVectors()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Angle).all()) == 1
    assert len(memory_session.query(Vector).all()) == 2
