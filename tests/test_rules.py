from sqlalchemy import create_engine

from proofer.informations import SqlAlchemyInformation, Line, Angle
from proofer.rules import SumAngles

import pytest


@pytest.fixture
def memory_engine():
    return create_engine('sqlite:///:memory:')


@pytest.fixture
def sqlalchemy_information(memory_engine):
    return SqlAlchemyInformation(memory_engine)


def test_SumAngles(sqlalchemy_information, memory_engine):
    point1 = 'A'
    angle_point = 'B'
    point2 = 'C'
    size1 = 30
    size2 = 60
    with memory_engine.connect() as connection:
        middle_point = 'D'
        connection.execute(Angle.insert(), {'point1': point1      , 'angle_point': angle_point, 'point2': middle_point, 'size': size1})
        connection.execute(Angle.insert(), {'point1': middle_point, 'angle_point': angle_point, 'point2': point2      , 'size': size2})
    
    tested_rule = SumAngles()
    
    sqlalchemy_information.execute(tested_rule)
    with memory_engine.connect() as connection:
        result = connection.execute(Angle.select(), {'point1': point1, 'angle_point': angle_point, 'point2': point2, 'size': size1 + size2})
        assert 1 == len(result)
