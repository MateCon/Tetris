from datetime import datetime, timedelta
from server_model.leaderboard import Leaderboard
from server_model.user import User
from server_model.session import Session
from server_model.game_result import GameResult


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


class LeaderboardSerializer:
    def __init__(self, aLeaderboard):
        self.leaderboard = aLeaderboard

    def serialize(self):
        serializedLeaderboard = []

        for i in range(min(10, self.leaderboard.size())):
            gameResult = self.leaderboard.at(i)
            serializedLeaderboard.append({
                "user_name": gameResult.user.name(),
                "score": gameResult.score,
                "level": gameResult.level,
                "lines": gameResult.lines,
                "creationDate": gameResult.creationDate.isoformat(),
                "time":  gameResult.time
            })
        return serializedLeaderboard


class LeaderboardDeserializer:
    def __init__(self, aGameResultDictionaryList):
        self.gameResultDictionaryList = aGameResultDictionaryList
        self.leaderboard = Leaderboard()

    def deserialize(self):
        for gameResultDictionary in self.gameResultDictionaryList:
            self.leaderboard.save(GameResult(
                User(gameResultDictionary.get("user_name")),
                gameResultDictionary.get("score"),
                gameResultDictionary.get("level"),
                gameResultDictionary.get("lines"),
                datetime.fromisoformat(gameResultDictionary.get("creationDate")),
                gameResultDictionary.get("time")
            ))
        return self.leaderboard
