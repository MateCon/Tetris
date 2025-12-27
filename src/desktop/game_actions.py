from abc import ABC, abstractmethod


class GameActions(ABC):
    @abstractmethod
    def tick(self):
        pass

    @abstractmethod
    def startMovingLeft(self):
        pass

    @abstractmethod
    def stopMovingLeft(self):
        pass

    @abstractmethod
    def startMovingRight(self):
        pass

    @abstractmethod
    def stopMovingRight(self):
        pass

    @abstractmethod
    def startDropping(self):
        pass

    @abstractmethod
    def stopDropping(self):
        pass

    @abstractmethod
    def hardDrop(self):
        pass

    @abstractmethod
    def rotateLeft(self):
        pass

    @abstractmethod
    def rotateRight(self):
        pass

    @abstractmethod
    def hold(self):
        pass


class RunningGameActions(GameActions):
    def __init__(self, aGameComponent, aGame):
        self.gameComponent = aGameComponent
        self.game = aGame

    def tick(self):
        self.game.tick()

    def startMovingLeft(self):
        self.gameComponent.leftCommandRepeater.start()

    def stopMovingLeft(self):
        self.gameComponent.leftCommandRepeater.stop()

    def startMovingRight(self):
        self.gameComponent.rightCommandRepeater.start()

    def stopMovingRight(self):
        self.gameComponent.rightCommandRepeater.stop()

    def startDropping(self):
        self.gameComponent.dropCommandRepeater.start()

    def stopDropping(self):
        self.gameComponent.dropCommandRepeater.stop()

    def hardDrop(self):
        self.game.hardDrop()

    def rotateLeft(self):
        self.game.rotateLeft()

    def rotateRight(self):
        self.game.rotateRight()

    def hold(self):
        self.game.hold()

    def togglePause(self):
        return PausedGameActions(self.gameComponent, self.game)

    def isPaused(self):
        return False


class PausedGameActions(GameActions):
    def __init__(self, aGameComponent, aGame):
        self.gameComponent = aGameComponent
        self.game = aGame

    def tick(self):
        pass

    def startMovingLeft(self):
        pass

    def stopMovingLeft(self):
        pass

    def startMovingRight(self):
        pass

    def stopMovingRight(self):
        pass

    def startDropping(self):
        pass

    def stopDropping(self):
        pass

    def hardDrop(self):
        pass

    def rotateLeft(self):
        pass

    def rotateRight(self):
        pass

    def hold(self):
        pass

    def togglePause(self):
        return RunningGameActions(self.gameComponent, self.game)

    def isPaused(self):
        return True
