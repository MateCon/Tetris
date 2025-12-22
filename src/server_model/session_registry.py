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


class SessionNotFound(Exception):
    pass


class SessionExpired(Exception):
    pass
