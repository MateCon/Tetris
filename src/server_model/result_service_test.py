from server_model.user_base import UserBase
from server_model.session_registry import SessionNotFound, SessionRegistry
from server_model.hash import HashStub
from server_model.clock import ClockStub
from server_model.id_generator import AutoincrementalIdGenerator
from server_model.database import MockDatabase
from server_model.auth_service import AuthService
from server_model.result_service import ResultService, ScoreTooLow
import pytest


class TestResultService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.clock = ClockStub(2025, 12, 23)
        self.sessionRegistry = SessionRegistry(self.clock, AutoincrementalIdGenerator())
        self.userBase = UserBase(self.sessionRegistry, HashStub())
        self.db = MockDatabase()
        self.authService = AuthService(self.db, self.userBase, self.sessionRegistry)
        self.resultService = ResultService(self.db, self.authService, self.clock)

    def test01_ResultIsSavedInTheDatabase(self):
        self.authService.register("Jack", "password")

        self.resultService.save("0", 5000, 4, 38, 61938)

        assert self.db.resultRepository().includes("Jack", 5000, 4, 38, self.clock.now(), 61938)

    def test02_ResultIsNotSavedInTheDatabaseIfTheScoreIsUnderMinimum(self):
        self.authService.register("Jack", "password")

        with pytest.raises(ScoreTooLow):
            self.resultService.save("0", 4999, 6, 52, 54200)

        assert not self.db.resultRepository().includes("Jack", 5000, 4, 38, self.clock.now(), 61938)

    def test03_ResultIsNotSavedInTheDatabaseIfTheSessionIsInvalid(self):
        with pytest.raises(SessionNotFound):
            self.resultService.save("0", 5000, 4, 38, 61938)

        assert not self.db.resultRepository().includes("Jack", 5000, 4, 38, self.clock.now(), 61938)

    def test04_ResultIsSavedIfTheSessionWasCreatedBeforeTheService(self):
        self.authService.register("Jack", "password")

        sessionRegistry = SessionRegistry(self.clock, AutoincrementalIdGenerator())
        userBase = UserBase(sessionRegistry, HashStub())
        authService = AuthService(self.db, userBase, sessionRegistry)
        resultService = ResultService(self.db, authService, self.clock)

        resultService.save("0", 5000, 4, 38, 61938)

        assert self.db.resultRepository().includes("Jack", 5000, 4, 38, self.clock.now(), 61938)
