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
        self.inputObserver.addKeydownObserver(pygame.K_LEFT, self.startMovingLeft)
        self.inputObserver.addKeyupObserver(pygame.K_LEFT, self.stopMovingLeft)

        self.inputObserver.addKeydownObserver(pygame.K_RIGHT, self.startMovingRight)
        self.inputObserver.addKeyupObserver(pygame.K_RIGHT, self.stopMovingRight)

        self.inputObserver.addKeydownObserver(pygame.K_s, self.startDropping)
        self.inputObserver.addKeyupObserver(pygame.K_s, self.stopDropping)

        self.inputObserver.addKeydownObserver(pygame.K_w, self.game.hardDrop)
        self.inputObserver.addKeydownObserver(pygame.K_a, self.game.rotateLeft)
        self.inputObserver.addKeydownObserver(pygame.K_d, self.game.rotateRight)

        self.isMovingRight = False
        self.timeSinceLastRightMove = 0
        self.amountOfConsecutiveRightMovements = 0

        self.isMovingLeft = False
        self.timeSinceLastLeftMove = 0
        self.amountOfConsecutiveLeftMovements = 0

        self.isDropping = False
        self.timeSinceLastDropMove = 0
        self.amountOfConsecutiveDropMovements = 0

    def startMovingRight(self):
        self.game.moveRight()
        self.isMovingRight = True
        self.timeSinceLastRightMove = 0
        self.amountOfConsecutiveRightMovements = 0

    def stopMovingRight(self):
        self.isMovingRight = False

    def startMovingLeft(self):
        self.game.moveLeft()
        self.isMovingLeft = True
        self.timeSinceLastLeftMove = 0
        self.amountOfConsecutiveLeftMovements = 0

    def stopMovingLeft(self):
        self.isMovingLeft = False

    def startDropping(self):
        self.game.softDrop()
        self.isDropping = True
        self.timeSinceLastDropMove = 0
        self.amountOfConsecutiveDropMovements = 0

    def stopDropping(self):
        self.isMovingLeft = False

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

    def nextSixPieces(self):
        return self.game.getNextSix()

    def update(self, millisecondsSinceLastUpdate):
        self.timeSinceLastTick += millisecondsSinceLastUpdate
        if self.timeSinceLastTick > 250:
            self.game.softDrop()
            self.timeSinceLastTick = 0

        self.timeSinceLastRightMove += millisecondsSinceLastUpdate
        if self.isMovingRight and self.timeSinceLastRightMove > 100 - self.amountOfConsecutiveRightMovements * 15:
            self.game.moveRight()
            self.timeSinceLastRightMove = 0
            self.amountOfConsecutiveRightMovements += 1

        self.timeSinceLastLeftMove += millisecondsSinceLastUpdate
        if self.isMovingLeft and self.timeSinceLastLeftMove > 100 - self.amountOfConsecutiveLeftMovements * 15:
            self.game.moveLeft()
            self.timeSinceLastLeftMove = 0
            self.amountOfConsecutiveLeftMovements += 1

        self.timeSinceLastDropMove += millisecondsSinceLastUpdate
        if self.isDropping and self.timeSinceLastDropMove > 100 - self.amountOfConsecutiveDropMovements * 15:
            self.game.softDrop()
            self.timeSinceLastDropMove = 0
            self.amountOfConsecutiveDropMovements += 1
