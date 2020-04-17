from abc import ABC, abstractmethod
from itertools import chain
import typing

from informations import Information, Angle, Line

          
class Rule(ABC):
    @abstractmethod
    def execute(self, information: Information):
        pass


class SimpleRule(Rule):
    def __init__(self, query: set, name: typing.Optional[str] = None):
        self.__query = query
        self.__conclusion = conclusion
        self.__name = name

    def execute(self, information: Information):
        for result in information.find_all(self.__query):
            yield self.__conclusion(result)


# Sum angles
# INESET INTO angles (point1, angle_point, point2, size)
# SELECT angles1.point1 as point1, angles1.angle_point as angle_point, angles2.point2 as point2, angles1.size + angles2.size as size
# FROM angles angles1, angles angles2
# WHERE angles1.angle_point == angles2.angle_point AND angles1.point2 == angles2.point1;
