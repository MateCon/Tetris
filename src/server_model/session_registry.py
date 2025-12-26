from server_model.session import Session


class SessionRegistry:
    def __init__(self, aClock, anIdGenerator):
        self._sessions = []
        self._clock = aClock
        self._idGenerator = anIdGenerator

    def createSessionFor(self, aUser):
        session = Session(self._idGenerator.nextId(), aUser, self._clock.now(), self._clock.aWeek())
        self._sessions.append(session)
        return session

    def verify(self, aSessionId):
        for session in self._sessions:
            if session.id() == aSessionId:
                if self._clock.now() >= session.expirationDate():
                    raise SessionExpired
                return
        raise SessionNotFound

    def verifyWith(self, aSessionId, aSessionRepository):
        session = aSessionRepository.find(aSessionId)
        if session is None:
            raise SessionNotFound
        if self._clock.now() >= session.expirationDate():
            raise SessionExpired

    def load(self, aSession):
        self._sessions.append(aSession)

    def size(self):
        return len(self._sessions)

    def isEmpty(self):
        return len(self._sessions) == 0

    def remove(self, anId):
        for session in self._sessions:
            if session.id() == anId:
                return self._sessions.remove(session)


class SessionNotFound(Exception):
    pass


class SessionExpired(Exception):
    pass
