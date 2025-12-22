import pytest
from server_model.user_base import UserBase, NameTaken, UserNotFound, WrongPassword
from server_model.user import User, NameTooLong, NameTooShort, PasswordTooLong, PasswordTooShort
from server_model.session_registry import SessionRegistry, SessionNotFound, SessionExpired
from server_model.clock import ClockStub
from server_model.id_generator import AutoincrementalIdGenerator
from server_model.hash import HashStub


class TestUserBase:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.clock = ClockStub(2025, 12, 22)
        self.idGenerator = AutoincrementalIdGenerator()
        self.sessionRegistry = SessionRegistry(self.clock, self.idGenerator)
        self.userBase = UserBase(self.sessionRegistry)
        self.hashStub = HashStub()
        self.john = User("John", "1234", self.hashStub)
        self.jack = User("Jack", "abcd", self.hashStub)
        self.someName = "Charlie"
        self.somePassword = "password"

    def test01_UserBaseStartsEmpty(self):
        assert self.userBase.size() == 0

    def test02_UserBaseCanRegisterAUser(self):
        self.userBase.register(self.john)

        assert self.userBase.size() == 1
        assert self.userBase.includes(self.john)

    def test03_UserBaseCanRegisterMultipleUsers(self):
        self.userBase.register(self.john)
        self.userBase.register(self.jack)

        assert self.userBase.size() == 2
        assert self.userBase.includes(self.john)
        assert self.userBase.includes(self.jack)

    def test04_UsersNotRegisteredAreNotInTheUserBase(self):
        assert not self.userBase.includes(self.john)

    def test05_AUserCanNotBeRegisteredUnderATakenName(self):
        firstJohn = User("John", self.somePassword, self.hashStub)
        secondJohn = User("John", self.somePassword, self.hashStub)

        self.userBase.register(firstJohn)

        with pytest.raises(NameTaken):
            self.userBase.register(secondJohn)

    def test06_AUserNameCanNotBeMoreThanTwentyCharactersLong(self):
        with pytest.raises(NameTooLong):
            User("Twenty One Characters", self.somePassword, self.hashStub)

    def test07_AUserNameCanNotBeLessThanThreeCharactersLong(self):
        with pytest.raises(NameTooShort):
            User("No", self.somePassword, self.hashStub)

    def test08_APasswordCanNotBeMoreThanTwentyCharactersLong(self):
        with pytest.raises(PasswordTooLong):
            User(self.someName, "Twenty One Characters", self.hashStub)

    def test09_APasswordCanNotBeLessThanthreeCharactersLong(self):
        with pytest.raises(PasswordTooShort):
            User(self.someName, "No", self.hashStub)

    def test10_LoginCreatesASessionThatExpiresInAWeek(self):
        self.userBase.register(self.john)

        session = self.userBase.login("John", "1234")

        assert session.user() is self.john
        assert session.expirationDate() == self.clock.now() + self.clock.aWeek()

    def test11_LoginFailsIfUserIsNotFound(self):
        with pytest.raises(UserNotFound):
            self.userBase.login("John", "1234")

    def test12_LoginFailsIfPasswordIsWrong(self):
        self.userBase.register(self.john)

        with pytest.raises(WrongPassword):
            self.userBase.login("John", "1235")

    def test13_SessionIdsAreUnique(self):
        self.userBase.register(self.john)

        firstSession = self.userBase.login("John", "1234")
        secondSession = self.userBase.login("John", "1234")

        assert firstSession.id() != secondSession.id()

    def test14_SessionVerificationFailsIfTheSessionDoesNotExist(self):
        self.userBase.register(self.john)

        unusedId = self.idGenerator.nextId()
        self.userBase.login("John", "1234")

        with pytest.raises(SessionNotFound):
            self.sessionRegistry.verify(unusedId)

    def test15_SessionVerificationFailsIfTheSessionIsExpired(self):
        self.userBase.register(self.john)

        session = self.userBase.login("John", "1234")

        self.clock.jumpForward(self.clock.aWeek())

        with pytest.raises(SessionExpired):
            self.sessionRegistry.verify(session.id())

    def test16_SessionCanBeVerifiedWithOneSessionInTheRegistry(self):
        self.userBase.register(self.john)

        session = self.userBase.login("John", "1234")

        self.sessionRegistry.verify(session.id())

    def test17_SessionCanBeVerifiedWithMultipleSessionsInTheRegistry(self):
        self.userBase.register(self.john)
        self.userBase.register(self.jack)

        session = self.userBase.login("John", "1234")
        self.userBase.login("Jack", "abcd")

        self.sessionRegistry.verify(session.id())

    def test18_UserPasswordIsHashed(self):
        user = User(self.someName, self.somePassword, self.hashStub)

        assert user._password != self.somePassword
