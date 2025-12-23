from abc import ABC, abstractmethod
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError 


class HashStrategy(ABC):
    @abstractmethod
    def hash(self, aString) -> str:
        pass

    @abstractmethod
    def verify(self, aHashedString, aString) -> bool:
        pass


class ArgonHash(HashStrategy):  # pragma: no cover
    def __init__(self):
        self.hasher = PasswordHasher()

    def hash(self, aString):
        return self.hasher.hash(aString)

    def verify(self, aHashedString, aString):
        try:
            self.hasher.verify(aHashedString, aString)
            return True
        except VerifyMismatchError:
            return False



class HashStub(HashStrategy):
    def hash(self, aString):
        return ''.join([chr(ord(char) + 1) for char in aString])

    def verify(self, aHashedString, aString):
        return aHashedString == self.hash(aString)
