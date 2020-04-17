from proofer.informations import SqlAlchemyInformation, Line, Angle

def test_sqlalchemy_information_insert_line():
    sqlalchemy_information = SqlAlchemyInformation()

    class DummyRule:
        def execute(self, session):
            line = Line('A', 'B')
            session.add(line)

    rule = DummyRule()
    sqlalchemy_information.execute(rule)
