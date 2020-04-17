from sqlalchemy import create_engine

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
            line = Line('A', 'B')
            session.add(line)

    rule = DummyRule()
    tested_sqlalchemy_information.execute(rule)
