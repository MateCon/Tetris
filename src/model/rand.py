from abc import ABC, abstractmethod
import random


class RandomIntStream(ABC):
    @abstractmethod
    def nextInteger(self, min, max) -> int:
        pass


class Rand(RandomIntStream):
    def nextInteger(self, min, max):
        return random.randint(min, max)


class RandStub(RandomIntStream):
    def __init__(self, someValues):
        self.values = someValues
        self.values.reverse()

    def nextInteger(self, min, max):
        return self.values.pop()
