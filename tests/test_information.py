from sqlalchemy import create_engine
import pytest

from proofer.informations import SqlAlchemyInformation, Line, Angle

@pytest.fixture
def memory_engine():
    return create_engine('sqlite:///:memory:', echo=True)


@pytest.fixture
def tested_sqlalchemy_information(memory_engine):
    return SqlAlchemyInformation(memory_engine)


def test_sqlalchemy_information_insert_line(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Line(point1='A', point2='B'))

    rule = DummyRule()
    tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(point1='A', angle_point='B', point2='C'))

    rule = DummyRule()
    tested_sqlalchemy_information.execute(rule)

def test_sqlalchemy_information_double_insert_angle(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(point1='A', angle_point='B', point2='C'))
            session.commit()
            session.add(Angle(point1='A', angle_point='B', point2='C'))
            session.commit()

    rule = DummyRule()
    tested_sqlalchemy_information.execute(rule)
