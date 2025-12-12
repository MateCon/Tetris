from desktop.desktop_component import DesktopComponent
from desktop.tetris_game_component import TetrisGameComponent
from model.tetris_game import TetrisGame
from model.rotation_list_generator import SegaRotationListGenerator
from model.kicks import ARSKicks
from model.rand import Rand
import pygame


class NextPieceDisplayComponent(DesktopComponent):
    def __init__(self, anApplicationContext, theNextPiece, cellSize):
        super().__init__(anApplicationContext)
        self.nextPiece = theNextPiece
        self.cellSize = cellSize

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

    def draw(self, anArea):
        board = self.nextPiece.asStringList()
        for y in range(4):
            for x in range(4):
                self.applicationContext.drawRect(
                    self.cellColor(board[y][x].lower()),
                    pygame.Rect(anArea.x + self.cellSize * x, anArea.y + self.cellSize * y, self.cellSize, self.cellSize)
                )

    def update(self, millisecondsSinceLastUpdate, theNextPiece):
        self.nextPiece = theNextPiece


class PlayPageComponent(DesktopComponent):
    def __init__(self, anApplicationContext):
        super().__init__(anApplicationContext)
        self.rows = 20
        self.cols = 10
        self.cellSize = 30
        self.game = TetrisGame(
            self.cols,
            self.rows,
            Rand(),
            SegaRotationListGenerator,
            ARSKicks
        )
        self.gameComponent = TetrisGameComponent(anApplicationContext, self.game, self.rows, self.cols, self.cellSize)
        self.nextPieceDisplayComponent = NextPieceDisplayComponent(anApplicationContext, self.gameComponent.nextPiece(), self.cellSize)

    def draw(self, anArea):
        self.applicationContext.drawRect(pygame.Color(0,0,0), anArea.asRect())
        self.gameComponent.draw(anArea)
        self.nextPieceDisplayComponent.draw(self.gameComponent.areaWithoutVanishZone(anArea).shifted(-self.cellSize * 5, 0))

    def update(self, millisecondsSinceLastUpdate):
        self.gameComponent.update(millisecondsSinceLastUpdate)
        self.nextPieceDisplayComponent.update(millisecondsSinceLastUpdate, self.gameComponent.nextPiece())
