from server_model.user_base import UserBase
from server_model.user import User, NameTooShort
from server_model.session_registry import SessionRegistry
from server_model.hash import HashStub
from server_model.clock import ClockStub
from server_model.id_generator import AutoincrementalIdGenerator
from server_model.database import MockDatabase
from server_model.auth_service import AuthService
import pytest


class TestAuthService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.sessionRegistry = SessionRegistry(ClockStub(2025, 12, 23), AutoincrementalIdGenerator())
        self.hashStrategy = HashStub()
        self.userBase = UserBase(self.sessionRegistry, self.hashStrategy)
        self.db = MockDatabase()
        self.authService = AuthService(self.db, self.userBase, self.sessionRegistry)

    def test01a_UserCanBeRegistered(self):
        self.authService.register("Jack", "password")

        assert self.userBase.includes("Jack")
        assert self.db.userRepository().includes("Jack")

    def test01b_WhenAUserRegistersASessionIsCreated(self):
        session = self.authService.register("Jack", "password")

        assert session.user().name() == "Jack"
        assert self.db.sessionRepository().includes(session.id())

    def test02_IfAUserCanNotBeRegisteredItIsNotStoredInTheDatabase(self):
        with pytest.raises(NameTooShort):
            self.authService.register("Ja", "password")

        assert not self.userBase.includes("Jack")
        assert not self.db.userRepository().includes("Ja")

    def test03_IfTheDatabaseFailsAddingTheUserNothingIsStored(self):
        self.db.userRepository().failOnNextQuery()

        with pytest.raises(Exception):
            self.authService.register("Jack", "password")

        assert self.userBase.isEmpty()
        assert self.db.userRepository().isEmpty()
        assert self.sessionRegistry.isEmpty()
        assert self.db.sessionRepository().isEmpty()

    def test04_IfTheDatabaseFailsAddingTheSessionTheItIsNotStoredInTheRegistry(self):
        self.db.sessionRepository().failOnNextQuery()

        with pytest.raises(Exception):
            self.authService.register("Jack", "password")

        assert self.userBase.includes("Jack")
        assert self.db.userRepository().includes("Jack")
        assert self.sessionRegistry.isEmpty()
        assert self.db.sessionRepository().isEmpty()

    def test05_IfAUserCanNotLogInNoSessionIsStored(self):
        with pytest.raises(Exception):
            self.authService.login("Jack", "password")

        assert self.sessionRegistry.isEmpty()
        assert self.db.sessionRepository().isEmpty()

    def test06_UserCanLogInIfAUserRegisteredBefore(self):
        self.authService.register("Jack", "password")

        session = self.authService.login("Jack", "password")

        assert session.user().name() == "Jack"
        assert self.db.sessionRepository().includes(session.id())

    def test07_IfASessionCanNotBeSavedInTheDatabaseThenItIsNotSavedInTheRegistry(self):
        self.authService.register("Jack", "password")
        self.db.sessionRepository().failOnNextQuery()

        with pytest.raises(Exception):
            self.authService.login("Jack", "password")

        assert self.sessionRegistry.size() == 1
        assert self.db.sessionRepository().size() == 1

    def test08_UserCanLogInIfAUserWasRegisteredOnTheDatabaseBeforeTheCreationOfTheService(self):
        self.db.userRepository().insert(User("Jack", self.hashStrategy.hash("password")))
        self.authService = AuthService(self.db, self.userBase, self.sessionRegistry)

        session = self.authService.login("Jack", "password")

        assert session.user().name() == "Jack"
        assert self.db.sessionRepository().includes(session.id())
