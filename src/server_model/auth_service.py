class AuthService:
    def __init__(self, aDatabase, aUserBase, aSessionRegistry):
        self.userBase = aUserBase
        self.sessionRegistry = aSessionRegistry
        self.database = aDatabase
        self.userRepository = self.database.userRepository()
        self.sessionRepository = self.database.sessionRepository()

        for user in self.userRepository.selectAll():
            self.userBase.load(user)

    def register(self, aName, aPassword):
        session = self.userBase.register(aName, aPassword)
        user = session.user()

        try:
            self.userRepository.insert(user)
        except Exception:
            self.userBase.remove(aName)
            self.sessionRegistry.remove(session.id())
            raise

        try:
            self.sessionRepository.insert(session)
        except Exception:
            self.sessionRegistry.remove(session.id())
            raise

        return session

    def login(self, aName, aPassword):
        session = self.userBase.login(aName, aPassword)

        try:
            self.sessionRepository.insert(session)
        except Exception:
            self.sessionRegistry.remove(session.id())
            raise

        return session

    def verifySession(self, aSessionId):
        self.sessionRegistry.verifyWith(aSessionId, self.database.sessionRepository())

