class ResultService:
    def __init__(self, aDatabase, anAuthService, aClock):
        self.database = aDatabase
        self.authService = anAuthService
        self.clock = aClock
        self.sessionRepository = self.database.sessionRepository()
        self.resultRepository = self.database.resultRepository()

    def save(self, aSessionId, aScore, aLevel, anAmmountOfLines, aTimeInMilliseconds):
        self.authService.verifySession(aSessionId)

        if aScore < 5000:
            raise ScoreTooLow

        session = self.sessionRepository.find(aSessionId)
        currentDate = self.clock.now()

        self.resultRepository.insert(session.user().name(), aScore, aLevel, anAmmountOfLines, currentDate, aTimeInMilliseconds)


class ScoreTooLow(Exception):
    pass
