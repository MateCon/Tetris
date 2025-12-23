from server_model.user import User


class UserBase:
    def __init__(self, aSessionRegistry, aHashStrategy):
        self._users = []
        self._sessionRegistry = aSessionRegistry
        self._hashStrategy = aHashStrategy

    def register(self, aName, aPassword):
        self.assertPasswordIsNotTooLong(aPassword)
        self.assertPasswordIsNotTooShort(aPassword)
        self.verifyNameAvailable(aName)
        user = User(aName, self._hashStrategy.hash(aPassword))
        self._users.append(user)
        return self._sessionRegistry.createSessionFor(user)

    def load(self, aUser):
        self._users.append(aUser)

    def verifyNameAvailable(self, aName):
        for user in self._users:
            if user.name() == aName:
                raise NameTaken

    def assertPasswordIsNotTooLong(self, aPassword):
        if len(aPassword) > 20:
            raise PasswordTooLong

    def assertPasswordIsNotTooShort(self, aPassword):
        if len(aPassword) < 3:
            raise PasswordTooShort

    def login(self, aName, aPassword):
        for user in self._users:
            if user.name() == aName:
                if user.hasPassword(aPassword, self._hashStrategy):
                    return self._sessionRegistry.createSessionFor(user)
                else:
                    raise WrongPassword
        raise UserNotFound

    def includes(self, aName):
        for user in self._users:
            if user.name() == aName:
                return True
        return False

    def remove(self, aName):
        for user in self._users:
            if user.name() == aName:
                return self._users.remove(user)

    def size(self):
        return len(self._users)

    def isEmpty(self):
        return len(self._users) == 0


class NameTaken(Exception):
    pass


class UserNotFound(Exception):
    pass


class WrongPassword(Exception):
    pass


class PasswordTooLong(Exception):
    pass


class PasswordTooShort(Exception):
    pass
