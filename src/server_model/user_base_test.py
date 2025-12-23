import pytest
from server_model.user_base import UserBase, NameTaken, UserNotFound, WrongPassword, PasswordTooLong, PasswordTooShort
from server_model.user import User, NameTooLong, NameTooShort, HashedPasswordTooLong
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
        self.userBase = UserBase(self.sessionRegistry, HashStub())

    def test01_UserBaseStartsEmpty(self):
        assert self.userBase.size() == 0

    def test02_UserBaseCanRegisterAUser(self):
        self.userBase.register("John", "1234")

        assert self.userBase.size() == 1
        assert self.userBase.includes("John")

    def test03_UserBaseCanRegisterMultipleUsers(self):
        self.userBase.register("John", "1234")
        self.userBase.register("Jack", "password")

        assert self.userBase.size() == 2
        assert self.userBase.includes("John")
        assert self.userBase.includes("Jack")

    def test04_UsersNotRegisteredAreNotInTheUserBase(self):
        assert not self.userBase.includes("John")

    def test05_AUserCanNotBeRegisteredUnderATakenName(self):
        self.userBase.register("John", "1234")

        with pytest.raises(NameTaken):
            self.userBase.register("John", "1234")

    def test06_AUserNameCanNotBeMoreThanTwentyCharactersLong(self):
        with pytest.raises(NameTooLong):
            self.userBase.register("Twenty One Characters", "1234")

    def test07_CanNotRegisterANameLessThanThreeCharactersLong(self):
        with pytest.raises(NameTooShort):
            self.userBase.register("No", "1234")

    def test08_CanNotRegisterANameMoreThanTwentyCharactersLong(self):
        with pytest.raises(PasswordTooLong):
            self.userBase.register("John", "Twenty One Characters")

    def test09_APasswordCanNotBeLessThanthreeCharactersLong(self):
        with pytest.raises(PasswordTooShort):
            self.userBase.register("John", "No")

    def test10_LoginCreatesASessionThatExpiresInAWeek(self):
        self.userBase.register("John", "1234")

        session = self.userBase.login("John", "1234")

        assert session.user().name() == "John"
        assert session.expirationDate() == self.clock.now() + self.clock.aWeek()

    def test11_LoginFailsIfUserIsNotFound(self):
        with pytest.raises(UserNotFound):
            self.userBase.login("John", "1234")

    def test12_LoginFailsIfPasswordIsWrong(self):
        self.userBase.register("John", "1234")

        with pytest.raises(WrongPassword):
            self.userBase.login("John", "1235")

    def test13_SessionIdsAreUnique(self):
        self.userBase.register("John", "1234")

        firstSession = self.userBase.login("John", "1234")
        secondSession = self.userBase.login("John", "1234")

        assert firstSession.id() != secondSession.id()

    def test14_SessionVerificationFailsIfTheSessionDoesNotExist(self):
        self.userBase.register("John", "1234")

        unusedId = self.idGenerator.nextId()
        self.userBase.login("John", "1234")

        with pytest.raises(SessionNotFound):
            self.sessionRegistry.verify(unusedId)

    def test15_SessionVerificationFailsIfTheSessionJustExpired(self):
        self.userBase.register("John", "1234")

        session = self.userBase.login("John", "1234")

        self.clock.jumpForward(self.clock.aWeek())

        with pytest.raises(SessionExpired):
            self.sessionRegistry.verify(session.id())

    def test16_SessionCanBeVerifiedWithOneSessionInTheRegistry(self):
        self.userBase.register("John", "1234")

        session = self.userBase.login("John", "1234")

        self.sessionRegistry.verify(session.id())

    def test17_SessionCanBeVerifiedWithMultipleSessionsInTheRegistry(self):
        self.userBase.register("John", "1234")
        self.userBase.register("Jack", "password")

        session = self.userBase.login("John", "1234")
        self.userBase.login("Jack", "password")

        self.sessionRegistry.verify(session.id())

    def test18_UserPasswordIsHashed(self):
        session = self.userBase.register("John", "1234")

        assert session.user().hashedPassword() != "1234"

    def test19_UserBaseCanLoadAnExistingUser(self):
        user = User("John", "some hashed password")
        self.userBase.load(user)

        assert self.userBase.size() == 1
        assert self.userBase.includes("John")
        assert user.hashedPassword() == "some hashed password"

    def test20_UserNameCanNotBeMoreThanTwentyCharactersLong(self):
        with pytest.raises(NameTooLong):
            User("Twenty One Characters", "some hashed password")

    def test21_UserNameCanNotBeLessThanThreeCharactersLong(self):
        with pytest.raises(NameTooShort):
            User("No", "some hashed password")

    def test22_HashedPasswordCanNotBeMoreThanOneHoundredLong(self):
        with pytest.raises(HashedPasswordTooLong):
            User("John", "this is a manually written string whose length is one character longer than one houndred, ending now.")
