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
            vector = Vector(start_point='A', end_point='B')
            session.add_all([vector, Angle(vector1=vector, size=-1)])
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
            vector1 = Vector(start_point='A', end_point='B')
            vector2 = Vector(start_point='D', end_point='C')
            session.add_all([vector1, vector2, Angle(vector1=vector1, vector2=vector2)])
            session.commit()

    rule = DummyRule()
    tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_linked_point(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            vector1 = Vector(start_point='A', end_point='B')
            vector2 = Vector(start_point='D', end_point='C')
            session.add_all([vector1, vector2, Angle(vector1=vector1, vector2=vector2)])
            session.commit()

    rule = DummyRule()
    tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_point1_expected(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            session.add(Angle(vector2=Vector(start_point='B', end_point='C')))
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_angle_point_expected(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            vector1 = Vector(start_point='A', end_point='B')
            session.add_all([vector1, Angle(vector1=vector1)])
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_point2_expected(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            vector1 = Vector(start_point='A', end_point='B')
            session.add_all([vector1, Angle(vector1=vector1)])
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_size_negative(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            vector1 = Vector(start_point='A', end_point='B')
            vector2 = Vector(start_point='D', end_point='C')
            session.add_all([vector1, vector2, Angle(vector1=vector1, vector2=vector2, size=-1)])
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_insert_angle_size_too_big(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            vector1 = Vector(start_point='A', end_point='B')
            vector2 = Vector(start_point='D', end_point='C')
            session.add_all([vector1, vector2, Angle(vector1=vector1, vector2=vector2, size=360)])
            session.commit()

    rule = DummyRule()
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)


def test_sqlalchemy_information_double_insert_angle_fails(tested_sqlalchemy_information):
    class DummyRule:
        def execute(self, session):
            vector1 = Vector(start_point='A', end_point='B')
            vector2 = Vector(start_point='D', end_point='C')
            session.add_all([vector1, vector2, Angle(vector1=vector1, vector2=vector2)])
            session.commit()

    rule = DummyRule()
    tested_sqlalchemy_information.execute(rule)
    with pytest.raises(IntegrityError):
        tested_sqlalchemy_information.execute(rule)
