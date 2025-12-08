from abc import ABC, abstractmethod


class Rand(ABC):
    @abstractmethod
    def nextInteger(self):
        pass


class RandStub(Rand):
    def __init__(self, someValues):
        self.values = someValues

    def nextInteger(self):
        return self.values.pop(0)
