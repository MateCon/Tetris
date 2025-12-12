import pygame
from desktop.desktop_component import DesktopComponent
from desktop.area import Area
from model.tetris_game import TetrisGame
from model.rotation_list_generator import SegaRotationListGenerator
from model.kicks import ARSKicks
from model.rand import Rand


class TetrisGameComponent(DesktopComponent):
    def __init__(self, anApplicationContext):
        super().__init__(anApplicationContext)
        self.rows = 20
        self.cols = 10
        self.borderWidth = 2
        self.game = TetrisGame(
            self.cols,
            self.rows,
            Rand(),
            SegaRotationListGenerator,
            ARSKicks
        )
        self.timeSinceLastTick = 0
        self.cellSize = 30
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

    def draw(self, anArea):
        boardArea = Area(0, 0, self.cellSize * self.cols, self.cellSize * (self.rows + 2))
        centeredBoardArea = boardArea.centeredAt(anArea)
        self.drawBoard(centeredBoardArea)
        centeredBoardAreaWithoutVanishZone = Area(
            centeredBoardArea.x,
            centeredBoardArea.y + self.cellSize * 2,
            centeredBoardArea.width,
            centeredBoardArea.height - self.cellSize * 2
        )
        self.drawBorderAround(centeredBoardAreaWithoutVanishZone)

    def update(self, millisecondsSinceLastUpdate):
        self.timeSinceLastTick += millisecondsSinceLastUpdate
        if self.timeSinceLastTick > 250:
            self.game.softDrop()
            self.timeSinceLastTick = 0
