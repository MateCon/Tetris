from server_model.leaderboard import Leaderboard
from server_model.game_result import GameResult


class ResultService:
    def __init__(self, aDatabase, anAuthService, aClock):
        self._database = aDatabase
        self._authService = anAuthService
        self._clock = aClock
        self._sessionRepository = self._database.sessionRepository()
        self._resultRepository = self._database.resultRepository()
        self._leaderboard = Leaderboard()

        for user in self._resultRepository.selectAll():
            self._leaderboard.save(user)

    def save(self, aSessionId, aScore, aLevel, anAmmountOfLines, aTimeInMilliseconds):
        self._authService.verifySession(aSessionId)

        if aScore < 5000:
            raise ScoreTooLow

        session = self._sessionRepository.find(aSessionId)
        currentDate = self._clock.now()

        gameResult = GameResult(session.user(), aScore, aLevel, anAmmountOfLines, currentDate, aTimeInMilliseconds)

        self._resultRepository.insert(gameResult)
        self._leaderboard.save(gameResult)

    def leaderboard(self):
        return self._leaderboard


class ScoreTooLow(Exception):
    pass
