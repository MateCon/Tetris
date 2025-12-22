class User:
    def __init__(self, aName, aPassword, aHashStrategy):
        self.assertNameIsNotTooLong(aName)
        self.assertNameIsNotTooShort(aName)
        self.assertPasswordIsNotTooLong(aPassword)
        self.assertPasswordIsNotTooShort(aPassword)
        self.hashStrategy = aHashStrategy
        self._name = aName
        self._password = self.hashStrategy.hash(aPassword)

    def name(self):
        return self._name

    def hasPassword(self, anotherPassword):
        return self.hashStrategy.verify(self._password, anotherPassword)

    def assertNameIsNotTooLong(self, aName):
        if len(aName) > 20:
            raise NameTooLong

    def assertNameIsNotTooShort(self, aName):
        if len(aName) < 3:
            raise NameTooShort

    def assertPasswordIsNotTooLong(self, aPassword):
        if len(aPassword) > 20:
            raise PasswordTooLong

    def assertPasswordIsNotTooShort(self, aPassword):
        if len(aPassword) < 3:
            raise PasswordTooShort


class NameTooLong(Exception):
    pass


class NameTooShort(Exception):
    pass


class PasswordTooLong(Exception):
    pass


class PasswordTooShort(Exception):
    pass
