from server_model.session_registry import SessionRegistry
from server_model.user_base import UserBase


class AuthService:
    def __init__(self, aDatabase, aClock, anIdGenerator, aHashStategy):
        self._sessionRegistry = SessionRegistry(aClock, anIdGenerator)
        self._userBase = UserBase(self._sessionRegistry, aHashStategy)
        self.database = aDatabase
        self.userRepository = self.database.userRepository()
        self.sessionRepository = self.database.sessionRepository()

        for user in self.userRepository.selectAll():
            self._userBase.load(user)

    def register(self, aName, aPassword):
        session = self._userBase.register(aName, aPassword)
        user = session.user()

        try:
            self.userRepository.insert(user)
        except Exception:
            self._userBase.remove(aName)
            self._sessionRegistry.remove(session.id())
            raise

        try:
            self.sessionRepository.insert(session)
        except Exception:
            self._sessionRegistry.remove(session.id())
            raise

        return session

    def login(self, aName, aPassword):
        session = self._userBase.login(aName, aPassword)

        try:
            self.sessionRepository.insert(session)
        except Exception:
            self._sessionRegistry.remove(session.id())
            raise

        return session

    def verifySession(self, aSessionId):
        self._sessionRegistry.verifyWith(aSessionId, self.database.sessionRepository())

    def userBase(self):
        return self._userBase

    def sessionRegistry(self):
        return self._sessionRegistry

