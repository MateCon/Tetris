class GameResult:
    def __init__(self, aUser, aScore, aLevel, anAmmountOfLines, currentDate, aTimeInMilliseconds):
        self.user = aUser
        self.score = aScore
        self.level = aLevel
        self.lines = anAmmountOfLines
        self.creationDate = currentDate
        self.time = aTimeInMilliseconds

    def __eq__(self, anotherGameResult):
        return self.user.name() == anotherGameResult.user.name() and self.score == anotherGameResult.score and self.level == anotherGameResult.level and self.lines == anotherGameResult.lines and self.creationDate == anotherGameResult.creationDate and self.time == anotherGameResult.time

    def __lt__(self, anotherGameResult):
        return self.score < anotherGameResult.score or (self.score == anotherGameResult.score and self.creationDate < anotherGameResult.creationDate)

    def __le__(self, anotherGameResult):
        return self < anotherGameResult or (self.score == anotherGameResult.score and self.creationDate == anotherGameResult.creationDate)
