from abc import ABC, abstractmethod


class IdGenerator(ABC):
    @abstractmethod
    def nextId(self) -> str:
        pass


class AutoincrementalIdGenerator:
    def __init__(self):
        self.currentId = 0

    def nextId(self):
        id = self.currentId
        self.currentId += 1
        return str(id)
