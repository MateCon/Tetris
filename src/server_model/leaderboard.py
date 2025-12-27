class Leaderboard:
    def __init__(self):
        self.values = []

    def size(self):
        return len(self.values)

    def at(self, aPosition):
        return self.values[aPosition]

    def save(self, aGameResult):
        if self.hasUser(aGameResult.user):
            previousBest = self.findResultFrom(aGameResult.user)
            if aGameResult > previousBest:
                self.values.remove(previousBest)
            else:
                return

        index = 0
        while index < self.size() and aGameResult <= self.values[index]:
            index += 1
        self.values.insert(index, aGameResult)

    def hasUser(self, aUser):
        for anotherResult in self.values:
            if anotherResult.user.name() == aUser.name():
                return True
        return False

    def findResultFrom(self, aUser):
        for anotherResult in self.values:
            if anotherResult.user.name() == aUser.name():
                return anotherResult
