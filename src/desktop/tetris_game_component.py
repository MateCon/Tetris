import pygame
from desktop.desktop_component import DesktopComponent
from desktop.area import Area
from desktop.held_command_repeater import HeldCommandRepeater
from desktop.next_piece_display_component import NextPieceDisplayComponent
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


class RunningGameActions(GameActions):
    def __init__(self, aGame, aLeftCommandRepeater, aRightCommandRepeater, aDropCommandRepeater):
        self.game = aGame
        self.leftCommandRepeater = aLeftCommandRepeater
        self.rightCommandRepeater = aRightCommandRepeater
        self.dropCommandRepeater = aDropCommandRepeater

    def tick(self):
        self.game.tick()

    def startMovingLeft(self):
        self.leftCommandRepeater.start()

    def stopMovingLeft(self):
        self.leftCommandRepeater.stop()

    def startMovingRight(self):
        self.rightCommandRepeater.start()

    def stopMovingRight(self):
        self.rightCommandRepeater.stop()

    def startDropping(self):
        self.dropCommandRepeater.start()

    def stopDropping(self):
        self.dropCommandRepeater.stop()

    def hardDrop(self):
        self.game.hardDrop()

    def rotateLeft(self):
        self.game.rotateLeft()

    def rotateRight(self):
        self.game.rotateRight()

    def togglePause(self):
        return PausedGameActions(self.game, self.leftCommandRepeater, self.rightCommandRepeater, self.dropCommandRepeater)

    def isPaused(self):
        return False


class PausedGameActions(GameActions):
    def __init__(self, aGame, aLeftCommandRepeater, aRightCommandRepeater, aDropCommandRepeater):
        self.game = aGame
        self.leftCommandRepeater = aLeftCommandRepeater
        self.rightCommandRepeater = aRightCommandRepeater
        self.dropCommandRepeater = aDropCommandRepeater

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

    def togglePause(self):
        return RunningGameActions(self.game, self.leftCommandRepeater, self.rightCommandRepeater, self.dropCommandRepeater)

    def isPaused(self):
        return True


class TetrisGameComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aGame, anAmmountOfRows, anAmmountOfCols, cellSize, aTetrisEventNotifier, aKeybindMapper, aColorScheme):
        super().__init__(anApplicationContext)
        self.rows = anAmmountOfRows
        self.cols = anAmmountOfCols
        self.game = aGame
        self.cellSize = cellSize
        self.borderWidth = 2
        self.colorScheme = aColorScheme
        self.timeSinceLastTick = 0
        self.inputObserver = self.applicationContext.inputObserver
        self.tetrisEventNotifier = aTetrisEventNotifier
        self.nextPieceDisplayComponent = NextPieceDisplayComponent(self.applicationContext, self, self.nextSixPieces(), self.cellSize, self.colorScheme)

        self.leftCommandRepeater = HeldCommandRepeater(self.game.moveLeft, 167, 33)
        self.rightCommandRepeater = HeldCommandRepeater(self.game.moveRight, 167, 33)
        self.dropCommandRepeater = HeldCommandRepeater(self.game.softDrop, 50, 33)

        self.gameActions = RunningGameActions(self.game, self.leftCommandRepeater, self.rightCommandRepeater, self.dropCommandRepeater)
        self.tetrisEventNotifier.attachPlacedPieceEvent(self.gameActions.stopDropping)
        aKeybindMapper(self)

        self.linesCleared = 0
        self.score = 0
        self.tetrisEventNotifier.attachRowClearEvent(self.onRowClear)
        self.tetrisEventNotifier.attachDoubleRowClearEvent(self.onDoubleRowClear)
        self.tetrisEventNotifier.attachTripleRowClearEvent(self.onTripleRowClear)
        self.tetrisEventNotifier.attachQuadrupleRowClearEvent(self.onQuadrupleRowClear)

    def tick(self):
        self.gameActions.tick()

    def startMovingLeft(self):
        self.gameActions.startMovingLeft()

    def stopMovingLeft(self):
        self.gameActions.stopMovingLeft()

    def startMovingRight(self):
        self.gameActions.startMovingRight()

    def stopMovingRight(self):
        self.gameActions.stopMovingRight()

    def startDropping(self):
        self.gameActions.startDropping()

    def stopDropping(self):
        self.gameActions.stopDropping()

    def hardDrop(self):
        self.gameActions.hardDrop()

    def rotateLeft(self):
        self.gameActions.rotateLeft()

    def rotateRight(self):
        self.gameActions.rotateRight()

    def togglePause(self):
        self.gameActions = self.gameActions.togglePause()

    def isPaused(self):
        return self.gameActions.isPaused()

    def currentLevel(self):
        return 1 + self.linesCleared // 10

    def onRowClear(self):
        self.linesCleared += 1
        self.score += self.currentLevel() * 100

    def onDoubleRowClear(self):
        self.linesCleared += 2
        self.score += self.currentLevel() * 300

    def onTripleRowClear(self):
        self.linesCleared += 3
        self.score += self.currentLevel() * 500

    def onQuadrupleRowClear(self):
        self.linesCleared += 4
        self.score += self.currentLevel() * 800

    def drawRect(self, aColor, aRectangle):
        self.applicationContext.drawRect(aColor, pygame.Rect(
            aRectangle.x + self.borderWidth,
            aRectangle.y + self.borderWidth, aRectangle.width,
            aRectangle.height
        ))

    def cellColor(self, aCell):
        return self.colorScheme.cellColor(aCell, self.isPaused())

    def drawBoard(self, anArea):
        board = self.game.asStringList()
        for y in range(self.rows + 2):
            for x in range(self.cols):
                self.applicationContext.drawRect(
                    self.cellColor(board[y][x].lower()),
                    pygame.Rect(anArea.x + self.cellSize * x, anArea.y + self.cellSize * y, self.cellSize, self.cellSize)
                )

    def area(self):
        return Area(0, 0, self.cellSize * self.cols, self.cellSize * (self.rows + 2))

    def centeredArea(self, anotherArea):
        return self.area().centeredAt(anotherArea)

    def areaWithoutVanishZone(self, anotherArea):
        centeredBoardArea = self.centeredArea(anotherArea)
        return Area(
            centeredBoardArea.x,
            centeredBoardArea.y + self.cellSize * 2,
            centeredBoardArea.width,
            centeredBoardArea.height - self.cellSize * 2
        )

    def draw(self, anArea):
        self.applicationContext.drawBigText(
            f"Level {self.currentLevel()}",
            (255, 255, 255),
            self.areaWithoutVanishZone(anArea).shifted(-self.cellSize * 7, 0).asRect()
        )
        self.applicationContext.drawBigText(
            f"Lines cleared: {self.linesCleared}",
            (255, 255, 255),
            self.areaWithoutVanishZone(anArea).shifted(-self.cellSize * 7, 40).asRect()
        )
        self.applicationContext.drawBigText(
            f"Score: {self.score}",
            (255, 255, 255),
            self.areaWithoutVanishZone(anArea).shifted(-self.cellSize * 7, 80).asRect()
        )

        self.drawBoard(self.centeredArea(anArea))
        self.drawBorderAround(self.areaWithoutVanishZone(anArea))
        self.nextPieceDisplayComponent.draw(
            self.centeredArea(anArea)
                .shifted(self.cellSize + self.area().width, 0)
        )

    def nextSixPieces(self):
        return self.game.getNextSix()

    def timeToSoftDrop(self):
        gavityTable = [ 0.01667, 0.021017, 0.026977, 0.035256, 0.04693,
                        0.06361, 0.0879, 0.1236, 0.1775, 0.2598,
                        0.388, 0.59, 0.92, 1.46, 2.36,
                        3.91 , 6.61, 11.43, 20.3 ]
        level = self.currentLevel()
        gravity = gavityTable[min(level, len(gavityTable) - 1)]
        return 1000/(60*gravity)

    def update(self, millisecondsSinceLastUpdate):
        self.timeSinceLastTick += millisecondsSinceLastUpdate
        timeToSoftDrop = self.timeToSoftDrop()
        if self.timeSinceLastTick > timeToSoftDrop:
            self.tick()
            self.timeSinceLastTick -= timeToSoftDrop

        self.rightCommandRepeater.update(millisecondsSinceLastUpdate)
        self.leftCommandRepeater.update(millisecondsSinceLastUpdate)
        self.dropCommandRepeater.update(millisecondsSinceLastUpdate)

        self.nextPieceDisplayComponent.update(millisecondsSinceLastUpdate, self.nextSixPieces())

    def destroy(self):
        self.inputObserver.removeFrom(self)

    def mapKeydown(self, aDeviceId, aKey, anAction):
        self.inputObserver.addKeydownObserver(self, aKey, aDeviceId, anAction)

    def mapKeyup(self, aDeviceId, aKey, anAction):
        self.inputObserver.addKeyupObserver(self, aKey, aDeviceId, anAction)
