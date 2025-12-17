from model.point import Point
from desktop.area import Area
from desktop.desktop_component import DesktopComponent
import pygame


class NextPieceDisplayComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aGameComponent, theNextSixPieces, cellSize, aColorScheme):
        super().__init__(anApplicationContext)
        self.gameComponent = aGameComponent
        self.nextSixPieces = theNextSixPieces
        self.cellSize = cellSize
        self.borderColor = (255, 255, 255)
        self.borderWidth = 2
        self.colorScheme = aColorScheme

    def cellColor(self, aCell):
        return self.colorScheme.cellColor(aCell, self.gameComponent.isPaused(), self.gameComponent.activeCharacter().lower())

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
        self.applicationContext.drawText("Next", (255, 255, 255), 22, innerArea.asRect())

    def update(self, millisecondsSinceLastUpdate, theNextSixPieces):
        self.nextSixPieces = theNextSixPieces
