import pygame
from desktop.desktop_component import DesktopComponent
from desktop.area import Area


class TetrisGameComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aGame, anAmmountOfRows, anAmmountOfCols, cellSize):
        super().__init__(anApplicationContext)
        self.rows = anAmmountOfRows
        self.cols = anAmmountOfCols
        self.game = aGame
        self.cellSize = cellSize
        self.borderWidth = 2
        self.timeSinceLastTick = 0
        self.inputObserver = self.applicationContext.inputObserver
        self.inputObserver.addKeyupObserver(pygame.K_LEFT, self.game.moveLeft)
        self.inputObserver.addKeyupObserver(pygame.K_RIGHT, self.game.moveRight)
        self.inputObserver.addKeyupObserver(pygame.K_w, self.game.hardDrop)
        self.inputObserver.addKeyupObserver(pygame.K_s, self.game.softDrop)
        self.inputObserver.addKeyupObserver(pygame.K_a, self.game.rotateLeft)
        self.inputObserver.addKeyupObserver(pygame.K_d, self.game.rotateRight)

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
        self.drawBoard(self.centeredArea(anArea))
        self.drawBorderAround(self.areaWithoutVanishZone(anArea))

    def nextPiece(self):
        return self.game.getNextPiece()

    def update(self, millisecondsSinceLastUpdate):
        self.timeSinceLastTick += millisecondsSinceLastUpdate
        if self.timeSinceLastTick > 250:
            self.game.softDrop()
            self.timeSinceLastTick = 0
