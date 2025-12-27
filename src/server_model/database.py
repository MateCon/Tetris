from abc import ABC, abstractmethod
from server_model.game_result import GameResult
from server_model.session_registry import SessionNotFound
from server_model.user import User
from server_model.session import Session


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
    def insert(self, aSession) -> None:
        pass


class MockSessionRepository(SessionRepository):
    def __init__(self):
        self._sessions = []
        self._hasToFail = False

    def insert(self, aSession):
        self.checkForFailure()
        self._sessions.append(aSession)

    def find(self, anId):
        for session in self._sessions:
            if session.id() == anId:
                return session
        return None

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


class ResultRepository(ABC):
    @abstractmethod
    def insert(self, aGameResult):
        pass

    @abstractmethod
    def selectAll(self) -> list[GameResult]:
        pass


class MockResultRepository(ResultRepository):
    def __init__(self):
        self._results = []

    def insert(self, aGameResult):
        self._results.append(aGameResult)

    def includes(self, aGameResult):
        return aGameResult in self._results

    def selectAll(self):
        return self._results


class Database(ABC):
    @abstractmethod
    def userRepository(self) -> UserRepository:
        pass

    @abstractmethod
    def sessionRepository(self) -> SessionRepository:
        pass

    @abstractmethod
    def resultRepository(self) -> ResultRepository:
        pass


class MockDatabase(Database):
    def __init__(self):
        self._userRepository = MockUserRepository()
        self._sessionRepository = MockSessionRepository()
        self._resultRepository = MockResultRepository()

    def userRepository(self):
        return self._userRepository

    def sessionRepository(self):
        return self._sessionRepository

    def resultRepository(self):
        return self._resultRepository
