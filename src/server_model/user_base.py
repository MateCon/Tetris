class UserBase:
    def __init__(self, aSessionRegistry):
        self._users = []
        self._sessionRegistry = aSessionRegistry

    def register(self, aUser):
        self.verifyNameAvailable(aUser)
        self._users.append(aUser)

    def verifyNameAvailable(self, aUser):
        for user in self._users:
            if user.name() == aUser.name():
                raise NameTaken

    def login(self, aName, aPassword):
        for user in self._users:
            if user.name() == aName:
                if user.hasPassword(aPassword):
                    return self._sessionRegistry.createSessionFor(user)
                else:
                    raise WrongPassword
        raise UserNotFound

    def includes(self, aUser):
        for user in self._users:
            if user is aUser:
                return True
        return False

    def size(self):
        return len(self._users)


class NameTaken(Exception):
    pass


class UserNotFound(Exception):
    pass


class WrongPassword(Exception):
    pass
