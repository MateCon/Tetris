class Session:
    def __init__(self, anId, aUser, aCreationDatetime, aDuration):
        self._id = anId
        self._user = aUser
        self._creationDatetime = aCreationDatetime
        self._duration = aDuration

    def id(self):
        return self._id

    def user(self):
        return self._user

    def creationDate(self):
        return self._creationDatetime

    def duration(self):
        return self._duration

    def expirationDate(self):
        return self._creationDatetime + self._duration
