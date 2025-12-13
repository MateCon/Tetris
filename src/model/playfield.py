from model.cell import Cell
from model.point import Point


class Playfield:
    def __init__(self, aWidth, aHeight, anEventNotifier):
        self.width = aWidth
        self.height = aHeight
        self.blocks = []
        self.eventNotifier = anEventNotifier

        for _ in range(self.height + 2):
            currentRow = []
            for _ in range(self.width):
                currentRow.append(Cell(self))
            self.blocks.append(currentRow)

    def pieceStartingPositionWithDimensions(self, someDimensions):
        return Point((self.width - someDimensions.x) // 2, self.height)

    def pointIsInDisplayableArea(self, aPoint):
        return self.pointIsInPlayfield(aPoint) and aPoint.y < self.height + 2

    def pointIsInPlayfield(self, aPoint):
        return aPoint.x >= 0 and aPoint.x < self.width and aPoint.y >= 0

    def addBlock(self, position, piece):
        self.blocks[position.y][position.x].occupyWith(piece)

    def hasBlockIn(self, position):
        return self.pointIsInDisplayableArea(position) and self.blocks[position.y][position.x].isOccupied()

    def addBlocks(self, currentPiece):
        currentPiece.do(lambda position: self.addBlock(position, currentPiece))

    def addClearRowAtTop(self):
        newRow = []
        for _ in range(self.width):
            newRow.append(Cell(self))
        self.blocks.append(newRow)

    def findCompletedRows(self):
        def isComplete(row):
            for block in row:
                if not block.isOccupied():
                    return False
            return True

        completedRows = []
        for row in self.blocks:
            if isComplete(row):
                completedRows.append(row)

        if len(completedRows) == 1:
            self.eventNotifier.notifyRowClear()
        if len(completedRows) == 2:
            self.eventNotifier.notifyDoubleRowClear()
        if len(completedRows) == 3:
            self.eventNotifier.notifyTripleRowClear()
        if len(completedRows) == 4:
            self.eventNotifier.notifyQuadrupleRowClear()

        return completedRows

    def clearRows(self, rows):
        for row in rows:
            self.blocks.remove(row)
            self.addClearRowAtTop()

    def checkForClearedLines(self):
        self.clearRows(self.findCompletedRows())

    def asCharMatrix(self) -> list[list[str]]:
        stringList = []

        for y in range(self.height + 2):
            currentRow = []
            for x in range(self.width):
                currentCharacter = self.blocks[y][x].character(Point(x, y))
                currentRow.append(currentCharacter)
            stringList.insert(0, currentRow)

        return stringList

