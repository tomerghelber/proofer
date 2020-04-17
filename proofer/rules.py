from abc import ABC, abstractmethod
import collections
from dataclass import dataclass
from itertools import chain
import typing


class Information(ABC):
    @abstractmethod
    def find_all(self, premise: set):
        pass


@dataclass
class Hole:
    id


@dataclass
class Explicit:
    value


class Sqlite3Information(Information):
    def __init__(self):
        self.__conn = sqlite3.connect(':memory:')

    def __set_sqlite3(self):
        cursor = self.__conn.cursor()
        
        # TODO: Should check that size is between 0 and 360
        # TODO: Should check that point1, point2 and angle_point are different.
        lines_table_string = '''CREATE TABLE lines (
            point1 TEXT NOT NULL,
            point2 TEXT NOT NULL,
            size REAL DEFAULT NULL
            CONSTRAINT lines_pk PRIMARY KEY (point1, point2)
        );'''
        cursor.execute(lines_table_string)

        # TODO: Should check that size is between 0 and 360
        # TODO: Should check that point1, point2 and angle_point are different.
        angles_table_string = '''CREATE TABLE angles (
            point1 TEXT NOT NULL,
            angle_point TEXT NOT NULL,
            point2 TEXT NOT NULL,
            size REAL DEFAULT NULL
            CONSTRAINT angles_pk PRIMARY KEY (point1, angle_point, point2)
        );'''
        cursor.execute(angles_table_string)
        
        cursor.commit();

#     def __cell(self, value: typing.Union[Hole, Explicit], name: str) -> typing.Union[typing.Mapping[int, str]], str]:
#         if value is None:
#             return (None, None)
#         if isinstance(Hole, value):
#             return {value.id: name}
#         elif isinstance(Explicit, obj.size):
#             return "{} = '{}'".format(name, value.value)
    
#     def __line_row(self, i: int, line: Line):
#         TABLE = 'lines'
#         table = '{}{}'.format(TABLE, i)
#         select = [table + '.point1',  table + '.point2', table + '.size']
#         where = [
#             self.__cell(line.point1, table + '.point1'),
#             self.__cell(line.point2, table + '.point2'),
#             self.__cell(line.size, table + '.size'),
#         ]
#         return table, select, where
    
#     def __angle_row(self, i: int, angle: Angle):
#         TABLE = 'angles'
#         table = '{}{}'.format(TABLE, i)
#         select = [table + '.point1',  table + '.angle_point', table + '.point2', table + '.size']
#         where = [
#             self.__cell(angle.point1, table + '.point1'),
#             self.__cell(angle.angle_point, table + '.angle_point'),
#             self.__cell(angle.point2, table + '.point2'),
#             self.__cell(angle.size, table + '.size'),
#         ]
#         return table, select, where

#     def __row(self, i, obj):
#         if isinstance(Line, obj):
#             return self.__line_row(i, obj)
#         elif isinstance(Angle, obj):
#             return self.__angle_row(i, obj)

#     def __build_select_statment(self, queries: set) -> str:
#         selects = []
#         tables = []
#         where_dynamic = collections.defaultdict(list)
#         where_static = []

#         for i, obj in enumerate(queries):
#             table, select, wheres = self.__row(i, obj)
#             tables += table
#             selects += select
#             for where in wheres:
#                 if isinstance(where, str):
#                     where_static += [where]
#                 else:
#                     where_id, where_value = where
#                     where_dynamic[where_id] += [where_value]

#         return 'SELECT ' + ', '.join(select) + ' FROM ' + ' JOIN '.join(tables) +\
#           ' WHERE ' + ' AND '.join(chain.from_iterable([where_static] + [map(lambda e: l[0] + ' = ' + e,l[1:]) for l in where]))

    def find_all(self, queries: set):
        raise NotImplemented()
        
          
class Rule(ABC):
    @abstractmethod
    def execute(self, information: Information):
        pass


class SimpleRule(Rule):
    def __init__(self, premise: set, conclusion: typing.Callable[[dict], set], name: typing.Optional[str] = None):
        self.__premise = premise
        self.__conclusion = conclusion
        self.__name = name

    def execute(self, information: Information):
        for result in information.find_all(self.__premise):
            yield self.__conclusion(result)


AngleSum = SimpleRule(
  set(
    Angle(Hole(1), Hole(2), Hole(3), Hole(4)),
    Angle(Hole(3), Hole(2), Hole(5), Hole(6))
  ),
  lambda result: set(Angle(result[1], result[2], result[5], result[4] + result[6]),
  'AngleSum'
)
