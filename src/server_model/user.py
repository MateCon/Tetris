class User:
    def __init__(self, aName, aHashedPassword):
        self.assertNameIsNotTooLong(aName)
        self.assertNameIsNotTooShort(aName)
        self.assertHashedPasswordIsNotTooLong(aHashedPassword)
        self._name = aName
        self._hashedPassword = aHashedPassword

    def name(self):
        return self._name

    def hasPassword(self, anotherPassword, aHashStrategy):
        return aHashStrategy.verify(self._hashedPassword, anotherPassword)

    def hashedPassword(self):
        return self._hashedPassword

    def assertNameIsNotTooLong(self, aName):
        if len(aName) > 20:
            raise NameTooLong

    def assertNameIsNotTooShort(self, aName):
        if len(aName) < 3:
            raise NameTooShort

    def assertHashedPasswordIsNotTooLong(self, aPassword):
        if len(aPassword) > 100:
            raise HashedPasswordTooLong


class NameTooLong(Exception):
    pass


class NameTooShort(Exception):
    pass


class HashedPasswordTooLong(Exception):
    pass
