from desktop.desktop_component import DesktopComponent
from desktop.area import Area
from desktop.held_command_repeater import HeldCommandRepeater
from desktop.next_piece_display_component import NextPieceDisplayComponent
from desktop.held_piece_display_component import HeldPieceDisplayComponent
from desktop.game_actions import RunningGameActions
from desktop.pause_component import PauseComponent
from tetris_model.game_score import GameScore
from tetris_model.time import Time


class GameComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aGame, anAmmountOfRows, anAmmountOfCols, cellSize, aTetrisEventNotifier, aKeybindMapper, aColorScheme, aRestartMethod, aDeleteMethod, aSession):
        super().__init__(anApplicationContext)
        self.rows = anAmmountOfRows
        self.cols = anAmmountOfCols
        self.game = aGame
        self.cellSize = cellSize
        self.borderWidth = 2
        self.colorScheme = aColorScheme
        self.session = aSession
        self.timeSinceLastTick = 0
        self.inputObserver = self.applicationContext.inputObserver
        self.tetrisEventNotifier = aTetrisEventNotifier
        self.nextPieceDisplayComponent = NextPieceDisplayComponent(self.applicationContext, self, self.nextSixPieces(), self.cellSize, self.colorScheme)
        self.heldPieceDisplayComponent = HeldPieceDisplayComponent(self.applicationContext, self, self.getHeldPiece(), self.cellSize, self.colorScheme)

        self.leftCommandRepeater = HeldCommandRepeater(self.game.moveLeft, 167, 33)
        self.rightCommandRepeater = HeldCommandRepeater(self.game.moveRight, 167, 33)
        self.dropCommandRepeater = HeldCommandRepeater(self.game.softDrop, 50, 33)

        self.gameActions = RunningGameActions(self, self.game)
        self.tetrisEventNotifier.attachPlacedPieceEvent(self.gameActions.stopDropping)
        aKeybindMapper(self)

        self.scoreTracker = GameScore(self.tetrisEventNotifier)

        self.pauseComponent = PauseComponent(self.applicationContext, self, self.cellSize, aRestartMethod, aDeleteMethod)

        self.tetrisEventNotifier.attachLostEvent(self.pauseComponent.focusRestart)
        self.tetrisEventNotifier.attachLostEvent(self.togglePause)

        self.time = Time.fromMilliseconds(0)

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

    def hold(self):
        self.gameActions.hold()

    def getHeldPiece(self):
        return self.game.getHeldPiece()

    def togglePause(self):
        self.leftCommandRepeater.stop()
        self.rightCommandRepeater.stop()
        self.dropCommandRepeater.stop()
        self.gameActions = self.gameActions.togglePause()

    def isPaused(self):
        return self.gameActions.isPaused()

    def pauseMoveDown(self):
        self.pauseComponent.moveDown()

    def pauseMoveUp(self):
        self.pauseComponent.moveUp()

    def pauseAccept(self):
        if self.isPaused():
            self.pauseComponent.accept()

    def drawArea(self, aColor, anArea):
        self.applicationContext.drawArea(aColor, Area(
            anArea.x + self.borderWidth,
            anArea.y + self.borderWidth, anArea.width,
            anArea.height
        ))

    def activeCharacter(self):
        return self.game.activeCharacter()

    def cellColor(self, aCell):
        return self.colorScheme.cellColor(aCell, self.isPaused(), self.activeCharacter().lower())

    def drawBoard(self, anArea):
        board = self.game.asStringListWithGhostPiece()
        for y in range(self.rows + 2):
            for x in range(self.cols):
                self.applicationContext.drawArea(
                    self.cellColor(board[y][x].lower()),
                    Area(anArea.x + self.cellSize * x, anArea.y + self.cellSize * y, self.cellSize, self.cellSize)
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
        areaWithoutVanishZone = self.areaWithoutVanishZone(anArea)
        self.applicationContext.drawText(
            self.session.user().name(),
            (255, 255, 255), 22,
            areaWithoutVanishZone.shifted(0, areaWithoutVanishZone.height + 10)
        )

        leftOfAreaWithoutVanishZone = areaWithoutVanishZone.shifted(-self.cellSize * 7, 0)
        self.applicationContext.drawText(
            f"Level {self.scoreTracker.level()}",
            (255, 255, 255), 22,
            leftOfAreaWithoutVanishZone.shifted(0, self.cellSize * 3)
        )
        self.applicationContext.drawText(
            f"Lines cleared: {self.scoreTracker.lines()}",
            (255, 255, 255), 22,
            leftOfAreaWithoutVanishZone.shifted(0, self.cellSize * 3 + 40)
        )
        self.applicationContext.drawText(
            f"Score: {self.scoreTracker.score()}",
            (255, 255, 255), 22,
            leftOfAreaWithoutVanishZone.shifted(0, self.cellSize * 3 + 80)
        )
        self.applicationContext.drawText(
            f"Time: {self.time.asString()}",
            (255, 255, 255), 22,
            leftOfAreaWithoutVanishZone.shifted(0, self.cellSize * 3 + 120)
        )

        self.drawBoard(self.centeredArea(anArea))
        self.drawBorderAround(self.areaWithoutVanishZone(anArea))
        self.nextPieceDisplayComponent.draw(
            self.centeredArea(anArea)
                .shifted(self.cellSize + self.area().width, 0)
        )
        self.heldPieceDisplayComponent.draw(
            self.centeredArea(anArea)
                .shifted(-self.cellSize * 8, 0)
        )

        if self.isPaused():
            self.pauseComponent.draw(self.areaWithoutVanishZone(anArea))

    def nextSixPieces(self):
        return self.game.getNextSix()

    def timeToSoftDrop(self):
        gavityTable = [ 0.01667, 0.021017, 0.026977, 0.035256, 0.04693,
                        0.06361, 0.0879, 0.1236, 0.1775, 0.2598,
                        0.388, 0.59, 0.92, 1.46, 2.36,
                        3.91 , 6.61, 11.43, 20.3 ]
        level = self.scoreTracker.level()
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
        self.heldPieceDisplayComponent.update(millisecondsSinceLastUpdate, self.getHeldPiece())

        if not self.isPaused() and not self.pauseComponent.lost():
            self.time = self.time + Time.fromMilliseconds(millisecondsSinceLastUpdate)
