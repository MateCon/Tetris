from abc import ABC, abstractmethod
import random


class RandomOrderingStream(ABC):
    @abstractmethod
    def nextOrdering(self, length) -> list[int]:
        pass


class Rand(RandomOrderingStream):  # pragma: no cover
    def nextOrdering(self, length):
        ordering = [n for n in range(length)]
        random.shuffle(ordering)
        return ordering


class RandStub(RandomOrderingStream):
    def __init__(self, someValues):
        self.values = someValues + [1 for _ in range(14)]
        self.values.reverse()

    def nextOrdering(self, length):
        return [self.values.pop() for _ in range(7)]
