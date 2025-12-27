from server_model.user_base import UserBase
from server_model.session_registry import SessionNotFound, SessionRegistry
from server_model.hash import HashStub
from server_model.clock import ClockStub
from server_model.id_generator import AutoincrementalIdGenerator
from server_model.database import MockDatabase
from server_model.auth_service import AuthService
from server_model.result_service import ResultService, ScoreTooLow
from server_model.game_result import GameResult
import pytest


class TestResultService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.clock = ClockStub(2025, 12, 23)
        self.sessionRegistry = SessionRegistry(self.clock, AutoincrementalIdGenerator())
        self.userBase = UserBase(self.sessionRegistry, HashStub())
        self.db = MockDatabase()
        self.authService = AuthService(self.db, self.clock, AutoincrementalIdGenerator(), HashStub())
        self.resultService = ResultService(self.db, self.authService, self.clock)

    def test01_ResultIsSavedInTheDatabase(self):
        session = self.authService.register("Jack", "password")
        expectedResult = GameResult(session.user(), 5000, 4, 38, self.clock.now(), 61938)

        self.resultService.save("0", 5000, 4, 38, 61938)

        assert self.db.resultRepository().includes(expectedResult)

    def test02_ResultIsNotSavedInTheDatabaseIfTheScoreIsUnderMinimum(self):
        session = self.authService.register("Jack", "password")
        expectedResult = GameResult(session.user(), 5000, 4, 38, self.clock.now(), 61938)

        with pytest.raises(ScoreTooLow):
            self.resultService.save("0", 4999, 6, 52, 54200)

        assert not self.db.resultRepository().includes(expectedResult)

    def test03_ResultIsNotSavedInTheDatabaseIfTheSessionIsInvalid(self):
        session = self.authService.register("Jack", "password")
        expectedResult = GameResult(session.user(), 5000, 4, 38, self.clock.now(), 61938)

        with pytest.raises(SessionNotFound):
            self.resultService.save("1", 5000, 4, 38, 61938)

        assert not self.db.resultRepository().includes(expectedResult)

    def test04_ResultIsSavedIfTheSessionWasCreatedBeforeTheService(self):
        session = self.authService.register("Jack", "password")

        authService = AuthService(self.db, self.clock, AutoincrementalIdGenerator(), HashStub())
        resultService = ResultService(self.db, authService, self.clock)
        expectedResult = GameResult(session.user(), 5000, 4, 38, self.clock.now(), 61938)

        resultService.save("0", 5000, 4, 38, 61938)

        assert self.db.resultRepository().includes(expectedResult)

    def test05_LeaderboardStartsEmptyIfTheDatabaseHasNoResults(self):
        assert self.resultService.leaderboard().size() == 0

    def test06_FirstResultAddedAppearsOnLeaderboard(self):
        session = self.authService.register("Jack", "password")

        self.resultService.save(session.id(), 5000, 4, 38, 61938)

        assert self.resultService.leaderboard().size() == 1
        assert self.resultService.leaderboard().at(0).score == 5000

    def test07_IsAResultFromANewUserIsSavedItAppearsOnTheLeaderboard(self):
        firstSession = self.authService.register("Jack", "password")
        secondSession = self.authService.register("John", "123")

        self.resultService.save(firstSession.id(), 6000, 4, 38, 61938)
        self.resultService.save(secondSession.id(), 5000, 4, 38, 61938)

        assert self.resultService.leaderboard().size() == 2
        assert self.resultService.leaderboard().at(0).score == 6000
        assert self.resultService.leaderboard().at(1).score == 5000

    def test08_AResultFromTheSecondUserAppearsOnTheLeaderboardInTheRightPosition(self):
        firstSession = self.authService.register("Jack", "password")
        secondSession = self.authService.register("John", "123")

        self.resultService.save(secondSession.id(), 5000, 4, 38, 61938)
        self.resultService.save(firstSession.id(), 6000, 4, 38, 61938)

        assert self.resultService.leaderboard().size() == 2
        assert self.resultService.leaderboard().at(0).score == 6000
        assert self.resultService.leaderboard().at(1).score == 5000

    def test09_AResultFromAnyUserAppearsOnTheLeaderboardInTheRightPosition(self):
        firstSession = self.authService.register("Jack", "password")
        secondSession = self.authService.register("John", "123")
        thirdSession = self.authService.register("Charlie", "boat")

        self.resultService.save(firstSession.id(), 5000, 4, 38, 61938)
        self.resultService.save(secondSession.id(), 7000, 4, 38, 61938)
        self.resultService.save(thirdSession.id(), 6000, 4, 38, 61938)

        assert self.resultService.leaderboard().size() == 3
        assert self.resultService.leaderboard().at(0).score == 7000
        assert self.resultService.leaderboard().at(1).score == 6000
        assert self.resultService.leaderboard().at(2).score == 5000

    def test10_IfThereIsATieOnTheLeaderboardTheOlderResultIsFavored(self):
        firstSession = self.authService.register("Jack", "password")
        secondSession = self.authService.register("John", "123")

        self.resultService.save(secondSession.id(), 5000, 5, 42, 61938)
        self.resultService.save(firstSession.id(), 5000, 4, 38, 61938)

        assert self.resultService.leaderboard().size() == 2
        assert self.resultService.leaderboard().at(0).level == 5
        assert self.resultService.leaderboard().at(1).level == 4

    def test11_IfTheResultIsNotANewBestItDoesNotAppearOnTheLeaderboard(self):
        session = self.authService.register("Jack", "password")

        self.resultService.save(session.id(), 6000, 4, 38, 61938)
        self.resultService.save(session.id(), 5000, 4, 38, 61938)

        assert self.resultService.leaderboard().size() == 1
        assert self.resultService.leaderboard().at(0).score == 6000

    def test12_IfTheResultIsIsANewBestOverridesThePreviousBestOnTheLeaderboard(self):
        session = self.authService.register("Jack", "password")

        self.resultService.save(session.id(), 5000, 4, 38, 61938)
        self.resultService.save(session.id(), 6000, 4, 38, 61938)

        assert self.resultService.leaderboard().size() == 1
        assert self.resultService.leaderboard().at(0).score == 6000

    def test13_LeaderboardStartsWithTheResultsFromTheDatabase(self):
        session = self.authService.register("Jack", "password")
        self.resultService.save(session.id(), 5000, 4, 38, 61938)
        authService = AuthService(self.db, ClockStub(2025, 12, 23), AutoincrementalIdGenerator(), HashStub())

        resultService = ResultService(self.db, authService, self.clock)

        assert resultService.leaderboard().size() == 1
        assert resultService.leaderboard().at(0).score == 5000
