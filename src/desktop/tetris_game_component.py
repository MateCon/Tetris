import pygame
from desktop.desktop_component import DesktopComponent
from desktop.area import Area
from desktop.held_command_repeater import HeldCommandRepeater
from model.point import Point


class TetrisGameComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aGame, anAmmountOfRows, anAmmountOfCols, cellSize, aTetrisEventNotifier):
        super().__init__(anApplicationContext)
        self.rows = anAmmountOfRows
        self.cols = anAmmountOfCols
        self.game = aGame
        self.cellSize = cellSize
        self.borderWidth = 2
        self.timeSinceLastTick = 0
        self.inputObserver = self.applicationContext.inputObserver
        self.tetrisEventNotifier = aTetrisEventNotifier

        self.leftCommandRepeater = HeldCommandRepeater(self.game.moveLeft, 167, 33)
        self.inputObserver.addKeydownObserver(self, pygame.K_LEFT, self.leftCommandRepeater.start)
        self.inputObserver.addKeyupObserver(self, pygame.K_LEFT, self.leftCommandRepeater.stop)

        self.rightCommandRepeater = HeldCommandRepeater(self.game.moveRight, 167, 33)
        self.inputObserver.addKeydownObserver(self, pygame.K_RIGHT, self.rightCommandRepeater.start)
        self.inputObserver.addKeyupObserver(self, pygame.K_RIGHT, self.rightCommandRepeater.stop)

        self.dropCommandRepeater = HeldCommandRepeater(self.game.softDrop, 50, 33)
        self.inputObserver.addKeydownObserver(self, pygame.K_s, self.dropCommandRepeater.start)
        self.inputObserver.addKeyupObserver(self, pygame.K_s, self.dropCommandRepeater.stop)
        self.tetrisEventNotifier.attachPlacedPieceEvent(self.dropCommandRepeater.stop)

        self.inputObserver.addKeydownObserver(self, pygame.K_w, self.game.hardDrop)
        self.inputObserver.addKeydownObserver(self, pygame.K_a, self.game.rotateLeft)
        self.inputObserver.addKeydownObserver(self, pygame.K_d, self.game.rotateRight)

        self.linesCleared = 0
        self.tetrisEventNotifier.attachRowClearEvent(self.onRowClear)
        self.tetrisEventNotifier.attachDoubleRowClearEvent(self.onDoubleRowClear)
        self.tetrisEventNotifier.attachTripleRowClearEvent(self.onTripleRowClear)
        self.tetrisEventNotifier.attachQuadrupleRowClearEvent(self.onQuadrupleRowClear)

    def onRowClear(self):
        self.linesCleared += 1

    def onDoubleRowClear(self):
        self.linesCleared += 2

    def onTripleRowClear(self):
        self.linesCleared += 3

    def onQuadrupleRowClear(self):
        self.linesCleared += 4

    def drawRect(self, aColor, aRectangle):
        self.applicationContext.drawRect(aColor, pygame.Rect(
            aRectangle.x + self.borderWidth,
            aRectangle.y + self.borderWidth, aRectangle.width,
            aRectangle.height
        ))

    def cellColor(self, aCell):
        colors = {
            'i': (255, 0, 0),
            'j': (0, 0, 255),
            'l': (255, 172, 0),
            'o': (255, 255, 0),
            's': (0, 255, 255),
            't': (255, 0, 255),
            'z': (0, 255, 0),
        }
        if aCell in colors.keys():
            return colors[aCell]
        return (0, 0, 0)

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
            f"Level {1 + self.linesCleared // 10}",
            (255, 255, 255),
            self.areaWithoutVanishZone(anArea).shifted(-self.cellSize * 8, 0).asRect()
        )
        self.applicationContext.drawBigText(
            f"Lines cleared: {self.linesCleared}",
            (255, 255, 255),
            self.areaWithoutVanishZone(anArea).shifted(-self.cellSize * 8, 40).asRect()
        )
        self.drawBoard(self.centeredArea(anArea))
        self.drawBorderAround(self.areaWithoutVanishZone(anArea))

    def nextSixPieces(self):
        return self.game.getNextSix()

    def timeToSoftDrop(self):
        gavityTable = [ 0.01667, 0.021017, 0.026977, 0.035256, 0.04693,
                        0.06361, 0.0879, 0.1236, 0.1775, 0.2598,
                        0.388, 0.59, 0.92, 1.46, 2.36,
                        3.91 , 6.61, 11.43, 20.3 ]
        level = 1 + self.linesCleared // 10
        gravity = gavityTable[min(level, len(gavityTable) - 1)]
        return 1000/(60*gravity)

    def update(self, millisecondsSinceLastUpdate):
        self.timeSinceLastTick += millisecondsSinceLastUpdate
        timeToSoftDrop = self.timeToSoftDrop()
        if self.timeSinceLastTick > timeToSoftDrop:
            self.game.softDrop()
            self.timeSinceLastTick -= timeToSoftDrop

        self.rightCommandRepeater.update(millisecondsSinceLastUpdate)
        self.leftCommandRepeater.update(millisecondsSinceLastUpdate)
        self.dropCommandRepeater.update(millisecondsSinceLastUpdate)

    def destroy(self):
        self.inputObserver.removeFrom(self)
