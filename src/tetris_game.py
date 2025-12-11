from piece_generator import PieceGenerator
from playfield import Playfield
from point import Point


class TetrisGame:
    def __init__(self, aWidth, aHeight, aRandomizer, aRotationListGeneratorClass, aKickAlgorithmClass):
        self.playfield = Playfield(aWidth, aHeight)
        self.randomizer = aRandomizer
        self.kickAlgoritm = aKickAlgorithmClass(self.playfield)
        self.pieceGenerator = PieceGenerator(
            self.playfield,
            self.randomizer,
            aRotationListGeneratorClass(),
            self.kickAlgoritm
        )
        self.currentPiece = self.pieceGenerator.nextPiece()

    def freezeCurrentPiece(self):
        self.playfield.addBlocks(self.currentPiece)
        self.currentPiece = self.pieceGenerator.nextPiece()
        self.checkForClearedLines()

    def tick(self):
        self.softDrop()

    def moveRight(self):
        self.currentPiece.move(Point(1, 0))

    def moveLeft(self):
        self.currentPiece.move(Point(-1, 0))

    def rotateRight(self):
        self.currentPiece.rotateRight()

    def rotateLeft(self):
        self.currentPiece.rotateLeft()

    def softDrop(self):
        self.currentPiece.moveIfCantMove(Point(0, -1), self.freezeCurrentPiece)

    def hardDrop(self):
        self.currentPiece.moveIfCanMoveIfCantMove(Point(0, -1), self.hardDrop, self.freezeCurrentPiece)

    def checkForClearedLines(self):
        self.playfield.checkForClearedLines()

    def asStringList(self):
        charMatrix = self.playfield.asCharMatrix()

        def callback(point):
            if self.playfield.pointIsInDisplayableArea(point):
                charMatrix[len(charMatrix) - point.y - 1][point.x] = self.currentPiece.activeCharacter()

        self.currentPiece.do(callback)

        return [''.join(row) for row in charMatrix]

