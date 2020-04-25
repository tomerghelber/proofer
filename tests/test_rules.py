from contextlib import closing

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from proofer.informations import SqlAlchemyInformation, Vector, Angle
from proofer.rules import SumAngles, SumVectors, ReverseAngle, ReverseVector

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
    angle1 = Angle(vector1=Vector(start_point='A', end_point='B'), vector2=Vector(start_point='C', end_point='D'), size=30)
    angle2 = Angle(vector1=angle1.vector2, vector2=Vector(start_point='E', end_point='F'), size=60)

    memory_session.add_all([angle1, angle2])
    memory_session.commit()

    tested_rule = SumAngles()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Angle).all()) == 3
    result = memory_session.query(Angle).filter_by(vector_id1=angle1.vector_id1, vector_id2=angle2.vector_id2).first()
    assert result.size == angle1.size + angle2.size


def test_SumAngles_on_first_empty_adds_nothing(sqlalchemy_information, memory_session):
    angle1 = Angle(vector1=Vector(start_point='A', end_point='B'), vector2=Vector(start_point='C', end_point='D'))
    angle2 = Angle(vector1=angle1.vector2, vector2=Vector(start_point='E', end_point='F'), size=60)

    memory_session.add_all([angle1, angle2])
    memory_session.commit()

    tested_rule = SumAngles()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Angle).all()) == 2


def test_SumAngles_on_second_empty_adds_nothing(sqlalchemy_information, memory_session):
    angle1 = Angle(vector1=Vector(start_point='A', end_point='B'), vector2=Vector(start_point='C', end_point='D'), size=30)
    angle2 = Angle(vector1=angle1.vector2, vector2=Vector(start_point='E', end_point='F'))

    memory_session.add_all([angle1, angle2])
    memory_session.commit()

    tested_rule = SumAngles()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Angle).all()) == 2


def test_ReverseAngle(sqlalchemy_information, memory_session):
    angle = Angle(vector1=Vector(start_point='A', end_point='B'), vector2=Vector(start_point='C', end_point='D'), size=30)

    memory_session.add(angle)
    memory_session.commit()

    tested_rule = ReverseAngle()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Angle).all()) == 2
    result = memory_session.query(Angle).filter_by(vector1=angle.vector2, vector2=angle.vector1).first()
    assert result.size == 360 - angle.size


def test_ReverseAngle_on_null_empty_size_not_adding(sqlalchemy_information, memory_session):
    angle = Angle(vector1=Vector(start_point='A', end_point='B'), vector2=Vector(start_point='C', end_point='D'))

    memory_session.add(angle)
    memory_session.commit()

    tested_rule = ReverseAngle()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Angle).all()) == 1


def test_ReverseVector(sqlalchemy_information, memory_session):
    vector = Vector(start_point='A', end_point='B', length=1)

    memory_session.add(vector)
    memory_session.commit()

    tested_rule = ReverseVector()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Vector).all()) == 2
    result = memory_session.query(Vector).get(vector.id)
    assert result.length == vector.length


def test_ReverseVector_on_null_adds_reverse(sqlalchemy_information, memory_session):
    vector = Vector(start_point='A', end_point='B')

    memory_session.add(vector)
    memory_session.commit()

    tested_rule = ReverseVector()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Vector).all()) == 2
    result = memory_session.query(Vector).get(vector.id)
    assert result.length == vector.length


def test_SumVectors(sqlalchemy_information, memory_session):
    vector1 = Vector(start_point='A', end_point='B', length=2)
    vector2 = Vector(start_point=vector1.end_point, end_point='C', length=3)
    angle = Angle(vector1=vector1, vector2=vector2, size=180)

    memory_session.add_all([angle, vector1, vector2])
    memory_session.commit()

    tested_rule = SumVectors()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Angle).all()) == 1
    assert len(memory_session.query(Vector).all()) == 3
    result = memory_session.query(Vector).filter_by(start_point=vector1.start_point, end_point=vector2.end_point).first()
    assert result.length == vector1.length + vector2.length


def test_SumVectors_on_first_empty_adds_nothing(sqlalchemy_information, memory_session):
    vector1 = Vector(start_point='A', end_point='B')
    vector2 = Vector(start_point=vector1.end_point, end_point='C', length=3)
    angle = Angle(vector1=vector1, vector2=vector2, size=180)

    memory_session.add_all([angle, vector1, vector2])
    memory_session.commit()

    tested_rule = SumVectors()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Angle).all()) == 1
    assert len(memory_session.query(Vector).all()) == 2


def test_SumVectors_on_second_empty_adds_nothing(sqlalchemy_information, memory_session):
    vector1 = Vector(start_point='A', end_point='B', length=2)
    vector2 = Vector(start_point=vector1.end_point, end_point='C')
    angle = Angle(vector1=vector1, vector2=vector2, size=180)

    memory_session.add_all([angle, vector1, vector2])
    memory_session.commit()

    tested_rule = SumVectors()

    sqlalchemy_information.execute(tested_rule)

    assert len(memory_session.query(Angle).all()) == 1
    assert len(memory_session.query(Vector).all()) == 2
