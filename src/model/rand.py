from abc import ABC, abstractmethod
import random


class RandomIntStream(ABC):
    @abstractmethod
    def nextInteger(self, min, max) -> int:
        pass

    @abstractmethod
    def nextOrdering(self, length) -> list[int]:
        pass


class Rand(RandomIntStream):
    def nextInteger(self, min, max):
        return random.randint(min, max)

    def nextOrdering(self, length):
        ordering = [n for n in range(length)]
        random.shuffle(ordering)
        return ordering


class RandStub(RandomIntStream):
    def __init__(self, someValues):
        self.values = someValues + [1 for _ in range(14)]
        self.values.reverse()

    def nextInteger(self, min, max):
        return self.values.pop()

    def nextOrdering(self, length):
        return [self.values.pop() for _ in range(7)]
