from desktop.desktop_component import DesktopComponent
from desktop.tetris_game_component import TetrisGameComponent
from desktop.area import Area
from model.tetris_event_notifier import TetrisEventNotifier
from model.tetris_game import TetrisGame
from model.rotation_list_generator import NintendoRotationListGenerator
from model.kicks import ARSKicks
from model.rand import Rand
from model.point import Point
import pygame


class NextPieceDisplayComponent(DesktopComponent):
    def __init__(self, anApplicationContext, theNextSixPieces, cellSize):
        super().__init__(anApplicationContext)
        self.nextSixPieces = theNextSixPieces
        self.cellSize = cellSize
        self.borderColor = (255, 255, 255)
        self.borderWidth = 2

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
        padding = Point(self.cellSize, self.cellSize)
        boardSize = Point(self.cellSize * 4, self.cellSize * 3)
        componentSize = padding + boardSize
        actualArea = Area(anArea.x, anArea.y, componentSize.x, componentSize.y)
        innerArea = actualArea.withPadding(padding.x, padding.y)
        currentArea = innerArea.copy()
        for piece in self.nextSixPieces:
            board = piece.asStringList()
            for y in range(3):
                for x in range(4):
                    self.applicationContext.drawRect(
                        self.cellColor(board[y][x].lower()),
                        pygame.Rect(
                            currentArea.x + self.cellSize * x,
                            currentArea.y + self.cellSize * y,
                            self.cellSize,
                            self.cellSize
                        )
                )
            currentArea = currentArea.shifted(0, boardSize.y)
        self.applicationContext.drawBigText("Next", (255, 255, 255), innerArea.asRect())

    def update(self, millisecondsSinceLastUpdate, theNextSixPieces):
        self.nextSixPieces = theNextSixPieces


class PlayPageComponent(DesktopComponent):
    def __init__(self, anApplicationContext):
        super().__init__(anApplicationContext)
        self.gameComponent = None
        self.initializeGame()
        anApplicationContext.inputObserver.addKeydownObserver(self, pygame.K_DELETE, self.initializeGame)

    def initializeGame(self):
        self.rows = 20
        self.cols = 10
        self.cellSize = 30
        self.tetrisEventNotifier = TetrisEventNotifier()
        self.game = TetrisGame(
            self.cols,
            self.rows,
            Rand(),
            NintendoRotationListGenerator,
            ARSKicks,
            self.tetrisEventNotifier
        )
        if self.gameComponent:
            self.gameComponent.destroy()
        self.gameComponent = TetrisGameComponent(self.applicationContext, self.game, self.rows, self.cols, self.cellSize, self.tetrisEventNotifier)
        self.nextPieceDisplayComponent = NextPieceDisplayComponent(self.applicationContext, self.gameComponent.nextSixPieces(), self.cellSize)

    def draw(self, anArea):
        self.applicationContext.drawRect(pygame.Color(0,0,0), anArea.asRect())
        self.gameComponent.draw(anArea)
        self.nextPieceDisplayComponent.draw(
            self.gameComponent.centeredArea(anArea)
                .shifted(self.cellSize + self.gameComponent.area().width, 0)
        )

    def update(self, millisecondsSinceLastUpdate):
        self.gameComponent.update(millisecondsSinceLastUpdate)
        self.nextPieceDisplayComponent.update(millisecondsSinceLastUpdate, self.gameComponent.nextSixPieces())
