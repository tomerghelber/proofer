from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
import pytest

from proofer.informations import SqlAlchemyInformation, Vector, Angle

@pytest.fixture
def memory_engine():
    return create_engine('sqlite:///:memory:')


@pytest.fixture
def tested_sqlalchemy_information(memory_engine):
    return SqlAlchemyInformation(memory_engine)


def test_sqlalchemy_information_insert_line(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Vector(start_point='A', end_point='B'))
            session.commit()

    rule = DummyRule()
    tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_line_point1_expected(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Vector(end_point='B'))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_line_point2_expected(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Vector(end_point='B'))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_size_negative(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(start_point1='A', end_point2='B', size=-1))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_double_insert_line_fails(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Vector(start_point='A', end_point='B'))
            session.commit()

    rule = DummyRule()
    tested_sqlalchemy_information.execute(rule)
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(start_point1='A', end_point1='B', start_point2='D', end_point2='C'))
            session.commit()

    rule = DummyRule()
    tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_linked_point(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(start_point1='A', end_point1='B', start_point2='B', end_point2='C'))
            session.commit()

    rule = DummyRule()
    tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_point1_expected(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(start_point2='B', end_point2='C'))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_angle_point_expected(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(start_point1='A', end_point2='C'))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_point2_expected(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(start_point1='A', end_point1='B'))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_size_negative(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(start_point1='A', end_point1='B', start_point2='B', end_point2='C', size=-1))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_size_too_big(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(start_point1='A', end_point1='B', start_point2='B', end_point2='C', size=-361))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_double_insert_angle_fails(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(start_point1='A', end_point1='B', start_point2='B', end_point2='C'))
            session.commit()

    rule = DummyRule()
    tested_sqlalchemy_information.execute(rule)
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)
