from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
import pytest

from proofer.informations import SqlAlchemyInformation, Line, Angle

@pytest.fixture
def memory_engine():
    return create_engine('sqlite:///:memory:')


@pytest.fixture
def tested_sqlalchemy_information(memory_engine):
    return SqlAlchemyInformation(memory_engine)


def test_sqlalchemy_information_insert_line(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Line(point1='A', point2='B'))
            session.commit()

    rule = DummyRule()
    tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_line_point1_expected(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Line(point2='B'))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_line_point2_expected(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Line(point2='B'))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_size_negative(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(point1='A', point2='B', size=-1))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_double_insert_line_fails(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Line(point1='A', point2='B'))
            session.commit()

    rule = DummyRule()
    tested_sqlalchemy_information.execute(rule)
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(point1='A', angle_point='B', point2='C'))
            session.commit()

    rule = DummyRule()
    tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_point1_expected(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(angle_point='B', point2='C'))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_angle_point_expected(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(point1='A', point2='C'))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_point2_expected(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(point1='A', angle_point='B'))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_size_negative(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(point1='A', angle_point='B', point2='C', size=-1))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_size_too_big(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(point1='A', angle_point='B', point2='C', size=-361))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_double_insert_angle_fails(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(point1='A', angle_point='B', point2='C'))
            session.commit()

    rule = DummyRule()
    tested_sqlalchemy_information.execute(rule)
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)
