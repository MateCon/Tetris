from shapes import Point


class TetrisGame:
    def __init__(self, aWidth, aHeight, aRandomizer):
        self.playfield = Playfield(aWidth, aHeight)
        self.randomizer = aRandomizer
        self.pieceGenerator = PieceGenerator(self.playfield, self.randomizer)
        self.currentPiece = self.pieceGenerator.nextPiece()

    def tick(self):
        if self.currentPiece.canMoveDown():
            self.currentPiece.moveDown()
        else:
            self.playfield.addBlocks(self.currentPiece)
            self.currentPiece = self.pieceGenerator.nextPiece()

    def asStringList(self):
        charMatrix = self.playfield.asCharMatrix()

        def callback(point):
            charMatrix[len(charMatrix) - point.y - 1][point.x] = 'x'

        self.currentPiece.do(callback)

        return [''.join(row) for row in charMatrix]


class Playfield:
    def __init__(self, aWidth, aHeight):
        self.width = aWidth
        self.height = aHeight
        self.blocks = []

        for _ in range(self.height + 2):
            currentRow = []
            for _ in range(self.width):
                currentRow.append(False)
            self.blocks.insert(0, currentRow)

    def pieceStartingPositionWithDimensions(self, someDimensions):
        return Point((self.width - someDimensions.x) // 2,
                     self.height + (2 - someDimensions.y))

    def addBlock(self, position):
        self.blocks[position.y][position.x] = True

    def hasBlockIn(self, position):
        return self.blocks[position.y][position.x]

    def addBlocks(self, currentPiece):
        currentPiece.do(lambda position: self.addBlock(position))

    def asCharMatrix(self) -> list[list[str]]:
        stringList = []

        for y in range(self.height + 2):
            currentRow = []
            for x in range(self.width):
                currentCharacter = '.'
                if y >= self.height:
                    currentCharacter = '-'
                if self.blocks[y][x]:
                    currentCharacter = 'x'
                currentRow.append(currentCharacter)
            stringList.insert(0, currentRow)

        return stringList


class Piece:
    def __init__(self, aPosition, someSquareOffsets, aPlayfield):
        self.position = aPosition
        self.squareOffsets = someSquareOffsets
        self.playfield = aPlayfield

    def includes(self, aPosition):
        for squareOffset in self.squareOffsets:
            if self.position + squareOffset == aPosition:
                return True
        return False

    def do(self, aCallback):
        for squareOffset in self.squareOffsets:
            aCallback(self.position + squareOffset)

    def allSatisfy(self, aCallback):
        for squareOffset in self.squareOffsets:
            if not aCallback(self.position + squareOffset):
                return False
        return True

    def moveDown(self):
        self.position = self.position + Point(0, -1)

    def canBlockMoveDown(self, blockPosition):
        newPosition = blockPosition + Point(0, -1)
        return newPosition.y >= 0 and not self.playfield.hasBlockIn(newPosition)

    def canMoveDown(self):
        return self.allSatisfy(self.canBlockMoveDown)


class PieceGenerator:
    def __init__(self, aPlayfield, aRandomizer):
        self.playfield = aPlayfield
        self.randomizer = aRandomizer

    def createIPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(4, 1)),
            [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)],
            self.playfield)

    def createJPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(3, 2)),
            [Point(0, 1), Point(0, 0), Point(1, 0), Point(2, 0)],
            self.playfield)

    def createLPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(3, 2)),
            [Point(2, 1), Point(0, 0), Point(1, 0), Point(2, 0)],
            self.playfield)

    def createOPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(2, 2)),
            [Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1)],
            self.playfield)

    def createSPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(3, 2)),
            [Point(0, 0), Point(1, 0), Point(1, 1), Point(2, 1)],
            self.playfield)

    def createZPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(3, 2)),
            [Point(0, 1), Point(1, 1), Point(1, 0), Point(2, 0)],
            self.playfield)

    def createTPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(3, 2)),
            [Point(0, 0), Point(1, 1), Point(1, 0), Point(2, 0)],
            self.playfield)

    def nextPiece(self):
        nextInteger = self.randomizer.nextInteger() - 1
        pieces = [
            self.createIPiece(),
            self.createJPiece(),
            self.createLPiece(),
            self.createOPiece(),
            self.createSPiece(),
            self.createZPiece(),
            self.createTPiece()
        ]
        return pieces[nextInteger]
