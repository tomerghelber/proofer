from contextlib import closing

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from proofer.informations import SqlAlchemyInformation, Line, Angle
from proofer.rules import SumAngles

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
    angle1 = Angle(point1='A', angle_point='B', point2 = 'D', size=30)
    angle2 = Angle(point2=angle1.point2, angle_point=angle1.angle_point, point2='C', size=60)
    
    memory_session.add_all([angle1, angle2])
    memory_session.commit()
    
    tested_rule = SumAngles()
    
    sqlalchemy_information.execute(tested_rule)
    
    result = memory_session.query(Angle).get([angle1.point1, angle1.angle_point, angle2.point2])
    assert result.size == angle1.size + angle2.size
