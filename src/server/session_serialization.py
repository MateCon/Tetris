from datetime import datetime, timedelta
from server_model.user import User
from server_model.session import Session


class SessionSerializer:
    def __init__(self, aSession):
        self.session = aSession

    def serialize(self):
        return {
            "id": self.session.id(),
            "user_name": self.session.user().name(),
            "creation_date": self.session.expirationDate().isoformat(),
            "duration": self.session.duration().total_seconds()
        }


class SessionDeserializer:
    def __init__(self, aSessionDictionary):
        self.sessionDictionary = aSessionDictionary

    def deserialize(self):
        return Session(
            self.sessionDictionary.get("id"),
            User(self.sessionDictionary.get("user_name")),
            datetime.fromisoformat(self.sessionDictionary.get("creation_date")),
            timedelta(seconds=int(self.sessionDictionary.get("duration")))
        )
