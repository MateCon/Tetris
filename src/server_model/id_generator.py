from abc import ABC, abstractmethod
from secrets import token_urlsafe


class IdGenerator(ABC):
    @abstractmethod
    def nextId(self) -> str:
        pass


class SecretIdGenerator(IdGenerator):  # pragma: no cover
    def nextId(self):
        return token_urlsafe(32)


class AutoincrementalIdGenerator(IdGenerator):
    def __init__(self):
        self.currentId = 0

    def nextId(self):
        id = self.currentId
        self.currentId += 1
        return str(id)
