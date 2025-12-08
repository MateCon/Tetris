from shapes import Point


class TetrisGame:
    def __init__(self, aWidth, aHeight, aRandomizer):
        self.playfield = Playfield(aWidth, aHeight)
        self.randomizer = aRandomizer
        self.currentPiece = PieceGenerator(self.playfield, self.randomizer).nextPiece()

    def asStringList(self):
        charMatrix = self.playfield.asCharMatrix()

        def callback(point):
            charMatrix[len(charMatrix) - point.y][point.x - 1] = 'x'

        self.currentPiece.do(callback)

        return [''.join(row) for row in charMatrix]



class Playfield:
    def __init__(self, aWidth, aHeight):
        self.width = aWidth
        self.height = aHeight

    def pieceStartingPositionWithDimensions(self, someDimensions):
        return Point((self.width - someDimensions.x) // 2,
                     self.height + (2 - someDimensions.y)).plus(Point(1, 1))

    def asCharMatrix(self) -> list[list[str]]:
        stringList = []

        for y in range(1, self.height + 2 + 1):
            currentRow = []
            for _ in range(1, self.width + 1):
                currentCharacter = '.'
                if y > self.height:
                    currentCharacter = '-'
                currentRow.append(currentCharacter)
            stringList.insert(0, currentRow)

        return stringList


class Piece:
    def __init__(self, aPosition, someSquareOffsets):
        self.position = aPosition
        self.squareOffsets = someSquareOffsets

    def includes(self, aPosition):
        for squareOffset in self.squareOffsets:
            if self.position.plus(squareOffset).equals(aPosition):
                return True
        return False

    def do(self, aCallback):
        for squareOffset in self.squareOffsets:
            aCallback(self.position.plus(squareOffset))


class PieceGenerator:
    def __init__(self, aPlayfield, aRandomizer):
        self.playfield = aPlayfield
        self.randomizer = aRandomizer

    def createIPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(4, 1)),
            [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)])

    def createJPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(3, 2)),
            [Point(0, 1), Point(0, 0), Point(1, 0), Point(2, 0)])

    def createLPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(3, 2)),
            [Point(2, 1), Point(0, 0), Point(1, 0), Point(2, 0)])

    def createOPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(2, 2)),
            [Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1)])

    def createSPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(3, 2)),
            [Point(0, 0), Point(1, 0), Point(1, 1), Point(2, 1)])

    def createZPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(3, 2)),
            [Point(0, 1), Point(1, 1), Point(1, 0), Point(2, 0)])

    def createTPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(3, 2)),
            [Point(0, 0), Point(1, 1), Point(1, 0), Point(2, 0)])

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
