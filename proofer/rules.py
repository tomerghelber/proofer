from abc import ABC, abstractmethod
import typing


class Rule(ABC):
    @abstractmethod
    def execute(self, information):
        pass


class SimpleRule(Rule):
    def __init__(self, premise: set, conclusion: typing.Callable[[dict], set], name: typing.Optional[str] = None):
        self.__premise = premise
        self.__conclusion = conclusion
        self.__name = name

    def execute(self, information):
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
