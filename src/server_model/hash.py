from abc import ABC, abstractmethod


class HashStrategy(ABC):
    @abstractmethod
    def hash(self, aString) -> str:
        pass

    @abstractmethod
    def verify(self, aHashedString, aString) -> bool:
        pass


class HashStub(HashStrategy):
    def hash(self, aString):
        return ''.join([chr(ord(char) + 1) for char in aString])

    def verify(self, aHashedString, aString):
        return aHashedString == self.hash(aString)
