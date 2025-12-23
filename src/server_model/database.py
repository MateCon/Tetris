from abc import ABC, abstractmethod
from server_model.user import User


class UserRepository(ABC):
    @abstractmethod
    def insert(self, aUser) -> None:
        pass

    @abstractmethod
    def selectAll(self) -> list[User]:
        pass


class MockUserRepository(UserRepository):
    def __init__(self):
        self._users = []
        self._hasToFail = False

    def insert(self, aUser):
        self.checkForFailure()
        self._users.append(aUser)

    def selectAll(self):
        return self._users

    def includes(self, aName):
        for user in self._users:
            if user.name() == aName:
                return True
        return False

    def isEmpty(self):
        return len(self._users) == 0

    def failOnNextQuery(self):
        self._hasToFail = True

    def checkForFailure(self):
        if self._hasToFail:
            self._hasToFail = False
            raise Exception


class SessionRepository(ABC):
    @abstractmethod
    def insert(self, aUser) -> None:
        pass


class MockSessionRepository(SessionRepository):
    def __init__(self):
        self._sessions = []
        self._hasToFail = False

    def insert(self, aUser):
        self.checkForFailure()
        self._sessions.append(aUser)

    def includes(self, anId):
        for session in self._sessions:
            if session.id() == anId:
                return True
        return False

    def isEmpty(self):
        return len(self._sessions) == 0

    def size(self):
        return len(self._sessions)

    def failOnNextQuery(self):
        self._hasToFail = True

    def checkForFailure(self):
        if self._hasToFail:
            self._hasToFail = False
            raise Exception


class Database(ABC):
    @abstractmethod
    def userRepository(self) -> UserRepository:
        pass

    @abstractmethod
    def sessionRepository(self) -> SessionRepository:
        pass


class MockDatabase(Database):
    def __init__(self):
        self._userRepository = MockUserRepository()
        self._sessionRepository = MockSessionRepository()

    def userRepository(self):
        return self._userRepository

    def sessionRepository(self):
        return self._sessionRepository
